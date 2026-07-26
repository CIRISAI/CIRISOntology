# RESULTS — could a survey measure gravity's whole-only share? A forecast

Pre-registered in `SKY_FORECAST_PREREG.md`, committed at **`b89ce48`** *before* `sky_forecast.py`
existed and before any number in it was computed. Scratchpad only: no Lean file, no
`Stance.lean`, no audit was touched, and `lake` was never run.

---

## SCOPE, FIRST AND LOAD-BEARING

**This is a forecast on mocks I generated myself. No real survey data was read. Nothing here
is a claim about the sky, about cosmology, or about nature.** The deliverable is a **go/no-go
for a real-data pre-registration**, and nothing else. Second-order perturbation theory is the
*leading-order* gravitational prediction, not N-body, so every number is a **lower anchor** —
which makes a GO conservative and a NO-GO provisional, exactly as §0 of the pre-registration
staked in advance.

---

## SCOPE, SECOND PART — what theorem protects this reading, and what does not

Added after §1–§11 were written, when a sibling corrected a scope claim I had been given.
It changes no measured number and it conditions how every one of them reads, so it goes here
rather than in an appendix.

**Everything measured in this document is the whole-only share OF THE BINARIZED FIELD** — the
`b = 2` sign-triple excess after a median split. That is a well-defined observable in its own
right, and it is the one the pilot recommended on three independent grounds
(`SKY_PILOT_RESULTS.md` §9.6). It is **not** the continuum share, and the relation between
them is an open question, not a background assumption.

**What does protect it, and is used here.**

* **Sklar / monotone invariance.** The median-split share is *exactly* invariant under per-cell
  monotone continuous maps, because such a map carries the median to the median and preserves
  every sign. So no pointwise nonlinearity in the readout — clipping, saturation, a lognormal,
  a rank map — can move it. This is not assumed here, it is **verified bit-for-bit**: gate GC
  finds **0 differing cells of 56 623 104** between each pointwise floor and its parent
  Gaussian.
* **The sign-symmetry lemma** (`Core/SignSymmetry.lean`). A sign-symmetric field binarizes to
  a state whose share is exactly 0. Every Gaussian arm here is sign-symmetric by construction,
  so its true reading is **exactly zero regardless of its pair structure**, and whatever it
  reads *is* the pipeline error. Measured: `t = +1.37` and `+1.40` over six independent
  realisations (§1). **That certifies the pipeline without needing any general result.**

**What does NOT protect it, stated so it cannot be leaned on.**

* The no-creation dichotomy (`Core/Creation.lean`, `6df61c5`) is proved for **same-alphabet
  `Bool → Bool`** per-cell maps, where the only deterministic options are bijections and
  constants. **The median split is `ℝ → Bool` — alphabet-reducing — and is not covered.** I
  make no claim that binarization cannot manufacture share, and the RG intuition runs the
  other way: coarse-graining a fine distribution that *is* pairwise-maxent generically yields
  a coarse one that is *not*, so deterministic coarse-graining can in principle mint `b = 2`
  share out of pure two-point structure. That is the live hypothesis a sibling (`kappa-edge`)
  is adjudicating, and this forecast **depends on its verdict**.
* **The consequence, precisely.** My controls are untouched either way: the Gaussian and
  pointwise floors are pinned to exactly zero by the two theorems above, whatever binarization
  does. What *is* conditional is the step from "gravity's binarized field reads nonzero" to
  "the continuum gravitational field carries whole-only pattern" — including §4's tidal
  reading at `z = +28`. **If `kappa-edge` confirms, that step needs a fine-`b` pair-maxent
  surrogate control at this pipeline's resolution: a field whose fine-grained distribution
  carries gravity's pair marginals and no order-3 content, pushed through the identical median
  split.** *When I first wrote this I added that I had no such control and could not build
  one. **That was wrong, and §13 is the retraction**: the control is a pure histogram
  computation, it is built, and it says the mechanism is real on gravity (`t = 4.3`, converged
  in `b`) but costs the deliverable only 14 % at `R = 10` while removing the `R = 25` result
  entirely. The dependency is no longer pending; it is measured.*
* The pilot already measured that the two numbers differ: `A(b=2)/A_∞ = 1.11–6.6`
  (`SKY_PILOT_RESULTS.md` §7). **Median binarisation can read five to six times the continuum
  value**, so "binarized share ≈ continuum share" was never available anyway.

**Where the theorem boundary helps rather than hurts.** The dominant systematic in this
document is a *spatial, cross-cell* filter (smoothing, mass assignment, window) manufacturing
share — §2, §10. `Core/Creation.lean` covers only *per-cell* maps, so it offers no protection
there, and none is claimed. **The forward-model requirement in §8 therefore stands with its
boundary now named exactly**: the filter systematic lies outside every no-creation result in
the repository, which is why it must be modelled and can never be argued away.

---

## THE HEADLINE

**The measurement is detectable at enormous significance — and it does not measure gravity.**
Both halves are load-bearing; §11 is the one that settles the second half, and it is a fired
prediction rather than a caveat.

A DESI-like volume would separate a 2LPT gravity mock from a pointwise-transform mock matched
in `P(k)` **and** in its one-point law at **z ≈ 67 at `R = 10` Mpc/h, 43 at 15, 23 at 25** —
and the required volume is **0.11–0.91 (Gpc/h)³**, twenty to two hundred times *less* than
DESI. Above `R = 40` Mpc/h it collapses: 41 (Gpc/h)³ needed at 40, and 130–500 beyond.
**Outcome (a) at `R ≤ 25` Mpc/h; outcome (b) at `R ≥ 40`** — *revised down to `R = 10–15`
by §12 and §13, which were run last: `R = 25` does not survive the binarization control, and
Poisson sampling at DESI density manufactures 130 % of the GAP.*

But the decomposition, which the pre-registration did not ask for and which I added when the
first sweep came back, changes what that detection *means*. Writing `A` for gravity's excess
over an exact-zero Gaussian and `M` for what the pointwise mock's own filter manufactures from
nothing, `GAP = A − M` identically, and at `R = 10`, equilateral:

| | `A` (gravity) | `M` (floor's filter) | `GAP` |
|---|---|---|---|
| value | `5.74e-04` | `−7.83e-03` | `8.41e-03` |
| paired `z` | 3.3 | **−60.2** | 38.0 |

**93 % of the gap is the floor's manufactured term, not gravity's own structure.** The
instrument separates gravity from a filtered local transform very well — but mostly because
the local transform, once filtered, produces a large signal *of the opposite sign*, not
because gravity's own whole-only structure is large.

And the measurement I added to settle it — reading the sign triples with **no filter at
all**, where the pointwise floors provably read exactly zero — says this:

> **The gravitational field's *intrinsic* whole-only excess is real but small and short-range.**
> Unfiltered, the second-order field reads `4.9e-04` at `z = +5` at 10 Mpc/h separations, and
> its **tidal sector alone reads `1.35e-03` at `z = +28`**. At 30 and 80 Mpc/h it is
> consistent with zero. The full field's net is small because the local sector contributes
> `−1.14e-03` with the opposite sign.

So the pre-registered interpretive stake — *the tidal sector counts as a YES* — **is met**,
at 10 Mpc/h separations, on a leading-order mock. Everything larger is pipeline.

---

## 1. GATES — all pass, and four of them caught real errors

`sky_forecast_gate.json`, `N = 384`, `L = 1500` Mpc/h.

| gate | result |
|---|---|
| **GA1–3** `b=2` machinery: parity → `ln 2`; independence → 0; 2000 sign-symmetric states → 0 | exact / `4.4e-16` |
| **GF1** real-space `δ⁽²⁾` vs a **brute-force `F₂` convolution** on `16³`, sector by sector | **`1.8e-07`** |
| **GF2a** linear displacement, `⟨dep/W · δ₁*⟩/⟨|δ₁|²⟩ → ε` | `0.994 … 0.998` |
| **GF2b** second-order displacement, alias-clean (2LPT − ZA) `→ ε²` with coefficient `3/7` | exponent **1.996**, coeff `0.988–0.996` |
| **GF3** 2LPT reproduces the linear field at low `k` in amplitude **and phase** | `P` ratio 0.977, cross-corr 0.985 |
| **GC** floor sign pattern identical to its parent Gaussian, pre-smoothing | **0 cells** of 56 623 104 beyond float32 rounding |
| **GD** `P(k)` match to the 2LPT target for `kR ≤ 2` | F0 `4.5e-07`, lognormal `8.1e-04`, rank `1.2e-03` |
| **GB** stride convergence on the 2LPT arm | `0.0000` |
| **GE** Gaussian and linear arms read zero within their own octant error | `1.61 σ` |
| **GH** orientation pooling is a mixture of *identical* laws | `0.0000` |
| tied fraction, every arm/scale/realisation | max **`7.1e-08`** |

**Four errors the gates caught, recorded rather than quietly fixed.**

1. **Nyquist sign convention.** `rfftn` calls the Nyquist mode `+N/2`, `fftn`'s fold calls it
   `−N/2`, so a spectral first derivative there is genuinely ambiguous. GF1 failed at **23 %**
   until every differentiated field was generated with the Nyquist planes empty.
2. **The white-noise fluctuation applied twice.** Building a floor at amplitude
   `√P_target[bin]` re-applies the `|w_k|²` shell fluctuation already inside `P_target`; the
   low-`k` bins missed by **35 %**. Dividing by the white noise's own shell power fixes it,
   and GD went from 0.35 to `4.5e-07`.
3. **CIC alias of a displaced lattice — twice misdiagnosed by me.** It is `O(ε)`, not
   `O(ε³)` — **11 %** of the linear signal at `k = k_Nyq/4` — so the pre-registered residual
   test could not converge. Interlacing (Sefusatti et al. 2016) halves it to 5–7 %. Then the
   second correction: the alias is **not** uncorrelated with `δ⁽²⁾` (corr 0.72), so a
   cross-spectrum does not rescue the test either. The gate that works differences the 2LPT
   and ZA deposits, which share the first-order displacement, so the alias cancels.
   **The alias is a property of the mock, and it is why the Eulerian SPT2 arm is carried as a
   cross-check on every conclusion below** — and GAP(SPT2) tracks GAP(2LPT) to 10–15 % with
   the same sign at every scale and geometry, so aliasing is not driving any result here.
4. **LPT damps small-scale power; it does not enhance it.** The pre-registration expected
   `P_2LPT/P_lin > 1` at high `k`; displacement smearing plus CIC gives **0.38**. This is a
   known LPT limitation against N-body, logged not gated, and it is precisely what makes this
   forecast a lower anchor.

**Three gate designs were amended, disclosed here.** GB/GE/GH are judged against the
octant-subsample error, because a single realisation cannot be tested against an absolute
threshold — on a small box the Gaussian arm's `|E|` *is* its own sampling noise, which is the
point. GC allows disagreements within float32 rounding of the median (0 cells survive that
test). GF3's high-`k` clause became a logged diagnostic for the reason in (4).

**Post-sweep GE, the version a single realisation could not do.** Pooling the exact-zero arms
over the six independent realisations of the small box: the config-averaged `E` reads
`t = +1.37` (Gaussian floor) and `t = +1.40` (linear field). **The theorem-protected null
holds.** The two track each other to three digits per realisation, which is the signature
being looked for: `E`'s scatter is a large-scale-mode common mode shared by every arm built
from the same phases — which is why the *paired* difference is the right statistic.

**Error bars are conservative, measured.** The octant-subsample SEM is **3.2× larger** than
the realisation-to-realisation SEM (median ratio 0.31). It is used only in the gates, never
in the forecast, which uses the realisation scatter.

---

## 2. THE DECOMPOSITION — `A`, `M`, `GAP`, and which side dominates

Small box, `N = 384`, `L = 768` Mpc/h (cell 2.0), `V = 0.453 (Gpc/h)³`, 6 realisations, all
arms from the same white noise. Floor = **F2, the rank-matched mock** (matched `P(k)` *and*
matched one-point law); the lognormal floor F1 is in §6.

| `R` | geometry | sides (Mpc/h) | `A` = grav − Gauss | `z` | `M` = floor's filter | `z` | `GAP` | `z_p` | `z_s`@DESI |
|---|---|---|---|---|---|---|---|---|---|
| 10 | equilateral | 16, 16.1, 16.1 | `5.74e-04` | 3.3 | `−7.83e-03` | −60.2 | `8.41e-03` | 38.0 | **67.0** |
| 10 | **folded** | 16, 32, 16 | **`5.98e-03`** | **18.7** | `+9.71e-03` | 33.7 | `−3.73e-03` | −7.3 | 20.7 |
| 10 | orthogonal | 16, 16, 22.6 | `1.77e-03` | 7.6 | `−6.10e-03` | −37.5 | `7.87e-03` | 36.4 | 56.4 |
| 10 | squeezed | 4, 16, 16.5 | `6.77e-05` | 1.0 | `−2.38e-03` | −41.7 | `2.45e-03` | 47.5 | 66.7 |
| 15 | folded | 22, 44, 22 | `5.18e-03` | 28.8 | `+7.82e-03` | 32.2 | `−2.64e-03` | −11.9 | 18.5 |
| 25 | folded | 38, 76, 38 | `3.93e-03` | 16.5 | `+6.90e-03` | 8.7 | `−2.97e-03` | −3.6 | 7.8 |

Two things read off this, and they point in different directions.

**(a) The gap is the floor's, not gravity's.** `|M/A|` is 13.6 (equilateral), 3.5
(orthogonal), 35.1 (squeezed) at `R = 10`. Since GC proves each floor's *pre-filter* sign
pattern is bit-identical to its parent Gaussian, **100 % of `M` is manufactured by the
smoothing** — the pilot's `SKY_PILOT_RESULTS.md` §6(a) effect, now measured on a realistic
pipeline, with a sign, and with a geometry dependence: negative at equilateral, orthogonal and
squeezed, **positive at folded**.

**(b) Gravity's own excess lives in the folded (collinear) configuration.** There `A` reaches
`5.98e-03` at `z = 18.7`, and `|M/A|` falls to 1.6. In nats, at `R = 10` folded, the share is
`I_2LPT = 4.30e-05` against an estimator floor of `I_F0 = 1.09e-06` — **39×** — where at
equilateral it is `1.36e-06` against `5.25e-07`, only 2.6×. **The whole-only share of the
gravity mock is a folded-configuration effect**, which is the shape where the `F₂` tidal
kernel `(2/7)(μ²−1/3)` is at its `|μ| = 1` maximum.

---

## 3. THE FORECAST TABLE — the deliverable

`z_s = |GAP| / [ σ(E_2LPT across realisations) × √(V_box/V) ]`, `V = 20 (Gpc/h)³`.
This is the **survey** number: one universe, a forward-modelled floor.

| `R` (Mpc/h) | box | `V_box` | `σ_R` | best geometry | `GAP` | `z_p` | **`z_s` @ DESI** | `V` needed for 5σ |
|---|---|---|---|---|---|---|---|---|
| **10** | small | 0.453 | 0.318 | equilateral | `8.41e-03` | 38.0 | **67.0** | **0.11 (Gpc/h)³** |
| **15** | small | 0.453 | 0.210 | equilateral | `5.49e-03` | 12.2 | **43.4** | **0.27** |
| **25** | small | 0.453 | 0.115 | squeezed | `1.11e-03` | 5.2 | **23.5** | **0.91** |
| **40** | large | 7.078 | 0.062 | equilateral | `2.05e-03` | 4.2 | 3.5 | 41 |
| **60** | large | 7.078 | 0.034 | folded | `−1.69e-03` | −3.8 | 1.9 | 135 |
| **100** | large | 7.078 | 0.015 | folded | `−1.78e-03` | −1.1 | 1.0 | 493 |
| **150** | large | 7.078 | 0.007 | equilateral | `−2.77e-03` | −1.2 | 1.1 | 432 |

`z_s` carries a **±30 % uncertainty** from estimating `σ` on six realisations, and it
**ignores the uncertainty in the modelled floor**, which on real data would dominate (§7).

**Cross-box consistency at the `R = 40` overlap** (cell 2.0 vs 5.0 Mpc/h): 7 of 8
configurations agree within 1.5 σ; equilateral at `r = 1.5R` differs by 3.1 σ. The small box
is the unreliable one there — its `σ_box` is **10× larger** and the triple sides reach 7.8 %
of the box — so the large-box row is the one quoted. One 3 σ in eight comparisons is
unremarkable, but it is recorded rather than averaged away.

---

## 4. THE UNFILTERED MEASUREMENT — added after the sweep, and it decides the reading

**Not pre-registered.** Added because the sweep exposed a question the pre-registration did not
ask: every floor's reading is 100 % filter-manufactured (GC), so is *gravity's* also?

The Eulerian SPT2 arm has no particles, no CIC and no smoothing, so at `R = 0` it is a
genuinely unfiltered field carrying the exact tree-level three-point structure. Its Gaussian
counterpart reads **exactly zero** by `share_eq_zero_of_signSymmetric`, and by GC the pointwise
floors read the same bit for bit. So `E(arm) − E(F0)` here is **intrinsic**, and no filter can
be blamed for it in either direction. `L = 1920` (cell 5.0 Mpc/h), 4 realisations, equilateral.

| separation | SPT2 (full) | LOCAL | SHIFT | **TIDAL** | linear | 2LPT (*not* unfiltered) |
|---|---|---|---|---|---|---|
| **10 Mpc/h** | `4.86e-04` (+5) | `−1.14e-03` (−5) | `8.1e-05` (+1) | **`1.35e-03` (+28)** | `7.5e-05` (0) | `2.38e-02` (+44) |
| **30 Mpc/h** | `3.2e-05` (0) | `8.0e-05` (0) | `1.3e-04` (0) | `1.7e-04` (+1) | `1.2e-04` (+1) | `2.36e-03` (+11) |
| **80 Mpc/h** | `3.3e-04` (+1) | `2.0e-04` (+5) | `2.2e-04` (+1) | `1.0e-04` (0) | `2.9e-05` (0) | `7.2e-05` (0) |

Four readings.

1. **The tidal sector carries intrinsic whole-only excess at `z = +28`, at 10 Mpc/h.** This is
   the pre-registered stake, and it is met — on a leading-order mock, at one separation, **and
   as a statement about the binarized field**. Per "Scope, second part", the step from here to
   the continuum field is conditional on `kappa-edge`'s verdict on whether the median split can
   itself mint `b = 2` share from pure pair structure. What is *not* conditional is the
   comparison: F0 and the pointwise floors are pinned to exactly zero by theorem whatever
   binarization does, so the *excess* is real even if its continuum meaning is pending.
2. **The full second-order field nets only `z = +5`** because the LOCAL sector contributes with
   the *opposite* sign. The two partially cancel.
3. **Beyond 30 Mpc/h the intrinsic excess is consistent with zero** at this volume. Everything
   the smoothed sweep sees at `R ≥ 10` with sides of 16–450 Mpc/h is therefore **pipeline**,
   on both sides of the comparison.
4. **The 2LPT particle arm reads 49× the Eulerian arm** at 10 Mpc/h. CIC deposit is a filter,
   so this arm cannot answer the intrinsic question; the discrepancy is a further measurement
   of how much a mass-assignment step manufactures. After smoothing at `R ≥ 10` the two arms
   agree on the GAP to 10–15 %, so the deposit scale is filtered out of the main result.

---

## 5. THE POISSON GATE — the valve configuration, and an honest under-power

*(Superseded in power by §13, which re-runs this properly after `Core/Valve.lean` landed.
The pre-registered run is left exactly as it was executed and reported here unchanged.)*

Poisson sampling is a per-cell stochastic map, hence a **mixture**, and `ECA_SPIKE_RESULTS.md`
records that mixtures manufacture higher-order structure from none. Applied to the exact-zero
Gaussian field at `n̄ = 1e-4 … 1e-2 (h/Mpc)³`, paired against the same field with no sampling:

**No monotone trend with `n̄` appears over two decades** (`n̄V_R` from 25 to 34 000). The
paired shift is bounded by `|ΔE| ≲ 2e-03` at every density, with no rise as `n̄` falls.

**Prediction F7 is not confirmed, and the run is under-powered** (3 realisations), so this is a
**bound, not a null**: a shot-noise term smaller than `2e-03` in `E` cannot be excluded, and
that is *comparable to the GAP itself at `R = 25`* (`1.1–3.8e-03`). The mechanism half of F7
survives — the contribution enters only through `Σ_i A_{1i}A_{2i}A_{3i} ζ_iii`, which needs two
nonzero off-diagonal correlations and is therefore suppressed at the separations used here.
**A real design must run this gate properly.** As it stands it is the weakest link in the
forecast, and it is stated that way rather than rounded up.

---

## 6. ROBUSTNESS — the gap does not depend on which pointwise floor is used

Against the **lognormal** floor F1 instead of the rank-matched F2, at `R = 10`: `GAP` is
`9.41e-03` (equilateral), `−5.03e-03` (folded), `8.63e-03` (orthogonal), `2.72e-03` (squeezed)
— **same sign everywhere, 10–35 % larger**. The two floors bracket gravity in post-smoothing
skewness (`R = 10`: gravity 1.073, rank 0.918, lognormal 1.213), so **skewness mismatch is not
what produces the gap**.

One honest limitation of the "matched one-point law" claim: the rank map matches the
one-point law of the field *entering* the pipeline. After smoothing they separate by ~15 %,
because different fields Gaussianise differently under a filter. Matched before the filter,
not after.

---

## 7. SCORECARD AGAINST THE PRE-REGISTRATION

| # | prediction | outcome |
|---|---|---|
| **F1** | `E_gravity ≠ 0` above the Gaussian floor at `R ≤ 40` | **SURVIVED** — `z` up to 30 at `R = 10–15`, largest in the folded configuration |
| **F2** | `d log|E| / d log σ_R = 1.0 ± 0.3` | **FAILED as staked.** On raw `E`: `−0.85 … +1.55`, mostly negative, because raw `E` is dominated by a phase common-mode. On the `GAP`, which removes it: `+1.0 … +1.7` (folded `+0.22`) — consistent for 3 of 8 configurations, high for the rest |
| **F3** | `E ∝ D` (growth) | **SPLIT (§11).** For gravity's own excess `A`: **SURVIVED**, exponent `+0.82` against a staked 1.0. For the `GAP`: **FAILED**, exponent `+0.12` — the deliverable statistic is blind to the growth factor |
| **F4** | LOCAL sector reads `≈ 0` | **FIRED, with the cause pre-registered.** LOCAL reads `−1.14e-03` at `z = −5`. The map `δ + (17/21)δ²` is monotone only for `δ > −0.618`, and the measured non-monotone fraction is **41 %** at cell 2.0 Mpc/h and 17 % at 5.0. The premise fails at these resolutions; the theorem is untouched, and is verified directly by GC (0 cells) |
| **F5** | `|GAP| / E_gravity > 0.1` at `R ≤ 40` | **SURVIVED**, overwhelmingly — the ratio usually exceeds 1 |
| **F6** | `|GAP|` largest at folded/squeezed, smallest at equilateral | **FAILED** — largest at equilateral, smallest at squeezed. *Post-hoc, flagged as post-hoc:* gravity's own excess `A` **is** largest at folded, which is what the tidal-kernel argument actually described; the argument was right about gravity and wrong about which quantity carries it, because `GAP` is dominated by the floor |
| **F7** | Poisson shot noise creates share, rising as `n̄` falls | **SURVIVED (§12).** The pre-registered 3-realisation run saw no trend; at 10 realisations the rise is monotone at `t = 12–31`, reaching **130 % of the GAP** at DESI density. My §5 null was a **power failure** and is retracted |
| **F8** | `z_s ∝ √V · R^{−2 … −2.5}` | **FAILED** — within the small box (10→25) the exponent is **−1.15**, much shallower, and then a cliff (−4.1 from 25→40). The mode-counting argument does not describe the scale dependence |

**Five of eight predictions failed or went unconfirmed.** F1 and F5 survived, which is what
the detectability verdict rests on. But §11 shows the trichotomy itself was mis-specified: the
criterion it attached to outcome (a) is met, and the interpretation it attached to that
criterion was wrong. That correction is recorded there rather than absorbed here.

---

## 8. THE VERDICT, against the criteria fixed in advance

> **(a) CONDITIONAL GO, at `R = 10–15` Mpc/h only.** `z_s ≥ 5` for a DESI-like volume with
> 20–200× statistical margin (0.11–0.27 (Gpc/h)³ needed), and the GAP retains 86–100 % of
> itself under the binarization control at `t = 13.7–20.5` (§13). **`R = 25` is withdrawn**:
> it passes on statistics (`z_s = 23`) and fails the binarization control (`t_corr = 0.5–0.9`).
> A real-data pre-registration is warranted **only if it jointly forward-models the spatial
> filter, the median split and Poisson sampling, and demonstrates the residual is below the
> signal** — which §12.3 shows is not automatic: matched sampling of the floor leaves 26–136 %
> of the GAP behind, at `t = 4.5–11.3`.
>
> **(b) VALID BUT TOO SMALL, at `R ≥ 40` Mpc/h.** The gap survives the paired test at `R = 40`
> (`z_p = 4.2`) but needs ~41 (Gpc/h)³, twice DESI; beyond `R = 60` it needs 130–500.

I pre-registered "(a) at `R ≤ 40`, (b) at `R ≥ 100`". **The transition is at a smaller scale
than I staked** — between 25 and 40 Mpc/h, not between 40 and 100.

**Four conditions on the GO, which a real pre-registration must carry and which are not
optional.**

1. **The detection would rest on the floor model, not on gravity.** 93 % of the gap is what
   the pointwise mock's filter manufactures (§2a). On real data that floor must be
   forward-modelled from the actual window, mask, selection and mass assignment — and
   `SKY_PILOT_RESULTS.md` §6(a) plus §2 here say that model *is* the measurement, not a
   correction to it.
2. **Gravity's intrinsic share is short-range.** Unfiltered, it is `z = +5` overall and
   `z = +28` in the tidal sector at 10 Mpc/h, and consistent with zero by 30 Mpc/h (§4). The
   scales where the measurement is detectable are not the scales where the effect is intrinsic.
3. **The shot-noise gate is not yet closed** (§5). Its bound is comparable to the signal at
   `R = 25`.

4. **`GAP ≠ 0` is a two-sided test that a Gaussian field also passes** — see §10.2, added
   after this section was written. The control that rescues it is §10.1: gravity's pointwise
   sector reads the same as the floor while its shift and tidal sectors do not.
5. **The systematic budget is not under control, and this is the binding condition.** Three
   independent channels each manufacture whole-only excess comparable to the signal: the
   spatial filter at **93 %** of the GAP (§2a), the median split at **14 %** at `R = 10` and
   ~62 % at `R = 25` (§13), and Poisson sampling at **130 %** at DESI density, falling to a
   still-significant **26 %** after matched forward-modelling (§12). **A design that does not
   model all three jointly will measure its own pipeline.**

**For `wild-share`, the open claim.** The pre-registered stake was that the non-pointwise
sector counts as a YES, existence and not novelty-of-mechanism being the question. **That stake
is met**: the tidal sector of a leading-order gravity mock carries whole-only sign-triple
excess at `z = +28` with no filter involved, on a field whose Gaussian counterpart is zero by a
machine-checked theorem. **But this is a fact about my mock, not about the sky**, and
`wild-share` stays open — what this buys is permission to *write* a real-data
pre-registration, which would itself still need a refuter pass and Eric's review.

---

## 9. WHAT THIS DOES NOT ESTABLISH

1. **Nothing about the sky.** No survey data, no catalogue, no cosmological parameter. Every
   field is mine.
2. **No stance change, under any outcome.** `wild-share` stays open. Nothing here goes near
   `Stance.lean`.
3. **Leading order only.** 2LPT and second-order Eulerian PT are not N-body; §1(4) measures
   one way this bites (LPT damps rather than enhances small-scale power). A no-go at `R ≥ 60`
   is a no-go for the leading order.
4. **No priority claim.** 2LPT (Buchert 1994; Bouchet et al. 1995; Scoccimarro 1998; Crocce,
   Pueblas & Scoccimarro 2006), the `F₂` decomposition, interlacing (Sefusatti, Crocce,
   Scoccimarro & Couchman 2016), lognormal and rank-matched mocks, and the copula framing
   (Sklar 1959; Scherrer et al. 2010; Qin, Yu & Zhang 2020) are all standard and credited. The
   pilot's addendum already records that the LSS copula programme asked the qualitative
   question first.
5. **Redshift-space distortions, survey geometry, mask and selection are absent.** All four are
   filters, and §2 is about filters. Their omission makes this forecast optimistic in a way
   that is **not** quantified here.
6. **The `A`/`M`/`GAP` decomposition is post-hoc.** It was added after the first sweep. It is
   arithmetic (`A − M = GAP` identically), not a new statistic, but it was not pre-registered
   and neither was §4's unfiltered measurement.
7. **Six realisations.** Every `σ` carries ~30 % uncertainty; the Poisson gate has three.

---

## 10. ADDENDUM — the smoothed sector run, one control that matters and one caveat that bites

Added after §1–§9 were written, when the pre-registered `sectors` job finished.
`N = 384`, `L = 1920`, 4 realisations, floor = rank-matched F2. All `z` are paired.

### 10.1 The control that matters: the pointwise sector's GAP is ZERO

`R = 40` Mpc/h, `E − E_F2` (i.e. the GAP), by sector:

| geometry | **LOCAL** (pointwise) | SHIFT | TIDAL | full SPT2 | 2LPT |
|---|---|---|---|---|---|
| equilateral | **`−7.8e-05` (−0.15)** | `6.51e-03` (+15.4) | `3.55e-03` (+16.1) | `2.55e-03` (+14.6) | `2.45e-03` (+12.9) |
| folded | **`1.17e-03` (+1.49)** | `−6.68e-03` (−6.0) | `−4.51e-03` (−15.8) | `−1.48e-03` (−2.8) | `−1.65e-03` (−2.6) |
| squeezed | **`1.16e-04` (+0.47)** | `2.08e-03` (+10.8) | `1.25e-03` (+9.8) | `8.08e-04` (+8.6) | `7.66e-04` (+6.9) |

**The LOCAL sector — `δ₁ + (17/21)δ₁²`, gravity's own pointwise term — reads the same as the
rank-matched pointwise floor, at `|z| ≤ 1.5` in all three geometries**, while the SHIFT and
TIDAL sectors read it at `z = 6–16`. This is the internal control the whole design needed:
the floor correctly absorbs a pointwise field carrying gravity's own local sector, so
**gravity's GAP is driven by the non-pointwise sectors and not by a mismatch in the pointwise
one.** It also means **F4, which fired on the *unfiltered* LOCAL reading (§7), survives in the
form that the measurement actually uses.** The full field's GAP is *smaller* than either
sector's because SHIFT and TIDAL partially cancel against LOCAL. At `R = 100` every sector is
consistent with zero, matching §3.

### 10.2 The caveat that bites: a purely Gaussian field also has a large GAP

At `R = 40`, equilateral, the **linear Gaussian field** — whose whole-only share is *exactly
zero* by theorem — reads `E_LIN − E_F0 = −2.6e-05` (`z = −1.2`, correctly zero) but
`E_LIN − E_F2 = 3.11e-03` at **`z = +14.4`**, which is **larger than gravity's own GAP of
`2.45e-03`**.

This is not a contradiction; it is arithmetic (`LIN − F2 = −M`, since LIN reads the same as
F0). But it makes explicit something §2 only implied, and it is the most important caveat in
this document:

> **`GAP ≠ 0` is a TWO-SIDED test.** It fires when a field has *more* non-pointwise structure
> than the model, and equally when it has *less pointwise* structure than the model. On its
> own, a nonzero GAP is **not** evidence that the field carries whole-only pattern — a
> Gaussian field passes it, and passes it more strongly than gravity does.

What separates the two cases is §10.1: gravity's GAP is accompanied by a LOCAL sector that
matches the floor, so gravity is the first case, not the second. **A real-data
pre-registration must carry that control**, or the measurement means much less than its
significance suggests. Restated in the direction that matters: through this pipeline,
**gravity's departure from the exact-zero reference is ~14× smaller than a pointwise mock's**
(`|A| = 5.7e-04` vs `|M| = 7.8e-03` at `R = 10`). What a survey would be detecting is largely
that *the sky is less like a filtered lognormal than a filtered lognormal is*.

---

## 11. SECOND ADDENDUM — the growth test, and the sharpest result in this document

The pre-registered `growth` job (F3) finished last. It re-runs the small box at `D = 0.6`
(`z ≈ 1`) against `D = 1.0`, same construction, 3 realisations. `σ_R` tracks `D` correctly
(measured ratio 0.62–0.63 against `D` ratio 0.600), so the mock scaled as intended.

Median ratio `X(D=0.6)/X(D=1.0)` over the configurations where `X` is significant at `D = 1`:

| quantity | median ratio | `d log X / d log D` | prereg F3 staked |
|---|---|---|---|
| **`A`** — gravity vs the exact-zero Gaussian | 0.656 (n=8) | **+0.82** | 1.0 |
| `M` — what the floor's filter manufactures | 0.908 (n=10) | +0.19 | — |
| **`GAP`** — gravity vs the pointwise floor | 0.939 (n=10) | **+0.12** | 1.0 |

**Gravity's own excess scales with the growth factor. The GAP does not.**

`A` behaves exactly as gravity should — grow the structure, grow the signal, exponent
`+0.82` against a staked 1.0. **F3 survives for `A`.** But the GAP is essentially unchanged
when the amount of gravitational evolution is cut by 40 %: exponent `+0.12`, inherited from
`M`, which is also nearly `D`-independent because the rank map is re-matched to whichever
one-point law the field has.

This is the cleanest statement of what §2, §10.2 and this section have been converging on,
and it is a *fired* prediction, not a survival:

> **The GAP is not a measurement of gravity.** A quantity that measured gravitational
> structure would scale with the growth factor. This one does not. Three independent
> demonstrations now say the same thing: 93 % of it is the floor's manufactured term (§2a); a
> Gaussian field produces a *larger* GAP than gravity does (§10.2); and it is blind to the
> growth factor (here).

**What the GAP does measure** is well-posed and still worth something: *is this field a
filtered pointwise transform of a Gaussian at this `P(k)` and this one-point law?* That is the
copula question of Scherrer et al. (2010) and Qin, Yu & Zhang (2020), sharpened to the
pair-envelope null and made filter-aware. A survey could answer it at `z ≈ 67`. It is simply
not the same question as *does gravitational clustering carry whole-only pattern*.

**What answers that question** is `A` — which scales with `D`, is largest in the folded
configuration where the tidal kernel peaks, and reaches `z = 18–30` — together with §4's
unfiltered reading, where the pointwise family is exactly zero by theorem and gravity's tidal
sector reads `z = +28`. Those two, not the GAP, carry the `wild-share` stake.

### Consequence for the verdict, stated as a correction to my own pre-registration

The trichotomy in `SKY_FORECAST_PREREG.md` §6 made outcome (a) turn on `z_s ≥ 5` **for the
GAP**, and attached to it the interpretive payoff that `wild-share` would get its first
decidable instance. **The numerical criterion is met with 20–200× margin, and the
interpretive attachment was wrong**: a 5σ GAP does not decide `wild-share`, because a Gaussian
field would also produce one. I wrote that criterion before seeing that `M` would dominate
`A`, and it is recorded here as a mis-specified pre-registration rather than quietly
re-interpreted. House rule 7 cuts this way whether the error is in the result or in the design.

The verdict in §8 stands as to **detectability**, and its condition (1) — that the detection
would rest on the floor model rather than on gravity — is now the whole of it rather than a
caveat.

---

## 12. THIRD ADDENDUM — the shot-noise gate, properly powered: THE VALVE OPENS

`sky_forecast_shotnoise.py`, **10 realisations** against the pre-registered gate's 3, run
after `Core/Valve.lean` landed. Same box as the small-scale sweep (`N = 384`, `L = 768`), so
the numbers are directly comparable to the GAP. §5's run is left exactly as it was executed.

`Valve.lean` proves that a per-cell **stochastic** channel returns a product state from a
product state (share exactly 0, never from nothing), but on a state that already carries
**pair structure** it can mint whole-only share. Poisson sampling is such a channel and the
field is such a state, so this is the valve configuration, and it had to be measured rather
than bounded.

### 12.1 F7 survives — and my pre-registered run was a power failure, not a null

Paired shift `mean[E(n̄) − E(∞)]`, base **F0** (correlated, share exactly zero), `R = 10`:

| `n̄` (h/Mpc)³ | equilateral | folded | squeezed |
|---|---|---|---|
| `1e-2` | `−3.70e-03` (−23.4) | `+3.73e-03` (+20.1) | `−1.20e-03` (−19.1) |
| `1e-3` | `−4.90e-03` (−12.7) | `+6.04e-03` (+23.5) | `−1.62e-03` (−12.6) |
| **`1e-4`** | **`−1.10e-02` (−22.0)** | **`+1.45e-02` (+31.4)** | **`−3.54e-03` (−22.0)** |

**Monotone rise as `n̄` falls, at `t = 12–31`.** That is exactly prediction F7. §5 reported "no
monotone trend over two decades" from three realisations; **that was under-power, and it is
retracted here.** House rule 7 applies to my own null as much as to my own survival.

### 12.2 The number that hurts

| `n̄` | manufactured `|ΔE|` | as a fraction of the GAP (`8.41e-03`) |
|---|---|---|
| `1e-2` | `3.70e-03` | **44 %** |
| `1e-3` | `4.90e-03` | **58 %** |
| **`1e-4` (DESI-like)** | **`1.10e-02`** | **130 %** |

**At DESI-like number density, Poisson sampling alone manufactures more whole-only sign-triple
excess than the entire deliverable GAP**, on a field whose true share is exactly zero.

### 12.3 It does not fully cancel when the floor is sampled the same way

Forward-modelling means sampling the floor at the same `n̄`. The residual,
`[E_2LPT(n̄) − E_2LPT(∞)] − [E_F0(n̄) − E_F0(∞)]`, paired:

| `R` | `n̄` | equilateral | folded | squeezed |
|---|---|---|---|---|
| 10 | `1e-4` | `−2.22e-03` (−8.6) | `−5.29e-03` (−11.3) | `−6.33e-04` (−4.5) |
| 10 | `1e-2` | `+3.24e-03` (+17.2) | `−3.30e-03` (−12.4) | `+1.02e-03` (+12.0) |
| 25 | `1e-4` | `+2.49e-03` (+1.7) | `−2.36e-03` (−2.5) | `+1.06e-03` (+2.0) |

Most of it cancels — but **the residual is still 26 % (equilateral) to 136 % (folded) of the
GAP at `R = 10`, and it is detected at `t = 4.5–11.3`.** Gravity and a Gaussian do not respond
identically to being Poisson-sampled, so a matched forward model reduces this systematic by
roughly 5× and does not remove it.

### 12.4 The valve signature, isolated

Comparing the correlated base with the **product-state** base, where the theorem says a
per-cell channel cannot mint:

| `R` | F0 (pair-structured) | WHITE (product state) |
|---|---|---|
| 10 | max `|t|` = **31.4** | max `|t|` = **33.6** |
| 25 | max `|t|` = **11.0** | max `|t|` = **1.4** |

**At `R = 25` the effect requires pair structure** — the product-state arm is null at `t = 1.4`
while the correlated arm fires at `t = 11.0`. That is `Valve.lean`'s mechanism, isolated in a
cosmological pipeline. **At `R = 10` both fire**, because there the post-sampling *smoothing*
— a cross-cell filter, which no no-creation theorem covers — dominates over the per-cell
channel. So the two manufacturing mechanisms are separable by scale, and both are present.

---

## 13. FOURTH ADDENDUM — the kappa-edge dependency, measured rather than left pending

`sky_forecast_binmint.py`, **8 realisations**, committed before it was run. §"Scope, second
part" said I could not build this control. **That was wrong and this is the retraction.**

Bin the smoothed field into `b` **quantile** bins; build the exact `(b,b,b)` triple histogram;
IPF onto the pair marginals to get `q`, the fine-grained **pairwise-maxent** state, which
carries all the field's fine pair structure and **no order-3 content**; then merge the lower
`b/2` and upper `b/2` bins — which, because the bins are quantile bins, **is exactly the
median split**. Any nonzero `b = 2` excess in the merged state is manufactured by the
coarse-graining alone. Worst IPF certificate `|share_H − share_KL|` anywhere: **`2.0e-11`**.

**The mechanism is real on gravity.** `E_manuf = 1.01e-03` at `t = 4.29` (`R = 10`,
equilateral), **converged in `b`**: `9.6e-04, 1.02e-03, 1.02e-03, 1.01e-03` for
`b = 4, 8, 16, 32`. So the median split does mint `b = 2` excess out of two-point structure —
`kappa-edge`'s hypothesis, confirmed on my own fields at my own resolution.

**But the gate is not clean and I will not overclaim it.** The two theorem-pinned arms must
read zero in the ensemble — F0 because a Gaussian's quantile binning is sign-symmetric, F2
because quantile bins are transform-invariant so a monotone map of a Gaussian has *its parent's*
fine histogram. They read max `|t| = 2.80` and `3.36` over six configurations. Gravity's
`4.29` sits above that pedestal but not far above it. **The mechanism is detected; its
amplitude is at the edge of this run's power.**

**What it does to the deliverable** — subtracting from each arm what its own fine pair
structure forces, `GAP_corr = [E_2LPT − E_manuf(2LPT)] − [E_F2 − E_manuf(F2)]`:

| `R` | geometry | `GAP_raw` | `GAP_corr` | surviving | `t_corr` |
|---|---|---|---|---|---|
| **10** | equilateral | `8.19e-03` | `7.01e-03` | **86 %** | **20.5** |
| **10** | folded | `−3.89e-03` | `−3.91e-03` | **100 %** | **−13.7** |
| **10** | squeezed | `2.45e-03` | `2.33e-03` | **95 %** | **17.2** |
| 25 | equilateral | `1.72e-03` | `6.62e-04` | 38 % | **0.53** |
| 25 | folded | `−2.64e-03` | `−3.17e-03` | 120 % | −2.80 |
| 25 | squeezed | `6.22e-04` | `4.32e-04` | 70 % | **0.94** |

**`R = 10` survives the control almost intact (86–100 %, `t = 13.7–20.5`). `R = 25` does
not** — two of three geometries fall below `t = 1`. **The `R = 25` row of §3's forecast table
is withdrawn.**

---

## 14. FILES

| | |
|---|---|
| `SKY_FORECAST_PREREG.md` | pre-registration, committed at `b89ce48` before any code |
| `sky_forecast.py` | 2LPT + CIC, Eulerian SPT2 with the `F₂` sector split, three floors, the `b=2` instrument, gates |
| `sky_forecast_unfiltered.py` | §4, the unfiltered reading (added after the sweep) |
| `sky_forecast_analyze.py` | the `A`/`M`/`GAP` decomposition and the tables |
| `sky_forecast_shotnoise.py` | §12, the powered valve/shot-noise gate (10 realisations) |
| `sky_forecast_binmint.py` | §13, the fine-`b` pair-maxent surrogate — the `kappa-edge` control |
| `sky_forecast_{gate,sweep,sectors,growth,poisson,unfiltered_L1920,shotnoise,binmint,binmint_b}.json` | raw results |
| `sky_forecast_*.log` | run logs, including the failing gates |

Seeds: gate 20260726, small sweep 20260801, large sweep 20260802, sectors 20260803, unfiltered
20260805, Poisson 20260901, shot-noise 20261001, binmint 20261101 and 20261205. Research → scratchpad memo → Eric's review. Nothing pushed.
