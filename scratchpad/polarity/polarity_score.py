"""POLARITY panel — per POLARITY_PREREG.md §1/§2, conventions from plane_annotate.py.

One question per item: the DIRECTION of the single changed span along its kind's axis,
with AMBIGUOUS permitted. Three model FAMILIES, temperature 0, stateless calls, resumable,
spend read from usage fields, hard cap $0.30 (prereg §2).
"""
from __future__ import annotations
import json, os, pathlib, sys, threading, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

URL = "https://api.deepinfra.com/v1/openai/chat/completions"
KEY = pathlib.Path(os.path.expanduser("~/.deepinfra_key")).read_text().strip()
HARD_CAP_USD = 0.30

MODELS = ["meta-llama/Llama-4-Scout-17B-16E-Instruct",
          "openai/gpt-oss-120b",
          "google/gemma-3-27b-it"]
PRICE = {"meta-llama/Llama-4-Scout-17B-16E-Instruct": (0.08, 0.30),
         "openai/gpt-oss-120b": (0.09, 0.45),
         "google/gemma-3-27b-it": (0.10, 0.20)}

# POLARITY_PREREG.md §1, verbatim.
AXIS = {
 "Rules":         ("binding MORE (may->must, wider scope, added obligation)", "binding LESS"),
 "Confidence":    ("MORE certain (hedge removed, precision tightened)", "LESS certain"),
 "Facts":         ("value/claim INCREASED or added", "DECREASED or removed"),
 "Priorities":    ("the named item moves UP the order", "moves DOWN"),
 "Process":       ("steps ADDED or order made stricter", "REMOVED or loosened"),
 "Premises":      ("assumption made STRONGER/wider-scoped", "weaker/narrower"),
 "Model":         ("framework made MORE specific/constraining", "less"),
 "Structure":     ("encoding made MORE explicit/structured", "less"),
 "Manner":        ("register made MORE formal", "less formal"),
 "Identity":      ("reclassified to a WIDER/higher-status category", "narrower/lower"),
 "Circumstances": ("instance made MORE specific", "less specific"),
}
# Record has no §1 row: the prereg's table defines eleven axes and omits it.
# Record items are carried through the runner unscored and reported as such.

def prompt_for(item):
    k = item["axis_kind"]
    plus, minus = AXIS[k]
    return f"""You compare two versions of a document. The change between them has already been classified: it is a change of **{k}**. Your only task is to say which DIRECTION along that kind's axis the change moves.

For {k}:
- "+" means: {plus}
- "-" means: {minus}

"+" and "-" are labels for direction, not value judgments: neither is better.
Answer "AMBIGUOUS" if the direction is genuinely undefined for this change — if the change is a {k} change but the axis above does not pick out a direction for it. Do not answer AMBIGUOUS merely because the call is hard.

BEFORE:
---
{item['before']}
---
AFTER:
---
{item['after']}
---
The change is located here: {item['variation_site']}
The changed text reads "{item['span_before']}" in the earlier version and "{item['span_after']}" in the later version.

Answer with JSON only: {{"polarity": "<+ or - or AMBIGUOUS>", "reason": "<one sentence>"}}"""

def ask(model, text, retries=3):
    body = json.dumps({"model": model, "temperature": 0.0,
                       "max_tokens": (900 if "gpt-oss" in model else 400),
                       "messages": [{"role": "user", "content": text}]}).encode()
    for i in range(retries):
        try:
            req = urllib.request.Request(URL, data=body, headers={
                "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                d = json.loads(r.read())
            u = d.get("usage", {})
            return d["choices"][0]["message"]["content"], u.get("prompt_tokens", 0), u.get("completion_tokens", 0)
        except Exception as e:
            if i == retries - 1:
                raise
            time.sleep(4 * (i + 1))

def norm(p):
    if p is None: return None
    s = str(p).strip().strip('"').strip("`").upper()
    if s.startswith("AMB"): return "AMBIGUOUS"
    if s.startswith("+") or s in ("PLUS", "POSITIVE"): return "+"
    if s.startswith("-") or s in ("MINUS", "NEGATIVE"): return "-"
    return None

def main(corpus_path, out_path, workers=12):
    items = [json.loads(l) for l in open(corpus_path) if l.strip()]
    items = [i for i in items if i["axis_kind"] in AXIS]
    done = set()
    outp = pathlib.Path(out_path)
    if outp.exists():
        for l in open(outp):
            try:
                r = json.loads(l); done.add((r["id"], r["model"]))
            except Exception:
                pass
    todo = [(it, m) for it in items for m in MODELS if (it["id"], m) not in done]
    print(f"{len(items)} scoreable-axis items, {len(todo)} calls to make "
          f"({len(done)} already on disk)", flush=True)
    lock = threading.Lock()
    state = {"spend": 0.0, "n": 0, "capped": False}
    f = open(outp, "a")

    def one(job):
        it, m = job
        if state["capped"]: return
        try:
            txt, ti, to = ask(m, prompt_for(it))
        except Exception as e:
            with lock:
                f.write(json.dumps({"id": it["id"], "model": m, "error": repr(e)[:300]}) + "\n"); f.flush()
            return
        pi, po = PRICE.get(m, (0.2, 0.6))
        rec = {"id": it["id"], "axis_kind": it["axis_kind"], "kind_target": it["kind_target"],
               "model": m, "raw": txt, "in_tok": ti, "out_tok": to}
        try:
            j = json.loads(txt[txt.index("{"): txt.rindex("}") + 1])
            rec["polarity"] = norm(j.get("polarity")); rec["reason"] = j.get("reason")
        except Exception:
            rec["polarity"] = None
        with lock:
            state["spend"] += ti * pi / 1e6 + to * po / 1e6
            if state["spend"] > HARD_CAP_USD:
                state["capped"] = True
                print(f"HARD CAP: ${state['spend']:.3f} — stopping", flush=True)
                return
            f.write(json.dumps(rec) + "\n"); f.flush()
            state["n"] += 1
            if state["n"] % 100 == 0:
                print(f"  {state['n']}/{len(todo)}, ${state['spend']:.3f}", flush=True)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(one, todo))
    f.close()
    print(f"DONE: {state['n']} new judgments, spend ${state['spend']:.4f}")
    pathlib.Path(outp.parent / "spend_this_run.json").write_text(
        json.dumps({"new": state["n"], "spend_usd": round(state["spend"], 5),
                    "capped": state["capped"]}) + "\n")
    return 3 if state["capped"] else 0

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="/home/emoore/CIRISOntology/scratchpad/polarity/scoring_corpus.jsonl")
    ap.add_argument("--out", default="/home/emoore/CIRISOntology/scratchpad/polarity/polarity_judgments.jsonl")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--limit", type=int)
    a = ap.parse_args()
    sys.exit(main(a.corpus, a.out, a.workers))
