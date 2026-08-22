# REG+ exact route-memory collapse scale — preregistration

**Status:** FROZEN BEFORE EXECUTION
**Date:** 2026-08-22

## Parent result

The preregistered density ladder through N=6 (`b6438126...`, result `9de7c430...`) was
DENSITY-SENSITIVE: median M stayed 0.333345 through N=5 and fell to 0.147472 at N=6.

## Question

At what higher exact occupancy, if any by N=12, does the same route-memory witness enter the
pre-existing low-memory band?

## Frozen law and geometry

Unchanged from the parent density ladder:

- 5x5 periodic axial triangular lattice
- six hard-core directional modes per site
- theta=1.30 rad
- Phi=30 degrees
- origin pair directions (0,3)
- identical conservation-sector complex unitaries
- exact carries permutation
- no Born read in the coherent arm
- entire origin site excluded from spectator placement at the post-first-collision start
- five exact global carries/collision cycles
- same coherent and initially-dephased arms
- same origin head-on-pair TV witness M_N.

## New occupancy levels

Run total particle numbers N=7,8,9,10,11,12, corresponding to 5..10 spectators.

At each N generate exactly 64 unique unordered spectator mode-sets from the same 144
non-origin candidate modes, sampling without replacement within a configuration.

Use NumPy PCG64 seeds:

- N=7: 2026082207
- N=8: 2026082208
- N=9: 2026082209
- N=10: 2026082210
- N=11: 2026082211
- N=12: 2026082212

Generated configuration lists are frozen raw artifacts and may not be altered after outcomes
are known.

## Named summaries

At every N report median, mean, p10, p90, fraction M>0.20, fraction M<0.05, min, max,
median coherent/dephased origin-pair support, maximum norm error, and maximum sparse support.

## Primary collapse-scale classification

Define N_c as the FIRST tested N in 7..12 satisfying both:

- median M_N < 0.05
- at least 50% of configurations have M_N < 0.05.

COLLAPSE-LOCATED: such an N_c exists. Report the first one only as the primary scale, while
still reporting all later levels.

NO-COLLAPSE-THROUGH-12: no tested N satisfies both conditions.

COMPUTE-LIMIT: more than 10% of the 64 configurations at any N hit the exact sparse support
cap before the named read. No inference is made beyond the last fully readable N.

No monotonicity requirement is imposed on this extension; the parent already showed a broad,
configuration-dependent distribution.

## Secondary interaction-exposure summary

For each initial spectator configuration compute the number E of spectator ballistic
worldline intersections with any of the six pair-route particle worldlines over t=1..4,
ignoring collision deflections. Report Spearman correlation between E and M_N at each N.
This is mechanistic secondary analysis only and cannot alter the collapse classification.

## Mechanical gates

Same as parent: exact N, no duplicate hard-core modes, norm error <1e-10, origin marginal
probability <=1+1e-10, all 64 configurations unless a declared COMPUTE-LIMIT occurs.

Sparse support cap remains 2,000,000 basis configurations per run. No amplitude pruning or
other approximation is permitted.

## Standing exclusions

Finite exact lattice model only. A located collapse scale is not a thermodynamic decoherence
constant; no-collapse-through-12 is not evidence of macroscopic coherence. The experiment
only identifies the occupancy range in which this fixed finite REG route-memory witness is
washed out under the frozen local grammar.
