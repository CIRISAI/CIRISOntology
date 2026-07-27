"""sawtooth_stake.py — emits the exact table the prereg stakes. Run before the prereg
is committed; every band in SAWTOOTH_FORWARD_PREREG.md is copied from this output.
"""
import json, os, math
import numpy as np
from sawtooth_calib import load, teeth, CONDS

HERE = os.path.dirname(os.path.abspath(__file__))
LN2 = math.log(2.0)
TOL = 0.20          # +/-20% band on the height law (within-arm interp err 3.3%, cross-arm 10%)
G_LO, G_HI = -0.6, 1.1


def main():
    rent, ns = load()
    T, SD = {}, {}
    for arm in ('A', 'B'):
        for c in CONDS:
            s = rent[arm][c]
            for k, (t, sd) in teeth(s, min(s), max(s)).items():
                T[(arm, k, c)], SD[(arm, k, c)] = t, sd
    jump = lambda arm, k: 100.0 * (math.log(ns[arm][k]) - math.log(ns[arm][k - 1]))
    C16 = {c: T[('B', 16, c)] * 16 / jump('B', 16) for c in CONDS}
    C32 = {c: T[('B', 32, c)] * 32 / jump('B', 32) for c in CONDS}
    Cint = lambda k, c: C16[c] + (C32[c] - C16[c]) * (k - 16) / 16.0

    out = {'conditions': [f'{e}|{l}' for e, l in CONDS], 'tol': TOL,
           'g_band': [G_LO, G_HI], 'C16': {f'{e}|{l}': C16[(e, l)] for e, l in CONDS},
           'C32': {f'{e}|{l}': C32[(e, l)] for e, l in CONDS}, 'plant': {}, 'after': {}}

    print('PLANTED-STEP PRESENCE BANDS  (pp)   pred = C_interp(k) * nstep*ln2*100 / k, +/-20%')
    print(f'{"k":>4} {"nstep":>6} | ' + ' '.join(f'{f"{e}/{l}":>16}' for e, l in CONDS))
    for k, nstep in [(24, 1), (26, 1), (28, 1), (30, 1), (28, 2)]:
        cells = []
        for c in CONDS:
            p = Cint(k, c) * nstep * LN2 * 100.0 / k
            lo, hi = p * (1 - TOL), p * (1 + TOL)
            out['plant'][f'{k}|{nstep}|{c[0]}|{c[1]}'] = [p, lo, hi]
            cells.append(f'{p:5.2f} [{lo:4.2f},{hi:5.2f}]')
        print(f'{k:>4} {nstep:>6} | ' + ' '.join(f'{x:>16}' for x in cells))

    print()
    print('NULL for the same k (arm B natural, NO planted step) -- already measured:')
    for k in (24, 26, 28, 30):
        print(f'{k:>4} | ' + ' '.join(f'{T[("B",k,c)]:>16.3f}' for c in CONDS))
    print('  baseline resolution sd (pp):')
    for k in (24, 26, 28, 30):
        print(f'{k:>4} | ' + ' '.join(f'{SD[("B",k,c)]:>16.4f}' for c in CONDS))

    print()
    print('AFTERMATH BANDS, arm B k=33,34,35   pred = -T(32)/3 + g,  g in [-0.6,+1.1]')
    print(f'{"k":>4} | ' + ' '.join(f'{f"{e}/{l}":>16}' for e, l in CONDS))
    cells = []
    for c in CONDS:
        t32 = T[('B', 32, c)]
        lo, hi = -t32 / 3.0 + G_LO, -t32 / 3.0 + G_HI
        for k in (33, 34, 35):
            out['after'][f'{k}|{c[0]}|{c[1]}'] = [-t32 / 3.0, lo, hi]
        cells.append(f'[{lo:+5.2f},{hi:+5.2f}]')
    for k in (33, 34, 35):
        print(f'{k:>4} | ' + ' '.join(f'{x:>16}' for x in cells))
    print(f'\n  T(32) per condition: ' + ' '.join(f'{T[("B",32,c)]:.3f}' for c in CONDS))
    print(f'  resolution sd at 32: ' + ' '.join(f'{SD[("B",32,c)]:.4f}' for c in CONDS))
    json.dump(out, open(os.path.join(HERE, 'sawtooth_stake.json'), 'w'), indent=1)
    print('\nwrote sawtooth_stake.json')


if __name__ == '__main__':
    main()
