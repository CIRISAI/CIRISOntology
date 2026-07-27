import sys; sys.path.insert(0,'scratchpad')
import numpy as np, json, dalitz_share as ds
rng=np.random.default_rng(24680)
d=dict(np.load('scratchpad/dalitz/kkk.npz')); sig,_=ds.apply_windows(d,'KKK')
sl,sh,q=d['slow'][sig],d['shigh'][sig],d['q'][sig]
x=(sl>np.median(sl)).astype(np.int64); y=(sh>np.median(sh)).astype(np.int64)
c0=(q>0).astype(np.int64); w=(-1.0)**(x+y)
OBS=9.188344356747535e-05
rows=[]
for eps in [0.0,0.01,0.02,0.03,0.04,0.05,0.06,0.07]:
    vals=[]
    for b in range(300):
        cp=c0.copy(); rng.shuffle(cp)
        keep=np.ones(len(x),bool); plus=cp==1
        keep[plus]=rng.random(plus.sum())<(1.0+eps*w[plus])/(1.0+eps)
        vals.append(ds.share_2x2x2(ds.table(x[keep],y[keep],cp[keep])))
    v=np.array(vals); frac=float(np.mean(v<=OBS))
    rows.append({'eps':eps,'mean_share':float(v.mean()),'median_share':float(np.median(v)),
                 'frac_at_or_below_observed':frac})
    print('eps=%-5g  mean=%.4e  median=%.4e   P(share <= observed)=%.3f'%(eps,v.mean(),np.median(v),frac))
excl=next((r['eps'] for r in rows if r['frac_at_or_below_observed']<0.05),None)
print('\n95%% EXCLUSION: whole-only checkerboard CP asymmetry eps >=',excl,'is excluded')
json.dump({'observed':OBS,'rows':rows,'excluded_eps':excl},open('scratchpad/dalitz/limit.json','w'),indent=1)
