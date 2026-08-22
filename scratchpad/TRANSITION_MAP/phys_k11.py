"""PHYS-K11-1 battery. Prereg frozen before first execution (PHYS_K11_PREREG.md).
Implementation note (notation fix, not design change): site dephasing implemented
in the standard form L(rho) = -i[H,rho] + gamma*(diag(rho) - rho)."""
import json, collections
import numpy as np
from scipy.linalg import expm, eigvals, eigh
rng = np.random.default_rng(20260823)
KINDS=['Priorities','Rules','Manner','Identity','Confidence','Facts','Circumstances','Process','Model','Structure','Premises']
PLAIN={'axiotic':'Priorities','deontic':'Rules','pragmatic':'Manner','ontological':'Identity','epistemic':'Confidence','empirical':'Facts','contingent':'Circumstances','procedural':'Process','nomological':'Model','structural':'Structure','axiomatic':'Premises','testimonial':'Record'}
KI={k:i for i,k in enumerate(KINDS)}
TW=[(KI['Priorities'],KI['Process']),(KI['Structure'],KI['Circumstances'])]

def anchor_c(path):
    J=[json.loads(l) for l in open(path)]
    tgt={json.loads(l)['id']:PLAIN[json.loads(l)['kind_target']] for l in open('/home/emoore/CIRISOntology/scratchpad/plane_corpus/corpus_full.jsonl')}
    by=collections.defaultdict(dict)
    for j in J: by[j['id']][j['model']]=j['kind']
    M=np.zeros((11,11))
    for i,t in tgt.items():
        if t not in KI: continue
        for v in by.get(i,{}).values():
            if v in KI: M[KI[t],KI[v]]+=1
    M=M/np.maximum(M.sum(axis=1,keepdims=True),1e-12)
    c=(M+M.T)/2; np.fill_diagonal(c,0)
    c=c/c[c>0].mean() if (c>0).any() else c
    c=c/ (c.sum()/(110))  # mean over ALL 110 off-diag entries (incl zeros) = 1
    np.fill_diagonal(c,0)
    return c

def group_avg(c):
    def sw(m,a,b):
        p=list(range(11)); p[a],p[b]=p[b],p[a]; return m[np.ix_(p,p)]
    return (c + sw(c,*TW[0]) + sw(c,*TW[1]) + sw(sw(c,*TW[0]),*TW[1]))/4

def H_of(c, chord=None, phi=0.0):
    H=c.astype(complex).copy()
    if chord is not None:
        i,j=chord; H[i,j]=c[i,j]*np.exp(-1j*phi); H[j,i]=c[j,i]*np.exp(1j*phi)
    return H

def liou_gap(H, g):
    I=np.eye(11)
    L=-1j*(np.kron(I,H)-np.kron(H.T,I))
    D=np.zeros((121,121))
    for i in range(11):
        P=np.zeros((11,11)); P[i,i]=1
        D+=np.kron(P,P)
    L=L+g*(D-np.eye(121))
    ev=eigvals(L)
    re=np.sort(ev.real)[::-1]
    return -re[1]  # gap: skip the steady state at ~0

R={}
cP2=anchor_c('panel2_validation.jsonl')
cSP=anchor_c('/home/emoore/CIRISOntology/scratchpad/plane_corpus/full_judgments.jsonl')

# ===== S1 =====
s1={}
for name,c in [('CUR-P2',cP2),('CUR-SP',cSP)]:
    cb=group_avg(c)
    ex={}
    for lab,(a,b) in zip(['Pri/Prc','Str/Cir'],TW):
        psi=np.zeros(11); psi[a]=1/np.sqrt(2); psi[b]=-1/np.sqrt(2)
        res=np.linalg.norm(cb@psi + cb[a,b]*psi)
        ex[lab]={'eig_pred':-cb[a,b],'residual':float(res)}
    w,V=eigh(c)
    leak={}
    for lab,(a,b) in zip(['Pri/Prc','Str/Cir'],TW):
        psi=np.zeros(11); psi[a]=1/np.sqrt(2); psi[b]=-1/np.sqrt(2)
        ov=np.abs(V.T@psi)**2
        leak[lab]=float(1-ov.max())
    s1[name]={'exact_tier':ex,'leakage':leak,'S1b_sign_StrCir_gt_PriPrc':bool(leak['Str/Cir']>leak['Pri/Prc'])}
R['S1']=s1

# ===== S2 =====
A=np.zeros((11,11))
chords=[(i,j) for i in range(1,11) for j in range(i+1,11)]
ph=rng.uniform(0,2*np.pi,len(chords))
Hp=cP2.astype(complex).copy(); Hm=cP2.astype(complex).copy()
for (i,j),p in zip(chords,ph):
    Hp[i,j]*=np.exp(-1j*p); Hp[j,i]*=np.exp(1j*p)
    Hm[i,j]*=np.exp(1j*p);  Hm[j,i]*=np.exp(-1j*p)
Up=expm(-1j*Hp); Um=expm(-1j*Hm)
R['S2']={'max_abs_U(-A)-U(A)^T':float(np.abs(Um-Up.T).max())}

# ===== S3 =====
GAM=[0.1,0.5,2.0]; PHI=np.linspace(0,2*np.pi,12,endpoint=False)
s3={'gamma':GAM,'phi':list(PHI)}
resp={}
even_worst=0.0
base={g:liou_gap(H_of(cP2),g) for g in GAM}
for ci,ch in enumerate(chords):
    row={}
    for g in GAM:
        nus=[liou_gap(H_of(cP2,ch,p),g) for p in PHI]
        nus=np.array(nus)
        # evenness: nu(phi) vs nu(2pi-phi): indices k and (12-k)%12
        ev=max(abs(nus[k]-nus[(12-k)%12]) for k in range(12))
        even_worst=max(even_worst,ev/max(base[g],1e-15))
        row[g]=float(np.abs(nus-base[g]).max()/base[g])
    resp[str(ch)]=row
s3['base_gap']= {str(g):float(base[g]) for g in GAM}
s3['even_worst_rel']=float(even_worst)
# dephased comparator
gD=50.0; baseD=liou_gap(H_of(cP2),gD)
topch=max(resp,key=lambda k:resp[k][0.5])
i,j=eval(topch)
respD=max(abs(liou_gap(H_of(cP2,(i,j),p),gD)-baseD) for p in PHI)/baseD
s3['dephased_top_response']=float(respD)
top=sorted(resp.items(),key=lambda kv:-kv[1][0.5])[:8]
s3['top_loops_g0.5']=[(k,{str(g):round(v,6) for g,v in val.items()}) for k,val in top]
R['S3']=s3

# ===== S4 =====
d=np.array([1,0,0,0,1,0,1,1,2,1,3])
eps_grid=np.exp(np.linspace(np.log(0.05),np.log(5),41))
ipr=[]
for e in eps_grid:
    Me=np.power(e,np.abs(d[:,None]-d[None,:])).astype(float); np.fill_diagonal(Me,0)
    w,V=eigh(Me)
    ipr.append(float(np.mean(np.sum(V**4,axis=0))))
R['S4']={'eps':[round(float(x),4) for x in eps_grid],'mean_IPR':[round(x,5) for x in ipr]}

# ===== S6 slice =====
pairs=[(i,j) for i in range(11) for j in range(i+1,11)]
PI={p:k for k,p in enumerate(pairs)}
def H2_of(H):
    n=len(pairs); H2=np.zeros((n,n),complex)
    for (i,j),a in PI.items():
        for k in range(11):
            if k!=i and k!=j:
                H2[PI[tuple(sorted((k,j)))],a]+=H[k,i]
                H2[PI[tuple(sorted((i,k)))],a]+=H[k,j]
    return H2
ti,tj=eval(topch)
p2=[]
for p in PHI:
    U2=expm(-1j*H2_of(H_of(cP2,(ti,tj),p)))
    p2.append(float(np.abs(U2[PI[(min(ti,tj),max(ti,tj))],PI[(0,1)]])**2))
p2=np.array(p2)
R['S6']={'loop':topch,'even_resid':float(max(abs(p2[k]-p2[(12-k)%12]) for k in range(12))),'range':float(p2.max()-p2.min())}

json.dump(R,open('phys_k11_results.json','w'),indent=1,default=str)
print("S1:",json.dumps(s1,indent=1)[:900])
print("S2 max|U(-A)-U(A)^T| =",R['S2']['max_abs_U(-A)-U(A)^T'])
print("S3 base gaps:",s3['base_gap'],"even_worst_rel:",s3['even_worst_rel'],"dephased_top:",s3['dephased_top_response'])
print("S3 top loops (g=0.5):"); 
for k,v in s3['top_loops_g0.5']: print("  ",KINDS[eval(k)[0]],"-",KINDS[eval(k)[1]],v)
print("S4 IPR ends:",R['S4']['mean_IPR'][0],R['S4']['mean_IPR'][20],R['S4']['mean_IPR'][-1])
print("S6:",R['S6'])
