# GAUGE TEST RESULTS — the gauge reading of `Circumstances` is DEAD

Run 2026-08-20 per `GAUGE_TEST_PREREG.md` (FROZEN 2026-08-20, before any arm was run).
Operationalisations the prereg left open were pinned in `gaugetest/EXECUTION_NOTE.md`
**before** the panel was invoked; they are listed in §7.

**3 arms × 248 items × 3 model families = 2,232 judgments, 0 request failures.
Spend $0.2495 of the $0.40 cap.**

## Headline

| stake | staked band | measured | verdict |
|---|---|---|---|
| **VOID gate** (evaluated first) | VOID if `pC − pA` not significantly above zero | `pC − pA` = **+3.8 pp**, one-sided p = **0.0207** | **NOT VOID** — the instrument resolves |
| **PRIMARY** | GAUGE CONFIRMED if `pB − pA` n.s. **and** `pB − pA < (pC − pA)/2` | `pB − pA` = **+4.2 pp**, p = **0.0129**; `(pC − pA)/2` = 1.9 pp | **NOT GAUGE — K-G1 FIRES** |
| **SECONDARY** Structure | orphans concentrate on `Manner` | **`Manner` 15/20 = 75%**, entropy 1.192 bits | **PREDICTION MET** |
| **SECONDARY** Circumstances | orphans scatter, or pile into `Facts` without block-coherence | **`Facts` 14/20 = 70%**, entropy 1.557 bits; corpus-wide its freed votes scatter over 8 kinds | **PREDICTION MET** |
| **K-G2** | fires if Circumstances's orphans concentrate coherently the way Structure's do | H 1.557 > 1.192 and top-share 70% < 75%; top destination is `Facts` | **DOES NOT FIRE** |

**One sentence:** removing `Circumstances` from the offered labels changed how the other ten
were read **at least as much** as removing `Structure` did — `pB` (6.1%) is if anything above
`pC` (5.7%), and the two are statistically indistinguishable — so `Circumstances` is not the
plane's labelling freedom, and **the evidence-driven "ten-plane" shape dies with it.**

## §0 The VOID determination, stated before the verdict — and how it was enforced

The prereg requires the control to be evaluated first. This was enforced mechanically, not by
intention: `analyse_gauge.py --stage void` **opens only `judgments_A.jsonl` and
`judgments_C.jsonl`**, computes `pA`, `pC` and the control test, and writes `void.json`. The
verdict stage refuses to run if `void.json` is absent, and it is the first stage that opens
arm B at all. `void.json` is on disk with a timestamp earlier than `gauge_results.json`.

**Determination: NOT VOID.**

- statistical: `pC` = 12/212 = 5.66% against `pA` = 4/212 = 1.89%; pooled one-sided
  z = 2.039, **p = 0.0207**; paired McNemar exact b = 9, c = 1, **p = 0.0107**. Removing a
  genuine content kind costs measurably more than re-running the same prompt.
- protocol: parse-failure rates 0.54% (A) / 0.27% (B) / 0.27% (C) against the 5% VOID
  threshold; all 744 (item, model) cells present in every arm; zero request failures.

**Said at full volume, because it bounds everything below: the control cleared its gate by
exactly one item.** `bands.json`, written from arm A alone while arm B was still in flight and
arm C had not started, records that 11 of 212 was the minimum count that would be significant
against `pA`. The control landed on 12. §3 is the honest accounting of what that fragility
does and does not survive.

## §1 The primary — perturbation over the untouched 212

Population: the items whose ORIGINAL 11-way BASE modal was neither `Circumstances` nor
`Structure`, identical in all three arms. **N = 212** (248 − 15 with no original modal −
9 with modal `Circumstances` − 12 with modal `Structure`). Original modals were read off the
existing BASE judgments, not re-derived.

| arm | label set | perturbed / 212 | fraction |
|---|---|---|---|
| **A** | full 11 + Record (re-run — the noise floor) | 4 | **1.89%** |
| **B** | 10 + Record, **`Circumstances` removed** | 13 | **6.13%** |
| **C** | 10 + Record, **`Structure` removed** (matched control) | 12 | **5.66%** |

| comparison | diff | z | p (one-sided) | p (two-sided) | McNemar exact |
|---|---|---|---|---|---|
| **C − A** (control) | +3.77 pp | 2.039 | **0.0207** | 0.0415 | b=9, c=1, p=0.0107 |
| **B − A** (treatment) | +4.25 pp | 2.228 | **0.0129** | 0.0259 | b=11, c=2, p=0.0112 |
| **B − C** (head to head) | +0.47 pp | 0.206 | 0.418 | 0.837 | b=8, c=7, p=0.50 |

95% CI on `pB − pA`: **+0.5 to +8.0 pp**. On `pC − pA`: +0.2 to +7.4 pp.

## §2 The verdict, read off the frozen bands

The prereg's **NOT GAUGE** band is a conjunction, and both halves are satisfied:

1. `pB − pA` **significantly above zero**: p = 0.0129 < 0.05. ✅
2. `pB − pA ≥ (pC − pA)/2`: **4.25 pp ≥ 1.89 pp**. ✅

So the frozen text applies verbatim: *"Its removal perturbs the others like a real kind's does.
**This kills the gauge reading and the ten-plane shape with it.**"*

**VERDICT: NOT GAUGE. K-G1 FIRES.**

The band only required B to cost at least *half* of what C costs. It cost **more** — 13 moved
items against 12 — though the two are indistinguishable (p = 0.84 two-sided). The reading under
test predicted `pB ≈ pA ≪ pC`. What the instrument returned is **`pB ≈ pC ≫ pA`**.

Gauge, operationally, means removing the direction does not change the content. It changed it.

## §3 Robustness — where this is fragile, where it is firm

All of §3 is **POST-HOC** except the first row, which was pinned in `EXECUTION_NOTE` G3 before
the panel ran. Nothing here displaces §§1–2; it exists so the reader can see what the verdict
rests on. Full numbers in `gaugetest/robustness.json`.

The primary's arithmetic is 13 against 12 against 4 events. That is thin, and one pre-pinned
sensitivity does not resolve at all:

| cut | A | B | C | B vs A | C vs A |
|---|---|---|---|---|---|
| **PRIMARY** (arm-tie = perturbed; pinned in advance) | 1.89% | 6.13% | 5.66% | **p = 0.0129** | **p = 0.0207** |
| **pinned sensitivity** — arm ties dropped pairwise | 1.45% | 3.86% | 2.91% | p = 0.063 | p = 0.077 |
| post-hoc — a tie still containing the original label is not a move | 1.42% | 3.77% | 2.83% | p = 0.063 | p = 0.156 |
| **post-hoc — VOTE level**, each vote paired to the SAME model's original vote (n ≈ 633) | 2.85% | **9.62%** | **8.37%** | **p = 3.2e-7** | **p = 9.8e-6** |
| post-hoc — STRICT items (no original vote for EITHER removed kind), modal, n = 201 | 1.00% | 4.98% | 5.47% | p = 0.0095 | p = 0.0056 |
| post-hoc — STRICT items, vote level (n ≈ 600) | 2.67% | 8.15% | 7.49% | **p = 1.4e-5** | **p = 7.3e-5** |

Three things to take from that table, and the second is adverse:

1. **Every cut preserves the ordering B ≥ C ≫ A**, and in no cut is B below C by more than
   noise. The finding that kills the gauge reading is the one quantity that is stable.
2. **The modal-level instrument is underpowered, and on the tie-dropping sensitivity the
   control fails** (p = 0.077 ≥ 0.05). Read through that sensitivity alone, this run would be
   **VOID**, not NOT-GAUGE. It is reported here as plainly as the verdict, per discipline rule
   7. The reason it is not the verdict is that it is a sensitivity and the primary tie rule was
   pinned as primary before any data existed — not because it is inconvenient.
3. **The vote-level analysis is the well-powered one and it is decisive.** Pairing each of the
   ~633 individual (item, model) votes against the *same model's* original vote triples the
   sample and removes the modal step entirely: the noise floor is 2.85%, removing
   `Circumstances` moves 9.62% of votes and removing `Structure` moves 8.37%, at p = 3e-7 and
   p = 1e-5. B vs C: p = 0.44, indistinguishable. This is post-hoc and is labelled so; it
   changes no verdict, and it is the reason the fragility in row 2 reads as *underpowered*
   rather than *contradictory* — every point estimate in every cut points the same way.

**The mechanism check that matters most.** An obvious objection: the untouched population is
defined by *modal*, so an item could still carry a minority vote for the removed kind, and
"perturbation" would just be that vote being displaced. Measured: 5 of the 212 carry a minority
`Circumstances` vote and 6 carry a minority `Structure` vote. Dropping all 11 leaves a strict
subpopulation of 201 items that never used either removed label at all, and the effect **grows**
(B 4.98%, C 5.47%, A 1.00%; vote level p = 1.4e-5 and 7.3e-5). The reorganisation is not
displaced votes. Removing `Circumstances` changes how the panel reads changes that never had
anything to do with `Circumstances`.

**A limitation arm A does not cover.** Arm A controls for re-running the same prompt; it does
not control for *editing the prompt at all*. Five of the 13 B-moves and 12 C-moves are the same
items (`axiomatic-policy-03`, `axiomatic-policy-04`, `axiomatic-config-02`,
`testimonial-config-03`, `epistemic-process-02`), which is what generic edit-sensitivity would
look like. This does not weaken the verdict — arm C is the correct comparator for arm B and the
prereg built it for exactly this reason — but a future design wanting to separate "removing
*this* kind" from "removing *a* kind" needs a third removal arm, or a null edit that changes the
prompt without removing anything.

## §4 The secondary — where the orphans go

Primary population is the prereg's: the removed kind's **authored** items, 20 each. Destination
is that arm's modal; `TIE` is its own category. Entropy is Shannon, in bits, plug-in (and so
downward-biased at n = 20 — but equally for both, since the two sets are the same size).

**Arm C — `Structure` removed (n = 20 authored)**

| destination | n |
|---|---|
| `Manner` | **15** |
| `Rules` | 2 |
| `Process` | 2 |
| `TIE` | 1 |

entropy **1.192 bits** (0.344 of log2 11); top share **75%**.
True-orphan sensitivity (items whose ORIGINAL modal *was* `Structure`, n = 12): `Manner` 9,
`Facts` 2, `TIE` 1 — entropy **1.041 bits**.

**Arm B — `Circumstances` removed (n = 20 authored)**

| destination | n |
|---|---|
| `Facts` | **14** |
| `TIE` | 2 |
| `Record` | 1 |
| `Identity` | 1 |
| `Process` | 1 |
| `Manner` | 1 |

entropy **1.557 bits** (0.450 of log2 11); top share **70%**.
True-orphan sensitivity (ORIGINAL modal *was* `Circumstances`, n = 9): `Facts` 6, `Identity` 1,
`Manner` 1, `TIE` 1 — entropy **1.447 bits**.

**Both staked predictions are MET.** `Structure`'s orphans concentrate on `Manner`, its own
block's surface, exactly as the block-absorption model predicts and exactly reproducing
`TWO_WAY_READING.md` §2. `Circumstances`'s pile into `Facts` — the cross-block destination the
prereg named in advance — with visibly higher entropy and a longer tail.

**K-G2 does NOT fire.** Its pinned rule (`EXECUTION_NOTE` G7b) needed `H(B) ≤ H(C)` **and**
`top-share(B) ≥ top-share(C)`; measured 1.557 > 1.192 and 70% < 75%. Both clauses fail, and the
top destination is `Facts`, which the prereg had already named as the incoherent sink. So the
secondary is clean: `Circumstances` does **not** behave like a content kind under removal in
*where its items go*.

**A better-powered version of the same question, post-hoc.** At the vote level over all 248
items, where did the removed kind's freed votes land?

| removed | votes freed | biggest gainer | share of freed | kinds gaining |
|---|---|---|---|---|
| `Structure` (arm C) | 37 | **`Manner` +24** | **65%** | 6 |
| `Circumstances` (arm B) | 30 | `Process` +11 | **37%** | 8 |

`Structure`'s mass has one home. `Circumstances`'s mass splits across `Process` +11,
`Identity` +8, `Record` +6, `Facts` +4, `Premises` +3, `Model` +3, `Priorities` +2 — and
`Manner` *loses* 6. That is the scatter the prereg staked, seen at three times the resolution.

**So the two halves of this test disagree about `Circumstances`, and both readings are real.**
It has no natural home in the content plane (secondary), and its removal nevertheless costs
the plane as much as a content kind's removal does (primary). Those are not contradictory:
a label with no single successor can still be doing work — its absence forces a *diffuse*
reorganisation, which is precisely the pattern of the primary. What dies is the inference from
"unlike the other ten" to "content-free".

One incidental observation, offered as an observation only: with `Circumstances` gone,
`gemma-3-27b-it` invented a twelfth label — it answered **`Scope`** on `structural-policy-03`
("the change alters the domain to which the rules apply"). One vote out of 744. Not evidence,
and not counted as anything; recorded because it is the sort of thing that should be in the
record rather than trimmed from it.

## §5 Kills

- **K-G1 — FIRED.** The labelling-freedom reading of `Circumstances` is dead, and with it the
  evidence-driven "ten-plane" shape. Recorded and marked. `basePlane_card = 11` is a theorem
  and was never at risk (see §8).
- **K-G2 — did not fire.** `Circumstances`'s orphans do not concentrate the way `Structure`'s
  do, on the pinned rule and on the better-powered vote-level version of it.

**What survives untouched.** The four flags that motivated the reading are measurements and
none of them is refuted here: `assertsContent = false`, disposition `outOfScope`, the
cross-block confusion leak to `Facts`, and the 85–94% zero polarity. This test refutes one
*explanation* of those flags. `Circumstances` remains the anomalous kind — this run adds a
fifth flag to the pile (its orphans have no home) and simultaneously removes the tidiest story
anyone had for why.

## §6 Protocol and spend

| arm | rows | (item, model) cells | parse failures | rate | arm-ties in the 212 | off-vocabulary |
|---|---|---|---|---|---|---|
| A | 744 | 744 | 4 | 0.54% | 1 | — |
| B | 744 | 744 | 2 | 0.27% | 5 | `Scope` ×1 |
| C | 744 | 744 | 2 | 0.27% | 6 | — |

The prereg's "panel protocol must match the existing BASE convention exactly or the run is
VOID" was discharged **in code**: the runner asserts, for all 248 items before any request is
sent, that the arm-A prompt is byte-identical to `plane_annotate.prompt_for(item, "BASE")`, and
aborts otherwise. Arms B and C differ from it in exactly three places — the count word
"Twelve"→"Eleven", the removed kind's one line in the offered-label block, and its name in the
answer-format enumeration — and the runner asserts that too. `BOUNDARY_NOTES` names only
Confidence/Facts and Model/Facts, so it is identical in all three arms and introduces no
asymmetry between the treatment and its control.

Independent validation of the modal convention: recomputing the original BASE modals for the
40 authored `Structure`/`Circumstances` items reproduces `TWO_WAY_READING.md` §2 cell for cell
(Structure → Manner 7, Facts 0, own 9; Circumstances → Facts 9, Manner 1, own 7, Identity 1).

**Spend: $0.0843 (A) + $0.0833 (B) + $0.0819 (C) = $0.2495 of the $0.40 cap.** No cap event.
Zero request failures across 2,232 calls.

## §7 Deviations, all pinned before the panel ran

Written into `gaugetest/EXECUTION_NOTE.md` before any arm was invoked (G1–G8 there):

1. **Original modal (G1)** — plurality over parsed BASE votes, tie for top → no modal, the
   convention of `polarity/build_corpus.py`. 15 of 248 items have no original modal.
2. **Untouched population (G2)** — items with a *defined* original modal that is neither
   removed kind. Items with no original modal have nothing to be perturbed from and are
   excluded from every arm, keeping the set identical across arms. N = 212.
3. **Arm ties (G3)** — an arm-modal tie counts as PERTURBED in the primary, because dropping
   tie items per arm would make the denominators differ. The tie-dropped sensitivity was
   pinned at the same time and is reported in §3; **it does not resolve, and that is stated in
   §3 as plainly as the verdict.**
4. **One-sided tests (G4)** — "significantly above zero" read as one-sided, α = 0.05, pooled
   two-proportion z. Two-sided p and McNemar exact reported beside every one.
5. **Secondary population (G5)** — the prereg's own numbers ("20 Circumstances, 20 Structure")
   identify the AUTHORED-target set, so that is primary; the modal-defined true-orphan set is
   reported beside it.
6. **A confound in the prereg's secondary (G5b)**, found from already-published data before
   any arm output existed: 9 of the 20 authored `Circumstances` items **already** read `Facts`
   with `Circumstances` on offer, so "piles into Facts" is partly true before the treatment.
   This is why the true-orphan sensitivity and the vote-level redistribution are reported —
   they are the populations that actually lose a label, and both agree with the primary
   secondary.
7. **K-G2's reading rule (G7b)** — fixed while the arms were in flight and before any judgment
   file had been opened.
8. **Order of computation (G8)** — `void.json` written from arms A and C only; the verdict
   stage refuses without it and is the first code that reads arm B.
9. **§3's rows 3–6 are POST-HOC** and are labelled as such where they appear. They change no
   verdict.
10. **The power curve in `power_curve.json`** was computed before any arm output was read; at
    n = 212 and a 2% base rate the design has 80% power against a true perturbation of ~7%.

## §8 Scope fence — reproduced verbatim from the prereg

> A pass shows the panel's readings of the other ten are insensitive to whether Circumstances
> is offered. That is evidence that Circumstances carries no content THE PANEL USES. It is NOT
> a proof that `instanceToken` is not a site (`basePlane_card = 11` is a theorem and is
> untouched), NOT a claim about physics, gauge fields or general covariance, and NOT a licence
> to renumber the taxonomy. The most it licenses is a stance claim about a measured asymmetry
> among the eleven, with this test named as its basis.

It was not a pass, so nothing is licensed. The fence still binds in the other direction and
should be said out loud: **a fail is equally not a claim about physics, gauge fields or general
covariance**, and it is not a result about human annotators — this is a three-model panel on an
authored corpus, and the human ceiling remains owed. What the fail licenses is exactly one
thing: the gauge/labelling-freedom reading of `Circumstances`, and the "ten-plane" shape that
rested on it, are off the table.

## Artifacts

`scratchpad/gaugetest/` — `EXECUTION_NOTE.md`, `RESUME.md`, `gauge_annotate.py` (runner),
`run_all.sh`, `originals.py` + `originals.json`, `analyse_gauge.py`, `void.json` (written
first), `gauge_results.json`, `robustness.py` + `robustness.json`, `bands.json`,
`power_curve.json`, `render_tables.py`, `judgments_{A,B,C}.jsonl` (744 rows each),
`spend_*.json`, `run_all.log`, `DONE_{A,B,C,ALL}`.
