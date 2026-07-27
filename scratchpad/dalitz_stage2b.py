#!/usr/bin/env python3
"""Stage 2b — Dye A refined.

The stage-2 dye test used ONE fixed permutation as its base, so the injected
parity component first cancelled that realisation's own random parity
fluctuation before growing.  That is a defect in my dye test, not in the data:
it is why the stage-2 Dye A curve dips below the floor at eps = 0.01-0.02.
Fixed here by averaging over many independent base permutations, and the grid is
refined to locate the 5-sigma sensitivity properly.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import dalitz_share as ds

rng = np.random.default_rng(31415926)
d = dict(np.load("scratchpad/dalitz/kkk.npz"))
sig, _ = ds.apply_windows(d, "KKK")
slow, shigh, q = d["slow"][sig], d["shigh"][sig], d["q"][sig]
Xt, Yt = float(np.median(slow)), float(np.median(shigh))
x = (slow > Xt).astype(np.int64)
y = (shigh > Yt).astype(np.int64)
c0 = (q > 0).astype(np.int64)
sgn_xy = (-1.0) ** (x + y)
sgn_x = (-1.0) ** x

NBASE, NPERM = 60, 20000
floor = ds.perm_null(x, y, c0.copy(), NPERM, rng)
fmed, fsd = float(np.median(floor)), float(np.std(floor))
out = {"floor_median": fmed, "floor_sd": fsd, "n_perm_floor": NPERM,
       "five_sigma_share": fmed + 5 * fsd}

for name, w in (("A_wholeonly", sgn_xy), ("B_paironly", sgn_x)):
    rows = []
    for eps in [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.10, 0.15, 0.20]:
        vals = []
        for b in range(NBASE):
            cp = c0.copy(); rng.shuffle(cp)
            keep = np.ones(len(x), bool)
            plus = cp == 1
            pacc = (1.0 + eps * w[plus]) / (1.0 + eps)
            keep[plus] = rng.random(plus.sum()) < pacc
            vals.append(ds.share_2x2x2(ds.table(x[keep], y[keep], cp[keep])))
        v = np.array(vals)
        rows.append({"eps": eps, "share_mean": float(v.mean()),
                     "share_sem": float(v.std() / np.sqrt(NBASE)),
                     "z_vs_floor": float((v.mean() - fmed) / fsd),
                     "frac_above_5sig": float(np.mean(v > fmed + 5 * fsd))})
    out["dye_" + name] = rows

# the pre-registered deliverable: smallest eps recovered at 5 sigma
a = out["dye_A_wholeonly"]
out["dyeA_5sigma_eps"] = next((r["eps"] for r in a if r["z_vs_floor"] >= 5), None)
out["dyeA_5sigma_share"] = next((r["share_mean"] for r in a if r["z_vs_floor"] >= 5), None)
out["dyeA_median_detect_eps"] = next((r["eps"] for r in a if r["frac_above_5sig"] >= 0.5), None)
json.dump(out, open("scratchpad/dalitz/stage2b.json", "w"), indent=1)

print("floor median %.4e  sd %.4e   5-sigma bar %.4e" % (fmed, fsd, fmed + 5 * fsd))
for name in ("A_wholeonly", "B_paironly"):
    print("\nDYE " + name)
    for r in out["dye_" + name]:
        print("  eps=%-5g share=%.4e +- %.1e   z=%8.2f   P(>5sig)=%.2f"
              % (r["eps"], r["share_mean"], r["share_sem"], r["z_vs_floor"], r["frac_above_5sig"]))
print("\n5-sigma eps (mean-based):", out["dyeA_5sigma_eps"],
      " share:", out["dyeA_5sigma_share"])
print("eps at which a MEDIAN run clears 5 sigma:", out["dyeA_median_detect_eps"])
