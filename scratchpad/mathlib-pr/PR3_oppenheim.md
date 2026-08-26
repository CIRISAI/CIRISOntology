# PR 3 — Oppenheim's inequality (status, obstacle, and PR draft)

## Status: ℝ proof READY (in repo); RCLike generalization is the OBSTACLE

The full theorem is proved and verified sorry-free over ℝ in the CIRISOntology
repo at **`CIRISOntology/Core/Entropy.lean`** (`oppenheim_det`, plus the general
contraction corollary `S_pairwise_hadamard_le`). It is NOT yet generalized to
`RCLike 𝕜`, and that generalization is the only thing standing between it and a
Mathlib PR. Details below.

## Statement (ℝ, as proved)

```
theorem oppenheim_det {k : ℕ} (A B : Matrix (Fin k) (Fin k) ℝ) :
    A.PosSemidef → B.PosSemidef → (∀ i, B i i = 1) → A.det ≤ (A ⊙ B).det
```

Proposed Mathlib name: `Matrix.PosSemidef.det_le_det_hadamard`.

## Proof structure (all in Core/Entropy.lean, verified)

Induction on dimension via the Schur complement:
- singular `A`: `det A = 0 ≤ det(A ⊙ B)` (`PosSemidef.det_nonneg` on the product,
  which is PSD by the Schur product theorem `hadamard_posSemidef`);
- `A` PosDef: split off the last coordinate (pivot `α > 0`); the block-determinant
  reduction `det_schur_reduce` gives `det A = α·det C_A` and
  `det(A ⊙ B) = α·det(C_A ⊙ B₁ + P)`; the block Schur–Hadamard identity
  `schur_hadamard_identity` shows `P` is PSD; then
  `det A = α·det C_A ≤ α·det(C_A ⊙ B₁)` (induction hypothesis)
  `≤ α·det(C_A ⊙ B₁ + P)` (determinant monotonicity, = PR 2's `det_le_det_add`)
  `= det(A ⊙ B)`.

Supporting lemmas (in Core/Entropy.lean): `schur_hadamard_identity`,
`det_schur_reduce`, `schur_posSemidef`, `schur_oneScalar`, `posDef_diag_pos`,
`posDef_fin_one`, `posSemidef_vecMulVec`, `hadamard_vecMulVec`, `submatrix_hadamard`,
`hadamard_fromBlocks`, `isHermitian_hadamard`, `posSemidef_smul`. Several of these
are independently PR-worthy (see "spin-offs").

## The RCLike generalization obstacle (precise)

Mathlib will want `RCLike 𝕜`, not ℝ. The obstruction is that the induction's
supporting lemmas are stated with the **symmetric** rank-one outer product
`vecMulVec u u` (= `u uᵀ`) and closed by entrywise `ring` over ℝ. Over `RCLike 𝕜`
the correct objects are **Hermitian** outer products `u uᴴ` (`= vecMulVec u (star u)`),
and every identity picks up conjugations. Concretely, to generalize:

1. `schur_hadamard_identity` — the crux algebraic identity
   `A₁ ⊙ B₁ − α⁻¹ (u∘v)(u∘v)ᴴ = (A₁ − α⁻¹ u uᴴ) ⊙ B₁ + α⁻¹ (u uᴴ) ⊙ (B₁ − v vᴴ)`
   must be re-derived with `star`; the `ring` closer becomes a `star`-aware
   computation (feasible: `star_mul'`, but no longer one `ring` call).
2. `schur_oneScalar` — `B · D⁻¹ · Bᴴ = (D₀₀)⁻¹ • (u uᴴ)` with `u i = B i 0`;
   the conjugate on the second factor changes.
3. `posDef_diag_pos` — `0 < A i i` becomes `0 < (A i i)` in `ComplexOrder` (the
   diagonal of a PosDef Hermitian matrix is a positive real); provable but needs
   the `re`/ComplexOrder handling.
4. `det_schur_reduce`, `schur_posSemidef` — already use `Bᴴ`, so mostly survive; the
   `vecMulVec` connectors (2) feed them.
5. The determinant monotonicity step is **already RCLike** (PR 2).

This is roughly a day of Lean work (re-proving ~6 helper lemmas with conjugates and
re-threading the induction), carrying no mathematical risk. It was out of scope for
this preparation pass.

**Option A (recommended):** generalize to `RCLike 𝕜` first, then submit. The det
monotonicity (PR 2) and Schur product (PR 1) it depends on are already RCLike, so
only the Oppenheim-specific helpers remain.

**Option B:** submit the ℝ special case now with a `TODO(RCLike)` and let a
follow-up generalize. Mathlib reviewers usually prefer A for a result this
classical, but B is defensible given the ℝ case is the one in most textbooks.

## Further generalization (independent of RCLike)

Our statement requires `B` unit-diagonal, which specializes the *fully* general
Oppenheim `det(A ⊙ B) ≥ det A · ∏ᵢ Bᵢᵢ` (Horn & Johnson, *Topics in Matrix
Analysis*, Theorem 5.2.4 / Oppenheim 1930) to `∏ᵢ Bᵢᵢ = 1`. The `∏ᵢ Bᵢᵢ` form
follows by scaling `B` to unit diagonal; worth adding in the same PR.

## PR draft

**Title:** `feat(LinearAlgebra/Matrix): Oppenheim's determinant inequality`

**Body:** Adds Oppenheim's inequality — for positive semidefinite `A` and `B`,
`det(A ⊙ B) ≥ det A · ∏ᵢ Bᵢᵢ` (Horn & Johnson, *Topics in Matrix Analysis*,
Thm 5.2.4; Oppenheim, *Inequalities connected with definite Hermitian forms*,
J. London Math. Soc. **5** (1930)). Depends on the Schur product theorem (PR 1)
and determinant monotonicity on the PSD cone (PR 2). Proof by Schur-complement
induction on dimension. [Attach the extracted, RCLike-generalized proof from
CIRISOntology/Core/Entropy.lean.]

## Spin-off PRs worth extracting from the helper lemmas

- `Matrix.PosDef` diagonal is positive (`posDef_diag_pos`) — small, generally useful.
- `Matrix.PosSemidef.smul` (nonneg scalar multiple of PSD is PSD) — currently absent.
- `Matrix.IsHermitian.hadamard` (Hadamard of Hermitian is Hermitian) — absent.
- block-Hadamard compatibility (`hadamard_fromBlocks`, `submatrix_hadamard`) —
  natural additions to `Data/Matrix/Hadamard.lean`.
