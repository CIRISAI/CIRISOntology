"""GATE 7: the k-general dual solver, checked where an exact answer exists."""
import math, sys
import numpy as np
sys.path.insert(0,"/home/emoore/CIRISOntology/scratchpad")
sys.path.insert(0,"/tmp/claude-1000/-home-emoore-CIRISOntology/4cf4fa5c-aaa3-4173-83b9-978cb75c887f/scratchpad")
import pump_curve as PC
from gate_pump_indep import share3_independent
LN2=math.log(2.0); ok=lambda b:"PASS" if b else "**FAIL**"
rng=np.random.default_rng(11)

print("7a. k=3: the GENERAL dual solver vs the exact 1-D solver (must agree)")
w=0.0
for _ in range(300):
    p=rng.random(8); p/=p.sum(); p=p.reshape(2,2,2)
    try: g=PC.share_dual(p)
    except Exception as e: print("   dual raised:",e); break
    g=g["share_upper"] if isinstance(g,dict) else (g[0] if isinstance(g,tuple) else g)
    w=max(w,abs(float(g)-share3_independent(p)))
print(f"   worst |dual - exact| over 300 random k=3 states = {w:.3e}  (staked 1e-6)  {ok(w<1e-6)}")

print("7b. k=3 pumped states (near-deterministic, the ipf-sharek-boundary-drift regime)")
w=0.0; rows=[]
for s in (0.02,0.1,0.3):
    for a in (0.01,0.05,0.2):
        if abs(a)>2*min(s,1-s): continue
        p=PC.apply_percell(PC.repetition(3),[PC.kernel(a,s)]*3)
        ex=share3_independent(p)
        g=PC.share_dual(p); g=g["share_upper"]
        try:
            ip=PC.share_ipf(p)[0]
        except Exception: ip=float('nan')
        rows.append((s,a,ex,float(g),float(ip)))
        w=max(w,abs(float(g)-ex))
print(f"   {'s':>6}{'a':>7}{'exact':>14}{'dual':>14}{'IPF':>14}{'IPF/exact':>11}")
for s,a,ex,g,ip in rows:
    r=ip/ex if ex>1e-300 else float('nan')
    print(f"   {s:6.2f}{a:7.3f}{ex:14.6e}{g:14.6e}{ip:14.6e}{r:11.4f}")
print(f"   worst |dual - exact| = {w:.3e}  {ok(w<1e-6)}")

print("7c. k=4..6 repetition code under the pump: dual must be an UPPER bound on")
print("    a rigorous lower bound, and share must be >= 0 and <= the cap in force")
for k in (4,5,6):
    p=PC.apply_percell(PC.repetition(k),[PC.kernel(0.1,0.15)]*k)
    g=PC.share_dual(p)
    cap=(k-2)*LN2
    u,l,res=g["share_upper"],g["share_lower"],g.get("residual",float("nan"));print(f"   k={k} upper={u:.6e} lower={l:.6e} bracket={u-l:.2e} resid={res:.1e} "f" >=0 {ok(l>=-1e-9)} <=(k-2)ln2={cap:.4f} {ok(u<=cap+1e-9)} bracket<=1e-6 {ok(abs(u-l)<=1e-6)}")

print("7d. never-from-nothing at k=4..6: a PRODUCT input must mint exactly zero")
for k in (4,5,6):
    m=rng.random(k)*0.6+0.2
    p=np.ones((2,)*k)
    for i in range(k):
        sh=[1]*k; sh[i]=2
        p=p*np.array([1-m[i],m[i]]).reshape(sh)
    q=PC.apply_percell(p,[PC.kernel(0.2,0.25)]*k)
    g=float(PC.share_dual(q)["share_upper"])
    print(f"   k={k}  share(channel(product)) = {g: .3e}   {ok(abs(g)<1e-9)}")
