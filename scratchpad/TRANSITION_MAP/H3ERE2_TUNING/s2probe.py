"""Stage-2-alone probe: re-run S2 on chosen items using ALREADY-RECORDED S1 outputs."""
import json,sys,threading
sys.path.insert(0,'/home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/H3ERE2_TUNING')
import h3ere2_v2 as h
from concurrent.futures import ThreadPoolExecutor
dataset, tracefile, idfile, var, out = sys.argv[1:6]
items={json.loads(l)['id']:json.loads(l) for l in open(dataset)}
want=set(json.load(open(idfile)))
seen=set(); jobs=[]
for l in open(tracefile):
    r=json.loads(l)
    if r['id'] in want and (r['id'],r['model']) not in seen and (r.get('s1') or {}):
        seen.add((r['id'],r['model'])); jobs.append(r)
done=set()
try:
    for l in open(out):
        r=json.loads(l); done.add((r['id'],r['model']))
except Exception: pass
jobs=[j for j in jobs if (j['id'],j['model']) not in done]
fn=h.S2S[var]
fh=open(out,'a'); lk=threading.Lock(); n=[0]
def one(r):
    o2=h.pjson(h.ask(r['model'], fn(items[r['id']], r['s1']), tag="probe-"+var))
    with lk:
        fh.write(json.dumps({"id":r['id'],"model":r['model'],"s2":o2},ensure_ascii=False)+"\n"); fh.flush()
        n[0]+=1
with ThreadPoolExecutor(max_workers=8) as ex: list(ex.map(one,jobs))
print("PROBE-DONE",var,n[0],flush=True)
