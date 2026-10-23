# APPROXIMATE BATH-EQUIVALENCE CLASSES — PREREG

Frozen 2026-08-22 after the exact dynamic-gray-algebra result and before the approximate-class simulation is written or run.

## Why this test exists

Two easier compression hypotheses have now failed their anti-hype gates:

1. closed/static soft-symmetry clustering loses to ordinary Krylov propagation;
2. low dynamic-bath generator/covariance rank does not imply a small invariant collective sector — one generic rank-1 diagonal profile already closes to all N emitters.

The exact dynamic result identifies the correct discrete invariant: the number of distinct complete emitter bath-coupling row profiles. Real molecular environments will rarely have exactly repeated rows, so the remaining computational question is whether **near-equivalent full profiles** give an error-controlled finite-time reduction.

## Model

Single-excitation cavity plus N emitters with uniform cavity coupling `g_i=1/sqrt(N)` and time-dependent diagonal disorder

`D(t) = sum_alpha xi_alpha(t) diag(a_alpha)`.

The emitter profile matrix A has row vectors `A_i=(a_1(i),...,a_r(i))`.

A partition into classes `C_m` replaces every row in a class by its class centroid `Abar_m`. The corresponding reduced cavity+class Hamiltonian has one collective class state per cluster, with cavity coupling `sqrt(|C_m|/N)` and time-dependent class energy `xi(t) dot Abar_m`.

## A priori defect certificate

For each emitter define row residual `e_i=A_i-Abar_class(i)`. For a given time,

`delta_i(t)=xi(t) dot e_i`.

The full-vs-clustered Hamiltonian perturbation is diagonal in emitter space, so

`||E(t)||_2 = max_i |delta_i(t)| <= ||xi(t)||_2 max_i ||e_i||_2`.

Define

`B_T = integral_0^T ||xi(t)||_2 dt * max_i ||e_i||_2`.

For unitary propagation from the same initial state, Duhamel gives the state-vector bound

`||psi(T)-psi_bar(T)||_2 <= B_T`

(and the same bound uniformly up to T using the truncated integral). The observed cavity-population error should therefore be <= `2 B_T + B_T^2`; this is conservative and is treated as a certificate, not an expected tight fit.

## Frozen constructions

`N = 128, 256, 512, 1024`, time horizon `T=20`, 200 equal time steps.

Two deterministic profile families, each with two temporal coordinates:

1. **SMOOTH-RING**:
   `A_i = (cos(2 pi i/N), sin(2 pi i/N))`.
   Every row is distinct, so the exact invariant sector is N-dimensional, but profiles lie on a smooth 1D manifold.
2. **SCRAMBLED-RING**:
   the same set of rows assigned to emitters by a fixed modular permutation. This has identical row geometry and therefore should be equally compressible by a row-profile compiler; it is a dye test against accidentally exploiting emitter ordering.

Temporal functions are fixed before execution:

`xi_1(t)=0.5 cos(0.7 t)+0.2 cos(1.9 t)`
`xi_2(t)=0.5 sin(0.7 t)+0.2 sin(1.3 t)`.

No stochastic averaging is used in this screen.

## Frozen clustering

Cluster by profile angle into `G in {4,8,16,32,64,128}` equal angular sectors. This is equivalent to clustering the complete two-coordinate row profiles, not instantaneous energies.

For each N/family/G report:

- max row residual;
- `B_T` and the resulting population-error certificate `min(1,2B_T+B_T^2)`;
- exact full-model cavity population vs reduced class-model population;
- max absolute population error and RMSE over the full trajectory;
- wall time for full and reduced propagation as descriptive only.

## Implementation gates

A1. G=N (tested separately at N=128) reproduces the full model at max population error <1e-10.

A2. SMOOTH-RING and SCRAMBLED-RING give the same reduced-model errors to <1e-10 for each N/G, because the physics is invariant under emitter relabeling.

A3. observed max cavity-population error never exceeds the frozen certificate by more than `1e-8` numerical slack.

Failure of A1-A3 voids interpretation.

## Scientific stakes

P1. Approximate profile classes are **finite-time useful** if at N=1024 some `G<=64` achieves max cavity-population error <=1e-3.

P2. The reduction is **N-stable** if the smallest G meeting 1e-3 changes by at most a factor 2 from N=256 to N=1024.

P3. This is NOT a simulation-SOTA claim even if P1/P2 pass. The model has only two smooth bath coordinates and no explicit non-Markovian hierarchy. Passing buys an implementation in an actual open-system representation (MPS-HEOM/HOPS/TTN-HEOM style) where the metric is solver-specific cost at fixed observable error.

P4. If no G<=128 meets 1e-3, approximate bath-equivalence is not promising even in this favorable smooth-profile control and the compiler route should be deprioritized.

## Chemistry/open-question fence

SMOOTH-RING is a geometric control, not a claim about a specific molecular cavity. Its purpose is to identify what must be measured from realistic molecular environments: the metric entropy / near-equivalence structure of complete molecule-to-bath coupling profiles over the bath coordinates that materially affect polariton dynamics. The empirical chemistry question is whether those profiles occupy a low-complexity manifold at the relevant spatial and vibrational correlation scales.
