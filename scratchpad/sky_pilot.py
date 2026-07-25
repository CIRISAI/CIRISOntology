#!/usr/bin/env python3
"""
sky_pilot.py -- the bispectrum bridge, simulation pilot.

Pre-registered in SKY_PILOT_PREREG.md, committed at 49c50de BEFORE this file existed.

Two arms:
  ARM 1 (exact)  -- analytic trivariate densities, quadrature, NO sampling anywhere.
  ARM 2 (fields) -- 3D Gaussian / lognormal / local-f_NL fields, sampled, all floors.

Nothing here touches Lean, Stance.lean or the audit.  No real survey data is read.

Usage:  python sky_pilot.py gate | arm1 | arm2 | all
"""
import json
import os
import sys
import time

import numpy as np
from scipy import special, stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

LN2 = float(np.log(2.0))
_TINY = 1e-300
HERE = os.path.dirname(os.path.abspath(__file__))


def log(*a):
    print(*a, flush=True)


# =====================================================================================
# SHARE MACHINERY, general alphabet size b  (b=2 reduces to the repository's share3)
# =====================================================================================

def _xlogx(x):
    x = np.asarray(x, dtype=np.float64)
    return np.where(x > 0.0, x * np.log(np.where(x > 0.0, x, 1.0)), 0.0)


def Hd(p):
    """Shannon entropy (nats) of an array of cell probabilities."""
    return float(-_xlogx(np.asarray(p, dtype=np.float64)).sum())


def pair_margs(p):
    """The three pair marginals of a (b,b,b) state."""
    return [p.sum(axis=2), p.sum(axis=1), p.sum(axis=0)]   # (12), (13), (23)


def pairwise_maxent(p, iters=200000, tol=1e-15):
    """IPF from uniform onto the pair-marginal constraints.  Multiplicative updates keep
    log q exactly a sum of pair functions, which is what makes the KL identity below a
    rigorous convergence certificate."""
    p = np.asarray(p, dtype=np.float64)
    b = p.shape[0]
    tgt = pair_margs(p)
    q = np.full(p.shape, 1.0 / p.size)
    err = np.inf
    for it in range(iters):
        for ax, (a0, a1) in enumerate([(0, 1), (0, 2), (1, 2)]):
            cur = q.sum(axis=[2, 1, 0][ax])
            ratio = np.where(cur > 0, tgt[ax] / np.where(cur > 0, cur, 1.0), 0.0)
            if ax == 0:
                q = q * ratio[:, :, None]
            elif ax == 1:
                q = q * ratio[:, None, :]
            else:
                q = q * ratio[None, :, :]
        cur = pair_margs(q)
        err = max(float(np.abs(cur[i] - tgt[i]).max()) for i in range(3))
        if err < tol:
            break
    return q, err, it + 1


def share_b(p, iters=200000, tol=1e-15):
    """Whole-only order-3 share of a (b,b,b) state, with a convergence certificate.

    Returns dict with
      share_H  = H(q) - H(p)          the definition
      share_KL = sum p log(p/q)       equal to share_H EXACTLY at the true maxent,
                                      because log q is a sum of pair functions and p,q
                                      share every pair marginal.  Their difference is a
                                      rigorous bound-like diagnostic on IPF convergence.
    """
    p = np.asarray(p, dtype=np.float64)
    p = p / p.sum()
    q, err, nit = pairwise_maxent(p, iters=iters, tol=tol)
    sH = Hd(q) - Hd(p)
    m = p > 0
    sKL = float(np.sum(p[m] * (np.log(p[m]) - np.log(np.maximum(q[m], _TINY)))))
    return dict(share_H=sH, share_KL=sKL, ipf_err=err, ipf_iters=nit,
                cert=abs(sH - sKL), H_p=Hd(p), H_q=Hd(q))


# --- b=2 reference solvers, imported from the validated Ising machinery ---------------
_POP = np.array([bin(i).count('1') for i in range(8)])
SIGMA8 = np.where(_POP % 2 == 0, 1.0, -1.0)


def share3_ref(p8):
    """The repository's fast b=2 solver (ising_field.share3): the pair envelope at k=3
    is one-dimensional, p + t*sigma, and the maxent is the unique root of dH/dt = 0."""
    p = np.asarray(p8, dtype=np.float64).ravel()
    even, odd = p[SIGMA8 > 0], p[SIGMA8 < 0]
    lo, hi = -even.min(), odd.min()
    if hi - lo <= 0:
        return 0.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        g = float((SIGMA8 * np.log(np.maximum(p + mid * SIGMA8, _TINY))).sum())
        if g < 0:
            lo = mid
        else:
            hi = mid
    t = 0.5 * (lo + hi)
    q = np.maximum(p + t * SIGMA8, 0.0)
    return float(-_xlogx(q).sum() + _xlogx(p).sum())


def share3_mp(p8, dps=60):
    """Arbitrary-precision b=2 reference (ising_field.share_mpmath)."""
    import mpmath as mp
    mp.mp.dps = dps
    P = [mp.mpf(repr(float(x))) for x in np.asarray(p8).ravel()]
    S = [mp.mpf(int(s)) for s in SIGMA8]
    lo = -min(P[i] for i in range(8) if S[i] > 0)
    hi = min(P[i] for i in range(8) if S[i] < 0)
    if hi - lo <= 0:
        return mp.mpf(0)
    g = lambda t: sum(S[i] * mp.log(P[i] + t * S[i]) for i in range(8))
    a, c = lo * mp.mpf('0.9999999999'), hi * mp.mpf('0.9999999999')
    for _ in range(400):
        m = (a + c) / 2
        if g(m) < 0:
            a = m
        else:
            c = m
    t = (a + c) / 2
    ent = lambda q: -sum(x * mp.log(x) for x in q if x > 0)
    return ent([P[i] + t * S[i] for i in range(8)]) - ent(P)


# =====================================================================================
# ROUTE B -- THE DERIVED BRIDGE   (SKY_PILOT_PREREG.md eq. (B))
#
#   I_C^(3) = 1/2 * [ A_1a A_2b A_3c zeta_abc ]^2 / perm(A) + O(zeta^3),   A = C^{-1}
#
# zeta is the FULL connected third-cumulant tensor on the three slots, coincident
# indices included -- zeta_111 is the one-point skewness, zeta_112 the collapsed term.
# =====================================================================================

def perm3(M):
    """Permanent of a 3x3 matrix (the determinant with all signs +)."""
    M = np.asarray(M, dtype=np.float64)
    return float(sum(M[0, s[0]] * M[1, s[1]] * M[2, s[2]]
                     for s in [(0, 1, 2), (0, 2, 1), (1, 0, 2),
                               (1, 2, 0), (2, 0, 1), (2, 1, 0)]))


def route_B(C, zeta):
    """The bridge.  C: (3,3) covariance.  zeta: (3,3,3) connected third cumulants."""
    A = np.linalg.inv(np.asarray(C, dtype=np.float64))
    num = float(np.einsum('a,b,c,abc->', A[0], A[1], A[2], np.asarray(zeta, float)))
    pm = perm3(A)
    return 0.5 * num * num / pm, num, pm


# =====================================================================================
# THE EXACT MODELS  (ARM 1) -- one-factor latent, everything by 1D quadrature
#
#   X_i = a_i Z + sqrt(1 - a_i^2) eps_i,   eps iid N(0,1),  Z standardised, cum3(Z)=gamma
#
#   C_ij = a_i a_j (i != j),  C_ii = 1,   zeta_abc = gamma * a_a a_b a_c
#
# Every cell probability is a one-dimensional integral over z of a product of Gaussian
# CDF differences -- machine precision at any b, any gamma, with NO sampling.
# =====================================================================================

def _simpson_w(n, h):
    w = np.ones(n)
    w[1:-1:2] = 4.0
    w[2:-1:2] = 2.0
    return w * (h / 3.0)


def _standardise(z, w):
    """The QUADRATURE IS THE DISTRIBUTION.  Renormalise the weights and affinely fix the
    nodes so the discrete law has mean 0 and variance 1 EXACTLY; then read its third
    cumulant off.  Route B is then fed the cumulants of the law actually used, not a
    nominal value the quadrature only approximates -- so no truncation error can leak
    into the comparison as a fake disagreement."""
    w = w / w.sum()
    m1 = float(np.sum(w * z))
    zc = z - m1
    v = float(np.sum(w * zc ** 2))
    zc = zc / np.sqrt(v)
    c3 = float(np.sum(w * zc ** 3))
    return zc, w, c3


# Quadrature step in units of the STANDARDISED latent.  Simpson error is O(h^4), and the
# integrands vary on scale 1 in z, so this fixes the accuracy independently of how long
# the skewed tail is -- which is what the first version of this gate got wrong.
HZ = 0.0015


def std_gamma_nodes(gam, nq=None, hz=HZ):
    """Quadrature for a standardised Gamma latent with third cumulant ~ `gam`.
    G ~ Gamma(k,1), Z = (G-k)/sqrt(k), cum3(Z) = 2/sqrt(k), so k = (2/gam)^2.
    Interval: the 1e-18 and 1-1e-18 quantiles of G, so no truncated tail can move the
    third moment at working precision.  Node count is set by a FIXED step in z."""
    k = (2.0 / gam) ** 2
    sk = np.sqrt(k)
    glo = float(stats.gamma.ppf(1e-18, k))
    ghi = float(stats.gamma.isf(1e-18, k))
    if nq is None:
        nq = int(((ghi - glo) / sk) / hz) + 1
    nq = max(nq, 2001) | 1
    g = np.linspace(glo, ghi, nq)
    logf = (k - 1) * np.log(g) - g - special.gammaln(k)
    w = _simpson_w(nq, g[1] - g[0]) * np.exp(logf)
    return _standardise((g - k) / sk, w)


def gauss_nodes(nq=None, span=20.0, hz=HZ):
    """Same interface for gamma = 0: a standard normal latent."""
    if nq is None:
        nq = int(2 * span / hz) + 1
    nq = max(nq, 2001) | 1
    z = np.linspace(-span, span, nq)
    w = _simpson_w(nq, z[1] - z[0]) * np.exp(-0.5 * z * z) / np.sqrt(2 * np.pi)
    return _standardise(z, w)


def latent_cells(a, edges, z, wz, chunk=None):
    """Exact (b,b,b) cell probabilities for the one-factor latent model.
    `edges` is a list of three arrays of bin edges (len b+1, ends +-inf).
    Assembled as a chunked BLAS matmul so the node count can be large enough for the
    quadrature to be converged even when the latent is heavily skewed."""
    a = np.asarray(a, dtype=np.float64)
    b = len(edges[0]) - 1
    per = []
    for i in range(3):
        s = np.sqrt(max(1.0 - a[i] ** 2, 1e-300))
        e = np.asarray(edges[i], dtype=np.float64)
        cdf = special.ndtr((e[None, :] - a[i] * z[:, None]) / s)   # (nq, b+1)
        per.append(np.ascontiguousarray(np.diff(cdf, axis=1)))     # (nq, b)
    if chunk is None:
        chunk = int(max(256, (1 << 22) // (b * b)))
    p = np.zeros((b * b, b))
    for lo in range(0, len(z), chunk):
        hi = min(lo + chunk, len(z))
        A, B, Cc = per[0][lo:hi], per[1][lo:hi], per[2][lo:hi]
        T = (A[:, :, None] * B[:, None, :]).reshape(hi - lo, b * b)
        p += T.T @ (wz[lo:hi, None] * Cc)
    p = p.reshape(b, b, b)
    return p / p.sum()


def latent_C_zeta(a, gam):
    a = np.asarray(a, dtype=np.float64)
    C = np.outer(a, a) + np.diag(1.0 - a ** 2)
    zeta = gam * np.einsum('a,b,c->abc', a, a, a)
    return C, zeta


def quantile_edges_gauss(b):
    """Quantile bin edges for a STANDARD NORMAL marginal (the latent model's marginal
    when gamma=0).  Symmetric, so the b=2 case is the median split."""
    qs = np.arange(1, b) / b
    e = special.ndtri(qs)
    return np.concatenate([[-np.inf], e, [np.inf]])


def quantile_edges_of(cdf_vec, b, lo=-60.0, hi=60.0):
    """Quantile edges for an arbitrary marginal given a VECTORISED CDF, by bisection on
    all b-1 edges at once."""
    t = np.arange(1, b) / b
    a_ = np.full(b - 1, lo)
    b_ = np.full(b - 1, hi)
    for _ in range(80):
        mid = 0.5 * (a_ + b_)
        lo_side = cdf_vec(mid) < t
        a_ = np.where(lo_side, mid, a_)
        b_ = np.where(lo_side, b_, mid)
    return np.concatenate([[-np.inf], 0.5 * (a_ + b_), [np.inf]])


def latent_marginal_cdf(ai, z, wz):
    """Vectorised marginal CDF of X_i = a_i Z + sqrt(1-a_i^2) eps_i."""
    s = np.sqrt(max(1.0 - ai ** 2, 1e-300))
    az = ai * z

    def cdf(x):
        x = np.atleast_1d(np.asarray(x, dtype=np.float64))
        return special.ndtr((x[:, None] - az[None, :]) / s) @ wz
    return cdf


# =====================================================================================
# GENERAL-C GAUSSIAN CELLS -- independent route, used to cross-check latent_cells
# 2D composite Gauss-Legendre over (x1,x2), third dimension analytic.
# =====================================================================================

def gauss_cells_general(C, edges, m=24, span=9.0):
    C = np.asarray(C, dtype=np.float64)
    s1, s2 = np.sqrt(C[0, 0]), np.sqrt(C[1, 1])
    # conditional law of x3 given (x1,x2)
    C12 = C[:2, :2]
    inv12 = np.linalg.inv(C12)
    beta = inv12 @ C[:2, 2]
    var3 = C[2, 2] - C[:2, 2] @ beta
    s3 = np.sqrt(max(var3, 1e-300))

    def axis_nodes(e, sd):
        lo = np.where(np.isfinite(e[:-1]), e[:-1], -span * sd)
        hi = np.where(np.isfinite(e[1:]), e[1:], span * sd)
        gx, gw = np.polynomial.legendre.leggauss(m)
        mid = 0.5 * (lo + hi)[:, None]
        hlf = 0.5 * (hi - lo)[:, None]
        return (mid + hlf * gx[None, :]).ravel(), (hlf * gw[None, :]).ravel()

    x1, w1 = axis_nodes(np.asarray(edges[0], float), s1)
    x2, w2 = axis_nodes(np.asarray(edges[1], float), s2)
    b = len(edges[0]) - 1
    X1, X2 = np.meshgrid(x1, x2, indexing='ij')
    W = np.outer(w1, w2)
    d = np.stack([X1.ravel(), X2.ravel()], axis=1)
    q = np.einsum('ni,ij,nj->n', d, inv12, d)
    dens = np.exp(-0.5 * q) / (2 * np.pi * np.sqrt(np.linalg.det(C12)))
    mu3 = d @ beta
    e3 = np.asarray(edges[2], float)
    cdf3 = special.ndtr((e3[None, :] - mu3[:, None]) / s3)
    p3 = np.diff(cdf3, axis=1)                                   # (n, b)
    wt = (W.ravel() * dens)[:, None] * p3                        # (n, b)
    nm = m
    wt = wt.reshape(b, nm, b, nm, b).sum(axis=(1, 3))
    return wt / wt.sum()


# =====================================================================================
# GATE -- everything must pass before a single measurement is reported
# =====================================================================================

def gate():
    log("=" * 78)
    log("GATE")
    log("=" * 78)
    res = {}
    rng = np.random.default_rng(20260725)
    ok = True

    def chk(name, passed, detail):
        nonlocal ok
        ok = ok and bool(passed)
        res[name] = dict(passed=bool(passed), detail=detail)
        log(f"  [{'PASS' if passed else 'FAIL'}] {name}: {detail}")

    # G1 -- general-b solver vs the repository's validated b=2 solvers
    worst_fast = worst_mp = 0.0
    for _ in range(200):
        p = rng.dirichlet(np.full(8, 0.7))
        s = share_b(p.reshape(2, 2, 2))
        worst_fast = max(worst_fast, abs(s['share_KL'] - share3_ref(p)))
    for _ in range(12):
        p = rng.dirichlet(np.full(8, 0.7))
        s = share_b(p.reshape(2, 2, 2))
        worst_mp = max(worst_mp, abs(s['share_KL'] - float(share3_mp(p))))
    chk("G1a general-b IPF vs fast b=2 solver (200 random states)",
        worst_fast < 1e-11, f"max |diff| = {worst_fast:.3e}")
    chk("G1b general-b IPF vs 60-digit mpmath (12 random states)",
        worst_mp < 1e-11, f"max |diff| = {worst_mp:.3e}")

    # G2 -- parity reads ln 2, independence reads 0
    par = np.zeros((2, 2, 2))
    for i in range(2):
        for j in range(2):
            par[i, j, (i + j) % 2] = 0.25
    sp = share_b(par)
    chk("G2a parity share = ln 2", abs(sp['share_KL'] - LN2) < 1e-12,
        f"{sp['share_KL']:.15f} vs {LN2:.15f}")
    si = share_b(np.full((2, 2, 2), 0.125))
    chk("G2b independent share = 0", abs(si['share_KL']) < 1e-14,
        f"{si['share_KL']:.3e}")

    # G3 -- explicit three-body coupling: closed form K tanh K - ln cosh K,
    #       and its weak-coupling limit K^2/2, which is Route B at C = I.
    worst_cf = worst_wk = 0.0
    for K in [0.1, 0.3, 0.5, 0.7, 0.9]:
        idx = np.indices((2, 2, 2))
        sg = np.where((idx.sum(axis=0) % 2) == 0, 1.0, -1.0)
        p = np.exp(K * sg)
        p /= p.sum()
        s = share_b(p)['share_KL']
        cf = K * np.tanh(K) - np.log(np.cosh(K))
        worst_cf = max(worst_cf, abs(s - cf))
        C = np.eye(3)
        z = np.zeros((3, 3, 3))
        z[0, 1, 2] = z[0, 2, 1] = z[1, 0, 2] = z[1, 2, 0] = z[2, 0, 1] = z[2, 1, 0] = np.tanh(K)
        worst_wk = max(worst_wk, abs(route_B(C, z)[0] - 0.5 * np.tanh(K) ** 2))
    chk("G3a three-body coupling vs closed form K tanhK - ln coshK",
        worst_cf < 1e-12, f"max |diff| = {worst_cf:.3e}")
    chk("G3b Route B at C=I equals 1/2 tanh^2 K",
        worst_wk < 1e-15, f"max |diff| = {worst_wk:.3e}")

    # G4 -- the sign-symmetry lemma, numerically (Core/SignSymmetry.lean)
    worst_ss = 0.0
    for _ in range(2000):
        h = rng.dirichlet(np.full(4, 0.8)) / 2.0
        p = np.zeros(8)
        for c in range(4):
            p[c] = h[c]
            p[7 - c] = h[c]
        worst_ss = max(worst_ss, abs(share_b(p.reshape(2, 2, 2))['share_KL']))
    chk("G4 sign-symmetric states read 0 (2000 random)",
        worst_ss < 1e-12, f"max |share| = {worst_ss:.3e}")

    # G5 -- the Gaussian cell machinery, against the exact orthant identity
    #        E[s_i s_j] = (2/pi) arcsin(rho)
    z, wz, _ = gauss_nodes()
    worst_or = 0.0
    for a in [(0.3, 0.5, 0.7), (0.9, 0.8, 0.6), (0.2, 0.2, 0.95)]:
        C, _ = latent_C_zeta(a, 0.0)
        e = [quantile_edges_gauss(2)] * 3
        p = latent_cells(a, e, z, wz)
        for (i, j) in [(0, 1), (0, 2), (1, 2)]:
            m = p.sum(axis=[2, 1, 0][{(0, 1): 0, (0, 2): 1, (1, 2): 2}[(i, j)]])
            emp = m[0, 0] + m[1, 1] - m[0, 1] - m[1, 0]
            worst_or = max(worst_or, abs(emp - (2 / np.pi) * np.arcsin(C[i, j])))
    chk("G5 latent Gaussian cells vs orthant identity (2/pi) arcsin(rho)",
        worst_or < 1e-10, f"max |diff| = {worst_or:.3e}")

    # G6 -- the two independent Gaussian cell routines agree
    worst_g = 0.0
    for a in [(0.3, 0.5, 0.7), (0.85, 0.7, 0.6)]:
        for b in [2, 4, 6]:
            C, _ = latent_C_zeta(a, 0.0)
            e = [quantile_edges_gauss(b)] * 3
            p1 = latent_cells(a, e, z, wz)
            p2 = gauss_cells_general(C, e, m=32)
            worst_g = max(worst_g, float(np.abs(p1 - p2).max()))
    chk("G6 latent vs general-C Gaussian cells (independent quadratures)",
        worst_g < 1e-9, f"max |diff| = {worst_g:.3e}")

    # G7 -- standardised gamma latent has the intended cumulants
    worst_c = worst_nom = 0.0
    for gam in [2.0, 0.5, 0.05, 0.001]:
        z2, w2, c3 = std_gamma_nodes(gam)
        m1 = float(np.sum(w2 * z2))
        m2 = float(np.sum(w2 * (z2 - m1) ** 2))
        worst_c = max(worst_c, abs(m1), abs(m2 - 1))
        worst_nom = max(worst_nom, abs(c3 - gam) / gam)
    chk("G7a standardised latent has mean 0 and variance 1 EXACTLY",
        worst_c < 1e-13, f"max |err| = {worst_c:.3e}")
    chk("G7b its measured cum3 matches the nominal gamma (labelling only)",
        worst_nom < 1e-4, f"max rel diff = {worst_nom:.3e}")

    # G9 -- cell probabilities are converged in the quadrature: node doubling
    worst_q = worst_s = 0.0
    for gam in [2.0, 0.1]:
        za, wa, _ = std_gamma_nodes(gam)
        zb, wb, _ = std_gamma_nodes(gam, hz=HZ / 2)
        for b in [2, 8, 16, 32]:
            ea = [quantile_edges_of(latent_marginal_cdf(0.6, za, wa), b)] * 3
            pa = latent_cells((0.6, 0.5, 0.7), ea, za, wa)
            pb = latent_cells((0.6, 0.5, 0.7), ea, zb, wb)
            worst_q = max(worst_q, float(np.abs(pa - pb).max()))
            sa, sb = share_b(pa)['share_KL'], share_b(pb)['share_KL']
            worst_s = max(worst_s, abs(sa - sb) / max(sa, 1e-300))
    chk("G9a REPORTED QUANTITY converged under quadrature refinement (rel.)",
        worst_s < 1e-6, f"max rel change in share = {worst_s:.3e}")
    chk("G9b cell probabilities converged under quadrature refinement",
        worst_q < 1e-13, f"max |diff| = {worst_q:.3e}")

    # G8 -- IPF convergence certificate is tight on the states this run will meet
    worst_cert = 0.0
    for b in [2, 3, 5, 8, 16]:
        z3, w3, _ = std_gamma_nodes(0.5)
        e = [quantile_edges_gauss(b)] * 3
        p = latent_cells((0.6, 0.5, 0.7), e, z3, w3)
        worst_cert = max(worst_cert, share_b(p)['cert'])
    chk("G8 |share_H - share_KL| on the run's own states (b up to 16)",
        worst_cert < 1e-13, f"max = {worst_cert:.3e}")

    res['ALL_PASS'] = bool(ok)
    log(f"\nGATE: {'ALL PASS' if ok else 'FAILURE -- run is void'}")
    return res, ok


# =====================================================================================
# ROUTE B2 -- the BINARY bridge, derived for the b=2 (median-split) reading
#
# At b=2 the pair envelope is one-dimensional: p_t = q + t*sigma preserves normalisation
# and all three pair marginals, and nothing else does.  Writing F(t) = H(q + t sigma),
#   F'(0) = -sum_s sigma(s) log q(s) = 0   (q is pairwise, so log q is a sum of pair
#                                           functions and sigma sums to zero over each),
#   F''(t) = -sum_s 1/(q+t sigma).
# Hence   share = (t^2/2) * sum_s 1/q(s) + O(t^3),   with   t = (tau_p - tau_q)/8,
# tau = E[s1 s2 s3].  So the b=2 share is quadratic in the EXCESS sign three-point
# product over what the sign pair marginals already force -- a moment route that never
# estimates an entropy.
# =====================================================================================

def route_B2(p8):
    """Quadratic (weak-coupling) prediction of the b=2 share, from the sign moments."""
    p = np.asarray(p8, dtype=np.float64).ravel()
    p = p / p.sum()
    even, odd = p[SIGMA8 > 0], p[SIGMA8 < 0]
    lo, hi = -even.min(), odd.min()
    if hi - lo <= 0:
        return 0.0, 0.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        g = float((SIGMA8 * np.log(np.maximum(p + mid * SIGMA8, _TINY))).sum())
        lo, hi = (mid, hi) if g < 0 else (lo, mid)
    t = 0.5 * (lo + hi)
    q = np.maximum(p + t * SIGMA8, 0.0)
    dtau = float((SIGMA8 * p).sum() - (SIGMA8 * q).sum())
    return 0.5 * t * t * float((1.0 / q).sum()), dtau


# =====================================================================================
# ARM 1 -- exact measurements
# =====================================================================================

def arm1_A1_discretisation(bs=(2, 3, 4, 5, 6, 8, 12, 16, 24, 32)):
    """A1: the Gaussian's binned share -- pure discretisation artifact, no signal."""
    log("\n" + "=" * 78)
    log("A1  DISCRETISATION BIAS: the share of a BINNED GAUSSIAN (truth = 0)")
    log("=" * 78)
    z, wz, _ = gauss_nodes()
    out = []
    cfgs = [(0.3, 0.3, 0.3), (0.5, 0.5, 0.5), (0.7, 0.7, 0.7),
            (0.9, 0.9, 0.9), (0.4, 0.6, 0.8)]
    for a in cfgs:
        row = dict(a=list(a), C=latent_C_zeta(a, 0.0)[0].tolist(), by_b={})
        for b in bs:
            e = [quantile_edges_gauss(b)] * 3
            p = latent_cells(a, e, z, wz)
            s = share_b(p)
            row['by_b'][b] = dict(share=s['share_KL'], cert=s['cert'], ipf_err=s['ipf_err'])
        out.append(row)
        log(f"  a = {a}   rho_12 = {a[0]*a[1]:.3f}")
        log("     b:  " + "  ".join(f"{b:>10d}" for b in bs))
        log("     I:  " + "  ".join(f"{row['by_b'][b]['share']:10.3e}" for b in bs))
    return out


def arm1_A2_lognormal(bs=(2, 3, 5, 8, 16)):
    """A2: transform invariance.  A lognormal field is a per-cell monotone transform of a
    Gaussian one; under QUANTILE bins the discrete states must be identical cell by cell."""
    log("\n" + "=" * 78)
    log("A2  THE LOGNORMAL IS A NULL: quantile-binned lognormal == binned Gaussian")
    log("=" * 78)
    z, wz, _ = gauss_nodes()
    out = []
    for a in [(0.5, 0.5, 0.5), (0.8, 0.6, 0.4)]:
        for sig in [0.3, 1.0, 2.0]:
            row = dict(a=list(a), sigma_g=sig, by_b={})
            for b in bs:
                eg = [quantile_edges_gauss(b)] * 3
                pg = latent_cells(a, eg, z, wz)
                # lognormal: X = exp(sig*g - sig^2/2) - 1, a strictly monotone per-cell map.
                # Quantile edges transform with it, so the cells are the SAME sets.
                el = [np.concatenate([[-np.inf],
                                      np.exp(sig * eg[0][1:-1] - sig ** 2 / 2) - 1.0,
                                      [np.inf]])] * 3
                # rebuild the lognormal cell probabilities from scratch in x-space:
                # P(X in (l,u]) = P(g in (ginv(l), ginv(u)]) -- computed independently
                gi = lambda x: (np.log(np.maximum(x + 1.0, 1e-300)) + sig ** 2 / 2) / sig
                eg2 = [np.concatenate([[-np.inf], gi(el[0][1:-1]), [np.inf]])] * 3
                pl = latent_cells(a, eg2, z, wz)
                sg_, sl_ = share_b(pg)['share_KL'], share_b(pl)['share_KL']
                row['by_b'][b] = dict(share_gauss=sg_, share_lognormal=sl_,
                                      max_cell_diff=float(np.abs(pg - pl).max()),
                                      share_diff=abs(sg_ - sl_))
            out.append(row)
            d = max(row['by_b'][b]['share_diff'] for b in bs)
            c = max(row['by_b'][b]['max_cell_diff'] for b in bs)
            log(f"  a={a} sigma_g={sig}:  max|share_LN - share_G| = {d:.3e}, "
                f"max cell diff = {c:.3e}")
    # ...and the lognormal's third cumulants, so "it has a bispectrum" is a number here
    log("\n  The same lognormal's connected third cumulants (so the null is not vacuous):")
    lg = []
    for a in [(0.5, 0.5, 0.5), (0.8, 0.6, 0.4)]:
        for sig in [0.3, 1.0, 2.0]:
            C, _ = latent_C_zeta(a, 0.0)
            # delta_i = exp(sig g_i - sig^2/2) - 1 with g the unit-variance latent field
            Cx = np.exp(sig ** 2 * C) - 1.0
            z3 = np.zeros((3, 3, 3))
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        z3[i, j, k] = (np.exp(sig ** 2 * (C[i, j] + C[i, k] + C[j, k]))
                                       - np.exp(sig ** 2 * C[i, j])
                                       - np.exp(sig ** 2 * C[i, k])
                                       - np.exp(sig ** 2 * C[j, k]) + 2.0)
            rb = route_B(Cx, z3)
            lg.append(dict(a=list(a), sigma_g=sig, zeta_123=float(z3[0, 1, 2]),
                           skew_1pt=float(z3[0, 0, 0]) / Cx[0, 0] ** 1.5,
                           routeB=rb[0], routeB_numerator=rb[1]))
            log(f"    a={a} sigma_g={sig}: zeta_123 = {z3[0,1,2]:.4e}, "
                f"1-pt skewness = {lg[-1]['skew_1pt']:.4f}, "
                f"Route B numerator = {rb[1]:.3e}, Route B = {rb[0]:.3e}")
    return dict(binned=out, cumulants=lg)


def arm1_A3_bridge(gammas=None, bs=(2, 3, 4, 6, 8, 12, 16, 24, 32, 48)):
    """A3/A4: Route A (exact, binned) vs the two derived bridges, swept in amplitude.

    Reported at every point:
      A(b)        the exact binned share of the skewed-latent triple
      G(b)        the exact binned share of the MATCHED GAUSSIAN (same C, same quantile
                  levels) -- the pure discretisation artifact, truth zero
      A(b) - G(b) the bias-subtracted reading, whose SCALING IN gamma is the test of
                  whether subtraction can rescue b >= 3
      B2          the binary bridge (quadratic truncation at b=2)
      B           the continuum bridge, eq. (B), from C and zeta
    """
    log("\n" + "=" * 78)
    log("A3/A4  ROUTE A vs ROUTE B, swept over the non-Gaussianity amplitude")
    log("=" * 78)
    if gammas is None:
        gammas = [2.0, 1.0, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002]
    zg, wg, _ = gauss_nodes()
    out = []
    for a in [(0.5, 0.5, 0.5), (0.8, 0.6, 0.4), (0.3, 0.3, 0.3)]:
        C0, _ = latent_C_zeta(a, 1.0)
        blk = dict(a=list(a), C=C0.tolist(), rows=[])
        gbias = {}
        for b in bs:
            gbias[b] = share_b(latent_cells(a, [quantile_edges_gauss(b)] * 3,
                                            zg, wg))['share_KL']
        blk['gauss_bias'] = {b: gbias[b] for b in bs}
        log(f"\n  a = {a}   C_12={C0[0,1]:.3f} C_13={C0[0,2]:.3f} C_23={C0[1,2]:.3f}")
        log(f"  {'gamma':>7} {'A(b=2)':>11} {'B2':>11} {'B2/A2':>7} {'B(cont)':>11} "
            f"{'A(48)':>11} {'G(48)':>11} {'A-G(48)':>11} {'bias/A':>8}")
        for gam in gammas:
            z, wz, gam_eff = std_gamma_nodes(gam)
            Cg, zeta = latent_C_zeta(a, gam_eff)
            row = dict(gamma=gam, gamma_eff=gam_eff, by_b={})
            cdfs = {}
            for ai in set(a):
                cdfs[ai] = latent_marginal_cdf(ai, z, wz)
            for b in bs:
                ecache = {ai: quantile_edges_of(cdfs[ai], b) for ai in cdfs}
                ee = [ecache[a[i]] for i in range(3)]
                p = latent_cells(a, ee, z, wz)
                s_ = share_b(p)
                ent = dict(share=s_['share_KL'], cert=s_['cert'],
                           gauss_bias=gbias[b],
                           subtracted=s_['share_KL'] - gbias[b])
                if b == 2:
                    b2, dtau = route_B2(p)
                    ent['routeB2'] = b2
                    ent['dtau'] = dtau
                row['by_b'][b] = ent
            rb, num, pm = route_B(Cg, zeta)
            row['routeB'] = rb
            row['routeB_num'] = num
            blk['rows'].append(row)
            r2 = row['by_b'][2]
            rL = row['by_b'][bs[-1]]
            log(f"  {gam:7.4g} {r2['share']:11.4e} {r2['routeB2']:11.4e} "
                f"{r2['routeB2']/max(r2['share'],1e-300):7.4f} {rb:11.4e} "
                f"{rL['share']:11.4e} {rL['gauss_bias']:11.4e} {rL['subtracted']:11.4e} "
                f"{rL['gauss_bias']/max(rL['share'],1e-300):8.3f}")
        out.append(blk)

    # --- the cross-term test: how does each column scale with gamma at weak coupling? ---
    log("\n  SCALING IN gamma over the weakest four amplitudes (prediction: 2 for a")
    log("  genuine share; 1 signals a cross term between artifact and signal):")
    log(f"  {'a':>18} {'A(b=2)':>9} {'A(b=3)':>9} {'A-G(b=3)':>10} {'A(b=48)':>9} "
        f"{'A-G(b=48)':>10}")
    for blk in out:
        g = np.log([r['gamma_eff'] for r in blk['rows'][-4:]])
        def sl(f):
            y = np.array([f(r) for r in blk['rows'][-4:]])
            if np.any(y <= 0):
                return np.nan
            return float(np.polyfit(g, np.log(y), 1)[0])
        vals = [sl(lambda r: r['by_b'][2]['share']),
                sl(lambda r: r['by_b'][3]['share']),
                sl(lambda r: abs(r['by_b'][3]['subtracted'])),
                sl(lambda r: r['by_b'][bs[-1]]['share']),
                sl(lambda r: abs(r['by_b'][bs[-1]]['subtracted']))]
        blk['slopes'] = dict(zip(['A_b2', 'A_b3', 'sub_b3', 'A_bmax', 'sub_bmax'], vals))
        log(f"  {str(tuple(blk['a'])):>18} " + " ".join(f"{v:9.3f}" for v in vals[:2])
            + f" {vals[2]:10.3f} {vals[3]:9.3f} {vals[4]:10.3f}")
    return out


def arm1_A5_slope(a=(0.5, 0.5, 0.5)):
    """P4: the weak-coupling slope.  At b=2 the share has a closed form from eight cell
    probabilities, so this can be pushed to arbitrary precision over many decades."""
    log("\n" + "=" * 78)
    log("A5  WEAK-COUPLING SLOPE  d log I / d log gamma   (prediction: 2.00 +- 0.05)")
    log("=" * 78)
    gams = [1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4, 1e-4]
    rows = []
    for gam in gams:
        z, wz, gam_eff = std_gamma_nodes(gam, nq=20001)
        ee = [quantile_edges_of(latent_marginal_cdf(a[i], z, wz), 2) for i in range(3)]
        p = latent_cells(a, ee, z, wz)
        s2 = share3_ref(p.ravel())
        s2mp = float(share3_mp(p.ravel(), dps=50))
        C, zeta = latent_C_zeta(a, gam_eff)
        rows.append(dict(gamma=gam, gamma_eff=gam_eff, share_b2=s2, share_b2_mp=s2mp, routeB=route_B(C, zeta)[0]))
        log(f"    gamma={gam:9.2e}   I(b=2) = {s2:12.5e}  (mp {s2mp:12.5e})   "
            f"Route B = {rows[-1]['routeB']:12.5e}")
    g = np.log([r['gamma'] for r in rows])
    y = np.log([max(r['share_b2_mp'], 1e-300) for r in rows])
    sl = float(np.polyfit(g, y, 1)[0])
    # the same slope on the weakest four points only
    sl4 = float(np.polyfit(g[-4:], y[-4:], 1)[0])
    log(f"\n    fitted slope (all points)      = {sl:.5f}")
    log(f"    fitted slope (weakest 4 points) = {sl4:.5f}")
    return dict(rows=rows, slope_all=sl, slope_weak=sl4)


def arm1():
    r = {}
    r['A1_discretisation'] = arm1_A1_discretisation()
    r['A2_lognormal'] = arm1_A2_lognormal()
    r['A5_slope'] = arm1_A5_slope()
    r["A3_bridge"] = arm1_A3_bridge()
    return r


# =====================================================================================
if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    t0 = time.time()
    out = {}
    if what in ('gate', 'all', 'arm1'):
        g, ok = gate()
        out['gate'] = g
        if not ok:
            log("\nGATE FAILED -- refusing to measure.")
            json.dump(out, open(os.path.join(HERE, 'sky_pilot_gate.json'), 'w'), indent=1)
            sys.exit(1)
    if what in ('arm1', 'all'):
        out['arm1'] = arm1()
        json.dump(out, open(os.path.join(HERE, 'sky_pilot_arm1.json'), 'w'), indent=1,
                  default=float)
    if what == 'gate':
        json.dump(out, open(os.path.join(HERE, 'sky_pilot_gate.json'), 'w'), indent=1,
                  default=float)
    log(f"\nelapsed {time.time()-t0:.1f}s")


# =====================================================================================
# ARM 2 -- 3D FIELDS.  Everything below is sampled, and every trap lives here.
# =====================================================================================

def get_xp(gpu=True):
    if gpu:
        try:
            import cupy as cp
            cp.cuda.runtime.getDeviceProperties(0)
            return cp, True
        except Exception:
            pass
    return np, False


def eh_nowiggle_T(k, Om=0.31, Ob=0.048, h=0.68, Tcmb=2.7255):
    """Eisenstein & Hu (1998) no-wiggle transfer function.  k in h/Mpc.
    Stated explicitly because 'a CDM-like P(k)' is not a specification."""
    k = np.asarray(k, dtype=np.float64) * h                      # -> 1/Mpc
    om, ob = Om * h * h, Ob * h * h
    th = Tcmb / 2.7
    s = 44.5 * np.log(9.83 / om) / np.sqrt(1.0 + 10.0 * ob ** 0.75)
    aG = (1.0 - 0.328 * np.log(431.0 * om) * (ob / om)
          + 0.38 * np.log(22.3 * om) * (ob / om) ** 2)
    Geff = Om * h * (aG + (1.0 - aG) / (1.0 + (0.43 * k * s) ** 4))
    q = np.where(k > 0, k * th * th / np.maximum(Geff, 1e-30), 1e-30)
    L0 = np.log(2.0 * np.e + 1.8 * q)
    C0 = 14.2 + 731.0 / (1.0 + 62.5 * q)
    return L0 / (L0 + C0 * q * q)


def kgrid(N, L, xp):
    kf = 2.0 * np.pi / L
    kz = xp.asarray(np.fft.rfftfreq(N) * N * kf)
    ky = xp.asarray(np.fft.fftfreq(N) * N * kf)
    k2 = (ky[:, None, None] ** 2 + ky[None, :, None] ** 2 + kz[None, None, :] ** 2)
    return xp.sqrt(k2)


def gaussian_field(N, L, kk, ns, seed, xp, transfer=None):
    """Gaussian field with P(k) proportional to k^ns T(k)^2, unit variance.
    Built as white noise -> FFT -> shape -> IFFT, so Hermitian symmetry is exact."""
    rng = np.random.default_rng(seed)
    w = xp.asarray(rng.standard_normal((N, N, N)))
    wk = xp.fft.rfftn(w)
    amp = xp.where(kk > 0, kk ** (ns / 2.0), 0.0)
    if transfer is not None:
        amp = amp * transfer
    g = xp.fft.irfftn(wk * amp, s=(N, N, N))
    return g / xp.sqrt((g * g).mean())


def smooth(f, kk, R, xp):
    return xp.fft.irfftn(xp.fft.rfftn(f) * xp.exp(-0.5 * (kk * R) ** 2), s=f.shape)


def binarise(f, xp):
    med = float(xp.median(f))
    tied = float((f == med).mean())
    return (f > med), tied


def triple_hist(sb, d1, d2, xp):
    """Empirical 8-cell state of (s(x), s(x+d1), s(x+d2)) over all x, periodic."""
    a = sb
    b = xp.roll(sb, tuple(-int(v) for v in d1), axis=(0, 1, 2))
    c = xp.roll(sb, tuple(-int(v) for v in d2), axis=(0, 1, 2))
    idx = (a.astype(xp.int64) * 4 + b.astype(xp.int64) * 2 + c.astype(xp.int64)).ravel()
    cnt = xp.bincount(idx, minlength=8).astype(xp.float64)
    cnt = cnt.get() if hasattr(cnt, 'get') else cnt
    return np.asarray(cnt) / cnt.sum()


def triple_cumulants(f, d1, d2, xp):
    """Full connected third-cumulant tensor zeta_abc and covariance C_ab for the triple
    (f(x), f(x+d1), f(x+d2)) -- coincident indices included, which is exactly what the
    bridge needs and exactly what a bispectrum measurement does not supply."""
    A = f
    B = xp.roll(f, tuple(-int(v) for v in d1), axis=(0, 1, 2))
    Cc = xp.roll(f, tuple(-int(v) for v in d2), axis=(0, 1, 2))
    V = [A, B, Cc]
    V = [v - float(v.mean()) for v in V]
    C = np.zeros((3, 3))
    for i in range(3):
        for j in range(i, 3):
            C[i, j] = C[j, i] = float((V[i] * V[j]).mean())
    Z = np.zeros((3, 3, 3))
    for i in range(3):                      # only the 10 distinct index multisets
        for j in range(i, 3):
            pij = V[i] * V[j]
            for k in range(j, 3):
                z = float((pij * V[k]).mean())
                for pp in {(i, j, k), (i, k, j), (j, i, k),
                           (j, k, i), (k, i, j), (k, j, i)}:
                    Z[pp] = z
    return C, Z          # third cumulant = third central moment for a zero-mean field


def white_noise(N, seed, xp):
    return xp.asarray(np.random.default_rng(seed).standard_normal((N, N, N)))


def shape_field(w, kk, ns, xp, transfer=None):
    """White noise -> P(k) ~ k^ns T(k)^2, unit variance.  Hermitian symmetry exact."""
    amp = xp.where(kk > 0, kk ** (ns / 2.0), 0.0)
    if transfer is not None:
        amp = amp * transfer
    g = xp.fft.irfftn(xp.fft.rfftn(w) * amp, s=w.shape)
    return g / xp.sqrt(float((g * g).mean()))


def make_field(kind, amp, w, kk, T, ns, R, xp):
    """(a) Gaussian, (b) lognormal, (c) local-f_NL-type -- all from the SAME white noise
    `w`, so a family's zero-amplitude member is a PAIRED control for its own ladder and
    the realisation variance cancels in the difference."""
    if kind == 'gauss':
        f = shape_field(w, kk, ns, xp, transfer=T)
    elif kind == 'lognormal_pt':
        # SMOOTH FIRST, THEN the pointwise map: delta is exactly a per-cell monotone
        # transform of the smoothed Gaussian field, so the transform theorem applies and
        # the median split must be BIT-IDENTICAL to the Gaussian's.
        g = smooth(shape_field(w, kk, ns, xp, transfer=T), kk, R, xp)
        if amp <= 0:
            return g
        return xp.exp(amp * g - 0.5 * amp * amp) - 1.0
    elif kind == 'lognormal_sm':
        # TRANSFORM FIRST, THEN smooth.  Identical ingredients, opposite order.  A filter
        # is not a per-cell map, so the theorem does NOT apply to this one.
        g = shape_field(w, kk, ns, xp, transfer=T)
        if amp <= 0:
            f = g
        else:
            f = xp.exp(amp * g - 0.5 * amp * amp) - 1.0
    elif kind == 'fnl':
        # primordial potential P_phi ~ k^(ns-4);  Phi = phi + a (phi^2 - <phi^2>);
        # delta(k) = M(k) Phi(k) with M ~ k^2 T(k), restoring P_delta ~ k^ns T^2.
        # A pointwise transform OF THE POTENTIAL followed by a scale-dependent filter,
        # so delta is NOT a pointwise transform of a Gaussian field -- which is exactly
        # why this one is the genuine positive control.
        phi = shape_field(w, kk, ns - 4.0, xp)
        Phi = phi + amp * (phi * phi - float((phi * phi).mean()))
        f = xp.fft.irfftn(xp.fft.rfftn(Phi) * (kk ** 2) * T, s=w.shape)
        f = f / xp.sqrt(float((f * f).mean()))
    else:
        raise ValueError(kind)
    return smooth(f, kk, R, xp)


def triple_hist_iso(sb, r, mode, xp):
    """8-cell state pooled over the three axis orientations of a configuration.
    mode 'L' = collinear (r, 2r);  mode 'T' = right angle (r along i, r along j)."""
    tot = np.zeros(8)
    for ax in range(3):
        if mode == 'L':
            d1 = [0, 0, 0]; d1[ax] = r
            d2 = [0, 0, 0]; d2[ax] = 2 * r
        else:
            d1 = [0, 0, 0]; d1[ax] = r
            d2 = [0, 0, 0]; d2[(ax + 1) % 3] = r
        tot += triple_hist(sb, d1, d2, xp)
    return tot / tot.sum()


def cfg_disp(r, mode, ax=0):
    if mode == 'L':
        d1 = [0, 0, 0]; d1[ax] = r
        d2 = [0, 0, 0]; d2[ax] = 2 * r
    else:
        d1 = [0, 0, 0]; d1[ax] = r
        d2 = [0, 0, 0]; d2[(ax + 1) % 3] = r
    return d1, d2


def arm2(N=256, L=1000.0, R=8.0, n_real=12, seed0=20260725, gpu=True):
    log("\n" + "=" * 78)
    log("ARM 2 -- 3D FIELDS  (N=%d, L=%.0f Mpc/h, Gaussian smoothing R=%.1f Mpc/h)" %
        (N, L, R))
    log("=" * 78)
    xp, on_gpu = get_xp(gpu)
    log(f"  backend: {'cupy/GPU' if on_gpu else 'numpy/CPU'}   cell = {L/N:.3f} Mpc/h")
    kk = kgrid(N, L, xp)
    T = xp.asarray(eh_nowiggle_T(kk.get() if hasattr(kk, 'get') else kk))
    ns = 0.96
    cfgs = [(r, m) for r in (2, 4, 8) for m in ('L', 'T')]
    cname = lambda r, m: f"{m}{r}"

    ladders = {
        'lognormal_pt': [0.0, 0.2, 0.5, 1.0, 2.0],
        'lognormal_sm': [0.0, 0.2, 0.5, 1.0, 2.0],
        'fnl':          [0.0, 0.03, 0.1, 0.3, 1.0, 3.0],
    }

    acc = {}          # (kind, amp, cfg) -> list of per-realisation shares
    S3 = {}
    ties = {}
    lognormal_identity = []
    cums = {}
    for rr in range(n_real):
        w = white_noise(N, seed0 + 1000 * rr, xp)
        base_bits = None
        for kind, amps in ladders.items():
            for amp in amps:
                f = make_field(kind, amp, w, kk, T, ns, R, xp)
                v = float((f * f).mean()) - float(f.mean()) ** 2
                S3.setdefault((kind, amp), []).append(
                    float(((f - f.mean()) ** 3).mean()) / v ** 2)
                sb, tied = binarise(f, xp)
                ties.setdefault((kind, amp), []).append(tied)
                # THE TRANSFORM THEOREM ON A 3D FIELD: the lognormal's median split must
                # be BIT-IDENTICAL to the Gaussian's, at every amplitude.
                if kind == 'lognormal_pt':
                    if amp == 0.0:
                        base_bits = sb.copy()
                    else:
                        lognormal_identity.append(
                            int((sb != base_bits).sum().get()
                                if on_gpu else (sb != base_bits).sum()))
                for (r, m) in cfgs:
                    acc.setdefault((kind, amp, cname(r, m)), []).append(
                        share3_ref(triple_hist_iso(sb, r, m, xp)))
                for (r, m) in cfgs:
                    d1, d2 = cfg_disp(r, m)
                    Cm, Zm = triple_cumulants(f, d1, d2, xp)
                    cums.setdefault((kind, amp, cname(r, m)), []).append(
                        (Cm, Zm, route_B(Cm, Zm)[0]))
                del f, sb
                if on_gpu:
                    xp.get_default_memory_pool().free_all_blocks()
        del w, base_bits
        if on_gpu:
            xp.get_default_memory_pool().free_all_blocks()
        log(f"  realisation {rr+1}/{n_real} done")

    log("\n  KILL K2 ON A 3D FIELD -- the lognormal's median split vs the Gaussian's:")
    log(f"    differing cells over {len(lognormal_identity)} field pairs "
        f"({N**3} cells each): max = {max(lognormal_identity) if lognormal_identity else 0}")

    results = []
    for kind, amps in ladders.items():
        base = {c: np.array(acc[(kind, 0.0, c)]) for c in [cname(r, m) for r, m in cfgs]}
        log(f"\n  === {kind.upper()} LADDER (paired against its own amp=0 member) ===")
        log("  " + " " * 33 + "ROUTE A (share, b=2)" + " " * 21 + "ROUTE B (bispectrum)")
        log(f"  {'amp':>6} {'S3':>9} {'cfg':>5} {'raw':>12} {'floor':>12} "
            f"{'excess':>12} {'+-':>10} {'z':>7} | {'floor':>11} {'excess':>11} "
            f"{'+-':>10} {'z':>7}")
        for amp in amps:
            row = dict(kind=kind, amp=amp, S3=float(np.mean(S3[(kind, amp)])),
                       tied=float(np.mean(ties[(kind, amp)])), cfg={})
            for (r, m) in cfgs:
                c = cname(r, m)
                v = np.array(acc[(kind, amp, c)])
                d = v - base[c]                     # PAIRED difference, same white noise
                rbv = np.array([t[2] for t in cums[(kind, amp, c)]])
                rbb = np.array([t[2] for t in cums[(kind, 0.0, c)]])
                rbd = rbv - rbb                     # Route B, paired the same way
                C, Z = cums[(kind, amp, c)][0][0], cums[(kind, amp, c)][0][1]
                sem = float(d.std(ddof=1) / np.sqrt(len(d))) if len(d) > 1 else np.nan
                rsem = float(rbd.std(ddof=1) / np.sqrt(len(rbd))) if len(rbd) > 1 else np.nan
                row['cfg'][c] = dict(raw=float(v.mean()), floor=float(base[c].mean()),
                                     excess=float(d.mean()), sem=sem,
                                     z=float(d.mean() / sem) if sem and sem > 0 else np.nan,
                                     routeB=float(rbv.mean()),
                                     routeB_floor=float(rbb.mean()),
                                     routeB_excess=float(rbd.mean()), routeB_sem=rsem,
                                     routeB_z=float(rbd.mean() / rsem) if rsem and rsem > 0
                                     else np.nan,
                                     zeta_123=float(Z[0, 1, 2]),
                                     C=C.tolist(), zeta=Z.tolist(),
                                     vals=[float(x) for x in v])
                if m == 'T' or r == 4:
                    e = row['cfg'][c]
                    log(f"  {amp:6g} {row['S3']:9.4f} {c:>5} {e['raw']:12.4e} "
                        f"{e['floor']:12.4e} {e['excess']:12.4e} {e['sem']:10.2e} "
                        f"{e['z']:7.2f} | {e['routeB_floor']:11.4e} "
                        f"{e['routeB_excess']:11.4e} {e['routeB_sem']:10.2e} "
                        f"{e['routeB_z']:7.2f}")
            results.append(row)
    return dict(runs=results, lognormal_max_differing_cells=
                int(max(lognormal_identity)) if lognormal_identity else 0,
                N=N, L=L, R=R, n_real=n_real)


def main_arm2():
    r = arm2()
    json.dump(r, open(os.path.join(HERE, 'sky_pilot_arm2.json'), 'w'), indent=1,
              default=float)
    return r
