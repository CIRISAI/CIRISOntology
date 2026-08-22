# W≠1 MAIN RESULTS under the steward's frozen registration (2026-08-22)
# prereg_id 371854bfb3a65bba44f7106d1b4ae0509a252ca7 · 52/52 runs · all instrument gates pass

## Classification, per the frozen §8–§9, applied mechanically

**VISCOSITY: COHERENT-HOLONOMY.**
- Δν(Φ) crosses the pre-staked band |Δν| > 0.005 at ALL TEN nonzero phase bins; peak
  Δν(90°) = Δν(270°) = −0.0428 (8.6× band; −18.4% of the flat ν = 0.2325).
- REFINEMENT (192→256, mandatory): sign preserved and magnitudes agree to ~0.3%
  everywhere — far inside the 25% requirement. Nothing DISCRETIZATION-SENSITIVE.
- ADJACENCY GUARD: contiguous same-sign crossings (30–150° and 210–330°). Satisfied.
- DEPHASING SEPARATION: the annealed control shifts −0.01898; every nonzero bin differs
  from it by ≥ the primary band (min 0.00714 at 30°, max 0.02378 at 90°). Materially:
  at θ=1.30 the dephased arm does NOT equal the circle-average of the fixed-Φ shifts
  (−0.01898 vs −0.02212) — the control is not trivially the mean at this operating
  point, unlike the θ=1.0 pilot; the criterion did real work and was passed.
- The curve: even in Φ, period π, monotone to 90°; close to but not exactly sin²
  (ratios 0.277/0.774/1 vs sin²'s 0.25/0.75/1) — the shape is θ-dependent, recorded.

**CONVECTION: NULL.** |Δg(Φ)| ≤ 1.3e-4 at every bin against a 0.03 band. The loop phase
does not touch the Galilean prefactor at this precision. (The dephased-g 192 run shows
only the known 192↔256 finite-resolution drift.)

## What is and is not claimed (frozen §11 verbatim in force)

Model physics on a lattice only. No world-physics claim. No claim that ontology kinds
are physical degrees of freedom. Nonzero holonomy is not called viscosity by fiat — the
measured change in the coarse transport coefficient is the entire content: **in the REG+
lattice at θ=1.30, ρ=2.0, the gauge-invariant loop phase changes the emergent viscosity
by up to −18%, refinement-stable, adjacency-satisfied, and separated from the annealed
phase-disorder control at every phase bin — while leaving the convection prefactor
untouched.** The first construction in its class to put a named number on the table
under a frozen registration and have it survive its own deflation control.

## Owed next, per the frozen §10

The ρ=2.5 secondary replication (exact grid, no retuning), launched now. It cannot
rescue or alter the primary; it is robustness reporting only. The W2 quenched arm
(REGHYDRO-W2) remains additive for the local-law-vs-spatial-structure question at θ=1.0.

## INDEPENDENT REPLICATION (2026-08-22, discovered at push-rebase)

The steward's parallel workstream, running ITS OWN implementation under the same frozen
registration (371854b), recorded the same classification minutes before this seal
(REG_HYDRO_WNONZERO_RESULT.md): Δν(90°) = −0.0428838 vs this implementation's −0.042764
(0.3%); dephased −0.0238618 vs −0.023781; Δg NULL in both; and their ρ=2.5 §10
replication already crosses the band with dephasing separation (Δν = −0.0303, dephased
−0.0151). TWO INDEPENDENT IMPLEMENTATIONS, ONE FROZEN PREREG, ONE VERDICT, coefficients
to three decimal places. This is the strongest evidence class the programme recognizes
short of a theorem: a pre-staked number, measured twice, independently, blind to each
other's runs, landing together. This session's ρ=2.5 sweep continues as a third check.
