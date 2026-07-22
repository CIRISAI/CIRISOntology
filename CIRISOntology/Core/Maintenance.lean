/-
CIRISOntology.Core.Maintenance — the rent clause, proved on the standard model.

The measured ledger law says shared pattern is never free to hold: an entry not
maintained decays, and holding one costs continuous upkeep. That is a claim
about the world, and it enters the stance as `measured`, on the predecessor
record.

THIS FILE PROVES THE MODEL, AND ONLY THE MODEL. Take the standard picture of a
rented entry: each step a fixed fraction `γ` of the amount decays away, and a
payment `α` is added back. Two facts follow, and they are the whole content of
the rent clause:

  * `rent_holds` — paying exactly what decay takes (`α = γ·S`) leaves the amount
    unchanged. Rent is the payment that buys standing still.

  * `unpaid_decays` — with no payment at all, the amount tends to zero. Not
    merely smaller: all the way down, given enough steps.

SCOPE. A theorem about a model says nothing about the world until something
connects them, and that connection is a separate, measured claim with its own
way of failing (`epistemology.md` §1). Nothing here asserts that any real
system obeys this model; the stance states that separately and at a lower
strength.
-/
import Mathlib.Analysis.SpecificLimits.Basic

namespace CIRISOntology.Core

open Filter Topology

/-- One step of a rented entry: decay removes the fraction `γ` of the current
    amount, and the payment `α` is added back. -/
def step (γ α S : ℝ) : ℝ := S - γ * S + α

/-- An entry left unpaid for `n` steps: only decay acts. -/
def unpaid (S₀ γ : ℝ) (n : ℕ) : ℝ := S₀ * (1 - γ) ^ n

/-- An entry paid its rent at every step: each step the payment is recomputed
    from the CURRENT amount, which is what "paying the rent" actually requires. -/
def paid (S₀ γ : ℝ) : ℕ → ℝ
  | 0     => S₀
  | n + 1 => step γ (γ * paid S₀ γ n) (paid S₀ γ n)

/-- THE RENT CLAUSE. Paying exactly what decay takes holds the entry exactly
    steady — no more and no less. Standing still is the thing the payment
    buys. -/
theorem rent_holds (γ S : ℝ) : step γ (γ * S) S = S := by
  unfold step
  ring

/-- THE RENT CLAUSE, FOR EVER. Paying the rent at every step holds the entry at
    exactly its starting amount, for any number of steps. "Steady forever" is
    this theorem, not a hand-wave from the one-step case. -/
theorem paid_const (S₀ γ : ℝ) (n : ℕ) : paid S₀ γ n = S₀ := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [paid, ih, rent_holds]

/-- Underpaying strictly loses ground: any payment short of what decay takes
    leaves the entry smaller than it was. This is a ONE-STEP statement, and the
    stance says only what it says. -/
theorem underpaid_shrinks {γ α S : ℝ} (h : α < γ * S) : step γ α S < S := by
  unfold step
  linarith

/-- `unpaid` is the iterate of the unpaid step: with `α = 0`, `n+1` steps is
    one step applied to `n` steps. This is what makes the decay statement below
    a statement about the same model. -/
theorem unpaid_succ (S₀ γ : ℝ) (n : ℕ) :
    unpaid S₀ γ (n + 1) = step γ 0 (unpaid S₀ γ n) := by
  unfold unpaid step
  ring

/-- NO UPKEEP, NO ENTRY. An unmaintained entry does not merely shrink; it tends
    to zero. Any decay fraction at all, however small, is enough. -/
theorem unpaid_decays {S₀ γ : ℝ} (hγ : 0 < γ) (hγ1 : γ ≤ 1) :
    Tendsto (unpaid S₀ γ) atTop (𝓝 0) := by
  have h₁ : (0:ℝ) ≤ 1 - γ := by linarith
  have h₂ : (1:ℝ) - γ < 1 := by linarith
  simpa [unpaid] using (tendsto_pow_atTop_nhds_zero_of_lt_one h₁ h₂).const_mul S₀

end CIRISOntology.Core
