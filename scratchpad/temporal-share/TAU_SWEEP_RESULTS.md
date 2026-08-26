# τ SWEEP — results

**Verdict by the frozen rule: PREPARATIONAL. But the label's own interpretation is not
supported by the data, and the pilot's DIRTY BASELINE did not reproduce.** All three
statements are reported together because reporting any one alone would mislead.

Design frozen in `TAU_SWEEP_PREREG.md` before the instrument was written.
`ibm_marrakesh`, pair (95, 99), idle arm only, 6 delays interleaved in one job,
4096 shots, floor at the **99.583rd** percentile of 2000 permutations (Bonferroni,
FWER 0.05 over 12 tests). Job `da7gnijsq5js73bjuilg`.
**Cost 29 s; 46 s total for the campaign, 554 s remaining.**

## The readings

| τ | `Δ_{B→A}` | corrected floor | ×floor |
|---|---|---|---|
| 64 ns | 2.691e-4 | 3.653e-4 | 0.737 |
| 256 ns | 1.078e-4 | 3.108e-4 | 0.347 |
| 1.02 µs | 2.126e-4 | 3.022e-4 | 0.704 |
| 4.10 µs | 5.295e-5 | 3.583e-4 | 0.148 |
| 16.4 µs | 1.566e-5 | 3.279e-4 | 0.048 |
| **65.5 µs** | **4.072e-4** | 3.350e-4 | **1.216 — ABOVE** |

`Δ_{A→B}` is below floor at every τ. Spearman(τ, `Δ_{B→A}`) = **−0.0857, p = 0.9207**;
tied fraction 0.000 in both variables, disclosed per house rule.

## Three findings

**1. The pilot's DIRTY BASELINE does not reproduce.** At the *same* τ = 64 ns the pilot
read 1.67× its floor; this sweep reads **0.737×** — below. Both halves moved: the
measurement fell (3.364e-4 → 2.691e-4) and the floor tightened (95th → 99.583rd
percentile). This is what `CLOSURE_PILOT_RESULTS.md` predicted against itself when it
recorded that its uncorrected exceedance was "consistent with chance" at a ≈19%
family-wise rate.

**2. The one exceedance is at the family-wise boundary.** 1.216× at τ = 65.5 µs. With 12
tests at per-test α = 0.00417, the expected number of exceedances is 0.05 and
P(≥1) ≈ 4.9%. Observing exactly one sits *on* the declared α, not comfortably inside it.

**3. PREPARATIONAL fires, but its interpretation does not.** The prereg reads that
outcome as "fixed cost at preparation or readout — subtractable as a constant."
**There is no constant.** The series has mean 1.775e-4 with sd 1.476e-4, so
**sd/mean = 0.83**. That is noise, not an offset.

## A defect in the frozen outcome table, recorded not repaired retroactively

`PREPARATIONAL` was defined as *exceeds floor at ≥1 τ AND does not rise*. That bucket
catches two different things — a genuine constant offset, and chance noise with one
borderline hit — and this reading is the second while the label names the first. **The
verdict stands as PREPARATIONAL because that is what the frozen rule returns; it is not
silently re-read as CLEAN.** But a successor must add a flatness test (is the series
consistent with a NONZERO constant?) rather than inferring a constant from the mere
absence of a trend.

## Consequence for the four-arm

The independent arm is in **better** shape than DIRTY BASELINE implied. The honest
statement is not "there is a baseline to subtract" but **"the idle cross-residual is
consistent with zero across three orders of magnitude in τ, with one boundary
exceedance."** The four-arm should therefore carry these six readings as a measured
baseline **distribution**, not a point offset — there is no point offset to carry.

**Dynamical coupling is excluded** over 64 ns – 65.5 µs on this pair: ρ = −0.086,
p = 0.92, and the theorem that licenses the inference is
`Core/MatterCoupling.independent_views_closed` — independent decay is a product map and
cannot manufacture a cross-residual however severe it gets.

## No rescue

One job. No delay dropped, no refit, no re-run, statistic unchanged, and the verdict
reported as the frozen rule returned it rather than as the data's shape suggests.
