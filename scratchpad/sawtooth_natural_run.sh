#!/bin/bash
# P-AFTER / P-ABSENT: arm B natural continuation. Sequential (memory), nice'd (shared box).
cd /home/emoore/CIRISOntology/scratchpad
source temporal-share/qenv/bin/activate 2>/dev/null
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4
for K in 33 34 35; do
  echo "=== k=$K start $(date -Is) ==="
  nice -n 10 python3 sawtooth_forward.py --k $K
  echo "=== k=$K done $(date -Is) rc=$? ==="
done
echo "=== NATURAL LADDER COMPLETE $(date -Is) ==="
