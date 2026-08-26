# Finite-model atlas v2 — stakes, written before `atlas_v2.py` exists

*2026-08-26. Target: `OBJECT_INVARIANT_HUNT.md`'s remainder item 5, "∇_c CURVATURE —
the last untested bridge: holonomy of ∇_c vs closure defect of state-dependent fibers",
and its hunt H2 (closure ↔ curvature). Method inherited verbatim from
`ATLAS_V1_STAKES.md`: the atlas is pure mathematics, so the researcher degree of freedom
is not about nature — it is about **which relations get called discoveries**. Anything I
can derive by hand before the run is written down here as DERIVED and its confirmation
counts as verification of the instrument, never as a finding. Only the items marked OPEN
can produce a finding.*

---

## 1. THE MODEL CLASS, fixed before enumeration

### 1.1 Base, fiber, mode

- **Base**: three contexts in a cycle, `c1 → c2 → c3 → c1`. Edges `e12, e23, e31`.
- **Mode**: `M = {0,1}` — the slowly-changing parameter on which a state-dependent
  fibration depends. "Slow" is a property of the *dynamics*, not of the fibration
  (§1.4): the adiabatic limit is `τ = id`.
- **Microstate**: `S`, `|S| = n ∈ {2,3,4}`.
- **World / root**: `X = M × S`, `|X| = 2n`. Every context has its OWN root; as sets
  they are all `X`, but they are related only by the re-root maps of §1.3. **There is no
  common source** — that is the whole point, and it is the only thing that lets
  curvature exist at all (`loop_asymmetry`).

### 1.2 The fibration (the view over each context)

Context `i` carries a view `q_i : X → F_i` with `|F_i| = k`:

```
q_i(m, s) = π_i^m(s)
```

so the fiber partition over context `i` **depends on the mode `m`**. Two variants,
both enumerated:

- **FIXED fibration** (presheaf limit): `π_i^0 = π_i^1` for all `i` — the view is
  mode-blind.
- **STATE-DEPENDENT fibration** (the stack): `π_i^0 ≠ π_i^1` for some `i`.

The mismatch is named once: **`β_i := π_i^1 ∘ (π_i^0)^{-1}`** (defined when the `π`
are bijections). `β_i = id` ⇔ context `i`'s fibration is mode-blind.

### 1.3 Transport (∇)

A re-root `r_ij : X → X` per edge, `r_ij(m,s) = (σ_ij(m), ρ_ij(s))` — a **mode action**
`σ_ij : M → M` and a **microstate action** `ρ_ij : S → S`. Two sectors, kept separate
because they are not the same physics:

- **mode-only sector** (`ρ_ij = id`): the re-root moves only the slow parameter. This is
  the stack-specific sector — the one the presheaf→stack upgrade is supposed to open.
- **base sector** (`σ_ij = id`): ordinary transport freedom, available already in the
  fixed-cover object (`transport_loop_can_be_nontrivial`).

The **carry** `γ_ij : F_i → F_j` is NOT free data: `ClaimTransport` requires
`q_j ∘ r_ij = γ_ij ∘ q_i`, which determines `γ_ij` on `range(q_i)` and may have **no
solution at all**. Non-existence is a first-class reading, not a discard.

**Holonomy** `γ_loop := γ_31 ∘ γ_23 ∘ γ_12`, a self-map of `range(q_1)`.
**Curvature** `F_γ ≠ 0` ⇔ `γ_loop ≠ id` on `range(q_1)`; its **class** is the cycle type
of `γ_loop` when `γ_loop` is a permutation, and its **support** is
`#{f ∈ range(q_1) : γ_loop(f) ≠ f}`.

### 1.4 Dynamics

`T : X → X`. Structured variant `T(m,s) = (τ(m), t_m(s))`; general variant, all
functions `X → X`. **Slowness of the mode** is `τ`: `τ = id` is the adiabatic limit; a
stochastic variant flips the mode with probability `p` per step.

Everything is pulled back to root 1, where the whole atlas becomes a chain of views on
ONE space:

```
q_1 ,  q̃_2 := q_2∘r_12 ,  q̃_3 := q_3∘r_23∘r_12 ,  q̃_1' := q_1∘r_loop
```

with `r_loop := r_31∘r_23∘r_12`.

### 1.5 The defect functional (one functional, two axes)

Uniform measure on `X`. For maps `u, w` out of `X`:

```
D(u | w) := H(u | w)      (nats; zero ⇔ u factors through w)
```

- **closure defect (time axis)**: `Δ_v = D(v∘T | v)` — zero ⇔ `Closed v T`.
- **transport defect (context axis)**: `δ_ij = D(q_j∘r_ij | q_i)` — zero ⇔ the carry
  `γ_ij` exists.
- **glued view**: `G(x) := (q_1 x, q̃_2 x, q̃_3 x)`; its closure defect `Δ_G = D(G∘T | G)`.

---

## 2. DERIVED IN THIS PREREG — the instrument must reproduce these exactly

*These are hand-derived here, before `atlas_v2.py` exists. If the enumeration
contradicts any of them the CODE IS WRONG and every other number it prints is void,
exactly as in v1. Confirming them is verification, not discovery.*

**D1 (the flat-limit gate — `mediator_fixes_range`).** If `r_loop = id_X` and all three
carries exist, then `γ_loop = id` on `range(q_1)`. *Reason:* the square gives
`γ_loop ∘ q_1 = q_1 ∘ r_loop = q_1`, and `mediator_fixes_range` pins it.
**This is the gate the brief demands. It must come out 100.0%.**

**D2 (the mode-blind gate — the sharpened form of "fixed fibration ⇒ flat").** If every
view is mode-blind AND the re-roots act only on the mode (`ρ_ij = id`), then
`γ_loop = id` on `range(q_1)`. *Reason:* every `q_i` is then a function of `s` alone,
`q_j∘r_ij = q_j`, so the three carries are genuine mediators of views out of a **common**
source, and `factors_cycle_trivial` applies verbatim.

**D2′ (the correction D2 forces, and it matters).** "Fixed fibration ⇒ flat" is FALSE as
usually stated: with `ρ_loop ≠ id` a mode-blind atlas has holonomy
`γ_loop = π_1^0 ρ_loop (π_1^0)^{-1} ≠ id`. State-dependence is NOT what unlocks
curvature in general — a *common source* is what forbids it. State-dependence unlocks
exactly the **mode sector**.

**D3 (holonomy = rent on the context axis).** Whenever `γ_loop` exists,
`γ_loop = id on range(q_1)` ⇔ `q_1 ∘ r_loop = q_1` ⇔ **`Held q_1 r_loop`**. So zero
curvature is `Held` and existence-of-`γ_loop` is `Closed q_1 r_loop`, and
`held_imp_closed` (already machine-checked) gives **zero curvature ⇒ the loop
transports**, for free.

**D4 (the mode-sector holonomy formula).** With `ρ_ij = id` and swap-flags
`ε_ij ∈ {0,1}` (1 = the edge flips the mode), and `π_i^0 =: a_i`, `α_i := (π_i^1)^{-1}a_i`:

```
γ_loop = a_1 · ( α_1^{-ε_31} α_3^{-ε_23} α_2^{-ε_12} ) · a_1^{-1}
```

— the curvature of the mode sector is **the ordered product of the fibration's
mode-mismatches, one factor per mode-flipping edge**, conjugated into context 1's
labels. Corollary: no mode-flipping edge, or all `α_i = id`, ⇒ flat (this contains D2).

**D5 (carry existence is a conjugacy condition).** In the bijective family the carry
`γ_ij` exists ⇔ `ρ_ij α_i ρ_ij^{-1} = α_j^{±1}` (sign `+` if the edge preserves the mode,
`−` if it flips it). A claim transports across an edge **iff the two contexts' fibration
mismatches are conjugate** through the re-root's microstate action.

**D6 (curvature is a permutation iff transport is reversible).** If every `r_ij` is a
bijection then `γ_loop` is a permutation of `range(q_1)`. *Reason:*
`γ_loop(range q_1) = range(q_1∘r_loop) = range(q_1)`, and a surjection of a finite set is
a bijection.

**D7 (the closure of the mode-flip view).** For the pure mode-advance dynamics
`T(m,s) = (¬m, s)`, `Closed q_i T` ⇔ `β_i² = id`.

---

## 3. STAKED, OPEN — what the enumeration decides

### B(i) — **zero holonomy ⇒ a closure/gluing property.** *Staked: FALSE.*

Precise form tested: `γ_loop = id on range(q_1)` ⇒ `Closed G T` (and the weaker
`⇒ Closed q_1 T`). **Predicted refutation mechanism** (from D4 + D7): curvature is a
*product* of the mismatches `β_i` while closure is *involutivity of each factor*; a
3-cycle `β` cubed is the identity, so a maximally mode-dependent atlas can be exactly
flat while no view is closed. **Predicted minimal counterexample: `k = 3`** (a 3-cycle
is needed; `k = 2` cannot supply one). Kill for the stake: no counterexample exists in
the exhaustive class — then the implication is real and is the finding.

### B(ii) — **nonzero holonomy ⇒ quantified closure failure of the glued view.**
*Staked: FALSE.*

Precise forms tested: (a) `γ_loop ≠ id` ⇒ `¬Closed G T`; (b) the quantified envelope
`Δ_G ≥ f(support(F_γ))` for ANY nondecreasing `f` with `f(1) > 0` — refuted by a single
model with `support ≥ 1` and `Δ_G = 0`. **Predicted minimal counterexample: `k = 2`**
(`β = swap` is its own inverse, so the view is closed while one flipping edge makes the
loop non-flat). Kill for the stake: no such model — then curvature really does force
glued-view failure.

### B(iii) — **the flat-limit gate.** Not open; it is D1/D2, and it is the atlas's own
kill: contradiction ⇒ the code is wrong, not the theorem.

### B(iv) — **THE SURVIVING BRIDGE, staked as TRUE: curvature is an automorphism of the
habit.**

> If the loop is a symmetry of the dynamics (`T ∘ r_loop = r_loop ∘ T`) and `q_1` is
> closed under `T` with rate `h` (`q_1∘T = h∘q_1`), then
> **`γ_loop ∘ h = h ∘ γ_loop` on `range(q_1)`.**

*Derivation staked with it:* `γ_loop(h(q_1 x)) = γ_loop(q_1(Tx)) = q_1(r_loop T x) =
q_1(T r_loop x) = h(q_1(r_loop x)) = h(γ_loop(q_1 x))`. Kill: a model satisfying both
hypotheses with `γ_loop∘h ≠ h∘γ_loop` on the range. Also staked: **both hypotheses are
load-bearing** — dropping equivariance must produce counterexamples (measured as a
commutator support `K > 0`), and so must dropping closure. If either hypothesis turns
out to be droppable the bridge is stronger than staked and that is a finding.

### B(v) — **lossy holonomy.** *OPEN, no prediction.* Does an irreversible re-root give a
`γ_loop` that is **not injective** on `range(q_1)` — a loop that returns fewer
distinctions than it took? D6 says reversibility forbids it. If a witness exists,
curvature has a dissipative sector the programme has never named; report the minimal
witness. If none exists in the general-function class, that is a theorem target instead.

### B(vi) — **loop transports where a leg does not.** *OPEN, no prediction.* Can
`Closed q_1 r_loop` hold while some `Closed q̃_j q̃_{j-1}` fails — the composite carrying
a claim the legs cannot? This is `comp_failure_convicts_second_leg` read backwards, and
a positive answer fences any inference from loop-level success to leg-level validity.

### B(vii) — **the adiabatic scaling.** *OPEN.* Under a mode that flips with probability
`p`, does the mode-sector closure defect of a state-dependent view enter at `O(p)` —
i.e. is the state-dependence invisible in the adiabatic limit and linear in the mode
rate? Report the fitted exponent; it is a measurement, not a stake.

---

## 4. Kill for the atlas itself

Inherited from v1 and strengthened: **if the enumeration contradicts D1 or D2, the atlas
code is wrong and every number in `ATLAS_V2_RESULTS.md` is void until repaired.** In
addition, the gauge reduction used to keep the sweeps exhaustive (relabelling each
context's readings so `π_i^0 = id`) must be checked numerically to leave the holonomy
class invariant; if it does not, the reduction is void and the sweeps must be rerun
unreduced.

## 5. What counts as the deliverable

Exactly as v1: **the smallest counterexample to every false bridge, and the strongest
surviving relation** — the latter stated precisely enough, with finite witness data,
to become a `decide`-able Lean target.
