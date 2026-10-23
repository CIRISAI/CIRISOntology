# BATH CORRELATION PROJECTOR — RESULTS

Executed 2026-08-22 against frozen `BATH_CORRELATION_PROJECTOR_PREREG.md` on GitHub Actions run `32585311005`, runner `bath_correlation_projector.py`.

Artifact: `9478883817`, ZIP SHA256 `ed749d1abf76e57656ac2c16d954fbd723f167013b22370352d2d47350cf646d`.

## Verdict

**B1–B4 all PASS.** The compact projector expression

`W = Tr[ Q_D D_B S D_B^† ]`

is numerically identical to the explicit sum over a dark-state basis on every frozen control and 500 random PSD correlation matrices (100 per N). For uniform bright amplitudes this reduces to

`W = Tr(Q_D S)/N`.

Worst explicit-basis vs projector discrepancy: `8.88e-16`.

This is a physics-facing coupling diagnostic, not a simulation-dimension diagnostic.

## Exact limits

For unit on-site noise:

- independent bath `S=I`: `W=(N-1)/N`, worst error `2.22e-16`;
- perfectly common bath `S=11^T`: `W=0`, numerical residual at most ~`1.25e-16`;
- G perfectly correlated equal blocks: `W=1-1/G`, worst error `2.22e-16`.

The block result is independent of N when G divides N:

| G | W |
|---:|---:|
| 2 | 0.5 |
| 4 | 0.75 |
| 8 | 0.875 |

This interpolates algebraically between the common-bath and independently addressable limits already familiar in molecular-polariton bath theory.

## Exponentially correlated ring bath

`S_ij = exp[-d_ring(i,j)/ell]` is PSD on every frozen grid and `W(ell)` decreases monotonically with correlation length, as staked.

| N | ell=.1 | .3 | 1 | 3 | 10 | 30 |
|---:|---:|---:|---:|---:|---:|---:|
| 8 | 0.87499 | 0.86575 | 0.73446 | 0.44259 | 0.17511 | 0.06371 |
| 16 | 0.93749 | 0.93288 | 0.86480 | 0.64783 | 0.31109 | 0.12215 |
| 32 | 0.96875 | 0.96644 | 0.93238 | 0.81168 | 0.50077 | 0.22489 |
| 64 | 0.98437 | 0.98322 | 0.96619 | 0.90539 | 0.69999 | 0.38509 |
| 128 | 0.99219 | 0.99161 | 0.98309 | 0.95269 | 0.84388 | 0.58673 |

## Thermodynamic consequence

A fixed correlation length is not enough to keep a large ensemble in the common-bath/protected regime. At fixed ell, the fraction of emitter pairs separated by distances much larger than ell grows with N; correspondingly `W` approaches the independent-bath side as the ring is enlarged.

The effect is visible even at ell=30: `W` grows from `0.0637` at N=8 to `0.5867` at N=128. At ell=3 the same progression is `0.443 -> 0.953`.

So bright-state protection in the thermodynamic limit requires the spatial bath-correlation scale to grow with system size, or some other collective structure that keeps `Tr(Q_D S)/N` small. A bath can be locally quite correlated while still becoming dark-activating on a much larger aggregate.

This supplies a clean spatial complement to the temporal mechanism identified by current MPS–HEOM work, where the phonon correlation time / spectral overlap regulates bright→dark transfer and the system size needed for thermodynamic convergence.

## Relation to the gray-rank and algebra screens

Three quantities must remain distinct:

1. **`W` — direct bright→dark coupling weight.** A physical rate prefactor (after the frequency-dependent bath spectrum is included).
2. **gray covariance/effective rank.** How many statistically important dark-driving noise directions exist at first order.
3. **full operator-algebra closure.** The exact system-space dimension reachable under arbitrary repeated dynamic disorder.

The concurrent gray-rank screen shows that long-range exponential correlations can have a small participation/effective rank even while strict 99%-energy rank is sizable. `DYNAMIC_GRAY_ALGEBRA_RESULTS.md` shows something stronger: even a single generic bath profile can have exact algebra closure N. Thus neither a small `W` nor a small covariance rank is, by itself, a simulation-compression theorem.

The computational opportunity is where all relevant approximations align: small physically weighted dark activation, rapidly decaying gray spectrum, and finite-time dynamics that do not explore the full algebra before the observable converges.

## Physics opportunity

The next experimentally/model-relevant question is now two-dimensional rather than one-dimensional:

- **temporal axis:** bath correlation time / spectral density at the polariton-dark splitting;
- **spatial axis:** `W(omega)=Tr[Q_D D_B S(omega)D_B^†]`, or its uniform-coupling reduction.

A concrete test is whether the thermodynamic convergence scale `N_T` for polariton observables collapses across partially correlated baths when plotted against a combination of the temporal spectral factor and this spatial dark-activation weight. The common and independent endpoints are known; the partially correlated interpolation is the useful target.

## Fence

The projector identity is a compact consequence of the general correlated-bath formalism, not a priority claim. It does not replace HEOM/HOPS/MPS/TTN simulation and does not predict compression cost. Its value is to name the physically relevant part of a spatial correlation matrix before asking a simulator to reproduce its consequences.
