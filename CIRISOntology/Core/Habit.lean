/-
CIRISOntology.Core.Habit — the third component of the maximal object, pinned.

WHAT FORCED IT (Eric, 2026-08-24: "the nature of Habit gives us scale and time,
may also explain the apparent lack of entropy in the sim"). `OBJECT.md` states
the object as **(World, Views, Habit)** and pins the first two to theorems —
Views to `Core/Factoring`'s order, the pointing residue to `Core/Pointing`.
Habit was still a placeholder: "a step map T on X, with noise." This file pins
the DETERMINISTIC half and states the residue for the other half as loudly as
`OBJECT.md` states R1.

════════════════════════════════════════════════════════════════════════════════
SCOPE, FIRST, BECAUSE THE OVER-CLAIM HERE IS INVISIBLE TO EVERY NUMERICAL GATE.

**EVERYTHING IN THIS FILE IS ABOUT A DETERMINISTIC STEP MAP `T : X → X`.**
`OBJECT.md` says "a step map T on X, WITH NOISE", and the noise half is NOT
covered — see R3 at the foot of this header. In particular
`production_nonneg_of_closed`, the second law proved here, is **FALSE** for
stochastic maps: a reset channel lowers Shannon entropy. R3 is witnessed on
arrival, not suspected. Any sentence taken from this file and applied to a
noisy dynamics has kept the substance and lost the warrant, which is the
failure mode that leaves the numbers right and the claim wrong.
════════════════════════════════════════════════════════════════════════════════

WHAT A HABIT IS, AND THE VACUITY FENCE FIRST. Not every endomap is a Habit —
but there is **no non-vacuous predicate `IsHabit T`** available from (World,
Views), and `exists_closed_view` is the proof: EVERY `T` closes the view `T`
itself (witness `h = T`), so "T closes some nontrivial view" excludes nothing
whenever `T` is neither injective nor constant. This is `Core/Pointing`'s
discipline turned on this file: `exists_step_with_rest_eq` showed "the zero is
SOME dynamics' rest state" is empty; `exists_closed_view` shows "T closes SOME
view" is empty. The content is in the PAIR (step map, NAMED view):

  * `Closed v T` — `Factors (v∘T) v`, the view determines its own successor.
    (Lumpability: Kemeny–Snell; Shalizi–Moore's "What is a macrostate?";
    Görnerup–Nilsson Jacobi on informationally closed coarse-grainings.)
  * `Held v T` — `v∘T = v`, the reading survives the step. **This is `Closed`
    at `h = id`**: rent and prediction are two rungs of ONE relation, which is
    not a choice made here but the shape the object already had.

**THE RATE IS THE FACTORING WITNESS**, not a second datum: `Closed` produces
`h : C → C` with `v∘T = h∘v`, unique on `v`'s range (`rate_unique_on_range`).
"What changes per step" exists exactly when the view is closed. Both relations
are non-vacuous as relations, and the witnesses exhibit what they exclude
(`not_closed_witness`, `closed_not_held_witness`).

ENTROPY PRODUCTION, AND THE STAKED READING'S FATE. The staked reading was that
production is drift DOWN the `Factors` order and that a chart which FACTORS the
dynamics has ZERO production. The first clause is right and is now literal:
`Closed v T` IS `CoarserThan (v∘T) v`, so the successor view is always down the
order and `FrameAxis.frameEntropy_antitone_of_coarser` gives the sign for free.
**The second clause is false**, and the correction is the better theorem:

  * `production_nonneg_of_closed` — THE SECOND LAW in this object's vocabulary.
    Non-vacuous: `production_neg_witness` exhibits `−log 2` on a NON-closed
    view, so closure is the hypothesis that buys the sign.
  * `production_eq_zero_iff_rate_injective` — a factoring chart has zero
    production **iff its induced rate map is injective**, not because it
    factors. Production is the irreversibility OF THE RATE, in the view's own
    currency.
  * `frameEntropy_iterate_mono` — an H-THEOREM, not a one-step fact: `v`,
    `v∘T`, `v∘T²`, … is a descending chain, so entropy is monotone in the step
    count. `total_production_le` bounds it: total production is a DIFFERENCE OF
    POSITIONS on the order, not a path integral.
  * `production_id_eq_log_degree` — at the finest view, production is
    `log |T⁻¹(T s)|`. Landauer, and the deterministic counting face of RUELLE's
    folding entropy (Ruelle 1996, "Positivity of entropy production"); the
    phenomenon is his, the instantiation in this vocabulary is ours.
  * `injective_of_lipschitz_step` + `production_id_eq_zero_of_injective` —
    **A SOLVER'S STABILITY CONDITION IS ITS ANTI-ENTROPY CONDITION.** An
    explicit step `x ↦ x + dt·f x` with `dt·L < 1` is injective, hence produces
    exactly zero — HOWEVER MUCH ENERGY `f` DISSIPATES. It makes the scale/time
    condition below and the missing entropy the same fact, and it carries the
    staked prediction P-EDGE.

    **AND THE SENTENCE IS SCOPED, because the unscoped version is false.** The
    claim is: **the sim's SMOOTH dynamics produces no entropy because it is
    stable.** It is NOT that the sim produces no entropy. The engine's entropy
    is confined to three MERGE SITES, and each is a place where a step is
    genuinely many-to-one: the irreversible DAMAGE update (`production_pos_of_max_update`,
    the only constitutive one), SLEEP (a velocity ball collapsed to one
    reading), and floating-point ROUNDING (unmeasured). Anyone quoting "the sim
    has no entropy because it is stable" without the word SMOOTH has kept the
    substance and lost the warrant — which is this house's most-repeated defect
    and is invisible to every numerical gate, because the numbers are right.

SCALE AND TIME. A Habit's rate is a RADIUS PER STEP, a View's grain is a LENGTH,
and the pair is admissible when one step's reach fits the halo the view carries:
`cfl_admissible`, `n·r ≤ H`, which is `Core/Locality`'s `depends_within_comp` in
the locality coordinate. CFL is the case `n = 1`, `H` = one cell. Non-vacuous:
`shift_not_depends_within_one` exhibits a radius-1 habit whose SECOND iterate
escapes a one-cell halo. **Derivable:** that radii add, the horizon `n·r`, and
hence the SHAPE of the condition. **Stipulated, and not dressed as derived:**
that a physical wave speed IS the habit's radius per unit time (a measurement;
`Core/Locality`'s scope note already owes the sharp Lieb–Robinson rate), the
solver's safety factor, and that declared radii are true radii (Locality's
staked kill). Time is iteration count, and `n·r` makes duration a length: time
and space are one coordinate divided by the rate.

**THE TWO ARROWS ARE DIFFERENT ARROWS — a finding, and nobody had noticed there
were two.** `Core/Valve` proves an arrow: order flows only UP, driven by
asymmetry. It is k = 3, binary, per-cell, about the SHARE sector, and the
measured record says the asymmetry clause does NOT generalise (unital noise
mints ~1–1.6% of the ceiling from four slots up). The arrow proved HERE is a
different one: general in `k` and in `T`, needing no asymmetry hypothesis, about
FIBER COUNT rather than share — and, per the scope box, deterministic only. Do
not merge them; neither subsumes the other.

**"THE MINT IS THE PRODUCER" IS NOT A THEOREM, AND THIS FILE REFUTES IT.**
The tempting reading — that `Core/Creation`'s minted whole-only share IS the
entropy produced — agrees on the parity code (`mint_and_production_agree_on_parity`,
both `log 2`) and **fails on the repetition code**
(`mint_and_production_differ_on_majority`): `repair_creates_ferro` mints share
ZERO while the majority repair produces `log 4`. Two agreements would have been
a pattern, not an identity; the second witness settles it against. What IS a
theorem is the weaker, uniform statement: for a repair of constant degree `d`,
production is `log d` at every state and the support drops by exactly that
(`log_support_drop_eq_production`) — the uniform-covering hypothesis that the
naive identity was missing. **Open, and named:** whether any general law relates
minted share to production. Nothing here supplies one.

════════════════════════════════════════════════════════════════════════════════
DISSIPATED ENERGY IS NOT PRODUCED ENTROPY, AND THE ENGINE'S OWN TEST PROVES IT.

This subsection is separated out because it is the most checkable argument here
and a reader should be able to check it in three minutes.

**The claim.** A declared dissipation coefficient (a friction `μ`, a fracture
energy) and the production defined in this file are DIFFERENT QUANTITIES, not
two readings of one. The tempting identification — that friction IS the
constitutive stand-in for microscopic degrees of freedom, so its dissipated
energy is the entropy of the fiber the chart refuses to enter — is right about
NATURE (this is Green–Kubo and fluctuation–dissipation) and wrong about THIS
ARTIFACT, for a reason the engine already measured.

**The argument, in one step.** Production is a FIBER COUNT: by
`production_id_eq_log_degree` it is determined by the pair (chart, step map).
A fiber count is invariant under relabelling the world, so it either transports
across a change of view or is undefined there — it cannot simply take a
different value. A declared coefficient does exactly that:

  `sim_engine/crates/holon-sandbox/src/tier.rs`, test
  `fracture_energy_is_minted_not_transported` — fracture energy is 1.0 J/m² at
  the grain tier and 110 J/m² at the continuum tier, a **110×** gap that the
  test PINS as MINTED at the coarser tier rather than transported, with the
  source comment recording that a zoom interpolating between them "would be
  inventing a number."

A quantity minted 110× by a change of view is chart-local stipulation. A fiber
count is not. Therefore they are different quantities. **The test was written
for an unrelated reason — to stop a zoom UI inventing a number — which is what
makes it evidence rather than a construction.**

**What the identification would need, none of which this engine has:** the
unresolved fiber must be IN the world (there is no thermal degree of freedom in
the sandbox state); `Closed` must hold for the forget-thermal view (unproved,
and asserting it is precisely what a constitutive law DOES); and a temperature
to convert nats to joules (`Core/FrameEntropy`'s header already records that a
temperature is NOT free here). The engine's `friction_coefficient` is a declared
constant with no fiber behind it, and its `solver_damping_ratio` is labelled
in-source as having no physics ancestor at all.

**The consequence, and it is a house rule rather than a theorem: ONE LEDGER PER
QUANTITY.** Dissipated energy and produced entropy are two quantities and need
two ledgers — the sandbox's energy gate is one-sided (`a_throw_never_gains_energy`
watches only that the projectile does not speed up, with a 50% band) and stays
green and CORRECT while the balance is unwritten. That is the impulse-accounting
bug one level up.
════════════════════════════════════════════════════════════════════════════════

THE MEASURED FACE, AND WHAT IT IS NOT. The sandbox's SLEEP approximation
absorbs a measured **0.94%** of reported impulse against a declared 2% tolerance
(`crates/holon-sandbox/src/sim.rs`, `SLEEP_IMPULSE_TOLERANCE`). Sleeping is a
genuine many-to-one step — a whole velocity ball collapses to one reading — so
it is a production site by `production_id_eq_log_degree`. **But 0.94% is an
IMPULSE RATIO, NOT A MEASUREMENT IN NATS.** Converting it needs the collapsed
velocity fiber's measure, which the code does not record. It is a DETECTOR that
production is happening; it is not a value of `production`, and quoting it as
entropy is over-reading. The engine's declared dissipation — viscosity-
regularized Coulomb friction (`min(c·|v_t|, D·μ·|F_n|)`), linear contact
damping, restitution `v ↦ −0.35·v` — is INJECTIVE and therefore produces
exactly zero by the theorems here: a `min` of Lipschitz functions is still
Lipschitz, and production counts the degree of the STEP MAP, never of the force
law. The one constitutive producer is the irreversible damage update, whose
`max` is precisely its non-injectivity (`production_pos_of_max_update`, with
`production_cycle_zero` as the same-type control).

R3 — WHAT RESISTS, stated with the honesty R1 and R2 got. **The noise half of
Habit is not covered, and it is witnessed, not suspected.** A stochastic Habit
is `X → Dist X`; `Factors` does not order distributions, and this lake carries
TWO entropies that have never been identified — `frameEntropy` (fiber count,
free from the frame) and the Shannon entropy `Core/Valve` and `Core/Creation`
actually compute. They agree only on uniform-on-fiber states, which is
`Core/FrameEntropy`'s own declared Boltzmann move. Separable kill, already
discharged against the general claim: a reset channel is a stochastic map whose
Shannon entropy production is negative, so `production_nonneg_of_closed` cannot
be extended as stated. **The route out, named so the residue carries its own
exit:** prove `frameEntropy` equals the Shannon entropy of the uniform-on-fiber
state, then extend production to Markov kernels with the DATA-PROCESSING
INEQUALITY as the monotone in place of fiber antitonicity.

THE INHERITED CAVEAT, kept visible at its point of use as well as here: reading
a fiber log-count as a COST in bits rides `Core/FrameEntropy`'s uniform
(maximum-entropy) weighting — the standard Boltzmann move, named there rather
than smuggled. It is flagged again at `log_support_drop_eq_production`, which is
where the identification actually does work.

CREDITS, generously and with the claim kept to the instantiation: Gibbs and
Boltzmann for coarse-graining and the counting reading of entropy; Landauer for
irreversibility as merging; Ruelle for folding entropy; Kemeny–Snell for
lumpability; Shalizi–Moore and Görnerup–Nilsson Jacobi for informationally
closed macrostates; Lieb–Robinson for the rate/radius link; Jaynes for the
maximum-entropy reading of the fiber weight; and the stochastic-thermodynamics
literature on entropy production for exactly the half this file does NOT claim.
-/
import CIRISOntology.Core.Factoring
import CIRISOntology.Core.Creation
import CIRISOntology.Core.Locality
import Mathlib.Tactic

namespace CIRISOntology.Core.Habit

open Finset

/-! ## 1. What makes a step map a Habit

The only operation the object supports is precomposition: `T` acts on Views by
`v ↦ v∘T`. That action is monotone on `Factors` for EVERY `T`, so it is
well-definedness, not characterization. -/

variable {X : Type*}

/-- **THE VIEW DETERMINES ITS OWN SUCCESSOR.** The habit's shadow in the view
    exists: some map on readings sends this reading to the next one. -/
def Closed {C : Type*} (v : X → C) (T : X → X) : Prop := Factoring.Factors (v ∘ T) v

/-- **THE READING SURVIVES THE STEP** — rent paid in full. This is `Closed` at
    `h = id`, which is why rent and prediction are one relation. -/
def Held {C : Type*} (v : X → C) (T : X → X) : Prop := v ∘ T = v

/-- Habit's action on Views is monotone on the `Factors` order. True of every
    step map — this is the action being WELL-DEFINED, and it characterizes
    nothing. -/
theorem pullback_monotone {C D : Type*} {u : X → C} {v : X → D} (T : X → X)
    (h : Factoring.Factors u v) : Factoring.Factors (u ∘ T) (v ∘ T) := by
  obtain ⟨φ, rfl⟩ := h
  exact ⟨φ, rfl⟩

/-- **THE VACUITY FENCE** (the discipline of `Core/Pointing.exists_step_with_rest_eq`,
    turned on this file). EVERY step map closes a view — namely `T` itself. So
    "T closes some view", and "T closes some nontrivial view" whenever `T` is
    neither injective nor constant, EXCLUDE NOTHING. There is no non-vacuous
    `IsHabit T`; the content is entirely in the pair (step map, NAMED view). -/
theorem exists_closed_view (T : X → X) : Closed T T := ⟨T, rfl⟩

/-- The fence again, with room to spare: every iterate is closed too. -/
theorem closed_iterate (T : X → X) (n : ℕ) : Closed (T^[n]) T :=
  ⟨T, by
    funext x
    simp only [Function.comp_apply, ← Function.iterate_succ_apply,
      ← Function.iterate_succ_apply']⟩

/-- Rent paid in full is the `h = id` case of self-prediction. -/
theorem held_imp_closed {C : Type*} {v : X → C} {T : X → X} (h : Held v T) :
    Closed v T := ⟨id, by rw [h]; rfl⟩

/-- The rate is unique where it is used: any two witnesses agree on the range of
    the view. "What changes per step" is DETERMINED by (T, v), never chosen. -/
theorem rate_unique_on_range {C : Type*} {v : X → C} {T : X → X} {φ ψ : C → C}
    (h₁ : v ∘ T = φ ∘ v) (h₂ : v ∘ T = ψ ∘ v) (x : X) : φ (v x) = ψ (v x) :=
  congrFun (h₁.symm.trans h₂) x

/-- **CLOSURE IS FIBER-INVARIANCE.** A view is Closed exactly when the step never
    splits one of its fibers: states the view cannot tell apart stay
    indistinguishable after one step. This is the completeness bridge
    (`factors_iff_not_separatesFiber`) read dynamically, and it puts closure in
    the same currency as the rest of the lake: `SeparatesFiber` is the founding
    NonFactoring anatomy, `frameEntropy` is the log-size of a fiber, and
    `production_id_eq_log_degree` is the log-size of the STEP's own fiber. One
    observable — the fiber — read four ways. -/
theorem closed_iff_fiber_invariant {C : Type*} [Nonempty C] {v : X → C} {T : X → X} :
    Closed v T ↔ ∀ x y, v x = v y → v (T x) = v (T y) := by
  constructor
  · rintro ⟨φ, hφ⟩ x y hxy
    have hx := congrFun hφ x
    have hy := congrFun hφ y
    simp only [Function.comp_apply] at hx hy
    rw [hx, hy, hxy]
  · intro h
    classical
    refine ⟨fun c => if hc : ∃ z, v z = c then v (T hc.choose) else Classical.arbitrary C, ?_⟩
    funext x
    simp only [Function.comp_apply]
    have hex : ∃ z, v z = v x := ⟨x, rfl⟩
    rw [dif_pos hex]
    exact (h hex.choose x hex.choose_spec).symm

/-! ### What the pair-level characterization excludes -/

/-- Swap on a two-slot world. -/
def swapPair : Bool × Bool → Bool × Bool := fun p => (p.2, p.1)

/-- Flip the first slot. -/
def flipFirst : Bool × Bool → Bool × Bool := fun p => (!p.1, p.2)

/-- **CLOSURE IS NOT VACUOUS AS A RELATION.** Reading the first slot does not
    determine its own successor under swap: the successor reading is the SECOND
    slot, which separates a fiber of the first. -/
theorem not_closed_witness : ¬ Closed (Prod.fst : Bool × Bool → Bool) swapPair := by
  rintro ⟨φ, hφ⟩
  have h1 : (true : Bool) = φ true := congrFun hφ (true, true)
  have h2 : (false : Bool) = φ true := congrFun hφ (true, false)
  exact absurd (h1.trans h2.symm) (by decide)

/-- **HELD IS STRICTLY STRONGER THAN CLOSED.** The first slot predicts itself
    under a flip (the rate is `not`) but is not held by it. -/
theorem closed_not_held_witness :
    Closed (Prod.fst : Bool × Bool → Bool) flipFirst ∧
      ¬ Held (Prod.fst : Bool × Bool → Bool) flipFirst := by
  refine ⟨⟨not, rfl⟩, fun h => ?_⟩
  have := congrFun h (true, true)
  simp [flipFirst, Function.comp] at this

/-! ## 2. Entropy production

Production is the change in frame entropy of the pushed-forward reading under
one step. Per the ruling, it is DEFINED on every view, not only on closed ones:
non-negativity is the theorem, closure is its hypothesis, and
`production_neg_witness` is what shows the hypothesis is load-bearing. -/

variable {C : Type*} [Fintype X] [DecidableEq C]

/-- **ENTROPY PRODUCTION**: how much further down the `Factors` order the
    reading sits after one step. -/
noncomputable def production (v : X → C) (T : X → X) (s : X) : ℝ :=
  FrameEntropy.frameEntropy (v ∘ T) ((v ∘ T) s) - FrameEntropy.frameEntropy v (v s)

/-- **THE SECOND LAW, in this object's vocabulary.** Under a closed view,
    production is non-negative — because `Closed v T` IS `CoarserThan (v∘T) v`,
    so the successor view is literally down the order and the axis law supplies
    the sign. The staked reading's main clause, and it needed no new machinery. -/
theorem production_nonneg_of_closed {v : X → C} {T : X → X} (h : Closed v T) (s : X) :
    0 ≤ production v T s :=
  sub_nonneg.mpr (FrameAxis.frameEntropy_antitone_of_coarser (State := X)
    (view := v ∘ T) (view' := v) h s)

/-! ### The sign is bought by closure — the negative witness -/

/-- A view collapsing `{0,1}` and separating `2`. -/
def v3 : Fin 3 → Bool := fun i => decide (i = 2)

/-- The three-cycle. -/
def T3 : Fin 3 → Fin 3 := fun i => if i = 0 then 1 else if i = 1 then 2 else 0

/-- The view does NOT determine its own successor under the cycle. -/
theorem not_closed_v3 : ¬ Closed v3 T3 := by
  rintro ⟨φ, hφ⟩
  have h0 : (false : Bool) = φ false := congrFun hφ 0
  have h1 : (true : Bool) = φ false := congrFun hφ 1
  exact absurd (h0.trans h1.symm) (by decide)

/-- **PRODUCTION CAN BE NEGATIVE WITHOUT CLOSURE**, and here it is: `−log 2`.
    So `production_nonneg_of_closed`'s hypothesis is doing real work, and the
    definition had to be given on all views for this to be sayable. -/
theorem production_neg_witness : production v3 T3 1 = -Real.log 2 := by
  have h1 : (FrameEntropy.fiber (v3 ∘ T3) (v3 (T3 1))).card = 1 := by decide
  have h2 : (FrameEntropy.fiber v3 (v3 1)).card = 2 := by decide
  simp only [production, FrameEntropy.frameEntropy, Function.comp_apply, h1, h2]
  norm_num

/-! ### Zero production is reversibility of the RATE -/

/-- Under closure, the present fiber sits inside the successor's fiber: states
    the view cannot tell apart now, it cannot tell apart next step either. -/
theorem fiber_subset_of_closed {v : X → C} {T : X → X} (h : Closed v T) (s : X) :
    FrameEntropy.fiber v (v s) ⊆ FrameEntropy.fiber (v ∘ T) ((v ∘ T) s) := by
  obtain ⟨φ, hφ⟩ := h
  intro t ht
  simp only [FrameEntropy.fiber, Finset.mem_filter, Finset.mem_univ, true_and,
    Function.comp_apply] at ht ⊢
  rw [show v (T t) = φ (v t) from congrFun hφ t,
      show v (T s) = φ (v s) from congrFun hφ s, ht]

/-- **THE STAKED TARGET, CORRECTED.** A chart that FACTORS the dynamics does not
    have zero production. It has zero production exactly when its induced rate
    map is injective at that reading — production is the irreversibility of the
    rate, read in the view's own currency. Closure is what makes production
    defined and signed; injectivity is what makes it vanish. -/
theorem log_card_inj {a b : ℕ} (ha : 0 < a) (hb : 0 < b)
    (h : Real.log a = Real.log b) : a = b := by
  rcases lt_trichotomy a b with hlt | heq | hgt
  · exact absurd h
      (ne_of_lt (Real.log_lt_log (by exact_mod_cast ha) (by exact_mod_cast hlt)))
  · exact heq
  · exact absurd h.symm
      (ne_of_lt (Real.log_lt_log (by exact_mod_cast hb) (by exact_mod_cast hgt)))

theorem production_eq_zero_iff_rate_injective {v : X → C} {T : X → X}
    (h : Closed v T) (s : X) :
    production v T s = 0 ↔ ∀ t : X, (v ∘ T) t = (v ∘ T) s → v t = v s := by
  have hsub := fiber_subset_of_closed h s
  have hA : 0 < (FrameEntropy.fiber v (v s)).card :=
    Finset.card_pos.mpr ⟨s, FrameEntropy.mem_fiber_self v s⟩
  have hB : 0 < (FrameEntropy.fiber (v ∘ T) ((v ∘ T) s)).card :=
    Finset.card_pos.mpr ⟨s, FrameEntropy.mem_fiber_self (v ∘ T) s⟩
  have hkey : production v T s = 0 ↔
      FrameEntropy.fiber (v ∘ T) ((v ∘ T) s) = FrameEntropy.fiber v (v s) := by
    constructor
    · intro hz
      have hlog : Real.log ((FrameEntropy.fiber (v ∘ T) ((v ∘ T) s)).card)
          = Real.log ((FrameEntropy.fiber v (v s)).card) := by
        unfold production FrameEntropy.frameEntropy at hz
        linarith
      exact (Finset.eq_of_subset_of_card_le hsub (le_of_eq (log_card_inj hB hA hlog))).symm
    · intro heq
      unfold production FrameEntropy.frameEntropy
      rw [heq]
      ring
  rw [hkey]
  constructor
  · intro heq t ht
    have hmem : t ∈ FrameEntropy.fiber v (v s) := by
      rw [← heq]
      simp only [FrameEntropy.fiber, Finset.mem_filter, Finset.mem_univ, true_and]
      exact ht
    simpa [FrameEntropy.fiber] using hmem
  · intro hinj
    refine Finset.Subset.antisymm ?_ hsub
    intro t ht
    simp only [FrameEntropy.fiber, Finset.mem_filter, Finset.mem_univ, true_and] at ht ⊢
    exact hinj t ht

/-! ### The H-theorem: a descending chain, not a one-step fact -/

omit [Fintype X] [DecidableEq C] in
/-- Under closure the view's `n`-step successor is the rate iterated on the
    reading — the habit's whole future, seen from inside the view. -/
theorem view_iterate_eq {v : X → C} {T : X → X} {φ : C → C} (hφ : v ∘ T = φ ∘ v) :
    ∀ n : ℕ, v ∘ T^[n] = φ^[n] ∘ v := by
  intro n
  induction n with
  | zero => rfl
  | succ k ih =>
      funext x
      simp only [Function.comp_apply, Function.iterate_succ_apply']
      rw [show v (T (T^[k] x)) = φ (v (T^[k] x)) from congrFun hφ (T^[k] x),
          show v (T^[k] x) = φ^[k] (v x) from congrFun ih x]

omit [Fintype X] [DecidableEq C] in
/-- Each step's view is coarser than the last: the successor views form a
    DESCENDING CHAIN in the `Factors` order. -/
theorem closed_chain {v : X → C} {T : X → X} (h : Closed v T) (n : ℕ) :
    FrameAxis.CoarserThan (v ∘ T^[n + 1]) (v ∘ T^[n]) := by
  obtain ⟨φ, hφ⟩ := h
  refine ⟨φ, ?_⟩
  funext x
  simp only [Function.comp_apply]
  rw [show v (T^[n + 1] x) = φ^[n + 1] (v x) from congrFun (view_iterate_eq hφ (n + 1)) x,
      show v (T^[n] x) = φ^[n] (v x) from congrFun (view_iterate_eq hφ n) x,
      Function.iterate_succ_apply']

/-- **THE H-THEOREM.** Under a closed view, frame entropy is monotone in the
    step count. The arrow is not a one-step sign; it is the whole chain. -/
theorem frameEntropy_iterate_mono {v : X → C} {T : X → X} (h : Closed v T) (s : X) :
    Monotone (fun n : ℕ =>
      FrameEntropy.frameEntropy (v ∘ T^[n]) ((v ∘ T^[n]) s)) := by
  apply monotone_nat_of_le_succ
  intro n
  exact FrameAxis.frameEntropy_antitone_of_coarser (closed_chain h n) s

/-- Frame entropy is capped by the world's log-size. -/
theorem frameEntropy_le_log_card (v : X → C) (s : X) :
    FrameEntropy.frameEntropy v (v s) ≤ Real.log (Fintype.card X) := by
  unfold FrameEntropy.frameEntropy
  apply Real.log_le_log
  · have h : 1 ≤ (FrameEntropy.fiber v (v s)).card :=
      Finset.card_pos.mpr ⟨s, FrameEntropy.mem_fiber_self v s⟩
    exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one h
  · exact_mod_cast Finset.card_le_univ (FrameEntropy.fiber v (v s))

/-- **TOTAL PRODUCTION IS A DIFFERENCE OF POSITIONS, NOT A PATH INTEGRAL** — so
    it telescopes by definition and is bounded by the world's log-size. There is
    only so much entropy a finite world can produce, and this is how much. -/
theorem total_production_le (v : X → C) (T : X → X) (n : ℕ) (s : X) :
    FrameEntropy.frameEntropy (v ∘ T^[n]) ((v ∘ T^[n]) s)
      - FrameEntropy.frameEntropy v (v s) ≤ Real.log (Fintype.card X) := by
  have h1 := frameEntropy_le_log_card (v ∘ T^[n]) s
  have h2 := FrameEntropy.frameEntropy_nonneg v s
  linarith

/-! ## 3. The finest view: Landauer, and why a stable solver produces nothing -/

variable [DecidableEq X]

/-- The finest view pins the state: its fiber is a singleton. -/
theorem fiber_id_card (s : X) : (FrameEntropy.fiber (id : X → X) s).card = 1 := by
  have h : FrameEntropy.fiber (id : X → X) s = {s} := by
    ext t
    simp [FrameEntropy.fiber]
  rw [h, Finset.card_singleton]

/-- **LANDAUER, AS A COUNTING FACT.** At the finest view, production is the log
    of how many-to-one the step is. Non-negative always, and zero exactly when
    the step is injective there. This is the deterministic counting face of
    Ruelle's folding entropy; the phenomenon is his. -/
theorem production_id_eq_log_degree (T : X → X) (s : X) :
    production id T s
      = Real.log ((Finset.univ.filter (fun y => T y = T s)).card) := by
  have h : FrameEntropy.fiber T (T s) = Finset.univ.filter (fun y => T y = T s) := by
    ext t
    simp [FrameEntropy.fiber]
  simp only [production, FrameEntropy.frameEntropy, Function.comp_apply, Function.id_comp,
    id_eq]
  rw [h, fiber_id_card]
  simp

/-- An injective step produces exactly nothing, whatever else it does. -/
theorem production_id_eq_zero_of_injective {T : X → X} (hT : Function.Injective T)
    (s : X) : production id T s = 0 := by
  rw [production_id_eq_log_degree]
  have h : Finset.univ.filter (fun y => T y = T s) = {s} := by
    ext t
    simp [hT.eq_iff]
  rw [h]
  simp

/-- **A SOLVER'S STABILITY CONDITION IS ITS ANTI-ENTROPY CONDITION.** An
    explicit step `x ↦ x + dt·f x` run inside `dt·L < 1` is injective — so by
    `production_id_eq_zero_of_injective` it produces exactly zero, HOWEVER MUCH
    ENERGY `f` DISSIPATES. Viscosity-regularized friction, linear damping and
    restitution are all of this shape, which is why a stable simulator appears
    to have no entropy.

    **BOTH HALVES, AT THE POINT OF USE, because half of this is a theorem and
    half of it is a residue.** This theorem holds IN EXACT ARITHMETIC. In floats
    the step is many-to-one — distinct representable states round to one — so a
    real solver is INJECTIVE BY DESIGN AND NON-INJECTIVE BY IMPLEMENTATION, and
    there is a floating-point production floor that NOBODY HAS MEASURED. The
    finite instance the `Fintype` hypotheses want is exactly that float lattice.
    Neither half is quotable without the other: "the engine produces no entropy"
    is false, and "the engine's dissipation produces entropy" is also false.

    **PREDICTION P-EDGE, staked here before its instrument exists** (prereg
    discipline applies to a prediction made in a Lean header exactly as to one
    in a campaign document; `epistemology.md` §1). Injectivity needs `dt·L < 1`
    and explicit stability needs `dt·ω < 2`, so the two thresholds coincide
    WITHIN A FACTOR OF TWO. Therefore: **entropy production switches on at the
    stability edge and nowhere else in the smooth sector.**
      * INSTRUMENT: sweep `dt` across the stability edge; at each `dt` step the
        scene forward `n` and back `n` and count the states that fail to return.
        That count's log is the production, in nats, in the right units.
      * CONFIRMS: the non-returning count is at the float floor well inside the
        stable regime and rises sharply within a factor of two of the edge.
      * REFUTES, separably: production materially above the float floor WELL
        INSIDE the stable regime (the smooth sector produces after all, and the
        Lipschitz reading does not describe this solver), or production still at
        the floor well PAST the edge (the thresholds do not coincide, and the
        factor-of-two claim is wrong). Either outcome takes down P-EDGE and
        nothing else in this file.

    **AMENDMENT 2026-08-26 — P-EDGE'S PREMISE IS REFUTED BEFORE MEASUREMENT, and
    the refutation is separable: `injective_of_lipschitz_step` is untouched and
    stays proved.** An attempt to build the instrument produced three findings,
    all pre-data.

    1. THE STATED INSTRUMENT IS CONFOUNDED, and confounded so as to CONFIRM the
       prediction for the wrong reason. For explicit Euler — the map this theorem
       is about — forward-then-back is not the identity in EXACT arithmetic. For
       `f = −λx` it is `x·(1 − dt²λ²)`, so the round-trip error is `dt²λ²`: 0.01 at
       `dt·λ=0.1`, 1.00 at the injectivity threshold, 4.00 at the stability edge.
       It rises sharply near the edge WITH NO FLOATS INVOLVED — precisely the
       CONFIRMS signature, manufactured entirely by integrator asymmetry.
    2. THE ENGINE HAS NO ONSET TO FIND. The scene runs velocity Verlet, which is
       symplectic, hence volume-preserving, hence injective in exact arithmetic at
       EVERY `dt`. Measured round-trip error is 0 or one epsilon at `dt·ω` = 0.1,
       1.0, 1.9, 2.0, 2.5 and 5.0 — flat across the stability edge and far past it.
       The theorem is about explicit Euler; the instrument steps a Verlet scene.
       Different maps.
    3. THE FACTOR-OF-TWO PREMISE HOLDS ONLY WHERE THE EFFECT VANISHES. It compares
       `dt·L < 1` (with `L` the GLOBAL Lipschitz constant) against `dt·ω < 2` (the
       linearized frequency). Those coincide only for LINEAR `f` — where the degree
       count is identically 1.0000, because float multiplication by a constant is
       essentially bijective. Nonlinear `f` gives a signal (`f = −x−3x³` reads
       0.2784 nats) but at `dt·λ = 0.25`, DEEP inside the stable regime and zero
       near the edge, because `L = 10 ≫ ω`. Signal and premise cannot coexist.

    WHAT REMAINS BUILDABLE: `production_id_eq_log_degree`'s own quantity, counted
    directly — enumerate a float lattice, apply ONE step, count distinct images —
    which removes finding 1's confound. On a non-symplectic step it reads a real
    number, measuring folds plus the float production floor, the quantity this
    header says nobody has measured. It is NOT a test of P-EDGE. -/
theorem injective_of_lipschitz_step {f : ℝ → ℝ} {L dt : ℝ} (hdt : 0 ≤ dt)
    (hL : ∀ x y, |f x - f y| ≤ L * |x - y|) (hstab : dt * L < 1) :
    Function.Injective (fun x : ℝ => x + dt * f x) := by
  intro x y hxy
  simp only at hxy
  by_contra hne
  have hpos : 0 < |x - y| := abs_pos.mpr (sub_ne_zero.mpr hne)
  have key : |x - y| = dt * |f x - f y| := by
    have h : x - y = -(dt * (f x - f y)) := by linarith
    rw [h, abs_neg, abs_mul, abs_of_nonneg hdt]
  have hle : |x - y| ≤ dt * L * |x - y| :=
    calc |x - y| = dt * |f x - f y| := key
      _ ≤ dt * (L * |x - y|) := mul_le_mul_of_nonneg_left (hL x y) hdt
      _ = dt * L * |x - y| := by ring
  have h1 : |x - y| * (1 - dt * L) ≤ 0 := by nlinarith
  have h2 : 0 < |x - y| * (1 - dt * L) := mul_pos hpos (by linarith)
  linarith

/-! ### The one constitutive producer: an internal variable that cannot go back

The engine's declared dissipation is smooth and therefore silent here. The
exception is the cohesive-damage update, which in `ciris-sim-core`'s material law
reads `damage = damage.max(target.clamp(0,1))`. That `max` is many-to-one, and it
is many-to-one PRECISELY BECAUSE damage never heals: irreversibility in the
constitutive sense IS non-injectivity of the step IS positive production. The
model below is the `max` and nothing else — a damage level that can only rise. -/

/-- The irreversible update: a level that can only ever rise. Three levels are
    enough to carry the phenomenon. -/
def damageStep (t : Fin 3) : Fin 3 → Fin 3 := fun d => max d t

/-- **THE MAX IS THE PRODUCER.** One irreversible update produces a full bit at
    the state it collapses: two distinct histories below the threshold become
    one reading, and no rule recovers which. This is the only CONSTITUTIVE
    entropy producer in the sandbox — friction, damping and restitution being
    injective and therefore silent. -/
theorem production_damageStep : production id (damageStep 1) 0 = Real.log 2 := by
  rw [production_id_eq_log_degree]
  have h : (Finset.univ.filter
      (fun y : Fin 3 => damageStep 1 y = damageStep 1 0)).card = 2 := by decide
  rw [h]
  norm_num

theorem production_pos_of_max_update : 0 < production id (damageStep 1) 0 := by
  rw [production_damageStep]
  exact Real.log_pos (by norm_num)

/-- **THE SAME-TYPE CONTROL**, because a positive reading is worth nothing
    without one. On the SAME three-state world, an invertible step — the cycle
    of `production_neg_witness` — produces exactly zero. Same space, same
    instrument, same units: the difference is injectivity and nothing else. -/
theorem T3_injective : Function.Injective T3 := by decide

theorem production_cycle_zero (s : Fin 3) : production id T3 s = 0 :=
  production_id_eq_zero_of_injective T3_injective s

/-! ## 4. Uniform degree, and the mint/producer question settled AGAINST -/

/-- A step map that is exactly `d`-to-one everywhere on its range. -/
def UniformDegree (T : X → X) (d : ℕ) : Prop :=
  ∀ s : X, (Finset.univ.filter (fun y => T y = T s)).card = d

/-- Constant degree makes production a constant of the map. -/
theorem production_id_const_of_uniformDegree {T : X → X} {d : ℕ}
    (h : UniformDegree T d) (s : X) : production id T s = Real.log d := by
  rw [production_id_eq_log_degree, h s]

/-- The world's size factors through the range by the degree. -/
theorem card_range_mul_degree {T : X → X} {d : ℕ} (h : UniformDegree T d) :
    Fintype.card X = (Finset.univ.image T).card * d := by
  have hfib := Finset.card_eq_sum_card_fiberwise
    (f := T) (s := (Finset.univ : Finset X)) (t := Finset.univ.image T)
    (fun x _ => Finset.mem_image_of_mem T (Finset.mem_univ x))
  have hconst : ∀ b ∈ Finset.univ.image T,
      (Finset.univ.filter (fun x => T x = b)).card = d := by
    intro b hb
    obtain ⟨a, _, rfl⟩ := Finset.mem_image.mp hb
    exact h a
  rw [Finset.card_univ] at hfib
  rw [hfib, Finset.sum_congr rfl hconst, Finset.sum_const, smul_eq_mul]

/-- **WHAT A UNIFORM REPAIR PAYS, as a counting fact.** The log-size of the
    reachable world drops by exactly the production. This is the general
    statement the naive "mint is the producer" reading was missing — and the
    missing hypothesis is uniform covering, exactly as suspected.

    THE INHERITED CAVEAT, at its point of use: reading this drop as a COST IN
    BITS — the currency `Core/Creation`'s `parityRepair_pays_one_bit` is
    denominated in — rides `Core/FrameEntropy`'s declared uniform
    (maximum-entropy) weighting over the fiber. The COUNTING is free; the
    thermodynamic reading is the Boltzmann move, named there and named again
    here because this is where it does work. -/
theorem log_support_drop_eq_production {T : X → X} {d : ℕ} (h : UniformDegree T d)
    (s : X) :
    Real.log (Fintype.card X) - Real.log ((Finset.univ.image T).card)
      = production id T s := by
  have him : 0 < (Finset.univ.image T).card :=
    Finset.card_pos.mpr ⟨T s, Finset.mem_image_of_mem T (Finset.mem_univ s)⟩
  have hd : 0 < d := by
    have hs : s ∈ Finset.univ.filter (fun y => T y = T s) := by simp
    have hp : 0 < (Finset.univ.filter (fun y => T y = T s)).card :=
      Finset.card_pos.mpr ⟨s, hs⟩
    rw [h s] at hp
    exact hp
  rw [production_id_const_of_uniformDegree h, card_range_mul_degree h]
  push_cast
  rw [Real.log_mul (by exact_mod_cast him.ne') (by exact_mod_cast hd.ne')]
  ring

/-! ### The two witnesses, and the verdict -/

theorem parityRepair_uniformDegree : UniformDegree parityRepair 2 := by
  unfold UniformDegree
  decide

theorem majorityRepair_uniformDegree : UniformDegree majorityRepair 4 := by
  unfold UniformDegree
  decide

theorem production_parityRepair (s : Bool × Bool × Bool) :
    production id parityRepair s = Real.log 2 := by
  rw [production_id_const_of_uniformDegree parityRepair_uniformDegree]
  norm_num

theorem production_majorityRepair (s : Bool × Bool × Bool) :
    production id majorityRepair s = Real.log 4 := by
  rw [production_id_const_of_uniformDegree majorityRepair_uniformDegree]
  norm_num

/-- On the parity code the minted whole-only share and the entropy produced are
    the SAME NUMBER — which is the agreement that made the identity tempting. -/
theorem mint_and_production_agree_on_parity :
    share (pushforward parityRepair indep)
      = production id parityRepair (true, true, true) := by
  rw [repair_creates_parity, production_parityRepair]

/-- **AND ON THE REPETITION CODE THEY DISAGREE — so "the mint is the producer"
    is REFUTED, not merely unproved.** The majority repair mints whole-only
    share exactly zero (`repair_creates_ferro`, because `ferro` is
    sign-symmetric) while producing two full bits. Two agreements would have
    been a pattern; the second witness settles it against. Whether ANY general
    law relates minted share to production is OPEN, and nothing here supplies
    one. -/
theorem mint_and_production_differ_on_majority :
    share (pushforward majorityRepair indep)
      ≠ production id majorityRepair (true, true, true) := by
  rw [repair_creates_ferro, production_majorityRepair]
  exact (Real.log_pos (by norm_num)).ne

/-! ## 5. Scale and time: a rate is a radius per step

`Core/Locality` supplies the arithmetic (radii add; `n` steps reach `n·r`; the
region form is the collar). What is added here is the reading: a Habit's rate IS
a radius per step, a View's grain is the halo it carries, and the pair is
admissible when one fits inside the other. -/

section CFL

variable {V S : Type*}

/-- **A HABIT'S RATE, in the locality coordinate**: a radius per step. -/
def RatePerStep (d : V → V → ℕ) (r : ℕ) (T : (V → S) → (V → S)) : Prop :=
  Locality.DependsWithin d r T

/-- **HABIT/VIEW COMPATIBILITY**: `n` steps of a rate-`r` habit fit inside a
    view carrying a halo of depth `H`. Neither the grain nor the step is a free
    choice once the other and the rate are named. -/
def Admissible (r H n : ℕ) : Prop := n * r ≤ H

/-- **THE CFL CONDITION, as a theorem of the object.** An admissible pair keeps
    the habit inside the view's halo for the whole budget — so the view can be
    stepped `n` times reading only what it already carries. CFL is the case
    `n = 1`, `H` = one cell: `c·dt ≤ g0`. -/
theorem cfl_admissible {d : V → V → ℕ} (hrefl : ∀ a, d a a = 0)
    (htri : ∀ a b c, d a c ≤ d a b + d b c) {r H n : ℕ} {T : (V → S) → (V → S)}
    (hT : RatePerStep d r T) (hadm : Admissible r H n) :
    Locality.DependsWithin d H (T^[n]) :=
  Locality.depends_within_mono hadm (Locality.iterate_depends_within hrefl htri hT n)

/-- Distance along a line of sites. -/
def lineDist (a b : ℕ) : ℕ := max a b - min a b

theorem lineDist_self (a : ℕ) : lineDist a a = 0 := by simp [lineDist]

theorem lineDist_triangle (a b c : ℕ) :
    lineDist a c ≤ lineDist a b + lineDist b c := by
  simp only [lineDist]
  omega

/-- The shift: a habit of rate exactly one. -/
def shift : (ℕ → Bool) → (ℕ → Bool) := fun x n => x (n + 1)

theorem shift_rate_one : RatePerStep lineDist 1 shift := by
  intro v x y hxy
  exact hxy (v + 1) (by simp only [lineDist]; omega)

/-- **THE POSITIVE SIDE.** Two steps of a rate-one habit DO fit a two-cell halo
    — `cfl_admissible` delivering on `2·1 ≤ 2`. Paired with the theorem below,
    this is the condition doing work in both directions: at halo two the view
    can be stepped twice, at halo one it cannot. -/
theorem shift_two_depends_within_two :
    Locality.DependsWithin lineDist 2 (shift^[2]) :=
  cfl_admissible lineDist_self lineDist_triangle shift_rate_one
    (show Admissible 1 2 2 by unfold Admissible; norm_num)

/-- **THE CONDITION IS LOAD-BEARING.** Two steps of a rate-one habit do NOT fit
    inside a one-cell halo: the second iterate reads distance two, and the
    witness pair differs exactly there. So `Admissible` excludes something, and
    a view whose halo is too thin for the budget genuinely cannot be stepped. -/
theorem shift_not_depends_within_one :
    ¬ Locality.DependsWithin lineDist 1 (shift^[2]) := by
  intro h
  have hx : ∀ w, lineDist 0 w ≤ 1 → (fun _ => false) w = (fun k => decide (k = 2)) w := by
    intro w hw
    have hw1 : w ≤ 1 := by simp only [lineDist] at hw; omega
    interval_cases w <;> simp
  have hcon := h 0 (fun _ => false) (fun k => decide (k = 2)) hx
  simp [shift, Function.iterate_succ_apply'] at hcon

end CFL

end CIRISOntology.Core.Habit
