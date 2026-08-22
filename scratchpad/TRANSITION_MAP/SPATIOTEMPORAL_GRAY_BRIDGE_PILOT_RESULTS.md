# SPATIOTEMPORAL GRAY BRIDGE — PILOT RESULTS

Executed 2026-08-22 as a staged implementation/trend pilot under `SPATIOTEMPORAL_GRAY_BRIDGE_PREREG.md`.

GitHub Actions run `32586261092`; artifact `9479136605`; ZIP SHA256 `95679de0bc9030b2ae83350c5f7b6f602a3f7190213efdac5dc0509dfa26efda`.

This pilot was explicitly not allowed to adjudicate the full frozen P1–P4 grid.

## Implementation gates

Both pilot gates pass:

- explicit common scalar OU noise keeps the dark population at a worst numerical residue `7.77e-16`;
- generated spatial covariance matrices reproduce targets to worst relative Frobenius error `0.127`, inside the frozen pilot tolerance `0.15`.

## Spatial result

The physical spatial factor

`W = Tr(Q_D S)/N`

orders the observed early dark-transfer slope correctly in **all six** nontrivial pilot cells (N=32,64 and tau_c=0.1,0.5,2):

`COMMON < BLOCK4 < RING3 < INDEPENDENT`,

with common-bath transfer at numerical floor.

Representative N=64 values:

| tau_c | arm | W | observed slope |
|---:|---|---:|---:|
| 0.1 | BLOCK4 | 0.750 | 1.879e-4 |
| 0.1 | RING3 | 0.905 | 2.258e-4 |
| 0.1 | INDEPENDENT | 0.984 | 2.458e-4 |
| 0.5 | BLOCK4 | 0.750 | 7.127e-4 |
| 0.5 | RING3 | 0.905 | 8.732e-4 |
| 0.5 | INDEPENDENT | 0.984 | 9.721e-4 |
| 2.0 | BLOCK4 | 0.750 | 1.024e-3 |
| 2.0 | RING3 | 0.905 | 1.295e-3 |
| 2.0 | INDEPENDENT | 0.984 | 1.444e-3 |

The spatial projector diagnostic therefore survives its first actual time-dependent stochastic dynamics test.

## Temporal mismatch exposed a preregistration convention error

The original prereg predictor used the full polariton splitting `Omega_R=2G` in the OU spectral density. But the pilot initializes an on-resonance upper polariton

`|UP>=(|c>+|B>)/sqrt(2)`,

whose energy is `+G`, while the dark manifold is centered at zero. The relevant UP->dark transition frequency is therefore

`Delta_PD = G = Omega_R/2`,

not the upper-lower splitting `2G`.

The original temporal stake is consequently a design/convention error and is not interpreted as a physics falsification. The prereg remains preserved; a corrected v2 test is frozen separately before any full-grid execution.

## Finite-time memory explains the apparent tau_c=2 enhancement

There is a second issue with comparing the pilot's finite-window slope to the asymptotic golden-rule rate.

At weak classical diagonal noise, second-order perturbation theory for the initialized upper polariton gives the parameter-free dark population

`P_D^(2)(t) = W sigma^2 integral_0^t (t-u) exp(-u/tau_c) cos(G u) du`.

Its long-time derivative is

`R_inf = W sigma^2 tau_c/(1+G^2 tau_c^2) = (W/2) J_OU(G)`,

but the pilot fits a slope over t in [1,4]. For long memory, that finite-window slope can substantially exceed the asymptotic rate because the oscillatory memory kernel has not yet accumulated its later cancelling contributions.

Using the same [1,4] OLS window, the second-order finite-time kernel predicts, before any fitted prefactor:

- tau_c=0.1: base W=1 slope `2.475e-4`;
- tau_c=0.5: `1.009e-3`;
- tau_c=2: `1.529e-3`.

Multiplying only by the known W gives close agreement with the pilot. For N=64 INDEPENDENT (W=0.984):

- tau_c=0.1: predicted ~`2.44e-4`, observed `2.46e-4`;
- tau_c=0.5: predicted ~`9.93e-4`, observed `9.72e-4`;
- tau_c=2: predicted ~`1.50e-3`, observed `1.44e-3`.

The same pattern holds at N=32. Thus the pilot suggests that the spatial factorization survives and that the temporal discrepancy is largely a **finite-time non-Markovian memory effect** plus the corrected polariton-dark gap convention.

## What is and is not learned

Learned:

1. common-bath protection is exact in the implemented stochastic dynamics;
2. W correctly orders spatial dark activation across partially correlated baths;
3. the relevant spectral gap for polariton->dark transfer is the polariton-dark gap, not the full Rabi splitting;
4. finite-window transfer can differ strongly from asymptotic FGR at long bath memory, and the second-order memory kernel gives a concrete parameter-free correction.

Not yet learned:

- whether the corrected kernel survives the full N/sigma/tau/spatial grid;
- whether deviations scale as sigma^4 or signal genuinely nonperturbative dynamics;
- whether the same factorization survives a quantum phonon bath / HEOM treatment;
- whether this controls the thermodynamic convergence scale N_T in the 2026 MPS-HEOM setting.

## Next gate

`SPATIOTEMPORAL_GRAY_BRIDGE_V2_PREREG.md` freezes the corrected full-grid test using the exact finite-time second-order kernel and the polariton-dark frequency G. The original prereg is not edited retroactively.
