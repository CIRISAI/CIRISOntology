# REG+ annihilating coherent Monte Carlo — preregistration

**Status:** FROZEN BEFORE EXECUTION
**Date:** 2026-08-22

## Purpose

The frozen independent-path complex Monte Carlo estimator reproduced exact LOW/MID data and
was controlled on L=7 HIGH and L=9 LOW, but became variance-uncontrolled in denser L=9 cells.
This experiment changes only the numerical representation, not the microscopic REG law.

The new estimator performs exact complex-weight annihilation between sampled histories that
arrive at the same basis configuration after every global cycle, followed by an unbiased
fixed-population resampling step. The goal is to reduce the phase/sign variance that defeated
the independent-path representation.

## Frozen microscopic dynamics

Identical to all preceding exact/coherent finite-size experiments:
- six hard-core directional carries on the triangular torus
- theta = 1.30 rad
- Phi = 30 degrees
- exact local conservation-sector unitaries
- exact carries permutation
- coherent arm and initially-dephased comparator
- same origin head-on-pair orientation probabilities and TV witness M
- evolve exactly L global carries/collision cycles before the read.

## Walker propagation

Each walker is one basis configuration and one complex weight. Local collision outputs are
sampled with q_k=|u_k|^2 and walker weight is updated by u_k/q_k. Carries are deterministic.
This is the same exact importance sampling used in the prior path-MC estimator.

## Annihilation and unbiased resampling

After every completed global collision cycle:

1. Aggregate all walkers with identical basis configuration c by complex summation:
   s_c = sum_{walkers at c} w.
2. This aggregation is the annihilation step; opposite/rotated phase contributions cancel
   before population control.
3. Let S = sum_c |s_c|. If S=0, the replica is declared ZERO-AMPLITUDE and the configuration
   is unreadable.
4. Sample exactly W new walkers independently with q_c=|s_c|/S.
5. A resampled walker at c receives weight
   w'_c = (S/W) * s_c/|s_c|.

Because q_c w'_c = s_c/W, the post-resampling walker-average amplitude is an unbiased
conditional estimator of the pre-resampling amplitude estimate. No phase is discarded and
no amplitude is threshold-pruned.

Perform this annihilation/resampling after every global cycle, including the last cycle
before the final probability estimator is formed.

## Quadratic observable estimator

Use two independent annihilating replicas A and B. Estimate final event probabilities with

P_hat(E) = Re sum_{c in E} conj(A_hat(c)) B_hat(c),

using the post-final-resampling amplitude maps. Same-replica |A_hat|^2 remains forbidden.
The dephased arm is the weighted sum of three separately propagated initial route branches.

## Batch structure and exact benchmark

For each configuration use 8 independent replica-pair batches, with the same deterministic
seed formula as the prior path-MC prereg, plus 50,000,000,000 to distinguish this estimator.

Benchmark against the exact paired L=7 LOW N=20 and MID N=25 configuration lists and exact M
values already frozen.

Candidate populations:
- W = 500
- W = 2,000
- W = 10,000

For each W report across all 32 exact benchmark configurations:
- median, p90, maximum |M_MC-M_exact|
- median, p90, maximum MC standard error
- LOW and MID aggregate low-memory classifications
- fraction of raw orientation-probability estimates outside [-0.05,1.05].

A W PASSES only if:
- median absolute error <= 0.010
- p90 absolute error <= 0.020
- maximum absolute error <= 0.050
- median MC SE <= 0.010
- p90 MC SE <= 0.020
- maximum MC SE <= 0.050
- LOW remains not low-memory
- MID remains low-memory
- <=5% of raw orientation estimates lie outside [-0.05,1.05].

Select the **smallest W that PASSES**. If none passes, verdict ANNIHILATING-MC-NOT-LICENSED.

## Held-out target cells

Because the previous estimator already exposed outcomes on the original finite-size target
configuration lists, this experiment uses NEW held-out configuration lists at the same
physical cells. They are generated before estimator licensing from fresh frozen seeds using
exactly the same uniform-without-replacement spectator sampling rule:

- L=7 HIGH N=31: seed 2026082373
- L=9 LOW N=32: seed 2026082391
- L=9 MID N=42: seed 2026082392
- L=9 HIGH N=52: seed 2026082393

Each cell has 16 unique configurations. These held-out lists are the only target data for
this estimator.

## Target readability and finite-size classification

At the licensed W, a held-out target cell is READABLE only if:
- all 16 configurations return finite estimates,
- median MC SE <= 0.015,
- p90 MC SE <= 0.030,
- maximum MC SE <= 0.050,
- <=5% of raw orientation estimates lie outside [-0.05,1.05].

Low-memory classification remains: median M<0.05 and at least 50% of configurations have
M<0.05.

DENSITY-SCALING-SUPPORTED only if held-out LOW is not low-memory and held-out HIGH is
low-memory at both L=7 and L=9. MID is diagnostic and cannot rescue a failed LOW/HIGH pair.

If a target cell fails readability, classify TARGET-STATISTICALLY-UNCONTROLLED and do not
increase W after target inspection.

## Standing exclusions

This is a stochastic numerical representation of the same finite coherent REG lattice model,
not a physical branching process. Passing held-out finite-size gates would support only a
finite-size density-scaling statement for the route-memory witness, not macroscopic quantum
coherence or world physics.
