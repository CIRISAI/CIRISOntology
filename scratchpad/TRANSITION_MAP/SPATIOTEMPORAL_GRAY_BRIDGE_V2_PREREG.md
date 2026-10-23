# SPATIOTEMPORAL GRAY BRIDGE V2 — CORRECTED FULL-GRID PREREG

Frozen 2026-08-22 after the staged pilot exposed a transition-frequency convention error and before any v2 full-grid code/output exists.

The original `SPATIOTEMPORAL_GRAY_BRIDGE_PREREG.md` is preserved unchanged. This v2 is a correction, not a retroactive edit.

## Correction licensed by the Hamiltonian

For resonant cavity-bright coupling G, the upper/lower polaritons have energies +/-G and the dark manifold lies at 0. The initialized upper polariton therefore transfers to dark states at the **polariton-dark gap**

`Delta_PD = G = Omega_R/2`,

not the full upper-lower Rabi splitting `Omega_R=2G` used in the original prereg.

## Finite-time second-order predictor

For zero-mean OU diagonal noise with

`E[xi_i(t)xi_j(0)] = sigma^2 S_ij exp(-|t|/tau_c)`

and the initialized upper polariton `(|c>+|B>)/sqrt(2)`, second-order perturbation theory predicts total dark population

`P2(t) = W sigma^2 integral_0^t (t-u) exp(-u/tau_c) cos(G u) du`,

where

`W = Tr(Q_D S)/N`

for uniform bright amplitudes.

This has no fitted coefficient. Its long-time slope is

`R_inf = W sigma^2 tau_c/(1+G^2 tau_c^2) = (W/2) J_OU(G)`.

The pilot showed that the finite-window slope, not R_inf, is required at long memory. Therefore the primary predictor is the OLS slope of `P2(t)` over the **same fixed window t in [1,4]** used for the simulated dark population.

## Frozen full grid

Use the same physical model and randomization plan as the original prereg:

- G=1;
- N in {32,64,128,256};
- spatial arms:
  - COMMON;
  - INDEPENDENT;
  - BLOCK-G, G in {2,4,8};
  - RING-EXP ell in {0.3,1,3,10};
- sigma in {0.02,0.05,0.1};
- tau_c in {0.02,0.05,0.1,0.2,0.5,1,2,5};
- T=20;
- at least 64 paired trajectories/cell;
- identical latent Gaussian seeds across spatial arms at fixed N,sigma,tau_c where dimensions permit;
- same stochastic OU construction and actual time-dependent Schrödinger propagation as the pilot.

The implementation may batch cells for runtime but may not change the grid after seeing results.

## Primary observables

For each cell:

- ensemble mean dark population trajectory;
- OLS dark-transfer slope over t in [1,4], `R_obs`;
- parameter-free finite-time perturbative slope `R_P2` from the analytic integral;
- asymptotic FGR slope `R_inf` as a secondary comparator;
- peak/final dark population and cavity population;
- Monte Carlo standard error for the fitted slope via trajectory bootstrap or per-trajectory slope distribution.

## Implementation gates

V1. COMMON bath dark population remains below 1e-8 in an explicit identical-noise control.

V2. Generated zero-lag spatial covariances reproduce target S within declared Monte Carlo tolerance; the pilot's 0.15 relative-Frobenius threshold remains the maximum allowed.

V3. The analytic finite-time integral is cross-checked against direct numerical quadrature to <1e-10 on a representative tau/t grid.

V4. At sigma=0, dark population remains at numerical floor for every spatial arm.

Failure voids scientific interpretation of affected cells.

## Scientific stakes

P1 — spatial factorization: at fixed N,sigma,tau_c, `R_obs` is nondecreasing with W across the spatial arms, allowing statistical ties. Require >=95% of nontrivial ordered comparisons to have the predicted sign, with no systematic reversed family.

P2 — weak-noise parameter-free accuracy: at sigma=0.02, over all non-common cells, median `|R_obs/R_P2-1| <= 0.10` and 90th percentile <=0.25.

P3 — sigma^2 perturbative scaling: from sigma=0.02 to 0.05, `R_obs/sigma^2` changes by <=15% in median over cells. Sigma=0.1 is explicitly allowed to leave the perturbative regime and is used to map breakdown.

P4 — finite-time memory necessity: on tau_c>=1 weak-noise cells, the finite-time predictor `R_P2` has at least 2x smaller median absolute fractional error than the asymptotic `R_inf`. If not, the pilot's apparent memory correction does not generalize.

P5 — corrected transition frequency: compare otherwise identical finite-time kernels using cos(G u) and cos(2G u). At sigma=0.02, the corrected G kernel must have at least 2x smaller median squared prediction error than the old 2G kernel. This directly audits the convention correction.

P6 — finite-size organization: for matched spatial scaling prescriptions, median `R_obs/R_P2` changes by <=15% from N=64 to N=256. RING-EXP at fixed ell is interpreted using its N-dependent W; no extra hidden rescaling is allowed.

P7 — breakdown map: at sigma=0.1, report where `|R_obs/R_P2-1| > 0.25`. If departures cluster by the dimensionless products `sigma*tau_c`, `G*tau_c`, dark population saturation, or another predeclared observable, that is an exploratory mechanism map, not a confirmatory law.

## Bridge meanings

- P1 fails: the spatial projector W is not a robust organizing variable even in the controlled stochastic surrogate.
- P1 passes but P2/P5 fail: the spatial bridge survives but the perturbative temporal kernel/frequency mapping is incomplete.
- P1/P2/P5 pass but P4 fails: asymptotic FGR is already sufficient; finite-time memory is not a distinct explanatory axis.
- P1-P6 pass: the classical colored-noise bridge survives strongly enough to justify a quantum-bath / HEOM confrontation.
- P3 or P7 shows systematic breakdown: the location of perturbative failure becomes the next physics target rather than being fitted away.

## External confrontation if bought

If P1-P6 pass, the next test is not another synthetic closed model. Compare the dimensionless spatial-temporal predictor against quantum-bath molecular-polariton calculations, especially the 2026 MPS-HEOM thermodynamic-convergence/phonon-timescale results. The target question is whether dark activation and/or N_T across partially correlated baths can be organized by the same spatial W combined with the relevant finite-time or spectral memory kernel.

## Fence

The second-order kernel is standard time-dependent perturbation theory specialized to the bright/dark geometry. Passing would establish a useful controlled bridge variable, not priority for perturbation theory, OU noise, FGR, or molecular-polariton dark-state physics.
