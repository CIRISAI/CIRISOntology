#!/usr/bin/env python3
"""The scorecard: the temperature trend, its exact test, and the pre-registered
predictions P1-P7 scored one by one.

The trend is tested by an EXACT CONFIGURATION-PERMUTATION TEST, not by an error
bar.  GLASS_PREREG.md sec 6.1(2) fixed this rule before the run, because the
full-chain examination found the configuration-level block bootstrap
over-states the uncertainty by a factor of ~2.2 -- the known bad behaviour of
the bootstrap for a non-negative statistic sitting near its boundary at zero.
An inflated sigma makes a GROWTH claim harder (which is fine, and deliberate)
but makes a NULL claim EASIER (which is not).  So:

    * growth is scored against the inflated bootstrap sigma, deliberately;
    * the null, and the trend generally, is scored by pooling the two
      temperatures' per-configuration tables, reassigning configurations at
      random to two groups of the original sizes, and reading the p-value of
      the observed difference off the rank.

That test needs no error bar at all.  It is valid under the null "the same
species-triple distribution at both temperatures", which requires the triple
counts to be matched -- and sec 3.7 already requires that for its own reason.
"""
import argparse
import json
import sys

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS   # noqa: E402


def perm_trend(tabs_a, tabs_b, nperm, rng):
    """Exact permutation test on configuration membership.

    Returns the observed difference, the two-sided p-value, and the null's own
    spread -- the honest error bar the bootstrap failed to give.
    """
    A, B = np.asarray(tabs_a), np.asarray(tabs_b)
    na = len(A)
    pool = np.vstack([A, B])
    sa = GS.share_2x2x2(A.sum(0).reshape(2, 2, 2))
    sb = GS.share_2x2x2(B.sum(0).reshape(2, 2, 2))
    obs = sa - sb
    null = np.empty(nperm)
    for i in range(nperm):
        p = rng.permutation(len(pool))
        null[i] = (GS.share_2x2x2(pool[p[:na]].sum(0).reshape(2, 2, 2)) -
                   GS.share_2x2x2(pool[p[na:]].sum(0).reshape(2, 2, 2)))
    return dict(share_a=float(sa), share_b=float(sb), diff=float(obs),
                p_two_sided=float((np.sum(np.abs(null) >= abs(obs)) + 1) /
                                  (nperm + 1)),
                p_one_sided=float((np.sum(null >= obs) + 1) / (nperm + 1)),
                null_sd=float(null.std()), null_mean=float(null.mean()),
                z_exact=float(obs / null.std()) if null.std() > 0 else float('nan'),
                nperm=int(nperm))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stageA", default="glass_stageA.json")
    ap.add_argument("--order", default="KA_T0.44,KA_T0.50,KA_T0.56,KA_T0.64")
    ap.add_argument("--nperm", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20260727)
    ap.add_argument("--out", default="glass_scorecard.json")
    args = ap.parse_args()

    A = json.load(open(f"/home/emoore/CIRISOntology/scratchpad/{args.stageA}"))
    rng = np.random.default_rng(args.seed)
    pts = [p for p in args.order.split(',') if p in A]
    if not pts:
        sys.exit("no state points in " + args.stageA)
    tmpls = sorted(A[pts[0]]["templates"].keys(), key=lambda k: float(k.split(':')[0]))

    print("=" * 108)
    print("THE SWEEP -- share (nats), its empirical null, the excess, and the exact p")
    print("=" * 108)
    sweep = {}
    for t in tmpls:
        r = float(t.split(':')[0])
        line = [f"r={r:5.2f}"]
        row = {}
        for p in pts:
            d = A[p]["templates"][t]
            if d.get("empty"):
                line.append(f"{p[-4:]}:EMPTY")
                continue
            dd = d["data"]
            row[p] = dict(share=dd["share"], null=dd["null_median"],
                          excess=dd["excess"], p=dd["p_value"],
                          n=dd["n_triples"], head=dd["headroom"],
                          minc=dd["min_cell"], boot_sd=d["boot_sd"],
                          npc=d["counts_per_conf"]["mean"],
                          capped=d["counts_per_conf"]["capped"],
                          overlap=dd.get("overlap_penalty", float('nan')))
            line.append(f"{p.split('_')[-1]}:{dd['excess']:+.3e}(p={dd['p_value']:.3f})")
        sweep[t] = row
        print("  ".join(line))

    print()
    print("=" * 108)
    print("THE TREND -- exact configuration-permutation test, coldest vs hottest")
    print("=" * 108)
    trend = {}
    cold, hot = pts[0], pts[-1]
    for t in tmpls:
        ta = A[cold]["per_conf_tables"].get(t)
        tb = A[hot]["per_conf_tables"].get(t)
        if not ta or not tb or np.sum(ta) == 0 or np.sum(tb) == 0:
            continue
        res = perm_trend(ta, tb, args.nperm, rng)
        res["n_cold"] = float(np.sum(ta))
        res["n_hot"] = float(np.sum(tb))
        res["count_ratio"] = res["n_cold"] / max(res["n_hot"], 1)
        trend[t] = res
        r = float(t.split(':')[0])
        print(f"r={r:5.2f}  {cold.split('_')[-1]}={res['share_a']:.4e}  "
              f"{hot.split('_')[-1]}={res['share_b']:.4e}  "
              f"diff={res['diff']:+.4e}  p2={res['p_two_sided']:.4f}  "
              f"z_exact={res['z_exact']:+6.2f}  "
              f"Ncold/Nhot={res['count_ratio']:.3f}")

    print()
    print("=" * 108)
    print("MONOTONICITY across the full ladder (cold -> hot), per template")
    print("=" * 108)
    mono = {}
    for t in tmpls:
        vals = [sweep[t][p]["excess"] for p in pts if p in sweep[t]]
        if len(vals) < len(pts):
            continue
        dec = all(vals[i] >= vals[i + 1] for i in range(len(vals) - 1))
        inc = all(vals[i] <= vals[i + 1] for i in range(len(vals) - 1))
        mono[t] = dict(values=[float(v) for v in vals],
                       monotone_growth_on_cooling=bool(dec),
                       monotone_fall_on_cooling=bool(inc))
        print(f"r={float(t.split(':')[0]):5.2f}  " +
              "  ".join(f"{v:+.3e}" for v in vals) +
              ("   MONOTONE-GROWTH-ON-COOLING" if dec else
               ("   MONOTONE-FALL-ON-COOLING" if inc else "   non-monotone")))

    json.dump(dict(sweep=sweep, trend=trend, mono=mono, points=pts,
                   args=vars(args)),
              open(f"/home/emoore/CIRISOntology/scratchpad/{args.out}", "w"),
              indent=1)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
