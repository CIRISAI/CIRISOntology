"""P-FORM as WRITTEN (pointwise Delta/a^2 within 2% 'anywhere') vs P-FORM as
IMPLEMENTED (a test on the fitted a->0 coefficient C).  Independent solver."""
import json, math, sys
import numpy as np
sys.path.insert(0,"/home/emoore/CIRISOntology/scratchpad")
sys.path.insert(0,"/tmp/claude-1000/-home-emoore-CIRISOntology/4cf4fa5c-aaa3-4173-83b9-978cb75c887f/scratchpad")
import pump_curve as PC
from gate_pump_indep import share3_independent
C = lambda r: 18.0*r**4/((1+2*r)*(1+3*r)*(1-r))
d = json.load(open("/home/emoore/CIRISOntology/scratchpad/pump_curveA.json"))
print(f"{'kappa':>6}{'r0':>8}{'a_hi':>8}{'Dlt/C(r0)a^2 @a_hi':>20}{'dev%':>9}{'2% band':>9}")
worst=0
for row in d["rows"]:
    s,r0 = row["s"], row["r0"]; a = max(row["a_vals"])
    p = PC.apply_percell(PC.repetition(3), [PC.kernel(a,s)]*3)
    ratio = share3_independent(p)/(C(r0)*a*a)
    dev = 100*abs(ratio-1)
    worst=max(worst,dev)
    print(f"{row['kappa']:6.2f}{r0:8.4f}{a:8.4f}{ratio:20.4f}{dev:9.2f}"
          f"{'PASS' if dev<=2 else '**FAIL**':>9}")
print(f"\nworst pointwise deviation at the top of a row's own window: {worst:.1f}%")
print("P-FORM as IMPLEMENTED (on the fitted C): C_ratio in "
      f"[{d['summary']['C_ratio_min']:.7f}, {d['summary']['C_ratio_max']:.7f}] -> PASS")
