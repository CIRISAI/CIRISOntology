# PR 2 — feat(LinearAlgebra/Matrix/PosDef): determinant inequalities for PSD matrices

## Title
`feat(LinearAlgebra/Matrix/PosDef): determinant nonnegativity and monotonicity on the PSD cone`

## Description

Adds a cluster of determinant facts for positive (semi)definite matrices over
`RCLike 𝕜` (with `open scoped ComplexOrder`), mirroring and extending the existing
`Matrix.PosDef.det_pos`:

```
theorem Matrix.PosSemidef.det_nonneg (hX : X.PosSemidef) : 0 ≤ X.det
theorem Matrix.PosSemidef.posDef_of_isUnit_det (hA : A.PosSemidef) (hdet : IsUnit A.det) : A.PosDef
theorem Matrix.PosSemidef.one_le_det_one_add (hQ : Q.PosSemidef) : 1 ≤ (1 + Q).det
theorem Matrix.PosDef.det_le_det_add (hX : X.PosDef) (hP : P.PosSemidef) : X.det ≤ (X + P).det
theorem Matrix.PosSemidef.det_le_det_add (hX : X.PosSemidef) (hP : P.PosSemidef) : X.det ≤ (X + P).det
```

Mathlib has `PosDef.det_pos` (`0 < det`) but not `PosSemidef.det_nonneg`, no
`PosDef`-from-nonsingularity bridge, and no determinant monotonicity on the PSD
cone. These are frequently-wanted gap-fillers (e.g. determinant monotonicity is a
prerequisite for Oppenheim's inequality and for Fisher-information / MLE arguments).

### Proofs (brief)

- `det_nonneg`: `det = ∏ (eigenvalues : 𝕜)`, each eigenvalue `≥ 0`; push the
  product through `RCLike.ofReal` and use `ofReal_nonneg`.
- `posDef_of_isUnit_det`: `IsUnit det ⇒ mulVec` injective ⇒ `X *ᵥ x ≠ 0` for
  `x ≠ 0`, then `PosSemidef.dotProduct_mulVec_zero_iff` gives strict positivity of
  the quadratic form (`lt_of_le_of_ne`).
- `one_le_det_one_add`: spectrally `1 + Q = U diag(1+λ) Uᴴ`, so
  `det(1+Q) = ∏(1+λᵢ) ≥ 1` since each `λᵢ ≥ 0` (`Finset.prod_le_prod` against `1`,
  lifted through `RCLike.ofReal`).
- `PosDef.det_le_det_add`: matrix determinant lemma on the Gram factor `P = MᴴM`
  gives `det(X+P) = det X · det(1 + M X⁻¹ Mᴴ)`; the second factor is `≥ 1` by
  `one_le_det_one_add` (`M X⁻¹ Mᴴ` is PSD as a congruence of `X⁻¹`), and `det X > 0`.
- `PosSemidef.det_le_det_add`: case on `IsUnit X.det`; if a unit, `X` is PosDef and
  we reduce to the previous lemma; otherwise `det X = 0 ≤ det(X+P)` by `det_nonneg`.

### Provenance

Standard. Horn & Johnson, *Matrix Analysis*, §7.8 (determinant monotonicity on the
PSD cone; the Löwner-order corollary `A ≼ B ⇒ det A ≤ det B`); `one_le_det_one_add`
is the `det(I + Q) ≥ 1` special case.

### Placement

`Mathlib/LinearAlgebra/Matrix/PosDef.lean`, in the `Det` region alongside
`det_pos` (add `import Mathlib.LinearAlgebra.Matrix.SchurComplement` for
`det_add_mul`, the matrix determinant lemma).

### Notes for reviewers

- All over `RCLike 𝕜` with `ComplexOrder`, consistent with `det_pos`.
- Could be split (e.g. `det_nonneg` + `posDef_of_isUnit_det` in one PR, the
  monotonicity chain in another) if a smaller review is preferred; they are grouped
  here because `det_le_det_add` depends on the others.
- `PosDef.det_le_det_add` / `PosSemidef.det_le_det_add` deliberately share a name
  across the two namespaces (dot-notation dispatches on the hypothesis).
