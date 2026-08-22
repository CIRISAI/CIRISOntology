# FAIR PROPAGATOR COST — PROFILE CLASSES VS FULL KRYLOV — RESULTS

Executed 2026-08-22 against frozen `FAIR_PROPAGATOR_COST_PREREG.md` on GitHub Actions run `32586465938`.

Artifact `9479232600`; ZIP SHA256 `36f7988f41a34e77221289ead28de651ce06702877e0bdc8aa9a5118292d4a7a`.

## Why this result supersedes the earlier dimension-only cost interpretation

`FINITE_TIME_REACHABILITY_RESULTS.md` found that a full-space restarted Krylov step needs only local dimension 4 while the approximate profile model needs 64 physical classes. A fairness audit correctly noted that basis size is not cost: the full Krylov vectors have length N+1, whereas class-space vectors have length G+1.

This screen uses the **same in-house restarted Arnoldi implementation on both arms**, the same midpoint time grid, the same target observable, and the same error threshold. It counts sparse matvec and orthogonalization work using the same hardware-independent proxy.

## Gates

FPC1–FPC3 all pass:

- minimum full-space Arnoldi dimension remains `m=4` for every N;
- the class-space Arnoldi calculation is converged relative to the intrinsic class-model error;
- smooth/scrambled relabeling error mismatch is `3.77e-15`.

## Primary result: class reduction wins actual arithmetic

At max cavity-population error `<=1e-3`, the minimum-cost configurations are:

| N | FULL | FULL `C_proxy` | CLASS | CLASS `C_proxy` | CLASS/FULL |
|---:|---|---:|---|---:|---:|
| 256 | m=4 | 1,642,400 | G=64, m=4 | 413,600 | 0.2518 |
| 512 | m=4 | 3,280,800 | G=64, m=4 | 413,600 | 0.1261 |
| 1024 | m=4 | 6,557,600 | G=64, m=4 | 413,600 | 0.06307 |

The corresponding class-model max population errors are:

- N=256: `6.06e-4`;
- N=512: `6.36e-4`;
- N=1024: `6.43e-4`.

The full m=4 Arnoldi error is `3.66e-6` at every N, well below the target but not enough to offset its O(N) vector cost.

Thus P1 passes strongly: at N=1024 the class arithmetic proxy is not merely <= half the full cost; it is about **6.3%**, a ~15.9x reduction.

P2 also passes: the CLASS/FULL cost ratio decreases approximately inversely with N while the selected G stays fixed at 64.

## Wall-time result

The frozen same-process timing protocol also passes P3 at N=1024: including one-time class construction, the class arm's median one-trajectory total is <=0.8 of the full propagation time.

P4 reports a break-even of **one trajectory**. In this simple deterministic profile construction, class detection/construction is negligible relative to the propagation saving.

Wall time is supportive rather than primary because this is Python/CI code; the hardware-independent arithmetic proxy is the stronger result.

## What is actually established

This resolves the apparent contradiction between the reachability and profile-class screens:

- exact dynamic algebra dimension: N;
- profile-class reduced physical dimension: 64;
- oracle trajectory POD rank: 8;
- local Krylov dimension: 4 on both the full and reduced spaces;
- **total arithmetic still favors the 64-class model because the Krylov vectors themselves are 64-dimensional rather than N-dimensional.**

So generic reachability and structural reduction are complementary, not mutually exclusive. The best composition here is:

`profile compression -> Krylov propagation`,

not profile compression instead of Krylov.

## Simulation consequence

The profile-class route is **REOPENED and passes its first fair computational gate** on the frozen smooth low-metric-entropy dynamic model.

This is not yet simulation SOTA. The result is only a controlled single-excitation surrogate, and `PROFILE_COMPLEXITY_RESULTS.md` shows that the advantage can disappear as complete bath-profile metric entropy grows. But the surviving algorithmic hypothesis is now concrete:

> When complete molecule-to-environment profiles admit an N-stable covering number G at the target physical error, structural profile reduction can reduce the state dimension before a standard Krylov/tensor/hierarchy solver, yielding work that scales with G rather than N.

The next external test must compare this composition against a production open-system method at fixed observables, not against an intentionally weak baseline.

## Physics/computation boundary

The computational gain depends on a physical property of the environment: the metric entropy / approximate equivalence structure of the complete system-bath coupling profiles. `PROFILE_COMPLEXITY_RESULTS.md` shows this is not guaranteed by low covariance rank, smoothness, or low generator count.

Therefore a real chemistry benchmark should first characterize or construct physically justified profile sets, then measure whether G remains subextensive with aggregate size.

## Fence

Restarted Arnoldi/Krylov and reduced-order modeling are prior art. This result does not establish superiority to MPS-HEOM, HOPS, TTN-HEOM, d-CUT-E, PIQS, or other production methods. It establishes only that the previously proposed structural reduction has a genuine common-kernel arithmetic advantage in one preregistered dynamic model after correcting a fairness error.
