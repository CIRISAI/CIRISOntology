# PRE-REGISTRATION — the confirmation campaign, on DESI DR1 BGS

The BOSS DR12 measurement (`SKY_REALDATA_*.md`) returned outcome (a) and was then **wounded** by
its own pre-registered refuter (`REFUTER_RESULTS.md`). This document pre-registers the
confirmation run on an independent survey. It is written and committed **before any DESI file
has been downloaded, opened or listed**.

**The author of this document has seen mocks and BOSS only.** Every number below about a DESI
catalogue, a DESI mock suite, a DESI column name or a DESI file size is recalled from the
published literature or from the data-release documentation as I remember it, is marked
*[to verify]*, and must be read off the actual headers at Stage 0 before any analysis choice
depends on it. Where I am unsure whether a thing exists at all, I say so in those words rather
than assuming it.

**`lake` has not been run. No Lean file, `Stance.lean`, or audit is involved, and none will be.**

**The deliverable is this document.** The unblind order is not the author's to give.

---

## 0. WHAT THIS DOCUMENT IS FOR

`Stance.lean` carries **`wild-share`** as **open**: does any of nature's unengineered processes
carry whole-only pattern — structure that no pair of observers can reconstruct? BOSS returned a
reading that met outcome (a) and then lost every one of its quoted significances to its own
refuter. **`wild-share` did not move, and should not have.** This run exists to decide it.

A confirmation is not a repetition. It has to attack the specific things that wounded the first
reading, on data whose systematics are not the same data's systematics. §1 is the wound; §2 is
the honest audit of whether DESI BGS actually heals it; §3 is the gate battery that carries over
as a hard prerequisite.

---

## 1. THE PRIORS OF RECORD

These are the **refuter-corrected** numbers, not the campaign's published ones. The campaign's
own numbers (9.4 / 13.5 / 50.8 σ) are **superseded and may not be quoted anywhere in this
campaign** except as labelled history (gate 12, current-numbers hygiene).

**Prior of record — detection significance, BOSS DR12, corrected under the refuter's `N2mw`
null** (`REFUTER_RESULTS.md` §A9):

| cap | `R` | `b` | campaign said | **prior of record** | at `ε = 0.5` | at `ε = 1` |
|---|---|---|---|---|---|---|
| **NGC** | **15** | **4** | 9.4 σ | **6.0 σ** | 5.6 σ | **4.6 σ** |
| **NGC** | **15** | **6** | 13.5 σ | **9.7 σ** | 8.5 σ | 7.4 σ |
| NGC | 10 | 4 | 40.5 σ | 20.9 σ | 12.7 σ | **1.1 σ** |
| NGC | 10 | 6 | 46.8 σ | 26.3 σ | 17.5 σ | 5.0 σ |
| NGC | 10 | 8 | 50.8 σ | 29.8 σ | 20.7 σ | 8.4 σ |
| SGC | 10 | 4 | 22.1 σ | 10.9 σ | 7.0 σ | −0.5 σ |
| SGC | 10 | 6 | 26.1 σ | 14.1 σ | 9.2 σ | 1.2 σ |
| SGC | 10 | 8 | 29.0 σ | 16.5 σ | 11.0 σ | 2.3 σ |
| SGC | 15 | 4 | 3.8 σ | **2.3 σ** | — | — |

**Prior of record — what survived, and it is the more informative half.** The refuter's
correction is **common-mode**: it moves the mock-side prediction by 0.56–0.61 where it moves the
data by 0.53–0.65, so *data-versus-prediction consistency survives every correction*
(`−1.91, −1.02, −1.54, −2.35` σ on the four SGC folded rows). **"The data's higher-order
structure matches the mock suite's" is the surviving claim. "The excess above all floors is
9.4–50.8 σ and is a lower bound" is not.**

**Prior of record — the margins that are thin.**

* `ε_crit` (the super-Poisson dispersion at which the reading drops below 5 σ) = **0.63–0.85**,
  against a literature-defensible galaxy stochasticity reaching **ε ≈ 0.5**. Margin **1.3–1.7×**.
* The catalogue's own weights are already **12.9 % (NGC) / 15.2 % (SGC) super-Poisson**
  (`κ = ⟨w²⟩/⟨w⟩`), and the BOSS null carried none of it.
* Sensitivity to fibre-collision weighting: **2.5–2.9 σ**, with the pre-registered §7.5 VOID gate
  **never run** and **not dischargeable with DR12 columns**.
* Cap asymmetry NGC > SGC on **4 of 4** folded rows by 5–9 %, worst **2.15 σ**, where Patchy
  predicts the caps equal to 0.2 %.
* The pointwise channel is **not bounded** by any null the campaign ran. An over-generous
  lognormal null eats the entire target (ratios −0.18 to −1.29).

**These nine caveats are this campaign's checklist**, and §3 maps each one to a numbered
prerequisite. A confirmation that reproduces the detection without moving any of these margins
confirms nothing.

---

## 2. THE CONFIRMATION PREMISE, TESTED AGAINST OUR OWN RECORD — AND IT IS PARTLY WRONG

The commission's premise is that BGS's 10–100× density "collapses the valve floor and the
stochasticity margin". **My own measured record does not support the word *collapses*, and I am
recording that before designing around it rather than discovering it at Stage 5.**

### 2.1 The density lever on the valve floor is worth about 2.5–3×, not 10–100×

Two independent routes through the campaign's own numbers, and they agree:

**Route 1 — the direct shot-noise minting measurement** (`SKY_FORECAST_RESULTS.md` §12; the
control that MINTED). Minted whole-only share on a field whose true share is exactly zero,
`R = 10`, as density falls:

| `n̄` [(h/Mpc)³] | minted share |
|---|---|
| `1e-2` (BGS-like) | `3.70e-03` |
| `1e-3` | `4.90e-03` |
| `1e-4` (LRG/ELG-like) | `1.10e-02` |

**Two decades of density buys a factor of 2.97.** Not ten, not a hundred. The reason is on the
record: at `R = 10` the *post-sampling smoothing* — a cross-cell filter that no no-creation
theorem covers — dominates over the per-cell sampling channel, and smoothing does not care how
many galaxies went into the cell.

**Route 2 — the floor-versus-signal interpolation** used by Amendment 1. `n̄V_R = 1.6` → 130 % of
signal; `n̄V_R = 15.7` → 58 %. A factor 9.8 in `n̄V_R` bought 2.24. Extrapolating the same log
slope from BOSS's `n̄V_R = 16.2` at `R = 15` to a BGS-like `n̄V_R` of order 250 *[to verify]*
gives another factor **≈ 2.6**, landing near **22 % of signal**.

> **Registered expectation, stated before the run: the valve floor falls by a factor of 2–3, to
> roughly 20–25 % of signal at `R = 15`. If Stage 5 measures a fall larger than 5×, that is a
> surprise and it is reported as one — most likely a difference in the smoothing channel, not a
> vindication of the premise.**

### 2.2 What DESI BGS *does* buy, ranked honestly

1. **Independent systematics.** BOSS fibre collisions, BOSS imaging weights, BOSS mask. DESI
   shares none of them. This is the single largest gain and it is the actual meaning of
   "confirmation". A cap asymmetry (caveat 6) that reappears in DESI is physics or is a shared
   pipeline bug; one that does not reappear was BOSS's.
2. **A dischargeable weight-variation VOID gate** — *if* DR1 BGS ships an alternative
   fibre-assignment scheme (§8). BOSS could not discharge it at all. This retires caveat 5 or
   states in writing that it cannot be retired.
3. **An N-body prediction.** AbacusSummit is N-body *[to verify that DR1 ships public cutsky BGS
   mocks from it]*. MultiDark-Patchy is not, which is why Amendment 4 withdrew outcome (b) and
   why outcome (a) had to be phrased as "consistent with the Patchy suite's higher-order
   structure". A first-principles suite removes that hedge from outcome (a)'s wording.
4. **A factor 2–3 on the valve floor**, per §2.1 — real, and worth having, and not a collapse.
5. **A new lever the premise did not name: small `R`.** At BGS density, `R = 8` sits in the same
   shot-noise regime BOSS's `R = 15` did *[to verify]*, and smaller smoothing volumes multiply
   the number of independent volumes as `R⁻³`. This is how BGS's *smaller volume* (§5.3) is paid
   for. It is registered as an extension arm in §7.3 with a rule, not a choice.

### 2.3 What BGS costs, stated because it cuts against the choice

**Volume.** BOSS DR12's shell volume was `5.388 (Gpc/h)³` (measured, Amendment 1). A BGS sample
over `0.1 < z < 0.4` on ~7 500 deg² is of order **`1 (Gpc/h)³`** *[to verify]* — roughly **5×
smaller**. The occupancy gate counts independent smoothing volumes, so **a 5× volume loss is a
5× occupancy loss, and the occupancy gate has already tightened three times in this
programme's history.** §7.2 works the consequence through and it is not comfortable: at
`R = 15` the `b` ladder may support **`b = 4` only, per cap** — which by the S2.3b precedent is a
single-rung result that cannot satisfy outcome (a) alone.

**This is the biggest reason the confirmation could fail, and it fails for the opposite reason
BOSS nearly did.** BOSS was density-limited; BGS is volume-limited. The design consequence is
§7.3's extension arm, and if that arm is unavailable the confirmation is scoped to `R = 10` and
below, or it does not happen.

---

## 3. THE TWELVE GATES, AS NUMBERED PREREQUISITES

`GATES.md`'s closing harvest registers twelve gates minted by the BOSS run and its refutation,
with the standing consequence that **all twelve are prerequisites for this run, the first seven
mechanizable in the pipeline driver itself.** They are restated here as numbered prerequisites
with a named discharge point and a named artifact. **A gate whose artifact does not exist is not
discharged, whatever anyone remembers** (that is prerequisite P7's whole content).

The first seven are **mechanized in `bgs_gates.py`**, which exposes `require_discharged(stage)`.
The unblind entry point calls it and **raises** if any entry is unresolved. Human-run gates are
marked as such with no rounding up.

| # | gate | mechanized? | discharge point | artifact | retires caveat |
|---|---|---|---|---|---|
| **P1** | **valve floor** — the null carries shot-noise NON-Gaussianity, not only its power; Poisson-resample through the identical selection | **driver** | Stage 5 | `bgs_stage5_valve.json`, key `valve[row]` present and finite for every reported row | — |
| **P2** | **null-construction sweep** — every surrogate-normalised reading reported under **≥ 2** defensible null constructions; the spread is a **quoted systematic** | **driver** | Stage 5 | `bgs_stage5_nulls.json` carries ≥2 null tags per row; `spread` field non-null | **1** |
| **P3** | **directional claims are measured** — any "conservative direction" / "lower bound" argument is TESTED by varying the mechanism | **driver** | Stage 5 | `bgs_stage5_direction.json`: clipped-fraction varied over ≥3 values, sign of `d(floor)/d(clip)` recorded | **2** |
| **P4** | **dispersion sweep** — nulls swept to literature-plausible super-Poisson dispersion; report `ε_crit` and the margin | **driver** | Stage 5 | `bgs_stage5_dispersion.json`: `eps_crit` per row, and measured `κ` from the catalogue's own weights | **3** |
| **P5** | **same null both sides** — prediction and data scored against **identically constructed** nulls | **driver** | Stages 4 + 6 | `bgs_null_signature.json`: the null-construction hash is identical on the mock side and the data side; driver compares and raises on mismatch | — |
| **P6** | **outcome completeness** — before unblinding, enumerate the "large, well-controlled reading whose decomposition was not performed" outcome, and every other non-verdict | **driver** | this document, §9 | §9 enumerates (a)(c)(d)(e); driver asserts the outcome-tag it emits is one of the enumerated set | — |
| **P7** | **gate discharge before unblind** — NO unblind while any pre-registered VOID gate is undischarged; discharge verified **against the record**, not memory | **driver** | Stage 6 entry | `bgs_gates.require_discharged('unblind')` reads every artifact above off disk and raises on any absence | **5** |
| **P8** | **lag-matched probes** — probes scan their structural parameter; equal spacing is an assumption to be tested | human | Stage 4 | the configuration parameter `rmult` swept over ≥3 values on mocks, reported; `rmult = 1.5` is not assumed | — |
| **P9** | **search caps declared** — bounded searches report their cap and saturation; a saturated search is a lower bound, never a count | human | Stages 1, 4 | IPF iteration cap and LP solver iteration cap reported per solve, with the saturated fraction | — |
| **P10** | **delocalisation correction** — masked-field surrogates carry the footprint power-restriction factor, **derived not tuned** | human | Stage 3 | the `1/√f` factor **re-derived for the DESI footprint** and checked against the measured `σ` ratio, as BOSS did (0.3887 vs `√0.154 = 0.3924`) | — |
| **P11** | **patch isotropy** — independent sky patches agree in **AMPLITUDE**, not merely each-vs-prediction | human | Stage 6 | ≥4 volume-matched patches; amplitude dispersion scored against the **mock-predicted** dispersion | **6** |
| **P12** | **current-numbers hygiene** — results documents carry only current-amendment numbers; superseded numbers appear only labelled as superseded | human | write-up | every superseded figure in this campaign's documents carries the word "superseded" on the same line | **8** |

**Caveats 4, 7 and 9 are not gates and are handled directly:**

* **Caveat 4 (the primary scale survived only narrowly).** §9(a) sets a **margin requirement**
  in advance rather than a bare 5 σ threshold.
* **Caveat 7 (the configuration-shape clause was never scored).** §9(a) makes shape a scored
  sub-criterion with its own rule, over **all** geometries, not folded only.
* **Caveat 9 (the pointwise channel is unbounded).** §4.4 registers a third null, `N3`, whose
  job is exactly to bound it.

---

## 4. TARGET STATISTIC, AND THE DUAL-NULL REQUIREMENT

### 4.1 The statistic carries over unchanged

`I_C⁽³⁾(b)`: the order-3 connected information of a `b`-level quantile-binned triple of smoothed
cells — the entropy gap between the state and the maximum-entropy state carrying its three pair
marginals. Estimated by IPF with the KL certificate `|share_H − share_KL| < 1e-9` (G9). Nothing
about the estimator changes; it was independently reimplemented and agreed to `9e-13` relative
(refuter A5), which is the one thing in the BOSS run that needs no re-litigation.

**Primary configuration: folded/collinear**, sides `(r, 2r, r)` with `r = rmult·R`,
`rmult = 1.5` — **and `rmult` is swept, not assumed** (P8).

### 4.2 The target, and why it is not a single number

    TARGET(null)  =  I_C⁽³⁾(data)  −  I_C⁽³⁾(null)

**P2 forbids reporting `TARGET` under one null.** Every reported row carries the target under at
least two independently-constructed nulls, and **the spread between them is quoted as a
systematic on the same line as the value.** The BOSS run reported one, and the refuter's second
construction moved it by 30–52 %.

### 4.3 The two required nulls, both pre-specified now

**`N_A` — the BOSS pipeline null (`N2`), carried over unchanged for comparability.**
Phase-randomise the gridded masked `δ` (keeping `|F(k)|`, applying the `1/√f` delocalisation
correction of P10), then Poisson-resample at the field's own `n̄(z)` through the identical
selection: `λ = α·n̄_ran·max(1 + δ_PR, 0)`. Carries shot-noise power **and** shot-noise
non-Gaussianity.

**`N_B` — the refuter's construction (`N2mw`), which is the one that cut BOSS by 30–52 %.**
The modulation carries the **clustering only** — the shot-noise power is removed in Fourier
*before* the phases are randomised, so Poisson supplies it once rather than twice — renormalised
to the data's own number density, and the counts are drawn with the data's own **weighted** shot
noise `κ = ⟨w²⟩/⟨w⟩`. On BOSS this dropped the clipped fraction from **37 % to 3.5 %** and
**raised** the floor by 24–50 %.

> **Registered in advance: `N_B` is the null of record for outcome (a).** `N_A` is reported
> beside it for comparability with BOSS and to make the spread visible. This is the branch the
> refuter's finding forces, and choosing it now removes the freedom to choose it later.

### 4.4 `N_C` — the pointwise-channel bracket (caveat 9)

The BOSS campaign had **no measurement bounding the pointwise channel**. Its attempt (`N2L`,
lognormal) was unfair by construction: a monotone per-cell map does not commute with smoothing,
so it manufactures genuine order-3 structure — the exact defect that killed the Stage 3 control
at skewness `+1.6688` and that the pilot measured at 66 σ.

**The fair construction, registered here:** match the **smoothed** field's one-point law *and*
its power spectrum, leaving nothing but higher-order phase coupling to differ. That is
**IAAFT** (iterative amplitude-adjusted Fourier transform) applied to the smoothed field.

> **`N_C` := IAAFT surrogate of the smoothed field, matched in marginal distribution and in
> `P(k)`.** Reported per row as a **bracket on the pointwise channel**, never as the null of
> record.

**The known limit of `N_C`, stated so it cannot be oversold** (house lesson
`temporal-share-realdata-nulls`): *IAAFT survival is not sufficient evidence of anything* — a
clip artifact has survived an IAAFT null at `z = 86` in this programme's own history. `N_C` is
used in one direction only: **if `TARGET(N_C) ≤ 0`, the pointwise channel is not bounded and
§9(e) applies.** A positive `TARGET(N_C)` is *not* independent confirmation and may not be
quoted as a significance.

### 4.5 Blinding

Blinding is **enforced in code**, as in BOSS: the data-reading entry point raises unless an
explicit unblind flag is passed, and that flag is set only at Stage 6, only under the unblind
order, and only after `bgs_gates.require_discharged('unblind')` returns clean. The prediction is
frozen to a committed JSON before Stage 6 and its git object is checked byte-identical at
scoring time (the check refuter A8 ran on BOSS and that BOSS passed).

---

## 5. DATA CHOICE — every property [to verify] at Stage 0

### 5.1 The sample

**Primary: DESI DR1 BGS**, LSS catalogues from `data.desi.lbl.gov` (public DR1), NGC and SGC,
with the released randoms. *[Everything in this subsection is to verify.]*

Two candidate samples, and **the choice is made at Stage 0 by a pre-registered rule, not by
preference**:

| | `BGS_BRIGHT-21.5` | `BGS_BRIGHT` |
|---|---|---|
| what it is *[to verify]* | absolute-magnitude-cut sample used for the DR1 full-shape analysis | the full `r < 19.5` bright sample |
| `N` *[to verify]* | ~300 000, `0.1 < z < 0.4` | substantially larger, strongly `z`-dependent |
| `n̄` *[to verify]* | roughly flat, order `5e-4`–`1e-3` | reaches `~1e-2` at `z < 0.2`, falls steeply |
| the problem | density gain over BOSS is only ~2–3×, not 10–100× | `n̄(z)` varies by orders of magnitude across the shell |

> **RULE S0-A, fixed now.** Compute `n̄V_R` at `R = 15` for both samples from the read `n̄(z)`.
> **Choose the sample with the larger `min(n̄V_R)` over the redshift range actually used**, where
> the range is trimmed to keep `n̄V_R` within a factor of 3 of its median (BOSS's uniform-density
> prediction already missed by 1.45× on a 10× `n̄(z)` variation — S1.2 — and a steeper gradient is
> a worse instrument, not a better one). Record both computations. If the two samples tie within
> 20 %, take `BGS_BRIGHT-21.5`, because it is the sample the collaboration's own mocks and
> systematics tests are built for.

**This is the honest reading of the commission's premise.** The "10–100× BOSS density" figure
describes `BGS_BRIGHT` at low `z`, over a small volume, with a steep selection. The sample with
a usable selection function may be the one with only a 2–3× density gain. Stage 0 decides it on
the read numbers and records which.

### 5.2 Redshift range and the growth lever

*[to verify]* `0.1 < z < 0.4`, `z_eff ≈ 0.3`. **The growth lever is dead on arrival and I am not
going to pretend otherwise**: `D(0.1)/D(0.4) ≈ 1.08`, giving a predicted signal ratio of ~1.06
with `A ∝ D^0.82`, requiring **~4 % per-bin precision** for 3 σ. BOSS needed 6.3 % and returned
*uninformative* exactly as pre-registered.

> **Registered: the growth check is reported as UNINFORMATIVE unless per-bin precision reaches
> 4 %, and it is expected to be uninformative. It is not a discriminator and no outcome depends
> on it.**

### 5.3 Volume, and the occupancy problem it creates

*[to verify]* DESI DR1 BGS footprint of order **7 500 deg²** over `0.1 < z < 0.4` gives a shell
volume of order **`1.0 (Gpc/h)³`** against BOSS's measured `5.388`. §7.2 works the occupancy
through. **If the read footprint gives a shell volume below `0.6 (Gpc/h)³`, the `R = 15` arm is
expected to fail the occupancy gate at every `b` in at least one cap, and §7.3's extension arm
becomes the primary rather than an extension — that reassignment is pre-registered here and is
not a Stage-5 decision.**

### 5.4 Disk, and the scoping trade

**Measured now, before any download: 43 GB free** on the working filesystem (935 G total, 96 %
used). `/home/emoore/skydata` already holds **62 GB** of BOSS tarballs and catalogues, none of
which may be deleted.

> **RULE S0-B, fixed now.** If the DESI download required for both caps exceeds **35 GB**, the
> campaign is **scoped to NGC only** — the larger cap, and the one that carried outcome (a)'s
> two-rung clause in BOSS.
>
> **The trade, stated rather than discovered:** a single-cap run **cannot** run the NGC-vs-SGC
> cap-consistency check that produced caveat 6. **P11 is therefore satisfied by sub-patches
> within the retained cap** — ≥4 volume-matched patches, amplitude dispersion scored against the
> mock-predicted dispersion — which is a *stronger* test than the two-cap version because it has
> more than one degree of freedom. This is a redesign of the check, not a waiver of it.

Mocks are **stream-processed and never fully extracted**, as Amendment 1 established. If a mock
suite is distributed as per-realisation files rather than a monolithic tarball, the pattern is
**download → measure → delete**, one realisation at a time, so peak storage is one realisation.

---

## 6. MOCKS — AND WHETHER THE FLOOR-PRECISION ARGUMENT TRANSPORTS

**This is the section most likely to end the campaign, and it is written before looking.**

### 6.1 What the BOSS run needed the mocks for, and how well

Three distinct jobs, and they have different precision requirements — the BOSS documents did not
always separate them and this one does:

| job | what supplies it | precision needed | BOSS achieved |
|---|---|---|---|
| **floor mean** (G10 closure numerator/denominator) | half-suite means | 10 % of signal | 0.14 % of floor — **70× inside the bar** |
| **σ for the detection** | realisation scatter | sets the quoted significance | 16 mocks ⟹ **σ uncertain by ±18 %**, i.e. "9.4 σ" carried ±1.7 σ from ensemble size alone |
| **the prediction** | suite mean | ≲1 % | 128 mocks; prediction moved <1 % from 16 → 128 |

**The `128-per-cap` argument was never about 128.** Amendment 2 measured the per-realisation
scatter of `I_C⁽³⁾` at **0.5–1.1 % of the floor mean** — ten times smaller than the mock campaign
had suggested — and *that* is why 128 sufficed with 70× margin. **The argument transports to any
suite size `n` for which `0.011/√n` stays inside the G10 bar**, which is satisfied at `n = 25`
(0.22 %) and even at `n = 8` (0.39 %) **if and only if the scatter on DESI geometry is
comparable.** That conditional must be measured, not assumed:

> **RULE S2-A.** Measure the per-realisation scatter of `I_C⁽³⁾` on the first 8 DESI mocks before
> committing to a suite size. If the scatter exceeds **3 %** of the floor mean, the transported
> argument fails and the required `n` is recomputed and recorded in an amendment.

**The `σ` job does not transport the same way**, and this is where a small suite bites: `σ` from
`n` draws is uncertain by roughly `1/√(2(n−1))`, so **`n = 25` gives ±14 %** and `n = 16` gave
BOSS ±18 %. A confirmation that quotes a significance carrying ±14 % from ensemble size alone is
repeating BOSS's weakest habit.

### 6.2 What DR1 ships — recalled, and all of it [to verify]

| suite | *[to verify]* what I believe | N-body? | job it could do |
|---|---|---|---|
| **AbacusSummit cutsky** (`SecondGenMocks`) | ~25 realisations covering the DESI footprint; whether BGS cutsky is in the **public** DR1 release is **the thing I am least sure of** | **yes** | prediction + floor (§7.1 closure satisfied for the first time in this programme) |
| **EZmock cutsky** | ~1000 realisations; effective-Zel'dovich, **not** N-body — the same class as Patchy | no | `σ` / covariance |

> **RULE S0-C.** Stage 0 reports, from the actual directory listing and file headers: which
> suites exist publicly for BGS, how many realisations, the per-realisation file size, the total
> bytes, and the columns. **Every one of those is currently a guess.**

### 6.3 The suite assignment, pre-registered with its own closure requirement

**If both suites exist:** AbacusSummit supplies **both** the floor model and the prediction (the
§7.1 same-suite closure requirement, satisfied); EZmock supplies **σ** only.

> **RULE S2-B — the cross-suite closure check, required.** `σ` measured on the EZmock suite and
> `σ` measured on the (smaller) AbacusSummit suite must agree within their own errors. **If they
> disagree, the larger `σ` is used, the disagreement is reported on the same line as every
> significance, and no significance is quoted to more than one significant figure.**

**If only EZmock exists:** the prediction provenance is no better than BOSS's, outcome (b) stays
withdrawn (it is withdrawn in this run regardless — §9), and outcome (a) keeps the Amendment-4
phrasing "consistent with the suite's higher-order structure". Recorded, not fatal.

**If neither exists publicly for BGS:** **the campaign stops at Stage 0 and reports that.** A
run with no floor model is not a measurement, and this programme's entire discipline says the
floor model — not statistics — is what decides.

> **This is the acceptable deliverable the commission named: "DR1 mocks cannot support the
> floor-precision argument yet" is a real outcome and is reported at the volume a detection
> would be.**

---

## 7. SCALES, THE `b` LADDER, AND THE OCCUPANCY GATE

### 7.1 The gate, unchanged

Occupancy = (independent smoothing volumes) / `b³`, where independent volumes are
`N_valid · cell³ / ((2π)^{3/2} R³)` — **not** galaxies and **not** raw triple counts (the error
S1.2(b) caught, which overstated independence by ~250×). Gate: **> 100**. Applied **per cap and
per scale**, never pooled — pooling two footprints is a mixture, and mixtures manufacture
higher-order structure from none (`ECA_SPIKE_RESULTS.md`; Amendment 2 §A2.3).

### 7.2 The forecast, and it is tight

Working BOSS's measured chain forward to a `1.0 (Gpc/h)³` BGS shell with the same ~0.5 boundary
retention *[all to verify]*:

| `R` | independent volumes (est.) | `b = 4` | `b = 6` | `b = 8` |
|---|---|---|---|---|
| 15 | ~9 000 | ~140 **marginal** | ~42 **FAIL** | ~18 **FAIL** |
| 10 | ~31 000 | ~480 PASS | ~143 PASS | ~60 **FAIL** |
| 8 | ~60 000 | ~940 PASS | ~278 PASS | ~117 PASS |

Split by cap the `R = 15` row fails outright in the smaller cap. **`R = 15` is expected to be a
single-rung scale at best, and outcome (a)'s two-or-more-`b` clause cannot rest on it** — the
same S2.3b situation BOSS hit in SGC, arriving here at the primary scale in both caps.

### 7.3 The extension arm, with a rule instead of a choice

> **RULE S0-D — the extension scale.** Let `R★` be the **smallest** `R` in `{12, 10, 8, 6}` at
> which the read `n̄V_R` is **≥ 16.2** — BOSS's measured `n̄V_R` at its own primary scale. `R★` is
> added to the analysis as a pre-registered scale. If no `R` in the set qualifies, there is no
> extension arm and the campaign runs `R ∈ {15, 10}` only.

**`R★` is a confirmation of the phenomenon, not of the BOSS reading**, and the two are reported
under different headings. The confirmation-proper scales are `R = 15` and `R = 10`, identical to
BOSS. `R★` is where BGS can actually speak, and its shot-noise regime is matched *by
construction* to the regime BOSS's primary scale sat in — which is what makes it a fair place to
look rather than a fishing expedition.

**The honest cost of `R★`, registered now:** it is a **new scale**, so (i) it carries no binmint
(G2) measurement — Stage 4 must run the binmint control **at `R★`** before it is read, exactly as
Amendment 1 required at `R = 15`, and if it behaves like `R = 25` did (`t_corr = 0.5–0.9`,
i.e. the signal does not survive coarse-graining) the arm is dropped; (ii) smaller `R` means more
nonlinearity, so the mock prediction is doing more work; (iii) it adds trials — §9's
look-elsewhere accounting covers it explicitly.

### 7.4 The `b` ladder

`b ∈ {4, 6, 8}` as before, decided by the occupancy gate per cap and per scale, nothing excluded
by hand. `b = 2` remains demoted to diagnostic (the binmint control fired on it). `b ≥ 16`
remains excluded in advance (the `kappa-edge` VOID regime).

---

## 8. THE WEIGHT-VARIATION VOID GATE, DESIGNED AGAINST DR1 COLUMNS

`SKY_REALDATA_PREREG.md` §7.5 is a **VOID** condition and the BOSS campaign **never ran it**
(caveat 5). It is restated here as a prerequisite that must be discharged before the unblind
(P7), and — per the commission — it is designed against the columns DR1 actually ships, with the
fallback written now rather than improvised if the columns are absent.

### 8.1 What Stage 0 must read, before any design is fixed

*[All to verify — these are column names I believe DR1 LSS catalogues carry, and I may be wrong
about any of them.]* `WEIGHT`, `WEIGHT_COMP` (fibre-assignment completeness, believed
`1/FRACZ_TILELOCID`), `WEIGHT_ZFAIL`, `WEIGHT_SYS` / imaging-systematics weights, `WEIGHT_FKP`,
`NX`/`NZ`, `FRACZ_TILELOCID`, `TILELOCID`, and — **the column this gate lives or dies on** —
**`BITWEIGHTS` / PIP weights** from the alternative-MTL realisations.

### 8.2 The gate, if DR1 ships an alternative fibre-assignment scheme

> **GATE W (primary form).** Recompute the target under (i) the default completeness weighting
> and (ii) the PIP / bitweight scheme, with **paired null seeds** so the null realisation cancels
> between schemes (the refuter's `refuter_a2.py` technique). **A shift exceeding the row's
> statistical error VOIDs that bin.**

This is the discharge BOSS could not perform, because DR12 carries no alternative scheme in
file. **If DR1 carries one, caveat 5 is retired for the first time in this programme.**

### 8.3 The gate, if it does not — the discharge that IS possible

**Said plainly: if DR1 BGS ships no alternative fibre-assignment scheme, the fibre-collision
analogue of §7.5 cannot be discharged in its primary form, and this document says so in advance
rather than reporting a pass that was never available.** What *is* available with any catalogue
carrying a per-object completeness column:

> **GATE W′ (fallback form) — the high-completeness subsample test.** Restrict to regions with
> completeness above a threshold `c★` (pre-registered at `c★ = 0.95`, adjusted at Stage 0 only if
> that threshold retains less than 30 % of the sample, in which case the largest threshold
> retaining 30 % is used and the number is recorded). In that subsample the fibre-assignment
> correction is **small by construction**, so the correction cannot be carrying the signal.
>
> **Score:** the target measured on the high-completeness subsample must agree with the
> full-sample target within the **mock-predicted** scatter for a subsample of that volume — the
> mocks supply the expected volume-scaling, so this is a scored comparison and not an eyeball.
> **A disagreement exceeding the mock-predicted scatter VOIDs the affected bin.**

**Why W′ is a real discharge and not a consolation prize.** The failure mode caveat 5 identifies
is that a spatially-correlated deletion-and-upweighting operation imprints order-3 structure that
lands inside the target with nothing subtracting it. W′ tests exactly that: it removes most of
the operation and asks whether the reading moves more than volume alone explains. It is weaker
than W in one specific way — it cannot distinguish "the correction is right" from "the correction
is wrong but small where completeness is high" — and that limitation is stated in the results,
not omitted.

**Both W and W′ are run if both are available.** Neither substitutes for the other.

### 8.4 Imaging systematics

BOSS's imaging channel was **CLEAR at ≤ 0.62 σ**. DESI's imaging systematics are different in
kind (three imaging surveys, different depth structure), so the BOSS result **does not
transport** and the variation is run: default vs no-`WEIGHT_SYS` vs any published alternative
(linear vs random-forest regression weights, if DR1 ships both *[to verify]*). Same VOID rule.

---

## 9. PRE-REGISTERED OUTCOMES AND KILLS — separable, and now COMPLETE

Outcome completeness is prerequisite **P6**, minted because the BOSS unblind produced a reading
that **fit no pre-registered outcome**. The enumeration below is closed: the driver asserts that
the outcome tag it emits is one of these five.

### (a) CONFIRMATION

*Criterion — every clause must hold, and each is separately reported:*

1. **Detection.** `TARGET(N_B)` positive at **≥ 5 σ** above the combined forward-modelled floor,
   folded configuration, at **two or more `b` rungs passing the occupancy gate within a single
   cap and scale**.
2. **Margin (caveat 4).** The **same rows** hold ≥ 5 σ at **`ε = 1.0`** — full extra
   Poisson-variance dispersion — i.e. **`ε_crit ≥ 1.0`**. BOSS's `ε_crit` was 0.63–0.85 and
   *failed* this. **A confirmation that does not move `ε_crit` past 1.0 does not confirm; it
   reproduces a wound.**
3. **Null-construction stability (caveat 1).** The spread between `TARGET(N_A)` and
   `TARGET(N_B)` is **quoted**, and the ≥ 5 σ verdict holds under **both**.
4. **Pointwise bracket (caveat 9).** `TARGET(N_C) > 0` on the primary rows. (Positive is
   necessary, not sufficient — §4.4.)
5. **Consistency in amplitude.** `|data − prediction| ≤ 3 σ` on the primary rows.
6. **Consistency in shape, SCORED (caveat 7).** Over **all** geometries at each scale — folded,
   equilateral, squeezed — the data/prediction ratios must show **no coherent scale-dependent
   trend**: the ratio's mean over non-folded rows must lie within 3 σ of the folded mean, at each
   scale separately. **BOSS would have failed this clause had it been scored** (all twelve
   non-folded `R = 10` rows below prediction at 0.71–0.94, all five non-folded `R = 15` rows
   above at 1.02–1.82). It is scored here, and a failure is reported as a failure of clause 6
   with the other clauses' verdicts standing.
7. **Patch isotropy not fired (caveat 6, P11).** Amplitude dispersion across ≥ 4 volume-matched
   patches within the mock-predicted dispersion.
8. **Weight gate discharged (caveat 5, §8).** GATE W and/or W′ run, and not voiding the row.

*What it licenses:* **`wild-share` gets its first confirmed YES instance** — and only then. The
interpretive stake is unchanged and is not renegotiated: the non-pointwise (tidal/shift) sector
counts as a YES, existence and not novelty-of-mechanism being the question.

*What it does not license:* any primordial-non-Gaussianity reading; any claim that the whole-only
share is *large* (`kappa-edge`'s H-BLIND puts the degree-3 direction at ~1 % of fine-grained
structure); any continuum claim (everything here is binned; the pilot measured binarised/continuum
ratios of 1.11–6.6); **any stance change without a separate refuter pass and Eric's review.**

### (b) EXCESS BEYOND PREDICTION — **WITHDRAWN, as in BOSS**

Withdrawn for this run regardless of mock provenance. If Stage 0 finds a public N-body suite, that
fact is **recorded** as making a future outcome-(b) campaign well-posed for the first time, and
nothing more. An anomaly claim needs its own pre-registration and its own refuter pass; it is not
a free rider on a confirmation run.

### (c) NULL ABOVE THE FLOORS

*Criterion:* `TARGET(N_B)` consistent with zero after all floors, with the floor uncertainty
measured.

*What it licenses:* **an honest upper bound** on the whole-only order-3 excess of the galaxy
density field at the stated scales and configurations, with the instrument validated by the gate
battery. **`wild-share` stays open** — and, given BOSS returned a wounded positive, a DESI null
is a substantive result about BOSS's systematics and is reported at exactly the volume a
detection would be.

### (d) VOID — the run produces no result

Any of: the Gaussian/surrogate control failing its exit diagnostics; **G1** pair-pinning at
analysis resolution; **G10** mock closure failing; **G9** failing at every `b`; the IPF
certificate exceeding `1e-9`; **P5** null-signature mismatch between the mock side and the data
side; **P7** finding any undischarged gate at the unblind boundary; GATE W or W′ voiding every
primary row.

*What it licenses:* a report of the void with the failing number, and nothing else.

### (e) NOT DECOMPOSED — the outcome BOSS produced and had not enumerated

*Criterion:* a **large, well-controlled reading whose decomposition into signal and floor could
not be performed** — concretely, any of:

* `TARGET(N_A)` and `TARGET(N_B)` differ by more than **50 %** of the larger (BOSS: 30–52 %,
  which sits right at this line and is why the line is drawn here);
* `TARGET(N_C) ≤ 0`, i.e. the pointwise channel is **not bounded** by any null run;
* the valve floor is not separable from the reading because the null's own skewness is dominated
  by clipping rather than by Poisson (the Amendment 5 §A5.3 condition, now **measured** under P3
  rather than argued).

*What it licenses:* **the reading is reported, in full, with its decomposition explicitly marked
as not performed, and it is not a detection and not a null.** It does not move `wild-share` in
either direction. **This outcome exists because the BOSS unblind landed here and the document had
nowhere to put it**, and the reading was cashed as a detection for one document-generation before
Amendment 5 caught it.

### Look-elsewhere accounting, declared in advance

Rows scored: 2 caps (or 1 under RULE S0-B) × up to 3 scales (`15`, `10`, `R★`) × up to 3 `b`
rungs × 3 geometries. **The two-rung clause of (a) is eligible only in folded**, and the
confirmation-proper verdict is read at `R = 15` and `R = 10`; `R★` is reported under its own
heading. At the significances in play a trials factor of order 10 costs ~0.3 σ at 6 σ, which is
recorded and is not a live threat — but it is recorded *before* the numbers, which is the point.

---

## 10. THE UNBLIND CHECKLIST — hard, machine-verified, and the unblind order is not the author's

**`bgs_gates.require_discharged('unblind')` reads each artifact off disk and raises on absence.
Nothing here is satisfied by recollection.**

| # | check | artifact key |
|---|---|---|
| 1 | Stage 0 inventory complete; every `[to verify]` in this document replaced by a read number | `bgs_stage0_inventory.json` :: `to_verify_resolved == true` |
| 2 | Sample chosen by RULE S0-A with both computations recorded | `.. :: rule_s0a` |
| 3 | Scoping decision by RULE S0-B recorded with the measured byte count | `.. :: rule_s0b` |
| 4 | Mock suites inventoried by RULE S0-C; suite assignment fixed | `.. :: rule_s0c` |
| 5 | `R★` fixed by RULE S0-D, or recorded as absent | `.. :: rule_s0d` |
| 6 | Scatter check RULE S2-A passed or amended | `bgs_stage2.json :: scatter_ok` |
| 7 | Cross-suite σ closure RULE S2-B run | `bgs_stage2.json :: sigma_closure` |
| 8 | **G10** mock closure PASS, per row, with the failures named | `bgs_stage2.json :: g10` |
| 9 | **G1** LP pair-pinning PASS at analysis resolution | `bgs_stage4.json :: g1` |
| 10 | **G2** binmint quantified, **including at `R★`** | `bgs_stage4.json :: g2` |
| 11 | **P8** `rmult` swept ≥3 values | `bgs_stage4.json :: rmult_sweep` |
| 12 | **P10** delocalisation factor re-derived for the DESI footprint | `bgs_stage3.json :: deloc` |
| 13 | **P1** valve floor measured, all rows | `bgs_stage5_valve.json` |
| 14 | **P2** ≥2 nulls per row, spread quoted | `bgs_stage5_nulls.json :: spread` |
| 15 | **P3** direction measured, clip swept ≥3 values | `bgs_stage5_direction.json` |
| 16 | **P4** `ε_crit` per row; catalogue `κ` measured | `bgs_stage5_dispersion.json` |
| 17 | **P5** null signature identical both sides | `bgs_null_signature.json :: match == true` |
| 18 | **GATE W and/or W′** run, verdict recorded | `bgs_stage5_weights.json` |
| 19 | prediction frozen and git-verified byte-identical | `bgs_frozen_prediction.json` + git object check |
| 20 | this document's outcome set is the driver's outcome set (**P6**) | driver assertion |

**Item 21 is not mechanizable and is stated anyway: the unblind order comes from Eric.** The
driver refuses without the flag; the flag is not set by the author.

---

## 11. RESOURCE PLAN

| stage | what | data | compute | gate before proceeding |
|---|---|---|---|---|
| **0** | Inventory: DR1 BGS LSS catalogues + randoms; mock suites; columns; `n̄(z)`; footprint; **every `[to verify]` resolved**; RULES S0-A/B/C/D applied | catalogues + randoms only *[size to verify]* | ~1 h | all rules applied and recorded; **any discrepancy changing a §5–§7 choice triggers an amendment before proceeding** |
| **1** | Pipeline adaptation: DESI readers, footprint from DESI randoms, weights; **reuse `sky_realdata.py`'s estimator, grid, IPF and LP unchanged** | — | ~0.5 d | the split-randoms null re-run on DESI geometry; G9 and G7 re-passed |
| **2** | Floor model + **G10 closure** on DR1 mocks; RULES S2-A, S2-B | *[to verify]*; stream/delete | hours | **G10. This is the go/no-go.** |
| **3** | Surrogate controls; **P10** delocalisation re-derivation | — | ~1 h | exit diagnostics (`σ` ratio, smoothed skewness ≈ 0) |
| **4** | **G1**, **G2** (incl. at `R★`), **P8** `rmult` sweep, **P9** caps | — | ~2 h | G1, G2 |
| **5** | **P1–P4**: valve floor, dual+bracket nulls, direction, dispersion; **§8 GATE W/W′** | — | ~3 h | all four artifacts present |
| **5f** | Prediction frozen and committed | — | — | git object recorded |
| **6** | **UNBLIND** — only after §10 returns clean **and the order is given** | — | ~1 h | — |
| **7** | Patch isotropy (**P11**), shape scoring, growth check, write-up with fired kills reported as plainly as survivals (**P12**) | — | — | — |

**Compute**: 32 cores, shared. BOSS measured ~26 s/realisation (SGC) and ~55 s (NGC) after
geometry caching; BGS's smaller volume should be cheaper per realisation, and a small suite makes
Stage 2 hours rather than days. **The binding constraints are disk (43 GB) and the public mock
situation, not compute.**

**Reused unchanged** (validated, and rewriting them would forfeit that validation):
`sky_realdata.py` (grid, interlaced CIC, masked smoothing, quantile binning, `connected_info`,
LP pinning, configs), `sky_stage2.CapGeometry` (iterative in-footprint threshold, smoothed
positivity-guarded denominator), `sky_surrogate.phase_randomise` and `measure_pair`,
`sky_stage7.poisson_resample`, `sky_artifact_gates` (Gate A σ-sanity, Gate B mask-perturbation).
**New code is confined to: DESI I/O, the `N_B`/`N_C` null constructions, `bgs_gates.py`, and the
GATE W/W′ weight variation.**

---

## 12. WHAT THIS DOCUMENT DOES NOT LICENSE

1. **It does not license running the measurement.** Eric's review is the gate, and the unblind
   order is separate from the review.
2. **It does not license any stance change under any outcome.** `wild-share` stays open until a
   completed measurement passes a separate refuter pass and Eric's review.
3. **It does not license quoting the BOSS campaign's published significances.** The priors of
   record are §1's corrected numbers.
4. **It does not license an anomaly claim** (outcome (b) is withdrawn), nor a primordial reading
   of anything.
5. **It does not claim novelty.** Connected information is Schneidman, Still, Berry & Bialek
   (2003) and Amari (2001); the copula question is Scherrer, Berlind, Mao & McBride (2010) with a
   non-Gaussian copula reported by Qin, Yu & Zhang (2020) on simulations; IAAFT is Schreiber &
   Schmitz (1996); interlacing is Sefusatti et al. (2016); AbacusSummit is Maksimova et al.
   (2021); EZmock is Chuang et al. (2015). Per the house lesson `convergent-art-pattern`, a
   novelty sweep by mathematical object is required before any write-up and its absence of a hit
   is weaker evidence than a hit would be.
6. **It does not assert that its author has seen DESI data.** He has not. No DESI file has been
   downloaded, opened, or listed at the moment of this commit.
7. **It does not promise the campaign is possible.** §6 names three states of the public mock
   situation and one of them stops the run at Stage 0.

---

*Pre-registration ends here. Nothing below this line existed when it was committed, and no DESI
datum had been read.*
