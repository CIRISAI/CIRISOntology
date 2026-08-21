# AMP_GRAMMAR_PRIOR_ART — prior-art and mechanism sweep on the neutral amplitude grammar

**Date:** 2026-08-21 · **Register:** prior-art sweep, not a result. Nothing here measures anything.
It sizes what is already published against the staked construction and says what is left.

**METHOD DISCLOSURE, up front and load-bearing.** The session's WebSearch budget was exhausted
(200/200) before this task began. The sweep was therefore run against **arXiv's public API,
OpenAlex, and the Wikipedia search API** by direct fetch, not against a general web index. That
biases coverage toward preprint-culture fields (physics, CS theory, quant-fin) and **against**
psychology journals, law reviews, database/security conference proceedings not mirrored on arXiv,
and books. Concretely: Busemeyer & Bruza's and Ilinski's books, Malaney's 1996 Harvard thesis, and
the trust/reputation systems literature were reachable only through citations and secondary
sources, not read. **Every proximity rating below should be read as a floor, not a ceiling** — the
unswept literature can only make the incumbents closer, never further away. Two ratings in
particular (quantum cognition's criticism literature; trust-semiring prior art) rest on secondary
evidence and are marked `[SECONDARY]`.

---

## 0. Verdicts up front

| Question | Verdict |
|---|---|
| **Q1 — Incumbents** | **CROWDED for the substrate, EMPTY for the target.** Amplitudes over concepts, words, questions and cognitive states are a 20-year field with its own no-go theorems and its own "are these models even quantum?" critique. Amplitudes over a **taxonomy of kinds of change / speech acts** returned **zero hits** on every phrasing tried |
| **Q2 — The contraction** | **CROWDED-ADJACENT, verging on OCCUPIED in the abstract.** "Same compositional skeleton, swap the complex/linear value object for an ordered/idempotent one" has **at least four independent names in four fields**, one of which (Maslov dequantization) is explicitly framed as a Bohr-correspondence-principle limit — i.e. the Inönü–Wigner flavour is already claimed. And the specific contraction target is occupied: **trust propagation as an ordered semiring path problem is Theodorakopoulos & Baras 2006, ~513 citations.** What is NOT done: deriving a *named deployed* framework as the contraction of a *named* amplitude grammar, and the no-go |
| **Q3 — Holonomy as attack** | **OCCUPIED in finance, at theorem strength, since 2009.** "The connection has zero curvature if and only if there is no arbitrage" is Vazquez–Farinelli's stated theorem; Farinelli's Geometric Arbitrage Theory explicitly *"parameterize[s] arbitrage strategies by its holonomy."* Our "accountability = enforced zero holonomy" **is their theorem in a new domain.** Ilinski is the 1997 ancestor and Malaney–Weinstein the contested cousin; both carry published refutations. What remains ours is the domain and the *direction of the arrow* — see §3.4 |

**The one finding that most changes what the programme should say about itself** is in §4.1 and it is
arithmetic, not literature: **55 + 45 = 100 is an identity that holds for every n, not a fact about
11.** The cycle rank of the complete graph K_n is exactly (n−1)(n−2)/2, which is exactly the number
of physical phases in U(n) after rephasing, for all n. The maximal object's headline counting is a
theorem of graph theory that was always going to come out right. It should never be presented as a
discovered coincidence.

---

## 1. Q1 — THE INCUMBENTS, HONESTLY SIZED

### 1.1 What each school puts amplitudes over

| School | Amplitudes live over | Do phases do work? | Proximity to ours |
|---|---|---|---|
| **Quantum cognition** (Busemeyer & Bruza; Pothos) | *Cognitive states* in a Hilbert space of beliefs/preferences; questions are **projectors**, not basis elements. Order effects arise from non-commuting projectors | **Partly, and contested.** Interference terms are the headline claim (disjunction effect, conjunction fallacy). But see §1.2 — a 2017 analysis argues the interference term is doing no work in the standard order-effect models | **ADJACENT.** Same formal apparatus, different carrier: their basis is *what an agent believes*, ours is *what kind of change occurred* |
| **Aerts / Brussels school** | *Concepts* and their combinations; "conceptuality interpretation"; extended Bloch representation | Yes, and pushed **past** Hilbert space deliberately (GTR model, "beyond-quantum") because Hilbert space provably could not deliver what they needed | **ADJACENT**, and instructive: they hit a wall and left the Hilbert space rather than abandon the phenomenon |
| **Khrennikov** | Contextual probability generally; "quantum-like" models across cognition, finance, biology | Yes — interference as the signature of contextuality | **ADJACENT** |
| **DisCoCat** (Coecke, Sadrzadeh, Clark) | *Word meanings* as vectors; **grammar** as the compositional wiring (pregroup reductions → tensor contractions) | **Essentially NO.** `all:"DisCoCat" AND all:"phase"` returned **zero results** on arXiv. In practice the vectors are real, usually from distributional counts; the categorical framework is `FdVect` over ℝ. The genuinely load-bearing extra structure the field added is **density operators and the Löwner order** for entailment (Bankova–Coecke–Lewis–Marsden 2016), which is an **ORDER**, not a phase | **CLOSE ON SKELETON, OPPOSITE ON PHASES.** Their composition-then-readout shape is ours. But the field that had complex amplitudes available for free **did not use them** — and where it needed extra expressive power it reached for an order, exactly the direction our contraction runs |
| **Quantum IR** (van Rijsbergen; Widdows) | Documents and queries as subspaces; relevance as projection | Mostly not — real vector spaces, projections, subspace lattices. Widdows' later work (with Pothos, 2023) runs cognitive decision models as actual quantum circuits | **ADJACENT** |

### 1.2 The standard criticisms — real, and sharper than "overfitting"

Two are load-bearing and both are stronger than the generic free-parameter complaint:

1. **"Are Quantum Models for Order Effects Quantum?"** (Moreira & Wichert, arXiv:1706.05080). The
   finding, in their own abstract's terms: **quantum interference effects play no role** in the
   projection-based models used for order effects. The models are *formally* quantum and
   *operationally* classical. This is the exact failure mode our construction must avoid: an
   amplitude grammar whose amplitudes never cash out is a more expensive notation, not a theory.
2. **A no-go from inside the field.** Aerts, Beltran, Sassoli de Bianchi, Sozzo & Veloz
   (arXiv:1604.08268) state that the quantum cognition paradigm was *"challenged by its proven
   impossibility to simultaneously model 'question order effects' and 'response replicability'."*
   Hilbert space is not merely unconstrained — on this pair of phenomena it is provably **too
   constrained**, and the school's response was to move beyond it.

`[SECONDARY]` The overfitting/post-hoc-Hilbert-space critique that the brief names is real and
widely made, but the direct sweep did not surface a canonical statement of it — the searches
`quantum cognition + criticism/critique/free parameters/model comparison` returned nothing on
arXiv. It lives in psychology journals (Behavioral and Brain Sciences commentary on Pothos &
Busemeyer 2013 is the usual citation). **Do not cite it as swept.**

### 1.3 The one genuinely empty cell

**Nobody puts amplitudes over a change/act taxonomy.** Queries run and their results:

- `"dialogue act" AND "quantum"` — **zero**
- `"speech act" AND "vector space" AND "semantics"` — **zero**
- `"DisCoCat" AND "phase"` — **zero**
- `"illocutionary"` — five hits, none quantitative in the relevant sense. The nearest miss is
  **Schumann, "Modal Calculus of Illocutionary Logic" (arXiv:1102.4636)**, which gives illocutionary
  forces a **many-valued, non-Archimedean** interpretation. That is an exotic *ordered* valuation
  over speech acts — again the ordered branch, not the amplitude branch.

**This is the clean novelty.** The basis is empirically derived (the eleven kinds), which is
precisely the thing the quantum cognition critique says the incumbents lack: their Hilbert spaces
are fitted post hoc, ours is fixed in advance by an independent derivation
(`Core/Generator.lean`, the coordinate-flatness study). That is a real methodological asset and it
should be the headline of any novelty claim — **not** the amplitudes, which are old.

---

## 2. Q2 — THE CONTRACTION QUESTION

**VERDICT: CROWDED-ADJACENT.** The abstract move is named four times over in four fields. The
domain target is occupied by a 2006 paper. The specific composite — *this* deployed grammar as the
contraction of *that* amplitude grammar — is unoccupied, and so is the no-go.

### 2.1 The move already has (at least) four names

| Name | Who | What it says | Proximity |
|---|---|---|---|
| **Maslov dequantization / the idempotent correspondence principle** | Litvinov & Maslov (arXiv:math/0101021); Litvinov (math/0507014, 1203.0522) | Idempotent/tropical mathematics is *"the result of a dequantization of traditional mathematics over numerical fields as the Planck constant ℏ tends to zero **taking imaginary values**"* — and they frame the correspondence explicitly *"in the spirit of N. Bohr's correspondence principle."* The Hamilton–Jacobi–Bellman equation is Maslov dequantization applied to **Schrödinger** | **OCCUPIED.** This is the Inönü–Wigner-flavoured claim, already made, already named, and made at exactly the right level of generality. Note that idempotent semirings are **naturally ordered** (a ≤ b iff a⊕b = b): "kill the phases" and "order the values" are not two steps in this literature, they are **one step**, because idempotency *is* the order |
| **Change of semiring** | Green, Karvounarakis & Tannen, *Provenance semirings* (PODS 2007); Green & Tannen 2017; Grädel & Tannen (arXiv:1712.01980, 1907.08470) | Annotate the computation with elements of a commutative semiring; ℕ[X] (polynomials, positive integer coefficients) is universal, and every specialization — Boolean, tropical, Viterbi, security lattice, probability — is a **semiring homomorphism** out of it | **VERY CLOSE, and the brief's instinct was right.** This *is* bookkeeping-over-semirings, and change-of-semiring is its central move |
| **Tropical tensor networks** | Liu, Wang & Zhang (arXiv:2008.06888) | Identical contraction skeleton; swap ℂ for the tropical semiring; the contraction now returns ground-state energy instead of an amplitude | **VERY CLOSE.** The tensor-network form of exactly our contraction |
| **Tarski / Lawvere Laplacian** | Ghrist & Riess (arXiv:2007.04099); Ghrist, Lopez, North & Riess (arXiv:2501.03890) | Cellular sheaves valued in **lattices with Galois connections** rather than vector spaces, with a Hodge theory whose degree-zero cohomology *"agrees with the global section functor"* — i.e. consensus. The 2025 paper generalizes to **quantale-enriched** categories, making the value object an explicit parameter | **VERY CLOSE, and the most structurally apt of the four.** This is our exact construction's ordered branch: sheaf-over-a-network, value object swapped from linear to ordered, consensus as H⁰ |

### 2.2 The important asymmetry in the provenance frame — assess it hard, as instructed

The brief asked whether provenance semirings are the true incumbent. **They are the right frame,
but the complex direction is the one that frame found hard, and this cuts both ways.**

Grädel & Tannen state plainly that provenance analysis was *"to a large extent, restricted to
positive query languages or the negation-free fragment of first-order logic"*, with abstractions
being *"multivariate polynomials with **positive integer coefficients**."* Handling mere
**negation** required inventing new machinery (a semiring of polynomials with dual indeterminates,
arXiv:1907.08470). Additive inverses are the boundary the field had to build a bridge over.

Two honest consequences:

- **Against us:** if plain negation needed a paper, "complex amplitudes over a provenance semiring"
  is not a new idea the field missed — it is a direction the field is aware of and finds
  structurally awkward. Any claim of novelty here must engage that literature, not step around it.
- **For us:** the difficulty is *real and structural*, not an oversight. It is the same obstruction
  as CEG_REPRESENTATION.md §4.2 (ℂ admits no field order) arriving from the database side. That
  two independent fields hit the same wall is corroboration that the wall is load-bearing — which
  makes the **contraction direction** (ordered ← complex) the defensible one, and the **lifting
  direction** (complex → ordered, "the deployed system is a shadow of an amplitude theory") the one
  carrying the burden of proof.

### 2.3 The domain target is already occupied

`[SECONDARY — OpenAlex metadata, paper not read]` **Theodorakopoulos & Baras, "On trust models and
trust evaluation metrics for ad hoc networks," IEEE JSAC 2006, ~513 citations.** Trust evaluation
as a **semiring path problem**: trust attenuates along a path, aggregates across paths. That is
CEG's attenuation-plus-aggregation structure, as an ordered semiring, twenty years ago.

So the object our construction proposes to *derive* is not an unexamined artifact. It is a
recognized instance of a standard algebraic pattern with a large citation record. Anyone who reads
the CEG monoid/semilattice analysis will place it there immediately.

### 2.4 What the sweep did NOT find

Genuinely empty, on the phrasings tried:

- `"CRDT" AND "quantum"` — **zero**
- `"quantum" AND "reputation system"` — **zero**
- `"quantum" AND "distributed ledger" AND "consensus" AND "classical limit"` — **zero**
- `"Inönü-Wigner contraction"` outside physics — **zero** (all hits are supergravity/AdS)
- `"trust" AND "semiring" AND "propagation"` on arXiv — **zero** (the hits are elsewhere, §2.3)

Quantum social choice exists but is a **different genre**: quantum *speedup* for voting rules
(Liu–Han–Xia–Yu, arXiv:2301.02995), quantum annealing for Kemeny aggregation, and evading
Arrow/Gibbard–Satterthwaite by enlarging the strategy space (arXiv:2309.02593). **None of it
derives a normative rule as a classical limit.** The direction of travel in that field is the
opposite of ours: they add quantum resources to beat a classical impossibility; we would derive the
classical system as a degeneration of a quantum one.

The nearest thing to "amplitudes over trust" is **van der Meer, Hoyte, Roeder & Bruza
(arXiv:2504.13918)**: quantum-like dynamics of *human reliability ratings* in human–AI interaction,
via interaction-dependent Hamiltonians. **NEAREST MISS, but it misses in the right way** — their
amplitudes are over a *human rater's cognitive state*, not over a *trust protocol's value algebra*.
It is quantum cognition applied to a trust topic, not a quantum trust grammar.

### 2.5 Q2 verdict, conservatively

**CROWDED-ADJACENT.** Claiming "we contract an amplitude grammar to an ordered one" as novel would
be a strike, and a well-known one: it is Maslov dequantization, or change of semiring, or the
tropical/linear swap, depending on which room you say it in. Claiming a **no-go** — that ordered
fail-secure aggregation is *necessarily* the order-restriction of a phase structure — is **OPEN**,
unclaimed, and is the only version of this question with a novel answer available. Note that the
obstruction half is already ours and already easy (ℂ has no field order); the hard and unclaimed
half is the **converse**: that every fail-secure ordered aggregator *arises* as such a restriction.
Nothing found bears on it.

---

## 3. Q3 — HOLONOMY AS ATTACK

**VERDICT: OCCUPIED, at theorem strength, and closer than the brief anticipated.**

### 3.1 The finance-gauge literature does state it, as a theorem

| Source | The statement |
|---|---|
| **Vazquez & Farinelli, "Gauge Invariance, Geometry and Arbitrage" (arXiv:0908.3043)** | *"such measure has a geometrical interpretation as a gauge connection. **The connection has zero curvature if and only if there is no arbitrage.**"* Asset present values are given by *"a line integral of the gauge connection"* |
| **Farinelli, "Geometric Arbitrage Theory and Market Dynamics Reloaded" (arXiv:0910.1671)** | *"Write arbitrage as curvature of a principal fibre bundle. **Parameterize arbitrage strategies by its holonomy.** Give the Fundamental Theorem of Asset Pricing a differential homotopic characterization"* |
| **Farinelli & Takada (arXiv:1904.11565)** | The (NUPBR) no-free-lunch condition given *"a geometric characterization … by the **zero curvature (ZC) condition**"* |
| **Ilinski, "Physics of Finance" (arXiv:hep-th/9710148), 1997** | The ancestor: NPV and currency exchange as **parallel transport in a fibre bundle**; interest and exchange rates as **connection components**; unit-of-account redefinition as the **gauge transformation** |

**So the brief's expectation is confirmed and then some.** "No-arbitrage = flatness of a connection"
is not a suggestive analogy in this literature; it is an if-and-only-if, and holonomy is named as
the parameterization of the attack. Our "accountability = enforced zero holonomy" is
**structurally the same theorem**, with `laundering` substituted for `arbitrage`, `delegation
graph` for `market`, and `attenuation` for `discounting`.

### 3.2 Both famous strands carry published refutations — carry this, do not quietly inherit it

- **Sornette, "Gauge Theory of Finance?" (arXiv:cond-mat/9804045)** dismantles Ilinski: the
  log-normal and Black–Scholes "re-derivations" are *"equivalent both in information and
  mathematical content to the simpler and well-known derivation."* The gauge apparatus bought
  nothing that Bachelier and Samuelson had not already bought.
- **Nguyen, "A Response to Economics as Gauge Theory" (arXiv:2112.03460)** does the same to
  Malaney–Weinstein, resolving their conjectures and concluding they *"provide no discernible value
  for the calculation of index numbers or rates of inflation."*

This is the **most important cautionary result in the whole sweep**, and it is exactly the Moreira
& Wichert failure mode from §1.2 recurring in a second field: *a correct and elegant gauge
formalism that changes no answer.* Twice now, in two fields, the amplitude/gauge apparatus has been
imported into a social domain, restated known results in new language, and been shown to add
nothing predictive. **Any claim we make must name the number that changes.**

`[SECONDARY]` Malaney's 1996 Harvard thesis (*The Index Number Problem: A Differential Geometric
Approach*) and Weinstein's Perimeter lecture are not indexed in arXiv or OpenAlex and were **not
read**. Everything above about Malaney–Weinstein is from Nguyen's response only.

### 3.3 The general form is also occupied — and this is the deeper hit

Beyond finance, "consistency = flatness, inconsistency = holonomy" is a developed mathematical
programme on **graphs**, which is our actual setting:

- **Gao, Brodzki & Mukherjee (arXiv:1610.09051)** establish *"the correspondence between
  synchronization problems in a topological group G over a connected graph Γ and the moduli space of
  **flat** principal G-bundles over Γ."* Consistency of pairwise transports **is** flatness. This is
  the K11-with-a-connection object, in general form.
- **Bandeira, Singer & Spielman (arXiv:1204.3873)** give the **graph connection Laplacian** and a
  Cheeger inequality for how far from consistent a system of pairwise ratios is — i.e. a spectral
  measure of accumulated holonomy.
- **Hansen & Ghrist, "Opinion Dynamics on Discourse Sheaves" (arXiv:2005.12798)** put exactly this
  machinery on a *social* network, with sheaves *"that can represent various modes of communication,
  including selective opinion modulation and **lying**."* Disagreement is a cohomological
  obstruction; lying is a non-trivial restriction map.

### 3.4 What is nonetheless still ours — stated conservatively

Three things survive, and only three:

1. **The domain and the sign of the design.** Every incumbent treats non-zero holonomy as a
   *finding* — arbitrage exists, opinions fail to reconcile, transports are inconsistent. CEG treats
   zero holonomy as a **normative requirement enforced at MUST strength for a stated adversarial
   reason** (§13.3 rejects cycle-closing delegation; §11.10 forbids amplification). The published
   theorem says *no-arbitrage implies flat*; CEG's design says *we will make it flat so that the
   attack cannot exist*. That inversion — flatness as an engineered safety property rather than a
   measured market condition — is not in the swept literature, and it is what CEG_REPRESENTATION.md
   §4.4 already derived independently. **This is a design observation, not a theorem, and should be
   graded as one.**
2. **The forward prediction it licenses.** The manufactured-floor warning already staked in
   MAXIMAL_OBJECT.md §"INSTRUMENT EXCLUSION" is strengthened, not weakened, by this sweep: the
   finance literature confirms that flat-by-construction systems have identically zero loop content.
   The prediction was staked before the sweep and survives it.
3. **Nothing in the mathematics.** "Loop gain = fraud" as *phenomenon* is also standard in
   anti-money-laundering practice — cycle detection in transaction graphs is routine (e.g.
   arXiv:1909.01060, arXiv:2509.10715), and currency-arbitrage-as-negative-cycle via log-transformed
   rates plus Bellman–Ford is undergraduate textbook material. **We should claim none of it.**

---

## 4. TWO CORRECTIONS THE SWEEP FORCES

### 4.1 The 55/45/100 counting is an identity for every n, not a fact about 11

For the complete graph K_n: edges = n(n−1)/2, and cycle rank = |E| − |V| + 1 = n(n−1)/2 − n + 1 =
**(n−1)(n−2)/2**. For U(n) after rephasing: angles = n(n−1)/2, physical phases = **(n−1)(n−2)/2**,
total = (n−1)².

These agree **identically, for all n**. At n = 11: 55 edges, 45 loop phases, 100 = 10². At n = 3:
3 edges, 1 loop phase, 4 = 2² — the familiar CKM count. The agreement is not a coincidence to be
discovered at 11; it is the reason the CKM phase count works at all, and it is standard discrete
gauge theory on a graph (gauge group U(1)^V acting on U(1)^E, quotient H¹(G; U(1)) of rank equal to
the cycle rank).

**Consequence for the page:** MAXIMAL_OBJECT.md's *"55 + 45 = 100, **exactly** the generalized
mixing-parameter count of U(11)"* reads as though a non-trivial check was passed. No check was
passed — it could not have failed. The honest phrasing is that the eleven kinds are being given the
standard structure of a U(1) connection on K₁₁, whose loop content is its first cohomology; the
parameter counts then agree by a graph-theoretic identity. **The content of the wager is entirely in
whether the phases are non-zero and measurable, not in the counting.** This costs the object nothing
it should have had, and removes a claim that a referee would puncture in one line.

### 4.2 The founding NonFactoring shape has a large, named literature

`Core/NonFactoring.lean` states: two wholes agreeing under every partial view, differing in the
quantity. That is, in the general case, **contextuality**, and it has been formalized
sheaf-theoretically for fifteen years:

- **Abramsky & Brandenburger (arXiv:1102.0264)**: *"contextuality, and non-locality as a special
  case, correspond exactly to **obstructions to the existence of global sections**."* Their framework
  is parameterized by an arbitrary commutative semiring, so the change-of-semiring axis of §2 is
  built into it.
- **Abramsky, Mansfield & Barbosa (arXiv:1111.3620)**: the obstruction as a **Čech cohomology
  class** — the cohomological invariant for "pairwise consistent, globally not."
- **Abramsky, "Relational Databases and Bell's Theorem" (arXiv:1208.6416)**: *"a remarkably direct
  correspondence"* between Bell's theorem and well-studied questions in **relational database
  theory** — precisely the record layer.
- **Abramsky, Barbosa, Kishida, Lal & Mansfield, "Contextuality, Cohomology and Paradox"
  (arXiv:1502.03097)** extends the unified view to database theory explicitly.
- **Atserias & Kolaitis, "Consistency of Relations over Monoids" (JACM 2025)**: local-to-global
  consistency across *"probability theory, relational databases, and quantum information"*, with
  **acyclicity** as the condition for local-to-global consistency.

**This is the closest prior art to the construction as a whole**, closer than quantum cognition and
closer than DisCoCat, because it already unifies the four things our construction assembles: a
record/relational layer, semiring-valued bookkeeping, the pairwise-blind-to-the-whole shape, and a
cohomological obstruction that lives in loops. That Atserias–Kolaitis ties local-to-global
consistency to **acyclicity** is the same structural fact CEG_REPRESENTATION.md §4.4 derived from
§13.3's cycle rejection, reached from the other side.

The existing `NonFactoring` results are not thereby wrong or worthless — they are machine-checked,
which this literature largely is not, and they are specific exhibited witnesses. But the **shape** is
not ours, the cohomological reading of it is not ours, and the programme's convergent-art house rule
applies: this is a **HIT** — corroboration plus free machinery — and Abramsky's school should be
credited by name wherever the shape is stated.

---

## 5. WHAT REMAINS CLAIMABLE

Stated conservatively, in descending order of confidence.

1. **The basis, not the amplitudes.** An **empirically derived, independently fixed** semantic basis
   (the eleven kinds: generator-derived, coordinate-flat at p<0.01 across 5,994 judgments, 11 = 4+7
   mechanized) is exactly what the standing critique of quantum cognition says the incumbents lack —
   their Hilbert spaces are fitted after the phenomenon. **This is a methodological claim about
   provenance of the basis, and it is clean.** It is also the only claim in this document that the
   sweep found no competitor for.
2. **Amplitudes over a change/act taxonomy is an empty cell.** Zero hits on every phrasing. Claimable
   as *"we know of no prior construction placing amplitudes over kinds of change"* — **with** the
   method disclosure of §0, since psychology and HCI venues were not swept.
3. **Machine-checked status.** `cp_phase_invisible_to_pairs`, `nonfactoring_*`, `bell_ceiling_*` are
   mechanized. The contextuality and finance-gauge literatures are, as far as this sweep saw, not.
   Mechanization of a known shape is a real but modest contribution and must be graded as
   scope-corroboration, per `shared-lemma-one-witness`.
4. **The no-go, if it can be proved.** "Every fail-secure ordered aggregator is the order-restriction
   of a phase structure" is unclaimed. The easy half (ℂ has no field order, so they cannot share a
   layer) is already in hand; the converse is open and is the only place a genuinely new theorem is
   available.
5. **Flatness-as-engineered-safety.** The inversion in §3.4(1). A design observation, not a theorem;
   worth one line, not a claim.

### What must NOT be claimed

- ❌ "Contraction of an amplitude structure to an ordered one" as a novel move — **Maslov
  dequantization**, and it is explicitly Bohr-correspondence-framed.
- ❌ "No-arbitrage/no-laundering = zero holonomy" as ours — **Vazquez–Farinelli 2009**, if-and-only-if.
- ❌ "Loop gain = fraud" as a formalization — folklore in AML; textbook via Bellman–Ford.
- ❌ "55 + 45 = 100 matches U(11)" as a passed check — an identity for all n (§4.1).
- ❌ "Pairwise-blind-to-the-whole" as a new shape — **Abramsky–Brandenburger 2011**, with a Čech
  cohomology invariant and an explicit database bridge.
- ❌ Trust-as-ordered-semiring-composition as an unexamined artifact — **Theodorakopoulos & Baras
  2006**, ~513 citations.

### The standing hazard, named once

Two independent fields have now imported gauge/amplitude apparatus into a social domain, produced
elegant restatements, and been shown by referees to have changed no answer (Sornette on Ilinski;
Nguyen on Malaney–Weinstein) — and a third has been told its interference terms do no work (Moreira
& Wichert on quantum cognition). **Three for three.** The base rate for this class of construction
delivering a number that would not otherwise have been obtained is, on the swept record,
approximately zero. Discipline rule 6 applies with unusual force: only a **confirmed advance
prediction** should move this object, and the prediction must name the quantity that changes.

---

## SOURCES

All arXiv identifiers verified by direct API fetch on 2026-08-21; OpenAlex items marked
`[SECONDARY]` where only metadata was retrieved.

**Q1 — incumbents.** arXiv:1706.05080 (Moreira & Wichert, *Are Quantum Models for Order Effects
Quantum?*); arXiv:1604.08268 (Aerts et al., *Quantum Cognition Beyond Hilbert Space I* — the
order-effects/replicability impossibility); arXiv:1508.03686 (Aerts & Sassoli de Bianchi, GTR
model); arXiv:2302.03012 (Widdows, Rani & Pothos, quantum circuits for decision-making);
arXiv:1105.1702 (Sadrzadeh & Grefenstette, DisCoCat constructions); arXiv:1601.04908
(Bankova–Coecke–Lewis–Marsden, graded entailment — the Löwner order); arXiv:2005.04147 (Meichanetzidis
et al., QNLP pipeline); arXiv:1608.01401 (Ashoush & Coecke, dual density operators);
arXiv:1102.4636 (Schumann, modal calculus of illocutionary logic).

**Q2 — contraction.** arXiv:math/0101021 (Litvinov & Maslov, *Correspondence principle for
idempotent calculus*); arXiv:math/0507014, arXiv:1203.0522 (Litvinov, Maslov dequantization; HJB as
dequantized Schrödinger); arXiv:1712.01980, arXiv:1907.08470 (Grädel & Tannen, semiring semantics;
the positivity restriction and the negation construction); arXiv:2202.10766 (Bourgaux et al.,
semiring provenance for Datalog); arXiv:2008.06888 (Liu, Wang & Zhang, tropical tensor networks);
arXiv:2007.04099 (Ghrist & Riess, Tarski Laplacian); arXiv:2501.03890 (Ghrist, Lopez, North & Riess,
Lawvere Laplacian, quantale-enriched); arXiv:2005.12798 (Hansen & Ghrist, discourse sheaves);
arXiv:2504.13918 (van der Meer, Hoyte, Roeder & Bruza, quantum-like trust dynamics);
arXiv:2301.02995, arXiv:2309.02593 (quantum voting — different genre). `[SECONDARY]` Green,
Karvounarakis & Tannen, *Provenance semirings*, PODS 2007; Green & Tannen, *The Semiring Framework
for Database Provenance*, 2017; Theodorakopoulos & Baras, IEEE JSAC 2006 (trust as semiring path
problem, ~513 cites).

**Q3 — holonomy.** arXiv:0908.3043 (Vazquez & Farinelli, zero curvature iff no arbitrage);
arXiv:0910.1671 (Farinelli, arbitrage strategies parameterized by holonomy); arXiv:1904.11565
(Farinelli & Takada, NUPBR as zero curvature); arXiv:hep-th/9710148 (Ilinski, gauge theory of
arbitrage); arXiv:cond-mat/9804045 (Sornette, the refutation); arXiv:2112.03460 (Nguyen, response to
Malaney–Weinstein); arXiv:1610.09051 (Gao, Brodzki & Mukherjee, synchronization ≅ flat bundles);
arXiv:1204.3873 (Bandeira, Singer & Spielman, graph connection Laplacian); arXiv:1909.01060,
arXiv:2509.10715 (laundering cycles, empirical).

**§4.2 — the NonFactoring shape.** arXiv:1102.0264 (Abramsky & Brandenburger); arXiv:1111.3620
(Abramsky, Mansfield & Barbosa, cohomology); arXiv:1208.6416 (Abramsky, *Relational Databases and
Bell's Theorem*); arXiv:1502.03097 (Abramsky et al., *Contextuality, Cohomology and Paradox*);
arXiv:1701.00656, arXiv:1807.04203 (Carù, limits of the cohomological invariant). `[SECONDARY]`
Atserias & Kolaitis, *Consistency of Relations over Monoids*, JACM 2025.

**Programme context.** `/home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/CEG_REPRESENTATION.md`
§0, §3.4, §4.2, §4.4; `/home/emoore/CIRISOntology/scratchpad/MAXIMAL_OBJECT.md`;
`/home/emoore/CIRISOntology/CLAUDE.md` discipline rules 1–7.
