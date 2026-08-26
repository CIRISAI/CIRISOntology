"""Does the low-noise I_C^(3) peak sit at an intrinsic operating point, or at the
finite-run crossover P_n ~ 1/(n*T)?

If the peak LOCATION halves when the run length T doubles, the peak marks the noise
level at which the run first stops being deterministic -- a property of how long we
ran, not of the rule. Batched over noise levels for speed.
"""
import sys, numpy as np
sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad')
import cupy as cp
import eca_spike as E
import eca_exact as X

NST = X.NST
IDX = cp.arange(NST, dtype=cp.int64)
BIT = [((IDX >> j) & 1) for j in range(X.N_CELLS)]
PN = [0.0] + [2.0 ** (-k) for k in range(17, 0, -1)]


def shares(v_batch, i, j, k):
    """I_C^(3) for every noise level in the batch."""
    key = 4 * BIT[i] + 2 * BIT[j] + BIT[k]
    P = v_batch.shape[0]
    out = cp.zeros((P, 8), dtype=cp.float64)
    for q in range(P):
        out[q] = cp.bincount(key, weights=v_batch[q], minlength=8)
    s, _, err, _ = E.shareK3_batch(out.reshape(P, 2, 2, 2))
    assert float(cp.asnumpy(err).max()) < 1e-12
    return cp.asnumpy(s)


CASES = [(25, (0, 1, 3), 'SPATIAL 1-2-14  (largest absolute peak)'),
         (46, (0, 1, 3), 'SPATIAL 1-2-14'),
         (58, (0, 1, 2), 'SPATIAL 1-1-15  (the 1886x rise)'),
         (110, (0, 1, 2), 'SPATIAL 1-1-15')]

print("Peak location vs run length T.  n = 17 cells, exact 2^17 propagation.")
print("A peak that tracks 1/(n*T) is a finite-run crossover, not an operating point.\n")
for rule, (i, j, k), tag in CASES:
    print(f"rule {rule:3d}  {tag}")
    for T in (100, 200, 400, 800):
        v, perm, idx = X.stationary_batch(rule, PN, T)
        a = shares(v, i, j, k)
        pk = int(a.argmax())
        print(f"    T={T:4d}  det={a[0]:.4e}  peak={a.max():.4e}  at P_n={PN[pk]:.4e}"
              f"   P_n*n*T = {PN[pk]*17*T:6.2f}")
    print()
