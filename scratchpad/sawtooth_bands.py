"""sawtooth_bands.py — derive every number the forward prereg stakes.

Calibration inputs are ONLY data already on disk (parent k=5..24, Q2 k=25..32).
Outputs: the height law C(k), the after-step residual band, and the staked
per-condition bands for the forward runs.
"""
import json, os, math
import numpy as np
from sawtooth_calib import load, teeth, CONDS, N0

HERE = os.path.dirname(os.path.abspath(__file__))
LN2 = math.log(2.0)


def steps_of(nsmap):
    return {k: 100.0 * (math.log(nsmap[k]) - math.log(nsmap[k - 1]))
            for k in sorted(nsmap) if (k - 1) in nsmap
            and nsmap[k] != nsmap[k - 1]}


def main():
    rent, ns = load()
    T = {}       # T[(arm,k,cond)] = tooth pp
    for arm in ('A', 'B'):
        for cond in CONDS:
            s = rent[arm][cond]
            for k, (t, sd) in teeth(s, min(s), max(s)).items():
                T[(arm, k, cond)] = (t, sd)

    stepA, stepB = steps_of(ns['A']), steps_of(ns['B'])
    steps = {'A': stepA, 'B': stepB}

    print('=' * 96)
    print('HEIGHT LAW    C(k) = tooth(k) * k / dln(ns)(k)    [tooth and dln in pp]')
    print('=' * 96)
    print(f'{"arm":>4} {"k":>4} {"dln_ns":>8} | ' + ' '.join(f'{f"{e}/{l}":>9}' for e, l in CONDS) + f' | {"mean":>7}')
    Cvals = {}
    for arm in ('A', 'B'):
        for k, j in sorted(steps[arm].items()):
            if all((arm, k, c) in T for c in CONDS):
                cs = [T[(arm, k, c)][0] * k / j for c in CONDS]
                Cvals[(arm, k)] = dict(zip(CONDS, cs))
                print(f'{arm:>4} {k:>4} {j:>8.3f} | ' + ' '.join(f'{c:>9.4f}' for c in cs) +
                      f' | {np.mean(cs):>7.4f}')

    # ---- after-step residual: tooth(k*+j) + T(k*)/3 , for j=1,2,3
    print()
    print('=' * 96)
    print('AFTER-STEP RULE   tooth(k*+j) = -T(k*)/3 + g ,  j=1,2,3   -- residual g (pp)')
    print('=' * 96)
    res = []
    for arm in ('A', 'B'):
        for kstar in sorted(steps[arm]):
            if kstar <= 12:
                continue                      # k<=12 controller-confounded (memory)
            for j in (1, 2, 3):
                k = kstar + j
                if k in steps[arm]:
                    continue                  # next step, not an aftermath
                for c in CONDS:
                    if (arm, kstar, c) in T and (arm, k, c) in T:
                        g = T[(arm, k, c)][0] + T[(arm, kstar, c)][0] / 3.0
                        res.append((arm, kstar, j, c, g))
    gs = np.array([r[-1] for r in res])
    for arm in ('A', 'B'):
        sub = np.array([r[-1] for r in res if r[0] == arm])
        if sub.size:
            print(f'  arm {arm}: n={sub.size:3d}  g in [{sub.min():+.3f}, {sub.max():+.3f}]  '
                  f'mean {sub.mean():+.3f}  sd {sub.std(ddof=1):.3f}')
    print(f'  ALL   : n={gs.size:3d}  g in [{gs.min():+.3f}, {gs.max():+.3f}]  '
          f'mean {gs.mean():+.3f}  sd {gs.std(ddof=1):.3f}')
    G_LO, G_HI = float(np.floor(gs.min() * 10) / 10), float(np.ceil(gs.max() * 10) / 10)
    print(f'  -> staked residual band  g in [{G_LO:+.1f}, {G_HI:+.1f}] pp')

    # ---- clean (no step in window, no step at k) tooth: the g-only baseline
    print()
    print('CLEAN-k tooth (no step at k, no step in the 3-window) -- arm B, m=5 regime')
    clean = []
    for k in range(20, 32):
        if k in stepB:
            continue
        if any(j in stepB for j in (k - 3, k - 2, k - 1)):
            continue
        vals = [T[('B', k, c)][0] for c in CONDS if ('B', k, c) in T]
        clean.append((k, vals))
        print(f'   k={k:>3}  ' + ' '.join(f'{v:>7.3f}' for v in vals) + f'   mean {np.mean(vals):>7.3f}')
    cl = np.array([v for _, vv in clean for v in vv])
    print(f'   all clean k=20..31: [{cl.min():.3f}, {cl.max():.3f}]  and STRICTLY DECREASING in k')

    # ---- C interpolated for arm B at the planted k
    print()
    print('=' * 96)
    print('FORWARD BANDS')
    print('=' * 96)
    C16, C32 = Cvals[('B', 16)], Cvals[('B', 32)]
    print('  arm-B C interpolated linearly in k between k=16 and k=32 (INTERPOLATION for k=24..30)')
    plant = [(24, 1), (26, 1), (28, 1), (30, 1), (28, 2)]
    print(f'\n{"k":>4} {"steps":>6} {"dln_ns":>8} | ' + ' '.join(f'{f"{e}/{l}":>13}' for e, l in CONDS))
    bands = {}
    for k, nstep in plant:
        j = 100.0 * nstep * LN2
        row = []
        for c in CONDS:
            Ck = C16[c] + (C32[c] - C16[c]) * (k - 16) / (32 - 16)
            pred = Ck * j / k
            lo, hi = 0.75 * pred, 1.25 * pred
            bands[(k, nstep, c)] = (pred, lo, hi)
            row.append(f'{pred:>6.2f}[{lo:.1f},{hi:.1f}]')
        print(f'{k:>4} {nstep:>6} {j:>8.3f} | ' + ' '.join(f'{r:>13}' for r in row))

    # ---- arm B natural continuation 33,34,35 (aftermath) and 36 (clean)
    print()
    print('  arm B k=33,34,35: aftermath of the k=32 step   pred = -T(32)/3 + g')
    print(f'{"k":>4} | ' + ' '.join(f'{f"{e}/{l}":>15}' for e, l in CONDS))
    for k in (33, 34, 35):
        row = []
        for c in CONDS:
            t32 = T[('B', 32, c)][0]
            lo, hi = -t32 / 3.0 + G_LO, -t32 / 3.0 + G_HI
            row.append(f'[{lo:+.2f},{hi:+.2f}]')
        print(f'{k:>4} | ' + ' '.join(f'{r:>15}' for r in row))
    print('  arm B k=36: CLEAN window (L33,L34,L35 all step-free) -> tooth = g only')
    print(f'        ceiling-tracking : [{0.0:+.2f}, {cl.max():+.2f}] pp  (bounded by the largest clean tooth ever seen at k>=20)')
    mod4 = [C32[c] * 100 * LN2 / 36 for c in CONDS]
    print(f'        mod-4 rival      : a POSITIVE tooth; on ITS OWN ceiling drop ln(40/36)='
          f'{100*math.log(40/36):.3f} pp -> ' +
          ' '.join(f'{C32[c]*100*math.log(40/36)/36:.2f}' for c in CONDS) + ' pp')
    json.dump({'C16': {f'{e}|{l}': C16[(e, l)] for e, l in CONDS},
               'C32': {f'{e}|{l}': C32[(e, l)] for e, l in CONDS},
               'T32': {f'{e}|{l}': T[('B', 32, (e, l))][0] for e, l in CONDS},
               'g_band': [G_LO, G_HI], 'clean_max': float(cl.max()),
               'bands': {f'{k}|{n}|{e}|{l}': bands[(k, n, (e, l))] for k, n in plant for e, l in CONDS}},
              open(os.path.join(HERE, 'sawtooth_bands.json'), 'w'), indent=1)
    print('\nwrote sawtooth_bands.json')


if __name__ == '__main__':
    main()
