#!/usr/bin/env python3
"""
sky_stage7_mocks.py -- the prediction, recomputed against the SAME null the data is scored
against.

WHY THIS IS NECESSARY.  The frozen prediction (Stage 5) is `I(mock) - I(plain phase-randomised
surrogate)`.  Amendment 5 scores the data as `I(data) - I(Poisson-RESAMPLED surrogate)`.  Those
two differ by the valve floor, so comparing them directly is exactly the apples-to-oranges
error this campaign keeps catching -- it would make the data look ~30 % low against a
prediction that still has the valve term in it.

So the prediction is recomputed the same way, on a subset of the suite:
    prediction_valve-corrected = mean[ I(mock) - I(N2 of that mock) ]

The FROZEN prediction is not altered.  This is a second, separately-labelled quantity, and both
appear in the results.

BLINDING: mocks only.
"""
import json
import os
import sys
import tarfile
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_realdata import F32, sky_to_cart, log                                   # noqa: E402
import sky_stage2 as S2                                                          # noqa: E402
from sky_stage7 import read_field, poisson_resample, measure                     # noqa: E402
from sky_surrogate import phase_randomise                                        # noqa: E402


def run(cap, n_mock=16, seed0=20261301, out=None):
    geo = S2.CapGeometry(cap)
    tf = tarfile.open(f"{S2.DATA}/Patchy-Mocks-DR12{cap}-COMPSAM_V6C.tar.gz", 'r|gz')
    res, t0 = [], time.time()
    fm = float(geo.m32.mean())
    for i, m in enumerate(tf):
        if i >= n_mock:
            break
        raw = tf.extractfile(m).read()
        a = S2._load_ascii(raw, 8); del raw
        sel = a[:, 6] > 0.5
        pos = sky_to_cart(a[sel, 0], a[sel, 1], a[sel, 2]).astype(np.float32)
        wt = a[sel, 7].astype(np.float64); del a
        dm, alpha = read_field(geo, pos, wt); del pos, wt
        r_m = measure(geo, dm)
        dpr = (phase_randomise(geo.g, dm, seed0 + 17 * i) / np.sqrt(fm)) * geo.m32
        r_1 = measure(geo, dpr)
        d2, cl = poisson_resample(geo, dpr, alpha, seed0 + 991 * i + 3)
        r_2 = measure(geo, d2)
        del dm, dpr, d2
        res.append(dict(mock=r_m, n1=r_1, n2=r_2, clipped=cl))
        if out:
            json.dump(dict(cap=cap, n=len(res), res=res), open(out, 'w'), default=float)
        log(f"    [{cap}] {i+1}/{n_mock}  clipped={cl:.4f}  "
            f"{(time.time()-t0)/(i+1):.0f}s each")
    tf.close()
    return res


if __name__ == '__main__':
    cap = sys.argv[1] if len(sys.argv) > 1 else 'SGC'
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 16
    log(f"STAGE 7 MOCK-SIDE VALVE  cap={cap}  n={n}")
    r = run(cap, n, out=f"{HERE}/sky_stage7_mocks_{cap}.json")
    log("\n  prediction recomputed against the SAME null the data is scored against:")
    log("  %-5s %-2s %-12s %11s %11s %11s %11s"
        % ("R", "b", "geom", "I_mock", "I_N2", "pred_valve", "valve"))
    for R in S2.RS:
        for b in S2.BS:
            for g in ('folded', 'equilateral', 'squeezed'):
                e = r[0]['mock'][R]['b'][b][g]
                if not e.get('occupancy_pass'):
                    continue
                im = np.array([x['mock'][R]['b'][b][g]['I'] for x in r])
                i1 = np.array([x['n1'][R]['b'][b][g]['I'] for x in r])
                i2 = np.array([x['n2'][R]['b'][b][g]['I'] for x in r])
                log("  %-5s %-2s %-12s %11.4e %11.4e %11.4e %11.4e"
                    % (R, b, g, im.mean(), i2.mean(), im.mean() - i2.mean(),
                       i2.mean() - i1.mean()))
