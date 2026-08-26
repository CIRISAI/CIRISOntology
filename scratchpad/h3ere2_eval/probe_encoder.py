import json, os, sys
sys.argv=[sys.argv[0]]
import numpy as np, onnxruntime as ort
from transformers import AutoTokenizer
NL=os.path.expanduser("~/CIRISOntology/scratchpad/nl_bridge_eval")
exec(open(os.path.expanduser("~/CIRISOntology/scratchpad/h3ere2_eval/encode_wild.py")).read().split("def main")[0].replace("import json, sys, os, time","import time"))
tok=AutoTokenizer.from_pretrained(f"{NL}/ft_merged")
so=ort.SessionOptions(); so.log_severity_level=3
sess=ort.InferenceSession(f"{NL}/onnx_q4f16/model_q4f16.onnx",so,providers=["CPUExecutionProvider"])
CASES=[
 ("clear Rules","Contractors may access the database.","Contractors are now FORBIDDEN from accessing the production database. Two approvals are required.","the access policy"),
 ("clear Identity","The service is called Aurora.","The service formerly called Aurora is now named Beacon; ownership moves to Payments.","the name and owner"),
 ("clear Manner","Errors are shown in Title Case.","Errors are now shown in sentence case, and timestamps use ISO-8601 instead of epoch.","the presentation style"),
 ("clear Facts","Throughput was 1.2M rps.","Measured throughput fell to 900K rps in the latest benchmark.","the measured value"),
]
opts={l:tok(f' "{l}"',add_special_tokens=False).input_ids for l in LABELS}
for name,b,a,v in CASES:
    o={"before":b,"after":a,"variation_site":v}
    msgs=[{"role":"system","content":SYS},{"role":"user","content":user_msg(o)}]
    text=tok.apply_chat_template(msgs,tokenize=False,add_generation_prompt=True,enable_thinking=False)+JSON_OPEN
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
        if dec is None: dec={l:round(float(lp[opts[l][step]]),2) for l in alive}
        tk=max(nxt,key=lambda t: lp[t]); alive=nxt[tk]; cur=cur+[tk]; step+=1
    print(f"  {name:<15} -> {alive[0]:<9} {dec}")
