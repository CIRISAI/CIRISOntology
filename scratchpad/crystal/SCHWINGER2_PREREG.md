# Pre-registration — SCHWINGER-2: the MPS rung, under convergence premises

**2026-08-27, frozen before the staked run; admissible only if the audit
exits 0.** SCHWINGER-1's conviction repaired at its named point: the same
Hamiltonian and the same exact referee (Schwinger 1962: M_V/g = 1/√π), now
at DMRG scale where the open chain holds the correlation length (at x = 16,
ξ ≈ 7 sites against N = 64 — a 9× margin where the ED campaign had 3×), and
with the new discipline as PREMISES: an unconverged ladder VOIDs, it never
extrapolates.

Instrument: two-site DMRG (White 1992; MPS-Schwinger tradition:
Bañuls–Cichy–Jansen–Cirac, credited), Coulomb term as a 6-channel MPO with an
accumulated-charge channel, sector control by λQ² penalty, excited state by
ground-state penalty projection. Dev-loop record, disclosed: three real
solver bugs found against dense/ED truth before any staked run —
broadcast-contaminated boundary environments, a transposed right-environment
leaving the effective operator non-Hermitian (tell: bond-dependent cycling
energies), and the sector-roaming global minimum that motivated the λQ²
channel. Final validation: DMRG reproduces exact ED including the projected
gap at 1.3e-14 (N=12, x=4) and 2.8e-12 (N=16, x=9).

defects: D-DET (deterministic computation, exact external referee), D-UNITS
(masses in units of g; x dimensionless).

gauge: scratchpad/crystal/gauge_dmrg.log

Family-wise: one staked arm.

## Frozen execution

`dmrg_schwinger.py staked`: x ∈ {4, 9, 16}; N ∈ {32, 48, 64}; χ ∈ {40, 64};
14 sweeps; λ = 20(x+1). Premises, each VOID-not-extrapolate:
- χ-convergence: |M(χ=64) − M(χ=40)| ≤ 1e-3 at every (x, N), else that point
  is flagged;
- N-convergence: |M(N=64) − M(N=48)| < 0.01 at each x, else that x VOIDs;
- fewer than 3 posable x ⇒ the campaign VOIDs (never a pass by shrinkage).
Extrapolation ladder (frozen): per-x linear fit in 1/N over {32, 48, 64};
then linear in 1/√x.

| arm | stake (numeric) | witness: | posability |
|---|---|---|---|
| S1 the vector mass | extrapolated M_V/g within **1/√π ± 0.05** | witness: none — the referee is Schwinger's exact solution; a miss convicts the chain at ITS scope, as SCHWINGER-1's did | SCHWINGER-1 measured the observable moving 0.30–1.13 across the grid; the planted MPO mutation moves it > 0.02 (gauge_dmrg.log); the premises can genuinely VOID |

Exits: CONFIDENCE — rungs 3–4 of the lepton ladder stand at MPS scale: the
mesh's gauge-fermion chain reproduces Schwinger's bound-state mass.
FALSIFICATION — the repaired chain is convicted too, and the ladder's rung 3
needs a different formulation, not a bigger lattice. VOID — the premises
fired; the run is not evidence either way and says so.
