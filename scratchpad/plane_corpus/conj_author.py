"""CONJUGATION TEST — item authoring + mechanical self-check.

Per CONJUGATION_TEST_PREREG.md (frozen 2026-08-20, items authored after the freeze).
Twelve institutional documents where the ONLY change is deontic modal strength
(must<->should, shall<->may, required<->encouraged). Governed action, scope, and
every other word identical. Four domains x 3.

Self-check is mechanical, per the standing corpus recipe (_helper.py) plus the
single-span verification the prereg's VOID gate names:
  1. the declared modal occurs EXACTLY ONCE (word-bounded) in `before`
  2. `after` is that one substitution and nothing else
  3. LCP/LCS minimal diff, expanded to word boundaries, is exactly ONE word on
     each side, and that word pair is a licensed modal pair -> single contiguous
     span, verified independently of the declaration
  4. the changed span is unique in `before`
  5. no taxonomy vocabulary in artifact text; no valence words anywhere
  6. no kind-name word inside the changed span
  7. word count in band, title line present
"""
from __future__ import annotations
import json, re, sys

OUT = "/home/emoore/CIRISOntology/scratchpad/plane_corpus/conj_items.jsonl"

# licensed deontic-strength pairs, unordered
PAIRS = {frozenset({"must", "should"}), frozenset({"shall", "may"}),
         frozenset({"required", "encouraged"})}

# taxonomy vocabulary banned from artifact text (standing recipe, _helper.py)
VOCAB = [r"\baxiotic\b", r"\bdeontic\b", r"\bpragmatic\b", r"\bontological\b",
         r"\bepistemic\b", r"\bempirical(ly)?\b", r"\bcontingent\b", r"\bnomological\b",
         r"\bstructural(ly)?\b", r"\btestimonial\b", r"\baxiomatic\b", r"\bprocedural(ly)?\b",
         r"\bpriorit(y|ies)\b", r"\brules?\b", r"\bmanners?\b", r"\bidentit(y|ies)\b",
         r"\bconfidence\b", r"\bfacts?\b", r"\bcircumstances?\b", r"\bprocess(es)?\b",
         r"\bmodels?\b", r"\bstructures?\b", r"\bpremises?\b", r"\brecords?\b"]
VALENCE = [r"\bwrong(ly)?\b", r"\berrors?\b", r"\bmistakes?\b", r"\bincorrect(ly)?\b",
           r"\bbugs?\b", r"\bfault(y|s)?\b"]


def span_of(a: str, b: str):
    """Minimal LCP/LCS diff expanded to word boundaries. Returns (span_a, span_b, start)."""
    n = min(len(a), len(b))
    p = 0
    while p < n and a[p] == b[p]:
        p += 1
    s = 0
    while s < n - p and a[len(a) - 1 - s] == b[len(b) - 1 - s]:
        s += 1
    ea, eb = len(a) - s, len(b) - s
    L = 0
    while p - L > 0 and re.match(r"\w", a[p - L - 1]):
        L += 1
    R = 0
    while ea + R < len(a) and re.match(r"\w", a[ea + R]):
        R += 1
    return a[p - L:ea + R], b[p - L:eb + R], p - L


ITEMS = [
 dict(id="conj-01", domain="policy", old="must", new="should",
  anchor="Officers must complete the mileage return",
  before="""Kingsmere Borough Council — Site Visit Travel Policy

Officers travelling to inspection sites within the borough book transport through the central desk at least two working days ahead. Where a site lies beyond the boundary, the journey is approved by the line manager before booking. Officers must complete the mileage return within five working days of the visit, using the sheet issued by the finance team. Receipts for parking and tolls are attached to the same return. Where a journey is cancelled after booking, the desk is notified the same day so the reservation can be released. The travel desk reviews outstanding returns each month and contacts officers whose returns remain open."""),

 dict(id="conj-02", domain="policy", old="shall", new="may",
  anchor="The hirer shall report the meter reading",
  before="""Harrowfield Water Authority — Standpipe Hire Policy

Contractors hiring a standpipe collect the fitting from the Eastgate depot and return it to the same counter at the end of the hire. Hire runs in fourteen-day blocks and is extended once by telephone. The hirer shall report the meter reading to the depot at the close of each block, quoting the hire number printed on the collar. Damaged fittings are exchanged at the counter and the exchange is noted against the hire number. Deposits are refunded within ten working days of return. The depot publishes a list of open hires each Friday so that overdue fittings can be chased by the district team."""),

 dict(id="conj-03", domain="policy", old="encouraged", new="required",
  anchor="Students are encouraged to submit a written reflection",
  before="""Nettlebridge College — Placement Debrief Policy

Students returning from an industrial placement meet their academic tutor within three weeks of the final day on site. The tutor writes a short summary of the meeting and files it with the placements office. Students are encouraged to submit a written reflection of no more than one thousand words before the meeting takes place. The placements office keeps a schedule of returning students and issues reminders four weeks ahead of each date. Where a placement ends early, the tutor is told by the office rather than by the student. Summaries are held for the length of the course and then destroyed under the retention schedule."""),

 dict(id="conj-04", domain="manual", old="should", new="must",
  anchor="The duty technician should note the start and finish times",
  before="""Bellhaven Leisure Centre — Pool Plant Manual: Backwash

Backwashing is carried out on Tuesday and Friday mornings before the pool opens to the public. Isolate the circulation pump at the local switch and confirm that the pressure gauge has fallen below one bar. Open the waste valve fully and run the reverse flow until the sight glass clears, which normally takes four minutes. The duty technician should note the start and finish times on the plant sheet mounted beside the panel. Close the waste valve, restore the circulation pump, and allow the filter to settle for ten minutes before chemical dosing resumes. Report any gauge reading above two bars to the centre engineer the same morning."""),

 dict(id="conj-05", domain="manual", old="may", new="shall",
  anchor="The operator may check the electrolyte level",
  before="""Ardwick Depot — Forklift Charging Manual

Charging takes place in the bay marked with yellow hatching at the north end of the shed. Park the truck square to the wall, apply the handbrake, and switch the key isolator to off before lifting the battery cover. Connect the charger lead to the truck socket first and then to the wall unit. The operator may check the electrolyte level with the dipstick supplied before the charge begins. Leave the cover raised for the whole of the charge so that gas can disperse. Disconnect at the wall unit first when charging finishes. Trucks left on charge overnight are logged on the sheet inside the shed door."""),

 dict(id="conj-06", domain="manual", old="required", new="encouraged",
  anchor="Technicians are required to log the lamp type",
  before="""Colverton Museum — Display Case Manual: Lamp Replacement

Lamps in the upright cases are changed by two people working together, one at the glass and one at the ladder foot. Switch off the case at the wall isolator and allow fifteen minutes for the housing to cool. Wear cotton gloves throughout so that the new lamp is not marked by handling. Technicians are required to log the lamp type and the case number on the sheet kept in the workshop. Reseat the housing until the catch clicks and check the beam angle from the visitor side of the glass. Spent lamps go into the labelled bin beside the workshop bench for collection by the estates contractor."""),

 dict(id="conj-07", domain="notice", old="must", new="should",
  anchor="Holders must carry cans to the standpipe",
  before="""Notice to Allotment Holders — Water Trough Closure

The trough at the Bramley Lane entrance is out of use from the fourth of March while the supply pipe is relaid. Water is available from the standpipe beside the store hut, which is open during the same hours as the site. Holders must carry cans to the standpipe rather than run hoses across the path, as the contractor's plant is working along that line. The store hut key is held by the site secretary and by the two committee members listed on the board. Work is expected to finish before the end of the month, and a further notice will be posted when the trough reopens."""),

 dict(id="conj-08", domain="notice", old="may", new="shall",
  anchor="Residents may book a collection",
  before="""Notice to Residents — Bulky Waste Collection, Fenwick Estate

A bulky waste round will run on the second Wednesday of each month from March until October. Items are left in the marked bay behind block C between six in the evening and eight the following morning, and not on the landings or the stairwell. Residents may book a collection through the estate office by the Friday before the round. Mattresses are wrapped in plastic sheeting, which the office supplies free of charge on request. Fridges and freezers are taken only when booked in advance, because they travel on a separate vehicle. Items left in the bay outside these hours are removed by the caretaker."""),

 dict(id="conj-09", domain="notice", old="required", new="encouraged",
  anchor="Patients are required to name their chosen pharmacy",
  before="""Notice to Patients — Repeat Prescription Ordering, Weirbank Surgery

From the first of April repeat prescriptions are ordered through the online portal or by posting the tear-off slip into the box in the entrance hall. Orders take two full working days to prepare, and the surgery is closed on Wednesday afternoons. Patients are required to name their chosen pharmacy when placing an order so that the script travels to the right counter. Telephone orders are no longer taken, as the line is needed for appointments. The reception team will help anyone who has not used the portal before, and printed guides are available at the desk in large type on request."""),

 dict(id="conj-10", domain="handbook", old="should", new="must",
  anchor="Lead teachers should carry the printed contact sheet",
  before="""Thornbury Academy — Staff Handbook: Educational Visits

Every visit off the school site is entered on the visits calendar at least six weeks before departure, together with the name of the lead teacher. The lead teacher prepares the assessment on the standard form and passes it to the educational visits coordinator for signature. Parents receive the letter and consent slip no later than three weeks before the date. Lead teachers should carry the printed contact sheet for the group in addition to the copy held in the school office. Coaches are booked through the approved supplier list held by the business manager. On return, the lead teacher tells the coordinator of anything that would change the assessment next time."""),

 dict(id="conj-11", domain="handbook", old="shall", new="may",
  anchor="A tenant shall seek written consent",
  before="""Ravensworth Housing Trust — Tenant Handbook: Garden Upkeep

Tenants look after the garden and any hedge that falls inside the boundary of the property. Grass is cut often enough to stay below thirty centimetres, and cuttings are composted or taken to the district tip rather than left at the kerb. A tenant shall seek written consent from the trust before removing a mature tree or laying a hard surface over more than a quarter of the plot. Fences on the boundary line belong to the trust and are repaired by the trust on report. Where a tenant is unable to keep the garden through ill health, the estate officer arranges help through the tenancy support team."""),

 dict(id="conj-12", domain="handbook", old="encouraged", new="required",
  anchor="Students are encouraged to circulate a short agenda",
  before="""Marlow Institute — Research Student Handbook: Supervision Meetings

Supervision meetings are held at least once a month during the first year and at least once each term thereafter. The student and the supervisor agree the date at the close of the preceding meeting. Students are encouraged to circulate a short agenda to the supervisory team two working days before each meeting. Notes are written by the student, agreed by the supervisor, and uploaded to the graduate school portal within a week. Where a supervisor is away for longer than a month, the second supervisor takes the meetings. The graduate school reviews attendance at the end of each session and contacts pairs whose meetings have lapsed."""),
]


def check(text, pats, ident, where):
    for p in pats:
        m = re.search(p, text, re.I)
        assert not m, f"{ident}: banned term {m.group(0)!r} in {where}"


def build():
    rows, report = [], []
    for it in ITEMS:
        ident, before, old, new = it["id"], it["before"], it["old"], it["new"]

        # (4) licensed pair
        assert frozenset({old, new}) in PAIRS, f"{ident}: unlicensed pair {old}/{new}"

        # (1) the modal occurs exactly once, word-bounded
        occ = len(re.findall(rf"\b{old}\b", before))
        assert occ == 1, f"{ident}: modal {old!r} occurs {occ}x in before"
        # the replacement word must not already occur (keeps the doc's texture identical)
        occ2 = len(re.findall(rf"\b{new}\b", before))
        assert occ2 == 0, f"{ident}: replacement {new!r} already occurs {occ2}x in before"

        # (2) after is that one substitution and nothing else
        after, n = re.subn(rf"\b{old}\b", new, before)
        assert n == 1 and after != before, f"{ident}: substitution count {n}"

        # (3) independent single-span verification via LCP/LCS + word expansion
        sa, sb, start = span_of(before, after)
        assert sa == old and sb == new, f"{ident}: span {sa!r}->{sb!r} != {old!r}->{new!r}"
        assert len(sa.split()) == 1 and len(sb.split()) == 1, f"{ident}: span not one word"
        # contiguity: reconstruct before from after using exactly this one span
        assert before[:start] + sb + before[start + len(sa):] == after, f"{ident}: not contiguous"

        # (4) span uniqueness in before
        assert len(re.findall(rf"\b{re.escape(sa)}\b", before)) == 1, f"{ident}: span not unique"

        # (6) no kind-name word inside the changed span
        check(sa, VOCAB + VALENCE, ident, "changed span (before)")
        check(sb, VOCAB + VALENCE, ident, "changed span (after)")

        # anchor sanity: the declared anchor sentence fragment is present and unique
        assert before.count(it["anchor"]) == 1, f"{ident}: anchor not unique"

        # (7) title line + word band
        lines = before.split("\n")
        assert len(lines) >= 3 and lines[1] == "", f"{ident}: no title line + blank"
        assert 4 <= len(lines[0].split()) <= 14, f"{ident}: title length"
        body_w = len(before.split())
        assert 90 <= body_w <= 140, f"{ident}: {body_w} words (need 90-140)"
        assert len(after.split()) == body_w, f"{ident}: word count changed"

        # (5) vocabulary / valence
        site = (f"In the sentence beginning “{it['anchor'].split(',')[0]}”, the word "
                f"“{old}” in the earlier version reads “{new}” in the later version; "
                f"the sentence is otherwise identical.")
        note = ("Deontic modal strength only: the governed action, who it binds, its scope and "
                "timing, and every other word are identical between versions.")
        for t, w in ((before, "before"), (after, "after")):
            check(t, VOCAB + VALENCE, ident, w)
        for t, w in ((site, "variation_site"), (note, "author_note")):
            check(t, VALENCE, ident, w)

        rows.append({"id": ident, "kind_target": "TEST", "domain": it["domain"],
                     "ambiguous_with": None, "difficulty": "test", "part": "CONJ",
                     "before": before, "after": after,
                     "variation_site": site, "author_note": note})
        report.append((ident, it["domain"], f"{old} -> {new}", body_w))

    with open(OUT, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"ALL CHECKS PASS — wrote {len(rows)} items to {OUT}\n")
    print(f"{'id':<9}{'domain':<10}{'span':<26}{'words'}")
    for r in report:
        print(f"{r[0]:<9}{r[1]:<10}{r[2]:<26}{r[3]}")
    return 0


if __name__ == "__main__":
    sys.exit(build())
