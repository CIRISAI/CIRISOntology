#!/usr/bin/env python3
"""CEILING FRACTIONS, against both denominators — the universal one and the sharp one.

Requested for cross-campaign comparability. Reports every headline reading as a
percentage of the machine-checked cap for three binary slots.

TWO DENOMINATORS, and the difference between them is the point.

  * `log 2` — `Core/ThirdCap.lean`'s `share_le_log_two`, proved for EVERY
    probability state on three binary slots with no hypothesis on the pair data,
    and attained exactly by the parity state (`share_max_eq_log_two`). This is
    the universal denominator every campaign divides by.

  * The SHARP, data-computable ceiling — `share_le_grouping_gaps`, the minimum
    over the three slot orientations of

        H(marg_ij) + H(marg_k) - H(p)   =   I(slot pair ; third slot).

    Every term is computable from the campaign's own table. It is never worse
    than `log 2` and can be far smaller. Flagged to this campaign by the water
    agent, whose synthetic proxies read 0.06%-17.5% of `log 2` on this bound and
    whose warning is exact: the per-orientation ceiling COLLAPSES when a label
    composition goes lopsided, and this campaign's slots are species at 80:20.

Both are reported, with the floor's own ceiling fraction beside each reading, so
that a reader can see how much of the apparent smallness is the instrument's
range rather than the substrate's structure.
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


def sharp_ceiling(tab):
    """min over the three slot orientations of H(pair) + H(third) - H(joint).

    Equals I(slot pair ; third slot) in each orientation; `ThirdCap.lean`'s
    `share_le_grouping_gaps` proves the share is below each of the three.
    """
    p = np.asarray(tab, dtype=float).reshape(2, 2, 2)
    p = p / p.sum()
    hp = H(p)
    outs = [H(p.sum(2)) + H(p.sum((0, 1))) - hp,     # (1,2) vs 3
            H(p.sum(1)) + H(p.sum((0, 2))) - hp,     # (1,3) vs 2
            H(p.sum(0)) + H(p.sum((1, 2))) - hp]     # (2,3) vs 1
    return min(outs), outs


def main():
    A = json.load(open("/home/emoore/CIRISOntology/scratchpad/glass_stageA.json"))
    B = json.load(open("/home/emoore/CIRISOntology/scratchpad/glass_stageB_paired.json"))
    pts = ["KA_T0.44", "KA_T0.50", "KA_T0.56", "KA_T0.64"]
    out = {}

    print("=" * 116)
    print("CEILING FRACTIONS -- share and floor, against log 2 and against the sharp "
          "data-computable ceiling")
    print("=" * 116)
    print(f"{'T':6s} {'r':>5s} {'share':>11s} {'floor':>10s} {'%log2':>8s} "
          f"{'floor%':>8s} {'sharp':>9s} {'sharp/log2':>10s} {'%sharp':>9s} "
          f"{'fl%sharp':>9s} {'p_B':>6s}")
    for t in ["1.300:1.300:1.300", "1.500:1.500:1.500"]:
        r = t.split(':')[0]
        for pt in pts:
            d = A[pt]["templates"][t]["data"]
            tab = np.array(d["table"]).reshape(2, 2, 2)
            p = tab / tab.sum()
            sh, orients = sharp_ceiling(tab)
            s = d["share"] - d["null_median"]          # floor already subtracted
            fl = d["null_median"]
            pB = float(p.sum((1, 2))[1])
            key = f"{pt}|{r}"
            out[key] = dict(
                share_raw=d["share"], floor=fl, share_minus_floor=s,
                pct_log2=100 * s / LOG2, floor_pct_log2=100 * fl / LOG2,
                sharp_ceiling=sh, sharp_over_log2=sh / LOG2,
                pct_sharp=100 * s / sh, floor_pct_sharp=100 * fl / sh,
                orientations=orients, p_B=pB,
                orient_spread=max(orients) - min(orients))
            o = out[key]
            print(f"{pt[-4:]:6s} {r:>5s} {d['share']:11.4e} {fl:10.3e} "
                  f"{o['pct_log2']:7.3f}% {o['floor_pct_log2']:7.4f}% "
                  f"{sh:9.4f} {o['sharp_over_log2']:9.3f}x "
                  f"{o['pct_sharp']:8.3f}% {o['floor_pct_sharp']:8.4f}% "
                  f"{pB:6.3f}")

    print()
    print("=" * 116)
    print("THE SURROGATE-SUBTRACTED EXCESS, as a ceiling fraction")
    print("=" * 116)
    for t in ["1.300:1.300:1.300", "1.500:1.500:1.500"]:
        r = t.split(':')[0]
        for pt in pts:
            if pt not in B or t not in B[pt]["templates"]:
                continue
            b = B[pt]["templates"][t]
            tab = np.array(A[pt]["templates"][t]["data"]["table"]).reshape(2, 2, 2)
            sh, _ = sharp_ceiling(tab)
            e, esd = b["excess"], b["excess_paired_sd"]
            out[f"{pt}|{r}"]["excess"] = e
            out[f"{pt}|{r}"]["excess_pct_log2"] = 100 * e / LOG2
            out[f"{pt}|{r}"]["excess_pct_sharp"] = 100 * e / sh
            print(f"{pt[-4:]:6s} r={r:>5s}  excess={e:10.3e} +- {esd:8.2e}  "
                  f"{100*e/LOG2:7.4f}% of log2   {100*e/sh:7.4f}% of sharp")

    print()
    print("=" * 116)
    print("HEADROOM vs COMPOSITION -- is the LP headroom a property of the state "
          "point rather than the template?")
    print("=" * 116)
    rows = []
    for t in sorted(A[pts[0]]["templates"].keys(), key=lambda k: float(k.split(':')[0])):
        for pt in pts:
            d = A[pt]["templates"][t]
            if d.get("empty"):
                continue
            tab = np.array(d["data"]["table"]).reshape(2, 2, 2)
            p = tab / tab.sum()
            pB = float(p.sum((1, 2))[1])
            rows.append((float(t.split(':')[0]), pt, pB, d["data"]["headroom"],
                         d["data"]["min_cell"], d["data"]["n_triples"]))
    lop = np.array([min(r[2], 1 - r[2]) for r in rows])     # lopsidedness
    head = np.array([r[3] for r in rows])
    ok = head > 0
    c = float(np.corrcoef(np.log(lop[ok]), np.log(head[ok]))[0, 1])
    print(f"  Spearman-free check: corr(log min(p_B,1-p_B), log headroom) over "
          f"{int(ok.sum())} (T, template) cells = {c:+.3f}")
    for r_ in sorted(rows, key=lambda x: x[3])[:6]:
        print(f"    r={r_[0]:5.2f} {r_[1][-4:]}  p_B={r_[2]:.4f}  "
              f"headroom={r_[3]:.4f}  min_cell={r_[4]:.0f}  N={r_[5]:.2e}")
    out["_headroom_composition_corr"] = c
    json.dump(out, open("/home/emoore/CIRISOntology/scratchpad/glass_ceiling.json", "w"),
              indent=1)
    print("\nwrote glass_ceiling.json")


if __name__ == "__main__":
    main()
