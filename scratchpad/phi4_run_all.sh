#!/bin/bash
cd /home/emoore/CIRISOntology/scratchpad
source temporal-share/qenv/bin/activate
MC=-2.2863
U0=1.15
set -x
python3 phi4_ridge.py --ridge    --mc $MC --u0 $U0 > phi4_ridge_stage.log   2>&1
python3 phi4_ridge.py --offcrit  --mc $MC --u0 $U0 > phi4_offcrit.log       2>&1
python3 phi4_ridge.py --controls --mc $MC          > phi4_controls.log      2>&1
python3 phi4_ridge.py --sep      --mc $MC --u0 $U0 > phi4_sep.log           2>&1
python3 phi4_ridge.py --bsweep   --mc $MC --u0 $U0 > phi4_bsweep.log        2>&1
python3 phi4_ridge.py --dose     --mc $MC --u0 $U0 > phi4_dose.log          2>&1
echo "ALL STAGES DONE"
