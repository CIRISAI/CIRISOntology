#!/usr/bin/env python3
"""
refuter_analyze.py -- turn the refuter runs into the numbers the verdict is scored on.

Post-unblind, post-hoc.  Pre-registered in REFUTER_PREREG.md.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PRIMARY = [('15.0', '4'), ('15.0', '6'), ('10.0', '4'), ('10.0', '6'), ('10.0', '8')]
EPS = [0.1, 0.25, 0.5, 1.0, 2.0, 4.0]

SIG = {(r['cap'], r['R'], r['b'], r['geom']): r for r in
       json.load(open(f"{HERE}/sky_final_verdict.json"))}
SUITE = {}
for cap in ('NGC', 'SGC'):
    S = json.load(open(f"{HERE}/sky_surrogate_{cap}.json"))['res']
    SUITE[cap] = S


def variant_target(r, name, R, b, g='folded'):
    """target = I(data) - mean over draws of I(null).  Returns (target, sem_of_null_mean)."""
    di = r['data'][R]['b'][b][g]
    if not di.get('occupancy_pass'):
        return None
    if name == 'N2pipe':
        vals = [r['repro_N2'][R]['b'][b][g]['I']]
    else:
        vals = [x[R]['b'][b][g]['I'] for x in r['family'][name]]
    v = np.array(vals)
    sem = v.std(ddof=1) / np.sqrt(v.size) if v.size > 1 else np.nan
    return di['I'] - v.mean(), sem, v.mean(), v.size


def report(cap):
    p = f"{HERE}/refuter_nulls_{cap}.json"
    if not os.path.exists(p):
        print(f"  [{cap}] not available")
        return None
    r = json.load(open(p))
    print("=" * 108)
    print(f"  A9 / A1 / A6  --  cap = {cap}    (post-unblind, post-hoc)")
    print("=" * 108)
    d = r.get('pipeline_null_density')
    if d:
        print(f"\n  A9b MECHANISM.  The pipeline's null modulates by max(1+dpr,0) and never")
        print(f"  renormalises.  Measured mean modulation = {d['mean_mod_cell']:.4f} (per cell) /"
              f" {d['mean_mod_weighted']:.4f} (density-weighted),")
        print(f"  with {100*d['clipped']:.1f}% of cells clipped.  The null is therefore sampled at"
              f" {d['mean_mod_weighted']:.2f}x the data's")
        print(f"  number density and carries only {1/d['mean_mod_weighted']:.2f}x the data's shot"
              f" noise.  Poisson minting is what")
        print("  the valve floor is supposed to measure, so the measured valve floor is too small.")
    mi = r.get('matched_info', {})
    print(f"\n  Refuter's matched modulation: shot power removed, {100*mi.get('clipped',0):.2f}% of"
          f" cells clip (pipeline: {100*r['repro_clipped']:.1f}%),")
    print(f"  cell-level sigma {mi.get('sigma_cf',0):.3f}, mean {mi.get('mean_mod',0):.4f}"
          f" (renormalised to 1 before sampling).")

    print("\n  smoothed-field sigma (the two-point amplitude the null is supposed to match):")
    for R in ('15.0', '10.0'):
        line = (f"    R={R:<5} data {r['data'][R]['sigma']:.4f}   N1 {r['repro_N1'][R]['sigma']:.4f}"
                f"   N2(pipeline) {r['repro_N2'][R]['sigma']:.4f}")
        for k in ('N2m', 'N2mw', 'N2L'):
            if k in r['family']:
                line += f"   {k} {np.mean([x[R]['sigma'] for x in r['family'][k]]):.4f}"
        print(line)

    print("\n  TARGET under each null, folded rows.  'det' uses the campaign's own sigma.")
    print("  %-10s %-5s %-2s %12s %12s %7s %7s %8s"
          % ("null", "R", "b", "I(null)", "target", "ratio", "det", "sem_null"))
    rows = []
    for (R, b) in PRIMARY:
        key = (cap, R, b, 'folded')
        if key not in SIG:
            continue
        sg = SIG[key]['sigma']
        base = None
        for name in ['N2pipe', 'N2m', 'N2mw'] + [f'N2eps{e:g}' for e in EPS] + ['N2L']:
            if name != 'N2pipe' and name not in r['family']:
                continue
            vt = variant_target(r, name, R, b)
            if vt is None:
                continue
            tgt, sem, inull, nd = vt
            if name == 'N2pipe':
                base = tgt
            rows.append(dict(cap=cap, R=R, b=b, null=name, target=tgt, I_null=inull,
                             sigma=sg, detect=tgt / sg, ratio=tgt / base if base else np.nan,
                             sem_null=sem, ndraw=nd))
            print("  %-10s %-5s %-2s %12.5e %12.5e %7.3f %7.1f %8.1e"
                  % (name, R, b, inull, tgt, tgt / base if base else np.nan, tgt / sg,
                     sem if sem == sem else -1))
        # the campaign's own recorded target, for reference
        print("  %-10s %-5s %-2s %12s %12.5e %7.3f %7.1f"
              % ("[recorded]", R, b, "-", SIG[key]['target'],
                 SIG[key]['target'] / base if base else np.nan,
                 SIG[key]['detect']))

    # ---- A1: critical dispersion
    print("\n  A1 -- critical negative-binomial dispersion.  Var = lam*(1+eps).")
    print("  The data's WEIGHTED counts are already super-Poisson at eps_w = kappa - 1 ="
          f" {r['kappa']-1:.4f}, measured")
    print("  from the catalogue, and the null carries none of it.")
    a1 = []
    for (R, b) in PRIMARY:
        key = (cap, R, b, 'folded')
        if key not in SIG:
            continue
        sg = SIG[key]['sigma']
        xs, ys = [0.0], []
        vt = variant_target(r, 'N2m', R, b)
        if vt is None:
            continue
        ys.append(vt[0] / sg)
        for e in EPS:
            n = f'N2eps{e:g}'
            if n not in r['family']:
                continue
            v = variant_target(r, n, R, b)
            if v:
                xs.append(e); ys.append(v[0] / sg)
        xs, ys = np.array(xs), np.array(ys)
        ec = np.nan
        if ys[0] < 5:
            ec = 0.0                      # already below 5 sigma with no extra dispersion
        else:
            for i in range(len(xs) - 1):
                if (ys[i] - 5) * (ys[i + 1] - 5) <= 0 and ys[i] != ys[i + 1]:
                    ec = xs[i] + (5.0 - ys[i]) * (xs[i + 1] - xs[i]) / (ys[i + 1] - ys[i])
                    break
        a1.append(dict(cap=cap, R=R, b=b, eps=list(xs), det=list(ys), eps_crit=float(ec)))
        print("    R=%-5s b=%-2s  det(eps): " % (R, b)
              + "  ".join(f"{x:g}:{y:.1f}" for x, y in zip(xs, ys))
              + f"   =>  eps_crit(5 sigma) = {ec:.2f}")

    # ---- A9a pedestal
    print("\n  A9a -- binmint pedestal (pure function of pair structure) and its deficit:")
    print("  %-10s %-16s %12s %12s %10s %10s"
          % ("null", "row", "ped(data)", "ped(null)", "deficit", "% of tgt"))
    peds = []
    for k in r['data_pedestal']:
        R, b, g = k.split('|')
        for name, src, psrc in (('N2pipe', r['repro_N2'], r['repro_N2_pedestal']),
                                ('N2m', r['family'].get('N2m', [None])[0],
                                 r['family_pedestal'].get('N2m')),
                                ('N2mw', r['family'].get('N2mw', [None])[0],
                                 r['family_pedestal'].get('N2mw'))):
            if psrc is None or k not in psrc:
                continue
            tgt = r['data'][R]['b'][b][g]['I'] - src[R]['b'][b][g]['I']
            dp = r['data_pedestal'][k]['pedestal'] - psrc[k]['pedestal']
            peds.append(dict(cap=cap, null=name, row=k, ped_data=r['data_pedestal'][k]['pedestal'],
                             ped_null=psrc[k]['pedestal'], deficit=dp, frac=dp / tgt))
            print("  %-10s %-16s %12.4e %12.4e %10.3e %9.1f%%"
                  % (name, k, r['data_pedestal'][k]['pedestal'], psrc[k]['pedestal'],
                     dp, 100 * dp / tgt))
    return dict(rows=rows, a1=a1, pedestal=peds,
                density=r.get('pipeline_null_density'), matched=mi, kappa=r['kappa'])


def mock_closure(cap):
    p = f"{HERE}/refuter_mock_{cap}.json"
    if not os.path.exists(p):
        return None
    m = json.load(open(p))['res']
    print("\n" + "=" * 108)
    print(f"  A9 CLOSURE ON MOCKS -- cap = {cap}, n = {len(m)}.  Does the correction move the")
    print("  PREDICTION by the same factor?  If it does, the consistency test is untouched and")
    print("  only the detection-against-zero moves.")
    print("=" * 108)
    print("  %-5s %-2s %14s %14s %14s %8s" % ("R", "b", "tgt(N2pipe)", "tgt(N2m)", "tgt(N2mw)",
                                              "ratio"))
    out = []
    for (R, b) in PRIMARY:
        e = m[0]['mock'][R]['b'][b]['folded']
        if not e.get('occupancy_pass'):
            continue
        t0 = np.mean([x['mock'][R]['b'][b]['folded']['I']
                      - x['n2_pipeline'][R]['b'][b]['folded']['I'] for x in m])
        t1 = np.mean([x['mock'][R]['b'][b]['folded']['I']
                      - x['n2m'][R]['b'][b]['folded']['I'] for x in m])
        t2 = np.mean([x['mock'][R]['b'][b]['folded']['I']
                      - x['n2mw'][R]['b'][b]['folded']['I'] for x in m])
        out.append(dict(cap=cap, R=R, b=b, pipe=t0, n2m=t1, n2mw=t2, ratio_m=t1 / t0,
                        ratio_mw=t2 / t0))
        print("  %-5s %-2s %14.5e %14.5e %14.5e %8.3f" % (R, b, t0, t1, t2, t1 / t0))
    return out


if __name__ == '__main__':
    res = {}
    for cap in ('NGC', 'SGC'):
        res[cap] = report(cap)
        res[f"{cap}_mock"] = mock_closure(cap)
    json.dump(res, open(f"{HERE}/refuter_analyze.json", 'w'), indent=1, default=float)
    print("\n  written refuter_analyze.json")
