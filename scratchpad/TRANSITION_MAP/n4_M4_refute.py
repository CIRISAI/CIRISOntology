"""Decisive stage: are the 200 not-implied M=4 candidates actually QUANTUM
inequalities, or merely holographic ones? A contraction map certifies holographic
validity only. MMI is the canonical example of a valid HEI that quantum states violate
(4-party GHZ kills it), so the expected outcome is mass refutation."""
import json, itertools, numpy as np
from n4_attack import vec, SUBS, evec
rng = np.random.default_rng(20260825)
NP = 4

res = json.load(open('n4_M4_results.json'))
cands = res['not_implied']
C = np.array([vec([set(t) for t in c['L']], [set(t) for t in c['R']]) for c in cands])
print(f"{len(C)} not-implied candidates under test")

alive = np.ones(len(C), bool)
def apply(psi, dims, tag):
    global alive
    S = evec(psi, dims)
    bad = (C @ S < -1e-9)
    n0 = alive.sum(); alive &= ~bad
    if alive.sum() < n0: print(f"  {tag}: killed {n0-alive.sum()}  (alive {alive.sum()})", flush=True)

D = 2**(NP+1)
g = np.zeros(D, complex); g[0] = g[-1] = 1/np.sqrt(2); apply(g, [2]*(NP+1), 'GHZ(5)')
w = np.zeros(D, complex)
for i in range(NP+1): w[1 << i] = 1
apply(w/np.linalg.norm(w), [2]*(NP+1), 'W(5)')
# 4-party GHZ with trivial purifier — the canonical MMI killer
g4 = np.zeros(2**NP, complex); g4[0] = g4[-1] = 1/np.sqrt(2)
apply(np.kron(g4, np.array([1.0, 0])), [2]*(NP+1), 'GHZ(4)xI')
# random states
for t in range(6000):
    dims = [int(x) for x in rng.integers(2, 4, size=NP+1)]
    v = rng.standard_normal(int(np.prod(dims))) + 1j*rng.standard_normal(int(np.prod(dims)))
    apply(v/np.linalg.norm(v), dims, f'random{t}' if t % 2000 == 0 else 'random')
    if not alive.any(): break

print(f"\nFINAL: {alive.sum()} of {len(C)} survive refutation")
if alive.any():
    print("SURVIVORS (candidate quantum inequalities not implied by SSA):")
    for i in np.where(alive)[0][:10]:
        c = cands[i]
        f = lambda T: ''.join('ABCD'[x] for x in T)
        print("   ", ' + '.join('S('+f(t)+')' for t in c['L']), '>=',
                   ' + '.join('S('+f(t)+')' for t in c['R']))
json.dump({'tested': len(C), 'survived': int(alive.sum()),
           'survivors': [cands[int(i)] for i in np.where(alive)[0]]},
          open('n4_M4_refute.json','w'))
