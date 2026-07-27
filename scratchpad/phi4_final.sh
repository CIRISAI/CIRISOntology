#!/bin/bash
cd /home/emoore/CIRISOntology/scratchpad
source temporal-share/qenv/bin/activate
python3 -u phi4_analyze.py > phi4_analyze_final.log 2>&1
python3 -u phi4_k4.py      > phi4_k4.log           2>&1
echo "FINAL ANALYSIS DONE"
