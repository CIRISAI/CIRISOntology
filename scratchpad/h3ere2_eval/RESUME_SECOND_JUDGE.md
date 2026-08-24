# K2 second judge — detached run state

Design frozen in `SECOND_JUDGE_PREREG.md` (committed `f283522`) before any calibration call
was made. Gates are `JUDGE_PROTOCOL.md`'s, unchanged. `judge.py` and `analyze.py` are used
**unmodified** — the only difference from the primary run is the model string.

## Stage 1 — calibration sweep (`run_calib_second.sh`, setsid)

All three candidates are calibrated on both gates regardless of early success, so the record
is not truncated. Log: `calib_second.log`. End marker: `calib_second.done`.

| tag | model | family | bias artifact | sens artifact |
|---|---|---|---|---|
| phi4 | `phi4:14b` | Microsoft | `judge_soft92_phi4_calib_bias.jsonl` | `judge_soft92_phi4_calib_sens.jsonl` |
| nemo | `mistral-nemo:12b` | Mistral/NVIDIA | `judge_soft92_nemo_calib_bias.jsonl` | `judge_soft92_nemo_calib_sens.jsonl` |
| llama31 | `llama3.1:8b` | Meta | `judge_soft92_llama31_calib_bias.jsonl` | `judge_soft92_llama31_calib_sens.jsonl` |

A stage is complete iff its jsonl exists AND its `==== STAGE ====` line appears in
`calib_second.log`. The script waits (up to 60 min) for a model to appear in `ollama list`
before its stages, because the pulls run concurrently; a model that never appears is
recorded as `UNAVAILABLE`, not silently skipped.

Gates, unchanged: sensitivity **>= 0.90** is the hard bar; identical-pair bias is reported
and mandates order-balanced scoring but is not disqualifying on its own — except that a
slot-1 rate of exactly 1.000 yields ZERO decisive pairs under order-balanced scoring and is
therefore a de facto disqualification (this is what actually silenced `qwen3:14b`).

## Stage 2 — the real pairs, ONE judge only

Selection is fixed in the prereg: highest sensitivity among passers, then lower bias, then
alphabetical. Exactly one second judge runs; no third is run to break a disagreement.

Runs `judge.py pairs <model> responses_{soft,gold}92.jsonl` on the **frozen** 92-item split,
corpus `nl_bridge_eval/test_split.jsonl`, sealed pairing seed 20260822. Responses are NOT
regenerated — and could not be: `bin/generate` does not compile at HEAD (see
`build_verify.log` and commit `f283522`).

Artifacts: `judge_soft92_<tag>_pairs.jsonl`, `judge_gold92_<tag>_pairs.jsonl`.
Expect ~7 min per pairs stage (the primary's soft+gold pairs took 7m and 7m).

## Stage 3 — split-verdict provision

`analyze.py <pairs.jsonl> <responses.jsonl>` for each, compared against the primary
(reproduced from the primary artifact this session, not quoted from prose):

| | primary `gemma3:12b`, soft run |
|---|---|
| C vs B | 26 W / 23 L of 49 decisive, rate 0.531, p = 0.7754, 42 flips |
| C vs A | 20 W / 46 L of 66 decisive, rate 0.303, p = 0.0019, 26 flips |

"Agrees" = same direction AND same side of alpha = 0.05, per the prereg.

## Resuming after a death

Delete the LAST (possibly partial) jsonl, comment out the completed `run_one` lines, relaunch
with setsid. `judge.py` is deterministic in pairing (seed 20260822), so a clean re-run of a
stage is identical work. Nothing in this lane writes to `RESULTS_K2.md`.
