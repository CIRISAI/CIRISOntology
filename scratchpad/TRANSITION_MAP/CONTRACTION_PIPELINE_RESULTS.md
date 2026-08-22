# CONTRACTION PIPELINE — built and validated (sealed 2026-08-23)

Executing CONTRACTION_FAMILY.md step 1 and 2. The rule was that nothing downstream is
believed until the checker re-derives MMI; it does, and three further controls pass.

## Stage 1 — the checker, gated
`contraction.py` decides existence of a boundary-respecting contraction map
`f : {0,1}^M → {0,1}^N` (arXiv:2409.17317 Thm 2.1). Reduction used: Hamming distance is
the hypercube graph distance, so only `M·2^(M-1)` EDGE constraints are needed — and the
code then re-verifies contraction on ALL pairs, as an independent check of that
reduction (it has never fired).

| control | required | result |
|---|---|---|
| **MMI** (the paper's star-graph example) | contraction map EXISTS | **exists** ✓ |
| **MMI reversed** | must NOT exist | **does not exist** ✓ |
| subadditivity | exists | exists ✓ |
| strong subadditivity | exists | exists ✓ |
**GATE PASSES.** The negative control is the load-bearing one: the checker can say no.

## Stage 2 — candidate QUANTUM inequalities at n=3, the control case
By Cor 4.1 a quantum inequality needs `N ≤ M`, so contraction maps with `M ≥ N` generate
candidates. Swept all (LHS, RHS) pairs over the 7 non-empty subsets of 3 parties,
M ≤ 3, disjoint sides: **177 candidates admit contraction maps**
(M=2,N=1: 33 · M=2,N=2: 6 · M=3,N=1: 116 · M=3,N=2: 18 · M=3,N=3: 4).
The M=2 family is immediately recognisable as subadditivity and the Araki–Lieb
variants, which is what it should be.

## Stage 3 — refutation, and the control result
Each candidate was tested against GHZ, W, product, and **4,000 random pure states over
mixed local dimensions 2–3** (a single violating state would be a self-contained
refutation certificate).

**REFUTED: 0 of 177. SURVIVED: 177.**

This is the correct control outcome, and it is informative in both directions. The
3-party quantum entropy cone is exactly SSA + weak monotonicity (Pippenger), so every
contraction-map candidate at n=3 MUST be a consequence of those — and none was
violated. A single refutation here would have meant a bug in the generator; zero means
generation and refutation are both behaving.

## What is now in hand
A validated two-sided pipeline: **generate** candidate quantum entropy inequalities from
contraction maps (finite, SAT-shaped), **refute** them with a violating state (finite
certificate, typed by our existing entropy machinery). The authors of arXiv:2409.17317
left exactly this direction as "future work"; the apparatus for it now exists and passes
its controls.

## Anti-hype, binding
Nothing here is a new inequality or a new theorem. n=3 was chosen BECAUSE the answer is
known — it is a control, not a discovery, and a survivor at n=3 is not evidence of
anything beyond correct implementation. The open case is n ≥ 4, where a survivor would
still need an implication check against known inequalities before being called a
candidate for anything, and would remain a CONJECTURE even then.
