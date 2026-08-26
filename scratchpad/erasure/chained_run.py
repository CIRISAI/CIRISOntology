#!/usr/bin/env python3
"""Chained-streams campaign — instrument for CHAINED_PREREG.md (frozen first).

C0 gauge (STOP-capable) -> C1 within-erasure defect, C2 cross-drive slow mode,
C3 derived work-magnitude law, C4 companion. Cluster bootstrap over chains,
98.75% CIs. Values are read only when `run` executes.
"""
from __future__ import annotations
import sys, json, glob
import numpy as np
import importlib.util
_s = importlib.util.spec_from_file_location("fp", "../fiber_pilot/fiber_pilot.py")
fp = importlib.util.module_from_spec(_s); _s.loader.exec_module(fp)

F0, Q = 1090.0, 7.0
FS_RAW, DS = 2.0e6, 100
FS_A = FS_RAW / DS                       # 20 kHz
SEG, DRIVE_END = 37, 18                  # analysis samples per erasure; drive ends at 18
CI_LO, CI_HI = 0.00625, 0.99375          # 98.75%
FB, VB = 8, 5
ROOT = "data/extracted/ZenodoLandauer/Chained Erasure/"
PROTOS = {"Basic": "Basic", "Enhanced": "Enhanced",
          "OptSingle": "Optimized Single, Etot", "OptMulti": "Optimized Multiple"}

def bins_pooled(vals, bit, trm, nb):
    out = np.zeros(vals.shape, np.int16)
    for st in (0, 1):
        m = bit == st
        tv = vals[trm & m]
        if len(tv) < nb: continue
        e = fp.quantile_edges(tv, nb)
        out[m] = np.digitize(vals[m], e[1:-1])
    return out

def cluster_ci(vals, chains, rng, n=1000):
    """bootstrap over unique chains; vals/chains flat arrays."""
    uc = np.unique(chains)
    per = {c: vals[chains == c].mean() for c in uc}
    arr = np.array([per[c] for c in uc])
    b = np.array([arr[rng.integers(0, len(arr), len(arr))].mean() for _ in range(n)])
    return float(np.quantile(b, CI_LO)), float(np.quantile(b, CI_HI))

def load_pos(pdir):
    f = sorted(glob.glob(ROOT + pdir + "/z[A-Za-z_]*.npy"))
    f = [x for x in f if "/z0" not in x and "/z1" not in x]
    assert len(f) == 1, f
    z = np.load(f[0], mmap_mode="r")
    x = np.asarray(z[:, ::DS], dtype=np.float64)          # (N, 3700)
    v = np.zeros_like(x); v[:, 1:] = np.diff(x, axis=1) * FS_A
    return x, v

def c1_defect(x, v, rng, lags=(1, 2, 4, 8, 16)):
    N, T = x.shape; n_er = T // SEG
    trm_chain = np.zeros(N, bool); trm_chain[rng.permutation(N)[:int(0.6 * N)]] = True
    rows = []
    for lag in lags:
        ts = [37 * k + t for k in range(n_er) for t in range(DRIVE_END, SEG - lag)]
        ts = np.array(ts)
        ci_ = np.repeat(np.arange(N), len(ts)); tt = np.tile(ts, N)
        b0 = (x[ci_, tt] > 0).astype(np.int8); b1 = (x[ci_, tt + lag] > 0).astype(np.int8)
        xv, vv = x[ci_, tt], v[ci_, tt]
        trm = trm_chain[ci_]
        fb_ = bins_pooled(xv, b0, trm, FB); vb_ = bins_pooled(vv, b0, trm, VB)
        fine = fb_ * VB + vb_; nf = FB * VB
        base = fp.fit_prob(b0[trm].astype(np.intp), b1[trm], 2)
        full = fp.fit_prob((b0.astype(np.intp) * nf + fine)[trm], b1[trm], 2 * nf)
        te = ~trm
        g = fp.score(base, b0[te].astype(np.intp), b1[te]) - \
            fp.score(full, (b0.astype(np.intp) * nf + fine)[te], b1[te])
        ci = cluster_ci(g, ci_[te], rng)
        rows.append({"h_ms": lag / FS_A * 1000, "gain": float(g.mean()), "ci": ci})
    return rows

def c2_slowmode(x, v, rng, ms=(1, 2, 4, 8, 16, 32)):
    N, T = x.shape; n_er = T // SEG
    trm_chain = np.zeros(N, bool); trm_chain[rng.permutation(N)[:int(0.6 * N)]] = True
    rows = []
    for m in ms:
        ks = np.arange(0, n_er - m)
        wit_t = 37 * ks + DRIVE_END
        end_t = 37 * (ks + m) + SEG - 1
        ci_ = np.repeat(np.arange(N), len(ks))
        wt = np.tile(wit_t, N); et = np.tile(end_t, N)
        b0 = (x[ci_, wt] > 0).astype(np.int8); b1 = (x[ci_, et] > 0).astype(np.int8)
        xv, vv = x[ci_, wt], v[ci_, wt]
        trm = trm_chain[ci_]
        fb_ = bins_pooled(xv, b0, trm, FB); vb_ = bins_pooled(vv, b0, trm, VB)
        fine = fb_ * VB + vb_; nf = FB * VB
        base = fp.fit_prob(b0[trm].astype(np.intp), b1[trm], 2)
        full = fp.fit_prob((b0.astype(np.intp) * nf + fine)[trm], b1[trm], 2 * nf)
        te = ~trm
        g = fp.score(base, b0[te].astype(np.intp), b1[te]) - \
            fp.score(full, (b0.astype(np.intp) * nf + fine)[te], b1[te])
        ci = cluster_ci(g, ci_[te], rng)
        rows.append({"m": int(m), "gain": float(g.mean()), "ci": ci})
    return rows

def calibrate_kT():
    """Equipartition on the single-erasure LATE window (4-5 ms), Basic_to0 (declared)."""
    z = np.load("data/extracted/ZenodoLandauer/Single Erasure/Basic Protocol/to0/z_Basic_0.npy",
                mmap_mode="r")
    x = np.asarray(z[:, ::DS], dtype=np.float64)
    v = np.diff(x, axis=1) * FS_A
    h1 = v[:, 79:89].ravel(); h2 = v[:, 89:99].ravel()
    m1, m2 = np.mean(h1**2), np.mean(h2**2)
    ok = abs(m1 - m2) / max(m1, m2) <= 0.20
    return 0.5 * (m1 + m2), ok, float(m1), float(m2)   # <v^2>_eq == kT/m in v-units

def c3_worklaw(x, v, W, v2_eq, rng):
    N, T = x.shape
    if W.shape[0] != N:
        # Enhanced ships 665 work rows against 605 trace rows with no mapping --
        # row alignment is unknowable, so C3 is VOID for that protocol, structurally.
        return {"VOID": f"row mismatch W={W.shape[0]} vs chains={N}, alignment unshipped"}
    n_er = min(T // SEG, W.shape[1])
    ks = np.arange(n_er)
    ci_ = np.repeat(np.arange(N), n_er)
    vt = np.tile(37 * ks + 1, N)
    vinit = np.abs(v[ci_, vt])
    w = np.asarray(W[:, :n_er]).ravel()
    fin = np.isfinite(w)
    vinit, w, ci_ = vinit[fin], w[fin], ci_[fin]
    qi = (np.argsort(np.argsort(vinit)) * 4 // len(vinit)).astype(int)
    mw = [float(w[qi == k].mean()) for k in range(4)]
    ke = vinit**2 / (2 * v2_eq)                          # kT units
    dke = float(ke[qi == 3].mean() - ke[qi == 0].mean())
    d = np.where(qi == 3, w, np.nan)                     # cluster bootstrap on Q4-Q1
    uc = np.unique(ci_)
    def stat(sel_chains):
        m = np.isin(ci_, sel_chains)
        return (w[m & (qi == 3)].mean() - w[m & (qi == 0)].mean())
    boots = []
    for _ in range(1000):
        sel = uc[rng.integers(0, len(uc), len(uc))]
        try: boots.append(stat(sel))
        except Exception: pass
    ci = (float(np.quantile(boots, CI_LO)), float(np.quantile(boots, CI_HI)))
    dW = float(w[qi == 3].mean() - w[qi == 0].mean())
    return {"meanW_by_q": mw, "dW_Q4Q1": dW, "dW_ci": ci, "dKE_kT": dke,
            "ratio": dW / dke if dke > 0 else None}

def gauge():
    from scipy.signal import lfilter
    rng = np.random.default_rng(20260826)
    w0 = 2*np.pi*F0; m_ = 1.0; KT = 1.0; Eb = 4.0
    x0 = np.sqrt(8*Eb/(m_*w0**2)); gam = m_*w0/Q
    dt = 1/(FS_A*80); c1 = np.exp(-gam/m_*dt); c2 = np.sqrt(KT/m_*(1-c1**2))
    Fq = lambda xx: -4*Eb*xx*(xx*xx/(x0*x0)-1)/(x0*x0)
    N, T = 200, 37*20
    X = np.empty((N, T)); xx, vv = x0, 0.0
    sub = int(1/(FS_A*dt))
    for i in range(N):
        for t in range(T):
            for _ in range(sub):
                vv += 0.5*dt*Fq(xx)/m_; xx += 0.5*dt*vv
                vv = c1*vv + c2*rng.standard_normal()
                xx += 0.5*dt*vv; vv += 0.5*dt*Fq(xx)/m_
            X[i, t] = xx
    Va = np.zeros_like(X); Va[:, 1:] = np.diff(X, axis=1) * FS_A
    r1 = c1_defect(X, Va, np.random.default_rng(1), lags=(1, 2, 4, 8))
    r2 = c2_slowmode(X, Va, np.random.default_rng(2), ms=(1, 2, 4))
    for r in r1: print(f"GAUGE C1 h={r['h_ms']:.2f}ms gain={r['gain']:+.5f} ci=[{r['ci'][0]:+.5f},{r['ci'][1]:+.5f}]")
    for r in r2: print(f"GAUGE C2 m={r['m']} gain={r['gain']:+.5f} ci=[{r['ci'][0]:+.5f},{r['ci'][1]:+.5f}]")
    ok = r1[0]["ci"][0] > 0
    print("GAUGE C0:", "TRANSFERS (C1 short-lag CI>0)" if ok else "STOP")
    json.dump({"c1": r1, "c2": r2, "transfers": bool(ok)}, open("chained_gauge.json","w"), indent=2)

def run():
    rng = np.random.default_rng(20260826)
    v2_eq, cal_ok, m1, m2 = calibrate_kT()
    print(f"calibration: <v2>_eq={v2_eq:.4e} halves=({m1:.4e},{m2:.4e}) ok={cal_ok}")
    res = {"calibration": {"v2_eq": v2_eq, "ok": bool(cal_ok), "halves": [m1, m2]}}
    for pname, pdir in PROTOS.items():
        x, v = load_pos(pdir)
        Wf = sorted(glob.glob(ROOT + pdir + "/*W*.npy"))
        W = np.load([f for f in Wf][0], mmap_mode="r")
        print(f"--- {pname}: chains={x.shape[0]} ---")
        c1 = c1_defect(x, v, np.random.default_rng(11))
        for r in c1: print(f"C1 {pname} h={r['h_ms']:.2f}ms gain={r['gain']:+.5f} ci=[{r['ci'][0]:+.5f},{r['ci'][1]:+.5f}]")
        c2 = c2_slowmode(x, v, np.random.default_rng(12))
        for r in c2: print(f"C2 {pname} m={r['m']:2d} gain={r['gain']:+.5f} ci=[{r['ci'][0]:+.5f},{r['ci'][1]:+.5f}]")
        c3 = c3_worklaw(x, v, W, v2_eq, np.random.default_rng(13))
        if "VOID" in c3:
            print(f"C3 {pname} VOID: {c3['VOID']}")
        else:
            print(f"C3 {pname} meanW_q={[round(m,3) for m in c3['meanW_by_q']]} dW={c3['dW_Q4Q1']:+.4f} "
              f"ci=[{c3['dW_ci'][0]:+.4f},{c3['dW_ci'][1]:+.4f}] dKE={c3['dKE_kT']:.4f} ratio={None if c3['ratio'] is None else round(c3['ratio'],3)}")
        # C4 companion
        Tf = sorted(glob.glob(ROOT + pdir + "/T*.npy")); Tc = np.asarray(np.load(Tf[0]))
        n_er = min(x.shape[1] // SEG, len(Tc))
        keq = np.array([np.mean(v[:, 37*k+1:37*k+3]**2)/v2_eq for k in range(n_er)])
        c4 = float(np.corrcoef(keq[:n_er], Tc[:n_er])[0, 1])
        print(f"C4 {pname} corr(per-index KE, T(k)) = {c4:+.3f}")
        res[pname] = {"c1": c1, "c2": c2, "c3": c3, "c4_corr_KE_T": c4}
        del x, v
    json.dump(res, open("chained_results.json", "w"), indent=2, default=float)

if __name__ == "__main__":
    {"gauge": gauge, "run": run}[sys.argv[1]]()
