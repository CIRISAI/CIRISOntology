import json, os, sys, time, urllib.request, threading
from concurrent.futures import ThreadPoolExecutor
import importlib.util
spec = importlib.util.spec_from_file_location("pa", "/home/emoore/CIRISOntology/scratchpad/plane_annotate.py")
pa = importlib.util.module_from_spec(spec); spec.loader.exec_module(pa)
key = open(os.path.expanduser('~/.deepinfra_key')).read().strip()
items = {json.loads(l)['id']: json.loads(l) for l in open('/home/emoore/CIRISOntology/scratchpad/plane_corpus/corpus_full.jsonl')}
recs = [json.loads(l) for l in open('panel2_validation.jsonl')]
keep = [r for r in recs if not (r['model'].startswith('zai') and r['kind'] is None)]
fails = [r for r in recs if r['model'].startswith('zai') and r['kind'] is None]
print("fixing", len(fails), flush=True)
fixed=[]; lock=threading.Lock()
def one(r):
    it = items[r['id']]
    prompt = pa.prompt_for(it, 'BASE')
    body = json.dumps({"model":"zai-org/GLM-4.5","temperature":0.0,"max_tokens":2500,
                       "messages":[{"role":"user","content":prompt}]}).encode()
    for att in range(4):
        try:
            req = urllib.request.Request("https://api.deepinfra.com/v1/openai/chat/completions",
                data=body, headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
            with urllib.request.urlopen(req, timeout=240) as resp:
                d = json.loads(resp.read())
            txt = d["choices"][0]["message"].get("content") or ""
            rec = dict(r); rec['raw'] = txt
            try:
                j = json.loads(txt[txt.index("{"): txt.rindex("}")+1])
                rec['kind']=j.get('kind'); rec['second']=j.get('second'); rec['reason']=j.get('reason')
            except Exception:
                rec['kind']=None
            with lock:
                fixed.append(rec)
                if len(fixed)%25==0: print(f"{len(fixed)}/{len(fails)}", flush=True)
            return
        except Exception as e:
            time.sleep(8*(att+1))
    with lock: fixed.append(dict(r))
with ThreadPoolExecutor(max_workers=8) as ex:
    list(ex.map(one, fails))
out = keep + fixed
open('panel2_validation.jsonl','w').write("\n".join(json.dumps(x) for x in out)+"\n")
nf=sum(1 for x in fixed if x['kind'] is None)
print("GLMFIX-DONE total", len(out), "residual", nf, flush=True)
