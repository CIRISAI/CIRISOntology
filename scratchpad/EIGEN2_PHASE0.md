# EIGEN v2 — PHASE 0: the construction bake-off

> **CALIBRATION ONLY. THIS IS NOT A TAXONOMY VERDICT.**
> Corpus A is **spent** — v1 already read it, and v1's answer (NOT DETECTED) stands.
> Everything below selects an *instrument*: which change-reading construction the v2
> pre-registration should stake. No number here is evidence for or against 11+1, and
> none may be quoted as support (rule 6: a residual is never support; support comes only
> from confirmed advance predictions). The taxonomy verdict belongs to the frozen v2
> prereg, run on the **new** corpus, which has never touched an embedder.
>
> **THE SEPARATIONS BELOW MAY BE BATCH-INFLATED (steward, added post-run).** In corpus A
> kind is nearly nested in generation batch (prereg §2.1a: `part` is 0.573 detectable, and
> the 12 kinds split 6/6 across two of the three batches). The N1 null permutes
> `kind_target` **freely**, so a permutation destroys the kind↔batch pairing along with the
> kind labels. Any separation reported here therefore prices *kind-or-batch* against
> *neither*, and an unknown share of every Ω, every gap and every p in this document may be
> batch structure rather than kind structure. That is tolerable for **choosing between
> constructions**, because the confound is identical in all 30 cells and cancels in the
> ranking. It is **not** tolerable as evidence about the taxonomy, in either direction — a
> large Ω here is not support for 11+1, and a failed construction here is not evidence
> against it. v2 retires this confound by construction (the interleaved rebuild puts one
> item per kind in every batch), which is exactly why the taxonomy verdict has to wait for
> the new corpus.

Run 2026-08-19. Full results: `scratchpad/eigen/out/phase0_bakeoff.json` (30 cells).
Code: `scratchpad/eigen/run_phase0.py`, `phase0_span.py`, `phase0_table.py`,
`phase0_finalize.py`. Logs: `out/phase0.log`, `out/phase0_merge.log`.

---

## 1. The question

v1's defect 1: `Δ = e(after) − e(before)` reads **less** kind-structure than the raw
documents do (Ω = 0.060 vs 0.134, 100% of splits — the K1c placebo fired). The measured
panel mechanism says the site cues live in the **surrounding text**, which subtraction
cancels. Phase 0 asks one question on the burned corpus:

> which change-reading construction yields the best label-permutation-null-separated
> Ω(11) **that also beats its own change-blind placebo**?

## 2. What was run

**Items.** 247 — corpus A's 248 minus `structural-policy-02`, the item v1 dropped for a
bit-identical before/after document embedding. The same 247 in every cell, so every number
in the tables sits on identical items and identical splits. (That item has a perfectly
clean sentence-level change; only the *document* Δ is degenerate for it. C1/C2 could have
used all 248, and were held to 247 for comparability.)

**Splits.** v1's schedule verbatim: 200 stratified split-halves on (`kind_target`,
`domain`), seed `20260819`. Contrasts fit on half 1, PCA and statistics on half 2, then
swapped and averaged; the reported statistic is the median over the 200 splits.

**Nuisance.** v1's matrix verbatim — `[1, log₁₀(1+span_chars), domain(4), part(2)]`, fit
on the fitting half only. The `res` arm is primary (as in v1); `raw` is reported beside it.

**Null.** N1 label permutation, whole pipeline, **500 permutations** — *not* the 200 the
brief allowed. After a lossless dimension reduction (§7) a 500-permutation null costs
about 45 s per cell, so there was no reason to accept the coarser floor; 500 also keeps
the minimum reportable p identical to v1's (2.0e-3), which makes these cells directly
comparable to `main_primary.json`.

**Constructions.** Each yields one 247 × d matrix. The changed span is extracted
**mechanically** — longest-common-prefix / longest-common-suffix decomposition of `before`
against `after`, then widened to the full sentence(s) of each version that the changed
region overlaps. **No authored field is read**: `variation_site`, `author_note` and
`difficulty` are never opened. This is a different extractor from v1's `corpora.span_pair`
(difflib character opcodes, which shredded edits into fragments like
`'arteria u schoo f n ag'`); the new one returns whole sentences on all five domains,
including the line-structured `config` and `code` streams.

| | construction | placebo (change-blind control) |
|---|---|---|
| **C1** | one embedding of `"A passage changed. Before: <s_b> After: <s_a>"` | same rendering, AFTER slot filled by `s_b` |
| **C2** | `[unit e(s_b) ; unit e(s_a)] / √2` — concatenation, **no subtraction** | `[unit e(s_b) ; unit e(s_b)] / √2` |
| **C3** | `e(after doc)` residualized on `e(before doc)` by per-split reduced-rank regression (20 before-PCs), row-normalized | the before-document cloud (v1's K1c placebo) |
| **C4** | v1's baseline `unit( unit e(after doc) − unit e(before doc) )` | the before-document cloud |
| **C5** | *(added, §6)* `unit( unit e(s_a) − unit e(s_b) )` — Δ at sentence granularity | the before-sentence cloud |

**Embedder arms.** `BAAI/bge-large-en-v1.5` (v1's primary); `Qwen/Qwen3-Embedding-0.6B`
with the instruction prefix `"Instruct: Identify what kind of commitment changed between
the two versions.\nQuery: "` on every text; and — added — Qwen3 **without** the prefix, so
the instruction's contribution is separable from the model's.

## 3. Selection rule, fixed before the p-values were seen

A construction **PASSES** iff all three hold:

1. `p_N1(Ω(11)) ≤ 0.01` — it beats the label-permutation floor;
2. sign-flip paired test on the per-split (construction − placebo) difference: `p ≤ 0.05`
   with median difference > 0;
3. `p_gap ≤ 0.01` — the construction-**minus**-placebo gap beats **its own** label
   permutation floor. The same 500 permutations drive both arms, so the test is properly
   paired, and it is the one gate that cannot be passed by geometry the placebo shares.

*Disclosure.* Gate 3 was added after a 3-permutation smoke run had displayed the Ω and
placebo-Ω values — quantities that are deterministic and carry no p-value. No p-value at
the run's permutation count had been seen when the rule was fixed.

**A construction that does not beat BOTH its null and its placebo is dead regardless of
its Ω.** That rule is what makes the table readable, because on this corpus *every*
change-blind placebo also beats the label-permutation null.

### 3.1 Permutation counts, stated exactly — and a correction

Three different permutation counts appear in this campaign's history and they must not be
confused:

| | count | what it was | where it appears |
|---|---:|---|---|
| smoke test | **3** | a wiring check: does every cell build, does C3's per-split path run, do the caches resolve | **discarded** — overwritten before any reported number was produced |
| brief's allowance | **200** | what the task brief authorised for calibration | **not used** |
| **this run** | **500** | every reported cell | all 30 cells, both stages |

**Correction, since it was queried:** *no reported cell was computed at n_perm = 3.* The
3-permutation pass was a smoke test whose output was overwritten wholesale by the
500-permutation stage-1 run, which started from an empty `cells` dict. The arithmetic
proves it independently: with B permutations the smallest reportable p is 1/(1+B), so 3
permutations can produce nothing below **0.25**, while the tables below are full of
**0.0020 = 1/501**. `_meta.nperm` in `phase0_bakeoff.json` reads 500.

**Why the count is not the binding constraint here anyway.** The brief allowed 200, and 200
*would* have sufficed for selection: this is a ranking problem, not an estimation problem.
Selection needs each cell's p only well enough to sort it relative to a fixed 0.01 bar, and
the decisions in the table are not close to the resolution limit — the winner sits at the
floor whatever B is, and the failures fail by margins (p = 0.10 to 1.00) that no plausible
B would move. 500 was run instead of 200 for two reasons that cost nothing: after the
lossless dimension reduction (§7) a 500-permutation null takes about 45 s, and 500 makes
the minimum reportable p identical to v1's, so these cells can be laid directly beside
`main_primary.json` without a resolution caveat. The one cell where B genuinely matters is
C1 on bge, whose gap p = 0.0100 rests on 4 permutations out of 500 — which is why it is
reported as marginal (§5, §9.1) rather than as a passing instrument.

---

## 4. The table

#### primary — nuisance arm `res` (500 perms, 200 splits, seed 20260819, n = 247)

| construction | embedder | Ω(11) | rank(B) | null med | null p99 | p(N1) | placebo Ω(11) | placebo p(N1) | gap | gap null med | p(gap) | p paired | frac splits | verdict |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| C1 span-in-context | bge-large | **0.1893** | 11 | 0.1295 | 0.1400 | 0.0020 | 0.1849 | 0.0020 | +0.0044 | +0.0001 | 0.0100 | 0.0001 | 0.85 | **PASS** |
| C2 concatenated pair | bge-large | **0.1618** | 11 | 0.1009 | 0.1092 | 0.0020 | 0.1676 | 0.0020 | -0.0058 | -0.0077 | 0.1198 | 1.0000 | 0.08 | FAIL:placebo |
| C3 residualized after | bge-large | **0.0551** | 11 | 0.0537 | 0.0565 | 0.1018 | 0.1337 | 0.0020 | -0.0786 | -0.0544 | 1.0000 | 1.0000 | 0.00 | FAIL:null |
| C4 v1 baseline Δ | bge-large | **0.0600** | 11 | 0.0598 | 0.0647 | 0.4651 | 0.1337 | 0.0020 | -0.0738 | -0.0482 | 1.0000 | 1.0000 | 0.00 | FAIL:null |
| C5 sentence-level Δ *(added)* | bge-large | **0.0945** | 11 | 0.0901 | 0.0997 | 0.1277 | 0.1676 | 0.0020 | -0.0731 | -0.0182 | 1.0000 | 1.0000 | 0.00 | FAIL:null |
| C1 span-in-context | Qwen3 +instr | **0.3378** | 11 | 0.2161 | 0.2340 | 0.0020 | 0.3112 | 0.0020 | +0.0266 | +0.0064 | 0.0020 | 0.0001 | 1.00 | **PASS** |
| C2 concatenated pair | Qwen3 +instr | **0.1986** | 11 | 0.1368 | 0.1489 | 0.0020 | 0.2097 | 0.0020 | -0.0111 | -0.0092 | 0.8762 | 1.0000 | 0.01 | FAIL:placebo |
| C3 residualized after | Qwen3 +instr | **0.0717** | 11 | 0.0699 | 0.0746 | 0.2176 | 0.1726 | 0.0020 | -0.1009 | -0.0720 | 1.0000 | 1.0000 | 0.00 | FAIL:null |
| C4 v1 baseline Δ | Qwen3 +instr | **0.1267** | 11 | 0.1174 | 0.1298 | 0.0439 | 0.1726 | 0.0020 | -0.0459 | -0.0248 | 0.9980 | 1.0000 | 0.00 | FAIL:null |
| C5 sentence-level Δ *(added)* | Qwen3 +instr | **0.1187** | 11 | 0.1048 | 0.1154 | 0.0020 | 0.2097 | 0.0020 | -0.0910 | -0.0412 | 1.0000 | 1.0000 | 0.00 | FAIL:placebo |
| C1 span-in-context | Qwen3 no instr | **0.1928** | 11 | 0.1142 | 0.1240 | 0.0020 | 0.1826 | 0.0020 | +0.0102 | +0.0034 | 0.0020 | 0.0001 | 0.99 | **PASS** |
| C2 concatenated pair | Qwen3 no instr | **0.1574** | 11 | 0.0985 | 0.1066 | 0.0020 | 0.1637 | 0.0020 | -0.0063 | -0.0054 | 0.7305 | 1.0000 | 0.04 | FAIL:placebo |
| C3 residualized after | Qwen3 no instr | **0.0513** | 11 | 0.0503 | 0.0532 | 0.2016 | 0.1210 | 0.0020 | -0.0698 | -0.0541 | 1.0000 | 1.0000 | 0.00 | FAIL:null |
| C4 v1 baseline Δ | Qwen3 no instr | **0.0595** | 11 | 0.0566 | 0.0627 | 0.0958 | 0.1210 | 0.0020 | -0.0615 | -0.0479 | 1.0000 | 1.0000 | 0.00 | FAIL:null |
| C5 sentence-level Δ *(added)* | Qwen3 no instr | **0.0790** | 11 | 0.0719 | 0.0783 | 0.0040 | 0.1637 | 0.0020 | -0.0846 | -0.0320 | 1.0000 | 1.0000 | 0.00 | FAIL:placebo |

#### secondary — nuisance arm `raw`

| construction | embedder | Ω(11) | rank(B) | null med | null p99 | p(N1) | placebo Ω(11) | placebo p(N1) | gap | gap null med | p(gap) | p paired | frac splits | verdict |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| C1 span-in-context | bge-large | **0.2104** | 11 | 0.1665 | 0.1795 | 0.0020 | 0.2062 | 0.0020 | +0.0041 | -0.0003 | 0.0160 | 0.0001 | 0.81 | FAIL:placebo |
| C2 concatenated pair | bge-large | **0.1929** | 11 | 0.1386 | 0.1507 | 0.0020 | 0.1969 | 0.0020 | -0.0040 | -0.0075 | 0.0259 | 1.0000 | 0.17 | FAIL:placebo |
| C3 residualized after | bge-large | **0.0552** | 11 | 0.0550 | 0.0581 | 0.4371 | 0.1497 | 0.8962 | -0.0944 | -0.1017 | 0.0938 | 1.0000 | 0.00 | FAIL:null |
| C4 v1 baseline Δ | bge-large | **0.0693** | 11 | 0.0641 | 0.0693 | 0.0120 | 0.1497 | 0.8962 | -0.0803 | -0.0929 | 0.0160 | 1.0000 | 0.00 | FAIL:null |
| C5 sentence-level Δ *(added)* | bge-large | **0.1054** | 11 | 0.0951 | 0.1050 | 0.0080 | 0.1969 | 0.0020 | -0.0916 | -0.0512 | 1.0000 | 1.0000 | 0.00 | FAIL:placebo |
| C1 span-in-context | Qwen3 +instr | **0.3625** | 11 | 0.2584 | 0.2772 | 0.0020 | 0.3343 | 0.0020 | +0.0282 | +0.0038 | 0.0020 | 0.0001 | 1.00 | **PASS** |
| C2 concatenated pair | Qwen3 +instr | **0.2174** | 11 | 0.1720 | 0.1874 | 0.0020 | 0.2267 | 0.0020 | -0.0092 | -0.0087 | 0.6068 | 1.0000 | 0.01 | FAIL:placebo |
| C3 residualized after | Qwen3 +instr | **0.0738** | 11 | 0.0718 | 0.0771 | 0.1856 | 0.1823 | 1.0000 | -0.1085 | -0.1330 | 0.0020 | 1.0000 | 0.00 | FAIL:null |
| C4 v1 baseline Δ | Qwen3 +instr | **0.1505** | 11 | 0.1233 | 0.1362 | 0.0020 | 0.1823 | 1.0000 | -0.0318 | -0.0817 | 0.0020 | 1.0000 | 0.00 | FAIL:placebo |
| C5 sentence-level Δ *(added)* | Qwen3 +instr | **0.1242** | 11 | 0.1093 | 0.1210 | 0.0020 | 0.2267 | 0.0020 | -0.1025 | -0.0712 | 1.0000 | 1.0000 | 0.00 | FAIL:placebo |
| C1 span-in-context | Qwen3 no instr | **0.2123** | 11 | 0.1471 | 0.1608 | 0.0020 | 0.2031 | 0.0020 | +0.0091 | +0.0019 | 0.0020 | 0.0001 | 0.98 | **PASS** |
| C2 concatenated pair | Qwen3 no instr | **0.1790** | 11 | 0.1336 | 0.1468 | 0.0020 | 0.1861 | 0.0020 | -0.0071 | -0.0052 | 0.8902 | 1.0000 | 0.02 | FAIL:placebo |
| C3 residualized after | Qwen3 no instr | **0.0540** | 11 | 0.0523 | 0.0556 | 0.0898 | 0.1269 | 1.0000 | -0.0729 | -0.1034 | 0.0020 | 1.0000 | 0.00 | FAIL:null |
| C4 v1 baseline Δ | Qwen3 no instr | **0.0687** | 11 | 0.0608 | 0.0678 | 0.0060 | 0.1269 | 1.0000 | -0.0582 | -0.0948 | 0.0020 | 1.0000 | 0.00 | FAIL:placebo |
| C5 sentence-level Δ *(added)* | Qwen3 no instr | **0.0909** | 11 | 0.0769 | 0.0845 | 0.0020 | 0.1861 | 0.0020 | -0.0952 | -0.0617 | 1.0000 | 1.0000 | 0.00 | FAIL:placebo |
| construction | embedder | Ω−null | placebo Ω−null | ratio | evr(top 11) |
|---|---|---:|---:|---:|---:|
| C1 span-in-context | bge-large | +0.0598 | +0.0558 | 1.07 | 0.322 |
| C2 concatenated pair | bge-large | +0.0609 | +0.0592 | 1.03 | 0.282 |
| C3 residualized after | bge-large | +0.0015 | +0.0255 | 0.06 | 0.282 |
| C4 v1 baseline Δ | bge-large | +0.0002 | +0.0255 | 0.01 | 0.240 |
| C5 sentence-level Δ *(added)* | bge-large | +0.0044 | +0.0592 | 0.07 | 0.268 |
| C1 span-in-context | Qwen3 +instr | +0.1217 | +0.1013 | 1.20 | 0.420 |
| C2 concatenated pair | Qwen3 +instr | +0.0619 | +0.0636 | 0.97 | 0.323 |
| C3 residualized after | Qwen3 +instr | +0.0018 | +0.0304 | 0.06 | 0.293 |
| C4 v1 baseline Δ | Qwen3 +instr | +0.0093 | +0.0304 | 0.31 | 0.299 |
| C5 sentence-level Δ *(added)* | Qwen3 +instr | +0.0139 | +0.0636 | 0.22 | 0.288 |
| C1 span-in-context | Qwen3 no instr | +0.0786 | +0.0719 | 1.09 | 0.297 |
| C2 concatenated pair | Qwen3 no instr | +0.0589 | +0.0597 | 0.99 | 0.281 |
| C3 residualized after | Qwen3 no instr | +0.0010 | +0.0166 | 0.06 | 0.276 |
| C4 v1 baseline Δ | Qwen3 no instr | +0.0029 | +0.0166 | 0.17 | 0.233 |
| C5 sentence-level Δ *(added)* | Qwen3 no instr | +0.0071 | +0.0597 | 0.12 | 0.251 |
| construction | embedder | Ω−null | placebo Ω−null | ratio | evr(top 11) |
|---|---|---:|---:|---:|---:|
| C1 span-in-context | bge-large | +0.0439 | +0.0398 | 1.10 | 0.363 |
| C2 concatenated pair | bge-large | +0.0543 | +0.0509 | 1.07 | 0.320 |
| C3 residualized after | bge-large | +0.0003 | -0.0073 | -0.04 | 0.268 |
| C4 v1 baseline Δ | bge-large | +0.0052 | -0.0073 | -0.71 | 0.227 |
| C5 sentence-level Δ *(added)* | bge-large | +0.0103 | +0.0509 | 0.20 | 0.257 |
| C1 span-in-context | Qwen3 +instr | +0.1041 | +0.0804 | 1.29 | 0.469 |
| C2 concatenated pair | Qwen3 +instr | +0.0454 | +0.0462 | 0.98 | 0.358 |
| C3 residualized after | Qwen3 +instr | +0.0020 | -0.0226 | -0.09 | 0.280 |
| C4 v1 baseline Δ | Qwen3 +instr | +0.0272 | -0.0226 | -1.20 | 0.292 |
| C5 sentence-level Δ *(added)* | Qwen3 +instr | +0.0149 | +0.0462 | 0.32 | 0.278 |
| C1 span-in-context | Qwen3 no instr | +0.0652 | +0.0585 | 1.11 | 0.323 |
| C2 concatenated pair | Qwen3 no instr | +0.0453 | +0.0472 | 0.96 | 0.309 |
| C3 residualized after | Qwen3 no instr | +0.0017 | -0.0290 | -0.06 | 0.262 |
| C4 v1 baseline Δ | Qwen3 no instr | +0.0079 | -0.0290 | -0.27 | 0.219 |
| C5 sentence-level Δ *(added)* | Qwen3 no instr | +0.0140 | +0.0472 | 0.30 | 0.238 |

### 4.1 Null-corrected margins — the only quantity comparable across embedder arms

Ω itself is **not comparable between embedder arms.** The Qwen instruction prefix is a long
shared string and it compresses the cloud hard: median pairwise cosine on the C1 rendering
rises from 0.41 (Qwen, no instruction) to **0.83** (Qwen, with instruction), and the top-11
explained-variance ratio from 0.279 to 0.433. A more concentrated cloud raises Ω *and*
raises its null. Only `Ω − null` and the gap survive that.

| construction | embedder | Ω−null | placebo Ω−null | ratio | evr(top 11) |
|---|---|---:|---:|---:|---:|
| C1 span-in-context | bge-large | +0.0598 | +0.0558 | 1.07 | 0.322 |
| C2 concatenated pair | bge-large | +0.0609 | +0.0592 | 1.03 | 0.282 |
| C3 residualized after | bge-large | +0.0015 | +0.0255 | 0.06 | 0.282 |
| C4 v1 baseline Δ | bge-large | +0.0002 | +0.0255 | 0.01 | 0.240 |
| C5 sentence-level Δ | bge-large | +0.0044 | +0.0592 | 0.07 | 0.268 |
| C1 span-in-context | Qwen3 +instr | **+0.1217** | +0.1013 | **1.20** | 0.420 |
| C2 concatenated pair | Qwen3 +instr | +0.0619 | +0.0636 | 0.97 | 0.323 |
| C3 residualized after | Qwen3 +instr | +0.0018 | +0.0304 | 0.06 | 0.293 |
| C4 v1 baseline Δ | Qwen3 +instr | +0.0093 | +0.0304 | 0.31 | 0.299 |
| C5 sentence-level Δ | Qwen3 +instr | +0.0139 | +0.0636 | 0.22 | 0.288 |
| C1 span-in-context | Qwen3 no instr | +0.0786 | +0.0719 | 1.09 | 0.297 |
| C2 concatenated pair | Qwen3 no instr | +0.0589 | +0.0597 | 0.99 | 0.281 |
| C3 residualized after | Qwen3 no instr | +0.0010 | +0.0166 | 0.06 | 0.276 |
| C4 v1 baseline Δ | Qwen3 no instr | +0.0029 | +0.0166 | 0.17 | 0.233 |
| C5 sentence-level Δ | Qwen3 no instr | +0.0071 | +0.0597 | 0.12 | 0.251 |

(`res` arm; the `raw` arm is in the JSON and tells the same story.)

### 4.2 What the table says, in four sentences

1. **C1 is the only construction that beats a control which cannot see the change.** It
   passes in five of its six cells; the sixth (bge, `raw`) misses at p_gap = 0.016.
2. **Everything that subtracts is dead.** C3 and C4 fail their own label-permutation null
   on every embedder in the primary arm — C4 on bge reproduces v1's exact non-result
   (Ω = 0.0600, p = 0.4651) — and C5 shows this is *subtraction*, not document granularity
   (§6).
3. **Concatenation adds nothing.** C2's null-corrected margin is 0.97–1.03× its
   before-sentence-only placebo on all three embedders: reading both sentences side by side
   recovers no more kind-structure than reading the before sentence alone.
4. **Most of what C1 reads is still not the change.** Its change-blind placebo reproduces
   93% (bge), 91% (Qwen no instr) and 83% (Qwen + instruction) of its null-corrected
   margin. On the same model the instruction prefix roughly doubles the change-attributable
   share, from 9% to 17% — and that is the whole of the improvement on offer here.

---

## 5. Recommendation

**WINNER: C1 — mechanical span-in-context, one embedding — on
`Qwen/Qwen3-Embedding-0.6B` with the change-kind instruction prefix, `res` arm primary.**

Two cells pass all three gates in **both** nuisance arms — C1 on Qwen with the instruction
and C1 on Qwen without it — and the instructed one wins on every margin that matters. It
passes at the resolution floor of a 500-permutation null (p = 0.0020 for both Ω and the
gap), with gap = +0.0266 (`res`) / +0.0282 (`raw`), the construction ahead of its placebo
on **100% of the 200 splits**, and the largest null-corrected margin in the whole table
(+0.1217). Its Ω(11) = 0.3378 [95% split interval 0.3137–0.3601] against a null median of
0.2161. Against v1's instrument the margin is 0.1217 vs 0.0002 — C4's reading on bge was,
to three decimals, nothing.

The instruction prefix earns its place: on the *same model*, the gap is +0.0102 without it
and +0.0266 with it (2.6×), and the change-attributable share of the margin rises from 9%
to 17%. Model and instruction both contribute and the ordering across all three arms is
monotone: bge +0.0044 → Qwen no-instruction +0.0102 → Qwen + instruction +0.0266.

**Five conditions bind this recommendation. It should not be carried into the v2 prereg
without them.**

1. **The primary statistic must be the gap, `Ω − Ω_placebo`, with its own label-permutation
   null — not Ω.** On corpus A, *every* construction's Ω beats the label-permutation floor,
   including placebos that cannot see the change at all (every `placebo p(N1)` in the
   primary arm is 0.0020). Ω alone therefore cannot discriminate a change-reader from a
   context-reader, and a v2 verdict staked on Ω would be uninterpretable.
2. **The placebo stays a required gate**, as the design doc already provides. This run is
   the numeric case for it: the gate is what killed C2, C3, C4 and C5.
3. **The power surface must be recomputed for the gap.** v1's surface (n ≈ 500 reaching
   Ω ≈ 0.27 at signal-scale 2) is an *Ω* surface and does not transfer. The winning gap is
   +0.0266 against a gap-null with median +0.0064 and 99th percentile +0.0149 — the
   observed effect clears the floor by less than a factor of two, a far tighter margin than
   the Ω surface implies. n for v2 should be set from a surface computed on the **gap**
   statistic before the prereg freezes.
4. **Name what the gap measures.** Because the extractor picks the sentence *by where the
   change is*, the placebo already encodes the change **site**. The gap therefore measures
   "kind information in the change **beyond its site**". That is arguably the right target,
   but it must be said in the prereg, and the interleaved rebuild should be designed so the
   same site can carry different kinds — otherwise site and kind stay confounded and the
   gap is measuring the residue of a confound rather than a coordinate.
5. **Carry the winner as a construction, not as an effect size** (steward's batch caveat,
   banner). Because kind is nearly nested in generation batch on corpus A and the N1 null
   permutes labels freely, an unknown share of every separation here is batch, not kind.
   The *ranking* survives — all 30 cells carry the identical confound, so it cancels when
   constructions are compared — but the *magnitudes* do not transfer. The prereg may stake
   C1 + Qwen + instruction as its instrument; it may not stake +0.0266, or any band derived
   from it, as an expected gap. v2's interleaved rebuild (one item per kind per batch)
   makes kind ⊥ batch by construction and is where a real magnitude first becomes available.

**Second arm, if one is wanted.** C1 on bge is the cheapest cross-embedder replication and
passes the primary arm — but marginally (p_gap = 0.0100, exactly at the bar; 4 of 500
permutations reached the observed gap) and it fails in the `raw` arm. Carry it as a
secondary that is *reported*, not as a conjunct that must fire.

**A calibrated expectation, stated now so it cannot be spun later.** 83% of the winner's
null-corrected margin is reproduced on this corpus by a control that cannot see the change.
If v2 reads null on the new corpus at 4× power with the placebo gate passed, that is a real
null of the geometry hypothesis and not an instrument excuse — the design doc already says
so, and this bake-off is what makes that commitment honest.

---

## 6. C5 — the construction added beyond the brief's four

The brief specified four. A fifth was added because C3 and C4 confound two explanations of
v1's defect 1: *subtraction cancels the site cues*, and *the document is the wrong unit*.
C5 is v1's difference vector taken at the **sentence** granularity — same subtraction, right
unit — with the before-sentence cloud as its placebo, matching granularity exactly as C4's
placebo matches C4's. It cost zero API calls (the sentence embeddings were already cached
for C2).

**Result: the unit helps, the subtraction still kills it.** Moving Δ from the document to
the sentence multiplies its null-corrected margin by ~20× on bge (+0.0002 → +0.0044) and
~1.5× on Qwen + instruction (+0.0093 → +0.0139) — but C5 still fails everywhere: on the
**null** for bge (p = 0.128), and on the **placebo** for both Qwen arms, where the
change-blind before-sentence control reads 4.6× (with instruction) and 8.4× (without) the
construction's own margin. So defect 1's diagnosis should be recorded as: **subtraction is
the primary failure**, and document granularity is a secondary aggravator worth about one
order of magnitude on a quantity that needs three.

### 6.1 The site leak, measured

The same three placebo clouds, ranked by null-corrected margin (`res` arm), quantify how
much kind-structure sits in text that **cannot see the change**:

| change-blind cloud | bge | Qwen +instr | Qwen no instr |
|---|---:|---:|---:|
| before **document** (v1's K1c placebo) | +0.0255 | +0.0304 | +0.0166 |
| before **sentence** (C2/C5 placebo) | +0.0592 | +0.0636 | +0.0597 |
| C1 placebo rendering | +0.0558 | +0.1013 | +0.0719 |

Selecting the sentence by where the change is **2.1–3.6× the readable kind structure** of
the unchanged document. This is prereg §4's measured leak (the *unchanged* document predicts
`kind_target` at 0.149 vs chance 0.083) amplified by the extractor. It is not a defect of
the extractor — you cannot read a change without locating it — but it is why gate 3 exists
and why condition 4 above is binding.

---

## 7. Method notes a reader should be able to check

**Lossless dimension reduction.** With n = 247 in d = 1024, every quantity the pipeline
forms (class means, least-squares residuals, centred SVDs, contrast Grams) stays inside the
row space of the cloud, and Ω is invariant under an orthonormal change of basis of any
subspace containing it. Each cloud is therefore re-coordinatised onto an orthonormal basis
of its own row space (d_eff = 247 in all 30 cells) before anything is computed. This is
exact, not an approximation, and it is **verified**: C4 on bge reproduces v1's published
numbers to every digit stored —

| | this run | v1 `main_primary.json` |
|---|---|---|
| Ω(11) | 0.059978486659569 | 0.059978486659569 |
| placebo Ω(11) (K1c `omega_before`) | 0.133740834924113 | 0.133740834924113 |
| null median | 0.059790 | 0.059790 |
| p(N1) | 0.465070 | 0.465070 |

It buys a 4× speedup (0.090 s vs 0.352 s per permutation), which is what made 500
permutations affordable across 30 cells.

**rank(B) = 11 in every one of the 30 cells**, as prereg §5.1's counting identity requires:
12 one-vs-rest centroid contrasts span exactly 11 dimensions for any labelling of any
corpus. Ω is reported against `r = rank(B)` throughout. No cell applies v1's V1 class-drop,
because dropping a class cannot change span(B) — any 11 of the 12 contrasts span the same
subspace as all 12.

**C3's residualization is partial, and this is disclosed.** The reduced-rank before-basis
was pinned at 20 principal components in advance, because only ~124 rows are available in a
fitting half. Those 20 carry **41%** of the before-cloud's variance, so C3 removes 41% of the
before-geometry, not all of it. It nonetheless lands on C4's reading (0.0551 vs 0.0600 on
bge), which says the result is insensitive to how much of the before-cloud comes out.

**`span_chars` in the nuisance matrix is v1's**, from v1's difflib extractor, held identical
across cells so C4 reproduces v1 exactly. The new extractor's changed-region length
correlates 0.86 with it.

**k = 11 is the pre-registered primary and nothing was promoted post hoc.** For the record,
C1's Ω is monotone in k and p = 0.0020 at *every* k in {5,7,9,11,13,15,20,30,40} on all
three embedders — the reading is broad-band, not a k = 11 artifact.

---

## 8. Spend

| | |
|---|---|
| this phase | **$0.00102** |
| cumulative (v1 + phase 0) | **$0.00496** |
| cap | $1.00 — used 0.5% |
| tokens | bge 362,223 (137 calls) · Qwen3 267,396 (72 calls) |

New texts embedded: sentence-before, sentence-after, the C1 rendering and the C1 placebo
rendering for bge and for Qwen-with-prefix, plus all six text sets for Qwen-without-prefix.
The full-document embeddings were reused from v1's cache. Both analysis runs made **zero**
API calls (`EIGEN_STRICT=1`).

Cache manifest (`scratchpad/eigen/cache/`, existing convention):

| model | sha256 | bytes |
|---|---|---|
| BAAI/bge-large-en-v1.5 | `c0d82282ee73e4c14f02bd696db4380af8b0cce58f99c2ea1ca568ebd7ee3dc8` | 46,616,988 |
| Qwen/Qwen3-Embedding-0.6B | `699cbea501a7962fce6f254ec612faaa0758efbdcf1018a80df06d4e696e2705` | 24,101,715 |

---

## 9. Anomalies and honest limitations

**Clean checks.** rank(B) = 11 and d_eff = 247 in all 30 cells. Zero degenerate (zero-norm)
Δ rows in all three embedder arms. v1 reproduced exactly. No cell hit the spend cap, no
retries, no VOID condition triggered.

**Anomalies worth recording.**

1. **The bge winner is marginal and arm-dependent.** C1 on bge passes at p_gap = 0.0100 —
   4 of 500 permutations reached the observed gap — and fails the `raw` arm at 0.0160. Do
   not describe bge as a passing instrument without that qualifier.
2. **In the `raw` arm the before-document placebo does not beat its own null**
   (p = 0.896 on bge, 1.000 on both Qwen arms; margin −0.007 to −0.029). Nuisance
   residualization removes the domain- and span-dominated principal directions, which lowers
   the null floor and *exposes* kind structure that the raw cloud's floor hides. This is an
   argument for keeping the residualized arm primary, as v1 had it, and it means `raw`-arm
   placebo comparisons are not interchangeable with `res`-arm ones.
3. **A large negative gap can be "significant" too.** Several cells show p_gap = 0.0020
   with a *negative* gap (e.g. C4.qwen.raw, −0.0318). The gap null is not centred at zero
   when the two clouds have different geometry, so p_gap is a one-sided test against that
   offset null, not a test against zero. Read the sign and the gap-null median together;
   both are in the table.
4. **The C1 placebo is an imperfect control.** Filling the AFTER slot with the BEFORE
   sentence produces a text with a duplicated clause, which no natural rendering would have.
   It is the brief's specified placebo and it is the conservative direction (redundancy, if
   anything, helps the placebo's geometry), but a reader should know the control text is
   degenerate in a way the construction text is not.
5. **The Qwen instruction confounds instruction-following with cloud compression.** The
   prefix raises median pairwise cosine to 0.83. The gap statistic is immune to that by
   construction, and the no-instruction arm brackets it, but the *mechanism* of the
   instruction's benefit is not established here — only its size.
6. **Corpus A is spent and this is a selection, not an estimate.** The winner was chosen
   from 30 cells on data v1 already read. The gap of +0.027 is a selected maximum and is
   **not** a forecast of what the new corpus will give; treating it as one would be exactly
   the error rule 6 forbids.
7. **Every separation may be batch-inflated** (steward; see the banner and §5 condition 5).
   Kind is nearly nested in generation batch on corpus A, and free label permutation breaks
   batch and kind together, so the N1 floor is a *kind-or-batch* floor. The ranking is
   protected because all 30 cells carry the same confound; the magnitudes are not. Note
   that the primary arm already regresses out `part`, which prereg §4 declares makes the
   test *harder* and biased toward the null — so the residual batch inflation is smaller in
   the `res` column than in `raw`, but it is not zero, because regressing out a variable
   that kind is nested in also removes genuine kind signal collinear with it. This is not
   fixable on corpus A. It is fixed by construction in v2's interleaved rebuild.
8. **Two deliverable-level corrections were made after the first hand-off**, both recorded
   here rather than silently: the `null p99` column was added to both tables at the
   steward's request, and a query about `n_perm = 3` was checked and found not to apply to
   any reported cell (§3.1). No cell was recomputed and no verdict changed.
