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
* every distinct two-site region has entropy exactly 2 log 2;
* this entropy saturates the exact Gibbs/von-Neumann ceiling for any two-qubit density.

Thus the candidate satisfies a finite analogue of the "vacuum entanglement is locally maximal"
ingredient in Jacobson's entanglement-equilibrium route. But two further obligations survive.
First, the same state FAILS a naive geometric area law if "area" is raw graph-edge count:
an adjacent pair on C5 has 2 cut edges, a separated pair has 4, while both have the same
entropy. Second, each two-site reduction is proportional to the identity, hence commutes with
every local operator and is invariant under every local unitary conjugation. The reduced state
alone therefore selects no distinguished local basis/boost flow; causal/dynamical structure must
supply that part of an Unruh/Bisognano-Wichmann-style bridge.

This is not a kill of DM-as-vacuum. It is a kill of the cheapest bridge from the currently
mechanized C5 whole-state to horizon area and temperature.
-/

import CIRISOntology.Core.BellCeiling
import CIRISOntology.Core.ThermalScale
import Mathlib.Tactic

namespace CIRISOntology.Core.DMVacuum

open Matrix
open scoped BigOperators ComplexOrder

variable {𝕜 : Type*} [RCLike 𝕜]

/-- A deliberately narrow finite DM-vacuum test predicate. The `DM` name is load-bearing:
    this is the vacuum property package for the existing dark-medium/capacity wager, not a
    new independent vacuum ontology. It asks only for global purity and maximally mixed
    two-site views; geometry and thermal/boost structure are tested separately below. -/
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

/-- The uniform two-bit state is a probability distribution. -/
theorem uniformPair_isProb : IsProb uniformPair := by
  constructor
  · intro x
    norm_num [uniformPair]
  · norm_num [uniformPair, Fintype.sum_prod_type, Fintype.sum_bool]

private lemma log_quarter : Real.log ((1 : ℝ) / 4) = -(2 * Real.log 2) := by
  rw [one_div, show (4 : ℝ) = 2 ^ 2 by norm_num, Real.log_inv, Real.log_pow]
  norm_num

private lemma log_four : Real.log (4 : ℝ) = 2 * Real.log 2 := by
  rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.log_pow]
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
  · simp [diagEmbed, uniformPair, map_ofNat]
  · simp [diagEmbed, Matrix.one_apply_ne hxy, Matrix.diagonal_apply_ne _ hxy]

/-- Every distinct two-site reading of the finite DM-vacuum candidate carries exactly
    two bits (natural-log units: 2 log 2) of entanglement entropy. -/
theorem psiC5_two_site_entropy {i j : Fin 5} (hij : i ≠ j) :
    vnEntropy (pairPtr i j (PsiC5 (𝕜 := 𝕜))) = 2 * Real.log 2 := by
  rw [pairPtr_PsiC5 hij, quarter_one_eq_diagEmbed, vnEntropy_diagEmbed,
      entropy_uniformPair]

/-- Every distinct two-site DM-vacuum reading is itself a density operator. -/
theorem psiC5_two_site_isDensity {i j : Fin 5} (hij : i ≠ j) :
    IsDensity (pairPtr i j (PsiC5 (𝕜 := 𝕜))) := by
  rw [pairPtr_PsiC5 hij, quarter_one_eq_diagEmbed]
  exact isDensity_diagEmbed uniformPair_isProb

/-- FINITE ENTANGLEMENT-EQUILIBRIUM WITNESS. Every distinct two-site DM-vacuum
    region saturates the von Neumann entropy ceiling: no other two-qubit density
    has higher entropy. This reuses the repository's quantum Gibbs bound. -/
theorem psiC5_two_site_entropy_is_maximal {i j : Fin 5} (hij : i ≠ j)
    (σ : Matrix (Bool × Bool) (Bool × Bool) 𝕜) (hσ : IsDensity σ) :
    vnEntropy σ ≤ vnEntropy (pairPtr i j (PsiC5 (𝕜 := 𝕜))) := by
  calc
    vnEntropy σ ≤ Real.log (Fintype.card (Bool × Bool)) := vnEntropy_le_log_card hσ
    _ = Real.log (4 : ℝ) := by norm_num
    _ = 2 * Real.log 2 := log_four
    _ = vnEntropy (pairPtr i j (PsiC5 (𝕜 := 𝕜))) :=
      (psiC5_two_site_entropy hij).symm

/-! ### Boost/thermal test: the reduced state itself selects no local direction -/

/-- A distinct two-site DM-vacuum reduction commutes with every local operator because
    it is proportional to identity. Thus the reduced density alone contains no preferred
    operator direction from which to read a boost generator. -/
theorem psiC5_two_site_commutes_with_every_operator {i j : Fin 5} (hij : i ≠ j)
    (A : Matrix (Bool × Bool) (Bool × Bool) 𝕜) :
    pairPtr i j (PsiC5 (𝕜 := 𝕜)) * A = A * pairPtr i j (PsiC5 (𝕜 := 𝕜)) := by
  rw [pairPtr_PsiC5 hij]
  simp [Matrix.smul_mul, Matrix.mul_smul]

/-- Stronger symmetry statement: every local unitary conjugation leaves the reduced
    DM-vacuum state unchanged. Any Rindler/boost direction must therefore be supplied by
    the causal/dynamical chart, not selected by this reduced density matrix alone. -/
theorem psiC5_two_site_unitary_invariant {i j : Fin 5} (hij : i ≠ j)
    (U : Matrix.unitaryGroup (Bool × Bool) 𝕜) :
    (U : Matrix (Bool × Bool) (Bool × Bool) 𝕜)
        * pairPtr i j (PsiC5 (𝕜 := 𝕜))
        * star (U : Matrix (Bool × Bool) (Bool × Bool) 𝕜)
      = pairPtr i j (PsiC5 (𝕜 := 𝕜)) := by
  have hU : (U : Matrix (Bool × Bool) (Bool × Bool) 𝕜)
      * star (U : Matrix (Bool × Bool) (Bool × Bool) 𝕜) = 1 :=
    mem_unitaryGroup_iff.mp U.2
  rw [pairPtr_PsiC5 hij]
  simp [Matrix.mul_smul, Matrix.smul_mul, hU]

/-- DM-named specialization of the general scale obstruction: a positive physical
    temperature cannot be obtained from the dimensionless DM frame entropy alone while
    respecting arbitrary energy rescaling. The DM gravity chart must supply a physical
    scale (boost acceleration/surface gravity/Hamiltonian gap or equivalent). -/
def DMEntropyOnlyTemperature (T : ℝ → ℝ) : Prop :=
  ThermalScale.ScaleCovariantTemperature T

theorem no_positive_DM_entropy_only_temperature :
    ¬ ∃ T : ℝ → ℝ, DMEntropyOnlyTemperature T ∧ ∀ s : ℝ, 0 < T s := by
  simpa [DMEntropyOnlyTemperature] using
    ThermalScale.no_positive_scale_covariant_entropy_only_temperature

/-! ### Geometry test: raw cut-edge count is not the entropy area functional -/

/-- The five undirected edges of the C5 ring, listed once. -/
def c5Edges : List (Fin 5 × Fin 5) :=
  [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]

/-- Number of microscopic C5 relations crossing a region boundary. -/
def cutEdges (region : Finset (Fin 5)) : ℕ :=
  (c5Edges.filter fun e => decide (e.1 ∈ region) != decide (e.2 ∈ region)).length

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
