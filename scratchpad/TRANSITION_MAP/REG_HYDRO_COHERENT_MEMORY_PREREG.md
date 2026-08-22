# REG+ exact carries-memory bridge — preregistration

**Status:** FROZEN BEFORE EXECUTION
**Date:** 2026-08-22

## Question

Does the loop-phase information that changed the locally-dephased hydrodynamic viscosity
survive an interval of exact, measurement-free `carries`, so that it can interfere again
when alternative conserved routes reconverge?

This is a bridge experiment, not a viscosity measurement. It tests the approximation that
was still present in REG_HYDRO_WNONZERO: local Born/dephasing after every collision.

## Exact sector

Use the exact two-particle hard-core occupation Hilbert sector of the same six-carry
triangular lattice. The lattice is an 11 x 11 periodic axial torus. There are 6*121 modes
and C(726,2) exact two-particle basis states. No product-state or molecular-chaos closure is
used in this bridge.

The local collision is the already-frozen theta=1.30 rad REG family. When both particles
occupy one site, the exact N=2 local block is applied. In particular, the zero-momentum
head-on pair sector is the three-route unitary

H(Phi) = [[0,1,exp(-i Phi)], [1,0,1], [exp(i Phi),1,0]],
U(Phi) = exp(-i theta H(Phi)).

All other exact N=2 conservation sectors use the same block structure already fixed by the
reference implementation. One-particle local sectors are identity. Streaming is the exact
six-direction carries permutation. No Born read occurs in the coherent arm.

## Initial state

At cycle 0, one exact head-on pair is localized at axial site (0,0), in direction pair
(0,3). Norm=1 exactly.

## Why L=11

For odd L, two particles sent into opposite directions from one site do not reoccupy one
site at any t=1..L-1. At t=L, each opposite-route branch returns to the origin. Thus the
first route reconvergence after the initial collision occurs after exactly 11 carries
steps, preventing an earlier collision from confounding the memory witness.

## Frozen phase grid

Phi = 0,30,60,90,120,150,180,210,240,270,300,330 degrees.

## Arms

1. COHERENT: exact state-vector evolution; no measurement between first and return collision.
2. DEPHASED: after the first collision only, erase coherences between the three head-on
   route branches while retaining their probabilities; propagate each branch through the
   identical carries interval and apply the identical second collision.
3. PHASE-RANDOMIZED: same as COHERENT, but the second collision phase is averaged uniformly
   over the same 12-point phase circle. This is a disorder/unknown-phase comparator, not a
   replacement for the DEPHASED arm.

## Read time

Apply the first collision at cycle 1, then 11 exact carries steps with no intervening
collision because the branches are spatially separated, then apply the second collision
at reconvergence. Read immediately after that second collision and before the next stream.

## Named number

Let p_coh(Phi) and p_deph(Phi) be the three probabilities for the three outgoing head-on
pair orientations after the second collision.

The primary memory witness is total-variation distance

M(Phi) = 1/2 * sum_j |p_coh,j(Phi)-p_deph,j(Phi)|.

Secondary, fully reported: signed route chirality C=p_+ - p_- in each arm.

## Gates and classifications

Mechanical gates: norm error <1e-12; probability sum error <1e-12; exact two-particle
number conservation; no branch re-collision before t=11.

MEMORY-SURVIVES: M(Phi)>0.05 at at least two adjacent nonzero phase bins.
MEMORY-STRONG: M(Phi)>0.20 at at least two adjacent nonzero phase bins.
MEMORY-NULL: max M(Phi)<0.01.
INTERMEDIATE: anything between those bands.

All 12 phase points are reported. No phase may be dropped.

## Replication

If MEMORY-SURVIVES, repeat unchanged on L=13. The named read is then after 13 carries steps.
The phase dependence must agree pointwise to absolute M difference <=0.01. The replication
is a geometry-period check only and cannot rescue the primary.

## Standing exclusions

This is exact model dynamics in a two-particle sector, not a fluid or world-physics result.
A positive result says only that local REG route phase can remain physically consequential
after exact carries when the alternatives later reconverge. It does not establish that the
previous viscosity shift survives in the many-body fully coherent hydrodynamic limit.
