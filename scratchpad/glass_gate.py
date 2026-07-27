#!/usr/bin/env python3
"""DOCIMASIA for the glass instrument: examine it before trusting it.

Every check here runs on SYNTHETIC data whose right answer is known -- three
of them from machine-checked theorems in this repository -- so none of it is a
reading on a real configuration and none of it is gated behind the
pre-registration.  A gate that has not seen dye cannot see anything
(`GATES.md`, reach 13).

  G1  parity state              share = log 2 exactly            (Core/Share)
  G2  product state             share = 0 exactly                (Core/Valve: valve_from_nothing)
  G3  sign-symmetric state      share = 0 exactly                (Core/SignSymmetry)
  G4  agreement with dalitz_share.share_2x2x2 on random tables
  G5  planted dye: an explicit three-body coupling, recovered
  G6  finite-sample floor of the estimator against 1/(2N)
  G7  triangle enumerator: exact count on a known lattice
  G8  triangle enumerator: minimum-image correctness across the boundary
  G9  headroom LP contains the measured share, and is wide on a free state
"""
import json
import sys

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as G  # noqa: E402

OUT = {}


def rec(name, ok, **kw):
    OUT[name] = dict(pass_=bool(ok), **kw)
    print(f"{'PASS' if ok else 'FAIL'}  {name}  " +
          "  ".join(f"{k}={v}" for k, v in kw.items()))
    return ok


def g1_parity():
    p = np.zeros((2, 2, 2))
    for a in (0, 1):
        for b in (0, 1):
            p[a, b, (a + b) % 2] = 0.25
    s = G.share_2x2x2(p)
    return rec("G1_parity", abs(s - np.log(2)) < 1e-12, share=s, target=np.log(2))


def g2_product():
    rng = np.random.default_rng(1)
    worst = 0.0
    for _ in range(200):
        m = [rng.uniform(0.05, 0.95) for _ in range(3)]
        p = np.einsum('i,j,k->ijk', [1 - m[0], m[0]], [1 - m[1], m[1]],
                      [1 - m[2], m[2]])
        worst = max(worst, G.share_2x2x2(p))
    return rec("G2_product_valve_from_nothing", worst < 1e-12, worst=worst)


def g3_signsym():
    rng = np.random.default_rng(2)
    worst = 0.0
    for _ in range(500):
        q = rng.random((2, 2, 2))
        p = q + q[::-1, ::-1, ::-1]          # enforce p(s) = p(-s)
        p /= p.sum()
        worst = max(worst, G.share_2x2x2(p))
    return rec("G3_sign_symmetric", worst < 1e-12, worst=worst)


def g4_cross():
    sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
    import dalitz_share as D
    rng = np.random.default_rng(3)
    worst = 0.0
    for _ in range(500):
        p = rng.random((2, 2, 2)) ** 3
        p /= p.sum()
        worst = max(worst, abs(G.share_2x2x2(p) - D.share_2x2x2(p)))
    return rec("G4_cross_dalitz", worst < 1e-12, worst_abs_diff=worst)


def g5_dye():
    """Planted three-body coupling on an ASYMMETRIC base -- the smallest dye the
    estimator can still see through its own floor at a stated N."""
    base = np.einsum('i,j,k->ijk', [.8, .2], [.8, .2], [.8, .2])
    chi = np.array([[[1., -1.], [-1., 1.]], [[-1., 1.], [1., -1.]]])
    rows = []
    for lam in (0.0, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3):
        p = base * np.exp(lam * chi)
        p /= p.sum()
        rows.append((lam, G.share_2x2x2(p)))
    mono = all(rows[i][1] <= rows[i + 1][1] + 1e-15 for i in range(len(rows) - 1))
    return rec("G5_dye_monotone", mono and rows[0][1] < 1e-15 and rows[-1][1] > 1e-4,
               curve=[(l, float(s)) for l, s in rows])


def g6_floor():
    """Finite-sample floor on a theorem-pinned zero, at the sample sizes this
    campaign will actually read.  The null is chi2_1-shaped, so the median and
    the p99 are both reported and no z is ever quoted from a sigma
    (`share-null-is-chi2-shaped`)."""
    rng = np.random.default_rng(4)
    base = np.array([.8, .2])
    out = {}
    for N in (10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7):
        vals = []
        for _ in range(200):
            p = np.einsum('i,j,k->ijk', base, base, base)
            c = rng.multinomial(N, p.ravel()).reshape(2, 2, 2)
            vals.append(G.share_2x2x2(c))
        v = np.array(vals)
        out[N] = dict(median=float(np.median(v)), mean=float(v.mean()),
                      p99=float(np.percentile(v, 99)), inv2N=1.0 / (2 * N))
        print(f"    N={N:>9}  median={out[N]['median']:.3e}  "
              f"mean={out[N]['mean']:.3e}  p99={out[N]['p99']:.3e}  "
              f"1/2N={out[N]['inv2N']:.3e}")
    # the floor must TRACK 1/(2N): one degree of freedom, the parity direction
    ratio = [out[N]['median'] / out[N]['inv2N'] for N in out]
    ok = all(0.2 < r < 3.0 for r in ratio)
    return rec("G6_floor_tracks_inv2N", ok, ratios=[float(r) for r in ratio],
               detail=out)


def g7_lattice():
    """Triangle enumerator against hand-countable cases on the simple cubic
    lattice, spacing 1, fully periodic.

      * template (1,1,1): no three sites are mutually at distance 1 on SC, so
        the count is EXACTLY 0.  A non-zero here is the enumerator inventing
        geometry.
      * template (1,1,sqrt2): slot 1 is the apex.  j runs over its 6 nearest
        neighbours; k over the remaining 5, of which one is j's opposite (at
        distance 2) and 4 are at sqrt2.  So the ORDERED count is exactly 24N.

    (An earlier version of this check used the 2D triangular lattice and FAILED
    -- because that lattice is not commensurate with a square periodic box, so
    the expectation was wrong and the enumerator was right.  Kept in the record
    rather than quietly swapped: `GATES.md` reach 8, the gate pointing the
    wrong way.)
    """
    n = 8
    g = np.arange(n, dtype=float)
    pts = np.stack(np.meshgrid(g, g, g, indexing='ij'), -1).reshape(-1, 3)
    L, N = float(n), len(pts)
    n_equi = len(G.triangles(pts, L, (1.0, 1.0, 1.0), 0.1))
    n_right = len(G.triangles(pts, L, (1.0, 1.0, np.sqrt(2.0)), 0.1))
    return rec("G7_simple_cubic", n_equi == 0 and n_right == 24 * N,
               equilateral=int(n_equi), expect_equilateral=0,
               right=int(n_right), expect_right=24 * N, N=N)


def g8_pbc():
    """Minimum image: a triangle straddling the periodic boundary must be found,
    and translating the whole system must not change the count."""
    rng = np.random.default_rng(7)
    L = 10.0
    pts = rng.random((300, 3)) * L
    t0 = len(G.triangles(pts, L, (1.5, 1.5, 1.5), 0.25))
    counts = []
    for sh in (0.37, 1.9, 5.5, 9.1):
        counts.append(len(G.triangles(np.mod(pts + sh, L), L, (1.5, 1.5, 1.5), 0.25)))
    return rec("G8_pbc_translation_invariant", all(c == t0 for c in counts),
               base=t0, shifted=counts)


def g9_headroom():
    lo, hi = G.share_headroom(np.full((2, 2, 2), 1 / 8))
    p = np.zeros((2, 2, 2))
    for a in (0, 1):
        for b in (0, 1):
            p[a, b, (a + b) % 2] = 0.25
    lo2, hi2 = G.share_headroom(p)
    s2 = G.share_2x2x2(p)
    return rec("G9_headroom", hi > 0.6 and hi2 > 0.6 and s2 <= hi2 + 1e-9,
               uniform_max=hi, parity_max=hi2, parity_share=s2)


if __name__ == "__main__":
    ok = all([g1_parity(), g2_product(), g3_signsym(), g4_cross(), g5_dye(),
              g6_floor(), g7_lattice(), g8_pbc(), g9_headroom()])
    json.dump(OUT, open("/home/emoore/CIRISOntology/scratchpad/glass_gate.json", "w"),
              indent=1, default=float)
    print("\nGATE", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
