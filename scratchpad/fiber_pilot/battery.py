#!/usr/bin/env python3
"""Robustness battery — instrument for FIBER_ROBUSTNESS_PREREG.md (frozen first).

INSTRUMENT-LEVEL QUANTIFICATIONS, declared here BEFORE any real-data run (the
prereg left R1/R2/R4 qualitative; these bands are frozen now and may not move):
  R1 PASS: for EACH view, pooled 0.1-5 ms force gain has 99.5% block CI > 0,
           AND the 100 ms gain < 0.5 x the 0.1-1 ms mean gain (contraction shape).
  R2 PASS: at matched horizons {0.5, 1, 5 ms}, the 99.5% CIs of the gain overlap
           across all sampling rates (time-invariance).
  R3 PASS: real force gain > the 95th percentile of 200 state-conditional AR(2)
           surrogates at EVERY horizon where the pilot CI excluded zero.
  R4 PASS: the max cell of the resolution grid <= 1.5 x the 8x5 cell at 1 ms.
Family-wise: CIs at 99.5%; permutation count 1000 where p is quoted.

`validate` mode gauges the ruler on synthetic traces with PLANTED truth (beta>0:
within-fiber position modulates switching) and a NULL (beta=0), with reduced
replicate counts (declared: gauging, not quoting).
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
from scipy.signal import lfilter
import importlib.util

_s = importlib.util.spec_from_file_location("fp", Path(__file__).parent / "fiber_pilot.py")
fp = importlib.util.module_from_spec(_s)
import types
# fiber_pilot imports h5py/sklearn/matplotlib at module level; fine in fenv.
_s.loader.exec_module(fp)

RNG = np.random.default_rng(20260826)
CI_LO, CI_HI = 0.0025, 0.9975          # 99.5%
PILOT_SIG_HORIZONS = [0.0001, 0.0005, 0.001, 0.005]   # where the pilot CI excluded 0

def block_ci(delta, times, lo=CI_LO, hi=CI_HI, block_s=0.5, n_boot=4000, rng=RNG):
    block = np.floor(times / block_s).astype(int)
    ub = np.unique(block)
    bm = np.array([delta[block == b].mean() for b in ub])
    boot = bm[rng.integers(0, len(bm), size=(n_boot, len(bm)))].mean(axis=1)
    return float(np.quantile(boot, lo)), float(np.quantile(boot, hi))

def gains(force, coarse, fs, horizons, fbins=8, vbins=5, train_frac=0.6,
          n_perm=0, rng=RNG):
    """The pilot pipeline, parameterized. Returns per-horizon dict."""
    velocity = np.empty_like(force); velocity[0] = 0.0
    velocity[1:] = np.diff(force) * fs
    train_end = int(train_frac * len(force))
    fb = fp.assign_bins(force, coarse, train_end, fbins)
    vb = fp.assign_bins(velocity, coarse, train_end, vbins)
    db = fb * vbins + vb
    out = []
    for hz in horizons:
        lag = max(1, int(round(hz * fs)))
        tr = np.arange(1, train_end - lag)
        stride = max(lag, int(round(0.001 * fs)))
        te = np.arange(train_end, len(force) - lag, stride)
        if len(te) < 5: continue
        ytr, yte = coarse[tr + lag], coarse[te + lag]
        base = fp.fit_prob(coarse[tr], ytr, 2)
        bl = fp.score(base, coarse[te], yte)
        fc_tr, fc_te = coarse[tr] * fbins + fb[tr], coarse[te] * fbins + fb[te]
        fl = fp.score(fp.fit_prob(fc_tr, ytr, 2 * fbins), fc_te, yte)
        nd = fbins * vbins
        dl = fp.score(fp.fit_prob(coarse[tr] * nd + db[tr], ytr, 2 * nd),
                      coarse[te] * nd + db[te], yte)
        fg, dg = bl - fl, bl - dl
        times = (te - train_end) / fs
        row = {"horizon_s": lag / fs, "n_test": len(te),
               "force_gain": float(fg.mean()), "force_ci": block_ci(fg, times, rng=rng),
               "dyn_gain": float(dg.mean()), "dyn_ci": block_ci(dg, times, rng=rng)}
        if n_perm:
            null = np.empty(n_perm)
            for p in range(n_perm):
                ftr, fte = fb[tr].copy(), fb[te].copy()
                for st in (0, 1):
                    i = np.flatnonzero(coarse[tr] == st); ftr[i] = rng.permutation(ftr[i])
                    i = np.flatnonzero(coarse[te] == st); fte[i] = rng.permutation(fte[i])
                pr = fp.fit_prob(coarse[tr] * fbins + ftr, ytr, 2 * fbins)
                null[p] = np.mean(bl - fp.score(pr, coarse[te] * fbins + fte, yte))
            row["perm_p"] = float((1 + np.sum(null >= fg.mean())) / (n_perm + 1))
        out.append(row)
    return out

# ---------------- views (R1) ----------------
def view_tutorial(force, train_end, rng):
    from sklearn.mixture import GaussianMixture
    g = GaussianMixture(2, random_state=20260826, n_init=1,
                        weights_init=np.array([0.1, 0.9]),
                        means_init=np.array([[8.0], [10.0]]),
                        precisions_init=np.array([[[4.0]], [[4.0]]])
                        ).fit(force[:train_end:5, None])
    o = np.argsort(g.means_.ravel())
    return np.where(g.predict(force[:, None]) == o[0], 0, 1).astype(np.int8)

def view_free_gmm(force, train_end, rng):
    from sklearn.mixture import GaussianMixture
    g = GaussianMixture(2, random_state=20260826, n_init=10).fit(force[:train_end:5, None])
    o = np.argsort(g.means_.ravel())
    return np.where(g.predict(force[:, None]) == o[0], 0, 1).astype(np.int8)

def view_threshold(force, train_end, rng, thr=9.3):
    return (force >= thr).astype(np.int8)

def view_hysteresis(force, train_end, rng):
    base = view_tutorial(force, train_end, rng)
    lo_vals = force[:train_end][base[:train_end] == 0]
    hi_vals = force[:train_end][base[:train_end] == 1]
    t_dn = np.quantile(hi_vals, 0.05)   # leave state 1 below this
    t_up = np.quantile(lo_vals, 0.95)   # leave state 0 above this
    out = np.empty(len(force), np.int8); s = base[0]
    for i, f in enumerate(force):
        if s == 1 and f < t_dn: s = 0
        elif s == 0 and f > t_up: s = 1
        out[i] = s
    return out

# ---------------- surrogates (R3) ----------------
def fit_ar2(x):
    x = x - x.mean()
    r = [np.dot(x[: len(x) - k if k else None], x[k:]) / (len(x) - k) for k in (0, 1, 2)]
    a = np.linalg.solve([[r[0], r[1]], [r[1], r[0]]], [r[1], r[2]])
    s2 = r[0] - a[0] * r[1] - a[1] * r[2]
    return a, max(s2, 1e-12)

def surrogate(force, coarse, train_end, rng):
    out = np.empty_like(force)
    for st in (0, 1):
        m = coarse == st
        mu = force[:train_end][coarse[:train_end] == st].mean()
        a, s2 = fit_ar2(force[:train_end][coarse[:train_end] == st])
        e = rng.normal(0, np.sqrt(s2), m.sum() + 500)
        stream = lfilter([1.0], [1.0, -a[0], -a[1]], e)[500:]
        out[m] = mu + stream
    return out

# ---------------- synthetic (validate mode) ----------------
def synth(n, fs, beta, rng, mu=(8.37, 10.30), sig=0.35, p_exit=(0.05, 0.002)):
    a_true = (1.2, -0.3)
    e = rng.normal(0, sig * np.sqrt(1 - 0.85), n + 500)   # rough innovation scale
    fine = lfilter([1.0], [1.0, -a_true[0], -a_true[1]], e)[500:]
    fine = fine / fine.std() * sig
    s = np.empty(n, np.int8); s[0] = 1
    u = rng.random(n)
    for i in range(1, n):
        st = s[i - 1]
        p = p_exit[0] if st == 0 else p_exit[1]
        if beta and st == 1:
            p = p * np.exp(-beta * fine[i - 1] / sig)     # dip toward low -> more likely to switch
        s[i] = (1 - st) if u[i] < min(p, 0.9) else st
    return (np.where(s == 0, mu[0], mu[1]) + fine).astype(float), s

# ---------------- modes ----------------
def validate():
    fs, n = 39062.5, 1_200_000
    hz = [0.0001, 0.001, 0.005, 0.02]
    print("=== VALIDATE: planted (beta=1.5) vs null (beta=0); reduced counts (gauging) ===")
    for name, beta in (("PLANTED", 1.5), ("NULL", 0.0)):
        rng = np.random.default_rng(7)
        force, coarse = synth(n, fs, beta, rng)
        g = gains(force, coarse, fs, hz, n_perm=200, rng=np.random.default_rng(11))
        te = int(0.6 * n)
        sur = np.array([[r["force_gain"] for r in
                         gains(surrogate(force, coarse, te, np.random.default_rng(100 + k)),
                               coarse, fs, hz, rng=np.random.default_rng(12))]
                        for k in range(50)])
        p95 = np.percentile(sur, 95, axis=0)
        for i, r in enumerate(g):
            beat = r["force_gain"] > p95[i]
            print(f"  {name} h={r['horizon_s']*1000:7.2f}ms gain={r['force_gain']:+.5f} "
                  f"perm_p={r.get('perm_p'):.4f} surr95={p95[i]:+.5f} "
                  f"{'REAL>SURR' if beat else 'within-surr'}")
    print("EXPECT: PLANTED beats surrogates at short horizons; NULL stays within them.")

def run(data_path):
    import h5py
    with h5py.File(data_path, "r") as h5:
        f1 = h5["Force HF/Force 1x"][::2]; f2 = h5["Force HF/Force 2x"][::2]
    force = ((f2 - f1) / 2.0).astype(float); fs = 39062.5
    n = len(force); te = int(0.6 * n)
    hz_all = [0.0001, 0.0005, 0.001, 0.005, 0.02, 0.1]
    res = {"quantifications": "see module docstring; frozen before this run"}
    # R1
    views = {"tutorial": view_tutorial, "free_gmm": view_free_gmm,
             "threshold_9p3": view_threshold, "hysteresis": view_hysteresis}
    r1 = {}
    for nm, vf in views.items():
        c = vf(force, te, RNG)
        frac0 = float(np.mean(c == 0))
        g = gains(force, c, fs, hz_all, n_perm=1000, rng=np.random.default_rng(21))
        pooled = [r for r in g if r["horizon_s"] <= 0.006]
        pool_mean = float(np.mean([r["force_gain"] for r in pooled]))
        short = float(np.mean([r["force_gain"] for r in g if r["horizon_s"] <= 0.0011]))
        h100 = [r for r in g if abs(r["horizon_s"] - 0.1) < 0.02]
        contract = bool(h100 and h100[0]["force_gain"] < 0.5 * short)
        sig = all(r["force_ci"][0] > 0 for r in pooled)
        r1[nm] = {"low_frac": frac0, "gains": g, "pooled_mean": pool_mean,
                  "all_pooled_ci_gt0": sig, "contracts": contract,
                  "pass": bool(sig and contract)}
        print(f"R1 {nm}: low_frac={frac0:.3f} pooled={pool_mean:+.5f} "
              f"ci>0={sig} contracts={contract} -> {'PASS' if r1[nm]['pass'] else 'FAIL'}")
    res["R1"] = r1
    # R2 (tutorial view, matched-ms horizons)
    r2 = {}
    for ds in (2, 4, 8):
        f2s = force[::ds]; fs2 = fs / ds; te2 = int(0.6 * len(f2s))
        c2 = view_tutorial(f2s, te2, RNG)
        g = gains(f2s, c2, fs2, [0.0005, 0.001, 0.005], n_perm=0,
                  rng=np.random.default_rng(31))
        r2[f"ds{ds}"] = g
        print(f"R2 ds x{ds}: " + "  ".join(
            f"{r['horizon_s']*1000:.1f}ms={r['force_gain']:+.5f}[{r['force_ci'][0]:+.5f},{r['force_ci'][1]:+.5f}]" for r in g))
    # overlap check at matched ms
    r2_pass = True
    for j in range(3):
        ivs = [ (r2[k][j]["force_ci"]) for k in r2 if len(r2[k]) > j ]
        lo, hi = max(i[0] for i in ivs), min(i[1] for i in ivs)
        if lo > hi: r2_pass = False
    res["R2"] = {"cells": r2, "pass": bool(r2_pass)}
    print(f"R2 -> {'PASS (CIs overlap at matched ms)' if r2_pass else 'FAIL'}")
    # R3
    c = view_tutorial(force, te, RNG)
    real = gains(force, c, fs, PILOT_SIG_HORIZONS, rng=np.random.default_rng(41))
    sur = np.array([[r["force_gain"] for r in
                     gains(surrogate(force, c, te, np.random.default_rng(1000 + k)),
                           c, fs, PILOT_SIG_HORIZONS, rng=np.random.default_rng(42))]
                    for k in range(200)])
    p95 = np.percentile(sur, 95, axis=0)
    r3_pass = all(r["force_gain"] > p95[i] for i, r in enumerate(real))
    res["R3"] = {"real": [r["force_gain"] for r in real], "surr95": p95.tolist(),
                 "pass": bool(r3_pass)}
    for i, r in enumerate(real):
        print(f"R3 h={r['horizon_s']*1000:6.2f}ms real={r['force_gain']:+.5f} surr95={p95[i]:+.5f}")
    print(f"R3 -> {'PASS' if r3_pass else 'FAIL — KILLED, no erasure freeze'}")
    # R4
    grid = {}
    for fb in (4, 8, 16):
        for vb in (3, 5, 9):
            g = gains(force, c, fs, [0.001], fbins=fb, vbins=vb,
                      rng=np.random.default_rng(51))[0]
            grid[f"{fb}x{vb}"] = g["dyn_gain"]
    base85 = grid["8x5"]; mx = max(grid.values())
    r4_pass = mx <= 1.5 * base85
    res["R4"] = {"grid": grid, "pass": bool(r4_pass)}
    print("R4 grid:", {k: round(v, 5) for k, v in grid.items()})
    print(f"R4 -> {'PASS (saturates)' if r4_pass else 'FAIL -> branch R4-prime'}")
    # tau_c
    g_tut = r1["tutorial"]["gains"]
    tau_c = next((r["horizon_s"] for r in g_tut if r["force_ci"][0] <= 0), None)
    res["tau_c_s"] = tau_c
    res["verdict"] = {"R1": all(v["pass"] for v in r1.values()), "R2": r2_pass,
                      "R3": r3_pass, "R4": r4_pass}
    print(f"tau_c (first CI touching 0) = {tau_c}")
    Path("battery_results.json").write_text(json.dumps(res, indent=2, default=float) + "\n")
    print("VERDICTS:", res["verdict"])

if __name__ == "__main__":
    if sys.argv[1] == "validate": validate()
    else: run(sys.argv[2])
