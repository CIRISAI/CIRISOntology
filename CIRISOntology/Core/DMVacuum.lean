/-
CIRISOntology.Core.DMVacuum — finite theorem-level tests for the existing DM-as-vacuum wager.

NAMING / STATUS. The published stance already wagers that dark matter is the medium/capacity
(the "paper" / capacity of the ledger). This file does NOT promote that physical identification.
It does one narrower thing requested by the gravity programme: every formal property called a
"vacuum" property here is explicitly a DM-vacuum property, so a successful horizon/entropy
bridge cannot quietly introduce a second vacuum object beside the dark-medium wager.

The first finite test double reuses the repository's strongest exact quantum whole-state,
`BellCeiling.PsiC5`. This cashes existing machinery rather than defining new entropy:

* the global state is pure (`vnEntropy_PsiC5 = 0`);
* every two-site reduction is maximally mixed (`pairPtr_PsiC5`);
* therefore every distinct two-site region has entropy exactly 2 log 2.

That is a useful vacuum-like entanglement witness, but the same state FAILS a naive geometric
area law if "area" is identified with the raw number of graph edges crossing the region:
an adjacent pair on C5 has 2 cut edges, a separated pair has 4, while both have the same
entropy. Thus "quantum whole-only + locality graph" does not automatically produce the area
functional gravity needs. The eventual DM vacuum must derive the correct geometric boundary
functional (or a gauge/rank reduction of it), not merely count microscopic cut relations.

This is not a kill of DM-as-vacuum. It is a kill of the cheapest bridge from the currently
mechanized C5 whole-state to horizon area.
-/

import CIRISOntology.Core.BellCeiling
import Mathlib.Tactic

namespace CIRISOntology.Core.DMVacuum

open Matrix
open scoped BigOperators ComplexOrder

variable {𝕜 : Type*} [RCLike 𝕜]

/-- A deliberately narrow finite DM-vacuum test predicate. The `DM` name is load-bearing:
    this is the vacuum property package for the existing dark-medium/capacity wager, not a
    new independent vacuum ontology. It asks only for global purity and maximally mixed
    two-site views; geometry is tested separately below. -/
def IsFiniteDMVacuum (ρ : Matrix (Fin 5 → Bool) (Fin 5 → Bool) 𝕜) : Prop :=
  vnEntropy ρ = 0 ∧
  ∀ {i j : Fin 5}, i ≠ j → pairPtr i j ρ = (1 / 4 : 𝕜) • 1

/-- The existing C5 graph state satisfies the finite DM-vacuum information conditions. -/
theorem psiC5_isFiniteDMVacuum : IsFiniteDMVacuum (PsiC5 (𝕜 := 𝕜)) := by
  constructor
  · exact vnEntropy_PsiC5
  · intro i j hij
    exact pairPtr_PsiC5 hij

/-- Uniform distribution on a two-bit region. -/
noncomputable def uniformPair : Bool × Bool → ℝ := fun _ => 1 / 4

private lemma log_quarter : Real.log ((1 : ℝ) / 4) = -(2 * Real.log 2) := by
  rw [one_div, show (4 : ℝ) = 2 ^ 2 by norm_num, Real.log_inv, Real.log_pow]
  norm_num

private lemma entropy_uniformPair : entropy uniformPair = 2 * Real.log 2 := by
  unfold entropy uniformPair
  simp only [Fintype.sum_prod_type, Fintype.sum_bool]
  norm_num [log_quarter]
  ring

/-- The maximally mixed two-qubit matrix is exactly the diagonal embedding of the
    uniform two-bit distribution. -/
theorem quarter_one_eq_diagEmbed :
    ((1 / 4 : 𝕜) • (1 : Matrix (Bool × Bool) (Bool × Bool) 𝕜))
      = diagEmbed (𝕜 := 𝕜) uniformPair := by
  ext x y
  rcases eq_or_ne x y with rfl | hxy
  · simp [diagEmbed, uniformPair]
  · simp [diagEmbed, Matrix.one_apply_ne hxy, Matrix.diagonal_apply_ne _ hxy]

/-- Every distinct two-site reading of the finite DM-vacuum candidate carries exactly
    two bits (natural-log units: 2 log 2) of entanglement entropy. -/
theorem psiC5_two_site_entropy {i j : Fin 5} (hij : i ≠ j) :
    vnEntropy (pairPtr i j (PsiC5 (𝕜 := 𝕜))) = 2 * Real.log 2 := by
  rw [pairPtr_PsiC5 hij, quarter_one_eq_diagEmbed, vnEntropy_diagEmbed,
      entropy_uniformPair]

/-! ### Geometry test: raw cut-edge count is not the entropy area functional -/

/-- The five undirected edges of the C5 ring, listed once. -/
def c5Edges : List (Fin 5 × Fin 5) :=
  [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]

/-- Number of microscopic C5 relations crossing a region boundary. -/
def cutEdges (region : Finset (Fin 5)) : ℕ :=
  (c5Edges.filter fun e => (e.1 ∈ region) != (e.2 ∈ region)).length

/-- Two adjacent sites have two cut relations. -/
theorem adjacent_pair_cutEdges : cutEdges ({0, 1} : Finset (Fin 5)) = 2 := by
  decide

/-- Two separated sites have four cut relations. -/
theorem separated_pair_cutEdges : cutEdges ({0, 2} : Finset (Fin 5)) = 4 := by
  decide

/-- Yet the adjacent and separated two-site regions have exactly the same entropy. -/
theorem adjacent_and_separated_same_entropy :
    vnEntropy (pairPtr (𝕜 := 𝕜) 0 1 PsiC5)
      = vnEntropy (pairPtr (𝕜 := 𝕜) 0 2 PsiC5) := by
  rw [psiC5_two_site_entropy (by decide : (0 : Fin 5) ≠ 1),
      psiC5_two_site_entropy (by decide : (0 : Fin 5) ≠ 2)]

/-- There is no positive constant entropy-per-raw-cut-edge that fits both regions.
    Therefore the C5 DM-vacuum candidate does not obtain a geometric area law merely by
    counting microscopic graph relations. A successful gravity bridge owes a different,
    physically derived boundary functional. -/
theorem no_positive_raw_cut_edge_area_density :
    ¬ ∃ α : ℝ, 0 < α ∧
      vnEntropy (pairPtr (𝕜 := 𝕜) 0 1 PsiC5) = α * cutEdges ({0, 1} : Finset (Fin 5)) ∧
      vnEntropy (pairPtr (𝕜 := 𝕜) 0 2 PsiC5) = α * cutEdges ({0, 2} : Finset (Fin 5)) := by
  rintro ⟨α, hα, hAdj, hSep⟩
  rw [psiC5_two_site_entropy (by decide : (0 : Fin 5) ≠ 1), adjacent_pair_cutEdges] at hAdj
  rw [psiC5_two_site_entropy (by decide : (0 : Fin 5) ≠ 2), separated_pair_cutEdges] at hSep
  have hlog : 0 < Real.log 2 := Real.log_pos (by norm_num)
  norm_num at hAdj hSep
  nlinarith

end CIRISOntology.Core.DMVacuum
