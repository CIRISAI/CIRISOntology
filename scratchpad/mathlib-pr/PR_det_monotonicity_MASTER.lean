/-
Determinant monotonicity on the PSD cone + `1 ≤ det(1+Q)`.

VERIFIED AGAINST MATHLIB MASTER @ bbc4475e9e8fd25fbc8e26d636dd8b37be8f105a
(toolchain leanprover/lean4:v4.33.0-rc1). Compiles sorry-free, standard axioms
[propext, Classical.choice, Quot.sound].

These are the GENUINELY-NEW results after checking master: Mathlib already has the
Schur product theorem (`Matrix.PosSemidef.hadamard`), `PosSemidef.det_nonneg`, and
the PSD→PosDef bridge (`posDef_iff_det_ne_zero` / `posDef_iff_isUnit`) — see
MASTER_FINDINGS.md. What remains missing is `1 ≤ det(1+Q)` and determinant
monotonicity on the PSD / Löwner cone.

Target file: `Mathlib/Analysis/Matrix/Order.lean` (where the Löwner order, det_nonneg
and the Schur product theorem now live in master), or `Mathlib/Analysis/Matrix/PosDef.lean`.

Provenance: Horn & Johnson, *Matrix Analysis*, §7.8 — determinant monotonicity on
the positive semidefinite cone (`A ≼ B ⇒ det A ≤ det B`); `one_le_det_one_add` is
the `det(I+Q) ≥ 1` special case.

Master-API notes (renames from our v4.14 originals):
  * `Mathlib.Data.Matrix.Hadamard`  → `Mathlib.LinearAlgebra.Matrix.Hadamard`
  * `Mathlib.LinearAlgebra.Matrix.Spectrum` / `.PosDef` (spectral half)
        → `Mathlib.Analysis.Matrix.Spectrum` / `Mathlib.Analysis.Matrix.PosDef`
  * `posSemidef_iff_eq_transpose_mul_self` REMOVED; use
        `CStarAlgebra.nonneg_iff_eq_star_mul_self.mp hP.nonneg` + `star_eq_conjTranspose`.
  * the Löwner order and `Matrix.PosSemidef` CStarAlgebra instance are scoped:
        `open scoped MatrixOrder Matrix.Norms.L2Operator`.
-/
import Mathlib.Analysis.Matrix.PosDef
import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.Analysis.Matrix.Order
import Mathlib.LinearAlgebra.Matrix.SchurComplement

open scoped ComplexOrder Matrix MatrixOrder Matrix.Norms.L2Operator
open Matrix

variable {𝕜 : Type*} [RCLike 𝕜] {n : Type*} [Fintype n] [DecidableEq n]

namespace Matrix

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
      simp [hDdef, Matrix.add_apply, Matrix.one_apply_eq, Matrix.diagonal_apply_eq,
        Function.comp_apply]
    · simp [hDdef, Matrix.add_apply, Matrix.one_apply_ne h, Matrix.diagonal_apply_ne _ h]
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

/-- **Determinant monotonicity** (positive definite version): `det X ≤ det (X + P)`
for `X` positive definite and `P` positive semidefinite. Via the matrix determinant
lemma on the Gram factor `P = MᴴM`. -/
theorem PosDef.det_le_det_add {X P : Matrix n n 𝕜}
    (hX : X.PosDef) (hP : P.PosSemidef) : X.det ≤ (X + P).det := by
  obtain ⟨M, hM⟩ := CStarAlgebra.nonneg_iff_eq_star_mul_self.mp hP.nonneg
  rw [Matrix.star_eq_conjTranspose] at hM
  have hunit : IsUnit X.det := hX.det_pos.ne'.isUnit
  have hPSD : (M * X⁻¹ * Mᴴ).PosSemidef := hX.inv.posSemidef.mul_mul_conjTranspose_same M
  have hfac : (X + P).det = X.det * (1 + M * X⁻¹ * Mᴴ).det := by
    rw [hM, det_add_mul _ _ hunit]
  rw [hfac]
  have h1 : 1 ≤ (1 + M * X⁻¹ * Mᴴ).det := hPSD.one_le_det_one_add
  calc X.det = X.det * 1 := (mul_one _).symm
    _ ≤ X.det * (1 + M * X⁻¹ * Mᴴ).det := mul_le_mul_of_nonneg_left h1 hX.det_pos.le

/-- **Determinant monotonicity** on the whole PSD cone: `det X ≤ det (X + P)` for
`X` and `P` both positive semidefinite. -/
theorem PosSemidef.det_le_det_add {X P : Matrix n n 𝕜}
    (hX : X.PosSemidef) (hP : P.PosSemidef) : X.det ≤ (X + P).det := by
  by_cases h : X.det = 0
  · rw [h]; exact (hX.add hP).det_nonneg
  · exact (hX.posDef_iff_det_ne_zero.mpr h).det_le_det_add hP

/-- The determinant is monotone on the Löwner order restricted to positive
semidefinite matrices: `A ≤ B ⇒ det A ≤ det B`. -/
theorem PosSemidef.det_le_det_of_le {A B : Matrix n n 𝕜}
    (hA : A.PosSemidef) (hAB : A ≤ B) : A.det ≤ B.det := by
  have hP : (B - A).PosSemidef := le_iff.mp hAB
  simpa using hA.det_le_det_add hP

end Matrix
