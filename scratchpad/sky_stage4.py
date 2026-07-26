#!/usr/bin/env python3
"""
sky_stage4.py -- STAGE 4: the two gates that ask whether the statistic is measuring anything
the pair structure has not already fixed.  Run on MOCKS at analysis resolution.

G1  LP PAIR-PINNING (kappa-edge, 3026a68).  Over EVERY distribution carrying the measured
    FINE (b' = 2b) pair marginals, how far can the coarse sign-triple moment tau move?  The LP
    is exact and needs no surrogate, no null, no IPF and no estimator.  A narrow interval means
    the reading is FORCED by pair structure and the arm is VOID.
    Pre-registered expectation (SKY_REALDATA_PREREG section 3.2): PASS, because kappa-edge
    identified the mechanism as near-DETERMINISM of the conditional support and measured that a
    Gaussian triple carrying the same pair correlations is NOT pinned (width 0.797), while a
    noise-free logistic map is (width 0.000).  A galaxy field smoothed at 15 Mpc/h is nowhere
    near deterministic.

G2  BINMINT at analysis resolution.  IPF the fine (b' = 2b) histogram onto its pair marginals
    to get q -- all the fine pair structure, NO order-3 content -- then merge to the analysis
    binning and read what is left.  Whatever q gives is manufactured by coarse-graining alone.
    On the mock campaign this cost 14 % of the deliverable at R = 10 and removed R = 25.

BLINDING: mocks only.  Never the real catalogue.
"""
import json
import os
import sys
import tarfile
import time

import numpy as np
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_realdata import (F32, sky_to_cart, quantile_labels, connected_info,   # noqa: E402
                          configs, _coarse2, log)
from sky_stage2 import CapGeometry, RS, OCC_MIN, _load_ascii, DATA            # noqa: E402
from sky_pilot import pairwise_maxent, route_B2                               # noqa: E402


def coarse_sign_vector(bp):
    """sigma(s) = product over axes of (+1 if the level is in the upper half else -1).
    Linear in the distribution, which is what makes the LP valid."""
    i = np.arange(bp ** 3)
    a0, a1, a2 = i // (bp * bp), (i // bp) % bp, i % bp
    h = bp // 2
    return (np.where(a0 >= h, 1.0, -1.0) * np.where(a1 >= h, 1.0, -1.0)
            * np.where(a2 >= h, 1.0, -1.0))


def lp_interval(p_fine, bp):
    """min/max of the coarse sign-triple moment over the marginal polytope of p_fine."""
    p = np.asarray(p_fine, float).ravel(); p = p / p.sum()
    n = bp ** 3
    s = coarse_sign_vector(bp)
    P = p.reshape(bp, bp, bp)
    idx = np.arange(n)
    a0, a1, a2 = idx // (bp * bp), (idx // bp) % bp, idx % bp
    rows, rhs = [], []
    for ax, (u, v) in enumerate([(a0, a1), (a0, a2), (a1, a2)]):
        tgt = P.sum(axis=[2, 1, 0][ax])
        for i in range(bp):
            for j in range(bp):
                r = np.zeros(n); r[(u == i) & (v == j)] = 1.0
                rows.append(r); rhs.append(tgt[i, j])
    rows.append(np.ones(n)); rhs.append(1.0)
    A, bq = np.array(rows), np.array(rhs)
    lo = linprog(s, A_eq=A, b_eq=bq, bounds=(0, 1), method='highs')
    hi = linprog(-s, A_eq=A, b_eq=bq, bounds=(0, 1), method='highs')
    if not (lo.success and hi.success):
        return None
    tau = float(s @ p)
    return dict(tau=tau, lo=float(lo.fun), hi=float(-hi.fun),
                width=float(-hi.fun - lo.fun))


def hist_at(geo, sm, ok, b, R, geom, stride, rmult=1.5):
    lab, _ = quantile_labels(sm, ok, b)
    sl = tuple(slice(0, ok.shape[i], stride) for i in range(3))
    ls = lab[sl]
    hs = np.zeros((b, b, b)); nt = 0
    for (d1, d2) in configs(R, geo.g.cell, rmult)[geom]:
        mm = (ok[sl] & np.roll(ok, (-d1[0], -d1[1], -d1[2]), (0, 1, 2))[sl]
              & np.roll(ok, (-d2[0], -d2[1], -d2[2]), (0, 1, 2))[sl])
        a1 = np.roll(lab, (-d1[0], -d1[1], -d1[2]), (0, 1, 2))[sl]
        a2 = np.roll(lab, (-d2[0], -d2[1], -d2[2]), (0, 1, 2))[sl]
        hs += np.bincount(((ls.astype(np.int64) * b + a1) * b + a2)[mm],
                          minlength=b ** 3).astype(np.float64).reshape(b, b, b)
        nt += int(mm.sum())
        del a1, a2, mm
    del lab, ls
    return hs, nt


def run(cap, n_mock=8, bs=(4, 6), geoms=('folded', 'equilateral'), seed0=20260901):
    geo = CapGeometry(cap)
    tf = tarfile.open(f"{DATA}/Patchy-Mocks-DR12{cap}-COMPSAM_V6C.tar.gz", 'r|gz')
    acc = {}
    t0 = time.time()
    for i, m in enumerate(tf):
        if i >= n_mock:
            break
        raw = tf.extractfile(m).read()
        a = _load_ascii(raw, 8); del raw
        sel = a[:, 6] > 0.5
        pos = sky_to_cart(a[sel, 0], a[sel, 1], a[sel, 2]).astype(np.float32)
        wt = a[sel, 7].astype(np.float64); del a
        g = geo.g
        n_gal = g.deposit(pos, wt); del pos, wt
        alpha = float(n_gal.sum()) / geo.tot_ran
        exp = alpha * geo.exp_ran
        delta = np.zeros_like(n_gal)
        np.divide(n_gal - exp, exp, out=delta, where=geo.mask)
        del n_gal, exp
        F = g.fwd((delta * geo.m32).astype(F32)); del delta
        for R in RS:
            num = g.smooth_k(F, R); ok = geo.ok[R]
            sm = np.zeros_like(num); np.divide(num, geo.den[R], out=sm, where=ok); del num
            stride = max(1, int(round(R / g.cell / 3)))
            for b in bs:
                if geo.occupancy(R, b) <= OCC_MIN:
                    continue
                bp = 2 * b
                if geo.occupancy(R, bp) <= 20:      # fine histogram must still be populated
                    continue
                for geom in geoms:
                    hf, ntf = hist_at(geo, sm, ok, bp, R, geom, stride)
                    pf = hf / hf.sum()
                    lp = lp_interval(pf, bp)
                    # G2: pair-maxent of the FINE histogram, merged to the analysis binning
                    q, err, _ = pairwise_maxent(pf, iters=20000, tol=1e-13)
                    ha, nta = hist_at(geo, sm, ok, b, R, geom, stride)
                    pa = ha / ha.sum()
                    ci_data = connected_info(ha)
                    # merge fine -> analysis binning (quantile bins, so the merge is exact)
                    fac = bp // b
                    qa = q.reshape(b, fac, b, fac, b, fac).sum(axis=(1, 3, 5))
                    ci_manuf = connected_info(qa / qa.sum())
                    E_data = float(route_B2(_coarse2(pa, b).ravel())[1])
                    E_manuf = float(route_B2(_coarse2(qa / qa.sum(), b).ravel())[1])
                    acc.setdefault(f"{R}|{b}|{geom}", []).append(dict(
                        lp_tau=lp['tau'], lp_lo=lp['lo'], lp_hi=lp['hi'], lp_width=lp['width'],
                        n_triples=ntf, I_data=ci_data['I'], I_manuf=ci_manuf['I'],
                        E_data=E_data, E_manuf=E_manuf,
                        cert=max(ci_data['cert'], ci_manuf['cert']), ipf_err=float(err)))
                    del hf, ha, q, qa
            del sm
        del F
        log(f"    [{cap}] mock {i+1}/{n_mock}  {(time.time()-t0)/(i+1):.0f}s each")
    tf.close()
    return geo, acc


if __name__ == '__main__':
    cap = sys.argv[1] if len(sys.argv) > 1 else 'SGC'
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    log(f"STAGE 4  cap={cap}  n_mock={n}")
    geo, acc = run(cap, n)
    out = {}
    log("\n  G1 LP PAIR-PINNING -- is tau forced by the fine pair marginals?")
    log("  %-6s %-3s %-12s %10s %10s %10s %10s %9s %8s"
        % ("R", "b", "geom", "tau", "LP min", "LP max", "width", "sem(tau)", "verdict"))
    for k, v in sorted(acc.items()):
        R, b, geom = k.split('|')
        tau = np.array([x['lp_tau'] for x in v])
        w = np.mean([x['lp_width'] for x in v])
        sem = tau.std(ddof=1) / np.sqrt(len(tau))
        ok = (w / 2.0) > 5 * sem
        out[k] = dict(width=w, sem=float(sem), passed=bool(ok))
        log("  %-6s %-3s %-12s %10.5f %10.5f %10.5f %10.5f %9.2e %8s"
            % (R, b, geom, tau.mean(), np.mean([x['lp_lo'] for x in v]),
               np.mean([x['lp_hi'] for x in v]), w, sem,
               "PASS" if ok else "VOID"))
    log("\n  G2 BINMINT at analysis resolution -- what the coarse-graining mints by itself")
    log("  %-6s %-3s %-12s %11s %11s %9s %11s %11s %8s"
        % ("R", "b", "geom", "I_data", "I_manuf", "manuf/I", "E_data", "E_manuf", "cert"))
    for k, v in sorted(acc.items()):
        R, b, geom = k.split('|')
        Id = np.mean([x['I_data'] for x in v]); Im = np.mean([x['I_manuf'] for x in v])
        out[k].update(I_data=Id, I_manuf=Im, frac=Im / Id if Id else np.nan,
                      E_data=float(np.mean([x['E_data'] for x in v])),
                      E_manuf=float(np.mean([x['E_manuf'] for x in v])),
                      cert=float(max(x['cert'] for x in v)))
        log("  %-6s %-3s %-12s %11.4e %11.4e %9.4f %11.3e %11.3e %8.1e"
            % (R, b, geom, Id, Im, Im / Id if Id else np.nan,
               out[k]['E_data'], out[k]['E_manuf'], out[k]['cert']))
    json.dump(out, open(f"{HERE}/sky_stage4_{cap}.json", 'w'), indent=1, default=float)
