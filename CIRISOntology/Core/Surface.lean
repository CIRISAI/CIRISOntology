/-
CIRISOntology.Core.Surface — the gross/subtle decomposition of the eleven kinds:
**11 = 4 surfaces + 7 depths**, mechanized.

WHERE THIS CAME FROM. The session's 4+7 analysis (2026-08-19) started from a
MEASURED lopsidedness in wild change-traffic — four of the eleven kinds carry the
overwhelming majority of what actually gets labelled — and asked whether the four
are a diet artifact or a structural feature of the generator. This file answers
the second half only: the four ARE one-per-block surface representatives of the
site model's own block structure, and the remaining seven are those blocks'
depths, distributed 3 + 2 + 0 + 2. The traffic measurement is not proved here and
must not be read out of these theorems (see the closing note).

THE BLOCKS ARE NOT NEW. `Block` is exactly `Scan.lean`'s force fibration wearing
a name: three illocutionary forces plus the force-neutral carriers
(`block_is_force_fibre`). Nothing is chosen in defining it. All the modelling
risk in this file is concentrated in ONE definition, `Block.surface`, and it is
concentrated deliberately so that a critic has a single target.

HOW `Block.surface` IS GROUNDED, honestly and in two halves:

  * For the three FORCE blocks the surface is FORCED, and the forcing is a
    theorem rather than a claim (`force_surface_forced`). Searle's table — the
    same table `Generator.lean` transcribes to justify the site model — assigns
    each force its own content kind: assertives claim (Facts), directives
    require (Rules), declarations make-count-as (Identity). Within each block
    exactly one site carries that kind, and it is the block's surface. It is also
    the site the measured use/mention mechanism reads: what varies when the
    block's surface FORM varies is the force-content site, not the apparatus
    around it.

  * For the CARRIER block there is no force, hence no content kind, hence no
    forcing (`carrier_iff_forceless`). Taking `register` — Manner — as the
    carrier surface is THE ONE MODELING CHOICE IN THIS FILE that symmetry does
    not make for us. Its grounding is empirical, not structural: in the measured
    wild traffic Manner is the carrier block's gross attractor (40 of 279 modal
    labels, against Structure and Circumstances between them taking a small
    remainder). A critic who prefers `encoding` gets a different gross four, and
    every theorem below that mentions `pragmatic` moves with the choice. That is
    stated here, in the file, so it can be attacked where it lives — the rival
    reading is a two-line edit and its consequences are all in `gross_four`.

SCOPE. Everything below is THEOREM-GIVEN-MODEL in exactly `Generator.lean`'s
sense, and inherits its frame entirely: these are `rfl`s about a model, not
findings about the world.
-/

import CIRISOntology.Core.Scan

namespace CIRISOntology.Core

/-! ### The blocks: the force fibration, named -/

/-- The four blocks a site can belong to: the three illocutionary forces'
    apparatus, plus the force-neutral carrier layer. -/
inductive Block
  | assertive
  | directive
  | declaration
  | carrier
  deriving DecidableEq, Repr

/-- The blocks, in the canonical order used by every list statement below. -/
def Block.all : List Block := [.assertive, .directive, .declaration, .carrier]

/-- Which block a site belongs to. -/
def Site.block : Site → Block
  -- assertive apparatus: what is claimed, how strongly, under what rule, on what premise
  | .factContent        => .assertive
  | .strengthMarker     => .assertive
  | .appliedRule        => .assertive
  | .foundingAssumption => .assertive
  -- directive apparatus: what is required, in what preference order, in what step order
  | .directiveContent   => .directive
  | .preferenceOrder    => .directive
  | .stepOrder          => .directive
  -- declarative apparatus: what counts as what
  | .declarationContent => .declaration
  -- the force-neutral carriers
  | .encoding           => .carrier
  | .register           => .carrier
  | .instanceToken      => .carrier

/-- The block a force budget's fibre belongs to — `none` is the carrier layer. -/
def Block.ofForce : Option Force → Block
  | none              => .carrier
  | some .assertive   => .assertive
  | some .directive   => .directive
  | some .declarative => .declaration

/-- **THE BLOCKS ARE NOT A NEW MODELLING CHOICE.** `Site.block` is `Scan.lean`'s
    `Site.force` composed with a renaming — the same partition, no new content.
    Whatever grounding the force assignment has (and whatever attack it is open
    to — see `Scan.lean`'s contested `appliedRule` / `foundingAssumption` call)
    transfers here unchanged, and no additional grounding is owed for `Block`. -/
theorem block_is_force_fibre (s : Site) : s.block = Block.ofForce s.force := by
  cases s <;> rfl

/-- The carrier block is exactly the force-neutral fibre. Stated because it is
    the reason the carrier's surface cannot be forced the way the others are:
    there is no force there to supply a content kind. -/
theorem carrier_iff_forceless (s : Site) :
    (s.block == Block.carrier) = s.force.isNone := by
  cases s <;> rfl

/-- The sites of a block. -/
def Block.sites (b : Block) : List Site :=
  Site.all.filter (fun s => s.block == b)

/-- THE FIT-GRADING, as a computation: the blocks hold 4, 3, 1, 3 sites. This is
    the `4+3+1+3` the session's analysis names, and it sums to eleven. -/
theorem block_cards : Block.all.map (fun b => (Block.sites b).length) = [4, 3, 1, 3] := rfl

theorem block_cards_sum : (Block.all.map (fun b => (Block.sites b).length)).sum = 11 := rfl

/-! ### The surface of a block

One site per block is its GROSS face — the one whose variation is what the block
looks like from outside. For the three force blocks this is forced; for the
carrier it is chosen. See the header. -/

/-- THE ONE CHOICE IN THIS FILE. Assertive shows as its claim, directive as its
    requirement, declaration as its counts-as — each forced by Searle's table
    (`force_surface_forced`). The carrier shows as its register, which is the
    choice: grounded in measured wild traffic, not in force symmetry. -/
def Block.surface : Block → Site
  | .assertive   => .factContent
  | .directive   => .directiveContent
  | .declaration => .declarationContent
  | .carrier     => .register

/-- Searle's assignment of a content kind to each force, transcribed from
    `Generator.lean`'s header (assertives → Facts, directives → Rules,
    declarations → Identity). Prior art, not carved here. -/
def Force.contentKind : Force → ChoiceKind
  | .assertive   => .empirical
  | .directive   => .deontic
  | .declarative => .ontological

/-- **THE FORCING, AS A THEOREM.** For every force, exactly one site in that
    force's block carries the force's own content kind — and it is the block's
    surface. So three of the four surfaces are not chosen: pick the speech-act
    table (already independently motivated, already used by `Generator.lean`) and
    the surfaces fall out. The singleton on the right is the strong form: not
    merely that the surface has the content kind, but that nothing else does. -/
theorem force_surface_forced (f : Force) :
    (Block.sites (Block.ofForce (some f))).filter (fun s => s.kind == f.contentKind)
      = [Block.surface (Block.ofForce (some f))] := by
  cases f <;> rfl

/-- The carrier block has no force, so `Force.contentKind` has nothing to say
    about it — the negative half of `force_surface_forced`, and the exact place
    the modelling choice enters. -/
theorem carrier_sites_forceless :
    (Block.sites .carrier).filter (fun s => s.force.isNone) = Block.sites .carrier := rfl

/-- Every block's surface belongs to that block. -/
theorem surface_block (b : Block) : (Block.surface b).block = b := by
  cases b <;> rfl

/-- The same, as membership in the block's site list. -/
theorem surface_mem_block (b : Block) : Block.surface b ∈ Block.sites b := by
  cases b <;> repeat first | exact List.Mem.head _ | apply List.Mem.tail

/-- DISTINCT BLOCKS HAVE DISTINCT SURFACES — so the four surfaces really are
    four, and `Block.surface` is a section of the block map rather than a
    collapse. -/
theorem surface_injective (b₁ b₂ : Block) : Block.surface b₁ = Block.surface b₂ → b₁ = b₂ := by
  intro h
  cases b₁ <;> cases b₂ <;> first | rfl | exact absurd h (by decide)

/-! ### Surfaces and depths -/

/-- A site is a SURFACE when it is its own block's surface. -/
def Site.isSurface (s : Site) : Bool := decide (Block.surface s.block = s)

/-- Otherwise it is a DEPTH — a subtle site, whose variation the block does not
    wear on its face. -/
def Site.isDepth (s : Site) : Bool := !s.isSurface

/-- The surfaces, in `Site.all` order. -/
def surfaces : List Site := Site.all.filter Site.isSurface

/-- The depths, in `Site.all` order. -/
def depths : List Site := Site.all.filter Site.isDepth

/-- The depths of one block. -/
def Block.depths (b : Block) : List Site := (Block.sites b).filter Site.isDepth

/-- The surfaces are exactly the image of `Block.surface` — the definition by
    self-identification and the definition by image agree, which is what lets
    the count 4 below be read as "one per block". -/
theorem isSurface_iff_image (s : Site) :
    s.isSurface = true ↔ ∃ b : Block, Block.surface b = s := by
  constructor
  · intro h
    exact ⟨s.block, of_decide_eq_true h⟩
  · intro h
    cases h with
    | intro b hb =>
      cases hb
      show decide (Block.surface (Block.surface b).block = Block.surface b) = true
      rw [surface_block b]
      exact decide_eq_true rfl

/-- Every site is a surface or a depth, never both and never neither. -/
theorem surface_xor_depth (s : Site) : s.isSurface = !s.isDepth := by
  cases s <;> rfl

/-- FOUR SURFACES. -/
theorem gross_card : surfaces.length = 4 := rfl

/-- SEVEN DEPTHS. -/
theorem depth_card : depths.length = 7 := rfl

/-- **11 = 4 + 7**, tied to `Site.all` so the two counts are counts of the same
    eleven sites the generator enumerates. -/
theorem surface_depth_partition :
    surfaces.length + depths.length = Site.all.length := rfl

theorem eleven_is_four_plus_seven :
    surfaces.length = 4 ∧ depths.length = 7 ∧ Site.all.length = 11 := ⟨rfl, rfl, rfl⟩

/-- THE DEPTHS PER BLOCK: assertive 3, directive 2, declaration 0, carrier 2.
    The declaration block is the degenerate one — it is all surface, a single
    site with no apparatus behind it — and that zero is why the seven do not
    divide evenly. -/
theorem depth_counts : Block.all.map (fun b => (Block.depths b).length) = [3, 2, 0, 2] := rfl

theorem depth_counts_assertive : (Block.depths .assertive).length = 3 := rfl
theorem depth_counts_directive : (Block.depths .directive).length = 2 := rfl
theorem depth_counts_declaration : (Block.depths .declaration).length = 0 := rfl
theorem depth_counts_carrier : (Block.depths .carrier).length = 2 := rfl

theorem depth_counts_sum : (Block.all.map (fun b => (Block.depths b).length)).sum = 7 := rfl

/-- Each block's sites split into its one surface and its depths — the fit
    grading 4 + 3 + 1 + 3 read blockwise as (1+3) + (1+2) + (1+0) + (1+2). -/
theorem block_card_eq_one_add_depths (b : Block) :
    (Block.sites b).length = 1 + (Block.depths b).length := by
  cases b <;> rfl

/-! ### The gross four and the subtle seven, as kinds -/

/-- The kind a block wears on its face. -/
def Block.grossKind (b : Block) : ChoiceKind := (Block.surface b).kind

/-- **THE GROSS FOUR.** The image of `Block.surface` under `Site.kind` is exactly
    Facts, Rules, Identity, Manner. Three of the four are forced by the speech-act
    table (`force_surface_forced`); the fourth, Manner, carries the file's one
    modelling choice. -/
theorem gross_four :
    Block.all.map Block.grossKind = [.empirical, .deontic, .ontological, .pragmatic] := rfl

/-- The same four in the public vocabulary, because the plain names are the ones
    the traffic measurement was taken in. -/
theorem gross_four_plain :
    Block.all.map (fun b => (Block.grossKind b).plain) = ["Facts", "Rules", "Identity", "Manner"]
    := rfl

/-- Counting by block and counting by site agree — the four surfaces of
    `Block.all` are the four sites `Site.isSurface` selects, kind for kind. -/
theorem gross_four_agrees :
    Block.all.map Block.grossKind = surfaces.map Site.kind := rfl

/-- **THE SUBTLE SEVEN**: Confidence, Priorities, Process, Model, Premises,
    Structure, Circumstances. -/
theorem subtle_seven :
    depths.map Site.kind =
      [.epistemic, .axiotic, .procedural, .nomological, .axiomatic,
       .structural, .contingent] := rfl

theorem subtle_seven_plain :
    depths.map (fun s => s.kind.plain) =
      ["Confidence", "Priorities", "Process", "Model", "Premises",
       "Structure", "Circumstances"] := rfl

/-- Distinct blocks wear distinct gross kinds — immediate from
    `surface_injective` and `generator_injective`, stated because the gross four
    being FOUR is the load-bearing half of `11 = 4 + 7`. -/
theorem grossKind_injective (b₁ b₂ : Block) : Block.grossKind b₁ = Block.grossKind b₂ → b₁ = b₂ :=
  fun h => surface_injective b₁ b₂ (generator_injective _ _ h)

/-- The eleven kinds of the generator's image are exactly the four gross plus
    the seven subtle, counted. `generator_image` supplies the eleven; this splits
    them without loss or overlap. -/
theorem gross_plus_subtle_is_the_image :
    (Block.all.map Block.grossKind).length + (depths.map Site.kind).length
      = (Site.all.map Site.kind).length := rfl

/-! ### The rival reading, so the choice is visible rather than merely admitted

`Scan.lean` builds the reading it contests rather than defending it in prose.
Same discipline here: the alternative carrier surface is built, and what it moves
is computed. -/

/-- THE RIVAL: `encoding` — Structure — as the carrier's surface, on the reading
    that the vehicle's gross face is its serialization rather than its register. -/
def Block.surfaceAlt : Block → Site
  | .carrier => .encoding
  | b        => Block.surface b

/-- WHAT THE CHOICE MOVES, exactly: one of the four gross kinds and one of the
    seven subtle. Structure and Manner trade places; nothing else in the file
    changes, and in particular the counts 4 and 7 and the per-block depth
    distribution 3/2/0/2 are untouched. So the arithmetic `11 = 4 + 7` is robust
    to losing the argument in the header — the ROSTER of the gross four is not. -/
theorem surfaceAlt_moves_one_kind :
    Block.all.map (fun b => (Block.surfaceAlt b).kind) =
      [.empirical, .deontic, .ontological, .structural] := rfl

/-- And the three forced surfaces are untouched by the rival, as they must be:
    the choice lives entirely in the block that has no force. -/
theorem surfaceAlt_agrees_on_forces (f : Force) :
    Block.surfaceAlt (Block.ofForce (some f)) = Block.surface (Block.ofForce (some f)) := by
  cases f <;> rfl

/-! ### What this file does NOT prove — read before quoting a number from it

**The empirical face is MEASURED, elsewhere, and is not touched by any theorem
above.** The observation that motivated the decomposition — 91.4% of wild
change-traffic (255 of 279 modal labels across four unrelated streams) carried by
the gross four, with Model and Premises never once surfacing as a wild modal —
lives in the session record. It is stream-conditioned until it predicts forward,
and the forward test is staked in `scratchpad/GROSS4_FORWARD_PREREG.md` (frozen
2026-08-19, with its own kill: gross-four share below 2/3 on the never-sampled
stream). Nothing here confirms it, and the derivational `4 + 7` above does not
die with it if it fires — they are separate objects, and the prereg says so.

**The M-theory comparison is an art-pattern and is fenced.** `4 + 7` also names a
decomposition in another subject entirely; that resemblance is catalogued in
`scratchpad/N18_BRIDGE_NOTE.md`, where it can be attacked as the analogy it is,
and it is INTEGER-LEVEL numerology under this programme's own gate. It must never
be read back into these theorems as support, and no theorem above mentions it.
The `rfl`s here know nothing about spacetime.

**And the count is model-relative.** As with everything downstream of
`Generator.lean`, the honest question is not "are there really four gross kinds?"
but "is the site model adequate?" — which is answered by measurement (the
ecological no-fit rate), never by this file. -/

end CIRISOntology.Core
