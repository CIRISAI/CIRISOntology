/-
CIRISOntology.Core.TwinTransport — the dynamical companion to DarkState, and the
fence that stops it being over-read.

WHY THIS EXISTS. `Core/DarkState.lean` proves that the ANTISYMMETRIC twin mode is
invisible to the rest of the graph (`dark_state_decoupled`). This file proves the
other half: a SYMMETRIC state never leaves the symmetric sector. Under a
twin-symmetric coupling, a configuration in which the two twins agree keeps them
agreeing — not approximately, not on average, but for every step and forever.

Together the two statements say the Z₂ × Z₂ character sectors of Core/Symmetry.lean
are DYNAMICALLY invariant: no evolution moves amplitude between them. The engine
carries that as a numerical diagnostic (`sectors::inter_sector_leakage`); here it is
a theorem about the discrete integrator the engine actually runs, at ring level,
with no analysis.

THE OCCASION. The h3ere2 pipeline seeds a whole surface block and reads off the
order in which the disturbance reaches each kind. Structure and Circumstances — the
twin pair (9,6) — were observed arriving adjacent in every path, which looked like
the dynamics reproducing the automorphism. `twins_move_together` is why: the
pipeline steps on the group-AVERAGED coupling, the block seedings are unions of
twin orbits, and so the twins are not merely adjacent but identical at every step.
Measured on the engine: trajectory difference exactly 0.0, arrival steps equal, in
all four blocks.

THE FENCE, AND IT IS THE POINT. `twinSymmetrise_is_symmetric` proves that
symmetrising ANY matrix yields a twin-symmetric one. So the twin identity
downstream is a property of the SYMMETRISATION, not evidence about the coupling
that went in. Measured on the engine: a fully scrambled coupling produces the same
exact tie. Nothing about the observed adjacency is a fact about the measured
object, and this file exists as much to block that inference as to make the
positive one.

FENCE. These are theorems about the MODEL — a discrete integrator over a
commutative ring. No claim is made here about the measured couplings, whose twin
symmetry is BROKEN (Core/DefectCoupling.lean measures the defect, and the engine
reads inter-sector leakage 4.51 on the measured matrix against machine zero on its
average).
-/
import Mathlib.Data.Matrix.Mul
import Mathlib.Data.Matrix.Basic
import CIRISOntology.Core.DarkState

namespace CIRISOntology.Core.TwinTransport

open Matrix
open CIRISOntology.Core.DarkState

variable {n : Type*} [Fintype n] [DecidableEq n] {R : Type*} [CommRing R]

/-! ### The swap is an involution, hence a permutation -/

theorem swap_involutive (a b : n) : ∀ k, swap a b (swap a b k) = k := by
  intro k
  by_cases hka : k = a
  · subst hka; simp
  · by_cases hkb : k = b
    · subst hkb; simp
    · rw [swap_other hka hkb, swap_other hka hkb]

/-- The twin swap as an equivalence, so sums may be reindexed by it. -/
def swapEquiv (a b : n) : n ≃ n where
  toFun := swap a b
  invFun := swap a b
  left_inv := swap_involutive a b
  right_inv := swap_involutive a b

@[simp] theorem swapEquiv_apply (a b k : n) : swapEquiv a b k = swap a b k := rfl

/-! ### Twin-invariant states -/

/-- A state that the twin swap does not move: the two twins carry equal values, and
every other site is fixed outright. This is the SYMMETRIC sector, the complement of
`DarkState.dark`. -/
def TwinInvariant (x : n → R) (a b : n) : Prop := ∀ k, x (swap a b k) = x k

/-- The whole content, at a point: a twin-invariant state assigns the twins the same
value. -/
theorem twins_equal {x : n → R} {a b : n} (h : TwinInvariant x a b) : x a = x b := by
  have := h b
  rwa [swap_b] at this

theorem TwinInvariant.add {x y : n → R} {a b : n}
    (hx : TwinInvariant x a b) (hy : TwinInvariant y a b) :
    TwinInvariant (fun k => x k + y k) a b := fun k => by
  simp only []; rw [hx k, hy k]

theorem TwinInvariant.sub {x y : n → R} {a b : n}
    (hx : TwinInvariant x a b) (hy : TwinInvariant y a b) :
    TwinInvariant (fun k => x k - y k) a b := fun k => by
  simp only []; rw [hx k, hy k]

theorem TwinInvariant.const_mul (r : R) {x : n → R} {a b : n}
    (hx : TwinInvariant x a b) : TwinInvariant (fun k => r * x k) a b := fun k => by
  simp only []; rw [hx k]

/-- **The transport lemma.** A twin-symmetric coupling maps twin-invariant states to
twin-invariant states. Everything else in this file is a corollary of it. -/
theorem mulVec_twin_invariant {c : Matrix n n R} {a b : n}
    (hc : TwinSymmetric c a b) {x : n → R} (hx : TwinInvariant x a b) :
    TwinInvariant (c *ᵥ x) a b := by
  intro k
  simp only [mulVec, dotProduct]
  calc ∑ j, c (swap a b k) j * x j
      = ∑ j, c (swap a b k) (swap a b j) * x (swap a b j) :=
        (Equiv.sum_comp (swapEquiv a b) (fun j => c (swap a b k) j * x j)).symm
    _ = ∑ j, c k j * x j :=
        Finset.sum_congr rfl (fun j _ => by rw [hc k j, hx j])

/-! ### The integrator the engine actually runs

`ciris-sim-core`'s harmonic regime is velocity Verlet on `x'' = -L x` at unit mass
(`Params::harmonic` sets `rest_scale = 0`, which collapses the spring term to
`F = -Lx` exactly — FSD §13). The step is written here over a commutative ring with
the two scalars supplied by the caller, so no division and no analysis enter: `h`
stands for `dt` and `hh` for `dt/2`.
-/

/-- One velocity-Verlet step of `x'' = -L x`, at unit mass. -/
def verlet (L : Matrix n n R) (h hh : R) (s : (n → R) × (n → R)) : (n → R) × (n → R) :=
  let vh : n → R := fun k => s.2 k - hh * (L *ᵥ s.1) k
  let x' : n → R := fun k => s.1 k + h * vh k
  (x', fun k => vh k - hh * (L *ᵥ x') k)

/-- A Verlet step preserves twin invariance of both position and velocity. -/
theorem verlet_preserves {L : Matrix n n R} {a b : n} (hL : TwinSymmetric L a b)
    (h hh : R) {s : (n → R) × (n → R)}
    (h1 : TwinInvariant s.1 a b) (h2 : TwinInvariant s.2 a b) :
    TwinInvariant (verlet L h hh s).1 a b ∧ TwinInvariant (verlet L h hh s).2 a b := by
  have hvh : TwinInvariant (fun k => s.2 k - hh * (L *ᵥ s.1) k) a b :=
    h2.sub ((mulVec_twin_invariant hL h1).const_mul hh)
  have hx' : TwinInvariant (fun k => s.1 k + h * (s.2 k - hh * (L *ᵥ s.1) k)) a b :=
    h1.add (hvh.const_mul h)
  exact ⟨hx', hvh.sub ((mulVec_twin_invariant hL hx').const_mul hh)⟩

/-- Twin invariance survives any number of steps. -/
theorem verlet_iterate_preserves {L : Matrix n n R} {a b : n} (hL : TwinSymmetric L a b)
    (h hh : R) : ∀ (m : ℕ) (s : (n → R) × (n → R)),
      TwinInvariant s.1 a b → TwinInvariant s.2 a b →
      TwinInvariant ((verlet L h hh)^[m] s).1 a b ∧
        TwinInvariant ((verlet L h hh)^[m] s).2 a b := by
  intro m
  induction m with
  | zero => intro s h1 h2; exact ⟨h1, h2⟩
  | succ m ih =>
      intro s h1 h2
      rw [Function.iterate_succ_apply]
      exact ih _ (verlet_preserves hL h hh h1 h2).1 (verlet_preserves hL h hh h1 h2).2

/-- **The twins move together.** Under a twin-symmetric coupling, from any start in
which the twins agree and their velocities agree, the two twins hold equal positions
at EVERY step — so any observable read off the trajectory (an arrival time, an order,
a threshold crossing) cannot separate them.

This is the theorem behind the h3ere2 observation, and it is exact: no tolerance
appears anywhere in it. -/
theorem twins_move_together {L : Matrix n n R} {a b : n} (hL : TwinSymmetric L a b)
    (h hh : R) (m : ℕ) {s : (n → R) × (n → R)}
    (h1 : TwinInvariant s.1 a b) (h2 : TwinInvariant s.2 a b) :
    ((verlet L h hh)^[m] s).1 a = ((verlet L h hh)^[m] s).1 b :=
  twins_equal (verlet_iterate_preserves hL h hh m s h1 h2).1

/-- A block seeding is twin-invariant exactly when it contains both twins or neither
— which is what makes the h3ere2 blocks qualify, since the twin swaps are
automorphisms of the site structure and so cannot split a block. -/
theorem twinInvariant_of_indicator {a b : n} (S : n → Prop) [DecidablePred S] (v : R)
    (hS : ∀ k, S (swap a b k) ↔ S k) :
    TwinInvariant (fun k => if S k then v else 0) a b := by
  intro k
  by_cases hk : S k
  · simp [hk, (hS k).mpr hk]
  · have hswap : ¬ S (swap a b k) := fun h => hk ((hS k).mp h)
    simp [hk, hswap]

/-! ### The fence

The positive theorems above are conditional on the coupling being twin-symmetric.
The engine's `relax` obtains that condition by AVERAGING over the group, and the
average of anything is symmetric. So the twin identity observed downstream is a
property of the averaging step and carries no information about its input.
-/

/-- The unnormalised twin symmetrisation. (Unnormalised so it needs no division and
lives over any commutative ring; the engine divides by the group order, which changes
nothing about symmetry.) -/
def twinSymmetrise (c : Matrix n n R) (a b : n) : Matrix n n R :=
  Matrix.of fun i j => c i j + c (swap a b i) (swap a b j)

/-- **The fence.** Symmetrising ANY matrix yields a twin-symmetric one — no
hypothesis on `c` whatsoever.

Consequence, and the reason this theorem is stated: observing that the twins behave
identically downstream of a symmetrisation is evidence about the symmetrisation and
NOT about the matrix that went into it. A scrambled coupling produces the same exact
tie as the measured one, and the engine confirms it numerically. Any reading of the
twin adjacency as a discovered property of the measured object is blocked here. -/
theorem twinSymmetrise_is_symmetric (c : Matrix n n R) (a b : n) :
    TwinSymmetric (twinSymmetrise c a b) a b := by
  intro i j
  simp only [twinSymmetrise, Matrix.of_apply]
  rw [swap_involutive a b i, swap_involutive a b j]
  exact add_comm _ _

/-- And therefore the conclusion holds downstream of a symmetrisation for EVERY
coupling — the hypothesis that made `twins_move_together` informative has been
supplied by the construction rather than by the data. -/
theorem twins_move_together_after_symmetrise (c : Matrix n n R) (a b : n)
    (h hh : R) (m : ℕ) {s : (n → R) × (n → R)}
    (h1 : TwinInvariant s.1 a b) (h2 : TwinInvariant s.2 a b) :
    ((verlet (twinSymmetrise c a b) h hh)^[m] s).1 a
      = ((verlet (twinSymmetrise c a b) h hh)^[m] s).1 b :=
  twins_move_together (twinSymmetrise_is_symmetric c a b) h hh m h1 h2


/-! ### M10 — why the kinds stay eleven

The engine's profile-class coarsening reads `N/G = 1.00` on K11: no two kinds merge at
any usable tolerance, and the first merge needs a tolerance LARGER than the mean
off-diagonal coupling itself. That is a measured fact about a particular matrix. What
follows is its structural half, and it needs no numbers at all.

Read together with `Core/Symmetry.lean`'s computed `aut_with_stack = 4`, the consequence
is sharp. The only transpositions that are automorphisms of the coupling are the two twin
swaps. So the ONLY pairs that could possibly carry identical profiles are the twin pairs —
and the measured defect in `Core/DefectCoupling.lean` (2.284 against 8.617) shows that even
they do not. Eleven genuinely different questions, not eleven labels on fewer distinctions.

This is also the other side of the failed scaling thesis (FSD §16): the same rigidity that
denies the simulation engine any profile repetition to compress is the taxonomy being
irredundant. The engine wanted duplicates; the object has none to give. -/

/-- If two kinds couple to everything alike, swapping them leaves every row alone. -/
theorem row_swap_eq_of_profile_eq {c : Matrix n n R} {a b : n}
    (hprof : ∀ k, c a k = c b k) (i k : n) : c (swap a b i) k = c i k := by
  by_cases hia : i = a
  · subst hia; rw [swap_a]; exact (hprof k).symm
  · by_cases hib : i = b
    · subst hib; rw [swap_b]; exact hprof k
    · rw [swap_other hia hib]

/-- **Identical profiles force an automorphism.** If two kinds couple to everything
alike, the transposition exchanging them fixes the entire coupling. Distinctness of the
kinds is therefore not a numerical accident of one measured matrix — it is exactly what
rigidity buys. -/
theorem twinSymmetric_of_profile_eq {c : Matrix n n R} (hsym : ∀ i j, c i j = c j i)
    {a b : n} (hprof : ∀ k, c a k = c b k) : TwinSymmetric c a b := by
  intro i j
  calc c (swap a b i) (swap a b j)
      = c i (swap a b j)   := row_swap_eq_of_profile_eq hprof i _
    _ = c (swap a b j) i   := hsym _ _
    _ = c j i              := row_swap_eq_of_profile_eq hprof j i
    _ = c i j              := hsym _ _

/-- The contrapositive, and the form M10 is actually used in: a rigid coupling has no
near-duplicate kinds. If transposing two kinds is not an automorphism, their profiles
must already differ somewhere. -/
theorem profile_ne_of_not_twinSymmetric {c : Matrix n n R} (hsym : ∀ i j, c i j = c j i)
    {a b : n} (h : ¬ TwinSymmetric c a b) : ∃ k, c a k ≠ c b k := by
  by_contra hcon
  push_neg at hcon
  exact h (twinSymmetric_of_profile_eq hsym hcon)

end CIRISOntology.Core.TwinTransport
