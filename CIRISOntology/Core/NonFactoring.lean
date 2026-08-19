/-
CIRISOntology.Core.NonFactoring — one shape, three published instances.

This repository already carries three results that read like the same sentence in
three vocabularies:

  * `Core.Third` — `pairwise_blind_to_parity` / `third_sees_parity`: two states
    present identical pair data and differ in total dependence.
  * `Core.FlavorBridge` — `cp_phase_invisible_to_pairs`: every member of the CP
    family presents identical pair data, and the members differ in whole-only
    share.
  * `Core.WrongKind` — `repairable_does_not_factor`: two (artifact, frame) pairs
    present identical artifact data and differ in repairability.

"Read like the same sentence" is a literary observation. This file makes it a
typed one, and nothing more. `NonFactoring` names the shape — a WITNESS PAIR:
two wholes agreeing under every partial view yet differing in the quantity — and
the three theorems below exhibit each published result as an instance of it, all
three derived from the published witnesses rather than re-argued.

WHAT THIS BUYS, exactly. `not_computable_of_nonFactoring` is the one general
consequence: a quantity with a witness pair is not a function of the joint view,
by the domain argument of `Core.Coordination` (`not_computable_from`) — the same
two-line fact about function domains, now instantiated a third and fourth time
rather than a second. So the corollaries at the end of the file are free: total
dependence is not computable from the three pair marginals, the whole-only share
is not computable from them either, and repairability is not computable from any
reading of the artifact alone.

WHAT THIS DOES NOT BUY, and the header says it here as well as at the foot: a
shared shape is not a shared quantity. See the closing note.

SCOPE. Every instance below is the instance its source file already scoped.
Instance 2 is a MODEL family wearing the Jarlskog invariant's shape and is not
flavour physics (`Core.FlavorBridge`'s header, points 1–3). Instance 3 is about
the SHAPE of the taxonomy, not its truth (`Core.WrongKind`'s header). This file
inherits both scopes and widens neither.
-/
import CIRISOntology.Core.Third
import CIRISOntology.Core.FlavorBridge
import CIRISOntology.Core.WrongKind

namespace CIRISOntology.Core

/-! ### The shape -/

/-- **THE SHAPE, in witness-pair form.** A quantity `q` FAILS TO FACTOR through a
    family of partial views `view` when two wholes agree under every one of those
    views and still differ in `q`.

    The views are typed per index (`View : ι → Type*`), because the three
    instances index different things: the three pair marginals of a three-slot
    state in the first two, and every artifact-only reading in the third.

    This is `Core.Coordination`'s `SeparatesFiber` with the summary presented as
    an indexed family instead of a single map — the same content, in the form all
    three published results already have. -/
def NonFactoring {ι : Type*} {State : Type*} {View : ι → Type*} {Datum : Type*}
    (view : (i : ι) → State → View i) (q : State → Datum) : Prop :=
  ∃ x y : State, (∀ i, view i x = view i y) ∧ q x ≠ q y

/-- The witness-pair form is the fiber-separating form: agreeing under every view
    is agreeing under the joint view. -/
theorem separatesFiber_of_nonFactoring {ι State Datum : Type*} {View : ι → Type*}
    {view : (i : ι) → State → View i} {q : State → Datum}
    (h : NonFactoring view q) :
    SeparatesFiber (fun x i => view i x) q := by
  obtain ⟨x, y, hv, hq⟩ := h
  exact ⟨x, y, funext hv, hq⟩

/-- **THE ONE GENERAL CONSEQUENCE.** A quantity with a witness pair is not
    computable from the views: there is no rule whatever — however clever,
    however nonlinear — that takes the whole family of partial readings as its
    input and returns the quantity.

    This is `Core.Coordination`'s `not_computable_from`, reused verbatim. The
    domain argument is doing all the work; `NonFactoring` only puts the three
    published results in the shape that argument accepts. -/
theorem not_computable_of_nonFactoring {ι State Datum : Type*} {View : ι → Type*}
    (view : (i : ι) → State → View i) (q : State → Datum)
    (h : NonFactoring view q) :
    ¬ ∃ g : ((i : ι) → View i) → Datum, ∀ x, q x = g (fun i => view i x) :=
  not_computable_from (fun x i => view i x) q (separatesFiber_of_nonFactoring h)

/-! ### The pair views, as one indexed family

Instances 1 and 2 share a view family literally, not by analogy: the same three
two-slot marginals of `Core.Share`, presented as a map out of `Fin 3`. -/

/-- The three two-slot readings of a three-slot state, as ONE indexed family of
    partial views. Same objects as `Core.Share`'s `marg₁₂ / marg₁₃ / marg₂₃`;
    only the packaging is new. -/
noncomputable def pairView : Fin 3 → (Bool × Bool × Bool → ℝ) → (Bool × Bool → ℝ)
  | 0 => marg₁₂
  | 1 => marg₁₃
  | 2 => marg₂₃

/-- `SamePairs` says exactly that the indexed family cannot tell two states
    apart. The repackaging is faithful, and this is the proof of it. -/
theorem pairView_of_samePairs {p q : Bool × Bool × Bool → ℝ} (h : SamePairs p q)
    (i : Fin 3) : pairView i p = pairView i q := by
  obtain ⟨h12, h13, h23⟩ := h
  fin_cases i
  · exact h12.symm
  · exact h13.symm
  · exact h23.symm

/-! ### Instance 1 — the founding state (`Core.Third`) -/

/-- **INSTANCE 1: PARITY.** Total dependence does not factor through the pair
    views. The witness pair is the repository's founding one, taken from the
    published theorems and not rebuilt: `parity` and `indep` carry identical
    two-slot data (`indep_samePairs`, which is `parity_pair_independent_*`
    reused), and their total dependence is `log 2` against `0`
    (`third_sees_parity`, `S_total_indep`).

    `pairwise_blind_to_parity` is the same fact read at the instrument; this is
    it read at the pair marginals. The two are not independent: the correlation
    matrix factors through the pair marginals (every off-diagonal entry is a sum
    against one of them), so the marginal-level statement implies the
    correlation-level one — that implication is stated in prose here and is NOT
    machine-checked in this file. -/
theorem nonfactoring_parity : NonFactoring pairView (S_total : (Bool × Bool × Bool → ℝ) → ℝ) :=
  ⟨parity, indep, pairView_of_samePairs indep_samePairs, by
    rw [third_sees_parity, S_total_indep]
    exact ne_of_gt (Real.log_pos (by norm_num))⟩

/-! ### Instance 2 — the CP family (`Core.FlavorBridge`) -/

/-- **INSTANCE 2, IN GENERAL FORM.** Any two members of the CP family with
    different whole-only share are a witness pair for `share` against the pair
    views: `cp_phase_invisible_to_pairs` supplies the agreement at every pair,
    and `share_cpState`'s closed form supplies the disagreement. -/
theorem nonfactoring_cpState {J J' : ℝ} (hJ : |J| ≤ 1) (hJ' : |J'| ≤ 1)
    (hne : cpShare J ≠ cpShare J') :
    NonFactoring pairView (share : (Bool × Bool × Bool → ℝ) → ℝ) :=
  ⟨cpState J, cpState J',
   pairView_of_samePairs (cp_phase_invisible_to_pairs J J'), by
    rw [share_cpState hJ, share_cpState hJ']
    exact hne⟩

/-- **INSTANCE 2: THE CP PHASE.** The whole-only share does not factor through
    the pair views, exhibited on a witness pair drawn from the INTERIOR of the CP
    family — a half-strength phase against the CP-even member — so that the
    instance is a statement about the family rather than about `parity` wearing a
    new name. (It is a line through `parity`: `cpState_neg_one`. The interior
    witnesses are chosen so that this instance does not lean on that.)

    The disagreement is `share_pos_of_cp_odd` against `share_zero_of_cp_even`,
    both published: a nonzero Jarlskog coordinate buys strictly positive share,
    the CP-even member has exactly none, and no two-slot reading of any kind
    separates them. MODEL ONLY — see the file header and
    `Core.FlavorBridge`'s scope section. -/
theorem nonfactoring_cp_phase :
    NonFactoring pairView (share : (Bool × Bool × Bool → ℝ) → ℝ) :=
  ⟨cpState (1/2), cpState 0,
   pairView_of_samePairs (cp_phase_invisible_to_pairs (1/2) 0), by
    rw [share_zero_of_cp_even (rfl : (0:ℝ) = 0)]
    exact ne_of_gt (share_pos_of_cp_odd (by rw [abs_of_nonneg] <;> norm_num)
      (by norm_num))⟩

/-! ### Instance 3 — the record relation (`Core.WrongKind`)

The third instance changes vocabulary completely and keeps the shape. The whole
is an (artifact, frame) pair; the partial views are the ARTIFACT-READS — every
property of the artifact alone, which is what the other eleven kinds are allowed
to consult; the quantity is repairability. -/

/-- The whole, in the taxonomy's vocabulary: a block together with the frame it
    is classified against. `Core.WrongKind`'s `classify(artifact, frame)`, as a
    single object so it can play the role of `State`. -/
abbrev Classified := String × Frame

/-- THE PARTIAL VIEWS, indexed by every artifact-only reading there is. This is
    the family `Core.WrongKind`'s `frameInvariant_of_artifact_only` describes:
    the readings available to a classification that is a property of the block.
    The index type is the function space itself, so the family is exhaustive by
    construction — no artifact-only reading is left out of it. -/
def artifactView : (String → Prop) → Classified → Prop :=
  fun g x => g x.1

/-- The quantity: whether what happened can still be established from what
    survives. `Core.WrongKind`'s `Repairable`, with its two arguments packed. -/
def repairableOf : Classified → Prop := fun x => Repairable x.1 x.2

/-- **INSTANCE 3: THE RECORD.** Repairability does not factor through the
    artifact-reads. The witness pair is `repairability_not_intrinsic`'s own — one
    fact and two corpora classifying it oppositely — repackaged: the two wholes
    share their artifact outright, so they agree under EVERY artifact-only
    reading trivially, and they differ in the quantity because the frame moved.

    This is `repairable_does_not_factor` in the shape of the other two. Note
    which published theorem is reused: `repairable_does_not_factor` is itself a
    `¬ ∃` conclusion and carries no witness pair to convert, so the derivation
    goes one step upstream to `repairability_not_intrinsic`, the exhibited
    witness both statements rest on. -/
theorem nonfactoring_record : NonFactoring artifactView repairableOf := by
  obtain ⟨fact, c₁, c₂, h₁, h₂⟩ := repairability_not_intrinsic
  refine ⟨(fact, c₁), (fact, c₂), fun _ => rfl, fun h => ?_⟩
  have h' : Repairable fact c₁ = Repairable fact c₂ := h
  exact h₂ (h' ▸ h₁)

/-! ### The three corollaries, free from the one general consequence -/

/-- Total dependence is not computable from the three pair marginals. The
    marginal-level strengthening of `total_not_computable_from_corr`, which says
    the same at the correlation matrix. -/
theorem total_not_computable_from_pairs :
    ¬ ∃ g : (Fin 3 → (Bool × Bool → ℝ)) → ℝ,
        ∀ p : Bool × Bool × Bool → ℝ, S_total p = g (fun i => pairView i p) :=
  not_computable_of_nonFactoring pairView S_total nonfactoring_parity

/-- The whole-only share is not computable from the three pair marginals either
    — which is the sentence `share`'s own definition makes it easy to assume
    away, since the share is DEFINED against the pair data. It is defined against
    the pair data and the state; the pair data alone does not determine it. -/
theorem share_not_computable_from_pairs :
    ¬ ∃ g : (Fin 3 → (Bool × Bool → ℝ)) → ℝ,
        ∀ p : Bool × Bool × Bool → ℝ, share p = g (fun i => pairView i p) :=
  not_computable_of_nonFactoring pairView share nonfactoring_cp_phase

/-- Repairability is not computable from the artifact-reads: no assignment of a
    verdict from artifact-only readings is correct at every frame.

    The COUNTERPART of `repairable_does_not_factor` through the general
    consequence, and not literally that statement: the summary here is the
    profile of ALL artifact-only readings, which is at least as informative as
    the artifact itself, so this is the non-computability statement at a richer
    input. The published `↔`-form is proved where it lives and is not
    re-derived. -/
theorem record_not_computable_from_artifact_reads :
    ¬ ∃ g : ((String → Prop) → Prop) → Prop,
        ∀ x : Classified, repairableOf x = g (fun r => artifactView r x) :=
  not_computable_of_nonFactoring artifactView repairableOf nonfactoring_record

/-! ### What this file establishes, and what it does not -/

/-- **THE HONEST FOOT OF THE FILE.**

    PROVED ABOVE, and it is the whole of what is proved: the three published
    results — `pairwise_blind_to_parity`/`third_sees_parity`,
    `cp_phase_invisible_to_pairs`, `repairable_does_not_factor` — are instances
    of ONE typed shape, `NonFactoring`, and each inherits the domain argument's
    conclusion from it. Shared shape, machine-checked, three instances.

    NOT PROVED ANYWHERE, and specifically not here: that the three are ONE
    QUANTITY. The identity claim — that the whole-only share IS the Record
    coordinate, one quantity read at different depths — is a WAGER, recorded in
    `scratchpad/N18_BRIDGE_NOTE.md` and in the session record, and nothing in
    this file bears on it. The instances do not even share a type: instance 1's
    quantity is a real number of nats, instance 3's is a proposition about a
    corpus of strings. A common shape is the weakest possible evidence for a
    common substance, and it is what is on offer.

    The gap is not decoration. `NonFactoring` is a low bar — it says a summary
    threw something away, which most summaries do — so exhibiting three instances
    is a statement about the FORM of three arguments and carries no weight about
    their subject matter. The wager's kill lives with the wager, not with this
    file; a reader who takes these theorems as support for the identity claim has
    read them for more than they say.

    Fields carrying `True` are recorded commitments, not proofs — the repository's
    standing convention (`Core.Coordination`'s `InstrumentReach`,
    `Core.Epistemics`' `Gate.mechanized`). -/
structure UnificationReach where
  /-- PROVED. One shape, three instances, each derived from the published
      witnesses: `nonfactoring_parity`, `nonfactoring_cp_phase`,
      `nonfactoring_record`. -/
  three_instances_of_one_shape : True
  /-- PROVED. The domain argument transfers to all three at once, giving the
      three non-computability corollaries with no further argument. -/
  domain_argument_transfers : True
  /-- WAGER, NOT PROVED HERE. That the whole-only share and the Record
      coordinate are one quantity at different depths. Recorded in
      `scratchpad/N18_BRIDGE_NOTE.md`; carries its own kill there. -/
  identity_of_the_quantities_is_a_wager : True
  /-- SCOPE, INHERITED. Instance 2 is a model family, not flavour physics;
      instance 3 is about the taxonomy's shape, not its truth. -/
  instance_scopes_inherited_not_widened : True
  /-- THE BAR IS LOW, stated so it is not mistaken for a result: a shared
      failure-to-factor is a fact about the form of three arguments, and is not
      evidence about their subject matter. -/
  shared_shape_is_not_shared_substance : True

/-- The reach is recorded. -/
def unification_reach : UnificationReach :=
  ⟨trivial, trivial, trivial, trivial, trivial⟩

end CIRISOntology.Core
