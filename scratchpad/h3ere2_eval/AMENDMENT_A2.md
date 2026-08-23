# h3ere2 PREREG — AMENDMENT A2: the soft encoding
**Written 2026-08-23, before any h3ere2 judgment exists.** Proposes a third run, to follow
the wild (J1-scoped) and gold-label (A1.2) runs. Neither of those is displaced.

## The structural problem A1.2 does not fix

`model-scout` observed that the wild run "cannot answer the prereg's actual claim about the
engine doing multi-step reasoning per item — because there is nothing per-item for it to
reason from." That is right, and **it is not a property of the substrate. It is a property of
the pipeline as built.**

The encoder emits a **single categorical label**. The path is then a deterministic function of
that label. So the engine's output is **per-category, not per-item** — with 4 surfaces the
treatment has at most 4 levels, no matter how many items are fed through it. A1.2 raises n from
2 to 4; it does not make the reasoning per-item. **No substrate can, while the interface
between the two stages is one categorical token.**

## The fix: seed from the distribution, not the argmax

The classifier **already computes logprobs over all four surfaces** and we discard everything
but the maximum. Instead:

- take the softmax over the four surface logprobs,
- seed **every** block, with amplitude proportional to its probability mass (split within a
  block as the current uniform rule does),
- relax as before.

`x₀` then varies **continuously per item**, so the relaxation path varies per item, and the
engine is doing work that depends on *this* change rather than on its category. **This uses
information the pipeline already produces and currently throws away — no new model, no new
labels, no additional inference cost.**

It is also strictly more faithful to the object: a real change rarely lands purely on one
kind, and the taxonomy's own confusion structure (Premises/Facts, Structure/Manner,
Model/Facts) says the boundaries are genuinely graded.

## Why this makes the primary testable
Under hard encoding, arm C is a handful of fixed orderings and a win could always be a property
of those particular paths. Under soft encoding **every item gets a distinct path**, so a C-vs-B
win is evidence about the *coupling's response to varying input* — which is the prereg's claim.

## Design, fixed now
- **Arms unchanged:** A base / B scrambled / C real. Scramble construction unchanged (off-diagonal
  permutation preserving symmetry, ten draws, the non-relabelling guard retained).
- **Same substrate as A1.2** (the 92-item frozen split), so soft-vs-hard is a controlled contrast:
  the *only* change is the encoder→state mapping.
- **Report hard and soft side by side.** If soft encoding does not change the verdict, the
  categorical bottleneck was not the limiting factor and that is worth knowing.
- **Guard against a new confound:** soft seeding could make all paths converge toward a single
  "average" ordering, which would *reduce* between-item variation rather than increase it.
  **Measure and report the number of distinct arm-C paths before judging.** If it is not
  materially above 4, the amendment failed on its own terms and must be reported as such.
- Kill unchanged: if C does not beat B, the coupling contributes nothing to response quality.

## Honest status
This is a **proposed improvement to the instrument, written before any verdict exists**, not a
response to a disappointing result. If the wild or gold runs return a clean answer, this run
still adds the per-item claim they cannot make.
