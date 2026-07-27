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

### 5.2 The precision of the limit, and why it is quoted to one significant figure

`water` supplies the point that bounds how this number may be written: **detection and precision
are different budgets.** A reading's own relative standard deviation is
`sqrt(2 + 8·N·share) / (2·N·share)`, so at the floor level (`N·share ≈ 0.2275`, the `χ²₁` median):

| `N·share` | relative sd of a single reading |
|---|---|
| **0.2275 (the floor)** | **430 %** |
| 3.32 (the floor's `p99`) | 81 % |
| 10 | 45 % |
| 100 | 14 % |

| target relative sd | needs `N·share` | as a multiple of the floor |
|---|---|---|
| 100 % | 2.2 | 9.8× |
| 50 % | 8.2 | 36× |
| 20 % | 50 | 221× |
| **10 %** | 200 | **880×** |

**Consequence, applied.** Every ceiling fraction in this document derives from **one** data reading
sitting near its floor, whose relative sd is therefore of order **400 %**. Quoting such a limit to
two or three significant figures would be false precision. **The headline upper limits below are
quoted to ONE significant figure**, and the number this pilot stands behind as *stable* is not the
single reading but the **null's `p95` in the same units** — an ensemble statistic from 300
realisations, which is what the sensitivity rows report.

This also sizes what a future campaign would need: a 10 % measurement of a whole-only share costs
roughly **880× the samples** a bare 5σ detection does. Any programme quoting ratios or ceiling
fractions rather than detections is bound by the precision budget, not the detection one.

### 5.3 The floor is a property of the sampling geometry, not of a formula

`water`'s `water_floor_plumbline.py` verifies the `χ²₁` law from scratch on a product model whose
true share is exactly zero by `valve_from_nothing`. **Run here, independently:** `median×N` =
0.2197–0.2342 against the predicted 0.2275, `mean×2N` = 0.967–1.020 against 1.000, `p99×N` =
3.03–3.42 against 3.317, **worst deviation 3.4 %, and composition-independent** across `p1` = 0.2
and 0.5 and `N` from 1e4 to 1e6.

So the law is right — **and it is a benchmark, not an operative floor.** `χ²₁/(2N)` is exact for
*independent* samples, and triples sharing pixels are not independent. The overlap penalty
`measured floor ÷ (0.2275/N)` now has four substrates behind it:

| construction | penalty |
|---|---|
| iid multinomial from an exact 8-cell distribution | 1.0× (exact) |
| triples on a tetrahedral network | 1.9× |
| triples sharing particles in a dense liquid | 5.8–7.9× |
| **this pilot's CMB pixel triples** | **2.2–42×** (§6.2) |
| dense ideal gas | 45× |

**This pilot never used the naive `(cells−1)/2N = 3.5/N` form**, and its floors were measured
through the byte-identical selection from the start, so there is no correction to apply here —
only an independent confirmation that the practice was the right one. The general rule, which is
`water`'s and worth carrying: **a floor is a property of your sampling geometry, not of anyone's
derivation. Send the plumb-line script; never send the number.**

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

### 6.4 V1 FIRES on 12 cells of 72; V6 does not fire, and nearly fooled this analysis

**V1 — occupancy.** **Twelve of the 72 pre-registered cells are ungauged and excluded**, and the
two instruments fail very differently.

*Planck:* exactly **one** of 36 — **`E008|b4`, worst surrogate `min_occ` = 44**. Nearest survivors
`S064|b4` (201) and `F016|b4` (487). Grid drops to **35**.

*WMAP:* **eleven of 36**, and **seven of them have `min_occ` exactly zero** — `E008|b3`, `E008|b4`,
`E016|b3`, `E016|b4`, `F016|b3`, `F016|b4`, `S064|b3`, `S064|b4`, plus `S128|b4` at 0, `S128|b3` at
20 and `E032|b4` at 51. The WMAP 9-yr ILC is delivered smoothed to **1° FWHM**, so at 8′ and 16′
separations on a 6.9′ pixel grid the three slots are nearly the same number and the `b ≥ 3` tables
**cannot populate their off-diagonal cells at all**. Grid drops to **25**.

**Those are precisely the rungs §4.1 kept on purpose**, as the near-degenerate stress case for
`GATES.md` reach 12's UNVERIFIED interior. The occupancy sluice reaches them first and rules them
ungauged before the solver ever gets a chance to drift on them. That is the right gate firing in
the right order — *depth stated as a rule; a reading below the validated detection limit is not a
detection* — but it means **the reach-12 stress case survives only at `b = 2`**, where the exact
1-D solver is the estimator and IPF is a diagnostic beside it.

**Primary grid: 35 + 25 = 60 cells, down from the pre-registered 72.** The leave-one-out null of
the primary test is recomputed on the surviving grid, as V1 requires. Tied fraction across all
cells: **max 8.8e−07**, disclosed.

**V6 — null construction.** The S2/S1 median ratios span **0.55 to 1.18** (Planck) and **0.56 to
1.28** (WMAP), which reads like a 45 % systematic between two null constructions. It is not. The null is heavy-tailed, so the median of
100 draws carries a large uncertainty; with the median's own standard error (`1.253 σ/√n`) the
largest separation is **1.14 σ** (Planck) and **1.08 σ** (WMAP), with means near 0.5 σ. **The two
constructions agree on both instruments and V6 does not fire.** The spread is quoted as a systematic of that size, not
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

`GATES.md` reach 2 has **no plumb line** and its dye test reads **UNVERIFIED at small
differentials**. This arm was built to supply both, and it does.

**THE PLUMB LINE — clip is EXACTLY invariant, bit for bit, in all 18 cases.**
`k ∈ {1.0, 1.5, 2.0}` × 3 templates × `b ∈ {2, 3}`, on a phase-randomised surrogate:
`share(clip) == share(base)` returns **`True` in every single one** — not "ratio 1.000" but
*the same float*. Clipping is weakly monotone and never moves a value across the median
threshold, so the table is literally the same table. This is the **certified boundary-stable
reading** reach 2 currently lacks, and it reproduces `moment-route-saturation-exposure`'s finding
(median binarization exactly invariant under readout clipping) on a new substrate. Credit for the
original is the array campaign's; this is a reproduction.

**THE SMALL-DIFFERENTIAL DYE — fold at `k = 2` moves the reading with 67 pixels per million.**
The fold flips the sign relative to the threshold for `|x| > 2kσ`, measured here at
**4.536e−02, 2.728e−03 and 6.677e−05** of pixels at `k = 1.0, 1.5, 2.0`:

| `k` | flipped fraction | `E032` | `E064` | `E128` | reading |
|---|---|---|---|---|---|
| 2.0 | **6.677e−05** | **+1.69 %** | **+2.48 %** | **+2.25 %** | small, and **the same sign on all three** |
| 1.5 | 2.728e−03 | +31.3 % | +7.2 % | +16.8 % | large, same sign on all three |
| 1.0 | 4.536e−02 | +47.3 % | **−90.8 %** | −47.6 % | scrambled — 4.5 % of signs flipped |

**What the gate can and cannot do, stated separately.** Its *discrimination between conventions*
is exact: clip's difference is bit-zero, so any nonzero fold difference is unambiguous, and at
`k = 2` that is a **67-parts-per-million** perturbation — by a wide margin the smallest
deliberately planted boundary perturbation this repository has put through any gate. Its
*sensitivity relative to the null*, which is the harder question, is weaker: a 2 % shift sits well
inside the floor's own scatter, so a single such reading could not be called significant on its
own. What carries it is that all three templates move **the same way** under a perturbation of 67
ppm — three near-independent readings agreeing in sign.

At `k = 1.0` the reading is not merely shifted but **scrambled**, including a sign-flip to −90.8 %
at `E064`. A fold convention applied at 1σ destroys the measurement rather than biasing it, which
is worth knowing before anyone reaches for one.

### 9.2 G6 — the dye, the detection limit, and the pre-registered criterion that was wrong

**V4 does NOT fire. The dye is emphatically visible** — up to **216×** its own `f = 0` value.
But the *detection limit as pre-registered* is not attained, and the reason is a finding.

**FACT 3 confirmed bit-for-bit at full scale, on the real pipeline.** D0 (pointwise only) and D2
(pointwise *after* filter) are **the same float** as their own `f = 0` map at
`f = 0.003, 0.01, 0.03, 0.1` — on all three templates, at **both** `b = 2` and `b = 3`, at
`N ≈ 3.9 × 10⁶`, through the real mask and the real HEALPix geometry. Both move only at `f = 0.3`,
exactly where `u ↦ u + f(u²−1)` stops being monotone on the sampled range (turning point
`u = −1/2f = −1.67`). A pointwise map cannot move a copula statistic, and that is now *measured
through this pipeline* rather than inherited from the registry's table.

**Only D1 — filter after pointwise — moves.** At `E032`, `8.13e−07 → 2.76e−05` across the sweep.

**The mechanism is SCALE-MATCHED to the filter, and that is the operational finding.** With the
smoothing at 60′ FWHM:

| template | `θ / θ_filter` | increment at `f = 0.3` | increment / floor median | factor over own `f = 0` |
|---|---|---|---|---|
| `E032` | 0.53 | 2.68e−05 | **30.0** | 33.9 |
| `E064` | 1.07 | 6.54e−05 | **16.7** | 8.1 |
| `E128` | 2.13 | 4.03e−06 | **0.43** | 215.9 |

**A filter of scale `θ_f` manufactures share on templates narrower than itself and barely touches
wider ones.** That is the 66 σ lesson quantified into a rule a future campaign can apply: *the
templates at risk from a given filter are those with `θ ≲ θ_f`.*

**The pre-registered detection limit is therefore not attained, and the criterion was the wrong
one.** §6.6 defined it as *the smallest `f` clearing the floor's `p99` on **all three**
templates*. Per template:

| template | smallest `f` clearing its own floor's `p99` |
|---|---|
| `E032` | **0.1** |
| `E064` | **0.3** |
| `E128` | not attained at `f ≤ 0.3` |

The conjunction over three templates is never satisfied, so the registered number does not exist.
**This is reported as the pre-registered criterion failing, not quietly replaced** — but the
diagnosis is that a conjunction was the wrong shape for a scale-matched mechanism: the three
templates do not have a common detection limit *because the dye does not act on them equally*, and
`E128` sits outside the filter's reach by construction. A future version should register a
per-template limit against a filter of declared scale.

**Two limits of this arm, stated because they bound what the number means.** The `f`-scaling of the
increment measures to an exponent of **≈1.4** at `E032`, against the `≈ f²` predicted in §6.6 —
but the arm uses **one base realisation**, whose `f = 0` value at `E128` landed at `1.87e−08`,
some 500× below that cell's floor median, and increments comparable to the floor cannot determine
an exponent. **One realisation with a noise-comparable baseline is not the instrument for
measuring a power law**, and no exponent is claimed from it.

**And `b = 3` is far less sensitive in relative terms** — D1 moves only **+7.9 % to +8.9 %** at
`f = 0.3`, because the reading there is dominated by the discretisation term of §6.3 rather than
by the planted structure. A dye that shifts a `b = 2` reading by 34× shifts its `b = 3` counterpart
by 9 %.

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
