# CEG2 — wire-format extension sketch: `carries` as a governed ROOM COUNT

**Status:** spec sketch, issue-ready for `CIRISAI/RATCHET` (and, on adoption, for the CEG spec
repo). Nothing here is implemented. No conformance suite exists.
**Date:** 2026-08-22
**Baseline:** CEG **1.0-RC29**, vendored at
`/home/emoore/CEWP/analysis/tier4-registry-trust/CEG-1.0-RC29-spec/`.
**Companion documents:** `REG_SPEC.md` (v0.3, the lab-frame grammar), `CEG2_CARRIES_NOTE.md`
(the design decision this sketch expands), `CEG_REPRESENTATION.md` and `REG_A2A.md` (the two
no-go analyses that constrain it), `BRIDGE_STAKES.md` (what the format's blindness buys us).

**One-line summary.** CEG2 adds exactly one governed capability to CEG — declared, budgeted,
countable transport of a claim from one dimension to another — and it adds it using CEG's own
extension idiom, so that a CEG1 message is a CEG2 message with the budget set to zero.

---

## 0. Why this exists

CEG walls off cross-dimension transport by construction: dimensions are firewalled, and there is
no primitive that moves a claim from dimension `d` to dimension `d'`. That wall is a real defense
against a real attack — **kind-laundering**, a change smuggled past a per-dimension auditor while
wearing a different dimension.

But the transport happens anyway, in the world. It is the single most robustly measured
phenomenon in the taxonomy programme: deep kinds of change *arrive wearing* surface kinds, and
they do so through three specific, twice-localized channels (Premises/Facts, Structure/Manner,
Model/Facts). Walling it off does not stop it; it stops it from being **declared**, which means
it stops it from being **counted**.

CEG2's thesis is that the auditable form of a real phenomenon is better than the absence of a
name for it — provided the declaration is budgeted, so that declaring transport buys you a
bounded, countable amount of it and nothing more.

---

## 1. CEG 1.0-RC29 recap

Terms in this section are CEG's, not the taxonomy's. An engineer who knows CEG can skip to §2.

### 1.1 The 1+4 primitive set

RC29's own framing (`01_foundation.md` §1.4, verbatim):

> The federation has exactly **one workhorse attestation primitive + four structural composers**
> at the **structural layer**. That is a genuine, narrow invariant — the *graph-operation* set is
> closed at five (`scores` + `delegates_to` / `supersedes` / `withdraws` / `recants`). It is
> **not** a claim that the whole grammar is five things.

| primitive | object | typing | role |
|---|---|---|---|
| `scores` | an **entity** | prospective, no prior required | the workhorse claim: `dimension`, `score ∈ [-1,+1]`, `confidence ∈ [0,1]`, `context`, `evidence_refs[]`, `valid_until`, plus envelope fields (`epistemic_mode`, `witness_relation`, `cohort_scope`, …) |
| `delegates_to` | an **entity pair** (two keys) | prospective, no prior required | authority grant: `delegated_scope[]`, `delegation_purpose`, `delegation_valid_from`, `delegation_valid_until` |
| `supersedes` | an **attestation** | retrospective, prior required | replacement / doctrinal development |
| `withdraws` | an **attestation** | retrospective, prior required | retraction, under one of four admission rules |
| `recants` | an **attestation** | retrospective, prior required | falsity admission — **not** correction (plain correction is `supersedes`) |

The 1+4 lockdown is asserted 108 times across the RC29 tree with zero counterexamples. Three
candidate sixth primitives were checked and all three are extensions of the existing five, not
additions to them:

- **`promote`** (local-tier → federation-tier): *"a 'tier' is recorded state on an attestation,
  **not a new primitive**."* Scope promotion rides `supersedes`.
- **`moderate` / `takedown` / `review`** (§11.10): `delegated_scope` **vocabulary values** on the
  existing `delegates_to`, plus dimension prefixes that ride `scores`. *"**1+4 preserved.** …
  **No new structural primitive.**"*
- **`canonical_binding`** (§4.2.2.2): *"**NOT a new admission rule** (no 'rule 5'). It composes:
  the binding is itself a `delegates_to`-shaped attestation."*

**That third bullet is the pattern CEG2 follows.** Every extension CEG has accepted so far is
either a `delegates_to`-shaped declaration or an envelope vocabulary riding `scores`. CEG2 is both,
and nothing else.

### 1.2 Ordered-lattice composition

CEG aggregates in a **partial order**, never in a group. §8.2's table, per polarity column:

| polarity column | aggregation |
|---|---|
| `signed` | mean of `score × confidence` |
| `boolean-via-score` | **min** |
| `positive-only` | **max** |
| `-1.0 only` | **min** |
| `enumerated` | most-recent by `signed_at` |
| detector dimensions | **median** — *"resists adversarial mean-pulling by a single captured detector"* |

Composer status resolves by a **priority**, not a timestamp: `recants` wins regardless of
`signed_at`, giving the total order

```
live  <  superseded  <  withdrawn  <  recanted            (§6.1 rule 1)
```

with `recanted` absorbing. So the composer sector acts as a **join-semilattice** (status joins
upward) and the delegation sector as a **meet-semilattice** (authority meets downward, by scope
intersection). Both are monotone; neither is invertible. Composers are idempotent on the dedup
triple `(references_attestation_id, attestation_type, attesting_key_id)`, which the substrate MUST
dedup on (§6.1); the prospective pair `scores` / `delegates_to` carry no reference field and are
therefore free rather than idempotent.

The engineering requirement underneath all of this is §6.1's opening line: *"consumers MUST
compute a deterministic verdict"*, together with §5.6.8.13's *"Resolution MUST NOT require chain
completeness"*. Composition is **confluent**: every ordering fact lives in the data
(`signed_at`, canonical tie-breaks), not in emission order.

### 1.3 Acyclic delegation, and attenuation

- **Acyclicity** (§13.3): *"Substrate MUST detect cycles … and reject the cycle-closing
  emission."* Delegation depth is capped at 5.
- **Attenuation** (§11.10): `child.scope ⊆ parent.scope` — constraints addable, never removable.
  §13.3 additionally caps trust at `0.5 × root_trust`. **Gain around any path is < 1.**

These two plus order-independent composition are CEG's **three independent flatness
requirements**, each with a stated security reason. §4 returns to them, because they are what
CEG2 must not break.

---

## 2. The carries extension: budgeted channels with slot-consuming transports

### 2.1 The form, and why it is a room count rather than a cursor

The obvious design for `carries` is a *cursor* — a per-claim pointer recording that this claim
came from another dimension, with a weight attached. That design is auditable per instance and
unauditable in aggregate: the attack is **undeclared volume**, and a per-instance annotation
governs no volume at all.

CEG2 instead declares a **channel with a ceiling**, and makes each transport **consume a slot**
in it. The audit is then a count, computable by any consumer from the graph alone.

### 2.2 Channel opening — `delegates_to`-shaped

A carries-channel is declared by a `delegates_to`-shaped attestation. Sketch of the envelope
extension (names provisional; shape is the point):

```
attestation_type: delegates_to
delegated_scope:  ["carries:open"]
carries_channel: {
  channel_id:   <stable id>
  dim_from:     <dimension>          # the origin dimension
  dim_to:       <dimension>          # the destination dimension
  ceiling_R:    <non-negative int>   # ROOM: max concurrently-live transports
  w_max:        <float in (0,1]>     # bound on |w|, the transport weight MODULUS
  valid_from / valid_until:          # the validity window
}
```

Rules, each inherited from an existing CEG law rather than invented:

1. **Owner-bound.** The channel is bound to the declaring key exactly as a delegation is. Only
   claims under that key (or a lawful sub-delegate) may ride it.
2. **Revocable via `withdraws`.** No new revocation machinery. Withdrawing the channel
   attestation closes the channel; live transports through it become unbacked and a consumer
   MUST treat them as untransported (i.e. they fall back to their `dim_from` reading).
3. **Sub-channels ATTENUATE.** `R_child ≤ R_parent` and `w_max_child ≤ w_max_parent`. This is
   the child-scope-subset rule applied to *capacity*: **never amplify**, verbatim CEG law
   (§11.10). Ceilings compose by subset exactly as scopes do, so admission needs no new maths.
4. **Acyclicity applies to channels.** A channel graph that closes a cycle in `(dim_from,
   dim_to)` under a single owner is a cycle-closing emission and is rejected on the same MUST as
   delegation cycles (§13.3). See §4.1 — this is not a convenience, it is the flatness
   requirement.

### 2.3 Transport — rides `scores`

An ordinary `scores` attestation gains envelope members:

```
attestation_type: scores
dimension:        <dim_to>            # the claim LANDS on the destination dimension
transported_via:  <channel_id>
origin_dimension: <dim_from>          # cited, so the reading is reversible by a consumer
slot:             <k ∈ 1..R>          # unique-use within the channel's live set
transport_weight: <float, |w| ≤ w_max>
```

The claim lands on `dim_to` **citing its `dim_from` origin and the room it occupies**. A
consumer that does not understand carries reads it as an ordinary `scores` on `dim_to` and is
never wrong about what was claimed — only blind to where it came from. A consumer that does
understand carries can discount by `w`, or refuse transported claims entirely on dimensions it
audits strictly.

### 2.4 The audit is a room count

> Live transported attestations through channel `c` ≤ `R_c`.

That inequality is the whole audit. It is checkable by **any** consumer from the graph alone, with
no trust in the declarer, no cryptographic ceremony beyond what CEG already requires, and no
global state beyond the channel's own live set. Slot uniqueness makes over-subscription a
detectable duplicate rather than a silent overflow.

**Aggregate transport is the governed object.** Laundering cannot hide volume in instances,
because volume is exactly what the ceiling governs.

### 2.5 Why room-count beats cursor — four reasons, each independently sufficient

1. **Aggregate auditability.** The attack is undeclared volume; a ceiling governs volume. A
   cursor governs nothing.
2. **Conservation on the wire.** Declared-vs-measured channel usage becomes a standing audit
   metric, and the physics-likeness conservation criterion (P1) acquires a wire-format shadow.
   See §5 for the honest limits of that claim.
3. **Composition for free.** Ceilings compose by subset, like scopes. No new admission maths.
4. **Fail-secure default.** No channel declared → `R = 0` → carries impossible → CEG1 recovered
   exactly. See §6.

A fifth reason is a design analogy rather than an argument, and is flagged as such: in the
lattice-dynamics workstream, **finite occupancy plus exact conservation sectors** is the
combination that produced lawful, measurable dynamics, while unbounded amplitude bookkeeping
produced nothing measurable. That is a heuristic from a different substrate. It motivated the
design; it does not justify it.

### 2.6 Layer honesty

Wire-mechanically, this is **"1+4 preserved"** — the channel is `delegates_to`-shaped, the
transport is `scores` plus envelope vocabulary, and both are the spec's own extension idiom.
Semantically, it is a **sixth verb**: the charter's 1+4+1, matching REG v0.3's 5+1.

Both statements are true at different layers, exactly as `promote` is simultaneously "not a new
primitive" (wire) and "a distinct governance act" (semantics). The spec should say both, in that
order, and not pretend the semantic addition is nothing.

---

## 3. The safety differential — armor derived, not asserted

The steward's principle, stated in `REG_SPEC.md`:

> Defining CEG vs REG is STRONGER THAN CEG ALONE as a safety move: with REG as the lab frame,
> every CEG defense becomes derivable — "REG minus a named threat" — instead of asserted.

The value of this for a spec is concrete. A defense that is asserted must be defended by taste;
a defense that is derived can be **audited**, and its scope can be checked. The three attacks
below are named, and two of the three now have derivations. Where a derivation was *not* found,
this document says so — that correction is §3.4.

### 3.1 Loop-gain laundering → killed by flatness

**The attack.** Route a claim around a cycle in the authority graph so that it returns with more
weight than it left with. Gain ≥ 1 around a loop *is* laundering; that is the definition, not an
analogy.

**CEG's kill.** Acyclicity at MUST strength (§13.3, cycle-closing emissions rejected) plus
non-amplifying attenuation (§11.10, `child.scope ⊆ parent.scope`; trust capped at
`0.5 × root_trust`). On an acyclic graph every connection is flat vacuously; with gain < 1 on
every path there is nothing to accumulate.

**CEG2's obligation.** Channels are a second edge type in a graph that previously had one. §2.2
rule 4 extends acyclicity to them, and §2.2 rule 3 extends attenuation. **A carries channel that
could close a loop would reintroduce exactly the attack CEG kills**, so this is the one place
where CEG2's design is not optional.

### 3.2 Cancellation erasure → killed by lattice aggregation

**The attack.** An adversary attests in antiphase to erase honest standing — the honest aggregate
is driven to the identity by *adding* contributions.

**The derivation** (`REG_A2A.md` §6.1, the erasure theorem). Let a readout be
`V(M) = f(⊕_{i∈M} v_i)` over an aggregation monoid `(V, ⊕)`. Call it *erasure-resistant* if no
adversary can drive a non-identity honest aggregate to the identity by adding contributions.

- If `(V, ⊕)` is a **group**, the readout is **never** erasure-resistant: for honest aggregate
  `h`, the adversary emits `h⁻¹`.
- If `(V, ⊕)` is **idempotent** (a semilattice), then `h ⊕ a ≥ h` for all `a`: the aggregate is
  monotone non-decreasing and nothing can be undone. Erasure-resistant. ∎

**Corollary, and it is the differential in theorem form:** *erasure-resistance is **equivalent**
to the aggregation monoid having no invertible elements — i.e. to being naturally ordered. Any
grammar that permits cancellation between attesters has chosen a group, and every group is
erasable.*

This **derives** CEG's §8.2 aggregation table rather than merely observing it. `min` / `max` /
`median` were not a taste; they were the only available move. `mean` is a group operation in
disguise. And it shows that **ownership is provably no defense here**: ownership is a
record-layer constraint, while the readout factors through the sum, so it has *zero shadow on
the readout*.

**CEG2's obligation.** Transported claims land on `dim_to` as ordinary `scores` and aggregate
under `dim_to`'s existing polarity column. **They never introduce a new aggregation.** CEG2
must not offer a "net transport" aggregation, a signed channel balance that consumers read, or
any other group-shaped quantity at the readout — doing so would reintroduce erasure through the
side door.

### 3.3 Kind-laundering → walled by CEG, measured by REG, *governed* by CEG2

**The attack.** A change is smuggled past a per-dimension auditor while wearing another
dimension. In the taxonomy's plain words: a changed assumption arrives as a burst of changed
Facts, and an auditor watching Premises sees nothing.

**CEG's kill.** Firewalled dimensions: there is no primitive that transports across them.

**Why that kill is incomplete.** The wall stops *declared* transport. Undeclared transport is
precisely what the taxonomy programme measures happening, through three specific channels, on
every instrument that has looked. CEG's dimensions are firewalled on the wire and porous in
the world.

**CEG2's move.** Make the declared form cheap, bounded and countable, so that the undeclared form
becomes the anomalous one. The audit question changes from *"did any transport occur?"*
(unanswerable) to *"does declared channel usage account for observed cross-dimension
correlation?"* (a measurement, with a null). Room-count is what makes the second question
answerable: a declared ceiling is a prediction about volume that the graph can be checked
against.

**Stated honestly:** this is a *hypothesis about auditability*, not a proved defense. It has the
shape of the other two but not yet their status. It becomes a measurement when the agent-stream
series (see the companion RATCHET series proposal) reports declared-vs-measured channel usage.

### 3.4 A fourth attack, unnamed in the spec and cheaper than cancellation

`REG_A2A.md` §6.2 derives the dual of erasure, which CEG's own documents do not name:

> **Quadratic sybil gain.** With per-attestation bound `|z| ≤ 1`, `N` colluding attesters emitting
> in phase produce `|Σ|² = N²`, while `M` honest attesters with dispersed stance produce
> `E|Σ|² = M` (a random walk). Hence **`N` coordinated attesters match `N²` dispersed honest
> ones.** ∎

Two consequences worth carrying into the CEG2 spec's justification, because they invert a common
assumption:

1. **Erasure costs linearly; manufacture pays quadratically.** Erasing standing of magnitude `R`
   needs `⌈R⌉` emissions; manufacturing standing `N²` needs `N`. Manufacture is the cheap attack,
   not defacement.
2. **The reward is largest where it matters.** Coherent gain beats incoherent numbers only when
   honest opinion is *dispersed* — i.e. on contested subjects, where the verdict is
   consequential.

CEG's mean aggregation gives `N` colluders out of `N+M` a weight of `N/(N+M) < 1` — bounded,
saturating, sublinear. **This is a defense CEG already had and had not named.** CEG2 preserves it
by §3.2's obligation.

### 3.5 The correction — one of the three flatness requirements has no threat under it

`REG_A2A.md` §8.3(c), reported because the pair was built to find exactly this: of CEG's three
flatness requirements, two are threat-motivated and now derived (lattice aggregation via §3.2;
acyclicity via the delegation-laundering literature). **The third — order-independent composition
— has no threat under it.** It is forced by well-definedness of any route-independent readout:
consumers MUST compute a deterministic verdict, and a deterministic verdict cannot depend on the
route.

So the slogan "every CEG defense is REG minus a named threat" survives with a one-third
correction, and the correction should appear in the spec rather than be smoothed away. Two
defenses are armor. One is arithmetic.

---

## 4. The no-go results as design constraints

Two results are settled and constrain CEG2 absolutely. They are stated here as constraints, not
as findings, because that is how a spec must consume them.

### 4.1 CONSTRAINT 1 — verdict-producing grammars are flat. CEG2 stays flat.

CEG is flat by **threat model**: three independent normative requirements each forbid holonomy,
each for a stated security reason (§1.3, §3.1).

REG — built expressly as the branch that removes those defenses — turns out to be flat **anyway**,
by a second and independent mechanism: **readout well-definedness**. A verdict that is a coherent
sum over attesters is a function of the record *if and only if* the inter-attester frame
connection is flat. The generalization was staked forward, before any instrument existed:

> **FORWARD PREDICTION (staked 2026-08-21).** Any grammar whose readout is required to be a
> deterministic function of the record — i.e. any *verdict-producing* grammar, adversarial or not
> — reads zero loop phase by construction. Removing CEG's threat model is **not sufficient** to
> build a loop-phase instrument. The instrument must be a substrate whose aggregation is
> *permitted to be route-dependent*, which means it cannot be an accountability protocol at all.

**Design consequence.** CEG2 must not attempt to be a phase instrument, and should not be
criticized for failing to be one. Two mechanisms independently forbid it, and the second applies
to *any* successor spec that produces verdicts. A CEG3 that "fixed" this would not be an
accountability protocol.

**Immediate concrete rule:** §2.2 rule 4 (channel acyclicity) is non-negotiable, and channel
composition must remain order-independent — the room count of a composed path is the minimum
along it (attenuation), never a product that accumulates.

### 4.2 CONSTRAINT 2 — phase is NEVER representable in the wire format

The ceiling and the weight bound govern **modulus only**. `arg(w)` is not a field, has no
encoding, and must not acquire one. CEG's deployed wire format is modulus-only; phase lives
lab-side in REG+, where it belongs and where it can never be deployed.

**This is the sealed no-go, and it is not a limitation to be worked around.** It is the same
statement as §4.1 from the representation side: CEG's available phase group is `Z₂` (a sign), not
`U(1)`; linearity dies at `min`/`max`/`median`, and it was killed *deliberately, for a stated
adversarial reason*.

### 4.3 The positive flip — the format's blindness is the anti-laundering control

Here is why §4.2 is an asset rather than a concession, and it is the sharpest thing in this
document.

The research programme wants to measure phase-like signatures — route interference, holonomy — in
**corpus** dynamics. The standing objection to any such measurement is that the instrument
manufactured it. That objection is not paranoid; the programme has been burned by manufactured
floors before, and has a standing rule against scoring kills on instruments that produce the
result by construction.

Because CEG's wire format is provably **modulus-only**, any phase-like signature found in corpus
routes **cannot have been injected by the carrier format**. The instrument is provably blind to
the quantity it would be accused of manufacturing. From `BRIDGE_STAKES.md`:

> Therefore any phase-like signature found in corpus routes CANNOT have been injected by the
> carrier format: the instrument is provably blind to the quantity. This is the founding shape
> again (the carrier blind to what the whole carries), now working FOR the bridge: the format's
> blindness is the control that discovered corpus holonomy would be real.

**Design consequence, and it is a hard one.** If a future revision were to make phase
representable "for research convenience", it would **destroy this control**. The blindness has to
be preserved deliberately, as a property, with the reason recorded in the spec — otherwise
someone will helpfully add an `arg_w` field in a later RC and quietly invalidate every corpus
phase measurement taken under it.

---

## 5. What CEG2 does and does not buy for the conservation question

`CEG2_CARRIES_NOTE.md` claims that room-count gives the conservation criterion (P1) a
wire-format invariant. That claim needs bounding, because the programme's own scoring is
stricter than it.

**What is true.** The room count is a genuine wire-level invariant: live transports through a
channel ≤ its ceiling, checkable from the graph. Declared-vs-measured usage is a real standing
audit metric, and it is the kind of quantity a series can report.

**What is not yet true.** That invariant is a property of the *format*, not a measurement of the
*object*. P1 is currently scored **NOT EARNED** precisely because no corpus-side measurement
distinguishes conserved flow from estimator bookkeeping — confusion matrices are row-stochastic
by construction, which proves nothing. A ceiling that a substrate enforces is in the same
category: it is conserved because we made it so.

**The bridge, and it is BS-1's job, not CEG2's.** Conservation earns P1 only if measured leakage
in **carries-closed segments** — chains whose inflow and outflow are fully observed — is
distinguishable from an open-system null. CEG2's contribution is that it makes carries-closed
segments *identifiable on the wire*: a segment is closed when every transport in it cites a
declared channel and every channel's usage is accounted. That is a real and useful contribution.
It is not the measurement.

---

## 6. Versioning and migration

### 6.1 CEG1 messages are valid CEG2 with `R = 0`

The extension is **strict opt-in**. With no `carries_channel` declared, `R = 0`, transport is
impossible, and the grammar is CEG1 exactly — not approximately, not modulo a compatibility
shim. The 1+4 lockdown survives as the `R = 0` sector, and every existing conformance test
remains valid unmodified.

### 6.2 Consumer behaviour by capability

| consumer | sees a transported `scores` as | risk |
|---|---|---|
| **CEG1 consumer** (does not know the envelope members) | an ordinary `scores` on `dim_to` | never wrong about *what* was claimed; blind to *where it came from*. This is the honest failure mode and it is the safe direction. |
| **CEG2 consumer** | a transported claim with a cited origin, weight and slot | may discount by `w`, or refuse transported claims on dimensions it audits strictly |
| **CEG2 auditor** | the channel's live set against its ceiling | can compute the room count from the graph alone |

**The asymmetry is deliberate.** An old consumer under-reads (treats a transported claim as
native) rather than over-reads. If the opposite were true — if an old consumer could be induced
to *over*-trust — the extension would not be safe to ship incrementally.

### 6.3 Migration steps

1. **Reserve the vocabulary.** `carries:open` as a `delegated_scope` value; the `transported_via`
   / `origin_dimension` / `slot` / `transport_weight` envelope members. Reservation alone changes
   no behaviour and can land in an RC before anything is implemented.
2. **Substrate: enforce the count.** Slot uniqueness within a channel's live set; ceiling check on
   admission; channel-graph acyclicity; attenuation on sub-channels. All four reuse existing
   enforcement paths (dedup, admission, cycle detection, scope subset).
3. **Consumers: opt in.** Publish the discount semantics; leave the default as "read as native",
   which is what a CEG1 consumer already does.
4. **Audit: publish declared-vs-measured.** The standing metric of §5.

### 6.4 Open questions this sketch does not settle

Named, so they are not mistaken for settled:

1. **Does `w` need to exist at all?** A pure room count (`R` alone, no weight) is strictly
   simpler and loses only the ability to declare *partial* transport. The weight bound `w_max`
   is in this sketch because the taxonomy's channels have measured moduli, but the wire format
   may not need to carry them.
2. **Channel granularity.** Per `(dim_from, dim_to)` pair, or per owner, or per subject? This
   sketch says per pair per owner. The choice determines how sub-channel attenuation composes
   and should be settled against a real deployment, not by argument.
3. **What happens to live transports when a channel is withdrawn?** §2.2 rule 2 says they fall
   back to `dim_from`. The alternative — they become invalid — is fail-secure in a different
   direction and needs a threat-model argument, not a preference.
4. **Interaction with `supersedes` chains.** If a transported claim is superseded, does the
   successor inherit the slot or consume a new one? Slot inheritance is cheaper; slot consumption
   is stricter. Unresolved.
5. **The taxonomy's own open residual.** Removal-of-content currently has no artifact-local home
   in the 11+1 at wild grain, with three candidate resolutions open. If it resolves toward the
   Record axis, that is a *dimension* question, not a carries question — but it would change
   which channels are worth declaring, and CEG's `withdraws` already homes removals on Record
   3/3 in every alignment run.

---

## 7. Provenance of every claim in this document

Because the style discipline requires it: which statements are measured, which are proved, and
which are design.

| statement | status |
|---|---|
| CEG's 1+4 lockdown, aggregation table, acyclicity, attenuation | **quoted from RC29**, via the LEG_B extraction |
| the erasure theorem (§3.2) and quadratic sybil gain (§3.4) | **proved**, `REG_A2A.md` §6.1/§6.2 — theorems about aggregation monoids, not about CEG's implementation |
| verdict-producing grammars are flat (§4.1) | **staked forward 2026-08-21** before any instrument existed, then derived from readout well-definedness |
| phase is not representable (§4.2) | **sealed no-go**, two independent mechanisms |
| the three boundary channels (Premises/Facts, Structure/Manner, Model/Facts) | **measured**, panel study, independently re-localized by the Babel instrument |
| the surface four carry ~91% of change traffic | **measured**, staked forward at 0.89, read 0.883 on a never-touched stream |
| room-count beats cursor (§2.5) | **design argument**, four reasons; the lattice analogy is flagged as heuristic |
| kind-laundering becomes auditable under CEG2 (§3.3) | **hypothesis**, not yet a measurement; the named instrument is the agent-stream series |
| room count gives P1 a wire-format invariant | **bounded in §5** — a format property, not an object measurement; P1 remains NOT EARNED |
