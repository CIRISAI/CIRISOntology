#!/usr/bin/env python3
"""
sky_forecast.py -- could a survey measure gravity's whole-only share?  A FORECAST.

Pre-registered in SKY_FORECAST_PREREG.md, committed at b89ce48 BEFORE this file existed.

Forecast on MY OWN MOCKS.  No real survey data is read anywhere.  Nothing here touches
Lean, Stance.lean or the audit, and `lake` is never run.

Gravity arms
  G0  ZA     -- Zel'dovich particles + CIC
  G1  2LPT   -- second-order Lagrangian PT particles + CIC          (the realistic mock)
  G2  SPT2   -- Eulerian second order, F2 kernel, split into
               LOCAL (17/21 d^2) | SHIFT (grad psi . grad d) | TIDAL (2/7 s_ij s_ij)

Pointwise floors, all built from the SAME white noise, all EXACTLY T(Gaussian) so the
zero-share theorem (Core/SignSymmetry.lean) applies to them before the final filter
  F0  phase-randomised Gaussian at matched P(k)      -- true share exactly 0
  F1  lognormal at matched P(k)                       -- the brief's floor
  F2  rank-matched (matches gravity's one-point law EXACTLY too) -- the PRIMARY floor

Statistic: the b=2 SIGNED SIGN-TRIPLE EXCESS E (route_B2's dtau), with the share in nats
alongside.  E is linear in the histogram, hence forecastable; the share is not.

Usage:  python sky_forecast.py gate | sweep | sectors | poisson | all
"""
import json
import os
import sys
import time

import numpy as np
from scipy import fft as sfft
from scipy import special

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_pilot import share3_ref, route_B2, eh_nowiggle_T, share_b, SIGMA8  # noqa: E402

WORKERS = int(os.environ.get('SKY_WORKERS', '0')) or None   # None -> scipy default (all)
F32 = np.float32


def log(*a):
    print(*a, flush=True)


# =====================================================================================
# COSMOLOGY  (fixed in the pre-registration, section 2)
# =====================================================================================
COSMO = dict(Om=0.31, Ob=0.048, h=0.68, ns=0.96, sigma8=0.81, Tcmb=2.7255)


def _pk_shape(k):
    """Unnormalised linear P(k) = k^ns T(k)^2, k in h/Mpc."""
    k = np.asarray(k, dtype=np.float64)
    T = eh_nowiggle_T(k, Om=COSMO['Om'], Ob=COSMO['Ob'], h=COSMO['h'], Tcmb=COSMO['Tcmb'])
    return np.where(k > 0, k ** COSMO['ns'] * T * T, 0.0)


def _sigma_R_tophat(norm, R=8.0):
    lk = np.linspace(np.log(1e-5), np.log(1e2), 8001)
    k = np.exp(lk)
    x = k * R
    W = 3.0 * (np.sin(x) - x * np.cos(x)) / x ** 3
    integ = k ** 3 * norm * _pk_shape(k) * W * W / (2 * np.pi ** 2)
    return float(np.sqrt(np.trapezoid(integ, lk)))


_A_NORM = COSMO['sigma8'] ** 2 / _sigma_R_tophat(1.0) ** 2


def pk_lin(k):
    """Linear P(k) in (Mpc/h)^3 at D=1, normalised to sigma_8 = 0.81."""
    return _A_NORM * _pk_shape(k)


def sigma_R_gauss(R, D=1.0):
    """rms of the D-scaled LINEAR field Gaussian-smoothed at R (reference number only)."""
    lk = np.linspace(np.log(1e-5), np.log(1e2), 8001)
    k = np.exp(lk)
    integ = k ** 3 * pk_lin(k) * np.exp(-(k * R) ** 2) / (2 * np.pi ** 2)
    return float(D * np.sqrt(np.trapezoid(integ, lk)))


# =====================================================================================
# GRID MACHINERY
# =====================================================================================
class Grid:
    """rfftn-layout k grid, shell binning, and the FFT helpers."""

    def __init__(self, N, L, nbin=48):
        self.N, self.L = N, L
        self.cell = L / N
        self.Vcell = self.cell ** 3
        self.V = L ** 3
        kf = 2 * np.pi / L
        kx = np.fft.fftfreq(N) * N * kf
        kz = np.fft.rfftfreq(N) * N * kf
        self.kx, self.kz = kx.astype(np.float64), kz.astype(np.float64)
        k2 = (kx[:, None, None] ** 2 + kx[None, :, None] ** 2 + kz[None, None, :] ** 2)
        self.kk = np.sqrt(k2).astype(np.float32)
        self.inv_k2 = np.zeros_like(k2, dtype=np.float32)
        np.divide(1.0, k2, out=self.inv_k2, where=k2 > 0)
        self.knyq = np.pi / self.cell
        # rfft double-count weights
        w = np.full(len(kz), 2.0)
        w[0] = 1.0
        if N % 2 == 0:
            w[-1] = 1.0
        self.wmode = np.broadcast_to(w[None, None, :], self.kk.shape).astype(np.float32)
        # log shell bins
        edges = np.concatenate([[0.0], np.exp(np.linspace(np.log(kf * 0.999),
                                                          np.log(self.knyq * 1.001), nbin))])
        self.kedges = edges
        self.kbin = (np.digitize(self.kk.ravel(), edges) - 1).astype(np.int32)
        self.kbin[self.kbin < 0] = 0
        self.nbin = len(edges) - 1
        self.kbin = np.clip(self.kbin, 0, self.nbin - 1)
        self.modes = np.bincount(self.kbin, weights=self.wmode.ravel().astype(np.float64),
                                 minlength=self.nbin)
        self.kcen = np.bincount(self.kbin,
                                weights=(self.wmode.ravel() * self.kk.ravel()).astype(np.float64),
                                minlength=self.nbin) / np.maximum(self.modes, 1e-30)
        self.kbin = self.kbin.reshape(self.kk.shape)
        # zero mode excluded from every spectrum
        self.mask0 = (self.kk > 0)
        # NYQUIST GUARD.  For a real field the +N/2 and -N/2 modes are the same mode, so a
        # spectral first derivative there is genuinely ambiguous in sign -- rfftn's last
        # axis calls it +N/2, fftn's fold calls it -N/2.  Every field this run differentiates
        # is generated with the Nyquist planes empty, which removes the ambiguity from both
        # routes at once.  (Without this, the F2 kernel check GF1 fails at 23 %.)
        nq = np.ones(self.kk.shape, dtype=np.float32)
        if N % 2 == 0:
            nq[N // 2, :, :] = 0.0
            nq[:, N // 2, :] = 0.0
            nq[:, :, -1] = 0.0
        self.nyq = nq

    # --- FFT ---
    def fwd(self, f):
        return sfft.rfftn(f, workers=WORKERS)

    def inv(self, F):
        return sfft.irfftn(F, s=(self.N,) * 3, workers=WORKERS)

    # --- spectra ---
    def measure_P(self, f):
        F = self.fwd(f)
        pw = (F.real.astype(np.float64) ** 2 + F.imag.astype(np.float64) ** 2)
        pw *= self.Vcell / self.N ** 3
        w = self.wmode.astype(np.float64) * self.mask0
        num = np.bincount(self.kbin.ravel(), weights=(pw * w).ravel(), minlength=self.nbin)
        den = np.bincount(self.kbin.ravel(), weights=w.ravel(), minlength=self.nbin)
        return num / np.maximum(den, 1e-30)

    def gauss_from_white(self, wk, Pfun3d):
        """wk = rfftn(white noise).  Returns a real field with the given P(k)."""
        amp = np.sqrt(np.maximum(Pfun3d, 0.0) / self.Vcell).astype(np.float32) * self.nyq
        amp[0, 0, 0] = 0.0
        return self.inv(wk * amp).astype(F32)

    def P_on_grid(self, Pbins):
        """Piecewise-constant-in-shell spectrum evaluated on the 3D k grid."""
        return np.asarray(Pbins, dtype=np.float32)[self.kbin]

    def white_bin_power(self, wk):
        """Per-shell power of the white noise itself (expectation 1, but it fluctuates).
        Dividing by this is what makes a floor field reproduce the gravity field's MEASURED
        P(k) rather than its expectation: without it the same |w_k|^2 fluctuation is applied
        twice -- once in the target, once in the floor -- and the low-k bins miss by ~35 %."""
        pw = (wk.real.astype(np.float64) ** 2 + wk.imag.astype(np.float64) ** 2)
        w = self.wmode.astype(np.float64) * self.mask0 * self.nyq
        num = np.bincount(self.kbin.ravel(), weights=(pw * w).ravel(), minlength=self.nbin)
        den = np.bincount(self.kbin.ravel(), weights=w.ravel(), minlength=self.nbin)
        return num / np.maximum(den, 1e-30) / self.N ** 3

    def smooth(self, f, R):
        return self.smooth_k(self.fwd(f), R)

    def smooth_k(self, F, R):
        W = np.exp(-0.5 * (self.kk.astype(np.float64) * R) ** 2).astype(np.float32)
        return self.inv(F * W).astype(F32)


# =====================================================================================
# GRAVITY -- second-order Eulerian PT (arm G2) and the 2LPT source
# =====================================================================================
def psi_second_derivs(g, d1k):
    """psi^(1)_,ij = IFFT[ k_i k_j delta_k / k^2 ]; trace = delta.  Returns dict."""
    N = g.N
    kv = [g.kx, g.kx, g.kz]
    shp = [(N, 1, 1), (1, N, 1), (1, 1, len(g.kz))]
    out = {}
    for i in range(3):
        for j in range(i, 3):
            ki = kv[i].reshape(shp[i]).astype(np.float32)
            kj = kv[j].reshape(shp[j]).astype(np.float32)
            out[(i, j)] = g.inv(d1k * (ki * kj * g.inv_k2)).astype(F32)
    return out


def spt2_sectors(g, d1, d1k, psi_ij):
    """LOCAL, SHIFT, TIDAL contributions to delta^(2) (Eulerian second order)."""
    N = g.N
    kv = [g.kx, g.kx, g.kz]
    shp = [(N, 1, 1), (1, N, 1), (1, 1, len(g.kz))]
    local = (17.0 / 21.0) * (d1 * d1)
    # SHIFT = grad(psi) . grad(delta),  psi_k = -delta_k/k^2
    shift = np.zeros_like(d1)
    for i in range(3):
        ki = kv[i].reshape(shp[i]).astype(np.float32)
        gp = g.inv((-1j) * (ki * g.inv_k2) * d1k).astype(F32)     # (grad psi)_i
        gd = g.inv((1j) * ki * d1k).astype(F32)                   # (grad delta)_i
        shift += gp * gd
        del gp, gd
    # TIDAL = 2/7 * s_ij s_ij,  s_ij = psi_,ij - delta_ij delta/3
    t = np.zeros_like(d1)
    for i in range(3):
        s = psi_ij[(i, i)] - d1 / 3.0
        t += s * s
        del s
    for (i, j) in [(0, 1), (0, 2), (1, 2)]:
        t += 2.0 * psi_ij[(i, j)] ** 2
    tidal = (2.0 / 7.0) * t
    del t
    return local, shift, tidal


def lpt_source(psi_ij):
    """S = sum_{i<j} [psi_,ii psi_,jj - psi_,ij^2]  (the 2LPT second-order source)."""
    p11, p22, p33 = psi_ij[(0, 0)], psi_ij[(1, 1)], psi_ij[(2, 2)]
    S = p11 * p22 + p11 * p33 + p22 * p33
    S -= psi_ij[(0, 1)] ** 2
    S -= psi_ij[(0, 2)] ** 2
    S -= psi_ij[(1, 2)] ** 2
    return S


def _cic_raw(g, psi, shift=0.0, chunks=4):
    """CIC-deposit one particle per grid cell displaced by psi (list of 3 arrays, Mpc/h)
    onto a grid offset by `shift` cells.  Returns delta = n/<n> - 1."""
    N, cell = g.N, g.cell
    acc = np.zeros(N ** 3, dtype=np.float64)
    step = max(1, N // chunks)
    ar = np.arange(N) + shift
    for lo in range(0, N, step):
        hi = min(lo + step, N)
        px = (ar[lo:hi, None, None] + psi[0][lo:hi] / cell).astype(np.float64)
        py = (ar[None, :, None] + psi[1][lo:hi] / cell).astype(np.float64)
        pz = (ar[None, None, :] + psi[2][lo:hi] / cell).astype(np.float64)
        px = np.broadcast_to(px, (hi - lo, N, N)).copy()
        py = np.broadcast_to(py, (hi - lo, N, N)).copy()
        pz = np.broadcast_to(pz, (hi - lo, N, N)).copy()
        i0 = np.floor(px).astype(np.int64); dx = (px - i0); i0 = np.mod(i0, N); del px
        j0 = np.floor(py).astype(np.int64); dy = (py - j0); j0 = np.mod(j0, N); del py
        k0 = np.floor(pz).astype(np.int64); dz = (pz - k0); k0 = np.mod(k0, N); del pz
        i1 = (i0 + 1) % N; j1 = (j0 + 1) % N; k1 = (k0 + 1) % N
        for a in range(2):
            ii = i1 if a else i0
            wa = dx if a else (1.0 - dx)
            for b in range(2):
                jj = j1 if b else j0
                wb = wa * (dy if b else (1.0 - dy))
                base = (ii * N + jj) * N
                for c in range(2):
                    kkk = k1 if c else k0
                    wc = wb * (dz if c else (1.0 - dz))
                    acc += np.bincount((base + kkk).ravel(), weights=wc.ravel(),
                                       minlength=N ** 3)
                del wb
        del i0, j0, k0, i1, j1, k1, dx, dy, dz
    m = acc.mean()
    return (acc.reshape(N, N, N) / m - 1.0).astype(F32)


def cic_deposit(g, psi, interlace=True):
    """CIC deposit with INTERLACING (Sefusatti, Crocce, Scoccimarro & Couchman 2016 --
    standard, credited).  Depositing a second time onto a half-cell-offset grid and
    averaging with the phase e^{i k.H} cancels the ODD aliases of the displaced particle
    lattice exactly.  Without it the alias is O(eps) at ~11 % of the linear signal at
    k = k_nyq/4 (gate GF2's note), and -- the reason it cannot simply be tolerated -- that
    alias is a deterministic function of the field, so it CORRELATES with delta^(2) and
    contaminates the second-order amplitude rather than merely adding noise."""
    d = _cic_raw(g, psi, shift=0.0)
    if not interlace:
        return d
    d2 = _cic_raw(g, psi, shift=0.5)
    N = g.N
    ph = np.exp(0.5j * g.cell * (g.kx[:, None, None] + g.kx[None, :, None]
                                 + g.kz[None, None, :])).astype(np.complex64)
    out = g.inv(0.5 * (g.fwd(d) + ph * g.fwd(d2))).astype(F32)
    del d, d2, ph
    return out


def build_gravity(g, wk, D=1.0, want_sectors=False, want_za=True):
    """Returns dict of gravity arms from one white-noise realisation."""
    Pgrid = pk_lin(np.maximum(g.kk.astype(np.float64), 1e-8)).astype(np.float32)
    Pgrid[0, 0, 0] = 0.0
    d1 = D * g.gauss_from_white(wk, Pgrid)
    del Pgrid
    d1k = g.fwd(d1)
    psi_ij = psi_second_derivs(g, d1k)
    out = {'LIN': d1}

    if want_sectors:
        local, shift, tidal = spt2_sectors(g, d1, d1k, psi_ij)
        out['SPT2'] = (d1 + local + shift + tidal).astype(F32)
        out['SPT2_LOCAL'] = (d1 + local).astype(F32)
        out['SPT2_SHIFT'] = (d1 + shift).astype(F32)
        out['SPT2_TIDAL'] = (d1 + tidal).astype(F32)
        out['_mono_viol'] = float((d1 < -21.0 / 34.0).mean())
        del local, shift, tidal
    else:
        local, shift, tidal = spt2_sectors(g, d1, d1k, psi_ij)
        out['SPT2'] = (d1 + local + shift + tidal).astype(F32)
        out['_mono_viol'] = float((d1 < -21.0 / 34.0).mean())
        del local, shift, tidal

    # --- displacements ---
    N = g.N
    kv = [g.kx, g.kx, g.kz]
    shp = [(N, 1, 1), (1, N, 1), (1, 1, len(g.kz))]
    S = lpt_source(psi_ij)
    del psi_ij
    Sk = g.fwd(S)
    del S
    psi1 = []
    for i in range(3):
        ki = kv[i].reshape(shp[i]).astype(np.float32)
        psi1.append(g.inv((1j) * (ki * g.inv_k2) * d1k).astype(F32))
    del d1k
    if want_za:
        out['ZA'] = cic_deposit(g, psi1)
    for i in range(3):
        ki = kv[i].reshape(shp[i]).astype(np.float32)
        psi1[i] += (3.0 / 7.0) * g.inv((1j) * (ki * g.inv_k2) * Sk).astype(F32)
    del Sk
    out['2LPT'] = cic_deposit(g, psi1)
    del psi1
    return out


# =====================================================================================
# POINTWISE FLOORS -- exactly T(Gaussian), tuned on the SPECTRUM (not the realisation)
# =====================================================================================
def make_lognormal_T(sig):
    """delta = exp(sig*g/sigma_g - sig^2/2) - 1.  Standardising g inside the map pins the
    output variance at exp(sig^2)-1 exactly, so the spectrum iteration only has to fix the
    SHAPE of P(k), not its amplitude."""
    def T(gf):
        s = float(gf.std())
        return (np.exp((sig / s) * gf - 0.5 * sig * sig) - 1.0).astype(F32)
    return T


def rank_table(target_field, nq=8193, sub=1 << 22, seed=7):
    """Quantile table of the target's one-point law.  Built ONCE per realisation."""
    rng = np.random.default_rng(seed)
    v = target_field.ravel()
    idx = rng.integers(0, v.size, size=min(sub, v.size))
    srt = np.sort(v[idx].astype(np.float64))
    qlev = ((np.arange(nq) + 0.5) / nq).astype(np.float32)
    return qlev, np.quantile(srt, qlev).astype(np.float32)


def make_rank_T(tab):
    """Monotone map carrying a standard Gaussian onto the tabulated one-point law."""
    qlev, qval = tab

    def T(gf):
        u = special.ndtr((gf / gf.std()).astype(np.float64)).astype(np.float32)
        return np.interp(u, qlev, qval).astype(F32)
    return T


def tune_floor(g, wk, Ptarget_bins, T_factory, n_iter=5, tol=0.005, wn=None):
    """Fixed point on the SPECTRUM: P_g <- P_g * Ptarget/Pmeasured, white noise fixed.
    Output is exactly T(Gaussian), so share_eq_zero_of_signSymmetric still applies."""
    if wn is None:
        wn = g.white_bin_power(wk)
    Pbase3d = (pk_lin(np.maximum(g.kk.astype(np.float64), 1e-8))
               / np.maximum(wn, 1e-30)[g.kbin]).astype(np.float32)
    Pbase3d[0, 0, 0] = 0.0
    Pb_bins = np.maximum(pk_lin(np.maximum(g.kcen, 1e-8)), 1e-30)
    c = np.maximum(Ptarget_bins, 0.0) / Pb_bins
    hist = []
    gf = None
    for it in range(n_iter):
        gf = g.gauss_from_white(wk, Pbase3d * np.asarray(c, dtype=np.float32)[g.kbin])
        T = T_factory(gf)
        f = T(gf)
        Pm = g.measure_P(f)
        ok = (Ptarget_bins > 0) & (Pm > 0) & (g.modes > 20)
        rel = np.abs(Pm[ok] / Ptarget_bins[ok] - 1.0)
        hist.append(float(rel.max()))
        if hist[-1] < tol:
            break
        c = np.where(ok, c * np.where(Pm > 0, Ptarget_bins / np.maximum(Pm, 1e-30), 1.0), c)
        c = np.maximum(c, 0.0)
        del f, T
    T = T_factory(gf)
    f = T(gf)
    return f, gf, c, hist


# =====================================================================================
# THE INSTRUMENT -- b=2 sign triples on a strided sub-lattice
# =====================================================================================
def binarise(f):
    med = float(np.median(f))
    sb = f > med
    tied = float(np.count_nonzero(f == np.float32(med))) / f.size
    return sb, tied, med


def _perm(d, s):
    return tuple(d[(j - s) % 3] for j in range(3))


def geometries(rc):
    """Displacement pairs in CELLS; each entry is a list of 3 lattice orientations."""
    rc = int(max(1, rc))
    h = int(max(1, round(rc / 2.0)))
    v = int(max(1, round(rc * np.sqrt(3) / 2.0)))
    q = int(max(1, round(rc / 4.0)))
    base = {
        'equilateral': ((rc, 0, 0), (h, v, 0)),
        'folded':      ((rc, 0, 0), (2 * rc, 0, 0)),
        'orthogonal':  ((rc, 0, 0), (0, rc, 0)),
        'squeezed':    ((q, 0, 0), (0, rc, 0)),
    }
    out = {}
    for name, (d1, d2) in base.items():
        out[name] = [(_perm(d1, s), _perm(d2, s)) for s in range(3)]
    return out


def side_lengths(d1, d2, cell):
    d1 = np.array(d1, float); d2 = np.array(d2, float)
    return tuple(round(float(x) * cell, 2)
                 for x in (np.linalg.norm(d1), np.linalg.norm(d2), np.linalg.norm(d1 - d2)))


def sign_hist(sb, d1, d2, stride, blocks=False):
    """8-cell sign-triple histogram on a strided sub-lattice.  With blocks=True the
    sub-lattice is split into 8 spatial octants and one histogram per octant is returned,
    so a per-realisation subsample error bar comes for free at no extra cost."""
    N = sb.shape[0]
    i = np.arange(0, N, stride)
    if not blocks:
        parts = [(i, i, i)]
    else:
        h = len(i) // 2
        parts = [(i[:h] if a else i[h:], i[:h] if b else i[h:], i[:h] if c else i[h:])
                 for a in (0, 1) for b in (0, 1) for c in (0, 1)]
    out = []
    for (ax, ay, az) in parts:
        a = sb[np.ix_(ax, ay, az)]
        b = sb[np.ix_((ax + d1[0]) % N, (ay + d1[1]) % N, (az + d1[2]) % N)]
        c = sb[np.ix_((ax + d2[0]) % N, (ay + d2[1]) % N, (az + d2[2]) % N)]
        idx = (a.astype(np.uint8) << 2) | (b.astype(np.uint8) << 1) | c.astype(np.uint8)
        out.append(np.bincount(idx.ravel(), minlength=8).astype(np.float64))
    return out


def triple_read(sb, orients, stride):
    """Returns (I, E, per-orientation E, octant-subsample SEM on E).

    Pooling over the 3 lattice orientations is a MIXTURE, and mixtures manufacture
    higher-order structure (the Kahle mechanism) -- it is legitimate here only because the
    three lattice orientations are exactly equivalent under the cubic symmetry of the grid
    and of an isotropic field, so the mixture is a mixture of identical laws.  The
    per-orientation spread is returned so that assumption is CHECKED (gate GH), not assumed.
    """
    Es, hs = [], np.zeros(8)
    blk = np.zeros((8, 8))
    for (d1, d2) in orients:
        parts = sign_hist(sb, d1, d2, stride, blocks=True)
        h = sum(parts)
        hs += h
        blk += np.array(parts)
        Es.append(route_B2(h / h.sum())[1])
    p = hs / hs.sum()
    Eb = [route_B2(b / b.sum())[1] for b in blk]
    sem = float(np.std(Eb, ddof=1) / np.sqrt(8))
    return share3_ref(p), route_B2(p)[1], Es, sem


# =====================================================================================
# GATES
# =====================================================================================
def brute_F2_check(N=16, L=200.0, seed=3):
    """GF1 -- real-space delta^(2) vs a brute-force F2 convolution in Fourier space."""
    g = Grid(N, L, nbin=8)
    rng = np.random.default_rng(seed)
    w = rng.standard_normal((N, N, N)).astype(F32)
    wk = g.fwd(w)
    P = pk_lin(np.maximum(g.kk.astype(np.float64), 1e-8)).astype(np.float32)
    P[0, 0, 0] = 0.0
    d1 = g.gauss_from_white(wk, P)
    d1 = (d1 - d1.mean()).astype(F32)
    d1k = g.fwd(d1)
    psi_ij = psi_second_derivs(g, d1k)
    loc, shf, tid = spt2_sectors(g, d1, d1k, psi_ij)
    d2_real = g.fwd((loc + shf + tid).astype(np.float64))

    # brute force on the FULL fft grid
    Fk = sfft.fftn(d1.astype(np.float64))
    kf = 2 * np.pi / L
    kidx = np.fft.fftfreq(N) * N
    KX = kidx[:, None, None] * kf * np.ones((1, N, N))
    KY = kidx[None, :, None] * kf * np.ones((N, 1, N))
    KZ = kidx[None, None, :] * kf * np.ones((N, N, 1))
    K = np.stack([KX, KY, KZ], -1).reshape(-1, 3)
    K2 = (K * K).sum(1)
    F1 = Fk.ravel()
    ii = np.arange(N ** 3)
    ix, iy, iz = np.unravel_index(ii, (N, N, N))
    out = np.zeros(N ** 3, dtype=np.complex128)
    for m in range(N ** 3):
        jx = (ix[m] - ix) % N
        jy = (iy[m] - iy) % N
        jz = (iz[m] - iz) % N
        j = (jx * N + jy) * N + jz
        k1 = K
        k2 = K[j]
        k1s, k2s = K2, K2[j]
        good = (k1s > 0) & (k2s > 0)
        dot = (k1 * k2).sum(1)
        mu = np.zeros(N ** 3)
        np.divide(dot, np.sqrt(np.maximum(k1s * k2s, 1e-300)), out=mu, where=good)
        r = np.zeros(N ** 3)
        np.divide(np.sqrt(k1s), np.sqrt(np.maximum(k2s, 1e-300)), out=r, where=good)
        F2 = 17.0 / 21.0 + 0.5 * mu * (r + 1.0 / np.maximum(r, 1e-300)) \
            + (2.0 / 7.0) * (mu * mu - 1.0 / 3.0)
        out[m] = np.sum(np.where(good, F2 * F1 * F1[j], 0.0))
    out = out.reshape(N, N, N) / N ** 3
    ref = out[:, :, :N // 2 + 1]
    m = g.kk > 0
    num = np.abs(d2_real[m] - ref[m]).max()
    den = np.abs(ref[m]).max()
    return float(num / den)


def eps_scaling_check(N=64, L=400.0, seed=11, eps=(0.2, 0.1, 0.05, 0.025)):
    """GF2 -- does the particle/CIC 2LPT pipeline actually carry eps*d1 + eps^2*d2?

    AMENDMENT, disclosed rather than patched away.  The pre-registration asked for the
    RESIDUAL of the deposited field against eps*d1 + eps^2*d2 to scale as eps^3.  It cannot:
    CIC deposit of a DISPLACED LATTICE carries an alias term
        sum_{n != 0} W_CIC(k + k_n) (k + k_n).Psi(k),
    which is O(eps) -- first order, not third -- with a size
    [sin(x)/(x+pi)]^2 * |k_n|/k  (x = k*cell/2), measured here at 11 % of the linear signal
    at k = k_nyq/4.  That is a property of the mock, not an error in it, and it is why the
    Eulerian SPT2 arm (no particles, no CIC, no aliasing) is carried alongside as the
    cross-check on every conclusion.

    Interlacing (Sefusatti et al. 2016) halves the alias but cannot remove it, and -- second
    correction, measured not assumed -- the alias is NOT uncorrelated with delta^(2): it is a
    deterministic function of the same field, and a cross-spectrum against delta^(2) still
    picks it up (corr 0.72 at the smallest eps tested).  So the alias floor eventually
    dominates the shrinking eps^2 signal from below, which is why the naive eps -> 0 test
    diverges rather than converging.

    What the gate must actually establish is that the LINEAR and SECOND-ORDER displacements
    are right in sign and coefficient.  Two projections do it, and the second is alias-clean:
      c1(eps) = <dep/W . conj(d1)>/<|d1|^2>                                  ->  eps
      c3(eps) = <(dep_2LPT - dep_ZA)/W . conj((3/7)S)>/<|(3/7)S|^2>          ->  eps^2
    c3 differences two deposits built from the SAME first-order displacement, so the O(eps)
    alias cancels and what is left is exactly the second-order displacement -3/7 D^2 grad
    psi^(2), tested for its sign and its 3/7.  Together with GF1 (the F2 kernel, exact to
    2e-7) this pins the gravity implementation.
    """
    g = Grid(N, L, nbin=8)
    rng = np.random.default_rng(seed)
    w = rng.standard_normal((N, N, N)).astype(F32)
    wk = g.fwd(w)
    P = pk_lin(np.maximum(g.kk.astype(np.float64), 1e-8)).astype(np.float32)
    P[0, 0, 0] = 0.0
    d1 = g.gauss_from_white(wk, P)
    d1 = (d1 - d1.mean()).astype(F32)
    d1k = g.fwd(d1)
    psi_ij = psi_second_derivs(g, d1k)
    loc, shf, tid = spt2_sectors(g, d1, d1k, psi_ij)
    d2 = (loc + shf + tid).astype(F32)
    del loc, shf, tid
    # CIC window
    kv = [g.kx, g.kx, g.kz]
    shp = [(N, 1, 1), (1, N, 1), (1, 1, len(g.kz))]
    Wc = np.ones(g.kk.shape)
    for i in range(3):
        x = kv[i].reshape(shp[i]) * g.cell / 2.0
        Wc = Wc * np.sinc(x / np.pi) ** 2
    S2 = ((3.0 / 7.0) * lpt_source(psi_ij)).astype(F32)
    sel = (g.kk > 0) & (g.kk < 0.25 * g.knyq)
    F1k = g.fwd(d1.astype(np.float64))[sel]
    FSk = g.fwd(S2.astype(np.float64))[sel]
    dn1 = float((np.abs(F1k) ** 2).sum())
    dnS = float((np.abs(FSk) ** 2).sum())
    c1, c3, alias = [], [], []
    for e in eps:
        out = build_gravity(g, wk, D=e)
        Fk = g.fwd(out['2LPT'].astype(np.float64))[sel] / Wc[sel]
        Fz = g.fwd(out['ZA'].astype(np.float64))[sel] / Wc[sel]
        c1.append(float((np.conj(F1k) * Fk).real.sum() / dn1))
        c3.append(float((np.conj(FSk) * (Fk - Fz)).real.sum() / dnS))
        alias.append(float(np.sqrt((np.abs(Fz - e * F1k) ** 2).mean())
                           / np.sqrt((np.abs(e * F1k) ** 2).mean())))
        del out, Fk, Fz
    sl1 = [c / e for c, e in zip(c1, eps)]
    sl3 = float(np.polyfit(np.log(eps), np.log(np.abs(c3)), 1)[0])
    co3 = [c / e ** 2 for c, e in zip(c3, eps)]
    return sl1, sl3, co3, alias


def gate(N=384, L=1500.0):
    log("=" * 78); log("GATE"); log("=" * 78)
    res, ok = {}, True

    def chk(name, passed, detail):
        nonlocal ok
        ok = ok and bool(passed)
        res[name] = dict(passed=bool(passed), detail=detail)
        log(f"  [{'PASS' if passed else 'FAIL'}] {name}: {detail}")

    # GA -- the b=2 machinery, re-validated here
    rng = np.random.default_rng(20260725)
    par = np.zeros(8)
    for i in range(2):
        for j in range(2):
            par[i * 4 + j * 2 + ((i + j) % 2)] = 0.25
    chk("GA1 parity -> ln2", abs(share3_ref(par) - np.log(2)) < 1e-12,
        f"{share3_ref(par):.15f}")
    chk("GA2 independence -> 0", abs(share3_ref(np.full(8, 0.125))) < 1e-14,
        f"{share3_ref(np.full(8, 0.125)):.3e}")
    worst = 0.0
    for _ in range(2000):
        h = rng.dirichlet(np.full(4, 0.8)) / 2.0
        p = np.zeros(8)
        for c in range(4):
            p[c] = h[c]; p[7 - c] = h[c]
        worst = max(worst, abs(share3_ref(p)))
    chk("GA3 sign-symmetric states -> 0 (2000 random)", worst < 1e-12, f"max = {worst:.3e}")

    # GF1 -- the F2 kernel
    t0 = time.time()
    e = brute_F2_check()
    chk("GF1 real-space delta^(2) vs brute-force F2 convolution (16^3)",
        e < 1e-5, f"max rel dev = {e:.3e}  ({time.time()-t0:.1f}s)")

    # GF2 -- the particle pipeline against the kernel
    t0 = time.time()
    sl1, sl3, co3, alias = eps_scaling_check()
    chk("GF2a linear displacement: <dep/W . d1*>/<|d1|^2> -> eps",
        max(abs(x - 1.0) for x in sl1) < 0.02, f"c1/eps = {['%.4f' % x for x in sl1]}")
    chk("GF2b second-order displacement (2LPT-ZA, alias-clean) -> eps^2 with coeff 3/7",
        abs(sl3 - 2.0) < 0.15 and max(abs(x - 1.0) for x in co3) < 0.12,
        f"exponent = {sl3:.3f}, c3/eps^2 = {['%.3f' % x for x in co3]}"
        f"  ({time.time()-t0:.1f}s)")
    log(f"  [note] CIC displaced-lattice alias, |ZA_dec - eps*d1|/|eps*d1| at k<k_nyq/4: "
        f"{['%.3f' % x for x in alias]}  -- O(eps), a property of the mock (see GF2 docstring)")
    res['cic_alias_frac'] = alias

    # --- one full-size realisation for the field-level gates ---
    g = Grid(N, L)
    log(f"\n  field gates on N={N}, L={L} (cell {g.cell:.3f} Mpc/h, "
        f"V={(L/1000.)**3:.2f} (Gpc/h)^3)")
    t0 = time.time()
    w = np.random.default_rng(20260726).standard_normal((N, N, N)).astype(F32)
    wk = g.fwd(w); del w
    arms = build_gravity(g, wk)
    log(f"    gravity arms built in {time.time()-t0:.1f}s")
    Ptar = g.measure_P(arms['2LPT'])
    Plin = g.measure_P(arms['LIN'])
    Fl = g.fwd(arms['LIN']); F2 = g.fwd(arms['2LPT'])
    wt = (g.wmode * g.mask0).astype(np.float64)
    xk = (Fl.real.astype(np.float64) * F2.real.astype(np.float64)
          + Fl.imag.astype(np.float64) * F2.imag.astype(np.float64)) * g.Vcell / g.N ** 3
    Px = (np.bincount(g.kbin.ravel(), weights=(xk * wt).ravel(), minlength=g.nbin)
          / np.maximum(np.bincount(g.kbin.ravel(), weights=wt.ravel(), minlength=g.nbin), 1e-30))
    del Fl, F2, xk

    # GF3 -- AMENDED.  The pre-registration expected P_2LPT/P_lin > 1 at high k.  It is not:
    # LPT displacement smearing DAMPS small-scale power (exp(-k^2 sigma_Psi^2/2), sigma_Psi
    # ~ 6 Mpc/h at z=0), and CIC damps it further.  That is a known limitation of LPT against
    # N-body, not an implementation error, and it is recorded as such -- it makes this
    # forecast a lower anchor at small R, which section 0 of the prereg already stakes.
    # What IS gated is the part that would catch an implementation error: at low k the mock
    # must reproduce the linear field, in amplitude AND phase.
    ok3 = (g.kcen > 0) & (g.kcen < 0.06) & (g.modes > 20)
    r_lo = float(np.mean(Ptar[ok3] / np.maximum(Plin[ok3], 1e-30)))
    rx = float(np.min(Px[ok3] / np.maximum(np.sqrt(Ptar[ok3] * Plin[ok3]), 1e-30)))
    hi = (g.kcen > 0.3) & (g.kcen < 0.8 * g.knyq) & (g.modes > 0)
    r_hi = float(np.mean(Ptar[hi] / np.maximum(Plin[hi], 1e-30)))
    chk("GF3 2LPT reproduces the linear field at low k (k<0.06) in amplitude and phase",
        abs(r_lo - 1) < 0.10 and rx > 0.97,
        f"P ratio {r_lo:.4f}, min cross-corr {rx:.4f}   [high-k ratio {r_hi:.3f} = LPT "
        f"displacement damping, logged not gated]")

    # floors
    t0 = time.time()
    wn = g.white_bin_power(wk)
    sigt = float(np.sqrt(np.log(1.0 + arms['2LPT'].astype(np.float64).var())))
    fLN, gLN, _, hLN = tune_floor(g, wk, Ptar, lambda gf: make_lognormal_T(sigt), wn=wn)
    tabR = rank_table(arms['2LPT'])
    fRK, gRK, _, hRK = tune_floor(g, wk, Ptar, lambda gf: make_rank_T(tabR), wn=wn)
    fG0 = g.gauss_from_white(wk, g.P_on_grid(Ptar / np.maximum(wn, 1e-30)))
    log(f"    floors tuned in {time.time()-t0:.1f}s  (LN residual {hLN[-1]:.4f}, "
        f"rank residual {hRK[-1]:.4f})")

    # GC -- the theorem on this pipeline, pre-smoothing
    nd, ndr = [], []
    for (f, gf) in [(fLN, gLN), (fRK, gRK)]:
        sa, _, ma = binarise(f)
        sb, _, _ = binarise(gf)
        diff = (sa != sb)
        nd.append(int(np.count_nonzero(diff)))
        # a disagreement is only a THEOREM violation if the value is not within float32
        # rounding of the median; at the boundary a monotone map can reorder in float32.
        ndr.append(int(np.count_nonzero(diff & (np.abs(f - np.float32(ma))
                                                > 8 * np.spacing(np.float32(abs(ma)))))))
        del sa, sb, diff
    chk("GC floor sign pattern identical to its parent Gaussian, beyond float32 rounding",
        max(ndr) == 0,
        f"differing cells of {N**3}: lognormal {nd[0]}, rank {nd[1]}; "
        f"not explained by rounding at the median: {ndr}")

    # GD -- P(k) match
    Pln, Prk, Pg0 = g.measure_P(fLN), g.measure_P(fRK), g.measure_P(fG0)
    sel = (g.kcen > 0) & (g.kcen < 2.0 / 10.0) & (g.modes > 20)
    dev = {n: float(np.abs(P[sel] / Ptar[sel] - 1).max())
           for n, P in [('F0', Pg0), ('F1', Pln), ('F2', Prk)]}
    chk("GD P(k) match to the 2LPT target for kR<=2 at R=10",
        max(dev.values()) < 0.03, f"max frac dev: {dev}")

    # GB / GE / GH -- strided reading, the Gaussian null, and orientation pooling.
    # All three are judged against the OCTANT-SUBSAMPLE error bar, because a single
    # realisation cannot be tested against an absolute threshold: on a small box the
    # Gaussian arm's |E| is dominated by its own sampling noise, which is the point.
    Rtest = 25.0
    st = max(1, int(round(Rtest / g.cell / 3)))
    fields = {'2LPT': arms['2LPT'], 'LIN': arms['LIN'], 'F0': fG0}
    gb, gez, gh, tied = 0.0, [], 0.0, 0.0
    geo = geometries(int(round(2 * Rtest / g.cell)))
    for nm, f in fields.items():
        sm = g.smooth(f, Rtest)
        sbv, tied, _ = binarise(sm)
        for gname, orients in geo.items():
            I, E, Es, sem = triple_read(sbv, orients, st)
            if nm == '2LPT' and abs(E) > 5 * sem:          # only where there IS a signal
                I2, E2, _, _ = triple_read(sbv, orients, max(1, st // 2))
                gb = max(gb, abs(E - E2) / abs(E))
                gh = max(gh, float(np.std(Es, ddof=1) / np.sqrt(3)) / abs(E))
            if nm in ('LIN', 'F0'):
                gez.append(abs(E) / max(sem, 1e-30))
        del sm, sbv
    chk("GB stride convergence on the 2LPT arm (E at stride vs stride/2, |E|>5 sigma)",
        gb < 0.05, f"max rel change = {gb:.4f} (stride {st})")
    chk("GE Gaussian/linear arms read zero within their own octant error",
        max(gez) < 4.0, f"max |E|/sigma over LIN and F0 = {max(gez):.2f}")
    chk("GH orientation pooling is a mixture of IDENTICAL laws (2LPT arm)",
        gh < 0.5, f"max orientation SEM / |E| = {gh:.4f}")
    res['tied_fraction'] = tied

    res['ALL_PASS'] = bool(ok)
    log(f"\nGATE: {'ALL PASS' if ok else 'FAILURE -- refusing to forecast'}")
    return res, ok


# =====================================================================================
# THE SWEEP
# =====================================================================================
ARMS_MAIN = ['2LPT', 'ZA', 'SPT2', 'LIN', 'F0', 'F1', 'F2']


def one_realisation(g, seed, Rs, D=1.0, sectors=False, rmults=(2.0,), want_za=False):
    w = np.random.default_rng(seed).standard_normal((g.N,) * 3).astype(F32)
    wk = g.fwd(w); del w
    arms = build_gravity(g, wk, D=D, want_sectors=sectors, want_za=want_za)
    mono = arms.pop('_mono_viol')
    Ptar = g.measure_P(arms['2LPT'])
    wn = g.white_bin_power(wk)
    sigt = float(np.sqrt(np.log(1.0 + arms['2LPT'].astype(np.float64).var())))
    arms['F1'], _, _, hLN = tune_floor(g, wk, Ptar,
                                       lambda gf: make_lognormal_T(sigt), wn=wn)
    tabR = rank_table(arms['2LPT'])
    arms['F2'], _, _, hRK = tune_floor(g, wk, Ptar, lambda gf: make_rank_T(tabR), wn=wn)
    arms['F0'] = g.gauss_from_white(wk, g.P_on_grid(Ptar / np.maximum(wn, 1e-30)))
    del wk

    sel = (g.kcen > 0) & (g.kcen < 2.0 / min(Rs)) & (g.modes > 20)
    pdev = {n: float(np.abs(g.measure_P(arms[n])[sel] / Ptar[sel] - 1).max())
            for n in ('F0', 'F1', 'F2')}

    out = dict(seed=seed, D=D, mono_viol=mono, pk_dev=pdev,
               ln_resid=hLN[-1], rank_resid=hRK[-1], R={R: dict(
                   stride=max(1, int(round(R / g.cell / 3))),
                   sigma_R_lin=sigma_R_gauss(R, D), arms={}) for R in Rs})
    for nm in list(arms.keys()):
        Fk = g.fwd(arms.pop(nm))          # one forward FFT per arm, reused at every R
        for R in Rs:
            rec = out['R'][R]
            st = rec['stride']
            sm = g.smooth_k(Fk, R)
            sbv, tied, _ = binarise(sm)
            rec['sigma_%s' % nm] = float(sm.std())
            rec['skew_%s' % nm] = float(((sm - sm.mean()) ** 3).mean() / sm.std() ** 3)
            del sm
            e = {}
            for rm in rmults:
                rc = int(max(1, round(rm * R / g.cell)))
                for gname, orients in geometries(rc).items():
                    I, E, Es, sem = triple_read(sbv, orients, st)
                    e[f"{gname}_r{rm:g}"] = dict(
                        I=float(I), E=float(E), sem_oct=sem,
                        E_orient=[float(x) for x in Es],
                        sides=side_lengths(*orients[0], g.cell))
            rec['arms'][nm] = dict(tied=tied, cfg=e)
            del sbv
        del Fk
    del arms
    return out


def sweep(N, L, Rs, n_real, seed0, tag, D=1.0, sectors=False, rmults=(2.0,),
          want_za=False):
    log("\n" + "=" * 78)
    log(f"SWEEP [{tag}]  N={N} L={L} V={(L/1000.)**3:.3f} (Gpc/h)^3  n_real={n_real} D={D}")
    log("=" * 78)
    g = Grid(N, L)
    runs = []
    for r in range(n_real):
        t0 = time.time()
        runs.append(one_realisation(g, seed0 + 1000 * r, Rs, D=D, sectors=sectors,
                                    rmults=rmults, want_za=want_za))
        log(f"  realisation {r+1}/{n_real} in {time.time()-t0:.1f}s   "
            f"P(k) dev {runs[-1]['pk_dev']}")
    return dict(tag=tag, N=N, L=L, V=(L / 1000.) ** 3, n_real=n_real, D=D, Rs=list(Rs),
                runs=runs)


# =====================================================================================
# POISSON GATE
# =====================================================================================
def poisson_gate(N=384, L=1500.0, Rs=(25.0, 60.0), nbars=(1e-4, 3e-4, 1e-3, 3e-3, 1e-2),
                 n_real=3, seed0=20260901):
    log("\n" + "=" * 78)
    log("POISSON GATE -- does shot noise manufacture share on an EXACT-ZERO field?")
    log("=" * 78)
    g = Grid(N, L)
    runs = []
    for r in range(n_real):
        w = np.random.default_rng(seed0 + 1000 * r).standard_normal((N,) * 3).astype(F32)
        wk = g.fwd(w); del w
        arms = build_gravity(g, wk)
        Ptar = g.measure_P(arms['2LPT'])
        wn = g.white_bin_power(wk)
        base = {'F0': g.gauss_from_white(wk, g.P_on_grid(Ptar / np.maximum(wn, 1e-30))),
                '2LPT': arms['2LPT']}
        del arms, wk
        rng = np.random.default_rng(seed0 + 77 + r)
        rec = {}
        for nm, f in base.items():
            lam0 = np.maximum(1.0 + f.astype(np.float64), 0.0)
            for nb in list(nbars) + [np.inf]:
                if np.isfinite(nb):
                    lam = (nb * g.Vcell) * lam0
                    n = rng.poisson(lam).astype(F32)
                    d = (n / (nb * g.Vcell) - 1.0).astype(F32)
                    del n, lam
                else:
                    d = f
                for R in Rs:
                    st = max(1, int(round(R / g.cell / 3)))
                    sm = g.smooth(d, R)
                    sbv, tied, _ = binarise(sm)
                    rc = int(max(1, round(2 * R / g.cell)))
                    for gname, orients in geometries(rc).items():
                        I, E, _, sem = triple_read(sbv, orients, st)
                        rec.setdefault((nm, float(nb), R, gname), []).append(
                            (I, E, sem, tied))
                    del sm, sbv
                if np.isfinite(nb):
                    del d
            del lam0
        runs.append({f"{k[0]}|{k[1]}|{k[2]}|{k[3]}": v for k, v in rec.items()})
        log(f"  realisation {r+1}/{n_real} done")
        del base
    return dict(N=N, L=L, Rs=list(Rs), nbars=list(nbars), n_real=n_real, runs=runs)


# =====================================================================================
if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    t0 = time.time()
    out = {}
    if what in ('gate', 'all'):
        gN = int(os.environ.get('SKY_GN', '384'))
        gL = float(os.environ.get('SKY_GL', '1500'))
        gres, ok = gate(N=gN, L=gL)
        out['gate'] = gres
        json.dump(out, open(os.path.join(HERE, 'sky_forecast_gate.json'), 'w'),
                  indent=1, default=float)
        if not ok:
            log("\nGATE FAILED -- refusing to forecast.")
            sys.exit(1)
    if what in ('sweep', 'all'):
        N = int(os.environ.get('SKY_N', '384'))
        r = {}
        r['small'] = sweep(N, float(os.environ.get('SKY_LS', '768')),
                           [10.0, 15.0, 25.0, 40.0],
                           int(os.environ.get('SKY_NR', '6')), 20260801, 'small-scale',
                           rmults=(1.5, 3.0))
        json.dump(r, open(os.path.join(HERE, 'sky_forecast_sweep.json'), 'w'),
                  indent=1, default=float)
        r['large'] = sweep(N, float(os.environ.get('SKY_LL', '1920')),
                           [40.0, 60.0, 100.0, 150.0],
                           int(os.environ.get('SKY_NR', '6')), 20260802, 'large-scale',
                           rmults=(1.5, 3.0))
        json.dump(r, open(os.path.join(HERE, 'sky_forecast_sweep.json'), 'w'),
                  indent=1, default=float)
        out['sweep'] = r
    if what in ('sectors', 'all'):
        s = sweep(int(os.environ.get('SKY_N', '384')), 1920.0, [40.0, 100.0],
                  4, 20260803, 'sectors', sectors=True, want_za=True, rmults=(1.5, 3.0))
        json.dump(s, open(os.path.join(HERE, 'sky_forecast_sectors.json'), 'w'),
                  indent=1, default=float)
        out['sectors'] = s
    if what in ('growth', 'all'):
        s = sweep(int(os.environ.get('SKY_N', '384')), 768.0, [15.0, 25.0], 3,
                  20260804, 'growth-D0.6', D=0.6, rmults=(1.5, 3.0))
        json.dump(s, open(os.path.join(HERE, 'sky_forecast_growth.json'), 'w'),
                  indent=1, default=float)
        out['growth'] = s
    if what in ('poisson', 'all'):
        p = poisson_gate(N=int(os.environ.get('SKY_PN', '384')))
        json.dump(p, open(os.path.join(HERE, 'sky_forecast_poisson.json'), 'w'),
                  indent=1, default=float)
        out['poisson'] = p
    log(f"\nelapsed {time.time()-t0:.1f}s")
