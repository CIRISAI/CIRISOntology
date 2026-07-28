# ARM A — advance test T1, declared BEFORE the matched-length re-run is analysed

**Written at the point in the run where the 41-configuration readings exist and the
201-configuration re-run is still in the MD queue.** The ordering is evidenced by file
timestamps: `water_arm_a.json` and `water_arm_a_run.log` are already written;
`water_mw_sweep_matchN.json` is still being produced by a running process, and the analysis of it
has not been started.

## What was seen

At the first pass the gate-passing `λ` ladder was read at **unequal configuration counts** —
41 frames at every `λ` except `23.15`, which had 201. That is the Dalitz D2 taint
(`GATES.md`: *a floor is drawn at the SAME sample size as the reading it gauges*), and it is being
corrected by re-running the six short points at the same production length. Count-matched on
triangles (cap 3776), the first-pass readings were:

| `λ` | `p₁` | share (nats) | floor median | `p` |
|---|---|---|---|---|
| 20 | 0.867 | 1.37e−06 | 3.61e−06 | 0.681 |
| 20.5 | 0.852 | 6.39e−07 | 3.02e−06 | 0.767 |
| 21.5 | 0.816 | 3.73e−06 | 3.43e−06 | 0.478 |
| 22 | 0.798 | 6.94e−06 | 2.76e−06 | 0.269 |
| 23.15 | 0.747 | 7.45e−06 | 6.51e−07 | **0.0166** *(201 configs)* |
| 25 | 0.638 | 6.58e−08 | 3.31e−06 | 0.927 |
| **27** | 0.463 | **4.41e−05** | 3.17e−06 | **0.0100** |

**Two points sit below `p = 0.05` out of fourteen tests** (seven `λ` × two count modes, and the
two modes are not independent). With seven `λ` points, `P(at least one p < 0.01) = 6.8 %` under
the null, so **neither is significant after the ladder's own multiplicity**, and the ladder is
**not monotone**: `λ = 25` is the *smallest* reading in the whole set and sits between the two
largest. Nothing is claimed from this pass.

## The test, staked now

> **T1.** The re-run gives every `λ` **201 configurations**, i.e. **5× the data** at the six short
> points, with a floor **≈ 5× lower**.
>
> * **If `λ = 27`'s reading is a property of the state point**, the share stays near
>   `4.4 × 10⁻⁵` nats while its floor falls, and its `p` drops well below `0.01`.
> * **If it is a fluctuation of a `χ²`-shaped null**, the share falls toward the new floor and `p`
>   returns to the interior of `[0, 1]`.
>
> The same test applies to `λ = 22`, whose first-pass reading (6.94e−06, `p = 0.269`) is the
> largest of the sub-threshold points, and — in the other direction — to `λ = 23.15`, which is
> the ONLY point whose configuration count does **not** change and which therefore must reproduce
> its own number to within the estimator's reproducibility.
>
> **`λ = 23.15` is the control on the test itself: it must not move.**

**Polarity, declared: a PASS of T1 is the λ = 27 reading PERSISTING.** A fall toward floor
fires it, and firing it means the first pass was noise — which is the outcome the non-monotone
ladder and the multiplicity arithmetic both already suggest.

**Whatever T1 returns, no verdict is scored on the first pass**, whose configuration counts were
mismatched by a factor of five and which is superseded by the re-run in
`WATER_RESULTS.md`. This document exists so that the re-run is a test rather than a re-reading.

Primary seed **20260727**.
