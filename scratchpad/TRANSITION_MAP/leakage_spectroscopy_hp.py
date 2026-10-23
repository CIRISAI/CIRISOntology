"""80-digit conditioning audit for high-loss quasi-dark linewidths.

Frozen in LEAKAGE_SPECTROSCOPY_HP_PREREG.md before this implementation.
The original double-precision spectroscopy gate remains failed regardless of outcome.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import mpmath as mp
import dark_state_k23 as k23

HERE=Path(__file__).resolve().parent
KAPPAS=[100.0,316.22776601683796,1000.0,3162.2776601683795,10000.0]
SVALS=[1e-4,3e-4]
mp.mp.dps=80

def mp_matrix(A):
    return mp.matrix([[mp.mpc(float(np.real(x)),float(np.imag(x))) for x in row] for row in A])

def hp_gamma(H0,V,QB,Ed,s,kappa):
    A=H0+s*V-0.5j*kappa*QB
    vals=mp.eig(mp_matrix(A),left=False,right=False)
    # High-loss quasi-dark mode is uniquely the least-decaying eigenvalue.
    vals=list(vals); lam=max(vals,key=lambda z: mp.im(z))
    others=sorted(vals,key=lambda z: mp.im(z),reverse=True)[1:]
    sep=float(mp.im(lam)-mp.im(others[0])) if others else None
    return {'Gamma':float(-2*mp.im(lam)),'real_lambda':float(mp.re(lam)),'real_offset_from_Ed':float(mp.re(lam)-Ed),'imag_separation_to_next':sep}

def run_pair(H,a,b):
    d,H0,V,QB,Ed,Ew,bright,v=k23.prepared(H,a,b)
    g2=float(np.sum(np.abs(v)**2)); rows=[]; hp_errs=[]; dp_errs=[]; stable_diffs=[]
    for kap in KAPPAS:
        C=k23.coefficient(kap,Ed,Ew,v); analytic_tail=kap*C/(4*g2)
        for s in SVALS:
            hp=hp_gamma(H0,V,QB,Ed,s,kap); dp=k23.resonance(H0+s*V,d,QB,kap)
            pred=s*s*C
            hr=hp['Gamma']/pred if pred>0 else None; dr=dp['Gamma']/pred if pred>0 else None
            he=abs(hr-1); de=abs(dr-1); hp_errs.append(he); dp_errs.append(de)
            if de<.005: stable_diffs.append(abs(hp['Gamma']/dp['Gamma']-1) if dp['Gamma']>0 else 0)
            rows.append({'kappa':kap,'s':s,'C':C,'analytic_tail_ratio':analytic_tail,'high_precision':hp,'double_precision':{'Gamma':dp['Gamma'],'dark_overlap':dp['dark_overlap']},'hp_ratio_to_s2C':hr,'dp_ratio_to_s2C':dr,'hp_abs_frac_error':he,'dp_abs_frac_error':de})
    endpoint=next(r for r in rows if r['kappa']==10000.0 and r['s']==3e-4)
    return {'Ed':Ed,'gDB2':g2,'rows':rows,'endpoint_ratio':endpoint['hp_ratio_to_s2C'],'median_hp_error':float(np.median(hp_errs)),'median_dp_error':float(np.median(dp_errs)),'stable_cell_max_hp_vs_dp_frac_change':max(stable_diffs) if stable_diffs else None}

def main():
    arms={'CUR-P2':HERE/'panel2_validation.jsonl','CUR-SP':k23.ROOT/'scratchpad/plane_corpus/full_judgments.jsonl'}
    out={'prereg':'LEAKAGE_SPECTROSCOPY_HP_PREREG.md','arms':{},'stakes':{}}
    endpoint=[]; ratios=[]; stable=[]
    for arm,path in arms.items():
        H=k23.anchor_c(path); out['arms'][arm]={'pairs':{}}
        for lab,(a,b) in k23.TWINS.items():
            r=run_pair(H,a,b); out['arms'][arm]['pairs'][lab]=r
            endpoint.append(abs(r['endpoint_ratio']-1)); ratios.append(r['median_dp_error']/max(r['median_hp_error'],1e-300))
            if r['stable_cell_max_hp_vs_dp_frac_change'] is not None: stable.append(r['stable_cell_max_hp_vs_dp_frac_change'])
            print(arm,lab,'endpoint',r['endpoint_ratio'],'median hp/dp',r['median_hp_error'],r['median_dp_error'],'improvement',ratios[-1],flush=True)
    out['stakes']={'HP1_all_endpoint_within_1pct':bool(max(endpoint)<=.01),'HP2_median_error_improvement_ge10x':bool(np.median(ratios)>=10),'HP3_stable_cells_change_lt0p5pct':bool(not stable or max(stable)<.005),'HP2_pair_improvement_factors':ratios,'HP3_max_stable_change':max(stable) if stable else None}
    (HERE/'leakage_spectroscopy_hp_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('STAKES',json.dumps(out['stakes'],indent=2))
if __name__=='__main__': main()
