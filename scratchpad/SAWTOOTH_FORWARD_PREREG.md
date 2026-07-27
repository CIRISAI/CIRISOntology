# SAWTOOTH FORWARD PREREG — the ceiling-tracking mechanism, staked before the data exist

**Frozen 2026-07-27. No k > 32 datum, and no planted-step datum of any k, exists at the time
of this commit.** The calibration below uses only rows already on disk (`rent_islands_results.json`,
k = 5..24, committed 2026-07-25; `rent_scaling_q2_{A,B}*.json`, k = 25..32, commit `44329f5`).
The predictions in §4 and §5 are staked against runs that have not been started.

---

## 0. PROVENANCE, AND A CORRECTION TO THE BRIEF — READ FIRST

The task brief asked for teeth at **k = 36 and k = 40**, on the grounds that the minimum
orthogonal-array size `N0(k) = 4·ceil((k+1)/4)` steps at k ≡ 0 (mod 4). That formula is real and
it is in the instrument — `rent_islands_design_check.N0`, line 97 — **but it governs ARM A, and
the confirmed k = 32 tooth is in ARM B.** The two arms have different ceilings:

| | substrate | run size `ns` | steps at | source |
|---|---|---|---|---|
| **ARM A** | minimum-size strength-2 OA | `N0(k) = 4·ceil((k+1)/4)` | k ≡ 0 (mod 4): 12, 16, 20, 24, 28, **32, 36, 40** | `rent_scaling_q2.py:600` |
| **ARM B** | minimal linear code | `2^ceil(log2(k+1))` | k = 2^j: 8, 16, **32**, 64 | `rent_scaling_q2.py:609`, `design_check.armB_columns:159` |

`RENT_SCALING_Q2_ADJUDICATION.md`'s table is arm B ("quotient-lean route"), and `B32.json`
records `ns = 64, m = 6` — the linear step 32 → 64, not the OA step 32 → 36. Both arms happen to
step at k = 32, which is why k = 32 was decisive; they diverge immediately afterwards.

**Consequence, stated as loudly as a confirmation would be: on arm B the ceiling-tracking
mechanism predicts NO tooth at k = 36 or k = 40 — its next ceiling step is k = 64.** The brief's
prediction is the arm-A prediction. It is not wrong about arm A; it is being asked of the wrong
arm. §4 therefore stakes what arm B's own ceiling actually implies, and §5 adds the presence
test the brief wanted, by a route the brief did not consider.

**Numbers I took from the brief rather than re-deriving are marked `[LEAD]` and are not used.**
The brief's ratio "0.47–0.63" divides arm B's measured tooth by arm A's ceiling drop and mixes
the arms; §3 derives the ratio from each arm's own ceiling. The brief's `11.778 / 10.536 / 9.531 pp`
are correct values of `Δln N0` at k = 32/36/40 (re-derived here) but they are arm A's drops.

---

## 1. FEASIBILITY, HONESTLY — WHAT CANNOT BE RUN AT ALL

**Arm A is impossible at k ≥ 32 on this box, and this was already declared.** For k = 32..40,
`N0(k)` ∈ {36, 40, 44} is not a power of two, so `build_one` falls to the `LeanFull` route
(`rent_scaling_q2.py:605-607`), which holds one or two `float64` buffers of size `2^k`
(`LeanFull._buffers`, line 392) plus a `2^k` popcount index. At k = 32 that is **34.4 GB for a
single buffer** on a 31 GB box, and it doubles per k. `RENT_SCALING_PREREG.md` §1.4 already set
the campaign ceiling at k = 31 for exactly this reason ("the 2^k barrier at the next non-linear
Hadamard order"). **The brief's k = 36 and k = 40 arm-A teeth are not expensive — they are
unreachable, and no amount of scheduling changes that.**

**Arm B's next natural ceiling step is k = 64**, needing a `2^58` dual buffer. Unreachable forever.

Arm B's cost is set by `r = k − m`; measured on this instrument (`secs` field, arm B):
r = 20..26 → 11.1, 25.8, 66.7, 137.0, 345.3, 940.0, 1795.1 s, and k = 32 (r = 26) → 2070.7 s.
The geometric ratio per unit r is **2.32**. Extrapolating from k = 32:

| k | r | projected time | persistent memory (`dual_w` i8 + buffer f64 + `leader_w` i16 = 11 B/elt) |
|---|---|---|---|
| 33 | 27 | ~1.3 h | 1.5 GB |
| 34 | 28 | ~3.0 h | 3.0 GB |
| 35 | 29 | ~7.0 h | 5.9 GB |
| 36 | 30 | ~16 h | 11.8 GB + BFS `np.unique` transients |

**What I am running: k = 33, 34, 35 (≈ 11.4 h total, ≤ 5.9 GB).**
**What I am dropping, and why: k = 36.** Not merely the 16 h and the 11.8 GB against a shared box
already at load 13.4 with Planck, rent-results and water-mw resident — the decisive reason is
that **k = 36 barely discriminates the two hypotheses once the height law is derived correctly**
(§3). Ceiling-tracking predicts a clean-window tooth in [0, +0.92] pp there; the mod-4 rival,
evaluated with the *same* height law on its *own* ceiling drop ln(40/36) = 10.536 pp, predicts
+0.75 to +1.01 pp. **Those bands overlap.** Sixteen hours buys an ambiguous answer. The brief's
"5.0–6.6 pp at k = 36" figure comes from conserving a ratio that mixes the arms; it is not what
the mechanism predicts for arm B, nor for arm A once C is measured. §5 buys a *decisive* presence
test for about seven minutes of compute instead.

---

## 2. CALIBRATION — ON DATA THAT ALREADY EXISTS (this is calibration, NOT confirmation)

`sawtooth_calib.py` applies the P-STEP32 tooth statistic at **every** k in both arms, k = 5..32.
Result, and it must be reported before anything else because it changes what is left to discover:

**The mechanism's LOCATION claim is already confirmed, retrospectively, at seven steps.**
Arm A shows a positive tooth in 6/6 conditions at k = 12, 16, 20, 24, 28 — every k ≡ 0 (mod 4),
and nowhere else. Arm B shows one at k = 16 and k = 32 — every k = 2^j, and nowhere else.
At non-step k the tooth is small and, wherever the 3-window is clean, of the opposite character.

**This is retrodiction and is counted as nothing.** It was found by me, after the fact, on
committed data, and it does not enter the confirmation count. It does two legitimate jobs: it
fixes the height law below, and it shows the k = 32 forward confirmation was a recurrence of an
already-present pattern rather than an isolated event — which *lowers* the evidential weight of
`RENT_SCALING_Q2_ADJUDICATION.md`'s "third advance prediction" and should be said plainly.

### 2.1 The height law

`C(k) ≡ tooth(k) · k / Δln(ns)(k)`, tooth and Δln in pp. Measured at all seven natural steps:

| arm | k | Δln ns | 0.01/10% | 0.01/50% | 0.01/1nat | 0.05/10% | 0.05/50% | 0.05/1nat |
|---|---|---|---|---|---|---|---|---|
| A | 12 | 28.768 | 3.5140 | 3.3500 | 2.4094 | 3.1173 | 2.6225 | 1.6705 |
| A | 16 | 22.314 | 3.5784 | 3.2705 | 2.6220 | 3.1469 | 2.6785 | 2.1046 |
| A | 20 | 18.232 | 3.6220 | 3.2262 | 2.8622 | 3.1637 | 2.7137 | 2.3952 |
| A | 24 | 15.415 | 3.6524 | 3.1993 | 3.0535 | 3.1800 | 2.7363 | 2.5945 |
| A | 28 | 13.353 | 3.6767 | 3.1796 | 3.2010 | 3.1965 | 2.7507 | 2.7369 |
| B | 16 | 69.315 | 3.4537 | 3.0638 | 2.8315 | 2.9597 | 2.5602 | 2.3138 |
| B | 32 | 69.315 | 3.4481 | 2.9378 | 3.2187 | 2.9507 | 2.5782 | 2.7225 |

C is stable across arms, across k, and across a 5× range of ceiling-drop size. **The tooth is
proportional to the ceiling drop and inversely proportional to k** — the brief's assumption that
the *ratio to the drop* is conserved is wrong by a factor of k, and that is why its k = 36 band
(5.0–6.6 pp) is about six times too large.

Interpolation error, validated within arm A (interpolate C between k = 16 and 28, test at 20, 24):
**max 3.33%, rms 1.41%**. Cross-arm difference at fixed k = 16: **≤ 9.9%**. The ±20% band staked
below therefore covers both, with margin.

### 2.2 The after-step rule (an arithmetic consequence, staked so it can fail)

The trailing 3-window means the three k *after* a step carry that step in their baseline. With
`ln rent(k) = f(k) + Σ s_j·1[k ≥ k_j]`, f smooth: at a step tooth = g + s; at step+1,2,3
tooth = g − s/3; elsewhere tooth = g, where g is the smooth curvature term. Measured residual
`g = tooth(k*+j) + T(k*)/3` over all 90 available (arm, step, j, condition) cells with k > 12
(k ≤ 12 excluded: the rent table is controller-confounded there by up to 18%):

**g ∈ [−0.503, +1.005] pp, mean +0.353, sd 0.291.** Staked band: **g ∈ [−0.6, +1.1] pp.**

Clean-window teeth (no step at k, none in the window), arm B k = 20..31: all in
**[+0.098, +0.923] pp, strictly decreasing in k.**

---

## 3. THE INSTRUMENT AND THE STATISTIC (unchanged from P-STEP32)

`L(k) = ln(rent/nat)(k) − ln(rent/nat)(k−1)`; `tooth(k) = L(k) − mean(L(k−3), L(k−2), L(k−1))`;
reported in percentage points. Six conditions, ε ∈ {0.01, 0.05} × target ∈ {10%, 50%, 1 nat},
identical to P-STEP32 so the comparison is like-for-like. Resolution floor = **sample** sd
(ddof = 1) of the three baseline L values.

> *Marked for the W2 gate:* `RENT_SCALING_Q2_ADJUDICATION.md` quotes the baseline sd with
> **ddof = 0** (its 0.085 / 0.063 / 0.048 / 0.078 / 0.055 / 0.044 pp equal my ddof = 1 values
> × √(2/3)). I use ddof = 1 throughout, which is the more conservative floor. No conclusion in
> that file changes; the "65×–145×" clearance becomes 53×–118×.

All rent values come from `rent_scaling_q2.py` only. Baseline points at m = 5, k = 20..24 are
**recomputed** on this instrument rather than taken from the parent, so no forward tooth mixes
two instruments (gate Q2-G1 pins them equal to 1e-10; this removes the question entirely).

---

## 4. FORWARD PREDICTION I — THE NATURAL LADDER, ARM B k = 33, 34, 35

Arm B's ceiling is **flat** across k = 32..63 (m = 6 throughout). Ceiling-tracking therefore
predicts these three k are pure aftermath of the k = 32 step:

**P-AFTER.** For k = 33, 34, 35 and each condition, `tooth(k) ∈ [−T(32)/3 − 0.6, −T(32)/3 + 1.1]` pp:

| k | 0.01/10% | 0.01/50% | 0.01/1nat | 0.05/10% | 0.05/50% | 0.05/1nat |
|---|---|---|---|---|---|---|
| 33 | [−3.09, −1.39] | [−2.72, −1.02] | [−2.92, −1.22] | [−2.73, −1.03] | [−2.46, −0.76] | [−2.57, −0.87] |
| 34 | [−3.09, −1.39] | [−2.72, −1.02] | [−2.92, −1.22] | [−2.73, −1.03] | [−2.46, −0.76] | [−2.57, −0.87] |
| 35 | [−3.09, −1.39] | [−2.72, −1.02] | [−2.92, −1.22] | [−2.73, −1.03] | [−2.46, −0.76] | [−2.57, −0.87] |

**P-ABSENT.** No k in {33, 34, 35} shows a **positive** tooth exceeding **+1.1 pp** (the top of the
clean-window range, +0.923, rounded up). A positive tooth above that at any of these k falsifies
ceiling-tracking on arm B, because arm B's ceiling provably does not move there.

*Honest statement of what this does and does not discriminate:* P-AFTER and P-ABSENT do **not**
separate ceiling-tracking from the mod-4 rival — the rival also has no step at 33, 34, 35. They
test that the curve is smooth and that the k = 32 step is a genuine one-off displacement rather
than the statistic manufacturing excursions. The mechanism test is §5.

---

## 5. FORWARD PREDICTION II — THE PLANTED STEP (the presence test the brief wanted)

The mechanism says the tooth is *caused* by a jump in the run size at fixed k. That is
manipulable: run the arm-B linear family with a **deliberately non-minimal** m, planting a
ceiling step of exactly `ln 2` (or `2 ln 2`) at a k where arm B has **no** natural step. The
planted drop at one step is **identical to the k = 32 drop**, so the height prediction involves
no extrapolation in drop size. It is also *cheaper* than the natural ladder (r = k − m falls).

Ladder: m = 5 for k = 20..k*−1, then m = 5+n at k*. Baseline window L(k*−3..k*−1) is clean m = 5.

**P-PLANT.** `tooth(k*) ∈ C_interp(k*)·n·ln2·100/k* × [0.8, 1.2]` pp, C interpolated in k between
arm B's own k = 16 and k = 32 (so k* = 24..30 is **interpolation, not extrapolation**):

| k* | steps n | 0.01/10% | 0.01/50% | 0.01/1nat | 0.05/10% | 0.05/50% | 0.05/1nat |
|---|---|---|---|---|---|---|---|
| 24 | 1 | 9.97 [7.97, 11.96] | 8.67 [6.93, 10.40] | 8.74 [6.99, 10.48] | 8.54 [6.83, 10.24] | 7.42 [5.94, 8.90] | 7.27 [5.82, 8.73] |
| 26 | 1 | 9.20 [7.36, 11.04] | 7.96 [6.37, 9.55] | 8.19 [6.56, 9.83] | 7.88 [6.30, 9.45] | 6.86 [5.48, 8.23] | 6.85 [5.48, 8.22] |
| 28 | 1 | 8.54 [6.83, 10.25] | 7.35 [5.88, 8.82] | 7.73 [6.18, 9.27] | 7.31 [5.85, 8.77] | 6.37 [5.10, 7.65] | 6.49 [5.19, 7.78] |
| 30 | 1 | 7.97 [6.37, 9.56] | 6.82 [5.46, 8.19] | 7.32 [5.86, 8.79] | 6.82 [5.46, 8.18] | 5.95 [4.76, 7.14] | 6.17 [4.94, 7.41] |
| 28 | **2** | 17.08 [13.66, 20.49] | 14.70 [11.76, 17.64] | 15.46 [12.37, 18.55] | 14.62 [11.70, 17.54] | 12.74 [10.19, 15.29] | 12.97 [10.38, 15.57] |

**The null is already measured.** At these same k with no planted step, arm B's tooth is
+0.560 / +0.336 / +0.263 / +0.217 pp (10%, ε = 0.01) and smaller elsewhere — the whole measured
set spans **[+0.105, +0.560] pp**, against predictions of 6–17 pp. The predicted effect is
**15× to 40× the natural value at the identical k**, and 50–150× the baseline resolution sd
(0.051–0.235 pp).

**P-LINEAR.** The n = 2 row at k = 28 tests the height law's linearity in the drop: it predicts
**twice** the n = 1 tooth at the same k. "One step is one fixed jump regardless of size" predicts
the n = 1 value; "height ∝ Δln ns" predicts the n = 2 band. These are disjoint.

---

## 6. ADJUDICATION — PINNED NOW

Per prediction, over the six conditions:

- **P-PLANT (per k\*, and P-LINEAR):** CONFIRMED iff the tooth is positive in **6/6** and inside
  its band in **≥ 5/6**, and every tooth clears **10×** its own baseline sd.
  *Locations right, quantitative form wrong* iff positive in 6/6 and clearing 10× resolution, but
  inside band in ≤ 4/6 — report the measured C and the direction of the miss.
  **FALSIFIED** iff the tooth fails to reach **+2.0 pp** in ≥ 2/6 conditions (that is ~4× the
  largest natural non-step tooth ever measured, +0.560, and ~20× the resolution): planting the
  cause did not produce the effect.
- **P-AFTER:** CONFIRMED iff inside band in ≥ 5/6 at each of k = 33, 34, 35.
- **P-ABSENT:** FALSIFIED iff any of k = 33, 34, 35 shows a tooth > +1.1 pp in ≥ 2/6 conditions.

**Campaign verdict.** The mechanism is **CONFIRMED by forward prediction** only if P-PLANT is
confirmed at **≥ 3 of the 4** planted k *and* P-LINEAR is confirmed *and* P-ABSENT is not
falsified. Anything less is reported as partial, with the failing clause named in the title line.

### Outcome meanings, fixed in advance

- **(a) P-PLANT + P-LINEAR + P-ABSENT all confirmed** → ceiling-tracking is confirmed by *forward
  prediction of a manipulated cause*, which is stronger than the location-matching the brief
  asked for: the step was put where nature does not put it, and the tooth followed, at the
  predicted height and with the predicted linearity. This is a genuine advance confirmation and
  may be counted as the programme's fourth.
- **(b) P-PLANT confirmed in sign and resolution but outside band** → the *cause* is right and the
  *height law* `C·Δln ns/k` is wrong. Report the measured C per condition and per k, and say the
  law is refuted in its quantitative form. Not a confirmation.
- **(c) P-PLANT falsified — a planted ln2 step produces no tooth** → the mechanism is FALSIFIED.
  The k = 32 tooth would then be a property of k = 32 or of the particular [32,6] code, not of the
  ceiling stepping, and the retrospective mod-4/2^j location match of §2 would need a different
  explanation. **This is to be reported as loudly as a confirmation, in the title line.**
- **(d) P-ABSENT falsified — a positive tooth at k = 33, 34 or 35** → the mechanism is FALSIFIED on
  arm B: a tooth appeared where the ceiling provably does not move. The k = 32 confirmation must
  then be re-read as a possible coincidence of the fit window, and `RENT_SCALING_Q2_ADJUDICATION.md`
  amended to say so.
- **(e) P-LINEAR fails alone (n = 2 gives the n = 1 tooth)** → the ceiling *step* is the cause but
  its *size* is not the driver; the law becomes "a tooth per step, height set by k alone".

**Arm A at k ≥ 32 is not adjudicated by this campaign and cannot be** (§1). The brief's k = 36 and
k = 40 predictions are therefore recorded as **UNTESTABLE ON THIS BOX**, not as open questions
awaiting effort. The retrospective arm-A confirmation at k = 12..28 (§2) is the only arm-A
evidence there is or will be here.

---

## 7. GATES CARRIED

1. **Catastrophic cancellation.** Kernel outputs checked for negative entries; `neg_mass` and
   `mass_dev` are recorded per row and any row with `neg_mass > 0` is reported, not silently used.
2. **Zero-cell roundoff.** The parent's `ceiling` column is unreliable below ~1e-9 and is not
   used; `ceiling_share` returns `share_max` in closed form for both routes.
3. **Target residual.** Rows with `target_resid_rel > 1e-6` are DROPPED, not adjusted (instrument
   default); a dropped row makes its condition unavailable rather than approximate.
4. **Pair-uniformity.** Every planted substrate must have dual distance `d ≥ 3` and
   `share_max = k·ln2 − ln|S|` exactly (gate Q2-G4). A planted code failing this is discarded
   before any rent is read, and the discard reported.
5. **Floors matched to sample size.** Resolution is the ddof = 1 sd of the *three* baseline L
   values actually used, per condition, never pooled.
6. **Search caps.** None: `armB_columns` is exhaustive only when C(2^m−1, k) ≤ 20000 and canonical
   otherwise; every planted code here is in the canonical branch, so no search is involved and no
   cap can saturate. The column list is recorded per run.
7. **Named denominators.** "6/6" is over the six conditions; "≥ 3 of 4" is over the four planted
   k. Ratios to resolution name the ddof.
8. **W2 / received numbers.** Every number taken from a sibling rather than re-derived is marked
   `[LEAD]` (§0) or flagged in §3 (the ddof discrepancy). All C values, all teeth, all bands and
   all timings in this file are computed by `sawtooth_calib.py` / `sawtooth_bands.py` /
   `sawtooth_stake.py` from JSON on disk.

## 8. FILES

`sawtooth_calib.py` (tooth at every k, both arms) · `sawtooth_bands.py` (height law, after-step
band) · `sawtooth_stake.py` → `sawtooth_stake.json` (the staked table above) ·
`sawtooth_forward.py` (the runner, planted + natural) · results → `SAWTOOTH_FORWARD_RESULTS.md`.
