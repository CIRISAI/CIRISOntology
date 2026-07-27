#!/bin/bash
cd /home/emoore/CIRISOntology/scratchpad
PY=/home/emoore/CIRISOntology/scratchpad/temporal-share/qenv/bin/python
while pgrep -x python3 >/dev/null && pgrep -f "[g]lass_gates[.]py" >/dev/null; do sleep 20; done
echo "REST START $(date)"
# COUNT-MATCHED: cap 1300 binds at BOTH primary templates at ALL four
# temperatures (minimum observed is 1330 per configuration at r=1.30, T=0.44),
# so every rung carries an identical triple count per configuration.
$PY glass_run.py --points KA_T0.44,KA_T0.50,KA_T0.56,KA_T0.64 --nconf 500 \
    --ndraw 300 --nboot 400 --cap 1300 --templates 1.30,1.50 \
    --out glass_stageA_matched.json > glass_stageA_matched.log 2>&1
echo "MATCHED DONE $(date)"
# the 2D replicate, ladder scaled to its own measured first peak (0.89 vs 1.07)
$PY glass_run.py --points KA2D_T0.23,KA2D_T0.30 --nconf 300 --ndraw 300 \
    --nboot 400 --cap 25000 --templates 0.89,1.08,1.25,1.50,1.75,2.08,2.50,4.00 \
    --out glass_stage2d.json > glass_stage2d.log 2>&1
echo "2D DONE $(date)"
