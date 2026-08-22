# PHYSICS CONFRONTATION — first results (2026-08-22; legs A and C2, plus the W-ladder)

## LEG A — THE COINCIDENCE INDEX: the steward's question, answered with numbers

Reference object: the PANEL-2 curated confusion matrix (licensed instrument, 248 items).
Nulls: 10,000 draws each from four generic 11-state ensembles (Dirichlet-stochastic,
Haar |U|^2, sparse-Dirichlet, deterministic-map+noise). A null "shows" a signature iff
its statistic is at least as extreme as the object's. Seeds 20260823.

| signature | object value | base rate across ensembles |
|---|---|---|
| S5 mixing localization (top-3 off-diag share 0.3985) | — | 0.0000 / 0.0000 / 0.0000 / 0.0021 |
| S4 a one-way axis (min flow ratio 0.0000 — Record, machine-exact) | — | 0.0000 in all four |
| S3 twin symmetry (named-pair asymmetry 0.1921) | — | 0.0052–0.2922 |
| S2 (cross-ensemble form) | — | VACUOUS as operationalized (best-of-330 vs our named split: 1.0 everywhere; reported as an operationalization failure, not evidence) |
| S2 (object-side form) | the named 4+7 split sits at the **99.7th percentile** of all 330 bipartitions of the object's own confusion geometry | — |
| **CONJUNCTION (S3∧S4∧S5)** | — | **0 / 10,000 in every ensemble: P < 1e-4** |

ANSWER to "how many 11-dimensional dynamical systems exhibit these behaviours":
effectively NONE — no generic draw in forty thousand shows even the S4∧S5 pair, and the
4+7 anatomy is nearly the optimal bipartition of the object's own measured structure.
The special-structure reading SURVIVES its kill (the conjunction is not generic).

## LEG C2 — THE AAS TEST: a split verdict, sharper than the stake

Microscopic Fourier analysis of the frozen three-route sector (theta=1.30):
- RETURN probabilities p[ii] carry ONLY even harmonics of Phi (odd harmonics machine-
  zero, ~1e-17): the Altshuler–Aronov–Spivak time-reversed-pair cancellation holds
  EXACTLY on closed walks. Mechanism-match at the diagonal.
- TRANSFER probabilities are strongly chiral (n=1 harmonic 0.245): microscopically the
  dynamics knows the loop orientation; p(phi+pi) != p(phi) locally (max diff 0.97).
- The macroscopic period-pi of nu(Phi) is EMERGENT SYMMETRIZATION: the two transfer
  chiralities swap exactly under phi -> -phi (p01(phi)=p02(-phi) to 4e-16), so any
  orientation-symmetric transport aggregate is even in phi.
VERDICT: PARTIAL MECHANISM MATCH — AAS-exact on returns; the transport's period-halving
is the lattice averaging its two chiralities, a cleaner statement than naive AAS and
still a named-mechanism rhyme (loop-pair cancellation where it applies, symmetry where
it does not). Recorded with the check values.

## THE W-LADDER, complete (the diagnostic series the steward asked run directly)

L9_LOW:  0.0551 → 0.0328 → 0.0257 → 0.0228 → 0.0240   (W = 1e4…1e6; converged ≈ 0.023–0.024)
L7_HIGH: 0.0675 → 0.0530 → 0.0458 → 0.0331             (W = 1e4…3e5)
Monotone Jensen decay on both flip-cells, convergence a factor ~2 below the 0.05 line;
the only "not low-memory" readings anywhere are the small-W rungs. The primary's
recorded L=9 LOW (0.0505 at W=1e4) sits on the biased first rung of a curve that
converges to 0.024. The artifact case is closed from this side.

## Standing

Leg B (the flavor structural table) remains to run. No stance change; steward review
owed on whether Leg A's conjunction result and the ladder enter the page.
