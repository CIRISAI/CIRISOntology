"""Three-way logit comparison on real prompts.

  REF  unquantised Qwen3-0.6B in PyTorch float32  -- the ground truth
  A    rten, 569.8 MB: 4-bit matmuls, fp16 embedding  -- the payload that works today
  B    rten, 346.1 MB: 4-bit matmuls, 4-bit embedding -- the payload under test

A vs B alone would only say how far the two payloads are apart. It would not say
whether that distance MATTERS, because the baseline is not itself exact -- it already
quantises all 196 matmul weights to 4 bits. So both are measured against REF, and the
question becomes: does swapping the embedding to 4 bits add error comparable to the
error the project has ALREADY accepted? That yardstick is the point of including REF.

Reported per prompt and pooled:
  * max and RMS logit difference, and the same relative to the logit spread
  * top-1 agreement -- the decision the decode loop actually makes
  * top-5 set agreement
  * KL(softmax REF || softmax X) -- distributional, not just the argmax
Deterministic runs, so a self-comparison of A against A is the zero floor and is
reported as a control.
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
        raise RuntimeError(f"{tag} failed on {name}: {r.stderr.strip()[-400:]}")
    x = read_flat(outp).copy()
    os.remove(outp)
    return x


def softmax(x):
    x = x - x.max(axis=-1, keepdims=True)
    e = np.exp(x, dtype=np.float64)
    return e / e.sum(axis=-1, keepdims=True)


def kl(p, q):
    q = np.clip(q, 1e-30, None)
    p = np.clip(p, 1e-30, None)
    return float(np.mean(np.sum(p * np.log(p / q), axis=-1)))


# ---- reference: unquantised PyTorch
import torch
from transformers import AutoModelForCausalLM
TOK = "/home/emoore/.cache/huggingface/hub/models--Qwen--Qwen3-0.6B/snapshots/c1899de289a04d12100db370d81485cdf75e47ca"
print("loading unquantised reference (PyTorch float32)...", flush=True)
ref_model = AutoModelForCausalLM.from_pretrained(TOK, dtype=torch.float32).eval()


def run_ref(name):
    b = open(os.path.join(OUT, f"{name}.input_ids.bin"), "rb").read()
    ndim = int(np.frombuffer(b[8:16], dtype=np.int64)[0])
    dims = np.frombuffer(b[16:16 + 8 * ndim], dtype=np.int64).tolist()
    ids = np.frombuffer(b[16 + 8 * ndim:], dtype=np.int64).reshape(dims)
    with torch.no_grad():
        return ref_model(torch.from_numpy(ids.copy())).logits.numpy().astype(np.float32)


rows = []
pool = dict(a_top1=0, b_top1=0, ab_top1=0, n=0, a_top5=0, b_top5=0,
            a_se=0.0, b_se=0.0, ab_se=0.0, cnt=0,
            a_max=0.0, b_max=0.0, ab_max=0.0, spread=0.0)
control_checked = False

for p in prompts:
    name = p["name"]
    A = run_rten(MODEL_A, name, "A")
    B = run_rten(MODEL_B, name, "B")
    R = run_ref(name)
    assert A.shape == B.shape == R.shape, (A.shape, B.shape, R.shape)

    if not control_checked:
        A2 = run_rten(MODEL_A, name, "A2")
        assert np.array_equal(A.view(np.uint32), A2.view(np.uint32)), \
            "control failed: two runs of the SAME model differ"
        print("control: two runs of model A are bit-identical -> the floor is exactly 0")
        control_checked = True

    a, b, r = A[0], B[0], R[0]
    spread = float(np.mean(r.max(axis=-1) - np.percentile(r, 1, axis=-1)))
    ra, rb, rab = a - r, b - r, b - a
    ta, tb, tr = a.argmax(-1), b.argmax(-1), r.argmax(-1)
    top5r = np.argpartition(-r, 5, axis=-1)[:, :5]
    top5a = np.argpartition(-a, 5, axis=-1)[:, :5]
    top5b = np.argpartition(-b, 5, axis=-1)[:, :5]
    ov_a = np.mean([len(set(x) & set(y)) for x, y in zip(top5r, top5a)]) / 5
    ov_b = np.mean([len(set(x) & set(y)) for x, y in zip(top5r, top5b)]) / 5

    n = a.shape[0]
    pool["n"] += n
    pool["a_top1"] += int((ta == tr).sum())
    pool["b_top1"] += int((tb == tr).sum())
    pool["ab_top1"] += int((ta == tb).sum())
    pool["a_top5"] += ov_a * n
    pool["b_top5"] += ov_b * n
    pool["a_se"] += float((ra ** 2).sum()); pool["b_se"] += float((rb ** 2).sum())
    pool["ab_se"] += float((rab ** 2).sum()); pool["cnt"] += ra.size
    pool["a_max"] = max(pool["a_max"], float(np.abs(ra).max()))
    pool["b_max"] = max(pool["b_max"], float(np.abs(rb).max()))
    pool["ab_max"] = max(pool["ab_max"], float(np.abs(rab).max()))
    pool["spread"] += spread * n

    sr, sa, sb = softmax(r), softmax(a), softmax(b)
    rows.append((name, p["tokens"],
                 float(np.sqrt((ra ** 2).mean())), float(np.sqrt((rb ** 2).mean())),
                 float((ta == tr).mean()), float((tb == tr).mean()),
                 kl(sr, sa), kl(sr, sb)))
    print(f"  {name} ({p['tokens']:3d} tok)  rmsA={rows[-1][2]:.4f} rmsB={rows[-1][3]:.4f} "
          f"top1A={rows[-1][4]:.3f} top1B={rows[-1][5]:.3f} "
          f"klA={rows[-1][6]:.5f} klB={rows[-1][7]:.5f}", flush=True)

n = pool["n"]
print("\n" + "=" * 78)
print(f"POOLED over {len(prompts)} real prompts, {n} token positions, "
      f"{pool['cnt']:,} logits per model")
print(f"  mean logit spread (max - 1st pct) per position: {pool['spread']/n:.2f}")
print()
print(f"{'quantity':<44} {'A: fp16 embed':>15} {'B: 4-bit embed':>16}")
print(f"{'RMS logit error vs unquantised reference':<44} "
      f"{np.sqrt(pool['a_se']/pool['cnt']):>15.4f} {np.sqrt(pool['b_se']/pool['cnt']):>16.4f}")
print(f"{'max |logit error| vs reference':<44} {pool['a_max']:>15.4f} {pool['b_max']:>16.4f}")
print(f"{'top-1 agreement with reference':<44} "
      f"{pool['a_top1']/n:>15.4f} {pool['b_top1']/n:>16.4f}")
print(f"{'top-5 overlap with reference':<44} "
      f"{pool['a_top5']/n:>15.4f} {pool['b_top5']/n:>16.4f}")
print()
print(f"  B vs A directly: RMS {np.sqrt(pool['ab_se']/pool['cnt']):.4f}, "
      f"max {pool['ab_max']:.4f}, top-1 agreement {pool['ab_top1']/n:.4f}")
print(f"  ratio of RMS error B/A: {np.sqrt(pool['b_se']/pool['a_se']):.3f}x")
json.dump(rows, open(os.path.join(OUT, "per_prompt.json"), "w"), indent=1)
