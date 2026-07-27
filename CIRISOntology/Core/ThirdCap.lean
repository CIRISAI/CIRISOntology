/-
CIRISOntology.Core.ThirdCap — THE DENOMINATOR: three binary slots cannot carry
more than one bit of whole-only share, with NO hypothesis on the pair data.

WHY THIS FILE EXISTS, AND WHY NOW. Four running campaigns (glass, Planck CMB,
eBOSS, and the Dalitz record) report every reading as a CEILING FRACTION —
measured whole-only share divided by `log 2` for three binary slots. The Planck
pilot audited that denominator's provenance and found the repository did not
prove what was being claimed. What was actually here:

  * `Core.Share.share_parity` — ATTAINMENT, exact: the parity state reads
    exactly `log 2`. So the value is REACHED.
  * `Core.ShareK.shareK_le_of_pair_uniform` — a cap of `(k−2)·log 2`, which at
    k = 3 reads `log 2` — but it HYPOTHESISES `pairMarg i j p = fun _ => 1/4`.
    No correlated real table satisfies that, so on measured data it does not
    apply.
  * `Core.ShareK.shareK_le_log_sub_pair` — the general cap
    `share ≤ k·log 2 − H(pair marginal)`, which at k = 3 is LOOSER than `log 2`
    whenever no pair marginal is uniform — i.e. on every real table.

So the denominator every campaign divides by was argued, not proved. This file
proves it, and the proof needs no hypothesis at all beyond `IsProb`.

WHAT IS PROVED HERE (machine-checked, hypotheses exactly as stated):

  * `entropy_marg₁₂_le` — MARGINAL MONOTONICITY for the pair view: a state's
    (1,2) marginal never carries more entropy than the state. The pointwise
    argument of `Core.ShareK.entropy_map_le`, stated directly in the `α×β×γ`
    formulation so no pushforward bridge is needed.
  * `marg₃_eq_of_samePairs`, `marg₃_isProb` — pair data fixes single data, so
    every competitor in the envelope carries the state's THIRD marginal too.
  * `share_le_pair_third_gap` — the SHARP, DATA-COMPUTABLE ceiling:
    `share p ≤ H(marg₁₂ p) + H(marg₃ p) − H(p)`. Every term on the right is a
    number a campaign can compute from its own table, and it is never worse
    than `log 2`. Campaigns that want a tighter denominator than the universal
    one should quote this; `share_le_grouping_gaps` gives all three slot
    orientations, so the honest ceiling is their minimum.
  * `share_le_log_card_third` — `share p ≤ log (card γ)`: the whole-only share
    of a three-slot state is capped by the log of the alphabet of the slot
    played off against the pair. General alphabets, not just bits.
  * `share_le_log_two` — THE TARGET. For three BINARY slots,
    `share p ≤ Real.log 2`, for EVERY probability state, with no hypothesis on
    the pair marginals.
  * `share_max_eq_log_two` — the two halves cashed together: the parity state
    reaches `log 2` and nothing exceeds it. `log 2` is the exact maximum of the
    whole-only share on three bits. THIS is the denominator.

WHAT REMAINS ARGUED, NOT PROVED — do not let the campaigns round this up:

  * Nothing about k > 3 improves here. At four slots and up the cap in force is
    `Core.HammingCap.shareK_le_of_four_pair_uniform` ((k−3)·log 2, and it DOES
    hypothesise four pair-uniform slots), with the tiers stated in that file.
    This file is k = 3 only.
  * `share_le_log_card_third` is stated against the THIRD slot's alphabet, so
    on unequal alphabets it is the third slot's bound, not the smallest slot's.
    The symmetric statements follow by reindexing (`Core.Creation.swap₁₃`,
    `swap₂₃`), but the general min-over-slots form is NOT mechanized here.
    `share_le_grouping_gaps` does mechanize all three orientations of the
    SHARP bound, at three binary slots only. Nothing on the page depends on the
    distinction: on three BINARY slots every orientation reads `log 2`.
  * That any process in nature carries a nonzero share is not touched by this
    file and is not proved anywhere.

ROUTE — AND A DEVIATION FROM THE BRIEF, STATED PLAINLY. This brick was briefed
to go through Shearer's inequality at k = 3
(`2·H(XYZ) ≤ H(XY) + H(XZ) + H(YZ)`) applied to the envelope maximizer. That
route is sound and was verified numerically alongside this one, but it is not
needed: at three slots the ONE-sided grouping bound already closes the problem.
For any competitor `q` in the envelope,

    H(q)  ≤  H(q₁₂) + H(q₃)          (grouping subadditivity, `entropy_grouping`)
          =  H(p₁₂) + H(p₃)          (q shares p's pair data, hence its single data)
          ≤  H(p)   + log |γ|        (marginal monotonicity; Gibbs on ONE slot)

so the whole envelope sits within `log |γ|` of `H(p)`, and the share — the
envelope's top minus `H(p)` — is at most `log |γ|`. Two stones, both already in
the repository. Shearer's inequality is not used and is not proved here; it
would be the right tool at k > 3, where no single grouping closes the gap.

CREDIT. Nothing in the underlying mathematics is ours. Grouping subadditivity
and the Gibbs bound are textbook (Cover & Thomas, *Elements of Information
Theory*, Thms 2.6.6 and 2.6.4). Shearer's inequality — the briefed route, not
taken — is Chung, Frankl, Graham & Shearer (*J. Combin. Theory Ser. A* 43:23,
1986), with the entropy form usually credited to Radhakrishnan. The maximum-
entropy-under-pair-constraints construction is Schneidman, Still, Berry &
Bialek (2003), as recorded in `Core.Share`. Ours is the mechanization, the
composition with the envelope, and the fact that at k = 3 the one-sided bound
suffices.

NUMERICAL PRE-CHECK. Run before any Lean was attempted, on 10⁶ random
three-bit states across four regimes (flat, sparse, spiky, and uniform-on-a-
random-support), with the EXACT k = 3 envelope solver — in the sign basis the
pair data fixes six of the seven parameters and the triple correlator is the
single free direction, so the envelope maximum is a golden section on a scalar,
not an IPF fit. Every check held with no violation; the largest share found
anywhere in the sample was `log 2` itself, to 6e-16, at the odd-parity state —
so the cap is not merely valid but tight, independently of the Lean. Script and
log: `scratchpad/temporal-share/SHEARER_NUMERIC.py` (`.log`).

Mathlib survey: `csSup_le` against the envelope's own member for the supremum;
`Real.log_le_log` for the pointwise comparison; `Finset.sum_comm` for the
marginal bookkeeping. Everything else is `Core.Share` / `Core.Creation`
machinery. No gaps to port.
-/
import CIRISOntology.Core.Creation

namespace CIRISOntology.Core

open scoped BigOperators

/-! ### Marginal monotonicity for the pair view -/

/-- MARGINAL MONOTONICITY: the (1,2) pair view of a three-slot state never
    carries more entropy than the state itself. Pointwise, as in
    `Core.ShareK.entropy_map_le`: a marginal cell always outweighs each joint
    cell inside it, so `log` compares termwise and the sums follow. Stated
    directly on `marg₁₂` so the envelope machinery needs no pushforward
    bridge, and no `DecidableEq`. -/
theorem entropy_marg₁₂_le {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    {p : α × β × γ → ℝ} (hp : IsProb p) :
    entropy (marg₁₂ p) ≤ entropy p := by
  obtain ⟨h0, -⟩ := hp
  have hle : ∀ a b c, p (a, b, c) ≤ marg₁₂ p (a, b) := fun a b c =>
    Finset.single_le_sum (fun c' _ => h0 (a, b, c')) (Finset.mem_univ c)
  have hgroup : ∑ ab : α × β, marg₁₂ p ab * Real.log (marg₁₂ p ab)
      = ∑ t : α × β × γ, p t * Real.log (marg₁₂ p (t.1, t.2.1)) := by
    simp only [Fintype.sum_prod_type]
    refine Finset.sum_congr rfl fun a _ => Finset.sum_congr rfl fun b _ => ?_
    rw [← Finset.sum_mul]
    rfl
  have key : ∀ t : α × β × γ, p t * Real.log (p t)
      ≤ p t * Real.log (marg₁₂ p (t.1, t.2.1)) := by
    rintro ⟨a, b, c⟩
    rcases (h0 (a, b, c)).eq_or_lt with h | h
    · rw [← h]; simp
    · exact mul_le_mul_of_nonneg_left (Real.log_le_log h (hle a b c)) h.le
  have hsum : ∑ t : α × β × γ, p t * Real.log (p t)
      ≤ ∑ t : α × β × γ, p t * Real.log (marg₁₂ p (t.1, t.2.1)) :=
    Finset.sum_le_sum fun t _ => key t
  unfold entropy
  rw [hgroup]
  linarith

/-! ### Pair data fixes the third marginal -/

/-- A state's THIRD single-slot marginal is a function of its (2,3) pair
    marginal, so every competitor in the envelope carries it unchanged. The
    general-alphabet form of `Core.Creation.marg₃_of_samePairs`. -/
lemma marg₃_eq_of_samePairs {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    {p q : α × β × γ → ℝ} (h : SamePairs p q) : marg₃ q = marg₃ p := by
  funext c
  have hr : ∀ r : α × β × γ → ℝ, marg₃ r c = ∑ b, marg₂₃ r (b, c) :=
    fun _ => Finset.sum_comm
  rw [hr, hr, h.2.2]

/-- The third marginal of a probability state is a probability state. -/
lemma marg₃_isProb {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    {p : α × β × γ → ℝ} (hp : IsProb p) : IsProb (marg₃ p) := by
  obtain ⟨h0, h1⟩ := hp
  refine ⟨fun c => Finset.sum_nonneg fun a _ =>
    Finset.sum_nonneg fun b _ => h0 (a, b, c), ?_⟩
  have hsum : ∑ c, marg₃ p c = ∑ t : α × β × γ, p t := by
    simp only [marg₃, Fintype.sum_prod_type]
    rw [Finset.sum_comm]
    exact Finset.sum_congr rfl fun a _ => Finset.sum_comm
  rw [hsum, h1]

/-! ### The sharp ceiling, and the denominator -/

/-- THE SHARP CEILING, data-computable: a three-slot state's whole-only share
    is at most the amount by which its (1,2) pair reading and its third-slot
    reading, added, overshoot the state's own entropy. Every quantity on the
    right is measurable from the table itself, so a campaign can quote a
    tighter ceiling than the universal `log 2` whenever its data supports one.

    Proof in one line: every competitor in the envelope has the SAME pair data,
    hence the same third marginal, so grouping subadditivity caps the whole
    envelope at `H(p₁₂) + H(p₃)` — a number depending on `p` alone. -/
theorem share_le_pair_third_gap {α β γ : Type*}
    [Fintype α] [Fintype β] [Fintype γ]
    {p : α × β × γ → ℝ} (hp : IsProb p) :
    share p ≤ entropy (marg₁₂ p) + entropy (marg₃ p) - entropy p := by
  have hmem : entropy p ∈ pairEnvelope p := ⟨p, hp, ⟨rfl, rfl, rfl⟩, rfl⟩
  have hsup : sSup (pairEnvelope p)
      ≤ entropy (marg₁₂ p) + entropy (marg₃ p) := by
    refine csSup_le ⟨entropy p, hmem⟩ ?_
    rintro h ⟨q, hq, hsame, rfl⟩
    have hg := entropy_grouping hq
    rw [hsame.1, marg₃_eq_of_samePairs hsame] at hg
    exact hg
  unfold share
  linarith

/-- THE CAP, general alphabets: a three-slot state's whole-only share is at
    most the log of the THIRD slot's alphabet size. The pair reading is
    already inside the state's own entropy (marginal monotonicity), so the
    only headroom the pair data leaves open is one slot's worth of Gibbs. -/
theorem share_le_log_card_third {α β γ : Type*}
    [Fintype α] [Fintype β] [Fintype γ] [Nonempty γ]
    {p : α × β × γ → ℝ} (hp : IsProb p) :
    share p ≤ Real.log (Fintype.card γ) := by
  have h1 := share_le_pair_third_gap hp
  have h2 : entropy (marg₁₂ p) ≤ entropy p := entropy_marg₁₂_le hp
  have h3 := marg₃_isProb hp
  have h4 : entropy (marg₃ p) ≤ Real.log (Fintype.card γ) :=
    entropy_le_log_card h3.1 h3.2
  linarith

/-- THE DENOMINATOR, proved: three binary slots carry at most one bit of
    whole-only share — for EVERY probability state, with no hypothesis on the
    pair marginals. This is the number every ceiling-fraction divides by. -/
theorem share_le_log_two {p : Bool × Bool × Bool → ℝ} (hp : IsProb p) :
    share p ≤ Real.log 2 := by
  have h := share_le_log_card_third hp
  rwa [Fintype.card_bool, Nat.cast_ofNat] at h

/-- ATTAINED AND NOT EXCEEDED: `log 2` is the exact maximum of the whole-only
    share on three binary slots. The parity state reaches it
    (`Core.Share.share_parity`) and nothing crosses it (`share_le_log_two`).
    Before this, the repository had the first half and a cap that assumed
    uniform pair data for the second; the ceiling fraction now divides by a
    proved number. -/
theorem share_max_eq_log_two :
    share parity = Real.log 2
      ∧ ∀ q : Bool × Bool × Bool → ℝ, IsProb q → share q ≤ Real.log 2 :=
  ⟨share_parity, fun _ hq => share_le_log_two hq⟩

/-! ### All three slot orientations of the sharp ceiling -/

/-- The sharp ceiling in each of the three slot positions: pair against the
    third slot, against the second, against the first. A campaign's honest
    data-computable ceiling is the MINIMUM of these three; each is at most
    `log 2` on binary slots, and each can be far smaller. The other two
    orientations come from `Core.Creation`'s reindexed grouping bounds. -/
theorem share_le_grouping_gaps {p : Bool × Bool × Bool → ℝ} (hp : IsProb p) :
    share p ≤ entropy (marg₁₂ p) + entropy (marg₃ p) - entropy p
      ∧ share p ≤ entropy (marg₁₃ p) + entropy (marg₂ p) - entropy p
      ∧ share p ≤ entropy (marg₂₃ p) + entropy (marg₁ p) - entropy p := by
  have hmem : entropy p ∈ pairEnvelope p := ⟨p, hp, ⟨rfl, rfl, rfl⟩, rfl⟩
  refine ⟨share_le_pair_third_gap hp, ?_, ?_⟩
  · have hsup : sSup (pairEnvelope p)
        ≤ entropy (marg₁₃ p) + entropy (marg₂ p) := by
      refine csSup_le ⟨entropy p, hmem⟩ ?_
      rintro h ⟨q, hq, hsame, rfl⟩
      have hg := entropy_grouping₁₃ hq
      rw [hsame.2.1, marg₂_of_samePairs hsame] at hg
      exact hg
    unfold share
    linarith
  · have hsup : sSup (pairEnvelope p)
        ≤ entropy (marg₂₃ p) + entropy (marg₁ p) := by
      refine csSup_le ⟨entropy p, hmem⟩ ?_
      rintro h ⟨q, hq, hsame, rfl⟩
      have hg := entropy_grouping₂₃ hq
      rw [hsame.2.2, marg₁_of_samePairs hsame] at hg
      exact hg
    unfold share
    linarith

end CIRISOntology.Core
