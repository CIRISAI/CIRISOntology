"""Observable-weighted commutator certificate for profile-class reduction.

Frozen in OBSERVABLE_COMMUTATOR_CERT_PREREG.md before this implementation.
Uses the exact midpoint piecewise-constant substrate from approx_bath_classes.py.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import expm_multiply

HERE=Path(__file__).resolve().parent
NS=[128,256,512,1024]; GS=[8,16,32,64,128]
T=20.0; NSTEPS=200; DT=T/NSTEPS

def xi(t):
    return np.array([0.5*math.cos(.7*t)+.2*math.cos(1.9*t),0.5*math.sin(.7*t)+.2*math.sin(1.3*t)])

def profiles(n,scrambled=False):
    th=2*math.pi*np.arange(n)/n; A=np.c_[np.cos(th),np.sin(th)]
    if scrambled: A=A[(37*np.arange(n)+11)%n]
    return A

def classes(A,G):
    ang=np.mod(np.arctan2(A[:,1],A[:,0]),2*math.pi)
    ids0=np.minimum(np.floor(G*ang/(2*math.pi)+1e-12).astype(int),G-1)
    means=[]; sizes=[]; rem=-np.ones(G,int)
    for k in range(G):
        m=ids0==k
        if m.any(): rem[k]=len(means); means.append(A[m].mean(0)); sizes.append(m.sum())
    return np.asarray(means),np.asarray(sizes),rem[ids0]

def red_H(means,sizes,n,t):
    en=means@xi(t); w=np.sqrt(sizes/n); m=len(means)
    H=np.zeros((m+1,m+1),complex); H[np.arange(1,m+1),np.arange(1,m+1)]=en
    H[0,1:]=w; H[1:,0]=w
    return H

def full_H(A,t):
    n=len(A); en=A@xi(t); g=1/math.sqrt(n)
    rows=list(range(1,n+1)); cols=rows.copy(); vals=list(en.astype(float))
    for j in range(1,n+1): rows.extend([0,j]); cols.extend([j,0]); vals.extend([g,g])
    return csr_matrix((vals,(rows,cols)),shape=(n+1,n+1),dtype=complex)

def propagate_full(A):
    q=np.zeros(len(A)+1,complex); q[0]=1; out=[1.0]
    for s in range(NSTEPS):
        H=full_H(A,(s+.5)*DT); q=expm_multiply((-1j*DT)*H,q,traceA=(-1j*DT)*H.diagonal().sum()); out.append(float(abs(q[0])**2))
    return np.asarray(out)

def propagate_red(means,sizes,n):
    q=np.zeros(len(means)+1,complex); q[0]=1; out=[1.0]
    for s in range(NSTEPS):
        H=red_H(means,sizes,n,(s+.5)*DT); q=expm((-1j*DT)*H)@q; out.append(float(abs(q[0])**2))
    return np.asarray(out)

def state_cert(A,means,ids):
    resid=float(np.max(np.linalg.norm(A-means[ids],axis=1)))
    integ=sum(DT*float(np.linalg.norm(xi((s+.5)*DT))) for s in range(NSTEPS))
    B=integ*resid
    return min(1.0,2*B+B*B)

def variance_formula(phi_full,E):
    p=np.abs(phi_full)**2
    mu=float(np.sum(p*E)); mu2=float(np.sum(p*E*E))
    return math.sqrt(max(0.0,mu2-mu*mu))

def cert(A,means,sizes,ids):
    n=len(A); m=len(means)
    # Backward boundary state phi(T)=|c>. phi(t)=Ubar(T,t)^dag |c>.
    phi_right=np.zeros(m+1,complex); phi_right[0]=1
    total=0.0; qerr=0.0
    for s in range(NSTEPS-1,-1,-1):
        tm=(s+.5)*DT; H=red_H(means,sizes,n,tm)
        Eemit=(A-means[ids])@xi(tm)
        def f(u):
            # u measured from left boundary; distance to right boundary is DT-u.
            ph=expm((1j*(DT-u))*H)@phi_right
            # Embed class-collective amplitudes in full emitter coordinates.
            full=np.empty(n+1,complex); full[0]=ph[0]
            full[1:]=ph[1:][ids]/np.sqrt(sizes[ids])
            E=np.r_[0.0,Eemit]
            return variance_formula(full,E)
        val,err=quad(f,0.0,DT,epsabs=1e-11,epsrel=1e-10,limit=30)
        total+=val+abs(err); qerr+=abs(err)
        phi_right=expm((1j*DT)*H)@phi_right
    return float(total),float(qerr)

def direct_commutator_gate(seed=20260822):
    rng=np.random.default_rng(seed); worst=0.0
    for n in [8,16,32]:
        for _ in range(20):
            z=rng.normal(size=n)+1j*rng.normal(size=n); z/=np.linalg.norm(z)
            E=rng.normal(size=n); P=np.outer(z,z.conj()); C=np.diag(E)@P-P@np.diag(E)
            op=float(np.linalg.svd(C,compute_uv=False)[0]); vf=variance_formula(z,E)
            worst=max(worst,abs(op-vf))
    return worst

def run_family(A):
    truth=propagate_full(A); out={}
    for G in GS:
        if G>len(A): continue
        means,sizes,ids=classes(A,G); pred=propagate_red(means,sizes,len(A)); obs=float(np.max(np.abs(pred-truth)))
        co,qe=cert(A,means,sizes,ids); cs=state_cert(A,means,ids)
        out[str(G)]={"observed_max_error":obs,"C_observable":co,"quadrature_error_added":qe,"C_state":cs,"classes":int(len(means))}
        print(' G',G,'obs',f'{obs:.3e}','Cobs',f'{co:.3e}','Cstate',f'{cs:.3e}',flush=True)
    return out

def main():
    cells={}; max_excess=-1e300; mismatch=0.0
    for n in NS:
        print('N',n,flush=True); sm=run_family(profiles(n,False)); sc=run_family(profiles(n,True)); cells[str(n)]={'SMOOTH':sm,'SCRAMBLED':sc}
        for G in GS:
            if G>n: continue
            max_excess=max(max_excess,sm[str(G)]['observed_max_error']-sm[str(G)]['C_observable'],sc[str(G)]['observed_max_error']-sc[str(G)]['C_observable'])
            mismatch=max(mismatch,abs(sm[str(G)]['C_observable']-sc[str(G)]['C_observable']))
    o1=direct_commutator_gate()
    row=cells['1024']['SMOOTH']['64']
    passing_obs=[G for G in GS if G<=1024 and cells['1024']['SMOOTH'][str(G)]['observed_max_error']<=1e-3]
    passing_cert=[G for G in GS if G<=1024 and cells['1024']['SMOOTH'][str(G)]['C_observable']<=1e-3]
    go=min(passing_obs) if passing_obs else None; gc=min(passing_cert) if passing_cert else None
    p2=bool(go is not None and gc is not None and gc<=2*go)
    vals256=cells['256']['SMOOTH']['64']['C_observable']; vals1024=cells['1024']['SMOOTH']['64']['C_observable']
    p3=bool(max(vals256,vals1024)<=2*max(min(vals256,vals1024),1e-300))
    out={'prereg':'OBSERVABLE_COMMUTATOR_CERT_PREREG.md','cells':cells,'gates':{'O1_commutator_variance_worst':o1,'O2_max_observed_minus_Cobs':max_excess,'O3_relabel_Cobs_mismatch':mismatch},'stakes':{'P1_G64_N1024_Cobs_le_0p05':row['C_observable']<=0.05,'P2_selector_within_2x':p2,'P3_Nstable_G64':p3,'observed_min_G':go,'certificate_min_G':gc}}
    (HERE/'observable_commutator_cert_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('GATES',json.dumps(out['gates'],indent=2)); print('STAKES',json.dumps(out['stakes'],indent=2))
if __name__=='__main__': main()
