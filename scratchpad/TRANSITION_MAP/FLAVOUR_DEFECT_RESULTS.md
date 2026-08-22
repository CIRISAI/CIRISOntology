# FDA-1 RESULTS — Leg B's B2 row, re-measured on a theorem-fixed estimator (sealed 2026-08-23)

Prereg FLAVOUR_DEFECT_PREREG.md frozen before any flavour number was computed.
Runner `flavour_defect.py`; PDG 2026 values from the verified `legb_sources/`.

## Gates — PASS (as they must: the estimator is a theorem)
G-A `tr(D²) = 4(Sw·Sw) − 2α²` (Core/DefectCoupling.trace_defect_sq): worst residual
3.6e-12 across all eight pairs. G-B `g_DB = Δ_σ/(2√2)`: worst 3.2e-16. The pipeline
reproduces the mechanized identities on real physics matrices.

## The measurement (one estimator, both sides, dimensionless)

| table | pair | Δ_σ | g_DB | **L_spec** |
|---|---|---:|---:|---:|
| QUARK `sym|V_CKM|²` | gen 1–2 | 0.235 | 0.083 | **0.0002** |
| | gen 2–3 | 7.094 | 2.508 | 0.2628 |
| | gen 1–3 | 6.859 | 2.425 | 0.2375 |
| LEPTON `sym|U_PMNS|²` | gen 1–2 | 2.998 | 1.060 | 0.3377 |
| | gen 2–3 | 0.608 | 0.215 | **0.0093** |
| | gen 1–3 | 2.390 | 0.845 | 0.1716 |
| OBJECT `sym` CUR-P2 (11×11) | twin Pri/Prc | 6.461 | 2.284 | 0.2766 |
| | twin Str/Cir | 24.374 | 8.617 | 0.6434 |

## Finding 1 — each flavour table has EXACTLY ONE near-exactly protected pair,
## and it is a DIFFERENT pair in the two tables
Quark: the 1–2 pair reads L_spec = 2e-4 — interchangeable to two parts in ten
thousand. Lepton: the 2–3 pair reads 9e-3. The other two pairs in each table sit at
0.17–0.34. Mechanism differs and is visible in the matrices: the quark 1–2 protection
is a near-degeneracy of the diagonal (|V_ud|² and |V_cs|² agree to ~1e-4 under
unitarity with small θ13, θ23), while the lepton 2–3 protection is near-MAXIMAL θ23
(sin²θ23 = 0.561, close to 1/2). Same statistic, two different physical causes.

## Finding 2 — the sharpened B2, and it CORRECTS Leg B
Leg B's B2 row read the object's twins as matching "the multiplet pattern —
exact-in-theory, lifted-in-measurement", with the lifting magnitude placed in the
SU(3)-breaking range. On one theorem-fixed estimator that reading has to be narrowed:

**The object's twins are NOT in the magnitude class of flavour's protected pairs.**
Pri/Prc (0.277) and Str/Cir (0.643) sit with — and above — flavour's UNPROTECTED
generation pairs (0.17–0.34), and are 30x to 1400x more broken than either table's
protected pair. The FORM claim survives (exact by theorem under symmetrization, lifted
in measurement — `Core/DarkState.lean` supplies the exact zero). The MAGNITUDE claim
does not: our twins behave like flavour's ordinary pairs, not like its protected ones.
This supersedes B2's magnitude language, which had already required one correction
(the two-convention SU(3) splice); a theorem-fixed statistic removes that error class.

## Finding 3 — orderings are table-dependent, on both sides
Quark ordering: 2–3 > 1–3 > 1–2. Lepton: 1–2 > 1–3 > 2–3. The two tables do not agree
on which pair is most broken, exactly as the object's own leakage MECHANISM was found
to be substrate-dependent (K2.1: CUR-P2 vs CUR-SP). The object's ordering
(Str/Cir > Pri/Prc) is universal across ITS substrates (5/5, UNIV-1) — which is a
stronger internal regularity than either flavour table shows across its pairs, and is
recorded as a difference, not as support for anything.

## Fence (from the prereg, binding)
A 3×3 vs an 11×11 on a dimensionless statistic. No isomorphism, no shared mechanism,
no revival of `phase-at-ceiling` or any dark-sector leg. The single job was to put
B2 on a theorem-fixed footing, and the outcome was to narrow our own claim.
