"""phi4_ridge.py — the pairwise-blind order-3 share I_C^(3) on 3D lattice phi^4,
through the Wilson-Fisher critical region.

Pre-registered in scratchpad/PHI4_RIDGE_PREREG.md, committed at 7ea57ea BEFORE this
file existed.

SCOPE.  A model computation in the 3D Ising universality class -- which is the
classical-critical universality class of the Higgs sector's scalar.  That is a statement
about a universality class.  Nothing here is about the Higgs, or about nature.

WHY.  The 2D siblings (ISING_FIELD_RESULTS.md, CFT_RIDGE_RESULTS.md) found the order-3
share peaks at criticality under weak symmetry breaking, on a ridge at h* ~ L^(-15/8),
carried by separated triples, mechanism = the CFT magnetisation sector.  The 3D Ising
class has y_h = 2.4819 against 2D's 1.875 and 6*beta/nu = 3.109 against 0.75, so
measuring the same phenomenon here DISCRIMINATES (class-portable vs 2D curiosity) rather
than merely confirming.

THE NEW RISK, and the reason for K3.  phi is CONTINUOUS.  Every reading needs a
binarization, and binarizing purely pairwise continuum dependence mints binary order-3
share.  The 2D siblings had no such channel.  Two thresholdings with declared roles:

  theta=0  -- the Z2-covariant order parameter sign(phi), apples-to-apples with 2D.
              Has a computable Gaussian artifact baseline (K3), quoted with every number.
  median   -- artifact-immune BY THEOREM.  Core/SignSymmetry.lean: a distribution
              symmetric under reflection about its median vector binarizes at the median
              to a sign-symmetric 8-cell state, share EXACTLY zero.  Every multivariate
              Gaussian is such a distribution at any mean, so the median route reads
              exactly zero on any Gaussian, at any h.

Usage:
    python3 phi4_ridge.py --gate
    python3 phi4_ridge.py --bracket | --binder | --hscan | --ridge | --offcrit
    python3 phi4_ridge.py --sep | --bsweep | --controls | --dose
"""
import sys, os, json, time, math, argparse
import numpy as np
from scipy import optimize, integrate, special

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ising_field import (SIGMA, LN2, H8, share3, maxent_t, share_mpmath,
                         all_measures, tau_int, analyse_block_counts)

# --- 3D Ising universality class (Kos-Poland-Simmons-Duffin-Vichi bootstrap) ----------
ETA = 0.0362978
NU = 0.629971
D = 3
BETA_NU = (D - 2.0 + ETA) / 2.0          # 0.5181489   Delta_sigma
Y_H = (D + 2.0 - ETA) / 2.0              # 2.4818511
assert abs(BETA_NU + Y_H - D) < 1e-12
U4_STAR = 0.4655                          # 3D Ising Binder cumulant, periodic cubic

_TINY = 1e-300

# =====================================================================================
# INSTRUMENT, general b:  IPF primal + Lagrangian dual, a two-sided certificate.
# At b = 2 this is validated against the exact one-dimensional solver in the gate.
# =====================================================================================

def share_b(P, iters=8000, tol=1e-14):
    """I_C^(3) for a (b,b,b) joint.  Returns (share, bracket_width, marg_violation).

    IPF finds the maximum-entropy state carrying all three pair marginals.  The dual
    D(theta) = log Z(theta) - <theta>_P is an UPPER bound on H(Q*) for every theta, so
    evaluating it at IPF's converged potentials brackets the answer from the other side.
    The bracket width is reported; a wide bracket is `ungauged`, not a number.
    """
    P = np.asarray(P, dtype=np.float64)
    P = P / P.sum()
    b = P.shape[0]
    P12, P13, P23 = P.sum(2), P.sum(1), P.sum(0)
    f12 = np.zeros((b, b)); f13 = np.zeros((b, b)); f23 = np.zeros((b, b))
    lg = lambda x: np.log(np.maximum(x, _TINY))
    prev = None
    for it in range(iters):
        Q = np.exp(f12[:, :, None] + f13[:, None, :] + f23[None, :, :])
        Q /= Q.sum()
        f12 += lg(P12) - lg(Q.sum(2))
        Q = np.exp(f12[:, :, None] + f13[:, None, :] + f23[None, :, :]); Q /= Q.sum()
        f13 += lg(P13) - lg(Q.sum(1))
        Q = np.exp(f12[:, :, None] + f13[:, None, :] + f23[None, :, :]); Q /= Q.sum()
        f23 += lg(P23) - lg(Q.sum(0))
        if it % 25 == 0:
            Q = np.exp(f12[:, :, None] + f13[:, None, :] + f23[None, :, :]); Q /= Q.sum()
            h = -(Q * lg(Q)).sum()
            if prev is not None and abs(h - prev) < tol:
                break
            prev = h
    Qu = np.exp(f12[:, :, None] + f13[:, None, :] + f23[None, :, :])
    Z = Qu.sum()
    Q = Qu / Z
    Hq = -(Q * lg(Q)).sum()
    Hp = -(P * lg(P)).sum()
    dual = math.log(Z) - (P12 * f12).sum() - (P13 * f13).sum() - (P23 * f23).sum()
    viol = max(np.abs(Q.sum(2) - P12).max(), np.abs(Q.sum(1) - P13).max(),
               np.abs(Q.sum(0) - P23).max())
    return Hq - Hp, float(dual - Hq), float(viol)


# =====================================================================================
# THE MATCHED PAIRWISE-CONTINUUM NULL (K3) — exact, not resampled.
#
# A Gaussian copula binarized at fixed thresholds gives an 8-cell state whose cells are
# trivariate-normal orthant probabilities.  Choosing the three copula correlations to
# reproduce the measured PAIR marginals exactly makes it the pair-matched null with no
# three-body structure by construction.  Its share is the binarization artifact baseline.
#
# Consistency built in: at the median (a = 0) the state is sign-symmetric and its share
# is exactly zero -- Core/SignSymmetry.lean, reproduced numerically in the gate.
# =====================================================================================

def _bvn_upper(h, k, r):
    """P(Z1 > h, Z2 > k) for standard bivariate normal with correlation r.
    Phi2(h,k;r) = Phi(h)Phi(k) + int_0^r phi2(h,k;s) ds, Gauss-Legendre, ~1e-14."""
    ndtr = special.ndtr
    if abs(r) < 1e-15:
        return (1 - ndtr(h)) * (1 - ndtr(k))
    x, w = np.polynomial.legendre.leggauss(64)
    s = 0.5 * r * (x + 1.0)
    jac = 0.5 * r
    dens = np.exp(-(h * h - 2 * s * h * k + k * k) / (2 * (1 - s * s))) / \
           (2 * np.pi * np.sqrt(1 - s * s))
    lower = ndtr(h) * ndtr(k) + jac * (w * dens).sum()     # P(Z1<=h, Z2<=k)
    return 1.0 - ndtr(h) - ndtr(k) + lower


def _tvn_upper(a1, a2, a3, r12, r13, r23):
    """P(Z1>a1, Z2>a2, Z3>a3), by conditioning on Z3 and integrating the bivariate."""
    s13 = math.sqrt(max(1 - r13 * r13, 1e-15))
    s23 = math.sqrt(max(1 - r23 * r23, 1e-15))
    rp = (r12 - r13 * r23) / (s13 * s23)
    rp = float(np.clip(rp, -0.999999, 0.999999))

    def f(z):
        return (math.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)) * \
               _bvn_upper((a1 - r13 * z) / s13, (a2 - r23 * z) / s23, rp)

    val, _ = integrate.quad(f, a3, a3 + 12.0, epsabs=1e-13, epsrel=1e-13, limit=200)
    return val


def gauss_copula_cells(a, r12, r13, r23):
    """The 8 cells of a Gaussian copula binarized at thresholds a=(a1,a2,a3).
    Cell index = 4*b1 + 2*b2 + b3 with b_i = 1 when phi_i is BELOW threshold, matching
    ising_field's convention (s_i = 1-2b_i, so b=0 <-> s=+1 <-> above threshold)."""
    out = np.zeros(8)
    for idx in range(8):
        b = [(idx >> 2) & 1, (idx >> 1) & 1, idx & 1]
        e = [1.0 if bb == 0 else -1.0 for bb in b]      # e=+1 means "above"
        out[idx] = _tvn_upper(e[0] * a[0], e[1] * a[1], e[2] * a[2],
                              e[0] * e[1] * r12, e[0] * e[2] * r13, e[1] * e[2] * r23)
    return out


def fit_copula(p8):
    """Solve for the Gaussian-copula state carrying p8's singles and pair marginals."""
    p = np.asarray(p8, dtype=np.float64); p = p / p.sum()
    r = p.reshape(2, 2, 2)
    # P(above) per site == P(b_i = 0)
    pa = [r[0].sum(), r[:, 0].sum(), r[:, :, 0].sum()]
    a = [float(special.ndtri(1.0 - max(min(x, 1 - 1e-12), 1e-12))) for x in pa]
    # pair probability of BOTH above
    pab = [float(r[0, 0].sum()), float(r[0, :, 0].sum()), float(r[:, 0, 0].sum())]
    rho = []
    for (i, j), tgt in zip([(0, 1), (0, 2), (1, 2)], pab):
        lo = _bvn_upper(a[i], a[j], -0.999)
        hi = _bvn_upper(a[i], a[j], 0.999)
        t = min(max(tgt, lo + 1e-15), hi - 1e-15)
        rho.append(float(optimize.brentq(
            lambda rr: _bvn_upper(a[i], a[j], rr) - t, -0.999, 0.999, xtol=1e-13)))
    cells = gauss_copula_cells(a, rho[0], rho[1], rho[2])
    return cells / cells.sum(), dict(a=a, rho=rho)


def mixture_null(p8):
    """K4: two-component Gaussian mixture, each component pairwise-only, opposite mean
    shifts (the two-phase latent collective mode).  5 parameters (w, mu, 3 correlations)
    against 7 free cells.  Returns (fitted cells, params, rms residual)."""
    p = np.asarray(p8, dtype=np.float64); p = p / p.sum()
    r = p.reshape(2, 2, 2)
    pa = [r[0].sum(), r[:, 0].sum(), r[:, :, 0].sum()]
    a0 = [float(special.ndtri(1.0 - max(min(x, 1 - 1e-12), 1e-12))) for x in pa]

    def model(th):
        w = 1.0 / (1.0 + math.exp(-th[0]))
        mu = abs(th[1])
        rr = [math.tanh(t) for t in th[2:5]]
        cp = gauss_copula_cells([x - mu for x in a0], *rr)
        cm = gauss_copula_cells([x + mu for x in a0], *rr)
        m = w * cp + (1 - w) * cm
        return m / m.sum()

    def resid(th):
        return (model(th) - p) / np.sqrt(np.maximum(p, 1e-9))

    best = None
    for w0 in (-0.5, 0.0, 0.5):
        for mu0 in (0.1, 0.5, 1.0):
            th0 = np.array([w0, mu0, 0.3, 0.3, 0.3])
            try:
                s = optimize.least_squares(resid, th0, xtol=1e-13, ftol=1e-13, max_nfev=3000)
            except Exception:
                continue
            if best is None or s.cost < best.cost:
                best = s
    m = model(best.x)
    return m, dict(w=float(1 / (1 + math.exp(-best.x[0]))), mu=float(abs(best.x[1])),
                   rho=[float(math.tanh(t)) for t in best.x[2:5]]), \
        float(np.sqrt(np.mean((m - p) ** 2)))


# =====================================================================================
# THE SAMPLER — checkerboard Metropolis, GPU, R replicas in parallel.
#
# Cluster updates are declared unavailable and are used NOWHERE: the Brower-Tamayo
# embedded-Ising update needs the global Z2 that h breaks.  One algorithm carries the
# whole map, so no comparison is confounded by an algorithm change.  The price is
# critical slowing down, paid for by measuring tau_int, thinning by it, and reporting
# N_eff rather than nominal N.
# =====================================================================================

KERNEL = r'''
extern "C" __global__
void mh_sweep(float* __restrict__ phi, unsigned long long* __restrict__ st,
              const int L, const int R, const int parity,
              const float c2, const float lam, const float hf, const float delta)
{
    const int L2 = L * L;
    const int L3 = L2 * L;
    const int half = L3 >> 1;
    long long tid = blockIdx.x * (long long)blockDim.x + threadIdx.x;
    if (tid >= (long long)R * half) return;
    const int r = (int)(tid / half);
    int s = (int)(tid % half);
    const int z = s / (L2 >> 1);
    int rem = s - z * (L2 >> 1);
    const int y = rem / (L >> 1);
    const int j = rem - y * (L >> 1);
    const int x = 2 * j + ((parity + y + z) & 1);

    const long long base = (long long)r * L3;
    const int n = x + L * y + L2 * z;
    const int xp = (x + 1 == L) ? 0 : x + 1;
    const int xm = (x == 0) ? L - 1 : x - 1;
    const int yp = (y + 1 == L) ? 0 : y + 1;
    const int ym = (y == 0) ? L - 1 : y - 1;
    const int zp = (z + 1 == L) ? 0 : z + 1;
    const int zm = (z == 0) ? L - 1 : z - 1;

    const float A =
        phi[base + xp + L * y + L2 * z] + phi[base + xm + L * y + L2 * z] +
        phi[base + x + L * yp + L2 * z] + phi[base + x + L * ym + L2 * z] +
        phi[base + x + L * y + L2 * zp] + phi[base + x + L * y + L2 * zm];

    unsigned long long s0 = st[base + n];
    s0 ^= s0 << 13; s0 ^= s0 >> 7; s0 ^= s0 << 17;
    float u1 = (float)((s0 >> 11) * (1.0 / 9007199254740992.0));
    s0 ^= s0 << 13; s0 ^= s0 >> 7; s0 ^= s0 << 17;
    float u2 = (float)((s0 >> 11) * (1.0 / 9007199254740992.0));
    st[base + n] = s0;

    const float f = phi[base + n];
    const float g = f + delta * (2.0f * u1 - 1.0f);
    const float f2 = f * f, g2 = g * g;
    const float dE = c2 * (g2 - f2) + lam * (g2 * g2 - f2 * f2) - (A + hf) * (g - f);
    if (dE <= 0.0f || u2 < expf(-dE)) phi[base + n] = g;
}
'''


class Phi4:
    def __init__(self, L, R, m2, lam, h, seed=0, xp=None):
        import cupy as cp
        self.cp = cp
        assert L % 2 == 0, "kernel assumes even L"
        self.L, self.R, self.m2, self.lam, self.h = L, R, m2, lam, h
        self.L3 = L ** 3
        self.c2 = 3.0 + 0.5 * m2
        rs = cp.random.RandomState(seed)
        self.phi = (0.3 * rs.standard_normal((R, self.L3), dtype=cp.float32)).astype(cp.float32)
        self.st = rs.randint(1, 2 ** 62, size=(R, self.L3), dtype=cp.uint64)
        self.mod = cp.RawModule(code=KERNEL)
        self.k = self.mod.get_function('mh_sweep')
        self.blk = 256
        self.nth = R * (self.L3 // 2)
        self.grd = (self.nth + self.blk - 1) // self.blk
        self.delta = 1.5
        self.rs = rs

    def _half(self, parity):
        cp = self.cp
        self.k((self.grd,), (self.blk,),
               (self.phi, self.st, cp.int32(self.L), cp.int32(self.R), cp.int32(parity),
                cp.float32(self.c2), cp.float32(self.lam), cp.float32(self.h),
                cp.float32(self.delta)))

    def sweep(self, n=1):
        for _ in range(n):
            self._half(0); self._half(1)

    def flip_now(self):
        """Global sign flip phi -> -phi, per replica, with probability 1/2.  Exact at
        h = 0 (the action is invariant), so it is a valid MCMC move applied at any point
        in the chain.  Applied ONCE PER MEASUREMENT rather than once per sweep: that
        already makes every measured configuration carry an independent random sign, so
        the measured ensemble is exactly Z2-symmetric, and it costs 1/200 as much -- the
        per-sweep version was 97% of the total runtime at L = 8 (0.35 of 0.36 ms)."""
        if self.h != 0.0 or not getattr(self, 'flip', True):
            return
        cp = self.cp
        s = (self.rs.rand(self.R) < 0.5).astype(cp.float32) * (-2.0) + 1.0
        self.phi *= s[:, None]

    def advance(self, n, chunk=200):
        """Sweep n times, offering the global flip every `chunk` sweeps."""
        done = 0
        while done < n:
            k = min(chunk, n - done)
            self.sweep(k); self.flip_now()
            done += k

    def tune(self, rounds=40, per=100):
        """Adapt delta to ~50% acceptance.  BURN-IN ONLY; frozen thereafter, so the
        measurement segment is a proper time-homogeneous Markov chain.

        Acceptance is measured over exactly ONE sweep, because each site is proposed
        exactly once per sweep.  Measuring it over `per` sweeps -- as the first version
        did -- reads the fraction of sites that changed at least once, which is ~1 at any
        step size, so the tuner saw acceptance ~1 always and inflated delta to 49."""
        cp = self.cp
        self.acc_rate = float('nan')
        for _ in range(rounds):
            self.sweep(max(per - 1, 1))
            old = self.phi.copy()
            self.sweep(1)
            acc = float((self.phi != old).mean())
            self.acc_rate = acc
            del old
            if acc > 0.55:
                self.delta *= 1.12
            elif acc < 0.45:
                self.delta /= 1.12
        return self.delta

    def mag(self):
        return self.cp.asnumpy(self.phi.mean(axis=1, dtype=self.cp.float64))

    def field4d(self):
        return self.phi.reshape(self.R, self.L, self.L, self.L)


# =====================================================================================
# GEOMETRY CLASSES — kept separate, never pooled (prereg section 7)
# =====================================================================================

def geoms_for(L):
    r = max(1, L // 4)
    return {
        'star':    ((1, 0, 0), (0, 1, 0), (-1, 0, 0)),
        'Lcorner': ((0, 0, 0), (1, 0, 0), (0, 1, 0)),
        'colin1':  ((0, 0, 0), (1, 0, 0), (2, 0, 0)),
        'colin-r': ((0, 0, 0), (r, 0, 0), (2 * r, 0, 0)),
        'far':     ((0, 0, 0), (L // 2, 0, 0), (0, L // 2, 0)),
    }


def _shift(a, d, cp):
    if d == (0, 0, 0):
        return a
    return cp.roll(a, shift=(-d[2], -d[1], -d[0]), axis=(1, 2, 3))


class Accum:
    """Per-replica accumulators: 8-cell counts per (threshold-set, geometry), continuum
    moments per geometry, and the global field moments."""

    def __init__(self, R, gnames, tnames):
        self.R = R
        self.counts = {t: {g: np.zeros((R, 8), np.int64) for g in gnames} for t in tnames}
        self.mom = {g: np.zeros((R, 5), np.float64) for g in gnames}   # a, ab, ac, bc, abc
        self.n = 0
        self.phi1 = np.zeros(R); self.phi2 = np.zeros(R)
        self.m2 = np.zeros(R); self.m4 = np.zeros(R)
        self.nm = 0

    def add_config(self, sim, geoms, thr, cp, do_counts=True):
        L, R = sim.L, sim.R
        f = sim.field4d()
        self.phi1 += cp.asnumpy(f.sum(axis=(1, 2, 3), dtype=cp.float64))
        self.phi2 += cp.asnumpy((f.astype(cp.float64) ** 2).sum(axis=(1, 2, 3)))
        M = cp.asnumpy(f.mean(axis=(1, 2, 3), dtype=cp.float64))
        self.m2 += M ** 2; self.m4 += M ** 4
        self.nm += 1
        levs = {}
        if do_counts:
            for tname, edges in thr.items():
                if len(edges) == 1:
                    levs[tname] = (f > edges[0]).astype(cp.uint8)
                else:
                    lv = cp.zeros(f.shape, cp.uint8)
                    for e in edges:
                        lv += (f > e).astype(cp.uint8)
                    levs[tname] = lv
        for g, dd in geoms.items():
            a = _shift(f, dd[0], cp); b = _shift(f, dd[1], cp); c = _shift(f, dd[2], cp)
            ab = a * b; ac = a * c; bc = b * c; abc = ab * c
            self.mom[g][:, 0] += cp.asnumpy(a.sum(axis=(1, 2, 3), dtype=cp.float64))
            self.mom[g][:, 1] += cp.asnumpy(ab.sum(axis=(1, 2, 3), dtype=cp.float64))
            self.mom[g][:, 2] += cp.asnumpy(ac.sum(axis=(1, 2, 3), dtype=cp.float64))
            self.mom[g][:, 3] += cp.asnumpy(bc.sum(axis=(1, 2, 3), dtype=cp.float64))
            self.mom[g][:, 4] += cp.asnumpy(abc.sum(axis=(1, 2, 3), dtype=cp.float64))
            del ab, ac, bc, abc
            for tname, lv in levs.items():
                nb = int(lv.max()) + 1 if lv.size else 2
                la = _shift(lv, dd[0], cp); lb = _shift(lv, dd[1], cp); lc = _shift(lv, dd[2], cp)
                nlev = 2 if tname.startswith('b2') or tname == 'theta0' else \
                    (3 if tname == 'b3' else 4)
                v = (la.astype(cp.int32) * nlev + lb.astype(cp.int32)) * nlev + lc.astype(cp.int32)
                off = (cp.arange(R, dtype=cp.int32) * (nlev ** 3))[:, None, None, None]
                cnt = cp.bincount((v + off).ravel(), minlength=R * nlev ** 3)
                key = self.counts[tname][g]
                if key.shape[1] != nlev ** 3:
                    self.counts[tname][g] = np.zeros((R, nlev ** 3), np.int64)
                self.counts[tname][g] += cp.asnumpy(cnt).reshape(R, nlev ** 3)
                del la, lb, lc, v, off, cnt
            del a, b, c
        self.n += 1


# =====================================================================================
# ONE GRID POINT
# =====================================================================================

def run_point(L, R, m2, lam, h, seed, n_burn=20000, n_samp=200, gap=None,
              tune_rounds=40, do_counts=True, geom_override=None, thr_extra=False,
              verbose=False, burn_mult=1.0, gap_mult=1.0, flip=True):
    import cupy as cp
    t0 = time.time()
    sim = Phi4(L, R, m2, lam, h, seed=seed)
    sim.flip = flip
    sim.tune(rounds=tune_rounds)
    nb = int(n_burn * burn_mult)
    sim.advance(max(nb - tune_rounds * 100, 1000))

    # tau_int, measured over the tail of burn-in, with NO flips inside the series so it
    # reads physical relaxation.  At h = 0 the slow mode is |M|: sign(M) is randomised by
    # the (exact) global flip, so tau_int(M) there measures the flip and not the physics.
    # At h != 0 there is no flip and M is the right series.  Both are recorded; the gap
    # is set by |M| at h = 0 and by M otherwise.
    def tau_of(n_series):
        s = []
        for _ in range(n_series):
            sim.sweep(1)
            s.append(sim.mag())
        s = np.asarray(s)[:, :min(R, 64)]
        return float(tau_int(s)), float(tau_int(np.abs(s)))

    t_m, t_a = tau_of(4000)
    tau = t_a if h == 0.0 else t_m
    if tau > 150:                                # too slow to be read in 4000 sweeps
        t_m2, t_a2 = tau_of(12000)
        t_m, t_a = max(t_m, t_m2), max(t_a, t_a2)
        tau = t_a if h == 0.0 else t_m
    sim.flip_now()
    if gap is None:
        # AMENDED, disclosed: the prereg said gap >= 2*tau_int.  Measured tau(|M|) is
        # ~400 sweeps near criticality, so 2*tau would spend 8x the compute buying
        # decorrelation that the N_eff apparatus already accounts for -- F is measured
        # ACROSS INDEPENDENT REPLICA CHAINS, so it captures all within-chain correlation,
        # temporal and spatial, and a Monte Carlo mean is unbiased at ANY thinning.  What
        # buys independent information is total sweeps, not gap.  The gap is therefore
        # capped at 200 and the freed compute goes into more configurations.  K5
        # (dose-vs-rate) tests exactly this: gap x 4 must not move the answer.
        gap = int(min(max(20, math.ceil(2.0 * tau)), 200))
    gap = int(max(5, round(gap * gap_mult)))

    geoms = geom_override if geom_override is not None else geoms_for(L)
    # calibration segment: thresholds fixed BEFORE the accumulation segment
    vals = []
    for _ in range(20):
        sim.advance(gap)
        v = cp.asnumpy(sim.phi[:, ::max(1, sim.L3 // 512)].ravel())
        vals.append(v)
    vals = np.concatenate(vals)
    thr = {'theta0': [0.0], 'median': [float(np.quantile(vals, 0.5))]}
    if thr_extra:
        for q in (0.3, 0.4, 0.6, 0.7):
            thr[f'b2q{int(q*10)}'] = [float(np.quantile(vals, q))]
        thr['b3'] = [float(np.quantile(vals, q)) for q in (1 / 3, 2 / 3)]
        thr['b4'] = [float(np.quantile(vals, q)) for q in (0.25, 0.5, 0.75)]

    acc = Accum(R, list(geoms), list(thr))
    for i in range(n_samp):
        sim.advance(gap)
        acc.add_config(sim, geoms, thr, cp, do_counts=do_counts)
    dt = time.time() - t0
    if verbose:
        print(f"      L={L} m2={m2:+.4f} h={h:.6g}  tau(M)={t_m:.1f} tau(|M|)={t_a:.1f} "
              f"gap={gap} delta={sim.delta:.3f} acc={sim.acc_rate:.2f}  {dt:.1f}s")
    npts = acc.n * L ** 3
    out = dict(L=L, R=R, m2=m2, lam=lam, h=h, seed=seed, tau_int=tau, gap=gap,
               tau_M=t_m, tau_absM=t_a, flip=bool(flip), acc_rate=float(sim.acc_rate),
               n_samp=acc.n, delta=float(sim.delta), secs=dt, thr=thr,
               phi1=float(acc.phi1.sum() / (acc.n * R * L ** 3)),
               phi2=float(acc.phi2.sum() / (acc.n * R * L ** 3)),
               M2=float(acc.m2.sum() / (acc.nm * R)), M4=float(acc.m4.sum() / (acc.nm * R)),
               counts={t: {g: acc.counts[t][g].tolist() for g in acc.counts[t]} for t in acc.counts},
               mom={g: (acc.mom[g] / npts).tolist() for g in acc.mom},
               geoms={g: list(map(list, geoms[g])) for g in geoms})
    out['U4'] = 1.0 - out['M4'] / (3.0 * out['M2'] ** 2)
    del sim
    cp.get_default_memory_pool().free_all_blocks()
    return out


# =====================================================================================
# READOUT
# =====================================================================================

def read_counts(counts_RC, rng, want_nulls=True):
    """Full pre-registered readout from per-replica cell counts (R, b^3)."""
    cb = np.asarray(counts_RC, dtype=np.float64)
    nlev = int(round(cb.shape[1] ** (1 / 3)))
    if nlev == 2:
        res = analyse_block_counts(cb, rng)
    else:
        tot = cb.sum(axis=0); p = tot / tot.sum()
        s, brk, viol = share_b(p.reshape(nlev, nlev, nlev))
        R = cb.shape[0]
        nper = cb.sum(axis=1); N = float(nper.sum())
        pb = cb / np.maximum(nper[:, None], 1)
        F = max(float(np.nanmax(pb.var(axis=0, ddof=1) / R /
                np.maximum(p * (1 - p), 1e-300) * N)), 1.0)
        Neff = N / F
        nb2 = 200
        bi = rng.integers(0, R, size=(nb2, R))
        bs = cb[bi].sum(axis=1); bs /= bs.sum(axis=1, keepdims=True)
        bsd = float(np.std([share_b(x.reshape(nlev, nlev, nlev))[0] for x in bs[:40]], ddof=1))
        # estimator floor: pair-maxent multinomial at N_eff
        _, _, _ = share_b(p.reshape(nlev, nlev, nlev))
        fl = []
        for _ in range(30):
            d = rng.multinomial(max(int(Neff), 8), p).astype(float); d /= d.sum()
            fl.append(share_b(d.reshape(nlev, nlev, nlev))[0])
        res = dict(share_raw=float(s), excess=float(s - np.mean(fl)),
                   floor_neff=float(np.mean(fl)), floor_sd=float(np.std(fl, ddof=1)),
                   boot_sd=bsd, N=N, N_eff=float(Neff), F_max=F, R_blocks=R,
                   min_cell=float(p.min()),
                   trustworthy=bool(p.min() * Neff >= 20 and Neff >= 1e3),
                   bracket=float(brk), marg_viol=float(viol), shuffle_floor=float('nan'),
                   cf_excess=float((s - np.mean(fl)) / LN2), tc=float('nan'),
                   omega=float('nan'), ic2=float('nan'), H=float('nan'))
        res['z'] = res['excess'] / max(res['floor_sd'], res['boot_sd'], 1e-300)
    if want_nulls and nlev == 2:
        tot = cb.sum(axis=0); p = tot / tot.sum()
        try:
            gc, gp = fit_copula(p)
            res['copula_share'] = float(share3(gc)[0])
            res['copula_rho'] = gp['rho']
            res['copula_a'] = gp['a']
            # bootstrap the copula baseline through the same replica bootstrap
            R = cb.shape[0]
            bi = rng.integers(0, R, size=(16, R))
            bs = cb[bi].sum(axis=1); bs /= bs.sum(axis=1, keepdims=True)
            cs = []
            for x in bs[:16]:
                try:
                    cs.append(share3(fit_copula(x)[0])[0])
                except Exception:
                    pass
            res['copula_sd'] = float(np.std(cs, ddof=1)) if len(cs) > 3 else float('nan')
        except Exception as e:
            res['copula_share'] = float('nan'); res['copula_err'] = str(e)
    return res


def moments_of(row, g):
    """Connected continuum moments of the triple, and the binary triple moment."""
    m = np.asarray(row['mom'][g], dtype=np.float64)     # (R,5)
    mu = m.mean(axis=0)
    a, ab, ac, bc, abc = mu
    c = [ab - a * a, ac - a * a, bc - a * a]
    U = abc - a * (ab + ac + bc) + 2 * a ** 3
    return dict(phi=float(a), c=[float(x) for x in c], U=float(U),
                var=float(row['phi2'] - row['phi1'] ** 2))


def binary_moments(counts_RC):
    cb = np.asarray(counts_RC, dtype=np.float64)
    p = cb.sum(axis=0); p = p / p.sum()
    s = np.array([1 - 2 * ((i >> k) & 1) for i in range(8) for k in (2, 1, 0)]).reshape(8, 3)
    m = [float((p * s[:, k]).sum()) for k in range(3)]
    c12 = float((p * s[:, 0] * s[:, 1]).sum())
    c13 = float((p * s[:, 0] * s[:, 2]).sum())
    c23 = float((p * s[:, 1] * s[:, 2]).sum())
    tau = float((p * s[:, 0] * s[:, 1] * s[:, 2]).sum())
    _, q, t = share3(p)
    sq = np.asarray(q)
    tau_q = float((sq * s[:, 0] * s[:, 1] * s[:, 2]).sum())
    return dict(m=m, c=[c12, c13, c23], tau=tau, tau_q=tau_q, dtau=tau - tau_q)


def p8_from_moments(m, c12, c13, c23, tau):
    """Rebuild the 8-cell state from its moments -- exact for binary triples."""
    s = np.array([[1 - 2 * ((i >> k) & 1) for k in (2, 1, 0)] for i in range(8)], float)
    return (1.0 + s[:, 0] * m[0] + s[:, 1] * m[1] + s[:, 2] * m[2]
            + s[:, 0] * s[:, 1] * c12 + s[:, 0] * s[:, 2] * c13 + s[:, 1] * s[:, 2] * c23
            + s[:, 0] * s[:, 1] * s[:, 2] * tau) / 8.0


# =====================================================================================
# EXACT FREE-FIELD PROPAGATOR (K2') — a plumb line with a computed, not estimated, answer
# =====================================================================================

def free_propagator(L, m2, disp):
    n = np.arange(L)
    k = 2 * np.pi * n / L
    kh = 2 * (1 - np.cos(k))
    K = kh[:, None, None] + kh[None, :, None] + kh[None, None, :] + m2
    out = []
    for d in disp:
        ph = np.cos(k[:, None, None] * d[0] + k[None, :, None] * d[1] +
                    k[None, None, :] * d[2])
        out.append(float((ph / K).sum() / L ** 3))
    return out


# =====================================================================================
# GATE (K6) — every test must pass before any grid runs
# =====================================================================================

def gate():
    print("=" * 84)
    print("GATE — instrument, nulls, sampler.  Prereg K6 (+ the K1/K2 zeros in miniature).")
    print("=" * 84)
    rng = np.random.default_rng(7)
    ok = True

    def rep(name, val, thresh, fmt="{:.3e}"):
        nonlocal ok
        good = val <= thresh
        ok = ok and good
        print(f"  [{'PASS' if good else 'FAIL'}] {name:<58s} " + fmt.format(val))
        return good

    # G1 parity reads ln 2
    par = np.zeros(8)
    for i in range(8):
        b = [(i >> 2) & 1, (i >> 1) & 1, i & 1]
        if (b[0] ^ b[1]) == b[2]:
            par[i] = 0.25
    rep("G1  parity share = ln 2", abs(float(share3(par)[0]) - LN2), 1e-12)

    # G2 independent state reads zero
    ind = np.full(8, 0.125)
    rep("G2  independent state = 0", abs(float(share3(ind)[0])), 1e-14)

    # G3 the lemma: 2000 random sign-symmetric states
    w = rng.random((2000, 4)); w = w / w.sum(axis=1, keepdims=True) / 2
    ss = np.zeros((2000, 8))
    for i in range(8):
        ss[:, i] = w[:, min(i, 7 - i)]
    ss = ss / ss.sum(axis=1, keepdims=True)
    rep("G3  sign-symmetric family (SignSymmetry.lean)", float(np.abs(share3(ss)[0]).max()), 1e-12)

    # G4 exact solver vs 60-digit mpmath, including near-deterministic corners
    err = 0.0
    for _ in range(30):
        p = rng.random(8) ** rng.integers(1, 9); p = p / p.sum()
        err = max(err, abs(float(share3(p)[0]) - float(share_mpmath(p))))
    rep("G4  float64 solver vs 60-digit mpmath", err, 1e-12)

    # G5 general-b IPF reproduces the exact b=2 solver
    e5 = 0.0
    for _ in range(40):
        p = rng.random(8); p = p / p.sum()
        s2 = float(share3(p)[0])
        sb, brk, viol = share_b(p.reshape(2, 2, 2))
        e5 = max(e5, abs(s2 - sb))
    rep("G5  IPF(b=2) vs exact 1-D solver", e5, 1e-10)

    # G6 THE COPULA NULL IS A NULL: at the median (a=0) it must read exactly zero
    e6 = 0.0
    for _ in range(30):
        rho = rng.uniform(-0.85, 0.85, 3)
        cells = gauss_copula_cells([0.0, 0.0, 0.0], *rho)
        e6 = max(e6, abs(cells.sum() - 1.0), abs(float(share3(cells / cells.sum())[0])))
    rep("G6  Gaussian copula at the median = 0 (the theorem)", e6, 1e-9)

    # G7 the copula fit reproduces the pair marginals it was fitted to
    e7 = 0.0
    for _ in range(20):
        p = rng.random(8) + 0.15; p = p / p.sum()
        gc, _ = fit_copula(p)
        r0 = p.reshape(2, 2, 2); r1 = gc.reshape(2, 2, 2)
        e7 = max(e7, np.abs(r0.sum(2) - r1.sum(2)).max(),
                 np.abs(r0.sum(1) - r1.sum(1)).max(), np.abs(r0.sum(0) - r1.sum(0)).max())
    rep("G7  copula null carries the data's pair marginals", e7, 1e-8)

    # G8 THE DYE TEST: a planted three-body coupling must be SEEN, and seen at the
    # right size (closed form: for p ~ exp(K s1s2s3) every pair marginal is 1/4, so the
    # pairwise maxent IS uniform and I_C^(3) = 3ln2 - H(p) exactly)
    worst = 0.0
    for K in (0.05, 0.2, 0.5, 0.9):
        s = np.array([1 - 2 * (bin(i).count('1') % 2) for i in range(8)], float)
        p = np.exp(K * s); p = p / p.sum()
        closed = 3 * LN2 - float(H8(p))
        worst = max(worst, abs(float(share3(p)[0]) - closed))
    rep("G8  dye test: planted 3-body coupling, vs closed form", worst, 1e-12)

    # G9 dye test on the copula null: planted 3-body structure must NOT be absorbed
    s = np.array([1 - 2 * (bin(i).count('1') % 2) for i in range(8)], float)
    p = np.exp(0.2 * s); p = p / p.sum()
    gc, _ = fit_copula(p)
    seen = float(share3(p)[0]) - float(share3(gc)[0])
    print(f"  [{'PASS' if seen > 0.9 * float(share3(p)[0]) else 'FAIL'}] "
          f"G9  planted 3-body survives the copula null{'':<21s} "
          f"{seen:.3e} of {float(share3(p)[0]):.3e}")
    ok = ok and seen > 0.9 * float(share3(p)[0])

    # G10 histogram construction vs brute force, on a small lattice
    try:
        import cupy as cp
        sim = Phi4(6, 4, -8.0, 1.0, 0.05, seed=3)
        sim.sweep(200)
        g = {'colin1': ((0, 0, 0), (1, 0, 0), (2, 0, 0))}
        acc = Accum(4, ['colin1'], ['theta0'])
        acc.add_config(sim, g, {'theta0': [0.0]}, cp)
        f = cp.asnumpy(sim.field4d())
        bf = np.zeros((4, 8), np.int64)
        for r in range(4):
            for z in range(6):
                for y in range(6):
                    for x in range(6):
                        b0 = int(f[r, z, y, x] > 0)
                        b1 = int(f[r, z, y, (x + 1) % 6] > 0)
                        b2 = int(f[r, z, y, (x + 2) % 6] > 0)
                        bf[r, b0 * 4 + b1 * 2 + b2] += 1
        rep("G10 histogram vs brute-force enumeration",
            float(np.abs(acc.counts['theta0']['colin1'] - bf).max()), 0.5, "{:.0f}")
        del sim
    except Exception as e:
        print(f"  [FAIL] G10 histogram vs brute force: {e}")
        ok = False

    # G11 K2' the sampler plumb line: free field vs the exact lattice propagator.
    #
    # AMENDED, with the arithmetic disclosed rather than the threshold moved.  The first
    # implementation ran 300 samples at gap 3 and read c(2) 0.64% low against a 0.5%
    # relative bar -- but at that sample size c(2)'s OWN statistical error was 0.7%
    # (phi4_g11_diag.py, 6 independent seeds), so the test could not be taken at the
    # precision it asserted.  Raising the statistics 6.7x moves the deviations to
    # +0.013%, +0.021%, +0.047% at |z| <= 1.9.  The amendment is to the SAMPLE SIZE; the
    # 0.5% bar is kept and is now applied where it can be read, and a z-test against the
    # measured across-seed error bar is added so the gate can never again be scored at a
    # precision its own noise does not support.
    try:
        L, m2f, Rf, NSEED = 12, 0.5, 256, 4
        g = {'colin1': ((0, 0, 0), (1, 0, 0), (2, 0, 0))}
        ex = free_propagator(L, m2f, [(0, 0, 0), (1, 0, 0), (2, 0, 0)])
        res = []
        for sd in range(NSEED):
            sim = Phi4(L, Rf, m2f, 0.0, 0.0, seed=1000 + 37 * sd)
            sim.tune(); sim.sweep(8000)
            acc = Accum(Rf, ['colin1'], ['theta0'])
            for _ in range(2000):
                sim.sweep(6)
                acc.add_config(sim, g, {'theta0': [0.0]}, cp, do_counts=False)
            mu = (acc.mom['colin1'] / (acc.n * L ** 3)).mean(axis=0)
            res.append([float(acc.phi2.sum() / (acc.n * Rf * L ** 3)),
                        float(mu[1]), float(mu[2])])
            del sim
            cp.get_default_memory_pool().free_all_blocks()
        res = np.array(res)
        mm, ss = res.mean(axis=0), res.std(axis=0, ddof=1) / math.sqrt(NSEED)
        e11 = 0.0; z11 = 0.0
        for i, nm in enumerate(['<phi^2>', 'c(1)', 'c(2)']):
            e11 = max(e11, abs(mm[i] / ex[i] - 1))
            z11 = max(z11, abs((mm[i] - ex[i]) / ss[i]))
            print(f"        {nm:>8s} {mm[i]:.8f} +- {ss[i]:.8f}  exact {ex[i]:.8f}  "
                  f"rel {(mm[i]/ex[i]-1)*100:+.3f}%  z={(mm[i]-ex[i])/ss[i]:+.2f}")
        rep("G11 K2' sampler vs exact free propagator (rel)", e11, 5e-3)
        rep("G11z K2' same, against its own error bar", z11, 3.0, "{:.2f}")
    except Exception as e:
        print(f"  [FAIL] G11 sampler plumb line: {e}")
        ok = False

    print("=" * 84)
    print(f"GATE {'PASSED' if ok else 'FAILED'}")
    print("=" * 84)
    return ok


def _dump(name, obj):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
    with open(path, 'w') as fh:
        json.dump(obj, fh)
    print(f"    -> {name}  ({os.path.getsize(path)/1e6:.1f} MB)")


def main():
    ap = argparse.ArgumentParser()
    for s in ('gate', 'bracket', 'binder', 'hscan', 'ridge', 'offcrit', 'sep',
              'bsweep', 'controls', 'dose'):
        ap.add_argument('--' + s, action='store_true')
    ap.add_argument('--mc', type=float, default=None, help='m_c^2 from the binder stage')
    ap.add_argument('--u0', type=float, default=None, help='peak u = h L^y_h from hscan')
    ap.add_argument('--tag', type=str, default='')
    a = ap.parse_args()

    if a.gate:
        return 0 if gate() else 1

    LAM = 1.0
    rng = np.random.default_rng(20260726)

    if a.bracket:
        # The declared S1 grid m2 in {-12..-5} came back ordered at EVERY point
        # (U4 = 0.63-0.67 = the two-delta value, <M^2> ~ 1-2), so it did not bracket the
        # transition.  Mean field puts it at m2 = 0 and fluctuations push it below; the
        # grid is re-centred on [-5, 0] with the SAME 8-point cap.  Disclosed as an
        # amendment to the grid, made on a control column (h = 0) before any h was swept.
        rows = []
        for L in (8, 12):
            for m2 in (-5, -4, -3, -2.5, -2, -1.5, -1, -0.5):
                r = run_point(L, 512, float(m2), LAM, 0.0, seed=101 + L,
                              n_burn=8000, n_samp=60, verbose=True, do_counts=False)
                rows.append(r)
                print(f"      L={L} m2={m2:+.1f}  <phi>={r['phi1']:+.4f} "
                      f"<M^2>={r['M2']:.5f}  U4={r['U4']:.4f}")
        _dump('phi4_bracket.json', rows)

    if a.binder:
        # Window narrowed from the declared half-width 0.6 to 0.20, disclosed: S1
        # bracketed the transition in (-2.5, -2.0), and a two-point smoke run at
        # m2 = -2.30 (h = 0, a control column) read U4 = 0.49 (L=16) -> 0.574 (L=32),
        # i.e. still ordered, localising the crossing to (-2.30, -2.00).  Same 9-point
        # cap, finer step.
        centre = a.mc if a.mc is not None else -2.25
        m2s = [centre - 0.05 + 0.10 * i / 8 for i in range(9)]
        rows = []
        for L in (8, 12, 16, 24, 32):
            R = 512 if L <= 16 else 256
            ns = 500 if L <= 16 else 300
            for m2 in m2s:
                r = run_point(L, R, float(m2), LAM, 0.0, seed=211 + L, n_burn=20000,
                              n_samp=ns, verbose=True)
                rows.append(r)
                print(f"      L={L:2d} m2={m2:+.4f}  U4={r['U4']:.5f}  "
                      f"<M^2>={r['M2']:.6f} tau={r['tau_int']:.0f}")
                _dump('phi4_binder.json', rows)

    if a.hscan:
        mc = a.mc
        rows = []
        hs = [0.0] + [10 ** (-4.0 + 4.0 * i / 11) for i in range(12)]
        for h in hs:
            r = run_point(8, 512, mc, LAM, float(h), seed=331, n_burn=20000,
                          n_samp=400, verbose=True)
            rows.append(r)
            _dump('phi4_hscan.json', rows)

    # ---- S3b the ridge: 12 u-values geometric about the S3a peak, plus h = 0 --------
    if a.ridge or a.offcrit:
        mc, u0 = a.mc, a.u0
        us = [0.0] + [u0 * 1.7 ** (i - 5.5) for i in range(12)]
        cols = ([(mc, 'crit')] if a.ridge else
                [(mc - 0.5, 'ord'), (mc + 0.5, 'dis')])
        Ls = (8, 12, 16, 24, 32) if a.ridge else (8, 12, 16)
        rows = []
        for m2, tag in cols:
            for L in Ls:
                R = 512 if L <= 16 else 256
                ns = 400 if L <= 16 else 200
                for u in us:
                    h = u / L ** Y_H
                    r = run_point(L, R, float(m2), LAM, float(h), seed=441 + L,
                                  n_burn=20000, n_samp=ns, verbose=True)
                    r['u'] = u; r['col'] = tag
                    rows.append(r)
                    _dump('phi4_ridge.json' if a.ridge else 'phi4_offcrit.json', rows)

    # ---- S5 separation scan, at the ridge peak only ---------------------------------
    if a.sep:
        mc, u0 = a.mc, a.u0
        rows = []
        for L in (8, 12, 16, 24, 32):
            R = 512 if L <= 16 else 256
            ns = 400 if L <= 16 else 200
            g = {f'r{r_}': ((0, 0, 0), (r_, 0, 0), (2 * r_, 0, 0))
                 for r_ in range(1, L // 2 + 1)}
            r = run_point(L, R, float(mc), LAM, float(u0 / L ** Y_H), seed=551 + L,
                          n_burn=20000, n_samp=ns, geom_override=g, verbose=True)
            rows.append(r)
            _dump('phi4_sep.json', rows)

    # ---- S6 b / threshold sweep, at the ridge peak (K7) -----------------------------
    if a.bsweep:
        mc, u0 = a.mc, a.u0
        rows = []
        for L in (8, 12, 16, 24):
            R = 512 if L <= 16 else 256
            ns = 400 if L <= 16 else 200
            r = run_point(L, R, float(mc), LAM, float(u0 / L ** Y_H), seed=661 + L,
                          n_burn=20000, n_samp=ns, thr_extra=True, verbose=True)
            rows.append(r)
            _dump('phi4_bsweep.json', rows)

    # ---- S7 controls ----------------------------------------------------------------
    if a.controls:
        rows = []
        # K2 / K2': the free field.  Gaussian at any h, so the MEDIAN route must read
        # exactly zero by share_eq_zero_of_signSymmetric, and theta=0 must NOT (that is
        # the binarization artifact, measured on a case where its size is computable).
        for m2f in (0.1, 1.0):
            for h in (0.0, 0.05, 0.2):
                r = run_point(12, 512, float(m2f), 0.0, float(h), seed=771,
                              n_burn=20000, n_samp=400, verbose=True)
                r['col'] = 'free'
                rows.append(r); _dump('phi4_controls.json', rows)
        # K1, the HARD version: h = 0 with the global sign flip switched OFF.  With the
        # flip on, the sampled ensemble is symmetric by construction and K1 tests the
        # estimator floor only; with it off, K1 also tests whether the sampler explores
        # both phases.  Both are reported.
        mc = a.mc
        for L in (8, 12, 16):
            for fl in (True, False):
                r = run_point(L, 512, float(mc), LAM, 0.0, seed=781 + L, n_burn=20000,
                              n_samp=400, flip=fl, verbose=True)
                r['col'] = 'k1flip' if fl else 'k1noflip'
                rows.append(r); _dump('phi4_controls.json', rows)

    # ---- K5 dose-vs-rate: the peak must not move with burn-in or thinning -----------
    if a.dose:
        mc, u0 = a.mc, a.u0
        rows = []
        for L in (8, 16):
            R = 512
            for bm, gm in ((1.0, 1.0), (4.0, 1.0), (1.0, 4.0), (4.0, 4.0)):
                for uu in (u0 / 1.7, u0, u0 * 1.7):
                    r = run_point(L, R, float(mc), LAM, float(uu / L ** Y_H),
                                  seed=881 + L, n_burn=20000, n_samp=400,
                                  burn_mult=bm, gap_mult=gm, verbose=True)
                    r['u'] = uu; r['burn_mult'] = bm; r['gap_mult'] = gm
                    rows.append(r); _dump('phi4_dose.json', rows)

    return 0


if __name__ == '__main__':
    sys.exit(main())
