# REG+ coherent path Monte Carlo — preregistration

**Status:** FROZEN BEFORE EXECUTION
**Date:** 2026-08-22

## Purpose

The frozen norm-budgeted amplitude-pruning representation was accurate on exact LOW/MID
benchmarks but became APPROXIMATION-UNCONTROLLED on the first L=7 HIGH target. This experiment
changes representation rather than retuning that failed approximation.

The new representation samples exact microscopic collision histories with complex weights.
No basis amplitude is deterministically dropped because it is small. The approximation is
statistical Monte Carlo error only.

## Frozen microscopic law

Identical to the exact finite-size model:
- six hard-core directional carries on the triangular torus
- theta = 1.30 rad
- Phi = 30 degrees
- exact local conservation-sector unitaries
- exact carries permutation
- coherent arm and initially-dephased comparator
- same origin head-on-pair TV witness M
- return after L global carries/collision cycles.

## Unbiased amplitude path estimator

A walker is one basis configuration plus one complex weight.

For the coherent arm, sample the initial head-on route j with probability
q_j = |a_j|^2, where a_j is the exact post-first-collision amplitude. Initialize walker
weight w=a_j/q_j.

At every subsequent local collision, for a basis input state with exact unitary column
coefficients u_k, sample output k with q_k=|u_k|^2 and update

w <- w * u_k/q_k.

For simultaneous collisions at different sites, sample each local output independently;
this is exact because the global local-collision block factorizes over sites.

Carries are exact deterministic permutations and do not change walker weight.

For W walkers, the amplitude estimator for final basis configuration c is

A_hat(c) = (1/W) sum_{walkers ending c} w.

Use TWO independent walker replicas A and B. Estimate an event probability by the real
replica cross product

P_hat(E) = Re sum_{c in E} conj(A_hat(c)) B_hat(c).

The independent-replica product is the frozen estimator; same-replica |A_hat|^2 is forbidden
because of its positive finite-W bias.

For the dephased arm, run each of the three initial route branches separately with fixed
initial configuration and unit weight, use the same independent-replica estimator, then
combine final probabilities with the exact frozen branch probabilities |a_j|^2.

## Batch structure and seeds

For each configuration and each candidate walker count, run 8 independent replica-pair
batches. The reported M is the mean over the 8 batch M estimates; its Monte Carlo standard
error is sample_sd(M_batch)/sqrt(8).

Seeds are generated deterministically as

seed = 202608220000 + 1000000*L + 10000*N + 100*config_index + 10*batch + replica,

with replica=0,1. Branch-specific dephased runs add 1,000,000,000*(branch+1).

## Candidate walker counts

Benchmark exactly:
- W = 2,000
- W = 10,000
- W = 50,000

No other W may be introduced after target outcomes are inspected.

## Exact benchmark gate

Use the same exact frozen L=7 configuration lists and exact M values:
- LOW: N=20, 16 configurations
- MID: N=25, 16 configurations.

For each candidate W over all 32 paired configurations report:
- median |M_MC - M_exact|
- 90th percentile absolute error
- maximum absolute error
- median MC standard error
- 90th percentile MC standard error
- LOW and MID aggregate low-memory classifications.

A walker count PASSES only if:
- median absolute error <= 0.010
- p90 absolute error <= 0.020
- maximum absolute error <= 0.050
- median MC SE <= 0.010
- p90 MC SE <= 0.020
- LOW remains not low-memory
- MID remains low-memory.

Select the **smallest W that PASSES**. If none passes, classify PATH-MC-NOT-LICENSED and
stop before target execution.

## Target execution after licensing

Only after W is licensed, run the frozen target configuration lists:
- L=7 HIGH, N=31, 16 configs
- L=9 LOW N=32, MID N=42, HIGH N=52, 16 configs each.

A target cell is READABLE only if:
- all 16 configurations return finite estimates,
- median MC SE <= 0.015,
- p90 MC SE <= 0.030,
- no configuration has MC SE > 0.050.

Use the existing finite-size classification: DENSITY-SCALING-SUPPORTED only if LOW is not
low-memory and HIGH is low-memory at both L=7 and L=9. MID remains diagnostic.

For aggregate low-memory classification use the 16 configuration mean-M estimates exactly as
in the exact prereg: median M<0.05 and at least 50% M<0.05.

## Deflation / sanity controls

On the exact benchmark report the fraction of raw probability estimates outside [0,1]. They
are not clipped before M computation. If more than 5% of orientation probability estimates
are outside [-0.05,1.05] at the selected W, classify ESTIMATOR-UNSTABLE and stop.

Also run the coherent arm with all collision phases replaced by their magnitudes |u_k| on the
first LOW configuration only. This is a diagnostic phase-erasure control and is not used for
walker-count selection.

## Standing exclusions

This is a stochastic numerical representation of a finite coherent lattice model, not a new
physical stochastic law. Passing the benchmark licenses only the named estimator at the
frozen W and finite sizes. Monte Carlo variance, sign/phase cancellation, and finite-size
recurrence remain explicit limitations.
