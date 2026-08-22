# MACHINE-CHECKABLE OPEN QUESTIONS — swept shortlist (sealed 2026-08-23)

External sweep against our actual stack. Verification limits carried from the scout:
WebSearch budget was exhausted before it started and arXiv/OpenAlex were rate-limited,
so most paper content is summarizer-mediated; verbatim abstracts were obtained only for
arXiv:2601.19979, 2412.15364, 2409.17317, 2501.03970, 2511.03537, 2601.13475, 2306.13319.

## THE RECOMMENDED TARGET — holographic entropy cone at N=6
He–Hubeny–Rota (arXiv:2412.15364, JHEP06(2025)055) computed every extreme ray of the
6-party cone: 208 new genuine orbits, 156 not violating a known holographic inequality,
graph models constructed for 150. **Six were left open.** He–Lee–Ooguri
(arXiv:2601.19979, JHEP06(2026)267) resolved 3 by reinforcement learning, leaving
**3 unresolved with evidence — explicitly not proof — of non-realizability**, which
would imply undiscovered holographic entropy inequalities at N=6. Separately **2 of the
150 constructed models contain a bulk cycle**, leaving open whether tree-topology
equivalents exist or whether they are counterexamples to the tree conjecture
(arXiv:2204.00075).

**Why it fits this stack better than anything else swept:** a graph realizes an entropy
vector iff for each of the 2⁶−1 = 63 non-empty subsets the min-cut equals the target
entry. Integer arithmetic, a handful of vertices, `decide`-sized — and it is exactly how
the 3 resolved rays were PROVEN (exhibit the graph, check the cuts). **Zero certified
numerics required.** Search is embarrassingly parallel and far below a 4090's reach.
The question is named as open in a refereed JHEP paper, so either outcome is
independently re-checkable by re-running the cuts, and failing to find a tree still
yields a bounded negative rather than an uninterpretable null.

**Named blockers, not smoothed:** proving NON-realizability needs either a new
inequality or a bound on internal graph vertices, and no such bound exists for general
graphs — which is precisely why Ooguri's group could only offer "evidence". The
contraction-map search space is (2^R)^(2^L), so naive sweeping is hopeless; the
partial-cube embedding algorithm of arXiv:2409.17317 or GPU heuristics are required.
And it is UNCONFIRMED whether the six mystery rays exist as machine-readable data.

**Cheapest first move, before any compute:** read Hubeny–Rota arXiv:2512.24490, which
is summarized as proving a **chordality condition necessary and sufficient** for
realizability by simple tree graph models. If it applies, the two bulk-cycle rays may
collapse to a polynomial-time chordality test — a very cheap win or a very cheap
disqualification. The scout did NOT read this paper and does not know its hypotheses or
refereed status; that is the first thing to check.

**House discipline binding this target:** preregister before looking. Stake in advance
that a found tree realization means the tree conjecture survives on these rays; that a
certified exhaustive absence up to a STATED VERTEX BOUND makes them counterexample
candidates; and **fix the vertex bound before running anything.**

## The rest of the ranked list, with the blocker named for each
2. **Certified conformal-bootstrap exclusion bounds** — the dual functional is a
   natural certificate and LeanCert's box-bounds API fits; two targeted searches
   returned ZERO relevant hits, so it is genuinely unoccupied. Blocker: nobody has a
   certified error bound on the rational approximation to the conformal blocks, so you
   would rigorously certify the wrong inequality. Scoped version: low-derivative-order
   single-correlator bound.
3. **Minimum 3D Kochen–Specker system** — answer lies in [24, 31]; the 24 lower bound
   came with the first computer-verifiable KS certificate (40.3 TiB DRAT at order 23;
   arXiv:2306.13319, extended arXiv:2604.19947). NOT tractable for us — cube-and-conquer
   SAT at cluster scale. Real unclaimed contribution needing no search compute:
   formalize the reduction from "KS system" to the SAT encoding so the DRAT certificate
   certifies the INTENDED statement.
4. **MUBs in dimension 6** — full problem is real-algebraic-geometry feasibility in 60+
   unknowns; Gröbner elimination does not terminate. Cheap bounded sub-target: formally
   check Joka's claimed MUB→MOLS implication (arXiv:2511.03537), which the scout judges
   very likely wrong — same author withdrew arXiv:2601.13475 at v5 with "The proof the
   paper gives is not correct." That is refereeing, not settling, and it plays to our
   strength.
5. **Quantum entropy cone** — ELEVATED by our entropy library but **UNRESEARCHED**;
   listed as a pointer only. The one verified hook: arXiv:2409.17317 states its
   contraction-map classification yields "a procedure to generate candidate quantum
   entropy inequalities", and candidate inequalities are REFUTABLE by machine (exhibit a
   violating state; the violation is a self-contained certificate our density-matrix API
   already types). Must be researched before anyone acts.
6. **Physlib** — venue, not a question (see FORMALIZATION_READINESS.md).
7. **Lieb–Oxford constant** — rigorous bounds [1.4442, 1.58]; the gap does not close by
   computation, the remaining distance is analysis. Scoped: formalize the certified
   numerical steps of the existing 1.58 proof.
8. **Computer-assisted PDE blowup** — the strongest precedent that machine checks settle
   physics, and live (Chen–Hou arXiv:2607.15256; DeepMind arXiv:2509.14185). **No
   computer-assisted PDE proof has been end-to-end formalized in any proof assistant** —
   unclaimed, and now feasible given LeanCert + girving/ray. Treat arXiv:2604.09949
   (claimed 3D Navier–Stokes singularity, unrefereed single author) as almost certainly
   wrong until refereed.

## Correction this sweep forced on us
FORMALIZATION_READINESS.md asserted that certified numerics "would require building a
certified-numerics stack first". **That was wrong** and is now marked superseded in
place: LeanCert and girving/interval exist and are maintained. The penalty on that whole
target class is a dependency and an integration cost, not a from-scratch build.

## FIRST MOVE EXECUTED (2026-08-23) — the chordality check is REAL and the target is well-posed

The scout flagged Hubeny–Rota arXiv:2512.24490 as the cheapest way to collapse or
disqualify the bulk-cycle rays, and could not read it. Fetched and read (verbatim
abstract). It delivers MORE than the scout's one-line summary suggested:

**"We prove that the 'chordality condition', which was established in arXiv:2412.18018
as a necessary condition for an entropy vector to be realizable by a holographic simple
tree graph model, is also sufficient. The proof is constructive... these results hold
for an arbitrary number of parties."**

So the literature now supplies a COMPLETE, DECIDABLE PIPELINE:
1. `arXiv:2412.18018` — the correlation-hypergraph representation and the chordality
   condition (also generalizes the holographic mutual-information/connectivity relation
   to arbitrary quantum systems);
2. `arXiv:2512.18702` — an EFFICIENT ALGORITHM constructing a simple tree graph model
   from a chordal entropy vector, plus first steps toward non-simple trees and toward
   "detection of unrealizability independently of knowing the inequalities";
3. `arXiv:2512.24490` — chordality is NECESSARY AND SUFFICIENT, constructively.

**Consequence for the two open bulk-cycle rays.** The question "is there a tree
realization?" reduces to "is this entropy vector CHORDAL?" — a finite check on a
hypergraph built from 63 subset entries. Chordal ⇒ run the published algorithm and the
realization is produced. Not chordal ⇒ NOT simple-tree realizable. **Caveat that must
be carried:** the conjecture of arXiv:2204.00075 concerns not-necessarily-simple trees,
so non-chordality disqualifies only the SIMPLE tree case; the general tree question
would remain open for that ray.

**Status: the cheap first move came back POSITIVE.** The target is well-posed, the
decision procedure is published, and no certified numerics are involved. What is still
needed before any work: the full text of arXiv:2412.18018 for the precise chordality
definition, and the two rays' entropy vectors from arXiv:2412.15364's tables (still
UNCONFIRMED whether these are published as machine-readable data).

## A bridge to our own library, noted
arXiv:2512.24490 states that any entropy vector realizable by a holographic graph model
is also realizable — at least approximately — by a STABILIZER STATE, and that these
techniques bear on "the structure of the stabilizer and quantum entropy cones". Our
`Core/BellCeiling.lean` is built on the C5 ring GRAPH STATE, with every pair marginal
computed and `bell_ceiling_exceeds_cap` proved. The holographic entropy cone and our
quantum-ceiling work are therefore about closely related objects — graph/stabilizer
states and their entropy vectors — which is the strongest connection this sweep found
between an open external question and machinery we already own.
