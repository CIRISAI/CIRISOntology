#!/usr/bin/env python3
"""
sky_forecast_binmint.py -- does the MEDIAN SPLIT itself mint b=2 share from pure
fine-grained pair structure?  The kappa-edge dependency, tested at THIS pipeline's
resolution instead of left pending.

In SKY_FORECAST_RESULTS.md's "Scope, second part" I wrote that I could not build this
control, because every null in the forecast is either Gaussian or a monotone map of one and
both are already forced to zero by theorem.  That was wrong, and this file is the retraction:
the control is constructible, it is cheap, and it is a pure histogram computation.

THE CONSTRUCTION.
  1. Smooth the field at R and bin it into b QUANTILE bins (b even), for b = 4, 8, 16, 32.
  2. Build the exact (b,b,b) triple histogram at a pre-declared geometry.
  3. IPF onto the pair-marginal constraints -> q, the FINE-GRAINED PAIRWISE-MAXENT state.
     By construction q carries all of the field's fine pair structure and NO order-3 content.
     Carry the pilot's KL certificate |share_H - share_KL| on every solve.
  4. Coarse-grain q by merging the lower b/2 bins and the upper b/2.  Because the bins are
     quantile bins, that merge IS the median split, exactly.
  5. Read the b=2 sign-triple excess E of the coarse-grained q.

If E(coarse-grained q) != 0, then the median split manufactures b=2 share out of two-point
structure alone, because q has none by construction.  That is the H-MANUFACTURED hypothesis,
adjudicated on my own fields at my own resolution.

PRE-DECLARED, before running (this file was written and committed before it was executed):
  * On a GAUSSIAN field the answer must be EXACTLY 0.  A Gaussian's quantile binning is
    sign-symmetric, its pair-maxent is sign-symmetric too, and the sign-symmetry lemma forces
    the merged b=2 state to zero.  This is the gate: a nonzero reading there is a bug, not a
    discovery.
  * On GRAVITY the answer is unknown to me.  I expect a small nonzero value, because the
    field is skewed and nothing forces the coarse-grained pair-maxent to stay pair-maxent.
  * The number that matters is E_manufactured against the measured GAP at the same R:
    if |E_manufactured| << |GAP| the forecast is safe; if comparable, the forecast's
    continuum interpretation is not available and the GAP must be re-read against this
    surrogate rather than against the pointwise floors.

Usage: python sky_forecast_binmint.py [n_real]
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_pilot import pairwise_maxent, share3_ref, route_B2              # noqa: E402
from sky_forecast import (Grid, build_gravity, binarise, geometries,      # noqa: E402
                          triple_read, tune_floor, make_rank_T, rank_table, F32, log)

BS = [4, 8, 16, 32]
RS = [10.0, 25.0]
GEOMS = ['equilateral', 'folded', 'squeezed']


def quantile_bin(f, b, sub=1 << 22, seed=5):
    """Quantile bins of the field.  For even b the merge of the lower b/2 and upper b/2 bins
    is EXACTLY the median split, which is what makes step 5 legitimate."""
    rng = np.random.default_rng(seed)
    v = f.ravel()
    s = np.sort(v[rng.integers(0, v.size, size=min(sub, v.size))].astype(np.float64))
    edges = np.quantile(s, np.arange(1, b) / b)
    return np.searchsorted(edges, f, side='right').astype(np.uint8)


def triple_hist_b(lab, d1, d2, stride, b):
    N = lab.shape[0]
    i = np.arange(0, N, stride)
    a = lab[np.ix_(i, i, i)].astype(np.int64)
    x = lab[np.ix_((i + d1[0]) % N, (i + d1[1]) % N, (i + d1[2]) % N)].astype(np.int64)
    y = lab[np.ix_((i + d2[0]) % N, (i + d2[1]) % N, (i + d2[2]) % N)].astype(np.int64)
    idx = (a * b + x) * b + y
    return np.bincount(idx.ravel(), minlength=b ** 3).astype(np.float64).reshape(b, b, b)


def coarse2(p, b):
    """Merge the lower b/2 and upper b/2 bins on each axis == the median split."""
    h = b // 2
    q = p.reshape(2, h, 2, h, 2, h).sum(axis=(1, 3, 5))
    return q / q.sum()


def run(N=384, L=768.0, n_real=3, seed0=20261101, out='sky_forecast_binmint.json'):
    g = Grid(N, L)
    log("=" * 100)
    log(f"BINARIZATION-MINTING TEST  N={N} L={L} cell={g.cell:.2f} Mpc/h  n_real={n_real}")
    log("  Does merging a FINE-GRAINED PAIRWISE-MAXENT state down to the median split")
    log("  manufacture b=2 sign-triple excess?  q has no order-3 content by construction.")
    log("=" * 100)
    acc = {}
    for r in range(n_real):
        t0 = time.time()
        w = np.random.default_rng(seed0 + 1000 * r).standard_normal((N,) * 3).astype(F32)
        wk = g.fwd(w); del w
        arms = build_gravity(g, wk, want_sectors=False, want_za=False)
        arms.pop('_mono_viol')
        Ptar = g.measure_P(arms['2LPT'])
        wn = g.white_bin_power(wk)
        arms['F0'] = g.gauss_from_white(wk, g.P_on_grid(Ptar / np.maximum(wn, 1e-30)))
        tabR = rank_table(arms['2LPT'])
        arms['F2'], _, _, _ = tune_floor(g, wk, Ptar, lambda gf: make_rank_T(tabR), wn=wn)
        del wk
        for nm in ('2LPT', 'F0', 'F2'):
            Fk = g.fwd(arms[nm])
            for R in RS:
                st = max(1, int(round(R / g.cell / 3)))
                sm = g.smooth_k(Fk, R)
                sb, _, _ = binarise(sm)
                rc = int(max(1, round(1.5 * R / g.cell)))
                geo = geometries(rc)
                # the field's OWN b=2 reading, for scale
                for gname in GEOMS:
                    _, E_field, _, _ = triple_read(sb, geo[gname], st)
                    acc.setdefault(f"{nm}|{R}|{gname}|field", []).append(E_field)
                del sb
                for b in BS:
                    lab = quantile_bin(sm, b)
                    for gname in GEOMS:
                        d1, d2 = geo[gname][0]          # one orientation: no mixture here
                        p = triple_hist_b(lab, d1, d2, st, b)
                        p = p / p.sum()
                        q, err, _ = pairwise_maxent(p, iters=20000, tol=1e-13)
                        m = p > 0
                        sH = float(-(q[q > 0] * np.log(q[q > 0])).sum()
                                   + (p[m] * np.log(p[m])).sum())
                        sKL = float((p[m] * (np.log(p[m])
                                             - np.log(np.maximum(q[m], 1e-300)))).sum())
                        cq = coarse2(q, b)
                        cp = coarse2(p, b)
                        acc.setdefault(f"{nm}|{R}|{gname}|b{b}", []).append(dict(
                            E_manuf=float(route_B2(cq.ravel())[1]),
                            I_manuf=float(share3_ref(cq.ravel())),
                            E_data=float(route_B2(cp.ravel())[1]),
                            I_data=float(share3_ref(cp.ravel())),
                            share_fine=sKL, cert=abs(sH - sKL), ipf_err=float(err)))
                    del lab
                del sm
            del Fk
        del arms
        json.dump(dict(N=N, L=L, n_real=r + 1, bs=BS, Rs=RS, geoms=GEOMS, data=acc),
                  open(os.path.join(HERE, out), 'w'),
                  indent=1, default=float)
        log(f"  realisation {r+1}/{n_real} in {time.time()-t0:.1f}s")
    return acc


def report():
    d = json.load(open(os.path.join(HERE, 'sky_forecast_binmint.json')))
    acc = d['data']
    log("\n" + "=" * 100)
    log("E_manuf = the b=2 sign-triple excess of a FINE-GRAINED PAIRWISE-MAXENT state,")
    log("merged to the median split.  q has NO order-3 content, so any nonzero value here is")
    log("manufactured by the coarse-graining alone.   n_real = %d" % d['n_real'])
    log("=" * 100)
    worst_cert, n = 0.0, d['n_real']
    log("  Each entry is mean +- SEM over realisations, with t = mean/SEM.  A SINGLE")
    log("  realisation cannot decide this: the surrogate reproduces the field's own sampled")
    log("  pair marginals, so E_manuf tracks E_field's noise realisation by realisation and")
    log("  only the ENSEMBLE MEAN separates manufacturing from noise propagation.")
    for nm in ('F0', 'F2', '2LPT'):
        tag = {'F0': 'GAUSSIAN -- ensemble mean must be 0 (sign-symmetry lemma). THE GATE.',
               'F2': 'rank-matched pointwise floor -- a monotone map of a Gaussian, also 0',
               '2LPT': 'GRAVITY -- the number that matters'}[nm]
        log(f"\n  {nm}   [{tag}]")
        for R in d['Rs']:
            for gname in d['geoms']:
                fk = f"{nm}|{R}|{gname}|field"
                if fk not in acc:
                    continue
                fv = np.array(acc[fk])
                sf = fv.std(ddof=1) / np.sqrt(len(fv)) if len(fv) > 1 else np.nan
                log(f"    R={R:5.0f} {gname:>12}   E_field = {fv.mean():10.3e} "
                    f"+- {sf:7.1e} (t={fv.mean()/max(sf,1e-30):+5.1f})")
                for b in d['bs']:
                    k = f"{nm}|{R}|{gname}|b{b}"
                    if k not in acc:
                        continue
                    e = np.array([x['E_manuf'] for x in acc[k]])
                    r = fv - e                     # the part NOT explained by fine pairs
                    worst_cert = max(worst_cert, max(x['cert'] for x in acc[k]))
                    se = e.std(ddof=1) / np.sqrt(len(e)) if len(e) > 1 else np.nan
                    sr = r.std(ddof=1) / np.sqrt(len(r)) if len(r) > 1 else np.nan
                    log(f"        b={b:3d}  E_manuf = {e.mean():10.3e} +- {se:7.1e} "
                        f"(t={e.mean()/max(se,1e-30):+5.1f}) | "
                        f"E_field - E_manuf = {r.mean():10.3e} +- {sr:7.1e} "
                        f"(t={r.mean()/max(sr,1e-30):+5.1f})")
    log(f"\n  worst IPF certificate |share_H - share_KL| anywhere: {worst_cert:.2e}")


if __name__ == '__main__':
    nr = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    sd = int(sys.argv[2]) if len(sys.argv) > 2 else 20261101
    ou = sys.argv[3] if len(sys.argv) > 3 else 'sky_forecast_binmint.json'
    if nr > 0:
        run(n_real=nr, seed0=sd, out=ou)
    if ou == 'sky_forecast_binmint.json':
        report()
