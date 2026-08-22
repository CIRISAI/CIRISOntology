#!/bin/bash
cd /home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/GPU_MC_BUILD
until [ -f mc_L7_LOW_N20_W100000.json ]; do sleep 20; done
sleep 5
python3 cascade_e2.py L7_MID_N25 10000 100000 >> mc_mid.log 2>&1
python3 cascade_e2.py L7_LOW_N20 1000000 >> mc_low.log 2>&1
python3 cascade_e2.py L7_MID_N25 1000000 >> mc_mid.log 2>&1
touch BENCH_DONE
