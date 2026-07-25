/-
CIRISOntology.Core.SignSymmetry — where NOT to look for whole-only structure.

WHAT IS PROVED. A three-bit state invariant under the GLOBAL sign flip — flip
every coordinate at once, `p(s) = p(−s)` — has whole-only share exactly zero:
`share_eq_zero_of_signSymmetric`. There is no hypothesis on the pair
correlations, no temperature, no coupling strength: the share is identically
zero across the whole sign-symmetric family, however strongly correlated its
members are.

THE ROUTE (three steps, all elementary).

  1. SYMMETRIZATION. Given any competitor `q` carrying `p`'s pair marginals,
     average it with its own flip: `symmetrize q := (q + q ∘ signFlip)/2`. It
     is a probability state (`symmetrize_isProb`), it is sign-symmetric
     (`symmetrize_signSymmetric`), and it still carries exactly `p`'s pair
     marginals (`samePairs_symmetrize`) — that last step is where the
     hypothesis is spent, because it needs `p`'s OWN pair marginals to be
     sign-symmetric (`marg₁₂_signSymmetric` and its two siblings).

  2. CONCAVITY. `entropy_le_symmetrize`: averaging a state with its flip never
     lowers the entropy. Two-point Jensen for `t·log t`, obtained from this
     repository's `mul_log_sub_le` — the same `log x ≤ x − 1` stone used for
     the Gibbs bound, for pinching, and for grouping subadditivity.

  3. UNIQUENESS. `eq_of_signSymmetric_of_samePairs`: on three bits a
     sign-symmetric probability state is DETERMINED by its three pair
     marginals. The flip pairs the eight cells into four antipodal classes, so
     there are four unknowns; normalization and one value from each of the
     three pair marginals are four independent linear constraints. Proved by
     solving that linear system cell by cell.

  Composing: every competitor `q` has `entropy q ≤ entropy (symmetrize q)
  = entropy p`. So `entropy p` is the GREATEST element of the pair envelope,
  not merely one of its elements, and the share — the gap from the state's own
  entropy to the top of the envelope — is exactly zero.

THE CONSEQUENCE, stated as a place not to look. A zero-field Ising model is
sign-symmetric at EVERY temperature, criticality included; so are the
transverse-field and kinetic Ising models, and so are the Z₂-symmetric maximum-
entropy models fitted to neural data. On three slots, the whole-only share of
every one of them is exactly zero. Published peaks in "higher-order structure"
at the Ising critical point are therefore peaks in some other quantity —
O-information, PID synergy, Φ, TSE complexity, specific heat — every one of
which is nonzero on purely pairwise systems. The design principle in the other
direction: **order-3 whole-only structure requires broken global sign
symmetry.** If a spin system is to carry any, the field must be nonzero or the
symmetry must be broken by hand.

A related trap, recorded because it caught us in draft: a large three-point
correlation function is NOT order-3 structure. A pairwise Hamiltonian with a
field can give ⟨s₁s₂s₃⟩ ≈ 0.91 with a share of order 1e−14. The correlator is
a moment; the share is what the pair marginals cannot reconstruct.

THE PARITY CONSISTENCY CHECK. `Core.Share` proves `share parity = log 2`,
strictly positive. That is not in tension with this file: `parity` is sign-ODD,
because flipping all three bits breaks `c = a XOR b`. Exhibited as a theorem,
`parity_not_signSymmetric`, so the edge of the lemma is visible rather than
asserted. In the other direction the lemma has teeth on a state we already
carry: `share_indep`, the uniform state's share is zero, is now one line.

CREDIT. The lemma was derived here, in this programme's own literature survey
(`scratchpad/temporal-share/SPIKE_SURVEY.md`, commit 1ffb17a), and numerically
verified there before any Lean was written: max |I_C^(3)| = 1.9e−10 nats over
2000 random sign-symmetric three-variable distributions, with the positive
controls firing (three-coin parity at ln 2 exactly, an explicit three-body
coupling at 0.247 nats). It is elementary and may well be known; we searched
and found no citation, and we are not claiming priority — we are recording
where it came from.

SCOPE. Proved here: three binary slots, the classical (diagonal) sector,
order 3. NOT proved here: the general statement that sign symmetry kills
connected information at every odd order on k slots — that is the form the
survey states and checked numerically (four variables, odd orders at 1.7e−13
while order 4 survives at 0.169 nats), and it is not mechanized. NOT proved
anywhere: any claim about which physical systems are sign-symmetric.

Mathlib survey: nothing needed beyond `Core.Share`; `IsGreatest.csSup_eq`
closes the supremum. No gaps to port.
-/
import CIRISOntology.Core.Share

namespace CIRISOntology.Core

open scoped BigOperators

/-! ### The global sign flip -/

/-- The global sign flip on three bits: complement every coordinate at once.
    In ±1 language this is `s ↦ −s`. -/
def signFlip (t : Bool × Bool × Bool) : Bool × Bool × Bool :=
  (!t.1, !t.2.1, !t.2.2)

/-- A state is SIGN-SYMMETRIC when complementing all three coordinates at once
    leaves it unchanged: `p(s) = p(−s)`. This is the Z₂ symmetry every
    zero-field Ising model has, at every temperature. -/
def SignSymmetric (p : Bool × Bool × Bool → ℝ) : Prop :=
  ∀ a b c, p (a, b, c) = p (!a, !b, !c)

/-- The flip is a relabeling of the eight cells, so no total sum notices it. -/
lemma sum_comp_signFlip (f : Bool × Bool × Bool → ℝ) :
    ∑ t, f (signFlip t) = ∑ t, f t := by
  simp only [signFlip, Fintype.sum_prod_type, Fintype.sum_bool, Bool.not_true,
    Bool.not_false]
  ring

/-! ### The symmetrization -/

/-- The sign-symmetrization of a state: average it with its own global flip. -/
noncomputable def symmetrize (q : Bool × Bool × Bool → ℝ) :
    Bool × Bool × Bool → ℝ :=
  fun t => (q t + q (signFlip t)) / 2

lemma symmetrize_signSymmetric (q : Bool × Bool × Bool → ℝ) :
    SignSymmetric (symmetrize q) := by
  intro a b c
  simp only [symmetrize, signFlip, Bool.not_not]
  ring

lemma symmetrize_isProb {q : Bool × Bool × Bool → ℝ} (hq : IsProb q) :
    IsProb (symmetrize q) := by
  refine ⟨fun t => ?_, ?_⟩
  · have h1 := hq.1 t
    have h2 := hq.1 (signFlip t)
    simp only [symmetrize]
    linarith
  · simp only [symmetrize]
    have h1 : ∑ t, (q t + q (signFlip t)) / 2
        = (∑ t, q t + ∑ t, q (signFlip t)) / 2 := by
      rw [← Finset.sum_div, Finset.sum_add_distrib]
    rw [h1, sum_comp_signFlip q, hq.2]
    norm_num

/-! ### Two-point concavity of the entropy -/

/-- Two-point Jensen for `t·log t`: the midpoint value never exceeds the
    average of the endpoint values. From `mul_log_sub_le` — the `log x ≤ x − 1`
    stone, applied at each endpoint against the midpoint. -/
private lemma mul_log_mix {x y : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y) :
    ((x + y) / 2) * Real.log ((x + y) / 2)
      ≤ (x * Real.log x + y * Real.log y) / 2 := by
  have hm0 : (0:ℝ) ≤ (x + y) / 2 := by linarith
  have h1 := mul_log_sub_le hx hm0 (fun h => by linarith)
  have h2 := mul_log_sub_le hy hm0 (fun h => by linarith)
  have key : ((x + y) / 2) * Real.log ((x + y) / 2)
      = (x * Real.log ((x + y) / 2) + y * Real.log ((x + y) / 2)) / 2 := by ring
  rw [key]
  linarith

/-- AVERAGING NEVER LOWERS THE ENTROPY: symmetrizing a state can only raise it.
    Pointwise two-point Jensen, then the flip-blindness of the total sum. -/
lemma entropy_le_symmetrize {q : Bool × Bool × Bool → ℝ} (hq : IsProb q) :
    entropy q ≤ entropy (symmetrize q) := by
  have hpt : ∀ t, symmetrize q t * Real.log (symmetrize q t)
      ≤ (q t * Real.log (q t)
          + q (signFlip t) * Real.log (q (signFlip t))) / 2 := fun t =>
    mul_log_mix (hq.1 t) (hq.1 (signFlip t))
  have hsum : ∑ t, symmetrize q t * Real.log (symmetrize q t)
      ≤ ∑ t, (q t * Real.log (q t)
          + q (signFlip t) * Real.log (q (signFlip t))) / 2 :=
    Finset.sum_le_sum fun t _ => hpt t
  have hrhs : ∑ t, (q t * Real.log (q t)
      + q (signFlip t) * Real.log (q (signFlip t))) / 2
      = ∑ t, q t * Real.log (q t) := by
    have hsplit : ∑ t, (q t * Real.log (q t)
        + q (signFlip t) * Real.log (q (signFlip t))) / 2
        = ((∑ t, q t * Real.log (q t))
            + ∑ t, q (signFlip t) * Real.log (q (signFlip t))) / 2 := by
      rw [← Finset.sum_div, Finset.sum_add_distrib]
    rw [hsplit, sum_comp_signFlip (fun u => q u * Real.log (q u))]
    ring
  unfold entropy
  linarith

/-! ### Sign-symmetric pair marginals -/

private lemma marg₁₂_signSymmetric {p : Bool × Bool × Bool → ℝ}
    (hp : SignSymmetric p) (a b : Bool) :
    marg₁₂ p (!a, !b) = marg₁₂ p (a, b) := by
  have h1 := hp a b true
  have h2 := hp a b false
  simp only [Bool.not_true, Bool.not_false] at h1 h2
  simp only [marg₁₂, Fintype.sum_bool]
  linarith

private lemma marg₁₃_signSymmetric {p : Bool × Bool × Bool → ℝ}
    (hp : SignSymmetric p) (a c : Bool) :
    marg₁₃ p (!a, !c) = marg₁₃ p (a, c) := by
  have h1 := hp a true c
  have h2 := hp a false c
  simp only [Bool.not_true, Bool.not_false] at h1 h2
  simp only [marg₁₃, Fintype.sum_bool]
  linarith

private lemma marg₂₃_signSymmetric {p : Bool × Bool × Bool → ℝ}
    (hp : SignSymmetric p) (b c : Bool) :
    marg₂₃ p (!b, !c) = marg₂₃ p (b, c) := by
  have h1 := hp true b c
  have h2 := hp false b c
  simp only [Bool.not_true, Bool.not_false] at h1 h2
  simp only [marg₂₃, Fintype.sum_bool]
  linarith

private lemma marg₁₂_symmetrize (q : Bool × Bool × Bool → ℝ) (a b : Bool) :
    marg₁₂ (symmetrize q) (a, b)
      = (marg₁₂ q (a, b) + marg₁₂ q (!a, !b)) / 2 := by
  simp only [marg₁₂, symmetrize, signFlip, Fintype.sum_bool, Bool.not_true,
    Bool.not_false]
  ring

private lemma marg₁₃_symmetrize (q : Bool × Bool × Bool → ℝ) (a c : Bool) :
    marg₁₃ (symmetrize q) (a, c)
      = (marg₁₃ q (a, c) + marg₁₃ q (!a, !c)) / 2 := by
  simp only [marg₁₃, symmetrize, signFlip, Fintype.sum_bool, Bool.not_true,
    Bool.not_false]
  ring

private lemma marg₂₃_symmetrize (q : Bool × Bool × Bool → ℝ) (b c : Bool) :
    marg₂₃ (symmetrize q) (b, c)
      = (marg₂₃ q (b, c) + marg₂₃ q (!b, !c)) / 2 := by
  simp only [marg₂₃, symmetrize, signFlip, Fintype.sum_bool, Bool.not_true,
    Bool.not_false]
  ring

/-- SYMMETRIZATION KEEPS THE PAIR DATA, provided the target state's own pair
    marginals are sign-symmetric — which they are, whenever it is. This is
    where the hypothesis of the main theorem is spent. -/
lemma samePairs_symmetrize {p q : Bool × Bool × Bool → ℝ}
    (hp : SignSymmetric p) (h : SamePairs p q) : SamePairs p (symmetrize q) := by
  obtain ⟨h12, h13, h23⟩ := h
  refine ⟨?_, ?_, ?_⟩
  · funext ab
    obtain ⟨a, b⟩ := ab
    rw [marg₁₂_symmetrize, h12, marg₁₂_signSymmetric hp]
    ring
  · funext ac
    obtain ⟨a, c⟩ := ac
    rw [marg₁₃_symmetrize, h13, marg₁₃_signSymmetric hp]
    ring
  · funext bc
    obtain ⟨b, c⟩ := bc
    rw [marg₂₃_symmetrize, h23, marg₂₃_signSymmetric hp]
    ring

/-! ### Uniqueness: three pair marginals pin a sign-symmetric state -/

/-- THE STRUCTURAL FACT. On three bits, a sign-symmetric probability state is
    determined by its three pair marginals. The flip pairs the eight cells into
    four antipodal classes — four unknowns — and normalization plus one value
    from each pair marginal are four independent linear constraints. Solved
    cell by cell. -/
lemma eq_of_signSymmetric_of_samePairs {p r : Bool × Bool × Bool → ℝ}
    (hp : IsProb p) (hr : IsProb r) (hps : SignSymmetric p)
    (hrs : SignSymmetric r) (hpair : SamePairs p r) : r = p := by
  obtain ⟨h12, h13, h23⟩ := hpair
  have E12 : ∀ a b : Bool, r (a, b, true) + r (a, b, false)
      = p (a, b, true) + p (a, b, false) := by
    intro a b
    have h := congrFun h12 (a, b)
    simpa [marg₁₂, Fintype.sum_bool] using h
  have E13 : ∀ a c : Bool, r (a, true, c) + r (a, false, c)
      = p (a, true, c) + p (a, false, c) := by
    intro a c
    have h := congrFun h13 (a, c)
    simpa [marg₁₃, Fintype.sum_bool] using h
  have E23 : ∀ b c : Bool, r (true, b, c) + r (false, b, c)
      = p (true, b, c) + p (false, b, c) := by
    intro b c
    have h := congrFun h23 (b, c)
    simpa [marg₂₃, Fintype.sum_bool] using h
  have Np := hp.2
  have Nr := hr.2
  simp only [Fintype.sum_prod_type, Fintype.sum_bool] at Np Nr
  have P1 : p (false, false, false) = p (true, true, true) := by
    simpa using hps false false false
  have P2 : p (false, false, true) = p (true, true, false) := by
    simpa using hps false false true
  have P3 : p (false, true, false) = p (true, false, true) := by
    simpa using hps false true false
  have P4 : p (false, true, true) = p (true, false, false) := by
    simpa using hps false true true
  have R1 : r (false, false, false) = r (true, true, true) := by
    simpa using hrs false false false
  have R2 : r (false, false, true) = r (true, true, false) := by
    simpa using hrs false false true
  have R3 : r (false, true, false) = r (true, false, true) := by
    simpa using hrs false true false
  have R4 : r (false, true, true) = r (true, false, false) := by
    simpa using hrs false true true
  funext t
  obtain ⟨a, b, c⟩ := t
  cases a <;> cases b <;> cases c <;>
    linarith [E12 false false, E12 false true, E12 true false, E12 true true,
      E13 false false, E13 false true, E13 true false, E13 true true,
      E23 false false, E23 false true, E23 true false, E23 true true]

/-! ### The lemma -/

/-- THE SIGN-SYMMETRY LEMMA: a three-bit state invariant under the global sign
    flip has whole-only share exactly zero. No hypothesis on its correlations:
    however strong the pair structure, nothing lives above the pairs.

    Read as a place not to look — a zero-field Ising model is sign-symmetric at
    every temperature, criticality included, so its order-3 whole-only share is
    identically zero throughout. Whatever peaks at such a critical point, it is
    not this quantity. Read as a design principle: order-3 whole-only structure
    requires broken global sign symmetry.

    The edge of the lemma is exhibited, not asserted: `parity_not_signSymmetric`
    shows the parity state is sign-ODD, which is why `share_parity = log 2`
    stands. -/
theorem share_eq_zero_of_signSymmetric {p : Bool × Bool × Bool → ℝ}
    (hp : IsProb p) (hsym : ∀ a b c, p (a, b, c) = p (!a, !b, !c)) :
    share p = 0 := by
  have hgreat : IsGreatest (pairEnvelope p) (entropy p) := by
    refine ⟨⟨p, hp, ⟨rfl, rfl, rfl⟩, rfl⟩, ?_⟩
    rintro h ⟨q, hq, hpairs, rfl⟩
    have h1 : entropy q ≤ entropy (symmetrize q) := entropy_le_symmetrize hq
    have h2 : symmetrize q = p :=
      eq_of_signSymmetric_of_samePairs hp (symmetrize_isProb hq) hsym
        (symmetrize_signSymmetric q) (samePairs_symmetrize hsym hpairs)
    rwa [h2] at h1
  unfold share
  rw [hgreat.csSup_eq]
  ring

/-- The uniform state is sign-symmetric, so its share is zero — one line, and
    the lemma's first customer. -/
theorem share_indep : share indep = 0 :=
  share_eq_zero_of_signSymmetric indep_isProb (fun _ _ _ => rfl)

/-! ### The lemma has teeth: a maximally correlated state with zero share

`share_indep` is a state with no correlation at all, so it proves nothing about
the lemma's reach. The state below has the strongest pair correlation three
bits admit — all three always agree — and is still sign-symmetric, being the
zero-temperature ensemble of the ferromagnetic Ising model, both ground states
kept. Its share is zero and its multi-information is two full bits. -/

/-- All three bits agree, both ways round: the T = 0 Ising ensemble. Maximally
    pair-correlated, and sign-symmetric because both ground states are kept. -/
noncomputable def ferro : Bool × Bool × Bool → ℝ :=
  fun t => if t.1 = t.2.1 ∧ t.2.1 = t.2.2 then 1/2 else 0

lemma ferro_isProb : IsProb ferro := by
  constructor
  · rintro ⟨a, b, c⟩
    unfold ferro
    dsimp only
    split <;> norm_num
  · unfold ferro
    simp only [Fintype.sum_prod_type, Fintype.sum_bool]
    norm_num

lemma ferro_signSymmetric : SignSymmetric ferro := by
  intro a b c
  cases a <;> cases b <;> cases c <;> simp [ferro]

/-- THE LEMMA WITH TEETH: the most strongly pair-correlated state on three bits
    has whole-only share exactly zero. All the order is in the pairs. -/
theorem share_ferro : share ferro = 0 :=
  share_eq_zero_of_signSymmetric ferro_isProb ferro_signSymmetric

private lemma log_half'' : Real.log ((1:ℝ)/2) = -Real.log 2 := by
  rw [one_div, Real.log_inv]

private lemma entropy_uniform_bool'' :
    entropy (fun _ : Bool => (1:ℝ)/2) = Real.log 2 := by
  unfold entropy
  rw [Fintype.sum_bool, log_half'']
  ring

private lemma ferro_marg₁ :
    (fun a => ∑ b, ∑ c, ferro (a, b, c)) = fun _ : Bool => (1:ℝ)/2 := by
  funext a
  cases a <;> simp [ferro, Fintype.sum_bool]

private lemma ferro_marg₂ :
    (fun b => ∑ a, ∑ c, ferro (a, b, c)) = fun _ : Bool => (1:ℝ)/2 := by
  funext b
  cases b <;> simp [ferro, Fintype.sum_bool]

private lemma ferro_marg₃ :
    (fun c => ∑ a, ∑ b, ferro (a, b, c)) = fun _ : Bool => (1:ℝ)/2 := by
  funext c
  cases c <;> simp [ferro, Fintype.sum_bool]

private lemma entropy_ferro : entropy ferro = Real.log 2 := by
  unfold entropy ferro
  simp only [Fintype.sum_prod_type, Fintype.sum_bool]
  norm_num [log_half'']
  ring

/-- And the contrast, so the zero above cannot be mistaken for "no order here":
    multi-information reads the same state at TWO bits. Same shape as
    `share_copied` / `S_total_copied`, one rung stronger — this state is
    sign-symmetric, so the zero is forced by symmetry alone, not computed. -/
theorem S_total_ferro : S_total ferro = 2 * Real.log 2 := by
  unfold S_total
  rw [ferro_marg₁, ferro_marg₂, ferro_marg₃, entropy_uniform_bool'',
    entropy_ferro]
  ring

/-! ### The parity consistency check -/

/-- THE EDGE OF THE LEMMA. The parity state is sign-ODD: flipping all three
    bits breaks `c = a XOR b`, sending a cell of weight `1/4` to a cell of
    weight `0`. So `share_parity = log 2` is not in tension with the lemma —
    parity sits exactly outside its hypothesis, and that is why it carries a
    bit. -/
theorem parity_not_signSymmetric : ¬ SignSymmetric parity := by
  intro h
  have h0 := h false false false
  simp only [parity, Bool.not_false] at h0
  norm_num at h0

end CIRISOntology.Core
