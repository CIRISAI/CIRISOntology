# Mathlib upstream contributions — prepared, NOT submitted

Verified against **mathlib4 master @ `bbc4475e9e8fd25fbc8e26d636dd8b37be8f105a`**
(toolchain v4.33.0-rc1, full lake cache). Submission is Eric's call, under his
account. See `MASTER_FINDINGS.md` for the full master re-verification.

## Status (post-master-verification)

| Item | Status | File |
|---|---|---|
| Schur product theorem | **DROPPED — already upstream** as `Matrix.PosSemidef.hadamard` (+ `PosDef.hadamard`) | — |
| PSD `det_nonneg`, PSD→PosDef bridge | already upstream | — |
| **Determinant monotonicity + `1 ≤ det(1+Q)`** | ✅ **master-verified, SUBMIT-READY** | `PR_det_monotonicity_MASTER.lean` + `PR_det_monotonicity_description.md` |
| Oppenheim's inequality | **IN PROGRESS** — needs RCLike generalization (proved in our repo first) | `PR3_oppenheim.md` |

## The Schur product theorem was independently proved upstream

Our `hadamard_posSemidef` (Schur product theorem) is **already in Mathlib master**
as `Matrix.PosSemidef.hadamard` (`Analysis/Matrix/Order.lean`), added by the Mathlib
community in the ~2 years since our pinned v4.14. This is **external validation** of
our result, not a loss — the field converged on the same theorem, same name, same
Gram-factorization proof. We simply don't need to submit it.

## The one submit-ready PR

`PR_det_monotonicity_MASTER.lean` — four genuinely-new, master-verified lemmas:
`PosSemidef.one_le_det_one_add`, `PosDef.det_le_det_add`, `PosSemidef.det_le_det_add`,
and the idiomatic Löwner form `PosSemidef.det_le_det_of_le` (`A ≤ B ⇒ det A ≤ det B`).
Master built the Löwner order but never proved `det` monotone on it — this fills that
gap. Description + placement in `PR_det_monotonicity_description.md`. Leave staged for
Eric to open the PR.

## Oppenheim (in progress)

Still absent from master. Our ℝ proof is complete (`CIRISOntology/Core/Entropy.lean`).
Being generalized to `RCLike 𝕜` (Hermitian outer products) in the repo first — so the
complex-general theorem is kept — then ported to master using the rename map in
`MASTER_FINDINGS.md`. See `PR3_oppenheim.md` for the obstacle/plan.

## Superseded artifacts (kept for reference)

`PR1_schur_product.lean` / `PR1_description.md` (dropped — upstream),
`PR2_det_inequalities.lean` / `PR2_description.md` (the det_nonneg / posDef-bridge
parts are upstream; the monotonicity parts became `PR_det_monotonicity_MASTER.lean`),
verified against our pinned v4.14. `PR_det_monotonicity_MASTER.lean` is the
master-verified successor.

Files here are untracked artifacts in the repo `scratchpad/`; not committed to CIRISOntology.
