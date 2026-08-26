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
