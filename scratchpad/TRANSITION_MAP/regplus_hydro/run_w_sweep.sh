#!/bin/bash
cd /home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/regplus_hydro
mkdir -p results_w
while read -r cfg; do
  out="results_w/${cfg%.json}_result.json"
  [ -f "$out" ] || python3 regplus_hydro.py "configs/$cfg" --out "$out"
  echo "done $cfg"
done < w_runlist.txt
echo W-SWEEP-COMPLETE
