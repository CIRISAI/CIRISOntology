#!/bin/bash
# K2 SECOND JUDGE — real pairs. Selected by SECOND_JUDGE_PREREG.md's frozen rule (highest
# sensitivity among gate-passers): llama3.1:8b, sens 0.935, the ONLY candidate of three to
# clear the unchanged 0.90 bar. judge.py UNMODIFIED; frozen 92-item split; sealed seed
# 20260822; responses NOT regenerated.
H=~/CIRISOntology/scratchpad/h3ere2_eval
T=~/CIRISOntology/scratchpad/nl_bridge_eval/test_split.jsonl
P=/tmp/rtenv/bin/python
M=llama3.1:8b
L=$H/pairs_second.log
: > $L
stage() { echo "==== STAGE $1 $(date +%H:%M:%S) ====" >> $L; }
stage "soft pairs ($M)"
$P $H/judge.py pairs "$M" $H/responses_soft92.jsonl $H/judge_soft92_llama31_pairs.jsonl $T >> $L 2>&1
stage "gold pairs ($M)"
$P $H/judge.py pairs "$M" $H/responses_gold92.jsonl $H/judge_gold92_llama31_pairs.jsonl $T >> $L 2>&1
stage "ALL DONE"; echo DONE > $H/pairs_second.done
