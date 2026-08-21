# LEG A — every machine-checked result in `CIRISOntology/Core/` that constrains transitions between the eleven kinds

Swept 2026-08-21. All 35 files in `CIRISOntology/Core/` were opened; the 13 that mention
`WrongKind`/`ChoiceKind`/`Site` plus `Interferometer.lean` were read in full. Nothing here is
built or re-proved — every theorem cited was located by name in the file attributed to it.

---

## 0. The headline, before the tables

**The library contains no theorem about temporal succession between kinds.** There is no
relation anywhere in `Core/` of the form "a change of kind *i* may/may not be followed by a
change of kind *j*". What the library actually mechanizes is four **operations on a single
change** — grounding, modulation, mention, absorption — each a total or partial function
`Site → Site`, plus two **axis results** (Record/frame, warrant) and one **co-availability**
result. Every cell below is a cell of one of those, and the file is organised so the
distinction cannot be lost:

* **§1 Operation channels (G, M, N, A).** "Apply this operation to a kind-*i* change and you
  get a kind-*j* change." These are the four channels that fill cells. They are *not*
  precedence: `ground` is a modelling definition of what grounds what, `mention` is
  use/mention conversion, `absorb` is the block's gross face.
* **§2 Genuine precedence / licensing constraints.** Three, and they are the only ones: the
  Record axis (§2.1), the frame-supply obligation (§2.2), and force-budget co-availability
  (§2.3).
* **§3 Block-level no-goes.** Constraints on whole 4→3 or block↔block correspondences that
  fix no individual cell.
* **§4 The matrix summary**, with the count.
* **§5 What was checked and excluded**, with reasons — including the result that most limits
  how much of the map can *ever* be theorem-backed (§5.1).

**Count: 33 of the 121 ordered (source, target) cells carry a positive theorem-backed verdict
(ALLOWED, COLLAPSES, or CONDITIONAL) under at least one named channel. 22 of those are
off-diagonal; 11 are self-loop COLLAPSES. The remaining 88 carry no positive verdict.** On the
Record axis, 22 further cells (11 in, 11 out) are FORBIDDEN and 1 (the Record self-loop) is
CONDITIONAL-monotone.

**Index set.** Eleven artifact-local kinds — Priorities, Rules, Manner, Identity, Confidence,
Facts, Circumstances, Process, Model, Structure, Premises (`basePlane_card = 11`,
`WrongKind.lean`) — plus Record, which is provably not one of them
(`record_not_site_generated`, `Generator.lean`; `record_not_rsite_generated`,
`Generator2.lean`) and is handled as a separate axis throughout.

---

## 1. Operation channels

### 1.1 Channel G — the grounding step (`Stack.lean`)

**`ground : Rung → Rung`**, defined on the four assertive-stack kinds only
(`stack_kinds`: Premises, Model, Facts, Confidence). Values: `foundingAssumption ↦
appliedRule ↦ factContent ↦ strengthMarker ↦ strengthMarker`.

| theorem | file | statement | cells fixed |
|---|---|---|---|
| `ground_climbs` | Stack.lean | below the top, `(ground r).height = r.height + 1` | Premises→Model, Model→Facts, Facts→Confidence: **ALLOWED** (each is the value of the step, and it strictly climbs) |
| `ground_moves` | Stack.lean | below the top, `ground r ≠ r` | Premises→Premises, Model→Model, Facts→Facts: **FORBIDDEN** (no rung below the top grounds itself) |
| `ground_top_fixed`, `ground_three`, `ground_terminal` | Stack.lean | `ground strengthMarker = strengthMarker`; three steps from any rung reach the top; every iterate at or beyond three stays there | Confidence→Confidence: **COLLAPSES** (the step's unique fixed point; the stack terminates and generates no fifth rung) |
| `iterate_site_is_one_of_four`, `iterate_site_in_stack` | Stack.lean | every iterate of `ground`, from any rung, is one of `factContent`, `strengthMarker`, `appliedRule`, `foundingAssumption` | {Premises, Model, Facts, Confidence} → each of the seven off-stack kinds: **FORBIDDEN**, 28 cells. Grounding never leaves the stack |
| `terminal_kind` | Stack.lean | `Rung.strengthMarker.kind = epistemic` | the terminus is Confidence, a kind, not a remainder |
| `modulate_eq_climb` | Stack.lean | `modulate r = Nat.repeat ground 3 r` | channels G and M agree at three steps (see §1.2) |

**Status caveat, from the file's own header:** the ordering is *a definition, not a
discovery* — a modelling commitment about the assertive apparatus. The kill is empirical and
outside Lean. So G's four positive cells are theorem-backed *given the model*, and the model
is the thing at risk.

### 1.2 Channel M — modulation / hedging (`Stack.lean`)

**`modulate : Rung → Rung`**, constant at `strengthMarker` (`modulate_const`). Same four-kind
domain.

| theorem | file | statement | cells fixed |
|---|---|---|---|
| `modulate_const`, `modulate_site` | Stack.lean | `modulate r = strengthMarker` from any rung; its site is `Site.strengthMarker` | Premises→Confidence, Model→Confidence, Facts→Confidence: **ALLOWED**. Attaching a strength marker to any rung of the stack yields a Confidence-site change and nothing else |
| **`modulate_idempotent`** | Stack.lean | `modulate (modulate r) = modulate r` | Confidence→Confidence: **COLLAPSES**. A hedge of a hedge is a hedge |
| `modulate_nested` | Stack.lean | `Nat.repeat modulate (n+1) r = modulate r` for every `n` | the same self-loop at arbitrary depth: iterated hedging composes into one marker and creates no new site to classify |
| `modulate_top` | Stack.lean | `modulate strengthMarker = strengthMarker` | the self-loop's base case |

M and G assign different verdicts to the same 44 cells: (Premises, Model) is ALLOWED under G
and FORBIDDEN under M; (Facts, Confidence) is ALLOWED under both.

### 1.3 Channel N — mention / use-mention conversion (`Symmetry.lean` §4, `Fit.lean` §4b)

**`mentionTarget : Site → Site`**, total: `directiveContent ↦ factContent`,
`declarationContent ↦ factContent`, everything else fixed.

| theorem | file | statement | cells fixed |
|---|---|---|---|
| `mention_collapses_force_surfaces` | Symmetry.lean | every force block's surface goes to the assertive surface | Rules→Facts, Identity→Facts: **ALLOWED** |
| `mention_not_injective`, `mention_fibre_over_facts`, `mention_fibre_kinds_plain` | Symmetry.lean | Rules and Identity have the same image; the fibre over Facts is exactly {Facts, Rules, Identity} | {Rules, Identity} → Facts: **COLLAPSES** — three kinds share one image, and the merge is irreversible |
| **`mention_idempotent`** | Symmetry.lean | `mentionTarget (mentionTarget s) = mentionTarget s` | Facts→Facts: **COLLAPSES**. There is no second-order mention site |
| `mention_fixed_points`, `mention_rank`, `mention_loses_two` | Symmetry.lean | nine sites are fixed; the projection is rank 9 of 11 | nine self-loops **COLLAPSE**: Facts, Confidence, Priorities, Process, Model, Premises, Structure, Manner, Circumstances |
| **`carrier_inert_under_mention`**, `mention_fixes_carriers` | Symmetry.lean | `(mentionTarget s).block == carrier` iff `s.block == carrier`; every carrier site is fixed | {Structure, Manner, Circumstances} ↔ every other kind, both directions, and the carrier off-diagonal: **FORBIDDEN**, 54 cells. Nothing enters or leaves the carrier layer under mention |
| **`null_is_inert`**, `null_fit_inert_under_mention` | Fit.lean | every null-fit site is fixed by mention, and mention neither moves a null-fit site out of the null cell nor any other site into it | Manner's off-diagonal row and column: **FORBIDDEN**, 20 cells. This is the null corner of the direction-of-fit 2×2 (`carrier_is_null`) |
| `nonNull_surface_collapses`, `mention_splits_by_fit` | Fit.lean | every non-null surface lands on `factContent`; fit alone decides which of the two happens | the split is exactly by fit: null → fixed, anything else → Facts |
| `mention_not_structurePreserving`, `mention_changes_force` | Symmetry.lean | mention is not an automorphism and does not commute with the force fibration | N is a projection, not a symmetry — the collapse is not undoable inside the model |

### 1.4 Channel A — block absorption (`Residuals.lean` §6)

**`absorb (s) = Block.surface s.block`**, total: each site to its own block's gross face. The
file calls it "the channel `Surface.lean`'s block model predicts a confusion should follow".

| theorem | file | statement | cells fixed |
|---|---|---|---|
| `absorb_table` | Residuals.lean | the eleven values, computed | Confidence→Facts, Model→Facts, Premises→Facts, Priorities→Rules, Process→Rules, Structure→Manner, Circumstances→Manner: **ALLOWED**, 7 cells (each depth to its own block's surface) |
| **`absorb_idem`**, `absorb_surface`, `absorb_fixed_iff` | Residuals.lean | `absorb ∘ absorb = absorb`; the fixed points are exactly the four surfaces | Facts→Facts, Rules→Rules, Identity→Identity, Manner→Manner: **COLLAPSES**, 4 cells |
| `surface_block` (via `absorb`'s definition) | Surface.lean | a block's surface is in that block | absorption never crosses a block: every cross-block cell **FORBIDDEN** |
| **`depth_counts_declaration`** (`= 0`), **`double_has_no_depth`**, `no_depth_is_double`, `depth_zero_iff_double` | Surface.lean, Fit.lean | the declaration block has zero depths, and having zero depths is equivalent to double direction of fit (`declaration_is_double`) | **Identity's absorption column is empty**: every (i, Identity) with i ≠ Identity is **FORBIDDEN**, 10 cells. Nothing sits beneath Identity to be absorbed into it |
| `absorbing_is_not_any_label_residual` | Residuals.lean | no labelling of the eleven sites, of any type, has absorption's commutant as its residual | A is a structurally different sector from every label in the model — it is not a relabelling in disguise |

**Choice-dependence, flagged in `Surface.lean`'s own header.** Taking `register` (Manner)
rather than `encoding` (Structure) as the carrier's surface is that file's one declared free
modelling choice. Under the rival (`Block.surfaceAlt`, `surfaceAlt_moves_one_kind`) the three
carrier cells become Manner→Structure, Circumstances→Structure, Structure→Structure. The other
eight cells of channel A are forced by Searle's table (`force_surface_forced`) and do not move.

---

## 2. Genuine precedence / licensing constraints

These are the only results in `Core/` that constrain one change relative to another rather
than describing an operation on a single change.

### 2.1 The Record axis — one-way, and sealed in both directions

| theorem | file | statement | cells fixed |
|---|---|---|---|
| **`repairable_monotone`** | FrameOrder.lean | `FrameMonotone Repairable`: `f ⊑ g → Repairable a f → Repairable a g` | **Record → Record: CONDITIONAL(frame grows) = ALLOWED.** Enlarging the archive never destroys a verdict |
| **`no_frame_restriction`** | FrameOrder.lean | `¬ ∀ a f g, f ⊑ g → Repairable a g → Repairable a f` | **Record → Record: FORBIDDEN downward.** A verdict does not survive shrinking the archive. The axis is a copresheaf, not a presheaf — the file corrects the word explicitly |
| `frameMonotone_iff_upSet`, `order_structure_of_monotone` | FrameOrder.lean | monotonicity *is* upward closure, per fact | each fact determines an up-set of frames — the formal content of "one-way" |
| **`defeasible_not_monotone`**, `defeasible_in_neither_class` | FrameOrder.lean | monotonicity is FALSE of defeasible provability, exhibited in the same types | **the monotone cell is CONDITIONAL on the membership model.** The file's header says so in terms: `repairable_monotone` is a theorem about the model, a substantive assumption about the world, and needs its own kill if ever published as a claim about records |
| **`kinds_are_frame_scalars`** (= `frameInvariant_of_artifact_only` ∧ `repairable_does_not_factor` ∧ `record_not_site_generated`), `kind_is_frame_scalar`, `record_is_the_only_non_scalar` | Symmetry.lean, WrongKind.lean, Generator.lean | any discriminator reading only the artifact is frame-invariant; kind assignment has no frame argument; Record is the only one of the twelve labels claimed frame-mobile | **Record → each of the eleven: FORBIDDEN, 11 cells.** No supply or change of frame can move any artifact-local kind label |
| **`repairable_does_not_factor`**, `repairability_not_intrinsic`, `repairable_not_frameInvariant` | WrongKind.lean | no artifact-only property computes repairability; one fact and two corpora classify it oppositely | **each of the eleven → Record: FORBIDDEN, 11 cells.** No artifact-local change determines the Record verdict |
| **`nonfactoring_record`**, **`record_not_computable_from_artifact_reads`** | NonFactoring.lean | Record is an instance of the `NonFactoring` shape; the profile of *all* artifact-only readings does not determine repairability | the strictly stronger **joint** statement: the eleven *together* do not determine Record. This is the sharpest form of the column |
| `defeasible_does_not_factor` | FrameOrder.lean | non-factoring survives the loss of monotonicity | the FORBIDDEN column is robust where the monotone cell is not |
| `record_in_no_scan` | Scan.lean | `testimonial ∉ scan F` for every force budget `F` | no expressive resource whatever generates Record — the column is empty at every rung of the resource family |
| `record_not_site_generated`, `record_not_rsite_generated` | Generator.lean, Generator2.lean | no site — speech-act or recognition-grounded — maps to `testimonial` | the same column, under both groundings |
| `frames_are_not_gauge`, `gauge_orbits_are_contentless`, `gauge_sector_is_order_degeneracy`, `readingEq_iff_mutual_le` | FrameOrder.lean | no reading-invariant action on frames can relate arbitrary frames; any invariant action moves a frame only within its own mutual-inclusion class | **Record → Record via a content-preserving frame move: COLLAPSES.** The only gauge sector is the corpus's presentation (order and multiplicity, `reverseAction`), which is exactly the frame order's failure of antisymmetry (`frame_order_not_antisymmetric`) |
| `monotone_not_imp_frameInvariant`, `frameInvariant_imp_monotone` | FrameOrder.lean | the containment gauge-like ⊆ order-like is strict, with `Repairable` the separating witness | the Record axis is strictly inside the monotone class and strictly outside the invariant one |

### 2.2 The frame-supply obligation — the one construction-order constraint

| theorem | file | statement | cells fixed |
|---|---|---|---|
| `Reading.frameSupplied` (field), **`reading_record_has_frame`** | Instrument.lean | a `Reading` whose kind is frame-dependent cannot be constructed without a frame; a Record reading always carries one | **frame supply must PRECEDE a Record reading.** A frameless Record instrument is not cautious, it is wrong — it must refuse |
| `record_entry_has_frame`, **`only_the_record_entry_carries_a_frame`** | Confront.lean | across thirteen documented historical changes, exactly one carries a frame, and it is the Record one | the other eleven kinds carry **no** such precedence obligation — measured against a real corpus |
| `abc_repairability_is_frame_relative` | Confront.lean | `Repairable abcClaim abcFrameRIMS ∧ ¬ Repairable abcClaim abcFrameWider` | `repairability_not_intrinsic` in the wild: same documents, opposite verdicts |
| `self_declared_frame_undetermined` | WrongKind.lean | letting each block declare its own frame leaves the verdict turning on the declaration rule | the frame cannot be internalised into a twelfth kind — it belongs to the harness |
| **`no_reading_owes_design`**, `zero_design_dependent` | Instrument.lean, WrongKind.lean | no kind's reading owes a design; no label is claimed design-mobile | **the design axis imposes nothing on any cell.** `designDependent` was retracted 2026-08-18 by the PLANE study's own pinned rule; the design-relativity survives only in the *disposition* verdict for Circumstances |

### 2.3 Co-availability under the force budget (`Scan.lean`)

Not succession — **licensing by shared resource**: `Site.available` is per-force, so a kind's
sites exist only if its force is in the budget, and blockmates arrive together.

| theorem | file | statement | cells fixed |
|---|---|---|---|
| `scan_assertive` (7 kinds) | Scan.lean | assertion alone yields Facts, Confidence, Model, Premises + the three carriers | all 12 ordered pairs among {Facts, Confidence, Model, Premises}: **CONDITIONAL(same force budget)** — each is available iff the others are |
| `scan_assertive_directive` (10 kinds) | Scan.lean | adding the directive brings Rules, Priorities and Process *together* | all 6 ordered pairs among {Rules, Priorities, Process}: **CONDITIONAL(same force budget)** |
| `scan_full`, `scan_full_card` (11), `scan_terminal` | Scan.lean | all three forces give eleven, and any budget containing all three gives exactly that | Identity arrives alone with the declarative force — it has no co-availability partner |
| **`scan_mono`**, `availableSites_mono`, `scan_le_full` | Scan.lean | adding a force never removes a kind | **the resource axis is monotone**: no kind is destroyed by enlarging the budget |
| **`carriers_survive_everything`**, `carriers_in_every_scan`, `scan_floor` (3) | Scan.lean | Structure, Manner and Circumstances are in every scan, including the empty budget | those three are **unconditionally available** — nothing licenses them and they license nothing |
| `scan_lattice` | Scan.lean | the eight budgets give 3, 7, 6, 4, 10, 8, 7, 11 | the chain 7→10→11 is one path; the file warns against reading it as a discovered sequence |

**Choice-dependence.** `scanAlt_chain_agrees` / `scanAlt_floor`: under the rival reading in
which `appliedRule` and `foundingAssumption` are force-neutral carriers, Model and Premises
join the unconditional floor. Only 2 of the 12 assertive co-availability cells — (Facts,
Confidence) and (Confidence, Facts) — survive that rival; the other 10 are choice-dependent.
The 6 directive cells are unaffected.

---

## 3. Block-level no-goes (constrain a whole correspondence, fix no single cell)

| theorem | file | statement | what it forbids |
|---|---|---|---|
| **`no_fit_conjugation`** | Symmetry.lean | there is **no** injective `f : Site → Site` inducing the assertive↔directive swap on blocks | the four assertive-block kinds {Facts, Confidence, Model, Premises} cannot be put into one-to-one correspondence with the three directive-block kinds {Rules, Priorities, Process}. It dies on cardinality — 4 into 3 — so no refinement of "symmetry" repairs it. The hypothesis is bare injectivity, not `StructurePreserving`, so the failure is not an artifact of the other components |
| (the fork `no_fit_conjugation` opens) | Symmetry.lean | the missing site would be a *directive strength marker* | prong (b) — that deontic strength is content, filed under Rules, not modulation filed under Confidence — is **an explicit model commitment, NOT proved, and its panel test is unrun**. It fixes no cell. Do not read it as a Rules/Confidence constraint |
| `structurePreserving_never_conjugates` | Symmetry.lean | the 24 automorphisms preserve the block outright | the same, cheaply, for the model's own symmetries |
| `dirCarrierSwap_plain`, `dirCarrierSwap_absorbing`, `blockMap_dirCarrierSwap` | Residuals.lean | the directive block and the carrier layer **can** be interchanged wholesale in the absorption sector: Rules↔Manner, Priorities↔Structure, Process↔Circumstances | an exhibited block-level correspondence — the one the fit-conjugation lacks |
| `dirCarrierSwap_not_automorphism`, `dirCarrierSwap_against_the_ten` | Residuals.lean | but it is not in the automorphism group and it breaks force, mention, and all three kind-derived labels | so the directive/carrier interchange is real only in the absorption sector and nowhere else |

---

## 4. Matrix summary

### 4.1 The positive matrix (rows = source, columns = target)

Channel key: **G** grounding, **M** modulation, **N** mention, **A** absorption, **V**
co-availability. `=` marks a self-loop COLLAPSES.

| source \ target | Pri | Rul | Man | Ide | Con | Fac | Cir | Pro | Mod | Str | Pre |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Priorities** | =N | A | · | · | · | · | · | V | · | · | · |
| **Rules** | V | =A | · | · | · | N | · | V | · | · | · |
| **Manner** | · | · | =N,A | · | · | · | · | · | · | · | · |
| **Identity** | · | · | · | =A | · | N | · | · | · | · | · |
| **Confidence** | · | · | · | · | =N,G,M | A,V | · | · | V | · | V |
| **Facts** | · | · | · | · | G,M,V | =N,A | · | · | V | · | V |
| **Circumstances** | · | · | A | · | · | · | =N | · | · | · | · |
| **Process** | V | A,V | · | · | · | · | · | =N | · | · | · |
| **Model** | · | · | · | · | M,V | G,A,V | · | · | =N | · | V |
| **Structure** | · | · | A | · | · | · | · | · | · | =N | · |
| **Premises** | · | · | · | · | M,V | A,V | · | · | G,V | · | =N |

**33 filled cells: 11 self-loop COLLAPSES + 22 off-diagonal. 88 of 121 are EMPTY — the vast
majority of the matrix has no theorem-backed positive verdict of any kind.**

Per-row positive counts: Priorities 3, Rules 4, Manner 1, Identity 2, Confidence 4, Facts 4,
Circumstances 2, Process 3, Model 4, Structure 2, Premises 4.

### 4.2 Empty rows and columns worth naming

* **Manner's off-diagonal row is completely EMPTY** — no theorem in `Core/` sends a Manner
  change anywhere. It is the null corner of the fit 2×2 (`carrier_is_null`), inert under
  mention (`null_is_inert`), its own absorption target, and unconditionally available. Its
  column has exactly two entries, both from absorption.
* **Identity's off-diagonal column is EMPTY, and provably so** — 10 cells FORBIDDEN by
  `depth_counts_declaration = 0` / `double_has_no_depth`. Nothing lies beneath the double-fit
  corner. Its row has one entry, Identity→Facts under mention.
* **Circumstances' and Structure's off-diagonal columns are EMPTY.** Each row has exactly one
  entry (→ Manner, under absorption), and that entry is the choice-dependent one.
* The **assertive block** {Facts, Confidence, Model, Premises} is the only densely filled
  region: all 12 of its ordered pairs carry a verdict, from three different channels.

### 4.3 Substantively FORBIDDEN cells (beyond mere functionality)

73 of the 121 carry a FORBIDDEN verdict backed by a theorem that says more than "this function
has a different value there":

* 28 — grounding never leaves the stack (`iterate_site_is_one_of_four`).
* 54 — nothing enters or leaves the carrier layer under mention (`carrier_inert_under_mention`,
  `mention_fixes_carriers`, `null_fit_inert_under_mention`); 12 of these overlap the above.
* 10 — Identity's absorption column (`double_has_no_depth`); 7 overlap the above.

Union of positive and substantively-forbidden: 104 of 121, leaving 17 cells that no theorem
touches even generously. **The 104 must not be read as "the map is 86% done."** Channels N and
A are total functions, so they mechanically assign *some* verdict everywhere; the informative
content is the 33 positives and the three structural blocks listed above, not the coverage
figure.

The 17 wholly untouched cells are worth naming, because they are the directive-to-assertive
and Identity-outward directions — exactly where a transition map would most want a verdict:

* Priorities → {Confidence, Facts, Model, Premises}
* Rules → {Confidence, Model, Premises}
* Identity → {Priorities, Rules, Confidence, Process, Model, Premises}
* Process → {Confidence, Facts, Model, Premises}

### 4.4 The Record axis (12th index)

| | verdict | backing |
|---|---|---|
| Record → each of the 11 | **FORBIDDEN** (11 cells) | `kinds_are_frame_scalars`, `frameInvariant_of_artifact_only` |
| each of the 11 → Record | **FORBIDDEN** (11 cells) | `repairable_does_not_factor`, `record_not_site_generated`, `record_in_no_scan` |
| all 11 jointly → Record | **FORBIDDEN** (strictly stronger) | `record_not_computable_from_artifact_reads` |
| Record → Record, frame growing | **CONDITIONAL(membership model) ALLOWED** | `repairable_monotone`, killed for defeasible provability by `defeasible_not_monotone` |
| Record → Record, frame shrinking | **FORBIDDEN** | `no_frame_restriction` |
| Record → Record, content-preserving frame move | **COLLAPSES** | `gauge_orbits_are_contentless`, `gauge_sector_is_order_degeneracy` |

**The Record axis is the best-constrained object in the whole map**: its row and column are
both fully determined, and the determination is a genuine relational result rather than an
operation's table.

### 4.5 The warrant axis (not one of the 121)

| | verdict | backing |
|---|---|---|
| warrant → each of the 11 + Record | **FORBIDDEN** (12 cells) | `warrant_invisible_to_kind` — two blocks identical in every content field, differing only in whose say-so backs them, receive the same kind, necessarily |
| warrant → each disposition | **FORBIDDEN** (12 cells) | `warrant_invisible_to_policy` — no policy derived from the class alone responds to a change of source |

---

## 5. Checked and excluded, with reasons

### 5.1 The result that bounds how much of this map can ever be theorem-backed

`aut_with_stack` / `aut_with_stack_card` (Symmetry.lean): with *all* of the model's geometry
imposed — force, surface, block, fit, the grounding order — the automorphism group is still
the Klein four: **Priorities ↔ Process and Structure ↔ Circumstances remain freely
interchangeable.** `klein_under_the_kind_structures` and `structure_semantics_split`
(Residuals.lean) sharpen it: the Structure↔Circumstances transposition survives *every one* of
the five geometric structures and none of the three kind-derived ones.

**Consequence for LEG B onward: any transition claim that distinguishes Priorities from
Process, or Structure from Circumstances, cannot be backed by the model's geometry — a
symmetry of the model swaps them.** Two escapes exist and only two, both mechanized:
`sevenPlusAsserts_is_Z2` (content assertion separates Structure from Circumstances but not
Priorities from Process — it halves the Klein four) and `sevenPlusDisposition_is_trivial`
(the disposition table separates both, killing it outright). Both escapes descend from
`WrongKind.lean`'s claim table, which that file's own header labels **recorded claim, not
proof**. So a Priorities/Process transition distinction has *no* theorem-backed route at all,
and a Structure/Circumstances one has only a claim-backed route.

### 5.2 Excluded: relabelling symmetry results

`orbits_plain`, `orbits_plain_with_stack`, `aut_without_stack` (24), `aut_with_stack` (4),
`surfaces_are_rigid`, `stack_order_breaks_assertive_symmetry`, `sp_comp`, `sp_id`, all of
`Residuals.lean` §§1–5 (the ten residuals, `refinement_matrix`, `the_nineteen_mismatches`,
`resKind_is_trivial`, `resFit_eq_resBlock`, the calibration to 24 and 4). These compute which
*permutations of the labels* preserve which structure. A permutation of labels is not a
transition between them, and none of these fixes a cell. `stack_order_breaks_assertive_symmetry`
is the exception worth a second look and still does not fix a cell: it says the grounding order
is the *only* structure in the library that tells Confidence, Model and Premises apart — which
is a fact about §1.1's standing, recorded here rather than in the tables.

### 5.3 Excluded: derivation, counting and adequacy results

`generator_image`, `generator_injective`, `every_site_classified`, `basePlane_card`,
`one_frame_dependent`, `no_label_moves_with_both`, `scan_full_is_basePlane`,
`gross_card`/`depth_card`/`surface_depth_partition` (11 = 4 + 7), `block_cards`,
`force_surface_forced`, `gross_four`, `subtle_seven`, `fit_bijection`, `fit_surjective`,
`fit_injective`, `double_and_null_are_the_only_diagonal`, `rsite_all_length`,
`generator2_image`, `generator2_transport`, `transport_injective`, `stack_card`,
`four_sites_in_stack`, `seven_sites_outside_stack`. All say what the model *contains*, not
what may move to what. `double_has_no_depth` and `depth_counts_declaration` are the two
exceptions and are used in §1.4 for exactly one thing: the emptiness of Identity's absorption
column.

### 5.4 Excluded: the disposition table

`WrongKind.disposition`, `binding_never_varies` (Rules, Structure and Record never carry
`vary`), `axiomatic_binds_by_varying` (Premises does — "binding" is two words wearing one),
`marker_matches_disposition`, `contingent_is_the_only_marker`,
`circumstances_asserts_nothing` (Confront.lean:583 — the actual name the lead asked for; it is
`WrongKind.contingent.assertsContent = false` by `rfl`).

These are **row properties, not transition cells**: they say whether a *harness* may vary a
kind, not what a change of one kind does to another. `circumstances_asserts_nothing` comes
closest to forcing a row — Circumstances asserts nothing about the artifact, so nothing about
the artifact can be derived from a Circumstances label — but `WrongKind.lean`'s own header
states that everything in that section is a **recorded claim, not a proof**, and the theorems
check the claim table's internal consistency rather than its truth. `Confront.lean` uses it to
exclude Circumstances from a corpus of historical changes (no comparison design exists there to
be relative to), and `kinds_not_reached` pins that Priorities, Rules and Circumstances remain
unexercised by that corpus.

Related and also excluded: `assertsContent_fixes_circumstances` (Residuals.lean) — every
permutation preserving content assertion fixes Circumstances, because it is the unique
`assertsContent = false` site. That is relabelling rigidity, and it belongs to §5.1's story.

### 5.5 Excluded: `Interferometer.lean`

`ifo_edges_55`, `ifo_cycle_rank_45`, `ifo_param_count` (100), `ifo_edge_anatomy` (6 + 28 + 21).
This is the parameter bookkeeping of the K11 wager. It **presumes the complete graph** — one
channel per unordered pair of kinds — so it forbids nothing and licenses nothing. Its own
header marks it WAGER-CLASS, model-side only. It is, however, the natural home for a
transition map's arithmetic if LEG B wants one: 55 undirected channels, 45 independent loop
phases, and a 4+7 partition into 6 surface–surface, 28 cross, 21 depth–depth.

### 5.6 Excluded: everything outside the taxonomy

`Coordination`, `Third`, `Share*`, `Entropy*`, `HammingCap`, `BellCeiling`, `Creation`,
`Valve`, `Flavor`, `FlavorBridge`, `SignSymmetry`, `Maintenance`, `Intensive`,
`OppenheimRCLike`, `ThirdCap`, `Temporal`, `Provenance`, `Epistemics`. None mentions the kinds.
The one cross-over is `NonFactoring.lean`, which unifies `pairwise_blind_to_parity`,
`cp_phase_invisible_to_pairs` and `repairable_does_not_factor` under one typed shape; only its
third instance is used above. That file's own foot states the limit plainly and it is repeated
here: **a shared shape is not a shared quantity**, the identity of the whole-only share with
the Record coordinate is a wager recorded elsewhere, and nothing in `NonFactoring.lean` bears
on it.

---

## 6. Standing caveats that travel with every cell above

1. **THEOREM-GIVEN-MODEL, throughout.** Every file from `Generator.lean` down inherits that
   frame explicitly. These are `rfl`s and case bashes about an eleven-element inductive type.
   The open question is not "are these the transitions?" but "is the site model adequate?",
   which is answered by measurement and by no theorem cited here.
2. **The grounding order is a definition, not a discovery** (`Stack.lean` header). Channel G
   and channel M both stand or fall with it, and its kill is empirical: exhibit a change whose
   strength marking composes into a genuinely new site.
3. **Three cells are choice-dependent** (Structure/Circumstances/Manner under absorption) and
   **ten more** (the assertive co-availability pairs involving Model or Premises), on two
   declared free modelling choices — `Surface.lean`'s carrier surface and `Scan.lean`'s
   placement of `appliedRule`/`foundingAssumption`. Both files build the rival and compute what
   it moves.
4. **No measurement is support for any cell above, and no cell is support for any
   measurement.** `Symmetry.lean` §3–4, `Stack.lean`'s header and `Residuals.lean`
   `structure_semantics_split` all cite panel results (PLANE, 5,994 judgments; the confusion
   lines Premises→Facts, Model↔Facts, Structure→Manner; the TWO_WAY_READING leakage counts) and
   all three say the same thing in terms: annotators blurring a boundary is a fact about
   annotators. Those citations are quoted in no claim's `basis` and are quoted in none here.
