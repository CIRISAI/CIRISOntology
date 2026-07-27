# AMENDMENT 3 — the dye arm was going to be judged against the wrong floor

**Prompted by a cheap rehearsal of the stage-4 dye arm at `NSIDE = 256` on synthetic Gaussian
surrogates, run while the stage-3 floors were computing and before stage 4 executed. No share has
been computed on Planck or WMAP pixel values. The primary grid, the templates, the ladders, the
test statistic of §7.2 and VOID conditions V1–V8 are untouched.**

The rehearsal was run for one reason: `PLANCK_PILOT_PREREG.md` §8 **V4** says that if the planted
dye D1 is invisible at every registered amplitude, *every* null reading in this pilot is UNGAUGED.
That is the condition under which the pilot fails as a pilot, and it is worth four minutes of
synthetic data to find out before spending four hours of real ones. It found two things: the
pre-registered prediction for D0 and D2 confirmed **exactly**, and a design flaw in what D1 was to
be compared against.

---

## 1. WHAT THE REHEARSAL CONFIRMED — FACT 3, bit for bit

`NSIDE = 256`, `C_ℓ ∝ 1/ℓ(ℓ+1)`, full sky, 600 000 triples per template, floor from 40
realisations. Share at `b = 2`, template `E032`:

| `f` | **D0** (pointwise only) | **D2** (pointwise after filter) | **D1** (filter after pointwise) |
|---|---|---|---|
| 0.003 | 1.621e−05 | 5.726e−09 | 8.888e−09 |
| 0.01 | **1.621e−05** | **5.726e−09** | 1.138e−08 |
| 0.03 | **1.621e−05** | **5.726e−09** | 3.250e−10 |
| 0.1 | **1.621e−05** | **5.726e−09** | 4.646e−07 |
| 0.3 | 2.391e−05 | 2.395e−07 | 8.563e−06 |

**D0 and D2 are bit-for-bit identical across `f = 0.003 … 0.1` and move only at `f = 0.3`** —
which is exactly where `u ↦ u + f(u² − 1)` stops being monotone on the sampled range (turning
point `u = −1/2f = −1.67`). This is the pre-registered prediction of §6.6, and it reproduces the
`TARGET_REGISTRY.md` §0 calibration table (bit-identical until `a = 0.3`) on a *sky* pipeline with
a HEALPix geometry and a template selection. A pointwise map cannot move a copula statistic, and
now that is measured through this pipeline rather than inherited.

**D1 moves, and only D1.** It rises from 5.7e−09 at `f → 0` to 8.6e−06 at `f = 0.3` — a factor of
~1500. The 66 σ mechanism is present and it is separable from its own pointwise ingredient by
operation order alone.

---

## 2. THE FLAW — three arms, three different reference fields, one floor

The pre-registration compares all three arms to one floor: the S1 surrogate ensemble. That is
wrong, and the rehearsal makes it obvious.

* **D0** lives on the unsmoothed field `u`. Its `f = 0` value is `share(u)` = **1.621e−05**.
* **D1 and D2** live on the **60′-smoothed** field. Their `f = 0` value is
  `share(smooth(u))` = **5.726e−09** — **2 800× lower**, because smoothing changes the field.

Judging D1 (which starts at 5.7e−09) against a floor built from *unsmoothed* surrogates (median
2.74e−06) would have compared a reading to a floor drawn on a different field. That is the harvest
gate ***floor matched to sample size*** — whose known-bad anchor is Dalitz D2, where harsh-cut
readings scored `z ≈ 2.0` against a full-sample floor and the rise vanished entirely once the
floors were size-matched (`3a7e029`) — failing on this pilot's own dye arm, in the same shape.

It would have failed in the *conservative* direction here (an inflated floor hiding the dye, hence
a false V4), which is why it is worth saying plainly: a gate firing the safe way is still the gate
firing.

There is a second reference error in the same place. The three arms share **one base realisation**,
and a single draw of a `χ²`-shaped null routinely sits several times its own median — D0's `f = 0`
value is **5.9× the floor median**, purely from being one draw. So the arms' reference is not the
ensemble at all; it is **their own `f = 0` map**.

---

## 3. THE AMENDMENT

**(i) `f = 0` is added to the dye sweep** as an explicit control, so each arm carries its own
zero point measured rather than inferred. `DYE_F` becomes `{0.0, 0.003, 0.01, 0.03, 0.1, 0.3}`.
This adds a control point; it removes nothing and changes no threshold.

**(ii) A second floor family is computed: the 60′-smoothed surrogate ensemble.** `n = 50`
realisations, each produced by applying to an S1 surrogate the **byte-identical** smoothing call
D1 uses (`hp.smoothing(fwhm = 60′, lmax = 4096, iter = 0)`). D0 is judged against the raw floor;
**D1 and D2 are judged against the smoothed floor.**

**(iii) Each arm's primary comparison is to its own `f = 0` map**, reported as
`share(f) − share(0)` and as bit-equality for the arms where the theorem predicts bit-equality.
The floor comparison (`> p99`) is retained as the pre-registered detection-limit criterion, now
against the matched family.

Nothing else changes. The detection limit is still defined as *the smallest `f` whose reading
clears its floor's 99th percentile on all three templates at `b = 2`*, and V4 still fires if D1
never clears it.

---

## 4. A LIMIT ON WHAT THE REHEARSAL SHOWS

The rehearsal is `NSIDE = 256`, a power-law spectrum, no mask, no beam, no noise, 600 000 triples
and a 40-member floor whose `p99` is essentially its maximum. **No number in §1 is a result of
this pilot** and none is carried into the results document. It establishes two things only: that
D0/D2 are exactly invariant where the theorem says they are, and that D1's reference field is not
D0's. Both are properties of the construction, not of the sky.

In particular, at that resolution and that floor **nothing cleared `p99` at any `f`**, including
D1 at 0.3. That is a statement about a 40-member floor on 600 000 triples, not a forecast for the
full run at 3.9e6 triples with a 50-member matched floor — but it is on the record here, before
the fact, so that if V4 does fire at full scale it cannot be presented as a surprise.

---

## 5. WHAT THIS DOES NOT CHANGE

The primary grid (72 cells), the twelve templates, the `b`-ladder, the surrogate counts for the
primary test, the test statistic and its leave-one-out calibration, the pre-registered expectation
of §7.1, and VOID conditions V1–V8 are **untouched**. No data reading has been taken.

The rehearsal script is not committed as an instrument: it is a scratch check whose only output is
this document. The amended arm is in `planck_pilot.py::stage4` and
`planck_pilot_analyze.py`, committed with this amendment and before stage 4 runs.
