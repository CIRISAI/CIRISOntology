# RATCHET series proposal — H3ERE2 in SHADOW MODE on the CIRIS agent

**Status:** proposal, issue-ready for `CIRISAI/RATCHET`. Nothing here is built.
**Date:** 2026-08-22
**Depends on:** `CIRISAgent` H3ERE pipeline (paths cited inline), the frozen H3ERE2 v2 candidate,
`REG_SPEC.md` v0.3, `BRIDGE_STAKES.md`.
**Headline constraint, up front:** the frozen H3ERE2 candidate **FAILED its held-out license**
(§3). This proposal is therefore for **shadow-mode data collection and instrument iteration
only**. It does **not** propose replacing live evaluation in the agent, and no experiment below
may be read as licensing that.

---

## 0. Terms, defined once

Readers who have not followed the research programme need six terms. Everything else is
ordinary engineering.

| term | meaning |
|---|---|
| **the eleven kinds** | A taxonomy of *what a change to a message actually varies*: Facts, Rules, Manner, Identity, Priorities, Confidence, Circumstances, Process, Structure, Model, Premises. Plus **Record** (the "+1"), which is not a twelfth kind but a relation about whose word is on the books. See the RATCHET README. |
| **the surface four** | Facts, Rules, Manner, Identity — readable straight off the text, and carrying ~91% of real change traffic (staked forward at 0.89, measured 0.883 on a never-touched stream). |
| **the deep seven** | The remainder. They rarely announce themselves; they arrive *wearing* a surface kind — "a changed assumption arrives as a burst of changed Facts". |
| **carries** | The name for that wearing: transport of claim content from kind `d` to kind `d'`. It is REG's sixth verb (`REG_SPEC.md` v0.3). |
| **carries-inversion** | The inverse operation: given a surface-classified change, infer which deep kind is wearing that surface here. This is what H3ERE2's stage 2 does. |
| **REG / CEG** | CEG is the deployed CIRIS Epistemic Grammar (a wire format for attestations). REG is its lab-frame counterpart — deliberately stripped of CEG's defenses so the attacks become measurable. REG is an instrument, never infrastructure; see §4. |
| **κ (kappa)** | Fleiss' kappa, chance-corrected inter-rater agreement across a panel of independent model families. |

**H3ERE** is the agent's existing evaluation pipeline — Hyper3 Ethical Recursive Engine
(`CIRISAgent/CONTRIBUTING.md:15`; glossary entry at `FSD/PROOF_OF_BENEFIT_FEDERATION.md:57`). **H3ERE2** is a *classifier pipeline for changes*, built in
the research programme, whose control flow deliberately mirrors H3ERE's. The two operate on
different objects. That mismatch is load-bearing and is stated plainly in §2.3 — do not let the
shared name imply a shared validation.

---

## 1. What H3ERE2 is

H3ERE2 is a three-stage recursive classifier that maps a change into a REG term — a **kind**
(one of 11+1) and a **verb** (one of REG's 5+1). The frozen candidate is
`h3ere2_v2.py`, sha256 `523fd6d0c45cd50e`, declared in
`scratchpad/TRANSITION_MAP/H3ERE2_TUNING/FROZEN_CANDIDATE.md`, invoked as

```
python3 h3ere2_v2.py full <dataset> <out.jsonl> v4 a5 -     # env NO_FAST_ON_FACTS=1
```

### 1.1 S1 — surface evaluation (`s1_v4`)

One call per change. The prompt **forces two candidates**: the item's best fit among the surface
four, *and* its best fit among the deep eight (deep seven + Record), named side by side. It then
demands a **ternary sufficiency verdict** — `SURFACE_ONLY` / `CLOSE` / `DEEPER` — plus the REG
verb, a confidence in [0,1], and a one-sentence rationale. It inherits an explicit
retention/comparison frame and applies four boundary tests.

The forced-two-candidate design is not cosmetic. Round 0 of tuning ran a single-choice S1 and it
returned `DEEPER` **zero times in 361 parseable calls**, with 97% of confidences ≥0.9 against a
0.7 gate: the pipeline was nearly flat. Forcing a named deep rival moved DEEPER-recall from 0 to
1.000 on the screen (`H3ERE2X_PREREG.md` AMENDMENT T2; `round1_2_3_tuning.md` round 1).

### 1.2 The gate

Fast-exit **only** on `SURFACE_ONLY`, at confidence ≥ 0.7 (frozen), **and never when the cleared
reading is Facts** (`NO_FAST_ON_FACTS=1`). The Facts carve-out was a measured round-3 fix: triage
is not competent to clear a Facts reading, because Facts is where two of the three known
confusion boundaries land. It moved curated Circumstances accuracy from 0.433 to 0.967.

Measured fast-exit rates: **4.8%** on the curated anchor (which is two-thirds deep by
construction) and **20.0%** on wild traffic. The gate is a wild-traffic economy; it barely fires
on deep-loaded data, by design.

### 1.3 S2 — carries-inversion with boundary priors (`s2_a5`)

Receives S1's output verbatim and asks the inversion question: *which deep kind would wear this
surface, here?* It carries keyed discriminators per deep kind, Identity/Facts protection, a
declared-basis test and an arrangement test. Its priors are the **three measured boundary
channels** — Premises/Facts, Structure/Manner, Model/Facts — which were predicted by the panel
study, then independently re-localized by the Babel instrument.

### 1.4 S3 — conscience verification, one guided retry (`s3_v1`)

A one-sided verifier: *"would `<deep>` wear `<surface>` here?"* → PASS/FAIL plus guidance text.
On FAIL, S2 re-runs **once** with that guidance injected. The retry is accepted **only if the
retry itself passes**; otherwise the first answer is kept (`keep-first`). If it still fails, the
final label is emitted **flagged UNVERIFIED**.

The keep-first rule replaced the original "second answer wins", on measurement: a two-sided
conscience wording FAILed 93% of items and its retries **damaged 29 and improved 11**. Round 1
of tuning; the rule change took curated accuracy from 0.578 to 0.750.

Measured conscience FAIL rate on curated: 0.195 over 354 firings. Route telemetry, curated:
recurse-pass 285, retry-rejected 46, retry-pass 23, fast 18.

---

## 2. How it maps onto the agent's H3ERE stages

### 2.1 The agent's pipeline as it stands

Step points are enumerated in `ciris_engine/schemas/services/runtime_control.py:102-116`
(`StepPoint`) — ten in all — and each has a phase module under
`ciris_engine/logic/processors/core/thought_processor/`. The evaluation-relevant subset:

| step | module | what it does |
|---|---|---|
| `GATHER_CONTEXT` | `gather_context.py` | builds context for evaluation |
| `PERFORM_DMAS` | `perform_dmas.py` | runs **three DMAs in parallel** (PDMA ethical, CSDMA common-sense, DSDMA domain), plus IDMA |
| `PERFORM_ASPDMA` | `perform_aspdma.py` | LLM action selection over the DMA outputs |
| `CONSCIENCE_EXECUTION` | `conscience_execution.py` | epistemic-faculty validation; may override with a stated reason |
| `RECURSIVE_ASPDMA` | `recursive_processing.py` | on conscience failure, re-run selection **with the override reason injected as guidance** |
| `RECURSIVE_CONSCIENCE` | `recursive_processing.py` | re-validate the retried action |
| `FINALIZE_ACTION` | `finalize_action.py` | final determination; DEFER/PONDER when retries are exhausted |

The DMA inventory is `ciris_engine/logic/dma/README.md:16` ("4 Core + 1 Recursive = 5 Total
DMAs"). The retry budget is `conscience_retry_limit: 2`
(`config/essential.yaml:32`, schema at `ciris_engine/schemas/config/essential.py:127`). The
recursive contract — *first bounce goes to RECURSIVE_ASPDMA, not PONDER* — is documented at
`ciris_engine/logic/conscience/README.md:157`.

### 2.2 The correspondence

H3ERE2's control flow was built as a mirror of exactly that shape, and the mirror is tight:

| H3ERE2 | H3ERE | note |
|---|---|---|
| S1 forced two-candidate + ternary verdict | `PERFORM_DMAS` + `PERFORM_ASPDMA` | **This is the consolidation.** Where H3ERE fans out to parallel evaluators and then selects, H3ERE2 issues one call that names two rival readings and adjudicates them in the same breath. |
| the gate (`SURFACE_ONLY` ∧ conf ≥ 0.7 ∧ ¬Facts) | — | **New.** H3ERE has no fast path. The gate is what buys the consolidation its cost back on the ~91% of traffic the surface four carry. |
| S2 carries-inversion | the recursive stage's *work* | H3ERE recurses to re-select an action; H3ERE2 recurses to un-launder a kind. Same position in the flow, different job. |
| S3 conscience verify | `CONSCIENCE_EXECUTION` | **Conscience moves.** In H3ERE it validates the *selected action*. In H3ERE2 it validates the *inversion claim* — a structural assertion about the object, not an ethical one about an output. |
| one guided S2 retry, keep-first | `RECURSIVE_ASPDMA` / `RECURSIVE_CONSCIENCE` | Same guidance-injection mechanic. **Budget differs: H3ERE2 retries once, H3ERE twice.** |
| final flagged `UNVERIFIED` | `FINALIZE_ACTION` → DEFER/PONDER | The unverified flag is H3ERE2's DEFER: an answer emitted with its warrant withheld. |

**Where the DMA consolidation claim actually bites.** The hypothesis is that the parallel-DMA
fan-out is doing work that a single forced-comparison call does as well or better on the bulk of
traffic, and that the fan-out earns its cost only on the residue the gate declines to clear. That
hypothesis is **untested on the agent** and is what experiment RS-2 (§5) exists to measure. It is
not established by anything in the research record.

### 2.3 The mismatch, stated plainly

H3ERE2 was validated as a **classifier of textual changes**, on revision chains and an authored
corpus. H3ERE evaluates **an agent's candidate actions** for ethical adequacy. These are different
objects. Nothing in H3ERE2's measurement record transfers automatically to the agent's task, and
the shared control-flow shape is a design inheritance, not evidence. Every experiment below is
scoped so that its result stands or falls on agent-stream data.

---

## 3. Validation status — carried honestly

**The frozen candidate is NOT LICENSED.** `VALIDATION_VERDICT.md`, 2026-08-22. The candidate ran
**once**, on data it had never seen: 124 odd-line curated items plus 238 wild units from
fresh-seed chains (seed 20260823). No reruns; the held-out samples are spent.

| criterion | measured | bar | verdict |
|---|---|---|---|
| L1 curated accuracy | 0.7177 | ≥ baseline 0.7177 (same items) | PASS (at par) |
| L1 deep-kind accuracy | 0.7083 | ≥ 0.7389 (baseline 0.6389 + 10 pts) | **FAIL by 3.1 points** |
| L2 wild cross-family κ | 0.3488 | ≥ 0.40 (pinned convention) | **FAIL** |
| L3 coverage | 1.000 / 1.000 | ≥ 0.85 | PASS |

Three things a reviewer should take from that table.

1. **The deep-kind improvement is real and roughly half what calibration claimed.** +6.9 points
   held-out against +16.3 on calibration. Tuning overfit about half its gain. The +10 bar was
   frozen in advance and was not met out of sample. It is not being re-litigated.
2. **The wild failure is not a surprise and not a collapse.** Amendment T4 anti-collapse guards
   (≥12 distinct labels emitted, modal label share ≤0.50) both **passed** — 12 labels, modal
   0.447. The pipeline failed honestly rather than by declining to classify. For contrast:
   pattern B posted the campaign's best wild κ (0.3997) by fast-exiting 87.5% of the time with
   curated accuracy 0.312 and deep-kind accuracy 0.004. **κ rewards shrinking the label space.**
   Read L2 jointly with L1 or it can be bought outright.
3. **L2 measures agreement, not validity.** A diagnosed defect — S2 firing Record on any textual
   deletion — *raised* the measured κ (0.3858 with deletion-shaped units, 0.3617 without),
   because all three families agreed on the same wrong label. Two independent prompt repairs were
   tried and both were rejected on measurement: they relocated the error to Premises rather than
   fixing it (13 and 12 items respectively). The defect stands, diagnosed and unfixed, on the
   record.

**What follows for this proposal.** The pipeline is usable as a **curated/validity instrument**
(at-par accuracy, +6.9 deep, full coverage) and as the **design basis** for the agent work. It is
not licensed to produce a wild verdict, and no experiment below stakes one behind it. The series
is data collection and instrument iteration. Any promotion past that requires a fresh held-out
sample at a new seed — held-out data is never reused (`H3ERE2X_PREREG.md` AMENDMENT T1).

### 3.1 One open finding this series inherits

**Removal-of-content has no artifact-local home in the 11+1 at wild grain.** Two independent
prompt repairs relocated deletion items to the same wrong kind. The error is the object's, not
the prompt's. Three candidate resolutions are open (T4 §2): deletions are Record-axis traffic;
a candidate REMOVAL kind (bounty-class, needs the standing two-witness bar); or deletions are
out of scope for a taxonomy of content-variations. Notably, CEG's `withdraws` lands on Record
3/3 in every alignment run — the deployed grammar already homes removals there. **The agent
stream is an unusually good instrument for this question**, because agent-side removals are
governed acts with an emitting verb attached, not diffs to be guessed at.

---

## 4. SHADOW MODE — the deployment design

### 4.1 The design

H3ERE2 runs **alongside** H3ERE, on the same traffic, at the same step points. It reads what
H3ERE reads. **It never acts.** Its output is a REG decomposition — kind, verb, confidence,
route telemetry, and the S2 posterior over "which deep kind wears this surface" — written to the
event log and to nothing else. No handler dispatch, no conscience override, no effect on
`FINALIZE_ACTION`, no path by which a shadow output can reach a user.

**Attachment point.** The pipeline already broadcasts at every step via the `@streaming_step`
decorator (`ciris_engine/logic/processors/core/step_decorators.py:256`; the paired
`@step_point` at `:356`), and
`FSD/TRACE_EVENT_LOG_PERSISTENCE.md` specifies the event-log persistence model that stops the
lens collapsing per-step broadcasts into one final-state row. Shadow H3ERE2 is a **consumer of
that event stream plus an emitter of its own event type**. It requires no change to any
decision path. If the trace event-log FSD is not yet implemented, RS-1 implements the subset it
needs and nothing more. (Implementer's note: that FSD is dated 2026-04-30 and its own
line references have drifted — it cites the decorator at `:194`; it is at `:256` today.)

### 4.2 Why shadow mode is the right instrument, not just the safe one

The programme needs a wild stream whose units are **single-change by construction**. Every wild
instrument tried so far fails on exactly that: raw revision diffs carry multiple changes per link
and the panel splinters on which one to classify (`LEGC_RESULTS.md`, five runs, all VOID on
agreement). The **block-scoped agent stream** — governed changes with a declared scope and an
emitting verb — is single-change by construction, and it has been the named successor instrument
across three separate documents (`LEGC_RESULTS.md`, `VALIDATION_VERDICT.md`,
`ATLAS_UNIV1_PREREG.md`). Shadow mode is how we get it.

So the safety story and the science story are the same design: shadow mode acts on nothing, and
acting on nothing is precisely what makes the stream a clean measurement.

### 4.3 The REG constraint, verbatim and binding

From `REG_SPEC.md`, the grammar's own founding statement:

> REG is a RESEARCH INSTRUMENT — the lab-frame grammar. It deliberately removes CEG's
> anti-attack defenses so the attack sector becomes measurable. **IT MUST NEVER BE DEPLOYED AS
> TRUST INFRASTRUCTURE**; CEG's flatness exists because attacks exist. The pair is the
> experiment: REG measures what CEG suppresses.

And from `H3ERE2_NOTE.md`, the fence on this exact application:

> REG remains lab-frame — H3ERE2 uses REG's MAP (the object + measured channels), not
> REG-as-trust-infrastructure.

This is not a caution to be weighed against convenience. It has a derivation. `REG_A2A.md` §6.1
proves the **erasure theorem**: a readout is erasure-resistant *if and only if* its aggregation
monoid has no invertible elements. REG's value layer is `(C, +)`, a group — so an adversary
erases arbitrary honest standing by emitting the inverse, and ownership constraints have
**zero shadow on the readout** because the readout factors through the sum. §6.2 adds the cheaper
dual: `N` colluding attesters emitting in phase produce `|Σ|² = N²` against `M` dispersed honest
attesters' `E|Σ|² = M`, so **manufacture is quadratically cheaper than erasure**, and the reward
is largest exactly on contested subjects where the verdict matters. A REG readout is not a
hardened CEG; it is a grammar with two proved attacks in it, kept in the lab on purpose.

**Concretely, for anyone implementing RS-1:** shadow H3ERE2 may write REG terms into the trace
event log as *research telemetry*. It may not write them into the attestation graph, may not
influence admission, standing, delegation, or any consumer-visible verdict, and may not be
exposed through any endpoint that a federation peer reads as trust signal.

### 4.4 Data handling

The shadow stream contains agent traffic. The series inherits whatever consent, retention and
redaction regime the agent's trace persistence already carries; it introduces no new collection.
One programme-specific hazard is worth naming because it has bitten before: a redaction/scrub
pass is not a control until it is adversarially probed — a regex ban-list in an earlier campaign
leaked at AUC 0.88, with the redaction marker itself as the second-strongest cue. If any scrub
is applied to shadow records, it gets a probe, not an assurance.

---

## 5. The series

Five experiments. Each names its promotion gate; each gate takes down its own experiment and
nothing beneath it. **No gate below authorizes replacing live evaluation.** The furthest any of
them reaches is "this instrument is licensed to produce a reading".

### RS-1 — shadow harness and instrument license

**Build:** the shadow consumer/emitter of §4.1, plus a REG-decomposition event type. Run
H3ERE2 (frozen v2, sha `523fd6d0c45cd50e`, unmodified) over the block-scoped agent stream.

**Measure:** coverage; label distribution; route telemetry (fast / recurse-pass /
retry-rejected / retry-pass); cost and added latency (shadow is off the critical path, so
latency is a resource question, not a UX one); and the anti-collapse guards.

**Promotion gate (staked before any run):**
- G1 coverage ≥ 0.85.
- G2 anti-collapse: ≥ 12 distinct labels, modal share ≤ 0.50 (T4 convention).
- G3 a **human-anchored subset** of ≥ 100 units, labelled from definitions by ≥ 2 humans,
  against which pipeline accuracy is reported. The human ladder rung is 0.831 (§6); the gate
  is that this number is *measured and reported*, not that it clears a bar — RS-1 is a license
  for the harness, not for the classifier.
- **Kill:** coverage below floor, or the guards fire → the harness is not producing a readable
  stream and RS-2..RS-5 do not run.

**What RS-1 does NOT do:** it does not license a wild κ reading. The held-out verdict already
says this architecture class does not clear 0.40 on wild traffic, and the agent stream is a
*different substrate*, not a retry on the same one.

### RS-2 — the DMA-consolidation comparison

**Question:** does one forced-comparison surface call reproduce what the parallel DMA fan-out
plus ASPDMA produce, on the traffic where the surface four live?

**Design:** for each shadowed thought, record (a) the existing DMA/ASPDMA outputs, (b) H3ERE2's
S1 surface reading and ternary verdict, (c) whether the gate would have fast-exited. Compare on
**agreement with the finalized action's own kind attribution**, on the gate-cleared subset and
the gate-declined subset separately. Cost is a reported term, not a criterion.

**Promotion gate:**
- Agreement between S1's reading and the fan-out's on the gate-cleared subset ≥ the
  fan-out's own cross-DMA agreement on that same subset, **and** the gate-declined subset shows
  strictly *lower* agreement (i.e. the gate is selecting the hard cases, not selecting at random).
- **Kill:** the gate-declined subset is no harder than the cleared subset → the gate is not
  triaging, the consolidation hypothesis has no support on this stream, and the DMA-consolidation
  line closes for this series.

**Honest expectation.** The gate fired 4.8% on deep-loaded curated data and 20.0% on wild
revision traffic. Agent traffic is a third substrate and its rate is unknown. If it fires near
zero, RS-2 reads null for lack of a triage split rather than against the hypothesis, and that
is the reading we will publish.

### RS-3 — conscience re-anchored on the +1 and mutations

**Question:** does the deletion residual (§3.1) resolve on a stream where removals are *governed
acts with a verb* rather than diffs to be inferred?

**Design:** S3's verification prompt is re-anchored, in shadow only, to two things it currently
handles badly: **Record** (the +1 — a claim about whether an event can still be established, not
about whether a document still contains a paragraph) and **mutations** (removal, replacement,
withdrawal). The agent's own emitted verb is available as ground truth for the *act*, which the
wild corpora never had. `withdraw → Record` was 9/9 and `authorize → Rules` 6/6 in the X read;
CEG's `withdraws → Record` is 3/3 across every alignment run.

**Promotion gate:**
- On removal-shaped units with a known emitting verb, the pipeline's kind assignment agrees with
  the verb-implied kind at a rate reported against a permutation floor, with the human-anchored
  subset as the validity check.
- **Kill:** the same relocation pattern reappears (removals scattering across Record / Premises /
  Facts / Structure at rates indistinguishable from the wild corpora) → the residual is confirmed
  as the object's, not the instrument's, and it escalates to the bounty machinery as a
  candidate taxonomy revision. **This kill is a result, not a failure**, and it is the
  world→model lane doing its job.

### RS-4 — the transition matrix from carries-inversion telemetry

**Question:** what does the 11(+1) × 11(+1) transition matrix look like on the agent stream?

**Design:** the S2 posterior over "which deep kind wears this surface here" *is* an estimate of a
mixing-matrix column — it is fit, not labelled, and it falls out of the classifier doing its
ordinary job. Accumulate it. Read out the five FD structure tests staked in `REG_SPEC.md`:
FD1 normalization, FD2 hierarchy, FD3 localization, FD4 phase sector, FD5 factorization.

**Promotion gate:**
- The matrix is read **only if** RS-1's gates hold on the accumulating stream and the estimator's
  own permutation null is computed alongside. Row-stochasticity is **not** evidence of
  conservation — confusion matrices are row-stochastic by construction, which is exactly why P1
  is currently scored NOT EARNED (`OBJ2_P_SCORING.md`).
- **Kill:** the matrix fails RS-1's gates on the accumulated sample → no FD reading, reported as
  unread.

**Fence, binding:** no FD verdict may be read behind an unlicensed pipeline
(`H3ERE2_NOTE.md` dependency chain). RS-4 produces a matrix and its nulls; whether it produces a
*verdict* depends on a license this series does not assume it will get.

### RS-5 — the bridge stakes

The agent stream is a **named instrument** for all three lattice-law bridge stakes frozen in
`BRIDGE_STAKES.md` (2026-08-22, before any corpus test). Each stake is separable; each kills only
its own P-claim.

| stake | what the agent stream measures | kill |
|---|---|---|
| **BS-1** (earns P1) | conservation in **carries-closed segments** — chains whose inflow and outflow are fully observed. Governed agent changes are unusually likely to be closed in this sense, which is why the stream is named for it. Measure sector totals along chains; compare leakage against an open-system null. | leakage statistically indistinguishable from the open-system null → conservation is bookkeeping, P1 stays unearned, stake dies. |
| **BS-2** (earns P3+P5 jointly) | the **even-harmonic route law**: closed loops (A→B→A and longer) should show reversal-symmetric statistics with odd-harmonic power at floor, while open transfer chains show measurable chirality. | odd-harmonic power in closed-loop statistics above the matched floor, or reversal-asymmetric returns → the transport law is lattice-only, stake dies. |
| **BS-3** (sharpens P5) | **loop-dependence, not mere order-dependence**: closed loops differing only in traversal direction should agree; open routes should differ. | direction-dependent closed loops at measured power → the symmetrization is not in the corpus, the sharpening dies. Babel's plain order-dependence result stands on its own either way. |

**Disclosure carried forward from `BRIDGE_STAKES.md`:** babel2's ij/ji pair items are a
ready-made BS-3 instrument but their judgments are **already sealed data**. Any babel2 reading
under BS-3 is EXPLORATORY, labelled as such, with no evidential weight. The stake cashes only on
a fresh stream — which is what RS-5 is for.

**The anti-laundering control we get for free.** CEG's deployed wire format is **modulus-only**;
phase is never representable (the sealed no-go, `CEG_REPRESENTATION.md` / `REG_A2A.md` §0). So
any phase-like signature found in agent-stream routes **cannot have been injected by the carrier
format** — the instrument is provably blind to the quantity it would be accused of manufacturing.
That blindness is the control that makes a BS-2/BS-3 reading worth taking.

---

## 6. The instrument ladder — calibrate before you read any number

Every agreement number in this programme sits somewhere on a measured ladder. Reviewers who do
not know the ladder will mis-read the series' outputs in both directions.

| substrate / instrument | κ | source |
|---|---|---|
| raw wild revision diffs, multi-change links | **0.247 – 0.295** | `LEGC_RESULTS.md` runs 1–2 |
| wild single-change units, licensed panel | **0.3488 – 0.386** | held-out 0.3488, calibration 0.386, sealed 0.355 |
| authored vignettes | **0.47** | campaign ladder, `LEGC_RESULTS.md` |
| curated single-span items, standing panel | **0.687** | PLANE study |
| curated single-span items, PANEL-2 (licensed stronger) | **0.711** | PANEL-2 license |
| **humans, labelling from definitions** | **0.831** | the human-anchor result |

**The load-bearing fact: the wild ceiling is substrate-intrinsic, not panel-strength-limited.**
Two independent three-family panels — one standing (0.687 curated), one licensed-stronger (0.711
curated) — both collapse to 0.29–0.36 on wild units. A third instrument (H3ERE2, built
specifically to break the ceiling by decomposing the mixture) reads 0.3488. That is now
**three independent wild samples clustering at ~0.35 across two panels and a recursive
pipeline**, with no label collapse. Wild changes are genuinely ambiguous mixtures at single-pass
grain.

Two consequences for how this series should be read:

1. **Do not expect the agent stream to read 0.687.** If it lands anywhere above ~0.40 that is
   already a substantive finding about the substrate — it would mean block-scoped governed
   changes are meaningfully less ambiguous than wild diffs, which is the whole premise of naming
   the stream as a successor instrument.
2. **Humans at 0.831 are the standing reason the human-label route is not closed.** The
   held-out verdict names *either* the human-label route *or* the block-scoped agent stream as
   the wild leg's instrument. This proposal pursues the second. It does not claim the second
   supersedes the first, and RS-1's G3 keeps a human anchor in every experiment.

---

## 7. What this proposal explicitly does not ask for

- **Not** replacing H3ERE's live evaluation stages. The candidate failed its license; §2.3 says
  why the validation would not transfer even if it had passed.
- **Not** deploying REG as trust infrastructure, in any form, anywhere, ever (§4.3).
- **Not** an FD verdict, a P-score, or a bridge-stake cash-out on this series' first data. Those
  require licenses this series is designed to *earn or fail*, not to assume.
- **Not** reuse of any held-out sample. New validation requires a new seed.

## 8. What a reviewer should push back on

Stated here so it does not have to be discovered:

1. **The DMA-consolidation hypothesis is the weakest link.** It is a design inheritance from a
   classifier validated on a different object. RS-2's kill is real and I expect it to be a live
   possibility.
2. **The gate may not fire on agent traffic.** Two measured rates, 4.8% and 20.0%, on two
   substrates neither of which is this one.
3. **κ on the agent stream may be uninterpretable** if block-scoped changes turn out to be
   dominated by one kind — the wild revision stream was 79/135 Manner out-degree, and a
   single-kind stream cannot exercise a transition matrix. RS-1's label distribution is the
   early warning.
4. **Shadow mode has a cost.** Doubling evaluation calls on live traffic is a real budget line,
   and the research programme's own tuning ran against a $3.50 fence. The series needs its own
   fence, set by whoever owns the agent's inference budget, before RS-1 runs.
