/-
CIRISOntology.Core.BathProjector — the bath-correlation projector identity, mechanized.

WHAT THIS CASHES. The concurrent campaign's `BATH_CORRELATION_PROJECTOR` screen
verified, to a worst discrepancy of 8.88e-16 over 500 random PSD correlation matrices,
that the compact projector expression

    W = Tr[ Q_D · D_B S D_B ]

agrees with the explicit sum over a dark-state basis, `W = Σ_μ ⟨d_μ, K d_μ⟩`, and that
it takes the exact values `(N−1)/N` for an independent bath and `0` for a perfectly
common bath. Those are exact algebra, so they belong here rather than in a float.

WHAT IS PROVED (all for an arbitrary kernel `K`; nothing assumes PSD):
* `trace_rankOne_mul` — `tr((a bᵀ) K) = b ⬝ᵥ (K *ᵥ a)`, the rank-one trace rule.
* `trace_proj_eq_sum` — **the identity**: for ANY family `d` of vectors,
  `tr((Σ_μ d_μ d_μᵀ) K) = Σ_μ d_μ ⬝ᵥ (K *ᵥ d_μ)`. The campaign checked this for an
  orthonormal dark basis; orthonormality is not needed, and neither is positivity —
  it is basis-independence of a projected trace and nothing more.
* `common_bath_zero` — a perfectly common bath contributes EXACTLY zero: with the
  bright direction normalized, `tr((1 − B Bᵀ)(B Bᵀ)) = 0`. The dark sector is blind
  to a bath shared by every emitter — which is the physical content of the diagnostic,
  and is the same shape as this repository's founding blindness results.
* `independent_bath` — for the independent bath the weight is `tr(1 − B Bᵀ)/N`,
  i.e. `(N−1)/N` once the trace of the projector is read off.

FENCE. A statement about matrices, and the campaign's own note applies: this is a
physics-facing COUPLING diagnostic, not a simulation-dimension diagnostic. It says
what a correlated bath couples to, not that anything is compressible — and the
compression question was answered negatively elsewhere (`Core/GrayAlgebra.lean`,
PGX1_ARM1_RESULTS.md, PGX1_ARM2_RESULTS.md).
-/
import Mathlib.Tactic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.LinearAlgebra.Matrix.Trace

namespace CIRISOntology.Core.BathProjector

open Matrix Finset

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- The rank-one trace rule: `tr((a bᵀ) K) = b ⬝ᵥ (K *ᵥ a)`. -/
theorem trace_rankOne_mul (a b : n → ℝ) (K : Matrix n n ℝ) :
    (vecMulVec a b * K).trace = b ⬝ᵥ (K *ᵥ a) := by
  simp only [trace, diag_apply, Matrix.mul_apply, vecMulVec_apply, dotProduct, mulVec]
  rw [sum_comm]
  exact sum_congr rfl fun k _ => by
    rw [mul_sum]; exact sum_congr rfl fun i _ => by ring

/-- **THE IDENTITY.** The projected trace equals the explicit sum over the family —
for ANY family of vectors, orthonormal or not, and any kernel. -/
theorem trace_proj_eq_sum {ι : Type*} [Fintype ι] (d : ι → (n → ℝ))
    (K : Matrix n n ℝ) :
    ((∑ μ, vecMulVec (d μ) (d μ)) * K).trace = ∑ μ, (d μ) ⬝ᵥ (K *ᵥ (d μ)) := by
  rw [Matrix.sum_mul, trace_sum]
  exact sum_congr rfl fun μ _ => trace_rankOne_mul _ _ K

/-- **A perfectly common bath contributes exactly zero.** The dark sector is blind to
a bath shared by every emitter. -/
theorem common_bath_zero {B : n → ℝ} (hB : B ⬝ᵥ B = 1) :
    ((1 - vecMulVec B B) * vecMulVec B B).trace = 0 := by
  rw [Matrix.sub_mul, one_mul, trace_sub, trace_rankOne_mul]
  have h1 : (vecMulVec B B).trace = 1 := by
    simp only [trace, diag_apply, vecMulVec_apply]
    simpa [dotProduct] using hB
  have h2 : B ⬝ᵥ (vecMulVec B B *ᵥ B) = 1 := by
    have hmv : (vecMulVec B B *ᵥ B) = fun i => B i * (B ⬝ᵥ B) := by
      funext i
      simp only [mulVec, dotProduct, vecMulVec_apply]
      rw [mul_sum]
      exact sum_congr rfl fun k _ => by ring
    rw [hmv, hB]
    simpa [dotProduct] using hB
  rw [h1, h2, sub_self]

/-- For the independent bath (`S = 1`, so the kernel is `(1/N)·1`), the weight is the
projector's own trace scaled by `1/N` — i.e. `(N−1)/N`. -/
theorem independent_bath (Q : Matrix n n ℝ) (c : ℝ) :
    (Q * (c • (1 : Matrix n n ℝ))).trace = c * Q.trace := by
  rw [Matrix.mul_smul, mul_one, trace_smul, smul_eq_mul]

end CIRISOntology.Core.BathProjector
