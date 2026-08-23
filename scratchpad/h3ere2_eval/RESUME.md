# K2 judging — detached run state (written 2026-08-23, before any real pair was judged)

`run_judge_all.sh` runs detached (setsid). Stages, in order, each with its own artifact;
a stage is complete iff its jsonl exists AND the stage line appears in `judge_all.log`;
`judge_all.done` marks the end. Judge: gemma3:12b (primary). qwen3:14b runs CALIBRATIONS
ONLY unless it passes both (it is expected to fail on measured slot-1 bias; if it passes,
JUDGE_PROTOCOL section 3 requires its full run — relaunch stages 7-8 by hand).

| stage | artifact |
|---|---|
| 1 soft calib_bias  | judge_soft92_calib_bias.jsonl |
| 2 soft calib_sens  | judge_soft92_calib_sens.jsonl |
| 3 soft pairs       | judge_soft92_pairs.jsonl |
| 4 gold calib_bias  | judge_gold92_calib_bias.jsonl |
| 5 gold calib_sens  | judge_gold92_calib_sens.jsonl |
| 6 gold pairs       | judge_gold92_pairs.jsonl |
| 7 qwen calib_bias  | judge_soft92_qwen_calib_bias.jsonl |
| 8 qwen calib_sens  | judge_soft92_qwen_calib_sens.jsonl |

To resume after a death: delete the LAST (possibly partial) jsonl, comment out completed
stages in `run_judge_all.sh`, relaunch with setsid. judge.py is deterministic in pairing
(seed 20260822) so a clean re-run of a stage is identical work.

Pre-judging gates already passed and recorded (prejudge_gate.py):
- soft: 30 distinct C paths / 92 (A2 gate PASS); C==B path 0/920
- gold: 4 distinct C paths = A1.2's design level (A2's gate does not bind it)
- entropy: median 0.057, 57.6% of items one-hot (H<0.10) — encoded_soft92.jsonl, n=92

Analysis after: `analyze.py judge_soft92_pairs.jsonl responses_soft92.jsonl` (same for gold).
Verdict framing is pre-committed in JUDGE_PROTOCOL section 1 (null = "rules out a large
effect"; at n=92 the thresholds are recomputed by analyze.py at the observed decisive n).
