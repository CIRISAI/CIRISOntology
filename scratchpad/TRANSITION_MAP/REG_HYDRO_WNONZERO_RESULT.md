# REG+ coherent holonomy transport — preregistered result

Prereg commit: `371854bfb3a65bba44f7106d1b4ae0509a252ca7`

## Frozen primary verdict

At rho=2.0, theta=1.30 rad, on both N=192 and N=256:

- `Delta g(Phi)`: **NULL**. Maximum absolute shift is below 1e-4, against the frozen 0.03 band.
- `Delta nu(Phi)`: **COHERENT-HOLONOMY**.
- At Phi=90 deg, N=256:
  - nu(0) = 0.2327317
  - nu(90) = 0.1898479
  - Delta nu = -0.0428838
  - annealed-dephasing nu = 0.2137097
  - fixed-90 minus dephasing = -0.0238618
- Adjacent 60/90/120-degree bins cross the 0.005 band with the same sign.
- The 192->256 shifts agree to much better than the prereg refinement tolerance.
- All long-wave viscosity fits remain R^2 ~ 1; this is not a fixed-point-destroyed outcome.

## Secondary rho=2.5 replication

The same frozen family reproduces the pattern:

- Delta g remains null.
- At Phi=90 deg, N=256:
  - nu(0) = 0.1857690
  - nu(90) = 0.1554697
  - Delta nu = -0.0302993
  - annealed-dephasing Delta nu = -0.0150647
  - fixed-90 minus dephasing = -0.0152346

## Mechanism-level reading

The local 3-route sector transition is unistochastic/bistochastic at every loop phase, so
the conserved equilibrium manifold is unchanged. The Euler-level convection coefficient
therefore stays fixed within sensitivity. Holonomy changes the non-conserved relaxation
spectrum instead:

- Phi=0 or pi: nontrivial local transition eigenvalues about -0.150622
- Phi=pi/2 or 3pi/2: about -0.488825

Correspondingly, at rho=2, N=256,

`Delta nu(Phi) ~= -0.04889 sin^2(Phi) + 0.00604 sin^4(Phi)`

with RMSE about 3.1e-5 over the frozen 12-point phase grid.

## Classification

This is a **model-physics transport result only**. It does not establish world-physics,
does not identify ontology kinds with physical degrees of freedom, and does not alter the
flatness theorem for verdict-producing grammars. The tractable model locally dephases after
each coherent collision; multi-step globally coherent carries remain untested.
