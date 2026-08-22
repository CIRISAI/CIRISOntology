"""Continue S2/S3 for items the tightened gate no longer fast-exits, reusing recorded S1."""
import json,sys,threading
sys.path.insert(0,'/home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/H3ERE2_TUNING')
import h3ere2_v2 as h
from concurrent.futures import ThreadPoolExecutor
items={it['id']:it for it in (json.loads(l) for l in open('/home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/h3ere2_curated.jsonl'))}
src={(r['id'],r['model']):r for r in (json.loads(l) for l in open('FINAL_curated.jsonl'))}
todo=[tuple(x) for x in json.load(open('rerouted_ids.json'))]
out=open('FINAL_curated_reroute.jsonl','a'); lk=threading.Lock(); n=[0]
done=set()
try:
    for l in open('FINAL_curated_reroute.jsonl'):
        r=json.loads(l); done.add((r['id'],r['model']))
except Exception: pass
todo=[t for t in todo if t not in done]
def one(key):
    i,m=key; r=src[key]; it=items[i]; o1=r.get('s1') or {}
    tr={"id":i,"model":m,"s1":o1,"gate":"facts-never-fast"}
    o2=h.pjson(h.ask(m,h.s2_a5(it,o1),tag="rr-s2")); tr["s2"]=o2
    kind=str(o2.get("kind","")).strip()
    if kind not in h.ALL12:
        tr["final"]=r.get('final'); tr["route"]="s2-parsefail-fallback"
    else:
        o3=h.pjson(h.ask(m,h.s3_v1(it,o1,kind,str(o2.get("rationale",""))),tag="rr-s3")); tr["s3"]=o3
        if str(o3.get("verdict","")).upper()=="PASS":
            tr["final"]=kind; tr["route"]="recurse-pass"
        else:
            o2b=h.pjson(h.ask(m,h.s2_a5(it,o1,guidance=str(o3.get("guidance",""))),tag="rr-s2r")); tr["s2_retry"]=o2b
            k2=str(o2b.get("kind","")).strip()
            o3b=h.pjson(h.ask(m,h.s3_v1(it,o1,k2 if k2 in h.ALL12 else kind,str(o2b.get("rationale",""))),tag="rr-s3r")); tr["s3_retry"]=o3b
            ok=str(o3b.get("verdict","")).upper()=="PASS" and k2 in h.ALL12
            tr["final"]= k2 if ok else kind
            tr["route"]="recurse-retry-"+("pass" if ok else "rejected")
    with lk:
        out.write(json.dumps(tr,ensure_ascii=False)+"\n"); out.flush(); n[0]+=1
        if n[0]%10==0: print(n[0],flush=True)
with ThreadPoolExecutor(max_workers=8) as ex: list(ex.map(one,todo))
print("REROUTE-DONE",n[0],flush=True)
