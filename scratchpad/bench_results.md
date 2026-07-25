# adversary-channel bench demo — RESULTS (pre-registered; frozen prereg in bench-...-prereg.md)

VERDICT: **SUCCESS — with a MECHANISM CORRECTION added 2026-07-25, see the top-of-file
correction block below before reading anything else.**

> ## CORRECTION (2026-07-25) — the readout runs through the clamp
>
> This document's prereg asserts the injection is "a smooth parameter modulation, NOT a
> clip/threshold readout nonlinearity (clip-boundary lesson honored)". A boundary
> discriminator run later (ARRAY_CAP_RESULTS.md, DIAG A) shows that was honoured in
> INTENT but not IN FACT. Re-running this exact construction (f=1, delta=0.10, T=4000)
> under a reflecting fold instead of the kernel's native clamp, with nothing else changed:
> bit recovery 0.94/0.94/0.94 -> 0.67/0.68/0.69, share 0.2511 -> 0.0010 (259x), and the
> channel's response to the injected bit REVERSES SIGN. Raising coupling pins more cells
> on the 0.001/0.999 rails and pinned cells are perfectly correlated in the phase metric.
>
> What survives: the DETECTION (the parity was externally constructed; the f=0 control
> floors), and the null at THIS demo's low-coupling operating point (integrated
> autocorrelation ~1). What does not: the claim that the number is a property of the
> array's dynamics. Every figure below is scoped to this kernel's native clamped readout.
>
> Separately: at couplings >= 0.35 the iid multinomial surrogate breaks down entirely
> (autocorrelation time 87-365, independent cross-run channels fire at z=34.9). Those
> couplings are outside this demo's range but any future run must not use that null there.
 (candidate for human review; pays `adversary-channel` bench-demo promote; nothing pushed to Stance.lean).

## Substrate — REAL runtime
Drove the ACTUAL CIRISArray GPU kernel (`/home/emoore/CIRISArray/src/runtime.py`,
`Ossicle.measure`, the r=3.70 diffusively-coupled logistic lattice at line ~176) on the
RTX 4090. NOT the numpy reimplementation, NOT a hand-written driver.
- 3 disjoint ossicle groups (rows) x 64 ossicles = 192 ossicles = channels A,B,C.
- Bits a,b indep uniform; c = a XOR b w.p. f, else fresh indep bit.
- Injection: bit -> COUPLING modulation on its group (coupling 0.05 -> 0.05+0.10). A smooth
  parameter modulation, NOT a clip/threshold readout nonlinearity (clip-boundary lesson honored).
- Held at validated SR operating point: additive sigma=1e-3 noise on oscillator states, r=3.70.
- Readout per channel = group-mean of the 'phase' metric (mean pairwise correlation of the 3
  oscillators). Binarize each channel at its OWN median (b=2). Two meters on the SAME data.

## GATE (before hardware) — PASS
- exact three-coin parity -> C3 = 0.693147 (= ln2). exact independent -> C3 = 0.
- sampled T=4000: parity z=2919 fires, pair floor; independent z=-0.7 floor. Surrogate bias floor ~2e-4.

## Money plot — primary seed 20260724, T=4000, 60 surrogates
| f | pair max|corr| | pair maxMI (nats) | C3_obs | null mean+/-sd | excess | z | tie | recov A,B,C |
|---|---|---|---|---|---|---|---|---|
| 0.00 | 0.038 | 7.2e-4 | 0.0000 | 0.0001+/-0.0002 | -0.0001 | -0.7 | 0.000 | .94/.94/.94 |
| 0.25 | 0.038 | 7.2e-4 | 0.0136 | 0.0001+/-0.0002 | 0.0134 | 67.4 | 0.000 | .94/.94/.93 |
| 0.50 | 0.034 | 5.8e-4 | 0.0539 | 0.0001+/-0.0002 | 0.0538 | 271.3 | 0.000 | .94/.95/.94 |
| 0.75 | 0.020 | 2.0e-4 | 0.1428 | 0.0001+/-0.0002 | 0.1427 | 750.1 | 0.000 | .94/.95/.94 |
| 1.00 | 0.011 | 6.1e-5 | 0.2628 | 0.0001+/-0.0001 | 0.2627 | 1867.7 | 0.000 | .94/.95/.93 |

Pair meter FLAT at floor across the whole dial (all |corr| within ~2.4sigma of 0; sampling
floor at T=4000 is sigma=1/sqrt(4000)=0.0158). Joint detector climbs monotonically from floor
(f=0, z=-0.7) to C3=0.263 (f=1, z=1868), every point clearing its own matched null.

## Controls
- NEGATIVE (f=0): both meters floor, C3 z=-0.7. NOT void. Reproduced z = -0.7 / +0.5 / -0.3 over 3 seeds.
- POSITIVE (f=1): joint detector fires z=1868; pair at floor. Reproduced z = 1868 / 1614 / 1364.
- Reproducibility: seeds 20260724, 99, 7 all give same shape (f=0 |z|<1; f=1 z>1300; monotone).
- SHUFFLE-C refuter (break trial alignment at f=1): C3 -> 0.0000, z in [-0.7,+0.5] over 5 shuffles
  (mean -0.40). Shuffle-all: z=-0.5. Confirms C3 is the constructed alignment, not an estimator artifact.

## Honest caveats
1. Real runtime used, but SR noise (sigma=1e-3) injected on states BETWEEN the kernel's 100-iter
   bursts (kernel has no per-iteration noise hook), not per-update. Minor: the dominant real noise
   is the chaotic logistic dynamics + finite-64-cell correlation sampling + float32 (that is what
   caps per-channel recovery at ~94%; per-ossicle d'~0.4, group-mean d'~3).
2. C3 at f=1 ~0.26 nats, WELL BELOW ideal ln2=0.693: real hardware noise (imperfect ~94% recovery)
   ate ~60% of the ideal parity. Noise is load-bearing, not cosmetic — and the demo still holds.
3. Runtime kernel has NO inter-ossicle coupling: the 3 groups do not physically interact. The
   triadic structure is IMPOSED via 3 independent control lines; the array supplies the per-channel
   real noise. Faithful to "BUILD it, do not hunt" — NOT a claim the array spontaneously makes parity.
4. b=2 median binarization; tied fraction = 0.000 (continuous group-mean readouts; b=3 trap avoided).

Files: bench_detector.py (meters+gate), bench_experiment.py (driver), bench_refuter.py (shuffle),
bench_probe.py / bench_dprime*.py (operating-point calibration).
