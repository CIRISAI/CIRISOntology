# REG+ exact three-particle coherence survival — preregistered result

Parent prereg: `7f7949d73261e037164948bb5f05a38657c97a08`
Pre-execution domain erratum: `ca8cdbd50c391beae85300923906d5500e52b775`

## Frozen verdict

**ROBUST-MEMORY.**

At Phi=30 degrees, theta=1.30, on the exact N=3 hard-core Fock sector of the 5x5
six-carry torus, all 144 admissible spectator modes were run.

The no-spectator exact bridge reference is:

`M2 = 0.3333452470`.

All-placement results:

- median M3 = 0.3333452470
- 10th percentile = 0.1367428879
- 90th percentile = 0.3333452470
- fraction M3 > 0.20 = 0.833333
- fraction M3 < 0.05 = 0.055556
- mean M3 = 0.2941735004
- minimum M3 = 0.0107292629

The preregistered ROBUST-MEMORY criteria are met.

## Contact stratification

Ballistic CONTACT placements: 120

- median M3 = 0.3333452470
- fraction >0.20 = 0.800000
- fraction <0.05 = 0.066667
- minimum = 0.0107292629

NO-CONTACT placements: 24

- every placement returns exactly M3 = M2 = 0.3333452470

Thus ordinary local interactions can attenuate route memory for special spectator
worldlines, but one spectator does not generically erase it.

## Mechanical gates

- all 144 corrected-domain placements present
- max state-norm error = 1.998e-15
- exact total particle number N=3
- marginalized origin head-on probabilities satisfy the probability bound

## Interpretation

This materially weakens the idea that the local Born/dephasing boundary in the existing
hydrodynamic model can simply be justified as automatic self-dephasing from one extra
environmental degree of freedom.

The result remains finite-sector model physics. It does not yet say that macroscopic
many-body REG remains coherent. The next discriminating variable is environmental
occupancy/density: add multiple exact spectators and measure the survival curve of the same
route-memory witness before attempting a coherent hydrodynamic closure.
