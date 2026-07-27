# The pump's SECOND axis — following AMENDMENT 3's reframing where it leads

**Why this exists.** `PUMP_RESULTS.md` AMENDMENT 3 reframes the pump as a convex combination:
a per-cell channel is linear and `ferro` is a two-point mixture, so the pumped state is
`½K(δ₀₀₀) + ½K(δ₁₁₁)` — two **product** states, each share exactly zero, whose mixture is not.
That is right, it is better than "the rate at which noise pumps", and **it has consequences the
reframing itself did not chase.** This document chases them.

Artifacts: `pump_mixture_axis.py` / `.json` / `.log`. All exact, k = 3 and k = 4, CPU, seconds.

---

## THE FOUR FINDINGS

1. **The decomposition is exact** — and it makes the pumped state a **one-hidden-bit model**.
2. **There is a second pump axis, and it obeys the same quadratic law.** Detuning the mixture
   weight off ½ makes a **unital** channel mint, exponent **1.999**.
3. **That axis has its own closed form**, derived here and verified to 0.04 %. It behaves
   **oppositely in noise strength** to the published one.
4. **`PUMP_RESULTS.md` §2's "fifth floor nobody budgeted for" is not a fifth floor.** The k ≥ 4
   symmetric-noise floor **is** the k = 3 state-asymmetry pump — an identity to **8.9e-16** across
   eleven strengths, with the mechanism verified.

---

## 1. The decomposition, and what it makes the state

Checked at `(a, s) = (0.2, 0.15)`:

| | |
|---|---|
| `\|K(ferro) − ½[K(δ₀₀₀) + K(δ₁₁₁)]\|` | **0.000e+00** |
| share of component `K(δ₀₀₀)` | 1.1e-16 |
| share of component `K(δ₁₁₁)` | −2.2e-16 |
| share of the 50/50 mixture | **1.894e-02** |

Constituents exactly zero, combination positive. AMENDMENT 3 is right.

**And the structure has a name.** Each component is a product state, so the pumped state is a
latent binary variable choosing between two product distributions, with the three slots
**conditionally independent given it**. That is the *hidden-element* model — and it is
**Schneidman et al. 2003 Fig. 3**, not Fig. 2:

> "if we observe only some of the elements of a network then the effect of the hidden elements may
> be to create new effective interactions among the observed elements. As examples (Fig. 3), when
> one hidden binary element determines the nature of pure pairwise interaction among the remaining
> elements, the observable subnetwork can have an effective 3–body interaction."

Fig. 3's abscissa is `γ = P(σ₄ = 0)` — **the mixture weight**. Fig. 2's is the noise amplitude.
**They are the campaign's two axes**, and the reframing puts us adjacent to both figures of the
same 2003 paper rather than one. It is also the mechanism of the dichotomized-Gaussian /
common-input literature (`PUMP_PRIOR_ART_ADDENDUM.md` §A4).

**One claim to temper.** "Our closed form answers the question Kahle called unsolved" is too
strong. Kahle et al. asked, in general, *whether the complexity of a convex combination of two
distributions is related to the complexities of its constituents.* We give a closed form for
**one two-parameter family of pairs of product states on three binary slots, in the small-detuning
limit**. That is a worked special case of their question, not an answer to it — and Schneidman had
already computed the two-component hidden-bit case numerically in 2003, six years before they
called it unsolved.

---

## 2. The second axis: a UNITAL channel pumps once the mixture is detuned

Let `mix(γ) = γ·δ₀₀₀ + (1−γ)·δ₁₁₁`. Its pair marginals are `(γ, 0, 0, 1−γ)` — perfectly
correlated — so the pair-maxent **is** the state and its share is **exactly zero at every γ**
(measured: 0.000e+00 over seven weights). A clean axis.

At `γ = ½` the input is sign-symmetric and `valve_needs_asymmetry` forces zero. **Off ½ it does
not apply**, and the unital channel mints (share in nats, `a = 0` throughout):

| γ | s=0.05 | s=0.10 | s=0.20 | s=0.30 |
|---|---|---|---|---|
| **0.50** | **0.0** | **4.4e-16** | **0.0** | **0.0** |
| 0.45 | 2.246e-04 | 2.829e-04 | 1.660e-04 | 3.485e-05 |
| 0.40 | 8.962e-04 | 1.125e-03 | 6.528e-04 | 1.348e-04 |
| 0.30 | 3.543e-03 | 4.368e-03 | 2.415e-03 | 4.649e-04 |
| 0.20 | 7.724e-03 | 9.148e-03 | 4.545e-03 | 7.548e-04 |
| 0.10 | 1.236e-02 | 1.323e-02 | 5.048e-03 | 6.094e-04 |
| 0.05 | 1.307e-02 | 1.209e-02 | 3.242e-03 | 2.804e-04 |

**Exponent in the detuning `δ = ½ − γ`: 1.999 (s=0.1) and 1.998 (s=0.2).** The same quadratic law
as the channel axis, for the same information-geometric reason (`PUMP_PRIOR_ART_ADDENDUM.md` §A3).

Peak of the axis: **1.335e-02 nat (1.93 % of ln 2) at γ = 0.0875, s = 0.1**.

---

## 3. Its closed form, derived — and it is the channel law's mirror image

Same route as `PUMP_PREREG.md` §4.3, with the input's **magnetisation** carrying the detuning
instead of the channel's asymmetry. `mix(γ)` has `m = −2δ`, `r = 1`, `c = −2δ`; a unital kernel
sends these to `m = −2δκ`, `r = κ²`, `c = −2δκ³`. The maximiser `c* = 3rm/(1+2r)` gives
`Δc = 4δκ³(1−κ²)/(1+2κ²)`, and `Δ = ½|g''|(Δc)²` with `|g''| = (1+2r)/[(1+3r)(1−r)]`:

> **`Δ = 8·δ²·κ⁶·(1−κ²) / [(1+2κ²)(1+3κ²)]`,  `δ = ½ − γ`,  `κ = 1−2s`**

Tested against the exact solver over 16 configurations: ratio **1.0000–1.0004 at δ = 0.01**,
degrading to 1.045 at δ = 0.10 exactly as an `O(δ⁴)`-truncated expansion should. Worst deviation
over the grid 4.5 %, and under 0.1 % throughout the small-detuning region.

**The contrast with the published law is the point, and it is qualitative:**

| | channel axis | state axis |
|---|---|---|
| law | `18 r₀⁴ a² / [(1+2r₀)(1+3r₀)**(1−r₀)**]` | `8 δ² κ⁶ **(1−κ²)** / [(1+2κ²)(1+3κ²)]` |
| the `(1−·)` factor | **denominator** | **numerator** |
| as noise → 0 | **diverges** — the pump is strongest at weak noise | **vanishes** — no noise, no mixing, no pump |
| peak in strength | none; monotone | **s = 0.0999, κ = 0.800** |
| strength coefficient at s = 0.01 / 0.10 / 0.30 | 34.1 / 1.26 / 0.0072 | 0.025 / **0.113** / 0.014 |

**`PUMP_RESULTS.md`'s headline "strength is a savage brake" is an axis-specific statement.** On
the channel axis it is right — `κ⁸` suppression. On the state axis strength is **the enabling
ingredient**: at zero noise the two components stay disjoint and no mixing occurs, so the pump
peaks at `s ≈ 0.10` and dies in both limits. Any downstream floor estimate must say which axis it
is on.

---

## 4. §2's "fifth floor" is the second axis, not a fifth thing

`PUMP_RESULTS.md` §2 reports that at k ≥ 4 a symmetric channel mints from a sign-symmetric state —
"a fifth floor nobody had budgeted for". Measured here:

> **`shareK₄(repetition₄ through BSC(s))` = `share₃(mix(γ=s) through BSC(s))`, exactly.**

| s | 0.02 | 0.05 | 0.10 | 0.20 | 0.30 | 0.40 | 0.45 |
|---|---|---|---|---|---|---|---|
| k=4 floor | 7.1521e-03 | 1.30669e-02 | 1.32325e-02 | 4.54485e-03 | 4.64918e-04 | 3.79296e-06 | 1.84874e-08 |
| k=3, γ=s | 7.1521e-03 | 1.30669e-02 | 1.32325e-02 | 4.54485e-03 | 4.64918e-04 | 3.79296e-06 | 1.84874e-08 |

**Worst difference over eleven strengths: 8.9e-16.**

**The mechanism, verified not asserted.** Condition the k = 4 pumped state on slot 4. Its marginal
is uniform, and the posterior on the hidden bit is exactly `(s, 1−s)` — so slots 1–3 given
slot 4 = 1 **are** the `γ = s` three-slot mixture. Checked at s = 0.17: the conditional matches
the pushed mixture to **5.6e-17**, and its k = 3 share equals the k = 4 `shareK` to all digits
(7.0108351698e-03 both).

**So the two findings are one finding.** The k ≥ 4 floor is not a new mechanism that appears at
four slots; it is the state-asymmetry pump, with the fourth slot playing the role of the latent
bit that detunes the mixture seen by the other three. `PUMP_RESULTS.md` §2's structural
explanation (even-order characters survive the sign flip, count `0, 1, 5, 16, 42` —
`PUMP_RESULTS_ADDENDUM.md` §A2) says *which directions* carry it; this says *what it is*.

**Caveat, stated because it is not proved.** That `shareK₄` equals the k = 3 share of this
particular conditional is a **measured identity on this family**, not a general theorem. Whether
it holds for other one-hidden-bit models, or at k ≥ 5, is untested here.

---

## 5. WHAT THIS CHANGES

| # | for | change |
|---|---|---|
| 1 | `PUMP_RESULTS.md` §8 | the downstream list has **four** floors, not five: the k ≥ 4 floor and the state-asymmetry pump are the same object, and one closed form covers both |
| 2 | `PUMP_RESULTS.md` §1 | "strength is a savage brake" is **channel-axis only**; on the state axis strength is the enabling ingredient and the pump peaks at s ≈ 0.10 |
| 3 | §9 / prior art | the reframing puts us adjacent to Schneidman **Fig. 3** as well as Fig. 2 — the same paper, the other axis; and the Kahle "unsolved" claim should read *a worked special case*, not an answer |
| 4 | any downstream floor | **two** laws, and a substrate can sit on either. Sky, glass and water substrates are not sign-symmetric, so the **state axis is the one that applies to them**, not the published channel law |

**Item 4 is the one that matters downstream.** `PUMP_RESULTS.md` §8 licenses mappings from the
channel-asymmetry law. But the channel law's `a = 0` control is theorem-pinned **only on
sign-symmetric inputs** (`PUMP_PRIOR_ART_ADDENDUM.md` §A2), and real substrates are generically
detuned. For those, the governing law is `8δ²κ⁶(1−κ²)/[(1+2κ²)(1+3κ²)]` — which **peaks at
intermediate noise instead of decaying**, and therefore does **not** license the reassuring
`κ⁸`-suppression argument. Any floor estimated from the channel law on a non-sign-symmetric
substrate is estimated from the wrong axis.

---

*Exact computation throughout, k = 3 and k = 4, no sampling, no fit except the two exponents.
Solver gated at `a4d3b38`. No Lean touched, `lake` never run, nothing moves `Stance.lean`.*
