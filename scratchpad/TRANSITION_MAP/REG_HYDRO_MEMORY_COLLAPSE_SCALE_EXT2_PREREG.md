# REG+ exact route-memory collapse scale extension II — preregistration

**Status:** FROZEN BEFORE EXECUTION
**Date:** 2026-08-22

## Parent result

The first collapse-scale search through N=12 returned NO-COLLAPSE-THROUGH-12, with median
M_12=0.093097 and 37.5% of configurations below 0.05.

## Question

Does the same frozen five-cycle route-memory witness cross the existing low-memory criterion
between total particle numbers N=13 and N=20?

## Frozen model

Everything is unchanged from prereg `81ae7bd3...`:

- 5x5 periodic axial triangular lattice
- six hard-core directional modes per site
- theta=1.30 rad
- Phi=30 degrees
- origin pair directions (0,3)
- exact conservation-sector complex unitaries
- exact carries permutation
- no Born read in coherent arm
- origin site excluded from initial spectator placement
- five carries/collision cycles
- same coherent-vs-initially-dephased TV witness M_N
- exact sparse support cap 2,000,000 with no pruning.

## Occupancy levels and sampling

Run N=13,14,15,16,17,18,19,20. At each N generate exactly 64 unique unordered spectator
mode-sets from the same 144 non-origin directional modes, without replacement within each
configuration.

Use NumPy PCG64 seeds:

- N=13: 2026082213
- N=14: 2026082214
- N=15: 2026082215
- N=16: 2026082216
- N=17: 2026082217
- N=18: 2026082218
- N=19: 2026082219
- N=20: 2026082220

Configuration lists are frozen raw artifacts.

## Primary endpoint

Use the same collapse criterion as the parent:

N_c is the FIRST tested N satisfying both:
- median M_N < 0.05
- at least 50% of configurations have M_N < 0.05.

COLLAPSE-LOCATED if an N_c exists.
NO-COLLAPSE-THROUGH-20 otherwise.
COMPUTE-LIMIT if >10% of one level exceed the exact sparse cap; no inference beyond the last
fully readable level.

All levels are reported even after a crossing is found.

## Named summaries

At each N: median, mean, p10, p90, fraction M>0.20, fraction M<0.05, min, max, median
coherent/dephased origin-pair support, maximum norm error, maximum sparse support, and the
same secondary ballistic-exposure Spearman correlation.

## Standing exclusions

Finite exact lattice model only. A crossing is a collapse scale of this five-cycle witness
on this 5x5 grammar, not a thermodynamic decoherence constant.
