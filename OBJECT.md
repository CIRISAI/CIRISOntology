# OBJECT — the maximal object, stated once

*2026-08-24. The mathematical description of the object the stance keeps
projecting, with the philological terms primary. Every row cites its
machine-checked witness. The unification is `CIRISOntology/Core/Factoring.lean`;
its two residues are reported below as loudly as the unification, per the stake —
R1 still resisting, R2 discharged on 2026-08-24 by `CIRISOntology/Core/Pointing.lean`.*

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
| **re-root** | changing to a view not comparable in the current chain | `GrainFloor.admissibility_change_is_reroot` |
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

**R1 — admissibility is factoring only on nested ladders.** Thresholds totally
order lengths; factoring only partially orders views; they agree exactly along
a nested chain (`grainFactors_iff_le`), and unrelated scales do not factor in
either direction even where thresholds compare. The engine's charts nest **by
construction** (the octree), which is why the threshold model is faithful
within one re-root ladder — and the failure of factoring **across** ladders is
the order-theoretic reason certificates do not transport across re-roots. G4
was never an engineering accident; it is non-comparability seen from inside.

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
