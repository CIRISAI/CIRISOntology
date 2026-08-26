/-
CIRISOntology.Core.HolonomyRate — the surviving curvature-closure bridge, from
atlas v2 (scratchpad/atlas/ATLAS_V2_RESULTS.md).

BOTH staked bridges died with decide-able minimal counterexamples: nonzero
holonomy does NOT imply closure failure (|X|=2 witness: a moving loop over a
Closed view), and zero holonomy does NOT imply closure (|X|=3 witness). The
naive bridge compared one relation's readings on two unrelated maps — zero
curvature IS `Held v r_loop`, rent-paid-in-full read on the TRANSPORT map, so
curvature and rent were always the same relation in two costumes
(`curvature_iff_held`).

WHAT SURVIVED: **curvature is an automorphism of the habit.** When the loop is a
symmetry of the step, the transported reading evolves exactly as the reading of
the transported state — the holonomy commutes with the induced rate. Verified
exhaustively at |X|=3 (183,303/183,303) and the equivariance hypothesis is
load-bearing (fails in 452,304 of 559,548 non-equivariant models).

MODE-SECTOR FINDING, recorded from the enumeration (not proved here): in the
bijective-view three-context family the sign is OPPOSITE to the staked bridge —
nonzero curvature forces every context view CLOSED. And a CORRECTION to this
repo's earlier framing: fixed fibration does not force view-side flatness; a
COMMON SOURCE does. `loop_asymmetry` is about the common source.

Also from the atlas, fences owed as future bricks: LOSSY holonomy exists
(holonomy-is-a-permutation needs reversible transport as a hypothesis), and a
loop can transport where a leg does not (64 % of obstructed atlases) — a round
trip is NOT evidence its legs were licensed; `comp_failure_convicts_second_leg`
must never be read backwards.
-/
import Mathlib.Data.Fin.VecNotation
import Mathlib.Logic.Function.Basic

/- Atlas v2's proposed Lean target, checked standalone (Mathlib not needed).
   The bridge that survived the v2 enumeration: see ATLAS_V2_RESULTS.md section 8. -/

/-- **CURVATURE IS AN AUTOMORPHISM OF THE HABIT.** If the re-root loop is a symmetry
    of the step and the view is `Closed` with rate `h`, the holonomy commutes with the
    rate on the view's range. Both hypotheses are load-bearing: dropping either admits
    counterexamples (atlas v2, exhaustive at |X| = 3). -/
theorem holonomy_commutes_with_rate
    {X C : Type _} {v : X → C} {T rloop : X → X} {γ h : C → C}
    (hcarry  : v ∘ rloop = γ ∘ v)      -- Closed v rloop, γ the transport witness
    (hclosed : v ∘ T = h ∘ v)          -- Closed v T,     h the rate
    (heqv    : T ∘ rloop = rloop ∘ T)  -- the loop is a symmetry of the step
    (x : X) : γ (h (v x)) = h (γ (v x)) := by
  have hc : ∀ y, γ (v y) = v (rloop y) := fun y => (congrFun hcarry y).symm
  have hr : ∀ y, h (v y) = v (T y)     := fun y => (congrFun hclosed y).symm
  have he : ∀ y, T (rloop y) = rloop (T y) := fun y => congrFun heqv y
  rw [hr, hc, ← he x, hc, hr]

/-- Zero curvature IS `Held` on the context axis (`Core/Habit.lean`'s `Held v T` at
    `T := rloop`): given the carry, the holonomy fixes every reading exactly when the
    round-trip reading agrees with the direct one. -/
theorem curvature_iff_held
    {X C : Type _} {v : X → C} {rloop : X → X} {γ : C → C}
    (hcarry : v ∘ rloop = γ ∘ v) :
    (∀ x : X, γ (v x) = v x) ↔ v ∘ rloop = v := by
  constructor
  · intro hfix; funext x; exact (congrFun hcarry x).trans (hfix x)
  · intro hheld x; exact ((congrFun hcarry x).symm.trans (congrFun hheld x))

/-- The glued view of a TRANSPORTABLE atlas carries exactly the base view — which is
    why "closure failure of the glued view" has no subject. -/
theorem glued_view_collapses
    {X C D E : Type _} {q1 : X → C} {g : C → D} {g' : D → E} :
    (fun x => (q1 x, g (q1 x), g' (g (q1 x))))
      = (fun c => (c, g c, g' (g c))) ∘ q1 := rfl

#print axioms holonomy_commutes_with_rate
#print axioms curvature_iff_held
#print axioms glued_view_collapses


/-! ### The atlas's minimal witnesses, as decidable finite data

Each is the smallest counterexample atlas v2 found, carried here so the dead
bridges stay dead BY MACHINE. `decide` closes all of them.
-/

namespace CIRISOntology.Core.HolonomyRate

/-- **B(ii) dead: maximal curvature over a perfectly closed view.** On two
    states with the identity dynamics and the swap re-root, the holonomy moves
    EVERY reading while the view is trivially Closed — so nonzero holonomy
    implies nothing about closure failure. -/
theorem curvature_without_closure_failure :
    -- the swap re-root carries the identity view with holonomy = swap ≠ id,
    (∀ x : Fin 2, (id : Fin 2 → Fin 2) (![1, 0] x) = ![1, 0] ((id : Fin 2 → Fin 2) x))
    ∧ ¬ (![1, 0] : Fin 2 → Fin 2) = id
    -- while the view is Closed under the (identity) dynamics:
    ∧ (∀ x y : Fin 2, (id : Fin 2 → Fin 2) x = id y → id ((id : Fin 2 → Fin 2) x) = id (id y)) := by
  refine ⟨fun x => rfl, ?_, fun x y h => by simpa using h⟩
  intro h
  have := congrFun h 0
  simp [Matrix.cons_val_zero] at this

/-- **B(i) dead: exact flatness over a view the dynamics does not close.** On
    three states, the re-root `(1,0,2)` is a genuinely nontrivial loop that is
    exactly flat (it preserves the view's fibers — `Held`), while the dynamics
    `(0,2,1)` splits a fiber of the view `(0,0,1)`. Zero holonomy implies
    nothing about closure. -/
theorem flatness_without_closure :
    -- Held: the loop preserves every reading of v = ![0,0,1]
    (∀ x : Fin 3, (![0, 0, 1] : Fin 3 → Fin 2) (![1, 0, 2] x) = ![0, 0, 1] x)
    -- the loop is not the identity
    ∧ ¬ (![1, 0, 2] : Fin 3 → Fin 3) = id
    -- and the view is NOT fiber-invariant under T = ![0,2,1]
    ∧ ¬ (∀ x y : Fin 3, (![0, 0, 1] : Fin 3 → Fin 2) x = ![0, 0, 1] y →
          (![0, 0, 1] : Fin 3 → Fin 2) (![0, 2, 1] x) = ![0, 0, 1] (![0, 2, 1] y)) := by
  refine ⟨by decide, ?_, by decide⟩
  intro h
  have := congrFun h 0
  simp [Matrix.cons_val_zero] at this

/-- **LOSSY HOLONOMY EXISTS** — the fence on "holonomy is a permutation". The
    constant re-root on two states carries the identity view with a holonomy
    that is NOT injective on the range: an irreversible re-root returns fewer
    distinctions than it took. Reversibility is a HYPOTHESIS, not a fact. -/
theorem lossy_holonomy_exists :
    (∀ x : Fin 2, (id : Fin 2 → Fin 2) ((fun _ => 0) x) = (fun _ => (0 : Fin 2)) ((id : Fin 2 → Fin 2) x))
    ∧ ¬ Function.Injective (fun _ : Fin 2 => (0 : Fin 2)) := by
  exact ⟨fun x => rfl, by intro h; have := h (a₁ := 0) (a₂ := 1) rfl; simp at this⟩

/-- **Holonomy IS a permutation under reversible carry.** If both the loop and
    an inverse of it carry the view, the two holonomies invert each other on a
    surjective view's whole codomain — the hypothesis the lossy witness shows
    is load-bearing. -/
theorem holonomy_bijective_of_reversible_carry
    {X C : Type*} {v : X → C} {r g : X → X} {γ γ' : C → C}
    (hgr : ∀ x, g (r x) = x) (hrg : ∀ x, r (g x) = x)
    (hc : v ∘ r = γ ∘ v) (hc' : v ∘ g = γ' ∘ v)
    (hsurj : Function.Surjective v) :
    Function.Bijective γ := by
  have hgi : ∀ c, γ' (γ c) = c := by
    intro c; obtain ⟨x, rfl⟩ := hsurj c
    have h1 : γ (v x) = v (r x) := (congrFun hc x).symm
    have h2 : γ' (v (r x)) = v (g (r x)) := (congrFun hc' (r x)).symm
    rw [h1, h2, hgr]
  have hig : ∀ c, γ (γ' c) = c := by
    intro c; obtain ⟨x, rfl⟩ := hsurj c
    have h1 : γ' (v x) = v (g x) := (congrFun hc' x).symm
    have h2 : γ (v (g x)) = v (r (g x)) := (congrFun hc (g x)).symm
    rw [h1, h2, hrg]
  exact Function.bijective_iff_has_inverse.mpr ⟨γ', hgi, hig⟩

/-- **B(vi) fence: a loop can carry where a leg cannot.** With a constant base
    view, the identity leg toward an identity target view has NO carry (the
    identity does not factor through a constant), while the loop carries
    trivially. A successful round trip is not evidence its legs were licensed —
    `comp_failure_convicts_second_leg` must never be read backwards. -/
theorem loop_carries_where_leg_fails :
    ¬ (∃ γ : Fin 2 → Fin 2, (id : Fin 2 → Fin 2) ∘ id = γ ∘ (fun _ => (0 : Fin 2)))
    ∧ (∃ γ : Fin 2 → Fin 2, (fun _ : Fin 2 => (0 : Fin 2)) ∘ id = γ ∘ (fun _ => (0 : Fin 2))) := by
  constructor
  · rintro ⟨γ, h⟩
    have h0 := congrFun h 0
    have h1 := congrFun h 1
    simp [Function.comp] at h0 h1
    rw [← h0] at h1
    exact absurd h1 (by decide)
  · exact ⟨id, rfl⟩

/-- **A5: closure does not descend the `Factors` order.** The identity view is
    Closed under `T = ![0,2,0]` (trivially), while its strict coarsening
    `![0,0,1]` is not: a tier's autonomy is not inherited by its own
    coarsenings — each context owes its own closure reading. -/
theorem closure_not_hereditary :
    (∀ x y : Fin 3, (id : Fin 3 → Fin 3) x = id y →
        id ((![0, 2, 0] : Fin 3 → Fin 3) x) = id (![0, 2, 0] y))
    ∧ ¬ (∀ x y : Fin 3, (![0, 0, 1] : Fin 3 → Fin 2) x = ![0, 0, 1] y →
        (![0, 0, 1] : Fin 3 → Fin 2) ((![0, 2, 0] : Fin 3 → Fin 3) x) =
          ![0, 0, 1] (![0, 2, 0] y)) := by
  exact ⟨fun x y h => by rw [show x = y from h], by decide⟩

/- IOU, stated so it cannot silently vanish: the MODE-SECTOR THEOREM (nonzero
curvature forces every context view Closed, in the bijective-view three-context
mode-only family — the OPPOSITE sign to the staked bridge) is measured and
counted exactly in `scratchpad/atlas/ATLAS_V2_RESULTS.md` §5 but NOT mechanized
here: a faithful formalization must reproduce that family's transport condition
as implemented in `atlas_v2_addendum.py`, and a mis-formalized brick would be
worse than an explicit debt. -/

end CIRISOntology.Core.HolonomyRate
