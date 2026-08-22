"""LEG A — the coincidence index. Operationalizations committed pre-run.
Reference object matrix: the PANEL-2 curated confusion matrix (target-kind x modal-kind,
248 items, licensed instrument). Each signature statistic is computed identically on the
object and on null draws; a null SHOWS a signature iff its statistic is at least as
extreme as the object's, in the object's direction. Seeds 20260823."""
import json, itertools, collections
import numpy as np
rng = np.random.default_rng(20260823)
PLAIN={'axiotic':'Priorities','deontic':'Rules','pragmatic':'Manner','ontological':'Identity','epistemic':'Confidence','empirical':'Facts','contingent':'Circumstances','procedural':'Process','nomological':'Model','structural':'Structure','axiomatic':'Premises','testimonial':'Record'}
KINDS=['Priorities','Rules','Manner','Identity','Confidence','Facts','Circumstances','Process','Model','Structure','Premises']  # 11 artifact-local
SURFACE_IDX=[KINDS.index(k) for k in ('Facts','Rules','Manner','Identity')]
TWINS=[(KINDS.index('Priorities'),KINDS.index('Process')),(KINDS.index('Structure'),KINDS.index('Circumstances'))]
# --- object matrix from sealed PANEL-2 curated judgments ---
J=[json.loads(l) for l in open('panel2_validation.jsonl')]
tgt={json.loads(l)['id']:PLAIN[json.loads(l)['kind_target']] for l in open('/home/emoore/CIRISOntology/scratchpad/plane_corpus/corpus_full.jsonl')}
by=collections.defaultdict(dict)
for j in J: by[j['id']][j['model']]=j['kind']
M=np.zeros((11,11))
for i,t in tgt.items():
    if t not in KINDS: continue
    votes=[v for v in by.get(i,{}).values() if v in KINDS]
    for v in votes: M[KINDS.index(t),KINDS.index(v)]+=1
M=M/np.maximum(M.sum(axis=1,keepdims=True),1e-12)  # row-stochastic on the 11
def stats(T):
    off=T-np.diag(np.diag(T))
    om=off.sum()
    s5 = np.sort(off.flatten())[::-1][:3].sum()/max(om,1e-12)          # top-3 off-diag share (higher=more localized)
    # S3 twins: for the two named transpositions on the OBJECT; for nulls, best two disjoint transpositions
    def swap_asym(T,a,b):
        P=np.eye(11); P[[a,b]]=P[[b,a]]
        return np.abs(P@T@P-T).sum()/max(T.sum(),1e-12)
    return s5, swap_asym
def best_two_disjoint_swaps(T):
    _,sa=stats(T)
    vals=sorted(((sa(T,a,b),(a,b)) for a,b in itertools.combinations(range(11),2)))
    best=[]; used=set()
    for v,(a,b) in vals:
        if a in used or b in used: continue
        best.append(v); used|={a,b}
        if len(best)==2: return max(best)
    return max(best)
def s4_oneway(T):
    off=T-np.diag(np.diag(T))
    r=[]
    for i in range(11):
        inn=off[:,i].sum(); out=off[i,:].sum()
        r.append(min(inn,out)/max(max(inn,out),1e-12))
    return min(r)  # lower = more one-way-like extreme state
def s2_block(T):
    off=T-np.diag(np.diag(T)); om=off.sum()
    def within(idx):
        idx=list(idx); rest=[i for i in range(11) if i not in idx]
        return (off[np.ix_(idx,idx)].sum()+off[np.ix_(rest,rest)].sum())/max(om,1e-12)
    ours=within(SURFACE_IDX)
    allv=[within(c) for c in itertools.combinations(range(11),4)]
    pct=sum(1 for v in allv if v>=ours)/len(allv)   # percentile of the 4+7 among all 330 splits (leg (c))
    return ours, pct, max(allv)
s5_obj,_=stats(M)
s3_obj=max(stats(M)[1](M,*TWINS[0]), stats(M)[1](M,*TWINS[1]))
s4_obj=s4_oneway(M)
s2_obj,s2_pct,_=s2_block(M)
print(f"OBJECT: S5 top3share={s5_obj:.4f}  S3 twin-asym(max of named)={s3_obj:.4f}  S4 min-flow-ratio={s4_obj:.4f}  S2 within-share(4+7)={s2_obj:.4f} (percentile among 330 splits: {s2_pct:.4f})")
def draw(ens):
    if ens=='dirichlet': T=rng.dirichlet(np.ones(11),11)
    elif ens=='haar':
        z=rng.normal(size=(11,11))+1j*rng.normal(size=(11,11))
        q,_=np.linalg.qr(z); T=np.abs(q)**2
    elif ens=='sparse': T=rng.dirichlet(np.ones(11)*0.15,11)
    elif ens=='detmap':
        T=np.zeros((11,11))
        for i in range(11): T[i,rng.integers(11)]=1.0
        T=0.9*T+0.1*rng.dirichlet(np.ones(11),11)
    return T
res={}
B=10000
for ens in ('dirichlet','haar','sparse','detmap'):
    c=collections.Counter(); conj=0
    for _ in range(B):
        T=draw(ens)
        hits={}
        hits['S5']= stats(T)[0]>=s5_obj
        hits['S3']= best_two_disjoint_swaps(T)<=s3_obj
        hits['S4']= s4_oneway(T)<=s4_obj
        w,_,mx=0,0,0
        # S2 for nulls: does the BEST 4-split reach the object's 4+7 within-share?
        hits['S2']= s2_block(T)[2]>=s2_obj
        for k,v in hits.items(): c[k]+=v
        conj+= all(hits.values())
    res[ens]={k:c[k]/B for k in c}|{'CONJUNCTION':conj/B}
    print(ens, {k:round(v,4) for k,v in res[ens].items()})
res['object']={'S5':s5_obj,'S3':s3_obj,'S4':s4_obj,'S2_within':s2_obj,'S2_percentile_among_own_splits':s2_pct}
json.dump(res,open('lega_results.json','w'),indent=1)
