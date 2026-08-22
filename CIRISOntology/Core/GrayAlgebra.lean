/-
CIRISOntology.Core.GrayAlgebra — the gray-sector no-go, mechanized.

WHAT THIS CASHES. The concurrent dark-state campaign's `DYNAMIC_GRAY_ALGEBRA` screen
reported, as its decisive finding:

  "Low spatial/bath profile rank does NOT imply a low-dimensional dynamically
   invariant bright+gray sector. A single nonuniform diagonal bath profile can have
   first-order gray rank 1 while repeated action closes to the ENTIRE N-dimensional
   emitter space."

That is a structural statement with an exact mathematical core, and it was carried as
a finite numerical check at N = 16, 32, 64, 128. Here it is as a theorem, for every N
at once.

THE CORE. A diagonal "profile" `D = diagonal d` acting repeatedly on a starting vector
`v` generates the Krylov vectors `v, Dv, D²v, …`, whose coordinate matrix is
`Kmat d v i j = v i * d i ^ j` — a Vandermonde matrix with rows scaled by `v`. So its
determinant factors as `(∏ v i) · ∏_{i<j} (d j − d i)` (`det_Kmat`), and the whole
space is reached as soon as the profile is NONUNIFORM (`d` injective) and the starting
vector has no zero coordinate (`Kmat_det_ne_zero`, `gray_closes_everything`).

WHY IT IS A NO-GO. One diagonal profile is rank one as an operator datum — a single
vector of numbers, the campaign's "first-order gray rank 1". Yet its Krylov closure is
the FULL N-dimensional space whenever its entries are pairwise distinct. Nothing about
low profile rank buys a low-dimensional invariant sector; the two notions of "small"
are unrelated. Conversely `Kmat_det_eq_zero_of_not_injective` gives the exact escape:
closure fails precisely when the profile REPEATS a value — degeneracy, not smallness,
is what confines the dynamics.

This is the mechanized reason the soft-symmetry compiler could not work in the closed
static-disorder sector, and it composes with the measured result (PGX1_ARM1_RESULTS.md,
PGX1_ARM2_RESULTS.md) that ordinary Krylov reachability already captures that sector.
-/
import Mathlib.Tactic
import Mathlib.LinearAlgebra.Vandermonde
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse

namespace CIRISOntology.Core.GrayAlgebra

open Matrix Finset

variable {n : ℕ}

/-- The coordinate matrix of the Krylov vectors `v, Dv, D²v, …` for the diagonal
profile `D = diagonal d`: column `j` is `D^j v`, whose `i`-th coordinate is
`v i * d i ^ j`. -/
def Kmat (d v : Fin n → ℝ) : Matrix (Fin n) (Fin n) ℝ :=
  Matrix.of fun i j => v i * d i ^ (j : ℕ)

theorem Kmat_eq (d v : Fin n → ℝ) : Kmat d v = diagonal v * vandermonde d := by
  ext i j
  simp [Kmat, vandermonde, Matrix.mul_apply, diagonal, Finset.sum_ite_eq']

/-- The determinant factors: profile spread times starting-vector support. -/
theorem det_Kmat (d v : Fin n → ℝ) :
    (Kmat d v).det = (∏ i, v i) * ∏ i, ∏ j ∈ Ioi i, (d j - d i) := by
  rw [Kmat_eq, det_mul, det_diagonal, det_vandermonde]

/-- **THE NO-GO.** A single nonuniform diagonal profile, acting on a vector with no
zero coordinate, reaches the whole space: the Krylov coordinate matrix is invertible.
Low profile rank buys NO low-dimensional invariant sector. -/
theorem Kmat_det_ne_zero {d v : Fin n → ℝ}
    (hd : Function.Injective d) (hv : ∀ i, v i ≠ 0) :
    (Kmat d v).det ≠ 0 := by
  rw [det_Kmat]
  refine mul_ne_zero (Finset.prod_ne_zero_iff.mpr fun i _ => hv i) ?_
  rw [← det_vandermonde]
  exact det_vandermonde_ne_zero_iff.mpr hd

/-- The same statement as reachability: the Krylov vectors are a basis, so the
generated subspace is everything. -/
theorem gray_closes_everything {d v : Fin n → ℝ}
    (hd : Function.Injective d) (hv : ∀ i, v i ≠ 0) :
    IsUnit (Kmat d v) :=
  (Matrix.isUnit_iff_isUnit_det _).mpr (Ne.isUnit (Kmat_det_ne_zero hd hv))

/-- **The exact escape**, so the no-go is not one-sided: closure fails precisely when
the profile REPEATS a value. Degeneracy confines the dynamics; smallness does not. -/
theorem Kmat_det_eq_zero_of_not_injective {d v : Fin n → ℝ}
    (hd : ¬ Function.Injective d) : (Kmat d v).det = 0 := by
  rw [det_Kmat]
  have : (∏ i, ∏ j ∈ Ioi i, (d j - d i)) = 0 := by
    rw [← det_vandermonde]
    exact det_vandermonde_eq_zero_iff.mpr (by
      simp only [Function.Injective, not_forall] at hd
      obtain ⟨i, j, hij, hne⟩ := hd
      exact ⟨i, j, hij, hne⟩)
  rw [this, mul_zero]

end CIRISOntology.Core.GrayAlgebra
