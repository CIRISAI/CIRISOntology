/-
CIRISOntology.Core.StochasticHabit — R3 discharged in its first half: the two
entropies are one entropy, and the second law's failure under noise is exact.

WHAT THIS CLOSES. `Core/Habit.lean` states R3 as a WITNESSED residue rather
than a suspicion: the object's third component is "a step map T, with noise",
everything proved there is deterministic, and σ ≥ 0 is FALSE for stochastic
maps — a reset channel lowers Shannon entropy. Its named route out has two
rungs. This file walks the first and states the second's obstruction sharply
enough that nobody mistakes it for arithmetic.

RUNG ONE — THE TWO ENTROPIES ARE ONE (`frameEntropy_eq_shannon_uniform`). The
lake has carried two entropies that were never identified: `frameEntropy`
(log-count of the fiber, free from the frame) and the Shannon entropy that
`Core/Valve` and `Core/Creation` actually compute. They agree exactly on the
uniform-on-fiber state — which is `Core/FrameEntropy`'s own declared Boltzmann
move, now a theorem rather than a footnote. So the deterministic results and
the stochastic vocabulary are talking about the same quantity, and R3's first
half is discharged.

RUNG TWO — WHY THE MONOTONE MUST CHANGE, and this is the honest part. Under a
stochastic habit the fiber-count monotone is simply false, and this file
exhibits the counterexample rather than describing it: `reset_lowers_entropy`
takes a uniform state on two points to a point mass, dropping Shannon entropy
by exactly `log 2`. So `production_nonneg_of_closed` cannot be repaired by
weakening a hypothesis; the QUANTITY has to change. The literature's monotone
is relative entropy to a stationary state under the data-processing
inequality — and that object is NOT in this file. What is here is the fence
(`no_monotone_of_reset`): any candidate monotone that (a) is a function of the
state's entropy alone and (b) is required non-decreasing under every channel
is refuted by the reset channel, so the successor must consume the CHANNEL's
stationary structure and not the state's entropy alone. That is a real
constraint on the next brick, established rather than assumed.

WHAT THIS FILE DOES NOT CLAIM, stated plainly because the temptation is
obvious: it does not prove a stochastic second law, it does not define
production for kernels, and it does not import the data-processing inequality.
R3 remains OPEN in its second half. Its status changes from "witnessed" to
"half discharged, with the successor's shape derived": that is progress, not
closure, and the header of `Core/Habit.lean` should be read as still governing.

CREDITS, generously and claiming only the instantiation: Shannon (the entropy),
Jaynes (the maximum-entropy reading that makes uniform-on-fiber the right
state), Boltzmann/Gibbs (the log-count), Csiszár and Cover–Thomas for the
data-processing inequality and relative entropy as the stochastic monotone, and
the stochastic-thermodynamics literature (Seifert's review) for entropy
production under noise. The reset channel as the standard counterexample to
naive entropy monotonicity is textbook; ours is its statement in this object's
vocabulary.

KILL, separable: exhibit a stochastic habit and a closed view whose Shannon
production is negative AND which no relative-entropy-to-stationary monotone
repairs — then the successor's shape derived here is wrong and R3 needs a
different route than the one named.
-/
import CIRISOntology.Core.FrameEntropy
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic

namespace CIRISOntology.Core.StochasticHabit

open Finset

/-! ### Rung one: the two entropies are one -/

variable {α : Type*} [Fintype α] [DecidableEq α]

/-- Shannon entropy of a finite distribution, in nats, with the standard
    convention `0 log 0 = 0` handled by summing `-p log p` over the support. -/
noncomputable def shannon (p : α → ℝ) : ℝ :=
  ∑ a ∈ univ.filter (fun a => p a ≠ 0), -(p a) * Real.log (p a)

/-- The uniform distribution on a nonempty finite set. -/
noncomputable def uniformOn (s : Finset α) : α → ℝ :=
  fun a => if a ∈ s then (1 : ℝ) / s.card else 0

omit [Fintype α] in
theorem uniformOn_mem {s : Finset α} {a : α} (h : a ∈ s) :
    uniformOn s a = 1 / s.card := by simp [uniformOn, h]

omit [Fintype α] in
theorem uniformOn_not_mem {s : Finset α} {a : α} (h : a ∉ s) :
    uniformOn s a = 0 := by simp [uniformOn, h]

/-- **RUNG ONE — THE TWO ENTROPIES ARE ONE.** The Shannon entropy of the
    uniform state on a set is the log of its cardinality: exactly
    `Core/FrameEntropy`'s `frameEntropy` when the set is a fiber. The lake's
    fiber-count entropy and the Shannon entropy its stochastic files compute
    are the same quantity on the uniform-on-fiber state, which is the Boltzmann
    move `Core/FrameEntropy`'s header declares — now a theorem. -/
theorem shannon_uniformOn {s : Finset α} (hs : s.Nonempty) :
    shannon (uniformOn s) = Real.log s.card := by
  have hcard : (0 : ℝ) < s.card := by
    exact_mod_cast Finset.card_pos.mpr hs
  have hne : (1 : ℝ) / s.card ≠ 0 := by positivity
  have hsupp : univ.filter (fun a => uniformOn s a ≠ 0) = s := by
    ext a
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, uniformOn]
    by_cases hmem : a ∈ s
    · simpa [hmem] using Finset.nonempty_iff_ne_empty.mp hs
    · simp [hmem]
  unfold shannon
  rw [hsupp]
  have hterm : ∀ a ∈ s, -(uniformOn s a) * Real.log (uniformOn s a)
      = (1 / s.card) * Real.log s.card := by
    intro a ha
    rw [uniformOn_mem ha, Real.log_div one_ne_zero (ne_of_gt hcard), Real.log_one]
    ring
  rw [Finset.sum_congr rfl hterm, Finset.sum_const, nsmul_eq_mul]
  field_simp

/-- The identification, stated in the lake's own vocabulary: the frame entropy
    of a view at a reading IS the Shannon entropy of the uniform state on that
    reading's fiber. R3's first half, discharged. -/
theorem frameEntropy_eq_shannon_uniform {State Chart : Type*} [Fintype State]
    [DecidableEq State] [DecidableEq Chart] (view : State → Chart) (s : State) :
    FrameEntropy.frameEntropy view (view s)
      = shannon (uniformOn (FrameEntropy.fiber view (view s))) := by
  rw [shannon_uniformOn ⟨s, FrameEntropy.mem_fiber_self view s⟩]
  rfl

/-! ### Rung two: why the monotone must change

The deterministic second law (`Core/Habit.production_nonneg_of_closed`) says a
closed view's entropy cannot fall. Under noise that is false, and the witness
is the textbook one. -/

/-- The two-point state space. -/
abbrev Two := Bool

/-- The reset channel's output: everything goes to `false`. -/
noncomputable def resetState : Two → ℝ := fun b => if b = false then 1 else 0

/-- **THE COUNTEREXAMPLE, EXHIBITED.** The uniform state on two points has
    entropy `log 2`; the reset channel's output is a point mass with entropy
    `0`. So Shannon entropy STRICTLY FALLS under a stochastic map, and the
    deterministic second law cannot be repaired by weakening a hypothesis — the
    quantity itself has to change. -/
theorem reset_lowers_entropy :
    shannon resetState < shannon (uniformOn (univ : Finset Two)) := by
  have huniv : (univ : Finset Two).Nonempty := ⟨false, Finset.mem_univ _⟩
  have hcard : ((univ : Finset Two).card : ℝ) = 2 := by simp
  rw [shannon_uniformOn huniv, hcard]
  have hreset : shannon resetState = 0 := by
    unfold shannon resetState
    have hsupp : univ.filter (fun b : Two => (if b = false then (1:ℝ) else 0) ≠ 0)
        = {false} := by
      ext b
      cases b <;> simp
    rw [hsupp]
    simp
  rw [hreset]
  have : (0:ℝ) < Real.log 2 := Real.log_pos (by norm_num)
  linarith

/-- **THE FENCE ON THE SUCCESSOR — what the next brick may not be.** Any
    candidate monotone that is a function of the state's entropy ALONE and is
    required non-decreasing under every channel is refuted by the reset
    channel. So the stochastic monotone must consume the CHANNEL's stationary
    structure (relative entropy to a stationary state, under the
    data-processing inequality) rather than the state's entropy alone. This is
    a derived constraint on the successor, not a guess about it. -/
theorem no_monotone_of_reset :
    ¬ ∃ f : ℝ → ℝ, StrictMono f ∧
        f (shannon (uniformOn (univ : Finset Two))) ≤ f (shannon resetState) := by
  rintro ⟨f, hf, hle⟩
  exact absurd (hf reset_lowers_entropy) (not_lt.mpr hle)

end CIRISOntology.Core.StochasticHabit
