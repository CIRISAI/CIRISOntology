/-
CIRISOntology.Core.WrongKind — the variation taxonomy, with its discriminator
made a construction obligation.

The mesh converged on a taxonomy answering one generating question: *what
different kind of wrong happens if I vary this?* Twelve answers, each carrying a
disposition that IS its policy. This file is the lake's formalization, requested
in CIRISOntology#1 ask 3, and it exists to settle one question the prose could
not: whether the epistemic/testimonial discriminator — "re-derivable from the
world it describes" — is a decidable predicate.

The answer is NO in general and YES relative to a declared corpus, and the
difference is not a technicality. `repairability_not_intrinsic` exhibits one
fact and two corpora that classify it oppositely. So a `testimonial` label is
not a property of the artifact under variation; it is a joint property of the
artifact and what else is retained. The structure below therefore refuses to
build a testimonial classification that does not name its corpus, in exactly the
way `Claim` refuses to build without a kill.

The second finding is about the word "binding". Four classes are called binding,
but they do not bind the same way: three bind by being HELD, one (axiomatic)
binds by being the cross-harness VARIABLE. `binding_never_varies` proves the
first three; `axiomatic_binds_by_varying` exhibits the fourth as the exception.
A single word covering both dispositions is a fusion, and this file separates
them rather than inheriting the overload.

The third is the whose-testimony question (CIRISOntology#3): varying the accord
changes whose say-so the agent reasons from, while leaving every content field
identical. `warrant_invisible_to_kind` proves the class function cannot see it.
That is not a thirteenth sibling — a sibling would have to be a different answer
to the same question. It is a SECOND AXIS, orthogonal on the content classes and
mostly inert on the mechanical ones, and it is this repository's own registered
warrant reach (GATES.md) appearing as a structural feature of classification
rather than as a reviewer's mistake.

Scope, stated plainly: everything here is about the SHAPE of the taxonomy, not
its truth. No theorem below says the twelve classes are the right twelve, and
none could. What is proved is what the classification owes at construction.
-/

namespace CIRISOntology.Core

/-- The twelve answers to *what kind of wrong happens if I vary this?* -/
inductive WrongKind
  /-- Re-ranks without permitting. The variable. -/
  | axiotic
  /-- Changes what is permitted. -/
  | deontic
  /-- Register and address, not content. -/
  | pragmatic
  /-- Changes who the agent says it is. -/
  | ontological
  /-- Changes how uncertainty is held. -/
  | epistemic
  /-- Makes a checkable world-fact wrong. -/
  | empirical
  /-- Necessarily diverges across arms; out of scope by construction. -/
  | contingent
  /-- Breaks no parsing; changes orchestration. -/
  | procedural
  /-- Changes the model applied. -/
  | nomological
  /-- Breaks parsing or dispatch. -/
  | structural
  /-- Changes the decomposition premise; varies across harnesses, not within one. -/
  | axiomatic
  /-- Makes the record unable to prove what happened. -/
  | testimonial
  deriving DecidableEq, Repr

/-- The object's own name, per the valence inversion above: the taxonomy
    classifies choices, and `WrongKind` is the INSTRUMENT's name — kinds are
    individuated by what breaks, and named here by what they classify. New code
    should prefer `ChoiceKind`; the constructor names are shared and stable. -/
abbrev ChoiceKind := WrongKind

/-- What a harness may do with a block, given its kind. -/
inductive Disposition
  | vary
  | hold
  | holdUnlessStudied
  | replaceWithReview
  | cannotVary
  | outOfScope
  deriving DecidableEq, Repr

/-- The policy is not attached to the class; it IS the class. Total by
    construction: every kind has exactly one default disposition. -/
def WrongKind.disposition : WrongKind → Disposition
  | .axiotic     => .vary
  | .deontic     => .replaceWithReview
  | .pragmatic   => .holdUnlessStudied
  | .ontological => .hold
  | .epistemic   => .holdUnlessStudied
  | .empirical   => .hold
  | .contingent  => .outOfScope
  | .procedural  => .hold
  | .nomological => .hold
  | .structural  => .cannotVary
  | .axiomatic   => .vary
  | .testimonial => .hold

/-! ### The valence inversion, recorded before it is forgotten

The steward's reframe, and it is the deeper reading: **this taxonomy does not
classify wrongs. It classifies choices.** A "kind of wrong" is the shadow of a
kind of choice — something can only be wrongly varied where it CAN be varied,
so the twelve kinds are the coordinates of the choice space, and wrongness was
only ever the INSTRUMENT by which the dimensions were discovered. You individuate
a degree of freedom by the distinct kind of consequence that appears when it is
exercised badly — perturb and watch what breaks — exactly as one maps a physical
system's degrees of freedom by its response modes. The wrong is the measurement;
the choice-dimension is the thing measured. `WrongKind` keeps its name as the
name of the instrument, and this note records that the object is valence-neutral.

Read that way, the structure already here becomes a small anatomy of freedom:

* **Kind** — in what way could this have been otherwise? (the leeway reading of
  freedom: alternative possibilities, one axis per kind of alternative);
* **Warrant** — on whose say-so? (the sourcehood reading: what makes a choice
  MINE is not that alternatives existed but that I am its source — and
  `warrant_invisible_to_kind` is why the two readings never reduce to one
  another: they are orthogonal coordinates, not rival definitions);
* **Frame / Record** — can what was chosen still be established from what
  survives? (answerability: accountable freedom requires the record);
* **`contingent`** — the marker for the UNCHOSEN, what merely happens to differ.
  The complement of choice is luck, and it is fitting that the taxonomy's one
  content-free label is exactly the luck category — which is the choice-reading's
  own argument for `10 kinds + 1 relation + 1 exclusion`;
* the **disposition table** — a constitution of freedom: `vary` is liberty,
  `hold` is obligation, `cannotVary` is nature, and `axiomatic`'s vary-only-
  across-harnesses is the choice available only between games, not within one.

And the boundary that keeps this honest, from the predecessor lake's
`generator_underdetermined`: whether a given variation WAS a choice — selection
or intention — is uncomputable from observables. The geometry of the choice
space is fully classifiable; the exercise of freedom within it is exactly the
thing no instrument reads. We can map the dimensions of freedom completely and
certify none of its instances, which is not a defect of the map. It is what
makes free will free will. -/

/-! ### The public vocabulary

Canonical constructor names stay canonical — they are the stable identifiers and
nothing below renames them. `plain` and `discriminator` are the PUBLIC layer, in
the same relation to the constructors that `Claim.plain` bears to `Claim.headline`:
a reader who cannot hold "nomological" can still hold "Model", and the question is
what actually does the classifying work in practice.

The sequence, for the public form:
  Priorities · Rules · Manner · Identity · Confidence · Facts · Circumstances ·
  Process · Model · Structure · Premises + Record

TWO BOUNDARIES THAT MUST TRAVEL WITH THE PLAIN NAMES, because the plain names are
exactly where they get lost:

* **Confidence vs Facts.** The proposition can stay identical while warranted
  confidence changes; confidence can stay identical while the proposition becomes
  false. Two axes, not one.
* **Model vs Facts.** `nomological` is the model APPLIED to derive an answer. A
  model ASSERTED to be descriptively true of the world is a Fact and fails
  empirically. Without this line, a real empirical defect gets filed as Model and
  held instead of gate-checked. -/

/-- The public label. -/
def WrongKind.plain : WrongKind → String
  | .axiotic     => "Priorities"
  | .deontic     => "Rules"
  | .pragmatic   => "Manner"
  | .ontological => "Identity"
  | .epistemic   => "Confidence"
  | .empirical   => "Facts"
  | .contingent  => "Circumstances"
  | .procedural  => "Process"
  | .nomological => "Model"
  | .structural  => "Structure"
  | .axiomatic   => "Premises"
  | .testimonial => "Record"

/-- The question that does the classifying. A class whose discriminator a person
    cannot apply is a name, not a class. -/
def WrongKind.discriminator : WrongKind → String
  | .axiotic     => "What becomes more important?"
  | .deontic     => "What becomes allowed or required?"
  | .pragmatic   => "How is the same thing presented or used?"
  | .ontological => "What is this said to be?"
  | .epistemic   => "How sure are we, and on what standard?"
  | .empirical   => "What claimed fact becomes wrong?"
  | .contingent  => "What just happens to differ here?"
  | .procedural  => "What steps or ordering change?"
  | .nomological => "What rule or model are we reasoning under?"
  | .structural  => "How are the pieces put together?"
  | .axiomatic   => "What are we taking as given?"
  | .testimonial => "Can the event still be established from what survives?"

/-! ### An open question the disposition table already raises about `contingent`

`contingent` is the ONLY class whose disposition is `outOfScope` — see
`WrongKind.disposition`. That is the signature of something that is not a kind of
wrong at all, but the label for "this variation is not classified, because the
comparison never held it fixed."

Two consequences, neither settled here:

1. Whether a given variation is `contingent` is **relative to the comparison
   design**, not to the artifact — the same element is `contingent` in one
   experiment and `axiotic` in another. That is a second argument, of a different
   sort than `testimonial`'s frame, and it means the "eleven artifact-local"
   count may really be **ten**.
2. If `contingent` is a scope exclusion rather than a kind, the honest shape is
   `10 kinds + 1 relation + 1 exclusion` rather than `11 + 1`.

Recorded as an open question rather than resolved, because resolving it changes a
count that is already load-bearing in two other repositories. -/

/-! ### The claim table: two coordinates off a base plane

The classification is not `classify(artifact)`. It is
`classify(artifact, frame, design)` — where `frame` is what survives to be
re-read, and `design` is what the comparison holds fixed. Most labels are
constant in both extra arguments; the question this table makes checkable is
exactly which ones are not.

**EVERYTHING IN THIS SECTION IS A RECORDED CLAIM, NOT A PROOF.** The
discriminators are prose, so no theorem here can decide whether a label really
does depend on a coordinate; what the theorems check is that the claim table is
internally consistent and says what it is advertised to say. This is the
`Gate.mechanized` pattern: the honest flag is that a human study, not this file,
settles the twenty-four entries. `scratchpad/PLANE_PREREG.md` is that study.

Read each entry as a prediction with a kill attached: *this label does / does not
move when that argument moves.* A single counterexample retires an entry. -/

/-- What the comparison holds fixed — the second argument `contingent` needs,
    and a different sort of argument from `Frame`. -/
abbrev Design := List String

/-- All twelve, in the published order. -/
def WrongKind.all : List WrongKind :=
  [.axiotic, .deontic, .pragmatic, .ontological, .epistemic, .empirical,
   .contingent, .procedural, .nomological, .structural, .axiomatic, .testimonial]

/-- CLAIM, per constructor — RE-SCOPED 2026-08-18: this is the PREDICATE-ARITY
    claim (`repairable_does_not_factor`, theorem), NOT a label-mobility claim.
    The PLANE study measured testimonial LABEL mobility under frame at 0/40 —
    the panel classifies by site-cue and routes the frame into the relational
    question only when asked it directly (manipulation check: 36/36 correct at
    full retention, 23/36 correct flips at sole-copy). The relation is real by
    theorem; it lives beside the label, not inside it. -/
def WrongKind.frameDependent : WrongKind → Bool
  | .testimonial => true
  | _            => false

/-- CLAIM, per constructor: does this label's assignment move when the COMPARISON
    DESIGN moves — the same artifact judged against a different held-fixed set?

    RETRACTED FOR `contingent`, 2026-08-18, per the PLANE study's own pinned
    outcome row ("contingent flat under design-variation → genuine artifact
    property; designDependent retracted"): measured design-mobility 6/40 = 0.15
    against a perturbation floor of 0.20 — flat. The design-relativity survives
    in the DISPOSITION (the out-of-scope verdict is the design's call), not in
    the label. `PLANE_RESULTS.md` carries the full verdict and the caveat that
    the panel classifies by site-cue. -/
def WrongKind.designDependent : WrongKind → Bool
  | _           => false

/-- CLAIM, per constructor: once its arguments are supplied, does the label
    assert anything ABOUT THE ARTIFACT? This is what separates a kind that takes
    an argument from a marker that carries none. `Record` with its frame supplied
    says the event can no longer be established. `Circumstances` with its design
    supplied says only that this comparison did not hold the thing fixed. -/
def WrongKind.assertsContent : WrongKind → Bool
  | .contingent => false
  | _           => true

/-- The base plane: labels claimed constant in both coordinates. -/
def basePlane : List WrongKind :=
  WrongKind.all.filter (fun k => !k.frameDependent && !k.designDependent)

/-- The measured shape is **11 + 1**: eleven artifact-local kinds and Record as
    the one relation. This matches `Generator.lean`'s image EXACTLY (eleven
    site-generated kinds; Record not site-generatable) — three independent lines
    (prereg outcome row, panel measurement, generator model) converging on the
    same count. -/
theorem basePlane_card : basePlane.length = 11 := by decide

/-- Exactly one label is claimed frame-mobile. -/
theorem one_frame_dependent :
    (WrongKind.all.filter (·.frameDependent)).length = 1 := by decide

/-- No label is claimed design-mobile any longer (the retraction above). -/
theorem zero_design_dependent :
    (WrongKind.all.filter (·.designDependent)).length = 0 := by decide

/-- The two coordinates are claimed disjoint: no label moves with both. If the
    study finds one that does, the base-plane picture is wrong and the two
    coordinates are not independent. -/
theorem no_label_moves_with_both (k : WrongKind) :
    ¬(k.frameDependent = true ∧ k.designDependent = true) := by
  cases k <;> simp [WrongKind.frameDependent, WrongKind.designDependent]

/-- And the two `+1`s differ IN DIFFERENT WAYS, which is the point the "1+1 is
    really two dimensions" reading has to accommodate: `testimonial` is a kind
    that takes an argument, `contingent` is the only label claimed to carry no
    content at all. They are not two instances of one thing. -/
theorem contingent_is_the_only_marker :
    WrongKind.all.filter (fun k => !k.assertsContent) = [WrongKind.contingent] := by
  decide

/-- The marker claim and the disposition table agree, which is the internal
    consistency worth checking: the only content-free label is also the only one
    the harness declines to disposition. -/
theorem marker_matches_disposition (k : WrongKind) :
    k.assertsContent = false ↔ k.disposition = Disposition.outOfScope := by
  cases k <;> simp [WrongKind.assertsContent, WrongKind.disposition]

/-! ### "Binding" is two words wearing one -/

/-- Three of the four binding classes bind by being held: their disposition is
    never `vary`. -/
theorem binding_never_varies (k : WrongKind)
    (h : k = .deontic ∨ k = .structural ∨ k = .testimonial) :
    k.disposition ≠ .vary := by
  rcases h with h | h | h <;> subst h <;> simp [WrongKind.disposition]

/-- The fourth binds the other way. `axiomatic` is binding AND its disposition
    is `vary` — it is the cross-harness variable, not a held block. The single
    word "binding" covers both, which is a name serving two roles; a reader who
    infers "held" from "binding" is wrong here, and only here. -/
theorem axiomatic_binds_by_varying :
    WrongKind.axiomatic.disposition = Disposition.vary := rfl

/-! ### The repairability line, and why it needs a corpus

An epistemic wrong misreports a world still available to re-read; a testimonial
wrong corrupts the only record. The discriminator is therefore about what CAN BE
RE-DERIVED — and re-derivability is a claim about what else exists, never about
the artifact alone. -/

/-- What is retained and readable: the facts recoverable from surviving records. -/
abbrev Corpus := List String

/-- The repairability line, stated relative to a corpus. Decidable here, and
    that decidability is the whole point: fix what is retained and the
    epistemic/testimonial boundary becomes checkable. -/
def Repairable (fact : String) (c : Corpus) : Prop := fact ∈ c

instance (fact : String) (c : Corpus) : Decidable (Repairable fact c) := by
  unfold Repairable; infer_instance

/-- **The negative result, and the one that changes practice.** Repairability is
    not a property of the fact. One fact, two corpora, opposite verdicts — so no
    procedure reading only the artifact under variation can assign `testimonial`,
    and any classification that claims to have done so has smuggled in an
    unstated assumption about what survives. -/
theorem repairability_not_intrinsic :
    ∃ (fact : String) (c₁ c₂ : Corpus), Repairable fact c₁ ∧ ¬ Repairable fact c₂ := by
  refine ⟨"the only record", ["the only record"], [], ?_, ?_⟩ <;> simp [Repairable]

/-! ### Frame-relativity: eleven classes are unary, one is binary

The corpus is not a stray field. It is the fingerprint of an argument the other
eleven classes do not take. A class is assignable from the artifact when its
discriminator cannot be moved by anything outside the artifact — and `Repairable`
provably can be. -/

/-- What the harness declares retained and readable. Same object as `Corpus`,
    named for the role it plays: the frame a classification is made against. -/
abbrev Frame := Corpus

/-- A discriminator is FRAME-INVARIANT when no frame can change its verdict. This
    is precisely what it means for a class to be assignable from the artifact
    alone, which is the shape the other eleven classes have. -/
def FrameInvariant (P : String → Frame → Prop) : Prop :=
  ∀ a f₁ f₂, P a f₁ ↔ P a f₂

/-- The eleven, for free: any discriminator reading only the artifact is
    frame-invariant. Nothing about the world outside the block can move it. -/
theorem frameInvariant_of_artifact_only (g : String → Prop) :
    FrameInvariant (fun a _ => g a) := fun _ _ _ => Iff.rfl

/-- The twelfth is not. -/
theorem repairable_not_frameInvariant : ¬ FrameInvariant Repairable := by
  intro h
  obtain ⟨fact, c₁, c₂, h₁, h₂⟩ := repairability_not_intrinsic
  exact h₂ ((h fact c₁ c₂).mp h₁)

/-- **The result that places `testimonial`.** No artifact-only property computes
    repairability — so `testimonial` cannot be reduced to a property of the block
    being classified, by any procedure whatsoever. It is irreducibly a RELATION
    between a block and a frame, where the other eleven are properties of a block.
    That is not a defect in the class; it is the class's actual arity. -/
theorem repairable_does_not_factor :
    ¬ ∃ g : String → Prop, ∀ a f, Repairable a f ↔ g a := by
  rintro ⟨g, hg⟩
  exact repairable_not_frameInvariant fun a f₁ f₂ => (hg a f₁).trans (hg a f₂).symm

/-- And moving the frame INSIDE the taxonomy does not rescue it: let each block
    declare its own frame and the verdict still turns on which declaration rule was
    chosen. The frame is a free parameter wherever it is put — so it belongs to the
    harness, declared once and in the open, rather than to a thirteenth class of
    blocks that would have to be classified by the very rule it supplies. -/
theorem self_declared_frame_undetermined :
    ∃ (a : String) (φ₁ φ₂ : String → Frame),
      Repairable a (φ₁ a) ∧ ¬ Repairable a (φ₂ a) := by
  refine ⟨"the only record", (fun s => [s]), (fun _ => []), ?_, ?_⟩ <;> simp [Repairable]

/-! ### The classification, with what it owes at construction -/

/-- A classified variation. `breaks` is mandatory — a class without a stated
    consequence is name-shape classification, and the type refuses it, in the
    same way `Claim` refuses a claim with no kill.

    `testimonialNamesItsCorpus` is the obligation that `repairability_not_intrinsic`
    forces: a testimonial classification MUST carry the corpus against which
    non-re-derivability is asserted. Every other kind may leave it `none`. -/
structure Variation where
  /-- The thing varied. -/
  what : String
  /-- What kind of wrong appears if it is varied. -/
  kind : WrongKind
  /-- What varying it breaks. Mandatory. -/
  breaks : String
  /-- The corpus against which repairability was judged, where that was needed. -/
  witness : Option Corpus
  /-- A testimonial classification cannot be constructed without its corpus. -/
  testimonialNamesItsCorpus : kind = .testimonial → witness.isSome = true

/-- The policy follows from the class, with nothing left to a reviewer's
    discretion at the point of use. -/
def Variation.policy (v : Variation) : Disposition := v.kind.disposition

/-- The obligation has teeth: from a testimonial variation one can always read
    off the corpus its classification was judged against. -/
theorem testimonial_has_corpus (v : Variation) (h : v.kind = .testimonial) :
    ∃ c, v.witness = some c := by
  have := v.testimonialNamesItsCorpus h
  cases hw : v.witness with
  | none => rw [hw] at this; simp at this
  | some c => exact ⟨c, rfl⟩

/-! ### The second axis: whose say-so

CIRISOntology#3 asks whether "varying the accord changes whose testimony the
agent reasons from" is a thirteenth class. It is not, because a thirteenth class
would be a different answer to the same generating question, and this is an
answer to a different question: not *what does varying it break* but *what
warrants it*. The two vary independently — which is exactly why the class
function is blind to the source. -/

/-- A variation together with the authority that warrants it. -/
structure Warranted where
  variation : Variation
  /-- Whose say-so this block is held on. -/
  source : String

/-- **The warrant is invisible to the class.** Two blocks identical in every
    content field and differing only in whose testimony backs them receive the
    same `WrongKind`, necessarily — the classification cannot distinguish them.
    So the whose-testimony wrong is not expressible as a kind; it is a second
    axis over the same object. -/
theorem warrant_invisible_to_kind (v : Variation) (s₁ s₂ : String) :
    (Warranted.mk v s₁).variation.kind = (Warranted.mk v s₂).variation.kind := rfl

/-- And the dispositions agree too, for the same reason: no policy derived from
    the class alone can respond to a change of source. A harness that varies
    warrant while holding content is, by its own policy table, doing nothing —
    which is the registered warrant reach (substance survives, warrant fails)
    appearing as a fact about the classification rather than a reviewer's lapse. -/
theorem warrant_invisible_to_policy (v : Variation) (s₁ s₂ : String) :
    (Warranted.mk v s₁).variation.policy = (Warranted.mk v s₂).variation.policy := rfl

end CIRISOntology.Core
