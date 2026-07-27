/-
CIRISOntology.Core.FlavorBridge — the flavour bridge: one family of three-slot
states in which the Jarlskog coordinate IS the whole-only share.

WHAT THIS FILE IS, and it must not be read as more. This repository carries two
separate three-body vanishing theorems that have never been joined:

  * `Core.Flavor` — the Jarlskog invariant `J = J_max(angles) · sin δ` is capped
    by its angle envelope (`abs_jarlskog_le_max`) and vanishes at the no-mixing
    pole (`jarlskogMax_zero_at_no_mixing`). Pure trigonometry.
  * `Core.Share` / `Core.SignSymmetry` — the whole-only share of a three-slot
    state vanishes identically on the sign-symmetric family
    (`share_eq_zero_of_signSymmetric`), and equals `log 2` on the parity state.

They vanish for what looks like the same reason — a T-odd / sign-odd coordinate
being switched off — and this file makes that "looks like" into a theorem, on a
MODEL. It exhibits one explicit one-parameter family of three-bit distributions
wearing the Jarlskog invariant's shape, and proves that on that family the two
vanishings are the SAME vanishing.

  `cpState J t = (1 + J · χ(t)) / 8`,   `χ(t) = σ₁σ₂σ₃`  (the ±1 triple product)

with `J` set to `jarlskog θ₁₂ θ₂₃ θ₁₃ δ` in `cpFamily`. The triple product is
the T-odd observable; `χ` is the parity character, the one direction on eight
cells that every two-slot reading is blind to.

WHAT IS PROVED (all sorry-free, all about this family).

  * `cp_phase_invisible_to_pairs` — EVERY member carries identical two-slot data:
    all three pair marginals are uniform `1/4` at every phase. So no pairwise
    reading of any kind distinguishes the CP-even member from any other, and
    `cpState_corr_eq_one` says the same at the instrument level — the correlation
    matrix is the identity for every `J`, exactly as it is for `parity`
    (`parity_corr_eq_one`). The phase lives entirely above the pairs.

  * `symmetrize_cpState` — the CP-SYMMETRIZED MEMBER IS THE UNIFORM STATE.
    Global sign flip is this model's CP conjugation: it sends the member at
    phase `J` to the member at `−J` (`cpState_neg_eq_signFlip`), so averaging a
    member with its conjugate erases the odd coordinate outright. Hence
    `share_symmetrize_cpState = 0`.

  * `share_cpState` — THE CLOSED FORM, exact:

        share (cpState J) = ((1+J)/2)·log(1+J) + ((1−J)/2)·log(1−J)

    for `|J| ≤ 1`. This is `log 2` minus the binary entropy of `(1+J)/2` — the
    whole-only share of the family is exactly the binary-entropy gap in the
    CP-odd coordinate. It is not a bound and not an asymptotic: the pair
    marginals are uniform, so the constrained maximum-entropy problem is solved
    by the unconstrained maximizer and the Gibbs bound closes it, the same
    reason `share_parity` is exact. At `J = ±1` it returns `log 2` — at `J = −1`
    the member is literally this repository's `parity` and at `J = +1` it is
    parity's complement — so the family interpolates the whole span the classical
    cap allows at `k = 3`, from zero to one bit.

  * `share_zero_of_cp_even` / `share_pos_of_cp_odd` / `share_cpState_eq_zero_iff`
    — THE BRIDGE ITSELF. Where the Jarlskog coordinate vanishes — and at
    `sin δ = 0` it does — the member is sign-symmetric and its share is exactly
    zero, by composition with `share_eq_zero_of_signSymmetric`; where the
    coordinate is nonzero the share is STRICTLY positive; and the share vanishes
    if and only if the coordinate does. One vanishing, two names.

  * `share_cpFamily_le_phase` / `share_cpFamily_le_jarlskogMax` — THE CEILING
    COMPOSES. The family's share obeys

        share (cpFamily θ δ) ≤ |sin δ| · cpShare (J_max(θ)) ≤ cpShare (J_max(θ))

    the closed form evaluated at `abs_jarlskog_le_max`'s own envelope, damped by
    the phase — the share's version of the Jarlskog bound, saturated only at
    maximal phase. It needs no octant hypothesis, because the closed form is
    even and reads the envelope's magnitude only. The route is concavity of the
    entropy along the family, which is affine in `J`:
    `cpState (t·M) = t·cpState M + (1−t)·indep`. That needed two general stones
    this file adds, `mul_log_convex` and `entropy_concave`.

  * `share_cpFamily_zero_at_no_mixing` — and the aligned pole is shared too:
    where any mixing angle vanishes, `J_max = 0`, so the family's whole-only
    share is exactly zero however large the phase.

  * `cpState_neg_one` / `share_parity_eq_cpShare` — THE FAMILY IS A LINE THROUGH
    THE REPOSITORY'S ANCHOR STATE, not an object bolted alongside it: at
    `J = −1` the member is literally `parity`, and the closed form there
    reproduces `share_parity = log 2`, computed earlier by a
    different route.

SCOPE — LOAD-BEARING, and the reason this file is not a physics claim.

  1. This is a MODEL BRIDGE. `cpState J` is a family of probability
     distributions on three bits that WEARS the Jarlskog invariant's algebraic
     shape. Nothing here derives it from a Lagrangian, from CKM unitarity, or
     from any decay amplitude. Substituting `jarlskog` for `J` is a choice made
     by hand in `cpFamily`, not a consequence of anything proved.

  2. The physics of T-odd triple products is NOT formalized here, and it is
     harder than the model. In real decays a triple-product asymmetry is faked
     by final-state interactions: strong rescattering phases produce a nonzero
     T-odd signal with no CP violation at all. Only the CP-CONJUGATE DIFFERENCE
     of the two asymmetries is clean. That distinction — the whole difficulty of
     the measurement — has no counterpart below, because this model has no
     final-state phases to fake anything. Any reading of these theorems as
     support for a flavour-physics claim is a misreading. The physical
     measurement is the Dalitz campaign, which lives in the scratchpad and is
     not proved anywhere.

  3. NOT PROVED ANYWHERE: that nature's flavour sector is described by this
     family, that the whole-only share is a measurable of any decay, or that
     the coincidence of the two vanishings is more than an algebraic one on a
     model built to display it.

CREDIT. The invariant and its reparametrization-invariance are Jarlskog's:
C. Jarlskog, "Commutator of the Quark Mass Matrices in the Standard Electroweak
Model and a Measure of Maximal CP Nonconservation", Phys. Rev. Lett. 55 (1985)
1039. The whole-only share is connected information / max-entropy irreducible
correlation (Schneidman–Still–Berry–Bialek 2003). The sign-symmetry lemma is
this programme's own (`Core.SignSymmetry`, credited there). What is ours here is
the composition: the exact closed form on this family, and the observation that
its zero set is precisely the CP-even sector. On the page this file backs the
`cp-cap` claim's context and the phase-at-ceiling wager, at model strength only.

Mathlib survey: `Real.log_lt_sub_one_of_pos` supplies the STRICT Gibbs stone the
positivity needs; everything else is this repository's `mul_log_sub_le`,
`entropy_le_log_card`, `IsGreatest.csSup_eq` and `le_csSup`. No gaps to port.
-/
import CIRISOntology.Core.SignSymmetry
import CIRISOntology.Core.Flavor

namespace CIRISOntology.Core

open scoped BigOperators
open Real

/-! ### The family -/

/-- THE PARITY CHARACTER, in ±1 language: the triple product `σ₁σ₂σ₃`. It is
    `−1` exactly on the four cells where the third bit is the XOR of the first
    two — the support of `parity` — and `+1` on the other four. This is the one
    direction on the eight cells that sums to zero along every pair fiber, so it
    is invisible to every two-slot reading; and it is the T-odd observable of
    the model, because the global sign flip reverses it. -/
noncomputable def parityChar (t : Bool × Bool × Bool) : ℝ :=
  pm t.1 * pm t.2.1 * pm t.2.2

/-- THE CP CONJUGATION OF THE MODEL. The global sign flip reverses the triple
    product: `χ(−s) = −χ(s)`. Everything below is this one line, developed. -/
theorem parityChar_signFlip (t : Bool × Bool × Bool) :
    parityChar (signFlip t) = -parityChar t := by
  obtain ⟨a, b, c⟩ := t
  cases a <;> cases b <;> cases c <;> simp [parityChar, signFlip, pm]

/-- THE FAMILY: the uniform state tilted along the parity character by an amount
    `J`. Every member has uniform pair marginals; the whole of its structure
    lives in the one coordinate `J`, which is the model's stand-in for the
    Jarlskog invariant. `cpState 0` is the uniform state and `cpState (±1)` is a
    parity state. -/
noncomputable def cpState (J : ℝ) : Bool × Bool × Bool → ℝ :=
  fun t => (1 + J * parityChar t) / 8

/-- THE FAMILY, PARAMETRIZED AS FLAVOUR IS: three mixing angles and one phase,
    with the odd coordinate set to the Jarlskog invariant
    `J = c₁₂s₁₂c₂₃s₂₃c₁₃²s₁₃ · sin δ`. The substitution is made by hand — see
    the file header; nothing derives it. -/
noncomputable def cpFamily (θ12 θ23 θ13 δ : ℝ) : Bool × Bool × Bool → ℝ :=
  cpState (jarlskog θ12 θ23 θ13 δ)

/-- The two-valued form of a member, which is what every computation below
    runs on: weight `(1−J)/8` on the four parity cells, `(1+J)/8` on the rest. -/
private lemma cpState_eq (J : ℝ) (t : Bool × Bool × Bool) :
    cpState J t = if t.2.2 = Bool.xor t.1 t.2.1 then (1 - J) / 8 else (1 + J) / 8 := by
  obtain ⟨a, b, c⟩ := t
  cases a <;> cases b <;> cases c <;> simp [cpState, parityChar, pm] <;> ring

/-- Every member with `|J| ≤ 1` is a probability state; outside that range the
    tilt would drive a cell negative. -/
theorem cpState_isProb {J : ℝ} (hJ : |J| ≤ 1) : IsProb (cpState J) := by
  obtain ⟨hlo, hhi⟩ := abs_le.mp hJ
  constructor
  · rintro ⟨a, b, c⟩
    rw [cpState_eq]
    dsimp only
    split <;> linarith
  · simp only [cpState_eq, Fintype.sum_prod_type, Fintype.sum_bool]
    norm_num
    ring

/-- The CP-even member is the uniform state: no tilt, no pattern at any order. -/
theorem cpState_zero : cpState 0 = indep := by
  funext t
  simp [cpState, indep]

/-- CP CONJUGATION FLIPS THE PHASE. The member at `−J` is the member at `J` read
    through the global sign flip — this model's CP conjugation. -/
theorem cpState_neg_eq_signFlip (J : ℝ) (t : Bool × Bool × Bool) :
    cpState (-J) t = cpState J (signFlip t) := by
  simp only [cpState, parityChar_signFlip]
  ring

/-- THE CP-SYMMETRIZED MEMBER IS THE UNIFORM STATE. Averaging a member with its
    own CP conjugate erases the odd coordinate outright — the T-even part of the
    family is a single point, and it is the point with no pattern at all. -/
theorem symmetrize_cpState (J : ℝ) : symmetrize (cpState J) = indep := by
  funext t
  simp only [symmetrize, cpState, indep, parityChar_signFlip]
  ring

/-- SIGN SYMMETRY IS EXACTLY CP-EVENNESS, in this family: a member is invariant
    under the global flip precisely when its Jarlskog coordinate vanishes. This
    is the hinge of the bridge — it puts `Core.SignSymmetry`'s hypothesis and
    `Core.Flavor`'s vanishing condition on the same footing. -/
theorem cpState_signSymmetric_iff {J : ℝ} : SignSymmetric (cpState J) ↔ J = 0 := by
  constructor
  · intro h
    have h0 := h false false false
    simp only [cpState, parityChar, pm, Bool.not_false] at h0
    norm_num at h0
    linarith
  · rintro rfl
    rw [cpState_zero]
    exact fun _ _ _ => rfl

/-! ### The phase is invisible to every pair -/

private lemma marg₁₂_cpState (J : ℝ) (ab : Bool × Bool) :
    marg₁₂ (cpState J) ab = 1 / 4 := by
  obtain ⟨a, b⟩ := ab
  simp only [marg₁₂, cpState, parityChar, pm, Fintype.sum_bool]
  cases a <;> cases b <;> norm_num <;> ring

private lemma marg₁₃_cpState (J : ℝ) (ac : Bool × Bool) :
    marg₁₃ (cpState J) ac = 1 / 4 := by
  obtain ⟨a, c⟩ := ac
  simp only [marg₁₃, cpState, parityChar, pm, Fintype.sum_bool]
  cases a <;> cases c <;> norm_num <;> ring

private lemma marg₂₃_cpState (J : ℝ) (bc : Bool × Bool) :
    marg₂₃ (cpState J) bc = 1 / 4 := by
  obtain ⟨b, c⟩ := bc
  simp only [marg₂₃, cpState, parityChar, pm, Fintype.sum_bool]
  cases b <;> cases c <;> norm_num <;> ring

/-- THE PHASE IS INVISIBLE TO EVERY PAIR. Any two members of the family carry
    EXACTLY the same two-slot data, at all three pairs, at every phase. There is
    no pairwise statistic whatever — linear, nonlinear, however clever — that
    separates the CP-even member from a maximally CP-odd one. Whatever the phase
    does, it does above the pairs. -/
theorem cp_phase_invisible_to_pairs (J J' : ℝ) : SamePairs (cpState J) (cpState J') :=
  ⟨by funext ab; rw [marg₁₂_cpState, marg₁₂_cpState],
   by funext ac; rw [marg₁₃_cpState, marg₁₃_cpState],
   by funext bc; rw [marg₂₃_cpState, marg₂₃_cpState]⟩

private lemma samePairs_cpState_indep (J : ℝ) : SamePairs (cpState J) indep := by
  have h := cp_phase_invisible_to_pairs J 0
  rwa [cpState_zero] at h

/-- THE SAME STATEMENT AT THE INSTRUMENT. The correlation matrix of every member
    is the identity, at every phase — the same reading `Core.Third` records for
    `parity` (`parity_corr_eq_one`) and for the uniform state
    (`indep_corr_eq_one`). The pairwise instrument reads its floor across the
    whole family. -/
theorem cpState_corr_eq_one (J : ℝ) :
    corrOf (cpState J) = (1 : Matrix (Fin 3) (Fin 3) ℝ) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [corrOf, cpState, parityChar, parityVar, pm, Matrix.one_apply,
      Fintype.sum_prod_type, Fintype.sum_bool] <;>
    ring

/-! ### The closed form: the share is the binary-entropy gap in `J` -/

/-- THE CLOSED FORM of the family's whole-only share, as a function of the odd
    coordinate alone: `log 2` minus the binary entropy of `(1+J)/2`. Even in
    `J` (`cpShare_neg`), zero only at `J = 0`, and `log 2` at `J = ±1`. -/
noncomputable def cpShare (J : ℝ) : ℝ :=
  ((1 + J) / 2) * Real.log (1 + J) + ((1 - J) / 2) * Real.log (1 - J)

/-- THE SHARE READS THE MAGNITUDE ONLY. Conjugate members — `J` and `−J`, the
    two CP images — carry exactly the same whole-only share. The share is a
    T-odd-magnitude reading, blind to the sign of the phase. -/
theorem cpShare_neg (J : ℝ) : cpShare (-J) = cpShare J := by
  simp only [cpShare]
  rw [show (1 : ℝ) + -J = 1 - J by ring, show (1 : ℝ) - -J = 1 + J by ring]
  ring

theorem cpShare_zero : cpShare 0 = 0 := by
  simp [cpShare]

private lemma log_eight' : Real.log (8 : ℝ) = 3 * Real.log 2 := by
  rw [show (8 : ℝ) = 2 ^ 3 by norm_num, Real.log_pow]
  norm_num

private lemma mul_log_div_eight {x : ℝ} (hx : 0 ≤ x) :
    (x / 8) * Real.log (x / 8) = (x / 8) * Real.log x - (x / 8) * (3 * Real.log 2) := by
  rcases hx.eq_or_lt with h | h
  · rw [← h]; norm_num
  · rw [Real.log_div h.ne' (by norm_num), log_eight']
    ring

/-- The top of every member's envelope is `3 log 2`: the pair marginals are
    uniform, so the uniform state itself is a competitor, and the Gibbs bound
    forbids anything higher. Same stone as `share_parity`. -/
private lemma cpState_envelope_sSup (J : ℝ) :
    sSup (pairEnvelope (cpState J)) = 3 * Real.log 2 := by
  refine IsGreatest.csSup_eq
    ⟨⟨indep, indep_isProb, samePairs_cpState_indep J, entropy_indep'⟩, ?_⟩
  rintro h ⟨q, hq, -, rfl⟩
  calc entropy q ≤ Real.log (Fintype.card (Bool × Bool × Bool)) :=
        entropy_le_log_card hq.1 hq.2
    _ = 3 * Real.log 2 := log_card_eight

/-- The member's own entropy, exactly: three bits less the binary-entropy gap. -/
theorem entropy_cpState {J : ℝ} (hJ : |J| ≤ 1) :
    entropy (cpState J) = 3 * Real.log 2 - cpShare J := by
  obtain ⟨hlo, hhi⟩ := abs_le.mp hJ
  have h1 : (0 : ℝ) ≤ 1 + J := by linarith
  have h2 : (0 : ℝ) ≤ 1 - J := by linarith
  have key : entropy (cpState J)
      = -(4 * ((1 + J) / 8 * Real.log ((1 + J) / 8))
          + 4 * ((1 - J) / 8 * Real.log ((1 - J) / 8))) := by
    unfold entropy
    simp only [cpState_eq, Fintype.sum_prod_type, Fintype.sum_bool]
    norm_num
    ring
  rw [key, mul_log_div_eight h1, mul_log_div_eight h2, cpShare]
  ring

/-- **THE CLOSED FORM.** The whole-only share of the family is exactly the
    binary-entropy gap in the Jarlskog coordinate — not a bound, not a limit.
    Every reading of this family's higher-order structure is a reading of `|J|`
    and of nothing else. -/
theorem share_cpState {J : ℝ} (hJ : |J| ≤ 1) : share (cpState J) = cpShare J := by
  unfold share
  rw [cpState_envelope_sSup J, entropy_cpState hJ]
  ring

theorem cpShare_nonneg {J : ℝ} (hJ : |J| ≤ 1) : 0 ≤ cpShare J := by
  rw [← share_cpState hJ]
  exact share_nonneg (cpState_isProb hJ)

/-! ### Positivity: the STRICT Gibbs stone -/

/-- The strict form of the `log x ≤ x − 1` stone, in the shape the two-cell
    computation wants: `t·log(2t) > t − 1/2` unless `t` is exactly `1/2`. At
    `t = 0` the left side is `−1/2` and the right side is `0`, so the strictness
    survives the boundary. -/
private lemma sub_half_lt_mul_log {t : ℝ} (ht : 0 ≤ t) (hne : t ≠ 1 / 2) :
    t - 1 / 2 < t * Real.log (t * 2) := by
  rcases ht.eq_or_lt with h | h
  · rw [← h]; norm_num
  · have h2 : (0 : ℝ) < t * 2 := by linarith
    have hne2 : t * 2 ≠ 1 := fun hc => hne (by linarith)
    have hne3 : (t * 2)⁻¹ ≠ 1 := by
      intro hc
      apply hne2
      have h4 : (t * 2) * (t * 2)⁻¹ = 1 := mul_inv_cancel₀ (ne_of_gt h2)
      rwa [hc, mul_one] at h4
    have hinv := Real.log_lt_sub_one_of_pos (inv_pos.mpr h2) hne3
    rw [Real.log_inv] at hinv
    have hstep : 1 - (t * 2)⁻¹ < Real.log (t * 2) := by linarith
    have hmul := mul_lt_mul_of_pos_left hstep h
    have hcalc : t * (1 - (t * 2)⁻¹) = t - 1 / 2 := by field_simp; ring
    linarith

/-- THE ODD SECTOR PAYS. Any nonzero Jarlskog coordinate buys strictly positive
    whole-only share. Two applications of the strict Gibbs stone, one at each of
    the family's two weights. -/
theorem cpShare_pos {J : ℝ} (hJ : |J| ≤ 1) (hne : J ≠ 0) : 0 < cpShare J := by
  obtain ⟨hlo, hhi⟩ := abs_le.mp hJ
  have ha : (0 : ℝ) ≤ (1 + J) / 2 := by linarith
  have hb : (0 : ℝ) ≤ (1 - J) / 2 := by linarith
  have hane : (1 + J) / 2 ≠ 1 / 2 := fun h => hne (by linarith)
  have hbne : (1 - J) / 2 ≠ 1 / 2 := fun h => hne (by linarith)
  have h1 := sub_half_lt_mul_log ha hane
  have h2 := sub_half_lt_mul_log hb hbne
  rw [show (1 + J) / 2 * 2 = 1 + J by ring] at h1
  rw [show (1 - J) / 2 * 2 = 1 - J by ring] at h2
  rw [cpShare]
  linarith

/-! ### The bridge -/

/-- **THE BRIDGE, EVEN SIDE.** At vanishing CP phase the member is sign-symmetric
    and its whole-only share is exactly zero — by composition with
    `share_eq_zero_of_signSymmetric`, the same lemma that kills the zero-field
    Ising family at every temperature. No hypothesis on the mixing angles: the
    T-even member has no whole-only structure however strongly mixed. -/
theorem share_zero_of_cp_even {J : ℝ} (hJ : J = 0) : share (cpState J) = 0 :=
  share_eq_zero_of_signSymmetric (cpState_isProb (by rw [hJ]; norm_num))
    (cpState_signSymmetric_iff.mpr hJ)

/-- **THE BRIDGE, ODD SIDE.** A nonzero Jarlskog coordinate gives strictly
    positive whole-only share. -/
theorem share_pos_of_cp_odd {J : ℝ} (hJ : |J| ≤ 1) (hne : J ≠ 0) :
    0 < share (cpState J) := by
  rw [share_cpState hJ]
  exact cpShare_pos hJ hne

/-- **THE TWO VANISHINGS ARE ONE VANISHING.** On this family the whole-only
    share is zero exactly where the Jarlskog coordinate is zero, which is exactly
    where the state is sign-symmetric. `Core.Flavor`'s CP-even condition and
    `Core.SignSymmetry`'s hypothesis pick out the same member. -/
theorem share_cpState_eq_zero_iff {J : ℝ} (hJ : |J| ≤ 1) :
    share (cpState J) = 0 ↔ J = 0 := by
  constructor
  · intro h
    by_contra hne
    exact absurd h (ne_of_gt (share_pos_of_cp_odd hJ hne))
  · exact share_zero_of_cp_even

/-- The CP-symmetrized member carries no whole-only share, whatever the phase it
    was symmetrized from. -/
theorem share_symmetrize_cpState (J : ℝ) : share (symmetrize (cpState J)) = 0 := by
  rw [symmetrize_cpState]
  exact share_indep

/-! ### Concavity, and the composition with the Jarlskog ceiling

The family is AFFINE in `J`, so scaling the phase down is literally mixing with
the uniform state. Concavity of the entropy therefore turns the Jarlskog
envelope bound into a bound on the share — with the phase damping carried
through. Two general stones are needed and neither was in the repository. -/

/-- TWO-POINT JENSEN FOR `t·log t`, at general weights. The midpoint case is
    `Core.SignSymmetry`'s `mul_log_mix`; this is the same `log x ≤ x − 1` stone
    applied at each endpoint against the mixture, and it is what makes the
    entropy concave. -/
theorem mul_log_convex {a b t : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) (ht0 : 0 ≤ t)
    (ht1 : t ≤ 1) :
    (t * a + (1 - t) * b) * Real.log (t * a + (1 - t) * b)
      ≤ t * (a * Real.log a) + (1 - t) * (b * Real.log b) := by
  have ht1' : (0 : ℝ) ≤ 1 - t := by linarith
  have hm : 0 ≤ t * a + (1 - t) * b :=
    add_nonneg (mul_nonneg ht0 ha) (mul_nonneg ht1' hb)
  rcases hm.eq_or_lt with hm0 | hmpos
  · have hta : t * a = 0 := by
      have h1 : 0 ≤ t * a := mul_nonneg ht0 ha
      have h2 : 0 ≤ (1 - t) * b := mul_nonneg ht1' hb
      linarith
    have htb : (1 - t) * b = 0 := by
      have h1 : 0 ≤ t * a := mul_nonneg ht0 ha
      linarith
    have hA : t * (a * Real.log a) = 0 := by
      rcases mul_eq_zero.mp hta with h | h <;> rw [h] <;> simp
    have hB : (1 - t) * (b * Real.log b) = 0 := by
      rcases mul_eq_zero.mp htb with h | h <;> rw [h] <;> simp
    rw [← hm0, hA, hB]
    simp
  · have h1 := mul_log_sub_le ha hm (fun _ => hmpos)
    have h2 := mul_log_sub_le hb hm (fun _ => hmpos)
    have h1' := mul_le_mul_of_nonneg_left h1 ht0
    have h2' := mul_le_mul_of_nonneg_left h2 ht1'
    have key : t * (a * Real.log (t * a + (1 - t) * b) - a * Real.log a)
        + (1 - t) * (b * Real.log (t * a + (1 - t) * b) - b * Real.log b)
        = (t * a + (1 - t) * b) * Real.log (t * a + (1 - t) * b)
          - (t * (a * Real.log a) + (1 - t) * (b * Real.log b)) := by ring
    have key2 : t * ((t * a + (1 - t) * b) - a) + (1 - t) * ((t * a + (1 - t) * b) - b)
        = 0 := by ring
    linarith

/-- THE ENTROPY IS CONCAVE. Mixing two states never destroys entropy; the
    mixture carries at least the average. Summed from `mul_log_convex`. -/
theorem entropy_concave {α : Type*} [Fintype α] {p q : α → ℝ}
    (hp : ∀ x, 0 ≤ p x) (hq : ∀ x, 0 ≤ q x) {t : ℝ} (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    t * entropy p + (1 - t) * entropy q
      ≤ entropy (fun x => t * p x + (1 - t) * q x) := by
  have h := Finset.sum_le_sum fun x (_ : x ∈ Finset.univ) =>
    mul_log_convex (hp x) (hq x) ht0 ht1
  rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum] at h
  unfold entropy
  linarith

/-- THE FAMILY IS AFFINE IN THE PHASE. Damping the Jarlskog coordinate by a
    factor `t` is exactly mixing the member with the uniform state. This is why
    the ceiling composes. -/
theorem cpState_mix (M t : ℝ) :
    (fun x => t * cpState M x + (1 - t) * indep x) = cpState (t * M) := by
  funext x
  simp only [cpState, indep, parityChar]
  ring

/-- THE PHASE DAMPS THE SHARE, linearly at worst: scaling the Jarlskog
    coordinate by `t ∈ [0,1]` scales the share down by at least `t`. Concavity
    of the entropy along the family's affine line. -/
theorem cpShare_mul_le {M t : ℝ} (hM : |M| ≤ 1) (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    cpShare (t * M) ≤ t * cpShare M := by
  have hTM : |t * M| ≤ 1 := by
    rw [abs_mul, abs_of_nonneg ht0]
    calc t * |M| ≤ 1 * |M| := mul_le_mul_of_nonneg_right ht1 (abs_nonneg M)
      _ = |M| := one_mul _
      _ ≤ 1 := hM
  have hc := entropy_concave (cpState_isProb hM).1 indep_isProb.1 ht0 ht1
  rw [cpState_mix, entropy_cpState hTM, entropy_cpState hM, entropy_indep'] at hc
  nlinarith [hc]

/-! ### The Jarlskog coordinate lands inside the simplex -/

private lemma abs_mul_le_one {x y : ℝ} (hx : |x| ≤ 1) (hy : |y| ≤ 1) : |x * y| ≤ 1 := by
  rw [abs_mul]
  calc |x| * |y| ≤ |x| * 1 := mul_le_mul_of_nonneg_left hy (abs_nonneg x)
    _ ≤ 1 := by rw [mul_one]; exact hx

private lemma abs_cos_sq_le_one (θ : ℝ) : |(cos θ) ^ 2| ≤ 1 := by
  rw [show (cos θ) ^ 2 = cos θ * cos θ by ring]
  exact abs_mul_le_one (abs_cos_le_one θ) (abs_cos_le_one θ)

/-- The Jarlskog invariant is a product of sines, cosines and one squared cosine
    — every factor of magnitude at most one — so it lands inside the family's
    simplex. The substitution in `cpFamily` is therefore legitimate at every
    angle and every phase, with no octant hypothesis. -/
theorem abs_jarlskog_le_one (θ12 θ23 θ13 δ : ℝ) : |jarlskog θ12 θ23 θ13 δ| ≤ 1 := by
  unfold jarlskog
  exact abs_mul_le_one (abs_mul_le_one (abs_mul_le_one (abs_mul_le_one
    (abs_mul_le_one (abs_mul_le_one (abs_cos_le_one _) (abs_sin_le_one _))
      (abs_cos_le_one _)) (abs_sin_le_one _)) (abs_cos_sq_le_one _))
    (abs_sin_le_one _)) (abs_sin_le_one _)

/-- The angle envelope lands inside the simplex too — it is `jarlskog` at
    maximal phase. -/
theorem abs_jarlskogMax_le_one (θ12 θ23 θ13 : ℝ) : |jarlskogMax θ12 θ23 θ13| ≤ 1 := by
  have h := abs_jarlskog_le_one θ12 θ23 θ13 (π / 2)
  rwa [show jarlskog θ12 θ23 θ13 (π / 2) = jarlskogMax θ12 θ23 θ13 by
    unfold jarlskog jarlskogMax; rw [sin_pi_div_two]; ring] at h

/-! ### The composition: the Jarlskog ceiling becomes a ceiling on the share -/

private lemma cpShare_jarlskog (θ12 θ23 θ13 δ : ℝ) :
    cpShare (jarlskog θ12 θ23 θ13 δ)
      = cpShare (|sin δ| * jarlskogMax θ12 θ23 θ13) := by
  have hfac : jarlskog θ12 θ23 θ13 δ = jarlskogMax θ12 θ23 θ13 * sin δ := by
    unfold jarlskog jarlskogMax; ring
  rcases le_or_lt 0 (sin δ) with h | h
  · rw [hfac, abs_of_nonneg h, mul_comm]
  · rw [hfac, abs_of_neg h,
      show jarlskogMax θ12 θ23 θ13 * sin δ
        = -(-sin δ * jarlskogMax θ12 θ23 θ13) by ring, cpShare_neg]

/-- **THE CEILING COMPOSES, with the phase carried through.** The family's
    whole-only share obeys the closed form evaluated at `abs_jarlskog_le_max`'s
    own angle envelope, damped by `|sin δ|`. This is the share's version of the
    Jarlskog bound: the mixing angles set the ceiling, and only maximal phase
    reaches it.

    It needs NO octant hypothesis, unlike `abs_jarlskog_le_max` itself, and the
    reason is worth recording rather than leaving to be rediscovered: the closed
    form is EVEN (`cpShare_neg`), so it reads the envelope's magnitude and never
    its sign. The octant is what makes `jarlskogMax` nonnegative, and nothing
    here needs that. -/
theorem share_cpFamily_le_phase (θ12 θ23 θ13 δ : ℝ) :
    share (cpFamily θ12 θ23 θ13 δ)
      ≤ |sin δ| * cpShare (jarlskogMax θ12 θ23 θ13) := by
  rw [cpFamily, share_cpState (abs_jarlskog_le_one θ12 θ23 θ13 δ), cpShare_jarlskog]
  exact cpShare_mul_le (abs_jarlskogMax_le_one θ12 θ23 θ13) (abs_nonneg _)
    (abs_sin_le_one δ)

/-- The same ceiling with the phase dropped: the family's share never exceeds
    the closed form at the angle envelope. The mixing angles alone cap the
    whole-only structure the phase can buy. -/
theorem share_cpFamily_le_jarlskogMax (θ12 θ23 θ13 δ : ℝ) :
    share (cpFamily θ12 θ23 θ13 δ) ≤ cpShare (jarlskogMax θ12 θ23 θ13) := by
  have hle := share_cpFamily_le_phase θ12 θ23 θ13 δ
  have hnn : 0 ≤ cpShare (jarlskogMax θ12 θ23 θ13) :=
    cpShare_nonneg (abs_jarlskogMax_le_one θ12 θ23 θ13)
  have hs : |sin δ| ≤ 1 := abs_sin_le_one δ
  nlinarith [hle, hnn, hs, abs_nonneg (sin δ)]

/-- **THE BRIDGE, ODD SIDE OFF — in flavour coordinates.** At vanishing CP phase
    the member of the family is sign-symmetric and its whole-only share is
    exactly zero, however strong the mixing. This is `share_zero_of_cp_even`
    composed through `jarlskog = J_max · sin δ`: `Core.Flavor`'s CP-conserving
    condition delivers `Core.SignSymmetry`'s hypothesis, and that lemma — the one
    that kills the whole zero-field Ising family at every temperature — closes
    it. The two vanishing theorems this repository carried separately are, on
    this model, the same theorem. -/
theorem share_cpFamily_zero_of_cp_even (θ12 θ23 θ13 δ : ℝ) (hδ : sin δ = 0) :
    share (cpFamily θ12 θ23 θ13 δ) = 0 := by
  have hJ : jarlskog θ12 θ23 θ13 δ = 0 := by
    unfold jarlskog; rw [hδ]; ring
  rw [cpFamily]
  exact share_zero_of_cp_even hJ

/-- The same at the level of the state, so the middle step is visible rather
    than inferred: at vanishing CP phase the member IS sign-symmetric. -/
theorem cpFamily_signSymmetric_of_cp_even (θ12 θ23 θ13 δ : ℝ) (hδ : sin δ = 0) :
    SignSymmetric (cpFamily θ12 θ23 θ13 δ) := by
  rw [cpFamily]
  refine cpState_signSymmetric_iff.mpr ?_
  unfold jarlskog; rw [hδ]; ring

/-- **THE ALIGNED POLE IS SHARED.** Where any mixing angle vanishes the Jarlskog
    envelope is zero (`jarlskogMax_zero_at_no_mixing`), so the family's
    whole-only share is exactly zero however large the CP phase. The no-mixing
    pole of `Core.Flavor` and the sign-symmetric locus of `Core.SignSymmetry`
    are the same place. -/
theorem share_cpFamily_zero_at_no_mixing (θ12 θ23 θ13 δ : ℝ)
    (h : θ12 = 0 ∨ θ23 = 0 ∨ θ13 = 0) : share (cpFamily θ12 θ23 θ13 δ) = 0 := by
  have hJ : jarlskog θ12 θ23 θ13 δ = 0 := by
    have hfac : jarlskog θ12 θ23 θ13 δ = jarlskogMax θ12 θ23 θ13 * sin δ := by
      unfold jarlskog jarlskogMax; ring
    rw [hfac, jarlskogMax_zero_at_no_mixing θ12 θ23 θ13 h, zero_mul]
  rw [cpFamily]
  exact share_zero_of_cp_even hJ

/-- The maximal-mixing endpoint carries no share either: at `θ₁₃ = π/2` the
    envelope vanishes, so CP violation and whole-only share vanish together at
    BOTH ends of the mixing range. -/
theorem share_cpFamily_zero_at_max_13mixing (θ12 θ23 δ : ℝ) :
    share (cpFamily θ12 θ23 (π / 2) δ) = 0 := by
  have hJ : jarlskog θ12 θ23 (π / 2) δ = 0 := by
    have hfac : jarlskog θ12 θ23 (π / 2) δ = jarlskogMax θ12 θ23 (π / 2) * sin δ := by
      unfold jarlskog jarlskogMax; ring
    rw [hfac, jarlskogMax_zero_at_max_13mixing θ12 θ23, zero_mul]
  rw [cpFamily]
  exact share_zero_of_cp_even hJ

/-- **THE ODD SIDE, IN FLAVOUR COORDINATES.** Wherever the mixing envelope is
    nonzero and the phase is nonzero, the family carries strictly positive
    whole-only share. With `share_cpFamily_zero_at_no_mixing` and
    `share_cpFamily_zero_at_max_13mixing` this is the full bridge in the
    parametrization `Core.Flavor` uses: the share is positive exactly where the
    Jarlskog invariant is, and zero exactly where it is. -/
theorem share_cpFamily_pos {θ12 θ23 θ13 δ : ℝ}
    (hmax : jarlskogMax θ12 θ23 θ13 ≠ 0) (hδ : sin δ ≠ 0) :
    0 < share (cpFamily θ12 θ23 θ13 δ) := by
  have hJ : jarlskog θ12 θ23 θ13 δ ≠ 0 := by
    have hfac : jarlskog θ12 θ23 θ13 δ = jarlskogMax θ12 θ23 θ13 * sin δ := by
      unfold jarlskog jarlskogMax; ring
    rw [hfac]
    exact mul_ne_zero hmax hδ
  rw [cpFamily]
  exact share_pos_of_cp_odd (abs_jarlskog_le_one θ12 θ23 θ13 δ) hJ

/-- **THE BRIDGE IN ONE LINE, in flavour coordinates.** The family's whole-only
    share vanishes if and only if the Jarlskog invariant does. Everything above
    composes to this: on this model, "CP-conserving" and "no structure above the
    pairs" are the same condition. -/
theorem share_cpFamily_eq_zero_iff (θ12 θ23 θ13 δ : ℝ) :
    share (cpFamily θ12 θ23 θ13 δ) = 0 ↔ jarlskog θ12 θ23 θ13 δ = 0 := by
  rw [cpFamily]
  exact share_cpState_eq_zero_iff (abs_jarlskog_le_one θ12 θ23 θ13 δ)

/-- THE SPAN IS FULL, so the closed form is not a statement about small numbers:
    at maximal Jarlskog coordinate the family IS a parity state and its share is
    exactly one bit — the same `log 2` that `share_parity` reads and that
    `Core.ShareK`'s classical cap allows at `k = 3`. -/
theorem cpShare_one : cpShare 1 = Real.log 2 := by
  norm_num [cpShare]

theorem share_cpState_one : share (cpState 1) = Real.log 2 := by
  rw [share_cpState (by norm_num), cpShare_one]

/-- THE FAMILY MEETS THE REPOSITORY'S ANCHOR STATE. At maximal CP-odd
    coordinate the member IS the parity state of `Core.Third` — the tilt puts
    all the weight on the four cells where the third bit is the XOR of the first
    two. So the family is not a new object bolted alongside the old one; it is a
    line through it. -/
theorem cpState_neg_one : cpState (-1) = parity := by
  funext t
  obtain ⟨a, b, c⟩ := t
  cases a <;> cases b <;> cases c <;> simp [cpState, parityChar, pm, parity] <;> norm_num

/-- THE CROSS-CHECK, and it is a real one: the closed form evaluated at maximal
    CP-odd coordinate must reproduce `share_parity`, which this repository proved
    earlier by an entirely different route. It does — `cpShare (−1) = log 2` and
    `share parity = log 2`, the same number by two independent computations. -/
theorem share_parity_eq_cpShare : share parity = cpShare (-1) := by
  rw [← cpState_neg_one]
  exact share_cpState (by norm_num)

end CIRISOntology.Core
