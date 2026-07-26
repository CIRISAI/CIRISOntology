# PRE-REGISTRATION — the whole-only order-3 excess of the galaxy density field, on real data

Commissioned by Eric conditional on two controls, both of which have now landed and **both of
which fired**. Written and committed **before any real survey data has been downloaded, opened
or looked at**.

**The author of this document has seen mocks only.** Every number quoted below about a real
catalogue — galaxy counts, number densities, effective volumes, redshift ranges, mock suite
sizes — is recalled from the published literature, is marked *[to verify]*, and must be read
off the actual catalogue headers at Stage 0 before any analysis choice depends on it. No
catalogue file has been touched. `lake` has not been run; no Lean file, `Stance.lean` or audit
is involved.

**The deliverable is this document. The measurement does not run until Eric has reviewed it.**

---

## 0. WHAT THIS DOCUMENT IS FOR, AND WHAT IT IS NOT

`Stance.lean` carries `wild-share` as **open**: does any of nature's unengineered processes
carry whole-only pattern — structure that no pair of observers can reconstruct? Gravitational
clustering is the largest wild process with a survey-measurable field, so it is the natural
first decidable instance.

`SKY_FORECAST_RESULTS.md` (mocks only) says such a measurement is worth attempting at
`R = 10–15` Mpc/h and **only** under conditions this document must encode. It also retired the
statistic I originally proposed for the job. This pre-registration is the redesign.

---

## 1. THE TWO CONTROLS, AND WHAT THEY FORCE

Both were commissioned as conditionals. Both fired. The conditional branches are therefore
**both** taken, and the design below is the "worst case" branch of the commission.

### 1.1 binmint FIRED — the median split manufactures `b = 2` excess

`sky_forecast_binmint.py`, 8 realisations, committed before it was run
(`SKY_FORECAST_RESULTS.md` §13). Binning into `b` quantile bins, IPF onto the pair marginals
to get the fine-grained **pairwise-maxent** state `q` (which carries all the field's fine pair
structure and *no* order-3 content), then merging the lower and upper halves — which for
quantile bins **is** the median split — leaves a nonzero `b = 2` excess:

> `E_manuf = 1.01e-03` at `t = 4.29` on gravity, **converged in `b`**
> (`9.6e-4, 1.02e-3, 1.02e-3, 1.01e-3` for `b = 4, 8, 16, 32`). Worst IPF certificate
> `|share_H − share_KL| = 2.0e-11`.

Two honest qualifications, both recorded rather than smoothed: the theorem-pinned control arms
(a Gaussian, and a monotone map of a Gaussian) must read exactly zero and read `max|t| = 2.80`
and `3.36` over six configurations, so gravity's `4.29` sits above a pedestal rather than far
above it; and the effect **costs the mock deliverable only 14 % at `R = 10`** (86–100 % of the
signal survives, `t = 13.7–20.5`) while **removing `R = 25` entirely** (`t_corr = 0.5–0.9`).

**Commission's branch: the `b = 2` sign-triple route is demoted to a secondary/diagnostic arm,
and the primary must be a statistic that survives the LP pair-pinning gate.** §3 is that
redesign.

### 1.2 shotnoise MINTED — the valve opens at survey densities

`sky_forecast_shotnoise.py`, 10 realisations (§12). `Core/Valve.lean` proves a per-cell
*stochastic* channel returns a product state from a product state — never from nothing — but
**can** mint whole-only share on a state carrying pair structure. Poisson sampling is such a
channel; a density field is such a state.

> Paired shift on a field whose true share is **exactly zero**, `R = 10`, rising monotonically
> as density falls: `3.70e-03 → 4.90e-03 → 1.10e-02` for `n̄ = 1e-2, 1e-3, 1e-4`, at
> `t = 23.4, 12.7, 22.0`. **At DESI-like density that is 130 % of the entire mock signal.**

The valve mechanism is isolated: at `R = 25` the correlated base fires at `max|t| = 11.0` while
a **product-state** base is null at `max|t| = 1.4` — minting requires pair structure, exactly
as the theorem says. At `R = 10` both fire, because there the post-sampling *smoothing* — a
cross-cell filter, which no no-creation theorem covers — dominates.

Matched forward-modelling (sampling the floor at the same `n̄`) removes most but not all of it:
the residual is **26 % (equilateral) to 136 % (folded)** of the signal, at `t = 4.5–11.3`.

**Commission's branch: shot noise becomes a forward-modelled floor carrying its measured
amplitude-versus-density curve, subtracted never ignored.** §5.3.

### 1.3 The third channel, already on record

The spatial filter (window, mass assignment, smoothing) manufactures **93 %** of the mock GAP
(§2a), and a filter applied after a pointwise map took an exact zero to a **66 σ** detection in
the pilot. `Core/Creation.lean` covers only *per-cell* maps, so **no no-creation theorem
protects against this**, and none is claimed.

**Three manufacturing channels, each comparable to the signal.** That is the design problem.

---

## 2. WHAT THE MOCK CAMPAIGN LICENSES, AND WHAT IT RETIRED

**Retired, by three independent demonstrations, and it must not reappear as the primary:** the
GAP — gravity minus a pointwise-transform mock at matched `P(k)`. It is 93 % floor rather than
signal; a purely Gaussian field produces a *larger* GAP than gravity does; and it is **blind to
the growth factor** (`d log GAP / d log D = +0.12`, against `+0.82` for gravity's own excess).
A quantity that measured gravitational structure would scale with growth. That one does not.

**Licensed as the target:** `A`, the intrinsic excess over a matched Gaussian — which scales
with growth at `+0.82`, is largest in the **folded/collinear** configuration where the `F₂`
tidal kernel `(2/7)(μ²−1/3)` reaches its `|μ| = 1` maximum, and whose tidal sector reads
`z = +28` unfiltered at 10 Mpc/h separations against a counterpart that is exactly zero by
`share_eq_zero_of_signSymmetric`.

---

## 3. TARGET STATISTIC

### 3.1 Primary — the bias-subtracted order-3 connected information at intermediate `b`

For a triple of smoothed cells at a declared configuration, let `I_C⁽³⁾(b)` be the order-3
connected information of the `b`-level quantile-binned triple: the entropy gap between the
state and the maximum-entropy state carrying its three pair marginals.

    Â(b)  =  I_C⁽³⁾(b)[data]  −  I_C⁽³⁾(b)[Gaussian mock through the IDENTICAL pipeline]

The subtraction is licensed by the pilot: the discretisation bias at `b ≥ 3` is **additive and
orthogonal to the signal**, measured to scale as `γ^2.000` to four significant figures after
subtraction, at every `b` and every configuration (`SKY_PILOT_RESULTS.md` §3). The Gaussian
mock is not analytic — it is a real mock catalogue carrying the same window, mask, `n̄(z)`,
fibre collisions and Poisson sampling (§4, §5).

**Primary configuration: folded/collinear**, sides `(r, 2r, r)` with `r ≈ 1.5R`, at
`R = 10` and `15` Mpc/h. That is where gravity's own excess lives (§2), not where the retired
GAP was largest.

**`b` is bounded from both ends and the bounds are pre-registered.** Below by the parity rule —
`b = 2` is demoted (§1.1); above by **occupancy**, because `kappa-edge` recorded that its
`b ≥ 16` rungs went **VOID** when occupancy collapsed to 8 %, the regime where IPF overstates
and no null controls it. So:

> **`b ∈ {4, 6, 8}`, subject to an occupancy gate: the expected count per cell of the `b³`
> histogram must exceed 100 at the analysis resolution, using the number of INDEPENDENT
> smoothing volumes (`V_eff / (2π)^{3/2}R³`), not the number of galaxies.** Any `b` failing
> that is not reported. *[Estimate to verify at Stage 0: for `V_eff ≈ 4 (Gpc/h)³` at
> `R = 10`, roughly 2.5e5 independent volumes, giving ~490 per cell at `b = 8` and ~3900 at
> `b = 4`. `b = 16` would give ~60 and is expected to fail the gate — which is the
> `kappa-edge` regime and is why it is excluded in advance.]*

Every IPF solve carries the KL certificate `|share_H − share_KL|`, per
`ISING_FIELD_RESULTS.md` §2 and the `ipf-sharek-boundary-drift` lesson; the run is void above
`1e-9`.

### 3.2 The LP pair-pinning gate — the reason the primary is not `b = 2`

`kappa-edge` (`3026a68`) established the failure mode with a **linear program on the marginal
polytope**, needing no surrogate, no null, no IPF and no estimator: over *every* distribution
carrying the measured fine-grained pair marginals, the coarse sign-triple statistic was
confined to a single point — so the published value was the one **forced** by the pair
marginals, not a measurement of three-way structure.

The LP applies to **linear** functionals of the distribution. The sign-triple moment
`τ = Σ σ(s) p(s)` is linear; a KL-based connected information is not. So the gate is run on
the linear functional and its verdict governs the arm:

> **GATE LP.** At the analysis resolution, and using the measured `b' = 2b` pair marginals,
> solve the LP for `min τ` and `max τ` over the marginal polytope. Report the interval width.
> **VOID the arm if the interval half-width is below 5× the statistical error on `τ`** — the
> statistic is then pinned by pair structure and carries no three-way freedom to measure.

**What I expect, and why, stated before running it.** `kappa-edge` identified the mechanism as
**near-determinism of the conditional support, not coupling strength**, and measured that *a
Gaussian triple carrying the same pair correlations is NOT pinned* (interval width 0.797) while
a noise-free logistic map is (width 0.00000). A galaxy field smoothed at 10 Mpc/h is nowhere
near deterministic. **I therefore expect GATE LP to pass comfortably, and I am pre-registering
that expectation so that a narrow interval is a surprise that voids the arm rather than a
detail to be explained afterwards.**

### 3.3 Secondary, clearly scoped — and explicitly *not the wild-share question*

Two secondary arms, reported and never promoted:

* **The `b = 2` sign-triple excess**, as a diagnostic only, carrying its binmint correction
  (§1.1) and its own LP gate. It is retained because it is theorem-protected against pointwise
  distortion (Sklar/monotone invariance, verified bit-for-bit at 0 differing cells of
  56 623 104) and is therefore the cleanest cross-check against readout nonlinearity, which is
  a different failure family from pinning.
* **The GAP — data against a pointwise-transform mock at matched `P(k)` and one-point law.**
  This is the filter-aware sharpening of the Scherrer, Berlind, Mao & McBride (2010) copula
  question, and Qin, Yu & Zhang (2020) already report the copula is non-Gaussian. It is a
  well-posed question and a survey can answer it at high significance.
  **This is not the wild-share question**, in those words, and no outcome of it will be
  reported as bearing on `wild-share`. A Gaussian field passes it, and passes it more strongly
  than gravity does.

---

## 4. DATA CHOICE

### 4.1 The decision, and the criterion that decides it

**Primary: BOSS DR12 combined LSS catalogues (LOWZ + CMASS), NGC and SGC, with the 2048
MultiDark-Patchy mock realisations per cap.** *[all catalogue properties to verify at Stage 0]*

**Confirmation, not primary: DESI DR1** — larger volume and higher density, but a younger
public mock infrastructure.

**The criterion is mock quality, and my own results are why.** Every one of the three
manufacturing channels (§1.3, §1.1, §1.2) contributes at 14–130 % of the signal, and none of
them can be deconvolved — they must be *measured on mocks that carry them*. So the binding
requirement is not survey volume and not number density; it is:

> **the floor must be measurable to better precision than the signal.**

2048 Patchy realisations measure a floor to `1/√2048 ≈ 2.2 %` of its per-realisation scatter.
My mock campaign's systematic residuals are 14–30 % of the signal. **The floor is therefore
measurable roughly an order of magnitude better than it needs to be — that is the license.** A
suite of ~100 realisations would not clear this bar, which is the honest reason DESI DR1 is the
confirmation set rather than the primary.

### 4.2 The density tension, stated because it cuts against this choice

BOSS density is **not** comfortable at the target scales. *[to verify]* CMASS `n̄ ≈ 4e-4
(h/Mpc)³` at peak gives `n̄ V_R ≈ 6` galaxies per smoothing volume at `R = 10` Mpc/h. My
measured shot-noise floor at `n̄V_R = 1.6` was 130 % of signal and at `15.7` was 58 %, so BOSS
sits **between those two points, with a shot-noise floor of order 60–100 % of the signal.**

This does not disqualify the choice — the floor is forward-modelled from mocks that share the
same `n̄(z)`, so a large floor that is *accurately measured* is workable while a small floor
that is *poorly measured* is not — but it is the single biggest reason this measurement could
fail, and it is stated here rather than discovered later. **If the Stage-2 mock closure test
(§5.6) shows the shot-noise floor is not reproduced to 10 %, the primary moves to the densest
available tracer (DESI BGS, `n̄ ~ 1e-3`–`1e-2` at `z < 0.4`) and this document is amended
before unblinding.**

### 4.3 Redshift bins, and the growth lever

*[to verify]* LOWZ `z_eff ≈ 0.32`, CMASS `z_eff ≈ 0.57`, and if eBOSS DR16 LRG is added
`z_eff ≈ 0.70`. For `Ω_m = 0.31` the growth factors are roughly `D = 0.80, 0.70, 0.66`.

**The lever is weak and I am not going to pretend otherwise.** `D(0.32)/D(0.70) ≈ 1.21`, and
with `A ∝ D^{0.82}` (measured, §11 of the forecast) the predicted ratio between the extreme
bins is only **1.17**. To resolve that at 3 σ requires each bin measured to **5.7 %**.

> **Therefore the growth-scaling check is pre-registered as a CONSISTENCY CHECK, not as a
> decisive discriminator, and its power is stated in advance: it can refute a floor-driven
> signal only if per-bin precision reaches ~6 %.** If it does not, the check is reported as
> uninformative rather than as a pass.

---

## 5. THE FULL BATTERY — every gate with its license

Each is a gate on the analysis, run on mocks first, and each names the result that licenses it.

| # | gate | license | fires ⟹ |
|---|---|---|---|
| **G1** | **LP pair-pinning** at analysis resolution (§3.2) | `kappa-edge` `3026a68` | **VOID** the arm |
| **G2** | **binmint** — fine-`b` pair-maxent surrogate merged to the analysis binning; its excess subtracted from every arm | §1.1, `SKY_FORECAST_RESULTS.md` §13 | correction applied; if it exceeds the signal, **VOID** |
| **G3** | **Shot-noise/valve floor**, forward-modelled with its measured amplitude-vs-`n̄` curve | `Core/Valve.lean` + §1.2 | subtracted, never ignored |
| **G4** | **Window/mask/fibre-collision floor FORWARD-modelled, never deconvolved** | pilot's 66 σ result; §1.3 | subtracted, never ignored |
| **G5** | **Sign-symmetric Gaussian mock control** through the identical pipeline — **must read exactly zero** | `share_eq_zero_of_signSymmetric` | nonzero ⟹ **VOID**, it is pipeline error |
| **G6** | **Phase-randomised null** of the data itself | standard; forecast §2 | must floor |
| **G7** | **Tied and railed fraction** reported for every reading | house rule 4; forecast measured `7.1e-08` on mocks | undisclosed ⟹ result not reportable |
| **G8** | **Growth scaling across `z` bins** (§4.3) | forecast F3, `+0.82` | consistency check, power stated |
| **G9** | **IPF certificate** `< 1e-9` on every solve; **occupancy `> 100`** per histogram cell | `ipf-sharek-boundary-drift`; `kappa-edge`'s VOID rungs | fails ⟹ that `b` not reported |
| **G10** | **Mock closure**: the full floor model, built from mocks, must reproduce the mocks' own reading to **10 %** | this document, §5.6 | fails ⟹ **VOID** |

### 5.6 Mock closure, the gate that decides whether any of this is possible

Build the entire floor model — window, mask, `n̄(z)`, fibre collisions, Poisson sampling,
binarization/binning — from one half of the mock suite, then predict the *other* half's reading
and compare. **This is the only gate that tests the floor model as a whole rather than one
channel at a time**, and given that the floor is 100–130 % of the signal, it is the gate this
measurement most plausibly fails. Threshold: the predicted floor must match the held-out mocks'
reading to 10 % of the *signal*, not 10 % of the floor.

### 5.7 Blinding

The data reading is computed **only after** G1–G10 have been run and passed on mocks and on the
data's own phase-randomised null. The gravitational prediction (§7) is fixed from N-body mocks
before the data reading is looked at. No gate threshold may be changed after any data number is
seen; if one must be, the change is recorded as an amendment with the number that prompted it,
per the pilot's Amendment discipline.

---

## 6. PRE-REGISTERED OUTCOMES AND KILLS — separable, each taking down its own claim

### (a) DETECTION — intrinsic tidal excess above all floors

*Criterion:* `Â(b)` positive at `≥ 5 σ` above the combined forward-modelled floor, in the
folded configuration, at `R = 10` and/or `15` Mpc/h, at two or more values of `b` that pass G9,
**and** consistent with the N-body-calibrated gravitational prediction (§7) in amplitude and
configuration shape, **and** not refuted by the growth check where that check has the power to
speak (§4.3).

*What it licenses:* **`wild-share` gets its first YES instance.** The interpretive stake is
already on record and is not re-negotiated here: the non-pointwise (tidal/shift) sector counts
as a YES, existence and not novelty-of-mechanism being the question.

*What it does not license:* any claim about primordial non-Gaussianity; any claim that the
whole-only share is large (the degree-3 direction holds ~1 % of the fine-grained structure, per
`kappa-edge`'s H-BLIND); any promotion in `Stance.lean` without a separate refuter pass and
Eric's review; any claim about the *continuum* share if the analysis rests on a binned reading
(§3.1 measures a binned quantity, and the pilot measured `A(b=2)/A_∞ = 1.11–6.6`).

### (b) EXCESS BEYOND THE GRAVITATIONAL PREDICTION

*Criterion:* (a)'s significance met, but the amplitude or configuration shape is inconsistent
with the N-body prediction at `≥ 5 σ`.

*What it licenses:* **nothing yet.** It is a separate anomaly claim requiring **its own
refuter pass** — mock-suite cross-validation, an independent tracer, and an independent
pipeline. **It is not automatically primordial**, and the document forbids that reading in
advance: an unmodelled systematic in a 100 %-of-signal floor is the far likelier explanation,
and three such systematics are already known to exist.

### (c) NULL ABOVE THE FLOORS

*Criterion:* `Â(b)` consistent with zero after all floors, with the floor uncertainty measured.

*What it licenses:* **an honest bound**, quoted as an upper limit on the whole-only order-3
excess of the galaxy density field at the stated scales and configurations, with the
instrument validated by G5/G6/G10. **`wild-share` stays open.** This is a real and publishable
outcome and is not a failure.

### (d) VOID — the run produces no result at all

Any of: **G5** nonzero (Gaussian control fails ⟹ pipeline error); **G1** showing pair-pinning at
analysis resolution (the statistic is forced by pair structure); **G10** mock closure failing
(the floor model does not describe the mocks, so it cannot describe the data); **G9** failing at
every `b`; or the IPF certificate exceeding `1e-9`.

*What it licenses:* a report of the void with the failing number, and nothing else. Per house
rule 7 the void is reported as plainly as a detection would be.

---

## 7. HONEST LIMITS

1. **My calibration is 2LPT — leading order, not N-body.** The forecast measured one way this
   bites: LPT *damps* small-scale power (`P/P_lin = 0.38` at high `k`) rather than enhancing
   it. **The gravitational prediction in (a) and (b) must come from N-body mocks, and it must
   be the same public suite used for the window and shot-noise model** — that is a closure
   requirement, not a convenience: a floor model and a signal prediction from different suites
   cannot be differenced honestly.
2. **The measured quantity is binned, not continuum.** §3.1 measures `I_C⁽³⁾(b)`. The pilot
   measured that binarised and continuum readings differ by factors of 1.11–6.6. No continuum
   claim is licensed.
3. **Redshift-space distortions: FORWARD-MODELLED.** RSD is a spatial (cross-cell) anisotropic
   map, exactly the family that manufactures share and that no no-creation theorem covers. It
   is in the mocks and is modelled with them; it is never deconvolved. Configurations are
   defined in redshift space and their orientation to the line of sight is a reported label,
   not a marginalised nuisance.
4. **Fibre collisions: FORWARD-MODELLED.** A deterministic, spatially-correlated *deletion* —
   again cross-cell. In the mocks, in the model.
5. **Imaging systematics and completeness weights: MARGINALISED**, with the analysis repeated
   under the published weight variants; a shift exceeding the statistical error between weight
   schemes **voids** the affected bin.
6. **Catalogue-level blunders VOID**: an undisclosed veto mask, a `n̄(z)` mismatch between data
   and mocks beyond the published tolerance, or a mock suite that does not share the data's
   window.
7. **The three manufacturing channels are not independent of each other** and my campaign
   measured them separately. Their joint behaviour is measured for the first time at G10, and
   if they compound rather than add, the closure test is where that shows up.
8. **Statistical power for outcome (a) is comfortable; systematic power is not.** The forecast's
   statistical requirement was `0.11–0.27 (Gpc/h)³` against a `~4 (Gpc/h)³` sample. **Nothing in
   this measurement is limited by statistics. Everything in it is limited by the floor model.**

---

## 8. RESOURCE PLAN — stages, volumes, compute

| stage | what | data volume | compute | gate to pass before proceeding |
|---|---|---|---|---|
| **0** | Catalogue and mock inventory; verify every *[to verify]* number against headers; fix `n̄(z)`, veto masks, weight definitions | ~1 GB (catalogues) | minutes | all recalled numbers replaced by read numbers; **any discrepancy that changes a §3–§4 choice triggers an amendment before proceeding** |
| **1** | Pipeline build: grid assignment (interlaced, as validated), smoothing, quantile binning, `I_C⁽³⁾(b)` estimator, LP solver | — | ~1 day dev | G7, G9 on synthetic input; the forecast's gate suite re-passed |
| **2** | Floor model on mocks: window, `n̄(z)`, fibre collisions, Poisson, binning; **G10 mock closure on a held-out half** | ~100 GB (2048 × 2 caps) *[to verify]* | ~4 h on 32 cores (≈2 min/mock/scale) | **G10 at 10 % of signal. This is the go/no-go.** |
| **3** | Gaussian and phase-randomised controls through the identical pipeline | ~10 GB | ~1 h | **G5 exactly zero**, G6 floors |
| **4** | LP pair-pinning at analysis resolution; binmint surrogate at analysis resolution | — | ~1 h | **G1**, **G2** |
| **5** | N-body gravitational prediction from the same suite | (shared with 2) | ~2 h | prediction fixed and recorded **before** unblinding |
| **6** | **Unblind**: the data reading, per `z` bin, per `b`, per configuration | — | ~1 h | — |
| **7** | Growth check across `z` bins; write-up with the fired kills reported as plainly as the survivals | — | — | — |

**Peak storage ~150 GB; peak compute ~1 core-week, comfortably inside one machine-day on 32
cores.** Stages 0–5 involve **no data reading whatsoever** except catalogue metadata; the data
number is produced once, at Stage 6, after every gate has passed.

**Scope decision Eric is being asked to approve:** the ~150 GB download and ~1 machine-day, and
the choice of BOSS DR12 + Patchy as primary over DESI DR1 (§4.1), with the §4.2 escape hatch to
a denser tracer if G10 fails on density grounds.

---

## 9. WHAT THIS DOCUMENT DOES NOT LICENSE

1. **It does not license running the measurement.** Eric's review is the gate.
2. **It does not license any stance change under any outcome**, including (a). `wild-share`
   stays open until a completed measurement passes a separate refuter pass and Eric's review.
3. **It does not license a primordial-non-Gaussianity reading of any excess** (§6b).
4. **It does not license reporting the GAP as bearing on `wild-share`** (§3.3), in those words.
5. **It does not claim novelty.** The copula programme asked the qualitative question in 2010
   (Scherrer, Berlind, Mao & McBride) and reported a non-Gaussian copula in 2020 (Qin, Yu &
   Zhang); connected information is Schneidman, Still, Berry & Bialek (2003) and Amari (2001);
   2LPT and the `F₂` decomposition are standard. What is new here is the pair-envelope null
   made filter-aware and the three manufacturing channels measured rather than assumed away.
6. **It does not assert that its author has seen the data.** He has not.

---

*Pre-registration ends here. Nothing below this line existed when it was committed, and no
survey datum had been read.*
