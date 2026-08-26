"""Rank agreement, not just logit distance.

What matters downstream is whether the CHOSEN token changes, and when the ranking
shifts, how far. Distance in logit space can be large while the ordering is intact,
and small while the top two swap. So this reports:

  * Spearman rho over the FULL 151,936-dim logit vector, per position -- does the
    whole ordering survive;
  * the rank each payload assigns to the token the unquantised reference ranked
    first -- when the argmax changes, does the reference's choice fall to rank 2 or
    to rank 500? That distinction is the difference between a harmless reshuffle at
    the top and real damage;
  * top-1 and top-5, repeated here so all the rank measures sit together.

Reported for BOTH payloads against the reference, because the baseline is not exact
either and the increment is the quantity of interest.
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
        raise RuntimeError(f"{tag} on {name}: {r.stderr.strip()[-300:]}")
    x = read_flat(outp).copy()
    os.remove(outp)
    return x


import torch
from transformers import AutoModelForCausalLM
TOK = "/home/emoore/.cache/huggingface/hub/models--Qwen--Qwen3-0.6B/snapshots/c1899de289a04d12100db370d81485cdf75e47ca"
print("loading unquantised reference...", flush=True)
ref_model = AutoModelForCausalLM.from_pretrained(TOK, dtype=torch.float32).eval()


def ids_of(name):
    b = open(os.path.join(OUT, f"{name}.input_ids.bin"), "rb").read()
    ndim = int(np.frombuffer(b[8:16], dtype=np.int64)[0])
    dims = np.frombuffer(b[16:16 + 8 * ndim], dtype=np.int64).tolist()
    return np.frombuffer(b[16 + 8 * ndim:], dtype=np.int64).reshape(dims)


def ranks_of(x):
    """Dense 0-based ranks, descending (rank 0 = largest)."""
    order = np.argsort(-x, kind="stable")
    r = np.empty_like(order)
    r[order] = np.arange(len(x))
    return r


# Full-vocab rho is dominated by the enormous tail of near-tied, never-sampled
# tokens, whose ordering is noise. rho100 restricts to the reference's top 100 --
# the only region a sampler ever draws from -- and is the decision-relevant one.
rho = {"a": [], "b": []}
rho100 = {"a": [], "b": []}
top1rank = {"a": [], "b": []}
t1 = {"a": 0, "b": 0}
n = 0

for p in prompts:
    name = p["name"]
    A, B = run_rten(MODEL_A, name, "A"), run_rten(MODEL_B, name, "B")
    with torch.no_grad():
        R = ref_model(torch.from_numpy(ids_of(name).copy())).logits.numpy().astype(np.float32)
    r, a, b = R[0], A[0], B[0]
    for i in range(r.shape[0]):
        rr = ranks_of(r[i]).astype(np.float64)
        best = int(r[i].argmax())
        top100 = np.argpartition(-r[i], 100)[:100]
        rr100 = ranks_of(r[i][top100]).astype(np.float64)
        for key, x in (("a", a[i]), ("b", b[i])):
            rx_full = ranks_of(x)
            rho[key].append(float(np.corrcoef(rr, rx_full.astype(np.float64))[0, 1]))
            rho100[key].append(float(np.corrcoef(rr100, ranks_of(x[top100]).astype(np.float64))[0, 1]))
            top1rank[key].append(int(rx_full[best]))
            t1[key] += int(x.argmax() == best)
        n += 1
    print(f"  {name} done ({n} positions)", flush=True)

print(f"\nrank agreement with the unquantised reference, {n} positions, "
      f"full {r.shape[1]:,}-token vocabulary")
print(f"{'measure':<52} {'A fp16 embed':>14} {'B 4-bit embed':>15}")
print(f"{'Spearman rho over the full logit vector (mean)':<52} "
      f"{np.mean(rho['a']):>14.5f} {np.mean(rho['b']):>15.5f}")
print(f"{'Spearman rho (5th percentile over positions)':<52} "
      f"{np.percentile(rho['a'],5):>14.5f} {np.percentile(rho['b'],5):>15.5f}")
print(f"{'Spearman rho over the reference top-100 (mean)':<52} "
      f"{np.mean(rho100['a']):>14.5f} {np.mean(rho100['b']):>15.5f}")
print(f"{'Spearman rho top-100 (5th percentile)':<52} "
      f"{np.percentile(rho100['a'],5):>14.5f} {np.percentile(rho100['b'],5):>15.5f}")
print(f"{'top-1 agreement (argmax unchanged)':<52} "
      f"{t1['a']/n:>14.4f} {t1['b']/n:>15.4f}")
print()
print("rank the payload gives to the token the REFERENCE ranked first")
print(f"{'  (0 = still first, so lower is better)':<52} {'A':>14} {'B':>15}")
for q, lab in [(50, "median"), (90, "90th pct"), (99, "99th pct"), (100, "worst")]:
    fa = np.percentile(top1rank['a'], q); fb = np.percentile(top1rank['b'], q)
    print(f"{'  ' + lab:<52} {fa:>14.0f} {fb:>15.0f}")
for thr in (1, 2, 5, 10):
    pa = np.mean(np.array(top1rank['a']) < thr); pb = np.mean(np.array(top1rank['b']) < thr)
    print(f"{'  reference top-1 still in payload top-' + str(thr):<52} "
          f"{pa:>14.4f} {pb:>15.4f}")
json.dump({"rho_a": float(np.mean(rho['a'])), "rho_b": float(np.mean(rho['b'])),
           "rho100_a": float(np.mean(rho100['a'])), "rho100_b": float(np.mean(rho100['b'])),
           "top1rank_a": top1rank['a'], "top1rank_b": top1rank['b']},
          open(os.path.join(OUT, "rankcorr.json"), "w"))
