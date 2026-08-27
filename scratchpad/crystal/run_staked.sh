#!/bin/bash
cd /home/emoore/CIRISOntology/scratchpad/crystal
python3 -u dmrg_schwinger.py staked > schwinger2_result.log 2>&1
echo $? > schwinger2.DONE
