/-
CIRISOntology.Core.Instrument — the twelve-instrument suite, with its honesty
enforced the way this repository enforces honesty: at construction.

One instrument per `ChoiceKind`, each a hybrid of heuristic labeling functions
and (where needed) a validated semantic judge, combined Snorkel-style. This file
carries the FORMAL skeleton — what an instrument owes before it may fire, and
what the suite may not claim before validation. The operational design is
`scratchpad/INSTRUMENT_SUITE_DESIGN.md`; the executable v0 of the four
heuristic-dominant instruments is `scratchpad/instruments/v0.py`.

Three commitments, enforced by type rather than review:

1. **Coordinate typing.** A reading of a frame-dependent kind cannot be
   constructed without its frame; a design-dependent kind, without its design
   (`Reading.frameSupplied` / `designSupplied`). This is `repairable_does_not_factor`
   compiled into the instrument layer: for `Record` there is nothing in the
   artifact alone to read, so an instrument that fires framelessly is not
   cautious, it is WRONG — it must refuse. Same for `Circumstances` and design.

2. **The suite ships unvalidated, and says so by theorem.** `validated` is a
   recorded commitment in the `Gate.mechanized` style — it may only become true
   when an XV-series bake-off clears the floor (kappa CI lower bound >= 0.70
   against a two-annotator ceiling, prevalence-corrected precision at the
   OPERATING point, locked holdout scored once). At this commit every entry is
   false, and `suite_ships_unvalidated` pins that as a fact a later edit must
   consciously break — flipping a flag without a bake-off shows up in the diff
   of a theorem, not a table cell.

3. **Every kind is covered** (`suite_covers_every_kind`), so a kind without an
   instrument cannot silently drop out of the programme.

The XV constraints this design inherits (RATCHET, judge series): prompt
architecture is not the lever; the judge MODEL is the lever and does not
generalize across axes — twelve bake-offs, not one; a corpus must encode the
construct — the PLANE study's authored pairs are the corpus factory.
-/

import CIRISOntology.Core.WrongKind

namespace CIRISOntology.Core

/-- A classification reading, with its coordinates supplied where the kind
    requires them. The obligations make a frameless `testimonial` reading or a
    designless `contingent` reading UNCONSTRUCTIBLE — the instrument-layer form
    of refuse-rather-than-guess. -/
structure Reading where
  kind : ChoiceKind
  frame : Option Frame
  design : Option Design
  frameSupplied : kind.frameDependent = true → frame.isSome = true
  designSupplied : kind.designDependent = true → design.isSome = true

/-- A Record reading always carries its frame. -/
theorem reading_record_has_frame (r : Reading) (h : r.kind = .testimonial) :
    ∃ f, r.frame = some f := by
  have hf := r.frameSupplied (by rw [h]; rfl)
  cases hr : r.frame with
  | none => rw [hr] at hf; simp at hf
  | some f => exact ⟨f, rfl⟩

/-- A Circumstances reading carried a design-obligation while `contingent` was
    claimed design-mobile. That claim was RETRACTED by the PLANE study's pinned
    outcome (see `WrongKind.designDependent`), so `designSupplied` is now
    vacuous for every kind and the theorem below records the retraction's
    consequence instead: no kind's READING owes a design any longer; the
    design-relativity lives in the DISPOSITION verdict, not the reading. -/
theorem no_reading_owes_design (r : Reading) :
    r.kind.designDependent = false := by
  cases hk : r.kind <;> rfl

/-- One instrument. `heuristics` and `judgeRole` are the operational content
    (documented, not proved); `validated` is the honesty flag, `Gate.mechanized`
    style — a recorded commitment whose flip requires a cleared bake-off. -/
structure InstrumentSpec where
  kind : ChoiceKind
  heuristics : List String
  judgeRole : String
  corpus : String
  validated : Bool

/-- The suite: twelve instruments, one per kind, in the published order.
    Heuristic content summarized; the operational detail lives in the design
    document and the v0 implementation. -/
def suite : List InstrumentSpec :=
  [ ⟨.structural,  ["parse-check", "schema-validate", "dispatch-resolve"],
      "NONE — the heuristic is the discriminator", "PLANE + synthetic breakage", false⟩
  , ⟨.procedural,  ["step-graph diff vs declared orchestration"],
      "tie-break on reordered-but-equivalent flows", "PLANE + workflow corpus", false⟩
  , ⟨.contingent,  ["membership lookup in the DECLARED design's held-fixed set"],
      "NONE — design-relative by definition", "PLANE design-swap conditions", false⟩
  , ⟨.testimonial, ["Repairable(fact, frame): re-derivability against the DECLARED frame"],
      "is the unrecoverable loss load-bearing", "PLANE frame-swap conditions", false⟩
  , ⟨.empirical,   ["claim extraction", "retrieval check against named sources"],
      "verdict on contested retrievals", "FEVER-style + PLANE", false⟩
  , ⟨.deontic,     ["modal/permission lexicon", "norm-extraction patterns"],
      "obligation-vs-permission boundary calls", "legal-NLP corpora + PLANE", false⟩
  , ⟨.epistemic,   ["hedge/certainty lexicon (CoNLL-2010 family)"],
      "warranted-confidence shifts without lexical hedges", "hedge corpora + PLANE", false⟩
  , ⟨.pragmatic,   ["register/formality classifier", "address-form detector"],
      "manner-vs-content boundary calls", "formality corpora + PLANE", false⟩
  , ⟨.ontological, ["entity-typing diff", "is-a assertion extraction"],
      "identity claims made obliquely", "typing corpora + PLANE", false⟩
  , ⟨.axiomatic,   ["premise/assumption detection (argument mining)"],
      "foundational-vs-incidental premise calls", "argument corpora + PLANE", false⟩
  , ⟨.axiotic,     ["comparative/priority language patterns"],
      "PRIMARY — re-ranking is judge territory", "PLANE axiotic strata", false⟩
  , ⟨.nomological, ["applied-framework citation patterns"],
      "PRIMARY — and the Model-vs-Facts trap is the corpus's job to load", "PLANE boundary items", false⟩
  ]

/-- Every kind has its instrument. A kind cannot silently drop out. -/
theorem suite_covers_every_kind (k : ChoiceKind) :
    ∃ i ∈ suite, i.kind = k := by
  cases k <;> simp [suite]

/-- THE HONESTY PIN: at this commit, nothing is validated. Flipping any flag
    breaks this theorem, so validation claims arrive as conscious diffs of a
    proof obligation, never as quiet table edits. The bake-off that earns a
    flip is specified in the design document, XV floors verbatim. -/
theorem suite_ships_unvalidated : ∀ i ∈ suite, i.validated = false := by
  simp [suite]

end CIRISOntology.Core
