/-
CIRISOntology.Core.Pointing — R2 discharged: the object needs no pointing
primitive, and the reason is not the dynamics.

WHAT FORCED IT. `OBJECT.md` closed the season's unification with two residues,
and R2 was the honest count: the stationarity ideal (`Core/SelfAudit`, last
section) is `Factors` PLUS a POINTING — the audit's distinguished "reads clean"
value `φ 0 = 0`. One relation and one pointing; two primitives, not one. The
commission was to pull that thread, with a hypothesis to refute first: that the
pointing is HABIT'S TRACE ON THE ORDER — every distinguished zero being some
dynamics' rest state, projected into a view.

THE SURVEY SAID MIXED, AND THE HYPOTHESIS IS THE MINORITY READING. Of the
pointings in the lake, three are rest states of a step map the structure names
(`Stagnation.motion`, the rent clause's payment deficit, and a self-consistent
process's residual). The rest are not, and no amount of goodwill makes them so:
a chart's deviation from the truth is a difference with no dynamics anywhere
near it; VOID is the view order's TOP (the contrast constant on the design);
determinacy is the view order's FLOOR (the fiber down to a singleton); the
whole-only share's zero is the rest state of an idempotent the ORDER generates,
not of Habit.

THE FINDING, and it is the families:

  **THE OBJECT NEEDS NO POINTING PRIMITIVE, BECAUSE EVERY POINTING IN THE LAKE
  IS THE COINCIDENCE SET OF MAPS THE OBJECT ALREADY NAMES** — in exactly five
  parent families:

    1. HABIT'S REST — `Coincide T id`. Witnessed here: `motion_eq_zero_iff_fixed`,
       `rentDeficit_eq_zero_iff_fixed`.
    2. VIEW-INDUCED SELF-PROJECTION — the fixed set of an idempotent the order
       generates (`rest_idempotent_eq_range` is its abstract shape; see the
       CREDIT and the NOT-MECHANIZED note below).
    3. SYMMETRY — the fixed set of a group action (`Core/SignSymmetry`'s zero
       is contained in it; classified, not re-proved here).
    4. THE DIAGONAL — truth against chart (`deviation_eq_zero_iff`). This is
       the door's home: `Core/SelfAudit`'s pinned observable.
    5. THE ORDER'S EXTREMES — the fiber at its floor and at its ceiling
       (`frameEntropy_eq_zero_iff`, `void_clean_eq_univ`).

WHAT THE FINDING IS NOT, and this fence is load-bearing. It is NOT "the pointing
derives from equality," and it is NOT "everything is an equalizer." Both are
EMPTY, and this file proves they are: `exists_step_with_rest_eq` exhibits, for
ANY pointed view on ANY state space with two points, a step map whose rest set is
exactly the clean locus; `coincide_const_eq_clean` does the same for equalizers
in one line. So "the zero is the rest state of SOME dynamics" and "the zero is
the coincidence set of SOME pair" say nothing whatever. The content is entirely
in NAMED: the maps are the ones the structure already carries, and the basepoint
is then FORCED rather than chosen (`basepoint_forced` — a view constant on the
locus admits exactly one clean value, and constancy is a real condition that
`not_restPointed_witness` shows can fail).

R2 ITSELF, CASHED. `StationarityAudit g A` is `Factors A g` plus `φ 0 = 0`, and
the pointing is ELIMINABLE: `factors_const_of_residual_eq` shows that factoring
ALONE forces the audit to be constant wherever the residual is, with no `Zero` on
the audit's codomain and no pointing in sight. The ideal's `φ 0 = 0` does not
decide which charts read clean; it NAMES the constant that `Factors` already
forced to exist (`clean_value_forced`). What the naming buys is calibration, and
the price is exact: without it the escape criterion needs TWO converged charts
reading differently (`not_factors_of_two_converged_differ`), and the one-point
version convicts the CONJUNCTION of factoring and calibration
(`fires_at_pinned_convicts`) — so ONE-POINT ESCAPE IS EXACTLY WHAT AN IMPORTED
TRUTH-PINNING THEOREM PAYS FOR, WHICH IS THE DOOR. R2's pointing traces to
`pinned_error_computable_from_chart`, not to Habit.

THE VALVE FENCE (the survey's observation, recorded so no reader conflates two
different relations to Habit). `Core/Valve`'s `valve_from_nothing` makes the
`share = 0` locus a FORWARD-INVARIANT SET of the noisy dynamics: independent
cells in, independent cells out. That is a conservation law, NOT a fixed-point
set — no state in it need be held still. `rest_invariantSet` shows rest implies
invariance; `invariantSet_ne_rest` shows the converse fails outright. The valve's
zero belongs to family 2, and its invariance under family 1 is a separate fact.

NOT MECHANIZED HERE, said plainly. That `share p = 0` holds exactly on the range
of the pair-marginal I-projection is NOT proved in this file; only the abstract
shape (`rest_idempotent_eq_range`) is. Family 3's containment is likewise a
classification of `Core/SignSymmetry`'s theorem, not a new proof. The honest
split is the same one `Core/ModeChart` makes for the sector count: the shape is
machine-checked, the instance is named and left where it lives.

CREDIT, generously, because none of the mathematics is ours. The shape is the
EQUALIZER (Mac Lane) — `Fix T = Eq(T, id)`, the diagonal is `Eq(π₁, π₂)`, VOID is
`Eq(contrast, const)`. Pointed sets and based spaces supply the pointing; the
AUGMENTATION IDEAL (maps vanishing at the basepoint) is literally what
`StationarityAudit` is, which is what `OBJECT.md`'s "pointed part of the cone"
was already saying in other words; `Option`'s basepoint is the same object in
programming clothes. Idempotent splitting and Knaster–Tarski stand behind family
2's abstract shape, and Csiszár's I-projection is the specific idempotent under
the whole-only share's zero. OURS IS THE IDENTIFICATION AND THE FENCE: that the
lake's dozen zeros fall into these five families, and that the existential
reading of any of them is vacuous.

SCOPE. A model brick over arbitrary types: no physics, no statistics, nothing
about the world. It does not claim the five families are exhaustive of pointings
in general — only that they exhaust the pointings SURVEYED (`Core/SelfAudit`,
`Core/Stagnation`, `Core/Maintenance`, `Core/Valve`, `Core/Creation`,
`Core/Coordination`, `Core/GrainFloor`, `Core/Posed`, `Core/FrameEntropy`,
`Core/Lattice`). Two surveyed structures carry NO pointing at all and are
recorded as such: `GrainFloor`'s refusal is a threshold compared against
tier-local data (which is exactly why capacity cannot move it and a re-root can),
and `Lattice.np` is an invariant with no distinguished value. Kill, separable:
exhibit a pointed structure in this lake whose clean locus is not the coincidence
set of maps the structure already names — one outside all five families — and R2
returns to primitive status with the miss recorded. Note what does NOT count,
by `exists_step_with_rest_eq`: producing a dynamics after the fact to fit a zero
is not evidence, in either direction.
-/
import CIRISOntology.Core.Stagnation
import CIRISOntology.Core.Maintenance
import CIRISOntology.Core.Factoring
import CIRISOntology.Core.FrameEntropy
import Mathlib.Tactic

namespace CIRISOntology.Core.Pointing

open CIRISOntology.Core.SelfAudit CIRISOntology.Core.Factoring

variable {X : Type*}

/-! ### The three objects, and the one that is data

A POINTED VIEW is a view plus a distinguished value of its codomain — the "reads
clean" datum R2 counted as a second primitive. A COINCIDENCE SET is where two
maps agree. REST is the coincidence set of a step map with the identity. -/

/-- The clean locus of a pointed view: the states that read the distinguished
    value. This set is what a pointing actually asserts about the world. -/
def Clean {C : Type*} (v : X → C) (c₀ : C) : Set X := {x | v x = c₀}

/-- The coincidence set (the equalizer) of two maps. -/
def Coincide {Y : Type*} (f g : X → Y) : Set X := {x | f x = g x}

/-- The rest set of a step map: the coincidence of the dynamics with standing
    still. `Habit`'s contribution to the pointing question, and only its. -/
def Rest (T : X → X) : Set X := Coincide T id

theorem mem_rest_iff {T : X → X} {x : X} : x ∈ Rest T ↔ T x = x := Iff.rfl

/-- A view is CALIBRATED on a set when it cannot tell the set's states apart.
    This is the condition under which a pointing is forced rather than chosen. -/
def CalibratedOn {C : Type*} (v : X → C) (S : Set X) : Prop :=
  ∀ ⦃x⦄, x ∈ S → ∀ ⦃y⦄, y ∈ S → v x = v y

/-- **THE POINTING IS FORCED, NOT CHOSEN.** A view constant on a nonempty locus
    admits exactly one clean value — so where calibration holds, the basepoint
    carries no information beyond the locus and the view. This is the entire
    content of the derivation, and the reason the vacuous readings fenced below
    are not it. -/
theorem basepoint_forced {C : Type*} {v : X → C} {S : Set X} (hne : S.Nonempty)
    (h : CalibratedOn v S) : ∃! c₀ : C, ∀ x ∈ S, v x = c₀ := by
  obtain ⟨x₀, hx₀⟩ := hne
  refine ⟨v x₀, fun x hx => h hx hx₀, ?_⟩
  intro c hc
  exact (hc x₀ hx₀).symm

/-- A pointed view is REST-POINTED for a NAMED step map when its clean locus is
    exactly that map's rest set. The name is the content; see the fence. -/
def RestPointed {C : Type*} (T : X → X) (v : X → C) (c₀ : C) : Prop :=
  Clean v c₀ = Rest T

theorem restPointed_calibrated {C : Type*} {T : X → X} {v : X → C} {c₀ : C}
    (h : RestPointed T v c₀) : CalibratedOn v (Rest T) := by
  intro x hx y hy
  rw [← h] at hx hy
  exact hx.trans hy.symm

/-- Rest-pointing forces the basepoint: the clean value is the view's reading at
    rest, and there is no second datum anywhere. -/
theorem restPointed_basepoint_forced {C : Type*} {T : X → X} {v : X → C} {c₀ : C}
    (h : RestPointed T v c₀) (hne : (Rest T).Nonempty) :
    ∃! c : C, ∀ x ∈ Rest T, v x = c :=
  basepoint_forced hne (restPointed_calibrated h)

/-! ### The fence: the existential readings are EMPTY

Both the commissioned hypothesis ("every pointing is some dynamics' rest state")
and its natural generalization ("every pointing is some pair's coincidence set")
are true of EVERYTHING, hence assert nothing. These two theorems are why the
definitions above quantify over a NAMED map and why `CalibratedOn` — a condition
that can fail — is where the content sits. -/

/-- **THE VACUITY BOMB.** For ANY subset of ANY state space with two points there
    is a step map whose rest set is exactly that subset. So "the clean locus is
    the rest state of some dynamics" is satisfiable for every pointing ever
    written down, and producing a dynamics after the fact to fit a zero is not
    evidence about anything. -/
theorem exists_step_with_rest_eq [Nontrivial X] (S : Set X) : ∃ T : X → X, Rest T = S := by
  classical
  obtain ⟨a, b, hab⟩ := exists_pair_ne X
  refine ⟨fun x => if x ∈ S then x else if x = a then b else a, ?_⟩
  ext x
  simp only [Rest, Coincide, Set.mem_setOf_eq, id_eq]
  by_cases hx : x ∈ S
  · simp [hx]
  · simp only [hx, if_false]
    by_cases hxa : x = a
    · subst hxa
      simp [hx, Ne.symm hab]
    · rw [if_neg hxa]
      simp [hx, Ne.symm hxa]

/-- **THE SAME BOMB FOR EQUALIZERS**, in one line: every clean locus is the
    coincidence set of the view with a constant. "Everything is an equalizer" is
    exactly as empty as "everything is at rest," and neither is the finding. -/
theorem coincide_const_eq_clean {C : Type*} (v : X → C) (c₀ : C) :
    Coincide v (fun _ => c₀) = Clean v c₀ := rfl

/-- And the definition is not vacuous in the other direction either: a pointed
    view can fail to be rest-pointed for a given dynamics. The identity map holds
    every state at rest, while the identity view reads clean at one state only. -/
theorem not_restPointed_witness : ¬ RestPointed (id : ℝ → ℝ) (id : ℝ → ℝ) 0 := by
  intro h
  have h1 : (1 : ℝ) ∈ Rest (id : ℝ → ℝ) := mem_rest_iff.mpr rfl
  rw [← h] at h1
  simp only [Clean, Set.mem_setOf_eq, id_eq] at h1
  exact one_ne_zero h1

/-! ### Family 1 — HABIT'S REST, witnessed twice

The two structures in the lake whose zeros really are the commissioned
hypothesis. `Core/Stagnation` keeps its one-directional statement; the
biconditional is new, and it is what makes the classification a theorem. -/

/-- **WITNESS 1.** The motion residual vanishes EXACTLY at the fixed points —
    `Core/Stagnation.motion_eq_zero_of_fixed` upgraded to a biconditional, which
    is what a classification needs and an implication does not supply. -/
theorem motion_eq_zero_iff_fixed (T : ℝ → ℝ) (x : ℝ) :
    Stagnation.motion T x = 0 ↔ T x = x := by
  simp [Stagnation.motion, sub_eq_zero]

/-- Stagnation's zero is rest-pointed for the iteration it is the motion of. -/
theorem motion_restPointed (T : ℝ → ℝ) : RestPointed T (Stagnation.motion T) 0 := by
  ext x
  simp only [Clean, Rest, Coincide, Set.mem_setOf_eq, id_eq]
  exact motion_eq_zero_iff_fixed T x

/-- The rent deficit at a payment: what the payment falls short of what decay
    takes. `Core/Maintenance.step γ α S = S - γ * S + α`, so this residual is
    literally `step - id`. -/
def rentDeficit (γ α S : ℝ) : ℝ := α - γ * S

/-- **WITNESS 2.** Rent paid in full is exactly the fixed point of the paid step:
    the ledger's "reads clean" IS the dynamics at rest, as a theorem rather than
    as a reading. -/
theorem rentDeficit_eq_zero_iff_fixed (γ α S : ℝ) :
    rentDeficit γ α S = 0 ↔ CIRISOntology.Core.step γ α S = S := by
  unfold rentDeficit CIRISOntology.Core.step
  constructor <;> intro h <;> linarith

/-- The rent clause's zero is rest-pointed for the paid step. -/
theorem rent_restPointed (γ α : ℝ) :
    RestPointed (CIRISOntology.Core.step γ α) (rentDeficit γ α) 0 := by
  ext S
  simp only [Clean, Rest, Coincide, Set.mem_setOf_eq, id_eq]
  exact rentDeficit_eq_zero_iff_fixed γ α S

/-- And the deficit reads zero exactly at the payment `Core/Maintenance`'s
    `rent_holds` names, so the two statements are one statement. -/
theorem rentDeficit_eq_zero_iff_paid (γ α S : ℝ) :
    rentDeficit γ α S = 0 ↔ α = γ * S := sub_eq_zero

/-! ### R2 itself: the stationarity ideal's pointing is a NAME

The residue as `OBJECT.md` stated it: the ideal is `Factors` plus `φ 0 = 0`. The
theorems below show the second conjunct does no work in the obstruction, what it
does buy, and what that costs when it is withdrawn. -/

variable {R A' : Type*}

/-- **THE UNPOINTED OBSTRUCTION.** Factoring alone forces the audit to agree
    wherever the residual agrees. No `Zero` on either codomain, no pointing, no
    convergence: this is the whole of `stationarityAudit_blind`'s content, and it
    is strictly more general than the pointed statement. -/
theorem factors_const_of_residual_eq {g : X → R} {A : X → A'}
    (h : Factors A g) {x y : X} (hg : g x = g y) : A x = A y := by
  obtain ⟨φ, hφ⟩ := h
  rw [hφ]
  simp only [Function.comp_apply, hg]

/-- The same, on the converged set: every audit factoring through the residual
    reads ONE value on every converged chart, however wrong those charts are. -/
theorem factors_blind_on_converged [Zero R] {g : X → R} {A : X → A'}
    (h : Factors A g) {x y : X} (hx : Converged g x) (hy : Converged g y) :
    A x = A y :=
  factors_const_of_residual_eq h (hx.trans hy.symm)

/-- **THE POINTING IS A NAME.** Given one converged chart, factoring already
    determines a unique value the audit takes on all of them. `φ 0 = 0` does not
    decide which charts read clean — it labels the constant `Factors` had already
    forced into existence. That is R2, discharged. -/
theorem clean_value_forced [Zero R] {g : X → R} {A : X → A'}
    (h : Factors A g) {x₀ : X} (hx₀ : Converged g x₀) :
    ∃! a₀ : A', ∀ x, Converged g x → A x = a₀ :=
  basepoint_forced (S := {x | Converged g x}) ⟨x₀, hx₀⟩
    (fun _ hx _ hy => factors_blind_on_converged h hx hy)

/-- **THE ESCAPE CRITERION, UNPOINTED**, and the honest price of dropping the
    basepoint: two converged charts that disagree convict the factoring, where
    the pointed version needed only one. -/
theorem not_factors_of_two_converged_differ [Zero R] {g : X → R} {A : X → A'}
    {x y : X} (hx : Converged g x) (hy : Converged g y) (hne : A x ≠ A y) :
    ¬ Factors A g :=
  fun h => hne (factors_blind_on_converged h hx hy)

/-- **AND WHAT THE DOOR PAYS FOR.** A single converged chart firing against an
    externally supplied clean value convicts a CONJUNCTION: either the audit does
    not factor through the residual, or the supplied value was never the audit's
    reading at rest. One-point escape is exactly what an imported truth-pinning
    theorem buys — `Core/SelfAudit.pinned_error_computable_from_chart` is the
    purchase, and the symmetry anchors (Lieb, particle-hole) are the currency.
    The calibration is a claim about the world, imported; it is not a primitive
    of the object. -/
theorem fires_at_pinned_convicts [Zero R] {g : X → R} {A : X → A'} {a₀ : A'} {x : X}
    (hx : Converged g x) (hfire : A x ≠ a₀) :
    ¬ (Factors A g ∧ ∃ y, Converged g y ∧ A y = a₀) := by
  rintro ⟨hf, y, hy, hcal⟩
  exact hfire ((factors_blind_on_converged hf hx hy).trans hcal)

/-- The ideal, decomposed: `StationarityAudit` is exactly the factoring plus one
    calibration datum at one converged chart. Both halves are already theorems
    elsewhere; putting them side by side is what makes the pointing's role
    visible. -/
theorem stationarityAudit_calibrated [Zero R] [Zero A'] {g : X → R} {A : X → A'}
    (hA : StationarityAudit g A) {x : X} (hx : Converged g x) :
    Factors A g ∧ ∃ y, Converged g y ∧ A y = 0 :=
  ⟨stationarityAudit_factors hA, x, hx, stationarityAudit_blind hA hx⟩

/-- **THE RECOVERED COROLLARY.** Blindness at every converged chart follows from
    factoring plus the calibration at ONE of them. `stationarityAudit_blind` is
    this with the calibration supplied by `φ 0 = 0`; nothing else in the ideal is
    doing work. -/
theorem blind_of_factors_of_calibrated [Zero R] {g : X → R} {A : X → A'} {a₀ : A'}
    (hf : Factors A g) {y : X} (hy : Converged g y) (hcal : A y = a₀)
    {x : X} (hx : Converged g x) : A x = a₀ :=
  (factors_blind_on_converged hf hx hy).trans hcal

/-! ### Family 2 — VIEW-INDUCED SELF-PROJECTION, and the valve fence

The whole-only share's zero and the pairwise instrument's floor are rest states
of an idempotent, but the idempotent is generated by the VIEW ORDER (replace the
state by the maximum-entropy state carrying its pair data), not by Habit. Only
the abstract shape is proved here; see the header's NOT MECHANIZED note and the
credit to Csiszár. -/

/-- The abstract shape of family 2: an idempotent's rest set is exactly its
    range. Standard (idempotent splitting); recorded so the classification has a
    machine-checked skeleton even though its instance lives elsewhere. -/
theorem rest_idempotent_eq_range {M : X → X} (hM : ∀ x, M (M x) = M x) :
    Rest M = Set.range M := by
  ext x
  constructor
  · intro hx
    exact ⟨x, hx⟩
  · rintro ⟨y, rfl⟩
    show M (M y) = M y
    exact hM y

/-- A set the dynamics maps into itself. Weaker than rest, and the distinction is
    the fence below. -/
def InvariantSet (T : X → X) (S : Set X) : Prop := ∀ ⦃x⦄, x ∈ S → T x ∈ S

/-- Rest implies invariance. -/
theorem rest_invariantSet (T : X → X) : InvariantSet T (Rest T) := by
  intro x hx
  have hfx : T x = x := hx
  show T (T x) = T x
  exact congrArg T hfx

/-- **THE VALVE FENCE.** Invariance does not imply rest — not even nearly: here
    is a dynamics with a forward-invariant set and NO fixed point at all.
    `Core/Valve.valve_from_nothing` makes the `share = 0` locus forward-invariant
    (independent cells in, independent cells out); that is a conservation law
    about the locus, not a claim that anything in it is held still. The two
    relations to Habit must not be conflated, and after this theorem they
    cannot be. -/
theorem invariantSet_ne_rest :
    ∃ (T : ℝ → ℝ) (S : Set ℝ), InvariantSet T S ∧ S ≠ Rest T := by
  refine ⟨fun x => x + 1, Set.univ, fun _ _ => Set.mem_univ _, ?_⟩
  intro h
  have h0 : (0 : ℝ) ∈ Rest (fun x : ℝ => x + 1) := by
    rw [← h]; exact Set.mem_univ 0
  have h1 : (0 : ℝ) + 1 = 0 := h0
  norm_num at h1

/-! ### Family 4 — THE DIAGONAL

`Core/SelfAudit`'s deviation is a difference, and its zero is the coincidence of
the chart with the truth. No dynamics is involved at any point, which is why the
commissioned hypothesis cannot reach it. -/

/-- The chart audits clean exactly when it coincides with the truth: the zero of
    a difference is the diagonal, and this is the pointing the door supplies. -/
theorem deviation_eq_zero_iff (w : World ℝ) :
    deviation w = 0 ↔ w.truth = w.chart := sub_eq_zero

/-! ### Family 5 — THE ORDER'S EXTREMES, and the DRY find

VOID and determinacy are the SAME object at its two ends. `Core/Posed`'s VOID is
the contrast's fiber swallowing the whole design — frame entropy at its ceiling.
`Core/FrameEntropy`'s zero is the fiber down to a singleton — the same quantity
at its floor. Both are pointings of the fiber, and the fiber is already in the
object; neither needs a dynamics, and neither gets one. -/

variable {State Chart : Type*} [Fintype State] [DecidableEq Chart]

/-- **THE FLOOR, as a biconditional.** `Core/FrameEntropy` proves one direction;
    the classification needs both. Frame entropy reads zero at an attained
    reading exactly when the frame pins the state — the view's fiber collapsed to
    the diagonal. -/
theorem frameEntropy_eq_zero_iff (view : State → Chart) (s : State) :
    FrameEntropy.frameEntropy view (view s) = 0 ↔
      (FrameEntropy.fiber view (view s)).card = 1 := by
  constructor
  · intro h
    have hpos : 0 < (FrameEntropy.fiber view (view s)).card :=
      Finset.card_pos.mpr ⟨s, FrameEntropy.mem_fiber_self view s⟩
    unfold FrameEntropy.frameEntropy at h
    rcases Real.log_eq_zero.mp h with h0 | h1 | hneg
    · exfalso
      have hc : (FrameEntropy.fiber view (view s)).card = 0 := by exact_mod_cast h0
      omega
    · exact_mod_cast h1
    · exfalso
      have hnn : (0 : ℝ) ≤ ((FrameEntropy.fiber view (view s)).card : ℝ) :=
        Nat.cast_nonneg _
      rw [hneg] at hnn
      norm_num at hnn
  · exact FrameEntropy.frameEntropy_eq_zero_of_card_one

/-- **THE CEILING.** A view that separates nothing has every fiber equal to the
    whole space — the other end of the same quantity. -/
theorem constant_iff_fibers_univ (view : State → Chart) :
    (∀ a b : State, view a = view b) ↔
      ∀ s : State, FrameEntropy.fiber view (view s) = Finset.univ := by
  constructor
  · intro h s
    ext t
    simp [FrameEntropy.fiber, h t s]
  · intro h a b
    have hmem : a ∈ FrameEntropy.fiber view (view b) := by
      rw [h b]; exact Finset.mem_univ a
    simpa [FrameEntropy.fiber] using hmem

/-- And the reading there is the largest the frame can give: the ceiling is
    `log` of the whole state space. -/
theorem frameEntropy_eq_log_card_of_constant {view : State → Chart}
    (h : ∀ a b : State, view a = view b) (s : State) :
    FrameEntropy.frameEntropy view (view s) = Real.log (Fintype.card State) := by
  unfold FrameEntropy.frameEntropy
  rw [(constant_iff_fibers_univ view).mp h s, Finset.card_univ]

/-- **VOID IS THE TOP.** A design that does not pose its contrast is one whose
    contrast is constant on it — and then the clean locus of the pointed view is
    the WHOLE design. `Core/Posed`'s distinguished outcome is the view order's
    ceiling, reached with no dynamics anywhere in the statement. -/
theorem not_poses_iff_constant {C V : Type*} (design : Set C) (contrast : C → V) :
    ¬ Posed.Poses design contrast ↔ ∀ a ∈ design, ∀ b ∈ design, contrast a = contrast b := by
  constructor
  · intro h a ha b hb
    by_contra hne
    exact h ⟨a, ha, b, hb, hne⟩
  · exact Posed.not_poses_of_constant

/-- VOID's clean locus, exhibited as the top: everything the design contains. -/
theorem void_clean_eq_univ {C V : Type*} {design : Set C} {contrast : C → V}
    (h : ¬ Posed.Poses design contrast) (a₀ : design) :
    Clean (fun x : design => contrast x.val) (contrast a₀.val) = Set.univ := by
  ext x
  simp only [Clean, Set.mem_setOf_eq, Set.mem_univ, iff_true]
  exact (not_poses_iff_constant design contrast).mp h x.val x.property a₀.val a₀.property

end CIRISOntology.Core.Pointing
