/-
CIRISOntology.Core.OppenheimRCLike — the complex-general (RCLike) Oppenheim.

The `ℝ` Oppenheim / general contraction of `Core.Entropy` (`oppenheim_det`,
`S_pairwise_hadamard_le`) generalized to any `RCLike 𝕜` (real AND complex,
Hermitian PSD), so the complex-general theorem is KEPT in the repo and is the
artifact for the eventual Mathlib port. Self-contained in namespace
`CIRISOntology.Core.Herm` to avoid clashing with the `ℝ` versions; those remain
the stance-facing corollaries.

Every result here is sorry-free on the standard three axioms (audited in
`Audit/AxiomAudit.lean`). The generalization from the `ℝ` proof: the symmetric
outer product `vecMulVec u u` (`u uᵀ`) becomes the Hermitian `vecMulVec u (star u)`
(`u uᴴ`); `star_trivial` becomes `star_mul'`; the order is `ComplexOrder`; and the
pivot bound `0 ≤ α⁻¹` is read off the real part. `schurEquiv` and the ambient
Mathlib come from `Core.Entropy`.
-/
import CIRISOntology.Core.Entropy
open Matrix
open scoped ComplexOrder BigOperators
namespace CIRISOntology.Core.Herm

variable {𝕜 : Type*} [RCLike 𝕜] {n : Type*} [Fintype n] [DecidableEq n]

omit [DecidableEq n] in
/-- Hermitian outer product `u uᴴ` (`= vecMulVec u (star u)`) is PSD. -/
theorem posSemidef_vecMulVec (u : n → 𝕜) : (vecMulVec u (star u)).PosSemidef := by
  have h : vecMulVec u (star u) = Matrix.col Unit u * (Matrix.col Unit u)ᴴ := by
    ext i j
    simp [Matrix.vecMulVec_apply, Matrix.mul_apply, Matrix.conjTranspose_apply,
      Matrix.col_apply, Pi.star_apply]
  rw [h]
  exact Matrix.posSemidef_self_mul_conjTranspose _

omit [Fintype n] [DecidableEq n] in
/-- The rank-one Hermitian Hadamard identity:
    `(u uᴴ) ⊙ (v vᴴ) = (u∘v)(u∘v)ᴴ`. -/
theorem hadamard_vecMulVec (u v : n → 𝕜) :
    (vecMulVec u (star u)) ⊙ (vecMulVec v (star v))
      = vecMulVec (fun i => u i * v i) (star (fun i => u i * v i)) := by
  ext i j
  simp only [Matrix.hadamard_apply, Matrix.vecMulVec_apply, Pi.star_apply, star_mul']
  ring

/-- The block Schur–Hadamard identity (Hermitian form). -/
theorem schur_hadamard_identity {m : Type*} (α : 𝕜) (u v : m → 𝕜) (A₁ B₁ : Matrix m m 𝕜) :
    A₁ ⊙ B₁ - α⁻¹ • vecMulVec (fun i => u i * v i) (star (fun i => u i * v i))
      = (A₁ - α⁻¹ • vecMulVec u (star u)) ⊙ B₁
        + α⁻¹ • ((vecMulVec u (star u)) ⊙ (B₁ - vecMulVec v (star v))) := by
  ext i j
  simp only [Matrix.sub_apply, Matrix.add_apply, Matrix.smul_apply, Matrix.hadamard_apply,
    Matrix.vecMulVec_apply, Pi.star_apply, smul_eq_mul, star_mul']
  ring

omit [Fintype n] [DecidableEq n] in
/-- The `1×1`-pivot Schur term in Hermitian vecMulVec form. -/
theorem schur_oneScalar (D : Matrix (Fin 1) (Fin 1) 𝕜) (B : Matrix n (Fin 1) 𝕜) :
    B * D⁻¹ * Bᴴ
      = (D 0 0)⁻¹ • vecMulVec (fun i => B i 0) (star (fun i => B i 0)) := by
  have hDinv : D⁻¹ 0 0 = (D 0 0)⁻¹ := by
    rw [Matrix.inv_def, Matrix.adjugate_fin_one, Matrix.det_fin_one]
    simp [Ring.inverse_eq_inv']
  ext i j
  rw [Matrix.mul_apply, Fin.sum_univ_one, Matrix.mul_apply, Fin.sum_univ_one]
  simp only [Matrix.conjTranspose_apply, Matrix.smul_apply, Matrix.vecMulVec_apply,
    Pi.star_apply, smul_eq_mul, hDinv]
  ring

/-- A diagonal entry of a PosDef matrix is positive (ComplexOrder). -/
theorem posDef_diag_pos {A : Matrix n n 𝕜} (hA : A.PosDef) (i : n) : 0 < A i i := by
  have h0 : (Pi.single i (1 : 𝕜) : n → 𝕜) ≠ 0 := by
    intro h
    have hii : (Pi.single i (1 : 𝕜) : n → 𝕜) i = (0 : n → 𝕜) i := congrFun h i
    rw [Pi.single_eq_same, Pi.zero_apply] at hii
    exact one_ne_zero hii
  have hstar : star (Pi.single i (1 : 𝕜) : n → 𝕜) = Pi.single i (1 : 𝕜) := by
    funext k; simp [Pi.star_apply, Pi.single_apply, apply_ite (star : 𝕜 → 𝕜)]
  have key := hA.2 (Pi.single i (1 : 𝕜)) h0
  rw [hstar, Matrix.mulVec_single, Matrix.single_dotProduct] at key
  simpa using key

/-- A `1×1` matrix with positive entry is PosDef. -/
theorem posDef_fin_one (D : Matrix (Fin 1) (Fin 1) 𝕜) (h : 0 < D 0 0) : D.PosDef := by
  have hd : D = diagonal (fun _ => D 0 0) := by
    ext i j; fin_cases i; fin_cases j; simp
  rw [hd]
  exact (posDef_diagonal_iff).mpr (fun _ => h)

/-- Hadamard of Hermitian is Hermitian. -/
theorem isHermitian_hadamard {m : Type*} {A B : Matrix m m 𝕜}
    (hA : A.IsHermitian) (hB : B.IsHermitian) : (A ⊙ B).IsHermitian := by
  ext i j
  simp only [Matrix.conjTranspose_apply, Matrix.hadamard_apply, star_mul']
  rw [← Matrix.conjTranspose_apply, ← Matrix.conjTranspose_apply, hA.eq, hB.eq]

/-- Nonnegative-scalar multiple of a PSD matrix is PSD. -/
theorem posSemidef_smul {m : Type*} [Fintype m] {c : 𝕜} (hc : 0 ≤ c)
    {X : Matrix m m 𝕜} (hX : X.PosSemidef) : (c • X).PosSemidef := by
  have hcs : star c = c := RCLike.conj_eq_iff_im.mpr (RCLike.nonneg_iff.mp hc).2
  refine ⟨?_, fun x => ?_⟩
  · show (c • X)ᴴ = c • X
    rw [Matrix.conjTranspose_smul, hcs, hX.1.eq]
  · rw [Matrix.smul_mulVec_assoc, Matrix.dotProduct_smul, smul_eq_mul]
    exact mul_nonneg hc (hX.2 x)

omit [Fintype n] [DecidableEq n] in
/-- Hadamard commutes with submatrix. -/
theorem submatrix_hadamard {p₁ p₂ q₁ q₂ : Type*} (A B : Matrix q₁ q₂ 𝕜)
    (f : p₁ → q₁) (g : p₂ → q₂) :
    (A ⊙ B).submatrix f g = A.submatrix f g ⊙ B.submatrix f g := by
  ext i j; simp [Matrix.hadamard_apply, Matrix.submatrix_apply]

omit [Fintype n] [DecidableEq n] in
/-- Hadamard acts blockwise. -/
theorem hadamard_fromBlocks {α₁ α₂ β₁ β₂ : Type*}
    (A₁ A₂ : Matrix α₁ β₁ 𝕜) (B₁ B₂ : Matrix α₁ β₂ 𝕜)
    (C₁ C₂ : Matrix α₂ β₁ 𝕜) (D₁ D₂ : Matrix α₂ β₂ 𝕜) :
    (Matrix.fromBlocks A₁ B₁ C₁ D₁) ⊙ (Matrix.fromBlocks A₂ B₂ C₂ D₂)
      = Matrix.fromBlocks (A₁ ⊙ A₂) (B₁ ⊙ B₂) (C₁ ⊙ C₂) (D₁ ⊙ D₂) := by
  ext i j; cases i <;> cases j <;> rfl

/-! ### determinant inequalities over RCLike (verified earlier; needed by the induction) -/

theorem posSemidef_det_nonneg {X : Matrix n n 𝕜} (hX : X.PosSemidef) : 0 ≤ X.det := by
  rw [hX.1.det_eq_prod_eigenvalues, ← RCLike.ofReal_prod, RCLike.ofReal_nonneg]
  exact Finset.prod_nonneg (fun i _ => hX.eigenvalues_nonneg i)

theorem posDef_of_posSemidef_isUnit_det {A : Matrix n n 𝕜}
    (hA : A.PosSemidef) (hdet : IsUnit A.det) : A.PosDef := by
  have hAinv : IsUnit A := (Matrix.isUnit_iff_isUnit_det A).2 hdet
  have hinj : Function.Injective A.mulVec := Matrix.mulVec_injective_iff_isUnit.mpr hAinv
  refine ⟨hA.1, fun x hx => ?_⟩
  have hAx : A *ᵥ x ≠ 0 := fun h => hx (hinj (by rw [h, Matrix.mulVec_zero]))
  have hne : star x ⬝ᵥ A *ᵥ x ≠ 0 := by rw [Ne, hA.dotProduct_mulVec_zero_iff]; exact hAx
  exact lt_of_le_of_ne (hA.2 x) (Ne.symm hne)

theorem one_le_det_one_add_posSemidef {Q : Matrix n n 𝕜} (hQ : Q.PosSemidef) :
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
  have huu : U.det * (star U).det = 1 := by rw [← Matrix.det_mul, hUV, Matrix.det_one]
  rw [key, Matrix.det_mul, Matrix.det_mul, hdiag, Matrix.det_diagonal, mul_right_comm,
    huu, one_mul]
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

theorem det_le_det_add_of_posDef_posSemidef {X P : Matrix n n 𝕜}
    (hX : X.PosDef) (hP : P.PosSemidef) : X.det ≤ (X + P).det := by
  obtain ⟨M, hM⟩ := Matrix.posSemidef_iff_eq_transpose_mul_self.mp hP
  have hunit : IsUnit X.det := hX.det_pos.ne'.isUnit
  have hPSD : (M * X⁻¹ * Mᴴ).PosSemidef := hX.inv.posSemidef.mul_mul_conjTranspose_same M
  have hfac : (X + P).det = X.det * (1 + M * X⁻¹ * Mᴴ).det := by
    rw [hM, Matrix.det_add_mul _ _ hunit]
  rw [hfac]
  have h1 : 1 ≤ (1 + M * X⁻¹ * Mᴴ).det := one_le_det_one_add_posSemidef hPSD
  calc X.det = X.det * 1 := (mul_one _).symm
    _ ≤ X.det * (1 + M * X⁻¹ * Mᴴ).det := mul_le_mul_of_nonneg_left h1 hX.det_pos.le

theorem det_le_det_add_of_posSemidef {X P : Matrix n n 𝕜}
    (hX : X.PosSemidef) (hP : P.PosSemidef) : X.det ≤ (X + P).det := by
  by_cases h : IsUnit X.det
  · exact det_le_det_add_of_posDef_posSemidef (posDef_of_posSemidef_isUnit_det hX h) hP
  · have hX0 : X.det = 0 := not_not.mp (isUnit_iff_ne_zero.not.mp h)
    rw [hX0]; exact posSemidef_det_nonneg (hX.add hP)

omit [DecidableEq n] in
/-- Schur product theorem (Hermitian/RCLike). -/
theorem hadamard_posSemidef {A B : Matrix n n 𝕜}
    (hA : A.PosSemidef) (hB : B.PosSemidef) : (A ⊙ B).PosSemidef := by
  obtain ⟨P, hP⟩ := Matrix.posSemidef_iff_eq_transpose_mul_self.mp hA
  obtain ⟨Q, hQ⟩ := Matrix.posSemidef_iff_eq_transpose_mul_self.mp hB
  have key : A ⊙ B
      = (Matrix.of (fun kl : n × n => fun i => P kl.1 i * Q kl.2 i))ᴴ
        * Matrix.of (fun kl : n × n => fun i => P kl.1 i * Q kl.2 i) := by
    ext i j
    rw [Matrix.hadamard_apply, hP, hQ, Matrix.mul_apply, Matrix.mul_apply,
        Matrix.mul_apply, Finset.sum_mul_sum, Fintype.sum_prod_type]
    refine Finset.sum_congr rfl fun k _ => Finset.sum_congr rfl fun l _ => ?_
    simp only [Matrix.conjTranspose_apply, Matrix.of_apply, star_mul']
    ring
  rw [key]
  exact Matrix.posSemidef_conjTranspose_mul_self _

open CIRISOntology.Core in
open CIRISOntology.Core in
/-- Block determinant reduction (Hermitian/RCLike). -/
theorem det_schur_reduce {k : ℕ} (A : Matrix (Fin (k + 1)) (Fin (k + 1)) 𝕜)
    (hHerm : A.IsHermitian) (hpiv : A (Fin.last k) (Fin.last k) ≠ 0) :
    A.det = A (Fin.last k) (Fin.last k)
      * (((A.submatrix (schurEquiv k) (schurEquiv k)).toBlocks₁₁
          - (A (Fin.last k) (Fin.last k))⁻¹
            • vecMulVec (fun i => A.submatrix (schurEquiv k) (schurEquiv k) (Sum.inl i) (Sum.inr 0))
                (star fun i => A.submatrix (schurEquiv k) (schurEquiv k) (Sum.inl i) (Sum.inr 0)))).det := by
  set M := A.submatrix (schurEquiv k) (schurEquiv k) with hM
  have hMh : M.IsHermitian := hHerm.submatrix (schurEquiv k)
  have hblk : M = fromBlocks M.toBlocks₁₁ M.toBlocks₁₂ M.toBlocks₂₁ M.toBlocks₂₂ :=
    (fromBlocks_toBlocks M).symm
  have h21 : M.toBlocks₂₁ = (M.toBlocks₁₂)ᴴ := by
    have hh := hMh; rw [hblk] at hh
    exact ((isHermitian_fromBlocks_iff.mp hh).2.1).symm
  have hα : A (Fin.last k) (Fin.last k) = M.toBlocks₂₂ 0 0 := by
    simp [hM, Matrix.toBlocks₂₂, Matrix.submatrix_apply, schurEquiv,
      finSumFinEquiv_apply_right, Fin.natAdd, Fin.last]
  have hDdet : (M.toBlocks₂₂).det = A (Fin.last k) (Fin.last k) := by
    rw [Matrix.det_fin_one, ← hα]
  have hDunit : IsUnit (M.toBlocks₂₂).det := by rw [hDdet]; exact hpiv.isUnit
  letI : Invertible (M.toBlocks₂₂) := (M.toBlocks₂₂).invertibleOfIsUnitDet hDunit
  have hAM : A.det = M.det := (det_submatrix_equiv_self (schurEquiv k) A).symm
  have hMdet : M.det = (M.toBlocks₂₂).det
      * (M.toBlocks₁₁ - M.toBlocks₁₂ * (M.toBlocks₂₂)⁻¹ * (M.toBlocks₁₂)ᴴ).det := by
    conv_lhs => rw [← fromBlocks_toBlocks M]
    rw [h21, det_fromBlocks₂₂, invOf_eq_nonsing_inv]
  rw [hAM, hMdet, hDdet, schur_oneScalar, ← hα]
  simp only [Matrix.toBlocks₁₂, Matrix.of_apply]

open CIRISOntology.Core in
open CIRISOntology.Core in
/-- PSD Schur complement (Hermitian/RCLike). -/
theorem schur_posSemidef {k : ℕ} (A : Matrix (Fin (k + 1)) (Fin (k + 1)) 𝕜)
    (hA : A.PosSemidef) (hpiv : 0 < A (Fin.last k) (Fin.last k)) :
    ((A.submatrix (schurEquiv k) (schurEquiv k)).toBlocks₁₁
      - (A (Fin.last k) (Fin.last k))⁻¹
        • vecMulVec (fun i => A.submatrix (schurEquiv k) (schurEquiv k) (Sum.inl i) (Sum.inr 0))
            (star fun i => A.submatrix (schurEquiv k) (schurEquiv k) (Sum.inl i) (Sum.inr 0))).PosSemidef := by
  set M := A.submatrix (schurEquiv k) (schurEquiv k) with hM
  have hMh : M.IsHermitian := hA.1.submatrix (schurEquiv k)
  have hMpsd : M.PosSemidef := hA.submatrix (schurEquiv k)
  have hblk : M = fromBlocks M.toBlocks₁₁ M.toBlocks₁₂ M.toBlocks₂₁ M.toBlocks₂₂ :=
    (fromBlocks_toBlocks M).symm
  have h21 : M.toBlocks₂₁ = (M.toBlocks₁₂)ᴴ := by
    have hh := hMh; rw [hblk] at hh
    exact ((isHermitian_fromBlocks_iff.mp hh).2.1).symm
  have hα : A (Fin.last k) (Fin.last k) = M.toBlocks₂₂ 0 0 := by
    simp [hM, Matrix.toBlocks₂₂, Matrix.submatrix_apply, schurEquiv,
      finSumFinEquiv_apply_right, Fin.natAdd, Fin.last]
  have hDpd : (M.toBlocks₂₂).PosDef := posDef_fin_one _ (by rw [← hα]; exact hpiv)
  letI : Invertible (M.toBlocks₂₂) := (M.toBlocks₂₂).invertibleOfIsUnitDet hDpd.det_pos.ne'.isUnit
  have hMpsd' : (fromBlocks M.toBlocks₁₁ M.toBlocks₁₂ (M.toBlocks₁₂)ᴴ M.toBlocks₂₂).PosSemidef := by
    have hh := hMpsd; rw [hblk, h21] at hh; exact hh
  have hsc := (PosSemidef.fromBlocks₂₂ M.toBlocks₁₁ M.toBlocks₁₂ hDpd).mp hMpsd'
  rw [schur_oneScalar, ← hα] at hsc
  simpa [Matrix.toBlocks₁₂, Matrix.of_apply] using hsc

open CIRISOntology.Core in
open CIRISOntology.Core in
/-- GENERAL OPPENHEIM (Hermitian/RCLike, unit-diagonal `B`). -/
theorem oppenheim_det {k : ℕ} : ∀ (A B : Matrix (Fin k) (Fin k) 𝕜),
    A.PosSemidef → B.PosSemidef → (∀ i, B i i = 1) → A.det ≤ (A ⊙ B).det := by
  induction k with
  | zero => intro A B _ _ _; simp [Matrix.det_fin_zero]
  | succ k ih =>
    intro A B hA hB hBd
    by_cases hApd : A.PosDef
    · have hαpos : 0 < A (Fin.last k) (Fin.last k) := posDef_diag_pos hApd (Fin.last k)
      set MA := A.submatrix (schurEquiv k) (schurEquiv k) with hMA
      set MB := B.submatrix (schurEquiv k) (schurEquiv k) with hMB
      set α := A (Fin.last k) (Fin.last k) with hαdef
      set A₁ := MA.toBlocks₁₁ with hA1
      set B₁ := MB.toBlocks₁₁ with hB1
      set u := fun i => MA (Sum.inl i) (Sum.inr 0) with hu
      set v := fun i => MB (Sum.inl i) (Sum.inr 0) with hv
      set CA := A₁ - α⁻¹ • vecMulVec u (star u) with hCA
      have hdetA : A.det = α * CA.det := det_schur_reduce A hApd.1 (ne_of_gt hαpos)
      have hBd_last : B (Fin.last k) (Fin.last k) = 1 := hBd (Fin.last k)
      have hABpiv : (A ⊙ B) (Fin.last k) (Fin.last k) = α := by
        rw [Matrix.hadamard_apply, hBd_last, mul_one]
      have hABherm : (A ⊙ B).IsHermitian := isHermitian_hadamard hA.1 hB.1
      have hdetAB : (A ⊙ B).det = α * (CA ⊙ B₁
          + α⁻¹ • (vecMulVec u (star u) ⊙ (B₁ - vecMulVec v (star v)))).det := by
        have hstep := det_schur_reduce (A ⊙ B) hABherm (hABpiv ▸ ne_of_gt hαpos)
        rw [hABpiv] at hstep
        rw [hstep]
        congr 2
        have hblk11 : ((A ⊙ B).submatrix (schurEquiv k) (schurEquiv k)).toBlocks₁₁ = A₁ ⊙ B₁ := by
          rw [submatrix_hadamard]; rfl
        have hoff : (fun i => (A ⊙ B).submatrix (schurEquiv k) (schurEquiv k) (Sum.inl i) (Sum.inr 0))
            = fun i => u i * v i := by
          funext i; rw [submatrix_hadamard]; rfl
        rw [hblk11, hoff, ← schur_hadamard_identity]
      have hCApsd : CA.PosSemidef := schur_posSemidef A hApd.posSemidef hαpos
      have hB1psd : B₁.PosSemidef := (hB.submatrix (schurEquiv k)).submatrix Sum.inl
      have hB1diag : ∀ i, B₁ i i = 1 := by
        intro i
        have := hBd (schurEquiv k (Sum.inl i))
        simpa [hB1, hMB, Matrix.toBlocks₁₁, Matrix.submatrix_apply] using this
      have hBvvpsd : (B₁ - vecMulVec v (star v)).PosSemidef := by
        have hh := schur_posSemidef B hB (by rw [hBd_last]; norm_num)
        rw [hBd_last, inv_one, one_smul] at hh
        exact hh
      have hαinv : (0 : 𝕜) ≤ α⁻¹ := by
        obtain ⟨hre, him⟩ := RCLike.pos_iff.mp hαpos
        have hαeq : ((RCLike.re α : ℝ) : 𝕜) = α := by
          have h := RCLike.re_add_im α; rw [him] at h; simpa using h
        rw [← hαeq, ← RCLike.ofReal_inv, RCLike.ofReal_nonneg]
        exact le_of_lt (inv_pos.mpr hre)
      have hPpsd : (α⁻¹ • (vecMulVec u (star u) ⊙ (B₁ - vecMulVec v (star v)))).PosSemidef :=
        posSemidef_smul hαinv (hadamard_posSemidef (posSemidef_vecMulVec u) hBvvpsd)
      have hCAB1 : (CA ⊙ B₁).PosSemidef := hadamard_posSemidef hCApsd hB1psd
      have hih : CA.det ≤ (CA ⊙ B₁).det := ih CA B₁ hCApsd hB1psd hB1diag
      have hmono : (CA ⊙ B₁).det ≤ (CA ⊙ B₁ + α⁻¹ • (vecMulVec u (star u) ⊙ (B₁ - vecMulVec v (star v)))).det :=
        det_le_det_add_of_posSemidef hCAB1 hPpsd
      rw [hdetA, hdetAB]
      exact mul_le_mul_of_nonneg_left (le_trans hih hmono) hαpos.le
    · have hdA0 : A.det = 0 := by
        rcases (posSemidef_det_nonneg hA).lt_or_eq with hlt | heq
        · exact absurd (posDef_of_posSemidef_isUnit_det hA hlt.ne'.isUnit) hApd
        · exact heq.symm
      rw [hdA0]
      exact posSemidef_det_nonneg (hadamard_posSemidef hA hB)

/-! ### The fully-general form (`∏ᵢ Bᵢᵢ`, `B` not required unit-diagonal) -/

/-- A diagonal entry of a PSD matrix is a nonnegative real. -/
theorem posSemidef_diag_nonneg {A : Matrix n n 𝕜} (hA : A.PosSemidef) (i : n) : 0 ≤ A i i := by
  have h0 := hA.2 (Pi.single i (1 : 𝕜))
  have hstar : star (Pi.single i (1 : 𝕜) : n → 𝕜) = Pi.single i (1 : 𝕜) := by
    funext k; simp [Pi.star_apply, Pi.single_apply, apply_ite (star : 𝕜 → 𝕜)]
  rw [hstar, Matrix.mulVec_single, Matrix.single_dotProduct] at h0
  simpa using h0

/-- A nonnegative real element of `𝕜` equals the cast of its real part. -/
theorem eq_ofReal_re_of_nonneg {z : 𝕜} (hz : 0 ≤ z) : z = ((RCLike.re z : ℝ) : 𝕜) := by
  have him : RCLike.im z = 0 := (RCLike.nonneg_iff.mp hz).2
  have h := RCLike.re_add_im z; rw [him] at h; simpa using h.symm

/-- Conjugating by a diagonal on both sides, entrywise. -/
theorem diag_conj_entry (c : n → 𝕜) (X : Matrix n n 𝕜) (i j : n) :
    (diagonal c * X * diagonal c) i j = c i * X i j * c j := by
  rw [Matrix.mul_diagonal, Matrix.diagonal_mul]

/-- FULLY GENERAL OPPENHEIM (Hermitian/RCLike): `det A · ∏ᵢ Bᵢᵢ ≤ det(A ⊙ B)` for PSD
    `A` and PSD `B` — the full textbook statement, dropping the unit-diagonal
    restriction. If some `Bᵢᵢ = 0` both sides collapse to `0`; otherwise scale `B` to
    unit diagonal by `D = diag(√Bᵢᵢ)` (so `A ⊙ B = D (A ⊙ B') D`,
    `det = (∏ Bᵢᵢ)·det(A ⊙ B')`) and apply `oppenheim_det`. -/
theorem oppenheim_prod {k : ℕ} (A B : Matrix (Fin k) (Fin k) 𝕜)
    (hA : A.PosSemidef) (hB : B.PosSemidef) :
    A.det * ∏ i, B i i ≤ (A ⊙ B).det := by
  by_cases hprod : (∏ i, B i i) = 0
  · rw [hprod, mul_zero]
    exact posSemidef_det_nonneg (hadamard_posSemidef hA hB)
  · have hBii_ne : ∀ i, B i i ≠ 0 := fun i h => hprod (Finset.prod_eq_zero (Finset.mem_univ i) h)
    have hBii_pos : ∀ i, 0 < B i i := fun i =>
      lt_of_le_of_ne (posSemidef_diag_nonneg hB i) (Ne.symm (hBii_ne i))
    have hre_pos : ∀ i, 0 < RCLike.re (B i i) := fun i => (RCLike.pos_iff.mp (hBii_pos i)).1
    set d : Fin k → 𝕜 := fun i => ((Real.sqrt (RCLike.re (B i i)) : ℝ) : 𝕜) with hd
    have hd_sq : ∀ i, d i * d i = B i i := by
      intro i
      have hre := (hre_pos i).le
      calc d i * d i
          = ((Real.sqrt (RCLike.re (B i i)) * Real.sqrt (RCLike.re (B i i)) : ℝ) : 𝕜) := by
            rw [hd]; push_cast; ring
        _ = ((RCLike.re (B i i) : ℝ) : 𝕜) := by rw [Real.mul_self_sqrt hre]
        _ = B i i := (eq_ofReal_re_of_nonneg (hBii_pos i).le).symm
    have hd_ne : ∀ i, d i ≠ 0 := fun i h => hBii_ne i (by rw [← hd_sq i, h, mul_zero])
    set e : Fin k → 𝕜 := fun i => (d i)⁻¹ with he
    set B' : Matrix (Fin k) (Fin k) 𝕜 := diagonal e * B * diagonal e with hB'
    have hstar_e : ∀ i, star (e i) = e i := by
      intro i
      simp only [he, hd]
      rw [star_inv₀, ← starRingEnd_apply, RCLike.conj_ofReal]
    have he_herm : (diagonal e)ᴴ = diagonal e := by
      rw [Matrix.diagonal_conjTranspose]
      exact congrArg diagonal (funext fun i => hstar_e i)
    have hB'psd : B'.PosSemidef := by
      have := hB.conjTranspose_mul_mul_same (diagonal e)
      rwa [he_herm] at this
    have hB'diag : ∀ i, B' i i = 1 := by
      intro i
      rw [hB', diag_conj_entry]
      simp only [he]
      rw [← hd_sq i]
      field_simp [hd_ne i]
    have hAB_eq : A ⊙ B = diagonal d * (A ⊙ B') * diagonal d := by
      ext i j
      rw [diag_conj_entry, Matrix.hadamard_apply, Matrix.hadamard_apply, hB', diag_conj_entry]
      simp only [he]
      field_simp [hd_ne i, hd_ne j]
      ring
    have hdetAB : (A ⊙ B).det = (∏ i, B i i) * (A ⊙ B').det := by
      rw [hAB_eq, Matrix.det_mul, Matrix.det_mul, Matrix.det_diagonal]
      rw [show (∏ i, B i i) = (∏ i, d i) * (∏ i, d i) from by
        rw [← Finset.prod_mul_distrib]; exact Finset.prod_congr rfl (fun i _ => (hd_sq i).symm)]
      ring
    rw [hdetAB]
    have hopp : A.det ≤ (A ⊙ B').det := oppenheim_det A B' hA hB'psd hB'diag
    have hprod_nonneg : 0 ≤ ∏ i, B i i := Finset.prod_nonneg (fun i _ => (hBii_pos i).le)
    calc A.det * ∏ i, B i i = (∏ i, B i i) * A.det := by ring
      _ ≤ (∏ i, B i i) * (A ⊙ B').det := mul_le_mul_of_nonneg_left hopp hprod_nonneg

end CIRISOntology.Core.Herm
