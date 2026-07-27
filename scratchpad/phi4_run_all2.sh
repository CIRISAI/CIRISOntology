#!/bin/bash
cd /home/emoore/CIRISOntology/scratchpad
source temporal-share/qenv/bin/activate
MC=-2.2863
U0=1.15
set -x
python3 phi4_ridge.py --eqtest  --mc $MC --u0 $U0 > phi4_eqtest.log   2>&1
python3 phi4_ridge.py --bsweep3 --mc $MC --u0 $U0 > phi4_bsweep3.log  2>&1
python3 phi4_ridge.py --deep    --mc $MC --u0 $U0 > phi4_deep.log     2>&1
echo "PHASE2 DONE"
