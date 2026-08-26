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
