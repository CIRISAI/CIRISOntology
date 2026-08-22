# REG+ coherent path Monte Carlo — target result

Prereg: `d9d17e886bdae71583cf6ed335600d7590d1aa4b`
License: `c539ead918412e99f04a69bf44661ec2e57e0bb0`

## Benchmark license

The smallest frozen candidate passing the exact paired L=7 LOW/MID benchmark was

`W = 10,000 walkers per replica`, with 8 independent replica-pair batches.

## Target result

**TARGET-STATISTICALLY-UNCONTROLLED**

### L=7 HIGH

- median M = 0.021762
- fraction M<0.05 = 0.875
- median SE = 0.002994
- p90 SE = 0.008418
- max SE = 0.032594
- classification: READABLE, LOW-MEMORY

### L=9 LOW

- median M = 0.050501
- fraction M<0.05 = 0.500
- median SE = 0.005823
- p90 SE = 0.012551
- max SE = 0.029392
- classification: READABLE, NOT LOW-MEMORY

### L=9 MID

- median M = 0.109684
- fraction M<0.05 = 0.125
- median SE = 0.029123
- p90 SE = 0.142954
- max SE = 0.344932
- classification: NOT READABLE under the frozen SE gates

### L=9 HIGH

The run was stopped after the target-control verdict became unrecoverable. Multiple
configuration estimates already exceeded the hard `SE <= 0.05` requirement; observed SE
values include >0.05 and one near 0.90. The cell is therefore not READABLE at the licensed
walker count regardless of its eventual point estimate.

## Interpretation

Complex-weight path sampling is substantially better behaved than basis-amplitude pruning:
it reproduces exact benchmarks and produces controlled estimates for L=7 HIGH and L=9 LOW.
But phase/sign cancellation creates a rapidly growing variance problem in the denser L=9
cells.

This is a representation/estimator limit, not evidence against coherent REG dynamics. The
next method should attack variance structurally rather than increasing W after target
inspection: e.g. branching/annihilating complex walkers or a locally entangled tensor
representation with explicit Schmidt-weight error accounting.
