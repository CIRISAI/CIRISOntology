"""Run every generated case through rten and compare to the ONNX Runtime reference.

Two bars, because the two runtimes do not have the same output type:

* float32 scales -- ORT computes `(float)(v - zp) * scale` in f32 and stores f32.
  RTen computes the same expression. The bar is BIT-EXACT; anything else is a bug.
* float16 scales -- ORT rounds that same f32 result to f16 on the way out, while RTen
  has no f16 tensors and keeps f32. The bar is `float16(rten) == ort` EXACTLY: same
  value, one rounding. A tolerance would hide a real disagreement here, so none is used.
"""
import json, os, subprocess, sys
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
HARNESS = sys.argv[1]
cases = json.load(open(os.path.join(OUT, "cases.json")))

def read_flat(path):
    b = open(path, "rb").read()
    ndim = int(np.frombuffer(b[8:16], dtype=np.int64)[0])
    dims = np.frombuffer(b[16:16 + 8 * ndim], dtype=np.int64).tolist()
    return np.frombuffer(b[16 + 8 * ndim:], dtype=np.float32).reshape(dims)

fails, rows = [], []
for c in cases:
    name = c["name"]
    outp = os.path.join(OUT, f"{name}.out.bin")
    r = subprocess.run([HARNESS, os.path.join(OUT, f"{name}.onnx"), outp,
                        f"indices={os.path.join(OUT, name + '.indices.bin')}"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        fails.append((name, "rten failed: " + (r.stderr.strip().splitlines() or ["?"])[-1]))
        continue
    got = read_flat(outp)
    ref = np.load(os.path.join(OUT, f"{name}.ref.npy"))
    if got.shape != ref.shape:
        fails.append((name, f"shape {got.shape} vs ref {ref.shape}")); continue

    if c["scale_dtype"] == "float32":
        exact = np.array_equal(got.view(np.uint32), ref.view(np.uint32))
        bar, ok = "bit-exact f32", exact
        maxabs = float(np.max(np.abs(got - ref))) if not exact else 0.0
    else:
        got16 = got.astype(np.float16)
        exact = np.array_equal(got16.view(np.uint16), ref.view(np.uint16))
        bar, ok = "f16(rten) == ort", exact
        maxabs = float(np.max(np.abs(got16.astype(np.float32) - ref.astype(np.float32)))) if not exact else 0.0
    rows.append((name, c["bits"], c["block_size"], c["use_zp"], c["scale_dtype"],
                 str(c["data_shape"]), bar, ok, maxabs, int(got.size)))
    if not ok:
        fails.append((name, f"{bar} FAILED, max|diff| = {maxabs:g}"))

print(f"{'case':>6} {'bits':>4} {'blk':>4} {'zp':>5} {'scale':>8} {'data shape':>14} {'bar':>17} {'result':>8} {'elems':>9}")
for n, b, bs, zp, sd, ds, bar, ok, ma, ne in rows:
    print(f"{n:>6} {b:>4} {bs:>4} {str(zp):>5} {sd:>8} {ds:>14} {bar:>17} {'PASS' if ok else 'FAIL':>8} {ne:>9}")
print()
tot_el = sum(r[9] for r in rows)
print(f"{len(rows)} cases run, {tot_el:,} output elements compared")
print(f"{sum(1 for r in rows if r[7])} PASS, {len(fails)} FAIL")
for n, why in fails:
    print(f"  FAIL {n}: {why}")
sys.exit(1 if fails else 0)
