# REG+ exact route-memory density ladder — preregistration

**Status:** FROZEN BEFORE EXECUTION
**Date:** 2026-08-22

## Question

The exact N=2 bridge showed MEMORY-STRONG, and the exact N=3 spectator test showed
ROBUST-MEMORY across one additional interacting particle. Does the same coherent route
memory collapse, remain finite, or stay essentially intact as environmental occupancy is
increased under the same exact REG local grammar?

This is an exact/sparse finite-sector dynamics test, not a fluid or world-physics claim.

## Frozen microscopic law

Use the same six-carry 5x5 periodic axial triangular lattice and the same local complex
collision family already frozen and tested:

- theta = 1.30 rad
- Phi = 30 degrees
- one-state local sectors identity
- every degenerate local (N,Px,Py) sector receives the same conservation-preserving unitary
- the N=2, P=0 three-route block is
  H(Phi)=[[0,1,exp(-iPhi)],[1,0,1],[exp(iPhi),1,0]]
  and U=exp(-i theta H)
- streaming is the exact six-direction carries permutation
- no Born read occurs in the coherent arm.

The first origin head-on pair is directions (0,3). The entire origin site is excluded from
spectator placement at the post-first-collision start, matching the N=3 domain correction.

## Density ladder

The established anchors are reported unchanged:

- N=2: M2 = 0.3333452470 from the exact no-spectator bridge
- N=3: exhaustive 144-placement result, median M3 = 0.3333452470

New exact sparse runs use total particle numbers:

- N=4: 2 spectators
- N=5: 3 spectators
- N=6: 4 spectators

For each new N, run exactly 64 frozen spectator configurations.

## Frozen spectator sampling

Candidate spectator modes are the 144 directional modes on the 24 non-origin sites.
Within one configuration, sample k=N-2 distinct modes without replacement. Multiple
spectators may occupy the same site if their directional modes differ; that is part of the
exact local Fock state and is not rejected.

Use NumPy PCG64 with the following seeds:

- N=4: 2026082204
- N=5: 2026082205
- N=6: 2026082206

Generate configurations sequentially from each RNG and reject only duplicate unordered
mode-sets. Stop after 64 unique configurations. The generated configuration lists are raw
artifacts and may not be altered after outcomes are known.

## Timing and arms

Apply the first local collision to the origin pair, producing the same three-route coherent
superposition as the prior bridge. Spectators are then tensored in as occupied modes.

Evolve for five exact global cycles:

  carries permutation -> simultaneous local conserved-sector collision at every occupied site.

At the fifth collision, immediately read the three origin head-on-pair orientation
probabilities, marginalizing over all spectator degrees of freedom.

COHERENT arm: exact sparse pure-state evolution from the post-first-collision route
superposition.

DEPHASED arm: erase only the three initial pair-route coherences after the first collision,
retain the same branch probabilities, evolve each branch through the identical many-particle
unitary dynamics, and average the final marginal probabilities.

## Named witness

For each spectator configuration s at total particle number N,

M_N(s) = 1/2 * sum_j |p_coherent,j(s)-p_dephased,j(s)|,

where j are the three origin head-on pair orientations after the fifth collision.

For every N report:

- median M_N
- mean M_N
- 10th and 90th percentiles
- fraction M_N > 0.20
- fraction M_N < 0.05
- minimum and maximum
- median origin-pair support sum in coherent and dephased arms.

The origin-pair support is secondary. M_N remains the primary witness even when interactions
move amplitude away from the returning-pair subspace.

## Primary ladder classification

ROBUST-THROUGH-N6:
- median M_6 >= 0.20, and
- at least 50% of N=6 configurations have M_6 > 0.20.

COLLAPSE-BY-N6:
- median M_6 < 0.05,
- at least 50% of N=6 configurations have M_6 < 0.05, and
- the medians satisfy M_3 >= M_4 >= M_5 >= M_6.

DENSITY-SENSITIVE:
- anything between those two outcomes, including non-monotone behavior.

The N=2 and N=3 anchors cannot be re-fit or replaced.

## Secondary survival-law fit

After the primary classification only, fit the median ladder N=3..6 to both:

1. exponential: M_N = A exp[-gamma (N-3)]
2. affine floor: M_N = M_inf + B/(N-2)

Report both residuals. Neither fit changes the primary verdict and neither may be called a
law from four points.

## Mechanical gates

For every coherent and branch run:

- norm error < 1e-10
- exact total particle number N
- no duplicate hard-core mode in a basis configuration
- marginalized origin-pair probability sum <= 1 + 1e-10
- all 64 frozen configurations present for each N unless a declared COMPUTE-LIMIT occurs.

The sparse exact state support is capped at 2,000,000 basis configurations per run. If that
cap would be exceeded, stop that configuration before truncation and classify it
COMPUTE-LIMIT; do not prune amplitudes and do not substitute an approximation. If more than
10% of configurations at one N hit COMPUTE-LIMIT, no primary classification is issued for
that N.

## Standing exclusions

Finite exact lattice model only. ROBUST-THROUGH-N6 would not establish macroscopic coherent
hydrodynamics; COLLAPSE-BY-N6 would not prove fundamental decoherence. The experiment only
measures how rapidly the already-established REG route-memory witness survives increasing
exact local occupancy under this fixed grammar.
