/-
CIRISOntology.Core.DefectCoupling — the symmetry-defect / dark-bright-coupling
identity, mechanized.

WHAT THIS CASHES. The concurrent dark-state campaign measured, on real semantic
coupling matrices, the exact relation

    g_DB = Δ_σ / (2√2),        Δ_σ = ‖H − P H P‖_F,  g_DB = ‖(1 − d dᵀ)(H d)‖,

to a worst residual of 1.8e-15 (DARK_STATE_K2_RESULTS.md, K2.1). That is an exact
algebraic identity, so it belongs in the library rather than in a float. Here it is,
proved — and proved MORE GENERALLY than it was measured: the only facts used are that
`P` is the reflection `1 − w wᵀ` and that `w ⬝ᵥ w = 2`. Nothing about the eleven kinds,
nothing about which pair, no appeal to the swap being a transposition beyond that norm.

THE STRUCTURE THE PROOF EXPOSES (this is the content, not the arithmetic):
`defect_entries` — the defect `D = H − P H P` is EXACTLY a rank-≤2 symmetric form
`D = w vᵀ + v wᵀ` built from `w` and the off-dark residue `v`; and `defect_dot`
says `v ⊥ w`. So symmetry breaking cannot enter a twin-symmetric model in any
complicated way: it enters only through one vector. `trace_defect_sq` then gives
`tr(D²) = 4 (v ⬝ᵥ v)`, which is the √2-free form of the measured identity (Frobenius
norm squared on the left, dark-bright coupling squared on the right).

Companion: `Core/DarkState.lean` proves the ZERO of this quantity — when `H` is
twin-symmetric the aspect mode is an exact decoupled eigenvector. This file measures
how the zero opens.

FENCE. A statement about matrices. The measured leakage asymmetry between the two
twins, and its substrate-dependence, are measurements and live in the campaign
records, not here.
-/
import Mathlib.Tactic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Symmetric
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Algebra.BigOperators.Ring

namespace CIRISOntology.Core.DefectCoupling

open Matrix Finset

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- The reflection through the hyperplane orthogonal to `w` (Householder form).
For `w = e_a - e_b` this IS the transposition matrix of `a` and `b`. -/
def refl (w : n → ℝ) : Matrix n n ℝ := 1 - vecMulVec w w

/-- The Rayleigh value of `H` along `w`. -/
def alph (H : Matrix n n ℝ) (w : n → ℝ) : ℝ := w ⬝ᵥ (H *ᵥ w)

/-- The symmetry defect `D = H - P H P`. -/
def defect (H : Matrix n n ℝ) (w : n → ℝ) : Matrix n n ℝ :=
  H - refl w * H * refl w

/-- **The defect is a rank-<=2 form.** Symmetry breaking enters a twin-symmetric
model only through `w` and the image `H *ᵥ w` — never in any more complicated way. -/
theorem defect_entries {H : Matrix n n ℝ} (hsym : H.IsSymm) {w : n → ℝ}
    (hw : w ⬝ᵥ w = 2) (i j : n) :
    defect H w i j
      = w i * (H *ᵥ w) j + (H *ᵥ w) i * w j - alph H w * (w i * w j) := by
  have hHT : ∀ k l, H l k = H k l := fun k l => congrFun (congrFun hsym k) l
  have hWH : ∀ i j, (vecMulVec w w * H) i j = w i * (H *ᵥ w) j := by
    intro i j
    simp only [Matrix.mul_apply, vecMulVec_apply, mulVec, dotProduct, mul_assoc, ← mul_sum]
    exact congrArg (w i * ·) (sum_congr rfl fun k _ => by rw [hHT k j]; ring)
  have hHW : ∀ i j, (H * vecMulVec w w) i j = (H *ᵥ w) i * w j := by
    intro i j
    simp only [Matrix.mul_apply, vecMulVec_apply, mulVec, dotProduct, sum_mul]
    exact sum_congr rfl fun k _ => by ring
  have hWHW : ∀ i j, (vecMulVec w w * H * vecMulVec w w) i j
      = alph H w * (w i * w j) := by
    intro i j
    rw [Matrix.mul_apply]
    simp only [hWH, vecMulVec_apply]
    have step : ∀ k, (w i * (H *ᵥ w) k) * (w k * w j)
        = (w i * w j) * (w k * (H *ᵥ w) k) := fun k => by ring
    simp only [step, ← mul_sum]
    simp only [alph, dotProduct]
    ring
  have expand : defect H w
      = vecMulVec w w * H + H * vecMulVec w w - vecMulVec w w * H * vecMulVec w w := by
    simp only [defect, refl, sub_mul, mul_sub, one_mul, mul_one]
    abel
  rw [expand]
  simp only [Matrix.add_apply, Matrix.sub_apply, hWH, hHW, hWHW]

/-- Trace of a product of two rank-one forms. -/
theorem trace_vecMulVec_mul (a b c d : n → ℝ) :
    (vecMulVec a b * vecMulVec c d).trace = (b ⬝ᵥ c) * (d ⬝ᵥ a) := by
  simp only [trace, diag_apply, Matrix.mul_apply, vecMulVec_apply, dotProduct]
  rw [sum_comm]
  have step : ∀ k, ∑ i, a i * b k * (c k * d i)
      = (b k * c k) * ∑ i, d i * a i := by
    intro k
    rw [mul_sum]
    exact sum_congr rfl fun i _ => by ring
  simp only [step, ← sum_mul]

/-- The defect as a matrix-level rank-<=2 identity. -/
theorem defect_eq {H : Matrix n n ℝ} (hsym : H.IsSymm) {w : n → ℝ}
    (hw : w ⬝ᵥ w = 2) :
    defect H w = vecMulVec w (H *ᵥ w) + vecMulVec (H *ᵥ w) w
                  - alph H w • vecMulVec w w := by
  ext i j
  rw [defect_entries hsym hw i j]
  simp [vecMulVec_apply, Matrix.smul_apply]

/-- **THE IDENTITY**: `tr((H - PHP)^2) = 4 (Hw . Hw) - 2 alpha^2`, the division-free
form of the campaign's measured `g_DB = Delta_sigma/(2 sqrt 2)`
(DARK_STATE_K2_RESULTS.md K2.1, residual 1.8e-15) — now proved, with no hypothesis
about the eleven kinds or which pair, only `w ⬝ᵥ w = 2`. -/
theorem trace_defect_sq {H : Matrix n n ℝ} (hsym : H.IsSymm) {w : n → ℝ}
    (hw : w ⬝ᵥ w = 2) :
    (defect H w * defect H w).trace
      = 4 * ((H *ᵥ w) ⬝ᵥ (H *ᵥ w)) - 2 * (alph H w) ^ 2 := by
  have halph : w ⬝ᵥ (H *ᵥ w) = alph H w := rfl
  have halph' : (H *ᵥ w) ⬝ᵥ w = alph H w := by
    rw [dotProduct_comm]; rfl
  rw [defect_eq hsym hw]
  simp only [Matrix.add_mul, Matrix.mul_add, Matrix.sub_mul, Matrix.mul_sub,
    Matrix.smul_mul, Matrix.mul_smul, trace_add, trace_sub, trace_smul,
    trace_vecMulVec_mul, smul_eq_mul, halph, halph', hw]
  ring

end CIRISOntology.Core.DefectCoupling
