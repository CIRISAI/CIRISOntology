# The broken fit-conjugation's empirical test — RESULTS (2026-08-20)

Executed against `CONJUGATION_TEST_PREREG.md` (frozen 2026-08-20; items authored after the
freeze, by `plane_corpus/conj_author.py`). No gate was moved, no threshold reinterpreted.

## VERDICT: forced-collapse resolution (b) CONFIRMED — Rules modal on 12 of 12

The frozen meaning: *"Modal label **Rules on >= 9 of 12**: the forced-collapse resolution (b)
is CONFIRMED as the panel's reading — deontic strength IS content; the broken conjugation is
a theorem about satisfaction-conditions, not an omission; `kinds-from-sites` survives its own
internally-generated challenge and gains a sentence."*

Rules is the modal label on **12 of 12** items — the maximum, against a threshold of 9.
Confidence is the modal label on **0** items, against a hidden-site threshold of 4. The
hidden-directive-strength prong (a) is **not alive** by the test's own frozen meaning; no
escalation to the steward is triggered, and `basePlane_card = 11` is not challenged by this
instrument.

The panel reads a change in deontic modal strength as a change in **what counts as
compliance**, not as modulation of a claim. `kinds-from-sites` survives an internally
generated challenge to the exact kill it stakes.

## VOID gates — all discharged, none fired

| gate (frozen wording) | outcome |
|---|---|
| any item failing single-span verification is dropped | **0 dropped** — all 12 passed on first authoring pass |
| below 9 surviving items the test is VOID | **12 surviving** |
| off-taxonomy modal on >2 items voids (legibility) | **0 off-taxonomy modals**; 0 NO FIT, 0 unparsed responses in 36/36 judgments |
| ties excluded per the standing convention | **0 ties** — every item had a strict plurality |

Single-span verification was mechanical and independent of the declaration: minimal LCP/LCS
diff, expanded to word boundaries, was required to be exactly one word on each side, to be a
licensed modal pair, to be unique in `before` under word-bounded matching, and to reconstruct
`after` exactly by that one contiguous substitution. Additionally enforced: the replacement
modal must not already occur anywhere in `before` (so the document's modal texture is
otherwise untouched), the standing corpus ban on taxonomy vocabulary in artifact text and on
valence words anywhere, word count 90–140, and a title line.

## Per-item result

Vote order is Llama-4-Scout-17B-16E / gpt-oss-120b / gemma-3-27b-it. Condition BASE only.

| id | domain | before → after span | the governed sentence (BEFORE) | votes | modal |
|---|---|---|---|---|---|
| conj-01 | policy | `must` → `should` | Officers **must** complete the mileage return within five working days of the visit, using the sheet issued by the finance team. | Rules, Rules, Confidence | **Rules** |
| conj-02 | policy | `shall` → `may` | The hirer **shall** report the meter reading to the depot at the close of each block, quoting the hire number printed on the collar. | Rules, Rules, Rules | **Rules** |
| conj-03 | policy | `encouraged` → `required` | Students are **encouraged** to submit a written reflection of no more than one thousand words before the meeting takes place. | Rules, Rules, Rules | **Rules** |
| conj-04 | manual | `should` → `must` | The duty technician **should** note the start and finish times on the plant sheet mounted beside the panel. | Rules, Rules, Rules | **Rules** |
| conj-05 | manual | `may` → `shall` | The operator **may** check the electrolyte level with the dipstick supplied before the charge begins. | Rules, Rules, Rules | **Rules** |
| conj-06 | manual | `required` → `encouraged` | Technicians are **required** to log the lamp type and the case number on the sheet kept in the workshop. | Rules, Rules, Rules | **Rules** |
| conj-07 | notice | `must` → `should` | Holders **must** carry cans to the standpipe rather than run hoses across the path, as the contractor's plant is working along that line. | Rules, Rules, Confidence | **Rules** |
| conj-08 | notice | `may` → `shall` | Residents **may** book a collection through the estate office by the Friday before the round. | Rules, Rules, Rules | **Rules** |
| conj-09 | notice | `required` → `encouraged` | Patients are **required** to name their chosen pharmacy when placing an order so that the script travels to the right counter. | Rules, Rules, Manner | **Rules** |
| conj-10 | handbook | `should` → `must` | Lead teachers **should** carry the printed contact sheet for the group in addition to the copy held in the school office. | Rules, Rules, Rules | **Rules** |
| conj-11 | handbook | `shall` → `may` | A tenant **shall** seek written consent from the trust before removing a mature tree or laying a hard surface over more than a quarter of the plot. | Rules, Rules, Rules | **Rules** |
| conj-12 | handbook | `encouraged` → `required` | Students are **encouraged** to circulate a short agenda to the supervisory team two working days before each meeting. | Rules, Rules, Rules | **Rules** |

Design balance, as authored: four items per modal pair (must/should, shall/may,
required/encouraged); three items per domain; six strengthening and six weakening.

## Distributions

Modal labels (plurality of 3, ties excluded), n = 12:

| modal label | items | share |
|---|---|---|
| Rules | 12 | 100% |
| Confidence | 0 | 0% |
| every other kind | 0 | 0% |
| tie / excluded | 0 | 0% |

Individual votes, n = 36:

| label | votes | share |
|---|---|---|
| Rules | 33 | 91.7% |
| Confidence | 2 | 5.6% |
| Manner | 1 | 2.8% |
| NO FIT / off-taxonomy / unparsed | 0 | 0% |

Per model, n = 12 each:

| model | Rules | Confidence | Manner |
|---|---|---|---|
| meta-llama/Llama-4-Scout-17B-16E-Instruct | 12 | 0 | 0 |
| openai/gpt-oss-120b | 12 | 0 | 0 |
| google/gemma-3-27b-it | 9 | 2 | 1 |

Secondary labels were offered by the prompt (multi-label permitted when "genuinely
irreducible") and **no judge used one on any item**: `second` is null in all 36 judgments.
The panel did not treat these changes as sitting between two kinds.

## Sub-threshold observations (recorded, not verdicts)

These do not move the verdict and no threshold was staked on them. They are recorded because
they are the only structure in the residual.

1. **All three non-Rules votes came from one model** (gemma-3-27b-it), so at the level of
   model families the reading is 2 of 3 unanimous and the third is 9/12. Per the standing
   convention that same-family annotators are one witness, this is one witness dissenting in
   part, not a distributed signal.

2. **All three non-Rules votes fell on WEAKENING items** — conj-01 (`must`→`should`),
   conj-07 (`must`→`should`), conj-09 (`required`→`encouraged`). That is 3 of the 6
   weakening items drawing a dissenting vote against 0 of the 6 strengthening items. The
   dissent reasons name the asymmetry explicitly: *"a lowered degree of obligation or
   certainty"* (conj-07), *"shifting from a mandate to a suggestion"* (conj-09). If deontic
   strength were pure content this direction-asymmetry would not be expected; a single
   annotator's 3/6 vs 0/6 on n = 12 is far too thin to support anything, and no advance
   prediction was staked on direction, so under discipline rule 6 this is **not support**
   for anything. It is a candidate for a future pre-registered instrument, nothing more.

3. **The Confidence votes read the modal epistemically, not deontically** — gemma's conj-01
   reason blends the two readings in one sentence ("the degree of obligation *or certainty*"),
   which is the Rules/Confidence boundary behaving exactly as the symmetry analysis predicted
   it would if it were contested. It was contested by 2 votes in 36.

## Scope and limits

- **Model panel only.** Three model families, BASE condition, one judgment each. No human
  annotator saw these items; the human ceiling owed to the PLANE study is owed here too.
- **Authored items, single author.** The twelve documents were written by the same author in
  one pass to a frozen recipe. Mechanical checks constrain the span, not the prose.
- **One condition.** BASE only, as the prereg specifies. The retention and design frames (F1,
  F2, D1, D2) and the provenance frames (W2, W3) were not run, so nothing here speaks to
  whether the reading is frame-stable.
- **A panel's reading is not a theorem.** The verdict is that the panel reads deontic strength
  as content. The prereg's resolution (b) is a claim about satisfaction-conditions; this test
  confirms it *as the panel's reading*, which is what the frozen meaning says it confirms, and
  not more.

## Provenance and spend

| | |
|---|---|
| prereg | `/home/emoore/CIRISOntology/scratchpad/CONJUGATION_TEST_PREREG.md` (frozen before items existed) |
| authoring + self-check | `/home/emoore/CIRISOntology/scratchpad/plane_corpus/conj_author.py` |
| items | `/home/emoore/CIRISOntology/scratchpad/plane_corpus/conj_items.jsonl` (12 items, all passing) |
| judgments | `/home/emoore/CIRISOntology/scratchpad/plane_corpus/conj_judgments.jsonl` (36 judgments) |
| runner | `plane_annotate.py`, unmodified; condition BASE, 3 models, temperature 0, 6 workers |
| tokens | 25,758 in / 3,065 out |
| **spend** | **$0.00347** against a $0.10 cap (cap enforced in-process at 0.10, never approached) |
| items dropped | **none** |
