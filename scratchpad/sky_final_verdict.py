#!/usr/bin/env python3
"""
sky_final_verdict.py -- the campaign's last scoring, per Amendment 5.

Everything is measured against the SAME null on both sides, which is the whole point:

  target_data       = I(data) - mean_nulls I(N2 of data)
  prediction_valve  = mean_mocks [ I(mock) - I(N2 of that mock) ]      <- recomputed, same null
  sigma             = std_mocks [ I(mock) - I(N2 of that mock) ]       <- cosmic variance of
                                                                          the target itself
  detection         = target_data / sigma
  consistency       = (target_data - prediction_valve) / sigma
  valve floor       = I(N2) - I(N1),  reported, and an UPPER BOUND while clipping is large

The FROZEN Stage-5 prediction is reported unchanged alongside, and is NOT used for the
consistency test -- it was computed against the plain surrogate and the two are not comparable.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
GEOMS = ('folded', 'equilateral', 'squeezed')
EXCLUDED = ('NGC', '15.0', '4', 'squeezed')


def main():
    dv = json.load(open(f"{HERE}/sky_stage7_valve.json"))
    frz = json.load(open(f"{HERE}/sky_stage5_frozen_prediction.json"))
    rows = []
    print("FINAL VERDICT (Amendment 5).  Same null on both sides.\n")
    print("  %-4s %-5s %-2s %-12s %11s %11s %10s %11s %8s %8s"
          % ("cap", "R", "b", "geom", "target", "pred_valve", "sigma",
             "valve", "detect", "consist"))
    for cap in ('SGC', 'NGC'):
        if cap not in dv:
            continue
        p = f"{HERE}/sky_stage7_mocks_{cap}.json"
        if not os.path.exists(p):
            print(f"  [{cap}] mock-side valve not available"); continue
        mk = json.load(open(p))['res']
        d = dv[cap]
        for R in ('15.0', '10.0'):
            for b in ('4', '6', '8'):
                for g in GEOMS:
                    e = d['data'][R]['b'][b][g]
                    if not e.get('occupancy_pass'):
                        continue
                    if (cap, R, b, g) == EXCLUDED:
                        print(f"  {cap:<4} {R:<5} {b:<2} {g:<12} EXCLUDED by prior ruling")
                        continue
                    i1 = np.array([x[R]['b'][b][g]['I'] for x in d['n1']])
                    i2 = np.array([x[R]['b'][b][g]['I'] for x in d['n2']])
                    tgt = e['I'] - i2.mean()
                    valve = i2.mean() - i1.mean()
                    mt = np.array([x['mock'][R]['b'][b][g]['I']
                                   - x['n2'][R]['b'][b][g]['I'] for x in mk])
                    pv, sd = mt.mean(), mt.std(ddof=1)
                    det = tgt / sd if sd > 0 else np.nan
                    con = (tgt - pv) / sd if sd > 0 else np.nan
                    rows.append(dict(cap=cap, R=R, b=b, geom=g, target=tgt, pred_valve=pv,
                                     sigma=sd, valve=valve, detect=det, consist=con,
                                     frozen=frz.get(f"{cap}|{R}|{b}|{g}", {}).get('signal')))
                    print("  %-4s %-5s %-2s %-12s %11.4e %11.4e %10.3e %11.4e %8.1f %8.2f"
                          % (cap, R, b, g, tgt, pv, sd, valve, det, con))
    fold = [r for r in rows if r['geom'] == 'folded']
    print("\n  PRIMARY (folded) — outcome (a) requires >=5 sigma above the combined floor,")
    print("  two or more b passing G9, and consistency with the prediction:")
    for r in fold:
        print("    %-4s R=%-5s b=%-2s  target %.4e = %5.1f sigma;  consistency %+5.2f sigma  %s"
              % (r['cap'], r['R'], r['b'], r['target'], r['detect'], r['consist'],
                 "OK" if abs(r['consist']) < 3 else "DEVIATES"))
    ok5 = [r for r in fold if r['detect'] >= 5]
    con_ok = all(abs(r['consist']) < 3 for r in fold)
    caps = {}
    for r in ok5:
        caps.setdefault((r['cap'], r['R']), set()).add(r['b'])
    two_rung = {k: v for k, v in caps.items() if len(v) >= 2}
    print(f"\n  rows >=5 sigma (folded): {len(ok5)}/{len(fold)}")
    print(f"  (cap,R) with two or more b at >=5 sigma: "
          f"{ {f'{k[0]} R={k[1]}': sorted(v) for k, v in two_rung.items()} }")
    print(f"  all folded rows consistent with the recomputed prediction: {con_ok}")
    print("\n  clipped fraction (Amendment 5 A5.3 -- large clipping makes the valve floor an")
    print("  UPPER bound, hence the target a LOWER bound):")
    for cap in dv:
        print("    %s: %.4f   skew N1 %+.4f  skew N2 %+.4f"
              % (cap, float(np.mean(dv[cap]['clipped'])),
                 float(np.mean([x['15.0']['skew'] for x in dv[cap]['n1']])),
                 float(np.mean([x['15.0']['skew'] for x in dv[cap]['n2']]))))
    json.dump(rows, open(f"{HERE}/sky_final_verdict.json", 'w'), indent=1, default=float)


if __name__ == '__main__':
    main()
