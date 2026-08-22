#!/usr/bin/env python3
"""W-cascade in the FROZEN PREREG'S REPORTING FORM, on OWN configurations.

This is NOT the official benchmark cascade: the frozen L=7 LOW/MID configuration lists and
their exact M values are not in the repository, so this uses 16 freshly drawn L=7 N=20
configurations with their exact M computed here. It licenses nothing. It exists to show that
this implementation's error/SE scale at each W matches the recorded CPU license's scale.
"""
from __future__ import annotations
import json, time
import numpy as np
import annihil_mc as A, exact_ref_sup as E, seeds_frozen as S

L, N, NCFG = 7, 20, 16
CAP = 8_000_000
WS = (500, 2000, 10000, 1_000_000)
A.set_backend("gpu")

cand = [m for m in range(6 * L * L) if m // 6 != 0]
cfgs, exacts = [], []
for c in range(NCFG):
    rng = np.random.default_rng(770000 + c)           # own seeds, not the frozen ones
    sp = sorted(rng.choice(cand, size=N - 2, replace=False).tolist())
    try:
        ex = E.run_exact(L, sp, cap=CAP)
    except RuntimeError as e:
        print(f"cfg {c}: EXACT CAP EXCEEDED -- {e}", flush=True); continue
    cfgs.append((c, sp)); exacts.append(ex)
    print(f"cfg {c}: exact M={ex['M']:.9f} max_basis={ex['max_support']:,d} "
          f"support={ex['support_coh']:.6f}", flush=True)

print(f"\n{len(cfgs)} configurations with exact M available\n")
out = {}
for W in WS:
    errs, ses, oors, nf, nan_cfgs = [], [], [], 0, 0
    t0 = time.time()
    for (c, sp), ex in zip(cfgs, exacts):
        seeds = [S.seed_pair(L, N, c, b) for b in range(8)]
        r = A.estimate_M(L, sp, W, 8, seeds)
        nf += r.get("nonfinite_batches", 0)
        if not np.isfinite(r["M"]):
            nan_cfgs += 1
            continue
        errs.append(abs(r["M"] - ex["M"])); ses.append(r["M_se"])
        oors.append(r["raw_out_of_range_fraction"])
    errs, ses = np.array(errs), np.array(ses)
    out[W] = dict(med_err=float(np.median(errs)), p90_err=float(np.percentile(errs, 90)),
                  max_err=float(errs.max()), med_se=float(np.median(ses)),
                  p90_se=float(np.percentile(ses, 90)), max_se=float(ses.max()),
                  oor=float(np.mean(oors)), secs=time.time() - t0,
                  zero_support_batches=nf, nonreadable_configs=nan_cfgs,
                  n_configs=int(len(errs)))
    o = out[W]
    print(f"W={W:>9,d}: |err| med={o['med_err']:.5f} p90={o['p90_err']:.5f} max={o['max_err']:.5f}"
          f" | SE med={o['med_se']:.5f} p90={o['p90_se']:.5f} max={o['max_se']:.5f}"
          f" | oor={o['oor']:.4f} | zero-support batches={o['zero_support_batches']}"
          f" configs={o['n_configs']} | {o['secs']:.0f}s", flush=True)

json.dump({str(k): v for k, v in out.items()}, open("cascade_own_configs.json", "w"), indent=1)
