import json, collections, random, sys
random.seed(20260821)
arms={json.loads(l)['id']:json.loads(l)['arm'] for l in open('t4_items.jsonl')}
def modals(path):
    J=[json.loads(l) for l in open(path)]
    byitem=collections.defaultdict(dict)
    for j in J: byitem[j['id']][j['model']]=j['kind']
    out={}
    for i,v in byitem.items():
        c=collections.Counter(v.values()); t,n=c.most_common(1)[0]
        out[i]=t if n>=2 else None
    return out
W=modals('t4_whole_judgments.jsonl'); CA=modals('t4_cuta_judgments.jsonl')
def shifts(arm):
    ids=[i for i,a in arms.items() if a==arm and W.get(i) and CA.get(i)]
    sh=[1 if W[i]!=CA[i] else 0 for i in ids]
    return sh, ids
shP,idsP=shifts('P'); shC,idsC=shifts('C')
rP=sum(shP)/len(shP); rC=sum(shC)/len(shC)
# one-sided permutation p for shift(P)-shift(C)>0
allv=shP+shC; lab=[1]*len(shP)+[0]*len(shC); obs=rP-rC
cnt=0; B=10000
for _ in range(B):
    random.shuffle(lab)
    a=[v for v,l in zip(allv,lab) if l]; b=[v for v,l in zip(allv,lab) if not l]
    if (sum(a)/len(a)-sum(b)/len(b))>=obs-1e-12: cnt+=1
p1=cnt/B
gate={"shift_P":round(rP,4),"shift_C":round(rC,4),"diff":round(obs,4),"p_one_sided":p1,
      "n_P":len(shP),"n_C":len(shC),
      "verdict":"PASS" if (obs>0 and p1<0.05) else "VOID-cut-never-read"}
json.dump(gate,open('t4_gate.json','w'),indent=1)
print("GATE1:",json.dumps(gate))
if gate["verdict"]!="PASS": sys.exit(0)
# stage 2: arm M
shM,idsM=shifts('M')
rM=sum(shM)/len(shM)
allv=shM+shC; lab=[1]*len(shM)+[0]*len(shC); obsM=rM-rC
cnt=0
for _ in range(B):
    random.shuffle(lab)
    a=[v for v,l in zip(allv,lab) if l]; b=[v for v,l in zip(allv,lab) if not l]
    if (sum(a)/len(a)-sum(b)/len(b))>=obsM-1e-12: cnt+=1
pM=cnt/B
# bootstrap upper bound on rM-rC
bsd=[]
for _ in range(B):
    x=[random.choice(shM) for _ in shM]; y=[random.choice(shC) for _ in shC]
    bsd.append(sum(x)/len(x)-sum(y)/len(y))
bsd.sort(); hi=bsd[int(0.975*B)]
moved=[i for i in idsM if W[i]!=CA[i]]
CONTENT={'Facts','Rules','Identity','Confidence','Premises'}
CARRIER={'Structure','Circumstances'}
dest=collections.Counter(CA[i] for i in moved)
content_share=sum(v for k,v in dest.items() if k in CONTENT)/max(1,len(moved))
carrier_share=sum(v for k,v in dest.items() if k in CARRIER)/max(1,len(moved))
half=0.5*(rP-rC)
res={"shift_M":round(rM,4),"shift_C":round(rC,4),"diff":round(obsM,4),"p":pM,
     "hi95":round(hi,4),"half_control":round(half,4),"moved_n":len(moved),
     "destinations":dict(dest),"content_share":round(content_share,3),"carrier_share":round(carrier_share,3)}
if pM<0.01 and obsM>=half and content_share>=2/3: res["band"]="HOLISM CONFIRMED"
elif pM>=0.05 and hi<half: res["band"]="REFUTED"
elif pM>=0.05: res["band"]="UNDERPOWERED"
elif obsM>=half and content_share<2/3: res["band"]="AMBIGUOUS-direction"
else: res["band"]="AMBIGUOUS"
res["K5b_carrier_adverse"]= carrier_share>=1/3
json.dump(res,open('t4_primary.json','w'),indent=1)
print("PRIMARY:",json.dumps(res))
# CUT-B secondary
CB=modals('t4_cutb_judgments.jsonl')
idsB=[i for i in idsM if CB.get(i)]
shB=[1 if W[i]!=CB[i] else 0 for i in idsB]
print("CUTB: shift",round(sum(shB)/max(1,len(shB)),4),"n",len(shB))
