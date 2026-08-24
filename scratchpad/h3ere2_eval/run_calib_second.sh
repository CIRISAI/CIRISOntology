#!/bin/bash
# K2 second-judge CALIBRATION sweep. Per SECOND_JUDGE_PREREG.md: all three candidates are
# calibrated on both gates regardless of how early one passes, so the record is complete
# rather than truncated at the first success. judge.py is used UNMODIFIED; the only thing
# that differs from the primary run is the model string.
H=~/CIRISOntology/scratchpad/h3ere2_eval
T=~/CIRISOntology/scratchpad/nl_bridge_eval/test_split.jsonl
R=$H/responses_soft92.jsonl
P=/tmp/rtenv/bin/python
L=$H/calib_second.log
: > $L
stage() { echo "==== STAGE $1 $(date +%H:%M:%S) ====" >> $L; }

# tag:model, in the pre-registered calibration order
run_one() {
  tag=$1; model=$2
  # wait for the model to finish pulling (phi4 is already local; the other two may not be)
  for i in $(seq 1 120); do
    ollama list | grep -q "^${model} " && break
    sleep 30
  done
  if ! ollama list | grep -q "^${model} "; then
    stage "$tag UNAVAILABLE - model never appeared in ollama list"; return
  fi
  stage "$tag calib_bias ($model)"
  $P $H/judge.py calib_bias "$model" $R $H/judge_soft92_${tag}_calib_bias.jsonl $T >> $L 2>&1
  stage "$tag calib_sens ($model)"
  $P $H/judge.py calib_sens "$model" $R $H/judge_soft92_${tag}_calib_sens.jsonl $T >> $L 2>&1
}

run_one phi4   phi4:14b
run_one nemo   mistral-nemo:12b
run_one llama31 llama3.1:8b

stage "ALL DONE"; echo DONE > $H/calib_second.done
