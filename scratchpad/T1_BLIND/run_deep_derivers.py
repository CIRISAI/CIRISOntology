import json, os, urllib.request
key = open(os.path.expanduser('~/.deepinfra_key')).read().strip()
model = "deepseek-ai/DeepSeek-R1-0528"
for i in (1,2,3):
    out = f"deep_deriver{i}.md"
    if os.path.exists(out): continue
    brief = open(f'api_brief_{i}.txt').read()
    req = urllib.request.Request(
        "https://api.deepinfra.com/v1/openai/chat/completions",
        data=json.dumps({"model": model, "messages":[{"role":"user","content":brief}],
                         "temperature":0.6, "max_tokens":16000}).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type":"application/json"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=1800))
        msg = r["choices"][0]["message"]
        text = msg.get("content") or ""
        open(out,'w').write(f"# deep_deriver{i} — {model}, temp 0.6, deep+blind cell\n\n" + text)
        print(f"deep {i} done: {len(text)} chars, {r.get('usage',{}).get('estimated_cost')}", flush=True)
    except Exception as e:
        print(f"deep {i} FAILED: {e}", flush=True)
print("DEEP-ALL-DONE", flush=True)
