# REG+ norm-budgeted coherent truncation — preregistration

**Status:** FROZEN BEFORE EXECUTION
**Date:** 2026-08-22

## Purpose

Exact fully coherent sparse evolution became support-limited in the preregistered L=7 HIGH
finite-size cell. This experiment introduces a controlled approximation that preserves
complex amplitudes and route interference while making every discarded component explicit.
It is not a Born/dephasing closure.

## Frozen microscopic law

Identical to the exact finite-size experiment:
- six hard-core directional carries
- theta=1.30 rad
- Phi=30 degrees
- exact local conservation-sector unitaries
- exact carries permutation
- coherent and initially-dephased arms
- same origin head-on-pair TV witness M.

Only the representation after a completed global collision is approximated.

## Truncation rule

After each global collision step, sort basis configurations by probability mass |a_i|^2
ascending. Remove the largest possible set of smallest components whose total removed
probability mass is <= delta_step. Do NOT renormalize. Continue the subsequent exact linear
unitary evolution of the retained subnormalized state.

Apply the same deterministic rule separately to the coherent state and each dephased-branch
state. Ties are broken lexicographically by the basis configuration.

Record at every step:
- support before and after truncation
- removed probability mass delta_t
- retained norm
- cumulative removed mass sum(delta_t)
- cumulative state-vector error budget B=sum_t sqrt(delta_t).

No amplitude may be removed except by this rule.

## Candidate budgets

Benchmark all four per-step budgets:
- 1e-8
- 1e-6
- 1e-4
- 1e-3

No other budget may be introduced after target-cell outcomes are inspected.

## Benchmark data — exact only

Use the exact frozen L=7 configuration lists already generated under prereg
`897401d6b4115011c2b98ac24f1a0d1e8a81e5cb`:

- LOW: L=7,N=20,16 configurations
- MID: L=7,N=25,16 configurations

The exact M values are the reference. HIGH and all L=9 outcomes are forbidden during budget
selection.

For each budget over the combined 32 benchmark configurations report:
- median absolute |M_approx-M_exact|
- 90th percentile absolute error
- maximum absolute error
- sign agreement for the binary LOW-MEMORY cell classification when aggregated per cell
- median and maximum B.

## Budget acceptance gate

A budget PASSES only if all are true:
- median absolute M error <= 0.005
- 90th percentile absolute M error <= 0.010
- maximum absolute M error <= 0.030
- LOW remains not LOW-MEMORY
- MID remains LOW-MEMORY.

Select the **largest** candidate delta_step that PASSES. This selection rule is frozen before
any HIGH/L9 approximate outcome.

If no budget passes, verdict APPROXIMATION-NOT-LICENSED and stop.

## Target execution after licensing

Only after a budget is licensed, run the frozen target configuration lists:
- L=7 HIGH, N=31, all 16 configs including the five exact support-capped cases
- L=9 LOW N=32, MID N=42, HIGH N=52, 16 configs each.

Use the same finite-size classification from prereg `897401d6...`:
DENSITY-SCALING-SUPPORTED only if LOW is not low-memory and HIGH is low-memory at both L=7
and L=9. MID is diagnostic.

An approximate target cell is READABLE only if:
- all 16 runs finish under a hard retained-support cap of 2,000,000, and
- median B <= 0.05 and maximum B <= 0.15 in both coherent and branch arms.
Otherwise classify that cell APPROXIMATION-UNCONTROLLED; it cannot support density scaling.

## Standing exclusions

This is a controlled numerical approximation to a finite coherent lattice model. Passing
benchmark error bands does not prove convergence in the thermodynamic limit. The discarded
norm and B are mandatory outputs; no target inference may hide or optimize them.
