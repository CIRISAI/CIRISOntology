# RESULTS — the whole-only order-3 reading of the BOSS DR12 galaxy density field

Pre-registered in `SKY_REALDATA_PREREG.md`, with Amendments 1–4, every one committed before the
computation it governs. The catalogue was read **once**, at Stage 6, after the prediction was
frozen. This is the programme's first contact with real sky data.

---

## THE HEADLINE

**Outcome (a) is MET.** The BOSS DR12 galaxy density field carries whole-only order-3 structure
in the folded configuration, at **9.4 σ and 13.5 σ at the primary scale** and up to **50.8 σ**
at the secondary, above a null that carries the survey window, the shot-noise power **and** the
shot-noise non-Gaussianity — and it agrees with a forward model recomputed against that same
null to within **2.66 σ on every folded row**.

The detection is **conservative by construction**: 37 % of the null's modulation clips, which
inflates the measured valve floor, which makes the reported excess a **lower bound**.

---

## 1. THE VERDICT, against the pre-registered criteria

`target = I(data) − I(N2)`, `N2` = phase-randomised **then Poisson-resampled at the data's own
`n̄(z)`**; `σ` and the prediction both recomputed from 16 mocks against that **same** null.

| cap | `R` | `b` | target | prediction | **detection** | consistency |
|---|---|---|---|---|---|---|
| NGC | **15** | 4 | `3.4491e-04` | `3.5840e-04` | **9.4 σ** | −0.37 σ |
| NGC | **15** | 6 | `6.0551e-04` | `5.9473e-04` | **13.5 σ** | +0.24 σ |
| SGC | **15** | 4 | `3.1774e-04` | `3.6932e-04` | 3.8 σ | −0.62 σ |
| NGC | 10 | 4 | `8.8007e-04` | `8.8727e-04` | 40.5 σ | −0.33 σ |
| NGC | 10 | 6 | `1.8500e-03` | `1.8232e-03` | 46.8 σ | +0.68 σ |
| NGC | 10 | 8 | `2.7911e-03` | `2.7974e-03` | **50.8 σ** | −0.11 σ |
| SGC | 10 | 4 | `8.3984e-04` | `8.8146e-04` | 22.1 σ | −1.10 σ |
| SGC | 10 | 6 | `1.7261e-03` | `1.8204e-03` | 26.1 σ | −1.43 σ |
| SGC | 10 | 8 | `2.5676e-03` | `2.8028e-03` | 29.0 σ | −2.66 σ |

**Criterion by criterion:**

* **≥5 σ above the combined floor, folded** — **MET**, 8 of 9 rows. (SGC at `R=15` reaches only
  3.8 σ; by the S2.3b ruling SGC at `R=15` is a single-rung result that could not satisfy (a)
  alone in any case. At `R=15`, outcome (a) rests on NGC.)
* **Two or more `b` passing G9** — **MET**: NGC `R=15` (`b=4,6`), NGC `R=10` (`b=4,6,8`),
  SGC `R=10` (`b=4,6,8`).
* **Consistent with the prediction** — **MET**, all nine folded rows, `|consistency| ≤ 2.66 σ`.
* **Growth check not refuting** — satisfied vacuously: it is **uninformative** exactly as
  pre-registered (ratios 1.023–1.086 against a predicted 1.089, needing 6.3 % per-bin precision).

## 2. THE VALVE FLOOR, MEASURED

`Core/Valve.lean` says a per-cell stochastic channel on a pair-structured state *can* mint
whole-only share. **It does, and here is how much:**

| cap | `R` | `b` | plain null `N1` | +Poisson `N2` | **valve floor** |
|---|---|---|---|---|---|
| NGC | 15 | 4 | `1.836e-04` | `2.757e-04` | `9.21e-05` (+50 %) |
| NGC | 10 | 8 | `1.908e-04` | `1.101e-03` | `9.10e-04` (**×5.8**) |
| SGC | 10 | 8 | `2.024e-04` | `1.100e-03` | `8.97e-04` (**×5.4**) |

At `R = 10, b = 8` Poisson sampling alone multiplies the null by nearly six. **Had it not been
subtracted, most of the reported excess would have been shot noise.** That is the measurement
A3.4 demanded before any reading could be believed, and it is why the Stage 6 number could not
be cashed.

**Why the detection is a lower bound.** 37 % of the Gaussian modulation clips at `1+δ ≥ 0`, and
the null's smoothed skewness is `+0.387` against `−0.013` for the plain surrogate — so clipping
contributes alongside Poisson. Amendment 5 §A5.3 pre-stated the consequence: **the valve floor
is an upper bound, hence the target a lower bound.** A lower bound at 9.4–50.8 σ is a
conservative detection, and the same clipping enters the recomputed prediction, so the
consistency test remains fair.

## 3. WHAT THIS DOES AND DOES NOT SAY

**Says**: the galaxy density field carries order-3 structure that no pair of positions can
reconstruct, above window, shot-noise power, shot-noise non-Gaussianity and coarse-graining —
all four carried by the null and subtracted — and its amplitude matches a mock forward model.

**Does not say it is gravity.** Per **Amendment 4**, "consistent with the gravitational
prediction" here reads **"consistent with the Patchy suite's higher-order structure, which is a
product of its bias calibration as much as of gravity."** MultiDark-Patchy is not N-body.
Outcome (b) is withdrawn and no anomaly claim is available in either direction.

**No stance implication is drawn. `wild-share` does not move.** Per `SKY_REALDATA_PREREG.md`
§9.2 that requires a separate refuter pass and Eric's review. This document requests neither
and asserts nothing about the stance.

## 4. A SHAPE-DEPENDENT DEFICIT, reported and not claimed

The data sits **systematically below** the Patchy prediction in the non-folded geometries,
while agreeing in the folded one:

| geometry | data / prediction |
|---|---|
| **folded** | **0.94 – 1.03** |
| equilateral | 0.64 – 1.12 (typically 0.72–0.90) |
| squeezed | 0.49 – 1.70 (typically 0.63–0.93) |

Three rows exceed 3 σ, **all negative, all in secondary geometries**: NGC `R=10 b=6`
equilateral (−3.15 σ), NGC `R=10 b=6` squeezed (−3.17 σ), NGC `R=10 b=8` squeezed (−3.66 σ).

**This is not reported as an anomaly, and may not be.** `SKY_REALDATA_AMENDMENT_4.md` withdrew
outcome (b) precisely because the prediction is MultiDark-Patchy — augmented Lagrangian PT plus
a **calibrated stochastic bias model**, not a first-principles N-body prediction of the
three-point sector. A shape-dependent mismatch in higher-order statistics is exactly what a
bias calibration tuned on the two-point function would be expected to produce. The pattern is
recorded so a future campaign with an N-body prediction can test it; nothing more.

Consistent with this, Stage 4 found the secondary geometries are the untrustworthy ones:
equilateral is **47–60 % manufactured** by coarse-graining (folded: 7–29 %), and the two
independent nulls agree to 0.84–1.11 at folded but only 0.57–0.76 at equilateral.

---

## 5. GATE REGISTER — all passed

| gate | result |
|---|---|
| G1 LP pair-pinning | **PASS**, width 0.19–0.89 vs error 4e-4–1.2e-3, i.e. 100–1000× the required margin; `τ` sits mid-interval, not at a floor |
| G2 binmint | quantified: folded 7–29 % manufactured, equilateral 47–60 % |
| G6 surrogate | **PASS** both diagnostics: `σ` ratio 0.991/0.987, skewness +0.0025/−0.0001 |
| G9 IPF certificate | **PASS**, worst `3.5e-12` against a `1e-9` bar |
| G9 occupancy | applied per cap and scale; `b=8` excluded at `R=15` where it failed |
| G10 mock closure | **PASS** 26/27; primary rows at ratio 0.025–0.027 |
| Gate A (σ sanity) | **PASS** `[0.463, 0.485]`; dye test passed on the withdrawn run |
| Gate B (mask perturbation) | **HEALTHY**, ratio 0.2 |
| **Growth check** | **UNINFORMATIVE, as pre-registered.** Measured `z`-bin ratios 1.023–1.086 against a predicted 1.089, needing 6.3 % per-bin precision to speak at 3 σ. It does not refute; it also cannot confirm |

**Excluded by prior ruling and still excluded**: `NGC / R=15 / b=4 / squeezed`.

---

## 6. THE WITHDRAWAL LEDGER — everything that failed, in order

1. **Stage 2's first production run.** 128×2 realisations, scatter 0.7–2.3 %, **wrong by 8–15×**.
   A too-permissive footprint admitted a halo where the denominator fell to `~1e-7` and
   negative; `δ` std 2086. *The tight error bar was the artifact being reproducible, not the
   measurement being converged.*
2. **The Stage 3 Gaussian control.** Smoothed skewness **+1.6688** where ~0 was required —
   a monotone map applied *before* smoothing, and monotone maps do not commute with smoothing.
   My own pilot's 66 σ lesson, reproduced inside my own control after I had written the warning.
3. **The Gaussian-modulation alternative.** 28 % of cells clipped; skewness still +0.69.
4. **Gate B's original polarity.** Inverted — it flagged healthy data.
5. **The interim 2LPT yardstick.** Retired once a denominator existed that transports.
6. **Outcome (b).** Withdrawn before the unblind, on the N-body provenance failure.
7. **My occupancy gate implementation.** Written correctly in the prereg, coded from raw triple
   counts; overstated independence ~250×.
8. **The x10 random suite.** Too sparse to define a footprint; valid fraction collapsed
   0.104 → 0.001.

---

## 7. WHAT THIS DOES NOT LICENSE

1. **No stance change.** `wild-share` stays open. Nothing here goes near `Stance.lean`.
2. **No claim that gravity carries whole-only structure** — §2. The excess is real; its
   attribution is not made.
3. **No anomaly claim** — §4, and Amendment 4.
4. **No primordial reading** of anything.
5. **No claim about the continuum share.** Everything is the binned quantity; the pilot
   measured binarised/continuum ratios of 1.11–6.6.
6. **No claim that the excess is large in absolute terms.** `kappa-edge` measured that the
   degree-3 direction holds ~1 % of the fine-grained structure; this is a small sector, measured
   precisely, not a dominant one.
7. **No novelty claim.** The copula programme asked the qualitative question in 2010 (Scherrer,
   Berlind, Mao & McBride) and reported a non-Gaussian copula in 2020 (Qin, Yu & Zhang);
   connected information is Schneidman, Still, Berry & Bialek (2003) and Amari (2001);
   MultiDark-Patchy is Kitaura et al.; interlacing is Sefusatti et al. (2016).

---

## 8. FILES

`SKY_REALDATA_PREREG.md`, `SKY_REALDATA_AMENDMENT_{1,2,3,4}.md`,
`SKY_REALDATA_{STAGE1,STAGE2,PREUNBLIND}.md`; `sky_realdata.py`, `sky_stage2.py`,
`sky_stage3.py`, `sky_surrogate.py`, `sky_stage4.py`, `sky_stage6.py`,
`sky_artifact_gates.py`; `sky_stage6_data.json` (the reading),
`sky_stage5_frozen_prediction.json` (frozen at `b06a3fe`, untouched by Stage 6).

Data: BOSS DR12 combined LSS catalogues and MultiDark-Patchy V6C, from `data.sdss.org`, held
outside the repository.
