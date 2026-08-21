# PANEL-2 — a stronger model panel, validated as a NEW NAMED INSTRUMENT
# FROZEN 2026-08-21, before any new-panel call ran.

Motivation: the instrument ladder (LEGC_RESULTS run 2). The standing 3-family panel
(Llama-4-Scout / gpt-oss-120b / gemma-3-27b) is frozen for all standing baselines (G1
comparability) and is NOT modified. PANEL-2 is a separate instrument: families
deepseek-ai/DeepSeek-V3.1 · Qwen/Qwen3-235B-A22B-Instruct-2507 ·
moonshotai/Kimi-K2-Instruct (three distinct labs), temperature 0, stateless, the
unchanged plane_annotate prompt.

VALIDATION SET: the curated corpus (corpus_full.jsonl, 248 items) at BASE — the substrate
where the standing panel measured kappa 0.687.

LICENSE CRITERIA, all three required, staked now:
- L1: PANEL-2 Fleiss kappa >= 0.60 on the validation set;
- L2: PANEL-2 modal agrees with the STANDING panel's modal on >= 0.70 of items where both
  are modal (commensurability);
- L3: coverage (modal exists) >= 0.85.
If licensed: PANEL-2 may run the wild unit corpus (legc2_items.jsonl); the wild matrix's
own VOID floor stays kappa >= 0.40 per TRANSITION_MAP_PREREG (unchanged). If any criterion
fails: PANEL-2 is NOT licensed, the failure is reported, and the wild matrix waits for
human labels or the block-scoped stream. Informational only (no criterion): hit-rate
against kind_target. Spend: ~774 + ~1035 calls, est < $0.50, human-upheld.
