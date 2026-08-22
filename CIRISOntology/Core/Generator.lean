/-
CIRISOntology.Core.Generator — the periodic-table move: derive the kinds from a
model of the artifact, so that exhaustiveness becomes a theorem GIVEN THE MODEL.

THE HONEST FRAME, stated before the definitions so it cannot be lost. Chemistry's
exhaustiveness proof required two halves: a generator (atomic number) and the
world's continued agreement to embed in it (no element without an integer Z).
This file is the first half only. The second is the ecological challenge
(`scratchpad/ECOLOGICAL_PREREG.md`): the measured NO-FIT rate on wild changes IS
the model's embedding-failure rate. Everything below is therefore
THEOREM-GIVEN-MODEL, and the question "are there more kinds?" does not vanish —
it MOVES to "is this model adequate?", which is answerable by measurement. That
relocation is the entire value: it is what made chemistry's question closeable.

CONVERGENT ART (found 2026-08-22, credited per house rule — hits, not strikes).
Stiles' Verbal Response Modes (1981; *Describing Talk*, 1992) is the closest
published precedent for this file's construction: THREE dichotomous principles
(source of experience, frame of reference, focus) generate 2^3 = 8 mutually
exclusive, exhaustive speech modes — a closed taxonomy as the exact image of a
generator, with a measured 64-cell form-x-intent matrix carrying off-diagonal
structure. Independently, Schluter & Theesfeld (2010) measured that ADICO coders
cannot reliably separate strategies/norms/rules — boundary confusion at predicted
kind boundaries, reported there as instrument defect rather than structure. Both
predate this repository; neither runs dynamics on the taxonomy.

NON-CIRCULARITY, the load-bearing worry. If the artifact model were a record
with twelve fields named after the kinds, the "derivation" would be tautology.
The defense is that the components are grounded in literatures older than this
repository — the mapping is DOCUMENTED so it can be attacked:

  * commitments with FORCE — speech-act theory's independently-motivated split
    (Searle 1975, "A Taxonomy of Illocutionary Acts"; Austin 1962):
    assertives (what is claimed true)          -> Facts
    directives (what is required/permitted)    -> Rules
    declarations (what counts as what)         -> Identity
  * graded strength markers on assertions (hedging/evidentiality — a standard
    linguistic category, CoNLL-2010 family)    -> Confidence
  * preference ORDER over outcomes (decision theory's ranking, distinct from
    permission by von Wright's deontic/axiological split) -> Priorities
  * step ORDER (process description)           -> Process
  * the inference rule APPLIED vs asserted (logic's use/mention line) -> Model
  * the serialization/encoding layer (form vs content, machine-readability)
                                               -> Structure
  * the register/presentation wrapper (sociolinguistic register) -> Manner
  * the founding assumptions everything composes over (argumentation theory's
    premises)                                  -> Premises
  * unbound instance details (tokens vs types) -> Circumstances

  The two RELATIONAL classifications do not appear as components, and that
  absence is itself derived structure: Record is a relation to a FRAME and
  Circumstances-as-verdict is a relation to a DESIGN (`repairable_does_not_factor`,
  the claim table). Sites generate the base kinds; READINGS generate the rest.

WHAT THE PRODUCT STRUCTURE BUYS. Because the model is a product of independent
components, "which component changed" is total and single-valued BY CONSTRUCTION
— that is the partition theorem, and its thinness is honest: the mathematical
content is small, and the empirical content (adequacy) is where the risk lives.
Exactly like atomic number: trivial arithmetic, world-historical adequacy.
-/

import CIRISOntology.Core.WrongKind

namespace CIRISOntology.Core

/-- The illocutionary split, from speech-act theory (Searle 1975; Austin 1962).
    Independent prior art: this trichotomy was not carved for our taxonomy. -/
inductive Force
  | assertive    -- claims the world is thus
  | directive    -- requires/permits
  | declarative  -- makes something count as something
  deriving DecidableEq, Repr

/-- A single-site variation of an artifact, as a site in the generator model.
    One constructor per independent component; the constructor IS the site. -/
inductive Site
  /-- an assertive's content changes truth-conditions -/
  | factContent
  /-- a strength/hedging marker on an assertive moves -/
  | strengthMarker
  /-- a directive's permission content changes -/
  | directiveContent
  /-- a declaration's counts-as content changes -/
  | declarationContent
  /-- the preference ORDER over outcomes is permuted -/
  | preferenceOrder
  /-- the step ORDER is permuted -/
  | stepOrder
  /-- the rule APPLIED to derive downstream content is swapped (use, not mention) -/
  | appliedRule
  /-- the founding assumption other components compose over is swapped -/
  | foundingAssumption
  /-- the serialization/encoding is altered -/
  | encoding
  /-- the register/presentation wrapper is altered -/
  | register
  /-- an unbound instance token (not intended invariant) differs -/
  | instanceToken
  deriving DecidableEq, Repr

/-- THE GENERATOR MAP: which kind a change at each site instantiates. -/
def Site.kind : Site → ChoiceKind
  | .factContent        => .empirical
  | .strengthMarker     => .epistemic
  | .directiveContent   => .deontic
  | .declarationContent => .ontological
  | .preferenceOrder    => .axiotic
  | .stepOrder          => .procedural
  | .appliedRule        => .nomological
  | .foundingAssumption => .axiomatic
  | .encoding           => .structural
  | .register           => .pragmatic
  | .instanceToken      => .contingent

/-- All sites. -/
def Site.all : List Site :=
  [.factContent, .strengthMarker, .directiveContent, .declarationContent,
   .preferenceOrder, .stepOrder, .appliedRule, .foundingAssumption,
   .encoding, .register, .instanceToken]

/-- EXHAUSTIVENESS OVER THE MODEL: every site is classified (totality is by
    construction — the map is total — and this pins coverage of the enumeration). -/
theorem every_site_classified (s : Site) : s ∈ Site.all := by
  cases s <;> repeat first | exact List.Mem.head _ | apply List.Mem.tail

/-- THE PARTITION IS EXACTLY THE BASE PLANE PLUS THE MARKER: the image of the
    generator map is the eleven artifact-local kinds — every base kind is
    generated by exactly one site, and `testimonial` is NOT in the image. -/
theorem generator_image :
    Site.all.map Site.kind =
      [.empirical, .epistemic, .deontic, .ontological, .axiotic, .procedural,
       .nomological, .axiomatic, .structural, .pragmatic, .contingent] := rfl

/-- The generator map is INJECTIVE: distinct sites, distinct kinds. Combined
    with `generator_image`, sites and artifact-local kinds are in bijection —
    the kinds are not merely covered but COUNTED by the model. -/
theorem generator_injective : ∀ s t : Site, s.kind = t.kind → s = t := by
  intro s t h
  cases s <;> cases t <;> first | rfl | exact absurd h (by decide)

/-- RECORD IS NOT SITE-GENERATED — and could not be. No constructor of `Site`
    maps to `testimonial`, matching `repairable_does_not_factor`: whether a
    change destroys establishability is not a property of the changed site but
    a relation to the surviving frame. The generator derives the base plane;
    the coordinates derive the rest. This is the 10+1+1 shape appearing as a
    property of the model's IMAGE rather than as a stipulation. -/
theorem record_not_site_generated : ∀ s : Site, s.kind ≠ .testimonial := by
  intro s; cases s <;> decide

/-- And `contingent` IS site-generated (the token/type line gives it a site)
    while its VERDICT remains design-relative per the claim table — the site
    says an instance token differed; whether that is in or out of scope is the
    design's call. The model thus reproduces the asymmetry the disposition
    table found: one relational kind has no site at all, the other has a site
    whose classification awaits a coordinate. -/
theorem contingent_site_exists : Site.instanceToken.kind = .contingent := rfl

end CIRISOntology.Core
