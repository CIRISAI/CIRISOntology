/-
CIRISOntology.Core.Corridor — the corridor's two walls, stated on the rent
clause's own objects.

This is the brick owed by the bridge note in the predecessor record
(coherence-ratchet, `papers/notes/torque_rent_corridor_bridge.md`, 2026-08-31):
the corridor that survives the programme's own kills is not an operating band
on mean correlation — that claim died under adversarial review and is not
restated here in any form — but the RENTED INTERIOR between two deaths, and
both walls compose directly with `Core/Maintenance.lean`:

  * the DISSOLUTION wall is `unpaid_decays` — pay nothing and the entry tends
    to zero;
  * the STASIS wall is `stasis_wall` below — over the worlds the model can
    hold, minimizing rent selects exactly the contentless world. Cost-alone
    selection picks the dead world. This mechanizes, in the rent model, the
    selection statement demonstrated exactly at CIRISHolon's TOE-NULL-1
    adjudication (SELECTOR-1): whatever selects must balance maintenance
    against productive organization, because rent-minimization alone exits
    the corridor at its frozen wall;
  * the interior is INHABITED, forever: any positive amount is held exactly
    steady for all time by paying its own rent (`corridor_inhabited`, from
    `paid_const`) — and holding it costs strictly positive payment
    (`living_rent_pos`), which is why the interior is called rented.

The mathematics here is deliberately immediate — a few lines each. The content
is the COMPOSITION: both walls and the inhabited interior stated on the same
`step`/`rent` objects the rent clause proves things about, so the corridor is
one file's worth of reading and cannot drift from the clause it rests on.

SCOPE, inherited from `Maintenance.lean` verbatim: this proves the MODEL and
only the model. The collapse pole (S → ∞, where an ensemble stops being a
state) is kernel-checked in the predecessor's formal tree
(coherence-ratchet `formal/CoherenceRatchet/`), not restated here. No claim
about any real system is made in this file; the stance carries those
separately, at their own strengths, with their own kills.
-/
import CIRISOntology.Core.Maintenance

namespace CIRISOntology.Core

/-- The rent of holding an amount `S` against decay fraction `γ`: exactly the
    payment `rent_holds` proves buys standing still. -/
def rent (γ S : ℝ) : ℝ := γ * S

/-- Paying `rent γ S` is precisely what holds `S` steady — the definition
    above is the one `rent_holds` is about, not a new quantity. -/
theorem rent_is_the_holding_price (γ S : ℝ) : step γ (rent γ S) S = S :=
  rent_holds γ S

/-- THE STASIS WALL. Over the worlds the model can hold (`0 ≤ S`), the dead
    world is always weakly cheapest, and it is the UNIQUE minimizer: rent
    ties the dead world's price only at zero content. A selector that
    minimizes rent alone therefore selects the contentless world — cost-alone
    selection is the frozen death, not safety. -/
theorem stasis_wall {γ : ℝ} (hγ : 0 < γ) {S : ℝ} (hS : 0 ≤ S) :
    rent γ 0 ≤ rent γ S ∧ (rent γ 0 = rent γ S ↔ S = 0) := by
  unfold rent
  constructor
  · nlinarith
  · constructor
    · intro h
      nlinarith
    · intro h
      simp [h]

/-- Holding anything at all costs strictly positive rent: the interior is
    rented, not free. -/
theorem living_rent_pos {γ S : ℝ} (hγ : 0 < γ) (hS : 0 < S) :
    0 < rent γ S := by
  unfold rent
  positivity

/-- THE INTERIOR IS INHABITED, FOREVER. Any positive amount is held exactly
    steady for all time by paying its own rent at every step — the corridor
    between the walls is not empty, and occupancy is bought, not given. -/
theorem corridor_inhabited (γ : ℝ) :
    ∃ S₀ : ℝ, 0 < S₀ ∧ ∀ n : ℕ, paid S₀ γ n = S₀ :=
  ⟨1, one_pos, fun n => paid_const 1 γ n⟩

end CIRISOntology.Core
