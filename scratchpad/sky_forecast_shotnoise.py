#!/usr/bin/env python3
"""
sky_forecast_shotnoise.py -- the shot-noise gate, properly powered, as the VALVE test.

Extension to the pre-registered `poisson` gate in sky_forecast.py, run after
`Core/Valve.lean` landed.  The original gate (n_real = 3, R = 25 and 60) is left exactly as
it was run and is reported separately; this is an ADDITION, not a replacement, and it is
labelled that way in SKY_FORECAST_RESULTS.md.

WHY IT IS NOW LOAD-BEARING RATHER THAN A NUISANCE TERM.  `Core/Valve.lean` proves two things
about per-cell STOCHASTIC channels acting on three cells:

  * `channel3_prod3` / `valve_from_nothing` -- a per-cell channel applied to a PRODUCT state
    returns a product state, whose whole-only share is exactly 0.  Never from nothing.
  * but on a state that already carries PAIR structure, a per-cell channel CAN mint
    whole-only share (existence, measured at 0.054 nat on the ferro habit under single-site
    damping).

Poisson sampling of a density field is a per-cell stochastic channel, and the field it acts
on is exactly the second case: correlated, with whole-only share exactly zero.  **So this is
the valve configuration, and whether the valve opens in a realistic pipeline is a measurement
this forecast has to make rather than bound.**

THREE BASE FIELDS, chosen so the theorem's boundary is the experiment's axis:

  F0     Gaussian at the 2LPT P(k).  Correlated; share EXACTLY 0 by
         `share_eq_zero_of_signSymmetric`.  **The valve configuration.**
  WHITE  spatially uncorrelated Gaussian.  A PRODUCT state at the cell level, so the Poisson
         channel provably cannot mint on it.  (Honest caveat: the pipeline's smoothing comes
         AFTER the channel and is not per-cell, so this arm is theorem-exact only up to the
         smoothing step -- it is a mechanism contrast, not a second exact null.)
  2LPT   gravity, to price the effect against the deliverable GAP at the same R.

Reported for every (base, nbar, R, geometry): the paired BIAS  mean[E(nbar) - E(inf)]  and
the added SCATTER, both against the GAP measured at the same R in the main sweep.

Usage: python sky_forecast_shotnoise.py [n_real]
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_forecast import (Grid, build_gravity, binarise, geometries, triple_read,   # noqa
                          side_lengths, F32, log)

NBARS = [1e-4, 1e-3, 1e-2]          # (h/Mpc)^3, the DESI-like range, two decades
RS = [10.0, 25.0]                   # the scales where the forecast GAP is detectable
RMULTS = (1.5, 3.0)


def run(N=384, L=768.0, n_real=10, seed0=20261001):
    g = Grid(N, L)
    log("=" * 100)
    log(f"SHOT-NOISE GATE (valve configuration)  N={N} L={L} cell={g.cell:.2f} Mpc/h  "
        f"V={(L/1000.)**3:.3f} (Gpc/h)^3  n_real={n_real}")
    log(f"  nbar = {NBARS} (h/Mpc)^3 ; nbar*V_cell = "
        f"{[round(n*g.Vcell, 4) for n in NBARS]} counts per cell")
    log("=" * 100)
    acc = {}
    for r in range(n_real):
        t0 = time.time()
        rs = np.random.default_rng(seed0 + 1000 * r)
        w = rs.standard_normal((N,) * 3).astype(F32)
        wk = g.fwd(w)
        arms = build_gravity(g, wk, want_sectors=False, want_za=False)
        arms.pop('_mono_viol')
        Ptar = g.measure_P(arms['2LPT'])
        wn = g.white_bin_power(wk)
        base = {'F0': g.gauss_from_white(wk, g.P_on_grid(Ptar / np.maximum(wn, 1e-30))),
                'WHITE': (w / w.std()).astype(F32),
                '2LPT': arms['2LPT']}
        del arms, wk, w
        prng = np.random.default_rng(seed0 + 77 + r)
        for nm, f in base.items():
            lam0 = np.maximum(1.0 + f.astype(np.float64), 0.0)
            for nb in NBARS + [np.inf]:
                if np.isfinite(nb):
                    n = prng.poisson((nb * g.Vcell) * lam0).astype(F32)
                    d = (n / (nb * g.Vcell) - 1.0).astype(F32)
                    del n
                else:
                    d = f
                Fk = g.fwd(d)
                for R in RS:
                    st = max(1, int(round(R / g.cell / 3)))
                    sb, tied, _ = binarise(g.smooth_k(Fk, R))
                    for rm in RMULTS:
                        rc = int(max(1, round(rm * R / g.cell)))
                        for gname, orients in geometries(rc).items():
                            I, E, _, sem = triple_read(sb, orients, st)
                            acc.setdefault(f"{nm}|{nb}|{R}|{gname}_r{rm:g}",
                                           []).append([I, E, sem, tied])
                    del sb
                del Fk
                if np.isfinite(nb):
                    del d
            del lam0
        del base
        json.dump(dict(N=N, L=L, V=(L / 1000.) ** 3, n_real=r + 1, nbars=NBARS,
                       Rs=RS, rmults=list(RMULTS), cell=g.cell, data=acc),
                  open(os.path.join(HERE, 'sky_forecast_shotnoise.json'), 'w'),
                  indent=1, default=float)
        log(f"  realisation {r+1}/{n_real} in {time.time()-t0:.1f}s")
    return acc


def report(path=None):
    d = json.load(open(path or os.path.join(HERE, 'sky_forecast_shotnoise.json')))
    acc = d['data']
    n = d['n_real']
    log("\n" + "=" * 100)
    log(f"PAIRED SHOT-NOISE TERM   mean[ E(nbar) - E(inf) ] +- SEM   over {n} realisations")
    log("=" * 100)
    out = {}
    for nm in ('F0', 'WHITE', '2LPT'):
        tag = {'F0': 'VALVE CONFIG: correlated, share exactly 0',
               'WHITE': 'PRODUCT state at the cell level: theorem says no minting',
               '2LPT': 'gravity'}[nm]
        log(f"\n  base = {nm}   [{tag}]")
        for R in d['Rs']:
            log(f"    R = {R:.0f} Mpc/h")
            log(f"      {'nbar':>8} {'nbar*V_R':>9} " +
                " ".join(f"{c:>17}" for c in ['equilateral_r1.5', 'folded_r1.5',
                                              'squeezed_r1.5', 'equilateral_r3']))
            for nb in d['nbars']:
                row, nvr = [], nb * (2 * np.pi) ** 1.5 * R ** 3
                for cfg in ['equilateral_r1.5', 'folded_r1.5', 'squeezed_r1.5',
                            'equilateral_r3']:
                    ka = f"{nm}|{nb}|{R}|{cfg}"
                    ki = f"{nm}|inf|{R}|{cfg}"
                    if ka not in acc or ki not in acc:
                        row.append(" " * 17); continue
                    a = np.array(acc[ka])[:, 1]
                    i = np.array(acc[ki])[:, 1]
                    dd = a - i
                    s = dd.std(ddof=1) / np.sqrt(len(dd))
                    out[(nm, nb, R, cfg)] = (dd.mean(), s, dd.std(ddof=1))
                    row.append(f"{dd.mean():9.2e}/{dd.mean()/max(s,1e-30):+5.1f}".rjust(17))
                log(f"      {nb:8.0e} {nvr:9.1f} " + " ".join(row))
    return out


if __name__ == '__main__':
    nr = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    if nr > 0:
        run(n_real=nr)
    report()
