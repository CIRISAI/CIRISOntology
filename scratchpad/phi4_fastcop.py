"""A vectorized Gaussian-copula orthant evaluator, and its gate against the slow one.

Why: `phi4_ridge._tvn_upper` integrates with `scipy.integrate.quad` at `epsabs=1e-13`,
which calls a Python function per node and costs **2.7 s per 8-cell copula evaluation**.
K4's mixture fit needs ~20000 of them per lattice size, so as written it cannot finish.
Measured first: dropping the tolerance to 1e-8 changes the cells by 2.8e-17 -- machine zero
-- so the tolerance was buying nothing.  Rather than merely loosening it, this replaces the
adaptive quadrature with FIXED-NODE Gauss-Legendre evaluated on all eight cells at once.

Same mathematics, no approximation traded away: the integrand is smooth and bounded on a
finite interval, which is the case Gauss-Legendre is exact-to-machine-precision for at
modest order.  The claim is not argued, it is GATED below against the existing
implementation on random states, and the node count is chosen by convergence rather than by
taste.
"""
import sys, os, time
import numpy as np
from scipy import special

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import phi4_ridge as P

_XL, _WL = np.polynomial.legendre.leggauss(64)          # for the inner bvn integral
_XO, _WO = np.polynomial.legendre.leggauss(256)         # for the outer z integral


def bvn_upper_vec(h, k, r):
    """P(Z1 > h, Z2 > k) for standard bivariate normal, vectorized over h, k, r."""
    h = np.asarray(h, float); k = np.asarray(k, float); r = np.asarray(r, float)
    h, k, r = np.broadcast_arrays(h, k, r)
    s = 0.5 * r[..., None] * (_XL + 1.0)                       # (..., 64)
    one = 1.0 - s * s
    dens = np.exp(-(h[..., None] ** 2 - 2 * s * h[..., None] * k[..., None]
                    + k[..., None] ** 2) / (2 * one)) / (2 * np.pi * np.sqrt(one))
    lower = special.ndtr(h) * special.ndtr(k) + 0.5 * r * (_WL * dens).sum(-1)
    return 1.0 - special.ndtr(h) - special.ndtr(k) + lower


def tvn_upper_vec(a1, a2, a3, r12, r13, r23):
    """P(Z1>a1, Z2>a2, Z3>a3), vectorized, by conditioning on Z3 (same reduction as the
    scalar version, with a fixed 256-node Gauss-Legendre rule on [a3, a3+12])."""
    a1, a2, a3, r12, r13, r23 = np.broadcast_arrays(
        *[np.asarray(x, float) for x in (a1, a2, a3, r12, r13, r23)])
    s13 = np.sqrt(np.maximum(1 - r13 * r13, 1e-15))
    s23 = np.sqrt(np.maximum(1 - r23 * r23, 1e-15))
    rp = np.clip((r12 - r13 * r23) / (s13 * s23), -0.999999, 0.999999)
    z = a3[..., None] + 6.0 * (_XO + 1.0)                      # [a3, a3+12]
    w = 6.0 * _WO
    g = (np.exp(-0.5 * z * z) / np.sqrt(2 * np.pi)) * bvn_upper_vec(
        (a1[..., None] - r13[..., None] * z) / s13[..., None],
        (a2[..., None] - r23[..., None] * z) / s23[..., None],
        np.broadcast_to(rp[..., None], z.shape))
    return (w * g).sum(-1)


_SGN = np.array([[1.0 if ((i >> (2 - j)) & 1) == 0 else -1.0 for j in range(3)]
                 for i in range(8)])


def cells_vec(a, r12, r13, r23):
    """The 8 binarized cells of a Gaussian copula, all at once.  Index convention matches
    phi4_ridge.gauss_copula_cells exactly (b_i = 1 when below threshold)."""
    e = _SGN                                                    # (8,3)
    out = tvn_upper_vec(e[:, 0] * a[0], e[:, 1] * a[1], e[:, 2] * a[2],
                        e[:, 0] * e[:, 1] * r12, e[:, 0] * e[:, 2] * r13,
                        e[:, 1] * e[:, 2] * r23)
    return np.asarray(out, float)


# =====================================================================================

if __name__ == '__main__':
    rng = np.random.default_rng(20260727)
    print("=" * 84)
    print("GATE — vectorized copula vs phi4_ridge's adaptive-quadrature implementation")
    print("=" * 84)
    worst = 0.0
    t_slow = t_fast = 0.0
    for trial in range(40):
        a = rng.normal(0, 1.2, 3)
        rho = rng.uniform(-0.85, 0.85, 3)
        # keep the implied 3x3 correlation matrix positive definite
        M = np.array([[1, rho[0], rho[1]], [rho[0], 1, rho[2]], [rho[1], rho[2], 1]])
        if np.linalg.eigvalsh(M).min() <= 0.02:
            continue
        t0 = time.time(); slow = P.gauss_copula_cells(a, *rho); t_slow += time.time() - t0
        t0 = time.time(); fast = cells_vec(a, *rho); t_fast += time.time() - t0
        worst = max(worst, float(np.abs(slow - fast).max()))
    print(f"  worst |cell difference| over random states : {worst:.3e}")
    print(f"  slow {t_slow:.2f} s   fast {t_fast:.3f} s   speedup {t_slow/max(t_fast,1e-9):.0f}x")

    # the theorem: at the median (a = 0) the state is sign-symmetric, share exactly zero
    worst0 = 0.0
    for _ in range(50):
        rho = rng.uniform(-0.8, 0.8, 3)
        M = np.array([[1, rho[0], rho[1]], [rho[0], 1, rho[2]], [rho[1], rho[2], 1]])
        if np.linalg.eigvalsh(M).min() <= 0.02:
            continue
        c = cells_vec(np.zeros(3), *rho)
        worst0 = max(worst0, abs(float(P.share3(c / c.sum())[0])))
    print(f"  share at a = 0 (must be EXACTLY 0 by SignSymmetry.lean) : {worst0:.3e}")
    ok = worst < 1e-12 and worst0 < 1e-12
    print("=" * 84)
    print(f"  {'PASS' if ok else 'FAIL'}")
    sys.exit(0 if ok else 1)
