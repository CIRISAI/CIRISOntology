#!/usr/bin/env python3
"""A2 viability check: is the 4-way softmax actually soft, or effectively one-hot?

If most items are near one-hot, soft seeding collapses back to hard encoding and the
bottleneck is the classifier's CONFIDENCE, not the encoder->engine interface.
Computes the full 4-way distribution (not just the decision-point pair) on the wild items.
"""
import json, os, sys, time, collections, math
import numpy as np, onnxruntime as ort
from transformers import AutoTokenizer
HERE = os.path.dirname(os.path.abspath(__file__))
NL = os.path.expanduser("~/CIRISOntology/scratchpad/nl_bridge_eval")
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
def um(o): return (f"BEFORE:\n{trunc(o['before'])}\n\nAFTER:\n{trunc(o['after'])}\n\n"
                   f"WHAT CHANGED: {o.get('variation_site','')}\n\nWhich family of change is this?")
def main(model_path, corpus):
    tok=AutoTokenizer.from_pretrained(f"{NL}/ft_merged")
    so=ort.SessionOptions(); so.log_severity_level=3
    s=ort.InferenceSession(model_path,so,providers=["CPUExecutionProvider"])
    opts={l:tok(f' "{l}"',add_special_tokens=False).input_ids for l in LABELS}
    items=[json.loads(l) for l in open(corpus)]
    out=[]; t0=time.time()
    for i,o in enumerate(items,1):
        msgs=[{"role":"system","content":SYS},{"role":"user","content":um(o)}]
        pre=tok(tok.apply_chat_template(msgs,tokenize=False,add_generation_prompt=True,
                enable_thinking=False)+JSON_OPEN).input_ids
        tot={}
        for l,lid in opts.items():
            ids=pre+lid; n=len(ids)
            lg=s.run(["logits"],{"input_ids":np.array([ids],dtype=np.int64),
                "attention_mask":np.ones((1,n),dtype=np.int64),
                "position_ids":np.arange(n,dtype=np.int64)[None,:]})[0][0]
            lp=0.0
            for k,t in enumerate(lid):
                row=lg[len(pre)-1+k].astype(np.float64)
                row=row-row.max(); lp+=float(row[t]-np.log(np.exp(row).sum()))
            tot[l]=lp
        v=np.array([tot[l] for l in LABELS]); v=v-v.max()
        p=np.exp(v); p=p/p.sum()
        H=float(-(p*np.log(p+1e-300)).sum())
        out.append({"id":o["id"],"stream":o.get("stream"),"probs":{l:float(x) for l,x in zip(LABELS,p)},
                    "entropy":H,"pmax":float(p.max()),"argmax":LABELS[int(p.argmax())]})
        if i%25==0: print(f"  {i}/{len(items)} {time.time()-t0:.0f}s",flush=True)
    json.dump(out,open(f"{HERE}/softmax_entropy.json","w"),indent=2)
    pm=np.array([r["pmax"] for r in out]); H=np.array([r["entropy"] for r in out])
    print(f"\nN={len(out)}   max entropy possible = ln4 = {math.log(4):.3f}")
    print(f"  entropy   mean={H.mean():.3f} median={np.median(H):.3f} min={H.min():.3f} max={H.max():.3f}")
    print(f"  p(max)    mean={pm.mean():.3f} median={np.median(pm):.3f}")
    for thr in (0.99,0.95,0.90,0.80):
        print(f"  items with p(max) >= {thr}: {int((pm>=thr).sum()):3d}/{len(out)} = {(pm>=thr).mean():.1%}")
    print(f"  items with entropy < 0.10 (effectively one-hot): {(H<0.10).sum()}/{len(out)} = {(H<0.10).mean():.1%}")
    print(f"  argmax spread:", dict(collections.Counter(r["argmax"] for r in out)))
if __name__=="__main__": main(sys.argv[1],sys.argv[2])
