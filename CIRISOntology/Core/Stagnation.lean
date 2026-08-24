/-
CIRISOntology.Core.Stagnation — motion is not error, and non-monotone reports
refute optimality with no reference in sight.

WHAT FORCED IT (the Q8 divergence, 2026-08-24; `sim_engine/output/q8_mps`,
Q8_MPS_PREREG.md as amended). The DMRG campaign measured the two kinds of
being wrong coming apart by nine orders of magnitude: at the stuck configs the
discarded weight — the process's own motion ledger — fell to 1e-17 while the
true error sat at 1e-2. Bigger ledger, worse answer, nothing truncated. The
mechanism is `Core/SelfAudit`'s limit wearing an optimizer: a sweep stuck at a
fixed point of its own environment reports zero motion, and zero motion says
nothing about distance to the target. This file mechanizes the two theorems
Q9's certificate-of-motion is built on.

THE TWO THEOREMS.

  * `fixedPoint_motion_blind` — THE BLINDNESS. The self-residual d(T x, x) is
    zero at every fixed point, and two fixed points with identical (zero)
    motion readings differ arbitrarily in error: motion does not factor to
    error, in exactly the witness-pair form the lake states blindness in.
    Truncation error is auditable from inside; stagnation error is not.
  * `not_optimal_of_regression` — THE DETECTOR, and the reason it is honest.
    Nested search spaces have monotone optima (`isLeast_mono_of_subset`:
    enlarge the space, the least value cannot rise). So if a ladder of
    searches S₁ ⊆ S₂ REPORTS a worse value on the larger space than some point
    of the smaller achieves, the report is PROVABLY not the optimum of S₂ —
    stagnation convicted from the process's own outputs plus one structural
    theorem, with no external reference consulted. This threads the SelfAudit
    needle exactly the way C3 did: the inclusion S₁ ⊆ S₂ is the
    theorem-pinned anchor (for MPS it is the fact that a χ-bounded manifold
    embeds in every larger one — warm-starting by padding REALIZES the
    inclusion as a concrete point), and the audit consumes chart reports plus
    that anchor, never the truth. Q8's measured face: E(χ) ran 8.6e-7 →
    1.49e-2 → 1.52e-2 → 7.4e-3 over χ = 32/64/128/256 at the plant — every
    later rung convicted by the first.

SCOPE. Order-theoretic model bricks: search spaces are sets, reports are real
values, the ansatz-nesting fact is a hypothesis here and a theorem of the
consuming method there. Nothing about MPS is proved in this file; what is
proved is why Q9's staked detector (non-monotone E(χ) ⇒ refuse) is a
refutation and not a heuristic. Kill, separable: exhibit a method whose search
spaces genuinely nest, whose reports are exact optima, and whose optima are
non-monotone — then `isLeast_mono_of_subset` does not model that method's
"search" and the detector's warrant collapses to heuristic there.
-/
import CIRISOntology.Core.Coordination
import Mathlib.Order.Bounds.Basic
import Mathlib.Tactic

namespace CIRISOntology.Core.Stagnation

/-! ### The blindness: motion does not factor to error -/

/-- The motion residual of an iteration at a point: how far one step moves it.
    Zero at every fixed point by definition of fixed point. -/
def motion (T : ℝ → ℝ) (x : ℝ) : ℝ := |T x - x|

theorem motion_eq_zero_of_fixed {T : ℝ → ℝ} {x : ℝ} (h : T x = x) :
    motion T x = 0 := by simp [motion, h]

/-- **THE BLINDNESS, in witness-pair form.** Two stagnant states present the
    identical motion reading (zero) and differ arbitrarily in error: the error
    separates a fiber of the motion view, so no rule computes error from
    motion. The identity map makes every point a fixed point, which is the
    honest cartoon of a sweep whose environment is built from its own state. -/
theorem error_separates_motion_fiber (target : ℝ) :
    SeparatesFiber (motion id) (fun x : ℝ => |x - target|) := by
  refine ⟨target, target + 1, ?_, ?_⟩
  · simp [motion]
  · simp

/-- The consequence, through the lake's spine: stagnation error is not
    computable from the motion ledger — the theorem Q8 measured at nine orders
    of magnitude. -/
theorem error_not_computable_from_motion (target : ℝ) :
    ¬ ∃ f : ℝ → ℝ, ∀ x : ℝ, |x - target| = f (motion id x) :=
  not_computable_from _ _ (error_separates_motion_fiber target)

/-! ### The detector: nested optima are monotone, so regressions convict -/

variable {α : Type*}

/-- **Enlarging the search space cannot raise the optimum.** One line of order
    theory, and the whole warrant of the χ-ladder anchor. -/
theorem isLeast_mono_of_subset {f : α → ℝ} {S₁ S₂ : Set α} (hsub : S₁ ⊆ S₂)
    {v₂ : ℝ} (h₂ : IsLeast (f '' S₂) v₂) {x : α} (hx : x ∈ S₁) :
    v₂ ≤ f x :=
  h₂.2 ⟨x, hsub hx, rfl⟩

/-- **THE DETECTOR.** If the larger search REPORTS a value worse than some
    point of the smaller search achieves, the report is not the optimum of the
    larger space — stagnation, convicted from reports plus the nesting anchor,
    no reference consulted. Q9's staked non-monotonicity refusal is this
    theorem's instance, with warm-start padding supplying the point `x`. -/
theorem not_optimal_of_regression {f : α → ℝ} {S₁ S₂ : Set α} (hsub : S₁ ⊆ S₂)
    {x : α} (hx : x ∈ S₁) {v₂ : ℝ} (hworse : f x < v₂) :
    ¬ IsLeast (f '' S₂) v₂ :=
  fun h₂ => absurd (isLeast_mono_of_subset hsub h₂ hx) (not_le.mpr hworse)

end CIRISOntology.Core.Stagnation
