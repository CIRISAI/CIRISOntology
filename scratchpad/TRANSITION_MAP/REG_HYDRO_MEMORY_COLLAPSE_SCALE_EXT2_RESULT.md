# REG+ exact route-memory collapse scale extension II — preregistered result

Prereg: `5b916913183340278875fdb17de4fd9e505ba313`

## Frozen verdict

**COLLAPSE-LOCATED.**

The first tested occupancy satisfying the frozen low-memory criterion is **N_c=13**.

At N=13:
- median M = 0.0463949048
- fraction M<0.05 = 0.531250

On the 5x5 six-mode lattice this is descriptively 0.520 particles/site, or 8.67% occupancy
of directional modes. Those normalizations are not claimed as universal densities.

| N | median M | mean M | p10 | p90 | frac >0.20 | frac <0.05 |
|---:|---:|---:|---:|---:|---:|---:|
| 13 | 0.046395 | 0.090207 | 0.011394 | 0.232338 | 0.172 | 0.531 |
| 14 | 0.062435 | 0.094133 | 0.018699 | 0.225715 | 0.141 | 0.422 |
| 15 | 0.058001 | 0.092523 | 0.010966 | 0.232442 | 0.172 | 0.438 |
| 16 | 0.050119 | 0.076224 | 0.011734 | 0.199018 | 0.109 | 0.500 |
| 17 | 0.045346 | 0.060463 | 0.010598 | 0.129525 | 0.062 | 0.562 |
| 18 | 0.036647 | 0.063989 | 0.006363 | 0.184321 | 0.062 | 0.625 |
| 19 | 0.026793 | 0.051026 | 0.005262 | 0.152289 | 0.047 | 0.703 |
| 20 | 0.018024 | 0.032188 | 0.006047 | 0.058299 | 0.016 | 0.844 |

## Shape beyond the primary crossing

The crossing is not monotone immediately: N=14 and N=15 rebound above the 0.05 median
threshold, and N=16 sits just above it. Descriptively, the first level after which every
remaining tested level satisfies the same low-memory criterion is N=17.

From N=17 through N=20 the median falls 0.04535 -> 0.03665 -> 0.02679 -> 0.01802, while the
fraction below 0.05 rises 0.5625 -> 0.6250 -> 0.7031 -> 0.8438. This sustained-crossing
observation is post hoc and does not replace N_c=13 as the preregistered primary number.

## Compute and invariants

All 512 frozen configurations at N=13..20 completed exactly. No COMPUTE-LIMIT occurred.
The largest sparse support was 149,644 basis configurations at N=20, below the frozen
2,000,000 cap. Norm errors remained at floating-point roundoff.

## Interpretation

The one-spectator result correctly ruled out immediate automatic dephasing, but increasing
exact environmental occupancy eventually suppresses the route-memory witness strongly in
this five-cycle finite model. The suppression is configuration-sensitive rather than a
simple monotone function of particle count.

The next decisive test is finite-size scaling at fixed particles/site with the return time
scaled with lattice size. If the crossing tracks density across larger odd tori, it becomes
a credible emergent decoherence scale for this REG lattice family; if it tracks absolute N
or the five-cycle recurrence geometry, it is a finite-box artifact.
