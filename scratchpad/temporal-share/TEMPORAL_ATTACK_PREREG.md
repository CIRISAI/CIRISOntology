# Pre-registration — the temporal re-attack: the share of a process, on the object

**Date:** 2026-07-25. **Status:** written BEFORE the phase-A numerics were run. The
instrument (tomography + entropy pipeline + theorem-gated prereg ladder) is validated
end-to-end by the Bell run (BELL_RESULTS.md, incl. correction). This document stakes
the temporal definition and the meaning of the phase-A outcomes; the hardware phase
gets its own addendum after phase A, before any job.

## The definition (the recognition, staked)

The whole-only share of a three-step quantum process is `qShare` — already mechanized
in `Core/ShareQuantum.lean` for arbitrary finite slot dimensions — applied to the
process's **Choi state over times**, with **slot k = the (input, output) leg pair of
time-step k** (dimension 4 per slot for a qubit process; the first slot is the
initial output leg, dimension 2). The two-time views are the pair partial traces
`ptr₁₂`/`ptr₁₃`/`ptr₂₃` of that object. Nothing new needs defining: the temporal
share IS the spatial functional on the temporal object. Per the 2026-07-24
kill-check, no pairwise-blind share on any multi-time object is published; this
identification is the claim to novelty, and it is falsified by finding it in print.

## Phase A — exact numerics, predictions staked first

Compute V (min pair S_vN − whole S_vN) and the share on the exact Choi states of
three process classes (one qubit, three times, causal breaks between steps):

1. **Markov process** (fresh unitary noise each step, no memory).
   PREDICTION: V < 0, share ≈ 0 — a Markov comb factorizes across the causal cuts.
2. **Classical-memory process** (the parity process: one classical bit carried).
   PREDICTION: V < 0 (the comb is separable across time; classical memory obeys
   monotonicity), share ≤ the classical cap.
3. **Coherent-memory process** (memory qubit entangling the times, returned
   decoupled at the end so the comb is pure).
   PREDICTION: V > 0 — the causal analog of the Bell violation: two-time views
   more entropic than the three-time whole. If this holds, the quantum edge
   SURVIVES the causal constraint, answering the campaign's open question
   (established for states, open for processes) in the affirmative, exactly.

**Meaning of outcomes:** (1) or (2) coming out V > 0 → the classical/causal
baseline is wrong or the construction is buggy — stop, diagnose, nothing proceeds.
(3) coming out V ≤ 0 for EVERY decoupled-memory construction tried → the causal
constraint may genuinely forbid the temporal edge — a major negative, recorded, and
the hardware phase is CANCELLED (no point measuring for an effect theory forbids);
the open claim's promote path would need re-thinking. (3) positive → phase B.

## Phase B (sketch; own addendum before any job)

The validated ladder, temporally: process tomography (measure-and-reprepare causal
breaks, IC instrument set) of (i) the coherent-memory comb — must violate (positive
control), (ii) the classical-memory comb — must obey (negative control), (iii) THE
NATURAL PROCESS: the device's idle dynamics at delays ~10–50 µs, the actual
`third-in-tsvf` promote clause. Thresholds from phase-A values + the machine-checked
classical monotonicity. Budget ≈ 400 s remaining; one job.
