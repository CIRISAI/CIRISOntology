"""Refutation stage: test candidate quantum inequalities against real quantum states.
A single violating state is a self-contained certificate that the candidate is NOT a
quantum entropy inequality."""
import itertools, numpy as np
from quantum_candidates import sweep, fmt
rng = np.random.default_rng(20260823)

def vn(rho):
    ev = np.linalg.eigvalsh(rho); ev = ev[ev > 1e-12]
    return float(-(ev * np.log(ev)).sum())

def rdm(psi, dims, keep):
    n = len(dims)
    psi = psi.reshape(dims)
    keep = sorted(keep); tr = [i for i in range(n) if i not in keep]
    perm = keep + tr
    p = np.transpose(psi, perm).reshape(int(np.prod([dims[i] for i in keep])), -1)
    return p @ p.conj().T

def entropies(psi, dims, nparties):
    S = {}
    for k in range(1, nparties + 1):
        for c in itertools.combinations(range(nparties), k):
            S[frozenset(c)] = vn(rdm(psi, dims, list(c)))
    return S

def random_state(dims):
    v = rng.standard_normal(int(np.prod(dims))) + 1j*rng.standard_normal(int(np.prod(dims)))
    return v / np.linalg.norm(v)

def named_states(n):
    out = {}
    d = [2]*(n+1)
    D = 2**(n+1)
    ghz = np.zeros(D, complex); ghz[0] = ghz[-1] = 1/np.sqrt(2); out['GHZ'] = (ghz, d)
    w = np.zeros(D, complex)
    for i in range(n+1): w[1 << i] = 1
    out['W'] = (w/np.linalg.norm(w), d)
    prod = np.zeros(D, complex); prod[0] = 1; out['product'] = (prod, d)
    return out

def test(cands, n, ntrials=4000):
    viol = {}
    states = list(named_states(n).items())
    for name, (psi, dims) in states:
        S = entropies(psi, dims, n)
        for idx, (M, N, L, R) in enumerate(cands):
            if sum(S[t] for t in L) < sum(S[t] for t in R) - 1e-9:
                viol.setdefault(idx, []).append(name)
    for t in range(ntrials):
        dims = [int(x) for x in rng.integers(2, 4, size=n+1)]
        psi = random_state(dims)
        S = entropies(psi, dims, n)
        for idx, (M, N, L, R) in enumerate(cands):
            if idx in viol: continue
            if sum(S[t] for t in L) < sum(S[t] for t in R) - 1e-9:
                viol.setdefault(idx, []).append(f'random(dims={dims})')
    return viol

if __name__ == '__main__':
    n = 3
    cands = sweep(n, 3)
    print(f"testing {len(cands)} candidates from the n={n} sweep against quantum states...")
    v = test(cands, n)
    print(f"\nREFUTED: {len(v)} of {len(cands)}")
    print(f"SURVIVED: {len(cands)-len(v)}")
    if v:
        print("\nfirst refutations:")
        for idx in list(v)[:8]:
            M,N,L,R = cands[idx]
            print(f"   {' + '.join('S('+fmt(t)+')' for t in L)} >= {' + '.join('S('+fmt(t)+')' for t in R)}   killed by {v[idx][0]}")
    print(f"\nCONTROL READING: at n=3 the quantum cone is SSA+WM (Pippenger). Survivors must")
    print( "be consequences of those; refuted ones were never quantum inequalities.")
