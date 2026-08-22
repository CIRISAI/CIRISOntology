# FINITE-TIME REACHABILITY VS PROFILE CLASSES — PARTIAL RESULTS

Executed 2026-08-22 against frozen `FINITE_TIME_REACHABILITY_PREREG.md` on GitHub Actions run `32585841969`, runner `finite_time_reachability.py`.

Artifact: `9479015694`, ZIP SHA256 `a6aab0f7ec7a828a5c9a9ab3c7572f909363e10f50233d089c160c3a2eb1c1a1`.

## Scope of this result

This first implementation executes the frozen profile-class arm and the oracle snapshot-POD arm. It also checks relabeling invariance and POD monotonicity. The adaptive time-dependent Krylov and online reachable-basis arms are **not yet implemented**, so preregistered P1/P3/P4 remain closed and no deployable solver-comparison claim is made.

## Gates implemented so far

- F2 relabeling mismatch, smooth vs scrambled profiles: `1.33e-15`.
- F3 POD observable error is monotone nonincreasing with rank.

Both pass.

## Decisive partial outcome

The frozen P2 hidden-low-rank diagnostic fires exactly as written:

| N | minimum oracle POD rank for max cavity-population error <=1e-3 | minimum profile classes G for same error |
|---:|---:|---:|
| 256 | 8 | 64 |
| 512 | 8 | 64 |
| 1024 | 8 | 64 |

The same result holds after deterministic emitter relabeling.

Thus the full time-dependent trajectory itself occupies a much smaller observable-relevant snapshot subspace than the physically interpretable profile-class basis. The 64-class N-stability result remains mathematically real, but it is **not evidence by itself of near-optimal compression**.

## Interpretation

This strengthens the anti-hype fork:

- exact dynamic algebra dimension: N;
- approximate profile-class dimension at 1e-3: 64, N-stable;
- oracle finite-trajectory dimension at the same observable tolerance: 8, also N-stable.

So finite-time dynamics can be far more compressible than complete-profile covering numbers suggest. A solver that learns the actually reachable trajectory may beat a static profile compiler by an order of magnitude in dimension.

However, POD uses future truth snapshots and is not deployable. It is an oracle diagnostic, not a fair performance baseline. The remaining question is whether generic **online** reachability/restarted Krylov can approach rank ~8 without expensive full-state information.

## Consequence for the compiler route

The burden of proof rises substantially. Approximate bath-equivalence remains interesting only if it provides at least one advantage generic online methods do not:

1. reusable basis across trajectories/parameters/bath realizations;
2. an a priori or adaptive error certificate unavailable to black-box reachable bases;
3. lower total matrix-vector/hierarchy work after basis construction;
4. substantially better behavior in an actual open-system hierarchy/tensor representation.

If adaptive Krylov/online reachability also stays O(10)-dimensional, the solver-SOTA angle should be cut and profile classes retained only as physically interpretable coarse-graining/certification language.

## Open physics angle

The rank-8 oracle result itself is a useful clue: the driven smooth two-coordinate bath explores a tiny finite-time manifold despite exact algebraic closure N. The open question becomes what sets this trajectory dimension physically — bath bandwidth, temporal frequency count, spatial profile smoothness, observation horizon, or polariton spectral filtering. Those dependencies are directly falsifiable and may matter more for simulation cost than exact symmetry.

## Fence

POD is an oracle diagnostic and cannot be cited as a practical algorithm. This partial result does not adjudicate preregistered P1/P3/P4 until adaptive time-dependent Krylov and an online reachable basis are implemented on the same frozen instance.
