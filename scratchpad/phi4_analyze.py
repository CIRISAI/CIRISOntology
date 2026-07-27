"""phi4_analyze.py — the pre-registered readouts for PHI4_RIDGE_PREREG.md.

Every number printed here is scored against a threshold written down in the
pre-registration before phi4_ridge.py existed.  Nothing is fitted that was not declared.
"""
import sys, os, json, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ising_field import share3, LN2
from phi4_ridge import (read_counts, binary_moments, moments_of, p8_from_moments,
                        fit_copula, mixture_null, share_b, BETA_NU, Y_H, U4_STAR)

np.seterr(all='ignore')

HERE = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(4242)


def load(name):
    p = os.path.join(HERE, name)
    return json.load(open(p)) if os.path.exists(p) else None


# =====================================================================================

def readout(row, thr, geom, nulls=True):
    c = row['counts'][thr][geom]
    d = read_counts(c, RNG, want_nulls=nulls)
    bm = binary_moments(c)
    d['bm'] = np.mean(bm['m']); d['bc'] = bm['c']; d['btau'] = bm['tau']
    d['dtau'] = bm['dtau']
    m = d['bm']
    d['k2'] = [x - m * m for x in bm['c']]
    d['k3'] = bm['tau'] - m * sum(bm['c']) + 2 * m ** 3
    cm = moments_of(row, geom)
    d['phi'] = cm['phi']; d['cphi'] = cm['c']; d['U'] = cm['U']; d['var'] = cm['var']
    return d


def ray(d, lam):
    """The parameter-free scaling ray: scale every connected binary moment by lam per
    spin, rebuild the 8-cell state exactly, evaluate the share."""
    m = d['bm'] * lam
    k2 = [x * lam ** 2 for x in d['k2']]
    k3 = d['k3'] * lam ** 3
    c = [x + m * m for x in k2]
    tau = k3 + m * sum(c) - 2 * m ** 3
    p = p8_from_moments([m, m, m], c[0], c[1], c[2], tau)
    if p.min() <= 0:
        return float('nan')
    return float(share3(p / p.sum())[0])


def parab_peak(x, y):
    """Sub-grid maximum by parabolic fit in ln x around the best grid point."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    ok = np.isfinite(y) & (x > 0)
    x, y = x[ok], y[ok]
    if len(x) < 3:
        return float('nan'), float('nan')
    i = int(np.argmax(y))
    i = min(max(i, 1), len(x) - 2)
    lx = np.log(x[i - 1:i + 2]); yy = y[i - 1:i + 2]
    a = np.polyfit(lx, yy, 2)
    if a[0] >= 0:
        return float(x[int(np.argmax(y))]), float(np.max(y))
    xs = -a[1] / (2 * a[0])
    return float(np.exp(xs)), float(np.polyval(a, xs))


def slope(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y) & (x > 0) & (y > 0)
    if ok.sum() < 2:
        return float('nan')
    return float(np.polyfit(np.log(x[ok]), np.log(y[ok]), 1)[0])


def verdict(val, pas, marg, name, target=None):
    if not np.isfinite(val):
        return 'UNGAUGED'
    return 'PASS' if val <= pas else ('MARGINAL' if val <= marg else 'FIRES')


# =====================================================================================

def do_binder():
    rows = load('phi4_binder.json')
    if not rows:
        print("  (no binder data yet)"); return None
    print("\n" + "=" * 84)
    print("S2 — BINDER CROSSING at h = 0.  U4* (3D Ising, periodic) = %.4f" % U4_STAR)
    print("=" * 84)
    Ls = sorted({r['L'] for r in rows})
    m2s = sorted({round(r['m2'], 5) for r in rows})
    tab = {}
    for r in rows:
        tab[(r['L'], round(r['m2'], 5))] = r['U4']
    print("   m2      " + "".join(f"  L={L:<7d}" for L in Ls))
    for m2 in m2s:
        print(f"  {m2:+.4f}  " + "".join(
            f"  {tab.get((L, m2), float('nan')):<9.4f}" for L in Ls))
    # crossings between consecutive L, by linear interpolation of U4(L1)-U4(L2)
    cross = []
    for a, b in zip(Ls[:-1], Ls[1:]):
        xs, ds = [], []
        for m2 in m2s:
            if (a, m2) in tab and (b, m2) in tab:
                xs.append(m2); ds.append(tab[(b, m2)] - tab[(a, m2)])
        xs, ds = np.array(xs), np.array(ds)
        sgn = np.where(np.diff(np.sign(ds)) != 0)[0]
        if len(sgn):
            i = sgn[0]
            t = -ds[i] / (ds[i + 1] - ds[i])
            mc = xs[i] + t * (xs[i + 1] - xs[i])
            u4 = tab[(a, xs[i])] + t * (tab[(a, xs[i + 1])] - tab[(a, xs[i])])
            cross.append((a, b, mc, u4))
            print(f"    crossing L={a:2d}/{b:<2d}  m_c^2 = {mc:+.4f}   U4 there = {u4:.4f}")
    if cross:
        mcs = [c[2] for c in cross]
        big = [c for c in cross if c[0] >= 12]
        mc = float(np.mean([c[2] for c in big])) if big else float(np.mean(mcs))
        print(f"\n  m_c^2 = {mc:+.4f}  (mean of the L>=12 crossings; spread "
              f"{np.std(mcs, ddof=1) if len(mcs) > 1 else 0:.4f} over all pairs)")
        print(f"  U4 at crossing = {np.mean([c[3] for c in cross]):.4f}  vs 3D Ising "
              f"{U4_STAR:.4f}  --> {'consistent' if abs(np.mean([c[3] for c in cross])-U4_STAR)<0.03 else 'DISCREPANT'}")
        return mc
    return None


def do_k1(rows, tag=''):
    print("\n" + "-" * 84)
    print(f"K1 — the sign-symmetry plumb line: h = 0 must read the floor {tag}")
    print("-" * 84)
    worst = 0.0; worstn = ''
    for r in rows:
        if r['h'] != 0.0:
            continue
        for thr in ('theta0', 'median'):
            for g in r['counts'][thr]:
                d = read_counts(r['counts'][thr][g], RNG, want_nulls=False)
                if abs(d['z']) > abs(worst):
                    worst = d['z']; worstn = f"L={r['L']} m2={r['m2']:+.3f} {thr}/{g}"
                print(f"    L={r['L']:2d} m2={r['m2']:+.3f} {thr:<7s} {g:<8s} "
                      f"raw={d['share_raw']:+.3e} excess={d['excess']:+.3e} "
                      f"z={d['z']:+6.2f}  N_eff={d['N_eff']:.2e}")
    print(f"  WORST |z| = {abs(worst):.2f} at {worstn}   -->  "
          f"{'K1 does not fire' if abs(worst) < 3 else 'K1 FIRES: RUN VOID'}")
    return abs(worst)


def do_ridge(mc=None):
    rows = load('phi4_ridge.json')
    if not rows:
        print("  (no ridge data yet)"); return
    print("\n" + "=" * 84)
    print("S3b — THE RIDGE.  theta=0 route, geometry colin-r (r = L/4) unless stated.")
    print("=" * 84)
    # S3c deep rows replace their S3b counterparts at the same (L, u).  Same estimator,
    # same thresholds, same grid points -- only 10-20x the independent samples.  Each
    # reading carries its OWN measured floor, so mixing sample sizes across L is legitimate
    # for the excess; it is recorded here rather than left for the reader to notice.
    deep = load('phi4_deep.json') or []
    extra = load('phi4_seeds32.json') or []
    DEEPL = sorted({r['L'] for r in deep})
    DEEPU = {(r['L'], round(r['u'], 6)) for r in deep}
    if extra:
        # S3d: independent seeds at the same (L, u) POOL.  The readout consumes per-replica
        # cell counts, so concatenating along the replica axis is exactly "more chains" --
        # not a longer chain, so it adds independent information rather than correlated
        # information, and F (measured across replicas) stays meaningful.  Continuum
        # moments are pooled the same way; scalars are averaged weighted by n_samp.
        by = {}
        for r in deep + extra:
            by.setdefault((r['L'], round(r['u'], 6)), []).append(r)
        pooled, npool = [], 0
        for k, grp in by.items():
            if len(grp) == 1:
                pooled.append(grp[0]); continue
            base = dict(grp[0])
            for t in base['counts']:
                for g in base['counts'][t]:
                    base['counts'][t][g] = sum(
                        (list(x['counts'][t][g]) for x in grp[1:]),
                        list(grp[0]['counts'][t][g]))
            for g in base['mom']:
                base['mom'][g] = sum((list(x['mom'][g]) for x in grp[1:]),
                                     list(grp[0]['mom'][g]))
            w = [x['n_samp'] for x in grp]; W = float(sum(w))
            for f in ('phi1', 'phi2', 'M2', 'M4'):
                base[f] = float(sum(x[f] * wi for x, wi in zip(grp, w)) / W)
            base['R'] = sum(x['R'] for x in grp)
            base['n_samp'] = grp[0]['n_samp']
            base['seeds'] = [x['seed'] for x in grp]
            pooled.append(base); npool += 1
        deep = pooled
        print(f"  S3d: {npool} (L, u) points pooled across independent seeds "
              f"({len(extra)} extra runs)")
        DEEPU = {(r['L'], round(r['u'], 6)) for r in deep}
        DEEPL = sorted({r['L'] for r in deep})
    if deep:
        key = {(r['L'], round(r['u'], 6)) for r in deep}
        rows = [r for r in rows if (r['L'], round(r['u'], 6)) not in key] + deep
        print(f"  S3c deep stage merged: {len(deep)} points at "
              f"L in {sorted({r['L'] for r in deep})} replace their S3b counterparts")
        for L in sorted({r['L'] for r in deep}):
            s = [r for r in deep if r['L'] == L][0]
            b = [r for r in load('phi4_ridge.json') if r['L'] == L][0]
            print(f"    L={L}: R {b['R']}->{s['R']}, n_samp {b['n_samp']}->{s['n_samp']} "
                  f"({s['R']*s['n_samp']/(b['R']*b['n_samp']):.0f}x independent samples)")
    Ls = sorted({r['L'] for r in rows})
    R = {}
    ROW = {}
    for r in rows:
        ROW[(r['L'], round(r['u'], 6))] = r
        for thr in ('theta0', 'median'):
            for g in r['counts'][thr]:
                R[(r['L'], round(r['u'], 6), thr, g)] = readout(r, thr, g, nulls=False)
    us = sorted({round(r['u'], 6) for r in rows if r['u'] > 0})

    # The Gaussian-copula null (K3) is an exact but expensive construction -- 8 trivariate
    # orthant integrals per fit, plus a 16-fold replica bootstrap for its own error bar.
    # It is therefore evaluated where K3 is scored (each L's peak on colin-r) and at the
    # two neighbouring grid points, rather than at all 650 readings.  Nothing is chosen
    # after the fact: the peak is located on the excess, which does not use the copula.
    for thr in ('theta0', 'median'):
        for L in Ls:
            xs = [u for u in us if (L, u, thr, 'colin-r') in R]
            if not xs:
                continue
            ys = [R[(L, u, thr, 'colin-r')]['excess'] for u in xs]
            i = int(np.argmax(ys))
            for j in range(max(0, i - 1), min(len(xs), i + 2)):
                k = (L, xs[j], thr, 'colin-r')
                R[k] = readout(ROW[(L, xs[j])], thr, 'colin-r', nulls=True)

    peaks = {}
    for thr in ('theta0', 'median'):
        print(f"\n  --- threshold: {thr} ---")
        print("    L     u*        h*          I_C^(3)     CF%      z     copula     "
              "excess/copula")
        for L in Ls:
            # Where the deep stage ran, the peak is located on the DEEP points only.  The
            # base points at the same L have floors 4-5x larger and would drag a parabola
            # fitted through both; mixing sample sizes is legitimate for a floor-subtracted
            # excess but not for a curvature fit.  Stated rather than left implicit.
            xs = [u for u in us if (L, u, thr, 'colin-r') in R]
            if L in DEEPL:
                xs = [u for u in xs if (L, u) in DEEPU]
            ys = [R[(L, u, thr, 'colin-r')]['excess'] for u in xs]
            ust, ypk = parab_peak(xs, ys)
            i = int(np.argmax(ys)) if len(ys) else 0
            d = R[(L, xs[i], thr, 'colin-r')] if xs else {}
            cop = d.get('copula_share', float('nan'))
            peaks[(L, thr)] = (ust, ypk, xs[i] if xs else float('nan'), d)
            print(f"    {L:<4d}  {ust:<8.3f}  {ust/L**Y_H:<10.3e}  {ypk:<10.3e}  "
                  f"{ypk/LN2*100:<7.4f}  {d.get('z', float('nan')):<6.1f} "
                  f"{cop:<10.3e} {d.get('excess', float('nan'))/cop if cop else float('nan'):<6.2f}")

    # ---- E1: does a ridge exist at all? ----
    print("\n  E1 — an interior maximum at h* > 0, exceeding its floor by >= 5 sigma at")
    print("       L <= 16.  (Interior-ness is NOT the finding: prereg section 8 states in")
    print("       advance that topology forces an interior maximum.  What E1 buys is the")
    print("       MAGNITUDE and its significance.)")
    for thr in ('theta0', 'median'):
        for L in Ls:
            ust, ypk, ub, d = peaks[(L, thr)]
            xs = [u for u in us if (L, u, thr, 'colin-r') in R]
            ys = [R[(L, u, thr, 'colin-r')]['excess'] for u in xs]
            interior = bool(xs) and 0 < int(np.argmax(ys)) < len(xs) - 1
            z = d.get('z', float('nan'))
            v = ('PASS' if (interior and z >= 5) else
                 'MARGINAL' if (interior and z >= 3) else 'FIRES')
            print(f"    {thr:<8s} L={L:<3d} interior={str(interior):<5s} "
                  f"peak z={z:7.1f}  I={ypk:.3e}  {v}"
                  + ("" if L <= 16 else "   (L > 16: not scored by E1)"))

    # ---- E2' peak locus ----
    print("\n  E2' — h* from the PEAK LOCUS (secondary; the 2D run showed this ruler is")
    print("        biased, because an entropy-gap maximiser is not a scaling observable)")
    print("        A size whose peak does not clear its floor has no peak LOCATION to")
    print("        contribute -- the quantity is undefined there, not merely noisy.  Both")
    print("        readings are printed: over every L, and over the L whose peak clears")
    print("        z >= 3.  The restriction is a statement about which sizes have the")
    print("        observable at all, and it is applied to the LOCUS, never to the peak")
    print("        height, which is reported at every L including where it is negative.")
    for thr in ('theta0', 'median'):
        Lv = [L for L in Ls if np.isfinite(peaks[(L, thr)][0])]
        hs = [peaks[(L, thr)][0] / L ** Y_H for L in Lv]
        s = slope(Lv, hs)
        Lg = [L for L in Lv if peaks[(L, thr)][3].get('z', -9) >= 3]
        hg = [peaks[(L, thr)][0] / L ** Y_H for L in Lg]
        sg = slope(Lg, hg) if len(Lg) >= 2 else float('nan')
        print(f"    {thr:<8s}  all L={Lv}: y_h = {-s:.4f}   "
              f"{verdict(abs(-s-Y_H),0.10,0.30,'')}")
        print(f"    {'':<8s}  z>=3 L={Lg}: y_h = {-sg:.4f}   "
              f"{verdict(abs(-sg-Y_H),0.10,0.30,'')}   (3D {Y_H:.4f}, 2D 1.8750)")
        print(f"    {'':<8s}  u* per L: " +
              " ".join(f"{L}:{peaks[(L,thr)][0]:.3f}" for L in Lv))

    # ---- E3 / E2 moment collapse ----
    print("\n  E3 — moment collapse at matched u, and E2 — y_h inferred from its drift")
    u0 = None
    # The matched u must be one where EVERY L is readable, so where the deep stage ran it
    # must be one of the deep grid points -- otherwise E4 would compare a deep L=16 against
    # a base L=32 that reads pure noise.
    cand = [u for u in us if all((L, u, 'theta0', 'colin-r') in R for L in Ls)
            and all((L, u) in DEEPU for L in DEEPL)]
    if cand:
        mid = [peaks[(L, 'theta0')][0] for L in Ls if np.isfinite(peaks[(L, 'theta0')][0])]
        tgt = float(np.median(mid)) if mid else cand[len(cand) // 2]
        u0 = min(cand, key=lambda u: abs(math.log(u / tgt)))
    if u0:
        print(f"    matched at u = {u0:.4f}")
        # The 2D sibling's lesson, carried forward as an instruction: the moment route's
        # expansion parameter is the PAIR correlation, so rho is quoted beside every
        # moment reading and decides whether the route is a meter or only a detector.
        print("    rho(r) = c(r)/var(phi) at this u, the moment route's expansion")
        print("    parameter (2D at criticality: 0.56-0.66, i.e. the route was a DETECTOR")
        print("    only and overstated the share by 25-64x):")
        for L in Ls:
            d = R.get((L, u0, 'theta0', 'colin-r'))
            if d:
                print(f"      L={L:<3d} rho = {d['cphi'][0]/d['var']:+.4f}   "
                      f"{'SMALL: the route is a meter here' if abs(d['cphi'][0]/d['var']) < 0.3 else 'O(1): DETECTOR ONLY'}")
        names = [('m', 'bm', BETA_NU), ('kappa2', 'k2', 2 * BETA_NU),
                 ('kappa3', 'k3', 3 * BETA_NU), ('U_phi', 'U', 3 * BETA_NU),
                 ('phi', 'phi', BETA_NU)]
        resc = {}
        for nm, key, dlt in names:
            vals = []
            for L in Ls:
                d = R.get((L, u0, 'theta0', 'colin-r'))
                if d is None:
                    vals.append(float('nan')); continue
                v = d[key]
                v = np.mean(v) if isinstance(v, list) else v
                vals.append(v * L ** dlt)
            resc[nm] = vals
            drift = abs(vals[-1] / vals[-2] - 1) * 100 if len(vals) > 1 and vals[-2] else float('nan')
            print(f"      {nm:<7s} L^{dlt:<6.4f}: " +
                  " ".join(f"{v:+.5f}" for v in vals) +
                  f"   drift(last pair) {drift:.2f}%  "
                  f"{verdict(drift, 3.0, 8.0, nm)}")
        # The exponents READ OFF DIRECTLY, which is the same E3 data inverted the other
        # way and is far better conditioned than E2's ruler: 2D and 3D differ by 4x in
        # Delta_sigma, so this discriminates the classes without needing to resolve
        # either one precisely.  Derived reading of E3, not a new stake.
        print("\n    E3 inverted — the exponents read directly off the moments at matched")
        print("    u (d ln X / d ln L).  3D and 2D predictions differ by 4x here, so this")
        print("    separates the CLASSES even where it cannot pin an exponent:")
        pred2d = {'m': -0.125, 'phi': -0.125, 'kappa2': -0.25, 'kappa3': -0.375,
                  'U_phi': -0.375}
        for nm, key, dlt in names:
            Lv, Xv = [], []
            for L in Ls:
                d = R.get((L, u0, 'theta0', 'colin-r'))
                if d is None:
                    continue
                v = d[key]
                v = np.mean(v) if isinstance(v, list) else v
                Lv.append(L); Xv.append(abs(v))
            if len(Lv) < 2:
                continue
            s_all = slope(Lv, Xv)
            s_big = slope(Lv[-2:], Xv[-2:])
            p3, p2 = -dlt, pred2d[nm]
            which = ('3D' if abs(s_big - p3) < abs(s_big - p2) else '2D')
            print(f"      {nm:<7s} measured {s_big:+.4f} (largest pair) "
                  f"{s_all:+.4f} (all L)   3D predicts {p3:+.4f}, 2D predicts {p2:+.4f}"
                  f"   -> {which}, off by {abs(s_big-p3):.4f} from 3D")
        # ...and y_h read through hyperscaling, beta/nu + y_h = d, which the
        # pre-registration names as its own internal check.  This inverts the SAME E3 data
        # as E2 does but divides by nothing, so it does not inherit E2's conditioning
        # problem.  Derived reading of pre-registered quantities; not a new stake.
        print("\n    y_h via hyperscaling (beta/nu + y_h = d = 3, the prereg's own")
        print("    internal check), from the cumulants' measured exponents over all L:")
        for nm, key, dlt in names:
            Lv, Xv = [], []
            for L in Ls:
                d = R.get((L, u0, 'theta0', 'colin-r'))
                if d is None:
                    continue
                v = d[key]
                Lv.append(L); Xv.append(abs(np.mean(v) if isinstance(v, list) else v))
            if len(Lv) < 3:
                continue
            order = {'m': 1, 'phi': 1, 'kappa2': 2, 'kappa3': 3, 'U_phi': 3}[nm]
            bn = -slope(Lv, Xv) / order
            print(f"      {nm:<7s} beta/nu = {bn:.4f} (3D 0.5181, 2D 0.1250)  ->  "
                  f"y_h = {3-bn:.4f}  (3D {Y_H:.4f}, 2D 1.8750)   "
                  f"{'consistent with 3D' if abs(3-bn-Y_H) < 0.15 else 'off'}")

        # y_h from the drift, using d ln X / d ln u measured at fixed L
        print("\n    E2 (PRIMARY) — y_h from the collapse:")
        print("      CAVEAT, measured not argued (phi4_e2_estimator_test.py): planting a")
        print("      known y_h on this same u grid recovers it exactly with pure scaling")
        print("      and to 0.03 for the 2D value -- but adding a correction to scaling")
        print("      (1 + a L^-0.832) of amplitude a = +-0.2 to +-0.5 scatters the answer")
        print("      by 0.17 to 0.44.  E2's +-0.10 PASS band is therefore FINER THAN THE")
        print("      RULER at these lattice sizes.  What the ruler can still do is tell")
        print("      2.4819 from 1.8750, a gap of 0.61.")
        ys = []
        for nm, key, dlt in names:
            L1, L2 = Ls[-2], Ls[-1]
            d1 = R.get((L1, u0, 'theta0', 'colin-r')); d2 = R.get((L2, u0, 'theta0', 'colin-r'))
            if d1 is None or d2 is None:
                continue
            i = us.index(u0)
            if i == 0 or i + 1 >= len(us):
                continue
            def val(L, u):
                dd = R.get((L, u, 'theta0', 'colin-r'))
                if dd is None:
                    return float('nan')
                v = dd[key]
                return np.mean(v) if isinstance(v, list) else v
            a, b = val(L2, us[i - 1]), val(L2, us[i + 1])
            if not (np.isfinite(a) and np.isfinite(b)) or a * b <= 0:
                continue
            dlnXdlnu = math.log(abs(b / a)) / math.log(us[i + 1] / us[i - 1])
            v1 = val(L1, u0) * L1 ** dlt; v2 = val(L2, u0) * L2 ** dlt
            if v1 * v2 <= 0 or abs(dlnXdlnu) < 0.05:
                print(f"      {nm:<7s}  |dlnX/dlnu| = {abs(dlnXdlnu):.3f} < 0.05 -> ungauged")
                continue
            yh = Y_H + math.log(v2 / v1) / (dlnXdlnu * math.log(L2 / L1))
            ys.append(yh)
            print(f"      {nm:<7s}  dlnX/dlnu = {dlnXdlnu:+.4f}   inferred y_h = {yh:.4f}")
        if ys:
            ym, ysd = float(np.mean(ys)), float(np.std(ys, ddof=1)) if len(ys) > 1 else 0.0
            print(f"      --> y_h = {ym:.4f} +- {ysd:.4f}   (3D {Y_H:.4f} | 2D 1.8750)   "
                  f"{verdict(abs(ym-Y_H),0.10,0.25,'')}")

    # ---- E4 amplitude ----
    print("\n  E4 — amplitude exponent at matched u (predicted -6*beta/nu = "
          f"{-6*BETA_NU:.4f}; the 2D run's analogous prediction FIRED and was explained)")
    for thr in ('theta0', 'median'):
        if not u0:
            break
        Lv = [L for L in Ls if (L, u0, thr, 'colin-r') in R]
        Iv = [R[(L, u0, thr, 'colin-r')]['excess'] for L in Lv]
        Ev = [max(R[(L, u0, thr, 'colin-r')]['floor_sd'],
                  R[(L, u0, thr, 'colin-r')]['boot_sd']) for L in Lv]
        print(f"    {thr:<8s} " + " ".join(f"L={L}:{v:.3e}+-{e:.1e}"
                                           for L, v, e in zip(Lv, Iv, Ev)))
        # Every consecutive pair is printed, not only the flattering ones: a two-point
        # slope over a factor of 2 in L is the average of its sub-intervals, so if the
        # sub-intervals scatter about the prediction and their average lands on it, that
        # is scatter averaging out and must be visible as such.
        for i in range(len(Lv) - 1):
            s = slope(Lv[i:i + 2], Iv[i:i + 2])
            # error on a two-point log-log slope, from the two readings' own error bars
            if Iv[i] > 0 and Iv[i + 1] > 0:
                ds = math.hypot(Ev[i] / Iv[i], Ev[i + 1] / Iv[i + 1]) / \
                    math.log(Lv[i + 1] / Lv[i])
            else:
                ds = float('nan')
            print(f"        local slope L={Lv[i]}->{Lv[i+1]}: {s:+.3f} +- {ds:.3f}"
                  f"   (3D predicts {-6*BETA_NU:+.3f}; 2D's analogue was FLAT)")
        # the largest pair BOTH of whose readings clear their floor -- a slope through a
        # point consistent with zero is not a measurement of an exponent
        Lg = [L for L in Lv if R[(L, u0, thr, 'colin-r')]['z'] >= 3]
        if len(Lg) >= 2:
            Ig = [R[(L, u0, thr, 'colin-r')]['excess'] for L in Lg]
            Eg = [max(R[(L, u0, thr, 'colin-r')]['floor_sd'],
                      R[(L, u0, thr, 'colin-r')]['boot_sd']) for L in Lg]
            s = slope(Lg[-2:], Ig[-2:])
            ds = math.hypot(Eg[-2] / Ig[-2], Eg[-1] / Ig[-1]) / math.log(Lg[-1] / Lg[-2])
            print(f"      largest READABLE pair L={Lg[-2]}->{Lg[-1]}: {s:+.4f} +- {ds:.4f}"
                  f"  -> {verdict(abs(s+6*BETA_NU), 0.5, 1.1, '')}")
            print(f"      (readable sizes at this u: {Lg})")
        # The pre-registered window is 16 -> 32; report it explicitly whether or not it is
        # the largest available pair, and say when it is unreadable.
        if 16 in Lv and 32 in Lv:
            i16, i32 = Lv.index(16), Lv.index(32)
            s = slope([16, 32], [Iv[i16], Iv[i32]])
            ds = (math.hypot(Ev[i16] / Iv[i16], Ev[i32] / Iv[i32]) / math.log(2)
                  if Iv[i16] > 0 and Iv[i32] > 0 else float('nan'))
            print(f"      PREREG WINDOW L=16->32: {s:+.4f} +- {ds:.4f}   "
                  f"{verdict(abs(s+6*BETA_NU), 0.5, 1.1, '')}")

    # ---- E4' the ray ----
    print("\n  E4' — the parameter-free scaling ray (rescale connected binary moments by")
    print("        (L2/L1)^(-beta/nu) per spin, rebuild the state, evaluate exactly)")
    if u0:
        for thr in ('theta0', 'median'):
            Lv = [L for L in Ls if (L, u0, thr, 'colin-r') in R]
            for i in range(len(Lv) - 1):
                L1, L2 = Lv[i], Lv[i + 1]
                pred = ray(R[(L1, u0, thr, 'colin-r')], (L2 / L1) ** (-BETA_NU))
                meas = R[(L2, u0, thr, 'colin-r')]['excess']
                res = (pred / meas - 1) * 100 if meas else float('nan')
                print(f"    {thr:<8s} {L1:2d}->{L2:<2d}  ray {pred:.4e}  measured "
                      f"{meas:.4e}  residual {res:+.2f}%   {verdict(abs(res),5,15,'')}")

    # ---- E5 h^2 gate ----
    print("\n  E5 — the h^2 gate at small h (a GATE: it follows from Z2 + analyticity")
    print("       whatever the mechanism, so it is not evidence for anything)")
    print("       Scored as pre-registered on the FOUR SMALLEST u, and then again on the")
    print("       smallest u the instrument can actually read (z >= 5, below the peak).")
    print("       The second window is POST-HOC and labelled: it is reported because the")
    print("       pre-registered window turns out to sit under the estimator floor, where")
    print("       the readings are consistent with zero and a log-log slope is undefined.")
    for L in Ls:
        xs = [u for u in us[:4] if (L, u, 'theta0', 'colin-r') in R]
        ys = [R[(L, u, 'theta0', 'colin-r')]['excess'] for u in xs]
        zs = [R[(L, u, 'theta0', 'colin-r')]['z'] for u in xs]
        s = slope(xs, ys)
        ipk = int(np.argmax([R[(L, u, 'theta0', 'colin-r')]['excess'] for u in us
                             if (L, u, 'theta0', 'colin-r') in R]))
        gx = [u for j, u in enumerate(us) if (L, u, 'theta0', 'colin-r') in R
              and j < ipk and R[(L, u, 'theta0', 'colin-r')]['z'] >= 5]
        gy = [R[(L, u, 'theta0', 'colin-r')]['excess'] for u in gx]
        sg = slope(gx, gy) if len(gx) >= 2 else float('nan')
        print(f"    L={L:<3d} prereg window (4 smallest u, z = "
              f"{','.join('%.1f' % z for z in zs)}): slope {s:+.4f} "
              f"{verdict(abs(s-2),0.05,0.15,'')}")
        print(f"          post-hoc window ({len(gx)} pts with z>=5 below the peak): "
              f"slope {sg:+.4f}  {verdict(abs(sg-2),0.05,0.15,'')}")
    print("\n    The same gate read through Delta_tau, which has no estimator floor.")
    print("    The prereg's own Step A is I_C^(3) = (1/128)[sum p_s^-1](Delta_tau)^2 +")
    print("    O(Delta_tau^3), so Delta_tau ~ h^1 IS the h^2 gate, measured on a moment")
    print("    instead of on an entropy difference.  The 2D sibling read it this way too")
    print("    (Delta_tau ~ h^1.000).  This is why the direct route above is unreadable:")
    print("    the h^2 regime is squeezed between the estimator floor below and the peak")
    print("    above, and at these sample sizes there is no window left between them.")
    for L in Ls:
        xs = [u for u in us[:6] if (L, u, 'theta0', 'colin-r') in R]
        ys = [abs(R[(L, u, 'theta0', 'colin-r')]['dtau']) for u in xs]
        s = slope(xs, ys)
        xs4 = xs[:4]; ys4 = ys[:4]
        print(f"    L={L:<3d} d ln|Delta_tau| / d ln u = {slope(xs4,ys4):+.4f} (4 smallest u)"
              f"  {s:+.4f} (6 smallest)   predicted 1.0000   "
              f"{verdict(abs(slope(xs4,ys4)-1),0.025,0.075,'')}")

    # ---- E6 geometry ----
    print("\n  E6 — separated vs local at the ridge (2D: separated won by ~4x)")
    if u0:
        gs = ['star', 'Lcorner', 'colin1', 'colin-r', 'far']
        print("    L    " + "".join(f"{g:<12s}" for g in gs))
        for L in Ls:
            vals = [R[(L, u0, 'theta0', g)]['excess'] if (L, u0, 'theta0', g) in R
                    else float('nan') for g in gs]
            print(f"    {L:<4d} " + "".join(f"{v:<12.3e}" for v in vals))
            best = gs[int(np.nanargmax(vals))] if np.any(np.isfinite(vals)) else '?'
            print(f"         largest: {best}")

    # ---- E8 U/dtau ----
    print("\n  E8 — U/Delta_tau as h -> 0 (2D: tends to 6.6-12.1, NOT to 1; the")
    print("       'connected info ~ (connected correlator)^2' route fails at criticality)")
    for L in Ls:
        row = []
        for u in us[:4]:
            d = R.get((L, u, 'theta0', 'colin-r'))
            if d and abs(d['dtau']) > 1e-12:
                row.append(d['U'] / d['dtau'])
        if row:
            print(f"    L={L:<3d} U/dtau at the 4 smallest u: " +
                  " ".join(f"{v:+.3f}" for v in row) +
                  f"   rho(r)={R[(L, us[0], 'theta0', 'colin-r')]['cphi'][0]/R[(L, us[0], 'theta0', 'colin-r')]['var']:+.3f}")

    # ---- K3 the central gate ----
    print("\n" + "-" * 84)
    print("K3 — BINARIZATION ARTIFACT.  The measured ridge must exceed its matched")
    print("     pairwise-continuum (Gaussian-copula) surrogate by >= 3 sigma.")
    print("-" * 84)
    print("  NOTE on the median column: by share_eq_zero_of_signSymmetric the Gaussian")
    print("  copula binarized AT ITS OWN MEDIAN has share exactly zero, so that baseline")
    print("  sits at roundoff (1e-11..1e-13) and the excess/copula RATIO there is set by")
    print("  floating point, not by physics.  The meaningful number in that column is z,")
    print("  whose denominator is the measured estimator floor.  The ratio is printed")
    print("  because suppressing it would hide which column is which.")
    for thr in ('theta0', 'median'):
        print(f"  {thr}:")
        for L in Ls:
            ust, ypk, ub, d = peaks[(L, thr)]
            cop = d.get('copula_share', float('nan'))
            csd = d.get('copula_sd', float('nan'))
            sd = max(d.get('floor_sd', 0), d.get('boot_sd', 0),
                     csd if np.isfinite(csd) else 0)
            z = (d['excess'] - cop) / sd if sd > 0 else float('nan')
            print(f"    L={L:<3d} excess={d['excess']:.4e}  copula={cop:.4e}  "
                  f"ratio={d['excess']/cop if cop else float('nan'):6.2f}  z={z:+7.2f}  "
                  f"{'clears' if z >= 3 else 'DOES NOT CLEAR'}")

    # ---- K4 mixture ----
    print("\n" + "-" * 84)
    print("K4 — MIXTURE NULL (two-component Gaussian, each component pairwise-only).")
    print("     Pre-registered adjudication: reproducing the share IDENTIFIES the")
    print("     mechanism as a single latent binary collective mode; it does not kill")
    print("     the ridge's existence, it bounds its interpretation.")
    print("-" * 84)
    for L in Ls:
        for thr in ('theta0',):
            ust, ypk, ub, d = peaks[(L, thr)]
            row = [r for r in rows if r['L'] == L
                   and abs(r['u'] - ub) <= 1e-6 * max(1.0, abs(ub))]
            if not row:
                continue
            if d.get('z', -9) < 3:
                print(f"    L={L:<3d} peak z = {d.get('z', float('nan')):.2f} < 3: below "
                      f"the instrument's reach, not fitted")
                continue
            cnt = np.asarray(row[0]['counts'][thr]['colin-r'], float).sum(axis=0)
            p = cnt / cnt.sum()
            try:
                # the vectorized copula (phi4_fastcop.py), gated at 2.2e-15 against the
                # adaptive-quadrature implementation and 283x faster -- the slow one costs
                # 2.7 s per evaluation and this fit needs ~20000 of them
                from phi4_k4 import mixture_fast
                m, prm, rms = mixture_fast(p)
                sm = float(share3(m)[0])
                print(f"    L={L:<3d} measured raw={d['share_raw']:.4e}  mixture="
                      f"{sm:.4e}  ratio={sm/d['share_raw']:5.2f}  fit rms={rms:.2e}  "
                      f"w={prm['w']:.3f} mu={prm['mu']:.3f}")
            except Exception as e:
                print(f"    L={L}: mixture fit failed: {e}")

    # ---- honesty ledger ----
    tot = sum(1 for k in R if k[3] == 'colin-r')
    bad = sum(1 for k in R if k[3] == 'colin-r' and not R[k].get('trustworthy', True))
    Fs = [R[k]['F_max'] for k in R if k[3] == 'colin-r']
    Ne = [R[k]['N_eff'] for k in R if k[3] == 'colin-r']
    print("\n" + "-" * 84)
    print(f"  occupancy sluice: {bad}/{tot} colin-r readings excluded as untrustworthy")
    print(f"  variance inflation F: median {np.median(Fs):.1f}  max {np.max(Fs):.3g}")
    print(f"  N_eff: min {np.min(Ne):.2e}  median {np.median(Ne):.2e}")
    print("\n  THE INSTRUMENT'S REACH, per L, at the peak (this is the run's binding")
    print("  limitation and it is reported whatever the verdicts say):")
    print(f"    {'L':>4s} {'R*n_samp':>10s} {'N raw':>10s} {'F':>9s} {'N_eff':>10s} "
          f"{'N_eff/(R*n)':>12s} {'floor sd':>10s} {'peak excess':>12s} {'z':>7s}")
    for L in Ls:
        ust, ypk, ub, d = peaks[(L, 'theta0')]
        r0 = ROW.get((L, ub))
        rn = (r0['R'] * r0['n_samp']) if r0 else float('nan')
        print(f"    {L:>4d} {rn:>10.3g} {d['N']:>10.3g} {d['F_max']:>9.3g} "
              f"{d['N_eff']:>10.3g} {d['N_eff']/rn:>12.2f} "
              f"{max(d['floor_sd'], d['boot_sd']):>10.3g} {d['excess']:>12.3e} "
              f"{d['z']:>7.2f}")
    print("  N_eff/(R*n_samp) ~ 1 says each (replica, configuration) pair carries about")
    print("  ONE independent triple: near criticality an L^3 lattice is one correlated")
    print("  blob, so the L^3 spatial translates are not L^3 independent samples.  This,")
    print("  not the physics, is what sets where the ridge stops being readable.")
    do_k1(rows, '(ridge stage, h=0 column)')
    return R, peaks, u0


# =====================================================================================
# The stages the first pass left without a readout: S3a, S4/E7, S5, S6/K7, S7/K2, K5.
# =====================================================================================

def do_hscan():
    rows = load('phi4_hscan.json')
    if not rows:
        print("  (no hscan data)"); return None
    print("\n" + "=" * 84)
    print("S3a — BROAD h SCAN at L = 8, m2 = m_c^2.  colin-r (r = L/4).")
    print("=" * 84)
    out = {}
    for thr in ('theta0', 'median'):
        print(f"\n  --- {thr} ---")
        print(f"    {'h':>10s} {'u':>9s} {'excess':>11s} {'z':>7s} {'copula':>11s} "
              f"{'ratio':>8s} {'min cell':>9s}")
        us, ys = [], []
        for r in rows:
            d = readout(r, thr, 'colin-r', nulls=True)
            u = r['h'] * r['L'] ** Y_H
            cop = d.get('copula_share', float('nan'))
            if u > 0:
                us.append(u); ys.append(d['excess'])
            print(f"    {r['h']:10.3e} {u:9.4f} {d['excess']:+11.3e} {d['z']:7.2f} "
                  f"{cop:11.3e} {d['excess']/cop if cop else float('nan'):8.1f} "
                  f"{d['min_cell']:9.2e}")
        up, yp = parab_peak(us, ys)
        out[thr] = (up, yp)
        print(f"    -> interior peak at u* = {up:.4f}  (h* = {up/8**Y_H:.3e})  "
              f"I_C^(3) = {yp:.3e} nats")
    return out


def do_offcrit():
    """E7 — the ridge must be CRITICAL: the peak at t = 0 must beat t = +-0.5 by >= 3x."""
    rows = load('phi4_offcrit.json')
    rid = load('phi4_ridge.json')
    if not rows or not rid:
        print("\n  (E7: no off-critical data)"); return
    print("\n" + "=" * 84)
    print("E7 — IS THE RIDGE CRITICAL?  peak(t=0) vs peak(m_c^2 +- 0.5), PASS >= 3x")
    print("=" * 84)
    for thr in ('theta0', 'median'):
        print(f"\n  --- {thr} ---")
        print(f"    {'L':>4s} {'peak t=0':>11s} {'peak ord':>11s} {'peak dis':>11s} "
              f"{'ratio vs worst':>15s}   verdict")
        for L in sorted({r['L'] for r in rows}):
            def pk(rs, col=None):
                xs, ys = [], []
                for r in rs:
                    if r['L'] != L or r['u'] <= 0:
                        continue
                    if col is not None and r.get('col') != col:
                        continue
                    xs.append(r['u'])
                    ys.append(readout(r, thr, 'colin-r', nulls=False)['excess'])
                return parab_peak(xs, ys)[1] if len(xs) >= 3 else float('nan')
            c0 = pk(rid); co = pk(rows, 'ord'); cd = pk(rows, 'dis')
            worst = max(co, cd)
            rat = c0 / worst if worst > 0 else float('inf')
            v = 'PASS' if rat >= 3 else ('MARGINAL' if rat >= 1.5 else 'FIRES')
            print(f"    {L:>4d} {c0:11.3e} {co:11.3e} {cd:11.3e} {rat:15.2f}   {v}")


def do_sep():
    rows = load('phi4_sep.json')
    if not rows:
        print("\n  (no separation scan)"); return
    print("\n" + "=" * 84)
    print("S5 — SEPARATION SCAN on colin-r at the ridge peak: I_C^(3) vs r")
    print("=" * 84)
    for thr in ('theta0', 'median'):
        print(f"\n  --- {thr} ---")
        for r in rows:
            L = r['L']
            # r = L/2 is DEGENERATE, not a data point: the triple is
            # (0, r, 2r) on a ring of size L, so 2r = L wraps the third site exactly onto
            # the first and the "triple" is a pair.  Its share is identically zero by
            # construction and it is dropped rather than plotted as a fall-off.
            gs = [g for g in sorted(r['counts'][thr], key=lambda s: int(s[1:]))
                  if (2 * int(g[1:])) % L != 0]
            vals = [readout(r, thr, g, nulls=False)['excess'] for g in gs]
            if not vals or not np.any(np.isfinite(vals)):
                continue
            best = gs[int(np.nanargmax(vals))]
            mx = max(vals)
            print(f"    L={L:<3d} " + " ".join(f"r{g[1:]}:{v:.2e}" for g, v in zip(gs, vals)))
            print(f"          peak at {best} (r/L = {int(best[1:])/L:.3f}); "
                  + (f"r=1 is {vals[0]/mx:.3f} of it" if mx > 0 else
                     "peak is not positive: this L is below the instrument's reach"))


def do_bsweep():
    """K7 — coarse-graining stability.  Existence from every stage that has it;
    LOCATION from the three-u stage, at its own factor-1.7 resolution."""
    rows = load('phi4_bsweep.json')
    r3 = load('phi4_bsweep3.json')
    if not rows and not r3:
        print("\n  (no b sweep)"); return
    print("\n" + "=" * 84)
    print("K7 — COARSE-GRAINING / THRESHOLD STABILITY.  A ridge that exists at only one")
    print("     b was minted by the bins.  Magnitudes are EXPECTED to differ with b.")
    print("=" * 84)
    if rows:
        print("\n  existence at the peak (excess over the N_eff floor, and its z):")
        ths = sorted(rows[0]['counts'].keys())
        print(f"    {'L':>4s} " + "".join(f"{t:>13s}" for t in ths))
        for r in rows:
            cells = []
            for t in ths:
                d = read_counts(r['counts'][t]['colin-r'], RNG, want_nulls=False)
                cells.append(f"{d['excess']:.2e}/{d['z']:.0f}")
            print(f"    {r['L']:>4d} " + "".join(f"{c:>13s}" for c in cells))
        print("    (cell = excess / z.  b=3 and b=4 read by IPF with its dual bracket;")
        print("     any bracket wider than 10% of the reading is ungauged, flagged below.)")
        wide = []
        for r in rows:
            for t in ths:
                d = read_counts(r['counts'][t]['colin-r'], RNG, want_nulls=False)
                br = d.get('bracket', 0.0)
                if np.isfinite(br) and abs(d['share_raw']) > 0 and \
                        abs(br) > 0.10 * abs(d['share_raw']):
                    wide.append(f"L={r['L']} {t} bracket={br:.2e} vs {d['share_raw']:.2e}")
        print(f"    IPF/dual bracket wider than 10%: "
              f"{len(wide) if wide else 'none'}" + ("  " + "; ".join(wide) if wide else ""))
    if r3:
        print("\n  LOCATION at factor-1.7 resolution (which of u0/1.7, u0, u0*1.7 wins):")
        ths = sorted(r3[0]['counts'].keys())
        for L in sorted({r['L'] for r in r3}):
            sub = sorted([r for r in r3 if r['L'] == L], key=lambda r: r['u'])
            line = []
            for t in ths:
                v = [read_counts(r['counts'][t]['colin-r'], RNG,
                                 want_nulls=False)['excess'] for r in sub]
                line.append(f"{t}:{['lo','mid','hi'][int(np.argmax(v))]}")
            print(f"    L={L:<3d} " + "  ".join(line))
        print("    All thresholds agreeing on the same bin is K7's location leg passing")
        print("    at the only resolution this stage has; it does not resolve finer.")


def do_controls():
    """K2 (free field) and K1 (h = 0, with the global flip on AND off)."""
    rows = load('phi4_controls.json')
    if not rows:
        print("\n  (no controls)"); return
    print("\n" + "=" * 84)
    print("S7 / K2 — THE FREE FIELD.  lambda = 0 is Gaussian, so the MEDIAN route's share")
    print("     is EXACTLY zero at every h by share_eq_zero_of_signSymmetric.  theta=0 is")
    print("     NOT protected there and its reading IS the binarization artifact, measured")
    print("     on the one case where the truth is known.")
    print("=" * 84)
    fr = [r for r in rows if r.get('col') == 'free']
    if fr:
        print(f"    {'m2':>6s} {'h':>6s} {'geom':>8s} {'median excess':>14s} {'z':>7s} "
              f"{'theta0 excess':>14s} {'z':>7s}")
        wm = 0.0
        for r in fr:
            for g in ('colin1', 'colin-r'):
                dm = read_counts(r['counts']['median'][g], RNG, want_nulls=False)
                dt = read_counts(r['counts']['theta0'][g], RNG, want_nulls=False)
                wm = max(wm, abs(dm['z']))
                print(f"    {r['m2']:6.2f} {r['h']:6.2f} {g:>8s} {dm['excess']:14.3e} "
                      f"{dm['z']:7.2f} {dt['excess']:14.3e} {dt['z']:7.2f}")
        print(f"    WORST |z| on the protected (median) route = {wm:.2f}  -->  "
              f"{'K2 does not fire' if wm < 3 else 'K2 FIRES: median route VOID'}")
    k1 = [r for r in rows if str(r.get('col', '')).startswith('k1')]
    if k1:
        print("\n  K1 at m_c^2, the HARD version: the global sign flip switched OFF, so the")
        print("  test is no longer guaranteed by construction — it asks whether the chain")
        print("  itself visits both phases.")
        for tag in ('k1flip', 'k1noflip'):
            sub = [r for r in k1 if r['col'] == tag]
            if sub:
                do_k1(sub, f'({tag})')


def do_dose():
    """K5 — the peak must not move with burn-in or thinning."""
    rows = load('phi4_dose.json')
    if not rows:
        print("\n  (no dose data)"); return
    print("\n" + "=" * 84)
    print("K5 — DOSE-vs-RATE.  h* must be invariant to burn-in x4 and thinning gap x4.")
    print("     This is the check the gap-cap amendment owes: if capping the gap at 200")
    print("     sweeps mattered, gap x4 would move the answer.")
    print("=" * 84)
    for L in sorted({r['L'] for r in rows}):
        print(f"\n  L = {L}")
        print(f"    {'burn':>5s} {'gap':>5s} {'tau':>6s} " +
              "".join(f"{'u=%.2f' % u:>12s}" for u in
                      sorted({r['u'] for r in rows if r['L'] == L})) + f"{'argmax':>9s}")
        us = sorted({r['u'] for r in rows if r['L'] == L})
        base = None
        for bm in (1.0, 4.0):
            for gm in (1.0, 4.0):
                sub = [r for r in rows if r['L'] == L and r['burn_mult'] == bm
                       and r['gap_mult'] == gm]
                if not sub:
                    continue
                sub = sorted(sub, key=lambda r: r['u'])
                v = [readout(r, 'theta0', 'colin-r', nulls=False)['excess'] for r in sub]
                am = us[int(np.argmax(v))]
                if base is None:
                    base = am
                print(f"    {bm:5.0f} {gm:5.0f} {sub[0]['tau_int']:6.0f} " +
                      "".join(f"{x:12.3e}" for x in v) + f"{am:9.2f}"
                      + ("" if am == base else "   <-- MOVED"))


def main():
    print("=" * 84)
    print("PHI4 RIDGE — pre-registered readouts (PHI4_RIDGE_PREREG.md, commit 7ea57ea)")
    print("=" * 84)
    # internal consistency: the 8-cell state must round-trip through its moments
    err = 0.0
    for _ in range(200):
        p = RNG.random(8); p = p / p.sum()
        bm = binary_moments([list((p * 1e9).astype(int))])
        q = p8_from_moments(bm['m'], bm['c'][0], bm['c'][1], bm['c'][2], bm['tau'])
        err = max(err, float(np.abs(q - p).max()))
    print(f"  [consistency] 8-cell round-trip through its moments: {err:.2e}")
    mc = do_binder()
    do_hscan()
    if load('phi4_ridge.json'):
        do_ridge(mc)
    do_offcrit()
    do_sep()
    do_bsweep()
    do_controls()
    do_dose()
    return 0


if __name__ == '__main__':
    sys.exit(main())
