# CEG REPRESENTATION — does the grammar admit a mathematical object comparable to flavour dynamics?

**Question put:** is there a representation of CEG (finite-dimensional state space + a mixing
group action) that can be set beside flavour dynamics (`C^n`, `U(n)`, rephasing invariants,
Jarlskog) **apples-to-apples**?

**Register, stated once and binding on every line below.** This is a **STRUCTURAL COMPARISON**.
Nothing here derives physics from the ledger, from CEG, or from the eleven kinds. The
predecessor no-go (`/home/emoore/coherence-ratchet/papers/notes/sm_escalator_statistics.md`
§"Verdict up front") closed that route at theorem strength: *"a function of `C` cannot output a
property that `C` does not determine"* — the ledger is blind to the **provenance** of a
correlation matrix, of which the state-space construction is one datum. The same fence applies
here in the same words: **CEG cannot derive flavour structure and flavour cannot license a CEG
claim.** What a structural comparison can do is say precisely *which* algebraic features the two
share, which they do not, and — where they do not — what the mismatch is made of. Two of the
five answers below are no-gos of exactly the `sm_escalator` pattern, and they are reported as
no-gos, not as findings.

**Sources are `LEG_B.md` first** (the authoritative extraction of the operation semantics), with
the vendored RC29 spec consulted only where LEG_B is silent. Every such excursion is marked
**[beyond LEG_B]** inline. Full SOURCES section at the end.

---

## 0. Summary of the five verdicts

| # | Question | Verdict |
|---|---|---|
| **Q1** | State sufficiency | **FALSE** for the candidate state; **CONDITIONAL** under enlargement — and the enlargement *is* the record, which §19.7 makes a decaying object |
| **Q2** | The algebraic object | **MONOID** — non-regular, trivial unit group. Not a group, not an inverse semigroup. Composer sector quotients to a **join-semilattice**; delegation sector is a **meet-semilattice** |
| **Q3** | Polarity structure | **FALSE** — no polar/complex reading survives. The available phase group is `Z2` (a sign), not `U(1)`; linearity dies at min/max/median, and it was killed **deliberately, for a stated adversarial reason** |
| **Q4** | Apples-to-apples | Two MATCH-in-shape rows, three STRUCTURED MISMATCH, one INCOMPARABLE. **The orchestrator's staked reading is COMPLICATED and half-refuted** — see §4.3 |
| **Q5** | Decidable core | A ~120-line `Core/CEGMonoid.lean` decides 9 of 10 target theorems; the tenth is spec-interpretation and must stay a flag, not a theorem |

**The single most consequential result, stated up front because it changes what the
interferometer programme should measure:** CEG contains **three independent normative flatness
requirements** — order-independent composition (§6.1), acyclic delegation (§13.3), and
non-amplifying attenuation (§11.10) — each of which exists to *prevent* an attack. In a trust
grammar, holonomy **is** the attack (gain around a loop = delegation laundering). So a loop-phase
measurement taken on CEG-derived data will read **zero by construction, not by evidence**. That
is a manufactured floor of exactly the class the programme has been burned by before
(`aisafety-mechanism-validated-negative`, `placebo-beats-permutation-null`). It is **not** a kill
of the maximal object; it is a demonstration that CEG is the wrong instrument to test it on, and a
forward prediction that should be staked before any such measurement is attempted.

---

## Q1 — STATE SUFFICIENCY

**VERDICT: FALSE for the candidate state. CONDITIONAL for the enlargement — and the price of the
enlargement is that the state becomes the record itself, which CEG's own §19.7 specifies as a
monotonically decaying object. Sufficiency is therefore not merely expensive; it is temporary.**

### 1.1 The candidate state, written down

Let the candidate be

```
X  =  ( F , D , t )

F : (attester, subject, dimension) -> (score, confidence)     the standing field
D : the delegation graph, edges labelled (scope, valid_from, valid_until)
t : wall-clock time                                            (validity windows)
```

Each operation is admissible-and-effective **factoring through X** iff both its precondition is a
predicate on `X` and its postcondition is a function of `X`.

### 1.2 Operation by operation

**`scores` — admissibility FACTORS, effect does NOT.**

Admissibility is essentially state-free: LEG_B §3.1 step 2 establishes *"its only lawful input
state is ∅"*. The conditional-required fields (`community_id` iff `cohort_scope == community`) are
envelope-internal, not state-dependent. So admissibility factors trivially.

The **effect** does not, and the reason is a standard fact about aggregation that the spec's own
§8.2 makes load-bearing **[beyond LEG_B: §8.2's aggregation table is not in LEG_B]**:

| Polarity column | Default aggregation | Insert-summarisable? | **Delete**-summarisable? |
|---|---|---|---|
| `signed` | mean of `score × confidence` | yes, carrying `(sum, count)` | yes, carrying `(sum, count)` |
| `boolean-via-score` | **min** | yes | **NO** |
| `positive-only` | **max** | yes | **NO** |
| `-1.0 only` | **min** | yes | **NO** |
| `enumerated` | most-recent by `signed_at` | yes | **NO** |
| detector dimensions | **median** | **NO** | **NO** |

The composed standing `F` is a summary of a multiset. Inserting into a min/max is cheap
(`min(m,x)`); **deleting** from one is not — if the removed element *was* the extremum you must
re-scan the multiset. Median is not even insert-summarisable. And CEG deletes: `withdraws` and
`supersedes` remove entries from the live set (LEG_B §3.3 step 2, §3.4 step 2).

So `F` is not closed under the grammar's own operations. **The standing field is a sufficient
state for a grammar with only `scores`, and for no larger fragment.**

**`delegates_to` — FACTORS, but only into a non-autonomous system.**

Every precondition is a predicate on `D`: the delegator holds the authority (§11.10 admit-(b)),
`sub_delegation ∈ granted scope`, attenuation `child.scope ⊆ parent.scope`, depth ≤ 5 (§13.3),
acyclicity (§13.3), the `identity_type` agency gate (§8.1.12.7). The effect is an edge addition.
Both factor through `(D, t)`.

**But** LEG_B §3.2 step 4 identifies the one transition in the whole grammar that occurs by the
passage of time and no emission: window expiry. Formally this means the dynamics is
**non-autonomous** — `X` alone does not determine the next state; `(X, t)` does, and `t` advances
without any operation. A comparison with flavour must carry this: flavour's `U` is a *fixed*
operator, CEG's admissible-move set is time-varying.

**`supersedes` / `withdraws` / `recants` — the reference is where sufficiency breaks.**

This is the key test the brief names. Take it in three cases.

*Case A — the referenced attestation is still live.* Its content is in the live set. If the state
is enlarged from `F` to the **multiset of live attestations keyed by attester** (call it `L`),
this case factors. Note the enlargement is already forced: §6.1 rule 4 requires each attester's
chain be evaluated independently, so entries cannot be pooled.

*Case B — the referenced attestation is already superseded or withdrawn.* It is **not** in `L`,
and a further composer against it is nonetheless admissible **and consequential**. LEG_B §3.5 step
3 is explicit: `recants` outranks the other two *regardless of `signed_at`*, so `(withdrawn) →
(recanted)` and `(superseded) → (recanted)` are lawful transitions that take effect out of time
order. A state holding only live entries cannot even locate the target, let alone update it.
**`L` is insufficient; the state must retain non-live entries with their statuses.**

*Case C — the residue that no enlargement of the content-state recovers.* Two items:

1. **The admission rule (§3.2.3).** `withdraws` is admitted under one of four authority paths, and
   the spec requires the substrate *record which one*: *"substrate SHOULD record which admission
   rule (1-4) admitted each `withdraws` Contribution … so downstream consumers can compose policy
   (e.g., higher confidence weight for subject self-revocation rule 2 than for proxy rule 3)."*
   The admitting rule is a property of the **delegation graph as it stood at admission time**. A
   proxy chain (rule 3) that later expires cannot be re-derived from the present `D`. So the
   admitting rule is genuine trajectory information, it is **consequential** (consumers weight by
   it), and **the spec's remedy is to record it** — i.e. CEG itself concedes the state is
   insufficient and patches the gap by writing history down. This is the cleanest instance in the
   whole grammar of the state-vs-trajectory distinction, and CEG lands on trajectory.

2. **The dedup set.** Composers are idempotent on `(references_attestation_id, attestation_type,
   attesting_key_id)` and *"the substrate MUST dedup on this triple"* (§6.1). Knowing that a replay
   is a no-op requires knowing the triple was seen — again a fact about the past.

### 1.3 The enlargement, and its price — say it plainly

Enlarging the state to make the grammar Markov requires: every attestation ever admitted, with its
status, its attester, its references, and the admission rule that let it in. **That is the audit
chain. The sufficient state and the record are the same object.** The spec says so from the other
direction — §11.8.2: the withdrawn Contribution *"remains in the audit chain — federation peers
retain the historical record"*; withdrawn ≠ deleted.

So the honest formulation is not "CEG needs a big state." It is: **CEG has no state/trajectory
distinction to make.** The grammar is defined on histories; the "state" is a synonym for the
history; and any attempt to summarise it into something smaller loses an admissibility condition
(Case B), a consequential weight (Case C.1), or an idempotence guarantee (Case C.2).

**And the price is not merely size.** §19.7 **[beyond LEG_B — LEG_B does not cite §19 at all]**
specifies that the record itself is not permanent. Verbatim: *"Revocation, retirement,
capacity-eviction, scheduled expiry, and natural aging are the same operation at different rates:
a monotonic descent of an item's fidelity, driven by pressure, toward and below a recoverability
boundary called the noise floor."* Below the floor *"only its contribution to a collective
survives — the item itself is information-theoretically unrecoverable."*

Two consequences, and I am careful to keep them separate:

- **Sufficiency is temporary.** `recants` requires the issuer be the target's original attester
  (§3.2.3). Once the target has descended below the noise floor, that predicate is not merely
  expensive to evaluate — it is undecidable from what survives. The admissible-move set therefore
  *shrinks* with storage pressure. This is CEG's own version of the rent clause: the state is
  never free, always rented, and underpayment strictly loses admissible moves.
- **What survives is exactly a lossy summary.** Below the floor the individual is gone and the
  collective blur remains — which is precisely the domain of `not_computable_from`
  (`Core/Coordination.lean`): a lossy summary cannot output what it discarded. Past the floor, the
  reference-carrying operations cannot be admitted, because the thing they reference is no longer
  individually there.

**INTERPRETATION RISK (flagged, not resolved).** §19.7's descent is written over "items" with a
`content_id` and `corpus_kind ∈ {trace, blob, av_chunk, …}` — content in fountain storage. §11.8.2
says the withdrawn *Contribution* remains in the audit chain. Whether §19.7's monotone descent
applies to `federation_attestations` rows themselves, or only to the content those rows point at,
**the spec does not say in either place**, and the two sections were written at different times
(§11.8.2 is pre-RC; §19.7 is RC14). The reading above (that sufficiency is temporary) holds only
under the first interpretation. Under the second, the attestation rows are permanent and only the
bodies decay — in which case sufficiency is permanent but the *evidence* is not, which weakens the
conclusion without reversing it. **This is the single largest under-determination bearing on Q1
and it should not be resolved silently by either leg.**

### 1.4 Q1 verdict

**FALSE** — neither the composed standing nor the live-set enlargement is a sufficient state. The
break is not exotic: min/max/median aggregation is not delete-summarisable, and `recants` acts on
already-dead entries. **CONDITIONAL-TRUE** under the enlargement to the full record, at the price
that the state *is* the record — and, under the live reading of §19.7, a record that decays, so
that the set of admissible operations contracts under storage pressure. **The comparison with
flavour must therefore begin by noting that CEG has no finite-dimensional state space at all: it
has an unbounded, append-only, decaying history.**

---

## Q2 — THE ALGEBRAIC OBJECT

**VERDICT: MONOID — specifically a graded, non-regular monoid of partial maps whose group of units
is trivial. NOT a group. NOT an inverse semigroup. The composer sector quotients onto a
join-semilattice; the delegation sector carries a dual meet-semilattice; the two prospective
primitives generate the free, non-idempotent part.**

### 2.1 The object, set up

Elements are the partial maps on record-states induced by single emissions
`a = (type, attester, target, envelope)`:

```
a(R)  =  R                       if a is a composer and its dedup triple is already in R   (§6.1)
      =  undefined               if a's preconditions fail in R
      =  R ++ [a]  with status updates on the referenced entry, otherwise
```

Composition is sequential emission. **Associativity is trivial** (composition of partial
functions). **The identity is the empty emission sequence.** So we have a monoid `M` of partial
transformations; equivalently, the small category whose objects are record-states and whose
morphisms are admissible emission sequences. Both readings are correct; the category is the
natural home for the reference dependency (§2.5) and the monoid for the invertibility question.

### 2.2 The grading, and the death of every inverse

Define `|R|` = number of admitted rows. Then for every generator, `|a(R)| ∈ {|R|, |R|+1}`, and
never less. **`M` acts by non-decreasing maps on `|·|`.** Immediately:

**Theorem (trivial unit group).** The only invertible element of `M` is the identity.
*Proof.* If `a·b = 1` then `|R| = |b(a(R))| ≥ |a(R)| ≥ |R|`, so both inequalities are equalities
and `a` and `b` act as the identity wherever defined. ∎

This is the machine-checkable content of §1.4's *"unilateral, monotonic graph claims"* and of
§10.1.6's forward-only rule (*"a later non-withdrawn write does NOT resurrect"*). **Witness
operation: `withdraws`.** Nothing in the grammar returns a withdrawn entry to live, and LEG_B §3.4
step 4 establishes this as absorbing, not merely unimplemented.

### 2.3 Is `withdraws` a partial inverse of `scores` or `delegates_to`? — NO, and the failure is
### instructive

An inverse semigroup requires, for each `a`, an `a*` with `a a* a = a` and `a* a a* = a*`.

**`withdraws` is not a partial inverse of `scores`.** Compute `s · w · s`: the record now holds a
withdrawn `scores` row, a `withdraws` row, and a fresh live `scores` row — three rows where `s`
alone left one. `|s w s (R)| = |R| + 3 ≠ |R| + 1 = |s(R)|`. The equation `s w s = s` fails on the
grading alone. **No choice of `w` fixes this**, because `s` strictly increases `|·|` and the
grading forbids any `x` with `|s x s (R)| = |s(R)|`. So:

**Theorem (not an inverse semigroup).** `scores` is not a regular element of `M`; hence `M` is not
regular; hence `M` is not an inverse semigroup. **Witness operation: `scores`.**

The intuition worth carrying: `withdraws` is not an *undo*, it is a *further claim*. §11.8.2 makes
this normative — the withdrawn contribution stays. The grammar has no undo, only more record.

**`recants` is not a partial inverse either, and it is further from one than `withdraws` is.**
`recants` moves a second axis (truth-at-issuance) and carries a reflexive cost onto the operator's
own standing (§3.2.2). An inverse restores; `recants` adds two irreversible facts. LEG_B §4's
"genuine surprise" — the only operation whose cost falls on the operator — is the algebraic
statement that `recants` is maximally *not* an inverse.

### 2.4 What IS there: two semilattices, opposite orientations

**The composer sector is idempotent.** §6.1's dedup triple covers exactly
`supersedes`/`withdraws`/`recants` (all three carry `references_attestation_id`); replaying one is
a no-op, so `c · c = c`. **The prospective pair is not covered** — `scores` and `delegates_to`
carry no `references_attestation_id`, so the dedup triple does not apply and `s · s ≠ s`. This is
LEG_B's 1+1+3 typing backbone appearing as an algebraic fact: **the retrospective three are
idempotent, the prospective two are free.**

**The composer idempotents commute on the verdict.** §6.1 rule 1 resolves races by a *priority*,
not a timestamp: *"`recants` wins regardless of `signed_at`."* So the resolved status is the
**maximum** over emitted composer types on the chain

```
live  <  superseded  <  withdrawn  <  recanted        (§6.1 rule 1, a total order)
```

and max is idempotent, commutative, associative. **The status axis is a 4-chain and the composer
sector acts on it as a join-semilattice, i.e. a commutative idempotent monoid.** `recanted` is the
top and is absorbing — the terminal state LEG_B §3.5 step 4 derives.

**The delegation sector is a meet-semilattice, dual.** Attenuation (§11.10) gives
`child.scope ⊆ parent.scope` with constraints addable but never removable, so composing grants
along a chain **intersects** scopes. Authority meets downward; status joins upward. Both are
monotone; neither is invertible. The two orientations are the algebraic form of LEG_B §4's
"raise/lower" table.

### 2.5 Which compositions are forbidden, and which commute

**Forbidden by precondition** (LEG_B §6, all normative):
cycle-closing `delegates_to` (MUST reject); `agency:*` scope onto an `infra`-only key (MUST
reject); sub-delegation without `sub_delegation` in the granted scope; any scope expansion;
`recants` by anyone but the original attester; `withdraws` by an issuer satisfying none of the four
rules; any composer whose `references_attestation_id` does not resolve; scoped `scores` missing
`community_id`/`family_id`. **Not forbidden, though often assumed to be:** a composer against an
already-composed target (that is how `recants`-after-`withdraws` works), and cross-attester
`supersedes` — LEG_B §7 flags the "same attester" clause as descriptive, handled by parallel-chain
evaluation (§6.1 rule 4) rather than rejection.

**Commuting pairs:** two `scores` anywhere (the §8.2 aggregations are symmetric functions of the
multiset, and even `enumerated`'s most-recent rule reads `signed_at` **from the data**, not from
emission order); a `scores` and any composer aimed elsewhere; two composers on the same target
(join, §2.4).

**The one genuine non-commutation is causal, not algebraic.** `w · s` is defined and `s · w` is
not, because `w` needs its target to exist. That is a happens-before dependency — the category
reading's arrow — and it is the whole of the non-commutativity. **CEG deliberately puts every
other ordering fact into the data** (`signed_at`, canonical tie-breaks) rather than into the
emission order. That design has a name: it is what makes the composition **confluent**, and
confluence is the engineering requirement behind §6.1's opening line (*"consumers MUST compute a
deterministic verdict"*) and §5.6.8.13's partition tolerance (*"Resolution MUST NOT require chain
completeness"*).

### 2.6 The irreversible core

Every non-identity element. More usefully, three distinguishable irreversibilities, which the rest
of this document keeps apart because conflating them is the error the staked expectation makes:

1. **Append-monotonicity** — `R ↦ R ++ [a]` is **injective**. The record dynamics loses *nothing*.
   Its non-invertibility is that the inverse is not an *admissible move*, not that information is
   destroyed. This is a deontic irreversibility: a claim once made cannot be unmade, only claimed
   about further.
2. **Absorbing states** — `withdrawn` (forward-only, §10.1.6) and `recanted` (terminal, §6.1 rule
   1). These are genuine sinks on the status chain.
3. **Readout contraction** — the composition `record ↦ verdict` is many-to-one and *is*
   information-destroying. It is not a dynamical map at all; it is a measurement.

### 2.7 A pure-gauge operation, found in the spec

§5.6.8.13, via LEG_B §3.3 step 8: for `organization` / `org_membership` / `partner_record`,
resolution is stable-id grouping and `supersedes` references are *"audit lineage only —
decoration, never resolution."* Algebraically: **on those three subject_kinds, `supersedes` acts
as the identity on the verdict while acting non-trivially on the record.** That is the definition
of a pure-gauge operation — it changes the representation and not the physical content. It also
means there is not one monoid but a family indexed by `subject_kind`, whose members differ in
which generators act trivially. Worth carrying into any Lean model as a parameter, not a constant.

### 2.8 Q2 verdict

**MONOID.** Non-regular (witness `scores`), trivial unit group (witness `withdraws`), graded by
record length. Not a group; not an inverse semigroup. Sub-structure: an idempotent commutative
**join-semilattice** on the 4-chain `live < superseded < withdrawn < recanted` (the three
retrospective composers), a dual **meet-semilattice** on delegation scopes (attenuation), and a
free non-idempotent part (the two prospective primitives). The category-on-histories reading is
equally valid and is where the reference dependency lives.

**INTERPRETATION RISK — the fork that would change this verdict.** If `attestation_id` is
content-derived (a hash of canonical bytes), then two byte-identical `scores` emissions collide and
`scores` becomes idempotent too — at which point the *entire* monoid is idempotent and commutative,
i.e. a pure join-semilattice, i.e. a textbook state-based CRDT. If `attestation_id` is
substrate-assigned in arrival order, `scores` is not idempotent and the verdict above stands. **The
spec supports both readings in different places**: §8's tie-break uses `canonical_bytes_hash`
(content-derived) while §6.1 rule 3 uses *"the substrate-assigned key (Persist's
`federation_attestations.attestation_id`)"* — and LEG_B §3.3 step 2 already flagged that these two
tie-breaks **differ**. Under the arrival-order reading, §6.1 rule 3's tie-break is itself
**order-dependent**, which punctures confluence on exact-`signed_at` ties. This is a real (if
measure-zero) crack in the flatness claimed in §3.4 below, and it is a spec inconsistency with
algebraic consequences, not a drafting nit.

---

## Q3 — THE POLARITY STRUCTURE

**VERDICT: FALSE. `(score, confidence)` does not support a polar/complex reading. The phase group
available is `Z2` — a sign — not `U(1)`. Linearity survives on exactly one of six default
aggregations and dies on the other five, and on the most sensitive of them it was killed
deliberately, for a stated adversarial reason.**

### 3.1 The pair, and what composition does to it

`score ∈ [-1,+1]`, `confidence ∈ [0,1]`, per dimension (§4). §4's own gloss insists the two carry
different information: *"Low confidence + high magnitude = 'I believe this strongly but I might be
wrong'; high confidence + low magnitude = 'I am sure the truth is near-neutral.'"*

But the default aggregation for the `signed` polarity column (§8.2) is the **mean of
`score × confidence`**. The map

```
pi : [-1,1] x [0,1] -> [-1,1],     (s, c)  |->  s * c
```

is a projection with infinite fibres: `(1.0, 0.5)` and `(0.5, 1.0)` are the two cases §4 goes out
of its way to distinguish, and `pi` sends both to `0.5`. **The envelope carries a distinction that
the default composition erases.** This is not a criticism — consumer policy may override §8.2 —
but it is decisive for the representation question: whatever the pair *means*, what the algebra
*sees* is one real number. There is no 2-dimensional state to complexify.

### 3.2 Is there a phase? — No: the group is `Z2`

A polar reading needs `z = r e^{i θ}` with `θ` ranging over a circle. CEG offers:

- `sign(score) ∈ {+1, −1}` — a two-element group, `Z2 = O(1)`, not `U(1)`.
- §2's Polarity axis: `Positive / Negative / Neutral / Indeterminate{reason}`. Three values plus a
  bottom, not a circle. `Indeterminate{reason}` is not a point on the sign line at all — it is a
  `⊥` carrying its own reason field.

**There is no continuous phase anywhere in the envelope.** Not in `score`, not in `confidence`, not
in the Polarity axis, not in any of the ~21 optional fields (§4). Every rotation the algebra admits
is a sign flip. `Z2` has no non-trivial irreducible complex representation beyond the sign
character; the "phase sector" is one bit, and it is already visible in the sign of the score —
i.e. **locally visible**, which is exactly what the interferometer's phases are defined not to be.

**A convergence worth recording, and not over-reading.** `Indeterminate{reason}` refuses to collapse
"I have no view", "not applicable", and "the evidence is balanced" into one symbol — it carries the
reason. That is the same refusal as the programme's own polarity AMENDMENT A1 (*"AMBIGUOUS
conflates ZERO, N/A and TIE"*), reached independently. Per the house rule on convergent art this is
a **HIT, not a strike**: CEG got there first on this point and the design should be credited, not
claimed. It cashes as nothing for the representation question.

### 3.3 Where linearity dies, exactly

| Aggregation (§8.2) | Algebraic type | Linear? |
|---|---|---|
| mean of `score × confidence` (`signed`) | convex combination of the products | **linear in the products**; *bilinear*, not linear, in `(s,c)` |
| **min** (`boolean-via-score`, `-1.0 only`) | lattice meet | **no** — piecewise-linear, not additive |
| **max** (`positive-only`) | lattice join | **no** |
| **most-recent** (`enumerated`) | argmax selector over `signed_at` | **no** — not a function of the values at all |
| **median** (detector dimensions) | order statistic | **no** |
| Policy D tie-break (§8.1.4) | inverse weighting by `affected_population_estimate` | **no** — and non-monotone in the usual weight |
| Policy A (§8.1.1) | mean over a **pinned trust set** | linear *after* a 0/1 gate that depends on the delegation graph — the gate is the nonlinearity |

So: **one of six default columns is linear, and only on a projected 1-D coordinate.** Everything
else is lattice-theoretic or selective.

**And the killing of linearity is deliberate and documented.** §8.2 assigns **median** to the
detector dimensions with the reason given in the table itself: *"resists adversarial mean-pulling
by a single captured detector."* Linear aggregation is manipulable by an outlier; the median is
not. **CEG rejected linearity on its most sensitive dimensions as an explicit security property.**
That is the strongest possible answer to "does anything support a vector-space reading": the
spec's own threat model forbids it precisely where it would matter, and a representation that
restored linearity would restore the attack.

### 3.4 The one linear structure in the spec — and it is a contraction semigroup, not a group

Policy C (§8.1.3) is *"weighted graph (EigenTrust-style) … transitive-trust propagation across the
full attestation graph, weighted by canonical-bootstrap distance **with confidence decay per
hop**."* EigenTrust is a principal-eigenvector computation: iterate `t ← C^T t` for a row-stochastic
`C`. This **is** genuine linear algebra — the only genuine linear algebra in CEG.

Its structure is exactly the wrong shape for the comparison, and informatively so:

- Non-negative entries, stochastic normalisation → **Perron–Frobenius**, one dominant eigenvector,
  real non-negative spectrum bounded by 1.
- "Confidence decay per hop" makes it **sub**-stochastic → strictly contractive → the iteration
  **forgets its initial condition**.
- Contractions form a **semigroup**, not a group. `U(n)` is a group, isometric, and forgets
  nothing.

§13.3's aggregate-weight cap (*"cap the trust weight any single terminal delegate can accumulate
from a given root at 0.5 × root_trust"*) is a further explicit contraction constraint, and its
stated purpose is anti-laundering. So the one place CEG has linear dynamics, it constrains that
dynamics to be **strictly gain-losing around any path** — which is the flatness requirement of
§0 restated in linear-algebraic clothes.

### 3.5 Q3 verdict

**FALSE.** No polar or complex reading survives. The pair `(score, confidence)` is projected to one
real coordinate by the only linear aggregation; the phase group is `Z2` and its one bit is locally
visible; five of six default aggregations are lattice or selection operations with no additive
structure; and the nonlinearity on the sensitive dimensions is a deliberate, documented
anti-manipulation choice. The single linear object in the spec is a **contractive Perron–Frobenius
semigroup**, whose defining property (forgetting) is the opposite of unitarity's (preserving).

---

## Q4 — THE APPLES-TO-APPLES TABLE

**VERDICT: two MATCH-in-shape rows (gauge sector, readout), three STRUCTURED MISMATCH (state
space — with a proof of obstruction; dynamics object — at the wrong layer; conservation vs
contraction), one INCOMPARABLE (no CEG mixing matrix exists). The staked expectation is
half-refuted and half-relocated: unitarity is Record-*preserving*, not Record-free, and CEG's
Record content is carried by RETENTION, not by non-invertibility.**

### 4.1 The table

| Row | CEG-as-derived | Flavour dynamics | Verdict |
|---|---|---|---|
| **State space** | the record `R`: an unbounded, append-only, decaying multiset of signed attestations with statuses, **plus wall-clock `t`**. No linear structure, no inner product, no dimension. The *verdict* space is per `(dimension, subject)` a point in a **real ordered interval** with a lattice | `C^n` (n=3): finite-dimensional complex Hilbert space, inner product, no order | **STRUCTURED MISMATCH — with a proof of obstruction.** See §4.2 |
| **Dynamics object** | monoid of partial maps: non-regular, trivial unit group, graded. Composer sector → join-semilattice; delegation → meet-semilattice | `U(n)` group action: compact connected Lie group, 9 real params at n=3, 4 physical after rephasing | **STRUCTURED MISMATCH.** Monoid vs group — but at the *wrong layer*; see §4.3 |
| **Gauge / redundancy sector** | canonicalisation: JCS member order, lexicographic sorting of set-semantics arrays, hex case, timestamp precision (§0.9–§0.9.2.1). Invariant = the canonical-bytes hash. **Residual freedom**: omit-vs-materialise leaves `(Z2)^k` per attestation with *"no observable difference"* (§0.9.2) | rephasing `U → D_L U D_R`: torus `U(1)^{n−1} × U(1)^{n−1}/U(1)`. Invariants = moduli `|U_ij|` and Jarlskog `J` | **MATCH IN SHAPE, MISMATCH IN CONSEQUENCE.** Both have a redundancy group and a named invariant. But CEG's quotient admits a **global section** ("omit all defaults") — its bundle is trivial and **zero residual phases remain**. Flavour's does not: `(n−1)(n−2)/2` phases survive every gauge fixing. **This is the decisive row** |
| **Conservation law** | attenuation: `child.scope ⊆ parent.scope`, total authority never increases (LEG_B §4). A **one-sided bound**, equality not required. Plus one true invariant: ≥1 live `moderate`-holder or the community MUST NOT federate (§11.11) | unitarity: `Σ_j \|U_ij\|² = 1` **exactly** — probability conserved | **STRUCTURED MISMATCH.** Contraction vs exact conservation. CEG's analogue is sub-stochastic; flavour's is stochastic-and-invertible |
| **Irreversibility** | three distinct kinds (§2.6): append-monotonicity (**injective — loses nothing**), absorbing states (`withdrawn`, `recanted`), readout contraction (**lossy**) | **none.** `U(n)` is a group; every evolution invertible. CP violation is a *phase asymmetry*, not an irreversibility — it is fully unitary | **STRUCTURED MISMATCH, and the staked reading needs correction.** See §4.3 |
| **Readout / measurement** | `record ↦ verdict` under §8.2: many-to-one, **deliberately order-blind** (confluence) | `U ↦ \|U_ij\|²`: many-to-one, **phase-blind** (`cp_phase_invisible_to_pairs`) | **MATCH IN SHAPE.** In both, the dynamics preserves and the *readout* is what loses — and in both, what it loses is route/phase content |
| **"Mixing matrix"** | none exists. There is no operator taking one kind of claim to another; the 55-channel object is a wager over the **eleven kinds**, not over CEG | `U` itself | **INCOMPARABLE.** Nothing in CEG plays this role, and constructing one would be an imported assumption, not a derivation |

### 4.2 Why the state-space row is a proof, not an opinion

CEG's composition is **monotone and lattice-based**: min, max, median, the status chain
`live < superseded < withdrawn < recanted`, the fail-secure "any negative trumps positive". The
monotonicity is load-bearing — it is what gives deterministic convergence, partition tolerance and
fail-secure behaviour.

An ordered field requires every square to be non-negative. In `C`, `i² = −1` and `1² = 1`, so
`−1 ≥ 0` and `1 ≥ 0` — contradiction. **`C` admits no field order.**

Therefore: **the order that makes CEG converge and the complex structure that would make it
interfere cannot coexist on the same layer.** This is a no-go of exactly the `sm_escalator`
pattern — a property the object does not determine cannot be output by a function of the object —
and it is reported as such. It does not say a complex structure is impossible *somewhere* in the
neighbourhood; it says it is impossible on the value algebra CEG actually composes over, so long
as that algebra stays ordered. Any future construction must therefore either give up the order (and
with it convergence, fail-secure aggregation, and the CRDT property) or give up the complex
structure. **It cannot have both, and the burden is on any proposal to say which it drops.**

### 4.3 The staked expectation, confronted

The orchestrator staked, and disclosed: *CEG's non-invertibility is exactly its Record content, and
flavour's unitarity is Record-free.*

**Verdict: COMPLICATED, with the second half REFUTED as stated.** Three findings, in order of
severity.

**(a) The second half is backwards.** Unitary evolution is **maximally Record-preserving**: it is
bijective, so the past is exactly recoverable from the present. What is Record-free is the **rate
readout** `|U_ij|²`, not the unitarity. The programme's own machinery already says this —
`cp_phase_invisible_to_pairs` is a statement about the *readout*, not about `U`. So the correct
pairing is one layer down from the staked one:

```
CEG record    <->  flavour amplitude    both retain route information; both dynamically invertible-in-principle
CEG verdict   <->  flavour rates        both lossy; both order/phase-blind
```

Under that pairing the "semigroup vs group" mismatch **compares the wrong layers** — CEG's *record*
dynamics against flavour's *state* dynamics. That is the sharpest correction this analysis
produces.

**(b) The first half conflates two irreversibilities that point in opposite directions.** CEG's
record dynamics is **injective** — appending loses nothing. Its non-invertibility is that the
inverse is not an admissible move, which is a *deontic* fact (you may not un-say), not an
*information-theoretic* one. The genuinely lossy map is the readout, which is not a dynamical map.
So "non-invertibility **is** the Record content" is false as an identity: **the Record content is
carried by retention** — §11.8.2's *"remains in the audit chain"* — **not by non-invertibility.**
Non-invertibility and retention are in fact opposed here: it is precisely *because* nothing is ever
removed that the record dynamics cannot be inverted by an admissible move, and precisely *because*
nothing is ever removed that the past stays provable.

**(c) There is nonetheless a real Record-shaped residue, and it is small, discrete, and
SHOULD-strength.** The staked reading is not empty. Two genuine route-dependences survive every
flatness requirement:

1. **The admission rule (§3.2.3).** Four authority paths reach the identical end-state
   (`withdrawn`), and consumers weight them differently (*"higher confidence weight for subject
   self-revocation rule 2 than for proxy rule 3"*). Same endpoints, different route,
   consequential difference. **That is a holonomy** — and its group is discrete (4 values), not
   `U(1)`. Its structure is exactly the founding NonFactoring shape: *two histories agreeing under
   the verdict readout, differing in the quantity.* But it is a **SHOULD**, not a MUST, so a
   conforming substrate may discard it — in which case the holonomy is genuinely lost and the
   route becomes unrecoverable.
2. **The §11.11 authority loop.** A `withdraws` against a `moderate` delegation deterministically
   induces a fresh grant to the highest-track-record member. Traverse the loop and the system
   returns to "has a moderator" **with a different holder** — a non-identity holonomy valued in a
   permutation group on members. Discrete again. LEG_B §5 already identified this as *"the only
   closed loop in the grammar"*; the algebraic reading is that it is the only loop with
   non-trivial holonomy.

### 4.4 The three flatness requirements — why a CEG-based null would be manufactured

CEG's normative core forbids holonomy in three independent places, each for a stated security
reason:

| Requirement | Source | What it forbids | Why |
|---|---|---|---|
| **Order-independent composition** | §6.1 (*"consumers MUST compute a deterministic verdict"*); §5.6.8.13 (*"Resolution MUST NOT require chain completeness"*) | route-dependence of the verdict | convergence + partition tolerance |
| **Acyclic delegation** | §13.3 (*"Substrate MUST detect cycles … and reject the cycle-closing emission"*) | **loops in the authority graph at all** | delegation laundering |
| **Non-amplifying attenuation** | §11.10 (`child.scope ⊆ parent.scope`); §13.3 (cap at `0.5 × root_trust`) | **gain ≥ 1 around any path** | trust amplification |

On an acyclic graph every connection is flat vacuously; with gain < 1 on every path there is
nothing to accumulate; with an order-independent join there is no route to remember. **In a trust
grammar, holonomy is the attack.** A system that had loop phases would be one in which routing a
claim around a cycle changed its weight — which is the definition of laundering, and which §13.3
rejects at MUST strength.

The methodological consequence is the one stated in §0 and it is the most actionable output of
this analysis: **any loop-phase measurement performed on CEG-derived data will read zero because
the spec requires it to, not because the world does.** That is a large manufactured floor in the
target class. Under the maximal object's own stated kill (*"the frame itself dies if loop
residuals are consistently zero"*), such a reading would appear to fire the kill while carrying no
evidential content whatever. **The kill must not be scored on this instrument.** The finding
should be staked forward, before any such measurement is designed.

This does not touch the maximal object. ALIGNMENT_RESULTS already established that CEG does not
span the eleven — it *"is not an eleven-spanning machine; it is a rules/record/facts machine"* —
so CEG was never the interferometer's instrument. What is new here is the *reason* it cannot be
one, and that the reason predicts the null in advance.

### 4.5 Q4 verdict

Two MATCH-in-shape rows (gauge sector; readout), three STRUCTURED MISMATCH (state space, with a
proof of obstruction; dynamics object, at the wrong layer; conservation vs contraction), one
INCOMPARABLE (there is no CEG mixing matrix, and manufacturing one would be an import). The staked
expectation is **half-refuted** (unitarity is Record-*preserving*, not Record-free) and **half-
relocated** (the Record content is retention, not non-invertibility) — with a small, discrete,
SHOULD-strength holonomy residue that survives and is worth its own line in the map.

---

## Q5 — THE DECIDABLE CORE

**VERDICT: a single ~120-line brick, `CIRISOntology/Core/CEGMonoid.lean`, decides 9 of 10 target
theorems on a finite toy by `decide`/`omega`. The tenth is spec-interpretation and must remain a
flag.**

**Specified, not built.** Nothing below has been written; this is the design.

### 5.1 The toy model

```
inductive Op    | scores | delegates | supersedes | withdraws | recants
inductive Status| live | superseded | withdrawn | recanted        -- a 4-chain
structure Entry where author : Fin 3; target : Option (Fin 8); status : Status; rule : Fin 4
abbrev Rec := List Entry                                          -- append-only
def rank : Status -> Nat                                          -- 0,1,2,3
def join (a b : Status) : Status                                  -- max by rank  (§6.1 rule 1)
def step (o : Op) (a : Fin 3) (tgt : Option (Fin 8)) : Rec -> Option Rec   -- partial, with dedup
def verdict : Rec -> Fin 8 -> Status                              -- the readout
```

Three attesters, eight slots, four statuses — small enough for `decide` over the whole reachable
set, large enough to carry every distinction the derivations use.

### 5.2 What is DECIDABLE — the ten theorems

| # | Theorem | Pins | Method |
|---|---|---|---|
| 1 | `join_comm`, `join_assoc`, `join_idem` | composer sector is a join-semilattice (§2.4) | `decide` on 4×4 |
| 2 | `recanted_absorbing : join s recanted = recanted` | `recants` is terminal (LEG_B §3.5) | `decide` |
| 3 | `status_monotone : rank (verdict (step o R) x) >= rank (verdict R x)` | nothing returns to live (§10.1.6) | `decide` on the reachable set |
| 4 | `length_monotone : (step o R).length >= R.length` | the grading (§2.2) | `simp`/`omega` |
| 5 | `unit_group_trivial : w != [] -> apply w R != R` for a witness `R` | no admissible undo (§2.2) | `omega` on lengths |
| 6 | `scores_not_idempotent : apply [scores,scores] R != apply [scores] R` | the prospective pair is free (§2.4) | `decide` |
| 7 | `composer_idempotent : apply [c,c] R = apply [c] R`, `c` retrospective | §6.1 dedup triple | `decide` |
| 8 | `not_regular : forall b, apply ([scores] ++ b ++ [scores]) R != apply [scores] R` | **not an inverse semigroup** (§2.3) | `omega` on the grading |
| 9 | `verdict_order_independent : verdict (apply [c1,c2] R) = verdict (apply [c2,c1] R)` | **the flatness theorem** — no holonomy in the composer sector (§4.4) | `decide` over composer pairs |
| 10 | `ceg_nonfactoring` | the holonomy residue (§4.3c) | `decide` on two exhibited records |

**Theorem 10 is the one worth building the brick for.** Exhibit `R1`, `R2` reached by different
admission rules (`rule = 1` vs `rule = 3`) with `verdict R1 x = verdict R2 x` but
`R1.rule != R2.rule`. That is *two wholes agreeing under the readout, differing in the quantity* —
the exact signature of `Core/NonFactoring.lean`. If it types against the existing `NonFactoring`
structure it becomes a **fourth witness** alongside `nonfactoring_parity`, `nonfactoring_cp_phase`
and `nonfactoring_record`, which is the highest-value outcome available here and is decidable.

Theorems 9 and 10 together are the honest statement of the whole analysis: **the verdict is flat,
and the route memory that flatness discards is exactly what the record is for.**

### 5.3 What is INHERENTLY SPEC-INTERPRETATION — must stay flags, never theorems

Five items. A Lean brick that *decided* any of these would be encoding a reading as a proof, which
is the failure mode the house rules name (`unconditional-statement-failure`: substance survives,
warrant fails, and the number is right so no numerical gate catches it).

1. **Is `attestation_id` content-derived or arrival-assigned?** Decides whether `scores` is
   idempotent, hence whether the whole object is a monoid or a pure CRDT semilattice (§2.8). §8 and
   §6.1 rule 3 point opposite ways. **Model it as a parameter; prove both branches.**
2. **Does §19.7's monotone descent apply to attestation rows or only to stored content?** Decides
   whether Q1's sufficiency is temporary or permanent (§1.3).
3. **Is the §3.2.3 admission-rule metadata part of the state?** It is a **SHOULD**. If discarded,
   theorem 10's holonomy vanishes. **The brick must carry the recording as a hypothesis, not bake
   it in.**
4. **Is cross-attester `supersedes` admissible?** LEG_B §7 flags it descriptive-not-enforced.
   Changes which compositions are in `dom(step)`.
5. **Which `subject_kind`?** §5.6.8.13 makes `supersedes` pure-gauge on three of them (§2.7). There
   is a *family* of monoids, not one. **Index the model by `subject_kind`.**

### 5.4 What the brick would NOT do

It would not model the composition policies (Q3 is a statement about real-valued aggregation, not
about the transition structure); it would not model time (the non-autonomy of §1.2 needs a clock
and buys nothing decidable); and it would carry **no world-claim** — like `Core/Interferometer.lean`,
it is bookkeeping for a wager, decidable and model-side only.

---

## Standing, and what this does NOT establish

- **No stance change is proposed.** Nothing here is `measured`; nothing is `proved` until the Q5
  brick exists and compiles. The Q4 §4.2 obstruction is a genuine theorem about ordered fields but
  it is a theorem about *the comparison*, not about CEG or about physics.
- **No derivation claim is made in either direction**, per the `sm_escalator` fence.
- **The maximal object is untouched.** §4.4 is a statement about instrument choice, not about the
  wager's truth. The forward prediction it licenses (a CEG-derived loop measurement reads zero by
  construction) should be **staked before** any such measurement is designed, or it is a residual
  and residuals are never support (discipline rule 6).
- **The one thing here that could become a proved claim** is Q5 theorem 10: a fourth
  `NonFactoring` witness, decidable, model-side. It is the recommended next brick.

---

## SOURCES

All paths absolute.

**Primary (per the brief): the extracted operation semantics.**
`/home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/LEG_B.md` — §1 the 1+4 set and the 1+1+3
typing backbone; §2.1–2.5 the sourced pre/postconditions of all five operations; §2.6 structural
vs emergent relations; §3.0 the reconstructed state vocabulary and its honest flag; §3.1–3.5 the
per-operation transition derivations; §3.6 the composed picture and the three carried facts; §4
the raise/lower/preserve orientation table; §5 duality and pairing (the one true inverse pair, the
`withdraws`/`recants` sibling split, `scores`'s internal polarity, no involutions); §6 the fifteen
normative prohibitions; §7 the honest gaps.

**Consulted where LEG_B is silent — CEG 1.0-RC29**,
`/home/emoore/CEWP/analysis/tier4-registry-trust/CEG-1.0-RC29-spec/`:

| File | Used for | Marked in text |
|---|---|---|
| `00_conformance.md` §0.9–§0.9.2.1 | JCS canonicalisation; the omit-vs-materialise rule and its *"no observable difference"* clause; set- vs sequence-semantics array sorting | Q4 gauge row |
| `02_grammar.md` | the eight axes; Polarity values incl. `Indeterminate{reason}` | Q3.2 |
| `03_primitives.md` §3.1, §3.2, §3.2.2, §3.2.3 | the wire shapes; the four-rule `withdraws` admission and the per-rule audit-metadata SHOULD | Q1.2 case C, Q4.3c |
| `04_envelope.md` §4 | the field table; the `score`/`confidence` gloss that the default aggregation erases | Q3.1 |
| `06_relations.md` §6.1 | precedence, the dedup triple, the substrate-assigned tie-break | Q2 throughout |
| `08_composition.md` §8.1.1–§8.1.4, **§8.2** | Policy A's pinned-trust gate; Policy C EigenTrust + per-hop decay; Policy D inverse weighting; **the aggregation table (mean / min / max / most-recent / median) and the stated anti-mean-pulling reason** | **Q1.2, Q3.3, Q3.4 — the single most load-bearing excursion beyond LEG_B** |
| `11_governance.md` §11.10, §11.11 | attenuation and revocable-at-any-link; the merit auto-promotion loop | Q2.4, Q4.3c |
| `13_anti_patterns.md` §13.3 | delegation laundering: depth cap, **MUST-reject cycles**, `0.5 × root_trust` weight cap | Q4.4 |
| `19_holonomic.md` §19.7–§19.7.3 | the noise floor; *"monotonic descent of an item's fidelity, driven by pressure"*; below-floor collective-only survival; `EjectionVerdict` | **Q1.3 — LEG_B does not cite §19 at all** |
| `01_foundation.md` §1.4 | the inductive-adequacy framing; *"unilateral, monotonic graph claims"*; the named falsification target | Q2.2 |

**FALSE FRIEND, flagged.** `19_holonomic.md`'s "holonomic" is **not** the interferometer's
holonomy. It names a *holographic* storage property — graceful degradation, any fragment
reconstitutes — with no connection, no parallel transport, and no loop integral anywhere in the
section. The section is nonetheless load-bearing for Q1 for an unrelated reason (the noise floor).
Do not cite §19 as evidence for or against loop phases.

**Programme context.**
`/home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/ALIGNMENT_RESULTS.md` — the tournament
conjecture is dead by its own staked kills; CEG concentrates on {Rules, Record, Facts}.
`/home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/TRANSITION_MAP_PREREG.md` — frozen
2026-08-21; Stage 1 design and NOTE A1's register distinction.
`/home/emoore/CIRISOntology/scratchpad/MAXIMAL_OBJECT.md` — the 55/45/100 counting, the four-part
kill, and *"the frame itself dies if loop residuals are consistently zero"* — the clause §4.4
warns must not be scored on a CEG instrument.
`/home/emoore/CIRISOntology/CIRISOntology/Core/Interferometer.lean` — the counting pinned;
`ifo_edges_55`, `ifo_cycle_rank_45`, `ifo_phase_count_agrees`, `ifo_param_count`.
`/home/emoore/coherence-ratchet/papers/notes/sm_escalator_statistics.md` §"Verdict up front" — the
no-go pattern and the fence this document operates under.
`/home/emoore/CIRISOntology/CLAUDE.md` — discipline rules 1–7, in particular rule 6 (a residual is
never support) as applied in §4.4.
