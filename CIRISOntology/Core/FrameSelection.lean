/-
CIRISOntology.Core.FrameSelection — the selection problem behind any entropy-to-gravity bridge.

`Core.FrameEntropy` proves that entropy is frame-relative: a frame is a coarse map,
its entropy is the log-cardinality of the corresponding fiber, refinement lowers it,
and independent fibers add. That result is intentionally prior to gravity.

This file attacks the next claim, not the proved one. If an entropy-dependent physical
law is to be intrinsic, the physically admissible frame/screen cannot be an arbitrary
observer choice. Two minimal facts are mechanized here, followed by the important
escape hatch that a covariant gravity theory is allowed to use.

1. ENTROPY LADDER. The same underlying four-state system admits three legitimate
   coarse maps with attained entropies log 4, log 2, and 0. Nothing in the bare
   `frameEntropy` construction selects one of them.

2. SYMMETRY OBSTRUCTION. A UNIQUE intrinsic selector can be impossible: if a symmetry
   fixes the state while acting freely on candidate screens, no equivariant unique
   selector exists.

3. FAMILY DISCHARGE. Uniqueness is not actually required. A Jacobson-style local
   causal-horizon construction may use an entire admissible family. If the physical
   reading is identical across that family, every selector gives the same observable
   and screen choice is physically irrelevant. The real obligation is therefore:
   derive the admissible family from physical structure and prove family consistency,
   not necessarily select one privileged screen.

WHAT THIS DOES NOT PROVE. It does not refute entropic gravity. It makes the fork exact:
either additional physical structure selects a screen, or an admissible horizon family
is derived and the downstream reading is invariant across it. External arbitrary choice
with differing physical predictions remains underdetermined.
-/

import CIRISOntology.Core.FrameEntropy

namespace CIRISOntology.Core.FrameSelection

open FrameEntropy

/-! ### 1. One state, three frame entropies -/

abbrev ToyState := Bool × Bool

/-- The maximally coarse frame: all four fine states have the same reading. -/
def coarseView : ToyState → Unit := fun _ => ()

/-- A one-bit frame: retain only the first coordinate. -/
def halfView : ToyState → Bool := Prod.fst

/-- The fully resolved frame. -/
def fineView : ToyState → ToyState := id

theorem coarse_fiber_card (s : ToyState) :
    (fiber coarseView (coarseView s)).card = 4 := by
  rcases s with ⟨a, b⟩
  cases a <;> cases b <;> decide

theorem half_fiber_card (s : ToyState) :
    (fiber halfView (halfView s)).card = 2 := by
  rcases s with ⟨a, b⟩
  cases a <;> cases b <;> decide

theorem fine_fiber_card (s : ToyState) :
    (fiber fineView (fineView s)).card = 1 := by
  rcases s with ⟨a, b⟩
  cases a <;> cases b <;> decide

/-- Same underlying state, maximally coarse frame: entropy = log 4. -/
theorem coarse_entropy (s : ToyState) :
    frameEntropy coarseView (coarseView s) = Real.log (4 : ℝ) := by
  unfold frameEntropy
  rw [coarse_fiber_card]
  norm_num

/-- Same underlying state, one-bit frame: entropy = log 2. -/
theorem half_entropy (s : ToyState) :
    frameEntropy halfView (halfView s) = Real.log (2 : ℝ) := by
  unfold frameEntropy
  rw [half_fiber_card]
  norm_num

/-- Same underlying state, fully resolved frame: entropy = 0. -/
theorem fine_entropy (s : ToyState) :
    frameEntropy fineView (fineView s) = 0 := by
  unfold frameEntropy
  rw [fine_fiber_card]
  simp

/-- The ambiguity is strict, not merely a relabeling: the three readings disagree. -/
theorem entropy_ladder_strict (s : ToyState) :
    frameEntropy fineView (fineView s)
      < frameEntropy halfView (halfView s)
    ∧ frameEntropy halfView (halfView s)
      < frameEntropy coarseView (coarseView s) := by
  rw [fine_entropy, half_entropy, coarse_entropy]
  constructor
  · exact Real.log_pos (by norm_num)
  · exact Real.strictMonoOn_log (by norm_num) (by norm_num) (by norm_num)

/-! ### 2. Symmetry can forbid a unique intrinsic screen selector -/

/-- Equivariance is the minimum requirement on an intrinsic selector: selecting
    commutes with a transformation of the physical state and its candidate screens. -/
def EquivariantSelector {G State Screen : Type*}
    (stateAct : G → State → State) (screenAct : G → Screen → Screen)
    (choose : State → Screen) : Prop :=
  ∀ g s, choose (stateAct g s) = screenAct g (choose s)

/-- General obstruction. If one transformation fixes a state but has no fixed
    candidate screen, no equivariant rule can select a unique screen for that state. -/
theorem no_equivariant_selector_of_fixed_state_free_screen
    {G State Screen : Type*}
    (stateAct : G → State → State) (screenAct : G → Screen → Screen)
    (g : G) (s : State)
    (state_fixed : stateAct g s = s)
    (screen_free : ∀ q : Screen, screenAct g q ≠ q) :
    ¬ ∃ choose : State → Screen, EquivariantSelector stateAct screenAct choose := by
  rintro ⟨choose, hchoose⟩
  have h := hchoose g s
  rw [state_fixed] at h
  exact screen_free (choose s) h.symm

/-- Bare symmetric state: the nontrivial transformation acts trivially on the state. -/
def bareStateAct : Bool → Unit → Unit := fun _ _ => ()

/-- Two candidate screens exchanged by the nontrivial transformation. -/
def twoScreenAct : Bool → Bool → Bool
  | false, q => q
  | true, q => !q

theorem true_screen_action_has_no_fixed_point :
    ∀ q : Bool, twoScreenAct true q ≠ q := by
  intro q
  cases q <;> decide

/-- Concrete witness: from a completely symmetric bare state and two screens exchanged
    by the symmetry, there is no symmetry-respecting UNIQUE selector. -/
theorem symmetric_bare_state_has_no_intrinsic_screen_selector :
    ¬ ∃ choose : Unit → Bool,
        EquivariantSelector bareStateAct twoScreenAct choose := by
  exact no_equivariant_selector_of_fixed_state_free_screen
    bareStateAct twoScreenAct true () rfl true_screen_action_has_no_fixed_point

/-! ### 3. A consistent horizon family needs no privileged selector -/

/-- A downstream physical reading is family-consistent when every admissible screen
    gives the same observable. The admissibility restriction belongs in the `Screen`
    type supplied by the gravity chart. -/
def FamilyConsistent {Screen Observable : Type*} (read : Screen → Observable) : Prop :=
  ∀ a b, read a = read b

/-- If the admissible horizon family is physically consistent, ANY two screen selectors
    give the same reading. Thus nonexistence of a unique equivariant selector is not a
    gravity kill by itself; observational screen dependence is. -/
theorem selector_irrelevant_of_family_consistent
    {State Screen Observable : Type*}
    (read : Screen → Observable)
    (hread : FamilyConsistent read)
    (choose₁ choose₂ : State → Screen) (s : State) :
    read (choose₁ s) = read (choose₂ s) :=
  hread _ _

end CIRISOntology.Core.FrameSelection
