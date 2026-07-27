# EBOSS STAGE 1 — **COMPLETE, and the pre-registered occupancy gate FIRED.**

Committed at the stage boundary, alongside `EBOSS_AMENDMENT_1.md`, which records the design
consequence. **The eBOSS galaxy catalogue's order-3 statistic has not been read.**
`sky_realdata.measure_catalogue` still raises without `stage6_unblind=True`, and nothing in this
stage passes it.

Stage 1's job was pipeline adaptation and its validation. Both are done. It also produced the
first eBOSS reading of any kind — on the **split-randoms field**, which carries the survey
geometry and by construction no clustering — and that reading is what fires the gate.

---

## S1.1 What was built, and what was deliberately not

`eboss_stage1.py`. **New code is confined to eBOSS FITS I/O and the geometry constructor**, as
`EBOSS_PREREG.md` §11 committed. Imported unchanged: `SurveyGrid`, `sky_to_cart`, the interlaced
CIC deposit, `masked_smooth`, `quantile_labels`, `triple_hist`, `connected_info` (IPF + KL
certificate), `configs`, and `sky_stage2.CapGeometry.measure` in full — together with every
constant BOSS settled on: `CELL = 6.0`, `DEN_THR = 0.99`, `MASK_FRAC = 0.50`,
`MASK_SMOOTH = 8.0`.

**None of those constants was retuned for eBOSS**, and that is a decision, not an oversight: they
are what make the two surveys comparable, `DEN_THR = 0.99` was adopted because `0.5` inflated a
pure shot-noise null by 6.6×, and retuning them after seeing an occupancy failure is the move the
whole apparatus exists to prevent.

## S1.2 Pipeline validation

| check | result |
|---|---|
| **Gate A** (σ sanity, band `[0.02, 2.0]`; dye test on the withdrawn BOSS run read `[40.96, 1548.23]`) | **PASS** on all four samples: σ ∈ `[0.161, 0.560]` |
| **G9** IPF certificate `< 1e-9` | **PASS**, worst `2.76e-12` across all samples and rows |
| **G7** tied/railed fraction | recorded per row |
| **BOSS reproduction control** | `sky_stage6.DataGeometry` on BOSS SGC returns `n_indep = 13719.066868616923`, **bit-identical** to the campaign's committed `sky_stage6_data.json` |

**The last row is the load-bearing one.** It was run *before* the gate verdict was written down,
because the only question worth asking about an occupancy shortfall is whether it is geometry or
a bug, and the answer is geometry.

## S1.3 The geometry, measured

| sample | grid | cells | randoms | mask frac | `n_indep` R=15 | `n_indep` R=10 | build |
|---|---|---|---|---|---|---|---|
| **LRG NGC** | 360×720×288 | 74.6 M | 5 460 719 | 0.0952 | **17 359** | **68 134** | 59 s |
| **LRG SGC** | 225×576×300 | 38.9 M | 3 453 453 | 0.1154 | **9 574** | **39 127** | 23 s |
| **ELG NGC** | 250×288×180 | 13.0 M | 3 728 363 | 0.1194 | **3 781** | **15 006** | 19 s |
| **ELG SGC** | 250×600×96 | 14.4 M | 3 609 460 | 0.0941 | **1 986** | **9 516** | 21 s |
| *BOSS SGC (control)* | 270×450×270 | 32.8 M | 16 623 786 | 0.152 | *13 719* | *52 935* | 104 s |

ELG SGC's valid fraction at `R = 15` is **0.034 of the grid and 0.36 of its own mask** — the
equatorial strips are 4–10° thick and the `R = 15` kernel eats them from both sides. That is the
geometric fact behind the worst entry in the table.

## S1.4 THE GATE VERDICT

**Occupancy, measured** (`n_indep / b³`; G9 requires `> 100`):

| sample | R | b=4 | b=6 | rungs | two-rung clause |
|---|---|---|---|---|---|
| *BOSS NGC — the detection being confirmed* | 15 | *653* | *193* | *4, 6* | *met* |
| **LRG NGC** | **15** | **271** | **80** | 4 | **FAILS** |
| **LRG SGC** | **15** | **150** | **44** | 4 | **FAILS** |
| **ELG NGC** | **15** | **59** | **18** | none | **FAILS** |
| **ELG SGC** | **15** | **31** | **9** | none | **FAILS** |
| **ELG NGC** | **10** | **234** | **69** | 4 | **FAILS** |
| **ELG SGC** | **10** | **149** | **44** | 4 | **FAILS** |
| **LRG NGC** | 10 | 1064 | 315 | 4, 6 | **met** |
| **LRG SGC** | 10 | 611 | 181 | 4, 6 | **met** |

> **At `R = 15` — the primary scale, where BOSS's surviving 6.0 σ / 9.7 σ detection lives — no
> eBOSS sample fields two `b` rungs. Outcome (a) is unreachable at the primary scale on every
> eBOSS sample, independently of what the data reads.**
>
> **`EBOSS_PREREG.md` §5.3's secondary arm (ELG at `R = 10`, `b ∈ {4, 6}`) is dead as designed** —
> one rung in both caps.
>
> **The only surviving two-rung configuration in the survey is LRG at `R = 10`**, where Stage 0
> measured `n̄V_R = 1.18 / 1.16` and projected a floor of ~140 % of signal, *extrapolated beyond
> this campaign's own measured density grid*.

**Why the Stage-0 estimate said otherwise, and whose fault that is:** `EBOSS_STAGE0.md` §S0.4
estimated occupancy from the shell volume and defended it against `SKY_REALDATA_AMENDMENT_2`
§A2.2's `n_indep = 33 264`, which is a **superseded** BOSS figure — the campaign's own final
artifacts record 13 935 (mock) and 13 719 (data). **That is prerequisite P12, current-numbers
hygiene, violated by me one commit after registering it.** Full record, correction and the
measured-vs-estimated table: `EBOSS_AMENDMENT_1.md`.

## S1.5 The split-randoms floor — a model-free floor measurement, and it is large

The split-randoms field splits the random catalogue in half, treats one half as galaxies, and
**down-samples it to the survey's own galaxy count so the shot noise is right**. It carries the
window, the selection function and the shot noise, and **no clustering whatsoever**. Whatever
`I_C⁽³⁾` it reads is manufactured by the pipeline. It needs no mock and no model.

Folded configuration, occupancy-passing rows only, with the §4.5 ceiling fraction:

| sample | R | b | **floor `I`** | **% of `ln 2`** | mock 0001 `I` | mock − floor | **floor / mock** |
|---|---|---|---|---|---|---|---|
| **LRG NGC** | 15 | 4 | `2.676e-04` | **0.0386 %** | `7.633e-04` | `4.957e-04` | **35 %** |
| **LRG NGC** | 10 | 4 | `1.756e-03` | 0.2534 % | `2.649e-03` | `8.931e-04` | **66 %** |
| **LRG NGC** | 10 | 6 | `3.293e-03` | 0.4750 % | `5.456e-03` | `2.163e-03` | **60 %** |
| **LRG SGC** | 15 | 4 | `3.164e-04` | 0.0456 % | — | — | — |
| **LRG SGC** | 10 | 4 | `1.689e-03` | 0.2437 % | — | — | — |
| **LRG SGC** | 10 | 6 | `3.162e-03` | 0.4562 % | — | — | — |
| **ELG NGC** | 10 | 4 | `5.077e-04` | 0.0732 % | `9.280e-04` | `4.203e-04` | **55 %** |
| **ELG SGC** | 10 | 4 | `4.169e-04` | 0.0601 % | — | — | — |

**How to read the last column, and how not to.** `floor / mock` is the fraction of a mock
realisation's *total* `I_C⁽³⁾` that the pipeline manufactures from geometry and shot noise alone.
It is **not** the campaign's valve floor and **not** `TARGET`: the pre-registered nulls `N_A` and
`N_B` carry the clustering's two-point power, which this field does not, so they sit *above* this
floor and the target is correspondingly smaller than `mock − floor`. **This column is a lower
bound on how much of the reading is manufactured, not an estimate of the target.** Quoting it as
a signal-to-floor ratio would be exactly the apples-to-oranges error this campaign keeps
catching.

What it does establish, model-free and before any null is built: **at `R = 10` the geometry and
shot noise alone account for 55–66 % of a mock's entire order-3 reading**, and at `R = 15` on
LRG — the row that would have carried the primary result — the floor is 35 % of the mock's total
while the surviving rung is a single one.

The ceiling-fraction column is reported per §4.5 **as a common denominator only**: `ln 2` is the
proved cap for three *binary* slots, and these are `b = 4` and `b = 6` readings. It is not a
compliance statement.

### S1.5a The same floor on BOSS — the comparison that makes the density finding model-free

`eboss_stage1_bossfloor.py` runs the **identical** split-randoms construction on BOSS DR12 SGC,
down-sampled to BOSS's own galaxy count. Same code, same constants, same seed discipline; the
run was repeated and reproduced **bit-identically** (`1.514183e-04`), which discharges **P13**,
gate-log provenance, for this artifact.

| folded row | **BOSS SGC** | **LRG SGC** | ratio | **LRG NGC** | **ELG SGC** | **ELG NGC** |
|---|---|---|---|---|---|---|
| R=15 b=4 | `1.514e-04` | `3.164e-04` | **2.1×** | `2.676e-04` | *occ fail* | *occ fail* |
| R=10 b=4 | `3.723e-04` | `1.689e-03` | **4.5×** | `1.756e-03` | `4.169e-04` | `5.077e-04` |
| R=10 b=6 | `5.977e-04` | `3.162e-03` | **5.3×** | `3.293e-03` | *occ fail* | *occ fail* |

**This is Stage 0's density finding, re-established without a single model.** LRG's manufactured
floor is **2.1× BOSS's at `R = 15` and 4.5–5.3× BOSS's at `R = 10`** — and `R = 10` is where
LRG's *only* surviving two-rung configuration lives. ELG, the denser sample, sits at 1.1–1.4× of
BOSS, which is the other half of the same story: ELG has the density and not the volume.

And the sharpest form of it, stated with its own caveat attached:

> **BOSS's entire corrected target at SGC `R = 10, b = 4` folded was `8.398e-04`. The floor that
> the identical pipeline manufactures on LRG SGC at that configuration — from geometry and shot
> noise alone, with no clustering in the field at all — is `1.689e-03`, which is 2.0× that whole
> signal.**
>
> *The caveat, because this is precisely where an apples-to-oranges error would go:* BOSS's
> `target` is measured against `N_A`/`N_B`, which carry the clustering's two-point power and
> therefore sit **above** this floor. The two numbers are not the same quantity and the ratio is
> **not** a signal-to-noise statement. What it is: the pipeline's irreducible manufactured
> contribution on the eBOSS sample exceeds, in absolute size, the entire quantity BOSS was able
> to measure — which is a statement about the instrument, and it needs no null to make.

## S1.6 Cost, and what Stage 2 would have been

| sample | geometry build | one mock realisation |
|---|---|---|
| ELG NGC | 19 s | **14 s** |
| LRG NGC | 59 s | ~45 s (est. from grid size) |

At 14 s/realisation, ELG's 128-mock floor suite is **30 minutes per cap** and the 512-realisation
σ suite is **2 hours** — against BOSS's 26–55 s/realisation and 60-hour full suite. **Compute was
never going to be the constraint here, and disk (8.4 GB free at this writing, 100 % full) would
have been comfortable too under RULE E-S2-DISK, since only the 2 MB `dat` files are needed.**
Stage 2 was affordable. It is not being run because the arms it would gauge cannot reach their
own primary outcome, not because it was too expensive.

## S1.7 STATE

| item | status |
|---|---|
| pipeline adapted to eBOSS | **COMPLETE** — `eboss_stage1.py`, new code confined to I/O + geometry |
| Gate A, G9, G7 | **PASS** on all four samples |
| BOSS reproduction control | **PASS, bit-identical** to the committed artifact |
| **G9 occupancy** | **FIRED** — no two-rung configuration at `R = 15` on any eBOSS sample |
| `EBOSS_STAGE0.md` §S0.4 | **superseded** by `EBOSS_AMENDMENT_1.md` §A1.3–A1.4 |
| Stage 2 (G10 closure) | **NOT STARTED — stopped at the fired gate**, per the commission |
| unblind | **not approached.** The order is not the author's, and P7 would raise regardless |

**Stopped here.** The commission's instruction is to stop at any gate that fires, and one has —
not on a marginal row but on the clause that defines the campaign's primary outcome, and for a
reason that does not depend on what the data reads. `EBOSS_AMENDMENT_1.md` §A1.6 lays out the
three options without smuggling a recommendation in as a finding; the choice among them is a
pre-registration-level decision and is Eric's.

**`wild-share` does not move. Nothing here bears on it in either direction:** no eBOSS share has
been read, and the only eBOSS numbers in this document are geometry, a pipeline floor on a field
with no clustering in it, and one mock realisation.

---

*Stage 1 ends here. Files: `eboss_stage1.py`, `eboss_stage1_bosscheck.py`,
`eboss_stage1_bossfloor.py` and their JSON outputs, committed beside this document. No `lake`, no
Lean, no `Stance.lean`, no audit was touched at any point in this campaign.*
