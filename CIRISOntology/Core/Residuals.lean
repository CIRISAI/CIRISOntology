/-
CIRISOntology.Core.Residuals — one structure at a time: what each piece of the
site model leaves free, and whether any two pieces disagree about it.

WHAT THIS FILE ASKS, and why the question has a shape worth borrowing.
`Symmetry.lean` computes the automorphism group of the site model with ALL its
structure imposed at once: force and surface together give 24, adding the
grounding order gives 4. That is a single number for the whole object. This file
takes the structures APART and computes, for each one ALONE, the subgroup of
permutations of the eleven sites that it fails to break — its RESIDUAL. Ten
structures, ten residuals, plus an eleventh channel that turns out not to be a
structure of the same kind at all (§6), and then the only question that matters:
do any two of them differ, and if so, is the difference a NESTING or a genuine
MISMATCH?

Seven of the ten are the site model's own geometry — force, surface, block, fit,
the grounding order, mention, the block-depth count. The last three descend from
`Generator.lean`'s kind map instead: the kind label itself, and `WrongKind.lean`'s
content-assertion flag and disposition table. That split is not decorative. It is
where the answer lives, because the two families disagree with each other
completely and a single transposition separates them (§4,
`structure_semantics_split`).

THE PLAYBOOK, named so the borrowing is visible rather than implied. In flavour
physics the observable content of the mixing matrix is not a symmetry group but
the MISALIGNMENT of two residual subgroups: a flavour symmetry is broken one way
in one sector and another way in another, each sector leaving its own residual
standing, and the mixing is the mismatch between the two bases those residuals
pick out. If the two residuals were nested — one contained in the other — there
would be nothing to mix, because one sector's basis would already diagonalise the
other. Mixing needs INCOMPARABILITY: two subgroups, neither containing the other.
So the question "does this structure have any mixing analogue at all?" becomes a
lattice computation, and that computation is the whole content here.

THE FENCE, and it is not decorative. That is a SHAPE borrowed to organise the
work. No theorem below says anything about flavour physics, about mixing angles,
or about CP violation; none may be quoted as evidence for any analogy; and the
comparison lives in `scratchpad/N18_BRIDGE_NOTE.md` where it can be attacked as
the analogy it is. What is actually below is `rfl`s and case bashes about an
eleven-element inductive type. In particular this file shares not one line with
`Core/FlavorBridge.lean`, which is about a three-bit probability family and is
equally fenced.

THE TWO PREDICTIONS, staked here in the header BEFORE the computations, because a
prediction written after the answer is not a prediction:

  * `resFit` CANNOT differ from `resBlock`. Direction of fit is a function of the
    block (`Fit.lean`'s `Site.fit s = s.block.fit`), so preserving the block
    preserves the fit for free; and `Fit.lean`'s `fit_injective` says the fit
    determines the block, so the implication runs back. The two constraints are
    the same constraint wearing different names, and the computation below should
    return identical partitions. If it did not, one of those two theorems would
    be wrong.
  * `resKind` MUST be trivial — the identity and nothing else. `Generator.lean`'s
    `generator_injective` makes the kind label injective on sites, so a
    kind-preserving map has nowhere to move anything. Stated so that the reader
    can see the extreme case: a structure fine enough to separate every site
    leaves no freedom at all, and a structure coarse enough to separate none
    would leave all of it.

Both are recorded as theorems below (`resFit_eq_resBlock`, `resKind_is_trivial`)
rather than as remarks, so that the prediction and its confirmation are the same
object.

WHAT IS MECHANIZED AND WHAT IS ARITHMETIC — read this before quoting a number.
A residual here is a Young subgroup: the label-preserving permutations of a
finite set, which is the product of the symmetric groups on the label's classes.
Two things follow, and they have DIFFERENT statuses in this file:

  * The PARTITION is mechanized. Each `res…` below is an explicit list of
    classes, checked against its own key by `isOrbitPartition` — every listed
    class is exactly an orbit, and the classes cover the eleven sites exactly
    once. That is a `rfl`, and the comparison results (§4) are theorems about
    permutations that never mention a count.
  * The ORDER is ARITHMETIC ON THE PARTITION. `residualOrder` multiplies the
    factorials of the class sizes. That the resulting number is the number of
    label-preserving bijections is the standard Young-subgroup count, and it is
    NOT proved here — no `Fintype`, no `Equiv.Perm`, no bijection is constructed.
    It is calibrated instead, at the two places where an independently mechanized
    count exists: the recipe returns 24 on the force-and-surface partition where
    `Symmetry.lean`'s `aut_without_stack_card` proves 24 by complete enumeration,
    and 4 on the joint partition of all seven non-kind structures — which §5 shows
    is exactly that file's force-surface-and-stack partition — where
    `aut_with_stack_card` proves 4. Two calibration points are two, not a proof.

SCOPE, inherited entirely from `Generator.lean`. Everything here is
THEOREM-GIVEN-MODEL. A residual of the model is not a residual of anything in the
world, and a mismatch between two of the model's structures is a fact about the
model. The honest question remains "is the site model adequate?", which is
answered by measurement and never by this file.
-/

import CIRISOntology.Core.Fit

namespace CIRISOntology.Core

/-! ### §0 The apparatus

Everything below runs on one idea: each structure of the site model is a LABEL on
sites, and the permutations it leaves standing are exactly the ones that never
move a site out of its label class. So a residual is presented by its partition
into classes, and comparing two residuals is comparing two partitions. -/

/-- **A RESIDUAL ELEMENT.** A permutation of the eleven sites that `key` does not
    break: injective (on an eleven-element type that is bijectivity — and every
    witness exhibited below is an explicit involution, so nothing is smuggled in
    by taking the weaker condition), and preserving the label.

    Deliberately the same shape as `Symmetry.lean`'s `StructurePreserving`, which
    is `Residual Site.force` and `Residual Site.isSurface` imposed together
    (`residual_forceSurface_iff_structurePreserving`, §5). -/
structure Residual {β : Type} (key : Site → β) (f : Site → Site) : Prop where
  /-- distinct sites go to distinct sites -/
  injective : ∀ s t : Site, f s = f t → s = t
  /-- the label of a site is untouched -/
  key_eq : ∀ s, key (f s) = key s

/-- The identity is in every residual, and residuals are closed under
    composition — so calling them subgroups below is earned rather than assumed.
    (Inverses come from finiteness, and every element exhibited in §4 is an
    explicit involution, so no appeal to finiteness is made anywhere.) -/
theorem residual_id {β : Type} (key : Site → β) : Residual key id :=
  ⟨fun _ _ h => h, fun _ => rfl⟩

theorem residual_comp {β : Type} {key : Site → β} {f g : Site → Site}
    (hf : Residual key f) (hg : Residual key g) : Residual key (f ∘ g) :=
  ⟨fun s t h => hg.injective s t (hf.injective _ _ h),
   fun s => (hf.key_eq (g s)).trans (hg.key_eq s)⟩

/-- Where a `key`-preserving map may send a site: everything wearing the same
    label. The direct analogue of `Symmetry.lean`'s `allowed`, written once and
    instantiated ten times so the ten answers are comparable. -/
def resOrbit {β : Type} [DecidableEq β] (key : Site → β) (s : Site) : List Site :=
  Site.all.filter (fun t => decide (key t = key s))

/-- The orbit function is a faithful re-encoding of the label: two sites have the
    same orbit exactly when they have the same label. This is what licenses §4's
    comparison matrix, which runs on orbit functions so that eight keys of eight
    different types can be compared in one computation. -/
theorem resOrbit_faithful {β : Type} [DecidableEq β] (key : Site → β) (a b : Site) :
    resOrbit key a = resOrbit key b ↔ key a = key b := by
  constructor
  · intro h
    have ha : a ∈ resOrbit key a :=
      List.mem_filter.mpr ⟨every_site_classified a, decide_eq_true rfl⟩
    rw [h] at ha
    exact of_decide_eq_true (List.mem_filter.mp ha).2
  · intro h
    show Site.all.filter _ = Site.all.filter _
    rw [h]

/-- A residual element sends a site into that site's orbit — the bridge from the
    Prop side to the computed partitions. -/
theorem residual_mem_orbit {β : Type} [DecidableEq β] {key : Site → β} {f : Site → Site}
    (h : Residual key f) (s : Site) : f s ∈ resOrbit key s :=
  List.mem_filter.mpr ⟨every_site_classified (f s), decide_eq_true (h.key_eq s)⟩

/-- **A SITE WITH A SINGLETON ORBIT IS FIXED BY THE WHOLE RESIDUAL.** The tool the
    content-assertion argument runs on (§4): a structure that marks exactly one
    site pins that site, and pins it for every permutation the structure
    admits. -/
theorem mem_single {a x : Site} (h : x ∈ [a]) : x = a := by
  cases h with
  | head => rfl
  | tail _ h => cases h

/-- Membership in a two-element orbit, narrowed. -/
theorem mem_pair {a b x : Site} (h : x ∈ [a, b]) : x = a ∨ x = b := by
  cases h with
  | head => exact Or.inl rfl
  | tail _ h =>
    cases h with
    | head => exact Or.inr rfl
    | tail _ h => cases h

theorem residual_fixes_of_singleton {β : Type} [DecidableEq β] {key : Site → β} {f : Site → Site}
    (h : Residual key f) {s : Site} (hs : resOrbit key s = [s]) : f s = s := by
  have hm := residual_mem_orbit h s
  rw [hs] at hm
  exact mem_single hm

/-- A residual is unchanged by re-encoding its key as an orbit function. -/
theorem residual_resOrbit_iff {β : Type} [DecidableEq β] (key : Site → β) (f : Site → Site) :
    Residual (resOrbit key) f ↔ Residual key f := by
  constructor
  · exact fun h => ⟨h.injective, fun s => (resOrbit_faithful key _ _).mp (h.key_eq s)⟩
  · exact fun h => ⟨h.injective, fun s => (resOrbit_faithful key _ _).mpr (h.key_eq s)⟩

/-- **THE PARTITION CHECK.** A list of classes presents `key`'s residual when
    every listed class is exactly the orbit of each of its members, and the
    classes together are the eleven sites, once each. Both halves are needed: the
    first without the second would allow classes to be dropped, the second
    without the first would allow them to be cut in the wrong places. -/
def isOrbitPartition {β : Type} [DecidableEq β] (key : Site → β) (cs : List (List Site)) : Bool :=
  cs.all (fun c => c.all (fun s => decide (resOrbit key s = c))) &&
  decide ((cs.foldr (fun c acc => c ++ acc) []).length = Site.all.length) &&
  Site.all.all (fun s => (cs.foldr (fun c acc => c ++ acc) []).contains s)

/-- Factorial, defined locally so this file needs no import beyond `Fit.lean`. -/
def residualFactorial : Nat → Nat
  | 0 => 1
  | n + 1 => (n + 1) * residualFactorial n

/-- **THE YOUNG ORDER OF A PARTITION**: the product of the factorials of the
    class sizes. ARITHMETIC ON THE PARTITION — see the header. That this counts
    the label-preserving bijections is standard and is not proved here; it is
    calibrated in §5 against `Symmetry.lean`'s two enumerated groups. -/
def residualOrder (cs : List (List Site)) : Nat :=
  cs.foldr (fun c n => residualFactorial c.length * n) 1

/-! #### Comparison

`Refines kx ky` says every permutation the first structure leaves standing is
also left standing by the second — subgroup containment, in the vocabulary of
partitions rather than of groups, since for these Young subgroups the two are the
same relation. -/

/-- Containment of residuals: `kx`'s residual sits inside `ky`'s. -/
def Refines {βx βy : Type} (kx : Site → βx) (ky : Site → βy) : Prop :=
  ∀ f : Site → Site, Residual kx f → Residual ky f

/-- Containment from the label side: if `kx` separating two sites is enough for
    `ky` to separate them, the residuals are nested. -/
theorem res_mono {βx βy : Type} {kx : Site → βx} {ky : Site → βy}
    (h : ∀ a b : Site, kx a = kx b → ky a = ky b) : Refines kx ky :=
  fun _ hf => ⟨hf.injective, fun s => h _ _ (hf.key_eq s)⟩

/-- The comparison, as a computation over the eleven sites. Runs on orbit
    functions so that keys of different types are comparable
    (`resOrbit_faithful`). -/
def refinesBool (kx ky : Site → List Site) : Bool :=
  Site.all.all (fun a => Site.all.all (fun b =>
    !decide (kx a = kx b) || decide (ky a = ky b)))

theorem refinesBool_sound {kx ky : Site → List Site} (h : refinesBool kx ky = true)
    (a b : Site) (hab : kx a = kx b) : ky a = ky b := by
  have h1 := List.all_eq_true.mp h a (every_site_classified a)
  have h2 := List.all_eq_true.mp h1 b (every_site_classified b)
  rw [decide_eq_true hab] at h2
  exact of_decide_eq_true h2

/-- **EVERY `true` IN §4's MATRIX IS A CONTAINMENT.** The computed Boolean is not
    left as a computed Boolean: it is discharged into a statement about
    permutations. -/
theorem refines_of_matrix {βx βy : Type} [DecidableEq βx] [DecidableEq βy]
    {kx : Site → βx} {ky : Site → βy}
    (h : refinesBool (resOrbit kx) (resOrbit ky) = true) : Refines kx ky :=
  res_mono (fun a b hab =>
    (resOrbit_faithful ky a b).mp (refinesBool_sound h a b ((resOrbit_faithful kx a b).mpr hab)))

/-! #### Witnesses

Every `false` in the matrix is discharged too, and by exhibiting a permutation
rather than by appealing to the computation: a transposition of two sites that
one structure cannot tell apart and the other can. That transposition IS the
mismatch object where one exists. -/

/-- The transposition of two sites. -/
def swapSite (a b : Site) : Site → Site :=
  fun s => if s = a then b else if s = b then a else s

theorem swapSite_left (a b : Site) : swapSite a b a = b := if_pos rfl

theorem swapSite_right (a b : Site) : swapSite a b b = a := by
  show (if b = a then b else if b = b then a else b) = a
  by_cases h : b = a
  · rw [if_pos h]; exact h
  · rw [if_neg h, if_pos rfl]

theorem swapSite_other {a b s : Site} (h1 : s ≠ a) (h2 : s ≠ b) : swapSite a b s = s := by
  show (if s = a then b else if s = b then a else s) = s
  rw [if_neg h1, if_neg h2]

/-- A transposition is an involution, hence a genuine permutation — the witnesses
    below are bijections and not merely injections. -/
theorem swapSite_involutive (a b s : Site) : swapSite a b (swapSite a b s) = s := by
  by_cases h1 : s = a
  · subst h1; rw [swapSite_left, swapSite_right]
  · by_cases h2 : s = b
    · subst h2; rw [swapSite_right, swapSite_left]
    · rw [swapSite_other h1 h2, swapSite_other h1 h2]

theorem inj_of_involutive {f : Site → Site} (h : ∀ s, f (f s) = s) :
    ∀ s t : Site, f s = f t → s = t := by
  intro s t hst
  rw [← h s, hst, h t]

/-- A transposition of two sites sharing a label preserves that label. -/
theorem swapSite_preserves {β : Type} {key : Site → β} {a b : Site} (h : key a = key b) (s : Site) :
    key (swapSite a b s) = key s := by
  by_cases h1 : s = a
  · subst h1; rw [swapSite_left]; exact h.symm
  · by_cases h2 : s = b
    · subst h2; rw [swapSite_right]; exact h
    · rw [swapSite_other h1 h2]

/-- The residual of `key` contains the transposition of any two sites `key`
    cannot tell apart. -/
theorem residual_swapSite {β : Type} {key : Site → β} {a b : Site} (h : key a = key b) :
    Residual key (swapSite a b) :=
  ⟨inj_of_involutive (swapSite_involutive a b), swapSite_preserves h⟩

/-- **NON-CONTAINMENT, WITNESSED.** Two sites that `kx` merges and `ky` separates
    give a permutation in `kx`'s residual and not in `ky`'s. Every `false` in §4
    is discharged through this lemma, so no comparison result rests on a Boolean
    computation alone. -/
theorem not_refines_of_pair {βx βy : Type} {kx : Site → βx} {ky : Site → βy} {a b : Site}
    (hx : kx a = kx b) (hy : ky a ≠ ky b) : ¬ Refines kx ky := by
  intro hr
  have := (hr _ (residual_swapSite hx)).key_eq a
  rw [swapSite_left] at this
  exact hy this.symm

/-! ### §1 The ten structures, and their residuals

Each structure is a labelling of the eleven sites, taken from the file that
introduced it and never re-declared here. Two of the ten need a name they did
not already have: the mention projection is not a label but a MAP, so §3 derives
the label it is equivalent to; and the block-depth count needs to be read as a
per-site quantity. The last two, content assertion and disposition, come from
`WrongKind.lean` rather than from the site geometry, which is exactly why they
turn out to disagree with all of it. -/

/-- The per-site block-depth count: how many depths the site's block has, read
    off `Surface.lean`'s `depth_counts` — the multiset [3, 2, 0, 2] worn as a
    label by each site of the corresponding block. -/
def Site.depthCount (s : Site) : Nat := (Block.depths s.block).length

theorem depthCount_values :
    Site.all.map Site.depthCount = [3, 3, 2, 0, 2, 2, 3, 3, 2, 2, 2] := rfl

/-- The label the mention projection turns out to be equivalent to (§3): the
    assertive surface, the two sites that collapse onto it, and everything the
    projection fixes. -/
def mentionClass : Site → Nat
  | .factContent        => 0
  | .directiveContent   => 1
  | .declarationContent => 1
  | _                   => 2

/-! #### 1. Force -/

/-- **THE RESIDUAL OF THE FORCE FIBRATION** (`Scan.lean`'s `Site.force`): the
    three illocutionary blocks and the force-neutral carriers, each free
    internally. -/
def resForce : List (List Site) :=
  [[.factContent, .strengthMarker, .appliedRule, .foundingAssumption],
   [.directiveContent, .preferenceOrder, .stepOrder],
   [.declarationContent],
   [.encoding, .register, .instanceToken]]

theorem resForce_is_the_partition : isOrbitPartition Site.force resForce = true := rfl

theorem resForce_plain :
    resForce.map (fun c => c.map (fun s => s.kind.plain)) =
      [["Facts", "Confidence", "Model", "Premises"],
       ["Rules", "Priorities", "Process"],
       ["Identity"],
       ["Structure", "Manner", "Circumstances"]] := rfl

theorem resForce_order : residualOrder resForce = 864 := rfl

/-! #### 2. Surface -/

/-- **THE RESIDUAL OF THE SURFACE/DEPTH SPLIT** (`Surface.lean`'s
    `Site.isSurface`): two classes only, the four gross faces and the seven
    depths, and this is by far the loosest of the eight. -/
def resSurface : List (List Site) :=
  [[.factContent, .directiveContent, .declarationContent, .register],
   [.strengthMarker, .preferenceOrder, .stepOrder, .appliedRule, .foundingAssumption,
    .encoding, .instanceToken]]

theorem resSurface_is_the_partition : isOrbitPartition Site.isSurface resSurface = true := rfl

theorem resSurface_plain :
    resSurface.map (fun c => c.map (fun s => s.kind.plain)) =
      [["Facts", "Rules", "Identity", "Manner"],
       ["Confidence", "Priorities", "Process", "Model", "Premises",
        "Structure", "Circumstances"]] := rfl

theorem resSurface_order : residualOrder resSurface = 120960 := rfl

/-! #### 3. Block -/

/-- **THE RESIDUAL OF THE BLOCK STRUCTURE** (`Surface.lean`'s `Site.block`).
    Written out independently rather than defined to be `resForce`, so that their
    agreement is a computed result and not a definition. -/
def resBlock : List (List Site) :=
  [[.factContent, .strengthMarker, .appliedRule, .foundingAssumption],
   [.directiveContent, .preferenceOrder, .stepOrder],
   [.declarationContent],
   [.encoding, .register, .instanceToken]]

theorem resBlock_is_the_partition : isOrbitPartition Site.block resBlock = true := rfl

theorem resBlock_order : residualOrder resBlock = 864 := rfl

/-! #### 4. Fit -/

/-- **THE RESIDUAL OF THE DIRECTION OF FIT** (`Fit.lean`'s `Site.fit`, which is
    `Block.fit ∘ Site.block`). Predicted in the header to coincide with
    `resBlock`; written out independently for the same reason. -/
def resFit : List (List Site) :=
  [[.factContent, .strengthMarker, .appliedRule, .foundingAssumption],
   [.directiveContent, .preferenceOrder, .stepOrder],
   [.declarationContent],
   [.encoding, .register, .instanceToken]]

theorem resFit_is_the_partition : isOrbitPartition Site.fit resFit = true := rfl

theorem resFit_order : residualOrder resFit = 864 := rfl

/-! #### 5. Stack -/

/-- **THE RESIDUAL OF THE GROUNDING ORDER** (`Symmetry.lean`'s
    `Site.stackHeight`, which reads `Stack.lean`'s `Rung.height`): the four rungs
    are pinned outright, because the four heights are four
    (`stackHeight_distinguishes_rungs`), and the seven off-ladder sites are
    completely free of one another. -/
def resStack : List (List Site) :=
  [[.factContent],
   [.strengthMarker],
   [.appliedRule],
   [.foundingAssumption],
   [.directiveContent, .declarationContent, .preferenceOrder, .stepOrder,
    .encoding, .register, .instanceToken]]

theorem resStack_is_the_partition : isOrbitPartition Site.stackHeight resStack = true := rfl

theorem resStack_plain :
    resStack.map (fun c => c.map (fun s => s.kind.plain)) =
      [["Facts"], ["Confidence"], ["Model"], ["Premises"],
       ["Rules", "Identity", "Priorities", "Process",
        "Structure", "Manner", "Circumstances"]] := rfl

theorem resStack_order : residualOrder resStack = 5040 := rfl

/-! #### 6. Mention -/

/-- **THE RESIDUAL OF THE MENTION PROJECTION** (`Symmetry.lean`'s
    `mentionTarget`). This one is not given as a label by any earlier file: the
    constraint is COMMUTATION with a map, `f ∘ mentionTarget = mentionTarget ∘ f`,
    and §3 proves it equivalent to preserving `mentionClass`. The partition is
    the assertive surface alone, the two sites that collapse onto it, and the
    nine-minus-one that the projection fixes. -/
def resMention : List (List Site) :=
  [[.factContent],
   [.directiveContent, .declarationContent],
   [.strengthMarker, .preferenceOrder, .stepOrder, .appliedRule, .foundingAssumption,
    .encoding, .register, .instanceToken]]

theorem resMention_is_the_partition : isOrbitPartition mentionClass resMention = true := rfl

theorem resMention_plain :
    resMention.map (fun c => c.map (fun s => s.kind.plain)) =
      [["Facts"],
       ["Rules", "Identity"],
       ["Confidence", "Priorities", "Process", "Model", "Premises",
        "Structure", "Manner", "Circumstances"]] := rfl

theorem resMention_order : residualOrder resMention = 80640 := rfl

/-! #### 7. Depth count -/

/-- **THE RESIDUAL OF THE BLOCK-DEPTH COUNT** (`Surface.lean`'s `depth_counts`
    read per site). Strictly coarser than the block itself, and for one reason
    only: the directive and carrier blocks both hold two depths, so this label
    cannot tell them apart. The 3/2/0/2 of `depth_counts` has a repeat in it, and
    the repeat is the whole difference. -/
def resDepthCount : List (List Site) :=
  [[.factContent, .strengthMarker, .appliedRule, .foundingAssumption],
   [.directiveContent, .preferenceOrder, .stepOrder, .encoding, .register, .instanceToken],
   [.declarationContent]]

theorem resDepthCount_is_the_partition : isOrbitPartition Site.depthCount resDepthCount = true :=
  rfl

theorem resDepthCount_plain :
    resDepthCount.map (fun c => c.map (fun s => s.kind.plain)) =
      [["Facts", "Confidence", "Model", "Premises"],
       ["Rules", "Priorities", "Process", "Structure", "Manner", "Circumstances"],
       ["Identity"]] := rfl

theorem resDepthCount_order : residualOrder resDepthCount = 17280 := rfl

/-! #### 8. Kind -/

/-- **THE RESIDUAL OF THE KIND LABEL** (`Generator.lean`'s `Site.kind`): eleven
    singletons, because the generator map is injective. -/
def resKind : List (List Site) :=
  [[.factContent], [.strengthMarker], [.directiveContent], [.declarationContent],
   [.preferenceOrder], [.stepOrder], [.appliedRule], [.foundingAssumption],
   [.encoding], [.register], [.instanceToken]]

theorem resKind_is_the_partition : isOrbitPartition Site.kind resKind = true := rfl

theorem resKind_order : residualOrder resKind = 1 := rfl

/-! #### 9. Content assertion

The first of two structures that are not geometry at all. `Site.kind` is injective,
so anything factoring through it is a coarsening of the finest possible partition
rather than a cut of the site model's own shape — which is exactly why these two
can disagree with the seven above. -/

/-- Whether a site's kind asserts something about the artifact
    (`WrongKind.assertsContent`). -/
def Site.assertsContent (s : Site) : Bool := s.kind.assertsContent

/-- **THE RESIDUAL OF CONTENT ASSERTION.** Two classes, and the second is a
    singleton: `WrongKind.lean`'s `contingent_is_the_only_marker` proves that
    Circumstances is the UNIQUE kind carrying no content, so this structure marks
    exactly one site and merges the other ten. It is by a wide margin the loosest
    residual here — and, as §4 shows, that does not stop it disagreeing with
    everything. -/
def resAssertsContent : List (List Site) :=
  [[.factContent, .strengthMarker, .directiveContent, .declarationContent,
    .preferenceOrder, .stepOrder, .appliedRule, .foundingAssumption, .encoding, .register],
   [.instanceToken]]

theorem resAssertsContent_is_the_partition :
    isOrbitPartition Site.assertsContent resAssertsContent = true := rfl

theorem resAssertsContent_plain :
    resAssertsContent.map (fun c => c.map (fun s => s.kind.plain)) =
      [["Facts", "Confidence", "Rules", "Identity", "Priorities", "Process",
        "Model", "Premises", "Structure", "Manner"],
       ["Circumstances"]] := rfl

theorem resAssertsContent_order : residualOrder resAssertsContent = 3628800 := rfl

/-! #### 10. Disposition -/

/-- What a harness may do with a change of this site's kind
    (`WrongKind.disposition`). -/
def Site.disposition (s : Site) : Disposition := s.kind.disposition

/-- **THE RESIDUAL OF THE DISPOSITION TABLE.** Six classes, one per policy. Note
    what it separates that no structural label does: Priorities from Process (vary
    against hold) and Structure from Circumstances (cannotVary against outOfScope)
    — the two swaps that survive everything in §5. -/
def resDisposition : List (List Site) :=
  [[.factContent, .declarationContent, .stepOrder, .appliedRule],
   [.strengthMarker, .register],
   [.directiveContent],
   [.preferenceOrder, .foundingAssumption],
   [.encoding],
   [.instanceToken]]

theorem resDisposition_is_the_partition :
    isOrbitPartition Site.disposition resDisposition = true := rfl

theorem resDisposition_plain :
    resDisposition.map (fun c => c.map (fun s => s.kind.plain)) =
      [["Facts", "Identity", "Process", "Model"],
       ["Confidence", "Manner"],
       ["Rules"],
       ["Priorities", "Premises"],
       ["Structure"],
       ["Circumstances"]] := rfl

theorem resDisposition_policies :
    resDisposition.map (fun c => c.map Site.disposition) =
      [[.hold, .hold, .hold, .hold],
       [.holdUnlessStudied, .holdUnlessStudied],
       [.replaceWithReview],
       [.vary, .vary],
       [.cannotVary],
       [.outOfScope]] := rfl

theorem resDisposition_order : residualOrder resDisposition = 96 := rfl

/-! #### The table -/

/-- **THE TEN ORDERS**, in the order the structures are introduced above: force,
    surface, block, fit, stack, mention, depth count, kind, content assertion,
    disposition. ARITHMETIC ON THE PARTITIONS — see the header, and §5 for the two
    calibration points. The ambient group is all 11! = 39,916,800 permutations of
    the eleven sites, so every one of these is a proper subgroup: even the
    loosest, content assertion's 10! = 3,628,800, is about nine percent of the
    ambient, and the loosest of the seven structural ones is under a third of one
    percent. -/
theorem residuals_table :
    [residualOrder resForce, residualOrder resSurface, residualOrder resBlock,
     residualOrder resFit, residualOrder resStack, residualOrder resMention,
     residualOrder resDepthCount, residualOrder resKind,
     residualOrder resAssertsContent, residualOrder resDisposition] =
      [864, 120960, 864, 864, 5040, 80640, 17280, 1, 3628800, 96] := rfl

/-- The number of classes, which is the more honest headline of the ten: how
    finely each structure cuts the eleven. Kind cuts them into eleven, content
    assertion into two. -/
theorem residuals_class_counts :
    [resForce.length, resSurface.length, resBlock.length, resFit.length,
     resStack.length, resMention.length, resDepthCount.length, resKind.length,
     resAssertsContent.length, resDisposition.length] =
      [4, 2, 4, 4, 5, 3, 3, 11, 2, 6] := rfl

/-! ### §2 The two predicted coincidences, at the level of permutations

The partitions above agree for force, block and fit, and that agreement is not an
accident of how the lists were typed: it follows from two theorems the earlier
files already proved. Both directions are stated, because a coincidence of
partitions is only a coincidence of residuals if the labels determine each
other. -/

/-- Block is a function of force — `Surface.lean`'s `block_is_force_fibre`. -/
theorem force_determines_block (a b : Site) : a.force = b.force → a.block = b.block := by
  intro h
  rw [block_is_force_fibre, block_is_force_fibre, h]

/-- And force is a function of block: `Block.ofForce` is injective, so the
    fibration loses nothing. -/
theorem block_determines_force (a b : Site) : a.block = b.block → a.force = b.force := by
  intro h
  cases a <;> cases b <;> first | rfl | exact absurd h (by decide)

/-- Fit is a function of block, by definition. -/
theorem block_determines_fit (a b : Site) : a.block = b.block → a.fit = b.fit := by
  intro h
  show a.block.fit = b.block.fit
  rw [h]

/-- And block is a function of fit — `Fit.lean`'s `fit_injective`. -/
theorem fit_determines_block (a b : Site) : a.fit = b.fit → a.block = b.block :=
  fun h => fit_injective _ _ h

/-- **PREDICTION CONFIRMED (1/2): FIT AND BLOCK ARE THE SAME CONSTRAINT**, and so
    is force. Not merely equal partitions — equal sets of permutations, in both
    directions, for the reason stated in the header. -/
theorem resFit_eq_resBlock :
    (∀ f : Site → Site, Residual Site.fit f ↔ Residual Site.block f) ∧
    (∀ f : Site → Site, Residual Site.block f ↔ Residual Site.force f) := by
  refine ⟨fun f => ⟨?_, ?_⟩, fun f => ⟨?_, ?_⟩⟩
  · exact fun h => res_mono fit_determines_block f h
  · exact fun h => res_mono block_determines_fit f h
  · exact fun h => res_mono block_determines_force f h
  · exact fun h => res_mono force_determines_block f h

/-- The same at the level of the enumerated partitions, which is what makes the
    three rows and columns of §4's matrix identical. -/
theorem resFit_partition_eq : resFit = resBlock ∧ resBlock = resForce := ⟨rfl, rfl⟩

/-- Kind separates every pair of distinct sites, so it refines every structure
    whatsoever — including any structure a later file might add. -/
theorem kind_refines_all {β : Type} (key : Site → β) :
    ∀ a b : Site, a.kind = b.kind → key a = key b :=
  fun a b h => by rw [generator_injective a b h]

/-- **PREDICTION CONFIRMED (2/2): THE KIND LABEL LEAVES NOTHING FREE.** A
    kind-preserving map is the identity, pointwise. This is the floor of the
    eight: no structure can have a smaller residual, because none can be finer
    than a partition into singletons. -/
theorem resKind_is_trivial {f : Site → Site} (h : Residual Site.kind f) : ∀ s, f s = s :=
  fun s => generator_injective _ _ (h.key_eq s)

/-- And the identity is in it, so the residual of kind is exactly the trivial
    group and not the empty set. -/
theorem resKind_has_identity : Residual Site.kind id := ⟨fun _ _ h => h, fun _ => rfl⟩

/-! ### §3 The mention residual is a label after all

Nine of the ten structures are labels on sites. The other is not: mention is
a MAP, and `Symmetry.lean` proves it is a projection rather than a symmetry —
idempotent, not injective, collapsing three surfaces onto one. The residual of a
map is the permutations that COMMUTE with it, which is a different kind of
condition. This section shows it comes to the same thing, and the derivation is
the only real content in this file that is not a case bash: commutation with the
projection forces the assertive surface to be fixed, and that in turn forces the
three-class partition. -/

/-- **THE CONSTRAINT MENTION IMPOSES**: a permutation that commutes with the
    projection. Note that this asks nothing about force, surface, block or kind —
    it is stated purely in terms of `mentionTarget`. -/
structure MentionCommuting (f : Site → Site) : Prop where
  /-- distinct sites go to distinct sites -/
  injective : ∀ s t : Site, f s = f t → s = t
  /-- and mentioning then moving is moving then mentioning -/
  commutes : ∀ s, f (mentionTarget s) = mentionTarget (f s)

/-- **THE ASSERTIVE SURFACE IS FIXED BY EVERY COMMUTING PERMUTATION**, and the
    argument needs only injectivity, not surjectivity. If Rules went somewhere
    that mention fixes, then Facts would have to go there too, and the map would
    not be injective; so Rules goes to something mention moves, and everything
    mention moves lands on Facts. -/
theorem mentionCommuting_fixes_fact {f : Site → Site} (h : MentionCommuting f) :
    f Site.factContent = Site.factContent := by
  have hd : f Site.factContent = mentionTarget (f Site.directiveContent) :=
    h.commutes Site.directiveContent
  cases he : f Site.directiveContent <;> rw [he] at hd <;>
    first
      | exact hd
      | exact absurd (h.injective _ _ (hd.trans he.symm)) (by decide)

/-- A site the projection fixes goes to a site the projection fixes. -/
theorem mentionCommuting_rest {f : Site → Site} (h : MentionCommuting f) {s : Site}
    (hs : mentionTarget s = s) (hne : s ≠ Site.factContent) : mentionClass (f s) = 2 := by
  have hfc := mentionCommuting_fixes_fact h
  have hc := h.commutes s
  rw [hs] at hc
  cases hx : f s <;> rw [hx] at hc <;>
    first
      | rfl
      | exact absurd hc (by decide)
      | exact absurd (h.injective _ _ (hx.trans hfc.symm)) hne

/-- A site the projection moves goes to a site the projection moves. -/
theorem mentionCommuting_pair {f : Site → Site} (h : MentionCommuting f) {s : Site}
    (hs : mentionTarget s = Site.factContent) (hne : s ≠ Site.factContent) :
    mentionClass (f s) = 1 := by
  have hfc := mentionCommuting_fixes_fact h
  have hc := h.commutes s
  rw [hs, hfc] at hc
  cases hx : f s <;> rw [hx] at hc <;>
    first
      | rfl
      | exact absurd hc (by decide)
      | exact absurd (h.injective _ _ (hx.trans hfc.symm)) hne

/-- **COMMUTING WITH MENTION IMPLIES PRESERVING THE THREE-CLASS LABEL.** -/
theorem mentionCommuting_preserves_class {f : Site → Site} (h : MentionCommuting f) (s : Site) :
    mentionClass (f s) = mentionClass s := by
  have hfc := mentionCommuting_fixes_fact h
  cases s
  case factContent => rw [hfc]
  case directiveContent => exact mentionCommuting_pair h rfl (by decide)
  case declarationContent => exact mentionCommuting_pair h rfl (by decide)
  case strengthMarker => exact mentionCommuting_rest h rfl (by decide)
  case preferenceOrder => exact mentionCommuting_rest h rfl (by decide)
  case stepOrder => exact mentionCommuting_rest h rfl (by decide)
  case appliedRule => exact mentionCommuting_rest h rfl (by decide)
  case foundingAssumption => exact mentionCommuting_rest h rfl (by decide)
  case encoding => exact mentionCommuting_rest h rfl (by decide)
  case register => exact mentionCommuting_rest h rfl (by decide)
  case instanceToken => exact mentionCommuting_rest h rfl (by decide)

/-- **AND CONVERSELY** — and this direction does not even need injectivity, which
    is worth stating: the label is not merely necessary for commutation, it is
    the whole of it. -/
theorem mention_commutes_of_class {f : Site → Site}
    (hk : ∀ s, mentionClass (f s) = mentionClass s) :
    ∀ s, f (mentionTarget s) = mentionTarget (f s) := by
  have hfc : f Site.factContent = Site.factContent := by
    have h0 := hk Site.factContent
    cases hx : f Site.factContent <;> rw [hx] at h0 <;>
      first | rfl | exact absurd h0 (by decide)
  have hfix : ∀ s, mentionClass s = 2 → f s = mentionTarget (f s) := by
    intro s h2
    have hs := hk s
    rw [h2] at hs
    cases hx : f s <;> rw [hx] at hs <;>
      first | rfl | exact absurd hs (by decide)
  have hpair : ∀ s, mentionClass s = 1 → mentionTarget (f s) = Site.factContent := by
    intro s h1
    have hs := hk s
    rw [h1] at hs
    cases hx : f s <;> rw [hx] at hs <;>
      first | rfl | exact absurd hs (by decide)
  intro s
  cases s
  case factContent =>
    show f Site.factContent = mentionTarget (f Site.factContent)
    rw [hfc]
    rfl
  case directiveContent =>
    show f Site.factContent = mentionTarget (f Site.directiveContent)
    rw [hfc, hpair Site.directiveContent rfl]
  case declarationContent =>
    show f Site.factContent = mentionTarget (f Site.declarationContent)
    rw [hfc, hpair Site.declarationContent rfl]
  case strengthMarker => exact hfix _ rfl
  case preferenceOrder => exact hfix _ rfl
  case stepOrder => exact hfix _ rfl
  case appliedRule => exact hfix _ rfl
  case foundingAssumption => exact hfix _ rfl
  case encoding => exact hfix _ rfl
  case register => exact hfix _ rfl
  case instanceToken => exact hfix _ rfl

/-- **THE MENTION RESIDUAL IS A LABEL RESIDUAL.** Commuting with the projection
    and preserving `mentionClass` are the same condition on permutations, so the
    eighth structure joins the other seven and the comparison in §4 is a
    comparison of like with like. -/
theorem mentionCommuting_iff_residual (f : Site → Site) :
    MentionCommuting f ↔ Residual mentionClass f :=
  ⟨fun h => ⟨h.injective, mentionCommuting_preserves_class h⟩,
   fun h => ⟨h.injective, mention_commutes_of_class h.key_eq⟩⟩

/-! ### §4 The comparison — and the answer

The lattice, computed. Rows and columns are in the order force, surface, block,
fit, stack, mention, depth count, kind; entry (i, j) is `true` when the i-th
residual is contained in the j-th. Every `true` becomes a theorem about
permutations through `refines_of_matrix`; every `false` is discharged separately
by an exhibited transposition, so nothing below rests on the computation alone. -/

/-- The ten structures as orbit functions, so that ten keys of ten
    different types can be compared in one computation
    (`resOrbit_faithful` is what licenses this). -/
def residualOrbits : List (Site → List Site) :=
  [resOrbit Site.force, resOrbit Site.isSurface, resOrbit Site.block, resOrbit Site.fit,
   resOrbit Site.stackHeight, resOrbit mentionClass, resOrbit Site.depthCount,
   resOrbit Site.kind, resOrbit Site.assertsContent, resOrbit Site.disposition]

/-- **THE CONTAINMENT MATRIX.** Read the near-emptiness off the diagonal: apart
    from the force/block/fit block, two nestings (force inside depth count,
    disposition inside content assertion), and the kind row (which is trivially
    inside everything), NO residual contains another. The structures of the site
    model are, with those exceptions, mutually incomparable — and the two
    kind-derived structures added last are incomparable with all seven of the
    geometric ones, in both directions. -/
theorem refinement_matrix :
    residualOrbits.map (fun kx => residualOrbits.map (fun ky => refinesBool kx ky)) =
      [[true,  false, true,  true,  false, false, true,  false, false, false],
       [false, true,  false, false, false, false, false, false, false, false],
       [true,  false, true,  true,  false, false, true,  false, false, false],
       [true,  false, true,  true,  false, false, true,  false, false, false],
       [false, false, false, false, true,  false, false, false, false, false],
       [false, false, false, false, false, true,  false, false, false, false],
       [false, false, false, false, false, false, true,  false, false, false],
       [true,  true,  true,  true,  true,  true,  true,  true,  true,  true],
       [false, false, false, false, false, false, false, false, true,  false],
       [false, false, false, false, false, false, false, false, true,  true]] := rfl

/-! #### The fifteen pairwise verdicts

Six distinct residuals (force, block and fit being one), hence fifteen unordered
pairs. Each is settled here in the strong form: either a containment with a
witness for its strictness, or a MISMATCH with a witness in each direction. -/

/-- **THE HEADLINE. FORCE AND SURFACE ARE MISALIGNED.** Neither residual contains
    the other, and each direction is witnessed by an explicit transposition:

      * Facts ↔ Confidence is a symmetry of the force fibration — both are
        assertive apparatus — and is not a symmetry of the surface/depth split,
        because Facts is its block's gross face and Confidence is a depth.
      * Facts ↔ Rules is a symmetry of the surface/depth split — both are gross
        faces — and is not a symmetry of the force fibration, because one is
        assertive and the other directive.

    THOSE TWO TRANSPOSITIONS ARE THE MISMATCH OBJECT. They are what
    `Symmetry.lean`'s 24 is the intersection of: force alone leaves 864 standing,
    surface alone leaves 120,960, and imposing both at once leaves 24, which is
    smaller than either — the two structures are cutting the eleven in
    incompatible directions rather than one refining the other. -/
theorem force_surface_mismatch :
    ¬ Refines Site.force Site.isSurface ∧ ¬ Refines Site.isSurface Site.force :=
  ⟨not_refines_of_pair (a := Site.factContent) (b := Site.strengthMarker) rfl (by decide),
   not_refines_of_pair (a := Site.factContent) (b := Site.directiveContent) rfl (by decide)⟩

/-- Force against the grounding order: mismatched. Confidence ↔ Model is a
    force symmetry the ladder breaks (`Symmetry.lean`'s
    `stack_order_breaks_assertive_symmetry`, the same map seen from here); Rules ↔
    Structure is a ladder symmetry the force breaks, because both are off the
    ladder and they are in different blocks. -/
theorem force_stack_mismatch :
    ¬ Refines Site.force Site.stackHeight ∧ ¬ Refines Site.stackHeight Site.force :=
  ⟨not_refines_of_pair (a := Site.strengthMarker) (b := Site.appliedRule) rfl (by decide),
   not_refines_of_pair (a := Site.directiveContent) (b := Site.encoding) rfl (by decide)⟩

/-- Force against mention: mismatched. Facts ↔ Confidence is a force symmetry
    mention breaks; Rules ↔ Identity is a mention symmetry the force breaks —
    which is exactly `mention_fibre_over_facts` seen as a residual, since those
    two sites are the ones the projection identifies. -/
theorem force_mention_mismatch :
    ¬ Refines Site.force mentionClass ∧ ¬ Refines mentionClass Site.force :=
  ⟨not_refines_of_pair (a := Site.factContent) (b := Site.strengthMarker) rfl (by decide),
   not_refines_of_pair (a := Site.directiveContent) (b := Site.declarationContent) rfl (by decide)⟩

/-- **THE ONE NESTING.** The depth count is strictly coarser than the force:
    every force symmetry preserves the count, and Rules ↔ Structure preserves the
    count without preserving the force. So this pair carries no mismatch — the
    depth count is the block structure with the 2 of the directive block and the
    2 of the carrier block confused, and nothing more. -/
theorem force_depthCount_nested :
    Refines Site.force Site.depthCount ∧ ¬ Refines Site.depthCount Site.force :=
  ⟨res_mono (fun a b h => by
      show (Block.depths a.block).length = (Block.depths b.block).length
      rw [force_determines_block a b h]),
   not_refines_of_pair (a := Site.directiveContent) (b := Site.encoding) rfl (by decide)⟩

/-- Force against kind: nested the other way, and strictly. Priorities ↔ Process
    is the witness, and it is the witness for every one of the five kind pairs
    below — the one transposition that every structure except kind admits. -/
theorem force_kind_nested :
    Refines Site.kind Site.force ∧ ¬ Refines Site.force Site.kind :=
  ⟨res_mono (kind_refines_all Site.force),
   not_refines_of_pair (a := Site.preferenceOrder) (b := Site.stepOrder) rfl (by decide)⟩

/-- Surface against the grounding order: mismatched. -/
theorem surface_stack_mismatch :
    ¬ Refines Site.isSurface Site.stackHeight ∧ ¬ Refines Site.stackHeight Site.isSurface :=
  ⟨not_refines_of_pair (a := Site.factContent) (b := Site.directiveContent) rfl (by decide),
   not_refines_of_pair (a := Site.directiveContent) (b := Site.encoding) rfl (by decide)⟩

/-- Surface against mention: mismatched. The second witness is the interesting
    one — Confidence ↔ Manner is invisible to the projection (neither site
    participates in use/mention) and visible to the surface split, since Manner is
    the carrier block's gross face and Confidence is a depth. -/
theorem surface_mention_mismatch :
    ¬ Refines Site.isSurface mentionClass ∧ ¬ Refines mentionClass Site.isSurface :=
  ⟨not_refines_of_pair (a := Site.factContent) (b := Site.directiveContent) rfl (by decide),
   not_refines_of_pair (a := Site.strengthMarker) (b := Site.register) rfl (by decide)⟩

/-- Surface against the depth count: mismatched. -/
theorem surface_depthCount_mismatch :
    ¬ Refines Site.isSurface Site.depthCount ∧ ¬ Refines Site.depthCount Site.isSurface :=
  ⟨not_refines_of_pair (a := Site.factContent) (b := Site.directiveContent) rfl (by decide),
   not_refines_of_pair (a := Site.factContent) (b := Site.strengthMarker) rfl (by decide)⟩

theorem surface_kind_nested :
    Refines Site.kind Site.isSurface ∧ ¬ Refines Site.isSurface Site.kind :=
  ⟨res_mono (kind_refines_all Site.isSurface),
   not_refines_of_pair (a := Site.preferenceOrder) (b := Site.stepOrder) rfl (by decide)⟩

/-- The grounding order against mention: mismatched. -/
theorem stack_mention_mismatch :
    ¬ Refines Site.stackHeight mentionClass ∧ ¬ Refines mentionClass Site.stackHeight :=
  ⟨not_refines_of_pair (a := Site.directiveContent) (b := Site.encoding) rfl (by decide),
   not_refines_of_pair (a := Site.strengthMarker) (b := Site.encoding) rfl (by decide)⟩

/-- The grounding order against the depth count: mismatched. Identity ↔ Manner is
    the first witness — both off the ladder, and their blocks hold 0 and 2 depths
    respectively, so the count separates what the ladder cannot see. -/
theorem stack_depthCount_mismatch :
    ¬ Refines Site.stackHeight Site.depthCount ∧ ¬ Refines Site.depthCount Site.stackHeight :=
  ⟨not_refines_of_pair (a := Site.declarationContent) (b := Site.register) rfl (by decide),
   not_refines_of_pair (a := Site.factContent) (b := Site.strengthMarker) rfl (by decide)⟩

theorem stack_kind_nested :
    Refines Site.kind Site.stackHeight ∧ ¬ Refines Site.stackHeight Site.kind :=
  ⟨res_mono (kind_refines_all Site.stackHeight),
   not_refines_of_pair (a := Site.preferenceOrder) (b := Site.stepOrder) rfl (by decide)⟩

/-- Mention against the depth count: mismatched. -/
theorem mention_depthCount_mismatch :
    ¬ Refines mentionClass Site.depthCount ∧ ¬ Refines Site.depthCount mentionClass :=
  ⟨not_refines_of_pair (a := Site.strengthMarker) (b := Site.encoding) rfl (by decide),
   not_refines_of_pair (a := Site.factContent) (b := Site.strengthMarker) rfl (by decide)⟩

theorem mention_kind_nested :
    Refines Site.kind mentionClass ∧ ¬ Refines mentionClass Site.kind :=
  ⟨res_mono (kind_refines_all mentionClass),
   not_refines_of_pair (a := Site.preferenceOrder) (b := Site.stepOrder) rfl (by decide)⟩

theorem depthCount_kind_nested :
    Refines Site.kind Site.depthCount ∧ ¬ Refines Site.depthCount Site.kind :=
  ⟨res_mono (kind_refines_all Site.depthCount),
   not_refines_of_pair (a := Site.preferenceOrder) (b := Site.stepOrder) rfl (by decide)⟩

/-! #### The two kind-derived structures against the seven geometric ones

Thirteen more pairs. Ten are mismatches and the pattern in them is not scattered:
ONE transposition — Structure ↔ Circumstances — is in every geometric residual and
in none of the kind-derived ones, and it accounts for all five of the
"geometric ⊄ content-assertion" directions at once. -/

/-- **THE ARGUMENT, MECHANIZED.** Content assertion marks exactly one site
    (`contingent_is_the_only_marker`: Circumstances is the unique kind with
    `assertsContent = false`), and a structure that marks exactly one site pins it.
    So every permutation preserving content assertion fixes Circumstances. -/
theorem assertsContent_fixes_circumstances {f : Site → Site}
    (h : Residual Site.assertsContent f) : f Site.instanceToken = Site.instanceToken :=
  residual_fixes_of_singleton h rfl

/-- Structure ↔ Circumstances, in whatever residual it fits — the reusable form,
    since this one transposition is the load-bearing witness below. -/
theorem residual_swapEncodingToken {β : Type} {key : Site → β}
    (h : key Site.encoding = key Site.instanceToken) : Residual key swapEncodingToken :=
  ⟨inj_of_involutive swapEncodingToken_involutive, fun s => by
    cases s <;> first | rfl | exact h.symm | exact h⟩

/-- **THE SPLIT, IN ONE STATEMENT.** Structure ↔ Circumstances survives every one
    of the five geometric structures — force, surface, the grounding order,
    mention, and the depth count — and survives none of the three kind-derived
    ones. It is a generator of `Symmetry.lean`'s Klein four, so a symmetry the
    model's whole geometry admits is broken by the content-assertion label alone.

    THE MEASURED CORROBORATION, credited and NOT proved here, and not evidence for
    anything above. On the authored corpus (`scratchpad/TWO_WAY_READING.md`, BASE
    modal against authored target, ties excluded) the two sites this transposition
    exchanges behave nothing alike under panel confusion: Structure → Manner 7 and
    Structure → Facts 0, against Circumstances → Manner 1 and Circumstances →
    Facts 9. Structure leaks to its own block's surface, as the block model would
    have it; Circumstances leaks across blocks to Facts. So a swap the geometry
    calls free is one the measured behaviour does not respect. That is a fact about
    annotators, it confirms no theorem here, and no theorem here predicts it — the
    honest relation is that the two point the same way. -/
theorem structure_semantics_split :
    (Residual Site.force swapEncodingToken ∧
     Residual Site.isSurface swapEncodingToken ∧
     Residual Site.stackHeight swapEncodingToken ∧
     Residual mentionClass swapEncodingToken ∧
     Residual Site.depthCount swapEncodingToken) ∧
    (¬ Residual Site.assertsContent swapEncodingToken ∧
     ¬ Residual Site.disposition swapEncodingToken ∧
     ¬ Residual Site.kind swapEncodingToken) := by
  refine ⟨⟨residual_swapEncodingToken rfl, residual_swapEncodingToken rfl,
           residual_swapEncodingToken rfl, residual_swapEncodingToken rfl,
           residual_swapEncodingToken rfl⟩, ?_, ?_, ?_⟩ <;>
    exact fun h => absurd (h.key_eq Site.encoding) (by decide)

/-- And it is in the Klein four, quoted as a table so the claim is literally
    against `Symmetry.lean`'s enumeration rather than against a re-derivation. -/
theorem klein_generator_broken_by_assertsContent :
    autWithStack.contains (Site.all.map swapEncodingToken) = true ∧
    ¬ Residual Site.assertsContent swapEncodingToken :=
  ⟨rfl, structure_semantics_split.2.1⟩

theorem force_assertsContent_mismatch :
    ¬ Refines Site.force Site.assertsContent ∧ ¬ Refines Site.assertsContent Site.force :=
  ⟨not_refines_of_pair (a := Site.encoding) (b := Site.instanceToken) rfl (by decide),
   not_refines_of_pair (a := Site.factContent) (b := Site.directiveContent) rfl (by decide)⟩

theorem surface_assertsContent_mismatch :
    ¬ Refines Site.isSurface Site.assertsContent ∧ ¬ Refines Site.assertsContent Site.isSurface :=
  ⟨not_refines_of_pair (a := Site.encoding) (b := Site.instanceToken) rfl (by decide),
   not_refines_of_pair (a := Site.factContent) (b := Site.strengthMarker) rfl (by decide)⟩

/-- **THE PAIR THE ARGUMENT WAS ABOUT.** The grounding order and content assertion
    are mismatched, with Structure ↔ Circumstances the witness in one direction and
    Facts ↔ Confidence in the other. -/
theorem stack_assertsContent_mismatch :
    ¬ Refines Site.stackHeight Site.assertsContent ∧
    ¬ Refines Site.assertsContent Site.stackHeight :=
  ⟨not_refines_of_pair (a := Site.encoding) (b := Site.instanceToken) rfl (by decide),
   not_refines_of_pair (a := Site.factContent) (b := Site.strengthMarker) rfl (by decide)⟩

theorem mention_assertsContent_mismatch :
    ¬ Refines mentionClass Site.assertsContent ∧ ¬ Refines Site.assertsContent mentionClass :=
  ⟨not_refines_of_pair (a := Site.encoding) (b := Site.instanceToken) rfl (by decide),
   not_refines_of_pair (a := Site.factContent) (b := Site.strengthMarker) rfl (by decide)⟩

theorem depthCount_assertsContent_mismatch :
    ¬ Refines Site.depthCount Site.assertsContent ∧
    ¬ Refines Site.assertsContent Site.depthCount :=
  ⟨not_refines_of_pair (a := Site.encoding) (b := Site.instanceToken) rfl (by decide),
   not_refines_of_pair (a := Site.factContent) (b := Site.directiveContent) rfl (by decide)⟩

theorem assertsContent_kind_nested :
    Refines Site.kind Site.assertsContent ∧ ¬ Refines Site.assertsContent Site.kind :=
  ⟨res_mono (kind_refines_all Site.assertsContent),
   not_refines_of_pair (a := Site.preferenceOrder) (b := Site.stepOrder) rfl (by decide)⟩

theorem force_disposition_mismatch :
    ¬ Refines Site.force Site.disposition ∧ ¬ Refines Site.disposition Site.force :=
  ⟨not_refines_of_pair (a := Site.factContent) (b := Site.strengthMarker) rfl (by decide),
   not_refines_of_pair (a := Site.factContent) (b := Site.declarationContent) rfl (by decide)⟩

theorem surface_disposition_mismatch :
    ¬ Refines Site.isSurface Site.disposition ∧ ¬ Refines Site.disposition Site.isSurface :=
  ⟨not_refines_of_pair (a := Site.factContent) (b := Site.directiveContent) rfl (by decide),
   not_refines_of_pair (a := Site.factContent) (b := Site.stepOrder) rfl (by decide)⟩

theorem stack_disposition_mismatch :
    ¬ Refines Site.stackHeight Site.disposition ∧ ¬ Refines Site.disposition Site.stackHeight :=
  ⟨not_refines_of_pair (a := Site.directiveContent) (b := Site.declarationContent) rfl (by decide),
   not_refines_of_pair (a := Site.factContent) (b := Site.appliedRule) rfl (by decide)⟩

theorem mention_disposition_mismatch :
    ¬ Refines mentionClass Site.disposition ∧ ¬ Refines Site.disposition mentionClass :=
  ⟨not_refines_of_pair (a := Site.directiveContent) (b := Site.declarationContent) rfl (by decide),
   not_refines_of_pair (a := Site.factContent) (b := Site.declarationContent) rfl (by decide)⟩

theorem depthCount_disposition_mismatch :
    ¬ Refines Site.depthCount Site.disposition ∧ ¬ Refines Site.disposition Site.depthCount :=
  ⟨not_refines_of_pair (a := Site.factContent) (b := Site.strengthMarker) rfl (by decide),
   not_refines_of_pair (a := Site.factContent) (b := Site.declarationContent) rfl (by decide)⟩

/-- **THE SECOND NON-DEGENERATE NESTING.** Disposition is strictly finer than
    content assertion, and the reason is `WrongKind.lean`'s own consistency check
    `marker_matches_disposition`: the only content-free label is the only one the
    harness declines to disposition, so the disposition table already knows
    everything content assertion knows. -/
theorem disposition_assertsContent_nested :
    Refines Site.disposition Site.assertsContent ∧
    ¬ Refines Site.assertsContent Site.disposition :=
  ⟨res_mono (by intro a b h; cases a <;> cases b <;> first | rfl | exact absurd h (by decide)),
   not_refines_of_pair (a := Site.factContent) (b := Site.directiveContent) rfl (by decide)⟩

theorem disposition_kind_nested :
    Refines Site.kind Site.disposition ∧ ¬ Refines Site.disposition Site.kind :=
  ⟨res_mono (kind_refines_all Site.disposition),
   not_refines_of_pair (a := Site.factContent) (b := Site.declarationContent) rfl (by decide)⟩

/-- **THE ANSWER, IN ONE STATEMENT.** Of the twenty-eight pairs among the eight
    distinct residuals, NINETEEN are MISMATCHES — neither residual contains the
    other — and the nine that are not are the seven kind pairs (where one side is
    the trivial group) and two genuine nestings: force inside the depth count, and
    disposition inside content assertion. Structure is not layered here: the site
    model's pieces cut the eleven in genuinely different directions.

    Only the mismatched pairs are collected; the comparable ones are stated above
    with their own witnesses, and are not mismatches. The first nine are among the
    geometric structures, the last ten are the kind-derived pair against them. -/
theorem the_nineteen_mismatches :
    (¬ Refines Site.force Site.isSurface ∧ ¬ Refines Site.isSurface Site.force) ∧
    (¬ Refines Site.force Site.stackHeight ∧ ¬ Refines Site.stackHeight Site.force) ∧
    (¬ Refines Site.force mentionClass ∧ ¬ Refines mentionClass Site.force) ∧
    (¬ Refines Site.isSurface Site.stackHeight ∧ ¬ Refines Site.stackHeight Site.isSurface) ∧
    (¬ Refines Site.isSurface mentionClass ∧ ¬ Refines mentionClass Site.isSurface) ∧
    (¬ Refines Site.isSurface Site.depthCount ∧ ¬ Refines Site.depthCount Site.isSurface) ∧
    (¬ Refines Site.stackHeight mentionClass ∧ ¬ Refines mentionClass Site.stackHeight) ∧
    (¬ Refines Site.stackHeight Site.depthCount ∧ ¬ Refines Site.depthCount Site.stackHeight) ∧
    (¬ Refines mentionClass Site.depthCount ∧ ¬ Refines Site.depthCount mentionClass) ∧
    (¬ Refines Site.force Site.assertsContent ∧ ¬ Refines Site.assertsContent Site.force) ∧
    (¬ Refines Site.isSurface Site.assertsContent ∧
      ¬ Refines Site.assertsContent Site.isSurface) ∧
    (¬ Refines Site.stackHeight Site.assertsContent ∧
      ¬ Refines Site.assertsContent Site.stackHeight) ∧
    (¬ Refines mentionClass Site.assertsContent ∧ ¬ Refines Site.assertsContent mentionClass) ∧
    (¬ Refines Site.depthCount Site.assertsContent ∧
      ¬ Refines Site.assertsContent Site.depthCount) ∧
    (¬ Refines Site.force Site.disposition ∧ ¬ Refines Site.disposition Site.force) ∧
    (¬ Refines Site.isSurface Site.disposition ∧ ¬ Refines Site.disposition Site.isSurface) ∧
    (¬ Refines Site.stackHeight Site.disposition ∧ ¬ Refines Site.disposition Site.stackHeight) ∧
    (¬ Refines mentionClass Site.disposition ∧ ¬ Refines Site.disposition mentionClass) ∧
    (¬ Refines Site.depthCount Site.disposition ∧ ¬ Refines Site.disposition Site.depthCount) :=
  ⟨force_surface_mismatch, force_stack_mismatch, force_mention_mismatch,
   surface_stack_mismatch, surface_mention_mismatch, surface_depthCount_mismatch,
   stack_mention_mismatch, stack_depthCount_mismatch, mention_depthCount_mismatch,
   force_assertsContent_mismatch, surface_assertsContent_mismatch,
   stack_assertsContent_mismatch, mention_assertsContent_mismatch,
   depthCount_assertsContent_mismatch,
   force_disposition_mismatch, surface_disposition_mismatch, stack_disposition_mismatch,
   mention_disposition_mismatch, depthCount_disposition_mismatch⟩

/-- **THE MISMATCH OBJECT, AS A TABLE**, in `Symmetry.lean`'s representation so it
    can be compared with that file's twenty-four directly: the two headline
    transpositions written out as their value tables on `Site.all`. -/
theorem mixing_element_tables :
    Site.all.map (swapSite Site.factContent Site.strengthMarker) =
      [.strengthMarker, .factContent, .directiveContent, .declarationContent,
       .preferenceOrder, .stepOrder, .appliedRule, .foundingAssumption,
       .encoding, .register, .instanceToken] ∧
    Site.all.map (swapSite Site.factContent Site.directiveContent) =
      [.directiveContent, .strengthMarker, .factContent, .declarationContent,
       .preferenceOrder, .stepOrder, .appliedRule, .foundingAssumption,
       .encoding, .register, .instanceToken] := ⟨rfl, rfl⟩

/-- And neither is an automorphism of the model — as it must be, since each
    breaks one of the two structures `StructurePreserving` imposes together. The
    mismatch object lives OUTSIDE `Symmetry.lean`'s group, which is the whole
    point: it is what the two structures disagree about, not what they agree
    on. -/
theorem mixing_elements_not_automorphisms :
    autNoStack.contains (Site.all.map (swapSite Site.factContent Site.strengthMarker)) = false ∧
    autNoStack.contains (Site.all.map (swapSite Site.factContent Site.directiveContent)) = false :=
  ⟨rfl, rfl⟩

/-! ### §5 The intersections, and the calibration

Imposing structures together intersects their residuals. Two intersections are
computed: all eight, and all but kind. The second is the interesting one, and it
is also where the arithmetic of §1 gets checked against a count that
`Symmetry.lean` proves by complete enumeration. -/

/-- The seven non-kind structures read off one site at once. A record rather
    than a tuple only because instance search does not reach a seven-fold
    product; nothing turns on the encoding. -/
structure SevenKey where
  force : Option Force
  surface : Bool
  block : Block
  fit : Fit
  height : Option Nat
  mention : Nat
  depth : Nat
  deriving DecidableEq, Repr

/-- And all eight. -/
structure EightKey where
  seven : SevenKey
  kind : ChoiceKind
  deriving DecidableEq, Repr

/-- All seven structures except kind, as one key. -/
def allButKindKey (s : Site) : SevenKey :=
  ⟨s.force, s.isSurface, s.block, s.fit, s.stackHeight, mentionClass s, s.depthCount⟩

/-- All eight. -/
def allKey (s : Site) : EightKey := ⟨allButKindKey s, s.kind⟩

/-- **THE INTERSECTION OF ALL SEVEN NON-KIND STRUCTURES.** Nine classes: seven
    sites pinned, and two surviving swaps — Priorities with Process, Structure
    with Circumstances. -/
def resAllButKind : List (List Site) :=
  [[.factContent], [.strengthMarker], [.directiveContent], [.declarationContent],
   [.preferenceOrder, .stepOrder], [.appliedRule], [.foundingAssumption],
   [.encoding, .instanceToken], [.register]]

theorem resAllButKind_is_the_partition : isOrbitPartition allButKindKey resAllButKind = true := rfl

theorem resAllButKind_order : residualOrder resAllButKind = 4 := rfl

/-- **AND IT IS EXACTLY `Symmetry.lean`'s KLEIN FOUR.** The seven structures'
    joint orbit function is `allowedStack` on the nose — so the intersection of
    everything except kind is the group that file computes with the grounding
    order imposed, and imposing mention and the depth count on top of force,
    surface and the ladder adds no constraint at all. -/
theorem resAllButKind_orbits_eq_allowedStack (s : Site) :
    resOrbit allButKindKey s = allowedStack s := by
  cases s <;> rfl

/-- The two structures the intersection does not use: mention and the depth count
    are implied by force, surface and the grounding order together. -/
theorem stackTriple_determines_mention (a b : Site)
    (h : (a.force, a.isSurface, a.stackHeight) = (b.force, b.isSurface, b.stackHeight)) :
    mentionClass a = mentionClass b := by
  cases a <;> cases b <;> first | rfl | exact absurd h (by decide)

theorem stackTriple_determines_depthCount (a b : Site)
    (h : (a.force, a.isSurface, a.stackHeight) = (b.force, b.isSurface, b.stackHeight)) :
    a.depthCount = b.depthCount := by
  cases a <;> cases b <;> first | rfl | exact absurd h (by decide)

/-- **THE CALIBRATION.** The joint residual of the seven is `Symmetry.lean`'s
    `StackPreserving`, so its order is that file's `aut_with_stack_card` — FOUR,
    proved there by exhibiting every element and proving no other survives
    (`aut_with_stack_complete`). The arithmetic of §1 returns 4 on the same
    partition (`resAllButKind_order`). That is one of the two places the recipe
    can be checked against a mechanized count. -/
theorem residual_allButKind_iff_stackPreserving (f : Site → Site) :
    Residual allButKindKey f ↔ StackPreserving f := by
  constructor
  · intro h
    exact ⟨⟨h.injective, fun s => congrArg SevenKey.force (h.key_eq s),
            fun s => congrArg SevenKey.surface (h.key_eq s)⟩,
           fun s => congrArg SevenKey.height (h.key_eq s)⟩
  · intro h
    refine ⟨h.toStructurePreserving.injective, fun s => ?_⟩
    have hf := h.toStructurePreserving.force_eq s
    have hs := h.toStructurePreserving.surface_eq s
    have hh := h.height_eq s
    have hb : (f s).block = s.block := force_determines_block _ _ hf
    have hfit : (f s).fit = s.fit := block_determines_fit _ _ hb
    have htriple : ((f s).force, (f s).isSurface, (f s).stackHeight)
        = (s.force, s.isSurface, s.stackHeight) := by rw [hf, hs, hh]
    have hm : mentionClass (f s) = mentionClass s := stackTriple_determines_mention _ _ htriple
    have hd : (f s).depthCount = s.depthCount := stackTriple_determines_depthCount _ _ htriple
    unfold allButKindKey
    rw [hf, hs, hb, hfit, hh, hm, hd]

/-- The Klein four, quoted from `Symmetry.lean` rather than recomputed: every
    permutation surviving all seven non-kind structures is one of its four
    tables. -/
theorem resAllButKind_is_klein {f : Site → Site} (h : Residual allButKindKey f) :
    autWithStack.contains (Site.all.map f) = true :=
  aut_with_stack_complete ((residual_allButKind_iff_stackPreserving f).mp h)

theorem resAllButKind_klein_card : autWithStack.length = 4 := aut_with_stack_card

/-- **THE SECOND CALIBRATION POINT.** Force and surface together — the two
    structures `StructurePreserving` imposes — cut the eleven into seven classes,
    and the arithmetic returns 24, which is `Symmetry.lean`'s
    `aut_without_stack_card`, likewise proved there by complete enumeration. -/
def resForceSurface : List (List Site) :=
  [[.factContent], [.strengthMarker, .appliedRule, .foundingAssumption],
   [.directiveContent], [.declarationContent], [.preferenceOrder, .stepOrder],
   [.encoding, .instanceToken], [.register]]

def forceSurfaceKey (s : Site) : Option Force × Bool := (s.force, s.isSurface)

theorem resForceSurface_is_the_partition :
    isOrbitPartition forceSurfaceKey resForceSurface = true := rfl

theorem resForceSurface_order : residualOrder resForceSurface = 24 := rfl

theorem resForceSurface_orbits_eq_allowed (s : Site) :
    resOrbit forceSurfaceKey s = allowed s := by
  cases s <;> rfl

/-- Force and surface together ARE `StructurePreserving`, so the 24 above is the
    enumerated 24. -/
theorem residual_forceSurface_iff_structurePreserving (f : Site → Site) :
    Residual forceSurfaceKey f ↔ StructurePreserving f := by
  constructor
  · exact fun h => ⟨h.injective, fun s => congrArg (·.1) (h.key_eq s),
                    fun s => congrArg (·.2) (h.key_eq s)⟩
  · intro h
    refine ⟨h.injective, fun s => ?_⟩
    unfold forceSurfaceKey
    rw [h.force_eq s, h.surface_eq s]

theorem resForceSurface_card : autNoStack.length = 24 := aut_without_stack_card

/-- **THE INTERSECTION OF ALL EIGHT IS THE IDENTITY ALONE**, and it is SMALLER
    than the Klein four rather than equal to it. The reason is entirely the kind
    label: it is injective on sites, so it pins everything by itself
    (`resKind_is_trivial`), and adding it to any collection of structures collapses
    the joint residual to nothing.

    Read as a fact about the model: the kind label carries strictly more
    separating power than all seven of the model's structural distinctions put
    together, because those seven cannot tell Priorities from Process nor
    Structure from Circumstances, and the label can. -/
theorem resAll_is_trivial {f : Site → Site} (h : Residual allKey f) : ∀ s, f s = s :=
  fun s => generator_injective _ _ (congrArg EightKey.kind (h.key_eq s))

def resAll : List (List Site) := resKind

theorem resAll_is_the_partition : isOrbitPartition allKey resAll = true := rfl

theorem resAll_order : residualOrder resAll = 1 := rfl

/-- The comparison the question asked for, stated plainly: the intersection of
    all eight is smaller than the Klein four, and the intersection of the seven
    that are not the kind label is exactly it. -/
theorem resAll_vs_klein :
    residualOrder resAll = 1 ∧ residualOrder resAllButKind = 4 ∧ autWithStack.length = 4 :=
  ⟨rfl, rfl, aut_with_stack_card⟩

/-! #### What the two kind-derived structures do to the Klein four

The sharpest way to see that they are not more of the same: impose each on top of
all seven geometric structures and watch what is left. Content assertion HALVES
the Klein four; disposition kills it outright. -/

/-- The seven geometric structures plus content assertion. -/
structure SevenPlusAssertsKey where
  seven : SevenKey
  asserts : Bool
  deriving DecidableEq, Repr

def sevenPlusAssertsKey (s : Site) : SevenPlusAssertsKey := ⟨allButKindKey s, s.assertsContent⟩

/-- Ten classes: only Priorities/Process survives. -/
def resSevenPlusAsserts : List (List Site) :=
  [[.factContent], [.strengthMarker], [.directiveContent], [.declarationContent],
   [.preferenceOrder, .stepOrder], [.appliedRule], [.foundingAssumption],
   [.encoding], [.register], [.instanceToken]]

theorem resSevenPlusAsserts_is_the_partition :
    isOrbitPartition sevenPlusAssertsKey resSevenPlusAsserts = true := rfl

theorem resSevenPlusAsserts_order : residualOrder resSevenPlusAsserts = 2 := rfl

/-- **CONTENT ASSERTION HALVES THE KLEIN FOUR.** Adding it to the seven geometric
    structures leaves exactly two permutations — the identity and the
    Priorities ↔ Process swap. The other generator, Structure ↔ Circumstances, is
    precisely what it kills (`structure_semantics_split`). Enumerated at the level
    of permutations, not counted: both survivors are exhibited. -/
theorem sevenPlusAsserts_is_Z2 {f : Site → Site} (h : Residual sevenPlusAssertsKey f) :
    (∀ s, f s = s) ∨ (∀ s, f s = swapPreferenceStep s) := by
  have h1 : f Site.factContent = Site.factContent := residual_fixes_of_singleton h rfl
  have h2 : f Site.strengthMarker = Site.strengthMarker := residual_fixes_of_singleton h rfl
  have h3 : f Site.directiveContent = Site.directiveContent := residual_fixes_of_singleton h rfl
  have h4 : f Site.declarationContent = Site.declarationContent :=
    residual_fixes_of_singleton h rfl
  have h5 : f Site.appliedRule = Site.appliedRule := residual_fixes_of_singleton h rfl
  have h6 : f Site.foundingAssumption = Site.foundingAssumption :=
    residual_fixes_of_singleton h rfl
  have h7 : f Site.encoding = Site.encoding := residual_fixes_of_singleton h rfl
  have h8 : f Site.register = Site.register := residual_fixes_of_singleton h rfl
  have h9 : f Site.instanceToken = Site.instanceToken := residual_fixes_of_singleton h rfl
  have hpo : f Site.preferenceOrder ∈ [Site.preferenceOrder, Site.stepOrder] :=
    residual_mem_orbit h Site.preferenceOrder
  have hso : f Site.stepOrder ∈ [Site.preferenceOrder, Site.stepOrder] :=
    residual_mem_orbit h Site.stepOrder
  rcases mem_pair hpo with e1 | e1 <;> rcases mem_pair hso with e2 | e2
  · exact absurd (h.injective _ _ (e1.trans e2.symm)) (by decide)
  · exact Or.inl (by
      intro s
      cases s <;>
        first | exact h1 | exact h2 | exact h3 | exact h4 | exact h5 | exact h6
              | exact h7 | exact h8 | exact h9 | exact e1 | exact e2)
  · exact Or.inr (by
      intro s
      cases s <;>
        first | exact h1 | exact h2 | exact h3 | exact h4 | exact h5 | exact h6
              | exact h7 | exact h8 | exact h9 | exact e1 | exact e2)
  · exact absurd (h.injective _ _ (e1.trans e2.symm)) (by decide)

/-- The seven geometric structures plus disposition. -/
structure SevenPlusDispKey where
  seven : SevenKey
  policy : Disposition
  deriving DecidableEq, Repr

def sevenPlusDispKey (s : Site) : SevenPlusDispKey := ⟨allButKindKey s, s.disposition⟩

theorem resSevenPlusDisposition_is_the_partition :
    isOrbitPartition sevenPlusDispKey resKind = true := rfl

/-- **DISPOSITION COLLAPSES THE KLEIN FOUR TO NOTHING.** It separates Priorities
    from Process (vary against hold) AND Structure from Circumstances (cannotVary
    against outOfScope), so it kills both generators. Adding it to the seven does
    what adding the kind label does, and the disposition table is much coarser than
    the kind label — six classes against eleven. -/
theorem sevenPlusDisposition_is_trivial {f : Site → Site} (h : Residual sevenPlusDispKey f) :
    ∀ s, f s = s := by
  intro s
  cases s <;> exact residual_fixes_of_singleton h rfl

/-- The three answers side by side, which is the whole point of the section:
    the seven geometric structures leave the Klein four; content assertion halves
    it; disposition and the kind label each leave nothing. -/
theorem klein_under_the_kind_structures :
    residualOrder resAllButKind = 4 ∧
    residualOrder resSevenPlusAsserts = 2 ∧
    residualOrder resKind = 1 :=
  ⟨rfl, rfl, rfl⟩

/-! ### §6 A third sector: the block-absorption channel

The ten structures above are all LABELS, and a label's residual is always a Young
subgroup — the full product of the symmetric groups on its classes. This section
adds a structure that is not a label, and the payoff is that its residual is not
of that shape at all.

ABSORPTION is the map sending each site to its own block's gross face. It is the
channel `Surface.lean`'s block model predicts a confusion should follow, and it is
the one the measured confusion mostly does follow. Asking which permutations
COMMUTE with it — the same question §3 asked of the mention projection — gives an
answer §3's did not: a genuine interchange of two whole blocks. -/

/-- **THE ABSORPTION MAP.** Every site goes to its own block's gross face. -/
def absorb (s : Site) : Site := Block.surface s.block

theorem absorb_table :
    Site.all.map absorb =
      [.factContent, .factContent, .directiveContent, .declarationContent,
       .directiveContent, .directiveContent, .factContent, .factContent,
       .register, .register, .register] := rfl

theorem absorb_idem (s : Site) : absorb (absorb s) = absorb s := by cases s <;> rfl

theorem absorb_surface (b : Block) : absorb (Block.surface b) = Block.surface b := by
  cases b <;> rfl

/-- Its fixed points are exactly the four surfaces — so absorption is to the block
    structure what `Symmetry.lean`'s mention is to the force structure: a
    projection onto the gross faces. -/
theorem absorb_fixed_iff (s : Site) : (absorb s == s) = s.isSurface := by cases s <;> rfl

/-- **THE CONSTRAINT ABSORPTION IMPOSES.** -/
structure Absorbing (f : Site → Site) : Prop where
  /-- distinct sites go to distinct sites -/
  injective : ∀ s t : Site, f s = f t → s = t
  /-- and absorbing then moving is moving then absorbing -/
  commutes : ∀ s, f (absorb s) = absorb (f s)

/-- The block permutation an absorbing map induces, read off what it does to the
    four surfaces. -/
def blockMap (f : Site → Site) (b : Block) : Block := (f (Block.surface b)).block

theorem absorbing_block_surface {f : Site → Site} (h : Absorbing f) (b : Block) :
    Block.surface (blockMap f b) = f (Block.surface b) := by
  have hc := h.commutes (Block.surface b)
  rw [absorb_surface] at hc
  exact hc.symm

/-- **THE BLOCK MAP IS WELL DEFINED ON EVERY SITE**, not just the surfaces: an
    absorbing map moves whole blocks. -/
theorem absorbing_block {f : Site → Site} (h : Absorbing f) (s : Site) :
    (f s).block = blockMap f s.block := by
  apply surface_injective
  rw [absorbing_block_surface h]
  exact (h.commutes s).symm

theorem absorbing_blockMap_injective {f : Site → Site} (h : Absorbing f) (b₁ b₂ : Block)
    (hb : blockMap f b₁ = blockMap f b₂) : b₁ = b₂ := by
  apply surface_injective
  apply h.injective
  rw [← absorbing_block_surface h, ← absorbing_block_surface h, hb]

theorem block_declaration_narrow {x : Site} (h : x.block = Block.declaration) :
    x = Site.declarationContent := by
  cases x <;> first | rfl | exact absurd h (by decide)

theorem block_carrier_narrow {x : Site} (h : x.block = Block.carrier) :
    x = .encoding ∨ x = .register ∨ x = .instanceToken := by
  cases x <;>
    first
      | exact Or.inl rfl
      | exact Or.inr (Or.inl rfl)
      | exact Or.inr (Or.inr rfl)
      | exact absurd h (by decide)

theorem block_cases (b : Block) :
    b = .assertive ∨ b = .directive ∨ b = .declaration ∨ b = .carrier := by
  cases b
  · exact Or.inl rfl
  · exact Or.inr (Or.inl rfl)
  · exact Or.inr (Or.inr (Or.inl rfl))
  · exact Or.inr (Or.inr (Or.inr rfl))

/-- **THE ASSERTIVE BLOCK CANNOT MOVE**, and the reason is `Symmetry.lean`'s: four
    sites do not fit into three, or into one. This is `no_fit_conjugation`'s
    counting argument doing duty again, in a place that file did not reach. -/
theorem absorbing_assertive_fixed {f : Site → Site} (h : Absorbing f) :
    blockMap f Block.assertive = Block.assertive := by
  have e1 : (f Site.factContent).block = blockMap f Block.assertive := absorbing_block h _
  have e2 : (f Site.strengthMarker).block = blockMap f Block.assertive := absorbing_block h _
  have e3 : (f Site.appliedRule).block = blockMap f Block.assertive := absorbing_block h _
  have e4 : (f Site.foundingAssumption).block = blockMap f Block.assertive := absorbing_block h _
  rcases block_cases (blockMap f Block.assertive) with hb | hb | hb | hb
  · exact hb
  · rw [hb] at e1 e2 e3 e4
    rcases block_directive_narrow e1 with a1|a1|a1 <;>
    rcases block_directive_narrow e2 with a2|a2|a2 <;>
    rcases block_directive_narrow e3 with a3|a3|a3 <;>
    rcases block_directive_narrow e4 with a4|a4|a4 <;>
    first
      | exact absurd (h.injective _ _ (a1.trans a2.symm)) (by decide)
      | exact absurd (h.injective _ _ (a1.trans a3.symm)) (by decide)
      | exact absurd (h.injective _ _ (a1.trans a4.symm)) (by decide)
      | exact absurd (h.injective _ _ (a2.trans a3.symm)) (by decide)
      | exact absurd (h.injective _ _ (a2.trans a4.symm)) (by decide)
      | exact absurd (h.injective _ _ (a3.trans a4.symm)) (by decide)
  · rw [hb] at e1 e2
    exact absurd (h.injective _ _
      ((block_declaration_narrow e1).trans (block_declaration_narrow e2).symm)) (by decide)
  · rw [hb] at e1 e2 e3 e4
    rcases block_carrier_narrow e1 with a1|a1|a1 <;>
    rcases block_carrier_narrow e2 with a2|a2|a2 <;>
    rcases block_carrier_narrow e3 with a3|a3|a3 <;>
    rcases block_carrier_narrow e4 with a4|a4|a4 <;>
    first
      | exact absurd (h.injective _ _ (a1.trans a2.symm)) (by decide)
      | exact absurd (h.injective _ _ (a1.trans a3.symm)) (by decide)
      | exact absurd (h.injective _ _ (a1.trans a4.symm)) (by decide)
      | exact absurd (h.injective _ _ (a2.trans a3.symm)) (by decide)
      | exact absurd (h.injective _ _ (a2.trans a4.symm)) (by decide)
      | exact absurd (h.injective _ _ (a3.trans a4.symm)) (by decide)

theorem absorbing_directive_ne_declaration {f : Site → Site} (h : Absorbing f) :
    blockMap f Block.directive ≠ Block.declaration := by
  intro e
  have e1 : (f Site.directiveContent).block = Block.declaration :=
    (absorbing_block h Site.directiveContent).trans e
  have e2 : (f Site.preferenceOrder).block = Block.declaration :=
    (absorbing_block h Site.preferenceOrder).trans e
  exact absurd (h.injective _ _
    ((block_declaration_narrow e1).trans (block_declaration_narrow e2).symm)) (by decide)

theorem absorbing_carrier_ne_declaration {f : Site → Site} (h : Absorbing f) :
    blockMap f Block.carrier ≠ Block.declaration := by
  intro e
  have e1 : (f Site.encoding).block = Block.declaration :=
    (absorbing_block h Site.encoding).trans e
  have e2 : (f Site.register).block = Block.declaration :=
    (absorbing_block h Site.register).trans e
  exact absurd (h.injective _ _
    ((block_declaration_narrow e1).trans (block_declaration_narrow e2).symm)) (by decide)

/-- **THE BLOCK MAP HAS EXACTLY TWO POSSIBILITIES.** Either it is the identity, or
    it interchanges the DIRECTIVE and CARRIER blocks. Nothing else survives: the
    assertive block is pinned by cardinality (4 into 3 or 1 fails), the declaration
    block is pinned because nothing else has room to land in a block of one, and
    the remaining two blocks are the same size — three sites each, one surface and
    two depths — so they can trade.

    `Symmetry.lean`'s `no_fit_conjugation` rules out the assertive/directive
    conjugation by counting 4 against 3. That argument says nothing about 3
    against 3, and this is what lives in the gap it leaves. -/
theorem absorbing_blockMap_cases {f : Site → Site} (h : Absorbing f) :
    (blockMap f Block.directive = Block.directive ∧
     blockMap f Block.carrier = Block.carrier ∧
     blockMap f Block.declaration = Block.declaration) ∨
    (blockMap f Block.directive = Block.carrier ∧
     blockMap f Block.carrier = Block.directive ∧
     blockMap f Block.declaration = Block.declaration) := by
  have ha := absorbing_assertive_fixed h
  have hnd := absorbing_directive_ne_declaration h
  have hnc := absorbing_carrier_ne_declaration h
  have hinj := absorbing_blockMap_injective h
  rcases block_cases (blockMap f Block.directive) with hd|hd|hd|hd <;>
  rcases block_cases (blockMap f Block.carrier) with hc|hc|hc|hc <;>
  rcases block_cases (blockMap f Block.declaration) with he|he|he|he <;>
  first
    | exact Or.inl ⟨hd, hc, he⟩
    | exact Or.inr ⟨hd, hc, he⟩
    | exact absurd hd hnd
    | exact absurd hc hnc
    | exact absurd (hinj _ _ (hd.trans ha.symm)) (by decide)
    | exact absurd (hinj _ _ (hc.trans ha.symm)) (by decide)
    | exact absurd (hinj _ _ (he.trans ha.symm)) (by decide)
    | exact absurd (hinj _ _ (hd.trans hc.symm)) (by decide)
    | exact absurd (hinj _ _ (hd.trans he.symm)) (by decide)
    | exact absurd (hinj _ _ (hc.trans he.symm)) (by decide)

/-- An absorbing map whose block permutation is trivial is exactly a
    `Symmetry.lean` automorphism. -/
theorem structurePreserving_of_blockMap_id {f : Site → Site} (h : Absorbing f)
    (hid : ∀ b, blockMap f b = b) : StructurePreserving f := by
  have hsurf : ∀ b, f (Block.surface b) = Block.surface b := by
    intro b
    have hb := absorbing_block_surface h b
    rw [hid] at hb
    exact hb.symm
  have hblk : ∀ s, (f s).block = s.block := by
    intro s
    rw [absorbing_block h, hid]
  refine ⟨h.injective, fun s => block_determines_force _ _ (hblk s), fun s => ?_⟩
  show decide (Block.surface (f s).block = f s) = decide (Block.surface s.block = s)
  rw [hblk s]
  by_cases hc : Block.surface s.block = s
  · have hfs : f s = s := by
      have hb := hsurf s.block
      rw [hc] at hb
      exact hb
    rw [hfs]
  · rw [decide_eq_false hc]
    exact decide_eq_false (fun hcon => hc (h.injective _ _ ((hsurf s.block).trans hcon)))

/-- And conversely every automorphism is absorbing, so `Symmetry.lean`'s
    twenty-four sit inside this residual. -/
theorem absorbing_of_structurePreserving {f : Site → Site} (h : StructurePreserving f) :
    Absorbing f :=
  ⟨h.injective, fun s => by
    show f (Block.surface s.block) = Block.surface (f s).block
    rw [surfaces_are_rigid h s.block, structurePreserving_preserves_block h s]⟩

theorem blockMap_of_structurePreserving {f : Site → Site} (h : StructurePreserving f) (b : Block) :
    blockMap f b = b := by
  show (f (Block.surface b)).block = b
  rw [surfaces_are_rigid h b, surface_block]

/-! #### The interchange, exhibited

The possibility the counting argument leaves open is realised, and here it is:
Rules ↔ Manner on the surfaces, Priorities ↔ Structure and Process ↔
Circumstances underneath. -/

/-- **THE BLOCK INTERCHANGE.** The directive apparatus and the carrier layer,
    swapped wholesale: each block's surface to the other's surface, each block's
    two depths to the other's two depths. -/
def dirCarrierSwap : Site → Site
  | .directiveContent => .register
  | .register         => .directiveContent
  | .preferenceOrder  => .encoding
  | .encoding         => .preferenceOrder
  | .stepOrder        => .instanceToken
  | .instanceToken    => .stepOrder
  | s                 => s

theorem dirCarrierSwap_plain :
    Site.all.map (fun s => ((s.kind.plain), (dirCarrierSwap s).kind.plain)) =
      [("Facts", "Facts"), ("Confidence", "Confidence"), ("Rules", "Manner"),
       ("Identity", "Identity"), ("Priorities", "Structure"), ("Process", "Circumstances"),
       ("Model", "Model"), ("Premises", "Premises"), ("Structure", "Priorities"),
       ("Manner", "Rules"), ("Circumstances", "Process")] := rfl

theorem dirCarrierSwap_involutive (s : Site) : dirCarrierSwap (dirCarrierSwap s) = s := by
  cases s <;> rfl

theorem dirCarrierSwap_absorbing : Absorbing dirCarrierSwap :=
  ⟨inj_of_involutive dirCarrierSwap_involutive, fun s => by cases s <;> rfl⟩

theorem blockMap_dirCarrierSwap :
    blockMap dirCarrierSwap Block.assertive = Block.assertive ∧
    blockMap dirCarrierSwap Block.directive = Block.carrier ∧
    blockMap dirCarrierSwap Block.declaration = Block.declaration ∧
    blockMap dirCarrierSwap Block.carrier = Block.directive := ⟨rfl, rfl, rfl, rfl⟩

theorem absorbing_comp {f g : Site → Site} (hf : Absorbing f) (hg : Absorbing g) :
    Absorbing (f ∘ g) :=
  ⟨fun s t hh => hg.injective s t (hf.injective _ _ hh),
   fun s => by
     show f (g (absorb s)) = absorb (f (g s))
     rw [hg.commutes s, hf.commutes (g s)]⟩

theorem blockMap_comp {f g : Site → Site} (hg : Absorbing g) (b : Block) :
    blockMap (f ∘ g) b = blockMap f (blockMap g b) := by
  show (f (g (Block.surface b))).block = (f (Block.surface (blockMap g b))).block
  rw [absorbing_block_surface hg b]

/-- **THE ABSORPTION RESIDUAL, CHARACTERIZED COMPLETELY.** A permutation commutes
    with absorption exactly when it is one of `Symmetry.lean`'s twenty-four
    automorphisms, or one of those twenty-four composed with the block
    interchange. Two cosets, and no third possibility. -/
theorem absorbing_iff {f : Site → Site} :
    Absorbing f ↔ (StructurePreserving f ∨ StructurePreserving (dirCarrierSwap ∘ f)) := by
  constructor
  · intro h
    rcases absorbing_blockMap_cases h with ⟨hd, hc, he⟩ | ⟨hd, hc, he⟩
    · refine Or.inl (structurePreserving_of_blockMap_id h ?_)
      intro b
      cases b
      · exact absorbing_assertive_fixed h
      · exact hd
      · exact he
      · exact hc
    · refine Or.inr (structurePreserving_of_blockMap_id
        (absorbing_comp dirCarrierSwap_absorbing h) ?_)
      intro b
      rw [blockMap_comp h b]
      cases b
      · rw [absorbing_assertive_fixed h]; rfl
      · rw [hd]; rfl
      · rw [he]; rfl
      · rw [hc]; rfl
  · rintro (hs | hs)
    · exact absorbing_of_structurePreserving hs
    · have hk : Absorbing (dirCarrierSwap ∘ (dirCarrierSwap ∘ f)) :=
        absorbing_comp dirCarrierSwap_absorbing (absorbing_of_structurePreserving hs)
      have heq : dirCarrierSwap ∘ (dirCarrierSwap ∘ f) = f := by
        funext s
        exact dirCarrierSwap_involutive (f s)
      rw [heq] at hk
      exact hk

/-- The two cosets are disjoint — so the residual is 24 + 24 and not 24 counted
    twice. The block map is what separates them, and it cannot be both. -/
theorem absorbing_halves_disjoint {f : Site → Site} (h : StructurePreserving f) :
    ¬ StructurePreserving (dirCarrierSwap ∘ f) := by
  intro hk
  have h1 := blockMap_of_structurePreserving hk Block.directive
  rw [blockMap_comp (absorbing_of_structurePreserving h) Block.directive,
    blockMap_of_structurePreserving h Block.directive] at h1
  exact absurd h1 (by decide)

/-- Duplicate-freeness for a list of tables, as a `Bool`, so the count below stays
    a kernel computation and costs no axioms. -/
def nodupTables : List (List Site) → Bool
  | []        => true
  | t :: rest => !rest.contains t && nodupTables rest

/-- **THE FORTY-EIGHT, ENUMERATED.** `Symmetry.lean`'s twenty-four tables, and the
    same twenty-four pushed through the block interchange. -/
def absorbingTables : List (List Site) :=
  autNoStack ++ autNoStack.map (fun t => t.map dirCarrierSwap)

theorem absorbing_card : absorbingTables.length = 48 := rfl

/-- And they are forty-eight DISTINCT permutations, so the count is a count. -/
theorem absorbing_tables_nodup : nodupTables absorbingTables = true := rfl

theorem absorbing_tables_are_permutations :
    (absorbingTables.all (fun t => t.length == 11) &&
     absorbingTables.all nodupSites &&
     absorbingTables.all (fun t => Site.all.all (fun s => t.contains s))) = true := rfl

/-! #### Why this sector is not like the other ten

The point of the section, and it is a structural point rather than a numerical
one: absorption's residual is not the residual of ANY labelling of the sites. -/

/-- The block interchange sends Priorities to Structure. If absorption were a
    label, the bare transposition of those two would therefore have to be
    absorbing as well — and it is not, because it moves Priorities out of the
    directive block while leaving the directive surface where it was. -/
theorem swapSite_priorities_structure_not_absorbing :
    ¬ Absorbing (swapSite Site.preferenceOrder Site.encoding) :=
  fun h => absurd (h.commutes Site.preferenceOrder) (by decide)

/-- **ABSORPTION IS NOT A LABEL RESIDUAL — no labelling of the eleven sites, of
    any type whatever, has it as its residual.** Every one of the ten structures
    in §1 is a label, so every one of their residuals is a full product of
    symmetric groups on its classes. This one is not, and the obstruction is
    exhibited rather than counted: it contains a permutation carrying Priorities to
    Structure but does not contain the transposition of those two.

    That is what makes it a THIRD KIND of sector rather than an eleventh
    structure. -/
theorem absorbing_is_not_any_label_residual :
    ¬ ∃ (β : Type) (key : Site → β), ∀ f, Absorbing f ↔ Residual key f := by
  rintro ⟨β, key, hiff⟩
  have h1 : Residual key dirCarrierSwap := (hiff _).mp dirCarrierSwap_absorbing
  have h2 : Residual key (swapSite Site.preferenceOrder Site.encoding) :=
    residual_swapSite (h1.key_eq Site.preferenceOrder).symm
  exact swapSite_priorities_structure_not_absorbing ((hiff _).mpr h2)

/-- Where the interchange stands against the ten. It survives the surface split,
    the grounding order and the depth count — every structure that cannot tell a
    directive site from the carrier site of matching rank — and breaks force,
    mention, and all three kind-derived labels. -/
theorem dirCarrierSwap_against_the_ten :
    (Residual Site.isSurface dirCarrierSwap ∧
     Residual Site.stackHeight dirCarrierSwap ∧
     Residual Site.depthCount dirCarrierSwap) ∧
    (¬ Residual Site.force dirCarrierSwap ∧
     ¬ Residual mentionClass dirCarrierSwap ∧
     ¬ Residual Site.assertsContent dirCarrierSwap ∧
     ¬ Residual Site.disposition dirCarrierSwap ∧
     ¬ Residual Site.kind dirCarrierSwap) := by
  refine ⟨⟨⟨inj_of_involutive dirCarrierSwap_involutive, fun s => by cases s <;> rfl⟩,
           ⟨inj_of_involutive dirCarrierSwap_involutive, fun s => by cases s <;> rfl⟩,
           ⟨inj_of_involutive dirCarrierSwap_involutive, fun s => by cases s <;> rfl⟩⟩,
          fun h => absurd (h.key_eq Site.directiveContent) (by decide),
          fun h => absurd (h.key_eq Site.directiveContent) (by decide),
          fun h => absurd (h.key_eq Site.instanceToken) (by decide),
          fun h => absurd (h.key_eq Site.directiveContent) (by decide),
          fun h => absurd (h.key_eq Site.directiveContent) (by decide)⟩

/-- And it is not an automorphism of the model, so this really is new ground
    rather than something `Symmetry.lean` already had. -/
theorem dirCarrierSwap_not_automorphism :
    autNoStack.contains (Site.all.map dirCarrierSwap) = false := rfl

/-! ### §7 What this file found, and what it does NOT prove

**THERE IS A MISMATCH, and it is not one mismatch but nineteen.** Of the
twenty-eight pairs among the eight distinct residuals, nineteen are incomparable:
neither subgroup contains the other, and both directions are witnessed by explicit
transpositions (`the_nineteen_mismatches`). Only nine pairs are comparable, and
seven of those are the degenerate ones where the kind label's trivial residual sits
inside everything. The two non-degenerate nestings are force inside the depth count
(which exists only because the 3/2/0/2 of `depth_counts` has a repeat in it) and
disposition inside content assertion (which exists because `WrongKind.lean`'s
`marker_matches_disposition` says the two tables agree on the one site that
matters).

**THE HEADLINE PAIR AMONG THE GEOMETRIC STRUCTURES IS FORCE AGAINST SURFACE.**
Facts ↔ Confidence is a force symmetry the surface split breaks; Facts ↔ Rules is a
surface symmetry the force fibration breaks (`force_surface_mismatch`,
`mixing_element_tables`). Neither is an automorphism of the model
(`mixing_elements_not_automorphisms`) — which is the content: the two structures
pick out different bases among the eleven, and `Symmetry.lean`'s 24 is what
survives that disagreement rather than what causes it.

**THE SHARPEST SINGLE OBJECT IS STRUCTURE ↔ CIRCUMSTANCES.** One transposition is
in every one of the five geometric residuals and in none of the three kind-derived
ones (`structure_semantics_split`). It is a generator of `Symmetry.lean`'s Klein
four, so a swap the model's whole geometry calls free is broken by the
content-assertion label acting alone — which follows from
`contingent_is_the_only_marker` by way of `assertsContent_fixes_circumstances`: a
structure that marks exactly one site pins it. Imposing content assertion on top of
all seven geometric structures therefore HALVES the Klein four to
{identity, Priorities ↔ Process} (`sevenPlusAsserts_is_Z2`), and imposing the
disposition table instead collapses it to the identity
(`sevenPlusDisposition_is_trivial`), because that table separates both generators.

**IT IS NOT, HOWEVER, THE FIRST MISMATCH IN THE STRUCTURE.** It was proposed as
one, and the record should be straight: nine mismatches among the geometric
structures alone were already established before content assertion was computed,
and force against surface is both earlier and, in the sense of what it separates,
larger. What Structure ↔ Circumstances is, is the SHARPEST mismatch — a single
transposition that cleanly separates the geometric structures from the semantic
ones as two blocks — and that is a better thing to be than the first.

**AND THERE IS A THIRD KIND OF SECTOR, not merely a third structure.** The
block-absorption channel (§6) is not a labelling, and its residual is provably not
the residual of any labelling whatever
(`absorbing_is_not_any_label_residual`). Commuting with absorption is exactly being
one of `Symmetry.lean`'s twenty-four automorphisms, or one of them composed with a
wholesale interchange of the DIRECTIVE block and the CARRIER block
(`absorbing_iff`) — forty-eight permutations, enumerated and checked distinct
(`absorbing_card`, `absorbing_tables_nodup`). That interchange lives exactly in the
gap `Symmetry.lean`'s `no_fit_conjugation` leaves: that theorem kills the
assertive/directive conjugation by counting four sites against three, and says
nothing about three against three. Rules ↔ Manner, Priorities ↔ Structure,
Process ↔ Circumstances, all at once, and it is not an automorphism of the model
(`dirCarrierSwap_not_automorphism`).

**THE ORDERS ARE ARITHMETIC, THE PARTITIONS AND THE COMPARISONS ARE NOT.** Stated
in the header and repeated here because this is where a reader will quote a number.
`residuals_table`'s ten figures are products of factorials of the computed class
sizes. That this counts label-preserving bijections is standard Young-subgroup
combinatorics and is NOT mechanized in this file; it is calibrated at two points
where `Symmetry.lean` proves a count by complete enumeration (`resForceSurface_order`
returns 24 against `aut_without_stack_card`, `resAllButKind_order` returns 4 against
`aut_with_stack_card`). Everything in §4 — every containment and every mismatch — is
a theorem about permutations and quotes no order at all. §6's 48 is likewise not
arithmetic: the tables are exhibited and their distinctness is checked.

**WHAT A MISMATCH OBJECT IS, AND WHAT IT IS NOT.** It is a transposition — or, in
§6, a block interchange — that one structure admits as a symmetry and another does
not. That is all it is. It is NOT a mixing matrix, and nothing above moves it any
closer to being one: there is no vector space here, no pair of bases, no unitary,
and no invariant playing the role of a Jarlskog. Nineteen incomparable pairs is a
fact about a partition lattice on eleven elements, and §6's non-Young residual is a
fact about one imprimitive subgroup of S₁₁. Turning any of it into a mixing matrix
would need an object this file does not construct and does not gesture at.

**AND THE MEASURED CORROBORATION IS CORROBORATION, NOT EVIDENCE.** The panel
confusion asymmetry between the two twins (`scratchpad/TWO_WAY_READING.md`:
Structure → Manner 7 and Structure → Facts 0, against Circumstances → Manner 1 and
Circumstances → Facts 9) points the same way as `structure_semantics_split`, and is
cited in that theorem's docstring for that reason. It is a measurement about
annotators. It cannot confirm a theorem about an inductive type, the theorem cannot
confirm it, and neither appears in the other's basis. In particular nothing above
predicted those counts, and the theorem would be exactly as true if they had come
out flat.

**AND THE COMPARISON IS OF STRUCTURES, NOT OF SECTORS.** The flavour reading in
the header supplies the QUESTION and nothing else. Two residual subgroups of a
symmetric group on an eleven-element inductive type are misaligned; no theorem
above mentions quarks, mixing, or CP, and none may be quoted as evidence for any
analogy. The analogies are in `scratchpad/N18_BRIDGE_NOTE.md` to be attacked.

**AND THE MODEL-RELATIVITY IS INHERITED WHOLE.** As with everything downstream of
`Generator.lean`, these are `rfl`s about an eleven-element type. `Surface.lean`'s
one modelling choice (Manner rather than Structure as the carrier's surface)
propagates here exactly as it does there: under the rival reading `resSurface`'s
two classes trade `register` for `encoding`, the class sizes 4 and 7 are
unchanged, the order 120,960 is unchanged, and every mismatch above survives with
one witness relabelled. `Stack.lean`'s grounding order is likewise a commitment,
and if its kill fires `resStack` is wrong about the world however sound it remains
about the model. -/

end CIRISOntology.Core
