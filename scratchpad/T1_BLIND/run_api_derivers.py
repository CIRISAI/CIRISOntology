import json, os, sys, urllib.request
key = open(os.path.expanduser('~/.deepinfra_key')).read().strip()
model = "deepseek-ai/DeepSeek-V3.1"
for i in (1,2,3):
    out = f"api_deriver{i}.md"
    if os.path.exists(out+'.done'): continue
    brief = open(f'api_brief_{i}.txt').read()
    req = urllib.request.Request(
        "https://api.deepinfra.com/v1/openai/chat/completions",
        data=json.dumps({"model": model, "messages":[{"role":"user","content":brief}],
                         "temperature":0.5, "max_tokens":8000}).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type":"application/json"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=900))
        text = r["choices"][0]["message"]["content"]
        usage = r.get("usage", {})
        open(out,'w').write(f"# api_deriver{i} — model {model}, temp 0.5, genuinely blind (brief-only)\n\n" + text)
        open(out+'.done','w').write(json.dumps(usage))
        print(f"deriver {i} done: {len(text)} chars, usage {usage}", flush=True)
    except Exception as e:
        print(f"deriver {i} FAILED: {e}", flush=True)
        sys.exit(1)
print("ALL-DONE", flush=True)
