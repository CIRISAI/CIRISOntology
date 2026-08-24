# APPROXIMATE BATH-EQUIVALENCE CLASSES — RESULTS

Executed 2026-08-22 against frozen `APPROX_BATH_CLASSES_PREREG.md` on GitHub Actions run `32585529483`, runner `approx_bath_classes.py`.

Artifact: `9478941357`, ZIP SHA256 `cbfc2e035dd5b318d99f50a114c0fa24f4e8f68a238892903e7b57c14654087a`.

## Implementation gates

A1–A3 all pass.

- singleton/full-profile reduction at N=128: max error `0.0`;
- smooth-ring vs scrambled-ring relabeling mismatch: `1.22e-15`;
- worst observed population error minus the frozen Duhamel certificate: `3.55e-15`.

The certificate is therefore valid for this instrument. It is deliberately worst-case and often saturates at 1, so validity is not the same as usefulness.

## Scientific stakes

**P1 passes.** At N=1024, `G=64` classes achieve max cavity-population error `6.44e-4`, below the frozen `1e-3` target.

**P2 passes strongly.** The minimum class count meeting `1e-3` is exactly `G=64` for every tested size N=128,256,512,1024. The approximate reduction is N-stable on this smooth two-coordinate profile manifold even though every molecular profile is distinct and the exact dynamic algebra is N-dimensional.

**P4 does not fire.** A useful `G<=128` reduction exists.

Frozen max-population errors:

| N | G=4 | G=8 | G=16 | G=32 | G=64 | G=128 |
|---:|---:|---:|---:|---:|---:|---:|
| 128 | 1.647e-1 | 4.189e-2 | 1.017e-2 | 2.419e-3 | 4.846e-4 | 3.55e-15 |
| 256 | 1.651e-1 | 4.201e-2 | 1.029e-2 | 2.540e-3 | 6.057e-4 | 1.212e-4 |
| 512 | 1.653e-1 | 4.205e-2 | 1.032e-2 | 2.570e-3 | 6.360e-4 | 1.515e-4 |
| 1024 | 1.654e-1 | 4.205e-2 | 1.033e-2 | 2.577e-3 | 6.435e-4 | 1.591e-4 |

The near-perfect N collapse at fixed G is the central positive result. For this construction, finite-time approximation complexity follows the metric complexity of the complete bath-profile manifold rather than the exact algebraic dimension.

## What did not pass automatically

The a priori Duhamel population certificate is too loose to select G efficiently. It is 1 for most G<=32 cells and remains `0.567–1.0` at G=64 even though observed error is only `~5e-4–6e-4`. The bound certifies safety but not practical compression.

This creates the next mathematical/computational problem: find a tighter **observable-weighted finite-time certificate** that exploits the fact that the cavity only samples a small part of the full state error. Such a certificate must be derived and frozen before being compared with observed error; fitting it to this trajectory would not count.

## Interpretation

This result reopens a narrow compiler route that the exact-algebra screen had seemed to close. The exact invariant sector can be extensive while the finite-time observable dynamics remain uniformly approximable by O(1) near-equivalence classes when complete molecule-to-bath profiles lie on a low-complexity manifold.

It does **not** establish simulation SOTA. The construction has two deterministic bath coordinates, a single-excitation system, and no explicit HEOM/HOPS hierarchy. Passing P1/P2 buys harder tests; it does not license a performance claim.

## Immediate falsifiers bought by this pass

1. **Intrinsic finite-time reachability:** compare the 64-class reduction with an oracle trajectory/POD rank and a time-dependent Krylov/reachable-space baseline. If those require far fewer than 64 directions, the class compiler is physically interpretable but computationally noncompetitive.
2. **Spatial–temporal bridge:** in a stochastic colored-noise polariton surrogate, test whether the projector weight `W(omega)` times the temporal bath spectrum predicts bright→dark transfer and its turnover with correlation time. Failure localizes the physics bridge; success gives a controlled bridge observable before HEOM.
3. **Profile complexity:** increase the number and roughness of bath coordinates. If minimum G scales extensively with N or bath-coordinate complexity under physically plausible profiles, the approximate-class route fails before an expensive tensor-network benchmark.
4. **Real open-system benchmark:** only if the above survive, insert the reduction into an MPS/HEOM/HOPS/TTN-style representation and compare solver cost at fixed physical-observable error.

## Fence

This is a favorable smooth-manifold control, not evidence that real molecular bath profiles have low metric entropy. The chemistry question is empirical: what is the covering number of the complete molecule-to-environment coupling profiles at the spatial and vibrational scales that materially affect polariton dynamics?
