import json, collections, random, itertools
random.seed(20260821)
J=[json.loads(l) for l in open('legc_judgments.jsonl')]
items={json.loads(l)['id']:json.loads(l) for l in open('legc_items.jsonl')}
by=collections.defaultdict(dict)
for j in J: by[j['id']][j['model']]=j['kind']
def modal(iid):
    c=collections.Counter(by.get(iid,{}).values()); 
    if not c: return None
    t,n=c.most_common(1)[0]
    return t if n>=2 else None
labels={iid:modal(iid) for iid in items}
cov=sum(1 for v in labels.values() if v)/len(labels)
MODELS=sorted({j['model'] for j in J})
rows=[[str(by[i].get(m,'MISS')) for m in MODELS] for i in items]
cats=sorted({k for r in rows for k in r}); N=len(rows); n=3
Pbar=0; pj=collections.Counter()
for r in rows:
    c=collections.Counter(r); Pbar+=(sum(x*x for x in c.values())-n)/(n*(n-1))
    for k,x in c.items(): pj[k]+=x
Pbar/=N; Pe=sum((pj[c]/(N*n))**2 for c in cats)
kappa=(Pbar-Pe)/(1-Pe)
print(f"coverage={cov:.3f} kappa={kappa:.4f}  (VOID floors: cov 0.70, kappa 0.40)")
# chains -> transitions
chains=collections.defaultdict(list)
for iid,it in items.items(): chains[it['chain']].append((it['link_ix'],iid))
T=collections.Counter(); trans=[]
for ch,ls in chains.items():
    ls.sort()
    labs=[labels[i] for _,i in ls]
    for a,b in zip(labs,labs[1:]):
        if a and b: T[(a,b)]+=1; trans.append((ch,a,b))
ntrans=len(trans); nchains=len({c for c,_,_ in trans})
print(f"transitions={ntrans} over chains={nchains} (effective N = chains)")
kinds=sorted({k for ab in T for k in ab})
print("\nT[i][j] (rows=from):")
print(f"{'':14}"+"".join(f"{k[:6]:>7}" for k in kinds))
for i in kinds:
    print(f"{i:14}"+"".join(f"{T.get((i,j),0):7d}" for j in kinds))
diag=sum(T[(k,k)] for k in kinds); off=ntrans-diag
print(f"\ndiagonal={diag} off={off} diag share={diag/max(1,ntrans):.3f}")
# permutation null for diagonal share (shuffle labels within chain)
B=10000; cnt=0
seqs=[[labels[i] for _,i in sorted(ls)] for ls in chains.values()]
seqs=[[x for x in s if x] for s in seqs]; seqs=[s for s in seqs if len(s)>=2]
obs=diag/max(1,ntrans)
for _ in range(B):
    d=t=0
    for s in seqs:
        s2=s[:]; random.shuffle(s2)
        for a,b in zip(s2,s2[1:]):
            t+=1; d+= (a==b)
    if d/max(1,t)>=obs: cnt+=1
print(f"TM3 diagonal dominance: share={obs:.3f} perm-p={cnt/B:.4f} (staked: exceeds null)")
# TM4: off-diagonal concentration in boundary channels + deep->surface
SURFACE={'Facts','Rules','Manner','Identity'}
BOUND={('Premises','Facts'),('Facts','Premises'),('Model','Facts'),('Facts','Model'),
       ('Structure','Manner'),('Manner','Structure')}
offpairs=[(a,b) for (a,b),c in T.items() if a!=b for _ in range(c)]
inb=sum(1 for a,b in offpairs if (a,b) in BOUND)
dsurf=sum(1 for a,b in offpairs if a not in SURFACE and b in SURFACE)
print(f"TM4: off-diag total={len(offpairs)}, boundary-channel={inb} ({inb/max(1,len(offpairs)):.3f}), deep->surface={dsurf} ({dsurf/max(1,len(offpairs)):.3f})")
# TM5 valence: mechanical revert/extend/independent
def span(a,b):
    n=min(len(a),len(b)); p=0
    while p<n and a[p]==b[p]: p+=1
    s=0
    while s<n-p and a[len(a)-1-s]==b[len(b)-1-s]: s+=1
    return a[p:len(a)-s], b[p:len(b)-s]
val=collections.Counter(); val_to_surface=collections.Counter(); val_to_deep=collections.Counter()
for ch,ls in chains.items():
    ls.sort()
    for (ix1,i1),(ix2,i2) in zip(ls,ls[1:]):
        it1,it2=items[i1],items[i2]
        rem1,add1=span(it1['before'],it1['after'])
        rem2,add2=span(it2['before'],it2['after'])
        lab=labels[i2]
        if rem1 and (rem1 in it2['after']) and add1 and (add1 not in it2['after']):
            v='revert'
        elif add1 and (add1 in it2['before'] or add1 in it2['after']) and (add2 and add1 in it2['after']):
            v='extend'
        else:
            v='independent'
        val[v]+=1
        if lab in SURFACE: val_to_surface[v]+=1
        elif lab: val_to_deep[v]+=1
print(f"TM5 valence: {dict(val)}")
print(f"  toward surface labels: {dict(val_to_surface)}  toward deep: {dict(val_to_deep)}")
# FD stakes
print("\nFD1 row normalization: row sums (transition counts per source kind):")
for i in kinds:
    print(f"  {i:14} out={sum(T.get((i,j),0) for j in kinds)}")
json.dump({"kappa":round(kappa,4),"coverage":round(cov,4),"ntrans":ntrans,"nchains":nchains,
           "T":{f"{a}|{b}":c for (a,b),c in T.items()},"diag_share":round(obs,4)},
          open('legc_scored.json','w'),indent=1)
