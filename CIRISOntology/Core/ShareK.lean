/-
CIRISOntology.Core.ShareK — the whole-only share on k slots, and THE CLASSICAL
CAP: the Bell-style bound the hardware experiment is staked against.

`Core.Share` fixed three slots. This file generalizes the classical share to
k binary slots and proves the inequality every classical state obeys — the
"CHSH ≤ 2" of the Logos programme:

  * `pushforward`, `entropy_map_le` — THE ENGINE: coarse-graining never raises
    entropy. A marginal cell always outweighs each joint cell inside it, so
    the comparison is pointwise; no Gibbs machinery needed. This is the
    precise sense in which classical books are monotone: the whole always
    carries at least the entropy of any of its views.
  * `pairMarg`, `pairEnvelopeK`, `shareK` — the k-slot share, same
    variational form as `Core.Share`.
  * `shareK_le_log_sub_pair` — THE CAP, general form: for any classical
    k-slot state, share ≤ k·log 2 − H(any pair marginal). No uniformity
    assumed; the bound moves with the measured pair entropy.
  * `shareK_le_of_pair_uniform` — the headline form: a classical k-slot state
    with one uniform pair marginal has share ≤ (k − 2)·log 2. At k = 3 the
    parity state saturates this (its share is exactly log 2 = (3−2)·log 2,
    `Core.Share.share_parity`) — classical states can reach the cap, never
    cross it.
  * `pairPtr`, `qPairEnvelopeK`, `qShareK` (+ bddAbove, nonneg) — the k-slot
    quantum share, the functional the hardware claim is stated in.

WHY THIS IS A BELL STRUCTURE. Von Neumann entropy is NOT monotone under
partial trace: a pure entangled whole has S = 0 while its pair reductions
are maximally mixed. The five-qubit ring graph state (AME(5,2), which
exists) is pure with every pair reduction maximally mixed, so its qShareK
is 5·log 2 — above the (5−2)·log 2 = 3·log 2 classical cap by 2·log 2. A
measured violation of `entropy_map_le`'s pattern (every pair reading MORE
entropy than the whole) is therefore something no classical 5-slot state
can produce. The cap is proved BEFORE the experiment; the threshold cannot
move after data.

SCOPE. Proved here: the items above, exact. NOT here, and said plainly: the
mechanized value qShareK(C5) = 5·log 2 (the ideal quantum ceiling — next
brick; the hardware claim needs only the cap), the tight classical maximum
(this cap is an upper bound; the best classical value we know is
2·log 2 at k = 5, via dual-distance-3 codes — exact-computed, not yet
mechanized), and any statement about what hardware actually holds.

Mathlib survey: `Finset.sum_fiberwise` carries the grouping;
`Real.log_le_log` the per-term comparison; the rest is `Core.Share` /
`Core.ShareQuantum` machinery. No gaps to port.
-/
import CIRISOntology.Core.ShareQuantum

namespace CIRISOntology.Core

open scoped BigOperators ComplexOrder
open Matrix

/-! ### The engine: coarse-graining never raises entropy -/

/-- The pushforward of a finite state along a map: the state of the view. -/
noncomputable def pushforward {X Y : Type*} [Fintype X] [DecidableEq Y]
    (π : X → Y) (p : X → ℝ) : Y → ℝ :=
  fun y => ∑ x ∈ Finset.univ.filter (fun x => π x = y), p x

/-- CLASSICAL BOOKS ARE MONOTONE: the entropy of any view is at most the
    entropy of the whole. Pointwise proof: a view cell always outweighs each
    whole cell inside it. This is the inequality the quantum experiment is
    designed to violate. -/
theorem entropy_map_le {X Y : Type*} [Fintype X] [Fintype Y] [DecidableEq Y]
    (π : X → Y) {p : X → ℝ} (hp : IsProb p) :
    entropy (pushforward π p) ≤ entropy p := by
  obtain ⟨h0, -⟩ := hp
  have hle : ∀ x, p x ≤ pushforward π p (π x) := fun x =>
    Finset.single_le_sum (fun x' _ => h0 x') (by simp)
  have hgroup : ∑ y, pushforward π p y * Real.log (pushforward π p y)
      = ∑ x, p x * Real.log (pushforward π p (π x)) := by
    rw [← Finset.sum_fiberwise Finset.univ π
      (fun x => p x * Real.log (pushforward π p (π x)))]
    refine Finset.sum_congr rfl fun y _ => ?_
    rw [Finset.sum_congr rfl (fun x hx => by
      rw [(Finset.mem_filter.mp hx).2]), ← Finset.sum_mul]
    rfl
  have key : ∀ x, p x * Real.log (p x)
      ≤ p x * Real.log (pushforward π p (π x)) := by
    intro x
    rcases (h0 x).eq_or_lt with h | h
    · rw [← h]; simp
    · exact mul_le_mul_of_nonneg_left (Real.log_le_log h (hle x)) h.le
  have hsum : ∑ x, p x * Real.log (p x)
      ≤ ∑ x, p x * Real.log (pushforward π p (π x)) :=
    Finset.sum_le_sum fun x _ => key x
  unfold entropy
  rw [hgroup]
  linarith

/-! ### The k-slot share and the cap -/

variable {k : ℕ}

/-- The (i, j) pair marginal of a k-slot state. -/
noncomputable def pairMarg (i j : Fin k) (p : (Fin k → Bool) → ℝ) :
    Bool × Bool → ℝ :=
  pushforward (fun x => (x i, x j)) p

/-- The pair envelope: entropies of all probability states carrying exactly
    the same pair marginals, at every pair of slots. -/
def pairEnvelopeK (p : (Fin k → Bool) → ℝ) : Set ℝ :=
  { h | ∃ q, IsProb q ∧ (∀ i j : Fin k, pairMarg i j q = pairMarg i j p)
        ∧ entropy q = h }

/-- The whole-only share of a k-slot state. -/
noncomputable def shareK (p : (Fin k → Bool) → ℝ) : ℝ :=
  sSup (pairEnvelopeK p) - entropy p

/-- THE CAP, general form: a classical k-slot state's share is at most
    k·log 2 minus the entropy of ANY of its pair marginals. The bound is
    stated against the measured pair entropy, so no uniformity assumption is
    needed on hardware. -/
theorem shareK_le_log_sub_pair (i j : Fin k) {p : (Fin k → Bool) → ℝ}
    (hp : IsProb p) :
    shareK p ≤ Real.log (Fintype.card (Fin k → Bool))
      - entropy (pairMarg i j p) := by
  have hmem : entropy p ∈ pairEnvelopeK p := ⟨p, hp, fun _ _ => rfl, rfl⟩
  have h1 : sSup (pairEnvelopeK p) ≤ Real.log (Fintype.card (Fin k → Bool)) := by
    refine csSup_le ⟨entropy p, hmem⟩ ?_
    rintro h ⟨q, hq, -, rfl⟩
    exact entropy_le_log_card hq.1 hq.2
  have h2 : entropy (pairMarg i j p) ≤ entropy p := entropy_map_le _ hp
  unfold shareK
  linarith

private lemma log_quarter'' : Real.log ((1:ℝ)/4) = -(2 * Real.log 2) := by
  rw [one_div, show (4:ℝ) = 2 ^ 2 by norm_num, Real.log_inv, Real.log_pow]
  norm_num

private lemma entropy_uniform_pair :
    entropy (fun _ : Bool × Bool => (1:ℝ)/4) = 2 * Real.log 2 := by
  unfold entropy
  simp only [Fintype.sum_prod_type, Fintype.sum_bool]
  norm_num [log_quarter'']
  ring

private lemma log_card_pow :
    Real.log (Fintype.card (Fin k → Bool)) = (k : ℝ) * Real.log 2 := by
  have h : (Fintype.card (Fin k → Bool) : ℝ) = (2 : ℝ) ^ k := by
    rw [Fintype.card_fun]
    push_cast
    simp
  rw [h, Real.log_pow]

/-- THE CAP, headline form: a classical k-slot state with one uniform pair
    marginal has share at most (k − 2)·log 2. At k = 3 the parity state
    saturates this bound exactly (`share_parity`); at k = 5 the five-qubit
    ring state's quantum share of 5·log 2 sits 2·log 2 above it. -/
theorem shareK_le_of_pair_uniform (i j : Fin k) {p : (Fin k → Bool) → ℝ}
    (hp : IsProb p) (huni : pairMarg i j p = fun _ => (1:ℝ)/4) :
    shareK p ≤ ((k : ℝ) - 2) * Real.log 2 := by
  have h := shareK_le_log_sub_pair i j hp
  rw [huni, entropy_uniform_pair, log_card_pow] at h
  linarith

/-! ### The k-slot quantum share (the functional the hardware claim lives in) -/

/-- The (i, j) pair partial trace of a k-slot operator (meaningful for
    i ≠ j): trace out every slot except i and j. -/
noncomputable def pairPtr {𝕜 : Type*} [RCLike 𝕜] (i j : Fin k)
    (ρ : Matrix (Fin k → Bool) (Fin k → Bool) 𝕜) :
    Matrix (Bool × Bool) (Bool × Bool) 𝕜 :=
  Matrix.of fun bc bc' =>
    ∑ x ∈ Finset.univ.filter (fun x => x i = bc.1 ∧ x j = bc.2),
      ρ x (Function.update (Function.update x i bc'.1) j bc'.2)

/-- The quantum pair envelope on k slots: the von Neumann entropies of ALL
    densities carrying exactly the state's pair partial traces. -/
def qPairEnvelopeK {𝕜 : Type*} [RCLike 𝕜]
    (ρ : Matrix (Fin k → Bool) (Fin k → Bool) 𝕜) : Set ℝ :=
  { h | ∃ σ, IsDensity σ ∧ (∀ i j : Fin k, pairPtr i j σ = pairPtr i j ρ)
        ∧ vnEntropy σ = h }

/-- The whole-only share of a k-slot quantum state. -/
noncomputable def qShareK {𝕜 : Type*} [RCLike 𝕜]
    (ρ : Matrix (Fin k → Bool) (Fin k → Bool) 𝕜) : ℝ :=
  sSup (qPairEnvelopeK ρ) - vnEntropy ρ

theorem qPairEnvelopeK_bddAbove {𝕜 : Type*} [RCLike 𝕜]
    (ρ : Matrix (Fin k → Bool) (Fin k → Bool) 𝕜) :
    BddAbove (qPairEnvelopeK ρ) := by
  refine ⟨Real.log (Fintype.card (Fin k → Bool)), ?_⟩
  rintro h ⟨σ, hσ, -, rfl⟩
  exact vnEntropy_le_log_card hσ

theorem qShareK_nonneg {𝕜 : Type*} [RCLike 𝕜]
    {ρ : Matrix (Fin k → Bool) (Fin k → Bool) 𝕜} (hρ : IsDensity ρ) :
    0 ≤ qShareK ρ := by
  have hmem : vnEntropy ρ ∈ qPairEnvelopeK ρ := ⟨ρ, hρ, fun _ _ => rfl, rfl⟩
  have := le_csSup (qPairEnvelopeK_bddAbove ρ) hmem
  unfold qShareK
  linarith

end CIRISOntology.Core
