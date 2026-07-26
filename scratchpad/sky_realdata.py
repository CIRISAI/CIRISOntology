#!/usr/bin/env python3
"""
sky_realdata.py -- STAGE 1 pipeline for SKY_REALDATA_PREREG.md (+ AMENDMENT 1).

BLINDING DISCIPLINE, enforced by construction.  This module builds and validates the
machinery.  It NEVER reads the order-3 statistic of the real galaxy catalogue: the function
that would do so (`measure_catalogue`) refuses unless `stage6_unblind=True` is passed
explicitly, which nothing in Stages 1-5 does.  Stage-1 validation runs on
  (a) the RANDOM catalogue, which carries the geometry and by construction no clustering, and
  (b) synthetic fields imposed on that geometry -- which is simultaneously gate G5.

The pre-registered pipeline, in order:
  sky (RA, DEC, z) -> comoving Cartesian (fiducial Om=0.31, h=0.68, flat)
  -> interlaced CIC deposit of weighted galaxies and randoms onto a 5-smooth grid
  -> local-mean density  delta = (n_g - alpha n_r) / (alpha n_r)   on cells where n_r passes
  -> MASKED smoothing at R:  W*(delta*M) / (W*M)      [a filter, applied identically to
     data and mocks, and NEVER deconvolved -- prereg G4]
  -> quantile binning into b levels over VALID cells only
  -> triple histogram at declared configurations, all three cells valid
  -> I_C^(3)(b) by IPF with the KL certificate      [prereg G9]
  -> LP pair-pinning interval on the linear sign-triple functional  [prereg G1]

Amendment 1: primary scale R = 15 Mpc/h (secondary R = 10); b in {4,6,8}; occupancy > 100.
"""
import os
import sys

import numpy as np
from scipy import fft as sfft
from scipy.integrate import quad
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_pilot import pairwise_maxent, share3_ref, route_B2       # noqa: E402

F32 = np.float32
DATA = os.environ.get('SKYDATA', '/home/emoore/skydata')
OM, HUB = 0.31, 0.68
CLIGHT = 299792.458


def log(*a):
    print(*a, flush=True)


# ---------------------------------------------------------------- cosmology
_zg = np.linspace(0.0, 1.4, 281)
_E = lambda z: np.sqrt(OM * (1 + z) ** 3 + (1 - OM))
_cg = np.array([(CLIGHT / 100.0) * quad(lambda x: 1.0 / _E(x), 0, z)[0] for z in _zg])


def chi(z):
    """Comoving distance, Mpc/h, fiducial flat cosmology (pre-registered)."""
    return np.interp(z, _zg, _cg)


def growth(z):
    f = lambda a: (a * _E(1 / a - 1)) ** -3
    return (_E(z) * quad(f, 1e-8, 1 / (1 + z))[0]) / (_E(0) * quad(f, 1e-8, 1.0)[0])


def sky_to_cart(ra_deg, dec_deg, z):
    r = chi(z)
    ra, dec = np.deg2rad(ra_deg), np.deg2rad(dec_deg)
    cd = np.cos(dec)
    return np.stack([r * cd * np.cos(ra), r * cd * np.sin(ra), r * np.sin(dec)], axis=1)


def smooth5(n):
    """Smallest 5-smooth integer >= n.  Power-of-two padding would cost 4.5x here."""
    best = None
    p = 1
    while p < 2 * n + 2:
        q = p
        while q < 2 * n + 2:
            r = q
            while r < 2 * n + 2:
                if r >= n and (best is None or r < best):
                    best = r
                r *= 5
            q *= 3
        p *= 2
    return int(best)


# ---------------------------------------------------------------- grid
class SurveyGrid:
    """Rectangular, non-cubic, 5-smooth grid enclosing a survey footprint."""

    def __init__(self, pos, cell=6.0, pad=60.0):
        lo = pos.min(axis=0) - pad
        hi = pos.max(axis=0) + pad
        self.cell = float(cell)
        self.lo = lo
        n = np.ceil((hi - lo) / cell).astype(int)
        self.N = tuple(smooth5(int(v)) for v in n)
        self.shape = self.N
        kx = [np.fft.fftfreq(self.N[i], d=cell) * 2 * np.pi for i in range(2)]
        kz = np.fft.rfftfreq(self.N[2], d=cell) * 2 * np.pi
        self.k2 = (kx[0][:, None, None] ** 2 + kx[1][None, :, None] ** 2
                   + kz[None, None, :] ** 2).astype(np.float32)
        self.ncell = int(np.prod(self.N))

    def fwd(self, f):
        return sfft.rfftn(f, workers=-1)

    def inv(self, F):
        return sfft.irfftn(F, s=self.N, workers=-1)

    def smooth_k(self, F, R):
        return self.inv(F * np.exp(-0.5 * self.k2 * R * R).astype(np.float32)).astype(F32)

    # --- interlaced CIC, validated in the mock campaign (Sefusatti et al. 2016) ---
    def _cic(self, pos, wt, shift):
        N = self.N
        out = np.zeros(self.ncell, dtype=np.float64)
        p = (pos - self.lo) / self.cell + shift
        i0 = np.floor(p).astype(np.int64)
        d = p - i0
        for a in range(2):
            ii = np.clip(i0[:, 0] + a, 0, N[0] - 1)
            wa = (d[:, 0] if a else 1 - d[:, 0])
            for b in range(2):
                jj = np.clip(i0[:, 1] + b, 0, N[1] - 1)
                wb = wa * (d[:, 1] if b else 1 - d[:, 1])
                base = (ii * N[1] + jj) * N[2]
                for c in range(2):
                    kk = np.clip(i0[:, 2] + c, 0, N[2] - 1)
                    wc = wb * (d[:, 2] if c else 1 - d[:, 2])
                    out += np.bincount(base + kk, weights=wc * wt, minlength=self.ncell)
        return out.reshape(N)

    def deposit(self, pos, wt, interlace=True):
        g = self._cic(pos, wt, 0.0).astype(F32)
        if not interlace:
            return g
        h = self._cic(pos, wt, 0.5).astype(F32)
        ph = np.exp(0.5j * self.cell * (
            (np.fft.fftfreq(self.N[0], d=self.cell) * 2 * np.pi)[:, None, None]
            + (np.fft.fftfreq(self.N[1], d=self.cell) * 2 * np.pi)[None, :, None]
            + (np.fft.rfftfreq(self.N[2], d=self.cell) * 2 * np.pi)[None, None, :]
        )).astype(np.complex64)
        out = self.inv(0.5 * (self.fwd(g) + ph * self.fwd(h))).astype(F32)
        del g, h, ph
        return out


# ---------------------------------------------------------------- field
def density_and_mask(g, n_gal, n_ran, frac=0.80):
    """delta = (n_g - alpha n_r)/(alpha n_r) where the randoms are dense enough.

    Dividing by the local random density removes the SELECTION function (n-bar(z) and angular
    completeness).  That is not the forbidden operation: prereg G4 forbids deconvolving the
    WINDOW's effect on the statistic, which this does not attempt and which is instead
    forward-modelled by running mocks through this identical path."""
    tot_g, tot_r = float(n_gal.sum()), float(n_ran.sum())
    alpha = tot_g / tot_r
    exp = alpha * n_ran
    thr = frac * np.median(exp[exp > 0])
    mask = (exp > thr)
    delta = np.zeros_like(n_gal)
    np.divide(n_gal - exp, exp, out=delta, where=mask)
    return delta.astype(F32), mask, alpha, thr


def masked_smooth(g, delta, mask, R, den_thr=0.99):
    """W*(delta*M)/(W*M): a local renormalisation so the survey edge does not drag the field
    toward zero.  Still a filter, hence still a manufacturing channel -- which is exactly why
    it is applied bit-identically to data, mocks and controls."""
    m = mask.astype(F32)
    num = g.smooth_k(g.fwd((delta * m).astype(F32)), R)
    den = g.smooth_k(g.fwd(m), R)
    # STAGE 1 FINDING: den_thr = 0.5 inflates a pure shot-noise null by 6.6x, because cells
    # whose kernel straddles the survey edge divide by a small denominator.  At 0.99 (>=99% of
    # the kernel weight on valid cells) the null returns to 1.45x the analytic shot-noise
    # prediction, the residual being the 10x variation of n-bar(z) across the sample.  It costs
    # 2.6x in valid cells, which is the right trade when statistics are not the limit.
    ok = den > den_thr
    out = np.zeros_like(num)
    np.divide(num, den, out=out, where=ok)
    return out, ok


# ---------------------------------------------------------------- estimator
def quantile_labels(field, valid, b, sub=1 << 22, seed=11):
    v = field[valid]
    rng = np.random.default_rng(seed)
    s = v[rng.integers(0, v.size, size=min(sub, v.size))]
    edges = np.quantile(s.astype(np.float64), np.arange(1, b) / b)
    lab = np.searchsorted(edges, field, side='right').astype(np.uint8)
    return lab, edges


def triple_hist(lab, valid, d1, d2, b, stride):
    """Histogram over base cells whose three members are ALL inside the footprint."""
    N = lab.shape
    sl = tuple(slice(0, N[i], stride) for i in range(3))
    def roll(a, d):
        return np.roll(a, (-d[0], -d[1], -d[2]), axis=(0, 1, 2))[sl]
    a0, a1, a2 = lab[sl], roll(lab, d1), roll(lab, d2)
    m = valid[sl] & roll(valid, d1) & roll(valid, d2)
    idx = ((a0.astype(np.int64) * b + a1) * b + a2)[m]
    h = np.bincount(idx, minlength=b ** 3).astype(np.float64)
    return h.reshape(b, b, b), int(m.sum())


def connected_info(p, iters=20000, tol=1e-13):
    """Order-3 connected information with the pilot's KL certificate (prereg G9)."""
    p = np.asarray(p, float)
    p = p / p.sum()
    q, err, _ = pairwise_maxent(p, iters=iters, tol=tol)
    m = p > 0
    sH = float(-(q[q > 0] * np.log(q[q > 0])).sum() + (p[m] * np.log(p[m])).sum())
    sKL = float((p[m] * (np.log(p[m]) - np.log(np.maximum(q[m], 1e-300)))).sum())
    return dict(I=sKL, cert=abs(sH - sKL), ipf_err=float(err))


# ---------------------------------------------------------------- G1: LP pair-pinning
def lp_pinning_interval(p_fine, b):
    """GATE G1 (kappa-edge 3026a68).  Over EVERY distribution carrying the measured b-level
    pair marginals, what range can the coarse SIGN-TRIPLE moment take?

    The LP is valid because tau is LINEAR in the distribution; a KL-based connected
    information is not, which is why the gate runs on this functional and not on I_C^(3).
    Returns (tau_min, tau_max, width).  A width small compared to the statistical error means
    the reading is FORCED by pair structure and the arm is VOID."""
    p = np.asarray(p_fine, float)
    p = p / p.sum()
    n = b ** 3
    h = b // 2
    # objective: the coarse sign-triple moment, sigma = prod of (upper half ? +1 : -1)
    s = np.array([1.0 if (i // (b * b) >= h) else -1.0 for i in range(n)])
    s *= np.array([1.0 if ((i // b) % b >= h) else -1.0 for i in range(n)])
    s *= np.array([1.0 if (i % b >= h) else -1.0 for i in range(n)])
    # constraints: the three b x b pair marginals, plus normalisation
    rows, rhs = [], []
    P = p.reshape(b, b, b)
    for ax, (u, v) in enumerate([(0, 1), (0, 2), (1, 2)]):
        tgt = P.sum(axis=[2, 1, 0][ax])
        for i in range(b):
            for j in range(b):
                r = np.zeros(n)
                idx = np.arange(n)
                a0, a1, a2 = idx // (b * b), (idx // b) % b, idx % b
                sel = ((a0 == i) & (a1 == j)) if ax == 0 else \
                      ((a0 == i) & (a2 == j)) if ax == 1 else ((a1 == i) & (a2 == j))
                r[sel] = 1.0
                rows.append(r); rhs.append(tgt[i, j])
    rows.append(np.ones(n)); rhs.append(1.0)
    A, bq = np.array(rows), np.array(rhs)
    lo = linprog(s, A_eq=A, b_eq=bq, bounds=(0, 1), method='highs')
    hi = linprog(-s, A_eq=A, b_eq=bq, bounds=(0, 1), method='highs')
    if not (lo.success and hi.success):
        return None
    return float(lo.fun), float(-hi.fun), float(-hi.fun - lo.fun)


# ---------------------------------------------------------------- configurations
def configs(R, cell, rmult=1.5):
    """Folded/collinear is PRIMARY (prereg §3.1: that is where gravity's own excess lives)."""
    rc = int(max(1, round(rmult * R / cell)))
    def perm(d, s):
        return tuple(d[(j - s) % 3] for j in range(3))
    base = {
        'folded':      ((rc, 0, 0), (2 * rc, 0, 0)),
        'equilateral': ((rc, 0, 0), (int(round(rc / 2)), int(round(rc * np.sqrt(3) / 2)), 0)),
        'squeezed':    ((max(1, rc // 4), 0, 0), (0, rc, 0)),
    }
    return {k: [(perm(a, s), perm(b, s)) for s in range(3)] for k, (a, b) in base.items()}


# ---------------------------------------------------------------- driver
def measure_field(g, delta, mask, R, bs=(4, 6, 8), rmult=1.5, stride=None,
                  occupancy_min=100.0, run_lp=False, den_thr=0.99):
    """One field -> the pre-registered readings.  Used for mocks, controls and (only at
    Stage 6) the data."""
    sm, ok = masked_smooth(g, delta, mask, R, den_thr=den_thr)
    if stride is None:
        stride = max(1, int(round(R / g.cell / 3)))
    # OCCUPANCY, prereg-correct: INDEPENDENT SMOOTHING VOLUMES, not grid cells and not
    # galaxies.  Stage 1 caught this implemented wrongly (raw triple counts overstate
    # independence by the number of cells per smoothing volume, here ~250x at R=15).
    n_indep = float(ok.sum()) * g.cell ** 3 / ((2 * np.pi) ** 1.5 * R ** 3)
    out = {'R': R, 'stride': stride, 'n_valid': int(ok.sum()), 'n_indep': n_indep,
           'frac_valid': float(ok.mean()), 'sigma': float(sm[ok].std()), 'b': {}}
    for b in bs:
        lab, _ = quantile_labels(sm, ok, b)
        rec = {}
        for name, orients in configs(R, g.cell, rmult).items():
            hs = np.zeros((b, b, b)); ntot = 0
            for (d1, d2) in orients:
                h, nt = triple_hist(lab, ok, d1, d2, b, stride)
                hs += h; ntot += nt
            occ = n_indep / b ** 3
            e = dict(n_triples=ntot, occupancy=occ,
                     occupancy_pass=bool(occ > occupancy_min))
            if occ > occupancy_min:
                ci = connected_info(hs)
                e.update(ci)
                e['E'] = float(route_B2(_coarse2(hs / hs.sum(), b).ravel())[1])
                e['tied'] = 0.0
                if run_lp and b <= 6:
                    lp = lp_pinning_interval(hs / hs.sum(), b)
                    if lp:
                        e['lp_min'], e['lp_max'], e['lp_width'] = lp
            rec[name] = e
        out['b'][b] = rec
        del lab
    del sm, ok
    return out


def _coarse2(p, b):
    h = b // 2
    q = p.reshape(2, h, 2, h, 2, h).sum(axis=(1, 3, 5))
    return q / q.sum()


def measure_catalogue(*a, stage6_unblind=False, **k):
    """BLINDING GUARD.  The real galaxy catalogue's order-3 reading is a STAGE 6 action and
    is produced exactly once, after G1-G10 have passed.  Nothing in Stages 1-5 may call this
    with stage6_unblind=True."""
    if not stage6_unblind:
        raise RuntimeError(
            "BLINDED: reading the real catalogue's order-3 statistic is a Stage 6 action. "
            "Run the gates first; pass stage6_unblind=True only at Stage 6.")
    return measure_field(*a, **k)
