import sys; sys.path.insert(0,'scratchpad')
import numpy as np, json, dalitz_share as ds
rng=np.random.default_rng(777333)
out={}
for mode in ('Kpipi','pipipi','piKK'):
    d=ds.load(mode)
    sig,side=ds.apply_windows(d,mode)
    sl,sh,q=d['slow'][sig],d['shigh'][sig],d['q'][sig]
    if len(sl)<100:
        out[mode]={'N':int(len(sl)),'status':'too few events'}; print(mode,out[mode]); continue
    x=(sl>np.median(sl)).astype(np.int64); y=(sh>np.median(sh)).astype(np.int64)
    c=(q>0).astype(np.int64)
    T=ds.table(x,y,c); o=ds.share_2x2x2(T)
    n=ds.perm_null(x,y,c.copy(),20000,rng)
    r=ds.significance(o,n)
    r['N']=int(T.sum()); r['min_cell']=int(T.min()); r['occupancy_pass']=bool(T.min()>=1000)
    lo,hi=ds.share_range_given_pairs(T)
    r['gate6a_max_reachable']=hi; r['gate6a_frac_used']=o/hi if hi>0 else None
    out[mode]=r
    print(mode, json.dumps({k:r[k] for k in ('N','min_cell','occupancy_pass','share','null_median','z','p','gate6a_frac_used')},indent=1))
json.dump(out,open('scratchpad/dalitz/secondaries.json','w'),indent=1)
