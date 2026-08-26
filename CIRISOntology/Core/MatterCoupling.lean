/-
CIRISOntology.Core.MatterCoupling — BACK-REACTION AS MUTUAL NON-CLOSURE.

The engine has two halves and no join: `ciris-sim-core/src/quantum_link.rs` carries
a DYNAMICAL plaquette flux (`H = 4g²E² − κ(U+U†)`) with no matter in it at all,
while the route sector carries a walker in a BACKGROUND holonomy. `Core/RouteGauge`
killed the identification of those two carriers, and did NOT kill coupling them —
K1 forbids saying route states ARE link flux states, not saying that two distinct
carriers interact.

THE POINT OF THIS FILE is that the coupling needs no new primitive. It is already
sayable in `Core/Habit`'s vocabulary:

  **matter moves flux and flux gates matter — so NEITHER view is `Closed`.**

`Closed v T` says a view determines its own successor. Were there no back-reaction,
the matter reading would predict matter and the flux reading would predict flux, and
both would be Closed. Back-reaction IS the failure, on both sides at once. Nothing
is added to the object; a coupling is a pair of non-closures.

THE MODEL, and it is deliberately the smallest thing that can carry the shape: one
matter particle on two sites, one link between them carrying the same spin-1
truncated flux the engine already uses (`{−1,0,+1}`, here indexed `Fin 3`). A hop
DRAGS the flux — crossing left-to-right raises it, right-to-left lowers it — and is
BLOCKED at the truncation boundary, exactly as `plaquette_raise` returns `None` at
`+1` ("the finite spin-1 truncation, not a gauge violation"). That blocking is what
makes the flux gate the matter; the drag is what makes the matter move the flux.

WHAT IS AND IS NOT CLAIMED. This is a MODEL BRICK on six states. It is not lattice
gauge theory, it does not derive Gauss's law, and `gauss_held` below is a computed
invariant of THIS map, not a theorem about nature. A U(1) link with staggered matter
is long-standing ground — Horn (Phys.Lett.B 100:149, 1981), Orland–Rohrlich
(Nucl.Phys.B 338:647, 1990), Chandrasekharan–Wiese (Nucl.Phys.B 492:455, 1997), and
the Schwinger-model literature generally. Nothing here is new physics. What is ours
is the reading: back-reaction stated as mutual non-closure of the object's own
`Closed`, so the connection stops being background WITHOUT a second primitive.

SCOPE FENCE, inherited and not widened: this file says nothing about the route
sector's carrier. It does not re-open K1 and does not identify anything with
anything.
-/
import CIRISOntology.Core.Habit

namespace CIRISOntology.Core.MatterCoupling

/-- Position of the one particle: `false` = left site, `true` = right site. -/
abbrev Pos := Bool

/-- The link's flux, in the engine's own spin-1 truncation: `0,1,2` reading `−1,0,+1`. -/
abbrev Flux := Fin 3

/-- The joint state. Six of them. -/
abbrev LinkState := Pos × Flux

/-- **THE STEP.** The particle hops and DRAGS the flux; the hop is BLOCKED where the
    truncation has no room, which is the engine's own convention and not a gauge
    violation. The guards mean the `Fin 3` arithmetic never wraps. -/
def hop (s : LinkState) : LinkState :=
  if s.1 then
    (if 0 < s.2.val then (false, s.2 - 1) else (true, s.2))
  else
    (if s.2.val < 2 then (true, s.2 + 1) else (false, s.2))

/-- Read the matter, discard the flux. -/
def matterView : LinkState → Pos := Prod.fst

/-- Read the flux, discard the matter. -/
def fluxView : LinkState → Flux := Prod.snd

/-! ### Back-reaction, stated twice -/

/-- **FLUX GATES MATTER.** The matter reading does not determine its own successor:
    two states agreeing on where the particle is disagree on where it goes next,
    because one is at the truncation boundary and the other is not. -/
theorem matter_not_closed : ¬ Habit.Closed matterView hop := by
  rintro ⟨φ, hφ⟩
  have h1 : matterView (hop (false, 1)) = φ (matterView (false, 1)) := congrFun hφ _
  have h2 : matterView (hop (false, 2)) = φ (matterView (false, 2)) := congrFun hφ _
  simp [matterView, hop] at h1 h2
  exact absurd (h1.symm.trans h2) (by decide)

/-- **MATTER MOVES FLUX.** The flux reading does not determine its own successor
    either: two states agreeing on the flux disagree on the next flux, because the
    particle crosses in opposite directions. This is the back-reaction proper. -/
theorem flux_not_closed : ¬ Habit.Closed fluxView hop := by
  rintro ⟨φ, hφ⟩
  have h1 : fluxView (hop (false, 1)) = φ (fluxView (false, 1)) := congrFun hφ _
  have h2 : fluxView (hop (true, 1)) = φ (fluxView (true, 1)) := congrFun hφ _
  simp [fluxView, hop] at h1 h2
  exact absurd (h1.trans h2.symm) (by decide)

/-! ### What IS closed: the two sectors are locked together -/

/-- Charge and flux, added mod 2. -/
def gauss (s : LinkState) : Bool := decide (((cond s.1 1 0) + s.2.val) % 2 = 1)

/-- **THE LOCK — Gauss's law in miniature, and the non-vacuous half.** Neither view
    is Closed, but this joint reading is `Held`: it survives the step unchanged. You
    cannot move the charge without moving the flux. Computed on all six states, so
    it is an invariant of THIS map and not a theorem about nature. -/
theorem gauss_held : Habit.Held gauss hop := by
  funext s
  revert s
  decide

/-- The lock is not the whole state: `gauss` is a genuinely lossy view, so
    `gauss_held` is not `Held` at the identity view wearing a disguise. -/
theorem gauss_is_lossy : ∃ s t : LinkState, gauss s = gauss t ∧ s ≠ t := by
  exact ⟨(false, 0), (true, 1), by decide, by decide⟩

end CIRISOntology.Core.MatterCoupling
