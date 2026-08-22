# EXECUTION AMENDMENT E2 — self-generated exact benchmark route

**Status: WRITTEN BEFORE ANY BENCHMARK OR TARGET RUN UNDER THIS AMENDMENT.**
**Date: 2026-08-21.** Authorised by the steward via the team lead.

Parent prereg: `REG_HYDRO_COHERENT_ANNIHILATING_MC_PREREG.md` (`5f65a5b`)
Blocked-status report this amends: `LICENSE_GPU.md` (verdict
`BLOCKED-MISSING-BENCHMARK-DATA`)

## Why this amendment exists

The frozen L=7 LOW N=20 and MID N=25 configuration lists and their 32 per-configuration
exact M values are not in this repository and are unavailable to this workstream. The frozen
cascade cannot be run against them. This amendment substitutes an exact benchmark that this
workstream generates and computes itself.

**What this licenses and what it does not.** Passing the cascade under E2 licenses **this
implementation against exact ground truth on these cells** — it demonstrates that the
annihilating estimator reproduces exact coherent dynamics at a stated walker count on the
L=7 LOW and MID physical cells. It does **not** establish concordance with the primary
workstream's CPU license, because it is computed on different configurations.

**Concordance with the primary's CPU license remains OWED.** When the primary's 32
configuration lists and exact M values arrive, the cascade must be re-run against them. Any
discrepancy reopens this license. This is a debt recorded at the moment of issue, not a
caveat added afterwards.

## D1 — Declared sampling interpretation (the underdetermined choices)

The prereg fixes the rule ("Candidate modes are every directional mode on non-origin sites.
Sample N−2 distinct modes without replacement per configuration using NumPy PCG64") and the
seeds, but not the following. Each is DECLARED here, before generation:

1. **Global mode index.** `mode = (y*L + x)*6 + a`, with `a` the carries channel 0..5 and
   the axial site `(x, y)`. The origin site is `(0,0)`, i.e. site index 0.
2. **Candidate set and its order.** Every mode whose site index is not 0, enumerated in
   **ascending mode index**. Size `6*(L*L − 1)`. The origin site is excluded wholesale, per
   the finite-size prereg's "origin site excluded from initial spectator placement".
3. **Generator scope.** **One** `numpy.random.Generator(PCG64(seed))` per **cell**, drawn
   from **sequentially** for `config_index = 0, 1, …, 15`. The generator is NOT re-seeded per
   configuration.
4. **Draw mechanics.** `rng.choice(candidates, size=N-2, replace=False)` per configuration,
   the result then **sorted ascending** for storage. `choice(replace=False)` is used, not a
   `permutation` prefix.
5. **Uniqueness.** The prereg requires "16 unique spectator configurations". Configurations
   are compared as sets of modes; a duplicate would be discarded and the next draw taken.
   Whether any duplicate occurred is reported (none is expected).
6. **The initial pair.** The origin site carries channels 0 and 3 (local state 9) and counts
   toward N, so N−2 spectator modes are drawn.

## D2 — Declared witness conventions (BOTH are computed)

The frozen text does not state whether the three orientation probabilities are normalised by
the origin head-on-pair support before the total-variation witness is formed. Both are
computed from the **same stored runs**, for every configuration, at every W:

- **NORMALISED** — `p_j = q_j / (q_0+q_1+q_2)` in each arm, then `M = ½Σ|p_j^coh − p_j^deph|`.
- **RAW** — `M_raw = ½Σ|q_j^coh − q_j^deph|`, the unnormalised orientation probabilities used
  directly.

**The license is issued under NORMALISED**, the reading favoured by the recorded LOW-cell
classification. RAW is reported beside every number. The raw per-configuration
`q_coh`/`q_deph` vectors are stored for every batch, so that if the primary later answers
"raw", the license re-issues from the stored runs **without re-running anything**.

## D3 — Amended walker-count ladder

The prereg's candidates were W ∈ {500, 2,000, 10,000}; W=10,000 was the smallest passing and
is the recorded CPU license. This amendment tests

- **W = 10,000** (also the eventual CPU-concordance anchor),
- **W = 100,000**,
- **W = 1,000,000**.

The prereg's selection rule is unchanged: **the smallest W that PASSES is licensed**. All
three are reported whether or not a smaller one passes. W is fixed by this rule before any
held-out cell is inspected, and **is not changed after target inspection**.

## D4 — Gates, verbatim from the parent prereg

A W PASSES only if, over all 32 benchmark configurations:
median |M_MC − M_exact| ≤ 0.010; p90 ≤ 0.020; max ≤ 0.050; median MC SE ≤ 0.010;
p90 MC SE ≤ 0.020; max MC SE ≤ 0.050; LOW remains not low-memory; MID remains low-memory;
≤5 % of raw orientation estimates lie outside [−0.05, 1.05].

Low-memory means median M < 0.05 **and** at least 50 % of configurations have M < 0.05.

Target readability, at the licensed W: all 16 configurations return finite estimates;
median MC SE ≤ 0.015; p90 ≤ 0.030; maximum ≤ 0.050; ≤5 % of raw orientation estimates
outside [−0.05, 1.05]. A cell failing readability is `TARGET-STATISTICALLY-UNCONTROLLED`.

`DENSITY-SCALING-SUPPORTED` only if held-out LOW is not low-memory **and** held-out HIGH is
low-memory at **both** L=7 and L=9, with all SE gates passing. MID is diagnostic only and
cannot rescue a failed LOW/HIGH pair.

## D5 — Held-out cells

Generated under the **same** declared interpretation D1, from the prereg's frozen seeds,
**before** the licensing cascade is run:

- L=7 HIGH N=31, seed 2026082373
- L=9 LOW  N=32, seed 2026082391
- L=9 MID  N=42, seed 2026082392
- L=9 HIGH N=52, seed 2026082393

16 configurations each. Benchmark cells use seeds 2026082271 (LOW N=20) and 2026082272
(MID N=25) from the finite-size prereg.

All six lists are frozen to `configs/` with a sha256 manifest before the cascade runs, and
no held-out cell is executed before the license is recorded.

## D6 — Exact ground truth

Exact M is computed by this workstream's dual-validated exact engine: two independent
implementations agreeing to 2.2e-16 on 25 many-body configurations, both reproducing the
published L=11 N=2 carries-memory bridge at all 12 phases to every published digit. The
exact support cap is raised from the finite-size prereg's 2,000,000; the cap actually used,
and any configuration exceeding it, is reported. **A benchmark configuration whose exact M
cannot be computed is reported and excluded from the gate statistics, with the count stated**
— it is never replaced by another draw.

## D7 — Standing exclusions, unchanged

Finite-size model dynamics only. Nothing here is a fluid, a physical decoherence density, or
a world-physics result. This amendment changes only which exact configurations the estimator
is benchmarked against, never the microscopic law, the witness, the gates, or the
classification rule.
