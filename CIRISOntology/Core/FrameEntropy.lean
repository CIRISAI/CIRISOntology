/-
CIRISOntology.Core.FrameEntropy — entropy comes free from the base frame, and this
file is the proof of exactly which entropy and exactly how free.

THE QUESTION (Eric, 2026-08-23): "I think we get entropy for free from the model —
comes from the base frame, right?"

THE ANSWER, made precise. Yes — with one honest qualification at the end. A frame
(chart, view) is a map from fine states to coarse readings. The frame's ENTROPY at
a reading is the log-count of the fine states compatible with it — the size of the
fiber: what the frame leaves undetermined, which is the same thing as what
refinement could still reveal. The model supplies the fiber with NO new structure:
it is the preimage of the very map the ledger already uses (`Core/Coordination`'s
fiber machinery, `Core/Lattice`'s sectors, the engine's latent children). Three
theorems then come free, and each is a load-bearing physics fact:

  * `frameEntropy_refine_le` — refining the frame can only lower entropy. Entropy
    is frame-relative and rides the frame axis, exactly where M15 said physics
    forces frame annotations. It is not a property of the holon; it is a property
    of (holon, frame).
  * `frameEntropy_add` — EXTENSIVITY IS FREE: fibers of independent subsystems
    multiply, so entropies add. The thermodynamic additivity of entropy is the
    ledger's compositional structure, not a further postulate.
  * `np_fiber_card` / `regplus_entropy_bounded` — the REG+ base frame's entropy is
    machine-checked: the fiber of `Core/Lattice.lean`'s `np` chart at any reading
    IS the conservation sector, so per-site frame entropy is ln 1, ln 2, or ln 3
    — the 53-sector object hands the engine its Boltzmann entropy with no choice
    made anywhere.

THE HONEST QUALIFICATION. What is free is the COUNTING (the fiber); reading the
log-count as thermodynamic entropy adds the uniform (maximum-entropy) weighting
over the fiber — the standard Boltzmann move, a chart choice, named here rather
than smuggled. And what is NOT free is entropic GRAVITY: the lake's
precedent-is-bits wager (Verlinde, Gough, the holographic school — credited there)
needs a temperature and a screen structure on top of S, and the two attempts to
cash its dark-energy normalization have KILLS ALREADY FIRED on the record
(Landauer leg at 3–5 dex; budget/FIRAS legs at 8.8 dex). This file supplies the S
the wager consumes; it supplies nothing the wager still owes. The quantum side of
the lake (`Core/EntropyIneq`'s `vnEntropy`) is the density-matrix counterpart;
this file is its classical, frame-indexed face.
-/
import CIRISOntology.Core.Lattice
import Mathlib.Analysis.SpecialFunctions.Log.Basic

namespace CIRISOntology.Core.FrameEntropy

open Finset

variable {State Chart : Type*} [Fintype State] [DecidableEq Chart]

/-- The fiber of a frame at a reading: every fine state the coarse reading leaves
    possible. The model already owns this object — it is the preimage of the
    ledger map. -/
def fiber (view : State → Chart) (c : Chart) : Finset State :=
  Finset.univ.filter (fun s => view s = c)

theorem mem_fiber_self (view : State → Chart) (s : State) :
    s ∈ fiber view (view s) := by
  simp [fiber]

/-- Frame entropy: the log-count of what the frame leaves undetermined. -/
noncomputable def frameEntropy (view : State → Chart) (c : Chart) : ℝ :=
  Real.log ((fiber view c).card)

/-- A reading actually attained has nonnegative entropy. -/
theorem frameEntropy_nonneg (view : State → Chart) (s : State) :
    0 ≤ frameEntropy view (view s) := by
  apply Real.log_nonneg
  have h : 1 ≤ (fiber view (view s)).card :=
    Finset.card_pos.mpr ⟨s, mem_fiber_self view s⟩
  exact_mod_cast h

/-- A frame that pins the state exactly carries zero entropy: determinacy is the
    zero of the frame's ledger. -/
theorem frameEntropy_eq_zero_of_card_one {view : State → Chart} {c : Chart}
    (h : (fiber view c).card = 1) : frameEntropy view c = 0 := by
  unfold frameEntropy
  rw [h]
  simp

/-! ### Refinement can only lower entropy -/

/-- A refined frame (the old reading plus any further detail) has a sub-fiber. -/
theorem fiber_refine_subset {Detail : Type*} [DecidableEq Detail]
    (view : State → Chart) (d : State → Detail) (c : Chart) (x : Detail) :
    fiber (fun s => (view s, d s)) (c, x) ⊆ fiber view c := by
  intro s hs
  simp only [fiber, Finset.mem_filter, Finset.mem_univ, true_and, Prod.mk.injEq] at hs ⊢
  exact hs.1

/-- **Entropy is what refinement has not yet revealed.** Refining the frame can
    only lower it — monotone in the frame axis, never in the holon. (Stated at an
    attained refined reading so both fibers are nonempty.) -/
theorem frameEntropy_refine_le {Detail : Type*} [DecidableEq Detail]
    (view : State → Chart) (d : State → Detail) (s : State) :
    frameEntropy (fun t => (view t, d t)) (view s, d s) ≤ frameEntropy view (view s) := by
  unfold frameEntropy
  apply Real.log_le_log
  · have h : 1 ≤ (fiber (fun t => (view t, d t)) (view s, d s)).card :=
      Finset.card_pos.mpr ⟨s, mem_fiber_self _ s⟩
    exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one h
  · exact_mod_cast Finset.card_le_card (fiber_refine_subset view d (view s) (d s))

/-! ### Extensivity is free: fibers multiply, entropies add -/

variable {State₂ Chart₂ : Type*} [Fintype State₂] [DecidableEq Chart₂]

/-- The fiber of a product frame is the product of the fibers. -/
theorem fiber_prod (v₁ : State → Chart) (v₂ : State₂ → Chart₂) (c₁ : Chart) (c₂ : Chart₂) :
    fiber (fun p : State × State₂ => (v₁ p.1, v₂ p.2)) (c₁, c₂)
      = (fiber v₁ c₁) ×ˢ (fiber v₂ c₂) := by
  ext p
  simp [fiber, Finset.mem_product, Prod.ext_iff]

/-- **EXTENSIVITY, free from the ledger's compositional structure.** Independent
    subsystems' frame entropies add, because their fibers multiply. Thermodynamic
    additivity of entropy is not a postulate here — it is the product structure of
    composition. (Stated at attained readings so both logs are of positive
    counts.) -/
theorem frameEntropy_add (v₁ : State → Chart) (v₂ : State₂ → Chart₂)
    (s₁ : State) (s₂ : State₂) :
    frameEntropy (fun p : State × State₂ => (v₁ p.1, v₂ p.2)) (v₁ s₁, v₂ s₂)
      = frameEntropy v₁ (v₁ s₁) + frameEntropy v₂ (v₂ s₂) := by
  unfold frameEntropy
  rw [fiber_prod, Finset.card_product]
  have h₁ : 0 < (fiber v₁ (v₁ s₁)).card := Finset.card_pos.mpr ⟨s₁, mem_fiber_self _ s₁⟩
  have h₂ : 0 < (fiber v₂ (v₂ s₂)).card := Finset.card_pos.mpr ⟨s₂, mem_fiber_self _ s₂⟩
  push_cast
  rw [Real.log_mul]
  · exact_mod_cast h₁.ne'
  · exact_mod_cast h₂.ne'

/-! ### The REG+ base frame's entropy, machine-checked

The fiber of `Core/Lattice.lean`'s conservation chart `np` at any attained reading
is the sector itself, so the base frame hands every site its Boltzmann entropy —
ln 1, ln 2, or ln 3 — with no choice made anywhere. -/

/-- Every sector of the REG+ base frame has one, two, or three states — the
    44/7/2 structure of `sector_dims`, read as fiber cardinalities. -/
theorem np_fiber_card : ∀ s : Fin 64,
    (fiber Lattice.np (Lattice.np s)).card = 1 ∨
    (fiber Lattice.np (Lattice.np s)).card = 2 ∨
    (fiber Lattice.np (Lattice.np s)).card = 3 := by
  decide

/-- The base frame's per-site entropy is bounded by ln 3 — the largest sector.
    Entropy came from the frame; the bound came from the ledger's own structure. -/
theorem regplus_entropy_bounded (s : Fin 64) :
    frameEntropy Lattice.np (Lattice.np s) ≤ Real.log 3 := by
  unfold frameEntropy
  apply Real.log_le_log
  · have h : 1 ≤ (fiber Lattice.np (Lattice.np s)).card :=
      Finset.card_pos.mpr ⟨s, mem_fiber_self _ s⟩
    exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one h
  · rcases np_fiber_card s with h | h | h <;> rw [h] <;> norm_num

end CIRISOntology.Core.FrameEntropy
