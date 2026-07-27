#!/usr/bin/env python3
"""
refuter_nulls_fast.py -- the trimmed A9/A1/A6 run for NGC.

Identical construction to refuter_nulls.py; the pedestal measurement and the wide eps grid are
dropped because this machine is shared and the full NGC run was CPU-starved.  Everything that
the verdict depends on is here: the pipeline's own null reproduced from its recorded seeds, the
matched-modulation nulls, two dispersion points bracketing the defensible range, and the
over-generous lognormal probe.

Post-unblind, post-hoc.  Pre-registered in REFUTER_PREREG.md.
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_realdata import log                                                  # noqa: E402
from sky_stage6 import DataGeometry, load_galaxies, ZMIN, ZMAX                # noqa: E402
from sky_stage7 import read_field, poisson_resample, measure                  # noqa: E402
from sky_surrogate import phase_randomise                                     # noqa: E402
from refuter_nulls import (weight_moments, matched_clustering_field, clip_mod,  # noqa: E402
                           lognormal_mod, sample_null, SEED0, RSEED)


def run(cap, n_null=2, eps_grid=(0.25, 0.5, 1.0), out=None):
    t0 = time.time()
    kappa = weight_moments(cap)['standard']['kappa']
    geo = DataGeometry(cap, ZMIN, ZMAX)
    pos, w = load_galaxies(cap, ZMIN, ZMAX)
    dm, alpha = read_field(geo, pos, w)
    del pos, w
    res = dict(cap=cap, kappa=kappa, alpha=float(alpha))
    res['data'] = measure(geo, dm)
    log(f"  [{cap}] data sigma R=15 {res['data'][15.0]['sigma']:.4f}  [{time.time()-t0:.0f}s]")
    fm = float(geo.m32.mean())
    fam = {}
    for i in range(n_null):
        dpr = (phase_randomise(geo.g, dm, SEED0 + 17 * i) / np.sqrt(fm)) * geo.m32
        mod_pipe = np.maximum(1.0 + dpr, 0.0)
        res['pipeline_mean_mod'] = float(
            (geo.exp_ran * mod_pipe)[geo.mask].sum() / geo.exp_ran[geo.mask].sum())
        del mod_pipe
        d2, cl = poisson_resample(geo, dpr, alpha, SEED0 + 991 * i + 3)
        fam.setdefault('N2pipe', []).append(measure(geo, d2))
        res['repro_clipped'] = cl
        del d2, dpr
        cf, info = matched_clustering_field(geo, dm, alpha, kappa, RSEED + 101 * i)
        mod, clipped = clip_mod(cf)
        if i == 0:
            res['matched_info'] = dict(info, clipped=clipped,
                                       sigma_cf=float(cf[geo.mask].std()))
        vs = [('N2m', dict(mode='poisson')), ('N2mw', dict(mode='clumped', kappa=kappa))]
        vs += [(f'N2eps{e:g}', dict(mode='nb', eps=e)) for e in eps_grid]
        for name, kw in vs:
            fld = sample_null(geo, mod, alpha, RSEED + 977 * i + 13, **kw)
            fam.setdefault(name, []).append(measure(geo, fld))
            del fld
        lm, linfo = lognormal_mod(cf, geo.mask)
        res['lognormal_info'] = linfo
        fldL = sample_null(geo, lm, alpha, RSEED + 977 * i + 29, mode='clumped', kappa=kappa)
        fam.setdefault('N2L', []).append(measure(geo, fldL))
        del fldL, lm, mod, cf
        res['family'] = fam
        if out:
            json.dump(res, open(out, 'w'), default=float)
        log(f"    [{cap}] draw {i+1}/{n_null} done  clipped(pipeline) {cl:.4f}  "
            f"mean mod {res['pipeline_mean_mod']:.4f}  [{time.time()-t0:.0f}s]")
    del geo, dm
    return res


if __name__ == '__main__':
    cap = sys.argv[1] if len(sys.argv) > 1 else 'NGC'
    nn = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    log("=" * 96)
    log(f"REFUTER A9/A1/A6 (trimmed)  cap={cap}  n_null={nn}   (post-unblind, post-hoc)")
    log("=" * 96)
    r = run(cap, nn, out=f"{HERE}/refuter_fast_{cap}.json")
    sig = {(x['cap'], x['R'], x['b'], x['geom']): x
           for x in json.load(open(f"{HERE}/sky_final_verdict.json"))}
    log("\n  %-10s %-5s %-2s %13s %13s %7s %8s" % ("null", "R", "b", "I(null)", "target",
                                                   "ratio", "det"))
    rows = []
    for R in (15.0, 10.0):
        for b in (4, 6, 8):
            e = r['data'][R]['b'][b]['folded']
            if not e.get('occupancy_pass'):
                continue
            k = (cap, str(R), str(b), 'folded')
            if k not in sig:
                continue
            base = None
            for name in ('N2pipe', 'N2m', 'N2mw', 'N2eps0.25', 'N2eps0.5', 'N2eps1', 'N2L'):
                if name not in r['family']:
                    continue
                iv = float(np.mean([x[R]['b'][b]['folded']['I'] for x in r['family'][name]]))
                tg = e['I'] - iv
                if base is None:
                    base = tg
                rows.append(dict(cap=cap, R=R, b=b, null=name, I_null=iv, target=tg,
                                 ratio=tg / base, sigma=sig[k]['sigma'],
                                 detect=tg / sig[k]['sigma']))
                log("  %-10s %-5s %-2s %13.5e %13.5e %7.3f %8.1f"
                    % (name, R, b, iv, tg, tg / base, tg / sig[k]['sigma']))
            log("  %-10s %-5s %-2s %13s %13.5e %7.3f %8.1f"
                % ("[recorded]", R, b, "-", sig[k]['target'], sig[k]['target'] / base,
                   sig[k]['detect']))
    json.dump(rows, open(f"{HERE}/refuter_fast_report_{cap}.json", 'w'), indent=1, default=float)
