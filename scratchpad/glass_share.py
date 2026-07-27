#!/usr/bin/env python3
"""The glass-transition whole-only instrument.

THE OBJECT.  Three particles at a fixed geometric template; each slot carries
that particle's SPECIES.  The reading is the connected information of order 3
(Schneidman, Still, Berry & Bialek, PRL 91:238701 (2003)) of the resulting
species triple: `share = S(Q) - S(P)` with `Q` the maximum-entropy distribution
carrying all three of `P`'s pair marginals.  Exact solver, one-dimensional
fibre, no IPF anywhere (`ipf-sharek-boundary-drift`).

WHY SPECIES AND NOT A BINNED FIELD.  The species alphabet is atomic.  There is
no continuum to bin, so the coarse-graining channel -- the single most dangerous
minting channel for this target -- is absent from the label by construction
rather than bounded by a sweep.  The only coarse-graining left in the design is
GEOMETRIC (the shell tolerance), and that one is measured by the fine-geometry
LP and the binmint pedestal below.

Credits for the physical question are in GLASS_PREREG.md and are not repeated
per-function here.  They are load-bearing: the residual-multiparticle-entropy
programme (Green 1952; Nettleton & Green 1958; Baranyai & Evans PRA 40:3817
(1989); Giaquinta & Giunta Physica A 187:145 (1992)) answers the same physical
question with a different -- and sign-indefinite -- object.
"""
import numpy as np

# ---------------------------------------------------------------------------
# the estimator: exact 2x2x2 share
# ---------------------------------------------------------------------------

SIGMA = np.array([[[1., -1.], [-1., 1.]], [[-1., 1.], [1., -1.]]])


def entropy(p):
    p = np.asarray(p, dtype=float)
    q = p[p > 0]
    return float(-np.sum(q * np.log(q)))


def share_2x2x2(p, tol=1e-15):
    """Whole-only share of a 2x2x2 table, exactly.

    The distributions carrying all three pair marginals of `p` are exactly the
    one-parameter family p + delta*SIGMA, since sum_k SIGMA[i,j,k] = 0 for every
    pair.  Entropy is strictly concave along it, so the pair-maxent is the unique
    root of dH/ddelta = -sum(SIGMA * log(p+delta*SIGMA)).  Bisection to machine
    precision.  (Byte-for-byte the solver of `dalitz_share.py`, re-stated here so
    this campaign's instrument is self-contained; cross-checked against it in
    the gate.)
    """
    p = np.asarray(p, dtype=float).reshape(2, 2, 2)
    s = p.sum()
    if s <= 0:
        return float("nan")
    p = p / s
    pos, neg = p[SIGMA > 0], p[SIGMA < 0]
    lo, hi = -pos.min(), neg.min()
    if hi - lo < tol:
        return 0.0

    def g(d):
        q = np.clip(p + d * SIGMA, 1e-300, None)
        return float(-np.sum(SIGMA * np.log(q)))

    a, b = lo + (hi - lo) * 1e-12, hi - (hi - lo) * 1e-12
    if g(a) < 0:
        return max(0.0, entropy(p + a * SIGMA) - entropy(p))
    if g(b) > 0:
        return max(0.0, entropy(p + b * SIGMA) - entropy(p))
    for _ in range(200):
        m = 0.5 * (a + b)
        if g(m) > 0:
            a = m
        else:
            b = m
    d = 0.5 * (a + b)
    return max(0.0, entropy(p + d * SIGMA) - entropy(p))


def share_headroom(p, ngrid=4001):
    """G-LP-a, the headroom: the interval the share can occupy over EVERY
    distribution carrying `p`'s three pair marginals.  All members of the fibre
    share one pair-maxent, so its entropy H* is a constant of the fibre and
    share(q) = H* - H(q); the reachable interval is [0, H* - min_d H].

    A collapsed interval means the pair marginals have left the statistic no
    room, and the reading is a restatement of them rather than a measurement
    (`KAPPA_EDGE_RESULTS.md` sec. 4).
    """
    p = np.asarray(p, dtype=float).reshape(2, 2, 2)
    p = p / p.sum()
    lo, hi = -p[SIGMA > 0].min(), p[SIGMA < 0].min()
    H = np.array([entropy(p + d * SIGMA) for d in np.linspace(lo, hi, ngrid)])
    return 0.0, float(H.max() - H.min())


# ---------------------------------------------------------------------------
# geometry: closed triangles at a template, under periodic boundaries
# ---------------------------------------------------------------------------

def wrap(pos, L):
    """Coordinates into [0, L)."""
    return np.mod(np.asarray(pos, dtype=np.float64), L)


def shell_adjacency(pos, L, rlo, rhi):
    """Dense boolean adjacency for the shell rlo <= r < rhi, minimum image.

    N is a few thousand, so the dense N x N boolean (17 MB at N=4096) is the
    cheap and unambiguous route; no tree, no cutoff bookkeeping, and the same
    code serves 2D and 3D.
    """
    pos = np.asarray(pos, dtype=np.float64)
    d = pos[:, None, :] - pos[None, :, :]
    d -= L * np.round(d / L)
    r2 = np.einsum('ijk,ijk->ij', d, d)
    A = (r2 >= rlo * rlo) & (r2 < rhi * rhi)
    np.fill_diagonal(A, False)
    return A


def _padded(A):
    """Neighbour lists as a padded (N, K) index array plus a validity mask."""
    N = A.shape[0]
    deg = A.sum(1)
    K = int(deg.max()) if deg.max() > 0 else 0
    NB = np.zeros((N, max(K, 1)), dtype=np.int32)
    M = np.zeros((N, max(K, 1)), dtype=bool)
    idx = np.nonzero(A)
    starts = np.zeros(N, dtype=np.int64)
    np.add.at(starts, idx[0], 0)  # no-op, kept for clarity
    order = np.argsort(idx[0], kind='stable')
    rows, cols = idx[0][order], idx[1][order]
    pos_in_row = np.arange(len(rows)) - np.repeat(
        np.concatenate(([0], np.cumsum(np.bincount(rows, minlength=N))[:-1])),
        np.bincount(rows, minlength=N))
    NB[rows, pos_in_row] = cols
    M[rows, pos_in_row] = True
    return NB, M, deg


def triangles(pos, L, tmpl, tol, rng=None, cap=None):
    """Vertex-index triples (i, j, k) closing the template.

    `tmpl = (r12, r13, r23)`.  Edge (1,2) and (1,3) are found from vertex 1's
    own shells; edge (2,3) is then a mask lookup, so the enumeration is
    (N, K12, K13) gathers and never a python loop over pairs.

    ORDERED triples are returned.  For the equilateral template that means each
    unordered triangle appears in all six orders, which is exactly the
    symmetrization the template's own symmetry demands -- the three slots are
    not physically distinguishable, so the reading must not depend on which
    particle was called slot 1.

    `cap` subsamples to at most `cap` triples per configuration, with the seed
    recorded; a capped count is a lower bound on the population and is reported
    as such (`GATES.md` harvest: search caps declared).
    """
    r12, r13, r23 = tmpl
    A12 = shell_adjacency(pos, L, r12 - tol, r12 + tol)
    A13 = A12 if r13 == r12 else shell_adjacency(pos, L, r13 - tol, r13 + tol)
    A23 = A12 if r23 == r12 else shell_adjacency(pos, L, r23 - tol, r23 + tol)

    NB12, M12, _ = _padded(A12)
    NB13, M13, _ = _padded(A13)
    N = pos.shape[0]
    close = A23[NB12[:, :, None], NB13[:, None, :]]
    ok = close & M12[:, :, None] & M13[:, None, :]
    ok &= (NB12[:, :, None] != NB13[:, None, :])
    ii, aa, bb = np.nonzero(ok)
    jj = NB12[ii, aa]
    kk = NB13[ii, bb]
    tri = np.stack([ii, jj, kk], axis=1).astype(np.int32)
    if cap is not None and len(tri) > cap:
        # cap TRIANGLES, not ordered triples -- see glass_run.triangles_from_d2
        key = np.sort(tri, axis=1)
        uniq, inv = np.unique(key, axis=0, return_inverse=True)
        mult = max(1, int(round(len(tri) / len(uniq))))
        ntri = max(1, cap // mult)
        if ntri < len(uniq):
            keep = rng.choice(len(uniq), size=ntri, replace=False)
            mask = np.zeros(len(uniq), dtype=bool)
            mask[keep] = True
            tri = tri[mask[inv]]
    return tri


def table_from_triples(tri, labels, nlab=2):
    """Contingency table of the slot labels over the triple list."""
    s = labels[tri]
    idx = (s[:, 0] * nlab + s[:, 1]) * nlab + s[:, 2]
    return np.bincount(idx, minlength=nlab ** 3).reshape((nlab,) * 3).astype(float)
