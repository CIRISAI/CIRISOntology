"""PLANE study — model-annotator runner. Per PLANE_PREREG.md + its 5b amendment.

Seven conditions x three model families x 240 items = 5,040 judgments. Stateless
API calls: each judgment is an independent request, so the in-context-fixation
control is satisfied automatically for MODEL annotators (no memory across calls);
the between-annotator discipline binds the human adjudication stage, not this one.
Recorded here so the prereg's protocol note is discharged, not skipped.

Valence-neutral throughout: the prompt asks "what kind of change", never "wrong".
Temperature 0. Resumable (skips already-written judgments). Cost tracked per call
from usage fields; aborts if projected spend exceeds the hard cap.
"""
from __future__ import annotations
import json, os, pathlib, sys, time, urllib.request

URL = "https://api.deepinfra.com/v1/openai/chat/completions"
KEY = pathlib.Path(os.path.expanduser("~/.deepinfra_key")).read_text().strip()
HARD_CAP_USD = 10.0

# Three FAMILIES — same-family annotators are one witness.
# Three FAMILIES (Meta / OpenAI-oss / Google). Smoke test 2026-08-18 found:
# gpt-oss is a reasoning model (needs max_tokens ~500 headroom for hidden
# reasoning); Qwen3 emits <think> blocks even with /no_think, so Gemma is the
# third family instead. All three verified returning parseable content.
MODELS = ["meta-llama/Llama-4-Scout-17B-16E-Instruct",
          "openai/gpt-oss-120b",
          "google/gemma-3-27b-it"]
# indicative $/Mtok (in, out) for cost projection; real spend read from usage
PRICE = {"meta-llama/Llama-4-Scout-17B-16E-Instruct": (0.08, 0.30),
         "openai/gpt-oss-120b": (0.09, 0.45),
         "google/gemma-3-27b-it": (0.10, 0.20)}

KINDS = ["axiotic","deontic","pragmatic","ontological","epistemic","empirical",
         "contingent","procedural","nomological","structural","axiomatic","testimonial"]
PLAIN = dict(zip(KINDS, ["Priorities","Rules","Manner","Identity","Confidence","Facts",
                          "Circumstances","Process","Model","Structure","Premises","Record"]))
DISC = {
 "axiotic":"What becomes more important?","deontic":"What becomes allowed or required?",
 "pragmatic":"How is the same thing presented or used?","ontological":"What is this said to be?",
 "epistemic":"How sure are we, and on what standard?","empirical":"What claimed fact becomes wrong?",
 "contingent":"What just happens to differ here?","procedural":"What steps or ordering change?",
 "nomological":"What rule or model are we reasoning under?","structural":"How are the pieces put together?",
 "axiomatic":"What are we taking as given?","testimonial":"Can the event still be established from what survives?"}

BOUNDARY_NOTES = """Two boundaries that matter:
- Confidence vs Facts: the proposition may stay identical while the warranted confidence changes; conversely, confidence may stay identical while the proposition itself becomes false.
- Model vs Facts: Model means the framework APPLIED to derive an answer. A model ASSERTED to be descriptively true of the world is itself a Fact."""

# --- the seven conditions (frame/design/warrant), one paragraph each, fixed ---
CONDITIONS = {
 "BASE": {"frame":"Assume every related record, log, and document survives and is available for consultation (full retention).",
          "design":"Assume the comparison holds everything else fixed: any element not named in the change description was identical between versions and is intended to stay identical.",
          "attr": None},
 "F1":   {"frame":"Assume PARTIAL retention: the artifact you see survives, but its sibling documents (upstream logs, source records, prior drafts, and any registers it references) have been destroyed and cannot be consulted.",
          "design":"Assume the comparison holds everything else fixed: any element not named in the change description was identical between versions and is intended to stay identical.",
          "attr": None},
 "F2":   {"frame":"Assume MINIMAL retention: only the two versions shown survive. No other record of any kind exists anywhere.",
          "design":"Assume the comparison holds everything else fixed: any element not named in the change description was identical between versions and is intended to stay identical.",
          "attr": None},
 "D1":   {"frame":"Assume every related record, log, and document survives and is available for consultation (full retention).",
          "design":"Assume the comparison holds fixed ONLY the document's substantive content requirements; incidental details (identifiers, timestamps, environment names, formatting, ordering of independent entries) were NOT controlled and are expected to differ between versions.",
          "attr": None},
 "D2":   {"frame":"Assume every related record, log, and document survives and is available for consultation (full retention).",
          "design":"Assume the changed element itself was SUPPOSED to be held fixed by the comparison design: whatever varied is something the comparison intended to keep identical.",
          "attr": None},
 "W2":   {"frame":"Assume every related record, log, and document survives and is available for consultation (full retention).",
          "design":"Assume the comparison holds everything else fixed: any element not named in the change description was identical between versions and is intended to stay identical.",
          "attr":"This change was made by the organization's own internal review board."},
 "W3":   {"frame":"Assume every related record, log, and document survives and is available for consultation (full retention).",
          "design":"Assume the comparison holds everything else fixed: any element not named in the change description was identical between versions and is intended to stay identical.",
          "attr":"This change was submitted anonymously by an unaffiliated outside party."},
}

def prompt_for(item, cond):
    c = CONDITIONS[cond]
    kinds_block = "\n".join(f"- {PLAIN[k]}: {DISC[k]}" for k in KINDS)
    attr = f"\nProvenance note: {c['attr']}\n" if c["attr"] else ""
    return f"""You classify a change between two versions of a document. Twelve kinds of change exist; pick the ONE whose question best captures what this change alters. Multi-label only if genuinely irreducible (then give up to two, primary first). "NO FIT" is allowed if none apply.

{kinds_block}

{BOUNDARY_NOTES}

Context for judgment:
- Retention: {c['frame']}
- Comparison: {c['design']}{attr}
BEFORE:
---
{item['before']}
---
AFTER:
---
{item['after']}
---
The change is located here: {item['variation_site']}

Answer with JSON only: {{"kind": "<one of: {', '.join(PLAIN.values())} or NO FIT>", "second": "<kind or null>", "reason": "<one sentence>"}}"""

def ask(model, text, retries=3):
    body = json.dumps({"model": model, "temperature": 0.0, "max_tokens": 500,
                       "messages":[{"role":"user","content": text}]}).encode()
    for i in range(retries):
        try:
            req = urllib.request.Request(URL, data=body, headers={
                "Authorization": f"Bearer {KEY}", "Content-Type":"application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                d = json.loads(r.read())
            u = d.get("usage", {})
            return d["choices"][0]["message"]["content"], u.get("prompt_tokens",0), u.get("completion_tokens",0)
        except Exception as e:
            if i == retries-1: raise
            time.sleep(4*(i+1))

def main(corpus_path, out_path, conditions=None, models=None, limit=None, workers=1):
    items = [json.loads(l) for l in open(corpus_path) if l.strip()]
    if limit: items = items[:limit]
    conds = conditions or list(CONDITIONS)
    mods = models or MODELS
    done = set()
    outp = pathlib.Path(out_path)
    if outp.exists():
        for l in open(outp):
            try: r=json.loads(l); done.add((r["id"], r["condition"], r["model"]))
            except Exception: pass
    import threading
    from concurrent.futures import ThreadPoolExecutor
    todo = [(it, cond, m) for it in items for cond in conds for m in mods
            if (it["id"], cond, m) not in done]
    lock = threading.Lock()
    state = {"spend": 0.0, "n": 0, "capped": False}
    f = open(outp, "a")

    def one(job):
        it, cond, m = job
        if state["capped"]: return
        txt, ti, to = ask(m, prompt_for(it, cond))
        pi, po = PRICE.get(m, (0.2, 0.6))
        rec = {"id": it["id"], "kind_target": it["kind_target"], "condition": cond,
               "model": m, "raw": txt, "in_tok": ti, "out_tok": to}
        try:
            j = json.loads(txt[txt.index("{"): txt.rindex("}")+1])
            rec["kind"] = j.get("kind"); rec["second"] = j.get("second"); rec["reason"] = j.get("reason")
        except Exception:
            rec["kind"] = None
        with lock:
            state["spend"] += ti*pi/1e6 + to*po/1e6
            if state["spend"] > HARD_CAP_USD:
                state["capped"] = True
                print(f"HARD CAP: projected ${state['spend']:.2f} — stopping", flush=True)
                return
            f.write(json.dumps(rec)+"\n"); f.flush()
            state["n"] += 1
            if state["n"] % 100 == 0:
                print(f"  {state['n']}/{len(todo)} judgments, est ${state['spend']:.2f}", flush=True)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(one, todo))
    f.close()
    print(f"DONE: {state['n']} new judgments, estimated spend ${state['spend']:.2f}")
    return 3 if state["capped"] else 0

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--conditions", nargs="*"); ap.add_argument("--models", nargs="*")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--workers", type=int, default=16)
    a = ap.parse_args()
    sys.exit(main(a.corpus, a.out, a.conditions, a.models, a.limit, a.workers))
