"""n=4: refute candidates by quantum states, then test whether survivors are IMPLIED
by the known quantum inequalities (all SSA instances on the purified 5-subsystem system,
which subsume weak monotonicity, subadditivity and Araki-Lieb).

A survivor that is NOT implied would be a candidate NEW quantum entropy inequality.
Expected outcome, stated before running: everything is implied. That is the honest
prior — no new unconstrained quantum inequality has been found since Pippenger."""
import itertools, json, numpy as np
from scipy.optimize import linprog
rng = np.random.default_rng(20260824)
NP = 4                                     # parties A,B,C,D ; subsystem 4 = purifier O
SUBS = [frozenset(c) for k in range(1, NP+1) for c in itertools.combinations(range(NP), k)]
IDX = {s: i for i, s in enumerate(SUBS)}   # 15 independent entropies

def canon(T):
    """entropy of any subset of {0..4} on a globally pure state -> index in SUBS"""
    T = set(T)
    if NP in T: T = set(range(NP)) - (T - {NP})
    T = frozenset(T)
    return None if not T else IDX[T]

def vec(plus, minus):
    v = np.zeros(len(SUBS))
    for T in plus:
        i = canon(T)
        if i is not None: v[i] += 1
    for T in minus:
        i = canon(T)
        if i is not None: v[i] -= 1
    return v

def known_inequalities():
    """all SSA instances over the 5 subsystems (subsumes WM/SA/AL on a pure state)"""
    out, seen = [], set()
    allsub = list(range(NP+1))
    for X in itertools.chain.from_iterable(itertools.combinations(allsub, k) for k in range(1, NP+1)):
        rest1 = [s for s in allsub if s not in X]
        for Y in itertools.chain.from_iterable(itertools.combinations(rest1, k) for k in range(1, len(rest1)+1)):
            rest2 = [s for s in rest1 if s not in Y]
            for Z in itertools.chain.from_iterable(itertools.combinations(rest2, k) for k in range(1, len(rest2)+1)):
                v = vec([set(X)|set(Y), set(Y)|set(Z)], [set(Y), set(X)|set(Y)|set(Z)])
                key = tuple(v)
                if key not in seen and any(v):
                    seen.add(key); out.append(v)
    return np.array(out)

def vn(rho):
    ev = np.linalg.eigvalsh(rho); ev = ev[ev > 1e-12]
    return float(-(ev*np.log(ev)).sum())

def rdm(psi, dims, keep):
    n=len(dims); psi=psi.reshape(dims); keep=sorted(keep)
    tr=[i for i in range(n) if i not in keep]
    p=np.transpose(psi, keep+tr).reshape(int(np.prod([dims[i] for i in keep])), -1)
    return p@p.conj().T

def evec(psi, dims):
    return np.array([vn(rdm(psi, dims, sorted(s))) for s in SUBS])

if __name__ == '__main__':
    cands = json.load(open('n4_candidates.json'))
    C = np.array([vec([set(t) for t in c['L']], [set(t) for t in c['R']]) for c in cands])
    print(f"{len(C)} candidates loaded")
    # ---- stage A: refutation by quantum states
    alive = np.ones(len(C), bool)
    special = []
    D=2**(NP+1)
    g=np.zeros(D,complex); g[0]=g[-1]=1/np.sqrt(2); special.append((g,[2]*(NP+1)))
    w=np.zeros(D,complex)
    for i in range(NP+1): w[1<<i]=1
    special.append((w/np.linalg.norm(w),[2]*(NP+1)))
    for psi,dims in special:
        S=evec(psi,dims); alive &= (C@S >= -1e-9)
    for t in range(3000):
        dims=[int(x) for x in rng.integers(2,4,size=NP+1)]
        v=rng.standard_normal(int(np.prod(dims)))+1j*rng.standard_normal(int(np.prod(dims)))
        S=evec(v/np.linalg.norm(v),dims)
        alive &= (C@S >= -1e-9)
        if t%1000==999: print(f"  refutation pass {t+1}: {alive.sum()} still alive")
    print(f"\nSTAGE A: refuted {len(C)-alive.sum()}, survived {alive.sum()}")
    # ---- stage B: implication by known inequalities
    A = known_inequalities()
    print(f"STAGE B: testing implication against {len(A)} distinct SSA instances")
    surv = np.where(alive)[0]
    not_implied = []
    for k, i in enumerate(surv):
        c = C[i]
        res = linprog(c=np.zeros(len(A)), A_eq=A.T, b_eq=c,
                      bounds=[(0, None)]*len(A), method='highs')
        if not res.success:
            not_implied.append(i)
    print(f"\nRESULT: {len(not_implied)} of {len(surv)} survivors are NOT implied by SSA/WM")
    if not_implied:
        print("  candidates for NEW quantum inequalities (first 5):")
        for i in not_implied[:5]:
            c=cands[i]
            f=lambda T: ''.join('ABCD'[x] for x in T)
            print("   ", ' + '.join('S('+f(t)+')' for t in c['L']), '>=',
                       ' + '.join('S('+f(t)+')' for t in c['R']))
    json.dump({'n_candidates':len(C),'survived':int(alive.sum()),
               'not_implied':[int(x) for x in not_implied]}, open('n4_attack_results.json','w'))
