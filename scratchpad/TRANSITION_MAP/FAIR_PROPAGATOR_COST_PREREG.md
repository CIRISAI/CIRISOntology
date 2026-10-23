# FAIR PROPAGATOR COST — PROFILE CLASSES VS FULL KRYLOV — PREREG

Frozen 2026-08-22 after the deployable reachability run revealed local Krylov dimension 4 versus profile-class dimension 64, but before any common-kernel cost comparison is executed.

## Why this correction is necessary

Basis dimension alone is not a fair computational comparison. A full-space Krylov matvec acts on N+1 states and costs O(N) for the frozen arrowhead Hamiltonian; a profile-class matvec acts on G+1 states and costs O(G). Therefore `m=4` in the full space can still be more expensive than a larger reduced model when `G << N`.

The previous finite-time reachability result is retained as a **dimension result**, not a final cost verdict. This test decides cost using the same propagation kernel on both arms.

## Frozen substrate

Exactly the SMOOTH-RING and SCRAMBLED-RING time-dependent model from `APPROX_BATH_CLASSES_PREREG.md` / `FINITE_TIME_REACHABILITY_PREREG.md`:

- N in {256,512,1024};
- T=20, 200 midpoint piecewise-constant steps;
- same two temporal coordinates;
- same cavity-population truth trajectory;
- target max cavity-population error <=1e-3.

## Common propagation kernel

Use the same in-house restarted Arnoldi step on every candidate arm, with local Krylov dimension

`m in {2,3,4,6,8,12}`.

Arms:

A. FULL: original N+1 arrowhead Hamiltonian.

B. CLASS-G: complete-profile centroid models with `G in {16,32,64,128}`.

No `scipy.expm_multiply` timing is used in the primary performance comparison because its internal adaptive matvec count differs between dimensions. It remains the truth generator only.

## Primary cost proxy

For each time step and Arnoldi dimension m, record:

- actual sparse Hamiltonian matvec count;
- Hamiltonian nonzeros `nnz`;
- modified-Gram-Schmidt inner-product/axpy count.

Frozen arithmetic proxy:

`C_proxy = sum_steps [ m * nnz(H) + 2 * dim * m*(m+1)/2 ]`.

The first term proxies sparse matvec work; the second proxies complex vector orthogonalization work. The same formula is applied to every arm. This is the primary hardware-independent metric.

## Wall-time protocol

Wall time is secondary. On the same GitHub runner and same Python process:

- one untimed warm-up per arm/configuration;
- three timed repeats;
- report median propagation time;
- include class construction time separately and in an amortized one-trajectory total;
- do not compare timings from different workflow runs as primary evidence.

## Gates

FPC1. Common Arnoldi FULL arm reproduces the prior minimum local dimension (`m<=4`) at <=1e-3 for all N, or any discrepancy is explained by identical code-path differences before interpretation.

FPC2. CLASS-G with sufficiently large G,m converges to the already measured class-model errors within 1e-5 absolute population error.

FPC3. SMOOTH/SCRAMBLED arithmetic proxy and observable errors agree to <1e-10; timing may differ only within descriptive noise.

## Scientific/computational stakes

P1 — real cost opening: at N=1024, the minimum-cost CLASS configuration meeting 1e-3 has `C_proxy <= 0.5 * C_proxy_FULL` for the minimum-cost FULL configuration meeting 1e-3.

P2 — scaling: the CLASS/FULL cost-proxy ratio decreases from N=256 to N=1024 while the selected G changes by at most factor 2. This would indicate a genuine size-scaling advantage on the frozen model.

P3 — one-trajectory wall time: including class construction, median CLASS total time is <=0.8 times FULL propagation time at N=1024. Wall time is supportive only; failure does not overturn P1 if Python overhead dominates.

P4 — repeated-trajectory reuse: report the break-even number of trajectories/parameter points after which one-time class construction is amortized. If construction is negligible this is ~1; if large, this determines whether ensemble/open-system use is plausible.

## Interpretation

- P1/P2 fail: the solver-performance profile-class route is closed on this model despite its N-stable approximation dimension.
- P1/P2 pass but P3 fails: structural arithmetic advantage exists but implementation/runtime is not yet competitive.
- P1/P2/P3 pass: buys a harder stochastic/non-Markovian benchmark, but is still not a SOTA claim until compared with production methods at fixed physical error.

## Fence

This corrects a fairness issue; it is not a new algorithm claim. Restarted Arnoldi/Krylov and reduced-order modeling are standard. Any useful residue is the interaction between complete-profile near-equivalence and solver cost under dynamic bath disorder.
