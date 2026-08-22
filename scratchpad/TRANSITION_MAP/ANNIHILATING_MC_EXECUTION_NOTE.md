# Annihilating coherent MC — pre-execution note (2026-08-22, this session)

Boundary state VERIFIED in the record: prereg 5f65a5b (frozen before execution; W-cascade,
gates, held-out seeds 2026082373/91/92/93), license 9312caa (W=10,000 passes all frozen
gates; both benchmark classifications preserved; no target outcome inspected). The
estimator lineage's kills are recorded (truncation APPROXIMATION-UNCONTROLLED; path-MC
target-limited by sign variance).

## GUARD REQUESTED BEFORE THE HELD-OUT RUN (closes a mutable link)

The license pins W but NOT the estimator implementation. Requested: commit the estimator
code or its sha256 to this record BEFORE the four held-out cells execute, and embed that
hash in the target outputs — the prereg_id discipline the hydro runner already enforces.
Without it, the license->target chain has one unhashed link.

## CONCORDANCE LANE (offered, this session's role)

After the primary workstream executes the held-out cells, this session will independently
REIMPLEMENT the estimator from the frozen prereg text alone (blind to the primary's target
numbers) and run at minimum the L=7 HIGH held-out cell for a two-implementation
concordance check — the pattern that served the W-sweep. The frozen success condition is
untouched: DENSITY-SCALING-SUPPORTED only if held-out LOW is not low-memory and HIGH is
low-memory at both sizes with all SE gates passing; MID diagnostic only; no W increase
after target inspection.

## GPU LICENSE RECORDED + A FINDING THE PRIMARY NEEDS (2026-08-22)

GPU implementation LICENSED at W=100,000 under RAW (smallest passing W; W=10,000 FAILS
under RAW on p90/max error and a MID classification flip). Convention decision RAW-primary
was issued by the orchestrator and independently derived by the supervisor with matching
reasoning; NORMALISED is stored beside, its MID gate vacuous (the exact answer fails it).

**JENSEN-BIAS FINDING — RELAY TO THE PRIMARY WORKSTREAM BEFORE THEIR HELD-OUT RUN.**
The frozen witness sums absolute values of noisy quantities, so batch estimates are
biased UPWARD, worst exactly where true M is near zero — the low-memory regime the
gates probe. Measured: at W=10,000 the exact MID median 0.031812 inflates to 0.052422,
CROSSING the 0.05 classification line; at W=100,000 it returns to 0.032264. The SE
cannot see this (it measures batch spread, not common offset). CONSEQUENCE: the
primary's CPU license at W=10,000 passed its benchmark, but its held-out cells at that W
sit nearer the bias edge than their error bars suggest — a held-out LOW-MEMORY
classification at W=10,000 could flip on Jensen bias alone. Recommendation to the
primary: run held-out at W>=100,000 or correct for the bias; at minimum report the
bias-sensitivity beside any W=10,000 classification.
