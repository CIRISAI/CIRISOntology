#!/usr/bin/env python3
"""
refuter_nulls.py -- ATTACKS A9 (null not two-point matched), A1 (non-Poisson stochasticity)
and A6 (pointwise-channel worst case), on the real BOSS DR12 field.

Post-unblind, post-hoc, adversarial.  Pre-registered in REFUTER_PREREG.md before any of this
was run.

The pipeline's Amendment-5 null N2 is built as
    dpr  = phase-randomise(delta_data) / sqrt(fmask) * mask        [keeps |F| of delta_data]
    lam  = alpha * exp_ran * max(1 + dpr, 0)                       [CLIPS 37% of cells]
    n    ~ Poisson(lam)
and delta_data ALREADY carries the survey's shot-noise power, so N2 ends up with
  (i)  a modulation whose large-scale amplitude has been damped by the clipping,
  (ii) a mean modulation of ~1.76 rather than 1, hence ~1.76x the data's number density and
       LESS shot noise per cell than the data has, and
  (iii) a second, independent, full-amplitude Poisson noise on top of the first.

This file builds the null family that isolates each of those:

  N2      pipeline's own null, reproduced bit-for-bit from the recorded seeds (integrity check)
  N2m     POWER-MATCHED: the modulation is the shot-noise-DECONVOLVED field, so that after
          resampling the total power returns to the data's; mean renormalised to 1
  N2mw    N2m, sampled with the data's own WEIGHTED shot noise  (kappa = <w^2>/<w>)
  N2eps   N2m, sampled negative-binomial at Var = lam*(1+eps)     [A1 dispersion sweep]
  N2L     N2m's clustering field pushed through a LOGNORMAL instead of a clip -- deliberately
          over-generous, because a per-cell monotone map does not commute with smoothing and
          therefore manufactures real order-3 structure.  An upper bound, not a fair null.

A9a additionally measures the BINMINT PEDESTAL (fine b'=2b pair-maxent merged to b) on the
data and on each null: the part of the reading that is a pure function of pair structure.
If the null's pedestal is below the data's, that difference is counted as signal by the
campaign's target.

Estimator code is deliberately UNCHANGED from the pipeline here -- the estimator is attacked
separately in refuter_a5.py.  What is under attack in this file is the NULL.
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_realdata import F32, quantile_labels, connected_info, configs, log   # noqa: E402
import sky_stage2 as S2                                                       # noqa: E402
from sky_stage6 import DataGeometry, load_galaxies, ZMIN, ZMAX                # noqa: E402
from sky_stage7 import read_field, poisson_resample, measure                  # noqa: E402
from sky_surrogate import phase_randomise                                     # noqa: E402
from sky_stage4 import hist_at                                                # noqa: E402
from sky_pilot import pairwise_maxent                                         # noqa: E402
from astropy.io import fits                                                   # noqa: E402

PRIMARY = [(15.0, 4), (15.0, 6), (10.0, 4), (10.0, 6), (10.0, 8)]
SEED0 = 20261201            # the pipeline's own Stage-7 seed, for the reproduction check
RSEED = 77001               # refuter seeds, disjoint from every pipeline seed


# ------------------------------------------------------------------ weight statistics
def weight_moments(cap, zlo=ZMIN, zhi=ZMAX):
    """kappa = <w^2>/<w> is EXACTLY the factor by which the data's weighted counts are
    super-Poisson relative to the null's unweighted Poisson draw at the same mean."""
    f = {'NGC': 'North', 'SGC': 'South'}[cap]
    with fits.open(f"{S2.DATA}/galaxy_DR12v5_CMASSLOWZTOT_{f}.fits.gz") as h:
        d = h[1].data
        z = np.asarray(d['Z'], float)
        m = (z > zlo) & (z < zhi)
        systot = np.asarray(d['WEIGHT_SYSTOT'], float)[m]
        cp = np.asarray(d['WEIGHT_CP'], float)[m]
        noz = np.asarray(d['WEIGHT_NOZ'], float)[m]
        fkp = np.asarray(d['WEIGHT_FKP'], float)[m]
    out = {}
    for name, w in (('standard', systot * (cp + noz - 1.0)),
                    ('none', np.ones(m.sum())),
                    ('no_systot', cp + noz - 1.0),
                    ('systot_only', systot),
                    ('standard_fkp', systot * (cp + noz - 1.0) * fkp)):
        out[name] = dict(n=int(w.size), mean=float(w.mean()),
                         m2=float((w * w).mean()),
                         kappa=float((w * w).mean() / w.mean()),
                         eps=float((w * w).mean() / w.mean() - 1.0))
    return out


# ------------------------------------------------------------------ shell-averaged spectra
def shell_index(g, nbin=256):
    k = np.sqrt(g.k2)
    kmax = float(k.max())
    idx = np.minimum((k / kmax * nbin).astype(np.int32), nbin - 1)
    cnt = np.bincount(idx.ravel(), minlength=nbin).astype(np.float64)
    return idx, cnt, nbin


def shell_power(g, F, idx, cnt, nbin):
    p = (F.real.astype(np.float64) ** 2 + F.imag.astype(np.float64) ** 2)
    s = np.bincount(idx.ravel(), weights=p.ravel(), minlength=nbin)
    del p
    return s / np.maximum(cnt, 1)


def noise_power(geo, alpha, kappa, idx, cnt, nbin, seed, ndraw=3):
    """Shell-averaged power of a pure shot-noise realisation on this geometry: per-cell
    variance of delta from weighted counts is kappa/(alpha*exp_ran)."""
    rng = np.random.default_rng(seed)
    v = np.zeros_like(geo.exp_ran)
    np.divide(kappa, alpha * geo.exp_ran, out=v, where=geo.mask)
    sd = np.sqrt(v).astype(F32)
    del v
    acc = np.zeros(nbin)
    for _ in range(ndraw):
        nu = (rng.standard_normal(geo.mask.shape, dtype=np.float32) * sd) * geo.m32
        acc += shell_power(geo.g, geo.g.fwd(nu), idx, cnt, nbin)
        del nu
    del sd
    return acc / ndraw


# ------------------------------------------------------------------ matched modulation
def matched_clustering_field(geo, dm, alpha, kappa, seed, ndraw=3):
    """Phase-random field whose per-mode amplitude is the data's with the shot-noise power
    REMOVED, so that re-sampling puts it back and the total returns to the data's."""
    g = geo.g
    idx, cnt, nbin = shell_index(g)
    F = g.fwd(dm)
    S = shell_power(g, F, idx, cnt, nbin)
    N = noise_power(geo, alpha, kappa, idx, cnt, nbin, seed + 5, ndraw=ndraw)
    r = np.clip(1.0 - N / np.maximum(S, 1e-30), 0.0, 1.0)
    rng = np.random.default_rng(seed)
    ph = np.exp(1j * rng.uniform(0.0, 2.0 * np.pi, F.shape)).astype(np.complex64)
    amp = (np.abs(F) * np.sqrt(r[idx]).astype(np.float32)).astype(np.float32)
    del F
    Fn = (amp * ph).astype(np.complex64)
    del amp, ph
    Fn[0, 0, 0] = abs(Fn[0, 0, 0])
    fm = float(geo.m32.mean())
    out = ((g.inv(Fn).astype(F32) / np.sqrt(fm)) * geo.m32).astype(F32)
    del Fn
    frac_kept = float(np.average(r, weights=cnt))
    return out, dict(frac_power_kept=frac_kept, nbin=nbin)


# ------------------------------------------------------------------ samplers
def _finish(geo, n, alpha):
    exp = alpha * geo.exp_ran
    d = np.zeros_like(n)
    np.divide(n - exp, exp, out=d, where=geo.mask)
    del n, exp
    return (d * geo.m32).astype(F32)


def sample_null(geo, mod, alpha, seed, mode='poisson', eps=0.0, kappa=1.0,
                renorm=True):
    """mod is the modulation 1+delta_clustering (already clipped/positive).  Draw counts with
    mean alpha*exp_ran*mod and the requested stochasticity."""
    m = mod
    if renorm:
        # weight by exp_ran so that sum(lambda) matches the data's total weighted count
        # EXACTLY, not just on a cell-count average
        mu = float((geo.exp_ran * m)[geo.mask].sum() / geo.exp_ran[geo.mask].sum())
        m = (m / mu).astype(F32)
    lam = (alpha * geo.exp_ran * m).astype(np.float64)
    rng = np.random.default_rng(seed)
    if mode == 'poisson':
        n = rng.poisson(lam).astype(F32)
    elif mode == 'clumped':                     # Var = kappa*lam, the weighted-count model
        n = (kappa * rng.poisson(lam / kappa)).astype(F32)
    elif mode == 'nb':                          # Var = lam*(1+eps), gamma-Poisson (Patchy's)
        nn = np.maximum(lam / max(eps, 1e-12), 1e-9)
        n = rng.negative_binomial(nn, 1.0 / (1.0 + eps)).astype(F32)
        del nn
    else:
        raise ValueError(mode)
    del lam
    return _finish(geo, n, alpha)


def clip_mod(field):
    c = float(((1.0 + field) < 0.0).mean())
    return np.maximum(1.0 + field, 0.0).astype(F32), c


def lognormal_mod(field, mask):
    """Positivity WITHOUT clipping: m = exp(s*g - s^2 var/2), s chosen so Var(m) = Var(g).
    Deliberately over-generous -- a per-cell monotone map before smoothing manufactures
    order-3 structure, which is precisely the defect that killed the Stage 3 control."""
    v = float(field[mask].var())
    s2 = np.log1p(v) / max(v, 1e-12)
    s = np.sqrt(s2)
    m = np.exp(s * field - 0.5 * s2 * v).astype(F32)
    return m, dict(sigma_g2=v, s=float(s), clipped=0.0)


# ------------------------------------------------------------------ A9a: binmint pedestal
def smoothed(geo, fld, R):
    F = geo.g.fwd(fld)
    num = geo.g.smooth_k(F, R)
    del F
    ok = geo.ok[R]
    sm = np.zeros_like(num)
    np.divide(num, geo.den[R], out=sm, where=ok)
    del num
    return sm, ok


def pedestal(geo, fld, rows=PRIMARY, geoms=('folded',)):
    """The part of I_C^(3) that a state carrying only the FINE (b'=2b) pair marginals already
    produces once it is coarse-grained to b.  A pure function of pair structure."""
    out = {}
    for R in sorted({r for r, _ in rows}, reverse=True):
        sm, ok = smoothed(geo, fld, R)
        stride = max(1, int(round(R / geo.g.cell / 3)))
        for (RR, b) in rows:
            if RR != R:
                continue
            bp = 2 * b
            if geo.occupancy(R, b) <= S2.OCC_MIN or geo.occupancy(R, bp) <= 20:
                continue
            for gm in geoms:
                hf, _ = hist_at(geo, sm, ok, bp, R, gm, stride)
                pf = hf / hf.sum()
                q, err, _ = pairwise_maxent(pf, iters=20000, tol=1e-13)
                fac = bp // b
                qa = q.reshape(b, fac, b, fac, b, fac).sum(axis=(1, 3, 5))
                ha, _ = hist_at(geo, sm, ok, b, R, gm, stride)
                out[f"{R}|{b}|{gm}"] = dict(
                    I=connected_info(ha)['I'],
                    pedestal=connected_info(qa / qa.sum())['I'], ipf_err=float(err))
                del hf, pf, q, qa, ha
        del sm
    return out


# ------------------------------------------------------------------ driver
def run(cap, n_null=4, eps_grid=(0.1, 0.25, 0.5, 1.0, 2.0, 4.0), out=None):
    t0 = time.time()
    wm = weight_moments(cap)
    kappa = wm['standard']['kappa']
    log(f"  [{cap}] weight moments: <w>={wm['standard']['mean']:.4f} "
        f"<w^2>={wm['standard']['m2']:.4f}  kappa=<w^2>/<w>={kappa:.4f}  "
        f"=> the data's counts are {100*(kappa-1):.1f}% super-Poisson relative to the null")

    geo = DataGeometry(cap, ZMIN, ZMAX)
    pos, w = load_galaxies(cap, ZMIN, ZMAX)
    dm, alpha = read_field(geo, pos, w)
    del pos, w
    res = dict(cap=cap, weights=wm, alpha=float(alpha), kappa=kappa)

    log(f"  [{cap}] measuring the data ...")
    res['data'] = measure(geo, dm)
    res['data_pedestal'] = pedestal(geo, dm)
    log(f"    data sigma R=15 {res['data'][15.0]['sigma']:.4f}  "
        f"skew {res['data'][15.0]['skew']:+.4f}   [{time.time()-t0:.0f}s]")

    # ---- integrity: reproduce the pipeline's own N2, seed for seed
    fm = float(geo.m32.mean())
    dpr0 = (phase_randomise(geo.g, dm, SEED0 + 0) / np.sqrt(fm)) * geo.m32
    # THE DIAGNOSTIC THAT PINS THE MECHANISM.  The pipeline's null modulates by
    # max(1+dpr, 0) and never renormalises it.  dpr is a phase-randomised copy of the data's
    # own cell-level delta, whose rms is ~3 (0.058 galaxies per 6 Mpc/h cell), so clipping a
    # zero-mean field of that width at -1 leaves a mean well above 1 -- and the null is then
    # sampled at that inflated density, with correspondingly LESS shot noise than the data.
    mod_pipe = np.maximum(1.0 + dpr0, 0.0)
    mean_cell = float(mod_pipe[geo.mask].mean())
    mean_wt = float((geo.exp_ran * mod_pipe)[geo.mask].sum() / geo.exp_ran[geo.mask].sum())
    del mod_pipe
    n2_0, cl0 = poisson_resample(geo, dpr0, alpha, SEED0 + 3)
    res['repro_N1'] = measure(geo, dpr0)
    res['repro_N2'] = measure(geo, n2_0)
    res['repro_N2_pedestal'] = pedestal(geo, n2_0)
    res['repro_clipped'] = cl0
    res['pipeline_null_density'] = dict(mean_mod_cell=mean_cell, mean_mod_weighted=mean_wt,
                                        clipped=cl0)
    log(f"    reproduced pipeline N1/N2 (seed {SEED0}) clipped={cl0:.4f} "
        f"sigma(N2,R=15)={res['repro_N2'][15.0]['sigma']:.4f}")
    log(f"    *** pipeline null mean modulation = {mean_cell:.4f} (cell) / {mean_wt:.4f} "
        f"(density-weighted): the null is sampled at {mean_wt:.2f}x the data's number "
        f"density, so it carries only {1/mean_wt:.2f}x the data's shot noise "
        f"[{time.time()-t0:.0f}s]")
    del dpr0, n2_0

    # ---- the matched clustering field
    fam = {}
    ped = {}
    for i in range(n_null):
        cf, info = matched_clustering_field(geo, dm, alpha, kappa, RSEED + 101 * i)
        mod, clipped = clip_mod(cf)
        mu = float(mod[geo.mask].mean())
        if i == 0:
            res['matched_info'] = dict(info, clipped=clipped, mean_mod=mu,
                                       sigma_cf=float(cf[geo.mask].std()))
            log(f"    matched modulation: power kept {info['frac_power_kept']:.4f}, "
                f"cell sigma {float(cf[geo.mask].std()):.3f}, clipped {clipped:.4f}, "
                f"mean {mu:.4f}")
        variants = [('N2m', dict(mode='poisson')),
                    ('N2mw', dict(mode='clumped', kappa=kappa))]
        if i < 2:
            variants += [(f'N2eps{e:g}', dict(mode='nb', eps=e)) for e in eps_grid]
        for name, kw in variants:
            fld = sample_null(geo, mod, alpha, RSEED + 977 * i + 13, **kw)
            fam.setdefault(name, []).append(measure(geo, fld))
            if i == 0 and name in ('N2m', 'N2mw'):
                ped[name] = pedestal(geo, fld)
            del fld
        # over-generous lognormal probe (A6)
        lm, linfo = lognormal_mod(cf, geo.mask)
        if i == 0:
            res['lognormal_info'] = linfo
        fldL = sample_null(geo, lm, alpha, RSEED + 977 * i + 29, mode='clumped', kappa=kappa)
        fam.setdefault('N2L', []).append(measure(geo, fldL))
        if i == 0:
            ped['N2L'] = pedestal(geo, fldL)
        del fldL, lm, mod, cf
        log(f"    null family draw {i+1}/{n_null} done   [{time.time()-t0:.0f}s]")
        res['family'] = fam
        res['family_pedestal'] = ped
        if out:
            json.dump(res, open(out, 'w'), default=float)
    del geo, dm
    return res


def run_mock(cap, n_mock=3, out=None):
    """CLOSURE.  The same correction applied on the MOCK side, so the verdict can say whether
    the null's defect is common-mode -- in which case the prediction moves with the target and
    the consistency test is untouched -- or data-specific."""
    import tarfile
    from sky_realdata import sky_to_cart
    geo = S2.CapGeometry(cap)
    kappa = weight_moments(cap)['standard']['kappa']
    tf = tarfile.open(f"{S2.DATA}/Patchy-Mocks-DR12{cap}-COMPSAM_V6C.tar.gz", 'r|gz')
    fm = float(geo.m32.mean())
    res, t0 = [], time.time()
    for i, m in enumerate(tf):
        if i >= n_mock:
            break
        raw = tf.extractfile(m).read()
        a = S2._load_ascii(raw, 8); del raw
        sel = a[:, 6] > 0.5
        pos = sky_to_cart(a[sel, 0], a[sel, 1], a[sel, 2]).astype(np.float32)
        wt = a[sel, 7].astype(np.float64); del a
        dm, alpha = read_field(geo, pos, wt); del pos, wt
        rec = dict(mock=measure(geo, dm))
        dpr = (phase_randomise(geo.g, dm, SEED0 + 17 * i) / np.sqrt(fm)) * geo.m32
        d2, cl = poisson_resample(geo, dpr, alpha, SEED0 + 991 * i + 3)
        del dpr
        rec['n2_pipeline'] = measure(geo, d2); rec['clipped'] = cl
        del d2
        cf, info = matched_clustering_field(geo, dm, alpha, kappa, RSEED + 101 * i)
        mod, clipped = clip_mod(cf)
        rec['matched_info'] = dict(info, clipped=clipped)
        for name, kw in (('n2m', dict(mode='poisson')),
                         ('n2mw', dict(mode='clumped', kappa=kappa))):
            fld = sample_null(geo, mod, alpha, RSEED + 977 * i + 13, **kw)
            rec[name] = measure(geo, fld)
            del fld
        del cf, mod, dm
        res.append(rec)
        log(f"    [{cap}] mock {i+1}/{n_mock} done  [{time.time()-t0:.0f}s]")
        if out:
            json.dump(dict(cap=cap, kappa=kappa, res=res), open(out, 'w'), default=float)
    tf.close()
    del geo
    return res


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'mock':
        cap = sys.argv[2]
        nm = int(sys.argv[3]) if len(sys.argv) > 3 else 3
        log("=" * 96)
        log(f"REFUTER A9 CLOSURE on MOCKS  cap={cap}  n_mock={nm}   (post-unblind, post-hoc)")
        log("=" * 96)
        run_mock(cap, nm, out=f"{HERE}/refuter_mock_{cap}.json")
        sys.exit(0)
    cap = sys.argv[1] if len(sys.argv) > 1 else 'SGC'
    nn = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    op = f"{HERE}/refuter_nulls_{cap}.json"
    log("=" * 96)
    log(f"REFUTER A9 / A1 / A6  --  cap={cap}  n_null={nn}   (post-unblind, post-hoc)")
    log("=" * 96)
    r = run(cap, nn, out=op)
    json.dump(r, open(op, 'w'), default=float)
    log(f"\n  written {op}")
