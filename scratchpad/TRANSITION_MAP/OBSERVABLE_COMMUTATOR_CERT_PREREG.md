# OBSERVABLE-WEIGHTED COMMUTATOR CERTIFICATE — PREREG

Frozen 2026-08-22 after the approximate-class Duhamel certificate proved valid but highly pessimistic, and before any observable-weighted certificate code/output exists.

## Prior-art fence

Goal-oriented/model-reduction error estimation is established, including observable-dependent quantum model reduction and a posteriori error estimates for Lindblad/Hamiltonian dynamics. No novelty is claimed for the general idea of observable-aware error bounds.

The narrow question here is whether the special structure of the current reduction — a diagonal emitter-energy defect and the cavity projector as target observable — yields a cheap closed-form certificate tight enough to drive the profile-class compiler without access to full truth.

## Exact bound target

Let H(t)=Hbar(t)+E(t), where Hbar is the centroid/profile-class Hamiltonian embedded in the full emitter space and E(t) is the diagonal residual energy defect. Let the final observable be the cavity projector O=|c><c|.

Define the backward Heisenberg observable under the reduced/centroid Hamiltonian,

`Obar(t) = Ubar(T,t)^dagger O Ubar(T,t)`.

The difference between full and reduced Heisenberg observables obeys a Duhamel equation giving the operator-norm bound

`||O_H(0)-Obar(0)|| <= integral_0^T || [E(t), Obar(t)] || dt`.

Therefore for any common normalized initial state,

`|<O>_H(T)-<O>_bar(T)| <= C_O(T)`

with

`C_O(T)=integral ||[E(t),Obar(t)]|| dt`.

For rank-one `Obar(t)=|phi(t)><phi(t)|` and Hermitian diagonal E(t), the commutator norm should equal the standard deviation of E in phi,

`||[E,|phi><phi|]|| = sqrt(<phi|E^2|phi>-<phi|E|phi>^2)`.

This closed-form identity is an implementation gate, not a novelty claim.

## Frozen substrate

Use exactly the SMOOTH-RING/SCRAMBLED-RING model from `APPROX_BATH_CLASSES_PREREG.md`, N in {128,256,512,1024}, G in {8,16,32,64,128}, T=20, same midpoint discretization and cavity-population observable.

Compute three bounds for every cell:

1. old state Duhamel population certificate `C_state=min(1,2B_T+B_T^2)`;
2. observable commutator certificate `C_O` using backward evolution under Hbar only;
3. observed max cavity-population error against full truth, solely for evaluation after the certificates are computed.

No fitted prefactor or calibration to observed error is allowed.

## Gates

O1. Direct SVD/operator-norm evaluation of `[E,|phi><phi|]` agrees with the variance formula to <1e-10 on seeded random checks.

O2. Observed cavity-population error never exceeds `C_O` by more than 1e-8 numerical slack.

O3. SMOOTH-RING/SCRAMBLED-RING certificates agree to <1e-10 after relabeling.

Failure voids interpretation.

## Scientific/computational stakes

P1 — useful tightening: at G=64, N=1024, `C_O <= 0.05`; the old state certificate is ~1, so this requires at least an order-of-magnitude practical tightening.

P2 — selector quality: the minimum G with `C_O<=1e-3` is at most 2x the observed minimum G meeting 1e-3. If the bound needs near-singleton classes, it is safe but not operationally useful.

P3 — N stability: at fixed G, `C_O` changes by at most factor 2 from N=256 to 1024, matching the observed error collapse qualitatively.

P4 — failure interpretation: if O2 passes but P1/P2 fail, retain the bound as mathematically correct and cut it as a compiler-selection mechanism; pursue residual/dual-weighted or adaptive a posteriori estimators only if a real open-system benchmark still warrants them.

## Open-system extension

If P1/P2 pass, the next derivation target is a dual/Heisenberg observable bound for Lindblad generators where the defect includes both Hamiltonian and jump-operator terms. That extension must be compared directly with established 2026 Lindblad a posteriori error-estimation methods rather than claimed as a general new framework.
