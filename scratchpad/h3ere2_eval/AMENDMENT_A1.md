# h3ere2 PREREG — AMENDMENT A1
**Written 2026-08-22, after the encoder distribution was seen and BEFORE any response was
judged or any judge output existed.** The trigger is a validity failure, not a result.

## The trigger: the encoder is non-discriminative on the prereg's substrate

The 4-way encoder returns **`Facts` for all 170 WILD items** — median decision margin 4.24
nats, only 3/170 with a runner-up within 1.0 nat, uniform across all three unrelated streams
(fedreg 60, github 50, osm 60). It is **not** a wiring defect: on four hand-written
unambiguous cases the same encoder, same protocol, discriminates correctly.

**Stated precisely, because the distinction matters: the encoder is non-discriminative here,
NOT demonstrably wrong.** The WILD items carry no gold labels, so we cannot tell whether
"Facts" is a correct reading of federal-register abstracts, github changes and OSM edits — a
case can be made that many such changes genuinely are assertive-family — or a collapse. What
is certain is that it carries **no per-item information**.

## Why this invalidates the primary as specified

The surface is the **only** per-item input to the engine. A constant surface means a constant
seed set, so **arm C's path is byte-identical across all 170 items**, and each scramble's
likewise. The treatment has **zero variation**: 170 documents, but n=1 in the thing being
tested. Any C-vs-B difference would be a property of one particular ordering, not of the real
coupling as a class.

The prereg's primary is therefore **not testable on this substrate**. That is a validity
failure and must not be reported as a null.

## A1.1 — the original run completes and is reported, with its scope narrowed
It is already generating and is cheap to finish. It will be reported as answering only:
**does the real coupling's ONE fixed propagation order yield better advice than ten scrambled
fixed orders?** It may **not** be described as testing whether the pipeline reasons per item,
because on this substrate it demonstrably does not.

## A1.2 — the amended primary: isolate the physics with a GOLD encoder
Re-run on the **92-item frozen test split**, using **gold surfaces** in place of the
classifier. Rationale: the prereg's question is whether the *coupling* produces better advice,
and routing through a classifier compounds encoder error into that test. Gold labels remove
the encoder as a variable entirely, and the split's label histogram (Facts 35, Manner 30,
Rules 16, Identity 11) gives genuine per-item treatment variation — 4 distinct real paths
instead of 1.

Everything else is unchanged and binding: same three arms, same scramble construction, same
judge protocol, primary is **C vs B**, kill unchanged.

**This is a substrate change made after seeing an encoder distribution. It is disclosed as
such.** It is not result-driven — no judge output exists — but the reader should weigh it
knowing when it was written.

## A1.3 — judging design (volume was left open in the prereg)
10 scrambles x 170 items = 1700 B responses; judging C against every scramble at both orders
is 3400 comparisons. Instead: **assign each item one scramble draw, rotating through the ten**
(item *i* gets draw *i* mod 10). This samples all ten scrambles across the item set while
keeping the comparison paired and the volume at 170 x 2 orders = 340 judgments per run. The
scramble distribution is represented without paying 10x.

## A1.4 — the encoder collapse is itself a REPORTABLE FINDING
Independent of the h3ere2 result: a classifier scoring 0.70–0.78 on the authored split
returns a single class on wild text from three unrelated streams. Whether that is domain shift
or correct reading is **undetermined and requires gold labels on wild items to settle**. It
bears directly on the h3ere2 concept — a decomposition stage that does not vary with input
cannot drive an adaptive pipeline — and it is reported whatever the judged result turns out
to be.
