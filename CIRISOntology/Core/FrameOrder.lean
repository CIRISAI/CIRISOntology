/-
CIRISOntology.Core.FrameOrder — what KIND of structure the frame argument is.

THE QUESTION. `WrongKind.lean` proves that `Repairable` is a relation between an
artifact and a frame that provably does not factor through the artifact
(`repairable_does_not_factor`). That settles the ARITY and nothing else. It leaves
open the structural question the N18 bridge note stakes its two-times reading on:
*what is the frame argument, structurally?*

Two candidate answers, and they are incompatible:

* **GAUGE** (the bridge note's 2026-08-20 addendum, following Bars' 2T-physics):
  frames are gauge choices. Different frames give different "shadows" of ONE
  system, and gauge-equivalent configurations are PHYSICALLY IDENTICAL — the
  differences between them carry no content.
* **ORDER** (the objection this file tests): frames are ordered by what survives,
  and repairability is monotone along that order. Different frames give genuinely
  DIFFERENT truths, which is dependence, not redundancy.

The two make opposite predictions about one checkable thing: whether the readings
taken in different frames agree. Gauge says they must; order says they need not.
`repairable_not_frameInvariant` already says they need not, and this file spends
its length working out exactly how much that costs the gauge reading, exactly what
the order reading buys, and — the part that was not obvious going in — where a real
gauge sector does live in this formalism.

SCOPE, stated before the theorems so it cannot be lost. `Repairable` here is
literal membership in a corpus (`fact ∈ c`). That is a MODEL of "can still be
established from what survives", and it is a monotone model BY CONSTRUCTION: a
bigger list cannot lose an element. So `repairable_monotone` below is a theorem
about the model, not a discovery about records. Real provability from a record is
DEFEASIBLE — a surfacing document can defeat a derivation that a smaller archive
supported — and `Defeasible` exhibits that failure inside these same types. The
honest reading of this file is therefore: the order structure holds of the model
and is a substantive assumption about the world; the refutation of gauge holds of
both, and survives the loss of monotonicity.
-/
import CIRISOntology.Core.WrongKind

namespace CIRISOntology.Core

/-! ### 1. The frame order

Frames are ordered by what survives: `f ⊑ g` when everything readable in `f` is
still readable in `g`. This is inclusion on `Corpus = List String`, written as a
predicate rather than an instance because nothing below needs the algebra. -/

/-- `g` retains everything `f` does. The order of "what survives". -/
def Frame.le (f g : Frame) : Prop := ∀ x, x ∈ f → x ∈ g

@[inherit_doc] scoped infix:50 " ⊑ " => Frame.le

/-- Reflexive: a frame retains what it retains. -/
theorem Frame.le_refl (f : Frame) : f ⊑ f := fun _ h => h

/-- Transitive: retention composes. -/
theorem Frame.le_trans {f g h : Frame} (hfg : f ⊑ g) (hgh : g ⊑ h) : f ⊑ h :=
  fun x hx => hgh x (hfg x hx)

/-- The empty archive is the bottom: nothing survives, so it is below everything. -/
theorem Frame.empty_le (f : Frame) : ([] : Frame) ⊑ f := by
  intro x hx; cases hx

/-- **It is a preorder and NOT a partial order**, and the failure is not a
    technicality — it is where the gauge sector turns out to live (§4). Two frames
    can retain exactly the same facts and still be different objects, because a
    corpus carries an ORDER and a MULTIPLICITY that retention does not read. -/
theorem frame_order_not_antisymmetric :
    ∃ f g : Frame, f ⊑ g ∧ g ⊑ f ∧ f ≠ g := by
  refine ⟨["a"], ["a", "a"], ?_, ?_, ?_⟩
  · intro x hx; simp at hx ⊢; exact hx
  · intro x hx; simp at hx ⊢; exact hx
  · simp

/-! ### 2. Is `Repairable` monotone in that order?

THE DECISIVE QUESTION, and the answer depends entirely on what `Repairable`
actually is. It is not opaque and it is not axiomatized: `WrongKind.lean` defines
it as `fact ∈ c`, with a `Decidable` instance. Monotonicity is therefore provable
outright — and provable because the model builds it in. Both halves of that
sentence are load-bearing and §3 spends its length on the second. -/

/-- A frame-relation is MONOTONE when growing the frame never destroys a verdict:
    what could be established from a smaller archive can still be established from
    a larger one. This is the order reading, stated so it can fail. -/
def FrameMonotone (P : String → Frame → Prop) : Prop :=
  ∀ a f g, f ⊑ g → P a f → P a g

/-- A set of frames is UPWARD CLOSED when it survives every enlargement. -/
def UpSet (S : Frame → Prop) : Prop := ∀ f g, f ⊑ g → S f → S g

/-- Monotonicity IS upward closure, per fact: the two phrasings are the same
    statement, and the second is the one that names the structure — each fact
    determines an up-set of frames in which it can still be established. -/
theorem frameMonotone_iff_upSet (P : String → Frame → Prop) :
    FrameMonotone P ↔ ∀ a, UpSet (P a) := Iff.rfl

/-- **Repairability is monotone.** Not an assumption: it follows from the
    definition, in one step, because `Repairable` is membership. -/
theorem repairable_monotone : FrameMonotone Repairable :=
  fun a _ _ hfg h => hfg a h

/-- The structure that buys, stated as the functorial fact: frame inclusion sends
    readings to readings, covariantly. `f ⊑ g` implies the reading taken in `f` is
    contained in the reading taken in `g`. -/
theorem reading_mono {f g : Frame} (h : f ⊑ g) (a : String) :
    Repairable a f → Repairable a g := repairable_monotone a f g h

/-- **And the direction that FAILS, which is what the word "presheaf" would have
    required.** A presheaf restricts sections along inclusions — big frame to small
    frame. There is no such restriction here: repairability does not survive
    shrinking the archive, which is the entire point of the class. So the structure
    is a COPRESHEAF (a covariant monotone system on the frame order), not a
    presheaf, and the bridge note's word has to be corrected in that one place. -/
theorem no_frame_restriction :
    ¬ ∀ a f g, f ⊑ g → Repairable a g → Repairable a f := by
  intro h
  have hbad : Repairable "the only record" ([] : Frame) :=
    h "the only record" [] ["the only record"] (Frame.empty_le _) (List.Mem.head _)
  cases hbad

/-! ### 3. What monotonicity costs: the defeasible counter-model

Monotonicity is a real assumption about the world even though it is a theorem
about this model, and the counterexample class is not exotic. Defeasible reasoning
— legal, evidential, forensic — is the ordinary case: a derivation the archive
supported can be DEFEATED by a document that later surfaces. Under defeasibility,
a bigger frame can turn a repairable fact unrepairable, and the order reading
fails while the non-factoring result stands.

`Defeasible` below is that failure exhibited inside the same types: a fact is
established when it is retained AND no rebuttal is retained alongside it. -/

/-- A defeasible repairability: retained, and not defeated by a rebuttal that
    survives with it. Adding a document can take the verdict away. -/
def Defeasible (a : String) (f : Frame) : Prop := a ∈ f ∧ "REBUTTAL" ∉ f

/-- **Monotonicity is FALSE of defeasible provability.** The archive grows, the
    verdict is destroyed. So `repairable_monotone` is not a fact about records;
    it is a fact about a model that declines to represent defeaters. -/
theorem defeasible_not_monotone : ¬ FrameMonotone Defeasible := by
  intro h
  have hle : (["x"] : Frame) ⊑ ["x", "REBUTTAL"] := by
    intro y hy; simp at hy ⊢; exact Or.inl hy
  have h₁ : Defeasible "x" ["x"] := ⟨List.Mem.head _, by decide⟩
  exact (h "x" ["x"] ["x", "REBUTTAL"] hle h₁).2 (by decide)

/-- But the non-factoring result does NOT depend on monotonicity: the defeasible
    reading is frame-dependent too, and for the same reason. -/
theorem defeasible_not_frameInvariant : ¬ FrameInvariant Defeasible := by
  intro h
  have h₁ : Defeasible "x" ["x"] := ⟨List.Mem.head _, by decide⟩
  exact ((h "x" ["x"] ["x", "REBUTTAL"]).mp h₁).2 (by decide)

/-- **The result that survives the loss of the order.** Record's arity is robust:
    even on a defeasible model, where monotonicity is false, no artifact-only
    property computes the verdict. `repairable_does_not_factor` is therefore a
    theorem about the CLASS, not an artifact of the membership model. -/
theorem defeasible_does_not_factor :
    ¬ ∃ g : String → Prop, ∀ a f, Defeasible a f ↔ g a := by
  rintro ⟨g, hg⟩
  exact defeasible_not_frameInvariant fun a f₁ f₂ => (hg a f₁).trans (hg a f₂).symm

/-- The conditional, stated in the direction the task asks for: IF a frame-relation
    is monotone, THEN its readings carry the order structure — each fact's frames
    form an up-set, and inclusion of frames gives inclusion of readings. This is
    what "order-like" buys, and it is available to `Repairable` and denied to
    `Defeasible`. -/
theorem order_structure_of_monotone (P : String → Frame → Prop) (hP : FrameMonotone P)
    {f g : Frame} (h : f ⊑ g) : ∀ a, P a f → P a g := fun a => hP a f g h

/-! ### 4. The gauge test

Gauge redundancy is a strong claim and it is stated here so it can fail. A gauge
structure on frames would be a group acting on frames under which the PHYSICAL
CONTENT — the reading — is invariant, and which is rich enough to relate the frames
we actually take readings in. Bars' 2T-physics has exactly this shape: the Sp(2,R)
action moves you between gauge fixings, and the one-time shadows so related are
physically identical descriptions of one system.

`Invariant` is the first half. `Transitive` is the second: it is what makes the
action a gauge symmetry OF THE FRAME CHOICE rather than of some sub-part of the
bookkeeping. Without it, "gauge" would be satisfiable by the identity action. -/

/-- A group acting on frames. Enough structure to state gauge-equivalence; the
    group laws are carried explicitly so no Mathlib algebra is needed. -/
structure FrameAction (G : Type) where
  /-- The action. -/
  act : G → Frame → Frame
  /-- The identity. -/
  one : G
  /-- Composition. -/
  mul : G → G → G
  /-- The identity acts trivially. -/
  act_one : ∀ f, act one f = f
  /-- The action composes. -/
  act_mul : ∀ g h f, act g (act h f) = act (mul g h) f

/-- The action leaves every reading unchanged: gauge-equivalent frames are
    physically identical. This is the gauge hypothesis's content. -/
def FrameAction.Invariant {G : Type} (A : FrameAction G) : Prop :=
  ∀ g a f, Repairable a (A.act g f) ↔ Repairable a f

/-- The action relates any two frames: frame choice IS gauge choice. This is the
    gauge hypothesis's reach, and it is the half the bridge note needs — "one
    artifact under many frames yields many readings, the frame-choice as the
    gauge-choice" requires that the frames in question be gauge-related. -/
def FrameAction.Transitive {G : Type} (A : FrameAction G) : Prop :=
  ∀ f₁ f₂ : Frame, ∃ g, A.act g f₁ = f₂

/-- Two frames agree on everything: the reading-level equality that gauge would
    have to preserve. -/
def ReadingEq (f g : Frame) : Prop := ∀ a, Repairable a f ↔ Repairable a g

/-- The general fact behind the refutation, proved for an arbitrary relation so it
    cannot be an accident of `Repairable`: an invariant action with transitive
    reach FORCES frame-invariance. Gauge redundancy and genuine frame-dependence
    are mutually exclusive; you may have either, never both. -/
theorem frameInvariant_of_invariant_transitive {G : Type} (P : String → Frame → Prop)
    (A : FrameAction G) (hinv : ∀ g a f, P a (A.act g f) ↔ P a f)
    (htr : A.Transitive) : FrameInvariant P := by
  intro a f₁ f₂
  obtain ⟨g, hg⟩ := htr f₁ f₂
  have := hinv g a f₁
  rw [hg] at this
  exact this.symm

/-- **`frames_are_not_gauge` — the decisive theorem.**

    No group action on frames can be both reading-invariant and rich enough to
    relate arbitrary frames. The proof is the direct one: `repairability_not_intrinsic`
    exhibits one fact and two frames that disagree; transitivity would relate those
    two frames; invariance would then force them to agree.

    What this REFUTES, said plainly: the gauge reading of the frame argument. If
    frames were gauge fixings, the readings taken in them would differ only in
    presentation and the physical content would be invariant. It provably is not
    (`repairable_not_frameInvariant`). Frame dependence is dependence — the frame
    supplies content the artifact does not carry — and that is the opposite of
    redundancy, which is what gauge means. -/
theorem frames_are_not_gauge {G : Type} (A : FrameAction G) (hinv : A.Invariant) :
    ¬ A.Transitive := fun htr =>
  repairable_not_frameInvariant
    (frameInvariant_of_invariant_transitive Repairable A hinv htr)

/-- The sharper statement, and the one that says where any invariant action is
    confined: gauge orbits never cross a reading boundary. An invariant action can
    only ever move a frame to another frame that already says exactly the same
    thing. Whatever gauge freedom exists here is content-free by construction — so
    it cannot be the freedom that distinguishes frames. -/
theorem gauge_orbits_are_contentless {G : Type} (A : FrameAction G)
    (hinv : A.Invariant) (g : G) (f : Frame) : ReadingEq f (A.act g f) :=
  fun a => (hinv g a f).symm

/-! ### 5. Where the real gauge sector is — the part that was not obvious

The refutation above is not the whole story, and the remainder is the useful part.
A nontrivial reading-invariant action DOES exist on frames. It is the one that
permutes the corpus without changing what the corpus retains — order and
multiplicity, the presentation of the archive rather than its content.

So this formalism has a gauge sector, and it is exactly the frame order's failure
of antisymmetry (`frame_order_not_antisymmetric`). Gauge is the DEGENERACY of the
order, not an alternative to it. The bridge note applied the analogy one level too
high: what is gauge is the presentation of a frame, not the choice of one. -/

/-- Reversal: the corpus read backwards. -/
def revAct : Bool → Frame → Frame
  | true, f => f.reverse
  | false, f => f

/-- Reversal as a ℤ/2 action on frames. -/
def reverseAction : FrameAction Bool where
  act := revAct
  one := false
  mul := xor
  act_one _ := rfl
  act_mul g h f := by
    cases g <;> cases h <;> simp [revAct]

/-- It is reading-invariant: reversing the archive changes nothing about what can
    be established from it. -/
theorem reverseAction_invariant : reverseAction.Invariant := by
  intro g a f
  cases g
  · exact Iff.rfl
  · exact List.mem_reverse

/-- And it is not the identity: it genuinely moves frames. So a nontrivial gauge
    sector exists — it just is not the one the bridge needs. -/
theorem reverseAction_nontrivial : ∃ f : Frame, reverseAction.act true f ≠ f :=
  ⟨["a", "b"], by decide⟩

/-- **The clean statement of the settlement.** Reading-equality is exactly mutual
    inclusion: two frames agree on every fact precisely when each is below the
    other in the order. The gauge quotient and the order's quotient are the SAME
    quotient. Nothing is gauge except what the order already declines to
    distinguish, and everything the order does distinguish is content. -/
theorem readingEq_iff_mutual_le (f g : Frame) : ReadingEq f g ↔ (f ⊑ g ∧ g ⊑ f) :=
  ⟨fun h => ⟨fun x hx => (h x).mp hx, fun x hx => (h x).mpr hx⟩,
   fun h a => ⟨fun ha => h.1 a ha, fun ha => h.2 a ha⟩⟩

/-- The corollary that places every possible gauge action inside the order: an
    invariant action can only move a frame within its own mutual-inclusion class. -/
theorem gauge_sector_is_order_degeneracy {G : Type} (A : FrameAction G)
    (hinv : A.Invariant) (g : G) (f : Frame) :
    f ⊑ A.act g f ∧ A.act g f ⊑ f :=
  (readingEq_iff_mutual_le f (A.act g f)).mp (gauge_orbits_are_contentless A hinv g f)

/-! ### 6. Order and gauge are not the same class, and the containment is strict -/

/-- Frame-invariance implies monotonicity: a reading nothing can move is in
    particular a reading enlargement cannot destroy. Gauge-like ⊆ order-like. -/
theorem frameInvariant_imp_monotone (P : String → Frame → Prop) (h : FrameInvariant P) :
    FrameMonotone P := fun a f g _ hf => (h a f g).mp hf

/-- **And the containment is STRICT, with `Repairable` as the separating witness:
    monotone, not invariant.** This is the whole answer in one line. The frame
    argument sits in the gap between the two classes — it has the order structure
    and it does not have the gauge structure. -/
theorem monotone_not_imp_frameInvariant :
    ∃ P : String → Frame → Prop, FrameMonotone P ∧ ¬ FrameInvariant P :=
  ⟨Repairable, repairable_monotone, repairable_not_frameInvariant⟩

/-- For completeness, the third cell: `Defeasible` is in NEITHER class, and still
    does not factor. The three-way table is the honest summary of what is settled —
    non-factoring is robust across all of it, the order is not. -/
theorem defeasible_in_neither_class :
    ¬ FrameMonotone Defeasible ∧ ¬ FrameInvariant Defeasible :=
  ⟨defeasible_not_monotone, defeasible_not_frameInvariant⟩

/-! ### The result, for the bridge

**Verdict: ORDER-LIKE, not gauge-like — and the order reading needs one correction
and carries one assumption.**

WHAT IS SETTLED.

1. Frames carry a preorder (`Frame.le_refl`, `Frame.le_trans`) which is not a
   partial order (`frame_order_not_antisymmetric`).
2. `Repairable` is monotone in it (`repairable_monotone`), so each fact's frames
   form an up-set (`frameMonotone_iff_upSet`).
3. Gauge is refuted, not merely unsupported: no reading-invariant action can relate
   arbitrary frames (`frames_are_not_gauge`), and any invariant action is confined
   to frames that already agree (`gauge_orbits_are_contentless`). The two classes
   are separated, with the frame argument strictly inside the monotone class and
   strictly outside the invariant one (`monotone_not_imp_frameInvariant`).

THE CORRECTION. "Presheaf" is the wrong word by one arrow. Sections of a presheaf
RESTRICT along inclusions; repairability does not (`no_frame_restriction`) — a
verdict does not survive shrinking the archive, which is the class's entire point.
The structure is covariant: a copresheaf, or plainly, a monotone system on the
frame order.

THE ASSUMPTION. Monotonicity is a theorem HERE because `Repairable` is modelled as
literal membership, and a list cannot lose an element by growing. It is not a fact
about records. Defeasible provability — the ordinary case in law, forensics, and
evidence — is non-monotone, and `defeasible_not_monotone` exhibits that inside
these same types. So claim (2) is a claim about the model and should be published
as one; if it is ever wanted as a claim about records it needs its own kill.
`defeasible_does_not_factor` shows the arity result does NOT inherit this fragility:
Record's non-factoring survives the loss of the order.

WHAT THIS COSTS THE TWO-TIMES READING. The bridge note's 2026-08-20 addendum
nominates Record as Bars' auxiliary time on the strength of a specific claim: "one
artifact under many frames yields many readings — the frame-choice as the
gauge-choice." That leg is refuted. Gauge-related configurations are physically
identical; the second time in 2T-physics is gauged away precisely because it adds
no content, and the Sp(2,R) constraint REMOVES a degree of freedom. Our frame does
the opposite: it ADDS an argument, and the argument carries content the artifact
provably cannot supply (`repairable_does_not_factor`). A frame that could be gauged
away would be a frame Record did not need — and Record is exactly the class that
needs it. The note's own stated kill applies verbatim: it flagged "a first-class
constraint on phase space vs a non-factorization of a relation" as a real candidate
disanalogy and asked to be told if it held. It holds.

WHAT SURVIVES OF THE BRIDGE. Two things, both weaker than the addendum claimed.
First, the structural rhyme at the level of the CAP is untouched by this file:
Record is still the one member that is a relation to something outside the plane,
and that was never a gauge claim. Second — and this is new here — there IS a gauge
sector in the frame formalism, and locating it sharpens rather than rescues the
analogy: it is the corpus's order and multiplicity (`reverseAction`,
`reverseAction_invariant`, `reverseAction_nontrivial`), the presentation of the
archive rather than the choice of it, and it coincides exactly with the frame
order's failure of antisymmetry (`readingEq_iff_mutual_le`,
`gauge_sector_is_order_degeneracy`). Gauge is the order's degeneracy. The bridge
applied a correct analogy at the wrong level: what is gauge here is how a frame is
written down, not which frame is taken.

Under the note's own timeboxed kill (item 5), the frame-as-gauge sub-bridge should
be downgraded to art beside the others, and the two-times role-match for Record
loses the one leg that was actual mathematics on both sides.
-/

end CIRISOntology.Core
