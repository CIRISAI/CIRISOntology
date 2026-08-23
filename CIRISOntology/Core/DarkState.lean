/-
CIRISOntology.Core.DarkState — the twin aspect mode as an EXACT dark state, and
the general return-evenness engine. Cashes the PHYS-K11-1 battery's exact tier
(PHYS_K11_RESULTS.md, 2026-08-23) into machine-checked form.

THE DARK-STATE THEOREM. The eleven kinds' automorphism group is Z₂ × Z₂ — abelian
(Core/Symmetry.lean). An abelian symmetry cannot force the multiplet degeneracies
that flavour's non-abelian symmetries force; what it forces instead is
DECOUPLING. For a hopping matrix `c` invariant under the transposition swapping a
twin pair `(a,b)`, the antisymmetric combination `e_a − e_b` is an EXACT
eigenvector with eigenvalue `−c a b`, and it is orthogonal to every other site's
row: the aspect mode is invisible to the rest of the graph.

`twin_dark_state` is the eigenvector statement; `dark_state_decoupled` is the
invisibility statement (every other row annihilates it). Both hold over any
commutative ring — no analysis, no spectral theory. The numerical face was
verified at residual 0.0 / 2.2e-16 on both sealed instruments; here it is exact
by proof.

RETURN EVENNESS, GENERALLY. `return_even_of_transpose`: whenever a Hamiltonian
family satisfies `H(-φ) = H(φ)ᵀ`, every DIAGONAL entry of any power — hence of
any polynomial, hence of the exponential in the limit — is even in φ. This is the
finite, ring-level core of Core/RouteSymmetry.lean's analytic statement, and it is
the theorem the K11 battery verified at 1.0e-15 under a full random 45-flux gauge
field. Stated for powers so it applies to every truncation of the propagator.

FENCE. These are theorems about the MODEL. The measured leakage ASYMMETRY
(L(Structure/Circumstances) 11.5× L(Priorities/Process), replicated) is a
measurement, reported in PHYS_K11_RESULTS.md, and is NOT claimed here.
-/
import Mathlib.Data.Matrix.Mul
import Mathlib.Data.Matrix.Basic

namespace CIRISOntology.Core.DarkState

open Matrix

variable {n : Type*} [Fintype n] [DecidableEq n] {R : Type*} [CommRing R]

/-- The transposition of two indices. -/
omit [Fintype n] in
def swap (a b : n) : n → n := Function.update (Function.update id a b) b a

omit [Fintype n] in
@[simp] theorem swap_a (a b : n) : swap a b a = b := by
  by_cases h : b = a
  · subst h; simp [swap, Function.update]
  · simp [swap, Function.update, h]

omit [Fintype n] in
@[simp] theorem swap_b (a b : n) : swap a b b = a := by
  simp [swap, Function.update]

omit [Fintype n] in
theorem swap_other {a b k : n} (ha : k ≠ a) (hb : k ≠ b) : swap a b k = k := by
  simp [swap, Function.update, ha, hb]

/-- The antisymmetric twin combination — the "aspect mode". -/
def dark (a b : n) : n → R := fun k => if k = a then 1 else if k = b then -1 else 0

/-- Invariance of a coupling matrix under the twin swap. -/
def TwinSymmetric (c : Matrix n n R) (a b : n) : Prop :=
  ∀ i j, c (swap a b i) (swap a b j) = c i j

/-- The universe splits as the twin pair plus everything else. -/
private theorem sum_split {M : Type*} [AddCommMonoid M] {a b : n} (hab : a ≠ b)
    (f : n → M) (hz : ∀ k, k ≠ a → k ≠ b → f k = 0) :
    Finset.univ.sum f = f a + f b := by
  rw [← Finset.sum_subset (Finset.subset_univ ({a, b} : Finset n))]
  · exact Finset.sum_pair hab
  · intro k _ hk
    have hka : k ≠ a := fun h => hk (by simp [h])
    have hkb : k ≠ b := fun h => hk (by simp [h])
    exact hz k hka hkb

/-- **Decoupling**: every row other than the twin's own two annihilates the aspect
mode — the mode is invisible to the rest of the graph. -/
theorem dark_state_decoupled {c : Matrix n n R} {a b : n} (hab : a ≠ b)
    (hsym : TwinSymmetric c a b) {k : n} (hka : k ≠ a) (hkb : k ≠ b) :
    (c.mulVec (dark a b)) k = 0 := by
  have h : c k a = c k b := by
    have := hsym k b
    rwa [swap_other hka hkb, swap_b] at this
  have : (c.mulVec (dark a b)) k
      = c k a * (dark a b : n → R) a + c k b * (dark a b : n → R) b := by
    simp only [mulVec, dotProduct]
    exact sum_split hab _ (by intro i hia hib; simp [dark, hia, hib])
  rw [this]; simp [dark, hab, Ne.symm hab, h]

/-- **The dark-state theorem**: the aspect mode is an exact eigenvector with
eigenvalue `−c a b`, for any twin-symmetric coupling with zero diagonal. -/
theorem twin_dark_state {c : Matrix n n R} {a b : n} (hab : a ≠ b)
    (hsym : TwinSymmetric c a b) (hdiag : c a a = 0) (hdiagb : c b b = 0) :
    c.mulVec (dark a b) = (-(c a b)) • (dark a b) := by
  funext k
  have expand : ∀ r : n, (c.mulVec (dark a b)) r
      = c r a * (dark a b : n → R) a + c r b * (dark a b : n → R) b := by
    intro r
    simp only [mulVec, dotProduct]
    exact sum_split hab _ (by intro i hia hib; simp [dark, hia, hib])
  by_cases hka : k = a
  · subst hka
    rw [expand k]
    simp [dark, hab, Ne.symm hab, hdiag, Pi.smul_apply]
  · by_cases hkb : k = b
    · subst hkb
      have hsy : c k a = c a k := by
        have h2 := hsym k a
        rw [swap_b, swap_a] at h2
        exact h2.symm
      rw [expand k]
      simp [dark, hab, Ne.symm hab, hdiagb, hsy, Pi.smul_apply]
    · have hd := dark_state_decoupled hab hsym hka hkb
      rw [hd]
      simp [dark, hka, hkb]

/-! ### Return evenness, at ring level -/

/-- **Return evenness**: if a family satisfies `H(-φ) = H(φ)ᵀ`, every diagonal
entry of every power is even in `φ`. The finite core of the analytic statement
verified numerically at 1.0e-15 under a full random 45-flux gauge field. -/
theorem return_even_of_transpose {Φ : Type*} (H : Φ → Matrix n n R) (neg : Φ → Φ)
    (h : ∀ φ, H (neg φ) = (H φ)ᵀ) (φ : Φ) (m : ℕ) (i : n) :
    (H (neg φ) ^ m) i i = (H φ ^ m) i i := by
  rw [h φ, ← Matrix.transpose_pow]
  rfl

end CIRISOntology.Core.DarkState
