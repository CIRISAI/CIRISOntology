#!/usr/bin/env python3
"""
refuter_a34.py -- ATTACK A3 (cap consistency) and ATTACK A4 (the 16-mock ensemble).

Pure re-analysis of the campaign's own recorded outputs.  No new field is built.
Post-unblind, post-hoc.  Pre-registered in REFUTER_PREREG.md.
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
GEOMS = ('folded', 'equilateral', 'squeezed')
PRIMARY = [('NGC', '15.0', '4'), ('NGC', '15.0', '6'),
           ('NGC', '10.0', '4'), ('NGC', '10.0', '6'), ('NGC', '10.0', '8'),
           ('SGC', '10.0', '4'), ('SGC', '10.0', '6'), ('SGC', '10.0', '8')]

out = {}
V = {(r['cap'], r['R'], r['b'], r['geom']): r
     for r in json.load(open(f"{HERE}/sky_final_verdict.json"))}

# ------------------------------------------------------------------ A3 cap consistency
print("=" * 100)
print("A3 -- CAP CONSISTENCY.  Gravity is isotropic: the two caps must agree in AMPLITUDE,")
print("     not merely both be positive.  Patchy predicts them equal to 0.6-1.8 %.")
print("=" * 100)
print("  %-5s %-2s %-12s %11s %11s %9s %9s %8s %10s"
      % ("R", "b", "geom", "NGC", "SGC", "sig_N", "sig_S", "diff/sig", "pred N-S"))
a3 = []
for R in ('15.0', '10.0'):
    for b in ('4', '6', '8'):
        for g in GEOMS:
            n, s = V.get(('NGC', R, b, g)), V.get(('SGC', R, b, g))
            if not (n and s):
                continue
            d = n['target'] - s['target']
            e = np.hypot(n['sigma'], s['sigma'])
            pd = n['pred_valve'] - s['pred_valve']
            a3.append(dict(R=R, b=b, geom=g, ngc=n['target'], sgc=s['target'],
                           diff=d, err=e, z=d / e, pred_diff=pd,
                           pred_rel=pd / (0.5 * (n['pred_valve'] + s['pred_valve']))))
            print("  %-5s %-2s %-12s %11.4e %11.4e %9.2e %9.2e %8.2f %10.4e"
                  % (R, b, g, n['target'], s['target'], n['sigma'], s['sigma'], d / e, pd))
out['a3'] = a3
fold = [x for x in a3 if x['geom'] == 'folded']
print("\n  FOLDED rows only, |z| for NGC-vs-SGC amplitude difference:")
for x in fold:
    print("    R=%-5s b=%-2s  NGC/SGC = %.4f   z = %+.2f   (mocks predict ratio %.4f)"
          % (x['R'], x['b'], x['ngc'] / x['sgc'], x['z'],
             (x['pred_diff'] + 0) / 1 * 0 + (V[('NGC', x['R'], x['b'], 'folded')]['pred_valve']
                                             / V[('SGC', x['R'], x['b'], 'folded')]['pred_valve'])))
zmax = max(abs(x['z']) for x in fold)
print(f"\n  worst folded cap-difference: |z| = {zmax:.2f}")
print("  16-mock sigma is itself uncertain by 1/sqrt(2*15) = 18 %; inflating both errors by")
print(f"  1.18 gives worst |z| = {zmax/1.18:.2f}, deflating gives {zmax*1.18:.2f}.")

# ------------------------------------------------------------------ A4 ensemble size
print("\n" + "=" * 100)
print("A4 -- THE 16-MOCK ENSEMBLE.  sigma and the recomputed prediction both come from 16")
print("     mocks/cap.  sky_surrogate_*.json has 128 of the SAME mocks with I(mock), I(N1).")
print("=" * 100)
a4 = {}
for cap in ('NGC', 'SGC'):
    S = json.load(open(f"{HERE}/sky_surrogate_{cap}.json"))['res']       # 128 mock+N1 pairs
    M = json.load(open(f"{HERE}/sky_stage7_mocks_{cap}.json"))['res']    # 16 mock+N1+N2
    n128, n16 = len(S), len(M)
    print(f"\n  [{cap}]  surrogate suite n={n128}   stage-7 mock-side n={n16}")
    rows = []
    for (c, R, b) in [p for p in PRIMARY if p[0] == cap]:
        Rf = float(R)
        bi = int(b)
        g = 'folded'
        try:
            im128 = np.array([x['mock'][R]['b'][b][g]['I'] for x in S])
            i1128 = np.array([x['surr'][R]['b'][b][g]['I'] for x in S])
        except KeyError:
            im128 = np.array([x['mock'][str(Rf)]['b'][str(bi)][g]['I'] for x in S])
            i1128 = np.array([x['surr'][str(Rf)]['b'][str(bi)][g]['I'] for x in S])
        im16 = np.array([x['mock'][R]['b'][b][g]['I'] for x in M])
        i116 = np.array([x['n1'][R]['b'][b][g]['I'] for x in M])
        i216 = np.array([x['n2'][R]['b'][b][g]['I'] for x in M])
        # integrity: are the first 16 of the 128 the SAME realisations?
        same = float(np.abs(im128[:16] - im16).max())
        tgt16 = im16 - i216                       # what the campaign used
        e128 = im128 - i1128                      # available for all 128
        e16 = im16 - i116
        v16 = i216 - i116                         # valve, mock side
        # 128-mock reconstruction of the prediction and its scatter
        pred128 = e128.mean() - v16.mean()
        # var(e - v) = var(e) + var(v) - 2cov(e,v); use the 16-mock covariance for the cross term
        cov = np.cov(e16, v16, ddof=1)
        sd128 = float(np.sqrt(max(e128.var(ddof=1) + cov[1, 1] - 2 * cov[0, 1], 0)))
        row = dict(cap=cap, R=R, b=b,
                   mock_I_match_max_abs_diff=same,
                   pred16=float(tgt16.mean()), sd16=float(tgt16.std(ddof=1)),
                   pred128=float(pred128), sd128=sd128,
                   e128_mean=float(e128.mean()), e16_mean=float(e16.mean()),
                   e128_sd=float(e128.std(ddof=1)), e16_sd=float(e16.std(ddof=1)),
                   valve_mean=float(v16.mean()), valve_sd=float(v16.std(ddof=1)))
        vv = V[(cap, R, b, 'folded')]
        row['target'] = vv['target']
        row['consist16'] = (vv['target'] - row['pred16']) / row['sd16']
        row['consist128'] = (vv['target'] - row['pred128']) / row['sd128']
        row['detect16'] = vv['target'] / row['sd16']
        row['detect128'] = vv['target'] / sd128
        rows.append(row)
        print("    R=%-5s b=%-2s | first-16 I(mock) identical to suite: max|d| = %.2e" %
              (R, b, same))
        print("        E[I_mock-I_N1]:  16 mocks %.5e +- %.2e   128 mocks %.5e +- %.2e  "
              "(shift %+.2f SEM16)"
              % (e16.mean(), e16.std(ddof=1) / 4, e128.mean(),
                 e128.std(ddof=1) / np.sqrt(128),
                 (e128.mean() - e16.mean()) / (e16.std(ddof=1) / 4)))
        print("        prediction:      16 %.5e (sd %.3e)    128-reconstructed %.5e (sd %.3e)"
              % (row['pred16'], row['sd16'], row['pred128'], sd128))
        print("        detection:       16 %.1f sigma -> 128 %.1f sigma | consistency %+.2f -> %+.2f"
              % (row['detect16'], row['detect128'], row['consist16'], row['consist128']))
    a4[cap] = rows
out['a4'] = a4

json.dump(out, open(f"{HERE}/refuter_a34.json", 'w'), indent=1, default=float)
print("\n  written refuter_a34.json")
