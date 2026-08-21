# LEG B — CEG operation semantics, extracted from primary sources

**Scope.** The CIRIS Epistemic Grammar's operation set: names, preconditions, postconditions,
content typing, and the transition structure derivable from them. Derivation uses the spec's
**own** vocabulary. No eleven-kind taxonomy vocabulary is imported (that alignment is a later step).

**Leg independence.** `scratchpad/TRANSITION_MAP/` did not exist when this leg ran; the directory
was created by this leg. No LEG_A material was read.

---

## 0. Source located, and the version question settled

**Primary source:** `/home/emoore/CEWP/analysis/tier4-registry-trust/CEG-1.0-RC29-spec/`
— CEG **1.0-RC29** (`README.md:17`: *"**Version**: 1.0-RC29 (Release Candidate — 1+4 surface
FROZEN; additive transport/substrate absorption in progress)"*). Vendored 2026-06-19 from
`CIRISAI/CIRISRegistry` at commit `2fb7a2c` per `/home/emoore/CEWP/analysis/SOURCES.md`
("CEG 1.0-RC29 spec + CIRIS Constitution 0.4"). SOURCES.md states the home repo remains
canonical and every file under `analysis/` is a verbatim vendored copy.

**Second copy found:** `/home/emoore/CIRISConformance/reference/CEG/` — CEG **1.0-RC6**
(2026-06-15). Older.

**No version ambiguity on operation semantics.** The five semantics-bearing files are
**byte-identical** between RC6 and RC29 (`diff -q` clean on `02_grammar.md`, `03_primitives.md`,
`06_relations.md`, `07_reserved.md`, `13_anti_patterns.md`). Everything in this document is
therefore stable across both versions found on disk. Where RC29 adds material the older copy
lacks (notably §11.10/§11.11, RC19–RC27), that is flagged inline as **RC29-only**.

Other `ceg` directories under `/home/emoore` (`CIRISPersist/src/ceg`, `persist-*/src/ceg`,
`ciris/ceg`, `CIRISAgent-wt-wizard/ceg`) are implementation/outbox trees, not specification.
`/home/emoore/CIRISRegistry/FSD/CEG/` holds only a 2.6 KB README. `/home/emoore/CIRISCore` and
`/home/emoore/RATCHET` contain no CEG specification.

---

## 1. The operation set: **five**, framed as "1+4"

The steward's guess of "roughly five: assert / authorize / replace / retract / correct" is
**correct in count and nearly correct in naming**, with one substantive mismatch on the fifth.

§1.4 (`01_foundation.md`), verbatim:

> The federation has exactly **one workhorse attestation primitive + four structural composers**
> at the **structural layer**. That is a genuine, narrow invariant — the *graph-operation* set is
> closed at five (`scores` + `delegates_to` / `supersedes` / `withdraws` / `recants`). It is
> **not** a claim that the whole grammar is five things.

| Steward's name | Actual spec name | Match |
|---|---|---|
| assert | `scores` | yes — §3.1 "the workhorse" |
| authorize | `delegates_to` | yes |
| replace | `supersedes` | yes |
| retract | `withdraws` | yes |
| correct | `recants` | **partial** — `recants` is *falsity-admission*, not correction. Plain correction is `supersedes` (§3.2: doctrinal development is `supersedes`, "NOT `recants` (which would assert prior was false)"). "Correct" as an inter-content edge is the open-vocabulary `topical_relation:corrects` (§5.6.8, dimension-level, not an operation). |

**Count verification.** RC29 asserts the 1+4 lockdown 108 times across the tree ("no new
structural primitive" / "zero new structural primitives" / "1+4 preserved" / "no 1+4 change"),
with zero counterexamples. Three candidate sixth operations were checked and all three fail:

- **`promote`** (local-tier → federation-tier, §10.1.5) — `10_endpoints.md:139`:
  *"a 'tier' is recorded state on an attestation, **not a new primitive**."* Scope promotion
  (self → global) rides `supersedes` (§8.1.8.1, worked at §14.4).
- **`moderate` / `takedown` / `review`** (§11.10, RC29-only) — these are `delegated_scope`
  **vocabulary values** on the existing `delegates_to`, plus dimension prefixes
  (`moderation:*`, `takedown_notice`, `reconsideration:*`) that ride `scores`.
  `11_governance.md`: *"**1+4 preserved.** A `delegated_scope` vocabulary + enforced-admission
  addition over the existing `delegates_to` … **No new structural primitive.**"*
- **`canonical_binding`** (§4.2.2.2) — *"`canonical_binding` is **NOT a new admission rule**
  (no 'rule 5'). It composes: the binding is itself a `delegates_to`-shaped attestation."*

**The asymmetry that matters for transitions.** The "1" and the "4" are different kinds of thing,
and the spec says so (§3.2 heading, verbatim): the four are *"Operations on the attestation graph
itself, **not** score-claims on entities."* `scores` claims about an **entity**; the four operate
on **attestations**.

**A second, finer split inside the four — 3 + 1 by typing.** `supersedes`, `withdraws` and
`recants` each carry `references_attestation_id` and so require a prior attestation.
`delegates_to` does **not** — its envelope is
`{delegated_scope[], delegation_purpose, delegation_valid_from, delegation_valid_until}`, with no
reference field; it binds two *keys* (`attesting_key_id` → `attested_key_id`). So:

- **`scores`** — entity-typed, prospective, no prior required.
- **`delegates_to`** — entity-pair-typed, prospective, no prior required.
- **`supersedes` / `withdraws` / `recants`** — attestation-typed, retrospective, prior required.

This 1 + 1 + 3 typing is the backbone of the transition structure derived in §3.

The §2 **Object** axis confirms the typing vocabulary: *"key_id (entity) / attestation_id /
contribution_id."*

**Report the surface beside the invariant** (§1.4's own instruction, worth carrying forward):
the five is the *structural* invariant, not the conformance surface — that is ~12 `subject_kind`s,
~21 optional envelope fields, 13 composition policies (A–M), 5 canonicalization families,
6 `consensus_protocol` kinds, plus the §7 reserved-prefix taxonomy. §1.4 also states the adequacy
claim is *"an **inductive adequacy result, not a closure theorem**"* over sixteen tested paths.

---

## 2. The operations, with sourced pre/postconditions

### 2.1 `scores` — the workhorse

**Source:** `03_primitives.md` §3.1; envelope semantics `04_envelope.md` §4.

§3.1 verbatim: *"The federation has exactly **one** workhorse attestation primitive. Every claim
about an entity — positive or negative, identity or capability or behavior or state or commitment,
by any attester source — is expressed as a `scores` attestation on a named dimension."*

**Preconditions**
- Attester holds a `federation_keys.key_id` (`attesting_key_id`); subject named by `attested_key_id`.
- Required envelope members (§4): `dimension`, `score` ∈ [−1.0, +1.0], `confidence` ∈ [0.0, 1.0].
- `dimension` must use a prefix admitted through the §1.3.1 four-test gate (T1 rules/verdicts
  separated; **T2 mechanism-descriptive not subjective-quality**; T3 version-pinned re-checkable;
  T4 never sole evidence for `slashing:*`).
- Conditional-required: `community_id` **iff** `cohort_scope == community`; `family_id` **iff**
  `cohort_scope == family` — §4 states the substrate *rejects* scoped Contributions missing the field.
- Some dimensions require non-empty `evidence_refs` by per-dimension policy (§5).
- **No prior record is required.** §6 classifies the no-reference case as **Standalone**:
  *"Self-contained attestation; no `references_attestation_id`."*

**Postconditions**
- A new attestation row exists carrying the claim.
- §1.2 consequence 2 (informative): *"The attester's score participates in constituting the
  entity's standing in the relational field that consumers compose policy over."*
- **No prior attestation changes state.** (Derived in §3.1 below.)

**Typing.** Applies to an **entity** on a named **dimension**, discriminated by `subject_kind`.

---

### 2.2 `delegates_to` — authorize

**Source:** `03_primitives.md` §3.2 / §3.2.1; `11_governance.md` §11.10 (RC29-only);
`13_anti_patterns.md` §13.3; `08_composition.md` §8.1.12.7 / §8.1.12.7.1.

§3.2 table verbatim: *"A authorizes B to sign on A's behalf within a bounded scope"* —
envelope `{delegated_scope[], delegation_purpose, delegation_valid_from, delegation_valid_until}`.

**Preconditions**
- The delegator holds the authority being delegated. Made normative for moderation duties at
  §11.10 admit-(b): *"the **root holds the duty over the target** and is **owner-bound**
  ([§5.6.8.10] — an accountable human)."*
- **Sub-delegation requires explicit grant** (§11.10): *"A `delegates_to` MAY permit its delegate
  to **deputize** … but **only if the delegator granted it**, by including `sub_delegation` in the
  granted `delegated_scope`."*
- **Attenuation** (§11.10): *"Every sub-delegation **attenuates, never expands**:
  `child.scope ⊆ parent.scope`, and constraints may be *added* but never removed."*
- **Depth ≤ 5** (§13.3, consumer-policy default, configurable).
- **Acyclicity** (§13.3): *"Substrate MUST detect cycles on the `delegates_to` graph and reject the
  cycle-closing emission."*
- **Agency gate** (§8.1.12.7, RC29): a delegate whose `identity_type` is `node`-only (no brain)
  MUST carry **only** `infra:*` scopes; *"a verifier MUST **reject** (treat as non-conformant,
  never grant) an `infra`-only key presenting any `agency:*` scope."*
- `delegated_scope[]` is set-semantics → lexicographically sorted before signing (§0.9.2.1).

**Postconditions**
- B may sign on A's behalf within `delegated_scope`, bounded by
  `[delegation_valid_from, delegation_valid_until]`.
- The grant is **revocable at any link** (§11.10, quoted under `withdraws` below).
- §3.2.1: also serves as the **authority-source claim** shape — naming a framework/principle as
  the source of a constitutional claim, replacing a `grounding:{tradition}:{principle}` prefix
  that would fail the §1.3.1 T2 gate.

**Typing.** Applies to an **entity pair** (delegator key → delegate key) over a **scope vocabulary**.
Not to a prior attestation.

---

### 2.3 `supersedes` — replace

**Source:** `03_primitives.md` §3.2; `06_relations.md` §6 / §6.1; `08_composition.md` §8.1.8.1;
`14_glossaries.md` §14.4 (worked example); `05_namespace.md` §5.6.8.13.

§3.2 table verbatim: *"This attestation row replaces a prior one **by the same attester**"* —
envelope `{references_attestation_id, supersession_reason, differs_in[]}`.

**Preconditions**
- `references_attestation_id` resolves to a prior attestation.
- Nominally by the same attester. **Honest flag:** §3.2 states this in the primitive table as a
  description, not as a MUST-reject at admission. §6.1 rule 4 handles the cross-attester case by
  *evaluating each attester's chain independently* ("the consumer sees N parallel chains"), so a
  cross-attester `supersedes` is not rejected — it simply does not bind the other attester's chain.
  Treat "same attester" as scoping, not as a prohibition.
- Idempotent and deduplicated on `(references_attestation_id, attestation_type, attesting_key_id)`
  (§6.1): *"replaying the same composer is a no-op. The substrate MUST dedup on this triple."*

**Postconditions**
- The prior ceases to be the resolution target. §8 uses the predicate **"latest non-superseded"**
  throughout as the live-entry selector (`08_composition.md` lines 321, 340, 575, 600; defined at
  line 589, stated there for the `community` subject_kind, as *"the `community` Contribution with
  the highest `signed_at`; on equal `signed_at`, the higher `canonical_bytes_hash` ([§0.9]) wins
  (total order, no ambiguity)"* — note this tie-break differs from §6.1 rule 3, which breaks
  same-`signed_at` composer races on the **lexicographically smallest** `attestation_id`).
- **No falsity claim is made about the prior.** §3.2: doctrinal development ("extends but does not
  contradict") is `supersedes`, *"NOT `recants` (which would assert prior was false)."*
- A replacement enters. §14.4's worked promotion carries `new_dimension` / `new_score` /
  `new_confidence` / `new_evidence_refs` / `new_cohort_scope` in the `supersedes` envelope itself.
- §14.4 pattern recap: *"widens `cohort_scope`, optionally morphs `sub_kind`, preserves
  `content_sha256` (no body re-upload), chains via `supersedes`. The promotion lineage is walkable
  via `references_attestation_id`."*

**Subject-kind-dependent caveat (§5.6.8.13, RC1-RC2 operational data):** for `organization` /
`org_membership` / `partner_record`, resolution is **stable-id grouping, NOT chain-walk**, and
*"`supersedes` references SHOULD be emitted when the prior is known and serve as **audit lineage
only** — decoration, never resolution."* So `supersedes`'s state effect is not uniform across
subject_kinds. This is the one place where the operation's postcondition is downgraded to
bookkeeping.

**Typing.** Applies to a **prior attestation**, carrying a replacement payload.

---

### 2.4 `withdraws` — retract

**Source:** `03_primitives.md` §3.2 / §3.2.3; `04_envelope.md` §4.2; `10_endpoints.md` §10.1.3 /
§10.1.6; `11_governance.md` §11.8.2 / §11.10 / §11.11; `13_anti_patterns.md` §13.4.

§3.2 table verbatim: *"I retract my prior attestation (**does NOT claim it was false**)"* —
envelope `{references_attestation_id, withdrawal_reason}`.

**Preconditions — the broadened four-rule admission (§3.2.3, CEG 0.6).**
*"Substrate MUST admit a `withdraws` Contribution against target `T` when the issuer's `key_id`
satisfies **ANY** of:"*

| # | Authority path |
|---|---|
| 1 | `issuer.key_id == T.attesting_key_id` — producer self-withdraw |
| 2 | `issuer.key_id ∈ T.subject_key_ids` — subject revocation |
| 3 | ∃ `delegates_to` chain: `issuer →* canonical_hash` where `canonical_hash ∈ T.subject_key_ids` AND `scope ⊇ {consent_revocation}` — proxy authority for non-enrolled subjects |
| 4 | `issuer` holds valid `delegates_to → any of 1-3` — delegated revocation |

- §3.2.3 also requires per-rule audit metadata: substrate SHOULD record **which** rule admitted
  each `withdraws`.
- Same idempotence/dedup triple as `supersedes` (§6.1).

**Postconditions**
- The prior is withdrawn; **truth-at-issuance is untouched** (the parenthetical in §3.2 is the
  whole distinction from `recants`).
- **The record survives.** §11.8.2 heading: *"Leaving is forward-only — the audit chain preserves
  the historical claim"*; body: *"The withdrawn `location_proof` Contribution **remains in the
  audit chain** — federation peers retain the historical record."* Withdrawn ≠ deleted.
- **Forward-only / no resurrection** (§10.1.6): *"an admitted `withdraws` (deactivation) is
  forward-only — a later non-withdrawn write does NOT resurrect."*
- **Against a `delegates_to`, it cascades** (§11.10): *"revocable at any link: a `withdraws`
  against **any** `delegates_to` in the chain invalidates everything downstream of it (UCAN-style
  proof-chain revocation) … can sever the entire subtree with a single revocation."*
- **Forced tier promotion for subject-side revocation** (§10.1.3): *"Consent revocations from
  subjects **MUST NOT** use the local-tier deferral path … any subsequent `consent:state:revoked`
  emission OR `withdraws` admitted under §3.2.3 rule 2 or 3 from a subject in that set MUST promote
  to federation-tier within a bounded window. Default window: **24 hours**."*
- **RC29-only, §11.11 rule 2 — a withdrawal that induces a grant.** *"When the named moderator
  lapses (`withdraws` against the `moderate` `delegates_to`, or inactivity past the community's
  freshness window), the member with the **highest `moderation_track_record`** is **automatically
  granted** the `moderate` duty"* — deterministic (track record, then earliest membership, then
  lexicographic `key_id`, *"so every peer auto-promotes the same member"*). If no eligible member
  exists the community **fails-secure** and MUST NOT federate: *"Better no group than an
  unmoderated one."*

**Typing.** Applies to a **prior attestation** — including, distinctively, to a prior
`delegates_to`, which is how authority is revoked.

---

### 2.5 `recants` — admit falsity

**Source:** `03_primitives.md` §3.2 / §3.2.2 / §3.2.3; `06_relations.md` §6.1;
`13_anti_patterns.md` §13.4.

§3.2 table verbatim: *"My prior attestation was false at issuance — admits epistemic error"* —
envelope `{references_attestation_id, recantation_reason, what_was_false}`.

**Preconditions**
- `references_attestation_id` resolves to a prior attestation.
- **Original attester only** (§3.2.3, verbatim): *"subject-side authority does NOT extend to
  `recants` (the falsity-admission primitive) — only the original attester can `recant` their own
  claim."* This is the sharpest asymmetry in the operation set: the consent axis is shared with the
  subject; the **truth axis is producer-exclusive**.
- Same idempotence/dedup triple (§6.1).

**Postconditions**
- The prior is marked false **at issuance**, with `what_was_false` naming the content of the error.
- **Outranks the other two composers unconditionally** (§6.1 rule 1): *"`recants` outranks
  `withdraws` outranks `supersedes` at the structural level. If the same attester emits multiple
  composers against the same prior attestation, `recants` wins **regardless of `signed_at`**
  (a falsity admission cannot be subsumed by a retraction or replacement)."*
- **A reflexive effect on the attester** (§3.2.2): *"Consumer policy can apply different trust
  adjustments to attesters who `recant` versus those who `withdraw`."* The operation changes the
  standing of the *operator*, not only of the target.

**Why it exists as a primitive at all** (§3.2.2, verbatim): *"no prior identity system (PGP,
SPKI/SDSI, W3C VC) typed epistemic-error-admission as a wire primitive distinct from retraction.
CEG types both because the Recursive Golden Rule applies to attesters: admitting error is a
primary act, not a derivative of retraction."*

**Typing.** Applies to a **prior attestation**, by its own author.

---

### 2.6 The eight relations, and which four are operations

§2's eighth axis and §6 together fix which relations are *structural* (operations) and which are
*emergent* (side effects of composition). This matters because emergent relations look like
transitions and are not:

| Relation | Realization (§6, verbatim) |
|---|---|
| Standalone | *"Self-contained attestation; no `references_attestation_id`."* |
| Refers-to-prior | *"Points to another attestation via `evidence_refs[]` or `context`; doesn't modify it."* **Emergent.** |
| Supersedes-prior | **`supersedes` structural primitive.** |
| Contradicts-prior | *"Emergent from negative score on a dimension where a prior positive exists."* **Emergent.** |
| Withdraws-prior | **`withdraws` structural primitive.** |
| Recants-prior | **`recants` structural primitive.** |
| Clarifies-prior | *"Emergent from updated score with refined context on the same dimension+object."* **Emergent.** |
| Delegated | **`delegates_to` structural primitive.** |

Four emergent, four structural. The emergent four are all realizations of `scores`; note that
"refers-to-prior" is explicitly marked *"doesn't modify it."*

---

## 3. Derived transition structure

### 3.0 First: what the state vocabulary actually is

**The spec has no single named status enum for an attestation.** It has *predicates* scattered
across §6.1, §8, and §10.1.6. The state names used below are reconstructed from those predicates,
and each is sourced. This is a derivation, not a quotation, and it is the one place in this
document where I am building vocabulary rather than lifting it.

| Axis | States | Source of the predicate |
|---|---|---|
| **Currency** | live (= *"latest non-superseded"*) / superseded / withdrawn | §8 resolution predicate; §6.1 precedence; §10.1.6 forward-only |
| **Truth-at-issuance** | not-asserted-false (default) / false-at-issuance | §3.2 `recants` vs the explicit "does NOT claim it was false" on `withdraws`/`supersedes` |
| **Authority** | no scope / holds scope S, window-bounded | §3.2 `delegates_to`; §11.10 admit-(a)/(b) |
| **Cohort scope** | self / family / community / affiliations / species / biosphere / federation | §2 Scope axis; §4 `cohort_scope` |
| **Tier** | local / federation | §10.1.5; §10.1.3 |
| **Event lifecycle** | open / cancelled / completed / superseded | §5.6.8.5 `event:lifecycle:{state}` — the spec's own worked state machine |
| **Consent stance** | granted / revoked / expired | §5.6.8.7 `consent_record.stance` |

Crucially, **§5.6.8.5 shows the label and the change are carried by different operations**:
*"Lifecycle state is consumer-side composition over the structural primitives + this dimension's
latest non-superseded emission."* The `scores` attestation carries the *label* of state; the
composers carry the *change* of state. Neither alone is the state. This is the single most
load-bearing structural fact for a transition map.

---

### 3.1 `scores` — the only operation with an empty precondition, and the only one that changes nothing

1. §3.1's wire shape contains no `references_attestation_id`; §6 classifies the no-reference case
   as **Standalone**. → `scores` cannot name a prior attestation.
2. Therefore it has no precondition on any existing content-state. Its only lawful input state is ∅.
3. §3.1 + §4: the postcondition is a new row bearing `(dimension, score, confidence)`.
4. Therefore: **(∅) → (live attestation by A about O on dimension D)**.
5. §6 lists *contradicts-prior* and *clarifies-prior* as **emergent**, and lists only
   `supersedes`/`withdraws`/`recants` in §6.1's precedence rules — i.e. only those three are in the
   state-changing set. → a second `scores`, even one carrying the opposite sign, leaves the first
   attestation **live**.
6. Therefore the prior's transition under a contradicting `scores` is **(live) → (live)**:
   two contradictory claims coexist and the consumer composes. Disagreement is *not* retraction.
7. Via the `event:lifecycle:{state}` family (§5.6.8.5), `scores` also carries **state labels**:
   `open` / `cancelled` / `completed` / `superseded`. By step 5 this label is a claim, not a
   change — the change requires the paired composer.

**Transitions carried:** ∅ → live (its own row). None, on any other row.

---

### 3.2 `delegates_to` — transitions in the authority relation, not in content state

1. §3.2's envelope has no reference field and binds `attesting_key_id → attested_key_id`. → the
   object of the transition is an entity pair, not a content entry.
2. Precondition (§11.10 admit-(b)): the root holds the duty and is owner-bound. →
   **(B holds ∅ over target T) → (B holds scope S over T)**.
3. §11.10 attenuation (`child.scope ⊆ parent.scope`, constraints added never removed) → along a
   chain the scope is **monotone non-increasing**:
   **(B holds S) → (C holds S′ ⊆ S)**, and only if `sub_delegation ∈ S`.
4. `delegation_valid_from` / `delegation_valid_until` → every authority state is
   **window-bounded**; outside the window the state is (holds ∅) with no operation required.
   This is the one state change in the whole grammar that occurs by the passage of time rather
   than by an emission.
5. §13.3 depth cap: a chain longer than 5 does not error — it **degrades**:
   *"chains longer than the cap are treated as `attestation:self_verify` only (no transitive
   trust)"*. → **(chain of depth 6) → (no transitive authority)**.
6. §13.3 cycles: the cycle-closing emission is rejected → the transition **does not occur at all**.
   Contrast with step 5: over-depth degrades, cycles are refused.
7. §8.1.12.7: onto a `node`-only identity, only `infra:*` scopes; `agency:*` MUST be rejected. →
   the reachable authority-state set is **typed by the delegate's `identity_type`**.
8. A `delegates_to` is itself an attestation, so it is in the domain of the three retrospective
   composers — which is exactly how §3.2.3 rule 4 and §11.10 revocation work.

**Transitions carried:** ∅ → holds-S (grant); holds-S → holds-S′⊆S (attenuating sub-delegation);
holds-S → ∅ (window expiry, no emission).

---

### 3.3 `supersedes` — a *paired* transition; moves currency, never truth

1. Precondition: a prior exists (§3.2). → input state must be a live-or-superseded entry.
2. Postcondition on the prior: it stops satisfying §8's "latest non-superseded" predicate. →
   **(live) → (superseded)**.
3. §3.2's doctrinal-development clause states no falsity claim is made. → the **truth axis is
   unchanged**: (not-asserted-false) → (not-asserted-false).
4. §14.4 carries `new_*` members in the same envelope. → simultaneously **(∅) → (live)** for the
   replacement. The operation is a *pair* of transitions, which is precisely what distinguishes
   "replace" from "retract".
5. §8.1.8.1 / §14.4 scope promotion: `differs_in: ["cohort_scope", "sub_kind"]`, `content_sha256`
   preserved → **(cohort_scope: self) → (cohort_scope: global)**, and
   **(sub_kind: draft) → (sub_kind: article)**, with the body unmoved.
6. §5.6.8.5 reschedule: `supersedes` with `differs_in: ["start_time","venue"]` →
   **(event: open) → (event: superseded)**.
7. §5.6.8.8.2 / CEG 0.18: `encryption_pubkeys` is *"`supersedes`-rotatable (rotate a KEM key
   without touching the signing identity)"* → **(occurrence bearing KEM key K) → (occurrence
   bearing K′)**, identity invariant.
8. §5.6.8.13 caveat (step 2 does **not** hold for `organization`/`org_membership`/`partner_record`):
   there `supersedes` is *"audit lineage only — decoration, never resolution"*, and currency is
   decided by stable-id grouping. → the currency transition is **subject-kind-conditional**.

**Transitions carried:** (live) → (superseded) **and** (∅) → (live), as one act; scope-widening;
sub_kind morph; key rotation; event open → superseded.

---

### 3.4 `withdraws` — moves currency, never truth; absorbing; cascades on authority

1. Precondition: a prior exists, and the issuer satisfies one of the four §3.2.3 rules. → unlike
   the other two retrospective composers, **the issuer need not be the author**.
2. Postcondition: **(live) → (withdrawn)**, with §3.2's explicit *"does NOT claim it was false"* →
   **truth axis unchanged**.
3. §11.8.2: the withdrawn Contribution *remains in the audit chain*. → **(withdrawn) is not
   (absent)**. The historical claim stays provable; only its currency is spent.
4. §10.1.6 `withdrawal_forward_only`: a later non-withdrawn write does not resurrect. →
   **(withdrawn) is absorbing** on the currency axis for that stable id. There is no
   (withdrawn) → (live) transition anywhere in the grammar.
5. Applied to a `delegates_to` (§11.10): everything downstream of the severed link is invalidated.
   → **one-to-many**: (authority chain live at L and below) → (L and its entire subtree invalid).
   This is the only operation with a fan-out postcondition.
6. §10.1.3: a `withdraws` admitted under rule 2 or 3 must promote within 24 h. → it drags a
   second-axis transition with it: **(tier: local) → (tier: federation)**, compulsory.
7. §11.11 rule 2 (RC29): a `withdraws` against a `moderate` `delegates_to` triggers deterministic
   auto-promotion of the highest-track-record member. → **the one place in the grammar where a
   lowering operation deterministically induces a raising one.** Authority does not vanish; it
   relocates. And if it cannot relocate, §11.11 rule 3 fails the whole community secure.

**Transitions carried:** (live) → (withdrawn), absorbing; (tier: local) → (tier: federation),
compulsory on subject-side revocation; (authority subtree live) → (invalid), cascading;
(no moderator) → (merit-promoted moderator), induced.

---

### 3.5 `recants` — the only operation that moves the truth axis; terminal

1. Precondition: a prior exists, **and the issuer is its original author** (§3.2.3). → the domain
   is strictly narrower than `withdraws`'s.
2. Postcondition: **(not-asserted-false) → (false-at-issuance)**, with `what_was_false` naming the
   error. By §3.2's phrasing on the other two, this is the **only** operation that moves this axis.
3. §6.1 rule 1: `recants` outranks the other two *regardless of `signed_at`*. → the transitions
   **(superseded) → (recanted)** and **(withdrawn) → (recanted)** are lawful and take effect out of
   time order.
4. The converse is explicitly denied — *"a falsity admission cannot be subsumed by a retraction or
   replacement"* → **(recanted) → (superseded)** and **(recanted) → (withdrawn)** do not take
   effect. Combined with step 3: **(recanted) is the terminal state** of the composer order.
5. §3.2.2: consumers may adjust trust in the *attester*. → a second, **reflexive** transition:
   **(attester standing s) → (attester standing < s)**. No other operation is stated to change the
   standing of the party performing it.

**Transitions carried:** (live | superseded | withdrawn) → (recanted), terminal; and reflexively,
the attester's own standing downward.

---

### 3.6 The composed picture

Currency axis (one entry, one attester's chain):

```
        scores
   ∅ ──────────▶ live ──── supersedes ───▶ superseded ─┐
                  │                                     │
                  ├──── withdraws ───▶ withdrawn ───────┤   (both, out of time order,
                  │                        ▲            │    by §6.1 rule 1)
                  │                        │ absorbing  │
                  │                     (no return)     ▼
                  └──── recants ──────────────────▶ recanted  [terminal]
```

Authority axis (a `delegates_to` chain):

```
   ∅ ──── delegates_to(S) ───▶ holds S ──── delegates_to(S′⊆S) ───▶ holds S′ ── … (depth ≤ 5)
                                  │
                                  ├── window expiry ──▶ ∅        (no emission needed)
                                  └── withdraws ──────▶ ∅ and the whole subtree below
```

Three facts fall out that a transition map should carry:

- **Every transition is forward-only.** §1.4 says it in the spec's own words: CEG attestations are
  *"unilateral, monotonic graph claims."* Nothing returns to `live`; nothing un-recants; nothing
  un-supersedes; §11.8.2 preserves the history rather than rewriting it. The grammar has no undo,
  only further claims.
- **Two independent axes, not one line.** `supersedes` and `withdraws` move currency and are
  explicitly silent on truth; `recants` moves both. The §6.1 precedence order is *not* a strength
  ordering on one scale — it is the statement that the truth axis dominates the currency axis when
  both are asserted by the same attester.
- **The label and the change are separate emissions.** §5.6.8.5: state is *"consumer-side
  composition over the structural primitives + this dimension's latest non-superseded emission."*
  A transition map keyed only on the composers will miss the `scores`-borne lifecycle label, and
  one keyed only on labels will miss every actual state change.

---

## 4. Orientation: which operations raise, lower, preserve

The spec supplies one explicit ranking (§6.1: `recants` > `withdraws` > `supersedes`) and one
explicit monotonicity statement (§1.4: *"unilateral, monotonic"*). Everything else below is derived,
and the derivation shows the ranking is **not** an orientation on a single scale — it needs four.

| Operation | Currency of target | Truth-at-issuance of target | Authority | Attester's own standing |
|---|---|---|---|---|
| `scores` | — (creates its own; changes no other) | — | — | — (but §1.2: it constitutes the *attested* entity's standing, sign-dependent) |
| `delegates_to` | — | — | **raises** the delegate's, never above the delegator's (attenuating) | — |
| `supersedes` | **lowers** (live → superseded) | **preserves** (explicitly) | — | — |
| `withdraws` | **lowers** (live → withdrawn, absorbing) | **preserves** (explicitly) | **lowers**, cascading, when aimed at a `delegates_to` | — |
| `recants` | **lowers** (terminal) | **lowers** (the only operation that does) | — | **lowers** (§3.2.2, §13.4) |

Reading the orientation question directly:

- **Raise:** only `delegates_to` (authority), and only non-amplifyingly — `child.scope ⊆
  parent.scope` means the system-wide authority total never increases. `scores` with a positive
  sign raises the *attested* entity's standing per §1.2, but that is the informative anthropology
  section, not a normative postcondition, and §1.2 is explicitly marked *"informative … an
  implementer may reject this anthropology and still be fully conforming."*
- **Lower:** `supersedes`, `withdraws`, `recants` — in that increasing order of severity, which is
  §6.1's ranking, and the severity is measured by how many axes each moves (one, one-plus-cascade,
  two-plus-reflexive).
- **Preserve:** `supersedes` and `withdraws` both preserve truth-at-issuance, and this is stated
  twice and load-bearingly (§3.2's parenthetical and §3.2.3's producer-exclusivity clause).
  `scores` preserves everything about every other entry.
- **The genuine surprise:** `recants` is the only operation whose cost falls on the *operator*.
  Every other operation's postcondition lands on its target. §13.4 exists precisely because that
  asymmetric cost is exploitable.

---

## 5. Duality and pairing

**One true inverse pair, and it is asymmetric.**
`delegates_to` ↔ `withdraws`, stated outright at §11.10: *"revocable at any link: a `withdraws`
against any `delegates_to` in the chain invalidates everything downstream of it."* The asymmetry is
structural and deliberate: `delegates_to` grants along **one edge**; `withdraws` severs **an entire
subtree**. Grant is local, revocation is global-downward. That is UCAN-style proof-chain revocation
and the spec names the lineage (UCAN / macaroons / SPKI-SDSI / ZCAP-LD).

**One sibling pair separated by exactly one bit — *not* a duality.**
`withdraws` and `recants` share an envelope shape modulo `what_was_false` and differ on exactly one
question: is a falsity claim made? §3.2.2 insists they are co-primary, not derived from one another:
*"admitting error is a primary act, not a derivative of retraction."* They are not inverses of
anything; they are two exits from `live` that differ in which axis they move. §13.4 is the spec's own
acknowledgement that the gap between them is arbitrage-able, with a consumer-policy countermeasure
(a `withdraws:recants` ratio, default threshold 5:1) rather than a wire fix.

**`scores` has an *internal* polarity that is not a pairing.**
Its `score` field is signed on [−1, +1], so the "opposite" of an assertion is another assertion. But
by §6 that yields the **emergent** relation *contradicts-prior*, and by §3.1/§3.2's split it is not
a graph operation: both attestations stay live and the consumer composes. **CEG deliberately
separates disagreement from retraction.** A negative `scores` is not the inverse of a positive one
in any state-transition sense — it is a second, coexisting claim. This is the pairing a transition
map is most likely to get wrong.

**`supersedes` has no inverse.** There is no un-supersede operation, and by §10.1.6's forward-only
rule and §11.8.2's audit-chain preservation there cannot be one. The only response to a supersession
is a further supersession.

**No operation is involutive; no operation is a retraction of itself.** The composers are idempotent
on `(references_attestation_id, attestation_type, attesting_key_id)` (§6.1) — replaying one is a
no-op, not a toggle. So the operation set forms no group and no involution: it is a
monotone forward-only rewriting system, exactly as §1.4's "unilateral, monotonic" states.

**One near-pairing worth flagging:** §11.11's merit auto-promotion makes a `withdraws` against a
`moderate` delegation *induce* a fresh `delegates_to`. That is not a duality but it is the only
closed loop in the grammar — authority lowered at one key is deterministically raised at another,
with a fail-secure floor if it cannot be.

---

## 6. What the spec itself marks forbidden or invalid

Normative prohibitions, quoted or tightly paraphrased with source:

| # | Prohibition | Source | Strength |
|---|---|---|---|
| 1 | *"Substrate MUST detect cycles on the `delegates_to` graph and reject the cycle-closing emission."* | §13.3 | MUST |
| 2 | Delegation depth cap 5 by default; over-cap chains *"are treated as `attestation:self_verify` only (no transitive trust)"* | §13.3 | MUST (consumer policy), configurable |
| 3 | Aggregate-weight concentration: cap any single terminal delegate's accumulated trust from one root at *"0.5 × root_trust by default"* | §13.3 | SHOULD |
| 4 | Sub-delegation only if `sub_delegation` ∈ granted scope; *"Every sub-delegation attenuates, never expands: `child.scope ⊆ parent.scope`, and constraints may be added but never removed"* | §11.10 | normative |
| 5 | *"a verifier MUST reject (treat as non-conformant, never grant) an `infra`-only key presenting any `agency:*` scope"* — "infrastructure must not have agency" made wire-checkable | §8.1.12.7, §1.3 | MUST |
| 6 | *"subject-side authority does NOT extend to `recants` … only the original attester can `recant` their own claim"* | §3.2.3 | normative |
| 7 | *"Consent revocations from subjects MUST NOT use the local-tier deferral path"*; must promote within 24 h | §10.1.3 | MUST NOT |
| 8 | *"a falsity admission cannot be subsumed by a retraction or replacement"* — `recants` wins regardless of `signed_at` | §6.1 | MUST (precedence) |
| 9 | Withdrawal is forward-only: *"a later non-withdrawn write does NOT resurrect"* | §10.1.6 | normative |
| 10 | Composers idempotent on `(references_attestation_id, attestation_type, attesting_key_id)`; *"The substrate MUST dedup on this triple"* | §6.1 | MUST |
| 11 | *"Resolution MUST NOT require chain completeness"* — partition tolerance; `supersedes` refs are audit lineage only for operational subject_kinds | §5.6.8.13 | MUST NOT |
| 12 | RC29: the principal is the chain root, never a payload field — *"there is deliberately no `on_behalf_of` (or equivalent) envelope field"*; *"Absence of a principal field is NOT an admit condition"*; a verifier *"MUST NOT read 'no field present' as 'as-self'"* | §11.10 | MUST NOT |
| 13 | RC29: subject authority resolves from the content's **establishing attestation**, never the action payload; the payload's `subject_key_ids` is *"advisory only"* on that path; unresolvable provenance **fails** (does not admit) | §11.10 | MUST NOT |
| 14 | RC29: a community MUST NOT federate without ≥1 live `moderate`-holder — *"Better no group than an unmoderated one."* | §11.11 | MUST NOT |
| 15 | Substrate rejects `cohort_scope: community` / `family` Contributions missing `community_id` / `family_id` | §4 | rejection |

**Marked as anti-patterns rather than invalid** (§13 — *"A CEG-Conforming Producer SHOULD NOT
emit attestations matching the anti-patterns below"*):

- Five rejected wire additions (§13.1), each failing the §1.3.1 T2 mechanism-vs-quality gate:
  `detection:emergent_deception:{axis}`, `attestation:l{N}:*`, `score:trustworthiness:{entity}`,
  `flag:bad_actor:{axis}`, `grounding:{tradition}:{principle}`.
- Six CEG-0.1 rejections from the 283-story stress test (§13.2), including
  `epistemic_mode: introspection` — rejected as a *"Cartesian shortcut — lone subject pre-declaring
  inner state as if that constitutes standing."*
- `withdraws` arbitrage (§13.4): dodging the recant penalty. Countermeasure is consumer-policy ratio
  tracking, *"not a wire-format change."*
- §13.5, the stated discipline behind all of them: *"the recurring shape across most anti-patterns:
  **extending the wire format so single attesters can pre-declare their own state more richly**…
  The wire format should **resist** primitives that let a single key announce its own state without
  external composition."*

**Marked out-of-grammar by design** (§1.4, and the spec's named falsification target):
atomic fair exchange / bilateral simultaneity. *"CEG attestations are unilateral, monotonic graph
claims; fair exchange is classically impossible without a trusted third party or a totally-ordered
ledger… CEG does not express it in-grammar — it bridges."* The spec names this as the test to push
on, and states the 1+4 claim would be refuted by a natural in-grammar expression of it.

---

## 7. Honest gaps in what could be extracted

- **No status enum exists in the spec.** The currency-axis state names (live / superseded /
  withdrawn / recanted) are reconstructed from §6.1's precedence, §8's "latest non-superseded"
  predicate, and §10.1.6's forward-only rule. Flagged at §3.0. A later leg should not cite these
  four as spec vocabulary.
- **`supersedes`'s "same attester" is descriptive, not enforced.** §3.2 states it in a table; no
  MUST-reject accompanies it, and §6.1 rule 4 handles cross-attester emissions by parallel-chain
  evaluation instead. Under-specified rather than prohibited.
- **`supersedes`'s postcondition is not uniform.** For the three operational subject_kinds it is
  demoted to audit decoration (§5.6.8.13). Any transition map must carry that exception.
- **`scores` admission preconditions are thin in-spec.** §4 gives required fields and the two
  conditional-required scope fields; whether the `attested_key_id` must pre-exist as a
  `federation_keys` row is not stated as an admission rule — and §1.2 consequence 1 argues the
  opposite direction (*"The attested entity is not prior to its attestations"*), which is
  informative, not normative.
- **`ciris.ai/grammar` was not fetched.** The on-disk RC29 spec is complete, self-consistent, and
  vendored from the named canonical commit; §14.0 records that the RC5 cut specifically *retired*
  the external `ciris.ai/cewp` placeholder citations by defining the terms in-spec. No web fetch
  was needed and none was performed.
- **The home repo is canonical, not this copy.** SOURCES.md: *"The home repo remains canonical —
  re-pull before relying on any document for a decision."* `/home/emoore/CIRISRegistry/FSD/CEG/`
  holds only a README, so the local checkout does not carry the spec; a re-pull of
  `CIRISAI/CIRISRegistry` would be the confirmation step if RC29 is later contested.

---

## SOURCES

All paths absolute. All section references are to the RC29 tree unless marked.

**Primary — CEG 1.0-RC29**, `/home/emoore/CEWP/analysis/tier4-registry-trust/CEG-1.0-RC29-spec/`:

| File | Sections used |
|---|---|
| `README.md` | version header (line 17); RC1–RC29 change log; the "1+4" framing paragraph |
| `00_conformance.md` | §0.2 CCP/CCC/CCS conformance levels (line 42); §0.5 timestamps; §0.6 hex; §0.9/§0.9.2.1 JCS canonical bytes + set-semantics sorting (line 211) |
| `01_foundation.md` | §1.2 Ubuntu commitment, consequences 1–2 (informative); §1.3 operational-language gate; §1.3.1 four-test prefix gate T1–T4; §1.4 the 1+4 minimal-and-adequate claim, the sixteen paths, the named falsification target; §1.5 Recursive Golden Rule |
| `02_grammar.md` | the eight reasoning axes — Polarity, Object, Time, Epistemic mode, Reversibility, Stake, Scope, Inter-attestation relations |
| `03_primitives.md` | **§3.1 `scores` wire shape; §3.2 the four structural composers table; §3.2.1 authority-source via `delegates_to`; §3.2.2 the `recants` distinction; §3.2.3 the four-rule broadened `withdraws` admission + the recants/withdraws composition clause** |
| `04_envelope.md` | §4 full envelope field table; §4.2–§4.2.2.2 `subject_key_ids`, canonical-hash subjects, rule-3 proxy vs `canonical_binding` |
| `05_namespace.md` | §5.6.8.1 `event_listing` sub_kind (line 261); §5.6.8.5 `event:lifecycle:{state}` (lines 397–405); §5.6.8.13 operational-data subject_kinds + stable-id resolution (line 1149); `topical_relation:{kind}` open vocabulary (line 273) |
| `06_relations.md` | **§6 the eight relations, structural vs emergent; §6.1 concurrent-write precedence + idempotence/dedup triple** |
| `08_composition.md` | "latest non-superseded" resolution predicate + tie-break (lines 321, 340, 575, 589, 600); §8.1.8.1 tiered-scope promotion; §8.1.12.7 Self-at-login + partnership-without-agency (lines 481–490) |
| `10_endpoints.md` | §10.1.3 consent revocations not local-tier-eligible (lines 122–131); §10.1.5 attestation tier model + `promote` (lines 139–170); §10.1.6 cross-region merge intents + `withdrawal_forward_only` (line 193) |
| `11_governance.md` | §11.8.2 leaving is forward-only / audit chain preserved (line 228); **§11.10 moderation as a delegable duty — enforced admission (a)/(b), deputization + attenuation, revocable-at-any-link (line 329)**; §11.11 named-moderator existence invariant + merit auto-promotion — *RC29-only* |
| `13_anti_patterns.md` | **§13.1 already-rejected wire additions; §13.2 CEG 0.1 rejections; §13.3 delegation laundering; §13.4 `withdraws` arbitrage; §13.5 the discipline pattern** |
| `14_glossaries.md` | §14.0 core terms (CEG / CEWP / fabric node / `ciris-canonical` / NodeCode); §14.3 envelope-reach table; **§14.4 promotion-via-`supersedes` worked example** |

**Provenance:** `/home/emoore/CEWP/analysis/SOURCES.md` — vendoring manifest; pulled 2026-06-19;
`CIRISRegistry` pinned at `2fb7a2c`, role *"CEG 1.0-RC29 spec + CIRIS Constitution 0.4"*.

**Corroborating copy — CEG 1.0-RC6**, `/home/emoore/CIRISConformance/reference/CEG/`.
Used only to verify version stability: `02_grammar.md`, `03_primitives.md`, `06_relations.md`,
`07_reserved.md`, `13_anti_patterns.md` are byte-identical to the RC29 tree.

**Checked and found not to contain a CEG specification:** `/home/emoore/CIRISCore`,
`/home/emoore/RATCHET`, `/home/emoore/CIRISRegistry/FSD/CEG/` (README only), and the
implementation trees `/home/emoore/CIRISPersist/src/ceg`, `/home/emoore/persist-{664,682,754}/src/ceg`,
`/home/emoore/ciris/ceg`, `/home/emoore/CIRISAgent-wt-wizard/ceg`.
