# RESULTS — habit dynamics on CIRISArray: lifespan, formation, taxonomy

Pre-registration frozen and committed at **`cb0e841`** *before* any run
(`scratchpad/HABIT_DYNAMICS_PREREG.md`). Substrate: the ACTUAL CIRISArray GPU kernel
(`/home/emoore/CIRISArray/src/runtime.py`, `Ossicle.KERNEL_CODE`) on the RTX 4090 Laptop
GPU, driven at `iterations = 1` so that the lag unit is one logistic step. Share machinery
and the clip/fold kernel builder imported from the sibling experiment
`array_cap_experiment.py`. Scratchpad only; nothing touches the Lean library, `Stance.lean`
or the audit.

---

## VERDICT

**BOTH pre-registered decay hypotheses are REJECTED. Neither exponential nor power law
describes the decay of whole-only pattern in this substrate — not at the validated
operating point, and not at a single one of 70 points on the coupling × noise map.**

The decay is not a curve at all. It is a **cliff**. At the validated operating point
(κ = 0.05, σ = 1e-3) the k = 3 temporal share is 0.0508 nats at lag 1, 0.0162 at lag 2, and
**exactly at its floor from lag 3 outward** — flat to lag 256, z ≈ 0 at every subsequent
lag. The exponential anchored on the only two live points over-predicts lag 3 by
**6.6 × 10³ σ**; the power law over-predicts it by **1.1 × 10⁴ σ**. Reduced χ² of the better
of the two full fits is **859** (clip) and **1227** (fold). This is not a close call between
the two families; it is both families failing together.

So the pre-registered meanings do **not** apply. There is no characteristic lifespan in the
exponential sense to report as the rent clause's shape, and there is no scale-free decay to
report as its refutation-by-criticality. **The whole-only pattern in this substrate has a
hard finite memory of 2 kernel iterations, and no tail whatsoever.**

Three further results, each with its own boundary-stability verdict:

1. **The whole dies long before the parts.** In the same binarized data, at the same lags:
   whole-only share clears its floor out to lag **2**; pairwise correlation clears its floor
   out to lag **16** (clip) / **11** (fold). Order-3 pattern is the *first* thing to go, not
   the last — by a factor of 5.5–8. STABLE across boundary conventions.
2. **Formation is as fast as decay.** From a randomized start the share reaches 90 % of its
   stationary value in **4 kernel iterations** (t₉₀ = 4, τ_form ≈ 4), with an oscillatory
   period-2 approach whose amplitude (7.7 %, 4.5 σ over t = 4–20) is gone by t ≈ 20–60. There
   is no slow congealing on this substrate.
3. **The "congealed habit" corner is never reached — 0 of 70 grid points.** The substrate
   reaches memoryless-like (55 of the 62 cells carrying real signal) and chaotic-churn (5);
   the only two frozen-but-empty cells are clip-only and fail the boundary discriminator.
   Nowhere is pattern both strong and persistent.

**Nothing here is a discovery of order-3 / whole-only structure in the array.** Its presence
was pre-committed as expected, and it is reported only as a magnitude. Everything claimed is
a shape, an ordering, or a timescale.

---

## GATES — all four PASS, before any measurement

| gate | result |
|---|---|
| 1. share machinery (`array_cap_experiment.gate()`) | PASS — k=3 exact parity → ln 2 exactly (saturates its cap); exact independence → 0; k=5 pair-uniform code state → 2 ln 2 exactly; IPF residual 0.0; `shareK(k=3)` ≡ `bench_detector.C3` to 0.0 on 20 random states; sampled parity fires (z = 1.97e5), sampled independence floors (z = 0.71) |
| 2. **kernel equivalence** (new) | PASS — with σ = 0, **100 calls at `iterations = 1` reproduce 1 call at `iterations = 100` BIT-IDENTICALLY** (max diff 0.000e+00), for both clip and fold builds |
| 3. **instrumentation fidelity** (new) | PASS — the clamp-counter build reproduces the SHIPPED `Ossicle` kernel bit-identically over 50 iterations |
| 4. **fit machinery** (new) | PASS — recovers τ = 25 to 0.5 %, α = 1.2 to 2.8 %, selects the generating family in both directions, returns DEGENERATE on pure noise |

Gate 2 is what licenses the whole experiment: driving at `iterations = 1` is not a modified
dynamics, it is the *same* trajectory read at finer stride. Without it the lag axis would
have been an assumption.

---

## MEASUREMENT 1 — LIFESPAN

κ = 0.05, σ = 1e-3, 2000 settle iterations, N = 1024 frames, 16 start times × 12 288
independent (ossicle, cell) replicas (T = 196 608 per lag), 5 independent seeds. Error bars
are the across-seed sd / √5 — real error bars from independent realizations.

### The curve (clip; fold agrees to < 1 % at every lag)

| Δ | excess (nats) | ± | ceiling fraction | pooled z | indep-safe z | pair max&#124;corr&#124; |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 5.076e-02 | 1.2e-04 | 0.0732 | 18024 | **563** | 0.593 |
| 2 | 1.621e-02 | 1.5e-04 | 0.0234 | 4364 | — | 0.434 |
| **3** | **−6.6e-07** | 7.9e-07 | −0.000 | **−0.2** | — | 0.155 |
| 4 | −2.0e-06 | 5.6e-07 | −0.000 | −0.5 | — | 0.039 |
| 8 | +2.2e-06 | 2.4e-06 | 0.000 | 0.8 | **−0.4** | 0.023 |
| 16 | −1.7e-06 | 3.9e-07 | −0.000 | −0.6 | — | 0.010 |
| 64 | −1.3e-06 | 7.9e-07 | −0.000 | −0.4 | **−0.9** | 0.002 |
| 256 | −1.1e-06 | 5.9e-07 | −0.000 | −0.3 | **−0.8** | 0.002 |

Floors: matched pairwise-maxent surrogate null 1.7e-06 ± 2.2e-06; shuffle floor
4.8e-06 ± 7.2e-06. Tied fraction **0.00000** at every lag. Cap-compliant at every lag
(`shareK ≤ k·ln2 − max_pair H(pair)`, and ≤ (k−2)·ln 2). Reproducibility across the 5 seeds:
excess(1) = 0.05051, 0.05074, 0.05054, 0.05090, 0.05113.

### Both hypotheses, and how they die

| | pre-registered verdict (AICc, as specified) | ΔAIC | fitted parameter | **adequacy** |
|---|---|---|---|---|
| clip | EXPONENTIAL | +736.4 | τ = 0.24 [0.24, 0.25] | **χ²_red = 859 → BOTH_REJECTED** |
| fold | EXPONENTIAL | +1565.4 | τ = 0.27 [0.27, 0.27] | **χ²_red = 1227 → BOTH_REJECTED** |

The pre-registered rule selected EXPONENTIAL, and reporting only that would have been
misleading in two independent ways, so both are stated:

- **The fitted τ lies below the instrument's resolution.** τ ≈ 0.25 kernel iterations, where
  the smallest lag the kernel can express is 1. A lifespan shorter than one step of the
  dynamics is not a lifespan; it is the fitter's way of saying "gone before I can look
  again".
- **The winning model does not fit the data.** χ²_red ≈ 10³. What the AIC comparison
  actually established is which of two inadequate models is less inadequate.

The sharpest single statement of the failure, anchored on the only two live points:

| model anchored on Δ = 1, 2 | prediction at Δ = 3 | observed at Δ = 3 | over-predicts by |
|---|---|---|---|
| exponential, τ = 0.876 | 5.18e-03 | −6.6e-07 ± 7.9e-07 | **6 580 σ** |
| power law, α = 1.647 | 8.31e-03 | −6.6e-07 ± 7.9e-07 | **10 600 σ** |

(fold: 4 250 σ and 6 900 σ respectively.)

**This is a pre-registered kill firing on both staked hypotheses at once.** It is reported
here as plainly as a survival would have been, per house discipline rule 7.

### The one shape that is real: whole-only dies before pairwise

The pair meter runs on exactly the same binarized triples. Using the large-lag plateau as
the pairwise floor (0.0027 ± 0.0011 clip, 0.0029 ± 0.0014 fold) and a 5-sd threshold:

| | last lag clearing its floor |
|---|---|
| whole-only share (k = 3) | **2** |
| pairwise &#124;corr&#124;, clip | **16** |
| pairwise &#124;corr&#124;, fold | **11** |

At Δ = 3 the pairwise correlation is still 0.155 — 136 sd above its floor — while the
whole-only share is exactly at zero. So the cliff is not "everything decorrelates at lag 3".
It is specifically the **order-3** structure vanishing while order-2 structure is still
plainly alive. Whole-only pattern is the most fragile layer in this substrate, by a factor of
5.5–8 in lag.

A mechanism is *suggested but not tested here*: the local system is a 3-node chain, so
b_t, b_{t+1}, b_{t+2} are all functions of one 3-dimensional state, and once the sampled span
2Δ exceeds that state's mixing time the order-3 term has nothing left to encode. This is a
hypothesis about why the cutoff is sharp, not a measurement, and is flagged as such.

---

## MEASUREMENT 2 — FORMATION

Fresh randomized initial states (the runtime's own `uniform(0.2, 0.8)`), **no settle**,
N = 256 frames from t = 0, share estimated at each elapsed t on frames (t, t+Δ, t+2Δ) pooled
over all 12 288 units at that single time — T = 12 288, genuinely i.i.d. across units at
every point of the curve. 8 independent initializations; error bars = across-init sd / √8.

**The primary threshold produced a degenerate point and this is reported, not buried.** With
the binarization threshold fixed at the attractor's late-quarter median (the pre-registered
primary), excess(t = 0) came out as −2.9e-16 — i.e. *exactly* zero, because the initial
uniform(0.2, 0.8) states do not straddle the attractor median, one channel is constant, and
the estimator returns 0 by construction. That is an artifact of the threshold, not a
measurement of the initial condition.

The pre-registered sensitivity — threshold recomputed within each t — settles it:

| | excess(0) | E_∞ (plateau) | excess(0) / E_∞ | t₉₀ | τ_form |
|---|---|---|---|---|---|
| Δ = 1, clip | 4.50e-03 | 5.093e-02 | 0.088 | **4** | 3.98 |
| Δ = 1, fold | 4.50e-03 | 5.093e-02 | 0.088 | **4** | 3.98 |
| Δ = 2, clip | 1.52e-04 | 1.584e-02 | 0.010 | **3** | 8.59 |
| Δ = 2, fold | 1.52e-04 | 1.583e-02 | 0.010 | **3** | 8.59 |

**BUILDS — at the instrument's resolution.** Whole-only pattern starts at 9 % of its
stationary value and reaches 90 % of it in **4 kernel iterations**. The approach is
oscillatory (period-2): the odd/even alternation is +7.7 % of the mean at t = 4–20 (4.5 σ),
+0.3 % at t = 20–60 (0.6 σ), and consistent with zero thereafter — so the ensemble's coherent
transient is gone by t ≈ 20–60 while the share itself has already plateaued by t ≈ 4.

**The pre-registered verdict function returned INDETERMINATE, and the reason is that the test
was mis-specified for a build this fast.** It asked for Spearman monotonicity over the first
half of the run: ρ = 0.073, p = 0.41 across t = 0…126, because 122 of those 127 points are
flat plateau. Over t = 0…9 the same statistic gives ρ = 0.697, p = 0.025. The pre-registered
number is reported as it came out; the honest description of the curve is BUILDS, with a
formation time of about 4 kernel iterations.

**Boundary discriminator: TRIVIAL for this measurement.** Clip and fold agree to 15
significant figures on excess(0) and τ_form, because during the first few iterations from a
randomized start the clamp has essentially not yet bound (rate 3.4e-5 / 4.0e-5 over the whole
run). The two kernels are the same function on the transient data that occurred, so their
agreement carries no information about robustness — exactly the case the prereg named.

**What this is NOT.** This is a **classical analogue only** of Smolin-style precedence
accumulation. It does not test precedence in quantum mechanics; there is no quantum content
anywhere in this measurement. And the timescale it delivers is 4 iterations, which is a
statement that on this substrate there is essentially **no** accumulation process to observe —
the pattern is present as soon as the dynamics have run at all.

---

## MEASUREMENT 3 — TAXONOMY

κ ∈ {0, 0.02, 0.05, 0.10, 0.20, 0.35, 0.50} × σ ∈ {0, 1e-4, 1e-3, 1e-2, 1e-1} × {clip, fold}
= 70 conditions. 2000 settle iterations, N = 512 frames, 16 lags, 8 start times, full
surrogate + shuffle floors and an independence-safe single-start z at Δ = 1 for every cell.
**Zero cap violations in 70 cells** (both the robust bound and the headline bound hold
everywhere) — an incidental replication of the sibling experiment's Job 1.

Because no cell admits an adequate exponential fit, the maps report the **model-free
lifespan**: the last lag whose excess clears 5 × its own error bar. The thresholds
themselves (CF ≥ 0.10 high, lifespan ≥ 20 long) are the pre-registered ones, unchanged.

### Ceiling fraction at Δ = 1 (excess / (k−2)·ln 2, the machine-checked cap)

```
CLIP    sigma \ kappa       0      0.02      0.05       0.1       0.2      0.35       0.5
        0              0.0599    0.0696    0.0718    0.0296    0.0517    0.0000    0.0000
        1e-4           0.0498    0.0689    0.0729    0.0301    0.0645    0.0633    0.0000
        1e-3           0.0548    0.0707    0.0750    0.0305    0.0654    0.1114    0.0028
        1e-2           0.0553    0.0673    0.0615    0.0322    0.0723    0.0918    0.0450
        1e-1          -0.0000    0.0002    0.0008    0.0025    0.0077    0.0076    0.0036

FOLD    sigma \ kappa       0      0.02      0.05       0.1       0.2      0.35       0.5
        0              0.0599    0.0696    0.0705    0.0804    0.1102    0.0329    0.0002
        1e-4           0.0498    0.0689    0.0737    0.0830    0.1102    0.0356    0.0005
        1e-3           0.0548    0.0707    0.0740    0.0771    0.1109    0.0356    0.0001
        1e-2           0.0553    0.0673    0.0622    0.0735    0.1014    0.0303    0.0005
        1e-1           0.0092    0.0100    0.0117    0.0117    0.0099    0.0011   -0.0000
```

### Lifespan — last lag clearing its floor, in kernel iterations

```
CLIP    sigma \ kappa       0      0.02      0.05       0.1       0.2      0.35       0.5
        0                   4         4         2         3        16        11        64*
        1e-4                4         5         2         3         8       192         192*
        1e-3                4         4         2         3         4        16        11
        1e-2                5         4         2         3         3         5         6
        1e-1                0         1         0        96         2         2         1

FOLD    sigma \ kappa       0      0.02      0.05       0.1       0.2      0.35       0.5
        0                   4         4         2         2         6         3         0
        1e-4                4         5         2         2         6         3         4
        1e-3                4         4         2         4         6         3         2
        1e-2                5         4         2         4         4         5         0
        1e-1                1         1         1         1         1         0         0
```
`*` = disqualified: the independence-safe z at Δ = 1 is 0.3 and 0.2 respectively, i.e. **no
signal at all**, so the "lifespan" is a pooled-estimator artifact. The independence-safe
check was pre-registered precisely to catch this and it did.

### Fitted τ

**`n/a` in all 70 cells.** Not one grid point, under either boundary, at any coupling or
noise, admits an adequate exponential or power-law fit. Final verdicts across the map:
46 BOTH_REJECTED, 17 INDETERMINATE, 4 DEGENERATE, 3 UNRESOLVED — **zero EXPONENTIAL, zero
POWER_LAW**. Every cell whose fit *is* adequate (χ²_red ≲ 5) is a cell with no signal to fit
(CF ≈ 0.001–0.03), and none of those selects a family either.

### Corners reached

Restricted to the 62 cells carrying real signal (independence-safe z at Δ = 1 above 5):

| corner | cells | where |
|---|---|---|
| **memoryless-like** (CF < 0.10, lifespan < 20) | **55** | essentially the whole map |
| **chaotic-churn** (CF ≥ 0.10, lifespan < 20) | 5 | fold κ = 0.20 at every σ ≤ 1e-2 (CF 0.10–0.11, lifespan 4–6); clip κ = 0.35, σ = 1e-3 |
| **frozen-but-empty** (CF < 0.10, lifespan ≥ 20) | 2 | clip only — κ = 0.35 σ = 1e-4, and κ = 0.10 σ = 0.1. Fold gives lifespan 3 and 1 at the same points ⇒ **ARTIFACT** |
| **congealed habit** (CF ≥ 0.10, lifespan ≥ 20) | **0** | **never reached** |

**The substrate reaches only memoryless-like and chaotic-churn.** Persistence and strength are
not simultaneously available on this device: everywhere pattern is strong it is short-lived,
and every long lifespan on the map is either clip-only (and reversed by the smooth boundary)
or has no signal behind it.

### Two structural facts the map delivers

**(a) Most of the whole-only share needs no coupling at all.** At κ = 0 the three oscillators
are uncoupled and `b` is an autonomous logistic map, yet CF = 0.050–0.060 — against 0.062–0.075
at κ = 0.05. Coupling adds roughly 20–40 %; the bulk of the array's temporal order-3 is
intrinsic to a *single* logistic map. Deflationary, and directly relevant to the standing
trap.

**(b) Coupling shortens the whole-only lifespan.** 4–5 iterations at κ ≤ 0.02, 2 at κ = 0.05.

Both facts are measured in the cells where **the clamp binds exactly zero times** (κ ≤ 0.02,
σ ≤ 1e-2, both boundaries, rate 0.00e+00). Two things follow and they are different: the
clip/fold comparison there is **vacuous as a test** (TRIVIAL, as pre-registered), *and* the
readings there **cannot be clamp artifacts at all**, because no clamp event occurred. The
second is the stronger fact and is why these are the cleanest numbers on the map.

**(c) Noise at σ = 0.1 erases everything**: CF drops to 0.001–0.012 and lifespan to 0–1
across the entire coupling dial, under both boundaries.

**The pre-registered deterministic degenerate corner did not misbehave.** κ = 0, σ = 0 was
named in advance as the cell where `b` is an autonomous *deterministic* map, so
(b_t, b_{t+Δ}, b_{t+2Δ}) lies on a curve and order-3 at small Δ is present by construction.
It reads CF = 0.0599 with lifespan 4 — indistinguishable from the same cell with noise added
(CF = 0.0548, lifespan 4 at σ = 1e-3). The construction therefore contributes nothing
anomalous, and no number in this run rests on it. Labelled as a construction regardless.

---

## CLIP vs FOLD — stability verdict per finding

| finding | verdict | evidence |
|---|---|---|
| lifespan = 2 at κ = 0.05; both families rejected | **STABLE** | levels agree to 0.3 % at every lag; lifespan identical (2); both arms BOTH_REJECTED; clamp binds (3.5e-5 / 4.1e-5) so non-trivial — though *weakly*, and this is the honest limitation of the discriminator at this operating point |
| whole dies before pairwise | **STABLE** | 16 vs 11 — adjacent grid points, both ≫ 2 |
| formation t₉₀ = 4 | **TRIVIAL** | clip and fold bit-identical on the transient; the clamp has not yet bound. No robustness information. |
| lifespan 4–5 and CF ≈ 0.05–0.07 at κ ≤ 0.02 | **TRIVIAL, but artifact-free by construction** | clamp binding rate exactly 0.00e+00 |
| CF at κ = 0.10 (0.030 clip vs 0.080 fold) and κ = 0.20 (0.052–0.072 vs 0.101–0.111) | **level ARTIFACT, shape roughly stable** | 1.7–2.7× level disagreement with the clamp active (2 %, 16 %); lifespans 3 vs 2–4 and 3–16 vs 4–6 |
| long lifespans (192, 64, 96, 16) at κ ≥ 0.20 clip | **ARTIFACT** | fold gives 3–6 at the same points; tied fraction reaches 0.086–0.097 (> the 0.01 threshold) at κ = 0.35–0.50, σ = 0; two of them have independence-safe z < 1; and the sibling run independently found the i.i.d. surrogate null void at κ ≥ 0.35 (integrated autocorrelation 87–365) |

**What is substrate:** the cliff shape and its rejection of both families; the 2-iteration
lifespan at κ = 0.05 and the 4–5-iteration lifespan where the clamp never fires; the
whole-before-pairwise ordering; the ≈ 4-iteration formation time; the absence of a congealed-habit
corner; the coupling-independence of most of the share.

**What is artifact-suspect:** every absolute ceiling-fraction level at κ ≥ 0.10 (the two
boundaries disagree by up to 2.7×); every long lifespan on the map; everything at
κ ≥ 0.35 under clip.

---

## COORDINATION — this run and the sibling cap-compliance run

`ARRAY_CAP_RESULTS.md` reports the array's ceiling fraction as **≈ 0.03 %** and states that
"the array as shipped presents no temporal structure at its own measurement cadence". This
run reads **7.3 %** at lag 1 on the same substrate with the same estimator. **These are the
same curve, sampled at two lags, and this measurement explains that one.** The shipped
kernel runs 100 logistic iterations per burst; the whole-only pattern is dead after 2. By the
device's own measurement cadence the pattern has been gone for 98 iterations. The sibling's
τ_int ≈ 1 (successive bursts fully decorrelated) and this run's 2-iteration lifespan are the
same fact measured from two directions.

The two runs also agree on the clamp-binding rate at κ = 0.05 (2.4e-5 / 3.1e-5 there,
3.5e-5 / 4.1e-5 here — the small excess is expected, since driving at `iterations = 1` injects
the σ noise 100× more often per unit of lattice time), and on zero binding at κ ≤ 0.02.

---

## WHAT IS NOT CLAIMED

1. **No discovery of order-3 / whole-only structure in the array.** Pre-committed and
   honoured: the level is expected, was reported only as a magnitude, and §"Two structural
   facts" shows most of it survives with the coupling turned off entirely.
2. **No world-claim from the rent clause, and no refutation of it either.**
   `Core/Maintenance.lean` is a theorem about a model; nothing measured here can touch it.
   What can be said is narrower and is said only about this substrate: **the rent clause's
   geometric shape is not the shape this lattice's whole-only pattern decays in**, and the
   `e-upkeep` wager gains no support from this run. The power-law alternative is rejected
   here too, so this run supports neither side of the pre-registered pair.
3. **No quantum content.** Measurement 2 is a classical analogue of precedence accumulation
   and nothing more.
4. **IAAFT was not used and would not have certified anything** (a clip artifact survived it
   at z = 86 on 2026-07-24). Its absence is not a gap.
5. **No absolute-level claim about the substrate** except in the cells where the clamp
   provably never fires.
6. **Instrument limits that bound every number above.** The minimum expressible lag is 1
   kernel iteration, so any lifespan below that is unresolvable in principle; the boundary
   discriminator is weak at κ = 0.05 (the clamp binds once per ~29 000 applications) and
   vacuous at κ ≤ 0.02; the i.i.d. surrogate null is unreliable at κ ≥ 0.35 (per the sibling
   run) and results there are reported but not quoted.

---

## FILES

- `scratchpad/HABIT_DYNAMICS_PREREG.md` — frozen at `cb0e841`, before any run
- `scratchpad/habit_dynamics.py` — driver, gates, fits, all three measurements
- `scratchpad/habit_lifespan.json`, `habit_taxonomy.json` + `.log`,
  `habit_formation.json` + `.log`, `habit_formation_perT.json` + `.log` — raw results
- imported machinery: `scratchpad/array_cap_experiment.py` (share, caps, clip/fold kernel
  builder), `scratchpad/bench_detector.py` (pair meter, C3 cross-check)

Primary seed 20260725; lifespan replicated across seeds {20260725, 99, 7, 1337, 4242};
formation across 8 initializations. Research → scratchpad memo → Eric's review. Nothing
pushed.

---
---

# FOLLOW-UP (same day, after the main run) — the dimensionless ratio, quantization, and null validity at high coupling

Three additions requested after `6b97e15`. Script: `scratchpad/habit_ratio.py`; raw output
`habit_ratio_results.json` / `habit_ratio.log`. Trajectories are reproduced with the same
seeds, settle and N as the taxonomy, so the new pair curves join to `habit_taxonomy.json`
row-for-row.

## FOLLOW-UP VERDICT

**A — the ratio: FRAGILE, unambiguously.** τ_share / τ_pair is **below 1 at 58 of the 61
signal-carrying grid points** where it is defined, by both matched definitions. At the
validated operating point it is **0.087** (floor-crossing definition) or **0.75** (1/e
definition). The DEEP-HABIT signature (ratio > 1) appears at exactly **4 cells out of 62 —
every one of them under the native clip boundary, and every one reversed by the reflecting
fold** (24.0 → 0.17, 17.5 → 0.19, 1.45 → 0.28, 2.20 → 0.03). On this substrate, whole-only
structure dying first is the finding, and the one signature that would have said otherwise
is a clamp artifact.

**B — quantization: NO, and it cannot even be tested here.** The largest whole-only share
anywhere on the entire map, at any lag, is **0.111 bits**. Integer plateaus require at least
1 bit. Zero of 1120 (grid point × lag) readings sit within 0.05 bits of a nonzero integer.
The substrate never holds even one eighth of a single bit of whole-only pattern.

**C — null validity: our null SURVIVES where the sibling's broke, and the cross-run control
proves it rather than asserting it.** Channels drawn from three independent runs — which
cannot share structure — floor at |z| ≤ 1.1 at every point tested, **including clip at
κ = 0.35 and κ = 0.50** where the sibling found cross-run channels firing at z = 34.9. The
reason is structural and is stated below. **A correction to the diagnostic itself is also
reported: τ_int = 1.00 is an artifact of the estimator's stopping rule on this readout and
must not be read as a clean bill of health.**

---

## A — τ_share / τ_pair, the dimensionless classifier

τ in kernel steps is unit-dependent and cannot classify across conditions; the ratio is
clock-independent. **The comparator is the pairwise mutual information of the same binarized
triples at the same lags** — chosen over the integrated autocorrelation time because MI is in
nats, exactly like the share, so numerator and denominator are the same kind of quantity.
(The main document's pairwise lifespans of 16 / 11 used max |corr| instead; on MI the same
data gives 23 / 23. Both are reported; nothing downstream depends on which.)

**No fitted τ_share exists to divide with** — the share decay rejects both fitted families
(main document §Measurement 1). So both timescales are taken model-free, in two matched
forms, and both are applied identically to numerator and denominator:

| definition | what it is |
|---|---|
| **L** | last lag whose value clears its own floor by 5 sd |
| **τ_e** | lag interval over which the value falls to 1/e of its lag-1 value, log-linear interpolation |

### At the validated operating point (κ = 0.05, σ = 1e-3, 5 seeds)

| | L_share | L_pair | **ratio_L** | τ_e(share) | τ_e(pair) | **ratio_τe** |
|---|---|---|---|---|---|---|
| clip | 2 | 23 | **0.087** | 0.876 | 1.163 | **0.753** |
| fold | 2 | 23 | **0.087** | 0.856 | 1.162 | **0.737** |

**STABLE across boundary conventions** — the two arms agree to 2 % on both definitions.

**The two definitions disagree by a factor of 8, and that disagreement is itself the
result.** The ratio is not a single number on this substrate because the two decays are not
in the same functional family: near the 1/e point the share and the pairwise MI fall at
comparable rates (ratio 0.75), but the share then falls off a cliff while the MI keeps
decaying smoothly, so by the floor-crossing point the ratio is 0.087. **The honest statement
is the classification, not the number: under every definition tried, at every operating
point, the ratio is below 1.** Reporting a single τ_share/τ_pair would have implied a
constancy the data do not have.

### Across the whole grid (62 cells carrying real signal)

| | n defined | min | median | max | **> 1.25** | ≈ 1 (0.8–1.25) | **< 0.8** |
|---|---|---|---|---|---|---|---|
| ratio_L | 61 | 0.000 | **0.188** | 24.0 | 3 | 0 | **58** |
| ratio_τe | 61 | 0.092 | **0.388** | 1.449 | 1 | 8 | **52** |

### The four DEEP-HABIT candidates, and why none survives

| κ | σ | clip ratio_L | clip ratio_τe | **fold ratio_L** | **fold ratio_τe** |
|---|---|---|---|---|---|
| 0.10 | 1e-1 | **24.0** | 0.727 | 0.167 | 0.342 |
| 0.35 | 1e-4 | **17.5** | 0.124 | 0.188 | 0.269 |
| 0.35 | 1e-3 | 0.70 | **1.449** | 0.188 | 0.279 |
| 0.50 | 1e-3 | **2.20** | n/a | 0.031 | 0.371 |

All four are the same cells the main document already flagged: they are exactly the cells
carrying the map's only long `L_share` values, which the boundary discriminator reverses.
**The clamp is what manufactures apparent deep habit.** Under a smooth boundary the
signature vanishes at every one of them.

**Classification, in the requested terms: ratio < 1 — higher-order pattern is the FRAGILE
part, and it dies first.** This is the boring-but-likely outcome and it is reported as
plainly as a DEEP-HABIT result would have been.

---

## B — is the decay quantized?

Code and stabilizer states carry share at integer multiples of ln 2, so a substrate shedding
whole-only *bits* one at a time would show plateaus near integers in share / ln 2. The curves
are shown in units of ln 2; no fit is forced.

**Measurement 1, share in bits vs lag** (κ = 0.05, 5-seed mean; clip, fold identical to 3 dp):

```
 lag:      1        2        3        4        6        8       ...   256
 clip:  0.07324  0.02338  -0.00000  -0.00000  0.00000  0.00000  ...  -0.00000
 fold:  0.07345  0.02283   0.00000   0.00000  0.00000  0.00000  ...   0.00000
```

**There is no plateau structure, and there is no room for any.**

- Largest whole-only share **anywhere** on the map, any coupling, any noise, any boundary,
  any lag: **0.1114 bits** (0.0772 nats), at clip κ = 0.35, σ = 1e-3 — itself a cell the
  boundary discriminator rejects. The largest boundary-stable value is 0.075 bits.
- **0 of 1120** (grid point × lag) readings fall within 0.05 bits of a nonzero integer.
- The curve has no flats at all: it is two points and then floor. Nothing to mistake for a
  step.

So the integer-plateau hypothesis is **untestable above n = 0 on this device** — not
refuted in general, simply unreachable, because the substrate never accumulates a whole bit
of whole-only pattern to shed. Reported as the null expectation confirmed, with the
limitation stated rather than dressed up as a test that passed.

---

## C — null validity at κ ≥ 0.35, and a correction to the τ_int diagnostic

The sibling run found the i.i.d. multinomial surrogate **broken for clip at κ ≥ 0.35**
(τ_int 87–365, effective sample ~16–70, cross-run channels firing at z = 34.9). That
constraint was taken seriously and tested directly rather than assumed to transfer.

### The cross-run control — three independent runs, which cannot share structure

Slot j of the triple is drawn from run j (seeds 20260725 / 424242 / 777), identical
parameters, identical marginals, identical autocorrelation, same start times, same pooling.
True share is zero by construction. Any |z| > 5 proves the null mis-specified.

| κ | σ | boundary | lag-1 ACF | within-run z | **cross-run z** | verdict |
|---|---|---|---|---|---|---|
| 0.05 | 1e-3 | clip | −0.539 | 8037 | **−0.7** | NULL SOUND |
| 0.20 | 1e-3 | clip | −0.319 | 9704 | **−0.6** | NULL SOUND |
| **0.35** | 1e-3 | **clip** | −0.600 | 12628 | **+0.1** | **NULL SOUND** |
| **0.50** | 1e-2 | **clip** | −0.736 | 4473 | **+0.0** | **NULL SOUND** |
| 0.35 | 1e-3 | fold | −0.711 | 2958 | **+1.1** | NULL SOUND |
| 0.20 | 1e-3 | fold | −0.512 | 12314 | **−0.3** | NULL SOUND |

**Why this reading survives where the sibling's did not — a structural difference, not a
rescue.** The sibling's channels are group-means of the phase metric read as a *time series*
across bursts, so its effective sample size is limited by the temporal autocorrelation of
that series. This reading's samples are **12 288 (ossicle, cell) replica units at a fixed
time slice**; cells do not couple to cells and ossicles do not couple to ossicles, so those
units are structurally independent, and the pooling exposure to temporal autocorrelation is
limited to the 8–16 start times. The cross-run control tests exactly that exposure — it uses
the same start times and the same pooling — and it floors. So z-scores from this experiment
**are** quotable at κ ≥ 0.35, on the evidence of the matched control, and the main
document's numbers there stand. They remain excluded from anything quotable on the separate
and unchanged grounds already given: boundary-unstable, and tie-contaminated (tie 0.086–0.097).

### Correction: τ_int = 1.00 on this readout is an artifact of the stopping rule

The sibling's `acf_time` accumulates the autocorrelation until the first non-positive term.
**This substrate's ACF is oscillatory with a strongly negative lag-1 term** — measured lag-1
ACF ranges from **−0.769 to +0.125** across the grid, and is negative at 67 of 70 cells. The
estimator therefore truncates immediately and returns exactly 1.00, which looks like a clean
bill of health and is nothing of the kind. Applying it without this check would have been the
mirror image of the sibling's failure: their rule over-reported dependence on a smooth
readout, and it under-reports on an oscillatory one.

A fixed-window estimate, `τ_fixed = 1 + 2 Σ_{L=1..32} ρ(L)` with no truncation, is reported
instead:

- **τ_fixed < 1 at 67 of 70 cells** (range −0.80 to 1.52). Below 1 means the samples are
  *anti*-correlated, so the effective sample size **exceeds** T and the i.i.d. surrogate is
  conservative, not optimistic.
- The only cells with τ_fixed > 1 are three high-noise ones (σ = 0.1, κ ≤ 0.05, clip;
  τ_fixed = 1.18–1.52 — at worst a 52 % inflation, against the sibling's 87–365×). Two of the
  three carry no signal at all (independence-safe z = −0.5 and +0.4) and the third is
  CF = 0.0008.
- The strongly negative lag-1 ACF also explains, independently, the period-2 oscillation seen
  in the formation transient (main document §Measurement 2).

**Nothing in the main document changes as a result of this follow-up.** The ratio sharpens
its central finding into a dimensionless, clock-independent form; the quantization check adds
a clean negative; and the null-validity control converts an inherited caution into a tested
result — while correcting the diagnostic that produced the caution.
