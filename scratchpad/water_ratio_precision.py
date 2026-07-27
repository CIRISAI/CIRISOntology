#!/usr/bin/env python3
"""WATER_AMENDMENT_3: what a CEILING FRACTION costs in bias and in variance.

OCCASION.  The glass campaign adjudicated this campaign's 3x ceiling-ratio
comparability rule against planted values (glass_ratiogauge.py, GLASS_RESULTS.md
sec 2.2a) and found it targets the wrong variable: the bias in a recovered
ceiling fraction tracks the CEILING and N, not the ceiling SWING, and falls as
0.2275/(N*share).  It proposed a replacement rule with a measured basis, and
attached a caveat cutting against itself -- its worst cell carries a 29.6%
relative sd on the ratio, "harmless against a 490% effect, fatal against a 50%
one."

WHY THIS SCRIPT.  This campaign's expected effects are NOT 490%.  Its design
sensitivity is 3e-5 nats against ceilings of order 0.07 nats -- a ceiling
fraction of ~0.04%.  So glass's caveat is the binding constraint here, not its
headline, and the question this script answers is: at THIS campaign's budgeted
sample size, what are the bias and the variance of a ceiling fraction?

WHAT IT DOES.  Builds tables of EXACTLY known share by moving along the parity
direction from a product model -- the one free direction of the pair envelope,
so the true share is computed on the exact distribution, not estimated.  Then
multinomial-samples at N and measures the estimator's relative bias and relative
sd against the two closed forms:

    relative bias of the share (hence of any ceiling fraction) ~ floor / share
                                                               = 0.2275/(N*share)
    relative sd   ~ sqrt(2 + 8*N*share) / (2*N*share)

the second following from var(chi2_1 with noncentrality 2N*share) = 2 + 8N*share.

Reads no water and no configuration of any kind.
"""
import sys

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS  # noqa: E402

SIGMA = GS.SIGMA


def planted(p1, delta):
    """Product model at composition p1, pushed along the parity direction.

    The pair marginals are unchanged by the shift (sum_k SIGMA[i,j,k] = 0), so
    the whole-only share of the result is carried entirely by `delta` and is
    computed exactly on the distribution itself.
    """
    m = np.array([1.0 - p1, p1])
    p = np.einsum("i,j,k->ijk", m, m, m) + delta * SIGMA
    if p.min() <= 0:
        return None, None
    return p, GS.share_2x2x2(p)


def main():
    rng = np.random.default_rng(20260727)
    print("CEILING-FRACTION PRECISION: bias and variance at known true share")
    print("predicted bias ~ 0.2275/(N*share);  predicted rel sd ~ "
          "sqrt(2+8*N*share)/(2*N*share)")
    print()
    print("%6s %10s %10s %9s %9s %9s %9s"
          % ("p1", "share", "N", "N*share", "bias", "pred", "rel sd"))
    for p1 in (0.5, 0.3):
        for delta in (0.004, 0.012, 0.030):
            p, s_true = planted(p1, delta)
            if p is None:
                continue
            q = p.ravel()
            for N in (10 ** 5, 10 ** 6, 10 ** 7):
                est = np.array([GS.share_2x2x2(rng.multinomial(N, q).reshape(2, 2, 2))
                                for _ in range(1500)])
                ns = N * s_true
                bias = est.mean() / s_true - 1.0
                relsd = est.std() / s_true
                pred = 0.2275 / ns
                print("%6.1f %10.3e %10.0e %9.1f %+8.2f%% %+8.2f%% %8.1f%%"
                      % (p1, s_true, N, ns, 100 * bias, 100 * pred, 100 * relsd))
    print()
    print("THIS CAMPAIGN'S OWN BUDGET (WATER_PREREG.md sec 6):")
    print("  design sensitivity      share = 3.0e-5 nats")
    print("  budgeted triples        N_tri = 6.7e5")
    print("  measured overlap        1.9x  ->  N_eff = 3.5e5")
    ne = 6.7e5 / 1.9
    ns = ne * 3.0e-5
    print("  N_eff * share           = %.1f" % ns)
    print("  predicted rel bias      = %+.1f%%" % (100 * 0.2275 / ns))
    print("  predicted rel sd        = %.0f%%" % (100 * np.sqrt(2 + 8 * ns) / (2 * ns)))
    # invert sqrt(2 + 8x)/(2x) = t  =>  4t^2 x^2 - 8x - 2 = 0
    #                             =>  x = [1 + sqrt(1 + t^2/2)] / t^2
    # (the first version of this line was wrong and reported that BETTER
    #  precision needed FEWER triples, which is how it was caught)
    for target in (0.30, 0.10):
        need = (1.0 + np.sqrt(1.0 + 0.5 * target ** 2)) / target ** 2
        chk = np.sqrt(2 + 8 * need) / (2 * need)
        print("  N_eff*share for %2.0f%% sd  = %.0f (check: %.1f%%)"
              "  -> N_tri = %.1e (%.0fx budget)"
              % (100 * target, need, 100 * chk, need / 3.0e-5 * 1.9, need / ns))


if __name__ == "__main__":
    main()
