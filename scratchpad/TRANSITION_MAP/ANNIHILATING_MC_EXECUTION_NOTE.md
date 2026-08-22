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
