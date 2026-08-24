# ADDENDUM A1 — the 4-way surface run

Written **before any model was run on the 4-way task**. The 12-way results are
already known; nothing about them was used to choose anything below except where
explicitly stated as a parallel-construction anchor.

## The grouping is Lean-derived, not hand-rolled

Parsed directly from source, not transcribed:
`Site.block` (`Core/Surface.lean`) composed with the inverse of `Site.kind`
(`Core/Generator.lean`), with the surface face from `Block.surface`.

| block | n | surface (`Block.grossKind`) | member kinds |
|---|---|---|---|
| assertive | 4 | **Facts** | Facts, Confidence, Model, Premises |
| directive | 3 | **Rules** | Rules, Priorities, Process |
| declaration | 1 | **Identity** | Identity |
| carrier | 3 | **Manner** | Structure, Manner, Circumstances |

Verified against the Lean's own theorems: `block_cards = [4,3,1,3]` reproduces,
and `gross_four_plain = ["Facts","Rules","Identity","Manner"]` reproduces. Map
frozen at `surface_map.json`.

## Record drops out, and this is forced by the object

`Site.block` is total on the **11 site-generated kinds**. Record (`testimonial`)
is provably NOT site-generated (`record_not_site_generated`), so it has no block
and therefore **no surface**. The 4-way task is defined on 11 kinds, not 12.

Consequence: the frozen test split's **8 Record items are excluded**, leaving
**n = 92**. Same frozen split otherwise — no re-draw, no re-shuffle.

## Anchors, computed from existing panel data BEFORE candidates ran

| baseline | 4-way top-1 |
|---|---|
| uniform random over 4 labels | 0.250 |
| **majority-class (always "Facts")** | **0.370** |
| Llama-4-Scout-17B | 0.777 |
| gpt-oss-120b | 0.819 |
| gemma-3-27b-it | 0.845 |
| **frontier panel pooled** | **0.814** |

**The families are imbalanced** — Facts 0.370, Rules 0.265, Manner 0.261,
Identity 0.105. So uniform chance (0.250) is NOT the right floor: a model that
answers "Facts" every time scores 0.370 and has learned nothing. The bar is set
against the majority-class baseline instead, and this is a deliberate departure
from "anchor to chance at 4 labels (0.25)", which would have been too generous.

## DECISION RULE — stated before any candidate ran

- **GRIP AT 4** iff top-1 beats the majority-class baseline of 0.370 at
  one-sided binomial p < 0.05. On n = 92 that is **top-1 >= 0.453** (>= 42/92).
- **STRONG GRIP** iff top-1 >= **0.500** (61% of the frontier ceiling, >2.5 SE
  above majority-class).
- **FLOOR AT 4** iff top-1 <= 0.370, i.e. no better than answering "Facts"
  every time. If BOTH candidates read floor at 4, the reported conclusion is
  that **sub-gigabyte is the wrong tier for this task**, not that the 4-way cut
  failed.
- **SmolLM2 vs Qwen3** is judged by **McNemar's exact test on the paired
  outcomes** (same items, paired data — per the A1 methodological correction),
  significance at p < 0.05. Overlapping marginal CIs are explicitly NOT the test.

## Prompt

Same architecture as the 12-way run so the two are comparable: one label out,
masked to the 4 surface names, temperature 0, `think: false`. Family descriptions
are quoted from `Site.block`'s own source comments in `Surface.lean` ("assertive
apparatus: what is claimed, how strongly, under what rule, on what premise", and
so on), so the label semantics are Lean-sourced rather than invented here.

## Positive control

`qwen3:14b` runs the identical 4-way harness. As at 12-way, a candidate floor
reading is only attributable to the models if the control clears the bar.

## What would invalidate this run

Valid-label rate < 1.00; any Record item scored; a changed split; or any
adjustment to prompt or threshold after a candidate score is seen.
