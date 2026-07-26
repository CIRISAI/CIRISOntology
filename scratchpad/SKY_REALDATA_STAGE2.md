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

## S2.5 State

| stage | status |
|---|---|
| 0 | COMPLETE (`8b0c108`) |
| 1 | COMPLETE (`13df53a`) |
| 2 | **first run WITHDRAWN**; corrected re-run in progress |
| 3 controls | machinery written (`sky_stage3.py`), blocked on the corrected Stage 2 |
| **G10** | **NOT SCORED** — needs the re-run and the Stage 3 denominator |
| 4, 5 | not started |
| 6 | not started; `measure_catalogue()` still raises without `stage6_unblind=True` |

**No stage may be reported as passed on the strength of the withdrawn run.**
