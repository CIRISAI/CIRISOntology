/-
CIRISOntology.Core.HolographicScaling — the area-law obligation.

`Core.FrameEntropy.frameEntropy_add` proves exact extensivity for independent
subsystems: product fibers multiply, so their frame entropies add. Consequently,
if a three-dimensional bulk is tiled by independent identical cells carrying
positive frame entropy `s`, doubling the linear size multiplies the bulk entropy
by eight.

A holographic screen with a size-independent entropy density instead scales with
area, so doubling linear size multiplies its budget by four. Both laws cannot be
the same positive entropy at more than one scale. The two-point contradiction is
all that is mechanized here; no continuum or gravity assumptions are needed.

This is NOT a refutation of holography or entropic gravity. It is the bridge
obligation: the gravity chart may not identify the already-proved independent
bulk frame entropy with screen entropy without deriving a nontrivial reduction
from bulk degrees of freedom to boundary degrees of freedom (constraints,
entanglement structure, gauge redundancy, causal accessibility, an area theorem,
etc.). If such a reduction is derived, this kill is discharged. If an area law is
simply inserted as an independent postulate, entropy did not come 'for free' all
the way to gravity.
-/

import CIRISOntology.Core.FrameEntropy

namespace CIRISOntology.Core.HolographicScaling

/-- A positive per-cell extensive entropy cannot obey one fixed area-density law
    at both linear size 1 and linear size 2. At L=1 the bulk has 1 cell and area
    unit 1; at L=2 it has 8 cells and area unit 4. -/
theorem positive_volume_entropy_not_same_area_law
    (s α : ℝ) (hs : 0 < s) :
    ¬ (s = α ∧ 8 * s = 4 * α) := by
  rintro ⟨h1, h2⟩
  rw [h1] at hs h2
  linarith

/-- Equivalent existential form: no size-independent screen coefficient can make
    positive independent-cell entropy simultaneously match volume scaling and
    area scaling at the first two cubic sizes. -/
theorem no_area_coefficient_for_positive_independent_bulk (s : ℝ) (hs : 0 < s) :
    ¬ ∃ α : ℝ, s = α ∧ 8 * s = 4 * α := by
  rintro ⟨α, h⟩
  exact positive_volume_entropy_not_same_area_law s α hs h

end CIRISOntology.Core.HolographicScaling
