import json, re, collections
raw=json.load(open('t5_raw.json'))
MODELS=["meta-llama/Llama-4-Scout-17B-16E-Instruct","openai/gpt-oss-120b","google/gemma-3-27b-it"]
VALID={"Priorities","Rules","Manner","Identity","Confidence","Facts","Circumstances","Process","Model","Structure","Premises","Record","NO FIT","NO-FIT"}
def parse(t):
    m=re.search(r'\{.*\}',t,re.S)
    if not m: return None
    try: d=json.loads(m.group(0))
    except Exception: return None
    k=str(d.get('kind','')).strip()
    if k=='NO-FIT': k='NO FIT'
    return {'kind':k if k in VALID else 'PARSE:'+k,'reason':str(d.get('reason',''))[:220],
            'so':str(d.get('survives_outside','')).lower().startswith('y')}
votes=collections.defaultdict(dict)
for kk,e in raw.items():
    tid,m=kk.rsplit('|',1)
    votes[tid][m]=parse(e['text'])
items=[json.loads(l) for l in open('t5_items.jsonl')]
tagnull=[json.loads(l) for l in open('t5_tagnull.jsonl')]
def unan(tid):
    v=votes.get(tid,{})
    ks=[v.get(m,{}).get('kind') if v.get(m) else None for m in MODELS]
    return ks[0] if len(set(ks))==1 and ks[0] else None, ks
# per-pair across conventions
pair={}
for it in items:
    uN,kN=unan(it['id']+'|GN'); uT,kT=unan(it['id']+'|GT')
    stable = uN is not None and uN==uT
    pair[it['id']]={'row':it['row'],'cat':it['category'],'lang':it['language'],
                    'value':it.get('value'),'uN':uN,'uT':uT,'det':uN if stable else None,
                    'kN':kN,'kT':kT}
# category-level
bycat=collections.defaultdict(list)
for p in pair.values(): bycat[(p['row'],p['cat'])].append(p)
catver={}
for (row,cat),ps in sorted(bycat.items()):
    if row==1: continue
    dets=[p['det'] for p in ps]
    c=collections.Counter(d for d in dets if d)
    top,n=c.most_common(1)[0] if c else (None,0)
    catver[(row,cat)]= (top if n>=2 else None, dets)
print("=== CATEGORY VERDICTS (non-row-1) ===")
for (row,cat),(v,dets) in sorted(catver.items()):
    print(f"row{row:>2} {cat:22} det={str(v):12} per-instance={dets}")
print("\n=== ROW 1 EVIDENTIALITY, PER VALUE ===")
for p in sorted((p for p in pair.values() if p['row']==1), key=lambda x:(x['lang'],x['value'])):
    print(f"{p['lang']:14} {p['value']:12} GN={str(p['uN']):11} GT={str(p['uT']):11} det={p['det']}")
# gloss instability at category level
insta=sum(1 for (row,cat),ps in bycat.items() for p in ps if p['uN'] and p['uT'] and p['uN']!=p['uT'])
tot_pairs_with_both=sum(1 for p in pair.values() if p['uN'] and p['uT'])
# kappa over all 80 units
units=[]
for it in items:
    for g in ('GN','GT'): units.append(it['id']+'|'+g)
for t in tagnull: units.append(t['id']+'|TN')
cats=set(); rows=[]
for u in units:
    v=votes.get(u,{})
    ks=[v.get(m,{}).get('kind','MISS') if v.get(m) else 'MISS' for m in MODELS]
    rows.append(ks); cats.update(ks)
cats=sorted(cats); N=len(rows); n=3
Pbar=0; pj=collections.Counter()
for ks in rows:
    c=collections.Counter(ks); Pbar+=(sum(x*x for x in c.values())-n)/(n*(n-1))
    for k,x in c.items(): pj[k]+=x
Pbar/=N; Pe=sum((pj[c]/(N*n))**2 for c in cats)
kappa=(Pbar-Pe)/(1-Pe)
print(f"\nkappa={kappa:.4f}  gloss-instability pairs={insta}/{tot_pairs_with_both}")
# tag-null
print("\n=== TAG-NULL ===")
for t in tagnull:
    u,ks=unan(t['id']+'|TN')
    print(f"{t['id']:22} type={t['pair_type']:5} unan={str(u):11} votes={ks}")
# NO-FIT / R and reasons
print("\n=== NO-FIT & non-Facts landscape ===")
allk=collections.Counter(p['det'] for p in pair.values() if p['det'])
print("determinate pair landings:", dict(allk))
json.dump({'pair':{k:{kk:vv for kk,vv in v.items() if kk not in('kN','kT')} for k,v in pair.items()},
           'kappa':round(kappa,4)}, open('t5_scored.json','w'), indent=1, default=str)
