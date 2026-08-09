"""Stage 2 — the floor model and G10 closure on DR1 BGS mocks. THE GO/NO-GO.

Runs at the one cell Stage 1 left admissible: R = 10, b = 4 (occupancy 186 > 100).
R = 15 is dead at every b and is not attempted. Both are pre-registered scales.

SUITE. AbacusSummit only, and that is a Stage-2 finding rather than a choice:
  - AbacusSummit bright/v1 (25 N-body realizations) ships BGS_BRIGHT — matching the
    S0-A sample at 0.968 of its in-shell count on the identical footprint.
  - EZmock bright/v1 (1000) ships BGS_ffa, whose count matches BGS_BRIGHT-21.5 to
    0.27% over the identical z span. It models the sample S0-A did NOT choose, and is
    therefore unusable as a floor model here.
  => RULE S2-B (cross-suite sigma closure) is NOT RUNNABLE on this sample. Recorded as
     not-runnable, never as passed. sigma from 25 draws carries +/-14% from ensemble
     size alone (1/sqrt(2(n-1))), which the prereg itself flags as BOSS's weakest habit.

The randoms are the DATA randoms, reused across mocks: the mock footprint matches the
data's to <0.1 deg in RA and DEC, and the mocks are built on the survey geometry. The
random field is therefore painted ONCE and shared, which is both correct and the only
way 25 realizations fit in the compute budget.

Estimator, grid, smoothing, binning, IPF and LP all imported unchanged from
sky_realdata.py per prereg §11.
"""

from __future__ import annotations

import gc
import glob
import json
import sys

import numpy as np
from astropy.io import fits

import sky_bgs_io as io
from sky_realdata import (SurveyGrid, density_and_mask, masked_smooth,
                          quantile_labels, triple_hist, connected_info, configs)

R = 10.0
B = 4
CELL = 6.0
RANDOMS = (0, 1, 2, 3)


def _mock_positions(path: str):
    with fits.open(path, memmap=True) as h:
        d = h[1].data
        z = np.asarray(d["Z"], dtype=np.float64)
        k = (z >= io.Z_LO) & (z <= io.Z_HI)
        ra = np.asarray(d["RA"], dtype=np.float64)[k]
        dec = np.asarray(d["DEC"], dtype=np.float64)[k]
        w = np.asarray(d["WEIGHT"], dtype=np.float64)[k]
        zz = z[k]
    from sky_realdata import sky_to_cart
    return sky_to_cart(ra, dec, zz), w


def measure_one(g, n_ran, pos, w):
    """One realization -> the R=10, b=4 reading. Same path the data would take."""
    n_g = g.deposit(pos, w)
    delta, mask, alpha, _ = density_and_mask(g, n_g, n_ran)
    del n_g
    sm, ok = masked_smooth(g, delta, mask, R)
    del delta, mask
    n_indep = float(ok.sum()) * g.cell ** 3 / ((2 * np.pi) ** 1.5 * R ** 3)
    occ = n_indep / B ** 3
    lab, _ = quantile_labels(sm, ok, B)
    sigma = float(sm[ok].std())
    del sm
    stride = max(1, int(round(R / g.cell / 3)))
    out = {"alpha": float(alpha), "n_indep": n_indep, "occupancy": occ,
           "occupancy_pass": bool(occ > 100.0), "sigma": sigma, "configs": {}}
    for name, orients in configs(R, g.cell, 1.5).items():
        hs = np.zeros((B, B, B)); ntot = 0
        for (d1, d2) in orients:
            h, nt = triple_hist(lab, ok, d1, d2, B, stride)
            hs += h; ntot += nt
        ci = connected_info(hs)
        ci["n_triples"] = int(ntot)
        out["configs"][name] = {k: float(v) if isinstance(v, (int, float, np.floating)) else v
                                for k, v in ci.items()}
    del lab, ok
    gc.collect()
    return out


def main():
    paths = sorted(glob.glob("desi_bgs/mocks/ab_*.fits"))
    if not paths:
        print("no mocks on disk", file=sys.stderr); return 1
    print(f"[stage2] {len(paths)} AbacusSummit realizations, R={R}, b={B}", flush=True)

    pos_r, w_r = io.load_randoms(RANDOMS)
    g = SurveyGrid(pos_r, cell=CELL)
    n_ran = g.deposit(pos_r, w_r)
    del pos_r, w_r
    gc.collect()
    print(f"[stage2] grid {g.N}; randoms painted once and shared", flush=True)

    rows = []
    for p in paths:
        pos, w = _mock_positions(p)
        r = measure_one(g, n_ran, pos, w)
        r["mock"] = p
        r["n_gal"] = int(len(pos))
        del pos, w
        gc.collect()
        rows.append(r)
        eq = r["configs"].get("equilateral", {})
        print(f"[stage2] {p}: n={r['n_gal']:,} occ={r['occupancy']:.1f} "
              f"share={eq.get('share', float('nan')):.6e}", flush=True)

    # --- RULE S2-A: per-realisation scatter against 3% of the floor mean ---
    s2a = {}
    for name in rows[0]["configs"]:
        v = np.array([r["configs"][name]["I"] for r in rows], dtype=float)
        mean, sd = float(v.mean()), float(v.std(ddof=1))
        s2a[name] = {"n": len(v), "mean": mean, "sd": sd,
                     "scatter_frac_of_mean": float(sd / mean) if mean else None,
                     "s2a_pass": bool(mean and sd / mean <= 0.03),
                     "sigma_ensemble_err": float(1.0 / np.sqrt(2 * (len(v) - 1))),
                     "max_cert": float(max(r["configs"][name]["cert"] for r in rows)),
                     "g9_pass": bool(max(r["configs"][name]["cert"] for r in rows) < 1e-9)}

    res = {"stage": 2, "R": R, "b": B, "suite": "AbacusSummit bright/v1",
           "n_realizations": len(rows),
           "s2b_cross_suite": "NOT RUNNABLE — EZmock models BGS_BRIGHT-21.5, not the S0-A sample",
           "rule_s2a": s2a, "rows": rows}
    with open("desi_bgs/stage2_scatter.json", "w") as f:
        json.dump(res, f, indent=1, default=float)
    print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1, default=float))
    return 0


if __name__ == "__main__":
    sys.exit(main())
