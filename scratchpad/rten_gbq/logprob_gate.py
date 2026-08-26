"""ADDENDUM A3's primary instruments, applied to the A/B payload pair.

A3 replaces accuracy+McNemar (underpowered at n=92) with:
  1. prediction agreement rate -- resolves at 1/92 = 0.011 per item;
  2. per-item logprob deviation over the four label continuations: mean and max
     |delta logprob|, and the rate at which the argmax MARGIN flips sign.

The four labels have distinct first tokens, so the label logprobs are read off a
single forward pass as log softmax over the full vocabulary restricted to those four.
REF picks are reused from the earlier run; only A and B are re-run, to save time.
"""
import json, os, subprocess, sys, time
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
EVAL = "/home/emoore/CIRISOntology/scratchpad/nl_bridge_eval"
HARNESS, MODEL_A, MODEL_B = sys.argv[1], sys.argv[2], sys.argv[3]
N_LAYERS = 28
LABELS = ["Facts", "Rules", "Identity", "Manner"]
FIRST_TOK = {"Facts": 37, "Rules": 26008, "Identity": 18558, "Manner": 44}

M = json.load(open(f"{EVAL}/surface_map.json"))
K2B, SURF = M["kind2block"], M["surface_plain"]
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


from transformers import AutoTokenizer
TOK = "/home/emoore/.cache/huggingface/hub/models--Qwen--Qwen3-0.6B/snapshots/c1899de289a04d12100db370d81485cdf75e47ca"
tok = AutoTokenizer.from_pretrained(TOK)


def ids_for(o):
    msgs = [{"role": "system", "content": SYS}, {"role": "user", "content": prompt_for(o)}]
    text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True,
                                   enable_thinking=False) + '{"family": "'
    return np.asarray(tok(text, add_special_tokens=False)["input_ids"], dtype=np.int64)[None, :]


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


def label_logprobs(model, ids):
    write_flat(f"{OUT}/g.input_ids.bin", ids, 0)
    write_flat(f"{OUT}/g.attention_mask.bin", np.ones_like(ids), 0)
    write_flat(f"{OUT}/g.position_ids.bin", np.arange(ids.shape[1], dtype=np.int64)[None, :], 0)
    args = [HARNESS, model, f"{OUT}/g.out.bin", "--only", "logits",
            f"input_ids={OUT}/g.input_ids.bin", f"attention_mask={OUT}/g.attention_mask.bin",
            f"position_ids={OUT}/g.position_ids.bin"]
    for i in range(N_LAYERS):
        args += [f"past_key_values.{i}.key={OUT}/past_empty.bin",
                 f"past_key_values.{i}.value={OUT}/past_empty.bin"]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[-300:])
    x = read_flat(f"{OUT}/g.out.bin")[0, -1].astype(np.float64)
    lse = np.log(np.exp(x - x.max()).sum()) + x.max()
    return np.array([x[FIRST_TOK[l]] - lse for l in LABELS])


items = [json.loads(l) for l in open(f"{EVAL}/test_split.jsonl")]
kept = [o for o in items if o["kind_target"] in K2B]
prev = {r["id"]: r for r in json.load(open(f"{OUT}/pred_4way.json"))}

rows, t0 = [], time.time()
for i, o in enumerate(kept, 1):
    ids = ids_for(o)
    la, lb = label_logprobs(MODEL_A, ids), label_logprobs(MODEL_B, ids)
    rows.append(dict(id=o["id"], gold=SURF[K2B[o["kind_target"]]],
                     ref=prev[o["id"]]["ref"], a=LABELS[int(la.argmax())],
                     b=LABELS[int(lb.argmax())], la=la.tolist(), lb=lb.tolist()))
    if i % 20 == 0:
        print(f"  {i}/{len(kept)}  {time.time()-t0:.0f}s", flush=True)

json.dump(rows, open(f"{OUT}/logprob_gate.json", "w"), indent=1)
n = len(rows)
la = np.array([r["la"] for r in rows]); lb = np.array([r["lb"] for r in rows])
d = np.abs(la - lb)
agree = sum(r["a"] == r["b"] for r in rows) / n
acc_a = sum(r["a"] == r["gold"] for r in rows) / n
acc_b = sum(r["b"] == r["gold"] for r in rows) / n

# Argmax margin: top label logprob minus runner-up. A sign flip means the decision
# changed, and the magnitude says how decisively.
def margin(L):
    s = np.sort(L, axis=1)
    return s[:, -1] - s[:, -2]

flips = np.array([r["a"] != r["b"] for r in rows])
print(f"\nADDENDUM A3 instruments, arms = rten fp16-embed (A) vs rten 4-bit-embed (B)")
print(f"  n = {n} frozen items, same prompt, same decoding, same runtime\n")
print(f"  1. prediction agreement rate       {agree:.4f}   ({sum(r['a']==r['b'] for r in rows)}/{n})"
      f"      criterion: >= 0.95 equivalent, < 0.90 NOT equivalent")
print(f"  2. accuracy gap                    {abs(acc_a-acc_b):.4f}   (A {acc_a:.4f}, B {acc_b:.4f})"
      f"   criterion: <= 0.03")
print(f"  3. mean per-item |delta logprob|   {d.mean():.4f}"
      f"                        criterion: <= 0.05")
print(f"     max  per-item |delta logprob|   {d.max():.4f}")
print(f"     items whose argmax flipped      {int(flips.sum())} of {n}")
if flips.any():
    print(f"     of those, A's winning margin    median {np.median(margin(la)[flips]):.4f}, "
          f"max {margin(la)[flips].max():.4f}   criterion: no flip with margin > 0.5")
    big = (margin(la) > 0.5) & flips
    print(f"     flips with A margin > 0.5       {int(big.sum())}")
verdict = ("EQUIVALENT" if (agree >= 0.95 and abs(acc_a-acc_b) <= 0.03 and d.mean() <= 0.05)
           else "NOT EQUIVALENT" if (agree < 0.90 or abs(acc_a-acc_b) > 0.06)
           else "INCONCLUSIVE AT THIS N")
print(f"\n  pre-registered verdict: {verdict}")
