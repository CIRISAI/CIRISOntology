# CHORDALITY ATTACK (CHORD-1) — FROZEN 2026-08-23 before any ray is tested

## The open question
He–Hubeny–Rota (arXiv:2412.15364, JHEP06(2025)055) constructed holographic graph models
for 150 of the 156 SSA-compatible N=6 extreme rays that violate no known holographic
inequality. **Two of those graphs contain a "bulk cycle" — rays #111 and #207** — and
the paper states verbatim: "it would be interesting to see if we can alternatively
realize them by tree graphs. We leave this for future exploration."

## Why it is decidable now
- `arXiv:2412.18018` Def. 1: β(X) = { I(Y:Z) : Y⊔Z = X, |Y|,|Z| ≥ 1 }, for |X| ≥ 2.
  Def. 2: β(X) is POSITIVE iff every I in it is > 0.
  Def. 3: the correlation hypergraph has V = the N+1 parties (purifier included) and
  one hyperedge e_X = X for each positive β-set.
  Thm 11: an entropy vector is simple-tree realizable ONLY IF the line graph L_P of
  that hypergraph (vertices = hyperedges, adjacency = non-empty intersection) is
  CHORDAL (every cycle of ≥4 vertices has a chord).
- `arXiv:2512.24490` proves chordality is also **SUFFICIENT**, constructively, for any
  number of parties.
So: **chordal ⟺ realizable by a simple tree graph model.**

## Data
`github.com/Max-Rota/SSA-compatible-Extreme-Rays-of-the-Subadditivity-Cone`
(Zenodo 10.5281/zenodo.14983856), file `n=6/rays.txt`: 208 rows × 63 integer entries,
lexicographic order over the non-empty subsets of 6 parties. Purification fixes
S(X) for any X containing the 7th (purifier) subsystem via S(X) = S(complement).

## Procedure (fixed before running)
For each ray: build S over all subsets of the 7 subsystems by purification; for every
X with |X| ≥ 2 test whether all bipartition mutual informations are strictly positive;
collect those X as hyperedges; build the line graph; test chordality by the standard
lexicographic-BFS / perfect-elimination-ordering algorithm.

## IMPLEMENTATION CONTROL — the load-bearing gate, stated before any result
The risk here is a coding error, not an interpretive one. The paper reports that of the
150 constructed graphs, **44 are simple trees**. So a correct implementation must find
**approximately 44 chordal rays among the 208** — and the 44 must be among the 150 with
constructed models. A wildly different count (say 5, or 150) means the implementation is
wrong and NO verdict on #111/#207 may be reported. This gate is checked FIRST.

## Staked outcomes for rays #111 and #207
- **CHORDAL** ⇒ by the sufficiency theorem a simple tree graph model EXISTS, so the ray
  is tree-realizable and is NOT a counterexample to the tree conjecture. The published
  algorithm (arXiv:2512.18702) would then construct it explicitly. This would answer the
  question the paper left open.
- **NOT CHORDAL** ⇒ NO simple tree realization exists. **Caveat carried, binding:** the
  conjecture of arXiv:2204.00075 concerns not-necessarily-simple trees, so this does
  NOT settle the general question — it narrows it, and makes the ray a candidate
  counterexample only for the simple case.
- Either way the result is checkable by anyone re-running the same public data.

## Anti-hype
This is applying two published theorems to published data. If it works, the credit is
theirs and the arithmetic is ours. No claim of a new theorem follows, and nothing here
touches the CIRISOntology stance.
