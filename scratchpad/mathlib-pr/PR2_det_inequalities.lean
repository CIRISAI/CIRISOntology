/-
PR 2 — Determinant inequalities for positive (semi)definite matrices.

Target file: `Mathlib/LinearAlgebra/Matrix/PosDef.lean`, in the `Det` /
`ComplexOrder` region alongside `PosDef.det_pos` (which these mirror and extend).
Requires `import Mathlib.LinearAlgebra.Matrix.SchurComplement` for the matrix
determinant lemma `det_add_mul` (already imported transitively in many callers;
add explicitly if needed).

Contents (five results, all over `RCLike 𝕜` with `open scoped ComplexOrder`,
matching the existing `PosDef.det_pos`):
  * `PosSemidef.det_nonneg`          — `0 ≤ det X`
  * `PosSemidef.posDef_of_isUnit_det` — PSD + unit determinant ⇒ PosDef
  * `PosSemidef.one_le_det_one_add`  — `1 ≤ det (1 + Q)`
  * `PosDef.det_le_det_add`          — `det X ≤ det (X + P)` (X PosDef, P PSD)
  * `PosSemidef.det_le_det_add`      — `det X ≤ det (X + P)` (both PSD)

Provenance: standard facts; e.g. Horn & Johnson, *Matrix Analysis*, Corollary
7.8.2 (determinant monotonicity: `A ≼ B ⇒ det A ≤ det B` on the PSD cone) and
Theorem 7.2.1 ff. `one_le_det_one_add` is the special case `det(I + Q) ≥ 1`.

VERIFIED: compiles sorry-free on Mathlib v4.14; standard axioms only (see
#print axioms). Adapt to current master before opening the PR.
-/
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.LinearAlgebra.Matrix.Spectrum
import Mathlib.LinearAlgebra.Matrix.SchurComplement

open scoped ComplexOrder Matrix

namespace Matrix

variable {𝕜 : Type*} [RCLike 𝕜] {n : Type*} [Fintype n] [DecidableEq n]

/-- The determinant of a positive semidefinite matrix is nonnegative. -/
theorem PosSemidef.det_nonneg {X : Matrix n n 𝕜} (hX : X.PosSemidef) : 0 ≤ X.det := by
  rw [hX.1.det_eq_prod_eigenvalues, ← RCLike.ofReal_prod, RCLike.ofReal_nonneg]
  exact Finset.prod_nonneg (fun i _ => hX.eigenvalues_nonneg i)

/-- A positive semidefinite matrix with a unit determinant is positive definite. -/
theorem PosSemidef.posDef_of_isUnit_det {A : Matrix n n 𝕜}
    (hA : A.PosSemidef) (hdet : IsUnit A.det) : A.PosDef := by
  have hAinv : IsUnit A := (isUnit_iff_isUnit_det A).2 hdet
  have hinj : Function.Injective A.mulVec := mulVec_injective_iff_isUnit.mpr hAinv
  refine ⟨hA.1, fun x hx => ?_⟩
  have hAx : A *ᵥ x ≠ 0 := fun h => hx (hinj (by rw [h, mulVec_zero]))
  have hne : star x ⬝ᵥ A *ᵥ x ≠ 0 := by rw [Ne, hA.dotProduct_mulVec_zero_iff]; exact hAx
  exact lt_of_le_of_ne (hA.2 x) (Ne.symm hne)

/-- `1 ≤ det (1 + Q)` for a positive semidefinite `Q`: the eigenvalues of `1 + Q`
are the `1 + λᵢ ≥ 1`, so their product is `≥ 1`. -/
theorem PosSemidef.one_le_det_one_add {Q : Matrix n n 𝕜} (hQ : Q.PosSemidef) :
    1 ≤ (1 + Q).det := by
  set U : Matrix n n 𝕜 := (hQ.1.eigenvectorUnitary : Matrix n n 𝕜) with hUdef
  set D : Matrix n n 𝕜 := diagonal (RCLike.ofReal ∘ hQ.1.eigenvalues) with hDdef
  have hUV : U * star U = 1 := (mem_unitaryGroup_iff).mp (hQ.1.eigenvectorUnitary).2
  have hQspec : Q = U * D * star U := hQ.1.spectral_theorem
  have key : (1 : Matrix n n 𝕜) + Q = U * (1 + D) * star U := by
    rw [mul_add, add_mul, mul_one, hUV, hQspec]
  have hdiag : (1 : Matrix n n 𝕜) + D
      = diagonal (fun i => 1 + RCLike.ofReal (hQ.1.eigenvalues i)) := by
    ext i j
    rcases eq_or_ne i j with h | h
    · subst h
      simp [hDdef, add_apply, one_apply_eq, diagonal_apply_eq, Function.comp_apply]
    · simp [hDdef, add_apply, one_apply_ne h, diagonal_apply_ne _ h]
  have huu : U.det * (star U).det = 1 := by rw [← det_mul, hUV, det_one]
  rw [key, det_mul, det_mul, hdiag, det_diagonal, mul_right_comm, huu, one_mul]
  have hcast : (∏ i, (1 + RCLike.ofReal (hQ.1.eigenvalues i)) : 𝕜)
      = ((∏ i, (1 + hQ.1.eigenvalues i) : ℝ) : 𝕜) := by
    rw [RCLike.ofReal_prod]
    exact Finset.prod_congr rfl (fun i _ => by rw [RCLike.ofReal_add, RCLike.ofReal_one])
  rw [hcast, ← RCLike.ofReal_one, RCLike.ofReal_le_ofReal]
  have hle := Finset.prod_le_prod (s := (Finset.univ : Finset n))
    (f := fun _ => (1 : ℝ)) (g := fun i => 1 + hQ.1.eigenvalues i)
    (fun i _ => zero_le_one)
    (fun i _ => le_add_of_nonneg_right (hQ.eigenvalues_nonneg i))
  simpa using hle

/-- **Determinant monotonicity on the positive definite cone**: `det X ≤ det (X + P)`
for `X` positive definite and `P` positive semidefinite. Via the matrix determinant
lemma applied to the Gram factor `P = MᴴM`. -/
theorem PosDef.det_le_det_add {X P : Matrix n n 𝕜}
    (hX : X.PosDef) (hP : P.PosSemidef) : X.det ≤ (X + P).det := by
  obtain ⟨M, hM⟩ := posSemidef_iff_eq_transpose_mul_self.mp hP
  have hunit : IsUnit X.det := hX.det_pos.ne'.isUnit
  have hPSD : (M * X⁻¹ * Mᴴ).PosSemidef := hX.inv.posSemidef.mul_mul_conjTranspose_same M
  have hfac : (X + P).det = X.det * (1 + M * X⁻¹ * Mᴴ).det := by
    rw [hM, det_add_mul _ _ hunit]
  rw [hfac]
  have h1 : 1 ≤ (1 + M * X⁻¹ * Mᴴ).det := hPSD.one_le_det_one_add
  calc X.det = X.det * 1 := (mul_one _).symm
    _ ≤ X.det * (1 + M * X⁻¹ * Mᴴ).det := mul_le_mul_of_nonneg_left h1 hX.det_pos.le

/-- **Determinant monotonicity on the whole PSD cone**: `det X ≤ det (X + P)` for
`X` and `P` both positive semidefinite. -/
theorem PosSemidef.det_le_det_add {X P : Matrix n n 𝕜}
    (hX : X.PosSemidef) (hP : P.PosSemidef) : X.det ≤ (X + P).det := by
  by_cases h : IsUnit X.det
  · exact (hX.posDef_of_isUnit_det h).det_le_det_add hP
  · have hX0 : X.det = 0 := not_not.mp (isUnit_iff_ne_zero.not.mp h)
    rw [hX0]; exact (hX.add hP).det_nonneg

end Matrix

#print axioms Matrix.PosSemidef.det_nonneg
#print axioms Matrix.PosSemidef.posDef_of_isUnit_det
#print axioms Matrix.PosSemidef.one_le_det_one_add
#print axioms Matrix.PosDef.det_le_det_add
#print axioms Matrix.PosSemidef.det_le_det_add
