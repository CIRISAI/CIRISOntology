# Eigen-alignment v2 — design (2026-08-19, from v1's measured defects)

v1 verdict: NOT DETECTED, with three specific, measured causes. v2 fixes each, and keeps
the calibration/test separation clean: constructions are selected on CORPUS A (already
burned by v1), the taxonomy is staked ONLY on the new corpus.

## The three defects -> three fixes

1. **K1c fired: Δ = e(after) − e(before) reads LESS kind-structure than raw documents**
   (0.060 vs 0.134, 100% of splits). The measured panel mechanism says site cues live in
   the SURROUNDING text — which subtraction cancels. → **Phase 0, construction bake-off**
   on corpus A: (C1) mechanical span-in-context, one embedded rendering of
   before-sentence/after-sentence; (C2) concatenated pair [e(ctx_b); e(ctx_a)] — no
   subtraction; (C3) e(after) residualized on e(before) per split; (C4) v1's Δ as
   baseline. Embedder arms: bge (v1 primary) and Qwen3 WITH an instruction prefix
   steering toward change-kind. Winner = best null-separated Ω(11) that also beats its
   placebo. LABELED: instrument calibration, no taxonomy verdict, corpus A is spent.
2. **Batch confound + power** (V11 fired both-within-batch; surface says n≈500 reaches
   Ω≈0.27 at signal-scale 2). → **The interleaved rebuild**: 40 authoring batches × 12
   items, ONE PER KIND PER BATCH (kind ⊥ batch by construction — V11 retires), domains
   rotated, difficulty stratified (9 clear + 3 hard-boundary per batch), single-span
   verified mechanically, ~480 items ≈ 4× corpus A.
3. **Rank resolution** (gauge σ_R = 0.92; R_kind read 0). → P1b stays Tier-1-banded in
   v2 unless the 8× surface rows say otherwise; the sharp claim waits for the corpus or
   instrument that earns it.

## Sequence (freeze discipline unchanged)

Phase 0 (calibration, corpus A, running) → prereg v2 drafted + adversarially refereed +
frozen, staking the chosen construction, n from the power surface, detection-primary /
strength-banded verdicts, K1c-style placebo as a REQUIRED gate, rival partitions kept →
panel annotation of the new corpus (BASE × 3) → the run → verifier. The new corpus
never touches an embedder before the freeze.

## What v2 cannot be blamed for in advance

If the winning Phase-0 construction still reads null on the NEW corpus at 4× power with
the placebo gate passed, that is a REAL null of the geometry hypothesis, not an
instrument excuse — and eleven-plus-one's geometric leg is closed as measured-absent,
with the label-level results standing on their own.
