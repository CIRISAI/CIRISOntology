#!/usr/bin/env python3
"""Exact-model verification: the MC estimator must converge to the exact witness as W grows,
and its reported standard error must be calibrated (z-scores ~ N(0,1))."""
from __future__ import annotations
import json, sys, time
import numpy as np
import annihil_mc as A, exact_ref_sup as E, seeds_frozen as S

BACKEND = sys.argv[1] if len(sys.argv) > 1 else "cpu"
A.set_backend(BACKEND)
CASES = [(3, 5, 4), (5, 8, 4), (7, 12, 3)]
WS = (500, 2000, 10000)

rows = []
for L, N, ncfg in CASES:
    cand = [m for m in range(6 * L * L) if m // 6 != 0]
    for c in range(ncfg):
        rng = np.random.default_rng(31337 + 101 * L + 7 * N + c)
        sp = sorted(rng.choice(cand, size=N - 2, replace=False).tolist())
        ex = E.run_exact(L, sp)
        for W in WS:
            t = time.time()
            seeds = [S.seed_pair(L, N, c, b) for b in range(8)]
            r = A.estimate_M(L, sp, W, 8, seeds)
            err = r["M"] - ex["M"]
            z = err / r["M_se"] if r["M_se"] > 0 else float("nan")
            rows.append(dict(L=L, N=N, cfg=c, W=W, M_exact=ex["M"], M_mc=r["M"],
                             se=r["M_se"], err=err, z=z,
                             oor=r["raw_out_of_range_fraction"],
                             uniq=r["mean_unique_configs"], secs=time.time() - t))
            print(f"L={L} N={N} c={c} W={W:>6d}: exact={ex['M']:.6f} mc={r['M']:.6f} "
                  f"err={err:+.6f} se={r['se'] if 'se' in r else r['M_se']:.6f} z={z:+.2f} "
                  f"t={rows[-1]['secs']:.1f}s", flush=True)

json.dump(rows, open(f"verify_exact_{BACKEND}.json", "w"), indent=1)
for W in WS:
    e = np.array([abs(r["err"]) for r in rows if r["W"] == W])
    z = np.array([r["z"] for r in rows if r["W"] == W])
    print(f"\nW={W}: median|err|={np.median(e):.6f} max|err|={e.max():.6f} "
          f"mean z={z.mean():+.2f} sd z={z.std(ddof=1):.2f} max|z|={np.abs(z).max():.2f}")
allz = np.array([r["z"] for r in rows])
print(f"\nALL: mean z={allz.mean():+.3f} sd z={allz.std(ddof=1):.3f} "
      f"(calibrated SE => mean 0, sd 1); n={len(allz)}")
