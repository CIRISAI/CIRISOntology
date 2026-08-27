# Pre-registration — TIER-3: the settling-dose law

**2026-08-27, frozen before either target runs; admissible only if the audit
exits 0.** The organization discovery replicated with a three-point
dose-response (momx residual 14.9 → 12.3 → 2.53 at warm-up 60 → 90 → 150,
adjudicated rounds). This round stakes it as a LAW on two never-run doses:
warm-up 30 (fresher than any measured scene) and warm-up 120 (interior).
Binary exit: **CONFIDENCE ⇔ all posable arms pass; FALSIFICATION ⇔ any posable
arm misses.** No rescue.

defects: D-UNITS (residuals are ratios of ratios — dimensionless; level law is
a rank correlation), D-FRAME-ZERO (construction premise reads the pre-step
meta line), D-DET (deterministic engine; interventional twin construction),
D-IDENT (id-keyed joins and coefficients).

gauge: scratchpad/omega/gauge_dose.log
gauge: scratchpad/omega/gauge_battery.log

Family-wise: Bonferroni over the 7 staked readings (D1, D2, D3, D4 × 2
targets, D5 × 2 targets).

## Frozen execution

`tier_closure_probe <dir> 2400 30` and `tier_closure_probe <dir> 2400 120`;
adjudicators `tier_battery.py` + `dose_adjudicate.py` as committed at this
freeze. INSUFFICIENT PAIRS (exit 2) or a failed construction premise VOIDs
that target; either target voiding VOIDs the dose arms (D1–D3 need both).

| arm | stake (numeric) | witness: | posability |
|---|---|---|---|
| D1 organization at 30 | momx residual > that run's random p75 | witness: none (the discovery at a fresher dose than ever measured; a fire says organization needs settling) | three adjudicated doses read 14.9/12.3/2.53 — the quantity moves; planted no-organization FIRES (gauge_dose.log) |
| D2 monotone dose | momx_resid(30) > momx_resid(120) | witness: none (the dose law's direction) | planted inversion FIRES |
| D3 interpolation | momx_resid(120) ∈ [2.53, 12.34] — the adjudicated bracketing neighbors | witness: none (the dose law's continuity; both exit prongs gauged) | planted low (1.2) and high (13.5) each FIRE |
| D4 early level law (× 2 targets) | Spearman(div_v, P_v) ≥ 0.8 at f = 300 ONLY — the law at its TIER-2-adjudicated scope; the late-time form is dead and not re-staked | witness: `sum_perturb_le` — the ceiling theorem; two rule-6 confirmations already (0.830, 0.880) | planted decorrelation reads 0.29 and FIRES (gauge_battery.log) |
| D5 budget (× 2 targets) | rise-epoch K ≤ 1.05; rise < 20 frames ⇒ VOID | witness: `interventional_iff_closed` frames the probe; the band is the `Aggregation` budget, unbreached in four geometries (1.0001–1.0044) | planted K = 1.087 FIRES |

Exits: CONFIDENCE — the settling-dose law stands with the discovery confirmed
at a fresh dose, the early level law gains two more rule-6 confirmations, the
budget two more geometries. FALSIFICATION — the named component dies: D1 →
organization needs settling (scoped, marked); D2/D3 → not a dose LAW (the
replication stands, the law dies); D4 → the early level law; D5 → the budget.
