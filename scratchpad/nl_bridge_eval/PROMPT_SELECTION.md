# Deployment prompt selection — written BEFORE the single frozen-test re-gate

**Not prereg-breaking.** Addenda A1/A2 governed *model selection*, which is settled
(Qwen3-0.6B chosen). Tuning a deployment prompt is a different activity. The 92-item test
split was not read during any of the tuning below and is read exactly once, after this note.

## Selected: V1_rules_hint

Baseline system prompt, unchanged, plus one appended paragraph:

> IMPORTANT: a change is Rules whenever it changes what is REQUIRED, PERMITTED, FORBIDDEN,
> prioritised, or the order/sequence of steps - even if it also mentions facts or figures.
> Deadlines, thresholds, obligations, approvals, and procedural reordering are Rules, not Facts.

## Why, on the deployed artifact (ft-q4kmb, Q4_K_M)

| variant | pool(138) | clean dev(18) | Facts | Rules | Identity | Manner |
|---|---|---|---|---|---|---|
| V0 baseline | 0.855 | 0.667 | 52/52 | **26/37** | 9/13 | 31/36 |
| **V1 rules-hint** | **0.935** | **0.722** | 52/52 | **34/37** | 10/13 | 33/36 |
| V2 member-glosses | 0.826 | 0.722 | 52/52 | 24/37 | 8/13 | 30/36 |
| V4 member+hint | 0.877 | 0.722 | 52/52 | 32/37 | 9/13 | 28/36 |
| V3/V5/V6 (few-shot) | 0.59-0.67 | 0.56-0.67 | — | — | — | — |

V1 is the only variant that lifts the target family substantially (**+8 Rules**) while harming
**no** other family, and it is best on both the contaminated pool and the clean dev slice.

## Two findings that shaped the choice

**1. Few-shot examples HURT the fine-tuned model, badly** — every few-shot variant lands
0.59-0.67 against a 0.855 baseline. The fine-tune learned a single-turn format; prepending
exemplar turns breaks it. The prefix-reuse cost argument is sound, but the quality effect
runs the other way. **If this prompt lever works it works through instructions, not examples.**

**2. The base model is NOT a valid proxy for selecting a prompt for the fine-tuned model.**
I ran the same sweep on base Qwen3-0.6B (where all 138 items are un-memorised) hoping for a
clean 138-item selection signal instead of 18. The two models respond **oppositely**:

| | base model | fine-tuned Q4_K_M |
|---|---|---|
| V1 Rules predicted | **119 of 138** | 34 of 138 |
| V1 Facts recall | 3/52 (from 32/52) | 52/52 (unchanged) |
| V1 overall | 0.500 -> **0.341** | 0.855 -> **0.935** |

On a model without task knowledge the hint is a **bias sledgehammer** ("everything is Rules").
On a model with it, the same words are a **calibration nudge**. So the clean-but-wrong-model
signal is worse than the noisy-but-right-model signal, and I am selecting on the latter while
recording that its pool is memorisation-contaminated.

## Known weakness of the tuning signal, stated before the gate

`Facts = 52/52` for every variant on the tuning pool is memorisation (the model was fitted to
loss 0.004 on 120 of these 138). On the frozen test split Q4_K_M read Facts 32/34 and
**Rules 8/24**. So the pool overstates absolute accuracy badly; what it can still show is the
*relative* movement of Rules, which is what V1 was chosen for.

## Pre-registered expectation for the gate

Q4_K_M baseline on test: **0.641**, Rules **8/24**.
V1 is predicted to raise Rules recall. **A gain concentrated in Rules with no loss elsewhere
confirms the lever; a flat or negative result means the loss is in capability rather than
elicitation, and the answer is a better quantiser rather than a better prompt.** Both are
reported plainly. One run, no re-selection afterwards.
