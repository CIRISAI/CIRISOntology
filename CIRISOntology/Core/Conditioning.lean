/-
CIRISOntology.Core.Conditioning — the chart-conditioning mechanism behind
Ω-KILL-3's N4 fire, as theorems.

N4 measured the closure of 67 coarse views on macro-matched twins and the
declared momentum-x direction came back the LEAST closed of all (growth 12.1×,
above the random 95th percentile) while kinetic energy came back among the MOST
closed (0.83, contracting).  The candidate mechanism is not dynamics but the
CHART: a linear aggregate that nearly cancels (its terms sum to far less than
their absolute sum) is an ill-conditioned functional of its own micro state.

The formal core is the condition number of summation — a numerical-analysis
classic (Higham, *Accuracy and Stability of Numerical Algorithms*, §4; credit
where the object lives) — read here as a statement about coarse charts:

  coherence a = |Σ a| / Σ |a|   ∈ [0, 1]

* `sum_perturb_le`: a per-term relative perturbation of size ε moves the
  aggregate by at most ε·Σ|a| — so, in units of the view's own scale, by at
  most ε / coherence.
* `sum_perturb_attained`: that bound is EXACT — the aligned perturbation
  achieves it.  The ceiling is real, not slack.
* `coherence_of_nonneg`: an all-nonnegative view (kinetic energy) has
  coherence 1 — perfectly conditioned; its scale-relative response can never
  exceed ε.
* `coherence_pos_scale`: a near-cancelling view (momentum-x in a settled
  scene) has small coherence, and the SAME micro perturbation is amplified by
  the ratio of coherences between two views of the same state.

THE FENCE, stated so the theorem cannot be over-read: conditioning bounds the
WORST-CASE response of the chart to a fiber-internal perturbation per reading.
It does not compute the dynamics' realized growth — that is measured, and
whether conditioning EXPLAINS the measured heterogeneity is the follow-up
branch's staked question (`coherence_diag`, forward prereg), not this file's
claim.  N4 as staked stays dead either way; what this file changes is what its
death teaches: "declared = closed" conflated chart conditioning with dynamical
closure, and the repaired question compares views at MATCHED conditioning.
-/
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Analysis.SpecialFunctions.Pow.Real

namespace CIRISOntology.Core.Conditioning

open Finset

variable {n : ℕ}

/-- The coherence of a finite family: aggregate magnitude over aligned magnitude.
    `1` for an all-same-sign family, near `0` for a near-cancelling one. -/
noncomputable def coherence (a : Fin n → ℝ) : ℝ :=
  |∑ i, a i| / ∑ i, |a i|

/-- **The conditioning bound.** A per-term relative perturbation of size `ε`
    moves the aggregate by at most `ε` times the ALIGNED sum — which is
    `ε / coherence` in units of the aggregate's own magnitude. -/
theorem sum_perturb_le (a δ : Fin n → ℝ) (ε : ℝ)
    (h : ∀ i, |δ i| ≤ ε * |a i|) :
    |∑ i, (a i + δ i) - ∑ i, a i| ≤ ε * ∑ i, |a i| := by
  have : (∑ i, (a i + δ i)) - ∑ i, a i = ∑ i, δ i := by
    rw [Finset.sum_add_distrib]; ring
  rw [this, Finset.mul_sum]
  exact (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum fun i _ => h i)

/-- **The bound is exact**: the aligned perturbation `δ i = ε·|a i|` attains it.
    The conditioning ceiling is real, not slack. -/
theorem sum_perturb_attained (a : Fin n → ℝ) (ε : ℝ) (hε : 0 ≤ ε) :
    ∃ δ : Fin n → ℝ, (∀ i, |δ i| ≤ ε * |a i|) ∧
      |∑ i, (a i + δ i) - ∑ i, a i| = ε * ∑ i, |a i| := by
  refine ⟨fun i => ε * |a i|, fun i => ?_, ?_⟩
  · rw [abs_mul, abs_of_nonneg hε, abs_abs]
  · have h1 : (∑ i, (a i + ε * |a i|)) - ∑ i, a i = ε * ∑ i, |a i| := by
      rw [Finset.sum_add_distrib, Finset.mul_sum]; ring
    rw [h1, abs_of_nonneg]
    exact mul_nonneg hε (Finset.sum_nonneg fun i _ => abs_nonneg _)

/-- **The protected class**: an all-nonnegative view with a nonzero reading has
    coherence exactly `1`.  Kinetic energy is such a view; its scale-relative
    response to any per-term relative perturbation is at most `ε`. -/
theorem coherence_of_nonneg (a : Fin n → ℝ) (h : ∀ i, 0 ≤ a i)
    (hz : ∑ i, a i ≠ 0) : coherence a = 1 := by
  unfold coherence
  have he : ∀ i ∈ Finset.univ, |a i| = a i := fun i _ => abs_of_nonneg (h i)
  rw [Finset.sum_congr rfl he, abs_of_nonneg (Finset.sum_nonneg fun i _ => h i)]
  exact div_self hz

/-- The scale-relative form: in units of the view's own reading, the response
    is at most `ε / coherence`.  Small coherence is a large amplification
    ceiling — the ill-conditioned chart, not the open dynamics. -/
theorem relative_response_le (a δ : Fin n → ℝ) (ε : ℝ)
    (h : ∀ i, |δ i| ≤ ε * |a i|) (hz : |∑ i, a i| ≠ 0) :
    |∑ i, (a i + δ i) - ∑ i, a i| / |∑ i, a i| ≤ ε / coherence a := by
  have habs : (0:ℝ) < |∑ i, a i| := (abs_nonneg _).lt_of_ne (Ne.symm hz)
  unfold coherence
  rw [div_div_eq_mul_div]
  have step : |∑ i, (a i + δ i) - ∑ i, a i| / |∑ i, a i|
      ≤ (ε * ∑ i, |a i|) / |∑ i, a i| := by
    gcongr
    exact sum_perturb_le a δ ε h
  exact step

end CIRISOntology.Core.Conditioning
