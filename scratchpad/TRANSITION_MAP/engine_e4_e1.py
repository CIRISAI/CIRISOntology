"""ENGINE GAP E4 (conserved quantities on K11) and E1 (a metric).

E4 prediction, stated before computing: K11 has no translation symmetry, so it has no
momentum. Its symmetry is Z2xZ2 (Symmetry.aut_with_stack_card = 4), so the conserved
charges should be the TWO TWIN PARITIES — and on the MEASURED matrix they should be
broken by exactly the defect we already measured (DefectCoupling).

E1: the natural metric on a spring network is resistance distance (commute time) from
the Laplacian — computable now."""
import json, collections, itertools, numpy as np
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
S=(M+M.T)/2; np.fill_diagonal(S,0); S=S/(S.sum()/110)

TW=[('Priorities','Process'),('Structure','Circumstances')]
def swapmat(a,b):
    P=np.eye(11); ia,ib=KI[a],KI[b]; P[[ia,ib]]=P[[ib,ia]]; return P
P1,P2=swapmat(*TW[0]),swapmat(*TW[1])
H0=sum(g@S@g for g in [np.eye(11),P1,P2,P1@P2])/4      # Z2xZ2 group average

print("=== E4: conserved charges on K11 ===")
print("group order:", 4, " (identity, two swaps, product) — matches aut_with_stack_card")
# character sectors: simultaneous eigenspaces of P1,P2 (both commute, both involutions)
sectors={}
for s1 in (1,-1):
    for s2 in (1,-1):
        Proj=(np.eye(11)+s1*P1)@(np.eye(11)+s2*P2)/4
        r=int(round(np.trace(Proj)))
        sectors[(s1,s2)]=(Proj,r)
        print(f"  sector (P1={s1:+d}, P2={s2:+d}): dim {r}")
print("  total:", sum(v[1] for v in sectors.values()))
# is H0 block diagonal (i.e. are the parities conserved)?
worst=0
for k1,(Pr1,_) in sectors.items():
    for k2,(Pr2,_) in sectors.items():
        if k1==k2: continue
        worst=max(worst, np.abs(Pr1@H0@Pr2).max())
print(f"  H0 inter-sector leakage (symmetrised): {worst:.2e}  -> parities CONSERVED")
worstM=0
for k1,(Pr1,_) in sectors.items():
    for k2,(Pr2,_) in sectors.items():
        if k1==k2: continue
        worstM=max(worstM, np.abs(Pr1@S@Pr2).max())
print(f"  H  inter-sector leakage (MEASURED):    {worstM:.4f}  -> broken by the measured defect")
V=S-H0
print(f"  ||V||_F (the breaking) = {np.linalg.norm(V,'fro'):.4f}")
print(f"  ratio leakage/||V||_F  = {worstM/np.linalg.norm(V,'fro'):.4f}")

print("\n=== E1: a metric from the Laplacian (resistance distance) ===")
L=np.diag(S.sum(axis=1))-S
Lp=np.linalg.pinv(L)
R=np.zeros((11,11))
for i in range(11):
    for j in range(11):
        R[i,j]=Lp[i,i]+Lp[j,j]-2*Lp[i,j]
tri=[R[i,j] for i in range(11) for j in range(i+1,11)]
print(f"  resistance distance: min {min(tri):.4f}  max {max(tri):.4f}  median {np.median(tri):.4f}")
# metric axioms check
viol=0
for i,j,k in itertools.combinations(range(11),3):
    if R[i,j] > R[i,k]+R[k,j]+1e-9: viol+=1
print(f"  triangle inequality violations: {viol}  (resistance distance IS a metric -> expect 0)")
print(f"  closest pair:  {K[int(np.unravel_index(np.argmin(R+np.eye(11)*1e9),R.shape)[0])]} - {K[int(np.unravel_index(np.argmin(R+np.eye(11)*1e9),R.shape)[1])]}")
print(f"  farthest pair: {K[int(np.unravel_index(np.argmax(R),R.shape)[0])]} - {K[int(np.unravel_index(np.argmax(R),R.shape)[1])]}")
for (a,b) in TW:
    print(f"  twin {a}/{b}: resistance {R[KI[a],KI[b]]:.4f}")
np.save('k11_metric.npy',R)
