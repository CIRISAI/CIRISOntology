import json, math, sys
import numpy as np
sys.path.insert(0,"/home/emoore/CIRISOntology/scratchpad")
sys.path.insert(0,"/tmp/claude-1000/-home-emoore-CIRISOntology/4cf4fa5c-aaa3-4173-83b9-978cb75c887f/scratchpad")
import pump_curve as PC
from gate_pump_indep import share3_independent
C = lambda r: 18.0*r**4/((1+2*r)*(1+3*r)*(1-r))
print("ratio Delta/(C(r0)a^2) across one row's window -- is the deviation a power of a?")
for s,kap in ((0.005,0.99),(0.25,0.50)):
    r0=(1-2*s)**2
    av=np.geomspace(min(0.25,min(s,1-s))/100.0, min(0.25,min(s,1-s)), 9)
    rs=[]
    for a in av:
        p=PC.apply_percell(PC.repetition(3),[PC.kernel(a,s)]*3)
        rs.append(share3_independent(p)/(C(r0)*a*a))
    rs=np.array(rs)
    print(f"\n kappa={kap}  r0={r0:.4f}")
    for a,r in zip(av,rs): print(f"   a={a:9.6f}  ratio={r:.6f}  (dev {100*(r-1):+7.3f}%)")
    m=(rs-1)>1e-9
    if m.sum()>=3:
        sl=np.polyfit(np.log(av[m]),np.log(rs[m]-1),1)[0]
        print(f"   (ratio-1) ~ a^{sl:.3f}")
