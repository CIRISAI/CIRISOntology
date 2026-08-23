/-
CIRISOntology.Core.Locality — N1's first rung: the aggregation warrant is a
locality theorem, and it is the POSITIVE face of the lake's factoring spine.

WHY THIS EXISTS. Every coarse tier of the engine leans on one unproved sentence:
"the coarse dynamics is well-defined, because what happens here depends only on
what is near." The engine carries its executable shape (`locality.rs`, the
z^d/d! horizon bound); the lake carried nothing. This file is the first rung:
locality COMPOSES, so a locally-generated dynamics has a horizon, and the state
inside a region factors through the initial data on a neighbourhood of it.

THE DRY OBSERVATION, and it reaches the whole lake. The negative results all
share one spine: a quantity that does NOT factor through a family of partial
views (`NonFactoring`, five witnesses). The aggregation warrant is the SAME
spine with the sign flipped: dynamics that DOES factor through local views —
`iterate_factors_through_ball` produces exactly the `∃ g, ... = g ∘ restrict`
that `not_computable_of_nonFactoring` refutes for the whole-only quantities. One
spine, both signs: the Logos is what fails to factor; physics is simulable
because its evolution factors. The two theorems are each other's shadow, and
the lake now holds both directions in one vocabulary.

WHAT THE MESH CONSUMES. `depends_within_comp` is the seam arithmetic: a shard
stepping n times needs boundary data of depth n·r and NOTHING ELSE — the
receipt a boundary exchange must carry is finite and computable in advance.
`iterate_factors_through_ball` is the replay warrant: a shard's interior state
is a FUNCTION of (its initial data, its boundary log), so any node can verify
any shard by deterministic replay. These are the two lemmas under "seamless"
(INTEGRATION_FRAME mesh notes), proved before the protocol exists.

SCOPE, and the named open rung. Discrete steps, an abstract ℕ-valued distance
with the triangle inequality, radius-r dependence: the coarsest honest model.
The z^d/d! CONTINUOUS-TIME bound (Lieb–Robinson; credit Lieb–Robinson 1972,
Hastings's locality programme) is the second rung and is OWED — this file
proves horizons exist and add; it does not prove the sharp growth rate. Kill,
separable: if the engine ever exhibits a certified update whose dependence
exceeds its declared radius (a nonlocal solver step counted as local — the
global Poisson solve of a gravity chart is the known candidate), the model here
does not describe that tier and its aggregation warrant must be re-earned.
-/
import Mathlib.Tactic

namespace CIRISOntology.Core.Locality

variable {V S : Type*}

/-- `F` depends within radius `r` of a distance `d`: the next value at any site
    is unchanged by edits outside the site's `r`-ball. The definition is the
    factoring property, stated pointwise. -/
def DependsWithin (d : V → V → ℕ) (r : ℕ) (F : (V → S) → (V → S)) : Prop :=
  ∀ (v : V) (x y : V → S), (∀ w, d v w ≤ r → x w = y w) → F x v = F y v

/-- **LOCALITY COMPOSES, and the radii ADD.** The whole file is this triangle
    argument: to know `G (F x)` at `v` you need `F x` on the `s`-ball, and each
    of those needs `x` on an `r`-ball inside the `(s+r)`-ball. -/
theorem depends_within_comp {d : V → V → ℕ}
    (htri : ∀ a b c, d a c ≤ d a b + d b c)
    {r s : ℕ} {F G : (V → S) → (V → S)}
    (hF : DependsWithin d r F) (hG : DependsWithin d s G) :
    DependsWithin d (s + r) (fun x => G (F x)) := by
  intro v x y hxy
  apply hG
  intro w hw
  apply hF
  intro u hu
  apply hxy
  calc d v u ≤ d v w + d w u := htri v w u
    _ ≤ s + r := Nat.add_le_add hw hu

/-- A radius-`r` dependence is also a radius-`r'` dependence for any `r' ≥ r`:
    horizons are upper bounds, monotone as they must be. -/
theorem depends_within_mono {d : V → V → ℕ} {r r' : ℕ} (h : r ≤ r')
    {F : (V → S) → (V → S)} (hF : DependsWithin d r F) :
    DependsWithin d r' F :=
  fun v x y hxy => hF v x y (fun w hw => hxy w (le_trans hw h))

/-- **THE HORIZON.** `n` steps of a radius-`r` update depend within `n·r`:
    influence has a speed limit, by induction on the composition law.
    (`hrefl` — each site is at distance zero from itself — is what makes the
    zero-step case read the site at all.) -/
theorem iterate_depends_within {d : V → V → ℕ}
    (hrefl : ∀ a, d a a = 0) (htri : ∀ a b c, d a c ≤ d a b + d b c)
    {r : ℕ} {F : (V → S) → (V → S)} (hF : DependsWithin d r F) :
    ∀ n : ℕ, DependsWithin d (n * r) F^[n] := by
  intro n
  induction n with
  | zero =>
      intro v x y hxy
      simp only [Function.iterate_zero, id_eq]
      exact hxy v (by simp [hrefl v])
  | succ k ih =>
      have h := depends_within_comp htri hF ih
      have heq : (k * r) + r = (k + 1) * r := by ring
      have h' : DependsWithin d ((k + 1) * r) (fun x => F^[k] (F x)) := heq ▸ h
      rw [Function.iterate_succ]
      exact h'

/-- **THE AGGREGATION WARRANT: the evolved state FACTORS through the ball.**
    The value at `v` after `n` steps is a function of the initial data on the
    `n·r`-ball and nothing else — the positive complement of the lake's
    `NonFactoring` shape, produced in exactly the form
    `not_computable_of_nonFactoring` refutes for whole-only quantities. This is
    the replay warrant of the mesh: interior state is a function of (initial
    data, horizon-deep boundary), so a shard is verifiable by deterministic
    replay from its receipts. -/
theorem iterate_factors_through_ball [Inhabited S] {d : V → V → ℕ}
    (hrefl : ∀ a, d a a = 0) (htri : ∀ a b c, d a c ≤ d a b + d b c)
    {r : ℕ} {F : (V → S) → (V → S)} (hF : DependsWithin d r F)
    (n : ℕ) (v : V) [∀ w, Decidable (d v w ≤ n * r)] :
    ∃ g : ({w : V // d v w ≤ n * r} → S) → S,
      ∀ x : V → S, F^[n] x v = g (fun w => x w.val) := by
  refine ⟨fun s => F^[n] (fun w => if h : d v w ≤ n * r then s ⟨w, h⟩ else default) v, ?_⟩
  intro x
  apply iterate_depends_within hrefl htri hF n v
  intro w hw
  simp [hw]

end CIRISOntology.Core.Locality
