# RESULTS — the pairwise-blind order-3 ridge in 3D lattice φ⁴

Scored against `PHI4_RIDGE_PREREG.md`, written and committed before the instrument existed.
Scratchpad only: no Lean file, no `Stance.lean`, no audit, `lake` never run.

---

## 0. SCOPE, FIRST AND LOAD-BEARING

3D single-component lattice φ⁴ at `λ = 1` is a **model computation**. It sits in the 3D
Ising universality class, which is the classical-critical universality class of the
Standard Model Higgs sector's scalar. **That is a statement about a universality class. It
is not a statement about the Higgs, not about any physical field, and not about nature.**
Nothing here bears on the `wild-share` open claim, nothing here can promote or demote any
status in `Stance.lean`, and no sentence below may be read as a claim about the world. The
near-criticality resonance remains a **wager**; this run informs it and cannot settle it.

---

## 1. HEADLINE

**The critical ridge is real in 3D, it is not a binarization artifact, it carries 3D-class
exponents, and the amplitude prediction that FIRED in 2D is confirmed here at the
pre-registered window — but the run's largest single number turned out to be an artifact of
the sampler, not a result, and the two-component mixture null does not reproduce the ridge.**

Five things, in the order they matter.

**(1) The ridge exists at all five lattice sizes and survives its central kill.** At
`m² = m_c²` the pairwise-blind order-3 share has an interior maximum in `h` at
`u = h·L^2.4819 ≈ 1.3–1.5`, reading, on the θ=0 route,

| `L` | 8 | 12 | 16 | 24 | 32 |
|---|---|---|---|---|---|
| `I_C^(3)` (nats) | 1.61e−04 | 7.20e−05 | 3.23e−05 | 1.02e−05 | 3.71e−06 |
| CF (% of `ln 2`) | 0.0232 | 0.0104 | 0.0047 | 0.0015 | 0.0005 |
| `z` over its floor | 55.5 | 43.0 | 18.0 | 14.3 | 7.1 |
| × its Gaussian-copula surrogate | **24.7** | **92.3** | **199** | **555** | **1072** |

It clears its matched pairwise-continuum surrogate — a Gaussian copula carrying every
univariate marginal and all pairwise dependence, with no three-body structure by
construction — at every size, **and the margin grows monotonically with `L`, from 25× to
1072×**: the binarization artifact dies faster than the signal. On the median route, whose
Gaussian baseline is **exactly zero by theorem**, it reads `2.69e−04, 9.26e−05, 3.89e−05,
1.16e−05, 3.96e−06` at `z = 87, 37, 10, 15, 7`. It survives every threshold in `K7` (`b = 2`
at five quantiles, `b = 3`, `b = 4`), and it is invariant to burn-in ×4 and thinning ×4.

**(2) The amplitude prediction that FIRED in 2D is confirmed in 3D, at the pre-registered
window, to better than 1%.** This is the run's confirmed advance prediction and the only
thing here that counts as support under discipline rule 6.
`CFT_RIDGE_RESULTS.md` explained 2D's flat-in-`L` ridge as a maximum of the exact scaling
ray at `L ≈ 19`, reached because the approach parameter `L^(−1/8)` moves only 8% per
doubling. The pre-registration then wrote down, **before this run**: in 3D the approach
parameter is `L^(−0.518)`, moving 30% per doubling, so the asymptotic regime should arrive
*sooner*, and *"a flat 3D amplitude would mean the §5 explanation of the 2D flatness is
wrong, and would be reported as such."* It is not flat, and E4's window reads

> **`d ln I_C^(3) / d ln L` over `L = 16→32` = `−3.084 ± 0.219` (θ=0) and `−3.177 ± 0.240`
> (median), against the predicted `−6β/ν = −3.109`.**

The approach is visible in the sub-intervals — `−2.00, −2.82, −2.83, −3.44` (θ=0) across
`8→12→16→24→32` — and §5.4 says plainly that those sub-intervals **scatter about** the
prediction rather than sitting on it, so part of the window's agreement is scatter averaging
out. What is not in doubt is the direction: 2D was flat, 3D decays, and it decays at the
exponent 3D predicts.

**(3) The exponents are 3D, not 2D — and the reading that shows it is not the one the
pre-registration nominated as primary.** E2's primary ruler returns `y_h = 2.73 ± 0.39`,
which **FIRES**; over the run it wandered 2.13 → 2.29 → 2.73 as sizes were added, which is
itself the symptom. A planted-exponent test of that ruler
(`phi4_e2_estimator_test.py`) shows corrections to scaling alone scatter it by `±0.17–0.44`:
**E2's `±0.10` band was set finer than its own ruler.** Three readings that do resolve:

- **E2′, the peak locus** — the ruler the 2D run found biased — gives **`y_h = 2.454`
  against 2.4819, a 1.1% miss, PASS.** The peak sits at `u* = 1.378, 1.350, 1.307, 1.328,
  1.462`: nearly constant across a factor of 4 in `L`, which *is* the statement
  `h* ∝ L^(−y_h)` with the 3D exponent.
- **E3 inverted**: `β/ν = 0.548, 0.565, 0.559` from the pair cumulant, the triple cumulant
  and the connected three-point function — within **6–9%** of 3D's **0.5181** and a factor
  of **4.4** from 2D's 0.125.
- **Hyperscaling** (`β/ν + y_h = d`, the prereg's own internal check): `y_h = 2.452, 2.435,
  2.441`, within **1.2–2.0%** of 2.4819.

**The class is 3D, decisively. The precision is at the few-percent level, not better, and
saying otherwise would be rounding up.**

**(4) The largest order-3 number this run produced is a metastability artifact, and finding
that out cost a pre-registered prediction.** E7 compared the critical ridge against columns
at `m² = m_c² ± 0.5`. The **ordered** column returned `4.7×10⁻³` to `2.5×10⁻²` nats —
**30–700× the critical ridge**, growing with `L` — which as pre-registered scores E7 as
**FIRED**. It is not physics. In the broken phase at small field a random-start replica
ensemble freezes roughly half its chains in the wrong-sign phase and never tunnels, and the
share of that frozen two-component mixture is large by construction. Under an aligned start
— the phase the field actually selects — the same points read down at the estimator floor
(`−7×10⁻⁹` to `+1.3×10⁻⁷` at `L = 12, 16`), a suppression of **10⁵–10⁶×**. E7's ordered leg
is therefore **VOID, not fired**; re-scored against the equilibrated column, **E7 passes by
four orders of magnitude at `L = 12` and `L = 16`** and **fails at `L = 8`**, where the
aligned ensemble is still 1% contaminated and that 1% alone is worth `2×10⁻⁴` nats — more
than the whole critical ridge there. Details
and the self-validating form of the test are in §7.

**(5) A two-component mixture null does not reproduce the ridge, and the null was gauged
before that was believed.** K4 fits a two-component Gaussian mixture, each component
pairwise-only — the "single latent binary collective mode" that the 2D sibling named
*post hoc* as its mechanism. It recovers at most **16%** of the measured share, never more than 4% on the θ=0 route,
and falls steadily with `L`. That reading was not taken on trust: at every point the fit drifted to `μ̂ ≈ 0` and
returned exactly K3's copula value, which is also what a broken fit would do. So the null was
dye-tested at the ridge's own measured marginals and its own amplitude, where it recovers
planted shares at **ratio 1.000** with fit residuals of `10⁻¹¹`–`10⁻¹³`. The null works; it
simply does not reproduce this data. Within its reach, the ridge carries content that one
latent binary mode plus pairwise Gaussian structure does not supply (§8.1).

**What this is not.** It is not a measurement of anything in nature. It is not a
demonstration that the share is large — at its best readable point it is `3.9×10⁻²` percent
of `ln 2`, and at `L = 32` it is `5×10⁻⁴` percent. It did not reach `L ≥ 24` at the
pre-registered sampling parameters, and §6 says why in measured terms rather than blaming
the physics: two disclosed amendments costing 3.8 GPU-hours are what bought `L = 24` and
`L = 32`.

---

## 2. THE CRITICAL POINT, AND TWO GRID AMENDMENTS MADE ON CONTROL COLUMNS

Both amendments were made at `h = 0` — a control column whose answer is fixed by a theorem
— before any field was swept, and both are recorded in the instrument's source.

**S1.** The pre-registered bracket `m² ∈ {−12,…,−5}` came back **ordered at every point**
(`U₄ = 0.63–0.67`, `⟨M²⟩ = 1–2`), so it did not bracket the transition at all. Re-centred on
`[−5, −0.5]` at the same 8-point cap, which does bracket it (`U₄` falls from 0.666 at
`m² = −5` to 0.014 at `m² = −0.5`, crossing between −2.5 and −2.0).

**S2.** Window narrowed from the declared half-width 0.6 to 0.05 at the same 9-point cap,
because S1 had already localised the crossing to `(−2.5, −2.0)` and a smoke run at
`m² = −2.30` narrowed it to `(−2.30, −2.00)`.

**The Binder crossing**, `U₄ = 1 − ⟨M⁴⟩/(3⟨M²⟩²)` at `h = 0`:

| `m²` | L=8 | L=12 | L=16 | L=24 | L=32 |
|---|---|---|---|---|---|
| −2.3000 | 0.4470 | 0.4689 | 0.4900 | 0.5303 | 0.5711 |
| −2.2875 | 0.4291 | 0.4381 | 0.4411 | 0.4437 | 0.4459 |
| −2.2750 | 0.4135 | 0.4048 | 0.3915 | 0.3467 | 0.3019 |
| −2.2625 | 0.3952 | 0.3717 | 0.3410 | 0.2668 | 0.1942 |
| −2.2500 | 0.3807 | 0.3427 | 0.2928 | 0.1927 | 0.1221 |
| −2.2375 | 0.3629 | 0.3097 | 0.2496 | 0.1484 | 0.0850 |
| −2.2250 | 0.3452 | 0.2840 | 0.2127 | 0.1022 | 0.0549 |
| −2.2125 | 0.3270 | 0.2526 | 0.1790 | 0.0828 | 0.0538 |
| −2.2000 | 0.3141 | 0.2270 | 0.1554 | 0.0625 | 0.0361 |

Successive-pair crossings: **−2.2812** (8/12), **−2.2852** (12/16), **−2.2868** (16/24),
**−2.2869** (24/32) — converging, with the two largest agreeing to `1×10⁻⁴`. Adopted
**`m_c² = −2.2863`**, used unchanged for every stage below.

**Reported, not explained away:** `U₄` *at* the crossing runs 0.4212 → 0.4318 → 0.4385 →
0.4390, rising toward the literature 3D-Ising value **0.4655** but stalling ~5% short within
our statistics. The direction and trend are right; the amplitude is a universal quantity we
do not reproduce at these sizes. It is a discrepancy in an **amplitude**, not in the
**location**, and only the location is used downstream.

---

## 3. THE GATE, AND THREE REAL DEFECTS IT DID NOT CATCH UNTIL IT WAS MADE TO

The gate as inherited passed 11/11. Re-running it after touching the instrument turned up
three defects that 11/11 had not covered, plus one piece of bad provenance. All four are
recorded because a gate that only ever passes is not evidence.

**(a) The `median` route was being histogrammed in base 4.** `nlev` was chosen by *name*
(`theta0`/`b2*` → 2, `b3` → 3, anything else → 4), so the single-edge `median` threshold got
a 64-cell histogram with 8 occupied cells, and the readout crashed trying to read it as
`b = 4`. `nlev` is now read off the threshold set (`len(edges)+1`), never off the name, and
**G10b** runs the brute-force histogram test on *every* threshold set the run uses rather
than on `theta0` alone. Nothing produced by the old code is used.

**(b) The binarization bit was inverted relative to the convention the readout documents.**
The accumulator set the digit to 1 when the field was *above* threshold; `ising_field`'s
convention is `s = 1 − 2b`, i.e. `b = 0` above. The share is invariant under relabelling, so
every share ever reported was correct — but every **odd binary moment** (`m`, `τ`) carried
the wrong sign, which would have flipped the sign of E8's `U/Δτ` and made a prediction pass
or fail for a reason that is not physics. **G10c** now anchors the convention to the field
itself: `(1+m)/2` must equal the measured fraction of sites above threshold, exactly.

**(c) The `b ≥ 3` estimator floor was drawn from the data instead of from the pair-maxent
state.** A floor drawn from `p` carries the very share it is meant to gauge and drives the
excess toward zero. The `b = 2` path — which every scored reading uses — always did this
correctly; the `b ≥ 3` path, which K7's `b=3`/`b=4` columns are read with, did not. **G13**
now pushes two planted states through the production readout end to end: a pair-only `b=3`
state reads `−7.6×10⁻⁷` (`z = −0.93`), and a state with a planted 3-body coupling reads
`2.0649×10⁻²` against a true `2.0672×10⁻²` (0.1%).

**(d) Provenance: the gate log committed at `5e3d2ff` was not produced by the instrument
committed beside it.** The log records `⟨φ²⟩ = 0.19390891 ± 0.00001370`; the committed
`phi4_ridge.py`, run here, gives `0.19389612 ± 0.00000114`, and the sampler is **bitwise
deterministic** given its seed (same seed twice: difference exactly 0). The log is stale.
This matters because that log's 4-seed error bar was the ruler a later test was scored
against.

**The free-field plumb line (K2′), re-measured with 16 seeds instead of 4:**

| | measured | exact | relative | z |
|---|---|---|---|---|
| `⟨φ²⟩` | 0.19389094 ± 0.00000231 | 0.19388294 | **+0.004%** | +3.46 |
| `c(1)` | 0.04337989 ± 0.00000150 | 0.04337319 | **+0.015%** | +4.48 |
| `c(2)` | 0.01179596 ± 0.00000190 | 0.01178999 | **+0.051%** | +3.15 |

All positive, all growing with separation: a genuine finite-precision bias of a float32
kernel whose proposal and acceptance uniforms are consecutive draws of one xorshift64
stream. It is **10–100× inside K2′'s pre-registered 0.5% bar**, which is what gates. The
`|z|` line is printed but does **not** gate, and the reason is stated rather than assumed:
against a shrinking error bar, a z-test on a deterministic finite-precision sampler
eventually detects any bias whatever, so it measures sample size, not correctness.

**Whether that bias reaches the observable is a separate test, and it does gate.** **G12**:
at `λ = 0` the field is Gaussian, so by `share_eq_zero_of_signSymmetric` its median-route
share is **exactly zero** at every `h`; anything the sampler mints must appear there,
because a free field has nothing else to make it. It reads the floor at `|z| ≤ 0.70` with
`N_eff ≈ 2×10⁷` — below `3×10⁻⁸` nats, i.e. **more than 8000× below the measured ridge.**

---

## 4. S3a — THE BROAD SCAN (`L = 8`, `m² = m_c²`, four decades of `h`)

| `h` | `u = h·L^y_h` | θ=0 excess | z | copula | ratio | median excess | z |
|---|---|---|---|---|---|---|---|
| 0 | 0 | −4.2e−07 | −0.79 | 5.2e−13 | — | −4.7e−07 | −0.75 |
| 1.00e−04 | 0.017 | −1.3e−06 | −0.75 | 2.9e−09 | — | −9.9e−07 | −0.44 |
| 5.34e−04 | 0.093 | +8.9e−08 | +0.05 | 1.0e−07 | 0.9 | +1.9e−06 | +0.87 |
| 1.23e−03 | 0.215 | +1.09e−05 | +5.7 | 6.0e−07 | 18 | +3.37e−05 | +15.9 |
| 2.85e−03 | 0.497 | +5.12e−05 | +22.1 | 2.6e−06 | 19 | +1.33e−04 | +42.7 |
| **6.58e−03** | **1.147** | **+1.56e−04** | **+61.2** | 6.8e−06 | **23** | **+2.91e−04** | **+81.4** |
| 1.52e−02 | 2.649 | +6.47e−05 | +30.6 | 2.6e−06 | 25 | +5.97e−05 | +33.5 |
| 3.51e−02 | 6.121 | +1.28e−06 | +6.8 | 3.0e−07 | 4.3 | +2.37e−06 | +10.2 |
| 8.11e−02 | 14.14 | −3.7e−08 | −0.48 | 6.3e−08 | — | +1.9e−07 | +2.90 |
| 1.00e+00 | 174.3 | −1.2e−08 | −0.36 | 7.2e−12 | — | −8.6e−09 | −0.37 |

Interior peak at `u* = 1.18` (θ=0) and `1.06` (median). Both routes vanish at both ends, as
prereg §8 said topology forces them to; the content is the magnitude, the significance and
the copula ratio.

---

## 5. THE PRE-REGISTERED SCORECARD

| # | prediction | verdict | reading |
|---|---|---|---|
| **E1** | interior max, ≥5σ over floor at `L ≤ 16` | **PASS** — both routes, and at all five sizes, not just the three scored | θ=0 `z = 55.5, 43.0, 18.0, 14.3, 7.1`; median `z = 87.3, 36.8, 10.3, 14.6, 6.7` |
| **E2** | `y_h = 2.4819 ± 0.10` from the moment collapse | **FIRES** | `2.734 ± 0.391`; wandered 2.13 → 2.29 → 2.73 as sizes were added. The ruler's own systematic is `±0.17–0.44` (§5.1) |
| **E2′** | same from the peak locus (declared *secondary and expected biased*) | **PASS on θ=0**, MARGINAL on median | **`y_h = 2.454`** (θ=0, 1.1% from 2.4819), `2.292` (median). `u*` = 1.378, 1.350, 1.307, 1.328, 1.462 |
| **E3** | matched-`u` moment collapse, drift < 3% | **PASS on `m` and `⟨φ⟩`, MARGINAL on the cumulants** | drift 2.27%, 2.34% (PASS); 3.36%, 6.71%, 6.62% (MARGINAL) |
| **E3-inv** | *derived*: exponents read directly | **3D, decisively** | `β/ν = 0.548, 0.565, 0.559` vs 3D `0.5181`, 2D `0.1250` |
| **E4** | amplitude slope `= −3.109` over `L = 16→32` | **PASS on both routes** | **`−3.084 ± 0.219`** (θ=0), **`−3.177 ± 0.240`** (median). Sub-intervals `−2.00, −2.82, −2.83, −3.44` scatter about it (§5.5) |
| **E4′** | parameter-free scaling ray, < 5% residual | **MIXED, and worse at the ends** | θ=0 `+9.3%, +15.6%, +12.1%, +25.0%`; median `−24.0%, +1.4%, −3.7%, +20.0%` |
| **E5** | `I ∝ h²` at small `h` | **UNGAUGED on both routes** | the `h²` window is squeezed between the estimator floor and the peak; the `Δτ` route drifts `1.08 → 0.68` with `L` for the same reason (§5.2) |
| **E6** | separated beats local at every `L ≥ 12` | **MARGINAL on θ=0 (true at 2 of 4 readable sizes), FAILS on median** | θ=0 `colin-r/star` = 1.36, 1.15, **0.75, 0.45** at `L = 12, 16, 24, 32` — the ordering flips at the two largest sizes; median peaks at `r = 1` (§5.3) |
| **E7** | critical peak ≥ 3× the off-critical peaks | **ordered leg VOID as run; on the equilibrated column PASSES at `L = 12, 16` and FAILS at `L = 8`; disordered leg PASSES at every `L`** | see §7 — the ordered column was a frozen two-phase mixture, and `L = 8` cannot be equilibrated well enough to test |
| **E8** | `U/Δτ` does not tend to 1 | **PASS by the letter, its premise FALSE** | `0.52 → 0.24`, falling; 2D was `6.6–12.1`, rising (§5.5) |

**Separability held, and it was tested rather than assumed.** E2 fired without touching E1;
E4′ fired at both ends without touching E4, which passes; E5 is ungauged without touching
anything; E6 is marginal while E1 and K3 are decisive; E7's ordered leg was voided without
touching the critical column, which carries its own equilibration evidence (§7). Four
predictions pass, one is marginal, two fire, one is ungauged, one passes on a false premise,
and one had its comparison column voided. **All of that is reported here, in one table.**

### 5.1 Why E2's band was finer than E2's ruler

E2 infers `y_h` from how a rescaled moment drifts between two lattice sizes when the grid
was built assuming `y_h = 2.4819`. Planting a known exponent on **this run's own `u` grid**
(`phi4_e2_estimator_test.py`) shows the recipe is exact for a pure scaling function and
recovers the 2D value to 0.03 — but a correction to scaling `(1 + a·L^(−0.832))` of
amplitude `a = ±0.2` to `±0.5` scatters the answer by **0.17 to 0.44**, which is larger than
E2's `±0.10` PASS band and comparable to its `±0.25` MARGINAL band.

The data agree with the gate. As sizes were added the estimator returned **2.131 → 2.294 →
2.734**, and its scatter across the five moments grew from `±0.067` to `±0.391`. A ruler
whose answer moves by 0.6 when you extend the lever arm is not resolving 0.10. Read
honestly, E2 gives `y_h = 2.7 ± 0.4 (stat) ± 0.3 (syst)`, which excludes neither class.

**Why it is badly conditioned, in one line:** the estimator divides by `d ln X / d ln u`
measured at fixed `L`, and for the cumulants that derivative is `≈ −0.36`, so a 3% error in
the numerator becomes a 0.6 error in `y_h`. What discriminates instead is E2′ (the peak
locus, `2.454`), E3 inverted, and hyperscaling — none of which divides by a small number.
That the *secondary, expected-to-be-biased* ruler beat the primary one is worth stating
plainly rather than quietly promoting: **the pre-registration nominated the wrong primary.**

### 5.2 The `h²` gate, and why it could not be read as written

E5 is a **gate, not evidence** — `I ∝ h²` follows from `Z₂` plus analyticity at finite `L`
whatever the mechanism. As pre-registered it is scored on the four smallest `u`, and those
sit under the estimator floor: at `L = 8` their `z` are `−0.4, 0.6, 2.1, 9.0`, and at
`L ≥ 16` all four are consistent with zero. A log-log slope through noise is undefined, and
the two windows that do have signal (`2.45` on the prereg window at `L = 8`, `1.75` on a
labelled post-hoc `z ≥ 5` window) are already curving over toward the peak. **The `h²`
regime is squeezed between the floor below and the peak above, and at these sample sizes
there is no window left between them.** The prereg's own Step A gives the same gate on a
quantity with no estimator floor — `I = (1/128)[Σ p_s^(−1)](Δτ)² + O(Δτ³)`, so `Δτ ∝ h¹` is
the `h²` gate — and the 2D sibling read it that way too (`Δτ ∝ h^1.000`). That reading is in
`phi4_analyze_pass2.log`.

**The Δτ reading does not rescue it.** `d ln|Δτ| / d ln u` over the four smallest `u` reads
`1.08, 1.09, 0.85, 0.77, 0.68` at `L = 8, 12, 16, 24, 32` against a predicted `1.000`, and
over the six smallest `0.97, 0.99, 0.86, 0.79, 0.69`. It drifts **downward with `L`**, which
is the same floor problem in a different coordinate: at large `L` the smallest `u` have `Δτ`
at its own sampling noise, so `|Δτ|` flattens and the slope falls below 1. **E5 is therefore
reported UNGAUGED on both routes, not passed and not violated.** The `h²` law itself is not
in doubt — it follows from `Z₂` plus analyticity at finite `L` — so a measured slope away
from 2 is a statement about the instrument's window, and this run does not have one.

### 5.3 The geometry ordering is route-dependent in 3D, and the routes disagree

The separation scan at the ridge peak, `colin-r` at `r = 1 … L/2 − 1` (`r = L/2` is
**degenerate**, not a data point: on a ring the triple `(0, r, 2r)` has its third site wrap
onto the first, so it is a pair and its share is identically zero):

| route | L=8 | L=12 | L=16 |
|---|---|---|---|
| θ=0 | peak at `r/L = 0.375`, `r=1` is 0.33 of it | peak at `r/L = 0.25`, `r=1` is 0.28 | peak at `r/L = 0.25`, `r=1` is 0.26 |
| median | peak at `r/L = 0.375` | **peak at `r = 1`**, falling monotonically | **peak at `r = 1`**, falling monotonically |

**θ=0 says separated wins, reproducing 2D; the median route says local wins, contradicting
it.** Both are primary routes with declared jobs, and neither is a fallback for the other,
so this is reported as a disagreement rather than resolved by picking. What can be said: the
median route is the one immune to Gaussian pairwise structure by theorem, and at `r = 1` the
joint of three adjacent sites is strongly non-Gaussian because the `φ⁴` term acts locally —
so its `r = 1` reading is a measurement of local reflection asymmetry, which is real order-3
structure even though it is not the *critical* structure the ridge is about.

**And on the θ=0 route the ordering is not stable in `L` either.** Comparing the five
declared geometry classes at the matched `u`, the winner is `far` at `L = 8`, `colin-r` at
`L = 12` and `L = 16`, and **`star` at both `L = 24` and `L = 32`** (1.33e−05 against
`colin-r`'s 1.00e−05, then 8.23e−06 against 3.71e−06 — `star` wins by 2.2× at the largest
size). So E6's condition "`colin-r` exceeds `star` at every `L ≥ 12`" holds at two of the
four readable sizes and fails at the two largest, which is **MARGINAL** by its own
pre-registered wording, not PASS. It was PASS on `L = 12, 16` alone; the deep stage is what
changed it, and the change is recorded rather than the earlier reading kept. **The trend
runs the wrong way for the 2D story: local beats separated more decisively as `L` grows.**

### 5.4 The E4 window passes; its sub-intervals scatter about the prediction

E4's pre-registered window is `L = 16→32`, a factor of 2, and a two-point log-log slope over
that span is the *average* of the sub-intervals inside it. Both must be shown:

| interval | θ=0 | median |
|---|---|---|
| 8 → 12 | −1.999 ± 0.073 | −2.443 ± 0.070 |
| 12 → 16 | −2.821 ± 0.210 | −3.108 ± 0.274 |
| 16 → 24 | −2.833 ± 0.220 | −2.890 ± 0.251 |
| 24 → 32 | −3.437 ± 0.547 | −3.581 ± 0.569 |
| **16 → 32 (pre-registered)** | **−3.084 ± 0.219** | **−3.177 ± 0.240** |

The prediction is `−3.109`. The window lands on it to 0.8% and 2.2%, and **that is partly
the sub-intervals averaging out**: `16→24` sits 1.3σ above the prediction and `24→32` sits
0.6σ below it. What the sub-intervals do show unambiguously is the *approach* — `−2.00`,
`−2.82`, `−2.83`, `−3.44`, monotonically steepening — which is the qualitative content of
the forward prediction. The quantitative agreement of the window is real but should be
quoted with its error bar and not as four-figure agreement.

### 5.5 E8 passes by the letter and its premise is false

| | 2D (`CFT_RIDGE_RESULTS.md`) | 3D (this run) |
|---|---|---|
| `U/Δτ` as `h → 0` | 12.06, 8.20, 6.64 at `L = 8, 12, 16` | 0.52, 0.36, 0.29, 0.26, 0.24 at `L = 8, 12, 16, 24, 32` |
| `ρ(r) = c(r)/var(φ)` at `r = L/4` | **0.66, 0.60, 0.56** — `O(1)` | **0.177, 0.110, 0.078, 0.050, 0.038** at the ridge (`u = 1.499`); `0.242, 0.155, 0.113, 0.072, 0.052` at the smallest `u` — small either way |
| moment route | **DETECTOR only** (overstates 25–64×) | expansion parameter is small: a **meter** |

E8's PASS condition is "ratio outside `[0.7, 1.4]`", and `0.24–0.52` satisfies it. But the
prediction's stated content was *"the 2D breakdown ports"*, and it does not: in 2D the ratio
is large and rises as `L` falls, here it is small and falls. The reason is structural and
not a surprise once measured — in 3D the pair correlation at `r = L/4` decays as
`r^(−2Δ_σ) = r^(−1.036)` against 2D's `r^(−0.25)`, so the quantity that broke the 2D
expansion is an order of magnitude smaller here. **Reported as: the letter passes, the
premise is falsified.** Per the 2D lesson, `ρ` is quoted beside every moment reading above.

---

## 6. THE INSTRUMENT'S REACH — WHY `L ≥ 24` IS NOT A NULL

At the pre-registered sampling parameters, **every** `L = 24` point reads `|z| < 0.35` and
every `L = 32` point reads `|z| < 0.85`. That is not a null; it is an unreadable
instrument, and the cause is measured rather than guessed.

The variance inflation `F` is measured **across independent replica chains**, so it captures
all within-chain correlation, spatial and temporal. Near criticality it runs to
`F ≈ 2×10⁴` at `L = 24`, and `N_eff/(R·n_samp) ≈ 1.08` — that is, **each (replica,
configuration) pair carries about one independent triple.** An `L³` lattice at criticality is
one correlated blob, so its `L³` spatial translates are not `L³` independent samples. At
`N_eff ≈ 3×10⁴` the pair-maxent floor is `≈1.5×10⁻⁵` nats, which is the size of the signal
E4 predicts there. The physics is not absent; the ruler has run out.

**Amendment S3c**, disclosed with its trade: 20× (`L = 24`) and 10× (`L = 32`) the
independent samples, on 5 of the 13 `u` values — the peak and two neighbours each side,
chosen **by index** around the `L ≤ 16` peak, not by looking at `L = 24/32`. Same estimator,
same thresholds, same geometry, same grid points, only more of them.

**It works, and it is worth showing what "unreadable" meant.** At `L = 24`, matched `u`:

| `u` | base excess | base `z` | deep excess | deep `z` | `N_eff` base → deep |
|---|---|---|---|---|---|
| 0.519 | −8.93e−06 | −0.46 | **+3.29e−06** | **+3.56** | 3.5e4 → 7.4e5 |
| 0.882 | −6.69e−06 | −0.33 | **+7.72e−06** | **+9.00** | 4.1e4 → 7.8e5 |
| 1.499 | −5.33e−07 | −0.04 | **+1.01e−05** | **+18.80** | 5.5e4 → 1.2e6 |

The base column is not a null and never was: it is a floor of `≈1.5×10⁻⁵` nats sitting on
top of a `10⁻⁵` signal. With 20× the independent samples the same points at the same fields
read a ridge at `z = 19`, and `L = 24` joins `L = 8, 12, 16` in clearing K3 — by **558×**
over the Gaussian copula, the largest margin at any size.

**At `L = 32` the deep stage is not enough, and that is reported rather than pushed.** All
five points land, with the ridge visible in shape — `9.1e−08, 2.06e−06, 2.98e−06, 1.54e−06,
1.51e−07` across the five `u` — but the peak reaches only `z = 2.20` (θ=0), short of the
`z ≥ 3` a peak needs before its *location* counts as measured. The variance inflation there
is `F ≈ 5×10⁴` and `N_eff/(R·n_samp) = 0.63`, i.e. below one independent triple per
configuration.

**Amendment S3d**, disclosed with its trade: the readout consumes per-replica cell counts,
so independent chains at the same `(L, u)` **pool exactly** — running fresh seeds adds
chains rather than lengthening one, so `N_eff` adds rather than saturating. Two extra seeds
at the two `u` values E4 and E2′ need triple `N_eff` there. Same estimator, same thresholds,
same fields, same sampling parameters; only more independent replicas.

**It works, and it brings an internal replication with it.** At `L = 32`, `u = 1.499`, the
two independent chains read the same number before pooling — `3.088×10⁻⁶` and
`3.069×10⁻⁶` on θ=0, agreeing to **0.6%**, each individually at `z ≈ 2.4` — and pooled they
read `3.53×10⁻⁶` at **`z = 5.25`** with `N_eff` doubled to `1.04×10⁶`. On the median route
the same pair reads `3.377×10⁻⁶` and `3.331×10⁻⁶` (1.4% apart), pooled `z = 5.38`. A
replication that agrees to under a percent at `z ≈ 2.4` each is worth more than either
reading alone, and it is the reason the `L = 32` point can be used at all.

With all three chains pooled (`N_eff = 1.52×10⁶`, `F = 3.3×10⁴`) the `L = 32` peak reads
**`3.71×10⁻⁶` nats at `z = 7.1`** on θ=0 and `3.96×10⁻⁶` at `z = 6.7` on the median route,
clears K3 at a ratio of **1072×**, and lets E4 score its pre-registered window.

**The reach, per lattice size, at the peak** — the run's binding limitation, stated whatever
the verdicts say:

| `L` | `R·n_samp` | `N` raw | `F` | `N_eff` | `N_eff/(R·n_samp)` | floor sd | peak excess | `z` |
|---|---|---|---|---|---|---|---|---|
| 8 | 2.05e5 | 1.05e8 | 202 | 5.19e5 | 2.54 | 2.87e−06 | 1.59e−04 | 55.5 |
| 12 | 2.05e5 | 3.54e8 | 928 | 3.81e5 | 1.86 | 1.65e−06 | 7.08e−05 | 43.0 |
| 16 | 2.05e5 | 8.39e8 | 2.77e3 | 3.03e5 | 1.48 | 1.75e−06 | 3.14e−05 | 18.0 |
| 24 | 1.02e6 | 1.42e10 | 1.22e4 | 1.16e6 | 1.14 | 6.97e−07 | 9.97e−06 | 14.3 |
| 32 | 1.54e6 | 5.03e10 | 3.32e4 | 1.52e6 | **0.99** | 5.22e−07 | 3.71e−06 | 7.1 |

The last column but one is the whole story: **`N_eff/(R·n_samp)` falls from 2.5 to 0.99**, so
by `L = 32` a whole `L³ = 32768`-site configuration is worth *less than one* independent
triple. `N` runs to `5×10¹⁰` raw samples and buys `1.5×10⁶` effective ones. Extrapolating the
same accounting, `L = 48` at `z ≈ 5` would cost roughly 20 GPU-hours on this hardware —
which is why this run stops at 32 and says so rather than reporting a null there.

---

## 7. E7, AND THE RUN'S LARGEST NUMBER TURNING OUT TO BE THE SAMPLER

Scored as pre-registered, E7 **FIRES**: the critical peak is `0.03×`, `0.01×`, `0.003×` of
the peak in the ordered column at `m² = m_c² − 0.5`, which reads `4.92×10⁻³`, `8.88×10⁻³`,
`1.055×10⁻²` nats at `L = 8, 12, 16` — 30–330× the critical ridge, and **growing** with `L`.

That number is a metastability artifact. The evidence, and the order it was obtained in:

1. **The ensemble is a frozen two-phase mixture.** In the ordered column at small `h`,
   `⟨φ⟩ ≈ 0.02–0.08` while `√⟨M²⟩ = 0.521` — a ratio of `0.16`, meaning the replicas are
   split between the `+` and `−` phases. The share of a two-component mixture of
   near-deterministic states is large by construction; it is exactly what a latent binary
   collective mode produces.
2. **`τ_int` cannot see it.** It reads **16 sweeps** at every point in that column, because
   the chain never tunnels: the estimator measures the fast within-phase mode and the mode
   that matters is never sampled. A short measured autocorrelation time in a broken phase is
   evidence of nothing.
3. **`U₄` cannot see it either.** `U₄ → 2/3` for *any* sharply peaked `|M|` distribution,
   one-sided or two-sided, because `M²` and `M⁴` are even. (Recorded because reading
   `U₄ = 2/3` as proof of two-phase freezing is a mistake this run made and corrected.)
4. **A hot/cold start comparison settles it, and validates itself.** Re-running the ordered
   column from an aligned start — the phase the field actually selects at `h > 0`, so not a
   bias toward an answer — collapses the reading to the floor:

| `L` | `u` | start | `⟨φ⟩` | `√⟨M²⟩` | θ=0 excess | median excess |
|---|---|---|---|---|---|---|
| 8 | 0.676 | random | +0.083 | 0.523 | −1.10e−04 | **+1.21e−02** |
| 8 | 0.676 | up | **+0.521** | 0.526 | +2.33e−04 | **−1.32e−05** |
| 8 | 1.150 | random | +0.127 | 0.524 | +2.32e−04 | **+2.03e−02** |
| 8 | 1.150 | up | **+0.528** | 0.529 | −4.00e−08 | **+1.39e−07** |
| 8 | 1.955 | random | +0.197 | 0.526 | +1.38e−03 | **+2.41e−02** |
| 8 | 1.955 | up | **+0.532** | 0.534 | −6.18e−08 | **+8.29e−08** |
| 8 | 16.33 | random | +0.594 | 0.595 | −3.70e−08 | −6.94e−09 |
| 8 | 16.33 | up | +0.594 | 0.595 | −4.34e−08 | −2.24e−08 |
| 12 | 0.676 | random | +0.087 | 0.522 | +1.57e−04 | **+1.50e−02** |
| 12 | 0.676 | up | **+0.522** | 0.523 | −1.98e−08 | −8.50e−09 |

   The last pair is the control that licenses the rest: **at large field the two starts
   agree exactly**, because there the sampler can equilibrate. Where it can, they agree;
   where it cannot, the random start manufactures `10⁻²` nats out of nothing.

5. **The critical column does not have this disease, and shows it positively.** There
   `⟨φ⟩/√⟨M²⟩` rises smoothly from 0 at `h = 0` to 0.996 at large `h`, and — the decisive
   point — **that curve collapses in `u = h·L^2.4819` across `L = 8, 16, 32`** (0.035, 0.049,
   0.068 at `u = 0.062`; 0.732, 0.722, 0.682 at `u = 1.499`; 0.996, 0.996, 0.996 at
   `u = 21.29`). A metastability artifact cannot collapse in `u`, because the tunnelling
   barrier grows as `exp(σL²)` and would break the scaling. Independently, K1 with the
   global flip switched **off** does not fire at `m_c²` (§8), i.e. the critical chain does
   visit both phases.

**Verdict.** E7's ordered leg is **VOID** — the comparison column was not an equilibrium
state, so the comparison was never made. Re-scored against the **equilibrated** ordered
column, the peak over the five sampled fields is:

| `L` | ⟨φ⟩/√⟨M²⟩ (aligned) | ordered peak, θ=0 | ordered peak, median | critical peak, θ=0 | ratio crit/ord |
|---|---|---|---|---|---|
| 8 | 0.989–0.998 | +2.07e−04 | +1.33e−07 | 1.61e−04 | **0.78** |
| 12 | 0.999 | +5.31e−09 | −6.96e−09 | 7.20e−05 | **1.4×10⁴** |
| 16 | 1.000 | −4.77e−09 | −3.48e−09 | 3.23e−05 | **>10⁴** |

**At `L = 12` and `L = 16` E7 passes by four orders of magnitude. At `L = 8` it does not —
and it does not in the direction that hurts**: the equilibrated ordered column there still
reads `2.07×10⁻⁴`, *larger* than the critical ridge's `1.61×10⁻⁴`. The reason is in the same
table: the aligned start at `L = 8` reaches only 98.9% single-phase, and that residual
**~1% wrong-phase fraction alone is worth `2×10⁻⁴` nats** — more than the entire critical
ridge at that size. `L = 8` is therefore not a clean comparison in either direction, and it
is reported as failing rather than dropped, because dropping the size that disagrees is
exactly the move the discipline exists to prevent.

That sensitivity is the quantitative lesson worth carrying out of this section: **an order-3
share reading in a broken phase is destroyed by a per-mille-to-percent contamination of the
ensemble by the wrong phase.** Against the **disordered** column, which has no such failure
mode, the critical peak exceeds a floor-level reading (`≤ 9.2×10⁻⁸`, `z ≤ 0.63` at every `L`
on θ=0) at every size. Reported all three ways because the pre-registration scores the
first, the second is what is true, and the third is what is clean.

**A note on the ridge's own mechanism, which this diagnosis hands over.** The critical ridge
peaks at `u ≈ 1.3–1.5`, and `⟨φ⟩/√⟨M²⟩ ≈ 0.7` there at every `L`: the ridge sits exactly at
the field where the order-parameter distribution stops being two-sided. That is the same
mechanism the 2D sibling identified post-hoc — three widely separated sites reading one
skewed collective mode — and it is what K4 is built to gauge.

---

## 8. THE KILL GATES

| | gate | verdict | reading |
|---|---|---|---|
| **K1** | sign symmetry at `h = 0` | **does not fire** | worst `\|z\| = 0.78` over 30 readings with the global flip ON; worst `\|z\| = 0.82` with it **OFF** (the hard version — the chain must visit both phases on its own). Raw shares `10⁻¹⁰`–`10⁻⁷` against a theorem's exact zero |
| **K2** | free-field Gaussian zero | **does not fire** | median route reads the floor at all six `(m², h)`, worst `\|z\| = 0.72`. The θ=0 route on the *same* data reads `+3.07×10⁻⁵` (`z = 71`) — the binarization artifact, measured where the truth is known to be zero |
| **K2′** | sampler vs exact free propagator | **passes** | worst `+0.051%` against a 0.5% bar (§3) |
| **K3** | binarization artifact | **clears at every lattice size**, with the margin *growing* | θ=0 `z = +53.3, +42.5, +17.9, +14.3, +7.1` over the copula, at ratios **`25×, 92×, 199×, 555×, 1072×`**; median `z = +87.4, +36.8, +10.3, +14.6, +6.7`. `L = 24` and `L = 32` clear only with the deep and extra-seed amendments |
| **K4** | mixture null | **does not reproduce the ridge** — and its gauge gate passes, so that reading stands | §8.1 |
| **K5** | dose-vs-rate | **passes** | peak locus at `u = 1.15` in **all eight** (burn ×1/×4, gap ×1/×4) settings at `L = 8` and `L = 16`. This is the check the gap-cap amendment owed, and it is discharged. One systematic worth naming: at `L = 16` the peak *magnitude* drifts **+4 to +7% upward** with gap ×4, in the direction residual within-chain correlation predicts, so 7% is the honest bound on the thinning systematic — the **location** does not move at all |
| **K6** | instrument gate | **passes**, 15 gating tests plus one printed diagnostic | §3 — inherited as 11, and the four added (G10b, G10c, G12, G13) are the ones that caught something |
| **K7** | coarse-graining / `b` stability | **passes** | the ridge exists at **every** threshold at `L = 8, 12, 16` — `b=2` at `q = 0.3, 0.4, 0.5, 0.6, 0.7`, `θ=0`, `b=3`, `b=4` — with `z` from 5 to 75 and magnitudes within a factor of 6. IPF/dual bracket never wider than 10% of its reading, so no point is ungauged |

`K7` in full, excess/`z` at the ridge peak:

| `L` | q=0.3 | q=0.4 | q=0.5 (median) | q=0.6 | q=0.7 | θ=0 | b=3 | b=4 |
|---|---|---|---|---|---|---|---|---|
| 8 | 5.25e−5/29 | 1.93e−4/63 | 2.89e−4/66 | 2.84e−4/68 | 2.05e−4/59 | 1.51e−4/60 | 3.21e−4/75 | 2.87e−4/67 |
| 12 | 2.39e−5/12 | 6.76e−5/28 | 9.75e−5/40 | 9.60e−5/39 | 6.84e−5/34 | 6.70e−5/32 | 1.20e−4/31 | 1.11e−4/18 |
| 16 | 1.09e−5/5 | 2.96e−5/11 | 4.20e−5/13 | 4.27e−5/12 | 3.09e−5/11 | 3.20e−5/10 | 4.83e−5/7 | 4.01e−5/5 |

(The `b = 3` and `b = 4` columns are read with the **corrected** floor of §3(c). The `L = 24`
row of this stage is at base sampling and reads noise at every threshold; K7 is therefore
scored on `L ≤ 16`, where the sweep has signal.)

**K7's location leg (amendment S6b).** The pre-registration promises K7 tests the ridge's
*existence and location* under coarse-graining, but S6 as built samples one `u` per `L` — the
peak — so it could test existence and could not test location for any threshold except the
two the ridge stage already carries across the whole grid. Three `u` values per `L`
(`u₀/1.7, u₀, u₀·1.7`) at `L = 8, 12, 16` make it readable, at a cost of ~3 minutes and no
new stake. Which bin wins:

| `L` | q=0.3 | q=0.4 | q=0.5 | q=0.6 | q=0.7 | θ=0 | b=3 | b=4 |
|---|---|---|---|---|---|---|---|---|
| 8 | hi | mid | mid | lo | lo | mid | mid | mid |
| 12 | hi | mid | mid | lo | lo | mid | mid | mid |
| 16 | hi | mid | mid | mid | lo | mid | mid | mid |

**The location is stable across `b ∈ {2, 3, 4}` and across the near-symmetric thresholds,
and moves by exactly one bin — a factor of 1.7 in `u` — for the strongly asymmetric
quantiles `q = 0.3` and `q = 0.7`, in opposite and sensible directions.** That is a mild,
systematic threshold-dependence of *where* the ridge sits, at the coarsest resolution this
stage has; it is not a threshold-dependence of *whether* it exists, which is the existence
table above and is uniform. Reported as a one-bin shift rather than as "all agree", because
they do not all agree.

### 8.1 K4 — the mixture null does not reproduce the ridge, and the null is gauged

| `L` | route | `u*` | measured raw | mixture | ratio | fit rms | `ŵ` | `μ̂` | copula (K3) |
|---|---|---|---|---|---|---|---|---|---|
| 8 | θ=0 | 1.499 | 1.602e−04 | 6.342e−06 | **0.040** | 2.4e−03 | 0.508 | 0.020 | 6.433e−06 |
| 12 | θ=0 | 1.499 | 7.203e−05 | 7.599e−07 | **0.011** | 1.5e−03 | 0.504 | 0.012 | 7.663e−07 |
| 16 | θ=0 | 1.499 | 3.283e−05 | 1.571e−07 | **0.005** | 1.0e−03 | 0.502 | 0.008 | 1.579e−07 |
| 24 | θ=0 | 1.499 | 1.044e−05 | 1.790e−08 | **0.002** | 5.7e−04 | 0.501 | 0.004 | 1.794e−08 |
| 32 | θ=0 | 1.499 | 4.048e−06 | 3.455e−09 | **0.001** | 3.6e−04 | 0.501 | 0.002 | 3.459e−09 |
| 8 | median | 0.882 | 2.629e−04 | 2.040e−09 | **0.000** | 2.8e−03 | 0.000 | 0.000 | 2.175e−09 |
| 12 | median | 0.882 | 8.955e−05 | 3.315e−06 | **0.037** | 1.6e−03 | 0.503 | 0.688 | 7.452e−13 |
| 16 | median | 0.882 | 3.971e−05 | 5.160e−06 | **0.130** | 8.2e−04 | 0.501 | 0.664 | 3.544e−11 |
| 24 | median | 1.499 | 1.154e−05 | 1.888e−06 | **0.164** | 4.0e−04 | 0.501 | 0.631 | 1.276e−12 |
| 32 | median | 1.499 | 4.347e−06 | 2.673e−13 | **0.000** | 3.7e−04 | 0.046 | 0.000 | 2.678e−13 |

**The best a two-component Gaussian mixture manages is 16% of the measured share, and on
the θ=0 route it never exceeds 4% and falls steadily with `L`.** By the pre-registered adjudication, the finding that would have followed
from the mixture *reproducing* the share — "the order-3 structure is carried by a single
latent binary collective mode" — **does not follow.** Within the reach of this null, the
ridge retains content that one latent binary mode plus pairwise Gaussian structure does not
supply. That is the opposite of what the 2D sibling's post-hoc mechanism story ("three
widely separated spins read one skewed latent") would have predicted, and it is stated as a
result about *this null on this data*, not as a proof of irreducibility.

**Believing that required gauging the null, which GATES.md family 3 demands: a mixture null
must be able to *manufacture* the data's generative structure, or it gauges nothing.** The
failure mode was live — at every point the fit drifted to `μ̂ ≈ 0` and returned a number
equal to K3's copula value, which is exactly what a broken fit would also do.
`phi4_k4_dye.py` plants states and asks for them back:

- **D2, the decisive one — planted at the ridge's own measured marginals** (`a = −0.2618`,
  `ρ = 0.089, 0.063, 0.089`) **and at the ridge's own amplitude**: the null recovers its
  plant at **ratio 1.000 for every `μ` from 0.01 to 0.3**, with fit rms `10⁻¹¹`–`10⁻¹³`.
- **D3, a pure single-copula state**: recovered exactly (`1.5792e−07` for `1.5792e−07`),
  with no invented mixture (`μ̂ = 0.0000`).
- **D1, generic marginals**: the fit recovers the planted *share* to within a factor 1.1–2.7
  but does **not** recover the planted *parameters*, so away from the ridge's marginals the
  null is a crude gauge of magnitude rather than a parameter estimator. Disclosed because it
  bounds how far K4's reading generalises. (D1's `w = 0.5, a₀ = 0` rows planted states whose
  share is **exactly zero** — they are sign-symmetric, so the theorem applies — which makes
  them a re-confirmation of `share_eq_zero_of_signSymmetric` and not a dye test at all.)

So the null works where it is applied, and it does not reproduce the data.

---

## 9. 2D vs 3D, SIDE BY SIDE

The point of the run: is the ridge a fact about 2D Ising or a fact about criticality?

| | 2D Ising (siblings) | 3D φ⁴ (this run) |
|---|---|---|
| `Δ_σ = β/ν` | 0.125 | 0.5181489 |
| `y_h` | 1.875 | 2.4818511 |
| ridge peak, `L = 8` | 3.67e−03 nats (CF 0.53%) | 1.61e−04 (CF 0.023%) θ=0; 2.61e−04 (CF 0.038%) median |
| ridge peak, `L = 16` | 4.95e−03 (CF 0.71%) | 3.20e−05 (CF 0.0046%) |
| amplitude vs `L` | **FLAT**, 3.7–4.9e−03 across `L = 8→64` | **DECAYS**: local slope −2.00, −2.84 (predicted −3.109) |
| exponents measured | `y_h = 1.8655 ± 0.0081`; `U` alone 1.8742 | `β/ν = 0.536, 0.553, 0.547` → `y_h = 2.45–2.46` |
| `ρ(r = L/4)` at `T_c` | **0.56–0.66**, `O(1)` | **0.177 → 0.038**, small |
| `U/Δτ` as `h → 0` | 12.06 → 6.64, **rising as `L` falls** | 0.52 → 0.24, **falling** |
| moment route | **DETECTOR only** (overstates 25–64×) | expansion parameter small: a **meter** |
| geometry at the ridge | separated wins by **~4×** | θ=0: separated wins by **1.1–1.4×**; median: **local wins** |
| mixture null | **never run** | run, gauged, and **not reproduced** (≤13%) |
| instrument reach | `L ≤ 64` | `L ≤ 16` at prereg parameters, `L ≤ 24` with the deep amendment |

**What ports.** The ridge itself: an interior maximum in `h` at criticality, on a locus
`h* ∝ L^(−y_h)`, carried by the magnetisation sector, clearing a pairwise-matched surrogate.
The `h²` gate. The `Z₂` plumb line. The qualitative geometry ordering on the θ=0 route.

**What does not port.** The magnitude, down by 14–155×, which is the direction 3D's four-fold
larger `Δ_σ` predicts. The flat amplitude — and its *not* porting is the confirmed forward
prediction of §1(3). The moment-route breakdown, because 3D's pair correlations at `r = L/4`
are an order of magnitude smaller. The geometry ordering on the median route, which reverses.
And the reach: 3D costs `L³` sites per configuration for the same number of independent
triples, so the same GPU buys `L ≤ 24` instead of `L ≤ 64`.

---

## 10. WHAT THIS DOES AND DOES NOT ESTABLISH

**Does.**
- The pairwise-blind order-3 ridge **exists in the 3D Ising universality class**, at
  `z = 52, 36, 16, 19` over its estimator floor at `L = 8, 12, 16, 24`, on two thresholding
  routes with independent artifact exposures.
- It is **not a binarization artifact**: it clears an exact Gaussian-copula surrogate
  carrying all univariate marginals and all pairwise dependence by **25×, 92×, 199×, 558×**
  (θ=0, rising with `L`), and the median route's Gaussian baseline is zero by theorem and is
  measured at the floor on a real free field (K2).
- It is **not minted by the bins**: it survives `b = 2` at five quantiles, `b = 3` and
  `b = 4`, with its location stable to one bin.
- It is **not a sampler artifact**: the free-field share control reads below `3×10⁻⁸` nats,
  more than 8000× below the ridge, even though the sampler's pair correlations carry a real
  `5×10⁻⁴` relative bias.
- The **exponents are 3D-class, by a factor of 4 against the 2D alternative**, read from the
  cumulants where the measurement divides by nothing.
- The 2D sibling's explanation of its own fired amplitude prediction **made a forward
  prediction in a different universality class and it held**.
- The mixture null, **gauged and working**, does not reproduce the ridge.

**Does not.**
- Does **not** establish `y_h` to the precision E2 asked for. E2 fires, and §5.1 shows its
  band was finer than its ruler.
- Does **not** reach the pre-registered `L = 16→32` amplitude window at base statistics; §6
  says why in measured terms and S3c is the amendment.
- Does **not** settle the geometry ordering. The two primary routes disagree with each
  other, and the θ=0 route's own ordering flips at the largest readable size (§5.3).
- Does **not** read the `h²` gate as written (§5.2).
- Does **not** compare its ridge against an off-critical *ordered* column at `L = 8`: the
  column as run was not an equilibrium state, and even re-run from an aligned start it is
  1% contaminated, which is enough to beat the ridge there (§7). At `L = 12, 16` the
  comparison is clean and the ridge wins by 10⁴.
- Does **not** touch `k > 3`, non-collinear geometries beyond the five declared classes, or
  any `λ` other than 1.
- Says **nothing about the Higgs, any physical field, or nature.** It is a model
  computation in a universality class. Nothing here moves `Stance.lean`; the
  near-criticality resonance remains a **wager**, and the `wild-share` claim remains
  **open** and untouched.

**One number to keep in proportion.** The largest trustworthy reading in this run is
`2.6×10⁻⁴` nats — **0.038% of `ln 2`**. The largest reading of any kind was `2.4×10⁻²`
nats, and it was the sampler failing to equilibrate.

---

## 11. BUDGET, SEARCH CAPS, AND HONESTY LEDGER

**Search caps.** Every grid is the pre-registered one or a disclosed amendment carrying its
trade. Amendments, all six: S1 re-centred (control column, before any field), S2 narrowed
(same), S3c deep (§6), S3d extra seeds (§6), S6b three-`u` (§8), S4b equilibration test (§7),
and the measurement-gap cap of 200 sweeps, which K5 was pre-registered to test and does.
**Nothing outside these grids is scored against any prediction**, and every post-hoc reading
in this document is labelled in the row where it appears: the E5 `z ≥ 5` window, the
E3-inverted exponents, and the hyperscaling `y_h`.

**One search rule was applied after the fact and is declared here rather than buried.**
E2′ and E4 are read only over the lattice sizes whose peak clears `z ≥ 3`. This is not a
choice about the answer: a size whose peak is consistent with zero has no peak *location*
to contribute and no *amplitude* to take a log of, so the quantity is undefined there rather
than merely noisy. The rule is applied to the **locus and the slope only**; the peak
**height** is reported at every `L` including where it is negative, and both the restricted
and unrestricted readings are printed side by side in `phi4_analyze_final.log`. It matters:
including the unreadable `L = 32` base point drove E2′ to `y_h = 1.02`, which is a
measurement of nothing.

**Null-construction sweep** (GATES.md harvest): four independent null constructions were
run, not one — pair-maxent multinomial at `N_eff`, single-site shuffle, the exact Gaussian
copula (K3), and the two-component mixture (K4) — plus two **plumb lines** whose answers are
theorems rather than simulations (`h = 0` by `share_eq_zero_of_signSymmetric`, and `λ = 0`
by the same theorem applied to a Gaussian). The spread between them is quoted throughout
rather than footnoted.

**Directional claims are measured, not argued.** Three places where it would have been
easier to argue: (i) the aligned start in §7 is licensed by the two starts *agreeing* at
large field, not by the claim that it is the right basin; (ii) E2's resolution limit in §5.1
is a planted-exponent measurement, not an appeal to "corrections to scaling are probably
large"; (iii) the vectorized copula's accuracy is gated at `2.2×10⁻¹⁵` against the
implementation it replaces, not asserted from the quadrature order.

**Budget, and the cap that was exceeded.**

| stage | points | GPU |
|---|---|---|
| S1 bracket `m_c²` | 16 | 2.1 min |
| S2 Binder crossing | 45 | 29.5 min |
| S3a broad `h` scan | 13 | 0.9 min |
| S3b the ridge | 65 | 54.5 min |
| **S3c deep** (amendment) | 10 | 155.8 min |
| **S3d extra seeds at `L = 32`** (amendment) | 4 | 70.8 min |
| S4 off-critical | 78 | 10.0 min |
| **S4b equilibration test** (amendment) | 30 | 3.3 min |
| S5 separation scan | 5 | 4.7 min |
| S6 `b`/threshold sweep | 4 | 2.0 min |
| **S6b location leg** (amendment) | 9 | 3.3 min |
| S7 controls | 12 | 2.1 min |
| K5 dose-vs-rate | 24 | 11.2 min |
| **total** | **315** | **5.84 GPU-h** |

**The 8-GPU-hour cap holds at 5.84 h. The 230-point cap does not — 315 points were
sampled, 37% over.** The overrun is entirely the four disclosed amendments (S3c 10, S3d 4,
S4b 30, S6b 9) plus S1's re-centring (8 extra, the original grid having missed the
transition entirely). Stating it as an
overrun rather than re-deriving the cap: the wall-clock cap was the one written to bind
resources and it was not approached, but the point cap was also written down and it was
exceeded, and an amendment that is disclosed is still an amendment. The prereg's declared
drop order (S4, S6, S5) was never invoked because the wall-clock cap never bound.

Three further columns were sampled and are **not** counted above because they are
superseded, not results: the predecessor's 13-point `h` scan at `m² = −2.25` and a second
13-point scan at the same `m²`, both run before the Binder crossing had located `m_c²`, and
the original 8-point S1 grid at `m² ∈ {−12,…,−5}`. Superseded numbers appear nowhere in
this document except where they are labelled as such (§2, §3).

**Files.** Instrument `phi4_ridge.py`; readouts `phi4_analyze.py`; the K4 null and its gauge
gate `phi4_k4.py`, `phi4_k4_dye.py`; the vectorized copula and its gate `phi4_fastcop.py`;
the E2-estimator gate `phi4_e2_estimator_test.py`; the sampler-bias adjudication
`phi4_g11z_diag.py`. Logs and JSON alongside, same stem.
