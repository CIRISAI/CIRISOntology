#!/bin/bash
H=~/CIRISOntology/scratchpad/h3ere2_eval
T=~/CIRISOntology/scratchpad/nl_bridge_eval/test_split.jsonl
P=/tmp/rtenv/bin/python
L=$H/judge_all.log
: > $L
stage() { echo "==== STAGE $1 $(date +%H:%M:%S) ====" >> $L; }
stage "1 soft calib_bias";  $P $H/judge.py calib_bias gemma3:12b $H/responses_soft92.jsonl $H/judge_soft92_calib_bias.jsonl $T >> $L 2>&1
stage "2 soft calib_sens";  $P $H/judge.py calib_sens gemma3:12b $H/responses_soft92.jsonl $H/judge_soft92_calib_sens.jsonl $T >> $L 2>&1
stage "3 soft pairs";       $P $H/judge.py pairs      gemma3:12b $H/responses_soft92.jsonl $H/judge_soft92_pairs.jsonl      $T >> $L 2>&1
stage "4 gold calib_bias";  $P $H/judge.py calib_bias gemma3:12b $H/responses_gold92.jsonl $H/judge_gold92_calib_bias.jsonl $T >> $L 2>&1
stage "5 gold calib_sens";  $P $H/judge.py calib_sens gemma3:12b $H/responses_gold92.jsonl $H/judge_gold92_calib_sens.jsonl $T >> $L 2>&1
stage "6 gold pairs";       $P $H/judge.py pairs      gemma3:12b $H/responses_gold92.jsonl $H/judge_gold92_pairs.jsonl      $T >> $L 2>&1
stage "7 qwen calib_bias";  $P $H/judge.py calib_bias qwen3:14b  $H/responses_soft92.jsonl $H/judge_soft92_qwen_calib_bias.jsonl $T >> $L 2>&1
stage "8 qwen calib_sens";  $P $H/judge.py calib_sens qwen3:14b  $H/responses_soft92.jsonl $H/judge_soft92_qwen_calib_sens.jsonl $T >> $L 2>&1
stage "ALL DONE"; echo DONE > $H/judge_all.done
