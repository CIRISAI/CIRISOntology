#!/usr/bin/env python3
"""Apply the frozen benchmark gates (E2 D4) under BOTH declared conventions."""
from __future__ import annotations
import json, sys
import numpy as np

CELLS = ["L7_LOW_N20", "L7_MID_N25"]
GATES = dict(med_err=0.010, p90_err=0.020, max_err=0.050,
             med_se=0.010, p90_se=0.020, max_se=0.050, oor=0.05)


def low_memory(M):
    """median M < 0.05 AND at least 50% of configurations have M < 0.05."""
    M = np.asarray(M)
    return bool(np.median(M) < 0.05 and np.mean(M < 0.05) >= 0.5)


def evaluate(W, conv):
    tag = "norm" if conv == "normalised" else "raw"
    errs, ses, oors, cls, exact_cls = [], [], [], {}, {}
    for cell in CELLS:
        ex = {r["cfg"]: r for r in json.load(open(f"exact_{cell}.json"))["results"] if r["ok"]}
        mc = json.load(open(f"mc_{cell}_W{W}.json"))["results"]
        Mmc, Mex = [], []
        for r in mc:
            e = ex.get(r["cfg"])
            if e is None:
                continue
            m_mc, m_ex = r[f"M_{tag}"], e[f"M_{tag}"]
            Mmc.append(m_mc); Mex.append(m_ex)
            errs.append(abs(m_mc - m_ex)); ses.append(r[f"SE_{tag}"])
            oors.append(r[f"oor_{tag}"])
        cls[cell] = low_memory(Mmc); exact_cls[cell] = low_memory(Mex)
    errs, ses = np.array(errs), np.array(ses)
    m = dict(med_err=float(np.median(errs)), p90_err=float(np.percentile(errs, 90)),
             max_err=float(errs.max()), med_se=float(np.median(ses)),
             p90_se=float(np.percentile(ses, 90)), max_se=float(ses.max()),
             oor=float(np.mean(oors)))
    checks = {k: (m[k] <= GATES[k]) for k in GATES}
    checks["LOW not low-memory"] = (cls["L7_LOW_N20"] is False)
    checks["MID low-memory"] = (cls["L7_MID_N25"] is True)
    return m, checks, cls, exact_cls


if __name__ == "__main__":
    Ws = [int(w) for w in sys.argv[1:]]
    for conv in ("normalised", "raw"):
        print(f"\n{'='*78}\nCONVENTION: {conv.upper()}\n{'='*78}")
        for W in Ws:
            try:
                m, checks, cls, ecls = evaluate(W, conv)
            except FileNotFoundError as e:
                print(f"W={W:,d}: not yet run ({e.filename})"); continue
            verdict = "PASS" if all(checks.values()) else "FAIL"
            print(f"\nW = {W:,d}   ->  {verdict}")
            for k in ("med_err", "p90_err", "max_err", "med_se", "p90_se", "max_se", "oor"):
                print(f"   {k:9s} = {m[k]:.5f}   gate <= {GATES[k]:.3f}   "
                      f"{'pass' if checks[k] else 'FAIL'}")
            for k in ("LOW not low-memory", "MID low-memory"):
                print(f"   {k:22s}      {'pass' if checks[k] else 'FAIL'}")
            print(f"   MC classification: LOW={'low-mem' if cls['L7_LOW_N20'] else 'not low-mem'}"
                  f", MID={'low-mem' if cls['L7_MID_N25'] else 'not low-mem'}")
            print(f"   EXACT classification: LOW={'low-mem' if ecls['L7_LOW_N20'] else 'not low-mem'}"
                  f", MID={'low-mem' if ecls['L7_MID_N25'] else 'not low-mem'}")
