"""Part 5: the CURVATURE BIAS of the tooth statistic, measured on step-free stretches,
with the fwd and bwd conventions kept apart (they have OPPOSITE bias)."""
import json, os, math
import numpy as np
exec(open('/home/emoore/CIRISOntology/scratchpad/sawtooth_audit_1.py')
     .read().split('# ------------')[0])
OUT=[]
def P(s=''):
    print(s); OUT.append(s)

STEPS_A={8,12,16,20,24,28}; STEPS_B={8,16,32}

def clean(k0,direction,steps,ks):
    w=[k0+i for i in range(1,4)] if direction=='fwd' else [k0-i for i in range(1,4)]
    if k0 in steps: return False
    if any(x in steps for x in w): return False
    return all(x in ks for x in w+[k0,k0-1])

P("="*104)
P("TABLE 9 — CURVATURE BIAS OF THE TOOTH STATISTIC, on STEP-FREE stretches only.")
P("  ARM B k=17..31 is 15 consecutive step-free widths -- the only clean stretch in the study.")
P("  fwd and bwd conventions are reported separately: the curve is convex in log, so fwd is")
P("  biased NEGATIVE and bwd is biased POSITIVE.  P-STEP32 used the bwd convention.")
P("="*104)
for arm,ks,steps in (('A',ALLK_A,STEPS_A),('B',ALLK_B,STEPS_B)):
    for direction in ('fwd','bwd'):
        P(f"  --- ARM {arm}, {direction} ---")
        P("     k  "+"".join(f"{CLAB[c]:>11}" for c in COND))
        acc={c:[] for c in COND}
        for k0 in ks:
            if not clean(k0,direction,steps,ks): continue
            cells=[]
            for eps,lab in COND:
                s=series(arm,eps,lab,ks); t,_=tooth(s,k0,0,direction)
                cells.append(f"{t*100:>11.4f}"); acc[(eps,lab)].append(t*100)
            P(f"  {k0:>4}  "+"".join(cells))
        if acc[COND[0]]:
            P("  mean:   "+"".join(f"{np.mean(acc[c]):>11.4f}" for c in COND))
            P("  sd:     "+"".join(f"{np.std(acc[c],ddof=1):>11.4f}" for c in COND))
        P()

P("="*104)
P("TABLE 10 — STEP TOOTH vs THE CONVENTION-MATCHED, STEP-FREE BIAS AT COMPARABLE k.")
P("  bias window: the 4 step-free k nearest k0 in the SAME arm and SAME convention.")
P("="*104)
P(f"{'arm':>3} {'k0':>3} {'dir':>4} {'condition':>10} {'tooth':>9} {'bias':>8} {'sd(bias)':>9} "
  f"{'step excess':>12} {'x sd':>7} {'campaign x':>11}")
for arm,k0,direction in (('A',24,'fwd'),('A',28,'fwd'),('B',16,'fwd'),('B',32,'bwd')):
    ks,steps=(ALLK_A,STEPS_A) if arm=='A' else (ALLK_B,STEPS_B)
    cand=sorted([k for k in ks if clean(k,direction,steps,ks)],key=lambda x:abs(x-k0))[:4]
    for eps,lab in COND:
        s=series(arm,eps,lab,ks)
        t,sd3=tooth(s,k0,0,direction)
        bs=[tooth(s,k,0,direction)[0]*100 for k in cand]
        m,sdb=float(np.mean(bs)),float(np.std(bs,ddof=1))
        P(f"{arm:>3} {k0:>3} {direction:>4} {CLAB[(eps,lab)]:>10} {t*100:>9.4f} {m:>8.4f} {sdb:>9.4f} "
          f"{t*100-m:>12.4f} {(t*100-m)/sdb:>7.1f} {t*100/(sd3*100):>11.1f}")
    P(f"    bias k used: {cand}")
    P('-'*104)
open('/home/emoore/CIRISOntology/scratchpad/part5.txt','w').write('\n'.join(OUT))
