# H3ERE2-X — pattern selection for the REG decomposition pipeline
# FROZEN 2026-08-22, before any pipeline call ran. prereg_id: H3ERE2X-20260822

## The question

Which pipeline pattern best decomposes wild change-lines into REG terms (kind + verb),
measured against the two-panel-replicated wild ceiling (single-pass kappa ~0.30-0.36)?

## H3ERE mechanics mirrored (verified in the agent engine)

Stage outputs feed later stages verbatim; a conscience-style validator can OVERRIDE with
a stated reason; on override the prior stage RETRIES ONCE with that guidance injected
(bounded recursion, exactly the engine's RECURSIVE_ASPDMA/RECURSIVE_CONSCIENCE shape).

## The three patterns (frozen)

- FLAT (baseline): the existing single-pass 12-kind instrument. No new wild calls —
  the sealed PANEL-2 judgments are the baseline arm.
- H3ERE2-A (gate-then-recurse): S1 surface evaluation — {Facts, Rules, Manner, Identity,
  DEEPER} + REG verb + confidence in [0,1] + one-sentence rationale. Confident surface
  (conf >= 0.7, frozen) -> final. Else S2 deep selection with CARRIES-INVERSION: S1's
  output verbatim + the three measured boundary priors + the deep-seven discriminators;
  outputs deep kind (or surface confirm) + verb + rationale. S3 conscience: verify the
  inversion ("would <deep> wear <surface> here?") PASS/FAIL + guidance; FAIL -> one S2
  retry with guidance; still FAIL -> final = S2's second answer flagged UNVERIFIED.
- H3ERE2-B (decompose-then-vote): S1 identical. S2 outputs a MIXTURE — every kind
  component present with weights summing to 1 (the ceiling finding says wild lines are
  mixtures; this pattern says so explicitly); final = argmax. S3 conscience on the top
  component, same retry rule.

## Instrument, data, seeds

Families: the licensed PANEL-2 trio (DeepSeek-V3.1, Qwen3-235B, GLM-4.5 @2500 tokens),
temp 0, stateless per stage. Data: (a) CURATED anchor — 124 items, every second line of
corpus_full.jsonl (seeded order, seed 20260822); (b) WILD — all 345 sealed units.
Each family runs the WHOLE pipeline independently (agreement measured on final outputs).

## License criteria per pattern (all required)

- L1 curated: end-to-end kind accuracy >= the single-pass baseline on the same 124
  (baseline computed from the sealed PANEL-2 validation judgments), AND accuracy on
  DEEP-kind targets improves by >= 10 points over that baseline.
- L2 wild: pipeline-level cross-family Fleiss kappa on final kinds >= 0.40 — the frozen
  wild floor, i.e. THE CEILING BREAK.
- L3 coverage >= 0.85 on both datasets. 
BEST PATTERN = licensed pattern with the highest wild kappa; tie -> higher deep-curated
accuracy. If none licenses: the ceiling stands against this architecture class too,
reported as such, and the human-label route is next.

## The X read (secondary, no criterion)

Verb assignments are recorded at every stage; X is READ from where verb determinacy
lives (S1-determinate verbs = fast set), reported descriptively for the H3ERE2 design.

## Fences

Cap $2.00, human-upheld. No stance change. The wild FD confrontation still requires the
winning pattern to pass THIS license before any FD reading (H3ERE2_NOTE dependency chain).

## AMENDMENT T1 (2026-08-22, steward-granted, recorded BEFORE any calibration error was inspected)

The steward grants TUNING LICENSE: H3ERE2 is an instrument with a known target, and
instrument development may iterate freely — prompts, the confidence gate, the boundary
priors, stage structure, X — against the CALIBRATION data (the current four runs:
curated-124-even + wild-345). The house pattern applies: gauge the ruler on planted
values, then stake.

THE VERDICT MOVES TO HELD-OUT VALIDATION, frozen now:
- curated held-out: the 124 ODD lines of corpus_full.jsonl (never used in tuning);
- wild held-out: FRESH revision chains, seed 20260823, target 50 chains, sampled by the
  sealed legc_sample recipe only after tuning is declared frozen;
- the final tuned pipeline runs ONCE on both; L1/L2/L3 apply to that run alone. Tuning
  iterations may be many; validation is single-shot. If validation fails, the pipeline
  returns to calibration and a NEW held-out wild sample (next seed) is required for any
  re-validation — held-out data is never reused.
