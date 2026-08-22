# SPATIOTEMPORAL GRAY BRIDGE — PREREG

Frozen 2026-08-22 after the bath-correlation projector and approximate bath-class results, before any bridge simulation code exists or any bridge outputs are inspected.

## Question

Does the same dark/gray structure that is exact in the K11 twin theorem and perturbatively quantitative in K2.3 remain predictive in a stochastic molecular-polariton surrogate where both spatial bath correlation and temporal bath spectrum matter?

The bridge is falsified if a physically motivated predictor built from the spatial dark-activation weight and the temporal noise spectrum does not organize bright->dark transfer even in this controlled setting.

## Model

Single-excitation Tavis-Cummings system with one cavity mode and N identical emitters at zero static disorder. Uniform light-matter coupling gives collective Rabi scale Omega_R = 2G. Use N in {32,64,128,256} with fixed collective coupling G=1.

Each emitter experiences zero-mean classical Gaussian Ornstein-Uhlenbeck energy noise `xi_i(t)` with covariance

`E[xi_i(t) xi_j(0)] = sigma^2 S_ij exp(-|t|/tau_c)`.

Spatial correlation matrices:

1. INDEPENDENT: `S=I`.
2. COMMON: `S=11^T`.
3. BLOCK-G with G in {2,4,8} equal perfectly correlated groups.
4. RING-EXP: `S_ij=exp(-d_ring(i,j)/ell)` with `ell in {0.3,1,3,10}`.

Noise strengths `sigma in {0.02,0.05,0.1}` and correlation times `tau_c in {0.02,0.05,0.1,0.2,0.5,1,2,5}`. Time horizon T=20. Use the same frozen random seeds across spatial-correlation arms for paired comparisons; at least 64 trajectories per cell.

## Predictor

For OU noise, use the two-sided spectral density

`J_OU(omega) = 2 sigma^2 tau_c / (1 + omega^2 tau_c^2)`.

For uniform bright amplitudes define the spatial factor

`W = Tr(Q_D S)/N`.

The frozen bridge predictor is

`R_pred = W * J_OU(Omega_R)`.

No fitted exponent, prefactor, shifted frequency, or nonlinear transform is allowed in the primary test.

## Observables

Initialize the upper/lower polariton combination that maximizes initial cavity/bright participation without dark population. For each cell report:

- ensemble-mean total dark-manifold population versus time;
- early-time dark-transfer slope over a frozen short-time window chosen in code before random draws are generated;
- peak dark population by T;
- cavity population decay envelope;
- pairwise ordering across spatial-correlation arms at fixed sigma,tau_c,N;
- finite-size variation from N=64 to 256.

The primary response is the early-time dark-transfer slope `R_obs`.

## Implementation gates

B1. COMMON bath gives dark population at numerical/stochastic floor relative to INDEPENDENT under identical scalar noise realization, because common diagonal noise is proportional to identity in emitter space and cannot directly activate dark states.

B2. At weak noise, doubling sigma from 0.02 to 0.05/0.1 produces transfer slopes consistent with sigma^2 scaling to within Monte Carlo uncertainty before saturation.

B3. For each S, the independently measured covariance from generated trajectories reproduces the target zero-lag S matrix to declared Monte Carlo tolerance.

Failure of B1-B3 voids bridge interpretation.

## Scientific stakes

P1 — spatial ordering: at fixed N,sigma,tau_c, `R_obs` is nondecreasing with W across common/block/ring/independent arms, allowing statistical ties.

P2 — temporal turnover: at fixed spatial arm and weak sigma, `R_obs(tau_c)` peaks within a factor 2 in tau_c of the maximum of `J_OU(Omega_R)`, which occurs near `tau_c=1/Omega_R`.

P3 — parameter-free organization: over weak-noise cells with nonzero W, Spearman rank correlation between `R_obs` and `R_pred` is >=0.9 and a zero-intercept linear fit has no systematic residual sign versus W or tau_c. The slope is descriptive, not a fitted rescue of the predictor.

P4 — finite-size bridge: after W is included, the relative change in `R_obs/R_pred` from N=64 to N=256 is <=25% for the same spatial scaling prescription. If not, finite-size collective structure not captured by W is material.

## Falsification meanings

- P1 fail: the projector weight is not even the correct spatial ordering variable in this surrogate.
- P1 pass, P2 fail: spatial bridge survives but temporal spectral matching is incomplete/nonperturbative.
- P1/P2 pass, P3 fail: W and J are qualitatively relevant but do not factorize; cross terms, memory, or polariton dressing matter.
- P1-P3 pass, P4 fail: finite-size thermodynamic convergence needs an additional collective variable.
- P1-P4 pass: the bridge earns a genuine non-Markovian quantum benchmark, not a claim of new molecular physics yet.

## Compression side-channel

For each trajectory also compute the numerical rank needed to represent the instantaneous centered noise vector in the dark manifold and the empirical trajectory/POD rank needed to reconstruct dark population within 1e-3. These are exploratory only and cannot establish SOTA. Their purpose is to see whether physics predictability and compressibility track the same spatial-temporal regimes or separate.

## Fence

This is a classical colored-noise single-excitation surrogate. It is not HEOM, HOPS, MPS-HEOM, a quantum phonon bath, or a thermodynamic-limit calculation. It tests whether a proposed bridge variable survives a deliberately controlled intermediate model before expensive quantum-bath work.
