#!/usr/bin/env python3
"""Stage 3 — PREREG 7b (flat phase space) and 7c (efficiency immunity).
Both run before the real charge labels are used."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import dalitz_share as ds

rng = np.random.default_rng(2718281)
M_B, M_K = ds.M_B, ds.M_K
C = M_B ** 2 + 3 * M_K ** 2
out = {}

# --- 7b: flat phase space, generated here so the truth is known exactly -----
def flat_dalitz(n, rng):
    lo, hi = (2 * M_K) ** 2, (M_B - M_K) ** 2
    keep_ac, keep_bc = [], []
    while sum(len(a) for a in keep_ac) < n:
        sac = rng.uniform(lo, hi, 4 * n)
        sbc = rng.uniform(lo, hi, 4 * n)
        sab = C - sac - sbc
        r = np.sqrt(sac)
        Ea = r / 2.0
        Eb = (M_B ** 2 - sac - M_K ** 2) / (2 * r)
        ok = (sac > lo) & (Eb > M_K)
        pa = np.sqrt(np.clip(Ea ** 2 - M_K ** 2, 0, None))
        pb = np.sqrt(np.clip(Eb ** 2 - M_K ** 2, 0, None))
        smax = (Ea + Eb) ** 2 - (pa - pb) ** 2
        smin = (Ea + Eb) ** 2 - (pa + pb) ** 2
        ok &= (sab > smin) & (sab < smax)
        keep_ac.append(sac[ok]); keep_bc.append(sbc[ok])
    sac = np.concatenate(keep_ac)[:n]; sbc = np.concatenate(keep_bc)[:n]
    return np.minimum(sac, sbc), np.maximum(sac, sbc)


N = 13537
frac_plus = 0.5
slow_f, shigh_f = flat_dalitz(N, rng)
xf = (slow_f > np.median(slow_f)).astype(np.int64)
yf = (shigh_f > np.median(shigh_f)).astype(np.int64)
cf = (rng.random(N) < frac_plus).astype(np.int64)
obs_f = ds.share_2x2x2(ds.table(xf, yf, cf))
null_f = ds.perm_null(xf, yf, cf.copy(), 20000, rng)
out["flat_phase_space"] = ds.significance(obs_f, null_f)
out["flat_phase_space"]["xy_cells"] = np.bincount(xf * 2 + yf, minlength=4).tolist()
out["flat_phase_space"]["N"] = N

# --- 7c: efficiency immunity.  Severe CHARGE-SYMMETRIC acceptance ----------
d = dict(np.load("scratchpad/dalitz/kkk.npz"))
sig, _ = ds.apply_windows(d, "KKK")
slow, shigh, q = d["slow"][sig], d["shigh"][sig], d["q"][sig]
x = (slow > np.median(slow)).astype(np.int64)
y = (shigh > np.median(shigh)).astype(np.int64)
c = (q > 0).astype(np.int64)

u = (slow - slow.min()) / (slow.max() - slow.min())
v = (shigh - shigh.min()) / (shigh.max() - shigh.min())
eff = np.exp(np.log(5.0) * (0.5 * u + 0.5 * v))      # factor 5 across the plane
eff /= eff.max()
out["efficiency_map"] = {"min": float(eff.min()), "max": float(eff.max()),
                         "ratio": float(eff.max() / eff.min())}

vals, keptN = [], []
for b in range(60):
    cp = c.copy(); rng.shuffle(cp)                    # charge association destroyed
    keep = rng.random(len(x)) < eff                   # SAME map for both charges
    vals.append(ds.share_2x2x2(ds.table(x[keep], y[keep], cp[keep])))
    keptN.append(int(keep.sum()))
vals = np.array(vals)
s2b = json.load(open("scratchpad/dalitz/stage2b.json"))
out["efficiency_immunity"] = {
    "share_mean": float(vals.mean()), "share_sem": float(vals.std() / np.sqrt(len(vals))),
    "floor_median": s2b["floor_median"], "floor_sd": s2b["floor_sd"],
    "z_vs_floor": float((vals.mean() - s2b["floor_median"]) / s2b["floor_sd"]),
    "mean_kept": float(np.mean(keptN)),
    "frac_above_5sig": float(np.mean(vals > s2b["five_sigma_share"]))}

json.dump(out, open("scratchpad/dalitz/stage3.json", "w"), indent=1)
print(json.dumps(out, indent=1))
