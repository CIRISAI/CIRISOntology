# POLARITON SOFT-SYMMETRY VIABILITY SCREEN — RESULTS

Executed 2026-08-22 against frozen `POLARITON_SOFTSYM_BENCH_PREREG.md` on GitHub Actions run `32584906329`, runner `polariton_softsym_bench.py`.

Primary artifact: `9478779724`, ZIP SHA256 `67a663b78f02d2d84f11f2e468edac9a5d3ae9f85e51bea831962187e911a9a0`.
Timing rerun artifact: `9478792821`, ZIP SHA256 `6776c43a3fdb94fda0ec05aa1fd09b935042a071b777c031402d86f214ca3f81`.

## Truth gates

Both implementation gates pass:

- T1 sparse `expm_multiply` vs dense diagonalization, worst max absolute photon-population error: `2.66e-13` (< `1e-10`).
- T2 exact zero-disorder two-state cavity/collective-bright reduction, worst RMSE: `9.58e-13` (< `1e-12`).

No performance interpretation is made without these gates.

## Headline verdict

**Closed/static soft-symmetry clustering is not the simulation-SOTA route. Ordinary Krylov already captures the reachable sector much more strongly.**

For every preregistered nonzero-disorder cell with `N >= 256`, the smallest Lanczos/Krylov dimension meeting photon-population RMSE `<=1e-4` is smaller than the defect-cluster dimension. P4 therefore fires on **100%** of qualifying cells.

The striking part is that the Krylov dimension is essentially independent of N at fixed disorder strength over `N=256,512,1024`:

| sigma/G | Krylov dimension at N=256,512,1024 | P5 ±20% stability |
|---:|---|---|
| 0.1 | 8, 8, 8 | PASS |
| 0.3 | 16, 16, 16 | PASS |
| 1.0 | 32, 32, 32 | PASS |
| 3.0 | 96, 96, 96 | PASS |

This is exactly the anti-hype outcome the prereg allowed: the state reachable from the cavity is already a low-dimensional moment/Krylov object even though the static disorder breaks permutation symmetry across all emitters.

## Defect clustering results

The K2-derived pair certificate is

`g_DB(i,j) = |omega_i-omega_j|/2`.

Greedy frequency clusters constrained by `g_DB <= tau` do produce accurate reduced models, and at weak disorder their required dimension is much smaller than N. For `N=256,512,1024`:

| sigma/G | defect-cluster dimensions |
|---:|---|
| 0.1 | 60, 74, 82 |
| 0.3 | 113, 152, 184 |
| 1.0 | 111, 150, 79 |
| 3.0 | 179, 271, 397 |

Only the `sigma=0.1` sequence satisfies the frozen ±20% N-stability criterion. The stronger-disorder cluster counts generally grow or fluctuate with N, as expected once a fixed pair-defect threshold resolves more of the disorder distribution.

These are useful physically interpretable coarse-grainings, but they are not competitive with the 8/16/32/96 Krylov dimensions.

## Static disorder-binning baseline

The frozen equal-count baseline grid was capped at 128 bins. At `N=256` it does not meet `1e-4` for any nonzero disorder on the tested grid; at `N=512`, only `sigma=0.1` reaches tolerance at `B=128`; at `N=1024` no nonzero-disorder cell reaches tolerance within `B<=128`.

A null `B=None` therefore means **the frozen baseline grid was insufficient**, not that no larger binned model could work. It is not used as a flattering comparison.

At the one qualifying `N>=256` cell where the static binning baseline does pass:

`N=512, sigma=0.1`:

- equal-count binning: 128 effective emitters;
- defect clustering: 74 effective emitters;
- Krylov: 8 states.

The defect clustering does not satisfy the preregistered 2× dimension advantage over binning (`74` is not <= `64`), but its propagation-time advantage was >2× on the first run. Because P3 requires a **reproducible** wall-time improvement, the entire workflow was rerun without changing code or data.

Timing replication for this cell:

| run | binning propagation | defect propagation | bin/defect ratio |
|---|---:|---:|---:|
| primary | 0.01273 s | 0.00451 s | 2.82× |
| rerun | 0.01090 s | 0.00462 s | 2.36× |

Thus the narrow P3 static-binning timing criterion **does replicate**. But it does not rescue the SOTA route, because the same cell's ordinary Krylov representation needs only 8 states and ~`1e-4` s propagation, plus ~`1.5–1.8e-3` s for its one-time basis construction.

## Scientific reading

This benchmark distinguishes two different notions of compression:

1. **interpretable species/coarse-graining compression** — defect clustering can beat a simple static-disorder binning baseline in one weak-disorder regime;
2. **dynamically reachable-subspace compression** — ordinary Krylov is dramatically stronger for this closed, time-independent single-excitation Hamiltonian.

Therefore a soft-symmetry compiler that only preconditions `H` before closed-system propagation is solving a problem that Krylov already solves better.

## Consequence for the SOTA programme

The closed/static route is **CLOSED as a SOTA target** by P4.

The next target moves to the regime current molecular-polariton work itself identifies as computationally harder: **time-dependent / non-Markovian disorder**, where the Hamiltonian and bath operators continually activate non-collective dark/gray directions and there is no single time-independent Krylov subspace to reuse.

This is also where the K2 object has a sharper possible role: not clustering energies, but bounding the rank/dimension of the **dark/gray subspace activated by the disorder operator algebra**.

A useful next invariant is the rank of the centered disorder action on the bright vector. For uniform light-matter couplings and diagonal disorder `D(t)=diag(delta_i(t))`, the instantaneous bright→dark drive is

`q(t) = Q_dark D(t) |B>`.

Across time, the dimension of `span{q(t)}` is the number of independent gray directions directly activated by the disorder process. Low-rank correlated disorder could therefore admit a compact gray sector; independent local baths should generically make this rank extensive. That is now the next falsifiable fork.

## Fence

This screen does not reproduce d-CUT-E, PIQS, or MPS–HEOM. Its equal-count binning is only a deliberately simple static-disorder baseline, and its Krylov benchmark is a closed single-excitation calculation. The negative SOTA verdict applies to **this closed/static route**, not to approximate symmetry reduction in open systems generally.
