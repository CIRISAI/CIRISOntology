# Lean v2 — the taxonomy as anvil (season design note, 2026-08-18)

Direction set by the steward: reorient the Lean around the 11+1 so it FORCES the
confrontation with math/physics/chemistry; if it survives, categorize the encyclopedia;
if that is clean, the Lean forces the PLANE characteristics as logical statements.
This note is the design. Nothing here touches the page; preregs freeze before data.

## Phase 1 — the confrontation corpus (documented historical changes)

`Core/Confront/{Math,Physics,Chemistry}.lean`: each entry is a documented, datable change
in the history of a hard science, forced through the `Reading` type — construct the
Reading with its coordinates, or exhibit a typed obstruction. A NO-FIT stops being a
survey answer and becomes a type error in public.

Candidate set (each with its primary source to be pinned before encoding):

| change | staked kind | why it bites |
|---|---|---|
| SI 2019: kilogram from artifact to constant | Premises | the ripple is COMPUTABLE: every derived unit inherits; the instrument's conjunction gets a wild test |
| IAU 2006: Pluto reclassified | Identity | our registry recipe in the wild — world unchanged, criteria adopted, entity re-carried |
| CODATA adjustment cycles | Facts | pure value updates; must NOT read as Premises despite touching constants |
| IUPAC 2009: atomic weights become intervals | Confidence | a precision statement changed, not a value — the hedge sits in the number's TYPE |
| element naming (104–109 wars; 2016 finals) | Identity/Manner | declaration-performed naming, the registry site |
| phlogiston → oxygen | Model | framework replacement with facts re-carried |
| adoption/independence of Choice (AC) | Premises | the mathematical Premises case, ripple = every theorem tagged AC |
| Bourbaki definition reforms (function-as-graph) | Structure/Premises | the boundary the panel confuses, encoded |
| notation reform (Leibniz/Newton; ≤ conventions) | Manner | content-preserving re-expression at scale |
| Wiles 1993→1995 gap repair | Process | the proof's steps changed; the theorem did not |
| Mochizuki–abc acceptance dispute | **Record** | the jewel: whether the proof is re-derivable is FRAME-RELATIVE (which community); `repairable_does_not_factor` in the wild |
| leap seconds / calendar reform | Circumstances/Premises | held-fixed set membership, design-declared |

Success criterion (staked): every entry constructs, and the kind assignments survive
adversarial review; the kill is a documented change that CANNOT construct and whose
obstruction is not the Record relation — that is a twelfth category candidate and the
taxonomy's own bounty fired from inside.

## Phase 2 — the encyclopedia

Scale `eco_sample_wiki2.py` (whole-paragraph, one-clean-paragraph gate) to thousands;
heuristic instruments prefilter, panel on a stratified sample. External bake-off: map the
Yang et al. (EMNLP 2017) 13-intention labeled corpus onto the 11+1 where determinate;
their classifier's F1 0.621 is the published bar on that substrate.

## Phase 3 — PLANE characteristics as logical statements

- Coordinate-flatness → a typed invariance obligation: a kind-predicate may not read the
  frame (`warrant_invisible_to_kind` style, per-instrument).
- Use/mention → a Force-typed feature: the Facts instrument must carry
  asserted-vs-reported, because the panel's measured failure is mention-as-use (part C/D).
- Record-as-relation → instruments for the 11 are functions of the artifact pair;
  the Record instrument alone takes the frame argument. The type signatures ARE the claim.

## The eigen-alignment experiment (prereg to freeze BEFORE any data)

Motivation, RE-AMENDED 2026-08-18 (steward's correction, same day): the first amendment
over-claimed. The shipped RATCHET audit script is 8-signal by construction and cannot
produce the report's rank-11 — but that shows the report's §2.1 came from a DIFFERENT,
wider analysis (per the steward: a wider corpus, actual values), whose feature list is
not in the release. A reproduction bracket run on everything we hold (8-signal audit;
both scrubbed 6,465-row tables; the 8,530-row production dump; covariance and
correlation variants) straddles the published triple (7, 11, 6.61) without reaching it —
the signature of a curated intermediate signal set, which is affirmative plausibility,
not refutation. Status: the RATCHET leg is REPORTED-BUT-UNPINNED — "three objects share
the integer 11" stands on two PINNED legs (Clifford-algebra cap; site-model image) plus
one unpinned, pinnable the day the original feature list surfaces. k_eff=11.5 remains a
calculation (−ln .01/.4). No annotation of RATCHET's report is owed on current evidence.
Gate registered: a non-reproduction is not a refutation until the original method is pinned. The bridge is runnable:

- **Prediction 1 (alignment):** on a change-describing corpus, the content principal
  directions align with the 11 kinds' one-vs-rest discriminator directions — not 7, not 13.
- **Prediction 2 (the relation's signature):** Record does NOT appear as a twelfth
  direction. It surfaces only as a frame-conditional factor: invisible to any
  artifact-only reading, appearing when the frame is supplied.
  `repairable_does_not_factor`, spoken in PCA.
- Kills, separable: rank far from 11 kills the alignment claim only; a stable twelfth
  content direction that tracks Record kills the relation-typing claim specifically.
- Discipline: prereg freezes estimator, corpus, alignment metric (e.g., CCA between
  discriminator subspace and PCA subspace, permutation-nulled), and BOTH thresholds
  before any embedding is computed. Rule 5 floor: label-shuffled null. Rule 3: the
  corpus's generative structure decides the null's granularity (documents, not tokens).

## Order of work

1. Freeze the eigen-alignment prereg (cheapest, sharpest teeth).
2. Phase-1 skeleton: `Confront.lean` types + three entries end-to-end (SI-2019, Pluto,
   Mochizuki-as-Record) to prove the mold, then fill.
3. Yang-corpus mapping note (external, free labels) before any Phase-2 spend.

## The applied branch

Added 2026-08-18 by the steward's direction: the A-node DAG — the 11+1 as a
verification-budget discipline for the CIRIS Agent (kind-classification DMA, exact
graph-memory ripple, kind-typed WA deferral, Record-typed audit integrity, kind-mix
telemetry) — lives in `APPLIED_BRANCH.md`, dependencies only, kills staked per node.
