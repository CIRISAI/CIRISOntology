"""Complete the 13 traces where a7 diverged from a5: run S3 (+guided retry) exactly as the
pipeline would, so v2.1's end-to-end curated numbers are exact rather than bounded."""
import json,sys,threading
sys.path.insert(0,'/home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/H3ERE2_TUNING')
import importlib.util
spec=importlib.util.spec_from_file_location("v21","/home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/H3ERE2_TUNING/h3ere2_v2_1.py")
h=importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
from concurrent.futures import ThreadPoolExecutor
D='/home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/'
items={json.loads(l)['id']:json.loads(l) for l in open(D+'h3ere2_curated.jsonl')}
probe={(r['id'],r['model']):r for r in (json.loads(l) for l in open('V21_cur_probe.jsonl'))}
want=[tuple(x) for x in json.load(open('v21_diff_ids.json'))]
out=open('V21_cur_finish.jsonl','a'); lk=threading.Lock()
done=set()
try:
    for l in open('V21_cur_finish.jsonl'):
        r=json.loads(l); done.add((r['id'],r['model']))
except Exception: pass
want=[k for k in want if k not in done]
def one(k):
    i,m=k; pr=probe[k]; it=items[i]; o1=pr['s1'] if 's1' in pr else None
    if o1 is None:
        # recover the recorded S1 from the frozen v2 traces
        for l in open('FINAL_curated.jsonl'):
            r=json.loads(l)
            if (r['id'],r['model'])==k: o1=r.get('s1'); break
    o2=pr['s2_a7']; kind=str((o2 or {}).get('kind','')).strip()
    o3=h.pjson(h.ask(m,h.s3_v1(it,o1,kind,str((o2 or {}).get('rationale',''))),tag="v21-s3"))
    rec={"id":i,"model":m,"s3":o3}
    if str(o3.get("verdict","")).upper()=="PASS":
        rec["final"]=kind; rec["route"]="recurse-pass"
    else:
        o2b=h.pjson(h.ask(m,h.s2_a7(it,o1,guidance=str(o3.get("guidance",""))),tag="v21-s2r"))
        k2=str(o2b.get("kind","")).strip()
        o3b=h.pjson(h.ask(m,h.s3_v1(it,o1,k2 if k2 in h.ALL12 else kind,str(o2b.get("rationale",""))),tag="v21-s3r"))
        ok=str(o3b.get("verdict","")).upper()=="PASS" and k2 in h.ALL12
        rec["final"]= k2 if ok else kind
        rec["route"]="recurse-retry-"+("pass" if ok else "rejected")
    with lk:
        out.write(json.dumps(rec,ensure_ascii=False)+"\n"); out.flush()
with ThreadPoolExecutor(max_workers=6) as ex: list(ex.map(one,want))
print("V21FINISH-DONE",len(want),flush=True)
