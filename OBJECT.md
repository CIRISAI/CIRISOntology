# OBJECT — the maximal object, stated once

*2026-08-24. The mathematical description of the object the stance keeps
projecting, with the philological terms primary. Every row cites its
machine-checked witness. The unification is `CIRISOntology/Core/Factoring.lean`;
its two residues are reported below as loudly as the unification, per the stake —
R1 still resisting — REFINED 2026-08-24 to name cross-root CLAIM transport specifically, after
PR #12 supplied the correspondence layer it had been bundled with — R2 discharged the same day by
`CIRISOntology/Core/Pointing.lean`.*

---

## The object

**One kind of arrow, two roles, one dynamics.**

- **World** — a state space `X`. Nothing else is assumed of it.
- **Arrows** — maps between state spaces. They occur in exactly two roles, and the
  roles are not two primitives:
  - a **VIEW** is an arrow out of a fixed `X`, ordered by the one relation

    > **`Factors u v ≔ ∃ h, u = h ∘ v`** — *everything u knows, v determines.*

  - a **TRANSPORT** is an arrow between different roots. `Core/RerootTransport.lean`
    gives the square that carries a claim along one.
- **Habit** — a step map `T` on `X`, with noise. The ledger metaphysics is `T`'s
  interaction with the arrows.

**WHY THE TWO ROLES ARE ONE PRIMITIVE, AND IT IS PROVED RATHER THAN STIPULATED.**
The roles behave differently for exactly one reason: **a view loop factors through a
common source and is therefore pinned; a transport loop has no common source and is
free.** `loop_asymmetry` states both halves together — `mediator_fixes_range` pins
any self-mediating view to the identity on its range, while
`transport_loop_can_be_nontrivial` exhibits a cycle of maps composing to something
else. So the object needs no separate `Transport` primitive; it needs the
observation of whether a loop shares a source. Both need only `propext`.

**THIS IS WHAT R1 WAS.** R1 was carried for a season as an open residue of a
three-part object — cross-root claim transport "not supplied by `Factors`." It is
not a gap. `Factors` compares arrows out of a common source, and a re-root has no
common source to compare through; the flatness of the view axis is precisely why no
amount of work on `Factors` could ever have produced it. **R1 was the second role
announcing itself.** `ClaimTransport` is its grammar, and the openness that remains
is per-claim licenses, not the shape of the object.

**WHAT IS DERIVED, NOT PRIMITIVE.** Two qualifiers that read like extra structure
are theorems:

- **"physically privileged" views** are the `Closed` ones — `Closed v T ≔ Factors (v ∘ T) v`,
  a view whose future is predictable from itself (`Core/Habit.lean`). A privileged
  scale is not declared; it is whatever closes.
- **"induced" dynamics** is `rate_unique_on_range`: at every tier below the top the
  child's step is DETERMINED by the parent's `(T, v)` and never chosen.

So the object is `(World, Arrows, Habit)` with privilege and inducedness falling out,
not `(state, privileged views, induced dynamics, transport)` with four things
stipulated.

**KILL, separable.** Exhibit a transport in this programme's scope that is not a map
— a relation, a span, or something needing a 2-cell — so that views and transports
cannot be the same primitive. That takes down the collapse and returns `Transport` to
primitive status, leaving `loop_asymmetry` true but no longer load-bearing.

The stance's shapes are positions and motions in this object. That is the sense in
which the published page's complexity is a projection: many faces, photographed one
at a time, of one triple.

## The dictionary — philological terms as positions in the order

| philological term | position/motion in the object | machine witness |
|---|---|---|
| **frame** | a view | `Core/FrameOrder`, `Core/FrameAxis` |
| **refinement / coarsening** | moving up / down the Factors order | `FrameAxis.CoarserThan` = `Factors` (`coarserThan_iff_factors`) |
| **re-root** | changing to a view not necessarily comparable in the current chain — independent named CORRESPONDENCES may still relate selected claimants across roots (see R1) | `GrainFloor.admissibility_change_is_reroot`; PR #12's probe |
| **correspondence / receipt** | a named witness relating positions in two re-rooted presentations. **Record-like**: data ABOUT the order, not a position in it — and provably weaker than transporting a claim | PR #12 (`reroot-holonomy.rs`), spatial sector only |
| **fiber** — *what refinement has not yet revealed* | the preimage a view cannot split | `FrameEntropy.fiber` |
| **entropy** | log-size of the fiber; monotone along the order, extensive under products, free of charge | `frameEntropy_refine_le`, `frameEntropy_add`, `np_fiber_card` |
| **claim** | a demanded view | `GrainFloor.Claim` |
| **tier** | a held view | `GrainFloor.Tier` |
| **admissible** | the demanded view factors through the held one — *on a nested ladder* (residue R1) | `Factoring.grainFactors_iff_le` |
| **floor refusal** — *"I cannot see finely enough"* | demanded view above the held one but present elsewhere in the order — frame-relative | `GrainFloor.inadmissible_persists`, `floorDemand_frameRelative` |
| **ceiling refusal** — *"there is nothing finer"* | demanded view absent from the order entirely — invariant under every re-root | `capDemand_not_frameRelative`, `flux_ceiling_refuses_at_every_tier` |
| **Logos** — whole-only content | quantities **not generated** by the partial views: `¬ Factors q (joint view)` | `NonFactoring` (five witnesses), `nonFactoring_iff_not_factors_joint` |
| **pairwise blindness** | a specific non-generation witness | `pairwise_blind_to_parity`, `cp_phase_invisible_to_pairs`, exchange sign, isomer, Record |
| **physics is simulable** | the dynamics T factors through local views | `Locality.iterate_factors_through_ball` |
| **chart** | a view a process computes with | `SelfAudit.chartData`, `ModeChart` |
| **the fence** | the chart's assumption measured against the exact state | `meanOcc` fence; measured face D_bool 0 → 0.44 |
| **self-audit** | a view of the chart's view | `SelfAudit` |
| **a self-consistent lie audits clean** | audits in the stationarity ideal read zero on every converged chart | `stationarityAudit_blind` |
| **the door** | audits outside the ideal — theorem-pinned anchors | `pinned_error_computable_from_chart`, `not_stationarityAudit_of_fires`; field face D1b 9/9 |
| **posed question** — *only differences interrogate* | the contrast does not factor through the trivial view; two solves exhibit the witness pair | `Posed.Poses`, `poses_iff_not_factors_trivial` |
| **VOID vs KILLED** | the Σ-pair's two components failing separately | `Posed.adjudicate_void_iff` |
| **reads clean** — *a pointing* | the coincidence set of maps the object already names; **not** a second primitive (R2) | `Pointing.clean_value_forced`, `basepoint_forced`; fence `exists_step_with_rest_eq` |
| **rest** | the dynamics coinciding with standing still — one of the five pointing families | `Pointing.Rest`, `motion_eq_zero_iff_fixed`, `rentDeficit_eq_zero_iff_fixed` |
| **rent** | work injected to hold a reading fixed under T | `Maintenance.rent_holds`, `underpaid_shrinks` |
| **decay** | unpaid drift down the order | `unpaid_decays` |
| **mint / valve** | T + noise creating non-generated positions, one way only | `Creation.repair_mints_from_noise`, `Valve.valve_upward_strict` |
| **maintenance creates the payer** | the mint's fixed-point reading | `repair_creates_ferro` |
| **stagnation** | T's fixed points read zero motion whatever the error; motion does not factor to error | `Stagnation.error_not_computable_from_motion` |
| **the certificate of motion** | nested optima are monotone, so regressions convict from reports alone | `Stagnation.not_optimal_of_regression` |
| **Record** | not a position in the order — data **about** the order; the 11+1's one frame-relation | `repairable_does_not_factor`, `record_not_site_generated` |
| **only invariants individuate** | a position in a description is a fact only if pinned by an invariant | `FactorizationKill`, M15, `RouteGauge`, `GrainFloor.capacity_irrelevant` |
| **the observer is a claimant** | the observer's acuity is a demanded view, joined like any other | sandbox acuity pin; `MESH_DESIGN` §0 |
| **quantum ceiling** | the quantum view order exceeds the classical budget | `bell_ceiling_exceeds_cap`, `qShareK_max_five` |
| **exclusion / solidity** | the base frame's per-slot cap, enforced by type | `pauli_cap`, `level_cap`, `fhpChart` / `fchcChart` |

## The residues — one still resisting, one discharged

**R1 — cross-root CLAIM transport is not supplied by `Factors`** (refined
2026-08-24; the nested-ladder theorem below is still the reason). Thresholds
totally order lengths; factoring only partially orders views; they agree exactly
along a nested chain (`grainFactors_iff_le`), and unrelated scales do not factor
in either direction even where thresholds compare. The engine's charts nest **by
construction** (the octree), which is why the threshold model is faithful within
one re-root ladder — and the failure of factoring **across** ladders is the
order-theoretic reason certificates do not transport across re-roots. G4 was
never an engineering accident; it is non-comparability seen from inside.

**The refinement, and it separates three things this document had bundled.**

| | question it answers | status |
|---|---|---|
| `Factors u v` | is the information in one view determined by the other? | proved, `Core/Factoring.lean` |
| **correspondence** | which region/claimant HERE is the same one THERE? | **exists** for the spatial sector (PR #12) |
| **claim transport** | does a license granted in the source chart survive that correspondence? | **OPEN — but it now has a GRAMMAR**: `Core/RerootTransport.lean` (`ClaimTransport`, identity, composition, `carry_path_independent`), with the certificate as a provably separate second square. What remains open is per-claim licenses, not the shape of the question. |

PR #12 establishes the middle item and only the middle item, on one concrete
family: a Q32 fixed-point spatial claimant transported Sandbox → Grain → Crystal
against the direct Sandbox → Crystal, with the address factors DERIVED from the
existing tier table (1200, 500, and their product 600000). Direct and composed
agree exactly, the closed receipt round-trips to identity, and a planted wrong
middle factor (501) is caught — so the flatness is a measurement, not a
tolerance choice. Verified at `origin/experiment/reroot-correspondence`
(`a5cc6d2`) before this entry was written.

**THE GRAMMAR LANDED (2026-08-25), and the openness is now sharper rather than
smaller.** `Core/RerootTransport.lean` supplies the square R1 had been missing —
`targetClaim ∘ reroot = carry ∘ sourceClaim` — with identity, composition, and a
path-independence theorem that needs NO AXIOMS: direct and composed readings
agree on every presented source claimant whenever the underlying reroot maps
agree. So Newton, position, momentum, energy and orientation do not each earn a
separate composition theorem. **And the fence is proved twice**: the license is a
second square that cannot be derived from the first, shown once degenerately
(logical independence) and once on a target certificate that is SATISFIABLE and
still unreachable — a real license this correspondence does not deliver, which is
the obstruction R1 actually names rather than an artefact of an empty predicate.
A finite three-root instrument validates the grammar and catches a planted wrong
middle map.

**What this does NOT do, said plainly:** it licenses nothing. Every physical
claim still owes its own `CertifiedTransport`, which is exactly why R1 stays
open. A grammar for asking the question is not an answer to it — and the
`Physical` predicate from the same source branch, whose Kraus witness was never
constructed, is deliberately NOT taken: an undischarged predicate is a question
wearing a theorem's clothes.

**Stated narrowly, because the temptations here are obvious.** Spatial
correspondence exists and is path-independent on the integral Crystal–Grain–
Sandbox triangle. That is not "re-root transport is solved", not "R1 is
solved", and emphatically not "curvature has been found": the connection came
out FLAT (`H = id`), which is exactly what nested Euclidean addressing must
give. It validates the instrument; it discovers no geometry. Runtime re-root
semantics are unchanged — the physical session still resets — and the receipt
remains a diagnostic binary rather than core machinery, deliberately.

**What would move it.** Claim transport needs the stronger square to commute:
the claimed quantity `q` must satisfy `q_B ∘ R_AB = T_AB^q ∘ q_A` for some
INDEPENDENTLY justified transport `T^q` of that quantity — an object that does
not yet exist for anything content-bearing. The experiment that would test it
transports something carrying internal orientation or state, not merely
position, around a closed re-root loop; a nontrivial invariant `H ≠ id` that no
change of presentation removes would be genuine holonomy. Flat position-only
addressing cannot produce one, by construction.

**Why this is a `Pointing`-clean result rather than a coincidence hunt.** The
maps were named before the readings: `direct`, `composed`, `id`, in
`holon-sandbox/src/bin/reroot-holonomy.rs`. The findings are their coincidence
sets — `direct = composed` and `R⁻¹R = id` —
and the planted mutant proves the coincidence is not automatic. That is exactly
the non-vacuous form `Core/Pointing.lean` requires: existing maps first,
coincidence second, with a fence showing the agreement could have failed.

**R2 — RESOLVED, 2026-08-24 (`Core/Pointing.lean`). The object needs no pointing
primitive.** As stated the residue was: the stationarity ideal is `Factors`
**plus** `φ 0 = 0`, so a "reads clean" value is distinguished data and the honest
count is two. It is one. The pointing is **eliminable**: factoring ALONE forces
an audit to agree wherever the residual agrees (`factors_const_of_residual_eq`,
no `Zero` on either codomain, no convergence hypothesis), so `φ 0 = 0` does not
decide which charts read clean — it **names** the constant `Factors` had already
forced into existence (`clean_value_forced`). What the name buys is
**calibration**, and its price is exact: without it the escape criterion needs
two converged charts that disagree, and the one-point version convicts the
conjunction of factoring and calibration (`fires_at_pinned_convicts`). So
**one-point escape is what an imported truth-pinning theorem pays for: R2's
pointing traces to THE DOOR** (`pinned_error_computable_from_chart`; the symmetry
anchors are the currency), **not to Habit.**

The general statement, and the families are the finding: **every pointing in the
lake is the coincidence set of maps the object already names**, in five parent
families — Habit's rest (`Coincide T id`; `motion_eq_zero_iff_fixed`,
`rentDeficit_eq_zero_iff_fixed`), view-induced self-projection (the fixed set of
an idempotent the ORDER generates — the whole-only share's zero; shape only,
credited to Csiszár), symmetry (`Core/SignSymmetry`'s zero), the diagonal (truth
against chart — the door's home, `deviation_eq_zero_iff`), and the order's
extremes (`frameEntropy_eq_zero_iff` at the floor, `void_clean_eq_univ` at the
ceiling — VOID and determinacy are the same quantity at its two ends). Two
surveyed structures carry no pointing at all: `GrainFloor`'s refusal is a
threshold against tier-local data, `Lattice.np` an invariant with no
distinguished value.

**What this is NOT**, and the fence is machine-checked. Not "the pointing derives
from equality," and not "everything is an equalizer": both readings are EMPTY.
For any pointed view on any state space with two points there is a step map whose
rest set is exactly the clean locus (`exists_step_with_rest_eq`), and every clean
locus is the coincidence set of the view with a constant (`coincide_const_eq_clean`).
The content is entirely in NAMED — the maps the structure already carries, with
the basepoint then FORCED rather than chosen (`basepoint_forced`; constancy on
the locus is a real condition, and `not_restPointed_witness` shows it can fail).
Producing a dynamics after the fact to fit a zero is not evidence in either
direction. Separable kill: exhibit a pointed structure in this lake whose clean
locus is not the coincidence set of maps the structure already names — one
outside all five families — and R2 returns to primitive status with the miss
recorded.

## The object at depth — one statement

*2026-08-26. This section replaces four written separately on 2026-08-25; they said
facets of one thing and are stated once here. Every row carries its status and its
witness. Readings are marked as readings.*

### 1. The object is a presheaf, and ONE axiom separates classical from quantum

A state, a cover of views, restriction between them. `Factors u v ≔ ∃ h, u = h ∘ v`
is the restriction map. Exactly one assumption separates the two cases: **whether
the cover has a global section.**

Classically the cover is directed and has a top — every view factors through the
identity view — and the whole-only share is capped at `(k−3)·ln2`
(`shareK_le_of_pair_uniform_ge_four`). Quantum-mechanically **the top comes off**:
`vnEntropy_PsiC5 = 0` while `pairPtr_PsiC5` gives every pair a full `2·log 2`, which
`Core/BellCeiling.lean` calls *the non-monotonicity that has no classical analogue*.
The parts know more than the whole and the share reaches `5·ln2`, the five-slot
maximum (`qShareK_max_five`), two bits above any classical cover
(`bell_ceiling_exceeds_cap`).

**That pair is the whole machine-checked separation.** Marginal-≤-joint for classical
distributions is textbook and is NOT proved here. Everything else in this section is
reading.

**CREDIT**, and `Core/NonFactoring.lean` already carries the sweep: the
presheaf-and-global-section reading is Abramsky–Brandenburger 2011, with
Abramsky–Mansfield–Barbosa's Čech invariant and Atserias–Kolaitis (JACM 2025). Ours
is the mechanization of four instances in one typed shape plus `bell_ceiling` as the
witness that the cover is genuinely non-directed.

### 2. Views is the FLAT axis — so curvature has exactly one place to live

One fact, three levels:

| level | the loop | status |
|---|---|---|
| **State** (re-roots) | a cycle `A → B → C → A` | **holonomy expressible** — a re-root is a CHOSEN map. Measured once: `G_∞(q) = q/(ε + qλ)` transfers to a Wilson-loop holonomy at max residual 9.8 % (`HOLONOMY_RENT_RESULTS`) |
| **Claim** (`ClaimTransport`) | the carried claim round that cycle | **curvature-transparent, proved.** `carry_path_independent` is CONDITIONAL on `rac = rbc ∘ rab`: the claim layer adds no holonomy and faithfully inherits the state layer's |
| **Views** (`Factors`) | a cycle `u → v → w → u` | **PROVABLY FLAT** — `factors_cycle_trivial`, `Core/Factoring.lean` |

`mediator_fixes_range` is the whole content in two lines: *any map carrying a view
back to itself is the identity on that view's range.* Every cycle is an instance.
All three declarations need **no axioms**.

And it is not flat merely because `Factors` quantifies existentially.
`factors_two_cycle_trivial` deliberately does not take the `Factors` hypotheses — it
takes the mediating maps themselves. Being handed a choice of restriction is
strictly stronger than being told one exists, and the loop is still pinned to the
identity.

**Consequence: curvature cannot live on the cover.** It has exactly one axis
available in this object, the transport, which is where the holonomy campaign
measured. **Limit**: this is a statement about THIS object's `Factors` order, not
about nature, and it does NOT survive a state-dependent cover — the presheaf → stack
upgrade — because the mediators would stop being plain functions out of a fixed `X`.
It is a fence and a signpost for what that upgrade must break.

### 3. The object is RECURSIVE: a tier is a Closed view, not a declared type

A View's codomain is a set, and nothing stops it being a World. `Core/Habit.lean`
says exactly when it is:

> `Closed v T ≔ Factors (v ∘ T) v` — the view determines its own successor.

Then a rate map `φ` exists on `C` and `(C, Views of C, φ)` **is the object again**. A
Closed view IS a tier and `φ` is its Habit. `rate_unique_on_range` makes the child's
dynamics DETERMINED by the parent's `(T, v)`, never chosen — no free parameter at any
depth. `Held` (`v ∘ T = v`) is the `φ = id` fixed point of the same recursion.

**So tiers are fixed points, not a taxonomy**, and this locates the branch schema's
error: `experiment/quantum-native-r1` wrote eight substrate tiers as eight declared
types, but `exists_closed_view` makes "is a tier" EMPTY as a unary predicate — every
`T` closes the view `T` itself. The content is the pair (step map, NAMED view).
Sandbox/Grain/Crystal are three closures of one object.

`Core/Aggregation.lean` supplies the approximate rung with a cost model: closure to
within `ε`, composition `εG + K·εF`, horizon budget linear at **`K ≤ 1`**. That
inequality is the horizontal-scaling condition, and it is MEASURABLE rather than
assumed — the file is explicit that `horizonBudget_le_of_nonexpansive` is there to
USE the budget, never to establish it.

**Where it bottoms out.** Read the Kraus lift `Φ_T(diag p) = diag(T_*p)` in the
recursion and the classical layer is a view of the quantum one: `ρ ↦ diag ρ`. That
view is Closed **exactly when decoherence has happened** — by construction for a
measure-and-prepare channel, and not for a general unitary, since `diag(UρU†)ᵢᵢ`
reads the off-diagonal `ρⱼₖ`. **Coherence IS the non-closure of the classical view**,
and `not_closed_witness` is already that shape in miniature. So a QASM circuit is a
Habit one level down — gates are the step map and `split_two_site` is already the
primitive that applies one. **The descent cannot be collapsed**:
`bell_ceiling_exceeds_cap`.

### 4. Coupling is a pair of non-closures — the connection stops being background

`Core/MatterCoupling.lean`. The engine had two halves and no join: a DYNAMICAL
plaquette flux (`one_plaquette_hamiltonian`, `H = 4g²E² − κ(U+U†)`) with no matter in
it, and a walker in a BACKGROUND holonomy. K1 (`Core/RouteGauge.lean`) killed
identifying those carriers; it does not forbid coupling two distinct ones.

The coupling needs **no new primitive**. Matter moves flux and flux gates matter, so
neither view is `Closed`: `matter_not_closed`, `flux_not_closed`. Were there no
back-reaction each view would predict its own successor. **Back-reaction IS the
mutual failure.** `gauss_held` is the non-vacuous positive — charge and flux locked
mod 2, so charge cannot move without moving flux — with `gauss_is_lossy` showing that
view genuinely discards information.

**`independent_views_closed` is what makes this a detector rather than a
restatement**: when the step is a product map, BOTH component views are Closed, for
every such map. Non-closure is not a generic affliction of lossy views; it fires
exactly on interaction. Axiom-free.

**What K1 leaves standing, and the flatness theorem privileges it.** K1 killed *the
grading* — "which term carries which Gauss charge" — which `RouteGauge` itself calls
a property of the presentation. **That is a view-axis quantity, and the view axis is
flat**, so a gauge structure living there was doomed by theorem;
`grading_is_gauge_pinned` is the concrete instance. What survived is the
matter-position reading, a transport-axis quantity — the only axis left open.

**Three holonomies, which must not be merged**: plaquette flux (dynamical, exact),
route walker (background φ), Record (a frame relation, different axis).

### Status

| rung | status |
|---|---|
| classical cap vs quantum ceiling | **proved** — `shareK_le_of_pair_uniform_ge_four`, `bell_ceiling_exceeds_cap` |
| the view axis is flat | **proved, axiom-free** — `Core/Factoring.lean` |
| claim transport is curvature-transparent | **proved** — `carry_path_independent` |
| `Closed` generates a child object, determined | **proved** — `Core/Habit.lean` |
| "is a tier" is empty as a unary predicate | **proved** — `exists_closed_view` |
| approximate closure, linear at `K ≤ 1` | **proved** — `Core/Aggregation.lean` |
| back-reaction as mutual non-closure, with its detector | **proved on a 6-state model** — `Core/MatterCoupling.lean` |
| rent law transfers to a Wilson-loop holonomy | **measured**, 9.8 % — `HOLONOMY_RENT_RESULTS` |
| the mesh's ACTUAL tiers are Closed views of one another | **UNMEASURED** |
| `K ≤ 1` on the real mesh | **UNMEASURED** — the horizontal-scaling condition |
| the engine's classical/quantum relation IS the diagonal lift | **NOT IMPLEMENTED** — no dependency edge exists |
| a dynamical connection in the ENGINE (not a 6-state model) | **OWED** |

### Kills, separable

- **The presheaf reading dies** if a result in scope is stateable in the quantum
  object but NOT as a presheaf over the view cover — one genuinely needing a tiered
  carrier rather than the dropped join.
- **The recursion reading dies** if two declared tiers have no rate map on the
  coarser reading and fall outside `Aggregation`'s budget: the stack is a taxonomy
  after all. `Core/Habit.lean` is untouched either way.
- **The coupling reading dies** if a step on a product space has both component views
  non-Closed while the components genuinely do not interact.
- **What the object is FOR**, distinct from its kills and already the stance's open
  question: find a WILD system whose whole-only share exceeds the classical cap. Every
  wild measurement to date is a CLASSICAL statistic under classical caps, which is why
  glass, water, CMB and flavour all read null WITHOUT touching it.

---

## Scope, and the kill

This document asserts a *reading*: that the season's machine-checked results
are positions and motions of (World, Views, Habit). The reading's kill,
separable and staked in `Core/Factoring.lean`: exhibit one of the unified
predicates whose intended use the Factors reading provably mis-adjudicates,
and that predicate returns to primitive status with the miss recorded. The
wagered physics (rent in e, audit in π; law-as-habit; precedent-is-bits)
remains wagered — this object is the *grammar* those wagers are written in,
and a grammar is not evidence for its sentences.

*The philological names are primary. The mathematics labels them; not the
reverse.*
