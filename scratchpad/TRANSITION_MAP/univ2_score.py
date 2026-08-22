"""UNIV-2 scorer. Applies the FOUR frozen stakes of UNIV2_PREREG.md to a fresh
substrate. Written before the substrate's judgments exist.

P-D uses a Diaconis-Sturmfels-style EXACT null: margin-preserving swap moves on the
symmetric disagreement table (the standing memory says a label-permutation null is
wrong for this data, and UNIV-1's mis-signed criterion is the reason this stake was
rewritten two-sided)."""
import json, sys, itertools, collections, math
import numpy as np
rng = np.random.default_rng(20260823)
K=['Priorities','Rules','Manner','Identity','Confidence','Facts','Circumstances','Process','Model','Structure','Premises']
KI={k:i for i,k in enumerate(K)}
D={'Facts':0,'Confidence':1,'Model':2,'Premises':3,'Rules':0,'Priorities':1,'Process':1,
   'Identity':0,'Manner':0,'Structure':1,'Circumstances':1}          # pinned from the Lean
dv=np.array([D[k] for k in K]); dd=np.abs(dv[:,None]-dv[None,:])
TW=[('Priorities','Process'),('Structure','Circumstances')]

def disagreement(path):
    by=collections.defaultdict(list)
    for l in open(path):
        j=json.loads(l)
        if j.get('kind') in KI: by[j['id']].append(j['kind'])
    S=np.zeros((11,11)); ev=0; items=0
    for i,vs in by.items():
        if len(vs)>=2: items+=1
        for a,b in itertools.combinations(vs,2):
            if a!=b: S[KI[a],KI[b]]+=1; S[KI[b],KI[a]]+=1; ev+=1
    marg=np.array([sum(1 for l in open(path) if json.loads(l).get('kind')==k) for k in K],float)
    p=marg/max(marg.sum(),1); ent=float(-(p[p>0]*np.log(p[p>0])).sum())
    return S, ev, items, ent

def cascade_r(S):
    off=S-np.diag(np.diag(S))
    v=np.sort(np.array([off[i,j] for i in range(11) for j in range(i+1,11)]))[::-1]
    t=[v[3*k:3*k+3].mean() for k in range(3)]
    if t[0]<=0 or t[1]<=0: return float('nan')
    return math.sqrt((t[1]/t[0])*(t[2]/t[1]))

def swap_asym(S,a,b):
    P=np.eye(11); ia,ib=KI[a],KI[b]; P[[ia,ib]]=P[[ib,ia]]
    return float(np.abs(P@S@P-S).sum()/max(S.sum(),1e-12))

def depth_ratio(S):
    off=S-np.diag(np.diag(S))
    same=off[(dd==0)&~np.eye(11,dtype=bool)].mean()
    cross=off[dd>0].mean()
    return float(cross/max(same,1e-12)), float(same), float(cross)

def s5(S):
    off=S-np.diag(np.diag(S))
    v=np.sort(np.array([off[i,j] for i in range(11) for j in range(i+1,11)]))[::-1]
    return float(v[:3].sum()/max(v.sum(),1e-12))

def ds_null(S, n=2000, burn=2000, thin=20):
    """margin-preserving symmetric swap moves (Diaconis-Sturmfels basis element)."""
    A=S.copy(); out=[]
    pairs=[(i,j) for i in range(11) for j in range(i+1,11)]
    steps=burn+n*thin
    for t in range(steps):
        (i,j),(k,l)=[pairs[x] for x in rng.choice(len(pairs),2,replace=False)]
        if len({i,j,k,l})<4: continue
        if A[i,j]>0 and A[k,l]>0:
            A[i,j]-=1; A[j,i]-=1; A[k,l]-=1; A[l,k]-=1
            A[i,l]+=1; A[l,i]+=1; A[k,j]+=1; A[j,k]+=1
        if t>=burn and (t-burn)%thin==0: out.append(s5(A))
    return np.array(out)

if __name__=='__main__':
    path=sys.argv[1]; label=sys.argv[2] if len(sys.argv)>2 else path
    S,ev,items,ent=disagreement(path)
    print(f"=== UNIV-2 on {label}")
    g1,g2,g3 = ev>=150, ent>=1.2, items>=40
    print(f"GATES: events={ev} (>=150: {g1})  entropy={ent:.3f} (>=1.2: {g2})  items={items} (>=40: {g3})")
    if not (g1 and g2 and g3):
        print("VOID — gates not met, no stake is scored."); sys.exit(0)
    r=cascade_r(S); pa = 0.45<=r<=0.60
    print(f"P-A cascade r = {r:.4f}   band [0.45,0.60] -> {'PASS' if pa else 'FAIL'}")
    a1=swap_asym(S,*TW[1]); a2=swap_asym(S,*TW[0]); pb=a1>a2
    print(f"P-B twin ordering: Str/Cir {a1:.4f} > Pri/Prc {a2:.4f} -> {'PASS' if pb else 'FAIL'}")
    ratio,same,cross=depth_ratio(S); pc=ratio>=1.5
    print(f"P-C depth inversion: cross {cross:.3f} / same {same:.3f} = {ratio:.3f}  (>=1.5) -> {'PASS' if pc else 'FAIL'}")
    obs=s5(S); null=ds_null(S)
    lo,hi=np.percentile(null,[5,95]); pd_=(obs<lo) or (obs>hi)
    print(f"P-D localization: S5={obs:.4f}  DS-null central90=[{lo:.4f},{hi:.4f}] -> {'PASS' if pd_ else 'FAIL'}")
    print(f"\nSUMMARY: {sum([pa,pb,pc,pd_])}/4 stakes passed on a substrate whose bands were frozen before it existed.")
