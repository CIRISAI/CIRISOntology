"""Exact, cheap v2.1 curated verification.

v2.1 differs from v2 by ONE clause inside stage 2. Items that fast-exit never reach stage 2 and
are therefore bit-identical. For routed items, re-run stage 2 ONLY (reusing v2's recorded stage-1
output verbatim, so the comparison is apples-to-apples), then run stage 3 + retry ONLY where a7's
answer differs from a5's — where they agree the whole downstream trace is identical by construction.
"""
import json,sys,threading
sys.path.insert(0,'/home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/H3ERE2_TUNING')
import importlib.util
spec=importlib.util.spec_from_file_location("v21","/home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/H3ERE2_TUNING/h3ere2_v2_1.py")
h=importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
from concurrent.futures import ThreadPoolExecutor
D='/home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/'
items={json.loads(l)['id']:json.loads(l) for l in open(D+'h3ere2_curated.jsonl')}
# the frozen v2 candidate = FINAL_curated with the reroute splice on top
base={}
for l in open('FINAL_curated.jsonl'):
    r=json.loads(l); base[(r['id'],r['model'])]=r
for l in open('FINAL_curated_reroute.jsonl'):
    r=json.loads(l); base[(r['id'],r['model'])]=r
routed=[k for k,r in base.items() if r.get('route')!='fast' and (r.get('s1') or {})]
print(f"routed items to probe: {len(routed)} of {len(base)} ({len(base)-len(routed)} fast-exit, unaffected)",flush=True)
out=open('V21_cur_probe.jsonl','a'); lk=threading.Lock(); n=[0]
done=set()
try:
    for l in open('V21_cur_probe.jsonl'):
        r=json.loads(l); done.add((r['id'],r['model']))
except Exception: pass
todo=[k for k in routed if k not in done]
def one(k):
    i,m=k; r=base[k]; it=items[i]; o1=r['s1']
    o2=h.pjson(h.ask(m, h.s2_a7(it,o1), tag="v21-s2"))
    rec={"id":i,"model":m,"s2_a7":o2,"s2_a5":(r.get('s2') or {}).get('kind'),
         "v2_final":r.get('final'),"v2_route":r.get('route')}
    with lk:
        out.write(json.dumps(rec,ensure_ascii=False)+"\n"); out.flush(); n[0]+=1
        if n[0]%50==0: print(f"{n[0]}/{len(todo)}",flush=True)
with ThreadPoolExecutor(max_workers=6) as ex: list(ex.map(one,todo))
print("V21CURPROBE-DONE",n[0],flush=True)
