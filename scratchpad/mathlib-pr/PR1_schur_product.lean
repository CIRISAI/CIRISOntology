/-
PR 1 — The Schur product theorem (Hadamard product of PSD matrices is PSD).

Target file: `Mathlib/LinearAlgebra/Matrix/PosDef.lean` (add `import
Mathlib.Data.Matrix.Hadamard`), placed near `posSemidef_conjTranspose_mul_self`.
Alternative placement: a new `Mathlib/LinearAlgebra/Matrix/Hadamard.lean`
(positivity of the Hadamard product), if reviewers prefer to keep the Hadamard
import out of `PosDef.lean`.

Provenance: Schur, J. (1911), "Bemerkungen zur Theorie der beschränkten
Bilinearformen mit unendlich vielen Veränderlichen", J. Reine Angew. Math. 140.
Textbook: Horn & Johnson, *Topics in Matrix Analysis*, Theorem 5.2.1 (Schur
product theorem). The proof here is the standard Gram-factorization argument:
if `A = Pᴴ P` and `B = Qᴴ Q` then `A ⊙ B = Rᴴ R` for the Khatri–Rao-type factor
`R⟨k,l⟩ i = P k i * Q l i`, so it is PSD.

VERIFIED: compiles sorry-free on Mathlib v4.14 (see #print axioms below);
standard axioms only. Adapt to current master before opening the PR.
-/
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Data.Matrix.Hadamard

open scoped ComplexOrder Matrix

namespace Matrix

variable {𝕜 : Type*} [RCLike 𝕜] {n : Type*} [Fintype n] [DecidableEq n]

omit [DecidableEq n] in
/-- **Schur product theorem**: the Hadamard (entrywise) product of two positive
semidefinite matrices is positive semidefinite. -/
theorem PosSemidef.hadamard {A B : Matrix n n 𝕜}
    (hA : A.PosSemidef) (hB : B.PosSemidef) : (A ⊙ B).PosSemidef := by
  obtain ⟨P, hP⟩ := posSemidef_iff_eq_transpose_mul_self.mp hA
  obtain ⟨Q, hQ⟩ := posSemidef_iff_eq_transpose_mul_self.mp hB
  have key : A ⊙ B
      = (Matrix.of (fun kl : n × n => fun i => P kl.1 i * Q kl.2 i))ᴴ
        * Matrix.of (fun kl : n × n => fun i => P kl.1 i * Q kl.2 i) := by
    ext i j
    rw [hadamard_apply, hP, hQ, mul_apply, mul_apply, mul_apply, Finset.sum_mul_sum,
      Fintype.sum_prod_type]
    refine Finset.sum_congr rfl fun k _ => Finset.sum_congr rfl fun l _ => ?_
    simp only [conjTranspose_apply, of_apply, star_mul']
    ring
  rw [key]
  exact posSemidef_conjTranspose_mul_self _

end Matrix

#print axioms Matrix.PosSemidef.hadamard
