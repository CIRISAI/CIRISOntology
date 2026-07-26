# RESULTS — the whole-only order-3 reading of the BOSS DR12 galaxy density field

Pre-registered in `SKY_REALDATA_PREREG.md`, with Amendments 1–4, every one committed before the
computation it governs. The catalogue was read **once**, at Stage 6, after the prediction was
frozen. This is the programme's first contact with real sky data.

---

## THE HEADLINE

**A large, highly significant excess is measured, it matches the forward model to within a few
per cent — and the pre-registered outcome (a) is NOT claimed, because a floor I myself said
had to be separated was not separated.**

Both halves are the result. The second is not a caveat attached to the first; it is the reason
the first cannot be cashed.

---

## 1. THE NUMBER

`Â = I_C⁽³⁾(data) − I_C⁽³⁾(phase-randomised surrogate of the data)`, folded/collinear
configuration, identical pipeline, `σ` = per-realisation mock scatter from 128 Patchy
realisations (the cosmic variance of one universe).

| cap | `R` | `b` | excess | frozen prediction | **detection** | residual |
|---|---|---|---|---|---|---|
| SGC | **15** | 4 | `4.4501e-04` | `4.5342e-04` | **5.9 σ** | −0.11 σ |
| NGC | **15** | 4 | `4.1971e-04` | `4.4550e-04` | **11.6 σ** | −0.72 σ |
| NGC | **15** | 6 | `7.3850e-04` | `7.1739e-04` | **15.0 σ** | +0.43 σ |
| SGC | 10 | 4 | `1.1345e-03` | `1.1770e-03` | 30.0 σ | −1.12 σ |
| NGC | 10 | 4 | `1.1678e-03` | `1.1705e-03` | 51.4 σ | −0.12 σ |
| SGC | 10 | 6 | `2.3931e-03` | `2.4840e-03` | 33.9 σ | −1.29 σ |
| NGC | 10 | 6 | `2.4998e-03` | `2.4782e-03` | 59.6 σ | +0.52 σ |
| SGC | 10 | 8 | `3.4715e-03` | `3.7039e-03` | 36.3 σ | −2.43 σ |
| NGC | 10 | 8 | `3.6975e-03` | `3.6946e-03` | 61.7 σ | +0.05 σ |

**Every folded row is consistent with the frozen prediction** (`|residual| ≤ 2.43 σ`, most
below 1 σ), in two independent caps, at two scales, at three binnings. The agreement was not
tuned: the prediction was frozen and committed at `b06a3fe` before the catalogue was opened.

---

## 2. WHAT THIS DETECTS, AND WHAT IT DOES NOT

**Detected**: the BOSS DR12 galaxy density field, smoothed at 10–15 Mpc/h and read in the
folded configuration, carries order-3 structure that a **phase-randomised field with exactly
the same `P(k)`** does not — at up to 61.7 σ, matching a forward model built from 128 mocks.

**Not established**: that this excess is *gravitational*. And this is not a hedge — it is a
constraint I wrote down before the unblind and am now bound by.

> `SKY_REALDATA_AMENDMENT_3.md` §A3.4, committed before Stage 6:
> *"The surrogate Gaussianises **every** phase coupling in the field, including the
> non-Gaussianity that Poisson shot noise imprints. So mock − surrogate contains gravity's
> excess AND any shot-noise-induced (valve) minting… For the **Stage 6 science signal** it is
> not sufficient on its own: the valve floor must still be separated… **no Stage 6 reading may
> be normalised by it without a further amendment.**"*

The surrogate carries the shot-noise *power* (it has the data's `P(k)`) but as a **Gaussian**
field — so it does not carry the shot-noise **non-Gaussianity**. `Core/Valve.lean` proves a
per-cell stochastic channel on a pair-structured state *can* mint whole-only share, and this
campaign measured it doing so at **130 % of the mock signal** at DESI-like density. BOSS sits
at `n̄V_R = 4.81` (`R = 10`) and `16.2` (`R = 15`) — squarely in that regime.

**So `Â` = (gravitational order-3) + (Poisson valve minting), and the two are not separated.**

## 3. THE VERDICT

Outcome (a) requires the excess to be *"positive at ≥ 5 σ **above the combined forward-modelled
floor**"*. The shot-noise floor is part of that combination and it was not subtracted.

> ### **Outcome (a) is NOT claimed.**
> ### **Outcome (c) does not apply** — the reading is emphatically not null.
> ### **No VOID condition fired** — every gate passed (§5).

**None of the pre-registered outcomes fits.** That is itself a finding: **the outcome set was
incomplete.** It enumerated detection, null and void, and did not enumerate *"a large,
well-controlled, prediction-matching reading whose decomposition into signal and floor was
never performed."* That is where this measurement landed.

**The single measurement that would settle it**, named so it can be executed: Poisson-resample
the phase-randomised surrogate at the data's own `n̄(z)` and re-measure. The difference between
that and the plain surrogate is the valve floor; `Â` minus that is the gravitational excess.
It is one Stage-3-style control, it costs about an hour, and it needs its own amendment because
it changes the target quantity.

**No stance implication is drawn. `wild-share` does not move.** Per `SKY_REALDATA_PREREG.md`
§9.2 that would require a completed measurement, a separate refuter pass and Eric's review, and
this measurement is not complete.

---

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
6. **No novelty claim.** The copula programme asked the qualitative question in 2010 (Scherrer,
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
