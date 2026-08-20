Verified every cited number against the artifacts on disk. Corpus tallies are all correct; the statistical design is not.

---

# ADVERSARIAL REFEREE REPORT — `/home/emoore/CIRISOntology/scratchpad/EIGEN2_PREREG.md`

**Verdict: NOT READY TO FREEZE.** 8 CRITICAL, 20 MAJOR, 15 MODERATE/MINOR. Two legs are unevaluable by algebra (C1, C5); one gate cannot fire (M8); one whole calibration base is the wrong embedder (C2) and the wrong class count (C3).

Artifacts read: `scratchpad/plane_corpus/eigen2/eigen2_corpus.jsonl` (labels only), `scratchpad/eigen/out/phase0_bakeoff.json`, `.../out/phase0.log`, `.../out/power_surface.json`, `.../out/power_surface.log`, `.../out/gauge.log`, `.../out/gauge_raw.json`, `.../out/main_primary.json`, `.../out/usage.json`, `scratchpad/eigen/{pipeline,common,corpora,gauge,gauge_power_surface,phase0_span,run_phase0}.py`, `scratchpad/eigen/cache/*.jsonl`, `EIGEN_ALIGNMENT_{PREREG,RESULTS}.md`, `LEAN2_CONFRONTATION.md`, `CIRISOntology/Core/WrongKind.lean`. No E2 text was embedded, annotated, or read; only §0.1-admissible label tallies were computed on E2.

---

## CRITICAL

**C1 — §7-N2: the split procedure produces ZERO splits. The primary analysis cannot run.**
N2 draws a kind-stratified half, then rejects unless every one of 40 batches is balanced to ±1, up to 1,000 redraws. Measured from the real labels (34 batches of 12, 6 of 11): the per-draw success probability is **4.8e-10** on the generous reading (`n_half ∈ {5,6,7}` for a 12-batch) and **8.7e-25** on the literal reading (`|n₁−n₂| ≤ 1` ⇒ exactly 6/6). Simulation: **0 successes in 200,000 draws**; median worst-batch imbalance is **8**. With 1,000 redraws × 200 split indices the expected number of usable splits is **9.6e-5**. Every split index is "skipped" and the "next seed" clause is circular — there is no next.
**Fix (verified working):** replace rejection sampling with a constructive **balanced bipartite edge 2-colouring**. Build the multigraph with vertices = 11 kinds ∪ 40 batches and one edge per item; join odd-degree vertices to a dummy; take an Eulerian circuit per component and 2-colour edges alternately. I ran this on the real labels: **0 constraint violations in 50 draws**, exact ±1 on *both* kind and batch simultaneously, halves of exactly 237 (per-kind 20/40, 29/59, 30/59, 18/37; per-batch 6/12, 6/11 or 5/11). Randomise by shuffling the edge insertion order. Cite de Werra's balanced bipartite edge-colouring theorem for the existence guarantee, and delete the skip-count reporting clause.

**C2 — §3.3 resolves PRIMARY = Qwen, but §§9.5/13/15/19/21 are all priced from bge. The stakes belong to the demoted arm.**
`phase0_bakeoff.json` now contains `C1.qwen.res`: verdict **PASS**, excess **+0.1217**, δ **+0.02664**. Both exceed bge's +0.0598 / +0.00437, so §3.3's rule resolves deterministically to **Qwen as PRIMARY**. Every anchor in the document is bge's:

| quantity | bge (quoted) | qwen (the actual primary) | ratio |
|---|---|---|---|
| Ω*(11) | 0.0598 | **0.1217** | 2.0× |
| δ | 0.00437 | **0.02664** | 6.1× |
| ψ = δ/Ω* | **0.073** | **0.219** | 3.0× |
| gap-null p99 | 0.0041 | **0.01492** | 3.6× |
| N1 null median | 0.1295 | **0.2161** | 1.7× |

Consequences: (i) **§9.5 Scenario A is pre-falsified.** Qwen's calibration δ = 0.0266 already exceeds A's upper edge of 0.020 at *half* the n, and Ω* = 0.1217 sits at A's upper edge before any n-scaling; A's own scaling factor (×1.4–2.1) predicts Ω* ∈ [0.17, 0.26], entirely above A's [0.07, 0.15]. (ii) **§15's margin discussion is about the wrong arm** — VG1 conjunct 4 is `max(0.005, gap-null p99)`, and on the primary the p99 term is ~0.015, so "0.005" never binds. (iii) **§19-D2 is factually false on the primary**: "a gate the calibration would not have cleared" — Qwen's δ clears 0.005 by 5× and its own p99 by 1.8×. (iv) §13's "D3 — 7.3%" is not the primary's number.
**Fix:** resolve §3.3 now (the artifact is on disk), paste both cells, and **re-derive every band, margin and ladder rung from the resolved primary's cell**, publishing the bge-priced versions as the witness arm's. Do not freeze with dual-provenance numbers.

**C3 — Phase 0 is a 12-class / rank(B) = 11 measurement; v2 is 11-class / rank(B) = 10. Never disclosed; every imported number is on a different normalization.**
`run_phase0.py` calls `run_arm(prep, labels, **12**, …)` (`corpora.KINDS` includes `testimonial`), and every cell records `rank_B = 11.0`. I verified the pipeline returns r = 10 for an 11-class partition (synthetic check: `r = [10.,…]`, null eigenvalue at 1.2e-16 relative), so the 11 in the artifact is the K=12 identity, not a numerical accident. Ω = (1/r)‖UᵀB‖²_F, so **every phase-0 Ω divides by 11 over a 12-column B**, while v2 divides by 10 over an 11-column B. Ω, Ω*, δ, ψ, the null medians, the band edges (§9.2 STRONG ≥ 0.25), §21 rung 3 (Ω* ≥ 0.19) and §9.5's scenario bands are all imported across that change without rescaling or mention. §1.4 correctly derives rank(B) = 10 but does not say the calibration it inherits was rank 11.
**Fix:** state in §3.2 that phase 0 ran K = 12 / rank(B) = 11 on Corpus A; recompute or explicitly re-price every carried-forward number, or re-run `C1.{primary}.res` on Corpus A with `testimonial` dropped (K = 11, rank 10) so the calibration is on v2's geometry. The vectors are cached; this costs no API spend.

**C4 — §8.2 reads the wrong power-surface row by a factor of 2 in n. The correct row puts V3b (primary VOID) at or below threshold.**
`gauge.py` sets `CLASS_SIZES = [12,12]+[10]*10` with the comment *"Corpus A **half** sizes"*, and `run_cell` draws **two independent halves of n rows each**. So the power surface's `n` column is a **per-half** size. E2's halves are ~237, so E2's row is **2× / n = 248**, not 4× / n = 496. Corrected numbers (`power_surface.log`):

| scale | σ_R (n=248) | ρ_gauge (n=248) | prereg quoted (n=496) |
|---|---|---|---|
| 1.0 | **1.566** | **0.172** | 1.98 / 0.291 |
| 1.5 | **1.511** | **0.320** | 1.373 / 0.476 |
| 2.0 | **1.318** | **0.445** | 1.316 / 0.618 |

Under Scenario A's own Ω* band the anchor lands at gauge scale ≈1.5–2.0 (Ω = 0.091–0.163 at n=248), where **ρ_gauge = 0.32–0.45** — and at scale 1.0, ρ_gauge = **0.172**, far below V3b's 0.30. §8.2 says "ρ_gauge sits near V3b's 0.30 threshold … V3b is a live risk." On the correct row, **V3b straddles or fires across the whole calibration-implied range**, and σ_R = 1.566 at the low end fires **V8**. The document understates its own most likely failure mode.
**Fix:** correct §8.2 to the 2× row and restate the forward statement as "V3b is more likely than not to fire and V8 is likely." Add one sentence to §8 fixing the convention: *"the gauge's per-half n is 237; the power surface's `n` is a per-half size, so E2's row is 2×/248."* §8's own geometry line ("n = 474 … halves at [18,19,…]") is ambiguous between the two and is what produced this error — an implementer setting `CLASS_SIZES` to the full class sizes would gauge at 2× the real resolution.

**C5 — §9.4/§8.1: P1b's bands are centred on the true rank (10) while the gauge's own recovered rank at that scale is 6.4–6.9. K2 fires from estimator bias with probability ≈1.**
At the corrected n = 248 row, `rkind_mean` = 3.37 (s=1.0), **6.42** (1.5), **6.89** (2.0), 7.85 (2.5). Under Scenario A the anchor is s ≈ 1.5–2.0. Tier 1's band is `|R_kind − 10| ≤ 2σ_R`, σ_R floored at 1 → [8,12]; Tier 2 is {9,10,11}. **A perfectly behaving instrument at the data's own scale reads 6.4–6.9 and falls outside both.** §9.4 then records "INCONSISTENT (K2)" and §16 reports K2 as taking down the "near 10" clause — a world-verdict manufactured entirely by a known, measured, downward estimator bias. This is the same class of defect as v1's unevaluable legs.
**Fix:** centre the band on the gauge's **mean recovered R_kind at the anchor scale (R̂)**, not on the planted rank: `|R_kind − R̂| ≤ 2σ_R`, with `R̂ − 10` quoted as the disclosed bias. Add a hard rule: if `|R̂ − 10| > σ_R` at the anchor, **P1b is UNDECIDED** and K2 cannot fire. Also reconcile §8.1 (σ_R > 1.5 → "no band verdict") with §9.4's "Tier 1 (always, if P1a DETECTED)" — they currently give opposite instructions.

**C6 — §9.5: the two scenarios are not internally consistent, and the scoring rule is not a partition.**
(a) A's three bands are mutually contradictory at the edges: Ω* = 0.15 with δ = 0.006 gives ψ = 0.04, which violates A's own ψ ∈ [0.05, 0.25] *and* lands in §13's `< 0.05` cell (DETECTED-BUT-CONTEXT-DOMINATED), which contradicts A's staked verdict cell (CHANGE-CARRIED ALIGNMENT). (b) The scoring rule reads only 2 of A's 5 conjuncts ("lands inside A's bands → A confirmed") while A also stakes ψ, VG1, the verdict cell and the strength band. (c) The clauses are OR'd, so outcomes get double- or non-assigned: Ω* = 0.10 (inside A) with δ = 0.0055 satisfies both "A" and "missed"; δ = 0.004 with Ω* = 0.10 satisfies B's δ clause and A's Ω* clause. (d) The most likely bge-shaped outcome, Ω* ∈ (0.02, 0.07) with VG1 passing, is covered by neither. (e) "Lands above A → A falsified high … makes the pass *stronger* evidence" converts a missed advance prediction into support, which is precisely what rule 6 forbids.
**Fix:** stake **one** ordered statistic (Ω*) with an exhaustive, mutually exclusive band partition covering (−∞, ∞); make δ and ψ *secondary* predictions scored separately; delete the "falsified high is stronger evidence" clause and replace it with "falsified high is a miss, reported as a miss; the §9.3 verdict is read independently."

**C7 — §§9.2, 9.3, 10: the "paired within split at p < 0.01" comparisons name no test and no null.**
P1a's third conjunct (`Ω_taxonomy > Ω_domain11`), P1d's δ-privilege conjunct (`δ_taxonomy > δ_domain11`) and §10's P3 comparison all demand p < 0.01 for a comparison whose reference distribution is never specified. The 200 splits share all 474 items and are near-replicates, so any across-split test (sign-flip, Wilcoxon, t) has a badly understated variance. VG1 gets this right — it pairs a sign-flip test *with* a label-permutation floor — and nothing else in the document does.
**Fix:** specify, for every "paired at p < 0.01", the same two-part apparatus as VG1: sign-flip across splits for direction **plus** a label-permutation floor (same 500 permutations, both arms) for magnitude, with the permutation floor as the governing p. State that splits are not independent units and that the sign-flip leg alone is not evidence.

**C8 — §12: the positive control's three classes use DIFFERENT item sets, so VG2 can be passed on topic.**
"For each family take the first N items in id order **where the trigger exists**." M1 (modals), M2 (numerals) and M3 (`is`/`are`/`does`) trigger on different documents; modal-bearing text skews to `policy`/`manual`, numeral-bearing to `registry`/`log`/`config`. The 3-class contrast is therefore confounded with domain and topic, and Ω_PC(3) can clear its null without the rendering encoding any edit — destroying the one inference VG2 exists to license ("failing it proves it cannot read edits at all"). §12's claim that "topic is held fixed within every pair" is true *within* a pair and irrelevant to a *between-class* contrast across different items.
**Fix:** restrict to the intersection — items where **all three** triggers exist — and render all three mutations of the **same** item. Each item then contributes one text to each class, topic is exactly balanced across classes by construction, and the contrast can only be driven by the edit. Stake a minimum N (e.g. ≥ 60) and a VOID if unreachable.

---

## MAJOR

**M1 — The instruction is never ablated, and the ablation is free.** `run_phase0.py`'s `SPEC` already contains `qwen_noinstr`, and I verified the **bare (uninstructed) Qwen vectors for all 247 C1 texts are already in the cache** (247/247 present). No cell was run. The primary arm is an instructed model whose instruction was written by the taxonomy's author with the taxonomy in hand; §3.3's justification ("only one of the two models can be told the task") is exactly the claim an ablation settles. Without it, "Qwen reads 2× bge's excess" cannot be separated into model capability vs. instruction steering, and the steering is an author-authored channel — the sharpest circularity route into the primary arm.
**Fix:** run `C1.qwen_noinstr.res` on Corpus A now (zero API spend) and paste it into §3.3; pre-register **Qwen-no-instruction as a required third arm on E2** (474 × 2 = 948 texts, inside budget) with a staked reading: if the uninstructed arm reads the same Ω* and δ, the instruction is inert; if it collapses, the primary's reading is instruction-manufactured and must be reported that way.

**M2 — The placebo carries an instruction with a false presupposition, and no diagnostic is staked.** `"Identify what kind of commitment changed between the two versions"` is applied to C1P, where the two versions are character-identical. §3.1's "a placebo that does not carry the instruction is not a placebo" is right but incomplete: an instructed model asked to find a change where none exists can produce a degenerate or idiosyncratic representation, inflating or deflating Ω_C1P for reasons unrelated to context-kind-reading, and δ is a difference of two nearly-parallel clouds (I measured median cos(C1, C1P) = **0.9895** qwen / **0.9916** bge on the calibration corpus).
**Fix:** stake a pre-registered diagnostic: median cos(e(C1P), e(ctx_before)) and the C1P cloud's anisotropy (evr_top11) with and without the instruction, plus the fixed reading if the instructed C1P cloud is materially more anisotropic than the bare one.

**M3 — §3.2 omits the pinned code's own disclosure about when the selection rule was set.** `run_phase0.py`'s docstring states: *"DISCLOSURE: (c) was added after a 3-permutation smoke run had shown the Omega and placebo-Omega values (which are deterministic and carry no p-value)."* Criterion (c) is the gap criterion; the gap's sign and size were already visible from those deterministic values, and (c) is what eliminates C1.bge.raw and C2. §3.2's "under a selection rule fixed before the permutation counts were seen" is literally true and materially misleading. In a prereg whose whole point is rule 1, the code's disclosure must be reproduced verbatim.

**M4 — The chosen construction passes the phase-0 selection by ONE permutation out of 500.** `C1.bge.res` has `p_gap_N1 = 0.00998 = (1+4)/501`. The next attainable value is `(1+5)/501 = 0.01198`, which **fails** the ≤ 0.01 rule. Had one more of 500 permutations exceeded, **no construction would have passed on bge**. §3.2's "C1 is the only construction that passes" is one seeded draw deep on the witness embedder.
**Fix:** disclose the exceedance count (4/500) beside p_gap wherever the selection is quoted.

**M5 — On the resolved primary, BOTH nuisance arms pass, and the raw arm has the larger gap.** `phase0.log`: `C1.qwen.raw` → Ω 0.3625, null 0.2584, excess 0.1041, placebo 0.3343, **gap +0.0282**, p_gap 0.0020, **PASS**. §3.2's "the residualized arm is the passing arm (C1.res passes, C1.raw fails on p_gap)" is a **bge-only** fact and is false on the primary. §3.3's substitution clause covers "a different **construction**", not "the same construction, other nuisance arm" — an unhandled branch that currently pins `res` on a justification that has evaporated.
**Fix:** add an explicit nuisance-arm resolution rule of the same form as §3.3's, resolved at freeze from the primary's cells, or state that `res` is pinned by v1 continuity alone and drop the phase-0 justification.

**M6 — §15-V1/V1b: "rank(B) falls" is arithmetically false, and V1b's gloss is off by two.** With K = 11 the contrasts obey exactly one linear relation, so rank = 10. Drop **one** class: the remaining 10 contrasts are linearly independent → **rank is still 10**. Rank only falls from the *second* drop. So `rank(B) < 7` ⟺ ≤ 6 classes kept, not the "fewer than 8 measurable classes" §15-V1b's gloss states. (v1's own artifact confirms the mechanism: `main_primary.json` shows `V1/fired = true`, `unmeasured = ['axiotic']`, `rank_B = 11.0` — the drop did not lower the rank.)
**Fix:** restate as `rank(B) = min(#classes kept, 10)`; restate V1b's threshold in classes-kept and align the gloss.

**M7 — §6's "Σ_j a_j = r exactly" is false as written, and the maxT justification rests on it.** The identity holds over *all* d directions, not over j = 1…40. The held-out cloud has ~237 PCs. Checkable directly from the artifact: `C1.bge.res` Ω(40) = **0.3640**, so Σ_{j≤40} a_j = 0.364 × 11 = **4.0**, not 11. (maxT remains the correct choice — it controls FWER under arbitrary dependence — but the stated reason is wrong and a referee will read the wrong reason as a wrong statistic.)
**Fix:** state `Σ_{j≤40} a_j ≤ r, with the shortfall (r − Σ) reported`, and justify maxT on arbitrary-dependence FWER control rather than on negative dependence.

**M8 — §11/§15-VG3: the χ² interleave gate cannot fire.** Measured on the real labels: kind × batch is 11 × 40 with **minimum expected cell 0.859**, 390 dof, χ² = 18.8, **p = 1.0000**. A χ² approximation at expected counts ≈1 with 390 dof has essentially no power and an unreliable null. No plausible drop pattern will push it below 0.05, so VG3 is decorative — and it is the *only* gate protecting the design claim on the analysed set. (§2.2 half-admits this for the descriptive χ², then reuses the same statistic as a numeric gate.)
**Fix:** replace VG3 with a direct combinatorial statistic — e.g. `max_b |kinds_missing_in_batch_b|` or the variance of per-batch kind composition — compared to a permutation null over drop patterns of the same size; or gate simply on "no batch loses > 3 items and no kind loses > 10% after drops."

**M9 — §11's D-B1 thresholds are mis-scaled, and the 0.573 that motivates the whole rebuild is quoted without its baseline.** v1 §2.1a/M1: batch was a **3-class** problem (part_a/b/c) and 0.573 was measured against a **majority baseline of 0.484** — a lift of **1.18×**. v2 quotes "0.573" twice (§2.2, §9.5-B) with the baseline dropped, where it reads as a strong confound. Meanwhile D-B1's thresholds are for a **40-class** problem with baseline 0.025: "≤ 0.10 → batch style is weak" is a **4× lift**, i.e. ~3.4× stronger in lift terms than the confound that forced the corpus rebuild.
**Fix:** restate 0.573 with its baseline and class count wherever it appears; restate D-B1's bands as lift-over-baseline (or normalized MI), with "weak" set no higher than v1's 1.18× lift.

**M10 — Difficulty is NOT flat across kind, and no arm, no nuisance term and no null covers it.** Measured from the labels: hard items per kind are 10 everywhere **except `empirical`, which has 20**. `ambiguous_with` targets concentrate on `empirical` (41) and `deontic` (35) — precisely the two n = 59 classes. So the two largest classes are also the designed attractors: `empirical`'s out-group contains 41 items written to resemble it, and it carries twice everyone's hard items. §2.1 reports only the 354/120 marginal, never the kind × difficulty cross-tab. `Z` contains span, domain and batch — **no difficulty term** — and N1/N1b/N1c are all blind to it. A NOT-DETECTED could be produced by the 120 hard items alone (rule 3: match the null to the generative structure).
**Fix:** report the kind × difficulty cross-tab in §2.1; add a **`clear`-only sensitivity arm (n = 354)** with its meaning fixed (reported, never headline); add **N1d, a difficulty-stratified permutation**; and either add difficulty to `Z` or state why not.

**M11 — §4's claim that the 40-level batch term is "a power gain, not a power tax" is asserted without measurement and is probably backwards.** With 237 fitting rows and 40 batches there are **≈5.9 items per batch per fitting half**. Each batch mean is estimated from ~6 points and, because the design puts ~1 item per kind per batch, that mean is a noisy estimate of the grand mean. The betas are then **applied to the held-out half**, whose items contributed nothing to those means — injecting ≈σ²/6 of pure estimation noise into every held-out vector before the SVD. §4 states the sign of this effect as a fact.
**Fix:** delete the sign claim; state the df arithmetic (5.9 items/batch/half) explicitly; and either shrink the batch term (ridge with a pinned λ, or partial pooling) or make the span+domain-only arm the primary with the full-batch arm reported beside it. The existing NUISANCE-DEPENDENT disagreement rule is good and should be kept either way.

**M12 — §4's nuisance column count is rank-deficient and contradicts the pinned code's convention.** `1 + 12 (domain) + 40 (batch) = 53` includes a constant plus full one-hots on both factors — rank-deficient by 2. `run_phase0.py`'s `dummies()` uses `sorted(set(vals))[1:]`, i.e. K−1 dummies, giving `1 + 11 + 39 = 51`. `lstsq` will silently take the minimum-norm solution.
**Fix:** state 51 with the drop-first convention, or state that full one-hot with min-norm `lstsq` is intended and that the reported column count is 53 with rank 51.

**M13 — §16-K1's blast radius does not distinguish an N1 failure from an N1b failure.** §9.2 kills P1a on either, and §16 assigns the same blast radius (the eigen-bridge paragraph, "for the second time"). But N1b preserves the kind↔span relation, and §0.1 **deliberately declined to measure E2's span spread** (v1's was 87×, Kruskal–Wallis p = 7.6e-16). If E2 reproduces anything like that, N1b's null rises toward the observed and K1 fires from edit length, not from geometry — and is reported as a taxonomy verdict. §19-D8 names the hazard but stakes no consequence.
**Fix:** add the sub-verdict **N1 passed / N1b failed → SPAN-CONFOUNDED**, reported under that name, with K1's blast radius restricted to "P1a beyond edit size"; and make the E2 span spread a **post-freeze design measurement (like D-B1) read before N1b's p is read**, with its meaning fixed now.

**M14 — VG1's "four conjuncts" are not four gates.** Conjuncts 1 (δ_median > 0) and 2 (sign-flip p ≤ 0.01 and frac_splits_gt ≥ 0.60) are near-deterministic functions of each other across 200 overlapping near-replicate splits: calibration shows `frac_splits_gt` = 0.855 (bge) / **1.000** (qwen) and `p_paired` = 1e-4 on δ values of 0.0044 / 0.0266. VG1 therefore reduces to conjuncts 3 (permutation floor) and 4 (margin) — and on bge conjunct 3 was the one that passed by a single permutation (M4).
**Fix:** say so in §15, and re-express VG1 as a two-gate test (permutation floor + margin) with 1–2 reported as descriptors, so the gate's real strictness is not overstated to the steward in §22.1.

**M15 — §13's ψ is unguarded, mis-scoped, and gates promotion on an interval-free point estimate.** (a) "ψ is undefined when Ω\* ≤ 0; in that case VG1 has already fired" is **false** — VG1 tests δ only. Ω\* ≤ 0 with VG1 passing is exactly the **CHANGE-READ, TAXONOMY-NULL** cell that §9.3 calls "the outcome v2 was built for," and in that cell a *mandatory* statistic is undefined. (b) ψ = δ/Ω\* is an unguarded ratio: Ω\* = 0.01 with δ = 0.006 reads ψ = 0.6 → "the alignment is the change's." (c) §21 rung 4 gates promotion on ψ ≥ 0.25 with no interval, and the primary's calibration ψ is **0.219** — inside noise of the bar.
**Fix:** define ψ only when Ω\* exceeds the N1 p99; add the missing branch for Ω\* ≤ 0 with VG1 passing; stake a permutation/bootstrap interval for ψ and condition rung 4 on the interval's lower bound, not the point estimate.

**M16 — §9.3's table claims exhaustiveness and omits a cell.** 2 (P1d) × 2 (P1a) = 4 non-VOID cells; the table has 3. Missing: **(P1d FAIL, P1a NOT DETECTED)** — VG1 held, δ-privilege failed, and no alignment either. This is a live outcome (the instrument reads changes but neither the taxonomy nor its privilege survives) and "every combination is named in advance" is false without it.
**Fix:** add the cell with its fixed name and meaning.

**M17 — §21 rung 2 (STRONG, Ω ≥ 0.25) is nearly free on the resolved primary.** Qwen's **N1 null median is already 0.2161** at n = 247 (null p99 = 0.2340). Clearing Ω(11) ≥ 0.25 therefore needs only Ω\* ≈ 0.034 — a "STRONG" label carrying almost no information. §9.2's drift disclosure quotes only bge's 0.1295 and never the primary's 0.216, so the disclosure understates the drift by a factor of ~1.7 on the arm that matters. Rung 3 (Ω\* ≥ 0.19) is the only live rung.
**Fix:** define the strength bands on Ω\* (or on (Ω − null_med)/(1 − null_med)) and delete the raw-Ω band, or collapse rungs 2 and 3 into rung 3 alone.

**M18 — §11's D-B3 states the wrong direction and leaves the governing null undefined.** N1 permutes freely, so its permuted labellings are batch-*unbalanced* and absorb batch style; N1c preserves the design's balance. If batch carries variance the expectation is **N1 null ≥ N1c null** — i.e. free permutation is conservative, which is the *good* direction. The prereg reads a disagreement as "the sharpest available evidence that batch matters after all" and prescribes only that the residualized arm becomes sole reported — it never says **which null governs P1a's p-value** after a disagreement. Switching to N1c would be anti-conservative.
**Fix:** state the expected direction; pin **N1 as the governing null in all branches**; and restate D-B3's meaning as "how much batch variance a random 11-way partition absorbs," not as a threat to the result.

**M19 — §3.4's V7 leaves the 0–2% over-length band unhandled, and the C1/C1P pairing can break.** DeepInfra returns HTTP 400 rather than truncating (v1 D-5). At 1.9% over-length, V7 does not fire and the run hard-fails on those requests. Worse, C1 and C1P have **different lengths**, so an item can be over-length in one arm only — silently unpairing δ.
**Fix:** specify: any item whose C1 **or** C1P text exceeds the context is dropped from **both** arms and from all rivals; the drop list and count are reported; V1b/V3/VG3 are re-evaluated on the reduced set.

**M20 — §8's Addition 3 (the two-world validation) is vestigial and expensive.** Record is excluded (§1.4), P2 has no v2 arm, and §5.2 already says LOKO "carries no verdict." Addition 3's only possible consequence is downgrading a no-verdict table from "reporting-only" to "EXPLORATORY." Its outcome is also close to pre-determined: v1's gauge returns `frac_12th_below_min = 0.920` at s = 1.5 — **below the staked 0.95** — at the scale the design expects. It is ~40% of the gauge's cell count.
**Fix:** cut it, or state explicitly what decision it changes.

---

## MODERATE / MINOR

**m1 — §6's row-space chance scale.** `k/474 = 0.0232` uses the full corpus, but `U_k` is the SVD of the **held-out half** (~237 rows). The comparable scale is `k/237 = 0.046`. Labelled "a scale, never a null," but it is a wrong number in a frozen document.

**m2 — §9.4's "at worst [8, 12]" is wrong above σ_R = 1.0.** At the V8 boundary σ_R = 1.5, the band is `|R − 10| ≤ 3` = **[7, 13]**, which cannot exclude 13 — Tier 1 is vacuous exactly where §8.1 says it still lives. State the band as a function of σ_R and give the σ_R at which Tier 1 becomes vacuous.

**m3 — §8's planted-rank grid {6, 10, 13} is not constructible as stated, and the gauge code does not support it.** With K = 11 the maximum between-class rank is 10, so "planted rank 13" is not a between-class rank. `gauge.py` already declares the workaround for K = 12 ("2 extra structured non-kind directions … an implementation specification the prereg leaves unspecified; it is declared here") — the prereg must import that declaration verbatim. Separately, `gauge.py` is hard-wired to `NK = 12`, `RECORD_IDX = 11`, 12-long `CLASS_SIZES`, and worlds `rank7/rank11/rank13` — there is **no `rank10` world**, and Addition 3's "10 content + 1 orthogonal" needs `nclass_content = 10`. §8 requires code changes not yet written.

**m4 — §8's half-size vector sums to 235, not 237.** `[18,19,20×7,29,29] = 235`; the complementary half is 239. The pipeline averages both directions. Say which the gauge uses (and see C4 on the per-half convention).

**m5 — §7.1's "domain-11 = the 12 domains with the two smallest merged" is ambiguous.** Verified counts: `report` 38 (unique smallest), then a **four-way tie at 39** (`bulletin`, `notice`, `policy`, `process`). The rule does not identify a second class. Pin a tie-break (alphabetical, or first-by-id) in the frozen text.

**m6 — §7.1's rank-matching requirement is automatically satisfied.** By §5.1's own identity, **any** 11-way partition with all cells non-empty has rank exactly 10, so K1b's "cannot fire if not rank-matched" escape hatch is dead except in the one real case: k-means-11 emptying a cell in a fitting half. Say that, and state what happens when k-means returns fewer than 11 non-empty clusters (currently `C[cnt==0] = 0` silently lowers the rank).

**m7 — §1.4 pins k = 11 as the primary while rank(B) = 10.** The primary Ω therefore sums one more PC than the kind subspace has dimensions, which is a systematic upward bias relative to the rank-matched Ω(10) — while §7.1 makes rank matching "mandatory" for rivals. State the inconsistency and its direction, or make Ω(10) the rank-matched co-primary.

**m8 — §22.7's compute estimate is low by roughly 5–10×.** v1's *smaller* gauge (24 rank cells + 16 world cells, n = 124/half) took **836 s** (`gauge.log`); v2's is 27 + 18 cells at n ≈ 237/half, i.e. ~3.7× the per-cell SVD cost → ~1 hour for the gauge alone, and ~4 h if an implementer reads §8 as n = 474/half. Phase-0 arms took 43–92 s each at n = 247/d_eff = 247; v2's arms are ~4× that, and §18 requires ≈40+ permutation arms (3 nulls × 2 renderings × 2 rivals × 2 sensitivity arms × 2 embedders). "Minutes-to-an-hour" understates it; a frozen protocol with a pinned order of work should not time out mid-run.

**m9 — §12's N is unknowable under §0.1's own abstention.** `N = min(120, the smallest family's count)` requires a mechanical regex pass over E2's `before` texts, which §0.1's *exhaustive* list of pre-freeze computations does not authorize. Either add the trigger counts to §0.1's admissible list (they are mechanical and label-free) or stake a VOID for unreachable N.

**m10 — §3.2 presents "four constructions" but the pinned code declares five.** `run_phase0.py` implements **C5** (v1's difference vector at *sentence* granularity) and documents it as *"the control that separates 'subtraction cancels the site cues' from 'the document is the wrong unit' — the two halves of the design doc's defect 1."* It was **not run** (`CONS` defaults to `C1,C2,C3,C4`; no C5 cell in the artifact). §3.2's conclusion — *"Subtraction is the defect, and it is not the only defect"* — is precisely the inference C5 was built to test, and it currently rests on C1-vs-C2 alone.

**m11 — §0.1 and READY-FOR-REFEREE misstate the phase-0 state, and §3.3/§22.2 cannot be executed yet.** `out/phase0_bakeoff.json` (mtime 19:36; prereg 19:37) already contains `C1.qwen.res`, and `out/phase0.log` shows `C1.qwen.raw` and `C2.qwen.res` also complete. Meanwhile phase 0 is **still running** (`C2.qwen.raw` in progress), so the "completed `phase0_bakeoff.json`" that §3.3's resolution rule and §3.3's substitution clause both reference does not exist. Correct the statement, and note that the substitution clause is currently unevaluable on the primary embedder because **no C2/C3/C4 Qwen cells existed when C1 was pinned**.

**m12 — The prereg silently re-bases the published prediction's integers.** `LEAN2_CONFRONTATION.md` Prediction 1 stakes alignment with "the 11 kinds' … directions — **not 7, not 13**." v2 tests rank 10 with "**not 6**, not 13" and Tier 2 band {9,10,11}. §1.4 says the counting identity moves but never says the *staked integers* move. §16-K1's blast radius names the paragraph as a whole while Prediction 2 (Record) correctly has no v2 arm.
**Fix:** add one line to §1.4 recording the re-basing (11 → 10; "not 7" → "not 6") and restrict K1's blast radius to Prediction 1.

**m13 — §3.2's verdict column reproduces an artifact mislabel.** `C1.bge.raw` is tagged `FAIL:placebo`, but its placebo test passes (median diff +0.00435, p_paired = 1e-4, frac_gt = 0.805); it fails criterion (c), p_gap = 0.0160. The prose gets it right ("C1.raw fails on p_gap"); the table label contradicts the prose.

**m14 — Citation drift.** §2.1 cites `Core/WrongKind.lean` **lines 167–178**; `WrongKind.plain` runs **166–178** (map itself verified correct). §19-D1 cites "`LEAN2_CONFRONTATION.md` §2"; the Yang et al. (EMNLP 2017) reference is at line 41 under "Phase 2 — the encyclopedia," and the eigen section is a separate later heading.

---

## Verified clean — state these as pre-priced rather than leaving them open

Everything below I checked against the artifacts and it holds:

- **Corpus identity:** sha256 `cf26b604…be7c40` ✓, 813,933 bytes ✓, 474 rows ✓, 11 fields ✓, exactly 1 distinct key set ✓, 474 distinct `before` and 474 distinct `after` ✓, `part` all `E2` ✓.
- **All label tallies exactly as printed:** the 11 class counts ✓, the 12 domain counts ✓, clear 354 / hard 120 ✓, 3 hard in every one of 40 batches ✓, `ambiguous_with` non-null on exactly the 120 hard items with the stated target distribution summing to 120 ✓, batches 0–39 with 34 of size 12 and 6 of size 11 ✓, kind × batch cells ∈ {0,1,2} with 396 ones + 39 twos + 5 zeros ✓, 35 batches carrying 11 distinct kinds and 5 carrying 10 ✓, χ² dof 390 / 110 both p = 1.0000 ✓, internal→plain map ✓.
- **§3.4's cost arithmetic:** 1,896 + 720 + 80 ≈ 2,700 ✓.
- **§15-V3 is inert by design** ✓ (minimum half-class is `epistemic` at 18, well above the floor of 12).
- **§15-V4 is empirically inert** — measured on the cached calibration C1 clouds: **zero** item pairs above cos 0.99 in either embedder (bge median pairwise cos 0.640, max 0.927; qwen median 0.830, max 0.970). Worth stating in §15 so the VOID is disclosed as pre-priced.
- **§15-V1 is near-inert but knife-edge** — measured median cos(C1, C1P) per class on the calibration corpus: bge global 0.99158, worst class `axiotic` **0.99895** against the 0.999 threshold (frac of items > 0.999 = 9.3%); qwen global 0.98953, worst class `procedural` 0.99500. No class fires on either embedder, but bge's `axiotic` sits 5 parts in 10⁵ from firing. Put these numbers in §15 so the threshold is disclosed as pre-priced rather than inherited from the Δ construction (whose cos scale is different: v1 measured `axiotic` at 0.9991 doc-level and V1 **did** fire there).

---

## The three changes that must happen before any signature

1. **Resolve §3.3 from the artifact now (PRIMARY = Qwen), then re-derive every band, margin, ψ anchor and ladder rung from the primary's cell on v2's K = 11 / rank 10 geometry.** As it stands the document stakes bge numbers on a Qwen run at a different class count — C2 and C3 together invalidate §9.5, §13, §15-VG1's margin, §19-D2/D3 and §21.
2. **Replace §7-N2 with the Euler-split construction (C1).** Without it there is no analysis at all.
3. **Re-read the power surface at n = 248 and re-centre P1b on the gauge's recovered rank (C4, C5).** Both currently point the run at verdicts the instrument's own calibration says it cannot render.