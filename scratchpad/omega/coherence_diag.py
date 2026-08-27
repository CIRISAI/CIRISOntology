#!/usr/bin/env python3
"""POST-HOC DIAGNOSTIC (labelled): does chart conditioning explain N4's heterogeneity?

Coherence chi_j(t) = rms_signed_j / rms_abs_j from the tier3_diag dump. Ceiling for
view r at t: P_r(t) = sum_j |w_rj| * A_j(t)/S_j  (A = rms_abs, S = frozen scale).
(a) LEVEL: Spearman rank-corr of measured div_v(t) vs P_v(t) across 67 views.
(b) GROWTH: rank-corr of measured g_v (verdict statistic) vs P_v(1200)/P_v(300)."""
import csv
import numpy as np
from analyze_tier import load

M = (1 << 64) - 1
def splitmix64(x):
    z = (x + 0x9E3779B97F4A7C15) & M
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M
    return z ^ (z >> 31)
def unit(h): return ((h >> 11) / (1 << 53)) * 2.0 - 1.0

W = np.zeros((64, 9))
for r in range(64):
    for j in range(9):
        key = ((r * 0x9E3779B97F4A7C15) ^ (j * 0xD1B54A32D192ED03)) & M
        W[r, j] = unit(splitmix64(key))
    W[r] /= np.linalg.norm(W[r])

S = [float(l.split('=')[1]) for l in open('tier3/swap_scales.txt')]
A = {}
for row in list(csv.reader(open('tier3_diag/swap_coherence.csv')))[1:]:
    f, j, rs, ra = int(row[0]), int(row[1]), float(row[2]), float(row[3])
    A.setdefault(f, [0.0]*9)[j] = ra
chi = {f: [float(l.split('=')[1])/A[f][j] if False else 0 for j,l in enumerate(open('tier3/swap_scales.txt'))] for f in A}
print("chi_j(t) = rms_signed/rms_abs:")
for row in list(csv.reader(open('tier3_diag/swap_coherence.csv')))[1:]:
    f, j, rs, ra = int(row[0]), int(row[1]), float(row[2]), float(row[3])
    if j in (0,1,2): print(f"  f={f:>4} moment {j} ({'momx momy ke'.split()[j]}): chi={rs/ra:.3f}")

micro, decl, rand = load('tier3/swap.csv', 'tier3/swap_scales.txt')
views = np.vstack([decl, rand])                      # 67 x T
Wfull = np.vstack([np.eye(9)[:3], W])                # declared = pure directions
def P(f): return np.abs(Wfull) @ (np.array(A[f]) / np.array(S))
g_meas = np.array([np.median(v[1200:2400])/max(np.median(v[60:300]),1e-300) for v in views])
g_pred = P(1200) / P(300)

def spearman(x, y):
    rx = np.argsort(np.argsort(x)); ry = np.argsort(np.argsort(y))
    return float(np.corrcoef(rx, ry)[0,1])

for f in (300, 1200):
    lvl = np.array([np.median(v[max(f-40,1):f+40]) for v in views])
    print(f"(a) LEVEL f={f}: Spearman(div_v, P_v) = {spearman(lvl, P(f)):+.3f}")
print(f"(b) GROWTH: Spearman(g_v, P_v(1200)/P_v(300)) = {spearman(g_meas, g_pred):+.3f}")
print(f"    declared g_meas = {g_meas[:3].round(2)}  g_pred = {g_pred[:3].round(3)}")
print(f"    momx: measured {g_meas[0]:.1f} vs ceiling-growth {g_pred[0]:.3f} -- "
      f"{'ceiling explains' if g_pred[0] > 3 else 'ceiling does NOT explain the growth; the divergence field itself organized'}")
# permutation p for the strongest correlation
rng = np.random.default_rng(0)
obs = spearman(g_meas, g_pred)
null = [spearman(g_meas, rng.permutation(g_pred)) for _ in range(5000)]
print(f"(b) permutation p = {(np.sum(np.abs(null) >= abs(obs))+1)/5001:.4f}")
