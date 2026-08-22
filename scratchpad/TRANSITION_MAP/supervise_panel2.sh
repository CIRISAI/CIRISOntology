#!/bin/bash
cd /home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP
last=0; stall=0
while true; do
  n=$(wc -l < legc2_panel2_judgments.jsonl 2>/dev/null || echo 0)
  if [ "$n" -ge 1035 ]; then echo "SUPERVISOR-COMPLETE $n"; break; fi
  if ! pgrep -f "[p]anel2_annotate" >/dev/null; then
    if [ "$n" -le "$last" ]; then stall=$((stall+1)); else stall=0; fi
    if [ "$stall" -ge 5 ]; then echo "SUPERVISOR-STALLED at $n"; break; fi
    last=$n
    nohup python3 panel2_annotate.py --corpus legc2_items.jsonl --out legc2_panel2_judgments.jsonl --conditions BASE --workers 6 >> legc2_panel2_b.log 2>&1 &
  fi
  sleep 30
done
