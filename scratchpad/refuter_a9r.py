#!/usr/bin/env python3
"""
refuter_a9r.py -- the one-line controlled experiment behind A9b.

The pipeline's null is
    lam = alpha * exp_ran * max(1 + dpr, 0)
and max(1+dpr,0) has a measured mean of 1.775, because dpr is a phase-randomised copy of the
data's cell-level delta whose rms is ~3 and clipping a zero-mean field of that width at -1
leaves a large positive mean.  The null is therefore drawn at 1.775x the data's number density.

This file changes EXACTLY that and nothing else:
    lam = alpha * exp_ran * max(1 + dpr, 0) / <max(1 + dpr, 0)>
same seeds, same phases, same clipping, same everything.  If the target moves, the density is
the mechanism; if it does not, my A9b attribution is wrong and I say so.

Post-unblind, post-hoc.  Pre-registered in REFUTER_PREREG.md.
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_realdata import F32, log                                            # noqa: E402
import sky_stage2 as S2                                                      # noqa: E402
from sky_stage6 import DataGeometry, load_galaxies, ZMIN, ZMAX               # noqa: E402
from sky_stage7 import read_field, measure                                   # noqa: E402
from sky_surrogate import phase_randomise                                    # noqa: E402

SEED0 = 20261201
PRIMARY = [(15.0, 4), (15.0, 6), (10.0, 4), (10.0, 6), (10.0, 8)]


def resample(geo, dpr, alpha, seed, renorm):
    mod = np.maximum(1.0 + dpr, 0.0)
    mu = 1.0
    if renorm:
        mu = float((geo.exp_ran * mod)[geo.mask].sum() / geo.exp_ran[geo.mask].sum())
        mod = (mod / mu).astype(F32)
    lam = alpha * geo.exp_ran * mod
    del mod
    n = np.random.default_rng(seed).poisson(lam).astype(F32)
    del lam
    exp = alpha * geo.exp_ran
    d = np.zeros_like(n)
    np.divide(n - exp, exp, out=d, where=geo.mask)
    del n, exp
    return (d * geo.m32).astype(F32), mu


def run(cap, n_null=3):
    t0 = time.time()
    geo = DataGeometry(cap, ZMIN, ZMAX)
    pos, w = load_galaxies(cap, ZMIN, ZMAX)
    dm, alpha = read_field(geo, pos, w)
    del pos, w
    res = dict(cap=cap, data=measure(geo, dm), n2=[], n2r=[], mu=None)
    fm = float(geo.m32.mean())
    for i in range(n_null):
        dpr = (phase_randomise(geo.g, dm, SEED0 + 17 * i) / np.sqrt(fm)) * geo.m32
        f0, _ = resample(geo, dpr, alpha, SEED0 + 991 * i + 3, False)
        res['n2'].append(measure(geo, f0)); del f0
        f1, mu = resample(geo, dpr, alpha, SEED0 + 991 * i + 3, True)
        res['n2r'].append(measure(geo, f1)); del f1, dpr
        res['mu'] = mu
        log(f"    [{cap}] pair {i+1}/{n_null}  mean modulation {mu:.4f}  [{time.time()-t0:.0f}s]")
        json.dump(res, open(f"{HERE}/refuter_a9r_{cap}.json", 'w'), default=float)
    del geo, dm
    return res


def report(cap):
    res = json.load(open(f"{HERE}/refuter_a9r_{cap}.json"))
    sig = {(r['cap'], r['R'], r['b'], r['geom']): r
           for r in json.load(open(f"{HERE}/sky_final_verdict.json"))}
    log(f"\n  A9b CONTROLLED -- cap={cap}: the ONLY change is dividing the modulation by its "
        f"mean ({res['mu']:.4f})")
    log("  %-5s %-2s %12s %12s %12s %12s %7s %8s %8s"
        % ("R", "b", "I(N2)", "I(N2 renorm)", "target", "target(re)", "ratio", "det", "det(re)"))
    out = []
    for (R, b) in PRIMARY:
        e = res['data'][str(R)]['b'][str(b)]['folded']
        if not e.get('occupancy_pass'):
            continue
        i0 = np.mean([x[str(R)]['b'][str(b)]['folded']['I'] for x in res['n2']])
        i1 = np.mean([x[str(R)]['b'][str(b)]['folded']['I'] for x in res['n2r']])
        t0_, t1 = e['I'] - i0, e['I'] - i1
        k = (cap, str(R), str(b), 'folded')
        sg = sig[k]['sigma']
        out.append(dict(cap=cap, R=R, b=b, I_n2=i0, I_n2r=i1, target=t0_, target_renorm=t1,
                        ratio=t1 / t0_, sigma=sg, detect=t0_ / sg, detect_renorm=t1 / sg))
        log("  %-5s %-2s %12.5e %12.5e %12.5e %12.5e %7.3f %8.1f %8.1f"
            % (R, b, i0, i1, t0_, t1, t1 / t0_, t0_ / sg, t1 / sg))
    json.dump(out, open(f"{HERE}/refuter_a9r_report_{cap}.json", 'w'), indent=1, default=float)
    return out


if __name__ == '__main__':
    cap = sys.argv[1] if len(sys.argv) > 1 else 'SGC'
    if not (len(sys.argv) > 2 and sys.argv[2] == 'report'):
        log("=" * 96)
        log(f"REFUTER A9b CONTROLLED  cap={cap}   (post-unblind, post-hoc)")
        log("=" * 96)
        run(cap)
    report(cap)
