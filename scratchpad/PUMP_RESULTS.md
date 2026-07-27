# PUMP campaign — results

**Pre-registration:** `PUMP_PREREG.md` (commit `64028fb`), frozen before any curve was computed.
**Prior art:** `PUMP_PRIOR_ART.md` (commit `8125797`). **Amendments:** `PUMP_AMENDMENT_1.md`,
five, all dated and all with data in hand, none rescuing a stake.
**Instrument:** `pump_curve.py`. **Records:** `pump_{dye,curveA,curveB,curveC,dose,qpu,sampled,coarse}.json`,
`pump_peak_ray.json`.

---

## THE HEADLINE

**The rate law is measured, and it has a closed form.** For three binary slots carrying
sign-symmetric pair structure, pushed through per-cell noise of asymmetry `a` and strength `s`:

> **`share = 18·r₀⁴·a² / [(1+2r₀)(1+3r₀)(1−r₀)] + O(a⁴)`,  `r₀ = (1−2s)²·ρ`**

confirmed against the exact solver to **3 parts in 10⁴** across κ = 1−2s from 0.99 down to 0.10
and input pair correlation ρ from 1.0 down to 0.05 — 61 gauged configurations, no exceptions.

**That figure is the COEFFICIENT, not the value, and the distinction is load-bearing.** The
formula is the leading term of an expansion in `a²`. Measured (AMENDMENT 4 §4.1,
`pump_correction_c.json`), the full statement is

> **`exact = closed × (1 + c(r₀)·a² + …)`**, with `c(r₀)` **minimum 3.01 near r₀ ≈ 0.36**, rising
> to **4.4 at r₀ = 0.64, 14.4 at r₀ = 0.81 and ≈ 95 at r₀ = 0.92**

so the value is within 2 % only for a ≲ 0.07 in the basin, and much less than that on a strongly
pair-correlated substrate. `c` is **not a constant** and a single correction coefficient is unsafe
at high pair correlation. Independently confirmed by the Planck pilot's sampled sky-geometry
gate — their 1.030 / 1.092 / 1.130 at a = 0.10 / 0.15 / 0.20 against this campaign's exact
1.0306 / 1.0705 / 1.1297, agreeing to 0.3 % at two of the three points.

**And the closed form answers a question that was left open in print.** Because a per-cell channel
is linear and `ferro` is a two-point mixture, the pumped state **is** `½·K(δ₀₀₀) + ½·K(δ₁₁₁)` — a
convex combination of two **product** states, each of whole-only share exactly zero (measured;
`|mixture − output| = 0.00e+00`). Kahle, Olbrich, Jost & Ay (2009) called *"whether the complexity
of a convex combination of two distributions is related to the complexities of the individual
constituents"* an **unsolved problem**. For this family the constituents are exactly zero and the
combination is the formula above.

**Three things are reported below as loudly as the closed form:** the campaign's own staked
k-scaling hypothesis is **refuted**; one of the repository's theorems is shown **not to
generalise** past three slots; and **the phenomenon itself, and the first curve of it, are not
ours** — they are Schneidman et al. 2003, Fig. 2, in the paper this repository already cites for
the quantity (`PUMP_AMENDMENT_1.md` §3.1, and the correction at the head of
`PUMP_PRIOR_ART.md`).

---

## THE VERDICT GRID

| stake | staked | measured | |
|---|---|---|---|
| **P-EVEN** `share(−a) = share(+a)` | exact | **2.2e-16** worst over 30 configurations | **PASS** |
| **P-EXP** exponent in `a` — *a calibration, not a finding* | ∈ [1.90, 2.10] | **2.006 – 2.072** (k=3), **2.007 – 2.050** (k=3…7) | **PASS** |
| **P-FORM** *as implemented* — the `a→0` coefficient | within 2 % | **1.000004 – 1.000279**, i.e. within **0.03 %** | **PASS** |
| **P-FORM** *as literally written* — `Δ/a²` pointwise, "anywhere" in the band | within 2 % | **3.85 % – 36.85 %**, firing on **13 rows of 13** | **FIRES** |
| **P-FORM-ρ** the `r₀⁴` law | fourth power | fitted **3.8125** vs the closed form's own effective slope **3.8126** over the same points | **PASS** |
| **P-K** k-scaling | **K-COUNT** (`∝ k` or `k³`) | `∝ k³` decisively worst (spread 4.1); `∝ k` beaten by the ceiling at every strength | **FIRES** |
| **P-QPU-1** our instrument vs the published prediction | ≤ 1 % | **0.0 %** (exact reproduction) | **PASS** |
| **P-QPU-2** hardware vs the designed-substrate law | ∈ [0.5, 2.0] | **0.815 – 1.348** over **6** in-band delays (t = 0 excluded: no pump, both terms at the hardware floor — AMENDMENT 4 §4.2) | **PASS** |
| **Arm F** does the law survive coarse-graining? | exploratory | **only when the coarse-graining is lumpable** | reported separately |

**P-FORM is two tests and they disagree — read AMENDMENT 2 before quoting either.** The prereg's
kill text says `Δ/a²` departing from the closed form "by more than 2 % **anywhere**", which is a
**pointwise** test; §3 of the same prereg defines the observable as `C ≡ lim_{a→0} Δ/a²`, which is
a **limit** test. The instrument implemented the limit. An independent gate by a second agent
(`PUMP_INSTRUMENT_GATE.md` §3, commit `a4d3b38`) recomputed the pointwise form and it **fires on
every row**, because the closed form is an `a→0` expansion and the deviation is exactly the next
term. Neither number is wrong; the record may not say "P-FORM passed" and stop. Both are in the
grid above, the pointwise table is in `PUMP_AMENDMENT_1.md` §6, and the kill is restated on `C`
there — which is what it should always have been, the exponent being textbook and the coefficient
the deliverable.

### Gates, all eight discharged before any physics was read

| gate | result |
|---|---|
| plumb lines (7 machine-checked states) | worst error **3.3e-16** |
| `valve_upward_bound` — a theorem's lower bound on a number we compute | bound 0.011962, **measured 0.021185**; and the state came back as `Core/Valve.lean`'s `bulge` exactly (9/16, 1/16 × 7) |
| two independent k=3 solvers agree | **6.6e-14** worst over 20 000 random states (staked 1e-12) |
| dual solver vs exact k=3 | **1.55e-15** (staked 1e-9) — *after a firing, see below* |
| cap compliance `share ≤ ln 2` | max 0.6174 over 20 000 states, no violation |
| **mixture null, theorem-pinned:** `a = 0` at the same strength | **6.7e-16** worst over 180 configurations — the unital channel mints exactly nothing at k=3, as `valve_needs_asymmetry` requires |
| dose-vs-rate composition identity | **3.3e-16** |
| IPF vs the exact solver | agrees to 2.8e-15 here; reported as a third number throughout, never as the answer |

**A gate fired on our own instrument and is kept in the record.** The k=3 plumb line applied to
the k≥4 dual machinery came back at **7.1e-9 against a staked 1e-9**. Cause: L-BFGS-B's stopping
tolerance, not an accuracy floor. Fixed with a closed-form Newton polish, re-gated at 1.55e-15.
The firing is in `PUMP_AMENDMENT_1.md` §3 because a plumb line that fires and is quietly re-tuned
has stopped being a plumb line.

---

## 1. The curve

Arm A, `ferro` through three identical kernels, exact solver, 13 gauged strengths:

| s | κ | r₀ | exponent | C measured | C closed form | ratio |
|---|---|---|---|---|---|---|
| 0.005 | 0.990 | 0.9801 | 2.0065 | 7.1558e+01 | 7.1557e+01 | 1.000004 |
| 0.020 | 0.960 | 0.9216 | 2.0060 | 1.5473e+01 | 1.5473e+01 | 1.000004 |
| 0.050 | 0.900 | 0.8100 | 2.0056 | 4.5380e+00 | 4.5380e+00 | 1.000004 |
| 0.100 | 0.800 | 0.6400 | 2.0068 | 1.2600e+00 | 1.2600e+00 | 1.000004 |
| 0.150 | 0.700 | 0.4900 | 2.0107 | 4.1603e-01 | 4.1603e-01 | 1.000007 |
| 0.200 | 0.600 | 0.3600 | 2.0182 | 1.3204e-01 | 1.3204e-01 | 1.000012 |
| 0.250 | 0.500 | 0.2500 | 2.0306 | 3.5714e-02 | 3.5714e-02 | 1.000020 |
| 0.300 | 0.400 | 0.1600 | 2.0343 | 7.1885e-03 | 7.1885e-03 | 1.000023 |
| 0.350 | 0.300 | 0.0900 | 2.0388 | 8.6597e-04 | 8.6600e-04 | 1.000026 |
| 0.400 | 0.200 | 0.0400 | 2.0433 | 3.9702e-05 | 3.9683e-05 | 1.000028 |
| 0.450 | 0.100 | 0.0100 | 2.0720 | 1.7764e-07 | 1.7306e-07 | 1.000279 |
| **0.475** | **0.050** | 0.0025 | — | — | 6.96e-10 | **UNGAUGED** |
| **0.490** | **0.020** | 0.0004 | — | — | 4.60e-13 | **UNGAUGED** |

The last two rows are reported as **ungauged, not as zero**: the pump falls off as **κ⁸** and
passes below the instrument's measured depth (1e-11 nat, 150× the two-solver bracket) at κ ≲ 0.1.
That is a measured statement about depth, not a limitation to apologise for.

**Two facts inside the formula worth separating**, because they point in opposite directions and
a reader will otherwise merge them:

- **Asymmetry is the pump** — the whole a-dependence, exponent 2, exactly even.
- **Strength is a savage brake** — the coefficient carries `κ⁸ = (1−2s)⁸`. Doubling the noise
  from s = 0.05 to s = 0.1 cuts the pump by **3.6×**; from 0.1 to 0.2, by **9.5×**.

**And the input pair correlation is the fuel, at the fourth power.** Arm B, 48 gauged
configurations across ρ ∈ [0.05, 1.0]: `C ∝ r₀⁴` at small `r₀`, fitted exponent **3.8125** against
the closed form's own effective slope over the same points, **3.8126**. Halve the surviving pair
correlation and the pump drops sixteenfold. This is why the pump is so much weaker on real
substrates than a linear intuition suggests, and it is the single most useful number in the
report for anyone estimating a floor.

**How far the formula may be quoted.** The prereg's declared band `|a| ≤ 0.25` was right for the
*coefficient* and too wide for the *value*. Measured at s = 0.1: within 2 % out to **a ≈ 0.07**,
within 10 % to a ≈ 0.15, 18 % low at a = 0.20. Beyond that only the exact solver is quoted.

---

## 2. THE THEOREM THAT DOES NOT GENERALISE — in TWO hypotheses, and we only found the second

**[AMENDED, see `PUMP_AMENDMENT_1.md` §3.2.] `valve_needs_asymmetry` has two load-bearing
hypotheses, not one, and this section originally reported only the limit we discovered
ourselves.** The theorem needs a **sign-symmetric input** *and* **three slots**:

| hypothesis | status | what breaks it |
|---|---|---|
| **sign-symmetric input** | **published counterexample since 2003** | Schneidman et al.'s AND gate under a fixed-probability per-cell flip — a **unital** channel — creates 0.0774 bits. AND is not sign-symmetric. Measured by us at `pump_schneidman_fig2.log` |
| **three slots** | **measured false at k ≥ 4 by this campaign** | below |

State asymmetry and channel asymmetry are **independent axes**. Every arm here holds the input
sign-symmetric, so this campaign's `a = 0` control is pinned **along the channel axis only**.



`Core/Valve.lean`'s `valve_needs_asymmetry` says a flip-covariant (unital) per-cell channel mints
**exactly zero** whole-only share from a sign-symmetric state, at any strength. Measured at k = 3:
**exactly zero, 6.7e-16 worst over 180 configurations.** Confirmed.

**At four slots and up it is false.** Same input (share exactly 0, measured ≤ 5e-14), same unital
channel, output verified sign-symmetric to **7e-18**:

| k | s=0.05 | s=0.1 | s=0.2 | s=0.3 | as a fraction of the (k−2)·ln2 ceiling, at s=0.1 |
|---|---|---|---|---|---|
| **3** | **4.4e-16** | **−1.1e-16** | **−1.1e-16** | **2.2e-16** | **0** |
| 4 | 1.307e-02 | 1.323e-02 | 4.545e-03 | 4.649e-04 | 0.96 % |
| 5 | 2.321e-02 | 2.729e-02 | 1.193e-02 | 1.566e-03 | 1.31 % |
| 6 | 3.198e-02 | 4.281e-02 | 2.224e-02 | 3.428e-03 | 1.54 % |
| 7 | 3.810e-02 | 5.663e-02 | 3.416e-02 | 6.061e-03 | 1.63 % |

**Why — and it is a counting fact, not an empirical surprise.** Under the global sign flip a
sign-basis coefficient transforms as `χ_S → (−1)^{|S|}χ_S`, so sign symmetry kills exactly the
**odd** `|S|`; pair-blindness means `|S| ≥ 3`. The surviving directions are the **even** subsets
of size ≥ 3, and there are:

| k | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|
| even pair-blind directions | **0** | 1 | 5 | 16 | 42 |

**k = 3 is the only case where every pair-blind direction is odd.** The vanishing at three slots
is not a general fact with an exception at four — *it is an accident of three*, and the floor
grows with k because the number of even survivors does. Verified directly on the k = 4 output: the
only non-zero coefficients are the six pairs at `κ² = 0.640000` and the single `|S| = 4` term at
`κ⁴ = 0.409600`, every odd one identically zero. **This argument is `pump-curve`'s**, supplied
after the measurement below and stronger than the reason originally given here
(AMENDMENT 4 §4.3). `Core/SignSymmetry.share_eq_zero_of_signSymmetric` is proved for three binary
slots and the restriction is now understood rather than observed. This repository already knew the fact and never drew the consequence:
`scratchpad/temporal-share/SPIKE_SURVEY.md` records the numerical check on four variables — odd
orders at 1.7e-13 while **order 4 survived at 0.169 nats** — and `Core/SignSymmetry.lean`'s SCOPE
paragraph says the general-k statement "is not mechanized". It is not merely unmechanized. **At
k ≥ 4 it is false**, and the file's design advice — *"order-3 whole-only structure requires broken
global sign symmetry"* — is correct as written for order 3 and must not be read as covering the
whole-only sector at more than three slots.

**What this costs, stated plainly.** The clean sentence "the pump is asymmetry, not strength" is a
**three-slot** sentence. On four slots and up, **symmetric noise alone mints roughly 1–1.6 % of
the ceiling**, and no symmetry argument protects a floor. Every campaign that reads more than
three slots and expects a symmetry-guaranteed zero has an unbudgeted floor of about that size.

**What it does not cost.** No Lean theorem is wrong: `valve_needs_asymmetry` states its
three-slot hypothesis and is confirmed exactly at three slots. What was wrong is the informal
generalisation, which lived in prose and in this campaign's own pre-registration.

---

## 3. k-scaling: the staked hypothesis is REFUTED

The excess above the symmetric baseline, `D_k(a,s)`, keeps **exponent 2 at every k** (2.007–2.050,
k = 3…7). What was staked was how its coefficient grows, and **K-COUNT was staked and loses**.

Spread of `C_k / normalisation` over k = 4…7 (1.000 would be a perfect law):

| s | / (k−2) *ceiling* | / k *slots* | / C(k,3) *triples* | / C(k,2) *pairs* |
|---|---|---|---|---|
| 0.05 | **1.173** | 1.218 | 4.105 | 1.642 |
| 0.10 | **1.133** | 1.447 | 3.455 | 1.396 |
| 0.20 | 1.346 | 1.923 | 2.600 | **1.158** |
| 0.30 | 1.833 | 2.619 | 1.909 | **1.310** |

- **`∝ k³` (triples) is decisively the worst** at low strength — spread 4.1. Refuted.
- **`∝ k` (slots) is beaten by the ceiling at every strength.** Refuted.
- **K-CEILING is the best single normalisation at weak noise** (spread 1.13–1.17), and the pair
  count wins at strong noise (1.16–1.31).

**Honest verdict: P-K FIRES.** K-COUNT, which the prereg staked and labelled its least confident
leg, is refuted in both its forms. K-CEILING is supported at weak noise and not at strong noise,
so **no single normalisation is flat across strength** — the k-dependence does not separate from
the strength dependence, which is a fact neither hypothesis anticipated. The symmetric baseline
`B_k` behaves differently again (its k-power runs 1.9 → 4.6 as s goes 0.05 → 0.3), so the two
objects do not even share a scaling.

---

## 4. Dose-vs-rate: "minted share per step" is a nuisance, and the invariant is named

Six trajectories, step-strengths from s = 0.01 to 0.1, up to 120 applications.

**The per-step rate is not step-count invariant and it is not close.** On one trajectory it runs
3.12e-2 → 2.43e-2 → 1.25e-2 → 4.55e-3 → 7.34e-4 → 6.88e-6 → 7.37e-9 at n = 1, 2, 5, 10, 20, 50,
100. **Four orders of magnitude.** Any campaign quoting a minting rate per step, per unit time or
per unit exposure is quoting a nuisance.

**The invariant is exact, and the gate is discharged by an identity rather than by a fit.** `n`
applications of `K` are one application of `K^n`, so the state depends only on the composed
channel and the whole many-step trajectory collapses onto the **same single-step curve** in the
composed channel's own coordinates `(a_eff, s_eff)`. Measured deviation across all six
trajectories and every step: **3.3e-16**.

**The bulge is universal.** Along any physical relaxation ray `a = α(1−κ)` — the ray every
amplitude-damping channel travels, with `α = 1 − 2p_exc` its asymmetry ratio:

| α | κ* at the peak | peak share (nat) | as a fraction of ln 2 |
|---|---|---|---|
| 1.00 | 0.8258 | 0.062440 | **9.008 %** |
| 0.95 | 0.8263 | 0.055121 | 7.95 % |
| 0.908 | 0.8268 | 0.049508 | 7.14 % |
| 0.80 | 0.8283 | 0.037007 | 5.34 % |
| 0.40 | 0.8328 | 0.008484 | 1.22 % |
| 0.10 | 0.8340 | 0.000517 | 0.075 % |

**The peak location is essentially independent of the channel: κ* = 0.826–0.834 across a tenfold
range in α**, and the peak height scales as **α^2.08** — the a² law again. So:

> **A relaxing three-bit habit puts at most 9.0 % of the one-bit ceiling into the whole-only
> sector, and it does so at 17.4 % relaxation, whatever the bath temperature.**

That is a parameter-free, quotable bound, and it is a prediction for any substrate that idles.

---

## 5. THE QPU POINT, OVERLAID — the cross-substrate number

Run 3, `ibm_marrakesh` Heron, qubits 6-7-8, job `d9in8jrjf64c739fprqg`. **Blinding was declared
absent in advance**: the bulge is already published, so this is a consistency check and nothing
here rests on it.

**QPU-1, the reproduction gate: our instrument reproduces the published zero-free-parameter
prediction column exactly — maximum relative deviation 0.0.** Independent code path, same measured
inputs. Our instrument is reading the same quantity the repository's is.

**The device's placement on the curve, which is what the overlay buys.** Measured per-qubit
excited-state populations `p_exc = (0.0367, 0.0102, 0.0905)` give asymmetry ratios
**α = (0.927, 0.980, 0.819)**, mean **0.908**. So this device idles on a ray very close to the
maximally asymmetric one — a cold bath, in the pump's coordinates — and that, not its noise
strength, is why it mints.

**QPU-2, the law:**

| t (µs) | a (mean) | κ (mean) | measured | closed form | ratio |
|---|---|---|---|---|---|
| 6.4 | 0.042 | 0.956 | 0.01946 | 0.02388 | 0.815 |
| 12.7 | 0.077 | 0.917 | 0.03575 | 0.03593 | 0.995 |
| 20.6 | 0.116 | 0.876 | 0.04480 | 0.04316 | 1.038 |
| 29.2 | 0.149 | 0.840 | 0.04795 | 0.04455 | 1.076 |
| 37.5 | 0.181 | 0.805 | 0.04807 | 0.04388 | 1.095 |
| 49.5 | 0.221 | 0.762 | **0.05405** | 0.04009 | 1.348 |

Ratios **0.758 – 1.348** over the seven in-band delays, inside the staked [0.5, 2.0]. **PASS.**
Outside the expansion band the closed form degrades exactly as declared (to 12× at 244 µs), which
is why the band was declared in advance.

**The single most valuable number in the report.** The universal peak formula, given nothing but
the device's mean asymmetry ratio α = 0.908, predicts a bulge of **0.0495 nat at κ* = 0.827**. The
hardware measured **0.05405 nat**, at a grid point one step past κ = 0.827.

> **Predicted 0.0495, measured 0.0541 — agreement to 9 %, from a four-line closed form whose only
> input is the average excited-state population of three superconducting qubits.**

Reported with its caveats, none of which are small: the three qubits have unequal channels, the
substrate is stretched-exponential rather than Markovian (run 2's fired shape kill), and the delay
grid does not sample κ*. Nine per cent is the claim; percent-level agreement is not.

---

## 6. The estimator floor — a correction useful to every campaign here

Arm G, 200 resamples per point, at states whose **true share is exactly zero**:

| N | measured median floor | `bias × N` |
|---|---|---|
| 100 | 3.35e-3 | 0.335 |
| 1 000 | 2.59e-4 | 0.259 |
| 10 000 | 1.97e-5 | 0.197 |
| 100 000 | 2.37e-6 | 0.237 |
| 1 000 000 | 2.41e-7 | 0.241 |

`bias × N` is flat at **≈ 0.22**, against **median(χ²₁)/2 = 0.2275**.

> **The finite-N floor of the k = 3 whole-only share is χ² with ONE degree of freedom:
> `median floor ≈ 0.227 / N` nat.**

Not `(cells−1)/2N = 3.5/N`, which over-states it **fifteenfold**. One degree of freedom, because
the k=3 pair envelope has exactly one free direction — the same fact the exact solver runs on.
Cross-checked at two strengths and five sample sizes.

**And the two mechanisms are cleanly separated, which was the point of the arm.** At a = 0 the
true share is zero and the estimator reads a pure 1/N bias. At a > 0 the estimator tracks the
true share to within 5 % at N = 100 and to 4 significant figures by N = 10⁴ — the valve is a
property of the distribution, the floor is a property of the sample, and at any N above a few
hundred they are not confusable at the sizes that matter here.

---

## 7. Arm F — coarse-graining, and the condition it hands the glass and water campaigns

Exploratory, separable, and it cannot feed the primary law. A four-letter cell pushed through a
four-letter per-cell channel, then binarized.

**The dye test first, because without it the number means nothing.** A **lumpable** fine channel —
one acting identically within each block of the partition — does induce an exact binary per-cell
channel. Through it, the instrument reads exponent **2.02–2.03** and coefficient ratio
**1.00002**. The a² law and its closed form survive a coarse-graining *exactly*, when the
coarse-graining is lumpable.

**Through a non-lumpable channel, the exponent is 1.09–1.53.** Same measure, same solver, same
substrate family. The difference is the coarse-graining.

Also measured: with a symmetric fine channel the binarized share is **exactly zero** (0, 1.1e-16,
0, −4.4e-16 at the four strengths), so the coarse-graining does not by itself manufacture share
here — it changes how the share depends on asymmetry.

> **Condition handed downstream: the pump law transfers across a binarization if and only if the
> binarization is lumpable with respect to the per-cell noise. Otherwise it does not, and the
> exponent is not 2.**

This is a *bound on transferability*, not a measured exponent for the non-lumpable family, since
that family's abscissa parametrizes the fine channel rather than an induced binary asymmetry.

---

## 8. DOWNSTREAM — what is licensed, what is not, and the unification's actual verdict

The prereg asked whether one law with one parameter replaces four separately-measured floors. The
honest answer is **partly, and the boundary is now sharp rather than assumed.**

| downstream | verdict | what it now gets |
|---|---|---|
| **QPU bulge** | **LICENSED** | a parameter-free prediction: peak `≈ 9.0 % × α² × ln 2` at κ* ≈ 0.827. Confirmed to 9 % on run 3 |
| **Planck pilot's valve floor** | **licensed if and only if** the instrument noise is same-alphabet per-pixel and its binarization is lumpable. **Both conditions are checkable and neither is checked here** | the closed form, once those two are discharged. Named as a prerequisite, not assumed |
| **sky shot-noise minting (130 %)** | **SPLIT, and the split is the finding** | the estimator half is `0.227/N` nat at k = 3 — **15× smaller than the naive `(cells−1)/2N`**. The valve half needs Poisson's own asymmetry put through this law, and Poisson-then-binarize is a coarse-graining whose lumpability is not established. The 130 % figure may **not** be reinterpreted wholesale |
| **glass / water coarse-graining floors** | **NOT LICENSED** | arm F gives them a sharp condition — lumpability — and the tools to test it. Their floors stay separately measured until that test is run |
| **anything at k ≥ 4** | **a new floor they did not have** | symmetric noise alone mints ≈ 1–1.6 % of the ceiling. No symmetry argument removes it |

**So the unification is real but narrower than the brief hoped, and it is reported at that size.**
Four floors do not become one parameter. What happened instead:

1. one floor (the QPU) became a **parameter-free prediction** and was confirmed;
2. one floor (the sky's estimator half) was **corrected by a factor of 15** in the direction that
   makes the campaign's problem smaller;
3. two floors (glass, water) got a **sharp, testable licensing condition** where they previously
   had an unexamined assumption;
4. and a **fifth floor nobody had budgeted for** was discovered at k ≥ 4.

---

## 9. SCOPE

Designed substrates and simulation, plus one hardware cross-check against a reading already in the
record. **Nothing here bears on `wild-share`** — which of nature's processes carry whole-only
structure — and nothing here is evidence that any wild process does.

**Nothing here moves `Stance.lean`**, and no stance change should be made from this run without a
separate refuter pass.

**Two repository corrections are NAMED, not made**, because this campaign does not touch the Lean:

1. `Core/Valve.lean`'s CREDIT paragraph should cite **Zhou, PRA 80, 022113 (2009)** and **Galla &
   Gühne, PRE 85, 046209 (2012)** alongside Kahle et al. — the creation of whole-only share by
   local channels is theirs, and `Core/Share.lean` already cites the same author's 2008 paper for
   the quantity itself. (`PUMP_PRIOR_ART.md`.)
2. `Core/SignSymmetry.lean`'s design advice and `Core/Valve.lean`'s `valve_needs_asymmetry`
   prose should say **three slots** wherever they currently read as general. The theorems are
   correct and hypothesis-stated; the surrounding prose invites a generalisation that this
   campaign measured to be **false at k ≥ 4**. (§2 above.)

**And the creation of whole-only share by local noise is not this programme's discovery — nor is
the first curve of it.** Both are **Schneidman, Still, Berry & Bialek, PRL 91:238701 (2003)**: Fig. 1
gives the quantity, Fig. 2 plots it against noise amplitude, and its AND and OR panels show a
**per-cell, unital** flip creating 0.0774 bits from a state with exactly `ferro`'s starting
condition. We measured that ourselves (`pump_schneidman_fig2.log`) rather than infer it from the
figure. Zhou 2009 and Galla & Gühne 2012 remain the first general statements and proofs, with the
mechanism stated in Girolami et al. 2017.

What is measured here for the first time, as far as two independent object-directed searches
reached, is narrower and should be quoted at that size: **the asymmetry-resolved law** — the
coefficient as a closed form in the channel's asymmetry, its strength and the input's pair
correlation, with its exponent, its theorem-pinned zero, its k-scaling, its two measured domain
limits, and a cross-substrate check. Kahle, Olbrich, Jost and Ay, whose paper `Core/Valve.lean`
already credits, called the general quantitative question "unsolved" in 2009, and §3.3 of the
amendments is an answer to it for one family.

**A third repository correction, named not made:** `Core/Valve.lean`'s CREDIT paragraph attributes
the creation mechanism to Kahle et al. Measured here, that attribution is wrong in the direction
that matters — Kahle et al.'s systems carry **no noise at all** and their peak is a two-phase
mixture, which is this repository's own metastability artifact. The correct citation for
*noise creating whole-only share* is **Schneidman et al. 2003 Fig. 2**, three references above it
in the same file.
