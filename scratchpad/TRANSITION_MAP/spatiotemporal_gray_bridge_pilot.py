"""Pilot execution for SPATIOTEMPORAL_GRAY_BRIDGE_PREREG.md.

This is a staged implementation/trend pilot only. It does NOT adjudicate the full
P1-P4 grid. It uses actual stochastic time-dependent single-excitation dynamics
under spatially correlated Ornstein-Uhlenbeck diagonal energy noise.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
SEED=20260822
NS=[32,64]
TAUS=[0.1,0.5,2.0]
SIGMA=0.05
NTRAJ=64
T=20.0
DT=0.01
NSTEPS=int(round(T/DT))
SLOPE_WINDOW=(1.0,4.0)
GCOUP=1.0


def corr_matrix(n,kind,param=None):
    if kind=='COMMON': return np.ones((n,n))
    if kind=='INDEPENDENT': return np.eye(n)
    if kind=='BLOCK4':
        S=np.zeros((n,n)); groups=np.array_split(np.arange(n),4)
        for g in groups: S[np.ix_(g,g)]=1.0
        return S
    if kind=='RING3':
        idx=np.arange(n); d=np.abs(idx[:,None]-idx[None,:]); d=np.minimum(d,n-d)
        return np.exp(-d/3.0)
    raise ValueError(kind)

def sqrt_psd(S):
    w,V=np.linalg.eigh((S+S.T)/2); w=np.clip(w,0,None)
    return V@np.diag(np.sqrt(w))@V.T

def Wfactor(S):
    n=len(S); one=np.ones(n)/math.sqrt(n); Q=np.eye(n)-np.outer(one,one)
    return float(np.trace(Q@S)/n)

def J_ou(tau,sigma=SIGMA,omega=2*GCOUP):
    return 2*sigma*sigma*tau/(1+(omega*tau)**2)

def rhs(c,e,x):
    # c shape (R,), e/x shape (R,N), rotating-frame TC with collective G=1.
    n=e.shape[1]; g=GCOUP/math.sqrt(n)
    dc=-1j*g*np.sum(e,axis=1)
    de=-1j*(g*c[:,None]+x*e)
    return dc,de

def rk4(c,e,x,dt):
    k1c,k1e=rhs(c,e,x)
    k2c,k2e=rhs(c+.5*dt*k1c,e+.5*dt*k1e,x)
    k3c,k3e=rhs(c+.5*dt*k2c,e+.5*dt*k2e,x)
    k4c,k4e=rhs(c+dt*k3c,e+dt*k3e,x)
    return c+dt*(k1c+2*k2c+2*k3c+k4c)/6, e+dt*(k1e+2*k2e+2*k3e+k4e)/6

def simulate(n,tau,kind):
    S=corr_matrix(n,kind); L=sqrt_psd(S); W=Wfactor(S)
    # Same seed per (n,tau), hence paired latent Gaussian stream across spatial arms.
    rng=np.random.default_rng(SEED + 1000*n + int(round(100*tau)))
    rho=math.exp(-DT/tau); innovation=SIGMA*math.sqrt(max(0.0,1-rho*rho))
    z=rng.normal(size=(NTRAJ,n)); x=SIGMA*(z@L.T)
    c=np.full(NTRAJ,1/math.sqrt(2),complex)
    e=np.full((NTRAJ,n),1/math.sqrt(2*n),complex)
    ts=np.linspace(0,T,NSTEPS+1); dark=np.empty(NSTEPS+1); cav=np.empty(NSTEPS+1)
    def measure(k):
        b=np.sum(e,axis=1)/math.sqrt(n)
        dark[k]=float(np.mean(np.sum(np.abs(e)**2,axis=1)-np.abs(b)**2))
        cav[k]=float(np.mean(np.abs(c)**2))
    measure(0)
    for s in range(NSTEPS):
        c,e=rk4(c,e,x,DT)
        z=rng.normal(size=(NTRAJ,n)); x=rho*x+innovation*(z@L.T)
        if (s+1)%100==0:
            norm=np.abs(c)**2+np.sum(np.abs(e)**2,axis=1)
            # Renormalize tiny RK drift trajectory-wise; record drift separately below.
            scale=np.sqrt(norm); c/=scale; e/=scale[:,None]
        measure(s+1)
    mask=(ts>=SLOPE_WINDOW[0])&(ts<=SLOPE_WINDOW[1])
    slope=float(np.polyfit(ts[mask],dark[mask],1)[0])
    return {'W':W,'R_pred':W*J_ou(tau),'R_obs':slope,'peak_dark':float(np.max(dark)),'final_dark':float(dark[-1]),'final_cavity':float(cav[-1])}

def covariance_gate(n,kind):
    S=corr_matrix(n,kind); L=sqrt_psd(S); rng=np.random.default_rng(SEED+777+n)
    Z=rng.normal(size=(4096,n)); X=Z@L.T; C=X.T@X/len(X)
    denom=max(float(np.linalg.norm(S,'fro')),1e-15)
    return float(np.linalg.norm(C-S,'fro')/denom)

def common_gate(n,tau):
    # Explicit scalar common OU: every emitter gets identical x(t). Dark population should stay zero.
    rng=np.random.default_rng(SEED+333+n+int(100*tau)); rho=math.exp(-DT/tau); inn=SIGMA*math.sqrt(1-rho*rho)
    xscalar=SIGMA*rng.normal(size=NTRAJ); c=np.full(NTRAJ,1/math.sqrt(2),complex); e=np.full((NTRAJ,n),1/math.sqrt(2*n),complex)
    worst=0.0
    for s in range(NSTEPS):
        x=np.repeat(xscalar[:,None],n,axis=1); c,e=rk4(c,e,x,DT); xscalar=rho*xscalar+inn*rng.normal(size=NTRAJ)
        b=np.sum(e,axis=1)/math.sqrt(n); dark=np.sum(np.abs(e)**2,axis=1)-np.abs(b)**2; worst=max(worst,float(np.max(np.abs(dark))))
    return worst

def main():
    kinds=['COMMON','BLOCK4','RING3','INDEPENDENT']; cells={}; cov={}; common={}
    for n in NS:
        cov[str(n)]={k:covariance_gate(n,k) for k in kinds}
        common[str(n)]={str(t):common_gate(n,t) for t in TAUS}
        for tau in TAUS:
            key=f'N{n}_tau{tau}'; cells[key]={}
            for k in kinds:
                r=simulate(n,tau,k); cells[key][k]=r
                print(key,k,'W',f"{r['W']:.3f}",'Rpred',f"{r['R_pred']:.3e}",'Robs',f"{r['R_obs']:.3e}",flush=True)
    # Pilot-only diagnostics: ordering and temporal-peak location.
    ordering={}; peaks={}
    for n in NS:
        for tau in TAUS:
            rows=cells[f'N{n}_tau{tau}']; order=sorted(kinds,key=lambda k:rows[k]['W']); vals=[rows[k]['R_obs'] for k in order]
            ordering[f'N{n}_tau{tau}']=bool(all(vals[i]<=vals[i+1]+5e-5 for i in range(len(vals)-1)))
        for k in kinds[1:]:
            vals=[cells[f'N{n}_tau{t}'][k]['R_obs'] for t in TAUS]; peaks[f'N{n}_{k}']=TAUS[int(np.argmax(vals))]
    out={'prereg':'SPATIOTEMPORAL_GRAY_BRIDGE_PREREG.md','scope':'pilot only; does not adjudicate full P1-P4','settings':{'N':NS,'taus':TAUS,'sigma':SIGMA,'ntraj':NTRAJ,'dt':DT,'slope_window':SLOPE_WINDOW},'cells':cells,'gates':{'B1_common_dark_worst':max(float(v) for d in common.values() for v in d.values()),'B3_cov_rel_frob_worst':max(float(v) for d in cov.values() for v in d.values())},'pilot':{'spatial_ordering':ordering,'temporal_peak_tau':peaks}}
    (HERE/'spatiotemporal_gray_bridge_pilot_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('GATES',json.dumps(out['gates'],indent=2)); print('PILOT',json.dumps(out['pilot'],indent=2))
if __name__=='__main__': main()
