# The Twelve-Instrument Suite — design, on the XV foundations

One hybrid heuristic–semantic instrument per `ChoiceKind`. Formal skeleton:
`Core/Instrument.lean` (coordinate typing enforced at construction; the suite pinned
unvalidated by theorem). Executable v0 of the four heuristic-dominant instruments:
`instruments/v0.py`, shipping with its own dye tests (11/11 at commit).

**Scope, per the steward: bigger than AI safety alone.** The suite classifies consequential
change in ANY artifact system — policy documents, law, code, configuration, records,
scientific claims. AI-safety trace evaluation (H3ERE blocks) is one application; change
audit, evidence-registry review, and anomaly triage (`GATES.md`) are others. The muon g−2
case is the standing demonstration of what mis-routing a wrong costs.

## Architecture

Snorkel-style per kind: heuristic labeling functions + judge labeling functions + coordinate
checks, combined by a label model learned from agreements/disagreements — never a single
prompt pretending to be an instrument. Three verdicts everywhere: FIRES / CLEAN /
**REFUSED** — the third is first-class, and coordinate-missing inputs always take it.

## The twelve, by build order

| # | kind (plain) | heuristic core | judge role | class |
|---|---|---|---|---|
| 1 | Structure | parse/schema/dispatch checks | none — heuristic IS the discriminator | **built (v0)** |
| 2 | Process | step-graph diff vs declared orchestration | reordered-but-equivalent tie-breaks | **built (v0)** |
| 3 | Circumstances | membership in DECLARED design's held set | none — design-relative by definition | **built (v0)** |
| 4 | Record | `Repairable(fact, frame)` — theorem-backed | is the unrecoverable loss load-bearing | **built (v0)** |
| 5 | Facts | claim extraction + retrieval vs named sources | contested retrievals | hybrid |
| 6 | Rules | modal/permission lexicons, norm extraction | obligation-vs-permission boundaries | hybrid |
| 7 | Confidence | hedge/certainty lexicons (CoNLL-2010 family) | unhedged warranted-confidence shifts | hybrid |
| 8 | Manner | register/formality classifiers | manner-vs-content boundaries | hybrid |
| 9 | Identity | entity-typing diff, is-a extraction | oblique identity claims | hybrid |
| 10 | Premises | argument-mining premise detection | foundational-vs-incidental calls | hybrid |
| 11 | Priorities | comparative/priority patterns | PRIMARY | judge-led |
| 12 | Model | applied-framework citation patterns | PRIMARY — Model-vs-Facts trap loaded in corpus | judge-led |

## Validation — the XV floors, verbatim, twelve times

Per instrument: κ CI **lower bound** ≥ 0.70 against a two-annotator human ceiling ·
prevalence-corrected precision reported at the **operating** point (the care-axis lesson:
86% → 42% under prevalence inversion) · locked holdout the harness refuses to score twice ·
its own bake-off (XV finding 2: the judge MODEL is the lever and does not generalize across
axes — the worst refusal model was the best care model). Plain direct prompts (finding 1:
architecture is not the lever). Corpus from the PLANE study's authored, adjudicated,
prevalence-balanced pairs (finding 3: the corpus must encode the construct — the boundary
items for Confidence/Facts and Model/Facts are already designed in).

**Honest outcome expected and pre-accepted:** some instruments will fail validation. A suite
shipped "9 validated, 3 open, each with its measured floor" is a result, per the care-axis
precedent. `suite_ships_unvalidated` in the Lean makes any validation claim arrive as a
conscious diff of a theorem, never a quiet table edit.

## Dependencies and order

PLANE study (corpus factory) → bake-offs for 5–10 → judge-led 11–12 last, with the largest
corpora. The four built instruments generate weak labels for the rest from day one.
Cross-check harness: the anomaly-triage sweep (vary warrant/frame/design, watch label
mobility) runs over the suite's own outputs — the instruments and the triage gate validate
each other.
