#!/usr/bin/env python3
"""SINGLE frozen-test re-gate of the selected deployment prompt (V1_rules_hint)."""
import json, sys, os, collections, urllib.request, time
HERE=os.path.dirname(os.path.abspath(__file__))
M=json.load(open(f"{HERE}/surface_map.json")); K2B,SURF=M["kind2block"],M["surface_plain"]
LABELS=["Facts","Rules","Identity","Manner"]
SCHEMA={"type":"object","properties":{"family":{"type":"string","enum":LABELS}},"required":["family"]}
FAM=[("Facts","the assertive family: what is claimed, how strongly, under what rule, on what premise"),
     ("Rules","the directive family: what is required, in what preference order, in what step order"),
     ("Identity","the declarative family: what counts as what"),
     ("Manner","the force-neutral carrier family: how it is encoded, how it is presented or registered, which instance it is")]
RULES_HINT=("\n\nIMPORTANT: a change is Rules whenever it changes what is REQUIRED, PERMITTED, "
            "FORBIDDEN, prioritised, or the order/sequence of steps - even if it also mentions "
            "facts or figures. Deadlines, thresholds, obligations, approvals, and procedural "
            "reordering are Rules, not Facts.")
def sysmsg(hint):
    return ("You classify what FAMILY of change was made to a document. "
            "Answer with exactly one label from this list:\n"
            + "\n".join(f"- {n}: {g}" for n,g in FAM)
            + "\nPick the single family the change belongs to." + (RULES_HINT if hint else ""))
def trunc(s,n=1400):
    s=s or ""; return s if len(s)<=n else s[:n]+"\n[...truncated]"
def um(o): return (f"BEFORE:\n{trunc(o['before'])}\n\nAFTER:\n{trunc(o['after'])}\n\n"
                   f"WHAT CHANGED: {o.get('variation_site','')}\n\nWhich family of change is this?")
def ask(model,msgs):
    body=json.dumps({"model":model,"messages":msgs,"stream":False,"format":SCHEMA,
        "options":{"temperature":0,"num_predict":32,"num_ctx":8192},"think":False}).encode()
    for a in range(3):
        try:
            req=urllib.request.Request("http://localhost:11434/api/chat",body,{"Content-Type":"application/json"})
            with urllib.request.urlopen(req,timeout=240) as r:
                return json.loads(json.loads(r.read())["message"]["content"])["family"]
        except Exception:
            if a==2: return None
            time.sleep(2)
def run(model,hint,tag):
    items=[o for o in (json.loads(l) for l in open(f"{HERE}/test_split.jsonl")) if o["kind_target"] in K2B]
    sm=sysmsg(hint); rows=[]
    for o in items:
        rows.append({"id":o["id"],"gold":SURF[K2B[o["kind_target"]]],
                     "pred":ask(model,[{"role":"system","content":sm},{"role":"user","content":um(o)}])})
    with open(f"{HERE}/pred4_test_{tag}.jsonl","w") as f:
        for r in rows: f.write(json.dumps(r)+"\n")
    acc=sum(r["pred"]==r["gold"] for r in rows)/len(rows)
    per=collections.defaultdict(lambda:[0,0])
    for r in rows: per[r["gold"]][0]+=(r["pred"]==r["gold"]); per[r["gold"]][1]+=1
    print(f"{tag}: acc={acc:.3f} ({round(acc*len(rows))}/{len(rows)})  " +
          "  ".join(f"{k}={c}/{t}" for k,(c,t) in sorted(per.items())))
    return rows,acc
if __name__=="__main__":
    m=sys.argv[1]
    run(m,False,f"{m}_V0"); run(m,True,f"{m}_V1")
