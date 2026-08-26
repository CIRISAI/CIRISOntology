/-
CIRISOntology.Core.Probe — the interventional signature, mechanized.

The A2 campaign (scratchpad/omega/interventional/) proved on planted truth that
probe-response separates coupling from correlation where observation cannot: the
COMPOSITION-2 falsification's B1 false-fire reproduces on a known-truth replica
under observation and reads exactly zero under probes. This file pays the five
Lean targets its theory note stated, each a few lines on `Core/Habit`'s closure
vocabulary, exactly as promised.

THE SHAPE. A probe is a map the view cannot see (`Blind`): a MANUFACTURED
WITNESS, supplying the second fiber point a single orbit almost never provides
(the note's Prop 5). Null response to every blind probe at lag 1 is EXACTLY
closure — `closed_iff_fiber_invariant` read operationally — provided the probe
set is rich enough to reach across fibers (`FiberTransitive`). On a product,
one-sided probes give the DIRECTED halves of `both_closed_iff_product`. And a
common driver yields null probe response in both directions at any correlation:
the twin holds the driver fixed BY CONSTRUCTION, which observation cannot.

SCOPE. Deterministic step maps, lag 1; the stochastic (distributional) version
and the two-arm rule live in the campaign's theory note, not here. Nothing here
is a claim about nature.

CREDIT: interventionist causality — Pearl (do-calculus), Woodward; the
manufactured-witness reading is this repository's, from the A2 campaign.
-/
import CIRISOntology.Core.MatterCoupling

namespace CIRISOntology.Core.Probe

variable {X : Type*}

/-- A probe the view cannot see: it moves only within fibers of `v`. -/
def Blind {C : Type*} (v : X → C) (δ : X → X) : Prop := v ∘ δ = v

/-- Null lag-1 response: probing before the step changes nothing the view reads
    after it. -/
def NullResponse {C : Type*} (v : X → C) (T δ : X → X) : Prop :=
  v ∘ T ∘ δ = v ∘ T

/-- **Closure silences every blind probe.** -/
theorem probe_response_null_of_closed {C : Type*} {v : X → C} {T : X → X}
    (h : Habit.Closed v T) {δ : X → X} (hδ : Blind v δ) :
    NullResponse v T δ := by
  obtain ⟨φ, hφ⟩ := h
  funext x
  have h1 : v (T (δ x)) = φ (v (δ x)) := congrFun hφ (δ x)
  have h2 : v (T x) = φ (v x) := congrFun hφ x
  have h3 : v (δ x) = v x := congrFun hδ x
  simp only [Function.comp_apply, h1, h2, h3]

/-- A probe set rich enough to reach any point of any fiber from any other. -/
def FiberTransitive {C : Type*} (v : X → C) (P : Set (X → X)) : Prop :=
  ∀ x y, v x = v y → ∃ δ ∈ P, δ x = y

/-- **Null response across a fiber-transitive probe set forces closure.** The
    converse direction: probes are manufactured witnesses, and enough of them
    reconstruct the fiber-invariance closure is. NOTE the hypothesis this does
    NOT take: blindness is not needed here — transitivity plus silence suffices.
    Blindness earns its keep only in the forward direction, which is the honest
    asymmetry of the signature and is now visible in the types. -/
theorem closed_of_probe_response_null {C : Type*} [Nonempty C]
    {v : X → C} {T : X → X} {P : Set (X → X)}
    (htrans : FiberTransitive v P)
    (hnull : ∀ δ ∈ P, NullResponse v T δ) :
    Habit.Closed v T := by
  rw [Habit.closed_iff_fiber_invariant]
  intro x y hxy
  obtain ⟨δ, hδP, hδx⟩ := htrans x y hxy
  have := congrFun (hnull δ hδP) x
  simp only [Function.comp_apply, hδx] at this
  exact this.symm

/-- **THE IFF.** Over a fiber-transitive blind probe set, interventional silence
    IS closure. -/
theorem interventional_iff_closed {C : Type*} [Nonempty C]
    {v : X → C} {T : X → X} {P : Set (X → X)}
    (hblind : ∀ δ ∈ P, Blind v δ) (htrans : FiberTransitive v P) :
    (∀ δ ∈ P, NullResponse v T δ) ↔ Habit.Closed v T :=
  ⟨closed_of_probe_response_null htrans,
   fun h δ hδ => probe_response_null_of_closed h (hblind δ hδ)⟩

/-! ### The product face: one-sided probes give the DIRECTED halves -/

/-- The A-side probes on a product: set the A coordinate, leave B alone. Snd-blind
    by construction, and fiber-transitive for `Prod.snd`. -/
def setA {A B : Type*} (a' : A) : A × B → A × B := fun p => (a', p.2)

theorem setA_blind {A B : Type*} (a' : A) :
    Blind (Prod.snd : A × B → B) (setA a') := rfl

theorem setA_fiberTransitive {A B : Type*} :
    FiberTransitive (Prod.snd : A × B → B) (Set.range (setA (B := B) (A := A))) := by
  rintro ⟨a, b⟩ ⟨a', b'⟩ h
  exact ⟨setA a', ⟨a', rfl⟩, by cases h; rfl⟩

/-- **The directed half, interventionally.** Null response of B's view to every
    A-probe is EXACTLY B's closure — "no arrow A→B". With the mirror on the other
    side and `both_closed_iff_product`, two-sided probe silence is productness. -/
theorem directed_probe_null_iff {A B : Type*} [Nonempty B] {T : A × B → A × B} :
    (∀ a', NullResponse (Prod.snd : A × B → B) T (setA a')) ↔
      Habit.Closed (Prod.snd : A × B → B) T := by
  constructor
  · intro h
    refine closed_of_probe_response_null (P := Set.range setA) setA_fiberTransitive ?_
    rintro δ ⟨a', rfl⟩; exact h a'
  · intro h a'
    exact probe_response_null_of_closed h (setA_blind a')

/-- **Two-sided probe silence IS productness** — the interventional
    `both_closed_iff_product`. -/
theorem product_iff_probe_null_both {A B : Type*} [Nonempty A] [Nonempty B]
    {T : A × B → A × B} :
    ((∀ a', NullResponse (Prod.snd : A × B → B) T (setA a')) ∧
     (∀ b', NullResponse (Prod.fst : A × B → A) T (fun p => (p.1, b')))) ↔
      ∃ (f : A → A) (g : B → B), T = fun s => (f s.1, g s.2) := by
  rw [← CIRISOntology.Core.MatterCoupling.both_closed_iff_product]
  constructor
  · rintro ⟨hA, hB⟩
    refine ⟨?_, directed_probe_null_iff.mp hA⟩
    · refine closed_of_probe_response_null
        (P := Set.range (fun b' => (fun p : A × B => (p.1, b')))) ?_ ?_
      · rintro ⟨a, b⟩ ⟨a', b'⟩ h
        exact ⟨fun p => (p.1, b'), ⟨b', rfl⟩, by cases h; rfl⟩
      · rintro δ ⟨b', rfl⟩; exact hB b'
  · rintro ⟨hfst, hsnd⟩
    exact ⟨fun a' => probe_response_null_of_closed hsnd rfl,
           fun b' => probe_response_null_of_closed hfst rfl⟩

/-! ### The common-driver face -/

/-- **A common driver is silent under probes at ANY correlation.** For
    `T (a,b,c) = (f a c, g b c, h c)` — two sectors driven by a shared `c`,
    with no arrow between them — every A-probe draws a null response from B's
    view, and neither view need be Closed. The twin holds the driver fixed by
    construction; observation cannot. This is the theorem behind the atlas's
    measured common-driver gap and COMPOSITION-2's B1 post-mortem. -/
theorem common_driver_probe_null {A B Cd : Type*}
    (f : A → Cd → A) (g : B → Cd → B) (h : Cd → Cd) (a' : A) :
    NullResponse (fun x : A × B × Cd => x.2.1)
      (fun x => (f x.1 x.2.2, g x.2.1 x.2.2, h x.2.2))
      (fun x => (a', x.2.1, x.2.2)) := rfl

end CIRISOntology.Core.Probe
