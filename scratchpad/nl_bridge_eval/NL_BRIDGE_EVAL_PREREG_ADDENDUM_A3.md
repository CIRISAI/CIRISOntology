# ADDENDUM A3 — the q4f16 equivalence gate

Written **before any q4f16 artifact was built or scored.**

## I am overruling the suggested criterion, and here is the arithmetic

The proposal was: equivalent iff McNemar non-significant AND the accuracy gap is
within a band. **The McNemar half of that is structurally uninformative at
n = 92**, and this is not a judgement call — it is a property of the test.

McNemar's exact test sees only the DISCORDANT pairs. At any n, the smallest
discordant total that can reach p < 0.05 **even when every discordant item falls
one way** is **6**:

| discordant items | best-case p (all one way) |
|---|---|
| 3 | 0.250 |
| 4 | 0.125 |
| 5 | 0.0625 |
| **6** | **0.0312** — first reachable |

A quantisation good enough to ship will agree with full precision on ~95%+ of
items, i.e. roughly 4-5 disagreements out of 92. **In that regime McNemar cannot
return a significant result no matter what the data say.** Passing the test
would therefore be guaranteed in advance and would evidence nothing. Reporting
"non-significant, therefore equivalent" would be reporting the sample size, not
the artifact.

The second half is also weak on its own: **two models can score identically while
disagreeing on many items.** Equal accuracy is not sameness — accuracy
marginalises away exactly the per-item behaviour we are trying to certify.

## What this split CAN and CANNOT resolve — stated plainly

- **Accuracy difference:** at n = 92 the paired 95% interval on an accuracy gap
  is roughly **±0.09**. So this split **cannot certify equivalence tighter than
  about 9 percentage points by accuracy**. A real 5-point degradation would pass
  an accuracy-based test. **This is too coarse to certify a shipping artifact**,
  and it is the honest answer to the question as posed.
- **Prediction agreement:** resolves at 1/92 = **0.011 per item** — roughly
  eight times finer than the accuracy route, because it does not marginalise.
- **Per-item logprob deviation:** continuous, no discretisation loss, by far the
  most sensitive quantity available at this n.

## Primary instrument (replacing accuracy + McNemar)

1. **Prediction agreement rate** — fraction of the 92 items where both builds
   emit the SAME label. This is the primary number.
2. **Per-item logprob deviation** over the four label continuations: mean and max
   |Δ logprob|, and the rate at which the argmax margin flips sign.
3. Accuracy and McNemar are still reported, **explicitly labelled underpowered**,
   so the record shows them rather than hiding a weak instrument.

## Pre-registered equivalence criterion

**EQUIVALENT** iff all three hold:
- prediction agreement **>= 0.95** (at most 4 disagreements of 92), AND
- accuracy gap **<= 0.03**, AND
- mean per-item |Δ logprob| **<= 0.05** with no item flipping its argmax by a
  margin greater than 0.5.

**NOT EQUIVALENT** if agreement < 0.90 or the accuracy gap exceeds 0.06.
Anything between is **INCONCLUSIVE AT THIS N**, reported as such, with the
recommendation to widen the corpus rather than to ship on a null result.

## Arms — all on the SAME frozen 92 items, same prompt, same decoding

The comparison is run on the **FINE-TUNED weights**, not the base model: the
deployed artifact is the fine-tune, and a base-model equivalence result does not
transfer to it.

- **A. torch bf16** — full-precision reference (already measured: 0.783).
- **B. ONNX fp32** — runtime control, isolating ONNX-vs-torch from quantisation.
- **C. ONNX q4f16** — the gate.

B is mandatory. Without it, any A-vs-C difference is uninterpretable, because it
would bundle the runtime change with the quantisation change.

## THE LARGER RISK, recorded here because it is already measured

The native target is Q4_K_M under llama.cpp; the browser target is q4f16 under
rten. Those differ in **runtime, tensor format, chat template and sampling**, not
only in quantisation. This programme has already measured that confound: the
SAME Qwen3-0.6B weights scored **0.467 under ollama and 0.315 under
transformers** — a 15-point swing from harness alone, **larger than any plausible
quantisation effect.**

Therefore: the q4f16 gate is run **within one runtime** (A/B/C above), and
cross-runtime artifact equivalence — the browser build versus the native build —
is a **separate gate that this addendum does not discharge**. Quoting a
within-runtime q4f16 pass as evidence that the browser artifact matches the
native one would be exactly the error this note exists to prevent.
