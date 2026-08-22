# REG+ annihilating coherent Monte Carlo — benchmark license

Parent prereg: `5f65a5bbac277ffb57216a9c0e7700325bc20990`

**Status: LICENSED BEFORE HELD-OUT TARGET EXECUTION**

The three frozen populations were benchmarked on the exact paired L=7 LOW/MID cells.

## W=500 — FAIL

- median abs M error = 0.06238
- p90 = 0.26633
- max = 0.51106
- median SE = 0.02163
- MID classification fails.

## W=2,000 — FAIL

- median abs M error = 0.01557
- p90 = 0.05626
- max = 0.10999
- median SE = 0.01160
- MID classification fails.

## W=10,000 — PASS

- median abs M error = 0.00611
- p90 abs error = 0.01459
- max abs error = 0.02784
- median MC SE = 0.00571
- p90 MC SE = 0.00998
- max MC SE = 0.01175
- LOW remains not low-memory: median M = 0.08883
- MID remains low-memory: median M = 0.04362
- no raw orientation-probability estimate crossed [-0.05,1.05].

All frozen gates pass. The licensed population is therefore:

`W = 10,000 walkers per replica, with complex annihilation/resampling after every global cycle`.

The held-out target configuration lists were generated under the preregistered seeds before
this license, but no held-out target outcome was executed or inspected before this commit.
