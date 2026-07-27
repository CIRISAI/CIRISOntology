# AMENDMENT 6 — the pilot was assuming the hypothesis its theorem spends. Now it measures it.

**Prompted by `pump-curve`'s two-axis correction (`PUMP_AMENDMENT_5`, commit `d98155d`), received
before the G7b sky run and before the stage-5 data reading. No data reading has been taken. The
primary grid, the templates, the ladders, the test statistic and VOID conditions V1–V8 are
untouched.**

---

## 1. THE CORRECTION RECEIVED

`pump-curve` reports that there are **two** pump axes, not one:

| | **channel axis** | **state axis** |
|---|---|---|
| input must be | **sign-symmetric** | **not** sign-symmetric |
| channel must be | asymmetric; a unital channel mints nothing | nothing — a **unital** channel suffices |
| noise dependence | `(1 − r₀)` in the **denominator**; diverges as noise → 0 | `(1 − κ²)` in the **numerator**; vanishes as noise → 0 |
| shape | monotone, `κ⁸` suppression | **interior peak** at `κ ≈ 0.80` |

Both have exponent 2; everything else inverts. Their specific warning: **real CMB pixel triples are
not sign-symmetric**, so an arm that inherits the data's own state sits on a mixture of axes, where
the `a = 0` control is no longer a null and `c(r₀)` does not apply.

---

## 2. WHAT THE CHECK FOUND ABOUT G7b — it was already on the intended axis, by construction

`planck_pilot_g7b.py` takes its base from **`surr.s1(...)`** — a **phase-randomised surrogate**,
not the SMICA map. Uniform random phases make the field's distribution invariant under global
negation, so its median-split table is sign-symmetric by construction. **G7b is on the channel
axis, and `pump-curve`'s law and `c(r₀)` apply to it as sent.**

That was luck as much as design: the arm uses a surrogate because the *geometry* is what makes it a
sky test — the real mask, the real template, the real correlated triples — while the *field* only
has to satisfy the law's hypothesis. The warning is nonetheless correct and would have bitten a
version of this arm built on the data map, which is exactly what "real sky geometry" could have
been taken to mean.

**It is now verified rather than assumed:** G7b reports the base's sign-symmetry statistic before
any channel is applied, and a base failing it voids the arm.

---

## 3. THE LARGER POINT — this pilot was assuming its own theorem's hypothesis

The check `pump-curve` asked for is not only about G7b. **The whole pilot rests on
`share_eq_zero_of_signSymmetric`, whose hypothesis is that the three-bit table satisfies
`p(s) = p(−s)` — and until now this pilot asserted that of the data instead of measuring it.**
The pre-registration argues it from the Gaussianity of the field and the median split. That
argument is sound for the *surrogate*, which is sign-symmetric by construction. For the *data* it
is an inference from a prediction of standard cosmology, which is the very thing being gauged.

So the statistic is now computed for **every reading in the pilot, data included.**

### 3.1 The statistic

Pair each cell with its bin-reversed partner `(i,j,k) ↔ (b−1−i, b−1−j, b−1−k)` — at `b = 2`
exactly the global sign flip. Under a sign-symmetric distribution a pair's count difference has
variance `n₊ + n₋` under multinomial sampling, so

    chi2 = Σ_pairs (n₊ − n₋)² / (n₊ + n₋)

is `χ²` with one degree of freedom per pair (4 at `b = 2`). Reported with its `p`, and with the
worst **fractional** asymmetry `max |n₊ − n₋| / (n₊ + n₋)`.

### 3.2 Calibrated before use

300 multinomial draws at `N = 4 × 10⁶` from genuinely sign-symmetric distributions:

| | measured | required |
|---|---|---|
| mean `p` | **0.499** | 0.5 |
| fraction with `p < 0.05` | **0.047** | 0.05 |
| fraction with `p < 0.01` | 0.003 | 0.01 |

And its power against a planted asymmetry at the same `N`:

| planted fractional asymmetry | `χ²` (dof 4) | `p` |
|---|---|---|
| 1.41e−03 | 6.0 | 0.196 |
| **3.65e−03** | 16.2 | **2.7e−03** |
| 7.70e−03 | 58.6 | 5.7e−12 |

**Sensitivity ≈ 3 × 10⁻³ fractional asymmetry at this `N`.** Both the calibration and the dye are
on the record before the statistic is read on anything.

---

## 4. THE OUTCOME REGISTERED IN ADVANCE, BOTH WAYS

Stated now so it cannot be chosen after the number is seen:

**(a) If the data's table is sign-symmetric within the test's sensitivity** — the theorem's
hypothesis holds on the data as well as on the surrogate, `share_eq_zero_of_signSymmetric` applies
exactly, and "theorem-pinned zero" is the correct description of what the pilot measured against.

**(b) If it is not** — the hypothesis fails on the data and **the framing must weaken**: the
theorem then pins the *surrogate* exactly and the *data* only approximately, so the honest
statement becomes *"the reading is consistent with the empirically measured floor"* rather than
*"consistent with a proved zero."* The primary test is unaffected — it always compared data to
surrogate, never to an assumed analytic zero — but every sentence in the results calling the
target theorem-pinned would have to be qualified, and per `pump-curve`'s table the data would sit
on the **state axis**, where minting does not require an asymmetric channel.

Note that the median split forces each slot's marginal to 50/50 by construction, so the leading
one-point asymmetry is removed and any residual is a genuine **joint** asymmetry. The map's
one-point skewness inside the mask is **−0.0131** (§1 of the results), so outcome (b) is not
far-fetched at `N = 4 × 10⁶`.

**Neither outcome changes the pre-registered expectation**, which was and remains: the reading is
expected to be consistent with zero, and a significant nonzero reading is a pipeline defect until
proven otherwise.

---

## 5. TWO SIMPLIFICATIONS ACCEPTED FROM `pump-curve`

* The "fifth floor at `k ≥ 4`" they had flagged is **not a separate phenomenon** —
  `shareK₄(rep₄ through BSC(s)) = share₃(mix(γ=s) through BSC(s))` to `1.1e−15`, the fourth slot
  acting as a latent bit. Nothing in this pilot is at `k ≥ 4`, so nothing changes here; recorded so
  a future sky campaign does not re-derive it.
* Their observation that this pilot's replacement justification for the N-sym arm — `X` symmetric,
  `E` symmetric and independent ⟹ sign-symmetric table ⟹ `share_eq_zero_of_signSymmetric` — is the
  **right** route rather than merely a cleaner one, because it turns on exactly the property that
  decides which axis the arm is on. They also flag that `valve_needs_asymmetry` carries **two**
  hypotheses, three slots *and* a sign-symmetric input, with Schneidman 2003's AND gate the
  published counterexample to the second. Recorded; this pilot's route needs only the state
  condition, and §3 now measures it.

---

## 6. WHAT THIS DOES NOT CHANGE

The primary grid, the twelve templates, the `b`-ladder, the surrogate counts, the primary test
statistic and its leave-one-out calibration, the pre-registered expectation of §7.1, and VOID
conditions V1–V8 are **untouched**. The statistic added here is a **diagnostic recorded alongside
every reading**; it gates no cell and vetoes nothing by itself. Stage 3's surrogate ensembles were
already complete when it was added and do not carry it; stages 4, 5, 6 and G7b do.
