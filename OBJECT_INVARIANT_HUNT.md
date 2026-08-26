# The invariant hunt — one defect, four faces, and what survived its first day

*2026-08-26. The search program for the maximal object's unique observable, absorbing
an external proposal (Codex, via Eric) and the first atlas run. This document is the
umbrella; stakes and readings live in `scratchpad/atlas/`.*

## The method, governing everything below

*Stated 2026-08-26 (Eric), recorded because message-only content is not record.*
The goal is to find the REAL maximal object and prove its existence — or disprove
it — via increasingly accurate models pressed against reality (simulators and
datasets) through the MISFIT PROTOCOL: every mismatch is forced to declare itself
either a conviction of the model (repair → more accurate) or a discovery (reality
informing the object → more true). Proof: one frozen model predicting across
different substrates with fewer freedoms than separate effective theories.
Disproof: a misfit that convicts every repair. The fiber ladder is the current
model; everything in this file is one turn of that loop.

## The proposal being hunted

Write the object as a state-dependent stack `π : E → C` with evolution `T`, transport
`∇`, and closed fibers recursing. Hunt ONE defect class Ω whose projections are:

| face | form |
|---|---|
| dynamical non-closure | `D_v = v∘T − T_v∘v` |
| transport curvature | `F_γ = ∇_γ − id` |
| contextuality | `[Ω̌] ≠ 0` (gluing obstruction) |
| maintenance cost | `W*_v = inf { Cost(U) : D_v(T+U) = 0 }` |

The bridge theorem to hunt: these are functorial images of one Ω. If no such Ω exists,
the object is a common notation, not a structure — `OBJECT_PRIOR_ART.md`'s standing
verdict, unchanged.

## Boundary conditions Ω must satisfy (proved before the hunt began)

1. **The flat limit.** In the fixed-cover object the view axis is provably flat
   (`factors_cycle_trivial`, axiom-free) while transport is free
   (`transport_loop_can_be_nontrivial`). Ω must vanish on view loops and reduce to
   ordinary holonomy on transport loops. `loop_asymmetry` is its boundary condition.
2. **The deterministic interaction face is EXACT.** `both_closed_iff_product`
   (`Core/MatterCoupling.lean`): on a product space, both coordinate views Closed iff
   the step is a product map. The closure face of Ω is an exact directed-coupling
   detector in this class — confirmed 256/256 by enumeration.

## What the first day killed, through the misfit protocol — each kill a discovery

- **"Mutual closure = no interaction" (stochastic): DEAD.** The gap is exactly
  common-driver correlation (measured: 0 defect both ways, up to 0.693 nats of created
  correlation). *Discovery:* `Closed` reads **directed influence**, not correlation.
  Consequence inherited by every intervention design: a common-driver control arm is
  mandatory.
- **"Share = contextual fraction": DEAD AS STATED.** Every classical state is its own
  global section; the three-coin parity state has share ln 2 and zero contextuality.
  *Discovery:* the faces of Ω are **differently typed** — share is (state, chart),
  contextuality is (cover). Ω cannot be one number; it must be a functor, and the
  surviving claim is that qShare bounds the contextual fraction of the *induced*
  empirical model. Untested.
- **"Maintenance cost priced by closure defect": DEAD.** The 2-bit parity code view is
  *exactly closed* under iid flip noise (Δ_v ≡ 0) while W* runs 0.79–0.97 — no f(Δ_v)
  prices W*. *Discovery:* **closure is autonomy, not stability.** An autonomous view
  decays under its own induced chain, and maintenance is priced on that chain's decay
  rate — which is the rent clause, already measured on three substrates. The
  autonomy–memory–work theorem *reduces to the rent law* for closed views.

## THE DIAGNOSIS the three kills share — Ω is the fiber, and the object was stated in predicates

*Added 2026-08-26, same day, after the atlas run. This is the answer to "what do the
three kills point at."*

**Each bridge failed the same way: it compared PREDICATES where the physics lives in
the WITNESSES.** The object's core relations are existence statements — `∃ h` in
`Factors`, `∃ φ` in `Closed`, "a global section exists" in contextuality — and every
kill happened where two situations agree on the predicate and differ in the witness:

1. Common-driver: each marginal's closure predicate holds; the JOINT witness — the
   coupling of the noise across fibers — carries the correlation. Invisible per-view.
2. Share vs contextuality: contextuality asks whether the gluing map's fiber is
   EMPTY; share measures entropy geometry WITHIN a nonempty fiber. Same map, two
   invariants at different levels — not one number.
3. Rent: `Closed` asserts `∃ φ`; the price of maintenance is a property OF φ — its
   decay rate. Existence is orthogonal to contraction.

**The repair, and the repo has been converging on it all season: take the FIBER as
the primitive.** Every face of Ω is already a fiber invariant somewhere in the tree:

| face | fiber reading | witness in the tree |
|---|---|---|
| factoring | fibers of `v` refine fibers of `u` | `factors_iff_not_separatesFiber` (the completeness bridge) |
| the founding shape | a quantity SPLITS a fiber | `SeparatesFiber`, the NonFactoring anatomy |
| **closure** | **the step never splits a fiber of the view** | **`closed_iff_fiber_invariant` — proved today, `Core/Habit.lean`** |
| entropy | log-size of the chart's fiber | `frameEntropy`, "entropy comes FREE from the base frame" |
| production | log-size of the STEP's own fiber | `production_id_eq_log_degree` |
| extensivity / its failure | fibers multiply ⟺ independence; **the common-driver gap is exactly the failure of fiber multiplicativity** (= mutual information) | `frameEntropy_add` + atlas Part 2 |
| rent | contraction rate of the induced dynamics ON the fiber partition | the rent clause, three substrates |
| contextuality | EMPTINESS of the gluing map's fiber | the stack face — untested, H2/H3 |
| holonomy | a loop-induced automorphism OF a fiber | transport face, `RerootTransport` |

So the corrected hunt is not "find a number Ω." It is: **state the object as the
fibration Codex proposed (`π : E → C`) with the fiber functor as its one observable,
and prove that each face above is a named invariant of that functor.** Emptiness →
contextuality. Cardinality/entropy → frame entropy and share. Forward-invariance
under `T` → closure. Splitting rate under `T⁻¹` → production. Induced contraction →
rent. Loop transport → holonomy. Inter-fiber correlation → the common-driver gap.

The bridge theorem that survives the kills, stated as a target: **the faces are the
cohomology-style ladder of ONE restriction map** — existence of a section (degree-0
emptiness), size of the section space (entropy), dynamics on it (closure/rent),
transport of it (holonomy). The kills were each an attempt to equate two DIFFERENT
rungs of that ladder; the object is the ladder.

## Ω(c) — the enriched fiber system: the steelman, the misfits, and the remainder

*2026-08-27 (Eric's formulation, backed by the season's record). The candidate maximal
object is* **Ω(c) = (Fib_π(c), μ_c, T_c, ∇_c, g_c)** *— which microstates a context
cannot tell apart; probability within those fibers; dynamics acting on them; transport
between contexts; the cost of maintaining the quotient. Physical content: an effective
state is objectively real to the extent that microscopic evolution respects its
fibers; interaction splits them, control repairs them, internal information contracts
on physical timescales, and maintaining the autonomy has a measurable energetic cost.*

### The steelman — every component has a measured face, every clause a confirmed instance

| component | strongest support |
|---|---|
| **Fib_π** | the fiber ladder, machine-checked end to end: `closed_iff_fiber_invariant`, `both_closed_iff_product` (+256/256), `loop_asymmetry`, the NonFactoring quartet — the founding parity theorem WAS fiber-splitting |
| **μ_c** | share/`frameEntropy` as fiber measure; the tweezer battery: gains 100–300× above dwell-matched AR surrogates, view-robust ×4, contracting in TIME not samples |
| **T_c** | `rate_unique_on_range` — the quotient dynamics is DETERMINED, never chosen; C1's contraction curve (0.30 bits at 0.2 ms → 0.04 by 0.8 ms) on a cycled real memory |
| **∇_c** | `ClaimTransport` + `comp_failure_convicts_second_leg` with TWO hardware instances; the rent law transferring to a Wilson-loop holonomy at 9.8 % |
| **g_c** | ΔW = ΔKE staked blind and confirmed (1.36, 0.607 ∈ [0.5, 2]); OptMulti staked < 0.5 and read −0.081; K = 1.0012 |

| clause | confirmed instance |
|---|---|
| interaction splits fibers | hardware one-way: 510× directional, correct sign; common-driver discriminator confirmed on hardware (defects 0, created 0.62 nats) — influence separated from correlation |
| control repairs them | optimization manufactures closure at TWO levels (witness power 0.07→0 across the protocol ladder; 250× within-erasure); OptMulti as an energy REGULATOR (third face) |
| information contracts on physical timescales | τ_c ≈ 20 ms (tweezer, surrogate-beaten); C1 contraction; KE identity exactly one drive deep ≈ τ_R |
| autonomy has energetic cost | the rent law — two rule-6 forward confirmations on someone else's calorimetry |

One estimator chain, unchanged, produced lawful readings on five substrates. That is
the steelman, and it is not thin.

### The misfits — each miss convicts a frozen-model OMISSION of a component Ω already carries

- **B1 (independent sessions read coupled) → μ_c is load-bearing, not decoration.**
  Determinism is a universal common driver; "splits" has no null without genuine
  measure. The frozen model ran a μ-FREE reading of Ω and the substrate refused it.
  The falsification killed the μ-free projection — the enriched tuple is what
  survives, and B1 is its proof of necessity.
- **B3 (no contraction at any lag) → contraction is a (T_c, μ_c) JOINT phenomenon.**
  A deterministic quotient chain never mixes, so fiber information never washes. This
  converts the contraction clause from an assumption into a THEOREM TARGET: defect at
  lag m bounded by the induced chain's mixing coefficient — Markov-chain mathematics,
  Lean-able, with B1/B3 as corollaries instead of embarrassments.
- **B2 (coupled halves at floor at lag 1) → the stake ignored ∇_c's light-cone.**
  Influence propagates at finite speed; `Aggregation.DependsWithinUpTo` carries the
  radius already, and the freeze didn't use it. Cross-defect stakes inherit the
  substrate's propagation time from (∇_c, g_c).
- **B4 (the interventional arm PASSED) → "evolution respects its fibers" is a
  do-statement, not a see-statement.** The observational projection of Ω fails on
  deterministic substrates; the interventional one read K = 1.0012 cleanly on the
  same data. Ω's reality clause is operationally interventional.
- Already absorbed from earlier rounds: g_c prices the QUOTIENT dynamics' decay, not
  the splitting defect (atlas H1); T_c/∇_c denote the REALIZED maps
  (`comp_failure_convicts_second_leg`, twice measured); and Ω's own parameters are
  rented (`hardware-bands-in-job-anchors`).

### The remainder — five bricks between here and the maximal

1. **THE MIXING THEOREM** (Lean, the keystone): for the induced chain `T_c` with
   mixing time τ_mix under μ_c, the closure defect at lag m contracts at τ_mix;
   deterministic ⇒ no mixing ⇒ no contraction. Makes the contraction clause a theorem
   given (T_c, μ_c), with τ_R and the 20 ms tweezer reading as its measured instances
   and B1/B3 as its corollaries.
2. **THE INTERVENTIONAL SIGNATURE**: define splitting via g_c-costed probes
   (B4-style); prove product ⟺ probe-response factorizes; it is the signature valid
   on BOTH substrate classes.
3. **μ_c IN LEAN**: `StochasticHabit`'s R3 successor (the DPI-based σ) is literally
   the missing formal component.
4. **g_c DERIVED**: W* priced by T_c's spectral gap — the H1′ function f, derived not
   fitted, with three substrates of rent data waiting to test it.
5. **∇_c CURVATURE** (atlas v2's transport layer): the last untested bridge —
   holonomy of ∇_c vs closure defect of state-dependent fibers.

Then the successor composition freeze: Ω tested AS THE TUPLE — all five components
load-bearing, interventional signatures where determinism lives, binary exit. That
claim is new, and it is the maximal one.

## The surviving hunts, sharpened

- **H1′ — excess cost of the hidden sector.** For a NON-closed view:
  `W*(non-closed) − W*(matched closed model) ≥ g(Δ_v)`, g derived not fitted. This is
  the residual work bridge and the first target for atlas v2.
- **H2 — closure ↔ curvature.** Needs the transport layer in the atlas (context
  graphs with transport loops). The stack is the only place D_v and F_γ can unify.
- **H3 — share ↔ contextuality, as a functor.** Build the induced empirical model of
  (state, chart, cover); test qShare vs contextual fraction on C5 (a known
  contextuality witness) and on nulls.
- **Hardware:** the four-arm intervention matrix (restoration job queued —
  `da7gslrsq5js73bjunl0` — is its joint-view arm), then the common-driver arm the
  atlas mandates; calorimetric second platform for whatever survives.

## Evidential standards (inherited verbatim)

Predicted non-closure: family-wise 5σ. Predicted closure: pre-registered equivalence
bounds — failing to reject zero is nothing. The unified object: one frozen structure
predicting all arms with better held-out economy than separate models, then a second
platform with no refitting. Anything less stays synthesis.
