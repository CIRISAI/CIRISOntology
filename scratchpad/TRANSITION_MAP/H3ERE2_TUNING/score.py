"""H3ERE2 scorer: curated accuracy, deep accuracy, wild Fleiss kappa, telemetry, confusion."""
import json, collections, math, sys, os
D='/home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/'
TMAP={'axiotic':'Priorities','deontic':'Rules','pragmatic':'Manner','ontological':'Identity',
 'epistemic':'Confidence','empirical':'Facts','contingent':'Circumstances','procedural':'Process',
 'nomological':'Model','structural':'Structure','axiomatic':'Premises','testimonial':'Record'}
SURFACE=["Facts","Rules","Manner","Identity"]
DEEP=["Priorities","Confidence","Circumstances","Process","Model","Structure","Premises"]
ALL12=SURFACE+DEEP+["Record"]
MODELS=["deepseek-ai/DeepSeek-V3.1","Qwen/Qwen3-235B-A22B-Instruct-2507","zai-org/GLM-4.5"]
SHORT={MODELS[0]:'DS',MODELS[1]:'QW',MODELS[2]:'GLM'}

def jl(p): return [json.loads(l) for l in open(D+p) if l.strip()]

def fleiss(units):
    """units: list of lists of category labels (one per rater). Unequal n handled by
    restricting to units with exactly n raters (the modal n)."""
    units=[u for u in units if u]
    n=collections.Counter(len(u) for u in units).most_common(1)[0][0]
    units=[u for u in units if len(u)==n]
    N=len(units)
    if N==0 or n<2: return float('nan'),0,0
    cats=sorted({c for u in units for c in u})
    P=[]
    pj=collections.Counter()
    for u in units:
        cnt=collections.Counter(u)
        for c,v in cnt.items(): pj[c]+=v
        P.append((sum(v*v for v in cnt.values())-n)/(n*(n-1)))
    Pbar=sum(P)/N
    Pe=sum((pj[c]/(N*n))**2 for c in cats)
    if abs(1-Pe)<1e-12: return float('nan'),N,n
    return (Pbar-Pe)/(1-Pe),N,n

def curated_baseline(ids):
    rows=[r for r in jl('panel2_validation.jsonl') if r['id'] in ids]
    gt={}
    for it in jl('h3ere2_curated.jsonl'): gt[it['id']]=TMAP[it['kind_target']]
    return rows,gt

def acc_report(pred, gt, label):
    """pred: dict (id,model)->kind (or None). returns dict of metrics"""
    out={}
    per={}
    for m in MODELS:
        hits=tot=cov=0
        for i,g in gt.items():
            k=pred.get((i,m),'__MISS__')
            if k=='__MISS__': continue
            tot+=1
            if k is not None: cov+=1
            if k==g: hits+=1
        per[SHORT[m]]={'n':tot,'acc':hits/tot if tot else 0,'cov':cov/tot if tot else 0}
    out['per_model']=per
    # pooled
    hits=tot=cov=0; dh=dt=0; sh=st=0
    conf=collections.Counter()
    for i,g in gt.items():
        for m in MODELS:
            k=pred.get((i,m),'__MISS__')
            if k=='__MISS__': continue
            tot+=1
            if k is not None: cov+=1
            ok = (k==g)
            hits+=ok
            if g in DEEP or g=='Record':
                dt+=1; dh+=ok
            else:
                st+=1; sh+=ok
            conf[(g,k if k else 'NONE')]+=1
    out['pooled']={'n':tot,'acc':hits/tot if tot else 0,'cov':cov/tot if tot else 0,
                   'deep_n':dt,'deep_acc':dh/dt if dt else 0,'surf_n':st,'surf_acc':sh/st if st else 0}
    out['confusion']=conf
    # per-target accuracy
    pt={}
    for i,g in gt.items():
        for m in MODELS:
            k=pred.get((i,m),'__MISS__')
            if k=='__MISS__': continue
            a=pt.setdefault(g,[0,0]); a[1]+=1; a[0]+= (k==g)
    out['per_target']={g:(v[0]/v[1],v[1]) for g,v in sorted(pt.items())}
    # cross-family kappa on curated
    units=[]
    for i in gt:
        u=[pred[(i,m)] for m in MODELS if pred.get((i,m)) is not None]
        units.append(u)
    out['kappa'],out['kappa_N'],out['kappa_n']=fleiss(units)
    return out

def load_traces(path):
    if not os.path.exists(D+path): return None
    rows=jl(path)
    pred={}; tel=collections.Counter(); s1conf={}
    for r in rows:
        f=r.get('final')
        pred[(r['id'],r['model'])]= f if f in ALL12 else None
        tel[r.get('route','?')]+=1
    return rows,pred,tel

def fmt(x,n=3):
    try: return f"{x:.{n}f}"
    except Exception: return str(x)
