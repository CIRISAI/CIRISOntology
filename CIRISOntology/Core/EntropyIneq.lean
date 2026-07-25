/-
CIRISOntology.Core.EntropyIneq — quantum entropy inequalities, from two tricks.

The temporal re-attack (TEMPORAL_ATTACK_PREREG.md, phase A) found that
causality forbids the Bell-type temporal edge, via one inequality: Araki–Lieb.
This file mechanizes the ladder to it. Every rung is one of two techniques
this repository already owns: the `log x ≤ x − 1` pointwise trick (Gibbs,
Jensen, pinching) and the determinant–polynomial multiset bridge (spectra
pinned through `det(x•1 − A)` and `Polynomial.funext`).

  * `vnEntropy_conj_unitary`, `vnEntropy_reindex` — the spectrum, hence the
    entropy, is blind to unitary conjugation and to relabeling. Bridge.
  * `mul_log_jensen` — finite Jensen for `t·log t`: the convex combination
    never exceeds the mixture term-wise. The `log x ≤ x − 1` trick, again.
  * `vnEntropy_le_entropy_diagRe` — THE PINCHING BOUND: von Neumann entropy
    is at most the classical entropy of the diagonal, in any basis. The
    diagonal is a doubly-stochastic mix of the spectrum (Schur–Horn, from
    unitarity alone), and Jensen closes it.
  * `entropy_grouping₂` — two-slot classical subadditivity (the 3-slot
    version is `Core.Share.entropy_grouping`; same Gibbs proof).

Later stages (this file, below): quantum subadditivity by pinching in the
product eigenbasis of the marginals; purification; complementary entropies
by Weinstein–Aronszajn; Araki–Lieb; and the causal past-view bound that
turns the phase-A discovery into a machine-checked theorem.

Mathlib survey: `Matrix.det_one_add_mul_comm` (Weinstein–Aronszajn) carries
the complementary-spectrum step; `Matrix.det_submatrix_equiv_self` the
relabeling; `Matrix.kroneckerMap` / `Matrix.blockDiagonal` the tensor
bookkeeping; the rest is `Core.Share*` machinery. No gaps to port.
-/
import CIRISOntology.Core.ShareK
import Mathlib.Data.Matrix.Kronecker

namespace CIRISOntology.Core

open Matrix
open scoped BigOperators ComplexOrder Kronecker

variable {𝕜 : Type*} [RCLike 𝕜]

/-! ### Spectrum blindness: unitary conjugation and relabeling -/

/-- Entropies agree when the two `det(x•1 − ·)` products agree pointwise:
    the multiset bridge, packaged for reuse. -/
lemma vnEntropy_congr_of_det {m m' : Type*} [Fintype m] [DecidableEq m]
    [Fintype m'] [DecidableEq m']
    {A : Matrix m m 𝕜} {B : Matrix m' m' 𝕜}
    (hA : A.IsHermitian) (hB : B.IsHermitian)
    (h : ∀ x : 𝕜, (x • (1 : Matrix m m 𝕜) - A).det
        = (x • (1 : Matrix m' m' 𝕜) - B).det) :
    vnEntropy A = vnEntropy B := by
  rw [vnEntropy_of_isHermitian hA, vnEntropy_of_isHermitian hB]
  refine entropy_congr_multiset ?_
  have hmul := multiset_eq_of_prod_linear (𝕜 := 𝕜)
    (fun i => (hA.eigenvalues i : 𝕜)) (fun j => (hB.eigenvalues j : 𝕜))
    (fun x => by rw [← det_smul_one_sub hA x, ← det_smul_one_sub hB x]; exact h x)
  have h' : (Finset.univ.val.map hA.eigenvalues).map ((↑) : ℝ → 𝕜)
      = (Finset.univ.val.map hB.eigenvalues).map ((↑) : ℝ → 𝕜) := by
    rw [Multiset.map_map, Multiset.map_map]
    exact hmul
  exact Multiset.map_injective (RCLike.ofReal_injective (K := 𝕜)) h'

/-- The entropy is blind to unitary conjugation. -/
theorem vnEntropy_conj_unitary {m : Type*} [Fintype m] [DecidableEq m]
    {A : Matrix m m 𝕜} (hA : A.IsHermitian) (U : Matrix.unitaryGroup m 𝕜) :
    vnEntropy ((U : Matrix m m 𝕜) * A * star (U : Matrix m m 𝕜)) = vnEntropy A := by
  have hU : (U : Matrix m m 𝕜) * star (U : Matrix m m 𝕜) = 1 :=
    mem_unitaryGroup_iff.mp U.2
  have hA' : ((U : Matrix m m 𝕜) * A * star (U : Matrix m m 𝕜)).IsHermitian := by
    rw [Matrix.IsHermitian]
    simp only [Matrix.conjTranspose_mul, Matrix.conjTranspose_conjTranspose,
      hA.eq, Matrix.mul_assoc, Matrix.star_eq_conjTranspose]
  refine vnEntropy_congr_of_det hA' hA fun x => ?_
  have key : x • (1 : Matrix m m 𝕜) - (U : Matrix m m 𝕜) * A * star (U : Matrix m m 𝕜)
      = (U : Matrix m m 𝕜) * (x • (1 : Matrix m m 𝕜) - A) * star (U : Matrix m m 𝕜) := by
    rw [Matrix.mul_sub, Matrix.sub_mul]
    congr 1
    rw [Matrix.mul_smul, Matrix.mul_one, Matrix.smul_mul, hU]
  rw [key, Matrix.det_mul, Matrix.det_mul, mul_right_comm, ← Matrix.det_mul, hU,
    Matrix.det_one, one_mul]

/-- The entropy is blind to relabeling the index type. -/
theorem vnEntropy_reindex {m m' : Type*} [Fintype m] [DecidableEq m]
    [Fintype m'] [DecidableEq m'] (e : m' ≃ m)
    {A : Matrix m m 𝕜} (hA : A.IsHermitian) :
    vnEntropy (A.submatrix e e) = vnEntropy A := by
  have hA' : (A.submatrix e e).IsHermitian := by
    rw [Matrix.IsHermitian, Matrix.conjTranspose_submatrix, hA.eq]
  refine vnEntropy_congr_of_det hA' hA fun x => ?_
  have key : x • (1 : Matrix m' m' 𝕜) - A.submatrix e e
      = (x • (1 : Matrix m m 𝕜) - A).submatrix e e := by
    ext i j
    rcases eq_or_ne i j with rfl | hij
    · simp
    · simp [Matrix.one_apply_ne hij, Matrix.one_apply_ne (fun h => hij (e.injective h))]
  rw [key, Matrix.det_submatrix_equiv_self]

/-! ### Finite Jensen for t·log t -/

/-- Convexity of `t ↦ t·log t` against finite weights, by the
    `log x ≤ x − 1` trick — no calculus. -/
lemma mul_log_jensen {ι : Type*} [Fintype ι] (w x : ι → ℝ)
    (hw : ∀ i, 0 ≤ w i) (hx : ∀ i, 0 ≤ x i) (hw1 : ∑ i, w i = 1) :
    (∑ i, w i * x i) * Real.log (∑ i, w i * x i)
      ≤ ∑ i, w i * (x i * Real.log (x i)) := by
  set c := ∑ i, w i * x i with hc
  have hc0 : 0 ≤ c := Finset.sum_nonneg fun i _ => mul_nonneg (hw i) (hx i)
  rcases hc0.eq_or_lt with h0 | h0
  · -- zero mixture: every summand vanishes
    have hz : ∀ i ∈ Finset.univ, w i * x i = 0 :=
      (Finset.sum_eq_zero_iff_of_nonneg
        fun i _ => mul_nonneg (hw i) (hx i)).mp h0.symm
    rw [← h0]
    simp only [zero_mul]
    refine Finset.sum_nonneg fun i _ => ?_
    rcases mul_eq_zero.mp (hz i (Finset.mem_univ i)) with h | h
    · rw [h, zero_mul]
    · rw [h]
      simp
  · -- positive mixture: per-term Gibbs
    have key : ∀ i, w i * x i - w i * c
        ≤ w i * (x i * Real.log (x i)) - w i * x i * Real.log c := by
      intro i
      rcases (hx i).eq_or_lt with h | h
      · rw [← h]
        have h1 : 0 ≤ w i * c := mul_nonneg (hw i) h0.le
        simp only [mul_zero, zero_mul, zero_sub, sub_zero]
        linarith
      · have hlog : Real.log (c / x i) ≤ c / x i - 1 :=
          Real.log_le_sub_one_of_pos (div_pos h0 h)
        rw [Real.log_div h0.ne' h.ne'] at hlog
        have h2 := mul_le_mul_of_nonneg_left hlog
          (mul_nonneg (hw i) h.le)
        have h3 : w i * x i * (c / x i - 1) = w i * c - w i * x i := by
          field_simp
          ring
        nlinarith [h2, h3]
    have hsum := Finset.sum_le_sum fun i (_ : i ∈ Finset.univ) => key i
    have e1 : ∑ i, (w i * x i - w i * c) = 0 := by
      rw [Finset.sum_sub_distrib, ← hc, ← Finset.sum_mul, hw1, one_mul, sub_self]
    have e2 : ∑ i, (w i * (x i * Real.log (x i)) - w i * x i * Real.log c)
        = (∑ i, w i * (x i * Real.log (x i))) - c * Real.log c := by
      rw [Finset.sum_sub_distrib]
      congr 1
      rw [← Finset.sum_mul, ← hc]
    rw [e1, e2] at hsum
    linarith

/-! ### The pinching bound -/

/-- The real diagonal of an operator. -/
noncomputable def diagRe {m : Type*} (ρ : Matrix m m 𝕜) : m → ℝ :=
  fun i => RCLike.re (ρ i i)

/-- THE PINCHING BOUND: the von Neumann entropy of a positive semidefinite
    operator is at most the classical entropy of its diagonal. The diagonal
    is a doubly-stochastic mixture of the spectrum — Schur–Horn from
    unitarity alone — and Jensen does the rest. -/
theorem vnEntropy_le_entropy_diagRe {m : Type*} [Fintype m] [DecidableEq m]
    {ρ : Matrix m m 𝕜} (hρ : ρ.PosSemidef) :
    vnEntropy ρ ≤ entropy (diagRe ρ) := by
  have hH := hρ.1
  set U : Matrix m m 𝕜 := (hH.eigenvectorUnitary : Matrix m m 𝕜) with hU_def
  set lam : m → ℝ := hH.eigenvalues with hlam_def
  set D : m → m → ℝ := fun i j => ‖U i j‖ ^ 2 with hD_def
  have hUU : U * star U = 1 := mem_unitaryGroup_iff.mp hH.eigenvectorUnitary.2
  have hUU' : star U * U = 1 := mem_unitaryGroup_iff'.mp hH.eigenvectorUnitary.2
  have hDnn : ∀ i j, 0 ≤ D i j := fun i j => sq_nonneg _
  have hrow : ∀ i, ∑ j, D i j = 1 := by
    intro i
    have := congrArg (fun M => RCLike.re (M i i)) hUU
    simp only [Matrix.mul_apply, Matrix.one_apply_eq, Matrix.star_apply,
      RCLike.star_def] at this
    rw [map_sum] at this
    calc ∑ j, D i j = ∑ j, RCLike.re (U i j * (starRingEnd 𝕜) (U i j)) := by
          refine Finset.sum_congr rfl fun j _ => ?_
          rw [RCLike.mul_conj, ← RCLike.ofReal_pow, RCLike.ofReal_re]
      _ = 1 := by rw [this]; simp
  have hcol : ∀ j, ∑ i, D i j = 1 := by
    intro j
    have := congrArg (fun M => RCLike.re (M j j)) hUU'
    simp only [Matrix.mul_apply, Matrix.one_apply_eq, Matrix.star_apply,
      RCLike.star_def] at this
    rw [map_sum] at this
    calc ∑ i, D i j = ∑ i, RCLike.re ((starRingEnd 𝕜) (U i j) * U i j) := by
          refine Finset.sum_congr rfl fun i _ => ?_
          rw [RCLike.conj_mul, ← RCLike.ofReal_pow, RCLike.ofReal_re]
      _ = 1 := by rw [this]; simp
  have hdiag : ∀ i, diagRe ρ i = ∑ j, D i j * lam j := by
    intro i
    have h1 : ρ i i = ∑ j, U i j * (lam j : 𝕜) * (starRingEnd 𝕜) (U i j) := by
      conv_lhs => rw [hH.spectral_theorem]
      rw [Matrix.mul_apply]
      refine Finset.sum_congr rfl fun j _ => ?_
      rw [Matrix.mul_apply, Finset.sum_eq_single j]
      · simp only [Matrix.diagonal_apply_eq, Function.comp_apply,
          Matrix.star_apply, RCLike.star_def]
      · intro b _ hb
        simp [Matrix.diagonal_apply_ne _ hb]
      · intro h
        exact absurd (Finset.mem_univ j) h
    show RCLike.re (ρ i i) = _
    rw [h1, map_sum]
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [mul_right_comm, RCLike.mul_conj, ← RCLike.ofReal_pow, ← RCLike.ofReal_mul,
      RCLike.ofReal_re]
  have hlam0 : ∀ j, 0 ≤ lam j := fun j => hρ.eigenvalues_nonneg j
  rw [vnEntropy_of_isHermitian hH]
  unfold entropy
  have main : ∀ i, (∑ j, D i j * lam j) * Real.log (∑ j, D i j * lam j)
      ≤ ∑ j, D i j * (lam j * Real.log (lam j)) := fun i =>
    mul_log_jensen (D i) lam (hDnn i) hlam0 (hrow i)
  have hswap : ∑ i, ∑ j, D i j * (lam j * Real.log (lam j))
      = ∑ j, lam j * Real.log (lam j) := by
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [← Finset.sum_mul, hcol j, one_mul]
  have hsum := Finset.sum_le_sum fun i (_ : i ∈ Finset.univ) => main i
  rw [hswap] at hsum
  have hrw : ∑ i, diagRe ρ i * Real.log (diagRe ρ i)
      = ∑ i, (∑ j, D i j * lam j) * Real.log (∑ j, D i j * lam j) := by
    refine Finset.sum_congr rfl fun i _ => ?_
    rw [hdiag i]
  linarith [hsum, hrw.ge, hrw.le]

/-! ### Two-slot classical subadditivity -/

/-- Two-slot grouping subadditivity: the 3-slot version is
    `entropy_grouping`; same Gibbs-against-own-marginals proof. -/
theorem entropy_grouping₂ {α β : Type*} [Fintype α] [Fintype β]
    {q : α × β → ℝ} (hq : IsProb q) :
    entropy q ≤ entropy (fun a => ∑ b, q (a, b))
      + entropy (fun b => ∑ a, q (a, b)) := by
  obtain ⟨h0, h1⟩ := hq
  set mA : α → ℝ := fun a => ∑ b, q (a, b) with hmA
  set mB : β → ℝ := fun b => ∑ a, q (a, b) with hmB
  have hA0 : ∀ a, 0 ≤ mA a := fun a => Finset.sum_nonneg fun b _ => h0 (a, b)
  have hB0 : ∀ b, 0 ≤ mB b := fun b => Finset.sum_nonneg fun a _ => h0 (a, b)
  have hleA : ∀ a b, q (a, b) ≤ mA a := fun a b =>
    Finset.single_le_sum (fun b' _ => h0 (a, b')) (Finset.mem_univ b)
  have hleB : ∀ a b, q (a, b) ≤ mB b := fun a b =>
    Finset.single_le_sum (fun a' _ => h0 (a', b)) (Finset.mem_univ a)
  set r : α × β → ℝ := fun t => mA t.1 * mB t.2 with hr
  have hr0 : ∀ t, 0 ≤ r t := fun t => mul_nonneg (hA0 t.1) (hB0 t.2)
  have habs : ∀ t, 0 < q t → 0 < r t := by
    rintro ⟨a, b⟩ hpos
    exact mul_pos (lt_of_lt_of_le hpos (hleA a b)) (lt_of_lt_of_le hpos (hleB a b))
  have hsA : ∑ a, mA a = 1 := by
    rw [hmA]
    rw [← h1, Fintype.sum_prod_type]
  have hr1 : ∑ t, r t = 1 := by
    rw [hr]
    rw [Fintype.sum_prod_type]
    calc ∑ a, ∑ b, mA a * mB b = ∑ a, mA a * ∑ b, mB b := by
          exact Finset.sum_congr rfl fun a _ => (Finset.mul_sum _ _ _).symm
      _ = ∑ a, mA a * 1 := by
          congr 1
          funext a
          congr 1
          rw [hmB, ← h1, Fintype.sum_prod_type, Finset.sum_comm]
      _ = 1 := by simp [hsA]
  have key : ∑ t, q t * Real.log (r t) - ∑ t, q t * Real.log (q t) ≤ 0 := by
    have h2 := Finset.sum_le_sum fun t (_ : t ∈ Finset.univ) =>
      mul_log_sub_le (h0 t) (hr0 t) (habs t)
    have h3 : ∑ t, (r t - q t) = 0 := by
      rw [Finset.sum_sub_distrib, hr1, h1, sub_self]
    have h4 : ∑ t, (q t * Real.log (r t) - q t * Real.log (q t))
        = ∑ t, q t * Real.log (r t) - ∑ t, q t * Real.log (q t) :=
      Finset.sum_sub_distrib
    linarith
  have hsplit : ∑ t : α × β, q t * Real.log (r t)
      = (∑ t : α × β, q t * Real.log (mA t.1))
        + ∑ t : α × β, q t * Real.log (mB t.2) := by
    rw [← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl ?_
    rintro ⟨a, b⟩ -
    rcases (h0 (a, b)).eq_or_lt with h | h
    · rw [← h]
      simp
    · have h1' : 0 < mA a := lt_of_lt_of_le h (hleA a b)
      have h2' : 0 < mB b := lt_of_lt_of_le h (hleB a b)
      show q (a, b) * Real.log (mA a * mB b) = _
      rw [Real.log_mul h1'.ne' h2'.ne']
      ring
  have hmAsum : ∑ t : α × β, q t * Real.log (mA t.1)
      = ∑ a, mA a * Real.log (mA a) := by
    rw [Fintype.sum_prod_type]
    refine Finset.sum_congr rfl fun a _ => ?_
    show ∑ b, q (a, b) * Real.log (mA a) = mA a * Real.log (mA a)
    rw [← Finset.sum_mul]
  have hmBsum : ∑ t : α × β, q t * Real.log (mB t.2)
      = ∑ b, mB b * Real.log (mB b) := by
    rw [Fintype.sum_prod_type, Finset.sum_comm]
    refine Finset.sum_congr rfl fun b _ => ?_
    show ∑ a, q (a, b) * Real.log (mB b) = mB b * Real.log (mB b)
    rw [← Finset.sum_mul]
  unfold entropy
  have := hsplit
  rw [hmAsum, hmBsum] at this
  linarith [key, this]

/-! ### Bipartite partial traces -/

/-- Trace out the right factor. -/
noncomputable def ptrR {a b : Type*} [Fintype b]
    (ρ : Matrix (a × b) (a × b) 𝕜) : Matrix a a 𝕜 :=
  Matrix.of fun x x' => ∑ y, ρ (x, y) (x', y)

/-- Trace out the left factor. -/
noncomputable def ptrL {a b : Type*} [Fintype a]
    (ρ : Matrix (a × b) (a × b) 𝕜) : Matrix b b 𝕜 :=
  Matrix.of fun y y' => ∑ x, ρ (x, y) (x, y')

lemma ptrR_isHermitian {a b : Type*} [Fintype b]
    {ρ : Matrix (a × b) (a × b) 𝕜} (h : ρ.IsHermitian) :
    (ptrR ρ).IsHermitian := by
  ext x x'
  simp only [Matrix.conjTranspose_apply, ptrR, Matrix.of_apply, star_sum]
  refine Finset.sum_congr rfl fun y _ => ?_
  rw [← Matrix.conjTranspose_apply, h.eq]

lemma ptrL_isHermitian {a b : Type*} [Fintype a]
    {ρ : Matrix (a × b) (a × b) 𝕜} (h : ρ.IsHermitian) :
    (ptrL ρ).IsHermitian := by
  ext y y'
  simp only [Matrix.conjTranspose_apply, ptrL, Matrix.of_apply, star_sum]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [← Matrix.conjTranspose_apply, h.eq]

lemma trace_ptrR {a b : Type*} [Fintype a] [Fintype b]
    (ρ : Matrix (a × b) (a × b) 𝕜) : (ptrR ρ).trace = ρ.trace := by
  simp only [Matrix.trace, Matrix.diag, ptrR, Matrix.of_apply]
  rw [Fintype.sum_prod_type]

lemma trace_ptrL {a b : Type*} [Fintype a] [Fintype b]
    (ρ : Matrix (a × b) (a × b) 𝕜) : (ptrL ρ).trace = ρ.trace := by
  simp only [Matrix.trace, Matrix.diag, ptrL, Matrix.of_apply]
  rw [Fintype.sum_prod_type, Finset.sum_comm]

/-- Partial trace preserves positive semidefiniteness: if `ρ = Sᴴ·S`, the
    traced operator is `Cᴴ·C` for the reshaped factor. No quadratic forms. -/
lemma ptrR_posSemidef {a b : Type*} [Fintype a] [Fintype b]
    [DecidableEq a] [DecidableEq b]
    {ρ : Matrix (a × b) (a × b) 𝕜} (h : ρ.PosSemidef) :
    (ptrR ρ).PosSemidef := by
  have hfac : ρ = h.sqrt ᴴ * h.sqrt := by
    rw [h.posSemidef_sqrt.1.eq, h.sqrt_mul_self]
  set C : Matrix ((a × b) × b) a 𝕜 :=
    Matrix.of fun ky x => h.sqrt ky.1 (x, ky.2) with hC
  have hCC : ptrR ρ = Cᴴ * C := by
    ext x x'
    simp only [ptrR, Matrix.of_apply, Matrix.mul_apply,
      Matrix.conjTranspose_apply, hfac, hC]
    rw [Fintype.sum_prod_type]
    exact Finset.sum_comm
  rw [hCC]
  exact Matrix.posSemidef_conjTranspose_mul_self C

lemma ptrL_posSemidef {a b : Type*} [Fintype a] [Fintype b]
    [DecidableEq a] [DecidableEq b]
    {ρ : Matrix (a × b) (a × b) 𝕜} (h : ρ.PosSemidef) :
    (ptrL ρ).PosSemidef := by
  have hfac : ρ = h.sqrt ᴴ * h.sqrt := by
    rw [h.posSemidef_sqrt.1.eq, h.sqrt_mul_self]
  set C : Matrix ((a × b) × a) b 𝕜 :=
    Matrix.of fun kx y => h.sqrt kx.1 (kx.2, y) with hC
  have hCC : ptrL ρ = Cᴴ * C := by
    ext y y'
    simp only [ptrL, Matrix.of_apply, Matrix.mul_apply,
      Matrix.conjTranspose_apply, hfac, hC]
    rw [Fintype.sum_prod_type]
    exact Finset.sum_comm
  rw [hCC]
  exact Matrix.posSemidef_conjTranspose_mul_self C

lemma isDensity_ptrR {a b : Type*} [Fintype a] [Fintype b]
    [DecidableEq a] [DecidableEq b]
    {ρ : Matrix (a × b) (a × b) 𝕜} (h : IsDensity ρ) : IsDensity (ptrR ρ) :=
  ⟨ptrR_posSemidef h.1, by rw [trace_ptrR]; exact h.2⟩

lemma isDensity_ptrL {a b : Type*} [Fintype a] [Fintype b]
    [DecidableEq a] [DecidableEq b]
    {ρ : Matrix (a × b) (a × b) 𝕜} (h : IsDensity ρ) : IsDensity (ptrL ρ) :=
  ⟨ptrL_posSemidef h.1, by rw [trace_ptrL]; exact h.2⟩

/-! ### Conjugation bookkeeping -/

lemma kronecker_conjTranspose' {l m n p : Type*}
    (A : Matrix l m 𝕜) (B : Matrix n p 𝕜) :
    (A ⊗ₖ B)ᴴ = Aᴴ ⊗ₖ Bᴴ := by
  ext ⟨i, j⟩ ⟨k, l'⟩
  simp [Matrix.conjTranspose_apply, Matrix.kroneckerMap_apply, star_mul']

lemma isDensity_conj_unitary {m : Type*} [Fintype m] [DecidableEq m]
    {ρ : Matrix m m 𝕜} (h : IsDensity ρ) {U : Matrix m m 𝕜}
    (hU : U * star U = 1) :
    IsDensity (star U * ρ * U) := by
  constructor
  · have : (star U * ρ * (star U)ᴴ).PosSemidef :=
      h.1.mul_mul_conjTranspose_same (star U)
    simpa [Matrix.star_eq_conjTranspose] using this
  · rw [Matrix.trace_mul_cycle, hU, Matrix.one_mul, h.2]

lemma isProb_diagRe {m : Type*} [Fintype m] [DecidableEq m]
    {ρ : Matrix m m 𝕜} (h : IsDensity ρ) : IsProb (diagRe ρ) := by
  constructor
  · intro i
    have hq : star (Pi.single i 1 : m → 𝕜) ⬝ᵥ ρ *ᵥ (Pi.single i 1) = ρ i i := by
      simp [Matrix.dotProduct, Matrix.mulVec, Pi.single_apply, apply_ite,
        Finset.mul_sum, mul_ite, ite_mul, mul_comm]
    have h0 : (0 : 𝕜) ≤ ρ i i := by
      rw [← hq]
      exact h.1.2 _
    exact (RCLike.nonneg_iff.mp h0).1
  · have : ∑ i, diagRe ρ i = RCLike.re ρ.trace := by
      unfold diagRe
      rw [← map_sum]
      rfl
    rw [this, h.2]
    simp

/-- The entry of a product-conjugated operator, fully expanded, in the
    simp-natural nesting order (primed indices outermost). -/
private lemma conj_kron_entry {a b : Type*} [Fintype a] [Fintype b]
    (ρ : Matrix (a × b) (a × b) 𝕜) (X : Matrix a a 𝕜) (Y : Matrix b b 𝕜)
    (p q : a × b) : ((X ⊗ₖ Y) * ρ * (X ⊗ₖ Y)ᴴ) p q
      = ∑ u', ∑ v', ∑ u, ∑ v, X p.1 u * Y p.2 v * ρ (u, v) (u', v')
          * (starRingEnd 𝕜) (X q.1 u') * (starRingEnd 𝕜) (Y q.2 v') := by
  simp only [Matrix.mul_apply, Matrix.conjTranspose_apply,
    Matrix.kroneckerMap_apply, Finset.sum_mul, RCLike.star_def, star_mul',
    Fintype.sum_prod_type]
  refine Finset.sum_congr rfl fun u' _ => Finset.sum_congr rfl fun v' _ =>
    Finset.sum_congr rfl fun u _ => Finset.sum_congr rfl fun v _ => by ring

/-- Partial-trace covariance under a product conjugation with a unitary
    right factor: the right factor collapses out. -/
lemma ptrR_conj_kronecker {a b : Type*} [Fintype a] [Fintype b] [DecidableEq b]
    (ρ : Matrix (a × b) (a × b) 𝕜) (X : Matrix a a 𝕜) {Y : Matrix b b 𝕜}
    (hY : Yᴴ * Y = 1) :
    ptrR ((X ⊗ₖ Y) * ρ * (X ⊗ₖ Y)ᴴ) = X * ptrR ρ * Xᴴ := by
  have hYe : ∀ v' v : b, (∑ y, (starRingEnd 𝕜) (Y y v') * Y y v)
      = if v' = v then 1 else 0 := by
    intro v' v
    have := congrFun (congrFun hY v') v
    simpa [Matrix.mul_apply, Matrix.conjTranspose_apply, Matrix.one_apply,
      RCLike.star_def] using this
  ext x x'
  show (∑ y, ((X ⊗ₖ Y) * ρ * (X ⊗ₖ Y)ᴴ) (x, y) (x', y)) = _
  calc ∑ y, ((X ⊗ₖ Y) * ρ * (X ⊗ₖ Y)ᴴ) (x, y) (x', y)
      = ∑ u', ∑ v', ∑ u,
          X x u * ρ (u, v') (u', v') * (starRingEnd 𝕜) (X x' u') := by
        rw [Finset.sum_congr rfl fun y (_ : y ∈ Finset.univ) =>
          conj_kron_entry ρ X Y (x, y) (x', y)]
        rw [Finset.sum_comm]
        refine Finset.sum_congr rfl fun u' _ => ?_
        rw [Finset.sum_comm]
        refine Finset.sum_congr rfl fun v' _ => ?_
        rw [Finset.sum_comm]
        refine Finset.sum_congr rfl fun u _ => ?_
        rw [Finset.sum_comm]
        rw [Finset.sum_congr rfl fun v (_ : v ∈ Finset.univ) => show
          (∑ y, X x u * Y y v * ρ (u, v) (u', v') * (starRingEnd 𝕜) (X x' u')
              * (starRingEnd 𝕜) (Y y v'))
            = (X x u * ρ (u, v) (u', v') * (starRingEnd 𝕜) (X x' u'))
                * (if v' = v then 1 else 0) from by
          rw [← hYe v' v, Finset.mul_sum]
          exact Finset.sum_congr rfl fun y _ => by ring]
        simp only [mul_ite, mul_one, mul_zero]
        rw [Finset.sum_ite_eq Finset.univ v'
          (fun v => X x u * ρ (u, v) (u', v') * (starRingEnd 𝕜) (X x' u'))]
        simp
    _ = (X * ptrR ρ * Xᴴ) x x' := by
        simp only [Matrix.mul_apply, Matrix.conjTranspose_apply, ptrR,
          Matrix.of_apply, Finset.sum_mul, Finset.mul_sum, RCLike.star_def]
        refine Finset.sum_congr rfl fun u' _ => ?_
        rw [Finset.sum_comm]

/-- Mirror covariance: a unitary left factor collapses out. -/
lemma ptrL_conj_kronecker {a b : Type*} [Fintype a] [Fintype b] [DecidableEq a]
    (ρ : Matrix (a × b) (a × b) 𝕜) {X : Matrix a a 𝕜} (Y : Matrix b b 𝕜)
    (hX : Xᴴ * X = 1) :
    ptrL ((X ⊗ₖ Y) * ρ * (X ⊗ₖ Y)ᴴ) = Y * ptrL ρ * Yᴴ := by
  have hXe : ∀ u' u : a, (∑ x, (starRingEnd 𝕜) (X x u') * X x u)
      = if u' = u then 1 else 0 := by
    intro u' u
    have := congrFun (congrFun hX u') u
    simpa [Matrix.mul_apply, Matrix.conjTranspose_apply, Matrix.one_apply,
      RCLike.star_def] using this
  ext y y'
  show (∑ x, ((X ⊗ₖ Y) * ρ * (X ⊗ₖ Y)ᴴ) (x, y) (x, y')) = _
  calc ∑ x, ((X ⊗ₖ Y) * ρ * (X ⊗ₖ Y)ᴴ) (x, y) (x, y')
      = ∑ u', ∑ v', ∑ v,
          Y y v * ρ (u', v) (u', v') * (starRingEnd 𝕜) (Y y' v') := by
        rw [Finset.sum_congr rfl fun x (_ : x ∈ Finset.univ) =>
          conj_kron_entry ρ X Y (x, y) (x, y')]
        rw [Finset.sum_comm]
        refine Finset.sum_congr rfl fun u' _ => ?_
        rw [Finset.sum_comm]
        refine Finset.sum_congr rfl fun v' _ => ?_
        rw [Finset.sum_comm]
        rw [Finset.sum_congr rfl fun u (_ : u ∈ Finset.univ) => Finset.sum_comm]
        rw [Finset.sum_congr rfl fun u (_ : u ∈ Finset.univ) =>
          Finset.sum_congr rfl fun v (_ : v ∈ Finset.univ) => show
            (∑ x, X x u * Y y v * ρ (u, v) (u', v') * (starRingEnd 𝕜) (X x u')
                * (starRingEnd 𝕜) (Y y' v'))
              = (Y y v * ρ (u, v) (u', v') * (starRingEnd 𝕜) (Y y' v'))
                  * (if u' = u then 1 else 0) from by
            rw [← hXe u' u, Finset.mul_sum]
            exact Finset.sum_congr rfl fun x _ => by ring]
        rw [Finset.sum_congr rfl fun u (_ : u ∈ Finset.univ) =>
          (Finset.sum_mul Finset.univ
            (fun v => Y y v * ρ (u, v) (u', v') * (starRingEnd 𝕜) (Y y' v'))
            (if u' = u then 1 else 0)).symm]
        simp only [mul_ite, mul_one, mul_zero]
        rw [Finset.sum_ite_eq Finset.univ u'
          (fun u => ∑ v, Y y v * ρ (u, v) (u', v') * (starRingEnd 𝕜) (Y y' v'))]
        simp
    _ = (Y * ptrL ρ * Yᴴ) y y' := by
        simp only [Matrix.mul_apply, Matrix.conjTranspose_apply, ptrL,
          Matrix.of_apply, Finset.sum_mul, Finset.mul_sum, RCLike.star_def]
        rw [Finset.sum_comm]
        refine Finset.sum_congr rfl fun u' _ => ?_
        rw [Finset.sum_comm]

/-! ### Quantum subadditivity -/

lemma diagRe_ptrR {a b : Type*} [Fintype b]
    (ρ : Matrix (a × b) (a × b) 𝕜) (x : a) :
    diagRe (ptrR ρ) x = ∑ y, diagRe ρ (x, y) := by
  unfold diagRe ptrR
  simp [map_sum]

lemma diagRe_ptrL {a b : Type*} [Fintype a]
    (ρ : Matrix (a × b) (a × b) 𝕜) (y : b) :
    diagRe (ptrL ρ) y = ∑ x, diagRe ρ (x, y) := by
  unfold diagRe ptrL
  simp [map_sum]

lemma diagRe_diagonal {m : Type*} [Fintype m] [DecidableEq m] (lam : m → ℝ) :
    diagRe (Matrix.diagonal (RCLike.ofReal ∘ lam) : Matrix m m 𝕜) = lam := by
  funext i
  simp [diagRe]

/-- QUANTUM SUBADDITIVITY: pinch in the product eigenbasis of the two
    marginals; the pinched classical state has the marginal SPECTRA as its
    marginals, and classical grouping subadditivity closes it. -/
theorem vnEntropy_subadd {a b : Type*} [Fintype a] [Fintype b]
    [DecidableEq a] [DecidableEq b]
    {ρ : Matrix (a × b) (a × b) 𝕜} (hρ : IsDensity ρ) :
    vnEntropy ρ ≤ vnEntropy (ptrR ρ) + vnEntropy (ptrL ρ) := by
  have hA := isDensity_ptrR hρ
  have hB := isDensity_ptrL hρ
  set UA : Matrix a a 𝕜 := (hA.1.1.eigenvectorUnitary : Matrix a a 𝕜) with hUA
  set UB : Matrix b b 𝕜 := (hB.1.1.eigenvectorUnitary : Matrix b b 𝕜) with hUB
  have hUAu : UA * star UA = 1 := mem_unitaryGroup_iff.mp hA.1.1.eigenvectorUnitary.2
  have hUAu' : star UA * UA = 1 := mem_unitaryGroup_iff'.mp hA.1.1.eigenvectorUnitary.2
  have hUBu : UB * star UB = 1 := mem_unitaryGroup_iff.mp hB.1.1.eigenvectorUnitary.2
  have hUBu' : star UB * UB = 1 := mem_unitaryGroup_iff'.mp hB.1.1.eigenvectorUnitary.2
  set W : Matrix (a × b) (a × b) 𝕜 := UA ⊗ₖ UB with hW
  have hWu : W * star W = 1 := by
    rw [hW, Matrix.star_eq_conjTranspose, kronecker_conjTranspose',
      ← Matrix.mul_kronecker_mul, ← Matrix.star_eq_conjTranspose (M := UA),
      ← Matrix.star_eq_conjTranspose (M := UB), hUAu, hUBu,
      Matrix.one_kronecker_one]
  set ρ' : Matrix (a × b) (a × b) 𝕜 := star W * ρ * W with hρ'
  have hρ'dens : IsDensity ρ' := isDensity_conj_unitary hρ hWu
  -- ρ' as a product conjugation with unitary factors on both sides
  have hform : ρ' = (star UA ⊗ₖ star UB) * ρ * (star UA ⊗ₖ star UB)ᴴ := by
    rw [hρ', hW, kronecker_conjTranspose', ← Matrix.star_eq_conjTranspose (M := star UA),
      ← Matrix.star_eq_conjTranspose (M := star UB), star_star, star_star]
    congr 1
    rw [Matrix.star_eq_conjTranspose, kronecker_conjTranspose',
      ← Matrix.star_eq_conjTranspose (M := UA), ← Matrix.star_eq_conjTranspose (M := UB)]
  -- entropy is blind to the conjugation
  have hent : vnEntropy ρ' = vnEntropy ρ := by
    have := vnEntropy_conj_unitary (𝕜 := 𝕜) hρ.1.1
      ⟨star W, unitary.star_mem (by
        rw [Matrix.mem_unitaryGroup_iff]
        exact hWu)⟩
    simpa [star_star] using this
  -- the conjugated marginals are the diagonalized marginals
  have hmargA : ptrR ρ' = Matrix.diagonal (RCLike.ofReal ∘ hA.1.1.eigenvalues) := by
    rw [hform, ptrR_conj_kronecker ρ (star UA)
      (by rw [← Matrix.star_eq_conjTranspose, star_star]; exact hUBu),
      ← Matrix.star_eq_conjTranspose (M := star UA), star_star]
    exact hA.1.1.star_mul_self_mul_eq_diagonal
  have hmargB : ptrL ρ' = Matrix.diagonal (RCLike.ofReal ∘ hB.1.1.eigenvalues) := by
    rw [hform, ptrL_conj_kronecker ρ (star UB)
      (by rw [← Matrix.star_eq_conjTranspose, star_star]; exact hUAu),
      ← Matrix.star_eq_conjTranspose (M := star UB), star_star]
    exact hB.1.1.star_mul_self_mul_eq_diagonal
  -- pinch, then classical subadditivity on the pinched state
  have hpinch : vnEntropy ρ' ≤ entropy (diagRe ρ') :=
    vnEntropy_le_entropy_diagRe hρ'dens.1
  have hclass : entropy (diagRe ρ')
      ≤ entropy (fun x => ∑ y, diagRe ρ' (x, y))
        + entropy (fun y => ∑ x, diagRe ρ' (x, y)) :=
    entropy_grouping₂ (isProb_diagRe hρ'dens)
  have hmA : (fun x => ∑ y, diagRe ρ' (x, y)) = hA.1.1.eigenvalues := by
    funext x
    rw [← diagRe_ptrR, hmargA, diagRe_diagonal]
  have hmB : (fun y => ∑ x, diagRe ρ' (x, y)) = hB.1.1.eigenvalues := by
    funext y
    rw [← diagRe_ptrL, hmargB, diagRe_diagonal]
  rw [hmA, hmB] at hclass
  rw [← hent, vnEntropy_of_isHermitian hA.1.1, vnEntropy_of_isHermitian hB.1.1]
  linarith [hpinch, hclass]

end CIRISOntology.Core
