#!/bin/bash
cd /home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/GPU_MC_BUILD
until [ -f BENCH_DONE ]; do sleep 30; done
for C in L7_HIGH_N31 L9_LOW_N32 L9_MID_N42 L9_HIGH_N52; do
  python3 cascade_e2.py $C 100000 >> heldout.log 2>&1
done
touch HELDOUT_DONE
