# GPU annihilating-MC — the 4090 plan (2026-08-22)

Hardware verified: RTX 4090 Laptop, 16 GB VRAM, CuPy installed.

## The challenge, honestly

Exact Fock enumeration grows exponentially with lattice/occupancy (1.78e6 reachable at
L=7 N=31); 16 GB buys ~1e8-1e9 resident amplitudes — possibly exact L=9 LOW/MID
(reachable-set growth curve requested from the primary workstream), never universality.
GPUs sell constant factors against an exponential.

## The real target: walker count in the licensed annihilating estimator

Two compounding wins: variance ~ 1/sqrt(W), AND annihilation efficiency RISES with
walker density (more same-configuration coherent cancellation per cycle — the
sign-problem cure strengthens with scale). CPU-licensed W=10,000 -> GPU W ~ 1e6-1e7.
Consequences: the four held-out cells run with wide SE margins; L=11 opens; N_c gets a
three-point finite-size-scaling ladder.

Implementation shape (GPU-native): bit-packed uint64 configuration keys; per-walker
parallel collision sampling (q_k=|u_k|^2, weight update u_k/q_k); annihilation =
sort-by-key + segmented complex reduce; resampling by prefix sums. Sort/memory-bound, so
laptop-4090 fp64 weakness is irrelevant; gates use fp64 accumulators.

## Discipline (binding)

A GPU port is a NEW IMPLEMENTATION: the frozen benchmark cascade re-runs in full, the
license is issued at the new W BEFORE any held-out execution, and W is fixed
pre-inspection per the frozen prereg. This build IS the independent concordance
reimplementation staked in ANNIHILATING_MC_EXECUTION_NOTE.md — written from the frozen
prereg text, blind to the primary's target numbers. One build, both purposes.

## Tensor-network caution, filed now

TN truncation error correlates with the measured phase: low-memory = scrambling =
volume-law entanglement = MPS/PEPS fail exactly where the answer is "memory lost". A TN
instrument's bias points along the measurement axis. Not the first tool; usable later
only with that confound explicitly designed for.

## CORRECTION (2026-08-22, supervisor-measured): annihilation power is walkers-per-CONFIGURATION

The note's premise — annihilation efficiency rises with walker density — is right in W
and WRONG IN THE CELL. Measured at W=1e6: L=7 LOW ~4,000 walkers/config (hence 5e-4
errors); L=9 HIGH ~1.3; L=11 ~1.5. At L=9 HIGH there is essentially nothing to annihilate
and the estimator degenerates toward the already-failed path-MC. VRAM tolerates W~2e7 =
only ~26/config there. The 100x walker increase does NOT rescue L=9 HIGH; if that cell
fails readability it is TARGET-STATISTICALLY-UNCONTROLLED per the frozen prereg, honestly,
and a different representation (not more walkers) is the successor question.
