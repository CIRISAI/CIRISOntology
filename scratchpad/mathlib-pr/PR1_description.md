# PR 1 — feat(LinearAlgebra/Matrix): the Schur product theorem

## Title
`feat(LinearAlgebra/Matrix/PosDef): the Schur product theorem (Hadamard product of PSD matrices is PSD)`

## Description

Adds the **Schur product theorem**: the Hadamard (entrywise) product `A ⊙ B` of
two positive semidefinite matrices over `RCLike 𝕜` is positive semidefinite.

```
theorem Matrix.PosSemidef.hadamard {A B : Matrix n n 𝕜}
    (hA : A.PosSemidef) (hB : B.PosSemidef) : (A ⊙ B).PosSemidef
```

Mathlib currently has the algebra of the Hadamard product `⊙`
(`Mathlib/Data/Matrix/Hadamard.lean`) but no positivity result, and it has the
Schur *complement* (block matrices) which is a different object. This fills that
gap. Dot-notation `hA.hadamard hB` is available.

### Proof

The standard Gram-factorization argument. Write `A = Pᴴ P` and `B = Qᴴ Q`
(`posSemidef_iff_eq_transpose_mul_self`). Then, entrywise,
`(A ⊙ B)ᵢⱼ = (Σₖ P̄ₖᵢ Pₖⱼ)(Σₗ Q̄ₗᵢ Qₗⱼ) = Σₖₗ (Pₖᵢ Qₗᵢ)‾ (Pₖⱼ Qₗⱼ) = (Rᴴ R)ᵢⱼ`
for the Khatri–Rao-type factor `R⟨k,l⟩ i = Pₖᵢ Qₗᵢ`, so `A ⊙ B = Rᴴ R` is PSD by
`posSemidef_conjTranspose_mul_self`.

### Provenance

I. Schur, *Bemerkungen zur Theorie der beschränkten Bilinearformen mit unendlich
vielen Veränderlichen*, J. Reine Angew. Math. **140** (1911), 1–28. Standard
textbook reference: Horn & Johnson, *Topics in Matrix Analysis*, Theorem 5.2.1.

### Placement

`Mathlib/LinearAlgebra/Matrix/PosDef.lean`, near `posSemidef_conjTranspose_mul_self`,
adding `import Mathlib.Data.Matrix.Hadamard`. If reviewers prefer to keep the
Hadamard import out of `PosDef.lean`, a small new file
`Mathlib/LinearAlgebra/Matrix/Hadamard.lean` works equally well.

### Notes for reviewers

- Stated over `RCLike 𝕜`; the proof needs only `posSemidef_iff_eq_transpose_mul_self`
  (RCLike) and `posSemidef_conjTranspose_mul_self` (`StarOrderedRing`).
- `open scoped ComplexOrder` is not needed for this statement (no order on `det`);
  it is only needed by the determinant PRs.
- `[DecidableEq n]` is `omit`-ted (unused).
