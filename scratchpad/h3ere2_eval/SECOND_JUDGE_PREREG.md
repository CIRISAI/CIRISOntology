# K2 SECOND JUDGE — selection rule, pre-registered

**Written 2026-08-24, before any calibration call has been made against any candidate.**
No gate in `JUDGE_PROTOCOL.md` is altered here. This file fixes only the things the
protocol left open when it named a secondary judge that then disqualified itself: *which*
candidates are tried, and *which* one runs if more than one clears the unchanged bars.

## What this does and does not do

This firms a FIRED kill. It does not re-run one. K2's verdict — C over B = 0.531
(26 W / 23 L of 49 decisive), sign test p = 0.775 — is closed, and nothing here can
reopen it. The single weakness being removed is that the verdict rests on ONE judge,
because `qwen3:14b` failed both calibration gates (identical-pair slot-1 rate 1.000;
sensitivity 0.870 against the 0.90 bar) and therefore judged no real pairs, so the
protocol's split-verdict provision never executed.

## The gates — UNCHANGED, quoted from JUDGE_PROTOCOL section 2

- **Calibration 1, identical pairs.** Same response in both slots, all items. Any
  departure from 0.5 is pure position bias. Bias >= 0.075 from 0.5 -> order-balanced
  scoring is mandatory and the bias is reported; this is **not** disqualifying on its own.
- **Calibration 2, known-gap pairs.** Intact response vs its own first sentence. The judge
  must prefer intact on **>= 0.90**. Below that, judging FAILED and no verdict is issued.

Neither threshold is moved. A candidate that fails is a recorded disqualification, exactly
as `qwen3:14b` was. Reporting three disqualifications is a legitimate outcome of this lane.

**One degeneracy note, stated in advance because it is about to matter.** Order-balanced
scoring counts a pair as decisive only when the same arm wins in BOTH orders. A judge whose
slot-1 rate is exactly 1.000 always picks slot 1, so under order-balanced scoring it yields
ZERO decisive pairs by construction — its verdict is empty, not merely noisy. So while the
protocol's letter makes only sensitivity disqualifying, a slot-1 rate of 1.000 is a de facto
disqualification, and that — not the sensitivity miss alone — is the sharper reason
`qwen3:14b` could issue no verdict. Recorded as a reading of the existing rule, not a new one.

## Candidates, and why these

The generator is Qwen3-0.6B and the primary judge is `gemma3:12b`. A useful second judge
should be a third family: same-family-as-generator risks correlated preference for
same-family prose (the protocol's own section 3 concern), and same-family-as-primary makes
inter-judge agreement uninformative. Candidates, in the order they will be calibrated:

1. `phi4:14b` — Microsoft
2. `mistral-nemo:12b` — Mistral / NVIDIA
3. `llama3.1:8b` — Meta

All three are distinct from both Qwen and Gemma. All are substantially larger than the 0.6B
generator, as PREREG.md requires. This is the complete list of what was tried; every
candidate's two measurements are reported whether it passes or fails.

Nothing else local was eligible: `qwen3:0.6b` IS the generator, `smollm2:360m-instruct-q4_K_M`
and the two `ft-*` artifacts are at or below generator scale, `gemma3:12b` is the primary,
and `qwen3:14b` is the recorded disqualification this lane exists to replace.

## Selection rule — FIXED NOW, before any number is seen

All three candidates are calibrated on both gates regardless of how early one passes, so the
record is complete rather than truncated at the first success.

Among candidates that pass, the one that runs is chosen by, in order:

1. highest **sensitivity** (the protocol's own quality bar);
2. if tied, **lower** identical-pair position bias;
3. if still tied, alphabetical by model name.

**Exactly one** second judge runs the real pairs. If it disagrees with the primary, that
disagreement IS the finding and stands as reported; no third judge will be run to break the
tie, because selecting a tiebreaker after seeing a disagreement is gate-shopping and would
convert a real result into a shopped one. A third judge runs only on explicit instruction
from outside this lane, and would be reported as an explicitly-labelled addition that
characterises a disagreement rather than overturning it.

## What the second judge runs, and what it may not touch

- The **frozen 92-item split**, same items, same corpus
  (`nl_bridge_eval/test_split.jsonl`), same `judge.py` with its sealed pairing seed
  20260822, same order-balancing. `judge.py` and `analyze.py` are used **unmodified**; the
  only thing that changes between the primary run and this one is the model string.
- Responses are **not** re-generated. `responses_soft92.jsonl` and `responses_gold92.jsonl`
  are the frozen inputs. (They could not be re-generated even if that were wanted: the
  `generate` binary does not compile at HEAD — see the build-verify finding.)
- `RESULTS_K2.md` is **not** edited by this lane. Output is a new section for an integrator.

## The three outcomes, staked before any number exists

- **Agrees on both primary (C vs B) and secondary (C vs A):** the verdict is firmed and the
  single-judge caveat is discharged.
- **Disagrees on the PRIMARY (C vs B):** the kill's SCOPE narrows and the record says so.
- **Disagrees on the SECONDARY (C vs A):** serious, and it escalates immediately — the
  secondary (0.303 at p = 0.0019, with C spending ~40% more tokens and wall time) is what
  feeds a product-direction decision outside this repo.

"Agrees" means the same direction and the same side of significance at alpha = 0.05, judged
by `analyze.py`'s own output on the second judge's pair file. A numerically different win
rate that lands on the same side of both is agreement; that is stated now so it cannot be
re-read later.
