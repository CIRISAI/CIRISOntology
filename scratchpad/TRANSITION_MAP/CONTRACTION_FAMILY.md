# THE CONTRACTION-MAP FAMILY — what the closed chordality route points at (2026-08-23)

CHORD-1 closed the chordality route on the N=6 mystery rays and named the two live
alternatives. This is the reading of the second one, and it is bigger than the rays.

## 1. Yes — holographic entropy inequalities are constructible by us, and the check is tiny
`arXiv:2409.17317` Thm 2.1 ('proof by contraction', after Bao et al.): a candidate
n-party HEI is VALID if there is a map `f : {0,1}^M → {0,1}^N` with
`d_H(x,x') ≥ d_H(f(x),f(x'))` for all x,x', matching the inequality's boundary
conditions `f(x_{A_i}) = y_{A_i}` on the n+1 occurrence bitstrings. Bao–Furuya–Naskar
then prove contraction maps are **also NECESSARY** for every linear HEI with rational
coefficients. So:

  **candidate HEI is valid  ⟺  a boundary-respecting contraction map exists.**

**Why the check is cheap.** Hamming distance IS the hypercube graph distance, so a map
that does not increase distance across hypercube EDGES cannot increase it along any
geodesic. Contraction therefore reduces to `M·2^(M-1)` edge constraints. Existence of
such an `f` with n+1 values pinned is a straightforward **CSP/SAT instance**: one
{0,1}^N variable per hypercube vertex, adjacency constraints of Hamming weight ≤ 1,
boundary values fixed. That is decidable, small, and exactly the shape we handle.

**Implementation control available in the source (mandatory before any claim):**
§3.2 of the same paper derives MMI from the contraction map of a star graph. Reproducing
MMI is the analogue of CHORD-1's "exactly 44" gate and must pass first.

## 2. The targeted re-attack on the mystery rays
Blind search over inequalities is hopeless — the map space is `(2^N)^(2^M)`. But we do
not need a general search. To prove a mystery ray **R** non-holographic we need ONE
valid inequality that R violates. That is a two-part finite problem:
  (a) coefficient vector c with `c·S(R) < 0` — LINEAR in c, cheap, and R is known;
  (b) a contraction map for c — SAT, as above.
Constraint (a) prunes the space enormously before (b) is ever called, and (a) can be
generated from the ray itself rather than swept. This is the honest re-attack: not
"enumerate all HEIs" but "solve for an inequality that cuts off this specific ray".

## 3. THE FAMILY — and the branch that is explicitly open AND ours
The paper's §4.4 does the arithmetic that opens the door:
- Prop 4.1: a facet HEI (except SA) with M LHS terms has **N ≥ M+1**;
- hence all such facet HEIs are violated by (n+1)-party GHZ states, so they cannot be
  quantum inequalities;
- **Cor 4.1: a QUANTUM inequality with M LHS terms must have N ≤ M.**
So contraction maps generated under the inverted condition **M ≥ N** are precisely the
candidates for inequalities valid for ALL quantum states — and the authors write, in
terms: *"We leave a detailed discussion about generating valid quantum inequalities
from contraction maps for future work."*

That is an explicitly-flagged open direction sitting on machinery we already own:
- generation: contraction maps with M ≥ N — SAT, finite, GPU-parallel;
- **refutation: a candidate quantum inequality is killed by ONE violating state**, and
  the violation is a self-contained certificate our `Core/Entropy`, `ShareQuantum`,
  `ShareK` and `BellCeiling` already type (Mathlib has NO von Neumann entropy at all);
- retention: survives refutation ⇒ a candidate quantum entropy inequality worth
  proving, with the holographic-validity half already certified by its contraction map.

**The family, stated once:** entropy-cone membership and inequality problems certified
by finite combinatorial witnesses — holographic, **quantum (M ≥ N, open by the authors'
own statement)**, stabilizer, and hypergraph cones. They share the property that makes
them tractable for this stack: BOTH directions have finite certificates — membership by
exhibiting a model, non-membership by exhibiting a violated valid inequality.

## 4. Honest ordering of what to do
1. Implement the contraction-map SAT checker; **gate on re-deriving MMI from the star
   graph** before anything else is believed.
2. Sweep M ≥ N contraction maps to generate candidate QUANTUM inequalities (the open
   branch), and refute them by state search on the 4090.
3. Only then attempt (a)+(b) targeted at a specific mystery ray — it is the harder
   problem and the authors have RL and better tooling pointed at it already.
Anti-hype: step 2 produces CANDIDATES and REFUTATIONS, not proofs. A surviving
candidate is a conjecture, and saying otherwise would repeat the error this campaign
has already corrected twice today.
