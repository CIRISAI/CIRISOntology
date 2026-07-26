# PRE-REGISTRATION — can a survey measure gravity's whole-only share? A forecast

Frozen and committed **before** `sky_forecast.py` existed and before any number in it was
computed. Scratchpad only: no Lean file, no `Stance.lean`, no audit, `lake` never run.
**No real survey data is touched anywhere in this experiment, and nothing here will be a
claim about the sky.**

Successor to `SKY_PILOT_PREREG.md` / `SKY_PILOT_RESULTS.md` (pilot committed at `49c50de`,
addendum at `e601aec`). The pilot validated the instrument. This forecasts what it would
read on a gravitationally evolved field, on **mocks I generate myself**.

---

## 0. SCOPE, FIRST AND LOAD-BEARING

This is a **forecast on my own mocks**. Every field is one I generate. The deliverable is a
**go/no-go for a real-data pre-registration** — not a result about the sky, not a
cosmological constraint, not an entry in the stance under any outcome.

Second-order perturbation theory is the **leading-order** gravitational prediction. It is
not full N-body. Everything below is therefore a **lower anchor**: it says what the leading
gravitational three-point structure delivers, and a real field has more. Where the forecast
says "not detectable", that verdict is only as strong as the lower anchor; where it says
"detectable", the higher-order terms can only help — so the asymmetry runs in the safe
direction for a go decision and in the unsafe direction for a no-go. **A no-go from this
forecast is a no-go for the leading order only, and must be stated that way.**

---

## 1. THE QUESTION, AND WHY THE ANSWER IS A DIFFERENCE

`Stance.lean`'s open claim `wild-share` asks whether any of nature's wild (unengineered)
processes carry whole-only pattern. Gravitational clustering is the largest wild process
there is, and it has a survey-measurable field. So: **does the matter density field carry
whole-only order-3 share, above what a pointwise transform of a Gaussian field already
manufactures?**

The second clause is the whole difficulty, and the pilot is why. Three facts from it fix
this design:

1. **`Core/SignSymmetry.lean` + the pilot's §4**: any per-cell monotone transform of a
   Gaussian field has **exactly zero** whole-only share at `b=2`. The lognormal — the
   standard non-Gaussian mock, with a large bispectrum — reads 0 to the last bit.
2. **The pilot's §6(a), unanticipated and the most consequential finding in it**: a
   **filter applied after** a pointwise map converts that exact zero into a **66 σ**
   detection. Cosmology always filters (window, mass assignment, redshift binning,
   selection). Any pipeline that smooths a transformed field is in that regime.
3. **The Kahle mixture lesson** (`ECA_SPIKE_RESULTS.md` correction block): convex
   combinations manufacture higher-order structure from none. **Poisson sampling of a
   density field is a per-cell stochastic map, hence a mixture**, hence a suspect.

So the raw share of a gravity mock is not the answer. The answer is the **gap**:

> **GAP := (gravity mock's reading) − (pointwise-transform mock at matched `P(k)`, run
> through the identical pipeline).**

If the gap is zero, this instrument cannot tell gravity from a local transform, and the sky
route to `wild-share` closes.

---

## 2. THE FIELDS

Cosmology fixed now: `Ω_m = 0.31`, `Ω_b = 0.048`, `h = 0.68`, `n_s = 0.96`, `T_cmb = 2.7255`,
Eisenstein–Hu no-wiggle transfer function (the pilot's `eh_nowiggle_T`), linear field
normalised to `σ_8 = 0.81` (top-hat, 8 Mpc/h) at `z = 0`, growth `D = 1`, EdS second-order
coefficient `D₂ = −(3/7) D₁²`.

### 2.1 Gravity, arm G1 — 2LPT with particles (the realistic mock)

Standard second-order Lagrangian perturbation theory (Buchert 1994; Bouchet et al. 1995;
Scoccimarro 1998; Crocce, Pueblas & Scoccimarro 2006 — credited, nothing here is new):

    ∇²ψ⁽¹⁾ = δ₁ ,    ∇²ψ⁽²⁾ = Σ_{i<j} [ ψ⁽¹⁾_,ii ψ⁽¹⁾_,jj − (ψ⁽¹⁾_,ij)² ]
    x = q − D₁ ∇ψ⁽¹⁾ − (3/7) D₁² ∇ψ⁽²⁾

one particle per grid cell, CIC deposit back to the same grid. **Second order is exactly
the order at which gravity's three-point structure first appears**, so this mock carries the
leading gravitational bispectrum by construction. 1LPT (Zel'dovich, second term dropped) is
run alongside as arm **G0**.

### 2.2 Gravity, arm G2 — Eulerian second-order PT, with the sector split

The same physics on the Eulerian grid, where the `F₂` kernel separates into three terms
that can be switched on one at a time:

    F₂ = 17/21 + (1/2)μ(k₁/k₂ + k₂/k₁) + (2/7)(μ² − 1/3)
    δ⁽²⁾ = (17/21) δ₁²   +   ∇ψ·∇δ₁   +   (2/7) s_ij s_ij
             LOCAL             SHIFT          TIDAL

with `s_ij = (∂_i∂_j∇⁻² − δ_ij/3) δ₁`. This arm exists to answer *which sector the share
comes from*, which the particle arm cannot:

* **LOCAL** is `δ₁ + c δ₁²` — a **pointwise** map of `δ₁`, monotone wherever
  `1 + 2cδ₁ > 0`, i.e. `δ₁ > −21/34 = −0.618`. By the theorem its contribution is
  **zero up to the non-monotone tail**, and that tail fraction will be reported. This is a
  pre-registered near-null, not an assumption.
* **SHIFT** and **TIDAL** are non-local. They are where any genuine gravitational
  whole-only share must live.

**Interpretive stake, fixed now**: the non-pointwise sector is **SHIFT + TIDAL together**.
The question `wild-share` asks is *existence*, not novelty-of-mechanism, so if either term
carries share, that counts as a YES. The sector split is reported so a reader can see which
one it was.

### 2.3 The pointwise floors (control (a) of the brief, sharpened)

All three are built from the **same white noise** as the gravity arms, so the comparison is
paired at the mode level and cosmic variance largely cancels.

| arm | construction | true pre-filter share |
|---|---|---|
| **F0 — phase-randomised** | Gaussian field with the gravity arm's `P(k)`. This is what real-sky practice uses as its null. | **exactly 0**, by `share_eq_zero_of_signSymmetric` |
| **F1 — lognormal** | `T(g) = exp(g − σ_g²/2) − 1`, with `P_g` tuned so `T(g)` has the gravity arm's `P(k)`. The brief's requested floor. | **exactly 0** (monotone per-cell map) |
| **F2 — rank-matched** | `T(g) = Q_grav(Φ(g/σ_g))`, `Q_grav` the empirical quantile function of the gravity field. Matches the gravity arm's **one-point law exactly** *and* its `P(k)`. | **exactly 0** (monotone per-cell map) |

**F2 is the primary floor and F1 is secondary**, and here is why, stated before the numbers:
the manufactured share of §1(2) is driven by the *strength of the pointwise nonlinearity*,
and F1's is set by the lognormal's own skewness, which is not gravity's. F2 has the same
one-point law as gravity by construction, so it removes the objection "the gap is only
because the two fields have different skewness". F1 is reported because the brief asked for
it and because it is the standard mock.

`P_g` for F1 and F2 is tuned by fixed-point iteration on the **spectrum**
(`P_g ← P_g · P_target/P_measured`) with the white noise held fixed. Iterating on the
spectrum and not on the realisation is deliberate: it keeps the output **exactly** of the
form `T(Gaussian)`, so the zero-share theorem still applies. (This is *not* IAAFT; IAAFT's
rank-and-refit iteration destroys that property, and `temporal-share-realdata-nulls` already
records that IAAFT survival is not sufficient evidence of anything.)

### 2.4 Shot noise (the mixture gate)

`n(x) ~ Poisson(n̄ V_cell (1 + δ))` with `1+δ` clipped at 0, then `δ_obs = n/(n̄V_cell) − 1`,
then the identical pipeline. Densities `n̄ ∈ {1e-4, 3e-4, 1e-3, 3e-3, 1e-2} (h/Mpc)³`, the
DESI-like range.

**Why this is a gate and not a nuisance.** Given `δ`, the counts in separated cells are
independent, so the observed triple's law is a **mixture of product laws** — the Kahle
mechanism. Concretely, at leading order the bridge reads
`A_{1a}A_{2b}A_{3c} ζ_abc`, and Poisson noise contributes a **diagonal-only** third cumulant
`ζ_iii ≠ 0`, whose contraction `Σ_i A_{1i}A_{2i}A_{3i} ζ_iii` is generically **nonzero**.
Adding independent per-cell noise is not a pointwise transform, so no theorem protects it.

### 2.5 The pipeline, identical for every arm

grid field → Gaussian smoothing at `R` → **median split** (`b=2`, the one binning with a
theorem under it) → sign triples at pre-declared geometries → the pilot's exact `b=2` solver
`share3_ref` and its signed excess.

---

## 3. THE STATISTIC

Two numbers per (arm, `R`, geometry), both from the pilot's validated `b=2` machinery:

* **`E` — the signed sign-triple excess.** `E = ⟨s₁s₂s₃⟩_measured − ⟨s₁s₂s₃⟩_pairwise-maxent`
  (the pilot's `route_B2` `dtau`). **`E` is the primary forecast statistic**: it is linear
  in the histogram, so it is approximately unbiased and approximately Gaussian, its error
  falls as `1/√V`, and its sign is informative. A biased-upward positive quantity cannot be
  forecast honestly; `E` can.
* **`I` — the share in nats** (`share3_ref`), the ontology's quantity, `I ≈ E²·(Σ1/q)/128`.
  Positive-definite and upward-biased; reported alongside, never used for the significance.

**GAP := E_gravity − E_floor**, per realisation, paired on white noise.

Two significances, both reported, and they answer different questions:

* **paired** `z_p = mean(GAP)/SEM(GAP)` over realisations — "is the gap real, given the same
  phases". This is the model-comparison question.
* **survey** `z_s = mean(GAP)/σ_V(E_gravity)` where `σ_V` is the realisation-to-realisation
  scatter of `E_gravity` scaled to survey volume by `√(V_box/V)` — **this is the forecast
  number**, because a real survey has one universe and a modelled floor. `V_DESI = 20
  (Gpc/h)³ effective`.

---

## 4. GEOMETRY AND SCALE

`R ∈ {10, 15, 25, 40, 60, 100, 150}` Mpc/h. Triple side scale `r ∈ {1.5R, 3R}`.
Four geometries, each pooled over 3 lattice orientations, sides given as multiples of `r`:

| name | displacements | sides |
|---|---|---|
| **equilateral** | `(r,0,0)`, `(r/2, r√3/2, 0)` rounded to the lattice | `≈ (r,r,r)` |
| **folded** (collinear) | `(r,0,0)`, `(2r,0,0)` | `(r,r,2r)` |
| **orthogonal** | `(r,0,0)`, `(0,r,0)` | `(r,r,r√2)` |
| **squeezed** | `(r/4,0,0)`, `(0,r,0)` | `(r/4, r, ≈r)` |

**Pre-registered geometry prediction.** The tidal term `(2/7)(μ²−1/3)` is smallest at
equilateral (`μ = −1/2` ⟹ `μ²−1/3 = −1/12`) and largest at folded and squeezed
(`|μ| = 1` ⟹ `2/3`). So I predict **`|GAP|` largest at folded/squeezed and smallest at
equilateral.** If instead equilateral is largest, the gap is not the tidal term and I must
say what it is.

---

## 5. GATES — all must pass before any forecast number is reported

| # | test | threshold |
|---|---|---|
| **GA** | the pilot's `b=2` machinery re-validated here: parity → `ln 2`; independence → 0; 2000 random sign-symmetric states → 0 | `< 1e-12` |
| **GB** | **stride convergence**: sign moments on a strided sub-lattice vs the full grid | `|ΔE| <` 2 % of `E`, at every stride used |
| **GC** | **the theorem on this pipeline**: floor field **before** the final smoothing has a sign pattern bit-identical to its parent Gaussian | **0** differing cells of `N³` |
| **GD** | `P(k)` match, gravity vs each floor, over the `k` range the smoothing keeps (`kR ≤ 2`) | max frac. dev `< 3 %` |
| **GE** | the **linear** Gaussian field through the full pipeline reads zero | `|E| <` its own realisation scatter, at every `R`, every geometry |
| **GF1** | real-space `δ⁽²⁾` equals a **brute-force `F₂` convolution** in Fourier space on a `16³` grid | rel. `< 1e-5` |
| **GF2** | the particle/CIC 2LPT pipeline reproduces `εδ₁ + ε²δ⁽²⁾` as `ε → 0`, residual scaling as `ε³` | fitted exponent `3.0 ± 0.3` |
| **GF3** | 2LPT `P(k)/P_lin → 1` at low `k`, `> 1` at high `k` | qualitative, logged |
| **GG** | Poisson gate returns to the F0 floor as `n̄ → ∞` | monotone in `n̄`, → floor |

**GA, GB, GC, GE, GF1, GF2 failing ⟹ VOID.** GD failing ⟹ the floor is not matched and the
gap is uninterpretable. GF3 and GG are diagnostics.

---

## 6. PREDICTIONS — every possible answer, and what each would mean

| # | prediction | reasoning | if it fails |
|---|---|---|---|
| **F1** | `E_gravity ≠ 0` and above the F0 floor at `R ≤ 40` | the shift term is a coordinate remap, manifestly non-pointwise | gravity's leading order carries no whole-only share at all — a strong and surprising negative |
| **F2** | `d log|E_gravity| / d log σ_R = 1.0 ± 0.3`; `d log I / d log σ_R = 2.0 ± 0.5` | tree-level reduced skewness `S₃` is scale-free, so the dimensionless third cumulant `≈ S₃σ_R`; the share is quadratic in it | the amplitude scaling is not the weak-coupling one; the perturbative reading is wrong |
| **F3** | at fixed `R`, `E ∝ D` (growth): halving `D` (i.e. `z ≈ 1`) halves `E` | same argument | as F2 |
| **F4** | **LOCAL-only** sector reads `≈ 0`, at the level set by its non-monotone tail fraction | pointwise theorem | the theorem is misapplied to this construction — I must find where |
| **F5** | **GAP ≠ 0**; specifically `|GAP| / E_gravity > 0.1` at `R ≤ 40` | the tidal term is nonzero and has no pointwise counterpart | see the trichotomy below |
| **F6** | `|GAP|` largest at folded/squeezed, smallest at equilateral | §4 | the gap is not the tidal shape |
| **F7** | **Poisson shot noise creates share** on an exact-zero field, rising as `n̄` falls, and suppressed at large separation (it enters only through `Σ_i A_{1i}A_{2i}A_{3i}ζ_iii`, which needs two nonzero off-diagonal correlations) | §2.4 | shot noise is benign — good news, and it would mean the mixture worry does not reach this estimator |
| **F8** | detection significance of the gap rises steeply toward small `R`, `z_s ∝ √V · R^{-2 …-2.5}` | signal `∝ σ_R ∝ R^{-0.75}`, noise `∝ R^{1.5}/√V` | the scale dependence is not the mode-counting one |

### The trichotomy, decided in advance (the brief's §5)

| outcome | criterion | what we conclude, and it is binding |
|---|---|---|
| **(a) GO** | `z_s ≥ 5` for `V = 20 (Gpc/h)³` at some `R` where the pointwise floor is trustworthy | **A real-data pre-registration is warranted.** `wild-share` gets its first decidable instance: does gravitational clustering carry whole-only pattern beyond the pointwise sector. Warranted ≠ done: the real prereg must still forward-model window, RSD, selection and shot noise, each of which §1(2) says can manufacture the signal. |
| **(b) VALID BUT TOO SMALL** | GAP survives the paired test (`z_p ≥ 5`) but `z_s < 5` at `V_DESI` | **Instrument valid, universe too small.** `wild-share` stays open, honestly, with the required volume quoted. |
| **(c) NO-GO** | GAP consistent with zero (`|z_p| < 3`) at every `R` and geometry | **At leading order, gravity is indistinguishable from a local transform in this basis.** The sky route to `wild-share` closes and we say so. Scoped by §0: leading order only. |

**Which I expect, and why.** **(a) at `R ≤ 40` Mpc/h, (b) at `R ≥ 100`.** The `F₂` tidal
term is nonzero at every triangle except the one where `μ² = 1/3`, and the shift term is a
coordinate remap that no per-cell map can imitate — so the gap should not be zero. The
uncertainty is entirely in **amplitude**, and specifically in whether the pointwise floor's
*manufactured* share (§1(2), a 66 σ effect in the pilot) is comparable to or larger than
gravity's genuine one. That is the number this forecast exists to produce. Outcome (c) is
live and I will report it as plainly as (a).

---

## 7. SIZES, AND THE FALLBACK LADDER

Target: `N = 512`, `L = 2000` Mpc/h (cell 3.906, `V = 8 (Gpc/h)³`), `n_real ≥ 6`,
CPU FFT (`scipy.fft`, threaded). GPU is shared with sibling agents and is not assumed.

Fallback if compute-bound, in this order, each recorded in the results:
`n_real` down to 4 → `N = 384, L = 1500` → drop `r = 3R` → drop `R = 150`.
**Whatever is actually run is what gets reported**, with the reduction named.

---

## 8. WHAT THIS CANNOT DELIVER, WRITTEN DOWN NOW SO IT CANNOT BE CLAIMED LATER

1. **Nothing about the sky.** No survey data, no catalogue, no cosmological parameter, no
   claim about nature. Every field is mine.
2. **No stance change under any outcome.** Not even outcome (a). `wild-share` stays open;
   what (a) buys is permission to *write a real-data pre-registration*, and that document
   would still need a refuter pass and Eric's review.
3. **Leading order only.** 2LPT and second-order Eulerian PT are not N-body. A no-go here is
   a no-go for the leading order, and the honest next step under (c) would be an N-body
   check, not a closure.
4. **No priority claim.** 2LPT, the `F₂` decomposition, lognormal mocks, rank-matched
   mocks and the copula framing are all standard and credited in §2. The pilot's addendum
   already records that the LSS copula programme (Scherrer et al. 2010; Qin, Yu & Zhang
   2020) asked the qualitative question first.
5. **The forecast's floors are mocks too.** "Gravity minus pointwise" is a difference of two
   fields I built. On real data the floor must be forward-modelled from the actual window,
   mask, selection and mass assignment, and §1(2) says that model is the dominant systematic,
   not a correction.
6. **Redshift-space distortions, survey geometry, mask and selection are absent.** All four
   are filters, and §1(2) is about filters. Their omission makes this forecast optimistic in
   a way that is not quantified here.

---

*Pre-registration ends here. Nothing below this line existed when it was committed.*
