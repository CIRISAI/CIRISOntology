# PGX-1 ARM 1 RESULTS — the N ladder to 10^6 (sealed 2026-08-23)

Prereg `POLARITON_GPU_EXT_PREREG.md` frozen before any code. Runner
`polariton_gpu_ext.py`; scorer `pgx1_score.py` written before results existed.
All arms on one RTX 4090, float64. Primary metric hardware-independent
(minimal reduced dimension); no wall-time claim is made anywhere.

## Truth gates — PASS with four orders of margin
G1 GPU Chebyshev vs scipy `expm_multiply`: 8.1e-15 at N=1024, 4.0e-15 at N=4096
(bar 1e-10). G2 sigma=0 two-state reduction: 1.32e-14 up to N=262144 (bar 1e-12).
Cross-check vs dense diagonalization at N=1024: 5.3e-14.

## The ladder (A = Krylov, C = defect clustering; minimal dimension at RMSE<=1e-4)

| sigma | A: N=1k,4k,16k,65k,262k,1M | C: same ladder |
|---|---|---|
| 0.1 | 8, 8, 8, 8, 8, 8 | 80, 96, 110, 126, 137, 149 |
| 0.3 | 16, 16, 16, 24, 24, 24 | 194, 253, 307, 355, 389, 421 |
| 1.0 | 48, 48, 48, 48, 48, 48 | 84, 103, 114, 125, 141, 147 |
| 3.0 | 96, 96, 128, 128, 128, none<=128 | 390, 260, 103, 115, 127, 134 |

Baseline B (equal-count binning) never converged within its grid at sigma=0.3 for
N>=4096, so C does beat B in that regime — and both lose to A.

## Verdicts under the frozen stakes
- **E1 FAILS at every sigma.** C's minimal dimension is far outside +/-20% across the
  ladder (0.1: 80->149; 0.3: 194->421; 1.0: 84->147). N-independent compression by
  defect clustering is FALSIFIED at scale. The CPU screen's PASS at sigma=0.1 was a
  two-decade artifact: over three more decades the same sequence keeps climbing.
- **E3 KRYLOV-ALREADY-CAPTURES-REACHABILITY fires in 20 of 24 cells**, by factors of
  3–15. The four exceptions are all sigma=3 — see the refinement below.
- **A is N-independent at sigma<=1** (8 / 16–24 / 48 flat over a 1000x size range) —
  the mechanism is self-averaging of the photon's spectral density; C must instead
  resolve the disorder support, which widens like sqrt(log N).

## Supplementary refinement (labelled exploratory, outside frozen scoring)
The frozen Krylov grid stops at 128 and sigma=3 hit that ceiling. Re-measured on a
dense grid with FULL reorthogonalization (twice-reorthogonalized Lanczos):
A_min = 110, 120, 130, 140 at N = 16k, 65k, 262k, 1M against C = 103, 115, 127, 134.
So at strong disorder the two are NECK AND NECK, C ahead by ~5% — far from the 2x
bar. Where both are measurable, plain and reorthogonalized Lanczos agree EXACTLY
(110, 120), which validates Arm 1's A values against orthogonality loss.

## Reading
Defect-certified near-twin clustering is **BASELINE-EQUIVALENT at best**: crushed by
Krylov at weak/moderate disorder, tied within 5% at strong disorder, never 2x better
anywhere on a three-decade ladder. Recorded caps: reduced dimensions above
EVAL_CAP=2500 were not diagonalized (a method needing more has already lost to a
baseline grid topping out at 1024).

## Independent convergence with the CPU screen
`POLARITON_SOFTSYM_BENCH_RESULTS.md` (different implementation, different hardware,
different seeds, N<=1024) reports Krylov 8/16/32/96 and P4 firing on 100% of
qualifying cells. Two independent instruments agree on the verdict and on the
N-independence of the Krylov dimension. The GPU adds the three decades that turn
the CPU screen's sigma=0.1 N-stability PASS into a measured FAIL.


## AMENDED 2026-08-23 — see PGX1_CORRECTION.md
The E3 `KRYLOV-CAPTURES` verdict is WITHDRAWN as an ARCHITECTURE verdict. Reduction
lowers the per-matvec cost O(N)->O(G); Krylov fixes the subspace dimension. They
COMPOSE and were never rivals. This file's measurements stand; the 'route is cut'
reading does not. The N/G ratio from this very ladder grows to 7037x at N=1e6.
