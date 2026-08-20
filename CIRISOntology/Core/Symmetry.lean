/-
CIRISOntology.Core.Symmetry — the symmetries of the site model, and the ones it
breaks.

WHAT THIS FILE IS. `Generator.lean` derives eleven kinds as the image of a site
model; `Scan.lean` computes what survives a restricted force budget;
`Surface.lean` splits the eleven into four surfaces and seven depths; `Stack.lean`
orders four of them into a grounding ladder. Each of those files asks what the
model CONTAINS. This one asks what the model's structure ALLOWS TO BE MOVED —
which sites can be interchanged without disturbing anything the earlier files
proved, and which cannot. The answer to that question is a group, and computing
it is the whole content here.

THE PLAYBOOK BEING TRANSLATED, named so the borrowing is visible rather than
implied. Four moves, in the order they are used below:

  * **Groups, in Wigner's use.** The structure-preserving maps of an object form
    a group, and its SIZE is a measure of how much slack the object has. A rigid
    object has a trivial group; an object with interchangeable parts has a big
    one. So "how arbitrary is this taxonomy?" becomes a computation (§1).
  * **Symmetry breaking is content.** When two slots stop being interchangeable,
    something distinguishes them, and that something is structure rather than
    accident. Here the breaking field is `Stack.lean`'s grounding order: it is
    exactly what collapses the assertive block's freedom from six to one (§1,
    `stack_order_breaks_assertive_symmetry`).
  * **No-go results.** Some enlargements of a symmetry are forbidden outright,
    and the proof is usually cheap — a counting argument, not a deep one. The
    fit-conjugation dies by cardinality, 4 against 3 (§2).
  * **Noether's shape.** A direction along which nothing changes carries a
    conserved quantity. Frame supply is such a direction for the eleven, and the
    kind label is what rides along it unchanged (§3).

THE FENCE, and it is not decorative. Every one of those four is a SHAPE borrowed
to organise the work. No theorem below says anything about physics, none may be
quoted as evidence for any analogy, and the comparisons live in the bridge note
(`scratchpad/N18_BRIDGE_NOTE.md`) where they can be attacked as the analogies they
are. In particular "Noether" here is a pun on invariance: there is no action, no
continuous parameter, and no conserved current anywhere in this file. What is
actually below is `rfl`s and case bashes about an eleven-element inductive type.

SCOPE, inherited entirely from `Generator.lean`. Everything here is
THEOREM-GIVEN-MODEL. A symmetry of the model is not a symmetry of the world, and
a rigidity of the model is not a discovery about change. The honest question
remains "is the site model adequate?", which is answered by measurement and never
by this file.
-/

import CIRISOntology.Core.Surface
import CIRISOntology.Core.Stack

namespace CIRISOntology.Core

/-! ### §0 The structure to be preserved

A symmetry has to be a symmetry OF something. The something is the structure the
earlier files put on `Site`: which force's apparatus a site is (`Scan.lean`),
whether it is its block's gross face (`Surface.lean`), and — as a separable
component, because it turns out to be the one that matters — where it stands in
the assertive grounding ladder (`Stack.lean`). -/

/-- Height in `Stack.lean`'s assertive grounding ladder, `none` off the ladder.
    The numbers are not re-declared here: they are `Rung.height`, read through
    the embedding `Rung.site`, so this component carries exactly the modelling
    commitment `Stack.lean` states and no more. -/
def Site.stackHeight : Site → Option Nat
  | .foundingAssumption => some Rung.foundingAssumption.height
  | .appliedRule        => some Rung.appliedRule.height
  | .factContent        => some Rung.factContent.height
  | .strengthMarker     => some Rung.strengthMarker.height
  | _                   => none

/-- The heights are the stack's, not new ones. -/
theorem stackHeight_rung (r : Rung) : r.site.stackHeight = some r.height := by
  cases r <;> rfl

/-- And the ladder is exactly `Stack.lean`'s four sites: a site has a height iff
    it is in the stack. -/
theorem stackHeight_isSome_iff_inStack (s : Site) : s.stackHeight.isSome = s.inStack := by
  cases s <;> rfl

/-- The four heights are four: distinct rungs stand at distinct heights, which is
    why adding this component pins the assertive block completely. -/
theorem stackHeight_distinguishes_rungs (r t : Rung) :
    r.site.stackHeight = t.site.stackHeight → r = t := by
  intro h
  cases r <;> cases t <;> first | rfl | exact absurd h (by decide)

/-- **A STRUCTURE-PRESERVING MAP OF THE SITE MODEL.** Injective (on an
    eleven-element type that is bijectivity — and every map the enumeration below
    returns is exhibited there as a composite of explicit involutions and a
    three-cycle, so nothing is being smuggled in by taking the weaker condition),
    commuting with the force fibration, and fixing the surface/depth split.

    Preservation of `Site.block` is NOT a separate component: it is implied,
    because `Surface.lean`'s `block_is_force_fibre` makes the block a function of
    the force (`structurePreserving_preserves_block`). -/
structure StructurePreserving (f : Site → Site) : Prop where
  /-- distinct sites go to distinct sites -/
  injective : ∀ s t : Site, f s = f t → s = t
  /-- the illocutionary force of a site is untouched -/
  force_eq : ∀ s, (f s).force = s.force
  /-- surfaces stay surfaces and depths stay depths -/
  surface_eq : ∀ s, (f s).isSurface = s.isSurface

/-- **AND THE SAME WITH THE GROUNDING ORDER ADDED.** The extra component is the
    whole subject of §1's second theorem: it is a separable requirement, and
    removing it is what lets the assertive block rotate. -/
structure StackPreserving (f : Site → Site) : Prop where
  /-- everything `StructurePreserving` asks -/
  toStructurePreserving : StructurePreserving f
  /-- and the rung a site stands on -/
  height_eq : ∀ s, (f s).stackHeight = s.stackHeight

/-- Preserving the force preserves the block, for free. -/
theorem structurePreserving_preserves_block {f : Site → Site} (h : StructurePreserving f)
    (s : Site) : (f s).block = s.block := by
  rw [block_is_force_fibre, block_is_force_fibre, h.force_eq]

/-! ### §1 Rigidity: the automorphism group, computed

The strategy is the obvious one and it is cheap because the type is finite.
`allowed s` is the set of sites a structure-preserving map is permitted to send
`s` to — everything with the same force and the same surface flag. That bounds
the group from above. The bound is then shown to be attained by exhibiting the
maps that realise it, so the group is computed rather than merely bounded. -/

/-- Where a structure-preserving map may send a site: same force, same surface
    flag. Derived from the two components rather than written by hand, so the
    orbits below cannot drift from the definition of the symmetry. -/
def allowed (s : Site) : List Site :=
  Site.all.filter (fun t => (t.force == s.force) && (t.isSurface == s.isSurface))

/-- The same, with `Stack.lean`'s grounding order added as a third component. -/
def allowedStack (s : Site) : List Site :=
  Site.all.filter (fun t =>
    (t.force == s.force) && (t.isSurface == s.isSurface) && (t.stackHeight == s.stackHeight))

/-- **THE ORBIT STRUCTURE, in the public vocabulary.** Read as the answer to
    "which labels could be interchanged without disturbing anything the model
    proves?": Facts, Rules, Identity and Manner are alone (they are their blocks'
    faces); Confidence, Model and Premises are mutually interchangeable; so are
    Priorities and Process; so are Structure and Circumstances. Nothing crosses a
    block, and nothing crosses the surface/depth line. -/
theorem orbits_plain :
    Site.all.map (fun s => (allowed s).map (fun t => t.kind.plain)) =
      [["Facts"],
       ["Confidence", "Model", "Premises"],
       ["Rules"],
       ["Identity"],
       ["Priorities", "Process"],
       ["Priorities", "Process"],
       ["Confidence", "Model", "Premises"],
       ["Confidence", "Model", "Premises"],
       ["Structure", "Circumstances"],
       ["Manner"],
       ["Structure", "Circumstances"]] := rfl

/-- With the grounding order added, the three-element orbit shatters into
    singletons: Confidence, Model and Premises stand at different heights of
    `Stack.lean`'s ladder, so nothing may move them. Two orbits survive, both
    off-stack. -/
theorem orbits_plain_with_stack :
    Site.all.map (fun s => (allowedStack s).map (fun t => t.kind.plain)) =
      [["Facts"],
       ["Confidence"],
       ["Rules"],
       ["Identity"],
       ["Priorities", "Process"],
       ["Priorities", "Process"],
       ["Model"],
       ["Premises"],
       ["Structure", "Circumstances"],
       ["Manner"],
       ["Structure", "Circumstances"]] := rfl

/-! #### The upper bound -/

/-- The pointwise constraint: anything agreeing with `s` on force and surface
    flag is in `allowed s`. One hundred and twenty-one ground cases. -/
theorem step_allowed (s t : Site) (hf : t.force = s.force) (hs : t.isSurface = s.isSurface) :
    (allowed s).contains t = true := by
  cases s <;> cases t <;>
    first | rfl | exact absurd hf (by decide) | exact absurd hs (by decide)

/-- The same with the height component. -/
theorem step_allowedStack (s t : Site) (hf : t.force = s.force) (hs : t.isSurface = s.isSurface)
    (hh : t.stackHeight = s.stackHeight) : (allowedStack s).contains t = true := by
  cases s <;> cases t <;>
    first
      | rfl
      | exact absurd hf (by decide)
      | exact absurd hs (by decide)
      | exact absurd hh (by decide)

theorem sp_mem_allowed {f : Site → Site} (h : StructurePreserving f) (s : Site) :
    (allowed s).contains (f s) = true :=
  step_allowed s (f s) (h.force_eq s) (h.surface_eq s)

theorem stp_mem_allowedStack {f : Site → Site} (h : StackPreserving f) (s : Site) :
    (allowedStack s).contains (f s) = true :=
  step_allowedStack s (f s) (h.toStructurePreserving.force_eq s)
    (h.toStructurePreserving.surface_eq s) (h.height_eq s)

/-- The four surfaces have singleton orbits, so a structure-preserving map fixes
    each of them. This is the half of the rigidity that `Surface.lean`'s forcing
    argument already pays for: three of the four surfaces are pinned by Searle's
    table, the fourth by that file's one modelling choice. -/
theorem allowed_singleton {s x : Site}
    (hs : s = .factContent ∨ s = .directiveContent ∨ s = .declarationContent ∨ s = .register)
    (h : (allowed s).contains x = true) : x = s := by
  rcases hs with rfl | rfl | rfl | rfl <;> cases x <;> first | rfl | exact absurd h (by decide)

/-- The assertive depths — Confidence, Model, Premises — form one orbit. -/
theorem allowed_assertiveDepth {s x : Site}
    (hs : s = .strengthMarker ∨ s = .appliedRule ∨ s = .foundingAssumption)
    (h : (allowed s).contains x = true) :
    x = .strengthMarker ∨ x = .appliedRule ∨ x = .foundingAssumption := by
  rcases hs with rfl | rfl | rfl <;> cases x <;>
    first
      | exact Or.inl rfl
      | exact Or.inr (Or.inl rfl)
      | exact Or.inr (Or.inr rfl)
      | exact absurd h (by decide)

/-- The directive depths — Priorities, Process — form one orbit. -/
theorem allowed_directiveDepth {s x : Site} (hs : s = .preferenceOrder ∨ s = .stepOrder)
    (h : (allowed s).contains x = true) : x = .preferenceOrder ∨ x = .stepOrder := by
  rcases hs with rfl | rfl <;> cases x <;>
    first | exact Or.inl rfl | exact Or.inr rfl | exact absurd h (by decide)

/-- The carrier depths — Structure, Circumstances — form one orbit. -/
theorem allowed_carrierDepth {s x : Site} (hs : s = .encoding ∨ s = .instanceToken)
    (h : (allowed s).contains x = true) : x = .encoding ∨ x = .instanceToken := by
  rcases hs with rfl | rfl <;> cases x <;>
    first | exact Or.inl rfl | exact Or.inr rfl | exact absurd h (by decide)

/-- Under the grounding order, seven of the eleven sites are pinned outright. -/
theorem allowedStack_singleton {s x : Site}
    (hs : s = .factContent ∨ s = .strengthMarker ∨ s = .appliedRule ∨ s = .foundingAssumption
        ∨ s = .directiveContent ∨ s = .declarationContent ∨ s = .register)
    (h : (allowedStack s).contains x = true) : x = s := by
  rcases hs with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> cases x <;>
    first | rfl | exact absurd h (by decide)

theorem allowedStack_directiveDepth {s x : Site} (hs : s = .preferenceOrder ∨ s = .stepOrder)
    (h : (allowedStack s).contains x = true) : x = .preferenceOrder ∨ x = .stepOrder := by
  rcases hs with rfl | rfl <;> cases x <;>
    first | exact Or.inl rfl | exact Or.inr rfl | exact absurd h (by decide)

theorem allowedStack_carrierDepth {s x : Site} (hs : s = .encoding ∨ s = .instanceToken)
    (h : (allowedStack s).contains x = true) : x = .encoding ∨ x = .instanceToken := by
  rcases hs with rfl | rfl <;> cases x <;>
    first | exact Or.inl rfl | exact Or.inr rfl | exact absurd h (by decide)

/-! #### Naming a permutation

A map `Site → Site` is its table of values on `Site.all`. `perm` writes that
table given only the seven depth images, because the four surfaces are fixed by
every automorphism (`allowed_singleton`) and so carry no information. The seven
arguments are, in order, the images of `strengthMarker`, `appliedRule`,
`foundingAssumption`, `preferenceOrder`, `stepOrder`, `encoding`,
`instanceToken` — Confidence, Model, Premises, Priorities, Process, Structure,
Circumstances. -/

/-- A candidate table, written from the seven depth images. -/
def perm (a₁ a₂ a₃ d₁ d₂ c₁ c₂ : Site) : List Site :=
  [.factContent, a₁, .directiveContent, .declarationContent, d₁, d₂, a₂, a₃, c₁, .register, c₂]

/-- The six permutations of the assertive depths, as `(image of strengthMarker,
    image of appliedRule, image of foundingAssumption)`. -/
def assertiveTriples : List (Site × Site × Site) :=
  [(.strengthMarker, .appliedRule, .foundingAssumption),
   (.strengthMarker, .foundingAssumption, .appliedRule),
   (.appliedRule, .strengthMarker, .foundingAssumption),
   (.appliedRule, .foundingAssumption, .strengthMarker),
   (.foundingAssumption, .strengthMarker, .appliedRule),
   (.foundingAssumption, .appliedRule, .strengthMarker)]

/-- The two permutations of the directive depths. -/
def directivePairs : List (Site × Site) :=
  [(.preferenceOrder, .stepOrder), (.stepOrder, .preferenceOrder)]

/-- The two permutations of the carrier depths. -/
def carrierPairs : List (Site × Site) :=
  [(.encoding, .instanceToken), (.instanceToken, .encoding)]

/-- **THE AUTOMORPHISM GROUP WITHOUT THE GROUNDING ORDER**, as tables: the
    product of the three orbits' symmetric groups. -/
def autNoStack : List (List Site) :=
  assertiveTriples.flatMap fun a => directivePairs.flatMap fun d => carrierPairs.map fun c =>
    perm a.1 a.2.1 a.2.2 d.1 d.2 c.1 c.2

/-- **THE AUTOMORPHISM GROUP WITH THE GROUNDING ORDER**, as tables. -/
def autWithStack : List (List Site) :=
  directivePairs.flatMap fun d => carrierPairs.map fun c =>
    perm .strengthMarker .appliedRule .foundingAssumption d.1 d.2 c.1 c.2

/-! #### The two groups, stated

Both are small and nontrivial, and that is the honest answer: the site model is
neither arbitrary (which would show as a large group) nor perfectly rigid (which
would show as a trivial one). The interesting number is the RATIO — 24 of the
11! = 39,916,800 permutations of the eleven sites survive without the grounding
order, and 4 with it. -/

/-- **WITHOUT THE GROUNDING ORDER: TWENTY-FOUR.** The group is
    S₃ × Z₂ × Z₂ — free permutation of {Confidence, Model, Premises}, independent
    swap of {Priorities, Process}, independent swap of
    {Structure, Circumstances}, and nothing else. Every one of the twenty-four is
    written out. -/
theorem aut_without_stack :
    autNoStack =
  [perm .strengthMarker .appliedRule .foundingAssumption
        .preferenceOrder .stepOrder .encoding .instanceToken,
   perm .strengthMarker .appliedRule .foundingAssumption
        .preferenceOrder .stepOrder .instanceToken .encoding,
   perm .strengthMarker .appliedRule .foundingAssumption
        .stepOrder .preferenceOrder .encoding .instanceToken,
   perm .strengthMarker .appliedRule .foundingAssumption
        .stepOrder .preferenceOrder .instanceToken .encoding,
   perm .strengthMarker .foundingAssumption .appliedRule
        .preferenceOrder .stepOrder .encoding .instanceToken,
   perm .strengthMarker .foundingAssumption .appliedRule
        .preferenceOrder .stepOrder .instanceToken .encoding,
   perm .strengthMarker .foundingAssumption .appliedRule
        .stepOrder .preferenceOrder .encoding .instanceToken,
   perm .strengthMarker .foundingAssumption .appliedRule
        .stepOrder .preferenceOrder .instanceToken .encoding,
   perm .appliedRule .strengthMarker .foundingAssumption
        .preferenceOrder .stepOrder .encoding .instanceToken,
   perm .appliedRule .strengthMarker .foundingAssumption
        .preferenceOrder .stepOrder .instanceToken .encoding,
   perm .appliedRule .strengthMarker .foundingAssumption
        .stepOrder .preferenceOrder .encoding .instanceToken,
   perm .appliedRule .strengthMarker .foundingAssumption
        .stepOrder .preferenceOrder .instanceToken .encoding,
   perm .appliedRule .foundingAssumption .strengthMarker
        .preferenceOrder .stepOrder .encoding .instanceToken,
   perm .appliedRule .foundingAssumption .strengthMarker
        .preferenceOrder .stepOrder .instanceToken .encoding,
   perm .appliedRule .foundingAssumption .strengthMarker
        .stepOrder .preferenceOrder .encoding .instanceToken,
   perm .appliedRule .foundingAssumption .strengthMarker
        .stepOrder .preferenceOrder .instanceToken .encoding,
   perm .foundingAssumption .strengthMarker .appliedRule
        .preferenceOrder .stepOrder .encoding .instanceToken,
   perm .foundingAssumption .strengthMarker .appliedRule
        .preferenceOrder .stepOrder .instanceToken .encoding,
   perm .foundingAssumption .strengthMarker .appliedRule
        .stepOrder .preferenceOrder .encoding .instanceToken,
   perm .foundingAssumption .strengthMarker .appliedRule
        .stepOrder .preferenceOrder .instanceToken .encoding,
   perm .foundingAssumption .appliedRule .strengthMarker
        .preferenceOrder .stepOrder .encoding .instanceToken,
   perm .foundingAssumption .appliedRule .strengthMarker
        .preferenceOrder .stepOrder .instanceToken .encoding,
   perm .foundingAssumption .appliedRule .strengthMarker
        .stepOrder .preferenceOrder .encoding .instanceToken,
   perm .foundingAssumption .appliedRule .strengthMarker
        .stepOrder .preferenceOrder .instanceToken .encoding] := rfl

theorem aut_without_stack_card : autNoStack.length = 24 := rfl

/-- **WITH THE GROUNDING ORDER: FOUR.** The group is Z₂ × Z₂, the Klein
    four-group: swap Priorities with Process, swap Structure with Circumstances,
    independently. The assertive block is now rigid. -/
theorem aut_with_stack :
    autWithStack =
  [perm .strengthMarker .appliedRule .foundingAssumption
        .preferenceOrder .stepOrder .encoding .instanceToken,
   perm .strengthMarker .appliedRule .foundingAssumption
        .preferenceOrder .stepOrder .instanceToken .encoding,
   perm .strengthMarker .appliedRule .foundingAssumption
        .stepOrder .preferenceOrder .encoding .instanceToken,
   perm .strengthMarker .appliedRule .foundingAssumption
        .stepOrder .preferenceOrder .instanceToken .encoding] := rfl

theorem aut_with_stack_card : autWithStack.length = 4 := rfl

/-- The grounding order costs a factor of six, and the six is exactly the
    assertive block's S₃. -/
theorem stack_order_costs_six : autNoStack.length = 6 * autWithStack.length := rfl

/-- Duplicate-freeness as a `Bool`, so the check below stays a kernel
    computation and costs no axioms. -/
def nodupSites : List Site → Bool
  | []      => true
  | s :: rest => !rest.contains s && nodupSites rest

/-- Every table in either group is a genuine permutation of the eleven sites:
    length eleven, duplicate-free, and hitting every site. So requiring only
    injectivity in `StructurePreserving` did not let a non-bijection through —
    the maps the enumeration returns are onto as well as one-to-one. -/
theorem aut_tables_are_permutations :
    (autNoStack.all (fun t => t.length == 11) &&
     autNoStack.all nodupSites &&
     autNoStack.all (fun t => Site.all.all (fun s => t.contains s)) &&
     autWithStack.all (fun t => t.length == 11) &&
     autWithStack.all nodupSites &&
     autWithStack.all (fun t => Site.all.all (fun s => t.contains s))) = true := rfl

/-! #### Completeness: nothing else survives

The 432-branch case bash. Each branch either exhibits the table in the group or
dies on injectivity, and there is nothing else it could do. -/

/-- **NO OTHER PERMUTATION SURVIVES (no grounding order).** Every
    structure-preserving map's table is one of the twenty-four. -/
theorem aut_without_stack_complete {f : Site → Site} (h : StructurePreserving f) :
    autNoStack.contains (Site.all.map f) = true := by
  have hfc : f .factContent = .factContent :=
    allowed_singleton (Or.inl rfl) (sp_mem_allowed h _)
  have hdc : f .directiveContent = .directiveContent :=
    allowed_singleton (Or.inr (Or.inl rfl)) (sp_mem_allowed h _)
  have hdl : f .declarationContent = .declarationContent :=
    allowed_singleton (Or.inr (Or.inr (Or.inl rfl))) (sp_mem_allowed h _)
  have hrg : f .register = .register :=
    allowed_singleton (Or.inr (Or.inr (Or.inr rfl))) (sp_mem_allowed h _)
  show autNoStack.contains
      [f .factContent, f .strengthMarker, f .directiveContent, f .declarationContent,
       f .preferenceOrder, f .stepOrder, f .appliedRule, f .foundingAssumption,
       f .encoding, f .register, f .instanceToken] = true
  rw [hfc, hdc, hdl, hrg]
  rcases allowed_assertiveDepth (Or.inl rfl)
    (sp_mem_allowed h .strengthMarker) with h₁ | h₁ | h₁ <;>
  rcases allowed_assertiveDepth (Or.inr (Or.inl rfl))
    (sp_mem_allowed h .appliedRule) with h₂ | h₂ | h₂ <;>
  rcases allowed_assertiveDepth (Or.inr (Or.inr rfl))
    (sp_mem_allowed h .foundingAssumption) with h₃ | h₃ | h₃ <;>
  rcases allowed_directiveDepth (Or.inl rfl)
    (sp_mem_allowed h .preferenceOrder) with h₄ | h₄ <;>
  rcases allowed_directiveDepth (Or.inr rfl)
    (sp_mem_allowed h .stepOrder) with h₅ | h₅ <;>
  rcases allowed_carrierDepth (Or.inl rfl)
    (sp_mem_allowed h .encoding) with h₆ | h₆ <;>
  rcases allowed_carrierDepth (Or.inr rfl)
    (sp_mem_allowed h .instanceToken) with h₇ | h₇ <;>
  rw [h₁, h₂, h₃, h₄, h₅, h₆, h₇] <;>
  first
    | rfl
    | exact absurd (h.injective _ _ (h₁.trans h₂.symm)) (by decide)
    | exact absurd (h.injective _ _ (h₁.trans h₃.symm)) (by decide)
    | exact absurd (h.injective _ _ (h₂.trans h₃.symm)) (by decide)
    | exact absurd (h.injective _ _ (h₄.trans h₅.symm)) (by decide)
    | exact absurd (h.injective _ _ (h₆.trans h₇.symm)) (by decide)

/-- **NO OTHER PERMUTATION SURVIVES (with the grounding order).** -/
theorem aut_with_stack_complete {f : Site → Site} (h : StackPreserving f) :
    autWithStack.contains (Site.all.map f) = true := by
  have hfc : f .factContent = .factContent :=
    allowedStack_singleton (Or.inl rfl) (stp_mem_allowedStack h _)
  have hsm : f .strengthMarker = .strengthMarker :=
    allowedStack_singleton (Or.inr (Or.inl rfl)) (stp_mem_allowedStack h _)
  have har : f .appliedRule = .appliedRule :=
    allowedStack_singleton (Or.inr (Or.inr (Or.inl rfl))) (stp_mem_allowedStack h _)
  have hfa : f .foundingAssumption = .foundingAssumption :=
    allowedStack_singleton (Or.inr (Or.inr (Or.inr (Or.inl rfl)))) (stp_mem_allowedStack h _)
  have hdc : f .directiveContent = .directiveContent :=
    allowedStack_singleton (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl rfl)))))
      (stp_mem_allowedStack h _)
  have hdl : f .declarationContent = .declarationContent :=
    allowedStack_singleton (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl rfl))))))
      (stp_mem_allowedStack h _)
  have hrg : f .register = .register :=
    allowedStack_singleton (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr rfl))))))
      (stp_mem_allowedStack h _)
  show autWithStack.contains
      [f .factContent, f .strengthMarker, f .directiveContent, f .declarationContent,
       f .preferenceOrder, f .stepOrder, f .appliedRule, f .foundingAssumption,
       f .encoding, f .register, f .instanceToken] = true
  rw [hfc, hsm, har, hfa, hdc, hdl, hrg]
  rcases allowedStack_directiveDepth (Or.inl rfl)
    (stp_mem_allowedStack h .preferenceOrder) with h₄ | h₄ <;>
  rcases allowedStack_directiveDepth (Or.inr rfl)
    (stp_mem_allowedStack h .stepOrder) with h₅ | h₅ <;>
  rcases allowedStack_carrierDepth (Or.inl rfl)
    (stp_mem_allowedStack h .encoding) with h₆ | h₆ <;>
  rcases allowedStack_carrierDepth (Or.inr rfl)
    (stp_mem_allowedStack h .instanceToken) with h₇ | h₇ <;>
  rw [h₄, h₅, h₆, h₇] <;>
  first
    | rfl
    | exact absurd (h.toStructurePreserving.injective _ _ (h₄.trans h₅.symm)) (by decide)
    | exact absurd (h.toStructurePreserving.injective _ _ (h₆.trans h₇.symm)) (by decide)

/-! #### Attainment: the bound is not slack

An upper bound on a symmetry group is worth little on its own — the group could
be trivial and the bound would still hold. So the twenty-four are exhibited: seven
concrete maps, and the composites that generate the rest. -/

/-- Confidence ↔ Model. -/
def swapMarkerApplied : Site → Site
  | .strengthMarker => .appliedRule
  | .appliedRule    => .strengthMarker
  | s               => s

/-- Confidence ↔ Premises. -/
def swapMarkerFounding : Site → Site
  | .strengthMarker     => .foundingAssumption
  | .foundingAssumption => .strengthMarker
  | s                   => s

/-- Model ↔ Premises. -/
def swapAppliedFounding : Site → Site
  | .appliedRule        => .foundingAssumption
  | .foundingAssumption => .appliedRule
  | s                   => s

/-- Confidence → Model → Premises → Confidence. -/
def rotAssertive : Site → Site
  | .strengthMarker     => .appliedRule
  | .appliedRule        => .foundingAssumption
  | .foundingAssumption => .strengthMarker
  | s                   => s

/-- The inverse rotation — exhibited rather than derived, so that the
    bijectivity of `rotAssertive` is witnessed by a map and not by an appeal to
    finiteness. -/
def rotAssertiveInv : Site → Site
  | .strengthMarker     => .foundingAssumption
  | .foundingAssumption => .appliedRule
  | .appliedRule        => .strengthMarker
  | s                   => s

/-- Priorities ↔ Process. -/
def swapPreferenceStep : Site → Site
  | .preferenceOrder => .stepOrder
  | .stepOrder       => .preferenceOrder
  | s                => s

/-- Structure ↔ Circumstances. -/
def swapEncodingToken : Site → Site
  | .encoding      => .instanceToken
  | .instanceToken => .encoding
  | s              => s

theorem rotAssertive_inv (s : Site) : rotAssertiveInv (rotAssertive s) = s := by cases s <;> rfl

theorem rotAssertive_order_three (s : Site) :
    rotAssertive (rotAssertive (rotAssertive s)) = s := by cases s <;> rfl

theorem swapPreferenceStep_involutive (s : Site) :
    swapPreferenceStep (swapPreferenceStep s) = s := by cases s <;> rfl

theorem swapEncodingToken_involutive (s : Site) :
    swapEncodingToken (swapEncodingToken s) = s := by cases s <;> rfl

theorem sp_id : StructurePreserving id where
  injective := fun _ _ h => h
  force_eq := fun _ => rfl
  surface_eq := fun _ => rfl

/-- The structure-preserving maps are closed under composition — so the group
    really is a group, and the twenty-four composites below are all in it. -/
theorem sp_comp {f g : Site → Site} (hf : StructurePreserving f) (hg : StructurePreserving g) :
    StructurePreserving (f ∘ g) where
  injective := fun s t h => hg.injective s t (hf.injective _ _ h)
  force_eq := fun s => (hf.force_eq (g s)).trans (hg.force_eq s)
  surface_eq := fun s => (hf.surface_eq (g s)).trans (hg.surface_eq s)

theorem sp_swapMarkerApplied : StructurePreserving swapMarkerApplied where
  injective := by intro s t hh; cases s <;> cases t <;> first | rfl | exact absurd hh (by decide)
  force_eq := by intro s; cases s <;> rfl
  surface_eq := by intro s; cases s <;> rfl

theorem sp_swapMarkerFounding : StructurePreserving swapMarkerFounding where
  injective := by intro s t hh; cases s <;> cases t <;> first | rfl | exact absurd hh (by decide)
  force_eq := by intro s; cases s <;> rfl
  surface_eq := by intro s; cases s <;> rfl

theorem sp_swapAppliedFounding : StructurePreserving swapAppliedFounding where
  injective := by intro s t hh; cases s <;> cases t <;> first | rfl | exact absurd hh (by decide)
  force_eq := by intro s; cases s <;> rfl
  surface_eq := by intro s; cases s <;> rfl

theorem sp_rotAssertive : StructurePreserving rotAssertive where
  injective := by intro s t hh; cases s <;> cases t <;> first | rfl | exact absurd hh (by decide)
  force_eq := by intro s; cases s <;> rfl
  surface_eq := by intro s; cases s <;> rfl

theorem sp_rotAssertiveInv : StructurePreserving rotAssertiveInv where
  injective := by intro s t hh; cases s <;> cases t <;> first | rfl | exact absurd hh (by decide)
  force_eq := by intro s; cases s <;> rfl
  surface_eq := by intro s; cases s <;> rfl

theorem sp_swapPreferenceStep : StructurePreserving swapPreferenceStep where
  injective := by intro s t hh; cases s <;> cases t <;> first | rfl | exact absurd hh (by decide)
  force_eq := by intro s; cases s <;> rfl
  surface_eq := by intro s; cases s <;> rfl

theorem sp_swapEncodingToken : StructurePreserving swapEncodingToken where
  injective := by intro s t hh; cases s <;> cases t <;> first | rfl | exact absurd hh (by decide)
  force_eq := by intro s; cases s <;> rfl
  surface_eq := by intro s; cases s <;> rfl

/-- The six assertive-block permutations, as maps, in the order
    `assertiveTriples` lists their tables. -/
def assertiveMaps : List (Site → Site) :=
  [id, swapAppliedFounding, swapMarkerApplied, rotAssertive, rotAssertiveInv, swapMarkerFounding]

/-- The two directive-block permutations, as maps. -/
def directiveMaps : List (Site → Site) := [id, swapPreferenceStep]

/-- The two carrier-block permutations, as maps. -/
def carrierMaps : List (Site → Site) := [id, swapEncodingToken]

theorem assertiveMaps_sp {a : Site → Site} (h : a ∈ assertiveMaps) : StructurePreserving a := by
  cases h with
  | head => exact sp_id
  | tail _ h => cases h with
    | head => exact sp_swapAppliedFounding
    | tail _ h => cases h with
      | head => exact sp_swapMarkerApplied
      | tail _ h => cases h with
        | head => exact sp_rotAssertive
        | tail _ h => cases h with
          | head => exact sp_rotAssertiveInv
          | tail _ h => cases h with
            | head => exact sp_swapMarkerFounding
            | tail _ h => cases h

theorem directiveMaps_sp {d : Site → Site} (h : d ∈ directiveMaps) : StructurePreserving d := by
  cases h with
  | head => exact sp_id
  | tail _ h => cases h with
    | head => exact sp_swapPreferenceStep
    | tail _ h => cases h

theorem carrierMaps_sp {c : Site → Site} (h : c ∈ carrierMaps) : StructurePreserving c := by
  cases h with
  | head => exact sp_id
  | tail _ h => cases h with
    | head => exact sp_swapEncodingToken
    | tail _ h => cases h

/-- **EVERY LISTED TABLE IS REALISED.** The twenty-four tables are, table for
    table and in order, the tables of the twenty-four composites `a ∘ d ∘ c`. So
    the enumeration is the group and not merely a bound on it. -/
theorem aut_without_stack_realised :
    autNoStack =
      assertiveMaps.flatMap fun a => directiveMaps.flatMap fun d => carrierMaps.map fun c =>
        Site.all.map (a ∘ d ∘ c) := rfl

/-- And every one of those composites is structure-preserving. -/
theorem aut_composite_sp {a d c : Site → Site}
    (ha : a ∈ assertiveMaps) (hd : d ∈ directiveMaps) (hc : c ∈ carrierMaps) :
    StructurePreserving (a ∘ d ∘ c) :=
  sp_comp (assertiveMaps_sp ha) (sp_comp (directiveMaps_sp hd) (carrierMaps_sp hc))

/-- The same for the grounding-order group: its four tables are the four
    composites of the two off-stack swaps. -/
theorem aut_with_stack_realised :
    autWithStack =
      directiveMaps.flatMap fun d => carrierMaps.map fun c => Site.all.map (d ∘ c) := rfl

theorem stp_id : StackPreserving id where
  toStructurePreserving := sp_id
  height_eq := fun _ => rfl

theorem stp_swapPreferenceStep : StackPreserving swapPreferenceStep where
  toStructurePreserving := sp_swapPreferenceStep
  height_eq := by intro s; cases s <;> rfl

theorem stp_swapEncodingToken : StackPreserving swapEncodingToken where
  toStructurePreserving := sp_swapEncodingToken
  height_eq := by intro s; cases s <;> rfl

theorem stp_comp {f g : Site → Site} (hf : StackPreserving f) (hg : StackPreserving g) :
    StackPreserving (f ∘ g) where
  toStructurePreserving := sp_comp hf.toStructurePreserving hg.toStructurePreserving
  height_eq := fun s => (hf.height_eq (g s)).trans (hg.height_eq s)

/-- **THE BREAKING FIELD, ISOLATED.** `swapMarkerApplied` — interchange
    Confidence with Model — is a symmetry of force and surface, and is not a
    symmetry once `Stack.lean`'s grounding order is required. That single map is
    the whole difference between 24 and 4: the assertive block's freedom is not
    an accident of the enumeration, it is what the grounding order is for. -/
theorem stack_order_breaks_assertive_symmetry :
    StructurePreserving swapMarkerApplied ∧ ¬ StackPreserving swapMarkerApplied := by
  refine ⟨sp_swapMarkerApplied, fun h => ?_⟩
  exact absurd (h.height_eq .strengthMarker) (by decide)

/-- The two survivors are survivors for a reason a reader can check: neither
    orbit is on the ladder at all. -/
theorem surviving_swaps_are_off_stack :
    (Site.preferenceOrder.stackHeight = none ∧ Site.stepOrder.stackHeight = none) ∧
    (Site.encoding.stackHeight = none ∧ Site.instanceToken.stackHeight = none) :=
  ⟨⟨rfl, rfl⟩, ⟨rfl, rfl⟩⟩

/-- **THE SURFACES ARE RIGID.** No automorphism moves any block's gross face,
    with or without the grounding order — so the measured gross four are not
    interchangeable with anything, and `Surface.lean`'s roster is not a labelling
    convention that a relabelling could undo. -/
theorem surfaces_are_rigid {f : Site → Site} (h : StructurePreserving f) (b : Block) :
    f (Block.surface b) = Block.surface b := by
  cases b
  · exact allowed_singleton (Or.inl rfl) (sp_mem_allowed h _)
  · exact allowed_singleton (Or.inr (Or.inl rfl)) (sp_mem_allowed h _)
  · exact allowed_singleton (Or.inr (Or.inr (Or.inl rfl))) (sp_mem_allowed h _)
  · exact allowed_singleton (Or.inr (Or.inr (Or.inr rfl))) (sp_mem_allowed h _)

/-! ### §2 The broken fit-conjugation

The natural thing to try next is to enlarge the symmetry so that it mixes the
blocks — to ask whether the assertive apparatus and the directive apparatus are
two copies of one thing wearing different clothes. They are not, and the proof is
a counting argument. -/

/-- The conjugation being tested: swap the assertive and directive blocks, leave
    declaration and carrier alone. -/
def Block.conj : Block → Block
  | .assertive => .directive
  | .directive => .assertive
  | b          => b

/-- The conjugation is an involution on blocks, and it does move something —
    so what fails below is not that the candidate symmetry is trivial. -/
theorem conj_involutive (b : Block) : b.conj.conj = b := by cases b <;> rfl

theorem conj_moves_assertive : Block.assertive.conj ≠ Block.assertive := by decide

/-- The arithmetic that kills it: the assertive block holds four sites, the
    directive block three. `Surface.lean`'s `block_cards` is where the 4 and the
    3 come from. -/
theorem assertive_directive_cards_differ :
    (Block.sites .assertive).length ≠ (Block.sites .directive).length := by decide

/-- Which sites sit in the directive block — the three-element target the four
    assertive sites would have to fit into. -/
theorem block_directive_narrow {x : Site} (h : x.block = Block.directive) :
    x = .directiveContent ∨ x = .preferenceOrder ∨ x = .stepOrder := by
  cases x <;>
    first
      | exact Or.inl rfl
      | exact Or.inr (Or.inl rfl)
      | exact Or.inr (Or.inr rfl)
      | exact absurd h (by decide)

/-- **NO FIT-CONJUGATION.** There is no injection of the site model into itself
    inducing the assertive/directive swap on blocks. Note the strength: the
    hypothesis is not `StructurePreserving` but bare injectivity plus the block
    swap, so the failure is not an artifact of the symmetry's other components —
    it is cardinality, four into three, and no refinement of the definition of
    "symmetry" can repair it.

    THE FORK THIS OPENS, both prongs, because the second is a commitment and not
    a result:

    (a) The missing site would be a directive STRENGTH marker — the deontic
        counterpart of `strengthMarker`, the thing that stands to "you must" as
        hedging stands to "it is". If that site exists, the site model is missing
        a constructor and the taxonomy is missing a kind. That is precisely the
        kill the kinds-from-sites derivation stakes: `Generator.lean`'s eleven is
        THEOREM-GIVEN-MODEL, and a twelfth site retires the theorem's premise
        rather than its proof.

    (b) The model's own answer is that there is no such site, and the reason is a
        distinction and not a convenience: epistemic strength MODULATES a claim
        without changing its truth-conditions ("probably p" and "p" are true
        together), whereas deontic strength changes COMPLIANCE-conditions ("you
        must φ" and "you should φ" are complied with differently). A change of
        deontic strength is therefore a change of what is required — content,
        filed under Rules — not a modulation, and it already has a site:
        `directiveContent`.

    (b) IS A MODEL COMMITMENT AND IT IS NOT PROVED HERE. Nothing below tests it.
        Its empirical test is a panel item pairing must/should variants against
        matched hedged/unhedged assertive variants and asking whether annotators
        route the deontic pair to Rules (commitment (b) holds) or to Confidence
        (a twelfth site is wanted); it is unrun. What the theorem establishes is
        narrower and exact: on the enumeration as it stands, the conjugation
        fails, and it fails for a reason that no amount of re-reading the
        existing eleven sites can fix. -/
theorem no_fit_conjugation :
    ¬ ∃ f : Site → Site,
        (∀ s t : Site, f s = f t → s = t) ∧ (∀ s : Site, (f s).block = (s.block).conj) := by
  rintro ⟨f, hinj, hb⟩
  have b₁ : (f .factContent).block = Block.directive := hb .factContent
  have b₂ : (f .strengthMarker).block = Block.directive := hb .strengthMarker
  have b₃ : (f .appliedRule).block = Block.directive := hb .appliedRule
  have b₄ : (f .foundingAssumption).block = Block.directive := hb .foundingAssumption
  rcases block_directive_narrow b₁ with h₁ | h₁ | h₁ <;>
  rcases block_directive_narrow b₂ with h₂ | h₂ | h₂ <;>
  rcases block_directive_narrow b₃ with h₃ | h₃ | h₃ <;>
  rcases block_directive_narrow b₄ with h₄ | h₄ | h₄ <;>
  first
    | exact absurd (hinj _ _ (h₁.trans h₂.symm)) (by decide)
    | exact absurd (hinj _ _ (h₁.trans h₃.symm)) (by decide)
    | exact absurd (hinj _ _ (h₁.trans h₄.symm)) (by decide)
    | exact absurd (hinj _ _ (h₂.trans h₃.symm)) (by decide)
    | exact absurd (hinj _ _ (h₂.trans h₄.symm)) (by decide)
    | exact absurd (hinj _ _ (h₃.trans h₄.symm)) (by decide)

/-- The weaker statement, for completeness: the symmetries computed in §1 do not
    conjugate either, and for the cheap reason — they preserve the block outright
    (`structurePreserving_preserves_block`), and the conjugation does not. -/
theorem structurePreserving_never_conjugates {f : Site → Site} (h : StructurePreserving f) :
    ¬ ∀ s : Site, (f s).block = (s.block).conj := by
  intro hc
  have := (structurePreserving_preserves_block h .factContent).symm.trans (hc .factContent)
  exact absurd this (by decide)

/-! ### §3 Kind is the frame scalar

The Noether-shaped statement, and the one place this file connects to a
measurement rather than to another theorem. Nothing is proved anew here: the
three components already exist, in `WrongKind.lean` and `Generator.lean`. What is
added is the single name under which they say one thing. -/

/-- A site-level reading is a FRAME SCALAR when supplying a different frame — a
    different account of what survives to be re-read — cannot move its verdict. -/
def SiteFrameInvariant (P : Site → Frame → Prop) : Prop := ∀ s f₁ f₂, P s f₁ ↔ P s f₂

/-- Every kind assignment is a frame scalar, and trivially so: `Site.kind` has no
    frame argument to be moved by. The triviality is the content — it is what
    "the label is intrinsic to the site" means, spelled out. -/
theorem kind_is_frame_scalar (k : ChoiceKind) : SiteFrameInvariant (fun s _ => s.kind = k) :=
  fun _ _ _ => Iff.rfl

/-- **KINDS ARE FRAME SCALARS; RECORD IS NOT.** Three existing results under one
    name: every artifact-only discriminator is frame-invariant, repairability
    provably is not artifact-only, and no site generates Record. Read in the
    borrowed vocabulary: frame supply is a direction along which the model is
    symmetric, kind is the quantity conserved along it, and Record is the one
    reading that fails to be conserved — which is exactly why it is a relation
    and not a kind.

    THE MEASURED FACE, credited and NOT proved here. The panel study
    (`PLANE_RESULTS.md`, 5,994 judgments) found the labels coordinate-flat at
    p < 0.01, κ = 0.687 — the empirical shadow of the invariance stated below,
    and the reason the invariance is worth naming rather than dismissing as a
    typing artifact. It is a measurement about CLASSIFIERS. It is not evidence
    for the theorem, the theorem is not evidence for it, and neither appears in
    the other's basis. The study's own retraction of `designDependent` is carried
    in `WrongKind.lean`, not re-litigated here. -/
theorem kinds_are_frame_scalars :
    (∀ g : String → Prop, FrameInvariant (fun a _ => g a)) ∧
    (¬ ∃ g : String → Prop, ∀ a f, Repairable a f ↔ g a) ∧
    (∀ s : Site, s.kind ≠ .testimonial) :=
  ⟨frameInvariant_of_artifact_only, repairable_does_not_factor, record_not_site_generated⟩

/-- And the two halves are about the same object: Record is the only one of the
    twelve labels claimed frame-mobile, and it is the only one with no site. -/
theorem record_is_the_only_non_scalar :
    (WrongKind.all.filter (·.frameDependent)) = [WrongKind.testimonial] := by decide

/-! ### §4 The conversion algebra: mention is a projection, not a symmetry

The last move. `Surface.lean` proves that each force block wears its own content
kind on its face. MENTION is the operation that takes a commitment and reports it
instead of making it — "the policy requires φ" instead of "φ is required" — and
under it those three faces stop being three. That is not a symmetry: it is not
injective, and it cannot be, which is what makes it worth naming separately. In
the borrowed vocabulary it is a CONTRACTION rather than an automorphism: a
degenerate limit in which distinctions are lost and cannot be recovered. -/

/-- **THE MENTION MAP.** Each force block's surface goes to the assertive
    surface; everything else stays. To mention a requirement or a declaration is
    to claim that it holds, so the content site moves to `factContent`; the
    apparatus (how strongly, in what order, under what rule) and the carriers
    (encoding, register, instance token) are untouched, because mentioning
    changes what is being done with a commitment, not how it is written.

    THE EXPOSURE IN THAT DEFINITION, stated here rather than left for a reader to
    find. Moving `directiveContent` while leaving `preferenceOrder` and
    `stepOrder` where they are ORPHANS the directive apparatus: the block keeps
    its depths and loses its face. A critic who reads mention as collapsing a
    whole block — apparatus and all — onto the assertive block gets a different
    map, and every count below moves with it. The orphaning is not a defect to be
    tidied away, though: it is the reason this operation is a projection and not
    a symmetry, since a symmetry could not have left a block faceless. -/
def mentionTarget : Site → Site
  | .directiveContent   => .factContent
  | .declarationContent => .factContent
  | s                   => s

/-- The map is exactly the collapse of `Surface.lean`'s three forced surfaces
    onto the assertive one — stated against `Block.surface` so the connection is
    a theorem and not a resemblance. -/
theorem mention_collapses_force_surfaces (f : Force) :
    mentionTarget (Block.surface (Block.ofForce (some f))) = Site.factContent := by
  cases f <;> rfl

/-- **IDEMPOTENT.** Mentioning a mention is a mention — there is no second-order
    mention site, exactly as `Stack.lean`'s modulation generates no second-order
    hedge. -/
theorem mention_idempotent (s : Site) : mentionTarget (mentionTarget s) = mentionTarget s := by
  cases s <;> rfl

/-- **NOT INJECTIVE.** Rules and Identity have the same mention. -/
theorem mention_not_injective :
    ∃ s t : Site, s ≠ t ∧ mentionTarget s = mentionTarget t :=
  ⟨.directiveContent, .declarationContent, by decide, rfl⟩

/-- **HENCE NOT A SYMMETRY.** `mentionTarget` is not in either group of §1, and
    not because of some fine structural component — it fails the first one. -/
theorem mention_not_structurePreserving : ¬ StructurePreserving mentionTarget := by
  intro h
  exact absurd (h.injective .directiveContent .declarationContent rfl) (by decide)

/-- It fails force-commutation too, which is the same fact seen from the other
    side: mention is what turns a requirement into a claim. -/
theorem mention_changes_force :
    (mentionTarget Site.directiveContent).force ≠ Site.directiveContent.force := by decide

/-- **THE CARRIERS ARE INERT.** The carrier block is exactly its own preimage:
    no carrier site is moved, and no non-carrier site is moved into one. The
    vehicle layer does not participate in the use/mention distinction at all. -/
theorem carrier_inert_under_mention (s : Site) :
    ((mentionTarget s).block == Block.carrier) = (s.block == Block.carrier) := by
  cases s <;> rfl

theorem mention_fixes_carriers {s : Site} (h : s.block = Block.carrier) :
    mentionTarget s = s := by
  cases s <;> first | rfl | exact absurd h (by decide)

/-- **WHAT THE PROJECTION COSTS, exactly.** Three sites share one image, and
    their kinds are Facts, Rules and Identity — the three forced surfaces of
    `Surface.lean` read as one.

    THE MEASURED FACE, credited and not proved here: this is the shape of the
    wild confusion the panel study reports. Part D's absorptions are Facts→Rules
    and Facts→Identity, and they are the two edges of this fibre;
    `Stack.lean`'s header notes that both are OFF its stack, which is right and
    is the complementary half — the stack explains the Premises/Facts and
    Model/Facts confusions, and this fibre explains the other two. Neither
    explanation is evidence for the other, and the measurement is evidence for
    neither: annotators blurring a boundary is a fact about annotators. -/
theorem mention_fibre_over_facts :
    Site.all.filter (fun s => mentionTarget s == Site.factContent) =
      [.factContent, .directiveContent, .declarationContent] := rfl

theorem mention_fibre_kinds_plain :
    (Site.all.filter (fun s => mentionTarget s == Site.factContent)).map (fun s => s.kind.plain) =
      ["Facts", "Rules", "Identity"] := rfl

/-- **THE RANK OF THE PROJECTION: eleven to nine.** Nine sites are fixed, and by
    idempotence the fixed points are the image, so mention loses exactly two
    dimensions of the site model. It is a projection onto the assertive surface,
    and the two lost dimensions are the other two forces' faces. -/
theorem mention_fixed_points :
    Site.all.filter (fun s => mentionTarget s == s) =
      [.factContent, .strengthMarker, .preferenceOrder, .stepOrder, .appliedRule,
       .foundingAssumption, .encoding, .register, .instanceToken] := rfl

theorem mention_rank : (Site.all.filter (fun s => mentionTarget s == s)).length = 9 := rfl

/-- The fixed points really are the image, so counting one counts the other.
    Forwards is `mention_idempotent`; backwards is that a fixed point is its own
    preimage. -/
theorem mention_fixed_iff_image (s : Site) :
    (mentionTarget s == s) = Site.all.any (fun t => mentionTarget t == s) := by
  cases s <;> rfl

theorem mention_loses_two :
    Site.all.length - (Site.all.filter (fun s => mentionTarget s == s)).length = 2 := rfl

/-! ### What this file does NOT prove — read before quoting a number from it

**The groups are groups OF THE MODEL.** 24 and 4 are counts of permutations of an
eleven-element inductive type under conditions stated in this file. They are not
statements about how much freedom a taxonomy of change has, and they become such
statements only through `Generator.lean`'s adequacy question, which no theorem
here touches.

**"S₃ × Z₂ × Z₂" and "the Klein four-group" are READINGS of the enumeration, not
mechanized isomorphisms.** There is no `Group` instance anywhere in this file and
no isomorphism is constructed. What IS mechanized is strictly: the twenty-four
tables (`aut_without_stack`), that they are exactly the tables of the twenty-four
composites `a ∘ d ∘ c` of the three factors' maps (`aut_without_stack_realised`),
that every such composite is structure-preserving (`aut_composite_sp`), that
structure-preserving maps compose (`sp_comp`) and include the identity (`sp_id`),
and that nothing else survives (`aut_without_stack_complete`). Those five facts
are what a reader should quote. The group-theoretic name is a convenience for
saying them in one breath, and it is doing no work that the five are not.

**The grounding order is a modelling commitment, so the 4 inherits its status.**
`Stack.lean` says in its own header that the ordering is a definition, not a
discovery, and states the kill: exhibit a change whose strength marking composes
into a genuinely new site. If that kill fires, the ladder is wrong about the
world and the honest automorphism group is 24, not 4. Both numbers are stated
above for exactly this reason — which of the two is the real one depends on a
commitment that is held openly and can fail.

**`Surface.lean`'s one modelling choice propagates here.** Taking `register`
rather than `encoding` as the carrier surface is that file's declared free
choice. Under the rival reading the carrier orbit is {register, instanceToken}
instead of {encoding, instanceToken} — the group is still Z₂ there, the counts 24
and 4 are unchanged, and only the ROSTER of what swaps with what moves. Same
robustness, and same exposure, as `gross_four`.

**Neither measurement cited above is support for anything proved here.** The
coordinate-flatness result (§3) and the wild-confusion result (§4) are
measurements about classifiers, credited where they are relevant and quoted in no
claim's basis. A theorem about an inductive type cannot be confirmed by a panel,
and a panel cannot be confirmed by a theorem.

**And the physics is a playbook, not a warrant.** The header names four borrowed
moves and fences them; the fence is repeated here because this is where a reader
who skipped the header will be tempted. Nothing above is evidence for any
analogy, and the analogies are not evidence for anything above. They are in
`scratchpad/N18_BRIDGE_NOTE.md` to be attacked. -/

end CIRISOntology.Core
