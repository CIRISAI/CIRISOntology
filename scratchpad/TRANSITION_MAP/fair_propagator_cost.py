"""Fair common-kernel cost comparison for FULL vs profile-class propagation.

Preregistered in FAIR_PROPAGATOR_COST_PREREG.md before this file existed.
Both arms use the same restarted Arnoldi implementation and frozen midpoint grid.
"""
from __future__ import annotations
import json, math, time
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import expm_multiply

HERE=Path(__file__).resolve().parent
NS=[256,512,1024]
GS=[16,32,64,128]
MS=[2,3,4,6,8,12]
T=20.; NSTEPS=200; DT=T/NSTEPS; TOL=1e-3

def xi(t):
    return np.array([.5*math.cos(.7*t)+.2*math.cos(1.9*t),.5*math.sin(.7*t)+.2*math.sin(1.3*t)])

def profiles(n,scrambled=False):
    th=2*np.pi*np.arange(n)/n; A=np.c_[np.cos(th),np.sin(th)]
    if scrambled: A=A[(37*np.arange(n)+11)%n]
    return A

def H_arrow(A,w,t):
    d=len(A); en=A@xi(t)
    rows=list(range(1,d+1)); cols=rows.copy(); vals=list(en.astype(float))
    for j,g in enumerate(w,start=1): rows.extend([0,j]); cols.extend([j,0]); vals.extend([float(g),float(g)])
    return csr_matrix((vals,(rows,cols)),shape=(d+1,d+1),dtype=complex)

def truth(A):
    n=len(A); w=np.full(n,1/math.sqrt(n)); q=np.zeros(n+1,complex); q[0]=1; out=[1.]
    for s in range(NSTEPS):
        H=H_arrow(A,w,(s+.5)*DT); q=expm_multiply((-1j*DT)*H,q,traceA=(-1j*DT)*H.diagonal().sum()); out.append(float(abs(q[0])**2))
    return np.asarray(out)

def class_model(A,G):
    t0=time.perf_counter()
    ang=np.mod(np.arctan2(A[:,1],A[:,0]),2*np.pi); ids0=np.minimum(np.floor(G*ang/(2*np.pi)+1e-12).astype(int),G-1)
    means=[]; sizes=[]
    for k in range(G):
        mask=ids0==k
        if mask.any(): means.append(A[mask].mean(0)); sizes.append(mask.sum())
    elapsed=time.perf_counter()-t0
    means=np.asarray(means); sizes=np.asarray(sizes)
    return means,np.sqrt(sizes/len(A)),elapsed

def arnoldi_step(H,q,m):
    beta=float(np.linalg.norm(q)); n=len(q)
    if beta==0: return q.copy(),0,0
    V=np.zeros((n,m),complex); K=np.zeros((m,m),complex); V[:,0]=q/beta
    mv=0; orth=0; k=m
    for j in range(m):
        z=H@V[:,j]; mv+=1
        for i in range(j+1):
            hij=np.vdot(V[:,i],z); K[i,j]=hij; z-=hij*V[:,i]; orth+=1
        if j+1<m:
            hn=float(np.linalg.norm(z)); K[j+1,j]=hn
            if hn<1e-14: k=j+1; break
            V[:,j+1]=z/hn
    y=np.zeros(k,complex); y[0]=beta; y=expm((-1j*DT)*K[:k,:k])@y
    return V[:,:k]@y,mv,orth

def run(A,w,m):
    q=np.zeros(len(A)+1,complex); q[0]=1; out=[1.]; proxy=0; total_mv=0; total_orth=0
    for s in range(NSTEPS):
        H=H_arrow(A,w,(s+.5)*DT); q,mv,orth=arnoldi_step(H,q,m); out.append(float(abs(q[0])**2))
        dim=H.shape[0]; proxy += mv*H.nnz + 2*dim*orth; total_mv+=mv; total_orth+=orth
    return np.asarray(out),{'C_proxy':int(proxy),'matvecs':int(total_mv),'orth_pairs':int(total_orth),'dimension':int(len(A)+1),'m':int(m)}

def timed(A,w,m,repeats=3):
    run(A,w,m) # warmup
    vals=[]
    for _ in range(repeats):
        t=time.perf_counter(); run(A,w,m); vals.append(time.perf_counter()-t)
    return {'repeats_s':vals,'median_s':float(np.median(vals))}

def eval_family(n,scrambled=False):
    A=profiles(n,scrambled); tr=truth(A); full={}; classes={}
    fw=np.full(n,1/math.sqrt(n))
    for m in MS:
        p,c=run(A,fw,m); c['max_pop_error']=float(np.max(np.abs(p-tr))); full[str(m)]=c
    constructions={}
    for G in GS:
        C,w,ct=class_model(A,G); constructions[str(G)]={'construction_s':ct,'dimension':len(C)+1}; classes[str(G)]={}
        for m in MS:
            p,c=run(C,w,m); c['max_pop_error']=float(np.max(np.abs(p-tr))); classes[str(G)][str(m)]=c
    fpass=[v for v in full.values() if v['max_pop_error']<=TOL]
    cpass=[v|{'G':int(G)} for G,dd in classes.items() for v in dd.values() if v['max_pop_error']<=TOL]
    fbest=min(fpass,key=lambda x:x['C_proxy']) if fpass else None
    cbest=min(cpass,key=lambda x:x['C_proxy']) if cpass else None
    timing={}
    if not scrambled and fbest and cbest:
        timing['FULL']=timed(A,fw,fbest['m'])
        C,w,ct=class_model(A,cbest['G']); timing['CLASS']=timed(C,w,cbest['m']); timing['class_construction_s']=ct
        timing['class_total_one_trajectory_s']=timing['CLASS']['median_s']+ct
        timing['break_even_trajectories']=1 if timing['CLASS']['median_s']>=timing['FULL']['median_s'] else float(max(1,math.ceil(ct/max(timing['FULL']['median_s']-timing['CLASS']['median_s'],1e-15))))
    print('N',n,'scrambled',scrambled,'FULL',None if fbest is None else (fbest['m'],fbest['C_proxy'],fbest['max_pop_error']),'CLASS',None if cbest is None else (cbest['G'],cbest['m'],cbest['C_proxy'],cbest['max_pop_error']),flush=True)
    return {'full':full,'classes':classes,'constructions':constructions,'best_full':fbest,'best_class':cbest,'timing':timing}

def main():
    cells={}; smooth={}; scrambled={}
    for n in NS:
        smooth[str(n)]=eval_family(n,False); scrambled[str(n)]=eval_family(n,True)
    mismatch=0.0
    for n in NS:
        for m in MS: mismatch=max(mismatch,abs(smooth[str(n)]['full'][str(m)]['max_pop_error']-scrambled[str(n)]['full'][str(m)]['max_pop_error']))
        for G in GS:
            for m in MS: mismatch=max(mismatch,abs(smooth[str(n)]['classes'][str(G)][str(m)]['max_pop_error']-scrambled[str(n)]['classes'][str(G)][str(m)]['max_pop_error']))
    fpc1=all(smooth[str(n)]['best_full'] is not None and smooth[str(n)]['best_full']['m']<=4 for n in NS)
    # FPC2: at G128,m12, common Arnoldi should lie within 1e-5 of intrinsic class error recorded in approx result scale; compare to high-m same class model isn't external, so require convergence across m8/12 <1e-5.
    fpc2=all(abs(smooth[str(n)]['classes']['128']['12']['max_pop_error']-smooth[str(n)]['classes']['128']['8']['max_pop_error'])<1e-5 for n in NS)
    ratios={str(n):smooth[str(n)]['best_class']['C_proxy']/smooth[str(n)]['best_full']['C_proxy'] for n in NS}
    p1=ratios['1024']<=.5; p2=ratios['1024']<ratios['256'] and max(smooth[str(n)]['best_class']['G'] for n in NS)<=2*min(smooth[str(n)]['best_class']['G'] for n in NS)
    tm=smooth['1024']['timing']; p3=bool(tm and tm['class_total_one_trajectory_s']<=.8*tm['FULL']['median_s'])
    out={'prereg':'FAIR_PROPAGATOR_COST_PREREG.md','smooth':smooth,'scrambled':scrambled,'gates':{'FPC1_full_m_le4':fpc1,'FPC2_class_m_converged':fpc2,'FPC3_relabel_max_error_mismatch':mismatch},'stakes':{'P1_N1024_class_cost_le_half_full':bool(p1),'P2_cost_ratio_decreases_with_N':bool(p2),'P3_N1024_walltime':p3,'P4_break_even_trajectories_N1024':tm.get('break_even_trajectories') if tm else None,'cost_ratio_class_over_full':ratios}}
    (HERE/'fair_propagator_cost_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('GATES',json.dumps(out['gates'],indent=2)); print('STAKES',json.dumps(out['stakes'],indent=2))
if __name__=='__main__': main()
