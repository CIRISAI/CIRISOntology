/-
CIRISOntology.Core.Confront — the taxonomy as an anvil.

The eleven-kinds-plus-Record taxonomy has so far been checked against a model
panel and against its own generator. That is a study of the taxonomy's SHAPE.
This file starts the other test, the one that can hurt: take documented,
datable changes from the history of the hard sciences and force each one
through the `Reading` type. Either the entry CONSTRUCTS — its kind is stated,
and whatever coordinate that kind demands is supplied — or it does not, and the
failure is a type error in public rather than a shrug in a survey.

WHAT WOULD KILL THIS. A documented change in mathematics, physics or chemistry
that cannot be constructed as a `Confrontation`, AND whose obstruction is not
the Record relation. Record-shaped obstructions are already predicted (that is
what `repairable_does_not_factor` says); anything else is a twelfth category
candidate and fires the taxonomy's own standing bounty from inside.

WHAT THIS FILE IS NOT. It is a MOLD, not a result. Three entries out of a
twelve-entry candidate table (`scratchpad/LEAN2_CONFRONTATION.md`); chemistry
has no entry at all yet; every kind assignment below is STAKED by us and has
not survived adversarial review. `mold_is_incomplete` and `chemistry_absent`
are pinned as theorems so that a later claim of coverage has to arrive as a
conscious diff of a proof obligation, not as a quietly longer list — the same
device as `Instrument.suite_ships_unvalidated`.

THE ANVIL IS THE TYPE. `Reading` refuses to build a `testimonial` entry with no
frame. That refusal is the whole point of encoding the Mochizuki–abc dispute
here: the surviving papers, referee reports and rebuttals are the same documents
for everyone, and the question "can 'abc is proved' still be re-derived?" still
gets opposite answers depending on which community's retained record you ask
against. `abc_repairability_is_frame_relative` exhibits that, in the wild, with
`Repairable` — the same predicate whose non-factoring is proved in
`Core/WrongKind.lean`.
-/

import CIRISOntology.Core.Instrument

namespace CIRISOntology.Core

/-- Which hard science the change is drawn from. Three constructors because the
    confrontation was scoped to mathematics, physics and chemistry; a change
    from outside those is out of scope for this file rather than unclassifiable. -/
inductive Domain
  /-- Pure mathematics, including the practice of proof and its acceptance. -/
  | mathematics
  /-- Physics, including metrology and astronomy. -/
  | physics
  /-- Chemistry, including nomenclature and the standard tables. -/
  | chemistry
  deriving DecidableEq, Repr

/-- The public label for a domain. -/
def Domain.plain : Domain → String
  | .mathematics => "Mathematics"
  | .physics     => "Physics"
  | .chemistry   => "Chemistry"

/-- One documented change, forced through the instrument layer.

    `stakedKind` is our claim about what kind of change it was; `reading` is the
    same claim built as a `Reading`, so that whatever coordinate the kind demands
    must actually be supplied before the entry exists. `kindMatchesStake` closes
    the gap between the two — an entry cannot advertise one kind in its table row
    and carry another in its reading.

    `sourcePin` names the PRIMARY document, not a summary of it. `plainWhy` is
    one sentence a general reader can hold; per house style, a change we cannot
    state that plainly is a change we have not understood well enough to encode. -/
structure Confrontation where
  /-- What happened, in a few words. -/
  name : String
  /-- When, as documented. -/
  date : String
  /-- Which science. -/
  domain : Domain
  /-- The kind of change we stake. -/
  stakedKind : ChoiceKind
  /-- The primary document this entry is pinned to. -/
  sourcePin : String
  /-- The same claim, built through the instrument layer's obligations. -/
  reading : Reading
  /-- One sentence, for a general reader. -/
  plainWhy : String
  /-- The staked kind and the constructed reading are the same kind. -/
  kindMatchesStake : reading.kind = stakedKind

/-- The public name of the staked kind ("Premises", "Identity", "Record", …). -/
def Confrontation.plainKind (c : Confrontation) : String := c.stakedKind.plain

/-! ### Entry 1 — the kilogram stops being an object (Premises)

The 2019 revision did not discover that the prototype kilogram was the wrong
mass. It changed what the definition is made of: a fixed numerical value of the
Planck constant instead of a cylinder in a vault at Sèvres. Nothing measured
came out different at the precision anyone works at, and that is exactly why
this is not a change of Facts.

The reason it is worth encoding is the RIPPLE, and the ripple is computable: the
kilogram is upstream of the newton, the joule, the pascal, the watt and the
volt, so a change of premises at the kilogram is inherited by every derived unit
that mentions it — the same shape as adopting an axiom and having every theorem
that uses it re-tagged. -/

/-- SI 2019: the kilogram redefined from an artifact to a fixed constant. -/
def si2019 : Confrontation where
  name := "SI redefinition: the kilogram becomes a fixed value of the Planck constant"
  date := "2019-05-20"
  domain := .physics
  stakedKind := .axiomatic
  sourcePin :=
    "CGPM Resolution 1 (26th meeting, 2018); BIPM, The International System of Units (SI), 9th ed. (2019)"
  reading :=
    { kind := .axiomatic
      frame := none
      design := none
      frameSupplied := by decide
      designSupplied := by decide }
  plainWhy :=
    "The kilogram stopped being a metal cylinder in a vault and became a number fixed by definition; no mass in the world changed, but every unit built on the kilogram — the newton, the joule, the watt, the volt — inherited the new footing, which is what makes it a change of premises rather than a change of fact."
  kindMatchesStake := rfl

/-! ### Entry 2 — Pluto is re-carried under adopted criteria (Identity)

Pluto did not move, lose mass, or acquire a new orbit in August 2006. A
criterion was adopted — a planet must have cleared the neighbourhood around its
orbit — and the same object was carried forward under a different type. This is
the registry recipe in the wild: world unchanged, criteria declared, entity
re-typed. It is `ontological` and not `empirical` for exactly that reason, and
the discriminator that does the work is `WrongKind.discriminator .ontological`,
"What is this said to be?" -/

/-- IAU 2006: Pluto reclassified as a dwarf planet. -/
def pluto : Confrontation where
  name := "IAU reclassification: Pluto becomes a dwarf planet"
  date := "2006-08-24"
  domain := .physics
  stakedKind := .ontological
  sourcePin :=
    "IAU XXVIth General Assembly, Prague: Resolution B5 (Definition of a Planet in the Solar System) and Resolution B6 (Pluto)"
  reading :=
    { kind := .ontological
      frame := none
      design := none
      frameSupplied := by decide
      designSupplied := by decide }
  plainWhy :=
    "Pluto did not move or change; astronomers adopted a criterion — a planet must have cleared its orbital neighbourhood — and carried the same object forward under a different name, so what changed is what it is said to be, not any fact about it."
  kindMatchesStake := rfl

/-! ### Entry 3 — abc, and why the frame is not optional (Record)

This entry exists because it is the one the type system can refuse. The
Inter-universal Teichmüller papers are published; the Scholze–Stix objection is
published; Mochizuki's reply is published. Nothing has been lost, so the naive
reading is "no Record problem here". But the Record question is not "did the
documents survive" — it is `WrongKind.discriminator .testimonial`, "can the
event still be established from what survives?", and that question has no
answer until you say ESTABLISHED BY WHOM, against WHICH retained record.

Two frames are exhibited below. One retains, as an established item, that abc
is proved; the other retains the same papers and the same reports without that
item. `Repairable` gives opposite verdicts on the same claim across those two
frames, which is `repairability_not_intrinsic` happening to a real dispute
rather than to a toy corpus. The `Reading` therefore cannot be built without
naming which frame it is read against, and we name the wider one. -/

/-- The claim whose re-derivability is at issue. -/
def abcClaim : String := "the abc conjecture is established"

/-- A frame in which the claim is a retained, established item. -/
def abcFrameRIMS : Frame :=
  [ abcClaim
  , "Mochizuki, Inter-universal Teichmuller Theory I-IV, PRIMS 57 (2021)"
  , "RIMS refereeing record for the PRIMS special issue" ]

/-- A frame retaining the same documents and the objections, without the claim
    itself as an established item. -/
def abcFrameWider : Frame :=
  [ "Mochizuki, Inter-universal Teichmuller Theory I-IV, PRIMS 57 (2021)"
  , "Scholze and Stix, Why abc is still a conjecture (2018)"
  , "Mochizuki, Report on discussions (2018)" ]

/-- **`repairability_not_intrinsic`, in the wild.** The same claim, the same
    surviving documents, opposite verdicts — because the two communities retain
    different things as established. This is why the Record entry below has to
    name its frame, and why an instrument that fired on the artifact alone here
    would not be cautious, it would be wrong. -/
theorem abc_repairability_is_frame_relative :
    Repairable abcClaim abcFrameRIMS ∧ ¬ Repairable abcClaim abcFrameWider := by
  constructor
  · decide
  · decide

/-- Mochizuki–abc: the acceptance dispute, read against the wider community's
    retained record. -/
def mochizuki : Confrontation where
  name := "Mochizuki-abc: the acceptance dispute over Inter-universal Teichmuller theory"
  date := "2021-03 (PRIMS 57 publication; dispute open)"
  domain := .mathematics
  stakedKind := .testimonial
  sourcePin :=
    "Mochizuki, Inter-universal Teichmuller Theory I-IV, PRIMS 57 (2021) 3-723; Scholze and Stix, Why abc is still a conjecture (2018)"
  reading :=
    { kind := .testimonial
      frame := some abcFrameWider
      design := none
      frameSupplied := fun _ => rfl
      designSupplied := by decide }
  plainWhy :=
    "Every paper, objection and reply survives, so nothing is lost; whether 'abc is proved' can still be re-derived depends on whose retained record you check it against, which is why this entry cannot even be written down without naming that record."
  kindMatchesStake := rfl

/-! ### The corpus, and what it is honestly allowed to claim -/

/-- The encoded entries, in the order they appear above. -/
def confrontations : List Confrontation := [si2019, pluto, mochizuki]

/-- The candidate changes from the season's table that are NOT encoded here.
    Carried in the source so the gap is visible to a reader of the file, not
    only to whoever opens the design note. -/
def notYetEncoded : List String :=
  [ "CODATA adjustment cycles (staked Facts)"
  , "IUPAC 2009: atomic weights become intervals (staked Confidence)"
  , "element naming disputes, 104-109, settled 2016 (staked Identity/Manner)"
  , "phlogiston to oxygen (staked Model)"
  , "adoption and independence of the Axiom of Choice (staked Premises)"
  , "Bourbaki definition reforms, function-as-graph (staked Structure/Premises)"
  , "notation reform: Leibniz vs Newton (staked Manner)"
  , "Wiles 1993 to 1995, the gap repair (staked Process)"
  , "leap seconds and calendar reform (staked Circumstances/Premises)" ]

/-- **The three entries construct.** Each row's staked kind is the kind its
    `Reading` was actually built with — that agreement is a field obligation, so
    this list is read off the constructed objects and not asserted beside them. -/
theorem confrontations_constructed :
    confrontations.map (·.stakedKind) =
      [WrongKind.axiomatic, WrongKind.ontological, WrongKind.testimonial] := rfl

/-- **The anvil left a mark.** Only the Record entry carries a frame. The other
    two are frameless not by choice but because their kinds do not demand one —
    and the Record entry is frameful not by diligence but because the type would
    not let it be built otherwise. -/
theorem only_the_record_entry_carries_a_frame :
    confrontations.map (·.reading.frame.isSome) = [false, false, true] := rfl

/-- The generic form of the same fact, inherited from the instrument layer: any
    Record entry, not merely this one, can have its frame read back off it. -/
theorem record_entry_has_frame (c : Confrontation) (h : c.stakedKind = .testimonial) :
    ∃ f, c.reading.frame = some f :=
  reading_record_has_frame c.reading (c.kindMatchesStake.trans h)

/-- The staked kind is never decorative: it is the reading's own kind. -/
theorem stake_is_the_reading (c : Confrontation) : c.reading.kind = c.stakedKind :=
  c.kindMatchesStake

/-- Which domains are actually represented. -/
theorem domains_encoded :
    confrontations.map (·.domain) = [Domain.physics, Domain.physics, Domain.mathematics] := rfl

/-- **HONESTY PIN: chemistry has no entry.** The confrontation was scoped to
    three sciences and covers two. Any statement that the taxonomy has been put
    to chemistry is false while this theorem holds, and adding the first
    chemistry entry breaks it — which is the intended cost. -/
theorem chemistry_absent : ¬ (Domain.chemistry ∈ confrontations.map (·.domain)) := by decide

/-- **HONESTY PIN: this is a mold, not a survey.** Three encoded against nine
    still owed. The success criterion staked in the design note is that EVERY
    entry constructs; three that do is a mold that works, not a criterion met. -/
theorem mold_is_incomplete : confrontations.length < notYetEncoded.length := by decide

/-- What this file commits to, in the `Gate.mechanized` style: fields whose type
    is `True` are RECORDED COMMITMENTS, not proofs, and are never presented as
    machine-checked. The theorems above are the machine-checked part; these four
    are the human part, written down so the difference stays visible. -/
structure MoldStatus where
  /-- Three entries are a mold for the encoding, not a validated taxonomy. -/
  three_entries_are_not_a_taxonomy : True
  /-- Every kind assignment above is staked by us and has not been through
      adversarial review; a contested row is a correction, not a surprise. -/
  kinds_are_staked_not_adjudicated : True
  /-- Each entry pins a primary document, not a secondary summary of one. -/
  sources_pinned_to_primary_documents : True
  /-- The kill is a documented change that cannot construct and whose
      obstruction is not the Record relation. -/
  the_kill_is_a_nonconstructible_change : True

/-- The commitments are in force. -/
def mold_status : MoldStatus := ⟨trivial, trivial, trivial, trivial⟩

end CIRISOntology.Core
