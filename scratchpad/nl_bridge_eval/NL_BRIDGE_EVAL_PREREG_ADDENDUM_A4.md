# ADDENDUM A4 — the Q4_K_M equivalence gate (the NATIVE artifact)

Written **before any GGUF was built or scored.**

## Why this run exists

A3 gated the browser artifact and I wrote that "the native GGUF target is unaffected."
**That was too strong and is corrected here: it was UNTESTED, not unaffected.** Q4_K_M is
also a 4-bit quantisation of the same fine-tuned weights, and A3's own proposed mechanism —
that a LoRA fine-tune's signal lives in small weight deltas that 4-bit rounding destroys —
applies to it in principle. Q4_K_M is a better quantiser (k-quant, per-block scales,
importance weighting) so it may well survive, but that is a hypothesis, and **Q4_K_M is
what ships**: every demo number the team holds runs on it.

## Design — within ONE runtime, deliberately

**F16 GGUF vs Q4_K_M GGUF, both under llama.cpp.** Same runtime, same chat template, same
sampling, same masking. Only the quantisation varies.

This is not a reversal of A3's refusal to compare native against the ONNX arms. That refusal
stands: cross-runtime spans template and sampling, and this programme measured a **15-point
swing from harness alone** (ollama 0.467 vs transformers 0.315 on identical weights), which
dwarfs any quantisation effect. Staying inside one runtime sidesteps that entirely.

Both builds are produced from the **same merged fine-tuned weights** (`ft_merged/`) — the
deployed artifact — not from the base model.

## Arms

- **E. F16 GGUF** — full-precision-in-runtime reference.
- **F. Q4_K_M GGUF** — the shipping native artifact.

Both scored on the **same frozen 92 items**, same prompt, same enum-masked decoding.

## Instruments — same hierarchy as A3

1. **Prediction agreement rate** (primary). Accuracy marginalises away per-item behaviour;
   two builds can score identically while disagreeing on many items.
2. Accuracy gap (secondary, and known coarse).
3. Decision-point logprob deviation, **if the runtime exposes logprobs**. If it does not,
   that is recorded as unavailable rather than substituted for.

## Power — carried over from A3, unchanged

n = 92 cannot certify equivalence tighter than **about ±9 accuracy points**. Prediction
agreement resolves at 1/92 = 0.011 per item, roughly eight times finer, which is why it is
primary. McNemar is reported but **remains structurally underpowered**: it cannot reach
p < 0.05 below 6 discordant items however they fall.

## Pre-registered criterion (identical to A3, so the two gates are comparable)

**EQUIVALENT** iff:
- prediction agreement **>= 0.95** (at most 4 disagreements of 92), AND
- accuracy gap **<= 0.03**.

**NOT EQUIVALENT** if agreement < 0.90 or the accuracy gap exceeds 0.06.
Between those: **INCONCLUSIVE AT THIS N**, with the recommendation to widen the corpus
rather than ship on a null.

## What a pass and a fail each mean

- **Pass** — Q4_K_M preserves the fine-tune, the demo numbers stand, and A3's failure is
  specific to the naive RTN ONNX quantiser rather than to 4-bit as such.
- **Fail** — the working system is materially worse than every number quoted for it, and
  the native target needs a better quantisation exactly as the browser target does. Reported
  as plainly as a pass.

## Note on the reference

Arm E is F16 **in llama.cpp**, not fp32. A3 measured bf16 costing 7.6 points against fp32 in
transformers, so a runtime's own float precision is not free. Arm E is therefore the correct
*within-runtime* reference for what Q4_K_M costs, and is NOT a claim about absolute ceiling.
