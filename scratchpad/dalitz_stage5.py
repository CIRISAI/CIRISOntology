import sys; sys.path.insert(0,'scratchpad')
import numpy as np, json, dalitz_share as ds
rng=np.random.default_rng(8080)

# ---- (A) control on the control: does Dye B really inject a pair asymmetry, ----
# ---- and is the share flat over MANY draws (not one)? ----
d=dict(np.load('scratchpad/dalitz/kkk.npz')); sig,_=ds.apply_windows(d,'KKK')
sl,sh,q=d['slow'][sig],d['shigh'][sig],d['q'][sig]
x=(sl>np.median(sl)).astype(np.int64); y=(sh>np.median(sh)).astype(np.int64)
c0=(q>0).astype(np.int64)
res={}
for label,w,eps in (('none',(-1.0)**x,0.0),('DyeB_0.20',(-1.0)**x,0.20)):
    sh_,dl_=[],[]
    for b in range(200):
        cp=c0.copy(); rng.shuffle(cp)
        keep=np.ones(len(x),bool); plus=cp==1
        keep[plus]=rng.random(plus.sum())<(1.0+eps*w[plus])/(1.0+eps)
        T=ds.table(x[keep],y[keep],cp[keep])
        Np,Nm=T[:,:,1].sum(1),T[:,:,0].sum(1); a=(Np-Nm)/(Np+Nm)
        sh_.append(ds.share_2x2x2(T)); dl_.append(a[0]-a[1])
    sh_=np.array(sh_); dl_=np.array(dl_)
    res[label]={'injected_ACP_gap_mean':float(dl_.mean()),'injected_ACP_gap_sd':float(dl_.std()),
                'share_mean':float(sh_.mean()),'share_median':float(np.median(sh_)),
                'share_p95':float(np.percentile(sh_,95)),'share_p99':float(np.percentile(sh_,99))}
    print(label,json.dumps(res[label],indent=1))
print('\nchi2_1 shape check: p99/median for a chi2_1 is 6.63/0.455 = 14.6')
for k,v in res.items(): print('  %-10s p99/median = %.1f'%(k,v['share_p99']/v['share_median']))

# ---- (B) dye calibration + limit for the clean high-statistics secondary, pipipi ----
d2=ds.load('pipipi'); s2,_=ds.apply_windows(d2,'pipipi')
sl2,sh2,q2=d2['slow'][s2],d2['shigh'][s2],d2['q'][s2]
x2=(sl2>np.median(sl2)).astype(np.int64); y2=(sh2>np.median(sh2)).astype(np.int64)
c2=(q2>0).astype(np.int64); w2=(-1.0)**(x2+y2)
OBS2=ds.share_2x2x2(ds.table(x2,y2,c2))
floor2=ds.perm_null(x2,y2,c2.copy(),20000,rng)
f2m,f2s=float(np.median(floor2)),float(np.std(floor2))
print('\npipipi N=%d  observed share=%.4e  floor median=%.4e sd=%.4e  5sig bar=%.4e'%(len(x2),OBS2,f2m,f2s,f2m+5*f2s))
rows=[]
for eps in [0.0,0.005,0.01,0.015,0.02,0.025,0.03]:
    v=[]
    for b in range(200):
        cp=c2.copy(); rng.shuffle(cp)
        keep=np.ones(len(x2),bool); plus=cp==1
        keep[plus]=rng.random(plus.sum())<(1.0+eps*w2[plus])/(1.0+eps)
        v.append(ds.share_2x2x2(ds.table(x2[keep],y2[keep],cp[keep])))
    v=np.array(v)
    rows.append({'eps':eps,'mean':float(v.mean()),'z':float((v.mean()-f2m)/f2s),
                 'frac_at_or_below_observed':float(np.mean(v<=OBS2))})
    print('  eps=%-6g mean=%.4e  z=%7.2f  P(<=obs)=%.3f'%(eps,v.mean(),rows[-1]['z'],rows[-1]['frac_at_or_below_observed']))
five=next((r['eps'] for r in rows if r['z']>=5),None)
excl=next((r['eps'] for r in rows if r['frac_at_or_below_observed']<0.05),None)
print('  pipipi: 5-sigma sensitivity eps =',five,'   95%% exclusion eps >=',excl)
json.dump({'dyeB_control':res,'pipipi':{'N':int(len(x2)),'observed':OBS2,'floor_median':f2m,
           'floor_sd':f2s,'rows':rows,'five_sigma_eps':five,'excluded_eps':excl}},
          open('scratchpad/dalitz/stage5.json','w'),indent=1)
