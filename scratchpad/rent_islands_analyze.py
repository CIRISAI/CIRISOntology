"""rent_islands_analyze.py — adjudicate the pre-registered predictions and draw the figure.

Reads rent_islands_results.json. Every verdict rule is the one written in
RENT_ISLANDS_PREREG.md (19f80c6) before the run. No rule is chosen here.
"""
import json
import numpy as np

RES = '/home/emoore/CIRISOntology/scratchpad/rent_islands_results.json'
FIG = '/home/emoore/CIRISOntology/scratchpad/rent_islands_figure.png'

STEPS_A = [8, 12, 16, 20, 24]       # ARM A ceiling steps: k = 0 (mod 4)
STEPS_B = [8, 16]                   # ARM B ceiling steps: k = 2^j
ISLANDS = [7, 11, 15, 19, 23]       # k = 3 (mod 4)
OUT_OF_SAMPLE = [16, 20, 24]        # k=8,12 are disclosed in-sample (prereg §1.3)
CONDS = [(0.01, '0.1'), (0.01, '0.5'), (0.05, '0.1'), (0.05, '0.5')]


def load():
    d = json.load(open(RES))
    rows = [r for r in d['rows'] if not r.get('dropped')]
    return d, rows


def pick(rows, arm, k, eps, label, mode='frac'):
    for r in rows:
        if (r['arm'] == arm and r['k'] == k and r['eps'] == eps
                and r['target_label'] == label and r['mode'] == mode):
            return r
    return None


def bar(x, lo, hi, w=46):
    """A crude monotone bar so the sawtooth is visible in plain text too."""
    f = (x - lo) / (hi - lo) if hi > lo else 0.0
    return '#' * max(1, int(round(f * w)))


def main():
    d, rows = load()
    dropped = [r for r in d['rows'] if r.get('dropped')]
    print("=" * 96)
    print("RENT ISLANDS — adjudication against RENT_ISLANDS_PREREG.md (19f80c6)")
    print("=" * 96)
    print(f"rows measured: {len(d['rows'])}   used: {len(rows)}   dropped: {len(dropped)}")
    for r in dropped:
        print(f"    DROPPED {r['tag']} eps={r['eps']} {r['target_label']}: "
              f"{r['drop_reason']}")

    # ---- hygiene, reported before any verdict --------------------------------
    resid = [r['target_resid_rel'] for r in rows]
    qs = [r['q_star'] for r in rows]
    print(f"\nHYGIENE: max relative target residual = {max(resid):.2e} (drop bar 1e-6); "
          f"q* range [{min(qs):.3e}, {max(qs):.3e}] (rails 1e-9 / 1-1e-9); "
          f"max |mass-1| = {max(r['mass_dev'] for r in rows):.2e}; "
          f"most negative probability = {min(r['neg_mass'] for r in rows):.2e}")

    # =========================================================================
    # THE G7 RESULT — which substrates are lossy, and how much it moves anything
    # =========================================================================
    print("\n" + "=" * 96)
    print("GATE G7 FIRED — pre-registered as a measurement with both outcomes meaningful.")
    print("Which substrates have a NON-EQUIVARIANT decoder (upkeep that cannot restore")
    print("the design state), and does it move the numbers the island test rests on?")
    print("=" * 96)
    print(f"{'tag':>5s} {'k':>3s} {'|S|':>5s} {'construction':>18s} {'profile dev':>12s} "
          f"{'eps-scan dev':>13s} {'ceiling/max':>12s} {'leak corr':>11s} {'resid':>10s}")
    for k in sorted({r['k'] for r in rows if r['arm'] == 'A'}):
        r = pick(rows, 'A', k, 0.05, '0.5')
        if r is None:
            continue
        src = r['name'].split('[')[-1].rstrip(']')
        print(f"{r['tag']:>5s} {k:3d} {r['ns']:5d} {src:>18s} {r['profile_dev']:12.3e} "
              f"{r['equiv_dev']:13.3e} {r.get('ceiling_frac', 1.0):12.9f} "
              f"{r['leak_correction_rel']:11.3e} {r['leak_residual_rel']:10.2e}")
    lossy = sorted({r['k'] for r in rows if r['arm'] == 'A' and not r['equivariant']})
    equiv = sorted({r['k'] for r in rows if r['arm'] == 'A' and r['equivariant']})
    print(f"\n  LOSSY (upkeep does not restore the design state): k = {lossy}")
    print(f"  EQUIVARIANT                                      : k = {equiv}")
    print("  This refines the parent's expectation (MAINTENANCE_SWEEP_PREREG §1.1), which")
    print("  predicted equivariance would hold at k=11 and lapse at k=8,9,10. Measured:")
    print("  it lapses at k=8 ONLY, holds at 9,10,11 — and the property does not follow")
    print("  full-width use of the array: k=19 uses all 19 columns of H20 and is lossy,")
    print("  while k=11 (H12) and k=23 (H24) at full width are exactly equivariant.")

    print("\n  CONFOUND AUDIT — is any predicted uptick explained by lossiness instead?")
    for k0 in STEPS_A:
        a, b = pick(rows, 'A', k0, 0.05, '0.5'), pick(rows, 'A', k0 - 1, 0.05, '0.5')
        if a is None or b is None:
            continue
        same = a['equivariant'] == b['equivariant']
        tooth = (a['rent_per_nat'] - b['rent_per_nat']) / b['rent_per_nat']
        biggest = max(a['leak_correction_rel'], b['leak_correction_rel'])
        # the second lossy channel: upkeep deposits less than uniform, inflating cost_erase
        hcd = max(a['Hc_deficit'] / (a['cost_erase'] / a['q_star']),
                  b['Hc_deficit'] / (b['cost_erase'] / b['q_star']))
        print(f"    k={k0-1}->{k0}: equivariance matched: {str(same):5s}  tooth "
              f"{100*tooth:+.4f}%   leak correction <= {100*biggest:.5f}% "
              f"({abs(biggest/tooth) if tooth else 0:6.2%} of tooth)   upkeep-deposit "
              f"deficit <= {100*hcd:.5f}% ({abs(hcd/tooth) if tooth else 0:6.2%} of tooth)")

    # =========================================================================
    # THE TABLE
    # =========================================================================
    print("\n" + "=" * 96)
    print("ARM A — rent/nat (cost_erase per nat held) at the exact target, by k")
    print("=" * 96)
    ks = sorted({r['k'] for r in rows if r['arm'] == 'A'})
    hdr = "  k  N0 density |"
    for eps, lab in CONDS:
        hdr += f"  e={eps} f={lab} |"
    print(hdr + "   flips/nat (e=.05,f=.5)")
    for k in ks:
        rr = [pick(rows, 'A', k, e, l) for e, l in CONDS]
        if any(x is None for x in rr):
            continue
        mark = ' *' if k % 4 == 3 else (' ^' if k % 4 == 0 else '  ')
        line = f"{k:3d}{mark}{rr[0]['ns']:3d} {rr[0]['density']:.4f} |"
        for x in rr:
            line += f"    {x['rent_per_nat']:9.6f} |"
        line += f"  {rr[3]['flips_per_nat']:9.5f}"
        print(line)
    print("  * = k = 3 (mod 4), Hadamard-attained (predicted island)")
    print("  ^ = k = 0 (mod 4), the ceiling steps down (predicted uptick)")

    # =========================================================================
    # P-ISLAND
    # =========================================================================
    print("\n" + "=" * 96)
    print("P-ISLAND — 20 pre-registered binary events: rent/nat(k0) > rent/nat(k0-1)")
    print("=" * 96)
    events, per_cond = [], {}
    for eps, lab in CONDS:
        row = []
        for k0 in STEPS_A:
            a = pick(rows, 'A', k0, eps, lab)
            b = pick(rows, 'A', k0 - 1, eps, lab)
            if a is None or b is None:
                row.append(None)
                continue
            up = a['rent_per_nat'] > b['rent_per_nat']
            rel = (a['rent_per_nat'] - b['rent_per_nat']) / b['rent_per_nat']
            row.append((k0, up, rel))
            events.append((eps, lab, k0, up, rel))
        per_cond[(eps, lab)] = row
    print(f"{'condition':>16s} | " + " | ".join(f"k={k:2d}" for k in STEPS_A))
    for (eps, lab), row in per_cond.items():
        cells = []
        for e in row:
            cells.append('  -- ' if e is None else (' UP  ' if e[1] else 'down '))
        print(f"  eps={eps} frac={lab} | " + " | ".join(cells))
    print(f"{'':>16s} | " + " | ".join(
        f"{'':5s}" for _ in STEPS_A))
    print("\n  relative size of each step (rent/nat(k0)/rent/nat(k0-1) - 1), vs predicted")
    pred = {8: 0.034, 12: 0.011, 16: 0.0047, 20: 0.0023, 24: 0.0012}
    print(f"{'condition':>16s} | " + " | ".join(f"  k={k:2d}   " for k in STEPS_A))
    for (eps, lab), row in per_cond.items():
        cells = ['   --    ' if e is None else f"{100*e[2]:+8.4f}%" for e in row]
        print(f"  eps={eps} frac={lab} | " + " | ".join(cells))
    print(f"{'density drop':>16s} | " + " | ".join(
        f"{100*pred[k]:+8.4f}%" for k in STEPS_A))

    n_up = sum(1 for e in events if e[3])
    n_tot = len(events)
    oos = [e for e in events if e[2] in OUT_OF_SAMPLE]
    oos_1620 = [e for e in events if e[2] in (16, 20)]
    n_oos_up = sum(1 for e in oos_1620 if e[3])
    print(f"\n  TOTAL UPTICKS: {n_up} / {n_tot}")
    print(f"  out-of-sample (k=16,20): {n_oos_up} / {len(oos_1620)}   "
          f"(k=24: {sum(1 for e in events if e[2]==24 and e[3])} / "
          f"{sum(1 for e in events if e[2]==24)})")
    if n_up >= 18 and n_oos_up >= 5:
        verdict = "P-ISLAND CONFIRMED"
    elif n_up <= 2:
        verdict = "P-ISLAND DEAD — rent/nat is monotone in k; the magic structure is irrelevant"
    else:
        verdict = "P-ISLAND MIXED"
    print(f"  >>> {verdict}")

    # island k's as local minima of the whole curve
    print("\n  local-minimum check on ARM A: is each k = 3 (mod 4) below BOTH neighbours?")
    for eps, lab in CONDS:
        got = []
        for k in ISLANDS:
            a, b, c = (pick(rows, 'A', k - 1, eps, lab), pick(rows, 'A', k, eps, lab),
                       pick(rows, 'A', k + 1, eps, lab))
            if None in (a, b, c):
                got.append(f"k={k}:--")
            else:
                ok = b['rent_per_nat'] < a['rent_per_nat'] and \
                     b['rent_per_nat'] < c['rent_per_nat']
                got.append(f"k={k}:{'MIN' if ok else 'no '}")
        print(f"    eps={eps} frac={lab}: " + "  ".join(got))

    # =========================================================================
    # P-DENSITY
    # =========================================================================
    print("\n" + "=" * 96)
    print("P-DENSITY — does the density ceiling MEDIATE the k-dependence?")
    print("=" * 96)
    for eps, lab in CONDS:
        pts = sorted([(pick(rows, 'A', k, eps, lab)['density'],
                       pick(rows, 'A', k, eps, lab)['rent_per_nat'], k)
                      for k in ks if pick(rows, 'A', k, eps, lab)])
        y = [p[1] for p in pts]
        mono = all(y[i] > y[i + 1] for i in range(len(y) - 1))
        inv = [(pts[i][2], pts[i + 1][2]) for i in range(len(y) - 1)
               if y[i] <= y[i + 1]]
        print(f"  eps={eps} frac={lab}: rent/nat strictly decreasing in density: {mono}"
              + ("" if mono else f"   inversions at k pairs {inv}"))
    # amplitude decay
    print("\n  tooth amplitude vs the predicted 1/k^2 decay of the density drop:")
    for (eps, lab), row in per_cond.items():
        rr = [e for e in row if e is not None]
        if len(rr) >= 3:
            ratios = [f"{100*e[2]/(100*pred[e[0]]):.2f}" for e in rr]
            print(f"    eps={eps} frac={lab}: observed/predicted per tooth "
                  f"(k={[e[0] for e in rr]}): {ratios}")

    # =========================================================================
    # P-DISSOCIATION
    # =========================================================================
    print("\n" + "=" * 96)
    print("P-DISSOCIATION — each arm should tick at its OWN step points, not the other's")
    print("=" * 96)
    print("  ARM A steps at k = 8,12,16,20,24;  ARM B steps at k = 8,16 only")
    for arm, steps, nonsteps in (('A', STEPS_A, []), ('B', STEPS_B, [12, 20, 24])):
        print(f"\n  ARM {arm}: rent/nat(k) vs rent/nat(k-1)")
        for eps, lab in CONDS:
            cells = []
            for k0 in sorted(set(STEPS_A + STEPS_B)):
                a, b = pick(rows, arm, k0, eps, lab), pick(rows, arm, k0 - 1, eps, lab)
                if a is None or b is None:
                    cells.append(f"k{k0}:--")
                    continue
                up = a['rent_per_nat'] > b['rent_per_nat']
                tag = 'UP ' if up else 'dn '
                own = '*' if k0 in steps else ' '
                cells.append(f"k{k0}{own}:{tag}")
            print(f"    eps={eps} frac={lab}: " + " ".join(cells))
    print("\n  (* marks that arm's OWN ceiling step. P-DISSOCIATION wants UP at * and")
    print("   down elsewhere. ARM B at k=12 and k=20 is the decisive cell.)")

    print("\n  ARM B' (d = 3 constrained) vs ARM B (d = 4) at k = 8 and 16 — the d confound:")
    for k in (8, 16):
        for eps, lab in CONDS:
            b = pick(rows, 'B', k, eps, lab)
            p = pick(rows, "B'", k, eps, lab)
            bm1 = pick(rows, 'B', k - 1, eps, lab)
            if None in (b, p, bm1):
                continue
            print(f"    k={k} eps={eps} f={lab}: B(d={b['d']}) {b['rent_per_nat']:.6f}  "
                  f"B'(d={p['d']}) {p['rent_per_nat']:.6f}  "
                  f"B at k-1 {bm1['rent_per_nat']:.6f}  -> uptick survives d-matching: "
                  f"{p['rent_per_nat'] > bm1['rent_per_nat']}")

    # =========================================================================
    # P-PERFECT
    # =========================================================================
    print("\n" + "=" * 96)
    print("P-PERFECT — are the perfect codes the mechanism? (predicted: NO on nats,")
    print("            YES on flips)")
    print("=" * 96)
    for k in (7, 15, 23):
        for eps, lab in CONDS:
            a, c = pick(rows, 'A', k, eps, lab), pick(rows, 'C', k, eps, lab)
            if a is None or c is None:
                continue
            print(f"  k={k:2d} eps={eps} f={lab}: ARM A |S|={a['ns']:5d} dens={a['density']:.4f}"
                  f" rent/nat={a['rent_per_nat']:.6f} flips/nat={a['flips_per_nat']:.5f}"
                  f"   | ARM C |S|={c['ns']:5d} dens={c['density']:.4f} "
                  f"rent/nat={c['rent_per_nat']:.6f} flips/nat={c['flips_per_nat']:.5f}"
                  f"   | C cheaper on nats: {c['rent_per_nat'] < a['rent_per_nat']}, "
                  f"on flips: {c['flips_per_nat'] < a['flips_per_nat']}")

    # =========================================================================
    # P-PLATEAU
    # =========================================================================
    print("\n" + "=" * 96)
    print("P-PLATEAU — power decline vs decline-to-floor vs linear, IN RANGE ONLY")
    print("=" * 96)
    from scipy.optimize import curve_fit
    f_pow = lambda k, a, b: a * k ** (-b)
    f_flo = lambda k, a, b, c: c + a * np.exp(-b * k)
    f_lin = lambda k, a, b: a + b * k
    for eps, lab in CONDS:
        kk = np.array([k for k in ks if pick(rows, 'A', k, eps, lab)], float)
        yy = np.array([pick(rows, 'A', int(k), eps, lab)['rent_per_nat'] for k in kk])
        out = {}
        for nm, f, p0 in (('power', f_pow, [1.0, 1.0]),
                          ('floor', f_flo, [1.0, 0.1, 0.1]),
                          ('linear', f_lin, [1.0, -0.01])):
            try:
                p, _ = curve_fit(f, kk, yy, p0=p0, maxfev=200000)
                r = yy - f(kk, *p)
                rss = float(np.sum(r ** 2))
                n, kp = len(yy), len(p)
                aic = n * np.log(rss / n) + 2 * kp
                out[nm] = (aic, p, rss)
            except Exception as e:
                out[nm] = (np.inf, None, np.nan)
        best = min(out, key=lambda m: out[m][0])
        print(f"  eps={eps} frac={lab}: best by AIC = {best.upper()}")
        for nm in ('power', 'floor', 'linear'):
            aic, p, rss = out[nm]
            ps = 'fit failed' if p is None else ' '.join(f"{v:.6g}" for v in p)
            print(f"      {nm:7s} AIC={aic:9.2f}  RSS={rss:.3e}  params: {ps}")
        if out['floor'][1] is not None:
            c = out['floor'][1][2]
            print(f"      fitted floor c = {c:.6g} "
                  f"({100*c/yy.min():.1f}% of the smallest measured rent/nat) "
                  f"— a curve parameter over k=5..{int(kk.max())}, NOT a prediction")
        # sawtooth as residual structure the smooth models cannot contain
        p = out[best][1]
        f = {'power': f_pow, 'floor': f_flo, 'linear': f_lin}[best]
        r = yy - f(kk, *p)
        sgn_isl = [float(r[list(kk).index(k)]) for k in ISLANDS if k in kk]
        sgn_stp = [float(r[list(kk).index(k)]) for k in STEPS_A if k in kk]
        print(f"      residuals of the best smooth fit: at islands (k=3 mod 4) "
              f"{['%+.2e'%v for v in sgn_isl]}")
        print(f"                                        at steps  (k=0 mod 4) "
              f"{['%+.2e'%v for v in sgn_stp]}")

    # =========================================================================
    # absolute-level secondary
    # =========================================================================
    print("\n" + "=" * 96)
    print("SECONDARY — the absolute-level condition (hold exactly 1.0 nat)")
    print("=" * 96)
    for eps in (0.01, 0.05):
        line = []
        for k0 in STEPS_A:
            a, b = (pick(rows, 'A', k0, eps, '1.0nat', 'abs'),
                    pick(rows, 'A', k0 - 1, eps, '1.0nat', 'abs'))
            if a is None or b is None:
                line.append(f"k{k0}:--")
            else:
                line.append(f"k{k0}:{'UP ' if a['rent_per_nat']>b['rent_per_nat'] else 'dn '}")
        print(f"  eps={eps} hold 1.0 nat: " + " ".join(line))
    print("  ARM A rent/nat holding exactly 1.0 nat:")
    for eps in (0.01, 0.05):
        vals = [(k, pick(rows, 'A', k, eps, '1.0nat', 'abs')) for k in ks]
        vals = [(k, v['rent_per_nat']) for k, v in vals if v]
        if not vals:
            continue
        lo, hi = min(v for _, v in vals), max(v for _, v in vals)
        print(f"    eps={eps}:")
        for k, v in vals:
            mark = '*' if k % 4 == 3 else ('^' if k % 4 == 0 else ' ')
            print(f"      k={k:2d}{mark} {v:10.6f}  {bar(v, lo, hi)}")

    # =========================================================================
    # instrument comparison
    # =========================================================================
    print("\n" + "=" * 96)
    print("INSTRUMENT — the parent's controller vs the fixed-point definition")
    print("=" * 96)
    for r in d['instrument_comparison']:
        print(f"  {r['old_tag']:4s}->{r['new_tag']:4s} eps={r['eps']} frac={r['frac']}: "
              f"achieved {r['old_achieved']:.4f} -> {r['new_achieved']:.6f}   "
              f"rent/nat {r['old_rent_per_nat']:.5f} -> {r['new_rent_per_nat']:.5f} "
              f"({100*(r['new_rent_per_nat']/r['old_rent_per_nat']-1):+.1f}%)")

    posthoc(rows, ks)
    figure(d, rows, ks)
    print(f"\nwrote {FIG}")


def posthoc(rows, ks):
    """EXPLORATORY. Nothing below was pre-registered; it exists because the primary and
    the pre-registered secondary disagreed, and the prereg (§4) says that disagreement is
    itself the finding and must be explained rather than resolved by choosing a winner."""
    print("\n" + "=" * 96)
    print("POST-HOC — NOT PRE-REGISTERED. Read as exploratory description of a mixed")
    print("primary result, not as evidence. No verdict below overrides §2's rules.")
    print("=" * 96)

    print("\n(a) THE TOOTH AGAINST THE LOCAL TREND. rent/nat falls steadily with k; a step")
    print("    only shows as an actual local MAXIMUM if the tooth beats that fall. Below:")
    print("    the log-jump at the step minus the mean log-jump within the run after it.")
    allc = CONDS + [(0.01, '1.0nat'), (0.05, '1.0nat')]
    for eps, lab in allc:
        mode = 'abs' if lab.endswith('nat') else 'frac'
        get = lambda k: (pick(rows, 'A', k, eps, lab, mode) or {}).get('rent_per_nat')
        cells = []
        for k0 in STEPS_A:
            a, b = get(k0), get(k0 - 1)
            run = [(get(j), get(j - 1)) for j in (k0 + 1, k0 + 2, k0 + 3)]
            run = [np.log(x / y) for x, y in run if x and y]
            if not (a and b and run):
                cells.append(f"k{k0}:  --   ")
                continue
            excess = np.log(a / b) - float(np.mean(run))
            cells.append(f"k{k0}:{100*excess:+7.3f}pp")
        print(f"    eps={eps} {lab:>7s}: " + " ".join(cells))
    print("    For comparison, the same statistic computed on the DENSITY CEILING alone:")
    dens = lambda k: (np.log(2) - np.log(4 * ((k + 4) // 4)) / k)
    cells = []
    for k0 in STEPS_A:
        run = [np.log(dens(j) / dens(j - 1)) for j in (k0 + 1, k0 + 2, k0 + 3)]
        cells.append(f"k{k0}:{100*(np.log(dens(k0)/dens(k0-1)) - np.mean(run)):+7.3f}pp")
    print("    density        : " + " ".join(cells))
    print("    -> the tooth is present in EVERY condition at similar size; what differs")
    print("       between frac=0.1 and frac=0.5 is the steepness of the trend it sits on.")

    print("\n(b) SIGN OF THE RESIDUAL after removing the best smooth fit (a*k^-b).")
    from scipy.optimize import curve_fit
    f_pow = lambda k, a, b: a * k ** (-b)
    for eps, lab in allc:
        mode = 'abs' if lab.endswith('nat') else 'frac'
        kk = np.array([k for k in ks if pick(rows, 'A', k, eps, lab, mode)], float)
        yy = np.array([pick(rows, 'A', int(k), eps, lab, mode)['rent_per_nat'] for k in kk])
        p, _ = curve_fit(f_pow, kk, yy, p0=[1.0, 1.0], maxfev=200000)
        r = yy - f_pow(kk, *p)
        isl = sum(1 for k in ISLANDS if k in kk and r[list(kk).index(k)] < 0)
        stp = sum(1 for k in STEPS_A if k in kk and r[list(kk).index(k)] > 0)
        print(f"    eps={eps} {lab:>7s}: islands below trend {isl}/5   steps above trend "
              f"{stp}/5   (10 events: {isl+stp}/10)")
    print("    A sawtooth of the predicted phase would put islands below and steps above.")


def figure(d, rows, ks):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    panels = CONDS + [(0.01, '1.0nat'), (0.05, '1.0nat')]
    fig, axes = plt.subplots(2, 3, figsize=(18.5, 9.5))
    for ax, (eps, lab) in zip(axes.ravel(), panels):
        mode = 'abs' if lab.endswith('nat') else 'frac'
        for arm, col, mk, nm in (('A', '#1f4e79', 'o', 'ARM A — minimum-size OA (max share)'),
                                 ('B', '#c05621', 's', 'ARM B — best linear, |S| = 2^m'),
                                 ('C', '#2f7d32', '^', 'ARM C — perfect codes')):
            pts = [(r['k'], r['rent_per_nat']) for r in rows
                   if r['arm'] == arm and r['eps'] == eps and r['target_label'] == lab
                   and r['mode'] == mode]
            pts.sort()
            if not pts:
                continue
            ax.plot([p[0] for p in pts], [p[1] for p in pts], mk + '-', color=col,
                    ms=4.5, lw=1.4, label=nm)
        for k in ISLANDS:
            ax.axvline(k, color='#1f4e79', lw=0.6, ls=':', alpha=0.55)
        for k in STEPS_A:
            ax.axvline(k, color='#a00000', lw=0.6, ls='--', alpha=0.45)
        ax.set_yscale('log')
        ax.set_xlabel('k  (slots)')
        ax.set_ylabel('rent / nat   (nats erased per step per nat held)')
        ttl = ('hold exactly 1.0 nat' if mode == 'abs'
               else f'hold {float(lab):.0%} of capacity')
        ax.set_title(f'ε = {eps},  {ttl}'
                     + ('   [pre-registered secondary]' if mode == 'abs' else ''))
        ax.grid(alpha=0.25, lw=0.5)
        ax.set_xticks(range(5, 25, 2))
        if (eps, lab) == panels[0]:
            ax.legend(fontsize=8, loc='upper right')
    fig.suptitle('Rent per nat vs number of slots — dotted blue: k ≡ 3 (mod 4), the '
                 'Hadamard-attained sizes;  dashed red: where the capacity ceiling steps '
                 'down\n(designed substrates; a measurement of PRICE, not of prevalence)',
                 fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(FIG, dpi=150)

    # a second figure: the sawtooth, as departure from the smooth trend
    fig2, axes2 = plt.subplots(1, 3, figsize=(18.5, 4.6))
    from scipy.optimize import curve_fit
    f_pow = lambda k, a, b: a * k ** (-b)
    for ax, (eps, lab) in zip(axes2, [CONDS[0], CONDS[3], (0.01, '1.0nat')]):
        mode = 'abs' if lab.endswith('nat') else 'frac'
        kk = np.array([k for k in ks if pick(rows, 'A', k, eps, lab, mode)], float)
        yy = np.array([pick(rows, 'A', int(k), eps, lab, mode)['rent_per_nat']
                       for k in kk])
        p, _ = curve_fit(f_pow, kk, yy, p0=[1.0, 1.0], maxfev=200000)
        rel = yy / f_pow(kk, *p) - 1.0
        cols = ['#1f4e79' if int(k) % 4 == 3 else ('#a00000' if int(k) % 4 == 0 else '#888')
                for k in kk]
        ax.bar(kk, 100 * rel, color=cols, width=0.72)
        ax.axhline(0, color='k', lw=0.8)
        ax.set_xlabel('k  (slots)')
        ax.set_ylabel('departure from the fitted power law  (%)')
        ttl = 'hold 1.0 nat' if mode == 'abs' else f'hold {float(lab):.0%}'
        ax.set_title(f'ε = {eps}, {ttl}:  residual after removing a·k^(−b)')
        ax.set_xticks(range(5, 25, 1))
        ax.grid(alpha=0.25, lw=0.5, axis='y')
    fig2.suptitle('The sawtooth, isolated: blue = k ≡ 3 (mod 4) (islands), '
                  'red = k ≡ 0 (mod 4) (ceiling steps down)', fontsize=10)
    fig2.tight_layout(rect=[0, 0, 1, 0.9])
    fig2.savefig(FIG.replace('.png', '_sawtooth.png'), dpi=150)


if __name__ == '__main__':
    main()
