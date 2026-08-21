import json, os, urllib.request, time
key = open(os.path.expanduser('~/.deepinfra_key')).read().strip()
MODELS = ["meta-llama/Llama-4-Scout-17B-16E-Instruct","openai/gpt-oss-120b","google/gemma-3-27b-it"]
PLAIN = {"axiotic":"Priorities","deontic":"Rules","pragmatic":"Manner","ontological":"Identity",
 "epistemic":"Confidence","empirical":"Facts","contingent":"Circumstances","procedural":"Process",
 "nomological":"Model","structural":"Structure","axiomatic":"Premises","testimonial":"Record"}
DISC = {
 "axiotic":"What becomes more important?","deontic":"What becomes allowed or required?",
 "pragmatic":"How is the same thing presented or used?","ontological":"What is this said to be?",
 "epistemic":"How sure are we, and on what standard?","empirical":"What claimed fact becomes wrong?",
 "contingent":"What just happens to differ here?","procedural":"What steps or ordering change?",
 "nomological":"What rule or model are we reasoning under?","structural":"How are the pieces put together?",
 "axiomatic":"What are we taking as given?","testimonial":"Can the event still be established from what survives?"}
BOUNDARY = """Two boundaries that matter:
- Confidence vs Facts: the proposition may stay identical while the warranted confidence changes; conversely, confidence may stay identical while the proposition itself becomes false.
- Model vs Facts: Model means the framework APPLIED to derive an answer. A model ASSERTED to be descriptively true of the world is itself a Fact."""
vocab = "\n".join(f"- {PLAIN[k]}: {DISC[k]}" for k in PLAIN)
TMPL = """You classify a change between two versions of a short document. Twelve kinds of change exist; pick the ONE whose question best captures what this change alters. "NO FIT" is allowed if none apply.

THE TWELVE KINDS:
{vocab}

{boundary}

Background on the marking involved (context only):
{preamble}

BEFORE:
---
{before}
---
AFTER:
---
{after}
---
The change is located here: {site}

Reply with STRICT JSON only:
{{"kind": "<one of the twelve kind names or NO FIT>",
 "second": "<kind or null>",
 "reason": "<one sentence>",
 "survives_outside": "<yes or no - Does deciding this require knowing what survives OUTSIDE the artifact being classified?>"}}"""
def ask(model, prompt):
    req = urllib.request.Request("https://api.deepinfra.com/v1/openai/chat/completions",
        data=json.dumps({"model":model,"messages":[{"role":"user","content":prompt}],
                         "temperature":0,"max_tokens":2500}).encode(),
        headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    return r["choices"][0]["message"]["content"]
results = {}
if os.path.exists('t5_raw.json'): results=json.load(open('t5_raw.json'))
tasks=[]
for l in open('t5_items.jsonl'):
    it=json.loads(l)
    for g in ('N','T'):
        tasks.append((f"{it['id']}|G{g}", it[f'gloss{g}_before'], it[f'gloss{g}_after'], it))
for l in open('t5_tagnull.jsonl'):
    it=json.loads(l)
    tasks.append((f"{it['id']}|TN", it['before'], it['after'], it))
for tid, b, a, it in tasks:
    for m in MODELS:
        kk=f"{tid}|{m}"
        if kk in results: continue
        p=TMPL.format(vocab=vocab,boundary=BOUNDARY,preamble=it['category_preamble'],
                      before=b,after=a,site=it['variation_site'])
        for att in range(3):
            try:
                results[kk]={"text":ask(m,p)}; break
            except Exception as e:
                print(kk,"retry",att,e,flush=True); time.sleep(5)
        json.dump(results,open('t5_raw.json','w'),indent=1)
        print(kk,"done",flush=True)
print("T5-MAPPING-DONE",len(results),flush=True)
