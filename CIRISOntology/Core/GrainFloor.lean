/-
CIRISOntology.Core.GrainFloor — you cannot buy your way out of a floor, and the
only operation that moves one is a change of frame.

WHY THIS EXISTS. `GrainFloor` is the engine's central refusal: a request to refine
below a tier's declared grain is refused rather than answered. It appears in
fourteen Rust modules and, until this file, in no Lean at all — the goal was
carrying an object the tool used everywhere and the lake named nowhere.

WHAT FORCED IT. The 4090 design study (`sim_engine/SANDBOX_4090.md`, commit
71a7509) was commissioned to design an atomically-accurate sandbox out of many
small holon engines on one card, and it turned NEGATIVE on its own headline. The
part that belongs here is not the throughput arithmetic; it is the correction the
study made to its own earlier pass. That pass had sold deeper residency as where
atomic accuracy lives. Measured, it is not: the card holds 1.19 grains of sand at
1 µm, and Z0 GRAIN's crack claim demands ℓ_ch/10 = 4.222e-7 m of a tier whose
floor is 1e-6 m — 2.37× short, ALWAYS, by the tier's own arithmetic. Capacity
lifted the floor by exactly zero. **`GrainFloor` is a property of the CLAIM
against g0, never of how many holons you can afford.**

THE FOUR STATEMENTS, and which are content.

  * `inadmissible_persists` and `admissibility_change_is_reroot` are the CONTENT.
    No refinement inside a tier makes an inadmissible claim admissible; and if a
    claim is refused on one tier and served on another, the second tier's floor is
    strictly finer. Refinement is bounded below by the floor; the only lever that
    moves the answer is a RE-ROOT, which is a change of base frame, not a step
    inside one.
  * `z0_crack_claim_inadmissible` / `z0_shortfall_factor` pin the engine's measured
    arithmetic into the lake: the shortfall is in (2.36, 2.37), machine-checked,
    so the study's number cannot drift away from the proof.
  * `capacity_irrelevant` and `demand_not_function_of_geometry` are NAMED
    RESTATEMENTS, flagged as such in the house style of `Core/ExchangeSign.lean`'s
    `pauli_cap`. They are true by construction. Their value is that the refusal is
    now DEFINED claim-relatively where CI can point at it, and that the scheduler
    consequence has a witness: two shards of identical size and grain can carry
    wildly different certification demand, so a geometry-based load balancer is
    wrong by construction. Balance by claim.

  * `cert_does_not_transport_across_reroot` is the FENCE, and it is the kernel of
    the study's G4 — *nothing certifies a join across a re-root*. A certificate is
    tier-indexed; the exhibited claim is served at the finer tier and refused at
    the coarser one, so a certificate earned on one side of a re-root states
    nothing on the other. Until the re-root ledger gate lands, a multi-tier swarm
    is uncertified BY CONSTRUCTION and the first swarm must be single-tier.

CONVERGENCE, recorded as the house pattern asks. `reroot_finer_admits_more` makes
tiers an ORDER under their floors with admissibility monotone along it — the same
shape `Core/FrameOrder.lean` finds for `Repairable`, and the same axis
`Core/FrameEntropy.lean`'s `frameEntropy_refine_le` rides. Three objects, one
structure: frames are an order, and the quantities that matter are monotone along
it, never invariant under it. That also sharpens the fence — `frameEntropy` is
monotone under REFINEMENT and simply not comparable across a RE-ROOT, because a
re-root replaces the base rather than refining it. G4 is that non-comparability in
the certificate coordinate.

THE SECOND KIND OF REFUSAL, and why it is in this file. Lighting up the vacuum
tier produced a refusal the ladder had not seen: the spin-1 link's **flux
ceiling**. Every other refusal in the engine says *I cannot see finely enough*.
This one says *there is nothing finer* — the link's state space has three values
and there is no fourth, so the refusal is exact rather than a resolution limit.
That distinction is not decoration, because it is exactly what the theorems above
turn on: `admissibility_change_is_reroot` says a floor refusal MOVES under a
re-root, and a ceiling refusal cannot, at any tier, ever. So the two kinds are
individuated by an invariance, and the test that separates them is a re-root —
the programme's own move (*only invariants individuate*) applied to the engine's
refusals. The final section mechanizes it: `capDemand_not_frameRelative` and
`invariant_refusal_is_universal`, with the engine's spin-1 link as the witness.

That also DRYs three things the lake was carrying separately. `Core/ExchangeSign`'s
`pauli_cap` (occupancy is `Bool`), `Core/ModeChart`'s `level_cap` (a g-degenerate
level holds at most g), and the flux ceiling are ONE KIND of refusal — a bound
belonging to the state space rather than to the chart — and `GrainFloor` is the
other. Graded honestly, per the house lesson about counting instantiations as
witnesses: that is scope, three instances of one kind, not three confirmations.

SCOPE. A model brick, and a small one: tiers and claims are single positive
lengths, caps are counts. It derives no physics and it does not establish that the
engine's floors are the right floors. It fixes what kind of quantity a refusal is.
The model's fidelity has a kill: if the engine ever delivers resolution finer than
a tier's declared g0 without a re-root, `achieved`'s clamp is the wrong model of
refinement and this file's content theorems describe nothing. The taxonomy has its
own, separable kill: if some re-root ever serves a demand the engine has typed as
a ceiling, that demand was a floor refusal misfiled, and the classification below
is not tracking the engine's actual refusals.
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace CIRISOntology.Core.GrainFloor

/-- A tier: one declared grain floor, strictly positive. The engine's `g0`. -/
structure Tier where
  g0 : ℝ
  g0_pos : 0 < g0

/-- A claim: the length scale a question demands be resolved. Z0 GRAIN's crack
    claim demands `ℓ_ch/10`. -/
structure Claim where
  ell : ℝ
  ell_pos : 0 < ell

/-- The claim is servable on the tier exactly when the tier's floor is no coarser
    than the scale demanded. This is the whole of the refusal: two numbers, and
    neither of them is a capacity. -/
def admissible (T : Tier) (c : Claim) : Prop := T.g0 ≤ c.ell

theorem admissible_iff (T : Tier) (c : Claim) : admissible T c ↔ T.g0 ≤ c.ell :=
  Iff.rfl

/-! ### Refinement inside a tier is bounded below by the floor -/

/-- Achieved resolution after `n` refinement steps at ratio `r` from an initial
    cell — clamped at the tier's declared floor. The clamp IS the floor: it is the
    modelling choice this file makes, and the kill in the header is aimed at it. -/
noncomputable def achieved (T : Tier) (cell₀ r : ℝ) (n : ℕ) : ℝ :=
  max T.g0 (cell₀ / r ^ n)

/-- No number of refinement steps crosses the floor. -/
theorem achieved_ge_floor (T : Tier) (cell₀ r : ℝ) (n : ℕ) :
    T.g0 ≤ achieved T cell₀ r n :=
  le_max_left _ _

/-- **CONTENT.** A refused claim stays refused under every amount of refinement
    inside the tier. Refining harder is not a route to an answer; it is the same
    refusal, later. -/
theorem inadmissible_persists (T : Tier) (c : Claim) (h : ¬ admissible T c)
    (cell₀ r : ℝ) (n : ℕ) : c.ell < achieved T cell₀ r n :=
  lt_of_lt_of_le (not_le.mp ((admissible_iff T c).not.mp h)) (achieved_ge_floor T cell₀ r n)

/-! ### The only lever is a re-root -/

/-- **CONTENT, and the load-bearing statement.** If a claim is refused on `T` and
    served on `T'`, then `T'` has a strictly finer floor. The answer to a refusal
    never changes inside a tier; when it changes, the tier changed — and a change
    of tier is a change of base frame, not a step within one. -/
theorem admissibility_change_is_reroot {T T' : Tier} {c : Claim}
    (h : ¬ admissible T c) (h' : admissible T' c) : T'.g0 < T.g0 :=
  lt_of_le_of_lt ((admissible_iff T' c).mp h') (not_le.mp ((admissible_iff T c).not.mp h))

/-- Tiers are ORDERED by their floors, and admissibility is monotone along that
    order: a finer tier serves everything a coarser one serves. (The convergence
    with `Core/FrameOrder.lean`'s `repairable_monotone` is noted in the header —
    same structure, third object.) -/
theorem reroot_finer_admits_more {T T' : Tier} (h : T'.g0 ≤ T.g0) {c : Claim}
    (hc : admissible T c) : admissible T' c :=
  le_trans h ((admissible_iff T c).mp hc)

/-- Admissibility is monotone in the claim: a coarser question is served wherever
    a finer one is. -/
theorem admissible_mono {T : Tier} {c₁ c₂ : Claim} (h : c₁.ell ≤ c₂.ell)
    (h₁ : admissible T c₁) : admissible T c₂ :=
  le_trans ((admissible_iff T c₁).mp h₁) h

/-! ### Capacity is not in the domain

An arena carries a tier and a capacity. Only one of the two appears in the
refusal. -/

/-- A concrete arena: a tier, and however many holons it can afford to hold. -/
structure Arena where
  tier : Tier
  capacity : ℕ

def arenaAdmissible (A : Arena) (c : Claim) : Prop := admissible A.tier c

/-- **NAMED RESTATEMENT** (true by construction; see the header). Two arenas on the
    same tier answer every claim identically however their capacities differ. This
    is what the 4090 study's measured correction says: 1.19 grains of sand resident
    on the card lifts `GrainFloor` by exactly zero. -/
theorem capacity_irrelevant (T : Tier) (c : Claim) (m n : ℕ) :
    arenaAdmissible ⟨T, m⟩ c ↔ arenaAdmissible ⟨T, n⟩ c :=
  Iff.rfl

/-- **NAMED RESTATEMENT**, and the scheduler's version: demand is not a function of
    geometry. One tier — one size, one grain — serves one claim and refuses
    another, so two shards of identical geometry can carry different certification
    cost. A geometry-based load balancer is wrong by construction; balance by
    claim. -/
theorem demand_not_function_of_geometry :
    ∃ (T : Tier) (c₁ c₂ : Claim), admissible T c₁ ∧ ¬ admissible T c₂ := by
  refine ⟨⟨1 / 1000000, by norm_num⟩, ⟨1 / 1000, by norm_num⟩,
          ⟨4222 / 10000000000, by norm_num⟩, ?_, ?_⟩ <;>
    simp only [admissible_iff] <;> norm_num

/-! ### The engine's measured arithmetic, pinned

Z0 GRAIN declares a 1 µm floor; its crack claim demands `ℓ_ch/10 = 4.222e-7 m`. -/

/-- The Z0 GRAIN tier: floor 1e-6 m. -/
noncomputable def z0Tier : Tier := ⟨1 / 1000000, by norm_num⟩

/-- Z0's crack claim: `ℓ_ch/10 = 4.222e-7 m`. -/
noncomputable def z0CrackClaim : Claim := ⟨4222 / 10000000000, by norm_num⟩

/-- The refusal, machine-checked on the engine's own numbers. -/
theorem z0_crack_claim_inadmissible : ¬ admissible z0Tier z0CrackClaim := by
  simp only [admissible_iff, z0Tier, z0CrackClaim]
  norm_num

/-- The shortfall factor lies in `(2.36, 2.37)` — the study's "2.37× short",
    pinned so the prose cannot drift from the proof. -/
theorem z0_shortfall_factor :
    236 / 100 * z0CrackClaim.ell < z0Tier.g0 ∧ z0Tier.g0 < 237 / 100 * z0CrackClaim.ell := by
  simp only [z0Tier, z0CrackClaim]
  constructor <;> norm_num

/-- And it is not purchasable: no refinement inside Z0 reaches the crack claim. -/
theorem z0_crack_claim_not_purchasable (cell₀ r : ℝ) (n : ℕ) :
    z0CrackClaim.ell < achieved z0Tier cell₀ r n :=
  inadmissible_persists z0Tier z0CrackClaim z0_crack_claim_inadmissible cell₀ r n

/-! ### The fence: G4 -/

/-- **THE FENCE.** A certificate is tier-indexed, and admissibility is not
    preserved across a re-root: the exhibited claim is served at the 1e-7 tier and
    refused at the 1e-6 tier. So a certificate earned on one side of a re-root
    states nothing on the other, and a join across one is not covered by either.
    This is the kernel of `SANDBOX_4090.md`'s G4 — until the re-root ledger gate
    lands, a multi-tier swarm is uncertified by construction. -/
theorem cert_does_not_transport_across_reroot :
    ∃ (T T' : Tier) (c : Claim), admissible T' c ∧ ¬ admissible T c := by
  refine ⟨z0Tier, ⟨1 / 10000000, by norm_num⟩, z0CrackClaim, ?_,
          z0_crack_claim_inadmissible⟩
  simp only [admissible_iff, z0CrackClaim]
  norm_num

/-! ### Two kinds of refusal, separated by a re-root

The engine's ladder now carries both. A FLOOR refusal is the chart failing to
resolve what was asked, and a re-root can serve it. A CEILING refusal is the state
space ending, and nothing serves it — the spin-1 link has three flux values and
there is no fourth at any tier. The two are individuated by an invariance, and the
discriminating experiment is a re-root. -/

/-- A cap: how many values a state space carries. The gauge link's flux has three;
    `Core/ExchangeSign`'s `pauli_cap` slot has two; `Core/ModeChart`'s g-degenerate
    level has `g+1`. One kind, three instances — scope, not three witnesses. -/
structure Cap where
  values : ℕ
  values_pos : 0 < values

/-- A cap demand is served exactly when it lands inside the state space. Note what
    is ABSENT from the definition: the tier. -/
def capAdmissible (K : Cap) (k : ℕ) : Prop := k < K.values

/-- A demand, as the ladder sees it: for each tier, whether that tier serves it. -/
def Demand : Type := Tier → Prop

/-- A floor demand — served by tiers fine enough. -/
def floorDemand (c : Claim) : Demand := fun T => admissible T c

/-- A ceiling demand — the tier does not appear, and that is the whole point. -/
def capDemand (K : Cap) (k : ℕ) : Demand := fun _ => capAdmissible K k

/-- A demand is FRAME-RELATIVE when some re-root changes its answer. -/
def frameRelative (D : Demand) : Prop := ∃ T T' : Tier, D T ∧ ¬ D T'

/-- **CONTENT.** A ceiling demand is not frame-relative: no re-root changes its
    answer, because the tier never entered the question. This is the exact sense in
    which the flux ceiling is *not* a GrainFloor. -/
theorem capDemand_not_frameRelative (K : Cap) (k : ℕ) :
    ¬ frameRelative (capDemand K k) := by
  rintro ⟨_, _, h, h'⟩
  exact h' h

/-- A floor demand IS frame-relative, whenever two tiers straddle the claim. -/
theorem floorDemand_frameRelative (c : Claim) (T T' : Tier)
    (h : T.g0 ≤ c.ell) (h' : c.ell < T'.g0) : frameRelative (floorDemand c) :=
  ⟨T, T', h, not_le.mpr h'⟩

/-- **CONTENT, and the classification.** A refusal that no re-root moves is refused
    at EVERY tier. So the ladder can tell its two refusals apart by experiment:
    re-root and look. A floor refusal moves (`admissibility_change_is_reroot` says
    that when it moves, the tier is what changed); a ceiling refusal is universal,
    and zooming forever will not serve it. -/
theorem invariant_refusal_is_universal {D : Demand} (hinv : ¬ frameRelative D)
    {T : Tier} (h : ¬ D T) : ∀ T' : Tier, ¬ D T' := by
  intro T' hT'
  exact hinv ⟨T', T, hT', h⟩

/-- The engine's witness: the spin-1 gauge link carries three flux values. -/
def spin1Flux : Cap := ⟨3, by norm_num⟩

/-- **THE FLUX CEILING, at every tier at once.** Raising past the third value is
    refused, and no zoom anywhere on the ladder serves it. This is the refusal that
    is exact rather than a resolution limit. -/
theorem flux_ceiling_refuses_at_every_tier : ∀ T : Tier, ¬ capDemand spin1Flux 3 T := by
  intro T h
  simp only [capDemand, capAdmissible, spin1Flux] at h
  omega

/-- And it is refused for the reason the taxonomy says: not because any tier is too
    coarse, but because nothing depends on the tier at all. -/
theorem flux_ceiling_is_not_a_floor_refusal :
    ¬ frameRelative (capDemand spin1Flux 3) :=
  capDemand_not_frameRelative _ _

end CIRISOntology.Core.GrainFloor
