#!/usr/bin/env python3
"""GAUGING THE CEILING-FRACTION RATIO WITH PLANTED VALUES.

The adjudication the water campaign asked for.  Its WATER_PREREG.md sec 5.4 fixes
"no ceiling fraction is compared across cells whose ceilings differ by more than
3x".  Applied to the glass ladder that PERMITS r=1.30 (ceiling swing x2.0) and
VOIDS r=1.50 (x7.2) -- and r=1.50 is where GLASS_RESULTS.md sec 2.2 reports a
trend surviving attenuation.  Two documents, two verdicts, one cell.

Per `axiomology.md` sec 5 that is settled against a case with a known answer, not
by assertion, and per this repository's own lesson (`forward-prediction-confirmed`:
GAUGE A RULER WITH PLANTED VALUES BEFORE STAKING A BAND) the way to do it is to
plant the answer and see whether the ruler returns it.

TWO QUESTIONS, and they are not the same question.

  Q1 -- DEFINITIONAL.  Is `share / ceiling` a well-defined population quantity
       that means the same thing at two cells with different ceilings?  This is
       not empirical and no threshold can bear on it: both terms are exact
       functions of the population table, and the ratio is "the fraction of the
       room available to the whole-only sector that the whole-only sector uses".
       That is the same sentence at every cell.  A ceiling-swing threshold
       therefore cannot be justified on definitional grounds, and this script
       does not test it.

  Q2 -- ESTIMATION, which is the real hazard.  At finite N, is the ESTIMATED
       ratio biased, and DOES THE BIAS DEPEND ON THE CEILING?  If a small
       ceiling systematically inflates or deflates the recovered ratio, then
       comparing ratios across a large ceiling swing compares two differently
       biased numbers, and a threshold is warranted -- at whatever swing the
       bias becomes material.  That is measurable, and it is what is measured
       here.

TWO ARMS.

  A. SYNTHETIC, fully planted: a family of 2x2x2 states in which the ceiling is
     swept over three decades while the TRUE ratio is pinned to a target by
     construction.  Recovery is scored against a value known exactly.

  B. THE REAL TABLES as their own planted populations: each of the eight glass
     cells is treated as a population whose exact share, ceiling and ratio are
     computable, then resampled at its own EFFECTIVE sample size (the raw triple
     count divided by that cell's measured overlap penalty, so the resampling
     carries the real precision rather than a flattering one).

Neither arm is a new physical measurement.  Both are gauges on a reporting
convention.
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


def ceiling(p):
    """min over the three orientations of H(pair) + H(third) - H(joint).
    `ThirdCap.lean`'s `share_le_grouping_gaps`."""
    p = np.asarray(p, dtype=float).reshape(2, 2, 2)
    p = p / p.sum()
    hp = H(p)
    return min(H(p.sum(2)) + H(p.sum((0, 1))) - hp,
               H(p.sum(1)) + H(p.sum((0, 2))) - hp,
               H(p.sum(0)) + H(p.sum((1, 2))) - hp)


SIG = GS.SIGMA


def planted_state(rho, target_ratio, tol=1e-12):
    """A state whose ceiling is set by `rho` and whose share/ceiling equals
    `target_ratio` by construction.

    Base: an exchangeable pair-correlated binary triple at marginal 1/2 with
    pair correlation `rho`, built from a symmetric pairwise Gibbs form.  Its
    ceiling rises with `rho`.  The whole-only content is then dialled in along
    the parity direction, which does not touch any pair marginal, and bisected
    until the ratio hits the target.
    """
    # exchangeable base: weight by number of agreeing pairs
    s = np.array([1.0, -1.0])
    base = np.zeros((2, 2, 2))
    for i in range(2):
        for j in range(2):
            for k in range(2):
                agree = s[i] * s[j] + s[i] * s[k] + s[j] * s[k]
                base[i, j, k] = np.exp(rho * agree)
    base /= base.sum()

    def at(d):
        q = base + d * SIG
        if q.min() <= 0:
            return None
        return q / q.sum()

    hi = min(base[SIG < 0].min(), base[SIG > 0].min()) * 0.999
    lo = 0.0
    # ratio is monotone in |d| over this range; bisect
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        q = at(mid)
        if q is None:
            hi = mid
            continue
        r = GS.share_2x2x2(q) / ceiling(q)
        if r < target_ratio:
            lo = mid
        else:
            hi = mid
        if abs(r - target_ratio) < tol:
            break
    q = at(0.5 * (lo + hi))
    return q, GS.share_2x2x2(q), ceiling(q)


def recover(p, N, ndraw, rng):
    """Resample a planted population at size N; return recovered ratios."""
    q = np.asarray(p, dtype=float).ravel()
    q = q / q.sum()
    out = np.empty(ndraw)
    for i in range(ndraw):
        c = rng.multinomial(N, q).reshape(2, 2, 2)
        cl = ceiling(c)
        out[i] = GS.share_2x2x2(c) / cl if cl > 0 else np.nan
    return out


def main():
    rng = np.random.default_rng(20260727)
    out = {}

    print("=" * 112)
    print("ARM A -- SYNTHETIC, fully planted: ceiling swept 3 decades, TRUE ratio "
          "pinned by construction")
    print("=" * 112)
    for target in (0.02, 0.20):
        print(f"\n  planted true ratio = {target:.3f}")
        print(f"  {'rho':>5s} {'ceiling':>9s} {'ceil/log2':>9s} {'true share':>11s} "
              f"{'N':>9s} {'recovered':>10s} {'bias':>9s} {'rel bias':>9s} {'sd':>9s}")
        rows = []
        for rho in (0.02, 0.05, 0.10, 0.20, 0.40, 0.80):
            p, sh, cl = planted_state(rho, target)
            true_r = sh / cl
            for N in (10 ** 5, 10 ** 6):
                r = recover(p, N, 400, rng)
                med = float(np.median(r))
                rows.append(dict(rho=rho, ceiling=cl, true_ratio=true_r,
                                 N=N, recovered=med, bias=med - true_r,
                                 rel_bias=(med - true_r) / true_r,
                                 sd=float(np.std(r))))
                print(f"  {rho:5.2f} {cl:9.5f} {cl/LOG2:9.4f} {sh:11.4e} "
                      f"{N:9.0e} {med:10.4f} {med-true_r:+9.4f} "
                      f"{100*(med-true_r)/true_r:+8.2f}% {np.std(r):9.4f}")
        out[f"synthetic_r{target}"] = rows
        cls = [r["ceiling"] for r in rows]
        rb = [abs(r["rel_bias"]) for r in rows]
        print(f"  ceiling swing over this family: {max(cls)/min(cls):.0f}x   "
              f"worst |relative bias|: {100*max(rb):.2f}%")

    print()
    print("=" * 112)
    print("ARM B -- THE EIGHT REAL GLASS CELLS as their own planted populations, "
          "resampled at EFFECTIVE N")
    print("=" * 112)
    A = json.load(open("/home/emoore/CIRISOntology/scratchpad/glass_stageA.json"))
    print(f"  {'T':6s} {'r':>5s} {'ceiling':>9s} {'true ratio':>10s} {'N_raw':>9s} "
          f"{'ovl':>5s} {'N_eff':>9s} {'recovered':>10s} {'rel bias':>9s} {'rel sd':>8s}")
    rows = []
    for t in ["1.300:1.300:1.300", "1.500:1.500:1.500"]:
        for pt in ["KA_T0.44", "KA_T0.50", "KA_T0.56", "KA_T0.64"]:
            d = A[pt]["templates"][t]["data"]
            tab = np.array(d["table"]).reshape(2, 2, 2)
            p = tab / tab.sum()
            cl = ceiling(p)
            true_r = GS.share_2x2x2(p) / cl
            ovl = d.get("overlap_penalty", 1.0)
            Neff = int(d["n_triples"] / max(ovl, 1.0))
            r = recover(p, Neff, 400, rng)
            med = float(np.median(r))
            rows.append(dict(point=pt, template=t, ceiling=cl, true_ratio=true_r,
                             N_raw=d["n_triples"], overlap=ovl, N_eff=Neff,
                             recovered=med, rel_bias=(med - true_r) / true_r,
                             rel_sd=float(np.std(r)) / true_r))
            print(f"  {pt[-4:]:6s} {t.split(':')[0]:>5s} {cl:9.5f} {true_r:10.5f} "
                  f"{d['n_triples']:9.2e} {ovl:5.1f} {Neff:9.2e} {med:10.5f} "
                  f"{100*(med-true_r)/true_r:+8.3f}% "
                  f"{100*np.std(r)/true_r:7.3f}%")
    out["real_cells"] = rows
    cls = [r["ceiling"] for r in rows]
    rb = [abs(r["rel_bias"]) for r in rows]
    print(f"\n  ceiling swing across all eight cells: {max(cls)/min(cls):.0f}x")
    print(f"  worst |relative bias| in the recovered ratio: {100*max(rb):.3f}%")
    print(f"  worst relative sd: {100*max(r['rel_sd'] for r in rows):.2f}%")

    json.dump(out, open("/home/emoore/CIRISOntology/scratchpad/glass_ratiogauge.json",
                        "w"), indent=1, default=float)
    print("\nwrote glass_ratiogauge.json")


if __name__ == "__main__":
    main()
