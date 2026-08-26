# Re-analysis of the prior boards under the banked repairs — labelled, verdicts unchanged

*2026-08-26. The banked analyzers (`onset_analyzer.py`): threshold-relative onset
(1 % of max — D-MATERIALIZE's mitigation) and the in-job one-way premise check
(reverse ≤ 10× floor — D-CHAN-DRIFT's mitigation). Applied retroactively to the
recorded data of both Ω-KILL campaigns. **The frozen verdicts stand. This is
information for the next freeze, not a rescue — and it retracts a prior PASS as
readily as it explains the misses.**

## The re-analyzed boards

| arm | frozen verdict | under banked repairs |
|---|---|---|
| Ω-1 A2 (asym 14×, reverse 19.7× floor) | PASS | **VOID-PREMISE** — the channel already failed one-wayness (19.7× > 10×); the pass was adjudicated on a premise that did not hold |
| Ω-1 B3 (per-node sectors) | MISS | **UNRESOLVABLE** — the banked 1 %-rule still reads gap 0, because the identity pedestal (48/116) EXCEEDS 1 % of max on index-paired data. Threshold onsets repair index-FREE observables only; legacy index-paired data admits at best the weaker pedestal-excess diagnostic (611/1956, labelled) |
| Ω-2 A2 (asym 2.8×, reverse 137× floor) | MISS | **VOID-PREMISE** — same rule, same reason, further along the same drift |
| Ω-2 B3′ (index-free aggregates) | MISS | **PASS** — gap = 901 frames (left 393, right 1294) against the ≥ 10 band |
| all other arms, both campaigns | as recorded | unchanged |

## What this says, precisely

Under the banked repairs, **Ω-KILL-2's board reads 7/7 posable arms passed, one
arm VOID-PREMISE** — the reading a freeze with today's registry would have
produced. And Ω-KILL-1's board LOSES its A2 pass to the same rule: the
re-analysis is not a friend of the claim; it is a friend of the record.

Three statements, all true, none substituting for another:
1. The composition claim is FALSIFIED as staked, three times; those verdicts are
   final.
2. The physical content behind every miss is now accounted: a 901-frame
   light-cone the frozen stake could not see, and a channel whose one-wayness
   was already gone by the second epoch.
3. A freeze written under the full current registry — index-free observables,
   threshold onsets, in-job premise checks — has, on the recorded data, no
   remaining counterexample. That is a PREDICTION about Ω-KILL-3, not a result.

## The device-physics finding, standing on its own

The CRX pair's reverse influence grew monotonically across four epochs
(6.25× → 16.8× → 19.7× → 137× floor). Whatever its mechanism (calibration
ageing, spectator drift), "the realized channel this circuit compiles to" is a
MOVING TARGET on week timescales — D-CHAN-DRIFT is a property of the platform,
not of one pair on one day.
