# Phase-3 run 1 — results record (ibm_marrakesh, job d9ibr3t0k0jc738jcv4g)

**Date:** 2026-07-25. 58 circuits × 4096 shots, 66 QPU seconds. Counts:
`hw_counts_ibm_marrakesh_d9ibr3t0k0jc738jcv4g.json`; analysis:
`hw_verdict_ibm_marrakesh_d9ibr3t0k0jc738jcv4g.json`, pipeline at commit `9c15933`.

## Verdict, by the pre-registered letter: VOID for claiming

The positive-control criterion in HW_PREREG.md ("share within ln 2 ± 3× bootstrap
spread") fired: measured 0.4327 (d=0) and 0.4006 (2 µs) against ln 2 = 0.6931. Per the
outcome table, no claim in any direction is made from this run.

**The criterion was mis-staked, and we say so plainly:** our own simulator gate
predicted 0.4357 for the positive control under device-like noise — the hardware
delivered 0.4327, within 0.003 nat of the model. The prereg demanded the IDEAL value
of a NOISY instrument; that is an authoring error in the pre-registration, not an
instrument failure, and it is exactly the kind of error the void-not-reinterpret rule
exists to catch. Any future run judges the positive control against the noise-modeled
band, staked in advance (done: BELL_PREREG.md).

## The data, as data

- **Positive control:** 0.4327 / 0.4006 nat vs noisy-model 0.4357 — instrument tracks
  the model on real hardware; the 2 µs delay costs ~0.03 nat (decoherence).
- **Negative control:** 6×10⁻⁵ / 6×10⁻⁶ nat — the mid-circuit measurement machinery
  does not manufacture share. False-positive floor ≈ nil.
- **Idle (natural process):** max over 27 bases = 0.0019 nat (d=0, YYY) and
  0.0021 nat (2 µs, ZZZ), each p = 0.002 against the max-statistic shot-noise null,
  both clearing the negative control — and both ~5× BELOW the pre-set 0.01-nat
  sensitivity bar. By the prereg: "below sensitivity, claimed as nothing."
- **Reading (not a claim):** a qubit holding its collapsed state between looks IS a
  one-bit memory; three noisy readouts of that persistent bit form a
  mixture-of-products distribution, which generically carries small positive share.
  The strongest basis being the collapse-persisting one fits this. A mundane-memory
  explanation, consistent, unclaimed.

Budget: 66 s spent, ~9.5 min remain (before the Bell run).
