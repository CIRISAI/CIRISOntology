#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mechanical self-check for the T5 corpus.

Reads scratchpad/T5/t5_items.jsonl and scratchpad/T5/t5_tagnull.jsonl and checks them
against RECOGNITION_PREREG.md section T5.4 (item form, two gloss conventions, attestation),
RECOGNITION_PREREG_A2.md BLOCKER-7 (one pair per evidential value per language), MAJOR-12
(the tag-null control) and MAJOR-13 (per-item citation), and RECOGNITION_PREREG_A3.md
(surviving instances). Exits non-zero on the first failure class found; prints a report.
"""
import json, os, re, sys

BASE = "/home/emoore/CIRISOntology/scratchpad/T5"
ITEMS_F = os.path.join(BASE, "t5_items.jsonl")
TAGNULL_F = os.path.join(BASE, "t5_tagnull.jsonl")

# --- the standing ban-set, copied verbatim from plane_corpus/_helper.py ------
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

# --- linguistic meta-vocabulary, banned in ARTIFACT TEXT ONLY ----------------
# (the category_preamble is licensed to use these; that is its job)
_META = [
    r"\bevidential(s|ity)?\b", r"\baspect(s|ual)?\b", r"\bperfective\b", r"\bimperfective\b",
    r"\boptative\b", r"\binjunctive\b", r"\bmirative(s)?\b", r"\bmirativity\b",
    r"\begophoric(ity)?\b", r"\bconjunct\b", r"\bdisjunct\b", r"\bhonorific(s)?\b",
    r"\bclassifier(s)?\b", r"\bswitch-reference\b", r"\bdefiniteness\b",
    r"\bmiddle voice\b", r"\bactive voice\b", r"\bassociated motion\b",
    r"\bmorpheme(s)?\b", r"\bsuffix(es)?\b", r"\bprefix(es)?\b", r"\baffix(es)?\b",
    r"\benclitic(s)?\b", r"\binflect(ed|ion|ional)?\b", r"\bgrammar\b", r"\bgrammatical(ly)?\b",
    r"\bclause(s)?\b", r"\bverb(s|al)?\b", r"\bnoun(s)?\b", r"\bpronoun(s)?\b",
    r"\bparticle(s)?\b", r"\bparadigm(s)?\b", r"\bdeixis\b", r"\bdeictic\b",
    r"\bpast tense\b", r"\bpresent tense\b", r"\bsecond person\b", r"\bfirst person\b",
    r"\bthird person\b", r"\bevidence marker\b", r"\bmarker(s)?\b",
]

KIND_NAMES = ["priorit", "rule", "manner", "identit", "confidence", "fact", "circumstance",
              "process", "model", "structure", "premise", "record"]

TAG_VOCAB = {
    "evidentiality":            ("EVID",   {"visual", "nonvisual", "apparent", "secondhand",
                                            "assumed", "direct", "reportative", "conjectural",
                                            "indirect"}),
    "perfective/imperfective":  ("ASPECT", {"bounded", "unbounded"}),
    "optative":                 ("MOOD",   {"statement", "wish"}),
    "middle voice":             ("VOICE",  {"active", "middle"}),
    "numeral classifiers":      ("CLF",    {"long-thin", "chunk", "small-animal",
                                            "large-animal", "animate", "inanimate"}),
    "egophoricity":             ("EGO",    {"self", "other"}),
    "switch-reference":         ("REF",    {"same-subject", "different-subject"}),
    "honorifics":               ("HON",    {"plain", "exalted"}),
    "mirativity":               ("MIR",    {"expected", "surprise"}),
    "associated motion":        ("MOTION", {"go-and-do", "come-and-do", "do-while-going"}),
    "definiteness":             ("DEF",    {"definite", "indefinite"}),
}

# --- the surviving (row -> language -> expected pair count) inventory --------
# T5_ATTEST section 2.4 lenient reading + A3.1 substitutes + A3.7 (Cupeno dropped);
# row 1 is per-value per BLOCKER-7.
EXPECTED = {
    1:  {"Tuyuca": 5, "Cuzco Quechua": 3, "Turkish": 2},
    2:  {"Russian": 1, "Mandarin": 1},
    3:  {"Georgian": 1, "Ancient Greek": 1},
    4:  {"Classical Greek": 1, "Fula": 1},
    7:  {"Mandarin": 1, "Japanese": 1, "Yucatec": 1},
    8:  {"Kathmandu Newar": 1, "Akhvakh": 1, "Tsafiki": 1},
    9:  {"Amele": 1, "Choctaw": 1, "Diyari": 1},
    11: {"Japanese": 1, "Korean": 1},
    12: {"Turkish": 1, "Hare": 1, "Magar": 1},
    13: {"Arrernte": 1, "Cavinena": 1},
    14: {"Arabic (Modern Standard)": 1, "Hungarian": 1},
}
ROW1_VALUES = {
    "Tuyuca":        {"visual", "nonvisual", "apparent", "secondhand", "assumed"},
    "Cuzco Quechua": {"direct", "reportative", "conjectural"},
    "Turkish":       {"direct", "indirect"},
}
ROW_CATEGORY = {1: "evidentiality", 2: "perfective/imperfective", 3: "optative",
                4: "middle voice", 7: "numeral classifiers", 8: "egophoricity",
                9: "switch-reference", 11: "honorifics", 12: "mirativity",
                13: "associated motion", 14: "definiteness"}

TAG_RE = re.compile(r"\[[A-Z]+:[a-z-]+\]")
FAILS = []


def fail(ident, msg):
    FAILS.append("%s: %s" % (ident, msg))


def scan(text, pats, ident, where):
    for p in pats:
        m = re.search(p, text, re.I)
        if m:
            fail(ident, "banned term %r in %s" % (m.group(0), where))


def scan_meta(text, ident, where):
    """Linguistic meta-vocabulary is banned in the SENTENCE WORDING only.

    The bracketed tag is not sentence wording -- naming its own category is the whole
    job of the tag, exactly as it is the whole job of the category_preamble -- so the
    tag span is removed before this scan. The tag is still covered by the _VOCAB /
    _VALENCE scan and by the separate kind-name check.
    """
    scan(TAG_RE.sub(" ", text), _META, ident, where)


def sentences(text):
    # strip the bracketed tag first so its colon/brackets cannot be miscounted
    t = TAG_RE.sub("X", text)
    return [s for s in re.split(r"[.!?]+(?:\s|$)", t) if s.strip()]


def load(path):
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def check_items(items):
    ids = [it["id"] for it in items]
    if len(set(ids)) != len(ids):
        fail("CORPUS", "duplicate ids")
    if len(items) != 34:
        fail("CORPUS", "expected 34 pairs, found %d" % len(items))

    seen = {}
    preambles = {}
    for it in items:
        i = it["id"]
        row, cat, lang = it["row"], it["category"], it["language"]

        # --- row/category/language inventory ---------------------------------
        if ROW_CATEGORY.get(row) != cat:
            fail(i, "row %s does not carry category %r" % (row, cat))
        seen.setdefault(row, {}).setdefault(lang, 0)
        seen[row][lang] += 1

        # --- citation --------------------------------------------------------
        if not it.get("citation") or len(it["citation"].strip()) < 40:
            fail(i, "citation missing or too short to name a primary")

        # --- row 1 carries a value, every other row does not ------------------
        if row == 1:
            if it["value"] not in ROW1_VALUES.get(lang, set()):
                fail(i, "value %r not in the verified inventory for %s" % (it["value"], lang))
        elif it["value"] is not None:
            fail(i, "value must be null outside row 1")

        # --- tags -------------------------------------------------------------
        prefix, vocab = TAG_VOCAB[cat]
        for t, w in ((it["tag_before"], "tag_before"), (it["tag_after"], "tag_after")):
            m = re.fullmatch(r"\[([A-Z]+):([a-z-]+)\]", t)
            if not m:
                fail(i, "%s %r is not a well-formed tag" % (w, t)); continue
            if m.group(1) != prefix:
                fail(i, "%s prefix %r is not the category's %r" % (w, m.group(1), prefix))
            if m.group(2) not in vocab:
                fail(i, "%s value %r outside the declared vocabulary" % (w, m.group(2)))
            for kn in KIND_NAMES:
                if kn in t.lower():
                    fail(i, "%s carries kind name %r" % (w, kn))
        if it["tag_before"] == it["tag_after"]:
            fail(i, "GLOSS-T tag does not move")

        # --- GLOSS-T: byte-identical except the tag span -----------------------
        tb, ta = it["glossT_before"], it["glossT_after"]
        for t, w in ((tb, "glossT_before"), (ta, "glossT_after")):
            n = len(TAG_RE.findall(t))
            if n != 1:
                fail(i, "%s carries %d bracketed tags, want exactly 1" % (w, n))
        if TAG_RE.findall(tb) and TAG_RE.findall(tb)[0] != it["tag_before"]:
            fail(i, "glossT_before's tag is not tag_before")
        if TAG_RE.findall(ta) and TAG_RE.findall(ta)[0] != it["tag_after"]:
            fail(i, "glossT_after's tag is not tag_after")
        if tb.replace(it["tag_before"], it["tag_after"], 1) != ta:
            fail(i, "GLOSS-T before/after differ outside the tag span")

        # --- GLOSS-N: differs, and carries no tag ------------------------------
        nb, na = it["glossN_before"], it["glossN_after"]
        if nb == na:
            fail(i, "GLOSS-N before/after are identical")
        for t, w in ((nb, "glossN_before"), (na, "glossN_after")):
            if TAG_RE.search(t):
                fail(i, "%s carries a bracketed tag" % w)

        # --- ban scans ---------------------------------------------------------
        for t, w in ((nb, "glossN_before"), (na, "glossN_after"),
                     (tb, "glossT_before"), (ta, "glossT_after")):
            scan(t, _VOCAB + _VALENCE, i, w)
            scan_meta(t, i, w)
            ns = len(sentences(t))
            if not (2 <= ns <= 5):
                fail(i, "%s has %d sentences, want 2-5" % (w, ns))
        scan(it["variation_site"], _VOCAB + _VALENCE, i, "variation_site")
        if len(sentences(it["variation_site"])) != 1:
            fail(i, "variation_site must be one sentence")

        # --- preamble identity per category -------------------------------------
        preambles.setdefault(cat, set()).add(it["category_preamble"])

    for cat, ps in preambles.items():
        if len(ps) != 1:
            fail("CATEGORY %s" % cat, "%d distinct preambles, want 1" % len(ps))
    allp = [next(iter(ps)) for ps in preambles.values()]
    if len(set(allp)) != len(allp):
        fail("CORPUS", "two categories share a preamble")

    if seen != EXPECTED:
        for row in sorted(set(list(seen) + list(EXPECTED))):
            if seen.get(row) != EXPECTED.get(row):
                fail("ROW %s" % row, "instances %r != expected %r"
                     % (seen.get(row), EXPECTED.get(row)))

    # row 1 value coverage
    for lang, vals in ROW1_VALUES.items():
        got = {it["value"] for it in items if it["row"] == 1 and it["language"] == lang}
        if got != vals:
            fail("ROW 1 %s" % lang, "values %r != inventory %r" % (sorted(got), sorted(vals)))

    # no two pairs may be byte-inverses of each other under either convention: a
    # panel that sees A->B and B->A on one text is being shown the same item twice.
    for a in range(len(items)):
        for b in range(a + 1, len(items)):
            x, y = items[a], items[b]
            for lo, hi in (("glossT_before", "glossT_after"),
                           ("glossN_before", "glossN_after")):
                if x[lo] == y[hi] and x[hi] == y[lo]:
                    fail(x["id"], "is the byte-inverse of %s under %s"
                         % (y["id"], lo.split("_")[0]))


def check_tagnull(tn, items):
    if len(tn) != 12:
        fail("TAGNULL", "expected 12 items, found %d" % len(tn))
    ids = [t["id"] for t in tn]
    if len(set(ids)) != len(ids):
        fail("TAGNULL", "duplicate ids")

    grid = {}
    main_texts = set()
    for it in items:
        main_texts.update([it["glossT_before"], it["glossT_after"],
                           it["glossN_before"], it["glossN_after"]])

    for t in tn:
        i = t["id"]
        if t["row"] not in (1, 7):
            fail(i, "tag-null is registered for rows 1 and 7 only")
        if ROW_CATEGORY.get(t["row"]) != t["category"]:
            fail(i, "row/category mismatch")
        if t["pair_type"] not in ("alpha", "beta"):
            fail(i, "pair_type %r" % t["pair_type"])
        grid.setdefault((t["row"], t["language"]), set()).add(t["pair_type"])

        before, after = t["before"], t["after"]
        prefix, vocab = TAG_VOCAB[t["category"]]
        for x, w in ((before, "before"), (after, "after")):
            tags = TAG_RE.findall(x)
            if len(tags) != 1:
                fail(i, "%s carries %d bracketed tags, want exactly 1" % (w, len(tags)))
            elif not tags[0].startswith("[" + prefix + ":"):
                fail(i, "%s tag %r is not the category's prefix" % (w, tags[0]))
            elif tags[0][len(prefix) + 2:-1] not in vocab:
                fail(i, "%s tag value outside the declared vocabulary" % w)
            scan(x, _VOCAB + _VALENCE, i, w)
            scan_meta(x, i, w)
            ns = len(sentences(x))
            if not (2 <= ns <= 5):
                fail(i, "%s has %d sentences, want 2-5" % (w, ns))
            if x in main_texts:
                fail(i, "%s duplicates a main-corpus text" % w)
        scan(t["variation_site"], _VOCAB + _VALENCE, i, "variation_site")

        tb, ta = t["tag_before"], t["tag_after"]
        if t["pair_type"] == "alpha":
            if tb != ta:
                fail(i, "alpha must hold the tag")
            if TAG_RE.findall(before) != TAG_RE.findall(after):
                fail(i, "alpha's tag is not byte-identical across before/after")
            if before == after:
                fail(i, "alpha's surrounding text does not differ")
        else:
            if tb == ta:
                fail(i, "beta must move the tag")
            if before.replace(tb, ta, 1) != after:
                fail(i, "beta differs outside the tag span")

    for row in (1, 7):
        langs = {k[1] for k in grid if k[0] == row}
        if len(langs) != 3:
            fail("TAGNULL row %d" % row, "%d languages, want 3 (%r)" % (len(langs), sorted(langs)))
    for k, types in grid.items():
        if types != {"alpha", "beta"}:
            fail("TAGNULL %r" % (k,), "pair types %r, want both" % sorted(types))

    # tag-null languages must be languages the row actually survives with
    for (row, lang) in grid:
        if lang not in EXPECTED.get(row, {}):
            fail("TAGNULL %s row %d" % (lang, row), "not a surviving instance of the row")


def selftest():
    """Positive control: the scanners must actually fire on planted violations."""
    global FAILS
    keep, FAILS = FAILS, []
    scan("the standing rules of the yard", _VOCAB + _VALENCE, "SELFTEST", "x")
    scan("this was the wrong shelf", _VOCAB + _VALENCE, "SELFTEST", "x")
    scan_meta("the evidential is obligatory here", "SELFTEST", "x")
    scan_meta("[EVID:visual] the bell rang twice", "SELFTEST", "x")  # tag span exempt
    fired = len(FAILS)
    FAILS = keep
    if fired != 3:
        fail("SELFTEST", "planted violations fired %d times, want 3" % fired)
    if len(sentences("One. Two [EVID:visual]. Three.")) != 3:
        fail("SELFTEST", "sentence counter miscounts around a tag")


def main():
    items = load(ITEMS_F)
    tn = load(TAGNULL_F)
    selftest()
    check_items(items)
    check_tagnull(tn, items)

    print("t5_items.jsonl      : %d pairs" % len(items))
    print("t5_tagnull.jsonl    : %d tag-null items" % len(tn))
    print("rows                : %s" % sorted({it["row"] for it in items}))
    print("categories          : %d" % len({it["category"] for it in items}))
    print("languages           : %d" % len({(it["row"], it["language"]) for it in items}))
    print("row 1 pairs by value: %s" % sorted(
        (it["language"], it["value"]) for it in items if it["row"] == 1))
    if FAILS:
        print("\nFAIL (%d):" % len(FAILS))
        for f in FAILS:
            print("  - " + f)
        sys.exit(1)
    print("\nALL CHECKS PASS")


if __name__ == "__main__":
    main()
