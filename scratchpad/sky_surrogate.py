#!/usr/bin/env python3
"""
sky_surrogate.py -- STAGE 3 (re-specified): the phase-randomised surrogate that supplies
G10's denominator, per AMENDMENT 3.

One surrogate per mock realisation: Fourier-transform the mock's own gridded masked delta,
replace every phase with a uniform random phase while KEEPING the amplitude, transform back,
and run the identical downstream pipeline (mask, smoothing, quantile binning, IPF).

Verified before use (Amendment 3 A3.2): PR preserves |F| to 2.3e-13, and smoothing commutes
with PR to 1.8e-07 because both are diagonal in Fourier.  The lognormal control failed exactly
because a monotone per-cell map does NOT commute with smoothing.

A3.6 requires this construction to pass its own diagnostic before G10 is scored:
    sigma(surrogate) ~ sigma(mock)          two-point structure survived
    smoothed skewness(surrogate) ~ 0        the phases really are destroyed
The second is the check that caught the previous control at +1.67.

BLINDING: reads Patchy mocks only.  Never the real catalogue.
"""
import json
import os
import sys
import tarfile
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_realdata import (F32, sky_to_cart, quantile_labels, connected_info,   # noqa: E402
                          configs, _coarse2, log)
from sky_stage2 import CapGeometry, RS, BS, OCC_MIN, _load_ascii, DATA         # noqa: E402
from sky_pilot import route_B2                                                 # noqa: E402


def phase_randomise(g, field, seed):
    """Keep |F(k)|, replace every phase.  Hermitian symmetry is preserved automatically by
    working in the rfft half-space and letting irfftn impose reality."""
    F = g.fwd(field)
    rng = np.random.default_rng(seed)
    ph = np.exp(1j * rng.uniform(0.0, 2.0 * np.pi, F.shape)).astype(np.complex64)
    F = (np.abs(F) * ph).astype(np.complex64)
    F[0, 0, 0] = abs(F[0, 0, 0])
    out = g.inv(F).astype(F32)
    del F, ph
    return out


def measure_pair(geo, pos, wt, seed, bs=BS, rs=RS, rmult=1.5):
    """Measure the mock AND its phase-randomised surrogate through the identical pipeline."""
    g = geo.g
    n_gal = g.deposit(pos, wt)
    alpha = float(n_gal.sum()) / geo.tot_ran
    exp = alpha * geo.exp_ran
    delta = np.zeros_like(n_gal)
    np.divide(n_gal - exp, exp, out=delta, where=geo.mask)
    del n_gal, exp
    dm = (delta * geo.m32).astype(F32)
    del delta
    # PHASE RANDOMISATION DELOCALISES THE POWER.  delta*M carries all its variance inside the
    # footprint; PR spreads that same total power uniformly over the whole grid, so restricting
    # back to the footprint recovers only a fraction f of it and sigma falls by sqrt(f).
    # Measured: ratio 0.3887 against sqrt(0.154) = 0.3924 -- the mechanism exactly.
    # The correction is the single principled factor 1/sqrt(f), NOT a tuned one: it restores the
    # in-footprint variance without touching the phases or the spectral shape.
    fmask = float(geo.m32.mean())
    surro = (phase_randomise(g, dm, seed) / np.sqrt(fmask)) * geo.m32
    out = {}
    for tag, fld in (('mock', dm), ('surr', surro)):
        F = g.fwd(fld)
        rec = {}
        for R in rs:
            num = g.smooth_k(F, R)
            ok = geo.ok[R]
            sm = np.zeros_like(num)
            np.divide(num, geo.den[R], out=sm, where=ok)
            del num
            v = sm[ok]
            r = {'sigma': float(v.std()),
                 'skew': float(((v - v.mean()) ** 3).mean() / v.std() ** 3), 'b': {}}
            del v
            stride = max(1, int(round(R / g.cell / 3)))
            for b in bs:
                occ = geo.occupancy(R, b)
                if occ <= OCC_MIN:
                    r['b'][b] = {n: dict(occupancy=occ, occupancy_pass=False)
                                 for n in configs(R, g.cell, rmult)}
                    continue
                lab, _ = quantile_labels(sm, ok, b)
                sl = tuple(slice(0, ok.shape[i], stride) for i in range(3))
                ls = lab[sl]
                bb = {}
                for name, orients in configs(R, g.cell, rmult).items():
                    hs = np.zeros((b, b, b)); nt = 0
                    for (d1, d2) in orients:
                        mm = (ok[sl]
                              & np.roll(ok, (-d1[0], -d1[1], -d1[2]), (0, 1, 2))[sl]
                              & np.roll(ok, (-d2[0], -d2[1], -d2[2]), (0, 1, 2))[sl])
                        a1 = np.roll(lab, (-d1[0], -d1[1], -d1[2]), (0, 1, 2))[sl]
                        a2 = np.roll(lab, (-d2[0], -d2[1], -d2[2]), (0, 1, 2))[sl]
                        hs += np.bincount(((ls.astype(np.int64) * b + a1) * b + a2)[mm],
                                          minlength=b ** 3).astype(np.float64).reshape(b, b, b)
                        nt += int(mm.sum())
                        del a1, a2, mm
                    ci = connected_info(hs)
                    bb[name] = dict(occupancy=occ, occupancy_pass=True, n_triples=nt,
                                    I=ci['I'], cert=ci['cert'],
                                    E=float(route_B2(_coarse2(hs / hs.sum(), b).ravel())[1]))
                r['b'][b] = bb
                del lab, ls
            rec[R] = r
            del sm
        out[tag] = rec
        del F
    del dm, surro
    return out


def run(cap, nmax=128, seed0=20260801, out=None):
    geo = CapGeometry(cap)
    tf = tarfile.open(f"{DATA}/Patchy-Mocks-DR12{cap}-COMPSAM_V6C.tar.gz", 'r|gz')
    res, t0 = [], time.time()
    for i, m in enumerate(tf):
        if i >= nmax:
            break
        raw = tf.extractfile(m).read()
        a = _load_ascii(raw, 8); del raw
        sel = a[:, 6] > 0.5
        pos = sky_to_cart(a[sel, 0], a[sel, 1], a[sel, 2]).astype(np.float32)
        wt = a[sel, 7].astype(np.float64)
        del a
        r = measure_pair(geo, pos, wt, seed0 + 1000 * i)
        del pos, wt
        r['name'] = m.name
        r['seed'] = seed0 + 1000 * i
        res.append(r)
        if out and (len(res) % 8 == 0 or len(res) == nmax):
            json.dump(dict(cap=cap, n=len(res), rs=RS, bs=BS, seed0=seed0, res=res),
                      open(out, 'w'), default=float)
        if len(res) % 8 == 0:
            log(f"    [{cap}] {len(res)}/{nmax}  {(time.time()-t0)/len(res):.1f}s/mock")
    tf.close()
    return geo, res


if __name__ == '__main__':
    cap = sys.argv[1] if len(sys.argv) > 1 else 'SGC'
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 128
    op = sys.argv[3] if len(sys.argv) > 3 else f"{HERE}/sky_surrogate_{cap}.json"
    log(f"SURROGATE RUN  cap={cap}  n={n}")
    g, r = run(cap, n, out=op)
    R0 = RS[0]
    sm = np.array([x['mock'][R0]['sigma'] for x in r])
    ss = np.array([x['surr'][R0]['sigma'] for x in r])
    km = np.array([x['mock'][R0]['skew'] for x in r])
    ks = np.array([x['surr'][R0]['skew'] for x in r])
    log(f"\n  A3.6 DIAGNOSTIC at R={R0:.0f}:")
    log(f"    sigma  mock {sm.mean():.4f}   surrogate {ss.mean():.4f}   "
        f"ratio {ss.mean()/sm.mean():.4f}  -> "
        f"{'PASS' if abs(ss.mean()/sm.mean()-1) < 0.05 else 'FAIL'}")
    log(f"    skew   mock {km.mean():+.4f}  surrogate {ks.mean():+.4f}          -> "
        f"{'PASS' if abs(ks.mean()) < 0.15 else 'FAIL'}   "
        f"[previous control read +1.6688 here]")
