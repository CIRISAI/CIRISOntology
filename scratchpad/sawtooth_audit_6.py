"""Part 6: the VALID counterfactual -- fixed-target vs fixed-fraction, side by side,
and the target elasticity that explains the difference."""
import json, os, math
import numpy as np
exec(open('/home/emoore/CIRISOntology/scratchpad/sawtooth_audit_1.py')
     .read().split('# ------------')[0])
OUT=[]
def P(s=''):
    print(s); OUT.append(s)

P("="*100)
P("TABLE 11 — THE VALID COUNTERFACTUAL FOR THE SAWTOOTH.")
P("  The campaign ran the fixed-target protocol itself, in 2 of its 6 conditions.")
P("  There the denominator is CONSTANT by construction, so the definitional share is 0 by")
P("  construction.  Compare the tooth with and without a stepping denominator:")
P("="*100)
P(f"{'arm':>3} {'k0':>3} {'eps':>5} {'tooth @ frac 10%':>17} {'tooth @ fixed 1 nat':>20} {'ratio abs/frac':>15}")
for arm,k0,d in (('A',8,'fwd'),('A',12,'fwd'),('A',16,'fwd'),('A',20,'fwd'),
                 ('A',24,'fwd'),('A',28,'fwd'),('B',8,'fwd'),('B',16,'fwd'),('B',32,'bwd')):
    ks=ALLK_A if arm=='A' else ALLK_B
    for eps in (0.01,0.05):
        tf,_=tooth(series(arm,eps,'0.1',ks),k0,0,d)
        ta,_=tooth(series(arm,eps,'1.0nat',ks),k0,0,d)
        P(f"{arm:>3} {k0:>3} {eps:>5} {tf*100:>16.4f}pp {ta*100:>19.4f}pp {ta/tf:>15.3f}")
P()
P("="*100)
P("TABLE 12 — THE VALID COUNTERFACTUAL FOR S1 (economies of scale).")
P("="*100)
P(f"{'arm':>3} {'eps':>5} {'hold':>12} {'b_rent':>9} {'fold k=5->31':>13} "
  f"{'ln-decline':>11} {'% of the 10% frac decline':>26}")
for arm,ks in (('A',ALLK_A),('B',ALLK_B)):
    for eps in (0.01,0.05):
        ref=None
        for lab,name in (('0.1','frac 10%'),('0.5','frac 50%'),('1.0nat','fixed 1nat')):
            s=series(arm,eps,lab,ks); kk=sorted(s)
            lk=np.log(kk); lr=np.log([s[k][0] for k in kk])
            b=np.polyfit(lk,lr,1)[0]; d=lr[0]-lr[-1]
            if ref is None: ref=d
            P(f"{arm:>3} {eps:>5} {name:>12} {b:>9.4f} {math.exp(d):>12.3f}x {d:>11.4f} {100*d/ref:>25.1f}%")
        P('-'*100)
P()
P("="*100)
P("TABLE 13 — TARGET ELASTICITY eta = d ln(rent/nat) / d ln(target) AT FIXED k.")
P("  This is why the naive numerator/denominator split OVERSTATES the definitional share:")
P("  the numerator is SOLVED against the denominator, so it moves with it.")
P("="*100)
P(f"{'arm':>3} {'k':>3} {'eps':>5} {'T=1nat':>9} {'T=10%':>9} {'T=50%':>9} {'eta(1->10%)':>12} {'eta(10->50%)':>13}")
for arm,ks in (('A',[8,12,16,20,24,28,31]),('B',[16,24,31,32])):
    for k in ks:
        for eps in (0.01,0.05):
            rs={}
            for lab in ('1.0nat','0.1','0.5'):
                r=get(arm,k,eps,lab)
                if r is None: rs=None; break
                rs[lab]=r
            if not rs: continue
            e1=math.log(rs['0.1']['rent_per_nat']/rs['1.0nat']['rent_per_nat'])/ \
               math.log(rs['0.1']['achieved']/rs['1.0nat']['achieved'])
            e2=math.log(rs['0.5']['rent_per_nat']/rs['0.1']['rent_per_nat'])/ \
               math.log(rs['0.5']['achieved']/rs['0.1']['achieved'])
            P(f"{arm:>3} {k:>3} {eps:>5} {rs['1.0nat']['rent_per_nat']:>9.5f} "
              f"{rs['0.1']['rent_per_nat']:>9.5f} {rs['0.5']['rent_per_nat']:>9.5f} "
              f"{e1:>12.4f} {e2:>13.4f}")
open('/home/emoore/CIRISOntology/scratchpad/part6.txt','w').write('\n'.join(OUT))
