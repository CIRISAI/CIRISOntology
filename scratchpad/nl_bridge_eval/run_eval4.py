#!/usr/bin/env python3
"""NL_BRIDGE 4-way surface eval. Grouping from surface_map.json (Lean-derived)."""
import json, sys, time, urllib.request

M = json.load(open("surface_map.json"))
K2B, SURF = M["kind2block"], M["surface_plain"]
LABELS = ["Facts", "Rules", "Identity", "Manner"]

# Family glosses quoted from Site.block's source comments in Core/Surface.lean
FAM = [
    ("Facts",    "the assertive family: what is claimed, how strongly, under what rule, on what premise"),
    ("Rules",    "the directive family: what is required, in what preference order, in what step order"),
    ("Identity", "the declarative family: what counts as what"),
    ("Manner",   "the force-neutral carrier family: how it is encoded, how it is presented or registered, which instance it is"),
]
MENU = "\n".join(f"- {n}: {g}" for n, g in FAM)
SYS = ("You classify what FAMILY of change was made to a document. "
       "Answer with exactly one label from this list:\n"
       f"{MENU}\n"
       "Pick the single family the change belongs to.")
SCHEMA = {"type": "object",
          "properties": {"family": {"type": "string", "enum": LABELS}},
          "required": ["family"]}

def trunc(s, n=1400):
    s = s or ""
    return s if len(s) <= n else s[:n] + "\n[...truncated]"

def prompt_for(o):
    return (f"BEFORE:\n{trunc(o['before'])}\n\nAFTER:\n{trunc(o['after'])}\n\n"
            f"WHAT CHANGED: {o.get('variation_site','')}\n\nWhich family of change is this?")

def ask(model, o, retries=3):
    body = json.dumps({"model": model,
        "messages": [{"role": "system", "content": SYS},
                     {"role": "user", "content": prompt_for(o)}],
        "stream": False, "format": SCHEMA,
        "options": {"temperature": 0, "num_predict": 24, "num_ctx": 4096},
        "think": False}).encode()
    for a in range(retries):
        try:
            req = urllib.request.Request("http://localhost:11434/api/chat", body,
                                         {"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(json.loads(r.read())["message"]["content"]).get("family")
        except Exception:
            if a == retries - 1: return None
            time.sleep(2)

def main(model, split, out):
    items = [json.loads(l) for l in open(split)]
    kept = [o for o in items if o["kind_target"] in K2B]   # Record has no block
    print(f"  items={len(items)} scored={len(kept)} dropped_Record={len(items)-len(kept)}")
    rows, t0 = [], time.time()
    for i, o in enumerate(kept, 1):
        pred = ask(model, o)
        rows.append({"id": o["id"], "gold_ctor": o["kind_target"],
                     "gold": SURF[K2B[o["kind_target"]]], "pred": pred})
        if i % 25 == 0: print(f"  {i}/{len(kept)}  {time.time()-t0:.0f}s", flush=True)
    with open(out, "w") as f:
        for r in rows: f.write(json.dumps(r) + "\n")
    corr = sum(r["pred"] == r["gold"] for r in rows)
    valid = sum(r["pred"] in LABELS for r in rows)
    print(f"MODEL {model}: 4way={corr/len(rows):.3f} ({corr}/{len(rows)}) "
          f"valid={valid/len(rows):.3f} elapsed={time.time()-t0:.0f}s")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
