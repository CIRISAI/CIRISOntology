# GLASS_DATA — the inventory, before any share is computed

**Stage 1 of the glass-transition campaign.** This document reports what is in the data and
nothing else. **No share, no order-3 quantity, and no campaign observable of any kind is
computed here.** The only structural quantity measured below is the **pair correlation
function** `g_αβ(r)`, which the campaign's instrument is blind to by construction and which has
been published for this model since 1995; it is measured here to fix the box edge, to confirm
the data is the model it claims to be, and to state where the coordination shells sit.

**SCOPE.** Simulated glass formers, not experimental glasses. A measurement contributing to a
decades-old dispute, not a solution to the glass transition. Nothing here bears on
`wild-share`; nothing here moves `Stance.lean`. No Lean file opened, `lake` never invoked.

---

## 1. THE SOURCE, AND ITS REACHABILITY

| | |
|---|---|
| **record** | Zenodo **10.5281/zenodo.10118191**, "GlassBench", creator **Gerhard Jung**, published **2023-11-21** |
| **licence** | **CC-BY-4.0** — redistribution and re-use permitted with attribution |
| **files** | `README` (2 147 B, md5 `f1a192f5…`) and `GlassBench.zip` (**6 042 260 027 B**, md5 `82c83a71…`) |
| **reachable** | **Yes**, with a caveat worth recording |

**The caveat, because it cost an hour.** The API endpoint
`https://zenodo.org/api/records/10118191/files/GlassBench.zip/content` answers **HTTP 206** on
ranges of a few MB but returns **HTTP 504** on anything larger — reproducibly, at 5 MB and at
20 MB, after a 30 s gateway timeout. The plain download URL
`https://zenodo.org/records/10118191/files/GlassBench.zip?download=1` serves the **same object**
with working ranges at **≈ 645 kB/s sustained** (measured on a 60 MB range). Metadata queries
are fine on the API (`x-ratelimit-limit: 133`).

**How it was fetched, and why not simply `wget`.** This box is at **99 % disk** with **5.7 GB
free** at the time of writing, and other work on the machine is consuming it. The archive
carries a **zip64 central directory**, and Zenodo honours HTTP ranges, so the central directory
was parsed once (`glass_zipfetch.py`) and only the members this campaign needs were pulled —
each one converted to a compact form and **the tarball deleted before the next was fetched**.
Peak extra disk: one tarball. Full manifest in §2, obtained **without downloading the archive**.

**One corruption incident, recorded rather than glossed.** Two downloader loops were
accidentally left running concurrently and appended to the same partial file, producing a
1.13 GB "member" where 590 MB was expected. It was caught by a size check, the partials were
deleted, and the fetcher now (a) runs under `flock` and (b) **verifies the zip's own CRC32 and
uncompressed length end-to-end** before a member is accepted. Every byte reported below passed
that check.

---

## 2. THE FULL MANIFEST — what is in the archive

Read from the zip64 central directory. 70 entries; the ones carrying data:

| member | uncompressed | what it is |
|---|---|---|
| `KA_models/T0.44.tar.gz` | 591 125 630 | 3D Kob–Andersen, **T = 0.44** |
| `KA_models/T0.50.tar.gz` | 581 122 195 | 3D Kob–Andersen, **T = 0.50** |
| `KA_models/T0.56.tar.gz` | 580 507 860 | 3D Kob–Andersen, **T = 0.56** |
| `KA_models/T0.64.tar.gz` | 580 090 855 | 3D Kob–Andersen, **T = 0.64** |
| `KA2D_models/T0.23.tar.gz` | 41 742 813 | 2D ternary, **T = 0.23** |
| `KA2D_models/T0.30.tar.gz` | 291 624 322 | 2D ternary, **T = 0.30** |
| `KA2D_trajectories/T0.23.tar.xz` | 397 384 372 | 2D isoconfigurational **trajectories** |
| `KA2D_trajectories/T0.30.tar.xz` | 2 979 229 176 | 2D isoconfigurational **trajectories** |
| `{KA,KA2D}_results/*` | ~40 kB total | figure scripts and their `.dat` inputs |
| **total** | **6 045 492 319** | |

**A finding, stated because it changes what is possible.** `KA_trajectories/` contains **only a
README** — 518 bytes. **The 3D Kob–Andersen isoconfigurational trajectories are NOT in this
archive.** Its README points to a separate repository
(`https://github.com/h3-Open-BDEC/pyg_botan`). What *is* here for the 3D system is
`KA_models/`, which despite the name contains the **configurations themselves** (§3), and that
is all this campaign needs — the question is **static**.

**What this campaign downloaded: the six `*_models` tarballs only, 2.67 GB.** The two
`KA2D_trajectories` tarballs (3.38 GB) were **deliberately not fetched**: they carry particle
*displacements* over time, which are the **dynamical** side of the benchmark. A static-order
campaign must not have a dynamical label anywhere near its estimator, and on a disk at 99 % the
cheapest way to guarantee that is not to have the file.

---

## 3. WHAT IS INSIDE — verified by reading the arrays, not the README

Each tarball holds one `.npz` per structure, under `T{temp}/{train,test}/`. Keys present,
read off the files:

**3D KA** (`N4096T{temp}_{1..500}.npz`) — `types`, `initial_positions`,
`initial_positions_inherent`, `initial_positions_cage`, `md_prop`, `bb_prop`, and for the test
split `BOTAN`, `CAGE`, `GlassMLP`, `SE3`, `SBO`, `SBO_CG`, `DEN`, `EPOT`, `PSI6`.

**Only three of these are retained** by `glass_convert.py` — `types`, `initial_positions`,
`initial_positions_inherent`. Everything else is a *dynamical propensity* or a *model
prediction*, and is discarded at ingestion so it cannot leak into a static reading.

### 3.1 The verified state points

| state point | configs | N | dim | box `L` | ρ | composition | inherent structures |
|---|---|---|---|---|---|---|---|
| **KA T=0.44** | **500** (400 train / 100 test) | 4096 | 3 | 15.0566 | **1.2000** | 3277 A : 819 B = **0.80005 : 0.19995** | **500 / 500** |
| **KA T=0.50** | **500** | 4096 | 3 | 15.0566 | **1.2000** | same | **500 / 500** |
| **KA T=0.56** | **500** | 4096 | 3 | 15.0566 | **1.2000** | same | **500 / 500** |
| **KA T=0.64** | *(see §6)* | 4096 | 3 | 15.0566 | 1.2000 | same | |
| **KA2D T=0.23** | *(see §6)* | 1290 | 2 | 32.8962 | 1.192 | ternary | |
| **KA2D T=0.30** | *(see §6)* | 1290 | 2 | 32.8962 | 1.192 | ternary | |

**Positions only. No velocities anywhere in the archive.** For a static-structure campaign that
is not a limitation, and it is worth saying plainly: there is no momentum information to
mis-use.

**The box was determined from the data, not assumed.** Coordinates are wrapped into
`[−L/2, L/2)`; the observed particle extent is `2 × 7.5282998 = 15.056600`, and the nominal
edge at the model's density `ρ = 1.2` is `(4096/1.2)^{1/3} = 15.056578`. **Relative
disagreement `< 1.5 × 10⁻⁶`** — the box is filled to its edge and `ρ = 1.2` exactly, as the
Kob–Andersen model specifies. The 2D box is stated in the dataset's own README as `32.8962`,
giving `ρ = 1290/32.8962² = 1.1919`.

### 3.2 It is the model it says it is — the pair structure

Species-resolved `g_αβ(r)`, 40 configurations per state point, minimum image:

| | `g_AA` peak | `g_AB` peak | `g_BB` peak | `g_AA` onset | `g` tail |
|---|---|---|---|---|---|
| **T = 0.44** | **1.070** (4.263) | **0.890** (5.351) | **1.390** (1.652) | 0.970 | 0.992–1.001 |
| **T = 0.50** | 1.070 (4.051) | 0.870 (5.079) | 1.390 (1.527) | 0.970 | 0.993–1.002 |
| **T = 0.56** | 1.070 (3.911) | 0.870 (4.955) | 1.430 (1.470) | 0.950 | 0.993–1.000 |

This is the Kob–Andersen mixture and nothing else: the AB peak sits **inside** the AA peak
(`σ_AB = 0.8`), and **`g_BB` is strongly suppressed at contact with its first peak pushed out to
1.39–1.43** — the model's defining B–B avoidance. All tails go to 1 within 0.8 %.

**One consequence, flagged here because the pre-registration must carry it.** B–B contacts are
rare at the first coordination shell. The **BBB cell** of the campaign's eight-cell table will
therefore be the sparse one, and the small-`r` templates are exactly where the occupancy sluice
and the LP pair-pinning gate are most likely to fire. That expectation is written into
`GLASS_PREREG.md` §5.1 and §5.3 **before** any table is seen.

Total `g(r)` first peak: **1.070** at T = 0.44 and 0.50, **1.050** at T = 0.56. The peak
**sharpens on cooling** (2.781 → 2.844 → 2.961), which is the ordinary and well-known weak
temperature dependence of the pair structure — and precisely the reason this campaign exists:
that change is small, while the dynamics change by orders of magnitude.

---

## 4. DOES THE TEMPERATURE LADDER STRADDLE THE INTERESTING REGIME?

**Stated plainly: partly, and less than one would want.**

**The 3D arm.** For the Kob–Andersen mixture at `ρ = 1.2` the literature values are a
mode-coupling temperature **`T_MCT = 0.435`** and an onset/melting temperature **`≈ 1.03`**.
The ladder is `T ∈ {0.64, 0.56, 0.50, 0.44}`.

* It **bottoms out essentially exactly at `T_MCT`** (0.44 vs 0.435).
* Its top, 0.64, is **still supercooled** — about `0.62 × T_onset`. **There is no
  high-temperature liquid anywhere in this dataset.** The field's own "liquid vs glass at
  matched `g(r)`" control therefore cannot be taken from GlassBench and must be generated, which
  is why `GLASS_PREREG.md` §4.5 pre-registers it as a *secondary* control that we must simulate
  ourselves — and pre-registers the possibility that it is not reached.
* It **does not approach the laboratory glass transition.** For this model `T_g` by
  extrapolation sits near 0.3; the ladder stops well above it. **No dataset of equilibrated
  configurations reaches `T_g` for this model**, because equilibrating there is the open problem.

**The dynamic range is nonetheless real.** From the dataset's own time grids
(`KA_results/times_*.dat`), the longest sampled time rises **0.52 → 1 650 → 6 860 → 130 000**
LJ units across `T = 0.64 → 0.56 → 0.50 → 0.44` — a factor of **2.5 × 10⁵** in the timescale the
benchmark had to cover, i.e. roughly **three to five decades of structural relaxation** across
four state points whose `g(r)` peak moves by 6 %.

**That gap is the campaign's whole subject**, and it is also the honest limit on what any
outcome can say: this ladder can show whether whole-only compositional order moves *over the
accessible supercooled range*, and it cannot show what happens at `T_g`.

**The 2D arm** is more extreme in relaxation time and poorer in rungs: two temperatures, with
`τ_α = 2 200` at `T = 0.30` and `τ_α = 918 306` at `T = 0.23` (from the dataset's README) — a
factor of **417** between two points. It is a **replicate in sign**, not an independent ladder.

---

## 5. WHAT IS AVAILABLE THAT THIS CAMPAIGN IS NOT USING, AND WHY

| present | not used, because |
|---|---|
| `md_prop`, `bb_prop` (isoconfigurational propensities) | **dynamical labels.** A static-order campaign must not have them near its estimator. Discarded at ingestion. |
| `BOTAN`, `CAGE`, `GlassMLP`, `SE3` predictions | model outputs, not data |
| `SBO`, `SBO_CG`, `DEN`, `EPOT`, `PSI6` (coarse-grained structural descriptors) | these are the **local-order-parameter fields** of the secondary design (`GLASS_PREREG.md` §3.2). They are *already coarse-grained by someone else*, with a smoothing kernel we did not choose, which is FACT 3's trap pre-applied. If the secondary arm runs, it must carry its own binmint battery and cannot lean on these. |
| `initial_positions_cage` | available for a subset only (structures 1–100 and 401–500); not needed by the primary design |
| `KA2D_trajectories` (3.38 GB) | dynamics; deliberately not downloaded |

---

## 6. STATUS OF THE FETCH AT THE TIME OF WRITING

`KA T=0.44`, `KA T=0.50`, `KA T=0.56` are **downloaded, CRC-verified, converted and
inventoried** — the numbers in §3.1 and §3.2 are read off those arrays. `KA T=0.64` and the two
`KA2D` points were still transferring when this document was committed; the manifest entries in
§2 for them are read from the archive's own central directory and are exact, and their verified
per-array inventory is filed in `glass_inventory.json` and reported in `GLASS_RESULTS.md`.

**No state point is scored, and no share is computed, on the strength of this document.**

---

## 7. CITATIONS REQUIRED BY THE DATASET'S OWN README

Carried here so they cannot be lost between stages:

* **Jung, Alkemade, Bapst, Coslovich, Filion, Landes, Liu, Pezzicoli, Shiba, Volpe, Zamponi,
  Berthier & Biroli**, *Roadmap on machine learning glassy liquids* (arXiv:2311.14752) — the
  dataset itself.
* **H. Shiba, M. Hanai, T. Suzumura & T. Shimokawabe**, *BOTAN: BOnd TArgeting Network for
  prediction of slow glassy dynamics by machine learning relative motion*, **JCP 158:084503
  (2023)**, doi:10.1063/5.0129791 — required for the **KA** dataset.
* **G. Jung, G. Biroli & L. Berthier**, *Predicting dynamic heterogeneity in glass-forming
  liquids by physics-inspired machine learning*, **PRL 130:238202 (2023)**,
  doi:10.1103/PhysRevLett.130.238202 — required for the **KA2D** dataset.
* **R. M. Alkemade, F. Smallenburg & L. Filion**, **JCP 158:134512 (2023)** — required if the
  cage states are used (they are not).

The scientific credits for the *question* — Green; Nettleton & Green; Baranyai & Evans;
Giaquinta & Giunta; Krekelberg et al.; Torquato & Stillinger; Shell; Coslovich; Banerjee et al.
— are in `GLASS_PREREG.md` §1, and are mandatory before any number.

---

## 8. FILES

| | |
|---|---|
| `glass_zipfetch.py` | zip64 central-directory parser and ranged member fetch, with CRC verification |
| `glass_convert.py` | streams a tarball to a compact `.npz`; keeps positions, inherent positions and types only |
| `glass_inventory.py` | box, density, composition and `g_αβ(r)`; **computes no share** |
| `glass_get.sh` | the sequential fetch-convert-purge driver, under `flock` |
| `glass_inventory.json` | the measured inventory, including full `g_αβ(r)` |
| `glass/compact/*.npz`, `glass/compact/*.meta.json` | the converted data and its per-tarball metadata, held outside the repository |

Data held outside git. Primary seed 20260727.
