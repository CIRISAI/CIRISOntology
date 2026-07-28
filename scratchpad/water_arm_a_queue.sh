#!/bin/bash
# Arm A supplementary runs, after the sec 5.6 cavitation gate fired on 6 of the 8
# pre-registered lambda points (`water_homog.log`).  See WATER_AMENDMENT_12.md.
#   FILL  the lambda dose INSIDE the homogeneous window, at the pre-registered
#         matched density rho = 0.997 g/cm^3
#   AMB   every lambda at its OWN ambient density (NPT, 1 atm) -- the alternative
#         matching, measured rather than argued
#   COLD  the sec 5.6 check-1 hot/cold start replicate on the two points that
#         passed the gate
set -u
cd /home/emoore/CIRISOntology/scratchpad
source /home/emoore/CIRISOntology/scratchpad/temporal-share/qenv/bin/activate
export LD_LIBRARY_PATH=/home/emoore/CIRISOntology/scratchpad/temporal-share/qenv/lib:${LD_LIBRARY_PATH:-}
S=/home/emoore/CIRISOntology/scratchpad
P=$S/water_mw.py

case "$1" in
fill)
  python3 $P --sweep --lams 15,16,17,19,20,21.5 --tag mw --ensemble nvt \
     --rho 0.997 -T 298 --threads 4 --out $S/water_mw_sweep_fill.json ;;
amb)
  python3 $P --sweep --lams 0,2,5,8,11,14,18,23.15 --tag amb --ensemble npt \
     -P 1.0 --rho 0.997 -T 298 --nequil 40000 --threads 4 --out $S/water_mw_amb.json ;;
cold)
  python3 $P --sweep --lams 20,23.15 --tag cold --ensemble nvt --start cold \
     --rho 0.997 -T 298 -n 1728 --threads 4 --out $S/water_mw_cold.json ;;
up)
  # extend the dose UPWARD, where cavitation cannot occur because a stronger
  # three-body term holds the network open harder.  The hazard in this
  # direction is the opposite one -- crystallisation (sec 5.6 check 3) -- and it
  # is gated for, not assumed against.
  python3 $P --sweep --lams 20.5,22,25,27 --tag mw --ensemble nvt \
     --rho 0.997 -T 298 --threads 4 --out $S/water_mw_sweep_up.json ;;
esac

# (appended) re-run the gate-passing points at the SAME production length as the
# original sweep.  The first fill/up runs took the default --nprod 20000 and gave
# 41 frames against lambda=23.15's 201: a five-fold configuration-count mismatch
# ACROSS the dose ladder, which is the Dalitz D2 taint (`GATES.md`: a floor is
# drawn at the SAME sample size as the reading it gauges) and is corrected here
# rather than absorbed into a per-cell floor.
if [ "${1:-}" = "matchN" ]; then
  python3 $P --sweep --lams 20,20.5,21.5,22,25,27 --tag mw --ensemble nvt \
     --rho 0.997 -T 298 --nprod 100000 --threads 4 --out $S/water_mw_sweep_matchN.json
fi
