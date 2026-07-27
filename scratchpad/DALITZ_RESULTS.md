# DALITZ RESULTS — the whole-only CP share of charmless three-body `B±` decays is NULL, and the null is gauged

Pre-registered in `DALITZ_PREREG.md` (`53db89d`), committed **before** any code existed and
before any Dalitz distribution, share, asymmetry or null had been computed. Prior art
adjudicated in `DALITZ_PRIOR_ART.md` (`727e006`); data inventoried in `DALITZ_DATA.md`
(`7510576`). Both were committed first.

**Scratchpad only.** No Lean file, no `Stance.lean`, no audit, `lake` was never run, nothing
pushed. Nothing here is proposed for the published page.

**Scope, first.** This is the LHCb 2011 open dataset (CERN Open Data record 4900), four modes of
which two are clean, our own selection, no released efficiency map. **It is not an LHCb
measurement and must not be described as one.**

---

## VERDICT

**Pre-registered outcome O2: no whole-only CP asymmetry, at a sensitivity we measured rather
than assumed.**

> On 13 537 `B± → K±K⁺K⁻` candidates, the whole-only share of `(x, y, c)` — the two binarised
> Dalitz coordinates and the CP tag — is **9.19 × 10⁻⁵ nats**, against a charge-permutation null
> whose median is **1.65 × 10⁻⁵** and whose spread is **5.20 × 10⁻⁵**. The excess is
> **7.5 × 10⁻⁵ nats, p = 0.118** on 10⁵ permutations. **Null.**
>
> The null is **gauged, not empty**: the pre-registered dye test locates the 5σ sensitivity at a
> **5 % whole-only CP asymmetry**, and a **checkerboard CP asymmetry of 6 % or larger is
> excluded at 95 %**. What the instrument would have seen, it did not see.
>
> The pre-declared secondary **`B± → π±π⁺π⁻`** carries 49 010 candidates — 3.6 times the primary
> — and is also null (share 1.82 × 10⁻⁵, **p = 0.185**), giving the campaign's **tightest
> limit: a whole-only CP asymmetry of ε ≥ 0.03 is excluded at 95 %**, with 5σ sensitivity at
> ε = 0.025.
>
> The instrument's defining property was demonstrated on the data's own statistics rather than
> argued. A pure-pair CP asymmetry was injected, **verified present** — the CP asymmetry gap
> between the two `x` bins moved from −0.0001 to **+0.1995**, twenty percentage points — and the
> whole-only reading **did not move**: median share 1.74 × 10⁻⁵ → 1.81 × 10⁻⁵ over 200 draws.
> Meanwhile a 5 % whole-only asymmetry is seen at 5σ. **That is the pairwise blindness,
> measured, with the injection independently confirmed to have happened.**

**One thing did not come out clean, and it is reported here rather than in a footnote.** The
pre-registered threshold-stability scan contains a contiguous cluster of high readings at
`X`-quantile 0.575. Correctly look-elsewhere corrected over the nine occupancy-passing
configurations, its global significance is **p = 0.017**. That is not a detection, it is not
cashed, and per `DALITZ_PREREG.md` §9 it may not become the headline. It is named in §8 as the
single thing a follow-up pre-registration on independent data would target.

---

## 1. THE HONEST ACCOUNTING — what fired, including on my own machinery

Seven things went wrong on my side: five defects in my own instruments and two pre-registered
expectations that turned out to be wrong. Five were caught mid-run, two after it. All seven are
recorded with what they cost, and none was quietly repaired.

| | what | outcome |
|---|---|---|
| **D1** | The stage-2 dye test used **one fixed base permutation**, so the injected parity component first *cancelled* that realisation's own random parity fluctuation before growing. This is why the stage-2 Dye A curve is non-monotone and dips **below** the floor at ε = 0.01–0.02. | **My defect.** Fixed by averaging over 60 independent base permutations (`dalitz_stage2b.py`). The corrected curve is monotone and gives the sensitivity quoted above. The stage-2 numbers are superseded and are labelled so. |
| **D2** | The first efficiency-immunity test compared harsh-acceptance runs against the **full-sample** floor. The share appeared to rise to z ≈ 2.0 as the acceptance got more severe — which would have been a real failure of the design's central protection. | **A confound, not an effect.** The harsh map also cut the sample from 13 537 to ~3 000, and the estimator's floor scales like 1/N. With **sample-size-matched floors** the rise vanishes entirely (§4). The lesson generalises: *a floor must be matched to the sample size the reading was taken at.* |
| **D3** | `share_range_given_pairs` — the pair-pinning gate — computed `H(p+δσ) − H(p)`, which is **not the share**. Since every member of the fibre shares one pair-maxent, the share is `H* − H(q)`, so the reachable interval is `[0, H* − min_δ H]`. | **My bug**, in the gate itself. Corrected in `dalitz_share.py` with the reasoning in the docstring. The corrected gate passes far more decisively than the buggy one appeared to (§5). |
| **D4** | `DALITZ_PREREG.md` §6b predicted the two-resolution LP interval would **shrink** with `b` and become uninformative. | **Wrong, in the informative direction.** The interval barely moves: width 1.449 at `b = 4`, 1.395 at `b = 8`. The gate stayed wide and is a genuine pass, not the vacuous check I predicted. |
| **D5** | `DALITZ_PREREG.md` §8 asserted Dye C (a band asymmetry inside one `x` cell) "must NOT be seen". Mid-run I convinced myself this was **wrong** — a band's `y`-profile generally differs from its cell's, which should generate share. | **The prereg's expectation held**, but for a reason narrower than it stated: the effect exists but is far below this sample's sensitivity. Dye C is therefore a **weak** test, not the clean blindness check the prereg implied, and the clean one is Dye B. Recorded so the prereg is not credited with more than it earned. |
| **D6** | The loader's track assignment for the two **mixed** modes (`K±π⁺π⁻`, `π±K⁺K⁻`) requires a *particular* one of the two same-sign tracks to be the kaon, using the ntuple's arbitrary `H1/H2/H3` order. It should have tried both assignments. Separately, folding the two opposite-sign invariants into (low, high) is correct for `KKK` and `πππ`, where the two same-sign hadrons are **identical**, but for the mixed modes it merges two physically distinct spectra. | **My defect**, caught after the run. **The `K±π⁺π⁻` and `π±K⁺K⁻` arms are therefore not interpretable as physics** and are reported in §7a as recorded-but-void. The two clean modes — `K±K⁺K⁻` and `π±π⁺π⁻` — are unaffected, and both are null. |
| **D7** | A single-draw version of the Dye B control appeared to show the share rising to 2.9 × 10⁻⁴ under a pure-pair injection, which would have fired **K2** and killed the implementation. | **A fluctuation, not an effect.** The share's null distribution is **χ²₁-like** — measured ratio of 99th percentile to median 9.8, against 14.6 for an exact χ²₁ — so it has a heavy right tail and a single draw carries almost no information. Over 200 draws the share is flat (§3c). **Consequence for reading this document: `z` computed from a median and a standard deviation is a poor summary of a χ²-shaped null, and the p-values are the honest measure throughout.** |

Nothing in this table changes the verdict. **D1, D2 and D7 would each have produced a false
alarm** had they gone uncaught — D7 would have fired a kill and killed the implementation.
**D3 would have produced a false reassurance**, and **D6 voids two of the four mode arms.**
Four of the seven were caught by a control disagreeing with another control rather than by
inspection, which is an argument for redundancy in the battery rather than for care.

---

## 2. THE OBSERVABLE, IN ONE PARAGRAPH

`DALITZ_PREREG.md` §1 proves that the mission's natural design — the three two-body masses as
three slots — is degenerate: with `m²₁₂+m²₁₃+m²₂₃ = C` exactly, cell `(+,+,+)` needs
`C > t₁+t₂+t₃` and `(−,−,−)` needs `C < t₁+t₂+t₃`, so **at least one of the eight sign cells is
empty for every choice of thresholds**, as a matter of kinematics. The observable is therefore
the whole-only share of `(x, y, c)`: `x` and `y` binarise the two ordered opposite-sign
invariants `m²(K⁺K⁻)_low`, `m²(K⁺K⁻)_high`, and `c` is the `B` charge. It is the part of the CP
asymmetry invisible to the charge-integrated Dalitz density and to **both** one-dimensional
asymmetry profiles. It vanishes exactly under CP conservation, and it is immune by construction
to the production asymmetry and to any charge-symmetric efficiency.

---

## 3. PRE-UNBLIND: THE PLUMB LINES AND THE DYE TESTS

### 3a. Plumb lines (PREREG §5) — all six pass to machine precision

| input | required | measured | |
|---|---|---|---|
| `parity` | `log 2` | 0.693147180559945**2** | (`log 2` = …45**3**; 1 ulp) |
| `copied` | 0 | 0.0 | exact |
| `ferro` | 0 | 0.0 | exact |
| 400 random **sign-symmetric** tables | 0 | max 4.4 × 10⁻¹⁶ | `share_eq_zero_of_signSymmetric`, machine-checked in Lean, used as a control on my code |
| 400 random **product** tables `P(x,y)·P(c)` | 0 | max 4.4 × 10⁻¹⁶ | the CP-conservation zero |
| uniform | 0 | 0.0 | exact |

**K7 does not fire.** The estimator is the exact 1-D `k=3` solver; **no IPF was used at any point
in this campaign**, at any stage, for any arm.

### 3b. Dye tests (PREREG §8) — the docimasia, run in both directions

All on **permuted** data, before any real charge label was used. 60 independent base
permutations per point; floor from 2 × 10⁴ permutations (median 1.65 × 10⁻⁵, sd 5.29 × 10⁻⁵).

| ε | **Dye A** whole-only — *must be seen* | **Dye B** pure-pair — *must NOT be seen* |
|---|---|---|
| 0.00 | 3.10e−5 (z = 0.27) | 3.28e−5 (z = 0.31) |
| 0.01 | 4.38e−5 (z = 0.52) | 4.84e−5 (z = 0.60) |
| 0.02 | 8.48e−5 (z = 1.29) | 3.87e−5 (z = 0.42) |
| 0.03 | 1.46e−4 (z = 2.44) | 3.93e−5 (z = 0.43) |
| 0.04 | 2.17e−4 (z = 3.78) | 3.37e−5 (z = 0.32) |
| **0.05** | **3.98e−4 (z = 7.20)** | 4.86e−5 (z = 0.61) |
| 0.06 | 4.91e−4 (z = 8.96) | 2.46e−5 (z = 0.15) |
| 0.08 | 8.46e−4 (z = 15.7) | 4.18e−5 (z = 0.48) |
| 0.10 | 1.24e−3 (z = 23.1) | 3.09e−5 (z = 0.27) |
| 0.15 | 2.94e−3 (z = 55.2) | 4.25e−5 (z = 0.49) |
| **0.20** | 5.16e−3 (z = 97.1) | **3.77e−5 (z = 0.40)** |

**The pre-registered deliverable: the smallest ε recovered at 5σ is ε = 0.05**, i.e. a share of
**4.0 × 10⁻⁴ nats**. A median run clears 5σ at that same ε.

**Dye B is the result of this section.** A pure-pair CP asymmetry of **20 %** — four times the
whole-only asymmetry the instrument sees at 5σ — leaves the reading flat at its floor, with no
trend whatever across a factor of 20 in ε. **K2 does not fire, and the instrument's pairwise
blindness is a measurement rather than a definition.** This is the check `GATES.md` finding C
says we most often skip.

**Dye C** (band asymmetry, ε up to 0.10) stayed at the floor throughout — a pass, but see **D5**:
it is a weak test and should not be credited as a second blindness demonstration.

### 3c. The control on the control — was the pair asymmetry actually injected?

Dye B's flatness means nothing unless the injection it is blind to was really there. Verified
directly, over 200 independent draws, by reading the injected asymmetry out of the pair marginal
it was injected into — the gap in CP asymmetry between the two `x` bins:

| | injected `A_CP` gap | share (median) | share (mean) | share (p95) |
|---|---|---|---|---|
| no injection | −0.0001 ± 0.017 | 1.74e−5 | 3.23e−5 | 1.10e−4 |
| **Dye B, ε = 0.20** | **+0.1995 ± 0.019** | **1.81e−5** | 3.57e−5 | 1.13e−4 |

**A twenty-percentage-point CP asymmetry is injected, confirmed present in the pair marginal to
0.1995 ± 0.019, and the whole-only reading does not move.** This is the campaign's central
instrumental result, and it is what separates the observable from every two-sample statistic in
`DALITZ_PRIOR_ART.md` §3 — all of which would report this injection as a large CP signal.

The same 200 draws also fix the **shape** of the null: the ratio of its 99th percentile to its
median is 9.8 (13.3 under injection), against 14.6 for an exact χ²₁. The null is χ²-shaped with
a heavy right tail, which is why **p-values, not `z`, are the honest summary everywhere in this
document** (see **D7**).

---

## 4. PRE-UNBLIND: THE NULLS

### 4a. Flat phase space (PREREG §7b) — K6 does not fire

13 537 events generated uniform in the physical Dalitz region by exact rejection sampling
against the two-body boundary, charges assigned at 50/50, identical pipeline:

> share **5.35 × 10⁻⁵**, null median 1.58 × 10⁻⁵, **z = 0.71, p = 0.234**.

The Dalitz boundary's shape and the level-set geometry manufacture nothing. This is the control
that would have caught §2's excluded design.

### 4b. Efficiency immunity (PREREG §7c) — the design's central protection, tested

A **charge-symmetric** acceptance applied identically to both charges on permuted data, with the
permutation floor recomputed **at the surviving sample size** (see **D2**):

| acceptance ratio across the plane | events surviving | share | z vs matched floor |
|---|---|---|---|
| 1.0 (none) | 13 537 | 3.53e−5 | 0.37 |
| 3.1 | 7 059 | 7.96e−5 | 0.44 |
| 8.2 | 4 211 | 1.70e−4 | 0.70 |
| **15.6** | 2 963 | 9.55e−5 | **0.10** |

**No trend with the severity of the acceptance.** A charge-symmetric efficiency varying by a
factor of **16** across the Dalitz plane manufactures no whole-only share. `DALITZ_PREREG.md`
§2.3's protection — the property that makes a dataset with no public efficiency map usable — is
**measured, not argued**, as the sky campaign's *directional-claims-are-measured* gate requires.

---

## 5. THE PRIMARY READING

**Unblinded after §3 and §4 were complete.** Thresholds fixed on the charge-integrated sample
(CP-blind by construction): `X̃ = 2.399 GeV²`, `Ỹ = 12.750 GeV²`. Tied fraction
**7.4 × 10⁻⁵** at each threshold.

| | |
|---|---|
| candidates in the signal window | **13 537** (7 133 `B⁺`, 6 404 `B⁻`) |
| cell counts `(x,y,c)` | 1131, 1571 / 1953, 2114 / 1939, 2128 / 1381, 1320 |
| **occupancy gate** (≥ 1000 per cell) | **PASS**, minimum cell 1131 |
| **share** | **9.188 × 10⁻⁵ nats** |
| permutation null (10⁵) | median 1.651 × 10⁻⁵, sd 5.197 × 10⁻⁵ |
| excess | 7.54 × 10⁻⁵ |
| **p** | **0.118** |

**Null.** For scale: the measured value sits where Dye A puts a whole-only CP asymmetry of about
**2–3 %**, which is well inside the floor's own spread.

### The exclusion limit

Calibrating against the dye curve — the fraction of injected runs whose share falls at or below
the observed value:

| ε | 0.00 | 0.01 | 0.02 | 0.03 | 0.04 | 0.05 | **0.06** | 0.07 |
|---|---|---|---|---|---|---|---|---|
| `P(share ≤ observed)` | 0.863 | 0.857 | 0.663 | 0.463 | 0.243 | 0.100 | **0.030** | 0.010 |

> **A whole-only ("checkerboard") CP asymmetry of ε ≥ 0.06 — a ±6 % relative rate difference
> between `B⁺` and `B⁻` in the diagonal pattern that no pair marginal shows — is excluded at
> 95 % on this dataset.**

---

## 6. THE GATES ON THE READING

### 6a. Pair-pinning at analysis resolution (PREREG §6a) — K5 does not fire

Using the **corrected** gate (see **D3**): every distribution carrying the measured table's three
pair marginals has a share somewhere in

> **[0, 0.370 nats]** — a width **4 029 times** the measured value.

The measured share uses **0.02 %** of the range it was free to move in. The reading is
emphatically **not** a restatement of the pair marginals. `DALITZ_PREREG.md` §6a predicted this
gate would pass, and gave the reason; it passes by a far larger margin than expected.

### 6b. Two-resolution LP (PREREG §6b) — and the prereg was wrong about it (**D4**)

Linear program over all distributions on the `b × b × 2` fine table carrying the measured fine
pair marginals `P(x_f,y_f)`, `P(x_f,c)`, `P(y_f,c)`, maximising and minimising the coarse
sign-triple:

| `b` | `T` observed | `T` range | width | coarse share reachable |
|---|---|---|---|---|
| 4 | −0.00214 | [−0.671, +0.779] | **1.449** | up to 0.371 |
| 8 | −0.00214 | [−0.671, +0.724] | **1.395** | up to 0.305 |

The interval **did not collapse** — it barely moved between `b = 4` and `b = 8`. The
pre-registered expectation that it would shrink toward pinning, and would therefore be
uninformative, was **wrong**; the gate is a genuine pass. Knowing the fine Dalitz density and
both fine one-dimensional asymmetry profiles leaves the whole-only share almost entirely free,
which is exactly the independence the observable was designed to have.

### K3. Magnet polarity — does not fire, but the test is UNDERPOWERED and that is the finding

| arm | N | min cell | share | null median | z | p |
|---|---|---|---|---|---|---|
| MagnetDown | 7 928 | **659** | 3.81e−5 | 2.85e−5 | 0.11 | 0.435 |
| MagnetUp | 5 609 | **472** | 1.99e−4 | 3.93e−5 | 1.27 | 0.133 |

`|z_Up − z_Down| = 1.16`, far below the 3σ bar: **K3 does not fire.** But **both arms fail the
pre-registered occupancy floor of 1000 events per cell** (659 and 472). By this campaign's own
rule those arms are **ungauged**, so the polarity control's *discriminating power is not
established* — its agreement is weak evidence, not a clean cross-check. Reported as loudly as a
detection would be, per `GATES.md`'s treatment of the ungauged outcome.

### K4. Sidebands — does not fire, and is also underpowered

Mass sidebands, 1 163 events, minimum cell **126**: share 2.71e−4, null median 1.97e−4,
**z = 0.12, p = 0.432**. Consistent with zero, so **K4 does not fire** — but at 126 events per
cell this arm too is far below the occupancy floor and is **ungauged**. The background is not
demonstrated clean; it is merely not demonstrated dirty.

---

## 7. THE THRESHOLD-STABILITY SCAN, AND ITS LOOK-ELSEWHERE

25 configurations, `X`- and `Y`-quantiles each over {0.35, 0.425, 0.5, 0.575, 0.65}.
**16 of the 25 fail the pre-registered occupancy floor and are ungauged.** The nine that pass:

| `X`q | `Y`q | share | min cell |
|---|---|---|---|
| 0.350 | 0.650 | 8.7e−9 | 1003 |
| 0.425 | 0.575 | 5.4e−5 | 1145 |
| 0.425 | 0.650 | 2.5e−7 | 1025 |
| **0.500** | **0.500** | **9.2e−5** *(the primary)* | 1131 |
| 0.500 | 0.575 | 8.0e−5 | 1048 |
| **0.575** | **0.425** | **3.35e−4** | 1089 |
| **0.575** | **0.500** | **3.01e−4** | 1062 |
| 0.650 | 0.350 | 1.29e−4 | 1025 |
| 0.650 | 0.425 | 7.1e−5 | 1067 |

There is a contiguous cluster at `X`q = 0.575 — and, among the occupancy-failing configurations,
it continues to `(0.575, 0.350)`, the largest reading in the whole scan. Contiguity in a scan is
what a real localised effect looks like, and it is also what a fluctuation looks like when
neighbouring configurations share most of their events.

**The look-elsewhere calculation, done properly.** Over 3 000 charge-permutation replicas, taking
the **maximum share across the same nine configurations** in each replica:

> null max-share median **7.8 × 10⁻⁵**, 95th percentile **2.45 × 10⁻⁴**, 99th **3.73 × 10⁻⁴**;
> observed max **3.35 × 10⁻⁴** ⇒ **global p = 0.017**.

**That is a 2.1σ-equivalent trials-corrected excess. It is not a detection and it is not
cashed.** Per `DALITZ_PREREG.md` §9 a secondary configuration may not become the headline; the
primary is null and stays the headline. What this cluster earns is one sentence in §8 and a
place in a future pre-registration — **not** a claim, and **not** a "hint" quoted without its
global p.

---

## 7a. THE PRE-DECLARED SECONDARY MODES

Run per `DALITZ_PREREG.md` §9 with the trials factor stated: four modes were declared, so any
significance below carries a factor of 4.

| mode | N | min cell | occupancy | share | null median | **p** | share / max reachable |
|---|---|---|---|---|---|---|---|
| `K±K⁺K⁻` *(primary)* | 13 537 | 1 131 | PASS | 9.19e−5 | 1.65e−5 | **0.118** | 2.0e−4 |
| **`π±π⁺π⁻`** | **49 010** | 5 079 | PASS | 1.82e−5 | 4.67e−6 | **0.185** | 3.8e−5 |
| `K±π⁺π⁻` | 48 302 | 5 024 | PASS | 7.40e−7 | 4.91e−6 | 0.782 | 1.6e−6 |
| `π±K⁺K⁻` | 3 805 | 410 | **FAIL** | 3.13e−6 | 6.17e−5 | 0.891 | 5.2e−6 |

**All null.** No mode approaches significance, before or after the trials factor.

**Two of the four arms are void, and the reason is my defect, not the data's** (see **D6**):
`K±π⁺π⁻` and `π±K⁺K⁻` were processed with a track assignment that requires a particular one of
the two same-sign tracks to be the kaon, taken from the ntuple's arbitrary ordering, and with a
(low, high) folding that merges two physically distinct spectra. Their readings are recorded
above for completeness and **must not be interpreted**. `π±K⁺K⁻` additionally fails occupancy.

**`π±π⁺π⁻` is clean and is the campaign's most sensitive arm.** Two identical same-sign pions
make the folding not merely valid but required, and it carries 3.6 times the primary's
statistics. Its own dye calibration:

| ε | 0.000 | 0.005 | 0.010 | 0.015 | 0.020 | **0.025** | 0.030 |
|---|---|---|---|---|---|---|---|
| mean share | 1.11e−5 | 1.61e−5 | 2.30e−5 | 3.69e−5 | 6.05e−5 | **9.06e−5** | 1.15e−4 |
| z | 0.44 | 0.79 | 1.28 | 2.25 | 3.89 | **5.99** | 7.70 |
| `P(share ≤ observed)` | 0.805 | 0.720 | 0.635 | 0.410 | 0.160 | 0.075 | **0.010** |

> **`B± → π±π⁺π⁻`: 5σ sensitivity at ε = 0.025, and a whole-only CP asymmetry of ε ≥ 0.03 is
> excluded at 95 %** — twice as tight as the primary's limit, and the strongest statement this
> campaign makes.

**A pre-registration lesson, recorded against myself.** `DALITZ_PREREG.md` §3 chose `K±K⁺K⁻` as
primary because the open dataset's selection was built around it. That reasoning was sound but
the consequence was costly: after our own PID selection the two pion-rich modes yield **3.6
times more candidates**, and the primary mode is the *least* sensitive clean arm in the
campaign. Declaring the primary on a yield estimate — which could have been made from the
charge-integrated data without unblinding anything — would have been strictly better, and costs
nothing in blinding. That is the rule to carry forward.

---

## 8. WHAT A FOLLOW-UP WOULD DO

Named here so that if anyone returns to this, the target is fixed in advance rather than chosen
after another look at the same data.

1. **The `X`q = 0.575 region of `B± → K±K⁺K⁻`, pre-registered as a single configuration**, on
   **independent data** — LHCb's 2012 open-data release, or the Run 1 stripping streams
   (`DALITZ_DATA.md` §1). Testing it again on the 2011 sample would be testing the fluctuation
   that generated it.
2. **Make `π±π⁺π⁻` the primary**, on a yield estimate taken from the charge-integrated data
   before unblinding (§7a). It is clean by construction, it is 3.6 times the size, and it
   already gives twice the limit.
3. **Fix the mixed-mode track assignment** (D6) — try both same-sign assignments, and drop the
   (low, high) folding for `K±π⁺π⁻` and `π±K⁺K⁻` in favour of the two physically distinct
   invariants. That recovers two arms of ~48 000 candidates each, which is more statistics than
   everything clean in this campaign combined.
4. **More statistics is the whole game.** The sensitivity floor scales roughly as `N^{-1/2}`;
   the full Run 1 `B → hhh` sample is one to two orders of magnitude larger than what is used
   here, which would reach ε of order 0.003–0.01.
5. **The occupancy floor must be met by the polarity and sideband arms**, not only the primary.
   In this run neither control was gauged, and that is the single largest structural weakness of
   the result (§6).

---

## 9. SCORECARD AGAINST WHAT WAS WRITTEN IN ADVANCE

| | pre-registered | outcome |
|---|---|---|
| plumb lines (§5) | six exact values | **ALL PASS**, machine precision. K7 does not fire |
| Dye A (§8) | must be seen; quote the 5σ ε | **SEEN**; 5σ at ε = 0.05 |
| Dye B (§8) | must NOT be seen | **NOT SEEN** to ε = 0.20. K2 does not fire |
| Dye C (§8) | must NOT be seen | not seen — but the test is **weak** (D5) |
| Dye B injection verified | not pre-registered; owed | **injection confirmed present** at `A_CP` gap +0.1995 ± 0.019 while the share stayed flat (§3c) |
| flat phase space (§7b) | consistent with the floor | **z = 0.71, p = 0.234**. K6 does not fire |
| efficiency immunity (§7c) | share stays at the floor | **PASS to a factor 16**, after D2 was fixed |
| occupancy (§4) | ≥ 1000 per cell | **PASS** on the primary (1131); **FAIL** on both polarity arms and the sideband |
| **primary** | — | **share 9.19e−5, p = 0.118 — NULL (outcome O2)** |
| gate 6a (§6a) | expected to pass | **PASS**, width 4 029× the measured value (after D3 fixed) |
| gate 6b (§6b) | expected to shrink and be uninformative | **WRONG (D4)** — stayed wide, a genuine pass |
| K3 polarity | 3σ bar | **does not fire** (1.16σ) — but both arms **ungauged** on occupancy |
| K4 sideband | 3σ bar | **does not fire** (0.12σ) — arm **ungauged** on occupancy |
| K5 pair-pinning | range < 20 % of measured | **does not fire** — range is 402 900 % of measured |
| K6 flat phase space | above floor | **does not fire** |
| secondaries (§9) | run with the trials factor | **all four null**; two void by my own defect (D6); `pipipi` clean and the most sensitive arm |
| search caps (§9) | declare and correct | **declared**; scan corrected to **global p = 0.017**, not cashed |

---

## 10. WHAT IS NOT CLAIMED

1. **No claim about nature beyond one dataset.** LHCb 2011 open data, one mode, our own
   selection, no efficiency map. Not an LHCb result.
2. **No stance change.** Nothing here touches `wild-share`, `adequacy`, `cp-cap`, the maximal-CP
   wager, or any Logos claim. `Core/FlavorBridge.lean` is a **model** bridge; this measurement is
   neither its confirmation nor its refutation, and its own header already says so.
3. **No priority claim.** `DALITZ_PRIOR_ART.md` grades the campaign **CONVERGENT-ADJACENT with an
   unswept web**, and its §4 credit paragraph — Bediaga *et al.*'s Miranda procedure, Williams'
   energy test, Davis–Menzo–Youssef–Zupan's optimal-transport statistic, and Schneidman *et al.*
   for the measure itself — is carried on anything arising from this work.
4. **No T-odd claim.** Triple products vanish identically in three-body decays of a spinless
   parent (`DALITZ_PRIOR_ART.md` §5). Our slots are binarised Dalitz coordinates and a charge
   tag, not momenta.
5. **The `X`q = 0.575 cluster is not a hint, a tension, or an indication.** It is a trials-
   corrected p = 0.017 in a scan whose primary configuration is null, and it is quoted only with
   that number attached.
6. **`b = 2` only.** No magnitude is quoted at any finer rung; the finer rungs appear solely
   inside gate 6b, as pre-registered.
7. **The `K±π⁺π⁻` and `π±K⁺K⁻` readings are not results.** They are recorded with the defect
   that voids them (D6) so that nobody re-derives them and believes them.
8. **The polarity and sideband controls were not gauged.** Their agreement is reported, and so is
   the fact that neither met the occupancy floor that would have made the agreement mean
   something.

---

## FILES

| | |
|---|---|
| `DALITZ_PRIOR_ART.md` | convergent-art adjudication — `727e006` |
| `DALITZ_DATA.md` | public-data inventory — `7510576` |
| `DALITZ_PREREG.md` | pre-registration — `53db89d`, before any code |
| `dalitz_share.py` | estimator (exact 1-D `k=3`), plumb lines, loader, nulls |
| `dalitz_stage2.py` | thresholds and the first dye tests — **superseded by stage 2b (D1)** |
| `dalitz_stage2b.py` | corrected dye tests, the sensitivity floor |
| `dalitz_stage3.py` | flat phase space, efficiency immunity |
| `dalitz_stage4.py` | the unblinding: primary, polarity, sidebands, both pinning gates, the scan |
| `dalitz/*.json` | every reading above, as produced |

Data (`scratchpad/dalitz/data/`, 1.1 GB from CERN Open Data record 4900) is gitignored and not
committed. Seed 20260726/20260727 throughout.
