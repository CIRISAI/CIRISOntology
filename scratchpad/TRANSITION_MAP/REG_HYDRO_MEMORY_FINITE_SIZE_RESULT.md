# REG+ route-memory finite-size scaling — preregistered result

Prereg: `897401d6b4115011c2b98ac24f1a0d1e8a81e5cb`

## Frozen verdict

**COMPUTE-LIMIT.**

The required L=7 HIGH cell (N=31, density 0.63265 particles/site, 7-cycle return) hit the
exact sparse support cap in 5 of 16 frozen configurations = 31.25%, exceeding the
preregistered >25% compute-limit threshold. Therefore no density-scaling classification is
issued, and L=9 was not executed after the gate fired.

Readable L=7 cells:

- LOW N=20, d=0.40816: median M=0.085881, 31.25% below 0.05 — not LOW-MEMORY.
- MID N=25, d=0.51020: median M=0.038276, 62.5% below 0.05 — LOW-MEMORY.
- HIGH N=31: 11/16 configurations readable; among those, median M=0.012349 and 100% are
  below 0.05, but this is descriptive only because the cell failed the compute gate.

The compiled exact runner was cross-checked against the independently completed Python
L=7 LOW cell and reproduced its median, mean, and threshold fractions to displayed
precision before being used on the heavier cells.

## Interpretation

The exact fully coherent state space becomes combinatorially large precisely near/above the
apparent memory-loss region. This prevents an exact finite-size scaling claim with the
present sparse-state representation. It is not evidence for or against density scaling.

The next earned method is a controlled many-body approximation benchmarked on all exact
readable cells: it must reproduce the N=2 bridge, N=3 spectator distribution, the 5x5 density
ladder, and the L=7 LOW/MID cells before being trusted at L=7 HIGH or L=9. Any truncation
error must be exposed as a named number rather than hidden.
