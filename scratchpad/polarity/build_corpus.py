"""POLARITY — step 1: build the scoring corpus (272 items) with mechanically extracted
single changed spans, and attach the EXISTING BASE-condition panel modal kind labels.

No polarity is assigned here. Nothing model-facing runs here.
Span extraction: word-level difflib on (before, after); an item is SINGLE-SPAN iff the
opcode list has exactly one non-'equal' block. Multi-span items are dropped and reported.
"""
from __future__ import annotations
import json, collections, difflib, pathlib, re, sys

R = pathlib.Path("/home/emoore/CIRISOntology/scratchpad/plane_corpus")
OUT = pathlib.Path("/home/emoore/CIRISOntology/scratchpad/polarity")

PLAIN = {"axiotic":"Priorities","deontic":"Rules","pragmatic":"Manner","ontological":"Identity",
 "epistemic":"Confidence","empirical":"Facts","contingent":"Circumstances","procedural":"Process",
 "nomological":"Model","structural":"Structure","axiomatic":"Premises","testimonial":"Record"}

def load(p):
    return [json.loads(l) for l in open(p) if l.strip()]

def toks(s):
    # keep whitespace as part of tokens so the span can be rebuilt verbatim
    return re.findall(r"\s*\S+", s)

def span(before, after):
    a, b = toks(before), toks(after)
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
    nblocks = len(ops)
    if nblocks == 0:
        return None, None, 0
    i1 = ops[0][1]; i2 = ops[-1][2]; j1 = ops[0][3]; j2 = ops[-1][4]
    return "".join(a[i1:i2]).strip(), "".join(b[j1:j2]).strip(), nblocks

def main():
    items = []
    for f, part in (("corpus_full.jsonl","FULL"), ("part_d.jsonl","D"), ("conj_items.jsonl","CONJ")):
        for r in load(R/f):
            r["_part"] = part
            items.append(r)
    print(f"loaded {len(items)} items ({collections.Counter(i['_part'] for i in items)})")

    # --- BASE-condition panel modals, from disk; ties (no plurality) excluded ---
    votes = collections.defaultdict(list)
    parse_fail = collections.Counter()
    for f in ("full_judgments.jsonl", "partd_judgments.jsonl", "conj_judgments.jsonl"):
        for r in load(R/f):
            if r.get("condition") != "BASE":
                continue
            if not r.get("kind"):
                parse_fail[f] += 1
                continue
            votes[r["id"]].append(r["kind"])
    modal, tie_ids = {}, []
    for iid, vs in votes.items():
        c = collections.Counter(vs).most_common()
        if len(c) > 1 and c[0][1] == c[1][1]:
            tie_ids.append(iid); continue
        modal[iid] = c[0][0]
    print(f"BASE judgments: {sum(len(v) for v in votes.values())} votes over {len(votes)} items; "
          f"unparsed BASE rows {dict(parse_fail)}; modal ties excluded: {len(tie_ids)}")

    out, dropped = [], []
    for r in items:
        sb, sa, nb = span(r["before"], r["after"])
        rec = {"id": r["id"], "part": r["_part"], "kind_target": r["kind_target"],
               "domain": r.get("domain"), "difficulty": r.get("difficulty"),
               "ambiguous_with": r.get("ambiguous_with"),
               "before": r["before"], "after": r["after"],
               "variation_site": r["variation_site"],
               "span_before": sb, "span_after": sa, "n_diff_blocks": nb,
               "base_modal": modal.get(r["id"]), "base_votes": votes.get(r["id"], []),
               "base_tie": r["id"] in tie_ids}
        # axis kind: the AUTHORED kind whose §1 rule defines this item's polarity axis.
        if r["kind_target"] in PLAIN:
            rec["axis_kind"] = PLAIN[r["kind_target"]]
        elif r["_part"] == "CONJ":
            rec["axis_kind"] = "Rules"   # author_note: "Deontic modal strength only"
        else:
            rec["axis_kind"] = None
        if nb != 1:
            dropped.append((r["id"], nb))
        out.append(rec)

    print(f"span blocks: {dict(collections.Counter(o['n_diff_blocks'] for o in out))}")
    if dropped:
        print(f"NOT single-span ({len(dropped)}): {dropped}")
    print("target-kind counts:", dict(collections.Counter(o['axis_kind'] for o in out).most_common()))
    p = OUT/"scoring_corpus.jsonl"
    with open(p, "w") as f:
        for o in out:
            f.write(json.dumps(o)+"\n")
    print("wrote", p, len(out))

if __name__ == "__main__":
    main()
