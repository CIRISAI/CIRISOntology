# PRE-REGISTRATION — the independent-sample confirmation attempt, on eBOSS DR16

Committed **before any order-3 quantity, correlation function or power spectrum has been
computed on any eBOSS catalogue**, and after `EBOSS_STAGE0.md` (`d60260a`), which read metadata
and the selection function only.

**This document has no `[to verify]` fields.** Unlike `SKY_REALDATA_PREREG.md`, which was written
before its catalogues were downloaded, and `SKY_BGS_PREREG.md`, whose Stage 0 was network-blocked,
this one is written *after* a completed Stage 0. Every catalogue property it rests on is a read
number with a committed script behind it. What it does not know is the only thing it must not
know: what the data reads.

**The deliverable is this document. Stages 1–2 may proceed on it; the unblind may not, and the
unblind order is not the author's to give.**

---

## 0. WHAT THIS DOCUMENT IS FOR

`Stance.lean` carries `wild-share` as **open**. BOSS DR12 scored its criterion MET and was then
**wounded by this programme's own pre-registered refuter**. The wounded yes is not cashed, and
the stance's named next instrument — DESI BGS — has been unreachable from this machine for two
days (`data.desi.lbl.gov`, re-verified today: still no route).

eBOSS DR16 is the reachable substitute. **This is a confirmation attempt on a partially
independent sample, not a new claim.** Whatever it finds, `wild-share` does not move without a
separate refuter pass and Eric's review.

**And Stage 0 has already established that the instrument is weaker than the one it is
confirming.** §2 states that in numbers before any design choice is made, because a
pre-registration that discovers its own weakness at Stage 6 is the failure mode this programme
keeps paying for.

---

## 1. THE PRIORS OF RECORD

**These are the refuter's CORRECTED numbers, not the campaign's published ones.** Quoting
9.4 σ / 13.5 σ / 50.8 σ anywhere in this campaign is a violation of prerequisite P12.

| | corrected | as published (superseded) |
|---|---|---|
| NGC `R=15 b=4` folded — **the primary rung** | **6.0 σ** | 9.4 σ |
| NGC `R=15 b=6` folded | **9.7 σ** | 13.5 σ |
| NGC `R=10 b=4 / 6 / 8` folded | **20.9 / 26.3 / 29.8 σ** | 40.5 / 46.8 / 50.8 σ |
| SGC `R=15 b=4` folded | **2.3 σ** | 3.5 σ |
| SGC `R=10 b=4 / 6 / 8` folded | **10.9 / 14.1 / 16.5 σ** | 22.7 / 26.5 / 29.4 σ |

And the five facts that qualify them:

1. **Null-construction dependence: 30–52 %.** The reported target falls by that much under a
   second defensible null. Every significance above is construction-dependent at the
   tens-of-percent level.
2. **The "lower bound" framing is falsified IN SIGN.** Less clipping produced a **larger** floor,
   not a smaller one (24–50 % larger).
3. **Stochasticity margin 1.3–1.7×, not orders of magnitude.** `ε_crit = 0.63–0.85` against a
   literature-defensible `ε ≈ 0.5`, with the catalogue's own weights already **13–15 %**
   super-Poisson (`κ = 1.1291` NGC, `1.1515` SGC).
4. **One pre-registered VOID gate (§7.5, weight variation) was never run**, and the reading is
   sensitive to fibre-collision treatment at **2.5–2.9 σ**.
5. **A cap asymmetry the mocks exclude**: NGC exceeds SGC on 4/4 folded rows by 5–9 %, worst
   **2.15 σ**, where Patchy predicts the caps equal to 0.2 %.

**What survived every correction, and is the thing this campaign is actually testing:** the
*consistency* between the data and the mock prediction, because the correction is **common-mode**.
The detection-against-zero is what was wounded.

---

## 2. WHAT STAGE 0 FORCES, STATED BEFORE ANY DESIGN CHOICE

The commission's premise is that eBOSS is a substitute instrument. **Measured, it is a
substantially worse one, in a way that is structural rather than fixable by design.**

### 2.1 The density is the binding constraint, and it fails differently for each tracer

From `EBOSS_STAGE0.md` §S0.3, with the floor projected on this campaign's own measured
amplitude-versus-density curve (calibrated first against Amendment 1's own numbers, which it
reproduces to 0.3 and 1.0 percentage points):

| sample | `n̄V_R` at R=15 | floor/signal | `n̄V_R` at R=10 | floor/signal | rungs at R=15 |
|---|---|---|---|---|---|
| **BOSS DR12 NGC** *(the thing being confirmed)* | 15.95 | **57.5 %** | 4.73 | 95.9 % | 4, 6, 8 |
| **LRG** NGC / SGC | **3.97 / 3.92** | **101 %** | 1.18 / 1.16 | 140 % ‡ | **4, 6** |
| **ELG** NGC / SGC | **17.87 / 19.91** | **54 / 51 %** ‡ | 5.29 / 5.90 | 92 / 89 % | **4 only** |
| **QSO** NGC / SGC | 0.94 / 0.85 | 147 / 150 % ‡ | 0.28 / 0.25 | 185 / 188 % ‡ | 4, 6, 8 |

‡ extrapolated beyond the measured grid `[1.6, 15.7]` and marked so.

> **The central finding, and this document is built around it: no eBOSS sample has BOSS's
> density and BOSS's volume at once. ELG has the density (it is the only eBOSS sample denser
> than BOSS) and can field exactly one `b` rung at the primary scale. LRG has the volume and its
> floor equals its signal.**

### 2.2 The independence is radial and partial

| sample | sky overlap with BOSS | radial overlap | **volume sharing BOSS's density field** |
|---|---|---|---|
| LRG | 99 % | 31.1 % | **31 %** |
| ELG | 99 % | 23.4 % | **23 %** |
| QSO | 99 % | 0 % | **0 %** |

**"Independent-sample confirmation" is therefore a claim that must be qualified in every
statement of any result from this run**, and the qualification is registered here in the exact
words to be used:

> *This is a confirmation on a different tracer over a partly independent volume: 23 % (ELG) /
> 31 % (LRG) of the confirmation volume samples the same density field as BOSS DR12, through
> different galaxies.*

QSO is the only fully independent eBOSS volume and is dead on density. That is not bad luck; it
is the same trade the survey makes everywhere.

### 2.3 What eBOSS DOES buy, ranked honestly

1. **1000 mock realisations per tracer per cap, individually downloadable.** `σ` to **±2.2 %**
   against BOSS's **±18 %** from 16 Patchy mocks. **This directly retires refuter caveat A4's
   stated residual** — that a "9.4 σ" was quoted to two significant figures with a ±1.7 σ error
   bar from the ensemble size alone. It is the single largest methodological gain available here.
2. **The §7.5 VOID gate becomes dischargeable.** `full_ALLdata` ships `sector_TSR`, `sector_SSR`
   and `COMP_BOSS`, joinable by `LRG_ID` / `EBOSS_TARGET_ID`, supplying a genuine alternative
   published completeness scheme. **BOSS had none and the gate died for that reason.**
3. **The randoms carry the weight columns.** BOSS's did not, which is what made the refuter's own
   FKP variant an artifact. An FKP-weighted variant is a legitimate test here.
4. **Four independent ELG patches** (`eboss21/22/23/25`) where BOSS offered two caps — a
   materially better patch-isotropy test (P11), which is refuter caveat 6's channel.
5. **A different tracer population.** ELG (star-forming, `b ≈ 1.4`) and LRG (`b ≈ 2.3`) have
   different fibre-collision, redshift-failure and imaging systematics from CMASS. **A systematic
   that produced BOSS's reading has no reason to reproduce it here.** That is the actual
   scientific content of a confirmation and it survives the density problem intact.

### 2.4 The projection, registered before the run

Scaling the priors of record by `(D_new/D_BOSS)^0.82 · √(n_indep ratio)` — amplitude scaling from
the forecast's measured `+0.82`, per-realisation `σ` as `1/√n_indep`; **tracer bias is NOT
carried and no factor is implied**:

| sample | R | b | prior | **projected** |
|---|---|---|---|---|
| LRG NGC | **15** | **4** | 6.0 | **4.1** |
| LRG NGC | **15** | **6** | 9.7 | **6.7** |
| ELG NGC | 15 | 4 | 6.0 | 1.9 *(and only one rung exists)* |
| ELG NGC | 10 | 4 / 6 | 20.9 / 26.3 | 6.8 / 8.5 |
| LRG NGC | 10 | 4 / 6 | 20.9 / 26.3 | 14.4 / 18.2 |

> **REGISTERED EXPECTATION, so that a detection is a surprise rather than a relief.** On this
> scaling the primary-scale two-rung clause of outcome (a) is **expected to fail on LRG**
> (4.1 σ at `b = 4`, below 5), and **cannot even be attempted on ELG at `R = 15`**. I expect this
> campaign to land on **outcome (c)** (an honest bound) or **outcome (e)** (a reading whose
> decomposition could not be performed), and I am writing that down now. If it lands on (a), the
> scaling was wrong and that is itself a finding requiring explanation, not celebration.

---

## 3. THE HARVEST GATES, AS NUMBERED PREREQUISITES

`GATES.md`'s closing harvest registers gates minted by the BOSS run and its refutation, with the
standing consequence that **all of them are prerequisites for the next survey-class run**. The
commission names twelve; **the table in `GATES.md` now carries sixteen** — four more were added
from the Dalitz and φ⁴ campaigns (`d22f1ea`). **All sixteen are prerequisites here.** Recording
the count discrepancy rather than silently taking twelve is itself P12.

The first seven are **mechanized in `bgs_gates.py`** — reused unchanged, not reimplemented; it is
survey-agnostic (`CampaignView` + `run_battery` + `require_discharged`) and its docimasia was
re-run today, all seven **VALIDATED** against the four stored BOSS views. `require_discharged()`
reads artifacts off disk and **raises**.

| # | gate | mechanized? | discharge point | artifact | retires caveat |
|---|---|---|---|---|---|
| **P1** | **valve floor** — the null carries shot-noise NON-Gaussianity, not only its power | **driver** | Stage 5 | `eboss_stage5_valve.json` :: finite `valve` on every reported row | — |
| **P2** | **null-construction sweep** — **≥ 2** defensible nulls per row, spread a **quoted systematic** | **driver** | Stage 5 | `eboss_stage5_nulls.json` :: ≥2 null tags per row, `spread` non-null | **1** |
| **P3** | **directional claims are measured** — any "conservative direction" claim is TESTED by varying the mechanism at ≥3 clustered levels spanning ≥1.5× | **driver** | Stage 5 | `eboss_stage5_direction.json` :: clip varied, sign of `d(floor)/d(clip)` recorded | **2** |
| **P4** | **dispersion sweep** — swept to literature-plausible super-Poisson dispersion; `ε_crit` and margin reported | **driver** | Stage 5 | `eboss_stage5_dispersion.json` :: `eps_crit` per row + measured `κ` | **3** |
| **P5** | **same null both sides** — prediction and data scored against identically-constructed nulls | **driver** | Stages 4+6 | `eboss_null_signature.json` :: mock hash == data hash | — |
| **P6** | **outcome completeness** — the emitted verdict is one of the enumerated outcomes | **driver** | §9 | driver asserts tag ∈ `{a,c,d,e}` | — |
| **P7** | **gate discharge before unblind** — no unblind while any VOID gate is undischarged | **driver** | Stage 6 entry | `require_discharged('unblind')` raises on any absence | **5** |
| **P8** | **lag-matched probes** — `rmult` swept over ≥3 values; equal spacing is tested, not assumed | human | Stage 4 | `eboss_stage4.json :: rmult_sweep` | — |
| **P9** | **search caps declared** — IPF and LP iteration caps reported with the saturated fraction | human | Stages 1, 4 | `eboss_stage4.json :: caps` | — |
| **P10** | **delocalisation correction** — the `1/√f` footprint factor **re-derived** for each eBOSS footprint, never carried over | human | Stage 3 | `eboss_stage3.json :: deloc`, checked against the measured `σ` ratio as BOSS did (0.3887 vs `√0.154`) | — |
| **P11** | **patch isotropy** — independent patches agree in **AMPLITUDE** | human | Stage 6 | see §9(a) clause 7 and §7.4 | **6** |
| **P12** | **current-numbers hygiene** — superseded numbers appear only labelled superseded | human | write-up | every superseded figure carries "superseded" on the same line | **8** |
| **P13** | **gate-log provenance** — a committed gate log must be REPRODUCIBLE from the instrument committed beside it | human | every stage | deterministic re-run of each stage's driver compared to its committed JSON before the log is trusted | — |
| **P14** | **floor matched to sample size** — a floor is drawn at the SAME sample size as the reading it gauges | human | Stages 2, 5 | every floor/null in this campaign records its own `n_indep` and `n_triples`, and they match the reading's | — |
| **P15** | **null-shape before z** — the null's SHAPE is measured before any `z` is quoted; heavy-tailed nulls get p-values, never median-and-σ | human | Stage 5 | `eboss_stage5_nulls.json :: null_shape` — skew/kurtosis and a normality test over the null ensemble, **per row**, committed before any significance is computed | — |
| **P16** | **equilibration diagnostics can be blind** | **N/A, and why** | — | this campaign runs no Markov chain and has no equilibration step; the gate is recorded as **not applicable** rather than silently dropped | — |

**Caveats 4, 7 and 9 are not gates and are handled directly:** caveat 4 (narrow survival) by
§9(a)'s explicit **margin** clause; caveat 7 (shape never scored) by §9(a) clause 6, which scores
it over all geometries; caveat 9 (pointwise channel unbounded) by `N_C` in §4.4.

---

## 4. TARGET STATISTIC, THE DUAL-NULL REQUIREMENT, AND THE CEILING FRACTION

### 4.1 The statistic carries over unchanged

`I_C⁽³⁾(b)`: the order-3 connected information of a `b`-level quantile-binned triple of smoothed
cells — the entropy gap between the state and the maximum-entropy state carrying its three pair
marginals. IPF with the KL certificate `< 1e-9` (G9). **Nothing about the estimator changes.** It
was independently reimplemented and agreed to `9e-13` relative (refuter A5); that is the one part
of the BOSS run needing no re-litigation, and reimplementing it would forfeit that validation.

Primary configuration **folded/collinear**, sides `(r, 2r, r)`, `r = rmult·R`, `rmult = 1.5` —
and `rmult` is **swept, not assumed** (P8).

### 4.2 The target is never one number

    TARGET(null)  =  I_C⁽³⁾(data)  −  I_C⁽³⁾(null)

**P2 makes dual-null reporting mandatory, not optional.** Every reported row carries the target
under **both** nulls of §4.3, and **the spread is quoted as a systematic on the same line as the
value**. This is not a robustness appendix: refuter A9 cut the BOSS target by 30–52 % by null
construction alone, and it did so on a campaign that reported one construction.

### 4.3 The two required nulls, both fixed now

**`N_A` — the BOSS pipeline null (`N2`), carried over unchanged for comparability.**
Phase-randomise the gridded masked `δ` (keeping `|F(k)|`, with P10's `1/√f` delocalisation
correction re-derived for the eBOSS footprint), then Poisson-resample at the field's own `n̄(z)`
through the identical selection: `λ = α·n̄_ran·max(1 + δ_PR, 0)`.

**`N_B` — the refuter's construction (`N2mw`).** The modulation carries the **clustering only**
(shot-noise power removed in Fourier *before* phase randomisation, so Poisson supplies it once
rather than twice), renormalised to the data's own number density, counts drawn with the data's
own **weighted** shot noise `κ = ⟨w²⟩/⟨w⟩`.

> **`N_B` is the null of record for outcome (a).** `N_A` is reported beside it for comparability
> with BOSS and to make the spread visible. This is the branch the refuter's finding forces and
> choosing it **now** removes the freedom to choose it later.

**`κ` is measured per sample, not carried over**, and Stage 0 has already measured it:
LRG **1.1025 / 1.1158**, ELG **1.2249 / 1.1810** (NGC/SGC), against BOSS's 1.1291 / 1.1515.
**ELG NGC at 22.5 % excess is the largest weight-induced dispersion in either survey.**

### 4.4 `N_C` — the pointwise-channel bracket (caveat 9)

**`N_C` := IAAFT surrogate of the smoothed field**, matched in marginal distribution *and* in
`P(k)`, leaving only higher-order phase coupling to differ. The BOSS attempt (`N2L`, lognormal)
was unfair by construction — a monotone per-cell map does not commute with smoothing.

**Its known limit, stated so it cannot be oversold** (house lesson
`temporal-share-realdata-nulls`): **IAAFT survival is not sufficient evidence of anything** — a
clip artifact survived IAAFT at `z = 86` in this programme's own history. `N_C` is used in **one
direction only**: if `TARGET(N_C) ≤ 0`, the pointwise channel is not bounded and §9(e) applies. A
positive `TARGET(N_C)` is **not** independent confirmation and may not be quoted as a
significance.

### 4.5 THE CEILING FRACTION — a required reporting field

The commission requires a common denominator for cross-scale synthesis with the SM, glass and
Planck legs. **Every headline reading, every floor and every residual is reported additionally as
a percentage of `ln 2 = 0.693147` nats**, the machine-checked cap on the whole-only share of
three binary slots (`Core/Third.lean`, `Core/HammingCap.lean`).

**And the honesty condition on that field, which is load-bearing.** The readings here are at
`b ∈ {4, 6}`, not `b = 2`. **`ln 2` is the proved cap for three BINARY slots and is NOT a proved
bound on a `b = 6` reading.** The ceiling fraction is therefore a **common denominator for
synthesis, never a compliance statement**, and it is labelled that way at every point of use. Any
sentence of the form "the reading is X % of the cap" without that qualification is a violation of
this section. (The separate question of cap *compliance* is `ShareK.lean`'s and is not what this
field reports.)

**The BOSS reference, computed and put on the record here so the eBOSS numbers land on a scale
that already has a point on it:**

| BOSS row (folded) | `I_data` | target | valve floor | **target / ln 2** | **valve / ln 2** |
|---|---|---|---|---|---|
| NGC R=15 b=4 | 6.206e-04 | 3.449e-04 | 9.210e-05 | **0.0498 %** | 0.0133 % |
| NGC R=15 b=6 | 9.227e-04 | 6.055e-04 | 1.391e-04 | **0.0874 %** | 0.0201 % |
| NGC R=10 b=8 | 3.892e-03 | 2.791e-03 | 9.101e-04 | **0.4027 %** | 0.1313 % |
| SGC R=15 b=4 | 6.212e-04 | 3.177e-04 | 1.259e-04 | **0.0458 %** | 0.0182 % |
| SGC R=10 b=8 | 3.668e-03 | 2.568e-03 | 8.974e-04 | **0.3704 %** | 0.1295 % |

**The whole BOSS detection lives between 0.046 % and 0.40 % of `ln 2`.** That is the number the
cross-scale synthesis needs and it has not been stated anywhere until now.

### 4.6 Blinding

**Enforced in code, as in BOSS.** `sky_realdata.measure_catalogue` already raises without
`stage6_unblind=True`; the eBOSS Stage-6 entry point calls it through the same guard **and
additionally calls `bgs_gates.require_discharged('unblind')` first**. The prediction is frozen to
a committed JSON before Stage 6 and its git object is checked byte-identical at scoring time.

---

## 5. SAMPLE CHOICE — decided now, on Stage-0 numbers, with the reasons on the record

Stage 0 is complete, so this is a decision and not a rule. Both arms are fixed **before any share
is computed**, and the freedom to pick the better-reading arm afterwards is removed by naming
both now with their own criteria.

### 5.1 Excluded in advance, with the reason

* **QSO — EXCLUDED on density.** `n̄V_R = 0.85–0.94` at `R = 15`: fewer than one galaxy per
  smoothing volume, off the measured floor grid entirely. It is excluded here, before any
  reading, so that it cannot be brought back as a third look if the other two disappoint.
* **LRGpCMASS — EXCLUDED on independence.** It **contains BOSS CMASS galaxies** (`ISCMASS` is a
  shipped column). It is not a confirmation sample in any sense. Its randoms were deliberately
  not downloaded.

### 5.2 PRIMARY: **LRG, `R = 15`, `b ∈ {4, 6}`, folded**

Chosen because it is the only eBOSS configuration that can *satisfy the two-rung clause at the
primary scale at all*: occupancy 797/236 (NGC) and 527/156 (SGC) at `b = 4/6`. Contiguous
standard eBOSS footprint, randoms at 51×, 69 % independent volume, `z_eff ≈ 0.75`.

**Its stated weakness, which is severe:** the floor is **101 % of signal** — worse than the worst
configuration BOSS ever ran (95.9 %, at BOSS's *secondary* scale). §2.4 projects **4.1 σ** at
`b = 4`. **This arm is expected to fail clause 1 of outcome (a).**

### 5.3 SECONDARY (dense arm): **ELG, `R = 10`, `b ∈ {4, 6}`, folded**

Chosen because it is the only eBOSS configuration where **two rungs and a sub-BOSS floor coexist**
(occupancy 637/189 NGC, 693/205 SGC; floor 89–92 %, against BOSS's 95.9 % at the same scale), and
because it is the more independent volume (77 %) and the more different tracer. §2.4 projects
**6.8 / 8.5 σ**.

**Its stated weaknesses:** the smallest volume in the survey (0.63–0.70 (Gpc/h)³, seven times
smaller than BOSS NGC); four disjoint patches, two of them equatorial strips only 4–10° thick
(~370 Mpc/h at `z_eff = 0.84`, against a `R = 15` kernel needing ~90 Mpc/h of clearance — which
is why `R = 15` is not this arm's scale); and the largest weight dispersion in either survey.

**ELG at `R = 15` is reported but is NOT eligible for outcome (a)**, because it fields one rung
(occupancy 189/56/24 — `b = 6` fails G9). That exclusion is registered now, before the reading,
exactly as the BOSS campaign excluded `b = 16` in advance on occupancy grounds.

### 5.4 The two arms are scored separately and never pooled

Pooling triple histograms across tracers or caps is **forbidden** — Amendment 2 §A2.3, on the
mixture-manufacture ground, and `ECA_SPIKE_RESULTS.md`'s correction block. Different windows,
different `n̄(z)`, different bias. Caps and tracers are combined only at the level of summary
statistics, never by pooling histograms. **There is no combined eBOSS significance in this
design and none may be computed.**

---

## 6. MOCKS, AND THE SUITE ASSIGNMENT

`dr17/eboss/lss/EZmocks/v1_0_0/realistic/` — **1000 realisations per tracer per cap**, columns
matching the data catalogue's, `n(z)` agreeing with the data to 1.4–1.6 % in total variation, and
`κ` reproducing the data's to 0.7 % (ELG) and 5 % (LRG).

### 6.1 The suite assignment, fixed now

| job | suite | why |
|---|---|---|
| floor model + forward model | realisations **1–128** per cap | Amendment 2's split |
| **G10 mock closure** | **1–64 vs 65–128**, held out | the go/no-go, unchanged |
| **`σ` for every significance** | realisations **1–512** per cap | the eBOSS-specific gain: `σ` to ±3.1 %, against BOSS's ±18 % |
| patch isotropy prediction (P11) | 1–128 | the mock-predicted dispersion the data must sit inside |

### 6.2 RULE E-S2-A — the suite size is not committed until the scatter is measured

Amendment 2 justified 128 by a **measured** per-realisation scatter of `I_C⁽³⁾` at **0.5–1.1 % of
the floor mean** — *on BOSS geometry*. **That does not transport by assertion**, and eBOSS
geometry is different in the direction that matters (smaller volumes, thinner footprints, more
boundary).

> **RULE E-S2-A.** Measure the per-realisation scatter on eBOSS geometry on the first 32
> realisations of each arm, **before** committing the suite size. If the scatter exceeds **2.5 %**
> of the floor mean, the 128-realisation floor no longer clears the G10 bar with the margin
> Amendment 2 relied on, and the suite size is recomputed and **recorded as an amendment** before
> Stage 2 proceeds.

### 6.3 RULE E-S2-B — one random file per cap, with the check that licenses it

The EZmock randoms differ between realisations and are the entire storage cost (97–137 GB per
tracer, unaffordable — see §11). The BOSS pipeline builds `CapGeometry` **once per cap** from the
randoms and reuses it, because the randoms encode the selection function, which is shared.

> **RULE E-S2-B.** One EZmock random file per tracer per cap defines the mock geometry, and the
> licensing check is run rather than assumed: **build the geometry from EZmock random 0001 and
> from random 0002 independently, and require the resulting `I_C⁽³⁾` on a common mock galaxy
> field to agree to better than 20 % of the per-realisation scatter measured under E-S2-A.**
> Failure means the selection function is not shared across realisations and the whole
> shared-geometry design is void — which is a Stage-2 VOID, reported as one.

### 6.4 The mock/data random-density mismatch, registered as a known difference

Mock randoms are **30×** the mock galaxy density; data randoms are **40–51×**. Amendment 2 §A2.2
established that ×10 collapses the mask to speckle and ×50 does not; 30× sits between and above
the fix. The footprint is defined on a **smoothed** random field, which is density-independent by
construction. **But it is a stated difference between the two sides of the same measurement**, and
prerequisite P5 makes it a thing to check: the mock-side and data-side geometries are built by the
identical code path and their `n_indep`, `frac_valid` and `σ` are compared and recorded.

### 6.5 What the mocks are NOT

EZmock is an **effective-Zel'dovich** approximate-gravity suite with a calibrated bias model
(Chuang et al. 2015), **not N-body** — exactly as Patchy was. **Outcome (b) is therefore withdrawn
here for the same reason Amendment 4 withdrew it on BOSS**, and any (a) verdict reads
"consistent with the EZmock suite's higher-order structure", which is a product of its bias
calibration as much as of gravity.

---

## 7. SCALES, THE `b` LADDER, THE OCCUPANCY GATE, AND PATCHES

### 7.1 The gate, unchanged

Occupancy > 100, counted in **independent smoothing volumes** (`n_indep / b³`), **per cap and per
tracer**, never pooled. IPF certificate `< 1e-9`. Tied and railed fraction disclosed for every
reading (G7). A `b` failing either is not reported.

Stage 0's occupancy is a **shell-volume estimate**, calibrated against Amendment 2's measured
valid-cell count on BOSS SGC (31 291 vs 33 264, 6 %). **Stage 2 replaces it with the measured
count, which for ELG's thin footprints will be lower** — so any Stage-0 occupancy failure is a
failure a fortiori, and any Stage-0 pass near the threshold must be re-checked at Stage 2 before
the rung is reported. **`LRG NGC R=15 b=8` sits at exactly 100 and is excluded in advance** rather
than being allowed to cross the line at Stage 2.

### 7.2 The `b` ladder

`b ∈ {4, 6}` for both arms. **`b = 8` is excluded in advance on occupancy** for every eligible
configuration (LRG R=15: 100/66; ELG R=10: 80/87), and `b = 16` remains excluded as it was on
BOSS. This is a narrower ladder than BOSS's and the reason is density, stated here rather than
discovered at Stage 2.

### 7.3 Scales

`R = 15` (LRG primary) and `R = 10` (ELG primary; LRG secondary). **No third scale and no `R★`
extension arm**: eBOSS has no configuration where a larger scale is affordable in occupancy, and
inventing one after the fact is the look-elsewhere problem P8 and the trials accounting exist to
prevent.

### 7.4 Patch isotropy (P11), scored across patches AND tracers

BOSS's caveat 6 was a **5–9 % signed cap asymmetry the mocks predicted at 0.2 %**. eBOSS offers a
better instrument for exactly that channel, and the scoring rule is fixed now:

1. **Within ELG: four patches** (`eboss21`, `eboss22`, `eboss23`, `eboss25`), each measured
   separately with its own geometry. Amplitude dispersion across the four is scored against the
   **mock-predicted** dispersion for the same four patches, not against equality.
2. **Within LRG: two caps**, same rule.
3. **Across tracers: LRG vs ELG amplitude is scored against the MOCK-PREDICTED LRG/ELG ratio, not
   against equality.** The two tracers have different bias and different `n̄`, so equality is not
   the null and treating it as one would manufacture a fake systematic. This is registered
   explicitly because it is the easy mistake.
4. **Fires** if the observed dispersion exceeds the mock-predicted dispersion by > 3 σ, or if the
   sign is coherent across all patches where the mocks predict no coherence.

**Some patches will be too small to carry `b = 6`.** Patch-level occupancy is reported with every
patch reading and a patch failing G9 is reported as *ungauged*, not as agreement.

---

## 8. THE WEIGHT-VARIATION VOID GATE, DESIGNED AGAINST COLUMNS THAT EXIST

`SKY_REALDATA_PREREG.md` §7.5 is a **VOID** condition and **was never run on BOSS**. It could not
be: the DR12 combined catalogue carried no alternative fibre-collision scheme. **eBOSS does.**

### 8.1 The columns, read at Stage 0

Clustering catalogues ship `WEIGHT_SYSTOT, WEIGHT_CP, WEIGHT_NOZ, WEIGHT_FKP, NZ` — **on both the
galaxies and the randoms**. `full_ALLdata` additionally ships `sector_TSR`, `sector_SSR`,
`COMP_BOSS`, `IMATCH`, joinable by `LRG_ID` / `EBOSS_TARGET_ID`; the ELG file also ships the
imaging regressors themselves (`galdepth_*`, `psfsize_*`, `nobs_*`, `mskbit`).

**What does NOT exist, established at Stage 0 by probing four paths: there are no PIP / bitwise
weights anywhere in the SAS eBOSS tree.** The Mohammad et al. (2020) pairwise-inverse-probability
weights are not distributed with these catalogues. The gate is designed against what ships.

### 8.2 GATE W — the fibre-collision channel

Standard scheme `w = WEIGHT_SYSTOT · (WEIGHT_CP + WEIGHT_NOZ − 1)`, against the **alternative
published completeness scheme** built from `sector_TSR` / `sector_SSR` / `COMP_BOSS`:

> **GATE W.** Re-run every primary row under (i) the standard scheme and (ii) the
> completeness-weighted scheme, with **paired null seeds** so the phase realisation cancels
> between schemes (the refuter's own technique). **A shift exceeding the row's σ VOIDS that row.**

**Registered in advance, because the refuter's own scoring of this channel was ambiguous and it
said so:** `w = 1` ("no weights at all") is **NOT** a variant scheme in this gate. Deleting a
correction for galaxies that were never observed is a known-wrong analysis, and a shift when a
necessary correction is deleted is expected rather than informative. It is reported as a
**diagnostic** and cannot void a row. Two published schemes are compared; a known-wrong one is
not one of them.

### 8.3 GATE W′ — the imaging-systematics channel

Variants: standard `WEIGHT_SYSTOT`; `WEIGHT_SYSTOT ≡ 1`; and (ELG only) a refit of the imaging
weight from the shipped regressors. On BOSS this channel was **CLEAR at ≤ 0.62 σ**; the
expectation is that it is clear here too, and it is registered so that a firing is a surprise.

**`WEIGHT_SYSTOT = 0.0` occurs exactly** on LRG NGC and QSO SGC. A zero systematic weight deletes
an object. The count is disclosed with every reading as part of the G7 tied/railed fraction, and
those objects are handled by the **same rule on data and mocks** — which is the only thing that
matters and the thing that would otherwise silently differ.

### 8.4 GATE W″ — the FKP variant, legitimate here and not on BOSS

Because the **randoms carry the weights**, an FKP-weighted variant can be applied to galaxies
*and* randoms, which is what makes it a systematics test rather than the spurious radial gradient
the refuter correctly struck from its own results. **Run, reported, and voiding nothing on its
own** — it is registered as the closure of a known defect in the refuter's record, not as a new
kill.

---

## 9. PRE-REGISTERED OUTCOMES — separable, and COMPLETE

Outcome completeness is prerequisite **P6**, minted because the BOSS unblind produced a reading
that **fit no pre-registered outcome**. This enumeration is closed and the driver asserts its tag
is in it.

### (a) CONFIRMATION

*Every clause must hold, and each is separately reported with its own verdict.*

1. **Detection.** `TARGET(N_B)` positive at **≥ 5 σ**, folded, at **two or more `b` rungs passing
   G9 within a single tracer, cap and scale**.
2. **Margin (caveat 4).** The same rows hold ≥ 5 σ at **`ε = 1.0`**, i.e. **`ε_crit ≥ 1.0`**.
   BOSS's was 0.63–0.85 and failed this. **A confirmation that does not move `ε_crit` past 1.0
   does not confirm — it reproduces a wound.** Given ELG's measured `κ − 1 = 22.5 %`, this clause
   is expected to be the hardest one here, and it is not weakened for that reason.
3. **Null-construction stability (caveat 1).** The `N_A`/`N_B` spread is **quoted**, and the ≥ 5 σ
   verdict holds under **both**.
4. **Pointwise bracket (caveat 9).** `TARGET(N_C) > 0` on the primary rows — necessary, not
   sufficient (§4.4).
5. **Amplitude consistency.** `|data − prediction| ≤ 3 σ`, prediction from the EZmock suite and
   read as §6.5 requires.
6. **Shape consistency, SCORED (caveat 7).** Over **all** geometries — folded, equilateral,
   squeezed — the data/prediction ratios show **no coherent scale-dependent trend**: the mean
   ratio over non-folded rows lies within 3 σ of the folded mean, at each scale separately.
   **BOSS would have failed this had it been scored.**
7. **Patch isotropy not fired (P11, §7.4).**
8. **Weight gate discharged (§8): GATE W run and not voiding the row.**

*Licenses:* **`wild-share` gets its first confirmed instance on a partly independent sample** —
and only with §2.2's qualification attached in the same sentence. *Does not license:* any
primordial reading; any claim the whole-only share is large (`kappa-edge`'s H-BLIND puts the
degree-3 direction at ~1 % of fine-grained structure; §4.5 puts BOSS's reading at 0.05–0.40 % of
`ln 2`); any continuum claim; **any stance change without a separate refuter pass and Eric's
review.**

### (b) EXCESS BEYOND PREDICTION — **WITHDRAWN** (§6.5)

Withdrawn on the same ground Amendment 4 withdrew it on BOSS: EZmock is not N-body. Nothing in
this run may be cited for or against an anomaly.

### (c) NULL ABOVE THE FLOORS

*Criterion:* `TARGET(N_B)` consistent with zero after all floors, with the floor uncertainty
measured.

*Licenses:* **an honest upper bound**, quoted with its ceiling fraction (§4.5), on the whole-only
order-3 excess of the eBOSS LRG/ELG density field at the stated scales. **`wild-share` stays
open.** Given BOSS returned a *wounded positive*, an eBOSS null is a **substantive result about
BOSS's systematics** and is reported at exactly the volume a detection would be. §2.4 registers
this as an expected landing.

### (d) VOID — the run produces no result

Any of: **G1** pair-pinning at analysis resolution; **G10** mock closure failing; **G9** failing
at every `b` in an arm; IPF certificate > `1e-9`; **RULE E-S2-B** failing (the mock selection
function is not shared across realisations); **P5** null-signature mismatch; **P7** finding any
undischarged gate at the unblind boundary; **GATE W** voiding every primary row; the surrogate
exit diagnostics failing (`σ`(surrogate) ≉ `σ`(field), or smoothed skewness(surrogate) not ≈ 0).

*Licenses:* a report of the void with the failing number, and nothing else. Per house rule 7 the
void is reported as plainly as a detection.

### (e) NOT DECOMPOSED — the outcome BOSS produced and had not enumerated

*Criterion:* a large, well-controlled reading whose decomposition into signal and floor **could
not be performed** — concretely, any of:

* `TARGET(N_A)` and `TARGET(N_B)` differ by more than **50 %** of the larger (BOSS: 30–52 %,
  which sits at this line and is why the line is here);
* `TARGET(N_C) ≤ 0` — the pointwise channel is not bounded by any null run;
* the valve floor is not separable because the null's own skewness is dominated by clipping
  rather than by Poisson (**measured** under P3, not argued).

*Licenses:* **the reading is reported in full, with its decomposition explicitly marked as not
performed. It is not a detection and it is not a null, and it does not move `wild-share` in
either direction.** This outcome exists because the BOSS unblind landed here and the document had
nowhere to put it. §2.4 registers this as the second expected landing.

### Look-elsewhere, declared in advance

Rows scored: **2 tracers × 2 caps × 1 scale each × 2 `b` rungs × 3 geometries = 24**, of which
**8 folded rows are eligible to carry clause 1** and 4 `(tracer, cap)` cells are eligible for the
two-rung clause. At the projected significances (4–9 σ) a trials factor of 4 costs ~0.2–0.3 σ.
Recorded **before** the numbers, which is the point.

---

## 10. THE UNBLIND CHECKLIST — machine-verified, and the order is not the author's

**`bgs_gates.require_discharged('unblind')` reads each artifact off disk and raises. Nothing here
is satisfied by recollection.**

| # | check | artifact |
|---|---|---|
| 1 | Stage 0 complete, all numbers read | `eboss_stage0*.json` (**done**, `d60260a`) |
| 2 | RULE E-S2-A scatter measured, suite size committed or amended | `eboss_stage2.json :: scatter` |
| 3 | RULE E-S2-B shared-geometry check passed | `eboss_stage2.json :: geom_closure` |
| 4 | **G10** mock closure PASS per row, failures named | `eboss_stage2.json :: g10` |
| 5 | **G1** LP pair-pinning PASS at analysis resolution | `eboss_stage4.json :: g1` |
| 6 | **G2** binmint quantified at both scales | `eboss_stage4.json :: g2` |
| 7 | **P8** `rmult` swept ≥3 values | `eboss_stage4.json :: rmult_sweep` |
| 8 | **P9** IPF/LP caps + saturated fraction | `eboss_stage4.json :: caps` |
| 9 | **P10** delocalisation re-derived per eBOSS footprint | `eboss_stage3.json :: deloc` |
| 10 | **P1** valve floor, all rows | `eboss_stage5_valve.json` |
| 11 | **P2** ≥2 nulls per row, spread quoted | `eboss_stage5_nulls.json :: spread` |
| 12 | **P15** null shape measured before any `z` | `eboss_stage5_nulls.json :: null_shape` |
| 13 | **P3** direction measured, clip swept ≥3 levels | `eboss_stage5_direction.json` |
| 14 | **P4** `ε_crit` per row + measured `κ` | `eboss_stage5_dispersion.json` |
| 15 | **P14** every floor's `n_indep`/`n_triples` matches its reading's | `eboss_stage5_*.json :: n_match` |
| 16 | **GATE W / W′ / W″** run, verdicts recorded | `eboss_stage5_weights.json` |
| 17 | **P5** null signature identical both sides | `eboss_null_signature.json :: match` |
| 18 | **P13** every committed gate log reproduced bitwise from its committed instrument | `eboss_provenance.json` |
| 19 | prediction frozen, git object byte-identical | `eboss_frozen_prediction.json` + git check |
| 20 | **P6** this document's outcome set is the driver's | driver assertion |
| 21 | ceiling fraction (§4.5) present on every reported row, with its qualification | `eboss_stage6*.json :: ceiling_frac` |

**Item 22 is not mechanizable and is stated anyway: the unblind order comes from Eric.** The
driver refuses without the flag, and the flag is not set by the author.

---

## 11. RESOURCE PLAN

| stage | what | data | compute | gate before proceeding |
|---|---|---|---|---|
| **0** | inventory | 2.90 GB (**done**) | done | **COMPLETE**, `d60260a` |
| **1** | pipeline adaptation: eBOSS FITS readers, footprint from eBOSS randoms, weight scheme; **reuse `sky_realdata.py` and `sky_stage2.CapGeometry` unchanged** | — | ~0.5 d | G9, G7 re-passed on eBOSS geometry; the randoms-only null re-run |
| **2** | floor model + **G10**; RULES E-S2-A, E-S2-B | mock `dat` 0.5–2 GB per arm + 1 random/cap | hours | **G10. The go/no-go.** |
| **3** | surrogate controls; **P10** re-derivation | — | ~1 h | exit diagnostics |
| **4** | **G1**, **G2**, **P8**, **P9** | — | ~2 h | G1, G2 |
| **5** | **P1–P4**, **P14**, **P15**, GATE W/W′/W″ | — | ~3 h | all artifacts present |
| **5f** | prediction frozen and committed | — | — | git object recorded |
| **6** | **UNBLIND** — only after §10 returns clean **and the order is given** | — | ~1 h | — |
| **7** | **P11** patch isotropy, shape scoring, write-up (**P12**, **P13**) | — | — | — |

**Disk is the binding constraint and it is worse than BOSS's was.** Free space at Stage 0's close:
**~11 GB of 935 GB, and falling** — the box is shared with other running campaigns. The mock plan
this permits, and which is registered as a limit rather than a preference:

> **RULE E-S2-DISK.** Mock **`dat` files only** (2.0 MB each: 256 MB per cap at 128 realisations,
> 1.0 GB per cap at 512 for the `σ` job) plus **one** random file per tracer per cap (~50 MB).
> **The per-realisation random suites (97–137 GB per tracer) are out of reach and are in no plan
> here.** If free space falls below **4 GB**, the `σ` suite is cut from 512 to 128 and the change
> is recorded as an amendment **with the measured byte count**, never silently.

**Compute**: 32 cores, shared. BOSS measured ~26 s/realisation (SGC, 32.8 M cells) after geometry
caching. ELG's volume is 2.6× smaller than BOSS SGC and LRG's comparable, so Stage 2 is hours.

**Reused unchanged, because rewriting them would forfeit their validation:** `sky_realdata.py`
(grid, interlaced CIC, masked smoothing, quantile binning, `connected_info`, LP pinning,
`configs`), `sky_stage2.CapGeometry` (iterative in-footprint threshold, smoothed
positivity-guarded denominator), `sky_surrogate.phase_randomise` / `measure_pair`,
`sky_stage7.poisson_resample`, `sky_artifact_gates` (Gate A σ-sanity, Gate B mask-perturbation),
and **`bgs_gates.py` in full**. **New code is confined to: eBOSS FITS I/O, the `N_B`/`N_C`
constructions, the GATE W/W′/W″ weight variation, the ELG per-patch geometry, and the eBOSS
`CampaignView` adapter.**

---

## 12. WHAT THIS DOCUMENT DOES NOT LICENSE

1. **It does not license the unblind.** Eric's review is one gate and the unblind order is a
   separate one.
2. **It does not license any stance change under any outcome.** `wild-share` stays open until a
   completed measurement passes a separate refuter pass and Eric's review. This is a confirmation
   attempt, not a claim.
3. **It does not license quoting BOSS's published significances.** The priors of record are §1's
   corrected numbers, and P12 makes that enforceable.
4. **It does not license calling this an independent sample without qualification.** 23–31 % of
   the confirmation volume shares BOSS's density field (§2.2), and the qualifying sentence is
   registered verbatim there.
5. **It does not license an anomaly claim** (outcome (b) withdrawn), nor a primordial reading.
6. **It does not license reading the ceiling fraction as a compliance statement** (§4.5). `ln 2`
   is the proved cap for three *binary* slots; these readings are at `b ∈ {4, 6}`.
7. **It does not license pooling caps, patches or tracers into a combined significance** (§5.4).
8. **It does not claim novelty.** Connected information is Schneidman, Still, Berry & Bialek
   (2003) and Amari (2001); the copula question is Scherrer, Berlind, Mao & McBride (2010) with a
   non-Gaussian copula reported by Qin, Yu & Zhang (2020) on simulations; IAAFT is Schreiber &
   Schmitz (1996); interlacing is Sefusatti et al. (2016); EZmock is Chuang et al. (2015); the
   eBOSS DR16 LSS catalogues are Ross et al. (2020). Per `convergent-art-pattern`, a novelty
   sweep **by mathematical object** is required before any write-up, and its absence of a hit is
   weaker evidence than a hit would be.
9. **It does not promise the campaign is possible.** §2.4 registers the expectation that it lands
   on (c) or (e), and §2.1 states the structural reason.
10. **It does not assert that its author has seen any eBOSS clustering statistic.** He has not.
    Stage 0 read positions, redshifts, weights and the shipped `NZ` column; no order-3 quantity,
    correlation function or power spectrum has been evaluated on any eBOSS catalogue at the
    moment of this commit.

---

*Pre-registration ends here. No eBOSS share has been computed. No `lake`, no Lean, no
`Stance.lean`, no audit is involved in this campaign at any stage.*
