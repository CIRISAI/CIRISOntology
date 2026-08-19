"""Instrument suite v0d — instruments 11 and 12, the two JUDGE-LED halves.

    axiotic (Priorities)   heuristic PREFILTER + judge PRIMARY
    nomological (Model)    heuristic PREFILTER + judge PRIMARY

`Core/Instrument.lean` types these two apart from the other ten: their `judgeRole`
is "PRIMARY", not a tie-break. Re-ranking is judge territory (axiotic); the
Model-vs-Facts trap is the corpus's job to load (nomological). So the shape here
is deliberately NOT the v0b shape:

    v0b (instruments 5-10):  the heuristic IS the reading.
    v0d (instruments 11-12): the heuristic is a GATE — recall-biased, cheap, and
                             allowed to be imprecise. The judge decides. A gated
                             item that the judge answers NO is a non-firing
                             reading, and the gate's only job is to keep the
                             judge off the 80% of changes that cannot be either
                             kind.

Interface, unchanged from v0/v0b: (before_text, after_text, ...) -> Reading dict
{kind, fired, evidence, refused, reason}. REFUSED stays first-class. With
`judge=None` (the default) the instrument returns the HEURISTIC-ONLY reading and
says so in evidence["judge"] — no network, no key, no spend.

Nothing here is validated and the Lean pins that (`suite_ships_unvalidated`).
The live bake-off below scores against the AUTHORED kind_target, which is the
authors' intent, not a human ceiling.
"""
from __future__ import annotations

import json
import os
import pathlib
import random
import re
import sys
import threading
import time
import urllib.request
from collections import Counter
from typing import Callable, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v0b import (  # noqa: E402
    DYE_ITEMS, STOPWORDS, _NUM, _changed, _config_key, _content, _enclosing_def,
    _is_definitional, _lower, _mode, _parent_keys, _reading, _refusal, _tokens,
    empirical,
)

# ================================================================ 11. axiotic (Priorities)
#
# What the gate is looking for: a change in WHAT BEATS WHAT. Three families of
# surface evidence, none sufficient alone in prose:
#
#   S1  an explicit preference/ranking word in the changed span
#   S2  a CONFLICT CONDITIONAL governing the changed span ("where crews cannot
#       cover every zone", "when the budget cannot cover both", "if the day runs
#       short") — the scarcity frame that makes an ordering a PRIORITY ordering
#       rather than a schedule
#   S3  an in-place PERMUTATION: the changed region's tokens are the same
#       multiset in a different order (a swap, not an edit)
#   S4  a rank-ish key / constant (priority, weight, rank, tier, precedence,
#       attention_rank, WEIGHTS, SERVICE_ORDER) whose value or list order moved
#   S5  code: the change sits in an ordering function (rank/sort/compare/pick)
#
# The discriminator against Process (procedural) is S2 + "the permutation is
# INSIDE a segment". A step list whose steps swap places is a Process change; a
# sentence whose two competing claimants swap places under a scarcity clause is
# a Priorities change. The gate encodes that; the judge is asked it directly.

AXIOTIC_STRONG = [re.compile(p, re.I) for p in (
    r"\bprecedence\b", r"\bpriorit(?:y|ies|ise|ize|ised|ized|ising|izing)\b",
    r"\bpreference[s]?\b", r"\bpreferred\b", r"\bfavou?r(?:ed|s|ing)?\b",
    r"\boutrank\w*\b", r"\boutweigh\w*\b", r"\bforemost\b",
    r"\btie[-_ ]?break\w*\b", r"\bimportance\b",
    r"\bmore important\b", r"\bmost important\b", r"\bmore valuable\b",
    r"\bgreatest weight\b", r"\bhighest weight\b",
    r"\btakes? precedence\b", r"\bahead of\b", r"\bsettles? the ordering\b",
    r"\bmerits? attention\b", r"\bin this order\b", r"\bcomes? first\b",
    r"\bfirst priority\b", r"\bin order of\b",
)]
# rank/weight also live in Model-speak ("percentile ranks", "weighted sum"), so
# they are strong ONLY when no derivation frame shares the span.
AXIOTIC_STRONG_SHARED = [re.compile(p, re.I) for p in (
    r"\brank(?:s|ed|ing)?\b", r"\bweight(?:s|ed|ing)?\b", r"\battention_rank\b",
)]
AXIOTIC_RELATION = [re.compile(p, re.I) for p in (
    r"\bbefore\b", r"\bahead\b", r"\bover\b", r"\brather than\b", r"\bthan\b",
    r"\bfirst\b", r"\bearlier\b", r"\bpreced\w*\b",
)]
CONFLICT_COND = re.compile(
    r"\b(where|when|whenever|if|should|unless)\b[^.;:]{0,90}?\b("
    r"cannot|can not|can't|unable|not enough|insufficient|runs? out|runs? short|"
    r"limited|scarce|conflict\w*|clash\w*|pull against|compet\w*|both|equal|"
    r"tie[sd]?|only one|either|contend\w*|trade[- ]?off)\b", re.I)
RANK_KEY_STRONG = re.compile(r"(priorit|weight|rank|precedence|preference|importance|tier)", re.I)
RANK_KEY_WEAK = re.compile(r"(order|seniority|severity|first|sequence)", re.I)
RANK_VALUE = re.compile(r"^(?:tier[-_ ]?\d+|p\d|\d{1,2})$", re.I)
RANK_VALUE_EXPLICIT = re.compile(r"^(?:tier[-_ ]?\d+|p\d)$", re.I)
ORDERING_FN = re.compile(r"(rank|sort|order|compare|priorit|pick|shortlist|weigh|score)", re.I)
# a derivation frame in the same span demotes rank/weight from strong to shared
NOMO_FRAME = re.compile(
    r"\b(calculat\w*|comput\w*|deriv\w*|obtained by|extrapolat\w*|estimat\w*|"
    r"normalis\w*|normaliz\w*|scor(?:e|es|ed|ing)|"
    r"assign\w*(?=[^.;]{0,40}\b(?:as|from|by|using)\b)|"
    r"fit(?:ting|ted)|interpolat\w*|aggregat\w*|smooth\w*|method\w*|formula\w*|"
    r"algorithm\w*|\bbasis\b|scheme|model(?:led|ed|ling|ing)?|curve|metric|"
    r"convention|round(?:ed|ing)|measured (?:as|by)|index|percentile)\b", re.I)


def _alnum_seq(segs: list[str]) -> list[str]:
    return [t for t in _lower(_tokens(" ".join(segs)))
            if any(c.isalnum() for c in t) and t not in STOPWORDS]


def _permuted(b_ch: list[str], a_ch: list[str]) -> bool:
    """Same tokens, different order — a swap rather than an edit."""
    b, a = _alnum_seq(b_ch), _alnum_seq(a_ch)
    return bool(b) and sorted(b) == sorted(a) and b != a


def _pure_reorder(bsegs: list[str], asegs: list[str]) -> bool:
    """Whole segments trade places and nothing else changes. A minimal diff of an
    adjacent swap is a MOVE, not a symmetric replace, so token-level permutation
    misses it; this catches it at segment level."""
    return sorted(bsegs) == sorted(asegs) and bsegs != asegs


def _within_segment_permutation(before: str, after: str, mode: str) -> bool:
    """Permutation that happens INSIDE one segment (Priorities-shaped) rather
    than by whole segments trading places (Process-shaped)."""
    b_ch, a_ch, _, _, bsegs, asegs, b_idx, a_idx = _changed(before, after, mode)
    if not _permuted(b_ch, a_ch):
        return False
    # whole-segment reorder: every changed BEFORE segment reappears verbatim in AFTER
    moved_whole = all(s in asegs for s in b_ch) and all(s in bsegs for s in a_ch)
    return not moved_whole


def _assigned_const(segs: list[str], idx: int) -> Optional[str]:
    """Name of the module-level assignment whose literal encloses segs[idx]."""
    def indent(s):
        return len(s) - len(s.lstrip())
    level = indent(segs[idx])
    for j in range(idx - 1, -1, -1):
        m = re.match(r"^(\s*)([A-Za-z_]\w*)\s*[:=]\s*[\[{(]?\s*$", segs[j])
        if m and len(m.group(1)) < level:
            return m.group(2)
        m2 = re.match(r"^(\s*)([A-Za-z_]\w*)\s*=\s*[\[{(]", segs[j])
        if m2 and len(m2.group(1)) < level:
            return m2.group(2)
    return None


def axiotic_heuristic(before: str, after: str) -> dict:
    """PREFILTER only. Recall-biased by design: it opens the gate, the judge
    closes it. Returns fired=True to mean 'worth a judge call'."""
    r = _refusal("axiotic", before, after)
    if r:
        return r
    mode = _mode(before, after)
    b_ch, a_ch, pairs, _, bsegs, asegs, b_idx, a_idx = _changed(before, after, mode)
    span = " ".join(b_ch + a_ch)
    doc = before + "\n" + after

    frame = bool(NOMO_FRAME.search(span))
    strong = [p.pattern for p in AXIOTIC_STRONG if p.search(span)]
    shared = [p.pattern for p in AXIOTIC_STRONG_SHARED if p.search(span)]
    if not frame:
        strong += shared
    relation = [p.pattern for p in AXIOTIC_RELATION if p.search(span)]
    conflict = CONFLICT_COND.search(span)
    perm_in = _within_segment_permutation(before, after, mode)
    perm_any = _permuted(b_ch, a_ch) or _pure_reorder(bsegs, asegs)

    # ---- structural (config/code) rank anchors
    rank_keys: list[str] = []
    if mode == "config":
        for idx_set, segs in ((b_idx, bsegs), (a_idx, asegs)):
            for i in idx_set:
                chain = _parent_keys(segs, i)
                k = _config_key(segs[i])
                if k:
                    chain.append(k)
                rank_keys += [c for c in chain
                              if RANK_KEY_STRONG.search(c) or RANK_KEY_WEAK.search(c)]
    ordering_fn = None
    if mode == "code":
        for idx_set, segs in ((b_idx, bsegs), (a_idx, asegs)):
            for i in idx_set:
                for cand in (_assigned_const(segs, i), _enclosing_def(segs, i)):
                    if cand and (RANK_KEY_STRONG.search(cand) or RANK_KEY_WEAK.search(cand)
                                 or ORDERING_FN.search(cand)):
                        rank_keys.append(cand)
                enc = _enclosing_def(segs, i)
                if enc and ORDERING_FN.search(enc):
                    ordering_fn = enc
    rank_strong = [k for k in rank_keys if RANK_KEY_STRONG.search(k)]

    # a rank-shaped VALUE moved. A bare small integer needs a rank-shaped key to
    # count; an explicitly ranked value (tier-2 -> tier-1, p1 -> p2) is its own
    # anchor, because the RANK LIVES IN THE VALUE, not the key.
    rank_value = False
    for bt, at in pairs:
        if not (bt and at):
            continue
        if all(RANK_VALUE.match(t) for t in bt + at):
            if rank_keys or all(RANK_VALUE_EXPLICIT.match(t) for t in bt + at):
                rank_value = True
                if not rank_keys:
                    rank_keys.append("<ranked value>")

    # header comment / whole-file preference frame, config+code only (short files)
    doc_pref = [p.pattern for p in AXIOTIC_STRONG if p.search(doc)] if mode != "prose" else []

    reasons = []
    if mode == "prose":
        if strong:
            reasons.append(f"preference lexicon in changed span: {strong[:3]}")
        if conflict and (perm_in or relation):
            reasons.append(f"conflict conditional '{conflict.group(0)[:60]}' governing an "
                           f"ordering relation {relation[:2]}")
        if perm_in and relation:
            # two claimants swap places ACROSS an ordering relation, inside one
            # sentence. This is the surface form a re-ranking shares with a
            # re-sequencing; separating them is exactly what the Lean spec hands
            # to the judge ("re-ranking is judge territory"), so the gate opens.
            reasons.append(f"in-sentence swap across ordering relation {relation[:2]} "
                           "— re-ranking or re-sequencing, judge decides")
    else:
        if rank_strong:
            reasons.append(f"rank/weight/priority key touched: {sorted(set(rank_strong))[:3]}")
        if perm_any and (rank_keys or doc_pref):
            reasons.append(f"in-place permutation under ordering anchor "
                           f"{sorted(set(rank_keys))[:2] or doc_pref[:2]}")
        if rank_value:
            reasons.append("rank-shaped value moved")
        if strong and (perm_any or rank_keys):
            reasons.append(f"preference lexicon + ordering change: {strong[:3]}")
        if mode == "code" and ordering_fn and not perm_any:
            # a comparator's tie-break attribute swapped: no permutation, but the
            # change sits in the function that DEFINES the ordering
            reasons.append(f"change inside an ordering function ({ordering_fn})")

    evidence = {"mode": mode, "strong": strong, "relation": relation,
                "conflict_conditional": bool(conflict),
                "permutation_in_segment": perm_in, "permutation_any": perm_any,
                "rank_keys": sorted(set(rank_keys))[:5],
                "derivation_frame_present": frame,
                "gate": "PREFILTER — the judge is PRIMARY for this kind"}
    if not reasons:
        return _reading("axiotic", False, evidence,
                        reason="no priority/ordering signal in the changed span")
    evidence["reasons"] = reasons
    return _reading("axiotic", True, evidence, reason="; ".join(reasons[:2]))


# ================================================================ 12. nomological (Model)
#
# What the gate is looking for: a change in WHICH FRAMEWORK IS APPLIED to derive
# an answer. Surface evidence:
#
#   N1  a derivation frame in the changed span (calculated / computed / derived
#       by / obtained by / extrapolated / normalised / scored / fitted / basis /
#       method / curve / metric / rounding)
#   N2  a method-key value change in config (smoothing, distance_metric,
#       tax_basis, growth_curve, rounding, interpolation, strategy)
#   N3  code: the identifier/call multiset in the changed lines DIFFERS — a
#       formula or function swap (mean -> median, kind="linear" -> "cubic",
#       haversine -> equirectangular). A permutation of the same identifiers is
#       Process, not Model, and is excluded.
#   N4  an applied-framework citation ("under the standard egress table", "per
#       the framework", "following the degree-day method", "assuming ...")
#
# Two guards carry the Model-vs-Facts trap:
#   G1  a pure value substitution (numbers/dates/names only, no method token, no
#       call change) does NOT fire — that is a value WITHIN the model (Facts).
#   G2  a definition/assumption POSITION (v0b `_is_definitional`, non-weak
#       pattern) does NOT fire — that is Premises. The weak 'basis'/'assuming'
#       patterns are exempted exactly where v0b exempts them: inside a
#       derivation, 'basis' is Model-speak.

NOMO_KEY = re.compile(
    r"(method|metric|basis|curve|smoothing|kind|scheme|model|algorithm|rounding|"
    r"interpolat|distance|aggregat|strategy|formula|rule|estimator|weighting|"
    r"normalis|normaliz)", re.I)
NOMO_CITE = re.compile(
    r"\b(?:under|per|following|using|in accordance with|according to|on)\s+"
    r"(?:the|this|that|a|an|its|each)?\s*(?:[\w-]+\s+){0,3}"
    r"(?:model|framework|standard|scheme|method|table|convention|basis|rule|"
    r"formula|curve|metric|regime|register|guidance)\b", re.I)
NOMO_ASSUME = re.compile(r"\bassum(?:e|es|ed|ing|ption)s?\b", re.I)
CALL_ID = re.compile(r"[A-Za-z_]\w*")


def _ident_multiset(segs: list[str]) -> Counter:
    return Counter(t for t in _lower(_tokens(" ".join(segs)))
                   if CALL_ID.fullmatch(t) and t not in STOPWORDS)


def nomological_heuristic(before: str, after: str) -> dict:
    """PREFILTER only. Recall-biased by design; the judge is PRIMARY."""
    r = _refusal("nomological", before, after)
    if r:
        return r
    mode = _mode(before, after)
    b_ch, a_ch, pairs, _, bsegs, asegs, b_idx, a_idx = _changed(before, after, mode)
    span = " ".join(b_ch + a_ch)

    frame = NOMO_FRAME.search(span)
    cite_b, cite_a = NOMO_CITE.search(" ".join(b_ch)), NOMO_CITE.search(" ".join(a_ch))
    assume = NOMO_ASSUME.search(span)

    # alphabetic content actually changed (not just a number/date/name swap)
    alpha_changed = False
    for bt, at in pairs:
        for t in _lower(bt + at):
            if t.isalpha() and t not in STOPWORDS and len(t) > 2:
                alpha_changed = True
    ids_b, ids_a = _ident_multiset(b_ch), _ident_multiset(a_ch)
    ident_swap = mode == "code" and ids_b != ids_a and sorted(ids_b.elements()) != sorted(ids_a.elements())

    method_key = None
    if mode == "config":
        for idx_set, segs in ((b_idx, bsegs), (a_idx, asegs)):
            for i in idx_set:
                chain = _parent_keys(segs, i)
                k = _config_key(segs[i])
                if k:
                    chain.append(k)
                hit = next((c for c in chain if NOMO_KEY.search(c)), None)
                if hit:
                    method_key = hit

    # ---- guards
    defn, why = _is_definitional(b_ch + a_ch, mode, pairs, None)
    evidence = {"mode": mode, "derivation_frame": frame.group(0) if frame else None,
                "citation_before": cite_b.group(0)[:60] if cite_b else None,
                "citation_after": cite_a.group(0)[:60] if cite_a else None,
                "assumption_cue": bool(assume), "method_key": method_key,
                "identifier_swap": ident_swap, "alpha_changed": alpha_changed,
                "gate": "PREFILTER — the judge is PRIMARY for this kind"}
    if defn:
        evidence["suppressed_by"] = f"definition position ({why})"
        return _reading("nomological", False, evidence,
                        reason=f"changed span sits in a definition/assumption position ({why}) "
                               "— route to Premises (axiomatic)")
    reasons = []
    if frame and alpha_changed:
        reasons.append(f"derivation frame '{frame.group(0)}' with a method term rewritten")
    if method_key:
        reasons.append(f"method key '{method_key}' changed value")
    if ident_swap:
        reasons.append("call/identifier multiset changed inside the computation "
                       "(formula swap, not a reordering)")
    if (cite_b or cite_a) and alpha_changed:
        reasons.append(f"applied-framework citation changed "
                       f"({(cite_b or cite_a).group(0)[:50]})")
    if assume and alpha_changed and frame:
        reasons.append("the assumption under which a quantity is derived changed")
    if not reasons:
        if not alpha_changed:
            evidence["suppressed_by"] = "pure value substitution"
            return _reading("nomological", False, evidence,
                            reason="only a value/date/name moved and no method term "
                                   "changed — a value WITHIN the model, route to Facts")
        return _reading("nomological", False, evidence,
                        reason="no applied-framework/derivation signal in the changed span")
    evidence["reasons"] = reasons
    return _reading("nomological", True, evidence, reason="; ".join(reasons[:2]))


# ================================================================ judge halves
#
# Prompts are FROZEN: written before the first API call, and not edited after any
# result was seen. The XV constraint this inherits — prompt architecture is not
# the lever, the judge MODEL is — means a re-worded prompt is a NEW instrument
# needing a new pre-registration, not a tuning knob.

URL = "https://api.deepinfra.com/v1/openai/chat/completions"
JUDGE_MODEL = "meta-llama/Llama-4-Scout-17B-16E-Instruct"
PRICE_IN, PRICE_OUT = 0.08, 0.30       # $/Mtok, indicative
HARD_CAP_USD = 1.00


class SpendCap(RuntimeError):
    pass


class _Spend:
    def __init__(self, cap: float = HARD_CAP_USD):
        self.cap, self.usd, self.calls = cap, 0.0, 0
        self.lock = threading.Lock()

    def add(self, tin: int, tout: int) -> None:
        with self.lock:
            self.usd += tin * PRICE_IN / 1e6 + tout * PRICE_OUT / 1e6
            self.calls += 1
            if self.usd > self.cap:
                raise SpendCap(f"hard cap ${self.cap:.2f} reached at ${self.usd:.4f}")

    def check(self) -> None:
        with self.lock:
            if self.usd > self.cap:
                raise SpendCap(f"hard cap ${self.cap:.2f} reached at ${self.usd:.4f}")


SPEND = _Spend()
_KEY: Optional[str] = None


def _key() -> str:
    global _KEY
    if _KEY is None:
        _KEY = pathlib.Path(os.path.expanduser("~/.deepinfra_key")).read_text().strip()
    return _KEY


def _ask(prompt: str, model: str = JUDGE_MODEL, retries: int = 3) -> tuple[str, int, int]:
    SPEND.check()
    body = json.dumps({"model": model, "temperature": 0.0, "max_tokens": 200,
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(URL, data=body, headers={
                "Authorization": f"Bearer {_key()}", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                d = json.loads(resp.read())
            u = d.get("usage", {})
            tin, tout = u.get("prompt_tokens", 0), u.get("completion_tokens", 0)
            SPEND.add(tin, tout)
            return d["choices"][0]["message"]["content"], tin, tout
        except SpendCap:
            raise
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(3 * (i + 1))
    raise RuntimeError(f"judge call failed after {retries} tries: {last}")


def _span_excerpt(before: str, after: str, limit: int = 700) -> tuple[str, str]:
    mode = _mode(before, after)
    b_ch, a_ch, *_ = _changed(before, after, mode)
    return (" / ".join(b_ch)[:limit] or "(nothing)",
            " / ".join(a_ch)[:limit] or "(nothing)")


AXIOTIC_JUDGE_PROMPT = """Two versions of a document differ in one place. Answer ONE question about that difference.

QUESTION: Did the change alter the ORDERING OF PRIORITY -- which thing wins, ranks higher, is weighted more, or is served first when things compete for the same limited resource or attention -- while leaving the set of permitted and required actions the same?

Answer YES only if what changed is a ranking, weighting, precedence, tie-break, or preference between things that could compete.
Answer NO if the change is instead:
- a different SEQUENCE of steps in a procedure (work done in a different order, with nothing competing),
- a different rule, method, model or formula used to compute something,
- a different permission, obligation or prohibition,
- a different factual value, name, date or place,
- a different definition or assumption,
- a different way of saying the same thing,
- anything else.

BEFORE:
---
{before}
---
AFTER:
---
{after}
---
The differing region, located by diff:
  BEFORE: {bspan}
  AFTER:  {aspan}

Answer with JSON only: {{"answer": "YES" or "NO", "reason": "<one sentence>"}}"""

NOMOLOGICAL_JUDGE_PROMPT = """Two versions of a document differ in one place. Answer ONE question about that difference.

QUESTION: Did the change alter WHICH framework, model, method, rule, basis or formula is APPLIED to derive an answer -- as opposed to changing a value, input or fact inside a framework that itself stayed the same?

Answer YES only if a different method/model/rule/basis is now being applied to get the answer.
Answer NO if the change is instead:
- only a number, name, date, quantity or reported fact, with the method unchanged,
- a claim ASSERTED to be descriptively true of the world (a model asserted as true of the world is a Fact, not an applied Model),
- a different ordering of priorities or weights between competing things,
- a different sequence of steps,
- a different permission or obligation,
- a definition or starting assumption that the rest of the document is read against,
- a different way of saying the same thing,
- anything else.

BEFORE:
---
{before}
---
AFTER:
---
{after}
---
The differing region, located by diff:
  BEFORE: {bspan}
  AFTER:  {aspan}

Answer with JSON only: {{"answer": "YES" or "NO", "reason": "<one sentence>"}}"""


def _judge(template: str, before: str, after: str, model: str = JUDGE_MODEL) -> dict:
    bspan, aspan = _span_excerpt(before, after)
    txt, tin, tout = _ask(template.format(before=before[:4000], after=after[:4000],
                                          bspan=bspan, aspan=aspan), model)
    ans, why = None, txt.strip()[:200]
    try:
        j = json.loads(txt[txt.index("{"):txt.rindex("}") + 1])
        ans = str(j.get("answer", "")).strip().upper()
        why = str(j.get("reason", ""))[:200]
    except Exception:  # noqa: BLE001
        m = re.search(r"\b(YES|NO)\b", txt.upper())
        ans = m.group(1) if m else None
    return {"answer": ans, "reason": why, "in_tok": tin, "out_tok": tout, "raw": txt[:400]}


def judge_axiotic(before: str, after: str, model: str = JUDGE_MODEL) -> dict:
    return _judge(AXIOTIC_JUDGE_PROMPT, before, after, model)


def judge_nomological(before: str, after: str, model: str = JUDGE_MODEL) -> dict:
    return _judge(NOMOLOGICAL_JUDGE_PROMPT, before, after, model)


# ================================================================ combined instruments


def _combined(kind: str, heur: Callable, judgefn: Callable,
              before: str, after: str, judge: Optional[str]) -> dict:
    """Heuristic gates, judge decides. judge=None -> heuristic-only reading."""
    rd = heur(before, after)
    if rd["refused"]:
        return rd
    if not rd["fired"]:
        rd["evidence"]["judge"] = "NOT CALLED — gate closed"
        return rd
    if judge is None:
        rd["evidence"]["judge"] = "NOT CALLED — heuristic-only mode (no model given)"
        rd["fired"] = True
        rd["reason"] = "GATE OPEN (heuristic-only mode); the judge is PRIMARY and was not called"
        return rd
    j = judgefn(before, after, judge)
    rd["evidence"]["judge"] = {"model": judge, "answer": j["answer"], "reason": j["reason"]}
    if j["answer"] == "YES":
        rd["fired"] = True
        rd["reason"] = f"gate open and judge YES: {j['reason']}"
    else:
        rd["fired"] = False
        rd["reason"] = (f"gate open but judge {j['answer']}: {j['reason']}"
                        if j["answer"] else "gate open but judge unparseable — reading withheld")
    return rd


def axiotic(before: str, after: str, judge: Optional[str] = None) -> dict:
    return _combined("axiotic", axiotic_heuristic, judge_axiotic, before, after, judge)


def nomological(before: str, after: str, judge: Optional[str] = None) -> dict:
    return _combined("nomological", nomological_heuristic, judge_nomological,
                     before, after, judge)


HEURISTICS = {"axiotic": axiotic_heuristic, "nomological": nomological_heuristic}
JUDGES = {"axiotic": judge_axiotic, "nomological": judge_nomological}


# ================================================================ dye tests
# v0b pattern: each PREFILTER must fire on exactly its own kind's planted item
# and stay clean on the other eleven, plus a refusal probe. Heuristic-only: the
# dye tests never call a judge and never spend.


def dye_tests() -> list[tuple[str, bool]]:
    results = []
    for iname, fn in HEURISTICS.items():
        for kind, (b, a) in DYE_ITEMS.items():
            rd = fn(b, a)
            want = (kind == iname)
            ok = rd["fired"] == want and not rd["refused"]
            verb = "fires on own" if want else f"clean on {kind}"
            results.append((f"{iname:11s} {verb}", ok))
        results.append((f"{iname:11s} refuses identical input",
                        fn("same text.", "same text.")["refused"]))
    return results


# ================================================================ live validation

CORPUS = "/home/emoore/CIRISOntology/scratchpad/plane_corpus/corpus_full.jsonl"
OUT = "/home/emoore/CIRISOntology/scratchpad/instruments/v0d_results.txt"
SEED = 20260818
N_NONTARGET = 40

PREREG = """PRE-REGISTRATION — v0d live validation (written before the first judge call)

SAMPLE. 20 authored-axiotic + 20 authored-nomological + 40 non-target items drawn
  with random.Random(20260818).sample from the 208 corpus items whose kind_target
  is neither. Ids printed below. No item is added or dropped after the draw.
GOLD. The AUTHORED kind_target, one-vs-rest. This is the authors' intent, NOT a
  human ceiling and NOT the panel; it validates nothing on its own, and the XV
  floor (kappa CI lower bound >= 0.70 against a two-annotator ceiling) is
  untouched by anything here.
JUDGE. meta-llama/Llama-4-Scout-17B-16E-Instruct, temperature 0, one call per
  item per instrument, prompts frozen before the first call.
REPORTED. For each instrument, three rows: PREFILTER-only, JUDGE-only (judge run
  on all 80 items regardless of the gate, to price what the gate costs in
  recall), and COMBINED (gate AND judge — the instrument as specified).
MEANING OF EVERY OUTCOME, fixed in advance:
  * combined P >= 0.70 AND R >= 0.70  -> the instrument is a CANDIDATE for an XV
    bake-off. Not validated. `suite_ships_unvalidated` still holds.
  * combined R < 0.50 with judge-only R >= 0.70 -> the GATE is the failure, not
    the judge; the finding is that the heuristic prefilter is over-tight and the
    correct v0e is a wider gate.
  * combined R < 0.50 with judge-only R < 0.70 -> the JUDGE does not carry the
    kind at this model; report as a judge failure.
  * combined P < 0.50 -> the instrument over-fires; report which kinds it eats.
  * Any prompt edit after seeing these numbers produces a NEW instrument
    requiring a NEW pre-registration. This run's numbers stand as reported.
IN-SAMPLE WARNING, stated before results. The two heuristic prefilters were
  written with the corpus visible (dye items + corpus-wide gate statistics), so
  every PREFILTER number is IN-SAMPLE and is descriptive, not evidence. The judge
  prompts were written from the Lean spec and the kind definitions only, before
  any judge call and before any judge output was seen.
MODEL-vs-FACTS READOUT, pre-specified: (a) how many authored-empirical items in
  the sample the nomological instrument fires on; (b) how many authored-
  nomological items it misses; (c) for each miss and each empirical false fire,
  whether v0b's `empirical` heuristic fires on the same item — the absorption
  direction the panel study measured.
"""


FOOTNOTE = """
--- FOOTNOTE ON REPRODUCIBILITY (observed, reported because it bears on every
    judge number above) ---
The registered analysis was executed twice with identical code, identical frozen
prompts and the same seed. Judge answers are NOT bitwise reproducible at
temperature 0 on this endpoint: the axiotic judge-only arm returned 20 false
positives on the first execution and 21 on the second; the nomological judge-only
arm returned 21 then 20. Both COMBINED rows were identical across the two runs
(axiotic P=1.00 R=1.00; nomological P=0.87 R=1.00), because the gate absorbs the
wobble. Single-run judge-only counts carry roughly +/- 1-2 items of noise. The
numbers in this file are the second execution. No verdict above turns on a
one-item difference, but a bake-off that means to CLEAR a floor must average over
repeats instead of quoting one run.

--- WHAT THIS RUN DOES NOT SHOW ---
1. The gate is IN-SAMPLE. Its rules were written with the corpus visible, so its
   precision on this corpus is descriptive. On the 80-item sample the axiotic
   gate scored P=1.00; on the full 248-item corpus the same gate scores P=0.74.
   The 1.00 is a lucky draw, the 0.74 is the honest figure, and even 0.74 is
   in-sample.
2. The judges are permissive: each says YES to about half the non-target items it
   is shown. A one-question judge tests MEMBERSHIP in a kind, not a PARTITION
   across the twelve; 27 of 80 items got YES from both judges. Neither instrument
   can yet be handed an unlabelled change and asked which kind it is.
3. Authored kind_target is the authors' intent. It is not the panel label and not
   a human ceiling. `suite_ships_unvalidated` is untouched by this file.
"""


def _prf(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return p, r, f


def load_corpus() -> list[dict]:
    with open(CORPUS) as f:
        return [json.loads(l) for l in f if l.strip()]


def sample_items(corpus: list[dict]) -> list[dict]:
    tgt = [d for d in corpus if d["kind_target"] in ("axiotic", "nomological")]
    other = [d for d in corpus if d["kind_target"] not in ("axiotic", "nomological")]
    rng = random.Random(SEED)
    return tgt + rng.sample(other, N_NONTARGET)


def gate_stats_full(corpus: list[dict]) -> list[str]:
    out = ["--- PREFILTER gate over the FULL 248-item corpus (IN-SAMPLE, descriptive) ---",
           f"{'instrument':12s} {'P':>6s} {'R':>6s} {'F1':>6s}  {'tp':>3s} {'fp':>3s} {'fn':>3s}  "
           "top gate-open sources (authored kind)"]
    for iname, fn in HEURISTICS.items():
        tp = fp = fn_ = 0
        src = Counter()
        for d in corpus:
            fired = fn(d["before"], d["after"])["fired"]
            g = d["kind_target"]
            if fired and g == iname:
                tp += 1
            elif fired:
                fp += 1
                src[g] += 1
            elif g == iname:
                fn_ += 1
        p, r, f = _prf(tp, fp, fn_)
        s = ", ".join(f"{k}:{v}" for k, v in src.most_common(4)) or "-"
        out.append(f"{iname:12s} {p:6.2f} {r:6.2f} {f:6.2f}  {tp:3d} {fp:3d} {fn_:3d}  {s}")
    return out


def live(workers: int = 8) -> str:
    from concurrent.futures import ThreadPoolExecutor
    corpus = load_corpus()
    items = sample_items(corpus)
    lines: list[str] = []
    say = lines.append
    say("=" * 78)
    say("v0d LIVE VALIDATION — instruments 11 (axiotic/Priorities) and 12 "
        "(nomological/Model)")
    say("=" * 78)
    say(PREREG)
    say(f"sample: {len(items)} items "
        f"({sum(1 for d in items if d['kind_target'] == 'axiotic')} axiotic, "
        f"{sum(1 for d in items if d['kind_target'] == 'nomological')} nomological, "
        f"{sum(1 for d in items if d['kind_target'] not in ('axiotic', 'nomological'))} non-target)")
    say("non-target ids drawn: " + ", ".join(
        sorted(d["id"] for d in items if d["kind_target"] not in ("axiotic", "nomological"))))
    say("")
    say(f"judge model: {JUDGE_MODEL}   hard cap: ${HARD_CAP_USD:.2f}")
    say("")
    say("\n".join(gate_stats_full(corpus)))
    say("")

    # ---- gates (free)
    gate = {d["id"]: {n: fn(d["before"], d["after"])["fired"]
                      for n, fn in HEURISTICS.items()} for d in items}
    emp = {d["id"]: empirical(d["before"], d["after"])["fired"] for d in items}

    # ---- judges (paid): all 80 items x both instruments
    jobs = [(d, n) for d in items for n in HEURISTICS]
    verdict: dict[tuple[str, str], dict] = {}
    capped = False

    def one(job):
        nonlocal capped
        d, n = job
        if capped:
            return
        try:
            verdict[(d["id"], n)] = JUDGES[n](d["before"], d["after"])
        except SpendCap as e:
            capped = True
            print(f"SPEND CAP: {e}", flush=True)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(one, jobs))

    say(f"judge calls made: {SPEND.calls}   spend: ${SPEND.usd:.4f} of "
        f"${HARD_CAP_USD:.2f} cap   capped: {capped}")
    unparsed = sum(1 for v in verdict.values() if v["answer"] not in ("YES", "NO"))
    say(f"judge answers: {len(verdict)}/{len(jobs)} returned, {unparsed} unparseable")
    say("")

    def jyes(id_, n):
        v = verdict.get((id_, n))
        return bool(v and v["answer"] == "YES")

    rows = {}
    say("--- one-vs-rest against AUTHORED kind_target, 80-item live sample ---")
    say(f"{'instrument':12s} {'arm':10s} {'P':>6s} {'R':>6s} {'F1':>6s}  "
        f"{'tp':>3s} {'fp':>3s} {'fn':>3s}  false fires by authored kind")
    for iname in HEURISTICS:
        for arm, pred in (("prefilter", lambda d, n=iname: gate[d["id"]][n]),
                          ("judge", lambda d, n=iname: jyes(d["id"], n)),
                          ("combined", lambda d, n=iname: gate[d["id"]][n] and jyes(d["id"], n))):
            tp = fp = fn_ = 0
            src = Counter()
            for d in items:
                f_ = pred(d)
                g = d["kind_target"]
                if f_ and g == iname:
                    tp += 1
                elif f_:
                    fp += 1
                    src[g] += 1
                elif g == iname:
                    fn_ += 1
            p, r, f1 = _prf(tp, fp, fn_)
            rows[(iname, arm)] = (p, r, f1, tp, fp, fn_, src)
            s = ", ".join(f"{k}:{v}" for k, v in src.most_common(4)) or "-"
            say(f"{iname:12s} {arm:10s} {p:6.2f} {r:6.2f} {f1:6.2f}  "
                f"{tp:3d} {fp:3d} {fn_:3d}  {s}")
    say("")

    # ---- pre-registered outcome reading
    say("--- pre-registered outcome reading (rule applied, not chosen after) ---")
    for iname in HEURISTICS:
        p, r, *_ = rows[(iname, "combined")]
        jp, jr, *_ = rows[(iname, "judge")]
        if p >= 0.70 and r >= 0.70:
            verdict_txt = "CANDIDATE for an XV bake-off (still unvalidated)"
        elif r < 0.50 and jr >= 0.70:
            verdict_txt = "GATE FAILURE — the prefilter is over-tight; the judge carries the kind"
        elif r < 0.50:
            verdict_txt = "JUDGE FAILURE — the kind is not carried at this model"
        elif p < 0.50:
            verdict_txt = "OVER-FIRES — precision below the pre-set floor"
        else:
            verdict_txt = "MIXED — neither floor cleanly met nor cleanly failed"
        say(f"  {iname:12s} combined P={p:.2f} R={r:.2f} (judge-only R={jr:.2f}) -> {verdict_txt}")
    say("")

    # ---- what the judge-only row costs the combined row (reading, post-numbers)
    say("--- READING (written after the numbers, and labelled as such) ---")
    for iname in HEURISTICS:
        cp, cr, *_ = rows[(iname, "combined")]
        jp, jr, *_ = rows[(iname, "judge")]
        gp, gr, *_ = rows[(iname, "prefilter")]
        say(f"  {iname}: judge-only precision {jp:.2f} vs combined {cp:.2f}. The judge "
            f"answers YES on roughly half the non-target items it is shown; the "
            f"discrimination in the combined row is carried by the GATE (prefilter "
            f"P={gp:.2f}), and the gate is IN-SAMPLE. Read the combined precision as "
            f"'an in-sample gate times a permissive judge', not as a validated judge.")
    both = sum(1 for d in items
               if jyes(d["id"], "axiotic") and jyes(d["id"], "nomological"))
    say(f"  the two judges are NOT mutually exclusive: {both}/{len(items)} items got YES "
        f"from BOTH one-question judges. A one-question judge tests membership, not "
        f"partition; the suite still owes an arbitration step between kinds.")
    say("")

    # ---- Model-vs-Facts readout (pre-specified)
    say("--- MODEL-vs-FACTS confusion readout (pre-specified) ---")
    empirical_items = [d for d in items if d["kind_target"] == "empirical"]
    nomo_items = [d for d in items if d["kind_target"] == "nomological"]
    say(f"authored-empirical items in sample: {len(empirical_items)}")
    fired_on_emp = [d for d in empirical_items
                    if gate[d["id"]]["nomological"] and jyes(d["id"], "nomological")]
    say(f"  nomological instrument FIRES on {len(fired_on_emp)}/{len(empirical_items)} of them "
        f"(Model eating Facts)")
    for d in fired_on_emp:
        v = verdict.get((d["id"], "nomological"), {})
        say(f"    {d['id']:26s} v0b-empirical-fires={emp[d['id']]!s:5s} judge: {v.get('reason', '')[:90]}")
    gate_only_emp = [d for d in empirical_items if gate[d["id"]]["nomological"]]
    say(f"  gate alone opened on {len(gate_only_emp)}/{len(empirical_items)}; the judge closed "
        f"{len(gate_only_emp) - len(fired_on_emp)} of those")
    missed = [d for d in nomo_items
              if not (gate[d["id"]]["nomological"] and jyes(d["id"], "nomological"))]
    say(f"authored-nomological items MISSED: {len(missed)}/{len(nomo_items)} "
        "(Facts/other eating Model)")
    for d in missed:
        v = verdict.get((d["id"], "nomological"), {})
        where = "gate closed" if not gate[d["id"]]["nomological"] else f"judge {v.get('answer')}"
        say(f"    {d['id']:26s} {where:12s} amb_with={d.get('ambiguous_with')} "
            f"v0b-empirical-fires={emp[d['id']]!s:5s} {v.get('reason', '')[:70]}")
    say(f"the four authored-nomological items marked ambiguous_with=empirical: "
        f"{[d['id'] for d in nomo_items if d.get('ambiguous_with') == 'empirical']}")
    hard_ok = [d for d in nomo_items if d.get("ambiguous_with") == "empirical"
               and gate[d["id"]]["nomological"] and jyes(d["id"], "nomological")]
    say(f"  of those, correctly fired: {len(hard_ok)}/"
        f"{len([d for d in nomo_items if d.get('ambiguous_with') == 'empirical'])}")
    say("")

    # ---- axiotic-vs-procedural readout (the gate's own designed discriminator)
    say("--- AXIOTIC-vs-PROCESS confusion readout ---")
    proc = [d for d in items if d["kind_target"] == "procedural"]
    ax_on_proc = [d for d in proc if gate[d["id"]]["axiotic"] and jyes(d["id"], "axiotic")]
    say(f"authored-procedural items in sample: {len(proc)}; axiotic instrument fires on "
        f"{len(ax_on_proc)}: {[d['id'] for d in ax_on_proc]}")
    ax_missed = [d for d in items if d["kind_target"] == "axiotic"
                 and not (gate[d["id"]]["axiotic"] and jyes(d["id"], "axiotic"))]
    say(f"authored-axiotic missed: {len(ax_missed)}")
    for d in ax_missed:
        v = verdict.get((d["id"], "axiotic"), {})
        where = "gate closed" if not gate[d["id"]]["axiotic"] else f"judge {v.get('answer')}"
        say(f"    {d['id']:26s} {where:12s} {v.get('reason', '')[:80]}")
    say("")
    say("--- per-item detail (id, authored, ax-gate/ax-judge, nomo-gate/nomo-judge) ---")
    for d in sorted(items, key=lambda x: x["id"]):
        av = verdict.get((d["id"], "axiotic"), {}).get("answer")
        nv = verdict.get((d["id"], "nomological"), {}).get("answer")
        say(f"  {d['id']:28s} {d['kind_target']:12s} "
            f"ax {'O' if gate[d['id']]['axiotic'] else '.'}/{str(av):4s} "
            f"nomo {'O' if gate[d['id']]['nomological'] else '.'}/{str(nv):4s}")
    say("")
    say(f"FINAL SPEND: ${SPEND.usd:.4f} over {SPEND.calls} calls "
        f"(cap ${HARD_CAP_USD:.2f}; capped={capped})")
    return "\n".join(lines)


def supplementary(workers: int = 8) -> str:
    """POST-HOC, and labelled as such. The registered 40-item non-target draw
    landed only 2 authored-empirical and 3 authored-procedural items, so the two
    confusion readouts the design cares most about — Model-vs-Facts and
    Priorities-vs-Process — were measured on denominators of 2 and 3. This adds
    the FULL empirical and procedural strata (20 each). It changes no metric, no
    prompt and no gate; it only widens the denominator of two readouts that were
    pre-specified and came back underpowered. Declared post-hoc; it may not be
    read as confirming anything the registered run did not already show."""
    from concurrent.futures import ThreadPoolExecutor
    corpus = load_corpus()
    emp_items = [d for d in corpus if d["kind_target"] == "empirical"]
    proc_items = [d for d in corpus if d["kind_target"] == "procedural"]
    lines: list[str] = []
    say = lines.append
    say("")
    say("=" * 78)
    say("SUPPLEMENTARY (POST-HOC) — the two confusion readouts on their FULL strata")
    say("The registered draw gave n=2 empirical and n=3 procedural. Adding the whole")
    say("stratum for each. No prompt, gate or metric changed. Post-hoc by declaration:")
    say("this widens a denominator, it does not confirm anything.")
    say("=" * 78)
    jobs = [(d, "nomological") for d in emp_items] + [(d, "axiotic") for d in proc_items]
    v: dict[tuple[str, str], dict] = {}
    capped = False

    def one(job):
        nonlocal capped
        d, n = job
        if capped:
            return
        try:
            v[(d["id"], n)] = JUDGES[n](d["before"], d["after"])
        except SpendCap as e:
            capped = True
            print(f"SPEND CAP: {e}", flush=True)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(one, jobs))

    say("")
    say("--- MODEL-vs-FACTS, full authored-empirical stratum (n=20) ---")
    g_open = fires = 0
    for d in emp_items:
        go = nomological_heuristic(d["before"], d["after"])["fired"]
        jy = v.get((d["id"], "nomological"), {}).get("answer") == "YES"
        g_open += go
        fires += go and jy
        if go:
            say(f"    {d['id']:26s} gate OPEN, judge {'YES  <-- FALSE FIRE' if jy else 'NO   (judge closed it)'}"
                f"   {v.get((d['id'], 'nomological'), {}).get('reason', '')[:80]}")
    say(f"  gate opened on {g_open}/20 empirical items; instrument (gate AND judge) fires on "
        f"{fires}/20  => Model-eats-Facts rate {fires / 20:.2f}")
    say(f"  judge alone would have said YES on "
        f"{sum(1 for d in emp_items if v.get((d['id'], 'nomological'), {}).get('answer') == 'YES')}/20")
    say("")
    say("--- PRIORITIES-vs-PROCESS, full authored-procedural stratum (n=20) ---")
    g_open = fires = 0
    for d in proc_items:
        go = axiotic_heuristic(d["before"], d["after"])["fired"]
        jy = v.get((d["id"], "axiotic"), {}).get("answer") == "YES"
        g_open += go
        fires += go and jy
        if go:
            say(f"    {d['id']:26s} gate OPEN, judge {'YES  <-- FALSE FIRE' if jy else 'NO   (judge closed it)'}"
                f"   {v.get((d['id'], 'axiotic'), {}).get('reason', '')[:80]}")
    say(f"  gate opened on {g_open}/20 procedural items; instrument (gate AND judge) fires on "
        f"{fires}/20  => Priorities-eats-Process rate {fires / 20:.2f}")
    say(f"  judge alone would have said YES on "
        f"{sum(1 for d in proc_items if v.get((d['id'], 'axiotic'), {}).get('answer') == 'YES')}/20")
    say("")
    say(f"SPEND after supplementary: ${SPEND.usd:.4f} over {SPEND.calls} calls "
        f"(cap ${HARD_CAP_USD:.2f}; capped={capped})")
    return "\n".join(lines)


if __name__ == "__main__":
    res = dye_tests()
    width = max(len(n) for n, _ in res)
    ok = True
    for name, passed in res:
        if not passed:
            print(f"  {name:<{width}}  FAIL")
        ok &= passed
    by = {}
    for name, passed in res:
        i = name.split()[0]
        by.setdefault(i, [0, 0])
        by[i][0] += passed
        by[i][1] += 1
    print(f"{'instrument':12s} dye tests (heuristic prefilter only)")
    for i, (p, n) in by.items():
        print(f"  {i:11s} {p}/{n} {'PASS' if p == n else 'FAIL'}")
    print(f"\n{'ALL DYE TESTS PASS' if ok else 'DYE FAILURE — gate not fit to ship'} "
          f"({sum(p for _, p in res)}/{len(res)})")
    if not ok:
        raise SystemExit(1)
    if "--gates-only" in sys.argv:
        print()
        print("\n".join(gate_stats_full(load_corpus())))
        raise SystemExit(0)
    if "--live" in sys.argv:
        text = live()
        if "--supp" in sys.argv:
            text += "\n" + supplementary()
        text += "\n" + FOOTNOTE
        with open(OUT, "w") as f:
            f.write(text + "\n")
        print()
        print(text)
        print(f"\n[written to {OUT}]")
    raise SystemExit(0)
