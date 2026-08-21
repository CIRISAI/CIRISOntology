/-
# Generator2 — the recognition-grounded site model, built as the FREEZE-CONSISTENCY CHECK

The frozen registration (scratchpad/RECOGNITION_PREREG.md §T1, as amended by A2/A3) staked
a re-grounding: the eleven artifact-local kinds as sites of RECOGNITION OF STATE AND
TRANSITION POTENTIAL rather than of speech acts. Credited ancestry: Katsuno–Mendelzon 1991
(update vs revision — the world moved vs my information was wrong), Millikan 1995
(pushmi-pullyu representations — the primitive that is both directions at once), Searle
(declaration — recognition that makes-so).

READ THE VERDICT BEFORE READING THE THEOREMS (scratchpad/T1_BLIND/T1_BLIND_VERDICT.md):
T1's PRIMARY IS NULL. Three blind derivation cells (shallow-blind, deep-blind,
deep-contaminated) were run before this file existed; NO blind application of the frozen
recipe reproduces the eleven-site structure from the recognition triple (the deep-blind
cell converges exactly on 2|M|+3 = 9), and the [3,2,0] gap profile encoded below appears
only when the deriver already knows the eleven. THEREFORE: the theorems in this file are
MATHEMATICS ABOUT THE FROZEN TABLE — the eleven CAN be organized as recognition sites, and
that organization is exact, injective, Record-excluding, and isomorphic to the speech-act
generator — and they are NOT evidence that recognition GENERATES the eleven. The
re-grounding stays a wager. The eleven's warrant is empirical (the corpus eigenstructure
and the panel record), not derivational. Two advance predictions of the mode-level story
were confirmed by the blind cells (PP1: Jakobson's image is not eleven; PP2: no blind
Habermas derivation contains a made-so site) — the mode → content-site story has rule-6
support; the depth profile does not.
-/
import CIRISOntology.Core.Generator

namespace CIRISOntology.Core

/-- The three recognition modes (frozen §T1.1). -/
inductive RecognitionMode
  /-- recognition that the world IS thus (KM revision) -/
  | stateRec
  /-- recognition that a transition is available or required (KM update) -/
  | transitionRec
  /-- recognition that MAKES-SO (Searle's declaration; Millikan's double-direction primitive) -/
  | constitution
  deriving DecidableEq, Repr

/-- The eleven recognition sites — THE FROZEN TABLE of §T1.2, verbatim in order.
    (The order deliberately differs from `Site.all`, so the image statement is
    about the set, never a list-order accident.) -/
inductive RSite
  /-- the recognized state itself -/
  | stateContent
  /-- how strongly the state is recognized -/
  | stateStrength
  /-- the recognition-rule APPLIED to reach it -/
  | stateRule
  /-- the founding given the recognition rests on -/
  | stateGiven
  /-- the recognized transition constraint -/
  | transitionContent
  /-- the ordering over recognized outcomes -/
  | outcomeOrder
  /-- the ordering over recognized steps -/
  | stepOrder
  /-- the constituted status -/
  | constitutedStatus
  /-- which encoding carries the recognition -/
  | carrierEncoding
  /-- how the recognition is presented -/
  | carrierPresentation
  /-- which unbound instance carries it -/
  | carrierToken
  deriving DecidableEq, Repr

/-- The frozen kind map (§T1.2, column `RSite.kind`). -/
def RSite.kind : RSite → WrongKind
  | RSite.stateContent => WrongKind.empirical
  | RSite.stateStrength => WrongKind.epistemic
  | RSite.stateRule => WrongKind.nomological
  | RSite.stateGiven => WrongKind.axiomatic
  | RSite.transitionContent => WrongKind.deontic
  | RSite.outcomeOrder => WrongKind.axiotic
  | RSite.stepOrder => WrongKind.procedural
  | RSite.constitutedStatus => WrongKind.ontological
  | RSite.carrierEncoding => WrongKind.structural
  | RSite.carrierPresentation => WrongKind.pragmatic
  | RSite.carrierToken => WrongKind.contingent

/-- All recognition sites, in the frozen order. -/
def RSite.all : List RSite :=
  [.stateContent, .stateStrength, .stateRule, .stateGiven,
   .transitionContent, .outcomeOrder, .stepOrder, .constitutedStatus,
   .carrierEncoding, .carrierPresentation, .carrierToken]

/-- T1-VOID-1's mechanical check: eleven constructors, no more, no fewer. -/
theorem rsite_all_length : RSite.all.length = 11 := rfl

/-- Every recognition site is enumerated. -/
theorem every_rsite_classified (s : RSite) : s ∈ RSite.all := by
  cases s <;> repeat first | exact List.Mem.head _ | apply List.Mem.tail

/-- THE IMAGE, as a multiset (MINOR-1: a permutation-strength statement, never
    a list-order accident): every kind occurs in the recognition sites' image
    exactly as often as in the speech-act sites' image — the same eleven
    artifact-local kinds, each once, and the Record's kind zero times in both.
    Stated by counts so the proof is `rfl` per kind and axiom-free. -/
theorem generator2_image :
    ∀ k : WrongKind,
      (RSite.all.map RSite.kind).count k = (Site.all.map Site.kind).count k := by
  intro k; cases k <;> rfl

/-- Distinct sites carry distinct kinds. -/
theorem generator2_injective :
    ∀ s t : RSite, s.kind = t.kind → s = t := by
  intro s t; cases s <;> cases t <;> decide

/-- THE +1 IS STILL NOT SITE-GENERATED: no recognition site yields the Record.
    (Mirrors `record_not_site_generated`; under recognition grounding the
    frame-relation remains outside the artifact-local image.) -/
theorem record_not_rsite_generated : ∀ s : RSite, s.kind ≠ .testimonial := by
  intro s; cases s <;> decide

/-- THE TRANSPORT (the strong form of "same image"): an explicit bijection
    between the speech-act sites and the recognition sites commuting with the
    kind map. This is a CONSISTENCY isomorphism between two hand-built tables,
    exhibiting that the two groundings organize the same eleven — it is not,
    and cannot be, evidence that either grounding generates them. -/
def transport : Site → RSite
  | .factContent        => .stateContent
  | .strengthMarker     => .stateStrength
  | .appliedRule        => .stateRule
  | .foundingAssumption => .stateGiven
  | .directiveContent   => .transitionContent
  | .preferenceOrder    => .outcomeOrder
  | .stepOrder          => .stepOrder
  | .declarationContent => .constitutedStatus
  | .encoding           => .carrierEncoding
  | .register           => .carrierPresentation
  | .instanceToken      => .carrierToken

/-- The transport commutes with the kind maps. -/
theorem generator2_transport (s : Site) : (transport s).kind = s.kind := by
  cases s <;> rfl

/-- The transport is a bijection (injective on a finite type of equal card). -/
theorem transport_injective : ∀ s t : Site, transport s = transport t → s = t := by
  intro s t; cases s <;> cases t <;> decide

end CIRISOntology.Core
