# PRE-UNBLIND STATE — everything fixed before the data number exists

**The real galaxy catalogue has never been read.** Blinding is enforced in code:
`sky_realdata.measure_catalogue()` raises unless `stage6_unblind=True`, and nothing in Stages
0–5 passes it. This document is the complete state Stage 6 will execute against, committed
before any data reading and intended to be reviewed before the unblind order is given.

---

## 1. GATE REGISTER — every result, with its number

| gate | what it tests | result |
|---|---|---|
| **G1 LP pair-pinning** | is `τ` forced by the fine (`b'=2b`) pair marginals? | **PASS**, every row, both caps |
| **G2 binmint** | what coarse-graining mints from pair structure alone | **quantified**, folded 7–29 %, equilateral 47–60 % |
| **G5 / Gaussian control** | *(superseded by the G6 surrogate — §4)* | first construction **withdrawn** |
| **G6 phase-randomised surrogate** | `P(k)`-exact null | **PASS** both exit diagnostics, both caps |
| **G9 IPF certificate** | `\|share_H − share_KL\| < 1e-9` | **PASS**, worst `3.5e-12` |
| **G9 occupancy** | `>100` independent smoothing volumes per cell | **PASS/FAIL per cap and scale**, applied, §3 |
| **G10 mock closure** | half-A predicts half-B to 10 % of signal | **PASS**, 26/27, one named exclusion |
| **Gate A** (added) | post-pipeline `σ` physically sane | **PASS** `[0.463, 0.485]`; dye test passed |
| **Gate B** (added) | mask-perturbation sensitivity | **HEALTHY**, ratio 0.2, bulk-dominated |

### G1 — the LP gate passes, and not narrowly

Over every distribution carrying the measured fine pair marginals, the coarse sign-triple
moment can range across a width of **0.19–0.89**, against a statistical error on `τ` of
`4.0e-04`–`1.2e-03`. The half-width exceeds the error by **100–1000×**, where the
pre-registration required 5×.

**The pre-registered expectation is confirmed for the pre-registered reason.** `kappa-edge`
identified the pinning mechanism as near-*determinism* of the conditional support, and measured
that a Gaussian triple carrying the same pair correlations is **not** pinned (width 0.797)
while a noise-free logistic map is (width 0.000). A galaxy field smoothed at 15 Mpc/h is
nowhere near deterministic, and it reads 0.19–0.89. Note also *where the data sits*: `τ ≈
0.004–0.010`, near the **middle** of a wide interval — not at its floor, which is where
`kappa-edge`'s array sat when the pinning verdict fired against it.

### G2 — binmint, and why it reinforces the primary configuration

Fraction of the reading manufactured by coarse-graining a fine pair-maxent state:

| geometry | `R = 15` | `R = 10` |
|---|---|---|
| **folded (primary)** | **0.17–0.29** | **0.071–0.19** |
| equilateral | 0.47–0.54 | 0.52–0.60 |

**Equilateral is more than half manufactured. Folded is 7–29 %.** This is an independent reason
to keep folded primary, arrived at after the choice was made on `F₂`-kernel grounds.

---

## 2. AN UNPLANNED CROSS-VALIDATION, and it favours the primary configuration

Two null constructions that **share no machinery** — one randomises Fourier phases, the other
solves a maximum-entropy problem on a histogram — should agree if both are measuring the same
thing.

| geometry | ratio (fine-pair-maxent) / (phase-randomised) |
|---|---|
| **folded (primary)** | **0.84 – 1.11** |
| equilateral | 0.57 – 0.76 |

**At the primary configuration two independent nulls agree to 5–16 %.** At equilateral they
disagree by 24–43 %. Neither was tuned to the other; this was not planned and is recorded
because it is evidence about which configuration is trustworthy, not because it flatters the
result.

---

## 3. THE ANALYSIS PATH STAGE 6 WILL EXECUTE — fixed, no freedom left

* **Primary**: `I_C⁽³⁾(b)` on the **folded/collinear** configuration, `R = 15` Mpc/h,
  `b ∈ {4, 6, 8}` subject to the per-cap occupancy gate. **Secondary**: `R = 10`.
* **Statistic**: `Â = I(data) − I(phase-randomised surrogate of the data)`, surrogate seeded
  and recorded, identical pipeline. Compared against the frozen prediction of §5.
* **Pipeline, bit-identical to the mocks**: `Ω_m = 0.31`, `h = 0.68`, flat; interlaced CIC on a
  5-smooth grid at `cell = 6` Mpc/h; footprint by iterative in-footprint density threshold
  (`MASK_FRAC = 0.50`); smoothed positivity-guarded denominator; masked smoothing
  `W*(δM)/(W*M)` with kernel threshold `0.99`; quantile binning on valid cells; triples with
  all three cells valid; IPF with the KL certificate.
* **Occupancy availability** (from the mocks; the data shares the geometry):

| | SGC | NGC |
|---|---|---|
| `R = 15` | `b=4` only (218) | `b=4` (656), `b=6` (194) |
| `R = 10` | `b=4` (838), `b=6` (248), `b=8` (105) | all three (2404, 712, 301) |

* **Excluded by name, already ruled**: `NGC / R = 15 / b = 4 / squeezed` (G10 ratio 0.1259).
  It may not be reinstated. Squeezed at `R = 15` is marginal in **both** caps and is to be read
  as such.
* **Outcome (a)'s two-rung clause** rests on `R = 10` in both caps and on NGC at `R = 15`; SGC
  at `R = 15` is a single-rung result and cannot satisfy (a) alone.

---

## 4. WHAT WAS WITHDRAWN ALONG THE WAY, so the record is not just the survivors

1. **Stage 2's first production run** — 128×2 realisations, tight 0.7–2.3 % scatter, wrong by
   8–15×. A too-permissive footprint admitted a halo where the denominator fell to `~1e-7` and
   negative; `δ` std 2086. **The tight error bar was the artifact being reproducible, not the
   measurement being converged.**
2. **The Stage 3 Gaussian control** — smoothed skewness `+1.6688` where `~0` was required,
   because I applied a monotone map *before* smoothing and monotone maps do not commute with
   smoothing. My own pilot's 66 σ lesson, reproduced inside my own control.
3. **The Gaussian-modulation alternative** — 28 % of cells clipped, skewness still `+0.69`.
4. **Gate B's original polarity** — inverted; it flagged healthy data.
5. **The interim 2LPT yardstick** — retired rather than reported, once a denominator existed
   that transports.

---

## 5. STAGE 5 — the frozen prediction, and an honest problem with its provenance

**Frozen now, primary configuration (folded), from 128 mock+surrogate pairs per cap:**

| cap | `R` | `b` | prediction (signal) | ± |
|---|---|---|---|---|
| SGC | 15 | 4 | **`4.5342e-04`** | `6.70e-06` |
| NGC | 15 | 4 | **`4.4550e-04`** | `3.19e-06` |
| NGC | 15 | 6 | **`7.1739e-04`** | `4.34e-06` |
| SGC | 10 | 4 | `1.1770e-03` | `3.35e-06` |
| NGC | 10 | 4 | `1.1705e-03` | `2.01e-06` |
| SGC | 10 | 6 | `2.4840e-03` | `6.24e-06` |
| NGC | 10 | 6 | `2.4782e-03` | `3.70e-06` |
| SGC | 10 | 8 | `3.7039e-03` | `8.45e-06` |
| NGC | 10 | 8 | `3.6946e-03` | `5.29e-06` |

Full table in `sky_stage5_frozen_prediction.json`. **The two caps agree to 1.8 % at `R = 15`
`b = 4` and 0.6 % at `R = 10`** — independent footprints, independent randoms, same number.

### 5.1 THE PROVENANCE PROBLEM, stated rather than absorbed

`SKY_REALDATA_PREREG.md` §7.1 requires: *"the gravitational prediction must come from N-body
mocks, and it must be the same public suite used for the window and shot-noise model — that is
a closure requirement, not a convenience."*

**MultiDark-Patchy is not an N-body suite.** It is augmented Lagrangian perturbation theory
plus a calibrated stochastic bias model, tuned to reproduce a BOSS-like two-point function.
The prediction frozen above therefore satisfies the *same-suite* half of that clause and
**violates the N-body half.**

**What this costs, precisely:**

* **Outcome (a) survives, weakened.** "Detected and consistent with the gravitational
  prediction" becomes "consistent with the Patchy suite's higher-order structure", which is a
  product of its bias calibration as much as of gravity.
* **Outcome (b) cannot be claimed against this prediction.** An excess beyond a
  bias-calibrated approximate-gravity mock is not evidence of an anomaly, because the mock was
  never a first-principles prediction of the three-point sector. **Outcome (b) is therefore
  suspended** until an N-body prediction exists.
* Using Patchy for *both* the floor model and the prediction is exactly the circularity §7.1
  was written to forbid, and it is being done here **knowingly and under protest**, recorded so
  that no later reader can mistake it for a satisfied requirement.

**Recommendation for the reviewer**: either acquire an independent N-body suite (Nseries, or
the MultiDark parent boxes) before Stage 6 is scored for outcome (b), or amend the
pre-registration to restrict this measurement to outcome (a) and (c) only. **I have not made
that choice; it changes what the measurement can claim and belongs with the reviewer.**

---

## 6. STATE

| stage | status |
|---|---|
| 0 inventory | COMPLETE, Amendment 1 |
| 1 pipeline | COMPLETE, two defects caught by its own null |
| 2 floor + **G10** | COMPLETE, **G10 PASS** (first run withdrawn) |
| 3 controls | COMPLETE via the G6 surrogate (first construction withdrawn) |
| 4 LP + binmint | **COMPLETE, both PASS/quantified** |
| 5 prediction | **FROZEN**, with the §5.1 provenance objection on the record |
| **6 unblind** | **NOT STARTED — awaiting the separate unblind order** |

**The catalogue is unread. `measure_catalogue()` still raises. No data number exists.**
