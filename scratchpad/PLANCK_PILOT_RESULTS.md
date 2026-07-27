# RESULTS — the Planck/WMAP plumb line

**Scope, first and unconditionally: this is an INSTRUMENT-VALIDATION PILOT on public CMB maps.
It is NOT a cosmology result. It is NOT an anomaly search. It is not an `f_NL` bound. Nothing in
it bears on `wild-share`, nothing in it goes near `Stance.lean`, no Lean file was opened for
editing and `lake` was never invoked.**

Pre-registered in `PLANCK_PILOT_PREREG.md` with `PLANCK_PILOT_AMENDMENT_{1,2,3,4,5}.md`, every one
committed before the computation it governs and before any share was computed on a Planck or WMAP
pixel value. The instrument (`planck_pilot.py`) and the analysis (`planck_pilot_analyze.py`) were
committed before they were run on data.

**The registered expectation, restated so it cannot be relitigated after the fact:** standard
cosmology predicts the CMB temperature field is Gaussian; a Gaussian field split at its own median
is sign-symmetric; `share_eq_zero_of_signSymmetric` (`Core/SignSymmetry.lean`, machine-checked)
says a sign-symmetric three-bit state has whole-only share **exactly zero**. So the `b = 2` reading
**must** be consistent with zero, and **a significant nonzero reading is this pipeline, not the
universe** — a defect until proven otherwise.

*(This document is being filled stage by stage as the run completes. Sections marked
**PENDING** have not been computed yet and carry no numbers; per the `current-numbers hygiene`
gate, no superseded number appears anywhere below unlabelled.)*

---

## 1. WHAT THIS PILOT WAS FOR

`TARGET_REGISTRY.md` §4.2 ranked the CMB **rank 2, THE PILOT**: scored **C** on "blind shape"
(weak as a discovery target — the share is quadratic where the field's own bispectrum estimator is
linear, and Planck has already reached `σ(f_NL^local) ≈ 5`) and **A** on baseline, theorem, data,
prior art and cost. Its deliverable is a **plumb line**: the only real-data field this programme
can reach where **the null is a theorem rather than a simulation**, on a real instrument with a
real mask (`f_sky = 0.8424`), a real beam and real anisotropic noise.

Registry row 12 records the adjacent target deliberately **not** run: the CMB anomalies
(hemispherical asymmetry, low-`ℓ` alignments, Cold Spot, lensing) are claims about **statistical
isotropy**, and this instrument does not address them. Nothing below is an anomaly search.

---

## 2. THE INSTRUMENT'S OWN DOCIMASIA, BEFORE THE FIELD

Two examinations of the apparatus, run before it was pointed at anything, in the sense of
`GATES.md`'s ancestor: *could this thing do the job at all.*

### 2.1 The estimator

`dalitz_share.py::share_2x2x2`, the exact 1-D `k = 3` solver (200 bisections to machine precision;
**no IPF at `b = 2` anywhere in this pilot**), on its own stored cases:

| case | read | required | |
|---|---|---|---|
| `parity` | 6.931e−01 | `ln 2` | PASS |
| `copied` | 0.000e+00 | 0 | PASS |
| `ferro` (maximal pair correlation) | 0.000e+00 | 0 | PASS |
| **sign-symmetric family**, worst of 400 random draws | **4.441e−16** | 0 | PASS |
| product family, worst of 400 random draws | 4.441e−16 | 0 | PASS |
| uniform | 0.000e+00 | 0 | PASS |

The sign-symmetric row is the theorem this whole pilot rests on, read at machine zero over 400
random states. `planck_pilot/estimator_plumb_lines.json`.

### 2.2 The analysis instrument

`GATES.md` reach 13 — *power of the control itself* — reads **UNVERIFIED as a general scheme**.
The primary test of §7.2 was therefore given a planted dye before it was allowed to judge anything,
on synthetic `χ²₁` ensembles at `n = 300`, 6 cells:

| input | `X` | null mean | `p(X)` | verdict |
|---|---|---|---|---|
| data drawn from the same null | **0** | 0.08 | 1.000 | **PASS**, correctly |
| the same data multiplied by **30** | **4** of 6 | 0.08 | **0.0033** | **ALARM**, correctly |

The gamma fit used for sub-resolution `p`-values returned **KS `p` = 0.911** against a true `χ²₁`
ensemble, confirming the family assumed by `share-null-is-chi2-shaped`. The leave-one-out null of
`X` came out at mean 0.08 against 0.06 expected for independent cells at a 1 % threshold.

**This is a dye test the registry did not previously hold for this class of statistic**, and it is
what licenses reading a null result from the primary test at all.

---

## 3. V8 — THE SURROGATE GATE FIRED TWICE, BEFORE ANY DATA READING

`PLANCK_PILOT_PREREG.md` §10 orders the surrogate-sanity gate first for exactly this reason. Full
detail in `PLANCK_PILOT_AMENDMENT_1.md` and `_2.md`; the short form:

**First firing — the criterion was measuring the verifier.** Read literally ("`C_ℓ` must match to
machine precision") V8 fired at a per-`ℓ` ratio of **46.2 at `ℓ = 2518`**, where SMICA's `C_ℓ` has
fallen **six decades** below the band carrying the signal — a factor of 40 on `7.7e−25 K²` against
a map variance of `1.17e−08 K²`. The criterion was restated in the form that tests the surrogate
rather than healpy's quadrature: exactness of `|a_ℓm|`, `ξ(θ)` at the templates' **own**
separations, and skewness. The old per-`ℓ` wording is **withdrawn as unmeasurable** — no correct
implementation can pass it, and a gate nothing can pass gets switched off.

**Second firing — and the first diagnosis was wrong.** Amendment 1 attributed WMAP's deficit to
healpy's analysis error at `lmax = 3·nside − 1` and moved WMAP to `lmax = 1024, iter = 3`. The
deficit came back at **1.682e−02, the same number to four significant figures.** The real cause:

> **`ℓ < 2` carries `5.194e−03` of the WMAP map's weighted harmonic variance** — matching the
> observed variance deficit to four figures. The delivered WMAP 9-yr ILC carries a residual
> **dipole at 11.5 % of the map's own σ** and a **monopole at 2.9 %**; `phase_randomise` zeroes
> `ℓ < 2` by construction, so the floor was being drawn against a field the data did not have.

That is not bookkeeping. A monopole and dipole are a deterministic position-dependent offset, so
across anchor positions the data is a **mixture of shifted distributions** — and a mixture of
shifted symmetric distributions is not symmetric about one global threshold, which is precisely
the hypothesis `share_eq_zero_of_signSymmetric` spends. **A known minting channel, present in one
map and absent from its own floor.** Both maps now have their full-sky `ℓ < 2` content removed by
exact HEALPix quadrature (`monopole = mean(m)`, `d_i = 3·mean(m·v_i)`), which touches `ℓ < 2` and
no `ℓ ≥ 2` mode at all and is therefore not a filter. On Planck it is a no-op at `6.4e−08`.

**V8 after the amendments — DISCHARGED, all three legs, both instruments:**

| leg | Planck (`lmax 4096`) | WMAP (`lmax 1024`) | bar |
|---|---|---|---|
| exactness of construction, `max Δ\|a_ℓm\|/\|a_ℓm\|` | **4.014e−16** | **4.014e−16** | `< 1e−12` |
| `ξ(θ)` at 8, 16, 32, 64, 128, 256′, max \|ratio − 1\| | **1.264e−10** | **6.500e−10** | `< 1e−03` |
| total variance, \|ratio − 1\| | **4.597e−11** | **4.642e−10** | `< 1e−03` |
| surrogate skewness inside the mask | **+0.00425 ± 0.00542** | **+0.02278 ± 0.04716** | ≈ 0 |

Eight and seven orders of magnitude better than before the amendments. For contrast, and because
the record should carry it in one place: the sky campaign's Stage 3 Gaussian control failed this
same check at a skewness of **+1.6688** (`SKY_REALDATA_RESULTS.md` §6 item 2).

---

## 4. THE GEOMETRY, AND THE REUSE THE FLOORS HAVE TO BE READ AGAINST

One draw of 4 000 000 anchors and azimuths (seed 20260727), shared across every template and both
instruments so that templates are compared on a common sample. Triples retained iff all three
pixels are unmasked.

| template | declared `(θ₁₂,θ₁₃,θ₂₃)′` | Planck `n_kept` | Planck realised′ | WMAP `n_kept` | WMAP realised′ |
|---|---|---|---|---|---|
| `E008` | (8, 8, 8) | 3 986 149 | 8.13, 8.10, 8.20 | 3 985 093 | 7.93, 7.92, **7.08** |
| `E016` | (16, 16, 16) | 3 973 897 | 15.93, 15.90, 15.89 | 3 971 685 | 15.51, 15.46, 15.24 |
| `E032` | (32, 32, 32) | 3 952 575 | 32.05, 32.05, 32.07 | 3 946 514 | 32.54, 32.42, 32.74 |
| `E064` | (64, 64, 64) | 3 913 801 | 63.96, 63.97, 63.92 | 3 908 668 | 63.69, 63.60, 63.61 |
| `E128` | (128, 128, 128) | 3 841 529 | 128.00, 128.01, 128.01 | 3 836 130 | 128.17, 128.20, 128.30 |
| `E256` | (256, 256, 256) | 3 716 818 | 256.0, 256.0, 256.0 | 3 711 780 | 255.80, 255.85, 255.87 |
| `F016` | (16, 16, 32) | 3 967 204 | 15.93, 15.93, 31.87 | 3 964 619 | 15.51, 15.53, 31.03 |
| `F064` | (64, 64, 128) | 3 890 497 | 63.96, 63.96, 127.94 | 3 885 692 | 63.71, 63.68, 127.44 |
| `F128` | (128, 128, 256) | 3 802 064 | 128.00, 128.01, 256.0 | 3 796 705 | 128.17, 128.09, 256.14 |
| `S064` | (8, 64, 64) | 3 938 980 | 8.13, 63.97, 63.99 | 3 935 440 | 7.92, 63.62, 63.56 |
| `S128` | (16, 128, 128) | 3 887 305 | 15.93, 128.01, 128.00 | 3 882 592 | 15.53, 128.17, 128.21 |
| `S256` | (32, 256, 256) | 3 798 283 | 32.04, 255.99, 256.01 | 3 792 635 | 32.53, 255.83, 255.91 |

Realised separations track declared to better than 2 % on Planck. The one visible departure is
WMAP `E008`'s third leg at **7.08′ against 8′ declared**: an 8′ triangle is under-resolved at
`NSIDE = 512`'s 6.9′ pixels. It is **kept, not dropped** — the near-degenerate rungs are the stress
case `GATES.md` reach 12 needs (its dye test reads UNVERIFIED *in the interior*).

`f_sky`: Planck 0.84241, WMAP 0.83998 under the common cut (Planck's `TMASK` `ud_grade`d to
`NSIDE 512` with the fully-unmasked-superpixel rule, so **both instruments read the same sky**);
0.49413 and 0.49372 under the conservative `|b| > 30°` cut.

**The reuse census, stated plainly because it caps the sensitivity.** Anchors are drawn *with
replacement*, and the sky has a finite number of pixels:

| | Planck `E064` | WMAP `E064` |
|---|---|---|
| triples | 3 913 801 | 3 908 668 |
| **distinct anchors** | 3 736 798 (4.5 % duplicated) | **2 030 687 (48.0 % duplicated)** |
| **distinct pixels used** | 10 244 268 of 42 397 229 available | **2 601 861 of 2 641 856 available** |
| mean reuse per used pixel | 1.15 | **4.51** |
| max reuse of one pixel | 8 | 21 |

**WMAP's nominal 3.9e6 triples are drawn from at most 2.6e6 distinct pixels — essentially its
whole unmasked sky — so its effective independent sample is far below its nominal `N` and its
floor will sit correspondingly higher.** This costs sensitivity, not validity: the surrogate
carries the byte-identical index arrays, so the measured floor absorbs it exactly. It is recorded
here rather than discovered in the comparison.

---

## 5. THE CEILING FRACTION, AND ITS DENOMINATOR

Every reading, residual and floor below is reported twice: in **nats**, and as a **ceiling
fraction** — the share divided by the cap for the same slot count and alphabet — so this pilot's
number can be set beside the other substrates carrying it.

**The denominator is machine-checked.** `CIRISOntology/Core/ThirdCap.lean` (commit `8925843`)
proves, sorry-free and axiom-audited:

| theorem | statement |
|---|---|
| `share_le_log_two` | `share ≤ log 2` for **every** state on three binary slots, **no hypothesis on the pair marginals** |
| `share_max_eq_log_two` | attainment (`share_parity`) and bound together — `log 2` is the **exact maximum** on three bits |
| `share_le_log_card_third` | `share ≤ log(card of the third slot's alphabet)`, **general alphabets** — so `b = 3` and `b = 4` are capped at `ln b`, also machine-checked |
| `share_le_grouping_gaps` | the **sharp, data-computable** ceiling `share ≤ H(pair) + H(remaining slot) − H(p)` in all three orientations; the honest per-table ceiling is their minimum |

**A correction this pilot owes, recorded rather than patched.** `PLANCK_PILOT_AMENDMENT_4.md`
audited this denominator and reported the upper-bound direction was *not* mechanized anywhere here
— `share_parity` gave attainment, `shareK_le_of_pair_uniform` assumed a uniform pair marginal that
no correlated real table has, and `shareK_le_log_sub_pair` was *looser* than `log 2`. That was true
when written, this pilot propagated it to the team lead, and **it is now false**: the brick it
named was built. `PLANCK_PILOT_AMENDMENT_5.md` carries the correction; every "NOT machine-checked"
flag on a ceiling fraction here is **withdrawn**.

**Two denominators are reported, because they answer different questions.**
`share_le_grouping_gaps` is far tighter on tables like ours — it reads `0.6931471805599452` on the
parity state (coinciding with `ln 2` to the last digit, as it must) and **0.0216 nats, ~3 % of
`ln 2`**, on a random near-independent table, which is what a Gaussian sky gives. So:

* **against `ln 2`** — the cross-campaign comparable number, the one the synthesis wants;
* **against the sharp per-table ceiling** — the honest *headroom*, i.e. how much whole-only
  structure this particular table could have carried given its own entropies.

Quoting only the first would flatter a near-independent table; quoting only the second would not be
comparable to anything.

**The `b ≥ 3` caveat that the new theorem does not touch:** per §2 of the pre-registration the
reference at `b ≥ 3` is the surrogate's own reading, **not zero** — a discretised Gaussian at
`b ≥ 3` carries genuinely nonzero order-3 connected information — so those ceiling fractions are
differential, and an absolute one quoted without its surrogate value is a reporting error.

**Why an upper limit needs no extra assumption here.** The estimator is positively biased at a true
share of zero — the finite-sample floor *adds* — so the raw reading bounds the truth from above.
And why the sensitivity is reported beside it: below the null's `p95` in the same units,
"consistent with zero" is a statement about the instrument, not about the sky.

### 5.1 A consistency check on the proved cap

Run before `ThirdCap.lean` was known to exist, when it stood in for the unmechanized step; kept as
a consistency check on a now-proved theorem, and labelled as such. **4 × 10⁵ random three-bit
states**, exact solver:

| ensemble | max share | fraction of `ln 2` |
|---|---|---|
| Dirichlet(1) on the 8-cell simplex, 2 × 10⁵ draws | 0.526590 | 0.7597 |
| Dirichlet(0.05), sparse / near-deterministic, 2 × 10⁵ draws | **0.663696** | **0.9575** |

Nothing crossed `ln 2`. The Shearer bound was violated in **0 of 20 000** draws and sat strictly
below `ln 2` in **20 000 of 20 000**. Independently consistent with the pump campaign's own
20 000-state compliance run (max 0.6174).

## 6. THE FLOORS AND THE NULL'S SHAPE

300 phase-randomised surrogates (**S1**, primary) per cell, plus 100 `synfast` realisations at the
measured `C_ℓ` (**S2**), 100 S1 realisations through the conservative `|b| > 30°` cut, and 50
theory realisations (**S3**, diagnostic). Every floor is drawn at the **same `N_kept`** as the
reading it gauges — the harvest gate *floor matched to sample size*, whose known-bad anchor is
Dalitz D2 (`3a7e029`).

### 6.1 The null is `χ²₁`-shaped, on a real sky pipeline

| | measured range (Planck, `b = 2`, 12 templates) | `χ²₁` |
|---|---|---|
| mean / median | **1.78 – 2.51** | 2.20 |
| p99 / median | **12.5 – 17.8** | 14.6 |

`share-null-is-chi2-shaped` confirmed on real data. **Every significance below is an empirical
`p`; no `z` is quoted from a median and a sigma.**

### 6.2 The effective independent-triple count, measured

For a `χ²₁` null the median is `0.4549/(2 N_eff)`, so the measured floor gives `N_eff` directly.

| template | `N_kept` | floor median (nats) | `N_eff` | `N/N_eff` |
|---|---|---|---|---|
| `E008` | 3 986 149 | 1.2428e−07 | 1.83e+06 | **2.2** |
| `E016` | 3 973 897 | 2.6335e−07 | 8.64e+05 | 4.6 |
| `E032` | 3 952 575 | 7.6716e−07 | 2.97e+05 | 13.3 |
| `E064` | 3 913 801 | 2.4472e−06 | 9.30e+04 | **42.1** |
| `E128` | 3 841 529 | 2.3751e−06 | 9.58e+04 | 40.1 |
| `E256` | 3 716 818 | 2.2126e−06 | 1.03e+05 | 36.2 |
| `F016` | 3 967 204 | 3.8954e−07 | 5.84e+05 | 6.8 |
| `F064` | 3 890 497 | 2.0176e−06 | 1.13e+05 | 34.5 |
| `F128` | 3 802 064 | 2.2182e−06 | 1.03e+05 | 37.1 |
| `S064` | 3 938 980 | 5.3696e−07 | 4.24e+05 | 9.3 |
| `S128` | 3 887 305 | 1.0169e−06 | 2.24e+05 | 17.4 |
| `S256` | 3 798 283 | 1.1183e−06 | 2.03e+05 | 18.7 |

**The pattern is the informative part, and it is the opposite of the naive expectation.** The
floor is *worst* at wide separations and *best* at narrow ones. Narrow triples are
near-deterministic — three nearly identical pixels — so the feasible parity direction is short and
the estimator's variance is small; wide triples are near-uniform and the feasible range is wide.
**The floor is set by how uniform the table is, not by `N` alone.** This is the same regime
distinction `ipf-sharek-boundary-drift` found for solver drift, showing up here in the sampling
floor, and it is measured rather than assumed.

In ceiling-fraction terms the Planck `b = 2` floor is **1.8e−05 % to 3.5e−04 % of `ln 2`**.

### 6.3 `b ≥ 3` is not a noise floor at all

| template | `b = 2` | `b = 3` | ratio |
|---|---|---|---|
| `E008` | 1.2428e−07 | **2.3781e−03** | **19 135** |
| `E016` | 2.6335e−07 | 1.6014e−03 | 6 081 |
| `E032` | 7.6716e−07 | 3.5293e−04 | 460 |
| `E064` | 2.4472e−06 | 2.4405e−05 | 10.0 |
| `E256` | 2.2126e−06 | 7.4332e−06 | 3.4 |

A **discretised correlated Gaussian genuinely carries order-3 connected information**, and it is
enormous next to the `b = 2` floor — four orders of magnitude at the narrowest template, where the
pixels are most correlated. This is `PLANCK_PILOT_PREREG.md` §2's warning confirmed at full force:
**at `b ≥ 3` the reference is the surrogate's own reading, never zero**, and an absolute `b ≥ 3`
number without its surrogate value is a reporting error, not a detection.

### 6.4 V1 FIRES on one cell; V6 does not fire, and nearly fooled this analysis

**V1 — occupancy.** Exactly **one** of 36 Planck cells falls below the pre-registered bar of 100
counts in every histogram cell: **`E008|b4`, worst surrogate `min_occ` = 44.** It is **ungauged**
and excluded from the primary grid, which drops to 35 Planck cells. Nearest survivors: `S064|b4`
(201) and `F016|b4` (487). Tied fraction across all cells: **max 8.8e−07**, disclosed.

**V6 — null construction.** The S2/S1 median ratios span **0.55 to 1.18**, which reads like a 45 %
systematic between two null constructions. It is not. The null is heavy-tailed, so the median of
100 draws carries a large uncertainty; with the median's own standard error (`1.253 σ/√n`) the
largest separation across all twelve templates is **1.14 σ**, and the mean is 0.5 σ. **The two
constructions agree and V6 does not fire.** The spread is quoted as a systematic of that size, not
as a disagreement.

What *does* differ is the **scatter**: S2's relative scatter runs up to **1.8×** S1's at the
intermediate templates. That is the expected signature of `synfast` carrying `C_ℓ` cosmic variance
which fixed-amplitude phase randomisation removes by construction (the "fixed field" of Angulo &
Pontzen 2016). S1 is primary as pre-registered, and it is the right primary for the question
asked: *does this sky carry order-3 structure beyond its own two-point function?* conditions on
the observed `C_ℓ`.

**This near-miss is itself the `null-shape before z` gate working.** Read as a ratio of medians the
spread looked like a 45 % systematic worth an amendment; read with the heavy-tailed null's own
uncertainty it is 1.1 σ. The gate's known-bad anchor is Dalitz D7, and this is the same shape of
error caught before it was written down.


## 7. THE DATA READING, AND THE PRIMARY TEST

**PENDING** — stage 5.

## 8. SMICA VERSUS WMAP

**PENDING** — stage 5.

## 9. THE ARMS

### 9.1 G5 — boundary: clip versus fold
**PENDING** — stages 4 and 5.

### 9.2 G6 — the dye, and the detection limit
**PENDING** — stage 4.

### 9.3 G7 — the valve: symmetric versus skewed per-pixel noise
**PENDING** — stage 4.

### 9.4 G8 — IPF versus the exact solver
**PENDING** — stage 5.

### 9.5 G4 — the degrade arm
**PENDING** — stages 5 and 6.

## 10. THE VOID REGISTER

**PENDING.**

## 11. WHAT THIS RUN DISCHARGED IN `GATES.md`

**PENDING.**

## 12. WHAT THIS RUN DOES NOT LICENSE

Unchanged from `PLANCK_PILOT_PREREG.md` §9 and `AMENDMENT_4.md` §4, and restated here so it travels with the numbers:

1. **No stance change.** `wild-share` does not move. Nothing here goes near `Stance.lean`; no Lean
   file was opened for editing; `lake` was never invoked.
2. **No cosmology result.** Not an `f_NL` bound, not a Gaussianity test competitive with the
   published bispectrum programme, not a statement about primordial physics.
3. **No anomaly claim in either direction.** Our instrument does not address statistical isotropy.
4. **No novelty claim.** Minkowski functionals on Planck maps (Novaes et al., CQG **34**:094002
   (2017)), the binned and modal bispectrum estimators, needlets, wavelets and phase statistics
   are the standing model-independent programme and have squeezed the substantive quantity harder
   with better-matched estimators. The registry's INSPIRE sweep found our *object* unnamed in the
   CMB corpus (4 hits, all false positives), and **unnamed is not unmeasured**. The estimator is
   Schneidman, Still, Berry & Bialek (2003) and Amari (2001); phase randomisation is the standard
   CMB surrogate; the maps are Planck 2018 SMICA and WMAP 9-yr ILC.
5. **If a nonzero residual survives every control**, it is a finding about **this pipeline** or
   about **the maps' processing** — component separation leaves non-Gaussian residuals — **never**
   about primordial physics.
