/-
CIRISOntology.Core.ModeChart — the mode-chart parameter, and the fence between the
cap and the Boolean.

WHY THIS EXISTS. The descriptor-chain meet review (L13) found that the exclusion
principle was being claimed by different tiers through DIFFERENT mode sets — six FHP
directions here, nuclear |nljm⟩ with degeneracy g = 4 there — with the chart
relation living in prose. Two instantiations of one principle were at risk of
being counted as one witness (the shared-lemma-one-witness trap, a paid house
lesson). This file makes the chart a Lean object:

  * `OccState M` — Boolean occupancy over an ARBITRARY finite mode set. The cap
    is enforced by type, as in `Core/Lattice.lean`, but the mode set is now a
    parameter.
  * `fhpChart` — the machine-checked identification of `Core/Lattice.lean`'s 64
    local states with `OccState (Fin 6)`: the founding object IS one chart of the
    general one, by equivalence, not by analogy.
  * `level_cap` — the g-degenerate statement: a level with internal degeneracy g
    holds at most g quanta. This is what the nuclear chart consumes; the FHP chart
    is the g = 1 case.
  * The FENCE (L10's repair, rung (iii) of the repaired meet criterion): Boolean
    occupancy is exact only for DETERMINATE states. Over mixtures the exact
    invariant is the CAP — mean occupancy in [0,1] — and a fractional mean is the
    measured face of correlation/mixture. `mean_occ_boolean_of_pure` and
    `mean_occ_le_one` state the two halves; correlated nuclear matter's ~30%
    occupation depletion is the physics this fence keeps us honest about.

SCOPE. Model bricks. The discharge of exclusion itself remains BY PAPER
(Pauli 1940) — see `Core/ExchangeSign.lean`'s header; this file supplies rungs
(iii) and (iv) of the repaired criterion: the chart identification and the
cap-not-Boolean fence. Nothing here derives physics; it stops two tiers from
double-counting one witness and stops the mean-field chart from being mistaken
for the invariant.

MEASURED COMPANION (2026-08-23, the Q-seam campaign;
`sim_engine/Q_SEAM_RESULTS.md`). The fence is now a measured number, not only a
witness: on the exact 1D Hubbard sweep, D_bool — the maximal distance of the
exact natural occupations from Boolean — reads exactly 0.000000 at U = 0 at
every chain length (where the determinantal chart is exact, as
`meanOcc_boolean_of_pure` says it must) and rises to 0.4405 at U/t = 16 (where
the chart's failure is total). `meanOcc_fractional_exists` is the model witness;
the sweep is its measured face. Same campaign, the negative kept next to the
positive: the beyond-pair share of the exact state does NOT track the chart's
error (Q6 kill fired, ρ = 0.099 against a staked 0.50, the estimator validated
by a derived plumb line) — the fence quantity D_bool tracks chart failure on
this family; the whole-only share does not. A wrongness-meter and a
beyond-pair-meter are different instruments.
-/
import CIRISOntology.Core.Lattice
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace CIRISOntology.Core.ModeChart

open Finset

/-- Boolean occupancy over an arbitrary mode set: the exclusion cap enforced by
    type, with the mode set a PARAMETER rather than a fixed six. -/
abbrev OccState (M : Type*) : Type _ := M → Bool

/-- Occupancy of one slot, as a number. At most one by type — the cap, stated
    per-slot. -/
def occNat {M : Type*} (x : OccState M) (m : M) : ℕ := if x m then 1 else 0

theorem occNat_le_one {M : Type*} (x : OccState M) (m : M) : occNat x m ≤ 1 := by
  unfold occNat; split <;> omega

/-! ### The FHP chart is one instantiation, by machine-checked equivalence -/

/-- `Core/Lattice.lean`'s 64 local states, read as occupancy states over the six
    directions. This is the CHART: the founding object as an instance of the
    parameterized one. -/
def fhpChart (s : Fin 64) : OccState (Fin 6) := fun k => Lattice.occ s k

/-- The chart is faithful: two local states agreeing in every direction are the
    same state. (Injectivity of the chart — the 64 states ARE the 2⁶ occupancy
    patterns, not merely mapped into them.) -/
theorem fhpChart_injective : Function.Injective fhpChart := by
  intro s t h
  apply Fin.ext
  apply Nat.eq_of_testBit_eq
  intro i
  by_cases hi : i < 6
  · have := congrFun h ⟨i, hi⟩
    simpa [fhpChart, Lattice.occ] using this
  · have hs := s.isLt
    have ht := t.isLt
    have hs6 : s.val < 2 ^ 6 := hs
    have ht6 : t.val < 2 ^ 6 := ht
    have h1 : Nat.testBit s.val i = false :=
      Nat.testBit_lt_two_pow (lt_of_lt_of_le hs6 (Nat.pow_le_pow_right (by omega) (by omega)))
    have h2 : Nat.testBit t.val i = false :=
      Nat.testBit_lt_two_pow (lt_of_lt_of_le ht6 (Nat.pow_le_pow_right (by omega) (by omega)))
    rw [h1, h2]

/-! ### The g-degenerate level cap -/

/-- A mode set with internal degeneracy: levels × internal slots. The nuclear
    chart (|nljm⟩ with spin–isospin g = 4) has this shape; the FHP chart is the
    degenerate case g = 1. -/
def levelOcc {L : Type*} {g : ℕ} (x : OccState (L × Fin g)) (l : L) : ℕ :=
  ∑ j : Fin g, occNat x (l, j)

/-- **THE LEVEL CAP.** A level with internal degeneracy g holds at most g quanta —
    the exclusion cap summed over the internal slots. This is the statement the
    nuclear tier consumes, and it is a THEOREM of the per-slot cap, not a new
    axiom. -/
theorem level_cap {L : Type*} {g : ℕ} (x : OccState (L × Fin g)) (l : L) :
    levelOcc x l ≤ g := by
  calc levelOcc x l ≤ ∑ _j : Fin g, 1 :=
        Finset.sum_le_sum (fun j _ => occNat_le_one x (l, j))
    _ = g := by simp

/-! ### The fence: the CAP is the invariant, the Boolean is a chart

States of knowledge are probability weights over determinate occupancy states.
The mean occupancy of a slot is then in [0,1] always — the cap survives mixing —
but it is 0-or-1 only for states that are determinate at that slot. Fractional
mean occupancy is therefore the measured face of mixture/correlation, and
Booleanity is a property of the CHART (the determinate, mean-field description),
never of the invariant. -/

variable {M : Type*} [Fintype M] [DecidableEq M]

/-- Mean occupancy of slot `m` under probability weights `p` over determinate
    states. -/
noncomputable def meanOcc (p : OccState M → ℝ) (m : M) : ℝ :=
  ∑ x : OccState M, p x * occNat x m

/-- The cap survives mixing: mean occupancy never exceeds one. (Nonnegativity of
    weights and normalization are the two hypotheses — exactly a probability.) -/
theorem meanOcc_le_one (p : OccState M → ℝ) (hp : ∀ x, 0 ≤ p x)
    (hsum : ∑ x : OccState M, p x = 1) (m : M) : meanOcc p m ≤ 1 := by
  unfold meanOcc
  calc ∑ x : OccState M, p x * occNat x m
      ≤ ∑ x : OccState M, p x * 1 := by
        apply Finset.sum_le_sum
        intro x _
        have h1 : (occNat x m : ℝ) ≤ 1 := by
          have := occNat_le_one x m
          exact_mod_cast this
        exact mul_le_mul_of_nonneg_left h1 (hp x)
    _ = 1 := by simpa using hsum

theorem meanOcc_nonneg (p : OccState M → ℝ) (hp : ∀ x, 0 ≤ p x) (m : M) :
    0 ≤ meanOcc p m := by
  unfold meanOcc
  apply Finset.sum_nonneg
  intro x _
  have h0 : (0 : ℝ) ≤ occNat x m := by unfold occNat; split <;> norm_num
  exact mul_nonneg (hp x) h0

/-- A determinate (point-mass) state has Boolean mean occupancy: the Boolean
    chart is EXACT exactly where the state is pure-determinate. -/
theorem meanOcc_boolean_of_pure (x₀ : OccState M) (m : M) :
    meanOcc (fun x => if x = x₀ then 1 else 0) m = occNat x₀ m := by
  unfold meanOcc
  rw [Finset.sum_eq_single x₀]
  · simp
  · intro b _ hb
    simp [hb]
  · intro h
    exact absurd (Finset.mem_univ x₀) h

/-- **THE FENCE, in witness form.** An even mixture of an occupied and an empty
    slot has mean occupancy strictly between the Boolean values: fractional mean
    occupancy EXISTS in the model, so Booleanity of the mean is a property of
    special states, not of the observable. (Correlated nuclear matter's ~30%
    depletion is the measured physics this brick keeps in scope.) -/
theorem meanOcc_fractional_exists [Inhabited M] :
    ∃ (p : OccState M → ℝ) (m : M),
      (∀ x, 0 ≤ p x) ∧ (∑ x : OccState M, p x = 1) ∧
      meanOcc p m ≠ 0 ∧ meanOcc p m ≠ 1 := by
  classical
  set a : OccState M := fun _ => true with ha
  set b : OccState M := fun _ => false with hb
  have hab : a ≠ b := by
    intro h
    have := congrFun h default
    simp [ha, hb] at this
  set p : OccState M → ℝ :=
    fun x => (if x = a then (1:ℝ)/2 else 0) + (if x = b then (1:ℝ)/2 else 0) with hp
  have hsum : ∑ x : OccState M, p x = 1 := by
    simp only [hp, Finset.sum_add_distrib, Finset.sum_ite_eq', Finset.mem_univ, if_true]
    norm_num
  have hmean : meanOcc p default = 1/2 := by
    unfold meanOcc
    simp only [hp, add_mul, Finset.sum_add_distrib, ite_mul, zero_mul,
      Finset.sum_ite_eq', Finset.mem_univ, if_true]
    simp [ha, hb, occNat]
  refine ⟨p, default, ?_, hsum, ?_, ?_⟩
  · intro x
    simp only [hp]
    have h1 : (0:ℝ) ≤ if x = a then (1:ℝ)/2 else 0 := by split <;> norm_num
    have h2 : (0:ℝ) ≤ if x = b then (1:ℝ)/2 else 0 := by split <;> norm_num
    exact add_nonneg h1 h2
  · rw [hmean]; norm_num
  · rw [hmean]; norm_num

end CIRISOntology.Core.ModeChart
