"""eca_omega_exact.py — Omega, Sigma and I_C^(3) from the SAME exact distribution.

Removes the estimator from both sides of the comparison: the paper's quantities and ours are
both computed from the exact 2^17-configuration stationary distribution, so any difference
between them is a difference between the measures, not between two estimators.
"""
import sys, os, json
import numpy as np, cupy as cp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eca_exact as X, eca_spike as E

N, NST = X.N_CELLS, X.NST


def H_exact(v):
    w = v[v > 0]
    return float(-(w * cp.log2(w)).sum())


def omega_exact(v):
    idx = cp.arange(NST, dtype=cp.int64)
    Hx = H_exact(v)
    H1 = 0.0
    for j in range(N):
        o = float(cp.sum(cp.where(((idx >> j) & 1) == 1, v, 0.0)))
        if 0 < o < 1:
            H1 += -(o * np.log2(o) + (1 - o) * np.log2(1 - o))
    Hm = 0.0
    for j in range(N):
        red = (idx & ((1 << j) - 1)) | ((idx >> (j + 1)) << j)
        Hm += H_exact(cp.bincount(red, weights=v, minlength=1 << (N - 1)))
    TC = H1 - Hx
    DTC = Hm - (N - 1) * Hx
    return dict(H=Hx, TC=TC, DTC=DTC, Omega=TC - DTC, Sigma=TC + DTC)


def main():
    rules = [int(x) for x in sys.argv[1:]] or [94, 163, 177, 131, 188, 110, 22, 28, 19, 18,
                                               46, 54, 97, 23, 178, 232, 130, 104]
    bitidx = [((cp.arange(NST, dtype=cp.int64) >> b) & 1) for b in range(N)]
    rows = []
    for rule in rules:
        for p in E.P_GRID:
            v, perm, idx = X.stationary(rule, p, 800)
            rec = dict(rule=rule, P_n=p, **omega_exact(v))
            for (d1, d2, d3) in E.SHAPES:
                rec[f'SPATIAL:{d1}-{d2}-{d3}'] = X.share_exact(
                    X.triple_from_v(v, 0, d1, d1 + d2, bitidx))
            aug = X.augmented_triples(v, perm, idx, p,
                                      [('TEMPORAL', [0], [0], [0])], bitidx)
            rec['TEMPORAL'] = X.share_exact(aug['TEMPORAL'])
            rows.append(rec)
        print(f"[omega-exact] rule {rule} done", flush=True)
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'eca_omega_exact.json'), 'w') as f:
            json.dump(rows, f, default=float)


if __name__ == '__main__':
    main()
