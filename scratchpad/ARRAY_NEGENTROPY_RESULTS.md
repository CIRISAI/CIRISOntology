# RESULTS — the moment-native whole-only instrument on CIRISArray

> **NAMING CORRECTION, made before anything else because the brief and this experiment's own
> filenames get it wrong.** This instrument is **not negentropy**, and the "negentropy route"
> label is false. Negentropy is `½‖u‖²` — the distance to the Gaussian, which is the maxent
> given the **covariance**. The whole-only share is the distance to the **pair envelope**,
> which constrains full pairwise **marginals**, a far larger family. The two differ by exactly
> the projection `P_{W^⊥}`, and that projection is the whole instrument. The sibling
> convergent-art check (commit `e601aec`, CORRECTION 1) shows the identity is not merely loose
> but wrong: on an exact lognormal, whose true share is **exactly zero**, Jones–Sibson
> negentropy reads **9.93 nats**. **Gate G4 of this run is precisely that discriminator, and
> it passes: the lognormal reproduces the Gaussian reading to `0.0`, bitwise.** The instrument
> is right; the name was not. Read "negentropy" nowhere below — the quantity is the
> pairwise-blind projection of the Edgeworth expansion.

Pre-registration frozen and committed at **`9251b5b`** *before* `array_negentropy.py` existed
(`scratchpad/ARRAY_NEGENTROPY_PREREG.md`). Substrate: the ACTUAL CIRISArray GPU kernel
(`/home/emoore/CIRISArray/src/runtime.py`, `Ossicle.KERNEL_CODE`) on the RTX 4090 Laptop GPU,
driven at `iterations = 1`, 512 ossicles × 64 cells = **32 768 structurally independent
replicas** per frame. 3 072 sweep readings + 4 transition scans + 64 cliff readings.
Scratchpad only; no Lean file, `Stance.lean` or the audit was touched, and `lake` was never
run.

**Scope, first and load-bearing.** CIRISArray is **our own designed chaotic hardware**. It is
not nature. Nothing here bears on `wild-share`, on `adequacy`, or on any claim about the
world. A clean null was an acceptable outcome and was not rescued.

---

## VERDICT

**The array carries genuine, boundary-stable, whole-only order-3 structure, and it is
measurable from third moments alone — no bin, no threshold, no entropy estimate, no IPF.**
The certified headline: the temporal triple `(b_t, b_{t+1}, b_{t+2})` at κ = 0.05 reads

> **ŝ₃ = 2.203 × 10⁻² nats (clip) and 2.181 × 10⁻² nats (fold) — agreeing to 1.0 % — which
> is 3.15 % of the machine-checked cap `ln 2`**, at z = −218 against its own error bar and
> z = −448 against the stricter analytic Gaussian null, with τ_fixed = 1.00, rail fraction
> 3.4 × 10⁻⁴, and the clamp demonstrably active (binding rate 3.5 × 10⁻⁵).

All four floors are clean everywhere: replica-shuffle max |z| = 2.69, circular-shift max
|z| = 2.65 over 512 controls (**0** exceeding 5), and at every cliff point the
Gaussian-copula floor reads |z| ≤ 0.6 and the cross-run floor |z| ≤ 1.4. **K2 never fires.**

Four findings beyond the headline, each with its own verdict:

1. **The ridge shape partly replicates, and the two axes behave differently.** The **noise**
   axis reproduces the ECA interior optimum on a continuous chaotic substrate — a clean
   interior maximum at σ = 0.03 at every κ ≤ 0.14. The **coupling** axis splits: the
   *spatial* and *causal* readings peak **at** the measured synchronization transition, as
   the Ising map predicts, while the *temporal* reading has its **deep minimum** there.
2. **My own P6 prediction failed, and the Ising geometry result transferred.** I predicted
   the temporal argmax would stay at Δ = 1 everywhere. At κ = 0.16 — exactly the transition —
   it moves to **Δ = 6**, with the separated readings 13× above the local one.
3. **A material correction to `HABIT_DYNAMICS_RESULTS.md`.** Its "hard finite memory of 2
   kernel iterations, and no tail whatsoever" is a **binarization artifact of the tail**. On
   the *same frames*, median binarization reads exactly zero from Δ = 3 outward while the
   continuous instrument resolves boundary-stable structure at Δ = 3, 4, 6 and 8. The cliff
   itself — three orders of magnitude between Δ = 2 and Δ = 3 — survives. The lifespan does
   not: it is **8, not 2**.
4. **The clip arm self-disqualifies above κ = 0.05.** The shipped clamp pins 2.7 % of the
   state at κ = 0.08 and 65 % at κ = 0.45. Over most of the map the boundary discriminator is
   therefore **unavailable, not failed** — and that is a fact about the device, not about the
   instrument.

**Two cautions that outlive this run, both aimed at our own new instrument.** (i) The degree-3
moment route reads **1 400× below** the binarized route at κ = 0.16, and the degree-4 extension
that would have adjudicated it **is not a valid estimate on this substrate** — it returns 0.75
nats where the proved cap is `ln 2` = 0.693. **K6 is UNRESOLVED, not fired.** (ii) **The
brief's central premise is refuted, measured on this substrate (§9).** Binarization was framed
as "the artifact family that has burned this programme three times today", to be removed by
going moment-native. The opposite is true for the artifact family that actually matters here:
under a one-sided readout clip the **median split is exactly invariant (ratio 1.000 at every
level, both boundaries)** while **this moment route inflates ×2.0 at a 10 % tie block**. Being
moment-native is the exposure, not the protection. The headline survives because it sits at a
rail fraction of 3.4 × 10⁻⁴ — 30× inside the rail threshold frozen before the run — but the
premise does not.

---

## 1. GATES — seven pass; three pre-registered criteria failed first and each was adjudicated

| gate | result |
|---|---|
| **G0** bridge algebra: closed form (B) vs a basis-free Gram–Schmidt projection of `W^⊥ ∩ P₃`, 12 random `(C, ζ)` | **PASS** — max relative error **3.0 × 10⁻¹⁴** |
| **G1** exact per-channel monotone invariance (`exp`, `x³`, `sinh`, affine, negation) | **PASS** — all five reproduce the reading **BITWISE (0.0)**, sign flipping only under negation |
| **G2** known-truth recovery on the skewed-latent triple | **PASS** — `d log ŝ / d log γ = 1.9761` (2.00 ± 0.05 required); bridge accuracy budget ≤ 5.3 % over γ = 0.1…0.4 |
| **G3** Gaussian-copula null floors | **PASS** — |z| < 5 on 100 % at ρ = 0, 0.5, 0.85; empirical/analytic sd for `w` = 1.073 / 0.977 / 0.961 |
| **G4** lognormal is the same null | **PASS** — identical to the Gaussian to **0.0** |
| **G5** kernel fidelity vs the SHIPPED `Ossicle` kernel, 50 iterations | **PASS** — **bit-identical**, max diff 0.0 |
| **G6** cross-instrument, on real array data | **PASS** — binarized `shareK` at κ = 0.05, σ = 1e-3, Δ = 1 reads **5.104e-2 / 5.073e-2** against `HABIT_DYNAMICS_RESULTS.md`'s **5.076e-2**: 0.6 % and 0.1 % |
| **G7** degree-4 machinery | **PASS** — `dim(W^⊥ ∩ P₄) = 4`; orthogonality to every function of ≤ 2 coordinates 1.8 × 10⁻¹⁶ |

### The three that failed first, and why none was fixed by moving a threshold

**G1 failed at 6 × 10⁻⁸, and the cause is the number format, not the estimator.** In float32
the transforms themselves collapse distinct values into **ties** — `exp` takes 32 762 distinct
inputs to 32 746 distinct outputs — and a tie is precisely where a rank map stops being
injective. In float64 every transform reproduces the reading bitwise. The float32 magnitude is
reported rather than hidden: it is the instrument's precision floor, **5.9 × 10⁻⁹ nats**.

**G3's criterion was written without saying which statistic.** Applied to `w`, the whole-only
coordinate that the bridge and every reported z actually use, it holds at every correlation
tested (ratios 1.073 / 0.977 / 0.961). Applied to `κ̂₁₁₁` it fails increasingly with ρ (ratios
1.073 / 0.674 / 0.220), because rank-Gaussianization conditions on the marginal order
statistics and `κ̂₁₁₁ ≈ x³` is dominated by exactly the marginal fluctuation that ranks pin
exactly. **For `κ̂₁₁₁` the analytic formula is a conservative upper bound; for `w` it is the
right null.** Every quoted reading therefore carries **two** z values — the empirical
across-frame bar and the stricter analytic one — and must clear both.

**G2's "within 3 error bars" is a sampling bar**, and at 5.4 × 10⁸ samples the sampling error
drops below the expansion's own truncation error, so it stops being the right test. The
departure was **attributed, not excused**: an ungaussianized control recovers the analytic
value to < 1 % at the same amplitude where the rank route runs 5 % high, so what is being seen
is the higher-order difference between two leading-order estimates of one invariant quantity.
That difference **is** the bridge's accuracy budget and is reported as such: ≤ 5.3 % for
γ ≤ 0.4, visibly breaking by γ = 1.6 (ratio 1.13).

### A bug the gates did not catch, and the check that did

`eigh` fixes eigenvector **signs** arbitrarily. A per-frame `W^⊥` basis therefore flips sign
between frames, and averaging the coordinates cancels at random — the degree-3 basis route
returned a mean of 0.0064 where the exact closed form gives −0.2089. It was caught by
comparing the two routes term by term: **the magnitudes agreed to 6 × 10⁻¹⁵ and the signs did
not.** The fix is one basis built from the pooled covariance, validated by requiring it to
reproduce the exact per-frame closed form at D = 3 — which it does to 0.2 %. Nothing in the
headline used the broken path (the headline is the closed form), but the D = 4 numbers in the
first cliff log did, and they are superseded by §8.

---

## 2. WHAT THE INSTRUMENT KILLS, MEASURED

The bridge, derived in the prereg and machine-checked in G0:

    I_C⁽³⁾ = ½ [ Σ_abc (C⁻¹)_{1a}(C⁻¹)_{2b}(C⁻¹)_{3c} ζ_abc ]² / perm(C⁻¹) + O(ζ³)

**The constant is ½**, and for `C = I` it collapses to `½ κ₁₁₁²`. Structurally absent, not
merely checked clean: entropy-estimator bias (no entropy is estimated), IPF drift (no IPF —
`ISING_FIELD_RESULTS.md` §2 recorded IPF reporting 9.8e-6 where the truth was 1.2e-10), tied
fractions and median splits (no threshold), and bin-count dependence.

**The clamp is not killed, and the moment route is more exposed to it** — which is why every
reading was taken under both boundaries and the rail fraction reported like a tied fraction.
§9 measures exactly how much more exposed, and the answer is worse than the prereg assumed.

**Prior art, credited and not claimed.** The pointwise-transform theorem that licenses
rank-Gaussianization is standard copula theory (Sklar 1959), and it was stated for
cosmological fields by Scherrer, Berlind, Mao & McBride (ApJL 708:L9, 2010), who measured the
2-point copula of the evolved dark-matter field and explicitly considered the hypothesis that
the full n-point copula is Gaussian — which is, in another vocabulary, "the whole-only share
is exactly zero at every order". Qin, Yu & Zhang (2020) report the copula is non-Gaussian.
Also credited: Jones & Sibson (1987) for the multivariate Edgeworth expansion whose
*projection* this is; Carron (2011) for lognormal moment-indeterminacy; McCullagh (1987) for
tensor Hermites; Schneidman, Still, Berry & Bialek (2003) and Amari (2001) for connected
information. The credit list is the sibling's (`e601aec`), adopted here rather than
re-derived. **Assume convergence.**

### The single sharpest demonstration that a moment is not a share

Two operating points of the same reading, same boundary, same noise:

| | `κ̂₁₁₁` (the raw third cross-moment) | whole-only share `ŝ₃` |
|---|---|---|
| κ = 0.16 | **+0.291** | 6.0 × 10⁻⁵ |
| κ = 0.30 | **+0.112** | 1.77 × 10⁻² |

**The raw third cross-moment is 2.6× smaller where the whole-only share is 294× larger.** The
`C⁻¹` contraction is what removes the part of the third moment that the pair marginals already
account for, and on real hardware that part is nearly all of it at κ = 0.16. This is
`SPIKE_SURVEY.md`'s thesis — a large three-point correlation is not order-3 structure — shown
inside a single quantity's own decomposition rather than across two different measures.

---

## 3. FLOORS AND RAILS

**Floors (K2 never fires).**

| control | n | mean z | sd | max abs z | exceeding 5 |
|---|---|---|---|---|---|
| replica-shuffle (`FARP`) | 256 | +0.059 | 0.912 | 2.69 | **0** |
| circular-shift (`SHIFT`) | 256 | −0.026 | 0.996 | 2.65 | **0** |
| Gaussian-copula (cliff points) | 8 | — | — | 0.59 | **0** |
| cross-run, independent seeds (`XRUN`) | 8 | — | — | 1.32 | **0** |

τ_fixed (no truncation-at-first-negative rule, per `HABIT_DYNAMICS` §C): median **1.000**,
4.5 % of readings above 2, max 54.4. Every quoted reading's error bar is inflated by its own
τ; the headline has τ = 1.00.

**Rails — the clamp diagnostic (fraction of state exactly on `0.001f` / `0.999f`).**

| κ | 0.00 | 0.02 | 0.05 | 0.08 | 0.12 | 0.16 | 0.30 | 0.45 | 0.60 |
|---|---|---|---|---|---|---|---|---|---|
| **clip** (σ = 1e-3) | 0 | 0 | 0.0003 | **0.027** | **0.077** | **0.121** | **0.286** | **0.654** | **0.619** |
| **fold** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**Two things must be said and not conflated.** (i) The pre-set 0.01 rail threshold
**disqualifies the clip arm from κ = 0.08 upward** — earlier and harder than P8 predicted
(it predicted κ ≥ 0.20). Above κ = 0.05 the boundary discriminator is therefore
**unavailable, not failed**. (ii) The fold arm reads rail = 0 **by construction** — a
reflecting fold maps into the interior — so a zero rail fraction is **not** a certificate that
fold is clamp-free. At κ = 0.16 the fold clamp still *binds* on 10.3 % of updates. Rail
fraction measures pinning; the clamp-binding rate measures exposure; they are different
numbers and both are reported.

---

## 4. THE RIDGE

### Tier A — boundary-certified (both arms rail-clean, both z bars cleared)

105 readings qualify. The top of the list, by the conservative (smaller-arm) value:

| reading | κ | σ | ŝ clip | ŝ fold | ratio | CF vs ln 2 | z_fold | z_cons |
|---|---|---|---|---|---|---|---|---|
| T3(Δ=1) | 0.02 | 0.03 | 1.064e-1 | 5.710e-2 | **1.86** | 8.24 % | −257 | −561 |
| T3(Δ=1) | 0.05 | 0.01 | 6.013e-2 | 4.249e-2 | 1.42 | 6.13 % | −304 | −636 |
| T3(Δ=1) | 0.05 | 0.003 | 2.572e-2 | 2.433e-2 | 1.06 | 3.51 % | −249 | −472 |
| **T3(Δ=1)** | **0.05** | **0.001** | **2.203e-2** | **2.181e-2** | **1.01** | **3.15 %** | **−221** | **−446** |
| T3(Δ=1) | 0.05 | 0 | 2.183e-2 | 2.172e-2 | 1.00 | 3.13 % | −218 | −444 |
| S3 (spatial a—b—c) | 0.05 | 0.001 | 2.896e-5 | 2.790e-5 | 1.04 | 0.0040 % | −22.6 | −21.4 |

**The boundary agreement degrades monotonically as the clamp gets busier** — 1.00 at σ ≤ 1e-3,
1.06 at 3e-3, 1.42 at 1e-2, 1.86 at 3e-2 — so the largest tier-A value is also the least
trustworthy one, and it is quoted with that stated rather than ranked first and left alone.
**The reading to quote is κ = 0.05, σ ≤ 3e-3: ŝ₃ ≈ 2.2 × 10⁻² nats, 3.15 % of `ln 2`, two
boundaries agreeing to 1 %.**

At κ = 0 and κ = 0.02 the clamp binds **exactly zero times**, so clip and fold are the same
function on the data that occurred: their agreement is TRIVIAL and carries no robustness
information — but those readings also **cannot be clamp artifacts at all**, which is the
stronger fact.

### Tier B — fold-only, where clip is rail-disqualified

766 fold readings clear both z bars but carry **no boundary-stability certificate**: T3(Δ=1)
at κ = 0.05, σ = 0.03 (4.40e-2), at κ = 0.08 (2.16e-2), and a second family at κ = 0.30
(1.77e-2, CF 2.55 %) where the disqualified clip arm reads 3.5–6.3e-2 with 25–36 % of its
state pinned. These are reported and are not quoted as findings.

### Cap compliance, incidentally

All **3 072** degree-3 readings satisfy the bound proved in `Core/ShareK.lean`: the largest
anywhere is 0.2445 nats = **35.3 %** of `ln 2`, and that one is at rail = 0.62 and excluded on
other grounds. **Zero violations.** A different instrument reaching the same verdict as
`ARRAY_CAP_RESULTS.md`'s Job 1.

---

## 5. THE SCORECARD AGAINST WHAT WAS WRITTEN IN ADVANCE

| | prediction | outcome |
|---|---|---|
| **P3** | some reading clears \|z\| > 5 under both boundaries, rail-clean | **SURVIVED** — decisively; K3 does not fire |
| **P4** | interior maximum in κ within 0.10–0.30 **and** within 0.05 of κ_c | **SPLIT** — see below |
| **P5** | interior maximum in σ in 1e-4…3e-2 | **SURVIVED** — σ* = 0.03 at every κ ≤ 0.14 |
| **P6** | separation does **NOT** transfer; argmax stays at Δ = 1 | **FIRED against me** — at κ = 0.16 the argmax is Δ = 6 |
| **P7** | the 2-iteration cliff survives continuous instrumentation | **SPLIT** — the cliff survives, the "no tail" claim does not |
| **P8** | clip rails > 0.01 at κ ≥ 0.20 | **SURVIVED, and understated** — rails begin at κ = 0.08 |
| **P9** | ŝ₃ within a factor of 3 of the binarized share at the operating point | **SURVIVED** — 2.203e-2 vs 5.104e-2, ratio 0.43 |

### P4 — the coupling axis splits, and the split is the result

The transition was located first, from the raw states (not the kernel's clamp-mediated `phase`
output). The naive order parameter `mean(ρ_ab, ρ_bc, ρ_ac)` **cancels** — the difference
coupling anti-correlates neighbours (ρ_ab, ρ_bc → −0.44) while driving the two ends together
(ρ_ac > 0) — so mean |ρ| and ρ_ac were used instead. Under **fold**, mean |ρ| rises steeply
through **κ_c ≈ 0.16–0.18**. Under **clip** there is a sharp jump at κ ≈ 0.30 to ρ_ac = 0.9995,
which is almost certainly the clamp pinning both ends on the same rail rather than dynamical
synchronization — the same mechanism `ARRAY_CAP_RESULTS.md` identified for the phase metric,
and it appears in **no** fold reading.

Measured symmetry breaking (the h-analogue): raw per-channel skewness runs −0.2 to −0.7 across
the whole map, so the flip symmetry is broken by the dynamics as expected from
`f(1−x) = f(x)`. **But by the transform theorem the marginal skewness is removable and
therefore cannot itself drive the share** — the invariant flip-odd content is the Gaussianized
third moments, and those are what §2 reports.

Then (fold, σ = 1e-3):

| κ | 0.05 | 0.08 | 0.12 | 0.14 | **0.16** | 0.18 | 0.22 | 0.30 |
|---|---|---|---|---|---|---|---|---|
| **S3** (spatial) | 2.8e-5 | 4.9e-4 | 3.7e-4 | 5.6e-4 | **1.55e-3** | 1.15e-3 | 3.3e-4 | 1.1e-4 |
| **C3** (causal) | 1.7e-5 | 7.7e-5 | 2.0e-4 | **2.58e-4** | 9.8e-5 | 7.7e-6 | 1.1e-5 | 3.6e-6 |
| **T3(Δ=1)** | **2.18e-2** | 1.6e-2 | 2.7e-3 | 7.8e-4 | **6.0e-5** | 2.3e-4 | 6.2e-3 | 1.77e-2 |

**The spatial reading peaks at κ = 0.16 and the causal one at κ = 0.14 — at the measured
transition, as the Ising map predicts. The temporal reading has its minimum there**, a factor
of 363 below its own κ = 0.05 peak. Both peaks are **tier B**. Honest limits: `C3`'s peak is a
clean interior maximum at every σ ≤ 0.03; `S3`'s κ = 0.16 peak is a *local* maximum — the value
rises again to 2.19e-3 at κ = 0.60, the top of the swept range, so `S3`'s global maximum is not
bracketed. `T3(Δ=1)` is bimodal, with a second peak at κ = 0.30.

### P5 — the ECA interior noise optimum transfers, with a deflationary caveat

T3(Δ=1), fold, argmax over σ is **0.03 at every κ ≤ 0.14**, with collapse at σ = 0.1:

| κ | σ = 0 | σ = 0.03 | σ = 0.1 | enhancement |
|---|---|---|---|---|
| 0.00 | 3.41e-3 | **4.90e-2** | 6.1e-5 | **14.4×** |
| 0.02 | 1.44e-2 | **5.71e-2** | 5.1e-5 | 4.0× |
| 0.05 | 2.17e-2 | **4.40e-2** | 1.0e-4 | 2.0× |

An interior optimum in both knobs, on a continuous chaotic substrate, matching the ECA
finding. **The caveat is that the largest enhancement is at κ = 0, where the three oscillators
are uncoupled and `b` is an autonomous logistic map.** So the noise optimum is a property of
the one-dimensional noisy logistic map, not of the coupled lattice — the same deflation
`HABIT_DYNAMICS_RESULTS.md` found for the level of the share, now found for its noise
response.

### P6 — my prediction failed and the Ising geometry transferred

Argmax over Δ of T3(Δ), fold, σ = 1e-3:

| κ | 0.02 | 0.05 | 0.10 | 0.14 | **0.16** | 0.18 | 0.20 | 0.30 |
|---|---|---|---|---|---|---|---|---|
| argmax Δ | 1 | 1 | 1 | 1 | **6** | 2 | 2 | 1 |

At κ = 0.16 the values are Δ=1: 6.0e-5, Δ=2: 6.8e-4, Δ=3: 5.6e-4, Δ=4: 1.6e-4, **Δ=6: 7.9e-4**
(z = +134). The local reading sits **13× below** the separated ones. This is the temporal form
of the Ising ridge's "separated triples win near criticality", and it appears at exactly the
transition and nowhere else. Two honest qualifications: it is **tier B** (no boundary
certificate), and the mechanism is as much "the local reading collapses" as "the separated
readings grow" — Δ = 1 falls by 363× at the transition while Δ = 6 does not.

The array **has no spatial separation axis at all** — the coupling graph is a 3-node path per
cell and cells do not interact — which was stated in the prereg before the run, so the
temporal-only test is a disclosed limitation, not a retrofit.

---

## 6. THE CLIFF — a material correction to `HABIT_DYNAMICS_RESULTS.md`

κ = 0.05, σ = 1e-3, **the same frames through both instruments**:

| Δ | ŝ₃ clip | ŝ₃ fold | ratio | z (moment) | **binarized excess** | z (binarized) |
|---|---|---|---|---|---|---|
| 1 | 2.203e-2 | 2.181e-2 | 1.01 | −218 | 5.104e-2 | +44 191 |
| 2 | 1.275e-3 | 1.268e-3 | 1.01 | +168 | 1.592e-2 | +13 077 |
| **3** | **1.057e-5** | **1.127e-5** | **1.07** | **−14.5** | **−6.0e-7** | **−0.4** |
| **4** | **4.333e-5** | **4.300e-5** | **1.01** | **−25.9** | **+2.0e-7** | **+0.2** |
| **6** | **1.101e-5** | **1.095e-5** | **1.01** | **+10.3** | **+1.6e-6** | **+1.1** |
| **8** | **1.282e-6** | **1.383e-6** | **1.08** | **+4.7** | **−8.9e-7** | **−1.1** |
| 12 | −6.5e-8 | −6.3e-8 | — | +0.1 | −6.4e-7 | −0.8 |
| 16 | −6.4e-8 | −4.7e-8 | — | +0.3 | −9.1e-8 | −0.1 |

`HABIT_DYNAMICS_RESULTS.md` reports Δ = 3 as "**exactly at its floor from lag 3 outward** —
flat to lag 256, z ≈ 0 at every subsequent lag". On the same substrate, at the same operating
point, with the binarized instrument reproduced to 0.6 % (G6), **the continuous instrument
resolves boundary-stable structure at Δ = 3, 4, 6 and 8** — two boundaries agreeing to 1–8 %,
rail-clean, with the Gaussian-copula floor at z = −0.08 and the cross-run floor at z = +0.34.

**What changes and what does not.** The **cliff survives**: three orders of magnitude between
Δ = 2 and Δ = 3, and the tail is 500–2 000× below the Δ = 1 value, so nothing about the shape
of the decay is overturned. The **"no tail whatsoever" claim does not survive**, and neither
does the lifespan: it is **8 kernel iterations, not 2**. Median binarization destroyed the
tail; the moment route did not manufacture it — the matched floors that would catch
manufacture all floor.

The tail is also **non-monotone** (Δ = 4 exceeds Δ = 3), consistent with the period-2
oscillation that `HABIT_DYNAMICS` found independently in the formation transient and in the
strongly negative lag-1 ACF.

**At κ = 0 — uncoupled, a single autonomous logistic map — both instruments see the tail**
(binarized Δ=3 = 1.72e-3 at z = 2 031). So the binarization blindness is specific to the
coupled case, and it is where the whole-only content is small that the median split loses it.

**Recommendation for Eric's review, not actioned here:** `HABIT_DYNAMICS_RESULTS.md`'s
Measurement 1 should carry this as a correction — its lifespan of 2 is the lifespan *of the
binarized reading*, and the ratio τ_share/τ_pair in its follow-up is computed from that
number. No prior file has been edited.

---

## 7. THE CROSS-INSTRUMENT DISAGREEMENT AT THE TRANSITION — K6 UNRESOLVED

At κ = 0.16, σ = 1e-3, fold, Δ = 1, on the same frames:

| | value |
|---|---|
| moment route `ŝ₃` | **6.01 × 10⁻⁵ nats** |
| binarized `shareK` excess | **8.46 × 10⁻² nats** (z = +87 952, tied fraction 0.00000) |
| ratio | **1 400×** |

The binarized value is not an outlier of that instrument: it is the same fold ridge
`HABIT_DYNAMICS_RESULTS.md` found at κ = 0.20 (CF 0.110 in units of `ln 2`, i.e. 0.076 nats),
reproduced here at κ = 0.16.

K6 asked whether ŝ₃ *and* ŝ₄ both fall far below a clean binarized reading. **ŝ₃ does. ŝ₄
cannot answer**, for the reason in §8. So **K6 is UNRESOLVED — the disagreement is real and
this run does not settle its cause.** The two candidates, neither tested here:

- the array's whole-only content at this operating point lives **above degree 3**, in the
  moment route's blind spot; or
- **coarse-graining increased** `I_C⁽³⁾` — which the prereg explicitly declined to rule out
  (§8.5), since monotonicity of the share under a per-channel pushforward requires the
  pairwise family to be closed under it, and that is not established.

A third possibility, offered as a hypothesis and labelled as one: at κ = 0.16 the *fold* clamp
binds on 10.3 % of updates, so the state carries heavy near-boundary pileup. A median split of
a piled-up distribution can express rule-like binary structure that low-order moments of the
rank-transformed variable do not see. This is a mechanism sketch, not a measurement.

**A first draft of this section reasoned in the wrong direction** — it treated the binned
reading as the one likely to be inflated by pileup. §9 measures the opposite: under a
saturating readout the binned route is the *exactly invariant* one and the moment route is the
exposed one. That does not settle κ = 0.16 either (the moment route reads **low** there, not
high, so inflation is not the question), but it removes the presumption I had been leaning on,
and it is corrected here rather than quietly dropped.

**This remains a caution for the moment route generally, including for the `SKY_PILOT` sibling
using the same bridge**: on a substrate with an active saturating nonlinearity, the degree-3
projection can understate a binned reading by three orders of magnitude.

---

## 8. THE DEGREE-4 EXTENSION IS NOT USABLE HERE, AND IT SAYS SO ITSELF

The prereg's §1.3 secondary was `ŝ_D = ½ Σ_m ⟨u, e_m⟩²` over an orthonormal basis of
`W^⊥ ∩ P_D`. With the sign bug fixed and the fixed-basis route validated against the exact
closed form to 0.2 %, at κ = 0.05, σ = 1e-3, fold:

| D | 3 | 4 | 5 |
|---|---|---|---|
| `ŝ_D` (nats) | 2.181e-2 | **7.51e-1** | **6.20** |

`Core/ShareK.lean` proves `share ≤ (k−2)·ln 2 = 0.6931` at k = 3. **D = 4 returns 0.751 and
D = 5 returns 6.20 — above the proved cap, by 8 % and by a factor of 9.** A valid estimate of
this quantity cannot do that. The second-order expansion `I_C⁽³⁾ = ½‖P_{W^⊥}u‖² + O(u³)`
requires `u` to be small, and once degree-4 and degree-5 directions are included on a substrate
this far from its Gaussian reference, it is not.

**The estimator self-diagnoses**, against a machine-checked bound, and the diagnosis is
reportable in one line: **the negentropy proxy passes the ShareK cap at D = 3 on all 3 072
readings and fails it at D ≥ 4.** D = 3 is where this instrument may be used on this substrate,
and the degree-3 blind spot (flip-symmetric whole-only content, §1.3 of the prereg) therefore
remains **untested**, not cleared.

---

## 9. THE BRIEF'S PREMISE IS REFUTED — measured, on this substrate

The brief that commissioned this run held that binarization is "a threshold nonlinearity,
exactly the artifact family that has burned this programme three times today", and that going
moment-native removes it. The sibling convergent-art check (`e601aec`, CORRECTION 3) says the
reverse: *"Being moment-native is the exposure, not the protection."* That was tested here
directly rather than assumed to transfer.

A one-sided readout clip at quantile `q` is applied to the **readout only** — the dynamics is
untouched — at the certified operating point (κ = 0.05, σ = 1e-3), on identical frames, through
three routes (`array_negentropy_cliptest.py`):

| tie block | 1-pt skewness | **(A) median-binarized** | **(B) bridge, no Gaussianization** | **(C) bridge, rank-Gaussianized** |
|---|---|---|---|---|
| 0 | −0.428 | 1.000 | 1.000 | 1.000 |
| 0.01 | −0.429 | **1.000** | 0.976 | **1.214** |
| 0.02 | −0.430 | **1.000** | 0.949 | **1.369** |
| 0.05 | −0.436 | **1.000** | 0.907 | **1.716** |
| 0.10 | −0.450 | **1.000** | 0.984 | **1.997** |
| 0.20 | −0.509 | **1.000** | 2.056 | 1.389 |
| 0.25 | −0.561 | **1.000** | 3.312 | 0.469 |

Ratios to the unclipped reading. Reproduced identically under both boundary conventions.

**The median split is exactly invariant — 1.000 at every level, because a clip is a monotone
map and cannot move the median, so not one binary cell changes.** Both moment routes move.
The rank-Gaussianized one — the instrument this run is built on — **inflates ×2.0 at a 10 %
tie block**, and rank-Gaussianization is *not* the protection I expected it to be: it is the
more exposed of the two moment routes at small tie blocks, because a clip creates a tie block
and mid-ranks collapse it to a single score.

**What this does to the headline: it constrains it, and the constraint was pre-registered.**
Every tie block above is a rail fraction of `1 − q`, and the rail threshold frozen before the
run is **0.01** — which this table shows admits up to ~21 % inflation at its own limit, a
number I could not have quoted in advance. The headline reading sits at rail = **3.4 × 10⁻⁴**
under clip and **0** under fold, 30× inside that threshold, and the two boundaries agree to
1.0 % — consistent with an exposure well under 1 % there. So the headline stands, but it stands
on the rail threshold doing its job, not on the moment route being intrinsically safe.

**What it does to the framing: the two instruments have complementary exposures and neither
dominates.** The binned route's exactness under readout saturation and its blindness to the
cliff tail (§6) are *the same property* — it is invariant because it looks only at the median
split, and it misses the tail for the same reason. The moment route sees ~500× finer structure
and pays for it with saturation exposure. **They should be run together, which is what §6
did**, and the brief's instruction to replace one with the other was wrong.

---

## 10. WHAT IS NOT CLAIMED

1. **Nothing about nature.** A designed chaotic lattice on our own GPU is a model system.
   `wild-share` is untouched, as is `adequacy` and every Logos claim.
2. **No stance change**, no `Stance.lean`, no Lean file, no audit, `lake` never run.
3. **No priority claim, and the closest prior art is named.** The invariance is Sklar (1959)
   copula theory, stated for cosmological fields by Scherrer et al. (2010); the parent
   expansion is Jones & Sibson (1987). See §2. The bridge is the *projection* of that
   expansion onto the one direction pairs cannot see, which is the step that cancels the
   pointwise sector; it was derived independently for the cosmological arm by the `SKY_PILOT`
   sibling and is shared, not duplicated as a discovery. **Assume convergence.**
4. **It is not negentropy** — see the correction at the head of this document; the label in
   the brief and in these filenames is wrong, and G4 is the gate that separates them.
5. **`ŝ₃` is a second-order proxy, not the share.** It is exact only to `O(u³)`, with a
   measured accuracy budget of ~5 % at moderate non-Gaussianity, and it is labelled `ŝ`
   throughout.
6. **No discovery of order-3 in the array.** Order-3 structure in a nonlinear lattice was
   pre-committed as expected and is reported as a magnitude against a ceiling, not as news.
   Most of it survives with the coupling turned off entirely (κ = 0 gives 3.4e-3 against
   2.2e-2 at κ = 0.05, and the σ-enhancement is *largest* at κ = 0).
7. **No boundary certificate above κ = 0.05.** Tier B is reported, never quoted.
8. **The κ = 0.16 disagreement is not adjudicated**, and the degree-3 blind spot is not
   cleared.
9. **IAAFT was not used and its absence is not a gap** — a clip artifact survived it at
   z = 86 on 2026-07-24.

---

## FILES

| | |
|---|---|
| `ARRAY_NEGENTROPY_PREREG.md` | pre-registration, committed `9251b5b` before any code |
| `array_negentropy.py` | instrument, gates, driver, transition scan, sweep, cliff |
| `array_negentropy_analyze.py` | the pre-registered verdict rules applied to the sweep |
| `array_negentropy_gate.log` | the full gate run |
| `array_negentropy_transition.{json,log}` | the synchronization transition |
| `array_negentropy_sweep.{json,log}` | 3 072 readings over (κ, σ, boundary, geometry) |
| `array_negentropy_cliff.{json,log}` | the cliff, with the binarized cross-instrument on the same frames |
| `array_negentropy_analysis.txt` | the applied verdicts, maps, ridge tables |
| `array_negentropy_cliptest.{py,json,log}` | §9, the readout-saturation exposure test (post-hoc, in response to `e601aec`) |

Primary seed 20260725; cross-run floors at seeds 424242 and 777. Research → scratchpad memo →
Eric's review. Nothing pushed.
