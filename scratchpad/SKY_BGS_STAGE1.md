# STAGE 1 — the gate **FIRES**. DESI DR1 BGS cannot run the pre-registered analysis at the primary scale.

Stage 1's gate is *the split-randoms null re-run on DESI geometry; G9 and G7 re-passed.* The null
ran. It did not return a wrong number — **it returned no number, because the pre-registered
occupancy gate refused every reading in the grid.** That refusal is the finding.

**Nothing in this document is a galaxy statistic.** The split-randoms null contains no galaxies by
construction, and the occupancy gate blocked every estimator call before it ran. The campaign is
still fully blind and this result did not require breaking it — which is the point of putting a
geometry gate before the data.

---

## S1.1 What ran

Two disjoint halves of the DR1 BGS_BRIGHT NGC random catalogue (realizations 0,1 against 2,3),
painted on one shared grid so that the geometry is identical between them. 19.8 M objects per
half. Pipeline reused unchanged from `sky_realdata.py` per §11; new code confined to
`sky_bgs_io.py` (I/O) and `sky_bgs_stage1.py` (the null's construction).

| | |
|---|---|
| grid | 176 × 270 × 176 at 6 Mpc/h |
| valid cells after masking | 867 989 |
| **valid volume** | **0.1875 (Gpc/h)³** |
| `α` | 0.4989 |
| mask fraction | 0.0459 |
| `σ` of the smoothed field | 0.0449 |
| **independent smoothing volumes at R = 15** | **3 527** |

---

## S1.2 The gate's verdict, at every `b`

Occupancy is `n_indep / b³` — independent smoothing volumes per histogram cell — and the
pre-registered floor is **> 100**.

| `b` | occupancy at R = 15 | passes? |
|---|---|---|
| 4 | **55.1** | **no** |
| 6 | **16.3** | **no** |
| 8 | **6.9** | **no** |

**Every configuration at every `b` fails.** `folded`, `equilateral` and `squeezed` alike; the gate
is a property of the geometry, not of the triple shape. No `share`, no `I₃`, no LP interval was
computed, because the pipeline correctly declined to compute one.

**G7 and G9 are therefore NOT EVALUABLE at this stage** — not passed, not failed. A tied-fraction
disclosure and an IPF certificate are properties of a reading, and there is no reading. Recorded
as not-evaluable rather than as a pass, because a gate that reports "pass" on an empty set is the
defect this campaign exists to avoid.

---

## S1.3 The volume, measured against what was assumed

| source | volume | vs measured |
|---|---|---|
| **measured here** | **0.1875 (Gpc/h)³** | — |
| prereg §5.3 estimate | ~1.0 (Gpc/h)³ | **5.3× optimistic** |
| BOSS, measured | 5.388 (Gpc/h)³ | **28.7× larger** |

§5.3 already warned the campaign was *"expected to fail the occupancy gate at every `b` in at
least one cap."* The measured position is worse than that sentence: **there is only one cap** (S0-B
scoped SGC out on disk), and it fails at every `b`.

**And the disk-driven scoping is not what fails it.** Scaling by the SGC random-file size
(647.7/1579.4 = 0.41 — an *estimate*, not a measurement, since SGC was never downloaded), both
caps together give ≈ 0.264 (Gpc/h)³ and ≈ 4 973 independent volumes → occupancy ≈ **78 at b = 4**,
still below the floor. **Restoring the second cap would not rescue the primary scale.** The
binding constraint is survey volume in the trimmed redshift shell, not disk.

---

## S1.4 The trade-off, which is the real result

Two different occupancies bind in opposite directions, and this sample is caught between them.

| `R` | `n̄V_R` (galaxies per volume, S0-D) | `n_indep` | occupancy @ b=4 | BOSS-comparable (`n̄V_R ≥ 16.2`)? | occupancy > 100? |
|---|---|---|---|---|---|
| **15** | **19.94** | 3 527 | **55.1** | **yes** | **no** |
| 12 | 10.21 | 6 889 | 107.6 | no | yes |
| 10 | 5.91 | 11 904 | 186.0 | no | yes |
| 8 | 3.02 | 23 250 | 363.3 | no | yes |

**No `(R, b)` in the pre-registered grid satisfies both conditions.** Smaller `R` buys independent
volumes and loses galaxies per volume, at exactly the rate that keeps the product out of reach.
At the one scale where DESI's density clears BOSS, the survey is too small to sample it; at every
scale where it is large enough to sample, the density is below the instrument BOSS used.

This is the quantitative form of Amendment 6.3. There the premise's failure was stated as
"1.23× occupancy, not 10–100×". Here it is stated as: **the 1.23× is real and it is not enough,
because the volume deficit is 28.7×, and the two do not trade against each other favourably.**

---

> ## CORRECTION (2026-08-09, coordinator, same day) — §S1.5 below over-concluded
>
> The verdict as first written said the campaign **"cannot be executed on DESI DR1 BGS."** That
> is too strong and I withdraw it. Checked against the prereg: **`R = 10` is a REGISTERED scale**
> — Stage 0 §S0.3 already recorded the scored grid as *1 cap × 2 scales (`15`, `10`)* — and at
> **`R = 10`, `b = 4` the occupancy is 186, which PASSES the floor of 100.**
>
> The correct verdict is narrower: **the primary scale is dead; one registered extension cell
> survives.** That is not a post-hoc rescue and not a relaxed gate — it is a cell the
> pre-registration named before any DESI datum existed, and continuation option 2 (dropping to
> `b = 3`) remains exactly as inadmissible as stated below.
>
> The honest caveat stands and is now the live question: at `R = 10` the density is
> `n̄V_R = 5.91` against BOSS's 16.2, so the shot-noise floor is ~2.7× worse per volume and the
> cell may be floor-dominated. **The prereg already contains the test for that** — Stage 2's
> **G10 mock closure is the go/no-go**, and DR1 ships 25 AbacusSummit N-body plus 1000 EZmock BGS
> realizations to run it on. The campaign is therefore **narrowed to one cell with a
> pre-registered procedure for deciding whether that cell is readable**, not ended.
>
> Recorded rather than edited away: the over-conclusion was mine, it ran in the pessimistic
> direction, and it was caught by re-reading the prereg's own grid rather than by any gate.

## S1.5 Verdict, and what it is not

**The confirmation campaign as pre-registered cannot be executed on DESI DR1 BGS.** Not "is
weaker than hoped" — the primary scale has no admissible `b`, and no scale in the extension set
has BOSS-comparable density.

**What this does NOT say.** It says nothing about whether whole-only structure exists in the
galaxy field. It is a statement about an instrument and a survey, made before any data statistic
was computed, and the BOSS reading's status is exactly what it was: **wounded by its own refuter
and not cashed.** This result neither confirms nor refutes it. `wild-share` remains **open**, and
the honest change is that its named instrument is now known not to reach.

**Available continuations, none taken here** — the choice belongs to the steward, and each is an
amendment, not an adjustment:

1. **Report as measured infeasibility** and stop, in the form the water campaign used: the design
   is sound, the substrate cannot carry it, the arithmetic is published so the next person does
   not repeat it. This is the honest default.
2. **Lower `b` to 3** — occupancy 130.6 at R = 15, which passes. But `b = 3` is outside the
   pre-registered set, coarsens the statistic, and would be a post-hoc grid choice made *after*
   seeing that the registered grid failed. That is the shape of the defect this campaign's own
   gates exist to catch, and it should not be done quietly if it is done at all.
3. **Widen the redshift shell** past S0-A's factor-of-3 trim to buy volume — at the price of the
   selection-function gradient the trim exists to control, on a sample whose untrimmed `n̄(z)`
   varies by 2418×.
4. **Wait for DR2** (401 today, collaboration-only) — more volume in the same shell, and the only
   continuation that does not trade a gate for a number.

**Recommendation, stated as one and not as a decision:** (1) with (4) named as the successor
instrument. Options 2 and 3 both buy a runnable number by relaxing a gate that was fixed before
the data was seen, and the campaign's whole value is that it did not do that.
