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
  * `qShareK_le_log_card` — THE QUANTUM CEILING: no k-slot quantum state's
    share exceeds k·log 2. Both terms bounded at once — the envelope's top by
    the quantum Gibbs bound, the subtracted entropy by `vnEntropy_nonneg`. The
    classical cap and this ceiling are the two sides of the Bell gap, and
    `Core.BellCeiling` shows the quantum side is EXACTLY tight at k = 5 while
    the classical side is not.

WHY THIS IS A BELL STRUCTURE. Von Neumann entropy is NOT monotone under
partial trace: a pure entangled whole has S = 0 while its pair reductions
are maximally mixed. The five-qubit ring graph state (AME(5,2), which
exists) is pure with every pair reduction maximally mixed, so its qShareK
is 5·log 2 — above the (5−2)·log 2 = 3·log 2 classical cap by 2·log 2. A
measured violation of `entropy_map_le`'s pattern (every pair reading MORE
entropy than the whole) is therefore something no classical 5-slot state
can produce. The cap is proved BEFORE the experiment; the threshold cannot
move after data.

SCOPE. Proved here: the items above, exact. Since written, two of the three
gaps below have closed: the ideal quantum ceiling qShareK(C5) = 5·log 2 IS
now mechanized (`Core.BellCeiling`), and the true classical maximum at k = 5
is now known exactly — it is 2·log 2, attained by the uniform distribution on
any of 60 eight-point supports and by nothing else (exhaustive vertex
enumeration of the pair-uniform polytope, `scratchpad/temporal-share/
CLASSICAL_MAX_K5.md`; EXACT-COMPUTED, NOT MECHANIZED). Note the consequence,
and do not blur the tiers: THIS FILE'S cap (k−2)·log 2 = 3·log 2 is therefore
NOT TIGHT at k = 5. It has since been improved by one bit, and the improvement
IS machine-checked: `Core.HammingCap` proves (k−3)·log 2 for every k ≥ 4, which
at k = 5 reads 2·log 2 and so meets the enumerated true maximum exactly. Cite
that file, not this one, for anything at four slots or more; this file's cap
remains the exact statement at k = 3, where the parity state saturates it.
Still NOT proved anywhere: any statement about what hardware actually holds.

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

/-- THE QUANTUM CEILING, general form: no k-slot quantum state's whole-only
    share exceeds k·log 2 — the whole capacity of the k-slot space. Two stones,
    one per term: the envelope's top is at most log(card) by the quantum Gibbs
    bound (`vnEntropy_le_log_card`), and the state's own entropy, which is
    subtracted, is at least zero (`vnEntropy_nonneg`).

    This is the ceiling the CLASSICAL cap is measured against. At k = 5 the cap
    of `shareK_le_of_pair_uniform` is 3·log 2 and this ceiling is 5·log 2 —
    and `Core.BellCeiling`'s ring state ATTAINS the ceiling, so the quantum
    bound here is exactly tight while the classical one is not. -/
theorem qShareK_le_log_card {𝕜 : Type*} [RCLike 𝕜]
    {ρ : Matrix (Fin k → Bool) (Fin k → Bool) 𝕜} (hρ : IsDensity ρ) :
    qShareK ρ ≤ (k : ℝ) * Real.log 2 := by
  have hmem : vnEntropy ρ ∈ qPairEnvelopeK ρ := ⟨ρ, hρ, fun _ _ => rfl, rfl⟩
  have h1 : sSup (qPairEnvelopeK ρ) ≤ Real.log (Fintype.card (Fin k → Bool)) := by
    refine csSup_le ⟨vnEntropy ρ, hmem⟩ ?_
    rintro h ⟨σ, hσ, -, rfl⟩
    exact vnEntropy_le_log_card hσ
  rw [log_card_pow] at h1
  have h2 : 0 ≤ vnEntropy ρ := vnEntropy_nonneg hρ
  unfold qShareK
  linarith

/-! ### The classical third in time, complete

The `third-in-tsvf` programme's classical face, assembled: parity across
three times needs memory (`parity_needs_memory`), one remembered bit
realizes it (`memory_realizes_parity`), the pattern carries exactly `log 2`
of whole-only share (`share_parity`), and — the capstone below — `log 2` is
the MAXIMUM any classical three-slot state with its pair data can carry.
The quantum side cannot beat it in time (`vnEntropy_causal_past`,
`Core.EntropyIneq`). Time's third is habit-shaped as a matter of theorem:
memory fills the classical allowance, and causality is why there is no
other allowance. -/

/-- The (1,2)-pair view of a three-slot state, as a pushforward. -/
lemma pushforward_pair_parity :
    pushforward (fun t : Bool × Bool × Bool => (t.1, t.2.1)) parity
      = fun _ => (1 : ℝ)/4 := by
  funext ab
  obtain ⟨a, b⟩ := ab
  unfold pushforward
  rw [Finset.sum_filter]
  simp only [Fintype.sum_prod_type, Fintype.sum_bool]
  cases a <;> cases b <;> norm_num [parity]

/-- The deviation-robust 3-slot cap: a classical three-slot state's share is
    at most the log of the state space minus the entropy of its (1,2) view.
    The same two stones as `shareK_le_log_sub_pair`. -/
theorem share_le_log_sub_pair₃ {α β γ : Type*}
    [Fintype α] [Fintype β] [Fintype γ]
    [DecidableEq α] [DecidableEq β]
    [Nonempty α] [Nonempty β] [Nonempty γ]
    {p : α × β × γ → ℝ} (hp : IsProb p) :
    share p ≤ Real.log (Fintype.card (α × β × γ))
      - entropy (pushforward (fun t : α × β × γ => (t.1, t.2.1)) p) := by
  have hmem : entropy p ∈ pairEnvelope p := ⟨p, hp, ⟨rfl, rfl, rfl⟩, rfl⟩
  have h1 : sSup (pairEnvelope p) ≤ Real.log (Fintype.card (α × β × γ)) := by
    refine csSup_le ⟨entropy p, hmem⟩ ?_
    rintro h ⟨q, hq, -, rfl⟩
    exact entropy_le_log_card hq.1 hq.2
  have h2 := entropy_map_le (fun t : α × β × γ => (t.1, t.2.1)) hp
  unfold share
  linarith

/-- THE CLASSICAL THIRD IN TIME SATURATES ITS CAP: the parity pattern —
    realized across three times by one remembered bit — carries exactly
    `log 2` of whole-only share, and no classical three-slot state with
    uniform pair data can carry more. Together with `parity_needs_memory`,
    `memory_realizes_parity`, and `vnEntropy_causal_past`, this completes
    the formal characterization of time's third: built by memory, worth one
    bit, capped there by causality. -/
theorem temporal_third_saturates :
    share parity = Real.log 2
    ∧ ∀ q : Bool × Bool × Bool → ℝ, IsProb q →
        pushforward (fun t : Bool × Bool × Bool => (t.1, t.2.1)) q
          = (fun _ => (1 : ℝ)/4) →
        share q ≤ Real.log 2 := by
  refine ⟨share_parity, fun q hq hu => ?_⟩
  have h := share_le_log_sub_pair₃ hq
  rw [hu, entropy_uniform_pair, log_card_eight] at h
  linarith

end CIRISOntology.Core
