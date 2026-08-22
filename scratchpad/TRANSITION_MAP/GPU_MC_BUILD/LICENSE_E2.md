# GPU annihilating coherent MC — E2 benchmark license

Parent prereg: `REG_HYDRO_COHERENT_ANNIHILATING_MC_PREREG.md` (`5f65a5b`)
Amendment: `EXECUTION_AMENDMENT_E2.md`, sha256 `51defb5c54ee2638df87e52b1440a0c5985f96ebe914cfb492e74a3b92731d9d`
(written and hashed BEFORE any run under it)
Configuration lists: `configs/MANIFEST.json`, sha256
`c44e455497c4cad492d56d150633aee36dfaea74aa81ed5d7f5e0bd1752039d9` (all six cells frozen,
zero duplicates, generated before the cascade)
Estimator: sha256(`regmodel.py` ‖ `mc_tables.py` ‖ `annihil_mc.py` ‖ `seeds_frozen.py`)
= `634cf7eff8e2cceb894c32e7a7a00cfca02159880abb2a0b7704383541076d26`

**Status: LICENSED BEFORE HELD-OUT TARGET EXECUTION.**

### Revision note (integrity chain)

This file was first written and hashed at
`1c345cffb59ab5688a09ce85b72ea4e922311035f5a95c945332f07e161136cd` **before any held-out cell
was executed**, already carrying the licensed population `W = 100,000` under RAW, decided by
the frozen rule from the completed W=10,000 (FAIL) and W=100,000 (PASS) benchmark runs.

It was edited afterwards, twice, and its hash therefore moved. Both edits are additive
reporting only and neither can move the selection:

1. the W=1,000,000 benchmark columns, which finished after the license was recorded — a larger
   candidate cannot displace the smallest passing one;
2. the independent dict-engine re-verification of the exact ground truth, and the
   pre-execution note on the selection rule.

**The estimator hash did not change**: `634cf7ef…` at license time and at the end of the
held-out run. The code that was licensed is the code that ran the targets.

## Licensed population

`W = 100,000 walkers per replica, with complex annihilation/resampling after every global
cycle, 8 independent replica-pair batches per configuration`

issued under the **RAW** witness convention — designated primary by the steward, recorded in
`EXECUTION_AMENDMENT_E2.md` ADDENDUM A1, which also carries the retraction of the earlier
weakly-favours-normalised reading. W=10,000 FAILS; W=100,000 PASSES; the prereg's rule selects
the smallest passing W, so no larger candidate can displace it.

NORMALISED is reported beside every number below, with its MID classification gate marked
**VACUOUS**. The finite-size verdict does not depend on the choice: `DENSITY-SCALING NOT
SUPPORTED` holds under both.

## THE CONVENTION IS RAW — and this reverses the earlier reading

`LICENSE_GPU.md` originally favoured the NORMALISED convention. That inference was drawn from
the **LOW** cell, which is "not low-memory" under **both** conventions and so never
discriminated. **MID** discriminates. Exact ground truth on the E2 configurations:

| cell | convention | exact median M | exact frac < 0.05 | exact classification |
|---|---|---:|---:|---|
| L=7 LOW N=20 | NORMALISED | 0.166625 | 0.0625 | not low-memory |
| L=7 LOW N=20 | **RAW** | **0.085881** | 0.1875 | not low-memory |
| L=7 MID N=25 | NORMALISED | 0.148188 | 0.1250 | **not low-memory** |
| L=7 MID N=25 | **RAW** | **0.031812** | **0.6250** | **LOW-MEMORY** |
| *recorded frozen LOW* | *primary* | *0.085881* | *0.3125* | *not low-memory* |
| *recorded frozen MID* | *primary* | *0.038276* | *0.6250* | *LOW-MEMORY* |

RAW reproduces the recorded classification in both cells and the recorded MID fraction
exactly; on LOW it returns 0.085881 against a recorded 0.085881, all six digits, on
independently drawn configurations. NORMALISED misses the MID classification outright. A
further 32 MID configurations from an unrelated seed give the same split (NORMALISED median
0.146 / frac 0.031, not low-memory; RAW median 0.0458 / frac 0.531, LOW-MEMORY), so it is
structural, not sampling noise.

**Under NORMALISED the frozen gate "MID remains low-memory" is unsatisfiable**: the exact
answer itself fails it, so no walker count can pass and a not-licensed verdict under
normalised would measure the convention rather than the estimator. Both conventions are
reported below; only RAW carries a live licensing decision.

There is also a mechanical reason RAW is better behaved. The normalised witness divides by the
origin-pair support, which on MID falls as low as 0.064. At W=10,000 the normalised error and
the support are rank-correlated at −0.41 (raw: −0.13), and the worst normalised configuration
returns |error| = 1.20 with SE 0.41 where its raw error is 0.056.

## Gate table — all 32 benchmark configurations, gates verbatim

### RAW (the licensed convention)

| gate | limit | W=10,000 | W=100,000 | W=1,000,000 |
|---|---:|---:|---:|---:|
| median abs error | ≤ 0.010 | 0.00344 pass | **0.00127 pass** | 0.00029 pass |
| p90 abs error | ≤ 0.020 | 0.02283 **FAIL** | **0.00406 pass** | 0.00082 pass |
| max abs error | ≤ 0.050 | 0.14271 **FAIL** | **0.01005 pass** | 0.00204 pass |
| median MC SE | ≤ 0.010 | 0.00486 pass | **0.00167 pass** | 0.00049 pass |
| p90 MC SE | ≤ 0.020 | 0.01143 pass | **0.00269 pass** | 0.00101 pass |
| max MC SE | ≤ 0.050 | 0.02185 pass | **0.00321 pass** | 0.00145 pass |
| out-of-range fraction | ≤ 0.05 | 0.00260 pass | **0.00000 pass** | 0.00000 pass |
| LOW remains not low-memory | — | pass | **pass** | pass |
| MID remains low-memory | — | **FAIL** | **pass** | pass |
| **verdict** | | **FAIL** | **PASS ← licensed** | **PASS** |

W=1,000,000 also passes, and passes by a further factor of ~4, but the frozen rule selects the
smallest passing candidate, so **W=100,000 is the licensed population**.

### NORMALISED (reported beside RAW; MID gate VACUOUS, no live decision)

**VACUOUS** means the gate cannot be satisfied under this convention at any walker count,
because the *exact* answer fails it. Its failure carries no information about the estimator.

| gate | limit | W=10,000 | W=100,000 | W=1,000,000 |
|---|---:|---:|---:|---:|
| median abs error | ≤ 0.010 | 0.00859 pass | 0.00258 pass | 0.00067 pass |
| p90 abs error | ≤ 0.020 | 0.07155 FAIL | 0.01202 pass | 0.00214 pass |
| max abs error | ≤ 0.050 | 1.20112 FAIL | 0.03812 pass | 0.00742 pass |
| median MC SE | ≤ 0.010 | 0.01091 FAIL | 0.00349 pass | 0.00112 pass |
| p90 MC SE | ≤ 0.020 | 0.03966 FAIL | 0.00803 pass | 0.00193 pass |
| max MC SE | ≤ 0.050 | 0.40871 FAIL | 0.01703 pass | 0.00371 pass |
| out-of-range fraction | ≤ 0.05 | 0.01302 pass | 0.00000 pass | 0.00000 pass |
| LOW remains not low-memory | — | pass | pass | pass |
| MID remains low-memory | — | **VACUOUS** | **VACUOUS** | **VACUOUS** |
| **verdict** | | **FAIL** | **FAIL — VACUOUS** | **FAIL — VACUOUS** |

At W=1,000,000 under NORMALISED **every numerical gate passes** — median error 0.00067, max
error 0.00742, max SE 0.00371 — and the MID classification gate still fails. That is the
cleanest possible demonstration that the gate is testing the convention rather than the
estimator: a hundred-fold increase in walkers cannot move it, because the exact answer is on
the wrong side of the threshold.

## Why W=10,000 fails, and it is not a coding defect

The witness is a sum of absolute values of noisy quantities, so each batch estimate is biased
upward by Jensen's inequality, and the bias is worst where the true M is near zero — which is
precisely the low-memory regime the MID gate tests. Under RAW the MID median inflates from an
exact 0.031812 to 0.052422 at W=10,000, crossing the 0.05 threshold and flipping the
classification; at W=100,000 it returns to 0.032264 and the classification is recovered. The
reported SE does not capture this bias, because it measures the spread of the batch estimates
rather than their common offset. The 100,000-walker population is what makes the frozen
classification gate meaningful.

Per-cell classification recovery under RAW:

| cell | exact | W=10,000 | W=100,000 |
|---|---|---|---|
| LOW median M | 0.085881 (not low-mem) | 0.089154 (not low-mem) | 0.087148 (not low-mem) |
| MID median M | 0.031812 (LOW-MEMORY) | 0.052422 (not low-mem ✗) | 0.032264 (LOW-MEMORY ✓) |

## Exact ground truth

Computed by a third independent exact implementation (`exact_gpu.py`), array-based, validated
against the dict engine to 1.9e-16 on many-body configurations on both backends and against
the published L=11 N=2 bridge. 16/16 configurations exact in both cells; norms unity to 1e-12;
heaviest configuration reached 10,411,983 basis configurations. No configuration exceeded the
cap, so no benchmark configuration was excluded.

The ground truth the license actually rests on was then re-derived by the **independent dict
engine** on every configuration light enough for it:

- L=7 LOW: **16/16** reproduced, worst difference 2.8e-16 (`M_norm`) and 1.7e-16 (`M_raw`).
- L=7 MID: **12/16** reproduced, worst difference 1.2e-14 and 3.9e-15. The four unchecked are
  the heavy configurations (0, 6, 8, 9; 0.9–10.4 million basis states), beyond the dict
  engine's reach.

So the MID classification that decides the convention rests on twelve independently
double-computed values plus four computed once, by an engine validated to 1e-16 elsewhere.

## Noted BEFORE the held-out cells were run: the selection rule optimises the wrong thing

The frozen rule licenses the **smallest** W that passes the benchmark. The benchmark cells are
L=7 LOW and MID; the targets include L=9 MID and HIGH, which are very much harder. The rule
therefore sets the walker count by benchmark economy and gives the targets whatever power
happens to be left over.

Measured before any held-out execution (`l9_probe.log`, one replica per cell, no witness
read): the distinct configurations occupied by 10⁶ walkers after the final resample are 253 at
L=7 N=20, 18,460 at L=9 N=32, and 746,772 at L=9 N=52. Annihilation can only cancel walkers
that meet on the same configuration, so its power is walkers-per-configuration: ~4,000 at L=7
LOW, ~1.3 at L=9 HIGH. **At the licensed W=100,000 that ratio at L=9 HIGH is of order 0.1** —
fewer walkers than occupied configurations — so essentially nothing annihilates there and the
estimator degenerates toward the independent-path estimator that already went
variance-uncontrolled in exactly that cell.

I therefore expect L=9 HIGH to fail readability at the licensed W, and record that expectation
here, before looking. The frozen prereg forbids raising W after target inspection, and that
rule is honoured: whatever the cell returns is reported as
`TARGET-STATISTICALLY-UNCONTROLLED` rather than rescued.

## What this licenses, and the debt

This licenses **this implementation against exact ground truth on these cells at W=100,000**.
It is **not** concordance with the primary workstream's CPU license: those 32 configurations
and their exact M values remain unavailable, and running against them **remains OWED**. Any
discrepancy reopens this license.

All raw per-batch `q_coh`/`q_deph` vectors are stored in `mc_<cell>_W<W>.json`, so the license
re-issues under either convention without re-running anything.

**No held-out target cell was executed or inspected before this license was recorded.**
