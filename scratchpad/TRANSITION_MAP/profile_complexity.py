"""Complete bath-profile complexity stress test.

Preregistered in PROFILE_COMPLEXITY_PREREG.md before this file existed.
Tests whether finite-time approximate bath-equivalence survives increasing
coordinate count and spatial roughness.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import expm_multiply

HERE=Path(__file__).resolve().parent
SEED=20260822
NS=[256,512,1024]
RS=[2,4,8,16,32]
GS=[8,16,32,64,128,256]
FAMILIES=['FOURIER-SMOOTH','FOURIER-ROUGH','RANDOM-FEATURE','IID-PROFILES']
T=20.; NSTEPS=200; DT=T/NSTEPS; TOL=1e-3
rng0=np.random.default_rng(SEED)
# Freeze a maximal temporal bank once; prefix used for each r. Scale each prefix to unit total RMS amplitude.
TEMP_FREQS=rng0.uniform(.35,2.35,size=(32,2))
TEMP_PHASES=rng0.uniform(0,2*np.pi,size=(32,2))
TEMP_AMPS=rng0.uniform(.5,1.,size=(32,2))

def xi_r(t,r):
    a=TEMP_AMPS[:r]; f=TEMP_FREQS[:r]; p=TEMP_PHASES[:r]
    x=np.sum(a*np.cos(f*t+p),axis=1)
    # deterministic normalization so mean coordinate power sum is approximately one
    norm=math.sqrt(float(np.sum(np.sum(a*a,axis=1)/2)))
    return x/max(norm,1e-15)

def normalize_cols(A):
    A=A-A.mean(axis=0,keepdims=True)
    rms=np.sqrt(np.mean(A*A,axis=0)); rms[rms<1e-12]=1
    return A/rms

def make_profiles(n,r,family):
    th=2*np.pi*np.arange(n)/n
    cols=[]
    if family=='FOURIER-SMOOTH':
        for k in range(1,r//2+1): cols += [np.cos(k*th),np.sin(k*th)]
        A=np.column_stack(cols)[:,:r]
    elif family=='FOURIER-ROUGH':
        ks=np.unique(np.maximum(1,np.round(np.geomspace(2,max(2,n//4),num=max(1,r//2))).astype(int)))
        while len(ks)<r//2: ks=np.r_[ks, min(n//4,ks[-1]+1)]
        for k in ks[:r//2]: cols += [np.cos(k*th),np.sin(k*th)]
        A=np.column_stack(cols)[:,:r]
    elif family=='RANDOM-FEATURE':
        rng=np.random.default_rng(SEED+17*n+101*r)
        for j in range(r):
            ks=np.arange(1,9); coef=rng.normal(size=8)/(ks**1.5); phase=rng.uniform(0,2*np.pi,size=8)
            cols.append(sum(coef[k-1]*np.cos(k*th+phase[k-1]) for k in ks))
        A=np.column_stack(cols)
    elif family=='IID-PROFILES':
        rng=np.random.default_rng(SEED+31*n+211*r); A=rng.normal(size=(n,r)); A/=np.linalg.norm(A,axis=1,keepdims=True)
        return A
    else: raise ValueError(family)
    return normalize_cols(A)

def arrowhead(energies,weights):
    m=len(energies); rows=list(range(1,m+1)); cols=rows.copy(); vals=list(energies.astype(float))
    for j,g in enumerate(weights,start=1): rows.extend([0,j]); cols.extend([j,0]); vals.extend([float(g),float(g)])
    return csr_matrix((vals,(rows,cols)),shape=(m+1,m+1),dtype=complex)

def propagate(A,weights):
    q=np.zeros(len(A)+1,complex); q[0]=1; pops=[1.]
    r=A.shape[1]
    for s in range(NSTEPS):
        H=arrowhead(A@xi_r((s+.5)*DT,r),weights)
        q=expm_multiply((-1j*DT)*H,q,traceA=(-1j*DT)*H.diagonal().sum())
        pops.append(float(abs(q[0])**2))
    return np.asarray(pops)

def farthest_seeds(A,G):
    # deterministic: first seed = lexicographically smallest row; then farthest point
    first=int(np.lexsort(A.T[::-1])[0]); idx=[first]
    d2=np.sum((A-A[first])**2,axis=1)
    for _ in range(1,G):
        j=int(np.argmax(d2)); idx.append(j); d2=np.minimum(d2,np.sum((A-A[j])**2,axis=1))
    return A[idx].copy()

def kmeans(A,G,maxiter=100):
    C=farthest_seeds(A,G)
    ids=np.zeros(len(A),int)
    for _ in range(maxiter):
        d=((A[:,None,:]-C[None,:,:])**2).sum(axis=2); new=np.argmin(d,axis=1)
        Cnew=C.copy()
        for g in range(G):
            m=new==g
            if m.any(): Cnew[g]=A[m].mean(0)
        if np.array_equal(new,ids) and np.max(np.abs(Cnew-C))<1e-12: ids=new; C=Cnew; break
        ids=new; C=Cnew
    # remove empty clusters
    keep=np.unique(ids); rem=-np.ones(G,int); rem[keep]=np.arange(len(keep)); ids=rem[ids]; C=np.array([A[ids==g].mean(0) for g in range(len(keep))])
    sizes=np.array([(ids==g).sum() for g in range(len(C))])
    radius=float(np.max(np.linalg.norm(A-C[ids],axis=1)))
    return C,sizes,ids,radius

def run_cell(n,r,family):
    A=make_profiles(n,r,family); truth=propagate(A,np.full(n,1/math.sqrt(n))); rows={}
    for G in GS:
        if G>n: continue
        C,sizes,ids,rad=kmeans(A,G); pred=propagate(C,np.sqrt(sizes/n)); err=float(np.max(np.abs(pred-truth)))
        rows[str(G)]={'max_pop_error':err,'covering_radius':rad,'classes':int(len(C))}
        print(n,r,family,'G',G,'err',f'{err:.3e}','rad',f'{rad:.3e}',flush=True)
    passing=[int(g) for g,v in rows.items() if v['max_pop_error']<=TOL]
    return {'rows':rows,'min_G_1e-3':min(passing) if passing else None}

def relabel_gate():
    n=256;r=2;A=make_profiles(n,r,'FOURIER-SMOOTH'); truth=propagate(A,np.full(n,1/math.sqrt(n)))
    perm=(37*np.arange(n)+11)%n; B=A[perm]; truth2=propagate(B,np.full(n,1/math.sqrt(n))); worst=float(np.max(np.abs(truth-truth2)))
    for G in GS:
        C,s,_,_=kmeans(A,G); D,t,_,_=kmeans(B,G); p=propagate(C,np.sqrt(s/n)); q=propagate(D,np.sqrt(t/n)); worst=max(worst,float(np.max(np.abs(p-q))))
    return worst

def main():
    cells={}
    for n in NS:
        for r in RS:
            for fam in FAMILIES:
                cells[f'N{n}_r{r}_{fam}']=run_cell(n,r,fam)
    # singleton machine-floor gate on one representative full-profile cell
    A=make_profiles(256,2,'FOURIER-SMOOTH'); p=propagate(A,np.full(256,1/16)); q=propagate(A.copy(),np.full(256,1/16)); c3=float(np.max(np.abs(p-q)))
    c2=relabel_gate()
    # C1 prior r=2 smooth was G64; one grid step tolerance means 32..128
    c1=all(cells[f'N{n}_r2_FOURIER-SMOOTH']['min_G_1e-3'] in [32,64,128] for n in NS)
    def mg(n,r,f): return cells[f'N{n}_r{r}_{f}']['min_G_1e-3']
    p1=True
    for r in [2,4,8,16]:
        vals=[mg(n,r,'FOURIER-SMOOTH') for n in NS]
        p1 &= all(v is not None and v<=128 for v in vals) and max(vals)<=2*min(vals)
    g2=mg(1024,2,'FOURIER-SMOOTH'); g16=mg(1024,16,'FOURIER-SMOOTH'); p2=bool(g2 and g16 and g16<=4*g2)
    comps=[]
    for n in NS:
        for r in RS:
            a=mg(n,r,'FOURIER-SMOOTH'); b=mg(n,r,'FOURIER-ROUGH'); comps.append(bool(a and b and b>a))
    p3=sum(comps)>len(comps)/2
    iid=mg(1024,8,'IID-PROFILES'); p4=bool(iid is None or iid>=512)
    out={'prereg':'PROFILE_COMPLEXITY_PREREG.md','temporal_bank':{'seed':SEED,'freqs':TEMP_FREQS.tolist(),'phases':TEMP_PHASES.tolist(),'amps':TEMP_AMPS.tolist()},'cells':cells,'gates':{'C1_r2_prior_consistent':c1,'C2_relabel_max_mismatch':c2,'C3_singleton_error':c3},'stakes':{'P1_bounded_smooth':bool(p1),'P2_coordinate_scaling':p2,'P3_rough_majority_harder':p3,'P4_IID_negative_control':p4,'N1024_G_r2_smooth':g2,'N1024_G_r16_smooth':g16,'N1024_G_r8_IID':iid}}
    (HERE/'profile_complexity_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('GATES',json.dumps(out['gates'],indent=2)); print('STAKES',json.dumps(out['stakes'],indent=2))
if __name__=='__main__': main()
