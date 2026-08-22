# REG+ exact carries-memory bridge — preregistered result

Prereg commit: `716d1b4a873ac44922e4c0eb1675241304046f1f`

## Frozen verdict

**MEMORY-STRONG.**

In the exact two-particle head-on sector on the 11x11 odd torus, the three coherent
collision branches are streamed for eleven exact carries steps with no measurement and no
intervening collision, then reconverge and are collided again.

The preregistered total-variation witness

`M(Phi) = TV(p_coherent(Phi), p_dephased(Phi))`

is:

| Phi | M |
|---:|---:|
| 0 | 0.231078 |
| 30 | 0.333345 |
| 60 | 0.180601 |
| 90 | 0.031972 |
| 120 | 0.180601 |
| 150 | 0.333345 |
| 180 | 0.231078 |
| 210 | 0.333345 |
| 240 | 0.180601 |
| 270 | 0.031972 |
| 300 | 0.180601 |
| 330 | 0.333345 |

The >0.20 MEMORY-STRONG band is crossed at multiple adjacent nonzero bins as frozen.

Mechanical gates pass to floating precision: norm and probability sums are unity to
~1e-15; particle number is exact; odd-torus arithmetic forbids branch re-collision before
the named return.

## L=13 replication

The frozen L=13 geometry-period replication agrees pointwise exactly in M. Under the
phase-neutral carries permutation, changing odd L changes only the return time, not the
branch amplitudes; the pointwise absolute difference is 0.

## Critical interpretation guardrail

**This bridge proves persistent coherent route memory across carries, not uniquely
holonomic memory by M>0 alone.**

At flat phase Phi=0, M is already 0.231078. Coherence between alternative collision routes
therefore matters even without nonzero Wilson-loop angle.

The holonomy-specific content is that the surviving-memory read is strongly modulated by
Phi: M ranges from 0.031972 to 0.333345 over the frozen phase circle, and route chirality
changes with loop orientation. Those phase-modulation quantities are descriptive follow-up,
not a replacement for the preregistered witness.

## What this closes and what it does not

The local Born/dephasing boundary used in REG_HYDRO_WNONZERO is physically consequential:
removing it changes later observable route probabilities after an arbitrarily long
measurement-free carries interval.

This still does NOT establish the many-body coherent hydrodynamic limit. The exact bridge
contains two particles and phase-neutral spatial carries; it tests route-memory survival,
not viscosity.

The next earned experiment is therefore a many-body approximation that retains local
coherences across streaming, benchmarked against both this exact bridge and the replicated
locally-dephased viscosity result.
