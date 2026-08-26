#!/usr/bin/env python3
"""Prompt variants for the DEPLOYED Q4_K_M artifact.

Tunes on TRAIN+DEV only. The 92-item test split is never read by this script --
enforced below by loading train_split.jsonl and nothing else.
Few-shot exemplars are drawn from a fixed 8-item TRAIN subset and those items are
excluded from scoring, so no variant is scored on its own examples.
"""
import json, os, sys, time, urllib.request, collections, random

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(f"{HERE}/surface_map.json")); K2B, SURF = M["kind2block"], M["surface_plain"]
LABELS = ["Facts", "Rules", "Identity", "Manner"]
SCHEMA = {"type":"object","properties":{"family":{"type":"string","enum":LABELS}},"required":["family"]}

BASE_FAM = [
 ("Facts","the assertive family: what is claimed, how strongly, under what rule, on what premise"),
 ("Rules","the directive family: what is required, in what preference order, in what step order"),
 ("Identity","the declarative family: what counts as what"),
 ("Manner","the force-neutral carrier family: how it is encoded, how it is presented or registered, which instance it is")]

# V4 glosses name the member kinds explicitly (from Surface.lean's block membership)
MEMBER_FAM = [
 ("Facts","ASSERTIVE - the change alters something CLAIMED to be true, how confident the claim is, which model/rule it was derived under, or what it assumes. Covers: Facts, Confidence, Model, Premises."),
 ("Rules","DIRECTIVE - the change alters what someone MUST or MAY do, which option takes precedence, or the ORDER OF STEPS to follow. Covers: Rules, Priorities, Process. Choose this whenever the change creates, removes or reorders an obligation, permission, priority or procedure."),
 ("Identity","DECLARATIVE - the change alters what something COUNTS AS: a definition, designation, classification or status conferred by saying so. Covers: Identity."),
 ("Manner","CARRIER - the change alters presentation or encoding rather than content: wording, format, register, labelling, or which particular instance is referenced. Covers: Structure, Manner, Circumstances.")]

def sysmsg(fams, extra=""):
    return ("You classify what FAMILY of change was made to a document. "
            "Answer with exactly one label from this list:\n"
            + "\n".join(f"- {n}: {g}" for n,g in fams)
            + "\nPick the single family the change belongs to." + extra)

RULES_HINT = ("\n\nIMPORTANT: a change is Rules whenever it changes what is REQUIRED, PERMITTED, "
              "FORBIDDEN, prioritised, or the order/sequence of steps - even if it also mentions "
              "facts or figures. Deadlines, thresholds, obligations, approvals, and procedural "
              "reordering are Rules, not Facts.")

def trunc(s,n=1400):
    s=s or ""; return s if len(s)<=n else s[:n]+"\n[...truncated]"
def user_msg(o):
    return (f"BEFORE:\n{trunc(o['before'])}\n\nAFTER:\n{trunc(o['after'])}\n\n"
            f"WHAT CHANGED: {o.get('variation_site','')}\n\nWhich family of change is this?")

def ask(model, msgs, retries=3):
    body=json.dumps({"model":model,"messages":msgs,"stream":False,"format":SCHEMA,
        "options":{"temperature":0,"num_predict":32,"num_ctx":8192},"think":False}).encode()
    for a in range(retries):
        try:
            req=urllib.request.Request("http://localhost:11434/api/chat",body,{"Content-Type":"application/json"})
            with urllib.request.urlopen(req,timeout=240) as r:
                return json.loads(json.loads(r.read())["message"]["content"])["family"]
        except Exception:
            if a==retries-1: return None
            time.sleep(2)

def variants(shots):
    def fewshot(items):
        m=[]
        for o in items:
            m.append({"role":"user","content":user_msg(o)})
            m.append({"role":"assistant","content":json.dumps({"family":SURF[K2B[o['kind_target']]]})})
        return m
    rules_shots=[o for o in shots if SURF[K2B[o['kind_target']]]=="Rules"]
    other=[o for o in shots if SURF[K2B[o['kind_target']]]!="Rules"]
    return {
     "V0_baseline":        (sysmsg(BASE_FAM), []),
     "V1_rules_hint":      (sysmsg(BASE_FAM, RULES_HINT), []),
     "V2_member_glosses":  (sysmsg(MEMBER_FAM), []),
     "V3_fewshot4":        (sysmsg(BASE_FAM), fewshot(shots[:4])),
     "V4_member+hint":     (sysmsg(MEMBER_FAM, RULES_HINT), []),
     "V5_member+fewshot":  (sysmsg(MEMBER_FAM), fewshot(shots[:4])),
     "V6_rulesheavy_shots":(sysmsg(MEMBER_FAM, RULES_HINT), fewshot(rules_shots[:2]+other[:2])),
    }

def main():
    model = sys.argv[1]
    only  = sys.argv[2] if len(sys.argv)>2 else None
    pool=[o for o in (json.loads(l) for l in open(f"{HERE}/train_split.jsonl")) if o["kind_target"] in K2B]
    rng=random.Random(7)
    by=collections.defaultdict(list)
    for o in pool: by[SURF[K2B[o['kind_target']]]].append(o)
    shots=[]
    for fam in ["Rules","Facts","Manner","Identity","Rules","Facts","Manner","Identity"]:
        g=[x for x in by[fam] if x not in shots]
        if g: shots.append(rng.choice(g))
    shot_ids={o["id"] for o in shots}
    # Reproduce finetune4.py's train/dev partition EXACTLY (same seed, same rule):
    # dev items were HELD OUT of training; train items were fitted to loss 0.004.
    ft_rng=random.Random(20260822); tr=[]; dv=[]
    byk=collections.defaultdict(list)
    for o in pool: byk[SURF[K2B[o["kind_target"]]]].append(o)
    for k in sorted(byk):
        g=sorted(byk[k],key=lambda x:x["id"]); ft_rng.shuffle(g)
        n_dev=max(1,round(len(g)*20/len(pool)))
        dv+=g[:n_dev]; tr+=g[n_dev:]
    dev_ids={o["id"] for o in dv}
    score_pool=[o for o in pool if o["id"] not in shot_ids]
    nclean=sum(1 for o in score_pool if o["id"] in dev_ids)
    print(f"tuning pool={len(score_pool)}; MEMORISED(train)={len(score_pool)-nclean} CLEAN(dev)={nclean}; TEST NEVER LOADED")
    V=variants(shots)
    out={}
    for name,(sm,fs) in V.items():
        if only and name!=only: continue
        rows=[]; t0=time.time()
        for o in score_pool:
            msgs=[{"role":"system","content":sm}]+fs+[{"role":"user","content":user_msg(o)}]
            rows.append({"id":o["id"],"gold":SURF[K2B[o['kind_target']]],"pred":ask(model,msgs)})
        for r in rows: r["clean"] = r["id"] in dev_ids
        acc=sum(r["pred"]==r["gold"] for r in rows)/len(rows)
        cl=[r for r in rows if r["clean"]]; mem=[r for r in rows if not r["clean"]]
        acc_clean=sum(r["pred"]==r["gold"] for r in cl)/max(1,len(cl))
        acc_mem=sum(r["pred"]==r["gold"] for r in mem)/max(1,len(mem))
        rc=[r for r in cl if r["gold"]=="Rules"]
        per=collections.defaultdict(lambda:[0,0])
        for r in rows: per[r["gold"]][0]+=(r["pred"]==r["gold"]); per[r["gold"]][1]+=1
        out[name]={"acc":acc,"acc_clean_dev":acc_clean,"n_clean":len(cl),
                   "acc_memorised_train":acc_mem,"rows":rows,
                   "rules_clean":[sum(r["pred"]==r["gold"] for r in rc),len(rc)],
                   "rules_recall":per["Rules"][0]/max(1,per["Rules"][1]),
                   "per_family":{k:[c,t] for k,(c,t) in per.items()},
                   "labels":dict(collections.Counter(r["pred"] for r in rows))}
        print(f"  {name:22s} pool={acc:.3f} | CLEAN(dev n={len(cl)})={acc_clean:.3f} | memorised={acc_mem:.3f}"
              f" | Rules_clean={sum(r['pred']==r['gold'] for r in rc)}/{len(rc)}"
              f" | Rules_all={per['Rules'][0]}/{per['Rules'][1]}  ({time.time()-t0:.0f}s)",flush=True)
        json.dump(out,open(f"{HERE}/prompt_tune_{model.replace(':','_')}.json","w"),indent=2)

if __name__=="__main__": main()
