#!/usr/bin/env python3
"""WATER_AMENDMENT_7: the ceiling estimator for a PARTIALLY symmetric template.

Glass supplied the soundness argument for amendment 5's two-branch rule: when
the three true orientations genuinely DIFFER, the min is the object the theorem
bounds and taking the mean would quote a ceiling LOOSER THAN THE ONE PROVED;
when they COINCIDE, the mean is the better estimator of their common value and
nothing is given up.

That argument has a consequence for this campaign that neither document caught.
This campaign's primary template is (2.80, 2.80, 4.573) -- the tetrahedral
triangle.  Its apex is DISTINGUISHED: r12 = r13, but r23 differs.  So the slot
symmetry group is not S3, it is the transposition of slots 2 and 3, and

    orientation (12|3) and orientation (13|2)  coincide BY SYMMETRY
    orientation (23|1)                          genuinely differs

Stage 0 measured exactly that: 0.0693, 0.0693, 0.1189 at the tetrahedral
template.  So neither branch of the rule applies as stated -- the correct
estimator is the MEAN OF THE SYMMETRY-EQUIVALENT PAIR, then the MIN against the
third.  This script checks that on a planted state with the same 2+1 structure.

AND THE CRITERION MATTERS: the "they coincide" branch must be justified by an
A PRIORI symmetry of the template, never by observing that the three estimates
are close -- because observed closeness is precisely what min-selection bias
manufactures.
"""
import sys
import numpy as np
sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS

SIGMA = GS.SIGMA


def gibbs_2plus1(J12, J13, J23, h1, h2, h3):
    """Pairwise Gibbs state with the apex distinguished: J12 = J13 != J23,
    h2 = h3 != h1.  Slots 2 and 3 are exchangeable; slot 1 is not."""
    s = np.array([1.0, -1.0])
    E = np.zeros((2, 2, 2))
    for a in range(2):
        for b in range(2):
            for c in range(2):
                si, sj, sk = s[a], s[b], s[c]
                E[a, b, c] = (J12 * si * sj + J13 * si * sk + J23 * sj * sk
                              + h1 * si + h2 * sj + h3 * sk)
    p = np.exp(E)
    return p / p.sum()


def three(p):
    p = np.asarray(p, float); tot = p.sum()
    if tot <= 0:
        return np.array([np.nan] * 3)
    p = p / tot; Hp = GS.entropy(p)
    return np.array([GS.entropy(p.sum(axis=ax)) + GS.entropy(p.sum(axis=sa)) - Hp
                     for ax, sa in (((2,), (0, 1)), ((1,), (0, 2)), ((0,), (1, 2)))])


def main():
    rng = np.random.default_rng(20260727)
    # apex distinguished, exactly the tetrahedral template's symmetry
    p0 = gibbs_2plus1(0.45, 0.45, 0.15, 0.10, 0.30, 0.30)
    p = p0 + 0.012 * SIGMA
    t3 = three(p)
    print("PLANTED 2+1 STATE (apex distinguished, slots 2<->3 exchangeable)")
    print("  true orientations (12|3, 13|2, 23|1) = %.6f  %.6f  %.6f"
          % tuple(t3))
    print("  |12|3 - 13|2| = %.2e   (symmetry-equivalent pair)" % abs(t3[0] - t3[1]))
    print("  23|1 - min    = %+.4f  (%.0f%% above the min: genuinely separated)"
          % (t3[2] - t3.min(), 100 * (t3[2] / t3.min() - 1)))
    truth = float(t3.min())
    print("  TRUE CEILING (the proved min) = %.6f" % truth)
    print()
    print("%8s %14s %14s %16s %14s"
          % ("N", "min of 3", "mean of 3", "pairmean-then-min", "one orient"))
    for N in (10 ** 5, 10 ** 6, 10 ** 7):
        tabs = rng.multinomial(N, p.ravel(), size=1500)
        e3 = np.array([three(t.reshape(2, 2, 2)) for t in tabs])
        est_min = e3.min(1)
        est_mean = e3.mean(1)
        est_pair = np.minimum(0.5 * (e3[:, 0] + e3[:, 1]), e3[:, 2])
        est_one = e3[:, 0]
        print("%8.0e %+13.3f%% %+13.3f%% %+15.3f%% %+13.3f%%"
              % (N,
                 100 * (est_min.mean() / truth - 1),
                 100 * (est_mean.mean() / truth - 1),
                 100 * (est_pair.mean() / truth - 1),
                 100 * (est_one.mean() / truth - 1)))
    print()
    print("mean-of-3 is BIASED HIGH here -- it quotes a ceiling ABOVE the proved")
    print("minimum, which is exactly the unsoundness glass named.  min-of-3 is")
    print("biased low by selection.  The pair-mean-then-min estimator is the one")
    print("the template's own symmetry licenses.")


main()
