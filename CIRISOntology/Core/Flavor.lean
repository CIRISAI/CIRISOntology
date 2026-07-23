/-
CIRISOntology.Core.Flavor — the Jarlskog CP-violation cap (pure trigonometry).

The Jarlskog invariant `J` is the reparametrization-invariant measure of CP
violation (T-symmetry breaking) in a `3×3` mixing matrix. In the standard
parametrization `J = c₁₂ s₁₂ c₂₃ s₂₃ c₁₃² s₁₃ sin δ` (`cᵢⱼ = cos θᵢⱼ`,
`sᵢⱼ = sin θᵢⱼ`). This file proves, at Lean strength:

  * `abs_jarlskog_le_max` — `|J| ≤ J_max(angles)` on the physical octant `[0,π/2]³`,
    where `J_max` is the same product with `|sin δ|` dropped: the CP-violation
    magnitude is capped by the mixing-angle envelope, saturated only at maximal
    phase `|sin δ| = 1`;
  * `jarlskogMax_zero_at_no_mixing` — `J_max = 0` when any angle `θᵢⱼ = 0` (the
    aligned / no-mixing pole);
  * `jarlskogMax_zero_at_max_13mixing` — `J_max = 0` at `θ₁₃ = π/2` (the opposite,
    maximal-1–3-mixing endpoint), so CP violation vanishes at BOTH ends of the range.

Ported verbatim from the predecessor's machine-checked K4 bound
(`coherence-ratchet/…/Core/FourLaws.lean`); Mathlib real-trigonometry only.

SCOPE (load-bearing). This file proves ONLY the angle-envelope cap and the
pole-vanishing — pure trigonometry. It does NOT import the copula machinery and
does NOT prove the copula-multi-information ensemble law (that the aligned pole is
the comonotone / high-coordination pole, and that coordination and `|J|` are
anti-correlated across the Haar ensemble). That bridge is MEASURED, not proved,
and belongs to the `flavor-two-books` claim, not here.
-/
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

namespace CIRISOntology.Core

open Real

/-- The Jarlskog invariant in the standard parametrization. -/
noncomputable def jarlskog (θ12 θ23 θ13 δ : ℝ) : ℝ :=
  cos θ12 * sin θ12 * cos θ23 * sin θ23 * (cos θ13) ^ 2 * sin θ13 * sin δ

/-- The angle-only Jarlskog magnitude bound (the `|sin δ| ≤ 1` envelope). -/
noncomputable def jarlskogMax (θ12 θ23 θ13 : ℝ) : ℝ :=
  cos θ12 * sin θ12 * cos θ23 * sin θ23 * (cos θ13) ^ 2 * sin θ13

/-- `J_max ≥ 0` on the physical octant `[0, π/2]³`: a product of nonnegative sines
    and cosines. -/
theorem jarlskogMax_nonneg {θ12 θ23 θ13 : ℝ}
    (h12 : θ12 ∈ Set.Icc 0 (π / 2)) (h23 : θ23 ∈ Set.Icc 0 (π / 2))
    (h13 : θ13 ∈ Set.Icc 0 (π / 2)) : 0 ≤ jarlskogMax θ12 θ23 θ13 := by
  have hpi : (0 : ℝ) ≤ π / 2 := by positivity
  have hc12 : 0 ≤ cos θ12 := cos_nonneg_of_mem_Icc ⟨by linarith [h12.1], h12.2⟩
  have hs12 : 0 ≤ sin θ12 := sin_nonneg_of_mem_Icc ⟨h12.1, by linarith [h12.2, pi_pos]⟩
  have hc23 : 0 ≤ cos θ23 := cos_nonneg_of_mem_Icc ⟨by linarith [h23.1], h23.2⟩
  have hs23 : 0 ≤ sin θ23 := sin_nonneg_of_mem_Icc ⟨h23.1, by linarith [h23.2, pi_pos]⟩
  have hc13 : 0 ≤ cos θ13 := cos_nonneg_of_mem_Icc ⟨by linarith [h13.1], h13.2⟩
  have hs13 : 0 ≤ sin θ13 := sin_nonneg_of_mem_Icc ⟨h13.1, by linarith [h13.2, pi_pos]⟩
  unfold jarlskogMax
  have hc13sq : 0 ≤ (cos θ13) ^ 2 := sq_nonneg _
  positivity

/-- **THE JARLSKOG BOUND.** `|J| ≤ J_max(angles)` on the physical octant: the
    CP-violation magnitude is bounded by the mixing-angle envelope, saturated only
    at maximal CP phase `|sin δ| = 1`. Proof: `|J| = J_max · |sin δ|` and
    `|sin δ| ≤ 1` with `J_max ≥ 0`. -/
theorem abs_jarlskog_le_max {θ12 θ23 θ13 δ : ℝ}
    (h12 : θ12 ∈ Set.Icc 0 (π / 2)) (h23 : θ23 ∈ Set.Icc 0 (π / 2))
    (h13 : θ13 ∈ Set.Icc 0 (π / 2)) :
    |jarlskog θ12 θ23 θ13 δ| ≤ jarlskogMax θ12 θ23 θ13 := by
  have hmax : 0 ≤ jarlskogMax θ12 θ23 θ13 := jarlskogMax_nonneg h12 h23 h13
  have hfactor : jarlskog θ12 θ23 θ13 δ = jarlskogMax θ12 θ23 θ13 * sin δ := by
    unfold jarlskog jarlskogMax; ring
  rw [hfactor, abs_mul, abs_of_nonneg hmax]
  calc jarlskogMax θ12 θ23 θ13 * |sin δ|
      ≤ jarlskogMax θ12 θ23 θ13 * 1 :=
        mul_le_mul_of_nonneg_left (abs_sin_le_one δ) hmax
    _ = jarlskogMax θ12 θ23 θ13 := by ring

/-- **THE ALIGNED POLE.** `J_max = 0` whenever any mixing angle vanishes
    (`θᵢⱼ = 0 ⇒ sin θᵢⱼ = 0`): at the no-mixing / rigid-alignment pole the CP
    violation is forced to zero. -/
theorem jarlskogMax_zero_at_no_mixing (θ12 θ23 θ13 : ℝ)
    (h : θ12 = 0 ∨ θ23 = 0 ∨ θ13 = 0) : jarlskogMax θ12 θ23 θ13 = 0 := by
  unfold jarlskogMax
  rcases h with h | h | h <;> subst h <;> simp

/-- **THE MAXIMAL-MIXING ENDPOINT.** At `θ₁₃ = π/2`, `cos θ₁₃ = 0`, so `J_max = 0`.
    Together with `jarlskogMax_zero_at_no_mixing`, CP violation vanishes at BOTH
    ends of each mixing angle's range — it lives only strictly between the poles. -/
theorem jarlskogMax_zero_at_max_13mixing (θ12 θ23 : ℝ) :
    jarlskogMax θ12 θ23 (π / 2) = 0 := by
  unfold jarlskogMax
  rw [cos_pi_div_two]; ring

end CIRISOntology.Core
