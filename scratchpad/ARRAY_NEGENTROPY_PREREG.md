# PRE-REGISTRATION — the moment-native (negentropy-route) whole-only instrument, on CIRISArray

Frozen and committed **before** `array_negentropy.py` existed and before any array number was
computed. Scratchpad only: no Lean file, no `Stance.lean`, no audit; `lake` is never run.

---

## 0. SCOPE, FIRST AND LOAD-BEARING

CIRISArray is **our own hardware**: a designed, coupled-logistic chaotic substrate we built.
It is not nature. **Nothing in this experiment bears on the `wild-share` open claim**, on
`adequacy`, or on any claim about the world. A clean null is an acceptable and complete
outcome and will not be rescued.

What this run *is*: a change of instrument. Every previous array campaign
(`ARRAY_CAP_RESULTS.md`, `HABIT_DYNAMICS_RESULTS.md`) measured the whole-only share by
**median-binarizing** the continuous readout and running a discrete maxent (IPF) estimator.
This run measures the same quantity **without binning, without binarizing, without entropy
estimation, and without IPF**, from third joint moments alone, and then uses that instrument
to look for the array's operating point of maximal *boundary-stable* whole-only structure.

---

## 1. THE QUANTITY, AND WHY A MOMENT CAN MEASURE IT

The whole-only share at order 3 for continuous `X = (X₁,X₂,X₃)` is

    I_C⁽³⁾(p) = sup{ H(q) : q carries p's three bivariate marginals } − H(p)

— the repository's `share` (`Core/Share.lean`), the connected information of order 3
(Schneidman, Still, Berry & Bialek 2003; Amari 2001).

### 1.1 The variational form (second order)

Write `p = φ_C(1+u)` with `φ_C` the Gaussian carrying `p`'s mean and covariance, and let
`W ⊂ L²(φ_C)` be the closed span of functions of **at most two** coordinates. Since `p` and
`φ_C` agree through order 2, `u ⟂ W`'s degree-≤2 part and

    H(p) = H(φ_C) − ½‖u‖² + O(u³),
    I_C⁽³⁾ = ½ ‖P_{W^⊥} u‖² + O(u³).                                              (2.2)

**The share is the squared length of the part of the state that no pair can see.** This is the
sibling `SKY_PILOT_PREREG.md` §2.1, derived there independently for the cosmological arm; the
same mathematics, shared as instructed. The negentropy framing is openly borrowed and
credited: Comon 1994; Hyvärinen & Oja 2000; the Edgeworth/projection-pursuit expansion of
Jones & Sibson 1987; tensor Hermites per McCullagh, *Tensor Methods in Statistics*, 1987.
**No priority is claimed for any of it.**

### 1.2 THE BRIDGE

Grade `L²(φ_C)` by Hermite degree. `W` is graded, `dim P₃ = 10`, the three pairs contribute
`3·4 − 3 = 9`, so `W^⊥ ∩ P₃` is **one-dimensional**, spanned by the tensor Hermite `h^{123}`.
With `A := C⁻¹` and `ζ_abc := cum(X_a,X_b,X_c)` (**including repeated indices**):

    ⟨u₃, h^{123}⟩ = A_{1a}A_{2b}A_{3c} ζ_abc,        ‖h^{123}‖² = perm(A),

    ┌─────────────────────────────────────────────────────────────────────────┐
    │  I_C⁽³⁾ = ½ · [ Σ_abc (C⁻¹)_{1a}(C⁻¹)_{2b}(C⁻¹)_{3c} ζ_abc ]² / perm(C⁻¹)│   (B)
    │           + O(ζ³)                                                        │
    └─────────────────────────────────────────────────────────────────────────┘

**The constant asked for in the brief is ½.** In the decorrelated limit `C = I`,
`perm(I) = 1` and (B) collapses to

    I_C⁽³⁾ ≈ ½ κ₁₁₁²,        κ₁₁₁ = E[x₁x₂x₃]  (zero-mean, unit-variance channels).

`κ₁₁₁` is **a mean of a product of three numbers**. No entropy estimate, no bin, no IPF, no
threshold.

### 1.3 The general estimator actually used (and why it is not just (B))

(B) is the degree-3 truncation. `W^⊥` also has directions at degree 4 and above: in the
tensor-Hermite basis `W^⊥` is spanned by `h^α` whose multi-index `α` has **all three indices
present**, so `dim(W^⊥ ∩ P_d)` is 1 at `d=3` (α = (1,1,1)), 3 at `d=4` ((2,1,1) and
permutations), 6 at `d=5`. The primary estimator is therefore stated at a truncation degree
`D` and computed basis-free:

    ŝ_D = ½ Σ_m ( E_p[e_m] − E_{φ_C}[e_m] )²

where `{e_m}` is an orthonormal basis of `W^⊥ ∩ P_D` in `L²(φ_C)`, built by Gram–Schmidt on
monomials with **exact** Gaussian moments (Isserlis). Every term is again a **sample moment
minus an analytic Gaussian moment**. `D = 3` is the primary (it *is* (B)); `D = 4` is the
pre-registered secondary.

**Why `D=4` is not optional.** Under the global flip `x → −x`, `h^α → (−1)^{|α|}h^α`, so a
jointly flip-symmetric distribution has **exactly zero** degree-3 whole-only content while its
degree-4 content may be large. `κ₁₁₁` is structurally blind to that class. Stated now so it
cannot be discovered later as a surprise: **a null at `D=3` is not a null on the share.**

### 1.4 THE INVARIANCE, AND WHY GAUSSIANIZATION IS LEGITIMATE

**Theorem (per-channel monotone invariance).** For strictly monotone `T₁,T₂,T₃` and
`Y_i = T_i(X_i)`, `I_C⁽³⁾(Y) = I_C⁽³⁾(X)` exactly, at every amplitude.

*Proof.* `T = T₁×T₂×T₃` acts coordinatewise, so `q` carries `p`'s pair marginals iff `T_*q`
carries `T_*p`'s: the constraint set maps bijectively. Differential entropy transforms as
`H(T_*q) = H(q) + Σ_i E_q[ln|T_i′|]`, and each correction depends only on the **one**-
dimensional marginals, which every member of the pair envelope shares. Supremum and state
entropy shift by the *same* constant; the difference is unchanged. ∎
(`SKY_PILOT_PREREG.md` §2.3; recorded here because the whole design rests on it.)

**Consequence.** Per-channel **rank-Gaussianization** — replace each channel by
`Φ⁻¹((rank − ½)/T)` — changes nothing about the quantity, because it is a per-channel monotone
map. It removes all marginal skewness and kurtosis from the estimator's path. And it does so
**exactly, not approximately, in the estimator too**: ranks are invariant under strictly
increasing maps, so the *entire pipeline* satisfies `pipeline(T(X)) ≡ pipeline(X)` bitwise for
increasing `T`, and flips only the sign of `κ₁₁₁` for decreasing `T` (leaving `ŝ` invariant).
This is Gate G1 and it is a bitwise test, not a tolerance test.

**Ties.** Rank ties are broken by **mid-rank** (average rank), which is a monotone
*non-decreasing* map — a legitimate coarse-graining — rather than by arbitrary order, which
would not be. After ranking, each channel is re-standardized to zero mean and unit variance so
`ζ_abc = E[x_a x_b x_c]` holds exactly.

### 1.5 WHAT THIS KILLS, AND WHAT IT DOES NOT

**Killed** (structurally absent, not merely checked):

| artifact family | why it is gone |
|---|---|
| entropy-estimator bias | no entropy is estimated; `κ̂₁₁₁` is a sample mean, unbiased, with an **analytic** null variance |
| IPF drift on near-deterministic states (`ISING_FIELD_RESULTS.md` §2: IPF reported 9.8e−6 where truth was 1.2e−10) | no IPF anywhere |
| tied fraction / median-split threshold | no threshold; ties enter only through mid-ranks and are reported |
| bin-count dependence and the `b ≥ 3` discretisation artifact (`SKY_PILOT_PREREG.md` §2.4) | no bins |
| marginal skewness/kurtosis leaking into the estimate | removed exactly by Gaussianization, which provably cannot change the target |

**NOT killed — and made worse.** The **clamp**. `fminf(fmaxf(x,0.001f),0.999f)` creates exact
point masses on the rails. A rail is a tie block: rank-Gaussianization maps it to a single
score, so a heavily railed channel's "Gaussianized" variable is a near-two-point variable, the
Gaussian reference `φ_C` is a bad reference, and the Edgeworth expansion behind (B) is invalid.
Moment estimators are *more* exposed to this than binned ones, because a point mass at an
extreme dominates a third moment. Therefore, mandatory and pre-set:

1. **Every reading is taken under both boundaries** — the shipped `clip` and the reflecting
   `fold` — from `array_cap_experiment.build_kernel`, which substitutes only the three clamp
   expressions and asserts they were present before substituting.
2. **Rail fraction is reported per channel like a tied fraction**: `rail = ` fraction of values
   exactly equal (float32) to `0.001f` or `0.999f`; `near_rail = ` fraction within `1e-6`.
3. **Pre-set rail threshold: 0.01.** A reading with `max_channel rail > 0.01` is **RAILED** and
   is excluded from every quoted result. It is still computed and reported.

---

## 2. SUBSTRATE AND READINGS

**Kernel.** The shipped `Ossicle.KERNEL_CODE` of `/home/emoore/CIRISArray/src/runtime.py`
(`r_base=3.70, r_spacing=0.03, twist_deg=1.1, n_cells=64`), compiled through
`array_cap_experiment.build_kernel(boundary)` (clip = verbatim arithmetic + a clamp counter
that does not enter the state update; fold = the same string with only the three clamp
expressions replaced). Driven at `iterations = 1`, licensed by `HABIT_DYNAMICS` Gate 2 (100
calls at `iterations=1` reproduce 1 call at `iterations=100` **bit-identically** at σ=0), so the
lag unit is one logistic step. Gaussian noise σ is added to the state before each call.

**Coupling graph, stated before any measurement.** Per (ossicle, cell) the kernel evolves a
**3-node path** `a — b — c`: `a↔b` via `twist_ab`, `b↔c` via `twist_bc`, and `b` driven by
`a+c−2b`. **`a` and `c` are not directly coupled.** Cells do not interact and ossicles do not
interact. So the device is `n_ossicles × 64` structurally independent replicas of one 3-node
chain. **The array therefore has no spatial separation axis at all**, and the Ising prediction
"separated triples beat local ones near criticality" is testable here only in its **temporal**
form. This is a limitation of the substrate, pre-registered rather than discovered.

Array geometry: `n_rows = 8, n_cols = 64` ⇒ 512 ossicles × 64 cells = **32 768 independent
replicas**, which are the estimator's i.i.d. sample at any fixed time slice.

**Readings** (all `k = 3`):

| tag | slots | what it is |
|---|---|---|
| `S3` | `(a_t, b_t, c_t)` | the only native coupled spatial triple |
| `C3` | `(a_t, b_{t+1}, c_{t+2})` | causally aligned along the chain's one-hop-per-step path |
| `T3(Δ)` | `(b_t, b_{t+Δ}, b_{t+2Δ})`, Δ ∈ {1,2,3,4,6,8,12,16} | the temporal cliff, continuously instrumented |
| `T3a(Δ)` | same on channel `a` (chain end), operating point only | robustness |
| `FARP` | `(a_t[i], b_t[π(i)], c_t[π′(i)])`, π,π′ random replica permutations | structural zero — replicas do not interact |
| `XRUN` | slot `j` from run `j` (independent seeds) | cross-run floor |

---

## 3. FLOORS AND ERROR BARS

**Primary statistic.** Per frame `t`, `κ̂₁₁₁(t)` is a mean over 32 768 structurally independent
replicas. The reported value is the mean over frames; the error bar is the across-frame sd
divided by `√(n_frames / τ_fixed)` with

    τ_fixed = max(1, 1 + 2 Σ_{L=1..min(32, n/4)} ρ_L)

computed on the per-frame `κ̂` series with **no truncation-at-first-negative rule** — that rule
returns a spurious 1.00 on this substrate's oscillatory ACF and the correction is recorded in
`HABIT_DYNAMICS_RESULTS.md` §C. `τ_fixed` is reported for every quoted reading.

**Floor 1 — Gaussian-copula surrogate (the pair-preserving null).** Draw `T` samples from
`N(0, Ĉ)` with `Ĉ` the measured normal-scores correlation matrix, push through the identical
pipeline. True order-3 content is zero by construction. Reported empirically and cross-checked
against the **analytic** null, which exists because the third moment of a Gaussian vanishes:

    E[κ̂₁₁₁] = 0,    Var[κ̂₁₁₁] = E_{φ_C}[x₁²x₂²x₃²] / T
                                = (1 + 2(ρ₁₂² + ρ₁₃² + ρ₂₃²) + 8ρ₁₂ρ₁₃ρ₂₃) / T.

The floor on `ŝ₃ = ½κ̂²` is then `≈ Var/2`, i.e. `O(1/T)` — **analytic, not fitted**.

**Floor 2 — replica-shuffle (`FARP`)**: independent permutation of the replica index per slot;
destroys all cross-channel structure.

**Floor 3 — cross-run (`XRUN`)**: slots from independent runs with different seeds, identical
parameters. Cannot share structure. Must floor at `|z| ≤ 5`.

**Temporal readings** additionally respect the autocorrelation lesson: **no i.i.d. surrogate is
trusted above coupling 0.35 without the matched control**. The frame-level `τ_fixed` above is
the variance inflation; `FARP` and `XRUN` are the matched controls; a **circular-shift**
surrogate (shift the replica axis of slots 2 and 3 by a random offset, preserving each
channel's own time structure exactly) is the third.

---

## 4. GATES — every one must PASS before any array number is believed

| gate | test | pass criterion |
|---|---|---|
| **G0** | the bridge's algebra: closed form (B) vs a basis-free Gram–Schmidt projection of `W^⊥ ∩ P₃` in `L²(φ_C)`, on random `C` and random symmetric `ζ` | max relative error `< 1e-9` |
| **G1** | **exact monotone invariance**: pipeline on `X`, `exp(X)`, `X³`, `sinh(X)`, `−X` | `|κ̂|` and `ŝ` identical to **0.0** (bitwise); sign flips only for `−X` |
| **G2** | **known-truth recovery**: skewed-latent triple `X_i = a_i Z + √(1−a_i²)ε_i`, `Z` with third cumulant γ, whose analytic `ζ_abc = γ a_a a_b a_c` and `C_ij = a_i a_j` make (B) closed-form | recovered `ŝ₃` within 3 error bars of the analytic value over ≥3 decades of γ, and `d log ŝ₃ / d log γ = 2.00 ± 0.05` |
| **G3** | **Gaussian null floors**: Gaussian copula at several `C`, `T` matched to the experiment | `\|z\| < 5` on ≥ 99 % of 200 draws; empirical vs analytic sd agree to 5 % |
| **G4** | **lognormal is a second null**: per-channel `exp` of G3's input | identical to G3 to **0.0** (this is G1 applied to the null) |
| **G5** | **kernel fidelity**: the clamp-counter clip build vs the shipped `Ossicle` kernel, 50 iterations, σ=0 | **bit-identical**, max diff `0.0` |
| **G6** | **cross-instrument**: on the same array data at the validated operating point, the binarized `shareK` of `array_cap_experiment` reproduces `HABIT_DYNAMICS_RESULTS.md`'s lag-1 value (0.0508 nats, κ=0.05, σ=1e-3) | within 10 % — proves the new driver reproduces the old measurement before the new instrument is trusted against it |
| **G7** | **degree-4 machinery**: `dim(W^⊥ ∩ P₄) = 4` (1 at degree 3, 3 at degree 4) and each basis element is `φ_C`-orthogonal to every function of ≤ 2 coordinates | dimension exact; orthogonality `< 1e-12` |

**Any gate failing ⇒ the run is VOID (K1) and no array number is reported as a measurement.**

G0, G1(analytic part), G2 and G7 involve **no array data whatsoever**. G0's algebra was checked
numerically on synthetic distributions before this file was committed (max relative error
7.6e-15, 8 random `(C, ζ)` pairs); that check is re-run inside the gate for the record.

---

## 5. THE SWEEP

### Stage 1 — locate the synchronization transition (before any share number is looked at)

The Ising map says order-3 peaks near **criticality** at **weak symmetry breaking**. The
array's distance-to-criticality analogue is coupling relative to its synchronization
transition, which is **measured, not assumed**:

- **order parameter** `ρ̄(κ)` = mean of the three across-replica correlations `ρ_ab, ρ_bc, ρ_ac`
  computed on the raw states at a fixed frame (not the kernel's clamp-mediated `phase` output —
  `ARRAY_CAP_RESULTS.md` established that the `phase` metric transduces coupling *through* the
  clamp);
- **sync error** `E(κ) = ⟨|a−b|⟩ + ⟨|b−c|⟩`;
- **susceptibility** `χ(κ) = dρ̄/dκ` by central difference, and the across-replica variance of
  the sync error.

`κ_c := argmax χ`. Grid: κ = 0 … 0.60 step 0.02, σ = 1e-3, both boundaries.

**The symmetry-breaking (h) analogue is measured, not assumed**, exactly as instructed. Two
diagnostics are reported and they are not the same thing:

- **naive**: per-channel skewness of the **raw** margins. The logistic map satisfies
  `f(1−x) = f(x)`, so it is *not* equivariant under `x → 1−x` and the flip symmetry is broken
  by the dynamics.
- **invariant**: by §1.4 the marginal skewness is **removable by a per-channel monotone map and
  therefore cannot itself drive the share**. The transform-invariant flip-odd content is the
  set of Gaussianized third moments — the pair-visible `κ_aab = E[x_a²x_b]` and the whole-only
  `κ₁₁₁`. Both are reported. Anyone reading marginal skewness as "the h-analogue" is reading
  the removable part.

### Stage 2 — the ridge

| axis | values |
|---|---|
| κ | {0, 0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.45, 0.60} ∪ {κ_c−0.04, κ_c−0.02, κ_c, κ_c+0.02, κ_c+0.04} |
| σ | {0, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1} |
| boundary | clip, fold |
| readings | S3, C3, T3(Δ=1,2,3,4,6,8,12,16), FARP, XRUN |

Settle 2000 iterations, 512 frames, seed 20260725. The top conditions by boundary-stable `ŝ₃`
are replicated at seeds {99, 7}. The operating point (κ=0.05, σ=1e-3) additionally carries
`T3a`, the `D=4` estimator, the binarized cross-instrument comparison (G6), and 5 seeds.

### Stage 3 — the temporal cliff, continuously instrumented

At κ = 0.05, σ = 1e-3 and at the stage-2 optimum: `T3(Δ)` for Δ = 1…16 with `ŝ₃`, `ŝ₄`, all
three floors, and the binarized `shareK` on the *same* frames for direct comparison.

---

## 6. PREDICTIONS — every possible answer, and what each would mean

| # | prediction | if it fails |
|---|---|---|
| **P1** | G1 holds bitwise | implementation bug ⇒ **VOID** |
| **P2** | G2 slope `= 2.00 ± 0.05` | the quadratic bridge is wrong ⇒ instrument unusable, report as a clean negative about the method |
| **P3** | `S3` carries `\|z\| > 5` under **both** boundaries at some κ > 0 with `rail ≤ 0.01` | ⇒ **"the array does not carry boundary-stable order-3 at degree 3"** — a clean null, consistent with the binarized nulls, reported and not rescued |
| **P4** | **interior maximum in κ**, located in 0.10–0.30 and within 0.05 of `κ_c` | monotone in κ, or a peak far from `κ_c` ⇒ the Ising "criticality" coordinate does not transfer to a continuous chaotic substrate |
| **P5** | **interior maximum in σ** somewhere in 1e-4…3e-2, exceeding both σ=0 and σ=1e-1 by > 3 error bars | monotone decay ⇒ the ECA interior noise optimum does not transfer |
| **P6** | the temporal-separation analogue of the Ising ridge does **NOT** transfer: `argmax_Δ T3(Δ)` stays at Δ = 1 at every κ including `κ_c` | if `argmax_Δ > 1` near `κ_c`, that **is** a genuine cross-substrate confirmation of "separated beats local at criticality" and is reported as the run's main positive result |
| **P7** | the 2-iteration cliff **survives** continuous instrumentation: `T3(Δ)` clears its floor at Δ = 1, 2 and floors from Δ = 3 at κ = 0.05 | a continuous tail at Δ ≥ 3 ⇒ the cliff was partly a binarization artifact and `HABIT_DYNAMICS_RESULTS.md` needs a correction — reported as loudly as the survival |
| **P8** | clip fires where fold does not at κ ≥ 0.20, and the rail fraction there exceeds 0.01 | if instead clip and fold agree at high κ, the clamp lesson has a boundary and that is worth recording |
| **P9** | `ŝ₃` at the operating point, Δ=1, is **within a factor of 3 of** the binarized 0.0508 nats | if `ŝ₃ ≪` binarized, run `ŝ₄`; if `ŝ₄` is still ≪, the array's whole-only content lives **above degree 3** and `κ₁₁₁` is the wrong summary — a finding about the instrument, and a caution for the moment route generally, including for the sky-pilot sibling |

**The deliverable of the sweep**, pre-committed: the (κ, σ, geometry) point of maximal
*boundary-stable, rail-clean* `ŝ₃`; its magnitude in nats and as a fraction of the
machine-checked cap `ln 2`; and a verdict on whether the ridge shape (interior maximum in both
knobs; separated > local near the transition) replicates.

---

## 7. KILLS — separable, each takes down its own claim and nothing beneath it

| kill | fires when | what dies |
|---|---|---|
| **K1** | any gate G0–G7 fails | **everything** — the run is VOID |
| **K2** | `FARP` or `XRUN` exceeds `\|z\| = 5` in a condition | that condition's null is mis-specified; its z-scores are voided (the *values* survive, as in `ARRAY_CAP_RESULTS.md`) |
| **K3** | no reading anywhere clears `\|z\| > 5` under both boundaries with `rail ≤ 0.01` | the positive claim only: **"no boundary-stable whole-only structure anywhere"**, a clean null |
| **K4** | structure clears its floor under `clip` but not under `fold` at the same point | the fourth clamp artifact of the day; reported loudly; no positive claim survives at that point |
| **K5** | no interior maximum in either knob | the ridge shape does not replicate on a continuous chaotic substrate; the Ising/ECA cross-substrate generalization loses this test case |
| **K6** | `ŝ₃` and `ŝ₄` both `≪` the binarized share at a point where the binarized reading is clean | the degree-3 moment route is an inadequate summary of this substrate's whole-only content — a caution that outlives this run |

---

## 8. WHAT THIS CANNOT DELIVER — written now so it cannot be claimed later

1. **Nothing about nature.** A designed chaotic lattice on our own GPU is a model system.
   `wild-share` is untouched.
2. **No stance change**, no `Stance.lean`, no Lean file, no audit, no `lake`. Research →
   scratchpad memo → Eric's review.
3. **No priority claim.** (B) is an Edgeworth/connected-information calculation; the negentropy
   route is Comon/Hyvärinen; the projection-pursuit expansion is Jones & Sibson. Assume
   convergence: this is very likely in print somewhere, and the credits go in the file header.
4. **`ŝ_D` is a second-order proxy, not the share.** It is exact only to `O(u³)`. Where the
   array's structure is strong it is a leading term, not a measurement of `I_C⁽³⁾`, and it will
   be labelled `ŝ` everywhere, never "the share".
5. **No claim that the binarized share is a lower bound on the continuous one.** Coarse-graining
   monotonicity for `I_C⁽³⁾` requires the pairwise family to be closed under the pushforward,
   which is not established here. Disagreements between the two routes will be reported as
   disagreements, not resolved by assumption.
6. **`D = 3` is blind to flip-symmetric whole-only structure** (§1.3). `D = 4` mitigates but
   does not eliminate the truncation.

---

*Pre-registration ends here. Nothing below this line existed when it was committed.*
