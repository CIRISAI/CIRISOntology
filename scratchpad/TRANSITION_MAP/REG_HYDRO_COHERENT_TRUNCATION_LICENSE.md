# REG+ coherent truncation benchmark — licensed budget

Parent prereg: `bbf5d30f12f645caa28201b09ed23c9001e2b100`

**Status: LICENSED BEFORE TARGET EXECUTION**

The four frozen per-step discarded-probability budgets were benchmarked against the exact
paired L=7 LOW (N=20) and MID (N=25) configuration lists. No HIGH or L=9 approximate target
outcome was inspected before this selection.

| delta_step | median abs M error | p90 abs error | max abs error | LOW class | MID class | max B (benchmark) |
|---:|---:|---:|---:|---|---|---:|
| 1e-8 | 1.11e-16 | 5.54e-9 | 2.08e-8 | not low-memory | low-memory | 0.000494 |
| 1e-6 | 1.06e-7 | 9.79e-7 | 8.23e-6 | not low-memory | low-memory | 0.004990 |
| 1e-4 | 5.94e-5 | 2.65e-4 | 6.22e-4 | not low-memory | low-memory | 0.059479 |
| 1e-3 | 8.48e-4 | 2.45e-3 | 5.32e-3 | not low-memory | low-memory | 0.219577 |

All four satisfy the preregistered accuracy/classification gate:
- median abs error <= 0.005
- p90 <= 0.010
- max <= 0.030
- LOW remains not low-memory
- MID remains low-memory.

The frozen selection rule therefore licenses the **largest passing budget**:

`delta_step = 1e-3`.

The relatively large benchmark B at this budget does NOT disqualify licensing because B is
not part of the frozen benchmark acceptance gate. It is, however, a warning for the separate
target-cell READABLE gate: every target cell must independently have median B <= 0.05 and
maximum B <= 0.15 in both coherent and branch arms. Failure there is
`APPROXIMATION-UNCONTROLLED`, not a reason to choose a smaller budget after seeing targets.
