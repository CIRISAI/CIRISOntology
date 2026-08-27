# Pre-registration — TIER-2: the battery round on fresh targets

**2026-08-27, frozen before either target runs; admissible only if
`Audit/prereg_audit.py` exits 0.** The standing tier validation battery
(`tier_battery.py`, born from Ω-KILL-3's N3/N4 misses and their misfit pass)
runs on TWO fresh targets: the same scene at warm-up 90 and warm-up 150 —
different awake sets, different swap sets, different relaxation stages than
anything measured. Binary exit: **CONFIDENCE ⇔ every posable arm passes on
BOTH targets; FALSIFICATION ⇔ any posable arm misses.** No rescue.

defects: D-UNITS (every band is dimensionless — standardized divergences,
ratios of ratios, rank correlations — or names its units; the Ω-3 N3 lesson is
built into the battery), D-FRAME-ZERO (the construction premise reads the
PRE-step raw-moment line from meta.txt, which the instrument emits at exactly
that frame), D-DET (the substrate is a deterministic engine; the arms are
interventional — macro-matched micro-different twin sessions ARE the probe),
D-IDENT (all joins and random-view coefficients are keyed by holon id, stable
under renumbering).

gauge: scratchpad/omega/gauge_battery.log

Family-wise: Bonferroni over the 10 staked readings (5 arms × 2 targets).

## Frozen execution

`tier_closure_probe <dir> 2400 90` and `tier_closure_probe <dir> 2400 150`,
adjudicated by `tier_battery.py` exactly as committed at this freeze. The
instrument refuses under 100 effective swaps (exit 2 → that target VOID, named:
a longer warm-up settles the scene and may empty the awake set). If BOTH
targets void, the round VOIDs.

## The arms (bands identical on both targets)

| arm | stake (numeric) | witness: | posability |
|---|---|---|---|
| T-construction | PREMISE: pre-step raw-moment L2 ≤ 1e-12 (VOID, not miss) | witness: none (permutation of identical summands; measured 3.0e-18 on the prior geometry) | planted post-step reading (3e-4) VOIDs |
| T-budget | median growth ratio of standardized 3-view coarse divergence over its RISE EPOCH (1%-onset to first ≥ 90% of max) ≤ 1.05; rise < 20 frames ⇒ VOID | witness: `interventional_iff_closed` frames the probe; the band is the `Aggregation` budget; the plateau-including form is refused (plateau domination — the Ω-3 B4′ lesson, applied to its own successor) | planted K = 1.087 FIRES; prior geometry read 1.0001 |
| T-levels | Spearman(div_v(f), P_v(f)) ≥ 0.8 across all 67 views at BOTH f = 300 and f = 1200 | witness: `sum_perturb_le` — the conditioning ceiling is the theorem; the staked correlation is the empirical law that realized divergences track their ceilings, measured once at +0.996/+0.935 and staked here as a rule-6 forward prediction | planted decorrelation reads +0.29 and FIRES |
| T-organize | momx growth residual (measured growth ÷ ceiling growth) > the 64 random views' residual p75 | witness: none — the organization DISCOVERY replicating or dying: on the prior geometry momx read 14.9 vs random p75 ≈ 7; a fire says it was geometry-specific | planted no-organization (residual 1.0) FIRES |
| T-protect | ke growth residual < the random views' residual p25 | witness: `coherence_of_nonneg` — ke is the protected all-nonnegative chart, coherence exactly 1 at every measured frame; the stake is that its DYNAMICS also avoids it (prior: 1.46 vs p25 ≈ 5) | planted unprotected ke FIRES |

## Exits

- **CONFIDENCE**: all posable arms pass on both targets — the conditioning
  level law gains two rule-6 confirmations and the organization/protection
  pattern replicates across relaxation stages.
- **FALSIFICATION**: any posable arm misses — the verdict names the component:
  T-budget → the `Aggregation` budget at tier scope; T-levels → the
  conditioning level law; T-organize/T-protect → the organization reading dies
  as geometry-specific and is marked dead.
- **VOID paths**: construction premise; rise epoch < 20 frames; INSUFFICIENT
  PAIRS exit 2 per target; both targets void ⇒ round void.
