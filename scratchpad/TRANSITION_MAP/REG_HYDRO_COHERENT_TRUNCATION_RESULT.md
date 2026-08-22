# REG+ coherent truncation — target result

Prereg: `bbf5d30f12f645caa28201b09ed23c9001e2b100`
Budget license: `109862a89884dbda3e5f7b9d5c5da0f4113b26dd`

## Frozen budget selection

All four candidate budgets passed the exact L=7 LOW/MID accuracy gate. The frozen selection
rule therefore licensed the largest passing budget:

`delta_step = 1e-3`.

This selection was recorded before any HIGH or L=9 approximate target outcome was inspected.

## Target verdict

**APPROXIMATION-UNCONTROLLED**

The L=7 HIGH target fails both independent READABLE gates immediately.

Among the first four frozen target configurations:

- completed coherent-arm B values are approximately 0.2197, 0.2142 and 0.1888, all above
  the frozen target maximum B=0.15;
- target configuration 2 has 5,626,213 basis states before truncation and 2,605,507 retained
  states afterward, exceeding the frozen retained-support cap of 2,000,000.

Because a READABLE target requires all 16 runs to finish under the support cap and satisfy
the B control bands, this cell is irreversibly unreadable under the licensed approximation.
Execution was stopped once the frozen verdict became mathematically unrecoverable.

No smaller delta may now be substituted: the prereg explicitly fixed the largest passing
benchmark budget before target inspection. L9 was therefore not opened, because the
finite-size scaling criterion already cannot be satisfied.

## Interpretation

The norm-budgeted amplitude-pruning approximation is accurate on the exact benchmark cells
but does not remain controlled in the harder coherent target regime. Approximation-control
difficulty grows precisely where many-body route support proliferates.

This is a negative numerical-method result, not a failure of the underlying coherent REG
model. The next representation should preserve locally generated entanglement structurally
rather than discarding basis amplitudes by magnitude; a tensor-network / locally entangled
ansatz is the natural next candidate, with this failed truncation arm retained as a
deflation control.
