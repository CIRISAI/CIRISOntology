"""rent_scaling_tooth_convention.py — reproduces every number in RENT_SCALING_TOOTH_CONVENTION.md.

Committed so the ruling can be re-run rather than trusted. Both tooth conventions, arm A and
arm B, teeth and elasticities, from the primary artifacts only.
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LN2 = np.log(2)
N0 = lambda k: 4 * int(np.ceil((k + 1) / 4))
mB = lambda k: int(np.ceil(np.log2(k + 1)))
DA = lambda k: (k * LN2 - np.log(N0(k))) / k
DB = lambda k: (k * LN2 - np.log(1 << mB(k))) / k


def tooth(f, k, mode):
    L = lambda j: np.log(f(j)) - np.log(f(j - 1))
    run = [k + 1, k + 2, k + 3] if mode == 'fwd' else [k - 3, k - 2, k - 1]
    return (L(k) - np.mean([L(j) for j in run])) * 100


def load(arm):
    out = {}
    for r in json.load(open(f'{HERE}/rent_islands_results.json'))['rows']:
        if r['arm'] != arm or r.get('dropped'):
            continue
        out.setdefault((r['eps'], r['target_label']), {})[r['k']] = float(r['rent_per_nat'])
    for k in range(25, 33):
        p = f'{HERE}/rent_scaling_q2_{arm}{k}.json'
        if not os.path.exists(p):
            continue
        for r in json.load(open(p))['rows']:
            if not r.get('dropped'):
                out.setdefault((r['eps'], r['target_label']), {})[k] = float(r['rent_per_nat'])
    return out


print('=== §1 arm-A teeth, both conventions ===')
d = load('A')
for step in (24, 28):
    F, B = [], []
    for key in sorted(d):
        v = d[key]
        if not all(x in v for x in range(step - 4, step + 4)):
            continue
        F.append(tooth(lambda j, v=v: v[j], step, 'fwd'))
        B.append(tooth(lambda j, v=v: v[j], step, 'bwd'))
    print(f'  k={step}: FORWARD {np.mean(F):+.3f} pp   BACKWARD {np.mean(B):+.3f} pp   '
          f'ratio {np.mean(F)/np.mean(B):.3f}   positive fwd {sum(x>0 for x in F)}/{len(F)} '
          f'bwd {sum(x>0 for x in B)}/{len(B)}')

print('\n=== §4 elasticity = rent tooth / |ceiling tooth|, single convention throughout ===')
print(f'  {"step":14s}{"FORWARD":>12s}{"BACKWARD":>12s}')
for arm, step in (('A', 16), ('A', 20), ('A', 24), ('A', 28), ('B', 32)):
    dd, D = load(arm), (DA if arm == 'A' else DB)
    row = []
    for mode in ('fwd', 'bwd'):
        ct = tooth(D, step, mode)
        need = range(step - 4, step + 4) if mode == 'fwd' else range(step - 4, step + 1)
        ts = [tooth(lambda j, v=v: v[j], step, mode) for v in dd.values()
              if all(x in v for x in need)]
        row.append(np.mean(ts) / abs(ct) if ts else float('nan'))
    print(f'  arm {arm} k={step:<8d}{row[0]:12.3f}{row[1]:12.3f}')
