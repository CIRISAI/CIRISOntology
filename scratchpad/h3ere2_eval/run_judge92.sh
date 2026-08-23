#!/bin/bash
# K2 judging, per JUDGE_PROTOCOL.md: calibrations BEFORE real pairs, per run.
# Usage: run_judge92.sh <soft|gold>
set -e
H=~/CIRISOntology/scratchpad/h3ere2_eval
T=~/CIRISOntology/scratchpad/nl_bridge_eval/test_split.jsonl
R=$H/responses_${1}92.jsonl
P=/tmp/rtenv/bin/python

$P $H/judge.py calib_bias gemma3:12b $R $H/judge_${1}92_calib_bias.jsonl $T 2>&1
$P $H/judge.py calib_sens gemma3:12b $R $H/judge_${1}92_calib_sens.jsonl $T 2>&1
$P $H/judge.py pairs      gemma3:12b $R $H/judge_${1}92_pairs.jsonl      $T 2>&1
echo DONE > $H/judge_${1}92.done
