"""Is share_3(gamma-mixture, BSC(s)) with gamma = s EXACTLY the k=4 symmetric-noise
floor at the same s?  Four accidental 7-figure matches say test it properly."""
import math, sys
import numpy as np
sys.path.insert(0,"/home/emoore/CIRISOntology/scratchpad")
import pump_curve as PC
sh3 = lambda p: PC.share3_golden(p)
def mix(g):
    p=np.zeros((2,2,2)); p[0,0,0]=g; p[1,1,1]=1-g; return p
def rep4(s):
    return PC.apply_percell(PC.repetition(4),[PC.kernel(0.0,s)]*4)
print(f"{'s':>7}{'k=4 rep, BSC(s)':>20}{'k=3 mix(gamma=s), BSC(s)':>28}{'|diff|':>12}")
w=0.0
for s in (0.02,0.05,0.08,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45):
    a=PC.share_dual(rep4(s))["share_upper"]
    b=sh3(PC.apply_percell(mix(s),[PC.kernel(0.0,s)]*3))
    w=max(w,abs(a-b)); print(f"{s:7.2f}{a:20.10e}{b:28.10e}{abs(a-b):12.2e}")
print(f"\nworst |difference| = {w:.3e}   -> {'IDENTITY (to solver precision)' if w<1e-9 else 'NOT an identity'}")

print("\nMechanism candidate: condition the k=4 pumped state on slot 4.")
print("P(slot4=1)=1/2, and the posterior on the hidden bit is exactly (s, 1-s),")
print("so slots 1-3 given slot4=1 ARE the gamma=s three-slot mixture.  Check:")
s=0.17
q=rep4(s); cond=q[:,:,:,1]; cond=cond/cond.sum()
m=PC.apply_percell(mix(s),[PC.kernel(0.0,s)]*3)
print(f"   |P(slots123 | slot4=1) - mix(gamma=s) pushed| = {np.abs(cond-m).max():.3e}")
print(f"   share of that conditional = {sh3(cond):.10e}")
print(f"   shareK of the k=4 state   = {PC.share_dual(q)['share_upper']:.10e}")
