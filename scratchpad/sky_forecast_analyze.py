#!/usr/bin/env python3
"""
sky_forecast_analyze.py -- turn sky_forecast.py's raw JSON into the forecast tables.

Reads sky_forecast_{gate,sweep,sectors,growth,poisson}.json.  Writes the numbers that
SKY_FORECAST_RESULTS.md quotes.  No new physics here, only bookkeeping.

Significances, both reported because they answer different questions:
  z_p  PAIRED    mean(gap)/SEM(gap) over realisations, gravity and floor on the SAME white
                 noise.  "Is the gap real, given the same phases."  Model comparison.
  z_s  SURVEY    mean(gap)/sigma_V, sigma_V = std(E_gravity across realisations) scaled to
                 the survey volume by sqrt(V_box/V).  THIS IS THE FORECAST NUMBER: a real
                 survey has one universe and a forward-modelled floor.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
V_DESI = 20.0            # (Gpc/h)^3 effective
GEOMS = ['equilateral', 'folded', 'orthogonal', 'squeezed']


def jload(name):
    p = os.path.join(HERE, f'sky_forecast_{name}.json')
    return json.load(open(p)) if os.path.exists(p) else None


def collect(block):
    """-> arms[(R, cfg, arm)] = array over realisations of E; same for I and sem."""
    E, I, S, meta = {}, {}, {}, {}
    for run in block['runs']:
        for R, rec in run['R'].items():
            R = float(R)
            meta[R] = dict(stride=rec['stride'], sigma_R_lin=rec['sigma_R_lin'])
            for arm, a in rec['arms'].items():
                meta[R].setdefault('sigma', {})[arm] = rec.get('sigma_%s' % arm)
                meta[R].setdefault('skew', {})[arm] = rec.get('skew_%s' % arm)
                for cfg, v in a['cfg'].items():
                    E.setdefault((R, cfg, arm), []).append(v['E'])
                    I.setdefault((R, cfg, arm), []).append(v['I'])
                    S.setdefault((R, cfg, arm), []).append(v['sem_oct'])
                    meta.setdefault('sides', {})[(R, cfg)] = v['sides']
    return ({k: np.array(v) for k, v in E.items()},
            {k: np.array(v) for k, v in I.items()},
            {k: np.array(v) for k, v in S.items()}, meta)


def _pair(a, b, V_box):
    d = a - b
    n = len(d)
    sem = d.std(ddof=1) / np.sqrt(n)
    sig = a.std(ddof=1)
    return dict(d=d.mean(), sem=sem,
                z_p=float(d.mean() / sem) if sem > 0 else np.nan,
                z_s=float(abs(d.mean()) / (sig * np.sqrt(V_box / V_DESI)))
                if sig > 0 else np.nan)


def stats(E, I, S, R, cfg, V_box, floor='F2'):
    """Three separate questions, kept separate:
      A   = E_2LPT - E_F0    gravity's own excess over an EXACT-ZERO Gaussian  (prereg F1)
      M   = E_floor - E_F0   what the pointwise mock's FILTER manufactures from nothing
      GAP = E_2LPT - E_floor the deliverable                                   (prereg F5)
    A - M = GAP identically, so the decomposition is exact and shows which side dominates."""
    g = E[(R, cfg, '2LPT')]
    z = E[(R, cfg, 'F0')]
    p = E[(R, cfg, floor)]
    out = dict(n=len(g), E_grav=g.mean(), E_floor=p.mean(), E_F0=z.mean(),
               sig_box=g.std(ddof=1), sig_F0=z.std(ddof=1),
               sem_oct=S[(R, cfg, '2LPT')].mean(),
               I_grav=I[(R, cfg, '2LPT')].mean(), I_floor=I[(R, cfg, floor)].mean(),
               I_F0=I[(R, cfg, 'F0')].mean(),
               E_F1=E[(R, cfg, 'F1')].mean(), E_F2=E[(R, cfg, 'F2')].mean())
    out['A'] = _pair(g, z, V_box)
    out['M'] = _pair(p, z, V_box)
    out['GAP'] = _pair(g, p, V_box)
    out['GAP1'] = _pair(g, E[(R, cfg, 'F1')], V_box)
    if (R, cfg, 'SPT2') in E:
        s = E[(R, cfg, 'SPT2')]
        out['E_SPT2'] = s.mean()
        out['GAP_SPT2'] = _pair(s, p, V_box)
        out['A_SPT2'] = _pair(s, z, V_box)
    # legacy flat keys used by scaling()
    out['gap'] = out['GAP']['d']
    out['sem_gap'] = out['GAP']['sem']
    out['z_p'] = out['GAP']['z_p']
    out['z_s'] = out['GAP']['z_s']
    return out


def report_sweep(name, block, floor='F2'):
    E, I, S, meta = collect(block)
    V_box = block['V']
    Rs = sorted({k[0] for k in E})
    cfgs = sorted({k[1] for k in E})
    print("\n" + "=" * 108)
    print(f"SWEEP {name}  N={block['N']} L={block['L']} V_box={V_box:.3f} (Gpc/h)^3  "
          f"n_real={block['n_real']}  floor={floor}  [V_DESI={V_DESI} (Gpc/h)^3]")
    print("=" * 108)
    print("  A = gravity - Gaussian(exact zero) | M = what the floor's FILTER manufactures "
          "| GAP = A - M = gravity - floor")
    print(f"{'R':>5} {'cfg':>17} {'sides Mpc/h':>21} | {'A':>10} {'z_p':>6} | "
          f"{'M':>10} {'z_p':>7} | {'GAP':>10} {'z_p':>7} {'z_s@DESI':>9} | "
          f"{'GAP(SPT2)':>10} {'z_p':>6} | {'sig_box':>9}")
    out = {}
    for R in Rs:
        for cfg in cfgs:
            if (R, cfg, '2LPT') not in E:
                continue
            st = stats(E, I, S, R, cfg, V_box, floor)
            out[(R, cfg)] = st
            sd = meta['sides'][(R, cfg)]
            gs = st.get('GAP_SPT2', dict(d=np.nan, z_p=np.nan))
            print(f"{R:5.0f} {cfg:>17} {str(tuple(sd)):>21} | {st['A']['d']:10.3e} "
                  f"{st['A']['z_p']:6.2f} | {st['M']['d']:10.3e} {st['M']['z_p']:7.2f} | "
                  f"{st['GAP']['d']:10.3e} {st['GAP']['z_p']:7.2f} {st['GAP']['z_s']:9.2f} | "
                  f"{gs['d']:10.3e} {gs['z_p']:6.2f} | {st['sig_box']:9.2e}")
    # sigma_R and skewness of the arms actually measured
    print("\n  measured sigma_R and one-point skewness of the SMOOTHED fields:")
    print(f"  {'R':>6} {'sig_lin(th)':>11} {'sig_2LPT':>9} {'sig_F2':>9} "
          f"{'skew_2LPT':>10} {'skew_F2':>9} {'skew_F1':>9} {'skew_F0':>9} {'stride':>7}")
    for R in Rs:
        m = meta[R]
        print(f"  {R:6.0f} {m['sigma_R_lin']:11.4f} {m['sigma'].get('2LPT', 0):9.4f} "
              f"{m['sigma'].get('F2', 0):9.4f} {m['skew'].get('2LPT', 0):10.4f} "
              f"{m['skew'].get('F2', 0):9.4f} {m['skew'].get('F1', 0):9.4f} "
              f"{m['skew'].get('F0', 0):9.4f} {m['stride']:7d}")
    return out, meta, E, I, S


def scaling(out, meta, key='E_grav', label='E_2LPT'):
    """F2 -- d log |X| / d log sigma_R, using the MEASURED sigma of the 2LPT field."""
    print(f"\n  amplitude scaling  d log |{label}| / d log sigma_R  "
          f"(prereg F2: 1.0 +- 0.3 for E, 2.0 +- 0.5 for I):")
    cfgs = sorted({k[1] for k in out})
    for cfg in cfgs:
        pts = [(meta[R]['sigma'].get('2LPT'), abs(out[(R, cfg)][key]))
               for R in sorted({k[0] for k in out}) if (R, cfg) in out]
        pts = [(a, b) for a, b in pts if a and b > 0]
        if len(pts) < 3:
            continue
        x = np.log([p[0] for p in pts]); y = np.log([p[1] for p in pts])
        print(f"    {cfg:>18}: {np.polyfit(x, y, 1)[0]:+.3f}   "
              f"(sigma {min(p[0] for p in pts):.3f}-{max(p[0] for p in pts):.3f})")


def report_sectors(block):
    E, I, S, meta = collect(block)
    Rs = sorted({k[0] for k in E})
    arms = sorted({k[2] for k in E})
    print("\n" + "=" * 108)
    print("SECTORS -- which part of the F2 kernel carries the excess "
          f"(N={block['N']} L={block['L']} n_real={block['n_real']})")
    print("=" * 108)
    print("  LOCAL = delta1 + (17/21)delta1^2 is a POINTWISE map of delta1, monotone where")
    print("  delta1 > -21/34; prereg F4 stakes that it reads ~0 up to that tail.")
    mv = np.mean([r['mono_viol'] for r in block['runs']])
    print(f"  non-monotone tail fraction of delta1 (delta1 < -0.618): {mv:.4f}\n")
    for R in Rs:
        for cfg in sorted({k[1] for k in E}):
            if (R, cfg, 'SPT2') not in E:
                continue
            print(f"  R={R:.0f} {cfg}  sides={meta['sides'][(R,cfg)]}")
            base = E[(R, cfg, 'F2')]
            for a in arms:
                if (R, cfg, a) not in E:
                    continue
                v = E[(R, cfg, a)]
                d = v - base
                print(f"      {a:>12}: E = {v.mean():10.3e} +- {v.std(ddof=1)/np.sqrt(len(v)):8.2e}"
                      f"   E - E_F2 = {d.mean():10.3e}  z_p = {d.mean()/max(d.std(ddof=1)/np.sqrt(len(d)),1e-30):6.2f}")
            print()


def report_poisson(block):
    print("\n" + "=" * 108)
    print("POISSON GATE -- does shot noise manufacture share on an EXACT-ZERO field?")
    print("=" * 108)
    acc = {}
    for run in block['runs']:
        for k, v in run.items():
            nm, nb, R, gname = k.split('|')
            for (I, E, sem, tied) in v:
                acc.setdefault((nm, float(nb), float(R), gname), []).append((I, E, sem, tied))
    for nm in ('F0', '2LPT'):
        print(f"\n  base field = {nm}"
              + ("   (true whole-only share EXACTLY zero by "
                 "share_eq_zero_of_signSymmetric)" if nm == 'F0' else "   (gravity)"))
        for R in sorted({k[2] for k in acc}):
            print(f"    R = {R:.0f} Mpc/h")
            print(f"      {'nbar':>10} {'geom':>13} {'E':>11} {'sem':>10} {'z':>7} "
                  f"{'I(nats)':>11} {'tied':>9}")
            for nb in sorted({k[1] for k in acc}):
                for gname in GEOMS:
                    key = (nm, nb, R, gname)
                    if key not in acc:
                        continue
                    a = np.array(acc[key])
                    E = a[:, 1]; sem = E.std(ddof=1) / np.sqrt(len(E))
                    lab = 'inf' if not np.isfinite(nb) else f"{nb:.0e}"
                    print(f"      {lab:>10} {gname:>13} {E.mean():11.3e} {sem:10.2e} "
                          f"{E.mean()/max(sem,1e-30):7.2f} {a[:,0].mean():11.3e} "
                          f"{a[:,3].mean():9.2e}")


def main():
    g = jload('gate')
    if g:
        print("GATE:", "ALL PASS" if g['gate'].get('ALL_PASS') else "FAILURE")
    sw = jload('sweep')
    allout = {}
    if sw:
        for name in ('small', 'large'):
            if name in sw:
                for fl in ('F2', 'F1'):
                    o, m, E, I, S = report_sweep(f"{name} [floor {fl}]", sw[name], floor=fl)
                    if fl == 'F2':
                        allout[name] = (o, m)
                        scaling(o, m, 'E_grav', 'E_2LPT')
                        scaling(o, m, 'I_grav', 'I_2LPT')
                        scaling(o, m, 'gap', 'GAP')
    gr = jload('growth')
    if gr:
        blk = gr if 'runs' in gr else gr.get('growth')
        if blk:
            report_sweep("growth D=0.6", blk, floor='F2')
    se = jload('sectors')
    if se:
        report_sectors(se)
    po = jload('poisson')
    if po:
        report_poisson(po)


if __name__ == '__main__':
    main()
