# SAWTOOTH FORWARD RESULTS — the ceiling step is the cause, proved by planting it

**Prereg:** `SAWTOOTH_FORWARD_PREREG.md`, commit `022096e`, frozen before any forward datum
existed. **Adjudicator:** `sawtooth_adjudicate.py`, mechanical application of §6.
**Verdict in one line: every clause decided so far is met — the mechanism is confirmed by forward
prediction of a *manipulated* cause (30 of 30 planted readings in band) — and the height law's
scale constant is NOT universal, which a control I added found and my own prereg's gate missed.
Two of the nine natural readings (k = 34, 35) are still computing, so the campaign verdict is
CONFIRMED-PENDING, not CONFIRMED.**

---

## 1. SCORECARD

| clause | what was staked | result |
|---|---|---|
| **P-PLANT** k = 24, 26, 28, 30 | a planted ln2 ceiling step gives a tooth of 5.9–12.0 pp | **CONFIRMED 4/4**, in band **6/6** at every k |
| **P-PLANT** k = 28, high-weight code | same, different column rule | **CONFIRMED**, in band 6/6 |
| **P-LINEAR** k = 28 | a 2·ln2 step gives **twice** the ln2 tooth | **CONFIRMED** — ratio **1.9847** (1.9714–1.9948) vs 2.000, and in band 6/6 |
| **column-rule control** (added by me, not staked) | — | **FIRED**: a degenerate code gives 0.26× the predicted tooth |
| **P-AFTER** k = 33 | tooth = −T(32)/3 + g, g ∈ [−0.6, +1.1] | **CONFIRMED**, in band **6/6** |
| **P-ABSENT** k = 33 | no positive tooth above +1.1 pp | **not falsified** (0/6) |
| **P-AFTER / P-ABSENT** k = 34, 35 | same | **PENDING** — still running (§5) |
| arm A at k ≥ 32 (the brief's k = 36, 40) | — | **UNTESTABLE ON THIS BOX**, established in prereg §1 |

**P-PLANT confirmed at 4 of 4 planted k (prereg required ≥ 3 of 4); P-LINEAR confirmed; P-AFTER
confirmed and P-ABSENT not falsified at the one natural k so far returned.** Counting readings
rather than clauses: **30 of 30 planted readings** (5 planted steps × 6 conditions) landed inside
bands staked before any of them existed, and **6 of 6** natural k = 33 readings did. Two natural
k remain (34, 35), and per §6 the campaign verdict requires P-ABSENT to survive at all three.

---

## 2. P-PLANT — THE CAUSE WAS PUT WHERE NATURE DOES NOT PUT IT, AND THE EFFECT FOLLOWED

Arm B's ceiling does not move at k = 24, 26, 28, 30. Running the same linear family at
m = 6 instead of the minimal m = 5 plants a ceiling step of exactly ln 2 there — the *same* drop
as the natural k = 32 step, so the height prediction extrapolates in nothing.

tooth (pp), predicted band from `sawtooth_stake.json` (committed `022096e`), against the
**measured natural tooth at the identical k**:

| k | cond | tooth | staked band | ×resolution | natural tooth, same k |
|---|---|---|---|---|---|
| 24 | 0.01/10% | **9.999** | [7.97, 11.96] ✓ | 43 | +0.560 |
| 24 | 0.01/50% | **8.666** | [6.93, 10.40] ✓ | 46 | +0.423 |
| 24 | 0.01/1nat | **8.932** | [6.99, 10.48] ✓ | 85 | +0.327 |
| 24 | 0.05/10% | **8.503** | [6.83, 10.24] ✓ | 39 | +0.503 |
| 24 | 0.05/50% | **7.443** | [5.94, 8.90] ✓ | 48 | +0.367 |
| 24 | 0.05/1nat | **7.473** | [5.82, 8.73] ✓ | 87 | +0.270 |
| 26 | 0.01/10% | **9.138** | [7.36, 11.04] ✓ | 38 | +0.336 |
| 26 | 0.01/50% | **7.901** | [6.37, 9.55] ✓ | 44 | +0.263 |
| 26 | 0.01/1nat | **8.280** | [6.56, 9.83] ✓ | 58 | +0.161 |
| 26 | 0.05/10% | **7.786** | [6.30, 9.45] ✓ | 36 | +0.311 |
| 26 | 0.05/50% | **6.827** | [5.48, 8.23] ✓ | 44 | +0.221 |
| 26 | 0.05/1nat | **6.956** | [5.48, 8.22] ✓ | 58 | +0.140 |
| 28 | 0.01/10% | **8.475** | [6.83, 10.25] ✓ | 65 | +0.263 |
| 28 | 0.01/50% | **7.297** | [5.88, 8.82] ✓ | 69 | +0.204 |
| 28 | 0.01/1nat | **7.773** | [6.18, 9.27] ✓ | 135 | +0.130 |
| 28 | 0.05/10% | **7.233** | [5.85, 8.77] ✓ | 59 | +0.244 |
| 28 | 0.05/50% | **6.341** | [5.10, 7.65] ✓ | 73 | +0.172 |
| 28 | 0.05/1nat | **6.550** | [5.19, 7.78] ✓ | 126 | +0.117 |
| 30 | 0.01/10% | **7.938** | [6.37, 9.56] ✓ | 71 | +0.217 |
| 30 | 0.01/50% | **6.798** | [5.46, 8.19] ✓ | 77 | +0.167 |
| 30 | 0.01/1nat | **7.353** | [5.86, 8.79] ✓ | 131 | +0.114 |
| 30 | 0.05/10% | **6.784** | [5.46, 8.18] ✓ | 65 | +0.202 |
| 30 | 0.05/50% | **5.939** | [4.76, 7.14] ✓ | 80 | +0.142 |
| 30 | 0.05/1nat | **6.208** | [4.94, 7.41] ✓ | 121 | +0.105 |

**24 of 24 readings inside their pre-registered bands.** The manipulation moves the statistic to
**15×–60×** its unmanipulated value at the same k, and every tooth clears its own baseline
resolution (ddof = 1) by 36×–135×.

The point-prediction error is far smaller than the ±20% band: across the 24 readings the mean
absolute error is **0.77%**, the worst **2.75%**, and the signed mean **+0.12%** — essentially
unbiased. The law `tooth = C(k)·Δln(ns)/k`, with C interpolated from arm B's own k = 16 and
k = 32 and nothing else, predicts the planted teeth to about one part in a hundred. Per-k mean
absolute error: 1.00% (k = 24), 0.92% (26), 0.76% (28), 0.41% (30).

**The elementary picture, at k = 24, ε = 0.01, 10%** (hand-checked from raw JSON, independent of
the adjudicator): on the natural m = 5 ladder rent/nat falls monotonically, 0.132305 → 0.127983 →
0.124110 → 0.120620 → 0.117617, so L(24) = **−0.0252**. Plant the ln2 step and rent/nat at the
*same k* is 0.129259 instead — L(24) = **+0.0692**. The step does not bend the curve, it reverses
it, and the reversal is the tooth.

---

## 3. P-LINEAR — HEIGHT IS LINEAR IN THE SIZE OF THE CEILING DROP

At k = 28 with the high-weight column rule (d_min = 11, non-degenerate), planting one ln2 step and
two ln2 steps:

| cond | n = 1 tooth | band | n = 2 tooth | band | ratio |
|---|---|---|---|---|---|
| 0.01/10% | 8.277 | [6.83, 10.25] ✓ | 16.438 | [13.66, 20.49] ✓ | 1.9860 |
| 0.01/50% | 7.211 | [5.88, 8.82] ✓ | 14.367 | [11.76, 17.64] ✓ | 1.9922 |
| 0.01/1nat | 7.593 | [6.18, 9.27] ✓ | 15.146 | [12.37, 18.55] ✓ | 1.9948 |
| 0.05/10% | 7.074 | [5.85, 8.77] ✓ | 13.945 | [11.70, 17.54] ✓ | 1.9714 |
| 0.05/50% | 6.240 | [5.10, 7.65] ✓ | 12.373 | [10.19, 15.29] ✓ | 1.9829 |
| 0.05/1nat | 6.409 | [5.19, 7.78] ✓ | 12.695 | [10.38, 15.57] ✓ | 1.9807 |

**Ratio 1.9847, range [1.9714, 1.9948], against a staked 2.000 — confirmed, and about 0.8% low.**
Both rows are in band 6/6. Doubling the ceiling drop doubles the tooth.

---

## 4. THE CONTROL THAT FIRED — C IS NOT UNIVERSAL, AND MY PREREG'S GATE DID NOT CATCH IT

I added a column-rule control that the prereg did not stake: the same k = 28, the same m = 6, the
same ln 2 ceiling drop, the same baseline ladder — only the choice of which columns of F_2^m to
use is different. It **fired**.

| column rule | code d_min | dual d | tooth, 0.01/10% | implied C | vs calibration C(32) = 3.4481 |
|---|---|---|---|---|---|
| canonical (arm B's own rule) | 12 | 4 | 8.475 | 3.4235 | −0.7% |
| high-weight | 11 | 4 | 8.277 | 3.3435 | −3.0% |
| **systematic [I \| P]** | **1** | 3 | **2.253** | **0.9101** | **−74%** |

**Diagnosis.** The systematic code is *degenerate*: it contains a weight-1 codeword, so one slot
alone carries a whole dimension of the code. `armB_columns`' **exhaustive** branch selects on
`(dual distance, then minimum distance)` — `design_check.py:169` — which would reject it outright;
its **canonical** branch, the one that actually applies at these k, is a fixed list that is not
selected on d_min but happens to achieve d_min = 8..13. So the protection against degeneracy is
explicit in one branch and incidental in the other. My planted-code gate (prereg §7.4) required
only pair-uniformity, `d ≥ 3` — which the degenerate code passes. **That is a gap in my own
pre-registered gate, found by a control I added after staking, and it is reported here rather
than repaired retroactively in the prereg.**

**What this costs the claim, stated plainly.** The height law as staked —
`tooth = C(k)·Δln(ns)/k` with C a function of k and condition only — is **refuted in its
universality**. C depends on the substrate's minimum distance, and by a factor of 3.8 between
d_min = 1 and d_min ≈ 12. The law holds, and holds to ~2%, across every *non-degenerate* code
tested (canonical d_min = 8..13, high-weight d_min = 11, and the seven natural steps of both arms);
it fails badly on a degenerate one.

**What this does not cost.** Two things survive the degenerate case intact:
1. the **sign and existence** of the tooth — the degenerate plant still gives a positive tooth in
   6/6, clearing resolution 15×–29×; planting the step still causes a tooth;
2. **linearity** — the degenerate family's ratio is **1.9484** (range 1.9359–1.9655), still within
   3.3% of 2.000. So the step-*size* law is robust where the scale constant is not.

**The gate that should have been there**, and which any future planted run must carry:
`d_min ≥ 2` at minimum, and to reproduce these C values, a code chosen by arm B's own criterion
(maximise dual distance, then minimum distance). Recorded as a standing amendment.

---

## 5. P-AFTER / P-ABSENT — k = 33 CONFIRMED, k = 34 AND 35 STILL RUNNING

Arm B's ceiling is flat across k = 32..63 (m = 6 throughout), so k = 33 is pure aftermath of the
k = 32 step. Measured (`sawtooth_B33.json`, 40.7 min):

| cond | tooth | staked band | in band |
|---|---|---|---|
| 0.01/10% | −2.506 | [−3.09, −1.39] | ✓ |
| 0.01/50% | −2.153 | [−2.72, −1.02] | ✓ |
| 0.01/1nat | −2.403 | [−2.92, −1.22] | ✓ |
| 0.05/10% | −2.120 | [−2.73, −1.03] | ✓ |
| 0.05/50% | −1.888 | [−2.46, −0.76] | ✓ |
| 0.05/1nat | −2.015 | [−2.57, −0.87] | ✓ |

**P-AFTER CONFIRMED, 6/6 in band. P-ABSENT not falsified — 0/6 above +1.1 pp**; every reading is
negative, as ceiling-tracking requires where the ceiling does not move.

*One honest note on the resolution here.* The baseline sd at k = 33 is large (3.20–4.28 pp)
because the window L(30), L(31), L(32) **contains the k = 32 step**, which is precisely the
contamination the after-step rule predicts. So the k = 33 teeth do **not** clear 10× their own
baseline sd, and the prereg deliberately did not ask them to — P-AFTER is adjudicated against an
empirical band built from 90 measured after-step residuals (prereg §2.2), not against that
inflated sd. The resolution-clearance requirement applies to P-PLANT, where the window is clean,
and there it is met by 36×–135×.

k = 34 and k = 35 are still running (projected ~3.0 h and ~7.0 h; `sawtooth_natural.log`). The
adjudicator scores them automatically as the files land. **Per prereg §6 the campaign verdict
requires P-ABSENT not to be falsified at any of the three k, so the verdict stands as
CONFIRMED-PENDING-k=34,35** — every clause decided so far is met, and two readings remain.

k = 36 was dropped in the prereg with its reason (bands overlap there once C is derived correctly;
16 h and 11.8 GB for an ambiguous answer). That decision stands and is not revisited by these
results.

k = 36 was dropped in the prereg with its reason (bands overlap there once C is derived correctly;
16 h and 11.8 GB for an ambiguous answer). That decision stands and is not revisited by these
results.

---

## 6. WHAT THE BRIEF ASKED FOR, AND WHAT WAS DELIVERED INSTEAD

The brief asked for teeth at k = 36 and 40 with absences between. Prereg §0–§1 established that
this is the **arm A** prediction while the confirmed k = 32 tooth is **arm B**, and that arm A at
k ≥ 32 is unreachable on this box (34.4 GB for one buffer). The brief's three clauses map onto
what was actually done as follows:

A fact the prereg understated, re-derived here: **the brief's k = 36 cannot even be built.**
`N0(36) = 40`, and order-40 Hadamard is not wired by any of the three constructions in
`rent_islands_design_check` — 39 is not prime (no Paley-I), 19 ≡ 3 (mod 4) (no Paley-II), 40 is
not a power of two (no Sylvester). `DC.hadamard(40)` raises `no construction wired for order 40`;
the same holds for k = 37, 38, 39. So k = 36 is unreachable for **two independent reasons** —
no construction *and* the 2^k memory wall — and k = 40 (N₀ = 44, Paley-I q = 43, which does build)
is blocked by memory alone at 2^40 states. The prereg cited only the memory wall.

- **Tooth locations.** Not tested forward at k = 36/40 — impossible. Tested forward instead by
  *planting* locations: 5 planted steps, all confirmed. Additionally, the location claim was found
  **already confirmed retrospectively at seven natural steps** in committed data (prereg §2) —
  which is why the planted design, not another natural k, was the informative experiment left.
- **Tooth absences.** Partly running (§5). Note the brief's expectation that absences would
  discriminate a "trend-fitting artifact" is weaker than hoped: the mod-4 rival and ceiling-tracking
  predict the *same* thing at k = 33, 34, 35, so those k test smoothness, not the mechanism. The
  planted arm carries the discriminating power.
- **Tooth heights.** The brief's ratio-conservation (0.47–0.63 of the ceiling drop) is wrong: the
  tooth scales as 1/k, so a conserved ratio over-predicts k = 36 by about six-fold. The corrected
  law was derived from seven natural steps and then **confirmed forward to 2%** on five planted
  ones — with the universality caveat of §4.

**Numbers taken from the brief and not re-derived: none are used.** The brief's Δln N0 values
(11.778 / 10.536 / 9.531 pp) were re-derived and are correct for arm A; its ratio band and its
implied k = 36/40 tooth heights were re-derived and are not.

---

## 7. GATES

| gate | status |
|---|---|
| Catastrophic cancellation | `neg_mass = 0.00e+00` on **every** row of every forward run; no negative kernel entries |
| Zero-cell roundoff | parent's `ceiling` column unused; `ceiling_share` returns `share_max` closed-form |
| Target residual < 1e-6 | max observed 3.25e-13; **zero rows dropped** |
| Pair-uniformity (Q2-G4) | `pair_dev = 0.0`, `share_max_dev = 0.0`, `d ≥ 3` on all 13 substrates; all PASS |
| **Minimum distance** | **gap found — see §4.** Not gated in prereg; d_min recorded per code from here on |
| Instrument agreement | runner reproduces committed `rent_scaling_q2_B25.json` to 9 decimal places on all 6 conditions |
| Floors matched to sample | resolution = ddof = 1 sd of the *three* baseline L values, per condition, never pooled |
| Search caps | none — every column rule is a closed-form deterministic list; no search, so no cap can saturate |
| Named denominators | "6/6" = the six conditions; "4/4" = the four canonical planted k; ratios name ddof |
| Baseline instrument purity | m = 5 ladder k = 20..24 recomputed on this instrument; each planted family adjudicated against its **own-rule** ladder |

**One correction to a sibling's file, carried from prereg §3:** `RENT_SCALING_Q2_ADJUDICATION.md`
quotes baseline sd with ddof = 0. Its "65×–145×" clearance is 53×–118× on the ddof = 1 convention
used here. No verdict in that file changes.

---

## 8. FILES

Prereg `SAWTOOTH_FORWARD_PREREG.md` @ `022096e` · calibration `sawtooth_calib.py`,
`sawtooth_bands.py` · staked bands `sawtooth_stake.py` → `sawtooth_stake.json` · runner
`sawtooth_forward.py` · adjudicator `sawtooth_adjudicate.py` → `sawtooth_verdicts.json` ·
data `sawtooth_{B20..B24,B2*sys,B2*hw,P24m6,P26m6,P28m6,P28m6sys,P28m7sys,P28m6hw,P28m7hw,P30m6}.json` ·
logs `sawtooth_{planted,sysbase,hwbase,natural}.log`.
