# FINITE-TIME REACHABILITY VS PROFILE CLASSES — RESULTS

Executed 2026-08-22 against frozen `FINITE_TIME_REACHABILITY_PREREG.md`.

First oracle-only run: GitHub Actions `32585841969`, artifact `9479015694`, ZIP SHA256 `a6aab0f7ec7a828a5c9a9ab3c7572f909363e10f50233d089c160c3a2eb1c1a1`.

Completed deployable-baseline run: GitHub Actions `32585962697`, artifact `9479078216`, ZIP SHA256 `802a33374997da848630306d60bf180815793cb36615e6a1b28d2bdb962b8577`.

## Gates

All implemented F1–F3 checks pass:

- every reduced-arm error is evaluated against the same full truth trajectory;
- smooth-ring vs deterministic scrambled-ring maximum error/dimension mismatch: `1.89e-15`;
- oracle POD error is monotone with rank;
- full snapshot rank reconstructs cavity population to a worst error `3.33e-15`.

## Headline result

**The profile-class compiler is not competitive as a propagation-reduction method on this frozen time-dependent surrogate. Generic restarted local Krylov is much smaller.**

At max cavity-population error `<=1e-3`:

| N | profile classes | oracle POD | restarted local Krylov |
|---:|---:|---:|---:|
| 256 | 64 | 8 | 4 |
| 512 | 64 | 8 | 4 |
| 1024 | 64 | 8 | 4 |

All three dimensions are N-stable across this range, but the generic deployable local Krylov arm needs only four directions per time step.

The frozen online residual-enriched global-basis grid did **not** reach `1e-3` before its threshold/cap limits, so it does not supply a competing positive result. That failure does not rescue profile classes, because restarted local Krylov already wins decisively.

## Frozen stakes

- P1, profile classes within 2× the online global dimension: **FAIL / not satisfied**; no online arm reached tolerance.
- P2, hidden low-rank finite-time dynamics: **PASS**; oracle POD rank is 8 while classes need 64.
- P3 N-stability:
  - profile classes: **PASS**;
  - restarted Krylov: **PASS**;
  - online global basis: **FAIL / no passing arm**.
- P4 time-dependence penalty: the N=1024 restarted Krylov dimension is **4**. Time dependence in this smooth deterministic model does not create a soft-symmetry solver niche.

## Consequence

The solver-SOTA interpretation of approximate profile classes is **CLOSED for this model**.

The positive `G=64` result remains scientifically useful in a narrower sense: an exactly N-dimensional operator algebra can have an N-independent finite-time approximation by complete-profile classes when those profiles lie on a smooth low-complexity manifold. But that does not imply computational optimality; generic propagation already exploits the reachable dynamics more strongly.

Approximate bath-equivalence should now be treated as one or more of:

1. a physically interpretable coarse-graining of molecule-to-bath coupling profiles;
2. a reusable parametrization across trajectories/parameters, if that reuse is later demonstrated;
3. an input to an a priori/a posteriori error certificate;
4. a possible structure for hierarchy/tensor compression only if an actual open-system representation shows a solver-specific benefit that local Krylov does not capture.

It should **not** be advertised as a superior propagator on the present single-excitation time-dependent model.

## Physics question opened by the failure

The stronger result is that finite-time trajectory complexity is far below both exact algebraic dimension and profile covering number:

`exact closure N  >>  profile classes 64  >>  oracle POD 8`,

while a deployable restarted propagator needs local dimension 4.

The next physics/computation question is therefore: **what sets the finite-time reachable dimension?** Candidate controls include temporal bandwidth/frequency count, spatial roughness of the bath profiles, polariton spectral filtering, observation horizon, noise strength, and genuinely non-Markovian quantum-bath memory. These are more promising complexity variables than exact symmetry alone.

## Fence

POD is an oracle diagnostic, not a deployable algorithm. Restarted Krylov is standard numerical prior art. This result is a falsification of a solver-performance hypothesis, not a negative statement about the usefulness of profile equivalence as a physical descriptor or about tensor/hierarchy methods in genuinely non-Markovian quantum-bath models.
