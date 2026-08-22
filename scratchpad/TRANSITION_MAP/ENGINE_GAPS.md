# WHAT THE OBJECT LACKS TO BE A GENERIC PHYSICS ENGINE (2026-08-23)

Steward's reframe, adopted: **the interface is not a visualization of the object — it is
the instrument that finds what the object is missing.** To make a simulation engine
that runs generic physics on this structure, you must supply things the object does not
yet have. Building the UI forces each gap into the open, concretely, with a screen that
either works or does not.

This is a construction list, not a complaint list. It is the same discipline as
REG_GAPS: each gap gets what the UI would expose, and what would close it.

## WHAT WE ALREADY HAVE (so the gaps are precise)
coupling matrix (measured) · symmetry group of order 4 (proved) · exact dark states and
decoupling (proved) · rank-≤2 defect structure with magnitude AND direction (proved) ·
53 conserved sectors on the triangular lattice (proved) · U(1) holonomy with
even-harmonic returns (proved) · positional susceptibility (M9) · depth grading (proved)
· a one-way axis (proved).

## THE GAPS

| # | missing | why physics needs it | what the UI exposes | what would close it |
|---|---|---|---|---|
| E1 | **A METRIC.** We have couplings, not distances. `k_ij` says how bound two kinds are; nothing says how FAR apart they are. | Forces need lengths; springs need rest lengths; any Lagrangian needs a metric. | Immediately: the layout has no principled rest length, so `linkDistance = 120f` stays arbitrary no matter how good `k_ij` is. The screen looks fine and means nothing. | Derive a metric from the coupling (resistance distance / commute time on the Laplacian is the natural candidate and is computable now). Whether it is THE metric is a question the object must answer, not the renderer. |
| E2 | **INERTIA.** M9 gives a response function, not a mass. Nothing in the object plays `m`. | Without mass there is no dynamics, only relaxation. F = ma needs the a. | Any gesture produces overdamped drift, never oscillation. You cannot ring the object. | Either derive mass from the field (susceptibility⁻¹ is a candidate) or accept the object is intrinsically first-order/dissipative — which would itself be a finding. |
| E3 | **A TIME SCALE.** θ is free (handoff U7, uncalibrated). | Rates need a clock. Everything we compute is dimensionless. | The animation speed is a slider with no correct setting. | Calibrate θ against a measured corpus rate (revision cadence) — or prove the object is scale-free in time, which would be stronger. |
| E4 | **CONSERVED QUANTITIES ON K11.** We proved 53 sectors on the TRIANGULAR lattice; the K11 object's commutant is uncomputed (handoff U4). | An engine without conservation drifts and blows up; conservation is what makes integration stable. | Long-running simulations lose or gain "stuff" with nothing to check against. Energy drift is visible within minutes. | Compute the commutant of the K11 collision set — this is finite and runnable now. |
| E5 | **AN ACTION PRINCIPLE.** No Lagrangian, no potential function. | Forces should be gradients of something. Without it, "force" is stipulated per-rule and cannot be composed. | Every new interaction has to be hand-coded; nothing derives. | Look for a potential whose gradient reproduces the measured couplings. If none exists, the object's dynamics is not variational — a real structural claim. |
| E6 | **LOCALITY.** K11 is COMPLETE. Every kind is adjacent to every other. There is no neighbourhood, no light cone, no propagation delay. | Field theory is built on locality. Waves, causality, and signal speed all presuppose it. | Perturbations appear everywhere at once. There is nothing to watch travel — which is exactly what makes a physics UI legible. | **This may not be a gap but a property.** M7 says the object's laws are of a connected field, not of kinds severally; non-locality is consistent with that. The UI question — "what should propagation look like on a complete graph?" — is the sharpest one on this list. |
| E7 | **A CONTINUUM LIMIT.** Eleven nodes, and coarse-graining is EXPLICITLY not covered by our theorems (the `Creation` fence; the kappa-edge pair-pinning warning). | Generic physics lives in continua, or at least needs a controlled coarse-graining. | You cannot zoom. There is no "more detail" — the object is 11 nodes at every scale. | Define and test a coarse-graining that preserves the proved structure. The mint theorems currently forbid assuming one exists. |
| E8 | **CONSISTENT DISSIPATION.** The Record axis is one-way; the rest is unitary. How they couple is the open minimal-dilation question (U6). | Mixing unitary and irreversible sectors incorrectly violates positivity and produces nonsense. | Irreversible edges either freeze the sim or leak probability. It will be visible as things vanishing. | Find the minimal dilation reproducing S4 = 0 without touching the unitary sector. |
| E9 | **BOUNDARY CONDITIONS.** What is outside the eleven? | Every simulation needs to know what happens at the edge of the model. | Objects that leave the field have nowhere to go; the purifier is implicit and unrendered. | The purifier/Record frame is the natural boundary — make it explicit and give it a rendering. |

## WHY THE INTERFACE IS THE RIGHT INSTRUMENT FOR THIS
Each gap above is invisible in a paper and unavoidable in a running engine. You cannot
render motion without a metric and an inertia; you cannot run for ten minutes without
conservation; you cannot zoom without a coarse-graining; you cannot animate propagation
on a complete graph without deciding what propagation MEANS there. **The UI does not
illustrate the physics — it is the falsifier that says which pieces are absent.**

## THE SHARPEST ONE
**E6.** The object may be genuinely non-local — and if it is, that is not a defect to
patch but a structural claim to state and test, consistent with M7. The interface makes
it concrete: build the screen, try to show something travelling, and discover whether
there is anything to show. That question is worth more than the other eight combined.
