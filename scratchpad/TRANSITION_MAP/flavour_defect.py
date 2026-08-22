"""FDA-1 runner. Frozen in FLAVOUR_DEFECT_PREREG.md before any flavour number computed.
Estimator is theorem-fixed by Core/DefectCoupling.lean + Core/DarkState.lean."""
import json, math, collections
import numpy as np

def ckm_pmns(s12,s23,s13,delta):
    c12,c23,c13=math.sqrt(1-s12**2),math.sqrt(1-s23**2),math.sqrt(1-s13**2)
    e=np.exp(1j*delta)
    V=np.array([
      [c12*c13, s12*c13, s13*np.conj(e)],
      [-s12*c23-c12*s23*s13*e, c12*c23-s12*s23*s13*e, s23*c13],
      [s12*s23-c12*c23*s13*e, -c12*s23-s12*c23*s13*e, c23*c13]])
    return V

def sym_norm(M):
    S=(M+M.T)/2.0
    off=S-np.diag(np.diag(S))
    m=off.sum()/(S.shape[0]*(S.shape[0]-1))
    return S/m

def diagnostics(S, a, b):
    n=S.shape[0]
    w=np.zeros(n); w[a]=1; w[b]=-1
    P=np.eye(n)-np.outer(w,w)
    D=S-P@S@P
    delta=np.linalg.norm(D,'fro')
    d=w/np.sqrt(2); Q=np.eye(n)-np.outer(d,d)
    gdb=np.linalg.norm(Q@S@d)
    u=S@w; alpha=w@u
    thm=4*(u@u)-2*alpha**2                     # Core/DefectCoupling.trace_defect_sq
    gateA=abs(np.trace(D@D)-thm)
    gateB=abs(gdb-delta/(2*math.sqrt(2)))       # K2 identity
    ev,V=np.linalg.eigh(S)
    ov=np.abs(V.T@d)**2
    return dict(delta=float(delta), gdb=float(gdb), L_spec=float(1-ov.max()),
                gateA=float(gateA), gateB=float(gateB))

R={}
# quark: PDG 2026 verified values
Vq=ckm_pmns(0.22517,0.04189,0.003763, math.radians(66.4))
# lepton: PDG 2026 global fit (NO best fit)
Vl=ckm_pmns(math.sqrt(0.307), math.sqrt(0.561), math.sin(math.radians(8.59)), math.radians(212))
for name,V in [('QUARK |V_CKM|^2',Vq),('LEPTON |U_PMNS|^2',Vl)]:
    S=sym_norm(np.abs(V)**2)
    R[name]={}
    print(f"=== {name}")
    for (a,b),lab in [((0,1),'gen 1-2'),((1,2),'gen 2-3'),((0,2),'gen 1-3')]:
        r=diagnostics(S,a,b); R[name][lab]=r
        print(f"  {lab}: Delta_sigma={r['delta']:.4f}  g_DB={r['gdb']:.4f}  L_spec={r['L_spec']:.4f}"
              f"   [gates {r['gateA']:.1e}, {r['gateB']:.1e}]")

# object arm, identical procedure
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
So=sym_norm(M); np.fill_diagonal(So, So[0,0]*0 + np.diag(sym_norm(M)))
So=sym_norm(M)
print("=== OBJECT (CUR-P2, 11x11)")
R['OBJECT']={}
for (a,b),lab in [((KI['Priorities'],KI['Process']),'twin Pri/Prc'),((KI['Structure'],KI['Circumstances']),'twin Str/Cir')]:
    r=diagnostics(So,a,b); R['OBJECT'][lab]=r
    print(f"  {lab}: Delta_sigma={r['delta']:.4f}  g_DB={r['gdb']:.4f}  L_spec={r['L_spec']:.4f}"
          f"   [gates {r['gateA']:.1e}, {r['gateB']:.1e}]")
json.dump(R,open('flavour_defect_results.json','w'),indent=1)
