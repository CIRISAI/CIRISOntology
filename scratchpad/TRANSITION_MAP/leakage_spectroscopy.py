"""Dark-state leakage spectroscopy / sum-rule screen.

Preregistered in LEAKAGE_SPECTROSCOPY_PREREG.md before this file existed.
Reuses the exact K2.3 substrate/conventions without changing the measured matrices.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
import dark_state_k23 as k23

HERE=Path(__file__).resolve().parent
KAPPAS=10.0**np.arange(-4.0,4.0001,0.25)
SVALS=[1e-4,3e-4]

def closed_lspec(H0,V,d,s):
    w,U=eigh(H0+s*V)
    ov=np.abs(d@U)**2
    order=np.argsort(ov)[::-1]
    return 1-float(ov[order[0]]),float(ov[order[0]]),float(ov[order[1]])

def run_pair(H,a,b):
    d,H0,V,QB,Ed,Ew,bright,v=k23.prepared(H,a,b)
    mu=np.abs(v)**2; det=Ed-Ew; g2=float(mu.sum())
    nz=np.abs(det)>1e-12
    chi=float(np.sum(mu[nz]/(det[nz]**2)))
    sum_rule_err=abs(g2-float(np.linalg.norm(QB@V@d)**2))
    lspec_rows=[]
    for s in SVALS:
        L,o1,o2=closed_lspec(H0,V,d,s)
        lspec_rows.append({'s':s,'Lspec':L,'Lspec_over_s2':L/s**2,'dark_overlap':o1,'second_overlap':o2})
    rows=[]; max_coeff_err=0.0
    for kap in KAPPAS:
        C=k23.coefficient(float(kap),Ed,Ew,v)
        nr=[]
        for s in SVALS:
            rr=k23.resonance(H0+s*V,d,QB,float(kap))
            ratio=rr['Gamma']/(s*s*C) if C>0 else None
            rec={'s':s,**rr,'ratio_Gamma_s2C':ratio}
            nr.append(rec)
            if rr['dark_overlap']>=.99 and ratio is not None:
                max_coeff_err=max(max_coeff_err,abs(ratio-1))
        rows.append({'kappa':float(kap),'C':C,'numeric':nr})
    weighted=mu/(det**2+1e-300)
    dom=int(np.argmax(weighted)); domfrac=float(weighted[dom]/weighted.sum()) if weighted.sum()>0 else 0
    Cs=np.array([r['C'] for r in rows]); kp=float(rows[int(np.argmax(Cs))]['kappa'])
    high=rows[-1]; low=rows[0]
    # use larger weak s for numerical asymptotic stakes to reduce eig roundoff
    sh=SVALS[-1]
    high_num=next(x for x in high['numeric'] if x['s']==sh)
    low_num=next(x for x in low['numeric'] if x['s']==sh)
    high_ratio=(high['kappa']*high_num['Gamma']/sh**2)/(4*g2) if g2>0 else None
    low_ratio=(low_num['Gamma']/(sh**2*low['kappa']))/chi if chi>0 else None
    return {'Ed':Ed,'bright_eigenvalues':Ew.tolist(),'detunings':det.tolist(),'mu':mu.tolist(),'gDB2':g2,'chi2':chi,'L1_sum_rule_abs_error':sum_rule_err,'Lspec_rows':lspec_rows,'rows':rows,'max_L2_coeff_abs_frac_error_overlap_ge_0p99':max_coeff_err,'dominant_susceptibility_mode':{'index':dom,'fraction':domfrac,'abs_detuning':abs(float(det[dom]))},'kappa_peak_analytic':kp,'P1_high_numeric_ratio_to_4g2':high_ratio,'P2_low_numeric_ratio_to_chi2':low_ratio}

def main():
    arms={'CUR-P2':HERE/'panel2_validation.jsonl','CUR-SP':k23.ROOT/'scratchpad/plane_corpus/full_judgments.jsonl'}
    out={'prereg':'LEAKAGE_SPECTROSCOPY_PREREG.md','arms':{},'gates':{},'stakes':{}}
    l1=0.; l2=0.; l3=0.; p1=True;p2=True;p3=True
    diag={}
    for arm,path in arms.items():
        H=k23.anchor_c(path); out['arms'][arm]={'pairs':{}}
        diag[arm]={}
        for lab,(a,b) in k23.TWINS.items():
            r=run_pair(H,a,b); out['arms'][arm]['pairs'][lab]=r
            l1=max(l1,r['L1_sum_rule_abs_error']); l2=max(l2,r['max_L2_coeff_abs_frac_error_overlap_ge_0p99'])
            lr=r['Lspec_rows'][0]; l3=max(l3,abs(lr['Lspec_over_s2']/r['chi2']-1) if r['chi2']>0 else 0)
            p1 &= r['P1_high_numeric_ratio_to_4g2'] is not None and abs(r['P1_high_numeric_ratio_to_4g2']-1)<=.01
            p2 &= r['P2_low_numeric_ratio_to_chi2'] is not None and abs(r['P2_low_numeric_ratio_to_chi2']-1)<=.01
            dom=r['dominant_susceptibility_mode']
            if dom['fraction']>=.70:
                p3 &= abs(r['kappa_peak_analytic']/(2*dom['abs_detuning'])-1)<=.25
            diag[arm][lab]=r['chi2']/r['gDB2'] if r['gDB2']>0 else None
            print(arm,lab,'g2',r['gDB2'],'chi2',r['chi2'],'domfrac',dom['fraction'],'kpeak',r['kappa_peak_analytic'],'highrat',r['P1_high_numeric_ratio_to_4g2'],'lowrat',r['P2_low_numeric_ratio_to_chi2'],flush=True)
    # substrate diagnosis: primary shows stronger Str/Cir susceptibility per defect than Pri/Prc; replicate does not require same direction.
    p4=bool(diag['CUR-P2']['Str/Cir']>diag['CUR-P2']['Pri/Prc'] and (diag['CUR-P2']['Str/Cir']/diag['CUR-P2']['Pri/Prc'])>(diag['CUR-SP']['Str/Cir']/diag['CUR-SP']['Pri/Prc']))
    out['gates']={'L1_max_sum_rule_abs_error':l1,'L2_max_numeric_coeff_abs_frac_error':l2,'L3_max_Lspec_chi_abs_frac_error':l3}
    out['stakes']={'P1_high_loss_numeric_sum_rule':bool(p1),'P2_low_loss_numeric_sum_rule':bool(p2),'P3_turnover_localization_when_dominant':bool(p3),'P4_substrate_resonance_diagnosis':p4,'chi2_over_g2':diag}
    (HERE/'leakage_spectroscopy_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('GATES',json.dumps(out['gates'],indent=2)); print('STAKES',json.dumps(out['stakes'],indent=2))
if __name__=='__main__': main()
