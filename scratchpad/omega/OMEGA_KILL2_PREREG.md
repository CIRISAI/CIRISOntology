# Pre-registration — Ω-KILL-2: the retry, under the checked-prereg standard

**2026-08-26, frozen before either run launches; admissible only if
`Audit/prereg_audit.py` exits 0 on this file.** Fresh data on every arm: a new
QPU job (a new epoch — genuinely fresh under D-EPOCH's own logic) and a fresh
engine run on the repaired instrument. Binary exit: **CONFIDENCE ⇔ 8/8;
FALSIFICATION ⇔ any posable arm misses.** No rescue.

defects: D-IDENT (mitigated — B3′/B4′ read INDEX-FREE sector aggregates, sums
invariant under renumbering; B1/B2 twin comparisons are valid because sham twins
execute identical operation sequences, hence identical certification), D-EPOCH
(all S1 floors and references in-job), D-GATE (all couplings staked on realized
channels: CRX and the hop as delivered, the driver as prepared), D-DET (all
engine arms interventional: probe vs sham).

gauge: scratchpad/omega/gauge_omega2.log

Family-wise: Bonferroni over the 8 staked arms; S1 floors at the 99.5th
percentile of 1000-rep permutation nulls, in-job.

## S1 — QPU, one fresh job

| arm | stake (numeric) | witness: | posability |
|---|---|---|---|
| A1 idle | both directional defects ≤ 3× floor | witness: `independent_views_closed` — hypothesis "product map": no gate is applied between the pair; μ: hardware noise is physical | pilot: idle readings varied 0.1×–1.67× across sessions |
| A2 one-way CRX | fwd ≥ 50× floor ∧ fwd ≥ 5× reverse | witness: none (directed detection; `product_of_both_closed` gives the contrapositive frame) | fwd measured 298–510× across epochs; reverse 0.2–19.7× — both vary |
| A3 hop `XXPlusYY(π/2)` | both ≥ 10× floor ∧ max/min ≤ 3 | witness: none (realized symmetric exchange; D-GATE: staked on the delivered channel) | measured 31–42× and asym 1.17–1.52 across two jobs |
| A4 common-driver | both ≤ 3× floor ∧ created ≥ 50× its floor | witness: `common_driver_probe_null` — hypothesis "T = (f a c, g b c, h c)": realized by construction, one classical bit drives X⊗X; the prepared inputs are the probes | created measured 0.606–0.616 twice; defects 0.0× twice |

## S2 — engine, fresh run, interventional, index-free

| arm | stake (numeric) | witness: | posability |
|---|---|---|---|
| B1 sham twins | per-node divergence exactly 0 at all 1200 frames | witness: none (geometry-seeded determinism; identical sequences ⇒ identical certification) | one-ULP nonzero fires the band (gauge) |
| B2 pre-probe | exactly 0 at all 240 frames | witness: none (same fact) | same two sides |
| B3′ light-cone, index-free | right-sector aggregate-KE response onset minus left-sector onset ≥ 10 frames | witness: none (finite contact propagation; the diagnostic measured a 1345-frame gap at excess level) | planted gap 2 fires; gap 35 passes (gauge) |
| B4′ K, index-free | median growth ratio of total aggregate divergence over frames 245–1200 ≤ 1.05 | witness: none (`Aggregation` non-expansiveness, measured 1.0012/1.00444 on two prior instruments) | planted expanding series (K = 1.083) fires |

Onset defined as the first frame where the sector's |KE_b − KE_a| exceeds 0 (a
deterministic engine: any nonzero is real; B1/B2 establish the zero baseline).
VOID only for double device failure; the test VOIDs if either substrate voids.
Verdict sentences: `COMPOSITION2_PREREG.md` §0's, with "square".
