# W≠1 PREREG — does coherent loop phase change transport? (R2)
# FROZEN 2026-08-22, before any W≠1 or dephasing transport run existed.
# prereg_id: REGHYDRO-W1-20260822

## The question and the named numbers

Does the gauge-invariant loop phase phi (W = e^{i phi} on the three-route conserved
collision sectors N=2,P=0 and N=4,P=0) change macroscopic transport, with nothing
hand-inserted? THE NUMBERS: Delta-nu(phi) = nu(phi) - nu(0) and Delta-g(phi) =
g(phi) - g(0), measured by the SAME estimators as the flat runs (shear-decay fit;
advected-mode phase-speed fit), at theta = 1.0.

## Design (all configs derive from the committed templates; code sha
1afd18704c33b349cf93094c5cbdd04a6912beec5bf2cc468acaddea3124fb9c; runner refuses
inference without this prereg_id)

- ARM C (coherent): phi in {0, pi/6, pi/3, pi/2, 2pi/3, 5pi/6, pi}; grid 96, rho 2.0,
  perturbation and windows exactly as the committed flat configs; experiments nu (modes
  1,2) and g.
- ARM D (dephasing deflation control): annealed phase randomization (phase_bins 48),
  same theta, same everything else — one run per experiment.
- BASELINE: phi = 0 (already measured: nu = 0.1296/0.1294, g flat-family baseline run
  fresh under the coherent family at phi=0 so the family is its own control).

## Staked readings

- W-EFFECT: |Delta-nu(phi)| or |Delta-g(phi)| exceeds 3x the mode-1-vs-mode-2
  discrepancy (the instrument's own precision floor, ~0.0002 on nu; the analogous
  fit-derived floor for g) with a smooth phi-dependence (monotone on [0,pi] or even in
  phi) AND the dephasing arm shows LESS THAN HALF the effect at matched theta ->
  coherent holonomy changes transport. The number is reported as the curve.
- DISORDER-NOT-HOLONOMY: effect present but the dephasing arm shows a comparable shift
  -> the shift is phase-disorder, not loop coherence. Reported as such; the
  three-for-three hazard's prediction confirmed for this construction.
- NULL: both curves flat within the precision floor -> coherent collision phase does
  not survive Born/dephasing streaming to the hydrodynamic scale. An honest bound, and
  the tractable-boundary caveat (phases not carried across streaming in R1) is the
  named suspect for any null — a full phase-carrying implementation is the successor,
  not a rescue of this run.
- FIXED-POINT-DESTROYED: the code's own status on any arm — reportable outcome, not
  failure.

## Scope fences

Model-lattice physics only; no world claim; no stance change; nu and g are properties
of THIS kinetic-closure instrument. The FHP identification bounds the flat sector;
novelty, if any, lives only in a confirmed W-EFFECT that the dephasing arm cannot mimic.
