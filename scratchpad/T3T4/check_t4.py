"""T4 mechanical self-check — reads t4_items.jsonl back and verifies it against
RECOGNITION_PREREG.md §T4 and RECOGNITION_PREREG_A2.md MAJOR-8/MAJOR-9.

Every check is mechanical. Nothing here reads the author's intent; the checks that
cannot be mechanised (does the document really carry the content elsewhere?) are
named in the FAILURES-BY-DESIGN note at the bottom and are NOT claimed as passed.
"""
from __future__ import annotations
import json, re, sys, collections

PATH = "/home/emoore/CIRISOntology/scratchpad/T3T4/t4_items.jsonl"

# ---------------------------------------------------------------- ban-set
# standing _VOCAB (plane_corpus/_helper.py)
VOCAB = [r"\baxiotic\b", r"\bdeontic\b", r"\bpragmatic\b", r"\bontological\b",
         r"\bepistemic\b", r"\bempirical(ly)?\b", r"\bcontingent\b", r"\bnomological\b",
         r"\bstructural(ly)?\b", r"\btestimonial\b", r"\baxiomatic\b", r"\bprocedural(ly)?\b",
         r"\bpriorit(y|ies)\b", r"\brules?\b", r"\bmanners?\b", r"\bidentit(y|ies)\b",
         r"\bconfidence\b", r"\bfacts?\b", r"\bcircumstances?\b", r"\bprocess(es)?\b",
         r"\bmodels?\b", r"\bstructures?\b", r"\bpremises?\b", r"\brecords?\b"]
# standing _VALENCE
VALENCE = [r"\bwrong(ly)?\b", r"\berrors?\b", r"\bmistakes?\b", r"\bincorrect(ly)?\b",
           r"\bbugs?\b", r"\bfault(y|s)?\b"]
# §T4.4 extension — each is a direct cue to the manipulation
T4EXT = [r"\bregister(s|ed|ing)?\b", r"\btones?\b", r"\bstyles?\b", r"\bpresentations?\b",
         r"\bphrasings?\b", r"\bwordings?\b", r"\bexcerpts?\b", r"\bboundar(y|ies)\b",
         r"\bholistic(ally)?\b", r"\bstandalone\b"]
ARTIFACT_BAN = VOCAB + VALENCE + T4EXT   # before / after / variation_site
NOTE_BAN = VALENCE + T4EXT                # author_note: standing recipe + the T4 cue words
FRAMING_BAN = VOCAB + VALENCE + T4EXT     # panel-facing copy: same bar as artifact text

# arm-M content anchors that must survive the change untouched
MODALS = ["must", "shall", "may", "should", "will", "required", "mandatory",
          "optional", "prohibited", "permitted", "obliged"]

DOMAINS = ("policy", "report", "config", "code", "process")

fails: list[str] = []


def bad(ident, msg):
    fails.append(f"{ident}: {msg}")


def scan(text, pats, ident, where):
    for p in pats:
        m = re.search(p, text, re.I)
        if m:
            bad(ident, f"banned term {m.group(0)!r} in {where}")


def diff_span(a: str, b: str):
    """Minimal LCP/LCS differing region. Returns (start, end_a, end_b)."""
    n = min(len(a), len(b))
    p = 0
    while p < n and a[p] == b[p]:
        p += 1
    s = 0
    while s < n - p and a[len(a) - 1 - s] == b[len(b) - 1 - s]:
        s += 1
    return p, len(a) - s, len(b) - s


def numerals(t):
    return collections.Counter(re.findall(r"\d+(?:[.,]\d+)*", t))


def modal_count(t):
    return collections.Counter(w for w in MODALS
                               if re.search(rf"\b{w}\b", t, re.I)
                               for _ in re.findall(rf"\b{w}\b", t, re.I))


def band(ident, dom, before):
    if dom == "policy":
        w = len(before.split())
        if not 80 <= w <= 250:
            bad(ident, f"policy word count {w} outside 80-250")
    elif dom == "report":
        w = len(before.split())
        if not 80 <= w <= 200:
            bad(ident, f"report word count {w} outside 80-200")
    elif dom == "config":
        n = len(before.strip().splitlines())
        if not 10 <= n <= 30:
            bad(ident, f"config line count {n} outside 10-30")
    elif dom == "code":
        n = len(before.strip().splitlines())
        if not 10 <= n <= 40:
            bad(ident, f"code line count {n} outside 10-40")
    elif dom == "process":
        s = len([l for l in before.splitlines() if re.match(r"\s*\d+\.", l)])
        if not 6 <= s <= 15:
            bad(ident, f"process step count {s} outside 6-15")
    else:
        bad(ident, f"bad domain {dom!r}")


def main():
    items = [json.loads(l) for l in open(PATH) if l.strip()]
    ids = [it["id"] for it in items]
    if len(set(ids)) != len(ids):
        dup = [i for i, c in collections.Counter(ids).items() if c > 1]
        fails.append(f"duplicate ids: {dup}")

    per_arm = collections.Counter(it["arm"] for it in items)
    for a in ("M", "C", "P"):
        if per_arm[a] != 24:
            fails.append(f"arm {a}: {per_arm[a]} items, need 24")

    ratios = collections.defaultdict(list)     # arm -> char ratios
    tok_ratios = collections.defaultdict(list)  # arm -> token ratios
    dom_by_arm = collections.defaultdict(collections.Counter)

    for it in items:
        ident, arm, dom = it["id"], it["arm"], it["domain"]
        before, after, old, new = it["before"], it["after"], it["old"], it["new"]
        cs, ce = it["cut_start"], it["cut_end"]
        dom_by_arm[arm][dom] += 1

        # --- the change itself
        if before.count(old) != 1:
            bad(ident, f"old occurs {before.count(old)}x in before")
            continue
        if after != before.replace(old, new):
            bad(ident, "after is not before.replace(old, new)")
        if after == before:
            bad(ident, "after == before")
        os_ = before.index(old)
        oe = os_ + len(old)

        # --- cut offsets
        if not (0 <= cs < ce <= len(before)):
            bad(ident, f"cut offsets out of range ({cs},{ce}) len={len(before)}")
            continue
        if not (cs <= os_ and oe <= ce):
            bad(ident, f"old span ({os_},{oe}) not inside cut ({cs},{ce})")
        if ce - cs >= len(before):
            bad(ident, "cut is the whole document")

        # --- the same offsets carry to `after` via the replacement
        delta = len(new) - len(old)
        if after[cs:ce + delta] != before[cs:ce].replace(old, new):
            bad(ident, "cut offsets do not carry to after")

        # --- bans
        scan(before, ARTIFACT_BAN, ident, "before")
        scan(after, ARTIFACT_BAN, ident, "after")
        scan(it["variation_site"], ARTIFACT_BAN, ident, "variation_site")
        scan(it["author_note"], NOTE_BAN, ident, "author_note")

        # --- domain band
        band(ident, dom, before)

        # --- cut ratio
        ratios[arm].append((ce - cs) / len(before))
        tok_ratios[arm].append(len(before[cs:ce].split()) / len(before.split()))

        # --- arm M: the change is register only
        if arm == "M":
            p, ea, eb = diff_span(before, after)
            if not (os_ <= p and ea <= oe):
                bad(ident, "minimal diff is not contained in the declared span")
            if numerals(old) != numerals(new):
                bad(ident, f"numerals move: {numerals(old)} -> {numerals(new)}")
            if modal_count(old) != modal_count(new):
                bad(ident, f"strength anchors move: {modal_count(old)} -> {modal_count(new)}")
            for f in ("cutb_framing", "cutb_start", "cutb_end",
                      "cutb_after_start", "cutb_after_end"):
                if f not in it:
                    bad(ident, f"arm M missing {f}")
            if "cutb_framing" in it:
                scan(it["cutb_framing"], FRAMING_BAN, ident, "cutb_framing")
                # the change must really straddle the division: the split point has
                # to fall strictly inside the run where old and new differ, on both
                # sides. Otherwise one party's fragment is identical before/after and
                # CUT-B shows no change at all.
                dp, dea, deb = diff_span(old, new)
                sb = it["cutb_end"] - os_ if it["cutb_side"] == "head" else it["cutb_start"] - os_
                sa = (it["cutb_after_end"] if it["cutb_side"] == "head"
                      else it["cutb_after_start"]) - os_
                if not (dp < sb < dea):
                    bad(ident, f"cutb division at old+{sb} outside the differing run ({dp},{dea})")
                if not (dp < sa < deb):
                    bad(ident, f"cutb division at new+{sa} outside the differing run ({dp},{deb})")
                bs, be = it["cutb_start"], it["cutb_end"]
                abs_, abe = it["cutb_after_start"], it["cutb_after_end"]
                side = it.get("cutb_side")
                if not (0 <= bs < be <= len(before)):
                    bad(ident, f"cutb offsets out of range ({bs},{be})")
                elif side == "head":
                    # the shown party holds the run up to a point INSIDE the change
                    if not (bs <= os_ < be < oe):
                        bad(ident, f"cutb head ({bs},{be}) does not straddle ({os_},{oe})")
                    elif abs_ != bs:
                        bad(ident, "head cutb_after_start must equal cutb_start")
                    elif after[bs:os_] != before[bs:os_]:
                        bad(ident, "cutb head text differs between before and after")
                    elif not old.startswith(before[os_:be]):
                        bad(ident, "cutb head tail is not a prefix of old")
                    elif not (os_ < abe <= os_ + len(new)):
                        bad(ident, f"cutb_after_end {abe} not inside the new span")
                    elif not new.startswith(after[os_:abe]):
                        bad(ident, "cutb after-tail is not a prefix of new")
                elif side == "tail":
                    # the shown party holds the run from a point INSIDE the change on
                    if not (os_ < bs < oe <= be):
                        bad(ident, f"cutb tail ({bs},{be}) does not straddle ({os_},{oe})")
                    elif abe != be + delta:
                        bad(ident, "tail cutb_after_end must be cutb_end + delta")
                    elif after[oe + delta:abe] != before[oe:be]:
                        bad(ident, "cutb tail text differs between before and after")
                    elif not old.endswith(before[bs:oe]):
                        bad(ident, "cutb tail head is not a suffix of old")
                    elif not (os_ <= abs_ < os_ + len(new)):
                        bad(ident, f"cutb_after_start {abs_} not inside the new span")
                    elif not new.endswith(after[abs_:oe + delta]):
                        bad(ident, "cutb after-head is not a suffix of new")
                else:
                    bad(ident, f"cutb_side must be head or tail, got {side!r}")
        else:
            for f in ("cutb_framing", "cutb_start", "cutb_end"):
                if f in it:
                    bad(ident, f"arm {arm} carries {f}")

    # ---------------------------------------------------------- MAJOR-8
    print("per-arm cut ratio (characters), MAJOR-8 constraint |max/min - 1| <= 0.20")
    means = {}
    tmeans = {}
    for a in ("M", "C", "P"):
        if ratios[a]:
            means[a] = sum(ratios[a]) / len(ratios[a])
            tmeans[a] = sum(tok_ratios[a]) / len(tok_ratios[a])
            print(f"  arm {a}: n={len(ratios[a])}  mean_char={means[a]:.4f}  "
                  f"min={min(ratios[a]):.3f} max={max(ratios[a]):.3f}  "
                  f"mean_tok={tmeans[a]:.4f}")
    if len(means) == 3:
        rel = max(means.values()) / min(means.values()) - 1
        trel = max(tmeans.values()) / min(tmeans.values()) - 1
        print(f"  relative spread: char {rel*100:.2f}%   token {trel*100:.2f}%")
        if rel > 0.20:
            fails.append(f"MAJOR-8: char cut-ratio spread {rel*100:.1f}% > 20%")
        if trel > 0.20:
            fails.append(f"MAJOR-8: token cut-ratio spread {trel*100:.1f}% > 20%")

    print("\ndomain balance")
    for a in ("M", "C", "P"):
        print(f"  arm {a}: " + "  ".join(f"{d}={dom_by_arm[a][d]}" for d in DOMAINS))
    tot = collections.Counter()
    for a in dom_by_arm:
        tot.update(dom_by_arm[a])
    print("  total:  " + "  ".join(f"{d}={tot[d]}" for d in DOMAINS))
    for a in ("M", "C", "P"):
        if dom_by_arm[a] != dom_by_arm["M"]:
            fails.append(f"domain profile of arm {a} does not match arm M")

    print(f"\nitems: {len(items)}   failures: {len(fails)}")
    for f in fails:
        print("  FAIL " + f)
    print("\nNOT mechanically checked, by design and stated so: whether an arm-M "
          "document really carries the content elsewhere; whether an arm-P grounding "
          "really lies outside the cut; whether an arm-C change is really local. "
          "Each is asserted in author_note and is the author's judgment.")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
