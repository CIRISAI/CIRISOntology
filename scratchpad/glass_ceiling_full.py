#!/usr/bin/env python3
"""The named-denominator column for EVERY cell in the campaign.

`GATES.md`'s named-denominator gate (d520c74): "X% of ceiling" is ambiguous
unless the ceiling is NAMED. Report BOTH the universal cap (ln 2 at k=3,
machine-checked, `Core/ThirdCap.lean::share_le_log_two`, attained exactly by
parity) AND the sharp per-table ceiling (`share_le_grouping_gaps`: the minimum
over the three slot orientations of H(pair) + H(third) - H(p), which is
I(slot pair ; third slot)).

Extends `glass_ceiling.py` from the two primary templates to the whole ladder --
3D at 11 templates x 4 temperatures, the 2D replicate, and the ideal-gas control
-- because the sharp caps bound what each template COULD have carried given its
own pair entropies, and that is a number worth having even on rungs whose
readings are void.
"""
import json
import sys

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS   # noqa: E402

LOG2 = float(np.log(2.0))


def H(a):
    a = np.asarray(a, dtype=float).ravel()
    a = a[a > 0]
    return float(-np.sum(a * np.log(a)))


def sharp(tab):
    p = np.asarray(tab, dtype=float).reshape(2, 2, 2)
    p = p / p.sum()
    hp = H(p)
    o = [H(p.sum(2)) + H(p.sum((0, 1))) - hp,
         H(p.sum(1)) + H(p.sum((0, 2))) - hp,
         H(p.sum(0)) + H(p.sum((1, 2))) - hp]
    return min(o), max(o) - min(o)


def run(path, pts, label):
    A = json.load(open(f"/home/emoore/CIRISOntology/scratchpad/{path}"))
    pts = [p for p in pts if p in A]
    if not pts:
        return {}
    tmpls = sorted(A[pts[0]]["templates"].keys(), key=lambda k: float(k.split(':')[0]))
    print(f"\n{'='*118}\n{label}\n{'='*118}")
    print(f"{'r':>6s} {'point':>7s} {'share-floor':>12s} {'%log2':>9s} "
          f"{'sharp cap':>10s} {'cap/log2':>9s} {'%sharp':>9s} "
          f"{'orient sprd':>11s} {'floor%sharp':>11s}")
    res = {}
    for t in tmpls:
        for pt in pts:
            d = A[pt]["templates"][t]
            if d.get("empty"):
                continue
            d = d["data"]
            tab = np.array(d["table"]).reshape(2, 2, 2)
            if tab.sum() == 0:
                continue
            cap, spread = sharp(tab)
            s = d["share"] - d["null_median"]
            fl = d["null_median"]
            res[f"{pt}|{t.split(':')[0]}"] = dict(
                share_minus_floor=s, pct_log2=100 * s / LOG2, sharp_cap=cap,
                cap_over_log2=cap / LOG2,
                pct_sharp=(100 * s / cap) if cap > 0 else float('nan'),
                floor_pct_sharp=(100 * fl / cap) if cap > 0 else float('nan'),
                orientation_spread=spread, n_triples=d["n_triples"])
            r = res[f"{pt}|{t.split(':')[0]}"]
            print(f"{t.split(':')[0]:>6s} {pt.split('_')[-1]:>7s} {s:12.4e} "
                  f"{r['pct_log2']:8.4f}% {cap:10.5f} {cap/LOG2:8.4f}x "
                  f"{r['pct_sharp']:8.3f}% {spread:11.2e} "
                  f"{r['floor_pct_sharp']:10.4f}%")
    return res


if __name__ == "__main__":
    out = {}
    out["KA3D"] = run("glass_stageA.json",
                      ["KA_T0.44", "KA_T0.50", "KA_T0.56", "KA_T0.64"],
                      "3D KOB-ANDERSEN -- full ladder, both denominators named")
    out["ideal"] = run("glass_stageA.json", ["SYNTH_ideal"],
                       "IDEAL-GAS CONTROL -- both denominators named")
    out["KA2D"] = run("glass_stage2d.json", ["KA2D_T0.23", "KA2D_T0.30"],
                      "2D TERNARY REPLICATE -- both denominators named")
    caps = [v["sharp_cap"] for g in out.values() for v in g.values()]
    sprd = [v["orientation_spread"] for g in out.values() for v in g.values()]
    print(f"\nsharp cap range over all {len(caps)} cells: "
          f"{min(caps):.2e} to {max(caps):.4f} nats "
          f"({min(caps)/LOG2:.5f}x to {max(caps)/LOG2:.4f}x of log 2) "
          f"-- a spread of {max(caps)/min(caps):.0f}x")
    print(f"worst orientation spread (template symmetrisation check): {max(sprd):.2e}")
    json.dump(out, open("/home/emoore/CIRISOntology/scratchpad/glass_ceiling_full.json",
                        "w"), indent=1)
    print("\nwrote glass_ceiling_full.json")
