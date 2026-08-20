/-
CIRISOntology.Core.Scan — the taxonomy's SCAN: what the generator yields when the
artifact is denied some of its expressive resources.

WHAT A SCAN IS. `Generator.lean` derives the eleven artifact-local kinds as the
image of a site model whose components are grounded in speech-act theory. That
derivation quietly assumes the artifact has ALL of the illocutionary force
available to it — it can claim, it can require, it can declare. Take one of those
away and some sites cease to exist: an artifact that cannot require anything has
no directive content to vary, no permission ordering, no step ordering. The kinds
those sites generate go with them. A SCAN is the taxonomy that survives a given
force budget, and this file computes the family.

THE RESULT, in one line: along the chain assertive ⊂ assertive+directive ⊂ all
three, the taxonomy runs **7 → 10 → 11**, and the eleven-kind taxonomy is the
TERMINAL member — no further force adds a kind, because there is no further
force. The taxonomy is not a free-standing list of eleven; it is the top of a
resource-indexed family, and the count 11 is what full expressive resource buys.

SCOPE — read this before reading a number off the file. Everything below is a
MODEL COMPUTATION. It says what the generator of `Generator.lean` yields under a
restricted force budget, and it inherits that model's honest frame entirely: this
is THEOREM-GIVEN-MODEL, and "are there more kinds?" remains the ecological
question, not a question these `rfl`s can touch. Nothing here is measured, and
nothing here is about the world.

AND THE NUMEROLOGY WARNING, stated in the file rather than left to a reader's
restraint. The chain {7, 10, 11} invites comparison with numeric sequences in
other subjects. This file makes no such comparison and licenses none; any
resemblance is SHAPE-ONLY, belongs in the design note where it can be attacked as
the analogy it is, and must never be read back into these theorems as support.
Two facts kept adjacent here for exactly that reason:

  * {7, 10, 11} is a CHAIN, not the lattice. There are eight force budgets and
    their cardinalities are {3, 4, 6, 7, 7, 8, 10, 11} (`scan_lattice`). The
    chain is the one obtained by adding forces in a particular ORDER, and a
    different order gives {4, 8, 11} or {6, 7, 11}. Choosing the order is a
    choice, and it is not forced by anything proved here.
  * The floor is 3, not 0. Strip every force and three kinds remain, because
    three sites are force-NEUTRAL carriers (`carriers_survive_everything`).

THE ASSIGNMENT MOST OPEN TO ATTACK, and — checked rather than guessed — what it
actually moves. Placing `appliedRule` and `foundingAssumption` under `assertive`
is a modelling call: a rule APPLIED to derive content, and an assumption
everything composes over, are the apparatus by which an artifact gets to
claiming, with no independent force of their own. Someone who instead reads them
as force-neutral carriers gets THE SAME CHAIN — 7 → 10 → 11, list for list
(`scanAlt_chain_agrees`) — because every budget in the chain already grants
assertion, so those two sites move between "assertive apparatus" and "carrier"
without ever leaving. The assignment is visible only in budgets that DENY
assertion, where it lifts the floor from 3 to 5 (`scanAlt_floor`). So the chain
and its terminus are robust to the contested call; the lattice's assertion-free
corner is not. That distinction is stated here because the first draft of this
header asserted the opposite, and computing it is what caught the error.
-/

import CIRISOntology.Core.Generator

namespace CIRISOntology.Core

/-! ### The force budget -/

/-- All three illocutionary forces. -/
def Force.all : List Force := [.assertive, .directive, .declarative]

/-- The enumeration is complete — there is no fourth force to add, which is what
    makes the three-force scan terminal rather than merely largest-so-far. -/
theorem Force.mem_all (f : Force) : f ∈ Force.all := by
  cases f <;> repeat first | exact List.Mem.head _ | apply List.Mem.tail

/-- WHICH FORCE'S APPARATUS A SITE IS. Three sites answer `none`: they are
    force-NEUTRAL carriers, the layer through which any force's commitments are
    transmitted. An encoding serializes a claim as readily as a requirement; a
    register presents either; an instance token is unbound detail under both. A
    carrier is available whatever the budget, which is why the floor is 3.

    See the header for the one contestable assignment (`appliedRule`,
    `foundingAssumption` as assertive apparatus). -/
def Site.force : Site → Option Force
  -- assertive apparatus: what is claimed, how strongly, under what rule, on what premise
  | .factContent        => some .assertive
  | .strengthMarker     => some .assertive
  | .appliedRule        => some .assertive
  | .foundingAssumption => some .assertive
  -- directive apparatus: what is required, in what preference order, in what step order
  | .directiveContent   => some .directive
  | .preferenceOrder    => some .directive
  | .stepOrder          => some .directive
  -- declarative apparatus: what counts as what
  | .declarationContent => some .declarative
  -- force-neutral carriers: they carry any force's commitments
  | .encoding           => none
  | .register           => none
  | .instanceToken      => none

/-- The carriers, named. -/
def Site.carriers : List Site := [.encoding, .register, .instanceToken]

/-- The carriers are exactly the force-neutral sites — the `none` fibre is not a
    leftover but a third of the model. -/
theorem carriers_are_the_neutral_sites :
    Site.all.filter (fun s => s.force.isNone) = Site.carriers := rfl

/-! ### Availability, and the scan -/

/-- Is this site available to an artifact whose force budget is `F`? A carrier
    always is; a force's apparatus only if that force is in the budget. -/
def Site.available (F : List Force) (s : Site) : Bool :=
  match s.force with
  | none   => true
  | some f => F.contains f

/-- The sites an artifact with force budget `F` actually has to vary. -/
def availableSites (F : List Force) : List Site :=
  Site.all.filter (Site.available F)

/-- THE SCAN: the kinds of change available under force budget `F` — the image
    of the generator map over the surviving sites.

    No deduplication step is applied, and none is needed: `scan_nodup` proves the
    image already carries each kind at most once, because `generator_injective`
    makes distinct sites give distinct kinds. That is the stronger statement, so
    the length below really is a count of DISTINCT kinds. -/
def scan (F : List Force) : List ChoiceKind :=
  (availableSites F).map Site.kind

/-- How many kinds a force budget buys. -/
def scanCard (F : List Force) : Nat := (scan F).length

/-- `Site.all` lists each site once. -/
theorem site_all_nodup : Site.all.Nodup := by decide

/-- THE SCAN IS DUPLICATE-FREE, for any budget whatever. So `scanCard` counts
    distinct kinds and no dedup pass can change it. -/
theorem scan_nodup (F : List Force) : (scan F).Nodup :=
  List.Pairwise.map Site.kind
    (fun a b hab hk => hab (generator_injective a b hk))
    (List.Nodup.sublist (List.filter_sublist Site.all) site_all_nodup)

/-! ### The three named budgets

Named so the chain can be stated once and referred to, not so the order in which
forces are added acquires any status it has not earned. See `scan_lattice`. -/

/-- Claiming only: an artifact that can assert and nothing else. -/
def Force.assertiveOnly : List Force := [.assertive]

/-- Claiming and requiring: assertion plus the deontic apparatus. -/
def Force.assertiveDirective : List Force := [.assertive, .directive]

/-! ### The chain: 7 → 10 → 11 -/

/-- ASSERTIVE ONLY GIVES SEVEN. An artifact that can only claim still has
    Structure, Manner and Circumstances — the carriers — plus the four kinds its
    own apparatus generates. Rules, Priorities, Process and Identity are absent,
    and absent for a reason a reader can check: there is no site to host them. -/
theorem scan_assertive :
    scan Force.assertiveOnly =
      [.empirical, .epistemic, .nomological, .axiomatic,
       .structural, .pragmatic, .contingent] := rfl

theorem scan_assertive_card : scanCard Force.assertiveOnly = 7 := rfl

/-- ADDING THE DIRECTIVE GIVES TEN. Rules, Priorities and Process arrive
    together, because they are one force's apparatus. Only Identity is still
    missing. -/
theorem scan_assertive_directive :
    scan Force.assertiveDirective =
      [.empirical, .epistemic, .deontic, .axiotic, .procedural,
       .nomological, .axiomatic, .structural, .pragmatic, .contingent] := rfl

theorem scan_assertive_directive_card : scanCard Force.assertiveDirective = 10 := rfl

/-- ALL THREE FORCES GIVE ELEVEN, and it is the generator's full image. -/
theorem scan_full : scan Force.all = Site.all.map Site.kind := rfl

theorem scan_full_card : scanCard Force.all = 11 := rfl

/-- And the eleven are the base plane's eleven. The two lists are in different
    orders — `Site.all`'s versus `WrongKind.all`'s — so this is stated as the
    count plus set equality rather than as list equality, which is what "the same
    taxonomy" actually means here. -/
theorem scan_full_card_eq_basePlane : scanCard Force.all = basePlane.length := rfl

theorem scan_full_is_basePlane (k : ChoiceKind) :
    k ∈ scan Force.all ↔ k ∈ basePlane := by
  -- Eleven kinds are in both lists and `testimonial` is in neither; both facts
  -- are built from `List.Mem`'s constructors rather than by `decide`, which
  -- would cost `propext` (list membership decides via `decidable_of_iff`).
  have step : ∀ (a b : ChoiceKind) (l : List ChoiceKind), a ≠ b → a ∉ l → a ∉ b :: l := by
    intro a b l hne hl hm
    cases hm with
    | head => exact hne rfl
    | tail _ hm => exact hl hm
  cases k <;> constructor <;> intro h <;>
    first
      | ((repeat first | exact List.Mem.head _ | apply List.Mem.tail); done)
      | (refine absurd h ?_
         repeat' first
           | (refine step _ _ _ ?_ ?_; · decide)
           | (intro hm; cases hm))

/-- Record is in no scan, at any budget — it was never site-generated, so no
    force budget can supply it. The one frame-relation stays outside the family
    entirely. -/
theorem record_in_no_scan (F : List Force) : WrongKind.testimonial ∉ scan F := by
  -- Peeled site by site rather than through `List.mem_map`, which would cost
  -- `propext` and `Quot.sound`; `record_not_site_generated` supplies each step.
  have step : ∀ (a b : ChoiceKind) (l : List ChoiceKind), a ≠ b → a ∉ l → a ∉ b :: l := by
    intro a b l hne hl hm
    cases hm with
    | head => exact hne rfl
    | tail _ hm => exact hl hm
  show WrongKind.testimonial ∉ (availableSites F).map Site.kind
  generalize availableSites F = l
  induction l with
  | nil => intro hm; cases hm
  | cons s l ih =>
    exact step _ _ _ (fun hk => record_not_site_generated s hk.symm) ih

/-! ### Monotonicity and terminality -/

/-- A bigger budget keeps every site the smaller one had. -/
theorem availableSites_mono {F₁ F₂ : List Force} (h : ∀ f : Force, f ∈ F₁ → f ∈ F₂) :
    availableSites F₁ ⊆ availableSites F₂ := by
  intro s hs
  rw [availableSites, List.mem_filter] at hs ⊢
  refine ⟨hs.1, ?_⟩
  have hav := hs.2
  rw [Site.available] at hav ⊢
  cases hf : s.force with
  | none => rfl
  | some f =>
    rw [hf] at hav
    exact List.elem_eq_true_of_mem (h f (List.mem_of_elem_eq_true hav))

/-- ADDING A FORCE NEVER REMOVES A KIND. The family is monotone in the budget,
    so the chain is a genuine ascent and not a reshuffle. -/
theorem scan_mono {F₁ F₂ : List Force} (h : ∀ f : Force, f ∈ F₁ → f ∈ F₂) :
    scan F₁ ⊆ scan F₂ :=
  List.map_subset Site.kind (availableSites_mono h)

/-- Every budget is under the full one. -/
theorem scan_le_full (F : List Force) : scan F ⊆ scan Force.all :=
  scan_mono (fun f _ => Force.mem_all f)

/-- A budget holding all three forces has every site. -/
theorem availableSites_univ {F : List Force} (h : ∀ f : Force, f ∈ F) :
    availableSites F = Site.all := by
  rw [availableSites]
  refine List.filter_eq_self.mpr (fun s _ => ?_)
  rw [Site.available]
  cases hf : s.force with
  | none => rfl
  | some f => exact List.elem_eq_true_of_mem (h f)

/-- THE FULL SCAN IS TERMINAL. Any budget containing all three forces gives
    exactly the three-force scan — no superset, no repetition, no ordering of the
    budget adds anything. This is trivial mathematics and it is the point: the
    eleven-kind taxonomy is where the family STOPS, and it stops because the
    generator has run out of force to be given, not because eleven was chosen. -/
theorem scan_terminal {F : List Force} (h : ∀ f : Force, f ∈ F) :
    scan F = scan Force.all := by
  rw [scan, scan, availableSites_univ h, availableSites_univ Force.mem_all]

theorem scan_terminal_card {F : List Force} (h : ∀ f : Force, f ∈ F) :
    scanCard F = 11 := by
  rw [scanCard, scan_terminal h]; rfl

/-! ### The whole lattice, so the chain cannot be mistaken for the family -/

/-- All eight force budgets. -/
def Force.budgets : List (List Force) :=
  [[], [.assertive], [.directive], [.declarative],
   [.assertive, .directive], [.assertive, .declarative], [.directive, .declarative],
   Force.all]

/-- THE FULL PICTURE, and the corrective to reading {7, 10, 11} as a discovered
    sequence: the eight budgets give cardinalities 3, 7, 6, 4, 10, 8, 7, 11. The
    chain this file names is one path up this lattice; adding declarative first
    gives 4 → 8 → 11 instead. Every path ends at 11 (`scan_terminal`), and that
    terminus is the only order-independent fact in the family. -/
theorem scan_lattice :
    Force.budgets.map scanCard = [3, 7, 6, 4, 10, 8, 7, 11] := rfl

/-- THE FLOOR IS THE CARRIERS. With no force at all, three kinds remain —
    Structure, Manner, Circumstances. An artifact that claims nothing, requires
    nothing and declares nothing can still be encoded differently, presented
    differently, and instantiated differently. Those three are the kinds of
    change that are about the vehicle rather than the message. -/
theorem carriers_survive_everything :
    scan [] = [.structural, .pragmatic, .contingent] := rfl

theorem scan_floor : scanCard [] = 3 := rfl

/-- And the floor is a floor: the carriers are in every scan. -/
theorem carriers_in_every_scan (F : List Force) : scan [] ⊆ scan F :=
  scan_mono (fun _ h => absurd h (by simp))

/-! ### The contested assignment, tested rather than asserted

The header names one modelling call that a reader could reasonably reject. Rather
than defend it in prose, the rival reading is built and the difference computed. -/

/-- THE RIVAL READING: `appliedRule` and `foundingAssumption` taken as
    force-neutral carriers — machinery the artifact has whether or not it can
    assert — instead of as assertive apparatus. Everything else unchanged. -/
def Site.forceAlt : Site → Option Force
  | .appliedRule        => none
  | .foundingAssumption => none
  | s                   => s.force

/-- The scan computed under the rival reading. -/
def scanAlt (F : List Force) : List ChoiceKind :=
  (Site.all.filter (fun s =>
    match s.forceAlt with
    | none   => true
    | some f => F.contains f)).map Site.kind

/-- THE CHAIN DOES NOT DEPEND ON THE CONTESTED ASSIGNMENT. All three rungs agree
    list for list, not merely in count: once a budget grants assertion, moving a
    site between "assertive apparatus" and "carrier" cannot remove it. The
    headline 7 → 10 → 11 therefore survives losing the argument in the header. -/
theorem scanAlt_chain_agrees :
    scanAlt Force.assertiveOnly = scan Force.assertiveOnly ∧
    scanAlt Force.assertiveDirective = scan Force.assertiveDirective ∧
    scanAlt Force.all = scan Force.all := ⟨rfl, rfl, rfl⟩

/-- WHERE IT DOES SHOW UP: the assertion-free corner of the lattice. The floor
    rises from 3 to 5 and the directive-only budget from 6 to 8, so the two
    readings ARE distinguishable — just not by any budget the chain visits. A
    scan that denies assertion is the experiment that separates them. -/
theorem scanAlt_floor : (scanAlt []).length = 5 := rfl

theorem scanAlt_directive_only : (scanAlt [Force.directive]).length = 8 := rfl

end CIRISOntology.Core
