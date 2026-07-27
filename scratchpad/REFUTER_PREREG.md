# REFUTER PRE-REGISTRATION — the adversarial pass on the BOSS DR12 whole-only order-3 detection

Written and committed **before any refutation computation is run.** My brief is to kill the
result if it can be killed. Every attack below states, in advance, what outcome counts as a
KILL, a WOUND, or a CLEAR, so that no result of mine can be re-scored after I see it.

**What I have already read** (this is the record under attack, and reading it is the job):
`SKY_REALDATA_PREREG.md`, Amendments 1–5, `SKY_REALDATA_STAGE1/STAGE2/PREUNBLIND.md`,
`SKY_REALDATA_RESULTS.md`, and the pipeline sources `sky_realdata.py`, `sky_stage{2,3,4,6,7}.py`,
`sky_surrogate.py`, `sky_stage7_mocks.py`, `sky_final_verdict.py`, plus the JSON outputs
`sky_final_verdict.json`, `sky_stage4_{NGC,SGC}.json`, `sky_stage7_valve.json`,
`sky_stage5_frozen_prediction.json`.

**Disclosure that matters for attack A9.** Before writing this document I read the `sigma` and
`skew` diagnostics that are *already recorded* in `sky_stage7_valve.json`, and they are what
prompted A9. They are part of the record under attack, not a result of mine. They are:

| cap | R | σ(data) | σ(N1) | σ(N2) | σ(N2)/σ(data) | skew(data) | skew(N2) | clipped |
|---|---|---|---|---|---|---|---|---|
| NGC | 15 | 0.4704 | 0.4660 | **0.3615** | **0.769** | +1.104 | +0.387 | 0.370 |
| NGC | 10 | 0.7090 | 0.7063 | **0.5927** | **0.836** | +1.635 | +0.617 | 0.370 |
| SGC | 15 | 0.4737 | 0.4693 | **0.3606** | **0.761** | +1.093 | +0.386 | 0.369 |
| SGC | 10 | 0.7066 | 0.7063 | **0.5867** | **0.830** | +1.610 | +0.610 | 0.369 |

---

## 0. WHAT COUNTS AS KILLING IT

The verdict under attack is **outcome (a)**: `target = I(data) − I(N2)` at ≥5 σ, folded, at two
or more `b` passing G9, consistent with the recomputed prediction. The pre-registered text is
"at `R = 10` **and/or** 15", and the S2.3b ruling makes four `(cap, R)` cells eligible to carry
the two-rung clause: NGC R=15 (`b=4,6`), NGC R=10 (`b=4,6,8`), SGC R=10 (`b=4,6,8`); SGC R=15
is single-rung and cannot carry (a) alone.

* **KILL** = every one of those cells loses its two-rung ≥5 σ status under a correction I can
  defend; **or** an independent recomputation (A5) disagrees with the pipeline beyond estimator
  tolerance; **or** a pre-registered gate is shown to have been mis-scored in a way that flips a
  verdict.
* **WOUND** = the ≥5 σ rows survive, but I demonstrate a named bias worth **≥10 % of the
  target** on a primary row in the direction that *inflates* the target, **or** I falsify a
  specific claim the results document makes (e.g. "the detection is a lower bound").
* **CLEAR** = the attack's demonstrated effect is **< 10 % of the target** on primary rows and
  changes no verdict. I quote the margin.

**Stated in advance so it cannot be spun later:** the `R = 10` rows sit at 22–51 σ. Nothing
short of a structural error (A5) or a floor increase of order 80–95 % can kill them. **I expect
the most likely honest verdicts are WOUND or CLEAR, not KILL, and I am registering that
expectation now so that a WOUND is not read as a failed attack and a CLEAR is not read as a
whitewash.** A refuter who only reports kills is not a refuter.

Everything I run is **post-unblind and therefore post-hoc**, and is labelled so throughout. I do
not re-score any pre-registered outcome. I attack it.

---

## A9 — THE NULL IS NOT TWO-POINT MATCHED (refuter-originated; not on the commissioned list)

**Why I am putting this first.** Amendment 3 §A3.2 makes the *entire* well-posedness argument
for the surrogate rest on one property: "Phase randomisation preserves `P(k)` exactly … the
two-point function is matched **by construction**, with no tuned parameter that can be got
wrong." That is true of `N1`. **Amendment 5 replaced the null with `N2`, and `N2` does not have
that property.** `N2` clips 37 % of its modulation at `1 + δ ≥ 0` and then adds a *second*,
independent, full-amplitude Poisson noise on top of a field that already carried the data's
shot-noise power. The recorded σ ratios above are the direct evidence: **the null's smoothed
rms is 17–24 % below the data's.**

Amendment 5 §A5.3 considered exactly one consequence of clipping — that it *manufactures*
skewness, hence inflates the valve floor, hence makes the target a lower bound. **It never
considered that clipping also destroys power.** Both effects are real and they push in opposite
directions. The record scores only the conservative one.

Two mechanisms follow, both of which *inflate* the target:

* **A9a — pedestal deficit.** `I_C⁽³⁾` at fixed `b` carries a floor that is a pure function of
  the pair marginals (the G2 "binmint" pedestal, measured on mocks at **29.3 %** of the reading
  at NGC R=15 b=4 folded and 7.1–19 % at R=10). If the null's pair structure is weaker than the
  data's, its pedestal is smaller, and the difference appears in `target` as signal.
* **A9b — under-sampled valve.** Clipping raises the mean modulation from 1 to ≈1.76, so `N2`
  is sampled at ~1.76× the data's number density and carries **less** shot noise per cell than
  the data does. The measured valve floor then *understates* the data's own Poisson minting.

**Corroborating evidence already in the record, which I did not generate:** the valve floor is
**negative** on every equilateral row and several squeezed rows (e.g. NGC R=15 b=4 equilateral,
`−1.57e-04`). `I(N2) < I(N1)` means adding Poisson noise *reduced* the reading — which is what a
pedestal collapse looks like, and it is largest exactly where the pedestal is largest
(equilateral, 47–60 % manufactured) and smallest where the pedestal is smallest (folded, 7–29 %).

### A9 tests, and what each outcome means

1. **A9a, direct.** Measure the binmint pedestal (`b' = 2b` fine histogram → IPF pair-maxent →
   merge to `b` → `I_C⁽³⁾`) on the **data** field and on the **N2** field, primary rows, both
   caps. Report `Δpedestal = pedestal(data) − pedestal(N2)` as a fraction of `target`.
2. **A9b, constructive.** Build `N2m`, a **power-matched** null: phase-randomise an amplitude
   `sqrt(max(|F(δ)|² − N_shot(k), 0))` so that after Poisson resampling the total power returns
   to the data's, with the clipped fraction and σ reported. Score `target_m = I(data) − I(N2m)`.

**Meaning, fixed now:**
* `target_m` below 5 σ on **all four eligible `(cap,R)` cells** → **KILL**.
* `Δpedestal` ≥ 10 % of target on a primary row, or `target_m` below `0.9 × target` on a primary
  row → **WOUND**, with the specific caveat that the "lower bound" framing is falsified and the
  target must be quoted with a stated downward correction.
* Both under 10 % → **CLEAR**, margin quoted.

A9b's own honesty condition: if `N2m` still clips more than 5 % of cells, or its σ misses the
data's by more than 5 %, I report it as an imperfect probe and say so rather than cashing it.

---

## A1 — NON-POISSON STOCHASTICITY

The valve floor was measured with pure Poisson resampling. Real galaxies are not Poisson: HOD
centrals are sub-Poisson, satellites super-Poisson, and — decisively for this pipeline — **the
deposited field is a weighted sum**, so its shot noise is inflated by `⟨w²⟩/⟨w⟩²` relative to
the unweighted Poisson the null draws. MultiDark-Patchy itself uses a **negative-binomial**
deviation-from-Poissonity in its stochastic bias model, so the mocks carry super-Poisson
stochasticity that the null does not.

**Test.** (i) Measure `⟨w²⟩/⟨w⟩²` directly from the BOSS catalogue — that is a floor on the
excess the null fails to carry, and it costs nothing. (ii) Rebuild the resampled null with
negative-binomial counts, `Var = λ(1+ε)`, at `ε ∈ {0.1, 0.25, 0.5, 1, 2, 4}`, sharing the same
phase-randomised modulation per seed so the comparison is paired. Find `ε_crit`, the dispersion
at which the NGC R=15 b=4 folded row drops below 5 σ.

**Meaning:** `ε_crit` at or below a dispersion defensible for BOSS galaxies (I will take
`ε ≤ 0.5`, i.e. shot noise up to 50 % above Poisson, as the outer edge of defensible, and state
my sources) → **KILL**. `ε_crit` in `(0.5, 2]` → **WOUND**. `ε_crit > 2` → **CLEAR**, margin
quoted as the factor by which the required dispersion exceeds the defensible range.

---

## A2 — SYSTEMATIC WEIGHTS (a pre-registered test that I believe was not run)

Prereg §7.5: "Imaging systematics and completeness weights: **MARGINALISED**, with the analysis
repeated under the published weight variants; a shift exceeding the statistical error between
weight schemes **voids** the affected bin." `sky_stage6.py` applies exactly one scheme,
`w = SYSTOT × (CP + NOZ − 1)`, and no weight-variant rerun appears anywhere in the record. I
will verify that reading of the record and then execute the test.

These are **correlated, multi-site** channels. No no-creation theorem covers them, and the
Amendment-5 null carries neither fibre collisions nor imaging systematics, so anything they
imprint on the order-3 sector lands in `target`.

**Test.** Recompute the primary rows (NGC, folded, R=15 `b=4,6` and R=10 `b=4,6,8`) under
(i) `w = 1`; (ii) `w = CP + NOZ − 1` (no SYSTOT); (iii) `w = SYSTOT` only; (iv) the published
scheme with FKP weights included. Each variant gets its own `N2` nulls, since the null is built
from the data field.

**Meaning:** a shift exceeding the row's `σ` on a primary row is, by the pre-registration's own
words, a **VOID** of that bin — I will report it as a **KILL of that bin** and, if it hits both
NGC R=15 rungs, a KILL of the R=15 arm. A shift between 0.3 σ and 1 σ → **WOUND**. Below 0.3 σ →
**CLEAR**.

---

## A3 — CAP CONSISTENCY

Gravity is isotropic; a cap-dependent *amplitude* is a systematics signature. NGC reads 9.4 σ
where SGC reads 3.8 σ at the same row, but significance is not amplitude.

**Test.** Compare `target_NGC` and `target_SGC` row by row, with the `σ` each row already
carries, propagating the 16-mock uncertainty on `σ` itself (`≈1/√(2·15) = 18 %`). Also compare
each cap against the *same* prediction, since the mocks predict the two caps to agree to 0.6–1.8 %.

**Meaning:** a cap difference above 3 σ on a primary row → **KILL of that row's
interpretation** (systematics-dominated). 2–3 σ → **WOUND**. Below 2 σ → **CLEAR**.

---

## A4 — THE 16-MOCK PREDICTION ENSEMBLE

`σ` and the recomputed prediction both come from **16** mocks per cap. `σ` from 16 draws is
itself uncertain by ~18 %, and the consistency test that outcome (a) leans on is
`|target − pred| < 3σ`.

**Test.** (i) Check whether the first 16 mocks are representative of the 128 measured in
`sky_surrogate_*.json`, using the identical quantity `I(mock) − I(N1)` available for both.
(ii) Reconstruct the 128-mock prediction as `mean₁₂₈[I(mock) − I(N1)] − mean₁₆[valve]`, with the
valve's own mock-to-mock scatter propagated, and compare against the 16-mock value. (iii) Launch
an extension of the mock-side `N2` ensemble and report it if it finishes.

**Meaning:** a prediction shift that moves any folded consistency beyond 3 σ → **WOUND**
(consistency was an artifact of a small ensemble). A `σ` that is understated by more than 25 % →
**WOUND**. Otherwise **CLEAR**.

---

## A5 — INDEPENDENT RECOMPUTATION

Reimplement the reading for the primary rows from the gridded field with **no estimator code
shared** with `sky_*.py`: my own Fourier smoothing, my own masked-smoothing division, my own
quantile binning, my own triple histogram, and a **dual/Newton** maximum-entropy solver rather
than IPF.

**Meaning:** agreement to `≤1e-6` relative → **CLEAR**. Disagreement above `1e-3` relative →
**KILL, regardless of every other outcome**. In between → **WOUND**, with the discrepancy
quoted and traced.

I will run it in two forms so a disagreement can be localised: (a) with the pipeline's own bin
edges, isolating the maxent solver and histogram; (b) with exact quantiles over all valid cells
instead of the pipeline's 4 194 304-cell subsample, which additionally tests whether the
subsampled edges bias `I`.

---

## A6 — THE SURROGATE'S SKEWNESS DEFICIT

The null reads smoothed skewness +0.387 against the data's +1.10. §A5.3 argues clipping's
contribution makes the floor an over-estimate. The adversarial reading is the opposite:
the null carries **less** pointwise non-Gaussianity than the data, and if that deficit mints
order-3 through the coarse-graining channel it inflates the target.

**The defence I must break first, stated fairly:** quantile binning is rank-based, so a pure
one-point-law difference between data and null is removed by construction (Sklar). The skewness
deficit can only bite through the *copula*, not the marginals.

**Test.** Build a deliberately over-generous null: a lognormal modulation matched to the data's
smoothed one-point law, Poisson-sampled. This null carries genuine order-3 structure (a monotone
map does not commute with smoothing — the exact defect that killed the Stage 3 control), so it
is an **upper bound** on what the pointwise channel can mint, not a fair null.

**Meaning:** if even this over-generous null leaves the target above 5 σ → **CLEAR**, and the
A5.3 conservative-direction argument survives its worst case. If it eats the target → **WOUND**
(not a kill: the probe is deliberately unfair), with the caveat that the pointwise channel is
unbounded by the current null.

---

## A7 — CONVERGENT ART

Search for prior measurements of copula non-Gaussianity, higher-order/connected information, or
maxent-gap statistics **on BOSS/SDSS data specifically**. The results document already disclaims
novelty (§7.7) and credits Scherrer et al. 2010, Qin, Yu & Zhang 2020, Schneidman et al. 2003,
Amari 2001.

**Meaning:** this attack cannot touch the measurement. If a prior published measurement of
essentially this quantity on this data exists, the finding is **re-scoped and credited** — I
will record it as a WOUND to any first-ness, and as CLEAR for the measurement itself.

---

## A8 — LOOK-ELSEWHERE AND EXCLUSION HYGIENE

Audit the S2.3b ruling, the `NGC/R=15/b=4/squeezed` exclusion, the Amendment-4 withdrawal of
outcome (b), and the Amendment-5 re-specification for post-hoc flexibility that favoured (a).
Specifically: was any exclusion or re-specification committed **after** a number that it
benefits was visible?

**Meaning:** any exclusion or threshold change made after the number it protects was visible →
**KILL** of the affected verdict. Documented pre-commitment with a stated reason → **CLEAR**.
Ambiguous ordering → **WOUND**.

I will also count the effective number of rows scored and state the look-elsewhere penalty
honestly, noting that at 40–51 σ it is not a live threat and at 9.4 σ it is worth a sentence.

---

## WHAT I WILL NOT DO

No `lake`. No Lean file, `Stance.lean` or audit touched. No stance recommendation — the verdict
goes to Eric. No re-scoring of a pre-registered outcome; only attacks on it. Every number I
produce is post-unblind and is labelled post-hoc. Files are pathspec-committed, never pushed.

---

*Refuter pre-registration ends. No refutation computation has been run.*
