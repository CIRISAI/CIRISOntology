/-
CIRISOntology.Core.Closure — the object contract: emergence as a lossy view
the dynamics never splits, and the macro-law that definition forces.

WHAT THIS BRICK IS. The stance's newest season answers "what makes a thing a
thing?" precisely enough for a machine to check: a THING is a summary (a
lossy view `v` of a fine state) that the world's update rule `T` never
splits — two states with the same summary today have the same summary
tomorrow. Everything the claim needs is four short theorems on that one
definition:

  * `viewClosed_iff_never_splits` — having a law of your own and never being
    split by the fine rule are the SAME condition;
  * `macro_law_forced`            — the coarse law is unique on every coarse
    state the view can produce: emergent law is derived, never fitted;
  * `viewClosed_comp`             — a closed view of a closed view is a
    closed view of the ground dynamics: tiers stack, one world supports many
    true descriptions;
  * `conserved_descends`          — a quantity the coarse law preserves is
    preserved by the fine dynamics, read through the view: conservation
    descends the tower for free.

The mathematics is deliberately elementary and borrowed knowingly — this is
the algebra of quotient dynamical systems (factor maps, semiconjugacy;
Moore-machine quotients on the computation side). Credit where the shape
lives: the sibling engineering programme (github.com/CIRISAI/CIRISHolon)
carries the identical contract as its OBJECT.md object definition
(`Closed v T ≔ ∃ h, v∘T = h∘v`) and instantiates it as a running physics
engine whose tiers are Closed views; its measured instance — a water
molecule certified against this very definition — is the stance's
`water-holon` claim. Convergence is scored as corroboration that the object
is real; the stance adds the reading and the measurement, not new
mathematics.

Noise and approximation deliberately do NOT appear here: the measured
instance handles them as pre-declared defect budgets on the closure, and
mechanizing that approximate form beside this exact one is the named
promotion price on the claim.
-/

namespace CIRISOntology.Core

variable {S V W C : Type}

/-- A view `v` is CLOSED under a dynamics `T` when some coarse update `h`
completes the square: summarize-then-step equals step-then-summarize.
This is the entire definition of an emergent object. -/
def ViewClosed (v : S → V) (T : S → S) : Prop :=
  ∃ h : V → V, ∀ x, v (T x) = h (v x)

/-- Closure is EXACTLY fiber-respect: a view has its own law of motion iff
the fine dynamics never splits an equivalence class of the view. The
forward direction is immediate; the reverse builds the coarse law by
choosing any representative of each summary (`Classical.choice`, one of the
three standard axioms). -/
theorem viewClosed_iff_never_splits (v : S → V) (T : S → S) :
    ViewClosed v T ↔ ∀ x y, v x = v y → v (T x) = v (T y) := by
  constructor
  · rintro ⟨h, hh⟩ x y hxy
    rw [hh x, hh y, hxy]
  · intro hs
    classical
    refine ⟨fun w => if hw : ∃ x, v x = w then v (T (Classical.choose hw)) else w,
      fun x => ?_⟩
    have hw : ∃ y, v y = v x := ⟨x, rfl⟩
    simp only [dif_pos hw]
    exact (hs (Classical.choose hw) x (Classical.choose_spec hw)).symm

/-- THE MACRO-LAW IS FORCED: any two coarse updates closing the same square
agree on every coarse state the view can produce — and since every state
reachable by the coarse dynamics from a summarized start is itself a
summary of a fine state, emergent law is unique where it is exercised.
Once `T` and `v` are fixed, there is nothing left to fit. -/
theorem macro_law_forced {v : S → V} {T : S → S} {h₁ h₂ : V → V}
    (c₁ : ∀ x, v (T x) = h₁ (v x)) (c₂ : ∀ x, v (T x) = h₂ (v x)) :
    ∀ x, h₁ (v x) = h₂ (v x) :=
  fun x => (c₁ x).symm.trans (c₂ x)

/-- TIERS STACK: a closed view `w` of the induced coarse dynamics is,
composed with `v`, a closed view of the ground dynamics directly. One
underlying evolution therefore supports a whole tower of autonomous
descriptions — coarser and coarser objects of the same world, not rival
substances. -/
theorem viewClosed_comp {v : S → V} {T : S → S} {h : V → V}
    (hv : ∀ x, v (T x) = h (v x)) {w : V → W} (hw : ViewClosed w h) :
    ViewClosed (fun x => w (v x)) T := by
  obtain ⟨g, hg⟩ := hw
  exact ⟨g, fun x => by show w (v (T x)) = g (w (v x)); rw [hv x]; exact hg (v x)⟩

/-- CONSERVATION DESCENDS FOR FREE: a reading `c` that the coarse law holds
invariant is held invariant by the fine dynamics, read through the view.
A conservation law proved at any tier is inherited by every finer one. -/
theorem conserved_descends {v : S → V} {T : S → S} {h : V → V}
    (hv : ∀ x, v (T x) = h (v x)) (c : V → C) (inv : ∀ w, c (h w) = c w) :
    ∀ x, c (v (T x)) = c (v x) :=
  fun x => by rw [hv x]; exact inv (v x)

end CIRISOntology.Core
