/-
CIRISOntology.Core.Fit — direction of fit as a 2×2, and the settlement of the
"odd one out" fork.

WHAT THIS FILE SETTLES. `Surface.lean` singles out four sites as the blocks' gross
faces — Facts, Rules, Identity, Manner. Two earlier theorems then nominate two
DIFFERENT members of that four as the singular one, and the disagreement was
recorded as an open fork in `scratchpad/DIMENSION_TABLE.md`:

  * BY DEPTH, Identity is singular: its block has zero depths where the other
    three have 3, 2 and 2 (`Surface.lean`'s `depth_counts`).
  * BY CONVERSION, Manner is singular: mention relates Facts, Rules and Identity
    and leaves Manner untouched (`Symmetry.lean`'s `carrier_inert_under_mention`).

Both are theorems, so neither can be argued away, and the fork was read as a
conflict. It is not one. The question "which surface is the odd one out" presumes
ONE singular corner; the four surfaces are the four cells of a 2×2, and a 2×2 has
a DIAGONAL — two corners, dual to each other. Identity is the double corner and
Manner is the null corner, and each entails exactly one of the two properties that
looked like rival answers (§3). The fork was malformed, not undecided.

THE 2×2 IS BORROWED, and the borrowing is the point rather than an embarrassment.
Direction of fit is Anscombe's (1957, *Intention* §32 — the shopper's list read
two ways), taken up by Austin (1962) and made a taxonomic component by Searle
(1975, "A Taxonomy of Illocutionary Acts"; 1976), with the DOUBLE direction of fit
assigned to declarations there and the four-way grid — including a null/empty
direction — set out in Searle & Vanderveken (1985). None of it is carved here.
This file does one thing to it: reads the two components as independent Booleans
and checks that `Surface.lean`'s four blocks occupy the four cells exactly.

WHERE THIS DEPARTS FROM SEARLE, stated up front because it is the file's real
exposure and a reader will otherwise assume more agreement than there is. Searle's
own null-direction cell is EXPRESSIVES (thanking, apologising) — a force, with a
sincerity condition, not an absence of force. The block occupying the null cell
here is `Surface.lean`'s CARRIER: the force-neutral vehicle layer, whose surface
is Manner. Those are not the same object, and the site model has no expressive
force to put in the cell (`Generator.lean`'s `Force` carries three of Searle's
five — commissives, which share the directive cell, and expressives, which own the
null one, are both absent). So `fit_surjective` below says every CELL of the 2×2
is realised by a block of this model. It does NOT say the model reproduces
Searle's five forces, and it must not be quoted as if it did.

SCOPE, inherited unchanged from `Generator.lean`. Everything here is
THEOREM-GIVEN-MODEL: `rfl`s and case bashes about a four-element inductive type
and an eleven-element one. A 2×2 of the model is not a 2×2 of speech, and the
honest question remains "is the site model adequate?", which is answered by
measurement and never by this file. The physics readings that the settlement
enables — gauge directions, in-plane time — live in `scratchpad/N18_BRIDGE_NOTE.md`
and are claimed NOWHERE below.
-/

import CIRISOntology.Core.Symmetry

namespace CIRISOntology.Core

/-! ### §1 The two components, and the four cells

Direction of fit is standardly TWO questions, not one axis with a middle. Reading
them as independent Booleans is what turns Searle's list into a grid. -/

/-- The two direction-of-fit components, as independent Booleans.

    `wordToWorld` — the word is answerable to the world: if they disagree, the
    word is what was wrong. `worldToWord` — the world is answerable to the word:
    if they disagree, the world is what is to be changed. A commitment may carry
    either, both, or neither, which is exactly why this is a 2×2. -/
structure Fit where
  /-- the word must match the world -/
  wordToWorld : Bool
  /-- the world must be made to match the word -/
  worldToWord : Bool
  deriving DecidableEq, Repr

/-- **THE ASSIGNMENT.** Searle's table, transcribed: assertives are answerable to
    the world, directives make the world answerable to them, declarations do both
    at once (the double direction of fit), and the null cell commits to neither.

    The first three rows are prior art and nothing is chosen in writing them. The
    fourth is where this file inherits `Surface.lean`'s ONE modelling choice: the
    carrier block is force-neutral, so it makes no commitment in either direction,
    and that is read as the null cell. See the header for how this differs from
    Searle's own occupant of that cell. -/
def Block.fit : Block → Fit
  | .assertive   => ⟨true,  false⟩
  | .directive   => ⟨false, true⟩
  | .declaration => ⟨true,  true⟩
  | .carrier     => ⟨false, false⟩

/-- A site's fit is its block's — sites do not carry a fit of their own, which is
    the same fact as fit being a property of the force and not of the apparatus. -/
def Site.fit (s : Site) : Fit := s.block.fit

/-- The four cells, in the canonical order used below. -/
def Fit.all : List Fit := [⟨false, false⟩, ⟨false, true⟩, ⟨true, false⟩, ⟨true, true⟩]

/-! ### §2 The four surfaces ARE the 2×2

Two halves, and both are needed. Injectivity says the fit is a complete invariant
of the block — no two blocks share a cell. Surjectivity says no cell is empty. Put
together, `Block.fit` is a bijection onto the grid, so the four surfaces are not
four things that happen to have fits: they are the grid. -/

/-- **DISTINCT BLOCKS, DISTINCT FITS.** So the fit is a complete invariant: naming
    a block's direction of fit names the block. -/
theorem fit_injective (b₁ b₂ : Block) (h : Block.fit b₁ = Block.fit b₂) : b₁ = b₂ := by
  cases b₁ <;> cases b₂ <;> first | rfl | exact absurd h (by decide)

/-- **EVERY CELL IS REALISED.** No cell of the 2×2 is empty. Read with
    `fit_injective`: no cell is doubled either. -/
theorem fit_surjective (f : Fit) : ∃ b : Block, Block.fit b = f := by
  cases f with
  | mk w r =>
    cases w <;> cases r
    · exact ⟨.carrier, rfl⟩
    · exact ⟨.directive, rfl⟩
    · exact ⟨.assertive, rfl⟩
    · exact ⟨.declaration, rfl⟩

/-- **THE FOUR SURFACES ARE THE 2×2**, both halves in one statement. This is the
    settlement's premise: a question of the form "which of the four is singular?"
    is a question about a grid, and grids have diagonals. -/
theorem fit_bijection :
    (∀ b₁ b₂ : Block, Block.fit b₁ = Block.fit b₂ → b₁ = b₂) ∧
    (∀ f : Fit, ∃ b : Block, Block.fit b = f) :=
  ⟨fit_injective, fit_surjective⟩

/-- The same, computationally: the blocks' fits are the four cells, each once. -/
theorem fit_image : Block.all.map Block.fit = [⟨true, false⟩, ⟨false, true⟩,
    ⟨true, true⟩, ⟨false, false⟩] := rfl

theorem fit_image_card : (Block.all.map Block.fit).length = 4 := rfl

/-- **THE TABLE, in the public vocabulary** — `scratchpad/DIMENSION_TABLE.md`'s
    2×2 mechanized, read through `Surface.lean`'s `grossKind` so the four names
    are the ones the measurement was taken in and not fresh labels. -/
theorem fit_table_plain :
    Block.all.map (fun b => ((Block.grossKind b).plain, b.fit.wordToWorld, b.fit.worldToWord)) =
      [("Facts", true, false), ("Rules", false, true),
       ("Identity", true, true), ("Manner", false, false)] := rfl

/-! ### §3 The diagonal: two singular corners, dual, not rival

The off-diagonal cells carry exactly one component each and are mirror images of
one another — Facts and Rules are the same shape seen from the two ends. The
diagonal cells are the ones where the two components AGREE, and there are exactly
two of them: both on, and both off. -/

/-- Both components: the word must match the world and the world must be made to
    match the word, at once. Searle's double direction of fit. -/
def Fit.isDouble (f : Fit) : Bool := f.wordToWorld && f.worldToWord

/-- Neither component: no commitment in either direction. -/
def Fit.isNull (f : Fit) : Bool := !f.wordToWorld && !f.worldToWord

/-- On the diagonal: the two components agree, whether both on or both off. -/
def Fit.isDiagonal (f : Fit) : Bool := f.wordToWorld == f.worldToWord

/-- The diagonal is exactly double-or-null — there is no third way for the
    components to agree. -/
theorem isDiagonal_iff_double_or_null (f : Fit) : f.isDiagonal = (f.isDouble || f.isNull) := by
  cases f with | mk w r => cases w <;> cases r <;> rfl

theorem declaration_is_double : (Block.fit .declaration).isDouble = true := rfl

theorem carrier_is_null : (Block.fit .carrier).isNull = true := rfl

/-- **THE SETTLEMENT, as a computation.** Exactly two blocks sit on the diagonal,
    and they are the declaration and the carrier. So the fork's presupposition —
    that there is ONE odd one out to be identified — is false in the model: there
    are two singular corners, and they are singular in dual ways rather than
    competing to be the same thing. -/
theorem double_and_null_are_the_only_diagonal :
    Block.all.filter (fun b => b.fit.isDiagonal) = [.declaration, .carrier] := rfl

theorem diagonal_card : (Block.all.filter (fun b => b.fit.isDiagonal)).length = 2 := rfl

/-- And the off-diagonal two are the single-fit ones: Facts and Rules carry one
    component each, which is why neither is singular in either of §4's senses. -/
theorem offDiagonal_is_facts_and_rules :
    Block.all.filter (fun b => !b.fit.isDiagonal) = [.assertive, .directive] := rfl

/-- The diagonal corners are distinct corners, not one corner described twice —
    stated because "dual, not rival" is the whole content of the settlement. -/
theorem double_is_not_null (f : Fit) : ¬(f.isDouble = true ∧ f.isNull = true) := by
  cases f with | mk w r => cases w <;> cases r <;> decide

/-! ### §4 The two entailments

This is where the settlement earns its keep. Each diagonal corner ENTAILS one of
the two properties that the fork treated as rival answers — depth-oddness for the
double corner, conversion-oddness for the null one — and each entailment is a
theorem about structure the earlier files already built, not a restatement of the
definition above. -/

/-- Which blocks are double, alongside `Surface.lean`'s depth distribution. The
    zero of `depth_counts` and the `true` of `isDouble` fall in the same position,
    and `depth_counts` is quoted by name rather than recomputed so the two lists
    are provably about the same four blocks in the same order. -/
theorem zero_sits_at_the_double :
    Block.all.map (fun b => (Block.depths b).length) = [3, 2, 0, 2] ∧
    Block.all.map (fun b => b.fit.isDouble) = [false, false, true, false] :=
  ⟨depth_counts, rfl⟩

/-- **(a) THE DOUBLE CORNER HAS NO DEPTHS.** The block whose fit is double has
    zero depths, in `Surface.lean`'s sense: no site of it is anything other than
    its own gross face.

    THE MODEL'S READING OF WHY THE ZERO IS FORCED, and it is a reading, offered
    because a bare `rfl` on `[3, 2, 0, 2]` explains nothing. A depth is a place
    where the GAP between saying and satisfying can be structured — how strongly
    the claim is held, under what rule it was derived, on what premise it rests,
    in what order the steps go. Double fit closes that gap: when the word must
    match the world and the world must be made to match the word in the same act,
    saying it IS satisfying it, and there is no interval left for an apparatus to
    live in. One cannot half-declare, cannot derive a declaration (it is the
    ground others are derived from), and cannot sequence a single constitutive
    act. The zero is not a gap in the enumeration; it is self-satisfaction.

    THE EMPIRICAL SHADOW, credited and NOT proved here, and NOT a measurement of
    this zero. `scratchpad/CONJUGATION_TEST_RESULTS.md` (12 of 12, model panel,
    2026-08-20) tested the DIRECTIVE block's missing strength depth: a change of
    deontic modal strength was read as Rules — content — rather than as
    Confidence, which is the panel confirming that satisfaction-conditions, not
    modulation, are what moved. That is the same gap-structure reading tested one
    block over. It says nothing about the declaration block, whose zero has no
    instrument pointed at it, and it is a fact about annotators either way. -/
theorem double_has_no_depth {b : Block} (h : b.fit.isDouble = true) :
    (Block.depths b).length = 0 := by
  cases b <;> first | rfl | exact absurd h (by decide)

/-- The converse, so the entailment is not one-sided: a block with no depths is
    the double one. Depth-oddness and double fit are the same corner. -/
theorem no_depth_is_double {b : Block} (h : (Block.depths b).length = 0) :
    b.fit.isDouble = true := by
  cases b <;> first | rfl | exact absurd h (by decide)

/-- The two directions in one Boolean identity. -/
theorem depth_zero_iff_double (b : Block) :
    ((Block.depths b).length == 0) = b.fit.isDouble := by
  cases b <;> rfl

/-- The null fit is exactly the carrier block — the bridge every §4(b) statement
    crosses to reach `Symmetry.lean`'s mention results. -/
theorem null_fit_iff_carrier {b : Block} (h : b.fit.isNull = true) : b = Block.carrier := by
  cases b <;> first | rfl | exact absurd h (by decide)

/-- The same as a Boolean identity, so it can be rewritten under. -/
theorem null_fit_eq_beq_carrier (b : Block) : b.fit.isNull = (b == Block.carrier) := by
  cases b <;> rfl

/-- **(b) THE NULL CORNER IS INERT UNDER MENTION.** Every site whose block has
    null fit is fixed by `Symmetry.lean`'s mention projection.

    THE READING: mention takes a commitment and reports it instead of making it,
    which is an operation ON a commitment. A null-fit block commits to nothing in
    either direction — it is the vehicle, not a claim about the world nor a demand
    on it — so there is nothing there to convert, and mention has no purchase.
    Inertness is not a further fact about Manner; it is null fit seen from the
    conversion side.

    `mention_fixes_carriers` is imported and used, not re-proved: the content of
    this theorem is the bridge from the fit coordinate to the existing result. -/
theorem null_is_inert {s : Site} (h : s.block.fit.isNull = true) : mentionTarget s = s :=
  mention_fixes_carriers (null_fit_iff_carrier h)

/-- The two-sided form, routed through `carrier_inert_under_mention` so the
    strong half of that theorem survives the translation: mention neither moves a
    null-fit site out of the null cell nor moves any other site into it. -/
theorem null_fit_inert_under_mention (s : Site) :
    (mentionTarget s).block.fit.isNull = s.block.fit.isNull := by
  rw [null_fit_eq_beq_carrier, null_fit_eq_beq_carrier]
  exact carrier_inert_under_mention s

/-- And the dual half, which is what makes the inertness singular rather than
    incidental: every NON-null surface is collapsed by mention onto the assertive
    one. Three convert to a single image, one does not participate. -/
theorem nonNull_surface_collapses {b : Block} (h : b.fit.isNull = false) :
    mentionTarget (Block.surface b) = Site.factContent := by
  cases b
  · exact mention_collapses_force_surfaces .assertive
  · exact mention_collapses_force_surfaces .directive
  · exact mention_collapses_force_surfaces .declarative
  · exact absurd h (by decide)

/-- **THE SPLIT, in one statement**: fit decides what mention does to a surface.
    Null, and it is fixed; anything else, and it lands on Facts. -/
theorem mention_splits_by_fit (b : Block) :
    (b.fit.isNull = true → mentionTarget (Block.surface b) = Block.surface b) ∧
    (b.fit.isNull = false → mentionTarget (Block.surface b) = Site.factContent) :=
  ⟨fun h => null_is_inert (by rw [surface_block]; exact h), fun h => nonNull_surface_collapses h⟩

/-! ### §5 Content-invariance is a DEFINITIONAL READING, not a theorem

READ THIS BEFORE QUOTING §4(b) IN SUPPORT OF ANYTHING. A bridge-note reading
(`scratchpad/N18_BRIDGE_NOTE.md`) proposes Manner as the structure's gauge
direction, on the ground that "gauge" means a transformation under which the
CONTENT is invariant. That reading needs "a Manner change leaves content
invariant". The honest question is whether this repository anywhere STATES that,
and the answer is:

**NO. `WrongKind.lean` does not state it, and nothing below proves it.** What
`WrongKind.lean` actually carries about `pragmatic` is three things, all recorded
as theorems here so a reader can check the gap rather than take this note's word
for it:

  * a CONSTRUCTOR DOCSTRING, "Register and address, not content" — prose attached
    to an inductive constructor, which no theorem reads and no gate enforces;
  * a DISCRIMINATOR STRING, "How is the same thing presented or used?"
    (`pragmatic_discriminator`) — where content-invariance is smuggled in by the
    phrase "the same thing", i.e. it is a presupposition of the question the
    classifier is asked, not a result;
  * a DISPOSITION, `holdUnlessStudied` (`pragmatic_disposition`) — which points
    the OTHER way: the taxonomy's own default is to hold Manner rather than vary
    it freely, and one does not hedge about varying something known to be
    content-free. Compare `contingent`, the label the taxonomy really does treat
    as carrying nothing: its disposition is `outOfScope`
    (`WrongKind.marker_matches_disposition`).

The strongest statement of it anywhere in the library is `Confront.lean`'s entry
10 (Leibniz's `dx` displacing Newton's dot), whose header calls content-preserving
re-expression "the whole content of a Manner change" and whose `plainWhy` field
says the same. That is prose and a string field of a record — a recorded reading
of a historical case, carrying exactly the weight `Epistemics.lean` gives a
`True`-valued field, which is none.

**AND THE NEAR-MISS THAT MUST NOT BE MISTAKEN FOR IT.** `WrongKind.assertsContent`
looks like the wanted property and is not: it asks whether the LABEL, once its
arguments are supplied, asserts anything about the artifact — not whether a change
of that kind preserves the artifact's content. It is `true` for `pragmatic`
(`pragmatic_assertsContent`), and `contingent` is the only label for which it is
false (`WrongKind.contingent_is_the_only_marker`). Reading `assertsContent` as
content-invariance would get the sign backwards.

So content-invariance of Manner changes is a DEFINITIONAL READING of the pragmatic
kind — it is what one means by putting a change under that label — and it is
therefore not available as an independent premise for the gauge reading. The gauge
reading may still be right; what it may not do is cite a theorem here, because
there is none, and a `null_fit_is_content_invariant` is deliberately ABSENT from
this file rather than proved cheaply against a definition that assumes it.

The empirical route, if anyone wants to close this: a panel item pairing
register-only rewrites against content-changing rewrites and measuring whether
downstream verdicts move. Unrun, unregistered, and not owed by any claim above. -/

theorem manner_is_the_null_surface : Block.grossKind .carrier = WrongKind.pragmatic := rfl

theorem manner_plain : (Block.grossKind .carrier).plain = "Manner" := rfl

theorem pragmatic_discriminator :
    WrongKind.pragmatic.discriminator = "How is the same thing presented or used?" := rfl

theorem pragmatic_disposition :
    WrongKind.pragmatic.disposition = Disposition.holdUnlessStudied := rfl

theorem pragmatic_assertsContent : WrongKind.pragmatic.assertsContent = true := rfl

/-! ### §6 What this file does and does not settle

**THE FORK IS SETTLED, AND IT WAS MALFORMED.** `scratchpad/DIMENSION_TABLE.md`
recorded two theorems singling out two different surfaces and read them as a
disagreement to be adjudicated. There was nothing to adjudicate: "which surface is
the odd one out" presumes a single distinguished cell, and the four surfaces are a
2×2 whose diagonal has two cells. Identity is odd by DEPTH because it is the
double corner (`double_has_no_depth`, with its converse `no_depth_is_double`);
Manner is odd by CONVERSION because it is the null corner (`null_is_inert`, with
its dual `nonNull_surface_collapses`). The two oddnesses are the two entailments
of the two dual corners, and Facts and Rules are the single-fit off-diagonal that
is odd in neither way. Nothing about the earlier theorems changes; only the
question they were both being asked to answer is retired.

**WHAT IS MECHANIZED, exactly, and it is the short list a reader should quote.**
That `Block.fit` is a bijection onto the four cells (`fit_bijection`); that
exactly two blocks are on the diagonal and which two
(`double_and_null_are_the_only_diagonal`); that double fit and zero depths are
equivalent (`depth_zero_iff_double`); and that null fit and mention-inertness
travel together in both directions (`null_fit_inert_under_mention`,
`nonNull_surface_collapses`). Everything else above is a docstring.

**THE READINGS ARE NOT MECHANIZED.** "There is no gap between saying and
satisfying, hence nowhere for a depth to live" is an explanation of a `rfl`, not a
derivation of it. The `rfl` would hold if the explanation were wrong. Same for
"nothing to convert" on the null side.

**THIS FILE INHERITS `Surface.lean`'s ONE MODELLING CHOICE.** Manner rather than
Structure as the carrier's surface is that file's declared free choice, grounded
in measured traffic and not in symmetry. Under the rival reading the null corner's
plain name is "Structure" and `fit_table_plain` moves with it. The 2×2 itself, the
diagonal, and both entailments are untouched — they are statements about BLOCKS,
and the rival changes only which site represents the carrier block. So the
settlement is robust to losing that argument; the ROSTER in `fit_table_plain` is
not, exactly as `gross_four` is not.

**AND THE PHYSICS IS NOT HERE.** The bridge note reads the null corner as a gauge
direction and the double corner as an in-plane time; those readings live in
`scratchpad/N18_BRIDGE_NOTE.md` to be attacked as the analogies they are, the
gauge one has an explicit warrant defect recorded in §5, and no theorem above
mentions either. The `rfl`s know nothing about gauge fields and nothing about
time. -/

end CIRISOntology.Core
