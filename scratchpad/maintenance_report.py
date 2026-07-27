"""maintenance_report.py — turn maintenance_sweep_results.json into the tables that go
into MAINTENANCE_SWEEP_RESULTS.md, and adjudicate every pre-registered prediction.

Reads only; runs nothing. Verdicts are computed from the data, not asserted.
"""
import json, sys
import numpy as np

LN2 = float(np.log(2))
R = json.load(open('/home/emoore/CIRISOntology/scratchpad/maintenance_sweep_results.json'))
ROSTER = ['L5', 'L7', 'E8', 'H8', 'H9', 'H10', 'H11', 'L11', 'L12', 'R12']
EPS = [0.005, 0.01, 0.02, 0.05, 0.10, 0.20]
QS = [0.0, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0]


def sec(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


sec("ROSTER as measured")
print(f"{'id':5s}{'k':>3s}{'|S|':>5s}{'d':>3s}{'share_max':>12s}{'/ln2':>8s}  kind")
for t in ROSTER:
    r = R['roster'][t]
    print(f"{t:5s}{r['k']:3d}{r['ns']:5d}{r['d']:3d}{r['share_max']:12.6f}"
          f"{r['share_max']/LN2:8.4f}  {r['kind']}")

# ---------------------------------------------------------------- P2 free decay
sec("P2 — free decay: is share_{t+1}/share_t -> lambda^{2d}?")
print(f"{'id':5s}{'d':>2s} | " + " ".join(f"{e:>17.3f}" for e in EPS))
bad = []
for t in ROSTER:
    row = []
    for e in EPS:
        f = R['free_decay'][f'{t}|{e}']
        row.append(f"{f['asym_ratio']:.5f}/{f['pred_ratio']:.5f}")
        if np.isfinite(f['asym_ratio']):
            rel = abs(f['asym_ratio'] / f['pred_ratio'] - 1)
            if rel > 0.01:
                bad.append((t, e, f['asym_ratio'], f['pred_ratio'], rel))
    print(f"{t:5s}{R['roster'][t]['d']:2d} | " + " ".join(f"{x:>17s}" for x in row))
print(f"\ncells deviating from lambda^(2d) by > 1%: {len(bad)} of {len(ROSTER)*len(EPS)}")
for b in bad[:12]:
    print(f"   {b[0]} eps={b[1]}: measured {b[2]:.6f} vs predicted {b[3]:.6f} "
          f"({b[4]*100:.2f}%)")

sec("P2 — 1/e times, measured vs predicted 1/(2 d ln(1/lambda))")
print(f"{'id':5s}{'d':>2s} | " + " ".join(f"{e:>15.3f}" for e in EPS))
for t in ROSTER:
    row = []
    for e in EPS:
        f = R['free_decay'][f'{t}|{e}']
        row.append(f"{f['tau_e']:.3f}/{f['pred_tau']:.3f}")
    print(f"{t:5s}{R['roster'][t]['d']:2d} | " + " ".join(f"{x:>15s}" for x in row))

# ---------------------------------------------------------------- P8 head-to-head
sec("P7 / P8 — head-to-head at FIXED k (free decay, exact)")
for (a, b, k) in [('H8', 'E8', 8), ('H11', 'L11', 11), ('L12', 'R12', 12)]:
    print(f"\n--- k = {k}: {a} (d={R['roster'][a]['d']}, |S|={R['roster'][a]['ns']}, "
          f"cap {R['roster'][a]['share_max']:.4f})  vs  {b} (d={R['roster'][b]['d']}, "
          f"|S|={R['roster'][b]['ns']}, cap {R['roster'][b]['share_max']:.4f})")
    for e in (0.02, 0.05, 0.10):
        sa = np.array(R['free_decay'][f'{a}|{e}']['share'])
        sb = np.array(R['free_decay'][f'{b}|{e}']['share'])
        n = min(len(sa), len(sb))
        diff = sa[:n] - sb[:n]
        live = (sa[:n] > 1e-14) | (sb[:n] > 1e-14)
        cross = np.flatnonzero(np.sign(diff[live][:-1]) != np.sign(diff[live][1:]))
        print(f"  eps={e}: t=0..8  {a}: " +
              " ".join(f"{x:.4f}" for x in sa[:9]))
        print(f"           t=0..8  {b}: " +
              " ".join(f"{x:.4f}" for x in sb[:9]))
        print(f"           {a} >= {b} at every live t: {len(cross) == 0}"
              f"   (sign changes: {len(cross)}"
              + (f", first at t={cross[0]}" if len(cross) else "") + ")")

# ---------------------------------------------------------------- P3/P4/P5
sec("P3 / P4 — stationary share vs q (exact), and the closed form")
for t in ROSTER:
    print(f"\n{t}  (share_max = {R['roster'][t]['share_max']:.6f}, d={R['roster'][t]['d']})")
    print(f"  {'eps':>6s} | " + " ".join(f"{q:>9g}" for q in QS))
    for e in EPS:
        row = []
        for q in QS:
            c = R['exact_sweep'][f'{t}|{e}|{q}']
            row.append(f"{c['retained']:9.5f}")
        print(f"  {e:6g} | " + " ".join(row))
    # closed-form agreement
    dev = [abs(R['exact_sweep'][f'{t}|{e}|{q}']['share_inf'] -
               R['exact_sweep'][f'{t}|{e}|{q}']['closed_form_share'])
           for e in EPS for q in QS if q > 0]
    print(f"  max |exact stationary - closed form| = {max(dev):.3e}")

sec("P3 — q = 1 (full upkeep): does the share sit exactly at share_max?")
print(f"{'id':5s}{'kind':10s} | " + " ".join(f"eps={e:<8g}" for e in EPS))
p3 = {}
for t in ROSTER:
    row, worst = [], 0.0
    for e in EPS:
        c = R['exact_sweep'][f'{t}|{e}|1.0']
        gap = c['share_max'] - c['share_inf']
        worst = max(worst, gap)
        row.append(f"{gap:12.3e}")
    p3[t] = worst
    print(f"{t:5s}{R['roster'][t]['kind']:10s} | " + " ".join(row))
print("\nP3 verdict per substrate (gap from share_max at q=1):")
for t in ROSTER:
    v = 'HOLDS (exact)' if p3[t] < 1e-12 else f'FAILS by {p3[t]:.3e} nats'
    print(f"   {t:5s} {R['roster'][t]['kind']:9s} {v}")

sec("P5 — does retention collapse onto rho = q/(2 eps d)?  (no threshold at q = eps)")
print(f"{'rho':>10s} {'retained':>10s} {'(rho/(1+rho))^2':>18s}   n cells")
rows = []
for t in ROSTER:
    d = R['roster'][t]['d']
    for e in EPS:
        for q in QS:
            if q <= 0:
                continue
            c = R['exact_sweep'][f'{t}|{e}|{q}']
            rows.append((q / (2 * e * d), c['retained'], t, e, q))
rows.sort()
bins = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30, 100, 1e9]
lo = 0.0
for hi in bins:
    sel = [r for r in rows if lo <= r[0] < hi]
    if sel:
        rho = np.mean([r[0] for r in sel])
        ret = np.mean([r[1] for r in sel])
        sd = np.std([r[1] for r in sel])
        print(f"{rho:10.4f} {ret:8.4f}+-{sd:.4f} {(rho/(1+rho))**2:18.4f}   {len(sel)}")
    lo = hi
print("\n(spread WITHIN a rho bin is the test: small spread => collapse holds)")

# ---------------------------------------------------------------- P6 cost
sec("P6 — the maintenance cost: cost_erase vs rent, and cost_erase = q*(share_max - share_pre)")
print(f"{'id':5s}{'eps':>7s}{'q':>7s}{'retained':>10s}{'cost_erase':>12s}"
      f"{'cost_flips':>12s}{'nats/slot/step':>15s}")
for t in ['L7', 'E8', 'H8', 'L12']:
    for e in (0.02, 0.05):
        for q in (0.003, 0.03, 0.3, 1.0):
            c = R['exact_sweep'][f'{t}|{e}|{q}']
            print(f"{t:5s}{e:7g}{q:7g}{c['retained']:10.5f}{c['cost_erase']:12.6f}"
                  f"{c['cost_flips']:12.6f}{c['cost_erase']/c['k']:15.6f}")

sec("M4 — the rent controller: the q that buys standing still, and its bill")
print(f"{'id':5s}{'eps':>7s}{'held@':>8s}{'share':>10s}{'q*':>10s}{'cost_erase':>12s}"
      f"{'rent':>10s}{'cost/rent':>11s}{'bits/slot/step':>15s}")
for key, v in R['rent'].items():
    if not v['held']:
        print(f"{v['tag']:5s}{v['eps']:7g}  NOT HELD")
        continue
    fa = v['share_held'] / v['share_max']
    ratio = v['cost_erase'] / v['rent_nats'] if v['rent_nats'] > 1e-12 else float('nan')
    print(f"{v['tag']:5s}{v['eps']:7g}{fa:8.3f}{v['share_held']:10.5f}{v['q_star']:10.5f}"
          f"{v['cost_erase']:12.6f}{v['rent_nats']:10.6f}{ratio:11.3f}"
          f"{v['cost_erase']/np.log(2)/v['k']:15.6f}")

# ---------------------------------------------------------------- equivariance
sec("TASK 2 / P3 — decoder equivariance: is dec#(uniform(S) (x) noise) uniform on S?")
print(f"{'id':5s}{'kind':10s}{'|S|':>5s} | " +
      " ".join(f"eps={e:<10g}" for e in [0.01, 0.05, 0.10, 0.20]) + "   deep(t=20)")
for t in ROSTER:
    e = R['equivariance'][t]
    row = [f"{e['rows'][str(x)]['max_dev'] if str(x) in e['rows'] else e['rows'][x]['max_dev']:14.3e}"
           for x in [0.01, 0.05, 0.10, 0.20]]
    print(f"{t:5s}{e['kind']:10s}{e['ns']:5d} | " + " ".join(row) +
          f"   {e['rows']['deep']['max_dev']:.3e}")

# ---------------------------------------------------------------- arms
sec("M5 — drift arms")
for t in ROSTER:
    a = R['arms'][f'AUT|{t}']
    m = a['max_share_change']
    print(f"  AUT      {t:5s}: {a['n_found']:3d} automorphisms, max |Dshare| = "
          + ("none found" if m is None else f"{m:.3e}"))
for t in ROSTER:
    a = R['arms'][f'SCRAMBLE|{t}']
    print(f"  SCRAMBLE {t:5s}: share {a['share_mean']:.4f} +- {a['share_sd']:.4f} "
          f"= {a['frac']:.2%} of max;  H fixed at ln|S|: {a['H_exact']}")
for t in ['L7', 'E8', 'H8', 'L12']:
    a = R['arms'][f'PERM|{t}']
    m = R['arms'][f'MISMATCH|{t}']
    print(f"  PERM     {t:5s}: max |Dshare| under pure drift = {a['max_change']:.3e}")
    print(f"  MISMATCH {t:5s}: full upkeep to the WRONG S -> {m['q1'][-1]:.5f} ; "
          f"no upkeep -> {m['q0'][-1]:.5f} ; max {m['share_max']:.5f}")

# ---------------------------------------------------------------- MC arm
sec("M6 — Monte-Carlo arm with the sibling-matched floors (5 seeds)")
print(f"{'id':5s}{'eps':>6s}{'q':>6s}{'t':>4s}{'excess':>12s}{'+-':>10s}"
      f"{'exact':>12s}{'z':>12s}{'null':>11s}{'shuffle':>11s} cap")
seen = set()
for key, v in R['mc'].items():
    if v['t'] not in (0, 2, 8, 32, 64):
        continue
    print(f"{v['tag']:5s}{v['eps']:6g}{v['q']:6g}{v['t']:4d}{v['excess']:12.6f}"
          f"{v['excess_sem']:10.2e}{v['exact_share']:12.6f}{v['z']:12.1f}"
          f"{v['null_mean']:11.2e}{v['shuffle_mean']:11.2e} {v['cap_ok']}")

sec("M6 — agreement: |MC excess - exact share|, pooled")
devs = [(abs(v['excess'] - v['exact_share']), v['excess_sem'], v['tag'], v['t'], v['q'])
        for v in R['mc'].values()]
d = np.array([x[0] for x in devs])
print(f"  n = {len(devs)}   median |dev| = {np.median(d):.3e}   max = {d.max():.3e}")
worst = sorted(devs, reverse=True)[:6]
for w in worst:
    print(f"    {w[2]} t={w[3]} q={w[4]}: dev {w[0]:.3e}  (sem {w[1]:.1e})")

sec("PAIR-UNIFORMITY (P1) across the whole exact sweep")
mx = max(v['max_pair_dev'] for v in R['exact_sweep'].values())
bytag = {}
for v in R['exact_sweep'].values():
    bytag[v['tag']] = max(bytag.get(v['tag'], 0), v['max_pair_dev'])
print(f"  max |pair marginal - 1/4| over ALL {len(R['exact_sweep'])} exact cells: {mx:.3e}")
for t in ROSTER:
    print(f"    {t:5s} {bytag[t]:.3e}"
          + ("   <- IPF branch used" if any(
              R['exact_sweep'][f'{t}|{e}|{q}']['used_ipf'] for e in EPS for q in QS)
             else ""))
