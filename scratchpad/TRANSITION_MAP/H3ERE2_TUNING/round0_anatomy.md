# H3ERE2 — ROUND 0 ERROR ANATOMY (calibration data, AMENDMENT T1 tuning license)

Scored 2026-08-21 by the tuning supervisor. Calibration data only. The held-out sets named
in T1 (curated ODD lines; wild seed 20260823) were NOT read, NOT sampled and NOT run.

## 0. A scoring-convention finding that must be settled before any verdict is read

The sealed wild baseline is quoted as kappa 0.3550. That number is reproducible **only**
under one convention: unparseable judgments are kept as their own category and all 345
units are scored. Under the two other defensible conventions the same sealed file reads:

| convention | wild Fleiss kappa | N units |
|---|---|---|
| nulls as a 13th category, all units (**the sealed one**) | **0.3550** | 345 |
| nulls dropped, "NO FIT" kept as a category | 0.3877 | 314 |
| nulls and "NO FIT" dropped, complete triples only | **0.4028** | 300 |

The frozen L2 floor is kappa >= 0.40. The listwise-complete convention therefore **already
clears the floor on the BASELINE**, with no pipeline at all. The ceiling break is a
convention choice unless the convention is pinned. All numbers below are reported under
the sealed convention (nulls as a category, all units) and every future round will report
both. This is flagged for the orchestrator, not resolved here: pinning the convention is
a prereg act, not a tuning act.

A second consequence follows and is load-bearing: **kappa rewards collapsing the label
space.** A pipeline whose fast path can only emit four labels will read higher agreement
than a twelve-way instrument for reasons that have nothing to do with better decomposition.
L1 (curated accuracy) is the only guard against buying L2 with label collapse, so from here
on every round reports the number of distinct labels the pipeline actually emits alongside
its kappa.

## 1. Baseline (sealed PANEL-2 single pass, same 124 even-line curated items)

Pooled over three families, 372 judgments: **accuracy 0.737, coverage 0.944, cross-family
kappa 0.798.** Surface-target accuracy 0.952 (n=126); **deep-target accuracy 0.626** (n=246).

Per-kind: Process 1.000 · Rules 1.000 · Facts 0.967 · Manner 0.967 · Identity 0.889 ·
Priorities 0.867 · Circumstances 0.733 · Model 0.633 · Record 0.633 · Structure 0.567 ·
Confidence 0.500 · **Premises 0.167**.

Dominant confusions: Confidence->Rules 11 · Premises->Facts 11 · Circumstances->Facts 8 ·
Model->Manner 7 · Premises->Rules 7 · Structure->Manner 5 · Premises->Model 4 ·
Record->Confidence 4 · Record->Manner 4.

Wild baseline: **kappa 0.3550** (sealed convention), coverage 0.952 by judgment,
0.843 by modal. Label distribution is Manner 519 / Facts 207 of 1035 — the wild stream is
copy-edit traffic, as LEGC_RESULTS recorded.

L1 therefore requires: curated accuracy >= 0.737 AND deep-target accuracy >= 0.726.

## 2. H3ERE2-A as frozen: the S1 gate is inert, and the failure is structural

Pattern A, curated, 372 traces, complete.

| | A (frozen) | baseline | 
|---|---|---|
| pooled accuracy | **0.333** | 0.737 |
| deep-target accuracy | **0.025** | 0.626 |
| surface-target accuracy | 0.921 | 0.952 |
| coverage | 0.995 | 0.944 |
| cross-family kappa (curated) | 0.618 | 0.798 |

Route telemetry: **fast 355 / 372 (95.4%)**, recurse-pass 7, recurse-retry-pass 2,
parse-fail 2. Conscience FAIL rate 2/12 of the cases that reached S3; both retries then
passed.

Three measured facts explain the whole collapse.

1. **S1 returned DEEPER exactly zero times** in 361 parseable calls. The surface
   distribution was Facts 144 / Manner 103 / Rules 76 / Identity 32 / unparseable 11.
2. **The confidence gate is inert.** Self-reported confidence was 0.90 or above on 97% of
   calls (mean 0.913, median 0.95); at the frozen 0.7 threshold it gates nothing. As a
   signal it is near-dead: AUC 0.608 for "the true kind is a surface kind", AUC 0.564 for
   "the final answer is correct".
3. **Fast-path deep accuracy is zero BY CONSTRUCTION.** The fast path can only emit one of
   the surface four, so every deep-target item that exits fast is wrong before the model
   is consulted: 0/233. Surface-target items on the fast path scored 116/125 = 0.928 — S1
   is excellent at what it is good at.

Consequently **all 12 items that reached S2 got there through S1 parse failures, not
through the gate** — and every one of them was a GLM-4.5 truncation. Of those 12, S2 was
right on 8 (Model 4/4, Structure 2/4, Record 1/1, Process 1/2). On its tiny biased sample,
**stage 2 works; it simply never receives traffic.**

Per-kind, pattern A: Facts 1.000, Rules 0.967, Manner 0.967, Identity 0.778, and then
Model 0.100, Structure 0.067, Process 0.033, and **0.000 for Priorities, Confidence,
Circumstances, Premises and Record**.

## 3. What the architecture can pay, arithmetically

Pipeline accuracy = (surface items kept on the fast path, scored by S1) + (everything
routed, scored by S2). A deep item that fast-exits is an unrecoverable loss; a surface item
routed to S2 costs only money, since S2 can confirm it. The gate must therefore be
**asymmetric**, and the two quantities that decide the licence are DEEPER-RECALL and S2's
deep accuracy. To clear L1's deep bar of 0.726 with an S2 that reads deep kinds at 0.78,
DEEPER-recall must be about 0.93 or better.

## 4. Stage-1 variants measured (DeepSeek-V3.1, 124 curated items each, ~$0.03/pass)

| S1 variant | DEEPER-recall | false-route | fast-exit rate | fast-exit acc | best_deep acc |
|---|---|---|---|---|---|
| v0 frozen (surface-or-DEEPER, scalar confidence) | 0.000 | 0.000 | 0.954 | 0.928 | n/a |
| v1 forced two-candidate, model picks the winner | 1.000 | 1.000 | 0.000 | n/a | 0.756 |
| v2 deep kinds given positive content, single choice | 0.707 | 0.167 | 0.476 | 0.971 | n/a |
| v3 two candidates + ternary SURFACE_ONLY/CLOSE/DEEPER verdict | 0.805 | 0.619 | 0.258 | **16/16** | **0.817** |

Three things worth keeping from this table.

- The frozen gate is not weakly calibrated, it is **identically zero**: no prompt in which
  DEEPER is the unnamed residual category ever gets chosen. All three worker families
  diagnosed this independently and identically before seeing each other's answers: a model
  asked to choose between four concrete options and one vague "other" takes an option.
- v1 shows the opposite failure. Asked to name a deep candidate and then judge, the model
  routes **everything**; its `answer` field carries no information. Its two-candidate
  ORACLE ceiling — the rate at which the true kind is in {best_surface, best_deep} — is
  0.782, so a two-candidate architecture is capped at 0.782 even with a perfect adjudicator.
- v3's ternary verdict is a real gate: when it says SURFACE_ONLY it was right 16/16, and
  its forced `best_deep` field alone reads deep kinds at **0.817 in a single call** — well
  above both the 12-way baseline's 0.626 and L1's 0.726 bar. Restricting the choice to the
  deep eight is where the two-stage architecture actually earns its keep.

## 5. The residual hole, and why it is not a prompt bug

v3's 16 missed deep items are **Circumstances 9, Premises 4, Structure 3**. Circumstances
alone is more than half the loss, and in 8 of those 9 misses S1 named Circumstances as its
own `best_deep` and then said SURFACE_ONLY anyway.

Reading the items explains it. Every Circumstances item is a substitution of an
interchangeable instance — a room number, a build host, a scratch path, a van, a courier
route, an example ticket. The model's rationales say, correctly, "a direct substitution of
one factual value for another". Under the discriminators H3ERE2 supplies, that IS Facts.

The corpus's own author notes carry the missing test: *"a comparison could hold it fixed or
let it float"*. And the licensed single-pass instrument that scores Circumstances at 0.733
supplies the frame H3ERE2 dropped — the BASE retention and comparison paragraphs from
`panel2_annotate.py`. **H3ERE2 regressed against its own baseline by discarding the framing
of the instrument it is trying to beat.** The round-1 repair is to inherit that frame
verbatim and to state the boundary as the taxonomy already implies it: Facts means a claim
becomes WRONG; an interchangeable instance that makes nothing wrong is Circumstances.

## 6. Coverage and the GLM truncation

Every S1 parse failure in the frozen run was GLM-4.5 (11 of 11), and the frozen runner gives
it the same 2,500-token ceiling as the non-reasoning families while it spends that budget on
hidden reasoning. Baseline coverage for GLM on curated was 0.839 against 1.000 and 0.992 for
the other two. v2 raises GLM's ceiling to 5,000 tokens and falls back to `reasoning_content`
when `content` is empty; this is a coverage (L3) repair, not an accuracy one.

## 7. Spend

Frozen orchestrator run, estimated from reconstructed prompt sizes (it keeps no ledger):
~$0.84 for all four arms, GLM's reasoning tokens dominating. Tuning spend is metered
per call in `H3ERE2_TUNING/spend.jsonl`: $0.11 through round 0. Screening protocol adopted
to protect the $2.00 fence: variants are screened on ONE family (~$0.03 per 124-item pass)
and only the finalist is confirmed on three.

## 8. The other three arms, scored when they landed

A-wild completed all 1,035 judgments before the frozen job was stopped on the budget alert;
B-curated completed all 372; B-wild reached 145 and is partial.

### Pattern B is near-degenerate with pattern A

| curated, 3 families | accuracy | deep | coverage | cross-family kappa |
|---|---|---|---|---|
| baseline single-pass | 0.737 | 0.626 | 0.944 | 0.798 |
| frozen pattern A | 0.333 | 0.025 | 0.995 | 0.618 |
| frozen pattern B | 0.312 | 0.004 | 0.997 | 0.719 |

Pattern B fast-exits **370 of 372** items (99.5%) and agrees with pattern A's final label on
85.5% of judgments. This is the predicted consequence of the shared, inert S1: A and B differ
ONLY in stage 2, and stage 2 sees 4.6% of traffic in A and 0.5% in B. **The frozen experiment
could not have chosen between its two patterns**, because the stage that distinguishes them
was never exercised. That is a fact about the gate, not about the patterns — the mixture-vs-
single-choice question the prereg wanted to answer remains open and is answerable only behind
a gate that routes.

### Pattern A on wild: the ceiling is not broken, it is slightly lowered

Full sealed corpus, 345 units, 1,035 judgments:

| | kappa (sealed conv.) | kappa (listwise) | coverage | distinct labels |
|---|---|---|---|---|
| baseline single-pass | 0.3581 | 0.4028 | 0.952 | 12 |
| frozen pattern A | **0.3429** | 0.3808 | 0.973 | 12 |

Pattern A reads BELOW the baseline on wild under either convention. Route telemetry on wild:
fast 881, recurse-pass 104, parse-fail 28, recurse-retry 22 — 85% fast-exit, and again every
parse failure is a GLM truncation. Its label distribution is Manner 563 / Facts 288 of 1,035,
with Premises appearing 51 times against the baseline's 14: the small amount of traffic that
does reach stage 2 comes back over-assigned to Premises.

So on the frozen build, none of L1, L2 or the A-vs-B choice is obtainable. This is what the
tuning license was granted for.

## 9. The relaunched arms, and the cleanest confirmation of section 0's warning

B-wild completed under Amendment T2 (the GLM fix). That makes the A-vs-B wild comparison
CONFOUNDED — A ran before the fix and carries 28 nulls, B ran after it and carries none — so
both the confounded and the confound-free readings are given.

On the 345 shared units, sealed convention (nulls scored as a category):

| | kappa | coverage | distinct labels |
|---|---|---|---|
| baseline single-pass | 0.3631 | 0.953 | 12 |
| frozen pattern A | 0.3471 | 0.972 | 12 |
| frozen pattern B | **0.3997** | 1.000 | 11 |

On the 317 units where BOTH arms answered completely, which removes the confound entirely:
**A 0.3808, B 0.4184**, A vs B label agreement 0.846. So B genuinely out-agrees A by ~0.038,
and roughly a third of its headline gap was the coverage repair.

**Pattern B is the highest wild kappa anything has produced in this campaign — 0.3997 sealed,
0.4184 confound-free — and it is the WORST classifier ever measured here.** Its curated
accuracy is 0.312 against a 0.737 bar and its deep-kind accuracy is 0.004 against a 0.726 bar.
It fast-exits 87.5% of wild items and 99.5% of curated ones, and it emits 11 distinct labels
where every other instrument emits 12.

That is section 0's warning, realised exactly: **kappa rewards collapsing the label space, and
the build that collapses it hardest scores best on L2.** Pattern B does not decompose wild
changes; it declines to, agreeably. It fails L1 by 43 points and is not licensed, and the fact
that it is the closest thing to an L2 pass in the whole campaign is an argument about the
criterion, not a result about the pattern.

The tuned candidate is the opposite trade: 0.3858 on wild with 12 labels, coverage 1.000 and
curated accuracy 0.801. If L2 is ever to mean "the mixture was decomposed" rather than "the
panel was persuaded to say less", it needs a companion condition — a label-diversity floor, or
simply the joint reading with L1 that the prereg already requires.
