/-
CIRISOntology.Core.Share — the whole-only share, defined on the state itself.

The stance's open claim (`third-in-tsvf`) asks for the whole-only share of a
multi-time state, defined on the object — the state over times — not on
readings of it. This file is the first half of that definition, mechanized:
the share for finite classical alphabets (the diagonal sector of the
three-slot process state), with the exhibited computation.

  * `IsProb` — a probability state: nonnegative, summing to one.
  * `marg₁₂`/`marg₁₃`/`marg₂₃`, `SamePairs` — the three two-slot marginals,
    and the relation "carries exactly the same pair data".
  * `pairEnvelope`, `share` — the pair-marginal envelope of a state (the
    entropies of all probability states with its two-slot marginals), and
    share(p) := sup(envelope) − entropy(p). Instrument-free: a variational
    functional of the state alone, no reading enters.
  * `entropy_le_log_card` — the Gibbs bound: entropy of any probability state
    is at most log of the alphabet size. The stone that makes the envelope
    bounded, hence the share well-defined. Proved from `log x ≤ x − 1`.
  * `share_nonneg` — the share is never negative on a probability state.
  * `share_parity` — THE EXHIBITED COMPUTATION: the parity state's share is
    exactly `log 2`. One bit. The same number that `third_sees_parity` reads
    on the whole and that one remembered bit realizes in `Core.Temporal` —
    by theorem, not analogy. The route: parity's pair marginals are uniform,
    so the constrained maximum-entropy problem is solved by the unconstrained
    maximizer, and the Gibbs bound closes it. This is why the known blocker
    ("pairwise-maxent projection needs machinery Mathlib does not carry")
    does not bind here: the exhibited state sits exactly where the projection
    is free.

The construction is connected information / max-entropy irreducible
correlation (Schneidman–Still–Berry–Bialek 2003; Zhou 2008 for the quantum
form on spatial states) — mathematics openly borrowed; the recognition is
putting it on the state-over-times, where the 2026-07-24 kill-check found it
absent. Pre-registered in `scratchpad/temporal-share/DEFINITION_PREREG.md`
before these proofs were attempted.

SCOPE. Proved here: the four items above, exact. NOT here, and said plainly:
the quantum lift (von Neumann entropy of the Choi object, marginals by
partial trace — same variational form, next brick), the vanishing of the
share on pairwise-determined states (needs grouping subadditivity of the
bespoke entropy; registered as the next obligation), and any claim about
which processes in nature carry a nonzero share.

Mathlib survey: `Real.log_le_sub_one_of_pos` carries the Gibbs bound;
`Real.log_inv`, `Real.log_mul`, `Real.log_pow` for bookkeeping;
`csSup` via `IsGreatest.csSup_eq` / `le_csSup`. No gaps to port.
-/
import CIRISOntology.Core.Third

namespace CIRISOntology.Core

open scoped BigOperators

/-- A probability state on a finite alphabet: nonnegative, summing to one. -/
def IsProb {α : Type*} [Fintype α] (p : α → ℝ) : Prop :=
  (∀ x, 0 ≤ p x) ∧ ∑ x, p x = 1

/-- The (1,2) two-slot marginal of a three-slot state. -/
noncomputable def marg₁₂ {α β γ : Type*} [Fintype γ]
    (p : α × β × γ → ℝ) : α × β → ℝ :=
  fun ab => ∑ c, p (ab.1, ab.2, c)

/-- The (1,3) two-slot marginal of a three-slot state. -/
noncomputable def marg₁₃ {α β γ : Type*} [Fintype β]
    (p : α × β × γ → ℝ) : α × γ → ℝ :=
  fun ac => ∑ b, p (ac.1, b, ac.2)

/-- The (2,3) two-slot marginal of a three-slot state. -/
noncomputable def marg₂₃ {α β γ : Type*} [Fintype α]
    (p : α × β × γ → ℝ) : β × γ → ℝ :=
  fun bc => ∑ a, p (a, bc.1, bc.2)

/-- `q` carries exactly the same two-slot data as `p`, at every pair of slots. -/
def SamePairs {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    (p q : α × β × γ → ℝ) : Prop :=
  marg₁₂ q = marg₁₂ p ∧ marg₁₃ q = marg₁₃ p ∧ marg₂₃ q = marg₂₃ p

/-- The pair-marginal envelope of a state: the entropies of ALL probability
    states carrying exactly its two-slot marginals. The whole-only share is
    how far the state's own entropy sits below the top of this set. -/
def pairEnvelope {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    (p : α × β × γ → ℝ) : Set ℝ :=
  { h | ∃ q, IsProb q ∧ SamePairs p q ∧ entropy q = h }

/-- THE WHOLE-ONLY SHARE, on the state itself: the entropy headroom the pair
    data leaves open, minus the entropy the state actually has. Zero when the
    pair data already determines the state's entropy; positive exactly when
    part of the state's order lives above every two-slot reading. -/
noncomputable def share {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    (p : α × β × γ → ℝ) : ℝ :=
  sSup (pairEnvelope p) - entropy p

/-! ### The Gibbs bound -/

private lemma sub_inv_le_mul_log {n t : ℝ} (hn : 0 < n) (ht : 0 ≤ t) :
    t - n⁻¹ ≤ t * Real.log (t * n) := by
  rcases ht.eq_or_lt with h | h
  · have h1 : 0 ≤ n⁻¹ := inv_nonneg.mpr hn.le
    rw [← h]
    simpa using by linarith
  · have htn : 0 < t * n := mul_pos h hn
    have h1 : Real.log (t * n)⁻¹ ≤ (t * n)⁻¹ - 1 :=
      Real.log_le_sub_one_of_pos (inv_pos.mpr htn)
    rw [Real.log_inv] at h1
    have h2 : 1 - (t * n)⁻¹ ≤ Real.log (t * n) := by linarith
    have h3 := mul_le_mul_of_nonneg_left h2 h.le
    have h4 : t * (1 - (t * n)⁻¹) = t - n⁻¹ := by
      field_simp
      ring
    linarith [h3, h4.symm.le, h4.le]

private lemma mul_log_mul {n t : ℝ} (hn : 0 < n) (ht : 0 ≤ t) :
    t * Real.log (t * n) = t * Real.log t + t * Real.log n := by
  rcases ht.eq_or_lt with h | h
  · rw [← h]; ring
  · rw [Real.log_mul h.ne' hn.ne']; ring

/-- THE GIBBS BOUND: the entropy of a probability state on a finite alphabet
    is at most the log of the alphabet size. This is what makes the pair
    envelope bounded — the share well-defined — and, on states whose pair
    marginals are uniform, it closes the maximum-entropy problem outright.
    Proved from `log x ≤ x − 1`; no entropy-maximization machinery needed. -/
theorem entropy_le_log_card {α : Type*} [Fintype α] [Nonempty α] {p : α → ℝ}
    (h0 : ∀ x, 0 ≤ p x) (h1 : ∑ x, p x = 1) :
    entropy p ≤ Real.log (Fintype.card α) := by
  have hcard : 0 < Fintype.card α := Fintype.card_pos
  set n : ℝ := (Fintype.card α : ℝ) with hn_def
  have hn : 0 < n := by rw [hn_def]; exact_mod_cast hcard
  have hsum : ∑ _x : α, n⁻¹ = 1 := by
    rw [Finset.sum_const, nsmul_eq_mul, Finset.card_univ]
    field_simp
  have key : (0 : ℝ) ≤ ∑ x, p x * Real.log (p x * n) := by
    have h2 : ∑ x, (p x - n⁻¹) ≤ ∑ x, p x * Real.log (p x * n) :=
      Finset.sum_le_sum fun x _ => sub_inv_le_mul_log hn (h0 x)
    have h3 : ∑ x, (p x - n⁻¹) = 0 := by
      rw [Finset.sum_sub_distrib, h1, hsum, sub_self]
    linarith
  have expand : ∑ x, p x * Real.log (p x * n)
      = (∑ x, p x * Real.log (p x)) + Real.log n := by
    rw [Finset.sum_congr rfl fun x _ => mul_log_mul hn (h0 x),
        Finset.sum_add_distrib, ← Finset.sum_mul, h1, one_mul]
  unfold entropy
  linarith [key, expand]

/-! ### Well-definedness and nonnegativity -/

/-- The envelope is bounded above — the supremum in `share` is honest. -/
theorem pairEnvelope_bddAbove {α β γ : Type*}
    [Fintype α] [Fintype β] [Fintype γ] [Nonempty α] [Nonempty β] [Nonempty γ]
    (p : α × β × γ → ℝ) : BddAbove (pairEnvelope p) := by
  refine ⟨Real.log (Fintype.card (α × β × γ)), ?_⟩
  rintro h ⟨q, hq, -, rfl⟩
  exact entropy_le_log_card hq.1 hq.2

/-- The state's own entropy sits in its envelope, so the share is never
    negative on a probability state. -/
theorem share_nonneg {α β γ : Type*}
    [Fintype α] [Fintype β] [Fintype γ] [Nonempty α] [Nonempty β] [Nonempty γ]
    {p : α × β × γ → ℝ} (hp : IsProb p) : 0 ≤ share p := by
  have hmem : entropy p ∈ pairEnvelope p := ⟨p, hp, ⟨rfl, rfl, rfl⟩, rfl⟩
  have := le_csSup (pairEnvelope_bddAbove p) hmem
  unfold share
  linarith

/-! ### The exhibited computation: the parity state's share is one bit -/

private lemma log_quarter' : Real.log ((1:ℝ)/4) = -(2 * Real.log 2) := by
  rw [one_div, show (4:ℝ) = 2 ^ 2 by norm_num, Real.log_inv, Real.log_pow]
  norm_num

private lemma log_eighth' : Real.log ((1:ℝ)/8) = -(3 * Real.log 2) := by
  rw [one_div, show (8:ℝ) = 2 ^ 3 by norm_num, Real.log_inv, Real.log_pow]
  norm_num

private lemma entropy_parity' : entropy parity = 2 * Real.log 2 := by
  unfold entropy parity
  simp only [Fintype.sum_prod_type, Fintype.sum_bool]
  norm_num [log_quarter']
  ring

private lemma entropy_indep' : entropy indep = 3 * Real.log 2 := by
  unfold entropy indep
  simp only [Fintype.sum_prod_type, Fintype.sum_bool]
  norm_num [log_eighth']
  ring

private lemma indep_isProb : IsProb indep := by
  constructor
  · intro x; unfold indep; norm_num
  · unfold indep
    simp only [Fintype.sum_prod_type, Fintype.sum_bool]
    norm_num

/-- The independent state carries exactly the parity state's pair data: both
    read `1/4` on every two-slot cell. The parity state's pair marginals are
    those of NO pattern at all — that is `parity_pair_independent_*`, reused. -/
private lemma indep_samePairs : SamePairs parity indep := by
  refine ⟨?_, ?_, ?_⟩
  · funext ab
    have h := parity_pair_independent_12 ab.1 ab.2
    unfold marg₁₂ indep
    simp only [Fintype.sum_bool] at h ⊢
    norm_num
    linarith [h]
  · funext ac
    have h := parity_pair_independent_13 ac.1 ac.2
    unfold marg₁₃ indep
    simp only [Fintype.sum_bool] at h ⊢
    norm_num
    linarith [h]
  · funext bc
    have h := parity_pair_independent_23 bc.1 bc.2
    unfold marg₂₃ indep
    simp only [Fintype.sum_bool] at h ⊢
    norm_num
    linarith [h]

private lemma log_card_eight :
    Real.log (Fintype.card (Bool × Bool × Bool)) = 3 * Real.log 2 := by
  have : (Fintype.card (Bool × Bool × Bool) : ℝ) = 8 := by
    simp [Fintype.card_prod]
  rw [this, show (8:ℝ) = 2 ^ 3 by norm_num, Real.log_pow]
  norm_num

/-- The top of the parity state's envelope is exactly `3 log 2`: the
    independent state attains it, and the Gibbs bound forbids more. -/
private lemma parity_envelope_sSup :
    sSup (pairEnvelope parity) = 3 * Real.log 2 := by
  refine IsGreatest.csSup_eq ⟨⟨indep, indep_isProb, indep_samePairs, entropy_indep'⟩, ?_⟩
  rintro h ⟨q, hq, -, rfl⟩
  calc entropy q ≤ Real.log (Fintype.card (Bool × Bool × Bool)) :=
        entropy_le_log_card hq.1 hq.2
    _ = 3 * Real.log 2 := log_card_eight

/-- THE SHARE OF THE PARITY STATE IS EXACTLY ONE BIT. Defined on the state
    itself — no instrument, no reading — the parity pattern's whole-only
    share is `log 2`: the same number the whole-reading sees
    (`third_sees_parity`) and the same single bit whose memory realizes the
    pattern across time (`memory_realizes_parity`). One number, by theorem. -/
theorem share_parity : share parity = Real.log 2 := by
  unfold share
  rw [parity_envelope_sSup, entropy_parity']
  ring

/-- The share it computes is strictly positive: the parity state carries
    whole-only order, as a property of the state alone. -/
theorem share_parity_positive : 0 < share parity := by
  rw [share_parity]
  exact Real.log_pos (by norm_num)

end CIRISOntology.Core
