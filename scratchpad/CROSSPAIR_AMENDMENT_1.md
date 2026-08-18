# CROSSPAIR AMENDMENT 1 — budget-forced reductions, committed BEFORE any circuit is submitted

Measured quota at design time: **106 s remaining** of 600 (period ends 2026-08-18 16:14 UTC,
reset behaviour unknown). The prereg's shape assumed a fresh window; the steward's call is to
run now. Reductions, each stated with what it costs:

1. **Basis combinations 4 → 2.** Same-basis only (ZZ⊗ZZ, XX⊗XX). Mixed combos are zero in QM
   and carry no staked prediction; same-basis is the natural channel for any shared-medium
   correlation and is what the entanglement_ledger shadow result licenses. Cost: no
   mixed-basis bound this run.
2. **Shots 8192 → 3072 per cell.** Per-cell correlator floor 1/√3072 ≈ 0.018; the published
   bound per separation lands near **|E_excess| ≲ 0.05 at 3σ** after control subtraction and
   basis pooling. Cost: a weaker ε(d) than designed; still a gauged bound, which is the
   deliverable.
3. **Preparations: bell + |00…0⟩ + |++…+⟩** (3, as pre-registered — no reduction).
4. **Separations: 4 values** on the coupling map, intra-pair distance fixed at 1 (no change).
5. **Two jobs only** — screen (≈2×2048 shots) then ONE batched main job (24 circuits × 3072).
   No retry exists inside the quota; a failed main job ends the campaign for this window and
   is reported as such.

Everything else in `CROSSPAIR_PREREG.md` — controls, interleaving within the batch, the
excess-over-floor reporting rule, the S2 shape discriminant (AIC ≥ 10), K1 — unchanged.
