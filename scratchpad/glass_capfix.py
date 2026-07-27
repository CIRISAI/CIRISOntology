#!/usr/bin/env python3
"""Cap TRIANGLES, not ordered triples -- the water campaign's one-line fix, verified.

THE CONFLICT THEY FOUND.  Two conditions this campaign and that one had each
adopted, whose conjunction neither document checked:

  * the count-matched cap (--cap 1300), which subsamples the ORDERED triple list
    with rng.choice, and
  * the orientation-class partition, whose a priori warrant is that the
    enumeration returns every triangle in ALL its symmetry-allowed orders.

The cap breaks exactly the warrant the partition needs.  Measured in
GLASS_RESULTS.md sec 2.2b: S3 deviation is EXACTLY 0.000e+00 on every uncapped
template and 6.2e-05 to 5.3e-04 on every capped one.

THE FIX.  Subsample the UNORDERED triangles and emit every ordering of each
selected one.  Same kept count, exact symmetry preserved.
"""
import sys

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_run as GR   # noqa: E402

XP = GR.XP


def cap_ordered(tri, cap, rng):
    """What glass_share/glass_run do today: rng.choice over the ordered list."""
    if cap is None or tri.shape[0] <= cap:
        return tri
    sel = XP.asarray(rng.choice(int(tri.shape[0]), size=cap, replace=False))
    return tri[sel]


def cap_triangles(tri, cap, rng):
    """Subsample unordered TRIANGLES; keep every ordering of each selected one."""
    if cap is None or tri.shape[0] <= cap:
        return tri
    t = GR.cp.asnumpy(tri) if GR.GPU else np.asarray(tri)
    key = np.sort(t, axis=1)
    uniq, inv = np.unique(key, axis=0, return_inverse=True)
    mult = max(1, int(round(len(t) / len(uniq))))
    ntri = max(1, cap // mult)
    if ntri >= len(uniq):
        return tri
    keep = rng.choice(len(uniq), size=ntri, replace=False)
    mask = np.zeros(len(uniq), dtype=bool)
    mask[keep] = True
    out = t[mask[inv]]
    return XP.asarray(out)


def s3_dev(tri, lab, nlab=2):
    import itertools
    tab = GR.table_of(tri, XP.asarray(lab), nlab)
    p = tab / tab.sum()
    return max(np.abs(p - np.transpose(p, ax)).max()
               for ax in itertools.permutations(range(3))) / p.max()


if __name__ == "__main__":
    rng = np.random.default_rng(11)
    N, L = 900, (900 / 1.2) ** (1 / 3)
    pos = (rng.random((N, 3)) - 0.5) * L
    lab = (rng.random(N) >= 0.8).astype(np.int8)
    d2 = GR.pair_dist2(pos, L)
    tri = GR.triangles_from_d2(d2, (1.5, 1.5, 1.5), 0.2, rng, cap=None)
    t = GR.cp.asnumpy(tri) if GR.GPU else tri
    nuniq = len(np.unique(np.sort(t, axis=1), axis=0))
    print(f"uncapped: {len(t)} ordered triples over {nuniq} triangles "
          f"(ratio {len(t)/nuniq:.2f})")
    print(f"{'cap':>8s} {'kept ord':>9s} {'kept tri':>9s} "
          f"{'S3 dev ORDERED':>15s} {'S3 dev TRIANGLES':>17s}")
    base = s3_dev(tri, lab)
    print(f"{'none':>8s} {len(t):9d} {nuniq:9d} {base:15.3e} {base:17.3e}")
    for cap in (len(t) // 2, len(t) // 4, len(t) // 10):
        a = cap_ordered(tri, cap, np.random.default_rng(5))
        b = cap_triangles(tri, cap, np.random.default_rng(5))
        na = int(a.shape[0]); nb = int(b.shape[0])
        print(f"{cap:8d} {na:9d} {nb:9d} {s3_dev(a, lab):15.3e} "
              f"{s3_dev(b, lab):17.3e}")
