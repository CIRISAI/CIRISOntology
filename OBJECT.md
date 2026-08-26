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

**(World, Views, Habit)** — one state space, one order, one dynamics.

- **World** — a set of states X. Nothing else is assumed of it.
- **Views** — every lossy summary `v : X → C`, ordered by the one relation:

  > **`Factors u v ≔ ∃ h, u = h ∘ v`** — *everything u knows, v determines.*

  This order is the only structure the season's theorems consume. Its
  completeness bridge (`factors_iff_not_separatesFiber`): a quantity factors
  through a view **exactly when** no witness pair separates a fiber — so the
  lake's negative results and its positive licenses are the two signs of one
  biconditional.
- **Habit** — a step map T on X, with noise. The ledger metaphysics is T's
  interaction with the view order.

The stance's shapes are positions and motions in this object. That is the
sense in which the published page's complexity is a projection: many faces,
photographed one at a time, of one triple.

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
maps were named before the readings: `R_direct`, `R_composed`, `id`. The
findings are their coincidence sets — `R_direct = R_composed` and `R⁻¹R = id` —
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

## The reading: one axiom separates the classical object from the quantum one

*Added 2026-08-25. This is a READING of results already in the tree, not a new
claim about nature, and it is labelled as one throughout.*

The object above is a **presheaf**: a state, a cover of views, and restriction
between them. `Factors` is the restriction map. Read that way, exactly one
assumption separates the classical object from the quantum one — **whether the
cover has a global section.**

Classically the cover is directed and has a top: every view factors through the
identity view, and a part never carries more entropy than the whole — the
standard marginal-≤-joint fact for classical joint distributions, **cited here as
textbook and NOT as a repository witness**, because this repo does not prove it.
What this repo does prove is the consequence that matters: the whole-only share
is capped at `(k−3)·ln2` from four slots up
(`shareK_le_of_pair_uniform_ge_four`).

*(A correction worth keeping, because the error is easy to repeat: an earlier
version of this paragraph cited `frameEntropy_refine_le` for that monotonicity.
That theorem is about a different quantity — the log-count of a CHART's unrevealed
fiber, which refinement lowers — not the entropy a STATE carries across views. It
is the quantity that goes non-monotone below, so the two must not be conflated.)*

Quantum-mechanically **the top comes off.** `vnEntropy_PsiC5 = 0` while
`pairPtr_PsiC5` gives every pair a full `2·log 2` — `Core/BellCeiling.lean`'s own
header calls it *the non-monotonicity that has no classical analogue*. The parts
know more than the whole; the order and the information measure come apart; the
share reaches `5·ln2`, the five-slot maximum (`qShareK_max_five`), two bits above
anything a classical cover can carry (`bell_ceiling_exceeds_cap`). **That last
pair is the whole machine-checked separation**: `shareK_le_of_pair_uniform_ge_four`
above, `bell_ceiling_exceeds_cap` below, both proved here. Everything else in this
section is reading.

So the quantum-native content is one sentence: **there is no common refinement.**
Not that information was lost — that there is no state space on which both views
are functions.

**WHAT THIS RECLASSIFIES.** Two residues stop being unfinished work and become
correctly-identified primitives.

- **R1 is the classical shadow of contextuality.** A claim cannot be transported
  across incomparable roots BY REFINEMENT, because in the general object there is
  no common refinement to route through. The transport must therefore be a named
  commuting square supplied per claim — which is exactly `ClaimTransport`. R1
  could never have been closed by forcing every root into one `Factors` chain,
  and that now has a reason rather than a track record of failed attempts.
- **R3's repair is forced rather than chosen.** `σ ≥ 0` fails for channels
  because it is stated about the STATE's entropy, which is not monotone here.
  DPI restores it because relative entropy IS monotone under the restriction
  maps — that is, the successor's job is to make the step a MORPHISM of the
  presheaf, which is what `Core/StochasticHabit.lean` still owes.

**CREDIT.** Almost none of this framing is ours, and `Core/NonFactoring.lean`'s
header already carries the sweep: the presheaf-and-global-section reading is
Abramsky–Brandenburger 2011, with Abramsky–Mansfield–Barbosa's Čech invariant and
Atserias–Kolaitis (JACM 2025). Ours is the mechanization of four instances in one
typed shape, plus `bell_ceiling` as a machine-checked witness that the cover is
genuinely non-directed. Scope-corroboration, never a first.

**WHERE THE SCHEMA WENT SIDEWAYS**, recorded so it is not rebuilt.
`experiment/quantum-native-r1` built a `Physical` structure, eight substrate
tiers, and a second quantum `World` ALONGSIDE the classical one, with R1 restated
as "a second square." But this is the same object with the join dropped, not a
new object needing a new schema. A taxonomy of substrates is not an object, and
at eight tiers there is no universality left to have. Nothing from that branch is
imported here beyond the Q8 SVD repair it also produced, which was taken on its
own merits and independently reproduced.

**KILL, separable.** Exhibit a result inside this programme's scope that is
stateable in the quantum object but NOT as a presheaf over the view cover — one
that genuinely requires a tiered carrier rather than the dropped join. That would
show the collapse to a single object is false economy and the branch's schema was
right after all.

**WHAT THE OBJECT IS FOR** — distinct from its kill, and already the stance's own
open question. Every wild measurement to date (glass, water, CMB, flavour, BOSS)
is a CLASSICAL statistic under classical caps, which is exactly why they all read
null WITHOUT touching this question. The instrument this reading names is: find a
wild system whose whole-only share exceeds the classical cap. That would show the
cover is non-directed in nature and not only in the model.

---

## The holonomic loop, stated once — and why Views is the flat axis

*Added 2026-08-25. The loop shape is DRY'd here: one fact, three levels. Two
levels are proved in this repository; the status of each is given, not blurred.*

**The shape.** Go around a closed path and ask what came back changed. Written
once, it is: *a map that carries something back to itself* — and the whole
question is whether that map is the identity.

| level | the loop | status |
|---|---|---|
| **State** (re-roots) | a cycle of re-root maps `A → B → C → A` | **holonomy is expressible** — a re-root is a CHOSEN function, so the composite need not be `id`. Measured once: the maintained-holonomy campaign, `G_∞(q) = q/(ε + qλ)` transferring at max residual 9.8 %. |
| **Claim** (`ClaimTransport`) | the carried claim around the same cycle | **curvature-transparent, proved.** `carry_path_independent` is CONDITIONAL on `rac = rbc ∘ rab`: the claim layer adds no holonomy of its own and faithfully inherits the state layer's. |
| **Views** (`Factors`) | a cycle of factorings `u → v → w → u` | **PROVABLY FLAT.** `factors_cycle_trivial`, `Core/Factoring.lean`. |

**The view axis is flat, and this is a theorem rather than a gap.**
`mediator_fixes_range` is the whole content in two lines: *any map carrying a
view back to itself is the identity on that view's range.* Every cycle is an
instance — collapse it with `factors_trans` and apply the core. All three
declarations depend on **no axioms**.

**And it is not flat merely because `Factors` quantifies existentially.**
`factors_two_cycle_trivial` deliberately does NOT take `Factors u v` and
`Factors v u` as hypotheses: it takes the two mediating maps themselves. Being
HANDED a choice of restriction is strictly stronger than being told one exists,
and the loop is still pinned to the identity. So the flatness survives choosing
the maps by hand — it is a property of the view order, not an artifact of how
the order is stated.

**WHAT THIS BUYS, and it sharpens the reading above rather than repeating it.**
That section called quantum and curvature "two independent axes — quantum
deforms the cover, curvature deforms the transport." The independence is now
one-sided and provable: **curvature cannot live on the cover at all.** In this
object it has exactly one axis available to it, the transport, which is where
the holonomy campaign already measured. That closes off an avenue rather than
opening one, which is the useful direction for a fence to point.

**What it does NOT buy**, stated because the temptation is real. A flat view
axis is not an argument that nature's view-cover is flat; it is a statement
about THIS object's `Factors` order. If the cover is ever made state-dependent —
the presheaf → stack upgrade the reading above names as the blocker — this
theorem does not survive the upgrade, because the mediating maps would no longer
be plain functions out of a fixed `X`. **The theorem is a fence on the current
object and a signpost for what an upgrade must break**, and it is the cheapest
available statement of what that upgrade would cost.

**The related campaign, at its actual strength.** `HOLONOMY_RENT_RESULTS`
returned *maintained in size, lost in structure*: the plateau holds at 0.435 to
six decimals out to R=4001 while the unmaintained loop falls 65 orders, and
fidelity stays at 0.9909 ONLY when the repair knows the design. The rent law
transfers at 9.8 % — quantitatively, by the pre-declared band. Two fences on
reading more into it than that: the residual is **operator structure**, and
removing the non-geometricity made it WORSE, so the scalar law is not carrying
the geometry; and `Core/RouteGauge.lean`'s **K1 killed the gauge
identification** (`grading_is_gauge_pinned` — the gauge content is a property of
the presentation, not of the route dynamics). One maintenance law with
three-substrate scope, which the campaign itself calls "a third substrate class
for a law measured on two." That is scope-corroboration, and it is not a
holonomic-dynamics equivalence.

---

## View dynamics: forced, not fitted — and the one staked prediction, audited

*Added 2026-08-25, in answer to "calculate the view dynamics for Factors by what
matches reality." The dynamics turns out not to be ours to calculate. What
reality can pin is something else, and the one staked prediction of that form
does not survive a pre-data audit.*

**THE DYNAMICS IS FORCED.** `Core/Habit.lean` settles it three times over:

1. **Precomposition is the only operation the object supports** — `T` acts on
   Views by `v ↦ v∘T`, and `pullback_monotone` shows that action is monotone on
   `Factors` for EVERY `T`. That is well-definedness, not characterization.
2. **The rate is determined, never chosen.** `rate_unique_on_range`: any two
   maps witnessing `v ∘ T = φ ∘ v` agree on the view's range. There is no free
   parameter for reality to fix.
3. **And the naive question is empty.** `exists_closed_view : Closed T T` —
   EVERY step map closes a view, namely `T` itself. So "the dynamics that closes
   views" excludes nothing. **The content is entirely in the pair (step map,
   NAMED view)**, which is the file's own vacuity fence.

So reality cannot select the view dynamics; it can only TEST a named view for
`Closed` (Kemeny–Snell lumpability), for `Held` (rent paid in full), or measure
its `production`. And selection is separately obstructed:
`Core/FrameSelection.lean` proves a unique intrinsic selector CAN fail to exist
(`no_equivariant_selector_of_fixed_state_free_screen`), with family-consistency
as the escape hatch.

### The one staked prediction, and its pre-data audit

`Core/Habit.lean` stakes **P-EDGE** — *entropy production switches on at the
stability edge and nowhere else in the smooth sector* — declared "before its
instrument exists." It appears in no results file and no test. Building it was
attempted here; **three findings arrived before any campaign ran, and together
they say the prediction as staked is not testable on this engine.**

**Finding 1 — the stated instrument is confounded, and confounded so as to
CONFIRM the prediction for the wrong reason.** The instrument is "step the scene
forward `n` and back `n` and count the states that fail to return." For the map
the theorem is actually about — explicit Euler, `x ↦ x + dt·f(x)` — forward-then-
back is not the identity even in EXACT arithmetic. For `f = −λx` it is exactly
`x·(1 − dt²λ²)`, so the relative round-trip error is `dt²λ²`: `0.01` at
`dt·λ=0.1`, `1.00` at the injectivity threshold, `4.00` at the stability edge. It
rises sharply near the edge **with no floats involved at all.** That is precisely
P-EDGE's CONFIRMS signature, produced entirely by integrator asymmetry.

**Finding 2 — the engine's own integrator has no onset to find.** The scene runs
**velocity Verlet** (`crates/sphere-demo`), which is symplectic, hence exactly
volume-preserving, hence injective in exact arithmetic at EVERY `dt`. Measured
round-trip error is `0` or one machine epsilon at `dt·ω` = 0.1, 1.0, 1.9, 2.0,
2.5 and 5.0 — flat across the stability edge and far past it. Instability shows
up as unbounded growth, never as non-injectivity. So exact-arithmetic production
is zero at all `dt`, and P-EDGE's own REFUTES clause ("production still at the
floor well PAST the edge") is satisfied structurally. The theorem is about
explicit Euler; the instrument steps a Verlet scene. **They are about different
maps.**

**Finding 3 — the factor-of-two premise holds only where the effect vanishes.**
P-EDGE compares injectivity (`dt·L < 1`, with `L` the GLOBAL Lipschitz constant
of `injective_of_lipschitz_step`) against stability (`dt·ω < 2`, set by the
linearized frequency at the operating point). Those coincide within a factor of
two only when `L = ω`, i.e. for LINEAR `f` — and there the degree count is
identically 1.0000 across `dt·λ ∈ [0.25, 1.3]`, because multiplying floats by a
constant is essentially bijective (float spacing scales with magnitude). Make `f`
nonlinear and there is something to measure — `f = −x − 3x³` on `[0.5,1]` reads
degree 1.3210, production 0.2784 nats — but that reading sits at `dt·λ = 0.25`,
DEEP inside the stable regime and *zero* nearer the edge, because `L = 10 ≫ ω`
there and the fold is a genuine exact-arithmetic non-injectivity that the
theorem's violated hypothesis explicitly permits. Nonlinearity buys a signal and
destroys the premise in the same move.

**Status: P-EDGE's premise is refuted structurally, before measurement, and the
refutation is separable** — it takes down P-EDGE and nothing else in
`Core/Habit.lean`. `injective_of_lipschitz_step` is untouched and remains proved;
what fails is the claim that its threshold tracks the stability edge.

### What IS buildable, and what it would measure

The measurable quantity is the one the Lean already names:
`production_id_eq_log_degree`, production `= log |T⁻¹(T s)|`. Count it directly —
enumerate a float lattice, apply ONE step, count distinct images — rather than by
round trip, which is what removes the Finding-1 confound. On a NON-symplectic
step it reads a real number, as the `0.2784` nats above shows. It measures folds
plus the float floor, and **the float production floor is the thing the header
says nobody has measured.** That is a genuine open instrument. It is not a test
of P-EDGE, and this document does not offer it as one.

---

## The object is RECURSIVE: a tier is a Closed view, not a type

*Added 2026-08-25. This section replaces "the mesh talks to the quantum sim"
with "they are the same object at two depths." Nothing external is introduced;
the recursion is generated by machinery already in `Core/Habit.lean`.*

**THE RECURSION, in one move.** A View is a lossy summary `v : X → C`. Its
codomain `C` is a set. Nothing stops `C` from being a World in its own right —
and `Core/Habit.lean` says exactly when it is:

> `Closed v T ≔ Factors (v ∘ T) v` — the view determines its own successor.

If `v` is Closed there is a rate map `φ` on `C` with `v ∘ T = φ ∘ v`. Then
`(C, Views of C, φ)` **is the object again**. A Closed view is not a summary of
a tier; it *is* a tier, and the tier's Habit is `φ`.

**The recursion is well-founded rather than a choice.**
`rate_unique_on_range` proves any two witnesses for `φ` agree on `v`'s range, so
the child's Habit is DETERMINED by the parent's `(T, v)` and never selected. The
object descends into itself with no free parameter at any depth. This is why
`Held` (`v ∘ T = v`) is the `φ = id` case: rent paid in full is the fixed point
of the same recursion, not a separate notion.

**SO TIERS ARE FIXED POINTS, NOT A TAXONOMY — and this is precisely where the
branch's schema went wrong.** `experiment/quantum-native-r1` wrote eight
substrate tiers as eight declared types. But a tier is not declarable: it is
whatever `Closed` returns at that depth, and `exists_closed_view` (every `T`
closes the view `T` itself) means "is a tier" is empty as a unary predicate. The
content is in the PAIR — a step map and a NAMED view. Sandbox, Grain and Crystal
are not eight-of-a-kind; they are three names for three closures of one object,
and the re-roots between them are the maps the recursion already supplies.

**The approximate rung, because exact closure is rare in the wild.**
`Core/Aggregation.lean` carries the quantitative form: `DependsWithinUpTo d r ε F`
is closure to within `ε`, composition costs `εG + K·εF`, and the horizon budget
`ε·∑Kⁱ` stays LINEAR at `K ≤ 1`. So a tier that is only approximately Closed is
still a tier, with a stated error budget, and depth is affordable exactly when
`K ≤ 1`. The recursion has a cost model, not just a predicate.

### Where the recursion bottoms out, and why QASM stops being external

Take the Kraus lift `K_x = |T(x)⟩⟨x|`, giving `Φ_T(diag p) = diag(T_*p)`: any
finite classical map lifts to a measure-and-prepare channel. Read it in the
recursion instead of as an embedding, and the classical layer is a VIEW of the
quantum layer — `ρ ↦ diag ρ`, read the populations, discard the coherences.

**That view is Closed exactly when decoherence has happened.** `Closed` demands
the output populations depend on the input populations alone. For a channel
built by the Kraus lift this holds by construction. For a general unitary it
fails — `diag(UρU†)ᵢᵢ` reads the off-diagonal `ρⱼₖ`, so the classical reading
cannot predict its own successor. **Coherence IS the non-closure of the classical
view**, and `not_closed_witness` in `Core/Habit.lean` is already this shape in
miniature: reading the first slot does not determine its own successor under
swap, because the successor reading is the second slot.

So the quantum layer is not another engine bolted beside the mesh. **It is the
next level down, entered exactly where the classical view stops being Closed.** A
QASM circuit is then a Habit at that level and nothing more exotic: gates are the
step map, `split_two_site` is already the primitive that applies one, and the
mesh's tiers are Closed views sitting above it. Running a circuit is running the
same object at a depth where `diag` is not Closed.

**And the recursion provably cannot be collapsed.** `bell_ceiling_exceeds_cap`:
the C5 ring state carries `5·ln2` where every classical cover caps at `3·ln2`.
The quantum level holds strictly more than any classical view of it can — so the
descent is forced, not stylistic.

### What this re-reads, and what it still owes

The dependency graph has no edge between `holon-mesh` and the quantum crates
(`q8-mps` depends on nothing; `q-seam` carries `ciris-sim-core` as a DEV
dependency only). Under the old framing that was an integration gap. Under the
recursion it is something more specific and more useful: **the missing artifact
is not a bridge, it is the CLOSURE TEST** — the check that says when the mesh's
classical view has stopped predicting its own successor and the finer level is
required. A bridge would be external plumbing; the closure test is the object's
own recursion step, and it is the honest thing to build.

| rung | status |
|---|---|
| `Closed` generates a child object; its Habit is determined | **proved** — `Core/Habit.lean` (`Closed`, `rate_unique_on_range`) |
| "is a tier" is empty as a unary predicate; content is (step, NAMED view) | **proved** — `exists_closed_view` |
| approximate closure with a composition budget, linear at `K ≤ 1` | **proved** — `Core/Aggregation.lean` |
| the descent cannot be collapsed | **proved** — `bell_ceiling_exceeds_cap` |
| the mesh's ACTUAL tiers are Closed views of one another | **UNMEASURED** — asserted nowhere, tested nowhere |
| the engine's classical/quantum relation IS the diagonal lift | **NOT IMPLEMENTED** — no edge exists |
| the closure test itself | **OWED** — the named next artifact |

**Kill, separable.** Exhibit two of the engine's declared tiers for which no
rate map exists on the coarser reading — i.e. the coarse tier is measurably NOT
Closed under the fine tier's step, and not Closed to within `Aggregation`'s
budget either. That would show the tier stack is a declared taxonomy after all
and not a chain of closures, and it would take down this section without
touching `Core/Habit.lean`, whose theorems are about the relation and not about
the engine's particular choice of tiers.

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
