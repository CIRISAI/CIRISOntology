# FINITE-TIME REACHABILITY VS PROFILE CLASSES — RESULTS

Executed 2026-08-22 against frozen `FINITE_TIME_REACHABILITY_PREREG.md`.

First oracle-only run: GitHub Actions `32585841969`, artifact `9479015694`, ZIP SHA256 `a6aab0f7ec7a828a5c9a9ab3c7572f909363e10f50233d089c160c3a2eb1c1a1`.

Completed deployable-baseline run: GitHub Actions `32585962697`, artifact `9479078216`, ZIP SHA256 `802a33374997da848630306d60bf180815793cb36615e6a1b28d2bdb962b8577`.

## Gates

All implemented F1–F3 checks pass:

- every reduced-arm error is evaluated against the same full truth trajectory;
- smooth-ring vs deterministic scrambled-ring maximum error/dimension mismatch: `1.89e-15`;
- oracle POD error is monotone with rank;
- full snapshot rank reconstructs cavity population to a worst error `3.33e-15`.

## Dimension result

At max cavity-population error `<=1e-3`:

| N | profile classes | oracle POD | restarted local Krylov |
|---:|---:|---:|---:|
| 256 | 64 | 8 | 4 |
| 512 | 64 | 8 | 4 |
| 1024 | 64 | 8 | 4 |

The frozen online residual-enriched global-basis grid did **not** reach `1e-3` before its threshold/cap limits.

This establishes a strong **dimension** result: generic finite-time propagation uses a much smaller local Krylov space than the static profile-class representation. It does **not by itself establish a cost result**, because a full-space Krylov matvec acts on N+1 states while a class-space matvec acts on G+1 states.

## Frozen stakes from this screen

- P1, profile classes within 2× the online global dimension: **FAIL / not satisfied**; no online arm reached tolerance.
- P2, hidden low-rank finite-time dynamics: **PASS**; oracle POD rank is 8 while classes need 64.
- P3 N-stability:
  - profile classes: **PASS**;
  - restarted Krylov: **PASS**;
  - online global basis: **FAIL / no passing arm**.
- P4 time-dependence penalty: N=1024 restarted local Krylov dimension is **4**.

## Fairness correction before any solver-cost verdict

A post-result audit caught a material comparison issue before a SOTA conclusion was allowed.

The profile-class propagation in this screen used `scipy.expm_multiply` in dimension G+1, whereas the full arm used an in-house restarted Arnoldi kernel in dimension N+1. The recorded class `matvec_equiv` was only a placeholder based on dimension × steps and did not count the internal `expm_multiply` work. More importantly, comparing local Krylov dimension 4 directly with class dimension 64 ignores the different cost per Hamiltonian matvec.

For the frozen arrowhead Hamiltonian:

- FULL matvec cost scales with N;
- CLASS matvec cost scales with G.

At N=1024 and G=64, a 4-vector full Krylov step can therefore still cost more arithmetic than a somewhat larger class-space propagation. The dimension result is valid; the previous cost-level statement that the solver route was closed was too strong.

`FAIR_PROPAGATOR_COST_PREREG.md` was frozen after this audit and before a common-kernel comparison. It uses the same Arnoldi implementation on both FULL and CLASS arms, a hardware-independent sparse-matvec + orthogonalization proxy, and same-run wall-time replication.

**Current status:** solver-performance verdict is REOPENED pending that fair cost test. No SOTA claim is licensed.

## What the dimension result still tells us

The finite-time structure is strongly compressed relative to exact algebraic closure:

`exact closure N  >>  profile classes 64  >>  oracle POD 8`,

while local propagation needs only a four-vector Krylov space per time step.

This means exact algebra dimension, profile covering number, global trajectory rank, and local integrator dimension are four different complexity notions. Any claim about simulation advantage must state which one is being reduced and compare actual work at fixed physical error.

The open physics/computation question becomes: what controls each complexity scale — temporal bandwidth, spatial roughness, polariton filtering, time horizon, stochastic memory, or quantum-bath entanglement — and when does a reusable profile basis beat repeatedly constructing local reachable spaces?

## Fence

POD is an oracle diagnostic, not a deployable algorithm. Restarted Krylov is standard numerical prior art. This result is a valid dimension comparison and a warning against conflating basis size with computational cost. The fair common-kernel cost test is required before closing or reviving the profile-class solver route.
