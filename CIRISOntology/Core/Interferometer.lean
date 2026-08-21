/-
# Interferometer counting — the maximal object's parameter bookkeeping, pinned

The steward's construction (scratchpad/MAXIMAL_OBJECT.md, 2026-08-20): the eleven kinds as
K11, complex mixing on the 55 edges, path-dependent information in the loop sector, Record
as the holonomy. WAGER-CLASS, model-side only; these theorems are the BOOKKEEPING of that
wager — graph-topological counts, decidable, no physics and no world-claim. What they pin:
the loop-phase count 45 is the CYCLE RANK of K11 (E − V + 1), which equals the
(n−1)(n−2)/2 physical-phase count of an 11×11 unitary after rephasing. CORRECTION
(2026-08-21): that equality is an IDENTITY for every n — never a passed check, it could
not have failed; recorded only so the wager's arithmetic cannot drift, carrying no
evidential weight. The 4+7 surface/depth
split (Core/Surface.lean) partitions the edges 6 + 28 + 21. First measurement of the
object's vertex structure: scratchpad/plane_corpus/BABEL_RESULTS.md (frame-orthogonality
exact; off-diagonal leakage localized on the three predicted confusion boundaries).
-/
import CIRISOntology.Core.Surface

namespace CIRISOntology.Core

/-- The vertex count: the eleven artifact-local kinds. -/
def ifoNodes : Nat := 11

/-- The edge count of K11: one channel per unordered pair. -/
def ifoEdges : Nat := ifoNodes * (ifoNodes - 1) / 2

theorem ifo_edges_55 : ifoEdges = 55 := rfl

/-- The cycle rank (first Betti number) of K11: where loop phases live. -/
def ifoCycleRank : Nat := ifoEdges - ifoNodes + 1

theorem ifo_cycle_rank_45 : ifoCycleRank = 45 := rfl

/-- The same 45 by the unitary-mixing route: (n−1)(n−2)/2 physical phases at n = 11.
    Two derivations, one number. -/
theorem ifo_phase_count_agrees :
    ifoCycleRank = (ifoNodes - 1) * (ifoNodes - 2) / 2 := rfl

/-- The full mixing-parameter count: 55 magnitudes + 45 loop phases = 100. -/
theorem ifo_param_count : ifoEdges + ifoCycleRank = 100 := rfl

/-- The 4+7 anatomy partitions the 55 channels: 6 surface–surface, 28 cross,
    21 depth–depth. -/
theorem ifo_edge_anatomy :
    (4 * 3 / 2) + 4 * 7 + (7 * 6 / 2) = ifoEdges := rfl

end CIRISOntology.Core
