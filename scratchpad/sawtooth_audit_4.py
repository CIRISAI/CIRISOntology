"""Part 4: the RAW uptick (the sawtooth you can see) split into numerator and denominator,
and the tooth measured against a LOCAL NON-STEP baseline instead of a scatter of L."""
import json, os, math
import numpy as np
exec(open('/home/emoore/CIRISOntology/scratchpad/sawtooth_audit_1.py')
     .read().split('# ------------')[0])
OUT=[]
def P(s=''):
    print(s); OUT.append(s)

P("="*112)
P("TABLE 7 — THE RAW STEP, SPLIT.  d ln(rent) = d ln(cost) - d ln(target) at k0 itself.")
P("  An UPTICK (the visible sawtooth) needs d ln cost > d ln target.")
P("="*112)
P(f"{'arm':>3} {'k0':>3} {'|S|':>8} {'condition':>10} {'d ln rent':>11} {'d ln cost':>11} "
  f"{'d ln target':>12} {'uptick?':>8}")
for arm,k0 in [('A',8),('A',12),('A',16),('A',20),('A',24),('A',28),('B',8),('B',16),('B',32)]:
    ks = ALLK_A if arm=='A' else ALLK_B
    up = 0
    for eps,lab in COND:
        s = series(arm,eps,lab,ks)
        dr, dc, dt = L(s,k0,0), L(s,k0,1), L(s,k0,2)
        u = 'UP' if dr>0 else 'dn'
        up += dr>0
        P(f"{arm:>3} {k0:>3} {NS[(arm,k0-1)]:>3}->{NS[(arm,k0)]:<3} {CLAB[(eps,lab)]:>10} "
          f"{dr*100:>10.4f}pp {dc*100:>10.4f}pp {dt*100:>11.4f}pp {u:>8}")
    P(f"   -> raw upticks {up}/6")
    P('-'*112)

P()
P("="*112)
P("TABLE 8 — THE TOOTH AGAINST A LOCAL NON-STEP BASELINE (the honest null for the statistic).")
P("  baseline = mean tooth at the non-step k within +-3 of k0; sd = their scatter.")
P("  The campaign's quoted 'resolution' is the sd of the three L values, which is NOT the")
P("  null distribution of the tooth statistic.")
P("="*112)
P(f"{'arm':>3} {'k0':>3} {'condition':>10} {'tooth(k0)':>10} {'local non-step mean':>20} "
  f"{'sd':>8} {'excess over local':>18} {'x sd':>8}")
for arm,k0,steps in [('A',24,{8,12,16,20,24,28}),('A',28,{8,12,16,20,24,28}),
                     ('B',16,{8,16,32}),('B',32,{8,16,32})]:
    ks = ALLK_A if arm=='A' else ALLK_B
    for eps,lab in COND:
        s = series(arm,eps,lab,ks)
        t0,_ = tooth(s,k0,0,'fwd')
        if t0 is None:
            t0,_ = tooth(s,k0,0,'bwd')
        loc=[]
        for kk in range(k0-3,k0+4):
            if kk==k0 or kk in steps: continue
            tv,_ = tooth(s,kk,0,'fwd')
            if tv is None: tv,_ = tooth(s,kk,0,'bwd')
            if tv is not None: loc.append(tv*100)
        if not loc or t0 is None: continue
        m,sd = float(np.mean(loc)), float(np.std(loc,ddof=1))
        P(f"{arm:>3} {k0:>3} {CLAB[(eps,lab)]:>10} {t0*100:>10.4f} {m:>20.4f} {sd:>8.4f} "
          f"{t0*100-m:>18.4f} {(t0*100-m)/sd if sd>0 else float('nan'):>8.1f}")
    P('-'*112)
open('/home/emoore/CIRISOntology/scratchpad/part4.txt','w').write('\n'.join(OUT))
