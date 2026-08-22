"""A2A BRIDGE via constraint-matching. Stakes stated in the header BEFORE running.

The three-generation collapse theorem (Core/DefectCoupling.defect_three_gen_collapse)
needs TWO hypotheses: n=3 AND equal row sums. Flavour satisfies both; the object
satisfies neither. That gives a CONSTRUCTIVE apples-to-apples protocol:
  step 1 - impose the missing conservation law (Sinkhorn -> doubly stochastic);
  step 2 - match dimension (restrict to 3-subsets, the shape of a flavour table);
  step 3 - whatever excess SURVIVES both is the object's genuine structure.

STAKES (frozen before execution):
 A. After Sinkhorn at n=11, the constrained floor is g_DB/|dS| >= sqrt(1/4+1/(2(n-2)))
    = 0.5528. If the twins collapse TO that floor, their excess was entirely the
    missing constraint. If they stay well above it, the excess is genuine.
 B. After Sinkhorn AND restriction to a 3-subset, the collapse theorem MUST hold
    (ratio exactly sqrt(3)/2 = 0.8660). Any deviation is a code error, not physics -
    this is the pipeline gate.
 C. The Sinkhorn scaling spread is a NEW measurable: how much backward conservation
    the object was missing. Reported as a signature entry, no prior expectation.
"""
import numpy as np, json, collections, math
from flavour_defect import sym_norm, ckm_pmns

def sinkhorn(S, iters=20000, tol=1e-14):
    """Symmetric Sinkhorn: returns doubly-stochastic D S D and the scaling d."""
    A=S.copy().astype(float); n=A.shape[0]; d=np.ones(n)
    for _ in range(iters):
        r=(A*np.outer(d,d)).sum(axis=1)
        dn=d/np.sqrt(r)
        if np.abs(dn-d).max()<tol: d=dn; break
        d=dn
    return np.outer(d,d)*A, d

def ratio(S,a,b):
    n=S.shape[0]; w=np.zeros(n); w[a]=1; w[b]=-1; dv=w/np.sqrt(2)
    Q=np.eye(n)-np.outer(dv,dv)
    return np.linalg.norm(Q@S@dv)/abs(S[a,a]-S[b,b])

PLAIN={'axiotic':'Priorities','deontic':'Rules','pragmatic':'Manner','ontological':'Identity','epistemic':'Confidence','empirical':'Facts','contingent':'Circumstances','procedural':'Process','nomological':'Model','structural':'Structure','axiomatic':'Premises','testimonial':'Record'}
K=['Priorities','Rules','Manner','Identity','Confidence','Facts','Circumstances','Process','Model','Structure','Premises']
KI={k:i for i,k in enumerate(K)}
J=[json.loads(l) for l in open('panel2_validation.jsonl')]
tgt={json.loads(l)['id']:PLAIN[json.loads(l)['kind_target']] for l in open('/home/emoore/CIRISOntology/scratchpad/plane_corpus/corpus_full.jsonl')}
by=collections.defaultdict(dict)
for j in J: by[j['id']][j['model']]=j['kind']
M=np.zeros((11,11))
for i,t in tgt.items():
    if t not in KI: continue
    for v in by.get(i,{}).values():
        if v in KI: M[KI[t],KI[v]]+=1
M=M/np.maximum(M.sum(axis=1,keepdims=True),1e-12)
S=sym_norm(M)
Sd,dscale=sinkhorn(S)
rs=Sd.sum(axis=1)
print(f"STEP 1 — Sinkhorn: row-sum spread/mean {(rs.max()-rs.min())/rs.mean():.2e} (was 0.761)")
print(f"  scaling spread max/min = {dscale.max()/dscale.min():.3f}   [STAKE C: the missing-conservation measure]")
floor=math.sqrt(0.25+1/(2*(11-2)))
print(f"\nSTAKE A — n=11 constrained floor = {floor:.4f}")
for lab,(a,b) in [('Pri/Prc',(KI['Priorities'],KI['Process'])),('Str/Cir',(KI['Structure'],KI['Circumstances']))]:
    print(f"  {lab}: before Sinkhorn {ratio(S,a,b):.4f}  ->  after {ratio(Sd,a,b):.4f}   (floor {floor:.4f})")
print("\nSTAKE B — restrict to 3-subsets, Sinkhorn, collapse MUST give 0.8660 (pipeline gate)")
import itertools
devs=[]
for tri in itertools.combinations(range(11),3):
    sub=Sd[np.ix_(tri,tri)]
    sub3,_=sinkhorn(sub)
    for (x,y) in [(0,1),(1,2),(0,2)]:
        if abs(sub3[x,x]-sub3[y,y])>1e-9: devs.append(abs(ratio(sub3,x,y)-math.sqrt(3)/2))
print(f"  {len(devs)} triple-pairs tested, worst deviation from sqrt(3)/2 = {max(devs):.2e}")
print("\nSTEP 2 — the object's 165 three-generation-shaped tables vs flavour's 2")
vals=[]
for tri in itertools.combinations(range(11),3):
    sub,_=sinkhorn(Sd[np.ix_(tri,tri)])
    for (x,y) in [(0,1),(1,2),(0,2)]:
        ds=abs(sub[x,x]-sub[y,y])
        if ds>1e-9: vals.append(ds)
vals=np.array(vals)
Vq=ckm_pmns(0.22517,0.04189,0.003763,math.radians(66.4)); Sq,_=sinkhorn(sym_norm(np.abs(Vq)**2))
Vl=ckm_pmns(math.sqrt(0.307),math.sqrt(0.561),math.sin(math.radians(8.59)),math.radians(212)); Sl,_=sinkhorn(sym_norm(np.abs(Vl)**2))
fq=[abs(Sq[x,x]-Sq[y,y]) for x,y in [(0,1),(1,2),(0,2)]]
fl=[abs(Sl[x,x]-Sl[y,y]) for x,y in [(0,1),(1,2),(0,2)]]
print(f"  object triples: n={len(vals)}  median dS={np.median(vals):.4f}  range [{vals.min():.4f},{vals.max():.4f}]")
print(f"  QUARK  dS per pair: {[round(x,4) for x in fq]}")
print(f"  LEPTON dS per pair: {[round(x,4) for x in fl]}")
print(f"  quark min {min(fq):.4f} sits at object percentile {100*(vals<min(fq)).mean():.1f}")
print(f"  lepton min {min(fl):.4f} sits at object percentile {100*(vals<min(fl)).mean():.1f}")
