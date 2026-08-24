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

## The re-run

Not yet run as of this commit. To follow in this same file once complete.
