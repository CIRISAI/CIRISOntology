# RESULTS — the Planck/WMAP plumb line

**Scope, first and unconditionally: this is an INSTRUMENT-VALIDATION PILOT on public CMB maps.
It is NOT a cosmology result. It is NOT an anomaly search. It is not an `f_NL` bound. Nothing in
it bears on `wild-share`, nothing in it goes near `Stance.lean`, no Lean file was opened for
editing and `lake` was never invoked.**

Pre-registered in `PLANCK_PILOT_PREREG.md` with `PLANCK_PILOT_AMENDMENT_{1,2,3,4,5,6}.md`, every
one committed before the computation it governs and before any share was computed on a Planck or
WMAP pixel value. The instrument (`planck_pilot.py`) and the analysis (`planck_pilot_analyze.py`)
were committed before they were run on data.

**The registered expectation, restated so it cannot be relitigated after the fact:** standard
cosmology predicts the CMB temperature field is Gaussian; a Gaussian field split at its own median
is sign-symmetric; `share_eq_zero_of_signSymmetric` (`Core/SignSymmetry.lean`, machine-checked)
says a sign-symmetric three-bit state has whole-only share **exactly zero**. So the `b = 2` reading
**must** be consistent with zero, and **a significant nonzero reading is this pipeline, not the
universe** — a defect until proven otherwise.

**THE HEADLINE, IN ONE LINE: the reading is consistent with zero on every cell of both
instruments — `X = 0` of 35 and `X = 0` of 25 against a leave-one-out p95 of 2.0 — and the CMB's
pairwise-blind order-3 share is bounded below `2 × 10⁻⁵` of one bit (`ln 2`) at these scales, by
an instrument that could not have seen anything below `1 × 10⁻⁵` of one bit. The pilot is a
plumb line and it hangs straight.**

*(All stages have run. Per the `current-numbers hygiene` gate, no superseded number appears
anywhere below unlabelled: Amendment 4 §1's denominator claim and `PREREG` §6.7's valve citation
are both superseded and both are labelled as such where they appear, in §5 and §9.3.)*

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

The data was read **once**, on the frozen grid, after stages 1–4 had run and been recorded —
`planck_pilot/stage5_data.json`, written 14:54 on 2026-07-27, with the analysis over it in
`planck_pilot/analysis.json`.

### 7.1 THE VERDICT — `X = 0` on both instruments; the ALARM branch does not open

**Not one cell of either surviving grid reads above the 99th percentile of its own matched S1
ensemble.**

| | Planck | WMAP |
|---|---|---|
| cells in the surviving grid (V1, §6.4) | 35 | 25 |
| **`X_data`** | **0** | **0** |
| leave-one-out null of `X`: mean | 0.46 | 0.33 |
| p95 (the pre-registered PASS bar) | 2.05 | 2.00 |
| **max over the 300 draws** | **15** | 8 |
| `p(X)` | 1.000 | 1.000 |
| **verdict (`PREREG` §7.2)** | **PASS** | **PASS** |

**The null's maximum is the reason the calibration was pre-registered rather than assumed.** One
of the 300 Planck surrogates, scored as though it were the data against the other 299, put **15
of its 35 cells** above p99. A binomial null would have called that a 30 σ detection. The cells
are correlated — common anchors, nested templates, nested `b` — and the leave-one-out null
measures that correlation instead of assuming it away. The full histogram is
`X_null_hist = [255, 22, 8, 3, 4, 1, 0, 0, 1, 3, 1, 1, …]`: 85 % of draws score zero and a thin
tail runs to 15.

**The b = 2 grid, cell by cell.** `p` is empirical against 300 realisations (resolution 3.3e−3);
no `z` is quoted anywhere.

| template | Planck share (nats) | / floor | `p` | WMAP share (nats) | / floor | `p` |
|---|---|---|---|---|---|---|
| `E008` | 6.798e−08 | 0.55 | 0.635 | 3.301e−08 | 0.45 | 0.648 |
| `E016` | 8.864e−08 | 0.34 | 0.671 | 3.473e−07 | 2.20 | 0.306 |
| `E032` | 1.041e−06 | 1.36 | 0.429 | 4.555e−06 | 4.85 | 0.150 |
| `E064` | 7.293e−06 | 2.98 | 0.229 | 2.107e−05 | 4.31 | 0.179 |
| `E128` | **1.707e−05** | **7.19** | **0.060** | **7.112e−05** | **6.49** | **0.096** |
| `E256` | 5.859e−06 | 2.65 | 0.269 | 3.869e−05 | 2.32 | 0.289 |
| `F016` | 3.659e−08 | 0.09 | 0.851 | 1.202e−06 | 3.95 | 0.166 |
| `F064` | 6.073e−06 | 3.01 | 0.249 | 3.517e−05 | 5.60 | 0.110 |
| `F128` | 9.609e−06 | 4.33 | 0.143 | 3.653e−05 | 3.49 | 0.259 |
| `S064` | 4.700e−07 | 0.88 | 0.535 | 4.799e−06 | 7.14 | **0.053** |
| `S128` | 2.808e−06 | 2.76 | 0.216 | 5.133e−06 | 2.58 | 0.249 |
| `S256` | 2.050e−06 | 1.83 | 0.369 | 1.413e−05 | 3.30 | 0.216 |

The three smallest `p` of the 24 are 0.053, 0.060 and 0.096 — on a `χ²₁`-shaped null whose
p99/median is 12.5–17.8 (§6.1), so a single cell sitting at 7× its floor median is an ordinary
draw, not a signal. **Five of the 24 read *below* their floor median.** That is the shape of a
true zero read through a heavy-tailed estimator.

**At `b ≥ 3` the reference is the surrogate, and the surrogate accounts for most of the
reading.** The manufactured fraction (`surrogate median ÷ data reading`, `PREREG` §6.2(ii) — the
quantity the sky campaign reported as 7–29 % folded / 47–60 % equilateral) is, for Planck at
`b = 3`:

| template | `E008` | `E016` | `E032` | `E064` | `E128` | `E256` | `F016` | `F064` | `F128` | `S064` | `S128` | `S256` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| manufactured | 98.9 % | 104.6 % | 98.1 % | 60.4 % | 32.6 % | 34.8 % | 100.0 % | 65.0 % | 43.3 % | 113.4 % | 96.6 % | 88.5 % |

**33 % to 113 % — and four cells above 100 %, meaning the surrogate reads *higher* than the
data.** The coarse-graining is manufacturing between a third and all of the absolute `b = 3`
number. Any `b ≥ 3` absolute figure quoted without this column is a reporting error, exactly as
`PREREG` §2 declared before the run.

### 7.2 THE UPPER LIMIT, with both denominators named and both margins stated

For a theorem-pinned-zero target the deliverable is a limit, and the estimator is positively
biased at a true share of zero, so **the raw reading bounds the truth from above with no further
assumption**. Per `GATES.md`'s *named-denominator reporting* gate and its cap/floor amendment,
both denominators are reported and the sharp one only where its margin over the floor is stated.

**The margin, first, because the amendment turns on it.** `glass`'s control printed **−1695 %**
of a theorem-pinned zero when the sharp cap collapsed *below* the reading's own floor. That
failure mode does not occur here and the numbers say by how much:

| | Planck `b2` | Planck `b3` | Planck `b4` | WMAP `b2` | WMAP `b3` | WMAP `b4` |
|---|---|---|---|---|---|---|
| **min sharp-cap / floor across cells** | **1 983** | **109** | **140** | **1 504** | **102** | **132** |
| max | 2.4e+06 | 1 030 | 889 | 7.5e+06 | 386 | 382 |

Every cell clears the stated `≥ 100` bar, the narrowest margin being **102×** (WMAP `S256|b3`).
**The sharp fraction is therefore defined on every cell of this pilot and none is declared
undefined.** It is worth stating that it clears by only a factor of a few at `b ≥ 3`: a campaign
one step nearer independence would land under the bar.

**The limits.** Per §5.2 the precision budget permits **one significant figure**, and the
rounding is ordinary — a single reading near its floor carries a relative sd of order 400 %, so
the difference between rounding up and down is four orders of magnitude smaller than the
uncertainty and choosing between them would be theatre. The stable number is the sensitivity row
of §7.3, not any of these.

| | against **`ln b`** (cross-substrate; `share_le_log_two` / `share_le_log_card_third`) | at | against the **sharp per-table ceiling** (`share_le_grouping_gaps`) | at |
|---|---|---|---|---|
| **Planck `b = 2`** | **< 2 × 10⁻⁵ = 0.002 %** | `E128` | **< 2 × 10⁻³ = 0.2 %** | `E128` |
| **WMAP `b = 2`** | **< 1 × 10⁻⁴ = 0.01 %** | `E128` | **< 2 × 10⁻³ = 0.2 %** | **`E256`** |
| Planck `b = 3` (differential) | < 3 × 10⁻⁵ = 0.003 % | `E128` | < 2 × 10⁻³ = 0.2 % | `E256` |
| Planck `b = 4` (differential) | < 2 × 10⁻⁵ = 0.002 % | `E128` | < 2 × 10⁻³ = 0.2 % | `E256` |
| WMAP `b = 3` (differential) | < 7 × 10⁻⁵ = 0.007 % | `E256` | < 2 × 10⁻³ = 0.2 % | `E256` |
| WMAP `b = 4` (differential) | < 1 × 10⁻⁴ = 0.01 % | `E128` | < 3 × 10⁻³ = 0.3 % | `E256` |

Unrounded, for the record: Planck `b=2` 2.463e−05 of `ln 2` and 1.805e−03 of its sharp cap; WMAP
`b=2` 1.026e−04 and 1.541e−03. The `b ≥ 3` rows are `reading − surrogate median`, never the
absolute number.

**The two denominators disagree about which cell is worst, and that is the gate's own second
clause showing up in the data.** For WMAP the largest `ln 2` fraction is at `E128` and the
largest sharp fraction is at `E256` — because the sharp cap *itself* falls by 2.2× between them
as the triple approaches independence. Against `ln 2` the reading rises 251× from `E008` to
`E128`; against the sharp cap it rises 7 900×, because the denominator is shrinking while the
numerator grows. **No statement about how this quantity varies with scale is complete without
naming its denominator.**

**Set beside the other substrates** (all against `ln 2` or `ln b`, the comparable denominator):
designed LFSR ~100 %, QPU valve bulge ~8 %, 2D Ising critical ridge ~0.66 %, chaotic oscillator
array ~0.03 %, **CMB `< 0.002 %`**. Those four are *received* numbers, not re-derived here
(§13).

### 7.3 THE SENSITIVITY — what this pilot could not have seen

A limit without this row is unreadable. The null's p95 in the same units, median over the cells:

| | Planck | WMAP |
|---|---|---|
| `b = 2`, as a fraction of `ln 2` | **1.1 × 10⁻⁵ (0.0011 %)** | **3.7 × 10⁻⁵ (0.0037 %)** |
| `b = 3`, differential, of `ln 3` | 2.4 × 10⁻⁵ | 1.7 × 10⁻⁴ |
| `b = 4`, differential, of `ln 4` | 2.3 × 10⁻⁵ | 1.8 × 10⁻⁴ |
| floor (null **median**), `b = 2`, of `ln 2` | 1.5 × 10⁻⁶ | 4.5 × 10⁻⁶ |

**The Planck `b = 2` limit is 2.2× its own sensitivity and the WMAP limit is 2.8×.** So the
honest reading of §7.2 is: *this pilot bounds the CMB's pairwise-blind share below ~2 × 10⁻⁵ of
one bit, and it could not have distinguished anything below ~1 × 10⁻⁵ of one bit from zero.* The
limit is set by the instrument, not by the sky. At `b = 3` and `b = 4` on WMAP the measured
differential is **below** the sensitivity outright, which is the same statement in its starkest
form.

### 7.4 V1 AND V2 ON THE DATA READING

**Occupancy (V1).** The exclusions of §6.4 were set by the *worst* of the data pass and all 300
surrogates. On the data pass alone the minimum cell occupancy is **112** (Planck `E008|b4`) and
**0** (WMAP `E008|b3`) — the WMAP `b ≥ 3` near-degenerate tables cannot populate their
off-diagonal cells at all, as §6.4 records. No excluded cell is reported as a number anywhere.

**Ties (V2).** Disclosed for every reading, as `epistemology.md` rule 4 requires:

| pass | max tied fraction | where |
|---|---|---|
| Planck primary | 4.287e−07 | `S128|b4` |
| Planck conservative | 5.275e−07 | `S256|b4` |
| WMAP primary | 1.876e−06 | `E064|b4` |
| WMAP conservative | 2.868e−06 | `E032|b4` |
| Planck degraded (`NSIDE` 256) | 4.293e−06 | `F016|b3` |
| zero-threshold variant, both instruments | **0** | — |

Every value is below 5e−06 and the largest affects fewer than 5 pixels in a million. **V2 does
not fire.** The zero-threshold pass reads exactly zero ties because no float32 pixel value equals
its cut exactly.

**Floor matching (V3).** `N_kept` was asserted equal between the data pass and every surrogate
pass, cell by cell: **0 mismatches on either instrument.** Structurally prevented by the shared
index arrays, and checked anyway.

### 7.5 AMENDMENT 6's REGISTERED BRANCH — and the statistic's own null is wrong

Amendment 6 added the sign-symmetry test so that the pilot would *measure* the hypothesis
`share_eq_zero_of_signSymmetric` spends rather than assert it of the data. It registered two
outcomes in advance, and §4.0 registered which quantity decides between them: **the `p`-value
says whether the state is off the symmetric point; the detuning `m` says whether that matters.**

**The `p`-value leg reads outcome (b): 7 of 12 Planck templates and 9 of 12 WMAP templates
reject sign symmetry at `p < 0.01`** (`χ²` 1.99–133.7 Planck, 1.71–545.8 WMAP; worst fractional
asymmetry 7.8e−03 and 2.5e−02).

**And that leg cannot be read literally, because the same statistic rejects on surrogates that
are sign-symmetric by construction.** A phase-randomised map has uniform random phases, so its
distribution is invariant under global negation — its median-split table *is* sign-symmetric,
with no inference involved. The statistic was recorded on three such maps at three templates:

| base | `E032` | `E064` | `E128` |
|---|---|---|---|
| S1, raw (stage-4 boundary / dye base) | `χ²` 28.17, `p` 1.2e−05 | 27.12, 1.9e−05 | 17.24, 1.7e−03 |
| S1, 60′-smoothed (D1/D2 `f = 0`) | 7.32, 0.120 | 72.98, 5.3e−15 | 8.70, 0.069 |
| S1 (G7b base) | 45.35, 3.4e−09 | 61.55, 1.4e−12 | 21.94, 2.1e−04 |

**Seven of those nine readings reject at `p < 0.01`, against a nominal rate of 0.01.** The mean
statistic is **32.3** where `χ²₄` expects 4.00 — the statistic is inflated **~8×**. The cause is
in this document already: `sign_asymmetry` assumes **multinomial** sampling variance, and §6.2
*measured* this pipeline's triples to carry `N/N_eff = 2.2–42`. Dividing the G7b base's `χ²` by
the measured `N/N_eff` at each template gives 3.4, 1.5 and 0.5 against a `χ²₄` median of 3.4 —
consistent with sign symmetry, as construction says it must be.

**So the `p`-value branch is undecidable with what is on disk**, and honestly so: a calibrated
version needs the statistic run over the full S1 ensemble, and stage 3 predates Amendment 6
(Amendment 6 §6 says exactly this). The nine surrogate readings are three maps, not thirty.

**The branch that is decidable is the one Amendment 6 §4.0 registered as decisive, and it comes
back closed.** With `pump-curve`'s state-axis floor `K·m²`, `K = 0.00712` (received, §13), and
this pilot's *measured* floors:

| | worst per-slot detuning `|m|` | registered threshold at that template | state-axis floor as a fraction of the measured floor |
|---|---|---|---|
| **Planck** | 8.14e−04 (`S064`) | 8.7e−03 | **0.88 %** (worst of 12) |
| **WMAP** | 6.10e−04 (`F064`) | 2.97e−02 | **0.22 %** (worst of 12) |

Every template's `m` is **11× to 240×** below the detuning at which the state axis would first
reach this pilot's own shot noise. **Registered in advance: "if the measured `m` comes back below
≈ 3e−03, the state-axis branch is closed by measurement, not by argument."** It did, on all 24
cells. The state axis cannot affect any reading in this document, whatever the `p`-value leg is
doing.

**The framing that survives.** The theorem pins the *surrogate* exactly — it is sign-symmetric by
construction, and the primary test always compared data to surrogate and never to an assumed
analytic zero. For the *data*, this pilot has **not** established sign symmetry to the precision
its own statistic claims, and it has established that the departure is too small to matter by the
route the correction was raised on. The honest sentence is therefore Amendment 6 outcome (a)
**on the quantity that decides**, and *unresolved* on the `p`-value leg, whose null this pilot has
now shown to be wrong for its own sampling geometry.

### 7.6 THE ZERO-THRESHOLD VARIANT

Declared in `PREREG` §2 and reported alongside: `τ = 0` for Planck (`τ` = the map mean for WMAP,
which carries a residual offset). At `b = 2`, ratio of the zero-threshold reading to the primary
(median-split) reading:

| | `E008` | `E016` | `E032` | `E064` | `E128` | `E256` | `F016` | `F064` | `F128` | `S064` | `S128` | `S256` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Planck | 0.21 | 0.001 | 0.72 | 1.01 | 1.05 | 0.90 | 0.66 | 1.04 | 0.93 | 0.90 | 0.90 | 0.77 |
| WMAP | 1.13 | 0.000 | 0.46 | 0.86 | 0.95 | 0.95 | 1.10 | 0.86 | 0.93 | 0.58 | 0.94 | 0.84 |

**Where the reading is above its floor the two thresholds agree to 15 %; where it is at the floor
they scatter by three orders of magnitude, which is what a `χ²₁`-shaped null does.** The
threshold moves by 5.4e−07 K on Planck (median vs zero) against a map σ of 1.08e−04 K, i.e.
0.5 % of σ; on WMAP it moves by 8.1e−04 mK against σ = 7.1e−02 mK, 1.1 % of σ. The reading does
not care. This is a stability check, not an independent reading:
the two thresholds share every pixel.

## 8. SMICA VERSUS WMAP — the free cross-instrument control

Two instruments, two component-separation pipelines, **one sky**, read through the **same sky
cut** (Planck's `TMASK` `ud_grade`d to `NSIDE` 512 with the fully-unmasked-superpixel rule;
`f_sky` 0.84241 and 0.83998). A real sky signal cannot appear in one and not the other except
through the instruments, so disagreement is foreground- or pipeline-attributable by construction.

**Scored on all 25 shared surviving cells: the largest disagreement is 1.82 σ and the median is
0.60 σ. Nothing exceeds 2 σ. The control PASSES.**

| | value |
|---|---|
| cells scored | 25 |
| max \|n σ\| | **1.82** (`E128|b3`) |
| median \|n σ\| | 0.60 |
| cells above 2 σ | **0** |

Each instrument's reading is normalised to its own matched floor and the difference is taken
against the quadrature sum of the two ensembles' relative scatters, as `PREREG` §7.3 registered.

**The control's power is very different at `b = 2` and at `b ≥ 3`, and saying so is part of
reporting it.** At `b = 2` the null's relative scatter is that of a `χ²₁` — the quadrature σ runs
**3.7 to 4.9** in units of floor-normalised reading — so the test could only have caught a
disagreement larger than about 9× in the floor-normalised reading. At `b ≥ 3` the null is narrow
and the quadrature σ runs **0.10 to 1.8**, and there the agreement is a real constraint: `E032|b3`
agrees to 0.46 σ on a σ of 0.099. **The sharp leg of this control is the `b ≥ 3` leg, and it is
the leg where the theorem does not apply** — which is worth knowing before anyone treats
cross-instrument agreement as confirmation of the `b = 2` null.

**A pre-registered secondary expectation FIRED, and `PREREG` §7.3 said its failure would be
informative.** It expected WMAP's beam-dominated small-θ rungs to carry a **higher** floor, on
the argument that a smoother field at fixed `N` has fewer effective independent triples. Measured:

| `b = 2` floor median (nats) | `E008` | `E016` | `F016` | `E064` | `E128` | `E256` |
|---|---|---|---|---|---|---|
| Planck | 1.243e−07 | 2.634e−07 | 3.895e−07 | 2.447e−06 | 2.375e−06 | 2.213e−06 |
| WMAP | **7.384e−08** | **1.579e−07** | **3.044e−07** | 4.892e−06 | 1.097e−05 | 1.669e−05 |

**WMAP's floor is LOWER than Planck's at exactly the three sub-beam templates the expectation was
made about, and higher everywhere else.** The reason is the one §6.2 already established and the
expectation did not use: the floor is set by **how uniform the table is**, not by `N_eff` alone.
At 8′ and 16′ WMAP's 1° beam makes the three slots nearly the same number, the feasible parity
direction is short, and the estimator's variance is *small*. The `N_eff` half of the argument was
right and the direction it was applied in was wrong. Recorded as a fired expectation, not
quietly dropped.

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

#### 9.1.1 The same arm on the SMICA map — the plumb line doubles, and one claim above weakens

Stage 5 ran the identical arm on the **data** map (`stage5_data.json::planck_boundary`), which
was not available when §9.1 was written.

**The plumb line holds on real sky data: `share(clip) == share(base)` returns `True` in all 18
data cases as well.** Combined with the surrogate arm, **clip is bit-for-bit invariant in 36 of
36 cases** — three `k`, three templates, two `b`, two maps. The flipped fractions on the data map
are 4.553e−02, 2.658e−03 and **5.663e−05** at `k = 1.0, 1.5, 2.0`, so the `k = 2` dye is **57
parts per million** here against 67 ppm on the surrogate.

**And it weakens something §9.1 says.** §9.1 argued that what carries the `k = 2` fold signal is
that *"all three templates move the same way"*. On the data map at `k = 2` all three also move the
same way — **in the opposite direction**: fold/base = 0.9232, 0.9771, 0.9945 at `E032`, `E064`,
`E128` (−7.7 %, −2.3 %, −0.55 %), against +1.69 %, +2.48 %, +2.25 % on the surrogate. If the sign
were a property of the perturbation both maps would agree; they do not. **The three templates
within one map share anchors and overlapping pixels, so their sign agreement is one piece of
evidence, not three**, and §9.1's sentence overstated it. The finding that survives, and it is the
one the gate needs, is the **discrimination**: clip is bit-zero in 36 of 36 and fold is nonzero in
36 of 36, at a perturbation of 57–67 ppm.

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

### 9.3 G7 — the valve arm, and the DOWNGRADE it carries

**Read the downgrade first, because it changes what this arm is.** `PLANCK_PILOT_AMENDMENT_5.md`
§2 found, before the arm ran, that it was citing a theorem whose hypothesis this pipeline does not
satisfy. `Core/Valve.lean`'s `valve_needs_asymmetry` is a statement about **kernels on `Bool`**:
its hypotheses are three flip-covariant `IsKernel` maps *and* a sign-symmetric input (verified
against the Lean signature in §13). `PREREG` §6.7 adds continuous noise to a continuous field and
binarizes **afterwards**, and `binarize(x + e)` is not a function of `binarize(x)` — a pixel just
above the threshold flips readily, one far above essentially never. **The composite is not a
per-cell channel on the binary alphabet, the binarization is not lumpable with respect to it, and
`valve_needs_asymmetry` does not license the N-sym prediction.**

The predictions are unchanged and their justification is cleaner: for a symmetric field `X` and
independent symmetric noise `E`, `X + E` is symmetric under global negation, so a split at the
symmetry centre gives a sign-symmetric table and the share is exactly zero **directly by
`share_eq_zero_of_signSymmetric`**, with no channel formalism at all. For skewed `E` the symmetry
breaks and the share may be nonzero.

**The consequence, stated as a downgrade and not buried: this pilot does NOT supply `GATES.md`
reach 9's missing valve plumb line.** `PREREG` §7.4 claimed it would. It does not, because it does
not test `valve_needs_asymmetry`. Reach 9's plumb line cell stays **NONE-YET** after this run —
and the arm built specifically to satisfy the hypothesis instead (G7b, §9.8) came back **VOID by
its own base check**, so that route did not rescue it either.

**What the arm did measure.** One S1 surrogate, noise added in pixel space at `ε ∈ {0.1, 0.5, 1.0}`
in units of σ, 20 realisations each, `b = 2`. Reported as the median of 20 against the *no-noise*
floor of 50 (`stage4_floor.json`); "mints" means the median clears that floor's p99.

| | `E032` | `E064` | `E128` |
|---|---|---|---|
| **N-sym**, `ε = 0.1` | 1.73× | 1.13× | 0.56× |
| `ε = 0.5` | 1.09× | 0.58× | 0.26× |
| `ε = 1.0` | 0.45× | 0.20× | 0.10× |
| **N-asym**, `ε = 0.1` | 1.63× | 1.15× | 0.59× |
| `ε = 0.5` | **14.59× MINTS** | 0.024× | 0.012× |
| `ε = 1.0` | **74.77× MINTS** | 0.82× | 0.30× |

**N-sym mints nothing at any ε on any template — 9 of 9 below the no-noise floor's p99, and
monotonically falling with ε.** The fall is expected and is not a null result about noise: symmetric
noise decorrelates the field, the feasible parity direction shortens, and the estimator's own
finite-sample floor drops with it (§6.2's mechanism). This is a **data-pipeline case for
`share_eq_zero_of_signSymmetric` under additive noise on a real sky field**, which is a filled
cell worth having — it is simply a different cell from the one `PREREG` §7.4 named.

**N-asym mints, hugely, and only at the most correlated template.** 14.6× and 74.8× the floor at
`E032`, and nothing at `E064` or `E128`, where it in fact *suppresses* the reading to 0.012–0.30×
at intermediate ε. The three templates' sign correlations, measured on a surrogate at the same
templates in §9.8, are ρ = 0.303, 0.138 and 0.112. A ρ⁴ scaling would
predict factors of 22× and 51× between `E032` and the other two, which is the right order for the
observed separation; that parallel is noted as **suggestive only**, because the pump rate law it
comes from is licensed for per-cell channels and this arm is exactly the one that is not.

So the pre-registered N-asym question — *does per-pixel skew alone mint on a Gaussian base at this
N?* — is answered **yes, at sufficient pair correlation**, which sharpens rather than settles the
sky campaign's attribution of its 5.8× floor to Poisson counting.

### 9.4 G8 — IPF versus the exact solver, in the interior and at the edge

`GATES.md` reach 12's dye test reads **VERIFIED at five orders of magnitude on near-deterministic
states, UNVERIFIED in the interior.** This arm measures the interior, on the same instrument and
in one run, against the exact 1-D solver that is the estimator everywhere in this pilot.

24 `b = 2` tables (12 templates × 2 instruments) spanning the near-uniform wide templates (the
interior) and the near-degenerate narrow ones (the edge):

| | Planck | WMAP |
|---|---|---|
| max \|IPF − exact\|, absolute | 1.55e−13 | **9.79e−13** |
| max \|ratio − 1\| | 2.9e−06 (`F016`) | **7.4e−06** (`E008`) |
| ratio at every wide template (`E064`…`S256`) | 1.000000 | 1.000000 |
| IPF iterations to `1e−13` | 7–31 | 10–**216** |
| max IPF certificate at `b ∈ {3,4}` (V7 bar `1e−12`) | 9.48e−14 | 9.77e−14 |

**In the interior IPF and the exact solver agree to every digit the certificate can resolve.** The
drift appears only at the near-degenerate rungs and it is at most **7 parts per million relative**
there — five orders of magnitude smaller than the 9.8e−6-against-1.2e−10 blowup
`ipf-sharek-boundary-drift` recorded on genuinely near-deterministic states, because these tables
are nowhere near deterministic. The iteration count is the better tell: WMAP `F016` needs **216**
iterations against 12 for WMAP's own `E128`, and iteration count tracks conditioning.

**No direction is claimed for the residual.** The differences are negative at the narrow templates
and positive at the wide ones on Planck, but they sit at 1e−13 to 1e−14 — the level of the IPF
convergence certificate itself — so the sign is solver tolerance, not drift. Claiming the
one-sided overstatement here would be reading a number below its own instrument's resolution.

**V7 does not fire.** Every `b ∈ {3,4}` cell met the `1e−12` certificate with three orders of
margin, so no cell was withheld on solver grounds.

### 9.5 G4 — the degrade arm: the filter is measured, not assumed

`ud_grade` to `NSIDE ∈ {512, 256}` — a top-hat over 16 and 64 pixels — applied **identically** to
the data and to a matched 100-realisation S1 floor at each level (`stage6_degrade_floor.json`,
2 × 100 realisations, 28 minutes). `PREREG` §6.4's registered expectation: the `b = 2` reading
stays at its floor because a linear filter of a Gaussian field is Gaussian, and **"if the b = 2
reading rises above its own matched floor under degrading, the filter is minting, and that is the
single most important thing this pilot could find."**

**At `b = 2` it does not, on 23 of 24 cells.** The one crossing is `S064|b2` at `NSIDE 512`
(5.796e−06 against a matched floor p99 of 5.011e−06, ratio-to-median 16.2). It is reported because
it was named in advance, and it is not a finding: **one cell of 24 above p99 is a 21 % event by
construction**, the same cell reads 0.14× its floor at `NSIDE 256`, and it reads 0.88× — *below*
its floor median — undegraded. A minting filter would not appear at one resolution and vanish at
the next.

**At `b = 3` the filter does move the reading, on exactly the templates where the theorem does not
apply.** Three of 24 `b = 3` cells clear their matched p99 — `E008|b3` at both degrade levels
(1.12× and 1.49× the floor median) and `F016|b3` at `NSIDE 256` (1.63×) — against 0.24 expected.
Those are the narrowest templates, where §6.3 measured the discretisation term to be 19 000× the
`b = 2` floor, and a top-hat over 16 or 64 pixels changes precisely the small-scale content that
term is made of. **This is the pre-registered asymmetry, cleanly: the filter leaves the
theorem-pinned rung alone and shifts the rung with no theorem behind it.**

**The floor's behaviour under degrading is the other registered quantity, and it is NOT
monotone.** `PREREG` §6.4 expected the floor to *fall* as the effective number of independent
triples falls. At `NSIDE 512` it does, on **9 of 12** templates; at `NSIDE 256` it **rises on 12
of 12**, by 1.1× to 2.0× (`E008|b2`: 1.243e−07 → 9.867e−08 → 1.742e−07; `F128|b2`: 2.218e−06 →
1.717e−06 → 4.387e−06). The registered direction is right for one step of degrading and wrong for
two, which is §6.2's finding again: **the floor is set by how uniform the table is**, and a
top-hat smooths the field toward degeneracy (lowering the floor) while simultaneously destroying
independent pixels (raising it). Which term wins depends on where the template sits relative to
the new pixel scale. The floor is a property of the sampling geometry, as §5.3 says, and it must
be re-measured after any change to that geometry rather than extrapolated — which is what the
matched 100-realisation floor at each level was for.

### 9.6 G1 — LP pair-pinning: no cell is pair-determined

`share_range_given_pairs` on every `b = 2` data table: the interval the share could occupy over
all distributions carrying the observed pair marginals. `GATES.md` reach 4 fires on a **collapsed**
feasible set — the registered bar is that the width be at least **100×** the reading's own scale.

| | Planck | WMAP |
|---|---|---|
| LP width, range over 12 templates | 0.107 – 0.580 nats | 0.00296 – 0.489 nats |
| **min width ÷ reading** | **3.2e+04** (`E128`) | **2.5e+03** (`F016`) |
| max width ÷ reading | 3.2e+06 (`E016`) | 1.3e+06 (`E008`) |
| min width ÷ floor median | 2.1e+05 | 9.7e+03 |

**The narrowest margin on either instrument is 2 463× the reading's own scale, against a
registered bar of 100×** — a factor of 25 inside the gate on the worst cell and five orders of
magnitude inside it on the best. Not one cell is pair-determined; the feasible set is enormous
next to everything measured in it, and the reading is a genuinely whole-only quantity throughout.
**G1 does not fire.**

The width itself carries §6.2's pattern again: it grows monotonically with separation (0.18 → 0.58
nats on Planck, 0.044 → 0.49 on WMAP) because wide triples are near-uniform and near-uniform
tables have long parity directions. The one visible outlier is WMAP `F016` at 0.00296 nats — a
folded 16′ triple at `NSIDE 512`, the most degenerate geometry in the ladder, where the feasible
set really is short. Even there the width is 2 463× the reading.

### 9.7 G3 / V5 — mask sensitivity, and the polarity criterion's own false-fire rate

Primary cut `TMASK` (`f_sky` 0.842/0.840) against the conservative cut `TMASK ∧ |b| > 30°`
(`f_sky` 0.494/0.494), with the polarity declared before the run: **the gate fires when the two
cuts DISAGREE by more than the conservative cut's own surrogate scatter**, and a *larger* reading
under the tighter cut fires it exactly as a smaller one does.

**Under the literal criterion it fires on 8 of 24 cells** (Planck `E128` 2.18σ and `F128` 1.11σ;
WMAP `E032` 2.49, `E064` 1.89, `E128` 1.93, `F064` 2.04, `S064` **3.35**, `S128` 1.07). **Under
the joint null scatter of the difference** — `√(σ²_primary + σ²_conservative)`, which is the
scatter the *difference* actually has, since both sides are single draws of heavy-tailed nulls —
**it fires on 6 of 24**, worst 2.04σ.

**That is not evidence of mask dependence; it is the arithmetic of a 1σ bar.** A 1σ threshold on a
two-sided difference fires on about 32 % of null cells, i.e. **7.7 of 24 expected**, against 8
observed under the literal form and 6 under the corrected one. Every conservative-cut reading sits
inside its own matched floor (empirical `p` from 0.35 to 0.97 on Planck and 0.50 to 0.98 on WMAP;
not one below 0.34). **V5 does not fire, and G3 PASSES.**

**The correction the run supplies to the criterion.** As registered, the gate had (i) a
one-sided denominator on a two-sided quantity, and (ii) **no stated false-fire rate**, which
`GATES.md` design rule 3 names as the way a gate ends up in arrears. A future version should
register the bar against the joint null with the rate written down — at 1σ this gate cries wolf
on a third of the cells it inspects, and at that rate it will be switched off rather than
believed.

One pattern is worth recording without over-reading it: **21 of the 24 conservative readings sit
below their own floor median** (Planck ratios 0.004–1.84, WMAP 0.002–1.07). The conservative cut
holds `N_kept` fixed while halving the available sky, so its triples overlap more, its floor rises
(Planck `E128`: 3.029e−06 against 2.375e−06 primary) — and the readings do not rise with it. On 24
correlated cells from one sky that is an observation, not a measurement.

### 9.8 G7b — the pump rate law on sky geometry: VOID by its own base check

Declared in `PLANCK_PILOT_AMENDMENT_5.md` §2.1 before it ran, and armed with the base-symmetry
verification Amendment 6 added: *"G7b reports the base's sign-symmetry statistic before any channel
is applied, and a base failing it voids the arm."*

**The base failed it. The arm is VOID as a test of the law, by its own pre-registered gate.**
`χ²` = 45.35, 61.55, 21.94 at `E032`, `E064`, `E128`, all with `p < 0.001` against the `p > 0.01`
bar; `axis` was written to the output as `MIXED -- see base_sign_symmetry` rather than
`channel (base sign-symmetric)`.

**And per §7.5 that check is the one whose null this pilot has shown to be wrong** — the base is a
phase-randomised surrogate, sign-symmetric *by construction*, and the same statistic rejects on 7
of 9 such maps. Deflated by the measured `N/N_eff`, the three `χ²` become 3.4, 1.5 and 0.5 against
a `χ²₄` median of 3.4. So the arm is very probably on the channel axis after all, and the pilot
cannot demonstrate it with what is on disk. **The verdict stands as written: VOID, numbers
reported as diagnostic, no verdict on the law.**

**The numbers, as diagnostic.** ρ measured from the sky triples — 0.3026, 0.1377, 0.1115 — three
values `pump-curve` did not choose. Prediction is their closed form with zero free parameters, and
their `c(r₀)` correction where `r₀` sits inside their measured grid (extrapolation refused).
Measured is the median of 24 realisations minus a channel-free floor at the same `N`.

| geometry | `a` | measured ÷ closed, `E032` / `E064` / `E128` | ÷ corrected |
|---|---|---|---|
| tied `s` | 0.01 | 3.42 / 22.91 / 9.54 | 3.41 / 22.90 / 9.54 |
| | 0.03 | 1.62 / 5.27 / 3.21 | 1.61 / 5.25 / 3.20 |
| | 0.10 | 1.21 / 2.00 / 1.76 | 1.18 / 1.92 / 1.69 |
| fixed `s` = 0.10 | 0.10 | 1.23 / 2.10 / 1.53 | 1.19 / 2.02 / 1.47 |
| | **0.20** | **1.25 / 1.72 / 1.51** | **1.10 / 1.47 / 1.29** |
| symmetric (`a` = 0) | 0.00 | +4.8e−07, −4.5e−07, −1.7e−06 nats — **at the floor, both `s`** | — |

**The `a = 0` control is clean**: six readings, all within ±2e−06 nats of the floor, three of them
negative. A symmetric per-cell channel mints nothing, measured on sky geometry.

**The disagreement's shape is the tell that it is not about the law.** `measured/closed` falls
monotonically from 22.9 to 1.2 as `a` rises — **worst exactly where the closed form is most
exact**, since `c` is *defined* as `lim_{a→0} δ/a²`. A defect in the law would go the other way,
and the arm's own docimasia on synthetic sign-symmetric triples measured the deviation at
+3.0 %/+9.2 %/+13.0 % at `a` = 0.10/0.15/0.20, i.e. `∝ a²` and exact as `a → 0`. Something additive
is sitting under the sky arm and being outgrown.

**The pilot names the two candidates it did not resolve, rather than adjudicating between them:**

1. **The arm's zero point is the ensemble floor median, not its own `a = 0` map.**
   `PLANCK_PILOT_AMENDMENT_3.md` §2 established for the dye arm that *"the arms' reference is not
   the ensemble at all; it is their own `f = 0` map"*, because a single draw of a `χ²`-shaped null
   routinely sits several times its median — D0's `f = 0` value was **5.9×** the floor median.
   **G7b did not inherit that fix.** An unsubtracted base share of ~1.6e−05 at `E032` would account
   for the small-`a` rows outright. That is above the arm's own channel-free floor p99 of 6.9e−06,
   so it is a tail draw — but the arm uses **one** base map read at three correlated templates, and
   one tail draw drags all three together, which is the pattern observed.
2. **The base's residual asymmetry.** `|m|` up to 7.2e−04 on the three bases. By §7.5's arithmetic
   the state-axis floor at that detuning is 0.2–0.6 % of the arm's own floor, far too small to
   explain the offsets — so this candidate is *disfavoured by measurement*, and named only so that
   the record shows it was checked rather than ignored.

**Two disclosures this arm owes.**

*The docimasia cannot be re-run as committed.* `planck_pilot_g7b_gate.py` line 33 unpacks four
values from `pump_law`, which has returned six since commit `7eb5a0c` added `c(r₀)`. The gate
script raises before it prints. Its results survive only in commit `7241e64`'s message and **the
script writes no artifact**, so those numbers are not re-derivable from a stored file. That is the
*gate-log provenance* gate firing on this campaign's own gate, and the fix is one line.

*The law and its correction table are `pump-curve`'s, received and not re-derived here* (§13).
Nothing in this section is a result about the law, and the open question goes back to the pump
campaign with the arm's defects named.

## 10. THE VOID REGISTER

Every VOID condition of `PREREG` §8, with its verdict. Ungauged is a first-class outcome and is
reported as loudly as a detection (`GATES.md` axiological rule 1).

| | condition | verdict | where |
|---|---|---|---|
| **V1** | occupancy ≤ 100 in any histogram cell | **FIRES — 12 of 72 cells ungauged and excluded.** Planck 1 (`E008\|b4`, min_occ 44); WMAP 11, seven of them at exactly 0. Primary grid 72 → **60**. Leave-one-out null recomputed on the surviving grid, as V1 requires | §6.4, §7.4 |
| **V2** | tied fraction not computed | **does not fire.** Disclosed for every reading; max **2.868e−06** on any primary or conservative pass, 4.293e−06 on the degraded passes, exactly 0 on the zero-threshold pass | §7.4 |
| **V3** | floor drawn at a different `N_kept` | **does not fire.** `N_kept` asserted equal between the data pass and every surrogate pass: **0 mismatches**, both instruments | §7.4 |
| **V4** | D1 dye invisible at every registered `f` | **does not fire.** The dye is visible up to **216×** its own `f = 0` value. The *conjunction over three templates* that defined the registered detection limit is never satisfied, and that is reported as the criterion failing, not as V4 | §9.2 |
| **V5** | primary and conservative cuts disagreeing beyond the conservative scatter | **does not fire.** 8 of 24 cells cross the literal 1σ bar and 6 of 24 cross the corrected joint-null bar, against **7.7 of 24 expected by construction**; every conservative reading sits inside its own floor (`p` ≥ 0.34). The criterion's own false-fire rate is the finding | §9.7 |
| **V6** | S1 and S2 floors disagreeing beyond their scatters | **does not fire**, and it nearly fooled the analysis: median ratios 0.55–1.28 read like a 45 % systematic, and with the heavy-tailed null's own median standard error the largest separation is **1.14σ** | §6.4 |
| **V7** | IPF failing `1e−12` at `b ≥ 3` | **does not fire.** Max certificate **9.77e−14**, three orders inside the bar. No cell withheld on solver grounds | §9.4 |
| **V8** | surrogate `C_ℓ` or skewness fouled | **FIRED TWICE before any data reading, and is DISCHARGED.** First on a criterion that measured the verifier rather than the surrogate (withdrawn as unmeasurable); second on WMAP's delivered residual **dipole at 11.5 % of σ**, a real minting channel present in one map and absent from its own floor, removed by exact `ℓ < 2` quadrature. All three legs now pass on both instruments | §3 |

**One additional VOID, raised by an arm rather than by `PREREG` §8:** arm **G7b is VOID** by the
base-sign-symmetry check Amendment 6 attached to it — and §7.5 shows that check's nominal null to
be wrong for this pipeline's sampling geometry, so the arm is void *and* the gate that voided it is
miscalibrated. Both halves are on the record and neither is used to rescue the other (§9.8).

## 11. WHAT THIS RUN DISCHARGED IN `GATES.md`

Written so the registry can be updated from it. **Discharge is claimed only where the arm ran and
produced its number**; an arm that ran and failed is reported failed, and an arm that did not
deliver what `PREREG` §7.4 promised says so. The claims below are human-enforced, per
`Gate.mechanized`: nothing here fails a build.

### 11.1 Cells this run FILLS

| `GATES.md` cell | was | now | evidence |
|---|---|---|---|
| **reach 2, plumb line** | **NONE-YET** | **FILLED — a certified boundary-stable reading.** `share(clip) == share(base)` bit-for-bit in **36 of 36** cases (3 `k` × 3 templates × 2 `b` × surrogate and data). Not "ratio 1.000": the same float | §9.1, §9.1.1 |
| **reach 2, dye test** | UNVERIFIED at small differentials | **FILLED at 57–67 parts per million** — fold at `k = 2` moves the reading in 36 of 36 cases where clip moves it in 0. Its *sensitivity against the null* is separately weak and is stated as such | §9.1, §9.1.1 |
| **reach 5, plumb line** | **NONE-YET** | **FILLED — a b-stable reading with its manufactured fraction measured.** `b = 2, 3, 4` all consistent with their own surrogates on 60 cells; manufactured fraction **33–113 %** at `b = 3`, tabulated per template | §7.1 |
| **reach 5, dye test** | PARTIAL — no planted bin-artifact sweep | **FILLED** — the same planted dye read through two coarse-grainings: D1 moves a `b = 2` reading by **34×** and its `b = 3` counterpart by **+7.9 to +8.9 %** | §9.2 |
| **reach 12, dye test** | VERIFIED at the edge, **UNVERIFIED in the interior** | **FILLED in the interior** — IPF vs the exact solver on 24 `b = 2` tables spanning near-uniform and near-degenerate: agreement to **≤ 7.4e−06 relative**, and to every digit the certificate resolves at every wide template | §9.4 |
| **reach 13 (power of the control)** | UNVERIFIED as a general scheme | **FILLED for this statistic class** — the primary test was given a planted dye before it judged anything: correct PASS on null-drawn data, correct **ALARM** (`p` = 0.0033) on the same data ×30, with the gamma fit's KS `p` = 0.911 | §2.2 |
| **reach 1, plumb line** | held live; not pinned as a fixed regression case | **PINNED** — a real-sky case with a proved-zero answer, mask and beam included: 60 cells, two instruments, `X = 0`, stored in `stage5_data.json` and `analysis.json` | §7.1 |
| **reach 9, dye test** | VERIFIED at 130 % only | **EXTENDED** — an asymmetric per-pixel channel's minting curve against ε, on a real sky field: **14.6× and 74.8×** the floor at ρ = 0.30, nothing at ρ = 0.14 and 0.11 | §9.3 |
| **harvest: floor matched to sample size** | — | **instance recorded** — every floor drawn through the byte-identical selection at the same `N_kept`; V3 checked at 0 mismatches; and Amendment 3 caught the arm where it would have failed, *before* the run | §7.4, `AMENDMENT_3` |
| **harvest: null-shape before z** | — | **two instances** — the `χ²₁` shape confirmed on a real sky pipeline (mean/median 1.78–2.51, p99/median 12.5–17.8), and the V6 near-miss where a "45 % systematic" read as 1.14σ once the null's own uncertainty was used | §6.1, §6.4 |
| **harvest: null-construction sweep** | — | **instance recorded** — S1 and S2 quoted side by side on every cell; agreement at ≤ 1.14σ; S2's scatter up to 1.8× S1's, attributed to `C_ℓ` cosmic variance | §6.4 |
| **harvest: named-denominator reporting** (with its cap/floor amendment) | — | **compliance instance** — both denominators on every reading, min sharp-cap/floor margin **102×** against the `≥ 100` bar, nothing declared undefined; **plus a live instance of the amendment's second clause**, WMAP's worst cell being `E128` against `ln 2` and `E256` against the sharp cap | §7.2 |

### 11.2 Cells this run does NOT fill, including one it promised

| `GATES.md` cell | state | why |
|---|---|---|
| **reach 9, plumb line (data case)** | **stays NONE-YET** | `PREREG` §7.4 claimed the N-sym arm would supply it. **It does not.** `valve_needs_asymmetry` is a statement about kernels on `Bool` with a sign-symmetric input, and `binarize(x + e)` is not a function of `binarize(x)`, so the composite is not a per-cell channel. The arm supplies a data case for `share_eq_zero_of_signSymmetric` under additive noise instead — a real cell, a different one. **G7b, built expressly to satisfy the hypothesis, is VOID by its own base check.** Reach 9 does not get its valve plumb line from this pilot | §9.3, §9.8 |
| **reach 1, dye test** | **PARTIAL → PARTIAL, with a number** | The planted-amplitude sweep ran, but the registered detection limit was defined as a **conjunction over three templates** and the conjunction is never satisfied. Per-template: `E032` `f` = 0.1, `E064` `f` = 0.3, `E128` not attained at `f ≤ 0.3`. The registered number does not exist, because a filter of scale `θ_f` manufactures share on templates narrower than itself and barely touches wider ones | §9.2 |
| **reach 6, plumb line** | **PARTIAL** | `PREREG` §7.4 offered D1 as *"a planted real result the artifact sluice must pass, beside a data reading it must not."* The let-through half is supplied — D1 is visible at up to 216× its own zero. The sluice itself (reach 6 fires on *implausible precision*) was never run as a check in this pilot, so the cell is not discharged | §9.2 |
| **reach 8, plumb line** | **FILLED WITH A CORRECTION, not with a clean case** | The run is clean — G3 passes, every conservative reading inside its own floor. But the registered polarity criterion has a one-sided denominator on a two-sided quantity and **no stated false-fire rate**; at its 1σ bar it fires on ~32 % of null cells. Storing this run as "the case the gate must leave alone" would store a gate that does not leave clean cases alone. The **corrected** criterion (joint null scatter, with a rate) is what this run supplies | §9.7 |
| **reach 11, dye test** | **PARTIAL → PARTIAL** | The occupancy sluice fired correctly in advance on 12 of 72 cells with measured `min_occ`, which is a second real firing. **No planted-sparsity sweep was run**, so the fraction at which the gate is *obliged* to alarm remains unset | §6.4 |
| **reach 3, 4, 7, 10** | unchanged | Reach 4 was *exercised* and passed with a 2 463× margin (§9.6), which is a plumb-line-style pass on a reach that already holds both cells; reaches 3, 7 and 10 were not aimed at by this pilot |
| **harvest: gate-log provenance** | **DEFECT DISCLOSED against this campaign** | `planck_pilot_g7b_gate.py` can no longer run against its own instrument (four-value unpack, six-value return since `7eb5a0c`), and it writes no artifact, so its docimasia numbers survive only in a commit message | §9.8 |

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

## 13. THE WARRANT AUDIT (W2), APPLIED TO THIS DOCUMENT

`GATES.md`'s **warrant reach** is PROPOSED, not validated, and its sharpest procedure is **W2**:
when a correction lands on a citation, re-audit **every** citation of that object across every
document of the campaign. This pilot has caught itself on exactly that twice — Amendment 4's
denominator claim (§5) and Amendment 5's valve citation (§9.3) — so the finished document is
audited before it is committed.

### 13.1 Every Lean citation, checked against the theorem's ACTUAL hypotheses

Read from the source files, not from memory or from a sibling's summary.

| cited as | actual statement and hypotheses | verdict |
|---|---|---|
| `share_eq_zero_of_signSymmetric` (`Core/SignSymmetry.lean:312`) | `{p : Bool × Bool × Bool → ℝ} (hp : IsProb p) (hsym : ∀ a b c, p (a,b,c) = p (!a,!b,!c)) : share p = 0` | **CORRECT as used.** Three **binary** slots only, and the hypothesis is exactly the global sign flip a median split of a symmetric field produces. It licenses **nothing at `b ≥ 3`**, and this document pins zero only at `b = 2` |
| `share_le_log_two` (`Core/ThirdCap.lean:212`) | `{p : Bool × Bool × Bool → ℝ} (hp : IsProb p) : share p ≤ Real.log 2` — **no hypothesis on the pair marginals** | **CORRECT.** This is the denominator of every `b = 2` ceiling fraction here |
| `share_max_eq_log_two` (`ThirdCap.lean:223`) | attainment (`share_parity`) **and** the bound, conjoined | **CORRECT.** `ln 2` is the exact maximum, not a convention |
| `share_le_log_card_third` (`ThirdCap.lean:198`) | general `α β γ`, `[Nonempty γ]`, `IsProb p` ⟹ `share p ≤ log (Fintype.card γ)` — the bound is on the **third slot's** alphabet | **CORRECT as used**, and the reason is worth stating: all three slots in this pilot carry the same `b` levels, so `log b` is the right number. A substrate with unequal alphabets would have to use *its* third slot's card |
| `share_le_grouping_gaps` (`ThirdCap.lean:235`) | three orientations, `H(pairᵢⱼ) + H(margₖ) − H(p)`; the honest ceiling is their **minimum** | **CORRECT**, and `planck_pilot.py::sharp_cap` computes exactly that minimum over the three orientations |
| `valve_needs_asymmetry` (`Core/Valve.lean:719`) | three `IsKernel` maps on `Bool`, all three `IsFlipCovariant`, **and** `hps : SignSymmetric p` | **CORRECTLY WITHDRAWN**, and the precise reason matters: the arm's base *does* satisfy `SignSymmetric`, and it is the **kernel** hypothesis that fails outright — the composite `binarize ∘ (· + e)` is not a map on `Bool` at all, so `IsKernel`/`IsFlipCovariant` have nothing to attach to. The withdrawal is §9.3's downgrade and it is carried into §11.2 |
| `valve_from_nothing` (`Valve.lean:317`) | a **product** state through three kernels ⟹ share 0 | **not used as a live warrant here**; it appears only as `water`'s plumb-line construction in §5.3 |
| `share_parity` (`Core/Share.lean:307`) | `share parity = Real.log 2` | **CORRECT**; §2.1's estimator plumb line reads 6.931e−01 against it |
| "sorry-free and axiom-audited" | `Audit/AxiomAudit.lean` lines 260–264 carry `assert_no_sorry` and lines 568–572 `assert_standard_axioms` for all five `ThirdCap` theorems, with stored `#print axioms` output `[propext, Classical.choice, Quot.sound]`; `share_eq_zero_of_signSymmetric` likewise at lines 138 and 450. No `sorry` occurs in either file | **VERIFIED.** The audit lives at repository root `Audit/`, not `CIRISOntology/Audit/` |
| `shareK_le_of_pair_uniform`, `shareK_le_log_sub_pair` (§5's superseded-history paragraph) | both exist in `Core/ShareK.lean` (lines 187 and 151) with the hypotheses §5 describes | **CORRECT**, and both are named there only as superseded history |

**No Lean file was opened for editing and `lake` was never invoked.** These are reads.

### 13.2 Numbers taken from a sibling and NOT re-derived here

Tagged **received-not-measured** at the point of entry, per `GATES.md`. None of them is a
measurement of this pilot and none should be re-quoted from this document as one.

| number | source | where it is used |
|---|---|---|
| the pump rate law `18 r₀⁴a²/[(1+2r₀)(1+3r₀)(1−r₀)]` | `pump-curve`, `PUMP_RESULTS.md`, commit `2dc6cfc` | the prediction G7b compares against (§9.8) |
| the correction table `c(r₀)` at eight `r₀` values | `pump-curve`, `PUMP_AMENDMENT_4` §4.1, commit `fbcb3ea` | the corrected prediction column (§9.8) |
| the state-axis prefactor `K = 0.00712` and the `m²` law | `pump-curve`, `PUMP_AMENDMENT_11` | the branch arithmetic (§7.5) and Amendment 6 §4.0's threshold table |
| overlap penalties 1.9× (tetrahedral), 5.8–7.9× (dense liquid), 45× (ideal gas) | `water` | the comparison table in §5.3. This pilot's own 2.2–42× **is** measured here |
| the precision-budget formula `√(2 + 8N·share)/(2N·share)` | `water` | §5.2. Its consequences are computed here from it |
| glass's control printing **−1695 %** of a theorem-pinned zero | `glass`, via `GATES.md`, commit `4acfca8` | the reason the cap/floor margin is stated in §7.2 |
| the sky campaign's 66σ filter artifact, +1.6688 control skewness, 5.8× valve floor | `SKY_REALDATA_RESULTS.md` | §3, §9.2, §9.3 |
| Dalitz D2 and D7 as known-bad anchors | `3a7e029` | §5.3, §6.1, §6.4 |
| cross-substrate ceiling fractions: LFSR ~100 %, QPU ~8 %, Ising ridge ~0.66 %, array ~0.03 % | prior campaigns | the comparison line in §7.2 |
| G7b's own docimasia (`a = 0` mints zero; ρ-independence to ~1 %; deviation `+3.4a²`) | this campaign's commit `7241e64` **message** | §9.8. **The gate script writes no artifact and can no longer run**, so even our own number here is not re-derivable from a stored file — disclosed as a gate-log-provenance defect |

### 13.3 What W2 caught in this document

Two things, both recorded above rather than silently fixed:

1. **§9.1's sign-coherence argument was overstated.** It read the three templates' agreement in
   sign under the `k = 2` fold as three near-independent readings. The data map moves all three the
   *other* way, so the sign is a property of the realisation, not of the perturbation, and the
   templates share anchors. Corrected in §9.1.1; the gate's discrimination claim is unaffected.
2. **Amendment 6's sign-symmetry statistic was cited as though its `p`-value were readable.** It is
   not, on this sampling geometry: it rejects on 7 of 9 surrogates that are sign-symmetric by
   construction. Corrected in §7.5, and propagated to §9.8, where it is what voided G7b, and to
   §10, where the void is recorded together with the miscalibration of the gate that produced it.
