# PR — feat(Analysis/Matrix): determinant monotonicity on the PSD cone

**Status: master-verified, submit-ready.** Compiles sorry-free against mathlib4
master @ `bbc4475e9e8fd25fbc8e26d636dd8b37be8f105a` (toolchain v4.33.0-rc1),
standard axioms only. Code: `PR_det_monotonicity_MASTER.lean`.

## Title
`feat(Analysis/Matrix/Order): the determinant is monotone on the PSD cone`

## Description

Mathlib has the Löwner order on Hermitian matrices (`Analysis/Matrix/Order.lean`:
`A ≤ B ↔ (B - A).PosSemidef`, with the `StarOrderedRing` / `NonnegSpectrumClass`
instances), and `PosDef.det_pos` / `PosSemidef.det_nonneg`, but it never proves that
`det` is **monotone** on this order. This PR adds that, plus the `det(1 + Q) ≥ 1`
special case it factors through:

```
theorem Matrix.PosSemidef.one_le_det_one_add (hQ : Q.PosSemidef) : 1 ≤ (1 + Q).det
theorem Matrix.PosDef.det_le_det_add     (hX : X.PosDef)     (hP : P.PosSemidef) : X.det ≤ (X + P).det
theorem Matrix.PosSemidef.det_le_det_add (hX : X.PosSemidef) (hP : P.PosSemidef) : X.det ≤ (X + P).det
theorem Matrix.PosSemidef.det_le_det_of_le (hA : A.PosSemidef) (hAB : A ≤ B) : A.det ≤ B.det
```

All over `RCLike 𝕜` with `open scoped ComplexOrder`, matching `det_pos`.

### Proofs

- `one_le_det_one_add`: spectrally `1 + Q = U diag(1 + λ) Uᴴ`, so
  `det(1+Q) = ∏(1 + λᵢ) ≥ 1` since each eigenvalue `λᵢ ≥ 0` (`Finset.prod_le_prod`
  against `1`, lifted through `RCLike.ofReal`).
- `PosDef.det_le_det_add`: matrix determinant lemma on the Gram factor
  `P = MᴴM` (from `CStarAlgebra.nonneg_iff_eq_star_mul_self`) gives
  `det(X+P) = det X · det(1 + M X⁻¹ Mᴴ)`; the second factor is `≥ 1` by
  `one_le_det_one_add`, and `det X > 0`.
- `PosSemidef.det_le_det_add`: case on `det X = 0`; if not, `X` is PosDef
  (`posDef_iff_det_ne_zero`) and reduce; if so, `det X = 0 ≤ det(X+P)` by `det_nonneg`.
- `det_le_det_of_le`: `A ≤ B` gives `(B - A)` PSD; apply `det_le_det_add` and simplify.

### Provenance

Horn & Johnson, *Matrix Analysis*, §7.8 — determinant monotonicity on the positive
semidefinite cone (`A ≼ B ⇒ det A ≤ det B`). `one_le_det_one_add` is the
`det(I + Q) ≥ 1` corollary.

### Placement

`Mathlib/Analysis/Matrix/Order.lean` (where the Löwner order, `det_nonneg`, and the
Schur product theorem already live) is the natural home for `det_le_det_of_le` and
the `det_le_det_add` pair. `one_le_det_one_add` could equally sit in
`Mathlib/Analysis/Matrix/PosDef.lean` next to `det_pos`/`det_nonneg`; keeping all
four together in `Order.lean` reads best as one "monotonicity" unit.

### Notes for reviewers

- The `det_le_det_of_le` Löwner statement is the headline; the `det_le_det_add`
  forms are the convenient working versions (`X ≤ X + P` since `P` is PSD).
- Uses the scoped instances `open scoped MatrixOrder Matrix.Norms.L2Operator` for the
  order and the CStarAlgebra Gram factorization.
