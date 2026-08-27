# Pre-registration — Ω-KILL-3: the TUPLE test

**2026-08-26, frozen before any staked run launches; admissible only if
`Audit/prereg_audit.py` exits 0 on this file.** The successor freeze the
invariant hunt demanded: Ω tested AS THE TUPLE — the repaired composition arms
as the premise-check backbone plus four arms aimed at components (μ, g, the
tier/view axis) that have never had a kill run at them. Binary exit:
**CONFIDENCE ⇔ every POSABLE arm passes; FALSIFICATION ⇔ any posable arm
misses.** No rescue; every VOID path is named below and closable from readings
alone.

defects: D-IDENT (REPAIRED at root — all engine observables join twin sessions
BY HOLON ID, never node index; `certify_at` renumbering cannot touch an id-join),
D-MATERIALIZE (all onsets threshold-relative at 1% of max via onset_analyzer.py;
re-certification dust cannot fire a band), D-CHAN-DRIFT (both QPU circuit sets
pinned to QPY — backbone sha256 71aba242…, N2 set sha256 70703201…; plus the
in-job one-way premise check below), D-EPOCH (every floor, reference, and
constant in-job; nothing frozen from a pilot epoch), D-GATE (all couplings
staked on realized channels; the planted validation of the analysis path uses
ideal-unitary counts and is labelled as such), D-DET (every engine arm is
interventional — probed vs sham twin, or micro-displaced vs reference twin;
observational closure is not staked on the deterministic substrate), D-BOUND-DOB
(the mixing bound is staked OUT-OF-SAMPLE only: alpha frozen on the train
split's L-step kernel, defect read on the held-out split; the in-sample form is
refused as unfalsifiable, the lag-1 out-of-sample form was ALSO refused when the
train side read alpha = 1 by disjoint support — the same absorption mechanism —
and gauge_n1.log demonstrates the staked L-step form CAN fire).

gauge: scratchpad/omega/gauge_omega2.log
gauge: scratchpad/omega/gauge_n1.log
gauge: scratchpad/omega/gauge_n2.log
gauge: scratchpad/omega/gauge_n34.log
gauge: scratchpad/omega/gauge_idjoin.log
gauge: scratchpad/omega/omega3_validate.log

Family-wise: Bonferroni over the 13 staked arms; all QPU floors at the 99.5th
percentile of in-job permutation nulls (2000 reps); N1 bands carry 3-sigma
chain-block bootstrap; N2 bands carry 3-sigma binomial shot error at 4096 shots.

## Frozen execution parameters

- QPU: ibm_marrakesh, pair (95, 99), ONE job = 20 pinned backbone circuits +
  17 pinned N2 circuits, 4096 shots (`s1_omega3.py submit`). N2 staked qubit =
  circuit qubit 0 = physical 95, frozen by fiat here (the screen record is
  per-pair and cannot rank the two); qubit 99 is an unscored replicate,
  reported alongside.
- Engine S2 fresh run: `idjoin_probe` at probe offset factor **0.3** (vs 0.2 in
  the prior campaign — a fresh probe geometry), probe frame 240, 2400 frames.
- Engine N3/N4 run: `tier_closure_probe <dir> 2400 60` (2400 frames, 60 warm-up
  frames stepped identically on both twins before the swap — a fresh session is
  all-asleep at exactly zero velocity, so an unwarmed swap is a no-op), 8×4 cell
  grid, ≥ 100 swapped equal-mass free-awake pairs required (the instrument exits
  2 otherwise — VOID-PREMISE, not a fudge). Adjudicator: `analyze_tier.py`,
  frozen. Views: 9 symmetric per-cell velocity moments standardized by frozen
  first-frame scene scales; the declared views are the three conserved-quantity
  directions (momx, momy, ke) in that space; comx is reported, unstaked; the 64
  random views are unit directions in the same space — every view is exactly
  blind to the swap at frame 0 (an earlier per-grain control was refused as
  unfair-by-construction: it read the swap itself while declared views read ULP,
  so the comparison would have fired on geometry, not physics).
- N1: erasure chained streams, Basic protocol, even-index chains = train,
  odd-index = test; fiber thresholds train-frozen; UNBLIND=1 gates the test side.

## S1 — QPU backbone (bands inherited from the Ω-KILL-2 freeze + banked repairs)

| arm | stake (numeric) | witness: | posability |
|---|---|---|---|
| A1 idle | both directional defects ≤ 3× floor | witness: `independent_views_closed` — hypothesis "product map": no gate between the pair; μ: hardware noise is physical | idle readings varied 0.1×–1.67× across sessions |
| A2 one-way CRX | fwd ≥ 50× floor ∧ fwd ≥ 5× reverse; **premise (in-job): reverse ≤ 10× floor, else VOID-PREMISE** | witness: none (directed detection) | fwd 298–510×, reverse 0.2–137× across epochs — both vary |
| A3 hop | both ≥ 10× floor ∧ max/min ≤ 3 | witness: none (realized symmetric exchange) | 31–75× and asym 1.17–1.52 across three jobs |
| A4 common-driver | both ≤ 3× floor ∧ created ≥ 50× its floor | witness: `common_driver_probe_null` — hypothesis realized by construction: one classical bit drives X⊗X | created 0.606–0.624 three times; defects 0.0× three times |

## S2 — engine backbone (fresh geometry, id-join observables)

| arm | stake (numeric) | witness: | posability |
|---|---|---|---|
| B1 sham twins | id-joined per-grain divergence exactly 0 at all 2400 frames ∧ join full (0 unmatched) | witness: none (geometry-seeded twin determinism) | one-ULP nonzero fires (gauge); prior campaign read 0/2400 |
| B2 pre-probe | exactly 0 at all 240 pre-probe frames | witness: none (same fact) | same two sides |
| B3″ per-grain light-cone | left-sector onset before right-sector onset, gap ≥ 10 frames, onsets at 1% of each sector's max | witness: none (finite contact propagation) | prior run: left 324, right 1047, gap 723; planted gap 2 fires |
| B4′ K | median growth ratio of total divergence (divL+divR) over the RISE EPOCH only — frames ≥ 245 from the total's 1%-of-max onset to its first frame ≥ 90% of max — ≤ 1.05; rise epoch < 20 frames ⇒ VOID (unposable) | witness: none (`Aggregation` non-expansiveness, measured 1.0012/1.00444/1.00439 on three instruments; the plateau-including window form was refused pre-freeze — a planted saturating expander read K = 1.0 on it, plateau domination, D-MATERIALIZE's mechanism at the other end of the curve) | planted K = 1.078 FIRES through the real adjudicator; instant rise VOIDs (gauge_idjoin.log) |

## N — the four new arms (components never yet under fire)

| arm | stake (numeric) | witness: | posability |
|---|---|---|---|
| N1 out-of-sample mixing bound | **the lag-1 form is REFUSED, recorded**: on the real train split alpha_hat(lag-1) = 1.000 by disjoint one-step support (states 0,7), making that bound ≥ 1 — vacuous, an arm that cannot fail. Staked form, by rule not by number: base lag L = the smallest train-diagnostic lag with alpha_hat < 0.9 (here L = 16, alpha_hat = 0.404); held-out defect(k·L) ≤ alpha_hat_train(L-step kernel)^k + 3σ_train(k·L) for ALL k ∈ {1,2,4} — frozen bounds 0.420358 (lag 16), 0.181323 (lag 32), 0.042828 (lag 64), each non-vacuous with margin ≥ 0.58 to the TV ceiling; the k=1 rung can fire only through train/test kernel drift (in-sample it holds identically by data processing), so the extrapolation content lives at k ≥ 2 — stated, not hidden | witness: `defect_le_alpha_pow` — hypotheses: one kernel, Markov step, alpha its Dobrushin coefficient, applied to the L-step chain; the arm tests whether that premise package extrapolates across the split on a wild substrate; the train diagnostic's non-submultiplicativity (alpha_hat(32) = 0.44 ≫ 0.404²) is why the arm is live | train-side chain-bootstrap spread (0.031–0.038) + 12/12 pair-count guard at every staked lag (`n1_train_side.log`); gauge PASS at all k, FIRE at k=4 (margin +0.085), and a MATCHED Markov control of the fire construction's own observed statistics passes everywhere — the violation is attributable to hidden-regime memory, not chart relabeling (gauge_n1.log) |
| N2a rent bracket | for every dose p ∈ {2,4,8,16}: R(p, C=2) within [min−3σ, max+3σ] of the two point predictions Pinf+(s0eff−Pinf)·λ_fast^p and ·λ_slow^p, all quantities in-job; **premise: decay ladder monotone non-increasing within 3σ√2, else N2a and N2b VOID-PREMISE** | witness: `rent_closed_form` (per-mode linear recursion) + `Ginf_at_Wstar`; the bracket is GCOST_DERIVATION §4.2 (nonneg mode weights ⇒ retention between the single-mode laws at the fastest and slowest observed modes); this substrate class already killed a decay-shape claim once (stretched-exponential record), which is what makes the arm live | planted single-mode and two-mode pass inside band; planted fast-channel dose FIRES (gauge_n2.log); predictions span R ≈ 0.03–0.85 across the dose axis |
| N2b cycle-memory | for every dose p: |R(p, C=4) − R(p, C=2)| ≤ 3σ√2 | witness: none (the fresh-deposit/Markov premise of the rent model, genuinely violable by environment memory across repairs) | planted 6% per-cycle deposit heating FIRES (gauge_n2.log) |
| N3 tier closure within budget | coarse divergence = standardized L2 of the 3 declared views; conjuncts, each numeric: (i) frame-0 coarse divergence ≤ 1e-9 × max micro divergence [construction premise]; (ii) median over frames 1200–2399 of coarse/micro ≤ 0.5; (iii) median per-frame growth ratio of coarse divergence, restricted to frames above 1% of its max, ≤ 1.05; posability gate: median micro over frames 1200–2399 ≥ 0.25 × median over frames 0–59, else VOID (dead transient) | witness: `interventional_iff_closed` — the micro-displaced twin IS the fiber-internal probe; a nonzero coarse response reads non-closure, and the stake is the `Aggregation` budget on it | gauge fires (ii) on planted amplification and (iii) on planted budget-burst, prongs named; planted dead transient VOIDs; smoke: micro sustained at ~2e-2 with declared views climbing |
| N4 view privilege | growth ratio g_v = median(div_v, frames 1200–2399) / median(div_v, frames 60–300), per view; all 3 declared g_v below the 25th percentile of the 64 random g_v; FIRES if any declared g_v exceeds the random median | witness: none (privileged-scale selection claim; a fire convicts "the declared tiers are the closed views" as post-hoc naming) | planted privileged passes, planted equalized FIRES, both through the real adjudicator (gauge_n34.log) |

## Exits (data-closable; branches pre-committed)

- **CONFIDENCE**: every posable arm passes. This is the first freeze in which
  the tuple's μ-face (N1), g-face (N2), and tier/view-face (N3/N4) can each
  fail separately; a pass is confidence in Ω AS THE TUPLE at tested scope.
- **FALSIFICATION**: any posable arm misses → the named component of the tuple
  is convicted at its stated scope; the verdict sentence names the arm and the
  component. No rescue; misfits go to the registry.
- **VOID paths** (each named, none scored as pass): A2 premise (reverse > 10×
  floor → channel-structure drift epoch, D-CHAN-DRIFT); N2 premise (non-monotone
  ladder → mode-weight assumption unposable); N3 premise (insufficient
  equal-mass pairs, exit 2); N1 posability (comparable-pair count below guard);
  device failure voids its substrate's arms; if BOTH engine and QPU void, the
  test VOIDs.
- **The record's own advance prediction, scored separately**: REANALYSIS.md
  predicts the 8 backbone arms read 8-posable-for-8 under the banked repairs.
  A premise-void among the backbone misses THAT prediction (a hit on the
  prereg-discipline claim, logged as such) without touching the tuple verdict,
  which runs on posable arms only.

Verdict sentences: `COMPOSITION2_PREREG.md` §0's, with "tuple". Onsets:
`onset_analyzer.py` (1% of max). Analysis scripts frozen at this commit:
`s1_omega3.py`, `oos_mixing.py`, `analyze_tier.py`, `analyze_idjoin.py`,
`tier_closure_probe.rs`, `idjoin_probe.rs`.
