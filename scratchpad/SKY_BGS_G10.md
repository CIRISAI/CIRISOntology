# G10 — the mock closure. **One row of three FAILS**, and the floor dominates the other two.

The prereg calls G10 *"the gate that decides whether any of this is possible"* and predicts it is
*"the gate this measurement most plausibly fails."* It was run on all 25 AbacusSummit N-body
realizations at the one admissible cell, `R = 10, b = 4`. **Still blind — mocks only.**

---

## G10.1 What was run, and what was NOT

**Construction: `N_A`** — phase-randomise the gridded masked `δ` keeping `|F(k)|`, then
Poisson-resample at the field's own `n̄` through the identical selection. Both pieces imported
unchanged from the validated modules.

**`N_A` is NOT the null of record.** The prereg registers **`N_B`** for outcome (a), because `N_B`
is the construction that cut BOSS by 30–52 %. `N_B` requires new code (shot-noise power removed
in Fourier *before* phase randomisation; weighted `κ = ⟨w²⟩/⟨w⟩`) and **was not run**. So this
tests whether the floor model **transports between disjoint halves of the suite at all** — a
necessary condition for G10, not the whole of it.

> **A pass here is not a G10 pass. A fail here is a G10 fail.**

Split: 12 build / 13 held out. Signal := `mean(mock reading) − mean(mock floor)`, the gravitational
excess the N-body mocks carry, per configuration. The 10 % threshold is 10 % **of that**.

---

## G10.2 The verdict, per row

| config | mock reading | floor | **floor as % of reading** | signal | closure miss | **% of signal** | G10 |
|---|---|---|---|---|---|---|---|
| folded | 7.968e-4 | 2.937e-4 | **36.9 %** | 5.031e-4 | 3.20e-6 | **0.6 %** | **PASS** |
| equilateral | 2.241e-3 | 1.910e-3 | **85.2 %** | 3.313e-4 | 2.73e-5 | **8.2 %** | **PASS** |
| squeezed | 1.352e-3 | 1.327e-3 | **98.2 %** | 2.464e-5 | 9.60e-6 | **38.9 %** | **FAIL** |

**`squeezed` fails, by nearly 4×.** Per the prereg's own table, *G10 fails ⟹ **VOID*** — so the
squeezed configuration is **VOID** at this cell and cannot be reported as a measurement whatever
the data later says.

**And the two passes should not be read as comfort.** The floor is **85.2 %** of the equilateral
reading and **98.2 %** of the squeezed one. BOSS's warning was that the floor ran 100–130 % of
signal; on DESI BGS at `R = 10` the floor is 85–98 % of the **total reading**, which is the same
statement in a worse coordinate. `equilateral` passes at 8.2 % against a 10 % threshold — inside,
but with 1.8 points of margin on a quantity whose ensemble `σ` carries **±14.4 %** from suite size
alone (RULE S2-A). **That margin is smaller than its own error bar.**

Only `folded` is comfortable, and it is comfortable because its floor fraction is 37 % rather than
85 % — i.e. because it is the configuration the manufacturing channel reaches least.

---

## G10.3 The clipping, which points straight at the missing null

**Mean clipped fraction: 0.350.** BOSS measured 37 % clipping under `N_A` and **3.5 % under
`N_B`** — a 10× reduction, and the reason `N_B` is the null of record. Our 35 % reproduces the
BOSS defect almost exactly.

So the one row that failed, and the one that passed with no margin, both did so under the null
**known to be the weaker of the two, in the direction that matters**. On BOSS, moving `N_A → N_B`
*raised* the floor by 24–50 %. If that transfers, the equilateral row's 8.2 % miss does not
survive the change, and the campaign has no admissible configuration left.

**This is a prediction and it is cheap to test, which is exactly why it must be recorded now
rather than after:** run the `N_B` closure. If the equilateral miss exceeds 10 % under `N_B`, all
three rows are VOID at `R = 10`, and — with `R = 15` already dead on occupancy (Stage 1) — the
campaign has no admissible cell at all.

---

## G10.4 A defect in my own code, found and fixed, recorded rather than quietly patched

The first G10 run crashed: `lam < 0 or lam contains NaNs`. Diagnosis, not assumption — the
**interlaced CIC deposit returns negative cell values outside the footprint** (measured minimum
**−6.95** on this grid), a known property of the interlaced scheme. Using the raw deposit as a
Poisson rate is therefore invalid.

**The validated path never had this bug**, because `sky_stage2.CapGeometry` supplies a
*positivity-guarded* denominator — it is in the prereg's own reuse list, and I did not use it. I
reimplemented the resampling inline instead. §11 confines new code to I/O and the null
constructions for exactly this reason, and I widened that boundary without noticing.

Fixed by evaluating the rate **on the mask only**, where `density_and_mask` already guarantees
`exp > thr > 0`. **This is a real instance of the rule the prereg wrote to prevent it, and it is
recorded here rather than edited away.** Gate candidate, for GATES.md: *reused-pipeline guards do
not transfer to code that bypasses the pipeline — if you reimplement a step, you inherit none of
its validation, including the guards you did not know were there.*

---

## G10.5 Standing

| gate / rule | status |
|---|---|
| Stage 0 rules S0-A/B/C/D | applied |
| Stage 1 split-randoms null | occupancy fired at `R = 15`, every `b` |
| occupancy at `R = 10, b = 4` | **PASS** (263.3 vs floor 100) |
| G9 IPF certificate | **PASS** (worst 1.4e-12 vs < 1e-9) |
| RULE S2-A scatter | **FAIL** (5.66 / 3.35 / 3.22 % vs 3 %) — recomputed `n` = 25, the whole suite |
| RULE S2-B cross-suite `σ` | **NOT RUNNABLE** (EZmock models the other sample) |
| **G10 closure, `N_A`** | **folded PASS · equilateral PASS (8.2 % of 10 %) · squeezed FAIL → VOID** |
| **G10 closure, `N_B` (null of record)** | **NOT RUN — G10 is therefore INCOMPLETE** |

**The campaign is not cleared to proceed.** One row is void, one passes inside its own error bar,
and the null the prereg registered as decisive has not been run. Stage 3 is not entered.

**Next, and it is a single well-defined job:** implement `N_B` and re-run this closure. It decides
whether anything on DESI DR1 BGS is measurable at all — and either answer is a clean,
pre-registered ending.
