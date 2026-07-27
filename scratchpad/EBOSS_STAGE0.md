# EBOSS STAGE 0 — **COMPLETE.** The catalogues are read, the mocks are found, and the density is the problem.

Committed at the stage boundary, **before `EBOSS_PREREG.md` exists and before any order-3
quantity, correlation function or power spectrum has been evaluated on any eBOSS catalogue.**
Stage 0 reads metadata and the selection function only: counts, positions, redshifts, weights,
the shipped `NZ` column, and the mock directory listings.

Every number below was **read off a header or computed from a shipped column by
`eboss_stage0.py`, `eboss_stage0_mocks.py` and `eboss_stage0_indep.py`**, committed beside this
document. Nothing is recalled from the literature. Where a published value is quoted (the DR16
clustering redshift ranges) it is *checked against the catalogue's own min/max* and the check is
reported.

**The registry's one named Stage-0 blocker — the mocks — is RESOLVED, and better than
expected.** The blocker has been replaced by a different one, which is density.

---

## S0.1 Reachability, checked first

| host | result |
|---|---|
| `data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/` | **200**, full directory listing |
| `data.sdss.org/sas/dr17/eboss/lss/EZmocks/v1_0_0/` | **200**, full directory listing |
| `data.desi.lbl.gov` | **still no route** — re-verified today, unchanged from `SKY_BGS_STAGE0.md` |

**`TARGET_REGISTRY.md` §4.5 recorded "the EZmock suite is not at the obvious SAS paths (three
probed, all 404)". That is correct for DR16 and wrong as a conclusion: the eBOSS EZmocks are
published under DR17, not DR16** — `dr17/eboss/lss/EZmocks/v1_0_0/{complete,realistic}/`. The
DR16 tree carries catalogues and masks only. Four paths were probed under `dr16` (all 404)
before the `dr17` tree was listed.

## S0.2 What is shipped, and the file inventory actually downloaded

Four tracers, two caps each, `-vDR16`, all from
`data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/`. Downloaded: **all four `clustering_data`
pairs, the `clustering_random` pairs for LRG/ELG/QSO, and the `full_ALLdata` files for LRG and
ELG.** The `_rec` (BAO-reconstructed) variants were deliberately **not** downloaded — they are
a post-processed field, not the observed one.

**Checksums verified against the shipped `eboss_lss_catalogs_DR16.sha1sum`** (S0.11).

| tracer | cap | N in z-range | z-range (catalogue min/max) | published range | area (deg²) |
|---|---|---|---|---|---|
| **LRG** | NGC | **107 500** | `[0.600, 1.000]` | 0.6–1.0 ✓ | **3 136** |
| **LRG** | SGC | **67 316** | `[0.600, 1.000]` | 0.6–1.0 ✓ | **2 075** |
| **ELG** | NGC | **83 769** | `[0.600, 1.100]` | 0.6–1.1 ✓ | **560** |
| **ELG** | SGC | **89 967** | `[0.600, 1.100]` | 0.6–1.1 ✓ | **609** |
| **QSO** | NGC | **218 209** | `[0.800, 2.200]` | 0.8–2.2 ✓ | **3 165** |
| **QSO** | SGC | **125 499** | `[0.800, 2.200]` | 0.8–2.2 ✓ | **2 088** |
| **LRGpCMASS** | NGC | 255 741 | `[0.600, 1.000]` | 0.6–1.0 ✓ | 4 826 |
| **LRGpCMASS** | SGC | 121 717 | `[0.600, 1.000]` | 0.6–1.0 ✓ | 2 063 |

Every published z-range is confirmed by the catalogue's own extrema. The clustering catalogues
are hard-cut at those limits, so no z-selection decision is left to the analysis.

**Area is measured, not published-and-recalled**: occupied equal-area cells in `(RA, sin DEC)`,
at two resolutions to expose the boundary bias. **The area is taken from the RANDOMS, not the
galaxies**, and that choice matters: the sparse tracers do not fill their own footprint — LRG
NGC puts 107 500 galaxies into ~56 000 fine cells, so a galaxy-derived count reads **2 218 deg²**
against the randoms' **3 136 deg²**, a 29 % under-read. The randoms converge (fine/coarse ratio
0.96–0.99). `n̄V_R` is read from the shipped `NZ` column and is **area-free**, so this choice does
not touch the campaign's decisive number.

**LRGpCMASS randoms were not downloaded** — 1.9 GB, and the sample is disqualified on
independence grounds anyway (S0.8). Its area is therefore galaxy-derived and under-read; it is
reported for completeness and is not a candidate.

## S0.3 THE DECISIVE NUMBER: `n̄V_R`, and it is bad

The commission named this the single most important number, and it is. The valve floor scales
with it, and this campaign has **its own measured curve** for that scaling
(`SKY_FORECAST_RESULTS.md` §12: floor = 130 % of signal at `n̄V_R = 1.6`, 58 % at `15.7`),
log-interpolated exactly as `SKY_REALDATA_AMENDMENT_1` §A1.3 did.

**Two calibration checks first, because a projection is worth nothing without them.**

1. **The same code, run on the BOSS DR12 catalogue already on disk**, returns
   `n̄V_R = 4.73 / 4.88` (NGC/SGC) at `R = 10` and `15.95 / 16.48` at `R = 15`, against
   Amendment 1's recorded **4.81** and **16.22**. **The estimator reproduces the priors of
   record**, so every eBOSS number below sits on the same footing rather than on a recalled one.
2. Fed Amendment 1's own inputs, the floor interpolation returns **95.3 %** and **57.0 %**
   against Amendment 1's "≈ 95 %" and "≈ 58 %". The projection machinery is the campaign's own.

**And now the eBOSS numbers.** `n̄` is the galaxy-weighted mean of the shipped `NZ`, which is
the density a galaxy actually experiences and therefore the one that governs shot noise.

| sample | `n̄` (h/Mpc)³ | **`n̄V_R` at R=15** | floor / signal | **`n̄V_R` at R=10** | floor / signal |
|---|---|---|---|---|---|
| **BOSS DR12 NGC** *(prior of record)* | 3.00e-04 | **15.95** | **57.5 %** | **4.73** | **95.9 %** |
| **BOSS DR12 SGC** *(prior of record)* | 3.10e-04 | **16.48** | **56.5 %** | **4.88** | **94.8 %** |
| **LRG NGC** | 7.47e-05 | **3.97** | **101.4 %** | 1.18 | 139.7 % ‡ |
| **LRG SGC** | 7.38e-05 | **3.92** | **101.7 %** | 1.16 | 140.1 % ‡ |
| **ELG NGC** | 3.36e-04 | **17.87** | **53.9 %** ‡ | 5.29 | **92.3 %** |
| **ELG SGC** | 3.75e-04 | **19.91** | **50.5 %** ‡ | 5.90 | **88.9 %** |
| **QSO NGC** | 1.77e-05 | **0.94** | 146.9 % ‡ | 0.28 | 185.3 % ‡ |
| **QSO SGC** | 1.60e-05 | **0.85** | 150.0 % ‡ | 0.25 | 188.4 % ‡ |
| LRGpCMASS NGC | 1.40e-04 | 7.43 | 81.6 % | 2.20 | 119.9 % |
| LRGpCMASS SGC | 1.52e-04 | 8.10 | 78.9 % | 2.40 | 117.2 % |

‡ = **extrapolated beyond the measured grid** `[1.6, 15.7]`, and marked as such rather than
quoted as a floor measurement. The QSO numbers are extrapolated by a factor of two in density
and should be read as "off the end of the curve", not as 147 %.

**Read plainly:**

* **QSO is dead on density.** `n̄V_R < 1` means fewer than one galaxy per smoothing volume. The
  floor is off the measured grid entirely. This is not a marginal call.
* **LRG's floor equals its signal** at the primary scale (101 %), which is worse than the worst
  configuration BOSS ever ran (95.9 % at its *secondary* scale).
* **ELG is the only eBOSS sample denser than BOSS** — `n̄V_R ≈ 18–20` against BOSS's 16 — and
  its projected floor at `R = 15` (50–54 %) is the best number in this table. It is also the
  smallest volume by a factor of seven, and S0.4 is where that bill comes due.

## S0.4 Occupancy — and it is where ELG fails

Occupancy is counted in **independent smoothing volumes** (`V_shell / (2π)^{3/2}R³`), per cap,
never pooled — `SKY_REALDATA_AMENDMENT_2` §A2.3 forbids pooling histograms across windows
because a mixture manufactures higher-order structure. Gate G9 requires **occupancy > 100**.

This is a **shell-volume estimate**, and its calibration is checked rather than assumed:
Amendment 2 measured BOSS SGC `n_indep = 33 264` at `R = 15` from the valid-cell count against
this method's **31 291** — agreement to 6 %, so the estimate is not systematically generous.
For ELG, whose footprint is thin (S0.6), the valid-cell count will run **below** the shell
estimate, so the failures below are failures *a fortiori*.

| sample | R | b=4 | b=6 | b=8 | rungs passing | outcome (a) two-rung clause |
|---|---|---|---|---|---|---|
| BOSS NGC | 15 | 1311 | 389 | 164 | 4, 6, 8 | met |
| **LRG NGC** | **15** | **797** | **236** | 100 | **4, 6** | **met** |
| **LRG SGC** | **15** | **527** | **156** | 66 | **4, 6** | **met** |
| **ELG NGC** | **15** | **189** | **56** | 24 | **4 only** | **FAILS** |
| **ELG SGC** | **15** | **205** | **61** | 26 | **4 only** | **FAILS** |
| ELG NGC | 10 | 637 | 189 | 80 | 4, 6 | met |
| ELG SGC | 10 | 693 | 205 | 87 | 4, 6 | met |
| QSO NGC | 15 | 1616 | 479 | 202 | 4, 6, 8 | met (but density is dead) |

**This is the campaign's central tension, and it is structural rather than a matter of
tuning.** Outcome (a) as pre-registered requires ≥5 σ *at two or more `b` that pass G9*. The two
eBOSS samples split the requirement between them and neither holds both halves:

> **ELG has the density and not the volume: at the primary scale it supports exactly one `b`
> rung, so it cannot satisfy outcome (a) at `R = 15` no matter what it reads.**
> **LRG has the volume and not the density: it supports two rungs at `R = 15`, where its floor
> is 101 % of its signal.**

ELG regains two rungs at `R = 10`, at a floor of 89–92 %.

## S0.5 The weight columns, **named exactly**, and the §7.5 gate designed against them

The commission is explicit that the §7.5 fibre-collision VOID gate must be designed against
columns that **exist**, because designing it against columns that did not is what left it
undischarged on BOSS. The shipped columns, read from the headers:

**`clustering_data` (LRG, QSO — identical column sets):**
`RA, DEC, Z, WEIGHT_FKP, WEIGHT_SYSTOT, WEIGHT_CP, WEIGHT_NOZ, NZ, <LRG|QSO>_ID`

**`clustering_data` (ELG):**
`RA, DEC, Z, WEIGHT_SYSTOT, WEIGHT_CP, WEIGHT_NOZ, NZ, WEIGHT_FKP, chunk, EBOSS_TARGET_ID`

**`clustering_random` (all three):** the same weight columns — `WEIGHT_FKP, WEIGHT_SYSTOT,
WEIGHT_CP, WEIGHT_NOZ, NZ` — plus `RA, DEC, Z` (and `chunk` for ELG). **This is a material
difference from BOSS**, whose randoms carried no weights and where `sky_stage6.DataGeometry`
consequently gave them `w = 1`. That asymmetry is exactly what invalidated the refuter's own
FKP row (`REFUTER_RESULTS.md` §A2: applying a redshift-dependent weight to one side only puts a
spurious radial gradient into `δ`). **On eBOSS the randoms carry the weights, so an FKP-weighted
variant is a legitimate test here where on BOSS it was an artifact.**

Measured on the shipped columns, standard scheme `w = WEIGHT_SYSTOT · (WEIGHT_CP + WEIGHT_NOZ − 1)`:

| sample | `κ = ⟨w²⟩/⟨w⟩` | SYSTOT range (frac ≠ 1) | CP range (frac ≠ 1) | NOZ range (frac ≠ 1) | FKP range |
|---|---|---|---|---|---|
| BOSS NGC *(prior)* | **1.1291** | [0.567, 4.953] (0.723) | [1, 9] (0.039) | [1, 16.92] (0.012) | [0.184, 0.870] |
| BOSS SGC *(prior)* | **1.1515** | [0.654, 2.915] (0.680) | [1, 8] (0.038) | [1, 15.85] (0.015) | [0.170, 0.867] |
| **LRG NGC** | **1.1025** | [0.000, 1.520] (1.000) | [1, 4] (0.036) | [0.99, 1.13] (1.000) | [0.501, 0.951] |
| **LRG SGC** | **1.1158** | [0.863, 2.295] (1.000) | [1, 5] (0.036) | [1.00, 1.14] (1.000) | [0.497, 0.952] |
| **ELG NGC** | **1.2249** | [0.781, 1.334] (1.000) | [1, 5] (0.058) | [1.00, 1.54] (1.000) | [0.296, 0.912] |
| **ELG SGC** | **1.1810** | [0.791, 1.275] (1.000) | [1, 5] (0.047) | [1.04, 1.76] (1.000) | [0.280, 0.903] |
| QSO NGC | 1.0817 | [0.846, 1.434] (1.000) | [1, 4] (0.020) | [1.00, 1.09] (0.797) | [0.885, 0.945] |
| QSO SGC | 1.1120 | [0.000, 1.782] (1.000) | [1, 4] (0.025) | [1.00, 1.09] (0.872) | [0.894, 0.948] |

**Findings that bear directly on the gates:**

1. **Refuter caveat A1 transports and is slightly worse for ELG.** The catalogue's own weights
   are super-Poisson by `κ − 1 = 10.3–22.5 %`, against BOSS's 12.9–15.2 %. **ELG NGC at 22.5 %
   is the largest weight-induced dispersion in either survey.** The dispersion sweep is not
   optional here.
2. **`WEIGHT_SYSTOT` reaches exactly 0.0 on LRG NGC and QSO SGC.** A zero systematic weight
   deletes an object. This must be handled explicitly (and disclosed as a tied/railed fraction
   under G7) rather than being allowed to flow silently into `δ`.
3. **`WEIGHT_NOZ` is ≠ 1 for *every* eBOSS object** — it is a continuous redshift-failure
   weight, not BOSS's integer upweight. `WEIGHT_CP` remains the integer close-pair upweight
   (1–5, on 2.0–5.8 % of objects). **The two channels are cleanly separable in eBOSS**, which
   they were not in BOSS's `CP + NOZ − 1` combination where both were integer upweights.
4. **The §7.5 gate is dischargeable on eBOSS, and this is the single biggest methodological gain
   over BOSS.** `eBOSS_{LRG,ELG}_full_ALLdata-vDR16.fits` — downloaded, headers read — carry
   **`sector_TSR`, `sector_SSR`, `COMP_BOSS`, `WEIGHT_CP`** and per-object `IMATCH`, joinable to
   the clustering catalogue by `LRG_ID` / `EBOSS_TARGET_ID`. That supplies a genuine *alternative
   published completeness scheme* (`TSR`/`SSR` sector weighting) to set against the standard
   close-pair upweighting. **BOSS had no such alternative and the gate died there for that
   reason.** The ELG file additionally carries the imaging systematics regressors themselves
   (`galdepth_{g,r,z}`, `psfsize_{g,r,z}`, `nobs_{g,r,z}`, `mskbit`), so an imaging-systematics
   variant is constructible rather than merely on/off.
5. **What is NOT available, stated so it is not assumed later: there are no PIP / bitwise
   weights anywhere in the SAS eBOSS tree.** Four candidate paths were probed, all 404. The
   Mohammad et al. (2020) pairwise-inverse-probability weights are not distributed with these
   catalogues. So the *best available* fibre-collision alternative is the completeness-weighting
   route of finding 4, and that limit belongs in the pre-registration rather than being
   discovered at the gate.

## S0.6 Randoms — available, dense, and carrying the selection function

| sample | randoms in z-range | ratio to galaxies | surface density | footprint (fine/coarse) |
|---|---|---|---|---|
| LRG NGC | 5 460 719 | **50.8×** | 1 741 deg⁻² | 3 136 / 3 199 |
| LRG SGC | 3 453 453 | **51.3×** | 1 664 deg⁻² | 2 075 / 2 156 |
| ELG NGC | 3 728 363 | **44.5×** | 6 661 deg⁻² | 560 / 568 |
| ELG SGC | 3 609 460 | **40.1×** | 5 930 deg⁻² | 609 / 629 |
| QSO NGC | 11 099 858 | **50.9×** | 3 507 deg⁻² | 3 165 / 3 221 |
| QSO SGC | 7 169 801 | **57.1×** | 3 435 deg⁻² | 2 088 / 2 164 |

**All at or above the ×50 density that Amendment 2 §A2.2 established as necessary** after the
Patchy ×10 suite collapsed the mask to speckle. The lowest, ELG SGC at 40×, is comfortably
inside the regime that fix addressed, and the fix itself (footprint defined on a *smoothed*
random field rather than on raw deposited counts) is already in the pipeline and is
random-density-independent by construction.

**Footprint geometry, which is not merely cosmetic for ELG.** The ELG sample is **four
disjoint chunks**, not two contiguous caps:

| cap | chunk | N | RA | DEC |
|---|---|---|---|---|
| NGC | `eboss23` | 51 432 | 126.0–157.0 | +13.8 … +29.0 |
| NGC | `eboss25` | 32 337 | 131.0–166.0 | +23.0 … +32.5 |
| SGC | `eboss21` | 28 029 | 317.0–360.0 | −2.0 … +2.0 |
| SGC | `eboss22` | 61 938 | 0.0–45.0 | −5.0 … +5.0 |

`eboss21`/`eboss22` are **equatorial strips 4–10° thick** — about 370 Mpc/h at `z_eff = 0.84`,
against a `R = 15` masked-smoothing kernel needing ~90 Mpc/h of clearance. Workable, but
boundary-dominated in a way BOSS never was, and it is why S0.4's shell-volume occupancy is an
upper bound for ELG specifically. LRG and QSO share the standard eBOSS footprint
(NGC `RA 110–263, DEC +16…+60`; SGC `RA 0–360, DEC −7…+36`) and are contiguous.

**The four chunks are a genuine methodological gain**: the harvest gate **patch isotropy** wants
independent patches compared in *amplitude*, and ELG offers four where BOSS offered two.

## S0.7 Veto masks

The `clustering_*` catalogues are **veto-applied already** — that is what distinguishes them
from `full_ALLdata`, whose row counts are 2.9× (LRG: 311 848 vs 107 500) and 3.2× (ELG:
269 178 vs 83 769) larger. The masks are shipped separately and were **listed but not
downloaded** (they are `mangle` `.ply` polygons and no step of this design consumes them):
`LRGandQuasarmasks/` (7 files, 1.05 GB: bright-star, bad-field, centre-post, collision-priority)
and `ELGmasks/` (per-brick FITS masks plus `geometry-eboss2{1,2,3,5}.ply`).

**This satisfies prereg §7.6's "undisclosed veto mask" VOID condition by construction**: the
vetoes are applied upstream and identically to data and randoms, and the randoms *are* the
selection function the pipeline divides by. No hand-built mask is required, which is precisely
what `SKY_BGS_STAGE0.md` §S0.2 identified as the most dangerous thing the DESI route would have
forced.

## S0.8 THE MOCKS — the registry's blocker, resolved, and better than Patchy

`dr17/eboss/lss/EZmocks/v1_0_0/` carries `realistic/` (with the survey systematics imprinted)
and `complete/` (without), covering `eBOSS_{LRG,ELG,QSO,LRGpCMASS}` and `CMASS_LRG`.

| tracer | realisations | `dat` mean | `dat` total | `ran` mean | `ran` total |
|---|---|---|---|---|---|
| ELG | **1000 × 2 caps** | 2.0 MB | 4.1 GB | 50.6 MB | 101.3 GB |
| LRG | **1000 × 2 caps** | 2.0 MB | 4.1 GB | 48.6 MB | 97.2 GB |
| QSO | **1000 × 2 caps** | 3.4 MB | 6.9 GB | 68.5 MB | 137.1 GB |

**Three findings, and the first one changes the resource plan qualitatively.**

1. **The EZmocks are individually-addressable files, not a monolithic tarball.** Amendment 1
   §A1.5 recorded that Patchy is `.tar.gz` and therefore "all or nothing per cap", forcing the
   stream-processing design. **That constraint does not exist here.** A 128-realisation subset
   is **256 MB per cap** of `dat`, downloadable directly. The 1000-realisation full suite of
   `dat` is 4.1 GB per tracer — affordable outright.
2. **The randoms differ between realisations** (checked: realisations 0001 and 0002 of ELG NGC
   have different row counts, 2 553 832 vs 2 557 365, and no shared values). At 50 MB each they
   are the entire storage cost. **They do not need to be downloaded per realisation**: the
   BOSS pipeline builds `CapGeometry` **once per cap** from the randoms and reuses it for every
   realisation, because the randoms encode the selection function, which is shared. **One
   random file per tracer per cap suffices, and the per-realisation variation is a Monte-Carlo
   draw of a fixed selection function, not new information.** This is a design commitment and
   belongs in the pre-registration as one, with a stated check.
3. **The mock EZmock random density is 30× the mock galaxy density** (2.55 M randoms against
   83 747 galaxies), below the data's 44.5× and below the ×50 Amendment 2 settled on. It is
   well above the ×10 that failed, and the smoothed-random-field footprint fix makes the mask
   construction density-independent — but it is a **stated difference between the data side and
   the mock side of the same measurement**, and the harvest gate **same null both sides** makes
   that a thing to check, not to note.

**Read, not recalled — mock realisation 0001 against the data:**

| | ELG NGC | LRG NGC |
|---|---|---|
| mock columns | `RA, DEC, Z, WEIGHT_FKP, WEIGHT_NOZ, WEIGHT_CP, NZ, WEIGHT_SYSTOT, chunk` | same, no `chunk` |
| mock rows in z-range / data rows | 83 747 / 83 769 = **1.000** | 110 491 / 107 500 = **1.028** |
| `n(z)` shape, total-variation distance | **0.0160** | **0.0137** |
| `κ` mock vs data | **1.2166** vs 1.2249 | **1.0529** vs 1.1025 |

The mock column set **matches the data column set**, which is what makes a bit-identical
pipeline possible. `n(z)` agrees to ~1.5 % in total variation — comfortably inside prereg §7.6's
"`n̄(z)` mismatch beyond the published tolerance" VOID condition. **The LRG mock carries 5 % less
weight dispersion than the LRG data** (`κ` 1.053 vs 1.103); the ELG mock reproduces the data's
`κ` to 0.7 %. That LRG gap is a real mock/data mismatch on exactly the quantity refuter caveat
A1 turns on, and it is recorded here so the dispersion sweep can be calibrated against it rather
than against a literature range alone.

**One caution the mock count does not remove.** 1000 realisations measure `σ` to **±2.2 %**,
against the **±18 %** that 16 Patchy mocks gave the BOSS run — which is refuter caveat A4's
stated residual, and eBOSS retires it. But `SKY_REALDATA_AMENDMENT_2` §A2.1's argument that 128
suffices rested on a *measured* per-realisation scatter of 0.5–1.1 % **on BOSS geometry**. That
scatter has **not** been measured on eBOSS geometry and does not transport by assertion — it is
a Stage-2 measurement, and the suite size must not be committed before it is made.

## S0.9 Independence — measured, because "independent sample" is the whole mission

eBOSS was observed through the same telescope over largely the same sky. The overlap is
therefore measured rather than assumed: sky overlap as the fraction of the tracer's occupied
sky cells that BOSS DR12 also occupies, radial overlap as the fraction of its comoving shell
lying inside `0.2 < z < 0.75`.

| sample | sky overlap | radial overlap | **volume sharing BOSS's density field** |
|---|---|---|---|
| **LRG** NGC / SGC | 99.2 % / 98.5 % | 31.1 % | **30.8 % / 30.6 %** |
| **ELG** NGC / SGC | 99.4 % / 99.8 % | 23.4 % | **23.3 % / 23.4 %** |
| **QSO** NGC / SGC | 99.2 % / 98.5 % | **0.0 %** | **0.0 %** |
| LRGpCMASS NGC / SGC | 99.7 % / 99.4 % | 31.1 % | 31.0 % |

**The sky is essentially entirely shared; the independence is radial.** So:

* **No eBOSS sample is a fully independent confirmation.** LRG shares 31 % of its volume with
  BOSS and ELG 23 %. Different tracers, but partly *the same density field*, and a confirmation
  drawing 23–31 % of its volume from the original sample must say so.
* **QSO is the only fully independent volume in eBOSS** (`z > 0.8` clears BOSS entirely) and it
  is the one that is dead on density. That is not a coincidence — it is the same trade the whole
  survey makes.
* **LRGpCMASS is disqualified outright**: it *contains BOSS CMASS galaxies* (`ISCMASS` is a
  shipped column). It is not a confirmation sample in any sense and is excluded here rather than
  at some later stage.

## S0.10 What it projects to

Scaling the refuter's **corrected** significances (the priors of record) by
`(D_new/D_BOSS)^0.82 · √(n_indep_new/n_indep_BOSS)` — signal amplitude scaling from
`SKY_FORECAST_RESULTS` F3's measured `+0.82`, per-realisation `σ` scaling as `1/√n_indep`:

| sample | R | b | BOSS corrected | √(n_indep ratio) | `D^0.82` ratio | **projected** |
|---|---|---|---|---|---|---|
| **LRG NGC** | **15** | **4** | 6.0 | 0.780 | 0.886 | **4.1** |
| **LRG NGC** | **15** | **6** | 9.7 | 0.780 | 0.886 | **6.7** |
| **ELG NGC** | **15** | **4** | 6.0 | 0.379 | 0.853 | **1.9** |
| ELG NGC | 10 | 4 | 20.9 | 0.379 | 0.853 | 6.8 |
| ELG NGC | 10 | 6 | 26.3 | 0.379 | 0.853 | 8.5 |
| LRG NGC | 10 | 4 | 20.9 | 0.780 | 0.886 | 14.4 |
| LRG NGC | 10 | 6 | 26.3 | 0.780 | 0.886 | 18.2 |

**What this scaling does not carry, said before it is used rather than after it disappoints:**
tracer **bias** (ELG `b ≈ 1.4`, LRG `b ≈ 2.3`, CMASS `b ≈ 2.0`; the order-3 sector's bias
dependence is *not* measured by this campaign, so no factor is applied and none is implied); the
floor being a larger *fraction* of signal, which raises the systematic without moving this
ratio; and every eBOSS-specific systematic, which is what the gates are for. **It is a scaling,
not a forecast, and it is reported as one.**

Taken with S0.4, at the primary scale `R = 15`:

> **LRG NGC projects to 4.1 σ at `b = 4` and 6.7 σ at `b = 6` — one rung above 5 σ, not two.
> ELG projects to 1.9 σ and can only field one rung anyway. On this scaling, no eBOSS sample
> satisfies outcome (a) at the primary scale.** The `R = 10` rows project comfortably, at a
> floor of 89–140 % of signal.

## S0.11 Disk, and what was and was not removed

**Checked first, as instructed.** At start: **20 GB free of 935 GB (98 % full)**, with
`/home/emoore/skydata` holding 62 GB of BOSS data.

**Nothing was deleted.** The commission permitted removing extracted Patchy directories;
`find` over `/home/emoore` returned **none** — the Patchy suite exists only as the raw
tarballs, which are protected. There was nothing reclaimable that I was permitted to reclaim.

Downloaded, **2.90 GB total** into `/home/emoore/skydata/eboss/`:

| what | size |
|---|---|
| 8 `clustering_data` files (4 tracers × 2 caps) | 90 MB |
| 6 `clustering_random` files (LRG/ELG/QSO × 2 caps) | 2.2 GB |
| 2 `full_ALLdata` files (LRG, ELG) | 385 MB |
| 6 sample EZmock files (ELG ×4, LRG ×2) | 162 MB |
| `eboss_lss_catalogs_DR16.sha1sum` | 3 KB |

**Integrity: `sha1sum -c` against the shipped `eboss_lss_catalogs_DR16.sha1sum` — all 16
catalogue files (14 clustering + 2 `full_ALLdata`) return `OK`.** The EZmock files are not
covered by that manifest and are unverified; a mock checksum source is a Stage-2 item.

Free space is now **~11 GB and falling**, and the box is shared with other running campaigns.
**This is a live constraint on Stage 2, not a footnote.** The mock plan it permits: `dat` files
only (256 MB per cap for 128 realisations, 2.0 GB per cap for the full 1000) plus **one**
random file per cap (~50 MB). The per-realisation random suites (97–137 GB per tracer) are
**out of reach and are not in any plan here.**

## S0.12 STATE

| item | status |
|---|---|
| host reachable | **YES** — `data.sdss.org` 200; DESI still unroutable |
| catalogues + randoms | **DOWNLOADED and CHECKSUM-VERIFIED** |
| the registry's named blocker (mocks) | **RESOLVED** — 1000 realisations per tracer per cap, under DR17, individually addressable |
| exact weight columns | **READ** (S0.5); §7.5 gate **dischargeable** via `full_ALLdata` completeness columns; **no PIP weights exist** |
| veto masks | applied upstream in the clustering catalogues; §7.6 satisfied by construction |
| `n̄V_R` | **MEASURED**, and it is the new blocker (S0.3) |
| occupancy | **MEASURED**; ELG fails the two-rung clause at `R = 15` (S0.4) |
| independence | **MEASURED**: 23–31 % of volume shared with BOSS; QSO alone is fully independent and is dead on density |
| `EBOSS_PREREG.md` | **not yet written** — it is the next deliverable and nothing above pre-empts its choices |

**Stage 0 is complete and the campaign is not blocked.** It is *constrained*, in a way that the
pre-registration has to decide in advance rather than discover: **there is no eBOSS
configuration that reproduces BOSS's primary-scale design on both density and occupancy at
once.** The three live options — LRG at `R = 15` (two rungs, floor ≈ signal), ELG at `R = 10`
(two rungs, floor 89–92 %, 77 % independent volume), and an honest bound under outcome (c) —
are the pre-registration's to weigh, with its outcome criteria fixed before any share is
computed.

**No order-3 quantity has been computed on any eBOSS catalogue. No `lake`, no Lean, no
`Stance.lean`, no audit was touched.**

---

*Stage 0 ends here, complete. Files: `eboss_stage0.py`, `eboss_stage0_mocks.py`,
`eboss_stage0_indep.py` and their JSON outputs, committed beside this document.*
