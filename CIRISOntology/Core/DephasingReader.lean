/-
CIRISOntology.Core.DephasingReader — the reader rule for pure dephasing.

A READER is a Hermitian operator `L` that an environment keeps measuring, with no
Hamiltonian of its own: the Lindblad equation `dρ/dt = −γ [L,[L,ρ]]`. When `L` is
diagonal with real eigenvalues `l : n → ℝ` (in the basis the reader reads), the
double commutator acts ENTRYWISE:

    [L,[L,ρ]]ᵢⱼ = (lᵢ − lⱼ)² · ρᵢⱼ,

so each matrix entry evolves on its own, `ρᵢⱼ(t) = exp(−γ (lᵢ−lⱼ)² t) · ρᵢⱼ(0)`.
Four consequences are proved here:

  (a) `dissipator_apply` — the entrywise identity, at matrix level;
  (b) `dissipator_diag` — populations are fixed: READING DOES NOT WRITE;
  (c) `dissipator_eq_zero_iff`, `solution_const_iff`, `solution_tendsto_zero_iff` —
      a coherence is untouched iff the reader gives its two ends the same value,
      and (γ > 0, nonzero initial coherence) it dies iff the values differ;
      `solution_hasDerivAt` + `solution_unique` say the explicit curve IS the
      solution of the equation, and the only one;
  (d) `phiSq_coherence_survives`, `phiSq_coherence_decays` — the φ² reader
      (`L = diag(xᵢ²)`) leaves the coherence between `x` and `−x` alone forever and
      kills every coherence across distinct `x²`.

THE LINK TO THE FOUNDING SHAPE, and how far it goes. The φ² reader's spectrum is
the view `x ↦ x²`, and that view is exactly the modulus-grade view of
`Core.ExchangeSign`'s DRY lemma: `phiSq_view_blind_to_well` is a DIRECT USE of
`nonFactoring_of_signChange` (with `C = Unit`, sign `ε = −1`), exhibiting the
which-well bit as a `NonFactoring` quantity against the φ² view. The dynamical
statement `reader_preserves_iff_same_fibre` is what makes the link more than a
pun: the dephasing channel spares a coherence EXACTLY when its two basis states
lie in one fibre of the reader's view. So the coherence the φ² reader cannot
destroy is precisely the coherence across a pair the view cannot tell apart, and
the which-well bit lives in that pair. That is the whole of the link; it is the
same lemma as `Core.NonFactoring`, not a new instance of anything.

SCOPE, stated plainly. ON THE MODEL ONLY; finite-dimensional pure dephasing (no
Hamiltonian, constant γ, diagonal reader); ONE WITNESS (the shape is the same
lemma as `Core.NonFactoring` / `Core.ExchangeSign`) — NOT EVIDENCE ABOUT THE
WORLD. In particular nothing here says what a φ² bath does once a Hamiltonian is
present (tunnelling mixes the wells and the reader's basis stops being
invariant); that question belongs to the measurement campaign, not to this file.
The time-dependent rate of a de Sitter bath (`e^{6N}`) is NOT covered: γ is a
constant here.

CREDIT. The result is standard and old; this file is its mechanization.
Pure-dephasing / pointer-basis: Zurek, Phys. Rev. D 24, 1516 (1981) (the pointer
basis is the eigenbasis of the operator the environment measures) and Phys. Rev.
D 26, 1862 (1982). Decoherence-free subspaces as degenerate eigenspaces of the
error generator: Zanardi–Rasetti, Phys. Rev. Lett. 79, 3306 (1997);
Lidar–Chuang–Whaley, Phys. Rev. Lett. 81, 2594 (1998). The φ² channel's sign
blindness in the vacuum-selection context: Christie, Joo, Kaplanek, Vennin,
Wands, JCAP 09 (2026) 125, arXiv:2512.14204 ((+φ₀)² = (−φ₀)²).
-/
import CIRISOntology.Core.ExchangeSign
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.Complex.RealDeriv
import Mathlib.Data.Matrix.Basic

namespace CIRISOntology.Core.DephasingReader

open Matrix Filter Topology

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- The commutator `[A,B] = AB − BA`. -/
noncomputable def comm (A B : Matrix n n ℂ) : Matrix n n ℂ := A * B - B * A

/-- The reader: the diagonal operator with real eigenvalues `l`. -/
noncomputable def reader (l : n → ℝ) : Matrix n n ℂ := diagonal (fun i => (l i : ℂ))

/-- The double-commutator dissipator `D(ρ) = [L,[L,ρ]]` for the reader `L`. -/
noncomputable def dissipator (l : n → ℝ) (ρ : Matrix n n ℂ) : Matrix n n ℂ :=
  comm (reader l) (comm (reader l) ρ)

/-! ### (a) The entrywise identity -/

/-- **(a)** `[L,[L,ρ]]ᵢⱼ = (lᵢ − lⱼ)² ρᵢⱼ` for diagonal `L`. -/
theorem dissipator_apply (l : n → ℝ) (ρ : Matrix n n ℂ) (i j : n) :
    dissipator l ρ i j = (((l i - l j) ^ 2 : ℝ) : ℂ) * ρ i j := by
  simp only [dissipator, comm, reader, sub_apply, diagonal_mul, mul_diagonal]
  push_cast
  ring

/-! ### (b) Reading does not write -/

/-- **(b)** The dissipator has zero diagonal: populations in the reader's basis are
    fixed. -/
theorem dissipator_diag (l : n → ℝ) (ρ : Matrix n n ℂ) (i : n) :
    dissipator l ρ i i = 0 := by
  rw [dissipator_apply]; simp

/-! ### (c) Which coherences survive -/

/-- **(c, generator form)** For a nonzero coherence, the dissipator leaves it alone
    iff the reader gives both ends the same value. -/
theorem dissipator_eq_zero_iff (l : n → ℝ) (ρ : Matrix n n ℂ) (i j : n)
    (hρ : ρ i j ≠ 0) : dissipator l ρ i j = 0 ↔ l i = l j := by
  rw [dissipator_apply, mul_eq_zero, Complex.ofReal_eq_zero, pow_eq_zero_iff two_ne_zero,
    sub_eq_zero]
  exact ⟨fun h => h.resolve_right hρ, Or.inl⟩

/-- The explicit solution of `dρ/dt = −γ D(ρ)`. -/
noncomputable def solution (γ : ℝ) (l : n → ℝ) (ρ₀ : Matrix n n ℂ) (t : ℝ) :
    Matrix n n ℂ :=
  fun i j => ((Real.exp (-(γ * (l i - l j) ^ 2 * t)) : ℝ) : ℂ) * ρ₀ i j

omit [Fintype n] [DecidableEq n] in
theorem solution_zero (γ : ℝ) (l : n → ℝ) (ρ₀ : Matrix n n ℂ) :
    solution γ l ρ₀ 0 = ρ₀ := by
  funext i j; simp [solution]

/-- The explicit curve solves the equation, entry by entry. -/
theorem solution_hasDerivAt (γ : ℝ) (l : n → ℝ) (ρ₀ : Matrix n n ℂ) (t : ℝ) (i j : n) :
    HasDerivAt (fun s => solution γ l ρ₀ s i j)
      (-(γ : ℂ) * dissipator l (solution γ l ρ₀ t) i j) t := by
  have hlin : HasDerivAt (fun s : ℝ => -(γ * (l i - l j) ^ 2 * s))
      (-(γ * (l i - l j) ^ 2)) t := by
    simpa using ((hasDerivAt_id t).const_mul (γ * (l i - l j) ^ 2)).neg
  have hexp := (hlin.exp).ofReal_comp.mul_const (ρ₀ i j)
  convert hexp using 1
  rw [dissipator_apply]
  simp only [solution]
  push_cast
  ring

/-- **Uniqueness.** Any differentiable curve whose entries satisfy the equation is
    the explicit solution started from its own initial value. -/
theorem solution_unique (γ : ℝ) (l : n → ℝ) (f : ℝ → Matrix n n ℂ)
    (hf : ∀ t i j, HasDerivAt (fun s => f s i j) (-(γ : ℂ) * dissipator l (f t) i j) t)
    (t : ℝ) : f t = solution γ l (f 0) t := by
  funext i j
  set c : ℝ := γ * (l i - l j) ^ 2 with hc
  -- g(s) = exp(c s) · f(s)ᵢⱼ has zero derivative.
  let g : ℝ → ℂ := fun s => ((Real.exp (c * s) : ℝ) : ℂ) * f s i j
  have hg : ∀ s, HasDerivAt g 0 s := by
    intro s
    have h1 : HasDerivAt (fun s : ℝ => c * s) c s := by
      simpa using (hasDerivAt_id s).const_mul c
    have h2 := (h1.exp).ofReal_comp.mul (hf s i j)
    convert h2 using 1
    rw [dissipator_apply, Complex.ofReal_mul, hc]
    simp only [Complex.ofReal_mul, Complex.ofReal_pow, Complex.ofReal_sub]
    ring
  have hconst : g t = g 0 :=
    is_const_of_deriv_eq_zero (fun s => (hg s).differentiableAt)
      (fun s => (hg s).deriv) t 0
  simp only [g, mul_zero, Real.exp_zero, Complex.ofReal_one, one_mul] at hconst
  simp only [solution]
  rw [← hconst, ← mul_assoc, ← Complex.ofReal_mul, ← Real.exp_add]
  have : -(γ * (l i - l j) ^ 2 * t) + c * t = 0 := by rw [hc]; ring
  rw [this, Real.exp_zero, Complex.ofReal_one, one_mul]

omit [Fintype n] [DecidableEq n] in
/-- **(c, flow form)** A nonzero coherence is constant for all time iff the reader
    gives both ends the same value (any nonzero rate). -/
theorem solution_const_iff (γ : ℝ) (hγ : γ ≠ 0) (l : n → ℝ) (ρ₀ : Matrix n n ℂ) (i j : n)
    (hρ : ρ₀ i j ≠ 0) : (∀ t, solution γ l ρ₀ t i j = ρ₀ i j) ↔ l i = l j := by
  constructor
  · intro h
    have h1 := h 1
    simp only [solution, mul_one] at h1
    have he : ((Real.exp (-(γ * (l i - l j) ^ 2)) : ℝ) : ℂ) = 1 := by
      have := mul_right_cancel₀ hρ (h1.trans (one_mul _).symm)
      exact this
    have he' : Real.exp (-(γ * (l i - l j) ^ 2)) = 1 := by exact_mod_cast he
    rw [Real.exp_eq_one_iff, neg_eq_zero, mul_eq_zero] at he'
    rcases he' with h0 | h0
    · exact absurd h0 hγ
    · exact sub_eq_zero.mp (pow_eq_zero_iff two_ne_zero |>.mp h0)
  · intro h t
    simp [solution, h]

omit [Fintype n] [DecidableEq n] in
/-- **(c, asymptotic form)** With `γ > 0` and a nonzero initial coherence, the
    coherence tends to zero iff the reader gives its two ends different values. -/
theorem solution_tendsto_zero_iff (γ : ℝ) (hγ : 0 < γ) (l : n → ℝ) (ρ₀ : Matrix n n ℂ)
    (i j : n) (hρ : ρ₀ i j ≠ 0) :
    Tendsto (fun t => solution γ l ρ₀ t i j) atTop (𝓝 0) ↔ l i ≠ l j := by
  constructor
  · intro h heq
    have hc : (fun t => solution γ l ρ₀ t i j) = fun _ => ρ₀ i j := by
      funext t; simp [solution, heq]
    rw [hc] at h
    exact hρ (tendsto_nhds_unique tendsto_const_nhds h)
  · intro hne
    have hd : l i - l j ≠ 0 := sub_ne_zero.mpr hne
    have hpos : 0 < γ * (l i - l j) ^ 2 := mul_pos hγ (by positivity)
    have hlin : Tendsto (fun t : ℝ => γ * (l i - l j) ^ 2 * t) atTop atTop :=
      tendsto_id.const_mul_atTop hpos
    have hexp : Tendsto (fun t : ℝ => Real.exp (-(γ * (l i - l j) ^ 2 * t))) atTop (𝓝 0) :=
      Real.tendsto_exp_neg_atTop_nhds_zero.comp hlin
    have hC : Tendsto (fun t : ℝ => ((Real.exp (-(γ * (l i - l j) ^ 2 * t)) : ℝ) : ℂ))
        atTop (𝓝 0) := by
      have h := (Complex.continuous_ofReal.tendsto 0).comp hexp
      rw [Complex.ofReal_zero] at h
      exact h
    have h := hC.mul_const (ρ₀ i j)
    rw [zero_mul] at h
    exact h

omit [Fintype n] [DecidableEq n] in
/-- The fibre form of (c): the channel spares the coherence between two basis states
    exactly when they lie in one fibre of the reader's view `l`. -/
theorem reader_preserves_iff_same_fibre (γ : ℝ) (hγ : 0 < γ) (l : n → ℝ)
    (ρ₀ : Matrix n n ℂ) (i j : n) (hρ : ρ₀ i j ≠ 0) :
    ¬ Tendsto (fun t => solution γ l ρ₀ t i j) atTop (𝓝 0) ↔ l i = l j := by
  rw [solution_tendsto_zero_iff γ hγ l ρ₀ i j hρ, not_not]

/-! ### (d) The φ² reader is sign-blind -/

/-- The φ² reader on a basis of field values `x : n → ℝ`: eigenvalues `xᵢ²`. -/
def phiSq (x : n → ℝ) : n → ℝ := fun i => x i ^ 2

omit [Fintype n] [DecidableEq n] in
/-- **(d, survival)** The φ² reader never touches the coherence between `x` and `−x`:
    it is constant for all time, at every rate. -/
theorem phiSq_coherence_survives (γ : ℝ) (x : n → ℝ) (ρ₀ : Matrix n n ℂ) (i j : n)
    (hx : x i = -x j) (t : ℝ) : solution γ (phiSq x) ρ₀ t i j = ρ₀ i j := by
  have : phiSq x i = phiSq x j := by simp [phiSq, hx]
  simp [solution, this]

omit [Fintype n] [DecidableEq n] in
/-- **(d, decay)** Across distinct values of `x²`, the φ² reader drives every
    nonzero coherence to zero. -/
theorem phiSq_coherence_decays (γ : ℝ) (hγ : 0 < γ) (x : n → ℝ) (ρ₀ : Matrix n n ℂ)
    (i j : n) (hρ : ρ₀ i j ≠ 0) (hx : x i ^ 2 ≠ x j ^ 2) :
    Tendsto (fun t => solution γ (phiSq x) ρ₀ t i j) atTop (𝓝 0) :=
  (solution_tendsto_zero_iff γ hγ (phiSq x) ρ₀ i j hρ).mpr hx

/-! ### The link: the φ² view does not factor the which-well bit -/

/-- The which-well bit of a one-slot field value: `1` on the positive side. -/
noncomputable def wellBit (ψ : Unit → ℝ) : ℝ := if 0 < ψ () then 1 else 0

/-- **The φ² view is blind to the well.** A DIRECT USE of `nonFactoring_of_signChange`
    (`C = Unit`, `ε = −1`): the view `ψ ↦ ψ²` — the φ² reader's spectrum — admits a
    witness pair (`x₀` and `−x₀`, any `x₀ > 0`) differing in the which-well bit. -/
theorem phiSq_view_blind_to_well :
    NonFactoring (fun (c : Unit) (ψ : Unit → ℝ) => (ψ c) ^ 2) wellBit :=
  nonFactoring_of_signChange (x := fun _ => (1 : ℝ)) (ε := fun _ => (-1 : ℝ))
    (fun _ => by norm_num) wellBit (by simp [wellBit])

omit [Fintype n] [DecidableEq n] in
/-- **The two halves together.** For two basis states at `x₀` and `−x₀` (`x₀ ≠ 0`):
    they differ in the which-well bit, and their coherence survives the φ² reader
    forever. The coherence the reader cannot destroy is exactly the one across the
    pair its view cannot separate. -/
theorem phiSq_spares_the_well_coherence (γ : ℝ) (x : n → ℝ) (ρ₀ : Matrix n n ℂ)
    (i j : n) (hx : x i = -x j) (h0 : x j ≠ 0) :
    wellBit (fun _ => x i) ≠ wellBit (fun _ => x j) ∧
      ∀ t, solution γ (phiSq x) ρ₀ t i j = ρ₀ i j := by
  refine ⟨?_, phiSq_coherence_survives γ x ρ₀ i j hx⟩
  rw [hx]
  rcases lt_or_gt_of_ne h0 with h | h
  · simp [wellBit, h, not_lt.mpr h.le, neg_pos.mpr h]
  · simp [wellBit, h, not_lt.mpr (neg_nonpos.mpr h.le)]

/-- **THE HONEST FOOT.** Recorded commitments, not proofs. -/
structure DephasingReach where
  /-- PROVED. Entrywise dissipator, fixed populations, survival iff same reader
      value, explicit solution and its uniqueness. -/
  reader_rule_proved : True
  /-- PROVED, SAME LEMMA. The φ² link is `nonFactoring_of_signChange` reused; one
      witness, not a new instance of the shape. -/
  link_is_one_witness : True
  /-- SCOPE. On the model only: finite dimension, no Hamiltonian, constant rate,
      diagonal reader. Not evidence about the world. -/
  model_only : True

def dephasing_reach : DephasingReach := ⟨trivial, trivial, trivial⟩

end CIRISOntology.Core.DephasingReader
