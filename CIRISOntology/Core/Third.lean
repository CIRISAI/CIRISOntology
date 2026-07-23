/-
CIRISOntology.Core.Third — the ruler, upgraded: a third-aware instrument, and
the exhibited state that separates it from the pairwise one.

The pairwise instrument's blindness (`Core.Coordination`) is not a fate. This
file carries the upgrade and the witness, both machine-checked:

  * `S_total` — total dependence (multi-information): the sum of the parts'
    entropies minus the joint entropy. It reads coordination at ALL orders.

  * `parity` — the simplest hidden state: three fair bits, the third the XOR
    of the first two. Any two of them are exactly independent; the three
    together are locked.

  * `pairwise_blind_to_parity` — the correlation matrix of the parity state
    is the identity, so `S_pairwise` reads exactly its floor, 0.

  * `third_sees_parity` — `S_total` reads exactly `log 2` on the same state,
    and `third_reading_positive` that this is strictly positive.

Together these discharge, inside this repository, the counterexample that the
stance's first claim stakes its kill on: a state with vanishing pairwise
structure and non-vanishing total dependence EXISTS, and the upgraded
instrument sees it.

SCOPE. This is the kernel of the upgrade, not its field deployment. The
bias-corrected, null-controlled synergy detector run against real data lives
in the predecessor record (github.com/CIRISAI/coherence-ratchet); its results
enter the stance as `measured`, never as `proved`.
-/
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.FinCases
import CIRISOntology.Core.Coordination

namespace CIRISOntology.Core

open scoped BigOperators

/-- Shannon entropy (natural log) of a finitely-supported distribution.
    Mathlib's convention `Real.log 0 = 0` makes empty outcomes contribute
    nothing, as they should. -/
noncomputable def entropy {α : Type*} [Fintype α] (p : α → ℝ) : ℝ :=
  -∑ a, p a * Real.log (p a)

/-- Total dependence (multi-information) of a joint state of three variables:
    what the parts' entropies say minus what the joint entropy says. This is
    the all-orders quantity of which `S_pairwise` reads only the second-order
    part. -/
noncomputable def S_total {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    (p : α × β × γ → ℝ) : ℝ :=
  entropy (fun a => ∑ b, ∑ c, p (a, b, c))
    + entropy (fun b => ∑ a, ∑ c, p (a, b, c))
    + entropy (fun c => ∑ a, ∑ b, p (a, b, c))
    - entropy p

/-- The parity state: three fair bits, the third the XOR of the first two.
    Each pair is exactly independent; the triple is fully locked. -/
noncomputable def parity : Bool × Bool × Bool → ℝ :=
  fun t => if t.2.2 = Bool.xor t.1 t.2.1 then 1/4 else 0

/-- ±1 encoding of a bit, so that correlations are plain expectations. -/
noncomputable def pm (b : Bool) : ℝ := if b then 1 else -1

/-- The three coordinates of the parity state as ±1 variables. -/
noncomputable def parityVar : Fin 3 → Bool × Bool × Bool → ℝ
  | 0 => fun t => pm t.1
  | 1 => fun t => pm t.2.1
  | 2 => fun t => pm t.2.2

/-- The correlation matrix of ANY state on three bits, read through the ±1
    coordinates. Means are zero and variances one on the states used here, so
    the raw second moments are the correlations. -/
noncomputable def corrOf (p : Bool × Bool × Bool → ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  Matrix.of fun i j => ∑ t, p t * (parityVar i t * parityVar j t)

/-- The correlation matrix of the parity state. -/
noncomputable def parityCorr : Matrix (Fin 3) (Fin 3) ℝ := corrOf parity

/-- The independent state: three fair bits with no rule tying them at all.
    It is the honest comparison for `parity` — same correlation matrix, no
    shared pattern whatsoever. -/
noncomputable def indep : Bool × Bool × Bool → ℝ := fun _ => 1/8

private lemma log_half : Real.log ((1:ℝ)/2) = -Real.log 2 := by
  rw [one_div, Real.log_inv]

private lemma log_quarter : Real.log ((1:ℝ)/4) = -(2 * Real.log 2) := by
  rw [one_div, show (4:ℝ) = 2 ^ 2 by norm_num, Real.log_inv, Real.log_pow]
  norm_num

private lemma entropy_uniform_bool :
    entropy (fun _ : Bool => (1:ℝ)/2) = Real.log 2 := by
  unfold entropy
  rw [Fintype.sum_bool, log_half]
  ring

private lemma entropy_parity : entropy parity = 2 * Real.log 2 := by
  unfold entropy parity
  simp only [Fintype.sum_prod_type, Fintype.sum_bool]
  norm_num [log_quarter]
  ring

private lemma parity_marg₁ :
    (fun a => ∑ b, ∑ c, parity (a, b, c)) = fun _ : Bool => (1:ℝ)/2 := by
  funext a
  cases a <;> simp [parity, Fintype.sum_bool] <;> norm_num

private lemma parity_marg₂ :
    (fun b => ∑ a, ∑ c, parity (a, b, c)) = fun _ : Bool => (1:ℝ)/2 := by
  funext b
  cases b <;> simp [parity, Fintype.sum_bool] <;> norm_num

private lemma parity_marg₃ :
    (fun c => ∑ a, ∑ b, parity (a, b, c)) = fun _ : Bool => (1:ℝ)/2 := by
  funext c
  cases c <;> simp [parity, Fintype.sum_bool] <;> norm_num

/-- The correlation matrix of the parity state is the identity: every pair of
    its variables is exactly uncorrelated. -/
theorem parity_corr_eq_one : parityCorr = (1 : Matrix (Fin 3) (Fin 3) ℝ) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [parityCorr, corrOf, parityVar, parity, pm, Matrix.one_apply,
          Fintype.sum_prod_type, Fintype.sum_bool] <;>
    norm_num

/-- PAIRS ARE INDEPENDENT, NOT MERELY UNCORRELATED. For every pair of the three
    coordinates, the two-variable distribution factors into the product of its
    marginals — the strongest form of "these two tell you nothing about each
    other". The published text says independence, so independence is what must
    be proved; uncorrelatedness alone would not license the sentence. -/
theorem parity_pair_independent_12 (a b : Bool) :
    (∑ c, parity (a, b, c)) = (1/2) * (1/2) := by
  cases a <;> cases b <;> simp [parity, Fintype.sum_bool] <;> norm_num

theorem parity_pair_independent_13 (a c : Bool) :
    (∑ b, parity (a, b, c)) = (1/2) * (1/2) := by
  cases a <;> cases c <;> simp [parity, Fintype.sum_bool] <;> norm_num

theorem parity_pair_independent_23 (b c : Bool) :
    (∑ a, parity (a, b, c)) = (1/2) * (1/2) := by
  cases b <;> cases c <;> simp [parity, Fintype.sum_bool] <;> norm_num

/-- The independent state presents the SAME correlation matrix as the parity
    state: the identity. The two states are indistinguishable to any reading of
    the correlation matrix. -/
theorem indep_corr_eq_one : corrOf indep = (1 : Matrix (Fin 3) (Fin 3) ℝ) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [corrOf, indep, parityVar, pm, Matrix.one_apply,
          Fintype.sum_prod_type, Fintype.sum_bool] <;>
    norm_num

/-- THE BLINDNESS, EXHIBITED. On the parity state the pairwise instrument
    reads exactly its floor. Nothing is missing from the reading that pairs
    could have shown; everything is missing that only the triple carries. -/
theorem pairwise_blind_to_parity : S_pairwise parityCorr = 0 := by
  rw [parity_corr_eq_one]
  exact S_pairwise_identity

/-- THE UPGRADE, EXHIBITED. On the same state the third-aware instrument
    reads exactly `log 2`: one full bit of coordination, all of it above
    second order. -/
theorem third_sees_parity : S_total parity = Real.log 2 := by
  unfold S_total
  rw [parity_marg₁, parity_marg₂, parity_marg₃, entropy_uniform_bool,
      entropy_parity]
  ring

/-- The third-aware reading on the parity state is strictly positive: the
    two instruments provably disagree, and the disagreement is the Third. -/
theorem third_reading_positive : 0 < S_total parity := by
  rw [third_sees_parity]
  exact Real.log_pos (by norm_num)

private lemma log_eighth : Real.log ((1:ℝ)/8) = -(3 * Real.log 2) := by
  rw [one_div, show (8:ℝ) = 2 ^ 3 by norm_num, Real.log_inv, Real.log_pow]
  ring

private lemma entropy_indep : entropy indep = 3 * Real.log 2 := by
  unfold entropy indep
  simp only [Fintype.sum_prod_type, Fintype.sum_bool]
  norm_num [log_eighth]
  ring

private lemma indep_marg₁ :
    (fun a => ∑ b, ∑ c, indep (a, b, c)) = fun _ : Bool => (1:ℝ)/2 := by
  funext a; simp [indep, Fintype.sum_bool]; norm_num

private lemma indep_marg₂ :
    (fun b => ∑ a, ∑ c, indep (a, b, c)) = fun _ : Bool => (1:ℝ)/2 := by
  funext b; simp [indep, Fintype.sum_bool]; norm_num

private lemma indep_marg₃ :
    (fun c => ∑ a, ∑ b, indep (a, b, c)) = fun _ : Bool => (1:ℝ)/2 := by
  funext c; simp [indep, Fintype.sum_bool]; norm_num

/-- The independent state carries no shared pattern at all: its total
    dependence is exactly zero. -/
theorem S_total_indep : S_total indep = 0 := by
  unfold S_total
  rw [indep_marg₁, indep_marg₂, indep_marg₃, entropy_uniform_bool, entropy_indep]
  ring

/-- THE SEPARATING WITNESS, CONSTRUCTED. The parity state and the independent
    state present the SAME correlation matrix and differ in total dependence.
    So total dependence separates a fiber of the correlation map. -/
theorem corr_separates_total :
    SeparatesFiber corrOf S_total := by
  refine ⟨parity, indep, ?_, ?_⟩
  · rw [show corrOf parity = parityCorr from rfl, parity_corr_eq_one, indep_corr_eq_one]
  · rw [third_sees_parity, S_total_indep]
    exact ne_of_gt (Real.log_pos (by norm_num))

/-- THE STEP THAT WAS PREVIOUSLY MADE IN ENGLISH, NOW MADE IN LEAN. Total
    dependence is not a function of the correlation matrix: there is no rule
    whatever — however clever, however nonlinear — that takes the pairwise
    correlation matrix as its input and returns the total dependence.

    This is the composition the stance's `pair-blindness` claim rests on. It was
    previously argued in prose from two separate theorems; an audit caught that,
    and this closes it. -/
theorem total_not_computable_from_corr :
    ¬ ∃ g : Matrix (Fin 3) (Fin 3) ℝ → ℝ, ∀ p, S_total p = g (corrOf p) :=
  not_computable_from corrOf S_total corr_separates_total

/-! ## The books read the same in any language: relabeling-invariance of `S_total`

A first price of "true books": the total-dependence reading is a fact about the
JOINT STATE, not about the names we give a coordinate's values. Renaming the
outcomes of one variable by any bijection leaves `S_total` exactly unchanged. -/

/-- Entropy is invariant under a bijective reindexing of the outcome set: renaming
    the values carries no information, so `−∑ p log p` is unmoved. The engine of
    relabeling-invariance, by reindexing the defining sum along the bijection. -/
private lemma entropy_comp_equiv {X : Type*} [Fintype X] (σ : X ≃ X) (p : X → ℝ) :
    entropy (fun x => p (σ x)) = entropy p := by
  unfold entropy
  rw [neg_inj]
  exact Equiv.sum_comp σ (fun y => p y * Real.log (p y))

/-- RELABELING-INVARIANCE. For any bijection `e` on the first coordinate's values,
    the total dependence of the relabeled state equals that of the original:
    `S_total (p ∘ relabel₁ e) = S_total p`. The first-coordinate marginal's entropy
    is invariant because entropy is (its outcomes are just renamed); the other two
    marginals and the joint entropy are literally unchanged after reindexing the
    summed-over first coordinate. So the instrument reads the partition, never the
    labels — the property any honest ledger of shared pattern must have. Stated for
    the first coordinate; the other two follow by the same argument. -/
theorem S_total_relabel_fst {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    (e : α ≃ α) (p : α × β × γ → ℝ) :
    S_total (fun x => p (e x.1, x.2.1, x.2.2)) = S_total p := by
  have hA : entropy (fun a => ∑ b, ∑ c, p (e a, b, c))
          = entropy (fun a => ∑ b, ∑ c, p (a, b, c)) :=
    entropy_comp_equiv e (fun a => ∑ b, ∑ c, p (a, b, c))
  have hB : (fun b => ∑ a, ∑ c, p (e a, b, c)) = (fun b => ∑ a, ∑ c, p (a, b, c)) := by
    funext b; exact Equiv.sum_comp e (fun a => ∑ c, p (a, b, c))
  have hC : (fun c => ∑ a, ∑ b, p (e a, b, c)) = (fun c => ∑ a, ∑ b, p (a, b, c)) := by
    funext c; exact Equiv.sum_comp e (fun a => ∑ b, p (a, b, c))
  have hD : entropy (fun x : α × β × γ => p (e x.1, x.2.1, x.2.2)) = entropy p :=
    entropy_comp_equiv (e.prodCongr (Equiv.refl (β × γ))) p
  show entropy (fun a => ∑ b, ∑ c, p (e a, b, c))
        + entropy (fun b => ∑ a, ∑ c, p (e a, b, c))
        + entropy (fun c => ∑ a, ∑ b, p (e a, b, c))
        - entropy (fun x : α × β × γ => p (e x.1, x.2.1, x.2.2))
      = entropy (fun a => ∑ b, ∑ c, p (a, b, c))
        + entropy (fun b => ∑ a, ∑ c, p (a, b, c))
        + entropy (fun c => ∑ a, ∑ b, p (a, b, c))
        - entropy p
  rw [hA, hB, hC, hD]

end CIRISOntology.Core
