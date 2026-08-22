# CHORD-1 RESULTS (sealed 2026-08-23; prereg frozen before any ray was tested)

Runner `chordality.py`; data `Max-Rota/SSA-compatible-Extreme-Rays-of-the-Subadditivity-Cone`
`n=6/rays.txt` (208 rays x 63 components), Zenodo 10.5281/zenodo.14983856.

## IMPLEMENTATION CONTROL — PASSES, exactly
Pre-staked: a correct implementation must find ~44 chordal rays among 208, matching the
paper's reported 44 simple-tree graphs; band 35-55, outside which no verdict may be
reported. **Measured: exactly 44.** The band was staked before running and the hit is
exact, which is the strongest available evidence the β-set / correlation-hypergraph /
line-graph / chordality pipeline is implemented correctly.

## RESULT for the two open bulk-cycle rays
**Ray #111: NOT chordal (54 hyperedges). Ray #207: NOT chordal (57 hyperedges).**
By Theorem 11 (arXiv:2412.18018) neither is realizable by a SIMPLE tree graph model.

**This narrows the open question; it does NOT settle it** — exactly as the prereg bound
in advance. He–Hubeny–Rota's open question concerns not-necessarily-simple trees
(the conjecture of arXiv:2204.00075), and chordality speaks only to the simple case.
The general tree question for #111 and #207 remains open.

## A COROLLARY THAT CLOSES THE ROUTE — the cheap disqualification
Necessity (Thm 11) gives {simple-tree realizable} ⊆ {chordal}. The paper reports 44
simple trees among its 150 constructed models, and we measure exactly 44 chordal rays.
Two sets, one contained in the other, of equal finite size — **so they are the same
set.** Therefore no ray outside those 44 is simple-tree realizable, and in particular
**none of the 6 orbits whose holographic realizability is unknown is chordal.**

Consequence, stated plainly: **the chordality criterion cannot resolve any of the
6 unknown rays** (nor the 3 left open after He–Lee–Ooguri arXiv:2601.19979). The
sufficiency theorem of arXiv:2512.24490 has no purchase on them, because sufficiency
only fires on chordal vectors and none of them is chordal. That route is closed, and
closing it cost one afternoon of arithmetic on public data.

## What this was and was not
This applies two published theorems to published data. The theorems are theirs; the
arithmetic is ours; **no new theorem is claimed** and nothing here touches the
CIRISOntology stance. The value is a negative that redirects effort: anyone hoping the
new chordality machinery would settle the N=6 mystery rays can stop, and the live
routes remain the ones the authors named — non-simple tree constructions
(arXiv:2512.18702 calls its own progress there "first steps") or a new holographic
entropy inequality via contraction maps (arXiv:2409.17317).

## Reproducibility
Anyone can re-run this: clone the public data, run `chordality.py`, check that the
control returns 44. Independent falsification of our claim requires only that.
