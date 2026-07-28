"""Part 3: the PLANTED arm decomposed, and the B31->B32 exact-share_max control."""
import json, os, math
import numpy as np
exec(open('/home/emoore/CIRISOntology/scratchpad/sawtooth_audit_1.py')
     .read().split('# ------------')[0])

OUT = []
def P(s=''):
    print(s); OUT.append(s)

# ---- the exact control the campaign already owns but did not read this way
P("=" * 100)
P("TABLE 5 — THE B31 -> B32 STEP: share_max IS EXACTLY UNCHANGED.")
P("  31*ln2 - ln32 = 32*ln2 - ln64.  So at this step the TARGET is identical in every")
P("  condition (frac AND abs), the fraction-of-capacity held is identical, and only k and")
P("  |S| move.  Any tooth here is UNCONTAMINATED by the stepping denominator.")
P("=" * 100)
sm31 = 31 * LN2 - math.log(32)
sm32 = 32 * LN2 - math.log(64)
P(f"  share_max(B31) = {sm31:.12f}   share_max(B32) = {sm32:.12f}   difference = {sm32-sm31:.3e}")
P()
P(f"{'condition':>10} {'target(31)':>12} {'target(32)':>12} {'d ln target':>12} "
  f"{'cost(31)':>11} {'cost(32)':>11} {'d ln cost':>11} {'d ln rent':>11}")
for eps, lab in COND:
    a, b = get('B', 31, eps, lab), get('B', 32, eps, lab)
    dl_t = math.log(b['achieved'] / a['achieved'])
    dl_c = math.log(b['cost_erase'] / a['cost_erase'])
    dl_r = math.log(b['rent_per_nat'] / a['rent_per_nat'])
    P(f"{CLAB[(eps,lab)]:>10} {a['achieved']:>12.6f} {b['achieved']:>12.6f} {dl_t*100:>11.4f}pp "
      f"{a['cost_erase']:>11.6f} {b['cost_erase']:>11.6f} {dl_c*100:>10.4f}pp {dl_r*100:>10.4f}pp")

# ---- the planted arm
P()
P("=" * 100)
P("TABLE 6 — THE PLANTED ARM (P-PLANT), DECOMPOSED.")
P("  Ladder: natural m=5 at k0-3..k0-1, then a PLANTED m=6 (|S| 32->64) at k0.")
P("  tooth = L(k0) - mean(L(k0-1), L(k0-2), L(k0-3)) with the planted rent at k0.")
P("=" * 100)


def load_plant(f):
    d = json.load(open(os.path.join(HERE, f)))
    out = {}
    for r in d['rows']:
        if not r.get('dropped'):
            out[(round(r['eps'], 6), r['target_label'])] = r
    return out


def nat_row(k, eps, lab):
    r = get('B', k, eps, lab)
    if r is not None:
        return r
    f = os.path.join(HERE, f'sawtooth_B{k}.json')
    if os.path.exists(f):
        return load_plant(f'sawtooth_B{k}.json').get((round(eps, 6), lab))
    return None


P(f"{'k0':>3} {'condition':>10} {'tooth(rent)':>12} {'denom-only':>11} {'tooth(cost)':>12} "
  f"{'excess':>9} {'% definitional':>14}")
for k0, pf in ((24, 'sawtooth_P24m6.json'), (26, 'sawtooth_P26m6.json'),
               (28, 'sawtooth_P28m6.json'), (30, 'sawtooth_P30m6.json')):
    if not os.path.exists(os.path.join(HERE, pf)):
        continue
    PL = load_plant(pf)
    for eps, lab in COND:
        key = (round(eps, 6), lab)
        if key not in PL:
            continue
        rows = {k: nat_row(k, eps, lab) for k in range(k0 - 4, k0)}
        if any(v is None for v in rows.values()):
            continue
        rows[k0] = PL[key]
        def Lc(k, field):
            return math.log(rows[k][field] / rows[k - 1][field])
        base = [Lc(k, 'rent_per_nat') for k in range(k0 - 3, k0)]
        tr = Lc(k0, 'rent_per_nat') - float(np.mean(base))
        tt = Lc(k0, 'achieved') - float(np.mean([Lc(k, 'achieved') for k in range(k0 - 3, k0)]))
        tc = Lc(k0, 'cost_erase') - float(np.mean([Lc(k, 'cost_erase') for k in range(k0 - 3, k0)]))
        den = -tt
        P(f"{k0:>3} {CLAB[(eps,lab)]:>10} {tr*100:>12.4f} {den*100:>11.4f} {tc*100:>12.4f} "
          f"{(tr-den)*100:>9.4f} {100*den/tr if abs(tr)>1e-12 else float('nan'):>13.1f}%")
    P('-' * 100)

open('/home/emoore/CIRISOntology/scratchpad/part3.txt',
     'w').write('\n'.join(OUT))
