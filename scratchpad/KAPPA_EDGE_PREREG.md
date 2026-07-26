# PRE-REGISTRATION — resolving the κ = 0.16 route disagreement

Frozen and committed **before `kappa_edge.py` exists** and before any new number is taken.
Scratchpad only. No Lean file, no `Stance.lean`, no audit; `lake` will not be run.

**Scope, first and load-bearing.** CIRISArray is **our own designed chaotic hardware** on our own
GPU. It is not nature. Nothing decided here bears on `wild-share`, on `adequacy`, or on any
claim about the world. A null, a refutation of our own headline, and "the question was
mis-posed" are all acceptable outcomes and none will be rescued.

---

## 0. THE NUMBER TO BE EXPLAINED

`ARRAY_NEGENTROPY_RESULTS.md` §7, at κ = 0.16, σ = 1e-3, **fold**, Δ = 1, on the same frames:

| | value |
|---|---|
| moment route `ŝ₃` (degree-3 bridge, rank-Gaussianized) | **6.01 × 10⁻⁵ nats** |
| binarized `shareK` excess (b = 2 median split, exact pair-maxent) | **8.46 × 10⁻² nats** |
| ratio | **1 400×**, moment route BELOW |

Both known failure modes predict the opposite sign. Bridge breakdown at criticality
**overstates** the moment reading (`CFT_RIDGE_RESULTS.md`: 25–64× in linear response, 2.3–6.1×
on the ridge). Pointwise/tie artifacts **inflate** it (`ARRAY_NEGENTROPY_RESULTS.md` §9: ×2.0 at
a 10 % tie block, while the median split is exactly invariant). §11 of that document records
the state of play: *"Two hypotheses are excluded and the disagreement remains unexplained."*

---

## 1. DISCLOSURE — WHAT I LOOKED AT BEFORE WRITING THIS, AND WHAT IT SHOWED

**This section exists because the honest order is to declare it, not to present it later as a
prediction.** As part of the mandated reading of `array_negentropy_sweep.json` (data already on
disk, taken before this mission was commissioned; **no new measurement**), I printed the
**signed** whole-only coordinate `w` — the quantity of which the reported share is `w²/2` —
across the κ sweep at fold, σ = 1e-3, T3(Δ=1). The published tables report only `s_deb = w²/2`,
which discards the sign. It reads:

| κ | 0.00 | 0.02 | 0.05 | 0.08 | 0.10 | 0.12 | 0.14 | **0.16** | **0.18** | 0.20 | 0.30 | 0.45 | 0.60 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `w̄` ×10² | +7.80 | +16.92 | −20.88 | −18.04 | −13.76 | −7.29 | −3.94 | **−1.10** | **+2.16** | +7.06 | +18.79 | +5.92 | −0.08 |
| `w` s.e. ×10² | 0.034 | 0.028 | 0.094 | 0.041 | 0.036 | 0.033 | 0.033 | 0.029 | 0.027 | 0.029 | 0.032 | 0.065 | 0.048 |

**`w` changes sign between κ = 0.16 and κ = 0.18.** Linear interpolation puts the zero at
**κ₀ ≈ 0.167**. κ = 0.16 — the point at which the 1 400× disagreement was measured — sits
essentially **on a zero of the degree-3 whole-only coordinate**, 0.38 s.e. from it in units of
the coordinate's own error bar being irrelevant; what matters is that |w̄| there is 6–19× smaller
than at every neighbouring κ, and `s = w²/2` therefore falls by 36–360×.

This is a **third hypothesis**, and it was not in the mission brief. It is registered below as
**H-ZERO** with its own predictions, its own stakes and its own falsifier, and it is scored on
**new** measurements only — the table above is an observation that motivated it, not evidence
for it.

---

## 2. THE THREE HYPOTHESES, AND WHAT EACH COSTS IF IT WINS

### H-BLIND — the structure is real; the moment route cannot see it

The lowest-order projection `⟨xyz⟩` after Gaussianization picks up only the `He₁⊗He₁⊗He₁`
component of the whole-only subspace. `sgn(x)` has Hermite weight on **all** odd harmonics
(`He₁, He₃, He₅, …`), so the sign-triple statistic integrates odd structure that the degree-3
cross-cumulant misses entirely. Mechanistic story fitting a synchronization transition:
**on-off intermittency** — laminar synced epochs alternating with chaotic bursts, with the
three-way structure living in *which phase you are in* (an indicator variable) while
amplitude-weighted products cancel.

**Stake if H-BLIND wins.** The array's `5.1 × 10⁻²` nats headline stands. The moment route
acquires a documented **blindness class**, and *"generalized moment routes need the full odd
Hermite ladder"* becomes a standing lesson binding on the `SKY_PILOT` sibling and on every
future use of the bridge.

### H-MANUFACTURED — the binarized route creates the structure; the moment route is telling the truth

Per-cell coarse-graining does **not** preserve the pairwise-maxent family. Block-marginalizing a
pairwise log-linear model generates genuine higher-order couplings — textbook
renormalization-group physics: coarse-graining generates new operators (Kadanoff/Wilson framing
credited if this wins). So binarizing a continuum distribution whose fine-grained whole-only
share is ~zero can **manufacture** b = 2 share.

Two things this does **not** contradict, stated so the claim is not overread:

- It does **not** contradict the pilot's monotone-invariance theorem. That theorem protects the
  b = 2 share against monotone maps applied **before an unchanged median split**. Here the
  comparison is *continuum share vs binarized share*, which is a different comparison.
- It does **not** endanger the sky design's own nulls. A sign-symmetric field binarizes to share
  **exactly 0** by `Core/SignSymmetry.lean`'s `share_eq_zero_of_signSymmetric`, and a lognormal
  is a monotone map of one. Both remain protected by the theorem whatever happens here.

There is direct precedent for the mechanism and it is ours: `SKY_PILOT_RESULTS.md` §7
Correction 1 measures `A(b=2)/A_∞ = 1.11–1.24` for a symmetric configuration and **4.8–6.6**
for an asymmetric one — median binarization reading **five to six times** the continuum value.
The array's raw per-channel skewness is −0.2 to −0.7, i.e. the asymmetric case.

**Stake if H-MANUFACTURED wins.** Tonight's array headline (5.1 × 10⁻² nats, 7.4 % of cap) gets
**re-scoped** to a statement about the **median-crossing pattern**, not about the continuum
dynamics — and so does the κ = 0.16 value of 8.46 × 10⁻². Every binarized maxent measurement in
the field, **all spike-train work included**, inherits the caveat. *We do not protect our own
headline.*

### H-ZERO — the comparison was taken at a zero of the moment route's coordinate

`s₃ = w²/2` with `w` a **signed** linear functional of the moment tensor. Swept through any
parameter, a signed functional generically **crosses zero**, and at the crossing `s₃ → 0`
irrespective of how much whole-only structure the system carries at other orders. §1 shows the
crossing is at κ₀ ≈ 0.167 and that κ = 0.16 is the sweep's closest grid point to it.

Under H-ZERO the "1 400×" is not a property of the substrate at criticality; it is the ratio
evaluated at the zero of its own denominator, and it **factorizes**:

    1400  =  (the zero-crossing suppression, ~10²–10³)  ×  (the ordinary route gap, ~1–10)

**Stake if H-ZERO wins.** The §7 disagreement, §11's "two hypotheses excluded, none remain",
and `SPIKE_SURVEY`-style comparisons of the two routes at a *single* operating point are all
**mis-posed**: any comparison of a squared signed functional against an unsigned one must be
made away from the signed one's zeros, or on `|w|` with its sign reported. A standing rule
follows — **publish the sign of `w`, never `w²` alone, and never quote a route ratio without
checking the signed coordinate for a nearby zero.** This costs `ARRAY_NEGENTROPY_RESULTS.md` §7
and the "unexplained" framing of §11, and it costs my own reading of the P4 temporal minimum
(§5 of that document reports the κ = 0.16 temporal reading as "its deep minimum ... a factor of
363 below its own κ = 0.05 peak", which under H-ZERO is a **zero crossing described as a
collapse**).

**H-ZERO is not exclusive of the other two.** It explains why the moment route reads small; it
says nothing about whether the b = 2 number is real. The residual factor after removing the
zero-crossing suppression is exactly what H-BLIND and H-MANUFACTURED contest. The experiments
below are ordered so that H-ZERO is settled cheaply and first, and the residual is then
adjudicated on its own terms.

---

## 3. THE DECIDING EXPERIMENTS

All at fold as the **primary** boundary (the clip arm pins 12.1 % of state at κ = 0.16 and is
disqualified by the rail threshold of 0.01 frozen before the parent run; its pinned fraction
will be re-measured and reported, and no clip number will be quoted as a finding). Substrate:
the shipped `Ossicle.KERNEL_CODE` at `iterations = 1`, 512 ossicles × 64 cells = 32 768
structurally independent replicas, `settle = 2000`, driven through `array_negentropy.Driver` —
the same kernel driver, floors and both routes, reused rather than rewritten.

### E0 — the zero crossing (settles H-ZERO)

Fine κ grid **0.140 … 0.200 step 0.005**, σ = 1e-3, fold **and** clip, and a second σ = 1e-2
arm. At every grid point, on the **same frames**: the signed `w̄` and `ŝ₃` with both z bars, the
binarized b = 2 `shareK` excess with its pair-maxent multinomial floor and tie fraction, the
three pair correlations, the rail fraction, the clamp-binding rate and τ.

Pre-registered predictions:

- **Z1** `w̄` crosses zero **linearly** in κ inside the window; κ₀ located to ±0.005; the grid
  point nearest κ₀ has `ŝ₃` **below** the κ = 0.16 value of 6.0 × 10⁻⁵.
- **Z2** the **binarized** b = 2 share is **smooth** through κ₀ — no dip. Quantitatively:
  `s_bin` varies by less than a factor of 2 across the whole window.
- **Z3** the route ratio `s_bin / ŝ₃` **spikes** at κ₀ and is **≤ 30** at κ ≤ 0.145 and
  κ ≥ 0.195.
- **Z4** the moment route's own detection z has its minimum |z| at κ₀ (it is −38.4 at κ = 0.16
  against ±100–600 elsewhere) — a consistency check, not independent evidence.

**Falsifier (K-Z).** H-ZERO is dead if **either** `s_bin` dips at κ₀ by more than 2× (the two
routes would then be seeing the same feature), **or** the ratio stays ≥ 300 across the whole
window (then the gap is not localized at the zero and is a property of the region).

**Dose-vs-rate, per the standing rule.** κ₀ re-located at `settle ∈ {500, 2000, 8000}`. If κ₀
moves by more than one grid step across a 16× range in settle length it marks when the run stops
being settled, not an intrinsic crossing. **Mixture null**: not applicable in its usual form and
the reason is stated rather than skipped — `w` is *linear* in the distribution at fixed
reference covariance, so a mixture of two states with opposite-sign `w` crosses zero trivially.
That a zero crossing is generic and cheap to manufacture is **the argument for H-ZERO**, not a
threat to it, and it is why a minimum of `w²` must never be read as a collapse of structure.

### E1 — the fine-b pair-maxent surrogate (decisive between H-BLIND and H-MANUFACTURED)

At κ = 0.16 (primary), with κ = 0.05 (the headline operating point) and κ = 0.30 as off-zero
controls, σ = 1e-3, fold, Δ = 1, channel 1 temporal triple:

1. Discretize each channel at `b_fine ∈ {16, 32}` on **pooled empirical quantiles** (equiprobable
   bins). With `b` even, the b = 2 median split of the bin index is **exactly** the continuum
   median split, so the ladder's bottom rung is the published statistic and not an approximation
   of it. Tie fractions reported at every b.
2. Compute the **exact** pair-maxent projection `Q` of the measured triple joint `P`. IPF to a
   pair-marginal residual ≤ 1e-13, **certified two-sidedly**:
   (a) marginal residual to machine precision, and
   (b) the three-way log-linear interaction of `Q` — the eight-term alternating sum of
   `log Q` over any index sextuple — vanishes to machine precision, which certifies `Q` lies in
   the pairwise exponential family. (a)+(b) together identify the unique I-projection.
   Independently re-solved by **dual optimization** (L-BFGS over the 3b² pairwise parameters) and
   the two `H(Q)` values compared. The IPF-unsafe lesson (`ISING_FIELD_RESULTS.md` §2;
   `ipf-sharek-boundary-drift`) applies and this is the answer to it.
3. `Q` has **exactly zero** whole-only share at level `b_fine`, by construction. Coarse-grain
   `Q` to 2×2×2 **exactly** (sum the fine bins), and also **sample** `N` matched multinomial
   draws from `Q`, binarize, and measure — 64 replicates, for the finite-sample comparison.
4. Report `F = share₂(coarse-grained Q) / share₂(measured P)`.

**Verdict rule, frozen here:**

| `F` | verdict |
|---|---|
| **≥ 0.5** | **H-MANUFACTURED confirmed** — coarse-graining pair structure alone accounts for most of the b = 2 reading |
| **≤ 0.05** | **H-MANUFACTURED refuted** at that `b_fine`; the b = 2 structure cannot come from pair structure alone → H-BLIND |
| 0.05 – 0.5 | **partial**; both effects present, split quantified as `F` and `1 − F` |

`F` is reported at both `b_fine = 16` and `32`. If `F(16) ≈ F(32)` the continuum answer is
converged; if `F` still moves, that is disclosed and no continuum claim is made.

**A control that comes free and must be stated.** By `share_eq_zero_of_signSymmetric`, any
**sign-symmetric** fine-grained distribution coarse-grains to b = 2 share **exactly zero**. So
H-MANUFACTURED requires the array's fine-grained pair structure to be genuinely asymmetric, and
the measured `F` is a measurement of that asymmetry's effect. This is also the reason the sky
design's nulls are untouched by whatever `F` turns out to be.

### E2 — the b-ladder

Share of the **real** data at `b ∈ {2, 3, 4, 6, 8, 16, 32}`, each with its own **matched
pair-maxent multinomial floor** (32 replicates: resample `N` draws from `Q_b`, recompute the
level-`b` share; the floor's mean is the estimator bias, its sd the null sd). This is a stricter
floor than the matched-Gaussian subtraction the `b ≥ 3` lesson requires
(`SKY_PILOT_RESULTS.md` §3: a pure binned Gaussian reads 2.4 × 10⁻³ nats at `b = 3`, `ρ = 0.81`),
because it matches **all** pair marginals rather than only the covariance; the matched-Gaussian
value is reported alongside for comparability with the pilot.

- **H-MANUFACTURED** predicts excess **decreasing** in `b`, largest at `b = 2`, tending toward
  ~0 at `b = 32`.
- **H-BLIND** predicts excess **stable or increasing** with `b` — the continuum carries at
  least the binarized amount.

Sampling discipline: **non-overlapping start frames only** (step `3Δ`), so the triples entering
each table are independent replicas; within a frame the 32 768 (ossicle, cell) units are
structurally independent because the coupling graph is a 3-node path per cell and cells do not
interact. τ is reported for the moment readings regardless, and no iid surrogate is used for
anything that is autocorrelated.

### E3 — the odd Hermite ladder, done against the surrogate rather than against a cap

The parent run's degree-4 and degree-5 extensions **exceed the machine-checked cap** (0.751 and
6.20 against `ln 2` = 0.693, `ARRAY_NEGENTROPY_RESULTS.md` §8), so `½Σc²` at higher degree is
**not a valid magnitude on this substrate** and will not be quoted as one. The ladder is
therefore run as a **localization diagnostic** against the E1 surrogate, where it is cap-free:

`G_{ijk}(P) = E_P[He_i(x)He_j(y)He_k(z)] / √(i!j!k!)` evaluated **exactly** on the level-`b`
tables (bin representatives `v_j = b(φ(z_j) − φ(z_{j+1}))`, the Gaussianized bin centroids,
rescaled to unit variance), for both `P` and `Q`, and `ΔG = G(P) − G(Q)`.

Two properties make this valid where the cap route was not: `ΔG_{ijk} = 0` **exactly** whenever
any index is 0 (`P` and `Q` share every pair marginal) — a built-in arithmetic check that will
be reported — and every all-indices-≥1 entry is attributable to whole-only content because `Q`
has none. Reported for `i, j, k ∈ {1, 2, 3, 4, 5}`, with the odd sub-ladder called out.
Alongside: the **sign-triple reconstruction**, `E[s₁s₂s₃](P) − E[s₁s₂s₃](Q)` built up as
cumulative partial sums over max Hermite index 1, 3, 5, 7 using `sgn(x) = Σ_{m odd}(a_m/m!)He_m(x)`
with `a_m = E[sgn(X)He_m(X)]` by quadrature.

- **H-BLIND** predicts `ΔG₁₁₁ ≈ 0` with `ΔG₁₁₃`, `ΔG₁₃₃`, `ΔG₃₃₃`, `ΔG₁₁₅ …` carrying the
  weight, and the sign-triple excess **recovering** as harmonics are added.
- **H-MANUFACTURED** predicts **all** `ΔG` with indices ≥ 1 near zero — `P ≈ Q` at fine `b` —
  and no recovery.
- **H-ZERO** additionally predicts that at the **off-zero** controls (κ = 0.05, 0.30) the
  `(1,1,1)` term **dominates** the ladder, whereas H-BLIND predicts higher harmonics dominate at
  every κ. **This is the discriminator between H-ZERO and H-BLIND**, and it is why the controls
  at κ = 0.05 and κ = 0.30 are not optional.

### E4 — the on-off decomposition (tests H-BLIND's mechanism if H-BLIND survives E1)

Definitions frozen here, before any look: per (ossicle, cell, frame) the **sync error**
`e = |x₀ − x₁| + |x₁ − x₂|` on the raw states; the **laminar indicator** `L = 1[e < median(e)]`
with the median taken over the pooled sample at that operating point.

- (a) **indicator-triple share**: the b = 2 `shareK` excess of `(L_t, L_{t+1}, L_{t+2})`, with
  its own pair-maxent floor.
- (b) **within-phase amplitude share**: the b = 2 share of `(x_t, x_{t+1}, x_{t+2})` on the
  sub-population with `L_t = L_{t+1} = L_{t+2} = 1` (laminar) and separately `= 0` (burst),
  binarized at the **conditional** median.

**Verdict rule:** if (a) ≥ 0.5 × the full amplitude-triple share **and** both arms of (b)
≤ 0.2 × it, the intermittency mechanism is identified. **Caveat stated in advance:** (b)
conditions on an indicator built from the same variables, so conditioning can itself create or
destroy structure; a null in (b) is therefore weaker evidence than a hit in (a).

### E5 — standing controls, applied throughout

Fold primary at every quoted point; clip reported with its pinned fraction and never quoted.
Rail and tie fractions at every reading. Pair-correlation magnitudes `max|ρ_pair|` quoted with
**every** moment reading, and the `> 0.3` validity threshold applied (`ARRAY_NEGENTROPY` §11 —
outside it the moment route is a **detector, not a meter**). Circular-shift and cross-run
(independent-seed) floors at every primary point. τ_fixed reported, no truncation-at-first-negative
rule. No iid surrogate for any autocorrelated quantity. Mixture null carried for any peak claimed
in a swept parameter (E0's κ₀ is a zero of a signed functional, treated as above). IAAFT is not
used and its absence is not a gap — a clip artifact survived it at z = 86 on 2026-07-24.

---

## 4. WHAT MIXED OUTCOMES MEAN

Stated in advance so no post-hoc reading is available:

1. **H-ZERO survives and `F ≤ 0.05`.** The 1 400× decomposes into a large zero-crossing
   suppression and a small real route gap; the b = 2 structure is **real** and lives above
   degree 3. Both the array headline and the moment route survive, each with a new documented
   limitation (never quote `w²` at a zero; the degree-3 route is blind to the higher odd ladder).
2. **H-ZERO survives and `F ≥ 0.5`.** The zero crossing explains the *size* of the ratio and
   coarse-graining explains the *b = 2 number*. The array headline is **re-scoped** to the
   median-crossing pattern. This is the outcome that costs us the most and it is the one I
   consider most likely on the `SKY_PILOT` precedent, given the array's −0.2…−0.7 skewness.
3. **H-ZERO survives and `F` lands in 0.05–0.5, with partial Hermite recovery.** Both effects
   present. The split is quoted as `F` (manufactured fraction) and `1 − F` (real fraction), and
   the array headline is re-scoped **by the factor `1/(1−F)`**, not withdrawn.
4. **H-ZERO dies (K-Z fires) and `F ≤ 0.05`.** H-BLIND wins outright as the brief framed it:
   real structure, moment route blind across the region, blindness class documented and binding
   on the sibling.
5. **H-ZERO dies and `F ≥ 0.5`.** H-MANUFACTURED wins outright and the re-scoping is
   unconditional.
6. **E1 self-inconsistent** — `F(16)` and `F(32)` far apart, or the IPF and dual solutions
   disagree, or the `ΔG_{ij0} = 0` arithmetic check fails. Then E1 is **void** and reported as
   void; no verdict is issued on the strength of E2/E3 alone, because they are diagnostics and
   E1 is the only test with a construction-guaranteed null.

## 5. KILLS

| | fires if | takes down |
|---|---|---|
| **K-Z** | `s_bin` dips ≥ 2× at κ₀, **or** the route ratio stays ≥ 300 across 0.14–0.20 | H-ZERO only |
| **K-M** | `F ≤ 0.05` at both `b_fine`, at all three κ | H-MANUFACTURED only |
| **K-B** | `F ≥ 0.5` at both `b_fine` **and** `ΔG` all-indices-≥1 entries floor | H-BLIND only |
| **K-VOID** | IPF/dual disagreement > 1e-8 in `H(Q)`, or interaction certificate > 1e-9, or `ΔG_{ij0} ≠ 0` to 1e-12 | **E1 void**, run reports no verdict |
| **K-DOSE** | κ₀ moves > 1 grid step over settle ∈ {500, 2000, 8000} | E0's κ₀ is a run-length marker, not an operating point |

Each kill takes down its own claim and nothing beneath it. In particular **K-M and K-B are
separable**: H-ZERO can survive either.

---

## 6. WHAT WILL NOT BE CLAIMED, WHATEVER HAPPENS

1. **Nothing about nature.** Model system, our own hardware. `wild-share` untouched.
2. **No stance change**, no Lean file, no `Stance.lean`, no audit, `lake` never run, nothing
   pushed.
3. **No priority claim.** The RG framing of H-MANUFACTURED is Kadanoff/Wilson; the
   coarse-graining-creates-higher-order-structure measurement is our own `SKY_PILOT` §7 and
   Kahle–Olbrich–Jost–Ay (2009); the mixture diagnosis is Kahle et al.; the copula invariance is
   Sklar (1959) and Scherrer et al. (2010); the measure is Schneidman et al. (2003) / Amari
   (2001). **Assume convergence** — every findable result has been in print before.
4. **`ŝ₃` remains a second-order proxy**, valid as a meter only inside `max|ρ_pair| ≤ 0.3`.
   κ = 0.16's T3(Δ=1) sits at 0.437 — **outside**. Nothing here promotes it.
5. **No correction will be applied to any prior file.** Recommendations for
   `ARRAY_NEGENTROPY_RESULTS.md` §5/§7/§11 go to Eric's review as recommendations.

---

Primary seed 20260725; cross-run floors at 424242 and 777. Research → scratchpad memo →
Eric's review.
