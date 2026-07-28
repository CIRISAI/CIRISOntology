#!/bin/bash
cd /home/emoore/CIRISOntology/scratchpad
source temporal-share/qenv/bin/activate 2>/dev/null
export OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
R() { echo "=== $* start $(date -Is) ==="; nice -n 12 python3 sawtooth_forward.py "$@"; }
# m=5 baselines, recomputed on this instrument (prereg s3)
for K in 20 21 22 23 24; do R --k $K; done
# P-PLANT: one ln2 step planted where arm B has none
R --k 24 --m 6
R --k 26 --m 6
R --k 28 --m 6
R --k 30 --m 6
# column-rule control + P-LINEAR (two ln2 steps)
R --k 28 --m 6 --rule systematic
R --k 28 --m 7 --rule systematic
echo "=== PLANTED ARM COMPLETE $(date -Is) ==="
