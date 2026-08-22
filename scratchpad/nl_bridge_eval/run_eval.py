#!/usr/bin/env python3
"""NL_BRIDGE zero-shot eval. Labels masked to the 12 kinds; only slotting varies."""
import json, sys, time, urllib.request, collections

# Verbatim from Core/WrongKind.lean: WrongKind.plain and WrongKind.discriminator
KINDS = [
    ("Priorities",    "axiotic",     "What becomes more important?"),
    ("Rules",         "deontic",     "What becomes allowed or required?"),
    ("Manner",        "pragmatic",   "How is the same thing presented or used?"),
    ("Identity",      "ontological", "What is this said to be?"),
    ("Confidence",    "epistemic",   "How sure are we, and on what standard?"),
    ("Facts",         "empirical",   "What claimed fact becomes wrong?"),
    ("Circumstances", "contingent",  "What just happens to differ here?"),
    ("Process",       "procedural",  "What steps or ordering change?"),
    ("Model",         "nomological", "What rule or model are we reasoning under?"),
    ("Structure",     "structural",  "How are the pieces put together?"),
    ("Premises",      "axiomatic",   "What are we taking as given?"),
    ("Record",        "testimonial", "Can the event still be established from what survives?"),
]
PLAIN = {c: p for p, c, _ in KINDS}
LABELS = [p for p, _, _ in KINDS]

MENU = "\n".join(f"- {p}: {q}" for p, _, q in KINDS)
SYS = ("You classify what KIND of change was made to a document. "
       "Answer with exactly one label from this list, choosing by its question:\n"
       f"{MENU}\n"
       "Pick the single label whose question the change best answers.")

SCHEMA = {"type": "object",
          "properties": {"kind": {"type": "string", "enum": LABELS}},
          "required": ["kind"]}

def trunc(s, n=1400):
    s = s or ""
    return s if len(s) <= n else s[:n] + "\n[...truncated]"

def prompt_for(o):
    return (f"BEFORE:\n{trunc(o['before'])}\n\n"
            f"AFTER:\n{trunc(o['after'])}\n\n"
            f"WHAT CHANGED: {o.get('variation_site','')}\n\n"
            "Which kind of change is this?")

def ask(model, o, retries=3):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": SYS},
                     {"role": "user", "content": prompt_for(o)}],
        "stream": False, "format": SCHEMA,
        "options": {"temperature": 0, "num_predict": 24, "num_ctx": 4096},
        "think": False,
    }).encode()
    for a in range(retries):
        try:
            req = urllib.request.Request("http://localhost:11434/api/chat", body,
                                         {"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=180) as r:
                txt = json.loads(r.read())["message"]["content"]
            return json.loads(txt).get("kind")
        except Exception as e:
            if a == retries - 1:
                return None
            time.sleep(2)

def main(model, split, out):
    items = [json.loads(l) for l in open(split)]
    rows = []
    t0 = time.time()
    for i, o in enumerate(items, 1):
        pred = ask(model, o)
        rows.append({"id": o["id"], "gold_ctor": o["kind_target"],
                     "gold": PLAIN.get(o["kind_target"]), "pred": pred,
                     "difficulty": o.get("difficulty"), "domain": o.get("domain")})
        if i % 20 == 0:
            print(f"  {i}/{len(items)}  {time.time()-t0:.0f}s", flush=True)
    with open(out, "w") as f:
        for r in rows: f.write(json.dumps(r) + "\n")
    valid = sum(r["pred"] in LABELS for r in rows)
    corr = sum(r["pred"] == r["gold"] for r in rows)
    print(f"MODEL {model}: top1={corr/len(rows):.3f} ({corr}/{len(rows)}) "
          f"valid_label_rate={valid/len(rows):.3f} elapsed={time.time()-t0:.0f}s")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
