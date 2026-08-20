#!/bin/bash
# GAUGE TEST — run arms A, B, C sequentially (sequential so the $0.40 cap accounting,
# which reads the spend_*.json files written at arm end, sees every earlier arm).
# Each arm retries up to 3 times; the runner is resumable, so a retry only fills gaps.
cd /home/emoore/CIRISOntology/scratchpad/gaugetest || exit 1
for ARM in A B C; do
  if [ -f "DONE_$ARM" ]; then echo "=== ARM $ARM already done ==="; continue; fi
  for TRY in 1 2 3; do
    echo "=== ARM $ARM attempt $TRY $(date -Is) ==="
    python3 gauge_annotate.py --arm "$ARM" --workers 12
    RC=$?
    echo "=== ARM $ARM attempt $TRY exit $RC ==="
    if [ $RC -eq 0 ]; then break; fi
    if [ $RC -eq 3 ]; then echo "SPEND CAP HIT — aborting all arms"; exit 3; fi
    sleep 10
  done
  if [ ! -f "DONE_$ARM" ]; then echo "ARM $ARM DID NOT COMPLETE"; exit 4; fi
done
echo "=== ALL ARMS COMPLETE $(date -Is) ==="
touch DONE_ALL
