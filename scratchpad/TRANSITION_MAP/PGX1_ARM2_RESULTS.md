# PGX-1 ARM 2 RESULTS — the disorder ensemble (sealed 2026-08-23)

256 independent disorder realizations (64 per cell), the statistics the CPU screen's
single seed could not provide. Scorer written before results existed.

## The measured ensemble

| cell | C_min median [range] | B baseline | A (Krylov) median |
|---|---|---|---|
| N=4096, sigma=0.3 | 254 [240,262] | **never converged, 64/64** (grid cap 1024) | 16 |
| N=4096, sigma=1.0 | 99 [95,105] | 128 | 48 |
| N=16384, sigma=0.3 | 305 [297,315] | **never converged, 64/64** | 16 |
| N=16384, sigma=1.0 | 114 [109,119] | 128 | 48 |

## E2 — and the reason it is NOT a flat negative
Against baseline B, candidate C wins **64 out of 64 realizations in every cell**
(sign test p = 1.08e-19). The win is utterly reproducible. But the EFFECT SIZE fails
the frozen bar: median(B/C) = 1.347 and 1.123 at sigma=1.0, against a required 2.0.

**This is the clearest demonstration in the campaign of why an effect SIZE must be
staked and not merely a significance.** A p-value of 1e-19 with a 1.1x effect would
have been reported as a triumph by any significance-only protocol. The prereg's 2.0
bar is what converts it into the correct verdict: real, reproducible, and too small
to matter.

At sigma=0.3 the comparison is CENSORED, not absent: B fails to converge anywhere
within its grid, so the observable quantity is a LOWER BOUND on the ratio —
median(B/C) > 1024/254 = 4.03 (N=4096) and > 1024/305 = 3.36 (N=16384). Both exceed
the 2.0 bar. **Reported honestly: against the disorder-binning baseline alone, C
would PASS at sigma=0.3.** The frozen scorer returns VOID/FAIL there because the
prereg never specified censored handling — my defect, already recorded; the censored
bound is the substantive reading and it favours the candidate.

## E3 — why the candidate still is not a route
The same ensemble measures the baseline that actually matters:
median A_min = 16 (sigma=0.3) and 48 (sigma=1.0), against C medians of 254–305 and
99–114. Krylov is **15.9x and 19.1x smaller** at sigma=0.3 and ~2x smaller at
sigma=1.0. `KRYLOV-ALREADY-CAPTURES-REACHABILITY` fires in every cell of the ensemble.

## Verdict
Defect-certified clustering beats ordinary disorder binning **reproducibly, and at
sigma=0.3 by more than 2x** — and loses to plain Lanczos by up to 19x in the same
cells. The candidate is not defeated by the baseline it was designed against; it is
defeated by the baseline that was already there. That is the honest shape of the
result, and it is the same conclusion the CPU screen reached at N<=1024 and Arm 1
reached across three decades: the closed-system static-disorder route is CUT, and the
remaining opportunity is the open-system / non-Markovian sector.
