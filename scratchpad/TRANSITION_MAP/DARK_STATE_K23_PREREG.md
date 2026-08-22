# DARK-STATE K2.3 PREREG — open the bright sector, measure the quasi-dark linewidth

Frozen 2026-08-22 before `dark_state_k23.py` exists or any K2.3 number is read. K2.3 was bought by the K2 spend rule: both Str/Cir continuations leave the weak-breaking regime early and enter strong branch competition, while Pri/Prc is substantially smoother.

## Physical question and boundary

This is the controlled open-system analogue of the exact twin dark state. Symmetry-protected photonic BICs become quasi-BICs when symmetry breaking opens a radiative channel; in the perturbative radiative-loss regime their linewidth is quadratic in the asymmetry (equivalently `Q ~ alpha^-2`). That law is established prior art, not ours. Current molecular-polariton work likewise treats disorder-driven activation of dark/gray states and bright→dark transfer as a central determinant of large-N dynamics.

K2.3 asks only whether the **measured K11 symmetry-breaking directions** exhibit the same controlled mathematical regime, and where they depart from it. No claim is made that the semantic Hamiltonian is a photonic material or molecule.

Prior-art anchors to credit in the results:

- Röntgen, Morfonios & Schmelcher, Phys. Rev. B 97, 035161 (2018): local permutation symmetry, compact localized states, symmetry block partitioning.
- symmetry-protected quasi-BIC inverse-square law: e.g. contemporary BIC literature and the 2025 Light: Science & Applications treatment of permittivity-asymmetric qBICs.
- Li, Venkatesh, Shi & Montoya-Castillo, arXiv:2603.06868 (2026): molecular polariton thermodynamic convergence under static/dynamic disorder, bright→dark transfer, MPS-HEOM.

## Inputs

Exactly the K2 objects, no new fitted matrix:

`H0 = (H + P H P)/2`

`Vodd = (H - P H P)/2`

`H(s) = H0 + s Vodd`

for both CUR-P2/CUR-SP and both twin pairs. `d` is the exact normalized antisymmetric twin dark vector. All energies/rates use the PHYS-K11-1 A2 unit (mean off-diagonal channel strength = 1).

## Open channel

At `s=0`, diagonalize the P-even bright block of `H0`. Let its eigenvectors/eigenvalues be `|b_j>, E_j`, with exact dark energy `E_d`.

Open **every bright eigenmode equally** to an absorbing continuum with rate `kappa`, leaving the dark projector untouched:

`H_eff(s,kappa) = H(s) - i (kappa/2) Q_B`,

where `Q_B = I - |d><d|`.

This is a resonance / no-return sink model. It is deliberately simpler than a molecular bath. Its purpose is to test the quasi-dark linewidth and the resonance denominator without introducing bath fitting.

For each `(s,kappa)`, identify the eigenvalue of `H_eff` whose right eigenvector has maximum normalized overlap with `d`; define

`Gamma(s,kappa) = -2 Im lambda_dark`.

If branch identity becomes ambiguous (largest two dark overlaps differ by <0.05), mark that cell BRANCH-AMBG rather than smoothing through it.

## Parameter-free weak-breaking prediction

Write `v_j = <b_j|Vodd|d>`. Standard second-order elimination of lossy bright modes predicts the **population linewidth** coefficient

`C(kappa) = sum_j |v_j|^2 kappa / ((E_d-E_j)^2 + (kappa/2)^2)`

and therefore

`Gamma(s,kappa) = s^2 C(kappa) + O(s^4)`.

This is frozen before the numerical linewidths are generated. The factor convention is fixed by the `-i kappa/2` term above; changing it after execution is forbidden.

## Grid

- `s = 0` plus 41 log-spaced points from `1e-5` to `1e-1`, then `{0.15,0.2,0.3,0.5,0.7,1.0}` for departure mapping.
- `kappa in {0.1, 0.3, 1.0, 3.0, 10.0}`.

The primary prediction tier is `s <= 1e-2`; larger `s` is diagnostic only.

## Stakes / gates

### O1 exact protection
At `s=0`, `Gamma=0` to numerical floor for every pair, arm and kappa. Failure = implementation defect.

### O2 quadratic opening
For each nondegenerate cell family, the log slope of `Gamma` vs `s` over the weak tier is `2 +/- 0.01`. Failure outside a declared floor/branch ambiguity = model failure or implementation defect, adjudicated by O3.

### O3 coefficient prediction — strongest gate
For `s <= 1e-2` above numerical floor,

`Gamma(s,kappa)/(s^2 C(kappa))`

must approach 1. Primary score: median absolute fractional error over the weak tier. PASS if <= 1%; 1–5% = MARGINAL; >5% = FAIL. Report every kappa/pair/arm separately; no averaging may rescue a failed family.

### O4 resonance/Zeno profile
`C(kappa)` itself is computed before the nonlinear sweep and reported. A near-resonant bright denominator should shift the kappa at which linewidth is largest; in the large-kappa limit the coefficient must fall approximately as `1/kappa` (absorptive/Zeno suppression). This is a model diagnostic, not a discovery stake.

### O5 measured-endpoint departure
At `s=1`, report `Gamma`, dark overlap, and branch ambiguity without fitting. K2 predicts Str/Cir will depart from its weak-law continuation much earlier than Pri/Prc; whether that remains true after opening the bright sector is a **staked sign/ordering diagnostic**, not a quantitative band.

## Lindblad cross-check

For one frozen representative point per pair (`s=0.01, kappa=1`), augment by an absorbing sink and use jump operators `sqrt(kappa)|sink><b_j|`. Start in `|d>`. Compare the initial/early decay of total population remaining in the original 11-dimensional system with the non-Hermitian linewidth. This is a convention/dye test only; the resonance eigenvalue remains the primary object.

## SOTA gate

No simulation-SOTA claim follows from a successful K2.3. It only licenses implementing the soft-symmetry compiler on an external many-body/open-system benchmark. The first credible chemistry target is the disordered molecular-polariton regime where MPS-HEOM tracks dark/gray activation and thermodynamic convergence. A SOTA claim requires a named cost reduction (bond dimension, hierarchy size, Krylov dimension, memory or wall time) at fixed observable error against an existing method.

## Spend rule

External benchmark work is bought only if O1–O3 pass and K2.3 identifies at least one controlled window in which the dark/bright reduction predicts the full numerical linewidth. If O3 fails broadly, stop and debug the reduction before any polariton benchmark.
