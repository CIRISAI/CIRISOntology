# POLARITON SOFT-SYMMETRY BENCHMARK — preregistered viability screen

Frozen 2026-08-22 before `polariton_softsym_bench.py` exists or any benchmark number is read.

This is **not** a claim to reproduce MPS–HEOM, CUT-E/d-CUT-E, or PIQS. It is a cheap external-model viability screen on the standard single-excitation disordered Tavis–Cummings (TC) Hamiltonian. Its job is to kill the soft-symmetry compiler idea early if ordinary Krylov propagation or established disorder binning already captures all available savings.

## Prior-art boundary

- Exact permutation symmetry reduction is established; PIQS exploits it for Lindblad ensembles.
- CUT-E exploits molecular permutation symmetry; d-CUT-E already handles static disorder by replacing a huge ensemble with a much smaller effective disorder representation.
- Current MPS–HEOM (Li et al., arXiv:2603.06868) targets the harder non-Markovian dynamic-disorder regime and reports linear-in-N tensor-network cost. That is the eventual comparison target only if this cheap screen survives.

Therefore **static-disorder compression is not novelty**. It is the calibration problem.

## Model

Single-excitation TC basis: one cavity photon `|c>` plus `N` emitter excitations `|i>`.

`H = wc |c><c| + sum_i wi |i><i| + sum_i gi (|c><i| + |i><c|)`.

Frozen units / construction:

- `wc = w0 = 0`;
- collective coupling `G = sqrt(sum_i gi^2) = 1`;
- uniform `gi = 1/sqrt(N)`;
- static frequency disorder `wi ~ Normal(0,sigma)` from RNG seed `20260822`;
- `N in {64,128,256,512,1024}`;
- `sigma in {0,0.1,0.3,1.0,3.0}`;
- initial state `|c>`;
- times `t = linspace(0,20,201)`.

Primary observable: photon population `P_c(t)`. Error metric: time-normalized RMSE against the full sparse Hamiltonian propagation. Primary tolerance `1e-4`, chosen to match the convergence scale used in the 2026 MPS–HEOM thermodynamic-limit study; this does **not** make the methods otherwise equivalent.

## Truth / implementation gates

T0: Full truth is `scipy.sparse.linalg.expm_multiply` on the `(N+1)` sparse arrowhead Hamiltonian.

T1: At `N=64`, selected cells are cross-checked against dense diagonalization; photon-population max error must be `<1e-10`.

T2: At `sigma=0`, the exact two-state cavity/collective-bright reduction must reproduce truth at `<1e-12` RMSE for every N.

Any T0–T2 failure voids performance interpretation.

## Baseline A — ordinary Lanczos/Krylov

Starting from `|c>`, construct the standard Hermitian Lanczos basis with dimensions

`m in {2,4,6,8,12,16,24,32,48,64,96,128}`.

Propagate in the tridiagonal Krylov matrix. Record the smallest `m` reaching RMSE `<=1e-4`, plus construction and propagation wall time.

This baseline is deliberately strong: if ordinary reachability already compresses the problem, the soft-symmetry compiler does not get credit for rediscovering Krylov.

## Baseline B — disorder/species binning

A d-CUT-E-shaped static-disorder baseline (not an implementation of the paper): sort emitters by `wi`, partition into `B` contiguous equal-count bins, replace each bin by one effective emitter at its coupling-weighted mean frequency with coupling `G_b=sqrt(sum_{i in b} gi^2)`.

`B in {1,2,4,8,16,32,64,128}` capped at N. Record the smallest B reaching the tolerance.

This measures the compression available from ordinary disorder discretization.

## Candidate C — defect-controlled near-twin clustering

For two uniformly coupled emitters with frequencies `wi,wj`, their swap-conjugation defect gives

`g_DB(pair) = |wi-wj|/2`.

Use that quantity directly as a clustering certificate. After sorting by frequency, greedily form the largest contiguous clusters whose frequency diameter obeys

`max(w)-min(w) <= 2 tau`,

so every pair inside a cluster has `g_DB <= tau`. Replace each cluster by one effective emitter with the same coupling-weighted mean frequency and aggregate coupling as in baseline B.

Sweep `tau/G in {0,0.001,0.003,0.01,0.03,0.1,0.3,1,3}`. Report cluster count, maximum certified within-cluster `g_DB`, RMSE, and wall time. The primary score is the **smallest cluster count that reaches 1e-4**, selected only from the frozen tau grid.

This is the first test of whether the K2 defect has computational predictive value outside K11. It is not claimed as a new disorder discretization algorithm.

## Stakes / anti-hype outcomes

P1: exact-symmetry control (T2) must pass.

P2: For each `(N,sigma)`, report the minimum reduced dimension needed by A, B, and C. No averaging may hide a bad regime.

P3: Candidate C earns a continuation only if, on at least one nonzero-disorder regime with N>=256, it reaches the tolerance with **at least 2x fewer effective emitter/species states than baseline B** OR gives a reproducible >=2x wall-time improvement at matched error. Otherwise static near-twin clustering is classified as `BASELINE-EQUIVALENT` and is not a SOTA route.

P4: If ordinary Krylov needs a dimension no larger than candidate C's reduced dimension on the same cells, record `KRYLOV-ALREADY-CAPTURES-REACHABILITY`; any future compiler must then target open-system/tensor-network structure rather than closed-system propagation.

P5: Scaling with N is descriptive. A claim of N-independent compression is allowed only if the reduced dimension stays within ±20% over N=256..1024 at fixed sigma and tolerance.

## What survives a likely negative

A failure of C to beat B or A is useful: it localizes the opportunity to the genuinely hard sector already identified by the literature—non-Markovian dynamic disorder / HEOM tensor structure—not static TC propagation. In that case the next benchmark should be symmetry adaptation of the **system+bath operator algebra**, not another closed Hamiltonian reduction.

No Stance change, no SOTA claim, no physics-world claim follows from this benchmark.
