/-
CIRISOntology.Core.Entropy — the entropic-contraction spine: the instrument's
floor is a genuine minimum, the pointwise operation cannot fabricate structure,
and where the arithmetic is small enough to close by hand, `S` provably falls.

WHAT THIS IS. The instrument `S = −ln det C` of `Core.Coordination` reads the
pairwise part of coordination. This file mechanizes the linear-algebra backbone
that says what `S` does under the natural coarsening operation — the Hadamard
(entrywise) product `A ⊙ B`, the matrix image of a pointwise transform of the
underlying variables. The physics question behind it is whether a purely local
model can drive `S` UP (manufacture apparent higher coordination out of a
pointwise relabelling). The answer, to the extent proved here, is no.

WHAT IS PROVED HERE (zero `sorry`, standard axioms only; audited in
`Audit/AxiomAudit.lean`):

  * BASE — `neg_log_det_nonneg`: for every real PSD unit-diagonal `C` with
    `det C > 0`, `0 ≤ −ln det C`. The chaos floor of `S` is a true minimum over
    ALL correlation matrices, not just the uniform family. `S_pairwise_nonneg`
    restates it for the repository's instrument, and `neg_log_det_eq_zero_iff`
    sharpens it: the floor is reached at exactly one matrix, `C = 1` — the same
    identity at which `Core.Coordination.S_pairwise_identity` reads zero.
    (Klein's inequality, general matrix form: `log λ ≤ λ − 1` per eigenvalue,
    summed against `Σ λ = tr C = n`.)

  * SCHUR — `hadamard_posSemidef`: the Hadamard product of two PSD matrices is
    PSD. Proved here directly (see the survey) via the Gram factorization: if
    `A = PᴴP` and `B = QᴴQ` then `A ⊙ B = RᴴR` for the row-tensor
    `R⟨k,l⟩ i = P k i · Q l i`, so it is PSD with no appeal to eigenvalues.
    `IsUnitDiag.hadamard` records that unit diagonals are preserved, so `A ⊙ B`
    is again a correlation matrix.

  * OPPENHEIM (n = 2) — `oppenheim_two`: for 2×2 unit-diagonal `C(a), C(b)` with
    `|a|,|b| ≤ 1`, `det(C(a) ⊙ C(b)) ≥ det C(a)`. The concrete determinant-raising
    step of the contraction, closed by hand at n = 2.

  * CONTRACTION — `S_pairwise_hadamard_le_two`: the corollary that ties the above
    to the instrument. At n = 2, for `|a| < 1`, `S(C(a) ⊙ C(b)) ≤ S(C(a))`: the
    pointwise operation does NOT raise `S`. Scoped honestly — this is the n = 2
    case only (see below). `neg_log_det_hadamard_nonneg` states the one thing
    Schur + Klein give at every n: `A ⊙ B` is a correlation matrix, so its `S`
    sits at or above the floor. That is a lower bound, NOT the contraction; the
    contraction at general n is not proved here.

  * INFRASTRUCTURE toward general Oppenheim — a battery of standalone reusable
    lemmas, all absent from Mathlib v4.14, that the Schur-complement induction
    rests on:
      - `one_le_det_one_add_posSemidef`: `1 ≤ det(1 + Q)` for PSD `Q`;
      - `posSemidef_det_nonneg`: `0 ≤ det X` for PSD `X`;
      - `posDef_of_posSemidef_det_pos`: PSD `+ det > 0 ⇒ PosDef`;
      - `det_le_det_add_of_posDef_posSemidef` and its general-cone extension
        `det_le_det_add_of_posSemidef`: determinant monotonicity `det X ≤ det(X+P)`;
      - `hadamard_fromBlocks`: `⊙` acts blockwise on `2×2` block matrices;
      - `hadamard_vecMulVec`: the rank-one identity `(u uᵀ) ⊙ (v vᵀ) = (u∘v)(u∘v)ᵀ`.
    STILL OPEN — hence the general contraction `S(A ⊙ B) ≤ S(A)` is not proved
    here: (i) the Schur complement of a PosDef matrix is PosDef; (ii) the block
    identity `M = C₁∘B₁ + rank-one PSD` for the `(1,1)` Schur pivot of `A ⊙ B`;
    (iii) the `Fin (n+1) ≃ Fin 1 ⊕ Fin n` reindex + `det_fromBlocks₁₁` assembly;
    (iv) the strong induction on dimension. The determinant and block-Hadamard
    machinery above are the pieces that WERE missing; the assembly is what remains.

PORTED. The BASE (Klein) and OPPENHEIM-2 results, and the `trace_eq_sum_eigenvalues`
helper, are ported from the predecessor
`coherence-ratchet/…/Core/EntropicContraction.lean` (T-C1, T-C3₂). SCHUR is NEW
here: the predecessor recorded it as an open roadmap item (its T-C2); the Gram
route above closes it.

================================================================================
MATHLIB v4.14 SURVEY (checked against .lake/packages/mathlib @ v4.14.0)
================================================================================
PRESENT and used:
  • `Matrix.PosSemidef`, `.eigenvalues_nonneg`, `.det_eq_prod_eigenvalues`,
    `.spectral_theorem`                          (LinearAlgebra/Matrix/{PosDef,Spectrum})
  • `Matrix.posSemidef_iff_eq_transpose_mul_self` — PSD ↔ `∃ B, A = BᴴB`  (PosDef.lean:287)
  • `Matrix.posSemidef_conjTranspose_mul_self`    — `(BᴴB)` is PSD          (PosDef.lean:267)
  • `Matrix.mem_unitaryGroup_iff` / `_iff'`        (LinearAlgebra/UnitaryGroup.lean:63,67)
  • `Finset.sum_mul_sum`, `Fintype.sum_prod_type`  (product of sums ↔ sum over pairs)
  • `Real.log_prod`, `Real.log_le_sub_one_of_pos`, `Real.log_lt_sub_one_of_pos`,
    `Real.log_le_log`                              (Analysis/SpecialFunctions/Log/Basic)

ABSENT — the reason the contraction stops where it does:
  • SCHUR PRODUCT THEOREM as a named lemma. `Data/Matrix/Hadamard.lean` carries
    only the algebra of `⊙` (comm/assoc/distrib), NO positivity; `Kronecker.lean`
    has no `PosSemidef`. So `hadamard_posSemidef` is proved from scratch here,
    via the Gram route — no Schur/Kronecker positivity is imported.
  • OPPENHEIM (general n): `det(A ⊙ B) ≥ det A · Πᵢ Bᵢᵢ`. Absent. The standard
    proof is induction on dimension through Schur complements
    (`SchurComplement.lean` has the block infrastructure) and depends on the
    Schur product theorem above; the n = 2 base case is closed here, the
    induction is the open work. This is the single missing step between the
    n = 2 contraction and the general contraction `S(A ⊙ B) ≤ S(A)`.
  • (−ln det) CONVEXITY on the PSD cone. Absent (no `StrictConcaveOn … det`).
    Not needed for the results above; it is what a convex-combination closure of
    the full no-phantom inequality would additionally require.

SCOPE. Everything here is forward linear algebra grounding the candidate
instrument `S = −ln det C`. It says what `S` and the pointwise operation do to
one another; it asserts nothing about whether any substrate realizes the
higher-order coordination the instrument cannot see (that is `Core.Coordination`
and `Core.Third`), and nothing about physics.
-/
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.LinearAlgebra.Matrix.Spectrum
import Mathlib.LinearAlgebra.Matrix.SchurComplement
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Matrix.Hadamard
import Mathlib.Data.Real.StarOrdered
import Mathlib.Algebra.BigOperators.Ring
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.FinCases
import CIRISOntology.Core.Coordination

namespace CIRISOntology.Core

open Matrix Real
open scoped BigOperators

variable {n : Type*} [Fintype n] [DecidableEq n]

/-! ## Definitions -/

/-- A correlation matrix has unit diagonal: `C i i = 1` for every index. The
    normalization that makes `S = −ln det C` read shape rather than scale. -/
def IsUnitDiag (C : Matrix n n ℝ) : Prop := ∀ i, C i i = 1

/-! ## Trace helper

Mathlib v4.14 has no direct "trace = sum of eigenvalues" for a real Hermitian
matrix; this derives it from the spectral theorem and cyclicity of the trace. -/

/-- The trace of a real Hermitian matrix is the sum of its eigenvalues. Via the
    spectral theorem `A = U diag(λ) Uᴴ` and `Uᴴ U = 1`. -/
theorem trace_eq_sum_eigenvalues {A : Matrix n n ℝ} (hA : A.IsHermitian) :
    A.trace = ∑ i, hA.eigenvalues i := by
  have hU : star (Matrix.IsHermitian.eigenvectorUnitary hA : Matrix n n ℝ)
      * (Matrix.IsHermitian.eigenvectorUnitary hA : Matrix n n ℝ) = 1 :=
    (mem_unitaryGroup_iff').mp (Matrix.IsHermitian.eigenvectorUnitary hA).2
  conv_lhs => rw [hA.spectral_theorem]
  rw [Matrix.trace_mul_comm, ← Matrix.mul_assoc, hU, Matrix.one_mul, Matrix.trace_diagonal]
  simp only [Function.comp_apply, RCLike.ofReal_real_eq_id, id_eq]

/-! ## BASE — Klein nonnegativity: the chaos floor is a true minimum -/

/-- BASE. KLEIN INEQUALITY, GENERAL MATRIX FORM: for any PSD unit-diagonal `C`
    with `det C > 0`, `0 ≤ −ln det C`. The floor of `S` over the whole
    correlation manifold, not just the uniform family. Proof: eigenvalues are
    positive (PSD + `det > 0`), sum to `tr C = n` (unit diagonal), and
    `log λ ≤ λ − 1` per eigenvalue gives `Σ log λ ≤ Σ(λ − 1) = 0`, i.e.
    `det C ≤ 1`. -/
theorem neg_log_det_nonneg {C : Matrix n n ℝ} (hC : C.PosSemidef)
    (hdiag : IsUnitDiag C) (hdet : 0 < C.det) : 0 ≤ -Real.log C.det := by
  set e := hC.1.eigenvalues with he
  have hdet_eq : C.det = ∏ i, e i := by simpa using hC.1.det_eq_prod_eigenvalues
  have hev_ne : ∀ i, e i ≠ 0 := by
    intro i hi
    have hz : ∏ j, e j = 0 := Finset.prod_eq_zero (Finset.mem_univ i) hi
    rw [← hdet_eq] at hz; exact absurd hz (ne_of_gt hdet)
  have hev_pos : ∀ i, 0 < e i := fun i =>
    lt_of_le_of_ne (hC.eigenvalues_nonneg i) (Ne.symm (hev_ne i))
  have hlog : Real.log C.det = ∑ i, Real.log (e i) := by
    rw [hdet_eq, Real.log_prod _ _ (fun i _ => hev_ne i)]
  have hsum_le : ∑ i, Real.log (e i) ≤ ∑ i, (e i - 1) :=
    Finset.sum_le_sum (fun i _ => Real.log_le_sub_one_of_pos (hev_pos i))
  have htraceC : C.trace = (Fintype.card n : ℝ) := by
    have hd : ∀ i, C i i = (1 : ℝ) := hdiag
    have htr : C.trace = ∑ i, C i i := rfl
    rw [htr]
    simp only [hd, Finset.sum_const, Finset.card_univ, nsmul_eq_mul, mul_one]
  have htrace : ∑ i, e i = (Fintype.card n : ℝ) := by
    rw [he, ← trace_eq_sum_eigenvalues hC.1, htraceC]
  have hsum_zero : ∑ i, (e i - 1) = 0 := by
    rw [Finset.sum_sub_distrib, htrace]
    simp [Finset.card_univ]
  rw [hlog]
  linarith [hsum_le, hsum_zero]

/-- BASE, restated for the instrument. `S_pairwise` of a PSD unit-diagonal
    correlation matrix with positive determinant is nonnegative: the chaos pole
    is the bottom of the instrument's range. -/
theorem S_pairwise_nonneg {m : ℕ} {C : Matrix (Fin m) (Fin m) ℝ}
    (hC : C.PosSemidef) (hdiag : IsUnitDiag C) (hdet : 0 < C.det) :
    0 ≤ S_pairwise C := by
  unfold S_pairwise
  exact neg_log_det_nonneg hC hdiag hdet

/-- BASE, sharpened (equality). The floor `−ln det C = 0` is reached IFF `C = 1`:
    the identity is the unique zero of `S` on the correlation manifold. This is
    the general-matrix companion of `Core.Coordination.S_pairwise_identity`
    (which exhibits the value 0 at `C = 1`); together they say the floor is
    attained there and NOWHERE else. Forward: equality in `log λ ≤ λ − 1` forces
    every eigenvalue to 1, and the spectral theorem reconstructs `C = 1`. -/
theorem neg_log_det_eq_zero_iff {C : Matrix n n ℝ} (hC : C.PosSemidef)
    (hdiag : IsUnitDiag C) (hdet : 0 < C.det) : -Real.log C.det = 0 ↔ C = 1 := by
  constructor
  · intro h0
    set e := hC.1.eigenvalues with he
    have hdet_eq : C.det = ∏ i, e i := by simpa using hC.1.det_eq_prod_eigenvalues
    have hev_ne : ∀ i, e i ≠ 0 := by
      intro i hi
      have hz : ∏ j, e j = 0 := Finset.prod_eq_zero (Finset.mem_univ i) hi
      rw [← hdet_eq] at hz; exact absurd hz (ne_of_gt hdet)
    have hev_pos : ∀ i, 0 < e i := fun i =>
      lt_of_le_of_ne (hC.eigenvalues_nonneg i) (Ne.symm (hev_ne i))
    have hlog : Real.log C.det = ∑ i, Real.log (e i) := by
      rw [hdet_eq, Real.log_prod _ _ (fun i _ => hev_ne i)]
    have hlog_zero : ∑ i, Real.log (e i) = 0 := by
      have hz : Real.log C.det = 0 := by linarith [h0]
      rw [hlog] at hz; exact hz
    have htraceC : C.trace = (Fintype.card n : ℝ) := by
      have hd : ∀ i, C i i = (1 : ℝ) := hdiag
      have htr : C.trace = ∑ i, C i i := rfl
      rw [htr]
      simp only [hd, Finset.sum_const, Finset.card_univ, nsmul_eq_mul, mul_one]
    have htrace : ∑ i, e i = (Fintype.card n : ℝ) := by
      rw [he, ← trace_eq_sum_eigenvalues hC.1, htraceC]
    have hsum_zero : ∑ i, (e i - 1) = 0 := by
      rw [Finset.sum_sub_distrib, htrace]; simp [Finset.card_univ]
    have hg_nonneg : ∀ i ∈ Finset.univ, 0 ≤ (e i - 1) - Real.log (e i) := by
      intro i _; linarith [Real.log_le_sub_one_of_pos (hev_pos i)]
    have hg_sum : ∑ i, ((e i - 1) - Real.log (e i)) = 0 := by
      rw [Finset.sum_sub_distrib, hsum_zero, hlog_zero, sub_zero]
    have hg_each := (Finset.sum_eq_zero_iff_of_nonneg hg_nonneg).mp hg_sum
    have hev1 : ∀ i, e i = 1 := by
      intro i
      by_contra hne
      have hlt := Real.log_lt_sub_one_of_pos (hev_pos i) hne
      have := hg_each i (Finset.mem_univ i)
      linarith
    rw [hC.1.spectral_theorem]
    have hdiag1 : (diagonal (RCLike.ofReal ∘ hC.1.eigenvalues) : Matrix n n ℝ) = 1 := by
      have hfun : (RCLike.ofReal ∘ hC.1.eigenvalues) = (fun _ => (1 : ℝ)) := by
        funext i; simp [Function.comp, RCLike.ofReal_real_eq_id, ← he, hev1 i]
      rw [hfun]; exact diagonal_one
    rw [hdiag1, Matrix.mul_one]
    exact (mem_unitaryGroup_iff).mp (Matrix.IsHermitian.eigenvectorUnitary hC.1).2
  · intro h
    subst h
    simp [Matrix.det_one, Real.log_one]

/-! ## SCHUR — the Hadamard product of PSD matrices is PSD

Absent from Mathlib v4.14 as a named lemma (see the header survey); proved here
from the Gram factorization. If `A = PᴴP` and `B = QᴴQ`, then entrywise
`(A ⊙ B)ᵢⱼ = (Σₖ P̄ₖᵢ Pₖⱼ)(Σₗ Q̄ₗᵢ Qₗⱼ) = Σₖₗ (Pₖᵢ Qₗᵢ)‾ (Pₖⱼ Qₗⱼ)`, which is
exactly `(RᴴR)ᵢⱼ` for the row-tensor `R⟨k,l⟩ i = Pₖᵢ Qₗᵢ`. A matrix of the form
`RᴴR` is PSD. -/

omit [DecidableEq n] in
/-- SCHUR PRODUCT THEOREM. The Hadamard (entrywise) product of two PSD matrices
    is PSD. Proved via the Gram route (`A ⊙ B = RᴴR`), so it imports no Schur or
    Kronecker positivity — there is none in Mathlib v4.14 to import. -/
theorem hadamard_posSemidef {A B : Matrix n n ℝ}
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
    simp only [Matrix.conjTranspose_apply, Matrix.of_apply, star_trivial]
    ring
  rw [key]
  exact Matrix.posSemidef_conjTranspose_mul_self _

omit [Fintype n] [DecidableEq n] in
/-- The Hadamard product of two unit-diagonal matrices is unit-diagonal: the
    correlation manifold is closed under `⊙`. With `hadamard_posSemidef`, `A ⊙ B`
    is again a correlation matrix. -/
theorem IsUnitDiag.hadamard {A B : Matrix n n ℝ}
    (hA : IsUnitDiag A) (hB : IsUnitDiag B) : IsUnitDiag (A ⊙ B) := by
  intro i
  rw [Matrix.hadamard_apply, hA i, hB i, mul_one]

/-! ## OPPENHEIM at n = 2, and the contraction it delivers -/

/-- OPPENHEIM at n = 2. For 2×2 unit-diagonal correlation matrices
    `C(a) = !![1,a;a,1]` and `C(b)` with `|a|,|b| ≤ 1`,
    `det(C(a) ⊙ C(b)) ≥ det C(a)`: the entrywise product shrinks the off-diagonal
    (`a ↦ ab`), raising the determinant. The `b = a` instance is the
    Hadamard-square step. General `n` is roadmapped (see the header survey). -/
theorem oppenheim_two (a b : ℝ) (_ha : |a| ≤ 1) (hb : |b| ≤ 1) :
    (!![1, a; a, 1] ⊙ !![1, b; b, 1] : Matrix (Fin 2) (Fin 2) ℝ).det
      ≥ (!![1, a; a, 1] : Matrix (Fin 2) (Fin 2) ℝ).det := by
  obtain ⟨hb1, hb1'⟩ := abs_le.mp hb
  have hb2 : b ^ 2 ≤ 1 := by nlinarith [hb1, hb1']
  have hprod : (!![1, a; a, 1] ⊙ !![1, b; b, 1] : Matrix (Fin 2) (Fin 2) ℝ)
      = !![1, a * b; a * b, 1] := by
    ext i j; fin_cases i <;> fin_cases j <;> simp [Matrix.hadamard_apply]
  rw [hprod, Matrix.det_fin_two_of, Matrix.det_fin_two_of]
  nlinarith [sq_nonneg a, mul_nonneg (sq_nonneg a) (sub_nonneg.mpr hb2)]

/-- CONTRACTION (n = 2). The corollary that ties the spine to the instrument: at
    n = 2, for `|a| < 1` and `|b| ≤ 1`, `S(C(a) ⊙ C(b)) ≤ S(C(a))`. The pointwise
    operation cannot raise `S`; a local relabelling manufactures no pairwise
    coordination. Immediate from `oppenheim_two` (`det` rises) and monotonicity
    of `log` (so `−log det` falls), using `det C(a) = 1 − a² > 0`.

    HONEST SCOPE: n = 2 only. The general `S(A ⊙ B) ≤ S(A)` needs Oppenheim at
    every `n`, whose induction is the one open step recorded in the header. -/
theorem S_pairwise_hadamard_le_two (a b : ℝ) (ha : |a| < 1) (hb : |b| ≤ 1) :
    S_pairwise (!![1, a; a, 1] ⊙ !![1, b; b, 1] : Matrix (Fin 2) (Fin 2) ℝ)
      ≤ S_pairwise (!![1, a; a, 1] : Matrix (Fin 2) (Fin 2) ℝ) := by
  have hopp := oppenheim_two a b (le_of_lt ha) hb
  have hpos : 0 < (!![1, a; a, 1] : Matrix (Fin 2) (Fin 2) ℝ).det := by
    rw [Matrix.det_fin_two_of]
    obtain ⟨h1, h2⟩ := abs_lt.mp ha
    nlinarith [mul_pos (by linarith : (0 : ℝ) < 1 - a) (by linarith : (0 : ℝ) < 1 + a)]
  unfold S_pairwise
  linarith [Real.log_le_log hpos hopp]

/-- CONTRACTION (general n), the honest lower bound. At every `n`, Schur + Klein
    give that `A ⊙ B` is a correlation matrix whose `S` sits at or above the
    chaos floor. This is NOT the contraction `S(A ⊙ B) ≤ S(A)` — that needs
    Oppenheim at general `n` — only the statement that the pointwise product
    lands back in the instrument's range and cannot read below the floor. -/
theorem neg_log_det_hadamard_nonneg {A B : Matrix n n ℝ}
    (hA : A.PosSemidef) (hB : B.PosSemidef) (hdA : IsUnitDiag A) (hdB : IsUnitDiag B)
    (hdet : 0 < (A ⊙ B).det) : 0 ≤ -Real.log (A ⊙ B).det :=
  neg_log_det_nonneg (hadamard_posSemidef hA hB) (hdA.hadamard hdB) hdet

/-! ## PSD determinant lower bounds — reusable stones toward general Oppenheim

Two determinant facts absent from Mathlib v4.14, proved here as standalone,
reusable results. They are the foundation the general Oppenheim induction rests
on; the induction itself (and hence the general contraction `S(A ⊙ B) ≤ S(A)`)
is NOT attempted here and remains open. -/

/-- `1 ≤ det (1 + Q)` for every real positive-semidefinite `Q`. Via the spectral
    theorem `Q = U · diag(λ) · Uᴴ` with `U` unitary, `1 + Q = U · diag(1+λ) · Uᴴ`,
    so `det(1 + Q) = ∏ᵢ (1 + λᵢ) ≥ 1` because every eigenvalue `λᵢ ≥ 0`. Absent
    from Mathlib v4.14. -/
theorem one_le_det_one_add_posSemidef {Q : Matrix n n ℝ} (hQ : Q.PosSemidef) :
    1 ≤ (1 + Q).det := by
  set U : Matrix n n ℝ := (hQ.1.eigenvectorUnitary : Matrix n n ℝ) with hUdef
  set D : Matrix n n ℝ := diagonal (RCLike.ofReal ∘ hQ.1.eigenvalues) with hDdef
  have hUV : U * star U = 1 := (mem_unitaryGroup_iff).mp (hQ.1.eigenvectorUnitary).2
  have hQspec : Q = U * D * star U := hQ.1.spectral_theorem
  have key : (1 : Matrix n n ℝ) + Q = U * (1 + D) * star U := by
    rw [mul_add, add_mul, mul_one, hUV, hQspec]
  have hdiag : (1 : Matrix n n ℝ) + D
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
  have hle := Finset.prod_le_prod (s := (Finset.univ : Finset n))
    (f := fun _ => (1 : ℝ)) (g := fun i => 1 + RCLike.ofReal (hQ.1.eigenvalues i))
    (fun i _ => zero_le_one)
    (fun i _ => by
      have hev : 0 ≤ hQ.1.eigenvalues i := hQ.eigenvalues_nonneg i
      simp only [RCLike.ofReal_real_eq_id, id_eq]; linarith)
  simpa using hle

/-- DETERMINANT MONOTONICITY on the cone: for positive-DEFINITE `X` and
    positive-semidefinite `P`, `det X ≤ det (X + P)`. Via the matrix determinant
    lemma (`det_add_mul`) with the Gram factor `P = MᴴM`:
    `det(X + P) = det X · det(1 + M X⁻¹ Mᴴ)`, where `M X⁻¹ Mᴴ` is PSD (congruence
    of the PSD inverse `X⁻¹`), so the second factor is `≥ 1` by
    `one_le_det_one_add_posSemidef`, and `det X > 0`. Absent from Mathlib v4.14. -/
theorem det_le_det_add_of_posDef_posSemidef {X P : Matrix n n ℝ}
    (hX : X.PosDef) (hP : P.PosSemidef) : X.det ≤ (X + P).det := by
  obtain ⟨M, hM⟩ := Matrix.posSemidef_iff_eq_transpose_mul_self.mp hP
  have hunit : IsUnit X.det := hX.det_pos.ne'.isUnit
  have hPSD : (M * X⁻¹ * Mᴴ).PosSemidef := hX.inv.posSemidef.mul_mul_conjTranspose_same M
  have hfac : (X + P).det = X.det * (1 + M * X⁻¹ * Mᴴ).det := by
    rw [hM, Matrix.det_add_mul _ _ hunit]
  rw [hfac]
  have h1 : 1 ≤ (1 + M * X⁻¹ * Mᴴ).det := one_le_det_one_add_posSemidef hPSD
  calc X.det = X.det * 1 := (mul_one _).symm
    _ ≤ X.det * (1 + M * X⁻¹ * Mᴴ).det := by
        exact mul_le_mul_of_nonneg_left h1 hX.det_pos.le

/-- The determinant of a real positive-semidefinite matrix is nonnegative — the
    product of its nonnegative eigenvalues. Absent from Mathlib v4.14. -/
theorem posSemidef_det_nonneg {X : Matrix n n ℝ} (hX : X.PosSemidef) : 0 ≤ X.det := by
  rw [hX.1.det_eq_prod_eigenvalues]
  apply Finset.prod_nonneg
  intro i _
  simpa using hX.eigenvalues_nonneg i

/-- A real positive-semidefinite matrix with positive determinant is positive
    definite. Via the Gram factorization `X = MᴴM`: `det X = det Mᴴ · det M`, so
    `det X > 0` forces `M` invertible, and then `xᴴ(MᴴM)x = ‖Mx‖² > 0` for `x ≠ 0`.
    (Mathlib v4.14 has no `posDef_of_eigenvalues_pos`.) -/
theorem posDef_of_posSemidef_det_pos {X : Matrix n n ℝ}
    (hX : X.PosSemidef) (hdet : 0 < X.det) : X.PosDef := by
  have hXinv : IsUnit X := (Matrix.isUnit_iff_isUnit_det X).2 hdet.ne'.isUnit
  have hinj : Function.Injective X.mulVec := Matrix.mulVec_injective_iff_isUnit.mpr hXinv
  refine ⟨hX.1, fun x hx => ?_⟩
  have hXx : X *ᵥ x ≠ 0 := fun h => hx (hinj (by rw [h, Matrix.mulVec_zero]))
  have hne : star x ⬝ᵥ X *ᵥ x ≠ 0 := by
    rw [Ne, hX.dotProduct_mulVec_zero_iff]; exact hXx
  exact lt_of_le_of_ne (hX.2 x) (Ne.symm hne)

/-- DETERMINANT MONOTONICITY, general form: for real positive-semidefinite `X`
    and `P`, `det X ≤ det (X + P)`. Extends `det_le_det_add_of_posDef_posSemidef`
    off the interior of the cone: if `X` is singular then `det X = 0 ≤ det(X+P)`
    (both PSD, so both determinants are `≥ 0` by `posSemidef_det_nonneg`);
    otherwise `X` is positive definite (`posDef_of_posSemidef_det_pos`). -/
theorem det_le_det_add_of_posSemidef {X P : Matrix n n ℝ}
    (hX : X.PosSemidef) (hP : P.PosSemidef) : X.det ≤ (X + P).det := by
  rcases lt_or_eq_of_le (posSemidef_det_nonneg hX) with hpos | hzero
  · exact det_le_det_add_of_posDef_posSemidef (posDef_of_posSemidef_det_pos hX hpos) hP
  · rw [← hzero]
    have : (X + P).PosSemidef := hX.add hP
    exact posSemidef_det_nonneg this

/-! ### Block-Hadamard compatibility — bookkeeping for the general Oppenheim induction

The one structural fact the (not-yet-mechanized) Schur-complement induction needs
about `⊙`: it acts blockwise. Proved here as a standalone reusable lemma. -/

/-- The Hadamard product acts blockwise on `2 × 2` block matrices: the block
    decomposition and `⊙` commute. Absent from Mathlib v4.14. -/
theorem hadamard_fromBlocks {α₁ α₂ β₁ β₂ : Type*}
    (A₁ A₂ : Matrix α₁ β₁ ℝ) (B₁ B₂ : Matrix α₁ β₂ ℝ)
    (C₁ C₂ : Matrix α₂ β₁ ℝ) (D₁ D₂ : Matrix α₂ β₂ ℝ) :
    (Matrix.fromBlocks A₁ B₁ C₁ D₁) ⊙ (Matrix.fromBlocks A₂ B₂ C₂ D₂)
      = Matrix.fromBlocks (A₁ ⊙ A₂) (B₁ ⊙ B₂) (C₁ ⊙ C₂) (D₁ ⊙ D₂) := by
  ext i j
  cases i <;> cases j <;> rfl

/-- The rank-one Hadamard identity: `(u uᵀ) ⊙ (v vᵀ) = (u∘v)(u∘v)ᵀ`. The step in
    the Schur-complement induction that turns the outer product of the Hadamard
    of two vectors into the Hadamard of their outer products. Over `ℝ`, `uᴴ = uᵀ`,
    so this is the real form of `(u∘v)(u∘v)ᴴ = (u uᴴ) ⊙ (v vᴴ)`. -/
theorem hadamard_vecMulVec {m : Type*} (u v : m → ℝ) :
    (vecMulVec u u) ⊙ (vecMulVec v v)
      = vecMulVec (fun i => u i * v i) (fun i => u i * v i) := by
  ext i j
  simp only [Matrix.hadamard_apply, Matrix.vecMulVec_apply]
  ring

/-- The Hadamard product commutes with reindexing/submatrix: taking a submatrix of
    a Hadamard product is the Hadamard product of the submatrices. Needed to move
    the induction's `Fin (n+1)` problem to `Fin 1 ⊕ Fin n` and back. Absent from
    Mathlib v4.14. -/
theorem submatrix_hadamard {p₁ p₂ q₁ q₂ : Type*} (A B : Matrix q₁ q₂ ℝ)
    (f : p₁ → q₁) (g : p₂ → q₂) :
    (A ⊙ B).submatrix f g = A.submatrix f g ⊙ B.submatrix f g := by
  ext i j
  simp [Matrix.hadamard_apply, Matrix.submatrix_apply]

omit [DecidableEq n] in
/-- An outer product `u uᵀ` (`= vecMulVec u u`) is positive semidefinite: it is the
    Gram matrix `(col u)(col u)ᴴ`. The rank-one PSD summand of the block Schur
    identity below. -/
theorem posSemidef_vecMulVec (u : n → ℝ) : (vecMulVec u u).PosSemidef := by
  have h : vecMulVec u u = Matrix.col Unit u * (Matrix.col Unit u)ᴴ := by
    ext i j
    simp [Matrix.vecMulVec_apply, Matrix.mul_apply, Matrix.conjTranspose_apply,
      Matrix.col_apply]
  rw [h]
  exact Matrix.posSemidef_self_mul_conjTranspose _

/-- THE BLOCK SCHUR-HADAMARD IDENTITY — the mathematical heart of the Oppenheim
    induction. When a `(1+n)×(1+n)` PSD matrix is split off its first coordinate
    with pivot `α`, off-diagonal column `u`, block `A₁`, and its unit-diagonal PSD
    partner is split with pivot `1`, off-diagonal `v`, block `B₁`, the Schur
    complement of `A ⊙ B` (left side) decomposes as `C₁ ⊙ B₁ + α⁻¹ (u uᵀ) ⊙ (B₁ − v vᵀ)`,
    where `C₁ = A₁ − α⁻¹ u uᵀ` is the Schur complement of `A`. Both summands are PSD
    (`C₁` PSD, `B₁` PSD; `u uᵀ` PSD, `B₁ − v vᵀ` = Schur complement of `B` PSD), which
    is what lets determinant monotonicity push the induction through. Proved purely
    entrywise — no block or inverse machinery. -/
theorem schur_hadamard_identity {m : Type*} (α : ℝ) (u v : m → ℝ)
    (A₁ B₁ : Matrix m m ℝ) :
    A₁ ⊙ B₁ - α⁻¹ • vecMulVec (fun i => u i * v i) (fun i => u i * v i)
      = (A₁ - α⁻¹ • vecMulVec u u) ⊙ B₁
        + α⁻¹ • ((vecMulVec u u) ⊙ (B₁ - vecMulVec v v)) := by
  ext i j
  simp only [Matrix.sub_apply, Matrix.add_apply, Matrix.smul_apply, Matrix.hadamard_apply,
    Matrix.vecMulVec_apply, smul_eq_mul]
  ring

end CIRISOntology.Core
