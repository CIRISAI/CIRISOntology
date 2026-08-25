# Q8 MPS RESULTS — in progress

**This file is opened before any reading of the re-run is seen**, per chief-of-staff-2's binding
requirement: the classification table below is pre-registered now, verbatim in team-lead's terms,
and may not be reinterpreted after data exist.

## Pre-registered classification: the four outcomes of G3-primary's per-sweep history

Applied per configuration, crossing G7's convergence call against G3-primary's monotonicity clause
(`hist.windows(2)`, staked slack `1e-9`) on that configuration's `energy_history`:

| G7 | monotonicity | outcome |
|---|---|---|
| stall (`converged=false`) | non-monotone | **(a) oscillation** — promotes toward the CORRECTNESS KILL |
| stall (`converged=false`) | monotone | **(b) slow convergence** — stays a G7 VOID, Q9's stagnation premise intact |
| `converged=true` | monotone | **(c) claim upgraded to warranted** |
| `converged=true` | non-monotone | **(d) right-by-reference, convergence claim RETRACTED with an asterisk** — G2 (which compares against q-seam's exact ground state directly and does not depend on sweep history) may still pass; what is retracted is only the claim "this converged," never the physics |

**(d) is not to be reinterpreted post hoc.** The scope is ALL 8 configurations in the `N ∈ {8,10}`
grid (fence widened from the original 3 stalling ones, per chief-of-staff-2/research-manager: the
early-stop criterion `|E_k − E_{k-1}| <= sweep_tol` alone cannot distinguish a settled state from a
turning point of an oscillation for ANY configuration, not only the ones that visibly failed to
reach it).

G3-primary's own two clauses (floor, monotonicity) are graded for vacuity separately, per
research-manager's conjunction-vacuity discipline: if `worst_rise` sits at machine zero across all
8 configurations, the monotonicity clause was never exercised and G3-primary is graded
floor-only-effective, not two-clause; if `worst_floor_margin` is enormous everywhere, the floor
clause is the vacuous one. Reported with the actual numbers once the run completes.

## Provenance note on the discarded run

A `full_grid_gates` run launched 2026-08-24 07:31:23 (PID 1498505/1498515) was found, on direct
evidence, to predate every defect fix (G3-primary's `energy_history`, the per-spin-orbital
particle-hole anchor, the exact-reference cache): source files were modified 10:36:38–10:44:55 and
the binary rebuilt 10:45:08, all after the process's start time, and `/proc/1498515/exe` resolved to
the ORIGINAL binary file marked `(deleted)` — the kernel keeps a running process bound to the inode
it exec'd, unaffected by later rebuilds overwriting the path. That run is discarded; none of its
per-config panics are findings. Its raw DMRG diagnostics (E, sweeps, discarded weight) are not
reused either, to keep this results file backed by one coherent, fully-instrumented run rather than
a patchwork of two binaries.

## The re-run — COMPLETE, 30,098 s (8h22m), and the four-outcome table resolves cleanly

Recorded by the integrator after the campaign lanes had stood down; the run outlived the
session that launched it. Raw log committed alongside this file
(`output/q8_mps/full_grid_gates.log`) so the readings below are checkable rather than
quoted.

**The table, adjudicated against the four outcomes committed at `3123000` BEFORE any
reading existed:**

| config | sweeps | converged | monotone | outcome |
|---|---|---|---|---|
| N=8 U=0 | 5/20 | yes | yes | **(c)** convergence claim warranted |
| N=8 U=1 | 5/20 | yes | yes | **(c)** |
| N=8 U=4 | 5/20 | yes | yes | **(c)** |
| N=8 U=16 | 20/20 | no | **no** | **(a)** oscillation |
| N=10 U=0 | 20/20 | no | **no** | **(a)** |
| N=10 U=1 | 20/20 | no | **no** | **(a)** |
| N=10 U=4 | 20/20 | no | **no** | **(a)** |
| N=10 U=16 | 20/20 | no | **no** | **(a)** |

**THREE VERDICTS, none of which required a judgement call the table had not already
made.**

1. **The §7 SWEEP KILL FIRES: 5 of 8 VOID against a threshold of 2.** Already ruled
   fired pre-closeout on three configs; the completed run raises the count and changes
   nothing about the adjudication.
2. **CASE (d) NEVER FIRED.** No configuration is converged-and-non-monotone. The five
   monotonicity failures are exactly the five VOID configurations — the seductive case,
   fenced in advance precisely because it would have been reinterpretable after the
   fact, simply did not occur. Per the standing ruling, a G7-VOID configuration is not
   a gate datum (`Posed.adjudicate_void_iff`: VOID is the question never posed), so
   **the correctness kill does NOT fire.**
3. **THE THREE CONVERGED CONFIGURATIONS ARE UPGRADED** from unwarranted-by-criterion to
   warranted: they converge in 5 sweeps with monotone histories and zero discarded
   weight.

**What the stalls actually look like, because "oscillation" spans two very different
magnitudes here and the record should not flatten them.** N=10 U=4 rises by 7e-5 on an
energy of −25.38 with the exact reference matched to 3.5e-6 relative — near-converged,
failing its band by a hair. N=10 U=16 is the pathological one: energy error 1.4e-2,
|m_i| = 0.276, Sz = 0.127, Sz² = 0.368 — the partially-melted Néel signature, with spin
observables far outside their bands on an ansatz that is not symmetry-adapted and
therefore does not forbid them.

**Consequence for Q9, unchanged and still open.** Case (a) across every stall means the
stalls are oscillations rather than slow convergence, which is what put Q9's stagnation
premise in question in the first place. That question is NOT settled here: the
canonical-form / rank-deficiency check is the discriminator, and until it reports, the
honest statement is that Q9's premise is unconfirmed rather than refuted. Nothing in
this run licenses rewriting Q9's design; it licenses waiting for the check that was
built to decide it.

## Post-adjudication repair experiment — canonicality was the discriminator

**Status: repair evidence on `experiment/q-sota-adapter`, not a retroactive re-reading of the
completed grid.** The historical 5/8 VOID and SWEEP KILL above remain the result of the binary that
produced them. The independent q-seam/direct/TNC/TeNPy comparison then localized why that binary
failed, and the same configurations were replayed after the repair.

The one-sided Jacobi SVD stopped when the **absolute** off-diagonal norm of its column Gram matrix
hit the arithmetic floor. In strong-coupling DMRG, retained Schmidt columns span many decades, so
an absolutely tiny cross term can still be a large **relative** overlap after each column is
normalized. That produced the measured asymmetry: right singular vectors (accumulated rotations)
stayed orthogonal while left singular vectors (normalized working columns) did not. A later local
solve then treated a non-orthonormal block basis as orthonormal, so its ordinary effective
eigenproblem was no longer the variational problem DMRG intended.

The repair makes the SVD's stopping condition the maximum normalized pairwise column overlap,
transposes wide matrices before the one-sided solve, reorthogonalizes numerically degenerate
completions twice, and refuses to consume an SVD that misses its canonicality tolerance. A direct
two-sweep regression at `N=8,U=16,chi=32` failed before the patch with left overlap defect
`1.7995051073022862e-5`; it passes after the patch at `9.079312803079102e-15`.

Targeted replays (all cold-started from the pinned Neel state, fixed 20-sweep cap):

| configuration | old reading | repaired reading | exact error | canonical defect L/R |
|---|---:|---:|---:|---:|
| N=8 U=16 chi=64 | stalled, `delta E=1.4947e-2` | 5 sweeps, `E=-1.262136132207331` | `1.26952e-10` | `3.19e-14 / 1.25e-13` |
| N=8 U=16 chi=128 | stalled, `delta E~1.52e-2` | 5 sweeps, `E=-1.262136132335229` | `9.46e-13` | `6.06e-14 / 2.73e-13` |
| N=8 U=16 chi=256 | stalled, `delta E=7.4009e-3` | 5 sweeps, `E=-1.262136132335044` | `7.61e-13` | `6.17e-14 / 2.73e-13` |
| N=10 U=16 chi=256 | stalled, `E=-1.5804191287` | 5 sweeps, `E=-1.602785021944129` | `3.45e-12` | `2.32e-13 / 1.16e-12` |

Every repaired history is monotone within the staked `1e-9` slack. The independent direct
state-vector View still matches q8's reported energy within `2.4e-12` at `chi=32`; the reporting
boundary remains acquitted. At that intentionally truncated ledger, the remaining `8.35e-7`
energy error is comparable to the four TeNPy arms (`6.04e-7` to `7.19e-7`) and is removed by
`chi=64`.

One debt remains separate rather than smuggled into this finding: the diagnostic's worst local
Lanczos residual over *all* bond solves is `3.80e-8` at N=8 and `2.44e-7` at N=10, above its
early-exit heuristic even though the final states pass the exact Door. The hard 80-vector cap still
accepts its final Ritz vector and should acquire its own acceptance/restart gate. It is no longer a
candidate explanation for the Q8 oscillation: restoring canonicality alone changes the failed
high-chi energies to exact-seam agreement and restores monotone convergence.

The full eight-configuration grid has not been rerun on the repaired binary, so a new grid-level
adjudication is still owed. These targeted readings establish the causal repair; they do not erase
the earlier evidence or silently declare the historical SWEEP KILL unfired.
