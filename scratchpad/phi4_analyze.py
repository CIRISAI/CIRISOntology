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
    Ls = sorted({r['L'] for r in rows})
    R = {}
    for r in rows:
        for thr in ('theta0', 'median'):
            for g in r['counts'][thr]:
                R[(r['L'], round(r['u'], 6), thr, g)] = readout(
                    r, thr, g, nulls=(g == 'colin-r'))
    us = sorted({round(r['u'], 6) for r in rows if r['u'] > 0})

    peaks = {}
    for thr in ('theta0', 'median'):
        print(f"\n  --- threshold: {thr} ---")
        print("    L     u*        h*          I_C^(3)     CF%      z     copula     "
              "excess/copula")
        for L in Ls:
            xs = [u for u in us if (L, u, thr, 'colin-r') in R]
            ys = [R[(L, u, thr, 'colin-r')]['excess'] for u in xs]
            ust, ypk = parab_peak(xs, ys)
            i = int(np.argmax(ys)) if len(ys) else 0
            d = R[(L, xs[i], thr, 'colin-r')] if xs else {}
            cop = d.get('copula_share', float('nan'))
            peaks[(L, thr)] = (ust, ypk, xs[i] if xs else float('nan'), d)
            print(f"    {L:<4d}  {ust:<8.3f}  {ust/L**Y_H:<10.3e}  {ypk:<10.3e}  "
                  f"{ypk/LN2*100:<7.4f}  {d.get('z', float('nan')):<6.1f} "
                  f"{cop:<10.3e} {d.get('excess', float('nan'))/cop if cop else float('nan'):<6.2f}")

    # ---- E2' peak locus ----
    print("\n  E2' — h* from the PEAK LOCUS (secondary; the 2D run showed this ruler is")
    print("        biased, because an entropy-gap maximiser is not a scaling observable)")
    for thr in ('theta0', 'median'):
        Lv = [L for L in Ls if np.isfinite(peaks[(L, thr)][0])]
        hs = [peaks[(L, thr)][0] / L ** Y_H for L in Lv]
        s = slope(Lv, hs)
        print(f"    {thr:<8s}  d ln h* / d ln L = {s:+.4f}   -> y_h = {-s:.4f}   "
              f"(3D {Y_H:.4f}, 2D 1.8750)   {verdict(abs(-s-Y_H),0.10,0.30,'')}")

    # ---- E3 / E2 moment collapse ----
    print("\n  E3 — moment collapse at matched u, and E2 — y_h inferred from its drift")
    u0 = None
    cand = [u for u in us if all((L, u, 'theta0', 'colin-r') in R for L in Ls)]
    if cand:
        mid = [peaks[(L, 'theta0')][0] for L in Ls if np.isfinite(peaks[(L, 'theta0')][0])]
        tgt = float(np.median(mid)) if mid else cand[len(cand) // 2]
        u0 = min(cand, key=lambda u: abs(math.log(u / tgt)))
    if u0:
        print(f"    matched at u = {u0:.4f}")
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
        # y_h from the drift, using d ln X / d ln u measured at fixed L
        print("\n    E2 (PRIMARY) — y_h from the collapse:")
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
        print(f"    {thr:<8s} " + " ".join(f"L={L}:{v:.3e}" for L, v in zip(Lv, Iv)))
        for i in range(len(Lv) - 1):
            s = slope(Lv[i:i + 2], Iv[i:i + 2])
            print(f"        local slope L={Lv[i]}->{Lv[i+1]}: {s:+.3f}")
        if len(Lv) >= 2:
            s = slope(Lv[-2:], Iv[-2:])
            print(f"      largest pair slope = {s:+.4f}  -> "
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
    for L in Ls:
        xs = [u for u in us[:4] if (L, u, 'theta0', 'colin-r') in R]
        ys = [R[(L, u, 'theta0', 'colin-r')]['excess'] for u in xs]
        s = slope(xs, ys)
        print(f"    L={L:<3d} small-u slope = {s:+.4f}   {verdict(abs(s-2),0.05,0.15,'')}")

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
            row = [r for r in rows if r['L'] == L and abs(r['u'] - ub) < 1e-9]
            if not row:
                continue
            cnt = np.asarray(row[0]['counts'][thr]['colin-r'], float).sum(axis=0)
            p = cnt / cnt.sum()
            try:
                m, prm, rms = mixture_null(p)
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
    do_k1(rows, '(ridge stage, h=0 column)')
    return R, peaks, u0


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
    if load('phi4_ridge.json'):
        do_ridge(mc)
    return 0


if __name__ == '__main__':
    sys.exit(main())
