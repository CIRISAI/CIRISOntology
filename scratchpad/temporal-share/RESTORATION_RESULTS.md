# RESTORATION — results. **RESTORATION FAILS.**

The headline is fixed by the prereg (§5, §6) and honored: **the enlarged view did NOT
restore closure where the theory said it must. The recursion claim takes damage on this
substrate.** Job `da7gslrsq5js73bjunl0`, `ibm_marrakesh`, pair (95, 99), frozen design
`RESTORATION_PREREG.md`. **Cost 11 s; campaign total 57 s, 543 s remaining.**

## The readings, against the frozen predictions

| arm | `Δ_A→B` | `Δ_B→A` | `Δ_joint` | floor | predicted joint | measured |
|---|---|---|---|---|---|---|
| **J** (`XXPlusYY`, conserves n ideally) | 1.09e-2 | 1.27e-2 | **5.93e-2** | 5.63e-4 | AT floor | **OPEN, 105×** |
| **R** (`CRX` both ways) | 9.37e-2 | 1.60e-2 | 9.93e-2 | 6.18e-4 | above (≈0.034) | **OPEN, 161× — as predicted** |

Both arms' marginals are above floor (the couplings took — MARGINALS SURVIVE did not
fire), and arm R behaved exactly as predicted, so **the discriminating power was real:
JOINT CLOSURE IS GENERIC did not fire either.** The failure is arm J's alone, and it is
the informative one.

## Post-hoc diagnostic (labelled as such; existing data, no new quota)

The same joint statistic computed on the PILOT and τ-SWEEP data separates the mechanism:

| condition | `Δ_joint` | ×floor |
|---|---|---|
| idle, τ = 64 ns (prep + readout only) | 1.17e-3 | 1.9 |
| **arm J, gate applied** | **5.93e-2** | **105** |

**The gate itself breaks n-conservation, by ~50× over the prep/readout baseline.** The
transpiled `XXPlusYY` on this backend is not an excitation-preserving channel at the
few-percent level — an ideally-conserving unitary decomposed into non-conserving native
gates conserves only as well as its calibration.

**Bonus finding, worth its own line: the idle joint residual GROWS with τ** — 7.5e-4 at
64 ns → 1.16e-2 (19× floor) at 65.5 µs. That is T1 asymmetry: amplitude damping does not
conserve n, and the two qubits decay at different rates, so `P(n_out|01)` and
`P(n_out|10)` separate with time. **The n-fiber statistic detects a dynamical asymmetry
the τ-sweep's marginal statistics read as borderline (1.2×) at best.** The fiber view is
the more sensitive instrument — measured, not asserted.

## What is damaged and what is not

- **Damaged, as staked:** "refinement restores closure" as a hardware-realizable claim
  on this device, this gate set, this view. No rescue: the prereg staked the hardware
  test, and the hardware test failed.
- **Not damaged:** `gauss_held` and the Lean 2×2 — theorems about the model map, which
  the hardware channel is not. The diagnostic shows the physical channel splits fibers
  the ideal gate preserves; in the ladder's terms, noise acts on the FIBER level and the
  test measured exactly that.

## Follow-up owed (a successor prereg, not this file)

Readout-mitigated, gate-characterized retry — or a platform where the conserving gate is
native. The joint view must be tested against a channel whose n-violation is bounded
BEFORE the arm is staked; this run measured that bound for free.

## No rescue

One job (client wait timed out; result fetched by id, never resubmitted). No refits, no
dropped preparations, statistic unchanged. Verdict reported as the frozen rule returned it.
