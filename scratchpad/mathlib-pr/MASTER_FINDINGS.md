# Verification against Mathlib master — findings

**Checked against:** mathlib4 master @ `bbc4475e9e8fd25fbc8e26d636dd8b37be8f105a`
(fresh shallow clone, `lake exe cache get`, toolchain `leanprover/lean4:v4.33.0-rc1`).
Our pinned build is v4.14.0 (Nov 2024); master is ~2 years newer.

## Headline: much of the proposed set is ALREADY in master

The 2 years since v4.14 upstreamed a large amount of PSD-matrix theory. Several
of our proposed contributions are now redundant:

| Proposed | Status in master | Where |
|---|---|---|
| Schur product `PosSemidef.hadamard` | **ALREADY THERE** (+ `PosDef.hadamard`, cites schur1911) | `Analysis/Matrix/Order.lean:239` |
| `PosSemidef.det_nonneg` | **ALREADY THERE** | `Analysis/Matrix/PosDef.lean:48` |
| PSD + unit det ⇒ PosDef | **ALREADY THERE** (`posDef_iff_isUnit`, `posDef_iff_det_ne_zero`) | `Analysis/Matrix/Order.lean:181,200` |
| (bonus we didn't propose) Kronecker PSD, full Löwner order | ALREADY THERE | `Analysis/Matrix/Order.lean` |

**So PR1 (Schur product) is fully redundant — do not submit.** Half of the
proposed PR2 (det_nonneg, the PSD→PosDef bridge) is also redundant.

## Genuinely NEW and now MASTER-VERIFIED (submit-ready)

File: **`PR_det_monotonicity_MASTER.lean`** — compiles sorry-free against master,
standard axioms. These are still absent from master:

- `Matrix.PosSemidef.one_le_det_one_add` — `1 ≤ det(1 + Q)`.
- `Matrix.PosDef.det_le_det_add` — `det X ≤ det(X + P)` (X PosDef, P PSD).
- `Matrix.PosSemidef.det_le_det_add` — `det X ≤ det(X + P)` (both PSD).
- `Matrix.PosSemidef.det_le_det_of_le` — the idiomatic Löwner form
  `A ≤ B ⇒ det A ≤ det B` (master already has the order, so this is the natural
  statement to add; determinant monotonicity on the PSD cone is genuinely missing).

Determinant monotonicity is a clean, wanted gap: master set up the Löwner order
and `StarOrderedRing`/`NonnegSpectrumClass` instances but never proved `det` is
monotone on it. This PR fills that.

## Oppenheim — still missing from master, still the real prize

No Oppenheim / `det_le_det_hadamard` anywhere in master. Our ℝ proof is complete
(`CIRISOntology/Core/Entropy.lean`). It needs the RCLike generalization (the
symmetric→Hermitian outer-product work described in `PR3_oppenheim.md`) before it
can go up; that is the remaining substantial task.

## Master-rename surprises (for whoever ports)

1. `Mathlib.Data.Matrix.Hadamard` → `Mathlib.LinearAlgebra.Matrix.Hadamard`.
2. The spectral / analytic PSD content moved out of `LinearAlgebra/Matrix/` into
   `Analysis/Matrix/`: `Analysis/Matrix/Spectrum.lean`, `Analysis/Matrix/PosDef.lean`,
   `Analysis/Matrix/Order.lean`, `Analysis/Matrix/HermitianFunctionalCalculus.lean`.
   (`LinearAlgebra/Matrix/PosDef.lean` still exists but holds only the algebraic
   half — no eigenvalues/det_pos.)
3. `posSemidef_iff_eq_transpose_mul_self` was REMOVED. The PSD infra is now
   CStarAlgebra/CFC-based; the Gram factor comes from
   `CStarAlgebra.nonneg_iff_eq_star_mul_self.mp hP.nonneg` (`+ star_eq_conjTranspose`).
4. The `Matrix.PosSemidef` CStarAlgebra instance and the Löwner order are **scoped**:
   need `open scoped MatrixOrder Matrix.Norms.L2Operator`.
5. Some `Matrix.add_apply` / `Matrix.one_apply_eq` / `Matrix.diagonal_apply_*` now
   need explicit `Matrix.` qualification (ambiguous otherwise).
6. New Lean module system: master files use `public import`. Plain `import` still
   works for a consuming file; a file added TO Mathlib would follow the new style.

## Bottom line

- **Submit-ready now (master-verified):** the four determinant-monotonicity /
  `one_le_det` lemmas in `PR_det_monotonicity_MASTER.lean`.
- **Drop:** PR1 (Schur) and the det_nonneg / posDef-bridge parts of PR2 — already upstream.
- **Remaining work:** Oppenheim, which needs the RCLike generalization first.
