/-
CIRISOntology.Core.QuantumObject — the quantum-native specialization of the
maximal object, with every finite classical simulator step embedded exactly.

THE DRY SPLIT. `Core.NativeObject` owns the one general object: a partial,
receipt-bearing commuting square between presented phases and World. This file
adds only the genuinely quantum data:

  * `Density H`, the finite-dimensional quantum World;
  * `KrausChannel`, an earned CPTP strengthening for physical evolution;
  * `diagonal` / `observe`, the classical-quantum seam already latent in
    `Core.ShareQuantum` and `Core.EntropyIneq`;
  * `liftClassicalStep`, which turns any finite deterministic step `T` into
    the measure-and-prepare evolution

        ρ ↦ diag (T_* diag(ρ)).

On diagonal input this is exactly `p ↦ T_* p`, not an approximation. Hence a
Newton, contact, damage, rounding, RK4, or static-curvature machine step can be
the World Habit of the same quantum object without materializing its enormous
density matrix. The executable implementation may keep `T` symbolically.

WHAT "ONE OBJECT AT EVERY TIER" CAN MEAN. `TieredDensity` supplies one semantic
state space over the disjoint union `Σ tier, State tier`. An ordinary solve is
required to preserve the tier block (`PreservesTier`). A transition that does
not is a re-root and still owes the receipt/certificate transport that OBJECT
R1 leaves open. Putting every tier in one sum type does not discharge R1.

CURVATURE. A fixed metric/chart may be included in the finite machine basis or
closed over by its step. Then the existing geodesic RK4 map is covered by the
same exact diagonal theorem. Dynamical geometry/backreaction is not thereby
proved: it needs a state family and a licensed geometry-changing Habit. No
claim about quantum gravity is made here.

SCOPE. Exact finite state semantics and exact commuting squares. The general
proof that `liftClassicalStep` has Kraus operators |T(x)><x| is intentionally
still an owed strengthening; this file proves density preservation and exact
classical realization, but does not label that unformalized rung `Physical`.
Approximate equality, trace/diamond norms, POVMs/instruments, and realization
by the Rust floating-point engine are also successors, not hidden assumptions.
-/
import CIRISOntology.Core.NativeObject
import CIRISOntology.Core.EntropyIneq
import CIRISOntology.Core.HammingCap
import Mathlib.Tactic

namespace CIRISOntology.Core.Quantum

open Matrix

/-! ### Quantum states and physical channels -/

/-- A finite-dimensional quantum state. Positivity and unit trace are carried
    by the type rather than re-checked by every View. -/
abbrev Density (H : Type*) [Fintype H] :=
  { ρ : Matrix H H ℂ // IsDensity ρ }

/-- Apply a finite Kraus family to an operator. -/
noncomputable def krausApply {In Out : Type*} [Fintype In]
    (operators : List (Matrix Out In ℂ)) (ρ : Matrix In In ℂ) : Matrix Out Out ℂ :=
  (operators.map fun K => K * ρ * Kᴴ).sum

/-- A finite-dimensional CPTP map presented by Kraus operators.

    `complete` is trace preservation. `mapsDensity` is retained as a proof
    cache at this first seam; constructing a channel still owes both facts. -/
structure KrausChannel (In Out : Type*) [Fintype In] [Fintype Out]
    [DecidableEq In] where
  operators : List (Matrix Out In ℂ)
  complete : (operators.map fun K => Kᴴ * K).sum = 1
  mapsDensity : ∀ ρ, IsDensity ρ → IsDensity (krausApply operators ρ)

namespace KrausChannel

/-- The state-level action of a Kraus channel. -/
noncomputable def applyDensity {In Out : Type*} [Fintype In] [Fintype Out]
    [DecidableEq In] (Φ : KrausChannel In Out) : Density In → Density Out :=
  fun ρ => ⟨krausApply Φ.operators ρ.1, Φ.mapsDensity ρ.1 ρ.2⟩

end KrausChannel

/-! ### The classical face inside the quantum World -/

/-- A finite classical probability state. -/
abbrev Distribution (X : Type*) [Fintype X] :=
  { p : X → ℝ // IsProb p }

/-- Embed a classical distribution as a diagonal density operator. -/
noncomputable def diagonal {X : Type*} [Fintype X] [DecidableEq X]
    (p : Distribution X) : Density X :=
  ⟨diagEmbed (𝕜 := ℂ) p.1, isDensity_diagEmbed p.2⟩

/-- Read the Born probabilities in the declared machine basis. -/
noncomputable def observe {X : Type*} [Fintype X] [DecidableEq X]
    (ρ : Density X) : Distribution X :=
  ⟨diagRe ρ.1, isProb_diagRe ρ.2⟩

/-- Push a classical state through a deterministic step. -/
noncomputable def pushforwardState {X Y : Type*} [Fintype X] [Fintype Y]
    [DecidableEq Y] (T : X → Y) (p : Distribution X) : Distribution Y :=
  ⟨pushforward T p.1, isProb_pushforward T p.2⟩

/-- Lift any classical distribution Habit into the density-operator World by
    observing once and preparing its output diagonally. -/
noncomputable def liftDistributionHabit {X Y : Type*} [Fintype X] [Fintype Y]
    [DecidableEq X] [DecidableEq Y]
    (K : Distribution X → Distribution Y) : Density X → Density Y :=
  fun ρ => diagonal (K (observe ρ))

/-- **THE CLASSICAL CHANNEL INSIDE THE QUANTUM OBJECT.** Measure in the declared
    machine basis, apply `T`, and prepare the resulting basis state. It is
    usable for non-injective and dissipative steps as well as reversible ones. -/
noncomputable def liftClassicalStep {X Y : Type*} [Fintype X] [Fintype Y]
    [DecidableEq X] [DecidableEq Y] (T : X → Y) : Density X → Density Y :=
  liftDistributionHabit (pushforwardState T)

/-- Diagonal embedding followed by observation is exactly the identity. -/
@[simp] theorem observe_diagonal {X : Type*} [Fintype X] [DecidableEq X]
    (p : Distribution X) : observe (diagonal p) = p := by
  apply Subtype.ext
  change diagRe (diagEmbed (𝕜 := ℂ) p.1) = p.1
  exact diagRe_diagonal p.1

/-- Every distribution Habit commutes with the diagonal seam. -/
@[simp] theorem liftDistributionHabit_diagonal {X Y : Type*}
    [Fintype X] [Fintype Y] [DecidableEq X] [DecidableEq Y]
    (K : Distribution X → Distribution Y) (p : Distribution X) :
    liftDistributionHabit K (diagonal p) = diagonal (K p) := by
  simp [liftDistributionHabit]

/-- Deterministic pushforwards compose exactly. -/
theorem pushforwardState_comp {X Y Z : Type*}
    [Fintype X] [Fintype Y] [Fintype Z]
    [DecidableEq Y] [DecidableEq Z]
    (T : X → Y) (U : Y → Z) (p : Distribution X) :
    pushforwardState U (pushforwardState T p) =
      pushforwardState (U ∘ T) p := by
  apply Subtype.ext
  exact pushforward_comp T U p.1

/-- **EXACT CLASSICAL REALIZATION.** On every classical input distribution,
    the lifted quantum evolution is precisely the classical deterministic
    transition—not merely equal on point states or in a small-step limit. -/
@[simp] theorem liftClassicalStep_diagonal {X Y : Type*}
    [Fintype X] [Fintype Y] [DecidableEq X] [DecidableEq Y]
    (T : X → Y) (p : Distribution X) :
    liftClassicalStep T (diagonal p) = diagonal (pushforwardState T p) := by
  simp [liftClassicalStep]

/-- A density evolution realizes a classical step when the diagonal square
    commutes for every classical distribution. -/
def RealizesClassical {X Y : Type*} [Fintype X] [Fintype Y]
    [DecidableEq X] [DecidableEq Y]
    (Φ : Density X → Density Y) (T : X → Y) : Prop :=
  ∀ p, Φ (diagonal p) = diagonal (pushforwardState T p)

/-- The lift realizes its source step by construction. -/
theorem liftClassicalStep_realizes {X Y : Type*}
    [Fintype X] [Fintype Y] [DecidableEq X] [DecidableEq Y]
    (T : X → Y) : RealizesClassical (liftClassicalStep T) T := by
  intro p
  exact liftClassicalStep_diagonal T p

/-- A sequence of classical solves remains exact after quantum lifting. -/
theorem liftClassicalStep_comp_diagonal {X Y Z : Type*}
    [Fintype X] [Fintype Y] [Fintype Z]
    [DecidableEq X] [DecidableEq Y] [DecidableEq Z]
    (T : X → Y) (U : Y → Z) (p : Distribution X) :
    liftClassicalStep U (liftClassicalStep T (diagonal p)) =
      liftClassicalStep (U ∘ T) (diagonal p) := by
  rw [liftClassicalStep_diagonal, liftClassicalStep_diagonal,
    liftClassicalStep_diagonal, pushforwardState_comp]

/-! ### One schema across tiers, without laundering a re-root -/

/-- One quantum state space over a disjoint union of tier-local bases. This is
    a semantic carrier; an implementation should retain its sparse/symbolic
    local representation rather than materialize the global matrix. -/
abbrev TieredDensity (Tier : Type*) (State : Tier → Type*)
    [Fintype (Sigma State)] := Density (Sigma State)

/-- An ordinary intra-tier step stays in its tier block. A step failing this
    predicate is a re-root candidate, not a certified ordinary Habit. -/
def PreservesTier {Tier : Type*} {State : Tier → Type*}
    (T : (Sigma State) → (Sigma State)) : Prop :=
  ∀ x, (T x).1 = x.1

/-! ### Specialization of the native receipt-bearing object -/

abbrev Phase (Chart Witness : Type*) := NativeObject.Phase Chart Witness
abbrev StepResult (Chart Witness Receipt : Type*) :=
  NativeObject.StepResult Chart Witness Receipt

/-- The native object specialized only at World = finite density operators. -/
abbrev Object (H Chart Witness Receipt Refusal : Type*) [Fintype H] :=
  NativeObject.Object (Density H) Chart Witness Receipt Refusal

/-- Certification is exactly the generic commuting-square certification. -/
abbrev Certified {H Chart Witness Receipt Refusal : Type*} [Fintype H]
    (O : Object H Chart Witness Receipt Refusal) : Prop :=
  NativeObject.Certified O

/-- A classical object with the exact same chart/receipt protocol. -/
abbrev ClassicalObject
    (X Chart Witness Receipt Refusal : Type*) [Fintype X] :=
  NativeObject.Object (Distribution X) Chart Witness Receipt Refusal

/-- **THE CONCRETE QUANTUM-NATIVE CONSTRUCTOR.** Lift a complete classical CIRIS
    object, not merely its step function. Chart witnesses, receipts, epochs,
    refusals, and executable control flow are reused exactly; only World and its
    denotation/Habit cross the diagonal quantum seam. -/
noncomputable def liftObject
    {X Chart Witness Receipt Refusal : Type*} [Fintype X] [DecidableEq X]
    (O : ClassicalObject X Chart Witness Receipt Refusal) :
    Object X Chart Witness Receipt Refusal where
  denote := fun chart => diagonal (O.denote chart)
  worldHabit := liftDistributionHabit O.worldHabit
  admissible := O.admissible
  validReceipt := O.validReceipt
  habit := O.habit

/-- The diagonal quantum lift preserves all four native certification gates.
    This is why Newton can reuse the existing CIRIS-native mesh/Q10 protocol
    rather than grow a second quantum-specific certificate language. -/
theorem certified_liftObject
    {X Chart Witness Receipt Refusal : Type*} [Fintype X] [DecidableEq X]
    {O : ClassicalObject X Chart Witness Receipt Refusal}
    (hO : NativeObject.Certified O) : Certified (liftObject O) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro before out hstep
    exact hO.accepts_admissible hstep
  · intro before out hstep
    exact hO.receipt_sound hstep
  · intro before out hstep
    exact hO.epoch_succ hstep
  · intro before out hstep
    have hworld := hO.conveys hstep
    simpa [NativeObject.Object.present, liftObject, liftDistributionHabit] using
      congrArg diagonal hworld

/-- A quantum object is physical when its World Habit is realized by a finite
    Kraus channel. Optimizers such as DMRG need not inhabit this predicate. -/
def Physical {H Chart Witness Receipt Refusal : Type*} [Fintype H]
    [DecidableEq H] (O : Object H Chart Witness Receipt Refusal) : Prop :=
  ∃ Φ : KrausChannel H H, ∀ ρ, O.worldHabit ρ = Φ.applyDensity ρ

/-! ### Quantum aliases for the world-generic Q10 gate -/

abbrev Fence (Chart Reading : Type*) := NativeObject.Fence Chart Reading

abbrev Door (H Reading : Type*) [Fintype H] :=
  NativeObject.Door (Density H) Reading

abbrev MotionView (Chart Witness Reading : Type*) :=
  NativeObject.MotionView Chart Witness Reading

abbrev ThreeLegGate
    (H Chart Witness FenceReading AnchorReading MotionReading : Type*)
    [Fintype H] :=
  NativeObject.ThreeLegGate (Density H) Chart Witness
    FenceReading AnchorReading MotionReading

namespace ThreeLegGate

variable {H Chart Witness Receipt Refusal : Type*} [Fintype H]
variable {FenceReading AnchorReading MotionReading Error : Type*}

/-- Q10's non-factoring obligation, specialized to density-operator World. -/
def ErrorNotCertified
    (G : ThreeLegGate H Chart Witness
      FenceReading AnchorReading MotionReading)
    (O : Object H Chart Witness Receipt Refusal)
    (error : Phase Chart Witness × Phase Chart Witness → Error) : Prop :=
  NativeObject.ThreeLegGate.ErrorNotCertified G O error

end ThreeLegGate

abbrev Verdict (Refusal Value : Type*) := NativeObject.Verdict Refusal Value

end CIRISOntology.Core.Quantum
