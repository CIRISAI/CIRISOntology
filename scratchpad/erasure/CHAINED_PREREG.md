# Pre-registration — the chained streams: three successors and a companion, one tree

**2026-08-26, frozen before any chained trajectory/work/temperature value is read**
(headers only so far; the paper's ensemble T and R figures are prior knowledge, so
ensemble-level curves are NOT blind — every stake below is chain-level or
instance-level, which the paper does not report). Fresh data: nothing from the
single-erasure unblind touched these files.

## Structure (headers)

Per protocol: `z*` (N_chains × 370000 at 2 MHz = 100 back-to-back 2t₀ erasures;
3700 raw / 37 analysis samples each, drive ends at analysis sample 18), `W` (N × 100
per-erasure work, kT), `T` (100, ensemble T_eff per index), `R` (100, ensemble
survival per index). N = 174 / 605–665 / 949 / 954. **The random target sequence is
NOT shipped**, so per-instance success is underivable — declared now, and no stake
uses it.

## The stakes

- **C1 (E1′ existence).** The within-erasure closure defect exists on chained streams:
  witness → next-bit gain above the C0-gauged floor at short lags inside assessment
  windows. *Kill:* nothing above floor.
- **C2 (E2′ slow mode — the two-component successor).** The witness at erasure k
  predicts the END-BIT of erasure k+m BEYOND the current bit (closure across the
  drive), and its decay in m gives the slow mode's timescale IN ERASURES. Staked
  direction: gain at m=1 above floor (the heterogeneity persists through a drive);
  decay over m reported. *Kill:* nothing at m=1 — the slow mode does not survive a
  drive, and the single-erasure flatness was within-window only.
- **C3 (E4′ — the derived magnitude law, the decisive one).** Per protocol, pooled
  over ~10⁵ instances: `Q4−Q1 of per-erasure W` **equals the initial-KE difference
  between quartiles**, in kT, ratio staked in **[0.5, 2]**. KE calibrated by
  equipartition (⟨½mv²⟩ = ½kT) on the single-erasure LATE window (4–5 ms; same
  instrument, units carry; declared). Predictions: ratio ∈ [0.5,2] in ≥2 of
  {Basic, Enhanced, OptSingle} — with the 20× statistics even Basic's 4 % effect
  resolves; **OptMulti ratio < 0.5** (the trained-robustness signature, staked as a
  PREDICTION this time). *Kill:* every protocol's ratio outside [0.5, 2].
- **C4 (E5 companion).** Per-chain witness content vs the ensemble T(k) heating curve
  and R(k); reported, no kill (no derivation).

## Tree

- **C0** gauge floors on synthetic chained-shape windows (matched f₀, Q, fs_a, 37-sample
  erasure segments); STOP if the planted effect does not transfer to 37-sample windows.
- **Calibration check:** equipartition computed on two disjoint halves of the late
  window must agree within 20 %; else C3 is **VOID (uncalibrated)** and the ratio is
  reported unitless.
- **C2 fails at m=1** → the slow mode is within-window only: report, and E2's
  two-component successor reverts to single-erasure diagnostics (labelled post-hoc).
- **C3 partial** (1 of 3 in band) → report per protocol; stake not passed; kill only at 0.
- **Posability screen (the E3′ fix, structural):** any survival-type cell needs ≥30
  outcome failures; none qualifies here (targets unshipped), which is why no survival
  stake appears.
- Cluster bootstrap over CHAINS everywhere (instances within a chain are dependent);
  CIs at 98.75 % (Bonferroni 0.05/4 across C1–C3 + the OptMulti sub-stake).

## No rescue beyond this tree.
