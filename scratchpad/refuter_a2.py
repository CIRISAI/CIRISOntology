#!/usr/bin/env python3
"""
refuter_a2.py -- ATTACK A2: the systematic-weight variation the pre-registration required
(SKY_REALDATA_PREREG.md section 7.5) and that Stage 6 did not run.

  "Imaging systematics and completeness weights: MARGINALISED, with the analysis repeated
   under the published weight variants; a shift exceeding the statistical error between weight
   schemes VOIDS the affected bin."

sky_stage6.py applies exactly one scheme.  This file runs the variants.

Everything else is held bit-identical to the pipeline: the same geometry, the same null
construction, and the SAME null seeds across variants, so the comparison is paired and the
phase-random realisation noise largely cancels between schemes.

Post-unblind, post-hoc.  Pre-registered in REFUTER_PREREG.md.
"""
import json
import os
import sys
import time

import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_realdata import F32, sky_to_cart, log                                # noqa: E402
import sky_stage2 as S2                                                       # noqa: E402
from sky_stage6 import DataGeometry, ZMIN, ZMAX                               # noqa: E402
from sky_stage7 import read_field, poisson_resample, measure                  # noqa: E402
from sky_surrogate import phase_randomise                                     # noqa: E402

SEED0 = 20261201
PRIMARY = [(15.0, 4), (15.0, 6), (10.0, 4), (10.0, 6), (10.0, 8)]


def load_galaxies_variants(cap, zlo=ZMIN, zhi=ZMAX):
    f = {'NGC': 'North', 'SGC': 'South'}[cap]
    with fits.open(f"{S2.DATA}/galaxy_DR12v5_CMASSLOWZTOT_{f}.fits.gz") as h:
        d = h[1].data
        z = np.asarray(d['Z'], float)
        m = (z > zlo) & (z < zhi)
        pos = sky_to_cart(np.asarray(d['RA'], float)[m],
                          np.asarray(d['DEC'], float)[m], z[m]).astype(np.float32)
        systot = np.asarray(d['WEIGHT_SYSTOT'], float)[m]
        cp = np.asarray(d['WEIGHT_CP'], float)[m]
        noz = np.asarray(d['WEIGHT_NOZ'], float)[m]
        fkp = np.asarray(d['WEIGHT_FKP'], float)[m]
    std = systot * (cp + noz - 1.0)
    return pos, {
        'standard': std,                       # what Stage 6 used
        'none': np.ones(std.size),             # no completeness weighting at all
        'no_systot': cp + noz - 1.0,           # drop the imaging-systematics weight
        'systot_only': systot,                 # drop fibre-collision / redshift-failure
        'standard_fkp': std * fkp,             # add the FKP weight
    }


def run(cap, n_null=3):
    t0 = time.time()
    geo = DataGeometry(cap, ZMIN, ZMAX)
    pos, wv = load_galaxies_variants(cap, ZMIN, ZMAX)
    fm = float(geo.m32.mean())
    res = {'cap': cap, 'n_null': n_null, 'variants': {}}
    for name, w in wv.items():
        dm, alpha = read_field(geo, pos, w)
        rec = dict(alpha=float(alpha), sum_w=float(w.sum()),
                   kappa=float((w * w).mean() / w.mean()))
        rec['data'] = measure(geo, dm)
        n2 = []
        for i in range(n_null):
            dpr = (phase_randomise(geo.g, dm, SEED0 + 17 * i) / np.sqrt(fm)) * geo.m32
            d2, cl = poisson_resample(geo, dpr, alpha, SEED0 + 991 * i + 3)
            del dpr
            n2.append(measure(geo, d2))
            del d2
        rec['n2'] = n2
        res['variants'][name] = rec
        del dm
        log(f"    [{cap}] weight scheme '{name}' done  sigma(R=15)="
            f"{rec['data'][15.0]['sigma']:.4f}   [{time.time()-t0:.0f}s]")
        json.dump(res, open(f"{HERE}/refuter_a2_{cap}.json", 'w'), default=float)
    del geo, pos
    return res


def report(cap):
    res = json.load(open(f"{HERE}/refuter_a2_{cap}.json"))
    sig = {(r['cap'], r['R'], r['b'], r['geom']): r['sigma']
           for r in json.load(open(f"{HERE}/sky_final_verdict.json"))}
    base = None
    log("\n  A2 -- TARGET under published weight variants, folded, cap=%s" % cap)
    log("  %-14s %-5s %-2s %13s %13s %11s %9s"
        % ("scheme", "R", "b", "I(data)", "target", "shift", "shift/sig"))
    out = []
    for name, rec in res['variants'].items():
        for (R, b) in PRIMARY:
            e = rec['data'][str(R)]['b'][str(b)]['folded']
            if not e.get('occupancy_pass'):
                continue
            i2 = np.mean([x[str(R)]['b'][str(b)]['folded']['I'] for x in rec['n2']])
            tgt = e['I'] - i2
            s = sig.get((cap, str(R), str(b), 'folded'))
            if name == 'standard':
                pass
            key = (R, b)
            out.append(dict(scheme=name, R=R, b=b, I=e['I'], I_n2=i2, target=tgt, sigma=s))
    base = {(r['R'], r['b']): r['target'] for r in out if r['scheme'] == 'standard'}
    for r in out:
        d = r['target'] - base[(r['R'], r['b'])]
        r['shift'] = d
        r['shift_over_sigma'] = d / r['sigma'] if r['sigma'] else float('nan')
        log("  %-14s %-5s %-2s %13.5e %13.5e %11.3e %9.2f"
            % (r['scheme'], r['R'], r['b'], r['I'], r['target'], d, r['shift_over_sigma']))
    json.dump(out, open(f"{HERE}/refuter_a2_report_{cap}.json", 'w'), indent=1, default=float)
    return out


if __name__ == '__main__':
    cap = sys.argv[1] if len(sys.argv) > 1 else 'SGC'
    nn = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    log("=" * 96)
    log(f"REFUTER A2 -- WEIGHT VARIANTS  cap={cap}  n_null={nn}  (post-unblind, post-hoc)")
    log("=" * 96)
    if not (len(sys.argv) > 3 and sys.argv[3] == 'report'):
        run(cap, nn)
    report(cap)
