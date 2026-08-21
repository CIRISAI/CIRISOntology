import json, os, urllib.request, time
key = open(os.path.expanduser('~/.deepinfra_key')).read().strip()
MODELS = ["meta-llama/Llama-4-Scout-17B-16E-Instruct","openai/gpt-oss-120b","google/gemma-3-27b-it"]
PLAIN = {"axiotic":"Priorities","deontic":"Rules","pragmatic":"Manner","ontological":"Identity",
 "epistemic":"Confidence","empirical":"Facts","contingent":"Circumstances","procedural":"Process",
 "nomological":"Model","structural":"Structure","axiomatic":"Premises","testimonial":"Record"}
DISC = {"axiotic":"What becomes more important?","deontic":"What becomes allowed or required?",
 "pragmatic":"How is the same thing presented or used?","ontological":"What is this said to be?",
 "epistemic":"How sure are we, and on what standard?","empirical":"What claimed fact becomes wrong?",
 "contingent":"What just happens to differ here?","procedural":"What steps or ordering change?",
 "nomological":"What rule or model are we reasoning under?","structural":"How are the pieces put together?",
 "axiomatic":"What are we taking as given?","testimonial":"Can the event still be established from what survives?"}
BOUNDARY = """Two boundaries that matter:
- Confidence vs Facts: the proposition may stay identical while the warranted confidence changes; conversely, confidence may stay identical while the proposition itself becomes false.
- Model vs Facts: Model means the framework APPLIED to derive an answer. A model ASSERTED to be descriptively true of the world is itself a Fact."""
vocab = "\n".join(f"- {PLAIN[k]}: {DISC[k]}" for k in PLAIN)
opsdoc = open('alignment_ops_extract.txt').read()
OPS = ["scores","delegates_to","supersedes","withdraws","recants"]
TMPL = """You classify operations from a signed-attestation grammar against a fixed vocabulary of twelve kinds of change (plus NO-FIT).

THE TWELVE KINDS:
{vocab}

{boundary}

THE GRAMMAR'S OPERATIONS, with their specification-sourced pre/postconditions:
{opsdoc}

THE QUESTION, for the operation "{op}" ONLY:
(a) Performing an act of "{op}" changes the state of the world of records. Considered as a change, an act of "{op}" is a change of WHICH KIND (one of the twelve, or NO-FIT)?
(b) Per its PRECONDITIONS as specified, which kinds of change can an act of "{op}" lawfully FOLLOW — that is, for which kinds K could a change of kind K put the world into a state that satisfies "{op}"'s preconditions where they were not satisfied before? List every kind that applies (possibly empty, possibly many).

Reply with STRICT JSON only:
{{"kind": "<one kind or NO-FIT>", "follows": ["<kind>", ...], "reason": "<two sentences at most>"}}"""
results={}
if os.path.exists('alignment_raw.json'): results=json.load(open('alignment_raw.json'))
for op in OPS:
    for m in MODELS:
        kk=f"{op}|{m}"
        if kk in results: continue
        p=TMPL.format(vocab=vocab,boundary=BOUNDARY,opsdoc=opsdoc,op=op)
        req=urllib.request.Request("https://api.deepinfra.com/v1/openai/chat/completions",
            data=json.dumps({"model":m,"messages":[{"role":"user","content":p}],
                             "temperature":0,"max_tokens":2500}).encode(),
            headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
        for a in range(3):
            try:
                r=json.load(urllib.request.urlopen(req,timeout=300))
                results[kk]={"text":r["choices"][0]["message"]["content"]}; break
            except Exception as e:
                print(kk,"retry",a,e,flush=True); time.sleep(5)
        json.dump(results,open('alignment_raw.json','w'),indent=1)
        print(kk,"done",flush=True)
print("ALIGNMENT-DONE",len(results),flush=True)
