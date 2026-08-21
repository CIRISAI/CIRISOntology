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
TMPL = """You classify kinds of change using a fixed vocabulary of twelve kinds (plus NO-FIT).

THE TWELVE KINDS (name: the question that identifies it):
{vocab}

{boundary}

THE SCENARIO (it describes a change to an artifact):
{vignette}

THE QUESTION: The scenario above describes a change to an artifact. That change is a change of which kind?

Reply with STRICT JSON only, no other text:
{{"kind": "<one of the twelve kind names above, or NO-FIT>",
 "second": "<optional second choice, or null>",
 "reason": "<one sentence>",
 "survives_outside": "<yes or no - Does deciding this require knowing what survives OUTSIDE the artifact being classified?>"}}"""
vignettes = json.load(open('vignettes.json'))
results = {}
if os.path.exists('t2_raw_run3.json'): results = json.load(open('t2_raw_run3.json'))
for vk, vtext in vignettes.items():
    for m in MODELS:
        kk = f"{vk}|{m}"
        if kk in results: continue
        prompt = TMPL.format(vocab=vocab, boundary=BOUNDARY, vignette=vtext)
        req = urllib.request.Request("https://api.deepinfra.com/v1/openai/chat/completions",
            data=json.dumps({"model":m,"messages":[{"role":"user","content":prompt}],
                             "temperature":0,"max_tokens":2500}).encode(),
            headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
        for attempt in range(3):
            try:
                r = json.load(urllib.request.urlopen(req, timeout=300))
                results[kk] = {"text": r["choices"][0]["message"]["content"],
                               "cost": r.get("usage",{}).get("estimated_cost")}
                break
            except Exception as e:
                print(f"{kk} attempt {attempt}: {e}", flush=True); time.sleep(5)
        json.dump(results, open('t2_raw_run3.json','w'), indent=1)
        print(f"{kk} done", flush=True)
print("T2-RUN3-DONE", len(results), flush=True)
