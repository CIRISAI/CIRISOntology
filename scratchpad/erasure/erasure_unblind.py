#!/usr/bin/env python3
"""E0d-proper gauge + the unblind. All pins from STAGE2_FREEZE.md (incl. 2b).

Modes: `gauge` (synthetic Langevin at pinned parameters -> floors + velocity-
signature check at the analysis rate) and `unblind` (E1-E4 on the real data).
"""
from __future__ import annotations
import sys, json, glob
from pathlib import Path
import numpy as np
import importlib.util

_s = importlib.util.spec_from_file_location("fp", "../fiber_pilot/fiber_pilot.py")
fp = importlib.util.module_from_spec(_s); _s.loader.exec_module(fp)

F0, Q = 1090.0, 7.0
T0 = 1.0 / F0
FS_RAW = 10000 / (2 * T0)          # 5.45 MHz
DS = 100
FS_A = FS_RAW / DS                 # 54.5 kHz
W_END = 50                         # analysis sample where assessment starts
TAU_R = Q / (np.pi * F0)           # 2.044 ms
CI_LO, CI_HI = 0.00625, 0.99375    # 98.75% (Bonferroni 0.05/4)
FB, VB = 8, 5
ROOT = Path("data/extracted/ZenodoLandauer/Single Erasure")
PROTOS = {"Basic": "Basic Protocol", "Enhanced": "Enhanced Protocol",
          "OptSingle": "Optimized Single, E_tot", "OptMulti": "Optimized Multiple"}

def load_cell(proto_dir, target):
    d = ROOT / proto_dir / (
        [p for p in ["to0","to1","ErasureTo0","ErasureTo1","Erasureto0","Erasureto1"]
         if (ROOT/proto_dir/p).exists() and p.lower().endswith(str(target))][0])
    def one(pref):
        f = sorted(glob.glob(str(d / f"{pref}*.npy")))
        assert len(f) == 1, (pref, d, f)
        return np.load(f[0], mmap_mode="r")
    return one("z0"), one("z1"), np.asarray(one("W")), np.asarray(one("Success")).astype(bool)

def pin_position(z0, z1, S, target):
    """Frozen fallback: final-sample sign agreement with Success semantics."""
    a0 = float(np.mean(((np.asarray(z0[:, -1]) < 0) if target == 0 else (np.asarray(z0[:, -1]) > 0)) == S))
    a1 = float(np.mean(((np.asarray(z1[:, -1]) < 0) if target == 0 else (np.asarray(z1[:, -1]) > 0)) == S))
    return (z0 if a0 >= a1 else z1), {"z0_agree": a0, "z1_agree": a1, "position": "z0" if a0 >= a1 else "z1"}

def prep(zpos, ds=DS):
    x = np.asarray(zpos[:, ::ds], dtype=np.float64)
    v = np.zeros_like(x); v[:, 1:] = np.diff(x, axis=1) * (FS_RAW / ds)
    return x, v

def bins_pooled(vals, bit, train_mask, nb):
    out = np.empty(vals.shape, np.int16)
    for st in (0, 1):
        tv = vals[train_mask][bit[train_mask] == st]
        e = fp.quantile_edges(tv, nb)
        m = bit == st
        out[m] = np.digitize(vals[m], e[1:-1])
    return out

def boot_ci(per_traj_gain, rng, lo=CI_LO, hi=CI_HI, n=2000):
    m = per_traj_gain
    b = np.array([m[rng.integers(0, len(m), len(m))].mean() for _ in range(n)])
    return float(np.quantile(b, lo)), float(np.quantile(b, hi))

def e3_cell(x, v, S, rng, fiber="both"):
    """Witness at sample W_END -> Success, beyond the bit. Returns per-test-traj gains."""
    N = len(S); tr = rng.permutation(N); ntr = int(0.6 * N)
    trm = np.zeros(N, bool); trm[tr[:ntr]] = True
    xb = x[:, W_END]; vb_ = v[:, W_END]
    bit = (xb > 0).astype(np.int8)     # side label; fibers are within-side
    fbin = bins_pooled(xb, bit, trm, FB); vbin = bins_pooled(vb_, bit, trm, VB)
    if fiber == "both": fine = fbin * VB + vbin; nf = FB * VB
    elif fiber == "pos": fine = fbin; nf = FB
    else: fine = vbin; nf = VB
    y = S.astype(np.int8)
    base = fp.fit_prob(bit[trm].astype(np.intp), y[trm], 2)
    full = fp.fit_prob((bit.astype(np.intp) * nf + fine)[trm], y[trm], 2 * nf)
    te = ~trm
    bl = fp.score(base, bit[te].astype(np.intp), y[te])
    fl = fp.score(full, (bit.astype(np.intp) * nf + fine)[te], y[te])
    return bl - fl, (bit, fine, nf, trm, y, bl)

def e3_perm_p(bit, fine, nf, trm, y, bl, gain_mean, rng, n_perm=1000):
    te = ~trm; null = np.empty(n_perm)
    for p in range(n_perm):
        f2 = fine.copy()
        for st in (0, 1):
            for m in (trm, te):
                i = np.flatnonzero(m & (bit == st)); f2[i] = rng.permutation(f2[i])
        pr = fp.fit_prob((bit.astype(np.intp) * nf + f2)[trm], y[trm], 2 * nf)
        null[p] = np.mean(bl - fp.score(pr, (bit.astype(np.intp) * nf + f2)[te], y[te]))
    return float((1 + np.sum(null >= gain_mean)) / (n_perm + 1)), float(np.percentile(null, 95))

def e1_gains(x, v, rng):
    """Pooled windowed closure defect inside the assessment window."""
    bit = (x > 0).astype(np.int8)
    N, T = x.shape; trm1 = np.zeros(N, bool); trm1[rng.permutation(N)[:int(0.6*N)]] = True
    out = []
    for lag in (1, 3, 6, 12, 24, 48):
        t0s = np.arange(W_END, T - lag)
        ctx_traj = np.repeat(np.arange(N), len(t0s))
        tt = np.tile(t0s, N)
        b_now = bit[ctx_traj, tt]; b_next = bit[ctx_traj, tt + lag]
        xv = x[ctx_traj, tt]; vv = v[ctx_traj, tt]
        trm = trm1[ctx_traj]
        fb_ = bins_pooled(xv, b_now, trm, FB); vb2 = bins_pooled(vv, b_now, trm, VB)
        fine = fb_ * VB + vb2; nf = FB * VB
        base = fp.fit_prob(b_now[trm].astype(np.intp), b_next[trm], 2)
        full = fp.fit_prob((b_now.astype(np.intp) * nf + fine)[trm], b_next[trm], 2 * nf)
        te = ~trm
        bl = fp.score(base, b_now[te].astype(np.intp), b_next[te])
        fl = fp.score(full, (b_now.astype(np.intp) * nf + fine)[te], b_next[te])
        g = bl - fl
        per_traj = np.array([g[ctx_traj[te] == i].mean() for i in np.flatnonzero(~trm1)])
        ci = boot_ci(per_traj[~np.isnan(per_traj)], rng)
        out.append({"h_ms": lag / FS_A * 1000, "gain": float(g.mean()), "ci": ci})
    return out

def gauge():
    from scipy.signal import lfilter
    rng = np.random.default_rng(20260826)
    w0 = 2*np.pi*F0; m = 1.0; KT = 1.0; Eb = 4.0
    x0 = np.sqrt(8*Eb/(m*w0**2)); gam = m*w0/Q
    dt = 1/(FS_A*80); c1 = np.exp(-gam/m*dt); c2 = np.sqrt(KT/m*(1-c1**2))
    Fq = lambda x: -4*Eb*x*(x*x/(x0*x0)-1)/(x0*x0)
    n_traj, T = 3000, 100
    X = np.empty((n_traj, T)); Vv = np.empty((n_traj, T))
    x = x0; v = 0.0
    sub = int(1/(FS_A*dt))
    for i in range(n_traj):
        for t in range(T):
            for _ in range(sub):
                v += 0.5*dt*Fq(x)/m; x += 0.5*dt*v
                v = c1*v + c2*rng.standard_normal()
                x += 0.5*dt*v; v += 0.5*dt*Fq(x)/m
            X[i, t] = x; Vv[i, t] = v
    S = (X[:, -1] > 0)  # "stays/ends up" analogue
    xa = X; va = np.zeros_like(X); va[:, 1:] = np.diff(X, axis=1) * FS_A
    g_both, aux = e3_cell(xa, va, S, np.random.default_rng(1))
    g_pos, _ = e3_cell(xa, va, S, np.random.default_rng(1), "pos")
    g_vel, _ = e3_cell(xa, va, S, np.random.default_rng(1), "vel")
    p, floor95 = e3_perm_p(*aux, g_both.mean(), np.random.default_rng(2), 400)
    print(f"GAUGE E3-style: both={g_both.mean():+.5f} pos={g_pos.mean():+.5f} "
          f"vel={g_vel.mean():+.5f} perm_p={p:.4f} floor95={floor95:+.5f}")
    print(f"GAUGE velocity-signature at fs_a: {'PRESENT' if g_vel.mean() > g_pos.mean() else 'ABSENT'}")
    e1 = e1_gains(xa, va, np.random.default_rng(3))
    for r in e1: print(f"GAUGE E1 h={r['h_ms']:6.3f}ms gain={r['gain']:+.5f} ci=[{r['ci'][0]:+.5f},{r['ci'][1]:+.5f}]")
    json.dump({"e3_both": g_both.mean(), "e3_pos": g_pos.mean(), "e3_vel": g_vel.mean(),
               "perm_p": p, "floor95": floor95, "e1": e1},
              open("gauge_proper.json", "w"), indent=2, default=float)

def unblind():
    rng = np.random.default_rng(20260826)
    res = {"pins": {"fs_raw": FS_RAW, "ds": DS, "fs_a": FS_A, "tau_R_ms": TAU_R*1000}}
    cells = {}
    e4_verdicts = {}
    for pname, pdir in PROTOS.items():
        for tgt in (0, 1):
            try:
                z0, z1, W, S = load_cell(pdir, tgt)
            except Exception as e:
                cells[f"{pname}_to{tgt}"] = {"error": str(e)[:120]}; continue
            zpos, pininfo = pin_position(z0, z1, S, tgt)
            x, v = prep(zpos)
            g, aux = e3_cell(x, v, S, np.random.default_rng(7))
            gp, _ = e3_cell(x, v, S, np.random.default_rng(7), "pos")
            gv, _ = e3_cell(x, v, S, np.random.default_rng(7), "vel")
            p, floor95 = e3_perm_p(*aux, g.mean(), np.random.default_rng(8))
            ci = boot_ci(g, np.random.default_rng(9))
            # E4
            vinit = np.abs(v[:, 1]); qs = np.quantile(vinit, [0.25, 0.5, 0.75])
            qi = np.digitize(vinit, qs)
            mw = [float(W[qi == k].mean()) for k in range(4)]
            d41 = W[qi == 3] - np.mean(W[qi == 0])
            b = np.array([np.mean(W[qi == 3][rng.integers(0, (qi==3).sum(), (qi==3).sum())]) -
                          np.mean(W[qi == 0][rng.integers(0, (qi==0).sum(), (qi==0).sum())])
                          for _ in range(2000)])
            e4ci = (float(np.quantile(b, CI_LO)), float(np.quantile(b, CI_HI)))
            cells[f"{pname}_to{tgt}"] = {
                "N": len(S), "success_rate": float(S.mean()), "pin": pininfo,
                "e3_gain": float(g.mean()), "e3_ci": ci, "e3_p": p, "e3_floor95": floor95,
                "e3_pos": float(gp.mean()), "e3_vel": float(gv.mean()),
                "e4_meanW_by_q": mw, "e4_Q4minusQ1_ci": e4ci}
            r = cells[f"{pname}_to{tgt}"]
            print(f"{pname}_to{tgt}: N={r['N']} succ={r['success_rate']:.3f} pin={pininfo['position']} "
                  f"E3={r['e3_gain']:+.5f} ci=[{ci[0]:+.5f},{ci[1]:+.5f}] p={p:.4f} "
                  f"pos={r['e3_pos']:+.5f} vel={r['e3_vel']:+.5f}")
            print(f"   E4 meanW by |v|-quartile: {[round(m,4) for m in mw]}  Q4-Q1 CI={[round(c,4) for c in e4ci]}")
        # protocol-level E4 verdict: monotone iff Q4-Q1 CI>0 in BOTH targets? staked per protocol:
    for pname in PROTOS:
        oks = []
        for tgt in (0,1):
            c = cells.get(f"{pname}_to{tgt}", {})
            if "e4_Q4minusQ1_ci" in c:
                mw = c["e4_meanW_by_q"]
                oks.append(c["e4_Q4minusQ1_ci"][0] > 0 and mw[3] > mw[0])
        e4_verdicts[pname] = bool(oks and all(oks))
    # E1/E2 on the pooled Basic cell (declared representative; others reported)
    z0, z1, W, S = load_cell(PROTOS["Basic"], 0)
    zpos, _ = pin_position(z0, z1, S, 0)
    x, v = prep(zpos)
    e1 = e1_gains(x, v, np.random.default_rng(11))
    for r in e1: print(f"E1 h={r['h_ms']:6.3f}ms gain={r['gain']:+.5f} ci=[{r['ci'][0]:+.5f},{r['ci'][1]:+.5f}]")
    res["cells"] = cells; res["e4_verdicts"] = e4_verdicts; res["e1_basic_to0"] = e1
    json.dump(res, open("unblind_results.json", "w"), indent=2, default=float)
    print("E4 verdicts:", e4_verdicts)

if __name__ == "__main__":
    {"gauge": gauge, "unblind": unblind}[sys.argv[1]]()
