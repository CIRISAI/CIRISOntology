# REG+ exact route-memory density ladder — preregistered result

Prereg: `b6438126a21e70bc264cc5dfe5c4d35e0cf7954b`

## Frozen verdict

**DENSITY-SENSITIVE.**

The established anchors were not refit:

- N=2: M2 = 0.3333452470
- N=3: median M3 = 0.3333452470

The new exact sparse 64-configuration levels are:

| total N | median M | mean M | p10 | p90 | frac M>0.20 | frac M<0.05 |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.333345 | 0.256856 | 0.010729 | 0.333345 | 0.703125 | 0.125000 |
| 5 | 0.333345 | 0.225210 | 0.010729 | 0.333345 | 0.578125 | 0.171875 |
| 6 | 0.147472 | 0.197708 | 0.010729 | 0.333345 | 0.468750 | 0.218750 |

At N=6 the median is below the ROBUST-THROUGH-N6 threshold of 0.20 but remains well above
the COLLAPSE-BY-N6 threshold of 0.05, so the preregistered classification is
DENSITY-SENSITIVE.

The medians are non-increasing from N=3 through N=6, but the distribution remains broad:
some configurations preserve the full two-particle witness while some fall to about
0.01073. This is not a uniform decoherence process at this occupancy.

## Origin-pair support

Median marginalized origin-pair support remains essentially 1 through N=5. At N=6 it falls
to about 0.8651 in both coherent and dephased arms. Thus part of the N=6 change is physical
redistribution out of the returning head-on-pair subspace, but the named TV witness is
computed on the same marginal in both arms and remains the frozen primary measure.

## Mechanical gates

All 64 configurations at each of N=4,5,6 completed. No COMPUTE-LIMIT occurred.
Maximum state-norm error over all runs was below 2.9e-15. Exact total particle number and
hard-core occupancy were preserved.

Maximum sparse supports were only 9, 17, and 21 basis configurations at N=4,5,6
respectively, because the five-cycle window is short and most random spectator worldlines do
not generate repeated route-branching collisions.

## Secondary descriptive fits

Across the four median points N=3..6:

- exponential M_N=A exp[-gamma(N-3)]: A=0.39240, gamma=0.24466, RSS=0.01445
- affine floor M_N=M_inf+B/(N-2): M_inf=0.20943, B=0.14870, RSS=0.01843

These four-point fits are descriptive only and are not promoted as laws.

## Interpretation

One extra spectator is insufficient to generically erase coherent route memory, but rising
occupancy begins to matter by N=6 on the 5x5 torus. The next discriminating object is the
collapse scale at higher exact occupancy, under a separately frozen extension. This remains
finite-lattice model physics and does not establish a thermodynamic decoherence law or a
many-body coherent fluid.
