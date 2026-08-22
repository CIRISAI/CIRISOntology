"""ATLAS UNIV-1 runner. Frozen with ATLAS_UNIV1_PREREG.md before first execution.
Estimator definitions here ARE the prereg's definitions."""
import json, collections, itertools, math, sys
import numpy as np
rng=np.random.default_rng(20260822)
PLAIN={'axiotic':'Priorities','deontic':'Rules','pragmatic':'Manner','ontological':'Identity','epistemic':'Confidence','empirical':'Facts','contingent':'Circumstances','procedural':'Process','nomological':'Model','structural':'Structure','axiomatic':'Premises','testimonial':'Record'}
KINDS=['Priorities','Rules','Manner','Identity','Confidence','Facts','Circumstances','Process','Model','Structure','Premises']
KI={k:i for i,k in enumerate(KINDS)}
SURFACE=[KI[k] for k in ('Facts','Rules','Manner','Identity')]
TWINS=[('Priorities','Process'),('Structure','Circumstances')]
SP='/home/emoore/CIRISOntology/scratchpad'

def load(path):
    return [json.loads(l) for l in open(path)]

def norm_kind(k):
    if k in KI: return k
    return PLAIN.get(k) if PLAIN.get(k) in KI else None

def items_of(rows):
    by=collections.defaultdict(dict)
    for j in rows:
        k=norm_kind(j.get('kind'))
        if k: by[j['id'] if 'id' in j else j.get('item_id')][j['model']]=k
    return by

def matrix_T(rows, truth):
    by=items_of(rows); M=np.zeros((11,11)); n_items=0
    for i,votes in by.items():
        t=truth.get(i)
        if t not in KI: continue
        n_items+=1
        for v in votes.values(): M[KI[t],KI[v]]+=1
    counts=M.copy()
    M=M/np.maximum(M.sum(axis=1,keepdims=True),1e-12)
    return M, counts, n_items

def matrix_D(rows):
    by=items_of(rows); S=np.zeros((11,11)); n_items=0; ev=0
    for i,votes in by.items():
        vs=list(votes.values())
        if len(vs)>=2: n_items+=1
        for a,b in itertools.combinations(vs,2):
            if a!=b: S[KI[a],KI[b]]+=1; S[KI[b],KI[a]]+=1; ev+=1
    return S, ev, n_items

def channels(M, typ):
    off=M-np.diag(np.diag(M))
    if typ=='T':
        ch={(i,j):off[i,j] for i in range(11) for j in range(11) if i!=j}
    else:
        ch={(i,j):off[i,j] for i in range(11) for j in range(i+1,11)}
    return ch, off

def cascade(ch):
    v=np.sort(np.array(list(ch.values())))[::-1]
    tiers=[v[3*k:3*k+3].mean() for k in range(3)]
    if tiers[0]<=0 or tiers[1]<=0: return tiers,float('nan')
    r=math.sqrt((tiers[1]/tiers[0])*(tiers[2]/tiers[1]))
    return tiers,r

def swap_asym(M,a,b):
    P=np.eye(11); ia,ib=KI[a],KI[b]; P[[ia,ib]]=P[[ib,ia]]
    return np.abs(P@M@P-M).sum()/max(M.sum(),1e-12)

def s5_block(off, typ):
    if typ=='T': flat=off.flatten()
    else: flat=np.array([off[i,j] for i in range(11) for j in range(i+1,11)])
    v=np.sort(flat)[::-1]; om=v.sum()
    s5=v[:3].sum()/max(om,1e-12)
    def within(idx):
        idx=list(idx); rest=[i for i in range(11) if i not in idx]
        return (off[np.ix_(idx,idx)].sum()+off[np.ix_(rest,rest)].sum())/max(off.sum(),1e-12)
    ours=within(SURFACE)
    allv=[within(c) for c in itertools.combinations(range(11),4)]
    pct=100.0*sum(1 for x in allv if ours>=x)/len(allv)
    return s5, ours, pct

def top3_pairs(ch, typ):
    if typ=='T':
        agg=collections.defaultdict(float)
        for (i,j),v in ch.items(): agg[tuple(sorted((i,j)))]+=v
    else:
        agg={k:v for k,v in ch.items()}
    top=sorted(agg.items(), key=lambda kv:-kv[1])[:3]
    return [tuple(sorted((KINDS[i],KINDS[j]))) for (i,j),_ in top]

def stats_for(M, typ):
    ch,off=channels(M,typ)
    tiers,r=cascade(ch)
    sa={f"{a}/{b}":swap_asym(M,a,b) for a,b in TWINS}
    s5,ours,pct=s5_block(off,typ)
    return dict(tiers=[round(t,4) for t in tiers], r=round(r,4),
                swap={k:round(v,4) for k,v in sa.items()},
                s5=round(s5,4), block_pct=round(pct,1),
                top3=top3_pairs(ch,typ))

def perm_null(rows, typ, truth, n=200):
    """Permute each judge's kind labels across items independently."""
    base=[dict(j) for j in rows]
    bymodel=collections.defaultdict(list)
    for idx,j in enumerate(base): bymodel[j['model']].append(idx)
    out=[]
    for _ in range(n):
        rowsp=[dict(j) for j in base]
        for m,idxs in bymodel.items():
            ks=[rowsp[i].get('kind') for i in idxs]
            rng.shuffle(ks)
            for i,k in zip(idxs,ks): rowsp[i]['kind']=k
        if typ=='T': M,_,_=matrix_T(rowsp,truth)
        else: M,_,_=matrix_D(rowsp)
        ch,off=channels(M,typ)
        _,r=cascade(ch)
        if typ=='T': flat=off.flatten()
        else: flat=np.array([off[i,j] for i in range(11) for j in range(i+1,11)])
        v=np.sort(flat)[::-1]
        out.append((r, v[:3].sum()/max(v.sum(),1e-12)))
    rs=np.array([o[0] for o in out]); s5s=np.array([o[1] for o in out])
    return dict(r_p5=round(float(np.nanpercentile(rs,5)),4), r_p95=round(float(np.nanpercentile(rs,95)),4),
                r_med=round(float(np.nanmedian(rs)),4),
                s5_p95=round(float(np.nanpercentile(s5s,95)),4), s5_med=round(float(np.nanmedian(s5s)),4))

truth_cur={json.loads(l)['id']:PLAIN[json.loads(l)['kind_target']] for l in open(f'{SP}/plane_corpus/corpus_full.jsonl')}
truth_bab={}
for l in open(f'{SP}/plane_corpus/babel2_items.jsonl'):
    j=json.loads(l); kt=j.get('kind_target')
    if kt: truth_bab[j['id']]=PLAIN.get(kt,kt)

SUBS=[
 ('CUR-P2','T', f'{SP}/TRANSITION_MAP/panel2_validation.jsonl', truth_cur, 'S'),
 ('CUR-SP','T', f'{SP}/plane_corpus/full_judgments.jsonl', truth_cur, 'S'),
 ('BAB2','T', f'{SP}/plane_corpus/babel2_judgments.jsonl', truth_bab, 'S'),
 ('LEGC2','D', f'{SP}/TRANSITION_MAP/legc2_panel2_judgments.jsonl', None, 'S'),
 ('ECO','D', f'{SP}/plane_corpus/eco_judgments.jsonl', None, 'S'),
 ('STACKEX','D', f'{SP}/plane_corpus/stackex_judgments.jsonl', None, 'S'),
 ('ECO2','D', f'{SP}/plane_corpus/eco2_judgments.jsonl', None, 'S'),
 ('ECO2W','D', f'{SP}/plane_corpus/eco2_wiki_judgments.jsonl', None, 'S'),
]
results={}
pool_rows=[]
for name,typ,path,truth,axis in SUBS:
    rows=load(path)
    if typ=='T':
        M,counts,n_items=matrix_T(rows,truth)
        events=int((counts-np.diag(np.diag(counts))).sum())
    else:
        M,events,n_items=matrix_D(rows)
    marg=np.array([sum(1 for j in rows if norm_kind(j.get('kind'))==k) for k in KINDS],float)
    p=marg/max(marg.sum(),1); ent=float(-(p[p>0]*np.log(p[p>0])).sum())
    gates=dict(G1_events=events, G2_entropy=round(ent,3), G3_items=n_items,
               scoreable=bool(events>=80 and ent>=1.2 and n_items>=40))
    entry=dict(type=typ, gates=gates)
    if gates['scoreable']:
        entry['stats']=stats_for(M,typ)
        entry['null']=perm_null(rows,typ,truth)
    else:
        pool_rows += rows if name in ('ECO','STACKEX','ECO2','ECO2W') else []
    results[name]=entry
    print(name, json.dumps(entry), flush=True)
if pool_rows:
    M,events,n_items=matrix_D(pool_rows)
    marg=np.array([sum(1 for j in pool_rows if norm_kind(j.get('kind'))==k) for k in KINDS],float)
    p=marg/max(marg.sum(),1); ent=float(-(p[p>0]*np.log(p[p>0])).sum())
    gates=dict(G1_events=events,G2_entropy=round(ent,3),G3_items=n_items,
               scoreable=bool(events>=80 and ent>=1.2 and n_items>=40))
    entry=dict(type='D',gates=gates)
    if gates['scoreable']:
        entry['stats']=stats_for(M,'D'); entry['null']=perm_null(pool_rows,'D',None)
    results['ECO-POOL']=entry
    print('ECO-POOL', json.dumps(entry), flush=True)
# JACC null
def jacc(a,b):
    A,B=set(a),set(b); return len(A&B)/len(A|B)
draws=[]
allpairs=[(i,j) for i in range(11) for j in range(i+1,11)]
for _ in range(10000):
    a=rng.choice(55,3,replace=False); b=rng.choice(55,3,replace=False)
    draws.append(jacc([allpairs[i] for i in a],[allpairs[i] for i in b]))
print('JACC-NULL mean', round(float(np.mean(draws)),4))
json.dump(results, open('atlas_univ1_results.json','w'), indent=1)
