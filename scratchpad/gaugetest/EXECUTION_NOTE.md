# GAUGE TEST — execution note. Written BEFORE any arm was invoked.

`GAUGE_TEST_PREREG.md` (FROZEN 2026-08-20) governs. This note pins only the choices the
prereg left open, and it is written and timestamped **before** the panel runs. Every item
here is a deviation-in-the-sense-of-a-pinned-detail and is reported in the results §
"Deviations".

## G1 — the ORIGINAL modal

Taken from the existing BASE judgments on disk, `plane_corpus/full_judgments.jsonl`, using
the **same convention as `polarity/build_corpus.py`** (which is the established BASE-modal
convention in this programme): rows with `condition == "BASE"`; rows whose `kind` failed to
parse are dropped as missing votes; modal = plurality over the surviving votes; **a tie for
top (two labels with equal top count) yields NO modal.** Not re-derived, per the brief.

Measured on the 248 corpus items: 774 BASE rows, 3 parse failures, **15 items with no modal
(ties)**.

## G2 — the untouched population (identical in every arm)

Items whose ORIGINAL modal is **defined** and is **neither `Circumstances` nor `Structure`**.
An item with no original modal has nothing to be perturbed *from*, so it cannot enter a
"differs from the original modal" fraction; excluding it keeps the item set identical across
arms, which the prereg requires.

**N = 212** (248 − 15 no-modal − 9 Circumstances-modal − 12 Structure-modal). Fixed now, and
the same 212 ids are scored in A, B and C.

## G3 — an arm's modal, and what a tie inside an arm means

Each arm's modal uses the identical convention (G1) on that arm's own judgments. An item
whose arm-modal is a **tie** has no plurality label; the pre-registered primary counts such
an item as **PERTURBED** (its original label no longer commands a plurality). Rationale: the
alternative — dropping tie items per arm — makes the denominator differ between arms, which
the prereg forbids.

**Sensitivity, also pinned now:** the same three fractions recomputed with arm-ties dropped
pairwise (item excluded from a comparison if it ties in either arm of that comparison).
Reported beside the primary whatever it shows.

`NO FIT` is a label like any other: an item reading `NO FIT` when its original modal was
`Facts` is perturbed. An item where **all three** votes fail to parse has no arm-modal and is
counted as perturbed by the primary rule; the count of such items is reported per arm, and if
it exceeds 5% of any arm the run is declared VOID on protocol grounds (this mirrors the
polarity study's 5% parse-failure VOID threshold).

## G4 — the two-proportion test

"Significantly above zero" is read as **one-sided**: pooled two-proportion z-test of
H0: p_X = p_A against H1: p_X > p_A, α = 0.05. Reported beside it, as sensitivities:
the two-sided p, and **McNemar's exact test** on the paired table (the arms share items, so
the paired test is the more powerful one; it is a sensitivity and not the pre-registered
primary, because the prereg says "two-proportion test").

## G5 — the secondary, where the orphans go

The prereg names "the removed kind's own items (20 Circumstances in B, 20 Structure in C)".
248-item counts by **authored `kind_target`** are exactly 20 `contingent` and 20 `structural`,
so the prereg's numbers identify the AUTHORED-TARGET set, and that is the primary secondary
population. Destination = that arm's modal for the item (ties reported as `TIE`, and included
in the entropy as their own category, since a scattered no-plurality read is itself the
absence of a natural home).

**Labelled sensitivity, pinned now:** the same tables over the MODAL-defined orphans (items
whose ORIGINAL modal was the removed kind: 9 Circumstances, 12 Structure). Small, reported
for completeness, no verdict rests on it.

Entropy is Shannon entropy in **bits** over the destination distribution, reported raw and
normalised by log2(number of available labels in that arm) = log2(11).

## G6 — the prompt adaptation, and the VOID-on-protocol check

The runner imports `plane_annotate.py` and reuses its `CONDITIONS["BASE"]`, `DISC`, `PLAIN`,
`BOUNDARY_NOTES`, `MODELS`, `PRICE`, `ask()` and its temperature/max_tokens verbatim. The
ONLY edits, applied by a single function:

1. the offered-label block loses the removed kind's line;
2. the count word "Twelve" becomes "Eleven";
3. the `one of:` enumeration in the answer format loses the removed plain name.

Nothing else changes. `BOUNDARY_NOTES` names Confidence/Facts and Model/Facts only, so it is
identical in all three arms and introduces no asymmetry between B and C.

**Enforced mechanically:** the runner asserts that the arm-A prompt is byte-identical to
`plane_annotate.prompt_for(item, "BASE")` for every item before any request is sent, and
aborts the run if it is not. This is the prereg's "must match the existing BASE convention
exactly or the run is VOID" check, discharged in code rather than by intention.

## G7 — spend

Cap $0.40 (prereg). Projected from the BASE run's measured per-model token usage:
**$0.2525** for 3 arms × 248 items × 3 models. Spend is accumulated from the API's own
`usage` fields, written to `spend.json` per arm, and the runner aborts at the cap.

## G5b — a confound in the prereg's secondary population, found before any arm output existed

Computed from the ALREADY-PUBLISHED BASE modals (nothing from this test's arms):

| authored kind | n | original modal distribution |
|---|---|---|
| `contingent` (Circumstances) | 20 | Facts 9, **Circumstances 7**, no-modal 2, Identity 1, Manner 1 |
| `structural` (Structure) | 20 | **Structure 9**, Manner 7, Rules 2, Process 2 |

(This reproduces `TWO_WAY_READING.md` §2 exactly, which independently validates that the modal
convention pinned in G1 is the same one the earlier pipeline used.)

The consequence for the prereg's secondary: **9 of the 20 authored Circumstances items already
read `Facts` while `Circumstances` was still on offer.** So "Circumstances's orphans pile into
Facts" is partly true before the treatment is applied — those items are not orphans at all.
Symmetrically, 11 of 20 authored Structure items already read something other than `Structure`.
The authored-target population therefore mixes true orphans with items that never used the
removed label.

The prereg's population is honoured as primary because it is the frozen one. The
**modal-defined orphan** sensitivity already pinned in G5 — items whose ORIGINAL modal WAS the
removed kind (9 with modal `Circumstances`, 12 with modal `Structure`, over the whole 248) — is
the population that actually loses a label, and the results document reports it beside the
primary and explains why. Pinned here, before any arm's judgments were read.

## G7b — K-G2's reading rule, pinned before any arm output was read

K-G2 is prose in the frozen prereg ("if Circumstances's orphans concentrate *coherently* on a
semantic neighbour the way Structure's do"), so it needs a rule, and the rule is fixed here
while the arms are still in flight and no judgment file has been opened.

K-G2 **fires** iff BOTH:
1. Circumstances's orphan distribution is at least as concentrated as Structure's —
   `H(B orphans) <= H(C orphans)` **and** `top-share(B) >= top-share(C)`; **and**
2. that top destination is a block-coherent neighbour, i.e. **not `Facts`**.

Clause 2 is not a loophole, it is the prereg's own text: the staked prediction is that
Circumstances "scatters **or piles into Facts** without block-coherence", and `TWO_WAY_READING`
§2 records `Facts` as the *cross-block* destination — the anomaly, not a coherent home. The
block surface for this block is `Manner` (the destination `Structure` leaks to in that same
table). If clause 1 holds with `Facts` on top, K-G2 does **not** fire, the staked prediction is
recorded as MET, and the concentration is nevertheless reported as adverse-leaning.

Entropy at n = 20 is downward-biased; the two orphan sets are the same size, so the comparison
is fair, and the raw plug-in entropy is reported with the bias named rather than corrected.

## G8 — order of computation

`analyse_gauge.py` computes and writes the **VOID determination first**, into `void.json`,
before any verdict-bearing quantity is written; the verdict step refuses to run if
`void.json` is absent. Same mechanical discipline as the polarity study's power-before-p.
