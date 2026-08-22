# PGX-1 CORRECTION — I tested the wrong architecture, and my own data supports theirs (2026-08-23)

The concurrent session's fairness audit reports that with the SAME restarted Arnoldi on
both models, a 64-class profile reduction cuts the hardware-independent arithmetic proxy
to 25.2% / 12.6% / 6.3% at three error targets — about 15.9x less work — and that the
right architecture is **profile reduction -> ordinary Krylov**, not profile reduction
VERSUS Krylov.

## The correction I owe
PGX-1 Arms 1 and 2 compared candidate C and baseline A as ALTERNATIVES and concluded
`KRYLOV-ALREADY-CAPTURES-REACHABILITY`. That conclusion answers the wrong question.
Krylov's DIMENSION is N-independent (8-48 across three decades, measured). But each
Krylov matvec on the full model costs O(N). Reduction does not compete with Krylov for
the subspace — it lowers the COST OF EVERY MATVEC, from O(N) to O(G). The two compose;
they were never rivals. My E3 verdict is therefore NOT a refutation of their claim, and
I withdraw the implication that it was.

## And my data makes their case stronger than the cell they measured
Arm 1 measured G across three decades. The economically relevant ratio N/G, from the
sealed table:

| sigma | N=1k | 4k | 16k | 65k | 262k | 1M |
|---|---:|---:|---:|---:|---:|---:|
| 0.1 | 13x | 43x | 149x | 520x | 1913x | **7037x** |
| 0.3 | 5x | 16x | 53x | 185x | 674x | **2491x** |
| 1.0 | 12x | 40x | 144x | 524x | 1859x | **7133x** |

**The compression ratio grows by three orders of magnitude across the ladder.** This is
the constructive reading of my own E1 FAILURE: G is not N-independent — it climbs like
the disorder support, ~sqrt(log N) — but it climbs FAR slower than N, so N/G improves
monotonically. E1 asked whether G is constant (it is not, and that stands as measured);
the question that matters for cost is whether N/G grows (it does, steeply). Both
statements are true and only the second is economically relevant.

## The mechanized explanation of their hard boundary
They report that compression erodes with complete bath-profile complexity, and that the
governing variable is **metric entropy / covering number of the coupling profiles, not
covariance rank, generator count, or spatial smoothness**.

`Core/GrayAlgebra.lean`, cashed in earlier today, is exactly that statement as a theorem:
`Kmat_det_ne_zero` — a profile whose values are pairwise DISTINCT closes its Krylov space
to the entire space regardless of how low its rank is; `Kmat_det_eq_zero_of_not_injective`
— confinement happens precisely when values REPEAT. Rank is the wrong invariant by
theorem; what confines dynamics is degeneracy, and its quantitative continuous analogue
is exactly a covering number at the tolerance scale. Their empirical boundary and my
theorem are the same fact from two directions.

## Status of the earlier PGX-1 verdicts under this correction
- E1 (G not N-independent): STANDS as measured, and is the input to the N/G table above.
- E2 (C vs B, 64/64 wins, median ratio 1.12-1.35 < 2.0): STANDS. It compared two
  reduction schemes, which IS an alternatives comparison, and is unaffected.
- E3 (KRYLOV-CAPTURES): **WITHDRAWN as an architecture verdict.** It remains true as
  the narrow statement it measured — Krylov needs fewer basis vectors than clustering
  needs classes — but that comparison does not bear on the composed architecture, and
  I should not have let it carry a "the route is CUT" reading.
- The "closed static-disorder route is cut" sentence in PGX1_ARM1_RESULTS.md and
  PGX1_ARM2_RESULTS.md is hereby AMENDED: cut as a RIVAL to Krylov, not cut as a
  PREPROCESSOR for it. The falsification I reported was real but narrower than I framed it.
