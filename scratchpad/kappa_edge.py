"""kappa_edge.py — resolving the kappa = 0.16 route disagreement on CIRISArray.

Pre-registered in scratchpad/KAPPA_EDGE_PREREG.md, committed at f5fa4b4 BEFORE this file
existed.  Three hypotheses, staked in that document:

  H-BLIND        the b=2 structure is real and lives above degree 3; the moment route's
                 He1 (x) He1 (x) He1 projection cannot see it.
  H-MANUFACTURED per-cell coarse-graining does not preserve the pairwise-maxent family
                 (Kadanoff/Wilson: coarse-graining generates operators), so binarizing a
                 continuum whose fine-grained share is ~0 can MANUFACTURE b=2 share.
  H-ZERO        (registered here, disclosed as motivated by a pre-run look at the already
                 collected sweep) the signed whole-only coordinate w crosses zero at
                 kappa ~ 0.167 and s3 = w^2/2, so the 1400x was read at a zero.

Reuses array_negentropy.py's kernel driver, floors and BOTH routes rather than rewriting
them; adds general-b discretisation, an exact pair-maxent projection with a two-sided
certificate, an independent dual solve, and the Hermite localisation.

Credits, openly borrowed and not claimed: coarse-graining generates higher-order operators
(Kadanoff 1966; Wilson 1971); coarse-graining creating connected information measured
(Kahle, Olbrich, Jost & Ay, PRE 79:026201, 2009; our own SKY_PILOT_RESULTS.md sec 7);
connected information of order k (Schneidman, Still, Berry & Bialek 2003; Amari 2001);
iterative proportional fitting (Deming & Stephan 1940; Csiszar 1975 for the I-projection
reading); copula invariance (Sklar 1959; Scherrer, Berlind, Mao & McBride 2010).
Assume convergence.

Usage:
    python3 kappa_edge.py --gate
    python3 kappa_edge.py --e0      # the zero crossing        (H-ZERO)
    python3 kappa_edge.py --e1      # fine-b surrogate + b-ladder + Hermite  (DECISIVE)
    python3 kappa_edge.py --e4      # on-off decomposition
    python3 kappa_edge.py --dose    # kappa_0 vs settle length
"""
import sys, os, json, time, argparse, itertools, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/emoore/CIRISArray')
sys.path.insert(0, '/home/emoore/CIRISArray/src')
sys.path.insert(0, HERE)

import array_negentropy as AN
import array_cap_experiment as ACE

LN2 = float(np.log(2))
SEED = 20260725


# =====================================================================================
# GENERAL-b SHARE MACHINERY  (ACE's is hardwired to b=2)
# =====================================================================================

def H(p):
    p = np.asarray(p, dtype=float).ravel()
    p = p[p > 1e-300]
    return float(-np.sum(p * np.log(p)))


def pair_marg3(p, i, j):
    """(i,j) pair marginal of a 3-slot state of arbitrary alphabet size."""
    k = 3 - i - j
    return p.sum(axis=k)


def pairwise_maxent3(p, iters=200000, tol=1e-14):
    """IPF from uniform to the maxent state carrying p's three pair marginals.
    The I-projection of uniform onto the pair envelope; at b=2 this is ACE's routine."""
    b = p.shape[0]
    prs = ((0, 1), (0, 2), (1, 2))
    marg = {ij: pair_marg3(p, *ij) for ij in prs}
    q = np.full(p.shape, 1.0 / p.size)
    err = np.inf
    for it in range(iters):
        for (i, j) in prs:
            qij = pair_marg3(q, i, j)
            ratio = np.where(qij > 0, marg[(i, j)] / np.where(qij > 0, qij, 1.0), 0.0)
            sh = [1, 1, 1]; sh[i] = b; sh[j] = b
            q = q * ratio.reshape(sh)
        err = max(float(np.abs(pair_marg3(q, i, j) - marg[(i, j)]).max()) for (i, j) in prs)
        if err < tol:
            break
    return q, err, it + 1


def share3(p, **kw):
    """shareK at k=3 for arbitrary alphabet size: sSup(pair envelope) - H(p)."""
    q, err, nit = pairwise_maxent3(p, **kw)
    return H(q) - H(p), q, err, nit


def interaction_certificate(q, nsamp=40000, rng=None):
    """The DUAL half of the certificate.  q is the pairwise maxent iff log q is a sum of
    three functions of coordinate pairs; equivalently the eight-term alternating sum

        L(x,y,z) - L(x',y,z) - L(x,y',z) - L(x,y,z')
                 + L(x',y',z) + L(x',y,z') + L(x,y',z') - L(x',y',z')      (L = log q)

    vanishes for every index sextuple.  Together with a zero pair-marginal residual this
    identifies the unique I-projection.  Sampled over random sextuples with all eight
    cells strictly positive; returns the max |.| found."""
    if rng is None:
        rng = np.random.default_rng(0)
    b = q.shape[0]
    if b < 2:
        return 0.0
    L = np.log(np.where(q > 0, q, np.nan))
    x = rng.integers(0, b, nsamp); X = rng.integers(0, b, nsamp)
    y = rng.integers(0, b, nsamp); Y = rng.integers(0, b, nsamp)
    z = rng.integers(0, b, nsamp); Z = rng.integers(0, b, nsamp)
    s = (L[x, y, z] - L[X, y, z] - L[x, Y, z] - L[x, y, Z]
         + L[X, Y, z] + L[X, y, Z] + L[x, Y, Z] - L[X, Y, Z])
    s = s[np.isfinite(s)]
    return float(np.abs(s).max()) if s.size else float('nan')


def pairwise_maxent3_dual(p, tol=1e-14):
    """INDEPENDENT solve of the same projection by convex duality, so the IPF answer is
    never trusted alone (ISING_FIELD_RESULTS.md sec 2: IPF read 9.8e-6 where the truth was
    1.2e-10).  Minimise

        Phi(f,g,h) = log sum_xyz exp(f_xy + g_xz + h_yz)
                     - <M01, f> - <M02, g> - <M12, h>

    whose gradient is (pair marginal of q) - (target pair marginal)."""
    from scipy.optimize import minimize
    b = p.shape[0]
    M01 = pair_marg3(p, 0, 1); M02 = pair_marg3(p, 0, 2); M12 = pair_marg3(p, 1, 2)
    n = b * b

    def unpack(th):
        return (th[:n].reshape(b, b), th[n:2 * n].reshape(b, b), th[2 * n:].reshape(b, b))

    def qof(f, g, h):
        a = f[:, :, None] + g[:, None, :] + h[None, :, :]
        mx = float(a.max())
        e = np.exp(a - mx)
        return e / e.sum(), mx + np.log(e.sum())

    def fun(th):
        f, g, h = unpack(th)
        q, lz = qof(f, g, h)
        val = lz - float((M01 * f).sum() + (M02 * g).sum() + (M12 * h).sum())
        gr = np.concatenate([(pair_marg3(q, 0, 1) - M01).ravel(),
                             (pair_marg3(q, 0, 2) - M02).ravel(),
                             (pair_marg3(q, 1, 2) - M12).ravel()])
        return val, gr

    th = np.zeros(3 * n)
    for _ in range(6):          # warm restarts: the dual has an exact gauge freedom
        res = minimize(fun, th, jac=True, method='L-BFGS-B',
                       options=dict(maxiter=50000, maxfun=100000, ftol=1e-16, gtol=1e-16,
                                    maxcor=30))
        if np.allclose(res.x, th, rtol=0, atol=0):
            break
        th = res.x
    f, g, h = unpack(res.x)
    q, _ = qof(f, g, h)
    err = max(float(np.abs(pair_marg3(q, i, j) - m).max())
              for (i, j), m in (((0, 1), M01), ((0, 2), M02), ((1, 2), M12)))
    return q, err, res.nit


def coarse2(q):
    """Exact coarse-graining of an even-b table to 2x2x2 by the MEDIAN split.  With
    equiprobable (quantile) bins and b even the median falls exactly on a bin boundary, so
    this is the published b=2 statistic and not an approximation of it."""
    b = q.shape[0]
    assert b % 2 == 0
    h = b // 2
    return q.reshape(2, h, 2, h, 2, h).sum(axis=(1, 3, 5))


# =====================================================================================
# DISCRETISATION
# =====================================================================================

def qbin(X, b):
    """Per-channel equiprobable binning on pooled empirical quantiles.  X (N,3)."""
    idx = np.empty(X.shape, dtype=np.int32)
    ties = []
    for j in range(3):
        x = X[:, j]
        qs = np.quantile(x, np.arange(1, b) / b)
        idx[:, j] = np.searchsorted(qs, x, side='right')
        ties.append(float(np.mean(np.isin(x, qs))))
    return idx, ties


def joint(idx, b):
    lin = (idx[:, 0].astype(np.int64) * b + idx[:, 1]) * b + idx[:, 2]
    cnt = np.bincount(lin, minlength=b ** 3).astype(float)
    return cnt.reshape(b, b, b) / cnt.sum()


# =====================================================================================
# HERMITE LOCALISATION
# =====================================================================================

def hermite_e(n, x):
    """Probabilists' He_n."""
    x = np.asarray(x, dtype=float)
    h0 = np.ones_like(x)
    if n == 0:
        return h0
    h1 = x.copy()
    for k in range(1, n):
        h0, h1 = h1, x * h1 - k * h0
    return h1


def bin_reps(b):
    """Gaussianized bin centroids v_j = b (phi(z_j) - phi(z_{j+1})), z_j = Phi^-1(j/b),
    rescaled to unit variance so the He_n are orthonormal on the discretised marginal."""
    from scipy.stats import norm
    z = norm.ppf(np.arange(b + 1) / b)
    ph = norm.pdf(z)
    ph[0] = 0.0; ph[-1] = 0.0
    v = b * (ph[:-1] - ph[1:])
    v = v - v.mean()
    return v / np.sqrt(float((v ** 2).mean()))


def hermite_table(p, v, nmax=5):
    """G[i,j,k] = E_p[He_i(vx) He_j(vy) He_k(vz)] / sqrt(i! j! k!), i,j,k = 0..nmax."""
    A = np.stack([hermite_e(i, v) / np.sqrt(float(math.factorial(i)))
                  for i in range(nmax + 1)])
    return np.einsum('xyz,ix,jy,kz->ijk', p, A, A, A, optimize=True)


SIGN_COEF = {m: (np.sqrt(2.0 / np.pi) * hermite_e(m - 1, np.array([0.0]))[0]
                 / float(math.factorial(m))) for m in (1, 3, 5, 7)}


def sign_triple_from_hermite(p, v, mmax):
    """Reconstruct E[sgn x sgn y sgn z] from odd Hermite triples up to index mmax.
    sgn(x) = sum_{m odd} (a_m/m!) He_m(x), a_m = sqrt(2/pi) He_{m-1}(0)."""
    odd = [m for m in (1, 3, 5, 7) if m <= mmax]
    A = {m: hermite_e(m, v) for m in odd}
    tot = 0.0
    for i in odd:
        for j in odd:
            for k in odd:
                c = SIGN_COEF[i] * SIGN_COEF[j] * SIGN_COEF[k]
                tot += c * float(np.einsum('xyz,x,y,z->', p, A[i], A[j], A[k],
                                           optimize=True))
    return tot


def sign_triple_exact(p):
    """E[s1 s2 s3] from the exact 2x2x2 coarse-graining (b even)."""
    c = coarse2(p)
    s = np.array([-1.0, 1.0])
    return float(np.einsum('xyz,x,y,z->', c, s, s, s))


# =====================================================================================
# THE ARRAY DRIVER — one collection, both routes, guaranteed same frames
# =====================================================================================

def collect(drv, kappa, sigma, boundary, seed, settle, nframes):
    """Drive the SHIPPED kernel at iterations=1. Returns raw float32 states (nframes,3,T),
    the rail fractions and the clamp-binding rate."""
    cp = AN._cp()
    drv.rt.configure_ossicles(r_base=3.70, r_spacing=0.03, twist_deg=1.1,
                              coupling=kappa, n_cells=drv.ncells, iterations=1)
    oss = drv.rt.array.ossicles
    cp.random.seed(seed)
    oss.states = cp.random.uniform(0.2, 0.8, (drv.n, 3, drv.ncells), dtype=cp.float32)
    clipbuf = cp.zeros(drv.n, dtype=cp.float32)
    args = (oss.states, oss.outputs, oss.baselines, oss.gpu_params,
            cp.int32(drv.n), cp.int32(drv.ncells), cp.int32(1), clipbuf)
    kern = drv.kernel(boundary)
    grid = ((drv.n + 255) // 256,); block = (256,)

    def burst():
        if sigma > 0:
            oss.states += cp.random.normal(0, sigma, oss.states.shape).astype(cp.float32)
        clipbuf.fill(0)
        kern(grid, block, args)

    for _ in range(settle):
        burst()
    R = cp.empty((nframes, 3, drv.T), dtype=cp.float32)
    rails = np.zeros((nframes, 3, 2))
    ctot = 0.0
    denom = float(drv.n * 3 * drv.ncells)
    for t in range(nframes):
        burst()
        for j in range(3):
            raw = oss.states[:, j, :].ravel()
            rails[t, j] = AN.rail_fraction(raw)
            R[t, j] = raw
        ctot += float(clipbuf.sum()) / denom
    cp.cuda.Stream.null.synchronize()
    return R, rails, ctot / nframes


def gaussianize_all(R):
    cp = AN._cp()
    nf, _, T = R.shape
    G = cp.empty((nf, 3, T), dtype=cp.float64)
    for t in range(nf):
        for j in range(3):
            G[t, j] = AN.gaussianize(R[t, j])
    return G


def triple_raw(R, d=1, chan=1, nonoverlap=True):
    """The temporal triple (x_t, x_{t+d}, x_{t+2d}) on one channel, stacked over
    NON-OVERLAPPING start frames so the rows are independent replicas."""
    cp = AN._cp()
    nf = R.shape[0]
    step = 3 * d if nonoverlap else 1
    starts = list(range(0, nf - 2 * d, step))
    cols = [cp.asnumpy(cp.concatenate([R[s + j * d, chan] for s in starts]).astype(cp.float64))
            for j in range(3)]
    return np.column_stack(cols), len(starts)


# =====================================================================================
# GATE — my own new machinery.  FAIL => no array number is believed.
# =====================================================================================

def gate(verbose=True):
    P = (lambda s: print(s)) if verbose else (lambda s: None)
    ok = True
    rng = np.random.default_rng(SEED)
    P("=" * 86)
    P("GATE — general-b share machinery, the certificate, and the coarse-graining test")
    P("=" * 86)

    # Ga: a product distribution has share exactly 0 at any b
    for b in (3, 4, 8):
        m = [rng.random(b) for _ in range(3)]
        m = [x / x.sum() for x in m]
        p = np.einsum('x,y,z->xyz', *m)
        s = share3(p)[0]
        P(f"Ga  product distribution b={b:<3} share = {s:+.3e}   (|.| < 1e-12 required)")
        ok &= abs(s) < 1e-12

    # Gb: at b=2 my routine equals ACE's, bit for bit in the reported share
    for _ in range(4):
        p = rng.random((2, 2, 2)); p /= p.sum()
        s_mine = share3(p)[0]; s_ace = ACE.shareK(p)[0]
        d = abs(s_mine - s_ace)
        ok &= d < 1e-13
    P(f"Gb  b=2 agreement with array_cap_experiment.shareK: max |diff| = {d:.2e}"
      f"   (< 1e-13 required)")

    # Gc: the interaction certificate has TEETH — ~0 on the projection, large on the data
    p = rng.random((6, 6, 6)) ** 3; p /= p.sum()
    q, err, nit = pairwise_maxent3(p)
    cq = interaction_certificate(q, rng=np.random.default_rng(1))
    cp_ = interaction_certificate(p, rng=np.random.default_rng(1))
    P(f"Gc  interaction certificate: on IPF projection {cq:.2e} (< 1e-9 required), "
      f"on the raw data {cp_:.2e} (must be >> that)   [ipf err {err:.1e}, {nit} its]")
    ok &= cq < 1e-9 and cp_ > 1e-3

    # Gd: the independent dual solve reproduces H(q).
    # THRESHOLD NOTE, so no one has to wonder whether a bar was moved: this gate is set at
    # the K-VOID threshold frozen in KAPPA_EDGE_PREREG.md sec 5, |dH| < 1e-8.  My first
    # draft asked 1e-10 and the dual floors at ~3e-10 for a structural reason -- the dual
    # has an exact gauge freedom (f -> f+c, g -> g-c leaves q invariant), so the Hessian is
    # singular and a first-order method cannot drive the gradient below ~1e-10.  IPF's own
    # marginal residual (~4e-15) is the tight one; the dual's job is INDEPENDENT
    # confirmation, not precision.  The achieved value is printed, not just the verdict.
    for b in (4, 8):
        p = rng.random((b, b, b)) ** 2; p /= p.sum()
        qi, ei, _ = pairwise_maxent3(p)
        qd, ed, nit = pairwise_maxent3_dual(p)
        dH = abs(H(qi) - H(qd))
        P(f"Gd  dual vs IPF b={b:<3} |dH| = {dH:.3e}  (< 1e-8 = the pre-registered K-VOID "
          f"bar) | marg resid ipf {ei:.1e} dual {ed:.1e}")
        ok &= dH < 1e-8

    # Ge: SIGN-SYMMETRIC fine structure coarse-grains to EXACTLY zero b=2 share.
    #     This is Core/SignSymmetry.lean's share_eq_zero_of_signSymmetric used as a
    #     control on my coarse-graining code: the test CANNOT fire on a symmetric field.
    for b in (4, 8, 16):
        p = rng.random((b, b, b)) ** 2
        p = p + p[::-1, ::-1, ::-1]
        p /= p.sum()
        q = pairwise_maxent3(p)[0]
        s2 = share3(coarse2(q))[0]
        P(f"Ge  sign-symmetric fine dist, b={b:<3} -> coarse-grained b=2 share = {s2:+.2e}"
          f"   (|.| < 1e-12 required; the Lean lemma)")
        ok &= abs(s2) < 1e-12

    # Gf: an ASYMMETRIC fine pairwise-maxent DOES manufacture b=2 share — the test can fire
    p = rng.random((8, 8, 8)) ** 3; p /= p.sum()
    q = pairwise_maxent3(p)[0]
    s2 = share3(coarse2(q))[0]
    P(f"Gf  asymmetric fine pair-maxent -> coarse-grained b=2 share = {s2:.3e}"
      f"   (> 1e-6 required: manufacture is POSSIBLE, so a null in E1 is informative)")
    ok &= s2 > 1e-6

    # Gg: Delta G vanishes exactly whenever any Hermite index is 0 (shared pair marginals)
    b = 8
    p = rng.random((b, b, b)) ** 2; p /= p.sum()
    q = pairwise_maxent3(p)[0]
    v = bin_reps(b)
    dG = hermite_table(p, v) - hermite_table(q, v)
    mask = np.zeros_like(dG, dtype=bool)
    for i in range(dG.shape[0]):
        for j in range(dG.shape[1]):
            for k in range(dG.shape[2]):
                if i == 0 or j == 0 or k == 0:
                    mask[i, j, k] = True
    P(f"Gg  max |Delta G| over entries with a zero index = {np.abs(dG[mask]).max():.2e}"
      f"   (< 1e-12 required)  | max over all-indices>=1 = {np.abs(dG[~mask]).max():.2e}")
    ok &= np.abs(dG[mask]).max() < 1e-12

    # Gh: for b even, the quantile-bin median split IS the continuum median split
    x = rng.standard_normal((100000, 3)) @ np.array([[1, .5, .2], [0, .8, .3], [0, 0, .7]])
    for b in (2, 8, 32):
        idx, ties = qbin(x, b)
        a = (idx >= b // 2).astype(np.int8)
        c = np.column_stack([ACE.binarize_median(x[:, j])[0] for j in range(3)])
        agree = int(np.abs(a - c).max())
        P(f"Gh  b={b:<3} median split identical to binarize_median: max diff = {agree}"
          f"   (0 required) | tie fractions {['%.1e' % t for t in ties]}")
        ok &= agree == 0

    # Gi: the Hermite table reproduces directly computed moments, exactly
    b = 32
    v = bin_reps(b)
    idx, _ = qbin(x, b)
    p = joint(idx, b)
    GT = hermite_table(p, v)
    vx = v[idx[:, 0]]; vy = v[idx[:, 1]]; vz = v[idx[:, 2]]
    d111 = abs(GT[1, 1, 1] - float((vx * vy * vz).mean()))
    d110 = abs(GT[1, 1, 0] - float((vx * vy).mean()))
    P(f"Gi  Hermite table vs direct moments: |dG111| = {d111:.2e}  |dG110| = {d110:.2e}"
      f"   (< 1e-12 required)")
    ok &= d111 < 1e-12 and d110 < 1e-12

    # Gj: on an INDEPENDENT triple with a symmetric marginal the sign-triple reconstruction
    # is exactly 0 at every truncation -- the reconstruction cannot invent a triple.
    m1 = rng.random(b); m1 = (m1 + m1[::-1]); m1 /= m1.sum()
    pi_ = np.einsum('x,y,z->xyz', m1, m1, m1)
    rec0 = [sign_triple_from_hermite(pi_, v, m) for m in (1, 3, 5, 7)]
    P(f"Gj  independent symmetric triple, sign reconstruction at m<=1,3,5,7: "
      f"{' '.join('%+.1e' % r for r in rec0)}   (all |.| < 1e-12 required)")
    ok &= max(abs(r) for r in rec0) < 1e-12

    # Gk: DISCLOSED, NOT GATING -- the truncated sgn series converges only in L2 and has a
    # Gibbs overshoot at 0, so the ABSOLUTE reconstruction of a sign triple is poor at
    # m <= 7.  It is used only on the DIFFERENCE data - surrogate, where the same
    # truncation is applied to both and the truncation error largely cancels.  The size of
    # the absolute error is measured here and reported rather than hidden.
    ex = sign_triple_exact(p)
    rec = [sign_triple_from_hermite(p, v, m) for m in (1, 3, 5, 7)]
    P(f"Gk  [DISCLOSED, not gating] correlated-Gaussian sign triple exact = {ex:+.6f} | "
      f"truncated {' '.join('%+.6f' % r for r in rec)} -> the m<=7 truncation error on an "
      f"ABSOLUTE sign triple is {abs(rec[-1]-ex):.1e}; only differences are quoted")

    P(f"\nGATE VERDICT: {'PASS' if ok else 'FAIL'}")
    return ok


# =====================================================================================
# E0 — the zero crossing
# =====================================================================================

def moment_reading(G, d=1, chan=1):
    r = AN.reading(G, [(0, chan), (d, chan), (2 * d, chan)])
    C = np.array(r['C_mean'])
    r['rho_max'] = float(max(abs(C[0, 1]), abs(C[0, 2]), abs(C[1, 2])))
    return r


def bin_reading(R, d=1, chan=1, n_surr=32, seed=SEED):
    X, nst = triple_raw(R, d=d, chan=chan)
    a = ACE.analyze([X[:, 0], X[:, 1], X[:, 2]], f'bin-d{d}', n_surr=n_surr, n_shuf=4,
                    rng=np.random.default_rng(seed))
    a['n_starts'] = nst
    return a, X


def stage_e0(args):
    cp = AN._cp()
    drv = AN.Driver(args.rows, args.cols)
    kaps = [round(0.140 + 0.005 * i, 4) for i in range(13)]
    arms = [('fold', 1e-3), ('clip', 1e-3), ('fold', 1e-2)]
    out = []
    for boundary, sigma in arms:
        print(f"\n--- E0 arm: {boundary}, sigma = {sigma} " + "-" * 40)
        for kap in kaps:
            t0 = time.time()
            R, rails, clamp = collect(drv, kap, sigma, boundary, args.seed,
                                      args.settle, args.nframes)
            G = gaussianize_all(R)
            m = moment_reading(G)
            bb, X = bin_reading(R, seed=args.seed)
            del G
            rec = dict(kappa=kap, sigma=sigma, boundary=boundary,
                       w=m['w_mean'][0], w_se=m['w_se'][0], s3=m['s_deb'],
                       z_mom=m['z'], z_cons=m['z_cons'], tau=m['tau'][0],
                       rho_max=m['rho_max'], C=m['C_mean'], kappa111=m['kappa111'],
                       rail=float(rails[:, :, 0].max()), clamp=clamp,
                       s_bin=bb['excess'], s_bin_raw=bb['share'], z_bin=bb['z'],
                       tie=bb['tie_max'], n_bin=bb['T'], null_bin=bb['null_mean'],
                       ratio=(bb['excess'] / m['s_deb'] if m['s_deb'] > 0 else float('inf')))
            out.append(rec)
            print(f"  k={kap:<6} w={rec['w']:+.5e}+-{rec['w_se']:.1e}  s3={rec['s3']:.4e} "
                  f"z={rec['z_mom']:+8.1f} | s_bin={rec['s_bin']:.4e} z={rec['z_bin']:+9.1f} "
                  f"tie={rec['tie']:.1e} | ratio={rec['ratio']:9.1f} rail={rec['rail']:.4f} "
                  f"rho={rec['rho_max']:.3f}  [{time.time()-t0:.0f}s]")
            del R
            cp.get_default_memory_pool().free_all_blocks()
    # locate kappa_0 per arm by linear interpolation of w
    for boundary, sigma in arms:
        sub = sorted([r for r in out if r['boundary'] == boundary and r['sigma'] == sigma],
                     key=lambda r: r['kappa'])
        k0 = None
        for a, b in zip(sub[:-1], sub[1:]):
            if a['w'] * b['w'] < 0:
                k0 = a['kappa'] + (b['kappa'] - a['kappa']) * abs(a['w']) / (abs(a['w']) + abs(b['w']))
                break
        print(f"\n  ZERO CROSSING [{boundary}, sigma={sigma}]: kappa_0 = "
              f"{('%.4f' % k0) if k0 else 'NONE IN WINDOW'}")
        out.append(dict(tag='K0', boundary=boundary, sigma=sigma, kappa_0=k0))
    with open(os.path.join(HERE, 'kappa_edge_e0.json'), 'w') as f:
        json.dump(out, f, indent=1, default=float)
    return out


# =====================================================================================
# E1 / E2 / E3 — the fine-b surrogate, the b-ladder, the Hermite localisation
# =====================================================================================

def ladder_point(X, b, n_surr, rng, want_dual=False, want_hermite=False):
    """One rung: level-b share of the data, its matched pair-maxent floor, and (optionally)
    the coarse-grained surrogate reproduction and the Hermite localisation."""
    N = X.shape[0]
    idx, ties = qbin(X, b)
    P = joint(idx, b)
    s, Q, err, nit = share3(P)
    cert = interaction_certificate(Q, rng=np.random.default_rng(7))
    rec = dict(b=b, N=int(N), tie_max=float(max(ties)), share=s, ipf_err=err, ipf_iters=nit,
               cert=cert, H_p=H(P), H_q=H(Q), nz_cells=int((P > 0).sum()), cells=b ** 3)
    if want_dual:
        qd, ed, nid = pairwise_maxent3_dual(P)
        rec.update(dual_dH=abs(H(Q) - H(qd)), dual_err=ed, dual_iters=int(nid))
    # matched pair-maxent multinomial floor = the estimator bias at this b (truth 0)
    flat = np.clip(Q.ravel(), 0, None); flat /= flat.sum()
    vals = np.empty(n_surr)
    for i in range(n_surr):
        c = rng.multinomial(N, flat).reshape(P.shape).astype(float)
        vals[i] = share3(c / c.sum())[0]
    rec.update(floor_mean=float(vals.mean()), floor_sd=float(vals.std(ddof=1)))
    rec['excess'] = s - rec['floor_mean']
    rec['z'] = rec['excess'] / rec['floor_sd'] if rec['floor_sd'] > 0 else float('nan')
    # matched-GAUSSIAN floor, for comparability with SKY_PILOT sec 3
    if b >= 2:
        v = bin_reps(b)
        C = np.corrcoef(np.stack([v[idx[:, j]] for j in range(3)]))
        try:
            L = np.linalg.cholesky(C + 1e-12 * np.eye(3))
            g = (L @ rng.standard_normal((3, min(N, 4_000_000)))).T
            gi, _ = qbin(g, b)
            rec['floor_gauss'] = share3(joint(gi, b))[0]
        except np.linalg.LinAlgError:
            rec['floor_gauss'] = float('nan')
    if b % 2 == 0:
        # E1 — the decisive reproduction test
        cP = coarse2(P); cQ = coarse2(Q)
        s2_data = share3(cP)[0]
        s2_surr = share3(cQ)[0]
        rec['s2_data'] = s2_data
        rec['s2_surrogate_exact'] = s2_surr
        rec['F'] = s2_surr / s2_data if s2_data > 0 else float('nan')
        # and the finite-sample version at matched N
        sv = np.empty(min(n_surr, 64))
        for i in range(sv.size):
            c = rng.multinomial(N, flat).reshape(P.shape).astype(float)
            sv[i] = share3(coarse2(c / c.sum()))[0]
        rec['s2_surrogate_samp'] = float(sv.mean())
        rec['s2_surrogate_samp_sd'] = float(sv.std(ddof=1))
        rec['sign_triple_data'] = sign_triple_exact(P)
        rec['sign_triple_surr'] = sign_triple_exact(Q)
    if want_hermite:
        v = bin_reps(b)
        GP = hermite_table(P, v); GQ = hermite_table(Q, v)
        dG = GP - GQ
        zi = np.abs([dG[i, j, k] for i in range(6) for j in range(6) for k in range(6)
                     if i == 0 or j == 0 or k == 0]).max()
        rec['dG_zeroindex_max'] = float(zi)
        rec['G_data'] = GP.tolist(); rec['G_surr'] = GQ.tolist()
        rec['sign_recon_data'] = [sign_triple_from_hermite(P, v, m) for m in (1, 3, 5, 7)]
        rec['sign_recon_surr'] = [sign_triple_from_hermite(Q, v, m) for m in (1, 3, 5, 7)]
    return rec


def stage_e1(args):
    cp = AN._cp()
    drv = AN.Driver(args.rows, args.cols)
    rng = np.random.default_rng(args.seed)
    out = []
    pts = [(float(a), float(b)) for a, b in (p.split(':') for p in args.points.split(','))]
    for (kap, sigma) in pts:
        for boundary in ('fold', 'clip') if args.both else ('fold',):
            print(f"\n{'='*86}\nE1/E2/E3 at kappa={kap} sigma={sigma} {boundary}\n{'='*86}")
            R, rails, clamp = collect(drv, kap, sigma, boundary, args.seed,
                                      args.settle, args.nframes)
            G = gaussianize_all(R)
            m = moment_reading(G)
            del G
            cp.get_default_memory_pool().free_all_blocks()
            X, nst = triple_raw(R, d=1, chan=1)
            print(f"  rail={rails[:,:,0].max():.4f} clamp={clamp:.3e} | moment route "
                  f"w={m['w_mean'][0]:+.5e} s3={m['s_deb']:.4e} z={m['z']:+.1f} "
                  f"rho_max={m['rho_max']:.3f} tau={m['tau'][0]:.2f}")
            print(f"  triples: {X.shape[0]} rows from {nst} NON-OVERLAPPING start frames")
            head = dict(kappa=kap, sigma=sigma, boundary=boundary,
                        rail=float(rails[:, :, 0].max()), clamp=clamp,
                        w=m['w_mean'][0], s3=m['s_deb'], z_mom=m['z'],
                        rho_max=m['rho_max'], tau=m['tau'][0], kappa111=m['kappa111'])
            for b in (2, 3, 4, 6, 8, 16, 32):
                t0 = time.time()
                rec = ladder_point(X, b, args.nsurr, rng,
                                   want_dual=(b <= 16), want_hermite=(b in (8, 16, 32)))
                rec.update(head); rec['tag'] = 'LADDER'
                out.append(rec)
                extra = ''
                if 'F' in rec:
                    extra = (f" | s2_data={rec['s2_data']:.4e} s2_surr={rec['s2_surrogate_exact']:.4e}"
                             f" F={rec['F']:.4f}")
                print(f"  b={b:<3} share={rec['share']:.4e} floor={rec['floor_mean']:.3e}"
                      f" excess={rec['excess']:+.4e} z={rec['z']:+9.1f}"
                      f" cert={rec['cert']:.1e} ipf={rec['ipf_err']:.1e}"
                      f"{'' if 'dual_dH' not in rec else ' dual_dH=%.1e' % rec['dual_dH']}"
                      f"{extra}  [{time.time()-t0:.0f}s]")
            # floors on the primary reading
            sh = ACE.shuffle_floor(np.column_stack(
                [ACE.binarize_median(X[:, j])[0] for j in range(3)]), n_shuf=8,
                rng=np.random.default_rng(args.seed))
            print(f"  SHUFFLE floor (b=2): {sh[0]:+.3e} +- {sh[1]:.1e}")
            out.append(dict(tag='SHUFFLE', kappa=kap, sigma=sigma, boundary=boundary,
                            mean=sh[0], sd=sh[1]))
            del R, X
            cp.get_default_memory_pool().free_all_blocks()
    with open(os.path.join(HERE, 'kappa_edge_e1.json'), 'w') as f:
        json.dump(out, f, indent=1, default=float)
    return out


# =====================================================================================
# E4 — the on-off decomposition
# =====================================================================================

def stage_e4(args):
    cp = AN._cp()
    drv = AN.Driver(args.rows, args.cols)
    out = []
    pts = [(float(a), float(b)) for a, b in (p.split(':') for p in args.points.split(','))]
    for (kap, sigma) in pts:
        R, rails, clamp = collect(drv, kap, sigma, 'fold', args.seed,
                                  args.settle, args.nframes)
        # per (replica, frame) sync error on the RAW states; laminar = below pooled median
        E = cp.abs(R[:, 0] - R[:, 1]) + cp.abs(R[:, 1] - R[:, 2])       # (nf, T)
        med = float(cp.median(E))
        L = (E < med).astype(cp.float32)
        nf = R.shape[0]
        starts = list(range(0, nf - 2, 3))
        Lc = [cp.asnumpy(cp.concatenate([L[s + j] for s in starts])) for j in range(3)]
        Xc, _ = triple_raw(R, d=1, chan=1)
        lam = np.column_stack(Lc).astype(np.int8)
        rng = np.random.default_rng(args.seed)
        full = ACE.analyze([Xc[:, 0], Xc[:, 1], Xc[:, 2]], 'full', n_surr=32, n_shuf=4,
                           rng=rng)
        pI, TI = ACE.emp_dist(lam)
        sI = share3(pI)[0]
        fl = ACE.surrogate_null(pI, TI, n_surr=32, rng=rng)
        sub = {}
        for name, sel in (('laminar', lam.sum(axis=1) == 3), ('burst', lam.sum(axis=1) == 0)):
            n = int(sel.sum())
            if n < 10000:
                sub[name] = dict(n=n, excess=float('nan'))
                continue
            a = ACE.analyze([Xc[sel, 0], Xc[sel, 1], Xc[sel, 2]], name, n_surr=32, n_shuf=4,
                            rng=rng)
            sub[name] = dict(n=n, share=a['share'], excess=a['excess'], z=a['z'],
                             tie=a['tie_max'])
        rec = dict(tag='E4', kappa=kap, sigma=sigma, boundary='fold', sync_median=med,
                   full_share=full['share'], full_excess=full['excess'], full_z=full['z'],
                   indicator_share=sI, indicator_floor=fl[0], indicator_sd=fl[1],
                   indicator_excess=sI - fl[0], lam_frac=float(lam.mean()), **{
                       f'{k}_{kk}': vv for k, v in sub.items() for kk, vv in v.items()})
        out.append(rec)
        print(f"\nE4 kappa={kap}: full amplitude-triple excess = {full['excess']:.4e}")
        print(f"   indicator-triple excess            = {sI - fl[0]:.4e}  "
              f"(ratio {(sI-fl[0])/full['excess']:.3f})")
        for name in ('laminar', 'burst'):
            e = sub[name].get('excess', float('nan'))
            print(f"   within-{name:<8} amplitude excess = {e:.4e}  "
                  f"(ratio {e/full['excess']:.3f}, n={sub[name]['n']})")
        del R, E, L
        cp.get_default_memory_pool().free_all_blocks()
    with open(os.path.join(HERE, 'kappa_edge_e4.json'), 'w') as f:
        json.dump(out, f, indent=1, default=float)
    return out


# =====================================================================================
# DOSE — does kappa_0 move with the settle length?
# =====================================================================================

def stage_dose(args):
    cp = AN._cp()
    drv = AN.Driver(args.rows, args.cols)
    out = []
    for settle in (500, 2000, 8000):
        ws = []
        for kap in (0.150, 0.160, 0.170, 0.180):
            R, rails, clamp = collect(drv, kap, 1e-3, 'fold', args.seed, settle, 256)
            G = gaussianize_all(R)
            m = moment_reading(G)
            ws.append((kap, m['w_mean'][0], m['s_deb']))
            print(f"  settle={settle:<6} k={kap:<6} w={m['w_mean'][0]:+.5e} "
                  f"s3={m['s_deb']:.4e}")
            del R, G
            cp.get_default_memory_pool().free_all_blocks()
        k0 = None
        for a, b in zip(ws[:-1], ws[1:]):
            if a[1] * b[1] < 0:
                k0 = a[0] + (b[0] - a[0]) * abs(a[1]) / (abs(a[1]) + abs(b[1]))
                break
        print(f"  settle={settle}: kappa_0 = {('%.4f' % k0) if k0 else 'NONE'}")
        out.append(dict(settle=settle, kappa_0=k0, w=[list(x) for x in ws]))
    with open(os.path.join(HERE, 'kappa_edge_dose.json'), 'w') as f:
        json.dump(out, f, indent=1, default=float)
    return out


# =====================================================================================

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gate', action='store_true')
    ap.add_argument('--e0', action='store_true')
    ap.add_argument('--e1', action='store_true')
    ap.add_argument('--e4', action='store_true')
    ap.add_argument('--dose', action='store_true')
    ap.add_argument('--rows', type=int, default=8)
    ap.add_argument('--cols', type=int, default=64)
    ap.add_argument('--settle', type=int, default=2000)
    ap.add_argument('--nframes', type=int, default=512)
    ap.add_argument('--nsurr', type=int, default=32)
    ap.add_argument('--seed', type=int, default=SEED)
    ap.add_argument('--points', type=str, default='0.16:1e-3,0.05:1e-3,0.30:1e-3')
    ap.add_argument('--both', action='store_true')
    ap.add_argument('--skipgate', action='store_true')
    args = ap.parse_args()

    if not args.skipgate:
        if not gate():
            print("GATE FAILED — the run is VOID. Refusing to report array numbers.")
            return 1
    if args.gate and not (args.e0 or args.e1 or args.e4 or args.dose):
        return 0
    import cupy as cp
    print(f"\nDEVICE: {cp.cuda.runtime.getDeviceProperties(0)['name'].decode()}")
    if args.e0:
        print("\n" + "=" * 86 + "\nE0 — the zero crossing (H-ZERO)\n" + "=" * 86)
        stage_e0(args)
    if args.e1:
        print("\n" + "=" * 86 +
              "\nE1/E2/E3 — fine-b surrogate, b-ladder, Hermite localisation\n" + "=" * 86)
        stage_e1(args)
    if args.e4:
        print("\n" + "=" * 86 + "\nE4 — the on-off decomposition\n" + "=" * 86)
        stage_e4(args)
    if args.dose:
        print("\n" + "=" * 86 + "\nDOSE — kappa_0 vs settle length\n" + "=" * 86)
        stage_dose(args)
    return 0


if __name__ == '__main__':
    sys.exit(main())
