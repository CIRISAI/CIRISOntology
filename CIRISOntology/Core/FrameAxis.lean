/-
CIRISOntology.Core.FrameAxis — the lake's order structure, stated once.

WHY THIS EXISTS (the DRY pass, Eric 2026-08-23: "get the lake DRY, that will
tell us what we have"). Three files carry the same structure in three
vocabularies:

  * `Core/FrameOrder`   — corpora ordered by inclusion; `Repairable` monotone.
  * `Core/FrameEntropy` — views ordered by refinement; the fiber shrinks, so
                          `frameEntropy` falls (`frameEntropy_refine_le`).
  * `Core/GrainFloor`   — tiers ordered by their floors; `admissible` monotone
                          (`reroot_finer_admits_more`).

One structure, three objects: **frames form an order, and the lake's
truth-bearing quantities are monotone along it — never invariant under it.**
This file states the structure once and re-derives the three as instances, so a
fourth object arriving with the same shape (the mesh's shard frames are the
expected fourth) instantiates a definition instead of repeating a file.

WHAT IS GENUINELY NEW HERE, beyond restatement:

  * `fiber_antitone_of_coarser` STRENGTHENS `frameEntropy_refine_le`: the
    refinement in `FrameEntropy` is the special case `view = Prod.fst ∘ view'`;
    here ANY factoring `view = h ∘ view'` (any coarsening whatever) grows the
    fiber and hence the entropy. Refinement was one rung; this is the axis.
  * `UpperAlong.comap` is the composition law the MESH consumes: a monotone map
    between frame orders pulls truth-bearing quantities back. A shard adopting
    its parent's frame through a monotone chart inherits every monotone verdict
    without recomputation — this is the lemma under "seamless" before any code
    exists.
  * `not_invariant_of_two_values`, stated once, replaces the per-file anti-gauge
    arguments: any quantity that takes two values along the order is
    frame-RELATIVE, so none of these quantities is gauge. (The full gauge
    refutation with its Defeasible fence stays in `Core/FrameOrder`, which
    proved it first and proves more.)

SCOPE. Definitions and order lemmas; no physics. The instances inherit each
source file's scope and widen none of them. `Core/FrameOrder`'s honest caveat
carries over verbatim: monotonicity holds of the MODELS (membership, fibers,
thresholds) by construction; that the world's records and tiers wear these
models is the substantive assumption, tested where each source file says.
-/
import CIRISOntology.Core.FrameOrder
import CIRISOntology.Core.FrameEntropy
import CIRISOntology.Core.GrainFloor

namespace CIRISOntology.Core.FrameAxis

open Finset

/-! ### The structure, once -/

/-- A truth-bearing quantity along a frame order: once true, true in every
    finer/larger frame. (`Core/FrameOrder`'s `UpSet`, freed from its fixed frame
    type.) -/
def UpperAlong {F : Type*} [Preorder F] (P : F → Prop) : Prop :=
  ∀ ⦃f g : F⦄, f ≤ g → P f → P g

/-- **THE COMPOSITION LAW (what the mesh consumes).** A monotone map between
    frame orders pulls truth-bearing quantities back: if `φ` sends shard frames
    into parent frames order-respectingly, every monotone verdict of the parent
    is a monotone verdict of the shard, with no recomputation. -/
theorem UpperAlong.comap {F G : Type*} [Preorder F] [Preorder G]
    {P : G → Prop} (hP : UpperAlong P) {φ : F → G} (hφ : Monotone φ) :
    UpperAlong (P ∘ φ) :=
  fun _ _ hfg h => hP (hφ hfg) h

/-- **THE ANTI-GAUGE LEMMA, once.** A quantity taking two values along the order
    is frame-relative: no reading of it is invariant across frames. Each source
    file argued this locally; it is one line, here, for all of them. -/
theorem not_invariant_of_two_values {F : Type*} [Preorder F]
    {P : F → Prop} {f g : F} (hf : P f) (hg : ¬ P g) :
    ¬ ∀ x y : F, P x ↔ P y :=
  fun h => hg ((h g f).mpr hf)

/-! ### The coarsening axis on views, and the strengthened entropy law -/

variable {State : Type*} [Fintype State]

/-- `view` is coarser than `view'` when it factors through it: everything the
    coarse reading knows, the fine reading determines. This is the frame order
    on VIEWS — `Core/FrameEntropy`'s refinement is the special case
    `h = Prod.fst`. -/
def CoarserThan {C C' : Type*} (view : State → C) (view' : State → C') : Prop :=
  ∃ h : C' → C, view = h ∘ view'

omit [Fintype State] in
/-- Coarsening is reflexive and composes — the axis is a genuine preorder. -/
theorem coarserThan_refl {C : Type*} (view : State → C) : CoarserThan view view :=
  ⟨id, rfl⟩

omit [Fintype State] in
theorem coarserThan_trans {C C' C'' : Type*} {v : State → C} {v' : State → C'}
    {v'' : State → C''} (h₁ : CoarserThan v v') (h₂ : CoarserThan v' v'') :
    CoarserThan v v'' := by
  obtain ⟨h, rfl⟩ := h₁
  obtain ⟨h', rfl⟩ := h₂
  exact ⟨h ∘ h', rfl⟩

/-- **THE AXIS LAW, strengthening `frameEntropy_refine_le`.** Under ANY
    coarsening — not merely the forget-one-detail refinement — the fiber at an
    attained reading grows: what a coarser frame leaves undetermined includes
    everything the finer one did. -/
theorem fiber_antitone_of_coarser {C C' : Type*} [DecidableEq C] [DecidableEq C']
    {view : State → C} {view' : State → C'} (h : CoarserThan view view')
    (s : State) :
    FrameEntropy.fiber view' (view' s) ⊆ FrameEntropy.fiber view (view s) := by
  obtain ⟨g, rfl⟩ := h
  intro t ht
  simp only [FrameEntropy.fiber, Finset.mem_filter, Finset.mem_univ, true_and] at ht ⊢
  simp [Function.comp, ht]

/-- And the entropy consequence: entropy is antitone along the whole coarsening
    axis. (`frameEntropy` is `Core/FrameEntropy`'s; the fiber there and
    `GrainFloor.fiber` here are definitionally the same filter.) -/
theorem frameEntropy_antitone_of_coarser {C C' : Type*} [DecidableEq C] [DecidableEq C']
    {view : State → C} {view' : State → C'} (h : CoarserThan view view')
    (s : State) :
    FrameEntropy.frameEntropy view' (view' s) ≤ FrameEntropy.frameEntropy view (view s) := by
  unfold FrameEntropy.frameEntropy
  apply Real.log_le_log
  · have h1 : 1 ≤ (FrameEntropy.fiber view' (view' s)).card :=
      Finset.card_pos.mpr ⟨s, FrameEntropy.mem_fiber_self view' s⟩
    exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one h1
  · exact_mod_cast Finset.card_le_card (fiber_antitone_of_coarser h s)

/-! ### The three published instances, re-derived -/

/-- Instance 1 — `Core/FrameOrder`: repairability is `UpperAlong` the corpus
    order. (The `Preorder` on frames is list inclusion, as there.) -/
theorem repairable_upperAlong (a : String) :
    ∀ ⦃f g : Corpus⦄, (∀ x, x ∈ f → x ∈ g) → Repairable a f → Repairable a g :=
  fun _ _ hfg h => hfg a h

/-- Instance 2 — `Core/GrainFloor`: admissibility of a fixed claim is
    `UpperAlong` the tier order (tiers ordered by "finer": `T ≤ T'` iff
    `T.g0 ≤ T'.g0` read with the finer tier below). -/
theorem admissible_upperAlong (c : GrainFloor.Claim) :
    ∀ ⦃T T' : GrainFloor.Tier⦄, T'.g0 ≤ T.g0 →
      GrainFloor.admissible T c → GrainFloor.admissible T' c :=
  fun _ _ h hc => GrainFloor.reroot_finer_admits_more h hc

omit [Fintype State] in
/-- Instance 3 — `Core/FrameEntropy`: the published refinement law is the
    `Prod.fst` case of the axis law. -/
theorem refine_is_a_coarsening {C D : Type*}
    (view : State → C) (d : State → D) :
    CoarserThan view (fun s => (view s, d s)) :=
  ⟨Prod.fst, rfl⟩

/-- And the three quantities are frame-RELATIVE, by the one lemma: exhibited on
    `GrainFloor`'s own tiers, where a claim is served finely and refused
    coarsely. -/
theorem admissible_not_invariant :
    ¬ ∀ T T' : GrainFloor.Tier,
        GrainFloor.admissible T GrainFloor.z0CrackClaim ↔
        GrainFloor.admissible T' GrainFloor.z0CrackClaim := by
  intro h
  exact GrainFloor.z0_crack_claim_inadmissible
    ((h GrainFloor.z0Tier ⟨1 / 10000000, by norm_num⟩).mpr (by
      simp only [GrainFloor.admissible_iff, GrainFloor.z0CrackClaim]
      norm_num))

end CIRISOntology.Core.FrameAxis
