# BATH CORRELATION ASYMPTOTICS — exact ring consequence

Derived 2026-08-22 from the passed bath-projector identity. This is an elementary model consequence, not a priority claim.

## Setup

Uniform bright state on an N-site ring,

`|B> = (1,...,1)/sqrt(N)`,

with unit-variance exponentially correlated diagonal noise

`S_ij = exp[-d_ring(i,j)/ell]`.

The passed projector diagnostic gives

`W_N(ell) = Tr(Q_D S)/N = 1 - <B|S|B>/N`.

Because S is circulant, `|B>` is its uniform eigenvector and `<B|S|B>` is exactly the row sum `R_N`.

Thus

`W_N = 1 - R_N/N`.

For even N, with `q=exp(-1/ell)`,

`R_N = 1 + 2 sum_{d=1}^{N/2-1} q^d + q^(N/2)`.

For odd N,

`R_N = 1 + 2 sum_{d=1}^{(N-1)/2} q^d`.

No diagonalization is required.

## Thermodynamic regimes

### 1. Fixed correlation length

For fixed finite ell, q<1 and the row sum stays O(ell) as N grows. Therefore

`R_N/N -> 0`

and

`W_N -> 1`.

So a bath can be strongly correlated over many neighboring molecules yet become effectively independent-bath-like for **total bright-to-dark activation** when the aggregate is made parametrically larger than the correlation length.

### 2. Correlation length proportional to system size

Let

`ell = alpha N`

with fixed `alpha>0`. Writing `x=d/N`, the row sum becomes a Riemann sum:

`R_N/N -> 2 integral_0^(1/2) exp(-x/alpha) dx`

so

`R_N/N -> 2 alpha [1-exp(-1/(2 alpha))]`.

Hence

`W_infty(alpha) = 1 - 2 alpha [1-exp(-1/(2 alpha))]`.

This is strictly between 0 and 1 for every finite positive alpha.

Examples:

| ell/N = alpha | W_infty |
|---:|---:|
| 1/16 | 0.87504 |
| 1/4 | 0.56767 |
| 1 | 0.21306 |
| 4 | 0.05998 |
| 10 | 0.02459 |

Thus merely scaling the phonon correlation length linearly with aggregate size does **not** generically recover the perfectly common-bath limit; it leaves a finite dark-activation fraction set by alpha.

### 3. Correlation length much larger than system size

For `alpha=ell/N >> 1`, expand the exponential:

`W_infty(alpha) = 1/(4 alpha) + O(alpha^-2)`

or equivalently

`W ~ N/(4 ell)`.

Therefore `W -> 0` requires `ell/N -> infinity` in this exponential-ring family: the bath correlation length must be parametrically larger than the aggregate.

## Reconciliation with the gray-rank screen

The concurrent gray-rank screen evaluates the second-order gray covariance `Q S Q`, while W measures the **total bright-to-dark coupling weight**. They answer different questions.

Two frozen long-range cases make the distinction quantitative:

- `ell=N/4`: gray participation/effective rank approaches about `5.5`, yet `W_infty≈0.568`;
- `ell=N/16`: effective rank approaches about `16.3`, yet `W_infty≈0.875`.

So a bath can have a very compressible direct-drive covariance spectrum while still coupling the bright state strongly to the dark manifold. Low effective rank is potentially good news for simulation cost; it is not physical dark-state protection.

Conversely, a small W does not prove a small exact simulation sector: `DYNAMIC_GRAY_ALGEBRA_RESULTS.md` gives a generic rank-1 profile with full algebraic closure N.

## Combined diagnostic

For correlated-bath polariton simulations, keep at least three axes separate:

1. `W(omega)` — physically weighted bright-to-dark activation at the relevant transition frequency;
2. spectral/effective rank of `Q S(omega) Q` — number of important direct gray-noise directions;
3. finite-time operator/tensor growth — whether repeated bath action actually makes the solver state expensive.

A credible compression regime is where the latter two are small enough at the required observable error. A physically protected regime additionally requires W to be small.

## Chemistry-facing question

The 2026 MPS-HEOM result identifies phonon **timescale** as a control on bright-to-dark transfer and thermodynamic convergence. The projector/asymptotic result identifies an independent **spatial collectivity** control.

The concrete next question is whether realistic molecular vibrational environments have a correlation length/profile whose scaling with aggregate size keeps `W(Omega_R)` bounded away from the independent-bath limit, and whether the same environments have sufficiently low effective gray rank to reduce non-Markovian simulation cost.

Those are two separate measurements; neither should be inferred from the other.
