#!/usr/bin/env python3
"""Third-party API worker driver (DeepInfra). Reads spec from a file, writes draft to a file."""
import json, os, sys, urllib.request

KEY = open(os.path.expanduser("~/.deepinfra_key")).read().strip()
URL = "https://api.deepinfra.com/v1/openai/chat/completions"

def call(model, system, user, max_tokens=16000, temperature=0.2):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Authorization": "Bearer " + KEY,
        "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1200) as r:
        d = json.load(r)
    return d["choices"][0]["message"]["content"], d.get("usage", {})

if __name__ == "__main__":
    model, sysf, usrf, outf = sys.argv[1:5]
    system = open(sysf).read()
    user = open(usrf).read()
    txt, usage = call(model, system, user)
    open(outf, "w").write(txt)
    print("MODEL", model, "USAGE", json.dumps(usage), "BYTES", len(txt))
