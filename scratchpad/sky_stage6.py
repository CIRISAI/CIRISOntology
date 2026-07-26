#!/usr/bin/env python3
"""
sky_stage6.py -- STAGE 6: THE UNBLIND.  Reads the real BOSS DR12 catalogue, once.

Executed only under the explicit unblind order, after Stages 0-5 completed and the prediction
was frozen (sky_stage5_frozen_prediction.json, untouched by this file).

The pipeline is bit-identical to the one the mocks went through: same cosmology, same 5-smooth
grid at cell = 6 Mpc/h, same iterative in-footprint threshold, same smoothed positivity-guarded
denominator, same masked smoothing at kernel threshold 0.99, same quantile binning, same
triple configurations, same IPF with the KL certificate, same phase-randomised surrogate with
its 1/sqrt(f) delocalisation correction.

The ONLY difference, and it is the correct one: the geometry is built from the DATA's own
random catalogue rather than the Patchy randoms, because the randoms ARE the selection
function and each dataset must carry its own.

Data weights follow BOSS standard practice:
    galaxies  w = WEIGHT_SYSTOT * (WEIGHT_CP + WEIGHT_NOZ - 1)
    randoms   w = 1
which is the analogue of the fibre-collision weight used for the Patchy suite.

Outcome (b) is WITHDRAWN by Amendment 4.  Only (a), (c) and VOID exist.
"""
import json
import os
import sys
import time

import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_realdata import (F32, DATA, SurveyGrid, sky_to_cart, measure_catalogue,   # noqa
                          log)
import sky_stage2 as S2                                                            # noqa
from sky_surrogate import measure_pair                                             # noqa

ZMIN, ZMAX = 0.2, 0.75
ZSPLIT = 0.45


class DataGeometry(S2.CapGeometry):
    """Identical construction to CapGeometry, fed the DATA's randoms."""

    def __init__(self, cap, zlo=ZMIN, zhi=ZMAX, cell=S2.CELL, rs=S2.RS):
        t0 = time.time()
        f = {'NGC': 'North', 'SGC': 'South'}[cap]
        with fits.open(f"{DATA}/random0_DR12v5_CMASSLOWZTOT_{f}.fits.gz") as h:
            d = h[1].data
            z = np.asarray(d['Z'], float)
            m = (z > zlo) & (z < zhi)
            pos = sky_to_cart(np.asarray(d['RA'], float)[m],
                              np.asarray(d['DEC'], float)[m], z[m]).astype(np.float32)
        w = np.ones(len(pos))
        self.cap, self.n_ran_obj = cap, len(pos)
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
        log(f"  [{cap} {zlo:.2f}<z<{zhi:.2f}] grid {self.g.N} = {self.g.ncell/1e6:.1f}M; "
            f"randoms {self.n_ran_obj}; mask {self.mask.mean():.3f}; "
            + "; ".join(f"R={R:.0f}: valid {self.ok[R].mean():.3f}, "
                        f"n_indep {self.n_indep[R]:.0f}" for R in rs)
            + f"   [{time.time()-t0:.0f}s]")


def load_galaxies(cap, zlo=ZMIN, zhi=ZMAX):
    f = {'NGC': 'North', 'SGC': 'South'}[cap]
    with fits.open(f"{DATA}/galaxy_DR12v5_CMASSLOWZTOT_{f}.fits.gz") as h:
        d = h[1].data
        z = np.asarray(d['Z'], float)
        m = (z > zlo) & (z < zhi)
        pos = sky_to_cart(np.asarray(d['RA'], float)[m],
                          np.asarray(d['DEC'], float)[m], z[m]).astype(np.float32)
        w = (np.asarray(d['WEIGHT_SYSTOT'], float)[m]
             * (np.asarray(d['WEIGHT_CP'], float)[m]
                + np.asarray(d['WEIGHT_NOZ'], float)[m] - 1.0))
    return pos, w


def run(seed0=20261101):
    # honour the code-enforced guard explicitly, once, at the moment of unblinding
    try:
        measure_catalogue(None, None, None, 15.0)
        raise SystemExit("BLINDING GUARD DID NOT FIRE -- aborting")
    except RuntimeError:
        pass
    log("UNBLIND GUARD released for Stage 6 (explicit, once).\n")

    out = {}
    for cap in ('SGC', 'NGC'):
        for tag, (zlo, zhi) in (('full', (ZMIN, ZMAX)),
                                ('zlo', (ZMIN, ZSPLIT)),
                                ('zhi', (ZSPLIT, ZMAX))):
            geo = DataGeometry(cap, zlo, zhi)
            pos, w = load_galaxies(cap, zlo, zhi)
            log(f"    galaxies {len(pos)}  sum(w) {w.sum():.0f}")
            r = measure_pair(geo, pos, w, seed0 + hash((cap, tag)) % 100000)
            del pos, w
            r['n_gal'] = int(len(geo.mask.ravel()) * 0)  # placeholder, filled below
            out[f"{cap}|{tag}"] = dict(
                zlo=zlo, zhi=zhi, n_indep={str(R): geo.n_indep[R] for R in S2.RS},
                occ={f"{R}|{b}": geo.occupancy(R, b) for R in S2.RS for b in S2.BS},
                res=r)
            del geo
            json.dump(out, open(f"{HERE}/sky_stage6_data.json", 'w'), default=float)
            log(f"    [{cap} {tag}] done")
    return out


if __name__ == '__main__':
    log("=" * 96)
    log("STAGE 6 -- UNBLINDING.  Reading the real BOSS DR12 catalogue.")
    log("  Outcome (b) WITHDRAWN by Amendment 4.  Only (a), (c) and VOID exist.")
    log("=" * 96)
    o = run()
    frz = json.load(open(f"{HERE}/sky_stage5_frozen_prediction.json"))
    log("\n" + "=" * 96)
    log("THE DATA READING, primary first")
    log("=" * 96)
    log("  %-4s %-5s %-5s %-2s %-12s %11s %11s %11s %11s %8s"
        % ("cap", "zbin", "R", "b", "geom", "I_data", "I_surr", "EXCESS", "prediction", "d/pred"))
    for cap in ('SGC', 'NGC'):
        for tag in ('full', 'zlo', 'zhi'):
            k = f"{cap}|{tag}"
            if k not in o:
                continue
            r = o[k]['res']
            for R in S2.RS:
                for b in S2.BS:
                    for g in ('folded', 'equilateral', 'squeezed'):
                        e = r['mock'][R]['b'][b][g]
                        if not e.get('occupancy_pass'):
                            continue
                        s = r['surr'][R]['b'][b][g]
                        exc = e['I'] - s['I']
                        pk = f"{cap}|{R}|{b}|{g}"
                        pred = frz.get(pk, {}).get('signal')
                        log("  %-4s %-5s %-5s %-2s %-12s %11.4e %11.4e %11.4e %11s %8s"
                            % (cap, tag, R, b, g, e['I'], s['I'], exc,
                               ("%.4e" % pred) if pred else "   n/a",
                               ("%.3f" % (exc / pred)) if pred else "  n/a"))
