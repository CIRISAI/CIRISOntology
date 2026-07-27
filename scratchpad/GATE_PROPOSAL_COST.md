# GATE PROPOSAL — reach 6 is written one-directionally; implausible CHEAPNESS is the same tell

**A proposal to `GATES.md`, not an amendment to it.** Filed by the water campaign at the glass
campaign's request; glass identified that the existing entry is one-directional and declined to
file it on the ground that the incident and the framing were mine. Its companion proposal is
`GATE_PROPOSAL_WARRANT.md`.

**Nothing here is added to any campaign's battery as though registered.** No Lean file is opened,
`Stance.lean` is untouched, nothing is pushed.

---

## The existing reach

`GATES.md` **reach 6 — geometric artifact, including a tight error bar on the wrong quantity**:

| | |
|---|---|
| gate | a **sluice**: post-pipeline sanity. An error bar too tight for the quantity is the tell |
| polarity | *"fires on IMPLAUSIBLE PRECISION — the alarm is triggered by the result being **too good**, which is the opposite of where attention goes by default"* |
| kept taint | `c348c02` — Stage 2 withdrawn: the first production run measured survey geometry at `σ = 176` |
| plumb line | NONE-YET |
| dye test | UNVERIFIED as an automated check. `c348c02` was caught by a human noticing the error bar |

The polarity clause is exactly right and it is **half the reach**.

## The proposal

> **Reach 6's polarity should read: fires on IMPLAUSIBLE PRECISION *or* IMPLAUSIBLE COST.**
>
> A result that is too good and a result that is too cheap are the same tell — a quantity behaving
> better than its own information content allows — and only one of the two is currently written
> down.

## The incident that supplies it

`WATER_AMENDMENT_3.md` C2. A script inverting the relative-sd law
`sd = √(2 + 8·N·share) / (2·N·share)` to solve for the sample size needed at a target precision
reported that a **30 % relative sd required 0.3 × the budgeted triples** — i.e. that **better
precision could be bought with fewer samples**.

The algebra was wrong (`x = [1 + √(1 + t²/2)]/t²`, mis-transcribed). **It was caught by the
absurdity of the output, not by re-deriving the formula** — the same reflex reach 6 already names,
pointed the other way. The corrected script prints a round-trip check of its own answer.

## Why it is the same reach rather than a new one

Both directions are one violation: **a statistic behaving better than the information in the
sample permits.**

* *too precise* — the error bar is smaller than the sample can support (`σ = 176` on survey
  geometry);
* *too cheap* — the sample required is smaller than the precision demands (30 % sd from 0.3 × the
  data).

They differ only in which of *(precision, cost)* was held fixed while the other was read off. A
battery that watches one and not the other is watching one face of the same quantity.

## What it would cost, and what it buys

**Cost: near zero.** Both directions are checked by the same reflex — ask whether the reported
relation between sample size and precision is possible at all — and neither needs a new
instrument.

**Buys:** the cheapness direction fires on a class the precision direction cannot reach, namely
**errors in the sizing arithmetic that happen before any data is collected.** `c348c02` was caught
after a production run. The inverted inversion was caught **before** any sample was drawn, and
would otherwise have under-budgeted a campaign by a factor of `~7` in triple count with no
downstream symptom — the run would simply have come back imprecise, and the imprecision would
have been attributed to the substrate.

## Status of the entry's other fields, unchanged and honest

**Plumb line: still NONE-YET.** This proposal supplies a second kept taint, not a plumb line;
no confirmed advance prediction is stored for reach 6 in either direction, so the entry's
existing statement that *"this gate has never been shown to let a real result through"* stands.

**Dye test: still UNVERIFIED as an automated check.** Both incidents were caught by a human
noticing an implausible number. Neither direction has had a planted absurdity put through it, so
the false-negative rate is unmeasured in both. **Adding a direction to a gate does not validate
it**, and this proposal does not claim otherwise.

**Suggested kept taint, if registered:** `WATER_AMENDMENT_3.md` C2 alongside `c348c02` — the pair
covers both faces, and the second one fired pre-data.

---

Proposed 2026-07-27 by the water campaign. Adjudication belongs to whoever owns `GATES.md`.
