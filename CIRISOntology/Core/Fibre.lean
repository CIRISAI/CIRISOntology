/-
CIRISOntology.Core.Fibre — the BASE of the fibre object.

ONE object: the fibres of a view, `SameFibre v x y ≔ v x = v y`. This file is
the bottom of the import graph for everything that reads it (Coordination,
FrameAxis, Factoring, NonFactoring, Closure, Habit, …), so every Core file can
state its shape through it. It holds:

  * the founding predicates, moved here verbatim from their old homes so there
    is ONE copy: `SeparatesFiber` + `not_computable_from` (from Coordination),
    `NonFactoring` + its two general consequences (from NonFactoring), and
    `Factoring.Factors` + `factors_refl` / `factors_trans` + the central lemma
    `factors_iff_not_separatesFiber` (from Factoring) — names and statements
    unchanged;
  * `SameFibre` and the DETERMINES / BLIND bridges;
  * THE ONE CHOICE CONSTRUCTION (`View.factors_iff_respects`): building a
    factoring map out of fibre-respect. The closure form
    (`View.factors_comp_iff_preserves`, no `Nonempty` needed) is derived from
    it; Closure, Habit and Factoring no longer carry their own copies.

These are definitional unifications — one witness, not several; no new
evidence about the world. The readings that need higher files (closed, probe,
entropy, record) are stated in `Core/View.lean`.
-/
import Mathlib.Tactic.PushNeg
import Mathlib.Data.Setoid.Basic
import Mathlib.Logic.IsEmpty

namespace CIRISOntology.Core

/-- A datum SEPARATES a fiber of a summary map when two states share the summary
    yet differ in the datum. This is exactly the condition under which the
    summary has thrown the datum away. -/
def SeparatesFiber {State Summary Datum : Type*}
    (summary : State → Summary) (d : State → Datum) : Prop :=
  ∃ a b : State, summary a = summary b ∧ d a ≠ d b

/-- THE DOMAIN ARGUMENT. A datum that separates a fiber of a lossy summary is
    not computable from that summary: there is no `g` with `d = g ∘ summary`.

    Instantiated twice in this repository — for the higher-order remainder of
    coordination (this file) and for every upstream construction datum
    (`Core.Provenance`). Both are the same two-line fact about function domains,
    and neither is a claim about physics. -/
theorem not_computable_from {State Summary Datum : Type*}
    (summary : State → Summary) (d : State → Datum)
    (h : SeparatesFiber summary d) :
    ¬ ∃ g : Summary → Datum, ∀ x, d x = g (summary x) := by
  rintro ⟨g, hg⟩
  obtain ⟨a, b, hs, hd⟩ := h
  exact hd (by rw [hg a, hg b, hs])

/-- **THE SHAPE, in witness-pair form.** A quantity `q` FAILS TO FACTOR through a
    family of partial views `view` when two wholes agree under every one of those
    views and still differ in `q`.

    The views are typed per index (`View : ι → Type*`), because the three
    instances index different things: the three pair marginals of a three-slot
    state in the first two, and every artifact-only reading in the third.

    This is `Core.Coordination`'s `SeparatesFiber` with the summary presented as
    an indexed family instead of a single map — the same content, in the form all
    three published results already have. -/
def NonFactoring {ι : Type*} {State : Type*} {View : ι → Type*} {Datum : Type*}
    (view : (i : ι) → State → View i) (q : State → Datum) : Prop :=
  ∃ x y : State, (∀ i, view i x = view i y) ∧ q x ≠ q y

/-- The witness-pair form is the fiber-separating form: agreeing under every view
    is agreeing under the joint view. -/
theorem separatesFiber_of_nonFactoring {ι State Datum : Type*} {View : ι → Type*}
    {view : (i : ι) → State → View i} {q : State → Datum}
    (h : NonFactoring view q) :
    SeparatesFiber (fun x i => view i x) q := by
  obtain ⟨x, y, hv, hq⟩ := h
  exact ⟨x, y, funext hv, hq⟩

/-- **THE ONE GENERAL CONSEQUENCE.** A quantity with a witness pair is not
    computable from the views: there is no rule whatever — however clever,
    however nonlinear — that takes the whole family of partial readings as its
    input and returns the quantity.

    This is `Core.Coordination`'s `not_computable_from`, reused verbatim. The
    domain argument is doing all the work; `NonFactoring` only puts the three
    published results in the shape that argument accepts. -/
theorem not_computable_of_nonFactoring {ι State Datum : Type*} {View : ι → Type*}
    (view : (i : ι) → State → View i) (q : State → Datum)
    (h : NonFactoring view q) :
    ¬ ∃ g : ((i : ι) → View i) → Datum, ∀ x, q x = g (fun i => view i x) :=
  not_computable_from (fun x i => view i x) q (separatesFiber_of_nonFactoring h)

end CIRISOntology.Core

namespace CIRISOntology.Core.Factoring

variable {X : Type*}

/-- **THE RELATION.** `u` factors through `v`: everything `u` knows, `v`
    determines. The view order of the maximal object. -/
def Factors {C D : Type*} (u : X → C) (v : X → D) : Prop :=
  ∃ h : D → C, u = h ∘ v

theorem factors_refl {C : Type*} (u : X → C) : Factors u u := ⟨id, rfl⟩

theorem factors_trans {C D E : Type*} {u : X → C} {v : X → D} {w : X → E}
    (huv : Factors u v) (hvw : Factors v w) : Factors u w := by
  obtain ⟨h₁, rfl⟩ := huv
  obtain ⟨h₂, rfl⟩ := hvw
  exact ⟨h₁ ∘ h₂, rfl⟩

end CIRISOntology.Core.Factoring

namespace CIRISOntology.Core.View

/-! ### The object -/

/-- **THE OBJECT.** `x` and `y` lie in one fibre of the view `v`: the view
    cannot tell them apart. This is `Setoid.ker v`, unbundled. -/
def SameFibre {X C : Type*} (v : X → C) (x y : X) : Prop := v x = v y

section Basic

variable {X C D : Type*}

theorem sameFibre_iff (v : X → C) (x y : X) : SameFibre v x y ↔ v x = v y := Iff.rfl

theorem sameFibre_refl (v : X → C) (x : X) : SameFibre v x x := rfl

theorem SameFibre.symm {v : X → C} {x y : X} (h : SameFibre v x y) :
    SameFibre v y x := Eq.symm h

theorem SameFibre.trans {v : X → C} {x y z : X} (h₁ : SameFibre v x y)
    (h₂ : SameFibre v y z) : SameFibre v x z := Eq.trans h₁ h₂

theorem sameFibre_equivalence (v : X → C) : Equivalence (SameFibre v) :=
  ⟨sameFibre_refl v, SameFibre.symm, SameFibre.trans⟩

/-- `SameFibre` is Mathlib's kernel setoid of the view. -/
theorem sameFibre_iff_ker (v : X → C) (x y : X) :
    SameFibre v x y ↔ Setoid.ker v x y := Iff.rfl

/-- A coarser view (anything computed from `v`) has coarser fibres. -/
theorem SameFibre.comp {v : X → C} {x y : X} (h : SameFibre v x y) (g : C → D) :
    SameFibre (g ∘ v) x y := congrArg g h

/-- The fibres of the joint view of an indexed family are the intersection of the
    members' fibres: agreeing under the joint view is agreeing under every view. -/
theorem sameFibre_joint {ι : Type*} {V : ι → Type*} (view : (i : ι) → X → V i)
    (x y : X) :
    SameFibre (fun z i => view i z) x y ↔ ∀ i, SameFibre (view i) x y :=
  ⟨fun h i => congrFun h i, fun h => funext h⟩

end Basic

/-! ### Reading 1 — DETERMINES -/

section Determines

variable {X C D : Type*}

/-- Forward half, hypothesis-free: a factoring quantity is constant on fibres. -/
theorem Factors.respects {u : X → C} {v : X → D} (h : Factoring.Factors u v) :
    ∀ x y, SameFibre v x y → u x = u y := by
  obtain ⟨g, rfl⟩ := h
  intro x y hxy
  exact congrArg g hxy

/-- **DETERMINES — THE ONE CHOICE CONSTRUCTION.** `u` factors through `v` iff `u`
    is constant on every fibre of `v`. The reverse direction builds the factoring
    map by choosing a representative of each attained fibre (`Classical.choice`)
    and needs a default value in `C` for readings `v` never attains. Every other
    "fibre-respect gives a map" in the library is derived from this one. -/
theorem factors_iff_respects [Nonempty C] (u : X → C) (v : X → D) :
    Factoring.Factors u v ↔ ∀ x y, SameFibre v x y → u x = u y := by
  refine ⟨Factors.respects, fun hconst => ?_⟩
  classical
  refine ⟨fun s => if hx : ∃ x, v x = s then u hx.choose else Classical.arbitrary C, ?_⟩
  funext x
  have hx : ∃ y, v y = v x := ⟨x, rfl⟩
  simp only [Function.comp_apply, dif_pos hx]
  exact (hconst _ _ hx.choose_spec).symm

/-- **THE CLOSURE FORM, hypothesis-free.** A view determines its own successor
    under `T` iff `T` maps fibres into fibres. No `Nonempty` is needed: if the
    view's codomain is empty so is the state space, and the identity closes the
    square. Derived from `factors_iff_respects`, not re-proved. -/
theorem factors_comp_iff_preserves (v : X → D) (T : X → X) :
    Factoring.Factors (v ∘ T) v ↔ ∀ x y, SameFibre v x y → SameFibre v (T x) (T y) := by
  rcases isEmpty_or_nonempty D with hD | hD
  · have : IsEmpty X := ⟨fun x => hD.false (v x)⟩
    exact ⟨fun _ x => isEmptyElim x, fun _ => ⟨id, funext fun x => isEmptyElim x⟩⟩
  · exact factors_iff_respects (v ∘ T) v

end Determines

/-! ### Reading 2 — BLIND -/

section Blind

variable {X C D : Type*}

/-- **BLIND.** A datum separates a fibre exactly when two states share a fibre of
    the summary and differ in the datum (this is the definition, re-read). -/
theorem separatesFiber_iff (v : X → D) (u : X → C) :
    SeparatesFiber v u ↔ ∃ x y, SameFibre v x y ∧ u x ≠ u y := Iff.rfl

/-- Blindness is the negation of fibre-respect; hypothesis-free. -/
theorem separatesFiber_iff_not_respects (v : X → D) (u : X → C) :
    SeparatesFiber v u ↔ ¬ ∀ x y, SameFibre v x y → u x = u y := by
  unfold SeparatesFiber SameFibre
  push_neg
  exact Iff.rfl

/-- Blindness is non-factoring (needs a default in `C`). -/
theorem separatesFiber_iff_not_factors [Nonempty C] (v : X → D) (u : X → C) :
    SeparatesFiber v u ↔ ¬ Factoring.Factors u v := by
  rw [factors_iff_respects, separatesFiber_iff_not_respects]

/-- **BLIND, indexed form.** `NonFactoring` is a witness pair in one fibre of the
    joint view; hypothesis-free. -/
theorem nonFactoring_iff_sameFibre_joint {ι : Type*} {V : ι → Type*}
    (view : (i : ι) → X → V i) (q : X → C) :
    NonFactoring view q ↔ ∃ x y, SameFibre (fun z i => view i z) x y ∧ q x ≠ q y := by
  constructor
  · rintro ⟨x, y, hv, hq⟩
    exact ⟨x, y, (sameFibre_joint view x y).2 hv, hq⟩
  · rintro ⟨x, y, hv, hq⟩
    exact ⟨x, y, (sameFibre_joint view x y).1 hv, hq⟩

/-- `NonFactoring` is `SeparatesFiber` against the joint view. -/
theorem nonFactoring_iff_separatesFiber_joint {ι : Type*} {V : ι → Type*}
    (view : (i : ι) → X → V i) (q : X → C) :
    NonFactoring view q ↔ SeparatesFiber (fun z i => view i z) q :=
  nonFactoring_iff_sameFibre_joint view q

end Blind

end CIRISOntology.Core.View

namespace CIRISOntology.Core.Factoring

variable {X : Type*}

/-! ### The completeness bridge: factoring is exactly fiber-nonseparation -/

/-- **THE CENTRAL LEMMA.** A quantity factors through a view iff no witness
    pair separates a fiber. The lake's negatives and its licenses are the two
    signs of this biconditional. -/
theorem factors_iff_not_separatesFiber {S D : Type*} [Nonempty D]
    (d : X → D) (summary : X → S) :
    Factors d summary ↔ ¬ SeparatesFiber summary d := by
  rw [View.factors_iff_respects, View.separatesFiber_iff_not_respects, not_not]

end CIRISOntology.Core.Factoring
