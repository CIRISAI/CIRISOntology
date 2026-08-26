"""EXHAUSTIVE search for a new quantum entropy inequality at n=4.

Space: every c in {-1,0,+1}^15 over the 15 independent entropies of a 4-party pure-plus-
purifier system. A candidate quantum inequality is c.S >= 0 for ALL quantum states.
Filter 1 (GPU): survive the whole structured state library.
Filter 2 (LP): NOT implied by the SSA cone.
Anything passing both is a candidate new quantum inequality. Expected: none — and an
exhaustive none is itself a citable bounded statement."""
import itertools, json, numpy as np, cupy as cp
from scipy.optimize import linprog
from state_library import SUBS
from n4_attack import known_inequalities

L = cp.asarray(np.load('state_library.npy').astype(np.float32))   # (K,15)
K, D = L.shape
print(f"library {K} x {D}")
A = known_inequalities(); print(f"SSA instances: {len(A)}")

TOT = 3**D
CH = 200_000
survivors = []
buf = cp.zeros((CH, D), dtype=cp.float32)
pw = np.array([3**i for i in range(D)], dtype=np.int64)
done = 0
while done < TOT:
    m = min(CH, TOT - done)
    idx = cp.arange(done, done + m, dtype=cp.int64)
    c = cp.zeros((m, D), dtype=cp.float32)
    t = idx.copy()
    for i in range(D):
        c[:, i] = (t % 3).astype(cp.float32) - 1.0
        t //= 3
    vals = c @ L.T                      # (m, K)
    ok = (vals.min(axis=1) >= -1e-6)
    ok &= (cp.abs(c).sum(axis=1) > 0)   # drop the zero vector
    w = cp.argwhere(ok).ravel()
    if w.size:
        for j in cp.asnumpy(w):
            survivors.append(cp.asnumpy(c[int(j)]).astype(int).tolist())
    done += m
    if (done // CH) % 15 == 0:
        print(f"  {done:,}/{TOT:,}  survivors so far {len(survivors):,}", flush=True)
print(f"\nFILTER 1 (state library): {len(survivors):,} of {TOT:,} survive")

notimp = []
for s in survivors:
    c = np.array(s, dtype=float)
    r = linprog(c=np.zeros(len(A)), A_eq=A.T, b_eq=c, bounds=[(0, None)]*len(A), method='highs')
    if not r.success:
        notimp.append(s)
print(f"FILTER 2 (implied by SSA): {len(notimp):,} survivors are NOT implied")
if notimp:
    f = lambda T: ''.join('ABCD'[x] for x in sorted(T))
    for s in notimp[:15]:
        pos = [f(SUBS[i]) for i in range(D) if s[i] > 0]
        neg = [f(SUBS[i]) for i in range(D) if s[i] < 0]
        print("   " + ' + '.join('S('+x+')' for x in pos) + '  >=  ' + ' + '.join('S('+x+')' for x in neg))
json.dump({'searched': TOT, 'survived_library': len(survivors), 'not_implied': notimp},
          open('exhaustive_results.json','w'))
