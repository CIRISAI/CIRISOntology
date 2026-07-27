#!/usr/bin/env python3
"""WATER_AMENDMENT_9: capping ORDERED TRIPLES breaks the symmetry the ceiling
estimator's a priori warrant depends on -- and capping TRIANGLES does not.

THE CONFLICT.  Two conditions this campaign has adopted collide:

  * WATER_AMENDMENT_1 A3 (binding on arm B): take the count-matched cap, because
    the glass campaign's raw triple counts RISE with temperature, the same
    direction a floor artifact would take.
  * WATER_AMENDMENT_7 G2: the ceiling estimator partitions the three
    per-orientation ceilings into symmetry-equivalence classes fixed A PRIORI
    from the template's geometry -- and the a priori warrant is that the
    enumeration returns every triangle in all its symmetry-allowed orders.

The glass campaign measured that its S3 invariance is EXACTLY zero on uncapped
templates and 6.2e-05 ... 5.3e-04 on capped ones.  The cap subsamples ORDERED
triples at random, and a random subset does not contain all orderings of a
triangle.  So the cap destroys exactly the symmetry the class partition relies
on, and under a cap the a priori warrant is void.

THE FIX, tested here: cap on TRIANGLES, not on ordered triples.  Subsample the
unordered triangles, then emit every symmetry-allowed ordering of each one
selected.  Same count control, exchangeability preserved exactly.

Reads no water: a synthetic point set, and the reading is a symmetry deviation
of a contingency table, not a share.
"""
import sys
import numpy as np
sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS


def s3_deviation(tab):
    """Worst relative deviation of an 8-cell table from S3 (slot-permutation)
    invariance.  Exactly zero iff the table is exchangeable."""
    t = np.asarray(tab, float)
    if t.sum() <= 0:
        return np.nan
    t = t / t.sum()
    worst = 0.0
    for perm in ((0, 2, 1), (1, 0, 2), (2, 1, 0), (1, 2, 0), (2, 0, 1)):
        d = np.abs(t - np.transpose(t, perm)).max()
        worst = max(worst, d / max(t.max(), 1e-300))
    return float(worst)


def cap_ordered(tri, cap, rng):
    """The glass instrument's cap: a random subset of ORDERED triples."""
    if cap is None or len(tri) <= cap:
        return tri
    return tri[rng.choice(len(tri), size=cap, replace=False)]


def cap_triangles(tri, cap, rng):
    """The fix: subsample unordered TRIANGLES, keep all their orderings."""
    if len(tri) == 0:
        return tri
    key = np.sort(tri, axis=1)
    _, inv = np.unique(key, axis=0, return_inverse=True)
    ntri = inv.max() + 1
    if cap is None:
        return tri
    # how many triangles fit under the ordered-triple budget
    per = len(tri) / ntri
    keep = int(max(1, min(ntri, np.floor(cap / per))))
    if keep >= ntri:
        return tri
    sel = set(rng.choice(ntri, size=keep, replace=False).tolist())
    mask = np.array([i in sel for i in inv])
    return tri[mask]


def main():
    rng = np.random.default_rng(20260727)
    N, L = 900, 20.0
    pos = rng.random((N, 3)) * L
    lab = (rng.random(N) < 0.35).astype(np.int8)
    tmpl = (2.4, 2.4, 2.4)          # equilateral: full S3, all six orderings
    tri = GS.triangles(pos, L, tmpl, 0.45, rng)
    ntri_unordered = len(np.unique(np.sort(tri, axis=1), axis=0))
    print("synthetic point set: N=%d  L=%.1f  equilateral template %s" % (N, L, tmpl))
    print("ordered triples = %d   unordered triangles = %d   ratio = %.2f"
          % (len(tri), ntri_unordered, len(tri) / max(ntri_unordered, 1)))
    print()
    print("%10s %10s %14s %16s" % ("cap", "kept", "cap ORDERED", "cap TRIANGLES"))
    full = GS.table_from_triples(tri, lab)
    print("%10s %10d %14.3e %16.3e"
          % ("none", len(tri), s3_deviation(full), s3_deviation(full)))
    for cap in (len(tri) // 2, len(tri) // 4, len(tri) // 10):
        a = cap_ordered(tri, cap, rng)
        b = cap_triangles(tri, cap, rng)
        print("%10d %10s %14.3e %16.3e"
              % (cap, "%d/%d" % (len(a), len(b)),
                 s3_deviation(GS.table_from_triples(a, lab)),
                 s3_deviation(GS.table_from_triples(b, lab))))
    print()
    print("Capping ORDERED triples breaks exchangeability; capping TRIANGLES")
    print("preserves it EXACTLY, at the same count control.  Under an ordered")
    print("cap the class-partition estimator's a priori warrant is void.")


main()
