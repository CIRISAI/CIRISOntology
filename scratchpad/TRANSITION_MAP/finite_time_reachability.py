"""Finite-time reachability baselines for the frozen smooth-profile model.

Preregistered in FINITE_TIME_REACHABILITY_PREREG.md before this file existed.
Primary purpose: determine whether the G=64 profile-class reduction is actually
competitive with generic finite-time trajectory/reachable subspaces.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import expm_multiply

HERE=Path(__file__).resolve().parent
NS=[256,512,1024]
GS=[4,8,16,32,64,128]
POD_RANKS=[2,4,8,16,24,32,48,64,96,128]
T=20.0; NSTEPS=200; DT=T/NSTEPS


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

def H_sparse(A):
    n=len(A); g=1/math.sqrt(n)
    rows=[]; cols=[]; vals=[]
    for j,e in enumerate(A,start=1):
        en=float(e@xi(0.0))
        rows += [j,0,j]; cols += [j,j,0]; vals += [en,g,g]
    return rows,cols,vals

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
    return np.asarray(out)

def pod_errors(Q):
    U,s,_=np.linalg.svd(Q,full_matrices=False)
    truth=pop(Q); out={}
    for r in POD_RANKS:
        if r>U.shape[1]: continue
        P=U[:,:r]@U[:,:r].conj().T
        Qr=P@Q
        pr=pop(Qr)
        out[str(r)]={"max_pop_error":float(np.max(np.abs(pr-truth))),"state_rel_frob":float(np.linalg.norm(Q-Qr)/np.linalg.norm(Q))}
    return out, s

def min_rank(d,tol=1e-3):
    x=[int(r) for r,v in d.items() if v['max_pop_error']<=tol]
    return min(x) if x else None

def run(scrambled=False):
    res={}
    for n in NS:
        print('N',n,'scrambled',scrambled,flush=True)
        A=profiles(n,scrambled); Q=full_traj(A); truth=pop(Q)
        pod,s=pod_errors(Q)
        cls={}
        for G in GS:
            p=class_traj(A,G)
            cls[str(G)]={"max_pop_error":float(np.max(np.abs(p-truth)))}
        res[str(n)]={"POD":pod,"classes":cls,"singular_values":s[:128].tolist(),"min_pod_1e-3":min_rank(pod),"min_class_1e-3":min([G for G in GS if cls[str(G)]['max_pop_error']<=1e-3],default=None)}
        print(' min POD',res[str(n)]['min_pod_1e-3'],'min class',res[str(n)]['min_class_1e-3'],flush=True)
    return res

def main():
    smooth=run(False); scrambled=run(True)
    mismatch=0.0
    for n in NS:
        for G in GS: mismatch=max(mismatch,abs(smooth[str(n)]['classes'][str(G)]['max_pop_error']-scrambled[str(n)]['classes'][str(G)]['max_pop_error']))
        for r in smooth[str(n)]['POD']:
            mismatch=max(mismatch,abs(smooth[str(n)]['POD'][r]['max_pop_error']-scrambled[str(n)]['POD'][r]['max_pop_error']))
    p2=bool(smooth['1024']['min_pod_1e-3'] is not None and smooth['1024']['min_pod_1e-3']<=16 and smooth['1024']['min_class_1e-3']==64)
    out={"prereg":"FINITE_TIME_REACHABILITY_PREREG.md","smooth":smooth,"scrambled":scrambled,"gates":{"F2_relabel_max_mismatch":mismatch,"F3_pod_monotone":all(all(list(v['POD'].values())[i]['max_pop_error']+1e-14>=list(v['POD'].values())[i+1]['max_pop_error'] for i in range(len(v['POD'])-1)) for v in smooth.values())},"stakes":{"P2_hidden_low_rank_dynamics":p2}}
    (HERE/'finite_time_reachability_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('GATES',json.dumps(out['gates'],indent=2)); print('STAKES',json.dumps(out['stakes'],indent=2))
if __name__=='__main__': main()
