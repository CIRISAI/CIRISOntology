# NL_BRIDGE eval — PRE-REGISTRATION

Written **before either candidate model was run**. Nothing below was chosen after
seeing a SmolLM2 or Qwen3 score.

## Question

Can `SmolLM2-360M-Instruct` (the pinned NL_BRIDGE model) carry enough semantic
grip on the 12-label taxonomy to be worth fine-tuning, or does the extra browser
payload of `Qwen3-0.6B` (919MB vs 388MB ONNX q4, 2.4x) buy enough to be forced?

## Taxonomy — 12 labels, from `Core/WrongKind.lean` (source of truth, not prose)

`WrongKind` has **12 constructors**. `basePlane_card` proves 11 are artifact-local;
`testimonial`/Record is the one frame-relation (`one_frame_dependent`). The
classifier therefore has **12 output labels**. Plain names from `WrongKind.plain`,
discriminator questions from `WrongKind.discriminator` — both quoted verbatim into
the prompt, because the Lean says the discriminator is what "does the classifying
work in practice".

Priorities · Rules · Manner · Identity · Confidence · Facts · Circumstances ·
Process · Model · Structure · Premises · Record

## Corpus and provenance

- **Labelled:** `scratchpad/plane_corpus/run_corpus.jsonl` — 258 authored items,
  gold field `kind_target` (constructor name), all 12 kinds, ~20-24 per kind,
  difficulty clear=192/hard=56 (on the 248-item subset), 5 domains.
- **Reference ceiling:** `scratchpad/plane_corpus/full_judgments.jsonl` — 5,418
  panel judgments, 258 items x 7 conditions x 3 frontier models. BASE condition
  gives the frontier baseline on these exact items.
- **NOT usable as scored test data:** `eco_corpus.jsonl` (170 wild items) carries
  `kind_target: "WILD"` — no gold label. The published "zero modal no-fits"
  result was about whether any label fit, not about accuracy. It cannot score a
  model and is excluded from this eval.

## Split — frozen now, before any run

Stratified by `kind_target`, seed 20260822, deterministic and recorded to disk:
**60% train / 40% test.** The test split is frozen at
`nl_bridge_eval/test_split.jsonl` and **no tuning ever sees it**. Train is for the
future fine-tune only.

## Reference anchors (computed from existing panel data, before candidates ran)

| baseline | top-1 |
|---|---|
| uniform random over 12 labels | 0.083 |
| frontier panel pooled (BASE) | **0.646** |
| best single frontier model (gemma-3-27b-it) | 0.674 |
| worst single frontier model (Llama-4-Scout-17B) | 0.609 |

These are 17B-120B models. They bound what "good" means here: this task is hard,
and 0.646 pooled is the realistic ceiling, not 1.0.

## Method

Both candidates get the **identical prompt** and identical decoding. Output format
is **masked to the 12 labels** (ollama structured output / GBNF grammar, the
functional equivalent of llguidance in production) so the model cannot emit a
malformed or out-of-vocabulary answer. Only semantic slotting varies — which is
precisely the production condition. Temperature 0, greedy, single label out.

## Primary metric

Top-1 accuracy against gold `kind_target` on the frozen test split.

## DECISION RULE — stated before any candidate ran

- **SmolLM2-360M PASSES** iff top-1 >= **0.25** on the test split (3x chance,
  ~39% of the frontier pooled ceiling) **AND** Qwen3-0.6B does not beat it by
  more than **15 points** absolute.
- **Switch to Qwen3-0.6B** iff SmolLM2 < 0.25, **or** Qwen3 - SmolLM2 > 15 points.
- **Both < 0.25** => neither is viable zero-shot; the decision defers entirely to
  a fine-tuned re-run and no zero-shot pick is made.

Rationale for 0.25: three times chance on 12 balanced classes, on a taxonomy the
model has never seen, demonstrates real semantic grip and therefore a fine-tune
worth attempting. Rationale for the 15-point gap: Qwen3 costs 2.4x the browser
payload. A gap under 15 points does not justify that, because zero-shot gaps at
this scale close disproportionately under task-specific fine-tuning. A gap over
15 points means SmolLM2 lacks the grip and the payload is worth paying.

## Secondary, pre-declared

- Valid-label rate. Under masking this MUST be 1.00; anything less is a harness
  bug, not a model result, and invalidates the run.
- Per-kind recall, and confusion concentration on the three boundaries the panel
  study predicted in advance: Premises/Facts, Structure/Manner, Model/Facts.
- Majority-class baseline on the same split, reported alongside.

## What would invalidate this eval

Valid-label rate < 1.00; a test/train id leak; or any change to prompt, split, or
threshold after a candidate score is seen. All three are checked and reported.

---

## ADDENDUM (team-lead, 2026-08-22): paired test replaces the overlapping-CI argument

The report argued the SmolLM2/Qwen3 gap "is inside the noise of two overlapping CIs."
Overlapping marginal CIs are a weak and slightly wrong test here, because **both models
scored the same 100 items** — that is paired data, and a paired test is strictly more
powerful. Ran McNemar's exact test on the shared items:

```
qwen3-0.6B wrong / SmolLM2 right :  6
qwen3-0.6B right / SmolLM2 wrong : 15
discordant                       : 21
exact two-sided p                = 0.0784   -> NOT significant at 0.05
```

**The conclusion survives the better instrument.** The 9-point gap does not reach
significance even paired, so "zero-shot cannot arbitrate this choice" stands, and the
prereg's no-pick outcome was correctly triggered.

One thing NOT to read into this: concordant-correct is zero (no item both models got
right). That looks striking but is unremarkable — at accuracies of 0.06 and 0.15 the
expected count under independence is 0.06 x 0.15 x 100 = **0.9**, so observing 0 is
ordinary. It is not additional evidence of mode collapse. The evidence for mode collapse
is the label histogram (78/100 into two labels, 65/100 into two labels), which is strong
on its own and does not need this.

**Status unchanged: no zero-shot pick. Deferred to the fine-tuned re-run.**
