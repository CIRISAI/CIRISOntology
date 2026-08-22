# FLAVOUR DEFECT ATTACK (FDA-1) — FROZEN 2026-08-23 before any flavour number is computed

Purpose: re-run Leg B's twin/multiplet comparison with the NEWLY MECHANIZED estimator,
so that both sides are measured by ONE theorem-fixed quantity instead of by
convention-chosen percentages. Leg B's B2 row had to be corrected once already
(the "10-27%" band was a two-convention splice); a theorem-fixed estimator removes
that whole class of error.

## Why this is now possible
`Core/DefectCoupling.lean` proves, for ANY symmetric `H` and any reflection `w` with
`w ⬝ᵥ w = 2`:
  * `defect_eq` — the symmetry defect `D = H − PHP` is EXACTLY `w(Hw)ᵀ + (Hw)wᵀ − α wwᵀ`;
  * `trace_defect_sq` — `tr(D²) = 4 (Hw ⬝ Hw) − 2 α²`, with `α = w ⬝ᵥ Hw`.
`Core/DarkState.lean` proves the zero of the same quantity: under exact twin symmetry
the antisymmetric mode is a decoupled eigenvector. There is therefore NO estimator
freedom left to abuse: the numbers below are forced by the matrices.

## What is computed (identical procedure both sides)
For each symmetric mixing matrix `S` and each index pair `(a,b)`:
`w = e_a − e_b` (so `w·w = 2`), `D = S − PSP`, `Δ_σ = ‖D‖_F`, `g_DB = ‖(1−dd ᵀ)Sd‖`
with `d = w/√2`, and `L_spec = 1 − max_k |⟨v_k|d⟩|²` (spectral leakage of the
antisymmetric mode). Normalisation: every matrix is scaled so its off-diagonal mean
is 1, exactly as the object's coupling matrix was (PHYS_K11_PREREG.md U1), so the
comparison is of DIMENSIONLESS quantities.

## Sides
- OBJECT: the sealed curated confusion matrix (CUR-P2), twin pairs
  (Priorities,Process) and (Structure,Circumstances). Values already sealed —
  L_spec 0.0542 and 0.6247 — and used here only as the comparison arm.
- QUARK: `S = sym(|V_CKM|²)` from PDG 2026 (legb_sources/ckm26.txt, verified).
- LEPTON: `S = sym(|U_PMNS|²)` from PDG 2026 (legb_sources/numix26.txt, verified).
  Generation pairs (1,2), (2,3), (1,3) for both.

## Gates (pipeline must pass before any comparison is read)
G-A: the mechanized identity `tr(D²) = 4(Sw·Sw) − 2α²` reproduced numerically to
<1e-12 on every matrix and pair. This is a THEOREM, so failure means the code is
wrong, never the physics.
G-B: the K2 identity `g_DB = Δ_σ/(2√2)` reproduced to <1e-12 (independent check of
the same algebra by a different route).

## Staked readings (before computation)
- S1 ORDERING: does either flavour table show a leakage ordering across its three
  generation pairs, and does the ordering track the mixing hierarchy? Any ordering is
  descriptive; NO claim of correspondence with the object's twin ordering may be made
  from a 3-pair vs 2-pair comparison — the sample is too small to order jointly.
- S2 SCALE: report the object's twin leakages and flavour's generation leakages on the
  same axis. This REPLACES Leg B's B2 percentage comparison. If flavour's leakages
  bracket the object's, say so; if they are orders apart, say that.
- S3 NULL EXPECTATION: a matrix with exactly degenerate diagonal in the pair and
  symmetric off-diagonals has ZERO defect (DarkState). So a small leakage means
  "this pair is nearly interchangeable in the mixing data", nothing more.
- ANTI-HYPE, binding: this compares a 3×3 to an 11×11 on a dimensionless statistic.
  It licenses NO isomorphism claim, NO shared-mechanism claim, and cannot revive
  `phase-at-ceiling` or any dark-sector leg. Its only job is to put Leg B's B2 row on
  a theorem-fixed footing.
