# The Logos Bell test — results (ibm_marrakesh, job d9ichsd0k0jc738jdt40)

**Date:** 2026-07-25. 488 circuits × 1024 shots, 134 QPU seconds. Pre-registration:
`BELL_PREREG.md` (committed `a318d66`, addendum 1 at `5675548`, gate pass `92c1bbe`),
threshold = the machine-checked classical cap (`Core/ShareK.lean`, commit `5c18af7`).

## Verdict: the pre-registered claim rule PASSES, and survives the refuter

**Pre-registered pipeline** (readout-corrected linear inversion + PSD projection,
B = 200 bootstrap):

| quantity | value |
|---|---|
| V (min pair S_vN − whole S_vN) | **+0.8585 nat** (ideal 1.3863) |
| bootstrap 1st percentile | +0.8058 |
| bias-corrected V | +0.8882 |
| S_vN whole | 0.5260 |
| min pair S_vN (of 10) | 1.3845 (ceiling 1.3863) |
| state fidelity | 0.877 |
| readout assignment fidelity (min) | 0.967 (≥ 0.95 ✓) |
| control (classical mixture) V | −0.945, bootstrap p99 = −0.954 (≤ 0 ✓) |

All four claim conditions hold. Every one of the ten pair views carries more entropy
than the whole it is a view of — the pattern `entropy_map_le` proves impossible for
any classical five-slot state.

**Refuter pass (mandatory, per house rules) — reconstruction-free route:** pair
entropies by direct pair tomography from counts; fidelity from the 32 stabilizer
expectations; whole-entropy bounded by the Fannes-type worst case
S ≤ h₂(F) + (1−F)·ln 31. No global reconstruction, no PSD projection anywhere.

- RAW counts (no readout correction at all): min pair S = 1.3835, F = 0.8358,
  S_whole ≤ 1.0104 → **V ≥ +0.3731**.
- Readout-corrected: min pair S = 1.3823, F = 0.9023 → **V ≥ +0.7265**.

The violation survives with every conservative choice stacked against it. The
refuter fails to refute.

## What was measured, stated carefully

A five-qubit ring graph state prepared on ibm_marrakesh was measured, by full
product-basis tomography, to hold whole-only structure that no classical five-slot
state can hold: its every pair view reads more entropy than its whole, violating the
machine-checked classical monotonicity (`entropy_map_le`) by at least 0.37 nat
(worst-case route) and by 0.86 nat (pre-registered estimator). Equivalently, via
`shareK_le_log_sub_pair`: any classical state with these pair readings has share
≤ 5 ln 2 − 1.38 ≈ 2.08 nat, and the measured object's reconstructed whole-only share
(≈ 5 ln 2 − 0.53 − pair-deviation ≈ 2.9 nat) exceeds what classical books permit.

**Scope, honestly:** engineered state, Bell-test methodology — the claim is that
nature's laws permit, and this device physically held, super-classical whole-only
share. It is NOT a claim about wild processes, and the temporal (process-tensor)
version of the question remains open. The k = 5 diagonal ptr↔marginal
correspondence and the mechanized ideal value qShareK(C5) = 5 ln 2 are the named
next Lean bricks.

## Budget ledger

Run 1 (idle): 66 s. Bell run: 134 s. Total 200 s of 600. Remaining ≈ 6.7 min.

## Stance implication (BATCHED for review — not applied)

Candidate claim, pending Eric's review + wording pass: measured — "a physical system
was measured holding more whole-only pattern than any classical five-part system can
carry; the classical bound is machine-checked here, the measurement record is this
repository" — with kill: an error found in the cap proof, the tomography analysis, or
a matched classical simulation reproducing V > 0 under the same pipeline.
