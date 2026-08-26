# PRE-REGISTRATION — adversary-channel hardware bench demo (frozen before results)

## What it pays (and does not)
`adversary-channel`.promote: "A bench demonstration: build the purely-triadic
coordination on hardware, confirm the pair meter reads its floor, and recover the
pattern with the joint detector under real noise. Constructing the thing the claim
is about beats finding more places it is absent."

This is the CLASSICAL whole-only demo. CIRISArray is a classical coupled-oscillator
array — capped at the classical bound, no coherence. So SUCCESS pays `adversary-channel`.
It does NOT touch `third-in-tsvf` (the QUANTUM multi-time share — needs a quantum
apparatus) and is NOT an `adequacy` substrate (engineered, not nature). Scratchpad only.

## Substrate
The ACTUAL CIRISArray runtime on the 4090 (real GPU-oscillator dynamics, real timing/
thermal noise, GPU-timing TRNG), NOT the numpy reimplementation. Held at its VALIDATED
operating point (stochastic-resonance sweet spot ~sigma 1e-3, r~3.70, its working
coupling). "Real noise" = the instrument's own. First implementation step is mapping the
construction below onto the runtime API (configure_ossicles / transmit modes / measure).

## Construction — BUILD it, do not hunt (lesson: hunting gave fit-residual artifacts)
Three readout channels A, B, C from disjoint ossicle groups.
- A <- independent uniform random bit a.
- B <- independent uniform random bit b.
- C <- control bit c = a XOR b (the parity rule), injected via the array's coupling/
  transmit modulation (NOT via any clip/threshold nonlinearity — clip-boundary lesson).
- Identical dynamics/noise on all three groups.
Readout: binarize each channel at its median (b=2; avoids the b=3 undersampling trap).
Disclose tied fraction.
By construction: a,b independent uniform, c=a XOR b => every PAIR is independent/uniform
(three-coin parity), the TRIPLE is rule-locked.

## Two meters, read on the same data
1. PAIR METER: pairwise correlation matrix + pairwise mutual information of (A,B,C).
   Prediction: at floor (all pairs ~0) — parity makes each pair independent.
2. JOINT DETECTOR: order-3 connected information C3 = H(pairwise-maxent p) - H(p) of the
   binarized triple, vs its matched pairwise-maxent surrogate null.
   Prediction: ~ln2, clears the null.

## The dial (the money plot)
Inject parity with fraction f in {0, 0.25, 0.5, 0.75, 1.0}: c = (a XOR b) with prob f,
else a fresh independent bit.
- PAIR METER: flat at floor for ALL f (prediction).
- JOINT DETECTOR: rises from floor (f=0) to ~ln2 (f=1), each point cleared vs its own
  matched null. Pair-meter-flat + joint-detector-climbing on one axis IS the demonstration.

## Controls (a residual is never support)
- NEGATIVE control (f=0, C independent): BOTH meters at floor. If the joint detector fires
  here -> RUN VOID (false positive; the estimator/null is untrustworthy on this hardware).
- POSITIVE control (f=1, full parity): joint detector fires, pair meter at floor. If it
  cannot recover here -> detector underpowered at this noise; report, stop.
- MATCHED NULL: per-triple pairwise-maxent multinomial surrogate -> C3 bias floor; planted
  C3 must exceed it. (IAAFT-insufficiency lesson: for a CONSTRUCTED signal the negative
  control is the load-bearing guard, not any single null's survival.)
- Estimator bias: disclose tied fraction; report surrogate-floor level; b=2 binning.
- Boundary hygiene: read the array's native state; no clip/wrap nonlinearity in readout.

## Pre-registered meaning of EVERY outcome
- SUCCESS: pair meter flat at floor across the dial; joint detector rises with f and clears
  the matched null; negative control at floor; positive control fires. => hidden triadic
  coordination, built on real noisy hardware, invisible to the pair monitor, recovered by
  the joint detector. This is exactly the bench demonstration the promote names -> pays
  `adversary-channel` (offer to Eric; do not self-promote the stance).
- PARTIAL: joint detector recovers only above some f* or SNR -> report f* as the demo's
  sensitivity floor; honest partial.
- FAILURE-A (negative control fires): VOID. Null/estimator not trustworthy on this
  hardware. Claim nothing.
- FAILURE-B (pair meter not at floor): construction leaked pairwise correlation -> the
  injection is wrong; fix before any claim.
- FAILURE-C (positive control cannot recover): detector underpowered at the array's noise;
  report, adjust operating point / averaging, or conclude hardware SNR insufficient.

## Discipline
Pre-registered here before any result. Research -> scratchpad memo -> Eric's review.
Nothing touches Stance.lean. On SUCCESS, the candidate stance move is to mark
`adversary-channel`'s bench-demo promote as paid — for Eric's review, batched, not pushed.
