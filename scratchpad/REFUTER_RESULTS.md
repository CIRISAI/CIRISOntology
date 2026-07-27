# REFUTER RESULTS — the adversarial pass on the BOSS DR12 whole-only order-3 detection

Pre-registered in `REFUTER_PREREG.md` (`94894fc`), committed before a single attack ran, with
KILL / WOUND / CLEAR fixed in advance for each attack. The attack code was committed before its
numbers were read (`c09ba2c`).

**Everything below is post-unblind and therefore post-hoc, and is labelled so.** No
pre-registered outcome is re-scored here. The pre-registered outcomes are attacked.

**Scope limits, stated up front rather than buried.** This box is shared and for most of the
session another process held 12 of the 32 cores. Consequently: the A9/A1 null family ran to
**four draws on SGC and two on NGC**, so the null-realisation noise on each row is real; the
A2 weight test completed on **SGC only, not NGC** (and one of its five schemes turned out to be
mis-specified by me — struck, with the reason, in §A2); and the mock-side
closure is **three mocks**, enough to establish that the correction is common-mode and nowhere
near enough to re-measure σ. Every table below says which. Nothing here is quoted to more
precision than its ensemble supports.

---

## SUMMARY VERDICT: **DETECTION WOUNDED**

The detection is not killed. Under every correction I can defend, both caps keep two or more `b`
rungs above 5 σ at `R = 10`, and NGC keeps both rungs at the primary scale `R = 15` — so outcome
(a)'s pre-registered criterion still has a ladder to stand on. But **not one of the reported
significances survives**, the headline's "lower bound" framing is falsified in sign, and a
pre-registered VOID gate turns out never to have been run.

**The caveats any stance treatment must carry:**

1. **The target is not robust to the null's construction.** A null built the way Amendment 5's
   own text describes — modulation carrying the clustering, Poisson supplying the shot noise —
   cuts the target by **30–52 %**. Every quoted significance falls: **NGC 9.4 σ → 6.0 σ,
   13.5 σ → 9.7 σ, 50.8 σ → 29.8 σ; SGC 22.1 σ → 10.9 σ, 29.0 σ → 16.5 σ.** The reported numbers
   are construction-dependent at the tens-of-percent level.
2. **The headline "the detection is a LOWER bound" is falsified in sign.** Amendment 5 §A5.3
   argued that heavy clipping inflates the valve floor, hence deflates the target. A null that
   clips **3.5 %** of cells instead of **37 %** produces a floor **24–50 % larger**, not smaller.
   The correction runs downward, not upward.
3. **The null carries no non-Poisson stochasticity, and the data's own weights alone are
   13–15 % super-Poisson** (`κ = ⟨w²⟩/⟨w⟩ = 1.129` NGC, `1.152` SGC, read straight off the
   catalogue). The dispersion that takes the corrected rows below 5 σ is `ε_crit = 0.63–0.85`,
   against a literature-defensible galaxy stochasticity reaching `ε ≈ 0.5`. **The margin is a
   factor of 1.3–1.7, not orders of magnitude.**
4. **The primary scale survives on NGC only narrowly** — `b = 4` falls from 9.4 σ to **6.0 σ**,
   and to 4.6 σ if `ε = 1`. On SGC the primary scale falls from 3.8 σ to 2.3 σ, though SGC at
   `R = 15` was already a single-rung row that could not carry (a).
5. **The reading is sensitive to fibre-collision weighting at 2.5–2.9 σ**, and the pre-registered
   §7.5 weight-variation gate — a **VOID** condition — **was never run by the campaign** and
   cannot be discharged with this catalogue's columns. Imaging systematics, the channel §7.5
   names first, are clean at ≤ 0.62 σ.
6. **A cap asymmetry the mocks do not predict**: NGC exceeds SGC on all four folded rows by
   5–9 %, worst 2.15 σ, where Patchy predicts the two caps equal to 0.2 %.
7. **Outcome (a)'s "configuration shape" clause was scored on folded rows only.** All twelve
   non-folded `R = 10` rows sit *below* prediction (0.71–0.94). Disclosed in §4 of the results,
   never scored against the clause it belongs to.
8. **`SKY_REALDATA_RESULTS.md` §4 carries pre-Amendment-5 numbers, unlabelled.**
9. **The pointwise channel is not bounded by the current null.** A deliberately over-generous
   null eats the entire target.

**What survives, and it is not nothing.** The *consistency* between the data and the Patchy
prediction survives every correction, because the correction is **common-mode**: the mock-side
target falls by 0.56–0.61 where the data-side falls by 0.53–0.65. And the estimator itself is
verified — an independent reimplementation agrees with the pipeline to `9e-13` relative.

---

## SCORECARD

| attack | verdict | the number |
|---|---|---|
| **A9** null not two-point matched (refuter-originated) | **WOUND** | target × 0.48–0.69; σ(null)/σ(data) = 0.76–0.84 |
| **A1** non-Poisson stochasticity | **WOUND** | `ε_crit = 0.63–0.85` vs defensible `ε ≈ 0.5`; measured `κ−1 = 0.13–0.15` |
| **A2** systematic weights | **CLEAR** on imaging, **WOUND** on fibre collisions | ≤0.62 σ vs **2.5–2.9 σ**; the §7.5 VOID gate was never run |
| **A3** cap consistency | **WOUND** | worst folded cap difference 2.15 σ; 4/4 rows same sign |
| **A4** 16-mock ensemble | **CLEAR** | prediction shift < 1 %; no row crosses 5 σ |
| **A5** independent recomputation | **CLEAR** (see caveat) | `9.3e-13`, `4.6e-11`, `2.5e-6`, `5.4e-6` relative |
| **A6** surrogate skewness deficit | **WOUND** | over-generous null drives target to −0.18 to −1.29 × |
| **A7** convergent art | **CLEAR** | no prior BOSS-data measurement of this quantity found |
| **A8** look-elsewhere / exclusion hygiene | **CLEAR** on thresholds, **WOUND** on scoring | frozen prediction git-verified untouched; shape clause unscored |

---

## A9 — THE NULL IS NOT TWO-POINT MATCHED *(refuter-originated; the largest single effect)*

Amendment 3 §A3.2 rests the surrogate's entire well-posedness on one property: "Phase
randomisation preserves `P(k)` exactly … the two-point function is matched **by construction**,
with no tuned parameter that can be got wrong." That is true of `N1`. **Amendment 5 replaced the
null with `N2`, which does not have it**, and the campaign's own recorded diagnostics say so:

| cap | R | σ(data) | σ(N1) | σ(N2) | σ(N2)/σ(data) |
|---|---|---|---|---|---|
| NGC | 15 | 0.4704 | 0.4660 | **0.3615** | **0.769** |
| NGC | 10 | 0.7090 | 0.7063 | **0.5927** | **0.836** |
| SGC | 15 | 0.4737 | 0.4693 | **0.3606** | **0.761** |
| SGC | 10 | 0.7066 | 0.7063 | **0.5867** | **0.830** |

`N2` is built as `λ = α·n̄_ran·max(1 + δ_PR, 0)`, and `δ_PR` is a phase-randomised copy of the
data's **cell-level** `δ`, whose rms is ≈ 3 (0.058 galaxies per 6 Mpc/h cell). So the modulation
is 96 % phase-randomised *shot noise*, 37 % of which the positivity clip then destroys — and a
fresh full-amplitude Poisson draw is added on top of a field that already carried the survey's
shot-noise power.

### A9b — my own mechanism claim, REFUTED by my own control

I pre-registered a specific mechanism: the clipped modulation has mean **1.775**, so the null is
drawn at 1.78× the data's number density and its shot noise is correspondingly gentler.
`refuter_a9r.py` tests exactly that by changing **one line** — divide the modulation by its own
mean — with the same seeds, same phases, same clipping, everything else identical.

| SGC, folded | target (pipeline) | target (renormalised) | ratio |
|---|---|---|---|
| R=15 b=4 | `2.797e-04` | `3.257e-04` | **1.164** |
| R=10 b=4 | `8.505e-04` | `7.331e-04` | 0.862 |
| R=10 b=6 | `1.731e-03` | `1.514e-03` | 0.875 |
| R=10 b=8 | `2.587e-03` | `2.283e-03` | 0.882 |

**The density accounts for 12–14 % at `R = 10` and moves `R = 15` the wrong way. My A9b
attribution was wrong, and my pre-registration said I would say so if it was.** The mean-1.775
modulation is a real defect of the construction, but it is not what drives the effect.

### A9 constructive — what does drive it

`refuter_nulls.py` builds `N2m`: the modulation carries the **clustering only** (the shot-noise
power is removed in Fourier before the phases are randomised, so Poisson supplies it once rather
than twice), which drops the clipped fraction from 37 % to 3.5 %, renormalised to the data's own
number density. `N2mw` additionally draws counts with the data's own **weighted** shot noise
(`κ = ⟨w²⟩/⟨w⟩`).

| SGC, folded | target (pipeline) | `N2m` | ratio | `N2mw` | ratio | det (pipeline → `N2mw`) |
|---|---|---|---|---|---|---|
| R=15 b=4 | `2.873e-04` | `1.859e-04` | 0.647 | `1.877e-04` | 0.653 | 3.5 → **2.3** |
| R=10 b=4 | `8.614e-04` | `4.552e-04` | 0.528 | `4.156e-04` | 0.482 | 22.7 → **10.9** |
| R=10 b=6 | `1.753e-03` | `1.007e-03` | 0.574 | `9.348e-04` | 0.533 | 26.5 → **14.1** |
| R=10 b=8 | `2.602e-03` | `1.524e-03` | 0.586 | `1.460e-03` | 0.561 | 29.4 → **16.5** |

**NGC** (the cap outcome (a) rests on at the primary scale; two draws).

First, the baseline check that makes the rest readable: my reproduction of the pipeline's own
null, from its recorded seeds, returns targets within **0.2–3.8 %** of the campaign's recorded
values on all five rows (ratios 0.981, 0.962, 0.994, 0.998, 1.003). **I am reproducing their
number before I move it.**

| NGC, folded | recorded det | `N2m` ratio → det | `N2mw` ratio → det | at `ε = 0.5` | at `ε = 1` |
|---|---|---|---|---|---|
| **R=15 b=4** | **9.4** | 0.662 → 6.4 | 0.621 → **6.0** | 5.6 | **4.6** |
| **R=15 b=6** | **13.5** | 0.706 → 9.9 | 0.694 → **9.7** | 8.5 | 7.4 |
| R=10 b=4 | 40.5 | 0.550 → 22.4 | 0.513 → 20.9 | 12.7 | **1.1** |
| R=10 b=6 | 46.8 | 0.598 → 28.0 | 0.561 → 26.3 | 17.5 | 5.0 |
| R=10 b=8 | 50.8 | 0.623 → 31.6 | 0.588 → 29.8 | 20.7 | 8.4 |

**NGC's primary-scale rungs survive the correction, but narrowly**: `9.4 σ → 6.0 σ` and
`13.5 σ → 9.7 σ`, both still above 5, so the two-rung clause at `R = 15` holds. At `ε = 1` the
`b = 4` rung falls to 4.6 σ and that clause fails.

(Detections use the campaign's own σ. Three mocks are not enough to re-measure σ under the
corrected null — the n=3 ratios scatter over 0.10–1.17 — so I do not claim a corrected σ, and I
say so rather than quoting one.)

**This is the falsification of the "lower bound" claim.** §A5.3 pre-stated the direction:
heavy clipping manufactures skewness, inflates the floor, and therefore *deflates* the target,
"hence the target a **lower** bound." Reducing the clipping by a factor of ten produced a floor
**24–50 % larger**. The sign of the argument is wrong.

### A9a — the pedestal deficit, measured directly

The binmint pedestal (fine `b' = 2b` pair-maxent merged to `b`) is the part of `I_C⁽³⁾` that is
a pure function of pair structure. Measured on the data field and on the pipeline's own null:

| SGC row | pedestal(data) | pedestal(N2) | deficit | as % of target |
|---|---|---|---|---|
| R=15 b=4 folded | `1.700e-04` | `1.358e-04` | `3.42e-05` | **11.9 %** |
| R=10 b=4 folded | `2.718e-04` | `1.657e-04` | `1.06e-04` | **12.3 %** |
| R=10 b=6 folded | `1.869e-04` | `1.404e-04` | `4.65e-05` | 2.7 % |

Two of three primary rows exceed my pre-registered 10 % materiality bar on this channel alone.
(The data's pedestal fraction, 27.4 % at R=15 b=4, reproduces the mock-measured 29.3 % of
Stage 4 — an independent check that my pedestal code is measuring the same thing.)

### Closure: the correction is COMMON-MODE

Run on three Patchy mocks, the same correction moves the **prediction** by nearly the same
factor as it moves the data:

| SGC, folded | mock target ratio (`N2m`/pipeline) | data target ratio |
|---|---|---|
| R=15 b=4 | 0.812 | 0.647 |
| R=10 b=4 | 0.558 | 0.528 |
| R=10 b=6 | 0.596 | 0.574 |
| R=10 b=8 | 0.610 | 0.586 |

So the corrected data-vs-prediction agreement is essentially preserved (`(data−mock)/σ` =
−1.91, −1.02, −1.54, −2.35 against the campaign's −0.62, −1.10, −1.43, −2.66). **The correction
attacks the detection-against-zero, not the consistency.** That distinction belongs in any
stance treatment: "the data's higher-order structure matches Patchy's" survives; "the excess
above all floors is 9.4–50.8 σ and is a lower bound" does not.

**Verdict: WOUND.** Both pre-registered wound conditions fire — `Δpedestal ≥ 10 %` of target on
a primary row, and `target_m < 0.9 × target` on every primary row.

---

## A1 — NON-POISSON STOCHASTICITY

**The part that needs no modelling.** The pipeline's null draws *unweighted* Poisson counts at
the mean of the data's *weighted* counts. Weighted counts are super-Poisson by exactly
`κ = ⟨w²⟩/⟨w⟩`, read straight off the catalogue for `w = SYSTOT·(CP + NOZ − 1)`:

| cap | `⟨w⟩` | `⟨w²⟩` | `κ` | excess the null does not carry |
|---|---|---|---|---|
| NGC | 1.0553 | 1.1916 | **1.1291** | **12.9 %** |
| SGC | 1.0586 | 1.2189 | **1.1515** | **15.2 %** |

**Grounding for the rest.** MultiDark-Patchy itself assigns tracers by sampling a **negative
binomial** to model deviation from Poissonity (Kitaura et al. 2014/2015/2016), so the mocks
carry super-Poisson stochasticity the null does not. HOD-based studies of galaxy counts-in-cells
report shot noise spanning roughly **80 %–133 %** of the Poisson variance (halo exclusion gives
sub-Poisson, satellite multiplicity super-Poisson; Baldauf, Seljak, Smith, Hamaus & Desjacques,
*Halo stochasticity from exclusion and nonlinear clustering*, PRD 88, 083507). Combining the
measured weight factor with that range puts a defensible total at `ε ≲ 0.5`, which is the outer
edge I pre-registered.

**Measured, on the A9-corrected base (SGC, folded, detection against the campaign's σ):**

| row | ε=0 | 0.1 | 0.25 | 0.5 | 1.0 | 2.0 | **ε_crit (5 σ)** |
|---|---|---|---|---|---|---|---|
| R=15 b=4 | 2.2 | 2.4 | 1.4 | 2.0 | 1.9 | −0.1 | **already < 5 σ** |
| R=10 b=4 | 12.0 | 11.4 | 10.4 | 7.0 | −0.5 | −14.0 | **0.63** |
| R=10 b=6 | 15.2 | 14.1 | 13.7 | 9.2 | 1.2 | −14.8 | **0.76** |
| R=10 b=8 | 17.2 | 16.2 | 15.3 | 11.0 | 2.3 | −14.0 | **0.85** |

`ε_crit` lands in `(0.5, 2]`. **Verdict: WOUND**, exactly as pre-registered for that band. The
kill does not fire — absurd dispersion is not needed, but the required dispersion does exceed
the defensible range, by a factor of only 1.3–1.7.

---

## A2 — SYSTEMATIC WEIGHTS: **THE PRE-REGISTERED TEST WAS NEVER RUN**

`SKY_REALDATA_PREREG.md` §7.5 is not advisory. It is a **VOID** condition:

> "Imaging systematics and completeness weights: **MARGINALISED**, with the analysis repeated
> under the published weight variants; a shift exceeding the statistical error between weight
> schemes **voids** the affected bin."

`sky_stage6.py` applies exactly one scheme, `w = WEIGHT_SYSTOT × (WEIGHT_CP + WEIGHT_NOZ − 1)`,
and no weight-variant rerun appears anywhere in the record — not in the results, not in the gate
register, not in the withdrawal ledger. **The gate register in `SKY_REALDATA_RESULTS.md` §5 is
headed "all passed" and does not list §7.5 at all.**

This matters more than a missing row, because the Amendment-5 null is built by phase-randomising
and Poisson-resampling **the data's own field**, so it carries **neither fibre collisions nor
imaging systematics**. Those are correlated, multi-site channels; `Core/Creation.lean` covers
only per-cell maps and the pre-registration says so in §1.3. Anything they imprint on the order-3
sector lands inside `target` with nothing subtracting it.

**I ran it, on SGC** (`refuter_a2.py`, paired null seeds so the phase realisation largely cancels
between schemes; all five variants completed, NGC did not complete on this machine):

| scheme | R=15 b=4 | R=10 b=4 | R=10 b=6 | R=10 b=8 |
|---|---|---|---|---|
| **standard** `SYSTOT·(CP+NOZ−1)` | — | — | — | — |
| **no SYSTOT** `CP+NOZ−1` | +0.49 σ | −0.62 σ | −0.16 σ | −0.10 σ |
| **SYSTOT only** | +0.61 σ | **−2.94 σ** | **−2.80 σ** | **−2.47 σ** |
| **no weights at all** | +0.58 σ | **−2.58 σ** | **−2.82 σ** | **−2.54 σ** |
| ~~standard × FKP~~ | *(−8.1, −6.8, −5.8 σ — **invalid, see below**)* | | | |

**The FKP row is mine and it is wrong; I am striking it rather than banking it.** FKP weights
must be applied to the galaxies **and the randoms**, and `sky_stage6.DataGeometry` gives the
randoms `w = 1`. Applying a redshift-dependent weight to one side only puts a spurious radial
gradient into `δ = (n_g − α n_r)/(α n_r)` — visible directly as the field's rms moving from
0.4737 to 0.4418. The −5.8 to −8.1 σ shifts are that artifact, not a systematics test, and no
weight-variant conclusion may be drawn from them.

The decomposition is clean and it is not the channel §7.5 names first:

* **Imaging systematics (`WEIGHT_SYSTOT`) are harmless here** — dropping them moves the target by
  at most **0.62 σ**. That channel is **CLEAR**.
* **The fibre-collision / redshift-failure weight (`CP + NOZ − 1`) is where the sensitivity
  lives** — dropping it moves the target by **2.5–2.9 σ** on all three `R = 10` primary rows, in
  the same direction every time. `SYSTOT only` and `no weights` agree, which is what pins the
  attribution.

**How to score it, said plainly rather than picked afterwards.** My pre-registration listed
`w = 1` as a variant and said a shift exceeding the row's σ is "a KILL of that bin". By the
letter, the SGC `R = 10` bins are killed. **I do not endorse that reading and I am saying so
rather than quietly keeping it**: dropping the fibre-collision upweighting is not a *published
alternative scheme*, it is a known-wrong analysis that deletes a correction for galaxies that
were never observed, and a shift when you delete a necessary correction is expected. What is
genuinely established is:

> **The reading is sensitive to fibre-collision treatment at the 2.5–2.9 σ level, and the DR12
> combined catalogue does not carry an alternative fibre-collision scheme (the published
> alternatives are the PIP / angular-upweighting corrections, which are not columns in this
> file). The pre-registered §7.5 VOID gate therefore cannot be discharged with the data at
> hand.**

**Verdict: the imaging-systematics channel is CLEAR (≤ 0.62 σ); the fibre-collision channel is a
WOUND (2.5–2.9 σ) that the pre-registered test cannot close.** And the gate itself was never run
by the campaign: `SKY_REALDATA_RESULTS.md` §5's gate register is headed "all passed" and does not
list §7.5 at all.

---

## A3 — CAP CONSISTENCY

Gravity is isotropic and Patchy predicts the two caps equal to 0.6–1.8 %. The data does not obey.

| folded row | NGC | SGC | NGC/SGC | mocks predict | `z` |
|---|---|---|---|---|---|
| R=15 b=4 | `3.449e-04` | `3.177e-04` | 1.086 | 0.970 | +0.30 |
| R=10 b=4 | `8.801e-04` | `8.398e-04` | 1.048 | 1.007 | +0.92 |
| R=10 b=6 | `1.850e-03` | `1.726e-03` | 1.072 | 1.002 | +1.61 |
| R=10 b=8 | `2.791e-03` | `2.568e-03` | 1.087 | 0.998 | **+2.15** |

Worst folded difference **2.15 σ**, and the sign is the same on 4 of 4 rows (the rows are
strongly correlated — same catalogue, overlapping triples — so I do not combine them into a
joint p-value and no such number should be quoted). The pattern also shows up as SGC reading
systematically low against its own prediction on every folded row (ratios 0.86–0.95) where NGC
reads 0.96–1.02. Inflating both errors by the 18 % uncertainty on a 16-mock σ gives 1.82;
deflating gives 2.53.

**Verdict: WOUND** (pre-registered 2–3 σ band). Not a kill, but a cap-dependent amplitude is a
systematics signature and it is not in the results document.

---

## A4 — THE 16-MOCK ENSEMBLE

The first 16 mocks used for σ and the recomputed prediction are **bit-identical** to the first 16
of the 128-realisation surrogate suite (`max |ΔI(mock)| = 0` on every primary row) — so the two
runs can be compared directly. They are representative: `E[I(mock) − I(N1)]` shifts by at most
**0.60 SEM₁₆** between the 16-mock and 128-mock means.

Reconstructing the prediction from all 128 (`mean₁₂₈[I(mock) − I(N1)] − mean₁₆[valve]`, with the
valve's covariance propagated):

| row | pred₁₆ | pred₁₂₈ | det₁₆ → det₁₂₈ | consist₁₆ → consist₁₂₈ |
|---|---|---|---|---|
| NGC 15/4 | `3.584e-04` | `3.550e-04` | 9.4 → 11.4 | −0.37 → −0.33 |
| NGC 15/6 | `5.947e-04` | `5.892e-04` | 13.5 → 12.4 | +0.24 → +0.33 |
| NGC 10/8 | `2.797e-03` | `2.795e-03` | 50.8 → 46.6 | −0.11 → −0.06 |
| SGC 10/8 | `2.803e-03` | `2.796e-03` | 29.0 → 24.5 | −2.66 → **−2.18** |

The prediction moves by under 1 %; the worst consistency *improves*; detections move by −15 % to
+21 % and no row crosses 5 σ. **The consistency was not an artifact of a wide 16-mock error
bar. Verdict: CLEAR.**

The honest residual: σ from 16 draws is uncertain by ≈ 18 %, and detection significances inherit
that. A campaign quoting "9.4 σ" to two significant figures is quoting a number whose error bar
is ±1.7 σ from the ensemble size alone.

---

## A5 — INDEPENDENT RECOMPUTATION

Reimplemented from the gridded field with no estimator code shared: my own Fourier smoothing
(`numpy.fft`, float64), my own masked-smoothing division, my own quantile binning (both the
pipeline's subsample recipe, coded independently, and exact quantiles over every valid cell), my
own periodic shift by concatenation rather than `np.roll`, my own histogram, and a **dual /
L-BFGS** maximum-entropy solver instead of IPF.

Solver pre-validated against the pipeline's IPF on synthetic correlated triples before touching
the data: relative agreement `1.9e-14` (b=4), `7.4e-13` (b=6), `8.4e-12` (b=8).

**On the real SGC field, folded:**

| row | pipeline `I` | independent `I` | relative difference |
|---|---|---|---|
| R=10 b=4 | `1.37228651e-03` | `1.37228651e-03` | **9.3e-13** |
| R=10 b=6 | `2.57493681e-03` | `2.57493681e-03` | **4.6e-11** |
| R=10 b=8 | `3.66746972e-03` | `3.66746074e-03` | `2.5e-06` |
| R=15 b=4 | `6.21231423e-04` | `6.21234752e-04` | `5.4e-06` |

The pipeline's own null (`N2`, regenerated from its recorded seeds) reproduces at the same
level. The few-parts-per-million rows are traced: **the pipeline runs the estimator in float32**
and I ran it in float64, so a handful of cells land on the other side of a quantile edge. Using
exact quantiles over all valid cells instead of the 4 194 304-cell subsample moves `I` by at most
**0.27 %**, i.e. ~0.4 % of the target — the binning estimator's own noise, and negligible against
a 35–52 % effect.

**Verdict: CLEAR in substance.** Stated against the letter of my own pre-registration: I set
"≤1e-6 → CLEAR", and two of four rows land at 2.5e-6 and 5.4e-6, which my document calls WOUND.
I set that band without anticipating that the pipeline runs in float32. I am recording both the
band and my reading of it rather than quietly re-scoring: **the estimator is correct, and the
disagreement is float precision.**

---

## A6 — THE SURROGATE'S SKEWNESS DEFICIT

The null reads smoothed skewness `+0.387` against the data's `+1.10`. §A5.3 reads that deficit in
the conservative direction. The adversarial reading is that the null carries *less* pointwise
non-Gaussianity than the data, and whatever that mints through the coarse-graining channel lands
in the target.

**The defence, stated fairly first:** quantile binning is rank-based, so a pure one-point-law
difference is removed by construction (Sklar). The deficit can only bite through the copula.

**The worst case, built:** `N2L` replaces the positivity clip with a **lognormal** modulation
matched in variance to the clustering field, then samples with the data's weighted shot noise.
It is deliberately unfair — a per-cell monotone map does not commute with smoothing, so it
manufactures genuine order-3 structure, which is the exact defect that killed the Stage 3
control. It reaches smoothed skewness `+1.215` against the data's `+1.093`.

| SGC folded | target under `N2L` | ratio to pipeline |
|---|---|---|
| R=15 b=4 | `−3.71e-04` | −1.29 |
| R=10 b=4 | `−1.57e-04` | −0.18 |
| R=10 b=6 | `−4.12e-04` | −0.24 |
| R=10 b=8 | `−5.70e-04` | −0.22 |

The over-generous null eats the entire target and more. **Verdict: WOUND**, exactly as
pre-registered for that outcome — this is not a kill, because the probe is unfair by
construction, but it establishes that **the pointwise channel is not bounded above by the
current null**, and the campaign has no measurement that bounds it.

---

## A7 — CONVERGENT ART

No prior measurement of order-3 connected information, multi-information, or a maximum-entropy
gap **on BOSS or SDSS survey data** was found. The nearest prior art, and how it sits:

* **Qin, Yu & Zhang 2020** (arXiv:2006.06182), which the results document credits for "reported
  a non-Gaussian copula", measures **simulations**, not survey data. The campaign's disclaimer is
  if anything *over*-generous to the prior art.
* **Scherrer, Berlind, Mao & McBride 2010** poses the copula question — correctly credited.
* Beyond-two-point *information content* has been measured on BOSS by other statistics —
  marked power spectra and the wavelet scattering transform in the SimBIG programme, and the
  3-point function / bispectrum in the standard analyses — but not as a maxent gap.
* Connected information is Schneidman, Still, Berry & Bialek 2003 and Amari 2001 — correctly
  credited.

**Verdict: CLEAR.** The measurement is untouched and the novelty framing is already appropriately
modest; nothing needs re-scoping. Per the house lesson `convergent-art-pattern`, absence of a
hit here is weaker evidence than a hit would be, and the sweep was by name and by mathematical
object, not exhaustive.

---

## A8 — LOOK-ELSEWHERE AND EXCLUSION HYGIENE

**Threshold and exclusion hygiene: CLEAR.** Checked against git rather than against the prose:

* `sky_stage5_frozen_prediction.json` is **byte-identical** from `b06a3fe` (the freeze) to HEAD —
  `git diff b06a3fe HEAD` on that path is empty, and the file has exactly one commit in its
  history.
* The `NGC / R=15 / b=4 / squeezed` exclusion and the S2.3b ruling on which `b` ladder carries
  (a) were both committed **before** the unblind, with reasons, and both concern rows that do not
  carry outcome (a).
* Amendment 4 (withdrawing outcome (b)) is pre-unblind.
* Amendment 5 is **post-unblind**, and the document says so. It moved the result **against** the
  claim: the Stage-6 reading of 5.9–61.7 σ became 3.8–50.8 σ. A post-hoc re-specification that
  costs the author significance is the honest direction, and the ordering is disclosed.
* Look-elsewhere: 26 rows scored, 9 folded, 4 `(cap,R)` cells eligible to carry the two-rung
  clause. At 22–51 σ a trials factor of 9 is irrelevant; at 9.4 σ it costs about 0.3 σ. Not a
  live threat either way.

**Scoring completeness: WOUND.** Two findings:

1. **Outcome (a) requires consistency "in amplitude *and configuration shape*."** The verdict
   scored consistency on the nine folded rows and reported the non-folded behaviour in a separate
   section (§4) headed "reported and not claimed". Under the Amendment-5 scoring, **all twelve**
   non-folded `R = 10` rows sit below prediction (ratios 0.71–0.94) while **all five** non-folded
   `R = 15` rows sit above (1.02–1.82). That is a coherent, scale-dependent shape mismatch, and it
   is the clause it belongs to that was not scored. Amendment 4 withdrew outcome (b) — the
   *excess*-beyond-prediction branch — which does not cover a shape *deficit* bearing on (a).
2. **`SKY_REALDATA_RESULTS.md` §4 is stale.** Its table ("folded 0.94–1.03") and its three named
   3 σ rows (`−3.15`, `−3.17`, `−3.66`) are the **Stage-6 / frozen-prediction** numbers, carried
   verbatim from the pre-Amendment-5 version of the document (`git show 28fadbd`). Under the
   Amendment-5 scoring in `sky_final_verdict.json` those rows read **−1.61, −1.41, −2.12** and the
   folded ratios are **0.86–1.02**. Two incompatible scorings appear in one document with no
   label — the apples-to-oranges error that `sky_stage7_mocks.py`'s own docstring says "this
   campaign keeps catching."

---

## FILES

`REFUTER_PREREG.md` (pre-registration, `94894fc`); attack code `refuter_nulls.py`,
`refuter_nulls_fast.py`, `refuter_a9r.py`, `refuter_a2.py`, `refuter_a5.py`, `refuter_a34.py`,
`refuter_analyze.py` (committed at `c09ba2c`, before their numbers were read); outputs
`refuter_nulls_SGC.json`, `refuter_fast_NGC.json`, `refuter_a9r_SGC.json`,
`refuter_a2_SGC.json`, `refuter_a5_SGC.json`, `refuter_mock_SGC.json`, `refuter_a34.json`,
`refuter_analyze.json`.  The NGC null-family and NGC weight-variant runs did not complete on
this machine and no file is claimed for them.

**No stance recommendation is made here.** `wild-share` is not mine to move. The verdict goes to
Eric.
