# EIGEN2 — DEVIATIONS AND RESOLUTIONS, recorded BEFORE the deviating computation runs

Per `EIGEN2_PREREG.md` §0.3: any deviation after the §24 freeze stamp is an amendment with a
timestamp, written **before** the deviating computation runs, and never edited in place.
Kept in this separate file rather than appended to the frozen prereg, so the frozen artifact's
own sha256 is not disturbed while other agents may be reading it.

Nothing here changes a staked band, margin, gate threshold, verdict rule or ladder rung.

---

## A1 — cache location (2026-08-19, before any embedding)

**Prereg §3.4** pins the vector cache to
`/home/emoore/CIRISOntology/scratchpad/eigen/cache/eigen_cache_<model-slug>.jsonl`.

**Deviation.** Vectors for this run are cached to
`/home/emoore/CIRISOntology/scratchpad/eigen2run/cache/eigen_cache_<model-slug>.jsonl`
instead, with a `cache/MANIFEST.sha256`.

**Why.** The v1/phase-0 cache is a shared artifact whose sha256 is pinned by
`phase0_bakeoff.json`, `phase0_freeze_snapshot.json` and `phase0_k11_reprice.json`, and other
agents in this session read it. Appending 3,000+ E2 vectors would alter that file's digest and
break the provenance of the calibration this prereg is anchored to.

**What is unchanged.** The cache **key** is byte-identical to the prereg's —
`sha256(model || "\x00" || text)` — and the v1 cache is opened **read-only** for lookups, so a
text already embedded by phase 0 is reused rather than re-billed. Both cache sha256s are
recorded in the results file, as §3.4 requires.

---

## A2 — the §8 gauge's per-half class sizes (2026-08-19, before the gauge runs)

**Prereg §8** pins "11 classes at E2's exact half-sizes as produced by §7.2's construction:
[18, 19, 20, 20, 20, 20, 20, 20, 20, 29, 30], summing to **236** … the gauge uses the
**237-row half** … with the odd class rounded to give 237."

**Resolution, not a choice.** The stated vector mixes the two halves (it takes `axiomatic`'s
19 from one half and `epistemic`'s 18 from the other) and therefore sums to 236. The frozen
construction's seed-0 halves, measured in `out/unit_tests.json`, are exactly

* half 1: `axiomatic 19, axiotic 20, contingent 20, deontic 30, empirical 29, epistemic 19,
  nomological 20, ontological 20, pragmatic 20, procedural 20, structural 20` = **237**
* half 2: the complement = `20, 20, 20, 29, 30, 18, 20, 20, 20, 20, 20` = **237**

Rounding the prereg's `19` up to `20` — the operation §8 names — turns its vector into
`[18, 20, 20, 20, 20, 20, 20, 20, 20, 29, 30]`, which is **exactly half 2 sorted**. The gauge
uses that vector. Sum 237, minimum class 18, as §8 and §15-V3 both describe.

---

## A3 — §7.3's permutation floor for the taxonomy-vs-rival comparisons (before analysis)

**Prereg §7.3(2)** pins the governing p for every "A beats B, paired" claim to "the same 500
label permutations driving both arms".

**Implementation, declared.** For the C1-vs-C1P gap this is unambiguous: one permuted kind-label
vector is applied to both clouds. For `Ω_taxonomy > Ω_domain11` and `δ_taxonomy > δ_domain11`
the two "arms" are two *label vectors on one cloud*, so the same wording is implemented as:
permutation index *b* applies the **same item permutation π_b to both label vectors**, giving
`Ω(tax[π_b]) − Ω(dom[π_b])` as the paired null for the observed difference.

**Why not the alternative.** Permuting only the taxonomy labels while holding the domain labels
fixed makes the difference-null a rigid shift of the N1 null, so its p-value is *identically*
`p_N1` and the rival conjunct becomes a restatement of the first conjunct rather than a second
test. Both quantities are reported; the paired-π p is the governing one, and `p_N1` is printed
beside it so a reader can see they are not independent.

For the k-means rival the prereg already specifies the floor ("the permutation of the
taxonomy's labels with the rival refit inside each permutation"); k-means is label-free, so this
reduces to `p_N1` by construction and is reported as such.

---

## A4 — §12's VG2 null (before the positive control runs)

**Prereg §12** stakes `Ω_PC(k=3)` against "its own N1 null", where N1 (§7) is a free
label permutation.

**Implementation, declared.** The gate is evaluated on the **literal N1** — free permutation of
the mutation-family label across all rendered rows — exactly as pinned. A second null,
**permutation of the three family labels within each item**, is computed and reported beside
it, because the control's generative structure is one item contributing exactly one row per
class (rule 3: match the null to the generative structure). If the two disagree the
disagreement is reported; the gate is not switched.

Splits for the control are drawn **over items**, not over rows, so an item's three renderings
never straddle a split (rule 3, granularity is the item).

---

## A5 — interpreter split (before the diagnostics run)

The pinned venv `/home/emoore/CIRISOntology/scratchpad/temporal-share/qenv/bin/python` has
numpy and scipy but **no scikit-learn and no tokenizers**. All primary numerics run there.
Two auxiliary computations run under the system `python3` (numpy 2.4.0, scipy 1.16.3,
scikit-learn 1.8.0, transformers 5.8.1, tokenizers 0.22.2):

* **§11-D-B1**, the TF-IDF 1–2gram + logistic batch-detectability diagnostic (reported
  diagnostic; no verdict depends on it);
* **§3.4**'s client-side token counting for the truncation pass (V7).

No primary statistic crosses interpreters.

---

## A6 — the rival partitions are ANNIHILATED by the frozen nuisance matrix (2026-08-19,
##      discovered mid-run, recorded before the corrective computation ran)

**The defect, measured, not argued.** Prereg §4 puts **domain dummies (12 levels)** and
**batch dummies (40 levels)** into the nuisance matrix `Z`. Prereg §7.1 makes **domain-11**
the non-taxonomy rival, and §11-D-B2 makes **batch** a label whose Ω is to be reported.
On the residualized (`res`) arm — the PRIMARY arm — these are incompatible:

* `Z` = [1, log10(1+span), domain(11 drop-first dummies), batch(39)] spans, on any fitting
  half, every domain-class indicator and every batch indicator;
* `Prepared` fits β by least squares **on the fitting half**, so the residual there is
  exactly orthogonal to span(Z[F]);
* therefore **every domain-class mean and every batch-class mean of the residualized
  fitting half is exactly zero**, and the rival's contrast matrix is numerically zero.

**Measured on E2** (synthetic-cloud check, so no result is read from it):
`‖C_domain11‖_F = 2.95e-14` under Z=full against `5.68` under Z=none, while the taxonomy's
contrast norm is unaffected (5.115 vs 5.687). The counting identity's null vector, which
sits at 3e-15 relative for the taxonomy, sits at 1.3 for the annihilated rival — i.e. the
rival's Gram is roundoff, its numerical `rank(B)` comes back **11 instead of 10**, and
`Ω_domain11` on the `res` arm is the projection of the leading PCs onto an arbitrary
floating-point noise subspace. It is not a rival reading; it is a division of noise by noise.

**Consequences, stated in full and carried into the results file:**

1. On the `res` and `spandom` arms, **P1a's third conjunct (`Ω_taxonomy > Ω_domain11`) is
   satisfied trivially and carries no information**, and the same is true of **K1b**, of
   **P1d's δ-privilege conjunct** and of **K1d**. They are reported as computed and
   simultaneously marked STRUCTURALLY UNINFORMATIVE ON THIS ARM.
2. **§11-D-B2's `Ω` with batch as the label is annihilated the same way** on the `res` arm.
3. The `raw` arm (`Z` = [1]) is uncontaminated and its rival comparison is real.

**The corrective computation, declared before it runs.** One additional post-freeze arm,
`rivalnodom`: the identical pipeline on the primary embedder with
`Z` = [1, log10(1+span), **batch(39)**] = 41 columns — the frozen `Z` with **only the term
that defines the rival removed**. N1 only (500 permutations, the same seed and the same
paired-π construction of A3). Its sole use is to make the rival conjunct evaluable; it is
**not** promoted to primary, it does **not** replace the pinned `res` arm's numbers, and the
pinned numbers are reported beside it. D-B2 is likewise recomputed with
`Z` = [1, log10(1+span), domain(11)].

**What this does not do.** It does not lower any gate, move any band, or change any verdict
rule. If the rival conjunct fails on `rivalnodom`, that is reported as a fired conjunct.

---

## A7 — §12's M1 trigger count differs from the prereg's pre-freeze measurement (2026-08-19)

**Prereg §0.1 / §12** record three kind-blind trigger marginals measured before the freeze:
M1 modal **272**, M2 numeral **208**, M3 negation **451**, three-way intersection **95**.

**Measured at run time:** M2 = **208** and M3 = **451** reproduce exactly. M1 = **278**, six
more than the pre-freeze count, so the intersection is **N = 99** rather than 95.

**Cause.** My M1 implementation matches `\b(may|should|must|will|can)\b` **case-insensitively**;
the pre-freeze count evidently did not, or bounded the token differently. This was promoted from
a prose note in the results file to a numbered amendment because it is a departure from a number
the prereg states, however small.

**Effect on any verdict: none.** §12's floor is `N ≥ 60` and the VOID branch is `N < 60`; 99 and
95 are both far clear of it, and every item still contributes exactly one rendering to each of
the three classes, which is the property the C8 fix required. The substitution table
(may→must, should→must, must→may, will→may, can→must) is the prereg's, unmodified.

---

## A8 — a configuration change made after seeing an unfavourable cell (2026-08-19)

**Recorded after the fact, which is itself the deviation.** A6 pre-registered the corrective
arm as **"N1 only"**. The ordering was:

1. `rivalnodom` ran with N1 only and printed **CHANGE-READ, TAXONOMY-NULL**;
2. `analysis.py` was then edited to add **N1b** to that arm's null list — beyond A6's text, and
   after the unfavourable cell had been seen;
3. the arm was re-run and returned **CHANGE-CARRIED ALIGNMENT**.

**Unfavourable cell → configuration change → favourable cell.** Stated in that order in
`EIGEN2_RESULTS.md` §18.1, without gloss.

**Why the change was correct.** §9.2 makes N1b a *required conjunct* of P1a and the assembly
code defaults a **missing** conjunct to `False`; N1b had never been computed on that arm, so the
first cell was a configuration bug, not a measurement. **Adding a required conjunct can only
make DETECTED harder to reach, never easier**, so the repair cannot manufacture the favourable
outcome — and the conjunct it added passed at the 0/500 floor.

**What is checkable.** N1 resumed from the on-disk checkpoint, so the rival conjunct — A6's only
purpose — is computed on **the same 500 draws before and after**, and its value is unchanged at
**+0.20771, 0/500**. Only the force-failed N1b conjunct changed, to 0.001996 (0/500).

**The lesson, recorded against the next run:** configuration belongs in the amendment, written
before the run. Here it was not.
