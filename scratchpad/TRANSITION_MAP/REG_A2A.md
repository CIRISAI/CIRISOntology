# REG — the apples-to-apples table, re-derived at the CEG standard (T-A2A, 2026-08-21)

**Question put:** does REG v0.2 meet the apples-to-apples test against flavour dynamics
(`C^n`, `U(n)`, rephasing invariants, unitarity, `|U_ij|²` readout) — at the same standard as
`CEG_REPRESENTATION.md`, with every row flagged BY-CONSTRUCTION or CONTINGENT?

**Register, stated once and binding on every line below.** This is a **STRUCTURAL COMPARISON** of
a *specification* against a *physical theory's algebra*. Nothing here derives physics from REG or
REG from physics; the `sm_escalator` fence (`a function of C cannot output a property that C does
not determine`) applies in the same words it applied to CEG. Additionally, and unlike the CEG
analysis: **REG is a spec written today (2026-08-21), not a deployed system with a conformance suite.**
Every derivation below is about a spec of ~70 lines, and where the spec is silent I
say so rather than filling it in. Where filling it in is unavoidable I mark the fork and derive
**both branches**.

**The anti-tautology discipline, stated before any result.** REG was constructed by taking the
other branch at each fork the CEG analysis identified: `C` instead of an ordered lattice, group
instead of monoid, holonomy observable instead of forbidden, exact conservation instead of
attenuation. A table that scores those four choices as four passes has measured nothing but its own
construction. So every row below carries a second verdict, and the document's own falsifiability
condition is stated up front: **if the CONTINGENT rows all pass, the analysis is worthless, because
the contingent rows are the only place REG could have failed.** They do not all pass. Five of seven
carry information, and four of those five come out against REG.

---

## 0. Verdicts up front

| # | Row | Comparison verdict | Anti-tautology flag |
|---|---|---|---|
| **R1** | **State space** | **MATCH in the field, STRUCTURED MISMATCH in the norm** — `C^{S×D}` is complex and finite-dimensional (match), but the per-cell bound `\|z\| ≤ 1` makes it the **ℓ^∞ polydisc**, not the ℓ² ball | **BY-CONSTRUCTION** for "complex"; **CONTINGENT** for the norm — **and the contingent half fires** (§2.1) |
| **R2** | **Dynamics object** | **STRUCTURED MISMATCH, both layers.** Value layer: an **abelian translation group** `(C,+)^{cells}` acting simply transitively — no invariants at all. Record layer: **not a group** — a non-regular monoid with trivial unit group, the same class as CEG | **CONTINGENT, and it refutes the spec's own claim** (§3) |
| **R3** | **Gauge / redundancy sector** | **STRUCTURED MISMATCH.** REG's bundle is trivialised by a global section (the stance calibration), so **zero residual phases** — the same endpoint as CEG, reached by the opposite route | **CONTINGENT — the most informative row after R7** (§4) |
| **R4** | **Conservation law** | **NAME MATCH, SHAPE MISMATCH.** `\|w\| = 1` on a channel is *per-wire* norm preservation; unitarity is *across-channel* row-sum conservation. REG has no cross-dimension structure, so it has no analogue of `Σ_j \|U_ij\|² = 1` | **BY-CONSTRUCTION** (the spec chose "exact conservation default"), **and the pass is spurious** (§7.4) |
| **R5** | **Irreversibility** | **MATCH at the readout, FORCED DICHOTOMY at the record.** *Invertible* and *loses nothing* are **not jointly satisfiable**; REG must pick, and picking invertible spends the Record kind | **CONTINGENT — the by-construction attempt fails** (§3.2) |
| **R6** | **Readout** | **MATCH IN SHAPE — the closest row.** Both `\|·\|²`, both many-to-one, both phase-blind. Two contingent defects underneath: it **destroys polarity**, and it carries **one index where flavour carries two** | **BY-CONSTRUCTION** for the form; **CONTINGENT** for the defects, which fire (§5) |
| **R7** | **"Mixing matrix"** | **INCOMPARABLE — REG has none.** Every generator is diagonal in the kind basis, and the state space's own norm **provably excludes** the mixing group | **CONTINGENT — the decisive row** (§2.1, §6) |

### The single most consequential result, stated up front

**REG's entire dynamical group is contained in flavour's *gauge* group.**

Every operation REG defines acts on the amplitude field either by translation (`attest`,
`withdraws`, `supersedes`) or by a **per-cell phase** (`recants`; `delegates_to`'s edge weight).
The unitary part of that is `U(1)^{cells}` — the diagonal torus. On the flavour side the diagonal
torus is exactly the rephasing group: the part that is quotiented out, the part carrying no
physical content, the part `cp_phase_invisible_to_pairs` is about being invisible *to*. Everything
flavour calls physical — the off-diagonal moduli `|U_ij|` and the 45 surviving phases — lives in
`U(11)/T`, and **no REG generator has a single nonzero off-diagonal matrix element.**

This is not a near miss. It is the statement that REG, built expressly to be the branch that
*could* carry the maximal object, occupies the complement of the sector the maximal object is
about. And it is doubly forced: once by the generators (no cross-kind verb exists), and once,
independently, by the state space (§2.1 — the per-cell confidence bound makes the state space an
ℓ^∞ polydisc, whose linear symmetry group is the monomial group `U(1)^n ⋊ S_n`, i.e. precisely the
mixing-free subgroup). **Two independent blocks means the finding survives either repair alone.**

### The second most consequential result

**Both grammars are forced flat, by different mechanisms, and the second mechanism is worse news
for the maximal object than the first.**

CEG is flat by threat model (three anti-attack MUSTs — `CEG_REPRESENTATION.md` §4.4). REG is flat
by **readout well-definedness**: a verdict that is a coherent sum over attesters is a function of
the record *if and only if* the inter-attester frame connection is flat (§4.3). The instrument
exclusion staked in `MAXIMAL_OBJECT.md` therefore generalises, and I stake the generalisation now,
before any measurement exists:

> **FORWARD PREDICTION (staked 2026-08-21, before any REG instrument exists).** Any grammar whose
> readout is required to be a deterministic function of the record — i.e. any *verdict-producing*
> grammar, adversarial or not — reads zero loop phase by construction. Removing CEG's threat model
> is **not sufficient** to build a loop-phase instrument. The instrument must be a substrate whose
> aggregation is *permitted to be route-dependent*, which means it cannot be an accountability
> protocol at all.

---

## 1. The object, written down

REG v0.2 = CEG's five verb surfaces, amplitude semantics underneath (`TREL_RESULTS.md`; v0.1's
abstract verbs scored 1/5 on corpus legibility and were withdrawn). Formalising the spec so the
derivations are checkable:

```
Cells      X = S × D            subjects × dimensions (D = the eleven kinds, by default)
Amplitude  z ∈ C, |z| ≤ 1       per attestation.  |z| = confidence, arg z = stance angle
                                (0 = full assertion, π = full denial)
Field      A : X → C            A(x) = Σ over live attestations at x
Record     R = the emission sequence, "group-composable, invertible — loses nothing"
Readout    V(x) = |A(x)|²       ordered, lossy, phase-blind; the ONLY place order appears
```

The five verbs, with their CEG preconditions retained (the v0.2 surface *is* CEG's, so its
preconditions come with it):

| verb | precondition | effect on `A(x)` | effect on `R` |
|---|---|---|---|
| `scores` / attest | none | `A += z` | append |
| `delegates_to` / channel | scope edge admissible | multiply by edge weight `w`; `\|w\| = 1` by default | append |
| `supersedes` / rotate | referent resolves | `A += (z' − z)` | append |
| `withdraws` / invert | referent resolves **AND** issuer authorised | `A −= z` | append |
| `recants` / flip | referent resolves **AND** issuer is the **original attester** | `A −= 2z` (`z ↦ e^{iπ}z`) | append |

**Two preconditions do all the algebraic work below**, and neither was designed with the algebra in
mind: **prior-existence** (the referent must resolve) and **ownership** (`recants` needs the
original attester; `withdraws` needs one of CEG's four authority paths). The brief is right that
these are partiality constraints. They are the reason the answer to C1 is not "group".

---

## 2. R1 — the state space, and the theorem hiding in `|z| ≤ 1`

### 2.1 The norm is ℓ^∞, and ℓ^∞ has no mixing group

The spec bounds the amplitude **per cell**: *"assigns to each (subject, dimension) an amplitude z in
C with |z| <= 1."* Not `Σ_d |z_d|² ≤ 1`. This is not a drafting accident — it is forced by the
semantics, and the semantics is right: an attester may be fully confident about a change's **Facts**
*and* fully confident about its **Rules** simultaneously. Confidence across the eleven kinds is not
a budget and must not be normalised. So:

```
REG state space (per subject) = { z ∈ C^11 : max_d |z_d| ≤ 1 }   — the closed POLYDISC, ℓ^∞ ball
Flavour state space           = { z ∈ C^3  : Σ_j |z_j|² = 1 }    — the SPHERE / projective space, ℓ²
```

Two classical theorems apply, and both cut the same way.

**(i) Linear isometries of `ℓ^∞_n(C)` are the monomial matrices** (Banach–Stone applied to
`ℓ^∞_n = C(K)` on `n` points; equivalently the `p ≠ 2` case of Banach–Lamperti). Every surjective
linear map preserving the polydisc is a permutation composed with a diagonal unimodular matrix:

```
Isom(ℓ^∞_n) = U(1)^n ⋊ S_n     — the maximal torus and its Weyl group
```

That group is **exactly the mixing-free subgroup of `U(n)`**: the normaliser of the maximal torus.
The coset space `U(n)/T`, where the moduli and all `(n−1)(n−2)/2` phases live, does not act on
REG's state space at all.

**(ii) Poincaré (1907): the polydisc and the ball are not biholomorphic for `n ≥ 2`**, and
`Aut(D^n) = (Aut D)^n ⋊ S_n` (Rudin). So the obstruction is not an artifact of insisting on linear
maps — there is no holomorphic change of coordinates that turns REG's state space into one the
mixing group acts on.

**VERDICT R1: MATCH in the field (both complex, both finite-dimensional), STRUCTURED MISMATCH in
the norm — and the mismatch is not cosmetic, it is the whole mixing sector.**

**FLAG: BY-CONSTRUCTION for the complex field** (REG was *defined* as the complex branch; scoring
this a pass measures nothing). **CONTINGENT for the norm, and it fires against REG.** The spec
could have written `Σ_d |z_d|² ≤ 1` and did not; it did not because the corpus semantics forbids
it. The chain is worth stating in one line because it is the deepest thing in this document:

> **The semantics of confidence forbids the mixing matrix.** Confidence across kinds is not a
> distribution, so the norm is ℓ^∞, so the state space is a polydisc, so the linear symmetry group
> is monomial, so there is no mixing.

**The repair, and its price.** Normalising across kinds (`Σ_d |z_d|² = 1`) restores the ball and
lets `U(11)` act — at the cost of asserting that confidence on Facts trades off against confidence
on Rules, which the corpus contradicts directly (an edit can be strongly *both*). This is a real
fork and I do not resolve it; I record that **the mixing sector and the confidence semantics cannot
both be had on this state space.**

### 2.2 The residue that does match

Positively: REG's state space is genuinely finite-dimensional and genuinely complex, and it has an
inner product available. CEG had neither (`CEG_REPRESENTATION.md` §4.1: *"an unbounded, append-only,
decaying multiset … no linear structure, no inner product, no dimension"*). That is a real
improvement, and it is exactly the improvement REG was built to deliver — hence uninformative as a
test, and marked so.

---

## 3. C1 — does the record layer form a group?

**ANSWER: NO. Not a group, not an inverse semigroup. Under the spec's own "loses nothing" clause it
is a non-regular monoid with trivial unit group — algebraically the same class as CEG. The most REG
can reach is a GROUPOID, and only by spending the Record.**

### 3.1 The claim is self-contradictory before any precondition is consulted

The spec asserts three properties of the record layer at once: **group-composable**, **invertible**,
**loses nothing**. Take them as written.

**Theorem (no lossless invertible record).** Let `F` be the free monoid on the generator set (the
emission sequences) and `ρ : F → T` the map to whatever the record layer *is*. "Loses nothing" is
the statement that `ρ` is **injective**. "Group" is the statement that `ρ(F)` is a group.

*Proof.* Suppose `ρ(F)` is a group containing a non-identity element `g = ρ(a)`. Then `g⁻¹ ∈ ρ(F)`,
so `g⁻¹ = ρ(b)` for some `b ∈ F`, and `ρ(ab) = gg⁻¹ = 1 = ρ(ε)`. But `ab ≠ ε` in the free monoid
(`|ab| = |a| + |b| > 0`). So `ρ` is not injective. Contrapositive: if `ρ` is injective, `ρ(F)` is a
free monoid, whose only invertible element is the identity. ∎

So `{group, invertible, lossless}` is **unsatisfiable for any non-trivial operation set** — a
one-line result, independent of complex values, independent of the preconditions, and it refutes the
spec's own sentence. The choice is forced:

- **Retention branch** (`withdraws` marks, CEG §11.8.2 *"remains in the audit chain"*): `ρ` is
  injective, append is length-monotone, the CEG grading theorem transfers **verbatim** — trivial
  unit group, non-regular (`attest · x · attest ≠ attest` by length for every `x`), not an inverse
  semigroup. **REG's record layer is then in the identical algebraic class as CEG's, and the
  complex values changed nothing.**
- **Deletion branch** (`withdraws` removes the row): `ρ` is invertible on that pair and **lossy** —
  the history `attest; withdraw` is identified with `ε`. Record content is destroyed exactly where
  `repairable_does_not_factor` says it lives.

**This is the sharpest single finding about REG's algebra:** the fork "group instead of monoid at
the record layer", which REG's construction treats as a free choice, **is not available**. The
record algebra is about append structure and preconditions, not about what the values are. Making
the values complex buys nothing here.

### 3.2 The layer correction, applied to REG

`MAXIMAL_OBJECT.md` §"LAYER CORRECTION" establishes that unitarity is Record-*preserving*
(bijective — both injective and invertible). How does `U(n)` have both when REG cannot?

Because flavour's state space is **not append-structured**. `U` acts bijectively on a fixed-dimension
vector; the state is *replaced*, not accumulated. And flavour is lossy in exactly the place REG would
have to be: **the factorisation is not recoverable.** `U₁U₂ = U₃` identifies two histories with one
element. So flavour occupies the *invertible-and-history-lossy* corner — the deletion branch — and
pays the same price, which is why "the past is exactly recoverable" in flavour means *the initial
state*, never *the route*.

**Corollary, and it is a correction to the REG construction's motivation:** REG cannot be
simultaneously more flavour-like *and* more Record-carrying than CEG. Those pull in opposite
directions on the same axis. CEG is at the lossless-non-invertible end; flavour is at the
invertible-lossy end; **REG as specified claims a point that does not exist.**

### 3.3 Group, groupoid, or inverse semigroup — the actual answer

Now bring in the preconditions, and work the deletion branch (the retention branch is settled above:
non-regular monoid, done).

**Not a group, because composition is essentially partial.** A group is a one-object groupoid: every
element composes with every element. `withdraws(id)` is undefined at any state where `id` does not
exist. That partiality is not removable without discarding the prior-existence precondition, which
is the precondition that makes `withdraws` mean anything. **Prior-existence is the group obstruction.**

**Ownership is *not* the group obstruction — and that turns out to be the whole story of C4.**
Ownership restricts *which attester may emit* an inverting generator; it does not remove any
generator's own inverse (`a` can always withdraw `a`'s own attest). So ownership is compatible with
groupoid structure. What ownership does instead is far more consequential: §5.2 shows it has **no
shadow whatsoever on the readout**.

**Not an inverse semigroup, on the spec's likeliest reading.** An inverse semigroup needs the
generating set closed under partial inverses. Checking each:

| generator | partial inverse admissible? |
|---|---|
| `attest(a,x,z)` | **yes** on the deletion branch — `withdraws` by `a` |
| `withdraws(a,id)` | **no** on fresh-assigned ids — restoring requires re-creating *that id*, and `attest` mints a new one. **Yes** on content-derived ids |
| `supersedes(id, z→z′)` | **yes** — `supersedes(id, z′→z)`, provided cross-attester supersedes is admissible (LEG_B §7 flags the same-attester clause descriptive-not-enforced) |
| `recants(id)` | **yes iff `recanted` is not absorbing** — `flip` is an involution on the value (`e^{iπ}·e^{iπ} = 1`), REG's one honest involution. CEG makes `recanted` terminal (§6.1 rule 1); if REG inherits that, `flip²` is inadmissible and `flip` has no inverse move |

So regularity turns on **two spec forks REG has not decided**: *(F1)* are attestation ids
content-derived or arrival-assigned? *(F2)* is `recanted` absorbing? These are the same two forks
`CEG_REPRESENTATION.md` §5.3 flagged as spec-interpretation, arriving again — REG inherited them
along with the verb surface.

**The best case, stated exactly.** On the deletion branch, with content-derived ids and
non-absorbing `recants`, the structure is the **category whose objects are record-states and whose
arrows are admissible emissions, and every arrow is invertible — a GROUPOID**, not a group. The
group fails on partiality; the inverse-semigroup reading is available too (a groupoid is an inverse
semigroup once you adjoin a zero for undefined composites), but *groupoid* is the honest name because
the partiality is typed by states, not by an absorbing element.

**C1 VERDICT: at best a GROUPOID; as written, a non-regular monoid; never a group. The obstruction
is prior-existence, and it is untouched by the value algebra.**

---

## 4. C2 — does interference actually go through? (the gauge question)

**ANSWER: only on the horn where it is trivial. There is a real dichotomy, both horns are bad for
the maximal object, and the interesting middle case is self-limiting.**

### 4.1 The spec pins the phase — which is the problem, not the solution

REG's second sentence fixes the phase absolutely: *"0 = full assertion, pi = full denial,
intermediate angles = partial reframings."* An absolutely calibrated angle is a **locally visible**
coordinate. And `MAXIMAL_OBJECT.md` defines the object's phases by the opposite property:

> *"Magnitudes are locally visible (what mixes, how strongly); phases are NOT locally visible — they
> are discovered only by going around loops."*

`CEG_REPRESENTATION.md` §3.2 disqualified CEG's `Z2` sign for exactly this reason — *"locally
visible, which is exactly what the interferometer's phases are defined not to be."* **The same
disqualification applies to REG's stance angle, and lifting `Z2` to `U(1)` does not repair it.**
REG's arc is a richer *stance coordinate*; it is not a connection. A locally visible phase is an
observable, and an observable is not a gauge sector.

### 4.2 Horn 1 — the anchor is shared

If a cell `(subject, dimension)` names one proposition, then every attester's `arg z = 0` means the
same thing, amplitudes are directly comparable, and cross-attester interference is well-defined and
gauge-independent. Good — no defect. But then:

- The bundle is **trivialised by a global section** (the assertion axis is a canonical frame). Zero
  residual phases survive gauge fixing. **This is the same endpoint as CEG's `(Z2)^k`
  omit-vs-materialise freedom** (`CEG_REPRESENTATION.md` §4.1: *"its bundle is trivial and zero
  residual phases remain"*) — reached by the opposite route, and it is the reason the R3 verdict
  below is MISMATCH and not MATCH.
- The construction reduces to **vector-valued scores in `R²` with a quadratic readout**. Restricted
  to `θ ∈ {0, π}` — the only two angles the corpus produced determinate readings for (`TREL_RESULTS`)
  — `Σ z_i` is real and `|Σ|²` is a strictly monotone reparametrisation of CEG's signed
  mean-of-`score×confidence`. **On the two-angle sublattice REG's readout carries no information CEG
  did not.** That is the Moreira–Wichert failure mode arriving exactly on schedule
  (`AMP_GRAMMAR_PRIOR_ART.md` §1.2: *"quantum interference effects play no role … formally quantum
  and operationally classical"*), and the prior-art sweep's standing hazard (three-for-three) says it
  should have been the prior expectation.

### 4.3 Horn 2 — the anchor is per-attester (the honest reading)

A REG cell is `(subject, dimension)`, and a **dimension is a kind of change, not a proposition**.
`Facts` is not a claim; it is a category. "I fully assert *at the Facts coordinate*" does not name a
truth-apt content that two attesters could be asserting *the same one of*. So attester `i`'s zero and
attester `j`'s zero are anchored to different things, and the relative phase between them is **not
determined by the spec**. That is a per-attester `U(1)` rephasing freedom, and it is fatal in a
specific, provable way:

**Theorem (moduli-only).** If `z_i ↦ e^{iα_i} z_i` is a redundancy (independent `α_i` per attester),
then the orbit of `(z_1,…,z_m)` under `U(1)^m` is determined by `(|z_1|,…,|z_m|)`. Hence **every
gauge-invariant readout factors through the multiset of moduli**, and no function of the multiset
that depends on relative phase is well-defined. `|Σ z_i|²` is not gauge-invariant:
`|Σ e^{iα_i} z_i|² ≠ |Σ z_i|²`. ∎

**Consequence: under Horn 2, interference is not merely unobservable — the verdict is not a function
of the record.** And the gauge-invariant remainder is *the moduli alone*, which is exactly the
information CEG composes over. **The gauge argument, run honestly, returns REG to CEG's regime.**

### 4.4 The middle case — a partial frame connection, and this IS the interesting outcome

The brief asks whether the problem *forces a connection / reference-frame structure*. It does, and
here is the structure, stated exactly.

Suppose the frames are related pairwise where they can be: a transport `g_{ij} ∈ U(1)` carrying
attester `j`'s stance frame into attester `i`'s, defined on the edges of an **attester agreement
graph** `Γ`. This is a `U(1)`-connection (a 1-cochain) on `Γ`, with gauge action
`g_{ij} ↦ e^{iα_i} g_{ij} e^{−iα_j}`. Aggregation relative to a base attester `0` is
`Σ_i g_{0i} z_i`, transported along a spanning tree.

**Theorem (aggregation is well-defined iff flat).** `Σ_i g_{0i} z_i` is independent of the choice of
spanning tree **iff** the connection has trivial holonomy around every cycle of `Γ`. If some cycle
carries `W ≠ 1`, two spanning trees give aggregates differing by a factor of `W` on the affected
attesters, and the verdict depends on a bookkeeping choice. ∎

This is Gao–Brodzki–Mukherjee's *synchronisation ≅ flat principal bundles* (arXiv:1610.09051)
arriving in REG, and Bandeira–Singer–Spielman's connection Laplacian (arXiv:1204.3873) supplies the
spectral measure of how far from flat a given attester population is. Credited, per the
convergent-art rule; the mathematics is theirs.

**And this is where the interesting outcome turns out to be self-limiting.** REG's readout is
*specified* to be a deterministic verdict. So REG **requires** the flat case. A grammar whose
readout is a coherent sum is **forced flat by well-definedness alone** — no threat model needed.
Hence the generalised instrument exclusion in §0.

**This also revises the CEG safety story, and the revision is a real result.** CEG carries three
flatness requirements, and `CEG_REPRESENTATION.md` §4.4 reads all three as anti-attack armour. The
derivation here says the first of the three is **not armour**: *order-independent composition is
forced by well-definedness of any route-independent readout*, adversaries or none. Only **acyclic
delegation** and **non-amplifying attenuation** are threat-motivated. The safety principle's "every
CEG defense becomes derivable as REG minus a named threat" survives — but one of the three defenses
turns out to have no threat under it, and REG is what shows that.

### 4.5 C2 verdict

**(a) is avoided, (b) arrives and is self-cancelling.** There is no gauge-dependence defect *if* the
absolute calibration holds — and then the phases are locally visible and there is no phase sector.
There *is* a real per-attester gauge freedom on the honest reading of what a dimension is — and then
the complete invariants are the moduli and interference is not observable at all. The connection
structure genuinely is forced in the middle case, which is the outcome the brief hoped for; but the
same construction shows REG's own readout requires that connection to be **flat**. **REG has
decorative phases at the attestation layer, not a 45-phase sector.**

---

## 5. C3 — what are REG's actual invariants?

### 5.1 The inventory

| freedom | is it a redundancy in REG? | invariants that survive |
|---|---|---|
| **global** `z ↦ e^{iα}z` (all attestations, all cells) | **Not a symmetry of the theory** (stance semantics is pinned) but **is a symmetry of the readout** (`\|Σ\|²`) | everything; but see §5.3 — the readout having *more* symmetry than the theory is itself the polarity defect |
| **per-attester** `z_i ↦ e^{iα_i}z_i` | Horn-dependent (§4) | if gauge: **the moduli `\|z_i\|` only**. If not gauge: everything, including relative phases |
| **per-cell** `A(x) ↦ e^{iα_x}A(x)` | not admitted — cells are independent, no cross-cell op relates them | vacuous |
| **frame connection** `g_{ij}` on the attester graph | gauge, in the middle case | **the moduli + the Wilson loops** `W_C = ∏_{e∈C} g_e` |
| **channel weights** `w_e` on the delegation graph | calibrated against stance, so **observable**, not gauge | the individual `w_e`, hence loop products as derived quantities |

### 5.2 Is there a REG-Jarlskog?

**Yes, and it is on the wrong graph.**

The Jarlskog invariant is the imaginary part of the smallest rephasing-invariant plaquette,
`J = Im(U_ij U_kl U*_il U*_kj)`. Its graph-theoretic analogue on a `U(1)` connection is the smallest
loop holonomy — the **triangle**:

```
W_{ijk} = arg( g_ij · g_jk · g_ki )  ∈ U(1)     — invariant under every per-attester rephasing
```

**This is a genuine invariant, it is the smallest one, and it has a measurement.** Measure the
relative stance of attesters `i,j` on a common cell (from their interference), likewise `j,k` and
`i,k`; the holonomy is `φ_ij + φ_jk − φ_ik`. Non-zero means: **three attesters pairwise reconcilable
but not jointly reconcilable.** That is the founding `NonFactoring` shape verbatim — two wholes
agreeing under every partial view, differing in the quantity — and it is Abramsky–Brandenburger's
obstruction to a global section (arXiv:1102.0264), credited.

**But the base graph is ATTESTERS, not KINDS.** The maximal object's 45 phases live on `K11` —
vertices are the eleven kinds, edges are cross-kind channels. `W_{ijk}` is an invariant of who is
attesting, not of what mixes with what. **REG supplies a Jarlskog-analogue on the wrong base space.**

And REG's own readout requires `W_{ijk} = 1` (§4.4). So REG's one non-trivial invariant is one the
spec's readout forbids from being non-trivial.

### 5.3 The invariant REG destroys

`|Σ z_i|²` is invariant under `Σ ↦ −Σ`. **So the verdict cannot distinguish unanimous assertion from
unanimous denial.** Both give `|R|²`. Mixed opinion gives `≈ 0`.

REG encodes polarity **in the phase** and then reads out **phase-blind**. The verdict measures
*coherence*, not *valence*. For a trust grammar this is disqualifying on its face — "every attester
says this key is revoked" and "every attester says this key is valid" produce the identical verdict —
and it is an internal inconsistency in the spec, not an interpretation of it. It is also the exact
inverse of CEG, whose readout preserves the sign, which is what makes fail-secure "any negative
trumps positive" expressible at all.

### 5.4 The trilemma

The three attempts to repair §5.3 exhaust the options, and they do not compose:

> **REG READOUT TRILEMMA.** No readout has all three of:
> **(a) gauge-independence** (invariant under per-attester rephasing);
> **(b) polarity preservation** (distinguishes assert-consensus from deny-consensus);
> **(c) non-locally-visible phase content** (a phase sector discoverable only around loops).
>
> - `|Σ z|²` gives **(a)** [in the flat case] and **(c)**, and loses **(b)**. — REG as specified.
> - `(|Σ z|², arg Σ z)` gives **(b)** and **(c)**, and loses **(a)** — `arg Σ` is not
>   rephasing-invariant.
> - a canonical frame + a signed real score gives **(a)** and **(b)**, and loses **(c)**. — **CEG.**

**CEG is the corner of the trilemma a deployed trust grammar must occupy.** That is the "armor you
can derive" the safety principle asks for, arriving as a derivation rather than a design taste — and
it is derived from REG, which is the pair working as intended.

---

## 6. C4 — the verdict layer, and the attacks stated as theorems

CEG's fail-secure property is bought by the lattice: aggregation is monotone in a partial order, so
a negative can trump but never be cancelled. Does REG have any analogue? **No, and the reason is a
theorem about `|Σ|²` aggregation, not a contingency of the design.**

### 6.1 The erasure theorem (the cancellation attack, generalised)

> **Theorem (erasure-resistance ⟺ no invertible elements).** Let a readout be
> `V(M) = f(⊕_{i∈M} v_i)` for an aggregation monoid `(V, ⊕)` and a multiset `M` of contributions.
> Call the readout **erasure-resistant** if no adversary, by *adding* contributions, can drive a
> non-identity honest aggregate to the identity.
>
> **(i)** If `(V,⊕)` is a **group**, the readout is **never** erasure-resistant: for honest
> aggregate `h`, an adversary emits `h⁻¹`.
> **(ii)** If `(V,⊕)` is **idempotent** (a semilattice) with induced order `x ≤ y ⟺ x ⊕ y = y`,
> then `h ⊕ a ≥ h` for all `a`: the aggregate is monotone non-decreasing and nothing can be undone.
> Erasure-resistant.
> **(iii)** REG's value monoid is `(C, +)` — a **group**. CEG's sensitive columns are `min`, `max`,
> `median` — **order statistics on an ordered set**. ∎

**This derives CEG's aggregation table from its threat model rather than merely observing it.** §8.2
assigns `median` to the detector dimensions with the stated reason *"resists adversarial
mean-pulling by a single captured detector"* — and the theorem says why that was the only available
move: `mean` is not erasure-resistant (it is a group operation in disguise — arbitrary contributions
can drive it anywhere), and `min`/`max`/`median` are (`min`/`max` absolutely; `median` up to a
breakdown point of 50%).

**Corollary, and it is the theorem-shaped CEG-vs-REG differential the brief asks for:**
*CEG's lattice aggregation is not one defense among several. Erasure-resistance is **equivalent** to
the aggregation monoid having no invertible elements — i.e. to being naturally ordered. Any grammar
that permits cancellation between attesters has chosen a group, and every group is erasable.*

**Ownership is provably no defense here.** Ownership is a *record-layer* constraint; the readout
factors through the homomorphism `record → Σ z ∈ (C,+)`, and the subgroup reachable by any single
attester's `attest` emissions is **all of `C`** (attest has no precondition). So an adversary who
owns nothing, references nothing, and satisfies no authority path erases arbitrary honest standing.
**Ownership has zero shadow on the readout.** This is the algebraic form of the spec's own safety
principle, promoted from a design remark to a derivation.

### 6.2 The amplification theorem (not named in the spec, and worse)

The spec names cancellation. It does not name the dual, which is cheaper:

> **Theorem (quadratic sybil gain).** With per-attestation bound `|z| ≤ 1`: `N` colluding attesters
> emitting in phase produce `|Σ|² = N²`. `M` honest attesters with dispersed stance angles produce
> `E|Σ|² = M` (a random walk). Hence **`N` coordinated attesters match `N²` dispersed honest ones.**
> ∎

Compare CEG: mean aggregation gives `N` colluders out of `N+M` a weight of `N/(N+M) < 1` — bounded,
saturating, sublinear. **REG's readout is unbounded and quadratic in coordination.**

Two further consequences worth stating because they are what a referee would find:

1. **Erasure costs linearly, manufacture pays quadratically.** With `|z| ≤ 1`, erasing standing of
   magnitude `R` needs `⌈R⌉` emissions; manufacturing standing `N²` needs `N`. **Manufacture is
   quadratically cheaper than erasure**, which inverts the usual assumption that defacing is the
   cheap attack.
2. **The reward is largest exactly where it matters.** Coherent gain beats incoherent numbers only
   when honest opinion is *dispersed* — i.e. on contested subjects. **REG's readout rewards
   coordination over correctness, precisely on the subjects where the verdict is consequential.**

### 6.3 C4 verdict

**REG has no fail-secure analogue at readout, and cannot have one.** The property CEG bought with
its lattice is equivalent to the absence of invertible elements, and REG's value layer is a group by
definition. The attack surface REG exposes is larger than the spec claims: cancellation (named) plus
quadratic amplification (unnamed, cheaper) plus polarity destruction (§5.3, which makes the other two
harder to detect, since a cancelled verdict and a genuinely contested one are the same number).

**This is REG working as designed as a research instrument** — the attacks became expressible,
hence derivable, hence nameable. It is also a hard, unambiguous restatement of why REG must never be
deployed, and the spec's own prohibition is thereby earned rather than asserted.

---

## 7. The seven rows in full

### 7.1 State space
**REG:** `{z ∈ C^{S×D} : |z(x)| ≤ 1}` — complex, finite-dimensional per subject, ℓ^∞ polydisc, no
order on the values, no normalisation across kinds, no probability interpretation (`|Σ|²` is not
normalised to sum to 1 over anything).
**Flavour:** `C^n`, ℓ² sphere / projective space, inner product, Born rule.
**COMPARISON: MATCH in the field, STRUCTURED MISMATCH in the norm** (§2.1).
**FLAG: BY-CONSTRUCTION** (complex) **+ CONTINGENT** (norm) — the contingent half fires.

### 7.2 Dynamics object
**REG, value layer:** the group generated by the five verbs' actions on `A` is the **abelian
translation group** `(C,+)^{cells}`, extended by per-cell phases `U(1)^{cells}`. Abelian,
non-compact, acting **simply transitively** — hence **no invariants at all**.
**REG, record layer:** non-regular monoid, trivial unit group; groupoid only on the deletion branch
(§3).
**Flavour:** `U(n)` — compact, connected, **non-abelian**, with a rich invariant theory (moduli,
Jarlskog).
**COMPARISON: STRUCTURED MISMATCH on both layers.** The category error underneath: **flavour's group
acts on a state; REG's operations accumulate into an accumulator.** Evolution is multiplicative;
attestation is additive. These are different mathematical roles and the spec conflates them by
calling both "unitary".
**FLAG: CONTINGENT — and it refutes the spec's own claim** that the record layer is a group.

### 7.3 Gauge / redundancy sector
**REG:** global rephasing is a readout symmetry broken by the stance semantics; per-attester
rephasing is either absent (canonical frame — bundle trivialised by a global section) or fatal
(readout not a function of the record). **Residual phases after gauge fixing: zero.**
**Flavour:** `U(1)^{n−1} × U(1)^{n−1}/U(1)`; `(n−1)(n−2)/2` phases survive **every** gauge fixing —
45 at `n = 11`.
**COMPARISON: STRUCTURED MISMATCH.** Same endpoint as CEG (trivial bundle, zero residual), opposite
route: CEG has no phases to remove, REG has only removable ones.
**FLAG: CONTINGENT.** This could have come out otherwise — a spec that left the stance anchor free
would have had a non-trivial bundle. REG pinned it in its second sentence, for legibility reasons,
and paid the phase sector for it.

### 7.4 Conservation law
**REG:** `channel` is *"norm-preserving by default"* — `|w_e| = 1` on a scope edge. Exact, not a
bound. No conservation of any kind at the aggregation layer: `attest` adds amplitude with no budget.
**Flavour:** `Σ_j |U_ij|² = 1` — exact, and **across channels**.
**COMPARISON: NAME MATCH, SHAPE MISMATCH.** These are different statements. REG's says *no leak on
one wire*; unitarity says *the total across all wires is fixed*. Unitarity is intrinsically a
cross-dimension constraint and REG has no cross-dimension structure to constrain. Formally: REG's
"unitarity" is `U(1)`, the `n = 1` case, i.e. the maximal torus — **the flavour gauge group** (§0).
**FLAG: BY-CONSTRUCTION** — REG was defined as *"exact conservation default instead of
attenuation"*, so the surface pass measures only the definition. **And the pass is spurious:** the
conserved quantity is not the analogous one. This is the clearest case in the table of a
by-construction row that a careless scoring would have counted as a match.

### 7.5 Irreversibility
**REG:** claimed lossless-and-invertible; **provably not both** (§3.1). Retention branch → CEG's
irreversibility exactly (append-injective, non-invertible). Deletion branch → invertible and
history-lossy. Readout `|Σ|²` is lossy **and destroys polarity** (§5.3).
**Flavour:** dynamics fully invertible (and history-lossy in the factorisation); readout `|U_ij|²`
lossy and phase-blind.
**COMPARISON: MATCH at the readout layer; FORCED DICHOTOMY at the record layer.** Flavour occupies
the deletion corner. REG can occupy it too — by spending the Record kind, which is the one thing the
eleven+1 taxonomy says is not artifact-local.
**FLAG: CONTINGENT — the by-construction attempt fails.** REG was built to make the record
invertible; the derivation shows the price was not costed.

### 7.6 Readout
**REG:** `V(x) = |Σ_i z_i|²`, many-to-one, phase-blind, ordered.
**Flavour:** `U ↦ |U_ij|²`, many-to-one, phase-blind (`cp_phase_invisible_to_pairs`).
**COMPARISON: MATCH IN SHAPE — the closest row in the table**, and closer than CEG's corresponding
row, which matched only in the abstract ("both lossy, both route-blind"). Two contingent defects
underneath: **(i)** polarity destruction (§5.3) — flavour has no analogue because flavour's phase was
never carrying the sign of a claim; **(ii)** **one index where flavour has two.** `|U_ij|²` is a
*transition rate* between two basis elements; `|Σ z(x)|²` is a *standing level* at one cell. There is
no REG object with two kind-indices, so even the matching row matches a different kind of object.
**FLAG: BY-CONSTRUCTION** for the Born form (the spec writes it) **+ CONTINGENT** for both defects,
which fire.

### 7.7 Mixing matrix
**REG:** none. Every generator is diagonal in the kind basis — `attest`, `supersedes`, `withdraws`,
`recants` touch one cell; `channel` multiplies by a scalar along a scope edge and, on the most
generous reading of scope-as-kind-subset, gives a **coordinate projection**, not a rotation. And
independently: the state space's linear symmetry group is monomial (§2.1), so no mixing group acts.
**Flavour:** `U` itself.
**COMPARISON: INCOMPARABLE — REG has no mixing matrix.**
**FLAG: CONTINGENT, and this is the decisive row.** REG *could* have been specified with a
cross-kind channel and was not. It was constructed by inverting CEG's four forks, and none of the
four is the fork that would have produced mixing. **The instrument built to carry the maximal object
does not contain the maximal object's central object.**

**Important distinction from CEG's INCOMPARABLE on this row.** CEG **forbids** loop structure (three
MUSTs). REG merely **omits** cross-kind channels. That is a much better position: REG is not
*disqualified* as an instrument, it is *incomplete* as one, and the missing piece is nameable (§8.2).

---

## 8. Verdict, and what carries information

### 8.1 Does REG meet A2A?

**NO.** Scoring the table honestly:

| | rows | which |
|---|---|---|
| **MATCH in shape** | 1½ | readout (R6); the field half of R1 |
| **STRUCTURED MISMATCH** | 4½ | state-space norm (R1), dynamics (R2), gauge (R3), conservation (R4), irreversibility at the record layer (R5) |
| **INCOMPARABLE** | 1 | mixing matrix (R7) |

That is *worse* than CEG's table (CEG: two MATCH, three MISMATCH, one INCOMPARABLE) on the rows
that matter, and better only on the rows REG was built to win.

**The pattern is the finding.** REG passes **exactly** the rows it was built to pass (complex
values, exact conservation, Born-form readout) and **every row whose verdict could have gone either
way comes out against it**. There is no row where REG was free to fail and did not.

### 8.2 Which rows carry information

**Carry information (CONTINGENT, and they fire):**

1. **R7, the mixing matrix** — the decisive row. REG has no cross-kind transport, and its own state
   space excludes the mixing group by two independent theorems. **The eleven-kind interferometer is
   not in REG.**
2. **R3, the gauge sector** — zero residual phases, by a *new mechanism*: readout well-definedness,
   not threat model. This generalises the instrument exclusion beyond CEG to every verdict-producing
   grammar (§0, staked forward).
3. **R2/R5, the record algebra** — `{group, invertible, lossless}` is unsatisfiable; the fork REG's
   construction treats as free is not available; the complex values changed nothing about the record.
4. **R6's defects** — polarity destruction is an internal inconsistency, and the one-index/two-index
   gap says the matching row matches a different object.
5. **R1's norm** — the semantics of confidence forbids the mixing matrix, via ℓ^∞.

**Carry no information (BY-CONSTRUCTION, and said so):**

- **R4, conservation.** Defined into existence, and the pass is spurious besides (§7.4).
- **R1's complex field.** Defined into existence.
- **R6's Born form.** Written into the spec verbatim.

### 8.3 What this hands forward

**(a) REG v0.3 needs a sixth verb, and it is nameable.** The missing object is a **cross-kind
channel** — transport of amplitude from dimension `d` to dimension `d′` with a complex weight. That
verb *is* the mixing matrix's off-diagonal element, and it corresponds to a real corpus phenomenon
already measured in modulus: a change emitted as one kind and consumed as another. The panel study's
three confusion boundaries (**Premises/Facts, Structure/Manner, Model/Facts**) and BABEL's exact
reappearance of the same three on an independent instrument (`BABEL_RESULTS.md`: *"the off-diagonal
leakage is localized on the known boundary map, not diffuse"*) are the candidate non-zero
off-diagonals. **The moduli have been measured; only the phase is missing.** Adding the verb costs
the ℓ^∞ norm (§2.1's fork) and must be pre-registered as such.

**(b) The instrument exclusion generalises** (§0). Staked forward, before any REG instrument exists.

**(c) The safety principle is upgraded and one-third corrected.** Two of CEG's three flatness
requirements are threat-motivated and now have derivations (§6.1 for lattice aggregation; §4.4's
literature for acyclicity). The **third — order-independent composition — has no threat under it**;
it is forced by well-definedness of any route-independent readout. "Every CEG defense becomes
derivable as REG minus a named threat" survives with that correction, and the correction is exactly
the kind of thing the pair was built to find.

**(d) The one number that changes, named.** Per the standing hazard
(`AMP_GRAMMAR_PRIOR_ART.md` §"standing hazard": three-for-three refutations of gauge/amplitude
imports into social domains that changed no answer), REG advances past instrument-spec only by
naming a quantity that would not otherwise have been obtained. The candidate this analysis produces
is **§5.2's triangle holonomy `W_{ijk}` — three attesters pairwise reconcilable, jointly not** —
measurable on labelled change-streams, distinct from any pairwise statistic, and with the caveat
stated in the same breath: it lives on the **attester** graph, not on `K11`, so it tests
NonFactoring at `n = 3` on the wrong base space. It is not the maximal object's number. **The
maximal object's number remains unmeasured and REG as specified cannot produce it.**

---

## 9. INTERPRETATION RISKS (flagged, not resolved)

1. **REG is 70 lines old.** Every derivation is about a spec written 2026-08-21, with no conformance
   suite, no implementation, and no second reader. The CEG analysis had RC29 and LEG_B to check
   against; this one has neither. **Several findings below are corrections a second draft could
   absorb**, and should be offered as such rather than scored as kills of a fixed object. The three
   that a redraft *cannot* absorb without a substantive cost are §3.1 (the unsatisfiable triple),
   §2.1 (ℓ^∞ vs mixing), and §6.1 (group ⟹ erasable).
2. **Horn 1 vs Horn 2 (§4.2/§4.3) is the largest under-determination in this document.** It turns on
   whether a `(subject, dimension)` cell names a proposition. I read it as naming a *kind*, because
   that is what the eleven are; but a REG that attached amplitudes to `(subject, dimension, claim)`
   triples would be on Horn 1 and several verdicts would move. **It should not be resolved silently
   by either leg.**
3. **Forks F1 (id derivation) and F2 (`recanted` absorbing) are inherited from CEG and still open.**
   They decide the C1 regularity answer (§3.3) but not the group answer, which is settled by
   prior-existence alone.
4. **"Scope" is undefined in REG.** I read `channel`'s scope edge as a subset of dimensions, which is
   the reading most generous to a mixing interpretation, and it still yields only projections. If
   scope means something else entirely (authority domains unrelated to kinds), R7's verdict is
   unchanged but the argument for it is shorter.
5. **The `|Σ|²` polarity defect (§5.3) may be a drafting error rather than a design position.** If
   the intended verdict is the complex aggregate `Σ z` (with `|Σ|²` merely its strength), then §5.3
   dissolves — and the trilemma's second corner is occupied instead, so R3 and R6 move but the A2A
   verdict does not.
6. **The quadratic-sybil result (§6.2) assumes honest stance angles are dispersed.** If honest
   attesters are in phase (unanimous), the gain is the same for both sides and the attack requires
   `N ≈ M`. The claim is therefore about *contested* subjects specifically, and is stated that way.
7. **No claim of novelty is made for any mathematics here.** §4.4 is Gao–Brodzki–Mukherjee; §5.2's
   shape is Abramsky–Brandenburger; §6.1 is elementary monoid theory and its trust-domain instance is
   Theodorakopoulos–Baras territory; §2.1 is Banach–Stone/Lamperti and Poincaré/Rudin. Per the
   convergent-art rule these are HITS — free machinery — and the credits belong upstream.

---

## SOURCES

All paths absolute.

**Primary — the object under test.**
`/home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/REG_SPEC.md` (v0.1, 2026-08-21) — the state
and value definition (`|z| ≤ 1`, stance angle semantics); the five verbs and their amplitude
effects; the record-layer claim (*"group-composable, invertible — loses nothing"*); the readout
(`|Σ|²`, *"ordered, lossy, phase-blind"*); the holonomy hook; the two tests and the anti-tautology
requirement; the safety principle.
`/home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/TREL_RESULTS.md` — the **v0.2 amendment**
that is the standing spec (CEG's verb surface, amplitude depth); the measured trade (A2A
comparability vs corpus legibility trade *precisely at the interference clauses*); `recants` losing
determinacy under the cancellation clause, which is the one corpus datum bearing directly on §6.

**Benchmark — the standard this document is held to, and the CEG-side columns of every row.**
`/home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/CEG_REPRESENTATION.md` — §0 (register and the
`sm_escalator` fence, adopted verbatim); §1.3 (state = record); §2.2 (the grading theorem, reused in
§3.1); §2.3 (non-regularity); §2.4 (the two semilattices); §3.2 (**locally-visible phases are
disqualified** — the argument §4.1 reuses against REG); §3.3 (the aggregation table and the
anti-mean-pulling reason, which §6.1 derives); §4.1 (the six-row table this one is set beside);
§4.2 (ℂ admits no field order); §4.4 (the three flatness requirements, one of which §4.4 here
reclassifies); §5.3 (forks F1/F2, inherited).

**The wager under test.**
`/home/emoore/CIRISOntology/scratchpad/MAXIMAL_OBJECT.md` — the 55/45/100 counting **with its
2026-08-21 correction** (an identity for every `n`, not a passed check); *"phases are NOT locally
visible"* (the definition §4.1 turns on); the instrument exclusion and layer correction, both
adopted; the prior-art credits block.
`/home/emoore/CIRISOntology/CIRISOntology/Core/Interferometer.lean` — `ifo_edges_55`,
`ifo_cycle_rank_45`, `ifo_phase_count_agrees`, `ifo_param_count`, `ifo_edge_anatomy`; the counting
pinned, model-side, no world-claim.

**Prior art — every mathematical credit in this document.**
`/home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/AMP_GRAMMAR_PRIOR_ART.md` — §1.2
(Moreira–Wichert, *"formally quantum, operationally classical"*, the failure mode §4.2 predicts REG
falls into); §3.3 (Gao–Brodzki–Mukherjee arXiv:1610.09051, synchronisation ≅ flat bundles — the
theorem of §4.4; Bandeira–Singer–Spielman arXiv:1204.3873, the connection Laplacian); §4.1 (the
`55+45=100` correction); §4.2 (Abramsky–Brandenburger arXiv:1102.0264 and the school — the shape of
§5.2); §2.3 (Theodorakopoulos–Baras 2006, trust as a semiring path problem — where §6.1's
domain instance belongs); the standing hazard (name the number that changes — §8.3(d)).

**Corpus facts cited.**
`/home/emoore/CIRISOntology/scratchpad/plane_corpus/BABEL_RESULTS.md` — orthogonality 11/11 exact;
diagonal 7/11; **the three confusion boundaries reappearing exactly** (Premises/Facts, Model/Facts,
Structure/Manner) with *"off-diagonal leakage localized on the known boundary map"* — the measured
moduli of §8.3(a).
`/home/emoore/CIRISOntology/CIRISOntology/Core/Surface.lean` — the 4+7 decomposition and the honest
localisation of its one modelling choice; the traffic figures §8.3(a) leans on.
`/home/emoore/CIRISOntology/CLAUDE.md` — the eleven+1 taxonomy and its measured standing (κ 0.687
across 5,994 judgments; the three predicted boundaries); discipline rules 1–7, in particular rule 1
(pre-register — §0's forward prediction is staked before its instrument exists), rule 2 (separable
kills), rule 6 (a residual is never support — §8.3(d) names the number rather than reporting one),
and rule 7 (report the fired kill as plainly as the survival).

**Standard mathematics used without citation to a programme document.** Banach–Stone / Lamperti
(linear isometries of `ℓ^∞_n` are monomial matrices — §2.1); Poincaré 1907 and Rudin,
*Function Theory in Polydiscs* (`Aut(D^n) = (Aut D)^n ⋊ S_n`; ball ≇ polydisc for `n ≥ 2` — §2.1);
the triviality of the unit group of a free monoid (§3.1); the classification of `U(1)^m`-orbits by
moduli (§4.3).
