# Held-out target cells — E2 result

Prereg: `REG_HYDRO_COHERENT_ANNIHILATING_MC_PREREG.md` (`5f65a5b`)
Amendment: `EXECUTION_AMENDMENT_E2.md`, sha256 `51defb5c…`
License: `LICENSE_E2.md` — **W = 100,000, RAW convention** — recorded at sha256 `1c345cff…`
before any held-out cell was executed; see its revision note for the additive edits made
afterwards, none of which can move the selection
Configurations: `configs/MANIFEST.json`, sha256 `c44e4554…`, generated before the licensing
cascade from the prereg's frozen held-out seeds under the interpretation declared in E2 D1

**RAW is the primary convention**, designated by the steward and recorded in
`EXECUTION_AMENDMENT_E2.md` ADDENDUM A1. NORMALISED is reported beside every number below. The
benchmark's MID classification gate is VACUOUS under NORMALISED; that gate does not appear
among the held-out readability criteria, so nothing here is marked vacuous — but note that
NORMALISED additionally loses the L=7 HIGH cell to a single low-support configuration, where
RAW reads it comfortably.

## VERDICT

**DENSITY-SCALING NOT SUPPORTED**, and the failure is not a compute limit.

| leg | required | measured (RAW, W=100,000) | |
|---|---|---|---|
| L=7 LOW not low-memory | yes | median M 0.085881, 18.75 % below 0.05 → not low-memory | **holds** |
| L=7 HIGH low-memory | yes | median M 0.045752, 56.25 % below 0.05 → LOW-MEMORY, READABLE | **holds** |
| L=9 LOW not low-memory | yes | median M 0.025655, 75.00 % below 0.05 → **LOW-MEMORY**, READABLE | **FAILS** |
| L=9 HIGH low-memory | yes | `TARGET-STATISTICALLY-UNCONTROLLED` | **not established** |
| L=9 MID | diagnostic only | `TARGET-STATISTICALLY-UNCONTROLLED` | — |

The L=7 pair behaves exactly as the density-scaling picture predicts: LOW keeps route memory,
HIGH loses it. **At L=9 the pattern breaks.** The L=9 LOW cell — which the picture requires to
retain memory — has already lost it, and it says so on a **fully readable** cell: SE median
0.00154, p90 0.00313, max 0.00336 against gates of 0.015/0.030/0.050, no out-of-range
estimates, no non-finite batches. This is a controlled negative, not a missing measurement.

L=9 HIGH is separately uncontrolled, so even the surviving leg is unestablished at L=9. Under
the frozen text this is `NOT SUPPORTED` rather than `REFUTED`, because `REFUTED` requires both
sizes readable and L=9 HIGH is not.

**W was not changed after target inspection.** L=9 HIGH is reported as what it is.

## Readability, both conventions, at the licensed W = 100,000

| cell | conv | median M | frac < 0.05 | class | SE med / p90 / max | out-of-range | verdict |
|---|---|---:|---:|---|---|---:|---|
| L=7 HIGH N=31 | **RAW** | 0.045752 | 0.5625 | LOW-MEMORY | 0.00221 / 0.01198 / 0.01986 | 0.0013 | **READABLE** |
| L=7 HIGH N=31 | norm | 0.212695 | 0.1250 | not low-mem | 0.01087 / 0.03873 / **2.38025** | 0.0052 | UNCONTROLLED |
| L=9 LOW N=32 | **RAW** | 0.025655 | 0.7500 | LOW-MEMORY | 0.00154 / 0.00313 / 0.00336 | 0.0000 | **READABLE** |
| L=9 LOW N=32 | norm | 0.111003 | 0.1250 | not low-mem | 0.00450 / 0.00885 / 0.01735 | 0.0000 | READABLE |
| L=9 MID N=42 | **RAW** | 0.063464 | 0.3750 | not low-mem | 0.00878 / 0.04648 / 0.05542 | 0.0169 | UNCONTROLLED |
| L=9 MID N=42 | norm | 0.233490 | 0.0625 | not low-mem | non-finite | 0.0603 | UNCONTROLLED |
| L=9 HIGH N=52 | **RAW** | 0.052067 | 0.5000 | not low-mem | 0.02177 / 0.25041 / 0.57363 | 0.0065 | UNCONTROLLED |
| L=9 HIGH N=52 | norm | non-finite | 0.1250 | — | non-finite | 0.0122 | UNCONTROLLED |

Both conventions give `DENSITY-SCALING NOT SUPPORTED`; the verdict does not depend on the
convention choice. NORMALISED is additionally far less usable — it loses L=7 HIGH to a single
configuration whose tiny origin-pair support drives M to 2.68 with SE 2.38, where the same
configuration's raw reading is 0.084967 ± 0.019860.

## L=9 HIGH failed exactly as predicted, before it was run

`LICENSE_E2.md` recorded, before execution, that L=9 HIGH was expected to fail readability at
the licensed W, because annihilation power is set by walkers-per-configuration and that ratio
collapses with cell density: ~4,000 at L=7 LOW, ~1.3 at L=9 HIGH at W=10⁶, hence ~0.1 at
W=10⁵. It failed: median SE 0.02177 against a 0.015 gate, p90 0.25041 against 0.030, max
0.57363 against 0.050, with non-finite batches from replicas sharing no configuration.

This is the same wall the path-MC estimator hit in the same cell. The annihilating
representation does not remove it; it moves it. Annihilation only helps where walkers meet,
and in the densest cell they do not meet.

## The frozen selection rule is the reason, and it is a design defect

The prereg licenses the **smallest** W passing a benchmark made of L=7 LOW and MID — the two
easiest cells in the study — then spends that W on targets up to L=9 HIGH. W=100,000 is ample
for the benchmark (max error 0.01005 against a 0.050 gate) and inadequate for L=9 HIGH by more
than an order of magnitude. W=1,000,000 also passed the benchmark and would have given L=9
HIGH roughly ten times the walker density, but the frozen rule forbids choosing it, and the
prereg equally forbids raising W once a target has been seen. Both rules were honoured.

A successor prereg should select W against the **hardest** target cell, or license a W per
cell fixed in advance from a cost model like `l9_probe.py`.

## Bias diagnostic — why the recorded path-MC L=9 LOW reading deserves re-examination

The recorded path-MC target result classifies L=9 LOW as **READABLE, NOT LOW-MEMORY** with
median M = 0.050501 and fraction M<0.05 = 0.500 — a hair above the 0.05 threshold, at
W=10,000.

This programme has now measured, against exact ground truth, that the frozen witness is biased
**upward** at small W, because M sums absolute values of noisy quantities and the bias is worst
where the true M is near zero. On the MID benchmark cell, where exact truth is known:

| | exact | W=10,000 | W=100,000 |
|---|---:|---:|---:|
| MID median M (RAW) | 0.031812 | **0.052422** | 0.032264 |
| MID classification | LOW-MEMORY | **not low-memory** | LOW-MEMORY |

An inflation of +0.020 at W=10,000 carried the median across exactly the 0.05 threshold and
flipped the classification. The recorded L=9 LOW median of 0.050501 sits 0.0005 above that same
threshold, measured at that same W.

So I ran my own held-out cells at the **smaller** W=10,000 as a bias diagnostic. This raises no
W after inspection and does not touch the frozen classification, which stands at the licensed
W=100,000. The result:

| cell | convention | W=10,000 | W=100,000 (licensed) |
|---|---|---|---|
| **L=9 LOW N=32** | **RAW** | **0.055073 → not low-memory** | **0.025655 → LOW-MEMORY** |
| L=9 LOW N=32 | norm | 0.157208 → not low-memory | 0.111003 → not low-memory |
| **L=7 HIGH N=31** | **RAW** | **0.067513 → not low-memory** | **0.045752 → LOW-MEMORY** |
| L=7 HIGH N=31 | norm | 0.328860 → not low-memory | 0.212695 → not low-memory |

At W=10,000 my L=9 LOW cell reads **0.055073** and classifies as not low-memory. The recorded
path-MC L=9 LOW reads **0.050501** and classifies as not low-memory, at the same W. Two
independent estimators on two independent configuration lists land within 0.005 of each other,
both a whisker above the threshold. Raising W tenfold more than halves my median and flips the
classification.

L=7 HIGH shows the same flip, so the effect is not peculiar to one cell: at W=10,000 this
estimator systematically reports median M inflated by an amount — here +0.022 to +0.030 —
that is comparable to the 0.05 classification threshold itself.

**This does not settle the primary's number**, which was computed on different configurations
with a different estimator, and I cannot rerun their list. But every classification in the
recorded path-MC target result was made at W=10,000, and the leg that kept density-scaling
alive — L=9 LOW being "not low-memory" — is the reading most exposed to this bias, sitting
0.0005 above the threshold. The test is cheap and decisive: **re-run the primary's L=9 LOW
list at W ≥ 100,000.** If its median falls below 0.05, that leg is lost on their data as it is
on mine.

## Per-configuration tables

Every value below is at W = 100,000. Raw per-batch `q_coh`/`q_deph` vectors for all of them
are stored in `mc_<cell>_W100000.json`, so either convention re-derives without re-running.

### L=7 HIGH N=31

| cfg | M (raw) | SE (raw) | M (normalised) | SE (norm) | non-finite batches |
|---:|---:|---:|---:|---:|---:|
| 0 | 0.051655 | 0.001468 | 0.209847 | 0.003814 | 0 |
| 1 | 0.049591 | 0.002177 | 0.320463 | 0.011238 | 0 |
| 2 | 0.019006 | 0.002019 | 0.084699 | 0.014211 | 0 |
| 3 | 0.016120 | 0.002252 | 0.033594 | 0.003848 | 0 |
| 4 | 0.219415 | 0.011589 | 0.267646 | 0.017982 | 0 |
| 5 | 0.014826 | 0.000619 | 0.084907 | 0.003176 | 0 |
| 6 | 0.007159 | 0.000572 | 0.053809 | 0.002925 | 0 |
| 7 | 0.051181 | 0.001614 | 0.322393 | 0.010507 | 0 |
| 8 | 0.017716 | 0.002340 | 0.042421 | 0.011299 | 0 |
| 9 | 0.084967 | 0.019860 | 2.680783 | 2.380251 | 0 |
| 10 | 0.118507 | 0.005083 | 0.215544 | 0.009531 | 0 |
| 11 | 0.165095 | 0.005145 | 0.218358 | 0.007038 | 0 |
| 12 | 0.016214 | 0.000851 | 0.310674 | 0.013612 | 0 |
| 13 | 0.062011 | 0.012367 | 0.148258 | 0.032900 | 0 |
| 14 | 0.012395 | 0.001735 | 0.254228 | 0.044558 | 0 |
| 15 | 0.041913 | 0.002372 | 0.208974 | 0.008905 | 0 |

**RAW** — median M = 0.045752, fraction M<0.05 = 0.5625 → **LOW-MEMORY**  
SE median 0.00221 (≤0.015), p90 0.01198 (≤0.030), max 0.01986 (≤0.050), out-of-range 0.0013 (≤0.05) → **READABLE**

**NORMALISED** — median M = 0.212695, fraction M<0.05 = 0.1250 → **not low-memory**  
SE median 0.01087 (≤0.015), p90 0.03873 (≤0.030), max 2.38025 (≤0.050), out-of-range 0.0052 (≤0.05) → **TARGET-STATISTICALLY-UNCONTROLLED** (failed: p90_se, max_se)

### L=9 LOW N=32

| cfg | M (raw) | SE (raw) | M (normalised) | SE (norm) | non-finite batches |
|---:|---:|---:|---:|---:|---:|
| 0 | 0.187236 | 0.002836 | 0.253610 | 0.002227 | 0 |
| 1 | 0.001523 | 0.000328 | 0.013935 | 0.001728 | 0 |
| 2 | 0.023276 | 0.003360 | 0.074177 | 0.010642 | 0 |
| 3 | 0.008027 | 0.000488 | 0.027888 | 0.001802 | 0 |
| 4 | 0.042173 | 0.001441 | 0.108345 | 0.003819 | 0 |
| 5 | 0.043713 | 0.001841 | 0.146762 | 0.004595 | 0 |
| 6 | 0.013673 | 0.000673 | 0.151697 | 0.006887 | 0 |
| 7 | 0.033788 | 0.002189 | 0.050222 | 0.003467 | 0 |
| 8 | 0.014300 | 0.001255 | 0.080978 | 0.004413 | 0 |
| 9 | 0.128696 | 0.001531 | 0.208020 | 0.002379 | 0 |
| 10 | 0.006101 | 0.000486 | 0.081958 | 0.006802 | 0 |
| 11 | 0.023577 | 0.000572 | 0.296079 | 0.005947 | 0 |
| 12 | 0.027734 | 0.003139 | 0.065747 | 0.007060 | 0 |
| 13 | 0.016728 | 0.001561 | 0.173124 | 0.017354 | 0 |
| 14 | 0.115342 | 0.001541 | 0.378123 | 0.004936 | 0 |
| 15 | 0.076621 | 0.003115 | 0.113660 | 0.002997 | 0 |

**RAW** — median M = 0.025655, fraction M<0.05 = 0.7500 → **LOW-MEMORY**  
SE median 0.00154 (≤0.015), p90 0.00313 (≤0.030), max 0.00336 (≤0.050), out-of-range 0.0000 (≤0.05) → **READABLE**

**NORMALISED** — median M = 0.111003, fraction M<0.05 = 0.1250 → **not low-memory**  
SE median 0.00450 (≤0.015), p90 0.00885 (≤0.030), max 0.01735 (≤0.050), out-of-range 0.0000 (≤0.05) → **READABLE**

### L=9 MID N=42

| cfg | M (raw) | SE (raw) | M (normalised) | SE (norm) | non-finite batches |
|---:|---:|---:|---:|---:|---:|
| 0 | 0.069749 | 0.006842 | 0.115592 | 0.011225 | 0 |
| 1 | 0.255394 | 0.051574 | 0.512196 | 0.077547 | 1 |
| 2 | 0.226447 | 0.055423 | 0.410507 | 0.211823 | 0 |
| 3 | 0.043927 | 0.007420 | 0.061049 | 0.010558 | 0 |
| 4 | 0.043677 | 0.008832 | 2.078601 | 0.972963 | 0 |
| 5 | 0.180819 | 0.041394 | 0.587810 | 0.099617 | 0 |
| 6 | 0.148467 | 0.015852 | 0.190564 | 0.023286 | 0 |
| 7 | 0.034083 | 0.002437 | 0.184496 | 0.012711 | 0 |
| 8 | 0.113685 | 0.024131 | 0.425568 | 0.092973 | 0 |
| 9 | 0.061385 | 0.005606 | 0.222943 | 0.023086 | 0 |
| 10 | 0.060988 | 0.008719 | 0.065069 | 0.008828 | 0 |
| 11 | 0.006357 | 0.000924 | 0.039798 | 0.004501 | 0 |
| 12 | 0.065543 | 0.006942 | 0.101998 | 0.020979 | 0 |
| 13 | 0.067747 | 0.025501 | 1.680852 | nan | 7 |
| 14 | 0.038845 | 0.021058 | 0.888036 | nan | 7 |
| 15 | 0.038382 | 0.004931 | 0.244036 | 0.027856 | 0 |

**RAW** — median M = 0.063464, fraction M<0.05 = 0.3750 → **not low-memory**  
SE median 0.00878 (≤0.015), p90 0.04648 (≤0.030), max 0.05542 (≤0.050), out-of-range 0.0169 (≤0.05) → **TARGET-STATISTICALLY-UNCONTROLLED** (failed: p90_se, max_se)

**NORMALISED** — median M = 0.233490, fraction M<0.05 = 0.0625 → **not low-memory**  
SE median nan (≤0.015), p90 nan (≤0.030), max nan (≤0.050), out-of-range 0.0603 (≤0.05) → **TARGET-STATISTICALLY-UNCONTROLLED** (failed: med_se, p90_se, max_se, oor, all finite)

### L=9 HIGH N=52

| cfg | M (raw) | SE (raw) | M (normalised) | SE (norm) | non-finite batches |
|---:|---:|---:|---:|---:|---:|
| 0 | 0.035919 | 0.005540 | 0.211580 | 0.030813 | 0 |
| 1 | 0.000000 | 0.000000 | nan | nan | 8 |
| 2 | 0.026116 | 0.004395 | 0.668874 | 0.139723 | 2 |
| 3 | 0.102621 | 0.036468 | nan | nan | 8 |
| 4 | 0.012613 | 0.007069 | 1.000000 | nan | 7 |
| 5 | 0.000000 | 0.000000 | nan | nan | 8 |
| 6 | 0.000000 | 0.000000 | nan | nan | 8 |
| 7 | 0.612748 | 0.390458 | 0.464866 | 0.164946 | 3 |
| 8 | 0.573626 | 0.573626 | nan | nan | 8 |
| 9 | 0.027746 | 0.004099 | 1.366636 | 0.618456 | 0 |
| 10 | 0.174392 | 0.110365 | 0.000000 | nan | 7 |
| 11 | 0.068215 | 0.060014 | nan | nan | 8 |
| 12 | 0.000000 | 0.000000 | nan | nan | 8 |
| 13 | 0.192152 | 0.103612 | 0.000000 | nan | 7 |
| 14 | 0.085004 | 0.085004 | nan | nan | 8 |
| 15 | 0.215961 | 0.090979 | 0.833333 | nan | 7 |

**RAW** — median M = 0.052067, fraction M<0.05 = 0.5000 → **not low-memory**  
SE median 0.02177 (≤0.015), p90 0.25041 (≤0.030), max 0.57363 (≤0.050), out-of-range 0.0065 (≤0.05) → **TARGET-STATISTICALLY-UNCONTROLLED** (failed: med_se, p90_se, max_se)

**NORMALISED** — median M = nan, fraction M<0.05 = 0.1250 → **not low-memory**  
SE median nan (≤0.015), p90 nan (≤0.030), max nan (≤0.050), out-of-range 0.0122 (≤0.05) → **TARGET-STATISTICALLY-UNCONTROLLED** (failed: med_se, p90_se, max_se, all finite)

## Finite-size classification


**RAW (licensed convention)**

- L=7 LOW not low-memory (benchmark cell, exact): **True**
- L=7 HIGH low-memory: **True**
- L=9 LOW not low-memory: **False**
- L=9 HIGH low-memory: **False**
- all required cells readable: **False**

→ **DENSITY-SCALING NOT SUPPORTED**

**NORMALISED**

- L=7 LOW not low-memory (benchmark cell, exact): **True**
- L=7 HIGH low-memory: **False**
- L=9 LOW not low-memory: **True**
- L=9 HIGH low-memory: **False**
- all required cells readable: **False**

→ **DENSITY-SCALING NOT SUPPORTED**
