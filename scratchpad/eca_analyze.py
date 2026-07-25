"""eca_analyze.py — adjudicate the pre-registered questions from the sweep JSON.

Decision rule is fixed in scratchpad/ECA_SPIKE_PREREG.md (committed at 421ba25) §8:
a spike requires (i) z_spike > 5, (ii) peak excess > 5 x null_sd, (iii) replication in all
seeds, (iv) cross-run refuter |z| < 5 at the peak, (v) no frozen slot.
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LN2 = float(np.log(2))
SELFCONJ = [15, 23, 43, 51, 77, 85, 105, 113, 142, 170, 150, 178, 204, 212, 232, 240]


def load(name):
    with open(os.path.join(HERE, name)) as f:
        return json.load(f)


def curves(rows):
    """(rule, reading) -> arrays sorted by P_n."""
    d = {}
    for r in rows:
        if r.get('reading') == 'OMEGA':
            continue
        d.setdefault((r['rule'], r['reading']), []).append(r)
    for k in d:
        d[k].sort(key=lambda r: r['P_n'])
    return d


def omega_curves(rows):
    d = {}
    for r in rows:
        if r.get('reading') == 'OMEGA':
            d.setdefault(r['rule'], []).append(r)
    for k in d:
        d[k].sort(key=lambda r: r['P_n'])
    return d


def spike_stat(cs):
    """Pre-registered spike statistic on one (rule, reading) curve."""
    ex = np.array([c['excess'] for c in cs])
    sem = np.array([c.get('excess_sem', np.nan) for c in cs])
    nsd = np.array([c['null_sd'] for c in cs])
    e0 = ex[0]
    j = int(np.argmax(ex[1:])) + 1                       # arg max over P_n > 0
    delta = ex[j] - e0
    den = np.sqrt(np.nan_to_num(sem[j]) ** 2 + np.nan_to_num(sem[0]) ** 2)
    z = delta / den if den > 0 else np.nan
    per = np.array(cs[j].get('excess_per_seed', [])) - np.array(cs[0].get('excess_per_seed', []))
    return dict(P_peak=cs[j]['P_n'], excess_det=e0, excess_peak=ex[j], delta=delta,
                z_spike=z, peak_over_floor=ex[j] / nsd[j] if nsd[j] > 0 else np.nan,
                all_seeds_up=bool(len(per) and np.all(per > 0)),
                refuter_z=cs[j].get('refuter_z', np.nan),
                min_slot_marg=cs[j]['min_slot_marg'],
                null_sd=nsd[j], sem_peak=sem[j], sem_det=sem[0], idx=j)


def declare(s):
    """The five pre-registered conditions."""
    c = dict(i_z=bool(s['z_spike'] > 5), ii_floor=bool(s['peak_over_floor'] > 5),
             iii_seeds=bool(s['all_seeds_up']),
             iv_refuter=bool(abs(np.nan_to_num(s['refuter_z'])) < 5),
             v_notfrozen=bool(s['min_slot_marg'] > 1e-6))
    return all(c.values()), c


def mechanism_exact(rule, p):
    """NO-DYNAMICS CONTROL, computed exactly (no sampling).

    Apply the rule ONCE to uniform i.i.d. inputs (a,b,c) and flip the output with
    probability p. Return I_C^(3) of each causal triple. Any structure here is the rule's
    own truth table read through a uniform input distribution -- it involves no cellular
    automaton, no lattice, no time evolution and no emergence whatsoever. If a measured
    CAUSAL curve tracks this one, its shape is a property of the mechanism and the noise,
    not of the dynamics.
    """
    import array_cap_experiment as ACE
    P = {'CAUSAL-LR': np.zeros((2, 2, 2)), 'CAUSAL-LC': np.zeros((2, 2, 2)),
         'CAUSAL-CR': np.zeros((2, 2, 2))}
    for a in range(2):
        for b in range(2):
            for c in range(2):
                y0 = (rule >> (4 * a + 2 * b + c)) & 1
                for y in range(2):
                    w = (1 - p) if y == y0 else p
                    P['CAUSAL-LR'][a, c, y] += 0.125 * w
                    P['CAUSAL-LC'][a, b, y] += 0.125 * w
                    P['CAUSAL-CR'][b, c, y] += 0.125 * w
    return {k: ACE.shareK(v)[0] for k, v in P.items()}


def fmt(x, n=6):
    return 'nan' if x is None or (isinstance(x, float) and np.isnan(x)) else f'{x:.{n}f}'


def main():
    out = []
    W = out.append

    # ---------------- FOCUS ----------------
    focus = load('eca_focus.json')
    cf = curves(focus)
    of = omega_curves(focus)
    Pn = sorted({r['P_n'] for r in focus})

    W("=" * 100)
    W("P1 GATE — the two-term linear rules, pre-committed as EXPECTED not discovered")
    W("=" * 100)
    W(f"{'rule':>5} {'mechanism':>22} {'reading':>12} {'I_C3 at P_n=0':>15} {'ln2':>10}")
    for rule, rd, mech in ((90, 'CAUSAL-LR', 's_{i-1} XOR s_{i+1}'),
                           (60, 'CAUSAL-LC', 's_{i-1} XOR s_i'),
                           (102, 'CAUSAL-CR', 's_i XOR s_{i+1}')):
        if (rule, rd) in cf:
            W(f"{rule:5d} {mech:>22} {rd:>12} {cf[(rule, rd)][0]['share']:15.9f} {LN2:10.6f}")

    W("")
    W("=" * 100)
    W("P2 GATE — the symmetry lemma on the 16 complementation-symmetric rules")
    W("=" * 100)
    W("max |I_C^(3)| over ALL readings and ALL 18 noise levels, vs the estimator floor")
    W(f"{'rule':>5} {'max|share|':>12} {'max|excess|':>12} {'max null_sd':>12} {'max |z|':>9} {'in paper Omega=0 list':>22}")
    zerolist = {0, 8, 32, 40, 128, 136, 160, 45, 75, 105, 150, 15, 51, 154, 170, 204}
    sc_rows = []
    for rule in sorted({r['rule'] for r in focus} & set(SELFCONJ)):
        rs = [c for (ru, _), cs in cf.items() if ru == rule for c in cs]
        if not rs:
            continue
        msh = max(abs(c['share']) for c in rs)
        mex = max(abs(c['excess']) for c in rs)
        msd = max(c['null_sd'] for c in rs)
        mz = max(abs(c['excess']) / c['null_sd'] if c['null_sd'] > 0 else 0 for c in rs)
        sc_rows.append((rule, msh, mex, msd, mz))
        W(f"{rule:5d} {msh:12.3e} {mex:12.3e} {msd:12.3e} {mz:9.2f} "
          f"{'yes' if rule in zerolist else 'NO -- nonzero Omega':>22}")

    W("")
    W("=" * 100)
    W("P0 CONTROL — the paper's Figure 1B entropy curves (bits), reproduced")
    W("=" * 100)
    hdr = "  ".join(f"{p:>8.2e}" if p else f"{'det':>8}" for p in Pn)
    W(f"{'rule':>5}  {hdr}")
    for rule in (8, 19, 22, 30, 45, 46):
        if rule in of:
            W(f"{rule:5d}  " + "  ".join(f"{c['H_plugin']:8.2f}" for c in of[rule]))

    W("")
    W("=" * 100)
    W("INTERNAL POSITIVE CONTROL — the paper's own quantities on the same trajectories")
    W("=" * 100)
    for q in ('Omega_plugin', 'Sigma_plugin'):
        W(f"\n{q} (bits)")
        W(f"{'rule':>5}  {hdr}")
        for rule in sorted(of):
            W(f"{rule:5d}  " + "  ".join(f"{c[q]:8.2f}" for c in of[rule]))

    W("")
    W("biphasic test on the paper's quantities: does the curve have an interior extremum")
    W("exceeding BOTH endpoints by > 0.5 bits?")
    W(f"{'rule':>5} {'Omega biphasic':>16} {'amount(bits)':>13} {'at P_n':>10} "
      f"{'Sigma biphasic':>16} {'amount':>9} {'at P_n':>10}")
    biph = {}
    for rule in sorted(of):
        row = [rule]
        for q in ('Omega_plugin', 'Sigma_plugin'):
            v = np.array([c[q] for c in of[rule]])
            best, bamt, bp = 'no', 0.0, np.nan
            for sgn in (1, -1):
                w = sgn * v
                k = int(np.argmax(w[1:-1])) + 1
                amt = min(w[k] - w[0], w[k] - w[-1])
                if amt > bamt:
                    bamt, bp = amt, of[rule][k]['P_n']
                    best = 'yes(+)' if sgn > 0 else 'yes(-)'
            row += [best if bamt > 0.5 else 'no', bamt, bp]
            biph[(rule, q)] = (bamt > 0.5, bamt, bp)
        W(f"{row[0]:5d} {row[1]:>16} {row[2]:13.2f} {row[3]:10.2e} "
          f"{row[4]:>16} {row[5]:9.2f} {row[6]:10.2e}")

    # ---------------- the pre-registered spike test ----------------
    W("")
    W("=" * 100)
    W("THE PRE-REGISTERED SPIKE TEST on I_C^(3) — focus stage")
    W("=" * 100)
    W("Delta = max over P_n>0 of excess - excess(P_n=0);  z_spike = Delta / sqrt(sem^2+sem0^2)")
    W(f"{'rule':>5} {'reading':>16} {'exc(det)':>11} {'exc(peak)':>11} {'Delta':>11} "
      f"{'P_peak':>9} {'z_spike':>9} {'pk/floor':>9} {'refZ':>7} {'seeds':>6} {'SPIKE':>6}")
    spikes = []
    allstats = {}
    for (rule, rd), cs in sorted(cf.items()):
        s = spike_stat(cs)
        allstats[(rule, rd)] = s
        ok, c = declare(s)
        if ok:
            spikes.append((rule, rd, s))
        # print the per-rule best readings and anything that fires
        if ok or s['z_spike'] > 3 or rd in ('TEMPORAL', 'CAUSAL-LR'):
            W(f"{rule:5d} {rd:>16} {s['excess_det']:11.3e} {s['excess_peak']:11.3e} "
              f"{s['delta']:+11.3e} {s['P_peak']:9.2e} {s['z_spike']:9.2f} "
              f"{s['peak_over_floor']:9.1f} {np.nan_to_num(s['refuter_z']):7.2f} "
              f"{'ok' if s['all_seeds_up'] else 'no':>6} {'YES' if ok else 'no':>6}")

    W("")
    W("per-rule best SPATIAL shape (the reading with the largest Delta):")
    W(f"{'rule':>5} {'best shape':>18} {'exc(det)':>11} {'exc(peak)':>11} {'Delta':>11} "
      f"{'P_peak':>9} {'z_spike':>9} {'SPIKE':>6}")
    for rule in sorted({r for r, _ in cf}):
        cand = [(rd, s) for (ru, rd), s in allstats.items()
                if ru == rule and rd.startswith('SPATIAL')]
        if not cand:
            continue
        rd, s = max(cand, key=lambda t: np.nan_to_num(t[1]['z_spike']))
        ok, _ = declare(s)
        W(f"{rule:5d} {rd:>18} {s['excess_det']:11.3e} {s['excess_peak']:11.3e} "
          f"{s['delta']:+11.3e} {s['P_peak']:9.2e} {s['z_spike']:9.2f} {'YES' if ok else 'no':>6}")

    W("")
    W(f"DECLARED SPIKES (all five pre-registered conditions): {len(spikes)}")
    for rule, rd, s in spikes:
        ok, c = declare(s)
        det_frozen = cf[(rule, rd)][0]['min_slot_marg']
        W(f"  rule {rule} {rd}: Delta={s['delta']:+.3e} at P_n={s['P_peak']:.2e}, "
          f"z_spike={s['z_spike']:.1f}, conditions={c}, "
          f"min slot marginal at P_n=0 = {det_frozen:.3e}"
          + ("  [DETERMINISTIC ENDPOINT IS FROZEN -- its zero is by construction]"
             if det_frozen < 1e-6 else ""))

    # ---------------- the no-dynamics mechanism control ----------------
    W("")
    W("=" * 100)
    W("NO-DYNAMICS CONTROL — the rule applied ONCE to uniform i.i.d. inputs, exact")
    W("=" * 100)
    W("Any CAUSAL curve that tracks this one is reading the rule's truth table through its")
    W("input distribution. No lattice, no time evolution, no emergence is involved here.")
    for rd in ('CAUSAL-LR', 'CAUSAL-LC', 'CAUSAL-CR'):
        W(f"\n{rd}:  measured (m) vs no-dynamics control (c), nats")
        W(f"{'rule':>5}  " + "  ".join(f"{p:>8.2e}" if p else f"{'det':>8}" for p in Pn))
        for rule in sorted({r for r, x in cf if x == rd}):
            mech = [mechanism_exact(rule, p)[rd] for p in Pn]
            meas = [c['share'] for c in cf[(rule, rd)]]
            if max(meas) < 1e-4 and max(mech) < 1e-4:
                continue
            W(f"{rule:5d}m " + "  ".join(f"{v:8.4f}" for v in meas))
            W(f"{'':5}c " + "  ".join(f"{v:8.4f}" for v in mech))

    # ---------------- floors, refuter, degeneracy ----------------
    W("")
    W("=" * 100)
    W("FLOORS, REFUTER AND DEGENERACY")
    W("=" * 100)
    nsd = np.array([r['null_sd'] for r in focus if r.get('reading') != 'OMEGA'])
    nm = np.array([r['null_mean'] for r in focus if r.get('reading') != 'OMEGA'])
    sm = np.array([r['shuffle_mean'] for r in focus if r.get('reading') != 'OMEGA'])
    rz = np.array([r.get('refuter_z', np.nan) for r in focus if r.get('reading') != 'OMEGA'])
    ipf = np.array([r['ipf_err'] for r in focus if r.get('reading') != 'OMEGA'])
    mm = np.array([r['min_slot_marg'] for r in focus if r.get('reading') != 'OMEGA'])
    W(f"matched pairwise-maxent surrogate null: mean {nm.mean():.3e}, sd {nsd.mean():.3e} "
      f"(max {nsd.max():.3e}) over {len(nsd)} sweep points")
    W(f"shuffle floor: mean {sm.mean():.3e}")
    W(f"IPF residual: max {ipf.max():.3e}")
    W(f"CROSS-RUN REFUTER |z|: max {np.nanmax(np.abs(rz)):.2f}, mean |z| {np.nanmean(np.abs(rz)):.2f}, "
      f"points with |z|>5: {int(np.sum(np.abs(rz) > 5))} of {int(np.sum(~np.isnan(rz)))}")
    W(f"tied fraction: 0.00000 at every point, structurally -- the substrate is natively "
      f"binary, there is no threshold and no median split")
    W(f"frozen slots (min slot marginal < 1e-6): {int(np.sum(mm < 1e-6))} of {len(mm)} "
      f"sweep points; smallest non-frozen slot marginal {mm[mm >= 1e-6].min() if (mm>=1e-6).any() else float('nan'):.3e}")

    # ---------------- SCREEN ----------------
    if os.path.exists(os.path.join(HERE, 'eca_screen.json')):
        scr = load('eca_screen.json')
        cs_ = curves(scr)
        W("")
        W("=" * 100)
        W("SCREEN — all 256 rules, R=65536, 400 steps, 1 seed")
        W("=" * 100)
        best = []
        for (rule, rd), cc in cs_.items():
            ex = np.array([c['excess'] for c in cc])
            nsd_ = np.array([c['null_sd'] for c in cc])
            j = int(np.argmax(ex[1:])) + 1
            d = ex[j] - ex[0]
            z = d / nsd_[j] if nsd_[j] > 0 else 0.0     # 1 seed: floor-relative only
            best.append((z, d, rule, rd, cc[j]['P_n'], ex[0], ex[j]))
        best.sort(reverse=True)
        W("top 25 by (peak - deterministic) / null_sd, over all 256 rules x 28 readings:")
        W(f"{'z_floor':>9} {'Delta':>11} {'rule':>5} {'reading':>16} {'P_peak':>9} "
          f"{'exc(det)':>11} {'exc(peak)':>11}")
        for z, d, rule, rd, p, e0, ep in best[:25]:
            W(f"{z:9.1f} {d:+11.3e} {rule:5d} {rd:>16} {p:9.2e} {e0:11.3e} {ep:11.3e}")
        sp = [b for b in best if b[3].startswith('SPATIAL') or b[3] == 'TEMPORAL']
        W("")
        W("top 15 restricted to the two PRIMARY readings (SPATIAL, TEMPORAL):")
        for z, d, rule, rd, p, e0, ep in sp[:15]:
            W(f"{z:9.1f} {d:+11.3e} {rule:5d} {rd:>16} {p:9.2e} {e0:11.3e} {ep:11.3e}")
        # equivalence-class consistency
        W("")
        def conj(n):
            return sum((1 - ((n >> (7 - k)) & 1)) << k for k in range(8))
        pairs, dif = 0, 0.0
        for (rule, rd), cc in cs_.items():
            c2 = cs_.get((conj(rule), rd))
            if c2 and conj(rule) != rule:
                pairs += 1
                dif = max(dif, max(abs(a['share'] - b['share']) for a, b in zip(cc, c2)))
        W(f"equivalence-class consistency: colour-inversion partners agree to {dif:.3e} nats "
          f"over {pairs} reading-pairs (I_C^(3) is exactly invariant under complementing all "
          f"three slots; the residual is Monte-Carlo, the two rules use different seeds)")

    txt = "\n".join(out)
    print(txt)
    with open(os.path.join(HERE, 'eca_analysis.txt'), 'w') as f:
        f.write(txt + "\n")


if __name__ == '__main__':
    main()
