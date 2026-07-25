# PRE-REGISTRATION — habit dynamics on CIRISArray: lifespan, formation, taxonomy

Written and committed BEFORE any hardware run. Substrate is the REAL CIRISArray GPU kernel.
Sibling experiment `ARRAY_CAP_PREREG.md` runs concurrently on the same box; its share
machinery and kernel builder are **imported, not reimplemented**.

---

## 0. THE STANDING TRAP, AND WHY THIS EXPERIMENT IS NOT CAUGHT BY IT

**Pre-committed, binding on every result below.** The 2026-07-24 hunt established that
order-3 / whole-only temporal structure in a coupled-logistic lattice is

- **EXPECTED** — all chaotic dynamics carry it, so its presence is not news;
- **IMPLEMENTATION-SENSITIVE** — clip boundary gave C3 = 0.0065 where wrap gave 0.0000 at
  identical coupling, and this kernel's own `fminf(fmaxf(x, 0.001f), 0.999f)` *is* that clip;
- **NOT CERTIFIED BY IAAFT** — a clip artifact survived an IAAFT null at z = 86.

**This experiment is therefore FORBIDDEN from claiming discovery of order-3 / whole-only
structure in the array, and no result of it may be so framed.** A positive share is the
expected outcome, is reported as a magnitude, and is never a finding.

**What this experiment is about instead: the DYNAMICS of that share — curves, not levels.**

The dodge is differential measurement. A constant additive artifact — clip-induced pile-up
at the boundary, or any other fixed estimator offset — contributes an **offset to the
absolute share**. It does **not** shape how share **varies with lag**, nor how share
**builds after a perturbation**. So:

- the **level** share(Δ) is artifact-contaminated and is never quoted as a substrate property;
- the **shape** — decay constant τ, model family (exponential vs power law), build time
  τ_form, exponent α — is what is measured, because the offset enters every point of the
  curve equally and drops out of the shape.

Every shape is fitted with an explicit additive plateau `c` as a free nuisance parameter,
so that a constant artifact is *absorbed* rather than assumed absent.

**The clip-vs-fold comparison is applied to the SHAPE, not the level.** Levels are expected
to differ between boundary conventions. A shape that is stable across boundary conventions
is a property of the substrate; a shape that flips is an artifact and is reported as one.

---

## 1. SUBSTRATE AND THE LAG UNIT

The ACTUAL kernel: `/home/emoore/CIRISArray/src/runtime.py`, `Ossicle.KERNEL_CODE`, driven
on the RTX 4090 Laptop GPU. No numpy reimplementation. **If the kernel cannot be driven,
the run is abandoned and reported as such — no substitute.**

Array: `n_rows = 3`, `n_cols = 64` ⇒ 192 ossicles; `n_cells = 64`; `r_base = 3.70`,
`r_spacing = 0.03`, `twist_deg = 1.1`. Read off the kernel and stated up front: every
ossicle receives the **same** parameter row (`_update_gpu_params` broadcasts one row to
all), cells do not couple to one another, and ossicles do not couple to one another.
Consequently the device is **12 288 statistically identical, independent replicas** of one
3-node chain `a — b — c` with `r_a = 3.70`, `r_b = 3.73`, `r_c = 3.76`. Pooling over
(ossicle, cell) units is therefore pooling over i.i.d. replicas, not over a heterogeneous
mixture — this is stated before the run because a heterogeneous mixture would itself
manufacture order-3 structure.

**The lag unit is one kernel logistic iteration**, and this requires driving the kernel with
`iterations = 1` per call, so that one call advances the lattice by exactly one step. This
is the same kernel, same code path, same compiled string — only the internal loop's trip
count differs. It is necessary: at r ≈ 3.7 the Lyapunov time is a few iterations, so at the
shipped `iterations = 100` every lag ≥ 1 burst is already past the decorrelation time and no
decay curve exists to measure.

Two consequences, both stated as design facts rather than discovered later:

- **KERNEL-EQUIVALENCE GATE (new, hardware-side).** With σ = 0, one hundred sequential calls
  at `iterations = 1` must reproduce one call at `iterations = 100` **bit-identically** (same
  float32 arithmetic, same order). Checked on the real device before any measurement. FAIL ⇒
  stop, no measurement, report the failure.
- The additive σ noise, injected on the states between calls, becomes **per-update** noise at
  `iterations = 1`. This *removes* the bench's caveat #1 (noise injected only between
  100-iteration bursts). It also means σ = 1e-3 here is applied 100× more often per unit of
  lattice time than at the validated bench operating point. σ is a swept dial in
  Measurement 3, and the σ = 1e-3 column is included as instructed; the difference in
  injection cadence is disclosed and not smoothed over.

### The boundary discriminator

Both boundary treatments are compiled from the **same** `KERNEL_CODE` string with **only**
the three clamp lines replaced (`build_kernel` imported verbatim from
`array_cap_experiment.py`):

- **CLIP** (native, as shipped): `fminf(fmaxf(x, 0.001f), 0.999f)`.
- **FOLD** (reflecting): a continuous triangular fold of the same interval — no flat region,
  no pile-up, no manufactured ties.

Both carry a clamp-event counter that does not enter the state update; the **clamp-binding
rate** is reported per condition. Interpretation rule, pre-registered: where the binding rate
is exactly zero, CLIP and FOLD are the *same function on the data that occurred*, so
agreement there is **TRIVIAL** and is labelled trivial — it is not evidence of robustness.

---

## 2. THE READING AND THE ESTIMATOR

**Reading (all three measurements):** k = 3 **temporal** share of one channel — oscillator
**b**, the chain's centre node, raw cell state — sampled at three times `t`, `t+Δ`, `t+2Δ`.
Channels are the three time slots. Samples are pooled over all 12 288 (ossicle, cell) units
and over a set of start times `t`.

Binarization: b = 2 at each channel's **own median** (primary: global median over the pooled
channel; secondary: per-unit median, reported as a robustness check). **Tied fraction
disclosed for every reading**; any reading with tied fraction > 0.01 is flagged
tie-contaminated and reported separately rather than quoted.

**Estimator:** `shareK(p) = H(pairwise-maxent(p)) − H(p)`, the maxent by iterative
proportional fitting to all pair marginals from uniform. Imported from
`array_cap_experiment.py`, which is gate-verified against `bench_detector.C3` to 1e-12 and
against exact parity (= ln 2) and exact independence (= 0).

**Cap:** the machine-checked classical cap at k = 3 is `(k−2)·ln 2 = ln 2 = 0.693147`
(`CIRISOntology/Core/ShareK.lean`, `shareK_le_of_pair_uniform`). The deviation-robust bound
`k·ln 2 − max_pair H(pair)` is computed alongside and any exceedance of either is reported
loudly as a pipeline defect, exactly as in the sibling prereg.

**Ceiling fraction** `CF = (share_obs − null_mean) / (k−2)·ln 2`, bias-corrected; raw
`share_obs / cap` reported alongside.

### Nulls and floors — and what is deliberately not used

- **Matched pairwise-maxent multinomial surrogate** at **every** grid point and **every** lag:
  draw T samples from the order-3-free maxent distribution carrying the observed pair
  marginals, recompute share. This is the estimator bias floor. 60 draws (30 for the
  formation curve, where 2048 separate share estimates are taken); mean ± sd;
  z = (share_obs − mean) / sd.
- **Shuffle floor**: independently permute each channel across samples; recompute share.
- **Excess is reported, never raw share.**
- **Independence-safe significance.** The pooled estimate reuses each unit at several start
  times, so its T overstates the independent sample count and its z is optimistic. The
  **shape** is taken from the pooled estimate (precision); the **significance** is quoted
  from a single-start estimate (T = 12 288, genuinely i.i.d. across units) at
  Δ ∈ {1, 8, 64, 256}. Both are reported.
- **IAAFT is NOT used and would not certify anything.** Stated plainly per the standing trap:
  a clip artifact survived IAAFT at z = 86 on 2026-07-24. Its survival is not evidence, so it
  is not run and its absence is not a gap.

---

## 3. MEASUREMENT 1 — LIFESPAN: how long a Logos pattern lives

Sweep Δ ∈ {1, 2, 3, 4, 6, 8, 11, 16, 23, 32, 45, 64, 91, 128, 181, 256} kernel iterations.
One trajectory per (seed, boundary): 2000 settle iterations, then N = 1024 recorded frames.
16 start times per Δ, spaced ≥ 8 iterations apart where the window allows. **R = 5
independent seeds**; the error bar on `excess(Δ)` is the across-seed sd / √5 — a real error
bar from independent realizations, not an estimator proxy.

### The two hypotheses, fitted and compared

Weighted least squares on `excess(Δ)` with weights `1/σ_Δ²`:

| | model | parameters |
|---|---|---|
| **E** | `excess(Δ) = A·exp(−Δ/τ) + c` | A, τ, c |
| **P** | `excess(Δ) = A·Δ^(−α) + c` | A, α, c |

Both have 3 parameters, so the AIC comparison reduces to a like-for-like χ² comparison.
`AICc = χ² + 2p + 2p(p+1)/(n−p−1)`; `ΔAIC = AICc_P − AICc_E` (positive favours exponential).
The two-parameter versions (`c = 0`) are fitted and reported alongside, but the plateau
versions are **primary** — because a constant clip artifact is exactly what `c` absorbs.

### Pre-registered meaning of every outcome — fixed before any number is seen

- **EXPONENTIAL WINS** (`ΔAIC ≥ 10`). Whole-only pattern in this substrate has a
  **characteristic lifespan**. τ is reported as that lifespan in kernel iterations. This is
  the shape the repository's rent clause predicts: `Core/Maintenance.lean` `unpaid_decays`
  makes an unmaintained entry decay geometrically, and the `e-upkeep` wager says the books
  are written in e. **Stated with the boundary the repository already enforces:
  `Core/Maintenance.lean` is a theorem about a MODEL, not about this lattice. An exponential
  here is a shape agreement between a physical substrate and the model's shape. It is
  evidence that the model's shape is not arbitrary; it is NOT a proof of the rent clause in
  the world and must never be laundered into one.**
- **POWER LAW WINS** (`ΔAIC ≤ −10`). Whole-only pattern in this substrate has **no
  characteristic lifespan** — the decay is scale-free, the signature of a critical system.
  α is reported. **This would mean the rent-clause bookkeeping is the wrong shape for this
  substrate**, and it is arguably the more interesting outcome. It is pre-committed here that
  a power-law result is reported as the headline, in the abstract of the results file, with no
  softening and no relegation to a caveat.
- **INDETERMINATE** (`|ΔAIC| < 10`). Both fits reported, no winner declared, and the reason
  (lever arm, noise, or genuine crossover) stated.
- **DEGENERATE.** `excess(Δ)` is at or below the floor for all Δ ≥ 1, or is non-monotone and
  noise-dominated. Then **no lifespan is measurable and no τ is quoted** — reported as
  DEGENERATE, not as "short τ".

### Shape stability across boundaries — the discriminator applied

| verdict | criterion |
|---|---|
| **STABLE** | same model family selected under CLIP and FOLD, **and** the shape parameter agrees within `\|θ_clip − θ_fold\| ≤ 0.20·max(\|θ\|)` |
| **ARTIFACT** | the selected model family flips, **or** the shape parameter differs by more than a factor of two |
| **MARGINAL** | anything in between — reported, not quoted |
| **TRIVIAL** | clamp-binding rate is exactly zero under CLIP — agreement carries no information |

**Only STABLE (and non-TRIVIAL) shapes are quoted as measurements of the substrate.**
Level differences between CLIP and FOLD are reported but do not by themselves trigger an
ARTIFACT verdict for a shape claim; that is the whole point of the differential design.

---

## 4. MEASUREMENT 2 — FORMATION: how a habit congeals

Fresh randomized initial states (`cp.random.uniform(0.2, 0.8)`, the runtime's own
initializer), **no settle**. Record N = 256 frames from t = 0. Fixed small lag: **Δ_f = 1**
primary, **Δ_f = 4** secondary. At each elapsed time t, share is estimated on frames
`(t, t+Δ_f, t+2Δ_f)` pooled over all 12 288 units at that single start time — so T = 12 288,
genuinely i.i.d. across units, at every point of the build curve.

**R = 8 independent initializations**; the build curve is the across-init mean and the error
bar is the across-init sd / √8.

Binarization threshold: per-channel median computed on the **late** portion (last 25% of the
run) and held fixed at all t — so the threshold is a property of the attractor, not of the
transient. Secondary, reported as sensitivity: threshold recomputed within each t.

Reported: `excess(t) = share(t) − null_mean(t)`, the **build curve**. Characteristic
formation time by two routes, both reported:

- **model fit**: `excess(t) = E_∞·(1 − exp(−t/τ_form))`;
- **model-free**: `t_90` = the first t at which `excess(t) ≥ 0.9·E_∞`, with
  `E_∞` = mean excess over the last 25% of the run.

### Pre-registered meaning of every outcome

- **BUILDS** — excess rises from a value consistent with the floor to a plateau clearing the
  floor, monotone by Spearman over the first half. Report τ_form and t_90 as the formation
  time. This is the empirical face of habit formation on this substrate.
- **ALREADY THERE** — excess at t = 0 is already within 10 % of the plateau. No formation
  transient is observable at this lag; the pattern is instantaneous at the instrument's
  resolution. Reported as such, not as a fast build.
- **DECAYS** — excess **falls** from initialization to the plateau. The randomized initial
  condition then carries MORE order-3 than the attractor does. This is a real result and is
  reported as a decay, explicitly **not** dressed up as formation.
- **NONE** — the plateau is consistent with the floor; there is nothing to time.

### What this is NOT — pre-committed

If it shows a clean onset, this is the first quantitative handle this project has on
**precedence accumulation in the Smolin sense — as a CLASSICAL ANALOGUE ONLY**. It does
**not** test Smolin precedence in quantum mechanics; this is a deterministic-plus-noise
classical lattice and carries no quantum content whatsoever. Any sentence in the results
that mentions precedence carries this label in the same sentence.

---

## 5. MEASUREMENT 3 — TAXONOMY: the behaviour map

Hold `r_base = 3.70`. Sweep the coupling dial and the noise:

- **κ ∈ {0.00, 0.02, 0.05, 0.10, 0.20, 0.35, 0.50}** (0.05 is the validated bench point);
- **σ ∈ {0, 1e-4, 1e-3, 1e-2, 1e-1}** (1e-3 is the validated SR operating point, included as
  instructed);
- both boundaries (CLIP, FOLD).

At each grid point: settle 2000 iterations, N = 512 frames, reduced lag sweep
Δ ∈ {1, 2, 4, 8, 16, 32, 64, 96, 128, 192}, 8 start times, full surrogate + shuffle floors.
Report the pair **(ceiling fraction at Δ = 1, lifespan τ from the Measurement-1 fit
procedure)** as a 2-D ASCII map, one map per quantity per boundary.

Two grid points are **expected degeneracies**, named in advance so they cannot be retrofitted
as findings:

- **κ = 0** — the three oscillators are uncoupled, so b is an autonomous logistic map. Its
  temporal order-3 is then entirely intrinsic to the single map. This column is the baseline
  that isolates how much of the temporal share is coupling-dependent.
- **κ = 0, σ = 0** — b is a *deterministic* autonomous map, so `(b_t, b_{t+Δ}, b_{t+2Δ})` is
  supported on a curve and strong order-3 at small Δ is present **by construction**. Labelled
  the deterministic degenerate corner; quoted as a construction, never as a measurement.

### Corner classification — thresholds fixed before the run

`CF ≥ 0.10` is **high**; `τ ≥ 20` kernel iterations is **long**.

| corner | CF | τ | name |
|---|---|---|---|
| low / short | < 0.10 | < 20 | **memoryless-like** |
| high / short | ≥ 0.10 | < 20 | **chaotic churn** |
| low / long | < 0.10 | ≥ 20 | **frozen but empty** |
| high / long | ≥ 0.10 | ≥ 20 | **congealed habit** — pattern both strong and persistent |

Grid points whose lifespan fit is DEGENERATE are placed in no corner and reported as
unclassifiable. **Which corners the substrate actually reaches is the deliverable**; if every
point lands in one corner, that is the result and is reported as "the substrate reaches only
corner X", not massaged by re-choosing thresholds. The median-split classification is
reported *alongside* the absolute-threshold one for reference, clearly labelled as a
post-hoc relative view.

---

## 6. GATE — machinery and hardware self-test, BEFORE any measurement. FAIL ⇒ stop.

1. **Machinery.** `array_cap_experiment.gate()` in full: exact k = 3 parity → share = ln 2
   (saturating its cap exactly); exact independence → 0; exact k = 5 pair-uniform code state
   → 2 ln 2; IPF residual < 1e-12; `shareK(k=3)` ≡ `bench_detector.C3` to 1e-12; sampled
   parity fires and sampled independence floors through the full pipeline including the
   surrogate null.
2. **Kernel equivalence (new).** On the real device, σ = 0: 100 calls at `iterations = 1`
   reproduce 1 call at `iterations = 100` bit-identically, for both CLIP and FOLD builds.
3. **Instrumented-kernel fidelity (new).** The clamp-counter build must reproduce the
   *shipped* kernel's states bit-identically under CLIP with σ = 0 — i.e. the instrumentation
   does not perturb the dynamics.
4. **Fit-machinery self-test (new).** The exponential/power-law fitter recovers τ and α to
   within 5 % on synthetic curves generated with the measured noise level, and `ΔAIC`
   correctly selects the generating family on both.

Any FAIL stops the run. Nothing is measured on a failed gate.

---

## 7. WHAT IS EXPLICITLY NOT CLAIMED

1. **No discovery of order-3 / whole-only structure in the array.** Pre-committed in §0. The
   presence of share is expected, implementation-sensitive, and reported only as a magnitude.
2. **No world-claim from the rent clause.** `Core/Maintenance.lean` is a theorem about a
   model. A matching shape on this lattice is a shape agreement, not a proof of the rent
   clause in the world.
3. **No quantum content.** Measurement 2 is a classical analogue of precedence accumulation
   and nothing more.
4. **No IAAFT certification.** Not used; its survival certifies nothing.
5. **No absolute-level claim about the substrate.** Levels are artifact-contaminated by
   construction; only shapes that pass the STABLE/non-TRIVIAL discriminator are quoted.
6. **Nothing touches the Lean library, `Stance.lean`, or the audit.** No `lake`. Scratchpad
   only. Prereg committed before the run; results and script committed after. No push.

Primary seed 20260725. Lifespan replicated across seeds {20260725, 99, 7, 1337, 4242};
formation across 8 initializations; taxonomy at the primary seed with κ = 0.05 replicated at
seeds 99 and 7.
