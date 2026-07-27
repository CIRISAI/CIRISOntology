"""rent_scaling_analyze.py — adjudicates RENT_SCALING_PREREG.md against the runs.

Nothing here chooses a subset, a threshold or a fit range after seeing a number: every rule
is quoted from the prereg section it comes from, in the code, at the point of use.

  --q1        H-IFF, H-ORBIT, the (T) consistency check
  --ceiling   the q=1 restorability measurement on every affordable structure, then H-CEILING
  --q2        the pre-registered fits, the k=28 step, the trend correction, H-DISSOC-2
"""
import sys, os, json, argparse, itertools
from math import comb
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
LN2 = float(np.log(2))
KCEIL = 23          # the q=1 ceiling pass affordability cut, DECLARED


# =====================================================================================
# Q1
# =====================================================================================

def q1(path=None):
    J = json.load(open(path or os.path.join(HERE, 'rent_scaling_q1.json')))
    rows = J['rows']
    print("=" * 96)
    print("QUESTION 1 — is the restorability boundary exactly algebraic?  (prereg §2)")
    print(f"roster: {len(rows)} structures; R computed where 2^k affordable, cut k <= "
          f"{J['kmax_R']}; node budget {J['node_budget']:,}")
    print("=" * 96)

    have_R = [r for r in rows if r['profile_dev'] is not None]
    prim = [r for r in have_R if r['rows_distinct']]
    print(f"\nR computed for {len(have_R)} of {len(rows)}; PRIMARY tally restricted to the "
          f"{len(prim)} with all N rows distinct (declared: a property of the structure).")
    inexact = [r for r in rows if not r['exact']]
    print(f"searches that exhausted their node budget: {len(inexact)} "
          f"{[r['label'] for r in inexact]}")

    # ---- (T): transitive => equivariant. A violation is an instrument fault.
    viol = [r for r in prim if r['transitive'] and r['profile_dev'] > 1e-12]
    print(f"\n(T) TRANSITIVE => EQUIVARIANT — violations: {len(viol)}  "
          f"{'consistent' if not viol else [r['label'] for r in viol]}")
    tr = [r for r in prim if r['transitive']]
    if tr:
        print(f"    {len(tr)} transitive structures, max profile_dev "
              f"{max(r['profile_dev'] for r in tr):.3e}")

    # ---- H-IFF necessity: equivariant => transitive?
    ctr = [r for r in prim if (not r['transitive']) and r['profile_dev'] < 1e-12]
    intr = [r for r in prim if not r['transitive']]
    print(f"\nH-IFF (NECESSITY: equivariant => transitive)")
    print(f"    intransitive structures: {len(intr)}")
    print(f"    of which EQUIVARIANT (counterexamples): {len(ctr)}")
    for r in ctr:
        print(f"      {r['label']:10s} |S|={r['ns']:3d} |Aut|={r['aut_order']:8d} "
              f"orbits={r['orbit_sizes']} levels={r['level_sizes']} "
              f"profile_dev={r['profile_dev']:.3e}")
    print(f"    VERDICT: {'H-IFF CONFIRMED' if not ctr else 'H-IFF DEAD in the necessity direction'}")

    # ---- H-ORBIT: level sets == orbits
    both = [r for r in prim if r['levels_eq_orbits'] is not None]
    eq = [r for r in both if r['levels_eq_orbits']]
    ref = [r for r in both if not r['orbits_refine_levels']]
    print(f"\nH-ORBIT (level sets == orbits)")
    print(f"    orbits refine levels (theorem) — violations: {len(ref)} "
          f"{[r['label'] for r in ref]}")
    print(f"    levels EQUAL orbits: {len(eq)} of {len(both)}")
    bad = [r for r in both if not r['levels_eq_orbits']]
    print(f"    strict coarsenings (accidental degeneracy): {len(bad)}")
    for r in bad[:14]:
        print(f"      {r['label']:10s} orbits {str(r['orbit_sizes'])[:34]:34s} "
              f"levels {str(r['level_sizes'])[:34]:34s} pdev={r['profile_dev']:.2e}")
    if len(bad) > 14:
        print(f"      ... and {len(bad)-14} more")
    print(f"    VERDICT: {'H-ORBIT CONFIRMED' if not bad else 'H-ORBIT DEAD'}")

    # ---- the ARM A ladder, which is the one the rent table lives on
    print("\nThe ARM A ladder (the widths the rent curve uses):")
    print(f"  {'k':>3s} {'|S|':>4s} {'lin':>5s} {'|Aut|':>12s} {'orbits':>26s} "
          f"{'trans':>6s} {'profile_dev':>12s} {'levels':>18s}")
    for r in sorted([x for x in rows if x['is_armA']], key=lambda x: x['k']):
        pd = f"{r['profile_dev']:.3e}" if r['profile_dev'] is not None else 'skip'
        print(f"  {r['k']:3d} {r['ns']:4d} {str(r['linear']):>5s} {r['aut_order']:12d} "
              f"{str(r['orbit_sizes'])[:26]:>26s} {str(r['transitive']):>6s} {pd:>12s} "
              f"{str(r['level_sizes'])[:18]:>18s}")
    return rows


# =====================================================================================
# the q = 1 restorability measurement, and H-CEILING
# =====================================================================================

def imbalance(sizes, n):
    """0 for a transitive action, -> 1 as the orbits shatter. I = 1 - sum|O|^2/|S|^2,
    rescaled so a single orbit reads 0 and all-singletons reads 1."""
    s = sum(x * x for x in sizes) / (n * n)
    return float((1.0 - s) / (1.0 - 1.0 / n)) if n > 1 else 0.0


def ceiling_pass(path=None, kmax=KCEIL, out=None):
    import rent_scaling_q2 as Q2
    import rent_islands_design_check as DC
    J = json.load(open(path or os.path.join(HERE, 'rent_scaling_q1.json')))
    rows = J['rows']
    todo = [r for r in rows if r['rows_distinct'] and not r['linear']
            and r['k'] <= kmax and r['profile_dev'] is not None]
    print("=" * 96)
    print(f"THE q=1 RESTORABILITY MEASUREMENT — {len(todo)} non-linear structures, k <= {kmax}")
    print("=" * 96)
    out_rows = []
    for r in todo:
        N, k = r['order_N'], r['k']
        H = DC.hadamard(N).copy()
        H = H * np.where(H[:, [0]] == -1, -1, 1)
        S = ((1 - H[:, 1:]) // 2).astype(np.int8)[:, :k]
        L = Q2.LeanFull(r['label'], 'Q1', k, S)
        rec = dict(label=r['label'], k=k, ns=L.ns, order_N=N,
                   transitive=r['transitive'], orbit_sizes=r['orbit_sizes'],
                   n_orbits=r['n_orbits'], imbalance=imbalance(r['orbit_sizes'], L.ns),
                   profile_dev=L.profile_dev, share_max=L.share_max)
        for eps in (0.01, 0.05):
            st = L.stat_share(1.0, eps)
            c, _ = L.solve_c(1.0, eps)
            rec[f'ceiling_frac_{eps}'] = float(st['share'] / L.share_max)
            rec[f'Hc_deficit_{eps}'] = float(np.log(L.ns) - st['H_c'])
            rec[f'tv_{eps}'] = float(0.5 * np.abs(c - 1.0 / L.ns).sum())
        L.free()
        out_rows.append(rec)
        print(f"  {r['label']:10s} |S|={L.ns:3d} trans={str(r['transitive']):5s} "
              f"I={rec['imbalance']:.4f} pdev={L.profile_dev:.3e} "
              f"ceil@.05={rec['ceiling_frac_0.05']:.12f} "
              f"Hcdef@.05={rec['Hc_deficit_0.05']:.3e} TV={rec['tv_0.05']:.3e}", flush=True)
    p = out or os.path.join(HERE, 'rent_scaling_ceiling.json')
    json.dump(dict(rows=out_rows, kmax=kmax), open(p, 'w'), indent=1)
    print(f"\n-> {p}")
    return out_rows


def _spearman(x, y):
    rx, ry = _rank(x), _rank(y)
    rx = rx - rx.mean()
    ry = ry - ry.mean()
    den = np.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    return float((rx * ry).sum() / den) if den > 0 else 0.0


def _rank(v):
    v = np.asarray(v, dtype=float)
    order = v.argsort()
    r = np.empty(len(v))
    r[order] = np.arange(len(v))
    # average ties
    for val in np.unique(v):
        m = v == val
        if m.sum() > 1:
            r[m] = r[m].mean()
    return r


def h_ceiling(path=None, eps=0.05):
    J = json.load(open(path or os.path.join(HERE, 'rent_scaling_ceiling.json')))
    rows = [r for r in J['rows'] if r['profile_dev'] >= 1e-12]      # the LOSSY population
    print("\n" + "=" * 96)
    print(f"H-CEILING — deposit deficit vs orbit imbalance, lossy structures only, eps={eps}")
    print("=" * 96)
    x = np.array([r['imbalance'] for r in rows])
    y = np.array([r[f'Hc_deficit_{eps}'] for r in rows])
    n = len(rows)
    rho = _spearman(x, y)
    print(f"  n = {n} lossy structures;  Spearman rho = {rho:+.4f}  "
          f"(prereg predicts POSITIVE)")
    # exact permutation null over the multiset of imbalance labels
    uniq = sorted(set(map(float, x)))
    nperm = np.math.factorial(n) if n <= 9 else None
    rng = np.random.default_rng(20260727)
    if nperm is not None and nperm <= 400000:
        null = np.array([_spearman(np.array(p), y)
                         for p in itertools.permutations(x)])
        how = f'exact, all {len(null):,} permutations'
    else:
        null = np.array([_spearman(rng.permutation(x), y) for _ in range(200000)])
        how = (f'{len(null):,} random permutations — full enumeration of {n}! is '
               f'infeasible, so this is a sampled null and is labelled one')
    p_two = float((np.abs(null) >= abs(rho) - 1e-12).mean())
    p_one = float((null >= rho - 1e-12).mean())
    print(f"  null: {how}")
    print(f"  null shape: mean {null.mean():+.4f}  sd {null.std():.4f}  "
          f"skew {float(((null-null.mean())**3).mean()/max(null.std(),1e-30)**3):+.3f}  "
          f"quantiles 5/50/95 = {np.percentile(null,5):+.3f}/"
          f"{np.percentile(null,50):+.3f}/{np.percentile(null,95):+.3f}")
    print(f"  p (one-sided, the pre-registered direction) = {p_one:.4g}")
    print(f"  p (two-sided)                               = {p_two:.4g}")
    if rho <= 0:
        v = 'H-CEILING DEAD — correlation of the wrong sign'
    elif p_one < 0.05:
        v = 'H-CEILING SUPPORTED at this sample size'
    else:
        v = f'H-CEILING UNRESOLVED at n={n} — sign right, p above 0.05'
    print(f"  VERDICT: {v}")
    for r in sorted(rows, key=lambda r: -r['imbalance'])[:40]:
        print(f"    {r['label']:10s} |S|={r['ns']:3d} orbits={str(r['orbit_sizes'])[:24]:24s}"
              f" I={r['imbalance']:.4f}  Hc_def={r[f'Hc_deficit_{eps}']:.3e}"
              f"  1-ceil={1-r[f'ceiling_frac_{eps}']:.3e}")
    return rho, p_one


# =====================================================================================
# Q2 — the fits
# =====================================================================================

def _load_q2():
    rows = []
    P = json.load(open(os.path.join(HERE, 'rent_islands_results.json')))['rows']
    for r in P:
        if not r.get('dropped'):
            r['src'] = 'parent'
            rows.append(r)
    for f in sorted(os.listdir(HERE)):
        if f.startswith('rent_scaling_q2_') and f.endswith('.json') and 'gate' not in f:
            for r in json.load(open(os.path.join(HERE, f)))['rows']:
                if not r.get('dropped'):
                    r['src'] = 'new'
                    rows.append(r)
    return rows


CONDS = [(0.01, 'frac', '0.1'), (0.01, 'frac', '0.5'), (0.01, 'abs', '1.0nat'),
         (0.05, 'frac', '0.1'), (0.05, 'frac', '0.5'), (0.05, 'abs', '1.0nat')]


def _series(rows, arm, cond):
    eps, mode, lab = cond
    d = {r['k']: r['rent_per_nat'] for r in rows
         if r['arm'] == arm and r['eps'] == eps and r['mode'] == mode
         and r['target_label'] == lab}
    ks = np.array(sorted(d))
    return ks, np.array([d[k] for k in ks])


def _fit(ks, ys, form, cfix=None):
    from scipy.optimize import least_squares
    ly = np.log(ys)

    def model(p, c=None):
        if form == 'F1':
            return np.log(p[0]) - p[1] * np.log(ks)
        if form == 'F2':
            cc = c if c is not None else p[2]
            return np.log(np.maximum(cc + p[0] * ks ** (-p[1]), 1e-300))
        if form == 'F3':
            cc = c if c is not None else p[2]
            return np.log(np.maximum(cc + p[0] * np.exp(-p[1] * ks), 1e-300))
        if form == 'F4':
            return np.log(np.maximum(p[0] + p[1] * ks, 1e-300))
        raise ValueError(form)

    if form == 'F1':
        p0 = [ys[0] * ks[0], 1.0]
    elif form == 'F2':
        p0 = [ys[0] * ks[0], 1.0] + ([] if cfix is not None else [0.5 * ys[-1]])
    elif form == 'F3':
        p0 = [ys[0], 0.1] + ([] if cfix is not None else [0.5 * ys[-1]])
    else:
        p0 = [ys[0], -1e-3]
    r = least_squares(lambda p: model(p, cfix) - ly, p0, method='lm', max_nfev=20000)
    sse = float(np.sum(r.fun ** 2))
    npar = len(p0) + (0 if cfix is None else 0)
    return sse, r.x, npar


def _aic(sse, n, p):
    return n * np.log(max(sse, 1e-300) / n) + 2 * p


def q2():
    rows = _load_q2()
    print("=" * 96)
    print("QUESTION 2 — does rent/nat plateau?  (prereg §3)")
    print("=" * 96)
    kmax = max(r['k'] for r in rows if r['arm'] == 'A')
    print(f"ARM A measured k = 5 .. {kmax}   ({sum(1 for r in rows if r['arm']=='A')} rows)")

    verdicts = []
    print(f"\n{'condition':22s} {'best':>5s} {'dAIC(F1-best)':>13s} {'floor c':>11s} "
          f"{'[c_lo, c_hi]':>26s} {'min rent':>10s} {'resolved':>9s}")
    for cond in CONDS:
        ks, ys = _series(rows, 'A', cond)
        if len(ks) < 8:
            continue
        n = len(ks)
        res = {}
        for form in ('F1', 'F2', 'F3', 'F4'):
            sse, par, npar = _fit(ks, ys, form)
            res[form] = (sse, par, _aic(sse, n, npar))
        best = min(res, key=lambda f: res[f][2])
        # floor profile on whichever of F2/F3 fits better
        ff = 'F2' if res['F2'][2] <= res['F3'][2] else 'F3'
        cgrid = np.linspace(0.0, 1.2 * ys[-1], 601)
        sses = np.array([_fit(ks, ys, ff, cfix=float(c))[0] for c in cgrid])
        smin = sses.min()
        keep = cgrid[sses <= smin * np.exp(4.0 / n)]
        clo, chi = float(keep.min()), float(keep.max())
        chat = float(cgrid[sses.argmin()])
        dA = res['F1'][2] - res[best][2]
        beats = res['F1'][2] - min(res['F2'][2], res['F3'][2])
        resolved = (beats >= 4.0) and (clo > 0) and (chi < 0.98 * ys[-1])
        verdicts.append(dict(cond=cond, best=best, dAIC_F1_minus_best=dA,
                             beats=beats, c=chat, c_lo=clo, c_hi=chi,
                             min_rent=float(ys[-1]), resolved=bool(resolved),
                             contains_zero=bool(clo <= 0)))
        lab = f"eps={cond[0]} {cond[1]}{cond[2]}"
        print(f"{lab:22s} {best:>5s} {dA:13.2f} {chat:11.5f} "
              f"[{clo:.5f}, {chi:.5f}]".ljust(75) +
              f" {ys[-1]:10.5f} {str(resolved):>9s}")

    nres = sum(v['resolved'] for v in verdicts)
    nzero = sum(v['contains_zero'] or v['best'] == 'F1' for v in verdicts)
    print(f"\n  PLATEAU-WITH-FLOOR rule (>= 4 of 6): {nres}/6")
    print(f"  CONTINUED-DECLINE rule  (>= 4 of 6): {nzero}/6")

    # sawtooth dominance
    saw = 0
    for cond in CONDS:
        ks, ys = _series(rows, 'A', cond)
        if len(ks) < 8:
            continue
        sse, par, _ = _fit(ks, ys, 'F1')
        pred = np.log(par[0]) - par[1] * np.log(ks)
        resid = np.log(ys) - pred
        step = resid[(ks % 4) == 0].mean() - resid[(ks % 4) == 3].mean()
        rms = float(np.sqrt((resid ** 2).mean()))
        if abs(step) > rms:
            saw += 1
        print(f"  sawtooth eps={cond[0]} {cond[1]}{cond[2]}: "
              f"step-minus-island residual {step:+.5f} vs RMS residual {rms:.5f}"
              f"  {'DOMINANT' if abs(step) > rms else ''}")
    print(f"  SAWTOOTH-DOMINATED rule (>= 4 of 6): {saw}/6")

    if nres >= 4:
        v = 'PLATEAU-WITH-FLOOR'
    elif nzero >= 4:
        v = 'CONTINUED DECLINE'
    elif saw >= 4:
        v = 'SAWTOOTH-DOMINATED'
    else:
        v = 'MIXED'
    print(f"\n  *** Q2 VERDICT OF RECORD: {v} ***")

    # ---- the steps, raw and trend-corrected (parent §7(a))
    print("\nSteps: raw uptick and the trend-corrected tooth (parent's §7(a) statistic)")
    print(f"{'condition':22s} " + " ".join(f"{'k='+str(k0):>16s}"
                                           for k0 in (8, 12, 16, 20, 24, 28)))
    upA = {k0: 0 for k0 in (8, 12, 16, 20, 24, 28)}
    for cond in CONDS:
        ks, ys = _series(rows, 'A', cond)
        d = dict(zip(ks, ys))
        cells = []
        for k0 in (8, 12, 16, 20, 24, 28):
            if k0 not in d or (k0 - 1) not in d:
                cells.append(f"{'-':>16s}")
                continue
            up = d[k0] > d[k0 - 1]
            upA[k0] += int(up)
            jumps = [np.log(d[k0 + i + 1]) - np.log(d[k0 + i])
                     for i in range(3) if (k0 + i + 1) in d and (k0 + i) in d]
            if jumps:
                tooth = (np.log(d[k0]) - np.log(d[k0 - 1])) - float(np.mean(jumps))
                cells.append(f"{('UP' if up else 'dn')+f' {100*tooth:+.2f}pp':>16s}")
            else:
                cells.append(f"{('UP' if up else 'dn')+' (no trend)':>16s}")
        print(f"eps={cond[0]} {cond[1]}{cond[2]:8s}".ljust(22) + " " + " ".join(cells))
    print(f"  upticks per step point (of 6 conditions): "
          + ", ".join(f"k={k}: {v}/6" for k, v in upA.items()))

    # the ceiling's own trend-corrected tooth, for the elasticity
    print("\n  the density ceiling's own trend-corrected tooth, for comparison:")
    import rent_islands_design_check as DC
    dens = {k: LN2 - np.log(DC.N0(k)) / k for k in range(5, kmax + 1)}
    for k0 in (8, 12, 16, 20, 24, 28):
        if k0 + 3 > kmax:
            continue
        jumps = [np.log(dens[k0 + i + 1]) - np.log(dens[k0 + i]) for i in range(3)]
        t = (np.log(dens[k0]) - np.log(dens[k0 - 1])) - float(np.mean(jumps))
        print(f"    k={k0}: {100*t:+.3f} pp")

    # ---- H-DISSOC-2
    print("\nH-DISSOC-2: ARM A steps at k=28, ARM B (m=5 throughout 25..31) steps nowhere")
    for arm in ('A', 'B'):
        up = 0
        tot = 0
        for cond in CONDS:
            ks, ys = _series(rows, arm, cond)
            d = dict(zip(ks, ys))
            if 28 in d and 27 in d:
                tot += 1
                up += int(d[28] > d[27])
        print(f"  ARM {arm}: {up}/{tot} conditions tick up at k=28")
    return verdicts


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--q1', action='store_true')
    ap.add_argument('--ceiling', action='store_true')
    ap.add_argument('--hceiling', action='store_true')
    ap.add_argument('--q2', action='store_true')
    a = ap.parse_args()
    if a.q1:
        q1()
    if a.ceiling:
        ceiling_pass()
    if a.hceiling:
        h_ceiling()
    if a.q2:
        q2()
