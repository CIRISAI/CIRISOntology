#!/usr/bin/env python3
"""
eboss_stage0_mocks.py -- STAGE 0, part 2: the EZmock inventory and the derived floor forecast.

Still metadata only.  Reads one EZmock realisation per tracer to establish columns, row counts
and the data-vs-mock n(z) agreement (a VOID condition, SKY_REALDATA_PREREG.md section 7.6),
and projects the shot-noise/valve floor onto each candidate sample from the campaign's OWN
measured amplitude-versus-density curve.

Writes eboss_stage0_mocks.json.
"""
import json
import os
import sys

import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_realdata import log                                    # noqa: E402

DATA = os.environ.get('SKYDATA', '/home/emoore/skydata')
EB, EZ = f"{DATA}/eboss", f"{DATA}/eboss/ez"
RS = [15.0, 10.0]

# SKY_FORECAST_RESULTS.md section 12, quoted in SKY_REALDATA_AMENDMENT_1 A1.3: the shot-noise
# floor as a fraction of the mock signal, measured at two densities.  AMENDMENT_1 interpolated
# LOGARITHMICALLY between them and this reproduces that operation exactly, including its
# reproduction of AMENDMENT_1's own numbers as a check.
FLOOR_GRID = [(1.6, 1.30), (15.7, 0.58)]


def floor_frac(nV):
    """Floor as a fraction of signal at n-bar V_R = nV, log-interpolated on the measured grid.

    OUTSIDE the grid this is an EXTRAPOLATION and is flagged as one.  The campaign never
    measured below n-bar V_R = 1.6, so the QSO numbers below are extrapolated and are reported
    as extrapolations rather than as a floor measurement.
    """
    (x0, y0), (x1, y1) = FLOOR_GRID
    t = (np.log(nV) - np.log(x0)) / (np.log(x1) - np.log(x0))
    return y0 + t * (y1 - y0), not (x0 <= nV <= x1)


def nz_hist(z, lo, hi, nb=40):
    h, e = np.histogram(z, bins=nb, range=(lo, hi))
    return h / h.sum(), e


def main():
    out = {'floor_grid': FLOOR_GRID, 'samples': {}, 'mocks': {}}
    s0 = json.load(open(f"{HERE}/eboss_stage0.json"))

    log("=" * 100)
    log("STAGE 0 part 2 -- floor projection from the campaign's OWN measured density curve")
    log("=" * 100)
    log("  reproduction check against AMENDMENT_1 A1.3 (which quotes 95% at R=10, 58% at R=15):")
    for nm, nV in (("BOSS R=10 (A1 quotes 4.81)", 4.81), ("BOSS R=15 (A1 quotes 16.22)", 16.22)):
        f, ex = floor_frac(nV)
        log(f"    {nm:32s} n-barV={nV:6.2f} -> floor {100*f:5.1f}% of signal{'  [EXTRAP]' if ex else ''}")

    log("")
    log(f"  {'sample':16s} {'R':>4s} {'nbarV_R':>8s} {'floor/signal':>13s} "
        f"{'occ b=4':>8s} {'occ b=6':>8s} {'occ b=8':>8s}  rungs>100")
    for key in ('BOSS|NGC', 'BOSS|SGC', 'LRG|NGC', 'LRG|SGC', 'ELG|NGC', 'ELG|SGC',
                'QSO|NGC', 'QSO|SGC', 'LRGpCMASS|NGC', 'LRGpCMASS|SGC'):
        if key.startswith('BOSS'):
            r = s0['boss_reference'][key.split('|')[1]]
        else:
            r = s0['tracers'].get(key)
        if r is None:
            continue
        rec = {}
        for R in RS:
            nV = r[f'nbarV_R{int(R)}_galweighted']
            f, ex = floor_frac(nV)
            occ = {b: r[f'occ_R{int(R)}_b{b}'] for b in (4, 6, 8)}
            rungs = [b for b in (4, 6, 8) if occ[b] > 100]
            rec[str(int(R))] = dict(nbarV=nV, floor_frac=f, extrapolated=bool(ex),
                                    occ=occ, rungs_passing=rungs,
                                    two_rung_clause=bool(len(rungs) >= 2))
            log(f"  {key:16s} {int(R):4d} {nV:8.2f} {100*f:12.1f}%{'*' if ex else ' '} "
                f"{occ[4]:8.0f} {occ[6]:8.0f} {occ[8]:8.0f}  "
                f"{','.join(map(str, rungs)) if rungs else 'NONE':>9s}"
                f"{'   <-- (a) two-rung clause FAILS' if len(rungs) < 2 else ''}")
        out['samples'][key] = rec

    # ---- the mocks, read rather than recalled
    log("")
    log("  EZmock realisations on disk, columns and n(z) agreement with the data:")
    for tracer, zlo, zhi in (('ELG', 0.6, 1.1), ('LRG', 0.6, 1.0)):
        f = f"{EZ}/EZmock_realistic_eBOSS_{tracer}_NGC_v7_0001.dat.fits.gz"
        if not os.path.exists(f):
            continue
        with fits.open(f) as h:
            cols = list(h[1].columns.names)
            zm = np.asarray(h[1].data['Z'], float)
            wm = {c: np.asarray(h[1].data[c], float) for c in cols
                  if c.startswith('WEIGHT') or c == 'NZ'}
        with fits.open(f"{EB}/eBOSS_{tracer}_clustering_data-NGC-vDR16.fits") as h:
            zd = np.asarray(h[1].data['Z'], float)
        md = (zd > zlo) & (zd < zhi)
        mm = (zm > zlo) & (zm < zhi)
        hd, _ = nz_hist(zd[md], zlo, zhi)
        hm, _ = nz_hist(zm[mm], zlo, zhi)
        # total-variation distance between the two normalised n(z) shapes
        tv = float(0.5 * np.abs(hd - hm).sum())
        rec = dict(columns=cols, rows_all_z=int(zm.size), rows_in_z=int(mm.sum()),
                   data_rows_in_z=int(md.sum()),
                   ratio_mock_over_data=float(mm.sum()) / float(md.sum()),
                   z_min=float(zm.min()), z_max=float(zm.max()),
                   nz_total_variation=tv,
                   weight_means={k: float(v[mm].mean()) for k, v in wm.items()},
                   kappa_standard=float(
                       ((wm['WEIGHT_SYSTOT'][mm] * (wm['WEIGHT_CP'][mm]
                                                    + wm['WEIGHT_NOZ'][mm] - 1)) ** 2).mean()
                       / (wm['WEIGHT_SYSTOT'][mm] * (wm['WEIGHT_CP'][mm]
                                                     + wm['WEIGHT_NOZ'][mm] - 1)).mean())
                   if 'WEIGHT_SYSTOT' in wm else None)
        out['mocks'][tracer] = rec
        log(f"    {tracer} NGC mock 0001: rows_all_z={rec['rows_all_z']}  "
            f"in {zlo}<z<{zhi}: {rec['rows_in_z']} vs data {rec['data_rows_in_z']} "
            f"(ratio {rec['ratio_mock_over_data']:.3f});  n(z) total-variation "
            f"{tv:.4f};  kappa_mock={rec['kappa_standard']:.4f}")
        log(f"      cols: {cols}")

    json.dump(out, open(f"{HERE}/eboss_stage0_mocks.json", 'w'), default=float, indent=1)
    log("\nwrote eboss_stage0_mocks.json")


if __name__ == '__main__':
    main()
