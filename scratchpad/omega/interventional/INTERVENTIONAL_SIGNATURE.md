# THE INTERVENTIONAL SIGNATURE — theory note

*2026-08-26. Remainder item 2 of `OBJECT_INVARIANT_HUNT.md`'s Ω(c) section. This note is
mathematics only: definitions, four theorems, one impossibility proposition, and one
counterexample. It stakes nothing about nature. The stakes live in
`INTERVENTIONAL_STAKES.md`, written before the instrument; readings live in
`INTERVENTIONAL_RESULTS.md`.*

**What it is for.** COMPOSITION-2 recorded a falsification whose mechanism was one
sentence: *the engine is deterministic, and the closure detector's null semantics assume
stochasticity.* Three observational arms missed (B1 independent sessions read coupled, B2
coupled halves at floor, B3 no contraction at any lag); the one interventional arm passed
(B4, K = 1.0012). The hunt doc's reading of B4 — **"evolution respects its fibers" is a
do-statement, not a see-statement** — is what this note makes precise. The target is a
splitting signature that is EXACT on deterministic substrates, immune to common drivers,
and directional.

---

## 0. Setting and notation

* `X` — a set of microstates. Finite wherever a proof says "finite"; otherwise arbitrary.
* `T : X → X` — deterministic dynamics. (§4 replaces it by a Markov kernel.)
* `v_A : X → A`, `v_B : X → B` — two coarse views (surjective, w.l.o.g.).
* `fib_B(x) = { y ∈ X : v_B y = v_B x }` — the fiber of `v_B` through `x`. This is Ω(c)'s
  first component, `Fib_π(c)`.
* `Closed v T` — the repo's predicate: `∃ φ, v ∘ T = φ ∘ v` (`Core/Habit.lean`). By
  `closed_iff_fiber_invariant`, equivalently `∀ x y, v x = v y → v (T x) = v (T y)`: **the
  step never splits a fiber of the view.**

**Probes.** A *probe on sector A* is a map `δ : X → X` that is **B-blind**:

> **(P)  `v_B ∘ δ = v_B`.**

That is the whole locality requirement: the probe writes only where `v_B` cannot see it.
(On a product space `X = A × B` with `v_A = fst`, `v_B = snd`, the maps
`δ_{a'} : (a,b) ↦ (a',b)` are exactly the B-blind ones that preserve the B coordinate.)
Write `𝒫_A` for the chosen probe set and `⟨𝒫_A⟩` for the monoid it generates. Every
element of `⟨𝒫_A⟩` is B-blind, since (P) is closed under composition.

**Probe-response.** Fix a discrepancy `d_B` on `B` with `d_B(b,b') = 0 ⟺ b = b'`. For
`δ ∈ 𝒫_A`, `x ∈ X`, lag `t ≥ 0`:

> **`R_{A→B}(δ, x, t) = d_B( v_B(T^t (δ x)), v_B(T^t x) )`.**

Two runs of the *same* law from two microstates that `v_B` cannot tell apart. The
unprobed run is the control, and on deterministic dynamics it is an **exact** control —
there is no null distribution anywhere in this definition.

> **NULL A→B probe-response** ⟺ `R_{A→B}(δ, x, t) = 0` for all `δ ∈ 𝒫_A`, `x ∈ X`, `t ≥ 0`.

---

## 1. The general deterministic theorem — the signature IS closure

**Definition (fiber-transitive probe set).** `𝒫_A` is *fiber-transitive for `v_B`* if for
every `x, y ∈ X` with `v_B x = v_B y` there is `δ ∈ ⟨𝒫_A⟩` with `δ x = y`. (The probes can
reach every microstate `v_B` cannot distinguish from the one you are at.)

> **Theorem 1 (interventional characterization of closure).**
> Let `v_B : X → B`, `T : X → X`, and `𝒫_A` a set of B-blind probes.
>
> **(⇐, no hypothesis on `𝒫_A`)** If `Closed v_B T` then the A→B probe-response is null at
> every lag.
>
> **(⇒, needs fiber-transitivity)** If `𝒫_A` is fiber-transitive for `v_B` and the A→B
> probe-response is null **at lag 1**, then `Closed v_B T`.
>
> Consequently, for fiber-transitive `𝒫_A`:
> **null at lag 1 ⟺ null at all lags ⟺ `Closed v_B T` ⟺ `T` never splits a fiber of `v_B`.**

*Proof.* (⇐) `Closed v_B T` gives `φ` with `v_B ∘ T = φ ∘ v_B`, hence by induction
`v_B ∘ T^t = φ^t ∘ v_B`. For B-blind `δ`,
`v_B(T^t δ x) = φ^t(v_B(δ x)) = φ^t(v_B x) = v_B(T^t x)`. So `R = 0` at every `t`. ∎

(⇒) Take `x, y` with `v_B x = v_B y`. By fiber-transitivity pick `δ ∈ ⟨𝒫_A⟩` with
`δ x = y`. Lag-1 nullity (which extends from `𝒫_A` to `⟨𝒫_A⟩`, because at each factor the
two runs enter the next probe at states with the same `v_B`, and the argument composes)
gives `v_B(T y) = v_B(T δ x) = v_B(T x)`. So `v_B ∘ T` is constant on `v_B`-fibers, which
is `closed_iff_fiber_invariant`'s right-hand side; hence `Closed v_B T`. ∎

**Reading.** The interventional signature is not a new invariant. It is the *operational
definition* of the invariant the lake already has: closure. Where the observational
detector asks whether B's record carries information about A, the probe **exhibits the
witness** — a second point in the same fiber — and asks whether `T` keeps them together.
That is exactly the hunt doc's diagnosis ("the object's core relations are existence
statements, and every kill happened where two situations agree on the PREDICATE and differ
in the WITNESS") turned into an instrument: *a probe is a manufactured witness.*

---

## 2. The product case — direction, and the recovery of `both_closed_iff_product`

Let `X = A × B`, `v_A = fst`, `v_B = snd`, `T(a,b) = (T_A(a,b), T_B(a,b))`, and
`𝒫_A = { δ_{a'} : (a,b) ↦ (a',b) : a' ∈ A }`. Each `δ_{a'}` is B-blind, and `𝒫_A` is
fiber-transitive for `v_B` (the fiber over `b` is `A × {b}`, and `δ_{a'}` reaches every
point of it). Say **there is no A→B coupling** iff `T_B(a,b) = T_B(a',b)` for all `a,a',b`
— i.e. `T_B` factors through `B`.

> **Theorem 2 (directed product form).** In the above setting:
> **null A→B probe-response ⟺ no A→B coupling**, and symmetrically for B→A.
> Hence **null in both directions ⟺ `T` is a product map ⟺ both coordinate views Closed**,
> which is `both_closed_iff_product` (`Core/MatterCoupling.lean`, confirmed 256/256 by the
> atlas).

*Proof.* Specialize Theorem 1: `Closed snd T` ⟺ `snd ∘ T` factors through `snd` ⟺ `T_B`
factors through `B` ⟺ no A→B coupling. The two-sided statement is
`product_of_both_closed` / `independent_views_closed`. ∎

**What this buys over the observational theorem.** `both_closed_iff_product` is a
*symmetric* detector: it says coupling is present, not which way it runs. The
probe-response version splits that iff into its two directed halves, each separately
testable, with an exact zero as the null on each side. Direction comes for free because
the probe has a location.

---

## 3. Common drivers, and why the twin construction is immune

This is the clause the observational route could not satisfy. The atlas measured the gap
(S2: both closure defects zero under a common driver while 0.693 nats of correlation were
created); COMPOSITION-2's B1 then showed the *estimated* observational defect fires anyway
on a deterministic substrate, where a shared law is a universal common driver.

> **Theorem 3 (common driver reads null both ways).** Let `X = A × B × C` and
> `T(a,b,c) = ( f(a,c), g(b,c), h(c) )` — A and B each driven by C, neither reading the
> other. Take `v_A = fst`, `v_B = snd`, and the coordinate probe sets
> `𝒫_A = {(a,b,c) ↦ (a',b,c)}`, `𝒫_B = {(a,b,c) ↦ (a,b',c)}`.
> Then the A→B and B→A probe-responses are **null at every lag**, for every state and
> every probe — while `v_A` and `v_B` may be arbitrarily strongly correlated under any
> initial distribution that randomizes `c`, and neither view need be `Closed`.

*Proof.* Write `x = (a,b,c)`, `x' = (a',b,c)`. Claim: `(T^t x)_{2,3} = (T^t x')_{2,3}` for
all `t`, by induction. At `t = 0` the B and C coordinates agree by construction. If they
agree at `t`, then `(T^{t+1}x)_2 = g((T^t x)_2, (T^t x)_3) = g((T^t x')_2, (T^t x')_3) =
(T^{t+1}x')_2`, and likewise for C via `h`. Hence `v_B(T^t x') = v_B(T^t x)` at every `t`.
The B→A statement is the mirror image. Correlation: `A_t` and `B_t` are both functions of
`(a_0, b_0, c_0)` through the shared `c`-orbit, and choosing `f = g` and `a_0 = b_0` makes
them equal, so `I(A_t ; B_t)` is as large as the marginal entropy allows. Non-closure:
`v_B` need not be Closed, since `g(b, ·)` may depend on `c`, which `v_B` cannot see. ∎

**The mechanism, in one sentence.** *The twin run holds the common driver fixed by
construction; observation cannot.* The probe-response is a functional of `T`'s dependence
structure alone — the shared driver's state, and the shared law, are literally the same
object in both members of the twin, so they cancel identically rather than statistically.
This is why the signature carries no null distribution, no floor, and no
Bonferroni: on a deterministic substrate the null value of a null arm is the integer 0.

Note the asymmetry with Theorem 1: Theorem 3 gives *null response with non-closure*. There
is no contradiction — `𝒫_A` in Theorem 3 is **not** fiber-transitive for `v_B` (its orbits
cannot move `c`, but `c` is invisible to `v_B`, so the `v_B`-fiber is strictly bigger than
any probe orbit). Fiber-transitivity is exactly the hypothesis that separates "no A→B
arrow" from "no hidden sector at all", and the directed reading of §2 is the one that
survives without it. **A probe set that cannot move the hidden sector measures the arrow,
not the closure.** That is a feature, and it is the precise sense in which the
interventional signature is *directed influence* rather than *autonomy*.

---

## 4. The stochastic version, and its subtleties stated honestly

Replace `T` by a Markov kernel `P` on `X`. Two inequivalent generalizations exist and they
must not be blurred.

**(D) Distributional response** — the causal-effect definition:
`R^dist_{A→B}(δ, x, t) = D( Law(v_B(X_t) | X_0 = δx) ‖ Law(v_B(X_t) | X_0 = x) )`
for any divergence `D` that vanishes only on equality (total variation, say).

**(C) Coupled-noise pathwise response** — the twin definition, and the one an engine or a
simulator can actually run. Realize `P` as `X_{t+1} = F(X_t, ξ_t)` with `ξ_t` an i.i.d.
noise stream; run probed and unprobed twins on the **same** realization `ξ_·`;
`R^path_{A→B}(δ, x, t) = E[ d_B( v_B(X'_t), v_B(X_t) ) ]`.

> **Theorem 4 (distributional version).** Let `X = A × B`, and let
> `Q(b' | a, b) = Σ_{a'} P((a',b') | (a,b))` be the B-marginal kernel. Then
> **`R^dist_{A→B} ≡ 0` at lag 1 (all states, all coordinate probes) ⟺ `Q(· | a,b)` does not
> depend on `a`** — and either side implies `R^dist_{A→B} ≡ 0` at every lag, because in
> that case the B-marginal is an autonomous Markov chain with kernel `Q`, so
> `Law(B_{t} | A_0 = a, B_0 = b) = Q^t(· | b)` for every `a`.

*Proof.* (⇒) lag-1 nullity at `(a,b)` against `δ_{a'}` says `Q(·|a',b) = Q(·|a,b)`;
quantify. (⇐) induction on `t`: `Law(B_{t+1}|A_0=a,B_0=b) = Σ_{b'} Law(B_t = b'|…) Q(·|b')`
and the inner term is `a`-free by hypothesis and the inductive hypothesis. ∎

Note what Theorem 4 does **not** require: no conditional independence of `A'` and `B'`
given the source. The B-marginal is the whole story for a B-view response.

### 4.1 Subtlety 1 — pathwise nullity is strictly stronger than causal nullity

`R^path ≡ 0 ⟹ R^dist ≡ 0` always (a.s.-equal paths have equal laws). **The converse is
false**, and the counterexample is small enough to be a unit test:

> `X = {0,1} × {0,1}`, `ξ_t = (ξ¹_t, ξ²_t)` i.i.d. fair bits,
> `F((a,b), ξ) = ( ξ¹ , ξ² ⊕ a )`.
> The B-marginal kernel is `Q(·|a,b) = Uniform{0,1}` for every `a, b`: **no causal effect
> on B at any lag**, `R^dist ≡ 0`. But the coupled twins at `a` and `a' = 1−a` give
> `B'_1 = ξ² ⊕ a' ≠ ξ² ⊕ a = B_1` with probability 1: **`R^path = 1`, maximal.**

The pathwise detector is reading *how the simulator consumed its randomness*, not what the
kernel does. Three consequences, all of them design requirements rather than caveats:

1. **A pathwise response is not by itself a coupling reading.** It must be adjudicated
   against a distributional arm (ensembles over independent noise streams). Claim coupling
   only when **both** fire. Pathwise-null, by contrast, *is* conclusive for causal nullity.
2. **The noise stream must be A-blind**: `ξ` indexed by `(time, sector, site)` and consumed
   in that order regardless of state. Any state-dependent RNG consumption order — the
   ordinary situation in a real engine, where refinement, spatial hashing or a
   variable-length loop reorders draws — manufactures exactly the counterexample above.
3. **A placebo probe on a sector known to be uncoupled** gauges the realization-dependent
   pedestal directly. This is the stochastic analogue of the exact-zero floor.

On deterministic dynamics the noise stream is empty, (C) and (D) coincide, and Theorems
1–3 are exact. **The interventional signature is sharpest exactly where the observational
one failed.**

### 4.2 Subtlety 2 — magnitude confounds direction; latency does not

In a chaotic deterministic system the response grows like `e^{λt}`, so the *size* of a
response mixes coupling strength with local amplification, and comparing `R_{A→B}` to
`R_{B→A}` by magnitude compares Lyapunov exponents as much as arrows. Two remedies, both
cheap:

* **Onset latency.** The first lag at which `R` leaves exact zero is the causal light-cone
  — the propagation time from the probe site to the read site. It is amplification-free
  and it is a *forward-predictable integer* on a lattice with a known interaction radius.
  This is Ω(c)'s `∇_c` entering the stake, which is precisely what COMPOSITION-2's B2
  omitted ("the stake ignored ∇_c's light-cone").
* **Within-sector normalization.** Divide by the A→A response to an identical probe, which
  carries the same local amplification and no cross-sector arrow.

### 4.3 Subtlety 3 — the exact-zero floor must be *measured*

On a deterministic substrate the null response is exactly `0`, and in floating point the
twins stay bitwise identical **provided the probe does not change the code path**. Mesh
refinement, node insertion/renumbering, spatial-hash iteration order and parallel reduction
order all break that. So the floor is a claim about the *scene*, not about the instrument,
and it has to be established the same way any control zero does: run the twins with the
**sham probe `δ = id`** and confirm bitwise-zero divergence across the whole window, and
record the divergence for a **pre-probe window** where it must also be exactly zero. An
instrument that starts recording at the probe frame cannot see its own pedestal.

---

## 5. The impossibility that explains B1 and B3

Why did the observational arms fail on a deterministic engine? Not because the estimator
was weak. Because the question is **not identifiable from one orbit**.

> **Proposition 5 (single-orbit non-identifiability of closure).** Let `X` be finite,
> `v_B : X → B` surjective with `|B| ≥ 2`, `x_0 ∈ X`, and let `O = {T^t x_0 : t ≥ 0}` be
> its forward orbit. Suppose `O` meets each `v_B`-fiber **at most once**, and some fiber
> contains a point outside `O` together with at least one other point. Then there exist
> `T', T'' : X → X` with `T'|_O = T''|_O = T|_O` — so the two systems produce the *identical
> observed trajectory*, and identical `v_A`, `v_B` records at every lag — with
> `Closed v_B T'` true and `Closed v_B T''` false.
> **Hence no statistic of the observed trajectory alone can decide closure.**

*Proof.* Define `h : B → B` by `h(v_B(z)) = v_B(T z)` for the unique `z ∈ O` in that fiber,
and arbitrarily elsewhere; `h` is well defined precisely because `O` meets each fiber at
most once. Put `T' x = T x` on `O`, and for `x ∉ O` let `T' x` be any point with
`v_B(T'x) = h(v_B x)` (exists by surjectivity). Then `v_B ∘ T' = h ∘ v_B`, so
`Closed v_B T'`. For `T''`, start from `T'`, take a fiber `F` with `|F| ≥ 2` and a point
`z ∈ F \ O`, and redefine `T'' z` to be any point whose `v_B`-value differs from
`h(v_B z)`; then `v_B ∘ T''` is not constant on `F`, so `¬ Closed v_B T''` by
`closed_iff_fiber_invariant`. Both agree with `T` on `O`. ∎

**In words: a single deterministic trajectory almost never visits two points of the same
fiber, and fiber-splitting is a statement about pairs in a fiber.** The observational
detector was being asked to answer a question its data does not contain; the probe is what
supplies the missing second point. B1 (independent sessions read coupled) and B3 (no
contraction at any lag) are corollaries of this proposition rather than embarrassments —
the same demotion the hunt doc gave them, here with a proof.

Stochasticity is what ordinarily rescues the observational route: noise makes the orbit
re-enter fibers, and `μ_c` supplies the null. That is the same boundary COMPOSITION-2
found from the other side — "the fiber/closure machinery is a theory of stochastic coarse
dynamics" — and Proposition 5 says *why* the boundary is there.

---

## 6. Lean targets (not attempted here — this brick is forbidden to touch the Lean)

The four statements are Lean-ready against `Core/Habit.lean` and `Core/MatterCoupling.lean`
with no new imports:

| target | statement |
|---|---|
| `probe_response_null_of_closed` | `Closed v T → ∀ δ, v ∘ δ = v → ∀ t x, v (T^[t] (δ x)) = v (T^[t] x)` |
| `closed_of_probe_response_null` | fiber-transitivity of `𝒫` + lag-1 nullity → `Closed v T` |
| `interventional_iff_closed` | the iff, i.e. Theorem 1 |
| `directed_product_of_probe_null` | Theorem 2's directed half, refining `both_closed_iff_product` into two arrows |
| `common_driver_probe_null` | Theorem 3 on `A × B × C` |

The first three are a few lines each given `closed_iff_fiber_invariant`; Theorem 3 is an
induction on the pair of coordinates. Whoever picks this up should note that Theorem 1's
(⇒) is the only one needing a hypothesis on the probe set, and that hypothesis is where the
common-driver case leaves the theorem alone.

---

## 7. Scope fence

Everything above is a statement about maps and kernels on a state space. Nothing here is a
claim about nature, about the engine, about hardware, or about Ω(c) being the maximal
object. What it establishes is narrower and is the whole point: **the splitting clause of
Ω(c) has an operational form that is exact on deterministic substrates, immune to common
drivers by construction, directional, and equal to the closure predicate the lake already
machine-checked** — plus a proof that its observational form was never identifiable from
the data COMPOSITION-2 gave it.
