import json, re, os

BASE = "/home/emoore/CIRISOntology/scratchpad/plane_corpus"
OUT = os.path.join(BASE, "part_a.jsonl")

# taxonomy vocabulary that must never appear in artifact text (before/after)
_VOCAB = [
    r"\baxiotic\b", r"\bdeontic\b", r"\bpragmatic\b", r"\bontological\b",
    r"\bepistemic\b", r"\bempirical(ly)?\b", r"\bcontingent\b", r"\bnomological\b",
    r"\bstructural(ly)?\b", r"\btestimonial\b", r"\baxiomatic\b", r"\bprocedural(ly)?\b",
    r"\bpriorit(y|ies)\b", r"\brules?\b", r"\bmanners?\b", r"\bidentit(y|ies)\b",
    r"\bconfidence\b", r"\bfacts?\b", r"\bcircumstances?\b", r"\bprocess(es)?\b",
    r"\bmodels?\b", r"\bstructures?\b", r"\bpremises?\b", r"\brecords?\b",
]
# valence words banned everywhere (artifacts AND notes)
_VALENCE = [r"\bwrong(ly)?\b", r"\berrors?\b", r"\bmistakes?\b", r"\bincorrect(ly)?\b", r"\bbugs?\b", r"\bfault(y|s)?\b"]

def _check(text, pats, ident, where):
    for p in pats:
        m = re.search(p, text, re.I)
        assert not m, f"{ident}: banned term {m.group(0)!r} in {where}"

def add(items, fresh=False):
    mode = "w" if fresh else "a"
    out = []
    for it in items:
        ident = it["id"]
        before, old, new = it["before"], it["old"], it["new"]
        assert before.count(old) == 1, f"{ident}: old-string count {before.count(old)}"
        after = before.replace(old, new)
        assert after != before, ident
        for t, w in ((before, "before"), (after, "after")):
            _check(t, _VOCAB + _VALENCE, ident, w)
        for f in ("site", "note"):
            _check(it[f], _VALENCE, ident, f)
        dom = it["domain"]
        if dom == "policy":
            w = len(before.split()); assert 80 <= w <= 250, f"{ident}: {w} words"
        elif dom == "report":
            w = len(before.split()); assert 80 <= w <= 200, f"{ident}: {w} words"
        elif dom == "config":
            n = len(before.strip().splitlines()); assert 10 <= n <= 30, f"{ident}: {n} lines"
        elif dom == "code":
            n = len(before.strip().splitlines()); assert 10 <= n <= 40, f"{ident}: {n} lines"
        elif dom == "process":
            s = len([l for l in before.splitlines() if re.match(r"\s*\d+\.", l)])
            assert 6 <= s <= 15, f"{ident}: {s} steps"
        else:
            raise AssertionError(f"{ident}: bad domain {dom}")
        out.append(json.dumps({
            "id": ident, "kind_target": it["kind"], "domain": dom,
            "ambiguous_with": it.get("amb"), "difficulty": it["diff"],
            "before": before, "after": after,
            "variation_site": it["site"], "author_note": it["note"],
        }, ensure_ascii=False))
    with open(OUT, mode) as f:
        f.write("\n".join(out) + "\n")
    print(f"wrote {len(out)} items (mode={mode})")
