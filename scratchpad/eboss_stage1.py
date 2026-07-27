#!/usr/bin/env python3
"""
eboss_stage1.py -- STAGE 1: pipeline adaptation to eBOSS DR16, and its validation.

Per EBOSS_PREREG.md section 11, new code is confined to eBOSS I/O and geometry.  The estimator,
grid, interlaced CIC, masked smoothing, quantile binning, connected_info, LP pinning and the
configurations are IMPORTED UNCHANGED from sky_realdata.py / sky_stage2.py -- rewriting them
would forfeit the validation they already carry (refuter A5 agreed with an independent
reimplementation to 9e-13 relative).

BLINDING.  This file builds geometry from the eBOSS RANDOM catalogues and measures
  (a) the split-randoms null, which carries the survey geometry and by construction NO
      clustering -- the Stage-1 validation field, and
  (b) EZmock realisations, which are mocks.
It NEVER reads the order-3 statistic of the eBOSS galaxy catalogue: that path goes through
sky_realdata.measure_catalogue, which raises without stage6_unblind=True, and additionally
through bgs_gates.require_discharged at Stage 6.

Writes eboss_stage1_<TRACER>_<CAP>.json.
"""
import json
import os
import sys
import time

import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_realdata import F32, SurveyGrid, sky_to_cart, log            # noqa: E402
import sky_stage2 as S2                                               # noqa: E402

DATA = os.environ.get('SKYDATA', '/home/emoore/skydata')
EB, EZ = f"{DATA}/eboss", f"{DATA}/eboss/ez"

# EBOSS_PREREG section 7.2/7.3: the ladder is b in {4,6} and the scales are fixed per arm.
ZR = {'LRG': (0.6, 1.0), 'ELG': (0.6, 1.1), 'QSO': (0.8, 2.2)}
ARM_R = {'LRG': [15.0, 10.0], 'ELG': [10.0, 15.0]}     # first entry is that arm's primary
BS = [4, 6]

# The standard eBOSS weight, and it is the SAME expression BOSS used -- WEIGHT_NOZ is continuous
# in eBOSS rather than an integer upweight, which changes the value but not the formula.
def wstd(d, idx):
    return (np.asarray(d['WEIGHT_SYSTOT'], float)[idx]
            * (np.asarray(d['WEIGHT_CP'], float)[idx]
               + np.asarray(d['WEIGHT_NOZ'], float)[idx] - 1.0))


def read_cat(path, zlo, zhi, weights=True, patch=None):
    """Positions and weights from an eBOSS-format FITS catalogue (data, random or EZmock)."""
    with fits.open(path, memmap=True) as h:
        d = h[1].data
        names = set(h[1].columns.names)
        z = np.asarray(d['Z'], float)
        m = (z > zlo) & (z < zhi)
        if patch is not None and 'chunk' in names:
            ch = np.asarray(d['chunk'])
            m &= np.array([str(c).strip().strip("b'") == patch for c in ch])
        idx = np.nonzero(m)[0]
        pos = sky_to_cart(np.asarray(d['RA'], float)[idx],
                          np.asarray(d['DEC'], float)[idx], z[idx]).astype(np.float32)
        if weights and {'WEIGHT_SYSTOT', 'WEIGHT_CP', 'WEIGHT_NOZ'} <= names:
            w = wstd(d, idx)
        else:
            w = np.ones(len(idx))
    return pos, w.astype(np.float64)


class EbossGeometry(S2.CapGeometry):
    """CapGeometry fed the eBOSS randoms.  Every constant and every step below the read is
    S2's, unchanged: the iterative in-footprint threshold, the 8 Mpc/h smoothed random field as
    the footprint definition (Amendment 2 A2.2), the smoothed positivity-guarded denominator,
    and DEN_THR = 0.99 (the Stage-1 finding that 0.5 inflates a shot-noise null by 6.6x)."""

    def __init__(self, tracer, cap, rs, cell=S2.CELL, patch=None, ran_path=None):
        t0 = time.time()
        zlo, zhi = ZR[tracer]
        p = ran_path or f"{EB}/eBOSS_{tracer}_clustering_random-{cap}-vDR16.fits"
        pos, w = read_cat(p, zlo, zhi, weights=False, patch=patch)
        self.cap = f"{tracer}|{cap}" + (f"|{patch}" if patch else "")
        self.tracer, self.capname, self.patch = tracer, cap, patch
        self.n_ran_obj = len(pos)
        self.g = SurveyGrid(pos, cell=cell)
        self.n_ran = self.g.deposit(pos, w)
        del pos, w
        exp0 = self.g.smooth_k(self.g.fwd(self.n_ran), S2.MASK_SMOOTH)
        t = float(exp0.mean())
        for _ in range(6):
            t = float(exp0[exp0 > 0.5 * t].mean())
        self.nbar_cell = t
        self.mask = (exp0 > S2.MASK_FRAC * t)
        self.exp_ran = np.maximum(exp0, 1e-12).astype(F32)
        del exp0
        self.m32 = self.mask.astype(F32)
        self.den, self.ok, self.n_indep = {}, {}, {}
        Fm = self.g.fwd(self.m32)
        for R in rs:
            d_ = self.g.smooth_k(Fm, R)
            o = d_ > S2.DEN_THR
            self.den[R], self.ok[R] = d_, o
            self.n_indep[R] = float(o.sum()) * cell ** 3 / ((2 * np.pi) ** 1.5 * R ** 3)
        del Fm
        self.tot_ran = float(self.exp_ran.sum())
        self.build_s = time.time() - t0
        log(f"  [{self.cap}] grid {self.g.N} = {self.g.ncell/1e6:.1f}M cells; randoms "
            f"{self.n_ran_obj}; mask {self.mask.mean():.4f}; nbar_cell {self.nbar_cell:.3f}; "
            + "; ".join(f"R={R:.0f}: valid {self.ok[R].mean():.4f}, n_indep {self.n_indep[R]:.0f}"
                        for R in rs) + f"   [{self.build_s:.0f}s]")


def split_randoms_null(geo, seed=7):
    """THE STAGE-1 VALIDATION FIELD.  Split the randoms in half; treat one half as 'galaxies'.

    The result carries the survey window, the selection function and the shot noise, and BY
    CONSTRUCTION carries no clustering.  Whatever I_C^(3) it reads is manufactured by the
    pipeline -- so it is simultaneously the G5-analogue pipeline-error control and a direct
    measurement of the valve/window floor at this geometry.  It needs no mock and no model.
    """
    zlo, zhi = ZR[geo.tracer]
    p = f"{EB}/eBOSS_{geo.tracer}_clustering_random-{geo.capname}-vDR16.fits"
    pos, w = read_cat(p, zlo, zhi, weights=False, patch=geo.patch)
    rng = np.random.default_rng(seed)
    half = rng.random(len(pos)) < 0.5
    # Scale the "galaxy" half down to the real galaxy count so the SHOT NOISE is right: a
    # half-random sample has ~25x the galaxy density and would read a floor 25x too small.
    with fits.open(f"{EB}/eBOSS_{geo.tracer}_clustering_data-{geo.capname}-vDR16.fits") as h:
        zz = np.asarray(h[1].data['Z'], float)
        n_gal = int(((zz > zlo) & (zz < zhi)).sum())
    if geo.patch:
        n_gal = int(n_gal * geo.n_ran_obj / len(pos) * 2)
    idx = np.nonzero(half)[0]
    keep = rng.choice(idx, size=min(n_gal, idx.size), replace=False)
    return geo.measure(pos[keep], w[keep], bs=BS, rs=list(geo.ok.keys()))


def gate_A_sigma(res, lo=0.02, hi=2.0):
    """Gate A, sigma sanity (sky_artifact_gates), whose dye test on the withdrawn BOSS run read
    [40.96, 1548.23] against this band.  Carried over unchanged."""
    s = [rec['sigma'] for rec in res.values()]
    return dict(sigma_min=min(s), sigma_max=max(s), pass_=bool(lo <= min(s) and max(s) <= hi))


def run(tracer, cap, patch=None):
    rs = ARM_R[tracer]
    geo = EbossGeometry(tracer, cap, rs, patch=patch)
    out = dict(tracer=tracer, cap=cap, patch=patch, cell=S2.CELL, rs=rs, bs=BS,
               den_thr=S2.DEN_THR, mask_frac=S2.MASK_FRAC, mask_smooth=S2.MASK_SMOOTH,
               grid=list(geo.g.N), ncell=geo.g.ncell, n_ran_obj=geo.n_ran_obj,
               mask_frac_measured=float(geo.mask.mean()), nbar_cell=geo.nbar_cell,
               build_s=geo.build_s,
               n_indep={str(R): geo.n_indep[R] for R in rs},
               frac_valid={str(R): float(geo.ok[R].mean()) for R in rs},
               occupancy={f"{R}|{b}": geo.occupancy(R, b) for R in rs for b in BS})

    t0 = time.time()
    sr = split_randoms_null(geo)
    out['split_randoms_null'] = sr
    out['split_randoms_s'] = time.time() - t0
    out['gate_A'] = gate_A_sigma(sr)

    # G9 (IPF certificate) and the occupancy verdict, per row.
    cert, occfail = [], []
    for R, rec in sr.items():
        for b, bb in rec['b'].items():
            for geom, e in bb.items():
                if not e.get('occupancy_pass'):
                    occfail.append(f"R={R} b={b} {geom} occ={e['occupancy']:.0f}")
                    continue
                cert.append(e['cert'])
    out['G9_cert_max'] = max(cert) if cert else None
    out['G9_cert_pass'] = bool(cert and max(cert) < 1e-9)
    out['occupancy_failures'] = occfail

    # A mock realisation through the identical path -- the first thing with clustering in it,
    # and the check that the mock reads ABOVE the geometry-only floor.
    mp = f"{EZ}/EZmock_realistic_eBOSS_{tracer}_{cap}_v7_0001.dat.fits.gz"
    if os.path.exists(mp) and patch is None:
        zlo, zhi = ZR[tracer]
        pos, w = read_cat(mp, zlo, zhi)
        t0 = time.time()
        out['mock_0001'] = geo.measure(pos, w, bs=BS, rs=rs)
        out['mock_s'] = time.time() - t0
        out['n_mock_gal'] = len(pos)
        del pos, w

    p = f"{HERE}/eboss_stage1_{tracer}_{cap}" + (f"_{patch}" if patch else "") + ".json"
    json.dump(out, open(p, 'w'), default=float, indent=1)
    log(f"  wrote {os.path.basename(p)}")
    return out


if __name__ == '__main__':
    tracer = sys.argv[1] if len(sys.argv) > 1 else 'ELG'
    cap = sys.argv[2] if len(sys.argv) > 2 else 'NGC'
    patch = sys.argv[3] if len(sys.argv) > 3 else None
    log("=" * 100)
    log(f"eBOSS STAGE 1 -- pipeline adaptation.  tracer={tracer} cap={cap} patch={patch}")
    log("  BLINDED: the galaxy catalogue's order-3 statistic is not read here.")
    log("=" * 100)
    o = run(tracer, cap, patch)
    log("")
    log(f"  Gate A (sigma sanity)   : {o['gate_A']}")
    log(f"  G9 IPF certificate max  : {o['G9_cert_max']}  pass={o['G9_cert_pass']}")
    log(f"  occupancy failures      : {o['occupancy_failures'] or 'none'}")
    log("")
    log(f"  {'R':>4s} {'b':>2s} {'geom':12s} {'I(split-randoms)':>17s} {'I(mock 0001)':>14s}"
        f" {'mock-floor':>12s}")
    for R in o['rs']:
        for b in BS:
            for geom in ('folded', 'equilateral', 'squeezed'):
                e = o['split_randoms_null'][R]['b'][b][geom]
                if not e.get('occupancy_pass'):
                    continue
                mm = o.get('mock_0001', {}).get(R, {}).get('b', {}).get(b, {}).get(geom)
                mi = mm['I'] if mm and mm.get('occupancy_pass') else None
                log(f"  {R:4.0f} {b:2d} {geom:12s} {e['I']:17.6e} "
                    f"{(mi if mi is not None else float('nan')):14.6e} "
                    f"{((mi - e['I']) if mi is not None else float('nan')):12.4e}")
