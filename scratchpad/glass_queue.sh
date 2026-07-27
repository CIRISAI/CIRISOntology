#!/bin/bash
cd /home/emoore/CIRISOntology/scratchpad
PY=temporal-share/qenv/bin/python
# wait for stage A and stage B to clear the GPU
while pgrep -f "glass_run.py --points KA_T0.44,KA_T0.50" >/dev/null || pgrep -f glass_surrogate.py >/dev/null; do sleep 30; done
echo "QUEUE START $(date)"
# 1. the binmint pedestal and the fine-geometry LP
$PY glass_gates.py --points KA_T0.44,KA_T0.50,KA_T0.56,KA_T0.64 --nconf 150 \
    --templates 1.07,1.30,1.50,1.80,3.00 --br 2,3,4 --out glass_gates.json \
    > glass_gates.log 2>&1
echo "GATES DONE $(date)"
# 2. the count-matched pass: a cap small enough to bind at EVERY temperature and
#    every template, so all four rungs carry identical triple counts per config
$PY glass_run.py --points KA_T0.44,KA_T0.50,KA_T0.56,KA_T0.64 --nconf 500 \
    --ndraw 300 --nboot 400 --cap 900 --templates 1.30,1.50,1.80,3.00,6.00 \
    --out glass_stageA_matched.json > glass_stageA_matched.log 2>&1
echo "MATCHED DONE $(date)"
# 3. the 2D replicate, ladder scaled to its own measured first peak (0.89/1.07)
$PY glass_run.py --points KA2D_T0.23,KA2D_T0.30 --nconf 300 --ndraw 300 \
    --nboot 400 --cap 25000 --templates 0.74,0.89,1.08,1.25,1.50,1.75,2.08,2.50,4.00,5.00 \
    --out glass_stage2d.json > glass_stage2d.log 2>&1
echo "2D DONE $(date)"
echo QUEUEALLDONE
