import json, os, glob, urllib.request
key = open(os.path.expanduser('~/.deepinfra_key')).read().strip()
models = {"ds": "deepseek-ai/DeepSeek-V3.1", "qw": "Qwen/Qwen3-235B-A22B-Instruct-2507"}
for f in sorted(glob.glob('score_input_d*.txt')):
    base = f.replace('score_input_','score_').replace('.txt','')
    brief = open(f).read()
    for tag, model in models.items():
        out = f"{base}_{tag}.md"
        if os.path.exists(out): continue
        req = urllib.request.Request(
            "https://api.deepinfra.com/v1/openai/chat/completions",
            data=json.dumps({"model":model,"messages":[{"role":"user","content":brief}],
                             "temperature":0.2,"max_tokens":4000}).encode(),
            headers={"Authorization": f"Bearer {key}","Content-Type":"application/json"})
        try:
            r = json.load(urllib.request.urlopen(req, timeout=900))
            open(out,'w').write(f"# {out} — {model}\n\n" + r["choices"][0]["message"]["content"])
            print(f"{out} done", flush=True)
        except Exception as e:
            print(f"{out} FAILED: {e}", flush=True)
print("SCORER2-ALL-DONE", flush=True)
