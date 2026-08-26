# CLOSURE PILOT — results

**Verdict, in one line: DIRTY BASELINE. The directions are separable by 88×, and the
idle pair does not close.** Both halves are reported as loudly as each other.

Design frozen in `CLOSURE_PILOT_PREREG.md` and committed before `closure_pilot.py`
existed. Backend `ibm_marrakesh`, pair (95, 99) chosen by measured screening,
τ = 64 ns, θ = π/2, 4096 shots × 8 circuits, one job, arms interleaved.
Screen `da7gjtu0ukec73839emg`, pilot `da7gkk3sq5js73bjufp0`.
**Cost: 17 s of 600** (583 remaining), against a pre-registered estimate of 16–21 s.

## The readings

| arm | `Δ_{A→B}` | floor | ×floor | `Δ_{B→A}` | floor | ×floor |
|---|---|---|---|---|---|---|
| **P0** idle | 8.612e-5 | 1.901e-4 | **0.45** | 3.364e-4 | 2.016e-4 | **1.67** |
| **P1** one-way CRX | 9.281e-2 | 1.821e-4 | **509.69** | 1.053e-3 | 1.684e-4 | **6.25** |

Forward/reverse asymmetry in P1: **88.1×**.

## What fired, by the prereg's own decision table

`DIRTY BASELINE` is checked first and it fires: P0's `Δ_{B→A}` sits at 1.67× its
permutation floor. **The idle pair does not close in one direction.**

The prereg's reading of this outcome, written before the data:

> The idle pair already fails to close: crosstalk at rest. Not a failure of the pilot —
> it is a finding, and it would mean the four-arm's "independent" arm is unavailable on
> this device and must be replaced by a measured-crosstalk baseline rather than an
> assumed-zero one.

That stands as written. **The four-arm may proceed, with its independent arm redefined
as a MEASURED baseline.**

## The separability question is answered, and answered strongly

The pilot existed to ask whether direction is readable at all. It is: P1's forward
residual is **510× its floor** while the reverse is 6.25×, an **88× asymmetry** on a
coupling that is one-way by construction. The instrument reads a known one-way
structure with the correct sign and a large margin. Directionality is not the risk it
was staked as.

## Cautions, including a defect in MY design

1. **The two exceedances are not comparable in strength.** P0's is 1.67× a 95th
   percentile; P1's forward is 510×. Recording both as "above floor" flattens a
   difference of two and a half orders of magnitude.
2. **No multiple-comparison correction was pre-registered, and four quantities are
   tested.** At 95th-percentile floors roughly one test in twenty exceeds by chance, so
   the family-wise false-positive rate across four is ≈19%. **P0's `Δ_{B→A}` is
   therefore consistent with chance.** This is a defect in the frozen design, recorded
   as one — **it is NOT used to reinterpret the verdict.** The rule was what it was and
   DIRTY BASELINE fired under it. A successor must declare its correction in advance.
3. **τ = 64 ns is ~3 orders below T1.** Whatever P0's residual is, it is unlikely to be
   dynamical crosstalk accumulated over the delay; readout or preparation correlation is
   the more plausible mechanism. That is a hypothesis and was not measured here.

## No rescue

The job was not re-run, `θ` and `τ` were not refit, no preparation was dropped, and the
statistic was not changed. One job, one reading, reported as it came.

## What this does NOT buy

Detecting directional influence between coupled qubits via a conditional divergence is
standard practice. A separable reading corroborates **the instrument**, not the
ontology — `CLOSURE_PILOT_PREREG.md` §8. The maximal object earns evidence only if one
frozen structure predicts all four arms with fewer freedoms than separate effective
models (`OBJECT_PRIOR_ART.md`).

## Sequel, owed before the four-arm freezes

- Declare a family-wise correction, in advance.
- Replace the "independent" arm's assumed-zero with the measured baseline this pilot
  produced.
- Determine whether P0's residual is readout/preparation or dynamical, by sweeping τ:
  a preparation/readout artefact is τ-independent, a dynamical one is not.
