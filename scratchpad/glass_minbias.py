#!/usr/bin/env python3
"""MIN-OF-THREE SELECTION BIAS in the sharp ceiling -- checked on this campaign's
own tables, because it lands on numbers already published.

The water campaign's finding: `share_le_grouping_gaps` supplies THREE
per-orientation ceilings and both campaigns quote their MINIMUM.  The minimum of
three NOISY estimates is biased downward by O(their sd) = O(N^-1/2) -- a
selection bias, not a plug-in bias -- and it is WORST when the three true values
coincide, because then the min of three noisy copies is pure downward selection.

GLASS_RESULTS.md sec 2.2b asserted the opposite: that this campaign's full
symmetrisation over the template's permutations makes the three orientations
coincide (worst spread 1.5e-5 nats), and therefore "the min is not doing any
hidden work here".  That is exactly the maximal-bias configuration.  Checked
here rather than conceded, because the three orientation estimates come from ONE
table and are correlated, which damps the selection bias by an amount only a
measurement can supply.

A downward-biased ceiling inflates every "% of sharp" quoted against it -- the
flattering direction, which is the one that matters.
"""
import json
import sys

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS   # noqa: E402


def H(a):
    a = np.asarray(a, dtype=float).ravel()
    a = a[a > 0]
    return float(-np.sum(a * np.log(a)))


def orients(tab):
    p = np.asarray(tab, dtype=float).reshape(2, 2, 2)
    p = p / p.sum()
    hp = H(p)
    return np.array([H(p.sum(2)) + H(p.sum((0, 1))) - hp,
                     H(p.sum(1)) + H(p.sum((0, 2))) - hp,
                     H(p.sum(0)) + H(p.sum((1, 2))) - hp])


def main():
    A = json.load(open("/home/emoore/CIRISOntology/scratchpad/glass_stageA.json"))
    R = {r["point"] + "|" + r["template"].split(':')[0]: r
         for r in json.load(open(
             "/home/emoore/CIRISOntology/scratchpad/glass_ratiogauge.json"))["real_cells"]}
    rng = np.random.default_rng(31337)
    ND = 600
    print("=" * 124)
    print("MIN vs MEAN of the three orientation ceilings, resampled at each cell's "
          "own effective N")
    print("=" * 124)
    print(f"{'cell':>16s} {'N_eff':>9s} {'true spread':>12s} {'true ceil':>10s} "
          f"{'min bias':>9s} {'mean bias':>10s} {'%sharp min':>11s} "
          f"{'%sharp mean':>12s} {'shift':>8s}")
    out = {}
    for t in ["1.300:1.300:1.300", "1.500:1.500:1.500"]:
        for pt in ["KA_T0.44", "KA_T0.50", "KA_T0.56", "KA_T0.64"]:
            d = A[pt]["templates"][t]["data"]
            tab = np.array(d["table"]).reshape(2, 2, 2)
            p = tab / tab.sum()
            o = orients(p)
            true_min, true_mean = o.min(), o.mean()
            key = pt + "|" + t.split(':')[0]
            Neff = R[key]["N_eff"]
            mn, mu = np.empty(ND), np.empty(ND)
            q = p.ravel()
            for i in range(ND):
                c = rng.multinomial(Neff, q).reshape(2, 2, 2)
                oo = orients(c)
                mn[i], mu[i] = oo.min(), oo.mean()
            bmin = (np.median(mn) - true_min) / true_min
            bmean = (np.median(mu) - true_mean) / true_mean
            share = d["share"] - d["null_median"]
            pm, pM = 100 * share / true_min, 100 * share / true_mean
            out[key] = dict(true_spread=float(o.max() - o.min()),
                            true_min=float(true_min), true_mean=float(true_mean),
                            bias_min=float(bmin), bias_mean=float(bmean),
                            pct_sharp_min=float(pm), pct_sharp_mean=float(pM))
            print(f"{pt[-4:]+' r='+t.split(':')[0]:>16s} {Neff:9.2e} "
                  f"{o.max()-o.min():12.2e} {true_min:10.5f} "
                  f"{100*bmin:+8.3f}% {100*bmean:+9.3f}% {pm:10.3f}% "
                  f"{pM:11.3f}% {100*(pM-pm)/pm:+7.2f}%")
    print()
    print("  'true spread' is max-min over the three orientations of the POPULATION "
          "table.")
    print("  'shift' is how much the quoted ceiling fraction moves if the mean is "
          "used instead of the min.")
    json.dump(out, open("/home/emoore/CIRISOntology/scratchpad/glass_minbias.json",
                        "w"), indent=1)
    print("\nwrote glass_minbias.json")


if __name__ == "__main__":
    main()
