# PRE-REGISTRATION ADDENDUM — mixture null, dose-vs-rate, and the filtering declaration

Addendum to `ARRAY_NEGENTROPY_PREREG.md` (frozen `9251b5b`). **Committed before
`array_negentropy_controls.py` existed and before either new control was run.** The main
sweep, cliff and clip-readout runs are already complete and committed (`15f7731`, `d9b8853`);
this addendum governs **two new controls** whose results may retract findings already reported,
and it is written so that they can.

Prompted by two team-lead messages carrying results from sibling runs: the ECA spike
adjudication (`9630d81`, correction `149d1bb`) and the sky-pilot refuter pass (`e601aec`).

---

## 0. WHAT IS ALREADY DONE, AND IS NOT RE-LITIGATED HERE

Three of the five points raised are already discharged in the committed record and are listed
so the addendum's scope is unambiguous:

| point | status |
|---|---|
| the share is **not** negentropy | **already corrected** — `ARRAY_NEGENTROPY_RESULTS.md` opens with the correction; **gate G4 is the discriminator and passes** (lognormal reproduces the Gaussian reading bitwise, where Jones–Sibson negentropy reads 9.93 nats). The reported quantity is and was the *projection* onto the one direction pairs cannot see — closed form (B), machine-checked against a basis-free projection in G0 to 3.0e-14 |
| the static-nonlinearity exposure lands on the **moment** route | **already measured, on this substrate** — `array_negentropy_cliptest.py` / §9: median split exactly invariant (1.000 at every level, both boundaries), this moment route ×1.21 at a 1 % tie block and ×2.0 at 10 %. The dual-route design was already run (§6) and the routes' disagreement already reported as a diagnostic (§7) |
| the clamp sits **inside** the recurrence, so fold-vs-clip stays mandatory | **already honoured** — every one of the 3 072 sweep readings was taken under both boundaries |

**New and binding: §1, §2, §3 below.**

---

## 1. THE MIXTURE NULL (Kahle, Olbrich, Jost & Ay, PRE 79:026201 (2009))

**The threat.** A convex combination of an ordered and a disordered distribution manufactures
higher-order structure **with no dynamics at all**. On the sibling's ECA data this null beat
the "1886× noise-creates-structure" headline by 1.9×: a no-dynamics straight line outperformed
the real sweep.

**This bears directly on the result this run has already reported.** `ARRAY_NEGENTROPY_RESULTS.md`
§5 reports P5 as SURVIVED — an interior maximum in σ at 0.03, reproducing the ECA interior
noise optimum on a continuous substrate. A noise sweep from σ = 0 to σ = 0.1 **is** a sweep
from ordered to disordered, so it is precisely the case the mixture null attacks.

**Protocol.** For each interior peak reported in a swept parameter `x` with endpoints `x_A`
(ordered) and `x_B` (disordered):

1. Collect the triple samples at `x_A` and at `x_B`, **as whole triples**, so each endpoint's
   own within-triple dependence is preserved intact.
2. For λ ∈ {0, 0.05, …, 1}, build the mixture `(1−λ)p_A + λp_B` empirically: draw each sample
   slot's triple from pool A with probability `1−λ` and from pool B with probability `λ`.
3. Push the mixture through the **identical** pipeline — same rank-Gaussianization, same moment
   tensor, same bridge, same sample size, same number of frames — so estimator noise is matched.
4. Report `max_λ ŝ₃(mixture)` against the dynamical peak `max_x ŝ₃(dynamics)`.

**The bar, fixed now: the dynamical peak must EXCEED the straight line's peak to count as a
property of the dynamics.** Ratio `R = max_x ŝ₃(dyn) / max_λ ŝ₃(mix)`.

| outcome | meaning |
|---|---|
| `R > 1` | the interior optimum is a property of the dynamics; P5 survives, now against a harder null |
| `R ≤ 1` | **the noise optimum is a mixture artifact.** P5's "SURVIVED" verdict is **retracted**, the ECA-replication claim comes down with it, and the retraction is reported as plainly as the survival was |

Applied to: the σ peak (endpoints σ = 0 and σ = 0.1) at κ = 0, 0.02, 0.05; and the κ peaks
(endpoints κ = 0 and κ = 0.60) for `T3d1`, `S3` and `C3`.

**Honest note on what the mixture null can and cannot settle.** A mixture of the sweep's own
endpoints is a null for "an interior peak requires dynamics at the interior point". It is not
a null for the *location* of the peak, and `R > 1` does not make the peak interesting — only
not-explained-by-mixing.

---

## 2. DOSE VS RATE

**The threat.** If a peak's *location* in the swept parameter scales as `1/T` with the run
length — equivalently, sits at fixed total dose, `parameter × T = const` — it marks *when the
run first stops being deterministic or settled*, not an intrinsic operating point. On the ECA
data, rules 25/46 failed exactly this: peak at a fixed dose of 3–7 expected flips, location
halving as `T` doubled.

**The analogue here, and why it is the settle length.** This run drives the kernel at
`iterations = 1` and injects noise before every iteration, then observes at lag Δ within a
trajectory that has been run for `settle` iterations. The stationary distribution of the noisy
map depends on σ but **not** on `settle` — *once settled*. So the dose test is exactly whether
that is true: if σ* moves with `settle`, the array was never settled and the "interior
optimum" is a transient dose effect rather than a property of the stationary dynamics.

**Protocol.** Re-run the σ sweep at `settle ∈ {250, 500, 1000, 2000, 4000}`, at κ = 0.02 and
κ = 0.05, both boundaries, everything else identical. Report σ*(settle) and the peak height.

**Two bars, both fixed now:**

- **Location.** Fit `log σ* = a − b·log(settle)`. `b ≈ 1` (within ±0.3) is the fixed-dose
  signature ⇒ **the peak is a dose artifact and P5 is retracted.** `b ≈ 0` (|b| < 0.3) means
  the location is intrinsic.
- **Height convergence.** The peak height must change by **< 10 % on doubling settle from 2000
  to 4000**. The bar is stated here so it can be missed; the sibling ECA memo claimed this bar
  and was still +18 %, and if this run misses it the miss is reported with its number rather
  than the bar being widened.

---

## 3. THE FILTERING DECLARATION

**The threat.** Smoothing or averaging applied *after* a pointwise nonlinearity converts
pointwise structure into genuine multi-cell share — 66σ in the sky-pilot (smooth-then-transform:
exact zero; transform-then-smooth: 66σ).

**Declaration, to be verified in code and reported either way:** this pipeline is believed to
contain **zero** filtering, smoothing, downsampling or averaging steps between the dynamics and
the triple. Each channel is a **raw state value at one (ossicle, cell, time)** — `oss.states[:,
j, :].ravel()`. The only operations applied are (i) per-channel rank-Gaussianization, a
pointwise per-channel map that averages nothing across cells or time, and (ii) the estimator's
expectation over the replica ensemble, which is an average **of** the statistic and not a
filter **of** the field entering the triple.

Notably **not** used: the kernel's own `phase` output, which *is* a cell-average and which
`ARRAY_CAP_RESULTS.md` showed transduces coupling through the clamp; and
`array_cap_experiment.reading_phase_groups`, which group-averages ossicles.

**If the code audit contradicts this declaration, the offending step is named and its scale is
swept as a control.** If it confirms it, the 66σ filter channel is **structurally absent** here
— which is a stronger statement than "checked and found clean", and is the only case in which
no filter-scale sweep is owed.

---

## 4. PRIOR ART — Schneidman, Still, Berry & Bialek (2003)

**The founding paper of this measure already swept noise and already found order-3 creation, at
0.077 bits (their Fig. 2).** Any "noise-enhanced whole-only structure" finding must engage that
as prior art rather than as a neighbour. The engagement is owed in the results document
regardless of how §1 and §2 come out, and the comparison to be made explicit is the
**magnitude**: this run's noise-enhanced tier-A peaks are 5.710e-2 and 4.897e-2 nats, i.e.
**0.0824 and 0.0707 bits**. Whatever §1 and §2 decide, **the magnitude is not new** and must
not be presented as if it were.

---

## 5. WHAT THIS ADDENDUM CANNOT DO

1. It cannot rescue P5. If either control fires, P5's SURVIVED verdict is retracted and the
   dead claim stays in the record, marked dead (house rule 7).
2. It touches nothing else. The headline (§VERDICT, the κ = 0.05 certified reading), the cliff
   correction (§6), the clip-readout refutation (§9) and the cap-compliance result do not
   depend on the σ axis and are unaffected by either outcome.
3. No stance change, no Lean, no `lake`, under any outcome.

---

*Addendum ends here. Nothing below this line existed when it was committed.*
