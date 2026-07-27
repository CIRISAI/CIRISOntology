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

### 4.0 The branch condition, quantified — `m`, not the `p`-value, decides whether it matters

`pump-curve` (`PUMP_AMENDMENT_11`) measured the state-axis floor at `a = 0` to be **exactly
quadratic in the detuning `m`** — `floor ≈ K·m²` to five significant figures across four decades,
saturating above `m ≈ 0.1`. The `m²` scaling is the universal part; the prefactor `K = 0.00712` is
at *their* `r` and `s`.

So the sign-symmetry `p`-value says **whether** this pilot is off the symmetric point, and `m` says
**whether that matters**. Those are different questions and both are now in the table (§3, and the
`magnetisation` field on every reading).

Setting `K·m²` equal to **this pilot's own measured floors** (not the naive `0.227/N`) gives the
detuning at which the state axis would first reach the noise:

| | most sensitive template | least sensitive |
|---|---|---|
| **Planck** | `m = 4.2e−03` (`E008`) | `m = 1.9e−02` (`E064`) |
| **WMAP** | `m = 3.2e−03` (`E008`) | `m = 4.8e−02` (`E256`) |

`pump-curve` quoted `m ≈ 2.8e−03` from the naive `0.227/N = 5.7e−08`. **This pilot's measured
floors are 2–42× higher than naive (§6.2), so its real threshold is ~1.5× looser still.**

**Registered before the number is seen:** if the measured `m` comes back below `≈ 3e−03`, the
state-axis branch is **closed by measurement, not by argument** — its floor sits beneath this
pilot's own shot noise at every template and cannot affect any reading. That is a clean result and
not a disappointment. Above that it climbs as `m²`, so a factor of 10 in `m` is a factor of 100 in
the floor, and outcome (b) would need the full treatment of §4.1.

One caveat on this pilot's `m`, stated so the threshold is read correctly: the binarization splits
at the median of the **pooled** three slots, which pins the *pooled* magnetisation near zero by
construction while leaving each slot's own `m` free. The reported `m` therefore measures genuine
per-slot asymmetry — the right quantity — but it is bounded small by the pooling, and a large `m`
is not available to this design even if the sky had one.

### 4.1 If outcome (b) lands, the state-axis law is a leading quadratic too

`pump-curve` supplies the band with the law, having found the same limitation on that branch that
this pilot found on the channel branch (`PUMP_AMENDMENT_6`):

* the state-axis closed form **over-predicts at large detuning** — by up to **2.44×** at strong
  noise (ratio 0.410 at `s = 0.49`, `d = 0.30`);
* `share/d²` is exact as `d → 0` and drifts **−3.7 % by `d = 0.20`**, **−10.4 % by `d = 0.30`**.

**So on that branch the law is used for the SHAPE and the floor is MEASURED, never predicted** —
which is what this pilot's primary test already does, since it compares data to surrogate rather
than to any analytic value. Given the map's one-point skewness of −0.0131 the detuning is likely
small enough that the quadratic holds, but the band is recorded rather than assumed.

And the hazard that comes with that branch, in `glass`'s framing: **the state-axis pump vanishes as
noise → 0 but PEAKS at `s ≈ 0.10`.** So *"our noise is weak"* is not by itself a safety argument —
reducing noise toward `s ≈ 0.10` walks *up* the curve, not down it. Recorded here because the
instinct it contradicts is the natural one.

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
