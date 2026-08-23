/-
CIRISOntology.Core.DMModular — exact modular-energy form for a symmetric spin-1
DM quantum link.

The one-plaquette Gauss sector in `Core.DMGauge` has electric levels -1,0,+1.
Whenever a one-link reduced state is diagonal and charge-conjugation symmetric,
its probabilities have the form (p, p0, p).  The modular energies `-log rho` are
then not an arbitrary three-level operator: they are exactly an affine function
of the electric-energy operator E^2,

  K = a I + beta E^2,
  a    = -log p0,
  beta = log (p0 / p).

This is the finite theorem-level content behind the simulator observation that the
DM-vacuum link's thermal/modular generator is the same local gauge-energy operator
already present in the Hamiltonian.  It does NOT derive a Rindler temperature or
Einstein gravity.  It removes one arbitrariness: once the reduced state has the
Gauss/charge-conjugation form, no extra local operator basis is required to express K.
-/

import CIRISOntology.Core.DMGauge
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic

namespace CIRISOntology.Core.DMModular

open DMGauge

/-- Charge-conjugation-symmetric one-link probability spectrum `(p,p0,p)`. -/
def linkProb (p p0 : ℝ) : FluxState → ℝ
  | ⟨0, _⟩ => p
  | ⟨1, _⟩ => p0
  | ⟨2, _⟩ => p

/-- Modular energy of a diagonal link state. -/
noncomputable def modularEnergy (p p0 : ℝ) (q : FluxState) : ℝ :=
  -Real.log (linkProb p p0 q)

/-- Electric energy cast to the real scalars used by modular thermodynamics. -/
def electricSqR (q : FluxState) : ℝ := (electricSq q : ℝ)

/-- The coefficient multiplying electric energy in the link modular Hamiltonian. -/
noncomputable def modularBeta (p p0 : ℝ) : ℝ := Real.log (p0 / p)

/-- Exact finite modular theorem: a symmetric spin-1 link reduction has
`K = -log(p0) I + log(p0/p) E^2`. -/
theorem modularEnergy_eq_affine_electric
    (p p0 : ℝ) (hp : 0 < p) (hp0 : 0 < p0) (q : FluxState) :
    modularEnergy p p0 q =
      -Real.log p0 + modularBeta p p0 * electricSqR q := by
  fin_cases q
  · simp only [modularEnergy, linkProb, modularBeta, electricSqR, electricSq, flux]
    rw [Real.log_div hp0.ne' hp.ne']
    push_cast
    ring
  · simp [modularEnergy, linkProb, modularBeta, electricSqR, electricSq, flux]
  · simp only [modularEnergy, linkProb, modularBeta, electricSqR, electricSq, flux]
    rw [Real.log_div hp0.ne' hp.ne']
    push_cast
    ring

/-- At a flat local spectrum the modular gauge coupling vanishes; this is the
finite obstruction seen in the maximally-mixed C5 reductions. -/
theorem modularBeta_eq_zero_of_flat (p : ℝ) (hp : 0 < p) :
    modularBeta p p = 0 := by
  unfold modularBeta
  rw [div_self hp.ne']
  simp

/-- If the zero-flux state is more probable than either charged flux state, the
modular electric-energy coefficient is positive. -/
theorem modularBeta_pos_of_zero_flux_dominates
    (p p0 : ℝ) (hp : 0 < p) (hdom : p < p0) :
    0 < modularBeta p p0 := by
  unfold modularBeta
  apply Real.log_pos
  exact (one_lt_div hp).mpr hdom

end CIRISOntology.Core.DMModular
