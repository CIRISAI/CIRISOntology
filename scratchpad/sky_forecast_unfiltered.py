#!/usr/bin/env python3
"""
sky_forecast_unfiltered.py -- the measurement that decides how the GAP should be read.

Not in the pre-registration.  Added after the first sweep and disclosed as an addition,
because the sweep exposed a question the prereg did not ask.

THE QUESTION.  Every pointwise floor has EXACTLY zero whole-only share before the final
filter (gate GC: bit-identical sign pattern to its parent Gaussian, 0 cells of 56.6M), so
100 % of a floor's reading is manufactured by the smoothing.  The sweep then shows the GAP
is dominated by the floor's manufactured term, not by gravity's.  That leaves one thing
undetermined: is GRAVITY's excess intrinsic, or is it also manufactured by the filter?

THE TEST.  Read the sign triples with NO smoothing at all.  The Eulerian SPT2 arm has no
particles, no CIC and no smoothing, so at R=0 it is a genuinely unfiltered field with the
exact tree-level three-point structure.  Its Gaussian counterpart F0 reads exactly zero by
share_eq_zero_of_signSymmetric, and by gate GC the pointwise floors read the same as F0
bit for bit.  So E(SPT2, R=0) - E(F0, R=0) is gravity's UNFILTERED whole-only excess, and
no filter can be blamed for it in either direction.

The 2LPT particle arm is reported alongside, but it is NOT unfiltered -- CIC deposit is a
filter -- so it cannot answer this question and is shown only for comparison.

Usage: python sky_forecast_unfiltered.py [N] [L] [n_real]
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_forecast import (Grid, build_gravity, binarise, geometries, triple_read,   # noqa
                          side_lengths, sigma_R_gauss, F32, log)


def run(N=384, L=1920.0, n_real=4, seed0=20260805, seps=(2, 6, 16), stride=2):
    g = Grid(N, L)
    log("=" * 96)
    log(f"UNFILTERED READING  N={N} L={L} cell={g.cell:.2f} Mpc/h  "
        f"V={(L/1000.)**3:.3f} (Gpc/h)^3  n_real={n_real}")
    log(f"  sigma of the linear field at the grid scale: {sigma_R_gauss(g.cell):.3f}")
    log("=" * 96)
    acc = {}
    for r in range(n_real):
        t0 = time.time()
        w = np.random.default_rng(seed0 + 1000 * r).standard_normal((N,) * 3).astype(F32)
        wk = g.fwd(w); del w
        arms = build_gravity(g, wk, want_sectors=True, want_za=False)
        arms.pop('_mono_viol')
        Ptar = g.measure_P(arms['2LPT'])
        wn = g.white_bin_power(wk)
        arms['F0'] = g.gauss_from_white(wk, g.P_on_grid(Ptar / np.maximum(wn, 1e-30)))
        del wk
        for nm in list(arms.keys()):
            sb, tied, _ = binarise(arms.pop(nm))
            for rc in seps:
                for gname, orients in geometries(rc).items():
                    I, E, _, sem = triple_read(sb, orients, stride)
                    acc.setdefault((rc, gname, nm), []).append((I, E, sem, tied))
            del sb
        del arms
        log(f"  realisation {r+1}/{n_real} in {time.time()-t0:.1f}s")

    out = dict(N=N, L=L, V=(L / 1000.) ** 3, n_real=n_real, seps=list(seps), stride=stride,
               cell=g.cell, sigma_grid=sigma_R_gauss(g.cell),
               data={f"{k[0]}|{k[1]}|{k[2]}": v for k, v in acc.items()})
    json.dump(out, open(os.path.join(HERE, f'sky_forecast_unfiltered_L{int(L)}.json'), 'w'),
              indent=1, default=float)

    log("\n  E with NO FILTER of any kind.  F0/F1/F2 all read the same thing here (gate GC),")
    log("  and its true value is EXACTLY 0 -- so E(arm) - E(F0) is intrinsic, not manufactured.")
    arms = ['SPT2', 'SPT2_LOCAL', 'SPT2_SHIFT', 'SPT2_TIDAL', 'LIN', '2LPT', 'F0']
    for rc in seps:
        log(f"\n  separation {rc} cells = {rc*g.cell:.0f} Mpc/h")
        log(f"    {'geom':>13} " + " ".join(f"{a:>13}" for a in arms))
        for gname in ['equilateral', 'folded', 'orthogonal', 'squeezed']:
            row = [f"    {gname:>13} "]
            for a in arms:
                k = (rc, gname, a)
                if k not in acc:
                    row.append(f"{'-':>13} "); continue
                v = np.array(acc[k])[:, 1]
                z = v.mean() / max(v.std(ddof=1) / np.sqrt(len(v)), 1e-30)
                row.append(f"{v.mean():9.2e}/{z:+5.1f}"[:13].rjust(13) + " ")
            log("".join(row))
        # the excess over the exact-zero Gaussian, paired
        log(f"    {'-- minus F0':>13} " + " ".join(f"{a:>13}" for a in arms[:-1]))
        row = [f"    {'(paired z)':>13} "]
        for a in arms[:-1]:
            k = (rc, 'equilateral', a)
            if k not in acc:
                row.append(f"{'-':>13} "); continue
            d = np.array(acc[k])[:, 1] - np.array(acc[(rc, 'equilateral', 'F0')])[:, 1]
            z = d.mean() / max(d.std(ddof=1) / np.sqrt(len(d)), 1e-30)
            row.append(f"{d.mean():9.2e}/{z:+5.1f}"[:13].rjust(13) + " ")
        log("".join(row) + "   [equilateral only]")
    return out


if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 384
    L = float(sys.argv[2]) if len(sys.argv) > 2 else 1920.0
    nr = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    run(N, L, nr)
