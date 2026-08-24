"""Aggregate frozen SPATIOTEMPORAL_GRAY_BRIDGE_V2 matrix slices."""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np

NS=[32,64,128,256]; SIGMAS=[0.02,0.05,0.1]

def load(root):
    root=Path(root); slices={}
    for n in NS:
        for s in SIGMAS:
            name=f'spatiotemporal_gray_bridge_v2_N{n}_s{s:g}.json'
            hits=list(root.rglob(name))
            if len(hits)!=1: raise RuntimeError((name,hits))
            slices[f'N{n}_s{s:g}']=json.loads(hits[0].read_text())
    return slices

def fracerr(obs,pred): return abs(obs/pred-1) if pred!=0 else None

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--out',default='spatiotemporal_gray_bridge_v2_results.json'); args=ap.parse_args()
    sl=load(args.root)
    gates={'V1_common_dark_worst':max(v['gates']['V1_common_dark_worst'] for v in sl.values()),
           'V2_cov_rel_frob_worst':max(v['gates']['V2_cov_rel_frob_worst'] for v in sl.values()),
           'V3_integral_error':max(v['gates']['V3_integral_error'] for v in sl.values()),
           'V4_zero_noise_dark_worst':max(v['gates']['V4_zero_noise_dark_worst'] for v in sl.values())}
    # P1: every unordered arm pair at fixed N,sigma,tau, sorted by W. Statistical ties count as allowed.
    good=0; total=0; reversals=[]
    for key,v in sl.items():
        for tk,rows in v['cells'].items():
            names=list(rows)
            for i in range(len(names)):
                for j in range(i+1,len(names)):
                    a,b=rows[names[i]],rows[names[j]]
                    if abs(a['W']-b['W'])<1e-12: continue
                    lo,hi=(a,b) if a['W']<b['W'] else (b,a)
                    se=math.sqrt(lo['R_se']**2+hi['R_se']**2)
                    ok=hi['R_obs']>=lo['R_obs'] or abs(hi['R_obs']-lo['R_obs'])<=2*se
                    total+=1; good+=int(ok)
                    if not ok: reversals.append({'slice':key,'tau':tk,'W_lo':lo['W'],'W_hi':hi['W'],'R_lo':lo['R_obs'],'R_hi':hi['R_obs'],'combined_se':se})
    p1frac=good/max(total,1)
    # P2 weak noise.
    e2=[]; old2=[]; sq2=[]
    for n in NS:
        v=sl[f'N{n}_s0.02']
        for tk,rows in v['cells'].items():
            for name,r in rows.items():
                if r['W']<1e-12: continue
                e2.append(fracerr(r['R_obs'],r['R_P2']))
                old2.append((r['R_obs']-r['R_old2G'])**2); sq2.append((r['R_obs']-r['R_P2'])**2)
    med2=float(np.median(e2)); p902=float(np.quantile(e2,.9))
    # P3 sigma scaling .02 -> .05.
    sc=[]
    for n in NS:
        a=sl[f'N{n}_s0.02']; b=sl[f'N{n}_s0.05']
        for tk in a['cells']:
            for name in a['cells'][tk]:
                x=a['cells'][tk][name]; y=b['cells'][tk][name]
                if x['W']<1e-12 or x['R_obs']==0: continue
                sc.append(abs((y['R_obs']/0.05**2)/(x['R_obs']/0.02**2)-1))
    medsc=float(np.median(sc))
    # P4 finite-time memory on tau>=1 weak-noise.
    ef=[]; ei=[]
    for n in NS:
        v=sl[f'N{n}_s0.02']
        for tk,rows in v['cells'].items():
            tau=float(tk[3:])
            if tau<1: continue
            for r in rows.values():
                if r['W']<1e-12: continue
                ef.append(fracerr(r['R_obs'],r['R_P2'])); ei.append(fracerr(r['R_obs'],r['R_inf']))
    medf=float(np.median(ef)); medi=float(np.median(ei))
    # P6 N64 vs N256 ratio R/P2.
    fs=[]
    for s in SIGMAS[:2]:
        a=sl[f'N64_s{s:g}']; b=sl[f'N256_s{s:g}']
        for tk in a['cells']:
            for name in a['cells'][tk]:
                x=a['cells'][tk][name]; y=b['cells'][tk][name]
                if x['W']<1e-12 or x['R_P2']==0 or y['R_P2']==0: continue
                rx=x['R_obs']/x['R_P2']; ry=y['R_obs']/y['R_P2']; fs.append(abs(ry/rx-1))
    medfs=float(np.median(fs))
    # P7 sigma=.1 breakdown cells.
    breakdown=[]
    for n in NS:
        v=sl[f'N{n}_s0.1']
        for tk,rows in v['cells'].items():
            for name,r in rows.items():
                if r['W']<1e-12: continue
                e=fracerr(r['R_obs'],r['R_P2'])
                if e>0.25: breakdown.append({'N':n,'tau':float(tk[3:]),'arm':name,'W':r['W'],'error':e,'peak_dark':r['peak_dark'],'sigma_tau':0.1*float(tk[3:]),'G_tau':float(tk[3:])})
    stakes={'P1_spatial_order_fraction':p1frac,'P1_pass':p1frac>=.95,
            'P2_median_frac_error':med2,'P2_p90_frac_error':p902,'P2_pass':med2<=.10 and p902<=.25,
            'P3_median_sigma2_change':medsc,'P3_pass':medsc<=.15,
            'P4_median_finite_error':medf,'P4_median_asymptotic_error':medi,'P4_pass':medf<=0.5*medi,
            'P5_mse_G_kernel':float(np.mean(sq2)),'P5_mse_2G_kernel':float(np.mean(old2)),'P5_pass':float(np.mean(sq2))<=0.5*float(np.mean(old2)),
            'P6_median_N64_to_N256_ratio_change':medfs,'P6_pass':medfs<=.15,
            'P7_breakdown_count':len(breakdown),'P7_breakdown_cells':breakdown,
            'P1_reversals':reversals}
    out={'prereg':'SPATIOTEMPORAL_GRAY_BRIDGE_V2_PREREG.md','slices':sl,'gates':gates,'stakes':stakes}
    Path(args.out).write_text(json.dumps(out,indent=2)+'\n')
    print('GATES',json.dumps(gates,indent=2)); print('STAKES',json.dumps({k:v for k,v in stakes.items() if k not in ['P7_breakdown_cells','P1_reversals']},indent=2))
if __name__=='__main__': main()
