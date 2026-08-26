"""The NL_BRIDGE 4-way surface eval, run through the ONNX payloads.

Task-level agreement, which is what actually decides whether ~346 MB ships. The
original eval (run_eval4.py) drove Ollama with a JSON grammar; that decoding path is
not available here, so this reproduces it faithfully rather than identically:

  * same 92 items, same system prompt, same family glosses, same truncation;
  * the assistant turn is opened with `{"family": "` so the model is answering the
    same question in the same shape;
  * the four labels have DISTINCT first tokens -- F(37), Rules(26008),
    Identity(18558), M(44) -- so taking the argmax over those four logits is exactly
    what greedy grammar-constrained decoding would emit, in one forward pass.

Because the decoding path differs from Ollama's, the ABSOLUTE score need not
reproduce the published 0.467. What is comparable is the three models against each
other on this one harness, so the unquantised reference is run too and is the control.
"""
import json, os, subprocess, sys, time
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
EVAL = "/home/emoore/CIRISOntology/scratchpad/nl_bridge_eval"
HARNESS, MODEL_A, MODEL_B = sys.argv[1], sys.argv[2], sys.argv[3]
LIMIT = int(sys.argv[4]) if len(sys.argv) > 4 else 0
N_LAYERS = 28

M = json.load(open(f"{EVAL}/surface_map.json"))
K2B, SURF = M["kind2block"], M["surface_plain"]
LABELS = ["Facts", "Rules", "Identity", "Manner"]
FIRST_TOK = {"Facts": 37, "Rules": 26008, "Identity": 18558, "Manner": 44}

FAM = [
    ("Facts",    "the assertive family: what is claimed, how strongly, under what rule, on what premise"),
    ("Rules",    "the directive family: what is required, in what preference order, in what step order"),
    ("Identity", "the declarative family: what counts as what"),
    ("Manner",   "the force-neutral carrier family: how it is encoded, how it is presented or registered, which instance it is"),
]
MENU = "\n".join(f"- {n}: {g}" for n, g in FAM)
SYS = ("You classify what FAMILY of change was made to a document. "
       "Answer with exactly one label from this list:\n"
       f"{MENU}\n"
       "Pick the single family the change belongs to.")


def trunc(s, n=1400):
    s = s or ""
    return s if len(s) <= n else s[:n] + "\n[...truncated]"


def prompt_for(o):
    return (f"BEFORE:\n{trunc(o['before'])}\n\nAFTER:\n{trunc(o['after'])}\n\n"
            f"WHAT CHANGED: {o.get('variation_site','')}\n\nWhich family of change is this?")


from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
TOK = "/home/emoore/.cache/huggingface/hub/models--Qwen--Qwen3-0.6B/snapshots/c1899de289a04d12100db370d81485cdf75e47ca"
tok = AutoTokenizer.from_pretrained(TOK)
print("loading unquantised reference (PyTorch float32)...", flush=True)
ref_model = AutoModelForCausalLM.from_pretrained(TOK, dtype=torch.float32).eval()


def ids_for(o):
    msgs = [{"role": "system", "content": SYS},
            {"role": "user", "content": prompt_for(o)}]
    text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True,
                                   enable_thinking=False)
    text += '{"family": "'
    return np.asarray(tok(text, add_special_tokens=False)["input_ids"],
                      dtype=np.int64)[None, :]


def write_flat(path, arr, tag):
    with open(path, "wb") as f:
        f.write(np.int64(tag).tobytes()); f.write(np.int64(arr.ndim).tobytes())
        f.write(np.asarray(arr.shape, dtype=np.int64).tobytes())
        f.write(np.ascontiguousarray(arr).tobytes())


write_flat(f"{OUT}/past_empty.bin", np.zeros((1, 8, 0, 128), dtype=np.float32), 1)


def read_flat(path):
    b = open(path, "rb").read()
    ndim = int(np.frombuffer(b[8:16], dtype=np.int64)[0])
    dims = np.frombuffer(b[16:16 + 8 * ndim], dtype=np.int64).tolist()
    return np.frombuffer(b[16 + 8 * ndim:], dtype=np.float32).reshape(dims)


def last_logits_rten(model, ids):
    write_flat(f"{OUT}/t.input_ids.bin", ids, 0)
    write_flat(f"{OUT}/t.attention_mask.bin", np.ones_like(ids), 0)
    write_flat(f"{OUT}/t.position_ids.bin", np.arange(ids.shape[1], dtype=np.int64)[None, :], 0)
    args = [HARNESS, model, f"{OUT}/t.out.bin", "--only", "logits",
            f"input_ids={OUT}/t.input_ids.bin",
            f"attention_mask={OUT}/t.attention_mask.bin",
            f"position_ids={OUT}/t.position_ids.bin"]
    for i in range(N_LAYERS):
        args += [f"past_key_values.{i}.key={OUT}/past_empty.bin",
                 f"past_key_values.{i}.value={OUT}/past_empty.bin"]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[-300:])
    return read_flat(f"{OUT}/t.out.bin")[0, -1].copy()


def pick(logits):
    scores = {lab: float(logits[FIRST_TOK[lab]]) for lab in LABELS}
    return max(scores, key=scores.get), scores


items = [json.loads(l) for l in open(f"{EVAL}/test_split.jsonl")]
kept = [o for o in items if o["kind_target"] in K2B]
print(f"items={len(items)} scored={len(kept)} dropped_Record={len(items)-len(kept)}", flush=True)
if LIMIT:
    kept = kept[:LIMIT]
    print(f"  LIMIT active: only {len(kept)} of them", flush=True)

rows = []
t0 = time.time()
for i, o in enumerate(kept, 1):
    ids = ids_for(o)
    with torch.no_grad():
        lr = ref_model(torch.from_numpy(ids.copy())).logits[0, -1].numpy()
    pr, _ = pick(lr)
    pa, _ = pick(last_logits_rten(MODEL_A, ids))
    pb, _ = pick(last_logits_rten(MODEL_B, ids))
    rows.append(dict(id=o["id"], tokens=int(ids.shape[1]),
                     gold=SURF[K2B[o["kind_target"]]], ref=pr, a=pa, b=pb))
    if i % 10 == 0:
        print(f"  {i}/{len(kept)}  {time.time()-t0:.0f}s", flush=True)

json.dump(rows, open(f"{OUT}/pred_4way.json", "w"), indent=1)


def acc(key):
    return sum(r[key] == r["gold"] for r in rows) / len(rows)


def agree(k1, k2):
    return sum(r[k1] == r[k2] for r in rows) / len(rows)


n = len(rows)
print(f"\n4-way surface eval, {n} items, mean prompt {np.mean([r['tokens'] for r in rows]):.0f} tokens")
print(f"{'model':<34} {'top1_4way':>10} {'k':>5}")
for key, label in [("ref", "unquantised reference (fp32)"),
                   ("a", "A  rten 569.8 MB fp16 embed"),
                   ("b", "B  rten 346.1 MB 4-bit embed")]:
    k = sum(r[key] == r["gold"] for r in rows)
    print(f"{label:<34} {acc(key):>10.4f} {k:>5}")
print(f"\nbaselines: uniform 0.250, majority-class 0.370, GRIP threshold 0.453, STRONG 0.500")
print(f"\npairwise label agreement (same prompt, same harness):")
print(f"  B vs A   {agree('a','b'):.4f}   ({sum(r['a']==r['b'] for r in rows)}/{n})")
print(f"  A vs REF {agree('ref','a'):.4f}")
print(f"  B vs REF {agree('ref','b'):.4f}")

# McNemar on the A/B discordant pairs -- is B measurably worse at the TASK?
b_only = sum((r["b"] == r["gold"]) and (r["a"] != r["gold"]) for r in rows)
a_only = sum((r["a"] == r["gold"]) and (r["b"] != r["gold"]) for r in rows)
print(f"\nMcNemar A vs B: A-only-correct {a_only}, B-only-correct {b_only}")
if a_only + b_only:
    from math import comb
    m, tot = min(a_only, b_only), a_only + b_only
    p = sum(comb(tot, i) for i in range(m + 1)) * 2 / 2 ** tot
    print(f"  exact two-sided p = {min(p,1.0):.4f}")
else:
    print("  no discordant pairs")

for key, label in [("ref", "REF"), ("a", "A"), ("b", "B")]:
    from collections import Counter
    print(f"  {label} label distribution: {dict(Counter(r[key] for r in rows))}")
