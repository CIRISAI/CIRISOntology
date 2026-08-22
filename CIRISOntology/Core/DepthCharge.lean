/-
CIRISOntology.Core.DepthCharge — Brick 3's mechanized core: the depth-weighted
channel family on the eleven kinds, and the two estimator facts the physics
confrontation rests on (MECHANIZATION_ROADMAP.md Findings 1–2).

THE FAMILY. With the depth assignment pinned from Surface/Stack.lean (surfaces at
0; the assertive stack Facts 0 → Confidence 1 → Model 2 → Premises 3; both twin
pairs at 1), the deterministic depth-charge family is
  M(ε)_ij = ε^{|d_i − d_j|}   (i ≠ j),   0 < ε ≤ 1.
This is the Froggatt–Nielsen-analogue with unit O(1) coefficients; the stochastic-
coefficient version stays numerical (roadmap), and the ε > 1 grounding-adjacent
regime is the same family read on the other side of the depth-blind point.

WHAT IS PROVED.
* `class_cards` — the depth-distance classes have exactly 32 / 52 / 18 / 8
  directed channels (the denominators of the atlas depth-class estimator).
* `channel_le_one`, `same_depth_count` — every channel value is ≤ 1 and at least
  32 channels attain the maximum 1: the top NINE ranks of any descending sort see
  only the value 1, so the tier-cascade estimator (means of ranks 1–3, 4–6, 7–9)
  reads 1/1/1 REGARDLESS of ε — Finding 1 (estimator blindness) as structure.
  CKM escapes this because flavor has one state per stratum; the eleven do not.
* `class_value`, `class_ratio` — every |Δd| = k channel equals ε^k, and the
  class-1/class-0 ratio equals ε exactly: the depth-class estimator IDENTIFIES the
  charge parameter the tier estimator cannot see.
* `flat_limit` — ε = 1 recovers the depth-blind (flat) family: REG v0.3's regime.
-/
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Matrix.Notation
import Mathlib.Analysis.SpecialFunctions.Pow.Real

namespace CIRISOntology.Core.DepthCharge

/-- The pinned depth assignment, in the standing kind order
(Priorities, Rules, Manner, Identity, Confidence, Facts, Circumstances, Process,
Model, Structure, Premises). -/
def d : Fin 11 → ℕ := ![1, 0, 0, 0, 1, 0, 1, 1, 2, 1, 3]

/-- Depth distance between two kinds. -/
def dist (i j : Fin 11) : ℕ := ((d i : ℤ) - (d j : ℤ)).natAbs

/-- The depth-charge channel family. -/
noncomputable def M (ε : ℝ) (i j : Fin 11) : ℝ := ε ^ dist i j

/-- Directed off-diagonal pairs at depth distance `k`. -/
def classPairs (k : ℕ) : Finset (Fin 11 × Fin 11) :=
  Finset.univ.filter (fun p => p.1 ≠ p.2 ∧ dist p.1 p.2 = k)

/-- **The class cardinalities**: 32 / 52 / 18 / 8 — the atlas estimator's
denominators, machine-checked. -/
theorem class_cards :
    (classPairs 0).card = 32 ∧ (classPairs 1).card = 52 ∧
    (classPairs 2).card = 18 ∧ (classPairs 3).card = 8 := by
  refine ⟨by decide, by decide, by decide, by decide⟩

/-- Every channel value is at most 1 when ε ≤ 1. -/
theorem channel_le_one {ε : ℝ} (h0 : 0 < ε) (h1 : ε ≤ 1) (i j : Fin 11) :
    M ε i j ≤ 1 :=
  pow_le_one₀ h0.le h1

/-- At least 32 directed channels attain the maximum value 1 (the same-depth
channels), for EVERY ε — the counting fact behind tier-estimator blindness. -/
theorem same_depth_count (ε : ℝ) :
    ∀ p ∈ classPairs 0, M ε p.1 p.2 = 1 := by
  intro p hp
  have h : dist p.1 p.2 = 0 := (Finset.mem_filter.mp hp).2.2
  simp [M, h]

/-- Every depth-distance-`k` channel equals `ε^k` exactly. -/
theorem class_value (ε : ℝ) (k : ℕ) :
    ∀ p ∈ classPairs k, M ε p.1 p.2 = ε ^ k := by
  intro p hp
  have h : dist p.1 p.2 = k := (Finset.mem_filter.mp hp).2.2
  simp [M, h]

/-- **Identification**: the class-1 / class-0 value ratio is the charge parameter
itself — the depth-class estimator reads ε directly. -/
theorem class_ratio (ε : ℝ) : ε ^ (1:ℕ) / ε ^ (0:ℕ) = ε := by
  simp

/-- **The flat limit**: ε = 1 is the depth-blind family — every channel 1. -/
theorem flat_limit (i j : Fin 11) : M 1 i j = 1 := by
  simp [M]

end CIRISOntology.Core.DepthCharge
