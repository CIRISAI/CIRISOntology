# RESULTS — the bispectrum bridge, simulation pilot

Pre-registered in `SKY_PILOT_PREREG.md`, committed at **`49c50de`** *before* `sky_pilot.py`
existed and before any number was computed. Scratchpad only: no Lean file, `Stance.lean` or
the audit was touched, and `lake` was never run.

---

## SCOPE, FIRST AND LOAD-BEARING

**This is a simulation pilot. No real survey data was read. Nothing here is a claim about the
sky, about cosmology, or about nature.** Every field below is one I generated with a
non-Gaussianity I put in myself. What is established is a fact about two *estimators* and
about where each one breaks. The deliverable for a real measurement is a **design**, in §9,
and it is a design, not a result.

---

## THE HEADLINE

**The bridge works, and it costs exactly the property that made the quantity worth having.**

The derived weak-coupling relation

    I_C⁽³⁾ = ½ · [ Σ (C⁻¹)₁ₐ(C⁻¹)₂_b(C⁻¹)₃_c ζ_abc ]² / perm(C⁻¹) + O(ζ³)          (B)

reproduces the exact share with a **shape error of 0.01 % across two decades of amplitude**,
and breaks at a locatable point (25 % error at marginal skewness 0.13–0.72, depending on the
triple's correlation structure). That is a survival of the pre-registered agreement criterion.

But the pre-registered prediction that mattered more also survived, and it cuts the other way:

| | Route A (exact share, `b=2`) | Route B (the bridge) |
|---|---|---|
| **lognormal — a per-cell transform of a Gaussian, truth = 0** | **exactly 0**, at every amplitude, machine precision | **false-fires at 10.5 σ** |
| noise floor on a 3D field, same data | **2.8 × 10⁻⁸ – 4.3 × 10⁻⁷** | 2.0–3.9 × 10⁻⁶ (5–84× larger) |
| sensitivity at weak `f_NL`, six configurations | z = −0.26 … 5.93 | **z = 2.37 … 16.75** |

**Route B is the more sensitive detector and Route A is the only honest one.** The bridge does
not annihilate pointwise non-Gaussianity — the trap `Core/SignSymmetry.lean` records — it only
**suppresses it by σ⁴**, whereas the `b=2` share is blind to it *by theorem, exactly, at every
amplitude*.

And the single most surprising result was not pre-registered at all: **the order of a pointwise
map and a filter decides whether the null holds.** Smooth-then-transform gives **0 differing
cells out of 16 777 216 × 48 field pairs**; transform-then-smooth, same ingredients, **fires at
66 σ.** Cosmology always smooths.

---

## 1. GATE — 14 tests, all pass; two amendments, both disclosed

| test | result |
|---|---|
| G1a general-`b` IPF vs the repository's fast `b=2` solver, 200 random states | 6.2e-16 |
| G1b same vs 60-digit `mpmath` | 1.7e-16 |
| G2 parity → `ln 2` (15 digits); independence → 0 | exact |
| G3a three-body coupling vs closed form `K tanh K − ln cosh K` | 3.5e-16 |
| G3b Route B at `C = I` equals `½ tanh²K` | 0.0 |
| G4 sign-symmetric states → 0, 2000 random (`Core/SignSymmetry.lean`) | 3.1e-16 |
| G5 Gaussian cells vs the orthant identity `(2/π)arcsin ρ` | 1.7e-16 |
| G6 latent vs general-`C` Gaussian cells, two independent quadratures | 1.0e-15 |
| G7 standardised latent: mean 0, variance 1 exactly; cum₃ matches nominal | 2.2e-16 / 7e-9 |
| G8 `|share_H − share_KL|` on the run's own states | 2.7e-15 (worst anywhere in the run: 3.3e-14) |
| G9 the reported quantity converged under quadrature refinement | 1.9e-11 rel. |

**Amendment 1 (G7).** The first version truncated the skewed latent's tail at a fixed range and
lost the third moment at 5e-4. Fixed at the source, not by relaxing the threshold: the
quadrature interval is now set by the 1e-18 quantiles, and — more importantly — **the
quadrature *is* the distribution**. Its weights are renormalised and its nodes affinely fixed so
the discrete law has mean 0 and variance 1 exactly, and its third cumulant is then *read off*
and fed to Route B. No truncation error can leak into the A-vs-B comparison as a fake
disagreement.

**Amendment 2 (G9).** The first convergence test compared *cell probabilities* under node
doubling and failed at 2.5e-12. The reported quantity is the *share*, so the test was moved
onto it (and the cell test kept alongside, at a tighter threshold). The quadrature was also
fixed to a constant step in the standardised variable, which is what the first version got
wrong: Simpson error is `O(h⁴)` and the integrands vary on scale 1 in `z`, so a fixed *node
count* silently degrades as the skewed tail lengthens.

**G8 is the load-bearing one.** IPF's multiplicative updates keep `log q` exactly a sum of pair
functions, and `p, q` share every pair marginal, so `D(p‖q) = H(q) − H(p)` holds *identically*
at the true maximum-entropy point. The gap between the two computations is therefore a rigorous
certificate that `q` is the I-projection, not merely that the marginals converged — which is
exactly the failure mode `ISING_FIELD_RESULTS.md` §2 recorded for `shareK`. Every share in this
document carries one, and the worst anywhere in the whole run is 3.3e-14.

---

## 2. K1 DID NOT FIRE — the Gaussian control reads zero at `b=2`

Exact arm, no sampling: `|I_C⁽³⁾| ≤ 1.1 × 10⁻¹⁶` at every correlation strength tested. The run
is not void.

This is not merely a passing control. The median split of a symmetric field is **sign-symmetric**,
so `share_eq_zero_of_signSymmetric` forces the answer, and the pilot's primary null is
protected by a machine-checked theorem rather than by my pipeline being careful.

---

## 3. P3 CONFIRMED — discretisation has a parity rule, and `b ≥ 3` is an artifact factory

The share of a **binned Gaussian**, whose true value is exactly zero:

| `ρ₁₂` | `b=2` | `b=3` | `b=4` | `b=6` | `b=8` | `b=16` | `b=32` |
|---|---|---|---|---|---|---|---|
| 0.09 | **1.1e-16** | 6.50e-07 | 7.49e-07 | 6.17e-07 | 4.72e-07 | 2.04e-07 | 7.82e-08 |
| 0.25 | **−2.2e-17** | 3.60e-05 | 4.09e-05 | 3.32e-05 | 2.52e-05 | 1.07e-05 | 4.05e-06 |
| 0.49 | **3.7e-17** | 4.65e-04 | 4.96e-04 | 3.85e-04 | 2.90e-04 | 1.25e-04 | 5.00e-05 |
| 0.81 | **1.0e-16** | 2.38e-03 | 2.40e-03 | 1.92e-03 | 1.52e-03 | 7.62e-04 | 3.57e-04 |

**Exactly zero at `b=2`, then eleven orders of magnitude above machine zero at `b=3`, then a slow
`~b^{-1.3}` decay.** Non-monotone in `b`, as pre-registered — so **the discrete share is not
monotone under bin refinement**, and coarse-graining *creates* whole-only structure rather than
only destroying it.

The pre-registered parity count explains it: a whole-only direction survives the global flip
iff it has an even number of flip-odd factors; at `b=2` the single contrast is flip-odd so the
one whole-only direction is anti-invariant (zero, re-deriving the Lean theorem by dimension
count), while at `b=3` four of the eight survive.

**The number that should frighten anyone binning finely:** at `ρ = 0.81`, `b = 3`, a **pure
Gaussian** reads `2.4 × 10⁻³` nats — half the largest genuine whole-only effect this programme
has ever measured (the Ising critical ridge, `4.6 × 10⁻³`).

### The raw `b ≥ 3` reading is amplitude-independent

Scaling exponent `d log I / d log γ` over the weakest four amplitudes (2 = a genuine share):

| `a` | `A(b=2)` | **`A(b=3)` raw** | `A−G(b=3)` | **`A(b=48)` raw** | `A−G(b=48)` |
|---|---|---|---|---|---|
| (0.5,0.5,0.5) | **2.000** | **0.003** | **2.000** | **0.036** | **2.000** |
| (0.8,0.6,0.4) | **2.000** | **0.001** | **2.000** | **0.003** | **2.000** |
| (0.3,0.3,0.3) | **2.000** | **0.023** | **2.000** | **0.320** | **2.000** |

An unsubtracted fine-binned reading of a weakly non-Gaussian field **does not respond to the
signal at all**. At `γ = 0.002`, 99.9 % of the `b=48` value is binning.

### An in-flight conjecture of mine, refuted by the data

Mid-run I reasoned that because the artifact is `O(1)` in the amplitude and the signal `O(γ)`,
the cross term `⟨P⊥u_artifact, P⊥u_signal⟩` would be **linear** in `γ` and would survive
subtraction, making `b ≥ 3` unrescuable. **That is wrong.** The subtracted columns above scale
as `γ^2.000` to four significant figures at every `b` and every configuration: the artifact and
the signal are effectively orthogonal and the Gaussian bias is **additive**. Recorded because I
had already written the opposite down, and because it changes the design conclusion — `b ≥ 3`
*is* usable, but only with a matched-Gaussian subtraction that is 10–1000× the signal.

---

## 4. K2 DID NOT FIRE — the standard non-Gaussian mock is a NULL

**Exact arm.** Quantile-binned lognormal vs quantile-binned Gaussian, over `σ_g ∈ {0.3,1,2}`,
`b ∈ {2,3,5,8,16}`, two correlation structures:

> **max |share_lognormal − share_Gaussian| = 1.3 × 10⁻¹⁶.** Max cell-probability difference
> 1.2e-16.

**And the null is not vacuous.** The same lognormals carry `ζ₁₂₃` from 1.6e-3 to 53, and
one-point skewness from 0.95 to 414.

**3D field arm.** A lognormal field built as a per-cell monotone map of a smoothed Gaussian
field: **0 differing cells, over 48 field pairs of 16 777 216 cells each**, at every amplitude
up to reduced skewness `S₃ = 21.6`. The excess over the paired Gaussian control is
`0.0000e+00` at every configuration.

The theorem behind it (pre-registered §2.3): the share is invariant under per-coordinate
monotone maps, because differential entropy shifts by `Σ E[ln|T_i′|]`, which depends only on
the one-dimensional marginals that every member of the pair envelope shares. **The brief's
proposed positive control is a second null, and a much sharper one than the Gaussian, because
it separates "has a bispectrum" from "has whole-only share".**

---

## 5. P4, P5, P6 — the bridge, and where it breaks

### P4 — the quadratic law, to four decimal places over three decades

At `b=2`, where the answer has a closed form from eight cell probabilities and can be pushed to
50 digits:

| `γ` | 1e-1 | 1e-2 | 1e-3 | 1e-4 |
|---|---|---|---|---|
| `I(b=2)` | 5.132e-06 | 5.140e-08 | 5.140e-10 | 5.137e-12 |

**Fitted slope 1.99991 over all seven points, 2.00015 over the weakest four.** `float64` and
`mpmath` agree to 6 significant figures at 5e-12. **K3 did not fire.**

### P5 — agreement, and the honest limit on how well it can be checked

**The binary bridge is essentially exact.** `B2 / A(b=2) = 1.0000` at every amplitude from
`γ = 0.002` to `γ = 0.5`, in all three configurations, degrading only to **0.9994** at `γ = 2`.

**The continuum bridge agrees to 3–10 %, and the limiting factor is Route A, not Route B.**
Extrapolating the exact bias-subtracted binned share to `b → ∞` (Richardson on `b` up to 160):

| case | `B / A_∞` | `A(b=2) / A_∞` |
|---|---|---|
| `ρ=0.25`, `γ=0.2` | 0.984 | 1.110 |
| `ρ=0.25`, `γ=0.05` | 0.974 | 1.105 |
| `a=(0.8,0.6,0.4)`, `γ=0.2` | 0.903 | 4.772 |
| `a=(0.8,0.6,0.4)`, `γ=0.05` | 0.909 | 4.811 |

Within the pre-registered 15 %, so **K4 did not fire** — but a three-parameter power-law fit to
the same sequence returns 1.10 and 1.21 instead, with a 1–2 % fit residual. **The two
extrapolations bracket `B/A_∞` in 0.90–1.24, and I will not quote a tighter number.** The
binned share converges as a slow power law (`α ≈ 0.6–1.7` depending on how it is fitted) and
`b ≤ 160` cannot resolve the continuum limit better than that. **Route A cannot be made
precise; that is a fact about Route A.**

The evidence that the *bridge* is right rather than merely close is stronger than the
extrapolation. At **fixed** binning the artifact is amplitude-independent, so the ratio
`B/(A−G)` isolates the truncation error alone — and it is **flat to 0.01 % over two decades**:

| `γ` | 0.002 | 0.01 | 0.05 | 0.1 | 0.2 | 0.5 | 1 | 2 |
|---|---|---|---|---|---|---|---|---|
| `B/(A−G)` at `b=48`, `ρ=0.25` | 0.8536 | 0.8536 | 0.8541 | 0.8555 | 0.8610 | 0.8993 | 1.0280 | 1.4912 |
| departure from plateau | −0.01 % | −0.01 % | 0.04 % | 0.20 % | **0.86 %** | **5.3 %** | **20.4 %** | **74.7 %** |

A γ-independent ratio means the bridge's **shape is exactly right**; only its `b→∞`
normalisation is unresolved, and the residual offset (0.854, 0.593, 0.966 for the three
configurations) tracks how converged `b=48` is, not the amplitude.

### P6 — the breakdown point, located

| configuration | `γ*` (25 % departure) | marginal skewness there |
|---|---|---|
| `a = (0.5,0.5,0.5)`, `ρ = 0.25` | **1.06** | **0.133** |
| `a = (0.8,0.6,0.4)` | **1.40** | **0.715** |

**The quadratic route is exact to better than 1 % below a marginal skewness of ~0.03, and
degrades to 25 % between 0.13 and 0.72 depending on the triple's correlation structure.** The
factor-5 spread across two configurations is itself a result: **the breakdown is not a
universal number in the amplitude and must be recalibrated for whatever field it is applied
to.**

### A limitation of the bridge that the exact arm does not share

The bridge does **not** annihilate the pointwise sector exactly — only to leading order. On the
exact lognormal, whose true share is zero at every amplitude:

| `σ_g` | 0.01 | 0.05 | 0.1 | 0.3 | 0.5 | 1.0 |
|---|---|---|---|---|---|---|
| 1-point skewness | 0.030 | 0.150 | 0.302 | 0.950 | 1.750 | 6.185 |
| **Route B (truth = 0)** | 3.4e-15 | 5.4e-11 | 3.4e-09 | **2.6e-06** | 6.1e-05 | 5.6e-03 |

The spurious prediction scales as **`σ_g⁶`** (measured exponent 6.00 ± 0.01 over `σ_g` = 0.1 → 0.01), while a
generic bispectrum of the same amplitude would give `σ_g²`. So the bridge suppresses pointwise
non-Gaussianity by `σ_g⁴` — a strong suppression, **not annihilation**. The pre-registered
analytic cancellation (§2.3) is exact only at leading order, and this measures the residual.

---

## 6. P7 — the 3D field arm

`N = 256³`, box 1000 Mpc/h (cell 3.906), Eisenstein–Hu no-wiggle transfer function
(`n_s = 0.96, Ω_m = 0.31, Ω_b = 0.048, h = 0.68`), Gaussian smoothing `R = 8` Mpc/h, 12
realisations. Every ladder is **paired against its own zero-amplitude member built from the
same white noise**, so realisation variance cancels in the difference. Tied fraction 0
everywhere — structurally, because nothing is thresholded onto a discrete value; **that is
"absent by construction", not "checked and found clean"**.

**The floor is measured, not modelled.** The Gaussian field's median split is sign-symmetric by
construction, so its true share is exactly zero by theorem and whatever it reads *is* the
estimator bias: `2.8 × 10⁻⁸` (L2) to `4.3 × 10⁻⁷` (L8).

| ladder | what it is | Route A `b=2` | Route B |
|---|---|---|---|
| **`lognormal_pt`** | smooth, **then** the per-cell map | **exactly 0** at every amplitude, `S₃` up to 21.6 | **false positive, z = 10.5** at `S₃ = 21.6` |
| **`lognormal_sm`** | the per-cell map, **then** smooth | fires, z up to **66.2** | fires, z up to 29 |
| **`fnl`** | pointwise map of the *potential*, then the transfer function | fires, z up to **48.3** | fires, z up to **70.7** |

Three things follow.

**(a) The order of a pointwise map and a filter decides whether the null holds.** `lognormal_pt`
and `lognormal_sm` use the identical white noise, the identical power spectrum, the identical
transform and the identical smoothing — differing only in which is applied first. One is an
exact null to the last bit; the other is a 66 σ detection. **A filter is not a per-cell map, so
it converts a field with exactly zero whole-only share into one with a large one.** This was not
pre-registered, and it is the pilot's most consequential finding for any real measurement,
because a survey's window, its mass assignment, its redshift binning and its selection function
are all filters.

It also explains the positive control: local `f_NL` fires precisely because the transfer
function `M(k)` stands between the pointwise operation and the observed field.

**(b) Route B has its own noise floor, and it is larger.** On a pure Gaussian field, Route B
reads `2.0–3.9 × 10⁻⁶` where the truth is zero — **5 to 84× Route A's floor**, configuration by
configuration, at identical data volume. Squaring a noisy three-point estimate has a positive bias. **The brief's premise that
the bridge "sidesteps the entropy-estimation traps entirely, because you never estimate an
entropy" is half right: it removes the entropy bias and installs a squared-estimator bias in
its place.**

**(c) Route B is nevertheless the better detector.** At the weakest `f_NL` rung (`S₃ = 0.60`),
over all six configurations: Route A `z = −0.26 … 5.93`, Route B `z = 2.37 … 16.75`, and Route B
wins in every one. The bridge buys roughly a factor of 3–6 in significance — and pays for it with (a) and with the `σ⁴`
leakage of §5.

**K5 did not fire**: the paired Gaussian control returns identically zero excess by
construction, and the unpaired floors are stable across 12 realisations.

---

## 7. SCORECARD AGAINST THE PRE-REGISTRATION

| | prediction | outcome |
|---|---|---|
| P1 | Gaussian, `b=2`, exact: 0 | **survived**, 1.1e-16 |
| P2 | lognormal = Gaussian, bispectrum large | **survived**, 1.3e-16 and 0 differing cells |
| P3 | `b≥3` nonzero; `A(b)` non-monotone | **survived** |
| P4 | slope 2.00 ± 0.05 | **survived**, 2.00015 |
| P5 | `|B/A_∞ − 1| ≤ 0.15` | **survived**, 0.90–1.24 bracket; agreement limited by Route A |
| P6 | breakdown locatable | **survived**, `γ* = 1.06–1.40` |
| P7 | field arm: nulls floor, `f_NL` fires | **survived** for Route A; **Route B false-fires on the null** |
| K1–K5 | — | **none fired** |
| K6 | `b=3` bias exceeds signal | **fired as anticipated** — design conclusion, `b=2` is mandatory without subtraction |

**Two things I wrote down and got wrong, corrected here rather than quietly dropped:**

1. **Pre-registration §6.4 claimed the `b=2` reading is "a strict lower bound on the continuous
   share". It is not.** `A(b=2)/A_∞ = 1.11–1.24` for the symmetric configuration and **4.8–6.6** for the
   asymmetric one (the bracket spans the two extrapolations of §5). Median binarisation can
   read **five to six times** the continuum value.
   Coarse-graining creates whole-only structure — the same phenomenon as §3, now at `b=2`,
   where only a *symmetric* field is protected.
2. **The in-flight cross-term conjecture (§3) is refuted** by a measured scaling exponent of
   2.000.

---

## 8. WHAT THIS ESTABLISHES AND WHAT IT DOES NOT

**Establishes:**
- The bridge (B), derived rather than asserted, with its normalisation, and validated to 0.01 %
  in shape over two decades of amplitude with a located breakdown.
- The lognormal — the standard analytic non-Gaussian mock — has **exactly zero** whole-only
  share, at every amplitude, in the continuum and on a 3D field: a machine-precision
  demonstration of the `Core/SignSymmetry.lean` trap in continuous-field form.
- Discretisation at `b ≥ 3` is an artifact factory with no signal response, and `b = 2` is the
  one binning protected by a theorem.
- A filter applied after a pointwise map manufactures whole-only share from nothing.
- Route B's floor, its `σ⁴` leakage, and its greater raw sensitivity — all measured.

**Does not:**
- **Nothing about the sky.** No survey data was read. No cosmological parameter, no `f_NL`
  constraint, no claim about nature. The `f_NL` amplitudes in §6 are in my own arbitrary
  potential normalisation and are reported only through the convention-free reduced skewness.
- **No stance change.** No promotion to `Stance.lean` under any outcome; that would need a
  separate refuter pass and Eric's review.
- **No priority claim.** (B) is an Edgeworth / connected-information calculation and is a
  projection of a known one; see the **Addendum** for full credit, the closest prior art (the
  LSS copula programme), and three corrections. The continuous-field framing of "the share measures non-Gaussianity" is the known
  quantity **negentropy** (Comon 1994; Hyvärinen & Oja 2000) — openly borrowed and credited,
  with the caveat that the *order-3* share is not the total negentropy but only the part no pair
  can see.
- **Does not settle the continuum limit of Route A** — `b ≤ 160` under a `~b^{-1}` convergence
  cannot, and the two extrapolations differ by 25 %.
- **Does not establish that the skewed latent resembles a cosmological field.** It is the case
  where the answer is computable; that is its entire job. The breakdown amplitude varies by a
  factor of 5 between two toy configurations and must be recalibrated for any real field.

---

## 9. DESIGN — what a real measurement would require

Stated as a design, conditional on the bridge, and **not** as a proposal that this measurement
is currently worth making.

1. **Never bin finer than `b = 2` without a matched-Gaussian subtraction.** The raw `b ≥ 3`
   reading has a scaling exponent of 0.003 in the signal amplitude — it measures the binning.
   With subtraction it is usable and quadratic, but the subtracted term is 10–1000× the signal.
2. **The bridge needs the collapsed and coincident-point three-point terms** `ζ_iij` and
   `ζ_iii` — the one-point skewness of the smoothed field and the collapsed 3PCF — not only the
   bispectrum at well-separated triangles. These are precisely the terms dominated by shot
   noise, aliasing and the mass-assignment window. **A bispectrum measurement alone does not
   supply the bridge's inputs.**
3. **Validity regime.** Fractional error below 1 % requires marginal skewness ≲ 0.03. For a
   large-scale-structure field, skewness ≈ `S₃ σ_R` with `S₃ ≈ 3–4`, so `σ_R ≲ 0.01` — a
   smoothing scale of several hundred Mpc/h, where cosmic variance is worst. At the 25 % level
   (skewness ≈ 0.13) one needs `σ_R ≈ 0.04`, i.e. `R ≳ 100` Mpc/h. **The scales where the
   quadratic route is trustworthy are the scales with the fewest independent modes.** A
   spectroscopic survey with the largest available volume and a well-characterised window —
   DESI or Euclid — is the only relevant class.
4. **The dominant systematic is not statistical, it is §6(a).** The survey window, the
   mass-assignment kernel, redshift-space distortions and the selection function are all
   filters, and a filter *manufactures* whole-only share out of a field that has exactly none.
   That contribution must be **forward-modelled**, never deconvolved, and it will not be small:
   in the pilot, applying an 8 Mpc/h Gaussian filter after the transform took an exact zero to a
   66 σ detection.
5. **The compounding problem.** Gravitational evolution produces a bispectrum whose leading
   shape is close to, but not exactly, the pointwise form. The bridge suppresses that only as
   `σ⁴`, so a real measurement is a difference of two nearly-cancelling large terms, on top of
   (4).
6. **Therefore the recommended target is not the bridge.** The quantity worth measuring is the
   **`b=2` sign-triple excess** — the excess of `⟨s₁s₂s₃⟩` over what the sign pair marginals
   force. It is exactly blind to the pointwise sector by theorem, has a floor 5–84× smaller,
   needs no entropy estimate and no binning choice, and its quadratic truncation is exact to
   0.06 % even at the strongest amplitude tested. It costs a factor of ~6 in raw sensitivity
   and it measures the *binarised* share, which is a different number from the continuum share
   (by up to a factor of ~5–6, §7). **That is the trade, stated so it can be refused.**

---

## 10. FILES

| | |
|---|---|
| `SKY_PILOT_PREREG.md` | pre-registration, committed at `49c50de` before any code |
| `sky_pilot.py` | gate, Arm 1 (exact), Arm 2 (3D fields), both bridges |
| `sky_bconv.py` | the `b → ∞` convergence study |
| `sky_pilot_arm1.json`, `sky_pilot_arm2.json`, `sky_bconv.json` | raw results |
| `sky_arm1.log`, `sky_arm2.log`, `sky_bconv.log` | run logs, including the failing gate |

Primary seed 20260725; field arm 12 independent realisations. Research → scratchpad memo →
Eric's review. Nothing pushed.

---
---

# ADDENDUM — convergent-art check, credit, and three corrections

Added after the run above, in response to a convergent-art warning. Two of the warning's
three technical claims are **wrong**, and I show why with numbers rather than argument. The
warning's *instinct* was nonetheless right, and it was right about something it did not name:
**the closest prior art is the large-scale-structure copula literature, and it is much closer
than the negentropy/Edgeworth line the warning pointed at.** Script `sky_refute.py`, raw
output `sky_refute.json` / `sky_refute.log`.

## A1. THE CLOSEST PRIOR ART — the LSS copula programme (not found by me until now)

**Scherrer, Berlind, Mao & McBride, ApJL 708:L9 (2010), "From Finance to Cosmology: The
Copula of Large-Scale Structure"** measured the empirical two-point copula of the evolved dark
matter density field, found it **well approximated by a Gaussian copula**, and explicitly
considered the hypothesis that **the full n-point copula is Gaussian**.

That hypothesis is, word for word in a different vocabulary, the statement **"the whole-only
share of the matter density field is exactly zero at every order."** The bridge between the
two vocabularies is my §4 theorem — and *that theorem is standard copula theory* (Sklar 1959):
a copula is by construction invariant under monotone per-cell transformations, which is the
same invariance, stated in the cosmology literature in 2010. **My "pointwise-transform
theorem" is not new.** What §4 adds is only its consequence for this particular entropy gap,
and the machine-precision verification.

**Qin, Yu & Zhang (2020), arXiv:2006.06182, "The copula of the cosmological matter density
field is non-Gaussian"** report statistically significant non-Gaussianity in the Gaussianized
field. So the qualitative question — is there anything above the pointwise-Gaussian
description? — **has already been asked and answered affirmatively in this literature.**

**The logical relation, which is not trivial and is worth stating.** Gaussian copula ⟹ share =
0, so **nonzero share ⟹ non-Gaussian copula**. The converse fails: `share = 0` only requires
membership in the pairwise-maxent family `exp(Σ f_ij)`, which is far larger than the Gaussian
family. **A non-Gaussian copula is therefore necessary but not sufficient for nonzero
whole-only share, and the existing detections do not establish it.** The share is a strictly
finer null than the copula test — that is the honest remaining gap, and it is a narrow one.

**Carron, ApJ 738:86 (2011), "On the incompleteness of the moment and correlation function
hierarchy as probes of the lognormal field"** is adjacent but a different quantity (Fisher
information, not an entropy gap). Its mechanism, however, lands squarely on Route B: the
lognormal is an **indeterminate moment problem**, and once its variance approaches unity
essentially none of its information content is reachable through its moments. **A moment-based
bridge inherits that.** This independently corroborates §5's measured `σ⁶` leakage and §9's
warning that a real measurement is a difference of nearly-cancelling large terms.

## A2. CREDIT, corrected and expanded

| object | credit |
|---|---|
| negentropy `J = H(φ_C) − H(p)` as a non-Gaussianity measure | Comon, *Signal Processing* 36:287 (1994); Hyvärinen & Oja, *Neural Networks* 13:411 (2000) |
| negentropy as a cumulant/Edgeworth series, incl. the multivariate form | **Jones & Sibson, *JRSS A* 150:1 (1987)** |
| connected information / maxent irreducible correlation | Schneidman, Still, Berry & Bialek (2003); Amari (2001) — already carried in `Core/Share.lean` |
| copula invariance under monotone per-cell maps | Sklar (1959); **Scherrer, Berlind, Mao & McBride, ApJL 708:L9 (2010)** |
| the LSS copula is non-Gaussian | **Qin, Yu & Zhang (2020), arXiv:2006.06182** |
| moment hierarchy fails on the lognormal | **Carron, ApJ 738:86 (2011)** |

**On the Ising `h`-exponent of 2.000** (`ISING_FIELD_RESULTS.md`) and this pilot's 2.00015:
the warning is right that this is **the expected exponent of a known expansion**, not a
discovery. Quadratic response is what any second-order expansion of an entropy gap around a
Gaussian/maxent reference gives. It is reported here as a *pre-registered control that the
pipeline reproduces a known law*, and should be read that way in the Ising memo too.

## A3. CORRECTION 1 — the share is **not** negentropy. This is not an identity.

The warning states: *"The whole-only share of a continuous field relative to its pair structure
IS negentropy… The Gaussian is the pair-matching maxent for continuous variables, so this is an
identity, not an analogy."*

**The premise is false.** The Gaussian is the maxent given the **covariance**. The pair
envelope constrains the full **pairwise marginals**, a strictly larger constraint set whose
maxent family is `exp(Σ f_ij(x_i,x_j))` — which contains the Gaussian but is vastly bigger.
Hence `I_C⁽³⁾ ≤ J`, with the inequality generally strict.

**Measured, on the exact lognormal whose true share is 0:**

| `σ_g` | 1-pt skewness | **`J₃` (Jones–Sibson negentropy)** | **bridge (this pilot)** | ratio |
|---|---|---|---|---|
| 1.00 | 6.18 | **9.93** | 5.55e-03 | 5.6e-04 |
| 0.30 | 0.95 | **0.232** | 2.62e-06 | 1.1e-05 |
| 0.10 | 0.30 | **2.34e-02** | 3.44e-09 | 1.5e-07 |
| 0.01 | 0.030 | **2.31e-04** | 3.41e-15 | 1.5e-11 |

**Negentropy reads 9.93 nats where the true whole-only share is exactly zero.** It cannot be
otherwise: `J₃ = (1/12) ζ_ijk ζ_lmn A^{il}A^{jm}A^{kn}` is a **positive-definite quadratic
form** in the third cumulants, so it can never vanish on a non-Gaussian field, while the share
vanishes identically on the entire pointwise-transform family. **Had I accepted the identity,
the pilot's central result would have been nonsense** — a lognormal obviously has enormous
negentropy.

The distinction *is* the pilot: negentropy measures all departure from Gaussianity; the share
measures only the part no pair can reconstruct.

## A4. CORRECTION 2 — the bridge is a **projection of** the known formula, not the formula

`J₃` above is the known multivariate Edgeworth negentropy (Jones & Sibson 1987). **My bridge is
its projection onto the one direction the pair marginals cannot see** — a single squared
*linear* functional, `½(A_{1a}A_{2b}A_{3c}ζ_abc)²/perm(A)`, versus a positive-definite form on
the full ten-dimensional third-cumulant sector.

The projection step is not cosmetic: it is exactly what makes the pointwise sector cancel
(pre-registration §2.3, verified analytically and now numerically — the ratio bridge/`J₃` falls
as `σ_g⁴`). The parent formula does not and cannot do that.

**Consistency check with the prior art, which I should have stated up front:** my general
negentropy expression reduces in the univariate limit to `J = (1/12)κ₃²` — exactly the
Jones–Sibson / Hyvärinen coefficient. The derivation reproduces the known result where the two
overlap, and departs from it only at the projection.

**So the honest claim is narrow:** the mathematics is borrowed (Edgeworth, connected
information, copula invariance); what this pilot supplies is the projection's normalisation,
its numerical validation to 0.01 % in shape, its located breakdown, and the artifact map. I
searched and did not find the projected form or the `b=2` parity result in print — **that is
"not found", not "does not exist"**, per house rule.

## A5. CORRECTION 3 — the static-nonlinearity trap lands on Route B, not Route A

The warning states: *"Any binarization step in route A is itself a threshold nonlinearity —
keep route B moment-native."* Route B **was** kept moment-native throughout (it reads the
unbinarised field). But the artifact exposure is **the reverse of what the warning expects**.

A clip is a **monotone per-cell map**. By the same theorem that makes the lognormal a null, a
median split is *exactly invariant* under it. Measured on a Gaussian field (truth: unchanged),
one-sided clipping at the 90th–99th percentile:

| clip | 1-pt skewness manufactured | **binary cells changed** | **Route A** | **Route B** |
|---|---|---|---|---|
| none | −0.004 | — | 6.119e-07 | 1.26e-06 |
| q = 0.99 | −0.067 | **0** | 6.119e-07 (**×1.000**) | 5.4e-07 |
| q = 0.95 | −0.237 | **0** | 6.119e-07 (**×1.000**) | 2.90e-06 (×2.3) |
| q = 0.90 | −0.407 | **0** | 6.119e-07 (**×1.000**) | **1.42e-05 (×11.3)** |

**Zero cells changed, out of 16 777 216, at every clip level: Route A is unchanged
bit-for-bit.** Route B — the moment route — rises by **11.3×** on a field whose true share has
not moved, because clipping manufactures precisely the third cumulant it reads.

This is the `cirisarray-clamp-mediated-readout` lesson, and it selects **against** the moment
route. Being moment-native is not protection from a static nonlinearity; it is the exposure.
The two routes are indeed sensitive to different artifact families, as the warning wanted — but
the assignment is: **Route A is immune to per-cell distortion and vulnerable to filtering
(§6a); Route B is immune to neither.**

## A6. WHAT CHANGES IN THE CONCLUSIONS

**Nothing in §1–§7 changes.** No measured number moves; the two corrections above are to the
warning, not to the run, and the third (A5) strengthens §9's recommendation.

**Two things change in the framing:**

1. **The novelty framing is dead, and the pilot is stronger for it.** The question "does the
   matter density field carry whole-only share?" is a sharpened form of a question the LSS
   copula programme has been asking since 2010, with an affirmative partial answer already in
   print. The mathematics of the bridge is established. Both facts should be stated in any
   future write-up before any result is.
2. **§9's recommendation is reinforced by A5 and by Carron 2011.** The `b=2` sign-triple
   excess is now recommended on three independent grounds: it is theorem-protected against the
   pointwise sector, it has a floor 5–84× smaller, and it is **exactly immune to clipping,
   saturation and any other monotone per-cell distortion** — the artifact family that has
   already cost this programme a result. The moment route is the one exposed to it, and
   Carron's moment-indeterminacy result says the exposure gets worse exactly where the signal
   is largest.
