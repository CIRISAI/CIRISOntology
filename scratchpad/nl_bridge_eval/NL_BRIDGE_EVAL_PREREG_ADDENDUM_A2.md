# ADDENDUM A2 — the Qwen3-0.6B 4-way fine-tune

Written **before the fine-tune was run and before any fine-tuned score was seen.**

## What is being tested

Whether task-specific fine-tuning on the thin 158-item train budget lifts
Qwen3-0.6B's 4-way surface accuracy materially above its own zero-shot 0.467.
SmolLM2-360M is NOT fine-tuned: it read floor at both granularities (0.060 at 12,
0.250 at 4 — uniform chance), so there is no signal to amplify and spending the
budget on it would be spending it to confirm a null already measured twice.

## Data — the freeze is preserved

- **Test: unchanged.** The same frozen 92 items (100-item split minus 8 Record).
  Not seen during training, not used for model selection, not used for early
  stopping.
- **Train: the 158-item train split**, subdivided **138 train / 20 dev**,
  stratified by surface family, seed 20260822. Dev is used for early stopping and
  nothing else. No test item is involved at any stage.

## Method

LoRA on `Qwen/Qwen3-0.6B`, 4-way surface target, **identical prompt** to the
zero-shot run (`run_eval4.py`'s system prompt and item rendering, family glosses
quoted from `Site.block`'s source comments). Scoring is **constrained argmax over
the four label strings** — the likelihood-space equivalent of masked decoding, so
the fine-tuned model is held to the same "format is guaranteed, only slotting
varies" condition as the zero-shot run.

## MANDATORY CONTROL — harness shift

The zero-shot numbers were produced through ollama; the fine-tuned numbers come
through transformers. That is a different stack, so **zero-shot Qwen3-0.6B is
re-scored under the transformers harness first.**

It must land within **±0.08** of the ollama figure (0.467), i.e. in
**[0.387, 0.547]**. If it does not, the two harnesses do not measure the same
thing and **the fine-tune comparison is reported as invalid** rather than
explained away. Every comparison below is against the transformers-harness
zero-shot number, not the ollama one.

## Anchors

| | 4-way top-1 |
|---|---|
| majority class ("Facts") | 0.370 |
| **Qwen3-0.6B zero-shot (the thing to beat)** | **0.467** |
| qwen3:14b zero-shot direct | 0.543 |
| frontier panel, 12-way projected (NOT our route) | 0.814 |

## DECISION RULE — stated before the run

- **FINE-TUNE WORKS** iff fine-tuned beats its own zero-shot on the same 92 items
  at **McNemar exact p < 0.05** (paired data; marginal CIs are not the test).
- **SHIP-WORTHY** iff fine-tuned **>= 0.543** — matching or beating what a 9.3GB
  model achieves zero-shot, from a 522MB model. This is the bar that would
  vindicate the pin flip.
- **BUDGET-BOUND** if fine-tuned improves numerically but fails McNemar. The
  honest reading is then that **158 items is too thin**, NOT that the model
  cannot do the task — and the recommendation becomes "label more data", with the
  dev curve reported as evidence.
- **FAILS** iff fine-tuned does not exceed its own zero-shot at all. That would
  make sub-gigabyte the wrong tier even with the coarser cut.

## Pre-declared risks

138 training examples across 4 imbalanced classes is very thin; overfitting is
the expected failure mode. The dev curve is reported whatever it shows. A
fine-tuned model that collapses onto "Facts" (the 0.370 majority) is a FAIL, not
a pass, however its loss curve looks — the label histogram is reported alongside
accuracy for exactly this reason.
