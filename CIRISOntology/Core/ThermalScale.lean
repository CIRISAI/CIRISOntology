/-
CIRISOntology.Core.ThermalScale — entropy does not supply a temperature scale.

`Core.FrameEntropy.frameEntropy` is a log-count. It is dimensionless and depends
only on the coarse map and the cardinality of its fiber. A thermal temperature,
by contrast, carries an energy scale (with k_B converting between temperature
and energy units).

The clean thought experiment is to keep the state space, coarse map and all
fiber cardinalities fixed while multiplying every physical energy by a positive
factor lambda. The frame entropy is unchanged. The corresponding thermal scale
must multiply by lambda. Therefore no nonzero temperature can be a function of
the dimensionless frame entropy alone while respecting that rescaling.

The theorem below is just that naturality obstruction, deliberately stripped of
thermodynamic detail. It does NOT say temperature cannot be derived in the full
holon theory. It says the derivation must consume at least one dimensionful
physical input: a Hamiltonian/energy gap, acceleration plus hbar/c/k_B, a surface
gravity, a clock scale, or an equivalent bridge. If such a scale is supplied by
the gravity chart, this obligation is discharged. If it is fitted or imported
solely to make the entropic force work, it is an external bridge constant.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace CIRISOntology.Core.ThermalScale

/-- A proposed temperature obtained only from a dimensionless entropy is scale
    covariant if rescaling the physical energy unit by any positive lambda scales
    the output temperature by lambda while leaving the entropy argument fixed. -/
def ScaleCovariantTemperature (T : ℝ → ℝ) : Prop :=
  ∀ λ : ℝ, 0 < λ → ∀ s : ℝ, T s = λ * T s

/-- The only scale-covariant temperature function of a dimensionless entropy
    alone is identically zero. A nonzero thermal scale therefore requires an
    additional dimensionful input. -/
theorem scale_covariant_entropy_only_temperature_is_zero
    (T : ℝ → ℝ) (hT : ScaleCovariantTemperature T) :
    ∀ s : ℝ, T s = 0 := by
  intro s
  have h2 := hT 2 (by norm_num) s
  linarith

/-- Existential kill form: there is no everywhere-positive temperature obtained
    from dimensionless entropy alone that obeys physical energy rescaling. -/
theorem no_positive_scale_covariant_entropy_only_temperature :
    ¬ ∃ T : ℝ → ℝ,
        ScaleCovariantTemperature T ∧ ∀ s : ℝ, 0 < T s := by
  rintro ⟨T, hT, hpos⟩
  have hz := scale_covariant_entropy_only_temperature_is_zero T hT 0
  exact (hpos 0).ne' hz.symm

end CIRISOntology.Core.ThermalScale
