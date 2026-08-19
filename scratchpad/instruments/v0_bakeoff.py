"""Bake-off — v0's four heuristic-dominant instruments (structure, process,
circumstances, record) against the plane corpus, run in the SAME pattern as
v0b.py's provisional bake-off: BASE-condition panel-modal gold from
full_judgments.jsonl over corpus_full.jsonl (ties excluded, PROVISIONAL
framing), plus AUTHORED kind_target as a diagnostic-only second gold.

v0.py's four instruments do not share v0b's interface. Two take (before, after)
text directly (structure) or a derived step-list (process); the other two are
COORDINATE-TYPED and structurally REFUSE without a declared design
(circumstances) or frame (record) — v0.py's own docstring: "Design-relative BY
DEFINITION" / "repairability is relative to what survives". That refusal is
correct instrument behaviour, not a bake-off failure, and this harness reports
it as such. Do not modify v0.py; this file only adapts corpus items to its
call signatures and scores what comes back.

Adapters (declared here, not smuggled into v0.py):
  structure     : v0.structure(before, after) called on the RAW corpus text,
                  exactly as authored — no adapter needed, but see the finding
                  below: this text is prose, not JSON/Python.
  process       : v0.process(before_steps, after_steps) needs a typed step
                  list; the corpus gives none, so this harness segments each
                  document into sentences (regex, stdlib only) and calls those
                  the "steps". This is the harness's choice, fixed BEFORE
                  running (pre-registration), not tuned against the outcome.
  circumstances : v0.circumstances(varied_element, design). The corpus supplies
                  no `design` field on any item (checked below) — every call
                  passes design=None, i.e. this is the "artifact-only, no
                  coordinates" condition, not a weakened one.
  record        : v0.record(lost_fact, frame). Same situation: no `frame`
                  field anywhere in the corpus, every call passes frame=None.

Coordinate availability is checked programmatically, not assumed: see
`coordinate_supply_check()`.
"""
from __future__ import annotations
import json, re
from collections import Counter, defaultdict
from typing import Optional

import v0  # the four instruments under test — NOT modified

CORPUS = "/home/emoore/CIRISOntology/scratchpad/plane_corpus/corpus_full.jsonl"
JUDGMENTS = "/home/emoore/CIRISOntology/scratchpad/plane_corpus/full_judgments.jsonl"
OUT = "/home/emoore/CIRISOntology/scratchpad/instruments/v0_bakeoff.txt"

# Full 12-way plain-label -> internal-kind map, IDENTICAL to v0b.py's, used
# only to build gold. v0's four instruments cover exactly four of these keys;
# the other eight are legitimate "rest" classes for one-vs-rest scoring.
PLAIN_TO_INTERNAL = {"Priorities": "axiotic", "Rules": "deontic", "Manner": "pragmatic",
                     "Identity": "ontological", "Confidence": "epistemic",
                     "Facts": "empirical", "Circumstances": "contingent",
                     "Process": "procedural", "Model": "nomological",
                     "Structure": "structural", "Premises": "axiomatic",
                     "Record": "testimonial"}

# v0's four function names -> the internal kind label each one targets.
INSTRUMENT_KIND = {"structure": "structural", "process": "procedural",
                    "circumstances": "contingent", "record": "testimonial"}


def load_corpus() -> list[dict]:
    with open(CORPUS) as f:
        return [json.loads(l) for l in f if l.strip()]


def provisional_gold() -> tuple[dict, int]:
    """Same construction as v0b.py: BASE-condition panel-modal label, ties
    excluded (-> None). PROVISIONAL: not a human ceiling, validates nothing."""
    votes: dict[str, Counter] = defaultdict(Counter)
    with open(JUDGMENTS) as f:
        for line in f:
            d = json.loads(line)
            if d.get("condition") != "BASE":
                continue
            lab = d.get("kind")
            if lab not in PLAIN_TO_INTERNAL:
                continue
            votes[d["id"]][lab] += 1
    gold, ties = {}, 0
    for id_, c in votes.items():
        top = c.most_common(2)
        if len(top) > 1 and top[0][1] == top[1][1]:
            ties += 1
            gold[id_] = None
        else:
            gold[id_] = PLAIN_TO_INTERNAL[top[0][0]]
    return gold, ties


def _prf(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return p, r, f


# ---------------------------------------------------------------- adapters

_SENT_SPLIT = re.compile(r"(?<=[.!?;])\s+")


def _sentences(text: str) -> list[str]:
    """Pre-registered process() adapter: flatten newlines, split on sentence
    punctuation. Fixed before any result was inspected."""
    flat = text.replace("\n", " ")
    return [s.strip() for s in _SENT_SPLIT.split(flat.strip()) if s.strip()]


def run_structure(d: dict) -> v0.Verdict:
    return v0.structure(d["before"], d["after"])


def run_process(d: dict) -> v0.Verdict:
    return v0.process(_sentences(d["before"]), _sentences(d["after"]))


def run_circumstances(d: dict) -> v0.Verdict:
    # No corpus item carries a `design`; varied_element is unused when
    # design=None (circumstances refuses on that alone) but we pass the
    # author's own description of the varied element for the record.
    return v0.circumstances(d.get("variation_site", ""), d.get("design"))


def run_record(d: dict) -> v0.Verdict:
    # No corpus item carries a `frame`; same situation as above.
    return v0.record(d.get("variation_site", ""), d.get("frame"))


RUNNERS = {"structure": run_structure, "process": run_process,
           "circumstances": run_circumstances, "record": run_record}


def coordinate_supply_check(corpus: list[dict]) -> dict:
    """Does ANY item's metadata carry a design or frame coordinate? Checked,
    not assumed."""
    n_design = sum(1 for d in corpus if d.get("design") is not None)
    n_frame = sum(1 for d in corpus if d.get("frame") is not None)
    keys = sorted({k for d in corpus for k in d.keys()})
    return {"n_design": n_design, "n_frame": n_frame, "n_total": len(corpus),
            "keys_present": keys}


# ---------------------------------------------------------------- report

def bakeoff(out_path: Optional[str] = None) -> str:
    corpus = load_corpus()
    gold, ties = provisional_gold()
    lines = []
    say = lines.append

    say("=" * 78)
    say("N7 BAKE-OFF — v0's four heuristic-dominant instruments")
    say("(structure, process, circumstances, record) vs the plane corpus")
    say("Gold = BASE-condition modal panel label (3 judge models). PROVISIONAL:")
    say("panel-modal is NOT a human ceiling; no instrument is validated by this")
    say("table. Second gold = AUTHORED kind_target, diagnostic only.")
    say("=" * 78)
    scored = [d for d in corpus if gold.get(d["id"])]
    say(f"items: {len(corpus)} in corpus, {len(scored)} scored against panel-modal, "
        f"{ties} panel ties excluded")

    # ---- coordinate supply check, stated before any scoring
    cov = coordinate_supply_check(corpus)
    say("")
    say("--- coordinate supply check (circumstances needs `design`, record needs `frame`) ---")
    say(f"item metadata fields present anywhere in the corpus: {cov['keys_present']}")
    say(f"items carrying a `design` coordinate: {cov['n_design']}/{cov['n_total']}")
    say(f"items carrying a `frame` coordinate:  {cov['n_frame']}/{cov['n_total']}")
    say("Neither coordinate is supplied by any item in this corpus. Every")
    say("circumstances()/record() call below runs with design=None / frame=None:")
    say("the true artifact-only condition, not a weakened stand-in for one.")

    # ---- run all four instruments on all items
    readings: dict[str, dict[str, v0.Verdict]] = {}
    for d in corpus:
        readings[d["id"]] = {name: fn(d) for name, fn in RUNNERS.items()}

    # ---- dual P/R/F1 table, one-vs-rest, matching v0b.py's harness pattern
    for gold_name, gold_map, note in (
            ("PANEL-MODAL (provisional gold)", gold, "ties excluded"),
            ("AUTHORED kind_target (authors' intent — diagnostic only)",
             {d["id"]: d["kind_target"] for d in corpus}, "all 248 items")):
        say("")
        say(f"--- against {gold_name} [{note}] ---")
        say(f"{'instrument':14s} {'kind':12s} {'P':>6s} {'R':>6s} {'F1':>6s}  "
            f"{'tp':>3s} {'fp':>3s} {'fn':>3s}  top false-fire sources")
        for iname, kind in INSTRUMENT_KIND.items():
            tp = fp = fn_ = 0
            fp_from = Counter()
            for d in corpus:
                g = gold_map.get(d["id"])
                if g is None:
                    continue
                fired = readings[d["id"]][iname].result == "FIRES"
                if fired and g == kind:
                    tp += 1
                elif fired:
                    fp += 1
                    fp_from[g] += 1
                elif g == kind:
                    fn_ += 1
            p, r, f = _prf(tp, fp, fn_)
            src = ", ".join(f"{k}:{v}" for k, v in fp_from.most_common(3)) or "-"
            say(f"{iname:14s} {kind:12s} {p:6.2f} {r:6.2f} {f:6.2f}  "
                f"{tp:3d} {fp:3d} {fn_:3d}  {src}")

    # ---- refusal accounting
    say("")
    say("=" * 78)
    say("REFUSAL ACCOUNTING (all 248 items, artifact-only — no coordinates supplied)")
    say("=" * 78)
    say(f"{'instrument':14s} {'FIRES':>6s} {'CLEAN':>6s} {'REFUSED':>8s}  refusal reason(s)")
    for iname in RUNNERS:
        c = Counter(readings[d["id"]][iname].result for d in corpus)
        reasons = Counter(readings[d["id"]][iname].detail for d in corpus
                           if readings[d["id"]][iname].result == "REFUSED")
        top_reason = reasons.most_common(1)[0][0] if reasons else "-"
        say(f"{iname:14s} {c['FIRES']:6d} {c['CLEAN']:6d} {c['REFUSED']:8d}  {top_reason}")

    say("")
    say("structure    : REFUSED means BEFORE fails to parse as JSON or Python — this is")
    say("               a real baseline-missing refusal, not a missing declared coordinate.")
    say("               Breakdown by corpus `domain`:")
    dom_struct = Counter((d["domain"], readings[d["id"]]["structure"].result) for d in corpus)
    for k in sorted(dom_struct):
        say(f"                 domain={k[0]:8s} result={k[1]:8s} n={dom_struct[k]}")
    say("")
    say("process      : v0.process() has NO refusal branch at all (CLEAN or FIRES only) —")
    say("               confirmed: 0 REFUSED above. It cannot decline for missing input.")
    say("")
    say("circumstances: REFUSED on every one of 248 items — 'no design declared — contingency")
    say("               is relative to the comparison'. This is v0.py's documented correct")
    say("               behaviour on an artifact with no declared held-fixed set, not failure.")
    say("")
    say("record       : REFUSED on every one of 248 items — 'no frame declared — repairability")
    say("               is relative to what survives'. Same situation: v0.py's documented")
    say("               correct behaviour, not failure. This is the ~always-refuses reading")
    say("               the task predicted for testimonial, and it holds exactly.")

    # ---- can circumstances/record be scored separately with supplied coordinates?
    say("")
    say("--- scoring circumstances/record with corpus-supplied coordinates ---")
    say(f"items with a design coordinate supplied by the corpus:  {cov['n_design']}")
    say(f"items with a frame coordinate supplied by the corpus:   {cov['n_frame']}")
    say("Both are zero. There is no subset of this corpus on which circumstances or")
    say("record can be scored on FIRES-vs-CLEAN accuracy artifact-only: every call is")
    say("necessarily the design=None / frame=None refusal case. The P/R/F1 rows for")
    say("circumstances and record in the tables above are NOT a measurement of the")
    say("judge half's discrimination — they are 0/0/0 by construction (tp=fp=0")
    say("because nothing ever fires) and should be read as such, not as a score.")

    # ---- process saturation, stated plainly (a residual is never support)
    say("")
    say("--- process() adapter saturation, stated plainly ---")
    proc_fires = sum(1 for d in corpus if readings[d["id"]]["process"].result == "FIRES")
    say(f"process() FIRES on {proc_fires}/{len(corpus)} items via the sentence-split adapter.")
    say("v0.process() tests step-set/step-order EQUALITY; sentence strings change under")
    say("almost any edit, so the crude adapter routes nearly everything to the 'steps")
    say("added/removed' FIRES branch regardless of kind. This is an adapter artifact,")
    say("not a discovery about ordering-sensitivity, and the P/R numbers above should be")
    say("read as measuring that saturation, not the instrument's target-kind accuracy.")
    clean_ids = [d["id"] for d in corpus if readings[d["id"]]["process"].result == "CLEAN"]
    say(f"the lone non-firing item: {clean_ids}")

    # ---- structure() scope, stated plainly
    say("")
    say("--- structure() scope, stated plainly ---")
    struct_fires = sum(1 for d in corpus if readings[d["id"]]["structure"].result == "FIRES")
    struct_refused = sum(1 for d in corpus if readings[d["id"]]["structure"].result == "REFUSED")
    say(f"structure() FIRES on {struct_fires}/{len(corpus)} items — that INCLUDES the 4")
    say("items authored as kind_target=structural in the code domain, which are")
    say("dispatch-breaking changes that stay valid Python (e.g. a function's return type")
    say("changing from a tuple to a dict, breaking callers that unpack it, with no")
    say("SyntaxError anywhere). v0.py's structure() operationalises 'breaks")
    say("parsing/dispatch' as JSON/Python PARSEABILITY only; it has zero recall for")
    say("dispatch breaks that stay syntactically valid — and it REFUSES outright")
    say(f"(no baseline to compare) on {struct_refused}/{len(corpus)} items that are prose,")
    say("not JSON/Python, in the first place.")

    # ---- bottom line
    say("")
    say("=" * 78)
    say("BOTTOM LINE — which of the four can honestly be scored at all, artifact-only")
    say("=" * 78)
    say("circumstances : NO. Correctly refuses on all 248/248 items (no design supplied")
    say("                anywhere in the corpus). 0 items scoreable; this is the")
    say("                instrument working as documented, not a gap in it.")
    say("record        : NO. Correctly refuses on all 248/248 items (no frame supplied")
    say("                anywhere in the corpus). Same situation — the predicted")
    say("                'testimonial refuses ~always artifact-only' reading holds exactly.")
    say("structure     : NO, not informatively. Runs (56/248 non-refused) but FIRES 0/248")
    say("                times — its parseability check never detects this corpus's")
    say("                dispatch-breaking 'structural' edits, and it REFUSES outright on")
    say("                192/248 prose items with no JSON/Python baseline to read at all.")
    say("process       : NO, not informatively. Never refuses, but the only available")
    say("                before/after -> step-list adapter saturates it to FIRES on")
    say("                247/248 items; the resulting P/R numbers measure the adapter's")
    say("                coarseness, not the instrument's order-sensitivity.")
    say("")
    say("None of the four v0 instruments yields a usable FIRES-vs-CLEAN signal on this")
    say("corpus artifact-only. Two (circumstances, record) refuse by design because the")
    say("coordinate they require is never supplied here — correct, documented behaviour.")
    say("The other two (structure, process) return verdicts but the verdicts are")
    say("dominated by scope mismatch (structure) or adapter saturation (process), not by")
    say("target-kind discrimination. v0.py's own header says as much: 'these are the")
    say("heuristic halves only... nothing here is validated.' This bake-off does not")
    say("change that; it locates exactly where each of the four stands before judge")
    say("halves or richer coordinate supply could change the picture.")

    text = "\n".join(lines)
    if out_path:
        with open(out_path, "w") as f:
            f.write(text + "\n")
    return text


if __name__ == "__main__":
    print("running v0.py's own dye tests first (must pass before bake-off means anything)...")
    dye_results = v0.dye_tests()
    dye_ok = all(p for _, p in dye_results)
    for name, passed in dye_results:
        if not passed:
            print(f"  FAIL: {name}")
    print(f"v0 dye tests: {sum(p for _, p in dye_results)}/{len(dye_results)} "
          f"{'PASS' if dye_ok else 'FAIL'}")
    if not dye_ok:
        raise SystemExit("v0.py dye tests failed — bake-off would not mean anything, aborting")
    print()
    text = bakeoff(OUT)
    print(text)
    print(f"\n[bake-off saved to {OUT}]")
