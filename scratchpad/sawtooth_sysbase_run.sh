#!/bin/bash
cd /home/emoore/CIRISOntology/scratchpad
source temporal-share/qenv/bin/activate 2>/dev/null
export OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
for K in 24 25 26 27; do nice -n 12 python3 sawtooth_forward.py --k $K --m 5 --rule systematic; done
echo "=== SYSBASE COMPLETE $(date -Is) ==="
