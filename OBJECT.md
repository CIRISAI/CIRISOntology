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

**THE SQUARE.** One lossy arrow against one motion:

```
      X ──T──▶ X          T : the motion (a step in time, a re-root in context,
      │        │              a probe in the fiber direction, a channel in measure)
      v        v          v : the arrow — what a context can read
      ▼        ▼
      C ──h──▶ C          does an h exist, and is it the identity?
```

Two questions, and the whole programme is their graded answers:

> **`Closed v T ≔ ∃ h, v∘T = h∘v`** — does the arrow survive the motion at all?
> **`Held v T ≔ v∘T = v`** — does it survive UNCHANGED?

**ONE RELATION, EVERY AXIS — this is the squint, and it is proved, not poetic:**
`Held` on the TIME axis is rent paid in full (`Core/Maintenance.lean`); `Held` on
the CONTEXT axis is zero curvature (`curvature_iff_held`); `Held` on the MEASURE
axis is stationarity (`Stationary T π ≔ push T π = π`, `Core/MuChannel.lean`); and
the PROBE asks the square's question by force — a blind probe is a fiber-direction
motion, and interventional silence IS closure (`interventional_iff_closed`). The
faces of Ω(c) = (Fib, μ, T, ∇, g) are the five places the same two questions get
asked, and squares COMPOSE: when two motions commute, their answers commute
(`holonomy_commutes_with_rate`, axiom-free — curvature is an automorphism of the
habit).

- **World** — a state space `X`. Nothing else is assumed of it.
- **Arrows** — maps between state spaces, in two roles that are one primitive:
  a **VIEW** points out of a fixed `X` (ordered by `Factors u v ≔ ∃ h, u = h∘v`);
  a **TRANSPORT** runs between roots (`ClaimTransport`'s square, with the
  certificate a provably separate second square). The roles differ for one
  provable reason — a view loop factors through a COMMON SOURCE and is pinned; a
  transport loop has none and is free (`loop_asymmetry`). **Correction, from the
  atlas:** it is the common source that forbids view-curvature, not fixedness of
  the fibration — mode-moving re-roots over a fixed fibration carry holonomy.
- **Habit** — a step map `T` on `X`, with noise. `μ` is LOAD-BEARING, not
  decoration: without genuine measure the square's failure has no null
  (deterministic defect is `{0,1}`-valued and never contracts —
  `det_defect_zero_or_one`; contraction is what noise buys, `defect_noisy_le`)
  and only probes can ask the question (`Probe.lean`, Prop 5's orbit
  non-identifiability).

**THE OBSERVABLE IS THE FIBER, and the quantities are its graded invariants** —
each grading a way the square can fail, each with its machine-checked witness:

| grading of the square | it is called | witness |
|---|---|---|
| refinement — `v`'s fibers refine `u`'s | factoring | `factors_iff_not_separatesFiber` |
| splitting — a quantity splits a fiber | the founding NonFactoring shape | `SeparatesFiber`; `pairwise_blind_to_parity` was this all along |
| size — log-count of a fiber | entropy | `frameEntropy` |
| the step's own fiber — `log \|T⁻¹(Ts)\|` | production | `production_id_eq_log_degree` |
| forward-invariance — the step never splits a fiber | closure; a TIER | `closed_iff_fiber_invariant` |
| **contraction rate** — how fast the defect fades | mixing | **`defect_le_alpha_pow`**: ≤ α(T)^m; `{0,1}` and frozen when deterministic |
| **descent in measure** — distance to stationarity never rises | the μ-face of the arrow of time | **`sigma_antitone`** (DPI), with `AbsCont` proved load-bearing |
| **the forced question** — silence under every blind probe | intervention; the manufactured witness | **`interventional_iff_closed`**; common drivers silent by `rfl` (`common_driver_probe_null`) |
| **the price** — minimum dose holding retention | rent | **`Ginf_at_Wstar`**, `Wstar_strictMono`; ε = 1 − λ_track, measured on four substrates |
| multiplicativity — fibers of independent parts multiply | extensivity; its failure is the common-driver gap | `frameEntropy_add`; `both_closed_iff_product` + `product_iff_probe_null_both` |
| emptiness — the gluing fiber is empty | contextuality | the stack face — OPEN (`OBJECT_PRIOR_ART.md` S3) |
| **conditioning — how loudly a chart repeats a whisper** | the condition number of the view (Higham's condition number of summation, worn as physics) | **`sum_perturb_le`**: a per-term relative perturbation moves an aggregate by at most ε/coherence in the view's own units; the bound is ATTAINED (`sum_perturb_attained`); an all-nonnegative chart has coherence exactly 1 (`coherence_of_nonneg`) — measured in the field: ke sits at χ = 1.000 at every frame while momx COLLAPSES 0.998 → 0.125, and the ceiling explains cross-view divergence LEVELS at Spearman +0.996/+0.935 over 67 views. The rung Ω-3's N4 was missing: without it, chart conditioning and dynamical openness are one conflated reading, and the privilege question is not yet posable |
| loop transport — a cycle acts on a fiber | holonomy, curvature | `curvature_iff_held`, `holonomy_commutes_with_rate`; LOSSY holonomy exists (`lossy_holonomy_exists`), permutation only under reversible carry (`holonomy_bijective_of_reversible_carry`); zero holonomy and closure are logically independent (`flatness_without_closure`, `curvature_without_closure_failure`) |

**Predicates were the wrong currency, and the dead bridges are the evidence**:
each tried to equate two DIFFERENT gradings and died at the boundary, by
enumeration with minimal witnesses now machine-checked. The object is not a rung
and not a defect number. **It is the square, and the ladder is its invariant
theory.** And the DRY pass collapsed the corpus's two primitives into one:
**the founding NonFactoring shape IS the square's NO** —
`nonfactoring_iff_not_closed` (`Core/Habit.lean`): with the single view `v` and
quantity `v∘T`, a witness pair (two states agreeing under the view, differing
after the motion) is EXACTLY the obstruction to `Closed`. The square asks;
`Closed` is its yes; the founding shape is the certificate of its no — and the
corpus's five walls (parity, CP phase, Record, exchange sign, and now
COHERENCE) are five non-closure certificates for five named motions. The fifth
is new (`Core/DiagonalLift.lean`): the classical tier is a RETRACT of the
quantum carrier (`bornView ∘ diagEmbed = id`), its lifted dynamics the
classical step conjugated by the retract pair (`liftChannel_factors`, by
`rfl`), Born readout `Closed` with the classical step itself as the rate map —
and the wall where that ends is a Hadamard: `diag_not_closed_under_coherence`.
The classical tier ends exactly where coherence begins, credited to Zurek's
einselection: pointer views are the Closed ones, the predictability sieve is
closure-selection. The diagonal-lift row is no longer unimplemented.

**WHAT IS DERIVED, NOT PRIMITIVE.** A physically privileged scale is a view whose
square commutes (`Closed`); its dynamics is then DETERMINED (`rate_unique_on_range`);
closed fibers recurse — `(C, Views of C, h)` is the object again, with cost model
`Aggregation` (linear at `K ≤ 1`, measured 1.0012 on the engine); and closure is
NOT hereditary down the `Factors` order (`closure_not_hereditary`) — every tier
owes its own square. **And privilege is TWO-DIMENSIONAL** (the N4 death, cashed):
a view's measured openness factors into its chart's conditioning (the ceiling,
`sum_perturb_le` — explains divergence LEVELS) times the dynamics' organization
into that direction (explains divergence GROWTH: the twins' difference field
organized INTO momentum-x, residual above the random 95th percentile, and AWAY
from kinetic energy, below the 10th — Spearman of growth against ceiling-growth
+0.05, p = 0.70: the growth is not the chart). The privilege question is only
posable at matched conditioning; TIER-2 stakes both halves forward.

**KILL, separable.** Exhibit an in-scope invariant of views and dynamics that is
NOT a graded invariant of the square — one requiring comparison of something other
than what arrows merge, split, size, preserve, contract, price, or transport. That
kills the square as the maximal reading, leaving every row's theorem standing.

The stance's shapes are positions on this ladder. The published page's complexity
is a projection: many gradings, photographed one at a time, of one square.

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

## The object at depth — the four load-bearing consequences

*2026-08-26, revised the same day the fiber reading landed. The head section now
states the object once; these four are its consequences, each with status and
witness. In fiber terms: §1 is where fibers can be EMPTY, §2 is where loops act on
them, §3 is forward-invariant fibers recursing, §4 is fiber-splitting as the
detector of coupling. Readings are marked as readings.*

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

**CREDIT, and the nearest prior art is nearer than this document used to say.**
The presheaf-and-global-section reading is **Döring–Isham topos quantum theory**:
the spectral presheaf replaces the classical state space, and the Kochen–Specker
theorem IS the non-existence of a global section of it (Isham–Butterfield from the
late 1990s; Döring–Isham `quant-ph/0703062`). That is not adjacent to the paragraph
above — it is the paragraph above, and it precedes us by about twenty years. Also
Abramsky–Brandenburger 2011, with Abramsky–Mansfield–Barbosa's Čech invariant and
Atserias–Kolaitis (JACM 2025), as `Core/NonFactoring.lean` already carries.

Ours is the mechanization of four instances in one typed shape, `bell_ceiling` as
the witness that the cover is genuinely non-directed, and the recursion/closure
layer — which topos quantum theory does NOT supply. Full comparison, as complete
systems rather than ingredients: `OBJECT_PRIOR_ART.md`.

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
measured. **Limit, CORRECTED by the atlas** (`ATLAS_V2_RESULTS.md`): what forbids
view-curvature is the COMMON SOURCE, not fixedness of the fibration — mode-moving
re-roots over a fixed fibration already carry holonomy, and the mode-only sector
(where the presheaf → stack upgrade actually lives) links curvature and closure
with the OPPOSITE sign to the naive bridge: nonzero curvature forces every context
view Closed there. `loop_asymmetry` is a statement about sharing a source.

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
| the detector fires DIRECTIONALLY on hardware | **measured** — `ibm_marrakesh`, one-way CRX: forward 510× floor, reverse 6.25×, **88× asymmetry**, correct sign (`CLOSURE_PILOT_RESULTS.md`) |
| `independent_views_closed` holds under severe decoherence | **measured, and a confirmed advance prediction** — independent decay is a product map, so the theorem forbids a cross-residual however severe the decay; idle pair stays at floor out to 65.5 µs ≈ T1, ρ = −0.086, p = 0.92 (`TAU_SWEEP_RESULTS.md`). **Graded weak**: the prediction is near-tautological to a physicist, and it is scope-corroboration of the detector, not support for the ontology |
| the discriminating arms: reciprocal coupling | **measured, as predicted** — both marginals and the joint open (161× floor), so joint closure is NOT generic (`RESTORATION_RESULTS.md`) |
| joint-view restoration on hardware | **FAILED, as staked** — the transpiled conserving gate splits the n-fibers at 105× floor, ~50× the prep/readout baseline; "refinement restores closure" is damaged on this substrate, gate-dominated, follow-up prereg owed. The Lean 2×2 is untouched (theorems about the model map). Bonus: the n-fiber statistic detects T1 asymmetry the marginal statistics read as borderline |
| **the realized arrow is not the declared arrow** — the second-square fence, measured TWICE | **measured, and the diagnostic is now a theorem** — RESTORATION (conserving gate splits fibers at 105× while prep/readout reads 1.9×) and S1-reciprocal (first CRX 0.96, composite reverse 0.082 vs ideal 0.50) are two hardware instances of `claim_transport_does_not_grant_certificate`'s physical face: a certificate granted for the circuit-as-written does not transport to the channel-as-realized. The counts-level inference that localizes such failures — first leg certified + composite failed ⇒ second leg convicted — is `comp_failure_convicts_second_leg` (`Core/RerootTransport.lean`, `Quot.sound` only) |
| **calibrations are RENTED** | **reading, with a measured instance and a standing repair** — S1's one-way band missed at 18.0× against 20× frozen from a pilot epoch that measured 88×: the staked constant decayed between sessions, which is `unpaid_decays` (`Core/Maintenance.lean`) surfacing in metrology — an unmaintained calibration is a decaying entry, and a frozen band on it carries an unpaid rent assumption. Repair, binding on every successor hardware freeze: **bands anchor to a same-session in-job calibration arm** (the QPU-habit campaign's own rule, which the composition freeze failed to inherit). Kill: an in-job-anchored band that still drifts within a session |
| the closure defect predicts SURVIVAL on thermodynamic ground truth | **measured** — underdamped-erasure memory (Zenodo 13829200): witness at end-of-drive predicts survival beyond the bit, p=0.001, CIs ≫ 0, velocity-dominant 30–800× against a ruler gauged as biased the other way (`scratchpad/erasure/ERASURE_RESULTS.md`) |
| **optimization MANUFACTURES closure** | **measured at TWO levels** — survival-level: witness predictive power 0.07 → marginal → 0 across the protocol ladder; and within-erasure on the fresh chained streams: trained protocols leave ~250× less within-fiber structure (C1, `CHAINED_RESULTS.md`). The control-theory face of the design-knowing repair. Kill: a trained protocol whose witness-relevance does NOT fall |
| the rent law ΔW = ΔKE, and its trained exception | **measured, with TWO rule-6 forward confirmations** — staked on unseen chained streams and confirmed: ratio 1.36 (Basic, 12-kT range) and 0.607 (OptSingle) inside the staked [0.5, 2]; and the repetition-trained protocol, staked < 0.5, read **−0.081** — it actively EXPLOITS incoming kinetic energy. Kill for the law: a fresh substrate reading outside band with valid calibration |
| the slow mode | **C2's kill MIS-FIRED; question OPEN** — the end-bit target is dominated by the unshipped random target sequence (~1 bit exogenous), capping any witness gain at ~P(fail)×heterogeneity ≈ 0.003, the observed noise scale: the zero was the instrument's coverage, not the scene. Kill re-graded VOID-by-construction; the posable successor (KE-identity persistence across drives) RAN, post-hoc and labelled: per-chain KE identity reads +0.102±0.019 at one drive and ~0 beyond two — if the slow mode exists it is SHORT, and the statistic is now burned for forward staking on this data. C1's contraction reading (peak 0.2 ms, gone by 0.8 ms) stands |
| rent law transfers to a Wilson-loop holonomy | **measured**, 9.8 % — `HOLONOMY_RENT_RESULTS` |
| the mesh's ACTUAL tiers are Closed views of one another | **FIRST MEASURED INSTANCE (Ω-3), and the reading is SPLIT**: on macro-matched micro-different twins (789 equal-mass velocity swaps, cell-aggregate views of the Sandbox tier), the `Aggregation` budget HELD (coarse growth ratio 1.0001) — but exact closure fails as `interventional_iff_closed` predicts on a deterministic substrate, and the VIEW-PRIVILEGE claim is **FALSIFIED**: the declared momentum-x direction is the LEAST closed of all 67 measured views (growth 12.1×, above the random 95th percentile) while kinetic energy is among the MOST closed (0.83, contracting). Closure among conserved-quantity directions is heterogeneous, not a class privilege; candidate mechanism, staked for the follow-up: near-cancelling aggregates (momx scene scale 24× below momy's) make the coarse reading a small difference of large numbers (`OMEGA_KILL3_RESULTS.md`) |
| `K ≤ 1` on the real engine | **MEASURED TRUE** — median coarse divergence growth 1.0012 under an interventional probe (`COMPOSITION2_RESULTS.md` B4): the horizontal-scaling condition holds |
| **the TUPLE claim — the golden Ω** | **CONFIDENCE (Ω-KILL-4), after FOUR falsifications at tested scopes** — the season's arc: COMPOSITION-2, Ω-KILL (certify_at identity), Ω-KILL-2 (materialization dust, channel drift), Ω-KILL-3 (tier/view face) each converted to registry entries and scope corrections; then TIER-2/TIER-3 cut the interim laws to true scope and NABLA-1 paid the ∇ row; and Ω-KILL-4 froze all five faces on fresh data at learned scope — fifteen arms, fourteen posable, **fourteen of fourteen passed** (`OMEGA_KILL4_RESULTS.md`): the discriminator's fifth replication, the budget's seventh geometry, the light-cone's third, both fresh mixing protocols at every lag, the rent bracket at four never-measured doses on both qubits, the connection law on a fresh cadence. A MEASURED SYNTHESIS at tested scope — one engine, one QPU pair, one thermodynamic memory — never a proof about the world; the kills stay armed and the named next scopes (mixed-mass scenes, a second engine, the quantum rung) can still fire them. The tuple's laws have never lost an arm whose premises held |
| **the mixing clause, OUT-OF-SAMPLE on wild data** | **measured, live, and it PASSED close** — `defect_le_alpha_pow` staked at base lag 16 on the chained erasure streams (the lag-1 form REFUSED pre-freeze: alpha = 1 by disjoint support, a vacuous bound — D-BOUND-DOB's absorption on real data); held-out defects 0.094/0.059/0.029 against frozen bounds 0.420/0.181/0.043, the lag-64 margin only 2.4σ with the held-out defect 71% above train (real kernel drift). The μ-face's first out-of-sample instance (`OMEGA_KILL3_RESULTS.md`) |
| **the rent bracket on hardware** | **measured** — GCOST §4.2's mode-mixture bracket held at every dose on BOTH qubits (staked q95: p=16 read 0.689 inside [0.612, 0.719]) with clean cycle-memory (max |R4−R2| = 0.009) and a monotone ladder; the g-face's first hardware instance, on the substrate class that killed a decay shape once (`OMEGA_KILL3_RESULTS.md`) |
| **conditioning, and the organization of divergence** | **proved + TIER-2 adjudicated: the laws cut to their true scope in one round** — the conditioning level law (`sum_perturb_le`'s ceiling tracked by realized divergences) survived rule 6 TWICE at early time (f=300: 0.830, 0.880 vs staked 0.8) and **DIED as staked at late time** (f=1200: 0.27/0.33 on fresh geometries, vs 0.935 on the original — dead, kept, marked); the ke-protection claim **DIED at deep settling** (warm-up 150: 1.24 not below the ensemble p25 of 0.60); and **T-organize replicated, then TIER-3 killed its monotone dose law and found the true shape: a PEAK** — five adjudicated doses read 1.2 → 14.9 → 12.3 → 7.7 → 2.5 (warm-up 30 → 150): organization does not exist in fresh scenes (there EVERYTHING organizes, p75 = 17.7, and momx's specialness inverts), it emerges with settling, peaks near warm-up 60, and dies as the scene freezes — a phenomenon of the intermediate relaxation regime, interior interpolation confirmed (D3), monotone law dead-kept-marked; the levels miss is the SAME phenomenon (direction-specific organization must decorrelate levels from static ceilings), and the early level law is now 4-for-4 on rule-6 forward confirmations (0.830/0.880/0.990/0.858). The `Aggregation` budget has passed SIX geometries (0.9997–1.0044) and has never been breached on this engine (`OMEGA_TIER2_RESULTS.md`, `OMEGA_TIER3_RESULTS.md`) |
| the engine's classical/quantum relation IS the diagonal lift | **IMPLEMENTED IN LEAN** (`Core/DiagonalLift.lean`): the retract pair, the commuting lift square (`lift_commutes`), Born recovery as a `Closed` view with `h = T` (`diag_view_closed_of_classical`), and the wall (`diag_not_closed_under_coherence` — the fifth NonFactoring witness). The ENGINE dependency edge (Gauge tier carrying the sandbox as its diagonal, gated by the QASM conformance harness) is the spin-out's first milestone — implemented as mathematics, owed as engineering |
| a dynamical connection in the ENGINE (not a 6-state model) | **PAID (NABLA-1, CONFIDENCE)** — a mass-weighted connection transporting intensive fields around a half-cell chart plaquette; its holonomy DERIVED exact for uniform weights ((I+Δx/4)(I+Δy/4) − I) and MEASURED on the realized connection: Pearson 0.9999/0.9994, slope 1.012/1.006 on momx/ke over 311 interior cell-samples, uniform-weight null at 7.6e-19. Two arms REFUSED pre-freeze and recorded (mass contrast 1.1× gives the state-dependence no lever — the refusal's prediction confirmed by the ±0.27 wobble); a mixed-mass scene is the named successor (`NABLA1_RESULTS.md`) |

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
