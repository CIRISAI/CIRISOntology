#!/usr/bin/env python3
"""Exact ground truth for the E2 benchmark cells (L=7 LOW N=20, MID N=25).

Stores the RAW q vectors so both declared witness conventions (E2 D2) are available without
recomputation.
"""
from __future__ import annotations
import json, sys, time
import numpy as np
import annihil_mc as A, exact_gpu as G

A.set_backend("gpu")
CAP = 60_000_000
ROW_BUDGET = 8_000_000

cell = sys.argv[1]
blob = json.load(open(f"configs/{cell}.json"))
L, N = blob["L"], blob["N"]
out = []
for c, sp in enumerate(blob["configs"]):
    t = time.time()
    try:
        r = G.run_exact(L, sp, cap=CAP, row_budget=ROW_BUDGET)
    except RuntimeError as e:
        print(f"{cell} cfg {c:2d}: EXACT-CAP-EXCEEDED  {e}", flush=True)
        out.append(dict(cfg=c, ok=False, error=str(e)))
        continue
    w = G.witnesses(r["q_coh"], r["q_deph"])
    out.append(dict(cfg=c, ok=True, q_coh=r["q_coh"].tolist(), q_deph=r["q_deph"].tolist(),
                    M_norm=w["M_norm"], M_raw=w["M_raw"],
                    support_coh=w["support_coh"], support_deph=w["support_deph"],
                    norm_coh=r["norm_coh"], max_support=r["max_support"],
                    secs=time.time() - t))
    print(f"{cell} cfg {c:2d}: M_norm={w['M_norm']:.9f} M_raw={w['M_raw']:.9f} "
          f"support={w['support_coh']:.6f} maxbasis={r['max_support']:,d} "
          f"norm={r['norm_coh']:.12f} t={time.time()-t:.1f}s", flush=True)

json.dump(dict(cell=cell, L=L, N=N, cap=CAP, row_budget=ROW_BUDGET, results=out),
          open(f"exact_{cell}.json", "w"), indent=1)
ok = [o for o in out if o["ok"]]
if ok:
    mn = np.array([o["M_norm"] for o in ok]); mr = np.array([o["M_raw"] for o in ok])
    print(f"\n{cell}: {len(ok)}/16 exact. NORMALISED median={np.median(mn):.6f} "
          f"frac<0.05={np.mean(mn<0.05):.4f} | RAW median={np.median(mr):.6f} "
          f"frac<0.05={np.mean(mr<0.05):.4f}")
