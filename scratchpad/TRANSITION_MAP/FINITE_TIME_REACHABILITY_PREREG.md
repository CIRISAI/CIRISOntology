# FINITE-TIME REACHABILITY VS PROFILE CLASSES — PREREG

Frozen 2026-08-22 after `APPROX_BATH_CLASSES_RESULTS.md` and before any finite-time baseline implementation exists.

## Question

The smooth-profile class compiler reached max cavity-population error <=1e-3 with G=64 independently of N from 128 to 1024. Is that a genuine computational advantage, or is it merely an interpretable but inefficient basis compared with generic finite-time reachability methods?

This test is explicitly allowed to kill the compiler route even though approximate bath classes passed their own gate.

## Frozen model

Use exactly the SMOOTH-RING and SCRAMBLED-RING time-dependent models from `APPROX_BATH_CLASSES_PREREG.md`: same N, T=20, temporal functions, uniform cavity coupling, and target observable (cavity population). No change to the physical instance is allowed.

Primary sizes: N in {256,512,1024}. Target max absolute cavity-population error <=1e-3 over the full trajectory.

## Arms

A. **Profile classes**: frozen G grid {4,8,16,32,64,128} and the same centroid reduction already tested.

B. **Oracle snapshot POD**: construct an SVD/POD basis from the exact full-state trajectory on the same time grid and report the minimum rank meeting the target when the exact projected trajectory is evaluated. This is an unattainable oracle lower-bound-like diagnostic, not a deployable competitor.

C. **Adaptive time-dependent Krylov**: propagate the full time-dependent Hamiltonian using restarted local Krylov subspaces over fixed time slabs, with Krylov dimension selected from a frozen grid and error checked against full truth. Report the maximum/mean local dimension and total matrix-vector products.

D. **Online reachable basis**: build a global basis incrementally from residual directions encountered during propagation, without using future truth snapshots. Freeze an orthogonal-residual enrichment threshold grid before execution. The basis is reusable over the whole trajectory once enriched.

All deployable arms must include basis-construction cost in wall time. Primary comparison is dimension/work at fixed error; wall time is secondary because implementation quality may differ.

## Gates

F1. Every reduced arm's reported observable error is recomputed directly against the same full truth trajectory.

F2. SCRAMBLED-RING produces the same profile-class and generic-baseline errors/work as SMOOTH-RING up to numerical tolerance, modulo timing noise.

F3. Oracle POD reconstruction error is nonincreasing with rank and reaches machine floor at full rank.

Failure voids performance interpretation.

## Scientific stakes

P1 — compiler competitiveness: profile classes remain computationally interesting only if the minimum G meeting 1e-3 is <=2x the minimum deployable global reachable-basis dimension, or if their total matrix-vector work is <=2x adaptive Krylov. Otherwise the compiler is downgraded to interpretability/diagnostics.

P2 — hidden low-rank dynamics: if oracle POD rank <=16 at N=1024 while profile classes need G=64, the positive approximate-class result is not evidence of strong compression; generic dynamics already live in a much smaller trajectory subspace.

P3 — N-stability: for each deployable arm, record whether its minimum dimension/work stays within a factor 2 from N=256 to 1024. If only profile classes are N-stable, that is a genuine algorithmic clue even if they are not smallest at this tolerance.

P4 — time dependence penalty: compare with the earlier static polariton Krylov benchmark. If adaptive time-dependent Krylov remains O(10)-dimensional/work-light, then time dependence alone does not open a SOTA niche for soft symmetry.

## What each outcome means

- Profile classes lose badly to B/C/D: retain them as a physical coarse-graining and certificate language, cut the solver-SOTA angle.
- Profile classes are comparable but not superior: pursue only if they provide stronger a priori error control or transfer across bath realizations/parameters.
- Profile classes win in reusable global dimension or work: buy the first actual open-system hierarchy/tensor benchmark.

## Fence

POD is an oracle diagnostic and cannot be cited as a practical method. Adaptive Krylov/reachable bases are generic numerical baselines, not claimed novel. The only possible contribution here is evidence that complete-profile near-equivalence provides reusable structure beyond what generic finite-time reachability already extracts.
