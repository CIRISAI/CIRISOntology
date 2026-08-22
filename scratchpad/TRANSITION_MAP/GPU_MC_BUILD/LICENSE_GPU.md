# GPU annihilating coherent MC — build report and license status

**Status: `BLOCKED-MISSING-BENCHMARK-DATA`. No license is issued.**

Parent prereg: `REG_HYDRO_COHERENT_ANNIHILATING_MC_PREREG.md` (commit `5f65a5b`)
CPU license: `REG_HYDRO_COHERENT_ANNIHILATING_MC_LICENSE.md` (commit `9312caa`, W=10,000)
Charter: `GPU_MC_NOTE.md` (commit `1b7b194`), `ANNIHILATING_MC_EXECUTION_NOTE.md` (`b447c16`)

Hardware: NVIDIA RTX 4090 Laptop, 15.57 GiB VRAM, CuPy 13.6.0, CUDA 13.0.

This build was written from the frozen prereg text alone. No estimator code from the primary
workstream was used; none exists in the repository and none was sought elsewhere. The only
code consulted is `regplus_hydro/regplus_hydro.py`, named in the charter as the frozen source
of the microscopic constants (sectors and unitaries).

## Why no license was issued

The frozen benchmark cascade in the prereg is gated on **per-configuration** quantities:

> "Benchmark against the exact paired L=7 LOW N=20 and MID N=25 configuration lists and exact
> M values already frozen." … "For each W report across all 32 exact benchmark configurations:
> median, p90, maximum |M_MC − M_exact| …"

Those artifacts are **not in the repository**, and never have been. Searched: every top-level
directory of the working tree, all untracked files, and every path that has ever appeared in
git history (`git log --all --diff-filter=ADMR --name-only`). The REG_HYDRO experiments are
recorded as prereg + result markdown only; no numeric artifact and no runner code was ever
committed.

Missing, precisely:

1. **The L=7 LOW N=20 configuration list** — 16 configurations, each an 18-mode spectator set.
2. **The L=7 MID N=25 configuration list** — 16 configurations, each a 23-mode spectator set.
3. **The 32 per-configuration exact M values.** Only two cell-level aggregates exist, in
   `REG_HYDRO_MEMORY_FINITE_SIZE_RESULT.md`: LOW median M = 0.085881 with 31.25 % below 0.05,
   MID median M = 0.038276 with 62.5 % below 0.05. Six of the eight frozen gates are
   per-configuration error and SE statistics, so cell aggregates cannot substitute.

The lists were **not regenerated**, per the execution instruction. They also could not be
regenerated reliably even if that were permitted: the prereg fixes the seeds (2026082271 LOW,
2026082272 MID) and the rule ("every directional mode on non-origin sites … N−2 distinct modes
without replacement using NumPy PCG64"), but not the candidate-array ordering, nor whether one
Generator is drawn from 16 times in sequence or re-seeded per configuration, nor whether the
draw is `Generator.choice(replace=False)` or a `permutation` prefix. Each choice yields a
different list, and the resulting error would be silent.

## An unpinned convention the benchmark data would settle

The frozen text does not state whether the three orientation probabilities are **normalised by
the origin head-on-pair support** before the TV witness is formed. The N=2 bridge cannot
discriminate — its support is exactly 1. On many-body cells it matters a great deal.

On 64 freshly drawn L=7 N=20 configurations, exactly computed here:

| witness convention | median M | fraction M < 0.05 | resulting cell class |
|---|---:|---:|---|
| normalised, `p_j = q_j / support` | 0.159999 | 0.1875 | not low-memory |
| raw, `q_j` used directly | 0.049654 | 0.5000 | low-memory |
| **recorded frozen LOW cell (16 configs)** | **0.085881** | **0.3125** | **not low-memory** |

A 20,000-sample bootstrap of the median of 16 draws contains 0.085881 under **both**
conventions ([0.0738, 0.2119] normalised; [0.0236, 0.1264] raw), so this comparison does
**not** resolve the convention. The recorded *classification* weakly favours the normalised
reading — the raw convention would classify this sample as low-memory, contradicting the
recorded "not LOW-MEMORY" for LOW. **This build implements the normalised convention.** If the
primary workstream used the raw convention, every number below shifts and the block must be
cleared before, not after, that is discovered.

## What WAS verified (gates that could be run)

### G1 — Microscopic model reconstruction, against in-repo exact data — **PASS**

The independent reconstruction reproduces the published exact N=2 carries-memory bridge
(`REG_HYDRO_COHERENT_MEMORY_RESULT.md`, L=11, θ=1.30) at **all 12 frozen phases, to every
published digit**:

| Φ° | 0 | 30 | 60 | 90 | 120 | 150 | 180 | 210 | 240 | 270 | 300 | 330 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| recorded | .231078 | .333345 | .180601 | .031972 | .180601 | .333345 | .231078 | .333345 | .180601 | .031972 | .180601 | .333345 |
| this build | .231078 | .333345 | .180601 | .031972 | .180601 | .333345 | .231078 | .333345 | .180601 | .031972 | .180601 | .333345 |

Norm and probability sums are unity to ~1e-15 throughout. This pins the sector construction,
the sign of the Wilson-loop phase, the carries permutation, the protocol timing (one collision,
then L × (stream, collide), read after the final collision), the dephasing definition and the
witness. Sector table: 53 sectors of dimensions 1/2/3 in counts 44/7/2, the two triples being
(9,18,36) and (27,45,54) — identical to the frozen reference.

### G2 — Micro-case tests — **12/12 PASS** (`test_micro.py`)

Unitarity `U†U = I` max deviation **1.110e-15 = 5.0 ulp**. The charter names 1e-15, which is
4.5 ulp and sits *below* the fp64 floor for a 3×3 Hermitian eigendecomposition; the gate is set
at 8 ulp = 1.78e-15 and the measured value is reported rather than the threshold quietly moved.
Also passing: collision column probabilities sum to 1 (9.99e-16); the stream permutation has
order exactly L for L=3,5,7,9,11; the MC site-state stream equals the exact mode permutation;
the bit-packed key is a bijection; two-walker annihilation `(1+2i)+(3−5i) = 4−3i`, `S = 5`;
resampled weight exactly `(S/W)·s_c/|s_c|`; opposite phases annihilate to `S = 0` exactly;
segmented sums over two configurations; resampling conditionally unbiased
(`E[A'(c)] = s_c/W`, 0.07 % over 20,000 resamplings); collision weight unbiased
(`E[w·1{out=k}] = u_k`); branch weights `|a_j|²` sum to 1 and match the exact projection.

### G3 — Exact-model verification — **PASS**

Two *independent* exact implementations (mine, and an API-worker draft written from the spec
and repaired by me) agree to **2.2e-16** on 25 many-body configurations across L=3, 5, 7, and
both reproduce the L=11 bridge. The worker's route projects the post-first-collision state onto
each origin orientation; mine forces the origin collision output. Their agreement confirms the
two preparations are equivalent.

MC → exact convergence at the benchmark cell's own parameters (L=7, N=20), own configurations:

| config | exact M | W=10,000 error | W=1,000,000 error | W=1e6 SE |
|---|---:|---:|---:|---:|
| a | 0.294344 | −0.008333 | **−0.000162** | 0.000450 |
| b | 0.152363 | +0.019662 | **−0.001564** | 0.001114 |
| c | 0.178612 | +0.025613 | **−0.002286** | 0.001046 |

Across a wider CPU sweep (L=3/5/7, 11 configurations, W=500/2,000/10,000) the estimator is
consistent with exact but carries a **positive bias of roughly +0.006 at W=10,000** (mean
z = +0.81 over 33 runs). This is intrinsic to the frozen estimator, not a defect of this
build: M is a sum of absolute values of noisy quantities, so Jensen's inequality biases each
batch estimate upward, and the prereg averages per-batch M. The bias falls with W and is
essentially gone at W=1e6.

### G4 — GPU resource measurement — **PASS, and the fallback is not needed**

At L=7, W=1,000,000, one replica: **0.85 s, 0.443 GiB peak pool**, against 15.57 GiB available.
A full 8-batch configuration (64 replica runs, both arms) takes **~55 s**. So W=1e6 costs about
3 % of VRAM; the prereg-note contingency "W=1e5 if 1e6 exceeds 16 GB" does not arise, and W=1e7
(~4.4 GiB) would also fit. CPU and GPU backends agree within combined standard error
(|Δ| ≤ 0.013, z ≤ 1.8) on independent RNG streams.

Annihilation efficiency is the reason this is cheap: after each cycle the 10⁶ walkers collapse
onto the reachable support, which at L=7 N=20 is only 10²–10⁴ distinct configurations. The
walker population is far denser than the state space, which is exactly the regime the charter
predicted would strengthen the cancellation.

### G5 — Estimator unbiasedness, separated from witness bias — **PASS**
(`test_estimator_unbiased.py`)

Averaging the replica-cross estimator over 400 independent replica pairs at L=3 N=5 and
comparing to the **exact raw** origin-pair probabilities `q_j` (not the derived witness):

| W | mean of 400 replica pairs | exact `q_j` | z |
|---:|---|---|---|
| 500 | 0.145971, 0.386014, 0.333558 | 0.147587, 0.385070, 0.332409 | −0.97, +0.23, +0.28 |
| 5,000 | 0.148876, 0.383683, 0.331105 | " | +2.49, −1.05, −1.14 |

Worst |z| = 2.49 over six comparisons. So the estimator itself is unbiased, and the
+0.006 bias in M at W=10,000 reported under G3 is located entirely in the witness's absolute
value — a property of the frozen definition, which this build must and does reproduce rather
than correct.

### G6 — A small-W failure mode found and instrumented

At W=500 the two replicas can share **no** configuration in the head-on-pair event set, making
the cross estimator's support exactly zero and M undefined. This build flags such batches as
non-finite and reports the count; it never averages over them. Under the frozen readability
gate ("all 16 configurations return finite estimates") such a configuration is unreadable.

### G7 — A latent infinity found by audit and removed

`cumsum(|u_k|²)` over a site's sector falls short of 1.0 by up to 9.99e-16 for **20 of the 64
local states**. A uniform draw landing in that gap selects `k = d(s)` — an out-of-sector slot
whose sampling probability is exactly 0 — and the `u_k/q_k` weight update then returns an
infinite weight, silently corrupting a batch. Expected incidence is order 1e-5 per benchmark
cell at W=1e6, so it would appear rarely and unreproducibly. The sampler now clamps `k` to the
site's own sector size via a per-state `KMAX` table. Results are bit-identical before and after
on the regression set, so this removes a latent failure rather than changing any number.

## Concordance with the recorded CPU license — indicative only

Error scale at each W, this implementation on **its own** L=7 N=20 configurations, beside the
recorded CPU license figures on the **frozen** L=7 LOW+MID lists. Different configurations, so
this is **not** a gate and licenses nothing; it is a scale check.

Recorded CPU license (frozen L=7 LOW N=20 + MID N=25, 32 configurations) versus this build
(16 fresh L=7 N=20 configurations, exact M computed here, GPU):

| W | | median abs err | p90 | max | median SE | p90 SE | max SE | out-of-range |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 500 | recorded | 0.06238 | 0.26633 | 0.51106 | 0.02163 | — | — | — |
| 500 | this build | 0.18640 | 0.56581 | 1.33487 | 0.05961 | 0.30719 | 0.62367 | 0.0560 |
| 2,000 | recorded | 0.01557 | 0.05626 | 0.10999 | 0.01160 | — | — | — |
| 2,000 | this build | 0.01494 | 0.10827 | 0.21068 | 0.02492 | 0.06373 | 0.11078 | 0.0052 |
| 10,000 | recorded | 0.00611 | 0.01459 | 0.02784 | 0.00571 | 0.00998 | 0.01175 | 0.0000 |
| 10,000 | this build | 0.00774 | 0.01559 | 0.03964 | 0.01310 | 0.01750 | 0.01800 | 0.0000 |
| 1,000,000 | this build | **0.00053** | **0.00143** | **0.00219** | **0.00077** | **0.00154** | **0.00173** | 0.0000 |

The error statistics track the recorded license closely at W=2,000 and W=10,000 (median
0.01494 vs 0.01557; 0.00774 vs 0.00611) and both fall monotonically with W in the same way.
The standard errors run about 2× larger here, and W=500 is much worse here — consistent with
this sample containing heavier configurations (exact basis support up to 5.0e4) and being
drawn entirely from the denser-tailed N=20 cell rather than pooled across N=20 and N=25.
On **these** configurations W=10,000 would fail the frozen median-SE gate (0.01310 > 0.010).
That is a statement about this configuration sample, not about the frozen benchmark, and it
is exactly why the frozen lists cannot be substituted.

At W=500 this build recorded 4 zero-support batches and a 5.6 % out-of-range fraction, which
exceeds the frozen 5 % `ESTIMATOR-UNSTABLE` threshold — the small-W instability of G6 is real
and lands where the frozen gates were designed to catch it.

**What W=1e6 buys.** Against the frozen benchmark gates, W=1e6 on these configurations clears
every one by an order of magnitude or more: median error 0.00053 vs a 0.010 gate (19×), p90
0.00143 vs 0.020 (14×), max 0.00219 vs 0.050 (23×), median SE 0.00077 vs 0.010 (13×), p90 SE
0.00154 vs 0.020 (13×), max SE 0.00173 vs 0.050 (29×), and no out-of-range estimate. Against
the tighter *target readability* gates (median SE ≤ 0.015, p90 ≤ 0.030, max ≤ 0.050) the margin
is 19×/19×/29×. The whole 16-configuration pass took 906 s.

This is the charter's central question answered with numbers: the 4090 moves the workable
population from 10,000 to 1,000,000, and on the *same* 16 configurations the median error falls
14.6× (0.00774 → 0.00053) and the median SE 17× (0.01310 → 0.00077), for 0.44 GiB and 15
minutes per cell. The variance headroom that defeated the path-MC estimator in the denser L=9
cells is squarely within reach — but only the *headroom* is demonstrated here. Nothing about
the held-out cells is licensed or known, and W must still be fixed pre-inspection by whoever
holds the frozen data.

## Forward caution: annihilation efficiency collapses in the dense cells

`l9_probe.py` propagates **one** replica at each held-out size — no witness is read, no target
cell is executed — and measures cost and, more importantly, how many *distinct* configurations
the W=10⁶ walkers occupy after the final resample:

| cell | s/replica | peak VRAM | distinct configs among 10⁶ walkers | walkers per config | 16-config cell |
|---|---:|---:|---:|---:|---:|
| L=7 N=20 (LOW) | 1.27 | 0.44 GiB | 253 | ~4,000 | ~22 min |
| L=9 N=32 (LOW) | 1.83 | 0.65 GiB | 18,460 | ~54 | ~31 min |
| L=9 N=52 (HIGH) | 1.86 | 0.65 GiB | 746,772 | **~1.3** | ~32 min |
| L=11 N=48 | 3.60 | 1.06 GiB | 663,593 | ~1.5 | ~61 min |

The charter reasons that "annihilation efficiency RISES with walker density (more
same-configuration coherent cancellation per cycle — the sign-problem cure strengthens with
scale)". That is right in W and wrong in the cell: the state space grows faster than the
population. Annihilation can only cancel walkers that *collide on the same configuration*, so
its power is set by walkers-per-configuration. At L=7 LOW that ratio is ~4,000 and the
estimator is effectively doing exact linear algebra with noise — which is why W=10⁶ reached
5e-4 there. At **L=9 HIGH it is ~1.3**: there is almost nothing to annihilate, and the
estimator degenerates toward the independent-path estimator that already went
variance-uncontrolled in precisely that cell.

Memory is not the binding constraint — 16 GiB tolerates roughly W=2×10⁷ — but that buys only
~26 walkers per configuration at L=9 HIGH, not thousands. **The 100× walker increase should
therefore not be assumed to rescue L=9 HIGH.** It plainly rescues the L=7 cells and probably
L=9 LOW; L=9 HIGH remains the open risk and must be judged on its own measured SE gates, at a
W fixed before any target is inspected.

(Caveat on the measurement: distinct-configurations-after-resampling is bounded above by W, so
at L=9 HIGH and L=11 it is a *lower* bound on the true reachable support and the real ratio may
be worse, not better.)

## Code hash guard

`ANNIHILATING_MC_EXECUTION_NOTE.md` asks that the estimator be hashed before any held-out cell
runs. For this implementation:

```
sha256(regmodel.py || mc_tables.py || annihil_mc.py || seeds_frozen.py)
  = 634cf7eff8e2cceb894c32e7a7a00cfca02159880abb2a0b7704383541076d26
```

Per-file digests are in `SHA256SUMS.txt`.

## What is needed to clear the block

1. The 32 frozen spectator configuration lists (L=7 LOW N=20, MID N=25), as mode-index sets.
2. Their 32 exact per-configuration M values.
3. A one-line statement of the witness normalisation convention (normalised or raw).

With those three, the official cascade runs unchanged in roughly 20 minutes at W=1e6.

**No held-out target cell has been executed. No target outcome has been inspected.**
