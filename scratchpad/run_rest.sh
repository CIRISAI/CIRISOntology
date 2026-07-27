#!/bin/bash
# Stages 4 -> 5 -> 6 -> G7b, in the pre-registered order: the whole battery is
# run on surrogates (stage 4) BEFORE the data reading (stage 5).
set -x
P=/home/emoore/CIRISOntology/scratchpad/temporal-share/qenv/bin/python
cd /home/emoore/CIRISOntology/scratchpad
export OMP_NUM_THREADS=16
until [ -f planck_pilot/stage3_null_shape.json ]; do sleep 30; done
echo "STAGE 3 COMPLETE $(date)"
$P planck_pilot.py 4 && echo "STAGE 4 DONE $(date)"
$P planck_pilot.py 5 && echo "STAGE 5 DONE $(date)"
$P planck_pilot.py 6 && echo "STAGE 6 DONE $(date)"
$P planck_pilot_g7b.py && echo "G7B DONE $(date)"
echo "ALL DONE $(date)"
