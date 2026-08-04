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
