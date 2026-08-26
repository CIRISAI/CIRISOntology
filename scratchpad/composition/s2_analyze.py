#!/usr/bin/env python3
"""S2' of COMPOSITION2_PREREG.md. `gauge` then `unblind`. Estimator settings fixed:
bit = sign(px); fiber = 4 rank bins of |px| within bit; cross-defect at lag 1 =
held-out gain of adding B's (bit,fiber) to A's for predicting A's bit(t+1).
Floors: 99th pct within-bit permutation (500 reps). CIs: 99% block bootstrap (1 s blocks).
"""
import sys, json
import numpy as np
import importlib.util
_s = importlib.util.spec_from_file_location("fp", "../fiber_pilot/fiber_pilot.py")
fp = importlib.util.module_from_spec(_s); _s.loader.exec_module(fp)
FPS = 60.0

def bits_fibers(x, trm):
    b = (x > 0).astype(np.int8)
    f = np.zeros(len(x), np.int16)
    for st in (0, 1):
        m = b == st; tv = np.abs(x[trm & m])
        if len(tv) < 4: continue
        e = fp.quantile_edges(tv, 4)
        f[m] = np.digitize(np.abs(x[m]), e[1:-1])
    return b, f

def cross_defect(xa, xb, lag, rng, n_perm=500):
    n = len(xa); trm = np.zeros(n, bool); trm[: int(0.6 * n)] = True
    ba, fa = bits_fibers(xa, trm); bb, fb_ = bits_fibers(xb, trm)
    ctxA = (ba.astype(np.intp) * 4 + fa)          # 8
    ctxAB = ctxA * 8 + (bb.astype(np.intp) * 4 + fb_)  # 64
    y = np.roll(ba, -lag).astype(np.int8)
    v = slice(0, n - lag)
    tr = trm[v]; te = ~trm[v]
    pA = fp.fit_prob(ctxA[v][tr], y[v][tr], 8)
    pAB = fp.fit_prob(ctxAB[v][tr], y[v][tr], 64)
    g = fp.score(pA, ctxA[v][te], y[v][te]) - fp.score(pAB, ctxAB[v][te], y[v][te])
    times = np.arange(n - lag)[te] / FPS
    ci = fp_block_ci(g, times, rng)
    null = np.empty(n_perm)
    for p in range(n_perm):
        fb2 = (bb.astype(np.intp) * 4 + fb_).copy()
        idx_tr = np.flatnonzero(trm); idx_te = np.flatnonzero(~trm)
        fb2[idx_tr] = rng.permutation(fb2[idx_tr]); fb2[idx_te] = rng.permutation(fb2[idx_te])
        c2 = ctxA * 8 + fb2
        p2 = fp.fit_prob(c2[v][tr], y[v][tr], 64)
        null[p] = np.mean(fp.score(pA, ctxA[v][te], y[v][te]) - fp.score(p2, c2[v][te], y[v][te]))
    return float(g.mean()), float(np.percentile(null, 99)), float(np.percentile(np.abs(null), 99)), ci

def fp_block_ci(delta, times, rng, block_s=1.0, n_boot=2000):
    block = np.floor(times / block_s).astype(int)
    ub = np.unique(block); bm = np.array([delta[block == b].mean() for b in ub])
    boot = bm[rng.integers(0, len(bm), size=(n_boot, len(bm)))].mean(axis=1)
    return float(np.quantile(boot, 0.005)), float(np.quantile(boot, 0.995))

def self_tau_c(x, rng, lags=(1, 2, 4, 8, 16, 32, 64)):
    n = len(x); trm = np.zeros(n, bool); trm[: int(0.6 * n)] = True
    b, f = bits_fibers(x, trm); ctx = b.astype(np.intp) * 4 + f
    base_ctx = b.astype(np.intp)
    rows = []
    for lag in lags:
        y = np.roll(b, -lag).astype(np.int8); v = slice(0, n - lag)
        tr, te = trm[v], ~trm[v]
        p0 = fp.fit_prob(base_ctx[v][tr], y[v][tr], 2)
        p1 = fp.fit_prob(ctx[v][tr], y[v][tr], 8)
        g = fp.score(p0, base_ctx[v][te], y[v][te]) - fp.score(p1, ctx[v][te], y[v][te])
        ci = fp_block_ci(g, np.arange(n - lag)[te] / FPS, rng)
        rows.append({"lag": lag, "gain": float(g.mean()), "ci": ci})
    tau_c = next((r["lag"] / FPS for r in rows if r["ci"][0] <= 0), None)
    return rows, tau_c

def autocorr_time(x):
    v = np.diff(x); v = v - v.mean()
    ac = np.correlate(v, v, "full")[len(v) - 1:]; ac /= ac[0]
    below = np.flatnonzero(ac < 1 / np.e)
    return (below[0] if len(below) else len(ac)) / FPS

def make_ar(n, rng, a=(1.2, -0.3), s=1.0):
    from scipy.signal import lfilter
    return lfilter([1.0], [1.0, -a[0], -a[1]], rng.normal(0, s, n + 500))[500:]

def gauge():
    rng = np.random.default_rng(20260826)
    n = 24000
    xa, xb = make_ar(n, rng), make_ar(n, rng)                      # independent
    g1, f1, a1_, _ = cross_defect(xa, xb, 1, np.random.default_rng(1))
    g2, f2, a2_, _ = cross_defect(xb, xa, 1, np.random.default_rng(2))
    # planted one-way: xb2 driven by xa
    drv = make_ar(n, rng); xb2 = 0.6 * np.roll(drv * np.sign(xa), 1) + 0.4 * make_ar(n, rng)
    g3, f3, a3_, _ = cross_defect(xb2, xa, 1, np.random.default_rng(3))
    print(f"GAUGE null: {g1:+.5f} (fl {f1:.5f}) / {g2:+.5f} (fl {f2:.5f})   planted A->B: {g3:+.5f} (fl {f3:.5f})")
    # tau ruler: OU with known tau
    tau_known = 8 / FPS
    ou = np.zeros(n); th = 1 / (tau_known * FPS)
    eps = rng.normal(0, 1, n)
    for i in range(1, n): ou[i] = ou[i - 1] * (1 - th) + np.sqrt(2 * th) * eps[i]
    rows, tc = self_tau_c(ou, np.random.default_rng(4))
    ratio = (tc / tau_known) if tc else None
    print(f"GAUGE tau ruler: tau_c={tc} vs known {tau_known:.4f} -> ratio={ratio}")
    ok = g3 >= 5 * a3_ and g1 <= f1 and g2 <= f2 and ratio is not None
    print("GAUGE:", "TRANSFERS" if ok else "STOP")
    json.dump({"null": [g1, f1, g2, f2], "planted": [g3, f3], "ratio": ratio,
               "transfers": bool(ok)}, open("s2_gauge.json", "w"), indent=2)

def unblind():
    import csv as csvmod
    rows = list(csvmod.reader(open("s2/arms_NI.csv")))[1:]
    cols = {name: np.array([float(r[i]) for r in rows]) for i, name in
            enumerate("frame,n1_px,n1_spd,n2_px,n2_spd,i_l_px,i_l_spd,i_r_px,i_r_spd".split(","))}
    G = json.load(open("s2_gauge.json")); ratio = G["ratio"]
    res = {}
    # B1
    a1, fl1, ab1, _ = cross_defect(cols["n1_px"], cols["n2_px"], 1, np.random.default_rng(11))
    a2, fl2, ab2, _ = cross_defect(cols["n2_px"], cols["n1_px"], 1, np.random.default_rng(12))
    res["B1"] = {"d12": a1, "f12": fl1, "d21": a2, "f21": fl2,
                 "pass": bool(a1 <= fl1 and a2 <= fl2)}
    print(f"B1 independent: {a1:+.5f} (fl {fl1:.5f}) / {a2:+.5f} (fl {fl2:.5f}) -> {res['B1']['pass']}")
    # B2: L -> R vs R -> L  (defect of adding L to predict R = Δ_{L→R})
    dLR, fLR, aLR, _ = cross_defect(cols["i_r_px"], cols["i_l_px"], 1, np.random.default_rng(13))
    dRL, fRL, aRL, _ = cross_defect(cols["i_l_px"], cols["i_r_px"], 1, np.random.default_rng(14))
    res["B2"] = {"dLR": dLR, "fLR": fLR, "aLR": aLR, "dRL": dRL,
                 "pass": bool(dLR >= 5 * aLR and dLR >= dRL)}
    print(f"B2 coupled: L->R {dLR:+.5f} (fl {fLR:.5f})  R->L {dRL:+.5f} -> {res['B2']['pass']}")
    # B3
    rows3, tc = self_tau_c(cols["i_l_px"], np.random.default_rng(15))
    tau_d = autocorr_time(cols["i_l_px"])
    lo, hi = ratio / 2.5 * tau_d, 2.5 * ratio * tau_d
    res["B3"] = {"tau_c": tc, "tau_data": tau_d, "band": [lo, hi],
                 "pass": bool(tc is not None and lo <= tc <= hi)}
    print(f"B3 contraction: tau_c={tc} tau_data={tau_d:.4f} band=[{lo:.4f},{hi:.4f}] -> {res['B3']['pass']}")
    # B4
    krows = list(csvmod.reader(open("s2/arm_K.csv")))[1:]
    dpos = np.array([float(r[2]) for r in krows])
    w = dpos[5:960]
    ratios = w[1:][w[:-1] > 0] / w[:-1][w[:-1] > 0]
    K = float(np.median(ratios))
    res["B4"] = {"K_median": K, "pass": bool(K <= 1.05)}
    print(f"B4 K: median={K:.4f} -> {res['B4']['pass']}")
    res["verdict"] = all(res[k]["pass"] for k in ("B1", "B2", "B3", "B4"))
    print("S2' ARMS:", {k: res[k]["pass"] for k in ("B1", "B2", "B3", "B4")})
    json.dump(res, open("s2_results.json", "w"), indent=2, default=float)

if __name__ == "__main__":
    {"gauge": gauge, "unblind": unblind}[sys.argv[1]]()
