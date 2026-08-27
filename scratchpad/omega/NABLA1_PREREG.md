# Pre-registration — NABLA-1: the engine's dynamical connection

**2026-08-27, frozen before the staked run; admissible only if the audit exits
0.** The ∇-face's first engine instrument (the OWED row): a mass-weighted
connection transporting intensive fields (momx/mass, ke/mass) around a
half-cell plaquette of charts, against the DERIVED uniform-weight holonomy
operator (exact, parameter-free): loop = (I+Δx/4)(I+Δy/4), so
H_pred = (Δx+Δy)φ/4 + ΔxΔyφ/16. The measured loop runs on the scene's own
mass field, so agreement is a law, not an identity. Binary exit: **CONFIDENCE
⇔ both posable readings pass; FALSIFICATION ⇔ either misses.** No rescue.

defects: D-UNITS (H_meas and H_pred are the same intensive units by
construction; slope is dimensionless), D-FRAME-ZERO (no frame-zero band —
all readings at sampled frames ≥ 90), D-DET (deterministic engine; the probe
is the chart loop itself, a context-axis motion, not an observational closure
stake), D-IDENT (fields are binned by position; no node-index comparison
anywhere in the chain).

gauge: scratchpad/omega/gauge_nabla.log

Family-wise: Bonferroni over the 2 staked readings (V1 × {momx, ke}).

## REFUSED ARMS, recorded (an arm that cannot fail is refused)

- **V2 (state-dependence localizes at mass contrast)**: the substrate's
  live-region cell-mass contrast is 1.1× and the surface band contributes ZERO
  high-contrast live samples (checked pre-freeze on labelled smoke) — no
  lever, refused.
- **V3 (commutation of transport with the step)**: at contrast 1.1× both
  sides are the same near-linear functional and the correlation is ~1
  tautologically — refused for the same reason the in-sample mixing bound was.

## Frozen execution

`nabla_probe <dir> 60 16 30 90` (warm-up 60; 16 samples at stride 30, frames
90–540; deterministic alternating re-throws every 90 frames keep the scene
live — smoke read 13 valid cells per sample against a 100 floor without them).
Adjudicator: `nabla_adjudicate.py` as committed at this freeze; validity =
transport and prediction both defined and the source field live; n < 100 ⇒
VOID.

| arm | stake (numeric) | witness: | posability |
|---|---|---|---|
| V1-momx | Pearson(H_meas, H_pred) ≥ 0.99 ∧ slope ∈ [0.90, 1.10], pooled interior cells, n ≥ 100 | witness: `curvature_iff_held` — Held on the context axis is zero curvature, and the derived operator is the quantitative form of NOT-Held for this connection; `holonomy_commutes_with_rate` frames why the loop is a lawful motion | design smoke (labelled): r = 0.9999, slope 1.010, median deviation 2.8% — the frozen run extends 3× beyond it in time with three MORE throws; planted coefficient errors ×2 and ÷2 both FIRE the slope band (gauge_nabla.log) |
| V1-ke | same bands on the ke-intensive field | witness: `curvature_iff_held` | same gauge; ke is the χ = 1 chart, so its φ is the best-conditioned field the connection carries |

**Premise (VOID, not miss)**: the uniform-weight null control — the pipeline
run with all weights 1 must reproduce H_pred to ≤ 1e-12 (the derivation is
EXACT for uniform weights; gauge read 1.2e-16). A violation is a pipeline
defect, not physics.

Exits: CONFIDENCE — the ∇-face has its first measured engine law: the
connection's holonomy is the derived operator within 10% at this contrast.
FALSIFICATION — the derived operator is wrong for the realized connection;
the deviation field is the diagnostic, and the OWED row stays owed.
