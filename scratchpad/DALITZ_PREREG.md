# DALITZ PREREG — pre-registration, committed before any measurement

**Committed before any Dalitz distribution, any share, any asymmetry and any null has been
computed.** Companions: `DALITZ_PRIOR_ART.md` (commit `727e006`) and `DALITZ_DATA.md`
(commit `7510576`), both committed before this document.

**Scratchpad only.** No Lean file, no `Stance.lean`, no audit, `lake` will not be run. Nothing
here promotes any claim on the published page.

---

## 0. DISCLOSURE — what has already been seen

Full disclosure, because a pre-registration that hides a look is worthless.

**Seen:** the ROOT tree schema of `B2HHH_MagnetDown.root` (26 branch names and types, 5 135 823
entries) and, over the first 200 000 entries, the distribution of the summed track charge
(101 640 at `+1`, 98 360 at `−1`). That is a pure normalisation count and carries no kinematic
and no Dalitz-position information.

**Not seen:** any invariant mass, any Dalitz coordinate, any distribution, any charge-dependent
kinematic quantity, any share, any asymmetry. The `MagnetUp` file has not been opened at all.

---

## 1. THE STRUCTURAL FACT, AND A DESIGN EXCLUDED BY PROOF

**A three-body Dalitz plot is two-dimensional.** The three two-body invariants obey the exact
kinematic constraint

> `m²₁₂ + m²₁₃ + m²₂₃ = M² + m₁² + m₂² + m₃² ≡ C`

so any three functions of the Dalitz point are three readouts of a **two-dimensional** random
variable. The mission's natural reading — take the three two-body masses as the three slots —
is therefore not merely risky, it is **provably degenerate**, and it is excluded here in advance
rather than discovered later.

### The exclusion, proved

Let the three slots be `sᵢ = sign(m²ᵢ − tᵢ)` for any thresholds `t₁, t₂, t₃` whatever. Then:

- the cell `(+,+,+)` requires `m²₁ > t₁`, `m²₂ > t₂`, `m²₃ > t₃`, hence `C > t₁+t₂+t₃`;
- the cell `(−,−,−)` requires `m²₁ < t₁`, `m²₂ < t₂`, `m²₃ < t₃`, hence `C < t₁+t₂+t₃`.

**At most one of these two cells can be non-empty, and if `t₁+t₂+t₃ = C` exactly, neither can.**
So for *every* choice of thresholds, at least one of the eight sign cells is **empty as a matter
of kinematics**, with no dynamics involved and identically so in flat phase space and in every
model.

An empty cell drives the state to the boundary of the marginal polytope, where the whole-only
share is determined by which cell is empty rather than by the decay. **This design is excluded
in advance and may not be used later without retracting this section.**

Two neighbouring traps, recorded so they are not walked into:

- **The parity trap.** Setting `s₃ = sign((x−x̃)(y−ỹ))` makes `s₃ = s₁s₂` identically, i.e. the
  state is *literally* this repository's `parity`, and the instrument returns its maximum
  `log 2` on any data whatever. Any slot design in which the third slot is a deterministic
  function of the first two is this trap wearing a different face.
- **The mutually-exclusive-band trap.** Three resonance-band membership indicators for bands
  that barely overlap leave the cells with two or three `+1`s nearly empty — the same
  boundary-of-the-polytope pathology, arrived at from the opposite direction.

### The consequence

No natural three-slot design *on the Dalitz plane alone* populates all eight cells, and any that
did would be reading its own level-set arrangement geometry rather than the decay. **The
whole-only share of a Dalitz distribution, with the three slots taken from the plane, is not the
campaign's observable.** What follows is.

---

## 2. THE OBSERVABLE

**The three slots are `(x, y, c)`: two binarised Dalitz coordinates and the CP tag.**

| slot | definition |
|---|---|
| `x` | `+1` if `m²_low > X̃`, else `−1` |
| `y` | `+1` if `m²_high > Ỹ`, else `−1` |
| `c` | `+1` for `B⁺`, `−1` for `B⁻` (the summed track charge) |

with `m²_low`, `m²_high` the lower and higher of the two opposite-sign two-body invariants, and
`X̃`, `Ỹ` thresholds fixed as stated in §4.

**The observable is `share(x, y, c)`** — the whole-only share of this 2×2×2 table, the entropy
gap between the table and the maximum-entropy table carrying its three pair marginals.

### What it means, in one sentence

It is **the part of the CP asymmetry that is invisible to the charge-integrated Dalitz density,
to the CP asymmetry of the `m²_low` projection, and to the CP asymmetry of the `m²_high`
projection** — the CP structure that no *pair* of `{x, y, c}` reveals.

### Why this design and not another — five properties, each of which is a reason

1. **It vanishes exactly under CP conservation.** CP conservation makes the charge independent
   of the kinematics, so `P(x,y,c) = P(x,y)·P(c)`, a product of a function of `(x,y)` and a
   function of `c`. That distribution is its own pair-maxent, so the share is **exactly zero** —
   not approximately, not asymptotically.
   **Provenance, stated precisely and not rounded up:** this repository's `share_copied`
   (`Core/Share.lean`) is the machine-checked special case — third slot independent of the first
   two, share exactly zero — proved via `entropy_grouping` and `marg₃_of_samePairs`. The general
   statement follows by the identical route and is **not** currently mechanized. It is recorded
   here as a candidate Lean brick and is used below as an *elementary fact verified numerically
   in the gate*, never as a machine-checked result.
2. **It is immune to the production asymmetry.** A global excess of `B⁺` over `B⁻` — the 3.3 %
   seen in §0, and the dominant nuisance in every `B±` CP measurement — changes only `P(c)`,
   leaves the product form intact, and contributes **exactly zero**.
3. **It is immune to any charge-symmetric efficiency, however non-uniform.** An acceptance
   `ε(x,y)` multiplies `P(x,y)` and preserves the product form, so it contributes exactly zero.
   **This is the property that makes the LHCb open dataset usable despite no efficiency map
   being public** (`DALITZ_DATA.md` §5), and it converts the inventory's central gap from a
   blocker into a stated, tested assumption.
4. **All eight cells are populated by construction**, since `c` is not a function of the plane.
   §1's exclusion does not touch it.
5. **The pair-pinning gate transfers properly.** Knowing the fine Dalitz density `P(x_f, y_f)`
   and the two fine one-dimensional asymmetry profiles `P(x_f, c)`, `P(y_f, c)` does **not**
   determine the joint. So §6's gate is a real test here, unlike in the excluded design where it
   would have been guaranteed to fire for reasons having nothing to do with the data.

### What it is NOT

It is not a measurement of the whole-only share *of a Dalitz distribution*. That quantity, as
§1 proves, is not well-posed with slots drawn from the plane. Any results document must say so
in its own first section, and must not let the campaign's original phrasing survive into the
write-up.

---

## 3. DATA, MODE, AND SELECTION

**Dataset.** CERN Open Data record 4900, LHCb 2011, `B2HHH_MagnetDown.root` +
`B2HHH_MagnetUp.root`. Verified schema in `DALITZ_DATA.md` §1.

**Primary mode: `B± → K±K⁺K⁻`.** Declared now, before any yield is examined. Reason, stated so
it cannot be re-chosen later: the open dataset's own selection was built around this mode (its
selection cuts on the `B` mass under the all-kaon hypothesis, and the shipped simulation file is
`B → KKK`), so using it is using the data as released rather than repurposing it.

**Pre-declared secondaries**, reported only with the trials factor of §9: `K±π⁺π⁻`,
`π±π⁺π⁻`, `π±K⁺K⁻`.

**Selection, fixed now.**

| cut | value |
|---|---|
| PID, primary mode | `ProbK > 0.5` and `ProbPi < 0.5` on all three tracks |
| muon veto | `isMuon == 0` on all three tracks |
| charge | `|Σ Hᵢ_Charge| == 1` |
| signal window | `|m(KKK) − 5279.3 MeV| < 30 MeV` |
| lower sideband | `5150 < m(KKK) < 5220 MeV` |
| upper sideband | `5340 < m(KKK) < 5410 MeV` |
| charm veto | reject if either `m²(K⁺K⁻)` combination lies within ±30 MeV of the `D⁰` mass (1864.8 MeV), to remove `B → D⁰K` feed-in, which is a different decay with its own CP structure |

No cut on `B_FlightDistance`, `B_VertexChi2` or `IPChi2` beyond what the open dataset already
applied; those are recorded but not used, and any later use is a new configuration counted in
§9.

**Magnet polarity.** The primary reading is `MagnetUp + MagnetDown` combined. Up and Down are
**also** read separately, and their agreement is a pre-registered kill (§10, K3). This is the
one genuine detector-systematics control the dataset affords, and it exists because
detector-induced charge asymmetries largely reverse sign with the magnet polarity while a
physical CP asymmetry does not.

---

## 4. BLINDING, AND THE BINNING LADDER

**Blinding rule.** `X̃` and `Ỹ` are the **medians of the charge-integrated sample** inside the
signal window. The charge-integrated distribution contains no CP information by construction, so
setting thresholds on it cannot tune the observable. The charge labels are attached only after
`X̃` and `Ỹ` are fixed and written into the results file.

**Occupancy gate**, declared in advance: every one of the 8 cells must contain **≥ 1000 events
for each charge separately**. Below that the configuration is **ungauged** — not zero, not a
detection — and is reported as such. (`GATES.md` reach 11.)

**The ladder.** The primary reading is at `b = 2` on each Dalitz coordinate, and **`b = 2` is
the only rung at which a magnitude is quoted.** The reason is on the record and is not being
re-litigated: at `b = 2` the pair-maxent is an exact one-dimensional problem with no iterative
fitting, whereas at `b ≥ 4` it requires IPF, which is known here to **one-sidedly overstate** the
share on sparse or near-deterministic tables (`ISING_FIELD_RESULTS.md` §2: 9.8e−6 read where the
truth was 1.2e−10; the `ipf-sharek-boundary-drift` lesson), and `KAPPA_EDGE_RESULTS.md` §7 voided
its own `b ≥ 16` rungs on exactly this ground.

Finer rungs `b ∈ {4, 8}` are computed as **diagnostics only**, with a two-sided
primal/dual bracket (`GATES.md` reach 12) reported alongside, and are **declared in advance to
be unquotable as magnitudes**.

---

## 5. THE ESTIMATOR

For a 2×2×2 table, the set of distributions carrying all three pair marginals is exactly the
one-parameter family

> `p_δ(s₁,s₂,s₃) = p̂(s₁,s₂,s₃) + δ·(−1)^{[s₁]+[s₂]+[s₃]}`

on the interval of `δ` where all eight cells stay non-negative. The pair-maxent is the entropy
maximum over that interval — a **one-dimensional strictly concave maximisation, solved to
machine precision by bisection on the derivative**. The share is `H(p_δ*) − H(p̂)`.

**No IPF is used at `b = 2`, at any stage, for any arm.** This is the "exact 1-D `k=3` solver"
that `GATES.md` reach 12 names as the plumb line for the bracket.

**Pipeline plumb lines, run before any data is touched** (`GATES.md` reach 1, and the `Ge`/`Gf`
pair from `KAPPA_EDGE_RESULTS.md` §9):

| check | required output |
|---|---|
| `parity` state in | exactly `log 2` |
| `copied` state in | exactly `0` |
| `ferro` state in | exactly `0` |
| any sign-symmetric table in | exactly `0` (`share_eq_zero_of_signSymmetric`, machine-checked) |
| any product table `P(x,y)·P(c)` in | exactly `0` |
| uniform table in | exactly `0` |

A failure on any of these voids the whole run before it starts.

---

## 6. THE PAIR-PINNING GATE — mandatory, with its expectation pre-registered

Two forms, and the distinction between them is pre-registered because conflating them would
manufacture a meaningless VOID.

### 6a. Analysis-resolution gate (the one with teeth here)

Given the three measured pair marginals of `(x, y, c)`, compute the exact interval of `δ` over
which all eight cells stay non-negative, and the range the share takes over it.

- **Expectation, written down in advance:** with millions of events over eight well-populated
  cells and no near-empty cell, the interval will be **wide** — the share will be free to move
  over a range large compared with any plausible reading. I expect this gate to **pass**.
- **It has teeth anyway**, and precisely against §1's failure mode: it fires exactly when a cell
  is near-empty and non-negativity pins `δ`. It is the gate that would have caught the excluded
  design.
- **VOID rule (K5):** if the reachable range of the share is **less than 20 % of the measured
  share** for either charge arm, the reading is **pair-pinned** and is reported as a restatement
  of the pair marginals, not as a whole-only measurement.

### 6b. Two-resolution gate (run, and expected to be uninformative — stated in advance)

Given the **fine** pair marginals `P(x_f, y_f)`, `P(x_f, c)`, `P(y_f, c)` at `b ∈ {4, 8}`,
compute by linear program the range of the coarse `b = 2` share, exactly as
`t_range_given_fine_marginals` does in `kappa_edge.py`.

- **Expectation, written down in advance:** the interval **shrinks monotonically as `b` grows**,
  because a finer `P(x_f, y_f)` localises the event ever more precisely. This is a property of
  the geometry, **not** a finding about the decay.
- **Therefore this gate's firing at large `b` is declared in advance to be uninformative and may
  not be reported as a VOID of the primary reading.** It is reported as a number, with this
  paragraph attached. The mission's warning that "resonance bands ARE pair structure" is
  correct and is *already answered by the design*: a CP asymmetry localised in a resonance band
  appears in `P(x_f, c)` and `P(y_f, c)` — in the pairs — and our observable is **supposed** to
  be blind to it. That is the instrument working, not failing.

---

## 7. NULLS

### 7a. Primary null — charge-label permutation

Pool the events in the signal window, randomly reassign the charge labels preserving the
observed `B⁺`/`B⁻` counts exactly, recompute the share. This null:

- reproduces the Dalitz density **exactly** (it is the data's own density);
- reproduces the sample sizes and the discreteness **exactly**;
- destroys **only** the charge association.

It therefore satisfies `GATES.md` reach 3 (match the null to the data's generative structure)
without modelling anything, and it is the same permutation null the energy test and the Miranda
procedure use — a deliberate choice, so our significance is comparable to the field's.

**`N = 10⁵` permutations for the primary p-value; `N = 10⁴` for scans.** The share is
non-negative, so the null has a **strictly positive floor**; the deliverable is
`share − median(null)` with the p-value, and **the raw share is never reported as a signal**
(`GATES.md` reach 1).

**No tail fitting.** If the observed value exceeds every permutation, the result is reported as
`p < 10⁻⁵` and nothing more. We will **not** fit a generalised extreme value function to the
null tail. This is pre-registered because the energy-test literature made exactly this mistake
and had to correct it — Barter, Burr & Parkes, arXiv:1801.05222, showed the GEV does not
describe the null well enough in a simple test case.

### 7b. Geometric null — flat phase space

Generate events uniform in the Dalitz plane inside the physical boundary, at the data's
statistics, assign charges at the observed proportions, run the identical pipeline. **Expected
reading: consistent with the permutation floor.** This separates the kinematic boundary's shape
and the level-set geometry from anything dynamical. `PhaseSpaceSimulation.root` is *not* used
for this — it is generator-level with its own selection history; we generate our own, where the
distribution is known exactly.

### 7c. Efficiency-immunity null

Apply a deliberately severe **charge-symmetric** reweighting `ε(x,y)` (a factor of 5 across the
plane) to permuted data and verify the share stays at the floor. This *tests* §2's property 3
rather than asserting it — required by the sky campaign's **directional-claims-are-measured**
gate, which exists because we have previously argued a direction from plausibility and been
**falsified in sign**.

---

## 8. THE DYE TEST — the docimasia, and it runs in both directions

`GATES.md` reach 13: a control that has not been shown to see a planted signal of the size that
matters gauges nothing, and its null reading is **ungauged**, not an all-clear.

**Dye A — whole-only injection (must be SEEN).** On permuted data, reweight the `c = +1` sample
by `1 + ε·(−1)^{[x]+[y]}`. This is exactly the parity direction of the 2×2×2 table: it leaves
`P(x,c)` and `P(y,c)` unchanged to first order and injects share and nothing else. Sweep
`ε ∈ {0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1}`.
**Deliverable, quoted with every null reading: the smallest `ε` recovered at 5σ.** A null result
without this number is not reportable.

**Dye B — pure-pair injection (must NOT be seen).** On permuted data, reweight `c = +1` by
`1 + ε·(−1)^{[x]}` — a CP asymmetry entirely inside the `x` projection, i.e. entirely inside a
pair marginal. Sweep the same `ε`.
**Required outcome: the share stays at the floor at every `ε`.** If it moves, the implementation
is not pairwise-blind and **K2 fires**, killing the implementation regardless of what the data
says. This is the direction we have most often skipped and it is mandatory here.

**Dye C — localised-band injection (must NOT be seen).** Inject a CP asymmetry confined to a
narrow band in `m²_low` — the physically realistic case, a resonance with a CP-violating
interference. If the band lies wholly inside one `x` cell this is a pair asymmetry and must not
move the share. This is the concrete form of the mission's resonance-band warning and it is
tested, not argued.

---

## 9. SEARCH CAPS, DECLARED IN ADVANCE

`GATES.md` harvest gate **search caps declared**: a bounded search reports its cap; a saturated
search is a lower bound, never a count.

| axis | configurations |
|---|---|
| modes | 1 primary + 3 pre-declared secondaries = **4** |
| magnet arms | combined (primary) + Up + Down = **3** |
| threshold-stability scan | `X̃`, `Ỹ` each at quantiles {0.35, 0.425, 0.5, 0.575, 0.65} = **25** |
| mass window variations | nominal + 2 = **3** |
| diagnostic `b` rungs | {4, 8} = **2**, unquotable as magnitudes |

**The primary result is ONE configuration**: primary mode, combined polarity, median thresholds,
nominal window. Everything else is secondary and is reported **with the trials factor stated on
the same line as the p-value**. A secondary configuration may not become the headline; if the
primary is null and a secondary is significant, the honest report is "the primary is null; a
secondary at 1-in-N trials showed X", and the follow-up is a new pre-registration on new data,
not a promotion.

---

## 10. OUTCOMES AND SEPARABLE KILLS

### Outcomes, enumerated before unblinding — including the non-verdicts

`GATES.md` harvest gate **outcome completeness** exists because a previous unblind fit no
pre-registered outcome. The list below is meant to be exhaustive.

| # | outcome | report |
|---|---|---|
| **O1** | share significantly above the permutation floor; all gates pass; Up and Down agree; sidebands clean | **A CP asymmetry in the whole-only sector of this dataset is detected.** Strength: a *measured* reading about the LHCb 2011 open dataset under our own selection — **not** an LHCb result, **not** a stance promotion, and carrying the efficiency caveat of `DALITZ_DATA.md` §1 |
| **O2** | consistent with the floor | **No whole-only CP asymmetry at this sensitivity**, quoted *with* Dye A's 5σ floor so the null is gauged and not empty |
| **O3** | significant, but Up and Down disagree (K3) or sidebands carry share (K4) | **Detector or background artifact**, reported as such and with equal prominence |
| **O4** | occupancy or pair-pinning gate fires (K5) | **Ungauged / VOID** — neither zero nor a detection, reported as loudly as a detection would be |
| **O5** | Dye A not recovered at the size claimed (K1), or Dye B moves the share (K2) | **The instrument is not gauged here**; no reading from this run means anything, whatever its p-value |
| **O6** | large, well-controlled reading whose decomposition into physical sources we cannot perform | reported as a **detected but unexplained** reading, explicitly listed here so it is not silently upgraded into a mechanism |
| **O7** | the primary mode fails occupancy or PID yields too few events | the campaign's deliverable is the prereg plus inventory, and we say so plainly |

### Kills — each takes down its own claim and nothing beneath it

| | kill | what it kills |
|---|---|---|
| **K1** | Dye A not recovered at 5σ at an `ε` giving a share at or below the measured value | this run's reading, in either direction. The method survives |
| **K2** | Dye B or Dye C moves the share above the floor | the **implementation** — it is not pairwise-blind. The observable's definition survives |
| **K3** | `|share(Up) − share(Down)|` exceeds 3σ of the combined permutation null | the **CP interpretation** of the reading. The reading itself stands as "a charge-correlated structure" |
| **K4** | the sideband share exceeds the floor at 3σ | the **signal-window reading**, until background-subtracted. Other arms survive |
| **K5** | the §6a reachable share range is below 20 % of the measured share | the reading's status as **whole-only**; it becomes a statement about pair marginals |
| **K6** | flat phase space (§7b) reads above the permutation floor | the **geometric null's** cleanliness, and with it any absolute-magnitude statement; the conjugate-difference structure survives |
| **K7** | any §5 plumb line returns a wrong value | the **whole run**, before it starts |

### Explicitly NOT a kill of anything on the published page

Whatever this campaign returns, it does **not** bear on `wild-share`, on `adequacy`, on the
`cp-cap` claim, on the maximal-CP wager, or on any Logos claim. `Core/FlavorBridge.lean` is a
**model** bridge and its own header says so; this measurement is not its confirmation and a null
here is not its refutation. Nothing here is proposed for `Stance.lean`.

---

## 11. WHAT IS NOT CLAIMED, WRITTEN BEFORE THE ANSWER IS KNOWN

1. **No priority claim.** `DALITZ_PRIOR_ART.md` grades this **CONVERGENT-ADJACENT with an
   unswept web**. Model-independent CP searches in three-body phase space are a mature
   programme; the credit paragraph (§4 there) is carried on any output.
2. **No T-odd claim.** `DALITZ_PRIOR_ART.md` §5 proves triple products vanish identically in
   three-body decays of a spinless parent. Our slots are binarised Dalitz coordinates and a
   charge tag, **not momenta**, and the sign triple `x·y·c` has no kinematic T-odd meaning.
3. **No efficiency correction exists and none is invented.** The design's protection against
   charge-symmetric acceptance is an argument (§2.3) that §7c *tests*; a charge-dependent
   acceptance with genuine three-way structure across the plane would fake the signal, and the
   magnet-polarity split (K3) is the only control we have against it. That control's power is
   not known in advance and will be quoted as measured, not assumed.
4. **This is one dataset, one year, one mode, our own selection.** It is not an LHCb measurement
   and must never be described as one.
5. **`b = 2` only for magnitudes.** The finer rungs are diagnostics, declared unquotable here
   (§4) before their values are known.
6. **The KLOE-2 arm, if run, is a control and not a CP measurement.** `η` is self-conjugate;
   what its Dalitz plane carries is a **C** reflection `X → −X`. If and only if the three slots
   can be constructed so that `X → −X` acts as the *global* sign flip of all three bits does
   `share_eq_zero_of_signSymmetric` apply, and that construction is an obligation to be
   discharged in writing before the arm is run — not assumed. Its data are unfolded densities,
   not counts (`DALITZ_DATA.md` §2), so every count-based gate in this document needs an
   explicit restatement there or the arm does not run.

---

## 12. ORDER OF OPERATIONS

1. Commit this document. **Done before any code exists.**
2. Implement the estimator; run the §5 plumb lines. Any failure stops the run (K7).
3. Run the §8 dye tests on permuted data — **before** the real charge labels are used. Record
   the 5σ floor.
4. Fix `X̃`, `Ỹ` from the charge-integrated sample (§4) and write them into the results file.
5. Run §7b (flat phase space) and §7c (efficiency immunity).
6. Unblind: attach the real charge labels, compute the primary reading and the §7a null.
7. Run §6a, then §6b with its expectation paragraph attached.
8. Run the secondaries with the §9 trials factor.
9. Write `DALITZ_RESULTS.md` reporting the fired kills as plainly as the survivals, keeping
   every gate's reading including the ungauged ones.

---

## FILES

| | |
|---|---|
| `DALITZ_PRIOR_ART.md` | convergent-art adjudication — `727e006` |
| `DALITZ_DATA.md` | public-data inventory — `7510576` |
| this document | pre-registration, committed before any measurement |
| `DALITZ_RESULTS.md` | to follow, or an explicit statement that the prereg is the deliverable |

Pre-registered 2026-07-26.
