# BATH CORRELATION PROJECTOR — preregistered physics-facing diagnostic

Frozen 2026-08-22 before `bath_correlation_projector.py` exists or any output is read.

## Purpose

The dynamic-gray algebra screen shows that exact simulation compression is governed by the full bath-coupling profile algebra, not covariance rank alone. A different, simpler question remains physically important: **how much of a correlated phonon bath directly drives the bright state into the dark manifold?**

This is already contained in the general site-to-site bath-correlation formalism of del Pino, Feist & García-Vidal (2015), who explicitly treat general `phi_ij(t)` / `S_ij(omega)` before specializing to common and independent baths. The 2026 MPS–HEOM polariton work gives the independent-bath bright→dark rate and its `(N-1)/N` factor. The compact projector formula below is therefore a derived diagnostic, not a priority claim.

## Derivation target

For diagonal site noise

`V(t) = sum_i xi_i(t) |i><i|`

with noise-spectrum matrix `S(omega)` and normalized molecular bright vector `B`, define `D_B = diag(B)` and dark projector

`Q_D = I - |B><B|`.

For any orthonormal dark basis `{d_mu}`, the total spectral weight driving `B` into all dark states is

`W(omega) = sum_mu d_mu^† D_B S(omega) D_B^† d_mu`

and should equal the basis-free expression

`W(omega) = Tr[ Q_D D_B S(omega) D_B^† ]`.

For uniform coupling `B_i=1/sqrt(N)`, this reduces to

`W = Tr(Q_D S)/N`.

This is the only primary identity.

## Frozen controls

For `N in {8,16,32,64,128}` and unit on-site noise (`S_ii=1`):

1. `INDEPENDENT`: `S=I` → predicted `W=(N-1)/N`.
2. `COMMON`: `S=11^T` → predicted `W=0`.
3. `BLOCK-G`: `G in {2,4,8}` equal groups, perfect correlation within group and zero across groups → predicted `W=1-1/G` when G divides N.
4. `RING-EXP`: molecules equally spaced on a ring, `S_ij=exp(-d_ring(i,j)/ell)`, with `ell in {0.1,0.3,1,3,10,30}` in lattice-spacing units. No closed numerical values are staked; `W` must decrease monotonically with ell and remain between 0 and `(N-1)/N`.
5. `RANDOM-PSD`: 100 seeded positive-semidefinite correlation matrices normalized to unit diagonal; explicit dark-basis sum and projector trace must agree to `<1e-10` relative/absolute floor.

RNG seed: `20260822`.

## Stakes

B1: basis-sum and projector-trace agree at `<1e-10` on every control and random PSD draw.

B2: independent/common limits reproduce `(N-1)/N` and `0` at `<1e-12`.

B3: block-correlated baths reproduce `1-1/G` at `<1e-12`.

B4: exponential-correlation `W(ell)` is monotone nonincreasing for each N and bounded by the independent/common limits.

## Physics reading if gates pass

`W(omega)` is the fraction-like spatial factor of bath noise that is **visible to the dark manifold from the bright state** at frequency omega. It cleanly separates:

- temporal/spectral matching, carried by the frequency dependence of `S(omega)` and the polariton-dark gap;
- spatial collectivity, carried by the projector trace.

The 2026 MPS–HEOM result that phonon timescales regulate bright→dark transfer supplies the temporal axis. This diagnostic supplies a complementary spatial-correlation axis.

A natural open question is then whether the thermodynamic convergence scale `N_T` collapses when plotted against a combination such as `W(Omega_R)` and the bath correlation time, across partially correlated baths. This benchmark does not test that claim; it only licenses the scalar diagnostic.

## Simulation relevance

`W` is **not** a compression guarantee. The rank-1 generic counterexample in `DYNAMIC_GRAY_ALGEBRA_RESULTS.md` proves that a bath can have a small first-order/direct drive space but full algebraic closure. `W` is a physical coupling-strength diagnostic, while bath-equivalence/algebra closure is the exact simulation-dimension diagnostic. Keeping those separate is the point.
