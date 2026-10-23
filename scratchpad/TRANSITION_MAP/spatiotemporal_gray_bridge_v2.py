"""Corrected full-grid spatiotemporal gray-bridge confrontation.

Frozen in SPATIOTEMPORAL_GRAY_BRIDGE_V2_PREREG.md before this file existed.
The primary predictor is the finite-time second-order OU memory kernel at the
polariton->dark gap G, with no fitted coefficient.
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np
from scipy.integrate import quad

HERE=Path(__file__).resolve().parent
SEED=20260822
GCOUP=1.0
NS=[32,64,128,256]
SIGMAS=[0.02,0.05,0.1]
TAUS=[0.02,0.05,0.1,0.2,0.5,1.0,2.0,5.0]
NTRAJ=64
T=20.0; DT=0.01; NSTEPS=int(round(T/DT))
SLOPE_WINDOW=(1.0,4.0)


def arms(n):
    out=[]
    out.append(('COMMON',np.ones((n,n))))
    out.append(('BLOCK2',block_corr(n,2)))
    out.append(('BLOCK4',block_corr(n,4)))
    out.append(('BLOCK8',block_corr(n,8)))
    for ell in [0.3,1.0,3.0,10.0]: out.append((f'RING{ell:g}',ring_corr(n,ell)))
    out.append(('INDEPENDENT',np.eye(n)))
    return out

def block_corr(n,g):
    S=np.zeros((n,n)); groups=np.array_split(np.arange(n),g)
    for q in groups: S[np.ix_(q,q)]=1.0
    return S

def ring_corr(n,ell):
    i=np.arange(n); d=np.abs(i[:,None]-i[None,:]); d=np.minimum(d,n-d)
    return np.exp(-d/ell)

def sqrt_psd(S):
    w,V=np.linalg.eigh((S+S.T)/2); w=np.clip(w,0,None)
    return V@np.diag(np.sqrt(w))@V.T

def Wfactor(S):
    n=len(S); b=np.ones(n)/math.sqrt(n)
    return float((np.trace(S)-b@S@b)/n)

def finite_kernel(t,tau,omega):
    a=1/tau-1j*omega
    return float(np.real(t/a-(1-np.exp(-a*t))/(a*a)))

def predictor_slope(W,sigma,tau,omega=GCOUP):
    ts=np.linspace(0,T,NSTEPS+1)
    P=np.array([W*sigma*sigma*finite_kernel(float(t),tau,omega) for t in ts])
    m=(ts>=SLOPE_WINDOW[0])&(ts<=SLOPE_WINDOW[1])
    return float(np.polyfit(ts[m],P[m],1)[0])

def asymptotic_rate(W,sigma,tau):
    return W*sigma*sigma*tau/(1+(GCOUP*tau)**2)

def rhs(c,e,x):
    n=e.shape[1]; g=GCOUP/math.sqrt(n)
    return -1j*g*np.sum(e,axis=1), -1j*(g*c[:,None]+x*e)

def rk4(c,e,x):
    k1c,k1e=rhs(c,e,x)
    k2c,k2e=rhs(c+.5*DT*k1c,e+.5*DT*k1e,x)
    k3c,k3e=rhs(c+.5*DT*k2c,e+.5*DT*k2e,x)
    k4c,k4e=rhs(c+DT*k3c,e+DT*k3e,x)
    return c+DT*(k1c+2*k2c+2*k3c+k4c)/6, e+DT*(k1e+2*k2e+2*k3e+k4e)/6

def simulate(n,sigma,tau,S,seed):
    L=sqrt_psd(S); rng=np.random.default_rng(seed)
    rho=math.exp(-DT/tau); inn=sigma*math.sqrt(max(0.,1-rho*rho))
    x=sigma*(rng.normal(size=(NTRAJ,n))@L.T)
    c=np.full(NTRAJ,1/math.sqrt(2),complex)
    e=np.full((NTRAJ,n),1/math.sqrt(2*n),complex)
    ts=np.linspace(0,T,NSTEPS+1)
    dark=np.empty((NTRAJ,NSTEPS+1),float); cav=np.empty(NSTEPS+1,float)
    def measure(k):
        b=np.sum(e,axis=1)/math.sqrt(n)
        dark[:,k]=np.maximum(0.,np.sum(np.abs(e)**2,axis=1)-np.abs(b)**2)
        cav[k]=float(np.mean(np.abs(c)**2))
    measure(0)
    for s in range(NSTEPS):
        c,e=rk4(c,e,x)
        x=rho*x+inn*(rng.normal(size=(NTRAJ,n))@L.T)
        if (s+1)%100==0:
            norm=np.abs(c)**2+np.sum(np.abs(e)**2,axis=1)
            scale=np.sqrt(norm); c/=scale; e/=scale[:,None]
        measure(s+1)
    m=(ts>=SLOPE_WINDOW[0])&(ts<=SLOPE_WINDOW[1])
    slopes=np.array([np.polyfit(ts[m],row[m],1)[0] for row in dark])
    mean_slope=float(np.mean(slopes)); se=float(np.std(slopes,ddof=1)/math.sqrt(NTRAJ))
    md=np.mean(dark,axis=0)
    return {'R_obs':mean_slope,'R_se':se,'peak_dark':float(np.max(md)),'final_dark':float(md[-1]),'final_cavity':float(cav[-1])}

def covariance_gate(n,S,seed):
    rng=np.random.default_rng(seed); L=sqrt_psd(S)
    Z=rng.normal(size=(4096,n)); X=Z@L.T; C=X.T@X/len(X)
    return float(np.linalg.norm(C-S,'fro')/max(np.linalg.norm(S,'fro'),1e-15))

def common_gate(n,sigma,tau):
    rng=np.random.default_rng(SEED+991+n+int(1e4*sigma)+int(100*tau))
    rho=math.exp(-DT/tau); inn=sigma*math.sqrt(1-rho*rho)
    z=sigma*rng.normal(size=NTRAJ); c=np.full(NTRAJ,1/math.sqrt(2),complex); e=np.full((NTRAJ,n),1/math.sqrt(2*n),complex)
    worst=0.
    for _ in range(NSTEPS):
        x=np.repeat(z[:,None],n,axis=1); c,e=rk4(c,e,x); z=rho*z+inn*rng.normal(size=NTRAJ)
        b=np.sum(e,axis=1)/math.sqrt(n); d=np.sum(np.abs(e)**2,axis=1)-np.abs(b)**2; worst=max(worst,float(np.max(np.abs(d))))
    return worst

def zero_noise_gate(n):
    c=np.array([1/math.sqrt(2)],complex); e=np.full((1,n),1/math.sqrt(2*n),complex); x=np.zeros((1,n)); worst=0.
    for _ in range(NSTEPS):
        c,e=rk4(c,e,x); b=np.sum(e,axis=1)/math.sqrt(n); d=np.sum(np.abs(e)**2,axis=1)-np.abs(b)**2; worst=max(worst,float(np.max(np.abs(d))))
    return worst

def integral_gate():
    worst=0.
    for tau in [0.02,0.1,0.5,2.,5.]:
        for t in [0.2,1.,4.,10.]:
            q=quad(lambda u:(t-u)*math.exp(-u/tau)*math.cos(GCOUP*u),0,t,epsabs=1e-13,epsrel=1e-13)[0]
            worst=max(worst,abs(q-finite_kernel(t,tau,GCOUP)))
    return worst

def run_slice(n,sigma):
    armset=arms(n); cells={}; cov={}
    for name,S in armset: cov[name]=covariance_gate(n,S,SEED+77+n+hash(name)%10000)
    for tau in TAUS:
        key=f'tau{tau:g}'; cells[key]={}
        base_seed=SEED+100000*n+int(round(1e5*sigma))+int(round(100*tau))
        for name,S in armset:
            W=Wfactor(S)
            r=simulate(n,sigma,tau,S,base_seed)
            r.update({'W':W,'R_P2':predictor_slope(W,sigma,tau,GCOUP),'R_old2G':predictor_slope(W,sigma,tau,2*GCOUP),'R_inf':asymptotic_rate(W,sigma,tau)})
            cells[key][name]=r
            print('CELL',n,sigma,tau,name,'W',f'{W:.5f}','obs',f"{r['R_obs']:.6e}",'p2',f"{r['R_P2']:.6e}",'se',f"{r['R_se']:.2e}",flush=True)
    return {'N':n,'sigma':sigma,'settings':{'ntraj':NTRAJ,'dt':DT,'T':T,'slope_window':SLOPE_WINDOW},'cells':cells,'gates':{'V1_common_dark_worst':max(common_gate(n,sigma,t) for t in [0.1,0.5,2.]),'V2_cov_rel_frob_worst':max(cov.values()),'V3_integral_error':integral_gate(),'V4_zero_noise_dark_worst':zero_noise_gate(n)}}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--N',type=int); ap.add_argument('--sigma',type=float); args=ap.parse_args()
    if args.N is not None and args.sigma is not None:
        out=run_slice(args.N,args.sigma); fn=HERE/f'spatiotemporal_gray_bridge_v2_N{args.N}_s{args.sigma:g}.json'; fn.write_text(json.dumps(out,indent=2)+'\n'); print('GATES',json.dumps(out['gates'],indent=2)); return
    out={'prereg':'SPATIOTEMPORAL_GRAY_BRIDGE_V2_PREREG.md','slices':{}}
    for n in NS:
        for s in SIGMAS: out['slices'][f'N{n}_s{s:g}']=run_slice(n,s)
    (HERE/'spatiotemporal_gray_bridge_v2_results.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__': main()
