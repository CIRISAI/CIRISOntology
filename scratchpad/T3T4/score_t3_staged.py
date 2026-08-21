import json, collections, random, sys
random.seed(20260821)
J=[json.loads(l) for l in open('t3_judgments.jsonl')]
byitem=collections.defaultdict(dict)
for j in J: byitem[j['id']][j['model']]=j['kind']
def modal(votes):
    c=collections.Counter(votes.values()); top,n=c.most_common(1)[0]
    return top if n>=2 else None
items={i:modal(v) for i,v in byitem.items()}
arm=lambda i: json.loads('{}') # placeholder
arms={json.loads(l)['id']:json.loads(l)['arm'] for l in open('t3_items.jsonl')}
# ---- STAGE 1: gate on D only ----
Drule=[i for i,a in arms.items() if a=='D-rule']; Dfact=[i for i,a in arms.items() if a=='D-fact']
def model_rate(ids): 
    m=[items[i] for i in ids if items[i] is not None]
    return sum(1 for x in m if x=='Model')/len(m) if m else 0.0, len(m)
r_rule,n_rule=model_rate(Drule); r_fact,n_fact=model_rate(Dfact)
R=r_rule-r_fact
# permutation p for control separation
pool=[(i,items[i]) for i in Drule+Dfact if items[i] is not None]
labels=[1]*sum(1 for i in Drule if items[i] is not None)+[0]*sum(1 for i in Dfact if items[i] is not None)
vals=[1 if k=='Model' else 0 for _,k in pool]
obs=R
cnt=0; B=10000
for _ in range(B):
    random.shuffle(labels)
    a=[v for v,l in zip(vals,labels) if l]; b=[v for v,l in zip(vals,labels) if not l]
    if abs(sum(a)/len(a)-sum(b)/len(b))>=abs(obs)-1e-12: cnt+=1
p_gate=cnt/B
# bootstrap R bounds
bs=[]
rl=[v for v,l in zip(vals,[1]*n_rule+[0]*n_fact) if l]; fl=[v for v,l in zip(vals,[1]*n_rule+[0]*n_fact) if not l]
rulevals=vals[:n_rule]; factvals=vals[n_rule:]
for _ in range(B):
    rr=[random.choice(rulevals) for _ in rulevals]; ff=[random.choice(factvals) for _ in factvals]
    bs.append(sum(rr)/len(rr)-sum(ff)/len(ff))
bs.sort(); R_lo=bs[int(0.025*B)]; R_hi=bs[int(0.975*B)]
gate={"R":round(R,4),"R_lo":round(R_lo,4),"R_hi":round(R_hi,4),"p_gate":p_gate,
      "n_rule_modal":n_rule,"n_fact_modal":n_fact,
      "rate_rule":round(r_rule,4),"rate_fact":round(r_fact,4)}
if R<0.30: gate["verdict"]="VOID-instrument-cannot-resolve"
elif p_gate>=0.01: gate["verdict"]="GATE-UNDERPOWERED"
else: gate["verdict"]="PASS"
json.dump(gate,open('t3_gate.json','w'),indent=1)
print("GATE:",json.dumps(gate))
if gate["verdict"]!="PASS": sys.exit(0)
# ---- STAGE 2: A vs B (only reached on PASS) ----
A=[i for i,a in arms.items() if a=='A']; Bm=[i for i,a in arms.items() if a=='B']
ra,na=model_rate(A); rb,nb=model_rate(Bm)
delta=abs(ra-rb)
avals=[1 if items[i]=='Model' else 0 for i in A if items[i] is not None]
bvals=[1 if items[i]=='Model' else 0 for i in Bm if items[i] is not None]
allv=avals+bvals; lab=[1]*len(avals)+[0]*len(bvals)
cnt=0
for _ in range(B):
    random.shuffle(lab)
    x=[v for v,l in zip(allv,lab) if l]; y=[v for v,l in zip(allv,lab) if not l]
    if abs(sum(x)/len(x)-sum(y)/len(y))>=delta-1e-12: cnt+=1
p_prim=cnt/B
# bootstrap upper bound on delta
bsd=[]
for _ in range(B):
    x=[random.choice(avals) for _ in avals]; y=[random.choice(bvals) for _ in bvals]
    bsd.append(abs(sum(x)/len(x)-sum(y)/len(y)))
bsd.sort(); d_hi=bsd[int(0.975*B)]
# modal coverage gate 2
cov=sum(1 for i in A+Bm if items[i] is not None)/len(A+Bm)
# leak destinations
leakA=collections.Counter(items[i] for i in A if items[i] not in (None,'Model'))
leakB=collections.Counter(items[i] for i in Bm if items[i] not in (None,'Model'))
res={"rate_A":round(ra,4),"rate_B":round(rb,4),"delta":round(delta,4),"p":p_prim,
     "delta_hi95":round(d_hi,4),"coverage":round(cov,4),
     "leak_A":dict(leakA),"leak_B":dict(leakB)}
if cov<0.70: res["band"]="VOID-gate2-coverage"
elif p_prim<0.01 and delta>=0.5*R_lo: res["band"]="SUBSTRUCTURE"
elif p_prim>=0.05 and d_hi<0.5*R_hi: res["band"]="ONE KIND"
elif p_prim>=0.05: res["band"]="UNDERPOWERED"
else: res["band"]="AMBIGUOUS"
json.dump(res,open('t3_primary.json','w'),indent=1)
print("PRIMARY:",json.dumps(res))
