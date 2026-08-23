# K2 — h3ere2 C-vs-B verdict (2026-08-23)

## VERDICT: NOT SUPPORTED — the kill fires, within its pre-committed scope

**Primary (A2 soft run, 92-item frozen split): C win rate over B = 0.531 (26 W / 23 L of
49 decisive), paired sign test p = 0.775.** Per JUDGE_PROTOCOL section 1's pre-committed
framing: this **rules out a large effect** (the significance threshold at decisive n = 49
is 0.640) and **cannot exclude a modest one** (< 0.58). The claim as staked — response
quality stops scaling with parameter count — required a large effect; it did not appear.
Scope (sealed): this falsifies THIS PIPELINE's use of the engine for response generation,
not the engine, taxonomy, or classifier.

**Side-by-side (A1.2 gold-hard run, same split): C over B = 0.608 (31/20 of 51), p = 0.161**
— numerically higher, not significant. Soft encoding did not change the verdict, so per
A2's own pre-registered reading, **the categorical bottleneck was not the limiting factor**.

**Secondary (C vs A): the pipeline is significantly WORSE than the bare 0.6B model.**
Soft: C win rate 0.303, p = 0.0019. Gold: 0.362, p = 0.0295. C spends ~40% more tokens
(78 vs 56) and ~40% more wall time doing it. The scaffold does not merely fail to help;
it costs quality.

## The two BINDING pre-judging measurements (A2)

1. **Distinct arm-C paths: 30 of 92** (modal path 40x; C path never equals the assigned
   B path, 0/920). Gate PASS — materially above 4, so the null is about the coupling's
   response to varying input, which is the prereg's claim. (Gold run: 4 distinct paths =
   A1.2's design level; A2's gate does not bind it.)
2. **Softmax entropy (fp32 ONNX classifier, n=92): median 0.057 of ln4 = 1.386; 57.6% of
   items effectively one-hot (H < 0.10); p(max) >= 0.99 on 50%.** Soft seeding partially
   collapses to hard on most items — classifier confidence is a real bottleneck — but the
   42% with genuine mass spread produced the path diversity above.

## Judge calibrations (before any real pair, per protocol)

| judge | identical-pair slot-1 | sensitivity (bar 0.90) | status |
|---|---|---|---|
| gemma3:12b (primary) | 0.868 (bias 0.368) | 0.902 | PASS — order-balanced scoring mandatory and applied |
| qwen3:14b (secondary) | **1.000** | 0.870 | **DISQUALIFIED** (both gates), no real pairs judged |

The verdict therefore rests on ONE judge; the protocol's split-verdict provision cannot
apply because the secondary failed its calibration. Flip rates on real pairs (46.2% soft,
44.0% gold) are reported per the revised rule as an effect-size signal — C and B are hard
to tell apart — not as instrument failure.

## Confound guards

- **Length: clean.** Judge picked the longer response 0.466 (p = 0.21) / 0.501 (p = 1.0).
- **Compute: reported.** A 56 tok / ~1.5-2.0 s; B and C 78 tok / ~2.0-2.6 s each. Favors
  C in the C-vs-A comparison, which C still lost.
- **Per-scramble win rates:** range 0.29-0.83 on small n, no wild outlier.
- **Strata (J1, diagnostic only):** surface strata are a mixture — soft run Facts 0.320 vs
  Rules 0.818, neither significant. The pooled number is not carried by one stratum in a
  provable way at this n.

## Deviations from the sealed protocols (all named, none touch the comparison)

1. **judge.py corpus path parameterised** (was hardwired to the wild corpus; the sealed
   pairing logic and seed 20260822 untouched).
2. **ciris-nl `Session::generate` reconstructed**: the eval binary was built from
   uncommitted code that commit d9ba56c landed without; rebuilt from the shipped binary's
   embedded template fragments and the untracked chat.rs. B and C share the renderer by
   construction; arm-A responses byte-identical across both runs (92/92) — determinism
   check passed. SYS_PATH's trailing `<|im_end|>` moved from the const into the template
   wrapper (no content change).
3. **relax_soft arrival readout**: A2 fixed the seeding but not the arrival rule for
   mass-carrying kinds; deviation-from-initial chosen — the unique reading that reduces
   exactly to the hard instrument at one-hot, machine-checked
   (`soft_one_hot_reduces_to_hard`, 13/13 crate tests).
4. **A1.2's quoted gold histogram does not reproduce**: actual gold 4-way histogram is
   Facts 34 / Rules 24 / Manner 24 / Identity 10 (surface_map.json, which predates A1);
   A1.2 said 35/30/16/11. No design impact; recorded.
5. **n = 92, not 170**: protocol power numbers were staked at 170; analyze.py recomputes
   thresholds at observed decisive n (0.640 / 0.637). The null's scope statement above
   uses the recomputed values.
6. **The wild run (A1.1) remains generated-but-unjudged** (responses.jsonl, 170 items,
   hard fp32). Its narrowed question ("one fixed ordering vs ten") is superseded by the
   two runs above; judging it costs ~700 more calls and is available on request.

## Provenance

encoded_soft92.jsonl / encoded_gold92.jsonl (encoder: nl_bridge_eval/onnx_fp32/model.onnx,
fp32, argmax reproduces the sealed 0.772); responses_{soft,gold}92.jsonl (1104 records
each; physics `symmetrised=false`, `dt=0.0005`, `Params::harmonic()`, asserted in code);
judge_{soft,gold}92_{calib_bias,calib_sens,pairs}.jsonl + judge_soft92_qwen_calib_*.jsonl;
judge_all.log (stage log); prejudge_gate.py, encode_soft92.py, run_generate_92.sh,
run_judge_all.sh, RESUME.md. Balanced random scramble assignment seed 20260822 (judge.py,
sealed). Crate: sim_engine/crates/h3ere2-eval (soft mode default, --hard flag);
sim_engine/crates/ciris-nl (chat.rs wired, Session::generate restored) — code uncommitted,
for review.
