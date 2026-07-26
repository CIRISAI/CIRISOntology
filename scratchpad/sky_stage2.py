#!/usr/bin/env python3
"""
sky_stage2.py -- STAGE 2: the floor model on the MultiDark-Patchy suite, and the G10 mock
closure test that is the pre-registered go/no-go.

Mocks are STREAM-read from the tarballs (Amendment 1): tarfile 'r|gz' yields members
sequentially without seeking and without expanding to disk.  Full expansion would be
~150-200 GB against 87 GB free.

Geometry is CACHED per cap.  The survey mask and its smoothed denominators W*M come from the
randoms, which are shared by every realisation, so they are built once.  Per mock only the
galaxy deposit and 1 forward + n_R inverse FFTs are paid.

BLINDING: this file never touches the real galaxy catalogue.  It reads Patchy mocks and the
Patchy randoms only.

Patchy mock columns : RA DEC z logM* nbar bias veto fibre_collision
Patchy random columns: RA DEC z nbar bias veto fibre_collision
Selection, standard for this suite: veto == 1, weight = fibre-collision weight.
"""
import io
import json
import os
import sys
import tarfile
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_realdata import (DATA, F32, SurveyGrid, sky_to_cart, quantile_labels,   # noqa
                          triple_hist, connected_info, configs, _coarse2, log)
from sky_pilot import route_B2                                                    # noqa

RS = [15.0, 10.0]          # primary, stressed secondary (Amendment 1)
BS = [4, 6, 8]            # the occupancy gate decides per cap and per scale, not by hand
OCC_MIN = 100.0
CELL = 6.0
DEN_THR = 0.99
MASK_FRAC = 0.80
MASK_SMOOTH = 8.0        # Mpc/h; footprint defined on the smoothed random field


def _load_ascii(raw, ncol):
    a = np.loadtxt(io.BytesIO(raw), usecols=range(ncol))
    return a


class CapGeometry:
    """Grid, mask and smoothed mask-denominators for one cap.  Built once, reused by every
    realisation -- this is what makes the suite affordable."""

    def __init__(self, cap, cell=CELL, rs=RS):
        t0 = time.time()
        p = f"{DATA}/Patchy-Mocks-Randoms-DR12{cap}-COMPSAM_V6C_x50.tar.gz"
        tf = tarfile.open(p, 'r|gz')
        m = next(iter(tf))
        raw = tf.extractfile(m).read()
        tf.close()
        a = _load_ascii(raw, 7)
        del raw
        sel = a[:, 5] > 0.5                       # veto
        ra, dec, z, w = a[sel, 0], a[sel, 1], a[sel, 2], a[sel, 6]
        del a
        self.cap = cap
        self.n_ran_obj = int(sel.sum())
        pos = sky_to_cart(ra, dec, z).astype(np.float32)
        del ra, dec, z
        self.g = SurveyGrid(pos, cell=cell)
        self.n_ran = self.g.deposit(pos, w)
        del pos, w
        # STAGE 2 FINDING: thresholding the RAW deposited random count is only a valid
        # footprint estimator when the randoms are dense.  With the x10 suite (~0.1 randoms
        # per cell) the mask degenerates to speckle and W*M > 0.99 is essentially never
        # satisfied -- valid fraction collapsed to 0.001 at R=15 against 0.104 on the
        # 50x-denser BOSS randoms.  Fixed two ways: the x50 suite (matching the data's random
        # density), and defining the footprint on a SMOOTHED random field, which is what a
        # footprint means and which is independent of random sparsity.
        exp0 = self.g.smooth_k(self.g.fwd(self.n_ran), MASK_SMOOTH)
        thr = MASK_FRAC * np.median(exp0[exp0 > 0])
        self.mask = (exp0 > thr)
        del exp0
        self.m32 = self.mask.astype(F32)
        self.den, self.ok, self.n_indep = {}, {}, {}
        Fm = self.g.fwd(self.m32)
        for R in rs:
            d = self.g.smooth_k(Fm, R)
            o = d > DEN_THR
            self.den[R], self.ok[R] = d, o
            self.n_indep[R] = float(o.sum()) * cell ** 3 / ((2 * np.pi) ** 1.5 * R ** 3)
        del Fm
        self.tot_ran = float(self.n_ran.sum())
        log(f"  [{cap}] grid {self.g.N} = {self.g.ncell/1e6:.1f}M cells; randoms "
            f"{self.n_ran_obj}; mask {self.mask.mean():.3f}; "
            + "; ".join(f"R={R:.0f}: valid {self.ok[R].mean():.3f}, n_indep {self.n_indep[R]:.0f}"
                        for R in rs)
            + f"   [{time.time()-t0:.0f}s]")

    def occupancy(self, R, b):
        return self.n_indep[R] / b ** 3

    def measure(self, pos, wt, bs=BS, rs=RS, rmult=1.5, run_lp=False):
        g = self.g
        n_gal = g.deposit(pos, wt)
        alpha = float(n_gal.sum()) / self.tot_ran
        exp = alpha * self.n_ran
        delta = np.zeros_like(n_gal)
        np.divide(n_gal - exp, exp, out=delta, where=self.mask)
        del n_gal, exp
        F = g.fwd((delta * self.m32).astype(F32))
        del delta
        out = {}
        for R in rs:
            num = g.smooth_k(F, R)
            ok = self.ok[R]
            sm = np.zeros_like(num)
            np.divide(num, self.den[R], out=sm, where=ok)
            del num
            stride = max(1, int(round(R / g.cell / 3)))
            rec = {'sigma': float(sm[ok].std()), 'stride': stride,
                   'n_indep': self.n_indep[R], 'b': {}}
            # The valid-TRIPLE mask depends only on (R, displacement), not on b, so it is
            # built once and reused across the b ladder.  It was the dominant cost.
            cfg = configs(R, g.cell, rmult)
            sl = tuple(slice(0, ok.shape[i], stride) for i in range(3))
            tmask = {}
            for name, orients in cfg.items():
                for (d1, d2) in orients:
                    key = (d1, d2)
                    if key not in tmask:
                        tmask[key] = (ok[sl]
                                      & np.roll(ok, (-d1[0], -d1[1], -d1[2]), (0, 1, 2))[sl]
                                      & np.roll(ok, (-d2[0], -d2[1], -d2[2]), (0, 1, 2))[sl])
            for b in bs:
                lab, _ = quantile_labels(sm, ok, b)
                ls = lab[sl]
                occ = self.occupancy(R, b)
                bb = {}
                for name, orients in cfg.items():
                    if occ <= OCC_MIN:
                        bb[name] = dict(occupancy=occ, occupancy_pass=False)
                        continue
                    hs = np.zeros((b, b, b)); nt = 0
                    for (d1, d2) in orients:
                        mm = tmask[(d1, d2)]
                        a1 = np.roll(lab, (-d1[0], -d1[1], -d1[2]), (0, 1, 2))[sl]
                        a2 = np.roll(lab, (-d2[0], -d2[1], -d2[2]), (0, 1, 2))[sl]
                        idx = ((ls.astype(np.int64) * b + a1) * b + a2)[mm]
                        hs += np.bincount(idx, minlength=b ** 3).astype(
                            np.float64).reshape(b, b, b)
                        nt += int(mm.sum())
                        del a1, a2, idx
                    ci = connected_info(hs)
                    bb[name] = dict(occupancy=occ, occupancy_pass=True, n_triples=nt,
                                    I=ci['I'], cert=ci['cert'],
                                    E=float(route_B2(_coarse2(hs / hs.sum(), b).ravel())[1]))
                rec['b'][b] = bb
                del lab, ls
            del tmask
            out[R] = rec
            del sm
        del F
        return out


def stream_mocks(cap, nmax, bs=BS, rs=RS, geo=None, out_path=None, every=10):
    """Stream-read the tarball and measure each realisation.  Writes incrementally so the
    run can be stopped at any point without losing work."""
    geo = geo or CapGeometry(cap)
    p = f"{DATA}/Patchy-Mocks-DR12{cap}-COMPSAM_V6C.tar.gz"
    tf = tarfile.open(p, 'r|gz')
    res, t0 = [], time.time()
    for i, m in enumerate(tf):
        if i >= nmax:
            break
        raw = tf.extractfile(m).read()
        a = _load_ascii(raw, 8)
        del raw
        sel = a[:, 6] > 0.5                    # veto
        pos = sky_to_cart(a[sel, 0], a[sel, 1], a[sel, 2]).astype(np.float32)
        wt = a[sel, 7].astype(np.float64)      # fibre-collision weight
        del a
        r = geo.measure(pos, wt, bs=bs, rs=rs)
        del pos, wt
        r['name'] = m.name
        res.append(r)
        if out_path and (len(res) % every == 0 or len(res) == nmax):
            json.dump(dict(cap=cap, n=len(res), cell=CELL, rs=rs, bs=bs,
                           den_thr=DEN_THR, mask_frac=MASK_FRAC,
                           mask_smooth=MASK_SMOOTH, res=res),
                      open(out_path, 'w'), default=float)
        if len(res) % every == 0:
            log(f"    [{cap}] {len(res)}/{nmax}  {(time.time()-t0)/len(res):.1f}s/mock")
    tf.close()
    return geo, res


if __name__ == '__main__':
    cap = sys.argv[1] if len(sys.argv) > 1 else 'SGC'
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    op = sys.argv[3] if len(sys.argv) > 3 else None
    log(f"STAGE 2  cap={cap}  n={n}  cell={CELL}  R={RS}  b={BS}")
    g, r = stream_mocks(cap, n, out_path=op, every=max(1, min(10, n // 4)))
    for R in RS:
        for b in BS:
            v = [x[R]['b'][b]['folded'] for x in r if x[R]['b'][b]['folded'].get('occupancy_pass')]
            if not v:
                log(f"  R={R:.0f} b={b} folded: OCCUPANCY GATE FAILS "
                    f"(occ={g.occupancy(R,b):.0f})"); continue
            I = np.array([x['I'] for x in v])
            log(f"  R={R:.0f} b={b} folded: I = {I.mean():.4e} +- {I.std(ddof=1)/np.sqrt(len(I)):.2e}"
                f"  scatter/mean = {I.std(ddof=1)/I.mean():.3f}  (n={len(I)}, occ={v[0]['occupancy']:.0f})")
