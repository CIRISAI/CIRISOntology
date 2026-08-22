# H3ERE2 — FROZEN TUNING CANDIDATE
# Tuning declared frozen 2026-08-21 by the tuning supervisor, under H3ERE2X_PREREG AMENDMENT T1.
# Calibration only. The held-out sets were NOT read, NOT sampled, NOT run.

## The pipeline file

`scratchpad/TRANSITION_MAP/H3ERE2_TUNING/h3ere2_v2.py`, invoked as

    python3 h3ere2_v2.py full <dataset> <out.jsonl> v4 a5 -

with the default environment (`NO_FAST_ON_FACTS=1`). `h3ere2.py` (v1) is untouched and remains
the frozen pattern-A/B implementation.

Stages: **S1 = s1_v4** (two forced candidates + ternary SURFACE_ONLY/CLOSE/DEEPER verdict,
inherited retention/comparison frame, four boundary tests) -> **gate** (fast-exit only on
SURFACE_ONLY, and never when the cleared reading is Facts) -> **S2 = s2_a5** (carries-inversion
with keyed discriminators, Identity/Facts protection, declared-basis test, arrangement test) ->
**S3 = s3_v1** (frozen one-sided conscience wording) -> on FAIL, one guided S2 retry, accepted
**only if the retry itself passes** (keep-first otherwise).

Instrument note carried with the candidate: GLM-4.5 runs with
`chat_template_kwargs={"enable_thinking": false}`.

## Calibration metrics

### Curated — the 124 even-line anchor, three families, 372 judgments

| | candidate | baseline (sealed PANEL-2) | L1 bar | verdict |
|---|---|---|---|---|
| end-to-end kind accuracy | **0.801** | 0.737 | >= 0.737 | **PASS** (+6.4 pts) |
| DEEP-kind-target accuracy | **0.789** | 0.626 | >= 0.726 | **PASS** (+16.3 pts) |
| coverage | **1.000** | 0.944 | >= 0.85 | **PASS** |
| cross-family kappa (no criterion) | 0.767 | 0.798 | — | slightly down |

Per family: DeepSeek 0.831, Qwen 0.782, GLM 0.790; coverage 1.000 on all three.
Like-for-like check on the two families whose configuration is unchanged from the baseline
panel (DeepSeek + Qwen): accuracy 0.806, deep 0.811 — better than pooled, so the GLM
thinking change is not carrying the result.

Per-kind: Process 1.000 · Circumstances 0.967 · Model 0.967 · Rules 0.900 · Manner 0.867 ·
Priorities 0.867 · Identity 0.806 · Record 0.800 · Structure 0.700 · Facts 0.733 ·
Confidence 0.600 · **Premises 0.472**.

Route telemetry: recurse-pass 285, recurse-retry-rejected 46, recurse-retry-pass 23, fast 18.
Conscience FAIL rate 0.195 (354 firings). Fast-exit rate 4.8% on this substrate.

### Wild — 115 sealed calibration units (every third of the 345), three families

Complete: all 345 traces, 115 complete triples, no missing data.

On EXACTLY these units, all three instruments:

| | kappa (sealed conv.) | kappa (listwise) | coverage | distinct labels |
|---|---|---|---|---|
| baseline single-pass | 0.3485 | **0.4213** | 0.933 | 12 |
| frozen pattern A | 0.3650 | 0.4046 | 0.977 | 12 |
| **tuned candidate** | **0.3858** | **0.3858** | **1.000** | 12 |

**L2 (kappa >= 0.40): FAILS.** Under the sealed convention the candidate is the best of the
three and still short of the floor by 0.014. Under the listwise convention it is the WORST of
the three, and the baseline clears the floor with no pipeline at all.

Two things must be said plainly about that table.

First, **the verdict is decided by the scoring convention, not by the instrument.** The
convention swing on the baseline is 0.073 — larger than any difference between the three
instruments. Until the convention is pinned as a prereg act, L2 is not a measurement.

Second, **the candidate is the only one of the three for which the convention does not
matter**, because its coverage is 1.000: it has no nulls to argue about. Its 0.3858 is a
clean number; the baseline's 0.4213 is what you get after discarding the 6.7% of judgments
where the baseline failed to answer. The like-for-like comparison against a coverage-repaired
baseline does not exist, and I did not manufacture one.

Route telemetry on wild: recurse-pass 205, recurse-retry-rejected 53, fast 69, recurse-retry-
pass 18. Fast-exit rate 20.0% — four times the curated rate, which is the fast path doing on
wild traffic what it was designed to do and could not do on the deep-loaded curated anchor.

### A wild-only defect, diagnosed and NOT fixed

The candidate assigns **Record to 9.0% of wild traces (31 of 345) against the baseline's 2.0%**, and 52%
of those calls land on deletion-shaped units. The cause is the S2 Record sentence firing on
any removal of text: deleting a paragraph does literally reduce what survives, so the test
reads TRUE, even though the prompt's own retention frame stipulates full retention and Record
is a claim about whether an EVENT can still be established, not about whether a document still
contains a paragraph. The curated corpus cannot expose this — its Record items are constructed
as genuine retention changes, and the candidate scores 0.800 on them.

The sharpest thing this defect shows is a defect in L2 itself: deletion-shaped units RAISE the
measured kappa (0.3858 including them, 0.3617 excluding), because all three families agree on
the same wrong label. **A systematically wrong label that every family agrees on passes an
agreement criterion.** L2 cannot see validity, and on this substrate it is partly measuring a
shared error.

The repair is one sentence in `s2_a5` — that a removal of content is not by itself a Record
change, and that under full retention the sibling records survive the deletion. I did not
apply it, because testing it costs roughly $0.40 and the spend fence had already been reached.
It is the first thing to spend on if the orchestrator funds another round, and it should be
tested BEFORE the single-shot validation, since validation is unrepeatable on a given sample.


## Licence verdict on calibration

| criterion | requirement | candidate | verdict |
|---|---|---|---|
| L1 curated accuracy | >= 0.737 | 0.801 | **PASS** |
| L1 deep-kind accuracy | >= 0.726 | 0.789 | **PASS** |
| L2 wild cross-family kappa | >= 0.40 | 0.386 | **FAIL** |
| L3 coverage, both datasets | >= 0.85 | 1.000 / 1.000 | **PASS** |

**Recommendation: H3ERE2-CAPPED on L2, licensed on L1 and L3.** Tuning turned a pipeline that
scored 0.333 on curated into one that beats its own baseline by 6.4 points overall and 16.3
points on deep kinds, at full coverage — the instrument leg is real and it is the leg the FD
readout needs. The wild agreement leg barely moved: +0.021 over frozen pattern A on matched
units (0.3650 -> 0.3858), which at N=115 is about one standard error and does not reach the
floor. Per H3ERE2X_PREREG, a pattern that fails any criterion is not licensed, so no FD verdict
may be read behind it.

On the stop rule I was given: the trigger that actually fired was the SPEND fence, not the
kappa-plateau rule. The plateau rule asks for two consecutive rounds of sub-0.02 wild gains,
and I have only ONE wild measurement of a tuned build — wild runs cost roughly $0.15 each and
the fence was reached first. So "capped" here is a statement about a criterion missed and a
budget exhausted, NOT a demonstrated plateau. A funded successor could still move L2; what the
evidence says is that three rounds of substantial curated gains bought 0.021 of wild agreement,
which is a poor exchange rate and the reason I would not fund more of the same.

The two-panel wild ceiling finding stands, and this run strengthens it rather than denting it:
a pipeline that decomposes wild changes far better on labelled data does NOT agree with itself
more on wild data. That is what "the ambiguity is substrate-intrinsic" predicts, and it is now
supported by a third instrument built specifically to break it.

## Tuning history

| round | change | curated acc | curated deep | notes |
|---|---|---|---|---|
| 0 | frozen pattern A, as built | 0.333 | 0.025 | S1 returned DEEPER 0 times in 361 calls |
| 1 | S1-v4 gate (forced deep candidate, ternary verdict, inherited frame) | — | — | screened alone: DEEPER-recall 0 -> 1.000 |
| 1 | two-sided conscience TRIED and REJECTED | 0.578 | 0.474 | FAILed 93%; retry damaged 29, improved 11 |
| 1 | keep-first-unless-verified retry rule | 0.750 | 0.803 | replaces the frozen "second answer wins" |
| 2 | S2-a4 (Identity/Facts protection) | 0.823* | 0.793* | Identity 4/12 -> 11/12 |
| 2 | S2-a5 (declared-basis + arrangement tests) | 0.855* | 0.841* | Premises 4/12 -> 7/12, Facts 7/10 -> 9/10 |
| 3 | three-family confirm exposed the single-family screen | 0.766 | 0.720 | deep MISSED the 0.726 bar by 0.6 pts |
| 3 | gate rule: triage may not clear a Facts reading | **0.801** | **0.789** | Circumstances 0.433 -> 0.967 |
| 3 | GLM enable_thinking=false | — | — | coverage 0.944 -> 1.000, 10x cheaper |

\* single-family screen (DeepSeek), S2 measured alone; not comparable to the three-family rows.

## The X read (secondary, no criterion)

Verb determinacy is settled at S1 and the recursion adds nothing to it: cross-family Fleiss
kappa on the verb is 0.590 at S1 and 0.571 after S2, unanimity 0.766 and 0.765. So the fast
stage is where the verb lives, which is what the H3ERE2 design note assumed.

Two verbs are both S1-determinate and kind-pure: **withdraw -> Record 9/9** and
**authorize -> Rules 6/6**. `replace` is determinate (unanimity 0.845) but carries almost no
kind information (purity 0.11 over 97 items) — it is the default verb, 78% of all traffic.
`recant` is middling (unanimity 0.714) and points at Identity 5/7, NOT at Facts as the design
note predicted from the alignment runs. `attest` and `authorize` are the indeterminate pair
(unanimity 0.200 and 0.000). And `carries` — the verb the whole architecture is named for —
was emitted once in 372 judgments: **no family detects the wearing operation at triage grain**,
which is an argument for the recursion, not against it.

Read against the design note's staked guess (X = 2 or 3, on delegate/withdraw/recant): the
measurement splits the note's two criteria apart. By DETERMINACY the fast set is
{replace, withdraw, recant}; by KIND-PURITY it is {withdraw, authorize}. Only `withdraw`
satisfies both. X = 1 on the conjunction, 3 on determinacy alone.

## What is NOT claimed

1. **This is calibration.** Every number above was produced on data the tuning saw. The verdict
   is the single-shot held-out run named in T1, which I have not touched.
2. **The curated discriminators are corpus-shaped.** The declared-basis and arrangement tests
   were written after reading the calibration corpus's own author notes. The held-out curated
   set is the odd lines of the SAME corpus and shares its authoring conventions, so a held-out
   curated result will be optimistic relative to a genuinely independent corpus. The held-out
   WILD sample is the honest generality test.
3. **The GLM instrument changed.** Baseline PANEL-2 ran GLM with reasoning on. The candidate
   runs it off. Like-for-like DeepSeek+Qwen figures are reported alongside every headline for
   exactly this reason.
4. **Premises is not fixed.** 0.472 pooled, against a baseline of 0.167. It is much better and
   still the worst kind by a wide margin. Its residue is Premises->Model (12) and
   Premises->Circumstances (6): a declared basis and an applied model are genuinely close, and
   the tests separate them only partly.
5. **The fast path barely runs on curated** (4.8%) because that corpus is two-thirds deep by
   construction. Its value is a wild-traffic property, and the wild numbers below are where it
   is actually tested.

## Spend

Metered per call in `H3ERE2_TUNING/spend.jsonl`: **$1.20** for all tuning — 14 screening and
confirmation runs, three worker design briefs, one adversarial critique round.

The frozen orchestrator run is NOT in that ledger (`h3ere2.py` keeps none) and was estimated
from reconstructed prompt sizes plus seven metered calls in its exact configuration at
**~$1.2-2.1**, dominated by GLM-4.5's hidden reasoning tokens. The combined figure is over the
$2.00 fence. This was escalated to the orchestrator mid-run with the measurement and the
verified fix; the job was stopped shortly afterwards, having completed A-curated (372) and
A-wild (1035) and, on a relaunch, B-curated (372), with B-wild partial at 145.

Screening protocol used throughout to protect the fence: variants screened on ONE family
(~$0.03 per 124-item pass), finalists confirmed on three; stage 2 screened ALONE against
recorded stage-1 outputs so its accuracy is measured independently of routing; and the
round-3 gate change re-ran only the 37 affected traces and spliced them, rather than
re-running all 372.

## Reproduction

    cd scratchpad/TRANSITION_MAP/H3ERE2_TUNING
    python3 h3ere2_v2.py full <dataset.jsonl> <out.jsonl> v4 a5 -     # all three families
    python3 - <<'X'                                                   # score
    import sys; sys.path.insert(0,'.'); from score import *
    X

Artifacts: `round0_anatomy.md` (frozen-build error anatomy, all four arms),
`round1_2_3_tuning.md` (the tuning rounds, including the rejected candidates),
`FINAL_curated.jsonl` + `FINAL_curated_reroute.jsonl` (the curated calibration run),
`FINAL_wild.jsonl` (the wild calibration run), `spend.jsonl` (the ledger),
`s1_proposals.json` / `s2_proposals.json` / `critique_a5.json` (worker output),
`s1scr_*.jsonl` / `s2scr_*.jsonl` (the screens).

## Held-out discipline

The T1 held-out sets were not read, not sampled and not run. `corpus_full.jsonl` odd lines
were never loaded by any script in this directory; no new wild sampling was performed; the
wild calibration subsample is a deterministic every-third slice of the ALREADY-SEALED 345
calibration units, written to `wild_sub.jsonl` for audit.
