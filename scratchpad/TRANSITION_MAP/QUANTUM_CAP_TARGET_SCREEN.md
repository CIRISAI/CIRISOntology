# QUANTUM-SECTOR CAP TEST — target screen BEFORE buying instrument time (2026-08-23)

Motivated by NATURE_TEST_ANALYSIS.md L4: the caps (`shareK`, `bell_ceiling_exceeds_cap`)
are the one PHYSICS claim the programme owns and nature can adjudicate. Before any QPU
spend, screen whether the dark-state line supplies a usable target. Discipline: compute
the ceiling before buying the instrument (the S1-before-S7 spend rule).

## Finding 1 — dark states are the WRONG target, and by a wide margin
The C5 ring state's 5·log2 share comes from being **2-uniform**: every pair marginal
exactly maximally mixed, so the pair-envelope tops out at log 32 while the state itself
reads zero entropy. Measured deviation of each candidate's worst pair marginal from I/4:

| state (k=5) | max |pair marginal − I/4| | 2-uniform? |
|---|---:|---|
| C5 ring graph state | 0.0000 | YES (the witness) |
| GHZ | 0.2500 | no |
| W | 0.3500 | no |
| **twin dark state (our aspect mode)** | **0.7500** | **no — the farthest of all tested** |

A single-excitation dark state is a LOCALIZED two-term superposition: its pair marginals
are nearly pure (mostly |00>), which pins the global state and collapses the envelope.
It is not a near-miss for the cap — it is the opposite extreme from the witness.
**The dark-state programme therefore supplies no high-share target, and QPU time spent
preparing dark states to probe the cap would be wasted.** Recorded so the spend does not
happen.

## Finding 2 — a design constraint that binds ANY future cap experiment
Whole-only share is NOT readable from counts in a single measurement basis. Computed
here: the C5 ring state's computational-basis distribution is exactly UNIFORM, so its
single-basis classical share is **0.0000 nats** — all 3.466 nats of its quantum share is
invisible to one basis. The twin dark state likewise reads 0.0000. This is the founding
shape again (`pairwise_blind_to_parity`) and it means a hardware cap test REQUIRES
tomography or a designed multi-basis witness; a counts-in-one-basis protocol cannot
detect the quantity even in principle. Any proposal that budgets for single-basis shots
is mis-specified.

## What survives as the actual quantum-sector route
- Targets must be 2-uniform-or-near: graph/stabilizer states (C5 is the proven witness),
  absolutely-maximally-entangled families — NOT dark, W, or GHZ states.
- Protocol must be multi-basis (tomographic or witness-based), sized against the known
  QPU traps in the record: screen qubits by measured error, never trust published
  calibration (13x discrepancy on record), clip-vs-fold every readout.
- Prior result stands: 124/124 hardware readings obeyed the cap, never closer than 36%
  of it. A test worth running must be designed to approach the ceiling, not merely
  re-confirm compliance far below it.
- LIMITATION, stated: engineered hardware is not a WILD process, so this route tests the
  cap theorem but does NOT close the Stance's wild-quantum open question.

## Verdict
The dark-state line contributed a mechanism, an instrument, and a falsification — but it
does not reach the caps. The quantum-sector instrument, if built, must be built on
2-uniform states and multi-basis readout. Screening cost: minutes. Spend avoided: a QPU
campaign aimed at a target that provably cannot show the effect.
