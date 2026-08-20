# POLARITY execution note — decisions pinned BEFORE any item is scored (2026-08-20)

`POLARITY_PREREG.md` GOVERNS. This file records only the operationalisations the prereg
leaves open, fixed here before a single polarity judgment exists. Written before
`polarity_score.py` was ever invoked; no polarity data existed at the time of writing.

**D1 — span extraction.** Longest-common-prefix / longest-common-suffix decomposition on
word tokens: the span runs from the start of the first non-`equal` diff block to the end of
the last. Single-span check = the resulting span is non-empty and does not degenerate to the
whole artifact. **All 272 items pass; none dropped.** 184 items have one contiguous
word-level block inside the span; 88 have 2–6 (re-orderings, unit-factorings, formula
rewrites — one *change* whose surface is interleaved, e.g. `procedural-report-03`,
`structural-report-02`). Internal block count is reported as a diagnostic, not a drop rule,
because dropping on it would delete most of Priorities, Process and Structure, whose axes
are re-ordering axes by definition.

**D2 — which kind's §1 rule frames the polarity question.** The item's **authored target
kind** (`kind_target`), NOT the panel's BASE modal. Reason: P2's outcome variable is the
panel's read label; if the polarity prompt were framed by that same read label, the new
variable would be entangled with the outcome and any asymmetry would be uninterpretable.
The authored target is fixed by the corpus and independent of the panel.

**D3 — CONJ items.** `conj_items.jsonl` carries `kind_target: "TEST"`; every item's own
`author_note` reads "Deontic modal strength only", and all twelve are modal-strength edits
(must/shall/required ↔ should/may/encouraged). Axis = **Rules**. Primary analysis includes
them; a sensitivity excluding all CONJ items is reported alongside.

**D4 — confusion matrix orientation.** Rows = authored target kind, columns = BASE-condition
panel modal, matching `TWO_WAY_READING.md` ("BASE modal vs authored target, ties excluded").
"Ties excluded" = items with no plurality among the three BASE votes (all three distinct).

**D5 — P2 pooled statistic.** For each qualifying kind, TVD between the read-label
distribution of its `+` items and that of its `-` items. **Primary read distribution = the
full confusion-matrix row** (every read label, the correct one included), because the prereg
glosses "the error distribution" as "(which kind the panel read it as)". **Pooling =
unweighted mean over qualifying kinds** (the question is about the taxonomy's kinds, so each
kind counts once). Pre-specified sensitivities, reported whatever they show: (i) errors-only
rows (read ≠ target), (ii) n-weighted pooling, (iii) CONJ excluded.
Null: 2,000 permutations of the polarity labels **within kind**; p = (1 + #{null ≥ obs})/2001.

**D6 — UNDERPOWERED, evaluated before any p-value.** Declared UNDERPOWERED if EITHER
(a) fewer than 4 kinds have ≥ 8 scoreable items in **both** polarities, OR
(b) `sd(null) > 1 − mean(null)` — the null's spread exceeds the room left between the null's
centre and the statistic's maximum attainable value (1 for a TVD mean), i.e. no observation
could be resolved against it.
Enforced by construction: `analyse_power.py` writes `power.json` and prints NO p-value;
`analyse_p.py` runs only after, and refuses to run if `power.json` is absent.

**D7 — P3 operationalisation.** The measured twin asymmetry is Structure→Manner 7 vs
Circumstances→Manner 1. Conditioning on sign = stratify the 2×2 (target ∈ {Structure,
Circumstances}) × (read = Manner vs read ≠ Manner) on polarity, and test with
Cochran–Mantel–Haenszel plus per-stratum Fisher exacts; also report the Structure-vs-
Circumstances polarity imbalance directly (that is the mechanism by which it *could* be an
artifact). SURVIVES = the stratified association keeps its direction and significance;
VANISHES = the association is carried by the polarity imbalance and dies within strata.
The Structure→Manner / Circumstances→Facts pair from `TWO_WAY_READING.md` is reported in
full as a 2×2×2 table so the reader can check both channels.

**D8 — polarity modal.** Plurality of the three model votes; all three distinct → AMBIGUOUS
(prereg: "ties -> AMBIGUOUS"); two parsed votes that disagree → AMBIGUOUS; fewer than two
parsed votes → counted as a parse failure against the 5% VOID rate.

**D9 — spend.** Hard cap $0.30 enforced in the runner, real spend read from usage fields.

**D10 — Record has no axis in the frozen table, and none is invented.** §1 defines polarity
for **eleven** kinds; `Record` (testimonial) has no row. The corpus the prereg names contains
**20 Record items**. Inventing a twelfth axis after freeze would be unfreezing the prereg, so
those 20 items are **not scored**: they are carried as *axis undefined by the prereg* and
reported at full volume. Consequence, stated in advance: the scored corpus is **252** items,
not 272. P1's AMBIGUOUS rate is reported primarily over the 252 items whose axis the prereg
defines (P1 asks whether the construct is scoreable, and the construct only exists for those
eleven), and secondarily over all 272 with Record counted as undefined. The §4 VOID floor
("fewer than 150 scoreable items") is applied to the actual scoreable count either way.
