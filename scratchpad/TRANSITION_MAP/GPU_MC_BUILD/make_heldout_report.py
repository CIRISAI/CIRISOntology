#!/usr/bin/env python3
"""Emit the per-cell, per-configuration held-out tables under both conventions."""
from __future__ import annotations
import json, sys
import numpy as np

W = int(sys.argv[1])
CELLS = [("L7_HIGH_N31", "L=7 HIGH N=31"), ("L9_LOW_N32", "L=9 LOW N=32"),
         ("L9_MID_N42", "L=9 MID N=42"), ("L9_HIGH_N52", "L=9 HIGH N=52")]
READ = dict(med_se=0.015, p90_se=0.030, max_se=0.050, oor=0.05)


def lm(M):
    M = np.asarray(M)
    return bool(np.median(M) < 0.05 and np.mean(M < 0.05) >= 0.5)


out = []
summary = {}
for cell, label in CELLS:
    try:
        d = json.load(open(f"mc_{cell}_W{W}.json"))["results"]
    except FileNotFoundError:
        out.append(f"\n### {label} — NOT RUN\n"); continue
    out.append(f"\n### {label}\n")
    out.append("| cfg | M (raw) | SE (raw) | M (normalised) | SE (norm) | non-finite batches |")
    out.append("|---:|---:|---:|---:|---:|---:|")
    for r in d:
        out.append(f"| {r['cfg']} | {r['M_raw']:.6f} | {r['SE_raw']:.6f} | "
                   f"{r['M_norm']:.6f} | {r['SE_norm']:.6f} | {r['nonfinite_batches']} |")
    sc = {}
    for tag, name in (("raw", "RAW"), ("norm", "NORMALISED")):
        M = np.array([r[f"M_{tag}"] for r in d]); SE = np.array([r[f"SE_{tag}"] for r in d])
        oor = float(np.mean([r[f"oor_{tag}"] for r in d]))
        m = dict(med_se=float(np.median(SE)), p90_se=float(np.percentile(SE, 90)),
                 max_se=float(SE.max()), oor=oor)
        ck = {k: m[k] <= READ[k] for k in READ}
        ck["all finite"] = bool(np.isfinite(M).all() and np.isfinite(SE).all())
        readable = all(ck.values())
        sc[tag] = dict(median_M=float(np.median(M)), frac=float(np.mean(M < 0.05)),
                       low_memory=lm(M), readable=readable, metrics=m,
                       failed=[k for k, v in ck.items() if not v])
        out.append(f"\n**{name}** — median M = {np.median(M):.6f}, fraction M<0.05 = "
                   f"{np.mean(M<0.05):.4f} → **{'LOW-MEMORY' if lm(M) else 'not low-memory'}**  ")
        out.append(f"SE median {m['med_se']:.5f} (≤0.015), p90 {m['p90_se']:.5f} (≤0.030), "
                   f"max {m['max_se']:.5f} (≤0.050), out-of-range {oor:.4f} (≤0.05) → "
                   f"**{'READABLE' if readable else 'TARGET-STATISTICALLY-UNCONTROLLED'}**"
                   + ("" if readable else f" (failed: {', '.join(sc[tag]['failed'])})"))
    summary[cell] = sc

print("\n".join(out))
print("\n## Finite-size classification\n")
for tag, name in (("raw", "RAW (licensed convention)"), ("norm", "NORMALISED")):
    exl = [r[f"M_{tag}"] for r in json.load(open("exact_L7_LOW_N20.json"))["results"] if r["ok"]]
    legs = {}
    legs["L=7 LOW not low-memory (benchmark cell, exact)"] = not lm(exl)
    for cell, key in (("L7_HIGH_N31", "L=7 HIGH low-memory"),
                      ("L9_LOW_N32", "L=9 LOW not low-memory"),
                      ("L9_HIGH_N52", "L=9 HIGH low-memory")):
        if cell not in summary:
            legs[key] = None; continue
        v = summary[cell][tag]["low_memory"]
        legs[key] = (not v) if "not low-memory" in key else v
    req = ["L7_HIGH_N31", "L9_LOW_N32", "L9_HIGH_N52"]
    allread = all(summary[c][tag]["readable"] for c in req if c in summary) and \
        all(c in summary for c in req)
    supported = allread and all(v is True for v in legs.values())
    print(f"\n**{name}**\n")
    for k, v in legs.items():
        print(f"- {k}: **{v}**")
    print(f"- all required cells readable: **{allread}**")
    print(f"\n→ **{'DENSITY-SCALING-SUPPORTED' if supported else 'DENSITY-SCALING NOT SUPPORTED'}**")
