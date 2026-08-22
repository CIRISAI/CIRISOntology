# REG+ coherent path Monte Carlo — benchmark license

Parent prereg: `d9d17e886bdae71583cf6ed335600d7590d1aa4b`

**Status: LICENSED BEFORE TARGET EXECUTION**

The frozen exact L=7 LOW/MID paired benchmark was run at W=2,000 and W=10,000 walkers per
replica. The prereg selects the smallest W that passes; therefore the W=50,000 candidate is
not needed once W=10,000 passes.

## W=2,000 — FAIL

- median absolute M error = 0.00847
- p90 absolute error = 0.02002 (above 0.020 gate by ~2.5e-5)
- maximum absolute error = 0.05183 (above 0.050 gate)
- median MC SE = 0.00764
- MID aggregate classification is not low-memory (exact MID is low-memory)

Therefore W=2,000 does not pass.

## W=10,000 — PASS

- median absolute M error = 0.00234
- p90 absolute error = 0.00604
- maximum absolute error = 0.01129
- median MC SE = 0.00315
- p90 MC SE = 0.00518
- maximum MC SE = 0.00688
- LOW remains not low-memory: median M_MC = 0.08538
- MID remains low-memory: median M_MC = 0.04091
- no raw orientation-probability estimate crossed the frozen instability interval
  [-0.05,1.05].

All frozen gates pass. The licensed representation therefore uses:

`W = 10,000 walkers per replica, 8 independent replica-pair batches per configuration`.

No HIGH or L=9 path-MC target outcome was inspected before this license was recorded.
