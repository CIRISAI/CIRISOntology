"""Part 2: S1 exponents, the non-step baseline for the tooth, and the NULL PROTOCOL."""
import json, os, math
import numpy as np

exec(open('/home/emoore/CIRISOntology/scratchpad/sawtooth_audit_1.py')
     .read().split('# ---------------------------------------------------------------- 1. DECOMPOSITION')[0])

OUT = []
def P(s=''):
    print(s)
    OUT.append(s)

# ================================================================ 2. S1 EXPONENTS
P("=" * 108)
P("TABLE 2 — S1 DECOMPOSED.  ln(rent/nat) = ln(cost) - ln(target).  OLS on ln k, ARM A k=5..31.")
P("  b_rent = b_cost - b_target.  A NEGATIVE b_rent is 'economies of scale'.")
P("=" * 108)
P(f"{'arm':>3} {'condition':>10} {'b_rent':>9} {'b_cost':>9} {'b_target':>9} | "
  f"{'tot dln rent':>12} {'from cost':>10} {'from target':>12} {'% definitional':>14}")
S1 = []
for arm, ks in (('A', ALLK_A), ('B', ALLK_B)):
    for eps, lab in COND:
        s = series(arm, eps, lab, ks)
        kk = sorted(s)
        lk = np.log(kk)
        lr = np.log([s[k][0] for k in kk])
        lc = np.log([s[k][1] for k in kk])
        lt = np.log([s[k][2] for k in kk])
        b_r = np.polyfit(lk, lr, 1)[0]
        b_c = np.polyfit(lk, lc, 1)[0]
        b_t = np.polyfit(lk, lt, 1)[0]
        d_r, d_c, d_t = lr[-1] - lr[0], lc[-1] - lc[0], lt[-1] - lt[0]
        # share of the TOTAL decline in rent/nat attributable to the growing denominator
        pct = 100.0 * (-d_t) / d_r if abs(d_r) > 1e-12 else float('nan')
        S1.append(dict(arm=arm, cond=CLAB[(eps, lab)], b_r=b_r, b_c=b_c, b_t=b_t,
                       d_r=d_r, d_c=d_c, d_t=d_t, pct=pct))
        P(f"{arm:>3} {CLAB[(eps,lab)]:>10} {b_r:>9.4f} {b_c:>9.4f} {b_t:>9.4f} | "
          f"{d_r:>12.4f} {d_c:>10.4f} {d_t:>12.4f} {pct:>13.1f}%")
    P('-' * 108)

P()
P("  Fold-change in rent/nat over the whole measured range, and what it is with the")
P("  denominator held FIXED (i.e. the numerator alone):")
P(f"{'arm':>3} {'condition':>10} {'rent/nat fold':>14} {'cost fold':>11} {'target fold':>12}")
for r in S1:
    P(f"{r['arm']:>3} {r['cond']:>10} {math.exp(-r['d_r']):>13.3f}x {math.exp(-r['d_c']):>10.3f}x "
      f"{math.exp(r['d_t']):>11.3f}x")

# ================================================================ 3. NON-STEP BASELINE
P()
P("=" * 108)
P("TABLE 3 — THE TOOTH AT EVERY k, STEP AND NON-STEP (forward convention, ARM A k=5..31).")
P("  If the statistic is unbiased the non-step values sit at ~0.  Curvature bias would put")
P("  them systematically off zero, and the 'tooth' would be partly that bias.")
P("=" * 108)
for arm, ks, steps in (('A', ALLK_A, {8, 12, 16, 20, 24, 28}), ('B', ALLK_B, {8, 16, 32})):
    P(f"  --- ARM {arm} ---")
    P("    k  " + "".join(f"{CLAB[c]:>11}" for c in COND) + "   step?")
    nonstep = {c: [] for c in COND}
    for k0 in ks:
        cells, ok = [], False
        for eps, lab in COND:
            s = series(arm, eps, lab, ks)
            t, _ = tooth(s, k0, 0, 'fwd')
            if t is None:
                cells.append(f"{'':>11}")
            else:
                ok = True
                cells.append(f"{t*100:>11.3f}")
                if k0 not in steps:
                    nonstep[(eps, lab)].append(t * 100)
        if ok:
            P(f" {k0:>4}  " + "".join(cells) + ("   STEP" if k0 in steps else ""))
    P("  non-step mean:  " + "".join(f"{np.mean(nonstep[c]):>11.3f}" for c in COND))
    P("  non-step sd:    " + "".join(f"{np.std(nonstep[c], ddof=1):>11.3f}" for c in COND))
    P("  non-step max:   " + "".join(f"{np.max(np.abs(nonstep[c])):>11.3f}" for c in COND))
    P()

# ================================================================ 4. NULL PROTOCOL
P("=" * 108)
P("TABLE 4 — THE NULL MAINTENANCE PROTOCOL.  No repair dynamics anywhere: the 'cost' is a")
P("  trivial function of the structure, pushed through the IDENTICAL rent/nat = cost/target.")
P("    N0  cost = 1                  (a constant; pays nothing for size)")
P("    N1  cost = eps * k            (pay per slot)")
P("    N2  cost = |S|                (pay per support point)")
P("    N3  cost = eps * share_max(k) (pay per nat available -- the 'perfectly proportional' null)")
P("=" * 108)

NULLS = {
    'N0 const': lambda k, ns, eps: 1.0,
    'N1 k': lambda k, ns, eps: eps * k,
    'N2 |S|': lambda k, ns, eps: float(ns),
    'N3 sharemax': lambda k, ns, eps: eps * (k * LN2 - math.log(ns)),
}

def null_series(arm, eps, lab, ks, f):
    out = {}
    for k in ks:
        r = get(arm, k, eps, lab)
        if r is None:
            continue
        tgt = r['achieved']
        c = f(k, r['ns'], eps)
        out[k] = (c / tgt, c, tgt)
    return out

for name, f in NULLS.items():
    P(f"  ---- NULL {name} ----")
    P(f"{'arm':>3} {'k0':>3} {'dir':>3} {'condition':>10} {'MEASURED tooth':>15} {'NULL tooth':>11} "
      f"{'null/meas':>10} | {'b_rent meas':>12} {'b_rent null':>12}")
    for arm, k0, direction in [('A', 24, 'fwd'), ('A', 28, 'fwd'), ('B', 16, 'fwd'), ('B', 32, 'bwd')]:
        ks = ALLK_A if arm == 'A' else ALLK_B
        for eps, lab in COND:
            s = series(arm, eps, lab, ks)
            sn = null_series(arm, eps, lab, ks, f)
            tm, _ = tooth(s, k0, 0, direction)
            tn, _ = tooth(sn, k0, 0, direction)
            if tm is None or tn is None:
                continue
            kk = sorted(s)
            lk = np.log(kk)
            b_m = np.polyfit(lk, np.log([s[k][0] for k in kk]), 1)[0]
            b_n = np.polyfit(lk, np.log([sn[k][0] for k in kk]), 1)[0]
            rat = tn / tm if abs(tm) > 1e-12 else float('nan')
            P(f"{arm:>3} {k0:>3} {direction:>3} {CLAB[(eps,lab)]:>10} {tm*100:>15.4f} {tn*100:>11.4f} "
              f"{rat:>10.3f} | {b_m:>12.4f} {b_n:>12.4f}")
        P('   ' + '-' * 100)
    P()

open('/home/emoore/CIRISOntology/scratchpad/part2.txt', 'w').write('\n'.join(OUT))
