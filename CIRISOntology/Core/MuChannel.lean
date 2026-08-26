/-
CIRISOntology.Core.MuChannel — R3's successor: the monotone that survives noise,
built from the CHANNEL's stationary structure instead of the state's entropy.

WHAT THIS CLOSES. `Core/StochasticHabit.lean` discharged R3's first half and
then fenced the second, in its own words:

    "σ ≥ 0 is FALSE for channels (reset channel witness); the successor must
     consume the channel's stationary structure (DPI), not the state's entropy."

Its `no_monotone_of_reset` proves that no function of the state's Shannon
entropy alone can be non-decreasing under every channel. It named the
replacement — relative entropy to a stationary state under the data-processing
inequality — and explicitly did NOT build it: "that object is NOT in this file."
This file builds it, on finite state spaces, with no admitted gaps.

WHAT IS HERE, in four rungs.

  1. `klDiv` — relative entropy of finite nonnegative-real distributions, with
     Lean's `0 * _ = 0` giving the standard `0 log 0 = 0` convention for free.
     Nonnegativity (`klDiv_nonneg`) via the log-sum inequality (`logSum_le`),
     proved from `Real.log_le_sub_one_of_pos` and nothing else.

  2. `klDiv_push_le` — THE DATA PROCESSING INEQUALITY for arbitrary finite
     stochastic kernels: pushing both arguments through one channel cannot
     increase the divergence. Log-sum applied per output cell, then Fubini.
     This is the general statement, not a deterministic-map special case.

  3. `sigma` — the successor itself: `σ_m = D(p T^m ‖ π)` for a channel `T` with
     stationary `π`. `sigma_antitone` proves it is monotone NON-INCREASING in
     `m`, immediately from DPI with the stationary distribution as the second
     argument. That is the well-behaved-for-channels quantity R3 asked for, and
     it is a fiber-measure statement: μ_c is what the monotone is computed
     against, which is the remainder item this brick was cut for.

  4. THE RECONCILIATION, both halves. The very channel that killed the old
     monotone satisfies the new one. `sigma_softReset_antitone`: a reset toward
     any full-support target is antitone in `m` from `m = 0`, while
     `softReset_lowers_shannon` shows that same channel STRICTLY lowers Shannon
     entropy from the uniform state — the two facts stand together, which is
     exactly the content of the fence. `sigma_softReset_strict_drop` is the dye
     test: the monotone is exhibited actually FALLING (`σ₁ = 0 < σ₀`), because an
     antitone sequence that never moves would satisfy rung 3 vacuously. And the
     point-mass reset of
     `StochasticHabit.resetState` gets its honest treatment: absolute continuity
     FAILS there (`hardReset_not_absCont`), the true divergence is `+∞` off the
     reals, and under Lean's junk convention the monotone visibly breaks
     (`hardReset_sigma_zero_lt_one`). The absolute-continuity hypothesis on
     every theorem below is therefore load-bearing, not decoration, and this
     file exhibits its failure rather than describing it.

WHAT THIS FILE DOES NOT CLAIM, stated plainly. It is finite-state and
real-valued: no measure-theoretic version, no `ℝ≥0∞` convention, so a
divergence that is genuinely infinite is OUT OF SCOPE rather than handled — and
the point-mass reset above is precisely such a case, kept and marked. It proves
no mixing rate: DPI gives monotone descent, never a CONTRACTION FACTOR, so the
mixing theorem (remainder item 1) is untouched by anything here and no rate
should be read out of `sigma_antitone`. It says nothing about entropy
production in the thermodynamic sense; `sigma` is entropy-production-LIKE in
that it is the standard monotone of stochastic thermodynamics, and the physical
identification is not made here.

CREDITS, generously and claiming only the mechanization: Kullback and Leibler
(the divergence, 1951); Gibbs (the nonnegativity, in its inequality form);
Cover and Thomas, *Elements of Information Theory*, Thm 2.7.4 and §2.7 (the
log-sum inequality and the data-processing inequality as used here, in exactly
this shape); Csiszár (the f-divergence framework in which DPI is the defining
property); Seifert's review (entropy production under noise, the physical
reading of `sigma`). Mathlib supplies `Real.log_le_sub_one_of_pos` and nothing
else that is specific to this argument — `Mathlib.InformationTheory` at this
pin carries no `klDiv`, so the divergence is defined here.

KILL, separable: exhibit a finite stochastic kernel `T`, a stationary `π`, and
an initial `p` absolutely continuous with respect to `π`, for which
`D(p T^{m+1} ‖ π) > D(p T^m ‖ π)` — then `sigma_antitone` is false and R3's
named successor is the wrong object. (A counterexample that drops absolute
continuity kills nothing: that hypothesis is stated, and its failure is
exhibited here.)
-/
import CIRISOntology.Core.StochasticHabit
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic

namespace CIRISOntology.Core.MuChannel

/-! ### Rung one: relative entropy on a finite state space -/

variable {α β : Type*} [Fintype α] [Fintype β]

/-- Relative entropy (Kullback–Leibler divergence) of finite real-valued
    distributions, in nats. Lean's `0 * x = 0` supplies the standard
    `0 log 0 = 0` convention with no side condition.

    The other standard convention — `p a > 0` and `q a = 0` giving `+∞` — is
    NOT representable in `ℝ`, and Lean's junk value `x / 0 = 0` silently reads
    such a term as `0`. Every result below therefore carries `AbsCont` as an
    explicit hypothesis, and `hardReset_sigma_zero_lt_one` exhibits what
    dropping it costs. -/
noncomputable def klDiv (p q : α → ℝ) : ℝ := ∑ a, p a * Real.log (p a / q a)

/-- A finite distribution: nonnegative and summing to one. -/
structure IsDist (p : α → ℝ) : Prop where
  nonneg : ∀ a, 0 ≤ p a
  total : ∑ a, p a = 1

/-- Absolute continuity `p ≪ q`: wherever `q` puts no mass, neither does `p`.
    This is the hypothesis under which the real-valued `klDiv` is the true
    divergence rather than a junk-truncated one. -/
def AbsCont (p q : α → ℝ) : Prop := ∀ a, q a = 0 → p a = 0

theorem klDiv_self (p : α → ℝ) : klDiv p p = 0 := by
  refine Finset.sum_eq_zero fun a _ => ?_
  by_cases h : p a = 0
  · simp [h]
  · rw [div_self h, Real.log_one, mul_zero]

/-- **THE LOG-SUM INEQUALITY.** For nonnegative `f`, `g` with `f ≪ g`,

      `(∑ f) · log ((∑ f)/(∑ g)) ≤ ∑ f i · log (f i / g i)`.

    Proved from `log x ≤ x - 1` alone: the per-index slack telescopes to
    `(∑ g)·(∑f/∑g) − ∑ f = 0`. This is Cover–Thomas Thm 2.7.1; everything
    downstream in this file is an instance of it. -/
theorem logSum_le {ι : Type*} [Fintype ι] (f g : ι → ℝ)
    (hf : ∀ i, 0 ≤ f i) (hg : ∀ i, 0 ≤ g i) (hac : ∀ i, g i = 0 → f i = 0) :
    (∑ i, f i) * Real.log ((∑ i, f i) / (∑ i, g i))
      ≤ ∑ i, f i * Real.log (f i / g i) := by
  have hF0 : (0 : ℝ) ≤ ∑ i, f i := Finset.sum_nonneg fun i _ => hf i
  have hG0 : (0 : ℝ) ≤ ∑ i, g i := Finset.sum_nonneg fun i _ => hg i
  rcases hG0.eq_or_lt with hGz | hGpos
  · -- The second argument is the zero measure: absolute continuity empties the first.
    have hgz : ∀ i, g i = 0 := fun i =>
      (Finset.sum_eq_zero_iff_of_nonneg fun j _ => hg j).mp hGz.symm i (Finset.mem_univ i)
    have hfz : ∀ i, f i = 0 := fun i => hac i (hgz i)
    simp [hfz, hgz]
  rcases hF0.eq_or_lt with hFz | hFpos
  · have hfz : ∀ i, f i = 0 := fun i =>
      (Finset.sum_eq_zero_iff_of_nonneg fun j _ => hf j).mp hFz.symm i (Finset.mem_univ i)
    simp [hfz]
  · have hGne : (∑ i, g i) ≠ 0 := ne_of_gt hGpos
    have key : ∀ i ∈ (Finset.univ : Finset ι),
        f i * Real.log ((∑ j, f j) / (∑ j, g j))
          ≤ f i * Real.log (f i / g i)
              + (g i * ((∑ j, f j) / (∑ j, g j)) - f i) := by
      intro i _
      rcases (hf i).eq_or_lt with hfi | hfi
      · -- No mass here: the slack term alone carries the inequality.
        have hz : f i = 0 := hfi.symm
        have hnn : 0 ≤ g i * ((∑ j, f j) / (∑ j, g j)) :=
          mul_nonneg (hg i) (div_nonneg hF0 hG0)
        rw [hz]
        simpa using hnn
      · -- Mass here forces mass there, and `log x ≤ x - 1` does the rest.
        have hgi : 0 < g i := by
          rcases (hg i).eq_or_lt with h | h
          · exact absurd (hac i h.symm) (ne_of_gt hfi)
          · exact h
        have hxpos : (0 : ℝ) < ((∑ j, f j) * g i) / ((∑ j, g j) * f i) :=
          div_pos (mul_pos hFpos hgi) (mul_pos hGpos hfi)
        have hlog := Real.log_le_sub_one_of_pos hxpos
        have hsplit : Real.log ((∑ j, f j) / (∑ j, g j)) - Real.log (f i / g i)
            = Real.log (((∑ j, f j) * g i) / ((∑ j, g j) * f i)) := by
          rw [← Real.log_div (ne_of_gt (div_pos hFpos hGpos))
                (ne_of_gt (div_pos hfi hgi))]
          congr 1
          field_simp
        have h1 : f i * Real.log (((∑ j, f j) * g i) / ((∑ j, g j) * f i))
            ≤ f i * ((((∑ j, f j) * g i) / ((∑ j, g j) * f i)) - 1) :=
          mul_le_mul_of_nonneg_left hlog (le_of_lt hfi)
        have h2 : f i * ((((∑ j, f j) * g i) / ((∑ j, g j) * f i)) - 1)
            = g i * ((∑ j, f j) / (∑ j, g j)) - f i := by
          field_simp
          ring
        have h0 : f i * Real.log ((∑ j, f j) / (∑ j, g j))
            - f i * Real.log (f i / g i)
            = f i * Real.log (((∑ j, f j) * g i) / ((∑ j, g j) * f i)) := by
          rw [← mul_sub, hsplit]
        linarith
    calc (∑ i, f i) * Real.log ((∑ j, f j) / (∑ j, g j))
        = ∑ i, f i * Real.log ((∑ j, f j) / (∑ j, g j)) := by rw [Finset.sum_mul]
      _ ≤ ∑ i, (f i * Real.log (f i / g i)
              + (g i * ((∑ j, f j) / (∑ j, g j)) - f i)) := Finset.sum_le_sum key
      _ = ∑ i, f i * Real.log (f i / g i)
              + ((∑ i, g i) * ((∑ j, f j) / (∑ j, g j)) - ∑ i, f i) := by
            rw [Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.sum_mul]
      _ = ∑ i, f i * Real.log (f i / g i) := by field_simp

/-- **GIBBS.** Relative entropy between finite distributions is nonnegative
    when the first is absolutely continuous with respect to the second. The
    hypothesis is not removable: see `hardReset_klDiv_neg`. -/
theorem klDiv_nonneg {p q : α → ℝ} (hp : IsDist p) (hq : IsDist q)
    (hac : AbsCont p q) : 0 ≤ klDiv p q := by
  have h := logSum_le p q hp.nonneg hq.nonneg hac
  rw [hp.total, hq.total] at h
  simpa [klDiv] using h

/-! ### Rung two: the data processing inequality for finite channels -/

/-- A finite stochastic kernel: nonnegative rows summing to one. -/
structure IsKernel (T : α → β → ℝ) : Prop where
  nonneg : ∀ a b, 0 ≤ T a b
  row : ∀ a, ∑ b, T a b = 1

/-- Push a distribution through a channel. -/
noncomputable def push (T : α → β → ℝ) (p : α → ℝ) : β → ℝ := fun b => ∑ a, p a * T a b

omit [Fintype β] in
theorem push_nonneg {T : α → β → ℝ} (hT : ∀ a b, 0 ≤ T a b) {p : α → ℝ}
    (hp : ∀ a, 0 ≤ p a) (b : β) : 0 ≤ push T p b :=
  Finset.sum_nonneg fun a _ => mul_nonneg (hp a) (hT a b)

theorem push_total {T : α → β → ℝ} (hT : IsKernel T) {p : α → ℝ}
    (hp : ∑ a, p a = 1) : ∑ b, push T p b = 1 := by
  unfold push
  rw [Finset.sum_comm]
  have : ∀ a ∈ (Finset.univ : Finset α), ∑ b, p a * T a b = p a := by
    intro a _
    rw [← Finset.mul_sum, hT.row a, mul_one]
  rw [Finset.sum_congr rfl this, hp]

theorem push_isDist {T : α → β → ℝ} (hT : IsKernel T) {p : α → ℝ}
    (hp : IsDist p) : IsDist (push T p) :=
  ⟨push_nonneg hT.nonneg hp.nonneg, push_total hT hp.total⟩

omit [Fintype β] in
/-- Absolute continuity survives a channel: if `q` cannot reach a cell then
    neither can `p`, because they travel by the same transition weights. -/
theorem absCont_push {T : α → β → ℝ} (hT : ∀ a b, 0 ≤ T a b) {p q : α → ℝ}
    (hq : ∀ a, 0 ≤ q a) (hac : AbsCont p q) : AbsCont (push T p) (push T q) := by
  intro b hb
  have hterm : ∀ a ∈ (Finset.univ : Finset α), q a * T a b = 0 :=
    (Finset.sum_eq_zero_iff_of_nonneg fun a _ => mul_nonneg (hq a) (hT a b)).mp hb
  refine Finset.sum_eq_zero fun a _ => ?_
  rcases mul_eq_zero.mp (hterm a (Finset.mem_univ a)) with h | h
  · rw [hac a h, zero_mul]
  · rw [h, mul_zero]

/-- **THE DATA PROCESSING INEQUALITY**, for arbitrary finite stochastic
    kernels. Sending both arguments through one channel cannot increase the
    divergence: information about which distribution you started from is never
    created by processing. Cover–Thomas Thm 2.7.4; the proof is the log-sum
    inequality applied in each output cell, then Fubini and the row sums.

    This is the object `Core/StochasticHabit` named and declined to import. -/
theorem klDiv_push_le {T : α → β → ℝ} (hT : IsKernel T) {p q : α → ℝ}
    (hp : ∀ a, 0 ≤ p a) (hq : ∀ a, 0 ≤ q a) (hac : AbsCont p q) :
    klDiv (push T p) (push T q) ≤ klDiv p q := by
  have cell : ∀ b ∈ (Finset.univ : Finset β),
      push T p b * Real.log (push T p b / push T q b)
        ≤ ∑ a, (p a * T a b) * Real.log ((p a * T a b) / (q a * T a b)) := by
    intro b _
    exact logSum_le (fun a => p a * T a b) (fun a => q a * T a b)
      (fun a => mul_nonneg (hp a) (hT.nonneg a b))
      (fun a => mul_nonneg (hq a) (hT.nonneg a b))
      (fun a h => by
        show p a * T a b = 0
        replace h : q a * T a b = 0 := h
        rcases mul_eq_zero.mp h with h' | h'
        · rw [hac a h', zero_mul]
        · rw [h', mul_zero])
  have collapse : ∀ b ∈ (Finset.univ : Finset β),
      (∑ a, (p a * T a b) * Real.log ((p a * T a b) / (q a * T a b)))
        = ∑ a, (p a * T a b) * Real.log (p a / q a) := by
    intro b _
    refine Finset.sum_congr rfl fun a _ => ?_
    by_cases hz : p a * T a b = 0
    · rw [hz, zero_mul, zero_mul]
    · have hpa : p a ≠ 0 := fun h => hz (by rw [h, zero_mul])
      have hTa : T a b ≠ 0 := fun h => hz (by rw [h, mul_zero])
      have hqa : q a ≠ 0 := fun h => hpa (hac a h)
      rw [mul_div_mul_right _ _ hTa]
  have fubini :
      (∑ b, ∑ a, (p a * T a b) * Real.log (p a / q a)) = klDiv p q := by
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl fun a _ => ?_
    have : ∀ b ∈ (Finset.univ : Finset β),
        (p a * T a b) * Real.log (p a / q a)
          = (p a * Real.log (p a / q a)) * T a b := by
      intro b _; ring
    rw [Finset.sum_congr rfl this, ← Finset.mul_sum, hT.row a, mul_one]
  calc klDiv (push T p) (push T q)
      = ∑ b, push T p b * Real.log (push T p b / push T q b) := rfl
    _ ≤ ∑ b, ∑ a, (p a * T a b) * Real.log ((p a * T a b) / (q a * T a b)) :=
        Finset.sum_le_sum cell
    _ = ∑ b, ∑ a, (p a * T a b) * Real.log (p a / q a) :=
        Finset.sum_congr rfl collapse
    _ = klDiv p q := fubini

/-! ### Rung three: the successor `σ` and its monotonicity

R3's fence says the stochastic monotone must consume the CHANNEL's stationary
structure. Here it does: `σ` is the divergence of the evolved state from the
channel's own stationary distribution — a quantity of the pair `(T_c, μ_c)`,
never of the state's entropy alone. -/

/-- Iterated push: `iterPush T m p` is `p Tᵐ`. -/
noncomputable def iterPush (T : α → α → ℝ) : ℕ → (α → ℝ) → (α → ℝ)
  | 0, p => p
  | m + 1, p => push T (iterPush T m p)

@[simp] theorem iterPush_zero (T : α → α → ℝ) (p : α → ℝ) : iterPush T 0 p = p := rfl

@[simp] theorem iterPush_succ (T : α → α → ℝ) (m : ℕ) (p : α → ℝ) :
    iterPush T (m + 1) p = push T (iterPush T m p) := rfl

/-- `π` is stationary for `T`. -/
def Stationary (T : α → α → ℝ) (π : α → ℝ) : Prop := push T π = π

theorem iterPush_isDist {T : α → α → ℝ} (hT : IsKernel T) {p : α → ℝ}
    (hp : IsDist p) : ∀ m, IsDist (iterPush T m p)
  | 0 => hp
  | m + 1 => push_isDist hT (iterPush_isDist hT hp m)

theorem iterPush_absCont {T : α → α → ℝ} (hT : IsKernel T) {π p : α → ℝ}
    (hπ : Stationary T π) (hπ0 : ∀ a, 0 ≤ π a) (hac : AbsCont p π) :
    ∀ m, AbsCont (iterPush T m p) π
  | 0 => hac
  | m + 1 => by
      have h := absCont_push hT.nonneg hπ0 (iterPush_absCont hT hπ hπ0 hac m)
      rw [hπ] at h
      exact h

/-- **THE SUCCESSOR.** `σ_m = D(p Tᵐ ‖ π)`: how far the evolved state still is
    from the channel's stationary distribution, measured against `π` as the
    fiber measure. This is the entropy-production-like quantity that IS
    well-behaved for channels, replacing the failed state-entropy `σ`. -/
noncomputable def sigma (T : α → α → ℝ) (π p : α → ℝ) (m : ℕ) : ℝ :=
  klDiv (iterPush T m p) π

@[simp] theorem sigma_zero (T : α → α → ℝ) (π p : α → ℝ) :
    sigma T π p 0 = klDiv p π := rfl

/-- **THE MONOTONE, ONE STEP.** Immediate from DPI with the stationary
    distribution in the second argument: the channel moves `π` nowhere, so the
    inequality it imposes is a descent for `p` alone. -/
theorem sigma_succ_le {T : α → α → ℝ} (hT : IsKernel T) {π p : α → ℝ}
    (hπ : Stationary T π) (hπ0 : ∀ a, 0 ≤ π a) (hp : IsDist p)
    (hac : AbsCont p π) (m : ℕ) : sigma T π p (m + 1) ≤ sigma T π p m := by
  have hstep : klDiv (push T (iterPush T m p)) (push T π)
      ≤ klDiv (iterPush T m p) π :=
    klDiv_push_le hT (iterPush_isDist hT hp m).nonneg hπ0
      (iterPush_absCont hT hπ hπ0 hac m)
  rw [hπ] at hstep
  exact hstep

/-- **THE MONOTONE.** `σ` is non-increasing in `m`: a stochastic habit run
    against its own stationary structure has a genuine second law, where the
    state's entropy had none. R3's second half, discharged on finite state
    spaces. -/
theorem sigma_antitone {T : α → α → ℝ} (hT : IsKernel T) {π p : α → ℝ}
    (hπ : Stationary T π) (hπ0 : ∀ a, 0 ≤ π a) (hp : IsDist p)
    (hac : AbsCont p π) : Antitone (sigma T π p) :=
  antitone_nat_of_succ_le (sigma_succ_le hT hπ hπ0 hp hac)

/-- And the monotone has a floor: `σ ≥ 0` throughout, so the descent is a
    descent to something. -/
theorem sigma_nonneg {T : α → α → ℝ} (hT : IsKernel T) {π p : α → ℝ}
    (hπ : Stationary T π) (hπd : IsDist π) (hp : IsDist p)
    (hac : AbsCont p π) (m : ℕ) : 0 ≤ sigma T π p m :=
  klDiv_nonneg (iterPush_isDist hT hp m) hπd
    (iterPush_absCont hT hπ hπd.nonneg hac m)

/-! ### Rung four: the reconciliation with `StochasticHabit`'s reset witness

The reset channel is the one that falsified state-entropy monotonicity. It
satisfies the new monotone — and the way it satisfies it is instructive, so
both halves are here: the full-support case where the theorem applies from
`m = 0`, and the point-mass case where absolute continuity fails and the
real-valued monotone visibly breaks. -/

open CIRISOntology.Core.StochasticHabit

/-- The reset (erasure) channel toward a target distribution `r`: forget the
    input entirely and emit `r`. `StochasticHabit.resetState` is the `r` of the
    witness there. -/
noncomputable def resetKernel (r : α → ℝ) : α → α → ℝ := fun _ b => r b

theorem resetKernel_isKernel {r : α → ℝ} (hr : IsDist r) : IsKernel (resetKernel r) :=
  ⟨fun _ b => hr.nonneg b, fun _ => hr.total⟩

/-- One application of the reset channel erases the input: whatever came in,
    `r` comes out. -/
theorem push_resetKernel {r p : α → ℝ} (hp : ∑ a, p a = 1) :
    push (resetKernel r) p = r := by
  funext b
  unfold push resetKernel
  rw [← Finset.sum_mul, hp, one_mul]

theorem resetKernel_stationary {r : α → ℝ} (hr : IsDist r) :
    Stationary (resetKernel r) r := push_resetKernel hr.total

/-- After one step the reset channel sits exactly on its stationary
    distribution, so the monotone is pinned at its floor from `m = 1` on. -/
theorem sigma_resetKernel_succ {r p : α → ℝ} (hr : IsDist r) (hp : IsDist p)
    (m : ℕ) : sigma (resetKernel r) r p (m + 1) = 0 := by
  have hstate : iterPush (resetKernel r) (m + 1) p = r := by
    rw [iterPush_succ]
    exact push_resetKernel (iterPush_isDist (resetKernel_isKernel hr) hp m).total
  unfold sigma
  rw [hstate, klDiv_self]

/-! #### The full-support reset: the theorem applies, and the entropy still falls -/

/-- The biased reset target on the two-point space: mass `t` on `false`. For
    `0 < t < 1` this has full support, so every distribution is absolutely
    continuous with respect to it. -/
noncomputable def softReset (t : ℝ) : Two → ℝ := fun b => if b = false then t else 1 - t

theorem softReset_isDist {t : ℝ} (h0 : 0 ≤ t) (h1 : t ≤ 1) : IsDist (softReset t) := by
  constructor
  · intro b; cases b <;> simp [softReset] <;> linarith
  · rw [Fintype.sum_bool]; simp [softReset]

theorem softReset_pos {t : ℝ} (h0 : 0 < t) (h1 : t < 1) (b : Two) : 0 < softReset t b := by
  cases b <;> simp [softReset] <;> linarith

theorem softReset_absCont {t : ℝ} (h0 : 0 < t) (h1 : t < 1) (p : Two → ℝ) :
    AbsCont p (softReset t) := fun b hb =>
  absurd hb (ne_of_gt (softReset_pos h0 h1 b))

/-- **THE RECONCILIATION, first half.** The reset channel toward a full-support
    target satisfies the new monotone from `m = 0`, for EVERY starting
    distribution — no hypothesis about the initial state beyond being one. -/
theorem sigma_softReset_antitone {t : ℝ} (h0 : 0 < t) (h1 : t < 1) {p : Two → ℝ}
    (hp : IsDist p) : Antitone (sigma (resetKernel (softReset t)) (softReset t) p) := by
  have hr := softReset_isDist (le_of_lt h0) (le_of_lt h1)
  exact sigma_antitone (resetKernel_isKernel hr) (resetKernel_stationary hr)
    hr.nonneg hp (softReset_absCont h0 h1 p)

/-- **THE RECONCILIATION, second half.** That same channel STRICTLY lowers
    Shannon entropy out of the uniform state — it is a genuine instance of
    `StochasticHabit.reset_lowers_entropy`'s phenomenon, not a defanged one.
    Taken with `sigma_softReset_antitone`: one channel, the old monotone
    falsified and the new one satisfied. That is what the fence predicted. -/
theorem softReset_lowers_shannon :
    shannon (softReset (1/4)) < shannon (uniformOn (Finset.univ : Finset Two)) := by
  have huniv : (Finset.univ : Finset Two).Nonempty := ⟨false, Finset.mem_univ _⟩
  have hcard : ((Finset.univ : Finset Two).card : ℝ) = 2 := by simp
  rw [shannon_uniformOn huniv, hcard]
  have hsupp : (Finset.univ : Finset Two).filter (fun b => softReset (1/4) b ≠ 0)
      = Finset.univ := by
    refine Finset.filter_true_of_mem fun b _ => ?_
    exact ne_of_gt (softReset_pos (by norm_num) (by norm_num) b)
  have hval : shannon (softReset (1/4))
      = -(3/4 : ℝ) * Real.log (3/4) + -(1/4 : ℝ) * Real.log (1/4) := by
    unfold shannon
    rw [hsupp, Fintype.sum_bool]
    norm_num [softReset]
  have hlog4 : Real.log (4 : ℝ) = 2 * Real.log 2 := by
    rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.log_pow]
    push_cast; ring
  have h34 : Real.log (3/4 : ℝ) = Real.log 3 - 2 * Real.log 2 := by
    rw [Real.log_div (by norm_num) (by norm_num), hlog4]
  have h14 : Real.log (1/4 : ℝ) = -(2 * Real.log 2) := by
    rw [Real.log_div (by norm_num) (by norm_num), Real.log_one, hlog4]; ring
  have hkey : 4 * Real.log 2 < 3 * Real.log 3 := by
    have h16 : Real.log (16 : ℝ) = 4 * Real.log 2 := by
      rw [show (16 : ℝ) = 2 ^ 4 by norm_num, Real.log_pow]; push_cast; ring
    have h27 : Real.log (27 : ℝ) = 3 * Real.log 3 := by
      rw [show (27 : ℝ) = 3 ^ 3 by norm_num, Real.log_pow]; push_cast; ring
    have := Real.log_lt_log (by norm_num : (0:ℝ) < 16) (by norm_num : (16:ℝ) < 27)
    rw [h16, h27] at this
    exact this
  rw [hval, h34, h14]
  linarith

/-- The uniform state on the two-point space is a distribution — the starting
    state of `StochasticHabit`'s witness. -/
theorem uniformTwo_isDist : IsDist (uniformOn (Finset.univ : Finset Two)) := by
  constructor
  · intro b
    by_cases hb : b ∈ (Finset.univ : Finset Two)
    · rw [uniformOn_mem hb]; positivity
    · rw [uniformOn_not_mem hb]
  · rw [Fintype.sum_bool, uniformOn_mem (Finset.mem_univ true),
      uniformOn_mem (Finset.mem_univ false)]
    norm_num

/-- **THE DYE TEST — the descent is real, not a tautology at zero.** An antitone
    sequence that is constant proves nothing, so here is the monotone actually
    falling: from the uniform state into the biased reset, `σ₁ < σ₀`, with
    `σ₀ = log 2 − (log 3)/2 > 0` and `σ₁ = 0`. Without this the antitonicity
    theorem would be satisfied by any channel that never moves anything. -/
theorem sigma_softReset_strict_drop :
    sigma (resetKernel (softReset (1/4))) (softReset (1/4))
        (uniformOn (Finset.univ : Finset Two)) 1
      < sigma (resetKernel (softReset (1/4))) (softReset (1/4))
        (uniformOn (Finset.univ : Finset Two)) 0 := by
  have hr : IsDist (softReset (1/4 : ℝ)) := softReset_isDist (by norm_num) (by norm_num)
  have h1 : sigma (resetKernel (softReset (1/4))) (softReset (1/4))
      (uniformOn (Finset.univ : Finset Two)) 1 = 0 :=
    sigma_resetKernel_succ hr uniformTwo_isDist 0
  have hf : uniformOn (Finset.univ : Finset Two) false = 1/2 := by
    rw [uniformOn_mem (Finset.mem_univ false)]; norm_num
  have ht : uniformOn (Finset.univ : Finset Two) true = 1/2 := by
    rw [uniformOn_mem (Finset.mem_univ true)]; norm_num
  have hval : sigma (resetKernel (softReset (1/4))) (softReset (1/4))
      (uniformOn (Finset.univ : Finset Two)) 0
      = (1/2 : ℝ) * Real.log (2/3) + (1/2 : ℝ) * Real.log 2 := by
    rw [sigma_zero]
    unfold klDiv
    rw [Fintype.sum_bool, hf, ht]
    norm_num [softReset]
  have h23 : Real.log (2/3 : ℝ) = Real.log 2 - Real.log 3 := by
    rw [Real.log_div (by norm_num) (by norm_num)]
  have hkey : Real.log 3 < 2 * Real.log 2 := by
    have h4 : Real.log (4 : ℝ) = 2 * Real.log 2 := by
      rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.log_pow]; push_cast; ring
    have := Real.log_lt_log (by norm_num : (0:ℝ) < 3) (by norm_num : (3:ℝ) < 4)
    rw [h4] at this
    exact this
  rw [h1, hval, h23]
  linarith

/-! #### The point-mass reset: absolute continuity fails, and so does the monotone

`StochasticHabit.resetState` is a point mass. The true divergence from the
uniform state to it is `+∞`, which `ℝ` cannot hold; Lean's `x / 0 = 0` reads
the offending term as `0` instead. The result is not a wrong theorem but a
theorem out of scope, and the scope condition is exactly `AbsCont`. Both facts
are exhibited rather than described. -/

theorem resetState_isDist : IsDist (resetState) := by
  constructor
  · intro b; cases b <;> simp [resetState]
  · rw [Fintype.sum_bool]; simp [resetState]

/-- Absolute continuity FAILS for the point-mass reset: the uniform state puts
    mass where `resetState` puts none. -/
theorem hardReset_not_absCont :
    ¬ AbsCont (uniformOn (Finset.univ : Finset Two)) resetState := by
  intro h
  have hz : uniformOn (Finset.univ : Finset Two) true = 0 := by
    refine h true ?_
    simp [resetState]
  rw [uniformOn_mem (Finset.mem_univ true)] at hz
  simp at hz

/-- With absolute continuity gone, the real-valued divergence goes NEGATIVE —
    the junk value `x / 0 = 0` truncating a `+∞` term to nothing. -/
theorem hardReset_klDiv_neg :
    klDiv (uniformOn (Finset.univ : Finset Two)) resetState = -(Real.log 2) / 2 := by
  have hf : uniformOn (Finset.univ : Finset Two) false = 1/2 := by
    rw [uniformOn_mem (Finset.mem_univ false)]; norm_num
  have ht : uniformOn (Finset.univ : Finset Two) true = 1/2 := by
    rw [uniformOn_mem (Finset.mem_univ true)]; norm_num
  have hlog12 : Real.log (1/2 : ℝ) = -Real.log 2 := by
    rw [Real.log_div one_ne_zero two_ne_zero, Real.log_one]; ring
  unfold klDiv
  rw [Fintype.sum_bool, hf, ht]
  norm_num [resetState]
  rw [hlog12]
  ring

/-- **AND SO THE HYPOTHESIS IS LOAD-BEARING.** Drop absolute continuity and the
    successor's monotonicity is false on the very witness that motivated it:
    `σ₀ < σ₁`. Nothing above is thereby weakened — `sigma_antitone` carries
    `AbsCont` — but the fence is now two-sided, and anyone tempted to delete the
    hypothesis has a counterexample waiting. -/
theorem hardReset_sigma_zero_lt_one :
    sigma (resetKernel resetState) resetState (uniformOn (Finset.univ : Finset Two)) 0
      < sigma (resetKernel resetState) resetState (uniformOn (Finset.univ : Finset Two)) 1 := by
  have h1 : sigma (resetKernel resetState) resetState
      (uniformOn (Finset.univ : Finset Two)) 1 = 0 :=
    sigma_resetKernel_succ resetState_isDist uniformTwo_isDist 0
  rw [h1, sigma_zero, hardReset_klDiv_neg]
  have : (0 : ℝ) < Real.log 2 := Real.log_pos (by norm_num)
  linarith

end CIRISOntology.Core.MuChannel
