# Pre-registration — SCHWINGER-1: rungs 3–4 of the lepton ladder

**2026-08-27, frozen before the staked run; admissible only if the audit
exits 0.** The crystal programme's first campaign: gauge-coupled lattice
fermions with an EXACTLY KNOWN kill. The massless Schwinger model (QED₂) in
the Hamer–Kogut spin formulation on an open staggered chain, gauge field
eliminated; sparse ED in the charge-zero sector. Schwinger's closed form is
the referee: the vector boson mass M_V/g = 1/√π = 0.564190.

Credits: Schwinger 1962 (the exact solution); Banks–Kogut–Susskind and
Hamer–Kogut (the lattice Hamiltonian); Hamer et al. (the ED tradition this
instrument follows); Jordan–Wigner via the same exchange-statistics floor the
lake proves (`composite_exchange_sign` — statistics is a composition rule).

defects: D-DET (exact deterministic computation; the referee is a closed
form), D-UNITS (masses in units of g; dimensionless x = 1/(ga)²).

gauge: scratchpad/crystal/gauge_schwinger.log

Family-wise: one staked arm; the condensate is reported EXPLORATORY and
unstaked (its continuum subtraction is a known subtlety; no band is claimed).

## Frozen execution

`schwinger.py staked`: x ∈ {4, 9, 16}, N ∈ {12, 14, 16, 18, 20}; at each x a
linear fit in 1/N over N ∈ {16, 18, 20}; then a linear fit in 1/√x. All
frozen here, no alternatives.

| arm | stake (numeric) | witness: | posability |
|---|---|---|---|
| S1 the vector mass | extrapolated M_V/g within **1/√π ± 0.05** | witness: none — the referee is Schwinger's exact solution, and a miss convicts OUR lattice-and-extrapolation chain, stated as such | raw readings sit far from target (0.948 at x=9, N=12 — the extrapolation carries real weight and can genuinely fail); both planted mutations move the observable by > 0.22 (gauge_schwinger.log); three analytic plants pass |

Exits: CONFIDENCE — the mesh's gauge-fermion chain produces the right bound
state mass from Schwinger's own physics: rungs 3–4 of the lepton ladder stand.
FALSIFICATION — the chain (formulation, sector, or frozen extrapolation
ladder) is convicted at stated scope; no rescue, and the diagnosis goes to the
next freeze, not this one.
