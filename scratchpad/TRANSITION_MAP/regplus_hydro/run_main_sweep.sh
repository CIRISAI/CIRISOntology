#!/bin/bash
cd /home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/regplus_hydro
mkdir -p results_main
while read -r cfg; do
  out="results_main/${cfg%.json}_result.json"
  if [ ! -f "$out" ]; then
    python3 regplus_hydro.py "configs_main/$cfg" --out "$out" || echo "FAILED $cfg"
  fi
  echo "done $cfg $(date +%H:%M:%S)"
done < main_runlist.txt
echo MAIN-SWEEP-COMPLETE
