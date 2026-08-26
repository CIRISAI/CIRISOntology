# Pre-registration — CLOSURE PILOT: are directional residuals separable on hardware?

**Date: 2026-08-26. Written and committed BEFORE the instrument exists and before any
reading.** Instrument: `closure_pilot.py`, to be written after this file is committed.
Raw: `closure_pilot_<jobid>.json`. Results: `CLOSURE_PILOT_RESULTS.md`.

## 0. What this is, and what it is NOT

This is a **gauge check on a ruler**, not a test of anything in the stance. Its only
job is to decide whether the four-arm closure challenge is runnable on this hardware
at all. It answers one question:

> Can a directional closure residual be distinguished from its reverse, on this
> device, for a deliberately ASYMMETRIC coupling?

**If not, the four-arm design VOIDS before it is staked**, and no QPU seconds are spent
on it. Two campaigns in this repository died staking that a boundary varies along an
axis without measuring the spread first (house memory,
`measure-the-boundary-spread-first`). This file is the refusal to make that mistake a
third time.

**Nothing here tests the maximal object.** A pass licenses the four-arm experiment and
nothing else.

## 1. Why directionality is the load-bearing part

`Core/MatterCoupling.lean` proves `independent_views_closed`: when the step is a
PRODUCT map, both component views are `Closed`, for every such map. That is what makes
non-closure a detector of interaction rather than a generic affliction. The four-arm
experiment's discriminating power lives entirely in the **one-way** arm — if
`Δ_{A→B}` and `Δ_{B→A}` cannot be separated, "reciprocal" and "one-way" read the same
and the design tests nothing.

**Crosstalk on superconducting hardware is generally reciprocal.** So separability is
a real risk and not a formality.

## 2. The instrument — preparation-based, no mid-circuit measurement

Closure asks whether `A_{t+1}` depends on `B_t` given `A_t`. Computing that from
measured pairs would need mid-circuit measurement and its error budget. It does not
have to.

**Prepare the input, measure the output.** For each of the four computational basis
inputs `(A_t, B_t) ∈ {00,01,10,11}`, evolve and measure `(A_{t+1}, B_{t+1})`. That
yields the full transition matrix `T : (A_t,B_t) → (A_{t+1},B_{t+1})` directly. The
input is KNOWN BY PREPARATION, never inferred.

Then, exactly as `Closed` states it:

- **`Δ_{B→A}`** — does `B_t` move `A_{t+1}` at fixed `A_t`?
  `Δ_{B→A} = Σ_{a} w_a · D_JS( P(A_{t+1} | A_t=a, B_t=0) ‖ P(A_{t+1} | A_t=a, B_t=1) )`
- **`Δ_{A→B}`** — the mirror, swapping roles.

`D_JS` is the Jensen–Shannon divergence in nats; `w_a = 1/2`, the two input values
weighted equally by construction, not by an observed frequency. **The statistic is
declared here and is not chosen after seeing the data.**

## 3. The two arms, one job, one environment

Both arms are submitted in ONE job, interleaved, on the same qubit pair, per the
one-run-one-environment rule (`Q10_PREREG.md` M2).

| arm | circuit | frozen expectation |
|---|---|---|
| **P0 — idle** | prepare, `delay(τ)`, measure | both residuals at the shot floor: with no coupling, both views close |
| **P1 — one-way** | prepare, `CRX(θ)` with **A control, B target**, `delay(τ)`, measure | `Δ_{A→B}` above floor, `Δ_{B→A}` at floor |

`τ` and `θ` are fixed in the instrument at commit time and are reported in the results
file whatever they are. `θ = π/2` and `τ` = the device's shortest supported non-zero
delay, so the arms differ in the coupling and in nothing else.

**Qubit selection is by MEASURED screening, never by `backend.properties()`** — house
memory `qpu-published-calibration-unusable`: published calibration came back 13× worse
than measured and VOIDed a 72-second job. The screen is a separate ~6 s job and its
readings are reported.

## 4. The floor, declared before it is needed

`Δ` is a divergence between two estimated distributions and is **positively biased at
finite shots** — it cannot be compared to zero. The floor is established by
**permutation**: shuffle the `B_t` label within each `A_t` stratum, recompute `Δ_{B→A}`,
repeat 500 times, take the 95th percentile. Same for the mirror. Bias is therefore
measured on the same data and the same shot count, not modelled.

Shots: 4096 per circuit, 8 circuits (2 arms × 4 preparations).

## 5. The decision, and every outcome named

| outcome | reading |
|---|---|
| **SEPARABLE** — in P1, `Δ_{A→B}` exceeds its permutation floor AND `Δ_{B→A}` does not, AND both are at floor in P0 | The ruler works. The four-arm challenge is licensed and may be pre-registered. |
| **NOT SEPARABLE** — in P1 both residuals exceed floor together, or neither does | **The four-arm design VOIDS.** Either the coupling is reciprocal as delivered, or the effect is below the shot floor. No seconds are spent on the four-arm. This is the outcome the pilot exists to catch and it is reported as loudly as a pass. |
| **BACKWARDS** — in P1 `Δ_{B→A}` exceeds floor while `Δ_{A→B}` does not | The instrument reads direction with the WRONG SIGN. That convicts the analysis or the circuit convention, not the hardware, and must be found before anything is staked. |
| **DIRTY BASELINE** — P0 shows either residual above floor | The idle pair already fails to close: crosstalk at rest. Not a failure of the pilot — it is a finding, and it would mean the four-arm's "independent" arm is unavailable on this device and must be replaced by a measured-crosstalk baseline rather than an assumed-zero one. |
| **VOID** | Job error, calibration drift mid-job, or screening failure. Reported as VOID, never as any of the above. |

## 6. No rescue

No refitting `θ` or `τ`, no dropping preparations, no switching the statistic, no
re-running until a direction appears. One job. If it VOIDs on device error the job may
be resubmitted UNCHANGED once, and the resubmission is recorded.

## 7. Cost

~6 s screening + ~10–15 s pilot, against 600 s of quota measured at 600 remaining
(2026-08-26, `usage_remaining_seconds: 600`). The four-arm, if licensed, is budgeted
separately at ~200–250 s.

## 8. What a pass does NOT buy

Detecting directional influence between coupled qubits via a conditional divergence is
**standard practice**, and a pass corroborates the instrument, not the ontology. The
maximal object earns evidence only if ONE frozen structure predicts all four arms with
fewer freedoms than separate effective models — `OBJECT_PRIOR_ART.md`'s standing
verdict. This pilot is a gauge check. It is filed as one.
