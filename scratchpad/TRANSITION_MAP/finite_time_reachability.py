"""Finite-time reachability baselines for the frozen smooth-profile model.

Preregistered in FINITE_TIME_REACHABILITY_PREREG.md before this file existed.
Compares the interpretable profile-class basis with an oracle POD diagnostic,
a restarted local Arnoldi/Krylov propagator, and an online residual-enriched
reachable basis that never uses future truth snapshots.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import expm_multiply

HERE=Path(__file__).resolve().parent
NS=[256,512,1024]
GS=[4,8,16,32,64,128]
POD_RANKS=[2,4,8,16,24,32,48,64,96,128]
KRYLOV_DIMS=[2,4,8,12,16,24,32]
ONLINE_THRESHOLDS=[1e-1,3e-2,1e-2,3e-3,1e-3,3e-4,1e-4]
ONLINE_CAP=128
T=20.0; NSTEPS=200; DT=T/NSTEPS
TOL=1e-3


def xi(t):
    return np.array([0.5*math.cos(.7*t)+.2*math.cos(1.9*t),
                     0.5*math.sin(.7*t)+.2*math.sin(1.3*t)])

def profiles(n,scrambled=False):
    th=2*math.pi*np.arange(n)/n
    A=np.c_[np.cos(th),np.sin(th)]
    if scrambled:
        idx=(37*np.arange(n)+11)%n
        A=A[idx]
    return A

def make_H(A,t):
    n=len(A); g=1/math.sqrt(n); en=A@xi(t)
    rows=list(range(1,n+1)); cols=list(range(1,n+1)); vals=list(en.astype(float))
    for j in range(1,n+1): rows.extend([0,j]); cols.extend([j,0]); vals.extend([g,g])
    return csr_matrix((vals,(rows,cols)),shape=(n+1,n+1),dtype=complex)

def full_traj(A):
    q=np.zeros(len(A)+1,complex); q[0]=1
    Q=[q.copy()]
    for s in range(NSTEPS):
        H=make_H(A,(s+.5)*DT)
        q=expm_multiply((-1j*DT)*H,q,traceA=(-1j*DT)*H.diagonal().sum())
        Q.append(q.copy())
    return np.column_stack(Q)

def pop(Q): return np.abs(Q[0])**2

def class_ids(A,G):
    ang=np.mod(np.arctan2(A[:,1],A[:,0]),2*math.pi)
    return np.minimum(np.floor(G*ang/(2*math.pi)+1e-12).astype(int),G-1)

def class_traj(A,G):
    ids=class_ids(A,G); means=[]; sizes=[]
    for k in range(G):
        m=ids==k
        if m.any(): means.append(A[m].mean(0)); sizes.append(m.sum())
    means=np.asarray(means); sizes=np.asarray(sizes)
    q=np.zeros(len(means)+1,complex); q[0]=1; out=[1.0]
    for s in range(NSTEPS):
        en=means@xi((s+.5)*DT); w=np.sqrt(sizes/len(A))
        rows=list(range(1,len(means)+1)); cols=rows.copy(); vals=list(en.astype(float))
        for j,g in enumerate(w,start=1): rows.extend([0,j]); cols.extend([j,0]); vals.extend([g,g])
        H=csr_matrix((vals,(rows,cols)),shape=(len(means)+1,)*2,dtype=complex)
        q=expm_multiply((-1j*DT)*H,q,traceA=(-1j*DT)*H.diagonal().sum())
        out.append(float(abs(q[0])**2))
    return np.asarray(out), int(len(means)), int(len(means)*NSTEPS)

def pod_errors(Q):
    U,s,_=np.linalg.svd(Q,full_matrices=False)
    truth=pop(Q); out={}
    for r in POD_RANKS:
        if r>U.shape[1]: continue
        Ur=U[:,:r]
        Qr=Ur@(Ur.conj().T@Q)
        pr=pop(Qr)
        out[str(r)]={"max_pop_error":float(np.max(np.abs(pr-truth))),"state_rel_frob":float(np.linalg.norm(Q-Qr)/np.linalg.norm(Q))}
    fullr=U.shape[1]
    Qfull=U@(U.conj().T@Q)
    fullerr=float(np.max(np.abs(pop(Qfull)-truth)))
    return out, s, fullr, fullerr

def arnoldi_step(H,q,m):
    beta=float(np.linalg.norm(q))
    if beta==0: return q.copy(),0
    n=len(q); V=np.zeros((n,m),complex); Hm=np.zeros((m,m),complex)
    V[:,0]=q/beta; k=m; matvecs=0
    for j in range(m):
        w=H@V[:,j]; matvecs+=1
        for i in range(j+1):
            hij=np.vdot(V[:,i],w); Hm[i,j]=hij; w-=hij*V[:,i]
        if j+1<m:
            hn=float(np.linalg.norm(w)); Hm[j+1,j]=hn
            if hn<1e-14:
                k=j+1; break
            V[:,j+1]=w/hn
    y=np.zeros(k,complex); y[0]=beta
    y=expm((-1j*DT)*Hm[:k,:k])@y
    return V[:,:k]@y,matvecs

def krylov_traj(A,m):
    q=np.zeros(len(A)+1,complex); q[0]=1; out=[1.0]; work=0
    for s in range(NSTEPS):
        H=make_H(A,(s+.5)*DT)
        q,mv=arnoldi_step(H,q,m); work+=mv
        out.append(float(abs(q[0])**2))
    return np.asarray(out),int(work)

def online_traj(A,threshold):
    n=len(A)+1
    V=np.zeros((n,1),complex); V[0,0]=1
    c=np.array([1+0j]); out=[1.0]; work=0; dims=[1]
    for s in range(NSTEPS):
        H=make_H(A,(s+.5)*DT)
        q=V@c
        hq=H@q; work+=1
        r=hq-V@(V.conj().T@hq)
        rn=float(np.linalg.norm(r))
        if rn>threshold and V.shape[1]<ONLINE_CAP:
            # Reorthogonalize the new direction before accepting it.
            v=r/rn
            v-=V@(V.conj().T@v)
            vn=float(np.linalg.norm(v))
            if vn>1e-12:
                V=np.column_stack([V,v/vn])
                c=np.r_[c,0j]
        HV=H@V; work+=V.shape[1]
        K=V.conj().T@HV
        c=expm((-1j*DT)*K)@c
        out.append(float(abs((V@c)[0])**2)); dims.append(V.shape[1])
    return np.asarray(out),{"final_dim":int(V.shape[1]),"max_dim":int(max(dims)),"mean_dim":float(np.mean(dims)),"matvec_equiv":int(work)}

def min_by_error(d,key='max_pop_error',tol=TOL):
    passing=[]
    for x,v in d.items():
        if v[key]<=tol: passing.append((float(x),v))
    return min(passing,key=lambda z:z[0])[0] if passing else None

def run(scrambled=False):
    res={}
    for n in NS:
        print('N',n,'scrambled',scrambled,flush=True)
        A=profiles(n,scrambled); Q=full_traj(A); truth=pop(Q)
        pod,s,pod_full_rank,pod_full_err=pod_errors(Q)
        cls={}
        for G in GS:
            p,dim,work=class_traj(A,G)
            cls[str(G)]={"max_pop_error":float(np.max(np.abs(p-truth))),"dimension":dim,"matvec_equiv":work}
        kry={}
        for m in KRYLOV_DIMS:
            p,work=krylov_traj(A,m)
            kry[str(m)]={"max_pop_error":float(np.max(np.abs(p-truth))),"local_dim":m,"matvec_equiv":work}
        online={}
        for th in ONLINE_THRESHOLDS:
            p,meta=online_traj(A,th)
            online[f'{th:.1e}']={"max_pop_error":float(np.max(np.abs(p-truth))),**meta}
        min_pod=min_by_error(pod)
        min_class=min([G for G in GS if cls[str(G)]['max_pop_error']<=TOL],default=None)
        min_kry=min([m for m in KRYLOV_DIMS if kry[str(m)]['max_pop_error']<=TOL],default=None)
        passing_online=[v for v in online.values() if v['max_pop_error']<=TOL]
        min_online=min((v['final_dim'] for v in passing_online),default=None)
        min_online_work=min((v['matvec_equiv'] for v in passing_online),default=None)
        res[str(n)]={"POD":pod,"classes":cls,"krylov":kry,"online":online,"singular_values":s[:128].tolist(),"pod_full_rank":pod_full_rank,"pod_full_error":pod_full_err,"min_pod_1e-3":None if min_pod is None else int(min_pod),"min_class_1e-3":min_class,"min_krylov_1e-3":min_kry,"min_online_dim_1e-3":min_online,"min_online_work_1e-3":min_online_work}
        print(' min POD',res[str(n)]['min_pod_1e-3'],'class',min_class,'krylov',min_kry,'online',min_online,flush=True)
    return res

def main():
    smooth=run(False); scrambled=run(True)
    mismatch=0.0
    for n in NS:
        for arm in ['classes','POD','krylov']:
            for k in smooth[str(n)][arm]:
                mismatch=max(mismatch,abs(smooth[str(n)][arm][k]['max_pop_error']-scrambled[str(n)][arm][k]['max_pop_error']))
        for k in smooth[str(n)]['online']:
            a=smooth[str(n)]['online'][k]; b=scrambled[str(n)]['online'][k]
            mismatch=max(mismatch,abs(a['max_pop_error']-b['max_pop_error']))
            mismatch=max(mismatch,abs(a['final_dim']-b['final_dim']))
    pod_monotone=all(all(list(v['POD'].values())[i]['max_pop_error']+1e-14>=list(v['POD'].values())[i+1]['max_pop_error'] for i in range(len(v['POD'])-1)) for v in smooth.values())
    pod_floor=max(v['pod_full_error'] for v in smooth.values())
    p2=bool(smooth['1024']['min_pod_1e-3'] is not None and smooth['1024']['min_pod_1e-3']<=16 and smooth['1024']['min_class_1e-3']==64)
    od=smooth['1024']['min_online_dim_1e-3']; cg=smooth['1024']['min_class_1e-3']
    p1_dim=bool(od is not None and cg is not None and cg<=2*od)
    def nstable(field):
        a=smooth['256'][field]; b=smooth['1024'][field]
        return bool(a is not None and b is not None and b<=2*a and a<=2*b)
    out={"prereg":"FINITE_TIME_REACHABILITY_PREREG.md","smooth":smooth,"scrambled":scrambled,
         "gates":{"F1_all_errors_against_same_truth":True,"F2_relabel_max_error_or_dim_mismatch":mismatch,"F3_pod_monotone":pod_monotone,"F3_pod_full_rank_max_error":pod_floor},
         "stakes":{"P1_profile_within_2x_online_dimension":p1_dim,"P2_hidden_low_rank_dynamics":p2,"P3_Nstable_classes":nstable('min_class_1e-3'),"P3_Nstable_krylov":nstable('min_krylov_1e-3'),"P3_Nstable_online":nstable('min_online_dim_1e-3'),"P4_krylov_dimension_N1024":smooth['1024']['min_krylov_1e-3']}}
    (HERE/'finite_time_reachability_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('GATES',json.dumps(out['gates'],indent=2)); print('STAKES',json.dumps(out['stakes'],indent=2))
if __name__=='__main__': main()
