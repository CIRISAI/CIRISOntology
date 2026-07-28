"""Adversarial decomposition of the rent campaign's two shapes.

rent_per_nat = cost_erase / achieved,  achieved == target (to <1e-12 rel).
  frac mode: target = f * share_max(k) = f * (k*ln2 - ln|S|)   -> DENOMINATOR STEPS with |S|
  abs  mode: target = 1.0 nat, CONSTANT in k                   -> DENOMINATOR DOES NOT STEP

So   ln(rent/nat) = ln(cost) - ln(target)
and any additive statistic T (the tooth) splits exactly:
     T[ln rent] = T[ln cost] - T[ln target]
The second term is PURE ARITHMETIC: it is a function of k and |S| only, with no dynamics.
"""
import json, os, math, itertools
import numpy as np

HERE = '/home/emoore/CIRISOntology/scratchpad'
LN2 = math.log(2)

COND = [(0.01, '0.1'), (0.01, '0.5'), (0.01, '1.0nat'),
        (0.05, '0.1'), (0.05, '0.5'), (0.05, '1.0nat')]
CLAB = {(0.01, '0.1'): 'e.01/10%', (0.01, '0.5'): 'e.01/50%', (0.01, '1.0nat'): 'e.01/1nat',
        (0.05, '0.1'): 'e.05/10%', (0.05, '0.5'): 'e.05/50%', (0.05, '1.0nat'): 'e.05/1nat'}


def load():
    rows = []
    d = json.load(open(os.path.join(HERE, 'rent_islands_results.json')))
    for r in d['rows']:
        rows.append(r)
    for f in sorted(os.listdir(HERE)):
        if f.startswith('rent_scaling_q2_') and f.endswith('.json') and f[16].isalpha():
            tag = f[len('rent_scaling_q2_'):-len('.json')]
            if not (tag[0] in 'AB' and tag[1:].isdigit()):
                continue
            rows.extend(json.load(open(os.path.join(HERE, f)))['rows'])
    return rows


ROWS = load()
TAB = {}   # (arm,k,eps,label) -> row
for r in ROWS:
    if r.get('dropped'):
        continue
    TAB[(r['arm'], r['k'], round(r['eps'], 6), r['target_label'])] = r

NS = {}
for r in ROWS:
    NS[(r['arm'], r['k'])] = r['ns']


def get(arm, k, eps, lab):
    return TAB.get((arm, k, round(eps, 6), lab))


def share_max(k, ns):
    return k * LN2 - math.log(ns)


def series(arm, eps, lab, ks):
    """returns dict k -> (rent, cost, target)"""
    out = {}
    for k in ks:
        r = get(arm, k, eps, lab)
        if r is None:
            continue
        out[k] = (r['rent_per_nat'], r['cost_erase'], r['achieved'])
    return out


def L(s, k, key):
    """log jump of component `key` (0 rent, 1 cost, 2 target) at k"""
    if k not in s or (k - 1) not in s:
        return None
    return math.log(s[k][key] / s[k - 1][key])


def tooth(s, k0, key, direction, n=3):
    """prereg §7a statistic. direction='fwd' -> baseline k0+1..k0+3, 'bwd' -> k0-3..k0-1"""
    base_ks = [k0 + i for i in range(1, n + 1)] if direction == 'fwd' else [k0 - i for i in range(1, n + 1)]
    ls = [L(s, k, key) for k in base_ks]
    l0 = L(s, k0, key)
    if l0 is None or any(x is None for x in ls):
        return None, None
    return l0 - float(np.mean(ls)), float(np.std(ls, ddof=1))


ALLK_A = list(range(5, 32))
ALLK_B = list(range(5, 33))

# ---------------------------------------------------------------- 1. DECOMPOSITION
STEPS = []   # (arm, k0, direction)
for k0 in (8, 12, 16, 20, 24, 28):
    STEPS.append(('A', k0, 'fwd'))
STEPS.append(('A', 28, 'bwd'))
for k0 in (8, 16):
    STEPS.append(('B', k0, 'fwd'))
STEPS.append(('B', 32, 'bwd'))

print("=" * 110)
print("TABLE 1 — TOOTH DECOMPOSITION.  tooth(rent) = tooth(cost) - tooth(target), exactly.")
print("  'denom-only' = -tooth(target): what the ratio does if the numerator is perfectly smooth.")
print("  units: percentage points of log jump (pp)")
print("=" * 110)
hdr = f"{'arm':>3} {'k0':>3} {'dir':>3} {'|S| step':>9} {'condition':>10} {'tooth(rent)':>12} {'denom-only':>11} {'tooth(cost)':>12} {'excess':>9} {'ratio':>7} {'base sd':>8}"
print(hdr)
DEC = []
for arm, k0, direction in STEPS:
    ks = ALLK_A if arm == 'A' else ALLK_B
    step = f"{NS[(arm,k0-1)]}->{NS[(arm,k0)]}"
    for eps, lab in COND:
        s = series(arm, eps, lab, ks)
        tr, sd = tooth(s, k0, 0, direction)
        tc, _ = tooth(s, k0, 1, direction)
        tt, _ = tooth(s, k0, 2, direction)
        if tr is None:
            continue
        den = -tt
        exc = tr - den
        ratio = tr / den if abs(den) > 1e-12 else float('nan')
        DEC.append(dict(arm=arm, k0=k0, dir=direction, cond=CLAB[(eps, lab)],
                        tooth=tr * 100, den=den * 100, tcost=tc * 100,
                        exc=exc * 100, ratio=ratio, sd=sd * 100))
        print(f"{arm:>3} {k0:>3} {direction:>3} {step:>9} {CLAB[(eps,lab)]:>10} "
              f"{tr*100:>12.4f} {den*100:>11.4f} {tc*100:>12.4f} {exc*100:>9.4f} "
              f"{ratio:>7.3f} {sd*100:>8.4f}")
    print('-' * 110)

json.dump(DEC, open('/home/emoore/CIRISOntology/scratchpad/dec.json', 'w'), indent=1)
