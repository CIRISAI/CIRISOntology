# REG+ exact route-memory collapse scale — preregistered result

Prereg: `81ae7bd3493424355c2acf05498a62e61a14768c`

## Frozen verdict

**NO-COLLAPSE-THROUGH-12.**

No tested occupancy N=7..12 satisfied both frozen collapse conditions: median M<0.05 and at
least 50% of configurations below 0.05.

| N | median M | mean M | p10 | p90 | frac >0.20 | frac <0.05 |
|---:|---:|---:|---:|---:|---:|---:|
| 7 | 0.147472 | 0.205094 | 0.066691 | 0.333345 | 0.453 | 0.094 |
| 8 | 0.147472 | 0.179511 | 0.010729 | 0.333345 | 0.406 | 0.203 |
| 9 | 0.138371 | 0.162350 | 0.012943 | 0.333345 | 0.391 | 0.328 |
| 10 | 0.138371 | 0.156389 | 0.036793 | 0.333345 | 0.313 | 0.219 |
| 11 | 0.134887 | 0.135233 | 0.024622 | 0.333345 | 0.234 | 0.313 |
| 12 | 0.093097 | 0.117044 | 0.016724 | 0.288132 | 0.219 | 0.375 |

All 384 runs completed with no COMPUTE-LIMIT. Maximum state-norm error remained below
4.4e-15. Maximum sparse support at N=12 was 816 basis configurations, far below the frozen
2,000,000 cap.

## Secondary exposure diagnostic

Median ballistic route-contact exposure rises from 4 at N=7 to 8 at N=12, but Spearman
correlations between exposure count and M are weak and unstable (roughly 0 to -0.27 across
levels). Simple contact count is therefore not a sufficient mechanistic predictor of memory
loss in this finite experiment.

## Interpretation

The route-memory distribution shifts downward with occupancy, but the process is broad and
nonuniform. Even at N=12 some configurations retain the full two-particle witness M=0.333345,
while the median has fallen to 0.0931. This rules out a sharp low-density automatic-dephasing
picture in the tested window but does not establish a finite asymptotic coherence floor.

Finite-lattice model physics only. The next registered extension should search higher N for
the first crossing of the same low-memory criterion without changing the five-cycle read or
local grammar.
