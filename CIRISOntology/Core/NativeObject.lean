/-
CIRISOntology.Core.NativeObject — the executable kernel of (World, Views,
Habit), stated once.

SQUINT. The object below is one receipt-bearing commuting square:

    presented phase  ──habit──▶  presented phase
          │ denote                    │ denote
          ▼                            ▼
        World       ──worldHabit──▶   World

The top arrow is partial because an implementation may have to refuse.  Its
input carries the chart witness and epoch that license the solve; an accepted
output carries a receipt.  `Certified.conveys` is the square.  Everything else
in this file says that an accepted square is admissible, receipted, and fresh.

This is the DRY seam.  Nothing here knows whether World is a classical machine
state, a probability distribution, a density operator, or a state indexed by
curvature.  `Core.QuantumObject` specializes World to density operators and
supplies the diagonal embedding of an arbitrary finite classical step.  Thus
"quantum native" does not force chart/receipt logic to be re-proved in quantum
notation, and it does not turn chart data into a physical amplitude.

The Q10 fence/Door/motion split is also world-generic and lives here.  A fence
reads a chart, a Door reads World, and motion reads a transition.  Their types
prevent one reading from being silently laundered into another.
-/
import CIRISOntology.Core.Habit
import Mathlib.Tactic

namespace CIRISOntology.Core.NativeObject

/-! ### The receipt-bearing commuting square -/

/-- A computational presentation consumed by one local solver phase.

    The witness and epoch are part of the input View.  They are not metadata
    that a mesh boundary may drop while forwarding the chart values. -/
structure Phase (Chart Witness : Type*) where
  chart : Chart
  witness : Witness
  epoch : ℕ

/-- An accepted step returns its next presentation and a transition receipt. -/
structure StepResult (Chart Witness Receipt : Type*) where
  phase : Phase Chart Witness
  receipt : Receipt

/-- A charted, partially executable presentation of one World-level Habit.

    `denote` is the View-to-World map.  `habit` is executable and may refuse;
    `worldHabit` is the semantic transition with which every accepted execution
    must commute.  The laws are deliberately kept in `Certified`, so mutants
    and incomplete implementations remain representable and can fail a gate. -/
structure Object (World Chart Witness Receipt Refusal : Type*) where
  denote : Chart → World
  worldHabit : World → World
  admissible : Phase Chart Witness → Prop
  validReceipt : Phase Chart Witness → StepResult Chart Witness Receipt → Prop
  habit : Phase Chart Witness → Except Refusal (StepResult Chart Witness Receipt)

namespace Object

variable {World Chart Witness Receipt Refusal : Type*}

/-- Denotation of a whole presented phase. Witness and epoch license the
    presentation but do not alter which World state its chart denotes. -/
def present (O : Object World Chart Witness Receipt Refusal) :
    Phase Chart Witness → World :=
  fun phase => O.denote phase.chart

/-- The executable Habit accepted `after` from `before`, for some receipt. -/
def Accepts (O : Object World Chart Witness Receipt Refusal)
    (before after : Phase Chart Witness) : Prop :=
  ∃ receipt, O.habit before = .ok ⟨after, receipt⟩

/-- Two phases present the same World state.  This is the fiber relation that
    a representation-change Habit-conveyance test exercises. -/
def SameWorld (O : Object World Chart Witness Receipt Refusal)
    (left right : Phase Chart Witness) : Prop :=
  O.present left = O.present right

/-- The total face of Habit conveyance: `present` semiconjugates a total phase
    step to the declared World Habit. -/
def TotalConveys (O : Object World Chart Witness Receipt Refusal)
    (step : Phase Chart Witness → Phase Chart Witness) : Prop :=
  O.present ∘ step = O.worldHabit ∘ O.present

/-- The old and new object are one object on the total face. A commuting square
    supplies exactly the factoring witness required by `Core.Habit.Closed`; the
    declared World Habit is the induced rate. -/
theorem closed_of_totalConveys (O : Object World Chart Witness Receipt Refusal)
    {step : Phase Chart Witness → Phase Chart Witness}
    (h : O.TotalConveys step) : Habit.Closed O.present step :=
  ⟨O.worldHabit, h⟩

end Object

/-- The four obligations an executable object must earn: admissible endpoints,
    a sound receipt, a fresh epoch, and the commuting square. -/
structure Certified {World Chart Witness Receipt Refusal : Type*}
    (O : Object World Chart Witness Receipt Refusal) : Prop where
  accepts_admissible : ∀ {before out}, O.habit before = .ok out →
    O.admissible before ∧ O.admissible out.phase
  receipt_sound : ∀ {before out}, O.habit before = .ok out →
    O.validReceipt before out
  epoch_succ : ∀ {before out}, O.habit before = .ok out →
    out.phase.epoch = before.epoch + 1
  conveys : ∀ {before out}, O.habit before = .ok out →
    O.present out.phase = O.worldHabit (O.present before)

namespace Certified

variable {World Chart Witness Receipt Refusal : Type*}
variable {O : Object World Chart Witness Receipt Refusal}

/-- Accepted phases cannot smuggle an inadmissible chart across a boundary. -/
theorem admissible_of_accepts (hO : Certified O) {before after}
    (h : O.Accepts before after) :
    O.admissible before ∧ O.admissible after := by
  obtain ⟨receipt, hstep⟩ := h
  exact hO.accepts_admissible hstep

/-- Every accepted phase has a valid receipt. -/
theorem receipt_of_accepts (hO : Certified O) {before after}
    (h : O.Accepts before after) :
    ∃ receipt, O.habit before = .ok ⟨after, receipt⟩ ∧
      O.validReceipt before ⟨after, receipt⟩ := by
  obtain ⟨receipt, hstep⟩ := h
  exact ⟨receipt, hstep, hO.receipt_sound hstep⟩

/-- An inadmissible input must receive a typed refusal, not silent acceptance. -/
theorem invalid_phase_refuses (hO : Certified O) {phase}
    (hbad : ¬ O.admissible phase) :
    ∃ refusal, O.habit phase = .error refusal := by
  cases hstep : O.habit phase with
  | error refusal => exact ⟨refusal, hstep⟩
  | ok out =>
      exact False.elim (hbad (hO.accepts_admissible hstep).1)

/-- **HABIT CONVEYANCE.** If two admissible presentations denote the same
    World state, any accepted certified successor phases still denote the same
    World state.  This is the representation-independent theorem behind Q8's
    MPS rechart probe and mesh gate M-G14. -/
theorem habit_conveyance (hO : Certified O)
    {left right left' right' : Phase Chart Witness}
    (hsame : O.SameWorld left right)
    (hleft : O.Accepts left left') (hright : O.Accepts right right') :
    O.SameWorld left' right' := by
  obtain ⟨leftReceipt, hleftStep⟩ := hleft
  obtain ⟨rightReceipt, hrightStep⟩ := hright
  calc
    O.present left' = O.worldHabit (O.present left) :=
      hO.conveys hleftStep
    _ = O.worldHabit (O.present right) := congrArg O.worldHabit hsame
    _ = O.present right' := (hO.conveys hrightStep).symm

end Certified

/-! ### Q10's three readings, once and without quantum assumptions -/

/-- A chart-internal fence.  `up` does not call the reading an error bound. -/
structure Fence (Chart Reading : Type*) where
  read : Chart → Reading
  up : Reading → Prop

/-- A theorem-pinned external anchor.  A Door reads World, not solver motion. -/
structure Door (World Reading : Type*) where
  read : World → Reading
  holds : Reading → Prop

/-- A transition reading such as monotonicity, residual, or production. -/
structure MotionView (Chart Witness Reading : Type*) where
  read : Phase Chart Witness → Phase Chart Witness → Reading

/-- Q10's chart fence, theorem-pinned Door, and motion reading remain three
    independently warranted Views. -/
structure ThreeLegGate
    (World Chart Witness FenceReading AnchorReading MotionReading : Type*) where
  fence : Fence Chart FenceReading
  door : Door World AnchorReading
  motion : MotionView Chart Witness MotionReading

namespace ThreeLegGate

variable {World Chart Witness Receipt Refusal : Type*}
variable {FenceReading AnchorReading MotionReading Error : Type*}

/-- The joint three-leg reading of a proposed transition. -/
def reading
    (G : ThreeLegGate World Chart Witness
      FenceReading AnchorReading MotionReading)
    (O : Object World Chart Witness Receipt Refusal) :
    Phase Chart Witness × Phase Chart Witness →
      FenceReading × AnchorReading × MotionReading :=
  fun transition =>
    (G.fence.read transition.2.chart,
      G.door.read (O.denote transition.2.chart),
      G.motion.read transition.1 transition.2)

/-- Q10's prohibition stated as a proof obligation: the three certificate legs
    do not determine distance-to-truth.  A concrete study must prove this with
    a separating witness; the name alone grants nothing. -/
def ErrorNotCertified
    (G : ThreeLegGate World Chart Witness
      FenceReading AnchorReading MotionReading)
    (O : Object World Chart Witness Receipt Refusal)
    (error : Phase Chart Witness × Phase Chart Witness → Error) : Prop :=
  ¬ Factoring.Factors error (G.reading O)

end ThreeLegGate

/-- A query may be served, refused, or VOID because the configured family does
    not pose it.  VOID is neither a value nor an ordinary failed gate. -/
inductive Verdict (Refusal Value : Type*) where
  | served : Value → Verdict Refusal Value
  | refused : Refusal → Verdict Refusal Value
  | void : Refusal → Verdict Refusal Value

end CIRISOntology.Core.NativeObject
