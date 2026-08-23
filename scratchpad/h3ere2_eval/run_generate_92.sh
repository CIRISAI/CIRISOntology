#!/bin/bash
H=~/CIRISOntology/scratchpad/h3ere2_eval
B=~/CIRISOntology/sim_engine/crates/h3ere2-eval
M=/tmp/claude-1000/-home-emoore-CIRISOntology/4cf4fa5c-aaa3-4173-83b9-978cb75c887f/scratchpad/models/Qwen3-0.6B-Q4_K_M.gguf
$B/target/release/generate $M $H/encoded_soft92.jsonl $H/responses_soft92.jsonl 2> $H/generate_soft92.log
echo DONE > $H/generate_soft92.done
$B/target/release/generate --hard $M $H/encoded_gold92.jsonl $H/responses_gold92.jsonl 2> $H/generate_gold92.log
echo DONE > $H/generate_gold92.done
