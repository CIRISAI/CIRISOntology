/-
CIRISOntology.Core.DiagonalLift — the classical/quantum relation IS the square.

The bridge OBJECT_PRIOR_ART.md priced: the engine's classical tier as the
DIAGONAL view of a quantum carrier, stated as theorems rather than a slogan.

A classical state on `n` outcomes is a probability vector; its lift is the
diagonal density matrix. A classical stochastic map `T` lifts to the channel
"measure in the computational basis, then evolve classically". Three theorems
and a wall:

* `lift_commutes` — the diagonal-lift SQUARE: lifting then applying the
  lifted channel equals stepping classically then lifting. The classical
  tier's dynamics is the quantum carrier's dynamics restricted to diagonals.
* `born_recovers` — computational-basis measurement after the lifted channel
  is the classical step after measurement: the Born view is a `Closed` view
  of the lifted dynamics, with the classical `T` itself as the rate map `h`.
* `diag_view_closed_of_classical` — the two above packaged in the square's
  own vocabulary: `v ∘ E = h ∘ v` with `v` = diagonal readout.
* `bornView_diagEmbed` — the classical tier is a RETRACT of the quantum
  carrier: `bornView ∘ diagEmbed = id`, and `liftChannel T` factors as
  `diagEmbed ∘ push T ∘ bornView` BY DEFINITION (`liftChannel_factors`, rfl) —
  the lifted dynamics is the classical step conjugated by the retract pair,
  and closure of the Born view is a formal consequence of the retraction.
* `hadamard_splits_diagonal` — THE WALL, the founding NonFactoring shape at
  the classical/quantum boundary: two states agreeing on the ENTIRE diagonal
  view (same Born statistics) that a coherence-generating unitary sends to
  states with DIFFERENT diagonals. No rate map `h` can exist for that motion:
  the diagonal view of a coherent dynamics is NOT Closed, and the classical
  tier ends exactly where coherence begins. Convergent art, credited: this is
  Zurek's einselection read through the square — pointer views are the Closed
  ones, and the predictability sieve is closure-selection.

Kill for the lift reading: an in-scope classical-tier behaviour of the engine
NOT reproduced by basis measurement of its lifted dynamics — the conformance
gate the CIRISHolon QASM harness will run at scale.
-/
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import CIRISOntology.Core.Habit
import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic

namespace CIRISOntology.Core.DiagonalLift

open Finset

variable {n : ℕ}

/-- A classical state: nonnegativity and normalization are carried by the
    campaigns that use them; the algebra below needs only the vector. -/
abbrev CState (n : ℕ) := Fin n → ℝ

/-- A stochastic map, row-stochastic entries `T i j = P(j | i)`. -/
abbrev SMap (n : ℕ) := Fin n → Fin n → ℝ

/-- The classical push-forward. -/
def push (T : SMap n) (p : CState n) : CState n := fun j => ∑ i, p i * T i j

/-- The lift of a classical state: the diagonal density matrix, kept as the
    real diagonal (the off-diagonal zeros are the definition, not a loss). -/
def diagEmbed (p : CState n) : Matrix (Fin n) (Fin n) ℝ :=
  Matrix.diagonal p

/-- The diagonal (Born) view of a density matrix. -/
def bornView (ρ : Matrix (Fin n) (Fin n) ℝ) : CState n := fun i => ρ i i

/-- The lifted channel: measure in the computational basis, evolve
    classically, re-prepare. On diagonals this is exactly `T`; on any state
    it reads only the diagonal — the decohering classical embedding. -/
def liftChannel (T : SMap n) (ρ : Matrix (Fin n) (Fin n) ℝ) :
    Matrix (Fin n) (Fin n) ℝ :=
  Matrix.diagonal (push T (bornView ρ))

/-- **The diagonal-lift square commutes**: lift-then-evolve = evolve-then-lift. -/
theorem lift_commutes (T : SMap n) (p : CState n) :
    liftChannel T (diagEmbed p) = diagEmbed (push T p) := by
  unfold liftChannel diagEmbed bornView
  simp [Matrix.diagonal]

/-- **Born measurement recovers the classical step** on every state the
    channel produces. -/
theorem born_recovers (T : SMap n) (ρ : Matrix (Fin n) (Fin n) ℝ) :
    bornView (liftChannel T ρ) = push T (bornView ρ) := by
  funext i
  unfold liftChannel bornView
  simp [Matrix.diagonal]

/-- **The classical tier is a Closed view of its lifted dynamics** — the
    square's own vocabulary: `v ∘ E = h ∘ v` with `v = bornView`, `h = push T`. -/
theorem diag_view_closed_of_classical (T : SMap n) :
    bornView ∘ liftChannel T = push T ∘ (bornView (n := n)) := by
  funext ρ
  exact born_recovers T ρ

/-- **The classical tier is a retract of the quantum carrier.** -/
theorem bornView_diagEmbed : (bornView (n := n)) ∘ diagEmbed = id := by
  funext p i
  simp [bornView, diagEmbed, Matrix.diagonal]

/-- The lifted channel factors THROUGH the classical state space, by
    definition: the conjugation of the classical step by the retract pair. -/
theorem liftChannel_factors (T : SMap n) :
    liftChannel T = diagEmbed ∘ push T ∘ (bornView (n := n)) := rfl

/-! ### The wall: coherence splits the diagonal view -/

/-- Two 2×2 states with the SAME diagonal (same Born view). `ρplus` carries
    coherence `1/2`; `ρmix` carries none. -/
noncomputable def ρplus : Matrix (Fin 2) (Fin 2) ℝ := !![1/2, 1/2; 1/2, 1/2]
noncomputable def ρmix : Matrix (Fin 2) (Fin 2) ℝ := !![1/2, 0; 0, 1/2]

/-- Hadamard conjugation. `H = (1/√2)·[[1,1],[1,−1]]`, so `H ρ H` is
    `(1/2)·H′ρH′` with the UNNORMALIZED `H′` — kept rational on purpose. -/
noncomputable def hadamardMap (ρ : Matrix (Fin 2) (Fin 2) ℝ) :
    Matrix (Fin 2) (Fin 2) ℝ :=
  let H' : Matrix (Fin 2) (Fin 2) ℝ := !![1, 1; 1, -1]
  (1 / 2 : ℝ) • (H' * ρ * H')

/-- **The founding shape at the quantum boundary**: the two states agree on
    the whole diagonal view, and the coherent motion sends them to states
    with DIFFERENT diagonals — so no `h` with `v ∘ U = h ∘ v` exists, and the
    diagonal view of a coherence-generating dynamics is not Closed. -/
theorem hadamard_splits_diagonal :
    bornView ρplus = bornView ρmix ∧
    bornView (hadamardMap ρplus) ≠ bornView (hadamardMap ρmix) := by
  constructor
  · funext i
    fin_cases i <;> simp [bornView, ρplus, ρmix]
  · intro h
    have h0 := congrFun h 0
    simp [bornView, hadamardMap, ρplus, ρmix, Matrix.mul_apply,
          Fin.sum_univ_two, Matrix.smul_apply] at h0

/-- **The fifth witness of the founding shape**: the diagonal view blind to
    coherence, the coherent motion revealing it. -/
theorem nonfactoring_coherence :
    NonFactoring (fun _ : Unit => bornView (n := 2))
      ((bornView (n := 2)) ∘ hadamardMap) :=
  ⟨ρplus, ρmix, fun _ => hadamard_splits_diagonal.1,
    hadamard_splits_diagonal.2⟩

/-- **The wall in the square's own vocabulary**: the diagonal view of a
    coherence-generating motion is not `Closed` — the classical tier ends
    exactly where coherence begins, as a non-closure certificate. -/
theorem diag_not_closed_under_coherence :
    ¬ Habit.Closed (bornView (n := 2)) hadamardMap :=
  (Habit.nonfactoring_iff_not_closed).mp nonfactoring_coherence

end CIRISOntology.Core.DiagonalLift
