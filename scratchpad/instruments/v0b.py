"""Instrument suite v0b — the six hybrid instruments' HEURISTIC HALVES, executable.

Companions to v0.py (structure, process, circumstances, record). This file adds
the heuristic halves of instruments 5-10 from INSTRUMENT_SUITE_DESIGN.md:

    empirical (Facts)        claim-extraction diff; retrieval is the JUDGE's job
    deontic (Rules)          modal/permission class-vector diff over the changed span
    epistemic (Confidence)   hedge/certainty lexicon diff with claim-content guard
    pragmatic (Manner)       register shift with the meaning-skeleton held invariant
    ontological (Identity)   is-a / type-assertion diff
    axiomatic (Premises)     definition-position + COMPUTED RIPPLE (downstream
                             dependency count) — the measured reason panels absorb
                             Premises into Facts is that nobody computes the ripple

Interface: each instrument is a function (before_text, after_text, ...) -> Reading
dict {kind, fired, evidence, refused, reason}. REFUSED is first-class (identical
or empty input: nothing to read), never an error.

Shared discriminator: every instrument diffs the two texts and reads only the
CHANGED sentences/lines. A document that merely contains "must" somewhere is not
a Rules change; only a modal that sits in the changed region can be.

v0b scope, stated: heuristic halves only. No retrieval, no judges, no network.
Nothing here is validated and the Lean pins that (`suite_ships_unvalidated`).
The bake-off below scores against PROVISIONAL gold (panel modal label, BASE
condition) — panel-modal is NOT a human ceiling and validates nothing.
"""
from __future__ import annotations
import difflib, json, re
from collections import Counter, defaultdict
from typing import Optional

# ---------------------------------------------------------------- shared plumbing

STOPWORDS = set("""a an the and or but if then than that this these those it its is are was
were be been being am do does did done has have had having will would should could of in
on at by for with to from as into onto over under about against between during before
after above below up down out off again further once here there when where why how all
any both each few more most other some such no nor not only own same so too very s t can
just don now we our ours you your yours he him his she her hers they them their theirs i
me my mine what which who whom while per via also within without upon toward towards
""".split())

NUMBER_WORDS = set("""zero one two three four five six seven eight nine ten eleven twelve
thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty
sixty seventy eighty ninety hundred thousand million billion half quarter dozen
""".split())

MONTHS = set("""january february march april may june july august september october
november december jan feb mar apr jun jul aug sep sept oct nov dec""".split())

_WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_'-]*|\d+(?:[.,:]\d+)*|\S")
_NUM = re.compile(r"\d+(?:[.,:]\d+)*")


def _tokens(text: str) -> list[str]:
    return _WORD.findall(text)


def _lower(toks: list[str]) -> list[str]:
    return [t.lower() for t in toks]


def _is_config(text: str) -> bool:
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines:
        return False
    kv = sum(1 for l in lines
             if re.match(r"""^\s*["']?[#\w.-]+["']?\s*:""", l)
             or l.strip().startswith(("- ", "#", "{", "}")))
    return kv >= max(3, 0.6 * len(lines))


def _is_code(text: str) -> bool:
    return bool(re.search(r"^\s*(def |class |import |from \w+ import |return |[A-Z_]+\s*=)", text, re.M))


def _mode(before: str, after: str) -> str:
    """prose | config | code — config checked first (yaml/json keys beat '=' hits)."""
    joined = before + "\n" + after
    if _is_config(joined):
        return "config"
    if _is_code(joined):
        return "code"
    return "prose"


def _segments(text: str, mode: str) -> list[str]:
    """Sentences for prose (title lines kept as their own segments), lines otherwise."""
    if mode != "prose":
        return [l for l in text.splitlines() if l.strip()]
    segs = []
    for chunk in text.split("\n"):
        chunk = chunk.strip()
        if not chunk:
            continue
        segs.extend(s.strip() for s in re.split(r"(?<=[.!?;])\s+", chunk) if s.strip())
    return segs


def _changed(before: str, after: str, mode: str):
    """Diff at token level, mapped back to segments. Returns
    (before_changed_segs, after_changed_segs, replace_pairs, n_regions,
     bsegs, asegs, b_changed_idx, a_changed_idx)."""
    bsegs, asegs = _segments(before, mode), _segments(after, mode)
    btoks, bmap = [], []
    for i, s in enumerate(bsegs):
        for t in _tokens(s):
            btoks.append(t); bmap.append(i)
    atoks, amap = [], []
    for i, s in enumerate(asegs):
        for t in _tokens(s):
            atoks.append(t); amap.append(i)
    sm = difflib.SequenceMatcher(None, btoks, atoks, autojunk=False)
    bidx, aidx, pairs, regions = set(), set(), [], 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        regions += 1
        bidx.update(bmap[i] for i in range(i1, i2))
        aidx.update(amap[j] for j in range(j1, j2))
        pairs.append((btoks[i1:i2], atoks[j1:j2]))
    b_changed = [bsegs[i] for i in sorted(bidx)]
    a_changed = [asegs[i] for i in sorted(aidx)]
    return b_changed, a_changed, pairs, regions, bsegs, asegs, sorted(bidx), sorted(aidx)


def _fuzzy_eq(a: str, b: str) -> bool:
    """Morphology-tolerant token match: equal, or common 4-char prefix."""
    if a == b:
        return True
    return len(a) >= 4 and len(b) >= 4 and a[:4] == b[:4]


def _content(toks: list[str]) -> list[str]:
    return [t for t in _lower(toks) if t.isalpha() and t not in STOPWORDS and len(t) > 1]


def _fuzzy_jaccard(a: list[str], b: list[str]) -> float:
    """Greedy fuzzy set overlap; 1.0 for two empty lists (nothing to disagree on)."""
    aa, bb = list(dict.fromkeys(a)), list(dict.fromkeys(b))
    if not aa and not bb:
        return 1.0
    matched = 0
    used = [False] * len(bb)
    for x in aa:
        for k, y in enumerate(bb):
            if not used[k] and _fuzzy_eq(x, y):
                used[k] = True; matched += 1
                break
    return matched / (len(aa) + len(bb) - matched)


def _config_key(line: str) -> Optional[str]:
    m = re.match(r"""^\s*["']?([\w.-]+)["']?\s*:""", line)
    return m.group(1) if m else None


def _parent_keys(segs: list[str], idx: int) -> list[str]:
    """Ancestor config keys of segs[idx] by indentation (yaml-style)."""
    def indent(s):
        return len(s) - len(s.lstrip())
    keys, level = [], indent(segs[idx])
    for j in range(idx - 1, -1, -1):
        ij = indent(segs[j])
        if ij < level or (ij == level and segs[idx].lstrip().startswith("-")):
            k = _config_key(segs[j])
            if k:
                keys.append(k)
                level = ij
                if ij == 0:
                    break
    return keys


def _enclosing_def(segs: list[str], idx: int) -> Optional[str]:
    """Name of the enclosing python def for segs[idx], if any."""
    def indent(s):
        return len(s) - len(s.lstrip())
    level = indent(segs[idx])
    for j in range(idx - 1, -1, -1):
        m = re.match(r"^(\s*)def\s+(\w+)", segs[j])
        if m and len(m.group(1)) < level:
            return m.group(2)
    return None


def _reading(kind: str, fired: bool, evidence: dict, refused: bool = False,
             reason: str = "") -> dict:
    return {"kind": kind, "fired": fired, "evidence": evidence,
            "refused": refused, "reason": reason}


def _refusal(kind: str, before: str, after: str) -> Optional[dict]:
    if not before.strip():
        return _reading(kind, False, {}, refused=True, reason="empty BEFORE — no baseline")
    if before == after:
        return _reading(kind, False, {}, refused=True, reason="texts identical — no change to classify")
    return None


# ---------------------------------------------------------------- lexicons

OBLIGATION = {"must", "shall", "required", "require", "requires", "mandatory",
              "obliged", "obligated", "binding", "compulsory"}
PERMISSION = {"may", "might", "permitted", "allowed", "optional", "discretionary",
              "encouraged", "voluntary"}
PROHIBITION = {"prohibited", "forbidden", "banned", "barred", "disallowed",
               "prohibits", "forbids"}
PERMISSION_STRICT = PERMISSION - {"may", "might"}  # no epistemic double life
# "shall" + event verb is legal futurity, not an obligation; "May I" is politeness
LEGALESE_SHALL = re.compile(
    r"\bshall\s+(commence|begin|start|apply|take|become|remain|expire|cease|end|be\s+deemed)\b")
POLITE_MAY = re.compile(r"\bmay\s+(i|we)\b", re.I)
# permission-structure identifiers (APPROVER_ROLES, user.scopes, signoffs_needed...)
NORM_IDENT = re.compile(
    r"(approv|permit|permiss|allow|deny|grant|acl\b|authoriz|authoris|privileg|forbid|"
    r"prohibit|access|scope|signoff|sign_off)", re.I)
SCOPE_TOGGLE = {"only", "unless", "except", "solely"}

HEDGE = {"may", "might", "could", "suggest", "suggests", "suggested", "likely",
         "probably", "possibly", "appears", "appear", "apparently", "preliminary",
         "provisional", "provisionally", "tentative", "tentatively", "estimated",
         "estimate", "estimates", "rough", "roughly", "indicative", "believe",
         "believed", "uncertain", "unconfirmed", "approximate", "approximately",
         "presumably", "perhaps", "arguably", "seems", "seemingly", "unverified"}
BOOSTER = {"establish", "establishes", "established", "confirm", "confirms",
           "confirmed", "definitely", "certainly", "certain", "conclusive",
           "conclusively", "demonstrates", "demonstrate", "demonstrated", "proves",
           "prove", "proven", "definitive", "definitively", "dependable", "reliable",
           "verified", "clearly", "undoubtedly", "unambiguous", "unambiguously",
           "decisive", "decisively", "final", "exact", "exactly", "precise",
           "precisely"}
HEDGE_PHRASES = [re.compile(p) for p in
                 (r"\bconsistent with\b", r"\bwe believe\b", r"\bit is possible\b",
                  r"\bcannot be ruled out\b", r"\bpoints? towards?\b")]
BOOSTER_PHRASES = [re.compile(p) for p in
                   (r"\bstrongly indicate\b", r"\bno doubt\b", r"\bbeyond question\b")]
EPISTEMIC_KEY = re.compile(r"(reliab|confid|certain|trust|verif|confirm|corrobor|evidence)", re.I)

POLITENESS = {"please", "kindly", "hereby", "aforementioned", "herein", "thereof",
              "pursuant", "undersigned", "henceforth", "forthwith", "aforesaid",
              "advised", "notified", "heretofore", "thereto", "herewith"}
GREETINGS = {"dear", "hello", "hi", "hey", "greetings", "everyone", "folks"}
SECOND_PERSON = {"you", "your", "yours", "yourself", "yourselves"}
CONTRACTIONS = re.compile(
    r"\b(don't|won't|can't|isn't|aren't|wasn't|weren't|doesn't|didn't|hasn't|haven't|"
    r"couldn't|shouldn't|wouldn't|we'll|we're|we've|you're|you'll|you've|they're|"
    r"they'll|it'll|let's|i'm|that's|there's|what's)\b", re.I)
FORMAL_PLAIN = {"commence": "start", "commences": "starts", "commencement": "start",
                "terminate": "end", "terminates": "ends", "utilise": "use",
                "utilize": "use", "purchase": "buy", "endeavour": "try",
                "endeavor": "try", "prior": "before", "subsequent": "after",
                "sufficient": "enough", "assistance": "help", "regarding": "about",
                "concerning": "about", "notify": "tell", "notification": "notice",
                "synchronised": "sync", "synchronisation": "sync",
                "synchronized": "sync", "synchronization": "sync",
                "requirement": "need", "obtain": "get", "receive": "get",
                "depart": "leave", "departure": "leave", "individuals": "people",
                "persons": "people", "additional": "more", "remainder": "rest",
                "attempt": "try", "complete": "finished", "ceased": "stopped",
                "operating": "up"}
COLLOQUIAL = [re.compile(p) for p in
              (r"\bgave up\b", r"\bok\b", r"\bokay\b", r"\bpretty much\b",
               r"\bsort of\b", r"\bkind of\b", r"\ba lot\b")]
NOTICE_FRAME = re.compile(
    r"\b(tenants|residents|staff|users|employees|customers|members|applicants|you)\s+"
    r"(?:is|are)\s+(?:hereby\s+)?(?:advised|notified|informed|reminded|requested)\s+that\b",
    re.I)
PASSIVE = re.compile(r"\b(?:is|are|was|were|be|been|being)\s+\w+(?:ed|en)\b")
MANNER_KEY = re.compile(r"(style|format|template|greeting|salutation|layout|tone|wording)$", re.I)

COPULA = {"is", "are", "was", "were", "remains", "remain", "becomes", "become",
          "constitutes", "constitute"}
COPULA_PHRASES = [re.compile(p) for p in
                  (r"\bclassified as\b", r"\btreated as\b", r"\bconsidered (?:a|an|to be)\b",
                   r"\bregarded as\b", r"\breclassified as\b")]
TYPE_KEY_PARTS = {"role", "type", "kind", "class", "category", "classification",
                  "canonical", "environment"}
APPOSITIVE_CUE = {"is", "are", "was", "were", "as", ",", "remains", "becomes",
                  "considered", "classified", "treated"}

# 'basis'/'assum*' are WEAK cues: inside a derivation ('computed on a straight-
# line basis', 'extrapolated assuming...') they are Model-speak, not a premise
WEAK_DEFN = re.compile(r"^(basis|assum)", re.I)
DEFN_PATTERNS = [re.compile(p, re.I) for p in (
    r"\bdefined as\b", r"\btaken (?:as|to be)\b", r"\bcounted (?:in|as|from)\b",
    r"\bcounts? (?:as|from)\b", r"\bstarts? from\b", r"\bstart from\b",
    r"\bstated against\b", r"\bstated per\b", r"\bmeasured against\b",
    r"\bread against\b", r"\bcompared against\b", r"\bbenchmark\b",
    r"\breference (?:year|point|period|date|frame)\b",
    r"\bbasis\b", r"\bbaseline\b", r"\bwe assume\b", r"\bassum(?:e|es|ed|ing|ption)s?\b",
    r"\bstipulat\w*\b", r"\bday zero\b", r"\beverything below\b",
    r"\ball\b[^.]{0,60}\brelative to\b",
    r"\bstarting (?:state|point|position|footing)\b",
    r"\bat tick zero\b", r"\btime basis\b",
    r"\ball (?:times|timestamps|dates|durations|comparisons|schedules|quantities|figures|amounts|values)\b",
    r"\bfor (?:the )?purposes? of\b", r"\bdowntime covers\b", r"\bcounting unit\b",
    r"\bworked example\b", r"\bthroughout\b", r"\bper batch of\b",
    r"\b(?:fall|falls|divided|grouped|sorted|split) into\b",
    r"\binto (?:two|three|four|five|six|\d+) (?:classes|categories|groups|tiers|bands|types|kinds|phases|stages)\b",
    r"\bin (?:two|three|four|five|six|\d+) (?:phases|stages|classes|categories|tiers|bands)\b")]
SCOPE_VERBS = {"includes", "include", "included", "excludes", "exclude", "excluded",
               "covers", "cover", "covered"}
CODE_CONST = re.compile(r"^\s*([A-Z][A-Z0-9_]{2,})\s*=")
BASIS_KEYS = {"units", "system", "currency", "frame", "coordinates", "coordinate",
              "epoch", "base", "basis", "baseline", "reference", "week_starts",
              "timezone", "calendar", "origin", "environments", "initial",
              "start_state", "defaults"}
TIME_BASIS = re.compile(r"\b(utc|local(?: site)? time|timezone|time zone|wall.?clock)\b", re.I)
TIME_USER = re.compile(r"\b(ts|time|timestamp|hour|date|now|second|minute|clock)\w*\b")

METHOD_CONTEXT = re.compile(
    r"\b(calculat|comput|deriv|formul|method|algorithm|model|scoring|scored|assessed|"
    r"depreciat|percentile|weighted|extrapolat|mean\(|stdev|threshold table|egress table)\w*", re.I)
CIRCUMSTANCE_CONTEXT = re.compile(
    r"\b(room|hall|venue|held (?:in|at|on)|scheduled|takes place|meeting on|"
    r"for example|e\.g\.|example|such as|office|offices|branch)\b", re.I)
CODE_ID = re.compile(r"\b[A-Z]{1,5}-\d{2,}\b")
CORROBORATION = {"observer", "observers", "reading", "readings", "confirmation",
                 "confirmations", "witness", "witnesses", "reviewer", "reviewers",
                 "quorum", "sources", "checks"}
PROCESS_COUNT = {"pass", "passes", "wave", "waves", "stage", "stages", "phase",
                 "phases", "round", "rounds", "step", "steps"}


def _modal_vector(sentences: list[str]) -> Counter:
    """Obligation/permission/prohibition class counts over a changed region.
    Legalese-shall and politeness-may are struck before counting."""
    text = " ".join(sentences)
    text = LEGALESE_SHALL.sub(" ", text)
    text = POLITE_MAY.sub(" ", text)
    v = Counter()
    for t in _lower(_tokens(text)):
        if t in OBLIGATION:
            v["obligation"] += 1
        elif t in PERMISSION:
            v["permission"] += 1
        elif t in PROHIBITION:
            v["prohibition"] += 1
    return v


def _modal_vector_strict(sentences: list[str]) -> Counter:
    """As above but may/might excluded — the epistemic instrument's guard."""
    text = LEGALESE_SHALL.sub(" ", " ".join(sentences))
    v = Counter()
    for t in _lower(_tokens(text)):
        if t in OBLIGATION:
            v["obligation"] += 1
        elif t in PERMISSION_STRICT:
            v["permission"] += 1
        elif t in PROHIBITION:
            v["prohibition"] += 1
    return v


def _certainty_vector(sentences: list[str]) -> Counter:
    text = " ".join(sentences).lower()
    v = Counter()
    for p in HEDGE_PHRASES:
        n = len(p.findall(text))
        v["hedge"] += n
        text = p.sub(" ", text)
    for p in BOOSTER_PHRASES:
        n = len(p.findall(text))
        v["booster"] += n
        text = p.sub(" ", text)
    for t in _lower(_tokens(text)):
        if t in HEDGE:
            v["hedge"] += 1
        elif t in BOOSTER:
            v["booster"] += 1
    return v


def _values(toks: list[str], mode: str) -> Counter:
    """Checkable-value tokens, lowercased: digits, number words, capitalised
    months, code ids, and (prose) mid-span capitalised names."""
    vals = Counter()
    low = _lower(toks)
    for i, (t, lt) in enumerate(zip(toks, low)):
        if _NUM.fullmatch(t):
            vals[t] += 1
        elif lt in NUMBER_WORDS or (
                "-" in lt and all(p in NUMBER_WORDS for p in lt.split("-") if p)):
            vals[lt] += 1  # 'forty' and 'twenty-five' alike
        elif lt in MONTHS and t[:1].isupper():
            # 'May' the month needs a nearby day/year; never 'may' the modal
            near = toks[max(0, i - 2):i + 3]
            if any(_NUM.fullmatch(x) for x in near):
                vals[lt] += 1
        elif CODE_ID.fullmatch(t):
            vals[t.lower()] += 1
        elif (mode == "prose" and i > 0 and t[:1].isupper() and lt not in STOPWORDS
              and t.isalpha() and len(t) > 2):
            vals[lt] += 1
    return vals


def _is_definitional(sentences: list[str], mode: str,
                     pairs: Optional[list] = None,
                     parent_chain: Optional[list[str]] = None) -> tuple[bool, str]:
    """Does the changed region sit in a definition/assumption position?"""
    text = " ".join(sentences)
    for p in DEFN_PATTERNS:
        m = p.search(text)
        if m:
            if WEAK_DEFN.match(m.group(0)) and METHOD_CONTEXT.search(text):
                continue  # 'basis'/'assuming' inside a derivation is Model-speak
            return True, f"pattern '{m.group(0)}'"
    if pairs:
        # a scope stipulation flipped in place: includes <-> excludes/covers
        for bt, at in pairs:
            bs, as_ = set(_lower(bt)) & SCOPE_VERBS, set(_lower(at)) & SCOPE_VERBS
            if bs and as_ and bs != as_:
                return True, f"scope stipulation {sorted(bs)} -> {sorted(as_)}"
    if mode == "code":
        for s in sentences:
            m = CODE_CONST.match(s)
            if not m:
                continue
            name = m.group(1)
            if NORM_IDENT.search(name):
                continue  # APPROVER_ROLES and kin: a permission structure (Rules)
            if re.search(r"(NEEDED|REQUIRED|MATCHES|CONFIRM|QUORUM)", name):
                continue  # a corroboration/approval threshold, not a basis
            if re.search(r"""=\s*["'][^"']*\d[^"']*[A-Za-z][^"']*["']"""
                         r"""|=\s*["'][^"']*[A-Za-z][^"']*\d[^"']*["']""", s):
                continue  # id-like quoted value (host/tag/stamp): a designator
            return True, f"module constant {name}"
        for s in sentences:
            if s.strip().startswith("#") and TIME_BASIS.search(s) \
                    and re.search(r"\b(all|every|throughout|this module)\b", s, re.I):
                return True, "time-basis comment"
    if mode == "config":
        for s in sentences:
            k = _config_key(s)
            if k and k.lower() in BASIS_KEYS:
                return True, f"basis key '{k}'"
        for k in (parent_chain or []):
            if k.lower() in BASIS_KEYS:
                return True, f"basis block '{k}'"
    return False, ""


# ---------------------------------------------------------------- 5. empirical (Facts)
def empirical(before: str, after: str, sources: Optional[list[str]] = None) -> dict:
    """Claim-extraction diff: fires when a checkable factual VALUE (number, date,
    named entity, measurement) is SUBSTITUTED in a declarative claim. NO retrieval —
    verifying the claim against sources is the judge's job, flagged in evidence.
    Suppressors route definitional changes to Premises, formula changes to Model,
    venue/schedule/example designators to Circumstances, permission counts to
    Rules, corroboration counts to Confidence, and mass re-expression to
    Structure/Manner."""
    r = _refusal("empirical", before, after)
    if r:
        return r
    mode = _mode(before, after)
    b_ch, a_ch, pairs, _, bsegs, asegs, b_idx, a_idx = _changed(before, after, mode)
    blow_full, alow_full = before.lower(), after.lower()

    sub_pairs = []          # replace-pairs where values on BOTH sides differ
    agg_b, agg_a = Counter(), Counter()
    for btoks, atoks in pairs:
        if not btoks or not atoks:
            continue  # value SUBSTITUTION needs both sides; pure add/drop is not it
        bv, av = _values(btoks, mode), _values(atoks, mode)
        # a case-toggled or moved word is not a new value: drop tokens the other
        # FULL text already contains (catches re-groupings and sentence re-splits)
        bv = Counter({k: n for k, n in bv.items() if not (k.isalpha() and k in alow_full)})
        av = Counter({k: n for k, n in av.items() if not (k.isalpha() and k in blow_full)})
        agg_b += bv
        agg_a += av
        if bv and av and bv != av:
            sub_pairs.append((btoks, atoks, sorted((bv - av).elements()),
                              sorted((av - bv).elements())))
    if not sub_pairs:
        return _reading("empirical", False, {"changed_values": [], "retrieval": "JUDGE"},
                        reason="no checkable value substituted in the changed span")
    if agg_b == agg_a:
        return _reading("empirical", False,
                        {"changed_values": [], "suppressed_by": "value permutation",
                         "retrieval": "JUDGE"},
                        reason="values only swapped positions — a re-ordering, not a new claim")
    if len(sub_pairs) >= 3:
        return _reading("empirical", False,
                        {"changed_values": [(p[2], p[3]) for p in sub_pairs],
                         "suppressed_by": "mass re-expression", "retrieval": "JUDGE"},
                        reason=f"{len(sub_pairs)} value regions rewritten at once — a re-presentation, "
                               "not a claim edit; route to Structure/Manner")
    # single-pair percent re-expression (0.42 <-> 42 percent) is Manner
    if len(sub_pairs) == 1:
        b_out, a_out = sub_pairs[0][2], sub_pairs[0][3]
        if len(b_out) == 1 and len(a_out) == 1:
            try:
                x, y = float(b_out[0].replace(",", "")), float(a_out[0].replace(",", ""))
                region = " ".join(sub_pairs[0][0] + sub_pairs[0][1]).lower()
                if x and y and (abs(x / y - 100) < 1e-6 or abs(y / x - 100) < 1e-6) \
                        and ("percent" in region or "%" in region):
                    return _reading("empirical", False,
                                    {"suppressed_by": "unit re-expression", "retrieval": "JUDGE"},
                                    reason="same quantity re-expressed (percent form) — route to Manner")
            except ValueError:
                pass

    region_b, region_a = " ".join(b_ch), " ".join(a_ch)
    region = region_b + " " + region_a
    changed_vals = [(p[2], p[3]) for p in sub_pairs]

    parent_chain = []
    if mode == "config":
        for i in b_idx:
            parent_chain += _parent_keys(bsegs, i)
            k = _config_key(bsegs[i])
            if k:
                parent_chain.append(k)
    defn, why = _is_definitional(b_ch + a_ch, mode, pairs, parent_chain)
    if defn:
        return _reading("empirical", False,
                        {"changed_values": changed_vals, "suppressed_by": why,
                         "retrieval": "JUDGE"},
                        reason="value sits in a definition/assumption position — route to Premises (axiomatic)")
    if mode == "config" and any(NORM_IDENT.search(k) for k in parent_chain):
        return _reading("empirical", False,
                        {"changed_values": changed_vals, "suppressed_by": "permission key",
                         "retrieval": "JUDGE"},
                        reason="value lives under a permission/approval key — route to Rules (deontic)")
    if mode == "config" and any(EPISTEMIC_KEY.search(k) for k in parent_chain):
        return _reading("empirical", False,
                        {"changed_values": changed_vals, "suppressed_by": "confidence key",
                         "retrieval": "JUDGE"},
                        reason="value lives under a confidence/verification key — route to Confidence (epistemic)")
    if METHOD_CONTEXT.search(region):
        return _reading("empirical", False,
                        {"changed_values": changed_vals,
                         "suppressed_by": "method/derivation context", "retrieval": "JUDGE"},
                        reason="value sits inside a computation rule — route to Model (nomological)")

    if mode == "code":
        for seg in b_ch + a_ch:
            if re.search(r"(NEEDED|REQUIRED|MATCHES|CONFIRM|QUORUM|CORROBOR)", seg):
                return _reading("empirical", False,
                                {"changed_values": changed_vals,
                                 "suppressed_by": "corroboration threshold",
                                 "retrieval": "JUDGE"},
                                reason="value is a corroboration/approval threshold — "
                                       "route to Confidence/Rules")

    # classify each substituted value against its whole changed region;
    # fire only if a PLAIN one remains
    def classify(val: str, seg_text: str) -> str:
        if CODE_ID.fullmatch(val.upper()) or CODE_ID.fullmatch(val):
            return "designator"
        toks = _tokens(seg_text)
        low = _lower(toks)
        for i, t in enumerate(low):
            if t != val.lower():
                continue
            near = low[max(0, i - 2):i + 3]
            if any(n in MONTHS for n in near):
                return "date-or-ref"
            if i > 0 and toks[i - 1] in ("#", "day"):
                return "date-or-ref"
            head = low[i + 1:i + 3]
            if any(h in CORROBORATION for h in head):
                return "corroboration-count"
            if any(h in PROCESS_COUNT for h in head):
                return "process-count"
        if val.lower() in MONTHS:
            return "date-or-ref"
        if ":" in val and re.fullmatch(r"\d{1,2}:\d{2}", val):
            return "date-or-ref"
        if val.isdigit() and val in re.sub(
                r"[^\d ]", " ", " ".join(re.findall(r"\d{4}-\d{2}-\d{2}[\w:-]*", seg_text))):
            return "date-or-ref"
        if mode == "config" and val.lower() in seg_text.lower() and re.search(
                r'"[^"]*\d[^"]*[A-Za-z][^"]*"|"[^"]*[A-Za-z][^"]*\d[^"]*"', seg_text):
            return "designator"  # value embedded in an id-like quoted string
        return "plain"

    classes = Counter()
    for btoks, atoks, b_out, a_out in sub_pairs:
        for v in b_out:
            classes[classify(v, region_b)] += 1
        for v in a_out:
            classes[classify(v, region_a)] += 1
    if classes and classes.get("plain", 0) == 0:
        top = classes.most_common(1)[0][0]
        route = {"designator": "Circumstances (contingent)",
                 "date-or-ref": "Circumstances (contingent)",
                 "corroboration-count": "Confidence (epistemic)",
                 "process-count": "Process (procedural)"}[top]
        return _reading("empirical", False,
                        {"changed_values": changed_vals, "suppressed_by": f"all values {top}",
                         "retrieval": "JUDGE"},
                        reason=f"changed values are {top} slots — route to {route}")
    if CIRCUMSTANCE_CONTEXT.search(region_b) and CIRCUMSTANCE_CONTEXT.search(region_a) \
            and not re.search(r"\b(per|total|average|rate|percent|%|mm|kg|km|litre|liter)\b",
                              region, re.I):
        return _reading("empirical", False,
                        {"changed_values": changed_vals,
                         "suppressed_by": "venue/schedule/example context",
                         "retrieval": "JUDGE"},
                        reason="value is a circumstantial designation — route to Circumstances (contingent)")
    return _reading("empirical", True,
                    {"changed_values": changed_vals, "value_classes": dict(classes),
                     "retrieval": "JUDGE — heuristic detects that a factual claim "
                                  "changed; it does NOT verify either version",
                     "sources": sources if sources else "none named"},
                    reason=f"checkable value substituted: {changed_vals[0][0]} -> {changed_vals[0][1]}")


# ---------------------------------------------------------------- 6. deontic (Rules)
def deontic(before: str, after: str) -> dict:
    """Modal/permission class-vector diff over the changed region: fires when the
    change alters what is obliged, permitted, or prohibited. A recast that carries
    the same modal through ('you must return' -> 'must be returned') keeps the
    vector flat and does not fire. Additional heuristics: a scope word (only/
    unless/except) toggling inside a modal-bearing sentence; membership or value
    change inside a permission structure (APPROVER_ROLES, signoffs_needed,
    user.scopes, an allow-function's return)."""
    r = _refusal("deontic", before, after)
    if r:
        return r
    mode = _mode(before, after)
    b_ch, a_ch, pairs, _, bsegs, asegs, b_idx, a_idx = _changed(before, after, mode)
    vb, va = _modal_vector(b_ch), _modal_vector(a_ch)
    if vb != va:
        delta = {k: va.get(k, 0) - vb.get(k, 0) for k in set(vb) | set(va)}
        return _reading("deontic", True,
                        {"modal_vector_before": dict(vb), "modal_vector_after": dict(va),
                         "delta": delta},
                        reason=f"obligation/permission/prohibition balance changed: {delta}")
    if sum(vb.values()):
        st_b = {t for t in _lower(_tokens(" ".join(b_ch))) if t in SCOPE_TOGGLE}
        st_a = {t for t in _lower(_tokens(" ".join(a_ch))) if t in SCOPE_TOGGLE}
        if st_b != st_a:
            return _reading("deontic", True,
                            {"scope_toggle": sorted(st_b ^ st_a),
                             "modal_vector": dict(vb)},
                            reason=f"scope of an obligation/permission changed "
                                   f"({sorted(st_b ^ st_a)} toggled beside a modal)")
    if mode == "config":
        for idx_set, segs in ((b_idx, bsegs), (a_idx, asegs)):
            for i in idx_set:
                keys = _parent_keys(segs, i)
                k = _config_key(segs[i])
                if k:
                    keys.append(k)
                hit = next((x for x in keys if NORM_IDENT.search(x)), None)
                if hit:
                    return _reading("deontic", True, {"norm_structure": hit},
                                    reason=f"change inside permission structure '{hit}'")
    if mode == "code":
        for idx_set, segs in ((b_idx, bsegs), (a_idx, asegs)):
            for i in idx_set:
                line = segs[i]
                m = re.match(r"^\s*([\w.]+)\s*[=:]", line)
                ident = m.group(1) if m else None
                encl = _enclosing_def(segs, i)
                for cand in (ident, encl, line):
                    if cand and NORM_IDENT.search(cand):
                        name = cand if cand in (ident, encl) else "changed line"
                        return _reading("deontic", True, {"norm_structure": name},
                                        reason=f"change inside permission structure ({name})")
    return _reading("deontic", False,
                    {"modal_vector_before": dict(vb), "modal_vector_after": dict(va)},
                    reason="no obligation/permission/prohibition altered in the changed span")


# ---------------------------------------------------------------- 7. epistemic (Confidence)
def epistemic(before: str, after: str) -> dict:
    """Hedge/certainty lexicon diff (CoNLL-2010 cue family): fires when the change
    moves confidence WITHOUT changing the underlying claim. Guards: (1) if the
    strict deontic vector moved too, the change is Rules territory — stand down;
    (2) the changed sentences minus certainty cues must still say the same thing,
    UNLESS the move is clearly directional (hedge down AND booster up, or the
    reverse). Config half: a confidence/verification key changing value."""
    r = _refusal("epistemic", before, after)
    if r:
        return r
    mode = _mode(before, after)
    b_ch, a_ch, _, _, bsegs, asegs, b_idx, a_idx = _changed(before, after, mode)
    cb, ca = _certainty_vector(b_ch), _certainty_vector(a_ch)
    if cb == ca:
        if mode == "config":
            for bl, al in zip(b_ch, a_ch):
                kb, ka = _config_key(bl), _config_key(al)
                if kb and kb == ka and EPISTEMIC_KEY.search(kb) \
                        and bl.split(":", 1)[-1] != al.split(":", 1)[-1]:
                    return _reading("epistemic", True,
                                    {"config_key": kb,
                                     "moved": f"{bl.split(':', 1)[-1].strip()} -> "
                                              f"{al.split(':', 1)[-1].strip()}"},
                                    reason=f"confidence key '{kb}' changed value")
        return _reading("epistemic", False,
                        {"certainty_before": dict(cb), "certainty_after": dict(ca)},
                        reason="no hedge/certainty cue moved in the changed span")
    if _modal_vector_strict(b_ch) != _modal_vector_strict(a_ch):
        return _reading("epistemic", False,
                        {"certainty_before": dict(cb), "certainty_after": dict(ca),
                         "suppressed_by": "deontic modal change"},
                        reason="the moved modal is an obligation/permission — route to Rules (deontic)")
    delta = {k: ca.get(k, 0) - cb.get(k, 0) for k in set(cb) | set(ca)}
    directional = (delta.get("hedge", 0) < 0 < delta.get("booster", 0)) or \
                  (delta.get("booster", 0) < 0 < delta.get("hedge", 0))
    strip = HEDGE | BOOSTER
    bc = [t for t in _content(_tokens(" ".join(b_ch))) if t not in strip]
    ac = [t for t in _content(_tokens(" ".join(a_ch))) if t not in strip]
    sim = _fuzzy_jaccard(bc, ac)
    if sim < 0.6 and not directional:
        return _reading("epistemic", False,
                        {"certainty_before": dict(cb), "certainty_after": dict(ca),
                         "content_similarity": round(sim, 3)},
                        reason="the claim itself changed alongside the cue — not a pure confidence move")
    return _reading("epistemic", True,
                    {"certainty_before": dict(cb), "certainty_after": dict(ca),
                     "delta": delta, "content_similarity": round(sim, 3),
                     "directional": directional},
                    reason=f"confidence moved ({delta}) while the claim held still")


# ---------------------------------------------------------------- 8. pragmatic (Manner)
def pragmatic(before: str, after: str) -> dict:
    """Register/formality shift with the meaning-skeleton invariant. Signals:
    second-person <-> impersonal, politeness/boilerplate or greeting tokens on one
    side only, formal<->plain word pairs, colloquialisms on one side, contraction
    toggles, passive<->active flip, pure function-word rewording, format-only
    reflow (same words, new layout), value re-expression (0.42 <-> 42 percent),
    and manner-keys in config (style/format/template/greeting...). Invariants:
    values, modal vector, and certainty vector all flat; content lemmas (after
    register normalisation) still matching."""
    r = _refusal("pragmatic", before, after)
    if r:
        return r
    mode = _mode(before, after)
    b_ch, a_ch, pairs, _, *_rest = _changed(before, after, mode)
    btext, atext = " ".join(b_ch), " ".join(a_ch)
    blow, alow = set(_lower(_tokens(btext))), set(_lower(_tokens(atext)))

    signals = []
    b2 = sum(1 for t in _lower(_tokens(btext)) if t in SECOND_PERSON)
    a2 = sum(1 for t in _lower(_tokens(atext)) if t in SECOND_PERSON)
    if (b2 == 0) != (a2 == 0):
        signals.append("second-person <-> impersonal")
    bp = sum(1 for t in _lower(_tokens(btext)) if t in POLITENESS)
    ap = sum(1 for t in _lower(_tokens(atext)) if t in POLITENESS)
    if (bp == 0) != (ap == 0):
        signals.append("politeness/boilerplate on one side")
    if ("please" in blow) != ("please" in alow):
        signals.append("politeness marker toggled")
    bg, ag = blow & GREETINGS, alow & GREETINGS
    if bg != ag and (bg or ag):
        signals.append(f"salutation shift {sorted(bg)} -> {sorted(ag)}")
    for formal, plain in FORMAL_PLAIN.items():
        if (formal in blow and any(_fuzzy_eq(plain, t) for t in alow)) or \
           (formal in alow and any(_fuzzy_eq(plain, t) for t in blow)):
            signals.append(f"formality pair {formal}<->{plain}")
            break
    bcol = [p.pattern for p in COLLOQUIAL if p.search(btext.lower())]
    acol = [p.pattern for p in COLLOQUIAL if p.search(atext.lower())]
    if bool(bcol) != bool(acol):
        signals.append("colloquialism on one side")
    if bool(CONTRACTIONS.search(btext)) != bool(CONTRACTIONS.search(atext)):
        signals.append("contraction toggle")
    if bool(PASSIVE.search(btext)) != bool(PASSIVE.search(atext)):
        signals.append("passive <-> active voice")
    pure_function = pairs and all(
        all(t in STOPWORDS or not any(c.isalnum() for c in t) for t in _lower(bt + at))
        for bt, at in pairs)
    if pure_function:
        signals.append("function-word-only rewording")

    def _alnum_seq(text: str) -> list[str]:
        drop = {"f", "fr", "rf", "str", "repr", "format"} if mode == "code" else set()
        return [t for t in _lower(_tokens(text))
                if any(c.isalnum() for c in t) and t not in STOPWORDS and t not in drop]
    reflow = _alnum_seq(btext) == _alnum_seq(atext) and btext != atext
    if reflow:
        signals.append("format-only reflow (same words, new layout)")

    reexpress = False
    for bt, at in pairs:
        bnums = [t for t in bt if _NUM.fullmatch(t)]
        anums = [t for t in at if _NUM.fullmatch(t)]
        if len(bnums) == 1 and len(anums) == 1:
            try:
                x, y = float(bnums[0].replace(",", "")), float(anums[0].replace(",", ""))
                pair_text = " ".join(bt + at).lower()
                if x and y and (abs(x / y - 100) < 1e-6 or abs(y / x - 100) < 1e-6) \
                        and ("percent" in pair_text or "%" in pair_text):
                    reexpress = True
                    signals.append("value re-expression (percent form)")
            except ValueError:
                pass

    if mode == "config":
        for bl, al in zip(b_ch, a_ch):
            kb, ka = _config_key(bl), _config_key(al)
            if kb and kb == ka and MANNER_KEY.search(kb):
                signals.append(f"manner key '{kb}'")
                break

    if not signals:
        return _reading("pragmatic", False, {"signals": []},
                        reason="no register/formality signal in the changed span")

    if not reexpress and _values(_tokens(btext), mode) != _values(_tokens(atext), mode):
        return _reading("pragmatic", False, {"signals": signals, "broken": "values"},
                        reason="a checkable value moved — content changed, not just manner")
    if _modal_vector(b_ch) != _modal_vector(a_ch):
        return _reading("pragmatic", False, {"signals": signals, "broken": "modal vector"},
                        reason="an obligation/permission moved — route to Rules (deontic)")
    if _certainty_vector(b_ch) != _certainty_vector(a_ch):
        return _reading("pragmatic", False, {"signals": signals, "broken": "certainty vector"},
                        reason="a confidence cue moved — route to Confidence (epistemic)")

    def _normalise(text: str) -> list[str]:
        text = NOTICE_FRAME.sub(" ", text)
        toks = []
        for t in _content(_tokens(text)):
            if t in POLITENESS or t in GREETINGS:
                continue
            toks.append(FORMAL_PLAIN.get(t, t))
        return toks

    sim = _fuzzy_jaccard(_normalise(btext), _normalise(atext))
    if sim < 0.5:
        return _reading("pragmatic", False,
                        {"signals": signals, "content_similarity": round(sim, 3)},
                        reason="content words diverge beyond a register recast")
    return _reading("pragmatic", True,
                    {"signals": signals, "content_similarity": round(sim, 3)},
                    reason=f"register shifted ({'; '.join(signals[:3])}) with content preserved")


# ---------------------------------------------------------------- 9. ontological (Identity)
def ontological(before: str, after: str) -> dict:
    """Is-a / type-assertion diff: fires when the changed span reassigns what
    something IS. Prose: a copular sentence whose subject survives and whose
    predicate nominal changes; or a nominal replace-pair sitting right after a
    copula/'as'/appositive comma, absent from the counterpart text. Config: a
    type-ish key (role/type/kind/class/category/canonical/environment...) changes
    value. Code: a class's base changes."""
    r = _refusal("ontological", before, after)
    if r:
        return r
    mode = _mode(before, after)
    b_ch, a_ch, pairs, _, bsegs, asegs, b_idx, a_idx = _changed(before, after, mode)

    if mode == "config":
        for bl, al in zip(b_ch, a_ch):
            mb = re.match(r"""^\s*["']?([\w.-]+)["']?\s*:\s*(.+)$""", bl)
            ma = re.match(r"""^\s*["']?([\w.-]+)["']?\s*:\s*(.+)$""", al)
            if mb and ma and mb.group(1) == ma.group(1) and mb.group(2) != ma.group(2):
                parts = re.split(r"[._-]", mb.group(1).lower())
                if parts[-1] in TYPE_KEY_PARTS or mb.group(1).lower() in TYPE_KEY_PARTS:
                    return _reading("ontological", True,
                                    {"type_key": mb.group(1),
                                     "retyped": f"{mb.group(2)} -> {ma.group(2)}"},
                                    reason=f"type key '{mb.group(1)}' reassigned: "
                                           f"{mb.group(2)} -> {ma.group(2)}")
    if mode == "code":
        for bl, al in zip(b_ch, a_ch):
            mb = re.match(r"^\s*class\s+(\w+)\s*\(\s*([\w.,\s]+)\)", bl)
            ma = re.match(r"^\s*class\s+(\w+)\s*\(\s*([\w.,\s]+)\)", al)
            if mb and ma and mb.group(1) == ma.group(1) and mb.group(2) != ma.group(2):
                return _reading("ontological", True,
                                {"class": mb.group(1),
                                 "retyped": f"{mb.group(2)} -> {ma.group(2)}"},
                                reason=f"class {mb.group(1)} rebased: "
                                       f"{mb.group(2)} -> {ma.group(2)}")

    # prose rule 1: copular sentence, subject held, predicate nominal changed
    for bs, as_ in zip(b_ch, a_ch):
        bl, al = _lower(_tokens(bs)), _lower(_tokens(as_))
        cop_b = next((i for i, t in enumerate(bl) if t in COPULA), None)
        cop_a = next((i for i, t in enumerate(al) if t in COPULA), None)
        phrase = any(p.search(bs) and p.search(as_) for p in COPULA_PHRASES)
        if cop_b is None or cop_a is None:
            if not phrase:
                continue
            cop_b, cop_a = 0, 0
        subj_sim = _fuzzy_jaccard(_content(bl[:cop_b]), _content(al[:cop_a]))
        pred_b, pred_a = _content(bl[cop_b + 1:]), _content(al[cop_a + 1:])
        pred_sim = _fuzzy_jaccard(pred_b, pred_a)
        if subj_sim < 0.7 or pred_sim >= 0.999 or not pred_b or not pred_a:
            continue
        head_b = bl[cop_b + 1] if cop_b + 1 < len(bl) else ""
        head_a = al[cop_a + 1] if cop_a + 1 < len(al) else ""

        def _nominal(head):
            if head in ("a", "an", "the", "no", "not", "part", "one"):
                return True
            return head.isalpha() and not head.endswith(("ed", "en", "ing")) \
                and head not in STOPWORDS
        if not (_nominal(head_b) and _nominal(head_a)):
            continue
        if _is_definitional([bs, as_], mode)[0]:
            return _reading("ontological", False,
                            {"suppressed_by": "definitional position"},
                            reason="the copula is a definition — route to Premises (axiomatic)")
        changed_pred = set(pred_b) ^ set(pred_a)
        if any(t.isdigit() or t in NUMBER_WORDS for t in changed_pred):
            continue  # a quantity moved, not a category — empirical territory
        return _reading("ontological", True,
                        {"subject_similarity": round(subj_sim, 3),
                         "retyped": f"{' '.join(pred_b)} -> {' '.join(pred_a)}"},
                        reason=f"category reassigned: {' '.join(pred_b)} -> {' '.join(pred_a)}")

    # prose rule 2: nominal replace-pair after copula/'as'/appositive comma,
    # each side absent from the counterpart text (a retype, not a re-order)
    blow_full, alow_full = before.lower(), after.lower()
    btok_all = _lower(_tokens(before))
    for bt, at in pairs:
        if not bt or not at:
            continue
        cb, ca_ = _content(bt), _content(at)
        if not cb or not ca_:
            continue
        if any(t.isdigit() or t in NUMBER_WORDS for t in _lower(bt + at)):
            continue
        if set(cb) & (HEDGE | BOOSTER | OBLIGATION | PERMISSION | PROHIBITION):
            continue
        if set(ca_) & (HEDGE | BOOSTER | OBLIGATION | PERMISSION | PROHIBITION):
            continue
        if any(_fuzzy_eq(x, y) for x in cb for y in ca_):
            continue  # shared stem: a modification, not a retype
        if any(w in alow_full for w in cb) or any(w in blow_full for w in ca_):
            continue  # words survive elsewhere: a re-ordering
        head = _lower(bt)[0]
        if not (head.isalpha() or head in ("a", "an", "the")) or \
                (head.isalpha() and head.endswith(("ed", "en"))):
            continue
        # find the tokens just before this span in the BEFORE text
        for i in range(len(btok_all) - len(bt) + 1):
            if btok_all[i:i + len(bt)] == _lower(bt):
                ctx = btok_all[max(0, i - 3):i]
                while ctx and ctx[-1] in ("a", "an", "the"):
                    ctx.pop()
                if ctx and ctx[-1] in APPOSITIVE_CUE:
                    return _reading("ontological", True,
                                    {"cue": ctx[-1],
                                     "retyped": f"{' '.join(cb)} -> {' '.join(ca_)}"},
                                    reason=f"category reassigned after '{ctx[-1]}': "
                                           f"{' '.join(cb)} -> {' '.join(ca_)}")
                break
    return _reading("ontological", False, {},
                    reason="no is-a/type assertion altered in the changed span")


# ---------------------------------------------------------------- 10. axiomatic (Premises)
def axiomatic(before: str, after: str, ripple_threshold: int = 2) -> dict:
    """Premises, with the RIPPLE COMPUTED — the measured reason panels absorb
    Premises into Facts is that nobody counts what depends on the changed term.
    Anchor: the defined term (prose), the assigned constant (code), or the basis
    key and its values (config). Ripple: how many OTHER segments mention the
    anchor — plus the segments that silently INHERIT a scope declaration (numeric
    lines under a units/currency basis; time-handling lines under a time-basis
    comment). Fires on definition-position AND ripple >= threshold (>= 1 for a
    named code constant: one reuse of a constant is already a dependency); a
    low-ripple value change routes toward Facts."""
    r = _refusal("axiomatic", before, after)
    if r:
        return r
    mode = _mode(before, after)
    b_ch, a_ch, pairs, _, bsegs, asegs, b_idx, a_idx = _changed(before, after, mode)
    changed_set = set(b_ch)
    other_segs = [s for s in bsegs if s not in changed_set]

    parent_chain = []
    if mode == "config":
        for i in b_idx:
            parent_chain += _parent_keys(bsegs, i)
    defn, why = _is_definitional(b_ch + a_ch, mode, pairs, parent_chain)

    # ---- anchors
    anchors: list[str] = []
    threshold = ripple_threshold
    inherit_numeric = inherit_time = False
    if mode == "code":
        for line in b_ch + a_ch:
            m = CODE_CONST.match(line)
            if m:
                anchors.append(m.group(1))
        if anchors:
            threshold = 1  # a named constant reused once is already a dependency
        else:
            for line in b_ch:
                if line.strip().startswith("#") or '"""' in line:
                    anchors.extend(w for w in _content(_tokens(line)) if len(w) >= 3)
                    if TIME_BASIS.search(line):
                        inherit_time = True
    elif mode == "config":
        for bl in b_ch:
            k = _config_key(bl)
            if k:
                anchors.append(k)
                if k.lower() in BASIS_KEYS:
                    inherit_numeric = True
        for k in parent_chain:
            anchors.append(k)
            if k.lower() in BASIS_KEYS:
                inherit_numeric = True
        # changed values are anchors too ('staging' removed from environments)
        for bt, at in pairs:
            anchors.extend(t for t in _content(bt + at) if len(t) >= 4)
    else:
        cand = set()
        for s in b_ch + a_ch:
            cand.update(w for w in _content(_tokens(s)) if len(w) >= 4)
        for w in sorted(cand):
            if any(any(_fuzzy_eq(w, t) for t in _content(_tokens(o))) for o in other_segs):
                anchors.append(w)

    # ---- ripple: other segments that depend on an anchor
    def _mentions(seg: str) -> bool:
        seg_low = seg.lower()
        for a in anchors:
            if mode == "prose":
                if any(_fuzzy_eq(a.lower(), t) for t in _content(_tokens(seg))):
                    return True
            else:
                for part in re.split(r"[._-]", a.lower()):
                    if len(part) >= 3 and part not in STOPWORDS and part in seg_low:
                        return True
        return False

    ripple_segs = [seg for seg in other_segs if _mentions(seg)]
    ripple = len(ripple_segs)
    inherited = 0
    if inherit_numeric:
        inherited += sum(1 for seg in other_segs
                         if re.search(r":\s*-?\d+(?:\.\d+)?\s*,?\s*$", seg)
                         and seg not in ripple_segs)
    if inherit_time:
        inherited += sum(1 for seg in other_segs
                         if TIME_USER.search(seg) and seg not in ripple_segs)
    ripple += inherited

    evidence = {"ripple": ripple, "ripple_mentions": len(ripple_segs),
                "ripple_inherited": inherited,
                "anchors": anchors[:8], "definitional": defn,
                "definitional_why": why, "mode": mode,
                "threshold": threshold}
    if defn and ripple >= threshold:
        return _reading("axiomatic", True, evidence,
                        reason=f"changed span sits in a definition/assumption position ({why}) "
                               f"and {ripple} downstream segments depend on it")
    if defn:
        return _reading("axiomatic", False, evidence,
                        reason=f"definition position but ripple {ripple} < {threshold} "
                               "— low dependency, route toward Facts (empirical)")
    return _reading("axiomatic", False, evidence,
                    reason="changed span is not in a definition/assumption position"
                           + (f" (ripple would be {ripple})" if ripple else ""))


# ---------------------------------------------------------------- dye tests
# Twelve planted items, one per kind. Each instrument must fire on exactly its
# own kind's item and stay CLEAN on the other eleven; plus one refusal probe.

DYE_ITEMS: dict[str, tuple[str, str]] = {
    "structural": ('{"retries": 3, "backoff": "fixed"}',
                   '{"retries": 3, "backoff": "fixed"'),
    "procedural": ("Release runbook. First fetch the artifact. Then vet the checksum. "
                   "Then activate the release.",
                   "Release runbook. First fetch the artifact. Then activate the release. "
                   "Then vet the checksum."),
    "contingent": ("The quarterly briefing is held in Room 214, refreshments from the "
                   "canteen.",
                   "The quarterly briefing is held in Room 318, refreshments from the "
                   "canteen."),
    "testimonial": ("Change log. 2026-05-20 wording clarified by the works council. "
                    "2026-06-02 caps revised.",
                    "Change log. 2026-05-20 wording clarified. 2026-06-02 caps revised."),
    "axiotic": ("Where crews cannot cover every zone, arterial routes are cleared "
                "before school frontages, and school frontages before residential "
                "loops.",
                "Where crews cannot cover every zone, school frontages are cleared "
                "before arterial routes, and arterial routes before residential "
                "loops."),
    "deontic": ("Operators may purge entries older than ninety days.",
                "Operators must purge entries older than ninety days."),
    "pragmatic": ("You must return your badge to your line manager before you leave.",
                  "All badges must be returned to the line manager before leaving."),
    "ontological": ("The relief fund is a charitable trust administered by the "
                    "finance office.",
                    "The relief fund is a budget line administered by the finance "
                    "office."),
    "epistemic": ("The pilot data suggest that queues shortened during the trial.",
                  "The pilot data establish that queues shortened during the trial."),
    "empirical": ("The visitor centre receives about forty thousand visits a year.",
                  "The visitor centre receives about seventy thousand visits a year."),
    "nomological": ("The late charge is calculated as one per cent simple interest "
                    "on the amount outstanding.",
                    "The late charge is calculated as one per cent compounded monthly "
                    "on the amount outstanding."),
    "axiomatic": ("Response times are counted in working days, and every deadline "
                  "below is read against that basis. Complaints receive an answer "
                  "within five days. Appeals conclude within ten days.",
                  "Response times are counted in calendar days, and every deadline "
                  "below is read against that basis. Complaints receive an answer "
                  "within five days. Appeals conclude within ten days."),
}

INSTRUMENTS = {"empirical": empirical, "deontic": deontic, "epistemic": epistemic,
               "pragmatic": pragmatic, "ontological": ontological,
               "axiomatic": axiomatic}


def dye_tests() -> list[tuple[str, bool]]:
    results = []
    for iname, fn in INSTRUMENTS.items():
        for kind, (b, a) in DYE_ITEMS.items():
            reading = fn(b, a)
            want_fire = (kind == iname)
            ok = reading["fired"] == want_fire and not reading["refused"]
            verb = "fires on own" if want_fire else f"clean on {kind}"
            results.append((f"{iname:11s} {verb}", ok))
        refuse = fn("same text.", "same text.")
        results.append((f"{iname:11s} refuses identical input", refuse["refused"]))
    return results


# ---------------------------------------------------------------- provisional bake-off

PLAIN_TO_INTERNAL = {"Priorities": "axiotic", "Rules": "deontic", "Manner": "pragmatic",
                     "Identity": "ontological", "Confidence": "epistemic",
                     "Facts": "empirical", "Circumstances": "contingent",
                     "Process": "procedural", "Model": "nomological",
                     "Structure": "structural", "Premises": "axiomatic",
                     "Record": "testimonial"}

CORPUS = "/home/emoore/CIRISOntology/scratchpad/plane_corpus/corpus_full.jsonl"
JUDGMENTS = "/home/emoore/CIRISOntology/scratchpad/plane_corpus/full_judgments.jsonl"


def load_corpus() -> list[dict]:
    with open(CORPUS) as f:
        return [json.loads(l) for l in f if l.strip()]


def provisional_gold() -> tuple[dict, int]:
    """Modal label per item over the BASE-condition panel. Ties -> None (excluded).
    PROVISIONAL: panel-modal, not a human ceiling — validates nothing."""
    votes: dict[str, Counter] = defaultdict(Counter)
    with open(JUDGMENTS) as f:
        for line in f:
            d = json.loads(line)
            if d.get("condition") != "BASE":
                continue
            lab = d.get("kind")
            if lab not in PLAIN_TO_INTERNAL:
                continue  # None / NO FIT / stray labels do not vote
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


def bakeoff(out_path: Optional[str] = None) -> str:
    corpus = load_corpus()
    gold, ties = provisional_gold()
    lines = []
    say = lines.append
    say("=" * 78)
    say("PROVISIONAL BAKE-OFF — v0b heuristic halves, one-vs-rest")
    say("Gold = BASE-condition modal panel label (3 judge models). PROVISIONAL:")
    say("panel-modal is NOT a human ceiling; no instrument is validated by this")
    say("table, and the Lean pins that (`suite_ships_unvalidated`).")
    say("=" * 78)
    scored = [d for d in corpus if gold.get(d["id"])]
    say(f"items: {len(corpus)} in corpus, {len(scored)} scored, {ties} panel ties excluded")

    readings: dict[str, dict[str, dict]] = {}
    for d in corpus:
        readings[d["id"]] = {n: fn(d["before"], d["after"]) for n, fn in INSTRUMENTS.items()}

    for gold_name, gold_map, note in (
            ("PANEL-MODAL (provisional gold)", gold, "ties excluded"),
            ("AUTHORED kind_target (authors' intent — diagnostic only)",
             {d["id"]: d["kind_target"] for d in corpus}, "all 248 items")):
        say("")
        say(f"--- against {gold_name} [{note}] ---")
        say(f"{'instrument':12s} {'P':>6s} {'R':>6s} {'F1':>6s}  {'tp':>3s} {'fp':>3s} {'fn':>3s}  top false-fire sources")
        for iname in INSTRUMENTS:
            tp = fp = fn_ = 0
            fp_from = Counter()
            for d in corpus:
                g = gold_map.get(d["id"])
                if g is None:
                    continue
                fired = readings[d["id"]][iname]["fired"]
                if fired and g == iname:
                    tp += 1
                elif fired:
                    fp += 1
                    fp_from[g] += 1
                elif g == iname:
                    fn_ += 1
            p, r, f = _prf(tp, fp, fn_)
            src = ", ".join(f"{k}:{v}" for k, v in fp_from.most_common(3)) or "-"
            say(f"{iname:12s} {p:6.2f} {r:6.2f} {f:6.2f}  {tp:3d} {fp:3d} {fn_:3d}  {src}")
        say("")

    # ---- the ripple question: does high ripple separate Premises from Facts?
    say("--- ripple feature (axiomatic instrument), by AUTHORED kind ---")
    say("fires needs BOTH definition-position AND ripple over threshold; the")
    say("separator is the CONJUNCTION — ripple alone is common, the pair is not.")
    say(f"{'kind_target':12s} {'n':>3s} {'defn%':>6s} {'med ripple':>10s} {'rip>=2%':>8s} {'defn&rip%':>9s}")
    by_kind: dict[str, list] = defaultdict(list)
    for d in corpus:
        ev = readings[d["id"]]["axiomatic"]["evidence"]
        if ev:
            by_kind[d["kind_target"]].append(
                (ev.get("definitional", False), ev.get("ripple", 0),
                 ev.get("threshold", 2)))
    for k in sorted(by_kind, key=lambda k: -sum(1 for x in by_kind[k] if x[0] and x[1] >= x[2])):
        rows = by_kind.get(k, [])
        rip = sorted(x[1] for x in rows)
        med = rip[len(rip) // 2]
        dpct = 100 * sum(1 for x in rows if x[0]) / len(rows)
        hi = 100 * sum(1 for x in rows if x[1] >= 2) / len(rows)
        both = 100 * sum(1 for x in rows if x[0] and x[1] >= x[2]) / len(rows)
        say(f"{k:12s} {len(rows):3d} {dpct:5.0f}% {med:10d} {hi:7.0f}% {both:8.0f}%")

    # ---- panel-vs-author disagreement on Premises: the absorption, measured here
    say("")
    say("--- Premises absorption check (panel gold vs authored, axiomatic items) ---")
    absorbed = Counter()
    for d in corpus:
        if d["kind_target"] == "axiomatic" and gold.get(d["id"]):
            absorbed[gold[d["id"]]] += 1
    say(f"panel-modal labels on the 24 authored-Premises items: {dict(absorbed)}")
    rec = sum(1 for d in corpus if d["kind_target"] == "axiomatic"
              and readings[d["id"]]["axiomatic"]["fired"])
    say(f"panel recovers {absorbed.get('axiomatic', 0)}/24; the ripple instrument fires on {rec}/24")

    # ---- suspicious items
    say("")
    say("--- suspicious items (heuristic flags, for human eyes — not verdicts) ---")
    for d in corpus:
        fires = [n for n, rd in readings[d["id"]].items() if rd["fired"]]
        _, _, prs, regions, *_r = _changed(d["before"], d["after"], _mode(d["before"], d["after"]))
        flags = []
        if len(fires) >= 3:
            flags.append(f"multi-fire {fires}")
        if regions >= 5:
            flags.append(f"{regions} separate diff regions (double-span?)")
        if d["kind_target"] == "axiomatic" and readings[d["id"]]["axiomatic"]["evidence"].get("ripple", 0) == 0:
            flags.append("authored Premises but ripple 0")
        g = gold.get(d["id"])
        if g and g != d["kind_target"] and d["kind_target"] in INSTRUMENTS \
                and readings[d["id"]][d["kind_target"]]["fired"] and g not in fires:
            flags.append(f"panel says {g}, author+instrument say {d['kind_target']}")
        if flags:
            say(f"  {d['id']:26s} {'; '.join(flags)}")

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
    by_inst = defaultdict(lambda: [0, 0])
    for name, passed in results:
        inst = name.split()[0]
        by_inst[inst][0] += passed
        by_inst[inst][1] += 1
    print(f"{'instrument':12s} dye tests")
    for inst, (p, n) in by_inst.items():
        print(f"  {inst:11s} {p}/{n} {'PASS' if p == n else 'FAIL'}")
    print(f"\n{'ALL DYE TESTS PASS' if ok else 'DYE FAILURE — instrument not fit to ship'} "
          f"({sum(p for _, p in results)}/{len(results)})")
    if ok:
        out = "/home/emoore/CIRISOntology/scratchpad/instruments/v0b_bakeoff.txt"
        print()
        print(bakeoff(out))
        print(f"\n[bake-off saved to {out}]")
    raise SystemExit(0 if ok else 1)
