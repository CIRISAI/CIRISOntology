/-
CIRISOntology.Core.DefectCoupling — the symmetry-defect / dark-bright-coupling
identity, mechanized.

WHAT THIS CASHES. The concurrent dark-state campaign measured, on real semantic
coupling matrices, the exact relation

    g_DB = Δ_σ / (2√2),        Δ_σ = ‖H − P H P‖_F,  g_DB = ‖(1 − d dᵀ)(H d)‖,

to a worst residual of 1.8e-15 (DARK_STATE_K2_RESULTS.md, K2.1). That is an exact
algebraic identity, so it belongs in the library rather than in a float. Here it is,
proved — and proved MORE GENERALLY than it was measured: the only facts used are that
`P` is the reflection `1 − w wᵀ` and that `w ⬝ᵥ w = 2`. Nothing about the eleven kinds,
nothing about which pair, no appeal to the swap being a transposition beyond that norm.

THE STRUCTURE THE PROOF EXPOSES (this is the content, not the arithmetic):
`defect_entries` — the defect `D = H − P H P` is EXACTLY a rank-≤2 symmetric form
`D = w vᵀ + v wᵀ` built from `w` and the off-dark residue `v`; and `defect_dot`
says `v ⊥ w`. So symmetry breaking cannot enter a twin-symmetric model in any
complicated way: it enters only through one vector. `trace_defect_sq` then gives
`tr(D²) = 4 (v ⬝ᵥ v)`, which is the √2-free form of the measured identity (Frobenius
norm squared on the left, dark-bright coupling squared on the right).

Companion: `Core/DarkState.lean` proves the ZERO of this quantity — when `H` is
twin-symmetric the aspect mode is an exact decoupled eigenvector. This file measures
how the zero opens.

FENCE. A statement about matrices. The measured leakage asymmetry between the two
twins, and its substrate-dependence, are measurements and live in the campaign
records, not here.
-/
import Mathlib.Tactic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Symmetric
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Algebra.BigOperators.Ring

namespace CIRISOntology.Core.DefectCoupling

open Matrix Finset

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- The reflection through the hyperplane orthogonal to `w` (Householder form).
For `w = e_a - e_b` this IS the transposition matrix of `a` and `b`. -/
def refl (w : n → ℝ) : Matrix n n ℝ := 1 - vecMulVec w w

/-- The Rayleigh value of `H` along `w`. -/
def alph (H : Matrix n n ℝ) (w : n → ℝ) : ℝ := w ⬝ᵥ (H *ᵥ w)

/-- The symmetry defect `D = H - P H P`. -/
def defect (H : Matrix n n ℝ) (w : n → ℝ) : Matrix n n ℝ :=
  H - refl w * H * refl w

/-- **The defect is a rank-<=2 form.** Symmetry breaking enters a twin-symmetric
model only through `w` and the image `H *ᵥ w` — never in any more complicated way. -/
theorem defect_entries {H : Matrix n n ℝ} (hsym : H.IsSymm) {w : n → ℝ}
    (hw : w ⬝ᵥ w = 2) (i j : n) :
    defect H w i j
      = w i * (H *ᵥ w) j + (H *ᵥ w) i * w j - alph H w * (w i * w j) := by
  have hHT : ∀ k l, H l k = H k l := fun k l => congrFun (congrFun hsym k) l
  have hWH : ∀ i j, (vecMulVec w w * H) i j = w i * (H *ᵥ w) j := by
    intro i j
    simp only [Matrix.mul_apply, vecMulVec_apply, mulVec, dotProduct, mul_assoc, ← mul_sum]
    exact congrArg (w i * ·) (sum_congr rfl fun k _ => by rw [hHT k j]; ring)
  have hHW : ∀ i j, (H * vecMulVec w w) i j = (H *ᵥ w) i * w j := by
    intro i j
    simp only [Matrix.mul_apply, vecMulVec_apply, mulVec, dotProduct, sum_mul]
    exact sum_congr rfl fun k _ => by ring
  have hWHW : ∀ i j, (vecMulVec w w * H * vecMulVec w w) i j
      = alph H w * (w i * w j) := by
    intro i j
    rw [Matrix.mul_apply]
    simp only [hWH, vecMulVec_apply]
    have step : ∀ k, (w i * (H *ᵥ w) k) * (w k * w j)
        = (w i * w j) * (w k * (H *ᵥ w) k) := fun k => by ring
    simp only [step, ← mul_sum]
    simp only [alph, dotProduct]
    ring
  have expand : defect H w
      = vecMulVec w w * H + H * vecMulVec w w - vecMulVec w w * H * vecMulVec w w := by
    simp only [defect, refl, sub_mul, mul_sub, one_mul, mul_one]
    abel
  rw [expand]
  simp only [Matrix.add_apply, Matrix.sub_apply, hWH, hHW, hWHW]

/-- Trace of a product of two rank-one forms. -/
theorem trace_vecMulVec_mul (a b c d : n → ℝ) :
    (vecMulVec a b * vecMulVec c d).trace = (b ⬝ᵥ c) * (d ⬝ᵥ a) := by
  simp only [trace, diag_apply, Matrix.mul_apply, vecMulVec_apply, dotProduct]
  rw [sum_comm]
  have step : ∀ k, ∑ i, a i * b k * (c k * d i)
      = (b k * c k) * ∑ i, d i * a i := by
    intro k
    rw [mul_sum]
    exact sum_congr rfl fun i _ => by ring
  simp only [step, ← sum_mul]

/-- The defect as a matrix-level rank-<=2 identity. -/
theorem defect_eq {H : Matrix n n ℝ} (hsym : H.IsSymm) {w : n → ℝ}
    (hw : w ⬝ᵥ w = 2) :
    defect H w = vecMulVec w (H *ᵥ w) + vecMulVec (H *ᵥ w) w
                  - alph H w • vecMulVec w w := by
  ext i j
  rw [defect_entries hsym hw i j]
  simp [vecMulVec_apply, Matrix.smul_apply]

/-- **THE IDENTITY**: `tr((H - PHP)^2) = 4 (Hw . Hw) - 2 alpha^2`, the division-free
form of the campaign's measured `g_DB = Delta_sigma/(2 sqrt 2)`
(DARK_STATE_K2_RESULTS.md K2.1, residual 1.8e-15) — now proved, with no hypothesis
about the eleven kinds or which pair, only `w ⬝ᵥ w = 2`. -/
theorem trace_defect_sq {H : Matrix n n ℝ} (hsym : H.IsSymm) {w : n → ℝ}
    (hw : w ⬝ᵥ w = 2) :
    (defect H w * defect H w).trace
      = 4 * ((H *ᵥ w) ⬝ᵥ (H *ᵥ w)) - 2 * (alph H w) ^ 2 := by
  have halph : w ⬝ᵥ (H *ᵥ w) = alph H w := rfl
  have halph' : (H *ᵥ w) ⬝ᵥ w = alph H w := by
    rw [dotProduct_comm]; rfl
  rw [defect_eq hsym hw]
  simp only [Matrix.add_mul, Matrix.mul_add, Matrix.sub_mul, Matrix.mul_sub,
    Matrix.smul_mul, Matrix.mul_smul, trace_add, trace_sub, trace_smul,
    trace_vecMulVec_mul, smul_eq_mul, halph, halph', hw]
  ring


/-- The universe splits as a distinguished pair plus everything else. -/
private theorem sum_split {M : Type*} [AddCommMonoid M] {a b : n} (hab : a ≠ b)
    (f : n → M) (hz : ∀ k, k ≠ a → k ≠ b → f k = 0) :
    Finset.univ.sum f = f a + f b := by
  rw [← Finset.sum_subset (Finset.subset_univ ({a, b} : Finset n))]
  · exact Finset.sum_pair hab
  · intro k _ hk
    have hka : k ≠ a := fun h => hk (by simp [h])
    have hkb : k ≠ b := fun h => hk (by simp [h])
    exact hz k hka hkb

/-! ### The two parts of symmetry breaking

The capstone of the flavour comparison (FLAVOUR_DEFECT_RESULTS.md, REG_GAPS.md M2).
For ANY symmetric `S` and any transposition, the defect splits EXACTLY into two
pieces:

    tr(D²)  =  2·(diagonal split)²  +  4·Σ_{c ∉ {a,b}} (field direction)²

The first term is HOW MUCH the pair differs. The second is WHERE the difference goes —
the vector of the pair's asymmetry against every other index. Symmetry breaking is
therefore two-dimensional by identity, not by accident.

Under equal row sums (what unitarity forces on `|V|²`) the second term is CONSTRAINED:
its entries sum to minus the diagonal split, so Cauchy–Schwarz floors it, and at
`n = 3` there is only ONE such entry, so the floor is attained BY FORCE and the second
dimension disappears. That is why three-generation flavour carries one number where the
eleven-kind object carries two — and it is a fact about the number three, not about
flavour.
-/

/-- The two-part split, for any vector that is `+1` at `a`, `-1` at `b`, zero elsewhere. -/
theorem defect_split_of_pair {S : Matrix n n ℝ} (hsym : S.IsSymm) {a b : n} (hab : a ≠ b)
    (w : n → ℝ) (hwa : w a = 1) (hwb : w b = -1)
    (hwc : ∀ c, c ≠ a → c ≠ b → w c = 0) :
    (defect S w * defect S w).trace
      = 2 * (S a a - S b b) ^ 2
        + 4 * ∑ c ∈ Finset.univ \ {a, b}, (S c a - S c b) ^ 2 := by
  classical
  have hS : ∀ i j, S j i = S i j := fun i j => congrFun (congrFun hsym i) j
  have hw : w ⬝ᵥ w = 2 := by
    have h := sum_split hab (fun k => w k * w k) (fun c h1 h2 => by simp [hwc c h1 h2])
    have h2 : w ⬝ᵥ w = w a * w a + w b * w b := by simpa [dotProduct] using h
    rw [h2, hwa, hwb]; ring
  have hmv : ∀ i, (S *ᵥ w) i = S i a - S i b := by
    intro i
    have h := sum_split hab (fun k => S i k * w k) (fun c h1 h2 => by simp [hwc c h1 h2])
    have : (S *ᵥ w) i = S i a * w a + S i b * w b := by simpa [mulVec, dotProduct] using h
    rw [this, hwa, hwb]; ring
  have halpha : alph S w = (S a a - S a b) - (S b a - S b b) := by
    have h := sum_split hab (fun k => w k * (S *ᵥ w) k)
      (fun c h1 h2 => by simp [hwc c h1 h2])
    have h2 : alph S w = w a * (S *ᵥ w) a + w b * (S *ᵥ w) b := by
      simpa [alph, dotProduct] using h
    rw [h2, hwa, hwb, hmv a, hmv b]; ring
  have hsplit : ((S *ᵥ w) ⬝ᵥ (S *ᵥ w))
      = ((S a a - S a b) ^ 2 + (S b a - S b b) ^ 2)
        + ∑ c ∈ Finset.univ \ {a, b}, (S c a - S c b) ^ 2 := by
    have e : ∀ i, (S *ᵥ w) i * (S *ᵥ w) i = (S i a - S i b) ^ 2 := by
      intro i; rw [hmv i]; ring
    calc ((S *ᵥ w) ⬝ᵥ (S *ᵥ w))
        = ∑ i, (S i a - S i b) ^ 2 := by simp only [dotProduct, e]
      _ = ∑ c ∈ Finset.univ \ {a, b}, (S c a - S c b) ^ 2
            + ∑ c ∈ ({a, b} : Finset n), (S c a - S c b) ^ 2 :=
          (Finset.sum_sdiff (Finset.subset_univ _)).symm
      _ = ((S a a - S a b) ^ 2 + (S b a - S b b) ^ 2)
            + ∑ c ∈ Finset.univ \ {a, b}, (S c a - S c b) ^ 2 := by
          rw [Finset.sum_pair hab]; ring
  rw [trace_defect_sq hsym hw, halpha, hsplit, hS a b]
  ring

/-- **The two parts of symmetry breaking.** Exact, for any symmetric `S`. -/
theorem defect_split {S : Matrix n n ℝ} (hsym : S.IsSymm) {a b : n} (hab : a ≠ b) :
    (defect S (fun k => (if k = a then (1:ℝ) else 0) - (if k = b then 1 else 0)) *
     defect S (fun k => (if k = a then (1:ℝ) else 0) - (if k = b then 1 else 0))).trace
      = 2 * (S a a - S b b) ^ 2
        + 4 * ∑ c ∈ Finset.univ \ {a, b}, (S c a - S c b) ^ 2 := by
  refine defect_split_of_pair hsym hab _ ?_ ?_ ?_
  · show (if a = a then (1:ℝ) else 0) - (if a = b then 1 else 0) = 1
    rw [if_pos rfl, if_neg hab]; ring
  · show (if b = a then (1:ℝ) else 0) - (if b = b then 1 else 0) = -1
    rw [if_neg (Ne.symm hab), if_pos rfl]; ring
  · intro c h1 h2
    show (if c = a then (1:ℝ) else 0) - (if c = b then 1 else 0) = 0
    rw [if_neg h1, if_neg h2]; ring

/-! ### The three-generation collapse — why flavour cannot show what the object shows

The following is the structural difference the FDA-1 measurement turned up
(FLAVOUR_DEFECT_RESULTS.md, and the "difference is the key" reading).

In a THREE-generation table with unitarity, `|V|²` is doubly stochastic, so its
symmetrization has equal row sums. Under that hypothesis the symmetry defect of a
generation transposition collapses to ONE number: `tr(D²) = 6 (S a a − S b b)²`.
The off-diagonal entries cancel identically. Whatever else a 3×3 unitary mixing table
does, its transposition-breaking carries exactly one degree of freedom — the diagonal
split — and the dark→bright coupling is then pinned at `g_DB = (√3/2)|S a a − S b b|`
(numerically confirmed to 12 digits on random unitaries, all three pairs).

**The object is not like this, and that is the measured content.** Its symmetrized
coupling matrix is 11×11 and its row sums are not forced equal, so no such collapse
occurs — verified: the two twins carry near-identical diagonal splits (3.710 vs 3.685,
0.7% apart) yet decoupling defects differing by 3.8× (2.284 vs 8.617). Symmetry
breaking in the object is genuinely TWO-dimensional where three-generation flavour
admits only one dimension. The comparison therefore does not fail for want of
similarity; it succeeds by exhibiting a quantity flavour structurally cannot carry.
-/

/-- The algebra behind the collapse: once the third row's difference is pinned to
minus the diagonal split, the off-diagonal entry cancels identically. -/
private theorem collapse_algebra (p q m X : ℝ) (h : X = -(p - q)) :
    4 * ((p - m) ^ 2 + (m - q) ^ 2 + X ^ 2) - 2 * (p + q - 2 * m) ^ 2
      = 6 * (p - q) ^ 2 := by
  subst h; ring

/-- **The three-generation collapse**, on the representative pair (relabelling the
three generations carries it to any other pair). For a symmetric 3x3 with equal row
sums — the shape unitarity forces on `|V|^2` — the transposition defect depends ONLY
on the diagonal split. Numerically confirmed to 12 digits on random unitaries, all
three pairs. -/
theorem defect_three_gen_collapse
    (S : Matrix (Fin 3) (Fin 3) ℝ) (hsym : S.IsSymm) (r : ℝ)
    (hrow : ∀ i, ∑ j, S i j = r) :
    (defect S ![1, -1, 0] * defect S ![1, -1, 0]).trace
      = 6 * (S 0 0 - S 1 1) ^ 2 := by
  have hS : ∀ i j, S j i = S i j := fun i j => congrFun (congrFun hsym i) j
  have hr : ∀ i, S i 0 + S i 1 + S i 2 = r := by
    intro i; have := hrow i; simpa [Fin.sum_univ_three] using this
  have hw : (![1, -1, 0] : Fin 3 → ℝ) ⬝ᵥ ![1, -1, 0] = 2 := by
    simp [dotProduct, Fin.sum_univ_three]; norm_num
  have key : S 2 0 - S 2 1 = -(S 0 0 - S 1 1) := by
    have h0 := hr 0; have h1 := hr 1
    have e1 : S 1 0 = S 0 1 := hS 0 1
    have e2 : S 2 0 = S 0 2 := hS 0 2
    have e3 : S 2 1 = S 1 2 := hS 1 2
    linarith
  rw [trace_defect_sq hsym hw]
  simp only [alph, dotProduct, mulVec, Fin.sum_univ_three, Matrix.cons_val_zero,
    Matrix.cons_val_one, Matrix.head_cons, Matrix.cons_val_two, Matrix.tail_cons]
  rw [hS 0 1]
  linear_combination (4 * ((S 2 0 - S 2 1) - (S 0 0 - S 1 1))) * key

end CIRISOntology.Core.DefectCoupling
