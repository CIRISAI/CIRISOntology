# STAGE-2 FREEZE — field mapping, counts, and the blindness ledger

*2026-08-26. Pins mappings and counts only; no stake, band, or kill moves (stage-1 §4).*

## E0a/E0b/E0c status

- **E0a PASS** — md5 `4e90d7c3...` verified on the 8.43 GB archive.
- **E0b PASS** — extracted, 30 GB, 183 files (`p7zip` no-sudo route).
- **E0c** — structure inventoried. **One blindness breach, recorded:** the `.txt`
  files are data columns, not codebooks, and a `cat` intended for a codebook displayed
  part of `SuccessBasic.txt` — the Basic protocol's MARGINAL per-trajectory success
  column (mostly 1s, some 0s). What this reveals: the Basic success rate, which the
  PAPER already reports (protocol level was never blind). What stays blind: every
  trajectory value, every work value, and every JOINT witness↔outcome relation —
  which is where all four stakes live. Verdict: stakes unaffected; procedure
  corrected — no `cat` on `.txt`/`.dat` under the data tree; npy headers only.

## The inventory (headers only)

| unit | files | shape | role |
|---|---|---|---|
| Single Erasure / {Basic, Enhanced, Optimized-Single-Etot, Optimized-Multiple} / {to0, to1} | `Success_*` | (N,) bool | **survival — E3 target** |
| ″ | `W_*` | (N,) float64 | **work — E4 target** |
| ″ | `z0_*`, `z1_*` | (N, 10000) float64 | per-trajectory traces — the witness source |
| Chained Erasure / 4 protocols | `z*, z0*, z1*` | (174–…, 370000) | 100-erasure chains — E5 (T_eff companion) |

Basic single-erasure counts: N(to0)=4588, N(to1)=4223. Other protocols pinned the
same way (headers) at unblind time and recorded in the results file.

## Pins

- **f₀ = 1090 Hz, Q = 7** (paper) → **τ_R = Q/(π f₀) = 2.044 ms** — E2's reference,
  frozen. The E0d dev gauge at exactly these values measured the τ_c ruler reading
  **2.45 × τ_R on known truth**; E2 is adjudicated as staked and reported through
  that calibration, both pre-declared.
- **THE ONE OPEN PIN: which of z0/z1 is position x(t), and the sample rate / segment
  boundaries** (erasure window vs quiescent window inside the 10000 samples).
  Resolution procedure, frozen: read the paper PDF shipped in the archive and the
  authors' GitHub code — codebooks, never array values. If the codebooks do not
  settle it, the pre-committed fallback: the array whose per-trajectory FINAL-sample
  sign agrees with `Success` semantics (to0 ⇒ x<0) is position — a structure-level
  consistency check using only the sign of one sample per trajectory, declared here
  before use.
- Estimator, unchanged: the battery pipeline; fibers = within-well position rank ×
  velocity rank (velocity = backward difference at the pinned fs); floors from E0d
  proper, rerun at the pinned fs on matched synthetic Langevin before unblinding.

## Order of operations from here

1. E0d proper (pinned f₀, Q, fs) → floors + ruler calibration at the real sampling.
2. Unblind per stake, Bonferroni 0.05/4: E1, E2 (quiescent windows), E3 (end-of-
   protocol witness → Success), E4 (initial |v| quartile → W, per protocol).
3. One results file, every branch of the tree reported, τ_c with both readings.

## STAGE-2b — final pins from the codebook, committed before the unblind script runs

- **fs_raw = 10000/(2t₀) = 5.45 MHz**; trajectory = samples 0–4999 protocol period,
  5000–9999 assessment period (paper: t_f = 2t₀, "one period protocol, one period
  assessment"; Δt ≈ 0.2 µs confirms).
- **Analysis rate: ×100 downsample → fs_a ≈ 54.5 kHz** (the regime where the chain is
  validated; single-sample differencing at 5.45 MHz on nm-scale interferometry is
  noise-amplified). Velocity = backward difference at fs_a, as frozen. Pre-declared
  robustness: repeat the headline cells at ×50 and ×200.
- **POSABILITY CONSEQUENCE, stated before unblinding:** the assessment window
  (0.917 ms) is 0.45 τ_R, so E2's contraction time cannot complete inside it. If the
  defect has not contracted by the window's end, E2 is **VOID-not-killed** with the
  lower bound τ_c > 0.9 ms reported against τ_R = 2.044 ms and the 2.45× ruler
  calibration. The chained streams are protocol-driven (E2′ imprint branch), not
  quiescent, and cannot substitute.
- **Position-array pin runs the frozen fallback**: final-sample sign agreement with
  `Success` semantics, one sample per trajectory, both arrays, numbers recorded. The
  non-position array is NOT used; velocity comes from differencing position (the
  validated chain, unchanged).
- **E3 operationalization**: witness at analysis-sample 50 (start of assessment):
  in-target bit + position rank (8) × velocity rank (5), bins from a 60 % trajectory
  train split; predict `Success` on the held-out 40 %; baseline = bit alone.
  Component split: position-only vs velocity-only fibers. PRIMARY = pooled across the
  8 protocol×target cells; per-cell reported. 1000 within-bit permutations; CIs at
  98.75 % (Bonferroni 0.05/4).
- **E4 operationalization**: |v| at the first defined analysis sample of the protocol
  period; quartiles per protocol×target over all trajectories; "monotone" = Q4−Q1
  mean-work difference > 0 with 98.75 % bootstrap CI excluding 0, all four quartile
  means reported. Stake passes at ≥3 of 4 protocols; kill at 0.
