# AMENDMENT A2 — the reconciliation amendment

**THE FREEZE TARGET IS `scratchpad/RECOGNITION_PREREG.md`.** That file, plus
`scratchpad/RECOGNITION_PREREG_ADDENDUM_A1.md`, plus this amendment, are the registration.
`scratchpad/RECOGNITION_PREREG_R.md` is **SUPERSEDED** and is not part of it.

**Written 2026-08-20, BEFORE FREEZE and before any leg ran.** No Generator2 exists, no mapper
or panel has been invoked, no item has been authored, no locale file in the evidential set has
been opened. This amendment exists because `scratchpad/REFEREE_REPORT.md` (11 BLOCKER ·
16 MAJOR · 11 MINOR) was filed against the drafts before the freeze, and every finding in it is
disposed of below.

**How this document binds.** It **supersedes textually by explicit override line**. Where an
entry below says *OVERRIDE*, the quoted text of [D], [R] or [A1] is replaced by the text given
here, and the superseded text stays in its own file, unedited, so the correction is visible as a
correction. None of [D], [R] or [A1] is modified. This amendment is the diff.

**Source pins, taken at read time** (per the shared-mutable-artifact gate, GATES.md 2026-08-20):

| document | md5 |
|---|---|
| `scratchpad/RECOGNITION_PREREG.md` [D] | `30bfd2cf9754676f7ee351a21e1d3692` |
| `scratchpad/RECOGNITION_PREREG_R.md` [R] | `36591251f93aaa4c03fee00139a629b6` |
| `scratchpad/RECOGNITION_PREREG_ADDENDUM_A1.md` [A1] | `5309c0164167900d73d1b529709c9c5f` |
| `scratchpad/REFEREE_REPORT.md` | `7c9e7242bca58b6d8f47f57fa90decc1` |
| `scratchpad/plane_annotate.py` | `01bb557ed20edba357e1861cb83ac23c` |

---

## §A2.0 Freeze target, document map, and the header lines owed at freeze

### A2.0.1 The map

| tag | file | status |
|---|---|---|
| **[D]** | `scratchpad/RECOGNITION_PREREG.md` | **THE FREEZE TARGET.** The base document. Everything in it stands except where an OVERRIDE below replaces it. |
| **[A1]** | `scratchpad/RECOGNITION_PREREG_ADDENDUM_A1.md` | In force, as amended by §A2.2 (BLOCKER-2, 9, 10) and §A2.4 (MINOR-9, 10, 11-iii). |
| **[A2]** | this file | The reconciliation amendment. Binding on all three. |
| **[R]** | `scratchpad/RECOGNITION_PREREG_R.md` | **SUPERSEDED.** Not part of the registration. Its unique machinery is ported by §A2.1 and only by §A2.1; nothing else in it is in force. It is kept unedited as the record of a second drafting. |

### A2.0.2 The header lines owed at freeze

Per BLOCKER-1's minimal fix, one line goes at the top of each file **at freeze time**. This
amendment does not edit those files; the orchestrator prepends these lines verbatim in the
freeze commit:

- To **[D]**, line 1: `**FREEZE TARGET. Amended by RECOGNITION_PREREG_ADDENDUM_A1.md and RECOGNITION_PREREG_A2.md; read all three.**`
- To **[A1]**, line 1: `**ADDENDUM to RECOGNITION_PREREG.md (the freeze target). Amended by RECOGNITION_PREREG_A2.md.**`
- To **[R]**, line 1: `**SUPERSEDED 2026-08-20. Not part of the registration. The freeze target is RECOGNITION_PREREG.md; this draft's unique machinery is ported by RECOGNITION_PREREG_A2.md §A2.1 and nothing else in this file is in force.**`

### A2.0.3 What this amendment does not do

It does not add a leg, a corpus, or a hypothesis. Every change below is a repair the referee
named, an orchestrator decision on a contradiction between drafts, or a consequence of one of
those two forced by consistency. Where a repair kills a worked example or a downstream
prediction, that death is recorded in **§A2.6** by name, **pre-freeze, by referee** — so that no
later reader mistakes it for a claim that died by data.

---

## §A2.1 Machinery ported from [R]

Four things and only four things are ported. Everything else in [R] is superseded.

### A2.1.1 THE CANDIDATE-SITE RULE — [R] §3, verbatim, with MAJOR-15's scoping sentence added

> Frozen **now**, before T2 and T5 can produce one. Without this, "we found a twelfth" and "we
> absorbed it" are both unfalsifiable, and the leg that finds one is worthless in either
> direction.
>
> A candidate kind `K` may be **named as a candidate twelfth** only if all six hold. Each is
> recorded PASS/FAIL/UNTESTED separately; a candidate failing any one is **absorbed, named, and
> the absorbing kind recorded**.
>
> | # | criterion | test |
> |---|---|---|
> | **C1 — distinct answer** | `K` is a different answer to *"what different kind of wrong happens if I vary this?"* — not a different word for an existing answer | write `K`'s discriminator question in the style of `WrongKind.discriminator`; a blind panel must distinguish `K`-targeted items from the nearest existing kind's items above the chance-corrected floor |
> | **C2 — rename survival** | strip `K`'s home-domain vocabulary and restate; what survives the rename is structure, what dies was the word | the steward's rename-one-side gate (GATES.md). Two independent restatements, both must survive |
> | **C3 — not a modulator** | `K` classifies rather than modulates | the idempotency test, **§A2.1.2** |
> | **C4 — not a composition** | `K` is not the conjunction of two existing kinds, nor a value on an existing axis | exhibit a `K`-change that no pair of existing kinds jointly labels without residue |
> | **C5 — a site, or provably none** | `K` either has a generator site, or is provably not site-generated in the way Record is (`record_not_site_generated`) | mechanized in Lean, or the leg reports UNTESTED and `K` stays a candidate |
> | **C6 — traffic, or a principled absence** | `K` appears in wild change-traffic, or there is a stated structural reason it cannot (as `Model`/`Premises` have) | re-score the existing 279+60 wild corpus for `K` as an available label |
>
> **A candidate twelfth that passes all six is named in the record and the count is reported as
> under challenge. It does not enter `Stance.lean` on the strength of one leg.** The Lean count
> (`basePlane_card = 11`) moves only after a second, independent leg agrees — the same
> two-witness bar the programme applies to everything else.
>
> **And the symmetric rule, so the frame is not one-sided:** a candidate that FAILS and is
> absorbed must have its absorbing kind named in the record, so that a later reader can see
> which absorptions the taxonomy has been made to perform. Ten absorptions into `Manner` would
> be a finding about `Manner`, not a run of clean wins.

**ADDED, per MAJOR-15 (the only edit to the ported text besides C3's cross-reference):**

> **The two-witness bar is PER CANDIDATE SITE: two independent legs must name the SAME site.
> N unrelated candidates are N separate challenges, each owing its own second witness.** Two
> different candidate twelfths arriving from two legs are two challenges, never one
> corroborated finding — the shared-lemma over-grade this programme has committed before.

### A2.1.2 THE IDEMPOTENCY DISCRIMINATOR — [R] §4, with BLOCKER-6's repair inline

**The rule, repaired. This replaces [R] §4's operative clause in its entirety:**

> **A candidate axis is a MODULATOR if STACKING it collapses (idempotent), and a KIND if
> STACKING it produces a distinct reading (non-idempotent).**
>
> **STACKING means iterating the SAME VALUE of the SAME MARKER. Composing two different values
> of one axis is COMPOSITION, and composition is tested by C4, not by C3.**

**The warrant, corrected (MINOR-4).** This is a **stipulated criterion**, not a theorem-backed
one. `Core/Stack.lean`'s `modulate` is `| _ => .strengthMarker` — a literal constant function on
a four-element type — and the file's own docstring says "DEFINITION; its idempotence is then a
theorem about it." The claim that `Stack.lean` grounds "a sharp, domain-independent test" is
**struck**. The test is a convention frozen in advance so it cannot be bent at scoring time,
which is all it needs to be, and all it is now advertised as.

**The evidence rule, ported unchanged from [R] §4 and [R] T5.4:** the test is applied to the
**surveyed evidence**, not to intuition — for T5 the stacking facts come from the typological
source, not from the analyst's ear (GATES.md: *every mechanism needs a new search*).

**The worked examples, re-scored under the repaired rule.**

| example | what it actually is | verdict under the repaired rule |
|---|---|---|
| *"probably probably p"* = *"probably p"* | same-value iteration of one marker | **IDEMPOTENT → modulator.** Survives. This is the certainty prediction, and it is the only one of the three that survives. |
| *"if A, if B, then p"* ≠ *"if A, then p"* | composition of two **different** antecedents | **NOT an idempotency example.** Re-filed as a C4 composition example. Under same-value iteration, *"if A, if A, then p"* ≡ *"if A, then p"* → **IDEMPOTENT**. |
| *"reported that it was inferred that p"* | composition of two **different** evidential values | **NOT an idempotency example.** Re-filed as a C4 composition example. Under same-value iteration, hearsay-of-hearsay is hearsay → **IDEMPOTENT**. |

**THE GAUGE PROBLEM THIS EXPOSES, AND THE CONTROL THAT NOW BLOCKS C3.** Under the repaired
rule, **all three** of the registration's worked examples return MODULATOR. A discriminator that
returns the same verdict on every case it has been exercised on is an instrument reading its own
floor, and the referee's charge — that the rule can be steered to "everything is a modulator" —
is answered by gauging it, not by asserting it is fine:

> **C3-CONTROL, frozen.** Before C3 may be used to absorb any candidate, the leg must supply
> **at least one axis, named in advance and sourced from the typological/standards literature
> rather than from the analyst's ear, on which the repaired test returns NON-IDEMPOTENT.**
> Absent that positive control, a C3 = MODULATOR verdict is **UNGAUGED**, may not absorb a
> candidate, and is reported as ungauged. (GATES.md reach 13: a control that cannot see planted
> dye cannot certify an absence.)

The C3-CONTROL axis must be named in the results document with its source. It is **not** named
here, deliberately: naming it from memory would be the exact failure the evidence rule above
forbids.

**Re-staked predictions, honestly signed.** Both of the predictions that died under the repair
are re-staked here, before freeze, with the sign the repaired test actually gives:

- **P2.4-R (T2, conditionality).** Under repaired C3, conditionality is **IDEMPOTENT** and reads
  **MODULATOR** — the reverse of [R]'s P2.4. Its C4 status is separately live: two different
  antecedents compose into a conjoined antecedent, which is another value of the same axis, so
  conditionality is predicted to **fail C4** as well. The landing prediction — [D] §T2.4's
  **P2.7, conditionality → Premises** — is **unchanged and stands on its own**; it never rested
  on the idempotency test and does not now.
- **P5.2-R (T5, source-of-knowing).** Under repaired C3, source-of-knowing is **IDEMPOTENT** and
  reads **MODULATOR** — the reverse of [R]'s P5.2. This is a **prediction reversal produced by
  the referee, recorded as one**, and it is stated before any typological source has been
  consulted for the stacking facts, which per the evidence rule are what actually decide it.

**Consequence for E2, pinned so it cannot be resolved after the fact.** [D] §T5.6's **E2** (a
SOURCE modulator distinct from strength, named as a candidate twelfth) now runs into C3: a
candidate that reads MODULATOR fails C3 and is **absorbed, with the absorbing kind named**. So:

> **If T5 returns E2 (unanimous landing on a single site outside the eleven) AND the repaired C3
> returns IDEMPOTENT on source-of-knowing from the source's own stacking facts, the two readings
> CONFLICT. That conflict is pre-staked as its own outcome — `E2-CONFLICT` — and it carries NO
> VERDICT in either direction.** The candidate is recorded as named-but-not-cashed, the C3
> result is recorded beside it, and a successor design is owed. Neither reading may be preferred
> at scoring time.

### A2.1.3 THE BLIND-DERIVER PROTOCOL FOR T1 — [R] §6.6 and §6.4, ported, repaired, and made SYMMETRIC

This is where T1's evidential content now lives (BLOCKER-3, BLOCKER-5). It replaces [R] §6.6 and
supersedes [D] §T1.6's mitigation (iii).

**T1-BLIND, frozen.** One pass, **three mode sets**, run before any image is read.

1. **Three derivers**, independent agents, **no repository access**, no part in authoring this
   registration or [D], [A1] or [R].
2. Each deriver receives **all three mode sets**, in an order randomized per deriver, each
   presented with its literature attribution, **none flagged as the target**:
   - the **recognition triple** (`stateRec` / `transitionRec` / `constitution`), attributed to
     Katsuno–Mendelzon 1991, Millikan 1995, Searle;
   - **Jakobson's six functions** (1960);
   - **Habermas's three validity claims** (1981).
3. Each deriver receives **R1–R4 verbatim from [D] §T1.3** and each mode set's stated
   satisfaction conditions, **and nothing else**. They are **not** told a count, **not** told a
   target exists, **not** told which set is the programme's own, and **not** given our kind
   names, `basePlane_card`, the number eleven, or any mention of this registration.
4. **MINOR-2's strip, mandatory:** the deriver-facing copy carries **no active-inference factor
   names** (`A`, `B`, `C`, `D`, `π`, `γ`). The literature names ("active inference", "Friston")
   may appear; the factor letters, whose count and roles are the answer, may not.
5. Each deriver writes, per mode, the **R2 gap arguments from that mode's own satisfaction
   conditions**, then enumerates the sites and names each in plain English, then computes the
   total. **Nine derivations** result (3 derivers × 3 mode sets).

**Scoring (MINOR-3), frozen.** A **third-party scorer** — an agent with no repository access and
no part in authoring — scores each derivation against the **eleven routing examples** below.
A derived site *matches* a routing example iff the scorer would route that example change to it.
The scorer knows the rubric has eleven entries; that is unavoidable and harmless, since the
scorer performs no derivation. Scoring is on **structure** (which primitive carries how many
depths, and what each depth is for), never on wording.

**THE ELEVEN ROUTING EXAMPLES — frozen here, in neutral vocabulary, no kind names:**

| # | example change | the [D] §T1.2 site it routes to |
|---|---|---|
| 1 | a report's stated measurement is changed from 4.2 to 4.9 | `stateContent` |
| 2 | "we conclude" becomes "we tentatively conclude"; the measurement is unchanged | `stateStrength` |
| 3 | the formula converting the sensor reading into the reported value is changed; the reading is unchanged | `stateRule` |
| 4 | the standing assumption the report rests on ("readings are taken at sea level") is changed | `stateGiven` |
| 5 | "operators may restart the process" becomes "operators must restart the process" | `transitionContent` |
| 6 | a policy's ranking of its goals is changed so that safety outranks throughput | `outcomeOrder` |
| 7 | two steps of a documented procedure are swapped | `stepOrder` |
| 8 | a document declares that a component previously called a draft now counts as ratified | `constitutedStatus` |
| 9 | the same table is moved from CSV to JSON; contents identical | `carrierEncoding` |
| 10 | a passage is rewritten from passive to active voice; content identical | `carrierPresentation` |
| 11 | the file recording the change is moved to a different directory; contents identical | `carrierToken` |

**THE SYMMETRY, which is BLOCKER-5's whole point.** Under this protocol the recognition triple
and the two placebos are put through **the same recipe, by the same agents, under the same
blindness, in the same pass**. Neither placebo's R2 gap count is any longer an authoring choice
made by someone who knows that "not eleven" is the wanted answer, and neither is Generator2's.

**OVERRIDE of [D] §T1.6 mitigation (iii).** [D] reads: *"an independent author is invited — the
steward or an unrelated agent **may** add a third placebo mode set at any time."* That invitation
is **replaced by a mandate**:

> The two placebos' R2 gap arguments **must** be authored by an agent with no repository access,
> not told the target count, and given only R1–R4 plus the mode set. Without them the placebo
> leg is **UNGAUGED** and, per **T1-VOID-3**, the primary is **uncashable**.

An additional third placebo mode set from the steward remains welcome and still counts equally;
it is now an addition to a blocking control rather than a substitute for one.

**T1-VOID-3, extended.** The leg is UNGAUGED — and the primary uncashable — if **any** of: a
placebo is authored after Generator2's image is known; a deriver has repository access; a
deriver is told the count, the roster, or which set is ours; the deriver-facing copy carries the
active-inference factor letters; fewer than **2 of 3** derivations are usable for any mode set;
or the scorer is not third-party.

**The placebo verdicts, restated on the blind pass.** [D] §T1.6's three-row table is unchanged in
meaning and re-anchored to the blind derivations:

| verdict | condition, on the blind pass |
|---|---|
| **DISCRIMINATING** | the recognition set's modal blind derivation reproduces the eleven-site structure and **neither** placebo's does |
| **RECIPE-DRIVEN** | **both** placebo sets' modal blind derivations also reproduce the eleven-site structure → candidate **WARRANT FAILURE** on `kinds-from-sites`, escalated at full volume, exactly as [D] §T1.6 states |
| **MIXED** | exactly one placebo set reproduces it → [D] §T1.6's downgrade applies verbatim |
| **UNGAUGED** | T1-VOID-3 fires |

[D] §T1.6's staked forward predictions **PP1** (Jakobson's image is not eleven) and **PP2**
(Habermas's image contains no Identity member) stand, and are now scored on the **blind**
derivations: PP2 obtains iff no blind Habermas derivation produces a site the scorer routes to
routing example 8.

**[R] §6.4's discount, ported verbatim into [D] §T1.0** (see BLOCKER-3):

> **THE DISCOUNT, STATED BEFORE THE RUN.** The author of this registration has already read
> `Generator.lean`. T1 therefore **cannot** be a blind test of "does a recognition grounding give
> eleven" — the target was known when the axes were written. A hit is **weak** support and will be
> reported as weak.

### A2.1.4 THE NO-ADAPTIVITY RULE — [R] G15, ported

> **No leg's design may change after seeing an earlier leg's result**, except by a numbered
> amendment written **before** the next leg runs.

Ported because the execution order in §A2.5 depends on it: putting the most dangerous leg last
is only insulation if nothing earlier may reach forward and rewrite it. The one clause in [D]
that violated it is deleted by **MAJOR-16**.

### A2.1.5 What is NOT ported from [R], stated so the omissions are visible

- **The five-blind-matcher / chimera-foil machinery** ([R] §5, §7.3, G9–G10). [D]'s three-mapper
  instrument is the frozen instrument, and MAJOR-3 states its thresholds as counts.
- **[R]'s five-primitive axis set, depth rule and hand-tuning ledger** ([R] §6.2–§6.5). [D]
  §T1.2's eleven-row frozen table and T1-VOID-1 are the freeze.
- **[R]'s three decoy generators** ([R] §6.7). [D]'s two placebo mode sets serve the same
  anti-tautology function. **Flagged for the orchestrator's review:** the decoy control is a
  *different* dye test (altered axis set rather than altered mode set) and would gauge whether
  the construction can fail at all. It is **not adopted here** because it is a design addition
  beyond the referee's findings, and adopting it silently would be the drift this amendment
  exists to prevent. It is a live recommendation, not a change.
- **[R]'s G1–G14 defaults**, its outcome tables, its kill statements, and its §14 combination
  matrix. [D]'s bands govern. The one §14 row the referee named is corrected in MAJOR-15.

---

## §A2.2 BLOCKER resolutions

### BLOCKER-1 — freeze target ambiguous; A1 cites a section that exists nowhere

> *Minimal fix.* "Name one file as the freeze target in one line at the top of both documents;
> replace '§0.5-style candidate-site machinery' with the literal rule it means ('the CANDIDATE
> SITE band of §T5.9'); mark the non-frozen draft **SUPERSEDED** in its first line, in the same
> commit as the freeze."

**FIXED.** The freeze target is named in this amendment's first line and in §A2.0.1; the three
header lines owed at freeze are given verbatim in §A2.0.2 for the orchestrator to prepend.

**OVERRIDE of [A1] §A1.1.7, CASE—distinct row.** The clause *"it does not trigger §0.5-style
candidate-site machinery on its own"* is replaced by:

> it does **not** trigger **the CANDIDATE SITE band of [D] §T5.9**, and by [A1]'s own
> subordination rule (§A1.1.0) it cannot: T5-I2 may not enter `F`, `R`, the 13-category
> denominator, the stage-2 recurrence criterion, or the ≈20% power bound.

### BLOCKER-2 — A1 moves a VOID threshold while declaring itself additive, and misattributes it

> *Minimal fix.* "Either write 'κ < 0.6, which is *stricter* than the delivered draft's 0.4 and
> applies to this instrument only', or change to 0.4. Do not leave two floors with one of them
> attributed to the wrong source."

**FIXED, as an explicit numbered change** (orchestrator decision 6: never silently).

> **CHANGE-A2-1.** [A1] §A1.2.4's fresh-annotation floor is **κ < 0.6**, which is **stricter
> than [D]'s 0.4** and **applies to the T5-I3 fresh-annotation instrument only**. [A1]'s
> attribution *"per the delivered draft's floor"* is **STRUCK as a misattribution**; the floor's
> source is `PLANE_PREREG.md` §5 (met at 0.687), not [D].

**Rationale for adopting 0.6 rather than restoring 0.4 here.** They gauge different tasks.
[D]'s 0.4 gauges a **cross-taxonomy mapping** across twelve labels between two differently-typed
taxonomies ([D] §T2.2's type mismatch is real and is a repair, not a dissolution) — a harder task
with a lower defensible floor. 0.6 is the house floor for **same-taxonomy annotation on clear
items**, and T5-I3's fresh annotation *is* that task on a new corpus; its nearest measured
comparator, the RATCHET κ study on this exact protocol, returned **0.831**. A 0.4 floor on a task
whose comparators run 0.687–0.831 would be no floor at all.

**Which κ floor applies where — the table the referee asked for, frozen:**

| instrument | floor | source | status |
|---|---|---|---|
| T2 mapper agreement ([D] §T2.5 VOID) | **κ < 0.4** | [D] | unchanged |
| T5-I1 mapper agreement ([D] §T5.9 VOID — agreement) | **κ < 0.4** | [D] | unchanged |
| T5-I3 fresh annotation ([A1] §A1.2.4) | **κ < 0.6** | `PLANE_PREREG.md` §5 | **CHANGE-A2-1** |

**And the honest correction to [A1]'s opening claim:** [A1] states it *"alters no band, no kill,
no VOID condition."* That was **not true** of §A1.2.4, and is now not true of §A1.2.5 or
§A1.2.6(b) either (BLOCKER-9, BLOCKER-10). The sentence is **struck**; [A1] is additive except
where §A2.2 says otherwise, and the exceptions are numbered.

### BLOCKER-3 — T1's five stakes are entailed by T1's own freeze; the outcome table lists outcomes the freeze forbids

> *Minimal fix.* "Import the rival draft's §6.4 discount verbatim: add to §T1.0 — 'Because §T1.2
> freezes the site list *and* the kind map, §T1.4's stakes are a consistency check on the freeze,
> not a result. T1's evidential content is exactly (i) the §T1.6 placebo comparison and (ii) an
> independent reader's verdict on the R2 arguments.' Then delete the three unreachable rows from
> §T1.5 or re-label them 'outcomes reachable only under the re-registration of T1-VOID-1'."

**FIXED,** both halves, plus the relocation the orchestrator directed.

**OVERRIDE — added to [D] §T1.0:**

> **§T1.4 IS THE FREEZE-CONSISTENCY CHECK, NOT THE DISCOVERY.** Because §T1.2 freezes the site
> list **and** the kind map, §T1.4's five stakes — completeness, image, injectivity, Record
> excluded, transport — are immediate arithmetic consequences of the frozen table and cannot fail
> except by transcription error. They are run and reported as a **consistency check on the
> freeze**. They are **not** T1's result and may not be quoted as one.
>
> **T1's evidential content is exactly two things:** (i) the **placebo differential** of §T1.6, as
> re-anchored to the blind pass by **A2 §A2.1.3**; and (ii) the **third-party scorer's verdict on
> the blind R2 derivations**, also §A2.1.3. Nothing else in T1 is evidence.
>
> Plus [R] §6.4's discount, verbatim: *the author of this registration has already read
> `Generator.lean`; T1 cannot be a blind test of "does a recognition grounding give eleven"; a hit
> is weak support and will be reported as weak.*

**OVERRIDE — [D] §T1.5's three rows are RE-LABELLED, not deleted.** Re-labelling is the more
honest of the two options the referee offers: it keeps visible that these outcomes were
contemplated and why they are unreachable.

| row | new label |
|---|---|
| DIFFERENT IMAGE — count ≠ 11 | **reachable only under the re-registration required by T1-VOID-1.** Its reading is unchanged and applies to the re-registered leg. |
| DIFFERENT IMAGE — same count, different kinds | as above |
| RECORD BECOMES SITE-GENERATED | as above |

### BLOCKER-4 — F1, the failure mode given "real probability", cannot be reported as a result

> *Minimal fix.* "One sentence in T1-VOID-1: 'An addition arising from an R2 derivation written
> and dated **before** the image is computed is an **F1 result**, not a VOID; only an addition
> made after the image is read voids the leg.'"

**RESOLVED, BY THE OPPOSITE ROUTE, ON THE ORCHESTRATOR'S DECISION 4 — and that divergence is
flagged here rather than buried.** The referee's fix would make F1 live by carving an exception
into T1-VOID-1. The orchestrator ruled instead that **T1-VOID-1 stands unamended**: a twelfth
constructor voids the leg, so **F1 is reachable only through re-registration**.

**OVERRIDE of [D] §T1.5's F1 row:**

> **F1 — the transition-strength site (count 12).** If R2 forces a `transitionStrength` site, the
> compiled `RSite` differs from §T1.2's frozen table by an addition, and **T1-VOID-1 fires: the
> leg is VOID and must be re-registered.** F1 is therefore **not a live escalation outcome of
> this registration.** It is recorded as **VOID — count 12**, the derivation that produced it is
> published in full, and the escalation to the steward under the standing bounty happens **in the
> re-registration**, where the twelve-site model can be staked in advance instead of discovered.
> The reconciliation owed to `CONJUGATION_TEST_RESULTS.md`'s 12/12 Rules verdict — which tested
> **deontic** strength and does **not** settle transition-*likelihood* strength — is owed in that
> re-registration as its own test, exactly as [D] says, and is not asserted here.

**Why the stricter route was taken, stated so it can be argued with.** The referee's exception
turns on "written and dated before the image is computed", certified by the steward. A date on a
file in a shared worktree is a timestamp, not a pin — `epistemology.md` §4 says so in terms, and
this repository logged a shared-mutable-artifact provenance violation **on 2026-08-20, the same
day** (GATES.md tail). The stricter route needs no certification of a thing the machine cannot
check. **The cost is real and is stated:** F1 was the outcome [D] §7 doubt 1 put "real
probability" on, and this route means the registration cannot cash it. It converts the
registration's most likely interesting T1 outcome into a VOID plus a re-registration.

**Consequent deletions, forced by this resolution:**

- **[D] §T5.11's exception dies** — see MAJOR-16. It was conditional on F1 producing a live
  twelve-site model, which it no longer can.
- **[D] §7 doubt 1's second half** — *"F1 (transition-strength → 12) is the reason to think it
  might not, and I would put real probability on it"* — stands as a **doubt**, but its
  implication that F1 is a reportable outcome of this leg is **struck**. The doubt is now: *T1
  may be a rename, and if the R2 derivations force a twelfth site the leg VOIDs rather than
  reports.*

### BLOCKER-5 — the anti-tautology control applies the recipe asymmetrically; its only real mitigation is optional

> *Minimal fix.* "Promote (iii) to blocking: 'the two placebos' R2 gap arguments must be authored
> by an agent with no repository access, not told the target count, and given only R1–R4 plus the
> mode set. Without them the placebo leg is **UNGAUGED** and, per T1-VOID-3, the primary is
> uncashable.'"

**FIXED, and made symmetric per orchestrator decision 4.** The full protocol is **§A2.1.3**. The
mandate is adopted verbatim; the symmetry goes further than the referee asked, because the
asymmetry the referee identified is not fixed by constraining only the placebos: Generator2's R2
was frozen in advance by an author who knew the target too. So the **same** blind pass produces
the R2 gap arguments for **all three** mode sets, none flagged as the target, and §T1.2's frozen
table is retained **only** as the anti-rigging freeze (you may not change the table after seeing
the image) with **no evidential weight of its own**.

### BLOCKER-6 — the idempotency discriminator conflates iteration with composition

> *Minimal fix.* "Replace the rule's operative clause with: '**stacking** means iterating the
> **same value of the same marker**; composing two different values of one axis is *composition*,
> tested by C4, not by C3.' Then re-stake the conditionality and source-of-knowing predictions
> **before** freeze."

**FIXED.** The repaired rule, the corrected warrant, the re-scored worked examples, the
**C3-CONTROL** that now blocks C3 from absorbing anything until a non-idempotent axis is
supplied from a source, and the two re-staked predictions (**P2.4-R**, **P5.2-R**, both signed
opposite to [R]'s) are all in **§A2.1.2**. The `E2-CONFLICT` outcome is pre-staked there so the
collision between a C3 = MODULATOR reading and an E2 candidate cannot be resolved after the fact.
Items that died are listed in §A2.6.

### BLOCKER-7 — T5's E1 is defined by the frozen statistics to read INDETERMINATE, and the frame does not code the values it ranges over

> *Minimal fix.* "For category 1 only: one minimal pair **per evidential value per language**
> (≈4–6 × 3), recount the judgment total and the cost line; add to §T5.6 — 'E1 obtains iff the
> per-value determinate landings are a subset of {Confidence, Model, Premises} using at least two
> of the three; dispersion across those three is E1, not indeterminacy'; and mark row 1's frame
> 'WALS 77/78 for presence, **Aikhenvald 2004 for values (secondary frame)**'."

**FIXED, all three parts.**

**OVERRIDE of [D] §T5.4, for category 1 only:** category 1 (Evidentiality) yields **one minimal
pair per evidential value that the language obligatorily marks**, not one pair per language. The
value inventory per language is taken from **Aikhenvald 2004** and **verified against her survey
before freeze**; the provisional counts — Tuyuca 5, Cuzco Quechua 3, Turkish 2, **10 pairs** —
are **NOT DATA** (received-numbers gate) and the source wins on conflict.

**OVERRIDE of [D] §T5.5's category-level determinacy rule, for category 1 only:** determinacy is
judged **per value** (unanimous across the three mappers and stable across both gloss
conventions), not by "≥2 of 3 language instances agree".

**OVERRIDE — added to [D] §T5.6:**

> **E1 obtains iff the per-value determinate landings are a subset of {Confidence, Model,
> Premises} using at least two of the three.** Dispersion across those three is **E1, not
> indeterminacy.** A per-value landing outside that set, or a value with no determinate landing,
> is scored separately and named. The §T5.6 caveat about mappers disagreeing *within* one item
> stands unchanged and is a different thing from dispersion *across* values.

**OVERRIDE of [D] §T5.3 row 1's frame column:** *"WALS **77/78 for presence** (a three-way
presence/type contrast: no grammatical evidentials / only indirect / both direct and indirect);
**Aikhenvald 2004 for the values — SECONDARY FRAME**, weaker independence guarantee, disclosed
per [D] §T5.2."* Row 1 therefore joins the four categories [D] §7 doubt 12 already flags as
weaker-independence, and doubt 12's count changes from four to **five of the most dangerous
prongs**.

**Recount:** +7 minimal pairs → **+42 judgments**. The full recount is in §A2.5.

### BLOCKER-8 — three T5 rows pre-register NO-FIT as a *confirmed prediction*

> *Minimal fix.* "One predicted landing per row; move every alternative into a separate
> 'alternative landing' column pre-declared to score as a **MISS**; and add one line to §T5.3:
> 'a NO-FIT on any row, including rows 4, 8 and 12, enters `R` and routes through §T5.9's
> CANDIDATE SITE band. §T5.8's defence applies only after the reason fields are read, and only to
> row 8.'"

**FIXED.** Every disjunctive prediction in [D] §T5.3 is split into one **predicted landing** and
one **alternative landing**, and **an alternative landing scores as a MISS**.

The six disjunctions the referee counted are rows **2, 4, 7, 9, 12, 14**; row **8** is the third
NO-FIT-as-prediction row and is treated with them. Where a disjunction's prongs were simply
listed, the **first-named prong is the predicted landing** — the non-arbitrary choice, and the one
that does not let this amendment re-stake the leg in a preferred direction.

| row | category | **predicted landing** (scores HIT) | **alternative landing** (scores MISS) |
|---|---|---|---|
| 4 | Middle voice | **Manner** | NO-FIT |
| 7 | Numeral classifiers | **Identity** | Structure |
| 8 | Egophoricity | **NO-FIT on the *who* axis** | any determinate landing inside the eleven |
| 9 | Switch-reference | **Structure** | Process |
| 12 | Mirativity | **Confidence** | NO-FIT |
| 14 | Definiteness/givenness | **Facts** | Premises |

**Row 2 is handled differently, and deliberately.** Its disjunction is not a prediction protecting
itself — it is a **registered disagreement between two named parties**, which [D] §T5.7 states in
advance with "whichever the blind mappers give, stands". Collapsing it to one landing would
silently pick a winner. Instead both prongs are scored as **rival pre-registered predictions**:

| row | rival A (the brief) | rival B ([D] §T5.7's registered dissent) |
|---|---|---|
| 2 | the **KM state/transition split** — Rules, or Model | **Facts** |

Exactly one of the two is recorded as **wrong** whichever way the row lands, which is the property
BLOCKER-8 exists to restore. The row contributes to `F` either way; a NO-FIT on it enters `R` like
any other.

Rows 1, 3, 5, 6, 10, 11, 13 already carried a single landing or an explicit distribution
(row 1's E1 distribution is governed by BLOCKER-7) and are unchanged.

**OVERRIDE — added to [D] §T5.3:**

> **A NO-FIT on any row — including rows 4, 8 and 12 — enters `R` and routes through §T5.9's
> CANDIDATE SITE band.** §T5.8's *who*-defence applies **only after the reason fields are read**,
> and **only to row 8**. No row's NO-FIT is exempt from `R` by prediction.

**Note on row 8, kept because it is the one place the design was right and the referee's fix
narrows it.** [D] §T5.8 registers the *who*-defence in advance precisely so it cannot be produced
afterwards, and explicitly refuses to extend it to evidentiality. That refusal stands. What is
struck is only "pre-registered as NOT adverse" doing the work of exempting row 8's NO-FIT from
`R`. It enters `R`; §T5.8 then applies to it and to nothing else; and MAJOR-10's new
**EXPECTED NO-FIT — warrant axis** band is where it lands.

### BLOCKER-9 — A1's REFUTED band cannot fire on the cleanest possible disconfirmation

> *Minimal fix.* "Drop the second conjunct: **REFUTED := the three predicted pairs take ≤10%.**
> Naming the top rival triple becomes a *reporting* requirement, not a band condition. Restate
> INDETERMINATE as 'anything not covered above'."

**FIXED, verbatim. OVERRIDE of [A1] §A1.2.5's band table and [A1] §A1.5's A1.h:**

| band | condition | reading |
|---|---|---|
| **CONCENTRATION HELD** | the three predicted pairs take **≥25%** of mixed-block pairs, p<0.01 against the null of MINOR-10 | the confusion geometry measured on the PLANE corpus reproduces on an unrelated, CI-governed corpus |
| **CONCENTRATION REFUTED** | the three predicted pairs take **≤10%** | the concentration reading is **refuted on this corpus** |
| **INDETERMINATE** | anything not covered above | no verdict |
| **VOID** | fresh-annotation κ < 0.6 (CHANGE-A2-1), or **<40** blocks in the mixed frame | ungauged |

**Reporting requirement, unconditional:** the **top rival triple is NAMED in the result section
whatever the band**, together with its share. It is no longer a condition on any band. The chance
baseline is defined per MINOR-9.

### BLOCKER-10 — A1's seen/unseen rule removes the only pre-staked contrary evidence and pre-commits that it loses

> *Minimal fix.* "Keep the exclusion; change the tie-break to: '**Neither governs.** A
> disagreement between the SEEN stratum and the primary is reported as an unresolved split, and
> the primary may not be quoted in any sentence that does not also carry the SEEN stratum's
> result.' Add one sentence to §A1.2.6(b): 'the exclusion removes items whose observed pattern is
> contrary to the prediction; the primary is therefore not a fair test *against that pattern*,
> only against a fresh one.'"

**FIXED,** with the pre-staked reconciliation rule orchestrator decision 5 requires.

**OVERRIDE of [A1] §A1.2.6(b)'s pre-commitment and [A1] §A1.5's A1.i.** The clause *"if the SEEN
stratum and the primary disagree, the primary governs"* is **STRUCK**. In its place:

> **THE RECONCILIATION RULE, pre-staked.**
> 1. The exclusion of the 30 `language_guidance` parts from the primary **stands** — the primary
>    must be blind, and this author has seen those items' disagreement structure.
> 2. **The SEEN stratum is annotated and reported alongside the primary, in the same table,
>    always.**
> 3. **If they AGREE:** the agreement is the result. The SEEN stratum adds **no independent
>    weight**, and the sentence saying so travels with it, because it is not blind.
> 4. **If they DISAGREE: NEITHER GOVERNS.** The result is an **UNRESOLVED SPLIT**. The primary
>    **may not be quoted in any sentence that does not also carry the SEEN stratum's result.** No
>    concentration verdict is available from this instrument, and a successor — a fresh corpus
>    with an author who has not seen its disagreement structure — is owed and named as owed.
> 5. **Regardless of outcome**, the result section carries §A1.2.6's n = 4 table verbatim and the
>    sentence *"zero of four sit on any of the three predicted boundaries, and not one touches
>    Facts, Manner or Model."*

**OVERRIDE — added to [A1] §A1.2.6(b):**

> The exclusion removes items whose **observed pattern is contrary to the prediction**; the
> primary is therefore **not a fair test against that pattern**, only against a fresh one.

**ADDED — the overlap pre-flight the referee names in his answer 5, which the numbered findings
do not carry:**

> **OVERLAP-CHECK, blocking.** Before the primary is computed, measure and write to disk **how
> many of the 30 seen `language_guidance` parts lie inside the mixed frame the primary is
> computed over.** If the overlap is **zero**, the exclusion is a **no-op** and must be reported
> as one — the primary was never at risk from those items, and the blindness argument for
> excluding them buys nothing. The number is reported either way.

### BLOCKER-11 — the one commitment advertised as mechanically enforced is not enforced by the named mechanism

> *Minimal fix.* "Either (a) set `HARD_CAP_USD` to the leg's cap before each run and record the
> value set in the results file … or (b) restate §5 as 'caps are human-upheld; the module's
> global `HARD_CAP_USD = 10.0` is a backstop, not the enforcement.' (b) is honest and free."

**FIXED — both (a) and (b), and no mechanical-enforcement claim is made** (orchestrator
decision 3).

**Verified at the primary, this pass:** `scratchpad/plane_annotate.py:18` is
`HARD_CAP_USD = 10.0` — a **single global** ceiling, **not per leg**, checked once per call
against cumulative in-run spend (line 147) and on breach it **prints and returns**
(`state["capped"] = True`, "HARD CAP: … stopping"). There is no per-leg notion and **no VOID
semantics anywhere in the module**.

**OVERRIDE of [D] §5's cap sentence.** *"Caps are enforced in-process by
`plane_annotate.HARD_CAP_USD`, per leg, and a cap event voids the leg"* is replaced by:

> **Spend caps are HUMAN-UPHELD.** No CI gate and no module enforces them; in `Gate.mechanized`
> terms this commitment is **false**, and `epistemology.md` §4 and `CLAUDE.md` both forbid
> advertising it otherwise. `plane_annotate.HARD_CAP_USD` is a **single global backstop at
> $10.00** that stops a runaway loop; it has no per-leg notion and no VOID semantics, and it sits
> **above** this registration's entire global cap, so it will never fire first.
>
> **Two human acts stand in its place, both leaving a file on disk:**
>
> **(1) PREFLIGHT, before the leg's first API call.** Write
> `scratchpad/recognition_spend/<leg>_preflight.json` containing: the leg's cap from §A2.5; the
> **cumulative spend across all prior legs**, read from their result files, not from memory; the
> projected judgment count and the projected spend; and **the value `HARD_CAP_USD` was set to for
> this run**, which is the leg's own cap. **A leg run without its preflight file already on disk
> is VOID on spend discipline**, and that VOID is reported like any other.
>
> **(2) POSTFLIGHT.** Append actual spend, actual judgment count, and whether the module's cap
> fired. Reported against cap in every results section, as [D] already requires.
>
> **A cap breach VOIDs the leg rather than truncating it** — that part of [D] §5 stands, and it
> is a human commitment, upheld by a human reading the postflight file.

---

## §A2.3 MAJOR resolutions

**All 16 FIXED. Zero ACCEPT-WITH-REASONS entries** (decision 7 permits up to three and prefers
fixes).

### MAJOR-1 — the two documents pin contradictory execution orders

> *Fix:* "pick one in the frozen file and delete the other's rationale paragraph."

**FIXED. ORCHESTRATOR'S DECISION 2, and it picks neither draft's order:** **T1 → T2 → T3+T4 →
T5**, with the rationale in §A2.5. **Both** superseded rationales are struck: [D] §5's "T5 second
*because* it is most likely to break the eleven" and [R] §15's "T5 last *because* the
adjudication rule should be exercised twice first". The full ordered table is §A2.5.

**One consequence to carry:** [D] §5 row 3 says T2 *"shares T5's mapping instrument, so it runs
on the same tooling."* Under the new order the dependency reverses — **T5-I1 shares T2's mapping
instrument**, and T2 is where the three-mapper schema (including MAJOR-4's new field and
MAJOR-3's count thresholds) is first exercised. [D] §T5.11's ordering dependence on T1 is
unaffected: T5 still runs after T1.

### MAJOR-2 — the spend regimes differ tenfold; A1 adds instruments with no cost line

> *Fix:* "give each A1 instrument its own cap outside T5-I1's $0.15, or state that A1 instruments
> run only after T5-I1's cap is discharged."

**FIXED.** §A2.5 is a **single spend table** with **one global cap of $6.00** (decision 3) and a
line for **every** instrument including every A1 one: T5-I2 ($0.00, VOID-EXPECTED), T5-I3, the A0
screen, and the T3 alternative corpora. Per-leg lines sum to **$2.75**; the **$3.25** difference
is an **unallocated reserve that may not be spent without a numbered amendment**, so the per-leg
lines are the operative caps rather than decoration.

### MAJOR-3 — the mapping instruments differ in size and rule; ≥50% on 3 judges is near-degenerate

> *Fix:* "state the thresholds as counts (3/3 = home; 2/3 = weak home, reported separately;
> 1/1/1 = SPLIT) … and say whether a mapper's *second* choice counts toward any of them. **It
> currently does not say, and that is a scoring-time freedom.**"

**FIXED.** [D]'s **three**-mapper instrument is kept; [R]'s five-matcher/≥50% machinery is not
ported (§A2.1.5).

**OVERRIDE of [D] §T2.3 and §T5.5's decision rule, stated as counts:**

| result | count | scores as |
|---|---|---|
| **HOME / DETERMINATE** | **3/3** mappers agree on one of the twelve kinds, **or** 3/3 say NO-FIT | determinate; counts toward `D` (T2) and `F`/`R` (T5) |
| **WEAK HOME** | **2/3** | **reported separately by name; counts toward NOTHING** — not `D`, not `F`, not `R`, not any band |
| **SPLIT** | **1/1/1** | reported with the three labels |

**And the freedom the referee found, closed:** a mapper's `second` field **counts toward no
threshold, no band and no determinacy judgment.** It is reported as a secondary distribution and
may be used **descriptively only**. This is frozen now rather than decided at scoring time.

### MAJOR-4 — the RECORD-ANALOGUE band is triggered by a judgment the instrument never elicits

> *Fix:* "add one frozen field to the mapper schema: 'Does deciding this require knowing what
> survives outside the artifact being classified? yes/no' and define the band on unanimity of
> that field."

**FIXED, verbatim.** The mapper output schema — frozen now, for T2 and T5-I1 alike — is: **kind ·
optional second · one-sentence reason · SURVIVES-OUTSIDE (yes/no)**, with the field worded
exactly:

> *"Does deciding this require knowing what survives OUTSIDE the artifact being classified?
> yes/no."*

**OVERRIDE of [D] §T2.5's ADVERSE — RECORD-ANALOGUE row:** the band fires iff **all three mappers
answer YES** on that field for an ISO dimension, qualifier or structural device. [D]'s pre-stated
adjudication criterion is unchanged in content — it is now **asked** rather than applied by the
author to free text, which is what [D] §T2.5 said it wanted and did not have. [D]'s stated prior
(ISO's dependence and rhetorical relations relate two acts both inside the annotated dialogue, so
on their face they are not Record-type) stands as a prior and is not the verdict.

### MAJOR-5 — T2's bands do not partition

> *Fix:* "extend PARTIAL to '…or D ≥ 6 with P2.1 **or** P2.2 failing', and add one line: 'the two
> ADVERSE rows are overlays; they fire independently of the D band and are reported alongside
> it.'"

**FIXED, verbatim. OVERRIDE of [D] §T2.5:** PARTIAL reads *"`D` in 3–5, **or** `D ≥ 6` with P2.1
**or** P2.2 failing."* And: *"the two **ADVERSE** rows are **overlays**: they fire independently of
the D band and are reported alongside it, never instead of it."*

### MAJOR-6 — T3's control gate is a decision point with no power statement

> *Fix:* "state the gate's own power numerically, or move 9 items from arms A/B into arm D
> (24 + 24) at no authoring cost."

**FIXED — by authoring, not by moving, plus the power statement, plus a band split.** Moving 9
items out of each of A and B would drop the primary arms to 21 and gut the power [D] §T3.4
registered at N = 30. Arm **D is raised to 24 + 24 by authoring 18 new items**; arms A and B stay
at 30 each. Authoring cost is real and is stated in §A2.5's authoring line.

**OVERRIDE of [D] §T3.5 gate 1**, which currently conflates two different failures:

| band | condition | reading |
|---|---|---|
| **VOID — instrument cannot resolve** | `R < 0.30` | the instrument cannot resolve a *known* kind boundary on this corpus at a usable effect size. No verdict on A vs B. |
| **GATE-UNDERPOWERED** | `R ≥ 0.30` **but** the control fails to separate at `p < 0.01` | the boundary is there at a usable size and the **gate** could not certify it. **No verdict on A vs B**, and this is explicitly **not** the instrument-cannot-resolve finding. |

**Registered power statement for the gate itself, which [D] did not carry.** At 24 vs 24 a
two-proportion test at `p < 0.01` two-sided reaches 80% power at a Model-modal rate difference of
**≈45 percentage points**, and ≈35 pp at roughly 55% power. At [D]'s original 15 vs 15 the 80%
figure was **≈57 pp**. Both numbers are stated so the gate's failures can be read for what they
are. This is GATES.md reach 13 ("power of the control itself") applied to our own control.

### MAJOR-7 — T3's decision threshold rides on an unbounded estimate of R

> *Fix:* "use the **lower** 95% bound on R for the SUBSTRUCTURE threshold and the **upper** bound
> for the ONE KIND threshold, and say so in the band table."

**FIXED, verbatim. OVERRIDE of [D] §T3.5:** SUBSTRUCTURE requires `Δ ≥ 0.5 × R_lo`; ONE KIND
requires the upper 95% bootstrap bound on `Δ` to be `< 0.5 × R_hi`; UNDERPOWERED is the
complement. `R_lo` and `R_hi` are the 95% bootstrap bounds on `R` over the **48** control items
(post-MAJOR-6), 10,000 resamples, and **both are reported with the point estimate**. This removes
the referee's coupling in which a lucky `R` raises the substructure bar and lowers the null bar at
once.

### MAJOR-8 — T4's arm P is unconstrained on cut ratio yet sets the pass threshold

> *Fix:* "extend the ±20% cut-ratio constraint to all three arms, measured and reported per arm."

**FIXED, verbatim. OVERRIDE of [D] §T4.3 constraint 1:** the **M-, C- and P-arm** cut ratios
(CUT tokens ÷ WHOLE tokens) must match within **20%**, **measured and reported per arm**. If they
do not, the interaction is **reported as confounded, not adjusted** — [D]'s own rule, now applied
to the arm that sets the threshold.

### MAJOR-9 — T4's gate 1 has no power statement, on 12 vs 24 items

> *Fix:* "state the gate's power, or raise arm P to 24 (the authoring budget line in §5 counts
> 150 items across T3+T4 and can absorb it)."

**FIXED — raise and state.** Arm **P goes to 24**; T4 is **24 + 24 + 24 = 72 items**. Gate 1's
own power: at 24 vs 24 one-sided `p < 0.05`, 80% power needs a shift difference of **≈33
percentage points**; at [D]'s 12 vs 24 it needed **≈42 pp**. Stated so a gate VOID can be read as
underpowered rather than as "the cut was never read". Authoring cost is in §A2.5.

### MAJOR-10 — T5's bands leave the pre-registered *expected* outcome unbanded

> *Fix:* "add two no-verdict bands — '**EXPECTED NO-FIT — warrant axis**' (`R ≥ 1`, §T5.8 applies,
> reasons about WHO) and '**RESIDUE, UNCLUSTERED**' (recurrence passes, reasons do not cluster)."

**FIXED, verbatim.** Two bands are added to [D] §T5.9, evaluated **after** CANDIDATE SITE and
**before** RESIDUAL, UNDERPOWERED:

| band | condition | reading |
|---|---|---|
| **EXPECTED NO-FIT — warrant axis** | `R ≥ 1` **AND** §T5.8's *who*-defence applies (reason fields about speaker identity, authority, whose knowledge it is) **AND** the row is row 8 | the warrant coordinate, which we already carry and `warrant_invisible_to_kind` proves is not a kind. **No verdict on a twelfth**, and the NO-FIT is still recorded in `R` and reported. |
| **RESIDUE, UNCLUSTERED** | `R ≥ 1` **AND** stage-2 recurrence **passes** **AND** the reason fields do **not** cluster semantically | a distinction that resists our sites across six unrelated families whose *reasons* we cannot read as one thing. **No verdict.** Recorded as a named residue at higher priority than RESIDUAL, UNDERPOWERED, and queued with the families named. |

### MAJOR-11 — stage 2's trigger over-runs its own budget, and the overflow is a free choice

> *Fix:* "pre-declare a deterministic recurrence order (ascending category number) and a hard
> cap, and record un-recurred qualifying categories by name as un-recurred."

**FIXED, verbatim. OVERRIDE of [D] §T5.5's stage 2:** qualifying categories (`R ≥ 1` or an
indeterminate reading) are recurred in **ascending category number**, hard cap **3 categories**
(54 judgments). **Every qualifying category not recurred is recorded BY NAME as un-recurred**, in
the results table, with its qualifying reason. A category that is not recurred cannot reach
CANDIDATE SITE (which requires recurrence) and is reported as **un-recurred, not as refuted** —
the distinction is the point.

### MAJOR-12 — GLOSS-T is not kind-neutral, and its bias runs toward the staked secondary

> *Fix:* "add a tag-null control — for ≥3 categories, run a GLOSS-T pair whose tag is
> **unchanged** while the text differs, and one whose tag changes to a *different value of the
> same category* — and pre-commit that carrier-label landings present under GLOSS-T and absent
> under GLOSS-N are scored as **convention artifacts**."

**FIXED, verbatim.** **TAG-NULL CONTROL**, added to [D] §T5.4, on **3 categories** chosen in
ascending category number from those with ≥3 obligatorily-marked values (so the second pair type
is constructible), × 3 languages × 2 pair types × 3 mappers = **54 judgments**:

- **pair type α — tag held, text varies:** the bracketed tag is **byte-identical** before and
  after while the surrounding text differs. Any landing on Structure / Circumstances here is
  **caused by the convention**, not by the category.
- **pair type β — tag varies within category:** the tag changes to a **different value of the same
  category** while the text is byte-identical. This is the GLOSS-T condition with the category's
  own semantics carried and nothing else.

**Pre-commitment, frozen:** a **carrier-label landing (Structure, Circumstances, Manner) that is
present under GLOSS-T and absent under GLOSS-N is a CONVENTION ARTIFACT**, scored as such,
reported separately, and **excluded from the "≥ 6 of 13 non-content" secondary stake** — which is
exactly the stake the convention biases in its own favour.

**And the mis-attribution the referee names, closed:** instability between conventions whose
cause is the tag rendering may **not** be routed into [D] §T5.9's **VOID — gloss** band ("we
measured English, not grammar"). The tag-null control separates the two: instability that appears
in pair type α is **convention-borne** and is reported under its own heading; only instability
outside it counts toward the 30% VOID — gloss threshold.

### MAJOR-13 — per-item attestation is owed on all 39–42 pairs, and two rows are prima facie at risk

> *Fix:* "add a citation/datapoint column to the frozen table and fill it before freeze; where
> WALS has no datapoint for the named language, mark the row **secondary frame** in the table
> itself rather than in prose."

**FIXED AS A DESIGN CHANGE, WITH A BLOCKING PRE-FREEZE TASK. This amendment cannot discharge it,
and says so rather than pretending.**

**OVERRIDE of [D] §T5.3:** the frozen category table gains a **CITATION / DATAPOINT column, one
entry per (category × language) instance** — a named published example or a WALS datapoint,
verified against the primary source. [D] §T5.4's attestation requirement is already
**VOID-bearing**; it now has somewhere to live.

> **BLOCKING PRE-FREEZE TASK T5-ATTEST.** The freeze does not happen until the citation column is
> filled for every instance. An unfilled instance is **VOID by [D] §T5.4** and is dropped, which
> moves the denominator — see MINOR-8, which makes the bands functions of the surviving `N`.

**The three at-risk rows, named with their disposition rules so the outcome is not an author's
choice at fill time:**

| row | risk | disposition rule |
|---|---|---|
| **3** (Optative, WALS 73A, Ancient Greek) | WALS 73A's discussion is Caucasian and South Asian; its sample is overwhelmingly modern and does not treat Ancient Greek | if WALS 73A has **no datapoint** for Ancient Greek, the instance is marked **secondary frame in the table** and row 3's frame column reads "WALS 73 for the category, named survey for the instance" |
| **14** (Definiteness, WALS 37A, Persian) | WALS 37A's value set includes **"No definite, but indefinite article"**, the value Persian is standardly assigned — which would fail T5's own **obligatory-marking** selection criterion | check Persian's **actual WALS 37A value** first. If it is "no definite article", the instance **fails the selection criterion and is dropped**, and a replacement instance from a third family is sought; if none is found before freeze, row 14 runs on **two** languages and is marked as such |
| **1** (Evidentiality, WALS 77, Cuzco Quechua) | ch. 77's text discusses Tuyuca and Turkish, not Cuzco Quechua | row 1 is already **secondary frame for values** (BLOCKER-7); if WALS 77 carries **no datapoint** for Cuzco Quechua, the instance is secondary-frame for presence too, and that is recorded in the table |

### MAJOR-14 — the two most dangerous prongs share a witness

> *Fix:* "replace Turkish in row 12 with a language whose mirative is not its evidential, or add
> to §T5.3: 'rows 1 and 12 share the Turkish morpheme and are **not independent**; a site
> supported by both counts as **one** witness.'"

**FIXED by the second option, with the first offered as an optional improvement.** Naming a
replacement language from memory would be exactly the armchair mechanism-assertion GATES.md
forbids ("every mechanism needs a new search"), and this amendment has no typological source open.

**OVERRIDE — added to [D] §T5.3:**

> **Rows 1 and 12 share the Turkish morpheme `-mIş` — simultaneously the canonical Turkish
> non-firsthand evidential and the canonical Turkish mirative, and whose status as a separate
> mirative category is the live dispute in the very literature the rows cite (DeLancey vs
> Aikhenvald). The two rows are NOT INDEPENDENT on that language. A candidate site supported by
> both counts as ONE witness, never two**, and is subject to §A2.1.1's per-candidate two-witness
> bar like any other. [D] §7 doubt 14 registers the T3/T5 version of this risk and misses this
> one; doubt 14 now covers both.

**Optional pre-freeze improvement (not required, and not a blocker):** replace row 12's Turkish
instance with a language whose mirative is distinct from its evidential, **verified against
DeLancey 1997 or Aikhenvald 2012 at the primary**. If done, the non-independence note is retained
in the record with the replacement noted beside it.

### MAJOR-15 — the two-witness rule is not scoped to a candidate, and the combination readings contradict each other

> *Fix:* "one sentence in §3 — 'the two-witness bar is **per candidate site**: two independent
> legs must name the **same** site. N unrelated candidates are N separate challenges, each owing
> its own second witness.' Delete 'the count moves twice' from the §14 row."

**FIXED, both halves.** The sentence is added to the ported §3 in **§A2.1.1**, verbatim.

**OVERRIDE of [R] §14's `T3 SPLIT-AND-DIVIDES + T5 TWELFTH` row.** [R] is superseded, so the row
is not in force; its reading is restated here corrected, because the combination is live under
[D] too:

> **T3 SUBSTRUCTURE + T5 CANDIDATE SITE** — **two different candidate sites from two unrelated
> probes.** They are **NOT** mutual corroboration and the count does **not** "move twice": each is
> a separate challenge owing its **own** second witness naming the **same** site. This is
> [D] §7 doubt 14's reading and it governs. The phrase *"the count moves twice"* is **struck**.

### MAJOR-16 — §T5.11's conditional re-registration is an adaptivity leak, and it contradicts the paragraph above it

> *Fix:* "pre-write the twelve-site version of §T5.6 now … so the branch is frozen rather than
> re-registered; or delete the exception and rely on the invariance claim the same section
> already makes."

**FIXED by deletion — the second option, and BLOCKER-4's resolution makes it forced rather than
chosen.** Under decision 4, T1 cannot deliver a live twelve-site model: an F1 derivation VOIDs T1
and sends it to re-registration. There is therefore no branch left to pre-write.

**OVERRIDE — [D] §T5.11's exception paragraph is DELETED in its entirety.** What remains of
§T5.11 is its invariance claim, which stands as written:

> T5 runs after T1 because T1 decides the vocabulary of the write-up. **The kind-level mapping is
> invariant to T1's outcome — the eleven kinds are the same set either way — so only the
> site-level narrative moves.** §T5.6's three outcomes are **not** re-registered under any T1
> result. If T1 VOIDs on a twelfth constructor, T5 still runs against the **eleven kinds**, and
> the twelve-site question belongs to the re-registration.

This closes the adaptivity leak the referee identified as the concrete inter-leg information
channel, and it is why §A2.1.4 ports G15: with the exception gone, no leg reaches forward.

---

## §A2.4 MINOR dispositions

All 11 **FIXED**. One line each.

1. **`rfl` unavailable for the stake as written** — **FIXED.** [D] §T1.0's *"`generator2_image` is
   `rfl`"* is **struck**; §T1.4 stake 2 is stated as `List.Perm` (or `Finset` equality) proved by
   `decide`, because §T1.2's list order deliberately differs from `Site.all`'s (verified: `Site.all`
   maps to `[empirical, epistemic, deontic, ontological, axiotic, procedural, nomological,
   axiomatic, structural, pragmatic, contingent]` while §T1.2's order gives
   `[…, nomological, axiomatic, deontic, axiotic, procedural, ontological, …]` — positions 3–8
   permuted), and proving it by `rfl` would mean silently re-ordering the list and undoing the
   anti-rigging device.
2. **Blind-deriver prompt leaks the answer** — **FIXED** in §A2.1.3 step 4: the active-inference
   factor letters `A`, `B`, `C`, `D`, `π`, `γ` are stripped from all deriver-facing copy; the
   literature names stay.
3. **Blind arm's pass criterion unscoreable** — **FIXED** in §A2.1.3: the **eleven routing
   examples are published in this amendment**, in neutral vocabulary, and a **third-party scorer**
   with no repository access and no authoring role does the scoring.
4. **Lean warrant for the idempotency test overread** — **FIXED** in §A2.1.2: the test is a
   **stipulated criterion**; the claim that `Stack.lean` grounds "a sharp, domain-independent test"
   is struck (verified: `modulate : Rung → Rung | _ => .strengthMarker`, a constant function, and
   the file's own docstring calls it a definition).
5. **K5b unreachable as written** — **FIXED.** [D] §T4.6's K5b is redefined on a **carrier share
   ≥ 1/3** of moved M-items landing on Structure or Circumstances — which can co-occur with the
   primary's ≥ 2/3 content-direction pass — so "reported adverse **even if the primary passes**"
   becomes reachable and is retained.
6. **K4b's "incoherent" undefined** — **FIXED.** [D] §T3.5's K4b: the staked destinations are
   pre-declared **B → Process/Rules, A → Facts/Premises**, and **incoherence := ≥ 50% of leak mass
   landing outside those destinations**.
7. **Genus labelled as family** — **FIXED.** [D] §T5.3 rows 5 and 12 read **Na-Dene** (Navajo,
   Hare), not "Athabaskan", which is a genus under Na-Dene in WALS; no row is lost, and an honest
   scorer applying [D] §T5.2's "family level, not genus" gate literally would have dropped both.
8. **Denominator 13 assumed** — **FIXED.** [D] §T5.3's *"expected surviving primary set: 13"* and
   §T5.9's *"`F` in 8–12 of 13"* are restated as functions of the **surviving denominator `N`**:
   PARTIAL is `F ≥ ⌈0.6N⌉` with the remainder indeterminate rather than NO-FIT; DEGENERATE is
   `> N/2` mapping to Facts; the power bound is stated as the **95% upper bound on a 0-of-`N`
   proportion**, computed from the realised `N` (at `N = 13` this is the ≈20% [D] quotes), and is
   never quoted as ≈20% unless `N = 13`.
9. **A1's chance baseline uniform where marginals are not; pair-extraction undefined for 3-class
   blocks** — **FIXED.** Chance is defined by the **fresh-label marginals**, not by 1/55;
   *"≈4.6× chance"* is **struck**; and the extraction rule is frozen as **all unordered pairs from
   the block's label set, each block weighted equally by dividing by its own pair count** (a
   3-class block contributes three pairs at weight 1/3 each). **The mixed frame is pinned:** a
   block is in-frame iff the **union of the fresh annotators' labels for it has cardinality ≥ 2**,
   whether from one annotator's multi-label or from disagreement between annotators.
10. **A1's permutation null degenerate; axiomatic stake presumes an unfixed frame** — **FIXED.**
    The null is **random reassignment of whole per-block label multisets across blocks** (a
    within-block label permutation leaves each block's unordered pair set invariant and cannot move
    the statistic — the same degeneracy as the margin-preserving cluster null already on the
    record); the fresh-annotation frame is pinned as **the full `en` block set** for the
    `axiomatic` rate stake and **the mixed frame of MINOR-9** for the concentration stake; the
    stake is restated as a **rate on the realised annotated `N`, ≥ 1%**; and **1–6 blocks ⇒ NO
    VERDICT** — KILL-A1.2 fires only at **exactly zero**.
11. **Three citation defects** — **FIXED.** (i) [D] §5's reporting rule is `epistemology.md`
    **L8 (§3)** and item **7** of `CLAUDE.md`'s discipline list, not "§7" (which is *What is
    borrowed here, and what is ours*); (ii) [D] §T3.5 cites **`scratchpad/gaugetest/analyse_gauge.py`**
    with its path, and the arm mapping is restated for this leg — that script's stage 1 loads
    **arms A and C** (verified at `analyse_gauge.py:119`), whereas **T3's control stage opens arm
    D only**, so it is the *two-stage refusal pattern* that is borrowed, not the arm letters;
    (iii) [A1] §A1.1.7's evaluation order is frozen as **VOID — provenance → VOID — register →
    CASE rows → NULL**, and VOID — register necessarily precedes NULL because it is counted on the
    **source side before any target locale is opened** ([A1] §A1.1.5, §A1.1.6 step 1).

---

## §A2.5 Execution order and the unified spend table

### A2.5.1 Execution order — ORCHESTRATOR'S DECISION 2

**T1 → T2 → T3 + T4 → T5.** Marked as the orchestrator's decision: it is **neither** [D]'s order
(T1 → T5 → T2 → T3+T4) **nor** [R]'s (T1 → T4 → T3 → T2 → T5), and both of those rationale
paragraphs are struck (MAJOR-1).

**The rationale, in one line: escalating exposure — panel legs after source legs, and the most
dangerous leg last with maximal insulation under the no-adaptivity rule (§A2.1.4).**

| order | leg | why here |
|---|---|---|
| **1** | **T1** — Generator2, the two placebos, the blind-deriver pass | free and decidable, and the placebo differential decides whether the generator's *warrant* is in question before anything is spent |
| **2** | **T2** — ISO 24617-2 mapping | a **source** leg: the work is reading Bunt 2017 and mapping 17 devices. It exercises the three-mapper schema (MAJOR-3's counts, MAJOR-4's SURVIVES-OUTSIDE field) on the cheap case, and it gives §A2.1.1's candidate-site rule its first workout on a candidate named in advance |
| **3** | **T3 + T4** together | the **panel** legs: one authoring pass, one panel session, shared self-check tooling. They run after the source legs because their instrument is the one T2 has just exercised, and they are the two legs whose kills are most contained |
| **4** | **T5** — typology | **last, and deliberately.** It is the only leg whose evidence comes from outside the programme's lineage and the only one whose positive outcome challenges a published count. Running it last, with §A2.1.4's no-adaptivity rule in force and §T5.11's exception deleted (MAJOR-16), means **nothing earlier can reach forward and rewrite what its outcomes mean** |

**Dependencies preserved:** T5 still runs after T1 ([D] §T5.11's invariance claim, exception
deleted). T5-I1 now shares **T2's** mapping instrument rather than the reverse (MAJOR-1). T5-I2
and T5-I3 run inside T5's slot, after T5-I1, and neither may enter T5-I1's statistics ([A1]
§A1.1.0's subordination rule, unchanged).

**Halting rules, frozen:** (i) a leg VOID is reported and does not halt the season; (ii) **any two
VOIDs halts the season** — the instrument suite, not the taxonomy, is what was measured, and the
instruments are repaired before re-registering; (iii) if the global cap is reached, remaining legs
are filed **UNGAUGED, never shrunk to fit**.

### A2.5.2 The unified spend table — ONE global cap, a line for every instrument

**GLOBAL CAP $6.00.** Per-leg lines sum to **$2.75 ≤ $6.00**. Caps are **human-upheld**
(BLOCKER-11); the preflight/postflight files are the record.

Judgment-cost basis: PLANE's measured **$0.63 for 5,994 judgments ≈ $0.000105/judgment**, on the
same three model families at temperature 0. Estimates below use it; caps carry 5–10× headroom so
a price surprise does not VOID a leg that was correctly designed.

| # | line | what it covers | judgments (est) | est spend | **CAP** |
|---|---|---|---|---|---|
| 1 | **T1** | Lean; the blind-deriver pass (3 derivers × 3 mode sets = 9 derivations); third-party scoring | agent time; ≤ 40 API calls if run by API | $0.02 | **$0.25** |
| 2 | **T2** | 17 ISO devices × 3 mappers, with the MAJOR-4 field in the same call | 51 | $0.01 | **$0.15** |
| 3 | **T3** | arms A 30 + B 30 + D 48 = 108 items × 3 models | 324 | $0.04 | **$0.40** |
| 4 | **T4** | arms M 24 + C 24 + P 24 = 72 items × 2 conditions × 3 models, plus CUT-B 24 × 3 | 504 | $0.06 | **$0.60** |
| 5 | **T5-I1** | typology: 234 base + 42 (BLOCKER-7) + 54 (MAJOR-12 tag-null) + 54 (stage 2, capped by MAJOR-11) | 384 | $0.05 | **$0.50** |
| 6 | **T5-I2** | 29-locale translation stack — **VOID-EXPECTED on provenance** ([A1] §A1.1.4) | 0 | $0.00 | **$0.00** |
| 7 | **T5-I3** | fresh annotation of the full `en` block set × 3 annotators (concentration stake needs the mixed frame; the `axiomatic` rate stake needs the whole set, MINOR-10) | 1,905 | $0.21 | **$0.60** |
| 8 | **A0 screen** | [A1] §A1.3.2 degeneracy screen on the RATCHET candidates — **local computation, no API** | 0 | $0.00 | **$0.00** |
| 9 | **T3-ALT** | RATCHET adjudication corpora, fresh kind annotation — **contingent**: runs only if the A0 screen clears **and** T3's primary authoring falls short | 816 | $0.09 | **$0.25** |
| | **ALLOCATED** | | **≈ 3,984** | **$0.48** | **$2.75** |
| | **UNALLOCATED RESERVE** | **may not be spent without a numbered amendment** | | | **$3.25** |
| | **GLOBAL** | | | | **$6.00** |

**Line 6 is $0.00 because T5-I2 is VOID-EXPECTED** ([A1] §A1.1.4: `generated_by:
claude-opus-4-6`, all locales class P0 by the manifest's own testimony). **It is un-voided only by
a numbered amendment** that both establishes a P2-or-better asset and moves spend from the
reserve. Registering it at $0.00 is the honest form: the instrument stays in the record with its
VOID visible, and it cannot quietly acquire a budget.

**The binding cost is authoring, not money** — and the referee's fixes raised it. [D] §5 counted
150 items across T3+T4; after MAJOR-6 (+18 to arm D) and MAJOR-9 (+12 to arm P) it is **180**.
T5's minimal pairs go from 39 to **46 + 18 tag-null pairs = 64 presentations-worth**, every one
carrying a verified citation (MAJOR-13's blocking task). [D] §5's authoring constraints are
unchanged and still bind: mechanical self-check, declared ban-sets, verified citations, and **no
author sees this document's predictions for the leg they are authoring**.

### A2.5.3 The preflight line-item check (BLOCKER-11)

Before each leg's first API call, written to
`scratchpad/recognition_spend/<leg>_preflight.json`:

```
{ "leg": "T2",
  "cap_usd": 0.15,
  "cumulative_spend_prior_legs_usd": 0.02,   // read from prior legs' result files, not memory
  "projected_judgments": 51,
  "projected_spend_usd": 0.01,
  "hard_cap_usd_set_for_this_run": 0.15,     // the value plane_annotate.HARD_CAP_USD was set to
  "written_at": "<ISO timestamp>" }
```

**A leg run without its preflight file already on disk is VOID on spend discipline.** Postflight
appends actuals. Neither file is a mechanical enforcement; both are the record that a human upheld
the cap, which is the strongest true thing available.

---

## §A2.6 What died in review — struck pre-freeze, BY REFEREE, not by data

Listed by name so that no later reader can mistake any of these for a claim that met contrary
evidence. **None of these died from a result. Every one died from an argument, before the freeze.**

### A2.6.1 Predictions reversed or withdrawn under BLOCKER-6's repair

| item | where | what happened |
|---|---|---|
| **[R] §4 worked example 2** — *"if A, if B, then p" ≠ "if A, then p"* | [R] §4 | **DIED as an idempotency example.** It composes two different antecedents. Re-filed as a **C4 composition** example. |
| **[R] §4 worked example 3** — *"reported that it was inferred that p"* | [R] §4 | **DIED as an idempotency example.** It composes two different evidential values. Re-filed as a **C4 composition** example. |
| **[R] §4 example 1's mirativity limb** | [R] §4 | **DIED.** The certainty limb is worked and survives; the mirativity limb is **asserted, never worked, and not source-backed**, which [R]'s own evidence rule forbids. |
| **[R] §7.4 P2.4's idempotency warrant** — *"conditionality is non-idempotent by §4"* | [R] §7.4 | **DIED.** Re-staked as **P2.4-R: IDEMPOTENT → modulator**, the opposite sign. [D] §T2.4's **P2.7** (conditionality → Premises) never rested on it and **survives untouched**. |
| **[R] §10.3 P5.2 as stated** — *"source-of-knowing is non-idempotent, hence not a modulator"* | [R] §10.3 | **DIED.** Re-staked as **P5.2-R: IDEMPOTENT → modulator**, the opposite sign. |
| **[R] §10.4 WARRANT band's second conjunct** — *"and P5.2 holds"* | [R] §10.4 | **DIED** with P5.2. Its function is taken by the pre-staked **`E2-CONFLICT`** outcome (§A2.1.2), which carries **no verdict** rather than resolving the collision. |
| **The claim that `Stack.lean` grounds the test** | [R] §4 | **DIED** (MINOR-4). `modulate` is a constant function; the test is a stipulated criterion. |

### A2.6.2 Outcomes that were unreachable and are now labelled as such

| item | where | what happened |
|---|---|---|
| **F1 as a live escalation outcome** | [D] §T1.5 | **DIED** (BLOCKER-4 + decision 4). A twelfth constructor VOIDs T1 by T1-VOID-1; F1 is reachable **only through re-registration**. This was the outcome [D] §7 doubt 1 put "real probability" on, and the registration can no longer cash it — stated plainly rather than softened. |
| **§T5.11's exception** — F1 forcing §T5.6's outcomes to be re-registered | [D] §T5.11 | **DELETED** (MAJOR-16). It was the registration's one inter-leg adaptivity leak, and BLOCKER-4's resolution leaves it nothing to condition on. |
| **[D] §7 doubt 1's F1 implication** | [D] §7 | **STRUCK.** The doubt survives; its implication that F1 is a reportable outcome of this leg does not. |
| **[D] §T1.5's three DIFFERENT-IMAGE rows** | [D] §T1.5 | **RE-LABELLED**, not deleted: "reachable only under the re-registration required by T1-VOID-1". |
| **[D] §T1.4's five stakes as a result** | [D] §T1.4 | **RECLASSIFIED** as the **freeze-consistency check**. They still run; they are no longer evidence. T1's evidence is the placebo differential and the blind derivations. |
| **[R] §14's *"the count moves twice"*** | [R] §14 | **STRUCK** (MAJOR-15). N unrelated candidates are N challenges, each owing its own second witness naming the same site. |

### A2.6.3 Bands, thresholds and claims replaced

| item | where | what happened |
|---|---|---|
| **The REFUTED band's second conjunct** — *"AND some other three pairs at ≥25%"* | [A1] §A1.2.5, A1.h | **DIED** (BLOCKER-9). It protected the prediction against the cleanest disconfirmation available. REFUTED is now the ≤10% condition alone. |
| **The seen-stratum tie-break** — *"the primary governs"* | [A1] §A1.2.6(b), A1.i | **DIED** (BLOCKER-10). Replaced by the pre-staked reconciliation rule: on disagreement, **neither governs**, and the split is the result. |
| **[A1]'s *"alters no band, no kill, no VOID condition"*** | [A1], opening | **STRUCK** as untrue of §A1.2.4 (BLOCKER-2) and now of §A1.2.5 and §A1.2.6(b) as well. |
| **[A1] §A1.2.4's attribution *"per the delivered draft's floor"*** | [A1] §A1.2.4 | **STRUCK** as a misattribution ([D]'s floor is 0.4). The 0.6 floor is kept as **CHANGE-A2-1**, scoped, sourced to `PLANE_PREREG.md` §5. |
| **[A1] §A1.2.5's *"≈4.6× chance"*** | [A1] §A1.2.5 | **STRUCK** (MINOR-9). The marginals are not uniform; chance is defined by the fresh-label marginals. |
| **[A1] §A1.2.5's within-block permutation null** | [A1] §A1.2.5 | **DIED** (MINOR-10) — degenerate: it leaves each block's pair set invariant. Replaced by cross-block reassignment of label multisets. |
| **The disjunctive prongs of T5 rows 4, 7, 8, 9, 12, 14** | [D] §T5.3 | **DEMOTED** to alternative landings that score as **MISSES** (BLOCKER-8). No row is a free win any more; rows 4, 8 and 12 in particular no longer pre-register NO-FIT as a confirmed prediction. Row 2's disjunction is **not** demoted — it is a registered two-party disagreement and both prongs are scored as rivals, so one named party is recorded wrong whichever way it lands. |
| **[D] §5's mechanical-enforcement sentence** | [D] §5 | **DIED** (BLOCKER-11). `HARD_CAP_USD = 10.0` is a single global backstop that prints and returns; caps are human-upheld and now leave preflight/postflight files. |
| **Both execution-order rationales** | [D] §5, [R] §15 | **STRUCK** (MAJOR-1). The orchestrator's order and rationale govern. |
| **[D] §T1.0's *"`generator2_image` is `rfl`"*** | [D] §T1.0 | **DIED** (MINOR-1). §T1.2's list order is deliberately permuted; the stake is `List.Perm`/`Finset` equality by `decide`. |
| **[D] §T4.6's K5b as originally defined** | [D] §T4.6 | **DIED** (MINOR-5) — it was the complement of the primary's pass condition. Redefined on a ≥1/3 carrier share so it can co-occur with a pass, as its own text intended. |
| **[D] §T1.6 mitigation (iii) as an invitation** | [D] §T1.6 | **DIED** (BLOCKER-5). It is now a **mandate**, and without it the placebo leg is UNGAUGED and the primary uncashable. |

### A2.6.4 What did NOT die, recorded so the amendment is not read as a demolition

The referee's own "what is solid" section stands, and this amendment adds nothing against it:
[D] §T2.1's ISO extraction is verbatim-accurate and was done the hard way; every Lean object
either document cites exists under the name cited; the `Generator.lean` header line quoted
"verbatim" in §T5.1 is verbatim, and the hedging/evidentiality conflation §T5.1 attacks is
genuinely in the file, named by the programme against its own interest; the two-stage staging
discipline is real and has a working precedent; and §T1.6, §A1.1.4, §A1.2.2, §A1.2.6 and §T5.5's
power statement are **model disclosures made before the run, against interest, in the frozen
text**. The defects repaired above are defects **in mechanism, not in candour**.

---

## §A2.7 Blocking tasks that must complete before the freeze

Listed because a freeze taken while any of these is open would freeze a document that cannot be
executed as written.

| # | task | owner | why blocking |
|---|---|---|---|
| **B1** | **T5-ATTEST** — fill the citation/datapoint column for every (category × language) instance, verified at the primary, applying MAJOR-13's three disposition rules | authoring agent | [D] §T5.4's attestation requirement is VOID-bearing; unfilled instances drop and move `N` |
| **B2** | Verify category 1's per-language evidential **value inventories** against Aikhenvald 2004 (provisional Tuyuca 5 / Cuzco Quechua 3 / Turkish 2 is **NOT DATA**) | authoring agent | BLOCKER-7's pair count, the judgment total and the T5-I1 spend line all ride on it |
| **B3** | Prepend the three header lines of **§A2.0.2** to [D], [A1] and [R] in the freeze commit | orchestrator | BLOCKER-1 |
| **B4** | Resolve [A1] §A1.2.1's **635 vs 634** discrepancy at the pinned commit ([A1] A1.k) before either number enters a table | whoever runs T5-I3 | received-numbers gate; MINOR-10's rate stake is a fraction of it |

**Not blocking, but owed before the leg it belongs to runs:** the **C3-CONTROL** axis of §A2.1.2,
named with its source, before C3 absorbs any candidate; and the **OVERLAP-CHECK** of BLOCKER-10,
written to disk before T5-I3's primary is computed.

---

**Written 2026-08-20, before freeze, before any leg ran. This amendment is the diff; [D], [R] and
[A1] are unedited. Pending orchestrator review, then freeze.**
