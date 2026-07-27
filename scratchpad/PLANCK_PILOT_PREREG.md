# PRE-REGISTRATION — the Planck/WMAP plumb line

**An instrument-validation pilot on public CMB maps. NOT a cosmology result. NOT an anomaly
search. Nothing here bears on `wild-share` and nothing here goes near `Stance.lean`.**

Written and committed **before any share is computed on either map.** The only numbers below
that came off the data are the FITS-header inventory of §1 and the one-point statistics quoted
there (npix, nside, units, mask fraction, map mean/std/skewness) — none of which is a reading of
the target statistic, and all of which were needed to design the run. No triple has been
histogrammed, no 2×2×2 table has been built, no `share` has been called on a Planck or WMAP
pixel value.

Registry: `scratchpad/TARGET_REGISTRY.md` §4.2 ranks this **rank 2, THE PILOT** — scored **C on
"blind shape"** (weak as a discovery target) and **A on baseline, theorem, data, prior art and
cost** (unbeatable as a plumb line). Row 12 of the same table records the adjacent target this
campaign is explicitly **not** running: the CMB anomalies (hemispherical asymmetry, low-`ℓ`
alignments, Cold Spot, lensing) are claims about **statistical isotropy**, and our instrument
does not address them. If this document or its successor drifts into anomaly-hunting, that is a
scope failure and should be called as one.

---

## 0. WHAT THIS IS FOR, IN ONE PARAGRAPH

Standard cosmology predicts the CMB temperature field is **Gaussian**. A Gaussian field split at
its own median gives a three-bit state invariant under the global sign flip, and
`share_eq_zero_of_signSymmetric` (`CIRISOntology/Core/SignSymmetry.lean`, machine-checked) says
such a state has whole-only share **exactly zero** — no hypothesis on the pair correlations, the
beam, the noise level or the sky cut. So this is the best available end-to-end test of **our own
instrument** on **real sky data with a theorem-pinned answer**. It must read zero. **Any
significant nonzero reading is our pipeline, not the universe**, and is to be treated as a
pipeline defect until proven otherwise. The deliverable is instrument validation and the filling
of `GATES.md` cells, not a discovery.

---

## 1. THE DATA — inventory, read off the files on this machine (2026-07-27)

| file | bytes | what it is |
|---|---|---|
| `/home/emoore/coherence-ratchet/experiments/cmb_books/data/smica_2048.fits` | 2 013 312 960 | Planck **COM_CMB_IQU-smica_2048_R3.00_full**. `PIXTYPE=HEALPIX`, `ORDERING=NESTED`, `NSIDE=2048` (50 331 648 px), `COORDSYS=GALACTIC`, `METHOD=SMICA`, `DATE=2018-04-10`, `BAD_DATA=-1.6375e+30` |
| `/home/emoore/coherence-ratchet/experiments/open_system_pomega/cmb_data/planck_smica_R3.fits` | 2 013 312 960 | **the same file.** Identical HDU structure, identical 67-card HDU-1 header, identical column set. Treated as one map; **not** used as an independent replicate |
| `/home/emoore/coherence-ratchet/experiments/open_system_pomega/cmb_data/wmap_ilc_9yr_v5.fits` | 25 174 080 | WMAP 9-yr **ILC**, `RELEASE=DR5`, `VERSION=PASS 5`, `RESOLUTN=9` → `NSIDE=512` (3 145 728 px), `ORDERING=NESTED`, `SKYCOORD=Galactic`, `FREQ=K-W bands combined`, `STOKES=Intensity` |
| `…/cmb_books/data/planck_bestfit_theory.txt` | 205 647 | Planck best-fit theory spectra, `# L TT TE EE BB PP`, `ℓ = 2…2508`, TT in `μK²` as `D_ℓ = ℓ(ℓ+1)C_ℓ/2π` |

**SMICA HDU 1** carries ten columns: `I_STOKES, Q_STOKES, U_STOKES, TMASK, PMASK, I_STOKES_INP,
Q_STOKES_INP, U_STOKES_INP, TMASKINP, PMASKINP`, all `1E` (float32), units `K_CMB` for the Stokes
columns and dimensionless for the masks. **SMICA HDU 2** carries `INT_BEAM` and `POL_BEAM`,
`LMIN=0`, `LMAX_I=LMAX_P=4096`.

**Masks are bundled — no external fetch is required.**

* `TMASK` is exactly binary, `unique = {0, 1}`, **f_sky = 0.842409** (42 397 229 unmasked pixels).
* `TMASKINP` is exactly binary, **f_sky = 0.984922** — the inpainted-map confidence mask.
* Verified: **zero** `BAD_DATA` sentinels in `I_STOKES` and zero in `I_STOKES_INP`.

One-point statistics, read off the files (needed to fix thresholds and noise amplitudes; not a
reading of the target):

| quantity | Planck `I_STOKES` | Planck `I_STOKES_INP` | WMAP `TEMPERATURE` |
|---|---|---|---|
| min / max | −5.755e−03 / +7.899e−03 K | −5.291e−04 / +5.510e−04 K | −0.4525 / +0.4422 mK |
| mean (full sky) | −2.87e−13 K | — | +2.039e−03 mK |
| std (full sky) | 1.0837e−04 K | 1.0757e−04 K | 7.106e−02 mK |
| mean / std / median **inside `TMASK`** | 3.732e−07 / 1.0769e−04 / 5.530e−07 K | — | — |
| one-point skewness | −0.01308 (inside `TMASK`) | — | −0.09017 (full sky) |

`INT_BEAM`: `b_0 = b_1 = 0` (monopole and dipole zeroed by construction), `b_2 = 1.000276`,
`b_2000 = 0.46560`, `b_4096 = 2.986e−03`.

**WMAP `N_OBS` is identically 1.0 on every pixel** — the ILC is a linear band combination and
carries no hit count. Consequence, stated in advance: WMAP's noise anisotropy is **not**
recoverable from this file, and no noise-weighting is attempted. The WMAP 9-yr ILC is delivered
smoothed to **1° FWHM**; every WMAP reading below that scale is beam-dominated and is declared as
such rather than dropped (see §4.1 — the beam-dominated rungs are deliberately retained as the
near-degenerate stress case for the solver gate).

**Units are irrelevant to the target and this is a theorem, not a convenience.** The b=2 share is
invariant under any strictly monotone pointwise map applied slot-wise (`share-is-not-negentropy`;
Sklar 1959). Planck in `K_CMB` and WMAP in `mK` therefore need no unit conversion, and none is
performed. The b≥3 quantile binning is likewise scale-free.

---

## 2. THE TARGET STATISTIC

For a triple of pixels at a declared angular template, let each pixel carry one label = its own
temperature coarse-grained to `b` levels. `share = S(Q) − S(P)`, where `P` is the empirical joint
on the `b³` cells and `Q` is the maximum-entropy distribution carrying all three of `P`'s pair
marginals. This is the **order-3 connected information** (Schneidman, Still, Berry & Bialek,
PRL **91**:238701 (2003); Amari 2001). `share ≥ 0` always, because `Q` maximises entropy over a
set containing `P`.

**b = 2 — the theorem-pinned rung, and the only one that is.** Exact 1-D solver
`scratchpad/dalitz_share.py::share_2x2x2`: the fibre of distributions carrying `P`'s three pair
marginals is the one-parameter family `p + δ·Σ` along the parity character, entropy is strictly
concave along it, and the maximiser is found by 200 bisections to machine precision. **No IPF is
used at b = 2** (`ipf-sharek-boundary-drift`).

**b ≥ 3 — NOT theorem-pinned, and this is pre-registered before it can be mistaken for a
result.** For `b ≥ 3` the fibre has dimension `(b−1)³ > 1` and the sign-symmetry argument does
not close: a discretised Gaussian at `b ≥ 3` has **genuinely nonzero** order-3 connected
information (`binning-and-filter-traps`: a pure Gaussian reads 2.4e−3 nats at `b ≥ 3`). **At
`b ≥ 3` the reference is not zero — it is the surrogate's own reading**, and only the
*differential* `share(data) − share(surrogate)` is interpretable. Any absolute `b ≥ 3` number in
the results document that is not accompanied by its surrogate value is a reporting error.

**The threshold.** One **common** threshold across the three slots, equal to the median of the
pooled values of all three slot arrays for that template and that map. A per-slot threshold is
**not** used: the theorem is about the joint distribution's symmetry centre, and three separate
estimates of one centre would add three sources of asymmetry for no gain. Secondary, declared
now and reported alongside: the **zero-threshold** variant (`τ = 0` for Planck, `τ = ` the map
mean for WMAP, which carries a +2.04e−03 mK offset). At `b ≥ 3` the cut points are the pooled
`b`-quantiles.

---

## 3. THE PIPELINE, STEP BY STEP

Every step below is applied **byte-identically** to the data map and to every surrogate. The
index arrays `(i₁, i₂, i₃)` are computed **once per template** from the geometry and the mask,
and reused unchanged for the data and all surrogates. This is the load-bearing construction: it
makes the selection function exactly common, so any selection effect cancels in the differential
and appears identically in the floor.

1. **Read** `I_STOKES` (Planck) or `TEMPERATURE` (WMAP), and `TMASK`. Reorder `NESTED → RING`
   once; all subsequent work is in RING.
2. **No smoothing and no degrading in the primary analysis.** The map is read at its native
   `NSIDE` with its native beam. **Smoothing is a filter and filters manufacture share** — the
   sky pilot took an exact zero to a **66 σ** detection with a linear filter applied after a
   pointwise map (`SKY_REALDATA_PREREG.md` §1.3, `SKY_REALDATA_RESULTS.md` §6 item 2), and
   `Core/Creation.lean` covers only *per-cell* maps, so no no-creation theorem protects against
   it. The primary run therefore adds **no** filter the instrument did not already apply.
   *Declared secondary* (§6.4): `ud_grade` to `NSIDE = 512` and `256`, which is a top-hat filter
   over 16 and 64 pixels, applied identically to data and surrogate, **with its effect measured
   and reported** rather than assumed harmless.
3. **Anchors.** `N_draw = 4 000 000` pixels drawn uniformly with replacement from the unmasked
   pixel list, `numpy.random.default_rng(20260727)`. A random azimuth `ψ ∈ [0, 2π)` per anchor
   from the same generator. The **same** anchors and azimuths are used for every template, so
   templates are compared on a common sample.
4. **Triple construction.** For anchor direction `n̂` with local right-handed frame
   `(ê₁, ê₂)` rotated by `ψ`, and template `(θ₁₂, θ₁₃, θ₂₃)`:
   `p₁ = n̂`; `p₂ = n̂ cos θ₁₂ + ê₁ sin θ₁₂`;
   `p₃ = n̂ cos θ₁₃ + (ê₁ cos φ + ê₂ sin φ) sin θ₁₃` with
   `cos φ = (cos θ₂₃ − cos θ₁₂ cos θ₁₃)/(sin θ₁₂ sin θ₁₃)`, `φ = +arccos(·)`.
   **Fixed chirality**, declared: `φ ≥ 0` always. The share is invariant under slot permutation
   and the random azimuth removes any preferred Galactic direction, so the chirality choice
   cannot introduce a directional artifact; it is declared because it is a choice.
5. **Retention.** A triple is retained iff **all three** pixels are unmasked. `N_kept` is
   reported per template. Expected `N_kept ≈ 0.71 × N_draw` at `f_sky = 0.842`.
6. **Read, threshold, histogram.** Gather the three slot values, form the common threshold or
   quantile cuts, bincount into `b³` cells.
7. **Solve.** `share_2x2x2` (exact) at `b = 2`; IPF at `b ∈ {3,4}` with the certificate of §5.

---

## 4. THE LADDERS

### 4.1 Geometry ladder — twelve templates, three families, five decades of scale

Pairwise separations in arcminutes. **The full lag-pair grid, never only the equally-spaced
diagonal** (`order3-probe-geometry`: the equally-spaced probe is provably blind to maximal
permanent temporal order-3, and the same argument applies to a fixed equilateral-only scan).

| family | id | `(θ₁₂, θ₁₃, θ₂₃)` | regime |
|---|---|---|---|
| **equilateral** | `E008` | (8, 8, 8) | close — sub-beam for WMAP, ~1.6× beam for Planck |
| | `E016` | (16, 16, 16) | close |
| | `E032` | (32, 32, 32) | intermediate |
| | `E064` | (64, 64, 64) | intermediate — 1°, WMAP's beam scale |
| | `E128` | (128, 128, 128) | wide |
| | `E256` | (256, 256, 256) | wide — 4.27°, first acoustic peak scale |
| **folded** (collinear) | `F016` | (16, 16, 32) | close |
| | `F064` | (64, 64, 128) | intermediate |
| | `F128` | (128, 128, 256) | wide |
| **squeezed** | `S064` | (8, 64, 64) | intermediate, one short leg |
| | `S128` | (16, 128, 128) | wide, one short leg |
| | `S256` | (32, 256, 256) | wide, one short leg |

Folded is exactly degenerate (`cos φ = −1`, `φ = π`) and is retained deliberately: it is the
configuration in which the sky campaign's readings were largest and its coarse-graining
manufacture smallest (7–29 % folded vs 47–60 % equilateral), so it is the configuration a
pipeline defect is most likely to show up in.

**Both instruments run all twelve.** WMAP's sub-beam rungs (`E008`, `E016`, `F016`, and the short
legs of the squeezed family) produce **near-degenerate** slot pairs — three almost-identical
values — and near-degeneracy is precisely where `ipf-sharek-boundary-drift` measured IPF
overstating the share by five orders of magnitude and where `GATES.md` reach 12 reads
**UNVERIFIED in the interior**. They are kept as the stress case, not dropped as inconvenient.

### 4.2 Binning ladder

`b ∈ {2, 3, 4}`. Occupancy gate: **every** cell must hold `> 100` counts or that `(template, b)`
is **ungauged** and is reported as such, never as zero (`GATES.md` reach 11; `8b0c108`). At
`b = 4`, 64 cells against `N_kept ≈ 2.8e6` gives an expected `~4.4e4` per cell; the gate is
expected to pass everywhere and its purpose is to be on the record if it does not.

### 4.3 The primary grid, and its size, fixed now

**12 templates × 3 `b` × 2 instruments = 72 primary cells.** Everything else in this document is
declared secondary and is not counted in the primary test of §7.

---

## 5. THE SURROGATES

**S1 — phase randomisation, primary.** `map2alm` of the **inpainted** map (`I_STOKES_INP` for
Planck, `TEMPERATURE` for WMAP — WMAP ships no inpainted variant, so its full sky including the
Galactic plane enters the surrogate's `C_ℓ`; declared, and the conservative-mask arm of §6.3 is
the check on it), `lmax = 3·NSIDE − 1` (6143 for Planck, capped at 4096 where the beam is
defined; 1535 for WMAP). Each `a_ℓm` keeps its modulus and takes a uniform random phase, subject
to the reality condition `a_{ℓ,−m} = (−1)^m a*_{ℓm}`; `a_{ℓ0}` takes a random sign.
`alm2map` back to the same `NSIDE`.

**This preserves the measured `C_ℓ` exactly, mode by mode** — it is the standard CMB surrogate,
it manufactures every pair correlation the data has, and by `share_eq_zero_of_signSymmetric` its
b=2 share is zero. It satisfies `GATES.md` reach 3 (mixture/manufacture): a null that cannot
produce the data's pair structure gauges nothing, and this one reproduces it bit for bit.

**S2 — Gaussian realisation at the measured `C_ℓ`, secondary and independent in construction.**
`synfast` from the `C_ℓ` of the same inpainted map. S1 fixes `|a_ℓm|` and randomises phase; S2
randomises both. **Two defensible null constructions, and the spread between them is a quoted
systematic, not a footnote** — this is the harvest gate *null-construction sweep*, whose
known-bad anchor is refuter A9 (`711ab65`).

**S3 — theory realisation, declared and diagnostic only.** `synfast` from
`planck_bestfit_theory.txt` TT (`ℓ ≤ 2508`) × `INT_BEAM`². Carries no noise and no foreground
residual, so it is **not** a floor for the data; it is reported to show how much of the measured
floor is signal-driven and how much is noise-driven. Planck only.

**Counts.** S1: **300** realisations per instrument. S2: **100**. S3: **50**. The floor for every
reading is drawn from surrogates carrying **the same index arrays and therefore the same
`N_kept`** — *floor matched to sample size*, the harvest gate whose known-bad anchor is
Dalitz D2 (`3a7e029`). No reading is ever compared to a floor taken at a different N.

---

## 6. THE BATTERY

### 6.1 G1 — LP pair-pinning

`share_range_given_pairs` on every b=2 table: the interval the share could occupy over all
distributions carrying the observed pair marginals. **Fires on a COLLAPSED feasible set**: if the
width is not at least 100× the reading's own scale, the reading is pair-determined and is not a
whole-only quantity (`GATES.md` reach 4; `kappa-edge` `3026a68`, `70535d4`). Reported for every
primary cell.

### 6.2 G2 — coarse-graining / binmint

Two legs. **(i) the b-ladder itself** — the b=2 reading is theorem-pinned to zero while the b≥3
reading is not, and the *shape* of the b-dependence in the data must match the surrogate's.
**(ii) the binmint surrogate** — at `b ≥ 3` the surrogate reading **is** the manufacture floor,
and the fraction of the data's absolute reading that the surrogate accounts for is reported as
the manufactured fraction, exactly as the sky campaign reported 7–29 % folded / 47–60 %
equilateral.

### 6.3 G3 — mask sensitivity, with its polarity declared in advance

Primary cut: `TMASK` (`f_sky = 0.8424`). Conservative cut: `TMASK ∧ |b| > 30°`
(`f_sky ≈ 0.842 × 0.5 = 0.42` before intersection; the realised value is reported). WMAP uses the
Planck `TMASK` `ud_grade`d to `NSIDE = 512` with a **fully-unmasked-superpixel** rule (a coarse
pixel is kept iff all 16 fine pixels are unmasked), so that the two instruments are read through
the **same sky cut** and their agreement is a real cross-check rather than a comparison of two
different skies. Additional WMAP-only variant: `|b| > 30°` alone, declared, since WMAP ships no
mask of its own.

**Polarity, declared before the run** (`GATES.md` reach 8, whose known-bad anchor `9180c6a` is a
gate that had its polarity inverted): the gate **fires when the conservative cut and the primary
cut DISAGREE by more than the conservative cut's own surrogate scatter.** Agreement is PASS.
A larger reading under the tighter cut is *not* automatically better and is *not* a
detection — it is a foreground-residual signature and fires the gate in exactly the same way as
a smaller one.

### 6.4 G4 — the filter arm, measured not assumed

`ud_grade` to `NSIDE ∈ {512, 256}` (Planck) applied identically to data and surrogate. The
reported quantity is **the change in the reading and the change in the floor** as a function of
the degrade factor. Pre-registered expectation: the b=2 reading stays at its floor (the theorem
is indifferent to any linear filter, because a linear filter of a Gaussian field is Gaussian),
and the **floor itself falls** as the effective number of independent triples falls. If the b=2
reading rises above its own matched floor under degrading, **the filter is minting** and that is
the single most important thing this pilot could find.

### 6.5 G5 — the boundary gate: clip versus fold

`GATES.md` reach 2 has **no plumb line** and its dye test is **UNVERIFIED at small
differentials**. This arm is built to supply both.

Applied in pixel space to the data map and to 50 S1 surrogates, at `k ∈ {1.0, 1.5, 2.0}` in
units of the map's own σ:

* **clip**: `x ↦ min(max(x, −kσ), +kσ)`. **Pre-registered prediction: the b=2 reading is
  EXACTLY unchanged, ratio 1.000000, bit for bit.** Clipping is weakly monotone and never moves a
  value across the median threshold, so the 2×2×2 table is literally the same table. This
  reproduces `moment-route-saturation-exposure` (median binarization is exactly invariant under
  readout clipping, ratio 1.000) on a new substrate, and it is the **certified boundary-stable
  reading** reach 2 currently lacks. Credit: that finding is ours and prior, from the array
  campaign; this is a reproduction, not a discovery.
* **fold**: `x ↦ 2kσ − x` for `x > kσ`, `x ↦ −2kσ − x` for `x < −kσ`. Non-monotone: it flips the
  sign relative to the threshold for `|x| > 2kσ`, i.e. for **4.6 % (k=1), 0.27 % (k=1.5),
  0.0063 % (k=2)** of pixels under Gaussian statistics. **Pre-registered prediction: fold changes
  the reading, and the k=2 rung is the small-differential dye** — 63 pixels per million, the
  smallest deliberately-planted boundary perturbation this repository has put through any gate.
  Whether the pipeline sees it at k=2 is the measurement.

**Fires on DISAGREEMENT between conventions.** Needs no null.

### 6.6 G6 — the dye test, and the detection limit it measures

`GATES.md` reach 1's dye test reads **PARTIAL — "validated at the 130 % scale. No
planted-amplitude sweep, so the smallest dye it can still see through its own floor is
unmeasured."** This arm measures it.

Base: one S1 surrogate map `g` (theorem-pinned zero), standardised to `u = g/σ`. Three arms,
`f ∈ {0.003, 0.01, 0.03, 0.1, 0.3}`, on templates `E032`, `E064`, `E128`, at `b ∈ {2, 3}`:

| arm | construction | pre-registered prediction |
|---|---|---|
| **D0** pointwise only | `u + f(u² − 1)` | **share EXACTLY at the floor** for `f ≤ 0.1`. A pointwise map cannot move a copula statistic. At `f = 0.3` the map `u ↦ u + f(u²−1)` stops being monotone on the sampled range (turning point `u = −1/2f = −1.67`) and the reading is *expected to rise* — reproducing the registry's own §0 calibration table, where the reading is bit-for-bit identical until `a = 0.3` |
| **D1** filter AFTER pointwise | `smooth_{60'}[ u + f(u² − 1) ]` | **nonzero, rising ≈ `f²`.** This is the 66 σ mechanism, deliberately planted. The smallest `f` whose reading clears the floor's 99th percentile is the pipeline's **method detection limit**, and it is the number reach 1 is missing |
| **D2** pointwise AFTER filter | `v + f(v² − 1)` with `v = smooth_{60'}[u]/σ_v` | **share EXACTLY at the floor** for `f ≤ 0.1`. Same two operations, opposite order. If D1 and D2 do not separate, the pipeline is not sensitive to operation order and every filter statement in this repository is ungauged |

`smooth_{60'}` is `hp.smoothing` at FWHM 60′, applied full-sky before masking.

**VOID condition (V4, §8): if D1 is invisible at every pre-registered `f`, the pipeline's
detection limit is above the largest planted dye and every null reading it produced is UNGAUGED —
not an all-clear.**

### 6.7 G7 — the valve arm: the theorem's own prediction, tested on the sky pipeline

`GATES.md` reach 9 (sampling / shot noise) records its plumb line as **"analytic only:
`valve_from_nothing`… No *data* case is stored (recorded gap)."** This arm supplies one.

`Core/Valve.lean`'s `valve_needs_asymmetry`: a **flip-covariant** per-cell kernel carries
sign-symmetric states to sign-symmetric states and therefore mints **exactly nothing at any noise
strength**; an **asymmetric** per-cell channel can mint. Additive symmetric noise is
flip-covariant. Independent per-pixel skewed noise is not.

Base: one S1 surrogate. Noise added in pixel space at `ε ∈ {0.1, 0.5, 1.0}` in units of σ,
20 realisations each, templates `E032`, `E064`, `E128`, `b = 2`:

| arm | noise | pre-registered prediction |
|---|---|---|
| **N-sym** | `ε σ · 𝒩(0,1)` per pixel | **exactly zero minting** — the reading stays inside the no-noise floor's `[p1, p99]` at every ε. This is the theorem |
| **N-asym** | `ε σ · (E − 1)`, `E ~ Exp(1)`: mean 0, variance 1, skewness +2 | **may mint.** The theorem forbids nothing here. Expected non-monotone in ε (at ε → ∞ the field becomes independent and the share returns to zero), so a peak at intermediate ε is the signature |

**Both outcomes of N-asym are informative and both are pre-registered.** If N-asym mints, reach 9
gains its data-case dye and the valve's field consequence is demonstrated on a second substrate.
If N-asym does *not* mint measurably, the finding is that **per-pixel skew alone is a weak minting
channel on a Gaussian base at this N**, which sharpens the sky campaign's attribution of its
measured 5.8× floor to Poisson *counting* — a channel that changes the alphabet — rather than to
skew as such.

### 6.8 G8 — IPF versus the exact solver

At `b = 2` the exact 1-D solver is used for every reading. **In addition**, IPF is run on the
identical tables and the discrepancy `share_IPF − share_exact` is reported per cell. `GATES.md`
reach 12's dye test reads **"VERIFIED at five orders of magnitude on near-deterministic states.
UNVERIFIED in the interior, where the drift is smaller and the temptation to use IPF is
higher."** The near-uniform tables of the wide templates are the interior; the near-degenerate
tables of WMAP's sub-beam templates are the exterior. Both are measured here, on the same
instrument, in one run.

**Fires when the bracket is wide or the fitted solution sits outside it.** At `b ∈ {3,4}` IPF is
the only available solver; its certificate is `max |fitted pair marginal − target| < 1e−12`
(relative), and monotone entropy increase across iterations. A cell failing the certificate is
**not reported at that b**.

### 6.9 G9 — ties, rails and occupancy

Tied fraction disclosed for every reading (`epistemology.md` rule 4; `GATES.md` reach 11):
the fraction of slot values exactly equal to the threshold or to a quantile cut point, and the
fraction of pixels at the map's own min/max. The maps are float32, so exact ties are possible and
their rate is a fact about the data, not about us. **A reading whose tied fraction is undisclosed
is not reportable.** Occupancy per §4.2.

### 6.10 G10 — null shape before z

`share-null-is-chi2-shaped`: the b=2 null is `χ²₁`-like — mean ≈ 2 × median, p99 ≈ 14 × median —
and the Dalitz D7 near-miss shows a single draw of such a null reading 2.9e−4 and firing a kill
that 200 further draws showed to be flat. **The null's shape is measured and reported before any
`z` is quoted, and no `z` is quoted from a median and a sigma.** Significances are empirical
p-values from the 300-member S1 ensemble; where the empirical resolution `1/(n+1) = 3.3e−3` is
insufficient, a parametric p is quoted **only** from a gamma fit whose KS p-value against the
same ensemble is reported in the same row. A parametric p without its KS is a reporting error.

---

## 7. THE PRE-REGISTERED EXPECTATION AND THE TEST

### 7.1 Stated plainly

**The reading is expected to be consistent with zero on every primary cell at `b = 2`, and
consistent with the surrogate on every primary cell at `b ≥ 3`. A significant nonzero reading is
to be treated as a PIPELINE DEFECT until proven otherwise, not as a detection.**

This is not modesty. It is what `share_eq_zero_of_signSymmetric` says about a Gaussian field, and
what `TARGET_REGISTRY.md` §4.2 argued at length *before* any data was read: the share is
quadratic where the field's own estimator is linear and Planck has already reached
`σ(f_NL^local) ≈ 5`; the naive local model is a **pointwise** map and contributes exactly zero;
what survives is a suppressed residual of an already-tiny signal. **We will not improve an `f_NL`
bound and we are not trying to.**

### 7.2 The primary test statistic, and its null calibrated rather than assumed

**`X` = the number of the 72 primary cells on which the data's reading exceeds the 99th
percentile of its own matched S1 ensemble.**

The 72 cells are **correlated** — common anchors, nested templates, nested `b` — so a binomial
null is wrong. The null distribution of `X` is obtained **leave-one-out over the surrogate
ensemble**: each of the 300 S1 realisations is scored as though it were the data against the
remaining 299, giving 300 draws of `X` under the exact correlation structure of the real grid.
This costs nothing extra and assumes nothing.

* **PASS** — `X` at or below the 95th percentile of its leave-one-out null.
* **ALARM** — `X` above it. The pipeline is then **fouled** and every subsequent field reading it
  produces is **ungauged** until the defect is found. This is reported loudly, per the brief and
  per `GATES.md`'s axiological rule (1): ungauged is a first-class outcome.

The same statistic is computed and reported separately per instrument (36 cells each), so a
defect in one pipeline does not foul the other — **separability**, `GATES.md` axiological
rule (3).

### 7.3 The SMICA-versus-WMAP consistency test

Two instruments, two component-separation pipelines, one sky, read through the **same sky cut**
(§6.3). Their agreement is itself a control and it is scored:

* On every shared template and `b`, the two instruments' readings, each normalised to its own
  matched floor (`share / median(null)`), must agree to within the quadrature sum of their own
  ensemble scatters. Disagreement is reported and is a **foreground- or pipeline-attributable**
  signature, never a sky signature — the two maps are of the *same sky*, so a real sky signal
  cannot appear in one and not the other except through the instruments.
* WMAP's small-θ rungs are beam-dominated and are expected to sit *lower* in absolute share (a
  smoother field at fixed N has fewer effective independent triples, hence a *higher* floor and a
  reading tracking it). This expectation is stated so that its failure is informative.

### 7.4 The deliverable

An explicit list of **which `GATES.md` cells this run discharges**, written so the registry can
be updated from it. The cells this pilot is aimed at, named in advance:

| `GATES.md` cell | current state | what this run supplies if it succeeds |
|---|---|---|
| reach 1, dye test | PARTIAL — no planted-amplitude sweep | §6.6 D1's detection limit: the smallest planted `f` visible above the floor |
| reach 1, plumb line | "held live; not pinned as a fixed regression case" | a pinned real-sky case with a proved-zero answer, mask and beam included |
| reach 2, plumb line | **NONE-YET** | §6.5 clip: a certified boundary-stable reading, ratio 1.000000 |
| reach 2, dye test | UNVERIFIED at small differentials | §6.5 fold at k=2: a 63-per-million planted perturbation |
| reach 5, plumb line | **NONE-YET** | §4.2 + §6.2: a b-stable reading with its manufactured fraction measured |
| reach 5, dye test | PARTIAL — no planted bin-artifact sweep | §6.6 at `b ∈ {2,3}`: the same dye read through two coarse-grainings |
| reach 6, plumb line | **NONE-YET** — never shown to let a real result through | §6.6 D1: a *planted* real result the artifact sluice must pass, beside a data reading it must not |
| reach 8, plumb line | **NONE-YET** | §6.3: a clean run stored as the case the mask-polarity gate must leave alone |
| reach 9, plumb line | analytic only, no data case | §6.7 N-sym: a data-pipeline case where symmetric noise mints zero |
| reach 9, dye test | VERIFIED at 130 % only | §6.7 N-asym: an asymmetric channel's minting curve versus ε |
| reach 12, dye test | UNVERIFIED **in the interior** | §6.8: IPF-vs-exact across near-uniform and near-degenerate tables in one run |
| reach 13 (power of the control) | UNVERIFIED as a general scheme | the whole of §6.6 is a docimasia of this battery |

**Discharge is claimed only where the arm ran and produced its number.** An arm that was
attempted and failed is reported as failed; an arm that was not run is reported as not run. No
cell is marked discharged from an argument.

---

## 8. VOID CONDITIONS — named in advance

A VOID is **ungauged**, which is neither zero nor a detection. It is reported as loudly as a
detection (`GATES.md` axiological rule 1).

* **V1 — occupancy.** Any cell of the `b³` histogram holding ≤ 100 counts ⟹ that
  `(instrument, template, b)` is ungauged and is excluded from the primary grid, with the
  exclusion and the resulting grid size reported. The primary test of §7.2 is recomputed on the
  surviving grid, and the leave-one-out null is recomputed on the *same* surviving grid.
* **V2 — ties.** Tied fraction not computed for a reading ⟹ that reading is not reportable.
* **V3 — floor mismatch.** Any reading whose floor was drawn at a different `N_kept` than the
  reading ⟹ void. (Structurally prevented by the shared index arrays; checked anyway, by
  asserting `N_kept` equality between the data pass and every surrogate pass.)
* **V4 — dead dye.** D1 (§6.6) invisible at every pre-registered `f` ⟹ the pipeline's detection
  limit is above the largest planted dye, and **every null reading in this document is
  UNGAUGED**, including the headline. This is the condition under which the pilot fails as a
  pilot while still being worth publishing.
* **V5 — mask-driven reading.** Primary and conservative cuts disagreeing by more than the
  conservative cut's own surrogate scatter ⟹ that cell is void for the primary grid and is
  reported as mask-driven.
* **V6 — null construction load-bearing.** S1 and S2 floors disagreeing by more than their own
  ensemble scatters ⟹ the spread is quoted as a systematic on every affected reading; if the
  spread exceeds the reading, that cell is void.
* **V7 — solver certificate.** IPF failing `1e−12` at `b ≥ 3` ⟹ that `b` is not reported for that
  cell.
* **V8 — surrogate sanity.** If the S1 ensemble's own `C_ℓ` does not match the data's to machine
  precision, or its measured skewness inside the mask is not consistent with zero at the
  ensemble's own scatter, the surrogate is fouled and everything downstream of it is void. This
  is the check the sky campaign's Stage 3 Gaussian control failed at skewness **+1.6688**
  (`SKY_REALDATA_RESULTS.md` §6 item 2), and it is run first, before any data reading.

---

## 9. WHAT THIS RUN CANNOT LICENSE, whatever it reads

1. **No stance change.** `wild-share` does not move. Nothing here goes near `Stance.lean` and no
   Lean file is opened for editing. `lake` is not invoked.
2. **No cosmology result.** Not an `f_NL` bound, not a Gaussianity test competitive with the
   published bispectrum programme, not a statement about primordial physics.
3. **No anomaly claim in either direction.** Registry row 12: our instrument does not address
   statistical isotropy.
4. **No novelty claim.** Minkowski functionals on Planck maps (Novaes et al., CQG **34**:094002
   (2017)), the binned and modal bispectrum estimators, needlets, wavelets and phase statistics
   are the standing model-independent programme, and they have squeezed the substantive quantity
   harder with better-matched estimators. The registry's INSPIRE sweep found our *object* unnamed
   in the CMB corpus (`ft "cosmic microwave background" and ft "connected information"` → 4 hits,
   all false positives), and **unnamed is not unmeasured**.
5. **If a nonzero residual survives every control**, it is a finding about **our pipeline** or
   about **the maps' processing** — component separation leaves non-Gaussian residuals, and
   SMICA's are documented — **never** about primordial physics. This is pre-registered so that it
   cannot be relitigated after a number is seen.

---

## 10. FILES AND EXECUTION ORDER

`planck_pilot.py` — the instrument, committed with this document, before it is run on data.

Stages, each committed before the next:

1. **V8 surrogate sanity** — `C_ℓ` match and surrogate skewness. No data reading.
2. **Geometry build** — index arrays per template, `N_kept` reported. No data reading.
3. **Floors** — S1/S2/S3 ensembles, null shape measured (§6.10). No data reading.
4. **Dye, boundary and valve arms** (§6.5–6.7) — all on surrogates. No data reading.
5. **The data reading**, once, on the frozen grid, after 1–4 have run and been recorded.
6. `PLANCK_PILOT_RESULTS.md`.

No threshold, ladder, template, surrogate count or VOID condition in this document may be changed
after a data number is seen. If one must be, it is recorded as an amendment naming the number
that prompted it, per the sky campaign's amendment discipline.
