# RESULTS — the critical ridge is the 2D Ising CFT's magnetisation sector

Pre-registered in `CFT_RIDGE_PREREG.md`, committed at **`de11b97`** *before* `cft_ridge.py`
existed. Scratchpad only: no Lean file, no `Stance.lean`, no audit; `lake` was never run.

**Scope, first and load-bearing.** The 2D Ising model is a **model system**, not nature.
Nothing here bears on the `wild-share` open claim and no sentence below should be read as a
claim about the world.

---

## THE HEADLINE

**The mechanism of the critical ridge is identified, and it is known physics.** At `T = T_c`
the correlators that feed the pairwise-blind order-3 share carry the 2D Ising CFT's spin
dimension `Δ_σ = 1/8` and its magnetic eigenvalue `y_h = 15/8`, to better than **0.1 %**:

| at matched `(r/L, u)`, `u = h L^(15/8)` | `L = 8` | `12` | `16` | `20` | drift |
|---|---|---|---|---|---|
| `m · L^(1/8)` (`β/ν = 1/8`) | 0.950125 | 0.952123 | 0.952889 | 0.953268 | **0.33 %** |
| `c(r) · L^(1/4)` (`η = 1/4`) | 1.205581 | 1.208682 | 1.209744 | 1.210315 | **0.39 %** |
| `τ(r) · L^(3/8)` | 1.220156 | 1.227011 | 1.229375 | 1.230602 | **0.86 %** |
| **`U(r) · L^(3/8)`** (connected 3-point) | −0.459288 | −0.458095 | −0.457705 | −0.457548 | **0.38 %** |

and the **parameter-free** consequence — take the exact moments at `L₁`, multiply by
`(L₂/L₁)^(−1/8)` per spin, evaluate the share exactly — predicts the next lattice's share
with residual **+2.25 %, +0.43 %, +0.18 %** (shrinking). Extended by the same rule and no
new input, it predicts an **independent Monte Carlo** at `L = 24` and `L = 32` to
**0.18 %** and **0.39 %**, and reproduces the sibling's `L = 8` and `L = 16` ridge values to
**0.8 %** and **0.4 %**.

**Three things the mission asked about came out differently from the hypothesis, and each is
reported as the interesting part rather than smoothed over.**

1. **`⟨σσε⟩` is not the operative object, and `C_σσε = 1/2` does not set the amplitude.**
   Pre-registered as a correction in Step D *before* running anything.
2. **The "connected information is quadratic in the connected correlator" route is wrong
   here — by a factor of 44 to 145.** `Δτ ≠ U`: the ratio `U/Δτ` tends to **6.6, 8.2, 12.1**
   (at `L = 16, 12, 8`) as `h → 0`, not to 1. The reason is not the field: it is that at
   `T_c` the *pair* correlations stay `O(1)` at every field, and that is the small parameter
   the route needs. The **exact** relation of Step A does hold, verified to **six digits**.
3. **The pre-registered `L^(−3/4)` amplitude exponent FIRED — and the CFT is not what
   failed.** The correlators scale perfectly; the *instrument* is far from its asymptotic
   regime, because the approach parameter is `λ = L^(−1/8)`, which moves 8 % per doubling.
   `I_C^(3)` along the exact scaling ray is **non-monotonic in `L` with a maximum at
   `L ≈ 19`**, and the local slope reaches `−0.75` only for `L ≳ 10⁵`. **The sibling's
   "flat across `L` = 8→64" is exactly this maximum, and is now explained quantitatively.**

**Scorecard against what was written down in advance.**

| | prediction | outcome |
|---|---|---|
| **E4** | moments collapse with `1/8, 1/4, 3/8` | **SURVIVES** — ≤ 0.1 % on the largest pair; confirmed independently by Monte Carlo (`m`: −0.1237, `U`: −0.3863) |
| **E7** | parameter-free moment rescaling (**primary**) | **SURVIVES** — 0.18 % |
| **E3** | `I_C^(3) ∝ h²` at small `h` (**gate**) | **PASSES** — 2.000 to four figures, and `Δτ ∝ h^1.000` |
| **E2** | ridge amplitude `∝ L^(−3/4)` | **FIRES** — and is explained; see §5 |
| **E5** | `L^(3/4) I_C^(3)` collapses | **FIRES** — same cause as E2 |
| **E8** | `r`-dependence is a crossover in `r/L`, not a power law | **SURVIVES** |
| **E1** | `h*(L) ∝ L^(−15/8)` | **SURVIVES** on the collapse reading: **`y_h = 1.8655 ± 0.0081`**, and **1.8742** from `U` alone. Marginal (`−1.97`) on the peak-locus reading, which §6 shows is the wrong ruler |
| **E6** | `r_sat ∝ h^(−8/15)` | **FIRES.** The pre-registered observable is unmeasurable (integer `r`); a substituted exact one gives `−0.5286` vs `−0.5333` but outside the pre-registration's own validity window, so it is not scored as a pass. See §8 |
| **G5** | `Δτ ≈ U` | **FAILS**, as the pre-registration required be checked before use |

---

## 1. GATES

| | |
|---|---|
| **G1** | exact transfer matrix vs the sibling's exact `2^N` enumeration, `4×4`, 8 `(T,h)` points: **max \|ΔI_C^(3)\| = 2.220e-16**. Two independent exact methods, machine precision. |
| **G2** | *the lemma.* `h = 0`, `L = 4…12`, three temperatures, every `r`: **max \|I_C^(3)\| = 4.441e-16** |
| **G3** | `lanczos(k=120)` vs untruncated `full` at `L = 12, 14`: **4.441e-16**; `k=60` vs `k=120`: 2.4e-13; at `L = 20`, `k=24` vs `k=100`: **9e-13** |
| **G4** | Onsager: `⟨s₀s₁⟩` at `T_c`, `h=0` runs 0.758437 (`L`=6) → 0.738121 (10) → 0.729298 (14) → **0.726532** (16), against `√2/2 = 0.707107` |
| **G6** | growth-then-turnover in `r` reproduced in the exact arm — the sibling's separation scan is confirmed, not merely repeated |
| **G7** | Arm B vs Arm A at `L = 16`: `I_C^(3)` **4.806230e-03 ± 1.25e-05** (MC) vs **4.804784e-03** (exact) — **0.03 %** |
| **G5** | **FAILED**, and therefore the weak-coupling route was not used. See §4. |

The lemma reading machine zero is `Core/SignSymmetry.lean` again, now on a second exact
solver: it is the lattice statement of the CFT's own `Z₂` selection rule `C_σσσ = 0`.

## 2. WHY THE PRIMARY ARM IS NOT MONTE CARLO

The sibling's honest weakness was that the ridge points are the hardest to sample: no cluster
algorithm exists in a field, variance inflation `F` reached `5.5e4`, `N_eff` fell to `3.8e3`,
and 26 % of grid points were discarded. Here the `L×L` torus is solved **exactly**: with
`T = D^(1/2) V D^(1/2)`, the single-row marginal is `w(σ) ∝ [T^L]_{σσ}`, and every moment of
a collinear triple follows to machine precision. `full` (no truncation) for `L ≤ 14`;
`lanczos` for `L ≥ 16`, validated against `full`.

**Arm B is also new, and is the better Monte Carlo estimator.** `I_C^(3)` is an exact smooth
function of five moments, and each moment has an **unbiased** estimator. So Arm B estimates
the *moments* and evaluates the exact function, instead of plugging an 8-cell histogram into
a nested-family entropy gap whose estimator is positively biased at `~1/(2N_eff)`. That is
what removes the floor/`N_eff`/variance-inflation apparatus: at `L = 16` it lands on the exact
answer to 0.03 % with a `0.26 %` error bar, and half the chains are started ordered and half
hot so that a short burn-in would show up as a hot/cold disagreement (`z = 2.31, 0.57, …`).

## 3. THE DERIVATION, and which steps held

**Step A (exact).** Along the one-dimensional pair envelope, `S'(τ_q) = 0` and
`S''= −(1/64)Σ_s p_s^(−1)`, so

> `I_C^(3) = (1/128)·[Σ_s p_s^(−1)]·(Δτ)² + O(Δτ³)`,  `Δτ = τ_p − τ_q = −8t*`.

**Verified where it must be exact.** As `h → 0` at `T_c`, `Δτ → 0` and the cubic remainder
must vanish:

| `L` | `h/h*` = 1e−4 | 1e−3 | 1e−2 | 1e−1 | 1 |
|---|---|---|---|---|---|
| 8 | 1.000000 | 1.000000 | 0.999971 | 0.997114 | 0.866035 |
| 12 | 1.000001 | 1.000000 | 0.999969 | 0.996957 | 0.878067 |
| 16 | 1.000001 | 1.000000 | 0.999970 | 0.996987 | (0.8919) |

(the ratio `I_C^(3) / [(1/128)Σp_s^(−1)Δτ²]`). **Step A is confirmed to six digits**, and
even on the ridge itself it accounts for 87–90 % of the share, improving with `L`.

**Step B (leading order) — REFUTED, and the reason is not the field.** `Δτ = U` requires all
*connected* correlators to be small. At `T_c` the pair correlations are `c(r) = 0.66, 0.60,
0.56` at `L = 8, 12, 16` **at any field**, so the expansion never applies on the critical
line. In the deep linear-response limit `h → 0`:

| `L` | `c(r)` | `U/Δτ` as `h → 0` |
|---|---|---|
| 8 | 0.6648 | **12.058** |
| 12 | 0.6005 | **8.196** |
| 16 | 0.5587 | **6.640** |

A finite, `L`-dependent limit, not 1. So the mission's suggested route `I_C^(3) ~ ½U²`
overstates the share by `(U/Δτ)²` ≈ **44 to 145** in the linear regime, and by 2.3–6.1× on
the ridge itself. The route is not merely imprecise here; it has the wrong exponent in `L`,
because `U` carries `L^(−3/8)` cleanly while `Δτ` does not (see §5).

This is the trap `Core/SignSymmetry.lean` already records in prose — *"a large three-point
correlation function is NOT order-3 structure"* — now with a number attached: on the critical
ridge the correlator and the structure differ by an order of magnitude, in a way that does
not go away as the symmetry-breaking field is turned off.

**Step C (exact given universality).** `U(r;h,L) = L^(−3/8) Ψ(r/L, hL^(15/8))`. This is what
E4 tests, and it holds.

**Step D — the correction to the stated hypothesis, pre-registered before any numerics.** The
mission proposed that the leading structure is "governed by `⟨σσε⟩` with `C_σσε = 1/2`". It
is not. Our triple is three **spins**; the object is `⟨σσσ⟩` in the field-perturbed theory,
whose linear-response kernel is the σ **four**-point function — `C_σσε` enters *squared* and
alongside the identity block, and `I_C^(3)` is not proportional to it. `⟨σσε⟩` governs
short-distance corrections, not the ridge; and the ridge sits at `u = O(1)`, which is not
perturbative in `h` at all, so no single OPE coefficient sets its amplitude. What the CFT
supplies at the ridge is the **scaling form and its exponents** — and those are exactly what
survived.

## 4. E4 — THE CFT CONTENT (the result)

Table in the headline. Two further checks:

**The collapse also holds in `r/L`, which is the three-point function's own shape.**
`U(r)·L^(3/8)` at matched `r/L = 1/4`: −0.4593, −0.4581, −0.4577, −0.4575 across `L` = 8→20.
At `r/L = 1/2` the pair correlator `c·L^(1/4)` gives 1.1619, 1.1656, 1.1670, 1.1677.

**Monte Carlo confirms it independently, over a different range and a different method.**
Arm B at `L = 16, 24, 32` (matched `u = 3`, `r/L = 1/4`):

| `L` | `m` | `τ` | `U` | `I_C^(3)` (from the moments) |
|---|---|---|---|---|
| 16 | 0.67336 ± 0.00037 | 0.43444 ± 0.00026 | −0.162418 | 4.806230e−03 ± 1.25e−05 |
| 24 | 0.64111 ± 0.00034 | 0.37406 ± 0.00021 | −0.138928 | 4.663187e−03 ± 1.21e−05 |
| 32 | 0.61869 ± 0.00033 | 0.33603 ± 0.00019 | −0.124316 | 4.319299e−03 ± 1.16e−05 |

fitted exponents `m`: **−0.1237** (predicted −0.125), `U`: **−0.3863** (predicted −0.375).

## 5. E2 FIRED — and the CFT is not what failed

The pre-registered amplitude exponent `−3/4` follows from `U ~ L^(−3/8)` **plus** the
weak-coupling square. The first half holds; the second does not, and E2 fires with it.

Because every moment carries one power of `λ = L^(−1/8)` per spin, the whole three-spin
distribution moves along a **one-parameter ray**, and `I_C^(3)` is an exact function of `λ`
on it. Evaluating that function — no new input, the amplitudes read off the exact `L = 20`
lattice:

| `L` | 8 | 12 | 16 | **20** | 24 | 32 | 48 | 64 | 128 | 4096 | 10⁵ | 10⁷ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ray `I_C^(3)` ×10³ | 3.442 | 4.536 | 4.794 | **4.774** | 4.655 | 4.336 | 3.742 | 3.287 | 2.268 | 0.209 | 0.019 | 0.0006 |
| local `dlnI/dlnL` | — | +0.680 | +0.192 | **−0.018** | −0.139 | −0.246 | −0.364 | −0.450 | −0.535 | −0.718 | −0.749 | −0.753 |

**The ridge amplitude has a maximum at `L ≈ 19` and the entire accessible range sits on it.**
The `−3/4` asymptote is real but is reached only for `L ≳ 10⁵`; at `L = 4096` the slope is
still `−0.718`. **E2 is therefore not a failure of the CFT but a statement about the
instrument**: the pairwise-blind share is a strongly nonlinear function of the moments, and
`L^(−1/8)` is too slow a knob to reach its quadratic regime on any lattice anyone will build.
Equivalently, `Δτ·L^(3/8)` drifts 12 % per size step while `U·L^(3/8)` drifts 0.03 %.

**The ray is predictive, not descriptive.** Calibrated on exact `L = 20` and extended with no
free parameter:

| | ray | measured | residual |
|---|---|---|---|
| Arm B Monte Carlo, `L = 24` | 4.6547e−03 | 4.663187e−03 ± 1.21e−05 | **+0.18 %** |
| Arm B Monte Carlo, `L = 32` | 4.3364e−03 | 4.319299e−03 ± 1.16e−05 | **−0.39 %** |
| ray local slope `L` 16→24 | −0.073 | −0.075 | |
| ray local slope `L` 24→32 | −0.246 | −0.266 | |

**Head-to-head with the sibling's independent Monte Carlo, at the sibling's own ridge
field.** Their `h*(L)` corresponds to `u = 2.835`; the exact arm was rerun at `u = 2.836`
and the ray rebuilt from its `L = 20` amplitudes. Their values are read from
`ising_mc_ridge.json`, geometry `colin-r(L/4)`:

| `L` | sibling, Monte Carlo | this work | residual |
|---|---|---|---|
| 8 | 3.6704e−03 | **3.6992e−03** (exact transfer matrix) | +0.78 % |
| 16 | 4.9454e−03 | **4.9656e−03** (exact transfer matrix) | +0.41 % |
| 32 | 4.5626e−03 | **4.5720e−03** (ray, no free parameter) | **+0.21 %** |
| 64 | 3.6999e−03 | **3.5371e−03** (ray, no free parameter) | −4.40 % |

The exact arm confirms their measurement where it can reach, and the parameter-free CFT
scaling ray reproduces the rest of their curve — including the turnover — over an 8× range in
linear size. (`L = 64` is the point they themselves flagged as least reliable, `N_eff` =
3.8e3.) **Their measurement was right; only its reading as "flat, therefore no critical
scaling" needs amending.** E4 and E7 are unchanged at this `u`: moment drifts 0.04 %, 0.04 %,
0.10 %, 0.03 %, and the E7 residuals +2.22 %, +0.43 %, +0.18 % — so neither result depends on
the choice of `u`.

## 6. E1 — the ridge locus, and why the peak is the wrong ruler

The pre-registered procedure (locate `h*` by maximising `I_C^(3)`) gives, at sub-grid
resolution by parabolic fit:

| `L` | 8 | 12 | 16 | 20 |
|---|---|---|---|---|
| `u* = h* L^(15/8)` | 2.6729 | 2.5787 | 2.5092 | 2.4491 |
| local slope of `h*(L)` | — | −1.9635 | −1.9700 | −1.9836 |

`−1.97` against the predicted `−1.875`: **marginal** by the pre-registered thresholds
(outside ±0.06, inside ±0.15). *The coarse scan inside `cft_ridge.py --hscan` reported
"FIRES" at `−2.12`; that verdict is void — its `u` grid has 5.6 % spacing, which alone
produces ±0.11 of slope error, so it could not test at the pre-registered precision. The
arithmetic is disclosed rather than the threshold moved.*

But the drift in `u*` has the **same cause as E2**: `I_C^(3)` is a nonlinear function of the
moments, so its maximiser inherits an `L`-dependence through `λ` even when the scaling is
exact. The peak of an entropy gap is not a scaling observable. The moments are.

**E1 measured from the collapse instead.** If the magnetic eigenvalue were `y ≠ 15/8`, then
holding `u = hL^(15/8)` fixed would hold the true argument fixed only up to `L^(y − 15/8)`,
and each rescaled moment would drift by `(dln f/dln u)(y − 15/8)ln(L₂/L₁)`. Measuring that
one derivative turns the observed drift into a value for `y`. Nothing is fitted:

| moment | rescaled drift, `L` 16→20 | `dln\|X\|/dln u` | inferred `y_h` |
|---|---|---|---|
| `m` | +0.040 % | +0.3997 | 1.8705 |
| `c(r)` | +0.047 % | +0.0951 | 1.8528 |
| `τ` | +0.100 % | +0.4325 | 1.8647 |
| **`U`** (the three-point function) | −0.034 % | −1.9436 | **1.8742** |

> **`y_h = 1.8655 ± 0.0081`** (spread across moments) against `15/8 = 1.8750`.
> From the connected three-point function alone, **1.8742** — `15/8` to 0.04 %.

**E1 survives** on this reading, by the same ±0.06 threshold that was pre-registered. That
the peak-locus route and the collapse route disagree is itself the §5 result: entropy-gap
observables carry an extra `L`-dependence that pure correlators do not.

## 7. E8 / E5 — the `r`-dependence, and why K4 fired for the sibling

`I_C^(3)` on the ridge rises with separation and turns over near `r/L ≈ 0.3`. The exact arm
shows the turnover the sibling's scan stopped just short of, and its cause is geometric, not
physical: for the collinear triple `(0, r, 2r)` on a ring the separations are
`(r, min(2r, L−2r), r)`, so beyond `r = L/4` the third site comes back toward the first.
`r = L/4` is the maximally-spread configuration and the right fixed ratio.

| `L = 16`, `u = 3` | r=1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| `I_C^(3)` ×10³ (exact) | 0.680 | 2.498 | 3.906 | 4.805 | **5.260** | 5.111 | 3.675 |
| `I_C^(3)` ×10³ (Arm B MC) | 0.682 | 2.503 | 3.908 | 4.806 | **5.259** | 5.109 | 3.672 |

**E8 survives**: the `r`-dependence is a crossover in `r/L`, not a power law, with
`W(r/L → 0) → 0` because a coincident triple is degenerate and has share exactly zero.
`E5` fires with `E2`: `L^(3/4) I_C^(3)` at `r/L = 1/4` runs 0.0173, 0.0295, 0.0384, 0.0452
— it does not collapse, for the reason in §5. **The sibling's K4 (that `star` would carry the
peak) fired for a real reason**: on the ridge the structure is carried by the collective mode
whose amplitude is set by `Δ_σ`, and separation helps until the ring geometry brings the
triple back together.

## 8. E6 FIRED — and the honest reading is that it was not testable

The prediction `ξ ∝ h^(−1/y_h) = h^(−0.533)` needs `1 ≪ ξ ≪ L`. Three instruments were
tried; the third is exact (`ξ = 1 / ln(λ₁/λ₂)` from the transfer matrix, no fit):

| `L = 16`, `u = hL^(15/8)` | 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 |
|---|---|---|---|---|---|---|---|---|
| `ξ` | 13.21 | 8.00 | 4.29 | 2.29 | 1.42 | 0.98 | 0.68 | 0.48 |
| local slope | — | −0.723 | −0.899 | −0.908 | −0.687 | −0.538 | −0.524 | −0.517 |

At `h = 0` the strip pins `ξ` at `4L/π = 20.4`, so everything with `ξ ≳ L/4` is
strip-dominated; everything with `ξ ≲ 1.5` is below one lattice spacing. **The
pre-registered window is essentially empty at `L ≤ 20` — one point per size.**

Two separate things then have to be said, and they point different ways.

**The pre-registered observable could not be measured at all.** `r_sat` was to be read off
the share-vs-`r` curve, but `r` is an integer and above `h ≈ 4h*` the curve peaks at `r = 1`,
so `r₉₀` saturates at the lattice spacing and carries no information (`cft_sat.json`).

**A substituted observable does confirm the exponent — outside the window the
pre-registration itself demanded.** Checking size-independence at matched `h` across three
strip widths:

| `h` | 0.05 | 0.10 | 0.20 | 0.40 | 0.80 |
|---|---|---|---|---|---|
| `ξ` (`L`=20) | 1.9377 | 1.3229 | 0.9171 | 0.6382 | 0.4466 |
| spread over `L` = 14, 17, 20 | 15.3 % | 1.2 % | **0.017 %** | **0.000 %** | **0.000 %** |
| local slope | — | −0.5507 | −0.5285 | −0.5230 | −0.5151 |

For `h ≥ 0.1` the gap is **bulk** to 1.2 % and to 0.02 % beyond, and the fitted exponent is
**−0.5286** against the predicted `−8/15 = −0.5333` — 0.9 %. But `ξ` there is 1.9 down to
0.45 lattice spacings, which is not `ξ ≫ 1`.

**So E6 is recorded as fired, and the substituted measurement is labelled post-hoc.** The
pre-registration set a validity window that the accessible sizes cannot satisfy; that is a
defect of the pre-registration. The bulk-scaling condition it was *meant* to enforce is
demonstrably met in the sub-lattice regime, and there the exponent agrees — but reading that
as a pass would be moving the goalposts after the fact, so it is not scored as one. **This is
the weakest part of the study.** What would settle it: `L ≳ 100`, where `ξ ∈ [3, 25]` is
available, reachable by Monte Carlo on `c(d)` but not by exact transfer matrix.

The earlier `cosh`-fit passes (`cft_sat.json`, `cft_sat2.json`, slopes −0.13 to −0.26) are
**superseded and wrong**: near the ridge `c(d)` is dominated by a non-decaying zero-mode
plateau (fitted values 0.52–0.69), which pins any real-space `ξ` fit at the lattice scale.
Recorded because the failure mode outlives this experiment.

## 9. E3 — the `h²` gate, which is a gate

At `T_c`, fixed `L` and `r`, small `h`: local slopes of `I_C^(3)(h)` are **2.000, 2.000,
2.000** (four figures) at `L = 8, 12, 16`, and `Δτ ∝ h^1.000`. **The gate passes.** As
pre-registered, this is *not* evidence for the CFT: it follows from `Z₂` plus analyticity in
`h` at finite `L` whatever the mechanism. The sibling's measured `2.000`, which the mission
called "a strong hint the quadratic route is right", is consistent with the CFT and equally
consistent with everything else — and the quadratic route is in fact wrong here (§3).
*(The scoring helper in `cft_ridge.py` labelled E3 "FIRES" because it reads the largest-`h`
local slope, where higher orders enter and the slope falls to 1.85. That is a reporting bug
in the helper, not a result; the pre-registered claim is the small-`h` regime.)*

## 10. HONESTY LEDGER

- Arm A carries **no statistical error**; the only approximation is the Lanczos truncation,
  whose retained-weight residual is `1e-16` at `k = 100` and `6e-11` at `k = 24`, and
  `k`-doubling changes `I_C^(3)` by `9e-13`.
- Arm A reaches only `L ≤ 20` and only **collinear, single-row** triples. `star` spans two
  rows and is out of its reach; that geometry is untouched here.
- Arm B error bars are replica-bootstrap across independent chains, so within-chain
  correlation is absorbed rather than modelled; hot/cold starts test burn-in
  (`z = 2.31, 0.57, 0.53`). `z = 2.31` at `L = 16` is the largest and is the one point where
  Arm A independently confirms the answer, at 0.03 %.
- **Three of eight pre-registered predictions fired** (E2, E5, E6). Two of those (E2, E5)
  are explained and the explanation is itself tested against independent data (§5). One
  (E6) is **not** rescued: its pre-registered observable was unmeasurable and its validity
  window unreachable, which is a defect of the pre-registration.
- **E1 is scored on a reading the pre-registration did not specify** — the moment collapse
  rather than the peak locus. That is a substitution made after seeing the peak-locus result
  drift, and it is flagged as such. Its justification (that an entropy-gap maximiser is not
  a scaling observable) is the same mechanism E2 established independently, but the
  substitution was still post-hoc and both readings are reported.
- One pre-registered gate (**G5**) failed outright, and the pre-registration's instruction
  ("where it is larger, (A)+(B) is reported as inapplicable rather than applied") was
  followed.
- `u = 3.0` was chosen for the collapse run *before* the ridge was located; the fitted `u*`
  is 2.45–2.67. The collapse is at matched `u`, so this does not affect E4/E7; it does mean
  the ray's amplitudes are for `u = 3`, and the ray at the sibling's `u = 2.836` is reported
  separately.
- The `L ≈ 19` maximum is a property of `u = 3` and `r/L = 1/4`; it is not claimed to be
  universal.
- No `k > 3`. No claim about `star`. No claim about any other model.

## 11. WHAT THIS DOES AND DOES NOT ESTABLISH

**Does:**
- Identifies the mechanism of the critical ridge as the **2D Ising CFT's magnetisation
  sector**: `Δ_σ = 1/8`, `η = 1/4`, `y_h = 15/8`, confirmed on the three-point function to
  0.4 %. **This is known physics, discovered in 1944/1984, not by us.** What is ours is
  having measured it with a pairwise-blind instrument.
- Explains the sibling's two open puzzles quantitatively: the flat-in-`L` amplitude (a
  maximum at `L ≈ 19` on the exact scaling ray) and the growth-then-saturation in `r`
  (a crossover in `r/L` closed by ring geometry).
- Refutes, with numbers, the natural "connected information ≈ ½(connected correlator)²"
  route on a critical line, and supplies the exact relation that replaces it.
- Contributes two reusable instruments: an exact torus transfer matrix for `I_C^(3)`, and a
  Monte Carlo estimator that measures **moments** rather than the entropy gap and therefore
  needs no bias floor.
- Confirms `Core/SignSymmetry.lean` a second time, at machine precision, and identifies it
  with the CFT selection rule `C_σσσ = 0`.

**Does not:**
- **Nothing about nature.** A spin lattice is a model.
- Does not establish `y_h = 15/8` from the peak locus (marginal at `−1.97`), nor `ξ(h)`
  (E6 untestable here).
- Does not reach the asymptotic `L^(−3/4)` regime, and shows it is unreachable in practice.
- Does not touch `star`, `k > 3`, or any non-collinear geometry.
- **No promotion to `Stance.lean`.** Any stance change needs a separate refuter pass and
  Eric's review.

## 12. FILES

| | |
|---|---|
| `CFT_RIDGE_PREREG.md` | pre-registration, committed at `de11b97` before any code |
| `cft_ridge.py` | transfer matrix, gates, all pre-registered runs, the scaling ray, Arm B |
| `cft_e1_fine.py` | E1 at sub-grid resolution (parabolic fit in `ln u`) |
| `cft_gate.log`, `cft_collapse.log`, `cft_hscan.log`, `cft_mc.log`, `cft_stepa.log`, `cft_gap.log`, `cft_bulk.log`, `cft_e1_fine.log`, `cft_collapse_u2836.log`, `cft_ktest.log` | run logs, including the superseded `xi` fits |
| `cft_collapse{,_u2836}.json`, `cft_e7{,_u2836}.json`, `cft_ray_A{,_u2836}.json` (`_u2836` = the sibling's ridge field), `cft_ray_B.json`, `cft_rscan.json`, `cft_hscan.json`, `cft_hsq.json`, `cft_mc.json`, `cft_stepa.json`, `cft_sat.json`, `cft_sat2.json`, `cft_gap.json`, `cft_bulk.json`, `cft_yh.json`, `cft_e1_fine.json` | raw results |
