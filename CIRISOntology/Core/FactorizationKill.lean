/-
CIRISOntology.Core.FactorizationKill — a direct kill for intrinsic whole-only state.

The founding parity witness is whole-only RELATIVE TO THE DECLARED PARTIAL VIEWS:
in coordinates (a,b,c), c=a xor b is invisible to every pair marginal and
`S_total parity = log 2`.

This file asks the harder question: is that whole-only content invariant under an
invertible refactorization of THE SAME eight-point state space?

No.  Use the bijective coordinate change

  (a,b,c) <-> (a,b,r),       r = c xor (a xor b).

It is its own inverse.  In the new coordinates the parity state is simply two fair
independent bits plus the fixed local coordinate r=false.  The joint distribution
therefore factors completely and its total dependence is zero.

So the machine-checked conclusion is deliberately sharp:

  whole-only-ness is not intrinsic under unrestricted invertible refactorization.

This does NOT refute `Core.NonFactoring`: that theorem is explicitly relative to a
chosen view family, and remains correct.  It refutes only the stronger move from
"fails to factor through THESE views" to "is ontically whole-only" unless the theory
also supplies a privileged admissible factorization/locality structure.  For the
runtime this matters because `Holon::whole` is stored on the holon itself, while
multiple charts/decompositions may declare different partial views.

KILL / REPAIR FOR THE MAXIMAL HOLON CLAIM:
* KILL if arbitrary invertible refactorizations are physically admissible while
  whole-only state is claimed to be an intrinsic property of a holon.
* REPAIR only by deriving/restricting an admissible factorization class (for example
  from locality, causal structure, interaction algebra, or an equivalent physical
  invariant), or by making whole-only state explicitly frame/factorization-relative.
-/
import CIRISOntology.Core.NonFactoring

namespace CIRISOntology.Core

/-- The parity-adapted chart.  The third coordinate records the residual from the
    parity constraint. -/
def parityChart (t : Bool × Bool × Bool) : Bool × Bool × Bool :=
  (t.1, t.2.1, Bool.xor t.2.2 (Bool.xor t.1 t.2.1))

/-- The chart is an involution, hence a bijective reparameterization of exactly the
    same finite state space. -/
theorem parityChart_involutive : Function.Involutive parityChart := by
  intro t
  rcases t with ⟨a, b, c⟩
  cases a <;> cases b <;> cases c <;> rfl

/-- Re-express a distribution in the parity-adapted chart.  Since `parityChart` is
    self-inverse, pullback and pushforward have the same pointwise formula here. -/
noncomputable def reframeDist (p : Bool × Bool × Bool → ℝ) : Bool × Bool × Bool → ℝ :=
  fun t => p (parityChart t)

/-- The founding parity state, expressed in the parity-adapted chart. -/
noncomputable def parityReframed : Bool × Bool × Bool → ℝ := reframeDist parity

/-- In the adapted chart the formerly whole-only parity relation is a LOCAL fixed
    coordinate: r=false with probability one. -/
theorem parityReframed_formula :
    parityReframed = fun t => if t.2.2 = false then (1 : ℝ) / 4 else 0 := by
  funext t
  rcases t with ⟨a, b, c⟩
  cases a <;> cases b <;> cases c <;>
    simp [parityReframed, reframeDist, parityChart, parity] <;> norm_num

/-- Stronger than a marginal statement: the reframed joint distribution factors as
    fair(a) * fair(b) * delta_false(r). -/
theorem parityReframed_factors (a b r : Bool) :
    parityReframed (a, b, r) =
      ((1 : ℝ) / 2) * ((1 : ℝ) / 2) * (if r = false then 1 else 0) := by
  cases a <;> cases b <;> cases r <;>
    simp [parityReframed, reframeDist, parityChart, parity] <;> norm_num

private lemma fk_log_half : Real.log ((1 : ℝ) / 2) = -Real.log 2 := by
  rw [one_div, Real.log_inv]

private lemma fk_log_quarter : Real.log ((1 : ℝ) / 4) = -(2 * Real.log 2) := by
  rw [one_div, show (4 : ℝ) = 2 ^ 2 by norm_num, Real.log_inv, Real.log_pow]
  norm_num

private lemma fk_entropy_uniform_bool :
    entropy (fun _ : Bool => (1 : ℝ) / 2) = Real.log 2 := by
  unfold entropy
  rw [Fintype.sum_bool, fk_log_half]
  ring

private lemma fk_entropy_delta_false :
    entropy (fun r : Bool => if r = false then (1 : ℝ) else 0) = 0 := by
  unfold entropy
  rw [Fintype.sum_bool]
  norm_num

private lemma fk_entropy_reframed : entropy parityReframed = 2 * Real.log 2 := by
  unfold entropy parityReframed reframeDist parityChart parity
  simp only [Fintype.sum_prod_type, Fintype.sum_bool]
  norm_num [fk_log_quarter]
  ring

private lemma fk_marg₁ :
    (fun a => ∑ b, ∑ r, parityReframed (a, b, r)) =
      fun _ : Bool => (1 : ℝ) / 2 := by
  funext a
  cases a <;>
    simp [parityReframed, reframeDist, parityChart, parity, Fintype.sum_bool] <;>
    norm_num

private lemma fk_marg₂ :
    (fun b => ∑ a, ∑ r, parityReframed (a, b, r)) =
      fun _ : Bool => (1 : ℝ) / 2 := by
  funext b
  cases b <;>
    simp [parityReframed, reframeDist, parityChart, parity, Fintype.sum_bool] <;>
    norm_num

private lemma fk_marg₃ :
    (fun r => ∑ a, ∑ b, parityReframed (a, b, r)) =
      fun r : Bool => if r = false then (1 : ℝ) else 0 := by
  funext r
  cases r <;>
    simp [parityReframed, reframeDist, parityChart, parity, Fintype.sum_bool] <;>
    norm_num

/-- The same probability state has ZERO total dependence in the adapted factorization.
    Compare `third_sees_parity : S_total parity = log 2`. -/
theorem reframed_parity_total_zero : S_total parityReframed = 0 := by
  unfold S_total
  rw [fk_marg₁, fk_marg₂, fk_marg₃, fk_entropy_uniform_bool,
      fk_entropy_uniform_bool, fk_entropy_delta_false, fk_entropy_reframed]
  ring

/-- **THE KILL, packaged.** An invertible coordinate change on the same finite state
    space changes the founding state's total dependence from one full bit (`log 2`)
    to zero.  Therefore the non-factoring/whole-only designation is not invariant
    under unrestricted refactorization. -/
theorem whole_only_not_invariant_under_invertible_refactorization :
    Function.Involutive parityChart ∧
    S_total parity = Real.log 2 ∧
    S_total parityReframed = 0 := by
  exact ⟨parityChart_involutive, third_sees_parity, reframed_parity_total_zero⟩

/-- Machine-readable reach fence: the theorem kills INTRINSIC whole-only-ness under
    unrestricted factorization, not the relative `NonFactoring view q` theorem. -/
structure FactorizationKillReach where
  invertible_same_state_space : True
  original_nonfactoring_result_preserved : True
  whole_only_not_factorization_invariant : True
  privileged_factorization_or_relative_whole_is_owed : True

/-- The reach is recorded. -/
def factorization_kill_reach : FactorizationKillReach :=
  ⟨trivial, trivial, trivial, trivial⟩

end CIRISOntology.Core
