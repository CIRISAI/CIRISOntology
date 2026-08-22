/-
CIRISOntology.Core.Lattice — Brick 1 of the confrontation core: the REG+ lattice's
local conservation structure, machine-checked.

WHAT IS PROVED. The REG+ triangular lattice's local state space is the 2^6 = 64
occupancies of the six carries directions. With the standard FHP direction vectors
in axial integer coordinates, the conserved pair (N, P) — occupancy count and
total momentum — partitions the 64 states into exactly 53 sectors with dimension
profile 44 × dim-1, 7 × dim-2, 2 × dim-3 (`sector_count`, `sector_dims`), matching
the reference implementation's numerically verified table (R1 handoff, 7/7
invariant tests, zero cross-sector transition probability). The three-route sector
that carries the holonomy physics (Core/RouteSymmetry.lean) is the N = 2, P = 0
fiber, and it is exactly the three opposite-pair states {9, 18, 36}
(`three_route_sector`) — the lattice-side anchor for the 3×3 route Hamiltonian.

WHAT IS DEFINITIONAL, STATED HONESTLY. REG+ collisions are DEFINED as unitaries
block-diagonal in these fibers; `SectorPreserving.n_eq`/`.p_eq` record that any
such map conserves N and P — by construction, not discovery. The mechanized
CONTENT of this file is the sector table itself: that the conservation pair
carves 64 into precisely this 53-part structure is a fact about the object, and
now a theorem.
-/
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Matrix.Notation

namespace CIRISOntology.Core.Lattice

/-- The six FHP directions in axial integer coordinates; opposite pairs sum to 0. -/
def dir : Fin 6 → ℤ × ℤ := ![(1,0), (0,1), (-1,1), (-1,0), (0,-1), (1,-1)]

/-- Occupancy of direction `k` in local state `s` (bit representation). -/
def occ (s : Fin 64) (k : Fin 6) : Bool := Nat.testBit s.val k.val

/-- Particle count. -/
def N (s : Fin 64) : ℕ := (Finset.univ.filter (fun k => occ s k)).card

/-- Total momentum. -/
def P (s : Fin 64) : ℤ × ℤ := Finset.univ.sum (fun k => if occ s k then dir k else 0)

/-- The conserved label. -/
def np (s : Fin 64) : ℕ × ℤ × ℤ := (N s, P s)

/-- Opposite directions cancel: the direction set is momentum-balanced. -/
theorem dir_balanced : Finset.univ.sum dir = (0, 0) := by decide

/-- **The sector count**: (N, P) partitions the 64 local states into exactly 53
sectors. -/
theorem sector_count : (Finset.univ.image np).card = 53 := by decide

/-- **The dimension profile**: 44 sectors of dimension 1, 7 of dimension 2, 2 of
dimension 3 — the reference implementation's table, now machine-checked. -/
theorem sector_dims :
    ((Finset.univ.image np).filter
      (fun v => (Finset.univ.filter (fun s => np s = v)).card = 1)).card = 44 ∧
    ((Finset.univ.image np).filter
      (fun v => (Finset.univ.filter (fun s => np s = v)).card = 2)).card = 7 ∧
    ((Finset.univ.image np).filter
      (fun v => (Finset.univ.filter (fun s => np s = v)).card = 3)).card = 2 := by
  refine ⟨by decide, by decide, by decide⟩

/-- **The three-route anchor**: the N = 2, P = 0 sector is exactly the three
opposite-pair states — the arena of `Core/RouteSymmetry.lean`'s holonomy
theorems. -/
theorem three_route_sector :
    Finset.univ.filter (fun s => np s = (2, (0, 0))) =
      ({⟨9, by omega⟩, ⟨18, by omega⟩, ⟨36, by omega⟩} : Finset (Fin 64)) := by
  decide

/-- A local map is sector-preserving when it fixes the conserved label. REG+
collisions are unitaries block-diagonal in the `np` fibers, hence their
underlying state maps satisfy this by construction. -/
def SectorPreserving (f : Fin 64 → Fin 64) : Prop := ∀ s, np (f s) = np s

theorem SectorPreserving.n_eq {f : Fin 64 → Fin 64} (h : SectorPreserving f)
    (s : Fin 64) : N (f s) = N s := congrArg Prod.fst (h s)

theorem SectorPreserving.p_eq {f : Fin 64 → Fin 64} (h : SectorPreserving f)
    (s : Fin 64) : P (f s) = P s := congrArg Prod.snd (h s)

end CIRISOntology.Core.Lattice
