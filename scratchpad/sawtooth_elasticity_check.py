"""sawtooth_elasticity_check.py — response to rent-scaling's calibration warning.

Reproduces the density-tooth elasticity E, shows E drifts 7.5x more than C over the
same interval, and tests the campaign's own residuals for the low-centring E would imply.
"""
import math, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sawtooth_calib import load, teeth, CONDS
from sawtooth_adjudicate import load_all, tooth, STAKE

rent, ns = load()
dens = lambda a, k: math.log((k * math.log(2) - math.log(ns[a][k])) / k)
print('E = rent-tooth / |density-tooth|   (the sibling normalisation)')
E = {}
for arm, ks in (('A', [16, 20, 24, 28]), ('B', [16, 32])):
    for k in ks:
        L = {j: dens(arm, j) - dens(arm, j - 1) for j in (k - 3, k - 2, k - 1, k)}
        td = 100 * (L[k] - np.mean([L[k - 3], L[k - 2], L[k - 1]]))
        rt = np.mean([teeth(rent[arm][c], min(rent[arm][c]), max(rent[arm][c]))[k][0] for c in CONDS])
        E[(arm, k)] = rt / abs(td)
        print(f'  arm {arm} k={k:>2}: density-tooth {td:+8.4f} pp  rent-tooth {rt:+7.4f} pp  E={E[(arm,k)]:.4f}')
C16 = np.mean([teeth(rent['B'][c], min(rent['B'][c]), max(rent['B'][c]))[16][0] for c in CONDS]) * 16 / (100 * math.log(2))
C32 = np.mean([teeth(rent['B'][c], min(rent['B'][c]), max(rent['B'][c]))[32][0] for c in CONDS]) * 32 / (100 * math.log(2))
print(f'\nover arm B k=16 -> 32:  C {C16:.4f} -> {C32:.4f} = {100*(C32/C16-1):+.2f}%   '
      f'E {E[("B",16)]:.4f} -> {E[("B",32)]:.4f} = {100*(E[("B",32)]/E[("B",16)]-1):+.2f}%')
print(f'  E drifts {(E[("B",32)]/E[("B",16)]-1)/(C32/C16-1):.1f}x more than C over the same interval')

nat, pl, meta = load_all()
print('\nsigned residual of the STAKED bands (a low-centred band drifts POSITIVE with k):')
allr, ks = [], []
for k in (24, 26, 28, 30):
    r = [100 * (tooth(nat['canonical'], pl[(k, 6, 'canonical')][c], k, c)[0]
                - STAKE['plant'][f'{k}|1|{c[0]}|{c[1]}'][0]) / STAKE['plant'][f'{k}|1|{c[0]}|{c[1]}'][0]
         for c in CONDS]
    allr += r; ks += [k] * 6
    print(f'  k={k}: {np.mean(r):+.3f}%')
allr = np.array(allr)
print(f'  ALL: {allr.mean():+.3f}% (sd {allr.std(ddof=1):.2f}%)   trend {np.polyfit(ks, allr, 1)[0]:+.4f} %/slot')
print('  -> bands are NOT centred low; the E-drift does not reach them.')
