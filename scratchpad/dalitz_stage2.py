#!/usr/bin/env python3
"""Stage 2 — thresholds (blind), then the dye tests on PERMUTED data.
PREREG sections 4 and 8, order of operations steps 3-4."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import dalitz_share as ds

rng = np.random.default_rng(20260726)
d = dict(np.load("scratchpad/dalitz/kkk.npz"))
sig, side = ds.apply_windows(d, "KKK")
slow, shigh, q = d["slow"][sig], d["shigh"][sig], d["q"][sig]
N = len(slow)

# --- PREREG 4: thresholds from the CHARGE-INTEGRATED sample (blind) ---------
Xt, Yt = float(np.median(slow)), float(np.median(shigh))
x = (slow > Xt).astype(np.int64)
y = (shigh > Yt).astype(np.int64)
c = (q > 0).astype(np.int64)

res = {"N_signal": int(N), "X_threshold_MeV2": Xt, "Y_threshold_MeV2": Yt,
       "X_threshold_GeV2": Xt / 1e6, "Y_threshold_GeV2": Yt / 1e6,
       "tie_fraction_x": float(np.mean(slow == Xt)),
       "tie_fraction_y": float(np.mean(shigh == Yt)),
       "xy_cell_counts_charge_integrated":
           np.bincount(x * 2 + y, minlength=4).astype(int).tolist()}

# --- PREREG 8: dye tests on PERMUTED data ----------------------------------
cperm = c.copy(); rng.shuffle(cperm)          # charge association destroyed

base_null = ds.perm_null(x, y, cperm, 2000, rng)
res["floor"] = {"median": float(np.median(base_null)), "sd": float(np.std(base_null)),
                "p95": float(np.percentile(base_null, 95)),
                "five_sigma": float(np.median(base_null) + 5 * np.std(base_null))}

EPS = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1]


def inject(mask_weight, eps, seed):
    """Rejection-sample the c=+1 arm with weight 1+eps*w, keep integer counts."""
    r = np.random.default_rng(seed)
    w = mask_weight
    keep = np.ones(len(x), bool)
    plus = cperm == 1
    pacc = (1.0 + eps * w[plus]) / (1.0 + eps)
    keep[plus] = r.random(plus.sum()) < pacc
    return x[keep], y[keep], cperm[keep]


sgn_xy = (-1.0) ** (x + y)          # Dye A: the parity direction
sgn_x = (-1.0) ** x                 # Dye B: pure pair (function of binned x alone)
# Dye C: a narrow band in s_low lying wholly inside the x=0 cell
band_lo, band_hi = np.percentile(slow, [20, 30])
band = ((slow >= band_lo) & (slow < band_hi)).astype(float)

for name, wgt in (("A_wholeonly", sgn_xy), ("B_paironly", sgn_x), ("C_band", band)):
    rows = []
    for eps in EPS:
        vals = []
        for k in range(12):
            xx, yy, cc = inject(wgt, eps, 900 + k)
            vals.append(ds.share_2x2x2(ds.table(xx, yy, cc)))
        vals = np.array(vals)
        med, sd = res["floor"]["median"], res["floor"]["sd"]
        rows.append({"eps": eps, "share_mean": float(vals.mean()),
                     "share_sd": float(vals.std()),
                     "z_vs_floor": float((vals.mean() - med) / sd)})
    res["dye_" + name] = rows

# smallest eps recovered at 5 sigma, for Dye A
res["dyeA_5sigma_eps"] = next((r["eps"] for r in res["dye_A_wholeonly"]
                               if r["z_vs_floor"] >= 5), None)
res["dyeA_5sigma_share"] = next((r["share_mean"] for r in res["dye_A_wholeonly"]
                                 if r["z_vs_floor"] >= 5), None)
res["band_percentiles_GeV2"] = [band_lo / 1e6, band_hi / 1e6]

json.dump(res, open("scratchpad/dalitz/stage2.json", "w"), indent=1)
print(json.dumps(res, indent=1))
