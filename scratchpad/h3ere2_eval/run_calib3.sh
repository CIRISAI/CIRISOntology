#!/bin/bash
# Calibration 3 (length preference) — collection for a candidate judge.
# AMENDMENT_J2_LENGTH_GATE.md. Run this BEFORE the candidate judges any real pair;
# `judge.py pairs` will refuse to run until it has passed.
#
#   Usage: run_calib3.sh <model> [<model> ...]      e.g. run_calib3.sh gemma3:12b
#
# HONEST PROVENANCE: this script is the forward-looking collector. The five readings already
# in the record (gemma3, llama3.1, phi4, mistral-nemo, qwen3) were collected on 2026-08-24 by
# an ad-hoc loop that was not saved; `calib_length.log` is that run's record. This script
# reproduces that loop's calls, but the artifacts it writes carry a `model` field the five do
# not, so it is NOT claimed to reproduce them byte for byte, and re-collection is not needed:
# the five are scored from disk by `calib3.score`, and `gate_calib3.sh` pins the result.
set -u
H=$(cd "$(dirname "$0")" && pwd)
T=~/CIRISOntology/scratchpad/nl_bridge_eval/test_split.jsonl
R=$H/responses_soft92.jsonl
P=${PY:-/tmp/rtenv/bin/python}
L=$H/calib_length.log

for model in "$@"; do
  tag=$(echo "$model" | cut -d: -f1 | tr -d '.')
  echo "==== $model $(date +%H:%M:%S) ====" >> "$L"
  $P "$H/calib_length.py" "$model" "$R" "$H/calib3_${tag}.jsonl" "$T" 2>&1 | tee -a "$L"
done
echo DONE > "$H/calib_len.done"
