# REG+ hydrodynamics R1 handoff

Target note: `scratchpad/TRANSITION_MAP/REG_HYDRO_NOTE.md`
Target note commit observed: `eb35abc7b299b276def1307b5cdabac10c86748a`

## Provenance

This package is a **reference reconstruction made after the chat session**.
No original source artifact from the earlier numerical discussion persisted.
Therefore:

- earlier chat numbers remain testimony;
- outputs under `results/` are fresh evidence produced by this reconstruction;
- an independent reproduction is still required for the house-rule R1 closure.

## Fresh checks in this package

- 7/7 invariant tests pass.
- 53 exact local `(N,Px,Py)` sectors: 44×dim-1, 7×dim-2, 2×dim-3.
- All collision families have zero cross-sector transition probability.
- Flat FHP-I control at rho=2:
  - measured `g = 0.2594852946050648`
  - continuum target `g = 0.25`
  - phase-fit `R^2 = 0.9997790071497894`
- Flat reversible sector-permutation shear:
  - mode 1 `nu = 0.12957371553312555`
  - mode 2 `nu = 0.12939565026814334`
  - both fits have `R^2` effectively 1.
- W!=1 matrix-level instrument smoke changes the N=2,P=0 three-route transition probabilities while preserving all invariants.
- The runner refuses W!=1/dephasing transport-coefficient inference without a non-empty frozen `prereg_id`.

## Holonomy pinned by the code

For the three-route conserved collision sector:

`H(phi) = [[0,1,exp(-i phi)], [1,0,1], [exp(i phi),1,0]]`

and

`U(phi) = exp(-i theta H(phi))`.

The directed product around the route triangle is `W = exp(i phi)`.
`phi` is treated as the gauge-invariant Wilson-loop angle supplied by an independent carries-link substrate, not as a site phase.

The tractable boundary is local Born/dephasing after each coherent collision; no phase coherence is carried across multiple spatial streaming steps in this R1 implementation.

## R2 status

No Delta-nu(phi) or Delta-g(phi) inferential W!=1 run is included.
The non-flat config and dephasing config are templates and are deliberately prereg-gated.
