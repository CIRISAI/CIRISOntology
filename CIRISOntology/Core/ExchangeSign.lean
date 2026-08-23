/-
CIRISOntology.Core.ExchangeSign — the fourth NonFactoring witness, derived through
a shared lemma rather than argued afresh; the composition rule for statistics; and
the cap rung of the repaired meet criterion.

WHY THIS EXISTS. The descriptor-chain programme's meet-in-the-middle review found
that the floor's exclusion axiom (`Core/Lattice.lean`, Boolean occupancy) does not
carry the exchange SIGN: hard-core bosons satisfy Boolean occupancy with commuting
operators, so the sign that separates fermions from hard-core bosons is invisible
to every occupancy view. That is the founding shape — two wholes agreeing under
every partial view, differing in a quantity — surfacing at the bottom of matter.
This file mechanizes the finite witness.

THE DRY OBSERVATION, which is the point of deriving rather than exhibiting. Three
of the four NonFactoring witnesses are now PHASES: `nonfactoring_parity` (a sign),
`nonfactoring_cp_phase` (a phase invisible to pair marginals), and the exchange
sign below (a sign invisible to Born views). Record, the frame-relation, is the
odd one out. So the general lemma is stated once — MODULUS-LEVEL VIEWS ARE BLIND
TO SIGN CHANGES (`nonFactoring_of_signChange`) — and the exchange witness is its
instance. The whole-only content of the Logos keeps turning out to be phase-grade
data that modulus-grade views cannot read; that observation is recorded here as an
observation, not a theorem.

SCOPE, stated so it cannot be over-read.
1. This is a MODEL brick: two modes, two particles, real amplitudes. It is not
   quantum field theory and it does not derive exclusion from relativity. The
   discharge of the floor's exclusion axiom remains BY PAPER (Pauli, Phys. Rev.
   58, 716 (1940); Streater–Wightman, Thm 4-10). This file is the
   witnessed-BY-MACHINE half of the repaired meet criterion, nothing more.
2. `pauli_cap` is a NAMED RESTATEMENT that the ledger's state space enforces the
   occupation cap by type (`occ` is `Bool`), not a derivation of the cap. Its
   value is that CI can point at the rung; the physics warrant stays a citation.
3. `composite_exchange_sign` is the Ehrenfest–Oppenheimer composition rule on the
   block-swap permutation: statistics is a rule re-derived at every composition
   boundary from total fermion count, never a stored flag of a tier.

CREDIT. Girardeau (J. Math. Phys. 1, 516 (1960)): the Bose–Fermi mapping — hard-core
bosons and free fermions share every density while differing in exchange symmetry —
is the physics literature's own statement that occupancy views are sign-blind; our
witness is its two-mode finite shadow. Ehrenfest–Oppenheimer, Phys. Rev. 37, 333
(1931), for composite statistics. The hard-core-boson witness as the gap in the
naive meet criterion is due to the descriptor-chain adversarial review (2026-08-23).
-/
import CIRISOntology.Core.NonFactoring
import CIRISOntology.Core.Lattice
import Mathlib.GroupTheory.Perm.Sign

namespace CIRISOntology.Core

/-! ### The shared lemma: modulus-level views are blind to sign changes -/

/-- **THE DRY LEMMA.** Over any configuration space, the family of pointwise
    Born views (`ψ c ^ 2`, one view per configuration — the COMPLETE modulus
    data, strictly finer than any occupancy marginal) cannot factor a quantity
    that a pointwise sign change alters. The witness pair is the state and its
    sign-flipped partner. -/
theorem nonFactoring_of_signChange {C : Type*} {x : C → ℝ} {ε : C → ℝ}
    (hε : ∀ c, (ε c) ^ 2 = 1) (q : (C → ℝ) → ℝ)
    (hq : q (fun c => ε c * x c) ≠ q x) :
    NonFactoring (fun (c : C) (ψ : C → ℝ) => (ψ c) ^ 2) q := by
  refine ⟨fun c => ε c * x c, x, ?_, hq⟩
  intro c
  simp only [mul_pow, hε c, one_mul]

/-! ### The instance: the exchange sign

Two particles on two modes, amplitudes on ordered configurations. The symmetric
state is the hard-core boson; the antisymmetric state is the fermion. -/

/-- Amplitudes on ordered two-particle configurations over two modes. -/
abbrev TwoParticle := Fin 2 × Fin 2 → ℝ

/-- The hard-core boson: symmetric, vanishing on double occupancy. -/
def psiSym : TwoParticle := fun c => if c.1 = c.2 then 0 else 1

/-- The fermion: antisymmetric (vanishes on double occupancy automatically;
    stated uniformly with `psiSym` so the two differ only in a sign). -/
def psiAnti : TwoParticle := fun c => if c.1 = c.2 then 0 else if c.1 < c.2 then 1 else -1

/-- The pointwise sign relating them. On the diagonal `psiSym` is zero, so the
    value there is immaterial; off the diagonal it is the exchange sign. -/
def exchangeFlip : Fin 2 × Fin 2 → ℝ := fun c => if c.1 < c.2 then 1 else -1

theorem exchangeFlip_sq (c : Fin 2 × Fin 2) : (exchangeFlip c) ^ 2 = 1 := by
  unfold exchangeFlip
  split <;> norm_num

theorem psiAnti_eq_flip_mul : psiAnti = fun c => exchangeFlip c * psiSym c := by
  funext c
  unfold psiAnti exchangeFlip psiSym
  rcases c with ⟨i, j⟩
  by_cases h : i = j
  · simp [h]
  · have hlt : i < j ∨ j < i := (Ne.lt_or_lt h)
    rcases hlt with hl | hl
    · simp [h, hl, not_lt.mpr (le_of_lt hl)]
    · have : ¬ i < j := not_lt.mpr (le_of_lt hl)
      simp [h, this]

/-- The exchange-operator expectation `⟨ψ | X | ψ⟩`: the swap of the two particle
    labels, read against the state. This is the quantity that carries the
    statistics. -/
def swapExpect (ψ : TwoParticle) : ℝ := ∑ c : Fin 2 × Fin 2, ψ c * ψ (c.2, c.1)

theorem swapExpect_psiSym : swapExpect psiSym = 2 := by
  unfold swapExpect psiSym
  simp [Fintype.sum_prod_type, Fin.sum_univ_two]
  norm_num

theorem swapExpect_psiAnti : swapExpect psiAnti = -2 := by
  unfold swapExpect psiAnti
  simp [Fintype.sum_prod_type, Fin.sum_univ_two]
  norm_num

/-- **THE FOURTH WITNESS.** The exchange expectation does not factor through the
    complete Born data: the fermion and the hard-core boson agree on the square
    of every amplitude — hence on every occupancy view, which the Born family
    refines — and differ in the exchange sign. Derived through
    `nonFactoring_of_signChange`, not exhibited afresh: the exchange sign is
    phase-grade data, and modulus-grade views cannot read phase. -/
theorem nonfactoring_exchange_sign :
    NonFactoring (fun (c : Fin 2 × Fin 2) (ψ : TwoParticle) => (ψ c) ^ 2) swapExpect := by
  have h : swapExpect (fun c => exchangeFlip c * psiSym c) ≠ swapExpect psiSym := by
    rw [← psiAnti_eq_flip_mul, swapExpect_psiAnti, swapExpect_psiSym]
    norm_num
  exact nonFactoring_of_signChange exchangeFlip_sq swapExpect h

/-- The general consequence, free from the shape: no rule whatever computes the
    exchange sign from the complete Born distribution. -/
theorem exchange_sign_not_computable :
    ¬ ∃ g : (Fin 2 × Fin 2 → ℝ) → ℝ,
        ∀ ψ : TwoParticle, swapExpect ψ = g (fun c => (ψ c) ^ 2) :=
  not_computable_of_nonFactoring _ _ nonfactoring_exchange_sign

/-! ### The composition rule: statistics is re-derived, never stored -/

/-- **EHRENFEST–OPPENHEIMER, as a permutation parity.** Exchanging two composites
    of `n` constituents each — the permutation applying the composite-label swap
    to every constituent — has sign `(-1)^n`. A composite of an odd number of
    fermions is a fermion; of an even number, a boson. Statistics is a rule
    applied at every composition boundary to the total constituent count; no tier
    may export it as a flag. (The staked floor export `A mod 2` was refuted by
    H-1, ⁶Li and ⁷Li; the rule below is what replaces it.) -/
theorem composite_exchange_sign (n : ℕ) {β : Type*} [DecidableEq β] [Fintype β]
    {c₀ c₁ : β} (h : c₀ ≠ c₁) :
    Equiv.Perm.sign (Equiv.prodCongrRight (fun _ : Fin n => Equiv.swap c₀ c₁))
      = (-1) ^ n := by
  rw [Equiv.Perm.sign_prodCongrRight]
  simp [Equiv.Perm.sign_swap h]

/-! ### The cap rung -/

/-- **THE CAP, AS THE LEDGER HOLDS IT.** The occupation of every direction in the
    REG+ local state is at most one — enforced by TYPE (`occ` is `Bool`), and this
    lemma is the named witness of that enforcement, not a derivation of it. This
    is rung (ii) of the repaired meet criterion: what relativity is owed to
    discharge is the anticommutation that FORCES this cap; what the machine holds
    today is that the ledger never represents a violation of it. -/
theorem pauli_cap (s : Fin 64) (k : Fin 6) :
    (if Lattice.occ s k then 1 else 0 : ℕ) ≤ 1 := by
  split <;> omega

end CIRISOntology.Core
