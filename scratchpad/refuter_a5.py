#!/usr/bin/env python3
"""
refuter_a5.py -- ATTACK A5: independent recomputation of the primary reading.

Shares NO estimator code with the pipeline.  Everything downstream of the gridded masked
delta is rewritten here:

  smoothing        my own Gaussian kernel on my own k-grid, via numpy.fft (the pipeline uses
                   scipy.fft and a cached k2 array)
  masked division  W*(dM)/(W*M) with the denominator built here from the mask
  binning          exact quantiles over ALL valid cells (variant 'exact'), and a separately
                   coded reproduction of the pipeline's 4194304-cell subsample recipe
                   (variant 'sub'), so that a disagreement can be localised
  shifts           periodic shift by concatenation, not np.roll
  histogram        my own flat index and accumulation
  maxent           DUAL / L-BFGS on  L = logsumexp(f+g+h) - <f,P12> - <g,P13> - <h,P23>,
                   not IPF.  q is exp(f_ij+g_ik+h_jk)/Z by construction, so the pair-marginal
                   residual is an independent convergence certificate.

The only things reused are the DATA LOADING and the FIELD CONSTRUCTION (geometry, deposit,
delta) -- the brief says "from the gridded fields", and rewriting the survey geometry would be
testing a different thing.

Post-unblind, post-hoc.  Pre-registered in REFUTER_PREREG.md.
"""
import json
import os
import sys
import time

import numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_realdata import log                                                  # noqa: E402
from sky_stage6 import DataGeometry, load_galaxies, ZMIN, ZMAX                # noqa: E402
from sky_stage7 import read_field, poisson_resample                           # noqa: E402
from sky_surrogate import phase_randomise                                     # noqa: E402

PRIMARY = [(15.0, 4), (15.0, 6), (10.0, 4), (10.0, 6), (10.0, 8)]
SEED0 = 20261201


# ------------------------------------------------------------------ my smoothing
def my_kgrid(shape, cell):
    kx = 2 * np.pi * np.fft.fftfreq(shape[0], d=cell)
    ky = 2 * np.pi * np.fft.fftfreq(shape[1], d=cell)
    kz = 2 * np.pi * np.fft.rfftfreq(shape[2], d=cell)
    return (kx[:, None, None] ** 2 + ky[None, :, None] ** 2 + kz[None, None, :] ** 2)


def my_smooth(field, k2, shape, R):
    F = np.fft.rfftn(field.astype(np.float64))
    F *= np.exp(-0.5 * k2 * R * R)
    return np.fft.irfftn(F, s=shape)


def my_masked_smooth(field, mask, k2, shape, R, thr=0.99):
    num = my_smooth(field * mask, k2, shape, R)
    den = my_smooth(mask, k2, shape, R)
    ok = den > thr
    out = np.zeros_like(num)
    np.divide(num, den, out=out, where=ok)
    return out, ok


# ------------------------------------------------------------------ my binning
def my_labels_exact(sm, ok, b):
    """Exact quantile edges over every valid cell -- no subsampling."""
    v = np.sort(sm[ok])
    n = v.size
    edges = np.array([v[min(n - 1, int(np.ceil(n * i / b)) - 1)] for i in range(1, b)],
                     dtype=np.float64)
    # np.quantile with the pipeline's default ('linear') on the full set, for comparison
    edges_lin = np.quantile(v, np.arange(1, b) / b)
    del v
    return np.searchsorted(edges_lin, sm, side='right').astype(np.uint8), edges_lin, edges


def my_labels_sub(sm, ok, b, nsub=1 << 22, seed=11):
    """Independently coded reproduction of the pipeline's documented subsample recipe."""
    v = sm[ok]
    rng = np.random.default_rng(seed)
    s = v[rng.integers(0, v.size, size=min(nsub, v.size))]
    del v
    edges = np.quantile(s.astype(np.float64), np.arange(1, b) / b)
    return np.searchsorted(edges, sm, side='right').astype(np.uint8), edges


# ------------------------------------------------------------------ my shift + histogram
def my_shift(a, d):
    """Periodic shift so that out[x] = a[x + d].  Implemented by concatenation, not np.roll."""
    out = a
    for ax, s in enumerate(d):
        if s % out.shape[ax] == 0:
            continue
        s = s % out.shape[ax]
        idx = [slice(None)] * 3
        idx[ax] = slice(s, None)
        head = out[tuple(idx)]
        idx[ax] = slice(0, s)
        tail = out[tuple(idx)]
        out = np.concatenate([head, tail], axis=ax)
    return out


def my_configs(R, cell, rmult=1.5):
    rc = int(max(1, round(rmult * R / cell)))
    base = {'folded': ((rc, 0, 0), (2 * rc, 0, 0))}
    res = {}
    for name, (d1, d2) in base.items():
        lst = []
        for s in range(3):
            lst.append((tuple(d1[(j - s) % 3] for j in range(3)),
                        tuple(d2[(j - s) % 3] for j in range(3))))
        res[name] = lst
    return res


def my_triple_hist(lab, ok, b, R, cell, stride, geom='folded'):
    sl = tuple(slice(0, lab.shape[i], stride) for i in range(3))
    H = np.zeros(b ** 3, dtype=np.float64)
    ntot = 0
    for (d1, d2) in my_configs(R, cell)[geom]:
        m = ok[sl] & my_shift(ok, d1)[sl] & my_shift(ok, d2)[sl]
        i0 = lab[sl][m].astype(np.int64)
        i1 = my_shift(lab, d1)[sl][m].astype(np.int64)
        i2 = my_shift(lab, d2)[sl][m].astype(np.int64)
        H += np.bincount(i0 * b * b + i1 * b + i2, minlength=b ** 3).astype(np.float64)
        ntot += int(m.sum())
        del m, i0, i1, i2
    return H.reshape(b, b, b), ntot


# ------------------------------------------------------------------ my maxent, DUAL not IPF
def my_pairwise_maxent(P, tol=1e-14, maxiter=20000):
    """min over (f,g,h) of  log sum_ijk exp(f_ij+g_ik+h_jk) - <f,P12> - <g,P13> - <h,P23>.
    At the optimum the pair marginals of q = exp(...)/Z equal those of P, and q is by
    construction a pairwise-exponential family member -- the maximum-entropy state carrying
    exactly the pair marginals.  Independent of iterative proportional fitting."""
    b = P.shape[0]
    P12 = P.sum(axis=2)
    P13 = P.sum(axis=1)
    P23 = P.sum(axis=0)

    def unpack(x):
        n = b * b
        return (x[:n].reshape(b, b), x[n:2 * n].reshape(b, b), x[2 * n:].reshape(b, b))

    def obj(x):
        f, g, h = unpack(x)
        A = f[:, :, None] + g[:, None, :] + h[None, :, :]
        Z = logsumexp(A)
        q = np.exp(A - Z)
        val = Z - (f * P12).sum() - (g * P13).sum() - (h * P23).sum()
        grad = np.concatenate([(q.sum(axis=2) - P12).ravel(),
                               (q.sum(axis=1) - P13).ravel(),
                               (q.sum(axis=0) - P23).ravel()])
        return val, grad

    x0 = np.zeros(3 * b * b)
    r = minimize(obj, x0, jac=True, method='L-BFGS-B',
                 options=dict(maxiter=maxiter, maxfun=maxiter * 2, ftol=1e-18, gtol=tol))
    f, g, h = unpack(r.x)
    A = f[:, :, None] + g[:, None, :] + h[None, :, :]
    q = np.exp(A - logsumexp(A))
    resid = max(np.abs(q.sum(axis=2) - P12).max(),
                np.abs(q.sum(axis=1) - P13).max(),
                np.abs(q.sum(axis=0) - P23).max())
    return q, float(resid), r


def my_connected_info(H):
    P = H / H.sum()
    q, resid, r = my_pairwise_maxent(P)
    m = P > 0
    I = float((P[m] * (np.log(P[m]) - np.log(np.maximum(q[m], 1e-300)))).sum())
    Sq = float(-(q[q > 0] * np.log(q[q > 0])).sum())
    Sp = float(-(P[m] * np.log(P[m])).sum())
    return dict(I=I, I_entropy_form=Sq - Sp, cert=abs((Sq - Sp) - I),
                marginal_resid=resid, nit=int(r.nit))


# ------------------------------------------------------------------ driver
def measure_independent(geo, fld, tag, rows=PRIMARY):
    k2 = my_kgrid(geo.mask.shape, geo.g.cell)
    mask = geo.mask.astype(np.float64)
    out = {}
    for R in sorted({r for r, _ in rows}, reverse=True):
        t0 = time.time()
        sm, ok = my_masked_smooth(fld.astype(np.float64), mask, k2, geo.mask.shape, R)
        stride = max(1, int(round(R / geo.g.cell / 3)))
        sig = float(sm[ok].std())
        for (RR, b) in rows:
            if RR != R:
                continue
            rec = {}
            for variant, labf in (('sub', my_labels_sub), ('exact', None)):
                if variant == 'sub':
                    lab, _ = my_labels_sub(sm, ok, b)
                else:
                    lab, _, _ = my_labels_exact(sm, ok, b)
                H, nt = my_triple_hist(lab, ok, b, R, geo.g.cell, stride)
                ci = my_connected_info(H)
                rec[variant] = dict(ci, n_triples=nt)
                del lab, H
            out[f"{R}|{b}|folded"] = dict(rec, sigma=sig)
            log(f"    [{tag}] R={R:.0f} b={b}: I(sub) {rec['sub']['I']:.8e}  "
                f"I(exact) {rec['exact']['I']:.8e}  resid {rec['sub']['marginal_resid']:.1e}  "
                f"[{time.time()-t0:.0f}s]")
        del sm, ok
    del k2, mask
    return out


def run(cap):
    geo = DataGeometry(cap, ZMIN, ZMAX)
    pos, w = load_galaxies(cap, ZMIN, ZMAX)
    dm, alpha = read_field(geo, pos, w)
    del pos, w
    res = {'cap': cap}
    log(f"  [{cap}] independent recomputation of the DATA")
    res['data'] = measure_independent(geo, dm, 'data')
    fm = float(geo.m32.mean())
    n2s = []
    for i in range(2):
        dpr = (phase_randomise(geo.g, dm, SEED0 + 17 * i) / np.sqrt(fm)) * geo.m32
        d2, cl = poisson_resample(geo, dpr, alpha, SEED0 + 991 * i + 3)
        del dpr
        log(f"  [{cap}] independent recomputation of the pipeline's N2, seed index {i}")
        n2s.append(measure_independent(geo, d2, f'N2#{i}'))
        del d2
    res['n2'] = n2s
    del geo, dm
    return res


if __name__ == '__main__':
    cap = sys.argv[1] if len(sys.argv) > 1 else 'SGC'
    log("=" * 96)
    log(f"REFUTER A5 -- INDEPENDENT RECOMPUTATION  cap={cap}   (post-unblind, post-hoc)")
    log("=" * 96)
    r = run(cap)
    json.dump(r, open(f"{HERE}/refuter_a5_{cap}.json", 'w'), indent=1, default=float)

    # side-by-side against the pipeline's recorded numbers
    dv = json.load(open(f"{HERE}/sky_stage7_valve.json"))[cap]
    log("\n  DATA:  pipeline I   vs   independent I    (folded)")
    log("  %-5s %-2s %14s %14s %12s %14s" % ("R", "b", "pipeline", "indep(sub)", "rel diff",
                                             "indep(exact)"))
    for (R, b) in PRIMARY:
        k = f"{R}|{b}|folded"
        if k not in r['data']:
            continue
        pe = dv['data'][str(R)]['b'][str(b)]['folded']
        if not pe.get('occupancy_pass'):
            continue
        a, c = pe['I'], r['data'][k]['sub']['I']
        log("  %-5s %-2s %14.8e %14.8e %12.2e %14.8e"
            % (R, b, a, c, abs(c - a) / a, r['data'][k]['exact']['I']))
