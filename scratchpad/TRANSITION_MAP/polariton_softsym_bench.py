"""External-model soft-symmetry viability screen.

Preregistered in POLARITON_SOFTSYM_BENCH_PREREG.md before this file existed.
This is a disordered single-excitation Tavis-Cummings calibration, not MPS-HEOM.
"""
import json
import math
import time
from pathlib import Path

import numpy as np
from scipy.linalg import eigh
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import expm_multiply

HERE = Path(__file__).resolve().parent
SEED = 20260822
NS = [64, 128, 256, 512, 1024]
SIGMAS = [0.0, 0.1, 0.3, 1.0, 3.0]
TIMES = np.linspace(0.0, 20.0, 201)
TOL = 1e-4
MS = [2,4,6,8,12,16,24,32,48,64,96,128]
BS = [1,2,4,8,16,32,64,128]
TAUS = [0.0,0.001,0.003,0.01,0.03,0.1,0.3,1.0,3.0]


def arrowhead_sparse(w, g):
    n=len(w)
    rows=[]; cols=[]; vals=[]
    for i,wi in enumerate(w, start=1):
        rows.append(i); cols.append(i); vals.append(float(wi))
        rows.extend([0,i]); cols.extend([i,0]); vals.extend([float(g[i-1]),float(g[i-1])])
    return csr_matrix((vals,(rows,cols)), shape=(n+1,n+1), dtype=float)


def photon_population_sparse(H):
    q=np.zeros(H.shape[0],complex); q[0]=1
    A=(-1j)*H.astype(complex)
    tr=(-1j)*H.diagonal().sum()
    states=expm_multiply(A,q,start=float(TIMES[0]),stop=float(TIMES[-1]),num=len(TIMES),endpoint=True,traceA=tr)
    return np.abs(states[:,0])**2


def photon_population_dense(w,g):
    n=len(w)
    H=np.zeros((n+1,n+1),float)
    H[1:,1:]=np.diag(w)
    H[0,1:]=g; H[1:,0]=g
    ev,V=eigh(H)
    weights=np.abs(V[0,:])**2
    amp=np.exp(-1j*np.outer(TIMES,ev)) @ weights
    return np.abs(amp)**2


def rmse(x,y):
    return float(np.sqrt(np.mean((np.asarray(x)-np.asarray(y))**2)))


def lanczos_coeffs(H,max_m=128,tol=1e-14):
    n=H.shape[0]
    q_prev=np.zeros(n,float)
    q=np.zeros(n,float); q[0]=1.0
    al=[]; be=[]
    beta_prev=0.0
    for j in range(max_m):
        z=H@q
        if j>0:
            z=z-beta_prev*q_prev
        alpha=float(np.dot(q,z)); z=z-alpha*q
        # Full reorthogonalization is unnecessary for this small m/arrowhead screen;
        # the tridiagonal approximation is independently scored against truth.
        al.append(alpha)
        if j==max_m-1:
            break
        beta=float(np.linalg.norm(z))
        if beta<tol:
            break
        be.append(beta)
        q_prev,q=q,z/beta
        beta_prev=beta
    return np.array(al),np.array(be)


def krylov_population(al,be,m):
    m=min(m,len(al))
    T=np.diag(al[:m])
    if m>1:
        b=be[:m-1]
        T+=np.diag(b,1)+np.diag(b,-1)
    ev,V=eigh(T)
    weights=np.abs(V[0,:])**2
    amp=np.exp(-1j*np.outer(TIMES,ev))@weights
    return np.abs(amp)**2, m


def aggregate_groups(w,g,groups):
    wr=[]; gr=[]
    for ids in groups:
        ids=np.asarray(ids,dtype=int)
        g2=g[ids]**2
        s=float(g2.sum())
        if s<=0: continue
        wr.append(float(np.sum(g2*w[ids])/s))
        gr.append(math.sqrt(s))
    return np.array(wr),np.array(gr)


def equal_count_groups(w,B):
    order=np.argsort(w)
    return [x for x in np.array_split(order,min(B,len(w))) if len(x)]


def defect_groups(w,tau):
    order=np.argsort(w)
    if tau==0:
        # Exact near-twin criterion: only identical frequencies can share a cluster.
        groups=[]; cur=[int(order[0])]; lo=float(w[order[0]])
        for ix in order[1:]:
            ix=int(ix)
            if float(w[ix])-lo <= 0.0:
                cur.append(ix)
            else:
                groups.append(cur); cur=[ix]; lo=float(w[ix])
        groups.append(cur); return groups
    width=2.0*tau
    groups=[]; cur=[int(order[0])]; lo=float(w[order[0]])
    for ix in order[1:]:
        ix=int(ix)
        if float(w[ix])-lo <= width:
            cur.append(ix)
        else:
            groups.append(cur); cur=[ix]; lo=float(w[ix])
    groups.append(cur)
    return groups


def reduced_population(wr,gr,truth_if_identical=None):
    if truth_if_identical is not None and len(wr)+1==len(truth_if_identical):
        return None
    if len(wr)<=256:
        return photon_population_dense(wr,gr)
    return photon_population_sparse(arrowhead_sparse(wr,gr))


def one_cell(N,sigma,cell_seed):
    rng=np.random.default_rng(cell_seed)
    w=rng.normal(0.0,sigma,N) if sigma>0 else np.zeros(N)
    g=np.full(N,1/math.sqrt(N))
    H=arrowhead_sparse(w,g)

    t0=time.perf_counter(); truth=photon_population_sparse(H); truth_time=time.perf_counter()-t0

    dense_check=None
    if N==64:
        dense=photon_population_dense(w,g)
        dense_check=float(np.max(np.abs(dense-truth)))

    # Exact two-state bright reduction at sigma=0.
    exact2=photon_population_dense(np.array([0.0]),np.array([1.0]))
    exact2_rmse=rmse(exact2,truth) if sigma==0 else None

    # Baseline A: one Lanczos build, score frozen prefix dimensions.
    t0=time.perf_counter(); al,be=lanczos_coeffs(H,max(MS)); build_time=time.perf_counter()-t0
    kres=[]
    for m in MS:
        t1=time.perf_counter(); p,meff=krylov_population(al,be,m); pt=time.perf_counter()-t1
        kres.append({'m_requested':m,'m_effective':meff,'rmse':rmse(p,truth),'prop_time_s':pt})
    kpass=[x for x in kres if x['rmse']<=TOL]
    kmin=min(kpass,key=lambda x:x['m_effective']) if kpass else None

    # Baseline B: equal-count disorder bins.
    bres=[]
    for B in BS:
        if B>N: continue
        groups=equal_count_groups(w,B)
        wr,gr=aggregate_groups(w,g,groups)
        t1=time.perf_counter(); p=photon_population_dense(wr,gr); pt=time.perf_counter()-t1
        bres.append({'B':len(groups),'rmse':rmse(p,truth),'prop_time_s':pt})
    bpass=[x for x in bres if x['rmse']<=TOL]
    bmin=min(bpass,key=lambda x:x['B']) if bpass else None

    # Candidate C: defect-certified near-twin clusters.
    cres=[]
    for tau in TAUS:
        groups=defect_groups(w,tau)
        wr,gr=aggregate_groups(w,g,groups)
        if len(groups)==N:
            p=truth; pt=0.0
        else:
            t1=time.perf_counter()
            p=photon_population_dense(wr,gr) if len(wr)<=256 else photon_population_sparse(arrowhead_sparse(wr,gr))
            pt=time.perf_counter()-t1
        max_gdb=0.0
        for ids in groups:
            if len(ids)>1:
                vals=w[np.asarray(ids,dtype=int)]
                max_gdb=max(max_gdb,float((vals.max()-vals.min())/2.0))
        cres.append({'tau':tau,'clusters':len(groups),'certified_max_gDB':max_gdb,'rmse':rmse(p,truth),'prop_time_s':pt})
    cpass=[x for x in cres if x['rmse']<=TOL]
    cmin=min(cpass,key=lambda x:x['clusters']) if cpass else None

    p3=False
    if bmin and cmin and cmin['clusters']*2 <= bmin['B']:
        p3=True
    # Wall-time arm only counts reduced propagation, intentionally conservative about setup.
    if bmin and cmin and cmin['prop_time_s']>0 and bmin['prop_time_s'] >= 2*cmin['prop_time_s']:
        p3=True

    p4=None
    if kmin and cmin:
        p4=bool(kmin['m_effective'] <= cmin['clusters'])

    return {
        'N':N,'sigma':sigma,'seed':cell_seed,'truth_time_s':truth_time,
        'dense_max_abs_check':dense_check,'exact2_rmse':exact2_rmse,
        'krylov':{'build_time_s':build_time,'rows':kres,'min_pass':kmin},
        'binning':{'rows':bres,'min_pass':bmin},
        'defect_clusters':{'rows':cres,'min_pass':cmin},
        'P3_candidate_continuation':p3,
        'P4_krylov_already_captures':p4,
    }


def main():
    out={'prereg':'POLARITON_SOFTSYM_BENCH_PREREG.md','tolerance':TOL,'cells':[]}
    idx=0
    for N in NS:
        for sigma in SIGMAS:
            seed=SEED+1000*N+idx
            print('RUN',N,sigma,flush=True)
            cell=one_cell(N,sigma,seed)
            out['cells'].append(cell)
            k=cell['krylov']['min_pass']; b=cell['binning']['min_pass']; c=cell['defect_clusters']['min_pass']
            print(' ', 'K=',None if not k else k['m_effective'],
                  'B=',None if not b else b['B'],
                  'C=',None if not c else c['clusters'],
                  'P3=',cell['P3_candidate_continuation'],'P4=',cell['P4_krylov_already_captures'],flush=True)
            idx+=1

    # Aggregate gates.
    dense=[x['dense_max_abs_check'] for x in out['cells'] if x['dense_max_abs_check'] is not None]
    exact=[x['exact2_rmse'] for x in out['cells'] if x['exact2_rmse'] is not None]
    qualifying=[x for x in out['cells'] if x['N']>=256 and x['sigma']>0]
    out['gates']={
        'T1_dense_worst':float(max(dense)),
        'T2_exact2_worst_rmse':float(max(exact)),
        'P3_any_qualifying_continuation':bool(any(x['P3_candidate_continuation'] for x in qualifying)),
        'P4_fraction_krylov_already_captures':float(np.mean([x['P4_krylov_already_captures'] for x in qualifying if x['P4_krylov_already_captures'] is not None])),
    }

    # P5 N-independence by method/sigma for N>=256; use min dimensions where all exist.
    p5={}
    for sigma in SIGMAS[1:]:
        xs=[x for x in out['cells'] if x['sigma']==sigma and x['N']>=256]
        for method,key in [('krylov','m_effective'),('binning','B'),('defect_clusters','clusters')]:
            vals=[]
            for x in xs:
                z=x[method]['min_pass']
                if z is not None: vals.append(float(z[key]))
            stable=False
            if len(vals)==3:
                mean=float(np.mean(vals)); stable=bool(max(abs(v-mean) for v in vals) <= 0.2*mean)
            p5[f'{sigma}:{method}']={'values':vals,'within_20pct':stable}
    out['P5_scaling']=p5

    with open(HERE/'polariton_softsym_bench_results.json','w') as f: json.dump(out,f,indent=2)
    print('\nGATES',json.dumps(out['gates'],indent=2))
    for k,v in p5.items(): print('P5',k,v)


if __name__=='__main__':
    main()
