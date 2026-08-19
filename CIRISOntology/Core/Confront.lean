/-
CIRISOntology.Core.Confront — the taxonomy as an anvil.

The eleven-kinds-plus-Record taxonomy has so far been checked against a model
panel and against its own generator. That is a study of the taxonomy's SHAPE.
This file is the other test, the one that can hurt: take documented, datable
changes from the history of the hard sciences and force each one through the
`Reading` type. Either the entry CONSTRUCTS — its kind is stated, and whatever
coordinate that kind demands is supplied — or it does not, and the failure is a
type error in public rather than a shrug in a survey.

WHAT WOULD KILL THIS. A documented change in mathematics, physics or chemistry
that cannot be constructed as a `Confrontation`, AND whose obstruction is not
the Record relation. Record-shaped obstructions are already predicted (that is
what `repairable_does_not_factor` says); anything else is a twelfth category
candidate and fires the taxonomy's own standing bounty from inside.

WHAT THIS FILE IS NOT, STATED ONCE AND MEANT THROUGHOUT. **Every kind assignment
below is STAKED BY US and has not survived adversarial review.** All twelve rows
of the season's candidate table (`scratchpad/LEAN2_CONFRONTATION.md`) now
construct, and that is exactly one half of the criterion staked in that note. The
other half — that the assignments survive attack — is NOT met, is not a theorem,
and could not be one. Three rows offered two kinds and we picked one; each pick
is recorded with its reason in the entry's docstring, and the three boundaries we
expect to be fought first are named where they occur (Model vs Facts at
Lavoisier, Confidence vs Facts at the IUPAC intervals, Structure vs Premises at
Bourbaki). A contested row is a correction we owe, not a surprise.

THE HONESTY PINS, AND WHAT BECAME OF THE OLD ONES. `chemistry_absent` and
`mold_is_incomplete` were pinned as theorems in the three-entry commit precisely
so that a later claim of coverage would have to arrive as a conscious diff of a
proof obligation. Both are now discharged, visibly and by name, in
`every_domain_encoded` and `candidate_table_exhausted`; neither was quietly
deleted. `kinds_not_reached` replaces them as the live pin — nine of the twelve
kinds are exercised by this corpus and three are not, and any statement that the
taxonomy has been put to the history of science in full is false while that
theorem holds. Same device as `Instrument.suite_ships_unvalidated`.

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

/-! ### Entry 4 — the constants are readjusted (Facts)

This entry earns its place by sharing Entry 1's date. The same international
apparatus released, on 20 May 2019, two changes that the taxonomy must
separate: the SI revision changed what the units ARE, and the
CODATA 2018 adjustment changed what the numbers SAY. Nothing in the CODATA
adjustment is declared; it is a least-squares fit to the measurements available
at the cut-off, and its output is a set of claims that new measurements can
falsify — which several of them promptly did to their predecessors.

The clean discriminator is the proton's charge radius. CODATA 2014 recommended
0.8751(61) fm; CODATA 2018 recommends 0.8414(19) fm. The new value is not inside
the old error bar. A published number that was right became wrong, on the same
definitional footing, which is what `WrongKind.discriminator .empirical` asks —
"What claimed fact becomes wrong?" — and is why this row must NOT read as
Premises merely because the words "fundamental constant" appear in it. -/

/-- CODATA 2018: the recommended values of the fundamental constants readjusted.
    Staked `empirical` and not `axiomatic` despite touching constants: the
    adjustment declares nothing, it fits, and its output is falsifiable by the
    next measurement — which is exactly what happened to the 2014 proton radius. -/
def codata2018 : Confrontation where
  name := "CODATA 2018: the recommended values of the fundamental constants are readjusted"
  date := "2019-05-20 (release; input data closed 2018-12-31)"
  domain := .physics
  stakedKind := .empirical
  sourcePin :=
    "E. Tiesinga, P. J. Mohr, D. B. Newell and B. N. Taylor, CODATA Recommended Values of the Fundamental Physical Constants: 2018, Rev. Mod. Phys. 93 (2021) 025010"
  reading :=
    { kind := .empirical
      frame := none
      design := none
      frameSupplied := by decide
      designSupplied := by decide }
  plainWhy :=
    "Nothing about what the constants ARE changed — the definitions stayed exactly where the SI revision had just put them — but new measurements moved the recommended numbers, and the proton's radius moved from 0.8751 to 0.8414 femtometres, outside its own former error bar: a published number that was right became wrong."
  kindMatchesStake := rfl

/-! ### Entry 5 — the atomic weights become intervals (Confidence)

For ten elements — hydrogen, lithium, boron, carbon, nitrogen, oxygen, silicon,
sulfur, chlorine and thallium — IUPAC stopped publishing a single standard
atomic weight with an uncertainty and started publishing an interval. No
measurement was withdrawn. What changed is what a bare number from the table is
warranted to mean: for a normal terrestrial material the honest answer depends
on where the sample came from, and the table now says so in its own type rather
than in a footnote.

THIS IS THE ROW WE EXPECT TO LOSE FIRST, and the attack is easy to state: IUPAC's
own reason for the interval is that the atomic weight genuinely VARIES among
natural materials, so a reader can fairly say the change is a change of Facts
(the proposition "carbon's atomic weight is 12.0107" was replaced) or of
Structure (the number's type changed from scalar to interval). We stake
Confidence because the pre-2009 single value was never asserted as the value of
any particular sample — it was a convention about how sure one may be when the
provenance is unknown — and it is that standard, not a measured quantity and not
a parsing rule, that the 2009 decision moved. If the panel comes back Facts, the
Confidence/Facts boundary in `WrongKind.plain`'s note is where the correction
lands, and this docstring is where it will be recorded. -/

/-- IUPAC 2009: standard atomic weights published as intervals for ten elements.
    Staked `epistemic` over `empirical`/`structural`: the single value it replaced
    was a convention about warranted confidence under unknown provenance, and it
    is that standard which moved. -/
def iupac2009 : Confrontation where
  name := "IUPAC 2009: standard atomic weights become intervals"
  date := "2009-08 (IUPAC General Assembly, Vienna; table published 2011)"
  domain := .chemistry
  stakedKind := .epistemic
  sourcePin :=
    "M. E. Wieser and T. B. Coplen, Atomic weights of the elements 2009 (IUPAC Technical Report), Pure Appl. Chem. 83 (2011) 359-396"
  reading :=
    { kind := .epistemic
      frame := none
      design := none
      frameSupplied := by decide
      designSupplied := by decide }
  plainWhy :=
    "For ten elements the single published atomic weight was replaced by a range, because the honest answer depends on where your sample came from; no measurement was found to be wrong, but how sure anyone is entitled to be about a bare number from the table changed, and the hedge now sits inside the published value instead of beside it."
  kindMatchesStake := rfl

/-! ### Entry 6 — elements 104 to 109 get their names (Identity)

Berkeley and Dubna had each synthesised and each named the same six elements,
and for two decades the literature carried two incompatible naming systems for
them. The 1997 IUPAC recommendation ended that by declaring, for the register,
which name each element carries: rutherfordium, dubnium, seaborgium, bohrium,
hassium, meitnerium.

The candidate table offered Identity or Manner, and the choice matters because
the two make opposite predictions about what was at stake. This is the Pluto
recipe again — world unchanged, registry declares, entity carried forward under
a name — with the extra feature that the naming was itself the performative act
that closed the dispute, which is the registry site the design note wanted
encoded. -/

/-- IUPAC 1997: the names of elements 104-109 settled. CHOICE — the table offered
    Identity or Manner and we stake Identity, because Manner requires the two
    candidate names to be interchangeable ways of writing the same registered
    entity, and that is precisely what the two laboratories denied: the names
    carried discovery attributions, so the vote declared what each element IS in
    the register rather than how an already-settled entity should be spelled. -/
def transfermium : Confrontation where
  name := "IUPAC 1997: the names of elements 104-109 are settled"
  date := "1997-08 (39th IUPAC General Assembly, Geneva)"
  domain := .chemistry
  stakedKind := .ontological
  sourcePin :=
    "IUPAC Commission on Nomenclature of Inorganic Chemistry, Names and symbols of transfermium elements (IUPAC Recommendations 1997), Pure Appl. Chem. 69 (1997) 2471-2473"
  reading :=
    { kind := .ontological
      frame := none
      design := none
      frameSupplied := by decide
      designSupplied := by decide }
  plainWhy :=
    "Two laboratories had each made and each named the same six elements, and the atoms were never in dispute; what IUPAC settled in 1997 is which name each element is carried under in the register — the world unchanged, the entry re-typed by declaration."
  kindMatchesStake := rfl

/-! ### Entry 7 — phlogiston gives way to oxygen (Model)

The weighings survive the revolution intact. A metal had always been observed to
gain weight when it was calcined, and it still does; what changed is the rule
under which that observation is explained — losing a substance called phlogiston
was replaced by gaining one called oxygen. That the old measurements are
re-carried unchanged into the new account is the Model signature, and it is the
reason this row is here rather than in a history footnote.

THE OBVIOUS ATTACK, and it is a good one: `WrongKind.plain`'s own Model-vs-Facts
note says that a model ASSERTED to be descriptively true of the world is a Fact
and fails empirically — and phlogiston was so asserted, as a real substance with
a real (sometimes negative) weight. A reviewer can therefore file this as Facts:
"phlogiston exists" became wrong. We stake Model because the datable change being
encoded is the replacement of the framework for reasoning about combustion and
calcination, whose diagnostic is precisely that the data are carried across; the
non-existence of phlogiston is a consequence drawn from the replacement, not the
change itself. Together with Entry 5 this is where we expect the corpus to bleed. -/

/-- Lavoisier: combustion re-derived under oxygen instead of phlogiston. Staked
    `nomological` over `empirical`: the measurements are re-carried unchanged and
    it is the reasoning framework that is replaced — the non-existence of
    phlogiston follows from the replacement rather than constituting it. -/
def lavoisier : Confrontation where
  name := "Phlogiston gives way to oxygen: Lavoisier's theory of combustion"
  date := "1785 (read to the Academie) / 1786 (Memoires for 1783) / 1789 (Traite)"
  domain := .chemistry
  stakedKind := .nomological
  sourcePin :=
    "A.-L. Lavoisier, Reflexions sur le phlogistique, Mem. Acad. Roy. Sci. (for 1783), Paris 1786, 505-538; Traite elementaire de chimie, Paris 1789"
  reading :=
    { kind := .nomological
      frame := none
      design := none
      frameSupplied := by decide
      designSupplied := by decide }
  plainWhy :=
    "The weighings did not change — a metal had always got heavier when it burned — but the rule under which that was explained was replaced: instead of losing a substance called phlogiston the metal gains one called oxygen, and every old measurement was carried across into the new account intact."
  kindMatchesStake := rfl

/-! ### Entry 8 — the Axiom of Choice (Premises)

Choice is the mathematical Premises case, and the reason it is worth a row is
that its history separates the three things the label can be confused with.
Zermelo's 1904 well-ordering proof made the assumption explicit; Gödel showed in
1938 that assuming it cannot introduce a contradiction that was not already
there; Cohen showed in 1963-64 that denying it cannot either. After that pair of
results, Choice is provably not a fact about sets that anyone can go and check.
It is something taken as given, and the ripple is the same computable one as the
kilogram's: every theorem whose proof uses it acquires a tag, and the tag
propagates to everything downstream. -/

/-- The Axiom of Choice: adopted 1904, proved independent 1938/1963-64. -/
def choice : Confrontation where
  name := "The Axiom of Choice: adopted, then proved independent"
  date := "1904 (Zermelo) / 1938 (Godel) / 1963-1964 (Cohen)"
  domain := .mathematics
  stakedKind := .axiomatic
  sourcePin :=
    "E. Zermelo, Beweis, dass jede Menge wohlgeordnet werden kann, Math. Ann. 59 (1904) 514-516; K. Godel, The consistency of the axiom of choice and of the generalized continuum-hypothesis, PNAS 24 (1938) 556-557; P. J. Cohen, The independence of the continuum hypothesis I-II, PNAS 50 (1963) 1143-1148 and 51 (1964) 105-110"
  reading :=
    { kind := .axiomatic
      frame := none
      design := none
      frameSupplied := by decide
      designSupplied := by decide }
  plainWhy :=
    "Choice is not a fact anyone can check about sets — it was proved that both taking it and refusing it are equally safe — so it is something a mathematician decides to take as given, and every theorem that uses it had to be re-tagged as depending on it, the same ripple the kilogram sent through the derived units."
  kindMatchesStake := rfl

/-! ### Entry 9 — a function becomes its graph (Structure)

Bourbaki replaced "a function is a rule assigning to each x a value f(x)" with
"a function is a functional graph together with the two sets it runs between".
No theorem of analysis changed truth value under the reform. What changed is how
the object is assembled out of pieces that were already granted, and the
diagnostic is that sentences stopped parsing: after the reform a function comes
with its codomain, so "the same function, regarded as landing in a larger set"
is not a well-formed description of one object any more, and surjectivity became
a property of the object rather than of a presentation of it.

The candidate table offered Structure or Premises, and this row was put in the
table because it is exactly the boundary the model panel confuses. -/

/-- Bourbaki: a function becomes its graph. CHOICE — the table offered Structure
    or Premises and we stake Structure, because nothing new was taken as given
    (the set theory was already the ground and no axiom was added or dropped),
    while the reform did break PARSING: a pre-reform sentence about a function
    with no declared codomain is not a post-reform sentence about anything, which
    is `structural`'s own discriminator and not `axiomatic`'s. -/
def bourbaki : Confrontation where
  name := "Bourbaki: a function becomes its graph"
  date := "1939 (Fascicule de resultats) / 1954 (Theorie des ensembles, ch. I-II)"
  domain := .mathematics
  stakedKind := .structural
  sourcePin :=
    "N. Bourbaki, Elements de mathematique, Theorie des ensembles: Fascicule de resultats (Paris: Hermann, 1939) and ch. II, Theorie des ensembles (Paris: Hermann, 1954)"
  reading :=
    { kind := .structural
      frame := none
      design := none
      frameSupplied := by decide
      designSupplied := by decide }
  plainWhy :=
    "Bourbaki stopped saying a function is a rule and said it is a set of pairs together with the two sets it runs between; no theorem changed truth value, but sentences that had been perfectly well formed before — 'the same function, viewed as landing in a bigger set' — stopped parsing, which is a change in how the pieces are put together rather than in what is taken as given."
  kindMatchesStake := rfl

/-! ### Entry 10 — dx over the dot (Manner)

Leibniz's differential notation and Newton's fluxion dot denote the same
derivative. No proposition of the calculus is true in one and false in the
other, and the century in which British mathematics kept the dot cost it
readership, collaborators and speed — not correctness. That is the whole content
of a Manner change: content-preserving re-expression, at a scale where the
re-expression nevertheless had consequences worth a row.

We pin two documents because the change has two datable ends: the notation's
introduction in 1684, and its adoption by the holdout community in 1816, when
the Cambridge Analytical Society published its translation of Lacroix. -/

/-- Notation reform: Leibniz's `dx` displaces Newton's dot. -/
def leibnizNotation : Confrontation where
  name := "Notation reform: Leibniz's dx displaces Newton's fluxion dot"
  date := "1684 (Leibniz, Acta Eruditorum) / 1816 (Cambridge adoption)"
  domain := .mathematics
  stakedKind := .pragmatic
  sourcePin :=
    "G. W. Leibniz, Nova methodus pro maximis et minimis, itemque tangentibus, Acta Eruditorum (Oct. 1684) 467-473; [C. Babbage, J. Herschel and G. Peacock], An Elementary Treatise on the Differential and Integral Calculus (translation of S. F. Lacroix), Cambridge 1816"
  reading :=
    { kind := .pragmatic
      frame := none
      design := none
      frameSupplied := by decide
      designSupplied := by decide }
  plainWhy :=
    "dy/dx and a dot over the letter mean exactly the same thing, and no theorem of calculus is true in one notation and false in the other; what a century of British holdout cost was not correctness but the ability to read and be read, which is the entire content of a change of manner."
  kindMatchesStake := rfl

/-! ### Entry 11 — the gap and the repair (Process)

The theorem Wiles announced in Cambridge in June 1993 is the theorem published
in the Annals in May 1995. In between, the referees found that one step — an
upper bound on a Selmer group, argued by an Euler system — did not hold, and it
was replaced by a different argument, developed with Richard Taylor and
published as the companion paper. The destination did not move; the route did.

The attack we expect is Confidence: between 1993 and 1995 the community's
warrant for believing Fermat's Last Theorem plainly changed. Our answer is that
the artifact under variation here is the PROOF, not the community's credence,
and what varies between the 1993 manuscript and the 1995 pair of papers is the
sequence of steps — `WrongKind.discriminator .procedural`, "What steps or
ordering change?". A Confidence reading has to make the proof's own content
constant, and it is not. -/

/-- Wiles 1993 to 1995: the gap and its repair. Staked `procedural` over
    `epistemic`: the community's credence did move, but the object being varied
    is the proof, and what differs between the two versions is its steps. -/
def wiles : Confrontation where
  name := "Fermat's Last Theorem: the 1993 gap and the 1995 repair"
  date := "1993-06 (Cambridge lectures) / 1994-09 (repair) / 1995-05 (publication)"
  domain := .mathematics
  stakedKind := .procedural
  sourcePin :=
    "A. Wiles, Modular elliptic curves and Fermat's Last Theorem, Ann. of Math. 141 (1995) 443-551; R. Taylor and A. Wiles, Ring-theoretic properties of certain Hecke algebras, Ann. of Math. 141 (1995) 553-572"
  reading :=
    { kind := .procedural
      frame := none
      design := none
      frameSupplied := by decide
      designSupplied := by decide }
  plainWhy :=
    "The statement announced in 1993 is the statement published in 1995; one step — an upper bound on a group — would not hold and was replaced by a different argument built with Richard Taylor, so the destination stayed exactly where it was and only the path to it changed."
  kindMatchesStake := rfl

/-! ### Entry 12 — the leap second (Premises)

Nobody discovered anything about the Earth in November 2022. What the CGPM
changed is a rule its own community had adopted: that broadcast civil time must
never differ from the Earth's rotation angle by more than a fixed tolerance —
0.7 s when the leap-second system entered force in 1972, 0.9 s after the 1974
revision — enforced by inserting whole seconds. Resolution 4 of the 27th CGPM
decided to raise that tolerance by or before 2035, which retires the leap second
in practice. Because every timekeeping system in operation is built on the old
rule, the ripple is computable in the same sense Entry 1's is.

The candidate table offered Circumstances or Premises. Circumstances is
excluded on the taxonomy's own terms, and the exclusion is machine-checked one
line below: `contingent` asserts nothing about the artifact
(`WrongKind.assertsContent .contingent = false`) because it is the label for what
a COMPARISON failed to hold fixed. A historical change has no comparison design,
so there is nothing for that label to be relative to here. -/

/-- Why nothing in this corpus can be `Circumstances`: the label carries no
    content about the artifact — it reports what a comparison did not hold fixed
    — and a documented historical change supplies no comparison to be relative
    to. This is the machine-checked half of Entry 12's choice. -/
theorem circumstances_asserts_nothing :
    WrongKind.contingent.assertsContent = false := rfl

/-- Leap seconds and the UTC tolerance. CHOICE — the table offered Circumstances
    or Premises and we stake Premises: the datable events are declarations with a
    computable ripple (the same shape as Entry 1), and Circumstances is ruled out
    by `circumstances_asserts_nothing`, since there is no comparison design here
    for a design-relative label to be relative to. -/
def leapSecond : Confrontation where
  name := "Leap seconds: the adopted tolerance between clock time and Earth time"
  date := "1972-01-01 (leap-second UTC in force) / 2022-11-18 (27th CGPM Resolution 4)"
  domain := .physics
  stakedKind := .axiomatic
  sourcePin :=
    "CCIR Recommendation 460 (1970) and Recommendation 460-1 (1974), establishing leap-second UTC and the 0.9 s tolerance; Resolution 4 of the 27th CGPM (2022), On the use and future development of UTC"
  reading :=
    { kind := .axiomatic
      frame := none
      design := none
      frameSupplied := by decide
      designSupplied := by decide }
  plainWhy :=
    "Nobody discovered anything about the Earth in 2022; what the treaty body changed is a rule it had adopted in the first place — that clock time must never drift more than a fraction of a second from the turning of the planet — and because the world's computers keep time on that rule, changing it is a change of footing rather than a change of circumstance."
  kindMatchesStake := rfl

/-! ### The corpus, and what it is honestly allowed to claim -/

/-- The encoded entries, in the order they appear above. -/
def confrontations : List Confrontation :=
  [ si2019, pluto, mochizuki
  , codata2018, iupac2009, transfermium, lavoisier
  , choice, bourbaki, leibnizNotation, wiles, leapSecond ]

/-- The candidate changes from the season's table that are NOT encoded here.
    Carried in the source so the gap is visible to a reader of the file, not
    only to whoever opens the design note. It is now empty, and
    `candidate_table_exhausted` pins that rather than leaving it to be noticed. -/
def notYetEncoded : List String := []

/-- **All twelve entries construct.** Each row's staked kind is the kind its
    `Reading` was actually built with — that agreement is a field obligation, so
    this list is read off the constructed objects and not asserted beside them. -/
theorem confrontations_constructed :
    confrontations.map (·.stakedKind) =
      [WrongKind.axiomatic, WrongKind.ontological, WrongKind.testimonial,
       WrongKind.empirical, WrongKind.epistemic, WrongKind.ontological,
       WrongKind.nomological, WrongKind.axiomatic, WrongKind.structural,
       WrongKind.pragmatic, WrongKind.procedural, WrongKind.axiomatic] := rfl

/-- **The anvil left a mark.** Only the Record entry carries a frame. The other
    eleven are frameless not by choice but because their kinds do not demand one
    — and the Record entry is frameful not by diligence but because the type
    would not let it be built otherwise. Twelve documented changes and exactly
    one of them needed an argument beyond the artifact: that is
    `repairable_does_not_factor` showing up as a shape in a corpus. -/
theorem only_the_record_entry_carries_a_frame :
    confrontations.map (·.reading.frame.isSome) =
      [false, false, true, false, false, false, false, false, false, false, false, false] := rfl

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
    confrontations.map (·.domain) =
      [Domain.physics, Domain.physics, Domain.mathematics,
       Domain.physics, Domain.chemistry, Domain.chemistry, Domain.chemistry,
       Domain.mathematics, Domain.mathematics, Domain.mathematics,
       Domain.mathematics, Domain.physics] := rfl

/-- **COVERAGE PIN, replacing `chemistry_absent`.** Every domain the
    confrontation was scoped to now has at least one entry. `chemistry_absent`
    was the honesty pin from the three-entry commit; it was DISCHARGED
    2026-08-18 by Entries 5, 6 and 7 rather than deleted silently, and this
    theorem is what stands in its place. -/
theorem every_domain_encoded (d : Domain) : d ∈ confrontations.map (·.domain) := by
  rw [domains_encoded]; cases d <;> decide

/-- The named supersession, so a reader searching for the old pin finds its
    negation and its date: `chemistry_absent` held until 2026-08-18. -/
theorem chemistry_present : Domain.chemistry ∈ confrontations.map (·.domain) :=
  every_domain_encoded .chemistry

/-- **SCOPE PIN, replacing `mold_is_incomplete`.** The season's candidate table
    is exhausted: twelve rows staked, twelve rows encoded, none owed.
    `mold_is_incomplete` (three against nine) was the honesty pin from the
    three-entry commit and is DISCHARGED 2026-08-18, not deleted. What it
    guarded is NOT thereby met: the staked success criterion has two conjuncts,
    and this theorem checks the one a theorem can — every candidate row
    constructs. The other, that the kind assignments survive adversarial review,
    is not machine-checkable and is carried as a recorded commitment in
    `MoldStatus.kinds_are_staked_not_adjudicated`. -/
theorem candidate_table_exhausted :
    confrontations.length = 12 ∧ notYetEncoded = [] := ⟨rfl, rfl⟩

/-- **HONESTY PIN, the live one.** The corpus reaches nine of the twelve kinds.
    Priorities and Rules have no entry because the confrontation was scoped to
    the hard sciences and those kinds live where norms are set, not where nature
    is described; Circumstances has none for the reason proved in
    `circumstances_asserts_nothing`. Any statement that the taxonomy has been put
    to the history of science in full is false while this theorem holds, and
    reaching a tenth kind breaks it — which is the intended cost. -/
theorem kinds_not_reached :
    WrongKind.all.filter (fun k => !(confrontations.map (·.stakedKind)).contains k)
      = [WrongKind.axiotic, WrongKind.deontic, WrongKind.contingent] := by
  simp only [confrontations_constructed]; decide

/-- What this file commits to, in the `Gate.mechanized` style: fields whose type
    is `True` are RECORDED COMMITMENTS, not proofs, and are never presented as
    machine-checked. The theorems above are the machine-checked part; these four
    are the human part, written down so the difference stays visible. -/
structure MoldStatus where
  /-- Twelve entries drawn from one design note's candidate table are a corpus we
      chose, not a sample of the history of science. -/
  twelve_entries_are_not_a_survey : True
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
