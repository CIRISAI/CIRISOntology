import json, os, urllib.request
key = open(os.path.expanduser('~/.deepinfra_key')).read().strip()
brief = open('scorer_brief.txt').read()
req = urllib.request.Request(
    "https://api.deepinfra.com/v1/openai/chat/completions",
    data=json.dumps({"model":"deepseek-ai/DeepSeek-V3.1","messages":[{"role":"user","content":brief}],
                     "temperature":0.2,"max_tokens":8000}).encode(),
    headers={"Authorization": f"Bearer {key}","Content-Type":"application/json"})
r = json.load(urllib.request.urlopen(req, timeout=1200))
open('scorer_report.md','w').write("# Third-party scorer report — model deepseek-ai/DeepSeek-V3.1, temp 0.2, brief-only\n\n" + r["choices"][0]["message"]["content"])
print("scorer done:", r.get("usage",{}), flush=True)
