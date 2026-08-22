"""M=4 extension on the GPU.

The expensive part is the CSP, but a cheap NECESSARY condition kills most candidates
first: the boundary conditions themselves must be contracting. For the 5 subsystems
(4 parties + purifier) with occurrence bitstrings x_p (M bits, LHS) and y_p (N bits,
RHS), a contraction map can only exist if
    popcount(x_p XOR x_q) >= popcount(y_p XOR y_q)   for every pair p,q
and the map must be well defined: x_p == x_q  =>  y_p == y_q.
Both are pure bit arithmetic over millions of candidate pairs -> GPU.
Survivors go to the exact CPU backtracking checker."""
import itertools, json, time, numpy as np, cupy as cp
from quantum_candidates import subsets
from contraction import exists_contraction
from n4_attack import vec, known_inequalities
from scipy.optimize import linprog

NP = 4
terms = subsets(NP)                        # 15 non-empty subsets of {0,1,2,3}
tmask = np.array([sum(1 << p for p in t) for t in terms], dtype=np.int32)
parties = list(range(NP)) + ['O']

def occ_bits(combos, masks):
    """combos: (K, L) array of term indices -> (K, NP) occurrence bitstrings"""
    m = masks[combos]                                   # (K, L)
    out = cp.zeros((combos.shape[0], NP), dtype=cp.int32)
    for p in range(NP):
        bit = ((m >> p) & 1)                            # (K, L)
        weights = cp.array([1 << u for u in range(combos.shape[1])], dtype=cp.int32)
        out[:, p] = (bit * weights).sum(axis=1)
    return out

def popcount(x):
    x = x - ((x >> 1) & 0x55555555)
    x = (x & 0x33333333) + ((x >> 2) & 0x33333333)
    x = (x + (x >> 4)) & 0x0f0f0f0f
    return (x * 0x01010101) >> 24

L4 = np.array(list(itertools.combinations(range(15), 4)), dtype=np.int32)   # 1365
gmask = cp.asarray(tmask)
X = occ_bits(cp.asarray(L4), gmask)                     # (1365, 4) LHS bitstrings
survivors = []
t0 = time.time()
for N in (1, 2, 3, 4):
    RN = np.array(list(itertools.combinations(range(15), N)), dtype=np.int32)
    Y = occ_bits(cp.asarray(RN), gmask)                 # (|RN|, 4)
    print(f"N={N}: {len(L4)}x{len(RN)} = {len(L4)*len(RN):,} pairs", flush=True)
    # pairwise subsystem comparisons, including the all-zero purifier (index -1 handled
    # by comparing each x_p against 0 as well)
    keep_total = 0
    CH = 200
    for s in range(0, len(L4), CH):
        xb = X[s:s+CH]                                   # (c,4)
        c = xb.shape[0]
        ok = cp.ones((c, len(RN)), dtype=cp.bool_)
        for p in range(NP):
            for q in range(p+1, NP):
                dx = popcount(xb[:, p] ^ xb[:, q])[:, None]
                dy = popcount(Y[:, p] ^ Y[:, q])[None, :]
                ok &= (dx >= dy)
                ok &= ~((dx == 0) & (dy != 0))
            # purifier: x_O = y_O = 0
            dxo = popcount(xb[:, p])[:, None]
            dyo = popcount(Y[:, p])[None, :]
            ok &= (dxo >= dyo)
            ok &= ~((dxo == 0) & (dyo != 0))
        idx = cp.argwhere(ok)
        keep_total += int(idx.shape[0])
        for a, b in cp.asnumpy(idx):
            li, ri = L4[s+int(a)], RN[int(b)]
            if set(li) & set(ri): continue
            survivors.append((tuple(li), tuple(ri)))
    print(f"   boundary filter kept {keep_total:,} ({time.time()-t0:.0f}s)", flush=True)
print(f"\nGPU filter: {len(survivors):,} pairs survive to the exact CSP")
json.dump([[[int(x) for x in a],[int(x) for x in b]] for a,b in survivors], open("n4_M4_survivors.json","w"))
