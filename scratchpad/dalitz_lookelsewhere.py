import sys; sys.path.insert(0,'scratchpad')
import numpy as np, json, dalitz_share as ds
rng=np.random.default_rng(555111)
d=dict(np.load('scratchpad/dalitz/kkk.npz')); sig,_=ds.apply_windows(d,'KKK')
sl,sh,q=d['slow'][sig],d['shigh'][sig],d['q'][sig]
c=(q>0).astype(np.int64)
CFG=[(0.35,0.65),(0.425,0.575),(0.425,0.65),(0.5,0.5),(0.5,0.575),(0.575,0.425),(0.575,0.5),(0.65,0.35),(0.65,0.425)]
XY=[]
for Xq,Yq in CFG:
    XY.append(((sl>np.quantile(sl,Xq)).astype(np.int64),(sh>np.quantile(sh,Yq)).astype(np.int64)))
obs=[ds.share_2x2x2(ds.table(x,y,c)) for x,y in XY]
obsmax=max(obs)
print('occupancy-passing configs, observed shares:')
for (Xq,Yq),s in zip(CFG,obs): print('   %.3f %.3f  %.4e'%(Xq,Yq,s))
print('observed MAX over the 9 =', obsmax)
NR=3000; mx=np.empty(NR)
cp=c.copy()
for i in range(NR):
    rng.shuffle(cp)
    mx[i]=max(ds.share_2x2x2(ds.table(x,y,cp)) for x,y in XY)
gp=(np.sum(mx>=obsmax)+1)/(NR+1)
print('LOOK-ELSEWHERE global p (max over 9 occupancy-passing configs, %d replicas) = %.4f'%(NR,gp))
print('null max-share: median %.3e  p95 %.3e  p99 %.3e'%(np.median(mx),np.percentile(mx,95),np.percentile(mx,99)))
json.dump({'configs':CFG,'observed':obs,'obs_max':obsmax,'global_p':float(gp),'n_replicas':NR,
           'null_max_median':float(np.median(mx)),'null_max_p95':float(np.percentile(mx,95))},
          open('scratchpad/dalitz/lookelsewhere.json','w'),indent=1)
