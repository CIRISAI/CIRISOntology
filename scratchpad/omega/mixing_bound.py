#!/usr/bin/env python3
"""Shared mixing-bound machinery for OMEGA_KILL (S1-A5, S3-M1) + gauges G1/G2.

defect(m) = max over v-fiber pairs (x,y) of TV( v-push of m-step dist from x,
v-push from y ). alpha-hat = Dobrushin coefficient of the measured 1-step kernel.
Stake: defect(m) <= alpha^m + 3*sigma_boot.  (defect_le_alpha_pow, realized.)
"""
import numpy as np

def tv(p, q): return 0.5 * float(np.abs(np.asarray(p) - np.asarray(q)).sum())

def kernel_from_pairs(now, nxt, S):
    K = np.zeros((S, S))
    for a, b in zip(now, nxt): K[a, b] += 1
    rows = K.sum(1, keepdims=True); rows[rows == 0] = 1
    return K / rows

def dobrushin(K):
    S = len(K)
    return max(tv(K[i], K[j]) for i in range(S) for j in range(S) if i < j) if S > 1 else 0.0

def defect_m(now, fut, S, vmap):
    """max over v-fiber state pairs of TV of v-pushed m-step empirical dists."""
    V = max(vmap) + 1
    dists = {}
    for s in range(S):
        sel = fut[now == s]
        if len(sel) < 20: continue
        d = np.zeros(V)
        for t in sel: d[vmap[t]] += 1
        dists[s] = d / d.sum()
    worst = 0.0
    for i in dists:
        for j in dists:
            if i < j and vmap[i] == vmap[j]:
                worst = max(worst, tv(dists[i], dists[j]))
    return worst

def boot_sigma(now, fut, S, vmap, rng, n=500):
    vals = []
    idx = np.arange(len(now))
    for _ in range(n):
        r = rng.integers(0, len(idx), len(idx))
        vals.append(defect_m(now[r], fut[r], S, vmap))
    return float(np.std(vals))

def adjudicate(series_states, S, vmap, ms, rng, label=""):
    now1, nxt1 = series_states[:-1], series_states[1:]
    K = kernel_from_pairs(now1, nxt1, S)
    a = dobrushin(K)
    rows = []
    for m in ms:
        now, fut = series_states[:-m], series_states[m:]
        d = defect_m(now, fut, S, vmap)
        sig = boot_sigma(now, fut, S, vmap, rng)
        bound = a ** m + 3 * sig
        ok = d <= bound
        rows.append({"m": int(m), "defect": d, "alpha_pow": a ** m, "sigma": sig,
                     "bound": bound, "pass": bool(ok)})
        print(f"{label} m={m}: defect={d:.5f}  alpha^m={a**m:.5f}  +3sig={bound:.5f}  {'PASS' if ok else 'VIOLATION'}")
    return a, rows

if __name__ == "__main__":
    rng = np.random.default_rng(20260826)
    # G1: known Markov chain on 4 states (2 bits: state = 2*b + hidden), v = bit
    S, N = 4, 200_000
    K = np.array([[.7,.1,.1,.1],[.1,.7,.1,.1],[.2,.1,.6,.1],[.1,.2,.1,.6]])
    x = np.zeros(N, int); 
    for i in range(1, N): x[i] = rng.choice(4, p=K[x[i-1]])
    vmap = np.array([0, 0, 1, 1])
    a, rows = adjudicate(x, S, vmap, (2, 3, 4), rng, "G1")
    true_a = dobrushin(K)
    print(f"G1 alpha-hat={a:.4f} vs true {true_a:.4f}  {'OK' if abs(a-true_a)<0.05 else 'ESTIMATOR OFF'}")
    g1_ok = all(r["pass"] for r in rows) and abs(a - true_a) < 0.05
    # G2: planted NON-Markov violation -- hidden slow regime not in the state
    reg = np.zeros(N, int); x2 = np.zeros(N, int)
    for i in range(1, N):
        reg[i] = reg[i-1] if rng.random() > 0.001 else 1 - reg[i-1]
        Kr = K if reg[i] == 0 else np.array([[.1,.1,.1,.7],[.1,.1,.7,.1],[.1,.7,.1,.1],[.7,.1,.1,.1]])
        x2[i] = rng.choice(4, p=Kr[x2[i-1]])
    a2, rows2 = adjudicate(x2, S, vmap, (2, 3, 4), rng, "G2")
    g2_fires = not all(r["pass"] for r in rows2)
    print(f"G2 planted non-Markov: instrument {'FIRES (can detect violation)' if g2_fires else 'CANNOT FIRE -- STOP'}")
    print("GAUGE:", "TRANSFERS" if (g1_ok and g2_fires) else "STOP")
