# g_c DERIVED — the rent function `f`, from the induced chain's spectrum

**Brick:** `OBJECT_INVARIANT_HUNT.md` remainder item 4 — *"W\* priced by T_c's spectral gap —
the H1′ function f, derived not fitted."*
**Date:** 2026-08-26. **Author lane:** gcost.
**Status of this file:** the derivation and its staked expectations, written and frozen
**before** `gcost_check.py` was written or run. The numeric check is §7's stakes, adjudicated in
`gcost_check.py`'s output; the confrontation with existing substrate data is `gcost_confront.md`.

**No fitted parameters appear anywhere in this file.** Every constant in every prediction is
either (a) read off the substrate's own measured decay, or (b) a target the user chooses (`δ`).
Any step that would need a fit is flagged in **FIT-FLAG** boxes and is not used in a prediction.

---

## 0. What the kill left standing, and what has to be derived

`scratchpad/atlas/ATLAS_V1_RESULTS.md` H1 killed the naive bridge: the 2-bit parity view
`c = a⊕b⊕1` is **exactly closed** under iid flip noise (Δ_v ≡ 0 at every ε) while the cost of
holding it at 0.99 runs 0.794 → 0.970. No `f(Δ_v)` can price `W*`, because the left side is zero
where the right side is large.

The kill named its own successor: *"maintenance is priced on the induced dynamics' decay rate."*
That is a claim with no function attached yet. This file attaches the function.

**The object.** A view `v : E → Q` with fibers `Fib_π(c)`; the microscopic step `T` descends to an
induced chain `T_c` on the quotient `Q` (this is exactly what `Closed` buys — `closed_iff_fiber_invariant`,
`rate_unique_on_range`: when the view is closed the quotient dynamics is *determined*, never chosen).
`T_c` is a finite Markov chain. It has its own equilibrium `μ_c` and its own approach to it. The
ledger entry being maintained is the view's **departure from that equilibrium** — the structure
that distinguishes the design state from the washed-out one.

---

## 1. Assumptions, stated once and referred to by name

| tag | assumption | where it bites |
|---|---|---|
| **A1 — finite ergodic quotient** | `T_c` is a finite, irreducible, aperiodic Markov kernel on `Q` with unique stationary `μ_c`, diagonalizable with eigenvalues `1 = λ₁ > \|λ₂\| ≥ … ≥ \|λ_n\|`. Absolute spectral gap `γ ≡ 1 − \|λ₂\|`. | Deterministic quotients (`γ = 0`) are **out of scope** — this is atlas B3's finding stated as a scope line, not an excuse. |
| **A2 — the ledger coordinate is the deviation from `μ_c`** | the tracked amount is `δ_t ≡ p_t − μ_c`, a sum-zero vector, **not** `p_t` itself. The ledger's zero is the induced chain's own equilibrium. | Getting this wrong rescales `δ` and therefore `W*`. Cf. the repo's own `energy-balance-zero-point` lesson: a balance must use the law's own zero. |
| **A3 — single tracked mode (the exact case)** | the design deviation is proportional to one left-eigenvector: `δ₀ = s₀·v_j`, `v_j T_c = λ_j v_j`. Write `λ ≡ λ_j` and **`ε ≡ 1 − λ`**. | §4 removes it and turns the equality into an inequality. |
| **A4 — the repair is an affine deposit ("reading (b)")** | `Rep_q(p) = (1−q)·p + q·p_des`. This is the reading the repo already adjudicated: `Core/Creation.lean`'s `repair_mints_from_noise` (the deposit cannot be proportional to what survives — it mints from pure noise), and `MAINTENANCE_SWEEP_RESULTS.md` P4/P5a/T4 measured it on two substrates. | §6 runs the rejected alternative (reading (a), proportional gain) as the discriminator control. |
| **A5 — order: decay, then repair** | one step is `p ↦ Rep_q(p T_c)`. This is the substrates' own order (noise, then decode). | §3.3 gives the other order exactly: it multiplies retention by `λ`. |
| **A6 — a scalar coordinate suffices** | the tracked quantity is a *number* (a mode amplitude), so the decayed state and the deposit are automatically parallel. | **This is the assumption the holonomy campaign broke.** §5 derives what happens when they are not, and it is the whole content of that substrate's 9.8 % residual. |

**Norm.** Under A3 the tracked amount is a coordinate, so no norm is needed. Where a norm *is*
needed (§4 mixtures, §5 operators) it is the inner-product norm: `χ²(μ_c)` for distributions
(the norm in which a reversible `T_c` is self-adjoint), Frobenius for operators. §5's *inequality*
survives in any norm (triangle inequality); §5's *quantitative* deficit needs the inner product.

---

## 2. The induced chain in ledger coordinates

Deviation from `μ_c` is preserved as a sum-zero vector by `T_c` (`μ_c T_c = μ_c`), so

```
δ_{t+1} = δ_t T_c            (free decay, no repair)
```

Under A3, `δ_t = s_t v`, and

```
s_{t+1} = λ · s_t            ⟹        s_t = λ^t s₀ .
```

**This is `unpaid` of `Core/Maintenance.lean` verbatim**, with the file's decay fraction `γ_Lean`
identified: `unpaid S₀ γ_Lean n = S₀(1−γ_Lean)^n`, so

> **`γ_Lean = 1 − λ = ε` — the per-step multiplicative loss of the tracked component.**

So the answer to "what is ε in chain terms" is:

> **ε is one minus the decay eigenvalue of the tracked mode of the induced chain `T_c`.**
> When the tracked mode is the slowest one, `ε = γ`, the spectral gap. When it is not, `ε > γ`.

Three worked identifications, all forced rather than chosen (each is confronted in `gcost_confront.md`):

| substrate | microscopic noise | tracked mode | `λ` | `ε` |
|---|---|---|---|---|
| atlas 2-bit code `{00,11}` | iid bit flip `ε_flip` | the parity bit `a⊕b` | `(1−2ε_flip)²` | `4ε_flip(1−ε_flip)` |
| LFSR / lattice records | iid bit flip `ε_flip` | Fourier character `χ_T`, `\|T\| = d` | `(1−2ε_flip)^d` | `1 − (1−2ε_flip)^d` |
| Wilson-loop holonomy | per-rung dephasing | the loop's rms singular value | 0.959913 (measured) | 0.040087 |

Note the first two: **ε is not the noise rate.** The noise rate is a microscopic parameter; `ε` is
a property of the *quotient*. Confusing them mis-prices maintenance by a factor of `d` (or of 2).
That distinction is the reason this is a derivation and not a rename.

---

## 3. The stationary retention `G_∞(q)` — derived

### 3.1 The recursion

One maintained step, A4 + A5, in ledger coordinates. The deposit `p_des` has deviation
`δ_des = p_des − μ_c = s₀ v` (the design *is* the full ledger entry, by definition of the entry):

```
δ_{t+1} = (1−q)·(δ_t T_c) + q·δ_des
s_{t+1} = (1−q)·λ·s_t + q·s₀
```

An affine scalar recursion with homogeneous factor `a ≡ (1−q)λ`. For every `q > 0`, `a < 1`, so it
converges from any start — **there is no threshold, as a matter of arithmetic**, which is why the
`q ≥ ε` reading has now failed on three substrates and why H2's kill could not have fired.

### 3.2 The fixed point

```
s_∞ = (1−q)λ s_∞ + q s₀
s_∞ (1 − (1−q)λ) = q s₀
```

Define retention `G_∞(q) ≡ s_∞ / s₀`:

```
              q                 q                    q
G_∞(q) = ───────────── = ───────────── = ─────────────────────
          1 − (1−q)λ        1 − λ + qλ         ε + q λ
```

> ### **THE LAW (derived)**    `G_∞(q) = q / (ε + qλ)`,  `ε = 1 − λ = 1 − (decay eigenvalue of the tracked mode)`

This is the repo's measured closed form exactly — `MAINTENANCE_SWEEP_RESULTS.md` P4
(`p̂_∞ = p̂_0 · q/(1−(1−q)λ^{|T|})`) and `HOLONOMY_RENT_PREREG.md` §4.1 reading (b) — **now
derived from the induced chain rather than posited and fitted.** It is exact under A1–A6 and
carries no free constant: `λ` is a measurable spectral quantity of `T_c`, `q` is the dose.

Sanity limits, all forced:
`G_∞(0) = 0` (`unpaid_decays`); `G_∞(1) = 1/(ε+λ) = 1` (full upkeep buys standing still exactly —
`paid_const`); monotone increasing in `q` (`dG/dq = ε/(ε+qλ)² > 0`); `G → 1` as `ε → 0`.

**Continuous-time form.** With decay rate `γ_c` and repair rate `q_c` per unit time,
`ṡ = −γ_c s + q_c(s₀ − s)` gives `G_∞ = q_c/(q_c + γ_c)`. This is the `ε → 0` limit of the
discrete law; the `λ` in the discrete denominator is purely a one-step discreteness correction.

### 3.3 The other order (repair, then decay)

`s_{t+1} = λ[(1−q)s_t + q s₀]` gives `G_∞ = qλ/(ε + qλ) = λ · G_∞^{A5}`. The two orders differ by
exactly the factor `λ`, i.e. by `O(ε)`. **Any confrontation must name its order**; all three repo
substrates are A5.

### 3.4 A second repair model: damage-conditional reset, and why it lands on the same law

The atlas's repair is not an affine deposit. It is **state-dependent**: repair fires *only when
the state has left the design set*, and then with probability `q`. That is a different channel,
and it is worth deriving separately rather than assuming A4 covers it.

Let `Q` carry a two-block partition `{B₀ (design), B₁ (damaged)}` and suppose the partition is
**exactly lumpable** for `T_c` (Kemeny–Snell: `Σ_{j∈B_k} T_ij` depends only on the block of `i`).
Then the block process is itself a Markov chain, `[[1−α, α],[β, 1−β]]`, with equilibrium
`μ₀ = β/(α+β)` and decay eigenvalue `λ = 1 − α − β`, so `ε = α + β`. Repair: after the step, if the
state is in `B₁`, reset to the design with probability `q`.

The maintained block kernel is `A ≡ P(0|0) = (1−α) + αq`, `B ≡ P(0|1) = β + (1−β)q`, stationary
`π₀ = B/(1−A+B)`. With `1−A+B = (α+β) + qλ` and (after cancellation) numerator `qα`, the ledger
coordinate `s = π₀ − μ₀` against `s₀ = 1 − μ₀ = α/(α+β)` gives

```
G_∞(q) = q / ( (α+β) + qλ ) = q / (ε + qλ) .
```

> **The damage-conditional reset obeys the same law, with `ε` read off the LUMPED chain.**
> Two structurally different repair channels, one retention law — because the law is a property
> of the induced chain's tracked mode, not of the repair's mechanism. This is what "priced by
> `T_c`'s spectral gap" means operationally.

Scope: **the lumping must be exact.** Where the design partition is not lumpable the block process
is not Markov, `λ` is not defined by the partition alone, and the law is not derived. That is
tested, not assumed (E10).

### 3.5 The half-dose

`G_∞(q) = ½ ⟹ q_half = ε/(2−λ) = ε/(1+ε) → ε` as `ε → 0`. (The prereg's form `ε/(2−λ)` and the
form `ε/(1+ε)` are the same number; `2−λ = 1+ε`.) **The half-holding dose is the decay rate**, to
first order in ε — the honest form of the dead `q* = ε` threshold intuition.

---

## 4. `W*` — the minimum repair rate. **This is `f`.**

Invert §3.2 at a retention target `1 − δ` (`δ` = the fractional loss the maintainer will tolerate):

```
   q
─────────  ≥  1 − δ
 ε + qλ
q ≥ (1−δ)ε + (1−δ)λ q
q [1 − (1−δ)λ] ≥ (1−δ)ε
```

and `1 − (1−δ)λ = 1 − λ + δλ = ε + δλ`, so

> ### **THE CANDIDATE `f` (derived)**
> ```
>                (1−δ)·ε              (1−δ)·γ
> W*(γ, δ)  =  ───────────  =  ───────────────────      [ ε = γ, λ = 1−γ ]
>                ε + δ·λ           γ + δ(1−γ)
> ```
> the minimum per-step repair dose that holds the tracked component at retention `≥ 1−δ`
> against an induced chain whose tracked mode decays with gap `γ`.

Equivalently, in terms of the retention target `r = 1 − δ`:  `W* = rγ / (γ + (1−r)(1−γ))`.

### 4.1 What `f` says

| limit | `W*` | reading |
|---|---|---|
| `δ → 1` | `→ 0` | demand nothing, pay nothing |
| `δ → 0` | `→ 1` | **perfect retention costs full upkeep, at any gap** — `q = 1`, and the LFSR's "the rent for perfect maintenance is exactly the noise rate" is the cost-side face of this |
| `γ → 0` | `→ 0` | a non-decaying quotient is free to hold (`rent_holds` with `γ = 0`) |
| small `γ`, fixed `δ` | `W* ≈ γ(1−δ)/δ` | **linear in the gap, hyperbolic in the tolerance.** The clean small-gap law: halving the tolerated loss doubles the rent |
| small `δ`, fixed `γ` | `W* ≈ 1 − δ/γ` | near-perfect retention: the *saving* from tolerating `δ` is `δ/γ`, so a slow chain (small γ) rewards tolerance far more than a fast one |

`W*` is increasing in `γ` (`∂W*/∂γ = δ(1−δ)/(γ+δ(1−γ))² > 0`) and decreasing in `δ`. Both signs
are forced, and both are falsifiable.

### 4.2 `f` is a LOWER BOUND when the tracked component is not a single mode

Drop A3. Let `δ₀ = Σ_j c_j v_j` and let the observable be a linear functional `φ` with
`w_j ≡ c_j⟨φ, v_j⟩`. Each mode obeys §3.2 independently (the recursion is linear and the deposit
is the design's own decomposition), so mode `j` retains `g_j = q/(1−(1−q)λ_j)` and

```
G_∞(q) = Σ_j w_j g_j / Σ_j w_j          — a weighted average of per-mode retentions.
```

`g_j` is increasing in `λ_j`, so for **nonnegative weights**

```
g_min ≤ G_∞ ≤ g_max = q / (1 − (1−q)|λ₂|) = q / (γ + q(1−γ)) ,
```

the single-mode law at the *slowest* mode. Requiring `G_∞ ≥ 1−δ` therefore requires
`g_max ≥ 1−δ`, hence

> **`W*_true ≥ f(γ, δ)`, with equality iff the tracked component is purely the slowest mode.**
> The spectral gap prices the **floor** on maintenance. Anything the view tracks that lives on
> faster modes only raises the bill.

**This derives `MAINTENANCE_SWEEP_RESULTS.md` P5b's own falsification.** P5b staked that retention
collapses onto a one-parameter family in `ρ = q/(2εd)`; it failed, and the results file's diagnosis
("I kept only the `w = d` Fourier mode… the correct form is `share_∞ ≈ ½ Σ_w A_w g_w²` over the
whole weight spectrum… retention is *not* a one-parameter family, and cannot be") is exactly §4.2.
Their measured single-mode correction factor `C = Σ_w A_w (d/w)²/A_d` running 1.02–5.21 across the
roster is the spread this inequality predicts.

### 4.3 Nonlinear observables: the law lives on the AMPLITUDE, not on the reading

`G_∞` is a retention of the **linear mode amplitude**. If the published observable is a nonlinear
function of it — as `share` is — the observable's retention is *not* `G_∞`. For a `k=3` parity
record with amplitude `p̂_∞ = G_∞ · p̂₀`,

```
share_∞ = ln2 − H_b((1 + p̂_∞)/2)  ,     share retention = share_∞ / share₀ .
```

Small-amplitude: `share ≈ ½ p̂²`, so share-retention `≈ G_∞²`. **A confrontation that compares a
share retention to `G_∞` directly is comparing the wrong quantities**, and §3 of `gcost_confront.md`
is where that matters.

Inverting for `W*` at a *share* target: solve `share_∞/share₀ = 1−δ_share` for the required
amplitude `g_req`, set `δ = 1 − g_req`, then apply `f`. No fit; one monotone 1-D inversion.

### 4.4 Schedule: `f` prices the *rate*, and the rate does not determine the price

Three schedules at the same mean effort `q`, all derived:

| schedule | derivation | retention |
|---|---|---|
| **continuous** — deposit strength `q` every step | §3.2 | `q/(ε+qλ)` |
| **stochastic** — full-strength reset with prob. `q` | age since last reset is Geometric(q), `P(age=k) = q(1−q)^k`; `E[λ^age] = q Σ_k (1−q)^k λ^k` | `q/(ε+qλ)` — **identical in mean** |
| **periodic** — full-strength reset every `P = 1/q` steps | ages cycle uniformly over `{0,…,P−1}`; cycle average `= (1/P)Σ_{k<P} λ^k` | `(1−λ^P)/(P(1−λ))` — **different** |

The mechanism, in one line: **a Bernoulli schedule at rate `q` leaves the entry unrepaired for a
mean of `(1−q)/q` steps; a periodic schedule at the same rate leaves it a mean of `(1/q − 1)/2`
steps — half as long.** Regular beats spread-thin because it halves the mean age, not because it
buys more repair.

Consequence for `f`: **`W*` as derived in §4 is the continuous/stochastic dose. A periodic
maintainer holds the same target for strictly less mean effort.** `f` is therefore also a bound in
the schedule axis — the *worst-case-schedule* rent. `HOLONOMY_RENT_RESULTS.md` §8 measured this
and named the same closed form; here it is derived alongside the reason.

---

## 5. Where the scalar derivation cannot be exact — the alignment bound (A6 removed)

The holonomy campaign's finding is that the residual is **operator structure, misalignment-signed,
9.8 %**. That is not noise around `f`; it is a derivable correction, and its derivation bounds
where a scalar `f` can be exact.

Let the tracked object be a vector/operator `X` in an inner-product space with norm `‖·‖`, decay
`X ↦ 𝔅X` with `‖𝔅X‖ ≤ λ‖X‖`, and deposit `D` with `‖D‖ = ‖X_des‖ ≡ 1`. The maintained step is
`X ↦ (1−q)𝔅X + qD`. Write `x = ‖X_∞‖` and let `cos θ` be the (stationary) alignment between
`𝔅X_∞` and `D`.

**(i) The bound, in any norm.** By the triangle inequality
`x ≤ (1−q)λ x + q`, hence

> **`G_∞^{operator} ≤ G_∞^{scalar} = q/(ε+qλ)`, with equality iff the deposit is parallel to the
> decayed state.**  Equivalently **`W*_operator ≥ W*_scalar = f(γ,δ)`.**

`f` is a bound from this side too, and the sign of every deviation is forced: **the measured
plateau must sit at or below the scalar law, never above, at every `q`.**

**(ii) The size of the deficit, in an inner-product norm.** Squaring the fixed point with
`a ≡ (1−q)λ`:

```
x² = a²x² + q² + 2aq x cosθ
(1−a²)x² − 2aq cosθ · x − q² = 0
x = q [ a cosθ + √(a² cos²θ + 1 − a²) ] / (1 − a²)
```

`cosθ = 1` recovers `q/(1−a)` exactly. Expanding near alignment (`cosθ = 1 − u`, `u` small):

```
x ≈ (q/(1−a)) · (1 − a u)      ⟹      relative deficit ≈ − a u = − (1−q) λ (1 − cosθ) .
```

> **Derived shape of the residual:** negative at every `q`; magnitude `∝ (1−q)`; **vanishing at
> `q = 1`** regardless of misalignment. A scalar ledger has one coordinate and cannot be
> misaligned; an operator can, and pays `(1−q)λ(1−cosθ)` for it.

**FIT-FLAG.** `cos θ` is itself `q`-dependent (at `q → 1` the maintained operator *is* the design,
so `cosθ → 1`). No closed form for `cosθ(q)` is derived here and **none is fitted**. The
predictions carried forward are the three parameter-free ones — *sign negative everywhere*,
*magnitude monotone decreasing in `q`*, *→ 0 at `q = 1`* — and nothing else. Anyone who wants the
magnitude must measure `cosθ`; it is an observable, not a constant.

**Scope line this puts on `f`.** A scalar `f(γ, δ)` is exact only where the tracked component is
(a) a single mode of `T_c` and (b) a scalar coordinate. Where the ledger entry is an operator,
`f` is a **lower bound on the rent**, tight as `q → 1` and loosest where maintenance matters most
(`q ≈ ε`). The holonomy substrate is the regime where this is measurable, and its 9.8 % is the
size of the effect on one 64×64 connection.

---

## 6. The discriminator: reading (a) must FAIL

The rejected payment model — proportional gain, `α = c·s` — gives `s_{t+1} = (λ + c)s_t`. With
`c = q`: `G_∞` is `0` for `q < ε`, undefined/`1` at `q = ε`, and divergent for `q > ε`. A hard
threshold at `q = ε`, no interior plateau. This is falsified on all three repo substrates
(P5a, T4, H2) and is run in §7 as a control that **must not** match the measurements. A check in
which both models fit is a check with no power.

---

## 7. STAKES — expectations frozen before `gcost_check.py` exists

Simulated finite chains, numpy only, **zero fitted parameters**. `γ` varied across more than an
order of magnitude. Two repair models (A4 affine deposit; damage-conditional reset, the atlas
model), plus the two extra schedules and the §6 control.

| id | stake | pre-declared pass bar | meaning if it fires |
|---|---|---|---|
| **E1** | single-mode, affine, A5: measured stationary `G_∞` equals `q/(ε+qλ)` | `max abs err < 1e−12` over the whole `(γ,q)` grid | the algebra is right |
| **E2** | `W*` by bisection on the simulated chain equals `f(γ,δ)` | `< 1e−9` (bisection tol) at every `(γ,δ)` | the inversion is right |
| **E3** | generic (multi-mode) initial deviation: `G_measured ≤ G_pred(γ)` and `W*_measured ≥ f(γ,δ)` | **100 % of cells**, and strict wherever off-`v₂` weight is nonzero | §4.2's bound holds; a violation kills the bound |
| **E4** | stochastic dosing mean retention equals the continuous law | `\|mean − pred\| < 3·sd/√N` | §4.4's age argument |
| **E5** | periodic dosing equals `(1−λ^P)/(P(1−λ))` exactly, and **exceeds** continuous at matched `q` | exact to `1e−12`; strict inequality in every cell | schedule-dependence is derived, not measured-and-explained |
| **E6** | **control:** reading (a) (proportional gain) does **not** reproduce the measurements — it shows a threshold at `q=ε` | must show divergence/zero across `q = ε`, i.e. relative error to `f` **> 100 %** somewhere on the grid | the check has discriminating power |
| **E7** | order-of-operations: repair-then-decay retention `= λ ×` decay-then-repair | `< 1e−12` | §3.3 |
| **E8** | the atlas 2-bit chain: exact stationary `P(in code)` reproduces `G = q/(ε+qλ)` with `λ = (1−2ε_flip)²` | `< 1e−12` | the identification of `ε` in §2 is the right one for that substrate |
| **E9** | **second repair model** — damage-conditional reset on an exactly lumpable multi-state chain reproduces `q/(ε+qλ)` with the LUMPED `ε`, and its `W*` matches `f` | `< 1e−12` (G), `< 1e−9` (W*) | §3.4: the law is a property of `T_c`, not of the repair mechanism |
| **E10** | **scope** — damage-conditional reset on a **non-lumpable** partition deviates from the law | deviation must be **> 1e−6** somewhere (a demonstration that the lumpability condition is load-bearing, not decorative). Magnitude is **not** predicted | if this shows *no* deviation the lumpability assumption is idle and should be dropped from the derivation |

**What would falsify `f`.** Named now, before any number:

1. **A finite ergodic quotient with an affine deposit whose stationary retention is not
   `q/(ε+qλ)`** where `ε = 1 − λ_track` — i.e. E1 fails. That kills the law outright.
2. **A measured `W*` strictly BELOW `f(γ,δ)`** on any substrate where `γ` and `δ` are both
   defined and the repair is an affine deposit. §4.2 and §5 make `f` a floor in two independent
   directions; a reading beneath it kills the floor.
3. **A residual on an operator substrate with the wrong sign** — a measured plateau *above*
   `q/(ε+qλ)` — kills §5(i), which is a triangle inequality, and would mean the deposit norm was
   mis-measured.
4. **A knee at `q = ε`** on any substrate — kills A4 in favour of reading (a) and takes `f` with
   it. (Three substrates have already declined to produce one.)
5. **`W*` insensitive to `γ`** at fixed `δ`: `f` says `∂W*/∂γ > 0` strictly. A substrate where
   changing the induced chain's gap does not move the required dose kills the pricing claim even
   if the algebra survives.

**What `f` does NOT claim.** It is a **rate**, not a **work**. Converting `W*` (repair dose per
step) into `βW*` (free energy per step) needs one more measured quantity — the thermodynamic cost
of one repair operation on that substrate — and this file does not supply it. The LFSR arm's
`cost = ε` corrected-bits-per-bit-per-step at `q = 1` is the operation-count face of the `δ → 0`
limit and is derived (at stationarity under full upkeep the decoder corrects exactly what the
noise flipped); the *erasure* currency is not. That is the open half of the H1′ bridge and is
declared as such in `gcost_confront.md` §5 ("Where the mapping is NOT defined").

---

## 7a. POST-RUN LOG — written after `gcost_check.py` ran, kept separate from the frozen stakes

**Result: 11/11 stakes passed** (`gcost_check.out`). One amendment and one instrument fix, both
declared:

1. **E4's frozen bar was an invalid estimator, and is reported both ways.** The stake said
   `|mean − pred| < 3·sd/√N` on a single run. The samples of a repair-and-decay trajectory are
   autocorrelated with time `≈ 1/(1−(1−q)λ)`, so `sd/√N` understates the standard error and that
   bar was never a 3σ bar. Judged by its letter, E4 fires at **2.16×**. Judged with a standard
   error that is actually one — 40 independent replicates, SE across replicate means — the worst
   deviation is **0.42×** the 3 SE bar. **This is a permissive amendment and is flagged as such:
   both numbers are in the output and in this file.** The underlying prediction (§4.4: stochastic
   dosing has the same *mean* retention as continuous) is exact algebra, not a fit; the amendment
   concerns only how the Monte-Carlo error was estimated.
2. **The spectral gap is read off the chain, not off the construction.** The first run set the gap
   by `a = γ/(1 − max_j|m_j|)`, which is the wrong eigenvalue when the extreme eigenvalue is
   negative; `γ` then missed its target by ~5e−3 and E2 read a 1.3e−3 discrepancy that was an
   artifact of the *construction*, not of `f`. Fixed by using the second largest **algebraic**
   eigenvalue, asserting the chain is lazy (all eigenvalues positive), and — the part that
   matters — **measuring `γ = 1 − λ₂` off `T` and using the measured value in `f`**, which is what
   the derivation says to do in the first place (`ε` is a spectral quantity of `T_c`, read off the
   object). E2 then passes at 9.1e−10 against a 1e−9 bisection tolerance.

No stake was added, removed, or relaxed after seeing a number, other than as recorded in (1).

## 8. Provenance of every constant used downstream

| constant | value | source | fitted? |
|---|---|---|---|
| atlas `λ = (1−2ε_flip)²` | at `ε_flip` = 0.02/0.05/0.1/0.2 | derived in §2 from the model's own noise | **no** |
| atlas `δ` | 0.02 | the atlas's own target `P(in code) ≥ 0.99`, converted through A2 (`G = 2π₀ − 1`) | **no** |
| LFSR `λ = (1−2ε_flip)^3` | `d = 3` | `MAINTENANCE_SWEEP_RESULTS.md` P1/P2, lowest nonzero Fourier weight | **no** |
| holonomy `λ = 0.959913`, `ε = 0.040087` | measured | `HOLONOMY_RENT_RESULTS.md` §2, the `q=0` arm | measured, not fitted |
| `cos θ(q)` | — | **not used** — FIT-FLAG in §5 | n/a |
