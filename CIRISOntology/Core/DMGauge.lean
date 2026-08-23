/-
CIRISOntology.Core.DMGauge — finite U(1) quantum-link structure on the existing
three-state route local space.

This file does not introduce a new ontological state category.  It reuses the same
three-dimensional local cardinality already singled out by the REG+ N=2,P=0 route
sector, but reads the three basis states as spin-1 electric flux -1,0,+1.

The purpose is deliberately narrow and falsifiable:

* `raise_flux_step` is the basis-action form of [E,U] = U;
* a plaquette raise increments every oriented edge by one where the truncated
  spin-1 raising operator is defined;
* every vertex Gauss difference is therefore exactly preserved;
* the closed-flux physical sector of one plaquette contains exactly three states.

That is enough structure for the simulator to carry the same local state as a finite
U(1) quantum link and for later gravity work to ask whether the DM-vacuum dynamics on
this physical subspace has the required modular/causal properties.
-/

import Mathlib.Data.Fintype.Card
import Mathlib.Tactic

namespace CIRISOntology.Core.DMGauge

/-- The existing three-state local space, interpreted as electric flux -1,0,+1. -/
abbrev FluxState := Fin 3

/-- Spin-1 electric flux eigenvalue. -/
def flux : FluxState → ℤ
  | ⟨0, _⟩ => -1
  | ⟨1, _⟩ => 0
  | ⟨2, _⟩ => 1

/-- Truncated U(1) raising action.  The top spin-1 state is annihilated. -/
def raise : FluxState → Option FluxState
  | ⟨0, _⟩ => some ⟨1, by omega⟩
  | ⟨1, _⟩ => some ⟨2, by omega⟩
  | ⟨2, _⟩ => none

/-- Basis-action form of `[E,U]=U`: whenever `U` raises a state, electric flux
increases by exactly one unit. -/
theorem raise_flux_step {q q' : FluxState} (h : raise q = some q') :
    flux q' - flux q = 1 := by
  fin_cases q <;> simp [raise] at h
  · subst q'; decide
  · subst q'; decide

/-- Four oriented links around one plaquette. Link `v` leaves vertex `v`, and
link `prev v` enters it. -/
abbrev PlaquetteConfig := Fin 4 → FluxState

/-- Previous edge in cyclic orientation. -/
def prev : Fin 4 → Fin 4
  | ⟨0, _⟩ => ⟨3, by omega⟩
  | ⟨1, _⟩ => ⟨0, by omega⟩
  | ⟨2, _⟩ => ⟨1, by omega⟩
  | ⟨3, _⟩ => ⟨2, by omega⟩

/-- Lattice U(1) Gauss charge at a vertex: outgoing minus incoming flux. -/
def gauss (c : PlaquetteConfig) (v : Fin 4) : ℤ :=
  flux (c v) - flux (c (prev v))

/-- `c'` is obtained by applying the plaquette raising operator to every oriented
link of `c`.  This relation is partial because spin-1 raising annihilates +1. -/
def PlaquetteRaised (c c' : PlaquetteConfig) : Prop :=
  ∀ i, raise (c i) = some (c' i)

/-- The magnetic plaquette move preserves every Gauss generator exactly.  This is
the basis-state version of `[G_v, B]=0`. -/
theorem plaquette_raise_preserves_gauss
    {c c' : PlaquetteConfig} (h : PlaquetteRaised c c') (v : Fin 4) :
    gauss c' v = gauss c v := by
  have hout := raise_flux_step (h v)
  have hin := raise_flux_step (h (prev v))
  unfold gauss
  linarith

/-- A closed-flux configuration has one common electric flux on the full loop. -/
def ClosedFlux (c : PlaquetteConfig) : Prop := ∀ i, c i = c 0

/-- Canonical closed loop carrying flux `q`. -/
def closedConfig (q : FluxState) : PlaquetteConfig := fun _ => q

@[simp] theorem closedConfig_closed (q : FluxState) : ClosedFlux (closedConfig q) := by
  intro i
  rfl

/-- Every closed-flux loop satisfies Gauss law at every vertex. -/
theorem closedFlux_gauss_zero {c : PlaquetteConfig} (hc : ClosedFlux c) (v : Fin 4) :
    gauss c v = 0 := by
  unfold gauss
  rw [hc v, hc (prev v)]
  ring

/-- The physical closed-flux sector is exactly one copy of the original three-state
local space. -/
def closedFluxEquiv : FluxState ≃ {c : PlaquetteConfig // ClosedFlux c} where
  toFun q := ⟨closedConfig q, closedConfig_closed q⟩
  invFun c := c.1 0
  left_inv q := rfl
  right_inv c := by
    apply Subtype.ext
    funext i
    exact (c.2 i).symm

/-- One plaquette therefore has exactly three Gauss-closed uniform-flux basis states. -/
theorem closedFlux_card : Fintype.card {c : PlaquetteConfig // ClosedFlux c} = 3 := by
  simpa using Fintype.card_congr closedFluxEquiv.symm

/-- Electric-energy level used by the finite quantum-link Hamiltonian. -/
def electricSq : FluxState → ℤ := fun q => flux q * flux q

@[simp] theorem electricSq_neg : electricSq ⟨0, by omega⟩ = 1 := by decide
@[simp] theorem electricSq_zero : electricSq ⟨1, by omega⟩ = 0 := by decide
@[simp] theorem electricSq_pos : electricSq ⟨2, by omega⟩ = 1 := by decide

end CIRISOntology.Core.DMGauge
