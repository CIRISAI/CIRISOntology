# STAGE 2 — the first production run is WITHDRAWN. No G10 verdict yet.

Committed at the stage boundary. **The real galaxy catalogue remains unread; blinding is still
code-enforced.** This document exists because the honest state of Stage 2 is not a G10 verdict
but a retraction, and that has to be on the record before the re-run produces numbers that
would otherwise quietly replace the withdrawn ones.

---

## S2.1 What was withdrawn, and why

The first Stage 2 production run completed 128 realisations per cap and reported
`I_C⁽³⁾` between `7.9e-03` and `4.7e-02` nats with per-realisation scatter of 0.7–2.3 %,
which looked like a clean, well-converged floor measurement. **It was not. Those numbers are
withdrawn in full.**

The Stage 3 control caught it within minutes of starting, by reading the mocks' post-pipeline
`σ` as **176** — an impossible value for a density contrast, which should be well below 1 at
`R = 15`. The defect chain:

1. Amendment 2 moved the footprint definition onto a **smoothed** random field (correctly —
   raw counts cannot define a footprint from a sparse suite). I left the **denominator** of
   `δ = (n_g − αn_r)/(αn_r)` on the **raw** counts.
2. Worse, the mask threshold was `MASK_FRAC × median(exp0[exp0 > 0])`. **That rule is
   meaningless on this grid.** The interlaced CIC deposit goes through an FFT round-trip, so
   ringing leaves tiny nonzero values over **60 %** of the grid. `exp0 > 0` therefore selects
   almost everything, the median collapses by ~10×, and the threshold admits a large
   low-density halo that is not survey footprint at all.
3. Inside that halo the denominator fell to `~1e-07` **and went negative** (raw min
   `−1.77e-02`, from the same interlacing ringing). `δ` exploded: **std = 2086**, with 6.8 %
   of masked cells at `|δ| > 10`.

**Measured effect on the withdrawn numbers**: with the footprint and denominator fixed, the
same mocks read **8–15× lower**:

| | withdrawn | corrected | ratio |
|---|---|---|---|
| SGC `R=15`, `b=4`, folded | `1.03e-02` | **`6.82e-04`** | 15.1× |
| SGC `R=10`, `b=4`, folded | `1.09e-02` | **`1.43e-03`** | 7.6× |
| SGC `R=10`, `b=6`, folded | `3.22e-02` | **`2.73e-03`** | 11.8× |

The withdrawn run's small scatter (0.7–2.3 %) was not evidence of correctness. It was stable
because the halo contribution is a *fixed geometric artifact* — the same every realisation —
so it added a large, highly reproducible pedestal. **A tight error bar on a wrong quantity is
exactly what it looks like.** Raw JSON retained as `sky_stage2_{NGC,SGC}_INVALID.json` rather
than deleted.

## S2.2 The fix

* **Footprint**: thresholded against the **iteratively estimated in-footprint density**
  (`t ← mean(exp0 > 0.5t)`, converged in ~6 passes), not against any median-over-positive
  rule. Measured in-footprint density 2.97 randoms/cell for SGC.
* **Denominator**: the **smoothed** random field, positivity-guarded. The expected galaxy
  count is the selection function; Poisson noise in the randoms has no business in the
  denominator of `δ`.

Post-fix SGC: mask 0.154 of the grid (was 0.302), valid 0.105 at `R = 15`, `δ` std **2.97** —
consistent with Poisson at 0.058 galaxies per cell, which is what it should be.

## S2.3 What this does to the `b` ladder — the gate tightens again

Corrected occupancies (independent smoothing volumes / `b³`), SGC:

| `R` | `b=4` | `b=6` | `b=8` |
|---|---|---|---|
| **15** | **218 PASS** | 65 **FAIL** | 27 **FAIL** |
| 10 | **838 PASS** | **248 PASS** | **105 PASS** |

At the primary scale SGC now supports **`b = 4` only**. NGC's ~2.4× volume should carry
`b = 4` and `b = 6`. The pre-registered ladder is unchanged and the gate keeps deciding per
cap and per scale; this is the third time it has tightened as a defect was removed, which is
the gate behaving correctly rather than a moving target.

## S2.3b UNBLINDING CRITERIA FIXED NOW: which `b` ladder outcome (a) rests on

Fixed here, **before any data number exists**, because the corrected occupancy table changes
which rungs are available and the pre-registration's outcome (a) requires "**two or more
values of `b` that pass G9**".

| scale | SGC | NGC (expected, ~2.4x volume) | rungs available |
|---|---|---|---|
| **R = 15 (primary)** | `b=4` only (218) | `b=4`, `b=6` | **SGC cannot supply two rungs** |
| **R = 10 (secondary)** | `b=4` (838), `b=6` (248), `b=8` (105) | all three | **three rungs, both caps** |

**Consequence, stated so it cannot be interpreted after the fact.** Outcome (a)'s two-rung
requirement is satisfiable at `R = 10` in both caps, and at `R = 15` only in NGC. The
pre-registered text reads "at `R = 10` **and/or** 15", so this is within it — but the
practical reading is now explicit:

* **`R = 15`, SGC**: single rung. A detection there is reported as a **single-`b` result and
  cannot on its own satisfy outcome (a)**.
* **`R = 15`, NGC**: two rungs (`b = 4, 6`) and can satisfy (a) alone.
* **`R = 10`, both caps**: three rungs and is the ladder outcome (a) principally rests on.

**This does not promote `R = 10` back to primary.** `R = 15` remains primary for the reason
Amendment 1 gave — its shot-noise floor is ~58 % of signal against ~95 % at `R = 10` — and a
`R = 15` result that clears every other gate stands on its own merits. What changes is only
that the *two-or-more-`b`* clause of (a) is carried by `R = 10` and by NGC at `R = 15`, and
that is now on the record rather than available for later interpretation.

## S2.4 Why there is no G10 verdict in this document

Two independent reasons, and both were flagged before any of this went wrong:

1. **The run it would be scored on has been withdrawn.** The corrected re-run is in progress
   (both caps, 128 realisations, ~2.1 h).
2. **G10's denominator does not exist yet.** §5.6 sets the bar at "10 % of the **signal**",
   but a Patchy mock carries gravity *and* the pipeline's manufactured terms, so a mock
   reading is not a floor measurement and cannot supply that denominator. The floor is what
   the identical pipeline reads on a matched-two-point Gaussian field with no gravitational
   higher-order structure — the Stage 3 control. **Stage 2's verdict and Stage 3's control
   interlock, and the control must run first.** This is an ordering error in my own
   pre-registration, identified before the data was touched and not as a response to any
   number.

On the 2LPT-calibrated amplitude as an interim yardstick, now instructed rather than offered:
**it will be reported, labelled interim, and it will not be allowed to decide the gate.**
Both numbers go in the memo with no silent substitution, as instructed. But the reason I
declined it first still holds and is recorded rather than dropped: That amplitude was measured in a periodic box, at `b = 2`, with a matched-Gaussian
subtraction and no window. Transporting it across geometry, binning and window to serve as the
denominator of a go/no-go is precisely the manufactured comparison I refused in §S1.5 and that
this programme keeps catching. The Gaussian control supplies a denominator measured **in the
same pipeline, on the same footprint, at the same `b`**, and it costs ~30 minutes.

**So G10 will be scored against three denominators, all reported:** (i) the Gaussian control,
measured in-pipeline — **the one that decides**; (ii) the 2LPT amplitude, **labelled interim
and flagged as non-transporting**; (iii) the Stage 5 N-body prediction, which is the final
scoring and supersedes both. **If (i) and (ii) disagree about the verdict, the disagreement is
reported and neither is chosen** — a go/no-go that depends on which non-transporting number
you pick is not a go/no-go, and that fact would itself be the finding.

## S2.6 THE CORRECTED RE-RUN, AND WHY G10 IS STILL NOT SCORED

The corrected re-run completed: both caps, n = 128, and both artifact gates were applied.

**GATE A (sigma sanity): PASS.** `sigma` in `[0.4629, 0.4847]` (SGC) and `[0.4667, 0.4814]`
(NGC), against a band of `[0.02, 2.0]`. Applied to the withdrawn run for contrast it reads
`[40.96, 1548.23]` and `[33.58, 1743.28]` -- **the gate would have caught the defect that got
past the first production run.**

**GATE B (mask-perturbation, corrected polarity): HEALTHY.** A 21 % change in footprint volume
moves the floor by 2 % (`dI = 1.31e-05` against a realisation scatter of `7.78e-05`, ratio
0.2). Bulk-dominated, not boundary-dominated.

**Closure numerators, which stand.** `|mean_A - mean_B|` over 64/64 halves, folded:

| cap | `R` | `b` | mean A | mean B | closure error |
|---|---|---|---|---|---|
| SGC | 15 | 4 | `6.557e-04` | `6.442e-04` | `1.15e-05` |
| SGC | 10 | 4 | `1.4267e-03` | `1.4262e-03` | `4.9e-07` |
| NGC | 15 | 4 | `6.333e-04` | `6.217e-04` | `1.17e-05` |
| NGC | 15 | 6 | `9.093e-04` | `8.899e-04` | `1.95e-05` |
| NGC | 10 | 8 | `3.8951e-03` | `3.8814e-03` | `1.36e-05` |

Twenty-seven passing rows; closure errors are `5e-07` to `2e-05`, i.e. 0.08-3 % of the floor.
**The numerator is solid. There is still no denominator, and this is why.**

### S2.6.1 My Stage 3 control is wrong, and the diagnosis is exact

The control was meant to be "a Gaussian field at matched two-point structure, Poisson-sampled
through the same window". Measured against the mocks it produced a **negative signal at the
primary scale** (`-7.8e-04`, i.e. the mocks reading *less* connected information than the
control). That is not physics. Three measurements locate the fault, and it is mine:

1. **The lognormal control over-manufactures.** Smoothed skewness at `R = 15`: **control
   `+1.6688`, mock `+1.1122`.** A Gaussian control must read `~0`. The control is carrying
   *more* higher-order structure than gravity does.
2. **The reason is an error in my own justification.** I argued the lognormal was equivalent to
   a Gaussian control because *quantile binning is invariant under monotone per-cell maps at
   every `b`*. That invariance is real, **but it holds only when the monotone map is the last
   operation before binning.** Here SMOOTHING intervenes: `smooth(lognormal)` is not a monotone
   map of `smooth(Gaussian)`. This is precisely the transform-then-smooth manufacturing that
   `SKY_PILOT_RESULTS.md` measured at 66 sigma -- **reproduced inside my own control**, by me,
   after I had written the warning.
3. **The Gaussian-modulation alternative does not rescue it.** Clipping at `1 + delta >= 0`
   manufactures its own skewness: at the amplitude needed to reach `sigma = 0.47`, **28 % of
   cells clip** and the smoothed skewness is still `+0.69`.

**The underlying reason both fail**: at BOSS density and `R = 15` a positive-definite density
field with `sigma = 0.47` is **intrinsically skewed**. "A Gaussian field at matched sigma" is
not a well-posed object at this amplitude, so no tuning of that construction can produce one.

### S2.6.2 The control that is actually right, and was pre-registered all along

**G6, the phase-randomised null**: randomise the Fourier phases of the mock's own gridded
`delta`, keep the amplitudes, run the identical smoothing and binning. It matches `P(k)`
**exactly by construction rather than by tuning one number**, destroys all higher-order
structure, and needs no positivity surgery because it never re-samples a point set.

The two-point mismatch that the sigma-only tuning left is measurable and is on its own enough
to disqualify the current control: mock `sigma(10)/sigma(15) = 1.5015`, control `1.4418` -- a
4 % shape error, against a statistic whose Gaussian bias runs roughly as `rho^4` to `rho^6`
(`SKY_PILOT_RESULTS.md` section 3). Phase randomisation has no such freedom to get wrong.

**G10 verdict: NOT SCORED.** Not PASS, not FAIL. The numerator is measured and healthy, both
artifact gates pass, and the denominator does not yet exist because the control that was to
supply it is mis-specified in a way I have now measured rather than argued. **Scoring G10
against it -- or against the interim 2LPT amplitude, which does not transport across geometry,
binning and window -- would be exactly the manufactured comparison this programme keeps
catching.**

**Stages 4 and 5 do not proceed.** The pre-registration makes G10 the go/no-go, and a gate that
has not been scored has not been passed.

## S2.5 State

| stage | status |
|---|---|
| 0 | COMPLETE (`8b0c108`) |
| 1 | COMPLETE (`13df53a`) |
| 2 | first run WITHDRAWN; **corrected re-run COMPLETE**, n=128 both caps, Gates A and B pass |
| 3 controls | **run, and the construction is WRONG** (S2.6.1). Correct route identified: the pre-registered G6 phase-randomised null (S2.6.2) |
| **G10** | **NOT SCORED** — numerator measured and healthy; denominator blocked on a mis-specified control (S2.6) |
| 4, 5 | not started |
| 6 | not started; `measure_catalogue()` still raises without `stage6_unblind=True` |

**No stage may be reported as passed on the strength of the withdrawn run.**
