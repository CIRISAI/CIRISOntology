#!/usr/bin/env python3
"""WATER_AMENDMENT_5: is the ceiling-fraction bias plateau REAL, or is it medians?

THE STATE OF THE QUESTION.  The glass campaign (glass_biaslaw.py,
GLASS_RESULTS.md 2.2a-i) confirmed this campaign's VARIANCE law on eight real
cells and found its BIAS law incomplete, with a correct and important
decomposition:

    rel_bias(ratio) = rel_bias(share) - rel_bias(ceiling)

-- because a ceiling fraction has TWO estimated quantities in it and the closed
form `1/(2*N*share)` describes the numerator alone.  It measured the ceiling's
term to be consistently NEGATIVE and dominant, and the ratio bias to PLATEAU
near +1% instead of falling as 1/(N*share).

BUT IT MEASURED MEDIANS THROUGHOUT, and said so.  Both candidate closed forms
are MEAN constants.  A median of a positively skewed estimator sits below its
mean, so a "negative bias" measured in medians is exactly what a skewed-but-
mean-unbiased estimator looks like.  This script measures BOTH, on the same
planted states, so the plateau is either confirmed as a real mean effect or
identified as a median artifact.

THE PLANTED FAMILY, and why the obvious one is useless here.  Starting from a
PRODUCT state and moving along the parity direction gives pair marginals that
are independent, and then

    ceiling = H(m1)+H(m2)+H(m3) - H(p) = share    exactly,

so the ratio is identically 1 and the family is degenerate for this question --
which is worth recording, because it was this campaign's first attempt.  The
family used instead starts from a PAIRWISE GIBBS state p0 (exp of a pairwise
Hamiltonian, hence its own pair-maxent), so Q = p0 and

    share(p0 + d*SIGMA) = H(p0) - H(p0 + d*SIGMA)     exactly,

with genuine pair correlations and a ratio far below 1.  Both truths are
COMPUTED on the exact distribution, never estimated.

Reads no water.
"""
import sys

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS  # noqa: E402

SIGMA = GS.SIGMA
S3 = np.array([[[(-1.0) ** (i + j + k) for k in (0, 1)] for j in (0, 1)]
               for i in (0, 1)])  # unused placeholder kept out of the maths


def gibbs_pairwise(J, h):
    """Pairwise Gibbs state on three bits: p(s) ~ exp(J*sum_{i<j} si sj + h*sum si).

    Being an exponential family with pairwise sufficient statistics, this state
    IS the maximum-entropy distribution carrying its own pair marginals, so its
    whole-only share is exactly zero and it serves as the `Q` of the planted
    family below.
    """
    s = np.array([1.0, -1.0])                     # index 0 -> +1, 1 -> -1
    E = np.zeros((2, 2, 2))
    for a in range(2):
        for b in range(2):
            for c in range(2):
                si, sj, sk = s[a], s[b], s[c]
                E[a, b, c] = J * (si * sj + si * sk + sj * sk) + h * (si + sj + sk)
    p = np.exp(E)
    return p / p.sum()


def exact_ceiling(p):
    """min over the three slot orientations of H(pair) + H(single) - H(p).

    `Core/ThirdCap.lean` `share_le_grouping_gaps`.  Computed on the exact
    distribution when `p` is exact, and on the empirical table when it is not.
    """
    p = np.asarray(p, dtype=float)
    tot = p.sum()
    if tot <= 0:
        return np.nan
    p = p / tot
    Hp = GS.entropy(p)
    out = []
    for pair_ax, sing_ax in (((2,), (0, 1)), ((1,), (0, 2)), ((0,), (1, 2))):
        out.append(GS.entropy(p.sum(axis=pair_ax)) + GS.entropy(p.sum(axis=sing_ax)) - Hp)
    return float(min(out))


def planted(J, h, delta):
    p0 = gibbs_pairwise(J, h)
    p = p0 + delta * SIGMA
    if p.min() <= 0:
        return None
    s_true = GS.entropy(p0) - GS.entropy(p)        # exact: Q = p0
    return dict(p=p, share=s_true, ceiling=exact_ceiling(p))


def relbias(est, truth):
    return dict(mean=float(est.mean() / truth - 1.0),
                median=float(np.median(est) / truth - 1.0))


def main():
    rng = np.random.default_rng(20260727)
    ndraw = 3000
    print("BIAS DECOMPOSITION of a ceiling fraction, MEAN vs MEDIAN")
    print("planted pairwise-Gibbs base + parity displacement; both truths exact")
    print("glass: rel_bias(ratio) = rel_bias(share) - rel_bias(ceiling)")
    print()
    hdr = ("%5s %9s %9s %8s | %-17s %-17s %-17s"
           % ("N*sh", "share", "ceiling", "ratio",
              "share bias", "ceiling bias", "ratio bias"))
    print(hdr)
    print("%5s %9s %9s %8s | %8s %8s %8s %8s %8s %8s"
          % ("", "", "", "", "mean", "med", "mean", "med", "mean", "med"))
    rows = []
    for (J, h, delta) in ((0.45, 0.25, 0.010), (0.45, 0.25, 0.030),
                          (0.30, 0.40, 0.020), (0.30, 0.40, 0.045)):
        pl = planted(J, h, delta)
        if pl is None:
            continue
        q = pl["p"].ravel()
        r_true = pl["share"] / pl["ceiling"]
        for N in (10 ** 5, 10 ** 6, 10 ** 7):
            tabs = rng.multinomial(N, q, size=ndraw)
            sh = np.array([GS.share_2x2x2(t.reshape(2, 2, 2)) for t in tabs])
            ce = np.array([exact_ceiling(t.reshape(2, 2, 2)) for t in tabs])
            ra = sh / ce
            bs, bc, br = (relbias(sh, pl["share"]), relbias(ce, pl["ceiling"]),
                          relbias(ra, r_true))
            print("%5.0f %9.2e %9.2e %8.4f | %+7.2f%% %+7.2f%% %+7.2f%% %+7.2f%% "
                  "%+7.2f%% %+7.2f%%"
                  % (N * pl["share"], pl["share"], pl["ceiling"], r_true,
                     100 * bs["mean"], 100 * bs["median"],
                     100 * bc["mean"], 100 * bc["median"],
                     100 * br["mean"], 100 * br["median"]))
            rows.append((N * pl["share"], bs, bc, br))
    print()
    print("CHECK 1 -- does the decomposition hold, separately in mean and median?")
    for tag in ("mean", "median"):
        d = [abs(br[tag] - (bs[tag] - bc[tag])) for _, bs, bc, br in rows]
        print("   %-6s  worst |ratio - (share - ceiling)| = %.3f pp"
              % (tag, 100 * max(d)))
    print()
    print("CHECK 2 -- does the MEAN ratio bias fall as 1/(N*share), or plateau?")
    for ns, bs, bc, br in rows:
        print("   N*share=%8.0f   mean ratio bias %+7.3f%%   0.5/(N*share)=%+7.3f%%"
              % (ns, 100 * br["mean"], 100 * 0.5 / ns))


if __name__ == "__main__":
    main()


def orientation_test():
    """WHY the ceiling is biased LOW as N^(-1/2): it is a MINIMUM of three.

    `share_le_grouping_gaps` gives three per-orientation ceilings and the honest
    denominator is their MINIMUM.  A minimum of three noisy estimates is biased
    downward by O(their spread) = O(1/sqrt(N)) -- NOT the O(1/N) of a plug-in
    bias -- and the bias is WORST when the three coincide, which is exactly the
    fully-symmetrised-template case.  Compared here against taking the MEAN of
    the three, which has no min-selection bias.
    """
    rng = np.random.default_rng(20260727)

    def three(p):
        p = np.asarray(p, float); tot = p.sum()
        if tot <= 0:
            return np.array([np.nan] * 3)
        p = p / tot; Hp = GS.entropy(p)
        return np.array([GS.entropy(p.sum(axis=ax)) + GS.entropy(p.sum(axis=sa)) - Hp
                         for ax, sa in (((2,), (0, 1)), ((1,), (0, 2)), ((0,), (1, 2)))])

    print()
    print("ORIENTATION TEST: is the ceiling's negative bias a MIN-OF-THREE effect?")
    print("%-22s %6s %9s %11s %11s %11s"
          % ("state", "N", "true sprd", "min bias", "mean bias", "one-orient"))
    for tag, (J, h, delta) in (("symmetric (J,h equal)", (0.45, 0.25, 0.010)),
                               ("symmetric (J,h equal)", (0.30, 0.40, 0.020))):
        pl = planted(J, h, delta)
        t3 = three(pl["p"]); spread = float(t3.max() - t3.min())
        for N in (10 ** 5, 10 ** 6):
            tabs = rng.multinomial(N, pl["p"].ravel(), size=2000)
            e3 = np.array([three(t.reshape(2, 2, 2)) for t in tabs])
            bmin = e3.min(1).mean() / t3.min() - 1.0
            bmean = e3.mean(1).mean() / t3.mean() - 1.0
            bone = e3[:, 0].mean() / t3[0] - 1.0
            print("%-22s %6.0e %9.2e %+10.3f%% %+10.3f%% %+10.3f%%"
                  % (tag, N, spread, 100 * bmin, 100 * bmean, 100 * bone))
    print()
    print("If min-bias >> mean-bias and mean-bias ~ one-orientation bias, the")
    print("negative ceiling bias is MIN SELECTION, not plug-in bias -- and the fix")
    print("is to average the orientations when symmetry makes them equal.")


orientation_test()
