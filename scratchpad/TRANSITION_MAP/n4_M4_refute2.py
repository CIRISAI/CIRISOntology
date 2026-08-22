"""Refutation, round 2 — with PRODUCT/DECOUPLED structures.

Round 1 was inadequate: random full-support pure states never decouple a subsystem.
The first 'survivor' was MMI + S(A), which is killed by making A pure and decoupled
while BCD+O violates MMI. Any refutation search that cannot produce that is too weak
to license a survivor claim."""
import json, itertools, numpy as np
from n4_attack import vec, SUBS, evec
rng = np.random.default_rng(20260826)
NP = 4

res = json.load(open('n4_M4_results.json'))
cands = res['not_implied']
C = np.array([vec([set(t) for t in c['L']], [set(t) for t in c['R']]) for c in cands])
alive = np.ones(len(C), bool)
print(f"{len(C)} candidates; round-1 survivors were {json.load(open('n4_M4_refute.json'))['survived']}")

def apply(psi, dims, tag):
    global alive
    S = evec(psi, dims); bad = (C @ S < -1e-9)
    n0 = alive.sum(); alive &= ~bad
    if alive.sum() < n0: print(f"  {tag}: killed {n0-alive.sum()} -> alive {alive.sum()}", flush=True)

def ghz(k):
    v = np.zeros(2**k, complex); v[0] = v[-1] = 1/np.sqrt(2); return v

def kron_all(vs):
    out = np.array([1.0+0j])
    for v in vs: out = np.kron(out, v)
    return out

one = np.array([1.0+0j, 0])
# GHZ on every subset of the 5 subsystems, the rest decoupled and pure
subsystems = list(range(NP+1))
for k in range(2, NP+2):
    for grp in itertools.combinations(subsystems, k):
        parts = []
        gv = ghz(k); gi = 0
        # build as tensor over subsystems in order, GHZ factor placed by reordering
        dims = [2]*(NP+1)
        psi = np.zeros(2**(NP+1), complex)
        for idx in range(2**k):
            # map GHZ basis index to full index
            bits = [(idx >> (k-1-j)) & 1 for j in range(k)]
            full = 0
            for j, s in enumerate(grp): full |= bits[j] << (NP - s)
            psi[full] += gv[idx]
        n = np.linalg.norm(psi)
        if n > 0: apply(psi/n, dims, f'GHZ{grp}')
        if not alive.any(): break
    if not alive.any(): break

# random states with a decoupled block
if alive.any():
    for t in range(4000):
        cut = rng.integers(1, NP+1)
        grp = tuple(sorted(rng.choice(subsystems, size=int(cut), replace=False)))
        rest = [s for s in subsystems if s not in grp]
        dims = [2]*(NP+1)
        a = rng.standard_normal(2**len(grp)) + 1j*rng.standard_normal(2**len(grp)); a/=np.linalg.norm(a)
        b = (rng.standard_normal(2**len(rest)) + 1j*rng.standard_normal(2**len(rest))) if rest else np.array([1.0+0j])
        if rest: b/=np.linalg.norm(b)
        psi = np.zeros(2**(NP+1), complex)
        for ia in range(2**len(grp)):
            bits_a = [(ia >> (len(grp)-1-j)) & 1 for j in range(len(grp))]
            for ib in range(2**len(rest)):
                bits_b = [(ib >> (len(rest)-1-j)) & 1 for j in range(len(rest))] if rest else []
                full = 0
                for j, s in enumerate(grp): full |= bits_a[j] << (NP - s)
                for j, s in enumerate(rest): full |= bits_b[j] << (NP - s)
                psi[full] = a[ia]*(b[ib] if rest else 1)
        apply(psi/np.linalg.norm(psi), dims, f'prod{t}' if t % 1500 == 0 else 'prod')
        if not alive.any(): break

print(f"\nROUND 2 FINAL: {alive.sum()} of {len(C)} survive")
if alive.any():
    for i in np.where(alive)[0][:8]:
        c = cands[i]; f = lambda T: ''.join('ABCD'[x] for x in T)
        print("   ", ' + '.join('S('+f(t)+')' for t in c['L']), '>=',
                   ' + '.join('S('+f(t)+')' for t in c['R']))
json.dump({'survived': int(alive.sum())}, open('n4_M4_refute2.json','w'))
