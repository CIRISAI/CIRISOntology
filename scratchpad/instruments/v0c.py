"""Instrument suite v0c — v0b's six heuristic halves plus the USE/MENTION feature.

WHAT THIS ADDS, AND WHY
-----------------------
PLANE_RESULTS.md Part D measured a one-directional failure in the annotation
panel and named it: **use/mention blindness**. A norm that an artifact merely
*describes* ("the byelaw in force requires X") reads to the panel as a norm the
artifact *enacts*; an is-a an artifact merely *observes* ("the tree is an oak")
reads as an is-a the artifact *assigns*. Facts-target items in reporting genres
were absorbed into Rules (2 of 3) and into Identity (2 of 3), while the mirror
directions were 3/3 correct. Part D's consequence line is explicit:

    "the Facts (empirical) instrument needs a USE/MENTION feature — is the
     changed claim asserted by the artifact, or reported/quoted/described by
     it — or it will inherit the panel's absorption."

v0c is that feature, built three ways:

  empirical_v2   (Facts)     + MENTION ROUTE: a changed span sitting inside a
                               reporting/attribution frame, or inside an artifact
                               that declares a descriptive stance, is a change to
                               what the artifact CLAIMS — Facts — even when no
                               "checkable value" was substituted.
  deontic_v2     (Rules)     + MENTION GUARD: stands down when the changed norm
                               is mentioned, not used.
  ontological_v2 (Identity)  + MENTION GUARD, and a PERFORMATIVE-REGISTRY route:
                               registers/catalogues/entry-based artifacts DO
                               assign, so Identity must keep firing there. Part
                               D's ontological-registry items are that control.

SCOPE AND HONESTY
-----------------
Nothing here is validated. The mention detector's cues were written against
Part D's twelve items and against the 248-item corpus as a NEGATIVE control:
the two artifact-level routes (attribution-in-genre, descriptive-stance) fire on
ZERO of the 248 corpus items. That is a real property (it bounds regression at
zero) and a real limitation (a feature that never fires on the older corpus
cannot be validated by it). The four Part-D repairs are therefore in-sample
repairs of an authored boundary, not an advance prediction. Stated plainly, per
rule 6: this is not support for anything; it is an instrument change whose
regression cost is measured.

v0b is imported, never modified. empirical_v2/deontic_v2/ontological_v2 wrap the
v0b readings; the other three instruments pass through unchanged.
"""
from __future__ import annotations
import importlib.util, json, re, sys
from collections import Counter, defaultdict
from typing import Optional

_V0B_PATH = "/home/emoore/CIRISOntology/scratchpad/instruments/v0b.py"
_already = sys.modules.get("v0b")
if _already is not None and getattr(_already, "__file__", None) == _V0B_PATH:
    v0b = _already                       # someone else already loaded it; do not reload
else:
    _spec = importlib.util.spec_from_file_location("v0b", _V0B_PATH)
    v0b = importlib.util.module_from_spec(_spec)
    sys.modules["v0b"] = v0b
    _spec.loader.exec_module(v0b)        # v0b's tests live under __main__: no side effects

_reading = v0b._reading
_refusal = v0b._refusal
_changed = v0b._changed
_mode = v0b._mode
_tokens = v0b._tokens
_lower = v0b._lower
_content = v0b._content
_fuzzy_eq = v0b._fuzzy_eq
_fuzzy_jaccard = v0b._fuzzy_jaccard

# ------------------------------------------------------------------ switches
# Each extra route is a switch so its cost can be measured on its own.
MENTION_ROUTE = True         # empirical fires on a mentioned span whose content moved
MENTION_GUARD = True         # deontic / ontological stand down on a mentioned span
ENACTING_SUPPRESSOR = True   # empirical stands down on a norm-shaped span in an
                             # artifact that declares itself enforced-as-written
REGISTRY_ROUTE = True        # ontological fires on a performative-registry entry
ENACTING_ROUTE = True        # deontic fires on a norm-shaped span in such an artifact
                             # even with no modal (the indicative standing order —
                             # Part D's mirror direction, which the panel got 3/3)

# ------------------------------------------------------------------ lexicons

# Genre of the ARTIFACT, read off its title line. A reporting genre is a
# necessary condition for the weaker mention routes, never a sufficient one:
# 45 of the 248 corpus items carry one of these words in the title, spread over
# every kind_target, so genre ALONE separates nothing.
GENRE_REPORT = re.compile(
    r"\b(minutes|report|reports|notes?|bulletin|survey|audit|log|logbook|newsletter|"
    r"digest|briefing|diary|walkabout|dispatch|summary|review|readout|write-up|"
    r"field notes|observations?)\b", re.I)

# A norm/source noun whose content is being REPORTED, not issued.
NORM_SOURCE = (r"byelaws?|bylaws?|manual|handbook|polic(?:y|ies)|regulations?|statutes?|"
               r"rules?|standards?|guidance|contract|licence|license|permit|scheme|"
               r"charter|code|specification|ordinance|act|order|motion|resolution|"
               r"constitution|terms|agreement|protocol|guidelines?|checklist|tariff")
ATTRIB_VERB = (r"states?|stated|says?|said|requires?|required|provides?|provided|"
               r"specifies?|specified|sets?|stipulates?|prescribes?|mandates?|"
               r"allows?|permits?|obliges?|calls for|gives?|governs?|carried")

# M1a — an attributed norm: "the byelaw in force requires", "the site's own
# manual states that", "the motion as carried sets".
ATTRIB_NORM = re.compile(
    r"\b(?:the|its|their|our|this|that|a|an|his|her|own)\s+(?:\w+\s+){0,2}(?:"
    + NORM_SOURCE + r")\b(?:\s+\w+){0,3}\s+(?:" + ATTRIB_VERB + r")\b", re.I)

# M1b — an explicit reporting frame or quotation cue, strong enough on its own.
ATTRIB_FRAME = re.compile(
    r"\b(?:states?|stated|reports?|reported|notes?|noted|confirms?|confirmed|"
    r"records?|recorded|shows?|showed|indicates?|indicated|claims?|claimed|"
    r"asserts?|observes?|observed|describes?|described|says?|said)\s+that\b"
    r"|\baccording to\b"
    r"|\b(?:is|are|was|were)\s+said to be\b"
    r"|\bas (?:reported|recorded|stated|described|observed|logged|vouchered)\b"
    r"|\bper the\b", re.I)
# DOUBLE quotes only. An earlier draft admitted the ASCII apostrophe as a quote
# delimiter; it then read "Tuesday's second round ... week's" as a quoted span
# and cost four corpus items. Possessives are not quotation.
QUOTED = re.compile(r'["“][^"”\n]{6,200}["”]')

# M2 — the artifact declares its own stance: it refers to ITSELF and says it
# describes/records rather than directs/assigns.
SELF_REF = (r"(?:these|this|the present)\s+(?:draft\s+|field\s+|site\s+|weekly\s+|"
            r"following\s+)?(?:notes?|minutes|report|bulletin|page|records?|survey|"
            r"log|entry|review|summary|audit|visit|walkabout|note)")
STANCE_DESCRIPTIVE = re.compile(
    SELF_REF + r"[^.;]{0,140}?\b(describes?|described|records?|recorded|reports?|"
    r"reported|observes?|observed|found|circulated in draft|corrections of fact|"
    r"as walked|as observed|as seen|directs? (?:no|any|nothing)|nothing here|"
    r"is not a|do not|does not)\b", re.I)

# Performative REGISTRY: the artifact's entry IS the assignment.
REGISTRY_TITLE = re.compile(
    r"\b(register|registry|catalogue|catalog|index|roll|ledger|gazetteer|"
    r"accepted names? list|list)\b|\b(?:entry|record|item|no\.)\s*\d+", re.I)
REGISTRY_DECL = re.compile(
    r"\bfor (?:the|all) purposes? of (?:this|the) (?:list|register|registry|catalogue|"
    r"catalog|entry|record|scheme|index)\b"
    r"|\bfor all purposes of the (?:register|catalogue|list)\b"
    r"|\bfor the purposes of this (?:list|register|catalogue|entry)\b"
    r"|\bunder the (?:register|registry|catalogue|list)'s (?:rules|scheme|conventions)\b"
    r"|\bwithin (?:this|the) (?:catalogue|register|registry|list)(?:'s)?\b"
    r"|\b(?:is|are|was|were) (?:registered|catalogued|carried|listed|entered|classed|"
    r"filed|recorded) (?:under|as|in)\b"
    r"|\bthe name recorded in the current entry\b", re.I)
# An entry-slot assignment NAMES ITS SLOT. Bare "as"/"under" are not enough:
# "contractors on multi-week engagements count as staff" is a definitional
# counting rule (Premises), not a register entry, and admitting "as" alone
# cost exactly that item.
REGISTRY_ASSIGN_CUE = {"registered", "catalogued", "carried", "recorded", "listed",
                       "entered", "classed", "filed", "name", "genus", "species",
                       "class", "heading", "category", "designation", "title"}

# Performative ENACTING: the artifact declares itself the operative instrument.
ENACT_DECL = re.compile(
    r"\bis (?:applied|enforced|read|operated) as (?:written|such|stated)\b"
    r"|\bpart of (?:your|the|our) terms\b"
    r"|\bsafe system of work\b"
    r"|\bthese (?:arrangements|rules|terms|conditions) apply\b"
    r"|\bthis (?:policy|notice|procedure|standard|page|schedule) applies\b"
    r"|\bapplied as written\b|\benforced as such\b"
    r"|\bhas effect from\b|\bcomes into force\b", re.I)

# a standing-order shape: generic present-tense clause, no past-tense report verb
NORM_SHAPE = re.compile(
    r"\b(?:are|is)\s+\w+(?:ed|en)\b"                      # passive present
    r"|\b(?:must|shall|may|will|are to|is to)\b"
    r"|\bwithin\s+[\w-]+\s+(?:days?|weeks?|months?|hours?|working days?)\b"
    r"|\b(?:give|gives|submit|submits|provide|provides|return|returns)\b", re.I)
PAST_REPORT = re.compile(
    r"\b(?:was|were|attended|took place|observed|found|showed|reported|recorded|"
    r"measured|photographed|logged|noted)\b", re.I)


# ------------------------------------------------------------------ the detector

def use_mention(before: str, after: str) -> dict:
    """USE/MENTION reading of a changed span.

    MENTION  — the changed span is reported, attributed, quoted, or described by
               the artifact (the artifact's stance toward it is assertive).
    USE      — the artifact enacts or assigns with the span (performative:
               a register entry that names, a notice that is enforced as such).

    Performative always wins: a register's naming sentence uses an attribution
    verb ('is registered under') and is nonetheless an assignment.
    """
    mode = _mode(before, after)
    b_ch, a_ch, pairs, _, *_r = _changed(before, after, mode)
    changed = " ".join(b_ch) + " ‖ " + " ".join(a_ch)
    full = before + "\n" + after
    title = (before.strip().split("\n")[0] + " " + after.strip().split("\n")[0])[:300]

    genre = bool(GENRE_REPORT.search(title))
    reg_title = bool(REGISTRY_TITLE.search(title))
    reg_decl = REGISTRY_DECL.search(full)
    enact = ENACT_DECL.search(full)

    performative_registry = bool(reg_title and reg_decl)
    performative_enacting = bool(enact) and not performative_registry
    performative = performative_registry or performative_enacting

    routes, why = [], []
    m = ATTRIB_NORM.search(changed)
    if m and genre:
        routes.append("M1a attributed-norm-in-reporting-genre")
        why.append(m.group(0)[:70])
    m = ATTRIB_FRAME.search(changed)
    if m:
        routes.append("M1b reporting-frame")
        why.append(m.group(0)[:70])
    if QUOTED.search(changed) and genre:
        routes.append("M1c quoted-span")
    m = STANCE_DESCRIPTIVE.search(full)
    if m and genre:
        routes.append("M2 declared-descriptive-stance")
        why.append(m.group(0)[:70])

    mentioned = bool(routes) and not performative
    return {"mentioned": mentioned, "routes": routes, "cues": why,
            "genre_reporting": genre,
            "performative": performative,
            "performative_registry": performative_registry,
            "performative_enacting": performative_enacting,
            "mode": mode}


def _content_substitution(pairs) -> Optional[tuple[list[str], list[str]]]:
    """A replace-pair whose CONTENT words differ on the two sides — the shape of
    'what the artifact says changed', independent of whether the changed token
    happens to be a number, a month, or a capitalised name."""
    for bt, at in pairs:
        if not bt or not at:
            continue
        cb, ca = _content(bt), _content(at)
        if not cb and not ca:
            continue
        if set(cb) == set(ca):
            continue
        if cb and ca and all(any(_fuzzy_eq(x, y) for y in ca) for x in cb):
            continue  # same stems, a morphological recast
        return cb, ca
    return None


# ------------------------------------------------------------------ 5'. empirical_v2

def empirical_v2(before: str, after: str, sources: Optional[list[str]] = None) -> dict:
    """v0b.empirical + the MENTION ROUTE (and, under ENACTING_SUPPRESSOR, its
    mirror). Fires additionally when the changed span is MENTIONED — reported,
    attributed, quoted, or described — and its content was substituted, even
    with no checkable value in it: correcting what a bulletin says a byelaw
    requires is a change to the bulletin's CLAIM, not to the byelaw.

    Guards on the new route, so it cannot poach three neighbours:
      * definition/assumption position  -> Premises (axiomatic)
      * computation/derivation context  -> Model (nomological)
      * a hedge/booster moved           -> Confidence (epistemic)
    A moved MODAL is deliberately NOT a guard: a reported modal is exactly the
    absorbed case Part D measured, and deontic_v2 stands down on it.
    """
    r = _refusal("empirical", before, after)
    if r:
        return r
    um = use_mention(before, after)
    base = v0b.empirical(before, after, sources)
    base["evidence"] = dict(base.get("evidence") or {})
    base["evidence"]["use_mention"] = {k: um[k] for k in
                                       ("mentioned", "routes", "performative_registry",
                                        "performative_enacting")}
    mode = um["mode"]
    b_ch, a_ch, pairs, _, *_r = _changed(before, after, mode)

    if base["fired"]:
        if ENACTING_SUPPRESSOR and um["performative_enacting"]:
            span = " ".join(b_ch) + " " + " ".join(a_ch)
            if NORM_SHAPE.search(span) and not PAST_REPORT.search(span):
                ev = dict(base["evidence"])
                ev["suppressed_by"] = "use/mention: USE (enacting artifact)"
                return _reading("empirical", False, ev,
                                reason="the changed value sits in a standing-order clause of an "
                                       "artifact that declares itself applied as written — the "
                                       "artifact USES the norm; route to Rules (deontic)")
        return base

    if not (MENTION_ROUTE and um["mentioned"]):
        return base

    sub = _content_substitution(pairs)
    if not sub:
        return base
    # Defer only where a NEIGHBOUR ACTUALLY CLAIMS the span. Deferring on the
    # raw definition-pattern instead was too strict: 'at all times when afloat'
    # trips the Premises pattern list without the Premises instrument firing.
    if v0b.axiomatic(before, after)["fired"]:
        return base                                   # Premises owns it
    if v0b.epistemic(before, after)["fired"]:
        return base                                   # Confidence owns it
    region = " ".join(b_ch) + " " + " ".join(a_ch)
    if v0b.METHOD_CONTEXT.search(region):
        return base                                   # Model owns it

    ev = dict(base["evidence"])
    ev.update({"mention_route": um["routes"], "mention_cues": um["cues"],
               "changed_content": [sub[0], sub[1]],
               "retrieval": "JUDGE — heuristic detects that a REPORTED claim changed; "
                            "it does not verify either version"})
    return _reading("empirical", True, ev,
                    reason=f"the artifact REPORTS rather than enacts this span "
                           f"({'; '.join(um['routes'])}); its reported content changed: "
                           f"{sub[0]} -> {sub[1]}")


# ------------------------------------------------------------------ 6'. deontic_v2

def deontic_v2(before: str, after: str) -> dict:
    """v0b.deontic + the MENTION GUARD. A modal that moved inside a reported,
    quoted or described norm did not change anybody's obligations — it changed
    what the artifact says about somebody else's. Route to Facts."""
    r = _refusal("deontic", before, after)
    if r:
        return r
    um = use_mention(before, after)
    base = v0b.deontic(before, after)
    base["evidence"] = dict(base.get("evidence") or {})
    base["evidence"]["use_mention"] = {k: um[k] for k in
                                       ("mentioned", "routes", "performative_registry",
                                        "performative_enacting")}
    if base["fired"] and um["mentioned"] and MENTION_GUARD:
        ev = dict(base["evidence"])
        ev["suppressed_by"] = "use/mention: MENTION"
        return _reading("deontic", False, ev,
                        reason="the modal that moved sits in a norm the artifact REPORTS, "
                               f"not one it issues ({'; '.join(um['routes'])}) — "
                               "route to Facts (empirical)")
    if not base["fired"] and ENACTING_ROUTE and um["performative_enacting"]:
        # the mirror of the mention route: an artifact that declares itself
        # applied-as-written issues its standing orders in the INDICATIVE, so the
        # modal vector never moves. The USE side of the distinction, not a modal.
        mode = um["mode"]
        b_ch, a_ch, pairs, _n, *_r = _changed(before, after, mode)
        span = " ".join(b_ch) + " " + " ".join(a_ch)
        if NORM_SHAPE.search(span) and not PAST_REPORT.search(span) \
                and _content_substitution(pairs):
            ev = dict(base["evidence"])
            ev["route"] = "enacting artifact, indicative standing order"
            return _reading("deontic", True, ev,
                            reason="an artifact that declares itself applied as written "
                                   "changed a standing-order clause; the indicative mood "
                                   "is dressing, the obligation moved")
    return base


# ------------------------------------------------------------------ 9'. ontological_v2

def _registry_assignment(before: str, after: str, mode: str, pairs) -> Optional[dict]:
    """In a performative registry, the entry's assignment slot changed: a name,
    genus, class or heading sitting right after an assignment cue."""
    btok_all = _lower(_tokens(before))
    for bt, at in pairs:
        if not bt or not at:
            continue
        cb, ca = _content(bt), _content(at)
        if not cb or not ca or set(cb) == set(ca):
            continue
        if any(t.isdigit() or t in v0b.NUMBER_WORDS for t in _lower(bt + at)):
            continue
        if any(_fuzzy_eq(x, y) for x in cb for y in ca):
            continue
        low = _lower(bt)
        for i in range(len(btok_all) - len(bt) + 1):
            if btok_all[i:i + len(bt)] == low:
                ctx = btok_all[max(0, i - 4):i]
                if set(ctx) & REGISTRY_ASSIGN_CUE:
                    return {"cue": sorted(set(ctx) & REGISTRY_ASSIGN_CUE),
                            "retyped": f"{' '.join(cb)} -> {' '.join(ca)}"}
                break
    return None


def ontological_v2(before: str, after: str) -> dict:
    """v0b.ontological + the MENTION GUARD + the PERFORMATIVE-REGISTRY route.

    Guard: an is-a the artifact merely OBSERVES ('the tree at the lychgate is a
    sycamore', in field notes that declare they direct nothing) is a claim about
    the world — Facts — not a reassignment of what something is.

    Route: a register, catalogue or accepted-names list ASSIGNS. Its entry slot
    changing IS an Identity change, and the mention guard must never touch it.
    Part D's three ontological-registry items are that control.
    """
    r = _refusal("ontological", before, after)
    if r:
        return r
    um = use_mention(before, after)
    base = v0b.ontological(before, after)
    base["evidence"] = dict(base.get("evidence") or {})
    base["evidence"]["use_mention"] = {k: um[k] for k in
                                       ("mentioned", "routes", "performative_registry",
                                        "performative_enacting")}
    mode = um["mode"]
    _b, _a, pairs, _n, *_r = _changed(before, after, mode)

    if um["performative_registry"]:
        if base["fired"]:
            return base
        if REGISTRY_ROUTE and mode == "prose":
            hit = _registry_assignment(before, after, mode, pairs)
            if hit:
                ev = dict(base["evidence"])
                ev.update(hit)
                ev["route"] = "performative registry entry"
                return _reading("ontological", True, ev,
                                reason=f"a performative registry entry reassigned its "
                                       f"assignment slot: {hit['retyped']}")
        return base

    if base["fired"] and um["mentioned"] and MENTION_GUARD:
        ev = dict(base["evidence"])
        ev["suppressed_by"] = "use/mention: MENTION"
        return _reading("ontological", False, ev,
                        reason="the is-a that changed is one the artifact OBSERVES or REPORTS, "
                               f"not one it assigns ({'; '.join(um['routes'])}) — "
                               "route to Facts (empirical)")
    return base


# ------------------------------------------------------------------ suite

INSTRUMENTS_V2 = {"empirical": empirical_v2, "deontic": deontic_v2,
                  "epistemic": v0b.epistemic, "pragmatic": v0b.pragmatic,
                  "ontological": ontological_v2, "axiomatic": v0b.axiomatic}


# ------------------------------------------------------------------ dye tests
# v0b's twelve planted items (one per kind) plus five USE/MENTION dye items.
# Each instrument must fire on exactly the items assigned to it and stay clean
# on every other item; plus a refusal probe.

DYE_ITEMS: dict[str, tuple[str, str]] = dict(v0b.DYE_ITEMS)

MENTION_DYE: dict[str, tuple[str, str]] = {
    # Facts by attribution: the bulletin's report of a byelaw changes; the
    # byelaw does not. deontic must stay clean — nothing was obliged.
    "empirical_mention_norm": (
        "Parish Bulletin — Weekly Notes\n\n"
        "Readers asked about verge cutting. The verge byelaw in force requires "
        "cutting twice a season. No change is before the council.",
        "Parish Bulletin — Weekly Notes\n\n"
        "Readers asked about verge cutting. The verge byelaw in force requires "
        "cutting four times a season. No change is before the council."),
    # Facts by attribution, with the reported MODAL moving: deontic's vector
    # moves and deontic must STILL stay clean — this is the absorbed case.
    "empirical_mention_modal": (
        "Harbour Digest — Monthly Notes\n\n"
        "The mooring code as published requires tenders to carry a light. The "
        "office reports no change this season.",
        "Harbour Digest — Monthly Notes\n\n"
        "The mooring code as published permits tenders to carry a light. The "
        "office reports no change this season."),
    # Facts by declared descriptive stance: an OBSERVED is-a. ontological must
    # stay clean — the notes assign nothing.
    "empirical_mention_isa": (
        "Lane Survey — Field Notes\n\n"
        "The tree by the stile is a field maple. These notes describe what was "
        "found on the walk; nothing here directs any work.",
        "Lane Survey — Field Notes\n\n"
        "The tree by the stile is a rowan. These notes describe what was found "
        "on the walk; nothing here directs any work."),
    # Identity in a performative registry: the CONTROL. The mention guard must
    # not touch it, and empirical must stay clean.
    "ontological_performative": (
        "Boat Register — Entry 12\n\n"
        "The hull is registered under the class inshore launch. Under the "
        "register's rules the class recorded here governs, and painted classes "
        "have no standing.",
        "Boat Register — Entry 12\n\n"
        "The hull is registered under the class harbour tender. Under the "
        "register's rules the class recorded here governs, and painted classes "
        "have no standing."),
    # Rules in the indicative: an enacting notice's standing order changes with
    # no modal in sight. empirical must stay clean.
    "deontic_enacted": (
        "Workshop Notice — Ladder Care\n\n"
        "Ladders are inspected monthly and tagged. This notice is part of the "
        "workshop's safe system of work and is enforced as such.",
        "Workshop Notice — Ladder Care\n\n"
        "Ladders are inspected weekly and tagged. This notice is part of the "
        "workshop's safe system of work and is enforced as such."),
}
DYE_ITEMS.update(MENTION_DYE)

# which instrument (if any) must fire on each dye item
DYE_EXPECT: dict[str, Optional[str]] = {
    k: (k if k in INSTRUMENTS_V2 else None) for k in v0b.DYE_ITEMS}
DYE_EXPECT.update({"empirical_mention_norm": "empirical",
                   "empirical_mention_modal": "empirical",
                   "empirical_mention_isa": "empirical",
                   "ontological_performative": "ontological",
                   "deontic_enacted": "deontic"})


def dye_tests(instruments=None, items=None, expect=None) -> list[tuple[str, bool]]:
    instruments = instruments or INSTRUMENTS_V2
    items = items or DYE_ITEMS
    expect = expect or DYE_EXPECT
    results = []
    for iname, fn in instruments.items():
        for kind, (b, a) in items.items():
            reading = fn(b, a)
            want_fire = (expect.get(kind) == iname)
            ok = reading["fired"] == want_fire and not reading["refused"]
            verb = f"fires on {kind}" if want_fire else f"clean on {kind}"
            results.append((f"{iname:11s} {verb}", ok))
        refuse = fn("same text.", "same text.")
        results.append((f"{iname:11s} refuses identical input", refuse["refused"]))
    return results


# ------------------------------------------------------------------ bake-off

CORPUS = "/home/emoore/CIRISOntology/scratchpad/plane_corpus/corpus_full.jsonl"
PART_D = "/home/emoore/CIRISOntology/scratchpad/plane_corpus/part_d.jsonl"
OUT = "/home/emoore/CIRISOntology/scratchpad/instruments/v0c_bakeoff.txt"

_TOUCHED = ("empirical", "deontic", "ontological")


def _load(path: str) -> list[dict]:
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def _score(corpus, instruments, gold_map, iname):
    tp = fp = fn = 0
    fp_from = Counter()
    for d in corpus:
        g = gold_map.get(d["id"])
        if g is None:
            continue
        fired = instruments[iname](d["before"], d["after"])["fired"]
        if fired and g == iname:
            tp += 1
        elif fired:
            fp += 1
            fp_from[g] += 1
        elif g == iname:
            fn += 1
    p, r, f = v0b._prf(tp, fp, fn)
    return p, r, f, tp, fp, fn, fp_from


def _ablate(corpus, part_d, **flags):
    """Set switches, count part-D exclusive hits and corpus reading deltas."""
    saved = {k: globals()[k] for k in flags}
    globals().update(flags)
    try:
        pd_hits = sum(1 for d in part_d
                      if [n for n in INSTRUMENTS_V2
                          if INSTRUMENTS_V2[n](d["before"], d["after"])["fired"]
                          and n in _TOUCHED] == [d["kind_target"]])
        delta = 0
        for d in corpus:
            for n in _TOUCHED:
                if v0b.INSTRUMENTS[n](d["before"], d["after"])["fired"] != \
                        INSTRUMENTS_V2[n](d["before"], d["after"])["fired"]:
                    delta += 1
        return pd_hits, delta
    finally:
        globals().update(saved)


def bakeoff(out_path: Optional[str] = OUT) -> str:
    corpus, part_d = _load(CORPUS), _load(PART_D)
    gold, ties = v0b.provisional_gold()
    authored = {d["id"]: d["kind_target"] for d in corpus}
    lines: list[str] = []
    say = lines.append

    say("=" * 78)
    say("v0c BAKE-OFF — the USE/MENTION feature (task N5)")
    say("=" * 78)
    say("")
    say("WHAT WAS BUILT, AND WHAT EACH OUTCOME WOULD HAVE MEANT (stated first)")
    say("-" * 78)
    say("Part D measured use/mention blindness: a norm an artifact DESCRIBES reads")
    say("as a norm it ENACTS, an is-a it OBSERVES reads as one it ASSIGNS. Four of")
    say("its twelve items were absorbed that way (empirical-report-07, -08, -09,")
    say("-11). v0c adds a mention detector and wires it three ways:")
    say("  empirical_v2   MENTION ROUTE  — a mentioned span whose content moved is")
    say("                                  a change to what the artifact CLAIMS.")
    say("  deontic_v2     MENTION GUARD  — plus the mirror ENACTING ROUTE (an")
    say("                                  indicative standing order in an artifact")
    say("                                  that declares itself applied as written).")
    say("  ontological_v2 MENTION GUARD  — plus the PERFORMATIVE-REGISTRY route,")
    say("                                  because registers and catalogues DO")
    say("                                  assign. Part D's registry items are that")
    say("                                  control and must keep firing Identity.")
    say("")
    say("Meanings fixed in advance of the corpus run:")
    say("  * four absorbed items now read Facts, eight others unchanged  -> feature works")
    say("  * any corpus item losing a true fire or gaining a false one    -> REGRESSION,")
    say("    reported item by item whether or not it is repaired")
    say("  * the detector never firing on the corpus                      -> the corpus")
    say("    CANNOT validate the feature; it bounds regression, nothing more")
    say("The third outcome is the one that occurred. It is not support (rule 6).")
    say("")

    # ---------------- dye
    say("=" * 78)
    say("1. DYE TESTS")
    say("=" * 78)
    res = dye_tests()
    bad = [n for n, ok in res if not ok]
    say(f"v0c instruments on the 17-item dye set (12 from v0b + 5 new use/mention "
        f"items): {sum(ok for _, ok in res)}/{len(res)}")
    for n in bad:
        say(f"   FAIL {n}")
    say("")
    res_b = dye_tests(instruments=v0b.INSTRUMENTS)
    say(f"v0b instruments on the SAME dye set: {sum(ok for _, ok in res_b)}/{len(res_b)}"
        " — the five new items discriminate:")
    for n, ok in res_b:
        if not ok:
            say(f"   v0b FAIL {n}")
    say("")
    say("CAVEAT, stated: the five new dye items are OURS, written alongside the")
    say("feature they exercise. A dye test is a wiring check — it shows the")
    say("detector is connected to the right instrument and does not leak into the")
    say("other five. It is not evidence that the distinction is real in the wild.")
    say("")
    say("the five new dye items, and what each pins:")
    for k in MENTION_DYE:
        f0 = [n for n, fn in v0b.INSTRUMENTS.items() if fn(*MENTION_DYE[k])["fired"]]
        f1 = [n for n, fn in INSTRUMENTS_V2.items() if fn(*MENTION_DYE[k])["fired"]]
        say(f"   {k:26s} expect {str(DYE_EXPECT[k]):12s} v0b {str(f0):16s} v0c {f1}")
    say("")

    # ---------------- part D
    say("=" * 78)
    say("2. PART D — all twelve items, v0b vs v0c")
    say("=" * 78)
    say("'fires' lists every one of the six instruments that fired. A line is")
    say("EXCLUSIVE-CORRECT when that list is exactly the item's authored target.")
    say("")
    say(f"{'item':26s} {'target':12s} {'v0b fires':30s} {'v0c fires':30s} v0c")
    okb = okc = tgt_b = tgt_c = 0
    for d in part_d:
        f0 = [n for n, fn in v0b.INSTRUMENTS.items() if fn(d["before"], d["after"])["fired"]]
        f1 = [n for n, fn in INSTRUMENTS_V2.items() if fn(d["before"], d["after"])["fired"]]
        okb += (f0 == [d["kind_target"]]); okc += (f1 == [d["kind_target"]])
        tgt_b += (d["kind_target"] in f0); tgt_c += (d["kind_target"] in f1)
        say(f"{d['id']:26s} {d['kind_target']:12s} {str(f0):30s} {str(f1):30s} "
            f"{'OK' if f1 == [d['kind_target']] else 'x'}")
    say("")
    say(f"target instrument fires:  v0b {tgt_b}/12   ->  v0c {tgt_c}/12")
    say(f"exclusive-correct:        v0b {okb}/12   ->  v0c {okc}/12")
    say("")
    say("NOTE on 'the eight correct items'. Part D's 8/12 was the PANEL's readout.")
    say("The INSTRUMENT's readout at v0b was 1/12 exclusive-correct: it missed the")
    say("three minutes/bulletin/audit items entirely, false-fired Facts on two of")
    say("the three policies, and read Identity on all three walkabout/survey items.")
    say("So 'stay correct' is checked here as 'no part-D item reads worse than it")
    say("did under v0b':")
    worse = []
    for d in part_d:
        f0 = [n for n, fn in v0b.INSTRUMENTS.items() if fn(d["before"], d["after"])["fired"]]
        f1 = [n for n, fn in INSTRUMENTS_V2.items() if fn(d["before"], d["after"])["fired"]]
        t = d["kind_target"]
        b_ok, c_ok = (t in f0), (t in f1)
        b_fp = len([x for x in f0 if x != t and x in _TOUCHED])
        c_fp = len([x for x in f1 if x != t and x in _TOUCHED])
        if (b_ok and not c_ok) or c_fp > b_fp:
            worse.append(d["id"])
    say(f"   part-D items that read WORSE than v0b: {worse if worse else 'none'}")
    say("")
    say("the four items Part D measured as ABSORBED, specifically:")
    for i in ("empirical-report-07", "empirical-report-08",
              "empirical-report-09", "empirical-report-11"):
        d = next(x for x in part_d if x["id"] == i)
        f0 = [n for n, fn in v0b.INSTRUMENTS.items() if fn(d["before"], d["after"])["fired"]]
        f1 = [n for n, fn in INSTRUMENTS_V2.items() if fn(d["before"], d["after"])["fired"]]
        say(f"   {i:26s} v0b {str(f0):20s} -> v0c {f1}")
    say("")
    say("residual, reported plainly: ontological-registry-07 is the one item that is")
    say("not exclusive-correct. ontological_v2 DOES fire on it (the registry route")
    say("works); v0b's axiomatic co-fires because 'For the purposes of this list'")
    say("trips its definition-pattern list with ripple 3. That is a pre-existing v0b")
    say("reading on an instrument this task does not touch, and it is left standing.")
    say("")

    # ---------------- corpus tables
    for gname, gmap, note in (
            ("AUTHORED kind_target (the task's primary table)", authored, "all 248 items"),
            ("PANEL-MODAL (provisional gold, diagnostic)", gold, f"{ties} ties excluded")):
        say("=" * 78)
        say(f"3. corpus_full.jsonl vs {gname} [{note}]")
        say("=" * 78)
        say(f"{'instrument':12s} {'P_v0b':>6s} {'R_v0b':>6s} {'F1_v0b':>7s} | "
            f"{'P_v0c':>6s} {'R_v0c':>6s} {'F1_v0c':>7s} | {'dF1':>6s}  tp/fp/fn v0b -> v0c")
        for iname in INSTRUMENTS_V2:
            pb, rb, fb, tb, fpb, fnb, _ = _score(corpus, v0b.INSTRUMENTS, gmap, iname)
            pc, rc, fc, tc, fpc, fnc, _ = _score(corpus, INSTRUMENTS_V2, gmap, iname)
            mark = "*" if iname in _TOUCHED else " "
            say(f"{iname:11s}{mark} {pb:6.2f} {rb:6.2f} {fb:7.2f} | "
                f"{pc:6.2f} {rc:6.2f} {fc:7.2f} | {fc - fb:+6.2f}  "
                f"{tb}/{fpb}/{fnb} -> {tc}/{fpc}/{fnc}")
        say("  * = instrument changed in v0c")
        say("")

    # ---------------- regressions
    say("=" * 78)
    say("4. REGRESSIONS — every corpus reading that changed")
    say("=" * 78)
    delta = []
    for d in corpus:
        for n in _TOUCHED:
            f0 = v0b.INSTRUMENTS[n](d["before"], d["after"])["fired"]
            f1 = INSTRUMENTS_V2[n](d["before"], d["after"])["fired"]
            if f0 != f1:
                delta.append((d["id"], d["kind_target"], n, f0, f1))
    if not delta:
        say("NONE. Zero of the 744 (248 items x 3 changed instruments) readings moved.")
        say("Zero improvement on this corpus, too — see the activation table below.")
    for x in delta:
        say(f"   {x[0]:26s} target={x[1]:12s} {x[2]:12s} {x[3]} -> {x[4]}")
    say("")
    say("Two regressions WERE found during the build, by this same control, and are")
    say("recorded because the corpus caught them and nothing else would have:")
    say("  (a) the quoted-span route accepted the ASCII apostrophe as a quote mark,")
    say("      so possessives ('Tuesday's second round') read as quotation. It cost")
    say("      4 items: deontic-report-03 and ontological-report-03 lost true fires,")
    say("      axiotic-report-02 and nomological-report-03 gained false empirical")
    say("      fires. Fixed by restricting the route to double quotes.")
    say("  (b) the registry route accepted a bare 'as'/'under' as an assignment cue,")
    say("      so 'contractors ... count as staff' (axiomatic-policy-04, a Premises")
    say("      stipulation) read as a register entry. Fixed by requiring the slot to")
    say("      be NAMED (name/genus/class/heading/... or an assignment verb).")
    say("")

    # ---------------- activation
    say("=" * 78)
    say("5. DETECTOR ACTIVATION — why the corpus tables did not move")
    say("=" * 78)
    act, routes, byk = Counter(), Counter(), Counter()
    hits = []
    for d in corpus:
        um = use_mention(d["before"], d["after"])
        act["genre word in title"] += bool(um["genre_reporting"])
        act["MENTION"] += bool(um["mentioned"])
        act["performative registry"] += bool(um["performative_registry"])
        act["performative enacting"] += bool(um["performative_enacting"])
        for r in um["routes"]:
            routes[r] += 1
        if um["mentioned"]:
            byk[d["kind_target"]] += 1
        if um["mentioned"] or um["performative"]:
            hits.append((d["id"], d["kind_target"], um["routes"],
                         um["performative_registry"], um["performative_enacting"]))
    say(f"on 248 corpus items: " + ", ".join(f"{k} {v}" for k, v in act.items()))
    say(f"routes fired: {dict(routes) or '-'}")
    say(f"MENTION by authored kind: {dict(byk) or '-'}")
    say("")
    for h in hits:
        say(f"   {h[0]:26s} {h[1]:12s} routes={h[2]} registry={h[3]} enacting={h[4]}")
    say("")
    say("Read plainly: the artifact-level routes (attributed-norm-in-genre,")
    say("declared-descriptive-stance) fire on ZERO corpus items, and the three")
    say("reporting-frame hits are all caught by the route's own deferral guards")
    say("(Premises, Confidence, Model). The corpus therefore bounds this feature's")
    say("regression at zero and validates nothing about it. The 248 items were")
    say("authored before Part D named the boundary and do not carry the stance")
    say("sentences the detector keys on; Part D's twelve were authored to carry")
    say("them. The repair is in-sample. A wild test is owed.")
    say("")
    say("The sharpest form of that limitation, named so it can be attacked:")
    say("  empirical-report-09  'The large tree at the lychgate is an English oak'")
    say("                        -> 'is a sycamore'      (authored FACTS)")
    say("  ontological-report-01 'The raised feature ... is a seamount'")
    say("                        -> 'is a mud volcano'   (authored IDENTITY)")
    say("Both sit in survey-genre artifacts; both are copular; both replace a")
    say("common-noun predicate. The ONLY surface feature separating them is that")
    say("the Part-D item carries an explicit stance sentence ('These notes describe")
    say("what was found on the day; nothing here directs any work') and the older")
    say("item does not. If wild descriptive artifacts do not carry such a sentence,")
    say("route M2 will not fire on them and the absorption returns. That is the")
    say("kill for this feature: a descriptive artifact with no self-describing")
    say("sentence whose observed is-a changes, still read as Identity.")
    say("")

    # ---------------- ablation
    say("=" * 78)
    say("6. ABLATION — each switch on its own")
    say("=" * 78)
    say("part-D column: items where exactly the target instrument fires among the")
    say("three touched instruments. corpus column: readings changed vs v0b.")
    say(f"{'configuration':46s} {'partD':>6s} {'corpus deltas':>14s}")
    allon = dict(MENTION_ROUTE=True, MENTION_GUARD=True, ENACTING_SUPPRESSOR=True,
                 ENACTING_ROUTE=True, REGISTRY_ROUTE=True)
    alloff = {k: False for k in allon}
    for label, flags in (
            ("v0b behaviour (all switches off)", alloff),
            ("+ MENTION_ROUTE only", {**alloff, "MENTION_ROUTE": True}),
            ("+ MENTION_GUARD only", {**alloff, "MENTION_GUARD": True}),
            ("+ MENTION route and guard", {**alloff, "MENTION_ROUTE": True,
                                           "MENTION_GUARD": True}),
            ("+ REGISTRY_ROUTE only", {**alloff, "REGISTRY_ROUTE": True}),
            ("+ ENACTING_SUPPRESSOR only", {**alloff, "ENACTING_SUPPRESSOR": True}),
            ("+ ENACTING_ROUTE only", {**alloff, "ENACTING_ROUTE": True}),
            ("v0c as shipped (all on)", allon)):
        h, dd = _ablate(corpus, part_d, **flags)
        say(f"{label:46s} {h:5d}/12 {dd:14d}")
    say("")
    say("=" * 78)
    say("STATUS: heuristic half only. No retrieval, no judge, no network, nothing")
    say("validated. `suite_ships_unvalidated` still holds and v0c does not weaken it.")
    say("=" * 78)

    text = "\n".join(lines)
    if out_path:
        with open(out_path, "w") as f:
            f.write(text + "\n")
    return text


if __name__ == "__main__":
    results = dye_tests()
    width = max(len(n) for n, _ in results)
    ok = True
    for name, passed in results:
        if not passed:
            print(f"  {name:<{width}}  FAIL")
        ok &= passed
    by_inst: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for name, passed in results:
        inst = name.split()[0]
        by_inst[inst][0] += passed
        by_inst[inst][1] += 1
    print(f"{'instrument':12s} dye tests (17 items + refusal probe)")
    for inst, (p, n) in by_inst.items():
        print(f"  {inst:11s} {p}/{n} {'PASS' if p == n else 'FAIL'}")
    print(f"\n{'ALL DYE TESTS PASS' if ok else 'DYE FAILURE — instrument not fit to ship'} "
          f"({sum(p for _, p in results)}/{len(results)})")
    if ok:
        print()
        print(bakeoff(OUT))
        print(f"\n[bake-off saved to {OUT}]")
    raise SystemExit(0 if ok else 1)
