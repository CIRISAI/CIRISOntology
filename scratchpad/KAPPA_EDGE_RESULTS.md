# RESULTS — the κ = 0.16 route disagreement, resolved; and the b = 2 median split re-scoped

Pre-registered in `KAPPA_EDGE_PREREG.md` (`f5fa4b4`), `KAPPA_EDGE_PREREG_ADDENDUM.md`
(`a586449`) and `KAPPA_EDGE_PREREG_ADDENDUM2.md` (`0885182`), each committed **before** the
code and the stage it governs existed. Substrate: the shipped `Ossicle.KERNEL_CODE` at
`iterations = 1`, 512 ossicles × 64 cells = 32 768 structurally independent replicas, driven
through `array_negentropy.Driver`. Scratchpad only; no Lean file, no `Stance.lean`, no audit;
`lake` was never run; nothing pushed.

**Scope, first and load-bearing.** CIRISArray is **our own designed chaotic hardware**. It is
not nature. Nothing here bears on `wild-share`, `adequacy`, or any claim about the world. The
outcome re-scopes one of our own headlines downward and that is reported as the headline.

---

## VERDICT

**All three hypotheses resolved, and the answer is a fourth thing that supersedes the question.**

> **The b = 2 median-split whole-only share, at this substrate's operating points, is not a
> measurement of three-way structure. It is a deterministic function of the fine-grained pair
> marginals — proved by linear programming, with no model, no surrogate, no IPF and no
> estimator.**
>
> At **κ = 0.05** — the array's published headline point — **every** probability distribution
> carrying the array's measured level-8 pair marginals has a b = 2 share of **exactly
> 5.0745 × 10⁻² nats**. The LP interval has width **0.00000**. The measured value is
> 5.0745 × 10⁻², and `ARRAY_NEGENTROPY_RESULTS.md` publishes **5.073 × 10⁻² (fold)** as a
> measured magnitude, 7.3 % of the machine-checked cap `ln 2`.
>
> At **κ = 0.16** the same LP confines the b = 2 share to **[8.5086, 8.9685] × 10⁻²** given the
> level-8 pair marginals (to a **single point**, 8.5086 × 10⁻², given the level-16 ones). The
> measured value is 8.5087 × 10⁻², sitting at the bottom of that interval.

**H-ZERO — CONFIRMED.** The signed whole-only coordinate `w` crosses zero at
**κ₀ = 0.1651** (fold, σ = 1e-3), **0.1646** (clip), **0.1664** (fold, σ = 1e-2), and
`ŝ₃ = w²/2`. κ = 0.16 sits on that zero. The binarized reading is flat through it (factor
1.13 across the whole window). **The 1 400× was the ratio evaluated at a zero of its own
denominator.**

**H-MANUFACTURED — CONFIRMED**, in a stronger form than it was posed, and on evidence that
does **not** include the surrogate ratio `F` (see the withdrawal in §2).

**H-BLIND — SURVIVES, relocated, and it is about the MOMENT route, not the b = 2 route.**
There *is* genuine fine-grained whole-only structure, and the degree-3 projection carries
**1.0 %** of it (κ = 0.16), **1.2 %** (κ = 0.05), **0.16 %** (κ = 0.30) of `Σ ΔG²` over the
Hermite directions. But that structure is invisible to the b = 2 split too, because the b = 2
split is pinned. **Neither instrument was reporting it.**

**Mixed outcome, per prereg §4 case 3, with the split quantified:** of the 1 400×, a factor of
~40 is the zero crossing (the ratio is 30–140 elsewhere in the window) and the remainder is
that the two instruments are measuring different things — one pinned by pair marginals, the
other projecting onto a direction holding ~1 % of the signal.

---

## 1. THE HONEST ACCOUNTING — what fired, including on my own machinery

Four pre-registered bars fired against me. None was waived; each is recorded with what it cost.

| | bar | outcome |
|---|---|---|
| **K-VOID** | IPF/dual disagreement > 1e-8 in `H(Q)` | **FIRED** at `b = 4, 6, 8`. Re-derived from the dual alone (FDUAL, §8): `\|F_dual − F_ipf\| ≤ 1.1 × 10⁻⁵` against a 0.01 bar. The verdict is solver-independent. |
| **W3** (POWER-1) | `F` falls below 0.5 | **FAILED** (`F ≥ 0.997`). Diagnosed as **my construction error**: the doping changed the pair marginals, so the surrogate was handed a copy of the injected structure. |
| **W3′** (POWER-2) | `F` falls below 0.5 with marginals held exactly fixed | **FAILED** (`F` saturates at **0.9526** as λ → ∞). Not a range problem — extended to λ = 25.6 with the injected coupling verified present (`cert = 8λ = 204.8` exactly). |
| **E4** verdict rule | indicator triple ≥ 0.5× full, within-phase ≤ 0.2× | **FAILED** on both legs (0.015, and 0.073 / 0.340). The intermittency mechanism is **not** identified. |
| **Z3** | route ratio ≤ 30 outside the crossing | **SPLIT** — spike confirmed far beyond prediction, baseline bar not met (30–140). |

### The withdrawal I owe, paid

`ADDENDUM2.md` §3 said: if POWER-2 also fails W3, *"the withdrawal is unconditional and that is
the headline."* **W3′ failed. I therefore withdraw `F ≈ 1` as evidence for H-MANUFACTURED.**
It appears below only as a consistency check.

**What carries the verdict instead needs no power control at all.** The linear program (§4)
computes the exact range of the coarse sign triple over *every* distribution with the measured
level-`b` pair marginals. It has no null, no surrogate, no estimator and no tunable. And it
**explains** W3′'s failure exactly: `F` bottoms at 0.9526 because
`s₂ ≤ 8.9685 × 10⁻²` for **any** such distribution, so
`F ≥ 8.5434/8.9685 = 0.9526`. The doping family was extremal after all; the bar was
unreachable by anything. **I did not get to keep `F`; I got a better instrument because
losing it forced me to look for one.**

---

## 2. E0 — THE ZERO CROSSING (H-ZERO)

Fine grid κ = 0.140…0.200 step 0.005, both boundaries, two noise levels; same frames through
both routes. Fold, σ = 1e-3:

| κ | 0.140 | 0.150 | 0.155 | **0.160** | **0.165** | **0.170** | 0.180 | 0.190 | 0.200 |
|---|---|---|---|---|---|---|---|---|---|
| `w̄` ×10² | −3.948 | −3.907 | −2.220 | **−1.110** | **−0.011** | **+0.865** | +2.140 | +4.529 | +7.071 |
| `ŝ₃` | 7.79e-4 | 7.63e-4 | 2.46e-4 | **6.16e-5** | **−1.5e-8** | **3.73e-5** | 2.29e-4 | 1.03e-3 | 2.50e-3 |
| `s_bin` | 7.84e-2 | 7.92e-2 | 8.25e-2 | **8.51e-2** | **8.61e-2** | **8.59e-2** | 8.10e-2 | 7.78e-2 | 7.59e-2 |
| ratio | 100.6 | 103.8 | 334.6 | **1 380.6** | **∞** | **2 299.9** | 353.8 | 75.9 | 30.3 |

At κ = 0.165, `w̄ = −1.10 × 10⁻⁴ ± 2.0 × 10⁻⁴` — consistent with zero at 0.5 σ — and the
moment route's own `z` falls to **−0.5**, from ±100–600 elsewhere.

- **Z1 SURVIVED.** `w` crosses linearly; κ₀ located to ±0.005 and stable at 0.1646–0.1664
  across **both boundary conventions and a 10× change in noise**.
- **Z2 SURVIVED, decisively.** The binarized reading varies by a factor of **1.135** across the
  whole window (1.09 at σ = 1e-2), against a 2× bar. It does not know the crossing is there.
- **Z3 SPLIT.** The spike is unambiguous; the ≤ 30 baseline bar is **not met** (30–140).
- **Z4 SURVIVED** (consistency only).
- **K-Z did not fire.**
- **Dose-vs-rate passes**, per the standing rule: κ₀ = **0.1658 / 0.1656 / 0.1657** at
  settle = 500 / 2000 / 8000. A 16× change in run length moves the crossing by 2 × 10⁻⁴ — **25×
  inside a single grid step**. The crossing is intrinsic, not a marker of when the run stops
  being settled.

Clip arm reported and not quoted: rail fraction 0.103–0.183 across this window, 10–18× the
0.01 threshold frozen before the parent run, so the boundary discriminator is **unavailable**
there. Its κ₀ = 0.1646 agrees with fold's anyway.

**A zero crossing of a signed linear functional is generic and cheap.** `w` is linear in the
distribution at fixed reference covariance, so *any* sweep that carries `w` through zero
produces an arbitrarily large route ratio at the crossing. **That is the argument, and it is
why a minimum of `w²` must never be read as a collapse of structure.** The mixture null is not
applicable in its usual form for exactly this reason, stated rather than skipped.

---

## 3. THE MOMENT ROUTE AT THE THREE OPERATING POINTS

| κ | `w̄` | `ŝ₃` | `z` | `max\|ρ_pair\|` | τ | regime |
|---|---|---|---|---|---|---|
| 0.05 | −2.086e-1 | 2.177e-2 | −386.6 | 0.561 | 1.00 | **OUTSIDE** (detector, not meter) |
| 0.16 | −1.107e-2 | 6.13e-5 | −68.0 | 0.437 | 1.00 | **OUTSIDE** |
| 0.30 | +1.879e-1 | 1.765e-2 | +844.4 | 0.550 | 1.84 | **OUTSIDE** |

All three sit outside `ARRAY_NEGENTROPY_RESULTS.md` §11's `max|ρ_pair| ≤ 0.3` validity regime.
Nothing here promotes `ŝ₃` to a magnitude.

---

## 4. THE LINEAR PROGRAM — the result the verdict rests on

The coarse sign triple `E[s₁s₂s₃]` is **linear** in the cell probabilities, and the level-`b`
pair marginals are **linear equality constraints**. So its exact range over every distribution
carrying those marginals is a linear program (HiGHS; `b = 8` is 512 variables and 192
constraints, `b = 16` is 4 096 and 768). Given the range of the sign triple and the b = 2 pair
marginals — which are fixed, because coarse-graining commutes with marginalisation — the b = 2
share follows exactly, since distributions on 8 cells with given pair marginals form a
**one-parameter** family (`c + δ·(−1)^(i+j+k)`).

| point | level | sign-triple range | width | ⇒ b = 2 share confined to | measured |
|---|---|---|---|---|---|
| **κ = 0.05** | b = 8 | [0.21424, 0.21424] | **0.00000** | **{5.0745e-2}** | 5.0745e-2 |
| κ = 0.05 | b = 16 | [0.21424, 0.21424] | **0.00000** | {5.0745e-2} | 5.0745e-2 |
| **κ = 0.16** | b = 8 | [0.30750, 0.31323] | 0.00573 | [8.5086e-2, 8.9685e-2] | 8.5087e-2 |
| κ = 0.16 | b = 16 | [0.30750, 0.30750] | **0.00000** | {8.5086e-2} | 8.5087e-2 |

*(Sign convention: `_sign_tilt` maps bin index ≥ b/2 to +1 while the 2×2×2 alternating tensor
is `(−1)^(i+j+k)`; the two differ by an overall sign at k = 3, so the LP's +0.21424 is the
data's −0.21424. Magnitudes agree to five decimals, which is itself the cross-check.)*

**For comparison, given only the b = 2 pair marginals** — i.e. throwing the fine-grained
information away — the b = 2 share could range over **[0, 9.43e-2]** at κ = 0.16 and
**[0, 7.31e-2]** at κ = 0.05. So the statistic has plenty of headroom **in general**; it is the
array's own fine-grained pair marginals that remove it.

### The mechanism, measured: near-determinism, not coupling strength

The array's temporal triple is nearly deterministic — it is a logistic-family map at
σ = 1e-3. Counting the fine (x, y) cells whose **support spans both signs of z**:

| point | b = 8 | b = 16 | joint occupancy, b = 8 → 32 |
|---|---|---|---|
| κ = 0.05 | **6 / 64** | **7 / 256** | 14.5 % → 2.7 % |
| κ = 0.16 | 16 / 64 | 28 / 256 | 26.2 % → 8.1 % |

Where the support does not straddle the median, `s(z)` is a **function of (x, y)** on the
support, so `s(x)s(y)s(z)` is a **pair term** there and carries no three-way information at all.
That is why the LP interval collapses, and it is also the correct reading of the b = 16
POWER-2 arm, where the interaction certificate reported the injected coupling had vanished —
it had been absorbed into pair terms, not lost to arithmetic.

---

## 5. THE LP's OWN GATE — it has teeth, and it locates the boundary

The LP is only worth anything if it can return a wide interval. Four controls, 2 × 10⁶ samples
each, identical pipeline:

| control | b = 8 sign-triple width | b = 2 share reachable | (x,y) spanning both z signs |
|---|---|---|---|
| independent triple | **1.9925** | [1.1e-7, **0.681**] | 64 / 64 |
| Gaussian copula **at the array's own ρ** (−0.44, −0.04, −0.44) | **0.7970** | [1.5e-14, 0.122] | 64 / 64 |
| Gaussian copula, weak ρ (0.15, 0.05, 0.15) | **1.6753** | [0, 0.439] | 64 / 64 |
| **deterministic logistic map** (r = 3.9, no noise) | **0.00000** | {**7.941e-2**} | **3 / 64** |

**This is the load-bearing control of the whole run.** A Gaussian triple carrying the array's
*own* pair correlations is **not** pinned — width 0.797. So the pinning is **not** a consequence
of strong pair correlation. A noise-free logistic map is pinned to a point, exactly as the
array is. **The mechanism is determinism of the conditional support, and coupling strength is
not the variable.**

---

## 6. WHAT THIS DOES AND DOES NOT IMPLY FOR b = 2 MEASUREMENTS ON OTHER SUBSTRATES

Written for the `SKY_FORECAST` sibling, whose b = 2 sign-triple route inherits this conclusion,
and for the spike-train literature generally.

**Where the manufacture bites.** Wherever the triple's conditional support is close to
deterministic — the third variable's value, given the first two, confined to one side of its
own median on most of the support. Deterministic and weakly-noised dynamical systems
(chaotic maps, low-noise recurrences, our array), and any tightly time-locked sequence. There
the b = 2 median split reports a number that the fine-grained **pair** marginals already fix,
and it should not be read as three-way structure at all.

**Where it should NOT bite, and the reason.** Stochastic near-Gaussian fields with broad
conditional distributions — the sky mocks' regime. The conditional law of the third variable
straddles the median over essentially the whole support, so `s(z)` is genuinely free given
(x, y), and the LP interval stays wide. **Measured above: at weak coupling the width is 1.675
of a possible ~2, i.e. the b = 2 statistic retains essentially all of its capacity.** The
strong-ρ Gaussian control (width 0.797) shows this survives even substantial correlation.

**What the sky agent should nevertheless do, and it is cheap.** Run the LP at its own pipeline
resolution — `t_range_given_fine_marginals(P, b)` in `kappa_edge.py` — on its actual binned
tables. It is exact, takes seconds at b = 8, needs no surrogate, no IPF and no null, and it
returns the interval within which that pipeline's b = 2 reading was free to move. **If the
interval is wide, the b = 2 number is a measurement and this memo does not touch it. If it is
narrow, the number was determined before the three-way structure was consulted.** That test is
strictly better than the fine-b pair-maxent surrogate control I was asked to design, because it
does not depend on the surrogate being the right null — and I recommend it in place of that
control.

**What this does not say.** It does **not** say median-split b = 2 measurements are generally
invalid; the gate above shows the opposite in three of four regimes. It does **not** touch
`Core/SignSymmetry.lean`: a sign-symmetric field still binarizes to share exactly 0 by
`share_eq_zero_of_signSymmetric`, and a lognormal is a monotone map of one, so the sky design's
nulls are protected by the theorem regardless of anything here. It does **not** contradict the
pilot's monotone-invariance theorem, which concerns monotone maps applied before an unchanged
median split — a different comparison.

---

## 7. THE b-LADDER — REPORTED AS UNINTERPRETABLE, LOUDLY

Level-`b` excess over the matched pair-maxent multinomial floor, with joint occupancy:

| b | 2 | 3 | 4 | 6 | 8 | 16 | 32 |
|---|---|---|---|---|---|---|---|
| **κ = 0.16** excess | 8.51e-2 | 3.20e-2 | 2.64e-3 | 3.13e-3 | 7.71e-3 | 3.49e-2 | **1.23e-1** |
| occupancy | 100 % | — | 51.6 % | 36.1 % | 26.2 % | 13.2 % | **8.1 %** |
| **κ = 0.30** excess | 2.74e-2 | 2.50e-2 | 5.25e-3 | 2.36e-2 | 3.43e-2 | 1.21e-1 | **2.68e-1** |
| occupancy | 100 % | — | 60.9 % | 48.1 % | 37.5 % | 24.4 % | **17.4 %** |

The rise from `b = 4` to `b = 32` looks like H-BLIND's prediction. **It is not reportable as
support**, and the reason is arithmetic rather than taste: the excess climbs monotonically as
occupancy collapses, and at κ = 0.30, `b = 32` it reaches **0.268 nats = 39 % of `ln 2`** on a
table that is 82.6 % empty. This is the sparse, near-deterministic regime in which IPF is known
to overstate (`ISING_FIELD_RESULTS.md` §2 — IPF read 9.8e-6 where the truth was 1.2e-10; the
`ipf-sharek-boundary-drift` and `eca-pairwise-blind-spike` lessons), and the matched
pair-maxent floor **cannot** catch it, because multinomial samples drawn from a dense `Q` are
not sparse. **No null in this run controls it. The b ≥ 16 rungs are void, and the b = 4–8 rungs
carry a caveat of the same kind.** `SKY_PILOT_RESULTS.md` §3's conclusion — b = 2 is the only
safe rung without subtraction — is reproduced here rather than overturned.

---

## 8. THE HERMITE LOCALISATION — where the real structure is, and why nobody saw it

`ΔG_{ijk} = E_P[He_i He_j He_k]/√(i!j!k!) − E_Q[·]`, evaluated **exactly** on the level-8
tables. Built-in arithmetic check: entries with any index 0 must vanish because `P` and `Q`
share every pair marginal — **max ≤ 2.2 × 10⁻¹⁰** at all three κ. Passed.

| κ | `ΔG₁₁₁` | share of `Σ ΔG²` in (1,1,1) | largest directions |
|---|---|---|---|
| 0.05 | −1.03e-3 | **1.17 %** | (1,4,5), (1,1,2), (1,3,5) |
| 0.16 | +1.11e-3 | **1.02 %** | (1,5,2), (1,3,2), (1,5,1) |
| 0.30 | +2.19e-3 | **0.16 %** | (4,2,2), (1,1,2), (1,1,4) |

**H-BLIND's mechanism is confirmed, but about the moment route only.** The genuine
fine-grained whole-only content is overwhelmingly *not* in the `He₁⊗He₁⊗He₁` direction that
the degree-3 bridge projects onto — that direction holds ~1 %. The degree-3 route is blind to
the other ~99 % by construction, and the parent run's §8 already showed the degree-4 and
degree-5 extensions exceed the machine-checked cap and cannot be used to recover it. **The
blindness class is real and is now localized.**

And the sign-triple reconstructions of `P` and `Q` are indistinguishable — at κ = 0.05,
`+0.214131` vs `+0.214131` — which is §4's pinning seen in a second, independent coordinate
system.

---

## 9. THE CONTROLS, IN FULL

**POWER-1** (registered `a586449`, ran, failed): W1 **pass exactly** (`F(0) = 1.0041` reproduced
the independently measured b = 8 value to four figures; the surrogate arm gave `F = 1.0000`
with genuine excess 1.3e-9). W2 pass. **W3 fail** — `F ≥ 0.997` while the doping nearly tripled
the b = 2 share (8.5e-2 → 2.07e-1). Cause: `M01_λ(x,y) = Σ_z P exp(λ s(x)s(y)s(z))/Z` depends
on λ, so the doping moved the pair marginals.

**POWER-2** (registered `0885182`): doping inside `{exp(pairwise + λ·s s s)}` with the level-`b`
pair marginals held **exactly** fixed, so `pair-maxent(P′_λ) = Q` and the surrogate term is
frozen. Verified, not assumed: projection check ≤ 1.8e-13, and `cert(P′_λ) = 8λ` **exactly** at
every λ up to 25.6 (204.8000 vs 204.8000).

| λ | 0 | 0.02 | 0.05 | 0.1 | 0.2 | 0.4 | 0.8 | 1.6 | ≥ 3.2 |
|---|---|---|---|---|---|---|---|---|---|
| fine-grained share (nats) | 0 | 3.7e-7 | 2.5e-6 | 1.1e-5 | 5.4e-5 | 3.0e-4 | 1.6e-3 | — | **3.44e-3 (sat.)** |
| `F` | 1.0000 | 0.9997 | 0.9991 | 0.9981 | 0.9956 | 0.9885 | 0.9686 | — | **0.9526 (sat.)** |

**W1′ pass. W2′ pass. W3′ FAIL** — and §4 proves the bar was unreachable by *any* distribution.

**W4′ — the sensitivity, which is the number the null must be quoted with.** `F` is resolved to
**± 0.0001** (BLOCK, 16 contiguous start-frame blocks), and the transfer function above converts
that to **≈ 4 × 10⁻⁷ nats** of genuine, sign-triple-aligned, fine-grained whole-only structure.
The measurement is `F = 1.0041 ± 0.0001` at b = 8 — i.e. **41 σ on the wrong side of 1** — and
the genuine b = 2 excess is **−3.47 × 10⁻⁴ ± 0.07 × 10⁻⁴ nats** (−51 σ), against a manufactured
8.5 × 10⁻². *This is the consistency check, not the evidence; the evidence is §4.*

**FDUAL** (owed by `a586449` after K-VOID fired): `|F_dual − F_ipf| = 1.1e-5, 1.2e-7, 6.1e-8` at
b = 4, 6, 8 against a 0.01 bar. **Solver-independent.** The prediction that motivated it — that
`F` turns on one number and is far less sensitive than `H(Q)` — held: `H(Q)` disagreed by
3.4e-6 where `F` disagreed by 1.1e-5 in ratio, i.e. 1e-5 in an O(1) quantity.

**E4, the on-off decomposition — FAILED its verdict rule, both legs.** Laminar/burst indicator
defined in advance as `e = |x₀−x₁| + |x₁−x₂|` below the pooled median. Indicator-triple excess
1.30e-3 = **0.015×** the full amplitude triple (needed ≥ 0.5); within-laminar 0.073×,
within-burst 0.340× (needed ≤ 0.2). **The intermittency mechanism is not identified**, and in
hindsight it could not have been: §4 says the b = 2 amplitude reading is pinned by the pair
marginals, so no decomposition of it can attribute it to a dynamical mechanism.

**Standing floors.** Shuffle floor at b = 2: +7.2e-8 ± 1.2e-7 (κ = 0.16), +6.0e-8 ± 7.7e-8
(κ = 0.05), +5.6e-8 ± 6.1e-8 (κ = 0.30) — clean against signals of 10⁻². Tie fractions
≤ 5.4e-7 everywhere. τ reported per reading (1.00, 1.00, 1.84). Non-overlapping start frames
throughout, so the multinomial floors act on independent replicas. IAAFT not used and its
absence is not a gap.

**Gate.** Ten checks, all pass, and it caught two bugs in my own new code before any array
number was taken: a missing log-partition shift in the dual solver, and an unachievable
criterion on the truncated `sgn` series. `Ge`/`Gf` are the pair that matters — a sign-symmetric
fine distribution coarse-grains to b = 2 share **exactly 0** (`Core/SignSymmetry.lean` used as a
control on my own code), while an asymmetric one manufactures 1.8e-4.

---

## 10. SCORECARD AGAINST WHAT WAS WRITTEN IN ADVANCE

| | prediction | outcome |
|---|---|---|
| **Z1** | `w` crosses zero, κ₀ located | **SURVIVED** — 0.1646–0.1664 across both boundaries and 10× in σ |
| **Z2** | `s_bin` smooth through κ₀, < 2× | **SURVIVED** — 1.135 |
| **Z3** | ratio ≤ 30 outside the crossing | **SPLIT** — spike far exceeds prediction; baseline is 30–140 |
| **Z4** | \|z\| minimal at κ₀ | **SURVIVED** — −0.5 |
| **K-Z** | H-ZERO's falsifier | **did not fire** |
| **E1 `F` rule** | F ≥ 0.5 ⇒ H-MANUFACTURED | measured 1.00, **but WITHDRAWN as evidence** (W3′) |
| **W1, W2** | POWER-1 | **PASS** |
| **W3** | POWER-1 | **FAIL** — my construction error |
| **W1′, W2′** | POWER-2 | **PASS** |
| **W3′** | POWER-2 | **FAIL** — and §4 shows the bar was unreachable by any distribution |
| **W4′** | sensitivity quoted with the null | **DELIVERED** — 4e-7 nats |
| **K-VOID** | IPF/dual > 1e-8 | **FIRED**; re-derived from the dual, `\|ΔF\| ≤ 1.1e-5` |
| **K-M** | F ≤ 0.05 kills H-MANUFACTURED | **did not fire** |
| **K-B** | F ≥ 0.5 + ΔG floors kills H-BLIND | **did not fire** — ΔG does **not** floor |
| **E4** | intermittency identified | **FAILED**, both legs |
| **K-DOSE** | κ₀ moves > 1 grid step over settle ∈ {500, 2000, 8000} | **did not fire** — κ₀ = 0.1658, 0.1656, 0.1657 over a 16× range in settle length. Total spread 2 × 10⁻⁴, **25× inside one grid step**. The crossing is an intrinsic operating point, not a run-length marker |

---

## 11. WHAT IS NOT CLAIMED

1. **Nothing about nature.** A designed chaotic lattice on our own GPU. `wild-share`,
   `adequacy` and every Logos claim are untouched.
2. **No stance change**, no Lean file, no `Stance.lean`, no audit, `lake` never run, nothing
   pushed.
3. **No priority claim.** The RG framing is Kadanoff (1966) / Wilson (1971); coarse-graining
   creating connected information is Kahle, Olbrich, Jost & Ay (PRE 79:026201, 2009) and our own
   `SKY_PILOT_RESULTS.md` §7, which already measured `A(b=2)/A_∞ = 4.8–6.6` on an asymmetric
   configuration; the measure is Schneidman, Still, Berry & Bialek (2003) and Amari (2001); IPF
   is Deming & Stephan (1940), the I-projection reading Csiszár (1975); copula invariance is
   Sklar (1959) and Scherrer et al. (2010). **Assume convergence** — I have not searched for
   prior art on "the marginal polytope pins a coarse-grained interaction", and it would be
   surprising if the LP argument were new.
4. **`ŝ₃` is not promoted.** All three operating points sit outside its `max|ρ_pair| ≤ 0.3`
   validity regime; it remains a detector, not a meter.
5. **The b ≥ 16 ladder rungs are void**, not weak evidence (§7).
6. **The fine-grained structure is not quantified in nats.** §8 localizes *where* it is (not in
   the degree-3 direction) but the level-`b` magnitudes that would size it are exactly the ones
   §7 voids. **How much genuine order-3 structure the array carries remains open.**
7. **No correction has been applied to any prior file.** §12 is a recommendation.

---

## 12. RECOMMENDED TO ERIC'S REVIEW, NOT ACTIONED

1. **`ARRAY_NEGENTROPY_RESULTS.md`'s VERDICT** currently reads: *"MAGNITUDE, at the same point:
   carried by the b = 2 median-split exact route... `shareK` reads 5.104e-2 (clip) and 5.073e-2
   (fold) — 7.4 % and 7.3 % of the machine-checked cap."* **That magnitude should be re-scoped.**
   Every distribution carrying the array's measured b = 8 pair marginals reads 5.0745e-2. The
   number is a property of the pair marginals, not a measurement of three-way structure.
2. **§7's "1 400×" and §11's "two hypotheses excluded and the disagreement remains
   unexplained"** are resolved: it is a zero crossing of `w` (κ₀ = 0.1651) times a route gap of
   30–140.
3. **§5's P4 reading** — *"the temporal reading has its deep minimum there... a factor of 363
   below its own κ = 0.05 peak"* — is a **zero crossing described as a collapse**.
4. **A standing rule, proposed:** publish the **sign** of `w`, never `w²` alone, and never quote
   a route ratio without checking the signed coordinate for a nearby zero.
5. **A second standing rule, proposed:** every b = 2 median-split share claim carries its **LP
   interval** — the range the statistic was free to move in given the fine-grained pair
   marginals. It is exact, cheap, surrogate-free, and it is what separates a measurement from a
   restatement of the pair marginals.

---

## FILES

| | |
|---|---|
| `KAPPA_EDGE_PREREG.md` | three hypotheses, kills, mixed outcomes — `f5fa4b4`, before any code |
| `KAPPA_EDGE_PREREG_ADDENDUM.md` | K-VOID fired; FDUAL; the power control — `a586449` |
| `KAPPA_EDGE_PREREG_ADDENDUM2.md` | W3 failed; the doping diagnosis; POWER-2; BLOCK — `0885182` |
| `kappa_edge.py` | gate, E0, E1/E2/E3, POWER-1/2, HEADROOM + the LP, E4, FDUAL, DOSE |
| `kappa_edge_e0.{json,log}` | the zero crossing, 39 conditions |
| `kappa_edge_e1.{json,log}` | b-ladder, surrogate, Hermite, three κ |
| `kappa_edge_e1_partial.log` | the first E1 attempt, stopped at b = 16 on IPF cost; kept |
| `kappa_edge_power.{json,log}` | POWER-1, the control that failed |
| `kappa_edge_power2.{json,log}`, `kappa_edge_power2ext.log` | POWER-2 and the λ extension to 25.6 |
| `kappa_edge_headroom.{json,log}` | the LP, the 2×2×2 headroom, the determinism counts |
| `kappa_edge_rest.log`, `kappa_edge_dose.json`, `kappa_edge_e4.json`, `kappa_edge_fdual.json` | E4, FDUAL, DOSE |

Primary seed 20260725. Research → scratchpad memo → Eric's review. Nothing pushed.
