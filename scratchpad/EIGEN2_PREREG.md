# PRE-REGISTRATION — the eigen-alignment experiment, version 2

**Drafted 2026-08-19. Revised 2026-08-19 after adversarial referee round (§23).
FROZEN 2026-08-19 (§24).** It governs a
run on a corpus no embedder has ever seen:
`/home/emoore/CIRISOntology/scratchpad/plane_corpus/eigen2/eigen2_corpus.jsonl`
(474 items, sha256 `cf26b604d8aeeebda906ad2c0729b1b71df5d37a55c25faf770447cf92be7c40`).

It supersedes nothing. `EIGEN_ALIGNMENT_PREREG.md` (v1, frozen 2026-08-18) and
`EIGEN_ALIGNMENT_RESULTS.md` (v1, run 2026-08-19) stand as written, including their fired
kills. Where this document reuses v1 machinery it cites the v1 section by number and says
what changed. Where it departs, it says why, with the measurement that forced the departure.

**The one-line reason v2 exists.** v1's instrument failed its own placebo — the change vector
Δ = e(after) − e(before) read *less* kind structure than the unchanged documents, in 0 of 200
splits (v1 §3, K1c). The steward's ruling on that result is the organising principle of this
document: **a meter that fails its own placebo renders no world-verdict in either direction.**
v1 therefore produced no geometry-null and no geometry-support (v1 §13). v2's single most
important structural change is that the placebo is promoted from a kill on an interpretation
to a **VOID condition on the whole run, evaluated before any verdict is read** (§15-VG1).

**What the referee round changed.** 8 CRITICAL and 20 MAJOR defects were raised against the
first draft; every one is dispositioned in §23. Four of them were structural: the split
procedure could not produce a single usable split (§7-N2, now a constructive Euler-circuit
2-colouring); the primary embedder resolved to Qwen while every staked number was priced from
bge; the calibration those numbers came from was a **12-class / rank(B) = 11** measurement
while v2 runs 11-class / rank(B) = 10; and the power surface was read one doubling off in n.
All four are fixed here against re-derived artifacts, and **every staked band, margin and
ladder rung in this revision is priced from `out/phase0_k11_reprice.json` — the calibration
re-run on v2's own geometry.**

**Three measurements were made for this revision that neither the draft nor the critique had**,
all on spent or synthetic data at zero API cost: the split construction was implemented and
its balance asserted over 200 draws (§7.2); the gauge's missing scale-0 rows were computed so
the power surface can be read as an excess at all (§8, §9.5); and the **instruction ablation
was re-priced on v2's geometry** (§3.3b). The last one is the most uncomfortable number in the
document: on the calibration corpus, the author-written instruction is what moves this
instrument across §13's boundary from "the reading is mostly context" (ψ = 0.158) to "the
change carries a substantial minority" (ψ = 0.256). The bare arm still passes every conjunct
on its own, so the construction is not a prompt artifact — but the headline's *shape* is
partly ours, and §21 rung 5 now makes the ablation a promotion condition.

---

## 0. Freeze declaration — what has been inspected, and what has not

### 0.1 The bright line on the new corpus

**No text of `eigen2_corpus.jsonl` has been embedded, annotated, or read as prose by any
model or by the author of this document.** What was computed on it, exhaustively:

| what was computed | why it does not contaminate |
|---|---|
| row count (474), field names (11 fields), key-set uniformity (1 distinct key set) | schema |
| `kind_target` counts (11 classes), `domain` counts (12), `difficulty` counts, `part` (all `E2`) | label tallies — v1 §0.2's admissible class |
| `batch` id range (0–39), per-batch sizes (11–12), kind × batch cross-tab, kind × domain cross-tab, **kind × difficulty cross-tab**, χ² on the first two | design verification — the whole point of the rebuild is that these tables are flat |
| `ambiguous_with` non-null count (120) and its target distribution | label tally |
| distinct-`before` and distinct-`after` counts (474 / 474) | de-duplication check |
| character length of the fields of **one** row | a length statistic |
| **the split feasibility simulation of §7-N2** (labels only: kind and batch ids) | combinatorics on the label columns; no text touched |
| **NEW, added this revision: three mechanical trigger marginals on `before` texts** (§12) — the *corpus-wide count* of items containing a modal, a standalone numeral, and an `is`/`are`/`does` form, and the size of their three-way intersection | see the guard below |

**The guard on the new admission.** §12's positive control cannot state whether its item set
is reachable without knowing how many items its three mutation families trigger on, and a
protocol that VOIDs for want of a two-second regex is worse than the disclosure. What was
computed is **kind-blind by construction**: three corpus-wide integers and their
intersection, never crossed with `kind_target`, `domain`, `batch` or `difficulty`, and no item
text was printed or read. The measured values are in §12. A marginal that is not crossed with
the label carries no information about the label↔text relation, which is the only relation
this experiment measures.

**Not computed, and deliberately left for after the freeze:** changed-span lengths per kind
(v1 §2.1b's 87× spread is a known hazard; N1b prices it unconditionally, and §11-D-S1 now
converts it into a post-freeze design measurement with its meaning fixed in advance); any
TF-IDF or bag-of-words proxy on the new text; any embedding; any panel annotation; any reading
of an item body.

**Two consequences of that abstention, stated now.** (i) v1 could stake a forward prediction
against a measured text-level power proxy (v1 §9.1). v2 cannot, and instead stakes its
forward prediction against the phase-0 calibration re-priced on v2's geometry and the
synthetic power surface (§9.5), which is weaker evidence and is labelled so. (ii) The nuisance
structure of the new corpus is *designed* rather than *measured*; §11 turns each design claim
into a post-freeze measurement with its meaning fixed here.

### 0.2 What was inspected on already-spent artifacts, and is admissible

Corpus A is **spent**: v1 read it end to end. Phase 0 (the construction bake-off) ran on
Corpus A precisely because it was already burned, and is **instrument calibration with no
taxonomy verdict attached** (`out/phase0_bakeoff.json` `_meta.label`). Its numbers are used
here for **selection and for pricing the bands** — and never as evidence about the taxonomy.
The full phase-0 table is reproduced in §3.2 with that label attached, including the caveat
that every phase-0 number is measured on a corpus whose kind is 6/6 nested in generation
batch (v1 §2.1a) and may therefore be **batch-inflated**.

Also inspected: v1's synthetic power surface (`out/power_surface.json`, no corpus text, no
embedding), v1's gauge output, v1's results document in full, and the two artifacts produced
by the referee round itself:

* **`out/phase0_freeze_snapshot.json`** — the phase-0 cells frozen at extraction time, immune
  to the shared-artifact append problem that made mid-run reads unreliable;
* **`out/phase0_k11_reprice.json`** — the C1 cells **re-run with `testimonial` dropped**, i.e.
  on an 11-class partition at `rank(B) = 10`, n = 227. This is v2's geometry and it is the
  anchor for every number staked below. It consumed no API spend (all vectors cached) and no
  E2 text.

### 0.3 Freeze scope

Everything in §§1–22 is frozen at the moment the steward signs §22. §23 is a record of the
referee round and is frozen with the rest. Any deviation after the signature is an amendment
with a timestamp, written **before** the deviating computation runs (`epistemology.md`
rule 1), and appended as a numbered section, never edited in place.

---

## 1. The claims under test

### 1.1 P1a — alignment (the eigen-bridge, restated for v2's instrument)

On a change-describing corpus rendered by the C1 construction (§3.1), the principal content
directions of the embedding cloud align with the 11 kinds' one-vs-rest discriminator
directions beyond what a label permutation, a span-stratified label permutation, a
difficulty-stratified label permutation, and a rival 11-way partition produce.

### 1.2 P1d — change-attribution (NEW, and the load-bearing half)

The alignment in P1a is carried by **the change**, not by the surrounding text: the C1
rendering reads strictly more kind-alignment than the **context-only placebo** rendering
C1P, which is identical in every character except that the changed slot is filled with the
*unchanged* text (§3.1).

**P1a without P1d is not the eigen-bridge.** v1's whole lesson is that a construction can
read kind structure while reading none of the change. This is why §15-VG1 makes P1d's floor a
VOID condition rather than a caveat, and why §9.3's verdict table names every combination.

### 1.3 P3 — the site claim (secondary, EXPLORATORY, pre-registered so it cannot be found later)

The context-only rendering C1P may itself carry kind. If it does, that is **not** support for
P1 — but it is a coherent, theory-adjacent statement (the kinds are the exact image of a
**site** model, `Core/Generator.lean`), and pre-registering it now is the only way to keep it
from being discovered post hoc in the placebo arm and promoted. It is staked in §10, marked
EXPLORATORY, and is **not promotable from this corpus at any strength**, because we authored
the items with the taxonomy in hand and chose the sites (v1 §19-D6).

**P3 is expected to pass, and that expectation is recorded now so its passing cannot be
narrated as a discovery.** On Corpus A the context-only cloud already cleared its own
permutation null decisively — v1 §3's auditor's supplementary computation measured
Ω_before(11) = 0.13374 against an N1 null median of 0.10827 at p = 0.001996, **0 of 500
permutations** — and the phase-0 C1P placebo excess on v2's geometry is +0.1010 (primary) and
+0.0570 (witness). A P3 pass on E2 is therefore the *predicted* outcome, not news.

### 1.4 Record (the 12th) is EXCLUDED BY CORPUS, and what that costs

`eigen2_corpus.jsonl` contains **11 kinds. There are no `testimonial` (Record) items.**
Verified: the `kind_target` vocabulary is exactly {axiomatic, axiotic, contingent, deontic,
empirical, epistemic, nomological, ontological, pragmatic, procedural, structural}.

This is consistent with the type — Record is the one **frame-relation**, not an artifact-local
kind, and a corpus of artifact pairs cannot exercise it — but the consequences are binding and
are stated before the run:

* **v1's P2-neg and P2-pos have no v2 arm.** They are not "not detected" here; they are **not
  asked**. The relation-typing claim stays exactly where v1 left it: both legs VOID by their
  own vacuity gates (v1 §6), unfalsifiable-at-null, neither supported nor refuted.
* **K3 and K4 cannot fire in v2, and their non-firing carries no weight whatsoever.**
* **The counting identity moves.** With K = 11 classes, the 11 one-vs-rest centroid contrasts
  obey one exact linear relation and span **exactly 10** dimensions (v1 §5.1, same algebra,
  one fewer class). So `rank(B) = 10`, Ω normalizes by 1/10, and **every Ω in the results file
  must be quoted with `rank(B) = 10` beside it**. Any sentence of the form "the 11 kinds'
  11-dimensional subspace" is forbidden; the object is the **11-class between-class subspace,
  dimension 10**.
* **The published prediction's integers are re-based, and this is the record of it.**
  `LEAN2_CONFRONTATION.md` line 70 stakes Prediction 1 as *"the 11 kinds' one-vs-rest
  discriminator directions — **not 7, not 13**"*, integers set when the taxonomy under test
  was 12 classes at rank 11. v2 tests **rank 10**, so the bracketing integers move to
  **"not 6, not 13"** and Tier 2's band moves to `R_kind ∈ {9, 10, 11}` (§9.4). This is a
  re-basing of the same claim onto one fewer class, not a weakening, and §16-K1's blast radius
  is restricted to **Prediction 1 only** — Prediction 2 (Record) correctly has no v2 arm.
* The primary principal-subspace size stays **k = 11** (§6), for continuity with v1's staked
  primary and because the claim is that the kinds sit among the *leading* directions, not that
  they exhaust exactly ten of them. **Disclosed inconsistency, with its direction:** Ω(11)
  sums one more PC than the kind subspace has dimensions, which biases it **upward** relative
  to the rank-matched Ω(10), while §7.1 makes rank-matching mandatory for the rivals. Ω(10) is
  therefore reported as a **rank-matched co-primary** beside every Ω(11), and the verdict is
  read from Ω(11) only if the two land in the same §9.3 cell; if they do not, the finding is
  published as **k-DEPENDENT** and is not promoted. k = 10 may not be promoted alone.

### 1.5 What v2 cannot decide, stated now

Whether the eleven are the *right* eleven; whether embedding geometry has any authority over a
taxonomy's correctness; anything at all about Record; anything about wild (non-authored)
change streams — the corpus is ours, written by us, with the taxonomy in hand (§19-D1). A
result here is a statement about **this construction, this corpus, these two embedders**.

---

## 2. Corpus — frozen

### 2.1 The one corpus

| role | path | rows | label field |
|---|---|---|---|
| **Corpus E2** (authored, interleaved, balanced) | `/home/emoore/CIRISOntology/scratchpad/plane_corpus/eigen2/eigen2_corpus.jsonl` | **474** | `kind_target` ∈ 11 internal names |

sha256 `cf26b604d8aeeebda906ad2c0729b1b71df5d37a55c25faf770447cf92be7c40`, 813,933 bytes.
Fields: `id, batch, part, kind_target, domain, difficulty, ambiguous_with, before, after,
variation_site, author_note`. One distinct key set across all 474 rows. 474 distinct `before`
texts and 474 distinct `after` texts (no artifact reuse).

**Class counts, verified:** axiomatic 39, axiotic 40, contingent 40, deontic 59, empirical 59,
epistemic 37, nomological 40, ontological 40, pragmatic 40, procedural 40, structural 40.
Internal→plain map, verbatim from `Core/WrongKind.lean` lines 167–178 (the `def
WrongKind.plain` line is 166): axiotic→Priorities, deontic→Rules, pragmatic→Manner,
ontological→Identity, epistemic→Confidence, empirical→Facts, contingent→Circumstances,
procedural→Process, nomological→Model, structural→Structure, axiomatic→Premises.

**Domains (12), verified:** config 40, registry 40, minutes 40, manual 40, catalogue 40,
handbook 40, log 40, policy 39, process 39, bulletin 39, notice 39, report 38.

### 2.1b Difficulty is NOT flat across kind, and the design owns it

**Measured from the labels, and reported here because the first draft reported only the
354/120 marginal:** hard items per kind are **10 for every kind except `empirical`, which
carries 20**. `ambiguous_with` is non-null on exactly the 120 hard items, naming the kind each
was written to sit near: **empirical 41, deontic 35**, axiotic 15, axiomatic 10, pragmatic 10,
structural 7, procedural 2.

So the two largest classes (`deontic` 59, `empirical` 59) are also the designed **attractors**,
and `empirical` additionally carries twice everyone else's hard items. This is a real
asymmetry in the generative structure of the corpus and the null must match it (rule 3). Three
consequences, all pre-committed:

1. **N1d, a difficulty-stratified label permutation, is added** to §7 as a reported null
   (not a required conjunct).
2. **A `clear`-only sensitivity arm (n = 354) is added** to §4, reported, never headline, with
   the pre-committed reading: if the primary and the clear-only arm land in different §9.3
   verdict cells, the finding is **DIFFICULTY-DEPENDENT** and is not promoted.
3. **`difficulty` is NOT added to the nuisance matrix `Z`**, and here is why: `Z` removes
   variance that is *not* the claim, and a hard item's difficulty is a property of how close
   its change sits to a neighbouring kind — which is part of what the taxonomy is being asked
   to resolve, not a nuisance orthogonal to it. Residualizing it out would remove the hardest
   part of the test and flatter the result. The stratified null (1) and the sensitivity arm (2)
   price the same structure without buying that flattery.

### 2.2 The interleave — the defect v1 could not fix, verified fixed

v1's deepest confound was that `kind_target` was nearly **nested in generation batch**: part_a
carried six kinds, part_b the disjoint other six, and batch was textually detectable at
**0.573 against a majority baseline of 0.484 on a 3-class (part a/b/c) problem — a lift of
1.18×** (v1 §2.1a; the baseline is quoted here every time the number is, because 0.573 read
bare looks like a far stronger confound than it is). The N1 label permutation is blind to
batch, so a pure batch effect reads as alignment. v1 answered with a batch nuisance term,
within-batch arms and V11, and conceded in §19-D9 that **no arm could be simultaneously fully
powered and fully batch-free**. Ruling 2 committed to the rebuild. This is it.

**Verified on the new corpus, from ids and labels only:**

* 40 batches, ids 0–39, **11 or 12 items each** (34 of size 12, 6 of size 11);
* the kind × batch table has cell values in **{0, 1, 2}** only — 396 ones, 39 twos, 5 zeros;
  each batch carries **10 or 11 distinct kinds** (35 batches carry 11, five carry 10);
* χ²(kind × batch) **p = 1.0000**, χ² = 18.82, dof 390;
* χ²(kind × domain) **p = 1.0000**, χ² = 22.62, dof 110.

A χ² p of exactly 1.0000 is not evidence of independence in the usual sense — it is the
signature of a table that is **more uniform than random assignment would make it**, which is
what "one per kind per batch, domains rotated" produces by construction. That is the intended
reading and it is the strongest statement available: batch and domain are not merely
uncorrelated with kind, they are **balanced against it by design**.

**And the χ² is descriptive only — it cannot serve as a gate.** The kind × batch table has a
**minimum expected cell of 0.859 and 100% of its cells below expected count 5**; at 390 dof
the χ² approximation has essentially no power and an unreliable null. The first draft reused
this same statistic as the numeric gate VG3; §11 now replaces it with a direct combinatorial
criterion that can actually fire.

**Consequence, and it is a change of sign.** On Corpus A, batch style could *manufacture*
kind alignment. On Corpus E2 it cannot: an 11-class contrast basis is orthogonal in
expectation to a 40-class balanced nuisance, so any batch-level style variance can only
**occupy principal directions that the kind subspace does not** — a power tax, not a
confound. **V11 is therefore retired.** It is replaced by the measurements of §11, whose job
is to verify the design claim rather than assume it.

### 2.3 Arms that are EXCLUDED, each with its reason

| arm | v1 role | v2 disposition |
|---|---|---|
| `part_d.jsonl` (12 items) | held-out spot check | **EXCLUDED** — Corpus A family, spent by v1, covers 3 kinds only (v1 §2.1) |
| `babel_items.jsonl` (10 items) | topic control | **EXCLUDED** — spent by v1 (0/10, v1 §7), and superseded: C1P is a **per-item** topic control on all 474 items, where Babel held topic fixed across 10. The placebo is strictly the stronger control and it is the same control |
| Corpus B / wild streams (279→227) | cross-corpus transfer | **EXCLUDED** — spent by v1, cannot kill by its own staked asymmetry (v1 §9-P1c), kind coverage measured-skewed, 43% one source. A wild arm belongs to a purpose-built wild corpus, not to this freeze |
| RATCHET (`accord_traces.jsonl`) | placebo P2 + K5 audit | **EXCLUDED** — K5 was withdrawn pre-data by the steward (v1 §21); the leg is REPORTED-BUT-UNPINNED and nothing here changes it. No RATCHET computation is part of v2 |
| `full_judgments.jsonl` frame conditions | P2-pos | **EXCLUDED** — no Record class in E2 (§1.4); the lever has nothing to move |

Excluding an arm is not a claim that it would have failed. Each is excluded because it is
spent, or because a stronger control replaces it, and saying so here prevents any of them
being run later and quoted as a confirmation.

---

## 3. Instrument — frozen

### 3.1 The construction: C1 span-in-context, ONE embedded text

Pinned verbatim to `/home/emoore/CIRISOntology/scratchpad/eigen/phase0_span.py`, sha256
`6053e2fc037445101d5010e28522bc22cf85209c7eb00f57ab757a8274212226`. No authored field
(`variation_site`, `author_note`, `kind_target`, `difficulty`, `ambiguous_with`) is read by
the construction; the only inputs are `before` and `after`.

1. **Mechanical span extraction.** `lcp_lcs(before, after)` — longest common prefix and
   longest common suffix — yields the single contiguous changed region on each side. This is
   deliberately **not** v1's `difflib` character-opcode span, which shredded edits into
   fragments (`'arteria u schoo f n ag'`).
2. **Sentence-window rendering.** `widen()` expands each region to the full sentence(s) of its
   own version that it overlaps. Sentence boundaries: `.`/`!`/`?` followed by
   whitespace-then-capital-or-quote-or-paren, plus hard newlines.
3. **One text.** `C1_TEMPLATE = 'A passage changed. Before: {b} After: {a}'` with `{b}`, `{a}`
   the two sentence windows. **One embedding per item. No subtraction anywhere.**
4. **The placebo.** `C1P = 'A passage changed. Before: {b} After: {b}'` — the identical
   template, identical prefix, identical before-window, with the after slot filled by the
   **before** window. It is character-identical to C1 except in the changed region, so its
   difference from C1 is exactly the change and nothing else.

Both C1 and C1P are embedded through the identical path, with the identical instruction
prefix where one applies. **A placebo that does not carry the instruction is not a placebo.**

### 3.2 Why C1 — the phase-0 bake-off, labelled selection-only

**Phase 0 is COMPLETE.** `out/phase0_bakeoff.json` holds **30 cells** — 5 constructions ×
3 embedder arms × 2 nuisance arms — elapsed 3,200 s, spend $0.005. The freeze-time snapshot is
`out/phase0_freeze_snapshot.json`. It ran four constructions plus a fifth on the spent
Corpus A (n = 247, v1's pinned item set, v1's 200 splits, 500 permutations), each against its
own context-only placebo, under this selection rule:

> PASS iff **(a)** p_N1(Ω(11)) ≤ 0.01 **and (b)** the sign-flip paired test on the per-split
> construction-minus-placebo difference gives p ≤ 0.05 with median > 0 **and (c)** the gap
> beats its own label-permutation floor at p_gap ≤ 0.01.

**The pinned code's own disclosure about when that rule was set, reproduced verbatim from
`run_phase0.py`'s docstring, because a prereg whose subject is rule 1 may not paraphrase it:**

> *"DISCLOSURE: (c) was added after a 3-permutation smoke run had shown the Omega and
> placebo-Omega values (which are deterministic and carry no p-value). No p-value at the run's
> permutation count had been seen when the rule was fixed."*

Criterion (c) is the gap criterion, and it is what eliminates `C1.bge.raw` and C2. The first
draft's "under a selection rule fixed before the permutation counts were seen" was literally
true and materially misleading; the disclosure above is the honest form and it stands beside
every use of the selection.

**Measured, all 30 cells, at phase-0's own geometry (K = 12, rank(B) = 11 — see the
normalization warning below):**

| cell | Ω(11) | null med | excess | placebo Ω | gap δ | p_gap | p_paired | frac_gt | p_N1 | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| **C1.qwen.res** | **0.3378** | 0.2161 | **+0.1217** | 0.3112 | **+0.02664** | 0.0020 | 1e-4 | 1.000 | 0.0020 | **PASS** |
| **C1.qwen.raw** | 0.3625 | 0.2584 | +0.1041 | 0.3343 | +0.02819 | 0.0020 | 1e-4 | 1.000 | 0.0020 | **PASS** |
| C2.qwen.res | 0.1986 | 0.1368 | +0.0619 | 0.2097 | −0.01110 | 0.8762 | 1.0 | 0.005 | 0.0020 | FAIL: placebo |
| C2.qwen.raw | 0.2174 | 0.1720 | +0.0454 | 0.2267 | −0.00922 | 0.6068 | 1.0 | 0.010 | 0.0020 | FAIL: placebo |
| C3.qwen.res | 0.0717 | 0.0699 | +0.0018 | 0.1726 | −0.10091 | 1.0 | 1.0 | 0.000 | 0.2176 | FAIL: null |
| C3.qwen.raw | 0.0738 | 0.0718 | +0.0020 | 0.1823 | −0.10846 | 0.0020 | 1.0 | 0.000 | 0.1856 | FAIL: null |
| C4.qwen.res **v1's Δ** | 0.1267 | 0.1174 | +0.0093 | 0.1726 | −0.04589 | 0.9980 | 1.0 | 0.000 | 0.0439 | FAIL: null |
| C4.qwen.raw | 0.1505 | 0.1233 | +0.0272 | 0.1823 | −0.03178 | 0.0020 | 1.0 | 0.000 | 0.0020 | FAIL: placebo |
| C5.qwen.res **Δ at sentence granularity** | 0.1187 | 0.1048 | +0.0139 | 0.2097 | −0.09099 | 1.0 | 1.0 | 0.000 | 0.0020 | FAIL: placebo |
| C5.qwen.raw | 0.1242 | 0.1093 | +0.0149 | 0.2267 | −0.10247 | 1.0 | 1.0 | 0.000 | 0.0020 | FAIL: placebo |
| **C1.bge.res** | **0.1893** | 0.1295 | **+0.0598** | 0.1849 | **+0.00437** | 0.0100 | 1e-4 | 0.855 | 0.0020 | **PASS** |
| C1.bge.raw | 0.2104 | 0.1665 | +0.0439 | 0.2062 | +0.00413 | 0.0160 | 1e-4 | 0.805 | 0.0020 | FAIL: p_gap |
| C2.bge.res | 0.1618 | 0.1009 | +0.0609 | 0.1676 | −0.00583 | 0.1198 | 1.0 | 0.080 | 0.0020 | FAIL: placebo |
| C2.bge.raw | 0.1929 | 0.1386 | +0.0543 | 0.1969 | −0.00402 | 0.0259 | 1.0 | 0.170 | 0.0020 | FAIL: placebo |
| C3.bge.res | 0.0551 | 0.0537 | +0.0015 | 0.1337 | −0.07860 | 1.0 | 1.0 | 0.000 | 0.1018 | FAIL: null |
| C3.bge.raw | 0.0552 | 0.0550 | +0.0003 | 0.1497 | −0.09440 | 0.0938 | 1.0 | 0.000 | 0.4371 | FAIL: null |
| C4.bge.res **v1's Δ, reproduced** | 0.0600 | 0.0598 | +0.0002 | 0.1337 | −0.07376 | 1.0 | 1.0 | 0.000 | 0.4651 | FAIL: null |
| C4.bge.raw | 0.0693 | 0.0641 | +0.0052 | 0.1497 | −0.08034 | 0.0160 | 1.0 | 0.000 | 0.0120 | FAIL: null |
| C5.bge.res | 0.0945 | 0.0901 | +0.0044 | 0.1676 | −0.07309 | 1.0 | 1.0 | 0.000 | 0.1277 | FAIL: null |
| C5.bge.raw | 0.1054 | 0.0951 | +0.0103 | 0.1969 | −0.09159 | 1.0 | 1.0 | 0.000 | 0.0080 | FAIL: placebo |
| **C1.qwen_noinstr.res** | **0.1928** | 0.1142 | **+0.0786** | 0.1826 | **+0.01024** | 0.0020 | 1e-4 | 0.990 | 0.0020 | **PASS** |
| C1.qwen_noinstr.raw | 0.2123 | 0.1471 | +0.0652 | 0.2031 | +0.00913 | 0.0020 | 1e-4 | 0.980 | 0.0020 | **PASS** |
| C2–C5.qwen_noinstr.{res,raw} | — | — | +0.0010…+0.0589 | — | −0.0952…−0.0062 | ≥0.0020 | 1.0 | ≤0.045 | — | all FAIL |

**What the completed table establishes.**

* **C1 is the only construction that passes, and now on all three arms rather than one.** The
  first draft could say this of bge alone. C2 (no subtraction, concatenated pair), C3
  (residualizing the after-cloud on the before-cloud), C4 (v1's Δ) and C5 (Δ at *sentence*
  granularity) fail on **every** embedder arm. `C4.bge.res` reproduces v1's headline exactly
  (0.0600 against a null of 0.0598) and reproduces v1's K1c signature at −0.0738.
* **Subtraction is the defect, and the document was also the wrong unit — both are now
  measured rather than inferred.** C5 exists precisely to separate the two ("*the control that
  separates 'subtraction cancels the site cues' from 'the document is the wrong unit'*",
  `run_phase0.py`). C5 takes v1's difference vector at **sentence** granularity — the unit fix
  without the subtraction fix — and it fails on both embedders (excess +0.0044 bge, +0.0139
  qwen, both placebo-negative). C2 removes the subtraction while keeping two embedded texts,
  and also fails. Only C1 — one embedded text, sentence granularity, no subtraction — passes.
  The first draft's claim that "subtraction is the defect, and it is not the only defect"
  rested on C1-vs-C2 alone; it now rests on the C5 control that was built to test it.
* **The substitution clause of §3.3 resolves NEGATIVE.** No construction strictly dominates C1
  on the primary embedder under the phase-0 rule: every C2–C5 qwen cell fails, and none has a
  higher excess or a positive gap. **C1 is pinned.**
* **`C1.bge.res` passed criterion (c) by one permutation out of 500** — p_gap = 0.00998 =
  (1+4)/501, four exceedances; the next attainable value, (1+5)/501 = 0.01198, fails the ≤ 0.01
  rule. **On the resolved primary this knife-edge does not exist**: `C1.qwen.res` and
  `C1.qwen.raw` both record p_gap = 0.001996, **0 of 500 exceedances**, the reporting floor.
  And on v2's own geometry the knife-edge disappears for bge too (§3.2b). The exceedance count
  is quoted beside p_gap wherever the selection is cited.

**What the table does not establish:** anything about the taxonomy. Corpus A's kind is 6/6
nested in batch (v1 §2.1a), so *both* the C1 excess and the C1P placebo excess may be
batch-style rather than kind. The bake-off is a comparison **among constructions on a common
confounded substrate** — valid for selection, worthless as evidence. §9.5 stakes exactly this
as the two-scenario forward prediction.

### 3.2b The normalization warning, and the re-priced calibration that answers it

**Every number in §3.2's table is a 12-class / `rank(B) = 11` measurement.**
`run_phase0.py` calls `run_arm(prep, labels, 12, …)` because `corpora.KINDS` includes
`testimonial`, and every cell records `rank_B = 11.0`. Since `Ω = (1/r)·‖UᵀB‖²_F`, phase 0
divides by 11 over a 12-column B while **v2 divides by 10 over an 11-column B**. Carrying
band edges, margins and ladder rungs across that change without rescaling was a defect of the
first draft (§23-C3) and it is fixed by measurement, not by argument:

**`out/phase0_k11_reprice.json` re-ran the C1 cells on Corpus A with `testimonial` items
dropped — 11 classes, `rank(B) = 10`, n = 227, the identical pipeline, 200 splits, 500
permutations, all vectors cached, zero API spend, no E2 text.** This is v2's geometry, and
**it, not §3.2's table, is the anchor for every staked number below.**

| re-priced on v2's geometry (K = 11, rank(B) = 10, n = 227) | `C1.qwen.res` **PRIMARY** | `C1.bge.res` **WITNESS** |
|---|---|---|
| Ω(11) | **0.34274** | 0.18961 |
| N1 null median | 0.21824 | 0.12666 |
| N1 null p99 | 0.23866 | 0.13998 |
| **Ω\* (excess)** | **+0.12450** | **+0.06295** |
| p_N1 | 0.001996 (0/500) | 0.001996 (0/500) |
| placebo Ω(11) | 0.31050 | 0.18250 |
| placebo excess | +0.10102 | +0.05700 |
| **δ (median of per-split diffs)** | **+0.031824** | **+0.005996** |
| δ (difference of medians) | +0.032245 | +0.007102 |
| p_paired (sign-flip) | 1.0e-4 | 1.0e-4 |
| frac_splits_gt | **1.000** | 0.915 |
| gap-null median | +0.009166 | +0.001196 |
| **gap-null p99** | **+0.018188** | +0.005068 |
| p_gap_N1 | **0.001996 (0/500)** | **0.001996 (0/500)** |
| **ψ = δ / Ω\*** | **0.2556** | 0.0952 |
| evr_top11 | 0.4292 | 0.3307 |
| d_eff | 227 | 227 |

**Three things this table changes, and they are the reason the first draft could not be
frozen.** (i) The primary's ψ is **0.256**, not the 0.073 the first draft made its organising
worry — the change carries roughly a quarter of the alignment-above-null, not a
thirteenth. (ii) The primary's δ is **0.0318**, seven times the 0.0044 the first draft priced
VG1's margin against, so the claim that "this design stakes a margin the calibration would not
have cleared" was **false on the arm that matters** and is withdrawn. (iii) On v2's geometry
`C1.bge.res` records p_gap = 0.001996, **0 of 500** — the one-permutation knife-edge of §3.2 is
an artifact of the K = 12 normalization and does not survive the re-pricing.

**The batch-inflation caveat, which binds every number in the table above.** Corpus A's kind
is 6/6 nested in generation batch and batch is textually detectable at a 1.18× lift from the
unchanged text (§2.2). Both the C1 excess and the C1P placebo excess may therefore be
batch-style rather than kind, and δ — their difference — inherits an unsigned share of that
contamination: batch style sits in *both* clouds and largely cancels, but it cancels exactly
only if the changed region carries batch style identically to the unchanged region, which is
not guaranteed. **We cannot sign the bias.** Every band, margin and rung staked from this
table is therefore staked with a stated multiple of slack against it (§9.5, §15-VG1, §21), and
§9.5 Scenario B names "the calibration was batch" as a fully-specified, separately-scored
outcome rather than a caveat.

### 3.3 The embedders — RESOLVED, v1's roles REVERSED

The first draft left this to a rule because phase 0 was still computing. **Phase 0 is
complete; the rule resolves; the assignment below is the frozen one.**

> **The rule as staked:** PRIMARY = instructed Qwen3-Embedding-0.6B iff the completed
> `phase0_bakeoff.json` records `C1.qwen.res` with verdict PASS **and** both excess and gap δ
> at least as large as `C1.bge.res`'s. Otherwise PRIMARY = bge.
>
> **The resolution:** `C1.qwen.res` = PASS, excess **+0.1217** vs bge's +0.0598 (2.0×),
> δ **+0.02664** vs bge's +0.00437 (6.1×). Both conditions met. **PRIMARY = Qwen.**
> The same ordering holds on v2's re-priced geometry: Ω\* 0.1245 vs 0.0629, δ 0.0318 vs 0.0060.

* **PRIMARY: `Qwen/Qwen3-Embedding-0.6B`**, instructed, via the DeepInfra OpenAI-compatible
  embeddings endpoint. **The instruction string is pinned verbatim, including the newline:**

      "Instruct: Identify what kind of commitment changed between the two versions.\nQuery: "

  prepended to **every** text this model embeds — C1, C1P, the positive control (§12), and the
  determinism gauge. 1024 dimensions.
* **SECOND WITNESS, required: `BAAI/bge-large-en-v1.5`**, no instruction prefix (symmetric
  use), 1024 dimensions. The headline verdict must replicate in **sign and verdict cell** on
  the witness, else the finding is published as **EMBEDDER-DEPENDENT** and is not promoted
  (v1 §3, house rule `shared-lemma-one-witness`). The witness's gate is **WG1** (§15), which
  is deliberately weaker than the primary's VG1 and says why.
* **THIRD ARM, REQUIRED, NEW: `Qwen/Qwen3-Embedding-0.6B` with NO instruction prefix** — the
  instruction ablation. See §3.3b. It is not a candidate primary; it exists to price one
  specific circularity.

**Justification for the reversal, and its caveat.** Three reasons, in decreasing strength:

1. **The construction is a task, and only one of the two models can be told the task.** C1 is
   not a document; it is a rendered comparison. bge is used symmetrically with no prefix and
   has no channel through which "read this as a change" can be said. The instructed Qwen arm
   exists precisely to steer the representation toward change-kind, and phase 0 was designed
   around that contrast. **This is the claim §3.3b's ablation settles rather than assumes.**
2. **Context length.** Qwen3-Embedding carries a 32k context; bge-large carries 512 tokens and
   the DeepInfra endpoint **rejects over-length input with HTTP 400 rather than truncating**
   (v1 deviation D-5). C1 renders two sentence windows plus a template — roughly twice the
   length of a single corpus field — so the truncation exposure is real and asymmetric. §3.4's
   V7 now handles the sub-threshold band explicitly.
3. **Phase-0's measured separation**, resolved above and re-priced in §3.2b.

**Nuisance-arm resolution — an unhandled branch of the first draft, resolved here.** §3.2's
"the residualized arm is the passing arm" was a **bge-only** fact. On the resolved primary
**both** arms pass: `C1.qwen.res` (excess +0.1217, δ +0.02664) and `C1.qwen.raw` (excess
+0.1041, δ +0.02819). Neither strictly dominates — `res` has the larger excess, `raw` the
marginally larger gap. The frozen rule:

> **`res` (the residualized arm) is PRIMARY**, on two grounds stated together: it carries the
> larger **excess** on the primary embedder, which is P1a's statistic; and it is v1's
> pre-registered primary, so keeping it is continuity rather than selection. **The `raw` arm's
> larger gap is disclosed here and reported beside every δ.** If the two arms land in different
> §9.3 verdict cells, the finding is **NUISANCE-DEPENDENT** and is not promoted — not resolved
> by picking the friendlier one.

**Construction substitution is CLOSED.** The completed artifact shows no construction strictly
dominating C1 on the primary (§3.2). **After the freeze, no substitution**, and no post-hoc
promotion of any other construction (§17).

### 3.3b The instruction ablation — a required third arm, and why

The primary is an instructed model whose instruction was **written by the taxonomy's author
with the taxonomy in hand**. That is the sharpest circularity route into the primary arm: a
reading of 2× bge's excess cannot be separated into model capability versus instruction
steering without the ablation, and the steering is an author-authored channel.

**Measured on Corpus A, all cells now in the artifact** (the first draft did not have them),
and re-priced on v2's own geometry so the comparison is not a normalization artifact:

| **v2's geometry: K = 11, rank(B) = 10, n = 227** | `C1.qwen.res.K11` **instructed** | `C1.qwen_noinstr.res.K11` **bare** | ratio |
|---|---|---|---|
| Ω(11) | 0.34274 | 0.19239 | 1.78× |
| N1 null median | 0.21824 | 0.11372 | 1.92× |
| **Ω\* (excess)** | **+0.12450** | **+0.07867** | **1.58×** |
| placebo Ω(11) | 0.31050 | 0.18023 | 1.72× |
| placebo excess | +0.10102 | +0.07065 | 1.43× |
| **δ** | **+0.031824** | **+0.012464** | **2.55×** |
| gap-null p99 | 0.018188 | 0.008848 | 2.06× |
| p_gap_N1 | 0.001996 (0/500) | 0.001996 (0/500) | — |
| **ψ** | **0.2556** | **0.1584** | 1.61× |
| evr_top11 | 0.4292 | 0.3075 | 1.40× |

*(The K = 12 phase-0 cells give the same picture — 1.55× on the excess, 2.60× on the gap — so
the effect is geometry-stable and is not an artifact of the re-pricing.)*

**The reading, fixed now, in three parts:**

1. **The instruction is not inert.** It is worth **1.58× on the excess and 2.55× on the gap**.
2. **The instruction is not the whole story either.** The bare Qwen arm **passes every phase-0
   conjunct on its own** — p_N1 at the 0/500 floor, p_gap at the 0/500 floor, δ positive in
   100% of splits — so C1 reads changes without being told to, and its δ of 0.012464 would
   clear §15-VG1's absolute floor (by 1.25×) and its own gap-null p99 of 0.008848.
3. **And here is the sharp part, staked so it is not discovered later:** the two arms fall in
   **different ψ bands of §13**. The instructed arm reads ψ = 0.256 — "the change carries a
   substantial minority of the alignment". The bare arm reads ψ = 0.158 — **"the reading is
   mostly context"**, §13's mandatory-disclosure band. **On the calibration corpus, the
   author-written instruction is what moves this instrument out of the mostly-context band.**
   That is the single most important number in this section and it is why the ablation is a
   required arm rather than a diagnostic.

**Staked for E2, before the run:**

* The bare-Qwen arm is embedded and analysed on all 474 items in both renderings (474 × 2 =
  948 texts, inside the §3.4 budget), through the identical pipeline.
* **If the bare arm reproduces the instructed arm's Ω\* and δ within the reported intervals,
  the instruction is inert on E2** and the primary's reading is a property of the construction,
  not of an author-written prompt.
* **If the bare arm collapses while the instructed arm passes** — δ_bare below VG1's margin
  while δ_instructed clears it — the primary's reading is **INSTRUCTION-DEPENDENT**, is
  published under that name, and **is not promotable**, because the channel that produced it
  was written by the taxonomy's author.
* **If the bare arm passes and the instructed arm does not**, the instruction is harmful and
  the run reports that plainly; the primary assignment is *not* switched post hoc (§17).
* Any intermediate outcome is reported as the measured ratio with no verdict attached.

### 3.4 Instrument hygiene

* **Determinism gauge, run first.** 20 fixed texts embedded twice in separate requests, per
  model, with the instruction applied where it applies. Median cos ≥ 0.9999 → proceed;
  < 0.999 → **VOID** (§15-V2); 0.999–0.9999 → recorded as a noise floor and continue.
* **Truncation, measured before embedding, with the sub-threshold band now handled.** Token
  counts for all C1 and C1P texts are computed client-side before the first request.
  * **> 2% of a model's texts over context → V7**: that model's arm switches to `BAAI/bge-m3`
    (8,192-token context), everything re-runs on that arm, and the switch is recorded.
  * **≤ 2% over context → the items are DROPPED, not truncated and not sent.** DeepInfra
    returns HTTP 400 rather than truncating (v1 D-5), so an unhandled 1.9% would hard-fail the
    run mid-flight. Worse, **C1 and C1P have different lengths**, so an item can be
    over-length in one arm only, which would silently unpair δ. The frozen rule: **any item
    whose C1 *or* C1P text exceeds the context on *any* embedder is dropped from both arms, all
    rivals, the positive control and every null, on every embedder.** One item set, everywhere.
    The drop list and count are reported, and V1b / V3 / VG3 are re-evaluated on the reduced
    set.
* **Caching.** Every vector cached to
  `/home/emoore/CIRISOntology/scratchpad/eigen/cache/eigen_cache_<model-slug>.jsonl`, keyed
  `sha256(model || "\x00" || text)`; the cache sha256 goes in the results file.
* **Cost.** 474 items × 2 renderings × 3 embedder arms = 2,844 texts, plus ≤ 570
  positive-control texts (§12: 95 items × 3 families × 2 embedders) and 120 gauge texts
  = **3,534 texts**, well under $0.05. Panel annotation (§20) is budgeted separately at
  ≤ $1.00. Hard cap **$3.00** total; abort and report if exceeded (§15-V10).

---

## 4. The matrix — frozen

For every item i the **primary cloud** is

    x_i = normalize( e( C1_i ) )                    (the C1 rendering, one embedded text)

and the **placebo cloud** is

    x'_i = normalize( e( C1P_i ) )                  (identical rendering, unchanged slot)

Both clouds are column-centred **on the fitting set only** before SVD, exactly as v1 §4.

**Nuisance residualization (the primary arm).** From each cloud, regress out
(i) `log10(1 + changed-region characters)` — the LCP/LCS region length, max of the two sides;
(ii) **domain dummies (12 levels)**; (iii) **batch dummies (40 levels)**. The regression is
fit **on the fitting half only** and applied to the held-out half.

**Column convention, pinned to the code rather than to prose.** `run_phase0.py`'s `dummies()`
uses `sorted(set(vals))[1:]` — i.e. **drop-first, K−1 dummies**. With a constant that is
**1 + 1 + 11 + 39 = 52 columns at full rank**, not the 53 the first draft stated (which was a
constant plus two full one-hots, rank-deficient by 2, and would have left `lstsq` silently
taking a minimum-norm solution). 52 columns against ~237 fitting rows, and that df cost is
disclosed here rather than discovered later. **The residualized arm is PRIMARY** (§3.3).

**The batch term's cost — the sign claim is WITHDRAWN and replaced by arithmetic.** The first
draft asserted that on E2 the batch term is "a power gain, not a power tax". That assertion is
withdrawn: it was stated as a fact without measurement, and the arithmetic points the other
way. With ~237 fitting rows over 40 batches there are **≈5.9 items per batch per fitting
half**; because the design puts ~1 item per kind per batch, each batch mean is a *noisy
estimate of the grand mean* built from ~6 points, and those coefficients are then **applied to
the held-out half**, whose items contributed nothing to them — injecting on the order of σ²/6
of pure estimation noise into every held-out vector before the SVD. What is true and
measurable is only this: on E2 kind ⊥ batch by design (§2.2), so the batch term cannot remove
*kind* signal the way it did on Corpus A (v1 §4's stated cost). Whether it is a net gain or a
net tax is **not asserted; it is measured by the arm comparison below and by §11-D-B2**, and
the answer is reported either way.

**Sensitivity arms, reported, never headline (v1 §17):**

| arm | what it drops | pre-committed disagreement rule |
|---|---|---|
| **span+domain-only** (no batch term, 13 columns) | the 39 batch dummies and their df cost | different §9.3 cell from the primary → **NUISANCE-DEPENDENT**, not promoted |
| **raw** (no residualization) | all of `Z` | different §9.3 cell → **NUISANCE-DEPENDENT**, not promoted |
| **clear-only** (n = 354, §2.1b) | the 120 hard items | different §9.3 cell → **DIFFICULTY-DEPENDENT**, not promoted |

None of these is resolved by picking the friendlier one.

---

## 5. Discriminator directions — frozen

**Label source: authored `kind_target`, primary**, for v1 §5's three reasons unchanged
(it is the design's intended coordinate; it is balanced by construction; panel modals import
the annotator instrument's own measured confusions). **Secondary arm: panel modal label at
BASE**, produced by the post-freeze protocol of §20, with v1 §2.3's frozen off-vocabulary
rule applied verbatim. **If the two arms disagree in verdict, the finding is
INSTRUMENT-DEPENDENT and is published as such.**

**Construction: class-centroid contrasts, not fitted classifiers** (v1 §5) —

    w_k = normalize( mean{x_i : label(i)=k} − mean{x_i : label(i)≠k} )

Logistic/LDA discriminators remain **excluded by design** at ~20 per class in 1024 dimensions.

### 5.1 The counting identity at K = 11

v1 §5.1's algebra, one class shorter. For one-vs-rest centroid contrasts on N items with class
sizes n_k and grand mean μ: c_k = N·(m_k − μ)/(N − n_k) and Σ_k n_k (m_k − μ) = 0. Therefore

* the **11 contrasts span exactly 10 dimensions**, for any labelling of any corpus;
* **any 10 of them span the same subspace as all 11**;
* `rank(B) = 10`, `S_kind` is the 11-class between-class subspace of dimension 10,
  orthonormalized by QR;
* the identity is preserved by the N1 permutation (permuted contrasts also span 10), so it
  cancels exactly and is **never reported as a result**;
* Ω renormalizes by `1/rank(B)`, and **`rank(B)` is quoted beside every Ω** (v1 §6, §15-V1).

**The arithmetic of dropped classes, verified rather than assumed.** When §15-V1 marks a class
UNMEASURED it removes that class's **contrast column** from B while its items remain in the
cloud. Verified by direct computation on synthetic 11-class data: **`rank(B) = min(#contrast
columns kept, 10)`.** So the *first* drop leaves rank at 10 — because any 10 of the 11
contrasts span the same 10 dimensions — and rank falls only from the **second** drop onward.
v1's own artifact confirms the mechanism at K = 12 (`main_primary.json`: `V1` fired,
`unmeasured = ['axiotic']`, `rank_B = 11.0` — unchanged). §15-V1b's threshold is therefore
restated in **classes kept**, not in rank, because the first draft's gloss was off by two.

### 5.2 LOKO directions — retained as a per-kind diagnostic only

v1 §5.2's leave-one-kind-out construction is retained, computed symmetrically for all 11
kinds, giving `A_k`, `ρ_k`, `η_k = A_k·ρ_k`. **In v2 it carries no verdict**: its verdict role
in v1 was the Record leg, which §1.4 excludes. It is reported as a table because it is the
cleanest available answer to "which kinds, if any, does this instrument see", and because
v1 §10's vacuity logic — **an instrument that finds no content directions anywhere cannot have
its silences interpreted** — is imported as §15-V5 in a reporting-only form.

---

## 6. Statistics — frozen

Let `U_k` = top-k right singular vectors of the centred held-out cloud, `B` = the orthonormal
basis of `S_kind` (10 columns; §5.1).

* **Subspace alignment** `Ω(k) = (1/r)·‖U_kᵀB‖_F²`, `r = rank(B)` (10, reduced per §5.1 if
  §15-V1 marks two or more classes UNMEASURED). Chance for random subspaces is quoted as a
  **scale only**: k/1024 = 0.0107 in the ambient space, and **k/237 = 0.0464** in the row space
  of the **held-out half** — the first draft's k/474 = 0.0232 used the full corpus, but `U_k`
  is the SVD of a ~237-row half, so 0.0464 is the comparable figure. **Neither is a null.**
  The permutation null is the floor (v1 §6, §7).
* **Excess** `Ω* = Ω(11) − median(N1 null)`. Because the C1 cloud is strongly anisotropic, the
  N1 null median is large (**0.2182 on the re-priced primary cell**, against a k/d scale of
  0.0107) and differs by embedder and by corpus. **Ω\* is the quantity that is comparable
  across arms, and every band, every forward prediction and every promotion rung is staked on
  Ω\* and δ, never on raw Ω.**
* **The gap** `δ = Ω_C1(11) − Ω_C1P(11)`, computed **paired within each split**, median over
  the splits — the *median of per-split differences*, which is the quantity VG1 gates. The
  *difference of medians* is reported beside it (the two differ by ~1% on the calibration:
  0.031824 vs 0.032245 primary, 0.005996 vs 0.007102 witness).
* **Attribution fraction** `ψ = δ / Ω*`, **guarded** — see §13 for the guard, which the first
  draft lacked. **Quoted beside every Ω in the results file wherever it is defined.**
* **Per-PC kind loading** `a_j = ‖Bᵀu_j‖²`, j = 1…40. **`Σ_{j≤40} a_j ≤ r`, with the shortfall
  `r − Σ_{j≤40} a_j` reported.** The first draft stated `Σ_j a_j = r exactly`; that identity
  holds over **all d directions**, not over the leading 40, and the held-out cloud has ~237
  PCs. Checkable directly from the artifact: `C1.bge.res` has Ω(40) = 0.3640 at r = 11, so
  Σ_{j≤40} a_j = **4.00**, not 11; `C1.qwen.res` gives **6.01**. **maxT remains the frozen
  choice, justified on FWER control under *arbitrary* dependence** — permutation maxT
  step-down (Westfall–Young) at FWER 0.05, not BH — and not, as the first draft said, on a
  negative dependence that does not obtain.
* **Kind rank** `R_kind` := #{ j ≤ 40 : a_j significant under maxT }. Free to take any value
  0…40. Counts *ranks at which loading exceeds the floor*; it does **not** assert that PC j is
  a reproducible direction (v1 §19-D8, which still binds: no sentence may say "PC 9 is the
  Structure direction").
* **LOKO** `A_k, ρ_k, η_k` for all 11 kinds (§5.2), reporting only.
* k is swept over **{5, 7, 9, 10, 11, 13, 15, 20, 30, 40}**; **k = 11 is the pre-registered
  primary with k = 10 as its rank-matched co-primary (§1.4), and no other k may be promoted
  post hoc** (§17).

---

## 7. Nulls — frozen, schedule pinned (v1 §7, reused with three additions and one replacement)

* **N1, label permutation (the rule-5 floor).** Permute `kind_target` across all 474 items,
  then run the **entire** 200-split pipeline on the permuted labels and take the median.
  **N_perm = 500.** p = (1 + #{null median ≥ obs median})/(1 + 500); **minimum reportable
  p = 2.0e-3**, and the **exceedance count is reported beside every p** so a knife-edge like
  §3.2's 4/500 is visible. Permutation is **free (unstratified)**, declared conservative in
  direction (§11-D-B3).
  * **Pinned schedule** (v1 §7): the held-out SVDs are computed **once** and reused across all
    500 permutations; only the centroid means, the QR and the Frobenius product recompute.
  * **Pinned combination rule:** the observed statistic is the **median over 200 splits**; the
    null is the distribution of that same median over the 500 permutations (null-of-medians,
    permutation index shared across splits). No per-split p-values are computed or combined.
  * **The same 500 permutations drive the C1 and C1P arms**, which is what makes δ's own
    permutation floor properly paired.
  * **N1 is the governing null for P1a's p-value in every branch** (§11-D-B3).
* **N1b, span-stratified label permutation — required conjunct.** Identical to N1 except
  labels are permuted **only within changed-region-length decile blocks**, preserving the
  kind↔span relation exactly. This is the only null that tests alignment *beyond edit size*,
  and it is required because v1 §2.1b measured an 87× span spread across kinds on Corpus A
  (Kruskal–Wallis p = 7.6e-16) and this design deliberately did **not** measure the
  corresponding number on E2 before the freeze (§0.1, §11-D-S1). Ω is additionally reported
  conditional on span decile. N_perm = 500.
* **N1c, batch-stratified label permutation (reported, not a required conjunct).**
  Permute labels **within each batch** (11–12 items, ~1 per kind). This preserves batch
  composition exactly. See §11-D-B3 for the expected direction and the governing-null rule.
* **N1d, difficulty-stratified label permutation (NEW, reported, not a required conjunct).**
  Permute labels within {clear, hard} blocks, preserving the kind↔difficulty relation exactly.
  Required by §2.1b's finding that `empirical` carries twice everyone's hard items and 41 of
  the 120 designed near-misses point at it. A NOT-DETECTED that N1d explains is a
  difficulty artifact, not a taxonomy verdict, and is reported under that name.
* **N2, split-halves — 200 splits, balanced JOINTLY on `kind_target` (11) AND `batch` (40) by
  construction.** This replaces the first draft's rejection sampler, which was measured to
  produce **zero usable splits** — see §7.2.
* **N-paired, the sign-flip randomisation on δ.** 10,000 sign flips of the per-split C1/C1P
  assignment, giving `p_paired` and `frac_splits_gt` (v1's K1c test, reused verbatim).
* **N4, rival partitions** — see §7.1.
* **Granularity is the item** (rule 3): every permutation and every split operates on whole
  items.

### 7.1 Rival partitions (N4), rank-matched — a v1 defect fixed

Two rivals, both fitted and evaluated by the identical pipeline, **paired within each of the
200 splits by §7.3's apparatus, and each with its own placebo δ**:

* **(i) k-means-11** on the fitting-half C1 cloud — the honest ceiling any 11-way partition can
  reach. Reported always as `Ω_kmeans − Ω_taxonomy`.
* **(ii) the non-taxonomy rival: domain-11** — the 12 authored domains collapsed to 11.
  **The merge is pinned, because the first draft's "merge the two smallest" does not identify a
  second class:** the counts are `report` 38 (unique smallest), then a **four-way tie at 39**
  (`bulletin`, `notice`, `policy`, `process`). **Frozen rule: merge `report` (38) with the
  alphabetically-first of the tied 39s, which is `bulletin`.** Domain is semantically coherent,
  is orthogonal to kind by design (§2.2), and is a **context** property: in a rendering that
  contains the context it is the strongest honest rival available.

**Rank matching, restated honestly.** v1's rival came back at rank(B) = 9 against the
taxonomy's 11, which made the rival's task structurally easier and the comparison unfair
(v1 §5's own disclosure). In v2 the requirement is **automatically satisfied for domain-11**:
by §5.1's identity *any* 11-way partition with all cells non-empty has rank exactly 10. So the
requirement has exactly **one** real case — **k-means-11 emptying a cluster in a fitting
half**, in which the pipeline's `C[cnt==0] = 0` would silently lower the rank. Frozen rule:
**if k-means returns fewer than 11 non-empty clusters in a fitting half, that split's k-means
comparison is dropped and counted**; if more than 10% of splits are dropped, the k-means
comparison is **reported as not rank-matched and cannot fire K1b**.

**Why the domain rival earns its place twice.** On Ω it prices "how much of this rendering's
principal geometry is topic". On δ it is a **negative control**: the domain of an artifact
does not change between before and after, so `δ_domain` should sit at zero. A δ_domain
materially above zero would mean the C1/C1P difference is leaking something other than the
change, and that is a diagnostic worth having in advance.

### 7.2 N2 — the split, replaced by a constructive balanced 2-colouring

**The defect, measured.** The first draft drew a kind-stratified half and then **rejected**
unless all 40 batches were balanced to ±1, up to 1,000 redraws. On the real labels (34 batches
of 12, 6 of 11) this **never succeeds**. Independently simulated for this revision:
**0 successes in 200,000 draws**, and the **median worst-batch imbalance is 8**. With 1,000
redraws × 200 split indices the expected number of usable splits is ~1e-4, every split index
is "skipped", and the "next seed" clause has nothing to fall through to. **The primary
analysis could not have run.**

**The replacement — a construction, not a search.** Build the bipartite multigraph with
vertices = 11 kinds ∪ 40 batches and **one edge per item** (kind ↔ batch). Join every
odd-degree vertex to a dummy vertex. Take an Eulerian circuit and **2-colour its edges
alternately along the circuit**; the two colours are the two halves. Every vertex of even
degree is entered and left in pairs, so each kind and each batch is split within ±1
simultaneously. Existence is guaranteed by de Werra's balanced bipartite edge-colouring
theorem; randomisation is by shuffling the edge insertion order, which permutes both the
adjacency order and the circuit.

**Verified on the real labels for this revision — 200 draws:**

* **0 constraint violations**, exact ±1 on **both** kind and batch **simultaneously**;
* halves of **exactly 237 / 237** every time;
* per-kind split at seed 0: 20/19, 20/20, 20/20, 29/30, 30/29, 18/19, 20/20, 20/20, 20/20,
  20/20, 20/20 — minimum half-class **18** (`epistemic`), comfortably above §15-V3's floor of 12;
* per-batch split: 6/6 for the 12-item batches, 6/5 or 5/6 for the 11-item batches;
* **200 distinct splits in 200 draws** — the randomisation is not degenerate.

**Two implementation guards, pinned, because a natural implementation gets this wrong.** Both
were found by writing the construction twice for this revision; the first version silently
produced ±2 violations on 3 of 50 draws.

1. **The total edge count, including dummy edges, must be even in every component**, or the
   circuit has odd length, its first and last edge receive the same colour, and the imbalance
   of 2 lands on the start vertex. On the real labels there are 4 odd-degree kind vertices
   (39, 59, 59, 37) and 6 odd-degree batch vertices (the six 11-item batches), so 10 dummy
   edges bring the total to 474 + 10 = 484, even, in a single component. **The implementation
   asserts both — even total, and even circuit length — and aborts rather than proceeding.**
2. **The colours must be assigned along the Eulerian circuit order**, i.e. Hierholzer's
   *reversed pop* order, **not** the DFS push order. Colouring the push order looks correct,
   passes casual inspection, and violates the balance.

Fit contrasts and the nuisance regression on half 1, centre + SVD + all statistics on half 2,
then swap and average. **No item ever contributes to both sides of a single split.** There is
no skip count to report, because nothing is rejected.

### 7.3 The paired-comparison apparatus — specified once, used everywhere

The first draft demanded "paired within split at p < 0.01" for P1a's rival conjunct, P1d's
δ-privilege conjunct and §10's P3 comparison **without naming a test or a reference
distribution**. The 200 splits share all 474 items and are near-replicates, so any across-split
test — sign-flip, Wilcoxon, t — has a badly understated variance and its p-value means
nothing on its own. VG1 got this right; nothing else did.

**Frozen: every comparison of the form "A beats B, paired at p < 0.01" in this document means
both of the following, and the permutation floor is the governing p.**

1. **Direction:** the sign-flip randomisation across splits on the per-split difference
   (A − B), 10,000 flips, reported as `p_signflip` and `frac_splits_gt`. **This leg alone is
   not evidence**, and the results file must say so wherever it is quoted: splits are not
   independent units.
2. **Magnitude, governing:** the same **500 label permutations** driving both arms, giving the
   permutation floor for the difference and `p_perm` with its exceedance count. **`p_perm` is
   the p-value the verdict reads.** Where a comparison has no meaningful label permutation
   (k-means-11, whose partition is refitted per split), the floor is the permutation of the
   *taxonomy's* labels with the rival refit inside each permutation, and that is stated in the
   results file.

Applies to: §9.2's `Ω_taxonomy > Ω_domain11`, §9.3's `δ_taxonomy > δ_domain11`, §10's P3
comparison, §7.1's k-means comparison, and every "paired" claim in §11.

---

## 8. GAUGE FIRST — the planted-rank gauge at v2's geometry, before any corpus embedding

House lesson `forward-prediction-confirmed`: *gauge the ruler with planted values before
staking a band.* v1 §8 is reused with the geometry re-staked, two additions, and one deletion.

**Geometry:** **the gauge's per-half n is 237**; d = 1024; **11 classes at E2's exact
half-sizes** as produced by §7.2's construction: [18, 19, 20, 20, 20, 20, 20, 20, 20, 29, 30],
summing to **236 for one half and 238 for the complement** — the gauge uses the **237-row
half**, drawing the two halves independently at the per-class sizes above with the odd class
rounded to give 237. Planted ranks **{6, 10, "10 + 3 non-kind"}**. Offset scale swept over
**{0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0} × the within-class σ**, **200 draws per cell**.

**The n convention, pinned, because reading it wrong cost the first draft its most important
forward statement.** `gauge_power_surface.py` sets `base = gauge.CLASS_SIZES`, and
`gauge.py`'s own comment reads *"Corpus A **half** sizes"*; `run_cell` then draws **two
independent halves of n rows each**. **So the power surface's `n` column is a PER-HALF size.**
E2's halves are 237, so **E2's row is the 2× row at n = 248 — not the 4× row at n = 496**. The
first draft read the 4× row and understated its own most likely failure mode. An implementer
who sets `CLASS_SIZES` to the *full* class sizes would gauge at twice the real resolution;
the pinned geometry line above says per-half explicitly for exactly this reason.

**Addition 1 — the scale-0 row is mandatory.** v1's power surface has no zero-signal row, so
gauge Ω values cannot be converted into excesses. Without it the gauge cannot be compared to
the corpus at all, because the corpus's null floor is anisotropy and the gauge's is isotropic
noise. The scale-0 row defines `Ω_gauge*(scale) = Ω_gauge(scale) − Ω_gauge(0)`, and it is
computed at every geometry the gauge reports.

**Addition 2 — the anchor scale is chosen by the measurement, from a table computed in
advance.** v1 validated its η statistic at anchor scale 4.0, where the gauge's own Ω was
0.299 — **five times the signal the corpus actually delivered** — and then had to disclose the
scope limit in the results (v1 §6). In v2 the whole gauge table is computed before any corpus
embedding, and the anchor is defined now as **the gauge row whose `Ω_gauge*` is closest to the
measured `Ω*`**, with linear interpolation between adjacent scales. Selecting a row from a
frozen table by a frozen rule is not a forking path; validating at a scale five times the data
is.

**Deletion — Ruling 3's two-world validation (the first draft's "Addition 3") is CUT.**
Record is excluded (§1.4), P2 has no v2 arm, and §5.2 already says LOKO carries no verdict, so
the two-world cell's only possible consequence was downgrading a no-verdict table from
"reporting-only" to "EXPLORATORY" — while costing ~40% of the gauge's cell count. Its outcome
was also close to pre-determined: v1's gauge returns `frac_12th_below_min = 0.920` at s = 1.5,
below the staked 0.95, at the scale the design expects. **It changes no decision and it is
removed.** The §5.2 LOKO table is published as reporting-only, unconditionally.

**Implementation declaration, imported verbatim from `gauge.py` because the prereg may not
leave it unspecified.** With an 11-class partition the between-class subspace has rank exactly
10 (§5.1), so a planted rank of 13 **is not constructible as a between-class rank**. `gauge.py`
records the resolution for the K = 12 case and it is adopted here for K = 11:

> *"'13 class-carrying between-class directions' is not constructible. The informative question
> the r=13 cell can answer is whether R_kind falsely counts strong NON-kind directions, which
> is exactly what the 'not 13' clause needs. This is an implementation specification of a
> generative model the prereg leaves unspecified; it is declared here."*

So the third world is **rank 10 plus 3 extra structured non-kind directions** carrying the same
per-direction variance as an average class direction. **`gauge.py` as it stands is hard-wired
to `NK = 12`, `RECORD_IDX = 11`, 12-long `CLASS_SIZES` and worlds `rank7 / rank11 / rank13`;
it has no `rank10` world. §8 therefore requires code changes that are not yet written, and
that is stated here rather than discovered at run time.**

**Quantities the gauge must return:** `σ_R` (largest across-scale s.d. of `R_kind` at planted
rank 10, over scales where mean recovered rank is within ±3 of planted); **`R̂` (mean recovered
`R_kind`) at every cell — now a load-bearing quantity, see §9.4**; `ρ_gauge` (median |cos|
between the same class's contrast fitted on two independent halves) at every cell; per-rank PC
replication |cos(u_j^{h1}, u_j^{h2})| for j ∈ {1, 2, 3, 5, 8, 10, 11, 13}.

### 8.1 The retraction ladder — automatic, per v1 §8.4 and Ruling 4

| gauge result | consequence, automatic, no human decision |
|---|---|
| σ_R ≤ 0.66 **and** \|R̂ − 10\| ≤ σ_R | **sharp clause lives**: P1b Tier 2 evaluated, band `R_kind ∈ {9, 10, 11}` — "not 6, not 13" is falsifiable-by-passing |
| 0.66 < σ_R ≤ 1.5 **and** \|R̂ − 10\| ≤ σ_R | "not 6, not 13" **RETRACTED in advance**; P1b Tier 1 only, band `\|R_kind − R̂\| ≤ 2σ_R` |
| **\|R̂ − 10\| > σ_R at the anchor** | **P1b is UNDECIDED and K2 CANNOT FIRE** (§9.4) — the estimator's own bias at the data's scale exceeds its spread, so no rank band is readable in either direction |
| σ_R > 1.5 | **V8 fires**: the rank leg cannot kill; `R_kind` is descriptive, with its interval, no band verdict |
| σ_R undefined (empty admissible set) | treated as σ_R > 1.5 |
| ρ_gauge < 0.30 at the anchor scale | **V3b fires**: centroid contrasts are unresolved at this class size, the split-half primary is **VOID**, and the run says so plainly |

**The first draft's §8.1 and §9.4 gave opposite instructions** — §8.1 said σ_R > 1.5 means "no
band verdict" while §9.4 said Tier 1 runs "always, if P1a DETECTED". The table above governs;
§9.4 defers to it.

### 8.2 What the power surface already says will happen — stated before the gauge runs

`out/power_surface.json` (synthetic, 100 draws/cell). **Read at the correct 2× row (per-half
n = 248 ≈ E2's 237)**, with the 1× row (per-half n = 124 ≈ the calibration's 113) beside it:

| planted scale | Ω (1×, n=124) | Ω (**2×, n=248**) | σ_R (**2×**) | **R̂ (2×)** | ρ_gauge (**2×**) |
|---|---|---|---|---|---|
| 1.0 | 0.0167 | **0.0307** | **1.566** | **3.37** | **0.172** |
| 1.5 | 0.0435 | **0.0908** | **1.511** | **6.42** | **0.320** |
| 2.0 | 0.0881 | **0.1630** | **1.318** | **6.89** | **0.445** |
| 2.5 | 0.1468 | **0.2431** | **1.284** | **7.85** | **0.567** |
| 3.0 | 0.2030 | **0.3092** | **0.994** | **7.85** | **0.652** |
| 4.0 | 0.2996 | **0.4138** | **1.021** | **8.72** | **0.771** |

**The forward statements, staked here, about the instrument and not the taxonomy:**

1. **The rank leg will be UNDECIDED, and this is near-certain.** Across Scenario A's whole
   staked band the gauge's recovered `R̂` runs **6.9–7.9** against a planted rank of 10, while
   σ_R runs **1.07–1.32**. So `|R̂ − 10|` is **2.2–3.1, always larger than σ_R**, and §8.1's
   third row fires. **"Not 6, not 13" is retracted in advance for the second time, and K2
   cannot fire.** If the v2 gauge returns `|R̂ − 10| ≤ σ_R` at the anchor, this statement is
   falsified and the rank leg becomes live — which would make it *stronger* evidence than
   expected.
2. **V3b and V8 are, to a good approximation, the same event as Scenario B (§9.5).** This is a
   correction to *both* the first draft and the referee report, and it is the sharpest thing
   the gauge says. Mapping the re-priced primary calibration through the gauge on §9.5's
   three-step excess convention (Ω\* = 0.1245 matches gauge scale **s ≈ 2.40** on the 1× row;
   the same scale on the 2× row predicts **Ω\* ≈ 0.217**), Scenario A's staked band
   Ω\* ∈ [0.15, 0.28] corresponds to **s ∈ [1.99, 2.86]**, where **ρ_gauge = 0.44–0.63 (V3b
   clear by 1.5–2.1×) and σ_R = 1.07–1.32 (V8 clear)**. Scenario B's upper edge Ω\* = 0.03
   corresponds to **s ≈ 1.09**, where **ρ_gauge = 0.197 (V3b FIRES) and σ_R = 1.56 (V8
   FIRES)**. The first draft said "V3b is a live risk" off the wrong row; the referee report
   said "V3b straddles or fires across the whole calibration-implied range" off a Scenario A
   priced from the demoted embedder at the wrong class count. On the corrected anchor at the
   corrected row, **neither V3b nor V8 fires in the world where the taxonomy is real at the
   calibration-implied scale, and both fire in the world where it is not.** They are resolution
   gates, and the resolution is adequate exactly when there is something to resolve.

**The honest limit of this mapping, stated because a forward prediction rests on it.** Raw Ω
values in the power surface are **not** comparable to corpus Ω: the gauge's floor is isotropic
noise, the corpus's is a label permutation on an anisotropic cloud. Addition 1's
excess-to-excess convention is what makes them comparable, and it makes them comparable
**approximately, not exactly** — the permutation null absorbs the corpus cloud's anisotropy,
which is the point, but the two excesses are still excesses over different floors and the map
between them is a modelling assumption, not a measurement. Everything above is labelled a
forward statement about the *instrument* for that reason. The 1×→2× ratios it rests on run
1.38–2.09 across scales.

---

## 9. Verdicts — staked bands

### 9.1 Order of evaluation, which is itself part of the freeze

1. **Gauge** (§8) → σ_R, R̂, ρ_gauge, the §8.1 ladder, V3b/V8 resolved. *No corpus text
   embedded yet.*
2. **Determinism gauge** (§3.4) → V2.
3. **Token-count pass** over C1 and C1P texts, all three embedder arms → V7 and the drop set.
4. **Embed C1 and C1P for all surviving items, all three arms**; per-class degeneracy → V1/V1b;
   near-duplicate ties → V4; class support → V3; record `rank(B)`.
5. **Positive control** (§12) → VG2.
6. **The placebo gate** (§15-VG1) → the instrument is VALID or the run is
   **VOID-AS-INSTRUMENT and stops here for verdict purposes**, with every number still
   reported.
7. Only if VALID: P1a, P1d, the rivals, P1b, the diagnostics.

**Step 6 is the structural change from v1.** In v1 the placebo was a kill on an
interpretation, evaluated at the end, and its firing had to be retro-fitted onto a verdict
that had already been read. Here the instrument proves it reads changes **before** its reading
counts for anything.

### 9.2 P1a — alignment (primary arm, primary embedder, k = 11), graded per v1 §22 Ruling 1

**DETECTED** iff all four:

* median Ω(11) beats the **N1** null at p < 0.01, **and**
* median Ω(11) beats the **N1b** span-stratified null at p < 0.01, **and**
* `Ω_taxonomy > Ω_domain11` by §7.3's apparatus at governing p < 0.01 (rank-matched, §7.1),
  **and**
* **the rank-matched co-primary Ω(10) satisfies the same three conjuncts** (§1.4). If Ω(11)
  passes all three and Ω(10) does not, P1a is **NOT DETECTED** and the finding is published as
  **k-DEPENDENT**, because the pass would then be carried by the one principal direction that
  the kind subspace has no dimension for.

**Strength, graded iff DETECTED — and graded on Ω\*, not on raw Ω.** v1 Ruling 1's edges were
set on v1's Δ cloud, whose N1 null median was **0.0598**. The re-priced primary's null median
is **0.2182** — 3.6× higher — so on the raw scale, `Ω(11) ≥ 0.25` requires an excess of only
**0.032** and would be a "STRONG" label carrying almost no information. Ruling 1's *numbers*
are not lowered, and its *meaning* is what gets carried across, by translating each edge
through v1's own null:

| band | **operative edge (on Ω\*)** | v1's raw-Ω edge, reported beside it |
|---|---|---|
| **STRONG** | **Ω\* ≥ 0.190** | Ω(11) ≥ 0.25 |
| **MODERATE** | **0.020 ≤ Ω\* < 0.190** | 0.08 ≤ Ω(11) < 0.25 |
| **WEAK** | **Ω\* < 0.020** | Ω(11) < 0.08 |

The right-hand column is reported for continuity with v1 and is labelled **"v1 units, not the
operative band"** wherever it appears. Never lower a floor: the operative edges are *higher*
bars than the raw-Ω edges on this cloud, not lower ones. **NOT DETECTED** if any conjunct
fails.

**KILL K1:** p ≥ 0.01 against N1 **or** against N1b → the alignment leg is dead on this
instrument (§16), **with the N1/N1b sub-verdicts of §16 distinguishing which**.
**KILL K1b:** `Ω_taxonomy ≤ Ω_domain11` → the taxonomy is not privileged among 11-way
partitions (§16). Separable from K1.

### 9.3 P1d — change-attribution, and the joint verdict table

**P1d PASSES** iff VG1's gates hold (§15-VG1) **and** `δ_taxonomy > δ_domain11` by §7.3's
apparatus at governing p < 0.01.

Every combination is named in advance, so no cell can be re-described after the fact. **The
first draft's table claimed exhaustiveness with one of the four non-VOID cells missing; it is
added here.**

| P1d | P1a | verdict name | what it means, fixed now |
|---|---|---|---|
| PASS | DETECTED | **CHANGE-CARRIED ALIGNMENT** | the eigen-bridge has support on this instrument, at the strength band read from Ω\* and with ψ quoted. This is the only cell from which promotion may even be proposed (§21) |
| PASS | NOT DETECTED | **CHANGE-READ, TAXONOMY-NULL** | the instrument demonstrably reads changes, and the 11 kinds are not recoverable from what it reads. This is a **real null of the geometry claim** — the outcome v1 could not produce, and the reason v2 was built |
| FAIL (VG1 held, δ-privilege failed) | DETECTED | **CONTEXT-PRIVILEGED** | alignment is real and is not the change's: the domain rival moves as much of the gap. Published under that name; not the eigen-bridge |
| **FAIL (VG1 held, δ-privilege failed)** | **NOT DETECTED** | **CHANGE-READ, NOTHING-PRIVILEGED** *(the added cell)* | the instrument reads changes, the taxonomy is not recoverable, **and** the taxonomy holds no privilege in the gap either. The strongest available negative reading short of VOID, and it is a **real null** on both legs |
| VG1 fired | any | **VOID-AS-INSTRUMENT** | no verdict in either direction. Ω, δ, ψ and every diagnostic are reported as numbers; no null, no support, no band, no promotion. The steward's ruling, encoded |

A sixth outcome is named because it is likely and must not be reported as one of the five:
**KIND-IS-IN-THE-CONTEXT** — VG1 fired *and* `Ω_C1P` clears its own N1/N1b nulls at p < 0.01.
The run is still VOID-AS-INSTRUMENT for P1; what is additionally true is that the context
rendering carries kind, which is §10's P3 and is EXPLORATORY there.

### 9.4 P1b — rank, two tiers, RE-CENTRED on the gauge's recovered rank

**The defect this fixes.** The first draft centred P1b's bands on the **planted** rank (10)
while the gauge's own **recovered** rank at the data's scale is 6.4–7.9 (§8.2). A perfectly
behaving instrument would therefore have read ~7, fallen outside both Tier 1's [8, 12] and
Tier 2's {9, 10, 11}, and §16 would have reported K2 as taking down the "near 10" clause — a
world-verdict manufactured entirely by a known, measured, downward estimator bias.

**Frozen: every band is centred on `R̂`, the gauge's mean recovered `R_kind` at the anchor
scale, and `R̂ − 10` is quoted as the disclosed bias wherever `R_kind` appears.**

| tier | condition to evaluate | outcome | band |
|---|---|---|---|
| **precondition** | \|R̂ − 10\| > σ_R at the anchor | **UNDECIDED, K2 cannot fire** | — |
| **Tier 1** | P1a DETECTED, precondition passed, σ_R ≤ 1.5 | **CONSISTENT** | `\|R_kind − R̂\| ≤ 2σ_R` |
| | | **INCONSISTENT (K2)** | outside that band |
| **Tier 2** (sharp) | additionally σ_R ≤ 0.66 | **PASS** | `R_kind ∈ {9, 10, 11}` |
| | | **KILL (K2)** | outside {9, 10, 11} |
| **UNDECIDED** | P1a NOT DETECTED, or VOID, or σ_R > 1.5 (V8), or the precondition fails | — | the rank leg is not evaluated |

**The band is a function of σ_R and is not summarised by a single interval.** The first draft
said "at worst [8, 12]", which is wrong above σ_R = 1.0: at σ_R = 1.5 the band is
`|R − R̂| ≤ 3`, six units wide, and **Tier 1 becomes vacuous — unable to exclude either 6 or
13 — for any σ_R ≥ 1.5**, which is exactly where §8.1's V8 boundary sits. The width is reported
as `4σ_R` beside every Tier 1 statement.

If `R_kind` lands near 7, no coincidence is spun with RATCHET's 90% horizon (v1 §9-P1b, §17);
the two are ranks of different objects and the RATCHET leg is REPORTED-BUT-UNPINNED (v1 §21).

### 9.5 FORWARD PREDICTION — one ordered statistic, exhaustively partitioned

**Why this is restaked.** The first draft's two scenarios were priced from `C1.bge.res` at
K = 12 — the demoted embedder at the wrong class count. On the resolved primary the numbers
move by 2–6×, which **pre-falsified Scenario A before the run**: the calibration's own δ
(0.0318) already exceeded A's upper edge of 0.020 at half the n. Worse, the scoring rule read
2 of A's 5 conjuncts, OR'd its clauses so outcomes could be double- or non-assigned, left the
most likely middle band uncovered, and converted a missed high prediction into *support*,
which rule 6 forbids.

**Frozen: one ordered statistic, `Ω*(11)` on the primary embedder's primary arm, partitioned
exhaustively and exclusively over (−∞, ∞). δ and ψ are SECONDARY predictions, scored
separately and never used to reassign the primary band.**

**The pricing, stated so it can be attacked.** The re-priced primary calibration is
Ω\* = **0.12450** at n = 227 (per-half 113). It is mapped to E2 through the gauge in three
steps, all on §8's excess-to-excess convention (Addition 1):

1. **Find the gauge scale that reproduces the calibration.** The calibration's per-half 113
   sits nearest the power surface's **1× row** (per-half 124). Subtracting that row's measured
   scale-0 floor, `Ω_gauge(0) = 0.01093`, gives excesses of 0.0772 at s = 2.0 and 0.1359 at
   s = 2.5; Ω\* = 0.12450 interpolates to **s ≈ 2.40**.
2. **Read the same scale at E2's resolution.** E2's per-half 237 sits nearest the **2× row**
   (per-half 248). At s ≈ 2.40 that row gives **Ω\* ≈ 0.217**.
3. **The floor's stability, measured rather than assumed.** The scale-0 Ω is the ambient-chance
   value `k/d = 11/1024 = 0.01074` and is essentially n-independent. Measured for this
   revision (`out/power_surface_scale0.json`): **0.01093 at 1× and 0.01086 at 2×** — a 0.6%
   difference — with ρ_gauge = 0.020/0.021 and R̂ = 0.04/0.06 at scale 0, as a zero-signal row
   should read. v1's own gauge independently read **0.0110** at its lowest-signal cell
   (`gauge.log`, `rank7@0.5`). The mapping above uses the two measured floors.

**Sensitivity, so the band is not a point dressed up.** On the raw-Ω mapping (no floor
subtraction) the same procedure gives **0.213** rather than 0.217 — a 2% shift, which does not
move the band. The 1×→2× ratio across the whole scale grid runs **1.38–2.09**, and perturbing
the calibration excess by ±20% moves the prediction over roughly **[0.18, 0.25]**. The staked
band widens that to cover the batch-inflation caveat of §3.2b in both directions.

| band on Ω\*(11) | name | scored as |
|---|---|---|
| **Ω\* < 0.03** | **Scenario B — "the calibration was batch"** | **B confirmed.** Corpus A's kind is 6/6 batch-nested and N1 cannot see batch; on E2, where kind ⊥ batch by design, that component vanishes and the excess collapses with it. VG1 is expected to fire; §8.2 says V3b and V8 fire here too. **B's confirmation is a statement about the CALIBRATION, not a world-verdict** — it says the phase-0 selection was confounded, and nothing about the taxonomy. Verdict read from §9.3, which will be VOID-AS-INSTRUMENT or KIND-IS-IN-THE-CONTEXT, i.e. **no verdict in either direction** |
| **0.03 ≤ Ω\* < 0.15** | **the middle** | **both predictions missed, low.** Reported as a miss in the same type size as a hit. Real signal, far below the calibration-implied scale — the interleave cost most of it, or the calibration was partly batch. Verdict read from §9.3 regardless |
| **0.15 ≤ Ω\* ≤ 0.28** | **Scenario A — "the taxonomy is real at the calibration-implied scale"** | **A confirmed**, scored as a rule-6 item **for the power model**. Support for the taxonomy leg comes only through the §9.3 verdict, never through the prediction |
| **Ω\* > 0.28** | **A missed high** | **a miss, reported as a miss.** The first draft called this "A falsified high … which makes the pass *stronger* evidence"; that converts a failed advance prediction into support and is deleted. The §9.3 verdict is read independently and is neither strengthened nor weakened by the miss |

**Secondary predictions, scored separately and reported whether or not the primary band hits:**

* **δ ∈ [0.020, 0.065]** — the calibration's 0.031824 carried through the same **1.74** ratio
  (point value **0.055**), widened.
* **ψ ∈ [0.15, 0.40]** — the calibration's 0.2556, widened. ψ is only scored where §13's guard
  defines it.
* **Ω\*_C1P ∈ [0.12, 0.25]** — the placebo's own excess, the calibration's 0.1010 carried
  through. **This is the named discriminator between A and B**: under A it stays large, under B
  it collapses with everything else. **If the placebo excess stays large while δ collapses,
  that is neither A nor B but KIND-IS-IN-THE-CONTEXT** (§9.3, §10).

A secondary miss alongside a primary hit is reported as exactly that, and neither is allowed
to relabel the other.

---

## 10. P3 — the site claim (secondary, EXPLORATORY, cannot be promoted)

**Statistic:** `Ω_C1P(11)` and its N1/N1b p-values, plus the paired comparison
`Ω_C1P,taxonomy` vs `Ω_C1P,domain11` by §7.3's apparatus.

**Staked reading, fixed before the data:**

* Both nulls cleared at p < 0.01 **and** the taxonomy beats the domain rival at governing
  p < 0.01 → **the change *site* carries the kind**, at embedding granularity, independently
  of what the change does. Consistent with `Core/Generator.lean`'s derivation of the kinds as
  the exact image of a **site** model — and consistent is the strongest word available.
* Either null missed → the site does not carry kind at this granularity. No kill fires; P3 is
  secondary.

**Four hard limits, pre-committed:**

1. **P3 is never support for P1.** They are different renderings and different claims; a
   residual is never support (rule 6).
2. **P3 is not promotable from this corpus at any strength.** We wrote the items and chose the
   sites with the taxonomy in hand. The most P3 can be is a hypothesis for a corpus somebody
   else wrote.
3. **P3 is EXPECTED to pass** (§1.3): v1 already measured Ω_before = 0.13374 against a null of
   0.10827 at 0/500, and the re-priced placebo excess is +0.1010 on the primary. A pass is the
   prediction, not the news, and the results file must say so in the same sentence that
   reports it.
4. P3 exists in this document so that a large placebo reading cannot be *discovered* in the
   results and then narrated as a finding. It is pre-registered, bounded, and labelled.

---

## 11. Design diagnostics — what replaces V11, and what verifies the interleave

v1's V11 bound the pooled arm to two within-batch arms because kind was nested in batch. E2's
design retires the confound (§2.2). **A design claim is not a measurement**, so each claim is
converted into a post-freeze measurement with its meaning fixed here.

| # | measurement | staked meaning |
|---|---|---|
| **D-B1** | 5-fold stratified TF-IDF 1–2gram + logistic accuracy predicting **batch** (40 classes) from the unchanged `before` text. **Majority baseline = 12/474 = 0.0253**, so the quantity read is **lift = accuracy / baseline**, not accuracy | **lift ≤ 1.2× (acc ≤ 0.030) → batch style is weak**, at or below the 1.18× lift that forced the corpus rebuild (§2.2). 1.2–3× → detectable; the batch-residualized primary is doing real work and the span+domain-only arm is reported beside it. **> 3× → batch style strong**; Ω_batch must be reported (D-B2) and the disclosure sentence is mandatory in the headline. *The first draft's thresholds (≤ 0.10 "weak") were an accuracy scale on a 40-class problem, i.e. a 4× lift called weak — roughly 3.4× stronger in lift terms than the confound the rebuild was for* |
| **D-B2** | `Ω(11)` computed with **batch as the label** (40 classes, rank(B) = 39, Ω renormalized by 1/39), against its own N1 null | this prices how much of the principal geometry batch occupies. It cannot inflate the kind reading — kind ⊥ batch means batch variance sits in directions the kind subspace does not use — but a large Ω_batch means batch is **taxing power**, and the reported Ω_kind is then an underestimate. Reported, never used to adjust a verdict |
| **D-B3** | **N1c** (batch-stratified permutation, §7) vs **N1** | **Expected direction, stated because the first draft had it backwards:** N1 permutes freely, so its permuted labellings are batch-*unbalanced* and absorb batch style, while N1c preserves the design's balance. If batch carries variance the expectation is **N1 null ≥ N1c null** — free permutation is the *conservative* one. **`N1` is the governing null for P1a in every branch**, including after a disagreement; switching to N1c would be anti-conservative and is forbidden (§17). D-B3's meaning is "how much batch variance a random 11-way partition absorbs", not a threat to the result. A large disagreement is reported as a headline caveat |
| **D-S1** | **NEW.** The E2 changed-span length distribution by kind: Kruskal–Wallis across the 11 kinds, and the max/min ratio of per-kind medians. Corpus A measured an **87× spread, KW p = 7.6e-16** (v1 §2.1b) | **Read BEFORE N1b's p-value is read**, so the N1b conjunct is interpreted rather than merely applied. Spread ≤ 5× → N1b is a light correction and K1-on-N1b would be a geometry verdict. Spread > 20× → N1b is doing very heavy lifting; an N1b failure is reported as **SPAN-CONFOUNDED** (§16-K1), not as a taxonomy verdict |

**And one gate, replacing the χ² the first draft used.** §2.2 measured why the χ² cannot fire:
min expected cell 0.859, 100% of cells below expected 5, 390 dof, χ² = 18.8, p = 1.0000. No
plausible drop pattern moves that below 0.05, so it was decorative — and it was the *only* gate
protecting the design claim on the analysed set.

> **§15-VG3, restated as a direct combinatorial criterion on the items actually used** (after
> V7 drops, V1 drops and V4 deduplication):
> **(a)** no batch loses more than **3** of its 11–12 items, **and (b)** no kind loses more
> than **10%** of its items, **and (c)** `max_b (11 − #distinct kinds in batch b) ≤ 3`.
> Any breach → the interleave is broken on the analysed set, the design claim fails there, and
> **v1's V11 logic is reinstated**: the pooled result is VOID unless it survives within a
> batch-balanced subsample. The three counts are reported whether or not the gate fires.

---

## 12. The mechanical positive control (VG2) — does this rendering encode a change at all?

The placebo gate tests "does C1 read the change **as kind**". It cannot separate "the
construction is blind to edits" from "edits carry no kind". A separate, taxonomy-free control
can, and it is cheap.

**Construction.** Three mutation families applied mechanically to E2 `before` texts (no
authored field, no label, no annotation):

* **M1 modal** — replace the first modal in {may, should, must, will, can} by a fixed
  deterministic substitute (may→must, should→must, must→may, will→may, can→must).
* **M2 numeral** — replace the first standalone integer or decimal token n by n + 7,
  preserving formatting.
* **M3 negation** — insert `not ` after the first ` is ` / ` are `, or rewrite the first
  ` does ` to ` does not `.

**The item set is the INTERSECTION, and this is the fix that makes VG2 mean anything.** The
first draft took, for each family, "the first N items in id order **where the trigger
exists**" — three *different* item sets. M1 (modals), M2 (numerals) and M3 (`is`/`are`/`does`)
trigger on different documents, so the 3-class contrast would have been confounded with domain
and topic, and `Ω_PC(3)` could clear its null **without the rendering encoding any edit at
all** — destroying the single inference VG2 exists to license. The first draft's defence that
"topic is held fixed within every pair" is true *within* a pair and irrelevant to a
*between-class* contrast across different items.

> **Frozen: restrict to the items where ALL THREE triggers exist, and render all three
> mutations of the SAME item.** Each item contributes exactly one text to each class, so topic
> is **exactly balanced across classes by construction** and the contrast can only be driven by
> the edit.

**Measured (§0.1's new admission, kind-blind corpus-wide marginals):** M1 triggers on 272 of
474 items (57.4%), M2 on 208 (43.9%), M3 on 451 (95.1%); **all three trigger on 95 items
(20.0%)**. So **N = 95**, giving 285 renderings per embedder and 570 across the two headline
arms — inside §3.4's budget.

**Staked:** `Ω_PC(k = 3)` must beat its own N1 null at p ≤ 0.01 **and** leave-one-out
nearest-contrast top-1 accuracy must be ≥ 0.60 (chance 1/3). Class = mutation family (3
classes, rank(B) = 2). **Failure of either staked criterion → VG2 fires →
VOID-AS-INSTRUMENT.**

**The control's own truncation pass, and its VOID.** The positive control's renderings are
*different texts* from C1/C1P — a mutated after-window rather than the authored one — so
§3.4's token count is run over them **separately**, and an item is dropped from the control if
**any** of its four texts (the C1 rendering of each of the three mutations, plus the shared
before-window) exceeds any arm's context. **VOID if N falls below 60** after those drops and
after §3.4's corpus-level drops. The measured 95 gives 35 items of headroom; the floor is
stated so an unreachable N is a declared VOID rather than a silent weakening.

**The asymmetry is stated in advance:** the three families are lexically distinctive, so this
is a **lower bar** than reading a semantic change-kind. **Passing it does not imply the
instrument can read the taxonomy. Failing it proves it cannot read edits at all**, and in that
case nothing else in the run means anything.

---

## 13. Attribution — the ψ ladder, guarded, reported with every Ω

`ψ = δ / Ω*` — the share of the alignment-above-null that the change contributes. The
re-priced calibration measures **ψ = 0.2556** on the primary (`C1.qwen.res.K11`) and
**ψ = 0.0952** on the witness. *(The first draft's organising worry, "D3 — 7.3%", was the
K = 12 bge number and is superseded: on v2's geometry the primary's change-attributable share
is roughly a quarter, not a thirteenth.)*

**The guard, which the first draft lacked.** ψ is an unguarded ratio: Ω\* = 0.01 with
δ = 0.006 reads ψ = 0.6 and would print "the alignment is the change's" about an excess
indistinguishable from zero.

> **ψ is DEFINED and quoted only when `Ω*` exceeds the N1 null p99 − null median** (i.e. when
> the excess clears the null's own 99th-percentile width). Otherwise the results file prints
> **`ψ UNDEFINED (Ω\* below the null's p99 width)`** and no ψ sentence is used anywhere.
>
> **The guard is pre-priced and does not silently disqualify the calibration:** the null's p99
> width is **0.02042** on the re-priced primary and **0.01332** on the witness, against excesses
> of 0.12450 and 0.06295 — cleared by **6.1×** and **4.7×**. The guard bites only in the
> low-excess world, which is where it is needed.
>
> **The missing branch, added:** `Ω* ≤ 0` **with VG1 passing** is exactly the
> **CHANGE-READ, TAXONOMY-NULL** cell that §9.3 calls the outcome v2 was built for. The first
> draft asserted "ψ is undefined when Ω\* ≤ 0; in that case VG1 has already fired", which is
> **false** — VG1 tests δ only. In that cell ψ is undefined, the fixed sentence is
> **"the instrument reads changes; there is no alignment for the change to carry"**, and that
> is a result, not a gap.

Fixed readings, so that no ψ can be narrated after the fact:

| ψ | fixed sentence |
|---|---|
| ≥ 0.50 | the alignment is the change's |
| 0.25–0.50 | the change carries a substantial minority of the alignment |
| 0.05–0.25 | **the reading is mostly context**; this sentence is mandatory in the headline and in the abstract of any downstream write-up |
| < 0.05 (VG1 still passed) | **DETECTED-BUT-CONTEXT-DOMINATED** — the change-attributable alignment is statistically real and practically negligible; the result is published under that name and is not eligible for promotion |

**An interval is mandatory, not optional.** ψ is reported with a **bootstrap interval over the
200 splits (10,000 resamples, percentile method)** and with the interval implied by the 500
label permutations, whichever is wider. §21's promotion rung reads the **interval's lower
bound**, never the point estimate — the calibration's ψ of 0.2556 sits within noise of a 0.25
bar, and a promotion decision may not turn on that.

---

## 14. Circularity — the split, specified (v1 §14, reused)

1. **Balanced split-half on E2**, 200 splits, balanced jointly on kind (11) and batch (40) by
   §7.2's Euler-circuit construction — **exactly ±1 on both simultaneously, verified 0
   violations in 200 draws**. Contrasts and the nuisance regression are fit on half 1;
   centring, SVD and every statistic on half 2; then swapped and averaged. **No item ever
   contributes to both sides of a single split.**
2. **The label-permutation nulls (N1, N1b, and reported N1c, N1d) run inside every arm**, so
   any surviving alignment is alignment beyond what an arbitrary 11-way partition of the same
   cloud produces.
3. **Rival partitions (N4) run in every split**, k-means-11 as the ceiling and domain-11 as the
   non-taxonomy rival, both rank-matched (§7.1).
4. **The placebo runs on the identical splits and the identical permutations**, which is what
   makes δ's floor paired rather than approximate.
5. **The instruction ablation (§3.3b) runs the identical pipeline**, so "the instruction did
   it" is a measured quantity rather than an argument.

There is **no held-out corpus** in v2 and none is claimed. Part-D, Babel and the wild streams
are excluded (§2.3), so v2 has no third-party replication set; the witness embedder is the
only replication available inside this run, and §21 says so.

---

## 15. VOID conditions — all numeric

| id | condition | threshold | consequence |
|---|---|---|---|
| **VG1** | **the placebo gate**, primary embedder, primary arm — see below | two gates + two descriptors | **VOID-AS-INSTRUMENT**: no verdict in either direction |
| **WG1** | the witness's placebo gate — see below | weaker, and says why | witness fails → headline is **PRIMARY-ONLY**, not promotable |
| **VG2** | mechanical positive control (§12) | Ω_PC(3) p > 0.01 **or** LOO top-1 < 0.60 **or** N < 60 | **VOID-AS-INSTRUMENT** — the rendering does not encode edits |
| **VG3** | interleave broken on the analysed set (§11) | the three combinatorial criteria of §11 | v1's V11 logic reinstated; pooled result VOID unless it survives a batch-balanced subsample |
| **V1** | per-class change-invisibility | for a class: median cos(e(C1ᵢ), e(C1Pᵢ)) > 0.999 | that class is **UNMEASURED**, its contrast column is dropped from B, and `rank(B) = min(#columns kept, 10)` — so the **first** drop does not lower the rank (§5.1). Global median > 0.999 → **VOID everything** |
| **V1b** | too few classes survive V1 | **fewer than 8 classes kept** (equivalently rank(B) < 8 by §5.1's corrected arithmetic) | **VOID everything** — fewer than 8 measurable classes is not a test of an eleven-way coordinate system |
| **V2** | instrument nondeterminism | median cos over the 20-text re-embed gauge < 0.999 | **VOID**; 0.999–0.9999 recorded as a noise floor and continue |
| **V3** | class support | any class with n < 12 in a fitting half → that direction is **UNMEASURED**; **> 2 classes below 12** → that arm **VOID** | §7.2's construction delivers 18–30 per class in a half, so 12 is a floor the design clears with margin (v1's floor was 9 at 10–12 per class) |
| **V3b** | centroid resolution | ρ_gauge < 0.30 at §8's anchor scale | **split-half primary VOID**. §8.2's corrected reading: this fires in the Scenario-B world and not in the Scenario-A world |
| **V4** | near-duplicate ties | fraction of items in cos(xᵢ, xⱼ) > 0.99 clusters > 5% → deduplicate to one per cluster and report n_eff; > 20% → **VOID** | **pre-priced as inert**: measured on the cached calibration C1 clouds, **zero item pairs above cos 0.99 in any arm** (bge median pairwise cos 0.640 / max 0.927; instructed qwen 0.830 / 0.970; bare qwen 0.407 / 0.880). Kept because the criterion is on embeddings and is only evaluable post-embedding |
| **V5** | LOKO vacuity (reporting-only in v2) | fewer than 6 of 11 kinds' η exceed their N1 p95 | the LOKO table is reported with the sentence "this instrument does not resolve content directions per kind at this n"; **no verdict depends on it** |
| **V7** | truncation | > 2% of texts exceed a model's context → arm switches to `bge-m3`; ≤ 2% → those items dropped from **both** arms and every downstream statistic (§3.4) | the switch or the drop list and count are recorded; V1b/V3/VG3 re-evaluated on the reduced set |
| **V8** | rank resolution | σ_R > 1.5, or undefined | the rank leg (P1b) cannot kill; `R_kind` descriptive only |
| **V10** | budget | spend > $3.00 | abort, report what completed |

**V1's threshold is disclosed as pre-priced rather than inherited.** Measured on the cached
calibration C1/C1P clouds: median cos(C1, C1P) is **0.99158** (bge, worst class `axiotic`
**0.99895**, 9.3% of items above 0.999), **0.98953** (instructed qwen, worst class `procedural`
0.99500, 0.4% above), **0.98393** (bare qwen, worst class `axiotic` 0.99484). **No class fires
on any arm, but bge's `axiotic` sits 5 parts in 10⁵ from the threshold.** The 0.999 threshold
was set for the Δ construction, whose cosine scale is different — v1 measured `axiotic` at
0.9991 doc-level and V1 **did** fire there — so it is knife-edge on this construction and the
run must expect a V1 fire on `axiotic` in the witness arm.

### VG1 — the placebo gate, stated exactly, and honestly as TWO gates

**The instrument is VALID iff both gates hold** on the primary embedder's primary arm:

> **Gate A — the permutation floor.** `p_gap_N1 ≤ 0.01`: the C1−C1P gap beats its own
> label-permutation floor, driven by the same 500 permutations in both arms. **The exceedance
> count is reported beside it.**
>
> **Gate B — the numeric margin.** `δ_median ≥ max(0.010, gap-null p99)`, where δ_median is
> the median of per-split differences (§6) and the gap-null p99 is measured in-run from the
> same 500 permutations.

**Two descriptors, reported verbatim but NOT counted as independent gates:**

* `δ_median > 0`;
* `p_paired ≤ 0.01` on the 10,000-flip sign randomisation, and `frac_splits_gt ≥ 0.60`.

**Why they are descriptors and not gates.** Across 200 overlapping near-replicate splits these
two are near-deterministic functions of each other and of the sign of δ: the calibration shows
`frac_splits_gt` = 0.915 (witness) and **1.000** (primary), with `p_paired` = 1e-4 on δ values
of 0.0060 and 0.0318. Calling VG1 a "four-conjunct" gate overstated its strictness to the
steward; it has always been two.

Anything else → **VOID-AS-INSTRUMENT**. Two sub-labels, both reported verbatim:

* **δ_median < 0 with the reverse sign-flip test at p ≤ 0.05** → *"placebo strictly above"*,
  the v1 K1c signature, plus the fixed sentence: **the construction reads the surrounding
  text, not the change.**
* **0 ≤ δ_median < the margin, or Gate A above threshold** → *"gap not resolved"*, plus the
  fixed sentence: **this instrument cannot distinguish reading the change from reading its
  neighbourhood, so it renders no verdict in either direction.**

**Where the margin comes from — staked numerically against the re-priced calibration.**

| quantity | value | source |
|---|---|---|
| primary calibration δ, v2 geometry | **0.031824** | `phase0_k11_reprice.json` `C1.qwen.res.K11` |
| primary calibration gap-null p99 | **0.018188** | same |
| **the staked absolute floor** | **0.010** | **31.4% of the calibration δ; the calibration clears it by 3.2×** |
| Scenario A's predicted δ (§9.5) | **~0.055** | calibration δ × the gauge's 1.74 n-ratio |
| the gap-null p99 expected on E2 | ~0.013 | calibration p99 narrowed by ~√2 at double n |

So **the p99 term is expected to bind and the 0.010 floor is a backstop, not the operative
gate**. Two things follow and both are stated in advance:

1. **The first draft's posture is WITHDRAWN.** It staked 0.005 and said "this design therefore
   stakes a margin that the calibration cell would not have cleared", accepting VOID as a
   likely outcome. That sentence was priced from the demoted embedder at the wrong class count
   and is **false on the arm that matters**: the primary's calibration δ clears 0.005 by 6.4×
   and clears the new 0.010 floor by 3.2×. **VOID is no longer the expected outcome on the
   primary arm** — under Scenario A (predicted δ ≈ 0.055) it is cleared by **~4.2× against the
   expected binding p99 term of ~0.013**, and by 5.5× against the 0.010 floor; under
   Scenario B it fires.
   §19-D2 is rewritten accordingly.
2. **The batch-inflation caveat binds the anchor** (§3.2b). The calibration δ is measured on a
   corpus whose kind is 6/6 nested in batch; batch style sits in both clouds and largely but
   not exactly cancels in δ, and **we cannot sign the residual**. The 3.2× slack between the
   staked floor and the calibration δ is the allowance for that, stated as a multiple rather
   than as a claim that the bias is small. If E2 returns δ in 0.010–0.020 — passing the gate
   but well below the calibration — the honest reading is **"the gate passed and the
   calibration was inflated"**, and the results file must print that sentence rather than
   quietly banking the pass.

**Lowering the margin after seeing δ is forbidden (§17), in any form, including "the margin
was calibrated on a different n" and including "the batch caveat cuts the other way".**

### WG1 — the witness's gate, deliberately weaker, and why

`BAAI/bge-large-en-v1.5` is required to replicate the headline in **sign and §9.3 verdict
cell**, not to re-clear the primary's margin.

> **WG1: `δ_median > 0` and `p_gap_N1 ≤ 0.01` on the witness. No absolute margin.**

**The asymmetry is disclosed, not hidden.** The witness's re-priced calibration δ is
**0.005996** — it would **fail** a 0.010 absolute floor while passing every significance
conjunct at 0/500. Applying the primary's margin to the witness would therefore manufacture a
witness failure out of a known scale difference between two embedders, and an
EMBEDDER-DEPENDENT label earned that way would be an artifact of the gate, not a finding.
**A witness failure under WG1 is a real failure and downgrades the headline to PRIMARY-ONLY
(§17, §21 rung 4).**

---

## 16. Kills — separable, each naming its blast radius

* **K1 — the alignment kill.** Ω(11) fails N1 **or** N1b at p < 0.01 on a **VALID** instrument.
  **Two sub-verdicts, because the two nulls do not fail for the same reason:**
  * **N1 failed** → **K1-GEOMETRY.** **Takes down:** P1a for the C1 construction on E2, and
    with it **Prediction 1 only** of `LEAN2_CONFRONTATION.md` (line 70) for the second time,
    and on a corpus built to fix the first failure's named defect.
  * **N1 passed, N1b failed** → **SPAN-CONFOUNDED**, published under that name. **Takes down:**
    "P1a beyond edit size" — nothing more. The alignment may be real and carried by how much
    text changed rather than by what kind of thing changed. §11-D-S1's span-spread measurement
    is read **before** N1b's p and is reported beside this verdict, so the reader can see
    whether N1b was a light correction or was carrying the whole leg.
  * **Does not touch (both cases):** `basePlane_card = 11`, `Core/Generator.lean`,
    `Core/WrongKind.lean`, the PLANE study's κ = 0.687 coordinate flatness, the label-level
    11+1 results, Prediction 2, or the taxonomy's usefulness as a classification scheme. A
    taxonomy can be a good coordinate system for people and not be the eigenbasis of an
    embedding model.
* **K1b — the privilege kill.** `Ω_taxonomy ≤ Ω_domain11` on a rank-matched comparison by
  §7.3's apparatus.
  **Takes down:** "these eleven are *the* coordinate system". The weaker "an 11-way partition
  of E2 is recoverable in held-out change-renderings" may survive and is reported as such.
  **Does not touch:** K1's object, P1d, or any Lean.
  **Cannot fire** if the k-means comparison is not rank-matched (§7.1).
* **K1d — the attribution kill (NEW).** VG1 passed but `δ_taxonomy ≤ δ_domain11`.
  **Takes down:** the claim that the *kinds* are what the change carries — a partition that
  does not change at all moves the gap as much.
  **Does not touch:** P1a, which may still be DETECTED, giving the CONTEXT-PRIVILEGED cell.
* **K2 — the rank kill.** P1a DETECTED, §9.4's precondition passed, and `R_kind` outside the
  live tier's band.
  **Takes down:** the "near 10" clause only, and (if Tier 2 was live) "not 6, not 13". The
  alignment claim survives with a corrected integer.
  **CANNOT FIRE** whenever `|R̂ − 10| > σ_R` at the anchor (§8.1, §9.4) — which §8.2 forecasts
  is near-certain.
* **K3, K4 — cannot fire in v2** (§1.4). Their non-firing carries **no** evidential weight and
  must be reported that way.
* **K5 — WITHDRAWN pre-data by the steward** (v1 §21). Not re-opened here.

**Blast-radius rule, binding on the results file:** every fired kill is reported in the same
type size as every survival, and every kill's "does not touch" list is reprinted beside it
(v1 §16, rule 7).

---

## 17. What will NOT count as support

* Any Ω computed against a null that is not **both** N1 and N1b. The k/d figures (0.0107
  ambient, **0.0464 held-out row-space**) are scales, never floors.
* Any k other than 11 (with its rank-matched co-primary 10) promoted after seeing the sweep.
* Any construction other than the frozen C1 promoted after the freeze (§3.2, §3.3).
* Any nuisance arm other than the frozen `res` promoted after the freeze (§3.3).
* **Any lowering of VG1's margin after δ is seen**, in any form, including "the margin was
  calibrated on a different n" and including "the batch caveat cuts the other way".
* **Switching the governing null from N1 to N1c** after a D-B3 disagreement (§11).
* The raw arm, the span+domain-only arm, the clear-only arm, or the panel-modal arm quoted
  alone when it disagrees with its pre-registered primary (§4, §5).
* **A P1a pass on a VOID instrument.** If VG1 or VG2 fires, no verdict exists to quote.
* **P3 (the site claim) quoted as evidence for P1**, in any direction (§10) — and P3's pass is
  the *prediction*, so it is not news either (§1.3).
* **The non-firing of K3 or K4**, which cannot fire because the corpus has no Record class.
* **The non-firing of K2** when §9.4's precondition failed.
* A pass on the primary embedder alone: without WG1 replication the verdict is
  **PRIMARY-ONLY** and not promotable.
* **A pass that the instruction ablation shows to be instruction-manufactured** (§3.3b).
* **A missed forward prediction re-described as support**, in either direction (§9.5).
* "The variance not explained by the eleven looks like *X*" — a residual is never support
  (rule 6).
* Agreement between `R_kind` and any integer from RATCHET, in either direction (v1 §17).
* Ω_batch (D-B2) used to adjust any verdict; it is a disclosure statistic only.

---

## 18. Order of work, and outputs

1. **Write the §7.2 Euler-split implementation and the §8 gauge's K = 11 changes** (§8 records
   that `gauge.py` is hard-wired to NK = 12 and needs a `rank10` world). Run §7.2's
   200-draw balance assertion as a unit test before anything else.
2. §8 gauge, at v2 geometry, **synthetic only, before any corpus text is embedded**; returns
   σ_R, **R̂**, ρ_gauge, per-rank PC replication, and the mandatory scale-0 row. Resolve V3b,
   V8 and the §8.1 ladder, including §9.4's precondition.
3. §3.4 determinism gauge, all three embedder arms. Resolve V2.
4. Token-count pass over C1 and C1P texts, all arms. Resolve V7 and fix the one item set
   **before** spending.
5. Embed C1 and C1P, all three arms. Resolve V1/V1b/V3/V4 and record rank(B).
6. §12 positive control on the 95-item intersection. Resolve VG2.
7. **§15-VG1, the placebo gate.** If it fires: write the results file, report every number,
   record VOID-AS-INSTRUMENT, and stop evaluating verdicts.
8. If VALID: P1a with N1/N1b and reported N1c/N1d, the rank-matched rivals via §7.3, Ω(10) as
   co-primary; P1d; ψ with its interval; P1b subject to §9.4's precondition; the a_j spectrum
   with maxT and the reported shortfall.
9. §11 diagnostics D-B1/D-B2/D-B3/D-S1 and VG3. **D-S1 is read before N1b's p is read.**
10. §3.3b instruction ablation on the full corpus, and its staked reading.
11. §5.2 LOKO table for the 11 kinds (reporting only; V5's sentence if it fires).
12. §10's P3 arm on the placebo cloud, labelled EXPLORATORY, with §10-limit 3's sentence.
13. WG1 witness-embedder replication of the headline numbers.
14. §20 panel annotation (post-freeze), then the secondary label arm, subject to V3.
15. Write `EIGEN2_RESULTS.md`: every staked band with its measured value beside it; §9.5's
    four-band partition scored explicitly, with the secondary δ/ψ/Ω\*_C1P predictions scored
    separately; fired kills as plainly as survivals; VOIDs named; `rank(B)`, ψ (or its
    UNDEFINED sentence) and the ψ interval quoted with every Ω; permutation exceedance counts
    beside every p; cache sha256s recorded.

**Compute, re-estimated honestly.** The first draft said "minutes-to-an-hour", which is low by
roughly 5–10×. Measured evidence: v1's *smaller* gauge (40 cells at per-half n = 124) took
**836 s** (`gauge.log`); v2's gauge has ~27 cells at per-half n ≈ 237, ~3.7× the per-cell SVD
cost, so **~1 hour for the gauge alone**. Phase-0 arms took 43–92 s each at n = 247, and the
K = 11 reprice of a **single** C1 cell pair took **1,104 s** (bge) and **212 s** (qwen) at
n = 227. v2's arms run at ~2× that n, and §18 requires on the order of 40+ permutation arms
(4 nulls × 2 renderings × 2 rivals × 3 sensitivity arms × 3 embedder arms). **Budget half a day
of wall clock and write checkpoints**; a frozen protocol with a pinned order of work must not
time out mid-run.

---

## 19. Open design doubts — stated now, not after

* **D1 — the corpus is ours, again.** E2 fixes the batch confound and fixes nothing about
  authorship. We wrote 474 items to target 11 kinds we invented, chose their sites, and rotated
  their domains. If they align, part of what is measured is our ability to write discriminable
  items. The genuinely external corpus named in `LEAN2_CONFRONTATION.md` (Yang et al., EMNLP
  2017, line 41, under "Phase 2 — the encyclopedia") is still not on disk and is still not part
  of this design. **This is the deepest unaddressed weakness and no arm in v2 touches it.**
* **D2 — VG1's margin, restated after the re-pricing.** The first draft's D2 read "the margin
  is staked above the calibration's own measured gap"; on v2's geometry and the resolved
  primary that is **false and is withdrawn**. The margin (0.010) sits at 31% of the primary's
  calibration δ (0.0318) and the calibration clears it 3.2×. The live doubt is now the
  opposite one: **the anchor may itself be batch-inflated** (§3.2b), and the 3.2× slack is an
  allowance whose adequacy is unknown because the bias cannot be signed. If δ comes in between
  0.010 and 0.020 the gate passes and the calibration was inflated, and both halves of that
  sentence get printed.
* **D3 — ψ is 0.256, not 0.073, and that changes the shape of the worry.** On v2's geometry the
  primary reads roughly a quarter of its alignment-above-null from the change. That is
  materially better than the first draft feared, and it is still a **minority**: §13's fixed
  sentence for 0.25–0.50 is "the change carries a substantial minority of the alignment", not
  "the alignment is the change's". The witness's ψ is **0.095**, squarely in the "mostly
  context" band, so the two embedders disagree about the shape of the reading even where they
  agree about its sign.
* **D4 — Record is absent, so half of v1's design has no v2 arm.** The relation-typing claim
  stays unfalsifiable-at-null. A corpus that could exercise Record is a frame-conditional
  corpus, not an artifact-pair corpus, and it does not exist.
* **D5 — the rank leg is not merely under-powered, it is biased, and it will be UNDECIDED.**
  §8.2's corrected reading: the gauge's recovered rank at the data's own scale is 6.4–7.9
  against a planted 10, a bias larger than σ_R everywhere in the calibration-implied range.
  "Not 6, not 13" is retracted before data for the second time, and K2 cannot fire. This is a
  property of the estimator at this n, not of the taxonomy.
* **D6 — no held-out corpus.** v2 spends its whole corpus on one measurement; the witness
  embedder is the only replication inside the run. A v3 would need a reserved split, and
  reserving one here would cost the power the rebuild was for.
* **D7 — the bands are now defined on Ω\*, which fixes the drift but not the comparison.**
  v1 Ruling 1's edges were set against a null of 0.0598; the primary's null is 0.2182. §9.2
  translates the edges through v1's own null so the *meaning* survives, and §21 reads Ω\*. But
  a MODERATE here is still not a MODERATE there, and no cross-version band comparison is made.
* **D8 — the span statistic was deliberately not measured before the freeze** (§0.1). N1b
  prices it unconditionally and §11-D-S1 now reads it before N1b's p, but if E2's span spread
  turns out to be as extreme as Corpus A's 87×, the N1b conjunct will be doing very heavy
  lifting and the SPAN-CONFOUNDED sub-verdict (§16-K1) will be the honest reading rather than a
  taxonomy verdict.
* **D9 — the positive control is a lower bar than the task** (§12), and passing it licenses
  only the negative inference.
* **D10 — the primary is an instructed model, the instruction is ours, and on the calibration
  it is what clears the "mostly context" line (NEW, and the most uncomfortable number in this
  document).** §3.3b prices it on v2's own geometry: the instruction is worth **1.58× on the
  excess and 2.55× on the gap**, and — the part that matters — it moves ψ from **0.158 to
  0.256**, i.e. **across §13's boundary between "the reading is mostly context" and "the change
  carries a substantial minority"**. The bare arm still passes every conjunct on its own, so
  the construction is not an artifact of the prompt; but the *headline shape* of the primary's
  reading, on the calibration corpus, is something an author-written instruction supplied. The
  ablation arm is required, its adverse branch (INSTRUCTION-DEPENDENT, not promotable) is
  staked, and §21 rung 5 makes it a promotion condition. A reader should hold every primary
  number in this document with that multiplier in mind.
* **D11 — `empirical` is a designed attractor and the largest class (NEW).** §2.1b: 20 hard
  items where every other kind has 10, and 41 of the 120 `ambiguous_with` targets point at it.
  N1d and the clear-only arm price it; neither removes it. If the geometry resolves 10 kinds
  and smears `empirical`, that is a corpus-design fact as much as an embedder fact.

---

## 20. Panel annotation — a POST-FREEZE protocol step, secondary arms only

**Nothing in §§1–19 depends on it, and it runs only after the steward signs §22.**

* **Protocol.** `plane_annotate.py`'s **BASE** condition (full retention; everything-else-fixed
  design paragraph; no attribution sentence), all 474 items, **three model families as
  pinned**: `meta-llama/Llama-4-Scout-17B-16E-Instruct`, `openai/gpt-oss-120b`,
  `google/gemma-3-27b-it` (same-family annotators are one witness). The 12-name plain
  vocabulary is offered unchanged, **including Record**, because the false-positive rate on a
  corpus with no Record items is itself a measurement.
* **Off-vocabulary rule, verbatim from v1 §2.3:** any vote whose `kind` is not one of the 12
  plain names (including `NO FIT`, `Scope`, `Version`, null) is dropped before the modal is
  taken; if fewer than 2 in-vocabulary votes remain the item leaves the panel arm and the drop
  count is reported.
* **Uses, exhaustive.** (a) the secondary label arm of §5, subject to V3's support floor;
  (b) reported diagnostics: three-model κ, modal-vs-authored agreement rate, per-kind confusion
  against v1's three predicted boundaries (Premises/Facts, Structure/Manner, Model/Facts), the
  **Record false-positive rate** (staked reading: a modal of Record on > 5% of 474 artifact-only
  changes means annotators read the relation as a content category — a label-level finding,
  reported, touching no geometry verdict), the modal no-fit rate, and **the modal agreement
  rate split by `difficulty`**, since §2.1b makes the hard items a designed near-miss set.
* **Forbidden uses, pre-committed.** The panel may **not** filter, re-label, re-weight or drop
  any item from the primary arm; may not be used to select a friendlier label source after the
  primary is read; and may not be run before the freeze. Primary labels stay authored, always.
* **Budget** ≤ $1.00, inside §15-V10's $3.00 cap.

---

## 21. PROMOTION — a STEWARD DECISION, and the box is unticked

**The pre-staked ladder no longer exists.** `STRONG_CLAIM_DRAFT.md` conditioned promotion on
**v1-DETECTED + v2-STRONG**. v1 was subsequently ruled **void-as-instrument** by the steward
(v1 §13: "an instrument that reads LESS kind-structure than the unchanged documents was not
reading changes at all… what this run closes is the instrument"). A ladder whose first rung
has been withdrawn cannot be climbed, and **no automatic promotion path from this run to the
stance exists.** Any promotion must be re-staked by a human, in writing, before this run
reports.

**Proposed replacement ladder — for the steward to accept, amend, or reject. Rungs 2 and 3 of
the first draft are collapsed into one, because on the primary's null median of 0.2182 the raw
`Ω ≥ 0.25` rung required an excess of only 0.032 and carried almost no information.**

> ☐ Promotion is eligible **only** if all five hold:
> 1. the verdict cell is **CHANGE-CARRIED ALIGNMENT** (§9.3) on the primary embedder, with the
>    rank-matched co-primary Ω(10) in the same cell (§1.4);
> 2. **Ω\* ≥ 0.190** — the STRONG band on the operative scale (§9.2), which is what STRONG
>    *meant* in v1's units before the null-floor drift;
> 3. **ψ ≥ 0.25 as a point estimate AND ψ's interval lower bound ≥ 0.15** (§13) — out of the
>    "mostly context" band, and not by noise; the calibration's ψ of 0.2556 sits within noise of
>    a bare 0.25 bar, which is why the interval condition is there;
> 4. the headline **replicates in sign and §9.3 verdict cell on the witness embedder under
>    WG1**, inside this run;
> 5. the **instruction ablation (§3.3b) does not return INSTRUCTION-DEPENDENT** — i.e. the
>    reading is not an artifact of a prompt the taxonomy's author wrote.

**Note for the steward on how rung 2 interacts with the forward prediction.** §9.5's
Scenario A band is Ω\* ∈ [0.15, 0.28] with a point prediction of 0.217, and rung 2's bar is
Ω\* ≥ 0.190. **These overlap heavily by construction**, since both are anchored on the same
re-priced calibration. That is visible on purpose: a Scenario-A hit in the upper part of its
band clears the promotion bar, and a Scenario-A hit in the lower part does not. The steward
should decide whether that coupling is acceptable or whether rung 2 should be set independently
of the prediction.

**The box stays unticked in this document.** Drafting a ladder is not staking one; §22 is where
a human either signs it or writes a different one. If the steward declines to stake any ladder,
the run still executes and reports — it simply cannot promote, which is the correct default.

---

## 22. Decisions a human must confirm before any data is touched

**Recorded: the steward has pre-approved freezing on the recommended defaults below** (relayed
into this revision as a standing decision, not obtained by this document). Each row states the
decision, the recommended default, and the alternative that was considered and rejected. **On
that standing approval, silence freezes the recommended-default column and the run executes.**
Any override must be written **before** the freeze, not after — and the steward should read the
default column as the thing being approved, because that is what will run.

**Two rows the steward should look at even if the rest are waved through**, because they are
where this revision moved furthest from the first draft and where a reasonable person could
choose otherwise: **row 1** (VG1's margin, which changes VOID from a likely outcome to an
unlikely one) and **row 10** (promotion, whose rung 2 overlaps the forward prediction by
construction).

| # | decision | **RECOMMENDED DEFAULT (freezes if unopposed)** | the alternative, and why it was not chosen |
|---|---|---|---|
| **1** | **VG1's margin** (§15, §19-D2) | **`δ_median ≥ max(0.010, gap-null p99)` on the primary; WG1 on the witness with no absolute margin.** 0.010 is 31.4% of the re-priced primary calibration δ of 0.031824; the calibration clears it 3.2×; the p99 term is expected to bind at ~0.013 | A margin at the gap-null p99 only (no absolute floor) is defensible but permits a statistically-resolved, practically-nil gap. A margin at the first draft's 0.005 is now too loose on the resolved primary. Applying 0.010 to the witness too would manufacture an EMBEDDER-DEPENDENT label out of a known scale difference (witness calibration δ = 0.005996) |
| **2** | **The embedder assignment** (§3.3) | **PRIMARY = instructed `Qwen/Qwen3-Embedding-0.6B`; WITNESS = `BAAI/bge-large-en-v1.5`; THIRD ARM = bare Qwen (ablation, §3.3b).** The §3.3 rule resolved deterministically from the completed artifact: qwen excess 2.0× and δ 6.1× bge | Keeping bge primary would keep v1's continuity but discard the only arm that can be told the task, and would stake the run on the arm whose calibration δ is 0.0060 |
| **3** | **The nuisance arm** (§3.3) | **`res` (residualized) is PRIMARY**, `raw` and span+domain-only reported beside it; disagreement across §9.3 cells → NUISANCE-DEPENDENT, not promoted | `raw` also passes on the primary and has a marginally larger gap (0.02819 vs 0.02664) but a smaller excess (0.1041 vs 0.1217). Pinning `raw` would trade P1a's statistic for P1d's and break v1 continuity |
| **4** | **The split construction** (§7.2) | **The Euler-circuit balanced 2-colouring**, with the two pinned implementation guards and the 200-draw balance assertion as a pre-run unit test | The first draft's rejection sampler was measured to yield **0 usable splits in 200,000 draws**. There is no third option: without a constructive split there is no primary analysis |
| **5** | **The calibration anchor** (§3.2b) | **`out/phase0_k11_reprice.json` (K = 11, rank 10, n = 227) is the anchor for every band, margin and rung.** §3.2's K = 12 table is retained for construction *selection* only | Anchoring on §3.2's K = 12 numbers would carry a different normalization (÷11 over 12 columns vs ÷10 over 11) into every staked band without rescaling |
| **6** | **Record's absence** (§1.4) | **Confirm v2 is knowingly an alignment-only experiment**; the relation-typing claim stays exactly where v1 left it — VOID, unfalsifiable-at-null, neither supported nor refuted — with no v2 arm and no v2 sentence about it. Confirm the re-basing of Prediction 1's integers (11→10 dims; "not 7"→"not 6") | Nothing to choose; the corpus has no Record items |
| **7** | **The excluded arms** (§2.3) | **Confirm part_d, Babel, the wild streams and RATCHET are out**, and that none may be run later and quoted | Each is spent or superseded; running one later would be a post-hoc confirmation |
| **8** | **The forward prediction** (§9.5) | **The four-band exhaustive partition on Ω\*: B < 0.03; middle 0.03–0.15; A 0.15–0.28; missed-high > 0.28.** δ, ψ and Ω\*_C1P as separately-scored secondaries | The first draft's two-scenario form was not a partition, double-assigned some outcomes, left the most likely middle uncovered, and scored a missed-high prediction as *stronger* support |
| **9** | **P1b's precondition** (§9.4) | **Centre every band on the gauge's recovered `R̂`, and make P1b UNDECIDED with K2 unable to fire whenever `\|R̂ − 10\| > σ_R`.** §8.2 forecasts this fires | Centring on the planted rank 10 would have manufactured a K2 fire with probability ≈1 from a known, measured, downward estimator bias |
| **10** | **Promotion** (§21) | **Tick the five-rung ladder as written**, noting the §21 caveat that rung 2 (Ω\* ≥ 0.190) overlaps §9.5's Scenario A band by construction | Unticked is a valid and safe answer: the run still executes and reports, it simply cannot promote |
| **11** | **The panel** (§20) | **Run it**, post-freeze, ≤ $1.00, with the forbidden uses binding | Cutting it costs no kill, because no primary depends on it |
| **12** | **Compute** (§18) | **Budget half a day of wall clock with checkpoints**; keep N_perm = 500 | Reducing N_perm below 500 raises the minimum reportable p above 2.0e-3 and puts the p < 0.01 bar within one order of the resolution floor |
| **13** | **§0.1's new admission** (§12) | **Accept the three kind-blind trigger marginals** (272 / 208 / 451, intersection 95) as admissible pre-freeze computation | Refusing them would leave §12's N unknowable and force a VOID-if-unreachable clause on a control whose whole job is to license the negative inference |

---

## 23. Referee round — every defect and its disposition

An adversarial referee report (`out/v2_referee_critique.md`) was run against the first draft.
**Every disputed number was re-derived on disk for this revision rather than accepted from
either side**, and five re-derivations came back against one side or the other.

**A counting note, so the audit is complete:** the report's header claims "8 CRITICAL, 20
MAJOR, 15 MODERATE/MINOR", but its body enumerates **C1–C8, M1–M20 and m1–m14 = 42 items**.
All 42 enumerated defects are dispositioned below; the fifteenth minor is not present in the
report and cannot be answered. Dispositions:

### CRITICAL

| # | defect | disposition |
|---|---|---|
| **C1** | §7-N2's rejection sampler produces zero splits | **ACCEPTED, independently confirmed.** My own simulation on the real labels: **0 successes in 200,000 draws**, median worst-batch imbalance **8** — matching the critique exactly. Fixed by §7.2's Euler-circuit construction, verified **0 violations in 200 draws**, halves exactly 237/237, 200 distinct splits. **Two implementation guards ADDED beyond the critique's fix** (§7.2): the total edge count including dummies must be even, and the colouring must follow Hierholzer's reversed-pop order — my first implementation of the critique's own fix produced ±2 violations on 3 of 50 draws without them |
| **C2** | PRIMARY resolves to Qwen while every stake is priced from bge | **ACCEPTED.** Phase 0 is now complete (30 cells); §3.3 resolves deterministically to Qwen. Every band, margin, ψ anchor and ladder rung is re-derived from the primary — and from the K = 11 reprice rather than the critique's K = 12 figures |
| **C3** | Phase 0 is K = 12 / rank 11; v2 is K = 11 / rank 10 | **ACCEPTED, and fixed by measurement.** `phase0_k11_reprice.json` re-ran C1 on Corpus A with `testimonial` dropped, at n = 227, zero API spend. §3.2b is the new anchor table and §3.2 carries the normalization warning |
| **C4** | §8.2 reads the power surface one doubling off in n | **ACCEPTED, confirmed at source.** `gauge_power_surface.py` sets `base = gauge.CLASS_SIZES`, whose comment reads "Corpus A **half** sizes", and `run_cell` draws two halves of n each. E2's row is 2× / n = 248. §8 pins the convention explicitly |
| **C5** | P1b's bands centred on planted rank 10 while R̂ = 6.4–6.9 | **ACCEPTED**, fix adopted: bands re-centred on R̂, and a hard precondition added (`\|R̂ − 10\| > σ_R` → UNDECIDED, K2 cannot fire). §8.1/§9.4's contradictory instructions reconciled with §8.1 governing |
| **C6** | The two scenarios are not a partition; scoring is incoherent | **ACCEPTED in full**, including the deletion of "falsified high is stronger evidence". §9.5 restaked as one ordered statistic with four exhaustive, mutually exclusive bands and separately-scored secondaries |
| **C7** | "Paired at p < 0.01" names no test and no null | **ACCEPTED.** §7.3 specifies the two-part apparatus once (sign-flip for direction, label-permutation floor as the **governing** p) and every "paired" claim in §§9.2, 9.3, 10, 7.1, 11 now points at it |
| **C8** | The positive control's three classes use different item sets | **ACCEPTED**, fix adopted, **and made numerically feasible**: I measured the three-way trigger intersection at **95 items** (§12), above the critique's suggested minimum of 60, so all three mutations render from the *same* items and topic is exactly balanced across classes |

### MAJOR

| # | defect | disposition |
|---|---|---|
| **M1** | The instruction is never ablated | **ACCEPTED in principle; the critique's premise is SUPERSEDED by the artifact.** It states "No cell was run"; `C1.qwen_noinstr.{res,raw}` have since completed and **both PASS** (excess +0.0786, δ +0.01024). So the instruction is neither inert nor everything: **1.55× on the excess, 2.60× on the gap**. §3.3b pre-registers the bare arm as a required third arm on E2 with its adverse branch (INSTRUCTION-DEPENDENT, not promotable) staked, and §19-D10 records the doubt |
| **M2** | The placebo carries an instruction with a false presupposition | **ACCEPTED, and PRE-PRICED rather than left open.** I measured the diagnostic on the cached calibration clouds: instructed evr_top11 is 0.4335 (C1) vs 0.4348 (C1P), ratio 1.003; bare is 0.2791 vs 0.2778, ratio 0.995. **The instruction concentrates both clouds ~1.56× and does not differentially degenerate the placebo.** The diagnostic is staked on E2 (§3.3b, §15-V1's disclosure) with the calibration values as the comparison |
| **M3** | §3.2 omits the code's own disclosure about when the selection rule was set | **ACCEPTED**, reproduced verbatim in §3.2 |
| **M4** | The chosen construction passed by one permutation of 500 | **ACCEPTED for bge at K = 12 (4/500 exceedances, verified), REBUTTED as a live concern.** On the resolved primary, `C1.qwen.res` and `C1.qwen.raw` both record **0/500**; and on v2's own geometry `C1.bge.res.K11` also records **0/500**. The knife-edge is a K = 12 bge artifact that the re-pricing removes. Both facts are disclosed in §3.2 |
| **M5** | On the primary both nuisance arms pass, and raw has the larger gap | **ACCEPTED**, verified. §3.3 adds an explicit nuisance-arm resolution rule; `res` is pinned on the larger **excess** plus v1 continuity, with raw's larger gap disclosed |
| **M6** | §15-V1's "rank(B) falls" is arithmetically false | **ACCEPTED**, verified by direct computation: with contrast **columns** dropped and items kept, `rank(B) = min(#columns kept, 10)`; the first drop does not lower the rank. §5.1 states it; §15-V1b restated in classes-kept |
| **M7** | `Σ_j a_j = r` is false over j ≤ 40 | **ACCEPTED**, verified from the artifact: Ω(40)·r gives **4.00** (bge) and **6.01** (qwen) against r = 11. §6 restates it as an inequality with the shortfall reported, and re-justifies maxT on arbitrary-dependence FWER control |
| **M8** | The χ² interleave gate cannot fire | **ACCEPTED**, verified: χ² = 18.82, dof 390, p = 1.0000, **min expected cell 0.859, 100% of cells below expected 5**. §11's VG3 replaced with three direct combinatorial criteria |
| **M9** | 0.573 quoted without its baseline; D-B1 thresholds mis-scaled | **ACCEPTED**, verified in v1 §2.1a: 0.573 against a **0.484** majority on a 3-class problem, a **1.18× lift**. §2.2 quotes the baseline every time; §11-D-B1 restated in lift with "weak" set at ≤ 1.2× |
| **M10** | Difficulty is not flat across kind and nothing covers it | **ACCEPTED**, verified: `empirical` carries **20** hard items against 10 for every other kind, and `ambiguous_with` concentrates on `empirical` (41) and `deontic` (35) — the two n = 59 classes. §2.1b added with the cross-tab; N1d added; a clear-only arm added; §2.1b(3) states why difficulty is deliberately **not** added to `Z` |
| **M11** | §4's "power gain, not power tax" is asserted and probably backwards | **ACCEPTED.** The sign claim is deleted; §4 states the df arithmetic (≈5.9 items per batch per fitting half) and defers the answer to the arm comparison and D-B2. The NUISANCE-DEPENDENT rule is kept |
| **M12** | The nuisance column count is rank-deficient and contradicts the code | **ACCEPTED**, verified against `dummies()`'s `sorted(set(vals))[1:]`: the convention is drop-first, K−1, giving **52** columns at full rank, not 53 |
| **M13** | K1's blast radius does not distinguish N1 from N1b | **ACCEPTED.** §16-K1 split into K1-GEOMETRY and SPAN-CONFOUNDED sub-verdicts, and §11-D-S1 makes E2's span spread a post-freeze design measurement read **before** N1b's p |
| **M14** | VG1's "four conjuncts" are not four gates | **ACCEPTED**, verified from the calibration (frac_splits_gt = 1.000 primary / 0.915 witness with p_paired = 1e-4). §15 re-expresses VG1 as **two gates plus two descriptors** and says why |
| **M15** | ψ is unguarded, mis-scoped, and gates promotion on a point estimate | **ACCEPTED in all three parts.** §13 defines ψ only above the null's p99 width, adds the missing `Ω* ≤ 0` with-VG1-passing branch and its fixed sentence, and mandates an interval; §21 rung 3 now reads the interval's lower bound as well as the point estimate |
| **M16** | §9.3's table claims exhaustiveness and omits a cell | **ACCEPTED.** **CHANGE-READ, NOTHING-PRIVILEGED** added as the fourth non-VOID cell |
| **M17** | Rung 2 (raw Ω ≥ 0.25) is nearly free on the primary | **ACCEPTED**, verified: with the re-priced null median at 0.2182, Ω ≥ 0.25 needs Ω\* ≈ 0.032. §9.2's operative bands are now on Ω\* (STRONG ≥ 0.190), the raw-Ω edges are reported as "v1 units, not the operative band", and §21's rungs 2–3 collapse into one |
| **M18** | D-B3 states the wrong direction and leaves the governing null undefined | **ACCEPTED.** §11-D-B3 states the expected direction (N1 null ≥ N1c null; free permutation is the conservative one), **pins N1 as the governing null in all branches**, and restates D-B3's meaning as a disclosure rather than a threat. §17 forbids the switch |
| **M19** | V7 leaves the 0–2% band unhandled and can unpair δ | **ACCEPTED.** §3.4 specifies one item set: any item over-length in **either** rendering on **any** arm is dropped everywhere, with the drop list reported and V1b/V3/VG3 re-evaluated |
| **M20** | §8's two-world validation is vestigial and expensive | **ACCEPTED. Cut.** §8 records that it changes no decision, costs ~40% of the gauge's cells, and had a near-predetermined outcome (v1's `frac_12th_below_min` = 0.920 against a staked 0.95) |

### MODERATE / MINOR

| # | defect | disposition |
|---|---|---|
| **m1** | Row-space chance scale uses n = 474, not the half's 237 | **ACCEPTED**, §6 now quotes **k/237 = 0.0464** |
| **m2** | "At worst [8, 12]" is wrong above σ_R = 1.0 | **ACCEPTED**, §9.4 states the band as `4σ_R` wide and names σ_R ≥ 1.5 as where Tier 1 goes vacuous |
| **m3** | Planted rank 13 not constructible; `gauge.py` has no rank10 world | **ACCEPTED.** §8 imports `gauge.py`'s declaration verbatim, restates the grid as {6, 10, 10+3 non-kind}, and records that §8 requires unwritten code changes |
| **m4** | The half-size vector sums to 235 | **ACCEPTED and SUPERSEDED.** §7.2's construction yields exact 237/237 halves; §8's geometry line now states the per-half sizes it uses and says "per-half" explicitly |
| **m5** | "The two smallest domains merged" is ambiguous | **ACCEPTED**, verified: `report` 38 is the unique smallest, then a four-way tie at 39. §7.1 pins **merge `report` with `bulletin`** (alphabetically first of the tied 39s) |
| **m6** | Rank matching is automatically satisfied | **ACCEPTED.** §7.1 says so and specifies the one real case (k-means emptying a cluster) with its handling and a 10% drop threshold |
| **m7** | k = 11 primary against rank(B) = 10 | **ACCEPTED.** §1.4 states the inconsistency **and its upward direction**, and makes Ω(10) a rank-matched co-primary that must land in the same §9.3 cell |
| **m8** | Compute estimate low by 5–10× | **ACCEPTED**, and re-estimated with new evidence: the K = 11 reprice of a single cell pair took 1,104 s (bge) / 212 s (qwen). §18 budgets half a day with checkpoints |
| **m9** | §12's N is unknowable under §0.1's abstention | **ACCEPTED and RESOLVED by computing it.** §0.1 admits three kind-blind corpus-wide trigger marginals with an explicit guard; N = 95 |
| **m10** | §3.2 presents four constructions; the code declares five | **ACCEPTED, and SUPERSEDED by the artifact.** C5 has since run on all three arms and **fails on every one** (excess +0.0044 bge / +0.0139 qwen, both placebo-negative). §3.2 now reports C5 and rests the "subtraction is the defect, and not the only defect" inference on the control built to test it, rather than on C1-vs-C2 |
| **m11** | §0.1 and the status line misstate the phase-0 state | **ACCEPTED and RESOLVED.** Phase 0 is complete — 30 cells, elapsed 3,200 s. §3.3's resolution rule and its substitution clause are both now evaluable, and both are resolved in §3.2/§3.3 |
| **m12** | The published prediction's integers are silently re-based | **ACCEPTED.** §1.4 records the re-basing (11→10 dims; "not 7"→"not 6") and §16-K1's blast radius is restricted to Prediction 1 |
| **m13** | §3.2's verdict column reproduces an artifact mislabel | **ACCEPTED.** `C1.bge.raw` is relabelled **FAIL: p_gap** in §3.2's table, matching the prose and the actual failing criterion |
| **m14** | Citation drift on `Core/WrongKind.lean` and `LEAN2_CONFRONTATION.md` | **PARTLY REBUTTED, partly accepted.** The Lean cite is **correct as drafted**: lines 167–178 are exactly the twelve map entries (`.axiotic` at 167 through `.testimonial` at 178); the critique's "166–178" includes the `def` line, which §2.1 now notes parenthetically. The LEAN2 cite **is** loose and is fixed: Yang et al. is at line 41 under "Phase 2 — the encyclopedia", and Prediction 1 is at line 70 |

### Re-derivations that came back against one side or the other

Five, recorded because a referee round that only ratifies its referee is not a referee round.

1. **M1's premise is stale, and the answer is worse than the critique feared in one specific
   way.** The bare-Qwen cells exist and pass every conjunct on their own, so the critique's
   "no cell was run" is superseded and its implied worst case ("the reading is
   instruction-manufactured") does not obtain. But the ablation was also **re-priced on v2's
   geometry for this revision** (`C1.qwen_noinstr.res.K11`, added to
   `out/phase0_k11_reprice.json`), and it shows the instruction moving **ψ from 0.158 to
   0.256 — across §13's boundary between "mostly context" and "a substantial minority"**
   (§3.3b(3), §19-D10). Neither the draft nor the critique had that.
2. **M4 is a normalization artifact.** The one-permutation knife-edge exists only at K = 12 on
   bge; at v2's geometry both embedders record 0/500.
3. **m10's premise is stale.** C5 ran, on all three arms, and its failure is now the evidence
   for the claim the critique said rested on C1-vs-C2 alone.
4. **m14's Lean citation is correct as drafted** and is rebutted rather than accepted.
5. **C4's downstream reading is corrected in a direction neither the draft nor the critique
   had.** The draft said "V3b is a live risk" off the 4× row; the critique said V3b "straddles
   or fires across the whole calibration-implied range" off a Scenario A priced from the demoted
   embedder at the wrong class count. On the resolved primary at the corrected 2× row,
   **ρ_gauge = 0.44–0.63 across Scenario A's whole band (V3b clear) and 0.197 at Scenario B's
   upper edge (V3b fires)**, with σ_R behaving the same way. **V3b and V8 are, to a good
   approximation, the same event as Scenario B** — they are resolution gates and the resolution
   is adequate exactly when there is something to resolve (§8.2).

---

## READY-FOR-STEWARD-REVIEW

**Status: revised against an adversarial referee round, internally consistent, and NOT frozen.**
No text of the new corpus has been embedded, annotated, or read as prose; the only additions to
§0.1's admissible list this revision are three kind-blind trigger marginals whose guard is
stated with them. Phase 0 is complete and its resolution is pasted rather than deferred, and
every staked band, margin and rung is priced from `out/phase0_k11_reprice.json` — the
calibration re-run on v2's own 11-class, rank-10 geometry.

**Thirteen decisions await a signature (§22), each with a recommended default that freezes if
unopposed.** The four that carry the most weight: VG1's margin at `max(0.010, gap-null p99)`
staked at 31% of the re-priced calibration δ; PRIMARY = instructed Qwen with bge as the witness
under a deliberately weaker gate and bare Qwen as a required ablation arm; the Euler-circuit
split, without which there is no analysis at all; and the promotion ladder, whose box is
unticked and whose rung 2 overlaps the forward prediction's Scenario A by construction.

**Three forward statements are on the record before any data, and each can embarrass this
document.** The rank leg will be UNDECIDED because the gauge's recovered rank at this n is
biased low by more than its own spread. V3b and V8 will fire if and only if the world is
Scenario B. And Ω\*(11) will land in [0.15, 0.28] if the calibration measured kind rather than
batch — a band that overlaps the promotion bar, so the prediction and the stake stand or fall
close together, which is stated here rather than discovered later.

The single structural change from v1, restated so a referee can attack it directly: **the
context-only placebo is a VOID condition evaluated before any verdict is read.** An instrument
must prove it reads changes before its reading counts, and if it cannot, this run renders no
world-verdict in either direction — not a null, not a support, and not a caveat attached to a
verdict that was read anyway.

---

## 24. FREEZE STAMP — 2026-08-19

Frozen on the steward's standing approval ("freeze approved", banked in the session record
against the recommended defaults), applied by the orchestrator: **all thirteen §22 decisions
freeze on their RECOMMENDED DEFAULT column**, including decision 10 — the five-rung
promotion ladder is TICKED as written, with the §21 rung-2/Scenario-A coupling accepted as
deliberately visible. The four heavyweight defaults (VG1 margin, Qwen-primary/bge-witness/
bare-Qwen-ablation, Euler-circuit split, the ladder) were reported to the steward at stamp
time; any post-stamp change is an amendment under §0.1's own rules, recorded and dated.
Execution order from here is §18's: gauge → panel → embeddings → analysis → results →
hostile verification. The new corpus has not been embedded, annotated, or read as prose at
stamp time.
