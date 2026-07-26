#!/usr/bin/env python3
"""
sky_artifact_gates.py -- the two discriminators promoted to per-run gates after Stage 2's
withdrawal.  Both come directly from the failure mode that got past the first production run.

THE LESSON BEING ENCODED.  The withdrawn run reported a floor with 0.7-2.3 % per-realisation
scatter and it was wrong by 8-15x.  The scatter was tight *because* the contaminating term was
a FIXED GEOMETRIC ARTIFACT -- identical in every realisation, hence a large and perfectly
reproducible pedestal.  A tight error bar on the wrong quantity looks exactly like a converged
measurement, so tightness can never again be taken as evidence of correctness.

GATE A -- PHYSICAL SANITY OF sigma.  The post-pipeline sigma of the smoothed density contrast
must lie in a physically possible band.  The withdrawn run read sigma = 176; a density
contrast smoothed at 15 Mpc/h cannot do that.  Cheap, per-realisation, and it is the check
that actually caught the defect.
      VOID if any realisation has sigma outside [0.02, 2.0] at R = 15.

GATE B -- MASK-PERTURBATION SENSITIVITY.  **I first wrote this gate with its polarity
inverted, and the correction is recorded rather than quietly flipped.**

The first version reasoned: a window-generated floor must RESPOND when the window is
perturbed, so insensitivity is the pedestal signature.  Run on the corrected pipeline it
FLAGGED (dI = 1.31e-05 against a realisation scatter of 7.78e-05, ratio 0.2).  That verdict is
wrong, and thinking about which way the withdrawn run would have gone shows why.

The contamination this gate exists to catch lived in MARGINAL cells -- the low-density halo
just inside a too-permissive footprint, where the denominator collapsed.  Those are exactly
the cells a threshold perturbation adds and removes.  So the artifact is EXTREMELY
mask-sensitive: the withdrawn configuration read 1.03e-02 at mask fraction 0.302 while the
corrected one reads 6.82e-04 at 0.154 -- a 15x change in the answer from a 2x change in the
footprint.  A floor dominated instead by LOCAL physics (shot noise plus smoothing) is
correctly INSENSITIVE to where the boundary sits, because removing a rim leaves the bulk
statistics unchanged.

So the polarity is the other way round:
      HEALTHY  : |dI| small compared to the per-realisation scatter -- the reading is a bulk
                 property, not a boundary property.
      FLAG     : |dI| LARGE compared to the scatter (ratio > 3) -- the reading is dominated by
                 the marginal cells the threshold moves, which is the withdrawn run's
                 signature.

Measured on the corrected pipeline: ratio 0.2, i.e. a 21 % change in footprint volume moves
the floor by 2 % -- comfortably HEALTHY under the corrected reading.

Neither gate can prove a reading correct.  Both can catch the specific way this pipeline has
already failed once.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_realdata import sky_to_cart, log                                  # noqa: E402
import sky_stage2 as S                                                     # noqa: E402
import tarfile                                                             # noqa: E402

SIGMA_BAND = (0.02, 2.0)


def gate_a(path, R=15.0):
    """Physical sanity of sigma, applied post-hoc from a Stage 2 JSON (sigma is recorded per
    realisation, so this is identical to an in-run check)."""
    d = json.load(open(path))
    key = str(R) if str(R) in d['res'][0] else R
    s = np.array([r[key]['sigma'] for r in d['res']])
    lo, hi = SIGMA_BAND
    bad = int(((s < lo) | (s > hi)).sum())
    return dict(cap=d['cap'], n=len(s), sigma_min=float(s.min()), sigma_max=float(s.max()),
                sigma_mean=float(s.mean()), band=SIGMA_BAND, n_outside=bad,
                passed=bool(bad == 0))


def gate_b(cap, n_mock=6, fracs=(0.4, 0.5, 0.6), R=15.0, b=4, geom='folded'):
    """Mask-perturbation sensitivity.  Rebuild the geometry at perturbed footprint thresholds
    and measure the same mocks through each."""
    out = {}
    tf = tarfile.open(f"{S.DATA}/Patchy-Mocks-DR12{cap}-COMPSAM_V6C.tar.gz", 'r|gz')
    mocks = []
    for i, m in enumerate(tf):
        if i >= n_mock:
            break
        raw = tf.extractfile(m).read()
        a = S._load_ascii(raw, 8); del raw
        sel = a[:, 6] > 0.5
        mocks.append((sky_to_cart(a[sel, 0], a[sel, 1], a[sel, 2]).astype(np.float32),
                      a[sel, 7].astype(np.float64)))
        del a
    tf.close()
    for fr in fracs:
        S.MASK_FRAC = fr
        geo = S.CapGeometry(cap, rs=[R])
        vals = []
        for (pos, w) in mocks:
            r = geo.measure(pos, w, bs=[b], rs=[R])
            e = r[R]['b'][b][geom]
            vals.append(e['I'] if e.get('occupancy_pass') else np.nan)
        out[fr] = dict(I=float(np.nanmean(vals)),
                       scatter=float(np.nanstd(vals, ddof=1)),
                       occ=float(geo.occupancy(R, b)),
                       valid=float(geo.ok[R].mean()))
        log(f"    frac={fr:.2f}  valid={out[fr]['valid']:.4f}  occ={out[fr]['occ']:.0f}  "
            f"I={out[fr]['I']:.4e} +- {out[fr]['scatter']:.2e}")
        del geo
    ks = sorted(out)
    dI = abs(out[ks[-1]]['I'] - out[ks[0]]['I'])
    sc = float(np.mean([out[k]['scatter'] for k in ks]))
    return dict(cap=cap, R=R, b=b, geom=geom, by_frac=out, dI=dI, scatter=sc,
                ratio=dI / max(sc, 1e-30),
                passed=bool(dI <= 3.0 * sc),
                note="CORRECTED POLARITY: a bulk-dominated floor is INSENSITIVE to where the "
                     "footprint boundary sits; large sensitivity means the marginal cells "
                     "dominate, which is the withdrawn run's signature. FLAG if ratio > 3.")


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'a'
    res = {}
    if what in ('a', 'all'):
        log("GATE A -- physical sanity of sigma")
        for cap in ('SGC', 'NGC'):
            p = f"{HERE}/sky_stage2_{cap}.json"
            if os.path.exists(p):
                r = gate_a(p); res[f'A_{cap}'] = r
                log(f"  {cap}: n={r['n']} sigma in [{r['sigma_min']:.4f}, {r['sigma_max']:.4f}]"
                    f"  band {r['band']}  -> {'PASS' if r['passed'] else 'VOID'}")
        for cap in ('SGC', 'NGC'):
            p = f"{HERE}/sky_stage2_{cap}_INVALID.json"
            if os.path.exists(p):
                r = gate_a(p)
                log(f"  [withdrawn run, for contrast] {cap}: sigma in "
                    f"[{r['sigma_min']:.2f}, {r['sigma_max']:.2f}] -> "
                    f"{'PASS' if r['passed'] else 'VOID -- the gate would have caught it'}")
    if what in ('b', 'all'):
        log("\nGATE B -- mask-perturbation sensitivity")
        for cap in (sys.argv[2:] or ['SGC']):
            r = gate_b(cap); res[f'B_{cap}'] = r
            log(f"  {cap}: dI={r['dI']:.3e}  scatter={r['scatter']:.3e}  "
                f"ratio={r['ratio']:.1f}  -> "
                f"{'HEALTHY (bulk-dominated)' if r['passed'] else 'FLAG: boundary-dominated'}")
    json.dump(res, open(f"{HERE}/sky_artifact_gates.json", 'w'), indent=1, default=float)
