# ATLAS UNIV-1 — the universality-of-constants fork (FROZEN 2026-08-22, before any cross-substrate constant was computed)

## Question
Are the object's measured constants substrate-independent (a law of recognition) or
substrate-contingent (an ecology)? This is the decisive leg of the comparison method
(COMPARISON_METHOD.md §4) and the atlas's first instrument.

## What was already seen (disclosed before running)
- ANCHOR (CUR-P2, curated corpus × PANEL-2): cascade 0.359/0.198/0.103 (r≈0.53), twin
  swap-asymmetries 5.8%/19.2%, S5=0.3985, 4+7 percentile 99.7% — ALL SEALED in Legs A/B.
- CUR-SP (same corpus × standing panel): the boundary TRIO (Premises/Facts,
  Structure/Manner, Model/Facts) sealed in the original study. Cascade/twin constants
  NEVER computed.
- B5 sealed a prior expectation: channel IDENTITIES differ between curated and
  Babel/wild instruments. So leg U-channels runs with a partially anticipated direction
  (toward DRIFT); U-cascade and U-twins are genuinely blind cross-substrate.
- No other substrate's constants have been computed. The runner below was written and
  frozen before its first execution.

## Substrate roster (frozen)
S-axis (the fork's substrates — distinct corpora):
- CUR: curated authored corpus. Two instruments: CUR-P2 (anchor, PANEL-2) and CUR-SP
  (standing panel, 5418 rows). TYPE T (truth-anchored).
- BAB2: babel2 authored corpus (330 rows). TYPE T.
- LEGC2: wild multi-stream units × PANEL-2 (1035 rows). TYPE D (disagreement).
- ECO family, wild streams × standing panel, TYPE D: ECO (510), STACKEX (180),
  ECO2 (180), ECO2W (147). Rule: score each separately if it passes gates; failers are
  pooled into ECO-POOL; ECO-POOL scored if it passes.
EXCLUDED with reasons: A0 traces (override near-determinism fouls kind tests — memory
gate; hash-keyed schema), gauge-test arms (manipulated corpora), pilot/partd (feeder
subsets of CUR), H3ERE2/heldout files (held-out reuse forbidden), polarity (no kind
judgment field), 29-language dump (lexicalization data, not change-confusion).
I-axis (instrument robustness, reported but NOT in the fork): CUR-P2 vs CUR-SP.

## Estimators (the runner atlas_runner.py IS the definition; sha recorded in results)
- TYPE T matrix: target-kind × modal-kind counts over the 11 artifact-local kinds,
  row-normalized. Channels = 110 directed off-diagonal entries.
- TYPE D matrix: for each item, each unordered pair of valid judge kinds with a≠b adds 1
  to symmetric S[a,b]. Channels = 55 undirected entries, share-normalized.
- C1 cascade: tier_k = MEAN of channels ranked [3k+1..3k+3] by size (k=0,1,2), on the
  matrix's own channel set; r = geometric mean of tier2/tier1 and tier3/tier2.
  (Exactly reproduces the sealed anchor 0.3588/0.1978/0.1032 on CUR-P2.)
- C2 twins: swap-asymmetry |PMP−M|₁/|M|₁ for the two named pairs (Priorities,Process)
  and (Structure,Circumstances); plus (TYPE T only) relative diagonal difference per pair.
- C3 localization: S5 = top-3 channel share of off-diagonal mass; and the 4+7 block
  within-share percentile among all 330 four-subsets (directed for T, symmetric for D).
- C4 channel identity: the top-3 channels as UNORDERED pairs (directed collapsed).

## Nulls (frozen)
- PERM: 200 draws; each judge's kind labels permuted across items independently
  (preserves judge marginals, destroys item structure). Same estimator on each draw.
- NULL-CAL for C1: if the anchor's r lies within [p5,p95] of its own PERM-null r
  distribution, the cascade leg is declared UNINFORMATIVE-AS-STATISTIC and drops from
  the fork (reported, not scored). A geometric-looking cascade from rank-sorting alone
  is generic; this calibration is the name-the-number discipline applied to B1.
- JACC-NULL: expected pairwise Jaccard of independent uniform 3-of-55 subsets,
  10,000 draws.

## Gates (a substrate scores only if ALL pass)
- G1: ≥80 off-diagonal events (T) / ≥80 disagreement pair-events (D).
- G2: judged-kind marginal entropy ≥1.2 nats.
- G3: ≥40 distinct items.

## Fork criteria (frozen)
- U-cascade (if informative per NULL-CAL): CONVERGENT if every scoreable S-axis r ∈
  [0.35,0.80]; DRIFTED if ≥2 substrates outside [0.25,0.95]; else MIXED.
- U-twins: CONVERGENT if the anchor ordering asym(St,Ci) > asym(Pr,Pc) holds in ≥3/4 of
  scoreable substrates AND each pair's magnitude is within ×3 of the anchor's;
  DRIFTED if the ordering flips in ≥1/2; else MIXED.
- U-channels: mean pairwise Jaccard of top-3 unordered channel sets across scoreable
  S-axis substrates. CONVERGENT if ≥3× JACC-NULL mean AND ≥1 channel present in ≥3/4 of
  substrates; DRIFTED if ≤1.5× JACC-NULL; else MIXED.
- U-localization: CONVERGENT if S5 > own PERM p95 in every scoreable substrate; MIXED if
  in all but one; DRIFTED otherwise.
- FORK: LAW-LIKE if ≥3 legs CONVERGENT and none DRIFTED; ECOLOGY if ≥2 DRIFTED;
  else INTERMEDIATE (reported as measured; no forced call). A leg dropped by NULL-CAL
  reduces the denominators accordingly (LAW-LIKE then needs all remaining legs
  CONVERGENT and none DRIFTED).

## Meaning of every outcome (staked)
- LAW-LIKE: the constants are substrate-independent → the strong-sense physics-likeness
  survives its hardest test to date; the Logos-as-common-account reading gains its first
  cross-substrate measured support. NOT yet a page claim — steward review required.
- ECOLOGY: the constants are substrate-contingent → the object is real-but-ecological;
  the strong reading is KILLED at the constants level (structure may still be universal
  — that remains Leg A's separate result). Report the kill plainly.
- INTERMEDIATE: neither; the atlas needs more substrates (human labels, the block-scoped
  agent stream) — named successors, no verdict.
Caveats staked now: all substrates here are LLM-panel instruments — a shared-panel
correlation exists (CUR-SP/ECO share one panel; CUR-P2/LEGC2 share another); PANEL-2 and
the standing panel are disjoint model sets, which is the strongest available decoupling.
Human-label replication remains owed regardless of outcome. Wild TYPE D and authored
TYPE T matrices estimate different conditionals; cross-type comparisons are reported
within-type first, cross-type descriptively.
