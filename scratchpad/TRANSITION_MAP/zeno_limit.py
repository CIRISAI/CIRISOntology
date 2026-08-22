"""Do the limits s->0 (weak symmetry breaking) and kappa->inf (strong loss) COMMUTE?

Model, built from the object's own coupling matrix:
  H0 = twin-symmetrised coupling (exact twin symmetry -> d is an exact dark state,
       Core/DarkState.twin_dark_state)
  V  = the odd part, so H(s) = H0 + s*V breaks the symmetry by dose s
  loss: non-Hermitian  H_eff(s,k) = H(s) - i*(k/2)*Q,  Q = 1 - d d^T (bright sector)
  Gamma(s,k) = -2*Im(E)  for the eigenvalue whose eigenvector has max dark overlap.

Perturbative prediction (second-order Feshbach / the K2.3 coefficient):
  Gamma ~ s^2 * C(k),  C(k) = sum_j |<b_j|V|d>|^2 * k / ((E_d-E_j)^2 + (k/2)^2)

The question is whether Gamma/(s^2 C(k)) -> 1 UNIFORMLY in k, or whether the order of
limits matters. Computed in extended precision so a failure cannot be a float artifact.
"""
import json, collections, itertools, numpy as np, mpmath as mp
mp.mp.dps = 60

K=['Priorities','Rules','Manner','Identity','Confidence','Facts','Circumstances','Process','Model','Structure','Premises']
KI={k:i for i,k in enumerate(K)}
PLAIN={'axiotic':'Priorities','deontic':'Rules','pragmatic':'Manner','ontological':'Identity','epistemic':'Confidence','empirical':'Facts','contingent':'Circumstances','procedural':'Process','nomological':'Model','structural':'Structure','axiomatic':'Premises','testimonial':'Record'}
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
S=(M+M.T)/2; np.fill_diagonal(S,0); S=S/ (S.sum()/110)

a,b=KI['Structure'],KI['Circumstances']
P=np.eye(11); P[[a,b]]=P[[b,a]]
H0=(S+P@S@P)/2; V=(S-P@S@P)/2
d=np.zeros(11); d[a]=1/np.sqrt(2); d[b]=-1/np.sqrt(2)
Q=np.eye(11)-np.outer(d,d)

# perturbative coefficient from the symmetry-restored bright spectrum
w,U=np.linalg.eigh(H0)
Ed=float(d@H0@d)
mu=[]; De=[]
for j in range(11):
    bj=U[:,j]
    if abs(bj@d)>1-1e-9: continue
    ov=float(bj@V@d)**2
    if ov>1e-18: mu.append(ov); De.append(float(w[j]-Ed))
mu=np.array(mu); De=np.array(De)
def Ck(k): return float(np.sum(mu*k/(De**2+(k/2)**2)))

def gamma(s,k):
    Hm=mp.matrix(11,11)
    for i in range(11):
        for j in range(11):
            Hm[i,j]=mp.mpf(H0[i,j])+mp.mpf(s)*mp.mpf(V[i,j])-1j*mp.mpf(k)/2*mp.mpf(Q[i,j])
    E,ER=mp.eig(Hm)
    best,bg=-1,None
    for idx in range(11):
        v=[ER[r,idx] for r in range(11)]
        nrm=mp.sqrt(sum(abs(x)**2 for x in v))
        ov=abs(sum(mp.mpf(d[r])*v[r] for r in range(11))/nrm)**2
        if ov>best: best,bg=ov,-2*mp.im(E[idx])
    return float(bg), float(best)

print(f"{'kappa':>10} {'s':>10} {'Gamma':>14} {'s^2*C(k)':>14} {'ratio':>10} {'dark ov':>9}")
rows=[]
for k in (0.1, 1.0, 10.0, 100.0, 1000.0):
    Ckv=Ck(k)
    for s in (1e-2, 1e-3, 1e-4):
        g,ov=gamma(s,k)
        pred=s*s*Ckv
        r=g/pred if pred>0 else float('nan')
        rows.append({'kappa':k,'s':s,'Gamma':g,'pred':pred,'ratio':r,'dark_overlap':ov})
        print(f"{k:>10g} {s:>10g} {g:>14.6e} {pred:>14.6e} {r:>10.5f} {ov:>9.4f}")
json.dump(rows,open('zeno_limit_results.json','w'))
