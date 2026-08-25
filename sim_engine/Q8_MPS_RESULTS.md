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
