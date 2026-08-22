# FORMALIZATION READINESS — what our stack can actually attack (2026-08-23)

Written while the target sweep runs, so capability is assessed BEFORE seeing the
target list and cannot be bent to fit it.

## Surveyed: what Mathlib gives us
| area | Mathlib coverage | verdict |
|---|---|---|
| TensorProduct | 143 files | strong |
| MeasureTheory | 357 files | strong |
| Deriv / analysis | 302 files | strong |
| Convexity | 140 files | strong |
| spectrum, unitary | 60 / 20 files | usable |
| Matrix.PosSemidef | 3 files | THIN |
| **von Neumann entropy** | **0 files — ABSENT** | **gap** |
| **certified/interval arithmetic** | **none found** | **BLOCKER** |

## Two conclusions that should govern target choice

**1. Our comparative advantage is QUANTUM INFORMATION formalization.**
Mathlib has no von Neumann entropy at all. We have built and audited roughly 200
declarations across `Core/{Entropy, EntropyIneq, ShareK, ShareQuantum, BellCeiling,
HammingCap, Third, Coordination}` — density matrices, partial traces, entropy
inequalities, a classical cap, a quantum ceiling with the C5 graph state's pair
marginals computed, and `bell_ceiling_exceeds_cap`. That is a working quantum-info
library in a language whose standard library lacks the central object. Any target in
this area starts from a real head start rather than from zero.

**2. Anything needing CERTIFIED NUMERICS is out of reach without new infrastructure.**
There is no interval-arithmetic library in Mathlib (the `Order/Interval` files are
order-theoretic, not numeric enclosures). So the celebrated computer-assisted-proof
class — Lorenz-attractor existence, fluid blowup enclosures, celestial-mechanics
rigour — would require building a certified-numerics stack first. That is a large
project in its own right and should be costed as such, not slipped in as a step.

## The shape of target we should prefer
Given the above, the tractable shape is: **a finite or algebraic core, in quantum
information or combinatorics, where the open question is whether a bound is tight or a
small configuration exists.** We have already done exactly this shape twice today
(`defect_split`, an exact identity; `GrayAlgebra`, a theorem with its converse
replacing a finite numerical check at N ≤ 128).

## Honest limits to state on any proposal
- No HPC allocation, no apparatus, no proprietary data.
- One GPU; good for exploration up to ~10^6 states, not for HPC-scale sweeps.
- Formalization effort is real: today's four modules took a full working session each
  in wall-clock terms, and they were EASY relative to open problems.
- A machine-checkable core does not make a problem easy; it makes it decidable in
  principle. The gap between those is where projects die.
