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

---

## CORRECTION (2026-07-25, same day, after prior-art review — before any stance change)

**The phrase "first measured super-classical Logos share" above and in commit
`cbe8919` is an over-claim, and is retracted.** The convergent-art review (requested
by Eric before promotion — correctly) finds the measured PHYSICS is textbook and has
been measured before, in stronger systems:

- Subsystem entropy exceeding the whole is THE standard entropic signature of
  entanglement: negative conditional entropy (Cerf–Adami, PRL 1997), operational
  meaning via state merging (Horodecki–Oppenheim–Winter, Nature 2005). For pure
  entangled states it is immediate, and every entangled-state tomography experiment
  since ~2001 implicitly demonstrates it.
- It has been measured DIRECTLY and framed as the beyond-classical entropy signature:
  Rényi entropies of subsystems above the pure whole in ultracold atoms (Islam et
  al., Nature 528, 77, 2015) and trapped ions via randomized measurements (Brydges
  et al., Science 364, 260, 2019).
- The state itself, AME(5,2) = the 5-qubit ring graph state, is a known object with
  published preparation circuits for superconducting hardware (Cervera-Lierta,
  Latorre, Goyeneche, "Quantum circuits for maximally entangled states," PRA 100,
  022342, 2019 — AME circuits designed to benchmark quantum computers).
- The classical bound (entropy monotone under marginalization) is Shannon-era
  textbook; our `entropy_map_le` is a MECHANIZATION of a known fact, never new
  mathematics, and the file said so.

**What this run actually is:** an end-to-end validation of OUR instrument — the
mechanized share formalism, the theorem-gated pre-registration method, and the
tomography pipeline — against physics that was never in doubt. The same honest
scoping as the CIRISArray bench demo: it validates the detector, it does not
discover the phenomenon. No staked promote condition is satisfied (`third-in-tsvf`
requires a NATURAL process; `logos` is proved and needed no hardware). Discipline
L6 applies: the confirmed advance prediction here was quantum mechanics', not ours.

**What remains ours, stated narrowly:** (1) the share defined on the
state-over-times — the TEMPORAL object — which the 2026-07-24 kill-check found
unpublished and which this spatial experiment did not touch; (2) the mechanized
theorem set (cap included) as verification artifacts; (3) possibly the METHOD — a
hardware experiment whose claim threshold is a machine-checked theorem committed
before the data, with pre-registered kills, gates, and refuter — for which we found
no precedent, held at wager confidence since today's search was partial.

**Stance recommendation:** no new flagship claim. At most, fold this run into
existing confidence/promote prose as instrument validation (adversary-channel
precedent), at Eric's discretion.
