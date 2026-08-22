# W2 PREREG — the quenched arm: local-parameter law or spatial phase structure?
# FROZEN 2026-08-22, before the quenched implementation or any run existed.
# prereg_id: REGHYDRO-W2-20260822

## What this run can and cannot adjudicate, stated first

In the R1 closure (Born read after each collision; no phase carried across streaming),
phi enters only as a parameter of each site's local stochastic collision |U(phi)|^2.
The W1 sweep measured nu(phi) = nu0 - 0.0105 sin^2(phi). The quenched arm decides
BETWEEN: (a) this is a POINTWISE LOCAL-PARAMETER LAW that self-averages over a random
static phi field — in which case the W1 "holonomy" naming OVERREACHES at this closure
(the deflationary reading is CONFIRMED: any local collision parameter with that profile
would do; loop-coherence language is not earned), reported at full volume; or (b) a
spatially random phi field produces transport BEYOND the self-average — spatial phase
structure matters, a named residual pointing at genuine loop physics. FULL coherence
attribution requires phase-carrying streaming (the R3 successor, specced separately);
this run cannot deliver it and will not claim it.

## Design

Arm Q: static phi_x i.i.d. uniform on the 48-bin grid (same marginal as W1's annealed
arm), per-site transition T(theta=1, phi_x), THREE seeded realizations (20260822+r).
Experiment: nu, modes 1 and 2, grid/rho/windows exactly as the committed flat configs.
Reference values from W1 (frozen): mean-field shift -0.00525 (the sin^2 average);
instrument floor 0.00085.

## Bands (evaluated on the mean over realizations, scatter reported)

- LOCAL-LAW CONFIRMED: |mean Delta-nu_Q - (-0.00525)| < 3 x max(floor, realization SD)
  -> (a) fires. The sin^2 curve stands as a measured local law; holonomy language is
  retracted for the R1 closure at full volume; the phase-carrying successor becomes the
  only route to a coherence claim.
- SPATIAL STRUCTURE: the difference exceeds the band -> (b): named residual, direction
  and magnitude reported, phase-carrying successor prioritized.
- FIXED-POINT-DESTROYED: reportable as itself.

Implementation is a NEW file (quenched_ext.py) importing the hash-pinned
regplus_hydro.py unmodified.
