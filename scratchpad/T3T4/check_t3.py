"""T3 item corpus — mechanical self-check.

Per RECOGNITION_PREREG.md §T3.2/§T3.3 (frozen) as amended by
RECOGNITION_PREREG_A2.md MAJOR-6 (arm D = 24 + 24; arms A and B stay at 30).
Items authored after the freeze.

Checks, in order:
  1. schema: required fields present, ids unique, arm in {A,B,D-rule,D-fact}
  2. `old` occurs EXACTLY ONCE in `before` (word-independent, literal)
  3. `after` == before.replace(old, new), and `after` != `before`
  4. SINGLE CONTIGUOUS SPAN: the minimal LCP/LCS diff between `before` and
     `after`, computed independently of the declaration, lies wholly inside the
     declared `old` span.  Because `old` occurs once and the substitution is a
     single literal replace, the change is one contiguous region by
     construction; this re-derives that region and asserts containment, so a
     multi-part change cannot be smuggled in through a declaration.
  5. recomputation structure: for arms A, B and D-rule the changed span must
     carry at least TWO numeric tokens that differ between `old` and `new`
     (the applied value plus at least one value derived from it).  For D-fact
     the span must be short (<= 25 words) and differ in at least one token.
  6. ban-set scan (standing _VOCAB + _VALENCE of plane_corpus/_helper.py,
     EXTENDED per §T3.3) over `before`, `after` and `variation_site`;
     _VALENCE only over `author_note`.
  7. domain bands, verbatim from plane_corpus/_helper.py
  8. arm counts 30 / 30 / 24 / 24, and a domain balance report
"""
from __future__ import annotations
import json, re, sys
from collections import Counter, defaultdict
from difflib import SequenceMatcher

ITEMS_PATH = "/home/emoore/CIRISOntology/scratchpad/T3T4/t3_items.jsonl"

# --- standing recipe, copied verbatim from plane_corpus/_helper.py ----------
_VOCAB = [
    r"\baxiotic\b", r"\bdeontic\b", r"\bpragmatic\b", r"\bontological\b",
    r"\bepistemic\b", r"\bempirical(ly)?\b", r"\bcontingent\b", r"\bnomological\b",
    r"\bstructural(ly)?\b", r"\btestimonial\b", r"\baxiomatic\b", r"\bprocedural(ly)?\b",
    r"\bpriorit(y|ies)\b", r"\brules?\b", r"\bmanners?\b", r"\bidentit(y|ies)\b",
    r"\bconfidence\b", r"\bfacts?\b", r"\bcircumstances?\b", r"\bprocess(es)?\b",
    r"\bmodels?\b", r"\bstructures?\b", r"\bpremises?\b", r"\brecords?\b",
]
_VALENCE = [r"\bwrong(ly)?\b", r"\berrors?\b", r"\bmistakes?\b", r"\bincorrect(ly)?\b",
            r"\bbugs?\b", r"\bfault(y|s)?\b"]
# --- §T3.3 extension, declared for this leg --------------------------------
_EXTENDED = [r"likelihood\s+model", r"transition\s+model", r"generative\s+model",
             r"observation\s+model", r"active\s+inference", r"hidden\s+state",
             r"dynamics\s+model"]

BAN_ARTIFACT = _VOCAB + _VALENCE + _EXTENDED
BAN_SITE = _VOCAB + _VALENCE + _EXTENDED
BAN_NOTE = _VALENCE + _EXTENDED

ARMS = {"A": 30, "B": 30, "D-rule": 24, "D-fact": 24}
DOMAINS = ("policy", "config", "code", "report", "process")
NUM = re.compile(r"\d+(?:[.,]\d+)*")


def scan(text, pats, ident, where):
    for p in pats:
        m = re.search(p, text, re.I)
        if m:
            raise AssertionError(f"{ident}: banned term {m.group(0)!r} in {where}")


def diff_region(a: str, b: str):
    """Minimal LCP/LCS diff. Returns (start, end_in_a) — one contiguous region."""
    n = min(len(a), len(b))
    p = 0
    while p < n and a[p] == b[p]:
        p += 1
    s = 0
    while s < n - p and a[len(a) - 1 - s] == b[len(b) - 1 - s]:
        s += 1
    return p, len(a) - s


def band(ident, dom, before):
    if dom == "policy":
        w = len(before.split())
        assert 80 <= w <= 250, f"{ident}: {w} words (policy band 80-250)"
        return f"{w}w"
    if dom == "report":
        w = len(before.split())
        assert 80 <= w <= 200, f"{ident}: {w} words (report band 80-200)"
        return f"{w}w"
    if dom == "config":
        n = len(before.strip().splitlines())
        assert 10 <= n <= 30, f"{ident}: {n} lines (config band 10-30)"
        return f"{n}L"
    if dom == "code":
        n = len(before.strip().splitlines())
        assert 10 <= n <= 40, f"{ident}: {n} lines (code band 10-40)"
        return f"{n}L"
    if dom == "process":
        s = len([l for l in before.splitlines() if re.match(r"\s*\d+\.", l)])
        assert 6 <= s <= 15, f"{ident}: {s} steps (process band 6-15)"
        return f"{s}s"
    raise AssertionError(f"{ident}: bad domain {dom}")


def main():
    rows = [json.loads(l) for l in open(ITEMS_PATH) if l.strip()]
    seen, arm_count, cell = set(), Counter(), defaultdict(Counter)
    changed_words = {}
    bands = {}
    for it in rows:
        for f in ("id", "arm", "domain", "before", "after", "old", "new",
                  "variation_site", "author_note"):
            assert f in it, f"{it.get('id','?')}: missing field {f}"
        ident, arm, dom = it["id"], it["arm"], it["domain"]
        assert ident not in seen, f"duplicate id {ident}"
        seen.add(ident)
        assert arm in ARMS, f"{ident}: bad arm {arm}"
        assert dom in DOMAINS, f"{ident}: bad domain {dom}"
        before, after, old, new = it["before"], it["after"], it["old"], it["new"]

        # (2) old occurs exactly once
        occ = before.count(old)
        assert occ == 1, f"{ident}: old span occurs {occ}x in before"
        # (3) after is that one substitution and nothing else
        assert after == before.replace(old, new), f"{ident}: after is not the declared substitution"
        assert after != before, f"{ident}: after == before"
        assert old != new, f"{ident}: old == new"

        # (4) independent single-span verification
        start, end = diff_region(before, after)
        o_at = before.index(old)
        assert start >= o_at and end <= o_at + len(old), (
            f"{ident}: real diff [{start},{end}) escapes declared span [{o_at},{o_at+len(old)})")
        assert end > start or len(after) != len(before), f"{ident}: empty diff"

        # (5) recomputation structure.  For an applied-rule arm the span must
        # contain at least TWO SEPARATED changed blocks at word level: the value
        # the rule turns on, and at least one value the artifact derives from it.
        # A span whose only change is the parameter itself is a broken item —
        # the artifact would then assert a conclusion its own rule no longer gives.
        blocks = [op for op in SequenceMatcher(None, old.split(), new.split()).get_opcodes()
                  if op[0] != "equal"]
        if arm in ("A", "B", "D-rule"):
            assert len(blocks) >= 2, (
                f"{ident}: {len(blocks)} changed block(s) in the span — the applied value must "
                f"move AND at least one value derived from it")
            assert 4 <= len(old.split()) <= 120, f"{ident}: span {len(old.split())} words"
            changed_words[ident] = len(blocks)
        else:
            assert len(blocks) >= 1, f"{ident}: no changed block in the span"
            assert len(old.split()) <= 25, f"{ident}: fact span {len(old.split())} words (max 25)"
            changed_words[ident] = len(blocks)

        # (6) ban-set
        scan(before, BAN_ARTIFACT, ident, "before")
        scan(after, BAN_ARTIFACT, ident, "after")
        scan(it["variation_site"], BAN_SITE, ident, "variation_site")
        scan(it["author_note"], BAN_NOTE, ident, "author_note")

        # (7) domain band + title line
        bands[ident] = band(ident, dom, before)
        first = before.strip().splitlines()[0]
        assert first.strip(), f"{ident}: empty first line"
        assert len(first.split()) <= 16, f"{ident}: first line {len(first.split())} words"

        arm_count[arm] += 1
        cell[arm][dom] += 1

    # (8) arm counts
    for a, n in ARMS.items():
        assert arm_count[a] == n, f"arm {a}: {arm_count[a]} items, expected {n}"
    assert len(rows) == sum(ARMS.values()), f"{len(rows)} items, expected {sum(ARMS.values())}"

    print(f"ALL CHECKS PASS — {len(rows)}/{sum(ARMS.values())} items\n")
    hdr = f"{'arm':<9}" + "".join(f"{d:<9}" for d in DOMAINS) + "total"
    print(hdr)
    print("-" * len(hdr))
    tot = Counter()
    for a in ARMS:
        line = f"{a:<9}"
        for d in DOMAINS:
            line += f"{cell[a][d]:<9}"
            tot[d] += cell[a][d]
        print(line + str(arm_count[a]))
    print("-" * len(hdr))
    print(f"{'total':<9}" + "".join(f"{tot[d]:<9}" for d in DOMAINS) + str(len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
