/-
CIRISOntology.Core.Intensive — the intensive (per-unit) coordination spine, proved here.

The programme's dark-energy reading has two branches. The disciplined one reads the
coordination balance PER UNIT — the intensive `S/k` — and its whole force rests on a
handful of facts about the equicorrelation (Kish) model that were, until now, argued in
the predecessor record (`s_of_a.py §5`, Mehler/Oppenheim) but never machine-checked here.
This file re-proves the tractable core of that spine, in this repository, sorry-free.

THE MODEL. `equicorr k ρ` is the `k × k` correlation matrix with `1` on the diagonal and a
single shared off-diagonal correlation `ρ` — the exchangeable/equicorrelation matrix. The
instrument of `Core.Coordination`, `S_pairwise C = −ln det C`, evaluated on it is the whole
object of study.

WHAT IS PROVED HERE:

  * `equicorr_det` — the determinant identity `det = (1 + (k−1)ρ)(1−ρ)^(k−1)` (the Kish
    identity), for `ρ ≠ 1`, via the rank-one (matrix-determinant) lemma.
  * `Sfun_eq` — the resulting closed form `S = −ln(1+(k−1)ρ) − (k−1)·ln(1−ρ)` on `[0,1)`.
  * `Sfun_nonneg`, `Sfun_pos` — `S ≥ 0`, and `S > 0` once `ρ > 0` and `k ≥ 2`: the balance
    reads its floor exactly at `ρ = 0` and is strictly above it otherwise.
  * `Sfun_monotoneOn` — `S` is monotone increasing in `ρ` on `[0,1)`: the can-only-grow
    direction of the instrument as correlation rises.
  * `Sfun_antitone_of_rho_antitone` — the CAN-ONLY-SHRINK statement: along any nonincreasing
    correlation path `ρ(a)`, `S` is nonincreasing. This is the intensive branch's spine.

  * `Sfun_div_k_tendsto` — the `k → ∞` intensive limit `S/k → −ln(1−ρ)` (target 3): in the
    large-system limit the single shared correlation is the whole per-unit balance. Proved
    via the closed form, a squeeze on the `1+(k−1)ρ` factor, and `ln k/k → 0`.

SCOPE. Everything here is a theorem about the equicorrelation MODEL. Whether the cosmic
matter field is described by it is a separate, measured question (`epistemology.md §1`), and
no stance claim is promoted by this file alone — it is the named promote-path for the
intensive dark-energy reading, not a promotion of it.
-/
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.LinearAlgebra.Matrix.SchurComplement
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import CIRISOntology.Core.Coordination

namespace CIRISOntology.Core

open scoped BigOperators
open Filter

/-- The `k × k` equicorrelation (Kish) matrix: `1` on the diagonal, a single shared
    correlation `ρ` off it. The exchangeable correlation model. -/
noncomputable def equicorr (k : ℕ) (ρ : ℝ) : Matrix (Fin k) (Fin k) ℝ :=
  Matrix.of fun i j => if i = j then 1 else ρ

/-- Rank-one decomposition: away from `ρ = 1`, `equicorr` is a scalar multiple of a
    rank-one update of the identity, the form the matrix-determinant lemma consumes. -/
lemma equicorr_eq_smul (k : ℕ) (ρ : ℝ) (hρ : ρ ≠ 1) :
    equicorr k ρ =
      (1 - ρ) • ((1 : Matrix (Fin k) (Fin k) ℝ)
        + Matrix.col Unit (fun _ => ρ / (1 - ρ)) * Matrix.row Unit (fun _ => (1 : ℝ))) := by
  have h1 : (1 - ρ) ≠ 0 := sub_ne_zero.mpr fun h => hρ h.symm
  ext i j
  by_cases hij : i = j
  · subst hij
    simp only [equicorr, Matrix.of_apply, if_pos rfl, Matrix.smul_apply, Matrix.add_apply,
      Matrix.one_apply_eq, Matrix.mul_apply, Matrix.col_apply, Matrix.row_apply,
      Fintype.sum_unique, smul_eq_mul]
    field_simp
  · simp only [equicorr, Matrix.of_apply, if_neg hij, Matrix.smul_apply, Matrix.add_apply,
      Matrix.one_apply_ne hij, Matrix.mul_apply, Matrix.col_apply, Matrix.row_apply,
      Fintype.sum_unique, smul_eq_mul, zero_add]
    field_simp

/-- The determinant of the equicorrelation matrix in factored (division) form, for `ρ ≠ 1`.
    Intermediate to the Kish identity. -/
lemma equicorr_det_factored (k : ℕ) (ρ : ℝ) (hρ : ρ ≠ 1) :
    (equicorr k ρ).det = (1 - ρ) ^ k * (1 + (k : ℝ) * (ρ / (1 - ρ))) := by
  rw [equicorr_eq_smul k ρ hρ, Matrix.det_smul, Fintype.card_fin,
    Matrix.det_one_add_col_mul_row]
  congr 1
  simp [Matrix.dotProduct, Finset.sum_const, Finset.card_univ, nsmul_eq_mul]

/-- THE KISH DETERMINANT IDENTITY (target 1). For `ρ ≠ 1` and `k ≥ 1`,
    `det (equicorr k ρ) = (1 + (k−1)ρ)(1−ρ)^(k−1)`. -/
theorem equicorr_det (k : ℕ) (ρ : ℝ) (hρ : ρ ≠ 1) (hk : 1 ≤ k) :
    (equicorr k ρ).det = (1 + ((k : ℝ) - 1) * ρ) * (1 - ρ) ^ (k - 1) := by
  have h1 : (1 - ρ) ≠ 0 := sub_ne_zero.mpr fun h => hρ h.symm
  obtain ⟨m, rfl⟩ := Nat.exists_eq_add_of_le hk
  rw [equicorr_det_factored _ ρ hρ]
  have hcast : ((1 + m : ℕ) : ℝ) = 1 + (m : ℝ) := by push_cast; ring
  rw [hcast, show 1 + m - 1 = m by omega, pow_add, pow_one]
  field_simp
  ring

/-! ## The instrument on the model, and its floor -/

/-- The pairwise instrument `S = −ln det C` on the equicorrelation model, as a function of
    `(k, ρ)`. This is the intensive-branch object. -/
noncomputable def Sfun (k : ℕ) (ρ : ℝ) : ℝ := S_pairwise (equicorr k ρ)

/-- On `[0,1)` the model determinant is strictly positive, so `ln` and the instrument are
    well-behaved. -/
lemma equicorr_det_pos (k : ℕ) (ρ : ℝ) (h0 : 0 ≤ ρ) (h1 : ρ < 1) :
    0 < (equicorr k ρ).det := by
  have ht : (0 : ℝ) < 1 - ρ := by linarith
  rw [equicorr_det_factored k ρ (ne_of_lt h1)]
  have hfrac : 0 ≤ ρ / (1 - ρ) := div_nonneg h0 (le_of_lt ht)
  have h3 : 0 < (1 - ρ) ^ k := pow_pos ht k
  have h2 : 0 < 1 + (k : ℝ) * (ρ / (1 - ρ)) := by positivity
  exact mul_pos h3 h2

/-- THE CLOSED FORM (target 2 scaffold). On `[0,1)` with `k ≥ 1`,
    `S = −ln(1+(k−1)ρ) − (k−1)·ln(1−ρ)`. -/
theorem Sfun_eq (k : ℕ) (ρ : ℝ) (h0 : 0 ≤ ρ) (h1 : ρ < 1) (hk : 1 ≤ k) :
    Sfun k ρ = -Real.log (1 + ((k : ℝ) - 1) * ρ) - ((k : ℝ) - 1) * Real.log (1 - ρ) := by
  have ht : (0 : ℝ) < 1 - ρ := by linarith
  have hlin : 0 < 1 + ((k : ℝ) - 1) * ρ := by
    have hkpos : (0 : ℝ) ≤ (k : ℝ) - 1 := by
      have : (1 : ℝ) ≤ (k : ℝ) := by exact_mod_cast hk
      linarith
    positivity
  unfold Sfun S_pairwise
  rw [equicorr_det k ρ (ne_of_lt h1) hk, Real.log_mul (ne_of_gt hlin) (pow_ne_zero _ (ne_of_gt ht)),
    Real.log_pow, Nat.cast_sub hk, Nat.cast_one]
  ring

/-- `S ≥ 0` on `[0,1)`: the balance is at or above its floor. Proof by the tangent bound
    `ln x ≤ x − 1`, applied to each factor of the determinant. -/
theorem Sfun_nonneg (k : ℕ) (ρ : ℝ) (h0 : 0 ≤ ρ) (h1 : ρ < 1) : 0 ≤ Sfun k ρ := by
  rcases Nat.eq_zero_or_pos k with hk | hk
  · subst hk
    simp [Sfun, S_pairwise, equicorr, Matrix.det_fin_zero]
  · have ht : (0 : ℝ) < 1 - ρ := by linarith
    have hkR : (1 : ℝ) ≤ (k : ℝ) := by exact_mod_cast hk
    have hlin : 0 < 1 + ((k : ℝ) - 1) * ρ := by nlinarith [mul_nonneg (by linarith : (0:ℝ) ≤ (k:ℝ)-1) h0]
    rw [Sfun_eq k ρ h0 h1 hk]
    have hb1 : Real.log (1 + ((k : ℝ) - 1) * ρ) ≤ ((k : ℝ) - 1) * ρ := by
      have := Real.log_le_sub_one_of_pos hlin; linarith
    have hb2 : Real.log (1 - ρ) ≤ -ρ := by
      have := Real.log_le_sub_one_of_pos ht; linarith
    have hcoef : (0 : ℝ) ≤ (k : ℝ) - 1 := by linarith
    nlinarith [mul_le_mul_of_nonneg_left hb2 hcoef]

/-- `S > 0` once `ρ > 0` and `k ≥ 2`: strictly above the floor. With the floor value
    `Sfun k 0 = 0` (below), this is the "equality iff ρ = 0" content of target 2. -/
theorem Sfun_pos (k : ℕ) (ρ : ℝ) (h0 : 0 < ρ) (h1 : ρ < 1) (hk : 2 ≤ k) : 0 < Sfun k ρ := by
  have hk1 : 1 ≤ k := le_trans (by norm_num) hk
  have ht : (0 : ℝ) < 1 - ρ := by linarith
  have hkR : (2 : ℝ) ≤ (k : ℝ) := by exact_mod_cast hk
  have hcoef : (1 : ℝ) ≤ (k : ℝ) - 1 := by linarith
  have hlin : 0 < 1 + ((k : ℝ) - 1) * ρ := by nlinarith
  rw [Sfun_eq k ρ (le_of_lt h0) h1 hk1]
  have hb1 : Real.log (1 + ((k : ℝ) - 1) * ρ) ≤ ((k : ℝ) - 1) * ρ := by
    have := Real.log_le_sub_one_of_pos hlin; linarith
  have hb2 : Real.log (1 - ρ) < -ρ := by
    have := Real.log_lt_sub_one_of_pos ht (by intro h; nlinarith [h]); linarith
  nlinarith [mul_lt_mul_of_pos_left hb2 (by linarith : (0:ℝ) < (k:ℝ) - 1)]

/-- The floor value: at zero correlation the instrument reads exactly its floor. -/
@[simp] theorem Sfun_zero (k : ℕ) : Sfun k 0 = 0 := by
  unfold Sfun S_pairwise equicorr
  have : (Matrix.of fun i j : Fin k => if i = j then (1 : ℝ) else 0)
      = (1 : Matrix (Fin k) (Fin k) ℝ) := by
    ext i j; by_cases h : i = j <;> simp [Matrix.one_apply, h]
  rw [this, Matrix.det_one, Real.log_one, neg_zero]

/-! ## Monotonicity in ρ, and the can-only-shrink statement -/

/-- The closed form of the instrument as a function on all of `ℝ`, used to carry the
    calculus. It agrees with `Sfun k` on `[0,1)` for `k ≥ 1` (`Sfun_eq`). -/
noncomputable def Sclosed (k : ℕ) (ρ : ℝ) : ℝ :=
  -Real.log (1 + ((k : ℝ) - 1) * ρ) - ((k : ℝ) - 1) * Real.log (1 - ρ)

/-- The derivative of the closed form on the open interval, in reduced form. -/
lemma Sclosed_hasDerivAt (k : ℕ) (x : ℝ) (hx0 : 0 < 1 + ((k : ℝ) - 1) * x) (hx1 : 0 < 1 - x) :
    HasDerivAt (Sclosed k)
      (((k : ℝ) - 1) / (1 - x) - ((k : ℝ) - 1) / (1 + ((k : ℝ) - 1) * x)) x := by
  have d1 : HasDerivAt (fun ρ => 1 + ((k : ℝ) - 1) * ρ) ((k : ℝ) - 1) x := by
    simpa using ((hasDerivAt_id x).const_mul ((k : ℝ) - 1)).const_add 1
  have d3 : HasDerivAt (fun ρ => 1 - ρ) (-1 : ℝ) x := by
    simpa using (hasDerivAt_id x).const_sub 1
  have d2 : HasDerivAt (fun ρ => Real.log (1 + ((k : ℝ) - 1) * ρ))
      (((k : ℝ) - 1) / (1 + ((k : ℝ) - 1) * x)) x := d1.log (ne_of_gt hx0)
  have d4 : HasDerivAt (fun ρ => Real.log (1 - ρ)) ((-1) / (1 - x)) x := d3.log (ne_of_gt hx1)
  have hval : ((k : ℝ) - 1) / (1 - x) - ((k : ℝ) - 1) / (1 + ((k : ℝ) - 1) * x)
      = -(((k : ℝ) - 1) / (1 + ((k : ℝ) - 1) * x)) - ((k : ℝ) - 1) * ((-1) / (1 - x)) := by
    ring
  rw [hval]
  exact (d2.neg).sub (d4.const_mul ((k : ℝ) - 1))

/-- `S` (closed form) is monotone increasing in `ρ` on `[0,1)`: as pairwise correlation
    rises, the pairwise instrument rises. Proof: the derivative is nonnegative. -/
lemma Sclosed_monotoneOn (k : ℕ) (hk : 1 ≤ k) :
    MonotoneOn (Sclosed k) (Set.Ico (0 : ℝ) 1) := by
  have hc : (0 : ℝ) ≤ (k : ℝ) - 1 := by
    have : (1 : ℝ) ≤ (k : ℝ) := by exact_mod_cast hk
    linarith
  have hcont : ContinuousOn (Sclosed k) (Set.Ico (0 : ℝ) 1) := by
    apply ContinuousOn.sub
    · refine (ContinuousOn.log ?_ ?_).neg
      · exact continuousOn_const.add (continuousOn_const.mul continuousOn_id)
      · intro x hx
        have : 0 < 1 + ((k : ℝ) - 1) * x := by nlinarith [hx.1, hx.2, mul_nonneg hc hx.1]
        exact ne_of_gt this
    · refine continuousOn_const.mul (ContinuousOn.log ?_ ?_)
      · exact continuousOn_const.sub continuousOn_id
      · intro x hx; exact ne_of_gt (by linarith [hx.2])
  apply monotoneOn_of_hasDerivWithinAt_nonneg (convex_Ico 0 1) hcont
    (f' := fun x => ((k : ℝ) - 1) / (1 - x) - ((k : ℝ) - 1) / (1 + ((k : ℝ) - 1) * x))
  · intro x hx
    rw [interior_Ico] at hx
    obtain ⟨hx0', hx1'⟩ := hx
    have hx0 : 0 < 1 + ((k : ℝ) - 1) * x := by nlinarith [mul_nonneg hc (le_of_lt hx0')]
    have hx1 : 0 < 1 - x := by linarith
    exact (Sclosed_hasDerivAt k x hx0 hx1).hasDerivWithinAt
  · intro x hx
    rw [interior_Ico] at hx
    obtain ⟨hx0', hx1'⟩ := hx
    have hx0 : 0 < 1 + ((k : ℝ) - 1) * x := by nlinarith [mul_nonneg hc (le_of_lt hx0')]
    have hx1 : 0 < 1 - x := by linarith
    rw [div_sub_div _ _ (ne_of_gt hx1) (ne_of_gt hx0)]
    apply div_nonneg
    · nlinarith [mul_nonneg hc (mul_nonneg (Nat.cast_nonneg k) (le_of_lt hx0'))]
    · exact le_of_lt (mul_pos hx1 hx0)

/-- MONOTONE IN ρ (target 2). On `[0,1)` with `k ≥ 1`, the instrument `Sfun k` is monotone
    increasing in the correlation `ρ`. -/
theorem Sfun_monotoneOn (k : ℕ) (hk : 1 ≤ k) : MonotoneOn (Sfun k) (Set.Ico (0 : ℝ) 1) := by
  have hcong : Set.EqOn (Sclosed k) (Sfun k) (Set.Ico (0 : ℝ) 1) := by
    intro ρ hρ; rw [Sfun_eq k ρ hρ.1 hρ.2 hk]; rfl
  exact (Sclosed_monotoneOn k hk).congr hcong

/-- CAN ONLY SHRINK (target 4). Along ANY nonincreasing correlation path `ρ(a)` valued in
    `[0,1)`, the intensive instrument `S(ρ(a))` is nonincreasing. This is the intensive
    branch's spine: with `ρ` falling, `S` can only fall. -/
theorem Sfun_antitone_of_rho_antitone (k : ℕ) (hk : 1 ≤ k) (ρ : ℝ → ℝ)
    (hmem : ∀ a, ρ a ∈ Set.Ico (0 : ℝ) 1) (hanti : Antitone ρ) :
    Antitone (fun a => Sfun k (ρ a)) :=
  fun _ _ hab => Sfun_monotoneOn k hk (hmem _) (hmem _) (hanti hab)

/-! ## The intensive limit (target 3): `S/k → −ln(1−ρ)` as `k → ∞`

The per-unit reading of the instrument. From `Sfun_eq`,
`S/k = −ln(1+(k−1)ρ)/k − ((k−1)/k)·ln(1−ρ)`; the second term tends to `−ln(1−ρ)`
(since `(k−1)/k → 1`) and the first is squeezed to `0` by
`0 ≤ ln(1+(k−1)ρ) ≤ ln k + ln(1+ρ)` (from `1+(k−1)ρ ≤ k(1+ρ)`) with `ln k/k → 0`. -/

/-- `ln k / k → 0`: the little-o of `log` against the identity (`isLittleO_log_id_atTop`),
    pulled back along the coercion `ℕ → ℝ`. -/
private lemma tendsto_log_natCast_div_atTop :
    Tendsto (fun k : ℕ => Real.log k / (k : ℝ)) atTop (nhds 0) := by
  have h : Tendsto (fun x : ℝ => Real.log x / x) atTop (nhds 0) := by
    simpa using Real.isLittleO_log_id_atTop.tendsto_div_nhds_zero
  exact h.comp (tendsto_natCast_atTop_atTop (R := ℝ))

/-- The determinant's `1+(k−1)ρ` factor contributes nothing per unit:
    `ln(1+(k−1)ρ)/k → 0`. Squeezed between `0` and `ln k/k + ln(1+ρ)/k`. -/
private lemma tendsto_logFirst_div (ρ : ℝ) (h0 : 0 ≤ ρ) :
    Tendsto (fun k : ℕ => Real.log (1 + ((k : ℝ) - 1) * ρ) / (k : ℝ)) atTop (nhds 0) := by
  have hup : Tendsto (fun k : ℕ => Real.log k / (k : ℝ) + Real.log (1 + ρ) / (k : ℝ))
      atTop (nhds 0) := by
    simpa using tendsto_log_natCast_div_atTop.add
      (tendsto_const_div_atTop_nhds_zero_nat (Real.log (1 + ρ)))
  refine tendsto_of_tendsto_of_tendsto_of_le_of_le' tendsto_const_nhds hup ?_ ?_
  · filter_upwards [eventually_ge_atTop 1] with k hk
    have hkR : (1 : ℝ) ≤ (k : ℝ) := by exact_mod_cast hk
    have hpos : 0 < (k : ℝ) := by linarith
    have hnum : 0 ≤ Real.log (1 + ((k : ℝ) - 1) * ρ) :=
      Real.log_nonneg (by nlinarith [mul_nonneg (by linarith : (0 : ℝ) ≤ (k : ℝ) - 1) h0])
    exact div_nonneg hnum hpos.le
  · filter_upwards [eventually_ge_atTop 1] with k hk
    have hkR : (1 : ℝ) ≤ (k : ℝ) := by exact_mod_cast hk
    have hpos : 0 < (k : ℝ) := by linarith
    have hρ1 : (0 : ℝ) < 1 + ρ := by linarith
    have hprod : (0 : ℝ) ≤ ((k : ℝ) - 1) * ρ := mul_nonneg (by linarith) h0
    have hbpos : 0 < 1 + ((k : ℝ) - 1) * ρ := by linarith
    have hle : 1 + ((k : ℝ) - 1) * ρ ≤ (k : ℝ) * (1 + ρ) := by nlinarith
    have hlog_le : Real.log (1 + ((k : ℝ) - 1) * ρ) ≤ Real.log ((k : ℝ) * (1 + ρ)) :=
      Real.log_le_log hbpos hle
    rw [Real.log_mul (ne_of_gt hpos) (ne_of_gt hρ1)] at hlog_le
    calc Real.log (1 + ((k : ℝ) - 1) * ρ) / (k : ℝ)
        ≤ (Real.log k + Real.log (1 + ρ)) / (k : ℝ) := (div_le_div_iff_of_pos_right hpos).mpr hlog_le
      _ = Real.log k / (k : ℝ) + Real.log (1 + ρ) / (k : ℝ) := add_div _ _ _

/-- THE INTENSIVE LIMIT (target 3). For fixed `ρ ∈ [0,1)`, the per-unit instrument `S/k`
    converges to `−ln(1−ρ)` as the number of units `k → ∞`. This is the intensive
    coordination density: in the large-system limit the single shared correlation is
    the whole per-unit balance, at rate `−ln(1−ρ)`. It completes the intensive spine.
    Proof: `Sfun_eq` gives `S/k = −ln(1+(k−1)ρ)/k − ((k−1)/k)·ln(1−ρ)`; the first term is
    squeezed to `0` (`tendsto_logFirst_div`), the coefficient `(k−1)/k → 1`. -/
theorem Sfun_div_k_tendsto (ρ : ℝ) (h0 : 0 ≤ ρ) (h1 : ρ < 1) :
    Tendsto (fun k : ℕ => Sfun k ρ / (k : ℝ)) atTop (nhds (-Real.log (1 - ρ))) := by
  have hinv : Tendsto (fun k : ℕ => ((k : ℝ))⁻¹) atTop (nhds 0) :=
    (tendsto_natCast_atTop_atTop (R := ℝ)).inv_tendsto_atTop
  have hR : Tendsto (fun k : ℕ => ((k : ℝ) - 1) / (k : ℝ)) atTop (nhds 1) := by
    refine Tendsto.congr' ?_ (by simpa using tendsto_const_nhds.sub hinv)
    filter_upwards [eventually_ge_atTop 1] with k hk
    have hk0 : (k : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr (by omega)
    rw [sub_div, div_self hk0, one_div]
  have hD : Tendsto (fun k : ℕ => -(Real.log (1 + ((k : ℝ) - 1) * ρ) / (k : ℝ))
      - (((k : ℝ) - 1) / (k : ℝ)) * Real.log (1 - ρ)) atTop (nhds (-Real.log (1 - ρ))) := by
    have := (tendsto_logFirst_div ρ h0).neg.sub (hR.mul_const (Real.log (1 - ρ)))
    simpa using this
  refine Tendsto.congr' ?_ hD
  filter_upwards [eventually_ge_atTop 1] with k hk
  rw [Sfun_eq k ρ h0 h1 hk]
  ring

end CIRISOntology.Core
