/-
CIRISOntology.Core.Valve — the one-way valve, as a theorem.

WHAT IS PROVED. Under STOCHASTIC PER-CELL channels — each slot pushed through
its own noise kernel, no kernel reading any other slot — order flows UP the
order hierarchy, never DOWN, and never FROM NOTHING. Three theorems on the
k = 3 binary model:

  * `valve_from_nothing` — NEVER FROM NOTHING. If the input is a product state,
    the output of any per-cell channel triple is a product state
    (`channel3_prod3`), and a product state's whole-only share is exactly zero
    (`share_prod3`). No amount of independent single-site noise, of any kind,
    on any product input, creates any whole-only share whatever. Stated again
    on the uniform state as `valve_from_nothing_indep`.

  * `valve_no_downward` — NEVER DOWNWARD. Push the parity state (whole-only
    order, every pair exactly independent) through ANY three per-cell kernels
    and all three pair marginals of the output are still exactly products of
    the output's own single-slot marginals. The whole-only habit may decay, and
    generically does, but its decay never deposits pairwise correlation. This
    is `marg₁₂_channel3_of_prod` and its two siblings — a pair marginal of the
    output is the input's pair marginal pushed through the two kernels
    concerned, so a product goes to a product — specialized at
    `parity_pair_independent_12/13/23`.

  * `valve_upward` — UPWARD FLOW EXISTS, exhibited. `ferro` (both bits-agree
    words, the T = 0 repetition-code ensemble) carries maximal PAIR order and,
    by `share_ferro`, whole-only share exactly zero. Push it through three
    copies of the γ = ½ amplitude-damping kernel and the output is the explicit
    rational state `bulge` — 9/16 on (F,F,F) and 1/16 on each of the other
    seven cells (`channel3_damp_ferro`) — whose whole-only share is STRICTLY
    POSITIVE. Per-cell noise, which cannot read any pair, moved order out of
    the pair sector and into the whole-only sector.

  * `valve_needs_asymmetry` — WHAT DRIVES THE PUMP, and it is not the noise.
    A FLIP-COVARIANT kernel — one that treats the two cell values alike, which
    on a normalized binary cell means exactly the binary symmetric channel —
    commutes with the global sign flip (`signSymmetric_channel3`), so it carries
    sign-symmetric states to sign-symmetric states and `share_eq_zero_of_signSymmetric`
    kills the whole family at once: share exactly zero, at any noise strength,
    from any sign-symmetric input, however strongly pair-correlated. The upward
    flow therefore REQUIRES a channel that breaks the flip symmetry. Damping
    breaks it (`damp_not_flipCovariant`), which is why `valve_upward` stands
    alongside this without tension. The odd sector is fed only by asymmetry.

THE ROUTE for the strict positivity, recorded because two were available and
only one was taken. The competitors carrying a given triple of pair marginals
on three bits form the line `p + t·χ`, where `χ` is the parity character (+1 on
the four even-parity cells, −1 on the four odd): χ sums to zero along every
pair fiber, which is exactly the pair-blindness computation `Core.Third` already
does for `parity`. The derivative route (differentiate `H(p + tχ)` at zero,
observe the slope is `−log 9 ≠ 0`) needs Mathlib's `hasDerivAt` plumbing; the
EXPLICIT-t route needs none, and is what closed here. At `t = −1/32` the
competitor is the explicit rational state `bulgeWitness` (17/32, three cells at
1/32, four at 3/32), its pair marginals are checked cell by cell against
`bulge`'s, and

    H(bulgeWitness) − H(bulge) = log 2 + (3/4)·log 3 − (17/32)·log 17 ≈ 0.01196

is positive because `17^17 < 2^32 · 3^24` — a comparison of two integers, which
`norm_num` settles. That number is a LOWER BOUND on the share
(`valve_upward_bound`), not the share: the exact optimum over `t` is
transcendental and is not computed here.

THE HARDWARE THIS MIRRORS. Measured on ibm_marrakesh (Heron), qubits 6-7-8, job
`d9in8jrjf64c739fprqg`, run 3 of the habit-lifecycle programme, pre-registered
in addendum 2 (commit `5d1780a`) before submission; 100 QPU seconds; readout
fidelity 0.9907, calibration drift 0.0009, no VOID. Three preparations, one
identical single-site noise process — idling:

  * the FERRO arm (pure pairwise order, share 0.00023 at t = 0) grew a
    whole-only bulge to 0.0541 nat at 49.5 µs while its pair covariances fell
    monotonically from ~0.99 to ~0.08 — up the hierarchy;
  * the INDEPENDENT-BITS arm stayed at 1.2 × 10⁻⁴ nat across 169 µs, the whole
    single-qubit error budget unable to move it — never from nothing;
  * the PARITY arm shed its whole-only share from 0.655 to 0.017 with its pair
    sector flat at 9 × 10⁻⁴ nat throughout, no pairwise bulge at any delay on
    any pair — never downward.

The bulge curve was tested against a prediction built from the same job's
measured per-qubit decays with ZERO free parameters and no functional form
assumed: χ² = 24.44 on 12 degrees of freedom (staked ≤ 32.21). Its peak
location (49.5 µs, staked 20.6-65.6 µs) and height (0.05405, staked
0.0433-0.0569) both landed inside their pre-registered bands. One criterion of
the five fired and stays fired: K-PAIRMULT reached 1.308 against a staked
[0.832, 1.176]; the record is `scratchpad/temporal-share/QPU_HABIT_RESULTS.md`,
and it reports the failure as loudly as the passes.

SCOPE, stated so the two cannot be confused. Everything below is a theorem
about the k = 3 BINARY MODEL under per-cell stochastic channels. It is not a
claim about hardware, and the hardware run is not evidence for it — the run is
this repository's own, from the same night, and it is what prompted asking
whether the model has this shape. Neither is a claim about nature's wild
processes.

THE BOUNDARY, load-bearing, and it must not be quoted loosely. **Nothing here
is a general data-processing inequality, and neither is `Core.Creation`'s
`percell_no_creation`. Do not cite either as one.** Both are proved for
SAME-ALPHABET per-cell maps: two-letter cells in, two-letter cells out. Within
that setting they are exact and they are sharp. ALPHABET-REDUCING per-cell maps
— coarse-graining, of which binarizing a larger-alphabet cell is the standard
case — are simply not covered. This file's kernels never change the alphabet at
all, and `percell_no_creation` runs on the dichotomy "every `Bool → Bool` is a
bijection or a constant", which is specific to two-letter cells: a map from
four letters to two is neither, so the argument as written does not reach it.
`Core.Creation`'s own header says so and this one repeats it, because the gap
is easy to lose and expensive to lose.

Whether a per-cell COARSE-GRAINING can genuinely create whole-only share is
therefore **open here**. The renormalization-group reading says it can, and the
question is under active empirical adjudication elsewhere in this programme
(the kappa-edge work). No theorem below bears on it in either direction, and a
later reading of this file must not treat the never-from-nothing and
never-downward legs as having settled it.

THE SHARPENING ACROSS TWO FILES, which is the point of this one.
`Core.Creation`'s `percell_no_creation` proves that a DETERMINISTIC per-cell map
can never raise the whole-only share — each factor is a bijection (a renaming,
share invariant) or a constant (a frozen slot, share zero). This file proves
that a STOCHASTIC per-cell channel CAN (`valve_upward`) — the dichotomy the
deterministic proof runs on simply does not exist for kernels, and a genuine
mixture is neither a renaming nor a freeze. But the stochastic gain is not free
and not general: it only ever feeds on order already present at a lower level
(`valve_from_nothing` — from independence, nothing comes), and it never runs the
other way (`valve_no_downward` — from the whole-only sector, nothing reaches the
pairs).

CREDIT. The multiplicative decay of correlations under independent single-site
noise is elementary probability. That mixing a state with per-cell noise can
CREATE higher-order interaction — the mechanism `valve_upward` exhibits — is
known: Kahle, Olbrich, Jost and Ay, "Complexity measures from interaction
structures", Phys. Rev. E 79, 026201 (2009), study exactly which interaction
orders a mixture can raise. The whole-only share itself is connected
information / max-entropy irreducible correlation (Schneidman-Still-Berry-Bialek
2003). What is ours here is the packaging as a valve with three separable
directions, machine-checked at k = 3, and the hardware arm that measured it.

Mathlib survey: `Real.log_lt_log` plus `norm_num` on an integer comparison
carries the witness inequality; `Equiv.prodAssoc` and this repository's
`entropy_reindex` carry the product-entropy identity; `le_csSup` against
`pairEnvelope_bddAbove` closes the supremum from below. No gaps to port.
-/
import CIRISOntology.Core.Creation

namespace CIRISOntology.Core

open scoped BigOperators

/-! ### Per-cell stochastic channels -/

/-- A stochastic kernel on one binary cell. `K y x` is the probability that the
    cell reads `y` on the way out given that it read `x` on the way in: entries
    nonnegative, and each INPUT's column of outcomes summing to one. -/
def IsKernel (K : Bool → Bool → ℝ) : Prop :=
  (∀ y x, 0 ≤ K y x) ∧ (∀ x, K true x + K false x = 1)

/-- One cell's state pushed through one cell's kernel. -/
noncomputable def push1 (K : Bool → Bool → ℝ) (p : Bool → ℝ) : Bool → ℝ :=
  fun y => ∑ x, K y x * p x

/-- THE PER-CELL CHANNEL on three binary slots: each slot is pushed through its
    own kernel, and no kernel reads any slot but its own. This is the stochastic
    counterpart of `Core.Creation`'s deterministic `percell`, and the model of
    the single-site noise the hardware arm idles under. -/
noncomputable def channel3 (K₁ K₂ K₃ : Bool → Bool → ℝ)
    (p : Bool × Bool × Bool → ℝ) : Bool × Bool × Bool → ℝ :=
  fun y => ∑ x : Bool × Bool × Bool,
    K₁ y.1 x.1 * K₂ y.2.1 x.2.1 * K₃ y.2.2 x.2.2 * p x

/-- A kernel's two rows are tied: knowing the `true` row fixes the `false` one.
    This is the form the column condition is spent in below — substituting it
    turns every channel-algebra goal into a polynomial identity. -/
private lemma kernel_false {K : Bool → Bool → ℝ} (hK : IsKernel K) (x : Bool) :
    K false x = 1 - K true x := by
  have := hK.2 x; linarith

lemma push1_isProb {K : Bool → Bool → ℝ} (hK : IsKernel K) {p : Bool → ℝ}
    (hp : IsProb p) : IsProb (push1 K p) := by
  refine ⟨fun y => Finset.sum_nonneg fun x _ => mul_nonneg (hK.1 y x) (hp.1 x), ?_⟩
  calc ∑ y, push1 K p y = ∑ x, (K true x + K false x) * p x := by
        simp only [push1, Fintype.sum_bool]; ring
    _ = ∑ x, p x := Finset.sum_congr rfl fun x _ => by rw [hK.2 x, one_mul]
    _ = 1 := hp.2

/-- A per-cell channel maps probability states to probability states. -/
theorem channel3_isProb {K₁ K₂ K₃ : Bool → Bool → ℝ} (hK₁ : IsKernel K₁)
    (hK₂ : IsKernel K₂) (hK₃ : IsKernel K₃) {p : Bool × Bool × Bool → ℝ}
    (hp : IsProb p) : IsProb (channel3 K₁ K₂ K₃ p) := by
  refine ⟨fun y => Finset.sum_nonneg fun x _ =>
    mul_nonneg (mul_nonneg (mul_nonneg (hK₁.1 _ _) (hK₂.1 _ _)) (hK₃.1 _ _)) (hp.1 x), ?_⟩
  calc ∑ y : Bool × Bool × Bool, channel3 K₁ K₂ K₃ p y
      = ∑ x : Bool × Bool × Bool,
          ((K₁ true x.1 + K₁ false x.1) * (K₂ true x.2.1 + K₂ false x.2.1)
            * (K₃ true x.2.2 + K₃ false x.2.2)) * p x := by
        simp only [channel3, Fintype.sum_prod_type, Fintype.sum_bool]; ring
    _ = ∑ x : Bool × Bool × Bool, p x :=
        Finset.sum_congr rfl fun x _ => by
          rw [hK₁.2 x.1, hK₂.2 x.2.1, hK₃.2 x.2.2]; ring
    _ = 1 := hp.2

/-! ### Never from nothing: a product in, a product out, share zero -/

/-- A product state on three binary slots: three independent cells. -/
noncomputable def prod3 (p₁ p₂ p₃ : Bool → ℝ) : Bool × Bool × Bool → ℝ :=
  fun t => p₁ t.1 * p₂ t.2.1 * p₃ t.2.2

/-- A PRODUCT IN, A PRODUCT OUT. Each kernel acts on its own factor and nothing
    couples them, so the channel maps the product of three cell states to the
    product of the three pushed cell states. No hypothesis on the kernels: this
    is an identity of sums. -/
theorem channel3_prod3 (K₁ K₂ K₃ : Bool → Bool → ℝ) (p₁ p₂ p₃ : Bool → ℝ) :
    channel3 K₁ K₂ K₃ (prod3 p₁ p₂ p₃)
      = prod3 (push1 K₁ p₁) (push1 K₂ p₂) (push1 K₃ p₃) := by
  funext y
  simp only [channel3, prod3, push1, Fintype.sum_prod_type, Fintype.sum_bool]
  ring

lemma isProb_prod2 {α β : Type*} [Fintype α] [Fintype β] {p₁ : α → ℝ} {p₂ : β → ℝ}
    (h₁ : IsProb p₁) (h₂ : IsProb p₂) : IsProb (fun ab : α × β => p₁ ab.1 * p₂ ab.2) := by
  refine ⟨fun ab => mul_nonneg (h₁.1 _) (h₂.1 _), ?_⟩
  simp only [Fintype.sum_prod_type]
  calc ∑ a, ∑ b, p₁ a * p₂ b = ∑ a, p₁ a * ∑ b, p₂ b :=
        Finset.sum_congr rfl fun a _ => (Finset.mul_sum _ _ _).symm
    _ = 1 := by rw [h₂.2]; simpa using h₁.2

/-- A cell state's two values are tied by normalization; substituting this turns
    every product-state goal below into a polynomial identity. -/
private lemma isProb_false {p : Bool → ℝ} (hp : IsProb p) : p false = 1 - p true := by
  have := hp.2; simp only [Fintype.sum_bool] at this; linarith

lemma prod3_isProb {p₁ p₂ p₃ : Bool → ℝ} (h₁ : IsProb p₁) (h₂ : IsProb p₂)
    (h₃ : IsProb p₃) : IsProb (prod3 p₁ p₂ p₃) := by
  refine ⟨fun t => mul_nonneg (mul_nonneg (h₁.1 _) (h₂.1 _)) (h₃.1 _), ?_⟩
  simp only [prod3, Fintype.sum_prod_type, Fintype.sum_bool]
  rw [isProb_false h₁, isProb_false h₂, isProb_false h₃]; ring

private lemma mul_log_mul' {x y : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y) :
    x * y * Real.log (x * y) = (x * y) * Real.log x + (x * y) * Real.log y := by
  rcases hx.eq_or_lt with h | h
  · rw [← h]; ring
  · rcases hy.eq_or_lt with h' | h'
    · rw [← h']; ring
    · rw [Real.log_mul h.ne' h'.ne']; ring

/-- INDEPENDENCE ADDS ENTROPY, exactly. Two independent cells carry the sum of
    their entropies — no more, because there is no shared pattern to discount,
    and no less. -/
theorem entropy_prod2 {α β : Type*} [Fintype α] [Fintype β] {p₁ : α → ℝ} {p₂ : β → ℝ}
    (h₁ : IsProb p₁) (h₂ : IsProb p₂) :
    entropy (fun ab : α × β => p₁ ab.1 * p₂ ab.2) = entropy p₁ + entropy p₂ := by
  have expand : ∑ ab : α × β, p₁ ab.1 * p₂ ab.2 * Real.log (p₁ ab.1 * p₂ ab.2)
      = ∑ a : α, ∑ b : β, p₁ a * p₂ b * Real.log (p₁ a * p₂ b) :=
    Fintype.sum_prod_type _
  have step : ∀ a : α, ∑ b : β, p₁ a * p₂ b * Real.log (p₁ a * p₂ b)
      = p₁ a * Real.log (p₁ a) + p₁ a * ∑ b, p₂ b * Real.log (p₂ b) := by
    intro a
    have hpt : ∀ b : β, p₁ a * p₂ b * Real.log (p₁ a * p₂ b)
        = (p₁ a * Real.log (p₁ a)) * p₂ b + p₁ a * (p₂ b * Real.log (p₂ b)) := by
      intro b
      have := mul_log_mul' (h₁.1 a) (h₂.1 b)
      linarith
    rw [Finset.sum_congr rfl fun b _ => hpt b, Finset.sum_add_distrib,
      ← Finset.mul_sum, ← Finset.mul_sum, h₂.2, mul_one]
  have key : ∑ ab : α × β, p₁ ab.1 * p₂ ab.2 * Real.log (p₁ ab.1 * p₂ ab.2)
      = (∑ a, p₁ a * Real.log (p₁ a)) + ∑ b, p₂ b * Real.log (p₂ b) := by
    rw [expand, Finset.sum_congr rfl fun a _ => step a, Finset.sum_add_distrib,
      ← Finset.sum_mul, h₁.2, one_mul]
  unfold entropy
  rw [key]; ring

/-- Three independent cells carry the sum of their three entropies. -/
theorem entropy_prod3 {p₁ p₂ p₃ : Bool → ℝ} (h₁ : IsProb p₁) (h₂ : IsProb p₂)
    (h₃ : IsProb p₃) :
    entropy (prod3 p₁ p₂ p₃) = entropy p₁ + entropy p₂ + entropy p₃ := by
  have hre := entropy_reindex (Equiv.prodAssoc Bool Bool Bool) (prod3 p₁ p₂ p₃)
  have heq : (fun u : (Bool × Bool) × Bool =>
        prod3 p₁ p₂ p₃ ((Equiv.prodAssoc Bool Bool Bool) u))
      = fun u : (Bool × Bool) × Bool =>
        (fun ab : Bool × Bool => p₁ ab.1 * p₂ ab.2) u.1 * p₃ u.2 := rfl
  rw [heq] at hre
  rw [← hre, entropy_prod2 (isProb_prod2 h₁ h₂) h₃, entropy_prod2 h₁ h₂]

lemma marg₁₂_prod3 {p₁ p₂ p₃ : Bool → ℝ} (h₃ : IsProb p₃) :
    marg₁₂ (prod3 p₁ p₂ p₃) = fun ab : Bool × Bool => p₁ ab.1 * p₂ ab.2 := by
  funext ab
  simp only [marg₁₂, prod3, Fintype.sum_bool]
  rw [isProb_false h₃]; ring

lemma marg₃_prod3 {p₁ p₂ p₃ : Bool → ℝ} (h₁ : IsProb p₁) (h₂ : IsProb p₂) :
    marg₃ (prod3 p₁ p₂ p₃) = p₃ := by
  funext c
  simp only [marg₃, prod3, Fintype.sum_bool]
  rw [isProb_false h₁, isProb_false h₂]; ring

/-- A PRODUCT STATE HAS NO WHOLE-ONLY SHARE, exactly zero. Its (1,2) marginal is
    already the product of two cell states and its third marginal the third,
    so grouping subadditivity caps every competitor at the state's own entropy —
    which the product attains, independence adding entropies exactly. -/
theorem share_prod3 {p₁ p₂ p₃ : Bool → ℝ} (h₁ : IsProb p₁) (h₂ : IsProb p₂)
    (h₃ : IsProb p₃) : share (prod3 p₁ p₂ p₃) = 0 := by
  refine share_eq_zero_of_entropy_maximal (prod3_isProb h₁ h₂ h₃) (fun q hq hpairs => ?_)
  have hg := entropy_grouping hq
  rw [hpairs.1, marg₃_of_samePairs hpairs, marg₁₂_prod3 (p₁ := p₁) (p₂ := p₂) h₃,
    marg₃_prod3 (p₃ := p₃) h₁ h₂, entropy_prod2 h₁ h₂] at hg
  rw [entropy_prod3 h₁ h₂ h₃]
  linarith

/-- NEVER FROM NOTHING. Independent cells in, independent cells out — so
    however violent the per-cell noise, and whatever three kernels it is built
    from, the whole-only share of the output is exactly zero. Order is never
    created out of no order at all.

    This is the theorem the hardware's independent-bits arm mirrors: the whole
    single-qubit error budget — relaxation, dephasing, readout, thermal
    excitation — provably cannot move that arm, and across 169 µs of idling it
    did not, staying at 1.2 × 10⁻⁴ nat. -/
theorem valve_from_nothing {K₁ K₂ K₃ : Bool → Bool → ℝ} (hK₁ : IsKernel K₁)
    (hK₂ : IsKernel K₂) (hK₃ : IsKernel K₃) {p₁ p₂ p₃ : Bool → ℝ}
    (h₁ : IsProb p₁) (h₂ : IsProb p₂) (h₃ : IsProb p₃) :
    share (channel3 K₁ K₂ K₃ (prod3 p₁ p₂ p₃)) = 0 := by
  rw [channel3_prod3]
  exact share_prod3 (push1_isProb hK₁ h₁) (push1_isProb hK₂ h₂) (push1_isProb hK₃ h₃)

/-- The uniform cell state: a fair coin. -/
noncomputable def unifBool : Bool → ℝ := fun _ => 1/2

lemma unifBool_isProb : IsProb unifBool := by
  refine ⟨fun _ => by norm_num [unifBool], ?_⟩
  simp only [unifBool, Fintype.sum_bool]; norm_num

/-- Pure noise is three independent fair coins. -/
lemma indep_eq_prod3 : indep = prod3 unifBool unifBool unifBool := by
  funext t; simp only [indep, prod3, unifBool]; norm_num

/-- NEVER FROM NOTHING, on the state with no pattern at any order: per-cell
    noise applied to pure noise leaves whole-only share exactly zero. -/
theorem valve_from_nothing_indep {K₁ K₂ K₃ : Bool → Bool → ℝ} (hK₁ : IsKernel K₁)
    (hK₂ : IsKernel K₂) (hK₃ : IsKernel K₃) :
    share (channel3 K₁ K₂ K₃ indep) = 0 := by
  rw [indep_eq_prod3]
  exact valve_from_nothing hK₁ hK₂ hK₃ unifBool_isProb unifBool_isProb unifBool_isProb

/-! ### Never downward: a pair marginal of the output is the input's, pushed -/

/-- THE PAIR-MARGINAL TRANSPORT LAW, slots one and two. The (1,2) marginal of
    the output is the (1,2) marginal of the input pushed through the two kernels
    concerned; the third kernel integrates away, whatever it is. -/
theorem marg₁₂_channel3 (K₁ K₂ : Bool → Bool → ℝ) {K₃ : Bool → Bool → ℝ}
    (hK₃ : IsKernel K₃) (p : Bool × Bool × Bool → ℝ) (a b : Bool) :
    marg₁₂ (channel3 K₁ K₂ K₃ p) (a, b)
      = ∑ u : Bool × Bool, K₁ a u.1 * K₂ b u.2 * marg₁₂ p u := by
  have e₃ := kernel_false hK₃
  simp only [marg₁₂, channel3, Fintype.sum_prod_type, Fintype.sum_bool, e₃]
  ring

/-- The same law at slots one and three. -/
theorem marg₁₃_channel3 (K₁ K₃ : Bool → Bool → ℝ) {K₂ : Bool → Bool → ℝ}
    (hK₂ : IsKernel K₂) (p : Bool × Bool × Bool → ℝ) (a c : Bool) :
    marg₁₃ (channel3 K₁ K₂ K₃ p) (a, c)
      = ∑ u : Bool × Bool, K₁ a u.1 * K₃ c u.2 * marg₁₃ p u := by
  have e₂ := kernel_false hK₂
  simp only [marg₁₃, channel3, Fintype.sum_prod_type, Fintype.sum_bool, e₂]
  ring

/-- The same law at slots two and three. -/
theorem marg₂₃_channel3 (K₂ K₃ : Bool → Bool → ℝ) {K₁ : Bool → Bool → ℝ}
    (hK₁ : IsKernel K₁) (p : Bool × Bool × Bool → ℝ) (b c : Bool) :
    marg₂₃ (channel3 K₁ K₂ K₃ p) (b, c)
      = ∑ u : Bool × Bool, K₂ b u.1 * K₃ c u.2 * marg₂₃ p u := by
  have e₁ := kernel_false hK₁
  simp only [marg₂₃, channel3, Fintype.sum_prod_type, Fintype.sum_bool, e₁]
  ring

/-- A PRODUCT PAIR MARGINAL STAYS A PRODUCT. If the input's (1,2) marginal
    factors, so does the output's — the two kernels act on separate factors and
    nothing couples them. This is the whole of "never downward": a channel that
    reads one cell at a time cannot manufacture a correlation between two. -/
theorem marg₁₂_channel3_of_prod (K₁ K₂ : Bool → Bool → ℝ) {K₃ : Bool → Bool → ℝ}
    (hK₃ : IsKernel K₃) {p : Bool × Bool × Bool → ℝ} {u₁ u₂ : Bool → ℝ}
    (h : ∀ v w, marg₁₂ p (v, w) = u₁ v * u₂ w) (a b : Bool) :
    marg₁₂ (channel3 K₁ K₂ K₃ p) (a, b) = push1 K₁ u₁ a * push1 K₂ u₂ b := by
  rw [marg₁₂_channel3 K₁ K₂ hK₃]
  simp only [push1, Fintype.sum_prod_type, Fintype.sum_bool, h]
  ring

theorem marg₁₃_channel3_of_prod (K₁ K₃ : Bool → Bool → ℝ) {K₂ : Bool → Bool → ℝ}
    (hK₂ : IsKernel K₂) {p : Bool × Bool × Bool → ℝ} {u₁ u₃ : Bool → ℝ}
    (h : ∀ v w, marg₁₃ p (v, w) = u₁ v * u₃ w) (a c : Bool) :
    marg₁₃ (channel3 K₁ K₂ K₃ p) (a, c) = push1 K₁ u₁ a * push1 K₃ u₃ c := by
  rw [marg₁₃_channel3 K₁ K₃ hK₂]
  simp only [push1, Fintype.sum_prod_type, Fintype.sum_bool, h]
  ring

theorem marg₂₃_channel3_of_prod (K₂ K₃ : Bool → Bool → ℝ) {K₁ : Bool → Bool → ℝ}
    (hK₁ : IsKernel K₁) {p : Bool × Bool × Bool → ℝ} {u₂ u₃ : Bool → ℝ}
    (h : ∀ v w, marg₂₃ p (v, w) = u₂ v * u₃ w) (b c : Bool) :
    marg₂₃ (channel3 K₁ K₂ K₃ p) (b, c) = push1 K₂ u₂ b * push1 K₃ u₃ c := by
  rw [marg₂₃_channel3 K₂ K₃ hK₁]
  simp only [push1, Fintype.sum_prod_type, Fintype.sum_bool, h]
  ring

/-- The single-slot transport law: the output's first marginal is the input's,
    pushed through the first kernel. The other two kernels integrate away. -/
theorem marg₁_channel3 (K₁ : Bool → Bool → ℝ) {K₂ K₃ : Bool → Bool → ℝ}
    (hK₂ : IsKernel K₂) (hK₃ : IsKernel K₃) (p : Bool × Bool × Bool → ℝ) (a : Bool) :
    marg₁ (channel3 K₁ K₂ K₃ p) a = push1 K₁ (marg₁ p) a := by
  have e₂ := kernel_false hK₂
  have e₃ := kernel_false hK₃
  simp only [marg₁, channel3, push1, Fintype.sum_prod_type, Fintype.sum_bool, e₂, e₃]
  ring

theorem marg₂_channel3 (K₂ : Bool → Bool → ℝ) {K₁ K₃ : Bool → Bool → ℝ}
    (hK₁ : IsKernel K₁) (hK₃ : IsKernel K₃) (p : Bool × Bool × Bool → ℝ) (b : Bool) :
    marg₂ (channel3 K₁ K₂ K₃ p) b = push1 K₂ (marg₂ p) b := by
  have e₁ := kernel_false hK₁
  have e₃ := kernel_false hK₃
  simp only [marg₂, channel3, push1, Fintype.sum_prod_type, Fintype.sum_bool, e₁, e₃]
  ring

theorem marg₃_channel3 (K₃ : Bool → Bool → ℝ) {K₁ K₂ : Bool → Bool → ℝ}
    (hK₁ : IsKernel K₁) (hK₂ : IsKernel K₂) (p : Bool × Bool × Bool → ℝ) (c : Bool) :
    marg₃ (channel3 K₁ K₂ K₃ p) c = push1 K₃ (marg₃ p) c := by
  have e₁ := kernel_false hK₁
  have e₂ := kernel_false hK₂
  simp only [marg₃, channel3, push1, Fintype.sum_prod_type, Fintype.sum_bool, e₁, e₂]
  ring

/-! #### The parity state's marginals, in the form the transport law wants -/

lemma marg₁₂_parity (v w : Bool) : marg₁₂ parity (v, w) = unifBool v * unifBool w :=
  parity_pair_independent_12 v w

lemma marg₁₃_parity (v w : Bool) : marg₁₃ parity (v, w) = unifBool v * unifBool w :=
  parity_pair_independent_13 v w

lemma marg₂₃_parity (v w : Bool) : marg₂₃ parity (v, w) = unifBool v * unifBool w :=
  parity_pair_independent_23 v w

lemma marg₁_parity : marg₁ parity = unifBool := by
  funext a
  cases a <;> simp [marg₁, parity, unifBool, Fintype.sum_bool] <;> norm_num

lemma marg₂_parity : marg₂ parity = unifBool := by
  funext b
  cases b <;> simp [marg₂, parity, unifBool, Fintype.sum_bool] <;> norm_num

lemma marg₃_parity : marg₃ parity = unifBool := by
  funext c
  cases c <;> simp [marg₃, parity, unifBool, Fintype.sum_bool] <;> norm_num

/-- NEVER DOWNWARD, at slots one and two: whatever three per-cell kernels the
    parity habit is pushed through, its first two slots come out exactly
    independent. -/
theorem valve_no_downward_12 {K₁ K₂ K₃ : Bool → Bool → ℝ} (hK₁ : IsKernel K₁)
    (hK₂ : IsKernel K₂) (hK₃ : IsKernel K₃) (a b : Bool) :
    marg₁₂ (channel3 K₁ K₂ K₃ parity) (a, b)
      = marg₁ (channel3 K₁ K₂ K₃ parity) a * marg₂ (channel3 K₁ K₂ K₃ parity) b := by
  rw [marg₁₂_channel3_of_prod K₁ K₂ hK₃ marg₁₂_parity,
    marg₁_channel3 K₁ hK₂ hK₃, marg₂_channel3 K₂ hK₁ hK₃, marg₁_parity, marg₂_parity]

theorem valve_no_downward_13 {K₁ K₂ K₃ : Bool → Bool → ℝ} (hK₁ : IsKernel K₁)
    (hK₂ : IsKernel K₂) (hK₃ : IsKernel K₃) (a c : Bool) :
    marg₁₃ (channel3 K₁ K₂ K₃ parity) (a, c)
      = marg₁ (channel3 K₁ K₂ K₃ parity) a * marg₃ (channel3 K₁ K₂ K₃ parity) c := by
  rw [marg₁₃_channel3_of_prod K₁ K₃ hK₂ marg₁₃_parity,
    marg₁_channel3 K₁ hK₂ hK₃, marg₃_channel3 K₃ hK₁ hK₂, marg₁_parity, marg₃_parity]

theorem valve_no_downward_23 {K₁ K₂ K₃ : Bool → Bool → ℝ} (hK₁ : IsKernel K₁)
    (hK₂ : IsKernel K₂) (hK₃ : IsKernel K₃) (b c : Bool) :
    marg₂₃ (channel3 K₁ K₂ K₃ parity) (b, c)
      = marg₂ (channel3 K₁ K₂ K₃ parity) b * marg₃ (channel3 K₁ K₂ K₃ parity) c := by
  rw [marg₂₃_channel3_of_prod K₂ K₃ hK₁ marg₂₃_parity,
    marg₂_channel3 K₂ hK₁ hK₃, marg₃_channel3 K₃ hK₁ hK₂, marg₂_parity, marg₃_parity]

/-- THE ONE-WAY VALVE, DOWNWARD HALF. Push the parity habit — whole-only order,
    every pair exactly independent — through ANY three per-cell kernels, and
    every pair of the output is STILL exactly independent: each two-slot
    marginal is the product of the output's own single-slot marginals.

    The habit's whole-only share generically decays, and on hardware it did,
    from 0.655 to 0.017 nat. What this theorem forbids is where the lost order
    could go: not into the pair sector, not at any strength of noise, not at any
    delay. The hardware arm measured that pair sector flat at 9 × 10⁻⁴ nat
    throughout, with no pairwise bulge on any pair. -/
theorem valve_no_downward {K₁ K₂ K₃ : Bool → Bool → ℝ} (hK₁ : IsKernel K₁)
    (hK₂ : IsKernel K₂) (hK₃ : IsKernel K₃) :
    (∀ a b, marg₁₂ (channel3 K₁ K₂ K₃ parity) (a, b)
        = marg₁ (channel3 K₁ K₂ K₃ parity) a * marg₂ (channel3 K₁ K₂ K₃ parity) b)
    ∧ (∀ a c, marg₁₃ (channel3 K₁ K₂ K₃ parity) (a, c)
        = marg₁ (channel3 K₁ K₂ K₃ parity) a * marg₃ (channel3 K₁ K₂ K₃ parity) c)
    ∧ (∀ b c, marg₂₃ (channel3 K₁ K₂ K₃ parity) (b, c)
        = marg₂ (channel3 K₁ K₂ K₃ parity) b * marg₃ (channel3 K₁ K₂ K₃ parity) c) :=
  ⟨valve_no_downward_12 hK₁ hK₂ hK₃, valve_no_downward_13 hK₁ hK₂ hK₃,
    valve_no_downward_23 hK₁ hK₂ hK₃⟩

/-! ### Upward: per-cell noise on pure pair order mints whole-only share -/

/-- The γ = ½ amplitude-damping kernel on one cell: an excited cell relaxes with
    probability one half, a relaxed cell stays put. The simplest per-cell noise
    that is neither a renaming nor a freeze — which is exactly why the
    deterministic argument of `Core.Creation` does not reach it. -/
noncomputable def damp : Bool → Bool → ℝ :=
  fun y x => if x then 1/2 else if y then 0 else 1

theorem damp_isKernel : IsKernel damp := by
  constructor
  · intro y x; cases y <;> cases x <;> norm_num [damp]
  · intro x; cases x <;> norm_num [damp]

/-- THE BULGE: what pure pair order becomes under three copies of the damping
    kernel. From the all-false word nothing moves; from the all-true word every
    cell relaxes independently, spreading half the weight evenly over all eight
    words. -/
noncomputable def bulge : Bool × Bool × Bool → ℝ :=
  fun t => if t.1 || t.2.1 || t.2.2 then 1/16 else 9/16

/-- THE EIGHT-CELL COMPUTATION, exact in rationals. -/
theorem channel3_damp_ferro : channel3 damp damp damp ferro = bulge := by
  funext y
  obtain ⟨a, b, c⟩ := y
  simp only [channel3, damp, ferro, bulge, Fintype.sum_prod_type, Fintype.sum_bool]
  cases a <;> cases b <;> cases c <;> norm_num

lemma bulge_isProb : IsProb bulge := by
  constructor
  · rintro ⟨a, b, c⟩; cases a <;> cases b <;> cases c <;> norm_num [bulge]
  · simp only [bulge, Fintype.sum_prod_type, Fintype.sum_bool]; norm_num

/-- THE COMPETITOR. The states carrying `bulge`'s three pair marginals form the
    line `bulge + t·χ` with `χ` the parity character; this is that line at
    `t = −1/32`, written out. It shifts weight off the four even-parity cells
    onto the four odd ones, which is invisible to every pair reading because the
    character sums to zero along every pair fiber. -/
noncomputable def bulgeWitness : Bool × Bool × Bool → ℝ :=
  fun t => if t.1 || t.2.1 || t.2.2 then
    (if t.2.2 = Bool.xor t.1 t.2.1 then 1/32 else 3/32) else 17/32

lemma bulgeWitness_isProb : IsProb bulgeWitness := by
  constructor
  · rintro ⟨a, b, c⟩; cases a <;> cases b <;> cases c <;> norm_num [bulgeWitness]
  · simp only [bulgeWitness, Fintype.sum_prod_type, Fintype.sum_bool]; norm_num

/-- THE PAIR-BLINDNESS OF THE COMPETITOR, checked cell by cell: it carries
    exactly `bulge`'s two-slot data at all three pairs, so it is a legitimate
    member of the envelope the share is measured against. -/
lemma bulgeWitness_samePairs : SamePairs bulge bulgeWitness := by
  refine ⟨?_, ?_, ?_⟩
  · funext ab; obtain ⟨a, b⟩ := ab
    cases a <;> cases b <;>
      simp only [marg₁₂, bulge, bulgeWitness, Fintype.sum_bool] <;> norm_num
  · funext ac; obtain ⟨a, c⟩ := ac
    cases a <;> cases c <;>
      simp only [marg₁₃, bulge, bulgeWitness, Fintype.sum_bool] <;> norm_num
  · funext bc; obtain ⟨b, c⟩ := bc
    cases b <;> cases c <;>
      simp only [marg₂₃, bulge, bulgeWitness, Fintype.sum_bool] <;> norm_num

private lemma log_nine : Real.log (9:ℝ) = 2 * Real.log 3 := by
  rw [show (9:ℝ) = 3 ^ 2 by norm_num, Real.log_pow]; norm_num

private lemma log_sixteen : Real.log (16:ℝ) = 4 * Real.log 2 := by
  rw [show (16:ℝ) = 2 ^ 4 by norm_num, Real.log_pow]; norm_num

private lemma log_thirtytwo : Real.log (32:ℝ) = 5 * Real.log 2 := by
  rw [show (32:ℝ) = 2 ^ 5 by norm_num, Real.log_pow]; norm_num

private lemma log_9_16 : Real.log ((9:ℝ)/16) = 2 * Real.log 3 - 4 * Real.log 2 := by
  rw [Real.log_div (by norm_num) (by norm_num), log_nine, log_sixteen]

private lemma log_1_16 : Real.log ((1:ℝ)/16) = -(4 * Real.log 2) := by
  rw [Real.log_div (by norm_num) (by norm_num), log_sixteen, Real.log_one]; ring

private lemma log_17_32 : Real.log ((17:ℝ)/32) = Real.log 17 - 5 * Real.log 2 := by
  rw [Real.log_div (by norm_num) (by norm_num), log_thirtytwo]

private lemma log_1_32 : Real.log ((1:ℝ)/32) = -(5 * Real.log 2) := by
  rw [Real.log_div (by norm_num) (by norm_num), log_thirtytwo, Real.log_one]; ring

private lemma log_3_32 : Real.log ((3:ℝ)/32) = Real.log 3 - 5 * Real.log 2 := by
  rw [Real.log_div (by norm_num) (by norm_num), log_thirtytwo]

lemma entropy_bulge : entropy bulge = 4 * Real.log 2 - (9/8) * Real.log 3 := by
  unfold entropy bulge
  simp only [Fintype.sum_prod_type, Fintype.sum_bool]
  norm_num [log_9_16, log_1_16]
  ring

lemma entropy_bulgeWitness :
    entropy bulgeWitness
      = 5 * Real.log 2 - (3/8) * Real.log 3 - (17/32) * Real.log 17 := by
  unfold entropy bulgeWitness
  simp only [Fintype.sum_prod_type, Fintype.sum_bool]
  norm_num [log_17_32, log_1_32, log_3_32]
  ring

/-- THE WITNESS INEQUALITY, and it is an integer comparison. The competitor has
    strictly more entropy than the state, because `17^17 < 2^32 · 3^24` —
    827240261886336764177 against 1213025622610333925376. No calculus, no
    derivative, no Mathlib gap: `norm_num` settles the integers and
    `Real.log_lt_log` carries them to the logarithms. -/
theorem entropy_bulge_lt_bulgeWitness : entropy bulge < entropy bulgeWitness := by
  have h : (17:ℝ) ^ 17 < 2 ^ 32 * 3 ^ 24 := by norm_num
  have hl := Real.log_lt_log (by positivity) h
  rw [Real.log_pow, Real.log_mul (by positivity) (by positivity), Real.log_pow,
    Real.log_pow] at hl
  push_cast at hl
  rw [entropy_bulge, entropy_bulgeWitness]
  linarith

/-- UPWARD FLOW EXISTS. `ferro` carries the strongest PAIR correlation three
    bits admit and whole-only share exactly zero (`share_ferro`). Push it
    through three copies of the γ = ½ damping kernel — per-cell noise, reading
    no pair, reading nothing but its own cell — and the whole-only share of the
    result is STRICTLY POSITIVE.

    Together with `valve_from_nothing` this is the valve's asymmetry: per-cell
    noise can move order UP the hierarchy, out of the pair sector and into the
    whole-only sector, but only where lower-order order already stands. From
    independence it makes nothing.

    This is the theorem the hardware's ferro arm mirrors: a whole-only bulge to
    0.0541 nat at 49.5 µs while the pair covariances fell from ~0.99 to ~0.08,
    against a zero-free-parameter prediction at χ² 24.44 on 12 degrees of
    freedom. The theorem is about this model; the run is about that device. -/
theorem valve_upward : 0 < share (channel3 damp damp damp ferro) := by
  rw [channel3_damp_ferro]
  have hmem : entropy bulgeWitness ∈ pairEnvelope bulge :=
    ⟨bulgeWitness, bulgeWitness_isProb, bulgeWitness_samePairs, rfl⟩
  have hle := le_csSup (pairEnvelope_bddAbove bulge) hmem
  unfold share
  linarith [entropy_bulge_lt_bulgeWitness]

/-- The witness's margin, kept as an explicit number so nothing is rounded up:
    the minted share is AT LEAST `log 2 + (3/4)·log 3 − (17/32)·log 17`, about
    0.01196 nat. This is a lower bound from one competitor, not the share: the
    exact optimum along the line `bulge + t·χ` is transcendental and is not
    computed here. -/
theorem valve_upward_bound :
    Real.log 2 + (3/4) * Real.log 3 - (17/32) * Real.log 17
      ≤ share (channel3 damp damp damp ferro) := by
  rw [channel3_damp_ferro]
  have hmem : entropy bulgeWitness ∈ pairEnvelope bulge :=
    ⟨bulgeWitness, bulgeWitness_isProb, bulgeWitness_samePairs, rfl⟩
  have hle := le_csSup (pairEnvelope_bddAbove bulge) hmem
  unfold share
  rw [entropy_bulgeWitness] at hle
  rw [entropy_bulge]
  linarith

/-- THE VALVE'S UPWARD DIRECTION AS A STRICT INCREASE, so "created" is not
    rhetoric: the input's whole-only share is exactly zero and the output's is
    strictly greater. -/
theorem valve_upward_strict : share ferro < share (channel3 damp damp damp ferro) := by
  rw [share_ferro]; exact valve_upward

/-! ### What drives the pump: the odd sector is fed only by asymmetry

`valve_upward` mints share with a DAMPING kernel, which treats the two cell
values differently — an excited cell decays, a relaxed one does not. That
asymmetry is not incidental to the minting; it is the whole of it. A kernel
that treats the two values alike mints nothing, from any sign-symmetric state,
however strong its pair correlation. -/

/-- A kernel is FLIP-COVARIANT when complementing input and output together
    leaves it unchanged: `K (!y) (!x) = K y x`. On a binary cell with normalized
    columns this is exactly the binary symmetric channel — one error rate, the
    same in both directions. Damping is not of this kind, and that is why it can
    pump. -/
def IsFlipCovariant (K : Bool → Bool → ℝ) : Prop := ∀ y x, K (!y) (!x) = K y x

/-- Given normalization, ONE equation makes a binary kernel flip-covariant: the
    two error rates agree. The other half, `K false false = K true true`, is
    then forced by the columns. -/
theorem isFlipCovariant_of_symm {K : Bool → Bool → ℝ} (hK : IsKernel K)
    (hs : K true false = K false true) : IsFlipCovariant K := by
  have h1 := hK.2 true
  have h2 := hK.2 false
  intro y x
  cases y <;> cases x <;> simp only [Bool.not_true, Bool.not_false] <;> linarith

/-- FLIP-COVARIANT KERNELS COMMUTE WITH THE GLOBAL FLIP. Complementing every
    cell of the input and complementing every cell of the output are the same
    operation for such a channel, so a sign-symmetric state stays sign-symmetric
    however hard it is pushed. Proved by reindexing the eight-cell sum through
    the flip, cell by cell. -/
theorem signSymmetric_channel3 {K₁ K₂ K₃ : Bool → Bool → ℝ}
    (h₁ : IsFlipCovariant K₁) (h₂ : IsFlipCovariant K₂) (h₃ : IsFlipCovariant K₃)
    {p : Bool × Bool × Bool → ℝ} (hp : SignSymmetric p) :
    SignSymmetric (channel3 K₁ K₂ K₃ p) := by
  have a₁ : K₁ false false = K₁ true true := by simpa using h₁ true true
  have b₁ : K₁ false true = K₁ true false := by simpa using h₁ true false
  have a₂ : K₂ false false = K₂ true true := by simpa using h₂ true true
  have b₂ : K₂ false true = K₂ true false := by simpa using h₂ true false
  have a₃ : K₃ false false = K₃ true true := by simpa using h₃ true true
  have b₃ : K₃ false true = K₃ true false := by simpa using h₃ true false
  have q1 : p (false, false, false) = p (true, true, true) := by
    simpa using hp false false false
  have q2 : p (false, false, true) = p (true, true, false) := by
    simpa using hp false false true
  have q3 : p (false, true, false) = p (true, false, true) := by
    simpa using hp false true false
  have q4 : p (false, true, true) = p (true, false, false) := by
    simpa using hp false true true
  intro a b c
  simp only [channel3, Fintype.sum_prod_type, Fintype.sum_bool]
  cases a <;> cases b <;> cases c <;>
    simp only [Bool.not_true, Bool.not_false, a₁, b₁, a₂, b₂, a₃, b₃, q1, q2, q3, q4] <;>
    ring

/-- THE PUMP IS THE ASYMMETRY. A per-cell channel whose kernels treat the two
    cell values alike mints NO whole-only share from any sign-symmetric state —
    exactly zero, at any noise strength, however strongly pair-correlated the
    input. The output is still sign-symmetric, and `share_eq_zero_of_signSymmetric`
    kills the whole family at once.

    So `valve_upward` is not a fact about noise in general. The upward flow needs
    a channel that breaks the global sign symmetry, and damping breaks it —
    `damp_not_flipCovariant`. -/
theorem valve_needs_asymmetry {K₁ K₂ K₃ : Bool → Bool → ℝ} (hK₁ : IsKernel K₁)
    (hK₂ : IsKernel K₂) (hK₃ : IsKernel K₃) (h₁ : IsFlipCovariant K₁)
    (h₂ : IsFlipCovariant K₂) (h₃ : IsFlipCovariant K₃)
    {p : Bool × Bool × Bool → ℝ} (hp : IsProb p) (hps : SignSymmetric p) :
    share (channel3 K₁ K₂ K₃ p) = 0 :=
  share_eq_zero_of_signSymmetric (channel3_isProb hK₁ hK₂ hK₃ hp)
    (signSymmetric_channel3 h₁ h₂ h₃ hps)

/-- The same statement on the state `valve_upward` pumps, so the contrast is
    exhibited on one input rather than argued: `ferro` through three flip-
    covariant kernels mints exactly zero, `ferro` through three damping kernels
    mints strictly more than zero. -/
theorem valve_needs_asymmetry_ferro {K₁ K₂ K₃ : Bool → Bool → ℝ} (hK₁ : IsKernel K₁)
    (hK₂ : IsKernel K₂) (hK₃ : IsKernel K₃) (h₁ : IsFlipCovariant K₁)
    (h₂ : IsFlipCovariant K₂) (h₃ : IsFlipCovariant K₃) :
    share (channel3 K₁ K₂ K₃ ferro) = 0 :=
  valve_needs_asymmetry hK₁ hK₂ hK₃ h₁ h₂ h₃ ferro_isProb ferro_signSymmetric

/-- THE EDGE OF THE LEMMA, exhibited rather than asserted: the damping kernel is
    NOT flip-covariant — a relaxed cell stays put with certainty while an
    excited one decays with probability one half — which is why `valve_upward`
    stands alongside `valve_needs_asymmetry` without tension. -/
theorem damp_not_flipCovariant : ¬ IsFlipCovariant damp := by
  intro h
  have := h true false
  simp only [Bool.not_true, Bool.not_false, damp] at this
  norm_num at this

/-- THE SHARPENING, stated where it can be checked. `Core.Creation`'s
    `percell_no_creation` says a DETERMINISTIC per-cell map never raises the
    whole-only share. This says a STOCHASTIC one can: there exist three kernels
    and a state on which the share strictly rises. The two are not in tension —
    a genuine mixture is neither a renaming nor a freeze, which is exactly the
    dichotomy the deterministic proof spends. -/
theorem stochastic_percell_can_create :
    ∃ (K₁ K₂ K₃ : Bool → Bool → ℝ) (p : Bool × Bool × Bool → ℝ),
      IsKernel K₁ ∧ IsKernel K₂ ∧ IsKernel K₃ ∧ IsProb p ∧
        share p < share (channel3 K₁ K₂ K₃ p) :=
  ⟨damp, damp, damp, ferro, damp_isKernel, damp_isKernel, damp_isKernel,
    ferro_isProb, valve_upward_strict⟩

end CIRISOntology.Core
