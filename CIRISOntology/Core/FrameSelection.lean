/-
CIRISOntology.Core.FrameSelection — the selection problem behind any entropy-to-gravity bridge.

`Core.FrameEntropy` proves that entropy is frame-relative: a frame is a coarse map,
its entropy is the log-cardinality of the corresponding fiber, refinement lowers it,
and independent fibers add. That result is intentionally prior to gravity.

This file attacks the next claim, not the proved one. If an entropy-dependent physical
law is to be intrinsic, the physically admissible frame/screen cannot be an arbitrary
observer choice. Two minimal facts are mechanized here.

1. ENTROPY LADDER. The same underlying four-state system admits three legitimate
   coarse maps with attained entropies log 4, log 2, and 0. Nothing in the bare
   `frameEntropy` construction selects one of them. This is not a defect in
   `FrameEntropy`; it is exactly what frame-relativity means. It becomes an
   underdetermination only for a downstream law that needs one physical entropy.

2. SYMMETRY OBSTRUCTION. An intrinsic selector should be equivariant: transforming
   the physical state and then selecting a screen must agree with selecting first and
   transforming the screen. If a symmetry fixes the bare state while acting freely on
   the candidate screens, no such selector exists. A two-screen witness is exhibited.
   Therefore a symmetric bare holon cannot, by symmetry-respecting logic alone, choose
   one of two symmetry-related screens. Any successful physical selector must get its
   asymmetry from additional structure (boundary conditions, dynamics, a source,
   causal accessibility, an extremality principle, etc.) or return an equivalence
   class rather than one privileged screen.

WHAT THIS DOES NOT PROVE. It does not refute entropic gravity and does not say that
real gravitational states lack the additional structure required to select screens.
It identifies the exact obligation: the selector and temperature must be derived from
physical structure not already contained in the fiber count. If the eventual gravity
chart supplies such structure and makes all admissible choices observationally
identical, this kill is discharged. If it must choose a frame externally, the bridge
is underdetermined.
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

/-- Concrete kill witness: from a completely symmetric bare state and two screens
    exchanged by the symmetry, there is no symmetry-respecting unique selector. -/
theorem symmetric_bare_state_has_no_intrinsic_screen_selector :
    ¬ ∃ choose : Unit → Bool,
        EquivariantSelector bareStateAct twoScreenAct choose := by
  exact no_equivariant_selector_of_fixed_state_free_screen
    bareStateAct twoScreenAct true () rfl true_screen_action_has_no_fixed_point

end CIRISOntology.Core.FrameSelection
