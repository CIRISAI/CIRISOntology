/-
CIRISOntology.Core.BellCeiling — THE IDEAL QUANTUM CEILING of the Logos Bell
test: the five-qubit ring graph state's whole-only share is exactly 5·log 2,
the absolute maximum the five-slot space allows, two full bits above the
classical cap.

`Core.ShareK` proved the cap: every classical five-slot state with one uniform
pair marginal has share at most (5 − 2)·log 2 = 3·log 2
(`shareK_le_of_pair_uniform`). That file recorded the quantum ceiling as the
next brick and did not claim it. This file supplies it.

  * `psiC5`, `PsiC5` — the C5 ring graph state, amplitude
    2^(−5/2)·(−1)^(Σ over ring edges), and its density operator
    ψψᴴ. `isDensity_PsiC5`: it is a density.
  * `vnEntropy_PsiC5` — the whole reads ZERO entropy. Route: `ψψᴴ = M·Mᴴ` for
    the column `M`, so Weinstein–Aronszajn
    (`vnEntropy_mul_conjTranspose_comm`, `Core.EntropyIneq`) hands the
    spectrum to the 1×1 matrix `Mᴴ·M = ‖ψ‖² = 1`, whose entropy is 0.
    No eigenvector is ever exhibited.
  * `pairPtr_PsiC5` — TWO-UNIFORMITY: every pair partial trace at distinct
    slots is (1/4)·1, maximally mixed. Each pair reads a full 2·log 2 while
    the whole reads 0 — the non-monotonicity that has no classical analogue.
  * `pairPtr_mixed5_eq_PsiC5` — the maximally mixed state carries EXACTLY the
    same pair data, at every pair of slots including i = j (which the
    envelope's quantifier reaches, and where the shared value is the
    single-slot maximally mixed reading, not (1/4)·1).
  * `bell_ceiling` — `qShareK ΨC5 = 5·log 2`, and
    `bell_ceiling_exceeds_cap` — `3·log 2 < qShareK ΨC5`. The envelope's top
    is the Gibbs bound log 32, attained by the maximally mixed member; the
    state itself sits at 0; the share is the full gap.
  * `qShareK_max_five` — the ceiling is not merely reached but is THE MAXIMUM:
    `5·log 2` is the greatest whole-only share any five-slot quantum state can
    have. Attainment from `bell_ceiling`, the upper half from
    `qShareK_le_log_card` (`Core.ShareK`). The quantum bound is exactly tight;
    the classical cap, as noted below, is not.

METHOD, stated plainly. The combinatorial core — that the C5 sign structure
makes every pair reduction maximally mixed — is discharged by `decide` over
the five explicit bits (`vec5`, `sum5`): 25 slot pairs × 16 index quadruples
× 32 states, as an INTEGER identity (`signF_sum`), with the real/𝕜 scalars
factored out first. The same integer closed form is verified for the
maximally mixed state (`mixF_sum`), so the two states' pair data agree by a
computation neither side can fudge. `decide` uses only the kernel; no
`native_decide`, no added axioms.

SCOPE. Proved here: the items above, exact, over any `RCLike` field. NOT here,
and said plainly: any statement about hardware, and the tight classical
maximum at k = 5 (the cap of `Core.ShareK` is an upper bound; the best
classical value we know is 2·log 2, exact-computed and not mechanized). The
gap this file proves is between the IDEAL quantum state and the PROVED
classical cap; it is not a measurement.

Mathlib survey: `Equiv.sum_comp` and `Fintype.sum_prod_type` carry the
five-bit coordinatization; `Matrix.det_one_sub_mul_comm` reaches this file
only through `Core.EntropyIneq`'s Weinstein–Aronszajn wrapper;
`IsGreatest.csSup_eq` closes the envelope; the rest is `Core.Share*`
machinery. No gaps to port.
-/
import CIRISOntology.Core.EntropyIneq

namespace CIRISOntology.Core

open Matrix
open scoped BigOperators ComplexOrder

/-! ### Five bits, explicitly

Everything finite below is checked by `decide`. That is only possible if the
state space is presented as five independent bits rather than as a function
type, so we fix the coordinatization once. -/

/-- Five explicit bits, as a point of the five-slot state space. -/
def vec5 (a p q r s : Bool) : Fin 5 → Bool
  | 0 => a
  | 1 => p
  | 2 => q
  | 3 => r
  | 4 => s

/-- The five-bit coordinatization of the five-slot state space. -/
def bits5 : (Bool × Bool × Bool × Bool × Bool) ≃ (Fin 5 → Bool) where
  toFun t := vec5 t.1 t.2.1 t.2.2.1 t.2.2.2.1 t.2.2.2.2
  invFun x := (x 0, x 1, x 2, x 3, x 4)
  left_inv := by rintro ⟨a, p, q, r, s⟩; rfl
  right_inv := by intro x; funext m; fin_cases m <;> rfl

/-- Any sum over the five-slot state space is the five-fold bit sum. This is
    the bridge that turns every finite claim below into a `decide`. -/
lemma sum5 {M : Type*} [AddCommMonoid M] (f : (Fin 5 → Bool) → M) :
    ∑ x : Fin 5 → Bool, f x
      = ∑ a : Bool, ∑ p : Bool, ∑ q : Bool, ∑ r : Bool, ∑ s : Bool,
          f (vec5 a p q r s) := by
  rw [← Equiv.sum_comp bits5 f]
  simp only [Fintype.sum_prod_type]
  rfl

lemma card_five_slots : Fintype.card (Fin 5 → Bool) = 32 := by
  simp [Fintype.card_fun]

/-- Updating one slot, in the shape `decide` can evaluate. -/
def updBit (i : Fin 5) (v : Bool) (x : Fin 5 → Bool) : Fin 5 → Bool :=
  fun m => if m = i then v else x m

lemma updBit_eq_update (i : Fin 5) (v : Bool) (x : Fin 5 → Bool) :
    updBit i v x = Function.update x i v := by
  funext m
  simp [updBit, Function.update_apply]

/-! ### The C5 ring graph state -/

/-- The C5 quadratic form on five bits: the ring's edge sum, mod 2. Edges are
    01, 12, 23, 34, 40 — written out rather than indexed, so that `decide`
    never meets `Fin` arithmetic. -/
def qform (a p q r s : Bool) : Bool :=
  xor (a && p) (xor (p && q) (xor (q && r) (xor (r && s) (s && a))))

/-- The ring parity of a five-slot state. -/
def c5parity (x : Fin 5 → Bool) : Bool := qform (x 0) (x 1) (x 2) (x 3) (x 4)

/-- The graph state's sign, as an integer, so the whole combinatorial core is
    an integer computation with no scalars in it. -/
def sgnZ (x : Fin 5 → Bool) : ℤ := if c5parity x then -1 else 1

lemma sgnZ_mul_self (x : Fin 5 → Bool) : sgnZ x * sgnZ x = 1 := by
  unfold sgnZ
  split <;> norm_num

variable {𝕜 : Type*} [RCLike 𝕜]

/-- THE FIVE-QUBIT RING GRAPH STATE: amplitude 2^(−5/2)·(−1)^(edge sum). -/
noncomputable def psiC5 : (Fin 5 → Bool) → 𝕜 :=
  fun x => (((sgnZ x : ℝ) / Real.sqrt 32 : ℝ) : 𝕜)

/-- Its density operator, ψψᴴ. -/
noncomputable def PsiC5 : Matrix (Fin 5 → Bool) (Fin 5 → Bool) 𝕜 :=
  Matrix.vecMulVec psiC5 (star psiC5)

lemma star_psiC5 (x : Fin 5 → Bool) : star (psiC5 (𝕜 := 𝕜) x) = psiC5 x := by
  rw [psiC5, RCLike.star_def, RCLike.conj_ofReal]

/-- Every entry of the density operator, with the normalization discharged:
    a signed rational, no square roots left. -/
lemma PsiC5_apply (x y : Fin 5 → Bool) :
    PsiC5 (𝕜 := 𝕜) x y = ((sgnZ x * sgnZ y : ℤ) : 𝕜) / 32 := by
  have hs : Real.sqrt 32 * Real.sqrt 32 = 32 := Real.mul_self_sqrt (by norm_num)
  have hreal : ((sgnZ x : ℝ) / Real.sqrt 32) * ((sgnZ y : ℝ) / Real.sqrt 32)
      = ((sgnZ x * sgnZ y : ℤ) : ℝ) / 32 := by
    rw [div_mul_div_comm, hs]
    push_cast
    ring
  show psiC5 x * star (psiC5 (𝕜 := 𝕜) y) = _
  rw [star_psiC5, psiC5, psiC5, ← RCLike.ofReal_mul, hreal]
  push_cast
  ring

lemma PsiC5_diag (x : Fin 5 → Bool) : PsiC5 (𝕜 := 𝕜) x x = 1 / 32 := by
  rw [PsiC5_apply, sgnZ_mul_self]
  norm_num

/-- The graph state is a density operator. -/
theorem isDensity_PsiC5 : IsDensity (PsiC5 (𝕜 := 𝕜)) := by
  constructor
  · exact posSemidef_vecMulVec_star psiC5
  · have : (PsiC5 (𝕜 := 𝕜)).trace = ∑ _x : Fin 5 → Bool, (1 / 32 : 𝕜) := by
      simp only [Matrix.trace, Matrix.diag]
      exact Finset.sum_congr rfl fun x _ => PsiC5_diag x
    rw [this, Finset.sum_const, Finset.card_univ, card_five_slots, nsmul_eq_mul]
    norm_num

/-! ### The whole reads zero

The purity of `ψψᴴ` is read off its complementary spectrum: `ψψᴴ = M·Mᴴ` for
the column `M`, and `Mᴴ·M` is the 1×1 matrix `‖ψ‖² = 1`. Weinstein–Aronszajn
(`Core.EntropyIneq`) equates their entropies. No eigenvector is exhibited. -/

/-- The state as a single column. -/
noncomputable def colC5 : Matrix (Fin 5 → Bool) Unit 𝕜 :=
  Matrix.of fun x _ => psiC5 x

private lemma col_mul_conjTranspose :
    (colC5 (𝕜 := 𝕜)) * (colC5 (𝕜 := 𝕜))ᴴ = PsiC5 := by
  ext x y
  simp only [Matrix.mul_apply, Matrix.conjTranspose_apply, colC5, Matrix.of_apply,
    Finset.univ_unique, Finset.sum_singleton, PsiC5, Matrix.vecMulVec_apply,
    Pi.star_apply]

private lemma conjTranspose_mul_col :
    (colC5 (𝕜 := 𝕜))ᴴ * (colC5 (𝕜 := 𝕜)) = 1 := by
  ext u u'
  have huu : u = u' := Subsingleton.elim u u'
  subst huu
  have hterm : ∀ x : Fin 5 → Bool,
      star (psiC5 (𝕜 := 𝕜) x) * psiC5 x = (1 / 32 : 𝕜) := by
    intro x
    rw [star_psiC5]
    have := PsiC5_diag (𝕜 := 𝕜) x
    rw [PsiC5, Matrix.vecMulVec_apply, Pi.star_apply, star_psiC5] at this
    exact this
  simp only [Matrix.mul_apply, Matrix.conjTranspose_apply, colC5, Matrix.of_apply,
    Matrix.one_apply_eq]
  rw [Finset.sum_congr rfl fun x _ => hterm x, Finset.sum_const, Finset.card_univ,
    card_five_slots, nsmul_eq_mul]
  norm_num

private lemma vnEntropy_one_unit : vnEntropy (1 : Matrix Unit Unit 𝕜) = 0 := by
  have h1 : (1 : Matrix Unit Unit 𝕜) = diagEmbed (fun _ : Unit => (1 : ℝ)) := by
    rw [diagEmbed]
    simp
  rw [h1, vnEntropy_diagEmbed]
  simp [entropy]

/-- THE WHOLE READS ZERO: the graph state is pure. -/
theorem vnEntropy_PsiC5 : vnEntropy (PsiC5 (𝕜 := 𝕜)) = 0 := by
  rw [← col_mul_conjTranspose, vnEntropy_mul_conjTranspose_comm,
    conjTranspose_mul_col, vnEntropy_one_unit]

/-! ### The pair data, by finite computation

Both the graph state and the maximally mixed state have every pair partial
trace of the form (integer)/32. The integers are computed by `decide` over
the five bits, and they agree — so the two states sit in the same pair
envelope. -/

/-- The graph state's integer weight at one point of the pair sum. -/
def signF (i j : Fin 5) (b' c' : Bool) (x : Fin 5 → Bool) : ℤ :=
  sgnZ x * sgnZ (updBit j c' (updBit i b' x))

/-- The maximally mixed state's integer weight at the same point. -/
def mixF (i j : Fin 5) (b' c' : Bool) (x : Fin 5 → Bool) : ℤ :=
  if updBit j c' (updBit i b' x) = x then 1 else 0

/-- The closed form both weights sum to. At distinct slots it is 8 on the
    diagonal of the pair index and 0 off it — that is two-uniformity, once
    divided by 32. At i = j the pair partial trace degenerates to the
    single-slot reading, and the value is 16 (i.e. 1/2). -/
def pairWeight (i j : Fin 5) (b c b' c' : Bool) : ℤ :=
  if i = j then (if b = c ∧ c' = b then 16 else 0)
  else (if b = b' ∧ c = c' then 8 else 0)

set_option maxRecDepth 100000 in
set_option maxHeartbeats 1000000 in
/-- THE COMBINATORIAL CORE, machine-checked: the C5 sign sum over any pair of
    slots. Every one of 25 × 16 × 32 cases is evaluated by the kernel. -/
theorem signF_sum : ∀ (i j : Fin 5) (b c b' c' : Bool),
    (∑ a : Bool, ∑ p : Bool, ∑ q : Bool, ∑ r : Bool, ∑ s : Bool,
      (if vec5 a p q r s i = b ∧ vec5 a p q r s j = c then
        signF i j b' c' (vec5 a p q r s) else 0))
      = pairWeight i j b c b' c' := by decide

set_option maxRecDepth 100000 in
set_option maxHeartbeats 1000000 in
/-- The same closed form for the maximally mixed state. -/
theorem mixF_sum : ∀ (i j : Fin 5) (b c b' c' : Bool),
    (∑ a : Bool, ∑ p : Bool, ∑ q : Bool, ∑ r : Bool, ∑ s : Bool,
      (if vec5 a p q r s i = b ∧ vec5 a p q r s j = c then
        mixF i j b' c' (vec5 a p q r s) else 0))
      = pairWeight i j b c b' c' := by decide

/-- A pair partial trace whose entries are (integer)/32 is the five-bit sum of
    those integers, over 32. -/
private lemma pairPtr_entry (i j : Fin 5) (b c b' c' : Bool)
    (ρ : Matrix (Fin 5 → Bool) (Fin 5 → Bool) 𝕜) (F : (Fin 5 → Bool) → ℤ)
    (hF : ∀ x : Fin 5 → Bool,
      ρ x (updBit j c' (updBit i b' x)) = ((F x : ℤ) : 𝕜) / 32) :
    pairPtr i j ρ (b, c) (b', c')
      = (((∑ a : Bool, ∑ p : Bool, ∑ q : Bool, ∑ r : Bool, ∑ s : Bool,
            (if vec5 a p q r s i = b ∧ vec5 a p q r s j = c
             then F (vec5 a p q r s) else 0)) : ℤ) : 𝕜) / 32 := by
  have hstep : ∀ x : Fin 5 → Bool,
      ρ x (Function.update (Function.update x i b') j c') = ((F x : ℤ) : 𝕜) / 32 := by
    intro x
    rw [← updBit_eq_update, ← updBit_eq_update]
    exact hF x
  show (∑ x ∈ Finset.univ.filter (fun x : Fin 5 → Bool => x i = b ∧ x j = c),
      ρ x (Function.update (Function.update x i b') j c')) = _
  rw [Finset.sum_congr rfl fun x _ => hstep x, ← Finset.sum_div, Finset.sum_filter,
    sum5 (fun x => if x i = b ∧ x j = c then ((F x : ℤ) : 𝕜) else 0)]
  congr 1
  push_cast
  exact Finset.sum_congr rfl fun _ _ => Finset.sum_congr rfl fun _ _ =>
    Finset.sum_congr rfl fun _ _ => Finset.sum_congr rfl fun _ _ =>
      Finset.sum_congr rfl fun _ _ => by split <;> simp

/-- The graph state's pair partial traces, entry by entry. -/
lemma pairPtr_PsiC5_apply (i j : Fin 5) (b c b' c' : Bool) :
    pairPtr i j (PsiC5 (𝕜 := 𝕜)) (b, c) (b', c')
      = ((pairWeight i j b c b' c' : ℤ) : 𝕜) / 32 := by
  rw [pairPtr_entry i j b c b' c' (PsiC5 (𝕜 := 𝕜)) (signF i j b' c')
    (fun x => by rw [PsiC5_apply]; rfl), signF_sum]

/-- The maximally mixed five-slot state. -/
noncomputable def mixed5 : Matrix (Fin 5 → Bool) (Fin 5 → Bool) 𝕜 :=
  diagEmbed (fun _ : Fin 5 → Bool => (1 / 32 : ℝ))

private lemma isProb_uniform32 : IsProb (fun _ : Fin 5 → Bool => (1 / 32 : ℝ)) := by
  constructor
  · intro _; norm_num
  · rw [Finset.sum_const, Finset.card_univ, card_five_slots, nsmul_eq_mul]
    norm_num

theorem isDensity_mixed5 : IsDensity (mixed5 (𝕜 := 𝕜)) :=
  isDensity_diagEmbed isProb_uniform32

/-- The maximally mixed state's pair partial traces, entry by entry — the same
    closed form as the graph state's. -/
lemma pairPtr_mixed5_apply (i j : Fin 5) (b c b' c' : Bool) :
    pairPtr i j (mixed5 (𝕜 := 𝕜)) (b, c) (b', c')
      = ((pairWeight i j b c b' c' : ℤ) : 𝕜) / 32 := by
  rw [pairPtr_entry i j b c b' c' (mixed5 (𝕜 := 𝕜)) (mixF i j b' c') (fun x => ?_),
    mixF_sum]
  rw [mixed5, diagEmbed, Matrix.diagonal_apply, mixF]
  rcases eq_or_ne x (updBit j c' (updBit i b' x)) with h | h
  · rw [if_pos h, if_pos h.symm]
    push_cast
    norm_num
  · rw [if_neg h, if_neg fun hc => h hc.symm]
    simp

/-- THE TWO STATES CARRY THE SAME PAIR DATA, at every pair of slots — the
    quantifier the envelope uses, `i = j` included. -/
theorem pairPtr_mixed5_eq_PsiC5 (i j : Fin 5) :
    pairPtr i j (mixed5 (𝕜 := 𝕜)) = pairPtr i j (PsiC5 (𝕜 := 𝕜)) := by
  ext bc bc'
  obtain ⟨b, c⟩ := bc
  obtain ⟨b', c'⟩ := bc'
  rw [pairPtr_mixed5_apply, pairPtr_PsiC5_apply]

/-- TWO-UNIFORMITY: at distinct slots the graph state's pair partial trace is
    maximally mixed. Each pair reads a full 2·log 2 while the whole reads 0.
    No classical five-slot state can do this — `entropy_map_le` forbids a view
    from reading more than the whole. -/
theorem pairPtr_PsiC5 {i j : Fin 5} (hij : i ≠ j) :
    pairPtr i j (PsiC5 (𝕜 := 𝕜)) = (1 / 4 : 𝕜) • 1 := by
  ext bc bc'
  obtain ⟨b, c⟩ := bc
  obtain ⟨b', c'⟩ := bc'
  rw [pairPtr_PsiC5_apply, pairWeight, if_neg hij, Matrix.smul_apply,
    Matrix.one_apply]
  by_cases h : b = b' ∧ c = c'
  · obtain ⟨rfl, rfl⟩ := h
    rw [if_pos ⟨rfl, rfl⟩, if_pos rfl, smul_eq_mul]
    norm_num
  · have hne : ((b, c) : Bool × Bool) ≠ (b', c') := fun hc =>
      h ⟨congrArg Prod.fst hc, congrArg Prod.snd hc⟩
    rw [if_neg h, if_neg hne, smul_zero]
    norm_num

/-! ### The ceiling -/

private lemma entropy_uniform32 :
    entropy (fun _ : Fin 5 → Bool => (1 / 32 : ℝ)) = 5 * Real.log 2 := by
  have hlog : Real.log ((1 : ℝ) / 32) = -(5 * Real.log 2) := by
    rw [one_div, Real.log_inv, show (32 : ℝ) = 2 ^ 5 by norm_num, Real.log_pow]
    norm_num
  unfold entropy
  rw [Finset.sum_const, Finset.card_univ, card_five_slots, nsmul_eq_mul, hlog]
  push_cast
  ring

private lemma log_card_five_slots :
    Real.log (Fintype.card (Fin 5 → Bool)) = 5 * Real.log 2 := by
  rw [card_five_slots, show ((32 : ℕ) : ℝ) = 2 ^ 5 by norm_num, Real.log_pow]
  norm_num

private lemma envelope_top :
    IsGreatest (qPairEnvelopeK (PsiC5 (𝕜 := 𝕜))) (5 * Real.log 2) := by
  constructor
  · refine ⟨mixed5, isDensity_mixed5, pairPtr_mixed5_eq_PsiC5, ?_⟩
    rw [mixed5, vnEntropy_diagEmbed]
    exact entropy_uniform32
  · rintro h ⟨σ, hσ, -, rfl⟩
    calc vnEntropy σ ≤ Real.log (Fintype.card (Fin 5 → Bool)) :=
          vnEntropy_le_log_card hσ
      _ = 5 * Real.log 2 := log_card_five_slots

/-- THE IDEAL QUANTUM CEILING: the five-qubit ring graph state's whole-only
    share is exactly 5·log 2 — the whole of the five-slot space's capacity.
    The state is pure, so it contributes nothing to the entropy subtracted;
    its pair data is that of the maximally mixed state, so the envelope's top
    is the unconstrained Gibbs bound. -/
theorem bell_ceiling : qShareK (PsiC5 (𝕜 := 𝕜)) = 5 * Real.log 2 := by
  rw [qShareK, envelope_top.csSup_eq, vnEntropy_PsiC5, sub_zero]

/-- THE BELL GAP: the ideal quantum value is strictly above the classical cap
    that `shareK_le_of_pair_uniform` proves for every five-slot classical
    state with a uniform pair marginal. Two full bits of daylight, both sides
    proved before any measurement. -/
theorem bell_ceiling_exceeds_cap :
    (3 : ℝ) * Real.log 2 < qShareK (PsiC5 (𝕜 := 𝕜)) := by
  rw [bell_ceiling]
  have h2 : 0 < Real.log 2 := Real.log_pos (by norm_num)
  linarith

/-- THE CEILING IS ATTAINED, AND IT IS THE MAXIMUM: at k = 5, `5·log 2` is
    exactly the greatest whole-only share any quantum state can have. The upper
    half is `qShareK_le_log_card` (nothing exceeds the space's capacity); the
    attainment is `bell_ceiling` (the ring graph state reaches it).

    Read against `shareK_le_of_pair_uniform`, this is the shape of the Bell
    structure at five slots: the quantum functional saturates its bound, the
    classical one is capped 2·log 2 lower — and, since the true classical
    maximum is lower still (2·log 2, exact-computed, not mechanized), the real
    gap is wider than the machine-checked one. Only the machine-checked gap is
    claimed. -/
theorem qShareK_max_five :
    IsGreatest {x : ℝ | ∃ ρ : Matrix (Fin 5 → Bool) (Fin 5 → Bool) 𝕜,
      IsDensity ρ ∧ qShareK ρ = x} (5 * Real.log 2) := by
  constructor
  · exact ⟨PsiC5, isDensity_PsiC5, bell_ceiling⟩
  · rintro x ⟨ρ, hρ, rfl⟩
    have h := qShareK_le_log_card (k := 5) hρ
    push_cast at h
    exact h

end CIRISOntology.Core
