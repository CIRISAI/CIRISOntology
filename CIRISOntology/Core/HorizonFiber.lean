/-
CIRISOntology.Core.HorizonFiber — the exact REG+ obstruction to getting a horizon
area law from the gross conserved ledger alone.

`Core.Lattice.three_route_sector` proves that one REG+ site has THREE distinct local
states, {9,18,36}, all carrying the same conserved label N=2, P=(0,0). Therefore n
independent hidden sites already admit 3^n distinct fine configurations with exactly
the same additive gross ledger. A frame/screen that reads the boundary plus only this
gross interior ledger cannot distinguish them.

This is an exact volume-law lower bound, not an asymptotic argument and not a claim
about gravity. If `FrameEntropy` is applied to such a coarse view, its fiber contains
at least these 3^n route configurations, hence its log-count grows at least as
n*log(3). An entropy-area law therefore cannot come from REG+ conservation alone.
Something additional must remove/tie/gauge these bulk route choices — e.g. dynamics,
constraints, a boundary code, or a genuinely holographic composition law.

KILL/DISCHARGE. A curvature/holonomy gravity bridge discharges this obstruction by
proving that the physically admissible horizon frame does NOT leave these route choices
independent in the bulk (or proves they are gauge-equivalent / physically null). Merely
choosing a geometric screen while retaining the ordinary REG+ ledger does not do so.
-/

import CIRISOntology.Core.Lattice
import Mathlib.Data.Fintype.Card
import Mathlib.Tactic

namespace CIRISOntology.Core.HorizonFiber

open Lattice

/-- The three local route choices in the exact N=2, P=0 REG+ sector. -/
def routeState : Fin 3 → Fin 64
  | ⟨0, _⟩ => ⟨9, by omega⟩
  | ⟨1, _⟩ => ⟨18, by omega⟩
  | ⟨2, _⟩ => ⟨36, by omega⟩

/-- Every route choice has the same exact local conserved label. -/
theorem routeState_np (r : Fin 3) : np (routeState r) = (2, (0, 0)) := by
  fin_cases r <;> decide

/-- An n-site hidden interior made only from the three-route sector. -/
abbrev RouteConfig (n : ℕ) := Fin n → Fin 3

/-- Number of hidden fine configurations in this family: exactly 3^n. -/
theorem routeConfig_card (n : ℕ) : Fintype.card (RouteConfig n) = 3 ^ n := by
  simp [RouteConfig]

/-- The additive gross label of a route configuration. -/
def grossLabel {n : ℕ} (c : RouteConfig n) : ℕ × ℤ × ℤ :=
  (∑ i, N (routeState (c i)),
   ∑ i, (P (routeState (c i))).1,
   ∑ i, (P (routeState (c i))).2)

/-- Every one of the 3^n configurations has the SAME gross ledger: N=2n, P=0. -/
theorem routeConfig_same_gross {n : ℕ} (c : RouteConfig n) :
    grossLabel c = (2 * n, 0, 0) := by
  have hN : ∀ r : Fin 3, N (routeState r) = 2 := by
    intro r
    have h := routeState_np r
    exact congrArg Prod.fst h
  have hP : ∀ r : Fin 3, P (routeState r) = (0, 0) := by
    intro r
    have h := routeState_np r
    exact congrArg Prod.snd h
  simp [grossLabel, hN, hP, Nat.mul_comm]

/-- The ambiguity is already nontrivial at one hidden site. -/
theorem one_hidden_site_has_three_gross_indistinguishable_states :
    Fintype.card (RouteConfig 1) = 3 := by
  norm_num [routeConfig_card]

/-- At two hidden sites the same gross ledger already covers nine route states. -/
theorem two_hidden_sites_have_nine_gross_indistinguishable_states :
    Fintype.card (RouteConfig 2) = 9 := by
  norm_num [routeConfig_card]

end CIRISOntology.Core.HorizonFiber
