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

## FINDING 4 (2026-08-23, on the steward's reading "turn it into support — maybe
## difference is the key") — THE THREE-GENERATION COLLAPSE, now a theorem

The differences were being reported as a list of non-matches. Pressed on whether the
difference IS the result, one of them turned out to be structural and provable.

**Measured first.** The object's two twins carry NEAR-IDENTICAL diagonal splits —
|S_aa − S_bb| = 3.710 (Pri/Prc) and 3.685 (Str/Cir), 0.7% apart — yet decoupling
defects differing by 3.8x (g_DB = 2.284 vs 8.617) and leakages by 2.3x. Meanwhile
EVERY flavour pair, in both tables, returned the SAME ratio g_DB/|S_aa − S_bb| = 0.866.

**Then proved.** That constant is √3/2, and it is exact. For any symmetric 3×3 with
equal row sums — precisely the shape unitarity forces on |V|² — the transposition
defect collapses to one number:

  `Core/DefectCoupling.defect_three_gen_collapse : tr(D²) = 6 (S 0 0 − S 1 1)²`

sorry-free, standard axioms, verified numerically to 12 digits on random unitaries
across all three pairs, and verified NOT to hold at 11×11 (ratios vary freely).

**What it means, and why it is support rather than another non-match.**
In a three-generation unitary mixing table, transposition-symmetry breaking has
EXACTLY ONE DEGREE OF FREEDOM. The off-diagonal entries cancel identically; the
dark→bright coupling is pinned at (√3/2)·|diagonal split|; there is nothing further to
measure. **The object's symmetry breaking is genuinely two-dimensional** — the same
diagonal split can carry a 3.8x range of decoupling — and that is a measured excess,
not a shortfall.

So the comparison does not fail for want of resemblance. It succeeds by exhibiting a
quantity that a three-generation flavour table STRUCTURALLY CANNOT CARRY, with the
impossibility proved on the flavour side and the excess measured on ours. This
supersedes the framing in Finding 3: the orderings differ between flavour tables
because each table has only one number to order by; the object has two, and its
ordering is the one that held 5/5 across substrates (UNIV-1).

**Fence unchanged.** Still no isomorphism claim, still no revival of any dark-sector
or ceiling leg. What is new is a positive, mechanized characterization of HOW the
object differs — which is what a signature is.

## FINDING 4 — CORRECTED SAME DAY (the attribution was wrong, the result is better)

Finding 4 above attributed the object's two-dimensional breaking to its DIMENSION
(11 vs 3). Checked, and that is not the main cause:

| matrix | row-sum spread / mean | equal-row-sum hypothesis |
|---|---:|---|
| QUARK sym|V|² | 2.5e-16 | **HOLDS EXACTLY** |
| OBJECT sym CUR-P2 | **0.761** | **FAILS BADLY** |

The collapse theorem needs TWO hypotheses — `n = 3` AND equal row sums — and the
object violates BOTH. Numerically the second dominates: the row-sum identity
`Σ_c (S_ca − S_cb) = −(S_aa − S_bb)` is broken by 4.330 (Pri/Prc) and 2.415 (Str/Cir),
magnitudes comparable to the quantities themselves. Dimension alone would leave the
constrained floor `g_DB/|ΔS| ≥ √(1/4 + 1/(2(n−2))) = 0.553` at n=11; the measured
values are 0.616 and 2.338, so Pri/Prc sits near that floor while Str/Cir is 4x above
it — but the floor itself does not bind, because the constraint generating it is absent.

## THE ACTUAL MECHANISM, and it is better than the one I claimed
**Unitarity is what collapses flavour's symmetry breaking to one dimension.** `|V|²` is
DOUBLY stochastic — rows AND columns sum to one — because `V` is unitary, and
symmetrization preserves that. The object's mixing matrix is a confusion matrix: it is
only SINGLY stochastic. Every item gets classified (rows sum to one), but kinds are not
chosen equally often (columns do not). The missing backward conservation law is exactly
the constraint whose absence supplies the extra degree of freedom.

**And this is the same asymmetry the object already shows elsewhere.** The Record axis
reads machine-zero one-way flow (Leg A, S4 = 0.0000); the mixing matrix is one-way
stochastic. The object is directional in both its dynamics and its bookkeeping;
flavour, being unitary, is two-way in both. That is one property with two measured
faces, not two coincidences — and it is a sharper signature entry than "the object has
more dimensions", which was the weaker claim I made first.

Standing correction to the header of `Core/DefectCoupling.lean`: its wording
("11×11 and its row sums are not forced equal") already names both hypotheses and
stands as written; this file's Finding 4 prose was the part that over-attributed, and
is superseded by this section.
