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

**2. [CORRECTED 2026-08-23 — I was wrong.] Certified numerics is a DEPENDENCY, not a build.**
The Mathlib fact below is right; the conclusion drawn from it was not. Two maintained
standalone Lean 4 packages exist and were verified reachable: **LeanCert**
(github.com/alerad/leancert, Apache-2.0, DOI 10.5281/zenodo.21681348, pushed
2026-08-22) providing a `leancert` tactic for point inequalities, quantified bounds
over boxes, root existence, finite sums and definite integrals; and
**girving/interval**, conservative interval arithmetic over a *software* float
(because Lean's native `Float` is untrusted), with `girving/ray` formalizing
Mandelbrot results as the nearest existing computer-assisted dynamics precedent.
Residual cost, stated honestly: neither is Mathlib-integrated, so combining enclosures
with Mathlib's real-analysis API has friction, and no computer-assisted PDE proof has
been formalized end-to-end anywhere. That is an integration cost and an unclaimed
opportunity — NOT the from-scratch build I asserted. The original (wrong) reasoning
is kept below, marked, per the house rule on dead claims.

**2-ORIGINAL, SUPERSEDED: Anything needing CERTIFIED NUMERICS is out of reach without new infrastructure.**
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


## Venue found (2026-08-23): where the entropy work could go
`HEPLean/HepLean` is now **`leanprover-community/physlib`** (physlib.io, Apache-2.0,
707 stars, Lean v4.33.0, lead maintainer Joseph Tooby-Smith; Zulip #479953-Physlib).
It carries a **`t-for-mathlib-qi`** label specifically for quantum-information material
destined for Mathlib, and a `PhyslibAlpha` staging area whose standards explicitly
welcome large or imperfect formalizations. Given that Mathlib has no von Neumann
entropy and we have ~200 audited declarations with no upstream home, this is a
concrete, uncontested deposit target. Caveat from the sweep: of 62 open non-PR issues
only THREE carry a `formalization` label; the rest are API design and documentation.
Physlib is building infrastructure, so it is an on-ramp and a venue — it will not
settle an open question.
