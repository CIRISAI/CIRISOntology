# AMENDMENT 3 — the G10 denominator, re-specified as the mock-minus-surrogate excess

Committed **before any new computation**. The corrected Stage 2 run and its two artifact gates
stand; only the denominator changes. The real galaxy catalogue remains unread and blinding
remains code-enforced.

---

## A3.1 What is re-specified

> **SIGNAL := `I_C⁽³⁾`(mock) − `I_C⁽³⁾`(phase-randomised surrogate of that same mock)**,
> one surrogate per realisation, seed recorded, both passed through the **identical**
> downstream pipeline. **G10's threshold is 10 % of that excess.**

The surrogate is built by Fourier-transforming the mock's own gridded masked `δ`, replacing
every mode's phase with a uniform random phase while **keeping its amplitude**, and
transforming back.

## A3.2 Why this is well-posed where the previous control was not

Three properties, and the first two are the load-bearing ones. **Both were verified
numerically before this amendment was written, not asserted:**

1. **Phase randomisation preserves `P(k)` exactly** — it changes only phases.
   Measured: `max | |PR(F)| − |F| | = 2.3e-13`. So the two-point function is matched **by
   construction**, with no tuned parameter that can be got wrong. This directly cures the 4 %
   two-point shape error that a one-number `σ` tuning left behind.
2. **Smoothing is diagonal in Fourier, so it COMMUTES with phase randomisation.**
   Measured: `max|smooth∘PR − PR∘smooth| / rms = 1.8e-07`. **This is precisely the property
   the lognormal control lacked.** A monotone per-cell map does *not* commute with smoothing,
   which is why `smooth(lognormal)` is not a monotone map of `smooth(Gaussian)` and why that
   control manufactured structure instead of measuring the floor.
3. **Quantile binning is rank-invariant**, so with `P(k)` matched and phases destroyed, the
   mock-minus-surrogate difference isolates the **copula sector at fixed two-point function** —
   which is the well-posed form of the target quantity.

**It also transports.** Because the surrogate is derived from each field's own modes, the
definition carries across geometry, binning and window automatically — curing the objection I
raised against the interim 2LPT amplitude, which was measured in a periodic box at `b = 2` and
cannot cross those boundaries. **The interim yardstick is therefore retired rather than
reported alongside**: it was only ever a stand-in for a denominator that did not exist, and
one now does.

## A3.3 The three measured numbers that forced this amendment

| measurement | value | what it showed |
|---|---|---|
| smoothed skewness at `R = 15`, lognormal control vs mock | **`+1.6688` vs `+1.1122`** | the control carried **more** higher-order structure than gravity; a Gaussian control must read `~0` |
| clipped-cell fraction of the Gaussian-modulation alternative at the required amplitude | **28 %**, and smoothed skewness still `+0.69` | positivity surgery manufactures its own skewness |
| two-point shape error left by `σ`-only tuning | **4 %** (`σ(10)/σ(15)`: mock `1.5015`, control `1.4418`) | against a statistic whose Gaussian bias runs as `ρ⁴`–`ρ⁶` |

The root cause, recorded because it is the generalisable lesson: **at BOSS density and
`R = 15`, a positive-definite density field with `σ = 0.47` is intrinsically skewed.** "A
Gaussian field at matched `σ`" is not a well-posed object at that amplitude, so no tuning of
that construction could have produced one.

## A3.4 What this denominator does and does not isolate — stated now, not later

The surrogate Gaussianises **every** phase coupling in the field, including the non-Gaussianity
that Poisson shot noise imprints. So:

* **mock − surrogate contains gravity's excess AND any shot-noise-induced (valve) minting.**
* For a **closure denominator** — a scale in which to express `|mean_A − mean_B|` — that is
  acceptable and is what this amendment adopts.
* For the **Stage 6 science signal** it is not sufficient on its own: the valve floor must
  still be separated, which is what `Core/Valve.lean` and the campaign's shot-noise measurement
  exist for. **This amendment re-specifies G10's denominator only. It does not re-specify the
  target quantity of the measurement**, and no Stage 6 reading may be normalised by it without
  a further amendment.

## A3.5 Carried forward unchanged

* **Closure numerators** from the corrected run: `5e-07` to `2e-05`, i.e. **0.08–3 % of the
  floor**, across 27 passing rows. Only the denominator changes.
* **Gate A (σ sanity): PASS** — `[0.4629, 0.4847]` SGC, `[0.4667, 0.4814]` NGC against a
  `[0.02, 2.0]` band. **Its dye test is passed**: applied retroactively to the withdrawn run it
  reads `[40.96, 1548.23]` and `[33.58, 1743.28]`, so it would have caught the defect that got
  past the first production run.
* **Gate B (mask-perturbation, corrected polarity): HEALTHY** — a 21 % change in footprint
  volume moves the floor 2 % (ratio 0.2), bulk-dominated rather than boundary-dominated.
* Every other gate, outcome, kill and data choice. `b ∈ {4,6,8}` with the per-cap occupancy
  gate; `R = 15` primary, `R = 10` stressed secondary; the S2.3b ruling on which ladder
  outcome (a) rests on.

## A3.6 A diagnostic this amendment must pass before G10 is scored

The surrogate is only doing its job if it is what it claims to be. Two checks, both cheap, both
required before the verdict:

* **`σ`(surrogate) ≈ `σ`(mock)** — the two-point structure survived the masked-field round trip.
* **smoothed skewness(surrogate) ≈ 0** — the phases really are destroyed. This is the exact
  check that caught the previous control at `+1.67`, now turned on its replacement.

**If either fails, G10 is again NOT SCORED and this amendment is superseded rather than
patched.**

---

*Amendment ends. No new computation preceded it; the catalogue is still unread.*
