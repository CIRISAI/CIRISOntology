# REG+ route-memory finite-size scaling — preregistration

**Status:** FROZEN BEFORE EXECUTION
**Date:** 2026-08-22

## Parent observation

On the 5x5 torus with a five-carries return, the preregistered first low-memory crossing was
N_c=13, descriptively 0.520 particles/site. A sustained low-memory regime appeared from
N=17 onward. This experiment asks whether that behavior tracks particles/site when the box
and route-return time are enlarged.

## Frozen microscopic law

Unchanged:
- six hard-core directional carries per site
- theta=1.30 rad
- Phi=30 degrees
- origin head-on pair directions (0,3)
- exact conservation-sector complex unitaries
- exact carries permutation
- coherent arm has no Born read
- dephased arm erases only the initial three pair-route coherences
- origin site excluded from initial spectator placement.

## Sizes and return time

Test odd periodic tori:
- L=7, read immediately after the 7th carries/collision return
- L=9, read immediately after the 9th carries/collision return.

The read time scales with L; it is not held at five cycles.

## Fixed occupancy bands

Use target particle densities d=N/L^2:
- LOW: d=0.40
- MID: d=0.52
- HIGH: d=0.64

Use nearest integer total N:

L=7:
- LOW N=20 (d=0.40816)
- MID N=25 (d=0.51020)
- HIGH N=31 (d=0.63265)

L=9:
- LOW N=32 (d=0.39506)
- MID N=42 (d=0.51852)
- HIGH N=52 (d=0.64198)

The initial pair counts toward N.

## Sampling

For each of the six size-density cells run exactly 16 unique spectator configurations.
Candidate modes are every directional mode on non-origin sites. Sample N-2 distinct modes
without replacement per configuration using NumPy PCG64.

Seeds:
- L7 LOW: 2026082271
- L7 MID: 2026082272
- L7 HIGH: 2026082273
- L9 LOW: 2026082291
- L9 MID: 2026082292
- L9 HIGH: 2026082293

Frozen configuration lists are raw artifacts and may not be altered after outcomes.

## Named witness and summaries

Same TV witness M between coherent and initially-dephased origin head-on-pair orientation
marginals at return.

Per cell report median, mean, p10, p90, fraction M>0.20, fraction M<0.05, min, max,
median origin-pair support, maximum norm error, maximum sparse support, and compute-limit
count.

Define a cell LOW-MEMORY if median M<0.05 and at least 50% of readable configurations have
M<0.05.

## Primary classification

DENSITY-SCALING-SUPPORTED if, at BOTH L=7 and L=9:
- LOW is not LOW-MEMORY, and
- HIGH is LOW-MEMORY,
with MID reported as the transition-band diagnostic (either state allowed).

DENSITY-SCALING-REFUTED if both sizes are readable but the LOW/HIGH ordering above fails at
one or both sizes.

COMPUTE-LIMIT if >25% of configurations in any required LOW or HIGH cell exceed the exact
support cap. In that case no density-scaling classification is issued beyond the readable
cells.

## Exact-compute cap

Sparse pure-state support cap = 2,000,000 basis configurations per coherent or branch run.
No amplitude pruning, tensor closure, or stochastic substitution is permitted. A run that
would exceed the cap is COMPUTE-LIMIT and stops before truncation.

## Standing exclusions

Finite-size model physics only. Even DENSITY-SCALING-SUPPORTED would identify a scaling
property of this REG lattice family, not a universal physical decoherence density. Failure
may indicate finite-box recurrence, insufficient samples, or a non-density control variable;
all are reportable outcomes.
