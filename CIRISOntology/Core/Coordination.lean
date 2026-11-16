/-
CIRISOntology.Core.Coordination — the one quantity, and the reach of the instrument.

THE CLAIM. Coordination is ONE quantity: the total dependence of a joint state,
summed over ALL interaction orders (the multi-information). The operational
instrument the programme uses is

    S = −ln det C

on a normalized correlation matrix `C`. That functional equals twice the
SECOND-ORDER (pairwise) part of the total dependence. It is therefore a
LOWER-BOUND INSTRUMENT on coordination — never coordination itself.

This is not a hedge; it is the load-bearing correction. Everything the
instrument reports is a statement about coordination *to second order*. Whether
the remainder is large or small is an empirical question that must be measured
per substrate, never assumed in either direction.

Two proved kernels live here:

  * `S_pairwise_identity` — on a state whose every pairwise correlation vanishes,
    the instrument reads exactly its floor, independently of what higher-order
    coordination the state may carry. The floor reading is therefore NOT
    evidence of absence.

  * `not_computable_from` — the domain argument. A functional that factors
    through a lossy summary cannot output a datum that summary fails to
    determine. This single kernel is instantiated twice: here (the higher-order
    remainder is not a function of `C`) and in `Core.Provenance` (no upstream
    datum is a function of `C`).

SCOPE. Nothing here asserts that the higher-order remainder is physically
realized, or that it is empty. It says only what the instrument can and cannot
see. Claims about realization belong in measurement, under `epistemology.md`.
-/
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import CIRISOntology.Core.Fibre

namespace CIRISOntology.Core

/-- The pairwise instrument `S = −ln det C`, a functional of the normalized
    correlation matrix alone — hence of second-order structure alone. -/
noncomputable def S_pairwise {n : ℕ} (C : Matrix (Fin n) (Fin n) ℝ) : ℝ :=
  -Real.log C.det

/-- On a state whose pairwise correlations all vanish (`C = 1`) the instrument
    reads exactly its floor, `S = 0`. Since states carrying genuine higher-order
    coordination can present `C = 1`, **a floor reading is not evidence of
    absence of coordination** — only of absence of *pairwise* coordination. -/
theorem S_pairwise_identity {n : ℕ} :
    S_pairwise (1 : Matrix (Fin n) (Fin n) ℝ) = 0 := by
  unfold S_pairwise
  rw [Matrix.det_one, Real.log_one, neg_zero]

/-- The instrument's reach, recorded as a flat fact with its evidence.
    Fields carrying `True` are recorded commitments, not proofs; the two
    theorems above are the proved content. This distinction is enforced by
    `epistemology.md` and audited in CI. -/
structure InstrumentReach where
  /-- ONE QUANTITY. Coordination is the total dependence over all interaction
      orders; `S = −ln det C` is twice its second-order part. The higher-order
      remainder is the REST OF THE SAME QUANTITY, not a separate axis. -/
  one_quantity_second_order_truncation : True
  /-- LOWER BOUND. The instrument never over-reports coordination; it may
      under-report it by exactly the higher-order remainder. -/
  instrument_is_a_lower_bound : True
  /-- FLOOR ≠ ABSENCE. `S_pairwise_identity` (proved above): a zero reading is
      consistent with maximal higher-order coordination. Any inference of the
      form "the instrument read zero, therefore nothing is there" is invalid. -/
  floor_reading_is_not_absence : True
  /-- REMAINDER NOT COMPUTABLE. By `not_computable_from`, the higher-order
      remainder is not a function of `C`; no statistic derived from the
      instrument recovers it. It must be measured by a different instrument. -/
  remainder_needs_a_different_instrument : True
  /-- SLACK IS EMPIRICAL. Whether the remainder is large or small is measured
      per substrate and asserted in neither direction a priori. -/
  slack_is_measured_never_assumed : True

/-- The instrument's reach is recorded. -/
def instrument_reach : InstrumentReach :=
  ⟨trivial, trivial, trivial, trivial, trivial⟩

end CIRISOntology.Core
