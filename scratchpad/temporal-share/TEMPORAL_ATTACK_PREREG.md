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

---

## PHASE-A OUTCOME (2026-07-25, same day): prediction 3 FIRED NEGATIVE — and it is a theorem

Staked classes 1 and 2 came out exactly as predicted (Markov and classical-memory
combs obey, V < 0; identity Markov saturates V = 0). Prediction 3 — that a coherent
memory could produce a temporal violation — **failed universally**: 0 of 800
Haar-random causal processes and every engineered coherent comb give V ≤ 0, best
exactly 0.

**The reason is structural, and short.** Comb causality forces the future input leg
out: tr_O3(T) = T₁₂ ⊗ I/2 (verified to 8×10⁻¹⁷ over 300 random combs). Araki–Lieb
then gives S(T) ≥ S(tr_O3 T) − S(O3) ≥ S(T₁₂) + ln 2 − ln 2 = S(past-pair). So for
EVERY causally ordered three-step process, the past-facing pair view never exceeds
the whole — hence min-pair ≤ whole, V ≤ 0 (verified: zero violations, 300 random
combs). **The Bell-type temporal edge is forbidden by causality itself.**

**The asymmetry is the fingerprint.** Only the contiguous-past view is protected;
the middle-skipping (1,3) view CAN exceed the whole (SWAP comb: 1.386 > 0.693).
Causality restores classical entropy monotonicity toward the past and only toward
the past — an arrow-of-time structure sitting inside the entropy pattern of the
state-over-times.

**Consequences, per the staked rules:**
- The hardware phase for the temporal-edge hunt is CANCELLED (the staked
  cancellation rule: no measuring for an effect theory forbids). Budget preserved.
- The campaign's open question — does the quantum edge survive the causal
  constraint? — is answered NO, in the min-pair form, with a three-line proof from
  standard ingredients (comb causality + Araki–Lieb). The framing is plausibly
  unpublished (the 2026-07-24 kill-check found no pairwise-blind-share treatment of
  multi-time objects at all), but the ingredients are textbook — held at wager
  confidence pending a literature pass; NOT claimed as deep new mathematics.
- Mechanization: the proof needs Araki–Lieb for von Neumann entropy, absent from
  Mathlib — named open step. The classical face (monotonicity) is already
  mechanized (`entropy_map_le`).
- Stance implication (BATCHED): `third-in-tsvf`'s "measure whether nature's books
  carry any" now has a sharper answer available for the causal-past form: nature's
  causally ordered books provably CANNOT carry super-classical whole-only share
  against their own past — the temporal Logos exists (temporal-memory, proved) but
  is classically bounded, unlike the spatial. Wording awaits Eric's review.

---

## Addendum 2 (2026-07-25, literature pass): the causal bound is CONVERGENT art

The phase-A outcome note held the causal-monotonicity framing "at wager confidence
pending a literature pass." The pass has now run. "Entropic limitations on fixed
causal order" (arXiv:2505.13681, May 2025) proves entropic inequalities for
fixed-causal-order processes whose Theorem 1, in the equal-dimension case, reads
H(whole) >= H(past) — our vnEntropy_causal_past, published months before our
independent derivation. As with the Schur product theorem: external validation of
the result, and the claim to new physics is withdrawn. What remains ours: the
machine-checked formalization (the Araki-Lieb ladder and the bound itself, which
that literature does not formalize), and the SHARE framing — the same pass
re-confirmed (arXiv:2312.10147 uses only bipartite mutual information on Choi
states and defines no pairwise-blind/connected measure) that the whole-only share
on multi-time objects and its memory-saturation characterization remain unpublished.
