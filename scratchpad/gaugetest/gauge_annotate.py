"""GAUGE TEST — panel runner for arms A / B / C. Per GAUGE_TEST_PREREG.md + EXECUTION_NOTE.md.

Three arms over plane_corpus/corpus_full.jsonl (248 items) x 3 model families, BASE
condition. The ONLY variable is the offered label set:
  A: full 11 + Record        (test-retest noise floor; prompt must be byte-identical to the
                              original BASE run)
  B: 10 + Record, Circumstances removed
  C: 10 + Record, Structure removed

Everything else -- condition text, boundary notes, discriminators, models, temperature,
max_tokens, retry policy, parse rule -- is imported from plane_annotate.py, not re-typed.
Resumable (skips judgments already on disk). Spend read from the API usage fields.
"""
from __future__ import annotations
import json, pathlib, sys, threading, time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import plane_annotate as PA

ROOT = pathlib.Path("/home/emoore/CIRISOntology/scratchpad/gaugetest")
CORPUS = pathlib.Path("/home/emoore/CIRISOntology/scratchpad/plane_corpus/corpus_full.jsonl")
CAP_USD = 0.40                      # prereg spend cap, whole test
ARMS = {"A": None, "B": "contingent", "C": "structural"}   # arm -> KINDS key removed


def prompt_for(item, removed=None):
    """plane_annotate.prompt_for(item, 'BASE') with ONE edit: the offered label set."""
    if removed is None:
        return PA.prompt_for(item, "BASE")
    kinds = [k for k in PA.KINDS if k != removed]
    c = PA.CONDITIONS["BASE"]
    kinds_block = "\n".join(f"- {PA.PLAIN[k]}: {PA.DISC[k]}" for k in kinds)
    names = ", ".join(PA.PLAIN[k] for k in kinds)
    return f"""You classify a change between two versions of a document. Eleven kinds of change exist; pick the ONE whose question best captures what this change alters. Multi-label only if genuinely irreducible (then give up to two, primary first). "NO FIT" is allowed if none apply.

{kinds_block}

{PA.BOUNDARY_NOTES}

Context for judgment:
- Retention: {c['frame']}
- Comparison: {c['design']}
BEFORE:
---
{item['before']}
---
AFTER:
---
{item['after']}
---
The change is located here: {item['variation_site']}

Answer with JSON only: {{"kind": "<one of: {names} or NO FIT>", "second": "<kind or null>", "reason": "<one sentence>"}}"""


def selfcheck(items):
    """EXECUTION_NOTE G6: arm A must be byte-identical to the original BASE prompt, and the
    B/C prompts must differ from it in exactly the ways declared."""
    for it in items:
        assert prompt_for(it, None) == PA.prompt_for(it, "BASE"), f"ARM A PROMPT DRIFT: {it['id']}"
    it = items[0]
    base = PA.prompt_for(it, "BASE")
    for arm, rem in (("B", "contingent"), ("C", "structural")):
        p = prompt_for(it, rem)
        assert "Eleven kinds" in p and "Twelve kinds" not in p, arm
        assert f"- {PA.PLAIN[rem]}:" not in p, arm
        # every other kind's line survives verbatim
        for k in PA.KINDS:
            if k == rem:
                continue
            assert f"- {PA.PLAIN[k]}: {PA.DISC[k]}" in p, (arm, k)
        # the only removed text is the kind's own line and its two name mentions
        assert PA.BOUNDARY_NOTES in p and PA.CONDITIONS["BASE"]["frame"] in p, arm
        assert p.count(PA.PLAIN[rem]) == 0, arm
        assert len(base) > len(p), arm
    print("SELFCHECK OK: arm A byte-identical to the original BASE prompt; B/C differ only in "
          "the offered label set", flush=True)


def main(arm, workers=12):
    removed = ARMS[arm]
    items = [json.loads(l) for l in open(CORPUS) if l.strip()]
    selfcheck(items)
    out_path = ROOT / f"judgments_{arm}.jsonl"
    done = set()
    if out_path.exists():
        for l in open(out_path):
            try:
                r = json.loads(l)
                done.add((r["id"], r["model"]))
            except Exception:
                pass
    todo = [(it, m) for it in items for m in PA.MODELS if (it["id"], m) not in done]
    print(f"ARM {arm}: removed={removed}; {len(items)} items x {len(PA.MODELS)} models; "
          f"{len(done)} on disk; {len(todo)} to run", flush=True)
    if not todo:
        (ROOT / f"DONE_{arm}").write_text(f"already complete {time.ctime()}\n")
        return 0

    # spend already booked by earlier arms / earlier partial runs of this arm
    prior = 0.0
    for p in ROOT.glob("spend_*.json"):
        try:
            prior += json.load(open(p))["spend"]
        except Exception:
            pass
    print(f"prior booked spend ${prior:.4f}; cap ${CAP_USD:.2f}", flush=True)

    lock = threading.Lock()
    state = {"spend": 0.0, "n": 0, "capped": False, "fail": 0}
    f = open(out_path, "a")

    def one(job):
        it, m = job
        if state["capped"]:
            return
        try:
            txt, ti, to = PA.ask(m, prompt_for(it, removed))
        except Exception as e:
            with lock:
                state["fail"] += 1
                print(f"  REQUEST FAIL {it['id']} {m}: {e}", flush=True)
            return
        pi, po = PA.PRICE.get(m, (0.2, 0.6))
        rec = {"id": it["id"], "kind_target": it["kind_target"], "arm": arm,
               "removed": removed, "condition": "BASE", "model": m, "raw": txt,
               "in_tok": ti, "out_tok": to}
        try:
            j = json.loads(txt[txt.index("{"): txt.rindex("}") + 1])
            rec["kind"] = j.get("kind"); rec["second"] = j.get("second"); rec["reason"] = j.get("reason")
        except Exception:
            rec["kind"] = None
        with lock:
            state["spend"] += ti * pi / 1e6 + to * po / 1e6
            if prior + state["spend"] > CAP_USD:
                state["capped"] = True
                print(f"HARD CAP: ${prior + state['spend']:.4f} — stopping", flush=True)
                return
            f.write(json.dumps(rec) + "\n"); f.flush()
            state["n"] += 1
            if state["n"] % 100 == 0:
                print(f"  {state['n']}/{len(todo)} judgments, this run ${state['spend']:.4f}", flush=True)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(one, todo))
    f.close()
    json.dump({"arm": arm, "spend": state["spend"], "n": state["n"], "request_failures": state["fail"]},
              open(ROOT / f"spend_{arm}_{int(time.time())}.json", "w"))
    print(f"ARM {arm} DONE: {state['n']} new judgments, ${state['spend']:.4f}, "
          f"{state['fail']} request failures", flush=True)
    if state["capped"]:
        return 3
    # completeness: every (item, model) present?
    have = set()
    for l in open(out_path):
        r = json.loads(l); have.add((r["id"], r["model"]))
    missing = [(it["id"], m) for it in items for m in PA.MODELS if (it["id"], m) not in have]
    if missing:
        print(f"INCOMPLETE: {len(missing)} missing — rerun this arm to resume", flush=True)
        return 4
    (ROOT / f"DONE_{arm}").write_text(f"complete {time.ctime()} n={len(have)}\n")
    return 0


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, choices=list(ARMS))
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--selfcheck-only", action="store_true")
    a = ap.parse_args()
    if a.selfcheck_only:
        selfcheck([json.loads(l) for l in open(CORPUS) if l.strip()])
        sys.exit(0)
    sys.exit(main(a.arm, a.workers))
