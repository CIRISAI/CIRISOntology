/-
CIRISOntology.Core.Temporal — the Logos read through TIME: the parity pattern,
laid across three moments, is unreachable without memory — and reachable with
exactly one remembered bit.

The stance's open claim (`third-in-tsvf`) names the next formal step: define
the whole-only share of multiple-time correlation and compute one example.
This file is the machine-checked kernel of that step, in the same minimal
setting as the rest of the core (three binary readings, exact arithmetic):

  * `memoryless` — a three-step process in which each step reads only the
    immediately previous outcome: p(z₁,z₂,z₃) = init z₁ · k₁ z₁ z₂ · k₂ z₂ z₃.
    The Markov shape, with NO further hypotheses — the factors need not even
    be nonnegative or normalized, which only strengthens the theorem below.

  * `parity_needs_memory` — NO memoryless process realizes the parity
    distribution across three times. Not "is unlikely to": the factorization
    does not exist, for any real-valued factors whatsoever.

  * `withMemory` / `memory_realizes_parity` — one remembered bit suffices:
    let the last step read the FIRST outcome too, and parity is realized
    exactly, by an explicit process (fair initial coin, fresh fair second
    coin, third reading the XOR of the two it remembers), whose factors are
    checked to be honest probability kernels in `memory_realizer_is_probability`.

  * `temporal_logos_is_memory` — the assembled reading, one citable witness:
    the same distribution that `Core.Third` proves pairwise-flat and
    whole-positive is, across time, impossible without memory and exact with
    one bit of it.

Read together with `Core.Third`: every PAIR of times in the parity pattern is
exactly independent (`parity_pair_independent_*`), so every two-time reading
is flat; the whole reads log 2 (`third_sees_parity`). What this file adds is
the temporal law: that whole-only correlation across times cannot be produced
by any memoryless dynamics and is produced by remembering a single bit. The
whole-only share of a process's multi-time correlation is a MEMORY
phenomenon — the temporal face of the Logos, in its simplest case.

SCOPE. Proved here: the theorems above, exact and assumption-free. The
maximum-entropy definition of the whole-only SHARE, with the parity state's
share computed to be exactly one bit, now lives in `Core.Share`
(`share_parity`); what remains NOT mechanized anywhere is the quantum lift
(von Neumann entropy of the state-over-times, marginals by partial trace)
and any claim about which processes in NATURE carry a nonzero share. The
numerical companion — a quantum realization on a system-plus-memory-qubit
circuit, Markovian controls reading zero, a memory dial sweeping the share
from 0 to 1 — lives in the session record, not in this library.

Mathlib survey: only `mul_eq_zero`, `Fintype.sum_bool`, and finite case
analysis are needed; nothing to port.
-/
import CIRISOntology.Core.Third

namespace CIRISOntology.Core

open scoped BigOperators

/-- A memoryless (Markov) three-step process on bits: an initial weight and
    two step kernels, each step reading ONLY the immediately previous
    outcome. No positivity or normalization is assumed — the impossibility
    theorem below holds for arbitrary real factors. -/
def memoryless (init : Bool → ℝ) (k₁ k₂ : Bool → Bool → ℝ) :
    Bool × Bool × Bool → ℝ :=
  fun t => init t.1 * k₁ t.1 t.2.1 * k₂ t.2.1 t.2.2

/-- A three-step process with ONE BIT of memory: the last step may read the
    first outcome as well as the second — the minimal extension beyond
    `memoryless`. -/
def withMemory (init : Bool → ℝ) (k₁ : Bool → Bool → ℝ)
    (k₂ : Bool → Bool → Bool → ℝ) : Bool × Bool × Bool → ℝ :=
  fun t => init t.1 * k₁ t.1 t.2.1 * k₂ t.1 t.2.1 t.2.2

/-- MEMORYLESSNESS CANNOT WRITE THE TEMPORAL PARITY. No memoryless process —
    no initial weight, no step kernels, normalized or not, signed or not —
    realizes the parity distribution across three times. The proof is three
    evaluations: realizing p(000) = 1/4 forces the first two factors of
    p(001) to be nonzero, realizing p(101) = 1/4 forces its third, and then
    p(001) = 0 is a vanishing product of three nonzero reals. -/
theorem parity_needs_memory :
    ¬ ∃ (init : Bool → ℝ) (k₁ k₂ : Bool → Bool → ℝ),
        memoryless init k₁ k₂ = parity := by
  rintro ⟨init, k₁, k₂, h⟩
  have h000 : init false * k₁ false false * k₂ false false = 1/4 := by
    simpa [memoryless, parity] using congrFun h (false, false, false)
  have h101 : init true * k₁ true false * k₂ false true = 1/4 := by
    simpa [memoryless, parity] using congrFun h (true, false, true)
  have h001 : init false * k₁ false false * k₂ false true = 0 := by
    simpa [memoryless, parity] using congrFun h (false, false, true)
  rcases mul_eq_zero.mp h001 with h' | h'
  · rw [h', zero_mul] at h000
    norm_num at h000
  · rw [h', mul_zero] at h101
    norm_num at h101

/-- ONE REMEMBERED BIT SUFFICES. The explicit process — fair initial coin,
    fresh fair second coin, third reading deterministically the XOR of the
    two outcomes it remembers — realizes the parity distribution exactly. -/
theorem memory_realizes_parity :
    withMemory (fun _ => 1/2) (fun _ _ => 1/2)
      (fun a b c => if c = Bool.xor a b then 1 else 0) = parity := by
  funext t
  obtain ⟨a, b, c⟩ := t
  by_cases hc : c = Bool.xor a b
  · norm_num [withMemory, parity, hc]
  · simp [withMemory, parity, hc]

/-- The realizing process is an honest probability process, machine-checked
    rather than asserted: every factor is nonnegative, the initial weights
    sum to one, and each kernel row sums to one over its outcome. -/
theorem memory_realizer_is_probability :
    (∀ a b c : Bool, (0:ℝ) ≤ (if c = Bool.xor a b then (1:ℝ) else 0)) ∧
    (∑ _a : Bool, ((1:ℝ)/2)) = 1 ∧
    (∀ a b : Bool, (∑ c : Bool, if c = Bool.xor a b then (1:ℝ) else 0) = 1) := by
  refine ⟨?_, ?_, ?_⟩
  · intro a b c
    by_cases h : c = Bool.xor a b <;> simp [h]
  · norm_num [Fintype.sum_bool]
  · intro a b
    cases hx : Bool.xor a b <;> simp [Fintype.sum_bool, hx]

/-- THE TEMPORAL READING, ASSEMBLED — one citable witness. There is a
    three-time distribution (the parity pattern) such that: no memoryless
    process realizes it; a process remembering one bit realizes it exactly;
    and its whole reading is log 2 (its pairwise flatness is
    `parity_pair_independent_*` in `Core.Third`). In this minimal setting,
    whole-only temporal correlation and memory are the same purchase. -/
theorem temporal_logos_is_memory :
    (¬ ∃ (init : Bool → ℝ) (k₁ k₂ : Bool → Bool → ℝ),
        memoryless init k₁ k₂ = parity) ∧
    (∃ (init : Bool → ℝ) (k₁ : Bool → Bool → ℝ)
        (k₂ : Bool → Bool → Bool → ℝ), withMemory init k₁ k₂ = parity) ∧
    S_total parity = Real.log 2 :=
  ⟨parity_needs_memory, ⟨_, _, _, memory_realizes_parity⟩, third_sees_parity⟩

end CIRISOntology.Core
