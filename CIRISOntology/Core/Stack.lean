/-
CIRISOntology.Core.Stack — the assertive apparatus is a GROUNDING STACK, and the
stack terminates.

WHAT THIS FILE SAYS, and in which register. Four of `Generator.lean`'s eleven
sites are not eleven-fold independent of one another: they stand in a grounding
order, each rung the ground of the next.

    foundingAssumption   (Premises)     what is taken as given
        founds
    appliedRule          (Model)        the rule reasoned under
        derives
    factContent          (Facts)        what is claimed true
        modulates
    strengthMarker       (Confidence)   how hard the claim is pressed

THE ORDERING IS A DEFINITION, NOT A DISCOVERY. It is a modelling commitment
about the assertive apparatus — assumptions found rules, rules derive facts,
markers modulate facts — written down here in the same spirit as
`Generator.lean`'s site model: stated in the open so it can be attacked. Nothing
below proves that the world's assertions are built this way, and no theorem here
could.

WHAT IS A THEOREM, GIVEN THE DEFINITION. The stack is CLOSED and it TERMINATES.
Climbing it generates no fifth rung, and the reason is not fiat: the only
operation available at the top is modulation — attaching a strength marker — and
modulation is IDEMPOTENT. A hedge of a hedge is a hedge. "Probably probably p"
is marked once, not twice; iterated marking composes into one marker and so
creates no new site to classify. The ladder stops where its own generator runs
out of new things to make (`modulate_idempotent`, `ground_terminal`,
`iterate_site_in_stack`).

A SCOPE NOTE ON THE WORD "ASSERTIVE". `Generator.lean`'s `Force.assertive`
covers two sites only: `factContent` and `strengthMarker`. The stack is wider
than the force: it adds the two sites an assertive STANDS ON rather than
consists of. "Assertive apparatus" is therefore the honest name, and the widening
is part of the modelling commitment, not a re-reading of Searle.

THE MEASURED SHADOW — cited as a shadow, never as support. `PLANE_RESULTS.md`
(5,994 panel judgments) reports that the dominant confusion lines are
Premises→Facts (uniform in all seven conditions, one-directional) and
Model↔Facts (flickering, both directions). Both are internal to this stack, and
adjacent in it; a third dominant line, Structure→Manner, is off-stack entirely.
Part D's absorptions (Facts→Rules, Facts→Identity) are also off-stack: Rules and
Identity are directive and declarative sites, not rungs. So the measurement says
annotators blur exactly where this file says the grounding order is tightest —
which is a fact about CLASSIFIERS, consistent with the stack and predicted by
nothing here. It is not evidence that the grounding relation holds, and it is
not quoted in any claim's `basis`.

NOT CLAIMED, explicitly: that the remaining seven sites carry no order of their
own; that this is the only grounding order over these four; that idempotent
modulation is a fact about language rather than a property of the model defined
below. The kill for the modelling commitment is empirical and lives outside
Lean: exhibit an artifact change whose strength marking composes into a
genuinely new site — a second-order hedge that classifies differently from a
first-order one — and the terminality clause is wrong about the world, however
sound it remains about the model.
-/

import CIRISOntology.Core.Generator

namespace CIRISOntology.Core

/-! ### The stack, as a definition -/

/-- A rung of the assertive grounding stack. DEFINITION: these four sites of
    `Generator.lean` are asserted here to stand in a grounding order, and this
    type is that assertion made structural. Constructor names deliberately match
    the sites they name, so the embedding is visibly the identity. -/
inductive Rung
  /-- what the artifact takes as given — the ground of everything above -/
  | foundingAssumption
  /-- the rule applied to derive content from the assumption -/
  | appliedRule
  /-- the claim itself: what is asserted true -/
  | factContent
  /-- the strength marker on that claim — the top, and the only rung that
      modulates rather than grounds -/
  | strengthMarker
  deriving DecidableEq, Repr

/-- The embedding into the generator model: every rung IS a site, so nothing in
    this file introduces new classifiable structure. -/
def Rung.site : Rung → Site
  | .foundingAssumption => .foundingAssumption
  | .appliedRule        => .appliedRule
  | .factContent        => .factContent
  | .strengthMarker     => .strengthMarker

/-- The kind a change at this rung instantiates, inherited from the generator
    map rather than re-declared. -/
def Rung.kind (r : Rung) : ChoiceKind := r.site.kind

/-- The stack, bottom to top. -/
def Rung.all : List Rung :=
  [.foundingAssumption, .appliedRule, .factContent, .strengthMarker]

/-- Which sites belong to the assertive apparatus. Decidable, and with content:
    seven of the eleven sites are outside it (`seven_sites_outside_stack`). -/
def Site.inStack : Site → Bool
  | .foundingAssumption => true
  | .appliedRule        => true
  | .factContent        => true
  | .strengthMarker     => true
  | _                   => false

/-- Depth above the ground, as a DEFINITION of the ordering. Height is what
    makes "stands to the next as ground to grounded" a checkable statement
    rather than a picture. -/
def Rung.height : Rung → Nat
  | .foundingAssumption => 0
  | .appliedRule        => 1
  | .factContent        => 2
  | .strengthMarker     => 3

/-- THE STEP UP THE STACK: from a rung to what it grounds. DEFINITION, including
    the load-bearing final clause — the step out of `strengthMarker` is
    `strengthMarker` itself, because what a strength marker grounds is a
    strength marker. That clause is the single place a fifth rung could have
    been introduced, and declining to introduce one there is the whole of the
    terminality claim; everything proved about it below is bookkeeping on this
    definition. -/
def ground : Rung → Rung
  | .foundingAssumption => .appliedRule
  | .appliedRule        => .factContent
  | .factContent        => .strengthMarker
  | .strengthMarker     => .strengthMarker

/-- MODULATION: attach a strength marker to whatever the rung carries. The
    result is a strength marker, from any rung and from the marker itself —
    which is the formal content of "a hedge of a hedge is a hedge". DEFINITION;
    its idempotence is then a theorem about it. -/
def modulate : Rung → Rung
  | _ => .strengthMarker

/-! ### Four rungs, four kinds -/

/-- The stack has exactly four members. -/
theorem stack_card : Rung.all.length = 4 := rfl

/-- And the enumeration is complete. -/
theorem every_rung_listed (r : Rung) : r ∈ Rung.all := by
  cases r <;> repeat first | exact List.Mem.head _ | apply List.Mem.tail

/-- The stack's image in the taxonomy, bottom to top: Premises, Model, Facts,
    Confidence. These are four of the eleven artifact-local kinds and no other. -/
theorem stack_kinds :
    Rung.all.map Rung.kind =
      [.axiomatic, .nomological, .empirical, .epistemic] := rfl

/-- The same statement in the public vocabulary, so the claim can be read
    without the constructor names. -/
theorem stack_plain :
    Rung.all.map (fun r => r.kind.plain) = ["Premises", "Model", "Facts", "Confidence"] := rfl

/-- Each rung's kind is distinct: the four rungs are four kinds, not one kind
    seen four ways. (Inherited from `generator_injective`, but stated here
    because the stack claim needs it directly.) -/
theorem rung_kind_injective : ∀ r t : Rung, r.kind = t.kind → r = t := by
  intro r t h
  cases r <;> cases t <;> first | rfl | exact absurd h (by decide)

/-- The embedding is injective: distinct rungs, distinct sites. -/
theorem rung_site_injective : ∀ r t : Rung, r.site = t.site → r = t := by
  intro r t h
  cases r <;> cases t <;> first | rfl | exact absurd h (by decide)

/-- The stack is a PROPER part of the site model: exactly four of the eleven
    sites are in it. -/
theorem four_sites_in_stack : (Site.all.filter Site.inStack).length = 4 := by decide

/-- And seven are outside — so `inStack` is a real restriction, not a predicate
    that happens to hold everywhere. -/
theorem seven_sites_outside_stack :
    (Site.all.filter (fun s => !s.inStack)).length = 7 := by decide

/-- Every rung sits inside the stack when read back as a site. -/
theorem rung_site_inStack (r : Rung) : r.site.inStack = true := by
  cases r <;> rfl

/-! ### The ordering climbs, and the top is the top -/

/-- Below the top, the step strictly climbs: one rung of height per step. This
    is what "stands to the next as ground to grounded" buys — the relation is
    not a cycle among the four. -/
theorem ground_climbs (r : Rung) (h : r ≠ .strengthMarker) :
    (ground r).height = r.height + 1 := by
  cases r <;> first | rfl | exact absurd rfl h

/-- Below the top, the step moves: no rung grounds itself. -/
theorem ground_moves (r : Rung) (h : r ≠ .strengthMarker) : ground r ≠ r := by
  cases r <;> first | decide | exact absurd rfl h

/-- The top is maximal in height. -/
theorem top_is_maximal (r : Rung) : r.height ≤ Rung.strengthMarker.height := by
  cases r <;> decide

/-- The top is a fixed point of the step — the definitional clause, isolated so
    that what depends on it is visible. -/
theorem ground_top_fixed : ground .strengthMarker = Rung.strengthMarker := rfl

/-! ### Modulation is idempotent, and that is why the stack ends

Iteration is core Lean's `Nat.repeat` — n-fold application, no Mathlib
machinery anywhere in this file. -/

/-- Modulation is constant: from any rung it returns the marker. Stated once
    because both the idempotence results and the nesting result run on it. -/
theorem modulate_const (r : Rung) : modulate r = Rung.strengthMarker := by
  cases r <;> rfl

/-- Modulating anything yields a strength marker: modulation does not produce a
    site of its own. -/
theorem modulate_site (r : Rung) : (modulate r).site = Site.strengthMarker := by
  cases r <;> rfl

/-- Modulating the top changes nothing. -/
theorem modulate_top : modulate .strengthMarker = Rung.strengthMarker := rfl

/-- **MODULATION IS IDEMPOTENT.** A hedge of a hedge is a hedge: marking an
    already-marked assertion composes into one strength marker, and generates no
    new site to classify. -/
theorem modulate_idempotent (r : Rung) : modulate (modulate r) = modulate r := by
  rw [modulate_const, modulate_const]

/-- The same, for arbitrarily deep nesting: any number of iterated hedges is one
    hedge. "Probably probably probably p" is marked once. -/
theorem modulate_nested (r : Rung) (n : Nat) :
    Nat.repeat modulate (n + 1) r = modulate r := by
  show modulate (Nat.repeat modulate n r) = modulate r
  rw [modulate_const, modulate_const]

/-- Modulation is exactly the top of the climb: hedging any rung lands where
    grounding it three times lands. The two operations of the model agree at the
    place the model says they must. -/
theorem modulate_eq_climb (r : Rung) : modulate r = Nat.repeat ground 3 r := by
  cases r <;> rfl

/-! ### Terminality: the stack generates no fifth site -/

/-- Three steps from ANY rung — not merely from the bottom — reach the top. -/
theorem ground_three (r : Rung) : ground (ground (ground r)) = Rung.strengthMarker := by
  cases r <;> rfl

/-- The same, as an iteration count. -/
theorem ground_reaches_top (r : Rung) : Nat.repeat ground 3 r = Rung.strengthMarker :=
  ground_three r

/-- **THE STACK TERMINATES.** Every further step stays at the top: from any
    rung, every iterate at or beyond three is the strength marker. There is no
    rung four. -/
theorem ground_terminal (r : Rung) (n : Nat) :
    Nat.repeat ground (n + 3) r = Rung.strengthMarker :=
  ground_three (Nat.repeat ground n r)

/-- **CLOSURE — no fifth site is generated.** Every iterate of the step, from
    any rung, read back into the generator model, is one of the four assertive
    sites. Thin BY DESIGN: `Rung` is a four-element type, so what this really
    checks is that `ground`'s definition never had to leave it — that the
    codomain choice at the top (`ground_top_fixed`) is the only thing standing
    between the model and an infinite ladder of markers. -/
theorem iterate_site_in_stack (r : Rung) (n : Nat) :
    (Nat.repeat ground n r).site.inStack = true := by
  generalize Nat.repeat ground n r = t
  exact rung_site_inStack t

/-- The same closure stated against the eleven sites by name, so the reader does
    not have to take the four-element type on trust. -/
theorem iterate_site_is_one_of_four (r : Rung) (n : Nat) :
    (Nat.repeat ground n r).site ∈
      [Site.foundingAssumption, Site.appliedRule, Site.factContent, Site.strengthMarker] := by
  generalize Nat.repeat ground n r = t
  cases t <;> repeat first | exact List.Mem.head _ | apply List.Mem.tail

/-- And the terminal site is `strengthMarker` — Confidence, the top of the
    taxonomy's assertive apparatus. What the stack ends in is a kind, not a
    remainder. -/
theorem terminal_kind : Rung.strengthMarker.kind = WrongKind.epistemic := rfl

end CIRISOntology.Core
