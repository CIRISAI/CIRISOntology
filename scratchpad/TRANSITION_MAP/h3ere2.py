"""H3ERE2 pipeline runner — per H3ERE2X_PREREG.md (frozen). prereg_id H3ERE2X-20260822."""
import json, os, re, sys, time, urllib.request, threading
from concurrent.futures import ThreadPoolExecutor
KEY = open(os.path.expanduser('~/.deepinfra_key')).read().strip()
MODELS = ["deepseek-ai/DeepSeek-V3.1","Qwen/Qwen3-235B-A22B-Instruct-2507","zai-org/GLM-4.5"]
SURFACE = ["Facts","Rules","Manner","Identity"]
DEEP = ["Priorities","Confidence","Circumstances","Process","Model","Structure","Premises"]
ALL12 = SURFACE + DEEP + ["Record"]
VERBS = ["attest","authorize","replace","withdraw","recant","carries"]
DISC = {"Priorities":"What becomes more important?","Rules":"What becomes allowed or required?",
 "Manner":"How is the same thing presented or used?","Identity":"What is this said to be?",
 "Confidence":"How sure are we, and on what standard?","Facts":"What claimed fact becomes wrong?",
 "Circumstances":"What just happens to differ here?","Process":"What steps or ordering change?",
 "Model":"What rule or model are we reasoning under?","Structure":"How are the pieces put together?",
 "Premises":"What are we taking as given?","Record":"Can the event still be established from what survives?"}
BOUNDARY_PRIORS = """Measured boundary channels (deep kinds most often arrive wearing these surfaces):
- Premises changes arrive wearing Facts (a changed assumption shows up as a burst of changed facts)
- Model changes arrive wearing Facts (a changed applied rule shows up as changed derived values)
- Structure changes arrive wearing Manner (a changed assembly shows up as changed presentation)"""
def ask(model, prompt, max_tokens=2500):
    body = json.dumps({"model":model,"temperature":0.0,"max_tokens":max_tokens,
                       "messages":[{"role":"user","content":prompt}]}).encode()
    for att in range(4):
        try:
            req = urllib.request.Request("https://api.deepinfra.com/v1/openai/chat/completions",
                data=body, headers={"Authorization":f"Bearer {KEY}","Content-Type":"application/json"})
            with urllib.request.urlopen(req, timeout=240) as r:
                d = json.loads(r.read())
            return d["choices"][0]["message"].get("content") or ""
        except Exception as e:
            time.sleep(8*(att+1))
    return ""
def pjson(t):
    m = re.search(r'\{.*\}', t, re.S)
    if not m: return {}
    try: return json.loads(m.group(0))
    except Exception: return {}
def item_block(it):
    return f"BEFORE:\n---\n{it['before']}\n---\nAFTER:\n---\n{it['after']}\n---\nThe change is located here: {it['variation_site']}"
def s1(model, it):
    p = f"""You evaluate a change between two document versions. First decide whether it is one of the four SURFACE kinds, or something DEEPER.
SURFACE kinds: {'; '.join(f'{k}: {DISC[k]}' for k in SURFACE)}
If none of those four is clearly what changed, answer DEEPER.
Also name the grammar verb the change enacts: attest (adds a claim), authorize (grants/denies standing), replace (substitutes content), withdraw (removes a prior contribution), recant (declares a prior contribution wrong), carries (a change of one kind arriving dressed as another).
{item_block(it)}
Reply STRICT JSON: {{"surface": "<Facts|Rules|Manner|Identity|DEEPER>", "verb": "<one verb>", "confidence": <0.0-1.0>, "rationale": "<one sentence>"}}"""
    return pjson(ask(model,p))
def s2A(model, it, s1out, guidance=None):
    g = f"\nCONSCIENCE GUIDANCE from the prior attempt (address it): {guidance}\n" if guidance else ""
    p = f"""A first-pass evaluation of this change produced: {json.dumps(s1out)}
The surface reading may be a deeper kind ARRIVING DRESSED as a surface kind.
{BOUNDARY_PRIORS}
DEEP kinds: {'; '.join(f'{k}: {DISC[k]}' for k in DEEP)}  (plus Record: {DISC['Record']})
{g}{item_block(it)}
Decide the true kind: either CONFIRM the surface reading or name the deep kind (or Record) this change actually is, and the verb.
Reply STRICT JSON: {{"kind": "<one of the twelve>", "verb": "<one verb>", "rationale": "<one sentence>"}}"""
    return pjson(ask(model,p))
def s2B(model, it, s1out, guidance=None):
    g = f"\nCONSCIENCE GUIDANCE from the prior attempt (address it): {guidance}\n" if guidance else ""
    p = f"""A first-pass evaluation of this change produced: {json.dumps(s1out)}
Wild changes are often MIXTURES of kinds. Decompose this change into its kind components.
All twelve kinds: {'; '.join(f'{k}: {DISC[k]}' for k in ALL12)}
{BOUNDARY_PRIORS}
{g}{item_block(it)}
Reply STRICT JSON: {{"components": {{"<kind>": <weight>, ...}}, "verb": "<one verb>", "rationale": "<one sentence>"}} with weights summing to 1, largest first."""
    return pjson(ask(model,p))
def s3(model, it, surface, kind, rationale):
    p = f"""Conscience check. A deeper evaluation claims this change is really kind "{kind}" (question: {DISC.get(kind,'')}), presenting on the surface as "{surface}". Its rationale: {rationale}
{item_block(it)}
Would a {kind} change genuinely wear this surface appearance here? Reply STRICT JSON: {{"verdict": "<PASS|FAIL>", "guidance": "<one sentence if FAIL, else null>"}}"""
    return pjson(ask(model,p))
def run_item(model, it, pattern):
    trace = {"id":it["id"],"model":model,"pattern":pattern}
    o1 = s1(model,it); trace["s1"]=o1
    surf = str(o1.get("surface","")).strip()
    try: conf = float(o1.get("confidence",0))
    except Exception: conf = 0.0
    if surf in SURFACE and conf >= 0.7:
        trace["final"]=surf; trace["final_verb"]=o1.get("verb"); trace["route"]="fast"
        return trace
    s2f = s2A if pattern=="A" else s2B
    o2 = s2f(model,it,o1); trace["s2"]=o2
    if pattern=="A":
        kind = str(o2.get("kind","")).strip()
    else:
        comps = o2.get("components",{}) or {}
        kind = max(comps, key=lambda k: comps.get(k,0)) if comps else ""
    if kind not in ALL12:
        trace["final"]=None; trace["route"]="parse-fail"; return trace
    o3 = s3(model,it,surf if surf in SURFACE else "unclear",kind,str(o2.get("rationale",""))); trace["s3"]=o3
    if str(o3.get("verdict","")).upper()=="PASS":
        trace["final"]=kind; trace["final_verb"]=o2.get("verb"); trace["route"]="recurse-pass"
        return trace
    o2b = s2f(model,it,o1,guidance=str(o3.get("guidance",""))); trace["s2_retry"]=o2b
    if pattern=="A":
        kind2 = str(o2b.get("kind","")).strip()
    else:
        comps = o2b.get("components",{}) or {}
        kind2 = max(comps, key=lambda k: comps.get(k,0)) if comps else ""
    o3b = s3(model,it,surf if surf in SURFACE else "unclear",kind2 if kind2 in ALL12 else kind, str(o2b.get("rationale","")))
    trace["s3_retry"]=o3b
    final = kind2 if kind2 in ALL12 else kind
    trace["final"]=final; trace["final_verb"]=o2b.get("verb") or o2.get("verb")
    trace["route"]="recurse-retry-"+("pass" if str(o3b.get("verdict","")).upper()=="PASS" else "unverified")
    return trace
def main(dataset, pattern, outpath):
    items = [json.loads(l) for l in open(dataset)]
    done=set()
    if os.path.exists(outpath):
        for l in open(outpath):
            try: r=json.loads(l); done.add((r["id"],r["model"]))
            except Exception: pass
    todo=[(it,m) for it in items for m in MODELS if (it["id"],m) not in done]
    lock=threading.Lock(); fh=open(outpath,"a"); n=[0]
    def one(job):
        it,m=job
        tr=run_item(m,it,pattern)
        with lock:
            fh.write(json.dumps(tr,ensure_ascii=False)+"\n"); fh.flush(); n[0]+=1
            if n[0]%50==0: print(f"{n[0]}/{len(todo)}",flush=True)
    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(one,todo))
    print(f"H3ERE2-{pattern}-DONE {dataset} {n[0]}",flush=True)
if __name__=="__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
