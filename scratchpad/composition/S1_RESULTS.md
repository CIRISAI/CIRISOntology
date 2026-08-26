# S1 — four-arm adjudication. **2 of 4 arms PASS; the confidence exit is DEAD; top line pending S2 but already at most UNPROVEN.**

Job `da7lelmsidac73afgso0`, screened pair (95, 99), 34 s quota this job (80 total
campaign, 520 remaining). Frozen bands: `COMPOSITION_PREREG.md` §2.

| arm | staked (law 2) | measured | verdict |
|---|---|---|---|
| idle | both defects at floor | 0.1× / 0.3× | **PASS** |
| **common-driver** | both at floor ∧ created corr above floor | 0.0× / 0.0×, **created 0.616 nats ≈ 2800× floor** | **PASS — the atlas-derived signature, first hardware confirmation** |
| one-way | fwd ≥ 50× floor ∧ asym ≥ 20× | fwd 342×, **asym 18.0×** | **MISS (band edge: 18.0 vs 20)** |
| reciprocal | both ≥ 20× floor | fwd 361×, **rev 0.2×** | **MISS (outright)** |

## The reciprocal miss, attributed at the counts level (diagnostic, not rescue)

Transpilation is clean: 4 CZs, and the CZ-basis synthesis carries the full ideal
reverse influence (P(A′=1 | prep 01) = 0.50). Hardware: prep 01 flipped A at
**0.082** — the second CRX (control q1 → target q0) delivered ~6× under strength
while the first ran near-ideal (0.96). The physically realized channel was not
reciprocal coupling at the staked strength. Same lesson as RESTORATION: **the
compiled gate is not the ideal gate**, now measured a second way. The miss stands
as staked; the attribution is recorded, not used.

The one-way miss is a band-edge drift: the pilot measured 88× asymmetry on this
pair; today's session delivered 18× against a 20× band frozen from the pilot's
epoch. Device drift between sessions was not in the model. Miss stands.

## What passed is not nothing

The two arms that DEFINE the detector's semantics both passed on hardware: closure
reads clean where nothing couples, and the common-driver arm — both directional
defects at zero while 0.62 nats of correlation is created — is the signature that
separates influence from correlation, derived in the atlas, staked in the freeze,
and never before tested on hardware. Law 2's DISCRIMINATIONS are confirmed; its
STRENGTH BANDS are what missed.

## A defect in the freeze itself, recorded

The falsification exit ("requires a refit to avoid a miss ⇒ notation") is
toothless as written: it fires only if the claimant RESCUES, which the no-rescue
clause forbids anyway. A falsification exit must be closable by DATA alone.
Lesson for any successor freeze: stake the notation-verdict on a defined
data condition (e.g., "≥ half the staked arms miss on any substrate"), not on
the claimant's subsequent behavior.
