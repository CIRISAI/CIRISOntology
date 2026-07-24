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
  * `entropy_grouping` — grouping subadditivity: a state's entropy is at most
    that of its (1,2) marginal plus that of its third marginal. Gibbs against
    the product of the state's OWN marginals; absolute continuity is
    automatic, because a state is dominated by its own marginals.
  * `share_copied` / `S_total_copied` — THE DISCRIMINATOR: on two copied bits
    and a free third, the share is exactly zero while multi-information reads
    `log 2`. With `share_parity_positive`, the two quantities are separated
    in both directions: the share is the part of the order living above every
    pair, and only that part.

The construction is connected information / max-entropy irreducible
correlation (Schneidman–Still–Berry–Bialek 2003; Zhou 2008 for the quantum
form on spatial states) — mathematics openly borrowed; the recognition is
putting it on the state-over-times, where the 2026-07-24 kill-check found it
absent. Pre-registered in `scratchpad/temporal-share/DEFINITION_PREREG.md`
before these proofs were attempted; the discriminator was pre-registered
outcome 4 and came out as staked.

SCOPE. Proved here: the items above, exact. NOT here, and said plainly: the
quantum lift (von Neumann entropy of the Choi object, marginals by partial
trace — same variational form, next brick), and any claim about which
processes in nature carry a nonzero share.

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

/-- The third single-slot marginal of a three-slot state. -/
noncomputable def marg₃ {α β γ : Type*} [Fintype α] [Fintype β]
    (p : α × β × γ → ℝ) : γ → ℝ :=
  fun c => ∑ a, ∑ b, p (a, b, c)

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

/-! ### Grouping subadditivity, and the discriminator

The share must vanish where the pair data already spends all the order —
otherwise it does not isolate whole-only content and is the wrong
definition (pre-registered outcome 4). The stone is grouping subadditivity
of the entropy, by Gibbs against the product of the state's own marginals;
absolute continuity is automatic, because a state is dominated by its own
marginals. -/

private lemma mul_log_sub_le {q r : ℝ} (hq : 0 ≤ q) (hr : 0 ≤ r) (h : 0 < q → 0 < r) :
    q * Real.log r - q * Real.log q ≤ r - q := by
  rcases hq.eq_or_lt with h0 | h0
  · rw [← h0]; simpa using hr
  · have hrpos := h h0
    have h1 : Real.log (r / q) ≤ r / q - 1 :=
      Real.log_le_sub_one_of_pos (div_pos hrpos h0)
    rw [Real.log_div hrpos.ne' h0.ne'] at h1
    have h2 := mul_le_mul_of_nonneg_left h1 h0.le
    have h3 : q * (r / q - 1) = r - q := by field_simp
    calc q * Real.log r - q * Real.log q = q * (Real.log r - Real.log q) := by ring
      _ ≤ q * (r / q - 1) := h2
      _ = r - q := h3

private lemma marg₁₂_nonneg {α β γ : Type*} [Fintype γ] {q : α × β × γ → ℝ}
    (h0 : ∀ t, 0 ≤ q t) (ab : α × β) : 0 ≤ marg₁₂ q ab :=
  Finset.sum_nonneg fun c _ => h0 (ab.1, ab.2, c)

private lemma marg₃_nonneg {α β γ : Type*} [Fintype α] [Fintype β] {q : α × β × γ → ℝ}
    (h0 : ∀ t, 0 ≤ q t) (c : γ) : 0 ≤ marg₃ q c :=
  Finset.sum_nonneg fun a _ => Finset.sum_nonneg fun b _ => h0 (a, b, c)

private lemma le_marg₁₂ {α β γ : Type*} [Fintype γ] {q : α × β × γ → ℝ}
    (h0 : ∀ t, 0 ≤ q t) (a : α) (b : β) (c : γ) :
    q (a, b, c) ≤ marg₁₂ q (a, b) :=
  Finset.single_le_sum (fun c' _ => h0 (a, b, c')) (Finset.mem_univ c)

private lemma le_marg₃ {α β γ : Type*} [Fintype α] [Fintype β] {q : α × β × γ → ℝ}
    (h0 : ∀ t, 0 ≤ q t) (a : α) (b : β) (c : γ) :
    q (a, b, c) ≤ marg₃ q c :=
  calc q (a, b, c) ≤ ∑ b', q (a, b', c) :=
        Finset.single_le_sum (fun b' _ => h0 (a, b', c)) (Finset.mem_univ b)
    _ ≤ ∑ a', ∑ b', q (a', b', c) :=
        Finset.single_le_sum (fun a' _ => Finset.sum_nonneg fun b' _ => h0 (a', b', c))
          (Finset.mem_univ a)

private lemma sum_marg₁₂ {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    (q : α × β × γ → ℝ) : ∑ ab, marg₁₂ q ab = ∑ t, q t := by
  simp only [marg₁₂, Fintype.sum_prod_type]

private lemma sum_marg₃ {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    (q : α × β × γ → ℝ) : ∑ c, marg₃ q c = ∑ t, q t := by
  simp only [marg₃, Fintype.sum_prod_type]
  rw [Finset.sum_comm]
  exact Finset.sum_congr rfl fun a _ => Finset.sum_comm

/-- GROUPING SUBADDITIVITY: a state's entropy is at most the entropy of its
    (1,2) marginal plus that of its third marginal. Gibbs against the product
    of the state's own two marginals; absolute continuity is automatic. -/
theorem entropy_grouping {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    {q : α × β × γ → ℝ} (hq : IsProb q) :
    entropy q ≤ entropy (marg₁₂ q) + entropy (marg₃ q) := by
  obtain ⟨h0, h1⟩ := hq
  set r : α × β × γ → ℝ := fun t => marg₁₂ q (t.1, t.2.1) * marg₃ q t.2.2 with hr_def
  have hr0 : ∀ t, 0 ≤ r t := fun t =>
    mul_nonneg (marg₁₂_nonneg h0 _) (marg₃_nonneg h0 _)
  have habs : ∀ t, 0 < q t → 0 < r t := by
    rintro ⟨a, b, c⟩ hpos
    exact mul_pos (lt_of_lt_of_le hpos (le_marg₁₂ h0 a b c))
                  (lt_of_lt_of_le hpos (le_marg₃ h0 a b c))
  have hr1 : ∑ t, r t = 1 := by
    have hm3 : ∑ c, marg₃ q c = 1 := by rw [sum_marg₃]; exact h1
    have hm12 : ∑ ab, marg₁₂ q ab = 1 := by rw [sum_marg₁₂]; exact h1
    simp only [hr_def, Fintype.sum_prod_type]
    calc ∑ a, ∑ b, ∑ c, marg₁₂ q (a, b) * marg₃ q c
        = ∑ a, ∑ b, marg₁₂ q (a, b) * ∑ c, marg₃ q c := by
          exact Finset.sum_congr rfl fun a _ => Finset.sum_congr rfl fun b _ =>
            (Finset.mul_sum _ _ _).symm
      _ = ∑ a, ∑ b, marg₁₂ q (a, b) := by simp [hm3]
      _ = 1 := by rw [← Fintype.sum_prod_type]; exact hm12
  have key : ∑ t, q t * Real.log (r t) - ∑ t, q t * Real.log (q t) ≤ 0 := by
    have h2 := Finset.sum_le_sum fun t (_ : t ∈ Finset.univ) =>
      mul_log_sub_le (h0 t) (hr0 t) (habs t)
    have h3 : ∑ t, (r t - q t) = 0 := by
      rw [Finset.sum_sub_distrib, hr1, h1, sub_self]
    have h4 : ∑ t, (q t * Real.log (r t) - q t * Real.log (q t))
        = ∑ t, q t * Real.log (r t) - ∑ t, q t * Real.log (q t) :=
      Finset.sum_sub_distrib
    linarith
  have hsplit : ∑ t, q t * Real.log (r t)
      = (∑ t : α × β × γ, q t * Real.log (marg₁₂ q (t.1, t.2.1)))
        + ∑ t : α × β × γ, q t * Real.log (marg₃ q t.2.2) := by
    rw [← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl ?_
    rintro ⟨a, b, c⟩ -
    rcases (h0 (a, b, c)).eq_or_lt with h | h
    · rw [← h]; simp
    · have hm12 : 0 < marg₁₂ q (a, b) := lt_of_lt_of_le h (le_marg₁₂ h0 a b c)
      have hm3 : 0 < marg₃ q c := lt_of_lt_of_le h (le_marg₃ h0 a b c)
      show q (a, b, c) * Real.log (marg₁₂ q (a, b) * marg₃ q c) = _
      rw [Real.log_mul hm12.ne' hm3.ne']
      ring
  have hm12sum : ∑ t : α × β × γ, q t * Real.log (marg₁₂ q (t.1, t.2.1))
      = ∑ ab : α × β, marg₁₂ q ab * Real.log (marg₁₂ q ab) := by
    simp only [Fintype.sum_prod_type]
    refine Finset.sum_congr rfl fun a _ => Finset.sum_congr rfl fun b _ => ?_
    rw [← Finset.sum_mul]
    rfl
  have hm3sum : ∑ t : α × β × γ, q t * Real.log (marg₃ q t.2.2)
      = ∑ c : γ, marg₃ q c * Real.log (marg₃ q c) := by
    simp only [Fintype.sum_prod_type]
    calc ∑ a, ∑ b, ∑ c, q (a, b, c) * Real.log (marg₃ q c)
        = ∑ a, ∑ c, ∑ b, q (a, b, c) * Real.log (marg₃ q c) :=
          Finset.sum_congr rfl fun a _ => Finset.sum_comm
      _ = ∑ c, ∑ a, ∑ b, q (a, b, c) * Real.log (marg₃ q c) := Finset.sum_comm
      _ = ∑ c : γ, marg₃ q c * Real.log (marg₃ q c) := by
          refine Finset.sum_congr rfl fun c _ => ?_
          simp only [marg₃, Finset.sum_mul]
  unfold entropy
  have := hsplit
  rw [hm12sum, hm3sum] at this
  linarith [key, this]

/-! ### The discriminator: pair structure without whole-only pattern -/

/-- Two copied bits and a free third: pair structure without any whole-only
    pattern. Multi-information reads it loudly; the share must read zero. -/
noncomputable def copied : Bool × Bool × Bool → ℝ :=
  fun t => if t.1 = t.2.1 then 1/4 else 0

private lemma log_half' : Real.log ((1:ℝ)/2) = -Real.log 2 := by
  rw [one_div, Real.log_inv]

private lemma entropy_uniform_bool' :
    entropy (fun _ : Bool => (1:ℝ)/2) = Real.log 2 := by
  unfold entropy
  rw [Fintype.sum_bool, log_half']
  ring

private lemma copied_isProb : IsProb copied := by
  constructor
  · rintro ⟨a, b, c⟩
    unfold copied
    dsimp only
    split <;> norm_num
  · unfold copied
    simp only [Fintype.sum_prod_type, Fintype.sum_bool]
    norm_num

private lemma entropy_copied : entropy copied = 2 * Real.log 2 := by
  unfold entropy copied
  simp only [Fintype.sum_prod_type, Fintype.sum_bool]
  norm_num [log_quarter']
  ring

private lemma entropy_marg₁₂_copied : entropy (marg₁₂ copied) = Real.log 2 := by
  have h : marg₁₂ copied = fun ab : Bool × Bool => if ab.1 = ab.2 then (1:ℝ)/2 else 0 := by
    funext ab
    unfold marg₁₂ copied
    cases ab.1 <;> cases ab.2 <;> simp [Fintype.sum_bool] <;> norm_num
  rw [h]
  unfold entropy
  simp only [Fintype.sum_prod_type, Fintype.sum_bool]
  norm_num [log_half']
  ring

private lemma marg₃_copied : marg₃ copied = fun _ : Bool => (1:ℝ)/2 := by
  funext c
  unfold marg₃ copied
  simp only [Fintype.sum_bool]
  norm_num

private lemma marg₃_eq_sum_marg₂₃ {α β γ : Type*} [Fintype α] [Fintype β]
    (q : α × β × γ → ℝ) (c : γ) : marg₃ q c = ∑ b, marg₂₃ q (b, c) :=
  Finset.sum_comm

private lemma marg₃_of_samePairs {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    {p q : α × β × γ → ℝ} (h : SamePairs p q) : marg₃ q = marg₃ p := by
  funext c
  rw [marg₃_eq_sum_marg₂₃, marg₃_eq_sum_marg₂₃, h.2.2]

private lemma copied_envelope_sSup :
    sSup (pairEnvelope copied) = 2 * Real.log 2 := by
  refine IsGreatest.csSup_eq
    ⟨⟨copied, copied_isProb, ⟨rfl, rfl, rfl⟩, entropy_copied⟩, ?_⟩
  rintro h ⟨q, hq, hpairs, rfl⟩
  have h1 : entropy q ≤ entropy (marg₁₂ q) + entropy (marg₃ q) := entropy_grouping hq
  rw [hpairs.1, marg₃_of_samePairs hpairs, entropy_marg₁₂_copied, marg₃_copied,
      entropy_uniform_bool'] at h1
  linarith

/-- THE DISCRIMINATOR, first half: the copied state's share is exactly zero.
    Its pair data already spends all its order; nothing lives above the pairs. -/
theorem share_copied : share copied = 0 := by
  unfold share
  rw [copied_envelope_sSup, entropy_copied]
  ring

private lemma copied_marg₁ :
    (fun a => ∑ b, ∑ c, copied (a, b, c)) = fun _ : Bool => (1:ℝ)/2 := by
  funext a
  cases a <;> simp [copied, Fintype.sum_bool] <;> norm_num

private lemma copied_marg₂ :
    (fun b => ∑ a, ∑ c, copied (a, b, c)) = fun _ : Bool => (1:ℝ)/2 := by
  funext b
  cases b <;> simp [copied, Fintype.sum_bool] <;> norm_num

private lemma copied_marg₃ :
    (fun c => ∑ a, ∑ b, copied (a, b, c)) = fun _ : Bool => (1:ℝ)/2 := by
  funext c
  cases c <;> simp [copied, Fintype.sum_bool] <;> norm_num

/-- THE DISCRIMINATOR, second half: multi-information reads the copied state
    loudly — `log 2`, its pair structure. Together with `share_copied` and
    `share_parity_positive`, this separates the share from `S_total` in both
    directions: the share is the part of the order that lives above every
    pair, and only that part. -/
theorem S_total_copied : S_total copied = Real.log 2 := by
  unfold S_total
  rw [copied_marg₁, copied_marg₂, copied_marg₃, entropy_uniform_bool', entropy_copied]
  ring

theorem S_total_copied_positive : 0 < S_total copied := by
  rw [S_total_copied]
  exact Real.log_pos (by norm_num)

end CIRISOntology.Core
