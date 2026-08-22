# H3ERE2 single-shot held-out validation — VERDICT: NOT LICENSED (2026-08-22)

Frozen candidate h3ere2_v2.py (sha 523fd6d0c45cd50e), run ONCE on data it never saw:
124 odd-line curated items + 238 wild units from fresh-seed chains. No reruns; the
held-out samples are spent.

| criterion | measured | bar | verdict |
|---|---|---|---|
| L1 accuracy | 0.7177 | >= baseline 0.7177 (same items) | PASS (at par) |
| L1 deep-kind | 0.7083 | >= 0.7389 (baseline 0.6389 + 10) | **FAIL by 3.1 pts** |
| L2 wild kappa | 0.3488 | >= 0.40 (pinned convention; T4 guards both PASS) | **FAIL** |
| L3 coverage | 1.000 / 1.000 | >= 0.85 | PASS |

## The honest reading

1. THE DEEP IMPROVEMENT IS REAL AND SMALLER THAN CALIBRATION CLAIMED: +6.9 points
   held-out vs +16.3 on calibration — tuning overfit roughly half its gain. The staked
   +10 bar was missed out-of-sample. No re-litigation: the bar was frozen, it was not met.
2. THE WILD CEILING IS NOW THE MOST REPLICATED NUMBER IN THE CAMPAIGN: ~0.35 on three
   independent wild samples (0.355 sealed, 0.386 calibration, 0.3488 held-out) across
   two licensed panels and a recursive pipeline, with no label collapse (12 labels,
   modal 0.447 — the T4 guards passed; the failure is honest). Substrate-intrinsic.
3. Per the frozen prereg: the ceiling stands against this architecture class; THE
   HUMAN-LABEL ROUTE (or the block-scoped agent stream) is the wild leg's instrument.
   The pipeline remains valuable as the CURATED/validity instrument (at-par accuracy,
   +6.9 deep, full coverage) and as the design basis for Objective 1 — with this verdict
   carried in the design record, not smoothed over.
