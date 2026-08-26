# The invariant hunt — one defect, four faces, and what survived its first day

*2026-08-26. The search program for the maximal object's unique observable, absorbing
an external proposal (Codex, via Eric) and the first atlas run. This document is the
umbrella; stakes and readings live in `scratchpad/atlas/`.*

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
