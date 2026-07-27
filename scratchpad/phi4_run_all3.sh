#!/bin/bash
cd /home/emoore/CIRISOntology/scratchpad
source temporal-share/qenv/bin/activate
set -x
python3 phi4_ridge.py --seeds32 --mc -2.2863 --u0 1.15 > phi4_seeds32.log 2>&1
python3 phi4_ridge.py --gate                          > phi4_gate.log     2>&1
echo "PHASE3 DONE"
