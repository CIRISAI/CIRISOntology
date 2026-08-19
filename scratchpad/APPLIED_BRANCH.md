# The applied branch — 11+1 as an engineering discipline for the CIRIS Agent

Added to the DAG 2026-08-18 by the steward's direction. Dependencies only, no dates.
Research nodes N1–N18 are in the session record and `LEAN2_CONFRONTATION.md`; the A-nodes
below hang off them. The business case is already MEASURED, not hoped: unassisted model
panels absorb Premises changes into Facts 24/24 and described norms into enacted ones —
models systematically under-audit the highest-blast-radius change kinds, while the cheap
instruments see what the models miss (ripple conjunction 100%/0% authored, 0/279 false
fires wild). A pipeline that knows WHICH KIND of change it is making can budget
verification by kind: that is the rent clause as engineering — every kind pays rent at its
own decay rate, and uniform scrutiny overpays on Manner while underpaying on Premises.

## Where it lands in the CIRIS Agent (integration points, named from the code)

| CIRIS surface | the 11+1 move |
|---|---|
| **H3ERE step 2 (Perform DMAs)** | a kind-classification DMA beside CSDMA/DSDMA: every candidate action that mutates state is classified (which of the 11 kinds, or Record) and emits (kind, verification budget, deferral flag) into ASPDMA's context |
| **H3ERE step 4 (Conscience Execution)** | conscience depth keyed by kind — Manner/Structure get lint-grade checks; Facts get retrieval; Rules get authorization review; Premises trigger the ripple check; recursive conscience (4B) reserved for high-blast kinds |
| **MemoryBus.memorize / graph memory** | in a graph memory the ripple is EXACT, not heuristic: descendant count of the touched node. Premises-kind writes (nodes with inheritors) get their blast radius computed before commit |
| **WiseBus / Wise Authority** | kind-typed deferral policy: Premises/Rules/Identity changes above staked thresholds auto-defer to WA; Manner never defers. Sharper than uncertainty-only deferral |
| **Audit Service** | Record made operational: "can this claim be re-derived from the audit graph" is the Repairable(fact, frame) check with the audit trail AS the frame; a frameless provenance query refuses at the type layer (`Reading.frameSupplied`) |
| **Config Service** | config edits are literally Premises/Structure changes; the approval flow inherits the kind-typed budget |
| **Telemetry / RATCHET monitoring** | the kind distribution of an agent's changes as a ~12-dim monitoring basis: an agent whose change-mix suddenly shifts toward Premises/Identity is alarming in a way raw volume never shows |

## A-nodes, dependencies only

| # | node | needs | staked kill (each separable) |
|---|---|---|---|
| A0 | **Retrodictive shadow replay** (free, data in hand): run the instruments over the 6,465 scrubbed CIRIS traces; do kind-readings + kind-budgets predict the 1,962 recorded overrides (30.3%) better than the entropy/coherence scores do? | — | if kinds predict overrides no better than the legacy faculties, the collapse loses information the four consciences were catching — the re-orientation is wounded before it starts, reported plainly |
| A1 | **Router demo, pre-registered**: 12-instrument router in front of an edit-agent benchmark, verification budget by kind | — (instruments v0b/v0c/v0d exist) | must beat a COST-MATCHED uniform-verification baseline on a fixed error budget, else taxonomy theater; absorption rate on held-out boundary items is the second band |
| A2 | **Graph-ripple Premises gate**: MemoryBus.memorize interception, blast radius = descendant count, exact | A1 verdict | gate must not fire on >1% of Facts-kind writes (precision floor); ripple-vs-panel disagreement adjudicated on a sample |
| A3 | **Kind-typed WA deferral policy** | A1 verdict | deferral volume must not grow >2x at matched risk coverage, else it is a spam generator |
| A4 | **Record-typed audit integrity**: re-derivability against the audit graph, frameless queries refuse | Confront.lean Record semantics (done) + A1 | the check must catch a planted audit-tamper in a red-team run; a pass on zero planted faults is VOID, not support |
| A5 | **Kind-mix telemetry watchdog** | A1 instruments in the trace path | alarm ROC vs planted anomalous-mix episodes; false-alarm budget staked first |
| A6 | **Absorption fine-tune**: contrast-pair corpus (described-vs-enacted, definitional-vs-incidental) from the item factories; fine-tune the agent's LLM tier | item factories (done); NOT gated on N9 | held-out absorption rate fails to drop below staked band = the intervention dies, kept marked |
| A7 | **Aux-loss / probes / steering**: predict-the-kind head on edit pairs; the 11 discriminator directions as runtime probes | **N9 DETECTED** (aux-loss), **N9 STRONG** (probes/steering) | aux head must beat the same head on a random 12-way partition (the rival-partition control, imported from the prereg) |
| A8 | **The re-orientation** (see below): DMA layer reports on the 11, conscience operates on the +1 and the mutations | A1 + A2 + A3 green | agent-level A/B: structured-call count must drop by the staked fraction at NON-INFERIOR incident rate on state-mutating actions; a call-count win with an incident regression is a fired kill, not a trade-off |

Order of cheapness: A1 is pure lab (benchmark + existing instruments); A2–A5 are adapters
on named CIRIS services; A6 is one fine-tune with a pre-registered success band; A7 waits
on the eigen verdict; A8 is the only node that touches production, and it is gated on
three green predecessors plus its own A/B.

## What this branch does NOT claim

The taxonomy types the CHANGE-HANDLING surface — every state-mutating tool call, memory
write, config edit — not all computation. For an agentic system that surface is most of
what matters, but the claim stops there. Nothing in this branch flips any `validated` flag
(`suite_ships_unvalidated` stands until the human ceiling exists), and nothing lands on
the published page until the research branch closes (house rule).

## The re-orientation (the steward's move, 2026-08-18)

Not a kind-DMA bolted beside CSDMA/DSDMA — the DMA layer itself re-oriented:

1. **The DMAs report on the 11.** Every DMA output collapses to one Reading schema:
   (kind, evidence, magnitude). The 11 artifact-local kinds are frame-free by theorem
   (`no_reading_owes_design`, coordinate-flatness measured at p<0.01), so the DMA pass
   needs no frame context — cheap, parallelizable, one schema where there were several.
   The existing faculties largely MAP onto kinds rather than being deleted: CSDMA's
   plausibility is a Facts-facing reading, DSDMA's domain alignment is Rules/Model-facing,
   entropy/coherence scores are Confidence-facing. A refactor of the reporting vocabulary,
   not a rebuild of the faculties.
2. **The conscience operates on the +1 and the mutations.** Record CANNOT live in the DMA
   layer — `repairable_does_not_factor` is machine-checked: no artifact-only predicate
   computes it. The conscience is the component that holds the frame (audit graph,
   covenant, WA relationship), so the frame-relation belongs there BY THEOREM, not by
   taste. Conscience asks: what does this mutation do to re-derivability, and does its
   kind-budget demand recursion (4B) or deferral (WiseBus)?
3. **Why this cuts calls and schemas.** The measured two-stage mechanism (labels
   site-cue-driven; frames computed on demand and never routed into labels) is how the
   models already factorize the problem — the architecture stops fighting the model's
   grain. Heuristic halves decide most changes without any LLM call (wild sweep: the
   instruments are decisive at 0 API cost on the bulk); the LLM structured call fires on
   gate-hit only; Manner/Structure-kind actions skip conscience recursion outright.
   The claim is STAKED, not assumed: schemas counted before/after, structured calls per
   H3ERE round counted before/after, at non-inferior incident rate — the A8 kill.

## The collapse arithmetic (steward's counts, 2026-08-18)

Today: THREE DMAs (`csdma.py`, `dsdma_base.py`, `idma.py` in `ciris_engine/logic/dma/`)
plus ASPDMA for selection; FOUR consciences (Entropy, Coherence, Optimization-Veto,
Epistemic-Humility in `ciris_engine/logic/conscience/`). The re-orientation's target:

- **DMAs 3 → 1.** One exhaustive kind-reader with one Reading schema. ASPDMA stays —
  selection is not classification.
- **Consciences 4 → 1.** Entropy, Coherence, and Humility are Confidence-facing readings
  of the artifact — they move DOWN into the DMA layer's kind report. Optimization-Veto is
  Priorities-guarding (Goodhart is a pair-check on a target) — it becomes the Priorities
  kind-budget. What remains — the only thing that MUST remain, by
  `repairable_does_not_factor` — is the frame-relation: one conscience operating on Record
  and the mutations, holding covenant + audit graph as its frame, with the kind-budgets
  as configuration rather than as separate faculties.
- **Depth is preserved by recursion, breadth by theorem.** The old architecture bought
  coverage with PARALLEL BREADTH — three DMAs and four consciences each watching a
  different angle, because none was exhaustive. `every_site_classified` /
  `generator_image` make the top exhaustive by theorem (adequacy measured: 1 NO-FIT in
  279 wild changes, and it was a glyph swap), so the parallel insurance can be retired
  and depth comes from the EXISTING recursion (3B/4B), triggered selectively by
  kind-budget. Exhaustiveness is what licenses collapse — only tidy things can be
  profound, as the steward put it; untidy tops need redundancy precisely because they
  cannot prove coverage.

The validation is A0 and it is free: the scrubbed trace corpus carries
`action_was_overridden` on every row (1,962 of 6,465 — 30.3%). Replay the traces through
the instruments and test, pre-registered, whether kind-readings predict the overrides the
production system actually issued — and specifically whether anything the four
consciences caught goes UNCAUGHT under kinds + one frame-conscience. That number decides
whether 3+4 → 1+1 is a collapse or an amputation, before a line of the agent changes.
