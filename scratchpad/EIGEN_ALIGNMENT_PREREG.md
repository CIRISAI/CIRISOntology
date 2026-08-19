# PRE-REGISTRATION — the eigen-alignment experiment

**Version 2, revised 2026-08-18 after adversarial referee round (task N1b). Still frozen
before any embedding is computed.** Design note it discharges: `LEAN2_CONFRONTATION.md`
§"The eigen-alignment experiment". **Nothing on any corpus has been run.**

**Referee verdict on version 1 was DO NOT RUN AS WRITTEN** — 6 CRITICAL, 11 MAJOR, 9 MINOR,
9 honesty defects, of which three (P2-neg's statistic, P2-pos's statistic, and the primary
arm's own VOID gate) were unevaluable *by algebra, before any data*. Every defect and its
disposition is recorded in **§20 Referee round**. That section is part of the record, not an
appendix: the version-1 text is not silently corrected, it is corrected in public.

## 0. Freeze declaration — what was inspected before freezing

### 0.1 Version 1 freeze (unchanged)

The design was written after inspecting, and only after inspecting: file paths, row counts,
field schemas, label distributions, condition vocabularies, character-length distributions,
and the first row of each corpus file. **No embedding was computed. No PCA was run on any
corpus. No item body beyond first-row samples and the prompt template was read.** The RATCHET
report and the PLANE prereg/results were read in full; both are already-published internal
records.

### 0.2 Version 2 — what the referee round additionally computed, and why it is admissible

The referee round ran computations on disk. They are declared here in full, because a
pre-registration that hides its own preparatory measurements is not one.

**Admissible, and used to re-stake this document (no embedding involved):**

| what was computed | why it does not contaminate | where it lands |
|---|---|---|
| synthetic rank-resolution pilot (planted signal, Gaussian noise, Corpus-A half class sizes) | synthetic only; contains no corpus text and no embedding | re-stakes §8's grid |
| counting-identity algebra, verified numerically on noise | algebra; true for any corpus | rebuilds §5, §10 |
| TF-IDF/logistic power proxy on Corpus A raw text | **no embedding model touched**; this is a bag-of-words ceiling on how much kind information the text carries at all | §9's forward prediction |
| changed-span character counts per kind | a length statistic, not a semantic one | §4's nuisance list, §7's N1b |
| generation-batch membership per item | file provenance | §4, §9-P1a-batch, V11 |
| RATCHET 8-signal PCA reproduction | a different object entirely (§2.4); it is the K5 evidence | §16-K5, fired |
| near-duplicate text proxies on Corpus B streams | text-level, not embedding-level | §15-V4 |
| off-vocabulary panel label counts | a label tally | §5 secondary arm |

**Not computed, still frozen:** no embedding of any text by any model; no PCA of any
embedding cloud; no Ω, no a_j, no R_kind, no AUC, no π; no reading of Corpus A item bodies
beyond the first-row samples of version 1 and the mechanical span extraction above (span
*lengths* and TF-IDF *token counts* were computed; no span was read).

**The bright line, stated so it can be checked later:** the §9 PASS floor for Ω(11) is
**unchanged at 0.25**. It was not lowered after the power proxy. The power proxy is used to
stake a **forward prediction that the floor will not be met** (§9.1), which is the rule-6-clean
use of it. Anyone auditing this can verify that 0.25 appears in version 1 and version 2 alike.

Everything in §§3–17 is frozen. Any deviation is an amendment with a timestamp, written
before the deviating computation runs, per `epistemology.md` rule 1.

## 1. The claim under test

If the 11+1 taxonomy is the coordinate system of change-descriptions, then:

* **P1 — alignment.** On a change-describing corpus, the principal content directions of the
  embedding cloud align with the 11 kinds' one-vs-rest discriminator directions, and the
  number of kind-carrying principal directions is near 11.
  * **P1's sharp clause — "not 7, not 13" — is CONDITIONALLY STAKED and may be retracted
    before any data.** §8's gauge decides whether the estimator can resolve 11 from 13 at
    n = 124. If it cannot (σ_R > 0.66), the clause is **retracted in advance** and P1b is
    demoted to "consistent / inconsistent with 11". Version 1 carried the clause
    unconditionally into a PASS band that admitted 13; that is defect C5, fixed here.
* **P2 — the relation's signature.** Record (the 12th) does **not behave like a twelfth
  content class**: its discriminator direction is not among the principal content directions
  that an independent half of the cloud recovers, while the base kinds' are. It surfaces
  instead as a frame-conditional factor: invisible to an artifact-only reading, appearing when
  the frame is supplied. (`repairable_does_not_factor`, spoken in PCA.)
  * **Wording corrected (defect C1).** Version 1 said "does not appear as a twelfth content
    *direction*". For a 12-class partition, a twelfth *between-class* direction cannot exist —
    the 12 one-vs-rest centroid contrasts obey one exact linear relation and span at most 11
    dimensions, for any labels on any corpus. "Twelfth direction" was therefore an ill-posed
    object. The testable claim is about **which directions the held-out PCA recovers**, and
    §10 rebuilds the statistic on a construction where Record's direction is genuinely
    outside the fitted span.

P1 and P2 are **separable**: each has its own statistic, its own null, and its own kill, and
neither kill touches the other. Neither kill touches `Core/Generator.lean`,
`Core/WrongKind.lean`, or the PLANE study's measured label flatness — those are a theorem, a
type, and a panel measurement respectively, and this experiment is a fourth, independent
instrument that can disagree with all three without retiring any of them.

**What this experiment cannot decide** (stated now so it cannot be claimed later): whether
the twelve are the *right* twelve; whether embedding geometry has any authority over a
taxonomy's correctness; and whether any of the three integers named "11" in the design note
are the same object. **§2.4 has now removed one of those three legs outright — K5 has FIRED,
by inspection, before the main run.**

## 2. Corpora — located, with roles fixed

### 2.1 PRIMARY (change-describing, labelled) — ours

| role | path | rows | label field |
|---|---|---|---|
| **Corpus A** (authored, balanced) | `/home/emoore/CIRISOntology/scratchpad/plane_corpus/corpus_full.jsonl` | 248 | `kind_target` ∈ 12 internal names |
| Corpus A-held (later authored, boundary-loaded) | `/home/emoore/CIRISOntology/scratchpad/plane_corpus/part_d.jsonl` | 12 | `kind_target` |
| **Corpus BAB** (one artifact, ten kinds) | `/home/emoore/CIRISOntology/scratchpad/plane_corpus/babel_items.jsonl` | 10 | `kind_target` (10 of 11 kinds; no `contingent`, no `testimonial`) |

Corpus A class counts, verified: axiotic 20, deontic 20, pragmatic 20, ontological 24,
epistemic 20, empirical 20, contingent 20, procedural 20, nomological 20, structural 20,
axiomatic 24, testimonial 20. Domains: policy 50, config 50, code 49, report 50, process 49.
Difficulty: clear 192, hard 56. Internal→plain map (from `Core/WrongKind.lean` lines 167–178,
used verbatim): axiotic→Priorities, deontic→Rules, pragmatic→Manner, ontological→Identity,
epistemic→Confidence, empirical→Facts, contingent→Circumstances, procedural→Process,
nomological→Model, structural→Structure, axiomatic→Premises, **testimonial→Record**.

Corpus A-held (`part_d.jsonl`, 12 items) covers **only three kinds** — empirical 6, deontic 3,
ontological 3. It therefore says nothing about the other nine, and scoring it "once, reported
once" is a spot check on three kinds, not a held-out replication (defect m7).

Corpus BAB verified: 10 items, **10/10 share one identical `before` text**, 10 distinct kinds,
no testimonial and no contingent. It is a genuine topic control.

### 2.1a Generation batch — a measured confound, disclosed and controlled (defect M1)

`kind_target` is very nearly **nested in generation batch**. Verified by matching ids:

| batch file | rows | kinds it contains |
|---|---|---|
| `part_a.jsonl` | 120 | ontological, empirical, epistemic, deontic, axiotic, pragmatic (20 each) |
| `part_b.jsonl` | 120 | structural, procedural, testimonial, axiomatic, nomological, contingent (20 each) |
| `part_c.jsonl` | 8 | ontological +4, axiomatic +4 (a top-up) |

There is **zero crossing between part_a and part_b**: a perfect 6-vs-6 split of the kinds by
batch. (Two kinds — ontological and axiomatic — additionally span part_c; the referee's
"no kind spans two batches" is very slightly too strong, and the correction does not help.)

**The batch signature is textually detectable.** TF-IDF 1–2 gram + logistic regression on the
unchanged `before` text predicts batch at **0.573** (5-fold stratified; majority baseline
0.484). Any batch-level stylistic drift is therefore a rank-1 predictor of a 6-vs-6 kind
split, contributes directly to Ω and to the top a_j — and **the N1 label permutation cannot
see it**, because permuting labels destroys the batch alignment, so a pure batch effect reads
as significant alignment. This is the single most dangerous confound in the design and version
1 did not name it.

Two controls, both pre-registered here (§4 and §9-P1a-batch), and one new VOID (V11).

### 2.1b Changed-span size is strongly kind-dependent — measured (defect M2)

Median changed-span characters by kind (mechanical `difflib` opcode span, verified):

| kind | contingent | empirical | deontic | axiomatic | pragmatic | ontological | epistemic | testimonial | nomological | axiotic | structural | procedural |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| median chars | 1.5 | 3.0 | 8.0 | 13.5 | 17.5 | 18.0 | 22.5 | 39.5 | 41.5 | 59.5 | 69.5 | **130.5** |

An **87× spread**; Kruskal–Wallis H = 96.82, **p = 7.6e-16**. Version 1 regressed out a single
`log10(1 + span chars)` term — a rank-1 linear removal against an 87× nonlinear dynamic range.
That is insufficient on its own, so a **span-stratified permutation null (N1b) is added and
made a required conjunct of P1a's PASS** (§7, §9).

### 2.2 PRIMARY (change-describing, unlabelled at fit time) — wild

**Corpus B** = the union of the three ecological files, 279 items, `kind_target = "WILD"`:

| path | rows | streams |
|---|---|---|
| `/home/emoore/CIRISOntology/scratchpad/plane_corpus/eco_corpus.jsonl` | 170 | fedreg 60, github 50, osm 60 |
| `/home/emoore/CIRISOntology/scratchpad/plane_corpus/eco_osm2.jsonl` | 60 | osm2 60 |
| `/home/emoore/CIRISOntology/scratchpad/plane_corpus/eco_wiki2.jsonl` | 49 | wiki2 49 |

Panel labels for B exist at BASE only (`eco_judgments.jsonl` 510, `eco2_judgments.jsonl` 180,
`eco2_wiki_judgments.jsonl` 147 judgments, 3 models per item). **B's labels are never used to
fit anything**; they are used only to report which kinds B actually exercises. Recorded in
advance: B's panel label distribution is severely skewed (Rules 209, Facts 136, Identity 39,
Manner 45 votes in the 170-item file) and contains **6 Record votes in 510** — so B is a
usable PCA cloud but is **not** a usable Record test-bed. All Record work is on Corpus A.

**Source concentration, disclosed (defect m8):** Corpus B is **43% OpenStreetMap**
(osm 60 + osm2 60 = 120 of 279), treated in §4 as 2 of 5 one-hot strata. Kind skew and source
concentration are two separate weaknesses and both are now named.

### 2.3 The frame-conditional judgment corpus (for P2-pos)

`/home/emoore/CIRISOntology/scratchpad/plane_corpus/full_judgments.jsonl` — 5,418 rows =
258 items (248 Corpus A + 10 Babel) × 7 conditions × 3 model families, fields `condition`,
`model`, `kind`, `second`, `reason`. Conditions are exactly the seven paragraph-pairs frozen
in `/home/emoore/CIRISOntology/scratchpad/plane_annotate.py` `CONDITIONS`:
BASE (full retention / everything-else-fixed), **F1** (partial retention: siblings destroyed),
**F2** (minimal retention: only the two versions survive), D1, D2 (design swaps), W2, W3
(attribution swaps). BASE/F1/F2 differ **only** in the Retention paragraph; W2/W3 differ from
BASE **only** by an appended provenance sentence. That is the lever P2-pos uses, and the
W-arm is its floor.
Coverage verified: 1,765 of 1,806 item×condition cells have all 3 models parsed, 41 have 2,
0 have fewer; `reason` is missing on 41 of 5,418 rows; reason length median 124 chars,
max 256 — **short**, which is a named weakness (§19-D3). The max of 256 is **not** a truncation
artifact: only 1 of 5,377 rows sits at 256.

**Off-vocabulary panel labels exist and now have a handling rule (defect m9).** Measured:
`full_judgments.jsonl` — 1 `Scope`, 1 `NO FIT`, 41 null; `eco_judgments.jsonl` — 2 `Version`,
12 `NO FIT`, 7 null; `eco2_judgments.jsonl` — 5 null; `eco2_wiki_judgments.jsonl` — 3 `NO FIT`,
2 null. **Frozen rule:** any vote whose `kind` is not one of the 12 plain names (including
`NO FIT`, `Scope`, `Version`, and null) is **dropped from the vote before the modal is taken**;
if fewer than 2 in-vocabulary votes remain for an item, the item is dropped from the
panel-modal secondary arm and the drop count is reported. Off-vocabulary rates are reported per
file. This rule touches only §5's secondary arm; the primary uses authored labels.

### 2.4 RATCHET — LOCATED, AUDITED, and K5 has FIRED (defect M8, h2)

**FOUND.** The n=6,465 dataset the `EMPIRICAL_REPORT.md` describes is on disk:

| file | rows | bytes | content |
|---|---|---|---|
| `/home/emoore/RATCHET/release/data_scrubbed_v1/trace_context.jsonl` | **6,465** | 10,662,771 | flat analysis view, **59 columns**, **25 numeric-capable** |
| `/home/emoore/RATCHET/release/data_scrubbed_v1/accord_traces.jsonl` | **6,465** | 223,057,500 | raw traces incl. JSONB blobs and free text |

Format: JSONL, one trace per line. Row count confirmed by `wc -l` and by
`release/MANIFEST.json` (`row_count: 6465`, sha256 pinned there). **Column count corrected to
59** (defect m2; version 1 said 60). The 25 numeric-capable columns are: attestation_level,
coherence_level, coherence_score, conscience_checks_count, cost_cents,
csdma_plausibility_score, dsdma_domain_alignment, entropy_level, entropy_score,
epistemic_humility_certainty, id, idma_correlation_risk, idma_k_eff, llm_calls,
optimization_veto_entropy_ratio, processing_ms, qa_question_num, t_action_ms, t_aspdma_ms,
t_conscience_ms, t_dma_ms, t_snap_ms, thought_depth, tokens_input, tokens_output.

**Free text, corrected (defect m1).** `action_rationale` is non-null on **2,148** rows of
`accord_traces.jsonl`, mean 710.4 chars, max 2,296 — that is the free-text tier, and it is what
placebo P2 uses. `reasoning_transparency` is **also non-null on 2,148 rows of that file**, but
it is **a binary float flag (1.0 on 1,673 rows, 0.0 on 475), not free text** — version 1 listed
it inside a sentence about free text, which was the error. It is absent from
`trace_context.jsonl` entirely (0 of 6,465). `trace_level` splits detailed 1,928 / generic
2,389 / full_traces 2,148.

**The object mismatch, and the audit that settles it.** The report's "99% variance horizon:
11 dimensions" is a PCA/eigen-statistic over **engineered scalar telemetry columns**, not over
semantic embeddings, and not over a 12-class taxonomy. Version 1 proposed to resolve the 11 by
"sweeping documented column subsets" — an unbounded search over up to 2^25 subsets with no
pre-specified list, no multiplicity control and no stopping rule, which could only manufacture
a false confirmation of the very numerology it claimed to guard against. **That sweep is
deleted.** In its place, a three-subset audit, all three reported, run and recorded here:

**AUDIT 1 — the shipped 8 signals on the qa_eval subset** (exactly what
`/home/emoore/RATCHET/stability-analysis/trace_audit.py` does: `task_class == 'qa_eval'`,
`dropna` on csdma_plausibility_score, dsdma_domain_alignment, entropy_score, coherence_score,
optimization_veto_entropy_ratio, tokens_input, tokens_output, processing_ms). n = 1,768
complete rows. Correlation-matrix eigenvalues:

    [2.633, 1.131, 0.960, 0.886, 0.819, 0.719, 0.502, 0.351]

| statistic | reproduced | `EMPIRICAL_REPORT.md` §2.1 says | verdict |
|---|---|---|---|
| 90% variance horizon | **7** | 7 | ✅ reproduces exactly |
| 99% variance horizon | **8** | 11 | ❌ and **8 is the full rank of an 8×8 matrix** — 11 is unreachable in principle |
| participation ratio | **5.575** | 6.61 | ❌ off by 19% |

**AUDIT 2 — all 25 numeric-capable columns** and **AUDIT 3 — the shipped 8 on all 6,465 rows
rather than the qa_eval subset** are to be run and reported for completeness. Neither can
rescue the 11 as a *reproduction*, because the shipped script defines the object and it is
8-dimensional; they are reported so the record shows what a wider or wider-rowed matrix does
give.

**K5 IS FIRED, BY INSPECTION, BEFORE THE MAIN RUN.** `EMPIRICAL_REPORT.md` §1.2 — two
paragraphs above the cited §2.1 — states in its own words:

> The value **11.5** represents the **Required Effective Dimensions** (k_eff) for achieving a
> 99% reduction in reasoning ambiguity, **assuming a standardized decay constant λ = 0.4**.
> Calculation: −ln(0.01)/0.4 ≈ 11.51.

The parsimonious reading is that §2.1's "intrinsic rank of 11" is §1.2's heuristic transplanted
into an empirical slot, not a measurement of any object. The companion statistic that *is* a
measurement — the 90% horizon of 7 — reproduces exactly from the shipped 8 columns; the 11 does
not and cannot. Adding columns to reach 11 would move the 7, which currently reproduces.
`/home/emoore/CIRISOntology/scratchpad/LEAN2_CONFRONTATION.md` line 56 **already says this**
("its k_eff=11.5 is a calculation (−ln .01/.4) and carries no weight"); version 1 of this
prereg claimed to have read that note in full and never connected the two, converting a
resolved question into a budgeted forking-paths computation. That was defect h2 and it is
corrected here.

**Consequence, frozen: RATCHET is SECONDARY, cannot support or kill P1, and its leg of the
"three objects share the integer 11" claim is now DEAD.** It enters twice and only twice:
* **(R-audit)** the three pre-specified subsets above; all three reported; K5's verdict already
  recorded as FIRED (§16-K5).
* **(R-placebo)** the 2,148 `action_rationale` texts are a non-change-describing corpus of
  comparable size and register; they serve as **placebo corpus P2** in §13.

The design note's "three objects share the integer 11" therefore stands on **at most two legs**
(Clifford-algebra cap; site-model image) **before this experiment runs**, and the note must be
amended to say so regardless of how the measurement lands. That amendment is now owed
unconditionally, not contingently.

## 3. Instrument — the embedder, frozen

* **PRIMARY:** `BAAI/bge-large-en-v1.5` via the DeepInfra OpenAI-compatible embeddings
  endpoint `https://api.deepinfra.com/v1/openai/embeddings` (verified served, 2026-08-18).
  1024 dimensions, 512-token context. **No instruction prefix** (symmetric use, not retrieval).
  Batch size 64 texts per request.
* **SECONDARY (witness-diversity arm, required):** `Qwen/Qwen3-Embedding-0.6B` (different
  family). The headline verdict must replicate in **sign and band membership** on the
  secondary, else the finding is published as **EMBEDDER-DEPENDENT** and not promoted. Same
  family ≠ second witness (house rule: `shared-lemma-one-witness`).
* **FALLBACK if either is unserved or truncates:** `BAAI/bge-m3` (1024-d, 8,192-token
  context). Local fallback is **not available**, corrected (defect m3): `sentence_transformers`
  **is** installed in this environment but `torch` is **not**, so the installed
  `sentence_transformers` cannot run a model. Installing `torch` is an amendment, not a default.
* **Truncation budget, scoped (defect m4).** *Artifact corpora* (A, A-held, BAB, B): longest
  single text is **1,273 chars** (`eco_wiki2.jsonl`, id `wiki2-19`, `after` field), 0 of 1,098
  texts exceed 2,048 chars; expected truncation **0**. *RATCHET rationales* (placebo P2 only)
  run longer: max **2,296** chars, **33 exceed 1,273** and **14 exceed 2,048** (≈ >512 tokens).
  14/2,148 = **0.65%**, below V7's 2% threshold, so V7 does not fire — but the exposure is on
  the record rather than inside an unqualified sentence. §15-V7 governs if the measured rate is
  worse than this.
* **Determinism gauge, run first.** Embed 20 fixed texts twice in separate requests. Record
  median cos(e₁,e₂). ≥0.9999 → deterministic, proceed. <0.999 → **VOID** (§15-V2).
* **Caching.** Every vector cached to
  `/home/emoore/CIRISOntology/scratchpad/eigen_cache_<model-slug>.jsonl`, keyed by
  `sha256(model || "\x00" || text)`. The cache file's sha256 is recorded in the results file
  so the run is auditable and re-runnable.

Cost, corrected (defect m6): ≈ **9,700** texts, not 6,500 — Corpus A 496, part_d 24, Babel 20,
Corpus B 558, reason texts 5,377, RATCHET rationales 2,148, span arm ≈1,098, determinism gauge
40. At ≤320 tokens each that is ≈3.1 M tokens per embedder, still well under $0.10 total.
Hard cap **$3.00**; abort and report if exceeded.

## 4. The matrix PCA runs on — frozen: the difference vector

For every item, PCA runs on the **document-level change vector**

    Δᵢ  =  normalize( ê(afterᵢ) − ê(beforeᵢ) ),      ê(x) = e(x)/‖e(x)‖₂

with `before`/`after` embedded **separately and verbatim** (no template, no site text, no
author note), and the cloud **column-centred on the fitting set only** before SVD.

**Why this and not a templated change description — now a measurement, not a judgement call.**
The templated route would have to carry `variation_site` or `author_note`, and both were
written by us with the target kind in mind. How much that leaks is measured, not asserted
(5-fold stratified TF-IDF 1–2 gram + logistic regression, chance = 1/12 = 0.083):

| predictor → `kind_target` | accuracy | ratio to chance |
|---|---|---|
| `variation_site` (author's description of the change) | **0.642** | 7.7× |
| changed span (mechanical diff) | **0.170** | 2.0× |
| `before` (the *unchanged* document) | **0.149** | 1.8× |
| `before` → `domain` (sanity: the text does carry strong structure) | **0.972** | — |

The author's description leaks **3.8× more label information than the change itself**. That
converts "the templated route is circular" from a judgement call into a number, and it is why
the difference vector is the primary. (It also, uncomfortably, shows that the *unchanged*
document carries almost as much kind signal as the change does — 0.149 vs 0.170. That is
placebo P1's whole point and §13 is rebuilt around it.)

**"Leakage-free" qualified (defect h9).** Δ is **leakage-free with respect to author-written
change descriptions** — it is a mechanical function of the two artifact states only, and it
cancels the shared topic. It is **not** leakage-free with respect to, and the following are
named as the nuisances it does not remove: **(i) generation batch** (§2.1a, 0.573 detectable),
**(ii) changed-span size** (§2.1b, 87× spread, p = 7.6e-16), **(iii) domain/stream**,
**(iv) our own authorship of the corpus** (§19-D6).

**Item-level unit normalization of Δ is deliberate**: it removes edit *magnitude*, which would
otherwise dominate PC1 and manufacture a spurious "first content direction". The un-normalized
cloud is computed and reported as a sensitivity arm, never as the headline.

**Secondary arm (span-only, leakage-free):** Δ_spanᵢ from a mechanical `difflib`
character-diff of before/after — embed the changed span from each side inside the fixed
carrier `"The text reads: <span>"`. Reported alongside; not the headline.

**Nuisance residualization (pre-registered, all arms reported).** From each Δ, regress out
(i) log₁₀(1 + changed-span character count), (ii) domain one-hot (Corpus A: 5 domains) or
stream one-hot (Corpus B: 5 streams), and — **added in version 2 (defect M1)** —
(iii) **generation-batch one-hot** (`part` ∈ {a, b, c}), Corpus A only. Fit the nuisance
regression **on the fitting half only** and apply to the held-out half.
**The residualized arm is the PRIMARY.** The raw arm is reported next to it.

**Stated cost of the batch term, in advance:** because kind is nearly nested in batch,
regressing out `part` also removes any genuine kind signal that is collinear with the 6/6
split. The batch term therefore makes P1a **harder to pass and biased toward the null** — an
acceptable direction for a control, and declared now so a WEAK result cannot later be blamed
on it retroactively. The within-batch arm (§9-P1a-batch) is the complementary control that
does *not* pay this cost, and V11 is what makes the pair binding.

This is a pre-registered control, not a post-hoc residual — and no residual is ever quoted as
support (rule 6).

## 5. Discriminator directions — frozen

**Label source: authored `kind_target`, primary.** Reasons, stated in advance: (a) it is the
design's intended coordinate and is independent of the annotator instrument whose confusions
are already measured and known (Premises→Facts, Structure→Manner, Model↔Facts); using panel
modals would import exactly those confusions into a claim about "the coordinate system";
(b) it is balanced by construction (20–24 per class), which centroid contrasts need;
(c) panel modal labels are severely unbalanced (Facts 1,083 votes vs Premises 70), so several
classes would fall under the §15-V3 support floor.
**Secondary arm: panel modal label at BASE** (majority of 3 in-vocabulary votes; §2.3's
off-vocabulary rule applies; ties broken by dropping the item). Reported alongside. **If the
two arms disagree in verdict, the finding is INSTRUMENT-DEPENDENT and is published as such —
not resolved by picking the friendlier one.**

**Construction: class-centroid contrasts, not fitted classifiers.**

    w_k  =  normalize( mean{Δᵢ : label(i)=k}  −  mean{Δᵢ : label(i)≠k} )

Logistic/LDA discriminators are **excluded by design**: at n≈20 per class in 1024 dimensions
they overfit to separability that the permutation null would then have to chase. Centroid
contrasts are stable at this n, have no hyperparameters, and are the standard concept-direction
construction.

### 5.1 THE COUNTING IDENTITY — stated exactly, and this time obeyed (defects C1, h1)

For one-vs-rest centroid contrasts on N items with class sizes n_k and grand mean μ,

    c_k  =  m_k − m_{¬k}  =  N·(m_k − μ) / (N − n_k),        and       Σ_k n_k (m_k − μ) = 0.

So the 12 un-normalized contrasts satisfy **one exact linear relation**, and:

* the 12 contrasts span **exactly 11 dimensions**, for any labelling of any corpus whatsoever;
* **any 11 of them span the same 11-dimensional between-class subspace as all 12**;
* therefore `w_Record` lies **exactly inside** the span of the other eleven. Verified
  numerically at Corpus A's exact half sizes (10×10 + 12×2 = 124) on pure Gaussian noise in
  d = 1024: rank(12 contrasts) = **11**, rank(first 11) = **11**,
  ‖w_Record − Proj_{S_kind} w_Record‖ = **1.3e-15**, ‖Proj_{S_kind} w_Record‖² = **1.0000**;
* a twelfth *between-class* direction **cannot exist** for a 12-class partition, so "is Record
  a twelfth direction?" is not a well-posed question about this construction.

**Version 1 named this hazard in bold and then walked into it** by declaring `w_Record` "kept
separate throughout" (defect h1). It is not separate and cannot be made separate inside a
12-class contrast basis. The consequences, all binding:

* "the discriminator subspace has rank 11" is a counting identity and **is never reported as a
  result**;
* "canonical correlations between 12 one-hot labels and anything cap at 11" is the same
  identity and **is never used as the rank statistic**;
* **Ω(11) is not Record-free.** `S_kind` built from the 11 base contrasts is numerically
  identical to the span of all 12. Every sentence about Ω must say "the 12-class between-class
  subspace", never "the 11 kinds' subspace excluding Record". This is a wording obligation on
  the results file, checked at write-up;
* the rank statistic (§6) is a count over **principal components of a held-out unlabelled
  cloud**, which is free to return any integer in 0…40;
* the alignment statistic is compared against a **label-permutation null that preserves the
  identity** — the permuted contrasts also span 11 dimensions, so the identity cancels exactly.
  (The referee independently confirmed this null is correctly constructed: at zero planted
  signal, median Ω(11) = 0.0116 against k/d = 0.0107, with a tight band. **N1 is the strongest
  part of this design and is kept verbatim.**)

`S_kind` := the span of the 12 contrasts (= the span of any 11 of them), orthonormalized by QR,
**dimension 11, and it contains `w_Record`**.

### 5.2 The identity-free construction: leave-one-kind-out (LOKO) — new in version 2

To ask "does kind k behave like a content class the cloud recovers?" *without* the identity, the
held-out kind must be outside the fitted span. For **each** kind k of the 12, symmetrically:

1. Remove **all** items of kind k from the fitting half.
2. Fit the 11 remaining one-vs-rest contrasts on what is left. By §5.1 they span **exactly 10**
   dimensions, for every k. Call this `S_{−k}` (dim 10, identical rank for all 12 kinds).
3. Form `ĝ_k` := normalize( mean{Δ : kind = k} − mean{Δ : kind ≠ k} ) on the fitting half.
   **`ĝ_k` was never in the fit**, so nothing forces it into `S_{−k}`.
4. On the **held-out** half, compute `A_k := ‖Proj_{U_11} ĝ_k‖²` — how much of direction k lies
   in the held-out top-11 principal subspace. Chance for a random direction is 11/1024 = 0.0107.
5. Compute `ρ_k` := median |cos| between `ĝ_k` fitted on the two independent halves of a split,
   over the 200 splits — direction replication.
6. **`η_k := A_k · ρ_k`** — the *replicable* principal-subspace loading of kind k.

`η_k` is the P2-neg primary statistic. It is symmetric across all 12 kinds, identity-free for
the held-out kind, and it is zero in both degenerate directions: pure noise gives ρ → 0, and a
direction fully absorbed by the other eleven gives A → the projection of a mixture, which the
N1 null prices correctly. All 12 `η_k` are reported in one table.

## 6. Statistics — frozen

Let `U_k` = top-k right singular vectors of the centred held-out cloud, `B` = orthonormal
basis of `S_kind` (11 columns; §5.1 — this is the full 12-class between-class subspace).

* **Subspace alignment** `Ω(k) = (1/r)·‖U_kᵀB‖_F² = (1/r)·Σᵢ cos²θᵢ` over the principal
  angles θᵢ, where **`r = rank(B)`**, normally 11 but **reduced when §15-V1 marks classes
  UNMEASURED** (defect M7). Ω ∈ [0,1]; Ω=1 iff `S_kind ⊆ span(U_k)`. `r` is reported beside
  every Ω. Chance for random subspaces in d=1024 at k=11 is k/d = 0.0107 — quoted only as a
  scale, never as the null.
* **Per-PC kind loading** `a_j = ‖Bᵀu_j‖²` ∈ [0,1] for j = 1…40: the fraction of principal
  direction j lying in the kind subspace. Note `Σ_{j=1}^{d} a_j = r` exactly, which makes the
  40 tests **negatively dependent** — this is why §7 uses maxT and not BH (defect M4).
* **Kind rank** `R_kind` := #{ j ≤ 40 : a_j significant vs the label-permutation null under the
  **permutation maxT step-down** procedure at family-wise α = 0.05 }. **R_kind is free to take
  any value 0…40.** `R_kind` counts *ranks at which kind loading exceeds the permutation
  floor*; it does **not** assert that PC j is a reproducible direction (§19-D8).
* **LOKO loadings** `A_k`, `ρ_k`, `η_k` for all 12 kinds (§5.2). Primary for P2-neg.
* **Identity-bound loading** `a_Record(11) = ‖Proj_{U_11} w_Record‖²` from the full 12-class
  fit — **reported as a secondary with §5.1's identity disclosed beside it**, never as the
  primary, because `w_Record` is a fixed linear combination of the other eleven contrasts and
  its expected value sits near their weighted *mean*, not near their min (defect M10).
* **Record separability** `AUC_Record` := leave-one-out cross-validated one-vs-rest AUC of the
  centroid-contrast score in the **full** 1024-d space, **reported with a 95% bootstrap CI
  (2,000 resamples) and with the same quantity and CI for all 11 other kinds** (defect M9).
* **Frame projection** (P2-pos) `π_k(T)` — defined in §11, **second-moment form**.

k is swept over {5, 7, 9, 11, 13, 15, 20, 30, 40}; **k = 11 is the pre-registered primary and
no other k may be promoted post hoc.**

## 7. Nulls — frozen, with the schedule pinned (defect M4)

* **N1, label permutation (the rule-5 floor).** Permute `kind_target` across all 248 Corpus A
  items, then run the **entire** 200-split pipeline on the permuted labels and take the median.
  **N_perm = 500** such whole-pipeline permutations. p = (1 + #{null median ≥ obs median}) /
  (1 + 500); **minimum reportable p = 2.0e-3**, which clears the p < 0.01 bar with margin.
  Permutation is **free (unstratified)** — declared conservative in direction, because permuted
  classes lose kind×domain and kind×batch balance and can therefore pick up domain or batch
  structure that the real labels also carry, raising the floor.
  * **Pinned schedule.** The half-2 SVD is invariant under half-1 label permutation, so the 200
    split SVDs are computed **once** and reused across all 500 permutations; only the 12
    centroid means, the 11-column QR, and the Frobenius product recompute. ≈2.5e10 flops total,
    minutes in numpy.
  * **Pinned combination rule.** The observed statistic is the **median over the 200 splits**;
    the null is the **distribution of that same median over the 500 permutations**
    (null-of-medians, permutation index shared across splits). No per-split p-values are
    computed and none are combined.
  * **Pinned multiplicity.** Because `Σ_j a_j = r` exactly, the 40 per-PC tests are negatively
    dependent and BH's PRDS assumption **does not hold**. Version 1's "BH FDR q = 0.05 over the
    40 tests" is **deleted**. Replaced by **permutation maxT step-down** (Westfall–Young) at
    family-wise α = 0.05 over the same 500 permutations.
* **N1b, span-stratified label permutation (new; required conjunct — defect M2).** Identical to
  N1 except labels are permuted **only within changed-span decile blocks**, which preserves the
  kind↔span relation exactly. This is the only null that tests alignment *beyond edit size*.
  N_perm = 500, same schedule and combination rule. Ω is additionally reported conditional on
  span decile.
* **N2, split-halves.** **N_split = 200** stratified random splits of Corpus A, stratified
  jointly on `kind_target` (12 levels) and `domain` (5 levels); fit contrasts on half 1, PCA on
  half 2, then swap and average. All headline numbers are medians over the 200 splits with
  [2.5, 97.5] percentile intervals.
* **N3, any-swap floor (P2-pos).** For the displacement statistics, the floor is the
  displacement produced by a *random* distinct condition pair drawn from the seven, item-paired
  (the pre-registered generalization of the PLANE study's post-hoc W-as-floor). 2,000 draws.
  **Applied to the second-moment statistic of §11, identically.**
* **N4, partition comparators (new — defect M6).** Two rival 12-way partitions, both fitted and
  evaluated by the identical pipeline: **(i) k-means-12** on the fitting-half Δ cloud (the
  honest ceiling any partition can reach), **(ii) a semantically-coherent non-taxonomy
  partition**: domain (5) × changed-span tercile (3) = 15 cells, collapsed to 12 by merging the
  three smallest. Paired within each of the 200 splits.
* **Granularity is the document** (rule 3): every permutation and every split operates on whole
  items, never on tokens or on before/after halves.

## 8. Rank-resolution gauge — re-staked (defect C4), runs BEFORE any corpus embedding

House lesson `forward-prediction-confirmed`: *gauge the ruler with planted values before
staking a band.* Synthetic clouds with **planted ranks 7, 11, 13**: n = 124 (the size of a
Corpus A half), d = 1024, class sizes exactly Corpus A's halves (10 × ten classes, 12 × two
classes), r planted class-carrying directions plus isotropic Gaussian noise.

### 8.1 Why version 1's grid was dead, with the arithmetic

At n = 124, d = 1024, ~10 per class, class-mean sampling noise has norm √(d/n_k) ≈ 10.1, while
an 11-dimensional planted offset at per-coordinate scale s has norm s·√11 ≈ 3.3s. Detection
therefore needs s ≳ 3. Version 1 staked the grid **{0.05, 0.10, 0.20, 0.40, 0.80}** — entirely
inside the undetectable regime. A synthetic pilot (15 reps/cell, planted rank 11, exact Corpus A
half sizes; **no embedding, no corpus text**) confirms it:

| scale ×σ | 0.00 | 0.05 | 0.10 | 0.20 | 0.40 | 0.80 | 1.50 | 3.00 | 4.00 | 6.00 | 9.00 | 12.0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| median Ω(11) | .0116 | .0101 | .0104 | .0105 | .0106 | .0126 | .0397 | .1970 | .2983 | .4438 | .5926 | .6595 |

Chance is k/d = **0.0107**. Every cell of version 1's grid reads chance. §8's definition of σ_R
("over the scales where the mean recovered rank is within ±3 of planted") would therefore be
taken over the **empty set**, leaving σ_R undefined — and with it P1b's band and V8 both
unevaluable. That was defect C4.

### 8.2 The re-staked grid, frozen

Offset scale is swept over **{0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 9.0}** × the within-class σ,
**200 draws per cell**, and `R_kind` is recorded for every (planted rank, scale) cell. This grid
is chosen so that median Ω(11) spans ≈[0.01, 0.60] and **straddles the P1a floor of 0.25 at
scale ≈ 3.5** — that is, the gauge brackets the band it is gauging.

**Disclosure (defect h4).** The grid is now chosen **by dimensional analysis and a synthetic
pilot**, not left untuned. Version 1's "the signal scale is not tuned to match anything
observed" was correct discipline that produced a dead instrument: untuned is not well-chosen.
The grid is tuned to **synthetic** detectability only; no corpus embedding exists and none was
consulted.

Define **σ_R** := the largest across-scale standard deviation of `R_kind` at planted rank 11,
over the scales where the mean recovered rank is within ±3 of planted. **If that set is still
empty on the re-staked grid, V8 fires automatically and the rank leg is demoted before the
measurement.** σ_R is never undefined at write-up time.

### 8.3 Two further quantities the gauge must return (defects C3, C6)

* **ρ_gauge — centroid-contrast replication at n ≈ 10/class.** Median |cos| between the same
  kind's contrast fitted on two independent synthetic halves, recorded at every grid cell.
  Feeds **V3b**.
* **PC-direction replication by rank j.** Median |cos(u_j^{half1}, u_j^{half2})| for
  j = 1, 2, 3, 5, 8, 11, 13, at every grid cell. The pilot already shows why this matters
  (15 reps, planted rank 11):

  | scale ×σ | 0.00 | 0.80 | 1.50 | 3.00 | 4.00 | 6.00 | 9.00 | 12.0 |
  |---|---|---|---|---|---|---|---|---|
  | PC j=1 | .017 | .019 | .298 | .744 | .844 | .923 | .965 | .980 |
  | PC j=5 | .028 | .031 | .022 | .314 | .573 | .737 | .885 | .933 |
  | PC j=11 | .026 | .027 | .017 | .015 | .024 | .033 | .041 | .031 |

  **At scale 12 — where Ω(11) = 0.66, far above P1a's floor — PC #11 still replicates at
  0.031, i.e. chance.** At n = 124 in d = 1024 (γ = 8.26, deep sub-BBP), individual principal
  directions beyond roughly the top 2–4 are **not estimable**. Version 1's K3 required
  `∃ j ≤ 13` replicating at |cos| ≥ 0.7, and P1b required "≥3 of PCs 8–11 individually
  significant" — both ask about directions that do not exist as reproducible objects at this
  n. **Both conjuncts are deleted** (defect C6); see §9-P1b and §10-K3.

### 8.4 Staked consequences, before data

| gauge result | consequence, automatic |
|---|---|
| σ_R ≤ 0.66 | **the sharp clause lives**: P1b Tier 2 is evaluated, band `R_kind ∈ {10, 11, 12}`, and "not 7, not 13" is a falsifiable-by-passing claim |
| 0.66 < σ_R ≤ 1.5 | "not 7, not 13" is **RETRACTED in advance**; P1b is Tier 1 only, band `|R_kind − 11| ≤ 2σ_R`; §1 is amended before data |
| σ_R > 1.5 | **V8 fires**: the rank leg cannot kill at all; `R_kind` is reported as a descriptive integer with its interval and no band verdict |
| σ_R undefined (empty admissible set) | treated as σ_R > 1.5 |
| ρ_gauge < 0.30 at the scale where Ω(11) ≈ 0.25 | **V3b fires**: centroid contrasts are unresolved at 10/class, the split-half primary is VOID, and the design falls back to the cross-corpus arm with that stated plainly |

## 9. P1 — staked bands

**P1a — alignment (primary: Corpus A split-half, residualized arm incl. batch term, primary
embedder, k = 11).**

| outcome | band | reading |
|---|---|---|
| **PASS** | median Ω(11) over 200 splits exceeds **both** the N1 and the N1b null at p < 0.01, **and** median Ω(11) ≥ **0.25**, **and** Ω_taxonomy > Ω_nontaxonomy paired at p < 0.01 (N4-ii), **and** V11 does not fire | the 12-class between-class subspace is substantially inside the top-11 principal subspace of an independent half, beyond edit size, beyond an arbitrary 12-way partition, and not explained by generation batch; the eigen-bridge has support |
| **WEAK** | any null cleared at p < 0.01 but median Ω(11) < 0.25 | statistically real, practically small: reported as a detected but weak alignment; **no promotion to the stance** |
| **KILL (K1)** | p ≥ 0.01 against N1 **or** against N1b | the alignment leg is dead — see §16-K1 |
| **KILL (K1b)** | Ω_taxonomy ≤ Ω_nontaxonomy (N4-ii) | alignment may be real but the **taxonomy is not privileged among 12-way partitions** — see §16-K1b. Separable from K1 |

The absolute floor **0.25 is unchanged from version 1** and is deliberately modest: k/d chance
is 0.0107, so 0.25 is ~23× chance, and an eleven-direction subspace recovering a quarter of its
mass in eleven of 1,024 held-out directions is a real effect while being reachable. Per §8.2's
pilot it corresponds to a class separation of ≈3.5σ.

**P1a-batch — the batch-free control (new; binding via V11 — defect M1).** Fit and evaluate the
identical pipeline **within part_a alone** (6 classes, between-class rank 5, n = 120, halves of
60 at 10/class) and **within part_b alone** (same shape), each with its own N1 null at the
appropriate rank r = 5. Alignment surviving *within* a single generation batch is the **only
batch-free evidence this corpus can supply**. Stake: **V11 fires** — P1a is VOID — if the pooled
Ω(11) passes while **both** within-batch arms fail their own N1 at p ≥ 0.01. A void is not a
caveat: the pooled pass is then attributed to batch and is not reported as alignment.

**P1b — rank, two tiers (defects C5, C6, h7).**

| tier | condition to evaluate it | outcome | band |
|---|---|---|---|
| **Tier 1** (always) | — | **CONSISTENT** | `\|R_kind − 11\| ≤ 2σ_R`, σ_R floored at 1 → at worst [9, 13] |
| | | **INCONSISTENT (K2)** | outside that band while P1a passed |
| **Tier 2** (sharp) | **only if §8 returns σ_R ≤ 0.66** | **PASS** | `R_kind ∈ {10, 11, 12}` — excludes 7 and excludes 13 |
| | | **KILL (K2)** | `R_kind` outside {10, 11, 12} while P1a passed |
| **UNDECIDED** | P1a killed or VOID | — | the rank leg is not evaluated (no alignment to count) |

Version 1's Tier-2-equivalent band was `|R_kind − 11| ≤ 3σ_R` with σ_R floored at 1, i.e.
⊇ [8, 14] — **which contains 13**, so "not 13" could have PASSED at R_kind = 13 (defect C5).
That band is deleted. Version 1's extra conjuncts — "≥3 of PCs 8–11 individually significant"
and "≤1 of PCs 12–15 significant" — are also **deleted** (defect C6): §8.3's pilot shows PCs at
those ranks do not replicate at this n even under strong planted signal, so those conjuncts ask
about non-objects. Per-PC replication is still **reported as a diagnostic** beside the a_j
spectrum.

If `R_kind` ≈ 7, report the measured count plainly and **do not** spin any coincidence with
RATCHET's 90% horizon of 7 — §2.4 has established the two are ranks of different objects, and
RATCHET's 7 is now the *only* RATCHET statistic that reproduces, which makes the coincidence
more tempting and no more meaningful.

**P1c — transfer (secondary, cross-corpus).** Contrasts from **all** of Corpus A; PCA on
**Corpus B** (wild, 279 items, labels unused), after §15-V4's per-stream deduplication.
Ω_B(11) with the same N1 and N1b nulls.
PASS: p < 0.01 on both and Ω_B(11) ≥ 0.15. FAIL: p ≥ 0.01 — reported as **"does not transfer to
wild streams"**, which does **not** kill P1a, because B's kind coverage is measured-skewed
(§2.2), its source concentration is 43% OSM (§2.2), and a null there is ambiguous by
construction. This asymmetry is declared now so that a transfer failure cannot be quietly
promoted into a kill, and a transfer success cannot be quietly promoted into the headline.

### 9.1 FORWARD PREDICTION, staked 2026-08-18 before any embedding exists (defects M5, h3)

Version 1 defended the 0.25 floor with "it is not a number chosen after seeing anything" —
true, and beside the point, because the document never asked whether 0.25 is **reachable**
(defect h3). A no-embedding power proxy was free to run and is now run (§4's table):
the changed span predicts kind at **0.170** (chance 0.083), barely above what the **unchanged**
document predicts (0.149). Cross-referencing §8.2's gauge, Ω(11) = 0.25 requires class
separation near 3.5σ — near-perfect separability, which a 2.0×-chance bag-of-words signal does
not suggest.

**Staked forward prediction, in advance, with the floor NOT lowered:**

> **Median Ω(11) on the primary arm will land in [0.02, 0.08] — the WEAK band — and P1a will
> not meet its 0.25 PASS floor.**

Meaning of every outcome, fixed now:
* **lands in [0.02, 0.08]** → a **confirmed advance prediction** about the instrument's reach
  (rule 6 support for the *power model*, not for the taxonomy), and P1a reads WEAK;
* **lands ≥ 0.25** → this prediction is **falsified** and P1a PASSES on a bar staked before the
  power proxy existed — which makes the pass *stronger* evidence, not weaker;
* **lands < 0.02 or fails N1/N1b** → K1 fires;
* **lands in [0.08, 0.25)** → prediction missed high, P1a still reads WEAK, and the miss is
  reported as a miss.

§19-D2 is amended accordingly: version 1 guessed the realistic field to be 0.10–0.20; the power
proxy says lower.

## 10. P2-neg — Record does not behave like a twelfth content class

Same primary setting as P1a (Corpus A split-half, residualized incl. batch, k = 11).
**Primary statistic: the LOKO η_k of §5.2, computed identically for all 12 kinds.**

| outcome | band | reading |
|---|---|---|
| **PASS** | (i) η_Record does **not** exceed its own N1 null's 95th percentile, **and** (ii) **≥ 6 of the 11 base kinds' η_k DO** exceed their own N1 null's 95th percentile, **and** (iii) η_Record ranks in the **bottom 3 of the 12** | the instrument demonstrably finds replicable principal content directions for most base kinds, and does not find one for Record: the relation-typing survives |
| **KILL (K3)** | (i) η_Record exceeds its N1 null's **99th** percentile, **and** (ii) ρ_Record ≥ 0.5 (the direction is stable across independent halves), **and** (iii) A_Record ≥ the median A_k over the 11 base kinds | a **stable, replicable content direction that tracks Record and is as principal as a typical base kind** — the relation-typing claim is killed, specifically and only |
| **INCONCLUSIVE** | anything else | "Record partially visible" — no promotion, no retraction |

**A-priori outcome probabilities, stated explicitly (defect h5).** Two hypotheses, priced
separately, because a band is only informative if the two differ:

* **H_null (Record is not a content direction, P2's own prediction).** Conjunct (i) holds with
  probability ≈0.95 by construction of the null. Conjunct (iii) — bottom 3 of 12 — holds with
  probability well above 0.25, since Record's η is genuinely small. Conjunct (ii) is a fact
  about the *other eleven* and is unaffected. So **PASS is the likely outcome under H_null**,
  which is what a well-posed confirmatory band should look like.
* **H_alt (Record behaves exactly like a base kind).** Conjunct (i) fails with probability
  ≈(the base kinds' detection rate, ≥6/11 by conjunct (ii)) — i.e. PASS is *unlikely*.
  Conjunct (iii) alone would hold at 3/12 = **0.25**, which is why (iii) is descriptive and
  never carries the verdict on its own.

So the evidential weight sits in the **conjunction of (i) with (ii)**: (ii) is what rules out
"the instrument found nothing anywhere", and without it (i) is vacuous. K3 under H_null has
probability ≈0.01 × P(ρ_Record ≥ 0.5 | noise) × ≈0.5, i.e. **well under 0.01**.

Version 1's PASS band ("a_Record ≤ min over the 11") was a
**1/12 = 0.083 event regardless of the hypothesis**, and combined with §5.1's identity — under
which `w_Record` is a weighted average of the other eleven and so is expected near their *mean*,
not their min — INCONCLUSIVE was the near-certain outcome (defect M10). The referee measured
`P(a_Record < min a_k)` across a full signal grid and found it flat at ≈1/12 and **not
increasing with signal**. That band is deleted.

**INCONCLUSIVE is an outcome, not an escape hatch (defect h5).** It is reported in the same
type size as PASS and KILL, and the results file must state which of the three conjuncts failed.

**Interpretability precondition (anti-vacuity), rebuilt (defects M9, C1).** A pass by *absence
of signal* is not a pass. The **primary** vacuity gate is now PASS-conjunct (ii): **≥6 of 11
base kinds detectable**. If fewer than 6 are, **P2-neg is VOID (§15-V5)** — the instrument
cannot see content directions at all and Record's absence means nothing.
`AUC_Record` is **demoted to a reported secondary** with a 95% bootstrap CI, alongside all 11
other kinds' AUCs with CIs, because with 20 positives its SE near 0.70 is ≈0.08–0.10 and a
bare threshold on it is close to a coin flip. **V5b** (secondary): if the **upper** bound of
AUC_Record's 95% CI is < 0.70, that is recorded as corroborating vacuity — it does not void on
its own.

**Secondary, with its identity disclosed:** `a_Record(11)` from the full 12-class fit, reported
next to the 11 base `a_k(11)`, with the §5.1 sentence "`w_Record` lies exactly inside the span
of the other eleven; its expected loading is near their weighted mean" printed in the same
table caption. It is never the primary and never carries a verdict.

**Named confound.** Record-target items were authored as artifacts about logs, minutes,
registers and audit trails; their surface topic may be linearly separable for purely lexical
reasons. The design does not assume this away — it **measures** it: high `AUC_Record` with low
`η_Record` is the exact signature of "separable but not a principal coordinate", and is the
result P2 predicts.

## 11. P2-pos — Record surfaces when the frame is supplied

Operationalized on the frame lever that already exists in the frozen study design (§2.3):
BASE/F1/F2 differ **only** in the Retention paragraph; W2/W3 differ from BASE **only** by an
attribution sentence, and the formal classifier is provably blind to attribution
(`warrant_invisible_to_kind`) — so W is the natural perturbation floor.

1. Embed `reason` text for every parsed judgment row (5,377 of 5,418; §2.3). Babel items are
   **excluded** (they share one base artifact and would dominate); n = 248 items.
2. Per item, per condition, average the 3 model vectors: `r̄(i,c)`.
3. Displacements: `D_frame(i) = r̄(i,F2) − r̄(i,BASE)`; `D_design(i) = r̄(i,D2) − r̄(i,BASE)`;
   `D_warrant(i) = r̄(i,W3) − r̄(i,BASE)`.
4. **Centre each displacement field on its corpus mean**: `D̃_T(i) = D_T(i) − mean_j D_T(j)`.
   This removes the constant lexical echo of the identical condition paragraph, leaving only the
   item-specific part. The step is mandatory, not optional.
5. **Projection statistic — SECOND MOMENT (defect C2):**

       π_k(T)  =  mean_i ⟨ D̃_T(i), ĝ_k ⟩²  /  mean_i ‖ D̃_T(i) ‖²

   the fraction of item-specific displacement *variance* lying along direction k. Chance for a
   random direction is ≈1/1024. `ĝ_k` are the **§5.2 LOKO directions** fitted on the
   **artifact-only Δ cloud** (never on reason text — that is the circularity guard here), used
   for all 12 kinds so the comparison is symmetric and identity-free.

   **Why the change.** Version 1's statistic was `π_k(T) = mean_i ⟨D̃_T(i), w_k⟩`, which by its
   own step 4 is `⟨mean_i D̃_T(i), w_k⟩ = ⟨0, w_k⟩ = **0**` — identically zero, for every kind,
   every condition, to float error. "π_Record(frame) is the largest of the 12" would have been
   decided by rounding noise, and the N3 floor would have been zero as well. V6 did not catch
   it, because V6 tests ‖D̃‖, which is non-zero. That was defect C2.
6. **Frame-lexicon control.** Primary arm strips a frozen stoplist from reason text before
   embedding: {retention, retained, survive, survives, surviving, survived, destroyed, sibling,
   siblings, consulted, consult, minimal, partial, "full retention", register, registers, log,
   logs, draft, drafts, record, records}. The unstripped arm is reported next to it. Fraction of
   reasons touched by the stoplist is reported. **Primary = stripped** (conservative).

| outcome | band | reading |
|---|---|---|
| **PASS** | `π_Record(frame)` exceeds the N3 any-swap floor at p < 0.01, **and** `π_Record(warrant)` and `π_Record(design)` do **not** exceed that floor, **and** `π_Record(frame)` is the largest of the 12 | the frame lever moves items along the Record axis and only the frame lever does: the relation shows up exactly where the type says it should |
| **NOT DEMONSTRATED** | `π_Record(frame)` within the N3 floor | Record's frame-conditionality is **not demonstrated by this instrument**. This does **not** kill P2 — a null instrument is not a refutation — but it is published as a half-supported pair, plainly |
| **SEPARATE KILL (K4)** | any base kind k ≠ Record has `π_k(frame)` above the floor at p < 0.01 | the artifact-locality of **that named kind** is contradicted at embedding granularity — a finding about that kind and about instrument sensitivity, not about Record |

The "largest of the 12" conjunct has a-priori probability 1/12 = 0.083 under exchangeability;
it is a **descriptive** conjunct and the **significance conjunct against N3 is what carries the
verdict**. Stated so it cannot be read as a 12× multiplier on the evidence.

**VOID for P2-pos** if the lever did not move anything item-specific: median ‖D̃_frame‖ ≤ 1.1 ×
median ‖D̃_warrant‖ (§15-V6). **V6b (new):** additionally VOID if
`mean_i ‖D̃_frame(i)‖² / mean_i ‖D_frame(i)‖² < 0.05` — i.e. if after centring, less than 5% of
the displacement energy is item-specific, the statistic of step 5 has no denominator worth
dividing by.

**Optional arm 3 (budgeted separately, ~1,500 calls, ≈$0.05; the orchestrator may cut it).**
Run the manipulation-check question ("Given the retention regime, can what changed still be
established from what survives? yes/no + one sentence") over Corpus A × {BASE-frame, F2-frame}
× 3 models — the same question the PLANE study asked post-hoc on 36 items and which the panel
answered 36/36 and 23/36. Staked **forward** prediction, before those items exist:
the item-level frame-flip indicator φᵢ is **not** predictable from the top-11 PCA coordinates
of the artifact-only Δ cloud (cross-validated AUC ≤ 0.60), while the artifact's own
Record-axis position `⟨Δᵢ, ĝ_Record⟩` **is** allowed to predict it (a log-heavy artifact may be
more frame-sensitive without Record being a content coordinate).
**Combination rule, pinned (defect h8):** version 1 said AUC > 0.75 from the top-11 PCA
coordinates "counts toward K3" — an unquantified fifth criterion bolted onto a kill §10 defines
by explicit conjuncts. That phrase is **deleted**. Arm 3 is a **standalone reported finding**:
AUC > 0.75 is recorded as **"the frame verdict is already latent in the artifact-only principal
directions"**, published under its own name, and it **does not enter K3's conjunction**. If the
steward wants it inside K3, that is an amendment, made before the arm runs.

## 12. Babel decathlon — the topic-confound control

Corpus BAB is **one artifact, ten edits, ten different kinds** — verified 10/10 sharing one
identical `before` text, so topic is held fixed by construction. Fit the 11 kind contrasts on
all of Corpus A (Babel is disjoint from it), then classify each Babel Δ by nearest contrast
direction (top-1 over the 11).

**Primary null: permutation over the 10 Babel labels** (all 10! assignments sampled at
N = 10,000), which accounts for the actual contrast geometry — nearest-direction assignment is
not 11 independent Bernoulli draws. The binomial is retained only as a scale.

**Binomial arithmetic, corrected (defect m5).** For n = 10, p = 1/11 the true values are
**P(X ≥ 3) = 0.0554, P(X ≥ 4) = 0.00915, P(X ≥ 5) = 0.00106**. Version 1 stated
P(X ≥ 5) ≈ 0.0025 and P(X ≥ 4) ≈ 0.014, both wrong, and the error mattered: **X = 4 already
meets this document's own p < 0.01 standard** while version 1 binned it "inconclusive".

Staked, with the discrepancy resolved deliberately rather than by arithmetic accident:
* **≥ 5/10 = PASS.** This is a **deliberately stricter bar than p < 0.01** (which ≥4 meets at
  p = 0.0092). The reason is stated in advance: with n = 10 and the referee-confirmed fact that
  the contrasts are not independent directions, a single lucky assignment at X = 4 is a thin
  reed for a control whose whole job is to be decisive about topic. 5/10 costs little and is
  clean.
* **4/10 = PASS-WEAK**, reported as "clears p < 0.01 on the binomial scale but below the staked
  bar", with the permutation p quoted as the operative number.
* **≤ 2/10 = FAIL.**
* **3/10 = inconclusive.**

**FAIL consequence, hardened (defect h6).** Version 1 said a FAIL means P1a's pass "must be
reported with that caveat attached" — elastic, with nothing retracted and nothing void. It is
now a named VOID: **V12** — Babel ≤ 2/10 **VOIDs P1a's interpretation**. The measured Ω is
still reported as a number; the sentence "the 11 kinds' directions carry kind" is not available,
because the directions were shown to be topic-driven on the one corpus where topic is held
fixed. This matches §13's Placebo P1, which correctly carried a kill.

Babel carries no `testimonial` and no `contingent` item, so this control says nothing about
Record and nothing about Circumstances.

## 13. Placebo corpora — where the alignment must NOT appear

* **Placebo P1 (same items, no change) — rebuilt (defect M3).** Version 1 compared the top-11
  before-cloud PCs against `S_kind`, which is defined on the **Δ** cloud. Δ-contrasts and
  before-cloud PCs live in different spaces and are near-orthogonal for trivial reasons, so
  Ω_before would have come back at chance and the placebo would have **passed vacuously** —
  inverting the control. And "the difference exceeding the N1 null at p < 0.01" was undefined,
  since N1 nulls Ω on one cloud, not a difference across two clouds. The control is **live and
  needed**: `before` text alone predicts kind at **0.149** vs chance 0.083 (1.8×), only just
  below the changed span's 0.170.

  **Rebuilt procedure, frozen:** build `S_kind^before` from **before-cloud** centroid contrasts
  on the **same fitting half**, and compute `Ω_before(11)` against the **before-cloud** held-out
  PCA — i.e. the identical pipeline run end-to-end on the before cloud. Compare `Ω_before` to
  `Ω_Δ` **paired within each of the 200 splits**. Null the paired difference by **permuting the
  Δ/before assignment within each split** (N_perm = 500).
  **Staked:** `Ω_Δ − Ω_before` must be **> 0 at p < 0.01** under that paired null. If the
  before-only topic cloud aligns as well as or better than the change cloud, the statistic is
  reading topic, not change — **that alone kills P1a's interpretation** even if P1a "passed"
  (kill K1c, §16).
* **Placebo P2 (RATCHET rationales):** 2,148 `action_rationale` texts from
  `accord_traces.jsonl`, embedded as single documents (no Δ — there is no before/after there;
  the placebo is deliberately a *different* object and is labelled as such). Report the
  parallel-analysis rank of that cloud. Staked meaning: **none for P1**. It exists to prevent
  the sentence "the rank came out 11 again" from being written about an unrelated corpus
  without its own null. If its rank is also ≈11, that is a fact about embedding clouds of ~2k
  short documents, and it **weakens** the taxonomy reading rather than supporting it — recorded
  in advance, in that direction. Note §3's truncation exposure: 14 of these 2,148 exceed 2,048
  chars (0.65%), below V7.

## 14. Circularity — the split, specified

The hazard: discriminator directions and principal directions estimated from the same items
guarantee alignment (the contrasts are literally functions of the cloud). Four defences, all
pre-registered:

1. **PRIMARY — stratified split-half on Corpus A.** 200 random splits, stratified jointly on
   `kind_target` (12) and `domain` (5). Contrasts (and the nuisance regression) fit on half 1;
   centring, SVD, and all statistics on half 2; then swapped; results averaged. **No item ever
   contributes to both sides of a single split.** Chosen as primary because Corpus A is the only
   corpus with balanced coverage of all 12 kinds (20–24 each).
   **Realised class sizes in a half: 10 for ten classes, 12 for two** (§15-V3 is re-staked to
   this arithmetic — defect C3).
2. **SECONDARY — cross-corpus transfer.** Contrasts from all of Corpus A; PCA on Corpus B (wild,
   labels never used). Stronger claim, weaker floor: see §9-P1c for why its failure cannot kill.
3. **The label-permutation nulls (N1 and N1b) run inside every arm**, so any alignment that
   survives is alignment beyond what an arbitrary 12-way partition of the same cloud would
   produce, and beyond what edit size alone would produce.
4. **Rival-partition comparators (N4) run in every split** — k-means-12 as the upper comparator
   and the domain×span-tercile partition as the non-taxonomy rival. Version 1 had a floor
   (random labels) and **no upper comparator at all**, so a P1a pass would have supported only
   "*an* authored 12-way partition of Corpus A is recoverable in held-out change-embeddings",
   not "**these** 11 are the coordinate system" (defect M6). **Reported always:** Ω_taxonomy,
   Ω_kmeans, Ω_nontaxonomy, and the gap Ω_kmeans − Ω_taxonomy.

Corpus A-held (`part_d.jsonl`, 12 items, **three kinds only** — §2.1) is reserved and untouched
until all primary numbers are written down; it is then scored once, reported once, and can only
add caveats — never promote. Its three-kind coverage is stated wherever it is quoted.

## 15. VOID conditions — thresholds staked, all numeric

| id | condition | threshold | consequence |
|---|---|---|---|
| **V1** | embedding degeneracy, **applied per class** (defect M7) | for a class: median cos(ê(before), ê(after)) > 0.999, or median ‖Δ_unnormalized‖ < 1e-3 | that class is **UNMEASURED**, its column is dropped from `B`, `rank(B)` falls, and **Ω renormalizes by 1/rank(B)** with the reduced rank reported. If the **global** median over all items also breaches, VOID everything |
| **V1b** | too few classes survive V1 | rank(B) < 8 | **VOID everything** — fewer than 8 measurable classes is not a test of an eleven-direction coordinate system |
| **V2** | instrument nondeterminism | median cos over the 20-text re-embed gauge < 0.999 | VOID (a non-reproducible instrument cannot carry a permutation test); 0.999–0.9999 → record as a noise floor and continue |
| **V3** | class support, **re-staked to the arithmetic** (defect C3) | any class with **n < 9** in a fitting half → that direction is **UNMEASURED**, not zero; **> 2 classes below 9** → **that arm VOID** | a stratified half of Corpus A delivers **10** per 20-item class and **12** per 24-item class. Version 1's threshold of 15 put **all twelve** classes below the floor, VOIDing the primary arm by arithmetic before any data — while §8 simultaneously specified the gauge at "12 classes of 10–11 items". 9 is the floor a half actually clears with margin |
| **V3b** | centroid resolution at 10/class (new — defect C3) | §8.3's ρ_gauge < 0.30 at the grid scale where median Ω(11) ≈ 0.25 | **split-half primary VOID**; fall back to the cross-corpus arm and say so plainly. This is the gauge-based justification version 1 asserted but never measured |
| **V4** | near-duplicate ties, **per stream** (defect M11) | within a stream: fraction of items in cos(Δᵢ,Δⱼ) > 0.99 clusters > 5% → **deduplicate to one per cluster within that stream** and report n_eff per stream; > 20% → **drop that stream** and report Corpus B's composition after the drop | version 1 left the granularity undefined and Corpus B is the *union* of three files, so a single stream's failure would ambiguously have voided B and P1c with it. **B is never voided wholesale by V4**; streams are dropped or re-weighted, and the surviving composition is reported. Note the true criterion is on embeddings and can only be evaluated post-embedding; two text-level proxies run at referee time did **not** reproduce the alarming rate the critique reported for osm — see §20-M11 |
| **V5** | P2-neg vacuity (primary) | fewer than **6 of 11** base kinds' η_k exceed their N1 95th percentile | **P2-neg VOID** — the instrument found no content directions anywhere, so Record's absence means nothing |
| **V5b** | P2-neg vacuity (secondary, non-voiding — defect M9) | upper bound of AUC_Record's 95% bootstrap CI (2,000 resamples) < 0.70 | recorded as corroborating vacuity in the results table; **does not void on its own**, because with 20 positives the SE near 0.70 is ≈0.08–0.10 |
| **V6** | P2-pos lever dead | median ‖D̃_frame‖ ≤ 1.1 × median ‖D̃_warrant‖ | **P2-pos VOID** — no item-specific lever, nothing to measure |
| **V6b** | P2-pos denominator dead (new — defect C2) | mean_i ‖D̃_frame(i)‖² / mean_i ‖D_frame(i)‖² < 0.05 | **P2-pos VOID** — after centring, the displacement is essentially all constant echo |
| **V7** | truncation | > 2% of texts exceed the embedder's context | switch to `BAAI/bge-m3`, re-run everything, record the switch. Measured exposure: artifact corpora 0%, RATCHET rationales 0.65% |
| **V8** | rank resolution | σ_R > 1.5 in the §8 gauge, **or σ_R undefined** | the rank leg (P1b) cannot kill; `R_kind` is reported descriptively with its interval and **no band verdict**; the "not 7, not 13" clause is retracted **before** the measurement |
| **V9** | parse floor | > 5% of reason rows unparsed for a condition | that condition is dropped from P2-pos and the drop is reported (current measured rate: 41/5,418 = 0.8%) |
| **V10** | budget | spend > $3.00 | abort, report what was completed |
| **V11** | batch attribution (new — defect M1) | pooled Ω(11) passes P1a **while both** within-part_a and within-part_b arms fail their own N1 at p ≥ 0.01 | **P1a VOID** — the pooled pass is attributed to generation batch, which the N1 permutation cannot see |
| **V12** | topic attribution (new — defect h6) | Babel top-1 accuracy ≤ 2/10 | **P1a's interpretation VOID** — the directions are topic-driven on the one corpus where topic is held fixed. Ω is still reported as a number |

## 16. Kills — separable, each naming its blast radius

* **K1 — the alignment kill.** Ω(11) fails to beat the N1 **or** the N1b null at p < 0.01 in the
  primary arm.
  **Takes down:** P1a, and with it the eigen-bridge in `LEAN2_CONFRONTATION.md` — "the 11 kinds
  are the principal content directions of change-embedding space" is dead, and the design note's
  bridge paragraph is withdrawn.
  **Does not touch:** P2 (evaluated independently), `basePlane_card = 11`, `Generator.lean`,
  the PLANE study's κ 0.687 / coordinate-flatness measurement, or the taxonomy's usefulness as a
  classification scheme. A taxonomy can be a good coordinate system for people and not be the
  eigenbasis of an embedding model.
* **K1b — the privilege kill (new — defect M6).** `Ω_taxonomy ≤ Ω_nontaxonomy` (the
  domain×span-tercile partition) in the primary arm.
  **Takes down:** the claim that **these** eleven are the coordinate system — an arbitrary
  semantically-coherent 12-way partition does as well or better. The weaker statement "*a*
  12-way partition of Corpus A is recoverable in held-out change-embeddings" may survive and is
  reported as such.
  **Does not touch:** K1's object (alignment may still be statistically real), P2, or any Lean.
* **K1c — the topic kill (was buried in §13).** `Ω_Δ − Ω_before ≤ 0` under the paired null of
  §13, or not > 0 at p < 0.01.
  **Takes down:** P1a's *interpretation* — the statistic is reading topic, not change. Ω is
  reported as a number and the change-reading is withdrawn.
  **Does not touch:** P2-neg (LOKO uses the same Δ cloud but asks a different question, and its
  own vacuity gate V5 is independent), or any Lean.
* **K2 — the rank kill.** Alignment real, `R_kind` outside the §9-P1b band of whichever tier is
  live.
  **Takes down:** the "near 11" clause only, and (if Tier 2 was live) "not 7, not 13". The
  alignment claim survives with a corrected integer, reported plainly.
* **K3 — the Record kill.** A stable, replicable content direction that tracks Record and is as
  principal as a typical base kind — **all three** conjuncts of §10's K3 row.
  **Takes down:** the relation-typing claim as an *empirical* claim — Record would be
  embedding-visible as a category. **Does not touch** `record_not_site_generated` (a theorem
  about the site model) or `repairable_does_not_factor` (a theorem). The stance's plain sentence
  "Record is a relation, not a category" would need re-scoping to "not site-generated, yet
  embedding-visible as a category", and that re-scoping is the required response.
  **Note the conjunct that was removed:** version 1 additionally required a replicating principal
  direction at some j ≤ 13. §8.3's pilot shows PC #11 replicates at chance (0.031) even where
  Ω(11) = 0.66, so that conjunct made K3 **unfireable** — a violation of house rule 2 (defect
  C6). It is gone.
* **K4 — the flatness kill (named per kind).** Some base kind k ≠ Record moves under the frame
  lever above the N3 floor at p < 0.01, on the second-moment statistic of §11.
  **Takes down:** the artifact-locality of that named kind at embedding granularity, and it
  contradicts the PLANE label-level flatness for that kind — reported as an instrument-sensitivity
  finding with the kind named. Takes down nothing else.
* **K5 — the numerology kill (RATCHET). ✅ FIRED — 2026-08-18, before the main run, by
  inspection and by reproduction.**
  **Evidence, both legs:** (a) the shipped 8-signal audit on qa_eval (n = 1,768) reproduces the
  **90% horizon of 7 exactly** but returns a **99% horizon of 8** — the full rank of an 8×8
  matrix, so 11 is unreachable in principle — and a participation ratio of **5.575** against the
  report's 6.61; (b) `EMPIRICAL_REPORT.md` §1.2, two paragraphs above §2.1, computes
  **11.51 = −ln(0.01)/0.4 under an assumed decay constant λ = 0.4**.
  **Takes down:** the third leg of "three objects share the integer 11". The design note's claim
  now stands on at most two legs (Clifford-algebra cap; site-model image), **unconditionally**,
  regardless of how P1 lands.
  **Required corrections, owed now:** (i) `/home/emoore/RATCHET/stability-analysis/EMPIRICAL_REPORT.md`
  §2.1's "intrinsic rank of 11" is annotated as not reproducible from the shipped audit and
  parsimoniously read as §1.2's heuristic; (ii) `LEAN2_CONFRONTATION.md`'s three-legs sentence is
  amended to two. **Neither correction may wait on this experiment's outcome.**

## 17. What will NOT count as support

* Any Ω computed against a null that is not the label permutation (N1) **and** the
  span-stratified permutation (N1b). The k/d figure is a scale, not a floor.
* Any k other than 11 promoted after seeing the sweep.
* The un-normalized-Δ arm, the raw (non-residualized) arm, the templated-description arm, or the
  panel-modal-label arm quoted alone when it disagrees with its pre-registered primary.
* A leftover: "the variance not explained by the 11 looks like Record" is a residual and is
  never support (rule 6).
* A pass on the primary embedder alone. Without replication on `Qwen/Qwen3-Embedding-0.6B` the
  verdict is **EMBEDDER-DEPENDENT**.
* Agreement between P1's number and RATCHET's 11 (§2.4: different objects, and the 11 is now a
  fired kill). **Also excluded: agreement between `R_kind` and RATCHET's 7**, which is the only
  RATCHET statistic that reproduces and is therefore the more tempting coincidence.
* Corpus A-held or Babel scored after the primary numbers and used to *raise* a verdict.
* **`a_Record(11)` from the 12-class fit quoted as the P2-neg primary** — §5.1's identity makes
  it a fixed function of the other eleven contrasts.
* **Any statement that Ω(11) measures "the 11 kinds excluding Record"** — §5.1: `w_Record` is
  inside `S_kind` exactly, and Ω is a statistic about the full 12-class between-class subspace.
* **A P1a pass without a within-batch arm surviving** (V11), or with `Ω_Δ ≤ Ω_before` (K1c), or
  with Babel ≤ 2/10 (V12), or with `Ω_taxonomy ≤ Ω_nontaxonomy` (K1b).
* **Arm 3's AUC quoted as contributing to K3.** It is a standalone finding (§11).

## 18. Order of work, and outputs

1. §8 rank-resolution gauge, re-staked grid (synthetic only — **before** any corpus text is
   embedded). Returns σ_R, ρ_gauge, PC-replication-by-rank. Resolve V3b and V8 **before** step 3.
2. §3 determinism gauge (20 texts, twice). Resolve V2.
3. Embed Corpus A, B, BAB, A-held before/after; build Δ; run §15-V1/V1b/V3/V4 checks and record
   rank(B), per-stream n_eff.
4. P1a (with N1, N1b, N4 comparators), **P1a-batch** (V11), then P1b; placebo P1 (K1c).
5. P2-neg — LOKO η table for all 12 kinds, plus the AUC table with CIs, plus the disclosed
   `a_Record(11)` secondary. Resolve V5/V5b.
6. Embed reason texts; P2-pos (stripped primary, unstripped secondary; second-moment statistic).
   Resolve V6/V6b/V9.
7. Babel decathlon (permutation-nulled; V12); Corpus A-held scored once, with its three-kind
   coverage stated.
8. Secondary embedder replication of the headline numbers only.
9. RATCHET: run AUDIT 2 and AUDIT 3 for the record (AUDIT 1 and K5's verdict are already
   written); R-placebo parallel-analysis rank.
10. Write `EIGEN_ALIGNMENT_RESULTS.md`: every staked band with its measured value beside it,
    the §9.1 forward prediction scored explicitly as confirmed/falsified/missed, fired kills
    stated as plainly as survivals, VOIDs named, `rank(B)` quoted with every Ω, and the cache
    sha256 recorded.
11. **Owed regardless of outcome:** the two K5 corrections named in §16-K5.

## 19. Open design doubts — stated now, not after

* **D1 — Δ is not obviously "the change".** Embedding models are trained for topical similarity;
  the difference of two near-identical documents may be dominated by the embedder's local
  geometry rather than by the semantics of the edit. The Babel decathlon (§12) and placebo P1
  (§13) are the checks; both now carry kills (V12, K1c) rather than caveats, but neither is
  decisive, and a P1a pass with a Babel PASS-WEAK would leave the reading genuinely ambiguous.
* **D2 — the 0.25 floor for Ω(11) is a judgement call, and is now predicted to be unmet.**
  It is staked in advance, unchanged from version 1, and defended by the 23×-chance argument.
  Version 1 guessed the realistic field at 0.10–0.20; §9.1's power proxy revises that **down** to
  a predicted 0.02–0.08. **The floor was deliberately not lowered** — if everything lands at
  0.02–0.08, this prereg will have set a bar that no taxonomy could clear on this corpus, and
  that is said here rather than discovered later.
* **D3 — reason texts are short** (median 124 chars, max 256) and are the panel's *restatement*
  of its own label, so P2-pos's displacement may be dominated by label-echo rather than by
  frame-reading. The centring step and the stoplist arm mitigate this; neither eliminates it.
  The 256 max is **not** a clipping artifact (only 1 of 5,377 rows sits there), so the weakness is
  brevity, not truncation. P2-pos is the weakest leg in this design and is labelled so in
  advance.
* **D4 — Corpus B's kind coverage is skewed and its sources are concentrated.** ~6 Record votes
  in 510, Rules/Facts/Identity/Manner dominant, **and 43% of the items are OpenStreetMap**
  (osm + osm2), treated as 2 of 5 one-hot strata. The cross-corpus transfer arm therefore tests
  only the kinds the wild streams exercise, on a source-concentrated cloud. A transfer null is
  uninformative about the rest, which is why §9-P1c cannot kill.
* **D5 — R_kind is sample-size sensitive.** More items find more significant PCs. The §8 gauge
  fixes the resolution at n = 124 but does not make the count corpus-independent; a different
  corpus size could legitimately return a different integer, and that is a limit of the rank
  leg, not a defect of the taxonomy.
* **D6 — authored corpus, authored by us, with the taxonomy in hand — and authored in two
  batches split 6/6 by kind.** Corpus A items were written to target kinds. If they align, part
  of what is measured is our own ability to write discriminable items, and part may be
  batch-level style (§2.1a: batch detectable at 0.573 from unchanged text). The batch nuisance
  term, the within-batch arms and V11 are the answers available; none is a corpus authored by
  someone who never saw the theory. The one genuinely external option — the Yang et al.
  (EMNLP 2017) 13-intention corpus named in `LEAN2_CONFRONTATION.md` §2 — is not on disk here and
  is not part of this design.
* **D7 — "not 7, not 13" may be unreachable, and §8 now decides it explicitly.** If
  σ_R > 0.66 the rhetorical clause dies quietly and in advance, which is the correct outcome, but
  it means the sharpest-sounding part of the prediction may never be tested. Version 1 let the
  clause survive into a band that admitted 13; that is fixed.
* **D8 — `R_kind` counts ranks, not reproducible directions (new).** §8.3's pilot shows that
  beyond roughly the top 2–4 PCs, individual principal directions are not estimable at n = 124 in
  d = 1024. `R_kind` is well-defined as a count of *ranks at which kind loading exceeds the
  permutation floor* — the *amount* of loading at rank j is far more stable than the *direction*
  u_j — but no sentence in the results file may say "PC 9 is the Structure direction". This is a
  real ceiling on what the rank leg can mean and it is stated before the data.
* **D9 — the batch control and the batch confound cannot both be fully served (new).** Kind is
  nearly nested in batch, so residualizing on batch removes genuine kind signal and the
  within-batch arms have only 6 classes and 60 items per half. There is no analysis on this
  corpus that is simultaneously fully powered and fully batch-free. That is a property of how the
  corpus was generated, not of the analysis, and the honest response is to report both arms and
  let V11 bind.

## 20. Referee round — every defect and its disposition

Adversarial critique received 2026-08-18 (task N1b), verdict **DO NOT RUN AS WRITTEN**.
Dispositions below. **All numbers in this section were re-derived independently at revision
time**; two of the critique's figures did not reproduce and are marked so.

### CRITICAL

| id | defect | disposition |
|---|---|---|
| **C1** | P2-neg ill-posed: `w_Record` lies exactly inside `S_kind` by the counting identity; a twelfth between-class direction cannot exist | **FIXED.** Independently verified at Corpus A half sizes on noise: rank(12) = 11, rank(11) = 11, ‖w_R − Proj‖ = 1.3e-15, ‖Proj‖² = 1.0000. §1's wording re-posed; §5.1 rewritten to state the identity *and obey it*; §5.2 adds the **leave-one-kind-out (LOKO)** construction where the held-out kind's direction is genuinely outside the fitted span; §10 rebuilt on `η_k = A_k·ρ_k` for all 12 kinds symmetrically; `a_Record(k)` demoted to a disclosed secondary (not deleted — it is a well-defined number, it is simply not independent of the other eleven, and §17 forbids quoting it as primary). The referee's stronger claim that the headline is "untestable by the stated statistic" is **partially rebutted**: `a_Record(11)` is not identically anything, and the comparison across 12 directions is meaningful; what is fatal is the *band* built on it (see M10) and the "kept separate" language (h1) |
| **C2** | P2-pos statistic `π_k(T)` is identically zero by its own step 4 | **FIXED.** Confirmed by algebra: step 4 sets mean_i D̃ = 0, so mean_i⟨D̃, w_k⟩ = ⟨0, w_k⟩ = 0. §11 step 5 replaced with the normalized second moment `mean_i⟨D̃, ĝ_k⟩² / mean_i‖D̃‖²`; N3 applied identically; bands re-derived; **V6b** added because the new statistic has a denominator that can also die |
| **C3** | V3's n < 15 floor VOIDs the primary arm by arithmetic (a half gives 10–12/class) | **FIXED.** Verified: max class 24 → half 12 < 15; all twelve classes below the floor. V3 re-staked to **n ≥ 9** (a half delivers 10 and 12), UNMEASURED/VOID logic kept, and **V3b** added — the §8 gauge must *measure* centroid replication at 10/class (ρ_gauge ≥ 0.30) rather than the design asserting stability |
| **C4** | §8's gauge grid lies entirely in the undetectable regime → σ_R undefined → P1b's band and V8 unevaluable | **FIXED.** Reproduced independently: median Ω(11) at scales {0, .05, .10, .20, .40, .80} = {.0116, .0101, .0104, .0105, .0106, .0126} against chance .0107 — every staked cell reads chance. Grid re-staked to **{0.5, 1, 1.5, 2, 3, 4, 6, 9}**, measured to span [.01, .59] and straddle 0.25 at ≈3.5. §8.4 adds an automatic fallback so σ_R is **never undefined at write-up** |
| **C5** | P1b's PASS band `\|R−11\| ≤ 3σ_R` with σ_R ≥ 1 admits 13, so "not 13" is unfalsifiable-by-passing | **FIXED.** P1b split into **Tier 1** (`≤ 2σ_R`, honest and resolution-limited) and **Tier 2** (`R ∈ {10,11,12}`, evaluated **only if σ_R ≤ 0.66**). §1 now carries the conditional retraction explicitly, resolving h7 at the same time |
| **C6** | K3's PC-replication conjunct is unattainable at n = 124 → the Record kill cannot fire | **FIXED.** Reproduced: PC #11 split-half replication is .015–.041 (chance) at every scale, including scale 12 where Ω(11) = 0.66; PC #1 reaches .744 at scale 3, PC #5 .314. Conjunct **deleted from K3**; the "≥3 of PCs 8–11 individually significant" conjunct **deleted from P1b**; per-PC replication retained as a **reported diagnostic** and gauged in §8.3; new doubt **D8** states the resulting ceiling on what `R_kind` can mean |

### MAJOR

| id | defect | disposition |
|---|---|---|
| **M1** | kind perfectly nested in generation batch; no nuisance term, no within-batch control; N1 cannot see it | **FIXED.** Verified by id-matching: part_a = 6 kinds ×20, part_b = 6 disjoint kinds ×20, part_c = ontological+axiomatic top-up ×4 each. Batch predicted from unchanged `before` at **0.573** vs majority 0.484. **§2.1a** added; **batch one-hot added to §4's residualization** with its cost stated in advance; **§9-P1a-batch** within-part arms added; **V11** makes the pair binding (pooled pass + both within-batch failures = P1a VOID). One correction to the critique: ontological and axiomatic *do* span two batches via part_c, so "no kind spans two batches" is slightly too strong — it does not help |
| **M2** | changed-span size strongly kind-dependent; one log-span covariate cannot remove it | **FIXED.** Independently measured: medians 1.5 (contingent) → 130.5 (procedural), **87× spread**, Kruskal H = 96.82, **p = 7.6e-16** (the critique's diff convention gave 3.0→76.0, 25×, p = 3.4e-14; same conclusion, mine is worse). **N1b span-stratified permutation added and made a required PASS conjunct**; Ω reported conditional on span decile |
| **M3** | Placebo P1 vacuous as written and its comparison statistic undefined | **FIXED.** §13 rebuilt: `S_kind^before` from before-cloud contrasts on the same fitting half, identical pipeline end-to-end on the before cloud, `Ω_before` vs `Ω_Δ` **paired within split**, null by permuting the Δ/before assignment within split. Promoted to a named kill **K1c**. The control is live: `before` → kind = **0.149** vs chance 0.083 (critique: 0.181; same story) |
| **M4** | N1 × N2 composition undefined; BH's PRDS assumption fails given `Σ a_j = r` | **FIXED.** §7 pins: N1 permutes all 248 labels then runs the whole 200-split pipeline (500 permutations, shared index); the 200 split SVDs are precomputed once; combination rule is **null-of-medians**; permutation is **free**, declared conservative in direction; **BH deleted**, replaced by **permutation maxT step-down** at FWER 0.05. Min reportable p = 2.0e-3 |
| **M5** | the 0.25 floor is likely unreachable and a free power check was skipped | **FIXED, rule-6 clean.** No-embedding TF-IDF proxy run and recorded (§4 table): span→kind 0.170, before→kind 0.149, variation_site→kind 0.642, before→domain 0.972 (critique: 0.202 / 0.181 / 0.666 / 0.976 — same story, mine slightly weaker). **The floor is NOT lowered.** Instead §9.1 stakes the predicted landing zone **[0.02, 0.08] = WEAK** as a **forward prediction before embedding**, with the meaning of every outcome fixed, including what it means if the prediction is falsified and P1a passes |
| **M6** | no rival-partition comparator; N1 tests only against random labels | **FIXED.** **N4** added: k-means-12 as upper comparator and domain×span-tercile (15→12) as the non-taxonomy rival, both paired within split. `Ω_taxonomy > Ω_nontaxonomy` made a **required PASS conjunct**, and its failure is the new separable kill **K1b**. Ω_kmeans − Ω_taxonomy reported always |
| **M7** | no per-class resolution gate; V1's global median will not fire on the sub-resolution classes | **FIXED.** **V1 applied per class**; failing classes are UNMEASURED, dropped from `B`, and **Ω renormalizes by 1/rank(B)** with the rank reported beside every Ω (§6). **V1b** added: rank(B) < 8 voids. contingent (median 1.5 chars) and empirical (3.0) are the named at-risk classes |
| **M8** | the R-audit is an unbounded forking-paths sweep, and is moot — K5 is answerable by inspection | **FIXED, and K5 recorded as FIRED.** Sweep **deleted**, replaced by a pre-specified three-subset audit. AUDIT 1 reproduced independently: n = 1,768 qa_eval complete rows, eigenvalues [2.633, 1.131, 0.960, 0.886, 0.819, 0.719, 0.502, 0.351], **90% horizon 7 ✓ (matches report)**, **99% horizon 8 ✗ (report 11; 8 is full rank)**, **participation ratio 5.575 ✗ (report 6.61)**. One refinement to the critique: it said "the companion statistics reproduce from the 8" — the 90% horizon does, the **participation ratio does not** (off 19%), so *only* the 7 reproduces. `EMPIRICAL_REPORT.md` §1.2's 11.51 = −ln(0.01)/0.4 confirmed verbatim, and `LEAN2_CONFRONTATION.md` line 56 already says it carries no weight (h2). Two corrections are now owed unconditionally (§16-K5) |
| **M9** | V5's AUC ≥ 0.70 gate is underpowered with no CI | **FIXED.** AUC **demoted from the primary vacuity gate**; the new primary gate is "≥6 of 11 base kinds detectable" (V5). AUC retained as **V5b**, non-voiding, gated on the **upper bound of a 95% bootstrap CI** (2,000 resamples), with all 12 AUCs and CIs reported |
| **M10** | P2-neg's PASS is a ~1/12 event regardless of the hypothesis, and C1 makes INCONCLUSIVE near-certain | **FIXED.** The "≤ min over the 11" band is **deleted**. §10 rebuilt on the LOKO η with an N1-priced significance conjunct plus a "bottom 3 of 12" descriptive rank; a-priori probabilities of every band are **stated in the document** (resolving h5), and INCONCLUSIVE is required to name which conjunct failed |
| **M11** | V4's granularity unspecified; Corpus B is a union so an osm failure ambiguously voids B | **FIXED structurally; the specific figure REBUTTED.** V4 is now **per stream**, with within-stream deduplication, per-stream n_eff, and **stream-drop instead of corpus-VOID**. But the critique's "osm 72.1% of pairs > 0.9" **did not reproduce** under either of two independent text proxies at revision time: on changed spans, char-ngram TF-IDF cosine > 0.9 gives fedreg 0.0% / github 0.65% / **osm 0.17%** / osm2 0.34% / wiki2 0.34% of pairs, and difflib ratio > 0.9 gives fedreg 0.0% / github 0.65% / **osm 0.28%** / osm2 0.79% / wiki2 0.26%; by *items in a cluster*, **github is the most duplicated stream (32%)**, not osm (5–7%). On `before` texts the picture is the same. The critique may have measured a different object. V4's real criterion is on embeddings and is only evaluable post-embedding, so the structural fix stands and no stream is pre-condemned |

### MINOR

| id | defect | disposition |
|---|---|---|
| **m1** | "`reasoning_transparency` non-null on 2,148" claimed FALSE (0 non-null) | **REBUTTED, with a different correction applied.** In `accord_traces.jsonl` — the file §2.4 cites — the key **is non-null on exactly 2,148 rows**, so version 1's count was right. The critique measured `trace_context.jsonl`, where the key is absent entirely (0 of 6,465). **The real error, now fixed:** the field is a **binary float flag (1.0 × 1,673, 0.0 × 475), not free text**, and version 1 listed it inside a sentence about free text |
| **m2** | "60 columns" → 59 | **FIXED.** Verified union of keys in `trace_context.jsonl` = **59**. The 25-name numeric list is exactly correct and is unchanged |
| **m3** | "`torch` and `sentence_transformers` are not installed (verified)" is half false | **FIXED.** Verified: `sentence_transformers` **is** installed, `torch` is **not**. §3 now reads "torch is not installed, so the installed sentence_transformers cannot run a model." The operative conclusion (no local fallback) is unchanged |
| **m4** | truncation claim unqualified once §13's placebo P2 is included | **FIXED.** Verified: artifact corpora max **1,273** (`eco_wiki2.jsonl`, `wiki2-19`, `after`), 0 of 1,098 texts > 2,048. RATCHET rationales max **2,296**, **33 > 1,273**, **14 > 2,048** = **0.65%**, below V7's 2%. §3 now scopes the claim and states the RATCHET distribution separately |
| **m5** | §12's binomial arithmetic wrong; X = 4 already meets p < 0.01 | **FIXED.** Recomputed for n = 10, p = 1/11: **P(X≥3) = 0.0554, P(X≥4) = 0.00915, P(X≥5) = 0.00106**. §12 states explicitly that **≥5 is a deliberately stricter bar than p < 0.01 and why**, adds a **4/10 = PASS-WEAK** band, and makes a **permutation null over the 10 Babel labels the primary**, with the binomial as a scale only |
| **m6** | cost text count 6,500 → ≈9,700 | **FIXED.** Itemized in §3: 496 + 24 + 20 + 558 + 5,377 + 2,148 + ~1,098 + 40 ≈ 9,761. Cost conclusion and the $3.00 cap unaffected |
| **m7** | part_d called "boundary-loaded held-out" but covers only 3 kinds | **FIXED.** Verified empirical 6 / deontic 3 / ontological 3. Stated in §2.1 and §14, and required wherever it is quoted |
| **m8** | Corpus B's 43% OSM source concentration undisclosed | **FIXED.** Disclosed in §2.2 and in §19-D4 alongside the kind skew |
| **m9** | off-vocabulary panel labels unmentioned and unhandled | **FIXED.** Verified: full_judgments 1 `Scope`, 1 `NO FIT`, 41 null; eco 2 `Version`, 12 `NO FIT`, 7 null; eco2 5 null; eco2_wiki 3 `NO FIT`, 2 null. §2.3 adds a frozen handling rule (drop off-vocabulary votes before the modal; drop the item if < 2 in-vocabulary votes remain; report rates) |

### HONESTY DEFECTS

| id | defect | disposition |
|---|---|---|
| **h1** | §5 names the counting identity as the primary hazard, then declares `w_Record` "kept separate throughout" | **FIXED.** The phrase is deleted. §5.1 now states that `w_Record` **cannot** be kept separate inside a 12-class contrast basis, forbids the "excluding Record" phrasing anywhere in the results file (§17), and §5.2 supplies the construction that *does* separate it |
| **h2** | claims to have read the RATCHET report "in full" while presenting its 11 as an open empirical object, when §1.2 two paragraphs above computes it as −ln(.01)/.4 — and the design note being discharged already says so | **FIXED.** §2.4 quotes §1.2 verbatim, cites `LEAN2_CONFRONTATION.md` line 56, deletes the sweep, and records **K5 as FIRED before the main run** with two corrections owed unconditionally |
| **h3** | "not a number chosen after seeing anything" substituted for a power calculation that was free to run | **FIXED.** §9.1 runs the power proxy and stakes a **forward prediction** on it, explicitly noting that the floor was **not** lowered and that innocence-of-provenance was never the question — reachability was |
| **h4** | "the signal scale is not tuned to match anything observed" reads as a virtue and functions as the defect | **FIXED.** §8.2 states plainly that untuned is not well-chosen, that version 1's grid was dead by dimensional analysis, and that the new grid is tuned to **synthetic detectability only** with no corpus embedding consulted |
| **h5** | INCONCLUSIVE is the modal outcome and is presented as a guard | **FIXED.** §10 states the a-priori probability of every band under H0 and H1, requires INCONCLUSIVE to name the failing conjunct, and (via M10's fix) replaces the band that made it near-certain |
| **h6** | §12's FAIL consequence is elastic ("must be reported with that caveat attached"), unlike §13's kill | **FIXED.** Babel ≤ 2/10 is now the named **V12**, which VOIDs P1a's *interpretation*, matching §13/K1c in force |
| **h7** | "not 7, not 13" survives verbatim into a band that admits 13 | **FIXED.** §1 carries the conditional retraction; §9-P1b's two tiers make the clause falsifiable-by-passing when live and retracted in advance when not (see C5) |
| **h8** | arm 3's "counts toward K3" is an unquantified fifth criterion | **FIXED.** The phrase is deleted; arm 3 is a **standalone reported finding** and explicitly does **not** enter K3's conjunction (§11, §17). Moving it inside K3 would require an amendment made before the arm runs |
| **h9** | "leakage-free" asserted without qualification | **FIXED.** §4 now reads "leakage-free **with respect to author-written change descriptions**" and names the four nuisances it does not remove (batch, span size, domain/stream, our own authorship), three of them with measured magnitudes |

### VERIFIED-TRUE — kept verbatim, not over-corrected

The referee confirmed the following against the artifacts, and this revision **does not touch
them**: all row counts and sha256 pins in `/home/emoore/RATCHET/release/MANIFEST.json`; the 25
numeric-capable column list; `action_rationale` non-null on 2,148 at mean 710.4 chars;
`trace_level` splits; Corpus A's 248 rows, class counts, domain and difficulty distributions and
248 distinct `before` texts; part_d = 12, babel = 10, eco stream counts; `full_judgments.jsonl`
= 258 × 7 × 3 with the seven conditions matching `plane_annotate.py`, 1,765/41/0 parse coverage,
reason median 124 / max 256 with only 1 row at 256 (**so D3's weakness is brevity, not
clipping**); Corpus B's 6 Record votes in 510; and Babel's 10/10 identical `before` text.

Kept verbatim by explicit instruction of the referee round, because they are the strongest parts
of the design: **N1's construction** (verified at zero planted signal to return median
Ω(11) = 0.0116 against k/d = 0.0107 with a tight band — no false positive); **unit-normalizing
Δ**; **making the residualized arm PRIMARY**; **forbidding LDA/logistic discriminators at n ≈ 20
in d = 1024**; **requiring a second-family embedder**; **document-granular permutation**; and the
pre-committed **§17 "what will NOT count as support"** list, which this revision extends rather
than trims.

---

## READY-FOR-STEWARD-REVIEW

**Status: revised, internally consistent, and not yet run.** Every CRITICAL and MAJOR defect is
fixed; two MINOR items (m1, and M11's specific figure) are rebutted with independently measured
counter-evidence and the surrounding structural fixes applied anyway. No corpus text has been
embedded. Steps 1–2 of §18 (both gauges) are the first executable actions and both are
synthetic or 40 texts.

**One kill has already fired and its consequences are owed now, not at the end:**
**K5** — the RATCHET "11" is `−ln(0.01)/0.4` under an assumed constant, not a measurement.
The two corrections named in §16-K5 do not depend on this experiment.

### Decisions a human must confirm before any data is touched

1. **The floor stays at 0.25 while the forward prediction says 0.02–0.08 (§9.1).** Confirm that
   this is the intended posture: a bar that is predicted to fail, kept unlowered, with the
   prediction scored. The alternative — re-staking the floor to the power calculation — is
   defensible but must be chosen **now**, in writing, and would make the WEAK band the target.
2. **The batch control's cost (§4, §9-P1a-batch, V11).** Residualizing on `part` removes genuine
   kind signal collinear with the 6/6 split, and the within-batch arms have 6 classes and 60
   items per half. Confirm you accept a design where **no arm is simultaneously fully powered
   and fully batch-free** (§19-D9), rather than regenerating Corpus A in interleaved batches —
   which is the only real fix and is a corpus rebuild, not an analysis change.
3. **P2-neg's replacement statistic (§5.2, §10).** The LOKO `η_k = A_k·ρ_k` is new and is not a
   standard instrument. Confirm it is the right operationalization of "Record does not behave
   like a twelfth content class", or name a preferred alternative before it runs.
4. **The conditional retraction of "not 7, not 13" (§1, §8.4, §9-P1b).** Confirm that the sharp
   clause may be retracted **automatically by the gauge**, before data, without a further human
   decision — §8.4 is written to fire on its own.
5. **K5's two owed corrections (§16-K5).** Confirm that `EMPIRICAL_REPORT.md` §2.1 and
   `LEAN2_CONFRONTATION.md`'s three-legs sentence are annotated **now**, independently of this
   experiment's outcome, and confirm who owns those edits — both files are outside this track.
6. **Arm 3's budget (§11).** ~1,500 model calls, ≈$0.05. Confirm run or cut; it is now a
   standalone finding and cutting it costs no kill.
7. **Compute budget for the pinned null schedule (§7).** 500 whole-pipeline permutations × 200
   splits × two nulls (N1 and N1b) × the placebo's paired null, with 200 SVDs precomputed.
   Estimated minutes, not hours, in numpy — but confirm the orchestrator is willing to spend it,
   because reducing N_perm below 500 raises the minimum reportable p above 2.0e-3 and would
   put the p < 0.01 bar within one order of the resolution floor.
