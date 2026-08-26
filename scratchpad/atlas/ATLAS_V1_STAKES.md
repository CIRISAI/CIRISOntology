# Finite-model atlas v1 — stakes, written before the enumeration runs

*2026-08-26. The atlas is pure mathematics — no researcher degree of freedom about
nature — but the stakes are still written first, because an enumeration that "finds"
what its author already proved reads as discovery when it is verification, and the
two must not blur. Program context: `OBJECT_INVARIANT_HUNT.md`.*

## Staked analytically, before the run

**S1 (proved, machine-checked).** On a product space with coordinate views,
deterministic dynamics: both views `Closed` **iff** the step is a product map —
`both_closed_iff_product`, `Core/MatterCoupling.lean`, axioms `[Quot.sound]`. The
atlas's deterministic sweep must confirm this EXACTLY (256/256 at 2×2) or the
enumeration code is wrong, not the theorem.

**S2 (staked, to be measured).** The iff FAILS stochastically, and the gap is exactly
common drivers: `a' = a⊕n`, `b' = b⊕n`, one shared `n ~ Bern(q)` gives
`I(B_t; A_{t+1} | A_t) = 0 = I(A_t; B_{t+1} | B_t)` (both views closed) while the joint
channel creates correlation (`I(A'; B' | A,B) > 0`). Consequence for the QPU
intervention matrix: a common-driver control arm is MANDATORY — closure defects read
directed influence, not correlation.

**S3 (staked as a refutation of a bridge AS STATED).** "Whole-only share = contextual
fraction" is dead on arrival for classical states: every classical joint distribution
is its own global section, so NO classical state is contextual in the
Abramsky–Brandenburger sense — while the three-coin parity state carries share `ln 2`.
Share does not lower-bound contextuality and cannot equal it. The bridge, if any,
must be a FUNCTOR: (state, chart, measurement cover) → empirical model, with the claim
reshaped to "qShare bounds the contextual fraction of the induced model." (C5 graph
states are known contextuality witnesses — plausible positive instance, not verified
here.)

**S4 (constraint on Ω from the flat-limit theorem).** Any unifying defect Ω must
REDUCE, in the fixed-cover limit, to: zero on the view axis (`factors_cycle_trivial` —
provably flat), free on transport (`transport_loop_can_be_nontrivial`). The stack
(state-dependent cover) is the only place `D_v` and `F_γ` can unify; `loop_asymmetry`
is the boundary condition Ω must satisfy.

## What the atlas hunts (not staked — open)

**H1 — the autonomy–memory–work frontier.** Across small repair models: pairs
(closure defect Δ_v of the unrepaired dynamics, minimum repair rate W* forcing the
view Held). Question: does a substrate-independent frontier `βW* ≥ f(Δ_v)` exist with
f derived, not fitted? v1 only PLOTS the frontier on one model family; any claimed f
would need derivation plus a second family.

## Kill for the atlas itself

If the deterministic sweep contradicts S1, the atlas code is wrong and every other
number it prints is void until repaired.
