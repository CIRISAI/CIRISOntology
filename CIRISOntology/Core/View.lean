/-
CIRISOntology.Core.View — the FIBRES of a view, and six readings of them.

ONE object, six readings; these bridges are definitional unifications — one
witness, not six; no new evidence about the world.

The object is the kernel relation of a view `v : X → C`:

    SameFibre v x y  ≔  v x = v y        "the view cannot tell x from y"

Every shape below was proved in its own file under its own name. This file adds
no mathematics about any of them; it states each one through `SameFibre`, so the
reader can see it is the same relation read six ways:

  | reading     | statement through `SameFibre`                                   | home                    |
  |-------------|-----------------------------------------------------------------|-------------------------|
  | DETERMINES  | `Factors u v ↔ ∀ x y, SameFibre v x y → u x = u y`              | `Core/Fibre.lean`       |
  | BLIND       | `SeparatesFiber v u ↔ ∃ x y, SameFibre v x y ∧ u x ≠ u y`;       | `Core/Fibre.lean`       |
  |             | `NonFactoring view q` is the same through the joint view        |                         |
  | CLOSED      | `ViewClosed v T ↔ Habit.Closed v T ↔ T maps fibres into fibres` | `Core/Closure`, `Habit` |
  | PROBE       | `Probe.Blind v δ ↔ ∀ x, SameFibre v (δ x) x`                    | `Core/Probe.lean`       |
  | ENTROPY     | `s ∈ FrameEntropy.fiber v (v t) ↔ SameFibre v s t`              | `Core/FrameEntropy`     |
  | RECORD      | a dephased coherence survives `↔ SameFibre l i j`               | `Core/DephasingReader`  |

ONE DEFINITION OF EACH. Closure is defined once: `Core.ViewClosed v T` has body
`Factoring.Factors (v ∘ T) v` and `Habit.Closed` is an `abbrev` of it, so
`habitClosed_iff_viewClosed` is `Iff.rfl`. Likewise `Probe.Blind` is an `abbrev`
of `Habit.Held` and `FrameAxis.CoarserThan` an `abbrev` of `Factoring.Factors`.

HYPOTHESES, stated honestly. The DETERMINES direction from fibre-respect to a
factoring map needs a default value in the quantity's codomain (`[Nonempty C]`)
and `Classical.choice`; it is the library's ONE choice construction
(`factors_iff_respects`, in `Core/Fibre.lean`). The closure form needs no
default (`factors_comp_iff_preserves`); every other bridge is hypothesis-free.

Placement: `SameFibre` and readings 1–2 live in the base file `Core/Fibre.lean`
(below Coordination, FrameAxis, Factoring, NonFactoring, Closure); this hub sits
above the higher homes and states readings 3–6.
-/
import CIRISOntology.Core.Fibre
import CIRISOntology.Core.Factoring
import CIRISOntology.Core.Habit
import CIRISOntology.Core.Closure
import CIRISOntology.Core.Probe
import CIRISOntology.Core.FrameEntropy
import CIRISOntology.Core.DephasingReader

namespace CIRISOntology.Core.View

open Filter Topology

/-! `SameFibre`, its API, and readings 1–2 (DETERMINES, BLIND) live in the
base file `Core/Fibre.lean`, under this same namespace, so files below this hub
can use them. -/

/-! ### Reading 3 — CLOSED (`Core/Closure.lean`, `Core/Habit.lean`) -/

section Closed

variable {S V : Type*}

/-- **THE TWO CLOSURES ARE ONE — by definition now.** `Habit.Closed` is an
    `abbrev` of `Core.ViewClosed`, whose body is `Factoring.Factors (v ∘ T) v`;
    this is `Iff.rfl`. Kept as a named witness of the merge. -/
theorem habitClosed_iff_viewClosed (v : S → V) (T : S → S) :
    Habit.Closed v T ↔ ViewClosed v T :=
  Iff.rfl

/-- **CLOSED.** A view has its own law of motion iff the dynamics maps every
    fibre into a fibre. Hypothesis-free (the coarse law defaults to the identity
    off the image). -/
theorem viewClosed_iff_preserves (v : S → V) (T : S → S) :
    ViewClosed v T ↔ ∀ x y, SameFibre v x y → SameFibre v (T x) (T y) :=
  viewClosed_iff_never_splits v T

/-- **CLOSED**, in `Habit`'s spelling; hypothesis-free. -/
theorem habitClosed_iff_preserves (v : S → V) (T : S → S) :
    Habit.Closed v T ↔ ∀ x y, SameFibre v x y → SameFibre v (T x) (T y) :=
  (habitClosed_iff_viewClosed v T).trans (viewClosed_iff_preserves v T)

end Closed

/-! ### Reading 4 — PROBE (`Core/Probe.lean`) -/

section Probe

variable {X C : Type*}

/-- **PROBE.** A probe is blind to the view iff it moves every state within its
    own fibre. -/
theorem blind_iff (v : X → C) (δ : X → X) :
    Probe.Blind v δ ↔ ∀ x, SameFibre v (δ x) x := funext_iff

/-- Fibre-transitivity is reachability within every fibre (the definition,
    re-read). -/
theorem fiberTransitive_iff (v : X → C) (P : Set (X → X)) :
    Probe.FiberTransitive v P ↔ ∀ x y, SameFibre v x y → ∃ δ ∈ P, δ x = y := Iff.rfl

/-- `Probe.interventional_iff_closed` through the object: over a
    fibre-transitive set of fibre-preserving probes, interventional silence is
    fibre-preservation by the dynamics. -/
theorem interventional_iff_preserves [Nonempty C] {v : X → C} {T : X → X}
    {P : Set (X → X)} (hblind : ∀ δ ∈ P, ∀ x, SameFibre v (δ x) x)
    (htrans : ∀ x y, SameFibre v x y → ∃ δ ∈ P, δ x = y) :
    (∀ δ ∈ P, Probe.NullResponse v T δ) ↔
      ∀ x y, SameFibre v x y → SameFibre v (T x) (T y) := by
  rw [Probe.interventional_iff_closed (fun δ hδ => (blind_iff v δ).2 (hblind δ hδ))
    htrans]
  exact Habit.closed_iff_fiber_invariant

end Probe

/-! ### Reading 5 — ENTROPY (`Core/FrameEntropy.lean`) -/

section Entropy

variable {State Chart : Type*} [Fintype State] [DecidableEq Chart]

/-- Membership in a frame's fibre at a reading. -/
theorem mem_fiber_iff (view : State → Chart) (c : Chart) (s : State) :
    s ∈ FrameEntropy.fiber view c ↔ view s = c := by
  simp [FrameEntropy.fiber]

/-- **ENTROPY.** `FrameEntropy.fiber view (view t)` is the `SameFibre` class of
    `t`: the entropy counts exactly the states the view cannot tell from `t`. -/
theorem mem_fiber_iff_sameFibre (view : State → Chart) (s t : State) :
    s ∈ FrameEntropy.fiber view (view t) ↔ SameFibre view s t :=
  mem_fiber_iff view (view t) s

end Entropy

/-! ### Reading 6 — RECORD (`Core/DephasingReader.lean`) -/

section Record

variable {n : Type*}

/-- **RECORD.** Under pure dephasing by the diagonal reader `l` (γ > 0, nonzero
    initial coherence), the coherence between `i` and `j` survives iff `i` and
    `j` lie in one fibre of the reader. `DephasingReader.reader_preserves_iff_same_fibre`
    with its conclusion named. ON THE MODEL ONLY. -/
theorem reader_preserves_iff_sameFibre (γ : ℝ) (hγ : 0 < γ) (l : n → ℝ)
    (ρ₀ : Matrix n n ℂ) (i j : n) (hρ : ρ₀ i j ≠ 0) :
    ¬ Tendsto (fun t => DephasingReader.solution γ l ρ₀ t i j) atTop (𝓝 0) ↔
      SameFibre l i j :=
  DephasingReader.reader_preserves_iff_same_fibre γ hγ l ρ₀ i j hρ

end Record

end CIRISOntology.Core.View
