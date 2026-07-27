#!/usr/bin/env python3
"""
sky_stage7.py -- the last measurement: the VALVE FLOOR, per Amendment 5.

Builds two nulls from the same field and measures the data against both:
  N1  plain phase-randomised surrogate            -- shot-noise POWER, Gaussian phases
  N2  N1 then POISSON-RESAMPLED at the field's own nbar(z) through the identical selection
                                                  -- shot-noise power AND non-Gaussianity
  VALVE FLOOR  =  I(N2) - I(N1)         a measurement, not a model
  TARGET       =  I(data) - I(N2)       the Amendment 5 quantity

Reports, per row and as Amendment 5 requires: the clipped fraction of the Gaussian modulation
and the null's own smoothed skewness.  If clipping contributes comparably to Poisson, the
valve floor is an UPPER BOUND and the verdict must say so.
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_realdata import (F32, quantile_labels, connected_info, configs,        # noqa: E402
                          _coarse2, log)
import sky_stage2 as S2                                                          # noqa: E402
from sky_stage6 import DataGeometry, load_galaxies, ZMIN, ZMAX                   # noqa: E402
from sky_surrogate import phase_randomise                                        # noqa: E402
from sky_pilot import route_B2                                                   # noqa: E402


def read_field(geo, pos, wt):
    g = geo.g
    n_gal = g.deposit(pos, wt)
    alpha = float(n_gal.sum()) / geo.tot_ran
    exp = alpha * geo.exp_ran
    d = np.zeros_like(n_gal)
    np.divide(n_gal - exp, exp, out=d, where=geo.mask)
    del n_gal, exp
    return (d * geo.m32).astype(F32), alpha


def poisson_resample(geo, dpr, alpha, seed):
    """Poisson-sample the phase-randomised CLUSTERING field at the field's own n-bar.
    lambda = alpha * <n_ran> * (1 + delta_PR), clipped at 0; n ~ Poisson(lambda)."""
    g = geo.g
    lam = alpha * geo.exp_ran * np.maximum(1.0 + dpr, 0.0)
    clipped = float(((1.0 + dpr) < 0.0)[geo.mask].mean())
    n = np.random.default_rng(seed).poisson(lam).astype(F32)
    del lam
    exp = alpha * geo.exp_ran
    d = np.zeros_like(n)
    np.divide(n - exp, exp, out=d, where=geo.mask)
    del n, exp
    return (d * geo.m32).astype(F32), clipped


def measure(geo, fld, bs=S2.BS, rs=S2.RS, rmult=1.5):
    g = geo.g
    F = g.fwd(fld)
    out = {}
    for R in rs:
        num = g.smooth_k(F, R); ok = geo.ok[R]
        sm = np.zeros_like(num); np.divide(num, geo.den[R], out=sm, where=ok); del num
        v = sm[ok]
        rec = {'sigma': float(v.std()),
               'skew': float(((v - v.mean()) ** 3).mean() / v.std() ** 3), 'b': {}}
        del v
        stride = max(1, int(round(R / g.cell / 3)))
        for b in bs:
            occ = geo.occupancy(R, b)
            if occ <= S2.OCC_MIN:
                rec['b'][b] = {n: dict(occupancy_pass=False) for n in configs(R, g.cell, rmult)}
                continue
            lab, _ = quantile_labels(sm, ok, b)
            sl = tuple(slice(0, ok.shape[i], stride) for i in range(3))
            ls = lab[sl]
            bb = {}
            for name, orients in configs(R, g.cell, rmult).items():
                hs = np.zeros((b, b, b))
                for (d1, d2) in orients:
                    mm = (ok[sl] & np.roll(ok, (-d1[0], -d1[1], -d1[2]), (0, 1, 2))[sl]
                          & np.roll(ok, (-d2[0], -d2[1], -d2[2]), (0, 1, 2))[sl])
                    a1 = np.roll(lab, (-d1[0], -d1[1], -d1[2]), (0, 1, 2))[sl]
                    a2 = np.roll(lab, (-d2[0], -d2[1], -d2[2]), (0, 1, 2))[sl]
                    hs += np.bincount(((ls.astype(np.int64) * b + a1) * b + a2)[mm],
                                      minlength=b ** 3).astype(np.float64).reshape(b, b, b)
                    del a1, a2, mm
                ci = connected_info(hs)
                bb[name] = dict(occupancy_pass=True, I=ci['I'], cert=ci['cert'],
                                E=float(route_B2(_coarse2(hs / hs.sum(), b).ravel())[1]))
            rec['b'][b] = bb
            del lab, ls
        out[R] = rec
        del sm
    del F
    return out


def run(n_null=8, seed0=20261201):
    res = {}
    for cap in ('SGC', 'NGC'):
        geo = DataGeometry(cap, ZMIN, ZMAX)
        pos, w = load_galaxies(cap, ZMIN, ZMAX)
        dm, alpha = read_field(geo, pos, w)
        del pos, w
        r_data = measure(geo, dm)
        n1s, n2s, clips = [], [], []
        for i in range(n_null):
            t0 = time.time()
            fm = float(geo.m32.mean())
            dpr = (phase_randomise(geo.g, dm, seed0 + 17 * i) / np.sqrt(fm)) * geo.m32
            n1s.append(measure(geo, dpr))
            d2, cl = poisson_resample(geo, dpr, alpha, seed0 + 991 * i + 3)
            clips.append(cl)
            n2s.append(measure(geo, d2))
            del dpr, d2
            log(f"    [{cap}] null {i+1}/{n_null}  clipped={cl:.4f}  {time.time()-t0:.0f}s")
        res[cap] = dict(data=r_data, n1=n1s, n2=n2s, clipped=clips)
        json.dump(res, open(f"{HERE}/sky_stage7_valve.json", 'w'), default=float)
        del geo, dm
    return res


if __name__ == '__main__':
    log("=" * 100)
    log("STAGE 7 -- THE VALVE FLOOR (Amendment 5).  The last measurement of the campaign.")
    log("=" * 100)
    res = run()
    frz = json.load(open(f"{HERE}/sky_stage5_frozen_prediction.json"))
    log("\n" + "=" * 100)
    log("  %-4s %-5s %-2s %-12s %11s %11s %11s %11s %10s %9s"
        % ("cap", "R", "b", "geom", "I_data", "I_N1(PR)", "I_N2(+Pois)",
           "VALVE", "TARGET", "T/pred"))
    rows = []
    for cap in ('SGC', 'NGC'):
        d = res[cap]
        for R in S2.RS:
            for b in S2.BS:
                for g in ('folded', 'equilateral', 'squeezed'):
                    e = d['data'][R]['b'][b][g]
                    if not e.get('occupancy_pass'):
                        continue
                    if cap == 'NGC' and R == 15.0 and b == 4 and g == 'squeezed':
                        continue
                    i1 = np.array([x[R]['b'][b][g]['I'] for x in d['n1']])
                    i2 = np.array([x[R]['b'][b][g]['I'] for x in d['n2']])
                    valve = i2.mean() - i1.mean()
                    tgt = e['I'] - i2.mean()
                    sd = i2.std(ddof=1)
                    pk = f"{cap}|{R}|{b}|{g}"
                    pred = frz.get(pk, {}).get('signal')
                    rows.append((cap, R, b, g, e['I'], i1.mean(), i2.mean(), valve, tgt,
                                 tgt / sd if sd > 0 else np.nan, pred))
                    log("  %-4s %-5s %-2s %-12s %11.4e %11.4e %11.4e %11.4e %10.3e %9s"
                        % (cap, R, b, g, e['I'], i1.mean(), i2.mean(), valve, tgt,
                           ("%.3f" % (tgt / pred)) if pred else "  n/a"))
    log("\n  CLIPPED FRACTION of the Gaussian modulation, and the nulls' smoothed skewness:")
    for cap in ('SGC', 'NGC'):
        d = res[cap]
        log("    %s: clipped %.4f   skew(data) %+.4f  skew(N1) %+.4f  skew(N2) %+.4f"
            % (cap, float(np.mean(d['clipped'])), d['data'][15.0]['skew'],
               float(np.mean([x[15.0]['skew'] for x in d['n1']])),
               float(np.mean([x[15.0]['skew'] for x in d['n2']]))))
    json.dump([{k: v for k, v in zip(
        ('cap', 'R', 'b', 'geom', 'I_data', 'I_N1', 'I_N2', 'valve', 'target', 'target_sig',
         'pred'), r)} for r in rows],
        open(f"{HERE}/sky_stage7_verdict.json", 'w'), indent=1, default=float)
