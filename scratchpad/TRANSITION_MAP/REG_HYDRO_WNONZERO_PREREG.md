# REG+ coherent holonomy transport — preregistration draft for freeze

**Status:** READY TO FREEZE; **NOT YET A REPOSITORY-FROZEN PREREG**  
**Prepared:** 2026-08-21  
**Reference implementation SHA-256:** `1afd18704c33b349cf93094c5cbdd04a6912beec5bf2cc468acaddea3124fb9c`

No inferential W!=1 transport coefficient (`Delta-nu`, `Delta-g`) was inspected while
preparing this document. Only flat-sector transport and matrix-level phase-response
instrument checks were used to choose the fixed design below.

## 1. Question

Starting from the validated flat-sector lattice-fluid positive control, does a genuine
REG loop phase change the emergent long-wave transport coefficients in a way that is:

1. nonzero against the flat `W=1` baseline,
2. stable under lattice refinement,
3. distinguishable from phase disorder with the same collision graph and magnitudes,
4. or does nonzero holonomy instead destroy the hydrodynamic fixed point?

The named numbers are

\[
\Delta\nu(\Phi)=\nu(\Phi)-\nu(0),
\qquad
\Delta g(\Phi)=g(\Phi)-g(0).
\]

Nothing else is promoted as the primary result.

## 2. Microscopic model — frozen family

Local six-carry Boolean occupation space:

\[
\mathcal H_x=\mathrm{span}\{|n_0\ldots n_5\rangle\},\qquad n_a\in\{0,1\}.
\]

Collision blocks never cross exact local `(N,Px,Py)` sectors.

For every 3-state conservation sector the complex Hermitian generator is frozen as

\[
H(\Phi)=
\begin{pmatrix}
0 & 1 & e^{-i\Phi}\\
1 & 0 & 1\\
e^{i\Phi} & 1 & 0
\end{pmatrix},
\qquad
U(\Phi)=e^{-i\theta H(\Phi)}.
\]

The directed internal triangle has

\[
W=e^{i\Phi}.
\]

Two-state sectors use the phase-free `sigma_x` block already in the reference code.
One-state sectors are identity.

The tractability boundary is also frozen: the local unitary is Born-read/dephased
after the collision and before spatial carries. This prereg therefore tests
**local coherent route interference**, not multi-step globally coherent quantum transport.

## 3. Flat-sector parameter selection

`theta = 1.30 rad` is frozen.

It was selected solely from `Phi=0` data because the flat long-wave viscosity has a
broad minimum there while exponential shear decay remains clean.

Primary density:

`rho = 2.0`

This is away from the FHP half-filling convection zero and remains in a well-behaved
low-density hydrodynamic sector.

No theta or density retuning is allowed after W!=1 execution starts.

## 4. Phase grid

Run the complete 12-point loop-phase circle:

`Phi = 0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330 degrees`.

No phase point may be omitted because it looks pathological.
`Phi=0` is the within-family flat baseline.

## 5. Primary grids and refinement

Primary grid: `N = 256`.

Mandatory refinement check: `N = 192`.

A claimed coefficient shift must preserve sign across 192 and 256 and agree in magnitude
to within the larger of:

- 25% relative difference, or
- the corresponding absolute detection band below.

Failure of refinement consistency is classified `DISCRETIZATION-SENSITIVE`, not support.

## 6. Viscosity estimator

Initial shear mode:

\[
u_x(y,0)=\epsilon\sin(2\pi m y/N),\quad u_y=0,
\]

with:

- `epsilon = 0.003`
- modes `m = 1,2`
- cycles `0..80`
- frozen fit window `5..50`.

For each mode fit

\[
\ln |A_m(t)| = a-\nu_m k_m^2 t.
\]

Primary viscosity:

\[
\nu(\Phi)=\frac{\nu_1(\Phi)+\nu_2(\Phi)}{2}.
\]

Flat instrument gate before reading Delta-nu:

- each log-amplitude fit `R^2 >= 0.999`,
- mode disagreement `|nu1-nu2| / mean(nu1,nu2) <= 0.02`.

If a nonflat run violates these because the mode no longer behaves diffusively, classify
that phase `FIXED-POINT-DISTURBED` and report the raw trajectory; do not force a viscosity.

Primary pre-staked viscosity effect band:

\[
|\Delta\nu(\Phi)| > 0.005.
\]

This is intentionally larger than the observed flat resolution/mode spread.

## 7. Convection estimator

Initial weak transverse wave on a uniform background:

\[
u_x=U_0,\qquad
u_y=\epsilon\sin(2\pi x/N),
\]

with:

- `U0 = 0.008`
- `epsilon = 0.0008`
- mode `m = 1`
- cycles `0..90`
- frozen phase-fit window `5..55`.

Let the unwrapped complex Fourier phase obey

\[
\arg A(t)=\arg A(0)-kct.
\]

Then

\[
g(\Phi)=c/U_0.
\]

Fit-quality gate:

`phase-fit R^2 >= 0.995`.

If the mode amplitude becomes too small for a valid phase fit, classify
`FIXED-POINT-DISTURBED`.

Primary pre-staked convection effect band:

\[
|\Delta g(\Phi)| > 0.03.
\]

The band is deliberately larger than the flat 192-to-256 finite-resolution drift.

## 8. Dephasing deflation control — mandatory

Run the exact same `theta`, density, grids, initial conditions and estimators with
the loop phase randomized uniformly on `[0,2pi)` independently each collision step.

Implementation: the frozen 48-bin annealed phase average already present as
`holonomy.mode = annealed_dephasing`.

The collision graph and all `|H_ij|` magnitudes are unchanged.

Classification:

- **COHERENT-HOLONOMY**: a fixed-Phi effect crosses its primary band, survives
  resolution, and differs from the dephasing control by at least the same primary band.
- **PHASE-DISORDER-COMPATIBLE**: fixed-Phi and dephased shifts are not separated by
  the corresponding primary band.
- **NULL**: no fixed-Phi point crosses either effect band and the fixed point survives.
- **FIXED-POINT-DISTURBED**: long-wave exponential/advective fitting fails at one or more
  phase points; this is a reportable physical outcome, not an analysis failure.
- **DISCRETIZATION-SENSITIVE**: apparent effect does not survive 192->256 refinement.

## 9. Multiple phases / adjacency guard

A single isolated phase-bin excursion is not enough for a coherent-holonomy claim.

At least **two adjacent nonzero phase bins** must cross the same named-number band with
the same sign, unless an exact symmetry point (`Phi=180 deg`) is the sole effect and the
neighboring bins move continuously toward it.

All 12 phase values and both named coefficients are reported regardless of verdict.

## 10. Secondary density replication

Only after the primary rho=2.0 analysis is sealed, repeat the exact frozen phase grid at:

`rho = 2.5`

No parameter changes except the density itself.

This is secondary robustness only; it cannot rescue a null primary result.

## 11. Standing exclusions

- Model physics on a lattice only.
- No claim that ontology kinds are literal physical degrees of freedom.
- No world-physics claim from a lattice transport shift.
- REG remains a research/lab grammar, never trust infrastructure.
- This substrate has no verdict readout; the generalized flatness theorem for
  verdict-producing/accountability grammars is untouched.
- Nonzero holonomy is not called viscosity, force, or curvature-induced fluidity by fiat.
  Only measured changes in the coarse transport coefficients may receive those labels,
  and only at model level.

## 12. Freeze condition

This prereg becomes executable only when the exact text (or a semantically identical
version with all numbers unchanged) is committed to the CIRISOntology record.

The execution config must carry that immutable commit SHA as `prereg_id`.

Before that commit exists, the reference runner must continue to refuse W!=1 and
dephasing transport-coefficient runs.
