# Phase 3 pre-registration — the share of a natural process, on quantum hardware

**Date:** 2026-07-24. **Status:** written BEFORE any circuit was built, any simulator
run, or any hardware job submitted. Per `epistemology.md` L1 this fixes the method, the
estimator, the nulls, and the meaning of every possible outcome. The QPU budget is 10
free minutes; nothing is submitted to hardware until the simulator gate below passes
AND Eric signs off on this document.

## The target: a natural process, honestly scoped

The open claim's last unpaid leg is "measure one natural process." The natural process
chosen: **the device's own idle dynamics** — one qubit of an IBM quantum processor,
measured at three successive times with free evolution (delay) between them. The
environment doing whatever it does between our looks is nature, not our rule. This is
deliberately NOT the engineered parity circuit — that appears below only as the
positive control (instrument validation), exactly as the CIRISArray bench demo was
honestly scoped as detector-validation.

**Claim domain if positive:** "this device, these timescales, the classical shadow of
its three-time readout process in the swept bases." Nothing broader.

## Design

One system qubit. Three measurement events M₁, M₂, M₃ (mid-circuit measurement),
each preceded by a basis rotation (and followed by the inverse), with delay `d`
between events. Outcomes form p̂(z₁, z₂, z₃).

- **Basis grid:** all 27 combinations B ∈ {X, Y, Z}³ (the Kant-test lesson: a single
  fixed probe is basis-contaminated; the sweep is the tomographic hedge).
- **Delays:** d₁ = 0 (back-to-back) and d₂ ≈ 2 µs (nearest backend-dt multiple).
- **Shots:** 4096 per circuit. 27 × 2 = 54 idle circuits.
- **Positive control (2 circuits, Z basis, both delays):** the one-remembered-bit
  parity process on hardware — `memory_realizes_parity` as a circuit: q0 in |+⟩;
  CNOT q0→q1; M₁(q0); H(q0); M₂(q0); CNOT q0→q1; M₃ = measure q1. Ground truth
  share = ln 2. No feedforward needed.
- **Negative control (2 circuits, Z basis, both delays):** same event structure, no
  memory: q0 |+⟩; M₁; H; M₂; H; M₃ all on q0 — a genuinely memoryless chain. Ground
  truth share = 0. Carries the SAME mid-circuit-measurement and readout systematics
  as the idle circuits — it is the matched instrument-noise null (L2: the null must
  match the generative structure of the measurement, not just the data).

Total: 58 circuits × 4096 shots, one job, estimated ≪ 5 of the 10 minutes.

## Estimator (fixed)

The mechanized definition, applied to each p̂: share(p̂) = H(σ̂\*) − H(p̂), natural log,
where σ̂\* is the maximum-entropy distribution with p̂'s three pair marginals, computed
by iterative proportional fitting (IPF) to tolerance 1e-12. This is `Core/Share.lean`'s
object, numerically.

## Nulls (fixed before any data)

1. **Estimator-bias floor (L4):** per circuit, parametric bootstrap — B = 1000 draws
   of 4096 samples from σ̂\* itself (whose true share is 0); the empirical distribution
   of the estimator on these draws is the floor. Report measured share as exceedance.
2. **Max-statistic over the grid:** the per-delay claim statistic is the MAX share
   over the 27 bases; its null is the max over the 27 per-basis bootstrap shares
   within each replicate. No Bonferroni gymnastics; the max-null is exact for the
   max-claim.
3. **Instrument-systematics floor:** the negative control's measured share (same
   measurement machinery, genuinely memoryless process). The idle claim must clear
   BOTH floors.

## Meaning of every outcome (fixed before any data)

- **Positive control off** (share outside ln 2 ± 3× its bootstrap spread, either
  delay): run VOID. No claim in any direction; the instrument failed on hardware.
  Report loudly, fix, re-pre-register before any further spend.
- **Negative control hot** (share above its own bootstrap floor by > the claimed
  threshold): mid-circuit measurement systematics manufacture false share; run VOID
  for claiming, kept as an instrument finding.
- **Idle share ≤ floors everywhere** (max over bases below both nulls, both delays):
  an honest NULL: no whole-only three-time share detected in this device's idle
  readout process at these timescales, sensitivity ≈ the floor (report it, L5). The
  open claim stays open; nothing promoted; the null is recorded as loudly as a
  positive would have been (L8).
- **Idle share > both floors** (max-statistic, empirical p < 0.01, either delay, and
  effect ≥ 0.01 nat): the first measured nonzero whole-only share of a natural
  process. Promotes ONLY the "measure one natural process" leg — separable; the
  definitional claims stand on their proofs regardless. Requires the refuter pass
  (second-guess rule) before any stance/page change.
- **Effect present but < 0.01 nat:** below the pre-set sensitivity bar — reported as
  "below sensitivity," claimed as nothing.

## Simulator gate (must pass before ANY hardware job)

On Aer, full pipeline end-to-end: (a) ideal positive control reads ln 2 within
bootstrap spread; (b) ideal negative control reads inside its floor; (c) under an Aer
noise model (readout error + depolarizing + thermal relaxation at device-like rates)
the positive control still clears the floors — the sensitivity check. Any failure:
fix pipeline, re-run gate; hardware only after a clean pass.

## Budget discipline

One main job. No adaptive re-runs based on peeking. If minutes remain and the main
job is clean, a SECOND pre-registered job (denser delays) may be designed — as its
own addendum to this document, written before submission, after Eric's sign-off.
