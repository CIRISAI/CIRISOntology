/-
CIRISOntology.Core.Third — the ruler, upgraded: a third-aware instrument, and
the exhibited state that separates it from the pairwise one.

The pairwise instrument's blindness (`Core.Coordination`) is not a fate. This
file carries the upgrade and the witness, both machine-checked:

  * `S_total` — total dependence (multi-information): the sum of the parts'
    entropies minus the joint entropy. It reads coordination at ALL orders.

  * `parity` — the simplest hidden state: three fair bits, the third the XOR
    of the first two. Any two of them are exactly independent; the three
    together are locked.

  * `pairwise_blind_to_parity` — the correlation matrix of the parity state
    is the identity, so `S_pairwise` reads exactly its floor, 0.

  * `third_sees_parity` — `S_total` reads exactly `log 2` on the same state,
    and `third_reading_positive` that this is strictly positive.

Together these discharge, inside this repository, the counterexample that the
stance's first claim stakes its kill on: a state with vanishing pairwise
structure and non-vanishing total dependence EXISTS, and the upgraded
instrument sees it.

SCOPE. This is the kernel of the upgrade, not its field deployment. The
bias-corrected, null-controlled synergy detector run against real data lives
in the predecessor record (github.com/CIRISAI/coherence-ratchet); its results
enter the stance as `measured`, never as `proved`.
-/
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.FinCases
import CIRISOntology.Core.Coordination

namespace CIRISOntology.Core

open scoped BigOperators

/-- Shannon entropy (natural log) of a finitely-supported distribution.
    Mathlib's convention `Real.log 0 = 0` makes empty outcomes contribute
    nothing, as they should. -/
noncomputable def entropy {α : Type*} [Fintype α] (p : α → ℝ) : ℝ :=
  -∑ a, p a * Real.log (p a)

/-- Total dependence (multi-information) of a joint state of three variables:
    what the parts' entropies say minus what the joint entropy says. This is
    the all-orders quantity of which `S_pairwise` reads only the second-order
    part. -/
noncomputable def S_total {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    (p : α × β × γ → ℝ) : ℝ :=
  entropy (fun a => ∑ b, ∑ c, p (a, b, c))
    + entropy (fun b => ∑ a, ∑ c, p (a, b, c))
    + entropy (fun c => ∑ a, ∑ b, p (a, b, c))
    - entropy p

/-- The parity state: three fair bits, the third the XOR of the first two.
    Each pair is exactly independent; the triple is fully locked. -/
noncomputable def parity : Bool × Bool × Bool → ℝ :=
  fun t => if t.2.2 = Bool.xor t.1 t.2.1 then 1/4 else 0

/-- ±1 encoding of a bit, so that correlations are plain expectations. -/
noncomputable def pm (b : Bool) : ℝ := if b then 1 else -1

/-- The three coordinates of the parity state as ±1 variables. -/
noncomputable def parityVar : Fin 3 → Bool × Bool × Bool → ℝ
  | 0 => fun t => pm t.1
  | 1 => fun t => pm t.2.1
  | 2 => fun t => pm t.2.2

/-- The correlation matrix of the parity state. Means are zero and variances
    one, so the raw second moments are the correlations. -/
noncomputable def parityCorr : Matrix (Fin 3) (Fin 3) ℝ :=
  Matrix.of fun i j => ∑ t, parity t * (parityVar i t * parityVar j t)

private lemma log_half : Real.log ((1:ℝ)/2) = -Real.log 2 := by
  rw [one_div, Real.log_inv]

private lemma log_quarter : Real.log ((1:ℝ)/4) = -(2 * Real.log 2) := by
  rw [one_div, show (4:ℝ) = 2 ^ 2 by norm_num, Real.log_inv, Real.log_pow]
  norm_num

private lemma entropy_uniform_bool :
    entropy (fun _ : Bool => (1:ℝ)/2) = Real.log 2 := by
  unfold entropy
  rw [Fintype.sum_bool, log_half]
  ring

private lemma entropy_parity : entropy parity = 2 * Real.log 2 := by
  unfold entropy parity
  simp only [Fintype.sum_prod_type, Fintype.sum_bool]
  norm_num [log_quarter]
  ring

private lemma parity_marg₁ :
    (fun a => ∑ b, ∑ c, parity (a, b, c)) = fun _ : Bool => (1:ℝ)/2 := by
  funext a
  cases a <;> simp [parity, Fintype.sum_bool] <;> norm_num

private lemma parity_marg₂ :
    (fun b => ∑ a, ∑ c, parity (a, b, c)) = fun _ : Bool => (1:ℝ)/2 := by
  funext b
  cases b <;> simp [parity, Fintype.sum_bool] <;> norm_num

private lemma parity_marg₃ :
    (fun c => ∑ a, ∑ b, parity (a, b, c)) = fun _ : Bool => (1:ℝ)/2 := by
  funext c
  cases c <;> simp [parity, Fintype.sum_bool] <;> norm_num

/-- The correlation matrix of the parity state is the identity: every pair of
    its variables is exactly uncorrelated. -/
theorem parity_corr_eq_one : parityCorr = (1 : Matrix (Fin 3) (Fin 3) ℝ) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [parityCorr, parityVar, parity, pm, Matrix.one_apply,
          Fintype.sum_prod_type, Fintype.sum_bool] <;>
    norm_num

/-- THE BLINDNESS, EXHIBITED. On the parity state the pairwise instrument
    reads exactly its floor. Nothing is missing from the reading that pairs
    could have shown; everything is missing that only the triple carries. -/
theorem pairwise_blind_to_parity : S_pairwise parityCorr = 0 := by
  rw [parity_corr_eq_one]
  exact S_pairwise_identity

/-- THE UPGRADE, EXHIBITED. On the same state the third-aware instrument
    reads exactly `log 2`: one full bit of coordination, all of it above
    second order. -/
theorem third_sees_parity : S_total parity = Real.log 2 := by
  unfold S_total
  rw [parity_marg₁, parity_marg₂, parity_marg₃, entropy_uniform_bool,
      entropy_parity]
  ring

/-- The third-aware reading on the parity state is strictly positive: the
    two instruments provably disagree, and the disagreement is the Third. -/
theorem third_reading_positive : 0 < S_total parity := by
  rw [third_sees_parity]
  exact Real.log_pos (by norm_num)

end CIRISOntology.Core
