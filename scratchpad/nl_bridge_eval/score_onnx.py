#!/usr/bin/env python3
"""Score an ONNX build on the frozen 92 with the SAME constrained-greedy trie
walk as the torch arm, and record the decision-point logprob vector."""
import json, sys, os, time
import numpy as np, onnxruntime as ort
from transformers import AutoTokenizer

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(f"{HERE}/surface_map.json")); K2B, SURF = M["kind2block"], M["surface_plain"]
LABELS = ["Facts", "Rules", "Identity", "Manner"]
FAM = [("Facts","the assertive family: what is claimed, how strongly, under what rule, on what premise"),
       ("Rules","the directive family: what is required, in what preference order, in what step order"),
       ("Identity","the declarative family: what counts as what"),
       ("Manner","the force-neutral carrier family: how it is encoded, how it is presented or registered, which instance it is")]
SYS = ("You classify what FAMILY of change was made to a document. "
       "Answer with exactly one label from this list:\n"
       + "\n".join(f"- {n}: {g}" for n,g in FAM) + "\nPick the single family the change belongs to.")
JSON_OPEN = '{"family":'

def trunc(s,n=1400):
    s=s or ""; return s if len(s)<=n else s[:n]+"\n[...truncated]"
def user_msg(o):
    return (f"BEFORE:\n{trunc(o['before'])}\n\nAFTER:\n{trunc(o['after'])}\n\n"
            f"WHAT CHANGED: {o.get('variation_site','')}\n\nWhich family of change is this?")

def run(sess, ids):
    n=len(ids); a=np.array([ids],dtype=np.int64)
    out=sess.run(["logits"],{"input_ids":a,
        "attention_mask":np.ones((1,n),dtype=np.int64),
        "position_ids":np.arange(n,dtype=np.int64)[None,:]})[0]
    return out[0,-1].astype(np.float64)

def logsoftmax(x):
    x=x-x.max(); return x-np.log(np.exp(x).sum())

def main(model_path, tag):
    tok=AutoTokenizer.from_pretrained(f"{HERE}/ft_merged")
    so=ort.SessionOptions(); so.log_severity_level=3
    t0=time.time(); sess=ort.InferenceSession(model_path,so,providers=["CPUExecutionProvider"])
    print(f"  loaded in {time.time()-t0:.1f}s")
    items=[o for o in (json.loads(l) for l in open(f"{HERE}/test_split.jsonl")) if o["kind_target"] in K2B]
    opts={l:tok(f' "{l}"',add_special_tokens=False).input_ids for l in LABELS}
    rows=[]; t0=time.time()
    for i,o in enumerate(items,1):
        msgs=[{"role":"system","content":SYS},{"role":"user","content":user_msg(o)}]
        text=tok.apply_chat_template(msgs,tokenize=False,add_generation_prompt=True,
                                     enable_thinking=False)+JSON_OPEN
        cur=tok(text).input_ids
        alive=list(LABELS); step=0; dec=None
        while len(alive)>1 and step<12:
            nxt={}
            for l in alive:
                if step<len(opts[l]): nxt.setdefault(opts[l][step],[]).append(l)
            if len(nxt)<=1:
                alive=next(iter(nxt.values())) if nxt else alive; step+=1
                if nxt: cur=cur+[list(nxt.keys())[0]]
                continue
            lp=logsoftmax(run(sess,cur))
            if dec is None:  # record the decision-point vector over the live options
                dec={l:float(lp[opts[l][step]]) for l in alive}
            tk=max(nxt,key=lambda t: lp[t]); alive=nxt[tk]; cur=cur+[tk]; step+=1
        rows.append({"id":o["id"],"gold":SURF[K2B[o["kind_target"]]],"pred":alive[0],"decision_logprobs":dec})
        if i%25==0: print(f"  {i}/{len(items)} {time.time()-t0:.0f}s",flush=True)
    with open(f"{HERE}/pred4_{tag}.jsonl","w") as f:
        for r in rows: f.write(json.dumps(r)+"\n")
    acc=sum(r["pred"]==r["gold"] for r in rows)/len(rows)
    print(f"ARM {tag}: 4way={acc:.3f} ({round(acc*len(rows))}/{len(rows)})")

if __name__=="__main__": main(sys.argv[1],sys.argv[2])
