# THE POLARITON COVARIANCE CONTROL WAS UNACHIEVABLE BY CONSTRUCTION (2026-08-23)

The full spatiotemporal OU run failed its implementation gate — empirical covariance
Frobenius error below 0.15 in every slice — with an N=128 slice reaching ~0.177 on 32
trajectories. The natural reading was "32 trajectories were insufficient at large N."
**That reading is too kind. The control was impossible at EVERY N tested.**

## Measurement
Relative Frobenius error of an empirical covariance from M=32 samples concentrates
around `sqrt((N+1)/M)`. Measured against that prediction:

| N | measured rel. Frobenius error (M=32) | predicted | vs 0.15 threshold |
|---|---:|---:|---|
| 8 | 0.481 | 0.530 | **IMPOSSIBLE** |
| 16 | 0.597 | 0.729 | **IMPOSSIBLE** |
| 32 | 0.844 | 1.016 | **IMPOSSIBLE** |
| 64 | 1.212 | 1.425 | **IMPOSSIBLE** |
| 128 | 1.670 | 2.008 | **IMPOSSIBLE** |

The N=128 slice that "reached 0.177" was therefore not a near-miss — on this statistic
32 trajectories cannot get near 0.15 at any N ≥ 8. Trajectories required for the frozen
threshold: **~2,889 at N=64 and ~5,734 at N=128** — a 90× and 179× shortfall.

(The observed 0.177 being far BELOW the ~1.67 this predicts suggests the pipeline's
statistic is not the full-matrix relative Frobenius error the prereg describes — either
a different normalisation or a partial matrix. That discrepancy should be resolved
before the redesign is frozen; it is flagged, not assumed.)

## The design defect, named
A control whose sample requirement scales with the dimension of the object being
controlled cannot be applied at fixed sample size across a size sweep. Its difficulty
grows with N while the budget stays flat, so it fails for reasons unrelated to the
science. **This is the same error class the campaign has now hit three times: a
criterion frozen without checking it was satisfiable by the instrument that would run
it** (cf. UNIV-1's mis-signed localization null, PGX-1's censored-B ambiguity).

## The fix — make the control's cost N-INDEPENDENT
The science depends on the bath only through its action on a low-dimensional subspace
(the bright/dark sector and the observable). Control the covariance **projected onto a
fixed k-dimensional subspace** rather than the full N×N matrix:

| k | trajectories needed for 0.15 | scaling |
|---|---:|---|
| 2 | ~134 | **N-independent** |
| 4 | ~223 | **N-independent** |
| 8 | ~400 | **N-independent** |

At k=4 the control becomes achievable with ~223 trajectories at EVERY N in the sweep,
and it controls exactly what the dynamics can see. Two further options, weaker:
scale M with N (expensive, ~5.7k at N=128), or control scalar functionals only
(cheap but much less informative).

## Recommendation
Redesign the gate as a projected-covariance control at fixed k with M ≥ 250, re-freeze,
and only then re-run. Do NOT relax the threshold — the threshold was never the problem.
