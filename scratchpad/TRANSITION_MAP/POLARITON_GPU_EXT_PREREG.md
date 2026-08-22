# POLARITON GPU EXTENSION (PGX-1) — preregistered, FROZEN 2026-08-23 before any code or number

Extension of `POLARITON_SOFTSYM_BENCH_PREREG.md` to the regimes a CPU CI runner
cannot reach. It does NOT re-score the CPU benchmark and cannot change its verdict:
the frozen CPU screen stands on its own runner. This adds three arms the CPU screen
could not run, on an RTX 4090.

## THE FAIRNESS RULE (binding, stated first)
A GPU must EXTEND THE REGIME, never WIN THE COMPARISON.
- ALL arms (truth, Krylov A, binning B, defect-clustering C) run on the SAME
  hardware in the same precision. No cross-hardware timing comparison is admissible.
- PRIMARY METRIC IS HARDWARE-INDEPENDENT: minimal reduced dimension reaching the
  frozen tolerance (and matvec count for Krylov). Wall time is reported as
  secondary/descriptive ONLY and may never carry a verdict.
- Any result that would flip if the hardware changed is void by construction.

## Frozen model constructions (inherited verbatim from the CPU prereg)
wc = 0; uniform gi = 1/sqrt(N) so collective G = 1; wi ~ Normal(0, sigma);
initial state |c>; times linspace(0,20,201); tolerance RMSE <= 1e-4 on P_c(t);
Krylov m grid {2,4,6,8,12,16,24,32,48,64,96,128}; bin grid B powers of two capped
at N (extended to 256, 512, 1024 for the larger N here); tau/G grid
{0,0.001,0.003,0.01,0.03,0.1,0.3,1,3}. Clustering rule unchanged: sort by wi,
greedy contiguous clusters of frequency diameter <= 2 tau (so certified pairwise
g_DB <= tau), each replaced by one effective emitter at the coupling-weighted mean
frequency with aggregate coupling sqrt(sum gi^2).

## Truth and its gates (the enabling method, declared before use)
GPU truth is Chebyshev-in-time propagation of the arrowhead H with step-adaptive
order, order raised until the state changes by < 1e-12 (self-convergence).
- G1: at N in {1024, 4096} the GPU truth must match scipy `expm_multiply`
  (the CPU screen's T0 truth) to max |dP_c| < 1e-10. FAIL ⇒ arms void.
- G2: at sigma = 0 the exact two-state cavity/bright reduction must match GPU
  truth to RMSE < 1e-12 at every N. FAIL ⇒ arms void.
- G3: float64 throughout; any arm run in reduced precision is void.

## ARM 1 — the N ladder (extends P5 by three decades)
N in {1024, 4096, 16384, 65536, 262144, 1048576}; sigma in {0.1, 0.3, 1.0, 3.0};
seed 20260823 + index. Report minimal reduced dimension for A, B, C per cell.
- STAKE E1: C's minimal cluster count stays within +/-20% across the FULL ladder at
  fixed sigma ⇒ N-INDEPENDENT COMPRESSION CONFIRMED AT SCALE. Any cell outside ⇒
  N-independence fails at scale (and the CPU screen's 2-decade window was too short
  to see it). Reported per sigma; no averaging across sigma.

## ARM 2 — the disorder ensemble (the CPU screen's single-seed gap)
N in {4096, 16384}; sigma in {0.3, 1.0}; R = 64 independent realizations
(seeds 20260823000 + r). For each realization record minimal reduced dimension for
B and C.
- STAKE E2 (the decisive one): C earns CONTINUATION only if the PAIRED median of
  (B_min / C_min) >= 2.0 AND a two-sided sign test over the 64 pairs rejects
  equality at p < 0.01. Beating B on a single draw is NOT sufficient — the CPU
  screen's P3 tests one realization and its primary score is a random variable.
- STAKE E3: if median(A_min_matvec_dimension) <= median(C_min) then
  KRYLOV-ALREADY-CAPTURES-REACHABILITY holds AT SCALE (the CPU P4 verdict extended).

## ARM 3 — the two-excitation sector (run only if Arms 1-2 complete)
N in {128, 256, 512}: basis {2 photons} + {1 photon, 1 emitter} + {2 emitters},
dimension 1 + N + N(N-1)/2. Initial state = 2 photons. Same tolerance and grids.
- STAKE E4: does the ordering of B vs C found at one excitation PERSIST into the
  two-excitation sector? A reversal (C loses at 1, wins at 2) localizes the
  opportunity to the multi-excitation sector — a real finding either way.
- Descriptive only if truth gates fail at these dimensions; no verdict from a
  failed-gate arm.

## Staked meanings (frozen)
- E2 FAILS (expected direction, stated in advance): defect-certified near-twin
  clustering is BASELINE-EQUIVALENT to ordinary disorder binning at scale and with
  statistics. The soft-symmetry compiler idea is then CUT for closed-system static
  disorder, and the remaining opportunity is the open-system / non-Markovian
  sector the literature already names. This is a useful negative and will be
  reported as plainly as a positive.
- E2 PASSES: continuation is bought for the open-system benchmark ONLY, still with
  no SOTA claim: beating a binning baseline on a model TC Hamiltonian is not
  beating MPS-HEOM, CUT-E, or PIQS, and no document may say otherwise.
- E1 FAILS while E2 PASSES: the compression is real but N-dependent; any claim must
  carry the N range it was measured in.
- No Stance change, no physics-world claim, no simulation-SOTA claim follows from
  any outcome of PGX-1.
