"""Where do the top-1 disagreements fall?

A pooled top-1 agreement of ~0.75 looks alarming until you ask WHICH positions
disagree. If the flips are at positions where the unquantised model is itself
near-indifferent between candidates, they cost little; if they are at confident
positions, they are real damage. This buckets every position by the reference
model's own confidence (its max softmax probability) and reports agreement within
each bucket, for the baseline AND the new payload, so the two are read side by side.

Also decodes a short greedy continuation from each of the three models as a sanity
check that the whole pipeline is sane rather than plausibly-wrong.
"""
import json, os, subprocess, sys
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
HARNESS, MODEL_A, MODEL_B = sys.argv[1], sys.argv[2], sys.argv[3]
N_LAYERS = 28
prompts = json.load(open(os.path.join(OUT, "prompts.json")))


def read_flat(path):
    b = open(path, "rb").read()
    ndim = int(np.frombuffer(b[8:16], dtype=np.int64)[0])
    dims = np.frombuffer(b[16:16 + 8 * ndim], dtype=np.int64).tolist()
    return np.frombuffer(b[16 + 8 * ndim:], dtype=np.float32).reshape(dims)


def run_rten(model, name, tag):
    outp = os.path.join(OUT, f"{name}.{tag}.bin")
    args = [HARNESS, model, outp, "--only", "logits",
            f"input_ids={OUT}/{name}.input_ids.bin",
            f"attention_mask={OUT}/{name}.attention_mask.bin",
            f"position_ids={OUT}/{name}.position_ids.bin"]
    for i in range(N_LAYERS):
        args += [f"past_key_values.{i}.key={OUT}/past_empty.bin",
                 f"past_key_values.{i}.value={OUT}/past_empty.bin"]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{tag} failed on {name}: {r.stderr.strip()[-300:]}")
    x = read_flat(outp).copy()
    os.remove(outp)
    return x


import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
TOK = "/home/emoore/.cache/huggingface/hub/models--Qwen--Qwen3-0.6B/snapshots/c1899de289a04d12100db370d81485cdf75e47ca"
print("loading unquantised reference...", flush=True)
ref_model = AutoModelForCausalLM.from_pretrained(TOK, dtype=torch.float32).eval()
tok = AutoTokenizer.from_pretrained(TOK)


def ids_of(name):
    b = open(os.path.join(OUT, f"{name}.input_ids.bin"), "rb").read()
    ndim = int(np.frombuffer(b[8:16], dtype=np.int64)[0])
    dims = np.frombuffer(b[16:16 + 8 * ndim], dtype=np.int64).tolist()
    return np.frombuffer(b[16 + 8 * ndim:], dtype=np.int64).reshape(dims)


EDGES = [0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 1.01]
buckets = {i: dict(n=0, a=0, b=0, ab=0) for i in range(len(EDGES) - 1)}

for p in prompts:
    name = p["name"]
    A, B = run_rten(MODEL_A, name, "A"), run_rten(MODEL_B, name, "B")
    with torch.no_grad():
        R = ref_model(torch.from_numpy(ids_of(name).copy())).logits.numpy().astype(np.float32)
    r = R[0]
    e = np.exp(r - r.max(-1, keepdims=True), dtype=np.float64)
    conf = (e / e.sum(-1, keepdims=True)).max(-1)
    tr, ta, tb = r.argmax(-1), A[0].argmax(-1), B[0].argmax(-1)
    idx = np.clip(np.digitize(conf, EDGES) - 1, 0, len(EDGES) - 2)
    for k in range(len(EDGES) - 1):
        m = idx == k
        buckets[k]["n"] += int(m.sum())
        buckets[k]["a"] += int((ta[m] == tr[m]).sum())
        buckets[k]["b"] += int((tb[m] == tr[m]).sum())
        buckets[k]["ab"] += int((ta[m] == tb[m]).sum())
    print(f"  {name} done", flush=True)

print("\ntop-1 agreement with the unquantised reference, by the REFERENCE's own confidence")
print(f"{'ref max prob':>16} {'positions':>10} {'share':>7} {'A fp16 embed':>14} {'B 4-bit embed':>15} {'B vs A':>9}")
tot = sum(v["n"] for v in buckets.values())
for k in range(len(EDGES) - 1):
    v = buckets[k]
    if v["n"] == 0:
        continue
    hi = "1.00" if EDGES[k + 1] > 1 else f"{EDGES[k+1]:.2f}"
    print(f"  [{EDGES[k]:.2f}, {hi}) {v['n']:>10} {v['n']/tot:>6.1%} "
          f"{v['a']/v['n']:>14.4f} {v['b']/v['n']:>15.4f} {v['ab']/v['n']:>9.4f}")

# --- generation sanity check
print("\ngreedy continuation from the same prompt (32 tokens), as a sanity check:")
name = prompts[0]["name"]
ids = ids_of(name)[:, :48]


def greedy_rten(model, ids, n=32):
    cur = ids.copy()
    for _ in range(n):
        for arr, tag, fn in [(cur, "input_ids", 0), (np.ones_like(cur), "attention_mask", 0),
                             (np.arange(cur.shape[1])[None, :], "position_ids", 0)]:
            with open(os.path.join(OUT, f"tmp.{tag}.bin"), "wb") as f:
                a = np.ascontiguousarray(arr.astype(np.int64))
                f.write(np.int64(0).tobytes()); f.write(np.int64(a.ndim).tobytes())
                f.write(np.asarray(a.shape, dtype=np.int64).tobytes()); f.write(a.tobytes())
        args = [HARNESS, model, f"{OUT}/tmp.out.bin", "--only", "logits",
                f"input_ids={OUT}/tmp.input_ids.bin",
                f"attention_mask={OUT}/tmp.attention_mask.bin",
                f"position_ids={OUT}/tmp.position_ids.bin"]
        for i in range(N_LAYERS):
            args += [f"past_key_values.{i}.key={OUT}/past_empty.bin",
                     f"past_key_values.{i}.value={OUT}/past_empty.bin"]
        subprocess.run(args, capture_output=True, check=True)
        nxt = int(read_flat(f"{OUT}/tmp.out.bin")[0, -1].argmax())
        cur = np.concatenate([cur, [[nxt]]], axis=1)
    return cur[0, ids.shape[1]:]


with torch.no_grad():
    ref_out = ref_model.generate(torch.from_numpy(ids.copy()), max_new_tokens=32,
                                 do_sample=False, pad_token_id=tok.eos_token_id)
print("  REF:", repr(tok.decode(ref_out[0, ids.shape[1]:])))
print("  A  :", repr(tok.decode(greedy_rten(MODEL_A, ids))))
print("  B  :", repr(tok.decode(greedy_rten(MODEL_B, ids))))
