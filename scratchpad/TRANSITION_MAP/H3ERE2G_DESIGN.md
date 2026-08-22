# H3ERE2-G — a GENERATOR of acceptable transformations (design, 2026-08-23)

Steward's architecture: **SLM decomposes → structural middle generates and filters →
same SLM renders an action.** The SLM does perception and expression; it does NOT do
the safety-critical reasoning. That is the right split, and the object supplies most of
the middle.

```
 input/state ──SLM──▶ (kind, content) tuples over the 11+1
                          │
                    ┌─────▼─────────────────────────────┐
                    │  STRUCTURAL MIDDLE  (no network)  │
                    │  reachability · equivalence ·     │
                    │  cost · acceptability · ordering  │
                    └─────┬─────────────────────────────┘
                          │  chosen typed transformation
      action ◀──SLM───────┘
```

## 1. COMPRESSIBILITY IS THE TRACTABILITY RESULT FOR THE MIDDLE
The middle searches transformations. Naively that is over N states; the surviving
simulation result says it is over **G profile classes** instead — measured at
**G=64 giving 6.3% of full arithmetic at N=1024, a 15.9× reduction**, with the
reduction improving as N grows. `GrayAlgebra.Kmat_det_ne_zero` + its converse say
exactly when this is available: **not when the state space is small, but when complete
relational profiles REPEAT.** Distinctness destroys confinement; degeneracy creates it.
So the middle stage is cheap precisely when many situations are relationally alike —
which is the normal case in a deployed UI, and is checkable at runtime (covering number
of observed profiles at the tolerance the UI needs).

## 2. WHAT THE OBJECT SPECIFIES, tied to theorems
| the middle needs | the object supplies | tie |
|---|---|---|
| a transformation TYPE SYSTEM | the eleven kinds, exhaustive given the model | `Generator.generator_image`, `WrongKind.basePlane_card` |
| REACHABILITY (what can change what) | the grounding order — a real partial order | `Stack.*`, `FrameOrder.repairable_monotone` |
| …but NOT a plan tree | hierarchy is rare (~21%); cycles are generic | M8 (CHORD-1) — **planner must handle cycles, not assume a DAG** |
| EQUIVALENCE classes (the compression) | the two twin swaps, exact up to measured breaking | `Symmetry.aut_with_stack_card` = 4 |
| a COST for conflating equivalents | breaking has two parts: magnitude AND direction | `DefectCoupling.defect_split` |
| a RISK/FRAGILITY model per move | fragility is POSITIONAL: rate = dose² × field susceptibility | **M9** — susceptibility computable from the field BEFORE the move |
| IRREVERSIBILITY marking | Record is one-way, machine-zero backflow | `Generator.record_not_site_generated`, Leg A S4 = 0.0000 |
| ACCEPTABILITY evaluated correctly | laws are of a connected field, never per-kind | **M7** — a move may NOT be judged in isolation |

**M9 is the one that surprised me into usefulness:** it gives the planner a *cost
function* that is computable from the field alone, before any move is applied. Fragility
is a property of where a distinction sits, not of how hard you push it.

**M7 is the binding safety constraint:** acceptability cannot be a per-move predicate.
Any implementation that scores moves independently is wrong by a result we proved today.

## 3. ACCEPTABILITY — where CIRIS principles enter
The filter is not learned; it is the covenant, evaluated over the field:
- the floor test (legitimacy at the point of least power) applies to the RESULTING
  field state, not to the move;
- irreversibility (Record) raises the bar — a one-way move needs stronger warrant;
- deep moves cost more than surface moves (depth as price, G1/M1), so prefer the
  shallowest transformation that reaches the goal;
- Wisdom-Based Deferral is the natural output when no acceptable transformation exists —
  the generator should be ABLE to return "defer", and that must be a first-class result,
  not a failure.

## 4. HONEST LIMITS — and a licensing reframe that matters
- **H3ERE2 is NOT LICENSED** (held-out wild κ = 0.3488 against a 0.40 bar). A generator
  built on it inherits that.
- **But the bar is different for this use.** The 0.40 bar was for a MEASUREMENT
  instrument, where a wrong label corrupts a statistic silently. In a UI the
  decomposition is a **proposal the user can see and correct**, and the middle stage is
  auditable independently of how the tuple was obtained. The right bar for a generator
  is *usefulness plus correctability*, and it should be stated and measured as such
  rather than borrowing the measurement threshold.
- The wild ceiling (κ ≈ 0.25–0.36, substrate-intrinsic across three samples) means even
  a perfect decomposer would disagree with a human panel at that rate on wild text. A UI
  must therefore be designed for disagreement: show the kind, allow the correction, and
  let the correction feed the record.
- Nothing here is validated as a deployed system. This is a design tied to results, not
  a claim that it works.

## 5. MINIMAL FIRST BUILD
1. **Typed state**: represent a situation as commitments across the 11 kinds (+Record).
2. **Move generator**: enumerate typed transformations reachable under the grounding
   order; collapse by twin equivalence; keep the direction from `defect_split`.
3. **Cost**: positional fragility (M9) + depth price + irreversibility premium.
4. **Filter**: covenant evaluation on the RESULTING FIELD (M7), with `defer` available.
5. **Render**: SLM turns the chosen typed move into an action, and shows the type.
Stage 2's collapse is where the 15.9× lives; stage 4 is where the safety lives; the SLM
never touches either.
