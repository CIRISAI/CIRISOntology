"""A structurally DIVERSE library of 4-party (+purifier) entropy vectors.

Round-1 failure taught the lesson: volume of random states is not coverage. What kills
candidates is STRUCTURE — decoupled subsystems, GHZ on subsets, stabilizer states. This
builds the library deliberately, then adds randomness on top."""
import itertools, numpy as np
NP = 4
SUBS = [frozenset(c) for k in range(1, NP+1) for c in itertools.combinations(range(NP), k)]

def vn(rho):
    ev = np.linalg.eigvalsh(rho); ev = ev[ev > 1e-12]
    return float(-(ev*np.log2(ev)).sum())

def rdm(psi, dims, keep):
    n=len(dims); psi=psi.reshape(dims); keep=sorted(keep)
    tr=[i for i in range(n) if i not in keep]
    p=np.transpose(psi, keep+tr).reshape(int(np.prod([dims[i] for i in keep])),-1)
    return p@p.conj().T

def evec(psi, dims):
    return np.array([vn(rdm(psi, dims, sorted(s))) for s in SUBS])

def place(vec_on_grp, grp, nsub, d=2):
    """embed a state on subsystems `grp` into the full nsub-subsystem space"""
    psi = np.zeros(d**nsub, complex)
    k = len(grp)
    for idx in range(d**k):
        bits = [(idx // d**(k-1-j)) % d for j in range(k)]
        full = 0
        for j, s in enumerate(grp): full += bits[j] * d**(nsub-1-s)
        psi[full] += vec_on_grp[idx]
    return psi

def build(rng, n_random=3000):
    nsub = NP+1
    lib = []
    def add(psi, dims):
        n=np.linalg.norm(psi)
        if n>1e-9: lib.append(evec(psi/n, dims))
    dims=[2]*nsub
    # 1. GHZ and W on every subset of subsystems, rest decoupled
    for k in range(2, nsub+1):
        for grp in itertools.combinations(range(nsub), k):
            g=np.zeros(2**k,complex); g[0]=g[-1]=1/np.sqrt(2); add(place(g,grp,nsub),dims)
            w=np.zeros(2**k,complex)
            for i in range(k): w[1<<i]=1
            add(place(w/np.linalg.norm(w),grp,nsub),dims)
    # 2. products of Bell pairs across all pairings
    for pairing in itertools.combinations(itertools.combinations(range(nsub),2), 2):
        (a,b),(c,d)=pairing
        if len({a,b,c,d})<4: continue
        bell=np.array([1,0,0,1],complex)/np.sqrt(2)
        psi=place(bell,(a,b),nsub); psi2=place(bell,(c,d),nsub)
        full=np.zeros(2**nsub,complex)
        for i in range(2**nsub):
            full[i]=psi[i]*psi2[i] if False else 0
        # build properly by tensoring index-wise
        full=np.zeros(2**nsub,complex)
        for x in range(4):
            for y in range(4):
                bx=[(x>>1)&1,x&1]; by=[(y>>1)&1,y&1]
                idx=0
                for j,s in enumerate((a,b)): idx |= bx[j]<<(nsub-1-s)
                for j,s in enumerate((c,d)): idx |= by[j]<<(nsub-1-s)
                full[idx]+=bell[x]*bell[y]
        add(full,dims)
    # 3. random stabilizer-ish: random Clifford-free graph states on subsets
    for k in range(2, nsub+1):
        for grp in itertools.combinations(range(nsub), k):
            for _ in range(6):
                edges=[(i,j) for i in range(k) for j in range(i+1,k) if rng.random()<0.5]
                v=np.ones(2**k,complex)/np.sqrt(2**k)
                for idx in range(2**k):
                    b=[(idx>>(k-1-j))&1 for j in range(k)]
                    s=sum(b[i]*b[j] for i,j in edges)
                    v[idx]*=(-1)**s
                add(place(v,grp,nsub),dims)
    # 4. random states with a decoupled block
    for _ in range(n_random//2):
        cut=int(rng.integers(1,nsub))
        grp=tuple(sorted(rng.choice(range(nsub),size=cut,replace=False)))
        rest=[s for s in range(nsub) if s not in grp]
        a=rng.standard_normal(2**len(grp))+1j*rng.standard_normal(2**len(grp)); a/=np.linalg.norm(a)
        pa=place(a,grp,nsub)
        if rest:
            b=rng.standard_normal(2**len(rest))+1j*rng.standard_normal(2**len(rest)); b/=np.linalg.norm(b)
            pb=place(b,rest,nsub)
            full=np.zeros(2**nsub,complex)
            for i in range(2**nsub):
                ga=0; gb=0
                for j,s in enumerate(grp): ga |= ((i>>(nsub-1-s))&1)<<(len(grp)-1-j)
                for j,s in enumerate(rest): gb |= ((i>>(nsub-1-s))&1)<<(len(rest)-1-j)
                full[i]=a[ga]*b[gb]
            add(full,dims)
        else: add(pa,dims)
    # 5. random full-support, mixed local dimensions
    for _ in range(n_random//2):
        dd=[int(x) for x in rng.integers(2,4,size=nsub)]
        v=rng.standard_normal(int(np.prod(dd)))+1j*rng.standard_normal(int(np.prod(dd)))
        add(v/np.linalg.norm(v),dd)
    return np.array(lib)

if __name__=='__main__':
    rng=np.random.default_rng(20260827)
    L=build(rng)
    np.save('state_library.npy', L)
    print(f"library: {L.shape[0]} entropy vectors x {L.shape[1]} components")
    # sanity: SSA and MMI behaviour
    i=lambda s: SUBS.index(frozenset(s))
    ssa=L[:,i([0,1])]+L[:,i([1,2])]-L[:,i([1])]-L[:,i([0,1,2])]
    mmi=L[:,i([0,1])]+L[:,i([0,2])]+L[:,i([1,2])]-L[:,i([0])]-L[:,i([1])]-L[:,i([2])]-L[:,i([0,1,2])]
    print(f"  SSA min over library = {ssa.min():+.4f}  (must be >= 0)")
    print(f"  MMI min over library = {mmi.min():+.4f}  (MUST be < 0 — library can kill MMI)")
