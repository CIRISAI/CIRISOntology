# REG+ three-particle coherence survival — preregistration

**Status:** FROZEN BEFORE EXECUTION
**Date:** 2026-08-22

## Question

The exact two-particle bridge showed MEMORY-STRONG across measurement-free carries. Does
one additional indistinguishable particle generically preserve, attenuate, or erase that
route memory through ordinary local REG collisions?

This is an exact finite-sector dynamics test, not a hydrodynamic claim.

## Geometry and microscopic law

Periodic 5 x 5 axial triangular lattice, six Boolean directional modes per site (150 modes),
fixed total particle number N=3. Evolve the exact complex state vector in the three-particle
hard-core Fock sector. No mean-field factorization and no Born read occurs during the
coherent arm.

Use the same frozen local collision family as the prior holonomy and memory experiments:
theta=1.30 rad; one-state sectors identity; every local degenerate (N,Px,Py) sector receives
the corresponding frozen complex unitary; the zero-momentum head-on pair 3-state block is
H(Phi)=[[0,1,exp(-iPhi)],[1,0,1],[exp(iPhi),1,0]]. Streaming is the exact six-direction
carries permutation.

## Primary loop phase

Phi=30 degrees.

This was fixed because the prior preregistered two-particle bridge reports its largest
memory witness there, M=0.333345. No three-particle spectator result was inspected when
choosing it.

## Initial pair

At site (0,0), occupy the head-on pair directions (0,3).

## Spectator population

Enumerate EVERY one-particle mode not already occupied by the pair: all 148 allowed
(site,direction) placements. No placement may be removed because it looks exceptional.

## Timing

At t=0 apply the first local collision to the origin pair. Then evolve the full exact
three-particle state for five carries/collision cycles using the same global rule. The pair
branches return to the origin after five carries on the odd torus, but spectator-induced
intermediate collisions are allowed and are the object of the test. Immediately after the
return collision, read the origin head-on-pair orientation probabilities, marginalizing over
the spectator's location/direction.

## Arms

COHERENT: exact pure-state evolution from the post-first-collision coherent superposition.

DEPHASED: replace the post-first-collision pair superposition by the incoherent mixture of
its three route branches, with the same branch probabilities. Evolve each branch as an exact
pure state through the identical three-particle dynamics and average the final observable.

## Named witness

For each spectator placement s,

M3(s)=1/2 sum_j |p_coherent,j(s)-p_dephased,j(s)|,

where j are the three head-on pair orientations at the origin after return collision.

Primary summary numbers, all frozen:

- median M3 over all 148 placements,
- 10th and 90th percentiles,
- fraction with M3>0.20,
- fraction with M3<0.05.

The two-particle no-spectator benchmark M2=0.333345 is a fixed reference, not refit.

## Classification

ROBUST-MEMORY: median M3 >= 0.20 and at least 50% of placements have M3>0.20.

ENVIRONMENT-SENSITIVE: median M3 is between 0.05 and 0.20, or fewer than 50% exceed 0.20
while fewer than 50% fall below 0.05.

ENVIRONMENT-DEPHASED: median M3 <0.05 and at least 50% of placements have M3<0.05.

## Contact stratification — secondary but preregistered

Classify spectator placements by whether, in the corresponding no-collision ballistic
paths, the spectator intersects any of the three pair-route particle worldlines before the
return. Report the same M3 summaries separately for CONTACT and NO-CONTACT strata. This is
mechanistic interpretation; the all-placement classification above remains primary.

## Mechanical gates

- state norm error <1e-10 in every coherent run,
- probability sum <=1+1e-10 for the marginalized head-on observable,
- exact total N=3 sector throughout,
- all 148 spectator placements present in raw output.

## Standing exclusions

Finite exact lattice model only. A positive memory result does not establish coherent
many-body hydrodynamics; a dephasing result does not prove fundamental decoherence. The test
only asks whether one extra REG degree of freedom, interacting under the same local grammar,
is sufficient to wash out the route memory already established in the two-particle sector.
