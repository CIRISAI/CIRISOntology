"""PGX-1 Arm 3 — the two-excitation sector. Frozen construction per
POLARITON_GPU_EXT_PREREG.md Arm 3. Runs only after Arms 1-2 complete.

Basis: |2c> + |1c,e_i> (N) + |e_i e_j> (i<j).  H = wc a+a + sum w_i s_i+ s_i-
+ sum g_i (a+ s_i- + a s_i+).  Bosonic factor sqrt(2) on the two-photon leg.
Initial state |2c>; observable = two-photon population."""
import json, math, time
import numpy as np, cupy as cp
from scipy.special import jv
from scipy.linalg import eigh as dense_eigh

TIMES = np.linspace(0.0, 20.0, 201); TOL = 1e-4
BS = [1,2,4,8,16,32,64,128,256]
TAUS = [0.0,0.001,0.003,0.01,0.03,0.1,0.3,1.0,3.0]
S2 = math.sqrt(2.0)

def h_apply(c2, phi, Psi, w, g):
    """Psi is the symmetric N x N pair amplitude with zero diagonal."""
    new_c2 = S2*(g @ phi)
    new_phi = w*phi + S2*g*c2 + (Psi @ g)
    new_Psi = (w[:,None] + w[None,:])*Psi + cp.outer(g, phi) + cp.outer(phi, g)
    cp.fill_diagonal(new_Psi, 0)
    return new_c2, new_phi, new_Psi

def cheb_two(w_h, g_h, times=TIMES):
    N = len(w_h)
    w = cp.asarray(w_h); g = cp.asarray(g_h)
    b = float(2*np.max(np.abs(w_h)) + 2.0)     # ||H|| <= 2max|w| + 2G
    dt = float(times[1]-times[0]); bt = b*dt
    K = 4
    while abs(jv(K, bt)) > 1e-17 and K < 400: K += 1
    K = max(K, 8)
    coef = cp.asarray(np.array([jv(k, bt)*(1 if k==0 else 2*(-1j)**k) for k in range(K+1)]))
    c2 = cp.array(1.0+0j); phi = cp.zeros(N, cp.complex128); Psi = cp.zeros((N,N), cp.complex128)
    out=[1.0+0j]
    for _ in range(len(times)-1):
        a0=(c2,phi,Psi)
        a1=tuple(x/b for x in h_apply(c2,phi,Psi,w,g))
        r=[coef[0]*a0[i]+coef[1]*a1[i] for i in range(3)]
        for k in range(2,K+1):
            hh=tuple(x/b for x in h_apply(*a1,w,g))
            a2=tuple(2*hh[i]-a0[i] for i in range(3))
            r=[r[i]+coef[k]*a2[i] for i in range(3)]
            a0,a1=a1,a2
        c2,phi,Psi=r
        out.append(complex(c2.get()))
    return np.abs(np.array(out))**2

def reduce_pop(wr, gr):
    """Exact two-excitation population for a reduced emitter set (dense)."""
    n=len(wr)
    dim=1+n+n*(n-1)//2
    idx={}; k=1+n
    for i in range(n):
        for j in range(i+1,n): idx[(i,j)]=k; k+=1
    H=np.zeros((dim,dim))
    for i in range(n):
        H[1+i,1+i]=wr[i]; H[0,1+i]=S2*gr[i]; H[1+i,0]=S2*gr[i]
        for j in range(i+1,n):
            p=idx[(i,j)]
            H[p,p]=wr[i]+wr[j]
            H[p,1+j]=gr[i]; H[1+j,p]=gr[i]
            H[p,1+i]=gr[j]; H[1+i,p]=gr[j]
    ev,V=dense_eigh(H); wt=np.abs(V[0,:])**2
    return np.abs(np.exp(-1j*np.outer(TIMES,ev)) @ wt)**2

def rmse(x,y): return float(np.sqrt(np.mean((np.asarray(x)-np.asarray(y))**2)))

def bin_reduce(ws, gs, B):
    n=len(ws); idx=np.linspace(0,n,B+1).astype(int); w2=gs**2
    wr=np.empty(B); gr=np.empty(B)
    for b in range(B):
        s,e=idx[b],idx[b+1]; m=w2[s:e].sum()
        wr[b]=(w2[s:e]*ws[s:e]).sum()/m; gr[b]=math.sqrt(m)
    return wr,gr

def tau_clusters(ws,gs,tau):
    n=len(ws); starts=[]; i=0
    while i<n:
        starts.append(i)
        j=np.searchsorted(ws,ws[i]+2*tau,side='right')-1
        i=max(j,i)+1
    starts=np.array(starts); w2=gs**2
    cm=np.concatenate(([0.],np.cumsum(w2))); cw=np.concatenate(([0.],np.cumsum(w2*ws)))
    ends=np.concatenate((starts[1:],[n])); m=cm[ends]-cm[starts]
    return (cw[ends]-cw[starts])/m, np.sqrt(m), len(starts)

if __name__=='__main__':
    rows=[]
    for N in (128,256,512):
        for s in (0.3,1.0):
            rng=np.random.default_rng(20260824+N+int(s*10))
            w=rng.normal(0,s,N); g=np.full(N,1/math.sqrt(N))
            t0=time.time(); truth=cheb_two(w,g); tt=time.time()-t0
            o=np.argsort(w); ws=w[o]; gs=g[o]
            bmin=None
            for B in BS:
                if B>N or B>140: break
                wr,gr=bin_reduce(ws,gs,B)
                if rmse(reduce_pop(wr,gr),truth)<=TOL: bmin=B; break
            cmin=None
            for tau in TAUS:
                if tau==0.0: continue
                wr,gr,k=tau_clusters(ws,gs,tau)
                if k>140: continue
                if rmse(reduce_pop(wr,gr),truth)<=TOL and (cmin is None or k<cmin): cmin=k
            rows.append({'N':N,'sigma':s,'B_min':bmin,'C_min':cmin,'t_truth':tt})
            print(f"N={N} s={s}: B={bmin} C={cmin} (truth {tt:.1f}s)",flush=True)
    json.dump(rows,open('pgx1_arm3.json','w'),indent=1)
