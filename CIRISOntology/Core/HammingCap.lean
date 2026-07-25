/-
CIRISOntology.Core.HammingCap — THE TIGHTENED CLASSICAL CAP: from four slots
up, a pair-uniform classical state's whole-only share is at most (k − 3)·log 2,
one full bit below the cap of `Core.ShareK`. At k = 5 this is exactly the true
classical maximum, so the Bell gap is now machine-checked at its real width.

`Core.ShareK` proved `shareK ≤ (k − 2)·log 2` for a pair-uniform classical
state, by bounding the envelope's top at log(card) and subtracting the pair
entropy. That cap is TIGHT at k = 3 — the parity state saturates it
(`temporal_third_saturates`) — and NOT tight from k = 4 up, because it never
uses the state's own entropy beyond a single pair reading. This file supplies
what it was missing: pair-uniformity forces the whole's entropy up, and the
forcing is the Hamming bound.

  * `kern_eq`, `kern_real` — THE REPRODUCING KERNEL of the four-bit cube:
    summed over all sixteen characters, χ(x)·χ(y) is 16 on the diagonal and 0
    off it. Discharged by `decide` over the 256 bit patterns as an integer
    identity; no `native_decide`, no added axioms.
  * `sum_chr1_zero`, `sum_chr2_zero` — pair-uniformity kills every character of
    weight one and two: ten of the sixteen Fourier coefficients vanish.
  * `inversion` — so a pair-uniform four-bit state is carried entirely by its
    five surviving characters: `16·p(x) = 1 + Σ c_a·χ_a(x)`.
  * `sum_sq_le_eighth` — THE COLLISION BOUND: `Σ p² ≤ 1/8`. The five survivors
    are ORTHONORMAL in L²(p) — every product of two distinct ones is a
    character of weight one or two, which pair-uniformity kills — so Bessel's
    inequality against the constant function caps `Σ c_a² ≤ 1`, and inversion
    turns that into the collision bound. Nonnegativity of `p` enters exactly
    once, as the termwise nonnegativity of the Bessel remainder.
  * `entropy_ge_three_log_two` — THE BASE CASE: every pair-uniform four-bit
    state carries at least 3·log 2 of entropy. The collision bound plus
    `entropy_ge_of_sum_sq_le` (`Core.Share`), which is Shannon-dominates-
    Rényi-2 in the only form needed.
  * `shareK_le_of_pair_uniform_four`, `shareK_le_of_four_pair_uniform` —
    the cap: `log 2` at k = 4, and `(k − 3)·log 2` for every k, by selecting
    four slots (`pairMarg_pushforward` keeps them pair-uniform) and running
    `entropy_map_le` once. The general form assumes only that SOME four slots
    have all six of their pair marginals uniform; nothing is assumed about the
    rest. `shareK_le_of_pair_uniform_ge_four` is the blanket-hypothesis
    corollary.

WHY THE BOUND IS THE HAMMING BOUND. A pair-uniform state is one whose Fourier
support avoids weights 1 and 2 — in coding terms, dual distance at least 3.
The Hamming bound then forces at least eight points' worth of mass, and the
eight-point uniform states (the dual-distance-3 codes, e.g. the even-weight
code on four bits) attain 3·log 2 exactly. The analytic proof above is that
counting argument in a form that survives fractional weights: the collision
probability, not the support size, is what pair-uniformity actually controls.

WHERE THE CAP IS TIGHT, AND WHERE IT IS MERELY TRUE. The bound (k − 3)·log 2
holds for every k. It EQUALS the true classical maximum exactly for
k = 4, 5, 6, 7, and is strictly loose from k = 8 on. The true maximum is not
the Hamming form at all but the ORTHOGONAL-ARRAY form

    max share = k·log 2 − log N₀(k),      N₀(k) = 4·⌈(k+1)/4⌉

(`scratchpad/temporal-share/HAMMING_FORM_SCAN.md`, with k = 5 also in
`CLASSICAL_MAX_K5.md`; EXACT-COMPUTED / argued there, NOT MECHANIZED). Since
N₀(k) ≥ 8 for every k ≥ 4, log N₀(k) ≥ 3·log 2 and this file's bound stays
valid everywhere; since N₀(k) = 8 exactly for k = 4…7, it is tight exactly
there. Read that as the honest two-tier statement: the UPPER bound is
machine-checked here, the ATTAINMENT is computed elsewhere, and only the upper
bound may be cited as proved.

DO NOT CONFUSE THIS WITH THE HAMMING CONJECTURE. The form
(k − ⌈log₂(k+1)⌉)·log 2 that motivated this work is FALSE from k = 8: a Paley
Hadamard matrix of order 12 gives a 12-point pair-uniform state with entropy
log 12 < log 16, beating the conjectured value. That form and this file's
(k − 3)·log 2 coincide only for k = 4…7, and they fail in opposite directions —
the Hamming form is too SMALL from k = 8 (hence false as a bound), while
(k − 3)·log 2 is too LARGE (hence true but loose). Nothing here proves the
Hamming conjecture, and nothing here needs to.

WHAT THIS DOES TO THE BELL GAP. At k = 5 the cap reads 2·log 2, which is the
true classical maximum, so the gap to `bell_ceiling`'s 5·log 2 is the full
3·log 2 rather than the 2·log 2 that `Core.ShareK` alone admits.

PRIOR ART — READ BEFORE ANNOUNCING ANYTHING FROM THIS FILE. Neither the problem
nor the route is ours. That the minimum entropy of k pairwise-independent
unbiased bits is log(k+1), and that it is attained exactly when a Hadamard
matrix of order k+1 exists, is Gavinsky and Pudlák (*On the Joint Entropy of
d-Wise-Independent Variables*, arXiv:1503.08154, Theorems 3.1/3.2/4.1, 2016),
proving a conjecture of Babai (2013) and extending Lancaster (*Ann. Math.
Statist.* 36:1313, 1965). The same polytope, the same Shannon-≥-Rényi-2 route
that `entropy_ge_of_sum_sq_le` mechanizes, and our exact case (µ=1/2, ν=1/4)
were independently set out by Albanna, Hillar, Sohl-Dickstein and DeWeese
(*Entropy* 19(8):427, 2017, Eqs. 15–21), who bracket the answer without closing
it. The orthogonal-array/Hadamard equivalence is Hedayat, Sloane and Stufken
(*Orthogonal Arrays*, 1999, Theorem 7.5, p. 148). Full adjudication with primary
sources: `scratchpad/temporal-share/HADAMARD_CONNECTION.md`.

WHAT THIS FILE ADDS, NARROWLY. Two things, and neither is the headline. First,
the k = 4 base case is log 8, which STRENGTHENS Gavinsky–Pudlák's log 5 at k = 4
by 0.678 bits — the published floor is not tight off k ≡ 3 (mod 4), and they do
not give the value there. Second, it is MECHANIZED, which none of the above is.
The general sharpening from log(k+1) to log(4⌈(k+1)/4⌉) is marked NOT FOUND IN
PRINT rather than new (one search pass; three is the house bar), and is neither
proved nor needed here.

AND THE LIMIT THAT GOES WITH IT: this file's bound is the best available ONLY
for k = 4…7. Written as k·log 2 − log 8 against Gavinsky–Pudlák's
k·log 2 − log(k+1), ours is strictly better at k = 4, 5, 6, ties at k = 7, and
is STRICTLY WORSE from k = 8 on, where log(k+1) > log 8. Do not cite
`shareK_le_of_four_pair_uniform` as the best known cap at large k; it is not.
At k ≡ 3 (mod 4) the exact value is equivalent to the Hadamard conjecture, open
since 1893 (smallest open case k = 667), so tightness in general is not a
tractable target and is not pursued.

SCOPE. Proved here: the items above, exact. NOT proved here, and said plainly:
any attainment claim (every "tight" above rests on unmechanized computation);
the exact maximum at any k ≥ 8 (the scan leaves k = 8 and k = 12 open even
unmechanized); and any statement about what hardware holds. The k = 3 case is
untouched and unchanged: `Core.ShareK`'s cap is already exact there, and this
file's base case does not reach it.

Mathlib survey: `Finset.sum_fiberwise` and `Finset.sum_fiberwise_of_maps_to`
carry the marginal bookkeeping; `Real.log_le_sub_one_of_pos` (through
`Core.Share`) carries the entropy step; `linear_combination` discharges the
sign algebra. No gaps to port.
-/
import CIRISOntology.Core.ShareK

namespace CIRISOntology.Core

open scoped BigOperators

/-! ### Four bits, explicitly -/

def vec4 (a b c d : Bool) : Fin 4 → Bool
  | 0 => a
  | 1 => b
  | 2 => c
  | 3 => d

def bits4 : (Bool × Bool × Bool × Bool) ≃ (Fin 4 → Bool) where
  toFun t := vec4 t.1 t.2.1 t.2.2.1 t.2.2.2
  invFun x := (x 0, x 1, x 2, x 3)
  left_inv := by rintro ⟨a, b, c, d⟩; rfl
  right_inv := by intro x; funext m; fin_cases m <;> rfl

lemma sum4 {M : Type*} [AddCommMonoid M] (f : (Fin 4 → Bool) → M) :
    ∑ x : Fin 4 → Bool, f x
      = ∑ a : Bool, ∑ b : Bool, ∑ c : Bool, ∑ d : Bool, f (vec4 a b c d) := by
  rw [← Equiv.sum_comp bits4 f]
  simp only [Fintype.sum_prod_type]
  rfl

lemma card_four_slots : Fintype.card (Fin 4 → Bool) = 16 := by
  simp [Fintype.card_fun]

lemma funext4 (x y : Fin 4 → Bool) :
    x = y ↔ (x 0 = y 0 ∧ x 1 = y 1 ∧ x 2 = y 2 ∧ x 3 = y 3) := by
  constructor
  · rintro rfl; exact ⟨rfl, rfl, rfl, rfl⟩
  · rintro ⟨h0, h1, h2, h3⟩
    funext m
    fin_cases m <;> assumption

/-! ### The sixteen characters of the four-bit cube -/

/-- The sign of a bit, as an integer — the form the kernel computation runs in. -/
def sZ (b : Bool) : ℤ := if b then -1 else 1

/-- The sign of a bit, as a real. -/
def sgn (b : Bool) : ℝ := if b then -1 else 1

lemma sgn_eq (b : Bool) : ((sZ b : ℤ) : ℝ) = sgn b := by
  cases b <;> norm_num [sZ, sgn]

/-- The total parity of a four-bit point. -/
def totB (x : Fin 4 → Bool) : Bool := xor (x 0) (xor (x 1) (xor (x 2) (x 3)))

/-- The four weight-one characters. -/
def chr1 (i : Fin 4) (x : Fin 4 → Bool) : ℝ := sgn (x i)

/-- The six weight-two characters. -/
def chr2 (i j : Fin 4) (x : Fin 4 → Bool) : ℝ := sgn (xor (x i) (x j))

/-- The weight-four character: total parity. -/
def chr4 (x : Fin 4 → Bool) : ℝ := sgn (totB x)

/-- The four weight-three characters — total parity with slot `i` cancelled
    out, which is exactly the product of the other three signs. -/
def chr3 (i : Fin 4) (x : Fin 4 → Bool) : ℝ := sgn (xor (x i) (totB x))

/-- The integer mirror of the reproducing kernel, in the eight bits, so that
    `decide` never meets `Fin` arithmetic. -/
def tot (a b c d : Bool) : Bool := xor a (xor b (xor c d))

def kern (a b c d a' b' c' d' : Bool) : ℤ :=
  1
  + (sZ a * sZ a' + sZ b * sZ b' + sZ c * sZ c' + sZ d * sZ d')
  + (sZ (xor a b) * sZ (xor a' b') + sZ (xor a c) * sZ (xor a' c')
     + sZ (xor a d) * sZ (xor a' d') + sZ (xor b c) * sZ (xor b' c')
     + sZ (xor b d) * sZ (xor b' d') + sZ (xor c d) * sZ (xor c' d'))
  + (sZ (tot a b c d) * sZ (tot a' b' c' d')
     + sZ (xor a (tot a b c d)) * sZ (xor a' (tot a' b' c' d'))
     + sZ (xor b (tot a b c d)) * sZ (xor b' (tot a' b' c' d'))
     + sZ (xor c (tot a b c d)) * sZ (xor c' (tot a' b' c' d'))
     + sZ (xor d (tot a b c d)) * sZ (xor d' (tot a' b' c' d')))

set_option maxRecDepth 100000 in
/-- THE REPRODUCING KERNEL, machine-checked: summed over all sixteen characters
    of the four-bit cube, χ(x)·χ(y) is 16 on the diagonal and 0 off it. All 256
    bit patterns are evaluated by the kernel as an integer identity. -/
theorem kern_eq : ∀ a b c d a' b' c' d' : Bool,
    kern a b c d a' b' c' d'
      = if a = a' ∧ b = b' ∧ c = c' ∧ d = d' then 16 else 0 := by decide

/-- The same identity in the reals, indexed by points rather than bits. -/
lemma kern_real (x y : Fin 4 → Bool) :
    1
    + (chr1 0 x * chr1 0 y + chr1 1 x * chr1 1 y + chr1 2 x * chr1 2 y
       + chr1 3 x * chr1 3 y)
    + (chr2 0 1 x * chr2 0 1 y + chr2 0 2 x * chr2 0 2 y + chr2 0 3 x * chr2 0 3 y
       + chr2 1 2 x * chr2 1 2 y + chr2 1 3 x * chr2 1 3 y + chr2 2 3 x * chr2 2 3 y)
    + (chr4 x * chr4 y + chr3 0 x * chr3 0 y + chr3 1 x * chr3 1 y
       + chr3 2 x * chr3 2 y + chr3 3 x * chr3 3 y)
      = if x = y then 16 else 0 := by
  have h := congrArg (fun z : ℤ => (z : ℝ))
    (kern_eq (x 0) (x 1) (x 2) (x 3) (y 0) (y 1) (y 2) (y 3))
  simp only [kern, tot] at h
  push_cast at h
  simp only [sgn_eq] at h
  simp only [chr1, chr2, chr3, chr4, totB]
  rcases eq_or_ne x y with rfl | hne
  · rw [if_pos ⟨rfl, rfl, rfl, rfl⟩] at h
    rw [if_pos rfl]
    linear_combination h
  · rw [if_neg fun hc => hne ((funext4 x y).mpr hc)] at h
    rw [if_neg hne]
    linear_combination h

/-! ### Pair-uniformity kills every character of weight one and two -/

/-- Averaging a function of a view against the state is averaging it against
    the view's own marginal. The same fiberwise grouping that carries
    `entropy_map_le`. -/
lemma sum_pushforward {X Y : Type*} [Fintype X] [Fintype Y] [DecidableEq Y]
    (π : X → Y) (p : X → ℝ) (f : Y → ℝ) :
    ∑ x, p x * f (π x) = ∑ y, pushforward π p y * f y := by
  rw [← Finset.sum_fiberwise Finset.univ π (fun x => p x * f (π x))]
  refine Finset.sum_congr rfl fun y _ => ?_
  rw [Finset.sum_congr rfl (fun x hx => by rw [(Finset.mem_filter.mp hx).2]),
    ← Finset.sum_mul]
  rfl

/-- A weight-one character reads zero against a state with a uniform pair
    marginal at that slot. -/
lemma sum_chr1_zero {p : (Fin 4 → Bool) → ℝ} {i j : Fin 4}
    (h : pairMarg i j p = fun _ => (1 : ℝ)/4) :
    ∑ x, p x * chr1 i x = 0 := by
  have hp := sum_pushforward (fun x : Fin 4 → Bool => (x i, x j)) p (fun bc => sgn bc.1)
  simp only [chr1]
  rw [hp]
  show ∑ bc : Bool × Bool, pairMarg i j p bc * sgn bc.1 = 0
  rw [h]
  simp only [Fintype.sum_prod_type, Fintype.sum_bool, sgn]
  norm_num

/-- A weight-two character reads zero against a state with that pair marginal
    uniform. -/
lemma sum_chr2_zero {p : (Fin 4 → Bool) → ℝ} {i j : Fin 4}
    (h : pairMarg i j p = fun _ => (1 : ℝ)/4) :
    ∑ x, p x * chr2 i j x = 0 := by
  have hp := sum_pushforward (fun x : Fin 4 → Bool => (x i, x j)) p
    (fun bc => sgn (xor bc.1 bc.2))
  simp only [chr2]
  rw [hp]
  show ∑ bc : Bool × Bool, pairMarg i j p bc * sgn (xor bc.1 bc.2) = 0
  rw [h]
  simp only [Fintype.sum_prod_type, Fintype.sum_bool, sgn]
  norm_num

/-! ### The characters multiply -/

lemma sgn_xor (a b : Bool) : sgn (xor a b) = sgn a * sgn b := by
  cases a <;> cases b <;> norm_num [sgn]

lemma sgn_mul_self (a : Bool) : sgn a * sgn a = 1 := by
  cases a <;> norm_num [sgn]

lemma chr4_mul_chr4 (x : Fin 4 → Bool) : chr4 x * chr4 x = 1 := sgn_mul_self _

lemma chr3_mul_self (i : Fin 4) (x : Fin 4 → Bool) : chr3 i x * chr3 i x = 1 :=
  sgn_mul_self _

/-- Weight four times weight three is weight one: the shared total parity
    cancels. -/
lemma chr4_mul_chr3 (i : Fin 4) (x : Fin 4 → Bool) :
    chr4 x * chr3 i x = chr1 i x := by
  simp only [chr4, chr3, chr1, sgn_xor]
  linear_combination (sgn (x i)) * (sgn_mul_self (totB x))

/-- Weight three times weight three is weight two: both total parities
    cancel. -/
lemma chr3_mul_chr3 (i j : Fin 4) (x : Fin 4 → Bool) :
    chr3 i x * chr3 j x = chr2 i j x := by
  simp only [chr3, chr2, sgn_xor]
  linear_combination (sgn (x i) * sgn (x j)) * (sgn_mul_self (totB x))

/-! ### Inversion: a pair-uniform state is carried by its five top characters -/

/-- `p` is pair-uniform: every pair of distinct slots reads the uniform
    marginal. This is the hypothesis the classical cap is stated under. -/
def PairUniform (p : (Fin 4 → Bool) → ℝ) : Prop :=
  ∀ i j : Fin 4, i ≠ j → pairMarg i j p = fun _ => (1 : ℝ)/4

/-- THE INVERSION FORMULA: a pair-uniform four-bit state is determined by its
    five surviving Fourier coefficients — the weight-four character and the
    four of weight three. Ten of the sixteen characters read zero, so the
    reproducing kernel collapses to these five plus the constant. -/
theorem inversion {p : (Fin 4 → Bool) → ℝ} (hp : IsProb p) (hu : PairUniform p)
    (x : Fin 4 → Bool) :
    16 * p x = 1
      + (∑ y, p y * chr4 y) * chr4 x
      + (∑ y, p y * chr3 0 y) * chr3 0 x
      + (∑ y, p y * chr3 1 y) * chr3 1 x
      + (∑ y, p y * chr3 2 y) * chr3 2 x
      + (∑ y, p y * chr3 3 y) * chr3 3 x := by
  have v10 : ∑ y, p y * chr1 0 y = 0 := sum_chr1_zero (hu 0 1 (by decide))
  have v11 : ∑ y, p y * chr1 1 y = 0 := sum_chr1_zero (hu 1 0 (by decide))
  have v12 : ∑ y, p y * chr1 2 y = 0 := sum_chr1_zero (hu 2 0 (by decide))
  have v13 : ∑ y, p y * chr1 3 y = 0 := sum_chr1_zero (hu 3 0 (by decide))
  have w01 : ∑ y, p y * chr2 0 1 y = 0 := sum_chr2_zero (hu 0 1 (by decide))
  have w02 : ∑ y, p y * chr2 0 2 y = 0 := sum_chr2_zero (hu 0 2 (by decide))
  have w03 : ∑ y, p y * chr2 0 3 y = 0 := sum_chr2_zero (hu 0 3 (by decide))
  have w12 : ∑ y, p y * chr2 1 2 y = 0 := sum_chr2_zero (hu 1 2 (by decide))
  have w13 : ∑ y, p y * chr2 1 3 y = 0 := sum_chr2_zero (hu 1 3 (by decide))
  have w23 : ∑ y, p y * chr2 2 3 y = 0 := sum_chr2_zero (hu 2 3 (by decide))
  have hdiag : ∑ y : Fin 4 → Bool, p y * (if x = y then (16 : ℝ) else 0) = 16 * p x := by
    rw [Finset.sum_congr rfl (fun y _ =>
      show p y * (if x = y then (16 : ℝ) else 0) = if x = y then 16 * p y else 0 by
        split_ifs <;> ring), Finset.sum_ite_eq]
    simp
  have key : ∀ y : Fin 4 → Bool, p y * (if x = y then (16 : ℝ) else 0)
      = p y
        + chr1 0 x * (p y * chr1 0 y) + chr1 1 x * (p y * chr1 1 y)
        + chr1 2 x * (p y * chr1 2 y) + chr1 3 x * (p y * chr1 3 y)
        + chr2 0 1 x * (p y * chr2 0 1 y) + chr2 0 2 x * (p y * chr2 0 2 y)
        + chr2 0 3 x * (p y * chr2 0 3 y) + chr2 1 2 x * (p y * chr2 1 2 y)
        + chr2 1 3 x * (p y * chr2 1 3 y) + chr2 2 3 x * (p y * chr2 2 3 y)
        + chr4 x * (p y * chr4 y) + chr3 0 x * (p y * chr3 0 y)
        + chr3 1 x * (p y * chr3 1 y) + chr3 2 x * (p y * chr3 2 y)
        + chr3 3 x * (p y * chr3 3 y) := by
    intro y
    rw [← kern_real x y]
    ring
  rw [← hdiag, Finset.sum_congr rfl fun y _ => key y]
  simp only [Finset.sum_add_distrib, ← Finset.mul_sum]
  rw [hp.2, v10, v11, v12, v13, w01, w02, w03, w12, w13, w23]
  ring

/-! ### The collision bound -/

/-- The pointwise expansion behind Bessel's inequality: squaring a combination
    of five orthonormal signs leaves the five squared weights on the diagonal
    and the lower-weight characters off it. Stated abstractly so that the only
    inputs are the five square relations and the ten product relations. -/
private lemma sq_expand (P C D0 D1 D2 D3 L0 L1 L2 L3 M01 M02 M03 M12 M13 M23
    c d0 d1 d2 d3 : ℝ)
    (hC : C * C = 1) (hD0 : D0 * D0 = 1) (hD1 : D1 * D1 = 1) (hD2 : D2 * D2 = 1)
    (hD3 : D3 * D3 = 1)
    (e0 : C * D0 = L0) (e1 : C * D1 = L1) (e2 : C * D2 = L2) (e3 : C * D3 = L3)
    (f01 : D0 * D1 = M01) (f02 : D0 * D2 = M02) (f03 : D0 * D3 = M03)
    (f12 : D1 * D2 = M12) (f13 : D1 * D3 = M13) (f23 : D2 * D3 = M23) :
    P * (c * C + d0 * D0 + d1 * D1 + d2 * D2 + d3 * D3) ^ 2
      = (c ^ 2 + d0 ^ 2 + d1 ^ 2 + d2 ^ 2 + d3 ^ 2) * P
        + (2 * c * d0) * (P * L0) + (2 * c * d1) * (P * L1)
        + (2 * c * d2) * (P * L2) + (2 * c * d3) * (P * L3)
        + (2 * d0 * d1) * (P * M01) + (2 * d0 * d2) * (P * M02)
        + (2 * d0 * d3) * (P * M03) + (2 * d1 * d2) * (P * M12)
        + (2 * d1 * d3) * (P * M13) + (2 * d2 * d3) * (P * M23) := by
  subst e0; subst e1; subst e2; subst e3
  subst f01; subst f02; subst f03; subst f12; subst f13; subst f23
  linear_combination (P * c ^ 2) * hC + (P * d0 ^ 2) * hD0 + (P * d1 ^ 2) * hD1
    + (P * d2 ^ 2) * hD2 + (P * d3 ^ 2) * hD3

/-- THE COLLISION BOUND: a pair-uniform four-bit state has collision
    probability at most 1/8. This is the Hamming bound in analytic clothing —
    the eight-point uniform states (the dual-distance-3 codes) attain it.

    Route: the five surviving characters are ORTHONORMAL in L²(p), because
    every product of two distinct ones is a character of weight one or two,
    which pair-uniformity kills. Bessel's inequality against the constant
    function 1 then caps the sum of their squared coefficients at 1, and
    inversion converts that cap into the collision bound. The nonnegativity of
    `p` enters exactly once, as the termwise nonnegativity of the Bessel
    remainder. -/
theorem sum_sq_le_eighth {p : (Fin 4 → Bool) → ℝ} (hp : IsProb p)
    (hu : PairUniform p) : ∑ x, p x ^ 2 ≤ 1/8 := by
  have v10 : ∑ y, p y * chr1 0 y = 0 := sum_chr1_zero (hu 0 1 (by decide))
  have v11 : ∑ y, p y * chr1 1 y = 0 := sum_chr1_zero (hu 1 0 (by decide))
  have v12 : ∑ y, p y * chr1 2 y = 0 := sum_chr1_zero (hu 2 0 (by decide))
  have v13 : ∑ y, p y * chr1 3 y = 0 := sum_chr1_zero (hu 3 0 (by decide))
  have w01 : ∑ y, p y * chr2 0 1 y = 0 := sum_chr2_zero (hu 0 1 (by decide))
  have w02 : ∑ y, p y * chr2 0 2 y = 0 := sum_chr2_zero (hu 0 2 (by decide))
  have w03 : ∑ y, p y * chr2 0 3 y = 0 := sum_chr2_zero (hu 0 3 (by decide))
  have w12 : ∑ y, p y * chr2 1 2 y = 0 := sum_chr2_zero (hu 1 2 (by decide))
  have w13 : ∑ y, p y * chr2 1 3 y = 0 := sum_chr2_zero (hu 1 3 (by decide))
  have w23 : ∑ y, p y * chr2 2 3 y = 0 := sum_chr2_zero (hu 2 3 (by decide))
  obtain ⟨c, hc⟩ : ∃ t : ℝ, ∑ y, p y * chr4 y = t := ⟨_, rfl⟩
  obtain ⟨d0, hd0⟩ : ∃ t : ℝ, ∑ y, p y * chr3 0 y = t := ⟨_, rfl⟩
  obtain ⟨d1, hd1⟩ : ∃ t : ℝ, ∑ y, p y * chr3 1 y = t := ⟨_, rfl⟩
  obtain ⟨d2, hd2⟩ : ∃ t : ℝ, ∑ y, p y * chr3 2 y = t := ⟨_, rfl⟩
  obtain ⟨d3, hd3⟩ : ∃ t : ℝ, ∑ y, p y * chr3 3 y = t := ⟨_, rfl⟩
  have hinv : ∀ x, 16 * p x - 1
      = c * chr4 x + d0 * chr3 0 x + d1 * chr3 1 x + d2 * chr3 2 x + d3 * chr3 3 x := by
    intro x
    have h := inversion hp hu x
    rw [hc, hd0, hd1, hd2, hd3] at h
    linarith
  -- (II): the second moment, read through the five coefficients.
  have hII : (16 : ℝ) * ∑ x, p x ^ 2 = 1 + (c ^ 2 + d0 ^ 2 + d1 ^ 2 + d2 ^ 2 + d3 ^ 2) := by
    have step : ∀ x : Fin 4 → Bool, 16 * p x ^ 2
        = p x + c * (p x * chr4 x) + d0 * (p x * chr3 0 x) + d1 * (p x * chr3 1 x)
          + d2 * (p x * chr3 2 x) + d3 * (p x * chr3 3 x) := fun x => by
      linear_combination p x * hinv x
    rw [Finset.mul_sum, Finset.sum_congr rfl fun x _ => step x]
    simp only [Finset.sum_add_distrib, ← Finset.mul_sum]
    rw [hp.2, hc, hd0, hd1, hd2, hd3]
    ring
  -- (I): the same quantity as the Bessel diagonal.
  have hI : ∑ x, p x * (16 * p x - 1) ^ 2
      = c ^ 2 + d0 ^ 2 + d1 ^ 2 + d2 ^ 2 + d3 ^ 2 := by
    have step : ∀ x : Fin 4 → Bool, p x * (16 * p x - 1) ^ 2
        = (c ^ 2 + d0 ^ 2 + d1 ^ 2 + d2 ^ 2 + d3 ^ 2) * p x
          + (2 * c * d0) * (p x * chr1 0 x) + (2 * c * d1) * (p x * chr1 1 x)
          + (2 * c * d2) * (p x * chr1 2 x) + (2 * c * d3) * (p x * chr1 3 x)
          + (2 * d0 * d1) * (p x * chr2 0 1 x) + (2 * d0 * d2) * (p x * chr2 0 2 x)
          + (2 * d0 * d3) * (p x * chr2 0 3 x) + (2 * d1 * d2) * (p x * chr2 1 2 x)
          + (2 * d1 * d3) * (p x * chr2 1 3 x)
          + (2 * d2 * d3) * (p x * chr2 2 3 x) := fun x => by
      rw [hinv x]
      exact sq_expand (p x) (chr4 x) (chr3 0 x) (chr3 1 x) (chr3 2 x) (chr3 3 x)
        (chr1 0 x) (chr1 1 x) (chr1 2 x) (chr1 3 x)
        (chr2 0 1 x) (chr2 0 2 x) (chr2 0 3 x) (chr2 1 2 x) (chr2 1 3 x) (chr2 2 3 x)
        c d0 d1 d2 d3
        (chr4_mul_chr4 x) (chr3_mul_self 0 x) (chr3_mul_self 1 x) (chr3_mul_self 2 x)
        (chr3_mul_self 3 x)
        (chr4_mul_chr3 0 x) (chr4_mul_chr3 1 x) (chr4_mul_chr3 2 x) (chr4_mul_chr3 3 x)
        (chr3_mul_chr3 0 1 x) (chr3_mul_chr3 0 2 x) (chr3_mul_chr3 0 3 x)
        (chr3_mul_chr3 1 2 x) (chr3_mul_chr3 1 3 x) (chr3_mul_chr3 2 3 x)
    rw [Finset.sum_congr rfl fun x _ => step x]
    simp only [Finset.sum_add_distrib, ← Finset.mul_sum]
    rw [hp.2, v10, v11, v12, v13, w01, w02, w03, w12, w13, w23]
    ring
  -- The Bessel remainder is a sum of nonnegative terms.
  have hfirst : ∑ x, p x * (16 * p x - 1) = 16 * (∑ x, p x ^ 2) - 1 := by
    rw [Finset.sum_congr rfl fun x _ =>
      show p x * (16 * p x - 1) = 16 * p x ^ 2 - p x by ring]
    rw [Finset.sum_sub_distrib, ← Finset.mul_sum, hp.2]
  have hU : ∑ x, p x * (2 - 16 * p x) ^ 2 = 2 - 16 * ∑ x, p x ^ 2 := by
    rw [Finset.sum_congr rfl fun x _ =>
      show p x * (2 - 16 * p x) ^ 2
        = p x * (16 * p x - 1) ^ 2 - 2 * (p x * (16 * p x - 1)) + p x by ring]
    rw [Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum, hI, hfirst, hp.2]
    linarith [hII]
  have hnonneg : 0 ≤ ∑ x, p x * (2 - 16 * p x) ^ 2 :=
    Finset.sum_nonneg fun x _ => mul_nonneg (hp.1 x) (sq_nonneg _)
  linarith [hU, hnonneg]

/-! ### Marginals of marginals -/

lemma isProb_pushforward {X Y : Type*} [Fintype X] [Fintype Y] [DecidableEq Y]
    (π : X → Y) {p : X → ℝ} (hp : IsProb p) : IsProb (pushforward π p) := by
  refine ⟨fun y => Finset.sum_nonneg fun x _ => hp.1 x, ?_⟩
  rw [← hp.2]
  exact Finset.sum_fiberwise Finset.univ π p

/-- Coarse-graining twice is coarse-graining once: a view of a view is a
    view. -/
lemma pushforward_comp {X Y Z : Type*} [Fintype X] [Fintype Y]
    [DecidableEq Y] [DecidableEq Z] (π₁ : X → Y) (π₂ : Y → Z) (p : X → ℝ) :
    pushforward π₂ (pushforward π₁ p) = pushforward (fun x => π₂ (π₁ x)) p := by
  funext z
  show ∑ y ∈ Finset.univ.filter (fun y => π₂ y = z),
      (∑ x ∈ Finset.univ.filter (fun x => π₁ x = y), p x)
    = ∑ x ∈ Finset.univ.filter (fun x => π₂ (π₁ x) = z), p x
  rw [← Finset.sum_fiberwise_of_maps_to
    (s := Finset.univ.filter (fun x => π₂ (π₁ x) = z))
    (t := Finset.univ.filter (fun y => π₂ y = z)) (g := π₁) (f := p)
    (fun x hx => by
      simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hx ⊢
      exact hx)]
  refine Finset.sum_congr rfl fun y hy => ?_
  refine Finset.sum_congr ?_ fun _ _ => rfl
  ext x
  simp only [Finset.mem_filter, Finset.mem_univ, true_and]
  constructor
  · intro h
    exact ⟨by rw [h]; exact (Finset.mem_filter.mp hy).2, h⟩
  · rintro ⟨-, h⟩
    exact h

/-- The pair marginals of a slot-selected marginal are the corresponding pair
    marginals of the whole: selecting four slots preserves pair-uniformity. -/
lemma pairMarg_pushforward {k : ℕ} (emb : Fin 4 → Fin k) (p : (Fin k → Bool) → ℝ)
    (i j : Fin 4) :
    pairMarg i j (pushforward (fun x : Fin k → Bool => fun m => x (emb m)) p)
      = pairMarg (emb i) (emb j) p := by
  unfold pairMarg
  rw [pushforward_comp]

/-! ### The base case, and the tightened cap -/

/-- THE BASE CASE: every pair-uniform four-bit state carries at least three
    bits of entropy. Pairwise independence buys two bits for free; the third
    is the Hamming bound — a pair-uniform state cannot concentrate on fewer
    than eight points' worth of mass, and the eight-point uniform states (the
    dual-distance-3 codes, e.g. the even-weight code) attain it exactly. -/
theorem entropy_ge_three_log_two {p : (Fin 4 → Bool) → ℝ} (hp : IsProb p)
    (hu : PairUniform p) : 3 * Real.log 2 ≤ entropy p := by
  have h := entropy_ge_of_sum_sq_le (n := 8) (by norm_num) hp.1 hp.2
    (by simpa using sum_sq_le_eighth hp hu)
  rwa [show (8 : ℝ) = 2 ^ 3 by norm_num, Real.log_pow, Nat.cast_ofNat] at h

/-- THE TIGHTENED CAP AT FOUR SLOTS: a classical four-slot state with all pair
    marginals uniform has whole-only share at most log 2 — one bit, not the
    two that `shareK_le_of_pair_uniform` allows. The improvement is exactly the
    base case above: the cap is (card) minus (the state's own entropy), and
    pair-uniformity forces that entropy up to 3·log 2. -/
theorem shareK_le_of_pair_uniform_four {p : (Fin 4 → Bool) → ℝ} (hp : IsProb p)
    (hu : PairUniform p) : shareK p ≤ Real.log 2 := by
  have hmem : entropy p ∈ pairEnvelopeK p := ⟨p, hp, fun _ _ => rfl, rfl⟩
  have h1 : sSup (pairEnvelopeK p) ≤ Real.log (Fintype.card (Fin 4 → Bool)) := by
    refine csSup_le ⟨entropy p, hmem⟩ ?_
    rintro h ⟨q, hq, -, rfl⟩
    exact entropy_le_log_card hq.1 hq.2
  have hcard : Real.log (Fintype.card (Fin 4 → Bool)) = 4 * Real.log 2 := by
    rw [card_four_slots, show ((16 : ℕ) : ℝ) = 2 ^ 4 by norm_num, Real.log_pow]
    norm_num
  rw [hcard] at h1
  have h2 := entropy_ge_three_log_two hp hu
  unfold shareK
  linarith

/-- THE TIGHTENED CAP, GENERAL FORM: if a classical k-slot state has FOUR
    slots whose six pair marginals are all uniform, its whole-only share is at
    most (k − 3)·log 2 — one full bit below `shareK_le_of_pair_uniform`.

    Note how little is assumed. `shareK_le_of_pair_uniform` needs one uniform
    pair marginal and pays (k − 2)·log 2; this needs six of them, on four
    slots, and pays a bit less. Nothing is assumed about the other k − 4 slots,
    and the four need not be the first four — `emb` picks them, and need not
    even be stated injective, since a repeated slot would make the hypothesis
    unsatisfiable on its own.

    The route is the engine of `Core.ShareK` run once: the selected four-slot
    marginal is again pair-uniform (`pairMarg_pushforward`), so the whole
    carries at least the base case's 3·log 2 (`entropy_map_le`), while the
    envelope's top is still only log(card). -/
theorem shareK_le_of_four_pair_uniform {k : ℕ} (emb : Fin 4 → Fin k)
    {p : (Fin k → Bool) → ℝ} (hp : IsProb p)
    (hu : ∀ i j : Fin 4, i ≠ j → pairMarg (emb i) (emb j) p = fun _ => (1 : ℝ)/4) :
    shareK p ≤ ((k : ℝ) - 3) * Real.log 2 := by
  have hmem : entropy p ∈ pairEnvelopeK p := ⟨p, hp, fun _ _ => rfl, rfl⟩
  have h1 : sSup (pairEnvelopeK p) ≤ Real.log (Fintype.card (Fin k → Bool)) := by
    refine csSup_le ⟨entropy p, hmem⟩ ?_
    rintro h ⟨q, hq, -, rfl⟩
    exact entropy_le_log_card hq.1 hq.2
  have hcard : Real.log (Fintype.card (Fin k → Bool)) = (k : ℝ) * Real.log 2 := by
    rw [show ((Fintype.card (Fin k → Bool) : ℕ) : ℝ) = (2 : ℝ) ^ k by
      rw [Fintype.card_fun]; push_cast; simp, Real.log_pow]
  have hq : IsProb (pushforward
      (fun x : Fin k → Bool => fun m : Fin 4 => x (emb m)) p) :=
    isProb_pushforward _ hp
  have hqu : PairUniform (pushforward
      (fun x : Fin k → Bool => fun m : Fin 4 => x (emb m)) p) := by
    intro i j hij
    rw [pairMarg_pushforward emb]
    exact hu i j hij
  have h3 := entropy_ge_three_log_two hq hqu
  have h4 := entropy_map_le
    (fun x : Fin k → Bool => fun m : Fin 4 => x (emb m)) hp
  rw [hcard] at h1
  unfold shareK
  linarith

/-- The same cap under the blanket hypothesis, for k ≥ 4: every pair marginal
    uniform. A corollary of `shareK_le_of_four_pair_uniform` with the first
    four slots selected. -/
theorem shareK_le_of_pair_uniform_ge_four {k : ℕ} (hk : 4 ≤ k)
    {p : (Fin k → Bool) → ℝ} (hp : IsProb p)
    (hu : ∀ i j : Fin k, i ≠ j → pairMarg i j p = fun _ => (1 : ℝ)/4) :
    shareK p ≤ ((k : ℝ) - 3) * Real.log 2 := by
  refine shareK_le_of_four_pair_uniform
    (fun i : Fin 4 => (⟨i.1, lt_of_lt_of_le i.2 hk⟩ : Fin k)) hp fun i j hij => ?_
  refine hu _ _ fun h => hij ?_
  simp only [Fin.mk.injEq] at h
  exact Fin.ext h

end CIRISOntology.Core
