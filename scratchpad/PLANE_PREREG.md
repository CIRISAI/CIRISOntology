# PRE-REGISTRATION — the base-plane study: is the taxonomy 11+1 or 10+1+1?

Frozen before any item is written or any annotator recruited. This is the human study that
the claim table in `Core/WrongKind.lean` explicitly defers to: the twenty-four entries of
`frameDependent` / `designDependent` are RECORDED CLAIMS, and this design is what can retire
them. Greenfield: no H3ERE, no agent, no CIRIS harness — artifacts and annotators only.

## 0. The question, and the two shapes it decides between

`classify(artifact, frame, design)`: which labels move when the FRAME moves (what survives
to be re-read), and which move when the COMPARISON DESIGN moves (what is held fixed)?

* **11+1**: eleven artifact-local kinds + frame-relative Record. (`contingent` is a kind.)
* **10+1+1**: ten artifact-local kinds + Record(frame) + Circumstances(design) — a base
  plane with two coordinates, where the two +1s differ in DIFFERENT ways (Record takes an
  argument and asserts content; Circumstances is the marker for the unchosen and asserts
  none — see `contingent_is_the_only_marker` and `marker_matches_disposition`).

**Staked now, per the claim table:** exactly one label moves under frame-variation
(`testimonial`), exactly one under design-variation (`contingent`), ten under neither.
**The at-risk entry, named in advance: `pragmatic`.** "Manner, not content" is a distinction
relative to what the design counts as content; if any base-plane label is design-mobile, it
is this one, and the plane is nine.

## 1. Corpus — greenfield, prevalence-balanced by construction

**Items are variation pairs**: an artifact plus a single localized change, the variation
site marked. Five artifact domains so no domain's habits masquerade as the taxonomy's:
prose policy, structured config (YAML/JSON), code, a factual report, a process description.

* **N = 240 pairs: 20 per kind × 12 kinds**, authored to target the kind, in every domain.
  Prevalence-balanced by construction — the IAA literature's finding that rare categories
  are prevalence-sensitive and unstable in isolation makes an unbalanced natural corpus
  unable to distinguish "frame-mobile" from "under-sampled".
* **Authored ≠ adjudicated.** The targeted kind is a hypothesis, not gold. Gold is the
  modal adjudicated label under the BASELINE condition (below).
* 20% of items are AUTHORED AMBIGUOUS (near a named boundary: confidence/facts,
  model/facts, manner/structure) — borderline concentration is signal, and the boundary
  pairs get their own κ per the two-annotator discipline.

## 2. Treatments — frame and design as crossed factors

Every item is classified under one of five conditions:

| condition | frame declared | design declared |
|---|---|---|
| BASELINE | F0: "everything survives" (full retention) | D0: "everything else held fixed" |
| FRAME-2 | F1: named partial corpus (the artifact's siblings destroyed) | D0 |
| FRAME-3 | F2: named minimal corpus (only the artifact survives) | D0 |
| DESIGN-2 | F0 | D1: a comparison that holds a DIFFERENT subset fixed |
| DESIGN-3 | F0 | D2: a comparison in which the varied element is among the held |

Frames and designs are one paragraph each, written in advance, identical across items.

## 3. Protocol — the three imports, applied

1. **Two-stage, location given.** The variation site is marked in every item; annotators
   judge KIND only. All disagreement is about kind, none about span.
2. **Between-annotator conditions.** No annotator sees the same item under two conditions
   — the in-context-fixation result says a first label anchors a second, and the anchor
   biases TOWARD stability, i.e. toward falsely confirming 11+1. Condition assignment is
   item-randomized; each annotator works one condition per item.
3. **Valence-neutral wording, per the choice inversion.** The prompt is *"what kind of
   change is this?"* with the twelve discriminator questions — never *"what kind of wrong"*.
   Asking for wrongs imports evaluation and costs agreement for nothing.

Annotators: ≥3 per item×condition, working from the public vocabulary + discriminators
(`WrongKind.plain` / `WrongKind.discriminator`), with the two boundary notes
(Confidence/Facts, Model/Facts) included verbatim. Multi-label permitted (composition is a
legal answer); NO-FIT is a recorded outcome routed to adjudication, never a forced choice.

## 4. The measurements

Per kind `k` and treatment axis `T ∈ {frame, design}`:

**MOBILITY(k, T)** := P(modal label ≠ baseline modal label | item authored-and-adjudicated
as `k` under baseline, judged under T's non-baseline conditions).

Report with per-kind κ (binary decomposition), against two floors measured in the same
study: (a) baseline test–retest instability (different annotator triples, same condition —
the free-floating disagreement rate), and (b) the ambiguous-item set scored separately, so
boundary noise cannot masquerade as coordinate-mobility.

**A kind is MOBILE on axis T** iff MOBILITY(k,T) exceeds the baseline instability floor at
p < 0.01 (permutation over condition labels — the null respects the item pairing, per the
under-dispersion lesson: no χ² on correlated readings).

## 5. Outcome meanings, pinned now

| result | reading |
|---|---|
| `testimonial` frame-mobile, `contingent` design-mobile, ten flat | **10+1+1 confirmed as claimed** — the claim table stands entry by entry |
| `contingent` flat under design-variation | it is a genuine artifact property; **11+1 stands**; `designDependent` retracted |
| `pragmatic` (or any base label) mobile on either axis | **the plane is smaller than ten**; the mobile label gains an argument, and the claim table is corrected, not defended |
| `testimonial` mobile under DESIGN too | the two coordinates are not disjoint; `no_label_moves_with_both` retires and the geometry is richer than two orthogonal axes |
| NO-FIT above 10% in any condition | the taxonomy is not fit-for-use on that domain; adjudicate per the four-way resolution tree before any structural conclusion |
| baseline κ < 0.6 on the unambiguous set | **VOID** — the instrument cannot carry the question; report the confusion matrix and stop |

## 5b. AMENDMENT (2026-08-18, before any item authored): the third treatment, and what this study is FOR

**The purpose, sharpened by an external anchor.** The muon g−2 tension — twenty years, 4.2σ,
chased as a world-wrong — dissolved when the prediction's WARRANT was varied (lattice vs the
correlated e⁺e⁻ data basis; `PROJECTION_UPDATE_G2.md`). The wrong was coordinate-borne, not
world-borne, and one coordinate sweep located it. This study validates precisely the
instrument that operation needs: can classifiers reliably detect that a label MOVES under a
coordinate swap? If yes, the anomaly-triage gate (GATES.md) has its validated instrument.

**The WARRANT treatment, added.** Conditions W-2/W-3: identical items with the varied
element ATTRIBUTED to different sources (in-house vs external authority vs anonymous), all
else byte-identical. The formal classifier is PROVABLY blind to this (`warrant_invisible_to_kind`)
— so any movement in human kind-labels under attribution swap is pure annotator authority
bias, a measured human deviation from a proven invariance. Prediction, staked: labels do not
move (the theorem's human shadow). If they do move, the process needs an attribution-masking
step before classification, and this study will have measured exactly how much.

Corpus cost: +2 conditions on the same 240 items, same between-annotator discipline;
judgments 3,600 → 5,040.

## 6. Prior art, carried in

Components convergent, assembly apparently ours (four searches, 2026-08-16): prevalence
sensitivity and borderline concentration (learner-corpus IAA literature), two-stage
location/description, in-context fixation (2605.08295), within-label variation as the
warrant axis observed in the wild (LiTEx 2505.22848), deontic/axiological as standard
meta-ethics vocabulary. The formal cousin of `repairability_not_intrinsic` is
**sheaf-theoretic contextuality** (Abramsky–Brandenburger): a label with no global section
over contexts — one fact, two frames, opposite verdicts — is a contextual classification,
and this study is a contextuality measurement on a taxonomy.

## 7. What this does not decide

Whether the twelve are the RIGHT twelve (exhaustiveness stays "empirically closed", never
proved); whether any variation WAS a choice (`generator_underdetermined` — the exercise of
freedom is exactly what no instrument reads); and nothing here touches TORQUE, whose
classes enter only through the shared vocabulary.

Cost estimate: 240 items × 5 conditions × 3 annotators = 3,600 judgments. At model-annotator
prices this is tens of dollars; at human prices it is a small grant. Run model-annotated
first as the pilot (three model families, per the witness-diversity rule — same-family
annotators are one witness), human-adjudicated on the disagreements.
