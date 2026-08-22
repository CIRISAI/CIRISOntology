# H3ERE2 TUNING ROUNDS 1-3 (calibration only, AMENDMENT T1)

Method throughout: three third-party families (DeepSeek-V3.1, Qwen3-235B, GLM-4.5) each
propose independently against a brief carrying the MEASURED error anatomy; a second family
cross-critiques adversarially; candidates are adopted only if they survive MEASUREMENT on
calibration data. Screening runs use ONE family (~$0.03 per 124-item pass) to protect the
spend fence; only finalists are confirmed on three. Every call is metered to `spend.jsonl`.

## Round 1 — the gate

Diagnosis (round0_anatomy.md, section 2): S1 never returns DEEPER and its scalar confidence
is inert. All three worker families returned the SAME diagnosis independently — a model asked
to choose among four concrete options and one vague "other" takes an option — and the same
class of fix: force the model to name a DEEP candidate and then compare the two readings.

Four S1 variants built and screened on 124 curated items (DeepSeek):

| variant | DEEPER-recall | false-route | fast-exit | fast-exit acc | best_deep acc |
|---|---|---|---|---|---|
| v0 frozen | 0.000 | 0.000 | 0.954 | 0.928 | n/a |
| v1 two candidates, model picks winner | 1.000 | 1.000 | 0.000 | n/a | 0.756 |
| v2 deep kinds given content, one choice | 0.707 | 0.167 | 0.476 | 0.971 | n/a |
| v3 two candidates + ternary verdict | 0.805 | 0.619 | 0.258 | 16/16 | 0.817 |
| v4 = v3 + inherited frame + four boundary tests | 1.000 | 0.905 | 0.032 | 4/4 | 0.793 |

ADOPTED: v4. Two repairs carried it. First, the ternary SURFACE_ONLY/CLOSE/DEEPER verdict —
a real gate where a scalar confidence was not. Second, and larger: **H3ERE2 had dropped the
retention/comparison frame that the licensed single-pass instrument carries**
(`panel2_annotate.py`, BASE condition), which is why it read Circumstances at 0.000 where the
baseline reads 0.733. v4 inherits that frame verbatim. REJECTED: v1 — its two-candidate
ORACLE ceiling is 0.782, so the architecture it implies is capped below what S2 later reached.

## Round 1 — the conscience, and a negative result kept

A two-sided S3 was written so the conscience could convict the DEEP reading, not only bless
it. Measured, composed, on 116 traces: **it FAILed 93% of the time**, 71% of those FAILs
landed on answers that were already correct, and the guided retry damaged 29 items while
improving 11. Composed accuracy fell to 0.578 against 0.774 for the same S2 with no
conscience at all. A conscience that always fails is inert in exactly the way the confidence
gate was inert.

Counterfactuals on the same traces (free, no new calls):

| final-answer rule | accuracy | deep |
|---|---|---|
| as-run: unverified retry wins (the frozen rule) | 0.578 | 0.474 |
| keep the first S2 answer, ignore S3 | 0.733 | 0.803 |
| accept the retry only if the retry itself PASSES | 0.750 | 0.803 |

ADOPTED: the frozen one-sided S3 wording (measured FAIL rate 0.202 on the final candidate,
against 0.93 for the two-sided one) plus the **keep-first-unless-verified** retry rule. The
prereg's "final = S2's second answer flagged UNVERIFIED" is the one frozen mechanic this
tuning changes, and it is changed on a measured 29-against-11 margin.

## Round 2 — stage 2

S2 was screened ALONE, fed recorded S1 outputs, so its accuracy is measured independently of
routing (124 items, DeepSeek):

| S2 variant | accuracy | deep | surface |
|---|---|---|---|
| baseline single-pass, for reference | 0.737 | 0.626 | 0.952 |
| a2/a3: carries-inversion + keyed discriminators | 0.774 | 0.817 | 0.690 |
| a4: a3 + Identity protection + tightened Circumstances test | 0.823 | 0.793 | 0.881 |
| a5: a4 + declared-basis test + arrangement test | **0.855** | **0.841** | 0.881 |

a3 bought deep accuracy by wrecking surface accuracy — Identity fell to 4/12, read as Model.
The repair is the PROTECT block: over-reading is exactly as wrong as under-reading, and a
renaming does not become a framework change because a framework could be imagined behind it.
Identity recovered to 11/12.

a5 attacks the two kinds still failing. Its first draft used a "ripple test" — *every other
statement keeps its wording while its meaning changes*. **Adversarial critique killed that
wording**: two families independently objected that the criterion is not CHECKABLE from a
BEFORE/AFTER pair plus a change site, and both proposed the same substitute, which was
adopted — a positional check on the declaration (units, epoch, coordinate frame, counting
convention, benchmark) plus a textual check that the remainder is unchanged. Premises rose
4/12 -> 7/12 and Facts 7/10 -> 9/10.

## Round 3 — the gate, again, on three families

The single-family screen flattered v4. Confirmed on all three families the candidate read
accuracy 0.766 and **deep 0.720 against a 0.726 bar — short by half a point**, i.e. by 1.5
items out of 246. The cause was located exactly, and it was the gate, not S2: DeepSeek
fast-exited 7 Circumstances items and Qwen 9, while GLM — which routes nearly everything —
scored Circumstances 9/10. **All 23 unsafe fast-exits had named Circumstances as their own
deep candidate and cleared it anyway.**

Fast-path precision, split by the surface reading it cleared:

| cleared reading | n | precision |
|---|---|---|
| Manner / Rules / Identity | 18 | **0.889** |
| Facts | 37 | **0.405** |

ADOPTED: **triage may not clear a Facts reading.** This is not a patch keyed to one kind; it
follows from the taxonomy. Facts is the surface that Circumstances, Premises and Model all
wear — they are three of the measured boundary channels — so a Facts reading is precisely the
one a cheap stage cannot certify, and only S2 can. The rule is implemented as the environment
switch NO_FAST_ON_FACTS so the pre-round-3 behaviour remains reproducible.

Effect on the three-family run (the 37 affected traces were re-routed through S2/S3 and
spliced, rather than re-running all 372): 21 deep items rescued from a guaranteed loss,
16 surface items needlessly re-routed at cost only. Circumstances 0.433 -> 0.967.

## Round 3 — the reasoning-token repair

GLM-4.5 is a reasoning model given the same 2,500-token ceiling as the other two families.
Metered: it spends ~1,400-2,600 completion tokens on a single classification, ~10x the cost
of DeepSeek or Qwen, 94s against 3s, and **every parse failure in the frozen A-curated arm
(11 of 11) was a GLM reasoning-token truncation**. Passing
`chat_template_kwargs={"enable_thinking": false}` returns the identical structural answer at
75 tokens. ADOPTED. Coverage went 0.944 -> 1.000.

This is an instrument change and is flagged as one: the baseline panel ran GLM WITH thinking,
so the three-family comparison against baseline is not strictly like-for-like. The
like-for-like check is reported alongside every headline: on DeepSeek and Qwen alone, whose
configuration is unchanged, the candidate reads accuracy 0.806 and deep 0.811 — better than
the pooled figure, so the result is not being carried by the GLM change.

## Round 4 — the Record repair, attempted twice and REJECTED both times

The wild-only defect from the freeze report: the candidate assigns Record to 9.0% of wild
traces against the baseline's 2.0%, and 52% of those land on deletion-shaped units, because
the S2 Record test fires on any removal of text.

Two repairs were written and measured with stage-2-alone probes against recorded stage-1
outputs (69 wild traces, 60 curated traces, ~$0.07 total — no pipeline re-runs):

- **a6**, a full RECORD_TEST paragraph stating what Record is not;
- **a7**, a single clause appended to a5's existing Record sentence, changing nothing else.

| | curated control (Record+Confidence targets, S2 alone, DeepSeek, n=20) | wild Record on deletions | wild Record on non-deletions |
|---|---|---|---|
| a5 incumbent | **16/20** (Record 9/10, Confidence 7/10) | 0.444 | 0.455 |
| a6 paragraph | 11/20 (Record 6/10, Confidence 5/10) | 0.250 | 0.303 |
| a7 one clause | 13/20 (Record 8/10, Confidence 5/10) | 0.361 | 0.364 |

**Both are rejected.** Each buys wild Record suppression at a proportional cost in curated
Record and Confidence accuracy, and — the decisive point — neither actually fixes the item.
Where a5 said Record on a deletion, a6 says **Premises** 13 times and a7 says Premises 12
times. The error moves; it does not go away.

That result is about the taxonomy, not the prompt. A deletion in a wild revision stream has
no comfortable home in the 11+1: the kinds describe what a change does to content, and a
deletion removes content without asserting anything, so the panel scatters across Record
(the evidence is gone), Premises (something taken as given is gone), Facts and Structure.
Two independent prompt interventions, one heavy and one minimal, both land in the same place.
This looks like a coverage gap in the object at wild grain, and a plausible contributor to the
wild agreement ceiling itself.

It also sharpens the L2 problem stated in round 0. Deletion-shaped units RAISE the incumbent's
measured kappa (0.3858 with them, 0.3617 without) because all three families agree on Record.
So the incumbent's wrong-but-agreed label is **propping up the number that L2 scores**, and
repairing the validity defect would LOWER the agreement statistic. On this substrate, validity
and L2 point in opposite directions, which is the strongest argument yet that agreement alone
is the wrong licence criterion for this instrument.

**Adopted: none. a5 stands.** a6 and a7 remain in `h3ere2_v2.py` (S2S) so the measurement is
reproducible, and the defect stays on the record as diagnosed-and-unfixed.
