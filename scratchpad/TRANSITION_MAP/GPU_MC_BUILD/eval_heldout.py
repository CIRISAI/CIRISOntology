#!/usr/bin/env python3
"""Held-out target readability + finite-size classification (E2 D4/D5), both conventions."""
from __future__ import annotations
import json, sys
import numpy as np

CELLS = ["L7_HIGH_N31", "L9_LOW_N32", "L9_MID_N42", "L9_HIGH_N52"]
READ = dict(med_se=0.015, p90_se=0.030, max_se=0.050, oor=0.05)


def low_memory(M):
    M = np.asarray(M)
    return bool(np.median(M) < 0.05 and np.mean(M < 0.05) >= 0.5)


def cell_report(cell, W, conv):
    tag = "norm" if conv == "normalised" else "raw"
    d = json.load(open(f"mc_{cell}_W{W}.json"))
    M = np.array([r[f"M_{tag}"] for r in d["results"]])
    SE = np.array([r[f"SE_{tag}"] for r in d["results"]])
    oor = np.array([r[f"oor_{tag}"] for r in d["results"]])
    finite = bool(np.isfinite(M).all() and np.isfinite(SE).all())
    m = dict(med_se=float(np.median(SE)), p90_se=float(np.percentile(SE, 90)),
             max_se=float(SE.max()), oor=float(np.mean(oor)))
    checks = {k: (m[k] <= READ[k]) for k in READ}
    checks["all finite"] = finite
    readable = all(checks.values())
    return dict(cell=cell, W=W, conv=conv, M=M.tolist(), SE=SE.tolist(),
                median_M=float(np.median(M)), frac_lt_05=float(np.mean(M < 0.05)),
                low_memory=low_memory(M), readable=readable, metrics=m, checks=checks)


if __name__ == "__main__":
    W = int(sys.argv[1])
    for conv in ("normalised", "raw"):
        print(f"\n{'='*78}\nHELD-OUT, CONVENTION: {conv.upper()}, W = {W:,d}\n{'='*78}")
        reps = {}
        for cell in CELLS:
            try:
                r = cell_report(cell, W, conv)
            except FileNotFoundError:
                print(f"{cell}: not run"); continue
            reps[cell] = r
            print(f"\n{cell}: median M={r['median_M']:.6f}  frac M<0.05={r['frac_lt_05']:.4f}"
                  f"  -> {'LOW-MEMORY' if r['low_memory'] else 'not low-memory'}")
            print(f"   SE median={r['metrics']['med_se']:.5f} p90={r['metrics']['p90_se']:.5f}"
                  f" max={r['metrics']['max_se']:.5f}  oor={r['metrics']['oor']:.4f}")
            print(f"   READABLE: {r['readable']}"
                  + ("" if r["readable"] else
                     "   -> TARGET-STATISTICALLY-UNCONTROLLED  (failed: "
                     + ", ".join(k for k, v in r["checks"].items() if not v) + ")"))
        need = ["L7_HIGH_N31", "L9_LOW_N32", "L9_HIGH_N52"]
        if all(c in reps for c in need):
            l7h, l9l, l9h = (reps[c] for c in need)
            ok = all(reps[c]["readable"] for c in need)
            # L=7 LOW is the benchmark cell; its exact classification is the L=7 LOW leg.
            # The L=7 LOW leg is not a held-out cell: it is the benchmark cell, whose exact
            # classification is known. Read it from the exact ground truth, both conventions.
            tag = "norm" if conv == "normalised" else "raw"
            exl = [r[f"M_{tag}"] for r in
                   json.load(open("exact_L7_LOW_N20.json"))["results"] if r["ok"]]
            l7low_not_lm = not low_memory(exl)
            supported = (ok and l7low_not_lm and l7h["low_memory"]
                         and (not l9l["low_memory"]) and l9h["low_memory"])
            print(f"\n   DENSITY-SCALING: {'SUPPORTED' if supported else 'NOT SUPPORTED'}")
            print(f"     L=7 LOW not low-memory  [{l7low_not_lm}]  (benchmark cell, exact)")
            print(f"     L=7 HIGH low-memory     [{l7h['low_memory']}]")
            print(f"     L=9 LOW not low-memory  [{not l9l['low_memory']}]")
            print(f"     L=9 HIGH low-memory     [{l9h['low_memory']}]")
            print(f"     all required cells readable [{ok}]")
        json.dump(reps, open(f"heldout_{conv}_W{W}.json", "w"), indent=1, default=str)
