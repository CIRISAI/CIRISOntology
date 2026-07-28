# EVALUATION METHODOLOGY — claims about H3ERE reasoning traces

**What this is.** A port of this repository's gate registry (`GATES.md`, 13 reaches + 23 harvest
rows) and its governing rules (`epistemology.md`, L1–L8) to a different measurement problem:
**claims that CIRIS H3ERE reasoning traces do or do not differ by model, language, context, or
change.**

**What this is not.** It is not a proposal to measure the whole-only share of anything in the
pipeline. §A says why, first and without hedging, because that is the mistake this document most
needs to prevent.

**Provenance of the pipeline description.** §0 is read from source in `/home/emoore/CIRISAgent`,
`/home/emoore/RATCHET` and `/home/emoore/CIRISConstitution`, all read-only. Every line is marked
**[read]** (I opened the file and the statement is in it) or **[inferred]** (a consequence I drew
that nobody wrote down). Nothing in `Stance.lean`, no Lean file, no audit; `lake` was never
invoked; nothing pushed.

**Scope limit, stated before anything else.** This document governs **method**. It contains no
measurement, licenses no finding, and is not evidence that any trace comparison has ever been
done correctly. It is a checklist earned by other people's failures, and every gate below carries
the specific failure that earned it, because a gate without its incident is advice.

---

## A. WHAT DOES NOT TRANSFER

### A.1 The whole-only share is not a deception detector, and must not be built into a trace metric

This repository's central measured quantity — the whole-only (order-3, pairwise-blind) share —
**does not detect deception, and we know that by having tried.**

**The negative, with its controls.** Two detectors were built and run on a capable model's own
validated deception: a model that competently lied about **45 %** of the time. Both came back
empty. The whole-only surplus and the pairwise consistency-load were **both about zero**, and each
had a **firing control** — `z = −306` and `z = +32` — so these are validated negatives, not blind
instruments returning silence. Source: `CIRISOntology/Stance.lean`, claim `ai-safety`, fields
`plain`, `kill` and `confidence`.

*(W2 note on that citation: the Stance's own fields disagree about the model size — `plain` says
"a 7B model", `kill` and `confidence` say "8B". The disagreement does not touch the result. It is
flagged here rather than smoothed over, and is a live warrant-reach instance in the published
text.)*

**And the mechanism says the failure was predictable.** The pump campaign measured the rate law
for how whole-only share is created (`PUMP_RESULTS.md`, headline):

> `share = 18·r₀⁴·a² / [(1+2r₀)(1+3r₀)(1−r₀)] + O(a⁴)`, with `r₀ = (1−2s)²·ρ`

confirmed against the exact solver to 3 parts in 10⁴ over 61 gauged configurations. Read it as a
sentence: **wherever there is maintained pair correlation `ρ` and per-cell noise with any
asymmetry `a`, whole-only share is manufactured out of nothing but those two ingredients.** That
is a description of every trained network, and of every trace corpus emitted by one. The quantity
therefore has a **high base rate in the target class**, which is the opposite of what a detector
needs.

**And the floor is large and measured.** The sky campaign measured the valve floor at **50 % to
5.8×** of the null, depending on scale (`GATES.md`, *valve floor*, `36874ed`). A whole-only
reading on traces is signal **plus** that floor, and the floor moves with sampling density — which
in a trace corpus is set by chain length, retry count and seal rate, all of which differ by
condition.

**The standing rule this yields, stated so it cannot be re-proposed in good faith:**

> A whole-only / order-3 / synergy / O-information reading is **not** admissible as evidence that
> a trace is deceptive, misaligned, or of lower integrity. It has no measured discriminative power
> for that question, it has a large manufactured floor, and it is generic in the class of systems
> being tested. Proposing it requires first refuting the two validated negatives and the rate law
> above, on the record, with a firing control.

**What DOES transfer is the null-and-control discipline, not the estimator.** Everything in §C is
estimator-agnostic: it applies to a mean, a rate, a rank test, a PCA eigenvalue spectrum, an LLM
judge score. That is the point of porting it.

### A.2 No result in this repository licenses any claim about reasoning QUALITY

Nothing measured here — not the share, not the rent clause, not `N_eff`, not the valve — is a
measurement of whether reasoning is **good**, **sound**, **honest**, or **well-aligned**. The
proved results are about probability distributions on three binary slots. The measured results are
about physical and simulated substrates. The wagers are wagers.

A trace metric may legitimately measure *whether a step fired*, *how long it took*, *what it
selected*, *how variable it is*. Whether the reasoning was **good** is a separate claim requiring
its own ground truth, its own kill and its own gates, and this repository supplies none of them.

### A.3 Gates from the registry that do not apply, named rather than padded

| registry gate | why it does not transfer |
|---|---|
| delocalisation correction; patch isotropy; dispersion sweep | survey-geometry specific (masked fields, sky patches, Poisson catalogues). No trace analogue. |
| catastrophic cancellation in alternating sums | applies to Krawtchouk-style estimators. Not used on traces. |
| solver / relaxation gap (IPF vs dual bracket) | applies only if someone runs a maxent solve on trace tables. §A.1 removes the main reason to. Keep it filed against the day someone does. |
| coarse-graining / binarization minting | applies **only** if continuous trace scores are binned. If you bin `coherence_score`, it applies in full and the b-ladder must be swept. If you compare categorical action types, `b` is fixed by the schema and there is nothing to mint. |
| zero-cell roundoff | weak analogue only: sparse categorical tables over 10 handlers × N conditions. State the floor if you compute an entropy over a mostly-empty table. |
| equilibration diagnostics can be blind | **[inferred]** the analogue is drift across `trial_index` within a run, which RATCHET lists as exploratory (`PRE_REGISTRATION.md` §11). No anchor exists in either record. Marked as a hypothesis about a gate, not a gate. |

---

## 0. THE PIPELINE, AS ACTUALLY READ

This section exists so §B and §C are about the real object. Where the sources did not settle
something, it says so instead of inventing a stage.

### 0.1 The stages

**[read]** `ciris_engine/schemas/services/runtime_control.py:102`, `class StepPoint(str, Enum)` —
"Points where single-stepping can pause in the H3ERE pipeline":

`START_ROUND` → `GATHER_CONTEXT` → `PERFORM_DMAS` → `PERFORM_ASPDMA` → `CONSCIENCE_EXECUTION` →
(`RECURSIVE_ASPDMA` → `RECURSIVE_CONSCIENCE`, optional, on conscience failure) → `FINALIZE_ACTION`
→ `PERFORM_ACTION` → `ACTION_COMPLETE` → `ROUND_COMPLETE`.

**[read]** The enum has **11 members**; its own docstring says "10 step points (0 setup + 7 core +
2 optional recursive)". The counts disagree. This is trivial and it is also exactly the
named-denominator hazard in miniature: *"the pipeline has N stages"* is not a well-formed
statement until N names its enumeration.

**[read]** `CONTRIBUTING.md` §"H3ERE Architecture Overview": 4 DMAs (PDMA, CSDMA, DSDMA + recursive
ASPDMA), **10 handlers** in a 3×3×3+1 structure (SPEAK/TOOL/OBSERVE · MEMORIZE/RECALL/FORGET ·
REJECT/PONDER/DEFER · TASK_COMPLETE), 6 message buses, 22 core services.

### 0.2 Where traces are emitted, and what a trace is

**[read]** `FSD/TRACE_EVENT_LOG_PERSISTENCE.md` §1: the pipeline broadcasts at every step via the
`@streaming_step` decorator (`ciris_engine/logic/processors/core/step_decorators.py:194`).

**[read]** `ciris_engine/schemas/services/runtime_control.py`, `class ReasoningEvent`: the event
types are `THOUGHT_START`, `SNAPSHOT_AND_CONTEXT`, `DMA_RESULTS`, `IDMA_RESULT`, `ASPDMA_RESULT`,
`TSASPDMA_RESULT` (deprecated), `VERB_SECOND_PASS_RESULT`, `CONSCIENCE_RESULT`, `ACTION_RESULT`,
`LLM_CALL`. **10 members; the docstring says "9 result events".** Same hazard as above.

**[read]** `FSD/TRACE_WIRE_FORMAT.md` §3 — the shipped unit is a **`CompleteTrace`**:
`trace_id`, `thought_id`, `task_id`, `agent_id_hash`, `started_at`, `completed_at`, `trace_level ∈
{generic, detailed, full_traces}`, `trace_schema_version`, `deployment_profile` (6 operator-declared
cohort fields), `components[]` in receipt order, and an Ed25519 `signature`.

**[read]** §3, `completed_at`: *"A trace is only sealed and shipped when `ACTION_RESULT` fires — no
action means it never happened."* **This is the single most important fact in this document for
§C.3.**

**[read]** §5.2 / §2 of the persistence FSD: the lens **collapses all broadcasts for one thought
into one row**, persisting the post-retry final state. DMA bounces (N alternatives per low-scoring
DMA), conscience overrides, up to 5 recursive ASPDMA retries, up to 5 recursive conscience
re-validations, and per-call LLM detail are all **lost** except the last write; only the cost
counters (`llm_calls`, `tokens`, `cost_usd`) survive because they sum.

### 0.3 What a trace comparison concretely operates on

Four distinct data layers, and a claim must say which it is about:

| layer | content | source |
|---|---|---|
| **per-trace scalar vector** | the 16-field projection: 6 continuous core (`csdma_plausibility_score`, `dsdma_domain_alignment`, `coherence_level`, `entropy_level`, `idma_k_eff`, `idma_correlation_risk`), 2 boolean core (`conscience_passed`, `action_was_overridden`), 4 **conditional** continuous (`entropy_score`, `coherence_score`, `optimization_veto_entropy_ratio`, `epistemic_humility_certainty`), 4 conditional boolean | **[read]** `RATCHET/experiments/exp1_multimodel_neff/phase0_smoke_analyze.py:44` (`PROJECTION_16`, `CORE_FIELDS`, `PATHS`) |
| **per-trace event sequence** | ordered `components[]`, step timings, retry structure | **[read]** wire format §3–§4 |
| **per-trace text** | rationales, reasoning summaries, prompts (`aspdma_prompt`, `entropy_prompt`, …) — present at higher `trace_level` | **[read]** `runtime_control.py`, `ConscienceExecutionStepData`, `FinalizeActionStepData` |
| **per-trace telemetry** | `tokens_total/input/output`, `cost_cents`, `energy_mwh`, `llm_calls`, `models_used`, `execution_time_ms` | **[read]** `ActionCompleteStepData` |

**[read]** RATCHET's `N_eff` is a per-chain PCA over the 16-dim projection, requiring ≥ 3 thoughts
per chain (`PRE_REGISTRATION.md` §10.1, §12).

### 0.4 What varies between runs

| axis | how it varies | source |
|---|---|---|
| **model** | one foundation model per run via OpenRouter; `models_used` recorded per trace | **[read]** `PRE_REGISTRATION.md` §5, §7 |
| **language** | `model_eval` fires every (question × language) pair into its own channel `model_eval_{code}_{qq}`, under a per-locale user account; 29 locales in `LANGUAGE_SPECS` | **[read]** `tools/qa_runner/modules/model_eval_tests.py:133–173` (`LANGUAGE_SPECS`), `:292`, `:361–365`, `:397` |
| **question / task** | in-tree default set is 4 questions, deliberately generic; sensitive sets are out-of-tree JSON via `--model-eval-questions-file` | **[read]** same file, `EVAL_QUESTIONS` comment block |
| **configuration** | `trace_level`, `deployment_profile` (6 fields), concurrency, `CIRIS_DISABLE_TASK_APPEND`, agent template/role | **[read]** wire format §3.2; `PRE_REGISTRATION.md` A2/A3 |
| **version** | `trace_schema_version` (2.7.0 vs 2.7.9 shapes differ in where `agent_id_hash` lives) | **[read]** wire format §3.1 |

### 0.5 The one prior trace-comparison campaign, and how it went

**[read]** RATCHET Exp 1 (`experiments/exp1_multimodel_neff/`) pre-registered "is `N_eff ≈ 7.1` a
property of the CIRIS constraint topology or of the underlying model?" with a locked decision rule
(K = number of models whose 95 % bootstrap CI ⊆ `[6.6, 7.6]`; K=5 PASS, K∈{3,4} PARTIAL, K≤2 FAIL),
locked n, no early stopping, no post-hoc outlier rules, and analysis-stage label blinding.

**[read]** Phase 1 (run `25935989178`) returned **INDETERMINATE** (Opus cell aborted at n=0). The
four populated models clustered at `N_eff ∈ [4.5, 6.6]`, below the window. Amendment A4's
diagnosis: the four **conditional** conscience fields populate *only when the reasoning encounters
boundary tension*. Chains where the base model is already aligned short-circuit the faculty
cascade, contribute no conditional fields, and pull the mean toward an **inactive floor**.
Formalized as `RATCHET.Experiments.BoundaryObservability` BO-1…BO-4.

**This is an occupancy failure — our reach 11 — already fired, in the target pipeline, found by
that team.** Every gate below inherits credibility from it: the failure mode is not imported, it
is native.

### 0.6 What the Constitution requires, and why most of it is not a statistical question

**[read]** `CIRISConstitution/constitution/part_1_foundation.md` §1.3 (`pdma`) makes the layer
ruling explicit: the PDMA (including the Order-Maximisation Veto) is **agent reasoning**, and the
fabric's only role is **attestation** — *"it records, and lets others verify, that the PDMA
(including the Veto check) was executed"*. The same section carries a Public Transparency rule:
deployments above 100 000 MAU must publish or API-expose redacted PDMA logs and WBD tickets within
180 days, and *"absence of publication voids any claim of CIRIS compliance."*

**[inferred, but directly]** Therefore most constitutional claims about traces are **verification**
claims, not statistical ones: did the step fire, is the audit hash chain intact, is the signature
valid, is the ticket present. Those are checked by inspection of every trace, not by a test against
a null. Treating a verification requirement as a statistical one — "conscience fired in 97 % of
traces, which is high" — is a category error that converts a *requirement* into a *finding*.

Where a constitutional question **is** statistical (e.g. "does the deferral rate differ between
languages in a way the Constitution's fairness commitments would care about"), it is a difference
claim and lands back in §B.

---

## B. THE CLAIM TYPES, AND WHAT THE NULL ACTUALLY IS

Five types. For each: the claim, the null, and the thing most likely to be mistaken for the null.

### B.1 "Traces differ between model A and model B"

**Null.** Trace-level assignment of the model label is exchangeable: the observed statistic is
compared against its distribution over **random reassignment of the model label to whole traces**,
preserving each trace's internal structure and preserving the (question × language × config) cell
composition of each arm.

**The trap.** A permutation over *traces pooled across cells* also permutes question and language,
so it tests "are these two sets of traces identical in any respect", not "does the model matter".
That is exactly the invalid permutation test `WATER_RESULTS.md` §3.3 caught: permuting two
ensembles that differ in composition builds two near-identical mixtures, so **any** real difference
looks extreme — it returned `p = 0.0005` against a bootstrap `z = +0.65`, and *"would have inverted
this document's verdict if taken at face value."* **Permute within cell, or state that you did not.**

**The second trap.** Models differ in how often they *emit* the conditional fields (§0.5). A
null that permutes labels but not missingness patterns cannot manufacture the missingness
difference, so a statistic sensitive to missingness will always look significant. Either the
statistic must be missingness-invariant, or the missingness rate is the finding and must be
reported as such.

### B.2 "Traces differ between languages"

**Null.** Same shape: permute the language label within (model × question × configuration).

**The trap, and it is specific and verified.** Language is **not** a clean treatment in the current
harness. `model_eval_tests.py:565–573`: if a native translation exists for that (question,
language), the agent receives the native text with **no wrapper**; otherwise it receives the
**English question with a language-directive prefix**. In the in-tree default set, 3 of 4 questions
carry translations, for exactly `{am, es, zh}`; the 4th carries none. So for the default
language list `["am","zh","en","es"]` the non-English arms are native-treatment on 3 of 4 questions
and wrapper-treatment on 1; for any of the other 25 locales in `LANGUAGE_SPECS` it is wrapper on
4 of 4.

The code comment states the consequence in the pipeline's own words: the wrapper *"creates an
artificial language mismatch that IRIS-C correctly flags as incoherent."* **A measured coherence
difference by language is, until proven otherwise, a measured translation-coverage difference.**

**A third, already-fired confound.** `LOCALE_USERS` (lines 39–52) and its comment: adding a locale
to `LANGUAGE_SPECS` without adding it there makes that locale's cells fall back to the admin
username — the recorded incident is the agent addressing Chinese- and Spanish-channel users as
"Jeff". Persona-fit is part of what a coherence metric reads.

### B.3 "Traces differ between contexts / configurations"

**Null.** Permute the configuration label across otherwise-matched runs. But **`trace_level` is not
a condition, it is an instrument setting**: `generic`, `detailed` and `full_traces` change what the
trace *contains* (wire format §3). Comparing across trace levels compares two instruments and is
**ungauged**, not a null result and not a difference.

**The trap.** `deployment_profile` fields are **agent-declared** (wire format §3.2), free-form for
`agent_role`. Grouping by a self-declared label and finding differences between groups is a claim
about labelling practice until the labels are shown to be independent of the outcome.

### B.4 "Traces differ before and after a change"

**Null.** The hardest of the five, because there is no simultaneous control arm. The only honest
nulls are (a) a **pre-period-only split** — divide the pre-change traces into two halves at a
random cut and measure the same statistic, giving the drift floor; and (b) an **unchanged-cell
control** — a subset of (question × language) cells the change provably cannot touch, which must
read null.

**The trap.** `trace_schema_version` changes, question-set rotation ("the corpus rotates as
attractor patterns evolve" — `model_eval_tests.py`, `EVAL_QUESTIONS` comment), and model-provider
drift all co-occur with deliberate changes. A before/after comparison with no unchanged-cell
control cannot separate them, and should say **ungauged**.

### B.5 "This agent's traces satisfy constitutional requirement X"

**There is usually no null, because this is usually not a statistical claim** (§0.6). The correct
form is a verification over the whole corpus with the exception count reported: *"N traces
examined, M lack a valid `audit_entry_hash`, here they are."* A p-value here is a category error.

**Where it is statistical**, it reduces to B.1–B.4 and inherits their nulls — plus one extra
requirement: the constitutional predicate must be **stated as an operational test before the
traces are read**, or the claim is a post-hoc reading of a document against data.

---

## C. THE GATE PORT

Each gate: the rule in trace terms · the **known-bad anchor** (our record, with the number) · the
**dye test** (the planted signal it must catch, or its verdicts are void) · its **depth**.

Ordering is by how much damage the gate has prevented elsewhere, not by convenience.

---

### C.1 Selection geometry — overlapping spans manufacture differences

**Rule.** If the units being compared **share material**, the comparison manufactures structure
from the sharing alone. In trace terms the shared material is: (a) follow-up thoughts inherit their
parent's task and context, so two "independent" traces from one task overlap; (b) `GATHER_CONTEXT`
pulls overlapping memory/graph state across traces in a session; (c) sliding windows over a step
sequence share steps; (d) the same question fired at 17 trials shares its prompt exactly. **Declare
the overlap geometry before the run, and run one arm at zero overlap.**

**Known-bad anchor.** `WATER_RESULTS.md` §3.4: at a compact template the three slots' cutoff
spheres share a common intersection, so a single particle is counted by all three labels at once —
a three-body coupling written in **by the filter**, from positions with no three-body physics.
Beyond `2 r_cut`, where no three spheres share a point, **the minting vanishes by a factor of
13 000**, and that was an **advance prediction**, confirmed. The far arm reads at floor at every
state point and on the ideal gas too.

**Dye test.** Two arms identical in every respect except overlap: (i) one trace per task vs (ii)
all traces including follow-ups from the same task. Plant **zero** true difference between
conditions. The gate must report the manufactured difference and its size. Then plant a small real
difference and show it survives at zero overlap.

**Depth.** Reads on any unit-of-analysis question. **Out of its depth** when the overlap cannot be
switched off — e.g. if every trace in the corpus is a follow-up. Then the reading is **ungauged**,
not clean.

---

### C.2 The structureless-input control

**Rule.** Push a **structureless corpus** through the byte-identical analysis: traces synthesised
by drawing each projection field iid from the pooled marginal, matched on chain length, event-type
counts, vocabulary size and token counts, with the condition labels assigned at random. Whatever it
reads is the pedestal. **Pre-register the void rule: pedestal ≥ 50 % of the reading ⇒ that cell is
VOID.**

**Known-bad anchor.** `WATER_RESULTS.md` §3.2: an **ideal gas** — a structureless Poisson point
process — pushed through the same template selection and the same coordination filter read
**1.61 × 10⁻⁴ nats, twenty-two times more than the real three-body liquid** (7.27 × 10⁻⁶), and more
than **any** reading in that campaign. It read 53× its own floor where the data read 15× its own.
By the campaign's own pre-registered rule, the primary reading is **VOID**; the pedestal is 2 200 %
of it.

**Dye test.** The control must read null on structureless input **and** must move when a difference
of the size that matters is planted into the synthetic corpus. A control that cannot see the dye
returns **ungauged**, not clean (`GATES.md` reach 13; `WATER_RESULTS.md` §7.4 discloses exactly
this gap on its own N3 null).

**Depth.** Reads on any statistic computed over trace fields. **Out of its depth** on statistics
over free text, where "matched on vocabulary" is not a well-defined synthesis — there, say so and
use a shuffled-text control with its own separate dye test.

---

### C.3 Survivorship — the corpus is a filtered corpus (TRACE-NATIVE, new)

**Rule.** **A trace is sealed and shipped only when `ACTION_RESULT` fires.** Every comparison
therefore runs on survivors. **Report the seal rate per arm before any statistic**, and treat a
seal-rate difference as a finding in its own right, not as a nuisance.

**Known-bad anchor — from the pipeline's own record, not ours.**
`FSD/TRACE_EVENT_LOG_PERSISTENCE.md` §2, the Spanish Mental Health case (thought
`th_seed_af724b5d_338cffac-b94`, channel `model_eval_es_06`): three `EthicalPDMA` calls timed out
(90 s, 90 s, 150 s+) and the cell hit `httpx.ReadTimeout` at 600 s wall. **Conscience activity for
this thought: zero — PDMA never produced a result for it to evaluate.** Same model, same ~32 666-char
prompt, same backend; the question content alone triggered the slowdown. That trace never reaches
`ACTION_RESULT`, so it is **not in the corpus** — and its absence is correlated with language and
with question content, which are exactly the variables under test.

Second anchor, same family: RATCHET Exp 1's Opus cell returned **n = 0** and the run was declared
INDETERMINATE rather than analysed on four models (`PRE_REGISTRATION.md` §7 catastrophic-failure
clause, A4). That is the correct handling and it is the standard here.

**Dye test.** Plant a differential seal failure: drop 10 % of one arm's traces, selected on a field
correlated with the outcome. The gate must report the seal-rate difference; the headline statistic
must be re-read on the seal-matched subset.

**Depth.** Reads on every claim in §B. **Out of its depth** on the *content* of unsealed traces,
which by construction is not in the corpus — the honest statement about them is a count and a
reason, never an estimate.

---

### C.4 Named denominators — and beware trends that reverse

**Rule.** Every "X % of ceiling" and every normalised trend names its denominator **and reports at
least two**: a **universal** denominator that cannot move between arms, and the **achievable**
per-arm ceiling. Different models and different languages have different achievable ceilings —
different numbers of populated projection dimensions, different token budgets, different action
repertoires actually reachable. **A trend claim is incomplete without its denominator, because the
two denominators can disagree about whether the trend exists at all.**

**Known-bad anchor.** `GLASS_RESULTS.md` §2.2: at `r = 1.30` the share **grows ×2.41 on cooling**
against the universal cap `ln 2`, and is **FLAT** against the sharp per-table ceiling — 1.95 %,
2.15 %, 2.00 %, 2.31 %, a span of 1.18 — **because the ceiling itself doubles on cooling**
(0.115 → 0.235). Same data, same instrument, two denominators, two opposite answers to "does it
grow". At `r = 1.50` the trend survives but attenuates from ×43.5 to ×5.9.

**The amendment, and it matters here.** `GLASS_RESULTS.md` §2.2b: as a state approaches
independence the sharp cap collapses **below the reading's own floor** and the fraction degenerates
into noise over noise — the theorem-pinned-zero ideal-gas control printed **−1695 %** and
**+1697 %** of ceiling. The registered rule (`GATES.md`, *named-denominator reporting*, as amended):
quote a sharp fraction only where the sharp cap exceeds the reading's own floor by a stated factor
(≥ 100 comfortable); below that, report the universal fraction and the bare cap, and declare the
sharp fraction **undefined**.

**Trace-specific instance, and it is the sharpest one available.** `N_eff` is an effective
dimensionality over a 16-field projection in which **8 fields are conditionally populated**. Its
achievable ceiling is the number of populated dimensions, which **differs by model by
construction** (§0.5). Reporting `N_eff` without the per-arm populated-dimension count is the glass
failure exactly: the reading and its ceiling move together and the trend is partly the ceiling's.

**Dye test.** Plant two arms with an identical *normalised* quantity but a ceiling that doubles in
one arm. The raw metric must show a trend; the correctly normalised one must not. Both must be
reported.

**Depth.** Reads on any ratio, fraction, rate, or dimensionless index. **Out of its depth** where
the achievable ceiling is not computable — then report the raw quantity and say the fraction is
undefined.

---

### C.5 Pair-pinning as a linear program — is the difference already determined?

**Rule.** Before believing that a trace statistic carries information beyond the obvious covariates,
**compute the range it was free to move in given those covariates.** Formulate as an LP: the
statistic is linear (or made linear) in the cell probabilities; the observed marginals over
`chain_length`, `token_count`, `llm_calls`, `selected_action`, `boundary_active` are linear equality
constraints. **If the feasible interval collapses, the statistic was determined before the
condition was consulted.**

**Known-bad anchor.** `KAPPA_EDGE_RESULTS.md` §4: at the array's **published headline point**
(κ = 0.05), every distribution carrying the measured level-8 pair marginals has a b=2 whole-only
share of **exactly 5.0745 × 10⁻² nats** — LP interval width **0.00000**. The measured value was
5.0745 × 10⁻², and the published headline described it as a measured magnitude, "7.3 % of the
machine-checked cap". It was a restatement of the marginals. The headline was re-scoped.

**And the mechanism is not what anyone guessed** (§5, the load-bearing control): a Gaussian triple
carrying **the array's own pair correlations** is *not* pinned — width 0.797 of a possible ~2 — while
a noise-free logistic map is pinned to a point. **The driver is near-determinism of the conditional
support, not coupling strength.** Trace analogue: if `conscience_passed` is a deterministic function
of `coherence_score` crossing a threshold on most of the support, then any three-way statistic over
`(coherence_score, conscience_passed, model)` is a two-way statistic wearing a hat.

**Dye test.** Construct a table whose target statistic is fully determined by the covariates; the LP
must return width 0. Construct one with genuine free room; the LP must return a wide interval. Both
directions, or the gate is one-sided.

**Depth.** Exact and cheap at small alphabets (seconds at b=8). **Out of its depth** near degeneracy,
where the LP is ill-conditioned, and on statistics that are not linear in the cell probabilities
without an approximation whose error is unstated.

---

### C.6 Mixture nulls — cross-model and cross-language comparison IS a mixture question

**Rule.** The null must be able to **manufacture the data's generative structure**. A comparison of
two arms is literally a two-component mixture question, so the null must include **a mixture with no
mechanism in it**: a convex combination of the two arms' own marginals with no interaction, and a
no-dynamics interpolation between the two conditions' endpoint distributions. If a mechanism-free
mixture reproduces the effect, the effect is not evidence of a mechanism.

**Known-bad anchor.** `ECA_SPIKE_RESULTS.md` correction block: the headline was a **1886×** rise in
order-3 under intermediate noise. **A no-dynamics straight line from the deterministic distribution
to uniform reaches 1.9× MORE than rule 58's real sweep** — 6.22 × 10⁻² against 3.31 × 10⁻². The
mixture null ate the headline. Rules 25/46 survived it; **no headline rule passed both this and the
dose check.**

Second anchor, in a *test statistic* rather than a null: `WATER_RESULTS.md` §3.3, above.

**Dye test.** The mixture null must fail to reproduce a planted genuine interaction — plant a
condition-dependent coupling and show the mixture cannot manufacture it — and must succeed in
reproducing a planted pure-composition difference.

**Depth.** Reads on any two-arm comparison. **Out of its depth** where the two arms' marginals cannot
be estimated independently of the effect (small n per cell), which is the occupancy gate's business.

---

### C.7 Floors matched to sample size — traces have different lengths, hence different N

**Rule.** **A floor is drawn at the same sample size as the reading it gauges.** Chain length,
thought count, event count and token count all differ by model and by language; the estimator's
finite-sample floor scales with them. Sub-sample readings get sub-sample floors, and a floor drawn
on the pooled corpus is not a floor for any arm.

**Known-bad anchor.** `DALITZ_RESULTS.md` D2: harsh-acceptance runs read `z ≈ 2.0` against a
**full-sample** floor and looked like a real failure of the design's central protection. The harsh
map also cut the sample from **13 537 to ~2 963**, and the floor scales as 1/N. **With
sample-size-matched floors the rise vanished entirely** — the final table reads z = 0.37, 0.44,
0.70, 0.10 across an acceptance ratio of 1.0 → 15.6.

Second anchor, disclosed rather than absorbed: `WATER_RESULTS.md` §3.1, where `λ = 23.15` carried 201
configurations against 41 everywhere else, its floor is correspondingly 5× lower, and *"its `p` is
not comparable to the others' — this is exactly the Dalitz D2 taint."*

**Dye test.** Take one corpus, split it into two halves of deliberately unequal size with **no** real
difference, and confirm the statistic reads null only when each half is scored against its own
floor.

**Depth.** Reads on every estimator with a finite-sample bias — which is every information-theoretic
quantity, every PCA eigenvalue, and every variance. **Out of its depth** on exactly-computed
quantities with no estimator (a count, a rate over the full corpus).

---

### C.8 Null shape before z — the null is not Gaussian and one draw is not a measurement

**Rule.** **Measure the null's shape before quoting any z.** Report the ratio of its 99th percentile
to its median. Heavy-tailed (χ²-like) nulls are summarised by **p-values against the empirical
distribution**, never by median-and-sigma. And a single draw of a null is not a measurement of it.

**Known-bad anchor.** `DALITZ_RESULTS.md` D7: a **single draw** of the Dye B control appeared to show
the share rising to **2.9 × 10⁻⁴** under a pure-pair injection, which **would have fired kill K2 and
killed the implementation.** Over 200 draws it is flat. The null's measured p99/median ratio is
**9.8** (13.3 under injection) against 14.6 for an exact χ²₁ — heavy right tail. The document's
standing consequence: *"p-values, not z, are the honest summary everywhere."*

Second anchor, the same trap caught on ourselves a campaign later: `WATER_RESULTS.md` §2.4 — one
realisation read 2.0 × 10⁻⁴ (p = 0.045), a second read 6.4 × 10⁻⁵ (p = 0.26). **Two draws, a factor
of three apart.** Redone as a 40-ensemble distribution.

**Dye test.** Draw the null ≥ 200 times and report its shape; then confirm that a planted effect at
the claimed size is recovered at the claimed p over repeated draws, not once.

**Depth.** Reads on every significance statement. No exceptions — the cost is one loop.

---

### C.9 Dose-versus-rate — does the effect track the driver or the exposure?

**Rule.** For any effect that appears at an intermediate value of a swept parameter, ask whether it
tracks the **rate** or the **total dose**. In trace terms: does a difference track the *per-step*
retry probability, or the *total number of retries*? The *per-call* latency, or the *total wall
time*? The *token rate*, or the *total tokens*? **Re-run at matched total exposure and at matched
rate; if the peak moves with run length, the parameter is not the driver.**

**Known-bad anchor.** `ECA_SPIKE_RESULTS.md` correction block: rules 25/46 peak at a fixed total
**dose** (`P_n × n × T` = 3–7 expected flips), so **the peak location halves as T doubles**, and the
height was still rising at T = 800 (+18 % from T = 200, against a claimed < 10 % convergence). Rules
58/110 are T-invariant to five figures — but their magnitudes are the mixture effect (C.6). **No
headline rule passed both controls.**

Second anchor, the general form: `GATES.md` reach 7, `7454647` — gravity's excess scaled with D while
the deliverable's gap did not, so the statistic was not measuring gravity. Water-lab form: *a sample
measured too late measures its own decay, not its source.*

**Dye test.** Plant an effect that is genuinely rate-driven and one that is genuinely dose-driven;
the gate must separate them. Two runs at 2× run length are sufficient and cheap.

**Depth.** Reads on any swept-parameter or intermediate-optimum claim. **Out of its depth** where run
length cannot be varied (a fixed production corpus) — then the claim is **ungauged** for this reach
and says so.

---

### C.10 Fixed-target control for swept ratios — the per-token/per-step trap

**Rule.** **When a ratio is swept against a variable that its own denominator is defined to track,
re-run at a fixed denominator before calling the trend a property of the numerator.** Every
per-token, per-step, per-thought, per-call and per-parameter normalisation is suspect by
construction, because token count, step count and call count all move with model and with language.

**Known-bad anchor.** `SAWTOOTH_AUDIT.md` §3–§3.1: the rent campaign's headline scale economy was a
factor of **2.68× decline** in cost per nat, exponent **−0.52**. Held at a **fixed amount of pattern**
— the same protocol, one knob changed — only **21.5–46.0 %** of the log-decline survives: fold
**1.21–1.57×**, exponent **−0.16 to −0.23**. In the fixed-fraction conditions **the numerator RISES
4.9–7.4×**; the "economy" is the denominator growing 13.0× faster. An economy of **size** and an
economy of **volume** were summed and reported as the first.

**And the same control ACQUITTED the sibling shape, which is why it is a gate and not a prejudice**
(§1.2–§1.3, §4): at a fixed target the sawtooth survives at **69–99 %**, and on ARM B the denominator
is **exactly invariant** at every step (verified to 3.6 × 10⁻¹⁵), so the whole uptick is numerator to
machine precision. **A gate that only ever deflates is not a gate.**

**The registered anti-wolf-cry clause** (§9.4): report **both** exponents; if the fixed-denominator
and co-varying-denominator readings agree within the campaign's stated numerical error budget, the
confound is null and one number may be quoted. In the rent case they differ by 2.3–3.2× and the gate
fires.

**Dye test.** `SAWTOOTH_AUDIT.md` supplies a planted one, already run: null protocol **N1**
(`cost = ε·k`, a closed form with **no dynamics anywhere**) pushed through the identical ratio
pipeline gives `b_rent = −0.3283` against a measured **−0.3238** — **agreeing to 1.4 %**. The same
null in the fixed-target conditions returns `b_rent = +1.0000`, the **wrong sign**. *"A gate that
cannot tell N1-in-frac from measured-in-frac is blind."* Both halves must be checked.

**Depth.** Reads on any ratio `X/Y` swept against `v` where `Y` is defined as a function of `v` —
**whether or not `Y` steps**; a smooth `Y` confounds just as hard. **Out of its depth** when `Y` is an
outcome rather than a set target (if the amount held is what the dynamics produced, not what the
solver aimed at, the fixed-denominator re-run is not constructible and the gate returns **ungauged**,
not clear). **Out of its depth on the numerator** — it gauges attribution, never whether the
numerator's response is real.

---

### C.11 Occupancy — minimum cell counts, and conditional fields that do not populate

**Rule.** Declare **in advance** a minimum count per cell below which the estimator may not be read
at all. Report, per arm, the **fraction of traces in which each conditional field populated**. A
reading below the validated detection limit is not a detection, and a cell below the floor is
**ungauged** — neither zero nor positive.

**Known-bad anchor #1, in the target pipeline.** RATCHET Exp 1 (§0.5): the four conditional
conscience fields populate only on boundary tension; averaging boundary-active and boundary-inactive
chains pulled `N_eff` to `[4.5, 6.6]` against a pre-registered window of `[6.6, 7.6]`. The correct
handling — which that team applied — is BO-2: **the measurement is well-defined only for
boundary-active chains**, and the boundary-inactive ones carry no information about the anchor.
Phase 1b requires a boundary-active question battery at a pre-registered per-question firing rate
`p_min ≥ 0.8`.

**Known-bad anchor #2, on the consequences of ignoring it.** `DALITZ_RESULTS.md` §6: the polarity
control's two arms had minimum cell counts of **659** and **472** against a pre-registered floor of
**1000**. They agreed — and the agreement means nothing, because both arms are ungauged, so *"the
polarity control's discriminating power is not established."* The sideband arm at 126 per cell is the
same. Of a 25-configuration threshold scan, **16 fail occupancy** and only 9 are scorable.

**Dye test.** Plant a known difference and progressively thin the sample; record the count at which
the gate stops seeing it. That number is the detection limit and must be quoted with every null.
`GATES.md` reach 11 records that we have never run this sweep — the fraction at which the gate is
*obliged* to alarm is unset. **Running it on traces is cheap and would be the first planted
occupancy sweep in the registry.**

**Depth.** Reads on every per-cell estimate. **Out of its depth** on corpus-level counts, which need
no floor.

---

### C.12 Ties, rails, and rank statistics

**Rule.** Report the **tied fraction** beside any rank-based statistic, and the **rail fraction**
(the share of readings at exactly 0.00 or exactly 1.00) beside any bounded score. Break ties
**randomly**, never by a deterministic rule correlated with index or arrival order.

**Why it bites on traces specifically.** Six of the sixteen projection fields are boolean — tied by
construction into two values. The continuous ones are bounded scores, and they are observed **on the
rails**: the correlation table in `FSD/TRACE_EVENT_LOG_PERSISTENCE.md` §2 (the Spanish timeout
investigation) records CSDMA at score **1.00** and DSDMA at score **0.00** in the same thought.
**[inferred]** Component receipt order is FIFO and sub-millisecond ties are broken by
`component_type` as a "coarse ordering hint" (wire format §3) — a deterministic tie-break correlated
with pipeline position, which is exactly the rule L3 forbids for rank statistics computed over
component order.

**Known-bad anchor.** `GATES.md` reach 11, kept taint: **the untrained-model control fires on tied
activations alone** — the tie structure, not the learning, produced the reading; and `95d1b3c`, IPF
is unsafe on sparse data. (The standing record also carries a measured 2× inflation of a moment-route
reading at a 10 % tie block; that figure is **received-not-measured** here — it was not re-derived
from its primary artifact for this document.)

**Dye test.** Inject a controlled tie fraction into a corpus with no real difference and show where
the rank statistic starts to read signal.

**Depth.** Reads on ranks, medians of bounded scores, and any statistic over event ordering. Cheap:
it is one number per field.

---

### C.13 Estimator-bias floor by permutation

**Rule.** Shuffle the condition labels, recompute with the **identical** estimator, and subtract that
floor. Two nulls are needed and they do different jobs: a **shuffle** null for estimator bias, and a
**generatively-matched** null (C.6) for the data's own structure. Report both.

**Known-bad anchor.** `GATES.md` reach 1, `b6527a8`: a **shot-noise-only run read 130 % of the
deliverable**, with the pre-registered null revealed as having no dye test at all.

**Dye test.** `GATES.md` reach 1 records the gap honestly: validated at the 130 % scale, **no
planted-amplitude sweep**, so the smallest dye it can see through its own floor is unmeasured. The
water campaign then closed it for its own instrument (`WATER_RESULTS.md` §2.3: a planted-ε ladder
located the detection limit at **3.8 × 10⁻⁴ nats — an order of magnitude above the pre-registered
design sensitivity of 3 × 10⁻⁵**). **Do the same for the trace instrument: plant a graded difference
and report the smallest one recovered above the floor.**

**Depth.** Reads on every information-theoretic and variance-based statistic.

---

### C.14 Probe polarity declared before the run

**Rule.** Before the run, write down **which direction of the diagnostic means PASS**. A gate whose
declared direction and implemented direction disagree is worse than no gate.

**Known-bad anchor.** `GATES.md` reach 8, `9180c6a`: Gate B had its polarity inverted; corrected with
the reasoning on the record, adjudicated against a run whose right answer was known (`c348c02`), and
**the reviewer's gate was the one that was wrong**. Second anchor, `GATES.md` *directional claims are
measured*: the sky campaign's "conservative direction" argument was **falsified in sign** — less
clipping produced a *larger* floor.

**Trace instance.** "Model A defers more, which is the conservative direction" is a directional claim.
It is tested by varying the mechanism, never argued from plausibility.

**Dye test.** Run the gate on a stored case with a known answer in **both** directions.

---

### C.15 Search caps and the look-elsewhere correction

**Rule.** Declare the size of the scan. A trace comparison scans (models × languages × questions ×
configurations × metrics), and that product is large: 29 locales × the projection's 16 fields is 464
cells before any model axis. **Report the number of cells scanned and correct the significance for
it, or the result is a maximum, not a measurement.**

**Known-bad anchor.** `DALITZ_RESULTS.md` §7: a contiguous cluster of high readings at one threshold
looked like a real localised effect. Corrected over the nine occupancy-passing configurations by
taking the **maximum across configurations in each of 3 000 permutation replicas**, the global p is
**0.017** — a 2.1σ-equivalent, explicitly *"not a detection and not cashed"*, quoted only with the
global number attached. Second anchor: `GATES.md` *search caps declared*, `4aea70d` — a saturated
search result is a lower bound, never a count, and an "inversion" was withdrawn on those grounds.

**Dye test.** Compute the null distribution of the **maximum** over the scanned cells, not of a single
cell.

**Depth.** Reads on every multi-cell comparison. **Out of its depth** on a single pre-registered cell,
which needs no correction and is the cheapest way to avoid this gate entirely.

---

### C.16 Received numbers are not measured numbers

**Rule.** A figure quoted in a message, a dashboard, or a sibling's document is **hearsay** until
re-derived from the primary artifact. **Tag it `received-not-measured` at the point of entry**, and
re-verify before it is used as data in any table, fit or floor. When a correction lands, sweep every
place the number already propagated.

**Known-bad anchor.** `GATES.md`, *received numbers are not measured numbers*: **glass took a
water-campaign number from a message into its own table as data; water's own re-check found the
number wrong — in glass's favour — and the correction had to be chased through a table it had already
entered.** `WATER_RESULTS.md` §9 then tags every glass-column number in its head-to-head as
`received-not-measured`, which is the discipline working.

**Trace instance, and it is the common case.** Model identity, token counts, cost and latency in a
trace are **reported by the pipeline**, and `deployment_profile` is **agent-declared** (§0.4, wire
format §3.2). They are received numbers with respect to any claim about the model. Where they can be
cross-checked (per-call `models_used` against the run configuration; `tokens_total` against the
provider's own accounting) they must be, and where they cannot, the claim inherits the pipeline's
accuracy as an unstated assumption — so state it.

**Dye test.** None numerical — the check is procedural, at ingest.

---

### C.17 Gate-log provenance and analysis reproducibility

**Rule.** A committed analysis output must be **reproducible from the instrument committed beside
it**. Deterministic pipelines are re-run and compared bitwise before the log is trusted.

**Known-bad anchor #1.** `GATES.md`, *gate-log provenance*: the phi4 gate log at `5e3d2ff` **was not
produced by its own committed instrument**, caught by re-running the bitwise-deterministic sampler.

**Known-bad anchor #2, and it is the one that transfers.** `GLASS_RESULTS.md` §2.1: **two paired
surrogate processes were accidentally started ninety seconds apart and wrote the same log and the same
JSON.** The draft was written from the first; the second overwrote it. Four numbers in a published
table were from a different run. The two runs differ only in a GPU RNG the surrogate does not seed —
*"a real reproducibility defect, now on the record and not yet fixed."*

**Trace instance.** Concurrent QA-runner sweeps write to timestamped tee directories
(`/tmp/qa-runner-lens-traces-<UTC-iso>/`), which mitigates the collision — but the analysis stage does
not inherit that protection. RATCHET already does the right thing and it should be copied verbatim:
**per-batch SHA-256 manifests (`tee_sha256.txt`) plus a re-fetch from lens to confirm round-trip
integrity** (`PRE_REGISTRATION.md` §14).

**Dye test.** Re-run the analysis from the committed traces and diff bitwise. If it is not bitwise
deterministic, seed it or record why it cannot be.

---

### C.18 Rails and thresholds — the boundary reach, honestly scoped

**Rule.** Where a reading passes through a clamp or a threshold, the clamp transduces what you are
measuring. Report the **rail fraction** per field per arm, and — where two conventions exist — read
under both.

**Known-bad anchor.** `GATES.md` reach 2, `30718a8`: the adversary-channel bench demo **collapses
259×** under a fold boundary rather than a clip; the readout runs through the kernel clamp, so the
boundary was transducing the coupling. The standing lesson (`cirisarray-clamp-mediated-readout`) is to
run every reading under both conventions.

**Honest scoping for traces.** There is no fold/clip choice in a trace pipeline, so **this reach ports
only partly**. What ports is the rail disclosure: conscience faculties compare a score against a
threshold (`entropy_threshold`, `coherence_threshold` — `FinalizeActionStepData`), so
`conscience_passed` is a thresholded readout of a continuous score, and a difference in pass-rate can
be a difference in score distribution *near the threshold* rather than anywhere else. **Report the
score distribution, not only the pass rate**, and report what fraction of the mass sits within a
stated distance of the threshold.

**Dye test.** Shift a score distribution by a known amount that does not cross the threshold; the
pass-rate must not move. Shift one that does; it must.

---

### C.19 The warrant reach — a right number held for a wrong reason (PROPOSED, not validated)

**Rule.** A claim whose **substance survives** and whose **warrant does not**. The scannable form: **a
true statement published without the condition that bounds it.** Enforcement is **procedural**, at a
fixed lifecycle point, because substance-surviving is exactly what removes the incentive to re-check.

**Known-bad anchor.** `GATE_PROPOSAL_WARRANT.md` §3 + §3a: **seventeen instances, three campaigns, one
week** — nine pump, four water, four glass. **Not one was caught by a numerical control.** The pump
campaign's eight-gate battery **passed everything at 1e−15 while five of its warrants were failing.**
The lead taint (`glass 3`) is the sharpest case: the claim was *numerically exactly correct* — every
quoted fraction shifted by **+0.00 %** under the correct method — while the stated reason for it was
the exact inverse of the truth.

**The procedures** (§6 lists five numbered, W1–W5, plus W2′ — six bullets):

- **W1** — cite to the **signature**, not the name: quote a theorem's hypotheses from source.
- **W2** — **sweep the class, not the instance**: when a correction lands on a citation, re-audit
  every citation of that object in every document of the campaign.
- **W3** — a **negative literature claim is a claim**, checked against the defining paper's figures.
- **W4** — a **mechanism attributed is a mechanism to be measured**.
- **W5** — an author's **second derivation** of their own result is worth more than a reader's first.
- **W2′** — a correction is not adopted until the **advice** changes too.

**Trace-specific form, which is where this reach will bite hardest.** Every claim of the form *"model
A's traces show more X because model A does Y"* is a mechanism attribution (W4). The pipeline supplies
several tempting ones that are **not measured by the trace**: "the model deferred because it was
uncertain", "the conscience fired because the content was risky", "the retry happened because the
first answer was bad". The trace records **that** the step fired, not **why**. Attributing a mechanism
to a counter is the warrant reach in its native habitat.

**Dye test.** **NONE-YET, and it cannot be numerical.** `GATE_PROPOSAL_WARRANT.md` §5: the failure is
invisible to numerical gates by construction, because the number is right. The plumb line must be
**planted** — an artifact in which a correct value is published with a demonstrably wrong
justification, built on purpose by one party and scored by another. That artifact does not exist. §9
of that document **recommends against registering the reach until it does**, and this port carries that
recommendation rather than quietly upgrading it.

**Depth.** Reads justifications, not numbers. **Out of its depth on anything a numerical gate already
covers.**

---

### C.20 Outcome completeness — the non-verdict must be enumerated in advance

**Rule.** Before unblinding, enumerate **every** possible outcome including the non-verdicts. The one
that must be named explicitly is:

> **"a large, well-controlled reading whose decomposition was never performed."**

**Known-bad anchor.** `GATES.md`, *outcome completeness*: the sky campaign's unblind **fit no
pre-registered outcome** (`28fadbd`), which is how a 61.7σ reading became uncashable. Companion:
*gate discharge before unblind* — **no unblind while any pre-registered VOID gate is undischarged**,
verified against the record and not memory; the sky campaign's §7.5 weight-variation VOID gate was
never run and the reading was sensitive at 2.5–2.9σ.

**Trace instance.** "Models A and B differ at 6σ on `N_eff`, and we did not decompose the difference
into (populated-dimension count, chain length, seal rate, retry count, prompt-token count)" is **not a
finding**. It is the named non-verdict, and it must be written down before the run so that it is
available to be reported.

---

## D. PRE-REGISTRATION TEMPLATE — a trace-comparison study

Fill it in, commit it, **then** run. The rule that binds is not "we will measure X" but "a value above
Y means the claim survives, below Y it dies" (`epistemology.md` L1).

---

```
# <NAME>_PREREG.md — pre-registration, frozen before any trace is read

## 0. SCOPE
Substrate: <agent version, trace_schema_version, model list, locale list, question set + its hash>
This is <simulated / production / QA-harness> data. It is not <the thing it will be mistaken for>.
Nothing here bears on <the claims it must not be allowed to touch>. No Lean file, no Stance.lean.

## 1. THE CLAIM
One sentence, in the form of B.1-B.5. Name the data layer (0.3) and the statistic exactly.
State what is NOT claimed, in a numbered list, before any result exists.

## 2. THE KILL — separable
K1: <observation that falsifies THIS claim and nothing beneath it>
   Bar: <number, direction, and the error bar it is measured against — name the sigma>
   (GLASS_RESULTS.md's K1 turned on WHICH sigma; the prereg chose the wrong one.
    Name the estimator of the error bar here, not after.)
Secondary kills K2..Kn, each separable, each with its own bar.

## 3. THE INSTRUMENT, AND ITS OWN EXAMINATION (docimasia — run BEFORE any comparison)
3.1 Plumb lines: inputs whose correct answer is known exactly, with the required values.
    (Dalitz ran six; all passed to machine precision. Water's analysis instrument
     RAISED ON THE FIRST FRAME the first time it was run.)
3.2 Dye test: planted differences at a graded ladder of sizes; report the smallest
    recovered above the floor. THIS NUMBER IS THE DETECTION LIMIT and is quoted with
    every null result the study produces.
3.3 Blindness check: a difference the statistic MUST NOT see, injected and VERIFIED
    PRESENT by reading it out of the channel it was injected into.
    (Dalitz §3c: a 20-point CP asymmetry confirmed at +0.1995 +/- 0.019 in the pair
     marginal while the whole-only reading did not move. The verification of the
     injection is not optional — Dye B's flatness means nothing without it.)

## 4. THE NULLS — each named with the failure it addresses
N1  label permutation, within cell            -> estimator bias (C.13)
N2  structureless synthetic corpus, matched   -> selection/pipeline minting (C.2)
N3  mechanism-free mixture of the two arms    -> mixture manufacture (C.6)
N4  seal-matched subsample                    -> survivorship (C.3)
N5  <second, independent null-construction>   -> null-construction sweep
    (GATES.md requires >= 2 defensible constructions with the spread quoted as a
     systematic. Glass and water BOTH had only one and BOTH disclosed it.)

## 5. THE GATES AND THEIR DISCHARGE POINTS
| gate | discharged when | verdict if undischarged |
|---|---|---|
| C.1 selection geometry   | zero-overlap arm run          | VOID for that cell |
| C.2 structureless control| pedestal < 50% of reading     | VOID for that cell |
| C.3 survivorship         | seal rate reported per arm    | VOID |
| C.4 named denominators   | both denominators reported    | trend claim not made |
| C.5 pair-pinning LP      | interval width reported       | UNGAUGED |
| C.7 floors matched to N  | per-arm floors drawn          | UNGAUGED |
| C.8 null shape           | p99/median reported, >=200 dr.| no z may be quoted |
| C.11 occupancy           | min cell count >= <declared>  | UNGAUGED (not zero) |
| C.12 ties/rails          | tied + rail fractions reported| rank stat not believed |
| C.15 look-elsewhere      | scan size declared + corrected| maximum, not measurement |
| C.17 provenance          | bitwise re-run diffed         | log not trusted |
NO UNBLIND WHILE ANY VOID GATE IS UNDISCHARGED. Discharge is verified against the
record, not memory.

## 6. THE OUTCOMES — every one, including the non-verdicts
(a) difference exceeds the bar and survives every gate  -> claim survives
(b) difference below the bar                            -> NULL, quoted with 3.2's limit
(c) difference exceeds the bar, one or more gates VOID  -> VOID, reported as loudly as (a)
(d) instrument cannot be read at the corpus's N         -> UNGAUGED
(e) LARGE, WELL-CONTROLLED READING WHOSE DECOMPOSITION
    WAS NEVER PERFORMED                                 -> NON-VERDICT (C.20)
(f) the difference is a difference in missingness        -> that is the finding; report it
(g) the two denominators disagree about the trend       -> report both; no trend claim
(h) arms not comparable (trace_level, schema version,
    translation coverage) differ                        -> UNGAUGED, not null

## 7. VOID CONDITIONS, declared now
- any arm whose min cell count is below <declared floor>
- any comparison across trace_level or across trace_schema_version shapes
- any language arm whose translation coverage differs from its comparator's
- any cell where the structureless pedestal reaches 50% of the reading
- any reading whose floor was drawn at a different N than the reading
- any statistic whose LP interval, given the declared covariates, has width 0

## 8. WHAT IS NOT CLAIMED
Numbered, written now, not after.

## 9. FILES, SEEDS, HASHES
Question-set hash. Per-batch SHA-256 manifest. Seed. Agent build. Model IDs as
returned by the provider, not as requested.
```

---

**One process note, and it is a mitigation rather than a guarantee.** On a shared worktree,
`git add` followed by a separate `git commit` is **not atomic across agents** — another agent's commit
sweeps your staged files into itself. The one-call form `git commit -m ... -- <pathspec>` stages and
commits atomically, **but fails on an untracked path**, so a genuinely new file still needs
`git add` first. Narrow the race by issuing the add and the commit in **one shell invocation** with the
pathspec still bounding the commit (`GATES.md`, *atomic pathspec commits*, with its defect disclosed).

---

## E. WHAT THIS COSTS, AND WHAT IT BUYS

### E.1 It is expensive, and the expense is real

The rent campaign's audit, the water campaign's twelve amendments, and the Dalitz campaign's seven
disclosed defects each cost roughly as much effort as the measurement they gate. `GATE_PROPOSAL_WARRANT.md`
§10 puts the honest comparison in a table: on the arm where the pre-registration was frozen **before**
the numbers existed, nine of eleven amendments were corrections and **not one number changed, because
none existed**. On the arm frozen after, six corrections landed on published numbers and their
justifications, and *"had any of them sat in the quoted rungs instead of beside them, the correction
would have cost a retraction."*

So the honest statement of cost is: **the discipline is cheapest when applied earliest, and its price
rises sharply after the first number is seen.**

### E.2 Cheap gates — run these always, no discussion

| gate | cost |
|---|---|
| **C.2 structureless control** | one synthetic corpus, one analysis run. The single highest-value gate in this document: it caught a 22× pedestal on a real campaign's headline. |
| **C.3 survivorship / seal rate** | two counts per arm. |
| **C.7 floors matched to N** | a loop. |
| **C.8 null shape** | 200 draws instead of 1. |
| **C.11 occupancy** | one count per cell, declared in advance. |
| **C.12 ties and rails** | one number per field. |
| **C.4 named denominators** | one extra column. |
| **C.16 received numbers** | a tag at ingest. |
| **C.19 W1–W5** | minutes of reading. `glass 1` was four `grep`s. |

**Together these are perhaps a day of work on a study that takes a week, and they carry most of the
protection.** Water's ideal gas, glass's second denominator, and Dalitz's 200 draws are each a
few hours, and each of the three would have prevented a published wrong headline.

### E.3 Expensive gates — run these when the claim is load-bearing

| gate | cost | when it earns it |
|---|---|---|
| **C.5 pair-pinning LP** | building the LP; exact but needs the statistic expressed linearly in cell probabilities | when a claim asserts the statistic carries information beyond the obvious covariates. It re-scoped a published headline three times (`70535d4`). |
| **C.6 full mixture nulls** | a second null-generator family, plus its own dye test | any two-arm comparison making a mechanism claim. `GATES.md` requires ≥ 2 null constructions with the spread quoted; glass and water each built one and disclosed it. |
| **C.13 planted-amplitude dye ladder** | a graded planting harness | once per instrument, then reused. Water's cost the campaign a rewrite and returned the fact that **the battery was an order of magnitude less sensitive than its design assumed**. |
| **C.10 fixed-target re-run** | a second sweep at a fixed denominator | any per-token/per-step claim. It re-scoped a headline by 2× and **acquitted** a sibling shape. |
| **C.1 zero-overlap arm** | a second corpus construction | any claim on windowed or follow-up traces. |

### E.4 What it buys

Three things, stated without inflation:

1. **Claims survive contact with a hostile reader**, because the hostile reader's first four moves —
   *what is your null, what is your floor, what is your denominator, what did you exclude* — are already
   answered in the document.
2. **A fired kill costs a day instead of a retraction.** Dalitz's D7 would have killed a working
   implementation on a single draw. Water's D2-equivalent would have reported a design failure that
   was a 1/N artifact. Glass's paired bootstrap moved a claim from "clears the bar at 9.8σ" to "does
   not clear it at 3.8σ" — and the campaign reported the second.
3. **The nulls are reusable and the results are not.** Every campaign above produced methodological
   findings worth more than its headline: the water campaign's null is a null, and its three
   instrument findings are permanent. The gates compound; the measurements do not.

**And the honest counterweight.** `GATES.md`'s own central self-criticism applies to this document in
full: **nine of thirteen reaches sit in *proposed* while being used as though validated**, six missing
a plumb line and six missing a dye test, and **no gate in the registry has a measured false-fire
rate**. Porting the gates does not port validation. Every gate in §C that lacks a stated dye test here
is a **hypothesis about a gate**, and the first trace study to run one should say which gate it
validated.

---

## F. W2 APPLIED TO THIS DOCUMENT

Per `GATE_PROPOSAL_WARRANT.md` §6, W2 — sweep the class, not the instance — applied to my own
citations before committing. Four findings, all disclosed:

1. **`Stance.lean`'s `ai-safety` claim disagrees with itself about the model size**: `plain` says
   "a 7B model that competently lied about 45 percent of the time"; `kill` and `confidence` say the
   negatives are "at 8B". Both cannot be right. The result — two validated negatives with firing
   controls at z = −306 and z = +32 — is unaffected. Flagged in §A.1 rather than silently picking one.

2. **`GATES.md` row 507 (the warrant reach) says "nine instances, three campaigns, one week", and
   `GATE_PROPOSAL_WARRANT.md` §3–§3a now carries seventeen** (nine pump, four water, four glass —
   §7's own count). The proposal document's §3 *header* also still says "nine" above a
   thirteen-row table. **The registry inherited a stale count from a stale header.** This is a live
   warrant-reach instance inside the gate registry itself, found by running W2, and it is exactly the
   failure the reach describes: the substance (the reach is real) survives; the warrant (how many
   incidents support it) was never re-checked after it grew.

3. **Two enumeration/docstring mismatches in the pipeline source**, both benign and both named in §0
   rather than glossed: `StepPoint` has 11 members and its docstring says 10; `ReasoningEvent` has 10
   members and its docstring says "9 result events". Neither affects any claim here; both are the
   named-denominator hazard in its smallest form.

4. **The brief for this document said the warrant reach has "five procedures"**; §6 lists five numbered
   (W1–W5) plus **W2′**, six bullets. §C.19 quotes all six.

**What I did NOT verify, marked as a gap rather than assumed clean.** I read schemas, FSDs,
pre-registrations and the language harness; I did **not** read the `@streaming_step` decorator
implementation, the lens persistence implementation, or the `ciris_accord_metrics` adapter. Statements
about what the pipeline *emits* are from the wire-format spec and the schema modules, which
`FSD/TRACE_WIRE_FORMAT.md` calls the contract and the implementation respectively; statements about
what the lens *stores* are from the persistence FSD, whose own status line reads **"DRAFT — no
implementation yet"** (v0.1, 2026-04-30). **So §0.2's last paragraph describes a documented defect in a
document that also proposes its fix, and whether the collapse is still current is UNVERIFIED here.**
Anyone acting on C.20's decomposition list should check that first.

---

## G. FILES READ

| file | used for |
|---|---|
| `CIRISOntology/GATES.md` | the registry: 13 reaches, 23 harvest rows, the four design rules, the axiological layer, the lifecycle |
| `CIRISOntology/epistemology.md` | L1–L8, the four strengths, the mechanization boundary |
| `CIRISOntology/CIRISOntology/Stance.lean` | the `ai-safety` claim (§A.1) |
| `scratchpad/WATER_RESULTS.md` | §C.1, §C.2, §C.7, §C.8, §C.13, §B.1 |
| `scratchpad/GLASS_RESULTS.md` | §C.4, §C.17 |
| `scratchpad/KAPPA_EDGE_RESULTS.md` | §C.5 |
| `scratchpad/DALITZ_RESULTS.md` | §C.7, §C.8, §C.11, §C.15, §D.3 |
| `scratchpad/ECA_SPIKE_RESULTS.md` | §C.6, §C.9 |
| `scratchpad/SAWTOOTH_AUDIT.md` | §C.10 |
| `scratchpad/GATE_PROPOSAL_WARRANT.md` | §C.19, §E.1, §F |
| `scratchpad/PUMP_RESULTS.md` | §A.1 (the rate law) |
| `CIRISAgent/ciris_engine/schemas/services/runtime_control.py` | `StepPoint`, `ReasoningEvent`, all step-data schemas |
| `CIRISAgent/ciris_engine/schemas/processors/phase_results.py` | phase result types |
| `CIRISAgent/FSD/TRACE_WIRE_FORMAT.md` | the CompleteTrace contract, `trace_level`, `deployment_profile`, the seal rule |
| `CIRISAgent/FSD/TRACE_EVENT_LOG_PERSISTENCE.md` | the collapse defect, the Spanish timeout case |
| `CIRISAgent/tools/qa_runner/modules/model_eval_tests.py` | `LANGUAGE_SPECS`, `LOCALE_USERS`, translation coverage, prefix-vs-native selection (lines 565–573) |
| `CIRISAgent/{AGENTS,CONTRIBUTING,CLAUDE}.md` | H3ERE structure: 4 DMAs, 10 handlers, 6 buses |
| `RATCHET/experiments/exp1_multimodel_neff/PRE_REGISTRATION.md` | the prior campaign, its locked rule, amendment A4 |
| `RATCHET/experiments/exp1_multimodel_neff/phase0_smoke_analyze.py` | `PROJECTION_16`, `CORE_FIELDS`, extraction paths |
| `RATCHET/experiments/exp1b_boundary_active/REGIME.md` | BO-1…BO-4, the boundary-active filter |
| `CIRISConstitution/constitution/part_1_foundation.md` | §1.3 PDMA, the attestation layer ruling, the transparency rule |

Scratchpad only. No Lean file opened, `Stance.lean` untouched, `lake` never invoked, the audit not
run, nothing in `../RATCHET`, `../CIRISAgent` or `../CIRISConstitution` modified, nothing pushed.
