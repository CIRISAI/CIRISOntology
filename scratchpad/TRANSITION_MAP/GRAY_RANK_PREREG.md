# GRAY-RANK SCREEN — PREREG

Frozen 2026-08-22 before execution. Follow-on to the negative closed/static polariton benchmark.

## Motivation

The closed single-excitation Tavis-Cummings benchmark showed that ordinary Krylov/Lanczos already compresses the dynamically reachable Hamiltonian sector more strongly than explicit near-twin clustering. The remaining credible simulation opportunity is therefore not static H compression. It is reduction of the *operator algebra that continually injects amplitude into dark/gray directions* in open or dynamically disordered models.

For uniform light-matter coupling define the normalized collective bright vector

`B = (1,...,1)/sqrt(N)`

and `Q = I - |B><B|`. For diagonal dynamic disorder `D(t)=diag(delta(t))`, the instantaneous bright-to-dark drive is

`q(t) = Q D(t) B = Q delta(t)/sqrt(N)`.

If the disorder vector has covariance `C = E[delta delta^T]`, then

`Cov(q) = Q C Q / N`.

Thus the rank/effective rank of `Q C Q` is the number of statistically independent gray directions directly activated by the bath at second order. This is a diagnostic of whether a gray-sector compression is even plausible before implementing MPS-HEOM or another non-Markovian solver.

## Frozen system sizes and bath covariance families

`N = 64, 128, 256, 512, 1024`.

Covariance families:

1. **independent**: `C=I`;
2. **common mode**: `C=11^T` (global frequency jitter);
3. **low-rank correlated**: `C=F F^T` with deterministic Fourier feature ranks `r=4,16` including the common mode;
4. **periodic exponential correlations**: `C_ij = exp(-d_periodic(i,j)/ell)` with `ell = 2, 8, N/16, N/4`.

No random seed is needed for these deterministic covariance matrices.

## Metrics

For `A = Q C Q` report:

- algebraic numerical rank with relative eigenvalue tolerance `1e-10 * lambda_max`;
- `r90`, `r99`, `r999`: minimum number of descending eigenvalues accounting for 90%, 99%, 99.9% of `trace(A)`;
- participation/effective rank `r_eff = (sum lambda)^2 / sum lambda^2`;
- fractions `r99/(N-1)` and `r_eff/(N-1)`.

For a purely illustrative HEOM combinatorial proxy, report

`aux(K,L)=binom(K+L,L)` for hierarchy depths `L=2,3,4`

using `K=r99` versus `K=N-1`. This is **not** a runtime prediction: actual HEOM cost also depends on bath decomposition, truncation, tensor structure, and implementation.

## Exact implementation gates

G1. independent bath: rank `N-1` and all nonzero eigenvalues equal to 1 within `1e-10` relative error.

G2. common-mode bath: `||Q C Q||_F < 1e-10` and rank 0.

G3. low-rank feature bath: projected rank <= `r-1` because the common Fourier feature lies in the bright direction.

Failure of G1-G3 voids interpretation.

## Scientific stakes

S1. **Independent local baths kill the rank-compression route** if `r99/(N-1) >= 0.95` for all N. This is expected and is an anti-hype control.

S2. **Fixed finite correlation length remains extensive** if, for `ell=2` and `ell=8`, `r99` grows proportionally with N and `r99/(N-1)` does not trend toward zero across the frozen sizes.

S3. **Long-range correlated disorder buys a gray-sector opportunity** if either `ell=N/16` or `ell=N/4` has `r99 <= 64` at N=1024 and its `r99` growth from N=256 to 1024 is <=2x while N grows 4x.

S4. The low-rank feature construction is a positive-control existence proof only. It cannot establish chemical realism.

## Interpretation fence

Even if S3 passes, do not claim simulation SOTA. The next gate would be an actual non-Markovian/open-system solver benchmark showing reduced MPS bond dimension, HEOM auxiliary/tensor cost, memory, or wall time at fixed physical-observable error. If S2 holds and S3 fails, the soft-symmetry route is narrowed to specially correlated environments rather than generic molecular baths.
