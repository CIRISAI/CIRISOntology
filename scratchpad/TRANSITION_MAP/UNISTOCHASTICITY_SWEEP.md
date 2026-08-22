# UNISTOCHASTICITY SWEEP — the object's mixing tables against known physics (sealed 2026-08-23)

Sweep of the A2A bridge's remaining unknown against a KNOWN physics object: a 3x3
doubly stochastic matrix `B` is UNISTOCHASTIC iff `B = |U|²` for some unitary `U` —
i.e. realizable as quantum amplitudes with NO ancilla. Exact criterion: the three
chain links `√(B_1j B_2j)` must satisfy the TRIANGLE INEQUALITY (row-orthogonality
closes as a triangle in the complex plane). Slack := (a+b−c)/c on the sorted links;
slack ≥ 0 is unistochastic, and slack → 0 is a DEGENERATE (flat) triangle, whose area
is the Jarlskog-type invariant — so slack is a moduli-only measure of PHASE CAPACITY.

## Process note, recorded because it is the finding's provenance
A first pass on the 248-item CUR-P2 matrix suggested enrichment. Two errors were
caught before anything was committed: (1) the matrix is 86% zero off-diagonal, so the
test was sparsity-driven; (2) my density check counted the ZEROED DIAGONAL as missing
channels, so no triple could ever register as dense — which had inverted the reported
direction. Both were found by checking, not by review. Re-run at strength below.

## Instrument: the pooled disagreement matrix
All kind-judgment corpora pooled: **25,286 disagreement events over 1,351 items**,
15.5% of the 110 off-diagonal channels empty (vs 86% for CUR-P2 alone). 139 of 165
triples are fully dense and carry the analysis.

## CONTROLS pass
CKM and PMNS are unistochastic, as they must be: slack **+0.0004** (CKM) and
**+0.0597** (PMNS). CKM sits essentially ON the boundary — a nearly flat triangle,
which is the moduli-side face of its tiny Jarlskog invariant (J = 3.16e-5).

## RESULT — the object's tables cluster at the unistochasticity boundary
| ensemble | median slack | % unistochastic |
|---|---:|---:|
| random symmetric doubly stochastic | +0.4717 | 92.6% |
| **diagonal-matched null** (same diagonal dominance) | **+0.2632** | 99.9% |
| **OBJECT, 139 dense triples** | **+0.0979** | 83.5% |
| PMNS | +0.0597 | yes |
| CKM | +0.0004 | yes (barely) |

The object sits far closer to the boundary than random matrices, **and the effect
SURVIVES the obvious confound**: against a null matched on diagonal dominance the
shift is still large (median +0.098 vs +0.263, Mann-Whitney p = 2.3e-20). The object
is also mildly DEPLETED in unistochasticity (83.5% vs 92.6%), i.e. a sixth of its
tables are not unitary-realizable at all.

## Reading, at earned strength
The object's measured mixing has **near-minimal phase capacity** — the same regime
CKM occupies, and unlike generic doubly stochastic matrices at matched diagonal.
Its moduli nearly determine its phases; there is very little room for interference
that the magnitudes do not already fix.

## Caveats, binding
- **The diagonal entries are a PROXY.** The disagreement matrix has no natural
  diagonal, so row sums were used as a self-agreement stand-in. That choice is
  arbitrary and could move the numbers; the diagonal-matched null controls for the
  LEVEL but not for the choice. A measured self-agreement diagonal is owed.
- The 139 triples come from ONE 11x11 and overlap heavily; p-values are descriptive
  of this matrix, not independent-sample significance.
- Sinkhorn is one (canonical) route to double stochasticity.
- This says NOTHING about the object being quantum, and licenses no isomorphism.
