import json, os, urllib.request
from items import ITEMS
key = open(os.path.expanduser('~/.deepinfra_key')).read().strip()
TMPL = """Write a concrete scenario of 2-4 sentences: a specific document, transcript, or record is changed, and the whole effect of the change is an instance of the following: {definition}. Describe only the artifact, the change, and its effect, in plain everyday language. Do not name any classification scheme, standard, dimension, or category. End with the sentence: 'The change described above is the whole difference between the two versions.'"""
out = {}
if os.path.exists('vignettes.json'): out = json.load(open('vignettes.json'))
for iid,(title,definition) in ITEMS.items():
    for v in (1,2):
        kk=f"{iid}#v{v}"
        if kk in out: continue
        req = urllib.request.Request("https://api.deepinfra.com/v1/openai/chat/completions",
            data=json.dumps({"model":"deepseek-ai/DeepSeek-V3.1",
                "messages":[{"role":"user","content":TMPL.format(definition=definition)}],
                "temperature":0.7,"max_tokens":400,"seed":20260821+v}).encode(),
            headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
        r = json.load(urllib.request.urlopen(req, timeout=300))
        out[kk]=r["choices"][0]["message"]["content"].strip()
        json.dump(out,open('vignettes.json','w'),indent=1)
        print(kk,"done",flush=True)
print("VIGNETTES-DONE",len(out),flush=True)
