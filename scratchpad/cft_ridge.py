"""cft_ridge.py — is the critical ridge of I_C^(3) the 2D Ising CFT?

Pre-registered in CFT_RIDGE_PREREG.md, committed at de11b97 BEFORE this file existed.

THE PRIMARY ARM IS NOT MONTE CARLO.  The sibling's ridge measurement was limited by
critical slowing down in a field (no cluster algorithm applies; variance inflation F
reached 5.5e4; 26% of grid points were discarded).  Here the L x L torus is solved
EXACTLY by transfer matrix: the single-row marginal is w(sigma) ~ [T^L]_{sigma,sigma}
with T = D^{1/2} V D^{1/2}, from which every moment of a collinear triple follows to
machine precision.  No sampling, no estimator, no bias, no decorrelation question.

Two independent implementations of the same object:
  `full`     — apply T L times to the identity in column chunks, read the diagonal.
               No truncation of any kind.  Used for L <= 14.
  `lanczos`  — w = sum_n (lam_n/lam_1)^L v_n^2 over the top-k eigenpairs.  Used for
               L >= 16, validated against `full` and with k doubled.

Usage:
    python3 cft_ridge.py --gate
    python3 cft_ridge.py --hscan     # E1: h*(L) ~ L^-y_h
    python3 cft_ridge.py --collapse  # E2/E4/E5/E7: moments and share vs L at fixed u
    python3 cft_ridge.py --rscan     # E8: r-dependence, and G6
    python3 cft_ridge.py --sat       # E6: saturation scale vs h
    python3 cft_ridge.py --hsq       # E3: the h^2 gate
"""
import sys, os, json, time, math, argparse
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ising_field import share3, all_measures, SIGMA, LN2, TC

HERE = os.path.dirname(os.path.abspath(__file__))

# CFT constants — all standard, none of them ours.
D_SIGMA = 0.125          # Delta_sigma = 1/8
D_EPS = 1.0              # Delta_epsilon = 1
C_SSE = 0.5              # C_{sigma sigma epsilon}
Y_H = 15.0 / 8.0         # magnetic RG eigenvalue = 2 - Delta_sigma
E2_EXP = -6.0 * D_SIGMA  # -3/4, the pre-registered ridge-amplitude exponent

# the eight cells, in ising_field's convention: index = 4*b1 + 2*b2 + b3, s = 1-2b
_B = np.array([[(i >> 2) & 1, (i >> 1) & 1, i & 1] for i in range(8)])
_S = 1 - 2 * _B                                  # (8,3) spins per cell


# =====================================================================================
# EXACT TORUS TRANSFER MATRIX
# =====================================================================================

class Torus:
    """L x L periodic Ising at temperature T in field h, solved exactly by transfer
    matrix along the rows.

        D(sigma) = exp[ K sum_i s_i s_{i+1} + (h/T) sum_i s_i ]      (diagonal)
        V(sigma,sigma') = prod_i exp[ K s_i s'_i ]                    (tensor product)
        T = D^{1/2} V D^{1/2}   (symmetric; same spectrum as VD, same diagonal in T^L)

    Z = Tr T^L and the exact single-row marginal is w(sigma) = [T^L]_{sigma,sigma} / Z.
    """

    def __init__(self, L, T, h):
        self.L, self.T, self.h = L, T, h
        self.K = 1.0 / T
        self.bh = h / T
        self.N = 1 << L
        idx = np.arange(self.N, dtype=np.int64)
        self.bits = ((idx[:, None] >> np.arange(L)[None, :]) & 1).astype(np.uint8)
        s = 1 - 2 * self.bits.astype(np.int16)
        bond = (s * np.roll(s, -1, axis=1)).sum(axis=1).astype(np.float64)
        mag = s.sum(axis=1).astype(np.float64)
        del s
        logd = self.K * bond + self.bh * mag
        self._logd_max = float(logd.max())
        self.sqrtd = np.exp(0.5 * (logd - self._logd_max))
        self.a = math.exp(self.K)
        self.b = math.exp(-self.K)
        self._lam1 = None

    # ---- V as a tensor product of 2x2 blocks: O(L 2^L) per column
    def apply_V(self, x):
        L, a, b = self.L, self.a, self.b
        shape = x.shape
        C = shape[1] if x.ndim == 2 else 1
        y = x
        for i in range(L):
            hi, lo = 1 << (L - 1 - i), 1 << i
            v = y.reshape(hi, 2, lo, C) if x.ndim == 2 else y.reshape(hi, 2, lo)
            y = (a * v + b * v[:, ::-1]).reshape(shape)
        return y

    def apply_T(self, x):
        sd = self.sqrtd[:, None] if (hasattr(x, 'ndim') and x.ndim == 2) else self.sqrtd
        return sd * self.apply_V(sd * x)

    def lam1(self, iters=300, tol=1e-14):
        """Leading eigenvalue by power iteration — used only to rescale, so that every
        column chunk of the `full` method shares one normalisation."""
        if self._lam1 is not None:
            return self._lam1
        v = np.ones(self.N) / math.sqrt(self.N)
        lam = 0.0
        for _ in range(iters):
            w = self.apply_T(v)
            new = float(np.linalg.norm(w))
            v = w / new
            if abs(new - lam) < tol * new:
                lam = new
                break
            lam = new
        self._lam1 = lam
        return lam

    # ---- implementation 1: no truncation at all
    def row_marginal_full(self, chunk=None, xp=None):
        L, N = self.L, self.N
        lam = self.lam1()
        use_gpu = xp is not None and xp is not np
        ap = xp if use_gpu else np
        if chunk is None:
            budget = (1 << 25) if use_gpu else (1 << 24)
            chunk = max(1, min(N, budget // N))
        sd = ap.asarray(self.sqrtd)
        a, b = self.a, self.b
        w = np.empty(N, dtype=np.float64)
        for j0 in range(0, N, chunk):
            j1 = min(j0 + chunk, N)
            c = j1 - j0
            X = ap.zeros((N, c), dtype=np.float64)
            Y = ap.empty((N, c), dtype=np.float64)
            X[ap.arange(j0, j1), ap.arange(c)] = 1.0
            for _ in range(L):
                X *= sd[:, None]
                for i in range(L):
                    hi, lo = 1 << (L - 1 - i), 1 << i
                    v, y = X.reshape(hi, 2, lo, c), Y.reshape(hi, 2, lo, c)
                    ap.multiply(v[:, 0], a, out=y[:, 0])
                    y[:, 0] += b * v[:, 1]
                    ap.multiply(v[:, 0], b, out=y[:, 1])
                    y[:, 1] += a * v[:, 1]
                    X, Y = Y, X
                X *= sd[:, None]
                X /= lam
            dg = X[ap.arange(j0, j1), ap.arange(c)]
            w[j0:j1] = ap.asnumpy(dg) if use_gpu else dg
            del X, Y, dg
            if use_gpu:
                xp.get_default_memory_pool().free_all_blocks()
        return w / w.sum(), dict(method='full', trunc_resid=0.0, k=N)

    # ---- implementation 2: spectral, truncated at k, with a convergence residual
    def row_marginal_lanczos(self, k=100):
        from scipy.sparse.linalg import LinearOperator, eigsh
        N, L = self.N, self.L
        op = LinearOperator((N, N), matvec=self.apply_T, dtype=np.float64)
        k = min(k, N - 2)
        ncv = min(N - 1, max(2 * k + 2, 20))
        vals, vecs = eigsh(op, k=k, which='LM', ncv=ncv)
        o = np.argsort(-np.abs(vals))
        vals, vecs = vals[o], vecs[:, o]
        rat = vals / vals[0]
        wt = np.sign(rat) ** L * np.abs(rat) ** L
        w = (wt[None, :] * vecs ** 2).sum(axis=1)
        resid = float(abs(wt[-1]))                 # weight of the last retained state
        return w / w.sum(), dict(method='lanczos', trunc_resid=resid, k=int(k),
                                 lam_ratio_last=float(abs(rat[-1])))


# =====================================================================================
# OBSERVABLES OF A COLLINEAR TRIPLE (0, r, 2r) IN ONE ROW
# =====================================================================================

def cells(w, bits, L, r):
    """Exact 8-cell distribution of (s_i, s_{i+r}, s_{i+2r}), averaged over the L
    translations in the row (translation invariance makes this an average of identical
    distributions, so it is variance reduction, not pooling)."""
    p8 = np.zeros(8)
    for i in range(L):
        v = ((bits[:, i].astype(np.int64) << 2)
             | (bits[:, (i + r) % L].astype(np.int64) << 1)
             | bits[:, (i + 2 * r) % L].astype(np.int64))
        p8 += np.bincount(v, weights=w, minlength=8)
    p8 /= L
    return p8 / p8.sum()


def pair_corr(w, bits, L, d):
    """Exact <s_i s_{i+d}>, averaged over translations."""
    tot = 0.0
    for i in range(L):
        si = 1 - 2 * bits[:, i].astype(np.float64)
        sj = 1 - 2 * bits[:, (i + d) % L].astype(np.float64)
        tot += float((w * si * sj).sum())
    return tot / L


def moments(p8):
    """The five moments, the Ursell three-point function, the maxent gap and the share.

    Delta_tau is EXACT here: q = p + t*sigma with sigma = s1 s2 s3, so
    tau_q = tau_p + 8t and Delta_tau = tau_p - tau_q = -8t, with t the maxent root."""
    p8 = np.asarray(p8, dtype=np.float64)
    m = [float((p8 * _S[:, j]).sum()) for j in range(3)]
    c = {(0, 1): float((p8 * _S[:, 0] * _S[:, 1]).sum()),
         (0, 2): float((p8 * _S[:, 0] * _S[:, 2]).sum()),
         (1, 2): float((p8 * _S[:, 1] * _S[:, 2]).sum())}
    tau = float((p8 * _S[:, 0] * _S[:, 1] * _S[:, 2]).sum())
    U = tau - (m[0] * c[(1, 2)] + m[1] * c[(0, 2)] + m[2] * c[(0, 1)]) + 2 * m[0] * m[1] * m[2]
    ic3, q, t = share3(p8)
    dtau = -8.0 * float(t)
    inv = float((1.0 / np.maximum(p8, 1e-300)).sum())
    return dict(m=float(np.mean(m)), m_all=m, c_r=c[(0, 1)], c_2r=c[(0, 2)], tau=tau,
                U=float(U), dtau=dtau, ic3=float(ic3), cf=float(ic3) / LN2,
                inv_sum=inv, quad=0.5 * dtau ** 2, quad_full=inv * dtau ** 2 / 128.0,
                min_cell=float(p8.min()), p8=p8.tolist())


def solve(L, T, h, method='auto', k=100, xp=None):
    tt = Torus(L, T, h)
    if method == 'auto':
        method = 'full' if L <= 14 else 'lanczos'
    if method == 'full':
        w, info = tt.row_marginal_full(xp=xp)
    else:
        w, info = tt.row_marginal_lanczos(k=k)
    return tt, w, info


def measure(L, T, h, rs, method='auto', k=100, xp=None, want_corr=True):
    tt, w, info = solve(L, T, h, method, k, xp)
    out = dict(L=L, T=T, h=h, u=h * L ** Y_H, info=info, r={}, corr={})
    for r in rs:
        if r < 1 or (2 * r) % L == 0 or r % L == 0:
            continue
        out['r'][r] = moments(cells(w, tt.bits, L, r))
    if want_corr:
        for d in range(0, L // 2 + 1):
            out['corr'][d] = pair_corr(w, tt.bits, L, d)
    return out


# =====================================================================================
# GATES
# =====================================================================================

def gate(xp=None):
    print("=" * 84)
    print("GATES — prereg section 5.  All six required before any prediction is scored.")
    print("=" * 84)
    ok = True

    # ---- G1: exact transfer matrix vs the sibling's exact 2^N enumeration, 4x4 lattice
    # Their 'colin1' geometry is ((0,0),(1,0),(2,0)) -- collinear inside one row, which
    # is exactly what the transfer matrix can reach.  Two completely independent exact
    # methods on the same object.
    with open(os.path.join(HERE, 'ising_exact.json')) as f:
        ex = json.load(f)
    Ts, hs = np.array(ex['T']), np.array(ex['h'])
    ref = np.array(ex['lattices']['4x4']['geoms']['colin1']['ic3'])
    picks = [(3, 5), (10, 12), (18, 0), (18, 14), (25, 20), (30, 9), (40, 25), (45, 30)]
    worst = 0.0
    for (ia, ib) in picks:
        Tv, hv = float(Ts[ia]), float(hs[ib])
        mm = measure(4, Tv, hv, [1], method='full', want_corr=False)['r'][1]
        worst = max(worst, abs(mm['ic3'] - ref[ia, ib]))
        print(f"       T={Tv:.3f} h={hv:.4f}: TM {mm['ic3']:.12e}  "
              f"enumeration {ref[ia, ib]:.12e}")
    print(f"(G1) transfer matrix vs sibling's exact 4x4 enumeration (colin1), "
          f"{len(picks)} (T,h) points:  max|dI_C3| = {worst:.3e}   (< 1e-10 required)")
    ok &= worst < 1e-10

    # ---- G2: the lemma.  h = 0 -> share exactly zero, every L, every r.
    worst2 = 0.0
    for L in (4, 6, 8, 10, 12):
        for T in (1.5, TC, 3.5):
            mm = measure(L, T, 0.0, list(range(1, L // 2)), method='full', xp=xp,
                         want_corr=False)
            for r, v in mm['r'].items():
                worst2 = max(worst2, abs(v['ic3']))
    print(f"(G2) *** LEMMA *** h=0, L=4..12, three temperatures, every r:  "
          f"max|I_C^(3)| = {worst2:.3e}   (< 1e-12 required)")
    ok &= worst2 < 1e-12

    # ---- G3: lanczos vs full, and k -> 2k
    worst3 = worst3b = 0.0
    for L in (12, 14):
        h = 3.0 * L ** (-Y_H)
        a = measure(L, TC, h, [1, 2, 3], method='full', xp=xp, want_corr=False)
        b = measure(L, TC, h, [1, 2, 3], method='lanczos', k=60, want_corr=False)
        c = measure(L, TC, h, [1, 2, 3], method='lanczos', k=120, want_corr=False)
        for r in a['r']:
            worst3 = max(worst3, abs(a['r'][r]['ic3'] - c['r'][r]['ic3']))
            worst3b = max(worst3b, abs(b['r'][r]['ic3'] - c['r'][r]['ic3']))
    print(f"(G3) lanczos(k=120) vs full, L=12,14:  max|dI_C3| = {worst3:.3e}   (< 1e-10)")
    print(f"     k=60 vs k=120:                    max|dI_C3| = {worst3b:.3e}   (< 1e-8)")
    ok &= worst3 < 1e-10 and worst3b < 1e-8

    # ---- G4: Onsager.  <s_0 s_1> at T_c, h=0 -> sqrt(2)/2 in the thermodynamic limit.
    print(f"(G4) nearest-neighbour correlation at T_c, h=0  (Onsager: "
          f"{math.sqrt(2)/2:.6f} as L -> inf)")
    c16 = float('nan')
    for L in (6, 10, 14, 16):
        tt, w, _ = solve(L, TC, 0.0, method='full', xp=xp)
        c16 = pair_corr(w, tt.bits, L, 1)
        print(f"       L={L:<3} <s0 s1> = {c16:.6f}")
    ok &= abs(c16 - math.sqrt(2) / 2) < 0.02

    print(f"\nGATE VERDICT (G1-G4): {'PASS' if ok else 'FAIL'}")
    print("G5 (Delta_tau vs Ursell) and G6 (growth in r) are scored inside the runs.")
    return ok


# =====================================================================================
# E1 — the ridge locus:  h*(L) ~ L^(-y_h)
# =====================================================================================

def find_hstar(L, r, method='auto', k=100, xp=None, u_lo=0.2, u_hi=40.0, n=13,
               refine=3, verbose=True):
    """Locate the h that maximises I_C^(3) at T = T_c for a triple at spacing r.
    Scan is placed in the scaling variable u = h L^(15/8) so the same window works at
    every L; that is grid PLACEMENT, and the fitted exponent below does not use it."""
    lo, hi = u_lo, u_hi
    best = None
    for it in range(refine + 1):
        us = np.geomspace(lo, hi, n if it == 0 else 5)
        n_it = len(us)
        vals = []
        for u in us:
            h = float(u) * L ** (-Y_H)
            mm = measure(L, TC, h, [r], method=method, k=k, xp=xp, want_corr=False)
            vals.append(mm['r'][r]['ic3'])
        vals = np.array(vals)
        j = int(np.argmax(vals))
        best = (float(us[j]), float(vals[j]))
        if verbose:
            print(f"    L={L} r={r} pass {it}: peak u={us[j]:.4f} "
                  f"I={vals[j]:.6e}  window[{lo:.3f},{hi:.3f}]")
        lo = us[max(j - 1, 0)]
        hi = us[min(j + 1, n_it - 1)]
        if hi / lo < 1.02:
            break
    u_star, i_star = best
    return dict(L=L, r=r, u_star=u_star, h_star=u_star * L ** (-Y_H), ic3_star=i_star)


def run_hscan(args, xp):
    print("\n" + "=" * 84)
    print("E1 / E2 — ridge locus and amplitude.  h*(L) at fixed r/L = 1/4, T = T_c.")
    print("=" * 84)
    rows = []
    for L in args.Ls:
        r = L // 4
        t0 = time.time()
        d = find_hstar(L, r, method=args.method, k=args.k, xp=xp)
        mm = measure(L, TC, d['h_star'], [r], method=args.method, k=args.k, xp=xp,
                     want_corr=False)['r'][r]
        d.update({kk: mm[kk] for kk in
                  ('m', 'c_r', 'c_2r', 'tau', 'U', 'dtau', 'ic3', 'cf', 'quad',
                   'quad_full', 'inv_sum', 'min_cell')})
        d['secs'] = time.time() - t0
        rows.append(d)
        print(f"  L={L:<3} r={r:<2} h*={d['h_star']:.6e}  u*={d['u_star']:.4f}  "
              f"I_C3={d['ic3']:.6e} (CF {100*d['cf']:.3f}%)  m={d['m']:.4f}  "
              f"U={d['U']:+.5f}  dtau={d['dtau']:+.5f}  [{d['secs']:.0f}s]")
    _dump('cft_hscan.json', rows)
    _report_power(rows, 'L', 'h_star', 'E1  h*(L)', -Y_H, tol=0.06, fire=0.15)
    _report_power(rows, 'L', 'ic3', 'E2  ridge I_C^(3)(L)', E2_EXP, tol=0.10, fire=0.30)
    for key, exp in (('m', -D_SIGMA), ('U', -3 * D_SIGMA), ('dtau', -3 * D_SIGMA)):
        _report_power(rows, 'L', key, f'E4  {key}(L)', exp, tol=0.06, fire=0.15)
    return rows


# =====================================================================================
# E4 / E5 / E7 — moment collapse and the parameter-free rescaling test
# =====================================================================================

def run_collapse(args, xp):
    print("\n" + "=" * 84)
    print("E4 / E5 / E7 — moments at MATCHED (r/L, u).  The CFT content, and the")
    print("parameter-free moment-rescaling test.")
    print("=" * 84)
    u = args.u
    rows = []
    for L in args.Ls:
        r = L // 4
        h = u * L ** (-Y_H)
        t0 = time.time()
        mm = measure(L, TC, h, [r], method=args.method, k=args.k, xp=xp, want_corr=True)
        d = dict(L=L, r=r, h=h, u=u, secs=time.time() - t0, info=mm['info'],
                 corr=mm['corr'])
        d.update(mm['r'][r])
        rows.append(d)
        print(f"  L={L:<3} r={r:<2} h={h:.5e}  m={d['m']:.5f}  c(r)={d['c_r']:.5f}  "
              f"c(2r)={d['c_2r']:.5f}  tau={d['tau']:.5f}")
        print(f"        U={d['U']:+.6f}  dtau={d['dtau']:+.6f}  "
              f"|dtau-U|/|dtau|={abs(d['dtau']-d['U'])/max(abs(d['dtau']),1e-30):.3f}  "
              f"I_C3={d['ic3']:.6e}  1/2 dtau^2={d['quad']:.6e}  "
              f"ratio={d['ic3']/max(d['quad'],1e-300):.3f}  [{d['secs']:.0f}s]")
    _dump('cft_collapse.json', rows)

    print("\n  --- E4: rescaled moments (should be L-independent) ---")
    print(f"  {'L':>4} {'m*L^1/8':>12} {'c(r)*L^1/4':>12} {'tau*L^3/8':>12} "
          f"{'U*L^3/8':>12} {'dtau*L^3/8':>12} {'I*L^3/4':>12}")
    for d in rows:
        L = d['L']
        print(f"  {L:>4} {d['m']*L**0.125:>12.6f} {d['c_r']*L**0.25:>12.6f} "
              f"{d['tau']*L**0.375:>12.6f} {d['U']*L**0.375:>12.6f} "
              f"{d['dtau']*L**0.375:>12.6f} {d['ic3']*L**0.75:>12.6f}")
    for key, exp, name in (('m', 0.125, 'm'), ('c_r', 0.25, 'c(r)'),
                           ('tau', 0.375, 'tau'), ('U', 0.375, 'U'),
                           ('dtau', 0.375, 'dtau')):
        v = np.array([d[key] * d['L'] ** exp for d in rows])
        drift = abs(v[-1] / v[-2] - 1.0) if len(v) > 1 else float('nan')
        print(f"  E4 {name:<6} rescaled drift over the largest L pair: "
              f"{100*drift:6.2f} %   -> {'SURVIVES' if drift<0.02 else ('FIRES' if drift>0.08 else 'marginal')}")

    print("\n  --- E7: MOMENT-RESCALING TEST (parameter-free) ---")
    print("  Take the exact moments at L1, scale by (L2/L1)^(-1/8) per spin, compute")
    print("  I_C^(3) EXACTLY from them, compare to the direct L2 value.  No amplitudes,")
    print("  no weak-coupling, no fitted parameter.")
    e7 = []
    for i in range(len(rows) - 1):
        a, b = rows[i], rows[i + 1]
        lam = (b['L'] / a['L']) ** (-0.125)
        p = _p8_from_moments(a['m'] * lam, a['c_r'] * lam ** 2, a['c_2r'] * lam ** 2,
                             a['tau'] * lam ** 3)
        pred = float(share3(p)[0])
        rel = pred / b['ic3'] - 1.0
        e7.append(dict(L1=a['L'], L2=b['L'], pred=pred, direct=b['ic3'], rel=rel))
        print(f"  L {a['L']:>3} -> {b['L']:>3}:  predicted {pred:.6e}   "
              f"direct {b['ic3']:.6e}   residual {100*rel:+7.2f} %")
    if e7:
        last = abs(e7[-1]['rel'])
        print(f"  E7 verdict: |residual| at the largest pair = {100*last:.2f} %  -> "
              f"{'SURVIVES' if last<0.03 else ('FIRES' if last>0.12 else 'marginal')}")
    _dump('cft_e7.json', e7)
    run_ray(rows, 'A')
    return rows, e7


def _p8_from_moments(m, c12, c13, tau):
    """Rebuild the 8-cell distribution from the exchangeable-triple moments
    (m1=m2=m3=m, c12=c23, c13, tau).  Exact inverse of `moments`."""
    p = np.empty(8)
    for v in range(8):
        s1, s2, s3 = _S[v]
        p[v] = (1.0 + m * (s1 + s2 + s3)
                + c12 * (s1 * s2 + s2 * s3) + c13 * s1 * s3
                + tau * s1 * s2 * s3) / 8.0
    return p


# =====================================================================================
# THE SCALING RAY — why L^(-3/4) need not be visible
# =====================================================================================
#
# If the moments carry the CFT exponents, then at fixed (r/L, u) the whole three-spin
# distribution moves along a ONE-PARAMETER ray:  m = A1 lam, c = A2 lam^2, tau = A3 lam^3,
# with lam = L^(-1/8) and the amplitudes A fixed by the shape functions.  I_C^(3) is an
# exact function of the moments, so it is an exact function of lam along that ray.  This
# routine evaluates it, using amplitudes read off a single measured lattice, and reports
# the local exponent d ln I / d ln L = -(1/8) d ln I / d ln lam.  Nothing new is assumed:
# it is the CFT scaling of Step C fed through the exact instrument of Step A.

def run_ray(rows, tag='A'):
    print("\n" + "=" * 84)
    print(f"THE SCALING RAY [arm {tag}] — I_C^(3) along m~lam, c~lam^2, tau~lam^3")
    print("=" * 84)
    ref = rows[-1]
    lam0 = ref['L'] ** (-0.125)
    A = (ref['m'] / lam0, ref['c_r'] / lam0 ** 2, ref['c_2r'] / lam0 ** 2,
         ref['tau'] / lam0 ** 3)
    print(f"  amplitudes read off L={ref['L']} (lam={lam0:.5f}): "
          f"m/lam={A[0]:.5f}  c/lam^2={A[1]:.5f}  tau/lam^3={A[3]:.5f}")
    out = []
    Ls = [8, 12, 16, 20, 24, 32, 48, 64, 128, 512, 4096, 10 ** 5, 10 ** 7, 10 ** 10]
    prev = None
    for L in Ls:
        lam = float(L) ** (-0.125)
        p = _p8_from_moments(A[0] * lam, A[1] * lam ** 2, A[2] * lam ** 2, A[3] * lam ** 3)
        if p.min() < 0:
            continue
        mm = moments(p)
        slope = (math.log(mm['ic3'] / prev[1]) / math.log(L / prev[0])) if prev else float('nan')
        out.append(dict(L=L, lam=lam, ic3=mm['ic3'], dtau=mm['dtau'], U=mm['U'],
                        quad=mm['quad'], quad_full=mm['quad_full'], slope=slope))
        print(f"  L={L:<12g} lam={lam:.5f}  I_C^(3)={mm['ic3']:.6e}  "
              f"dtau={mm['dtau']:+.6f}  1/2 dtau^2={mm['quad']:.3e}  "
              f"I/(1/2 dtau^2)={mm['ic3']/max(mm['quad'],1e-300):6.3f}  "
              f"local dlnI/dlnL={slope:+.4f}")
        prev = (L, mm['ic3'])
    _dump(f'cft_ray_{tag}.json', out)
    return out


# =====================================================================================
# E8 / G6 — the r-dependence
# =====================================================================================

def run_rscan(args, xp):
    print("\n" + "=" * 84)
    print("E8 / G6 — r-dependence on the ridge at matched u, and its collapse in r/L.")
    print("=" * 84)
    u = args.u
    out = []
    for L in args.Ls:
        h = u * L ** (-Y_H)
        rs = [r for r in range(1, L // 2) if (2 * r) % L != 0]
        t0 = time.time()
        mm = measure(L, TC, h, rs, method=args.method, k=args.k, xp=xp, want_corr=True)
        row = dict(L=L, h=h, u=u, corr=mm['corr'], secs=time.time() - t0,
                   r={str(r): mm['r'][r] for r in mm['r']})
        out.append(row)
        print(f"  L={L}  h={h:.5e}")
        for r in sorted(mm['r']):
            d = mm['r'][r]
            print(f"    r={r:<3} r/L={r/L:.3f}  I_C3={d['ic3']:.5e}  "
                  f"U={d['U']:+.5f}  dtau={d['dtau']:+.5f}  "
                  f"|dtau-U|/|dtau|={abs(d['dtau']-d['U'])/max(abs(d['dtau']),1e-30):.3f}  "
                  f"I*L^3/4={d['ic3']*L**0.75:.5f}")
        print(f"    [{row['secs']:.0f}s]")
    _dump('cft_rscan.json', out)
    return out


# =====================================================================================
# E6 — the saturation scale
# =====================================================================================

def run_sat(args, xp):
    print("\n" + "=" * 84)
    print("E6 — saturation scale vs field.  Prediction: r_sat ~ h^(-1/y_h) = h^(-0.533)")
    print("for h above the ridge (xi_h < L), and ~L below it.")
    print("=" * 84)
    L = args.satL
    rs = [r for r in range(1, L // 2) if (2 * r) % L != 0]
    hstar = args.u * L ** (-Y_H)
    hs = [hstar * f for f in (1, 2, 4, 8, 16, 32, 64)]
    out = []
    for h in hs:
        mm = measure(L, TC, float(h), rs, method=args.method, k=args.k, xp=xp,
                     want_corr=True)
        vals = np.array([mm['r'][r]['ic3'] for r in sorted(mm['r'])])
        rr = np.array(sorted(mm['r']))
        peak = float(vals.max())
        r90 = float(np.interp(0.9 * peak, vals[:int(np.argmax(vals)) + 1],
                              rr[:int(np.argmax(vals)) + 1])) if peak > 0 else float('nan')
        r80 = float(np.interp(0.8 * peak, vals[:int(np.argmax(vals)) + 1],
                              rr[:int(np.argmax(vals)) + 1])) if peak > 0 else float('nan')
        xi, _pl = _fit_xi(mm['corr'], L, mm['r'][rs[0]]['m'])
        out.append(dict(L=L, h=float(h), u=float(h) * L ** Y_H, peak=peak,
                        r90=r90, r80=r80, xi=xi, r_argmax=float(rr[int(np.argmax(vals))]),
                        curve={str(r): mm['r'][r]['ic3'] for r in sorted(mm['r'])}))
        print(f"  h={h:.5e} (h/h*={h/hstar:5.1f})  peak I={peak:.4e} at r={rr[int(np.argmax(vals))]}"
              f"   r90={r90:.2f}  r80={r80:.2f}  xi={xi:.3f}")
    _dump('cft_sat.json', out)
    _report_power(out, 'h', 'r90', 'E6  r90(h)', -1.0 / Y_H, tol=0.08, fire=0.20)
    _report_power(out, 'h', 'xi', 'E6b xi(h)', -1.0 / Y_H, tol=0.08, fire=0.20)
    return out


def _fit_xi(corr, L, m):
    """Connected correlation length on a torus.

    NOT simply c(d) - m^2.  At T_c near the ridge the order parameter has a broad,
    skewed distribution, so c(d) tends to a NON-ZERO plateau at d = L/2 which is the
    zero mode, not a correlation.  Fitting cosh to c(d) - m^2 mixes that plateau into
    the decay and biases xi down.  So the plateau is fitted, not assumed:

        c(d) = P + A [cosh((L/2 - d)/xi) - 1],

    linear in (P, A) at fixed xi, so xi is found by a 1-D scan with a 2x2 solve inside.
    Returned with the fitted plateau so the caller can check xi << L before using it."""
    d = np.array(sorted(int(k) for k in corr), dtype=float)
    g = np.array([corr[k] for k in sorted(corr, key=lambda z: int(z))], dtype=float)
    sel = d >= 1
    dd, gg = d[sel], g[sel]
    if len(dd) < 4:
        return float('nan'), float('nan')
    best, bx, bP = None, float('nan'), float('nan')
    for xi in np.geomspace(0.3, 3 * L, 900):
        f = np.cosh((L / 2.0 - dd) / xi) - 1.0
        M = np.array([[len(dd), f.sum()], [f.sum(), (f * f).sum()]])
        rhs = np.array([gg.sum(), (gg * f).sum()])
        try:
            P, A = np.linalg.solve(M, rhs)
        except np.linalg.LinAlgError:
            continue
        res = float(((gg - P - A * f) ** 2).sum())
        if best is None or res < best:
            best, bx, bP = res, float(xi), float(P)
    return bx, bP


# =====================================================================================
# STEP A, verified where it must be exact:  h -> 0
# =====================================================================================

def run_stepa(args, xp):
    """Two checks that need no CFT at all.

    (1) Step A says I_C^(3) = (1/128)[sum_s 1/p_s](Delta tau)^2 + O(Delta tau^3).  As
        h -> 0 at T_c, Delta tau -> 0 while the pair correlations stay O(1), so the
        cubic remainder must vanish and the ratio must go to exactly 1.  If it does
        not, Step A is wrong.
    (2) Step B says Delta tau = U + higher order.  This prints U/Delta tau in the same
        limit.  Step B predicts 1.  Whatever it converges to is the honest answer."""
    print("\n" + "=" * 84)
    print("STEP A / STEP B, verified in the h -> 0 limit at T = T_c")
    print("=" * 84)
    out = []
    for L in (8, 12, 16):
        r = L // 4
        print(f"  L={L}, r={r}:")
        for h in [args.u * L ** (-Y_H) * f for f in (1e-4, 1e-3, 1e-2, 1e-1, 1.0)]:
            mm = measure(L, TC, float(h), [r], method='auto', k=args.k, xp=xp,
                         want_corr=False)['r'][r]
            ra = mm['ic3'] / mm['quad_full'] if mm['quad_full'] > 0 else float('nan')
            rb = mm['U'] / mm['dtau'] if mm['dtau'] != 0 else float('nan')
            out.append(dict(L=L, r=r, h=float(h), ratio_stepA=ra, ratio_U_over_dtau=rb,
                            **{kk: mm[kk] for kk in ('ic3', 'U', 'dtau', 'm', 'c_r',
                                                     'quad', 'quad_full', 'inv_sum')}))
            print(f"    h={h:.4e}  I={mm['ic3']:.5e}  m={mm['m']:.2e}  c(r)={mm['c_r']:.4f}"
                  f"   I/[(1/128)S dtau^2] = {ra:.6f}   U/dtau = {rb:8.4f}")
    _dump('cft_stepa.json', out)
    return out


def run_gap(args, xp):
    """E6, third pass — xi from the TRANSFER-MATRIX GAP, which is exact.

    Fitting cosh to c(d) on a torus failed for a reason worth recording: near the ridge
    c(d) is dominated by a non-decaying plateau (the zero mode), and the exponential
    sits on top of it, so at the fields where the ridge lives the fitted xi never left
    the lattice cutoff.  On a STRIP of width L (infinite in the other direction) the
    same correlation length is simply xi = 1 / ln(lam_1 / lam_2), with no fit at all.
    Valid as the bulk length once xi << L; at h = 0 it saturates at the strip value
    L/(2 pi Delta_sigma) = 4L/pi, so the window is exactly xi in [2, L/4]."""
    from scipy.sparse.linalg import LinearOperator, eigsh
    print("\n" + "=" * 84)
    print("E6 (third pass) — xi = 1/ln(lam_1/lam_2) from the transfer matrix. Exact.")
    print(f"Prediction: xi ~ h^(-1/y_h) = h^({-1/Y_H:.4f}) once xi << L.")
    print("=" * 84)
    out = []
    for L in args.Ls[-2:]:
        print(f"  L={L}   (strip value at h=0 is 4L/pi = {4*L/math.pi:.1f}; "
              f"valid window xi in [2, {L/4:.1f}])")
        for u in (1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0, 128.0, 256.0, 512.0):
            h = u * L ** (-Y_H)
            tt = Torus(L, TC, float(h))
            op = LinearOperator((tt.N, tt.N), matvec=tt.apply_T, dtype=np.float64)
            vals = eigsh(op, k=4, which='LM', return_eigenvectors=False)
            v = np.sort(np.abs(vals))[::-1]
            xi = 1.0 / math.log(v[0] / v[1]) if v[1] > 0 and v[0] > v[1] else float('nan')
            okv = 2.0 < xi < L / 4.0
            out.append(dict(L=L, u=u, h=float(h), xi=float(xi), valid=bool(okv)))
            print(f"    u={u:7.1f}  h={h:.6e}  xi = {xi:9.4f}   "
                  f"{'USE' if okv else 'excluded'}")
        sub = [o for o in out if o['L'] == L and o['valid']]
        if len(sub) >= 2:
            _report_power(sub, 'h', 'xi', f'E6  xi(h) at L={L}', -1.0 / Y_H, 0.08, 0.20)
        else:
            print(f"  E6 at L={L}: {len(sub)} valid point(s) — NOT TESTABLE")
    _dump('cft_gap.json', out)
    return out


def run_bulk(args, xp):
    """Is the transfer-matrix gap length the BULK correlation length, or a strip artefact?

    The pre-registered validity window for E6 was 1 << xi << L.  This asks the question the
    window was a proxy for, directly: at MATCHED h, does xi depend on the strip width?  If
    it does not, the value is bulk whatever xi's size in lattice units."""
    from scipy.sparse.linalg import LinearOperator, eigsh
    print("\n" + "=" * 84)
    print("E6 support — xi at MATCHED h across strip widths.  Bulk, or strip artefact?")
    print("=" * 84)
    hs = [0.05, 0.10, 0.20, 0.40, 0.80]
    tab = {}
    for L in (14, 17, 20):
        row = []
        for h in hs:
            tt = Torus(L, TC, float(h))
            v = np.sort(np.abs(eigsh(LinearOperator((tt.N, tt.N), matvec=tt.apply_T,
                                                    dtype=np.float64), k=4, which='LM',
                                     return_eigenvectors=False)))[::-1]
            row.append(1.0 / math.log(v[0] / v[1]))
        tab[L] = row
        print(f"  L={L:<3} " + "  ".join(f"h={h:.2f}: {x:7.4f}" for h, x in zip(hs, row)))
    arr = np.array([tab[L] for L in (14, 17, 20)])
    spread = [100 * (arr[:, j].max() / arr[:, j].min() - 1) for j in range(len(hs))]
    print("  spread across L at fixed h: " + "  ".join(f"{s:.3f} %" for s in spread))
    lx, ly = np.log(hs), np.log(tab[20])
    sl = np.diff(ly) / np.diff(lx)
    print("  local slopes (L=20): " + "  ".join(f"{s:+.4f}" for s in sl))
    print(f"  global fit {np.polyfit(lx, ly, 1)[0]:+.4f}   predicted {-1/Y_H:+.4f}")
    print("  NOTE: xi here is 1.9 down to 0.45 lattice spacings, i.e. OUTSIDE the")
    print("  pre-registered window xi >> 1.  Reported post-hoc; E6 is not scored on it.")
    _dump('cft_bulk.json', dict(h=hs, xi={str(L): tab[L] for L in tab}, spread=spread,
                                slopes=sl.tolist()))
    return tab


def run_yh(args, xp):
    """E1, measured from the COLLAPSE rather than from a peak location.

    The peak of I_C^(3) in h is a poor ruler: I_C^(3) is a nonlinear function of the
    moments, so its maximiser inherits an L-dependence from that nonlinearity and drifts
    even when the scaling is exact.  The correlators do not have that problem.  If the
    magnetic eigenvalue is y rather than y_h = 15/8, then holding u = h L^(y_h) fixed
    holds the TRUE argument h L^y fixed only up to L^(y - y_h), and each rescaled moment
    drifts by (dlnf/dlnu)(y - y_h)ln(L2/L1).  Measuring dlnf/dlnu turns the observed
    drift into a bound on y.  Nothing is fitted; one derivative is measured."""
    print("\n" + "=" * 84)
    print("E1 (second pass) — y_h from the moment collapse, not from a peak location.")
    print("=" * 84)
    Ls = args.Ls[-2:]
    us = [args.u / 1.25, args.u, args.u * 1.25]
    dat = {}
    for L in Ls:
        r = L // 4
        vals = []
        for u in us:
            mm = measure(L, TC, float(u) * L ** (-Y_H), [r], method='auto', k=args.k,
                         xp=xp, want_corr=False)['r'][r]
            vals.append(mm)
        dat[L] = vals
        dl = {}
        for key in ('m', 'c_r', 'tau', 'U'):
            a, b = abs(vals[0][key]), abs(vals[2][key])
            dl[key] = math.log(b / a) / math.log(us[2] / us[0])
        dat[str(L) + 'dlog'] = dl
        print(f"  L={L}: dln|X|/dln u at u={args.u}:  " +
              "  ".join(f"{k}={dl[k]:+.4f}" for k in dl))
    L1, L2 = Ls
    print(f"\n  inferred magnetic eigenvalue from each moment (predicted {Y_H:.4f}):")
    out = []
    for key, ex in (('m', 0.125), ('c_r', 0.25), ('tau', 0.375), ('U', 0.375)):
        v1 = abs(dat[L1][1][key]) * L1 ** ex
        v2 = abs(dat[L2][1][key]) * L2 ** ex
        D = math.log(v2 / v1)
        s = 0.5 * (dat[str(L1) + 'dlog'][key] + dat[str(L2) + 'dlog'][key])
        y = Y_H - D / (s * math.log(L2 / L1)) if abs(s) > 1e-9 else float('nan')
        out.append(dict(moment=key, drift=D, dlogdu=s, y_inferred=y))
        print(f"    {key:<5} rescaled drift {100*D:+7.3f} %   dln/dlnu {s:+.4f}   "
              f"-> y_h = {y:.4f}   (dev {abs(y-Y_H):.4f})")
    ys = [o['y_inferred'] for o in out if np.isfinite(o['y_inferred'])]
    if ys:
        dev = abs(float(np.mean(ys)) - Y_H)
        print(f"  mean over moments: y_h = {np.mean(ys):.4f} +- {np.std(ys):.4f}  "
              f"(spread across moments)  -> "
              f"{'SURVIVES' if dev < 0.06 else ('FIRES' if dev > 0.15 else 'marginal')}")
    _dump('cft_yh.json', out)
    return out


def run_sat2(args, xp):
    """E6 with the plateau-corrected xi, restricted to the window where the answer can
    mean anything: 1.2 < xi < L/4, i.e. the correlation length resolved by the lattice
    and not cut off by the box."""
    print("\n" + "=" * 84)
    print("E6 (second pass) — xi(h) with the zero-mode plateau FITTED, not assumed.")
    print("Valid only where 1.2 < xi < L/4; points outside are printed and excluded.")
    print("=" * 84)
    out = []
    for L in (12, 16, 20):
        hstar = args.u * L ** (-Y_H)
        print(f"  L={L}  (h* = {hstar:.5e}, valid xi window [1.2, {L/4:.1f}])")
        for f in (0.5, 1, 1.5, 2, 3, 4, 6, 9, 14):
            h = hstar * f
            mm = measure(L, TC, float(h), [max(1, L // 4)], method='auto', k=args.k,
                         xp=xp, want_corr=True)
            m = mm['r'][max(1, L // 4)]['m']
            xi, P = _fit_xi(mm['corr'], L, m)
            okv = 1.2 < xi < L / 4.0
            out.append(dict(L=L, h=float(h), hf=f, xi=xi, plateau=P, m=m, valid=bool(okv)))
            print(f"    h/h*={f:5.1f}  h={h:.5e}  xi={xi:7.3f}  plateau={P:.5f}  "
                  f"m={m:.4f}  {'USE' if okv else 'excluded'}")
    _dump('cft_sat2.json', out)
    for L in (12, 16, 20):
        sub = [o for o in out if o['L'] == L and o['valid']]
        if len(sub) >= 2:
            _report_power(sub, 'h', 'xi', f'E6  xi(h) at L={L}', -1.0 / Y_H, 0.08, 0.20)
        else:
            print(f"  E6 at L={L}: only {len(sub)} point(s) in the valid window — "
                  f"NOT TESTABLE at this size")
    return out


# =====================================================================================
# E3 — the h^2 gate
# =====================================================================================

def run_hsq(args, xp):
    print("\n" + "=" * 84)
    print("E3 — small-h behaviour at T_c, fixed L and r.  GATE, NOT EVIDENCE:")
    print("I_C^(3) ~ h^2 follows from Z2 plus analyticity whatever the mechanism.")
    print("=" * 84)
    out = []
    for L in (8, 12, 16):
        r = L // 4
        hstar = args.u * L ** (-Y_H)
        hs = hstar * np.geomspace(1e-3, 0.3, 8)
        rows = []
        for h in hs:
            mm = measure(L, TC, float(h), [r], method=args.method, k=args.k, xp=xp,
                         want_corr=False)['r'][r]
            rows.append(dict(L=L, r=r, h=float(h), **{kk: mm[kk] for kk in
                                                      ('ic3', 'U', 'dtau', 'm', 'quad')}))
            print(f"  L={L:<3} h={h:.4e}  I_C3={mm['ic3']:.6e}  U={mm['U']:+.4e}  "
                  f"dtau={mm['dtau']:+.4e}")
        out += rows
        _report_power(rows, 'h', 'ic3', f'E3  I_C^(3)(h) at L={L}', 2.0, tol=0.02, fire=0.10)
        _report_power(rows, 'h', 'dtau', f'E3b dtau(h) at L={L}', 1.0, tol=0.02, fire=0.10)
    _dump('cft_hsq.json', out)
    return out


# =====================================================================================
# ARM B — MONTE CARLO, BUT MEASURING MOMENTS, NOT THE ENTROPY GAP
# =====================================================================================
#
# The sibling estimated I_C^(3) directly from an 8-cell histogram.  That statistic is a
# nested-family entropy gap: its plug-in estimator is POSITIVELY BIASED at ~1/(2 N_eff),
# which forced the whole floor/N_eff/variance-inflation apparatus and cost 26% of the
# grid.  But I_C^(3) is an exact, smooth function of five moments, and each moment has an
# UNBIASED estimator with O(1) variance.  So: estimate the moments, then evaluate the
# exact function.  Bias then enters only at second order in the moment errors, and is
# bounded by the bootstrap below rather than modelled.  Arm B is reported only if it
# reproduces Arm A at L = 16 (gate G7).

def mc_moments(L, T, h, R, n_burn, n_samp, gap, rs, xp, seed=0):
    """Checkerboard Metropolis in a field; returns per-replica moment estimates so the
    error bar comes from independent chains rather than from a model."""
    rs_rng = xp.random.RandomState(seed) if hasattr(xp.random, 'RandomState') \
        else np.random.RandomState(seed)
    s = (rs_rng.randint(0, 2, size=(R, L, L)) * 2 - 1).astype(xp.int8)
    # EQUILIBRATION TEST, not a speed-up: the second half of the chains starts fully
    # ordered (the field-favoured state), the first half hot.  Insufficient burn-in
    # biases the two halves in OPPOSITE directions, and the replica scatter would not
    # show it; comparing the halves does.
    s[R // 2:] = 1
    yy, xx = xp.meshgrid(xp.arange(L), xp.arange(L), indexing='ij')
    color = ((xx + yy) % 2).astype(xp.int8)
    masks = [(color == 0), (color == 1)]

    def sweep():
        for mk in masks:
            nb = (xp.roll(s, 1, axis=2) + xp.roll(s, -1, axis=2)
                  + xp.roll(s, 1, axis=1) + xp.roll(s, -1, axis=1)).astype(xp.float32)
            dE = 2.0 * s.astype(xp.float32) * (nb + xp.float32(h))
            acc = (dE <= 0) | (rs_rng.rand(R, L, L).astype(xp.float32)
                               < xp.exp(-dE / xp.float32(T)))
            s[...] = xp.where(acc & mk[None, :, :], -s, s)

    for _ in range(n_burn):
        sweep()
    acc_m = xp.zeros(R, dtype=xp.float64)
    acc_c = {d: xp.zeros(R, dtype=xp.float64) for d in range(1, L // 2 + 1)}
    acc_t = {r: xp.zeros(R, dtype=xp.float64) for r in rs}
    for _ in range(n_samp):
        for _ in range(gap):
            sweep()
        sf = s.astype(xp.float64)
        acc_m += sf.mean(axis=(1, 2))
        for d in acc_c:
            acc_c[d] += 0.5 * ((sf * xp.roll(sf, -d, axis=2)).mean(axis=(1, 2))
                               + (sf * xp.roll(sf, -d, axis=1)).mean(axis=(1, 2)))
        for r in rs:
            acc_t[r] += 0.5 * (
                (sf * xp.roll(sf, -r, axis=2) * xp.roll(sf, -2 * r, axis=2)).mean(axis=(1, 2))
                + (sf * xp.roll(sf, -r, axis=1) * xp.roll(sf, -2 * r, axis=1)).mean(axis=(1, 2)))
        del sf
    g = lambda a: (xp.asnumpy(a) if hasattr(xp, 'asnumpy') else np.asarray(a)) / n_samp
    return dict(m=g(acc_m), c={d: g(acc_c[d]) for d in acc_c},
                tau={r: g(acc_t[r]) for r in rs})


def _mc_pack(per, L, r, nboot=400, rng=None):
    """Replica-bootstrap: resample chains, rebuild the exact 8-cell distribution from the
    resampled moments, and evaluate I_C^(3) exactly on each.  No entropy-estimator bias
    model is needed because no entropy is ever estimated from counts."""
    rng = rng or np.random.default_rng(7)
    R = len(per['m'])
    m, c1, c2, tau = per['m'], per['c'][r], per['c'][min(2 * r, L - 2 * r)], per['tau'][r]
    def build(idx):
        p = _p8_from_moments(m[idx].mean(), c1[idx].mean(), c2[idx].mean(), tau[idx].mean())
        return p
    p0 = build(np.arange(R))
    mm = moments(p0)
    bi = rng.integers(0, R, size=(nboot, R))
    bs = np.array([float(share3(build(bi[i]))[0]) for i in range(nboot)])
    mm['ic3_sd'] = float(bs.std(ddof=1))
    mm['m_sd'] = float(m.std(ddof=1) / math.sqrt(R))
    mm['tau_sd'] = float(tau.std(ddof=1) / math.sqrt(R))
    mm['R'] = R
    return mm


def run_mc(args, xp):
    print("\n" + "=" * 84)
    print("ARM B — Monte Carlo on the MOMENTS (unbiased), share evaluated exactly from")
    print("them.  Gated on reproducing Arm A at L = 16.")
    print("=" * 84)
    if xp is None:
        import numpy as _np
        xp = _np
    out = []
    for L in args.mcLs:
        r = L // 4
        h = args.u * L ** (-Y_H)
        # tau_int ~ L^z with z ~ 2.17 for Metropolis and no cluster algorithm available
        # in a field.  Gap and burn-in are both scaled by it; independence is then read
        # off the ACROSS-CHAIN scatter rather than modelled.
        tau_sw = max(20.0, 0.35 * L ** 2.17)
        gap = int(max(10, round(tau_sw)))
        burn = int(max(500, 6 * tau_sw))
        R, n_samp = args.R, args.nsamp
        t0 = time.time()
        per = mc_moments(L, TC, float(h), R, burn, n_samp, gap,
                         [rr for rr in range(1, L // 2) if (2 * rr) % L != 0], xp,
                         seed=20260725 + L)
        half = R // 2
        hot = _mc_pack({kk: (per[kk][:half] if kk == 'm' else
                             {q: per[kk][q][:half] for q in per[kk]}) for kk in per}, L, r)
        cold = _mc_pack({kk: (per[kk][half:] if kk == 'm' else
                              {q: per[kk][q][half:] for q in per[kk]}) for kk in per}, L, r)
        d = _mc_pack(per, L, r)
        d['hot_cold'] = dict(m_hot=hot['m'], m_cold=cold['m'], ic3_hot=hot['ic3'],
                             ic3_cold=cold['ic3'], tau_hot=hot['tau'], tau_cold=cold['tau'])
        dz = abs(hot['m'] - cold['m']) / max(2 * d['m_sd'], 1e-12)
        d['equil_z'] = float(dz)
        print(f"  [equilibration] hot m={hot['m']:.5f} cold m={cold['m']:.5f}  "
              f"z={dz:.2f}  (|z|>3 means burn-in too short)  tau_sw={tau_sw:.0f} "
              f"gap={gap} burn={burn}")
        d.update(L=L, r=r, h=float(h), u=args.u, secs=time.time() - t0,
                 R=R, n_samp=n_samp, gap=gap, burn=burn,
                 rcurve={str(rr): float(np.mean(per['tau'][rr])) for rr in per['tau']})
        # exact share at every r, from the same moments
        curve = {}
        for rr in per['tau']:
            c1 = float(np.mean(per['c'][rr]))
            c2 = float(np.mean(per['c'][min(2 * rr, L - 2 * rr)]))
            p = _p8_from_moments(float(np.mean(per['m'])), c1, c2,
                                 float(np.mean(per['tau'][rr])))
            curve[str(rr)] = float(share3(p)[0])
        d['share_curve'] = curve
        out.append(d)
        print(f"  L={L:<3} r={r:<2} h={h:.5e}  m={d['m']:.5f}+-{d['m_sd']:.5f}  "
              f"c(r)={d['c_r']:.5f}  tau={d['tau']:.5f}+-{d['tau_sd']:.5f}")
        print(f"        U={d['U']:+.6f}  dtau={d['dtau']:+.6f}  "
              f"I_C3={d['ic3']:.6e} +- {d['ic3_sd']:.2e}   "
              f"I*L^3/4={d['ic3']*L**0.75:.5f}   [{d['secs']:.0f}s]")
        print(f"        share vs r: " + "  ".join(
            f"r={rr}:{curve[rr]:.3e}" for rr in sorted(curve, key=int)))
    _dump('cft_mc.json', out)
    if len(out) > 1:
        run_ray(out, 'B')
        _report_power(out, 'L', 'ic3', 'E2  ridge I_C^(3)(L)  [Arm B]', E2_EXP, 0.10, 0.30)
        for key, exp in (('m', -D_SIGMA), ('U', -3 * D_SIGMA), ('dtau', -3 * D_SIGMA)):
            _report_power(out, 'L', key, f'E4  {key}(L)  [Arm B]', exp, 0.06, 0.15)
    return out


# =====================================================================================

def _report_power(rows, xkey, ykey, name, predicted, tol, fire):
    x = np.array([float(r[xkey]) for r in rows], dtype=float)
    y = np.array([abs(float(r[ykey])) for r in rows], dtype=float)
    good = (x > 0) & (y > 0) & np.isfinite(y)
    x, y = x[good], y[good]
    if len(x) < 2:
        print(f"  {name}: too few points")
        return
    lx, ly = np.log(x), np.log(y)
    slopes = np.diff(ly) / np.diff(lx)
    glob = float(np.polyfit(lx, ly, 1)[0])
    last = float(slopes[-1])
    dev = abs(last - predicted)
    verdict = 'SURVIVES' if dev < tol else ('FIRES' if dev > fire else 'marginal')
    print(f"  {name}: predicted {predicted:+.4f} | local slopes "
          f"[{', '.join(f'{s:+.3f}' for s in slopes)}] | last {last:+.4f} | "
          f"global fit {glob:+.4f}  -> {verdict}")


def _dump(name, obj):
    p = os.path.join(HERE, name)
    with open(p, 'w') as f:
        json.dump(obj, f, default=float)
    print(f"  wrote {p}")


def main():
    ap = argparse.ArgumentParser()
    for a in ('gate', 'hscan', 'collapse', 'rscan', 'sat', 'sat2', 'hsq', 'mc',
              'stepa', 'yh', 'gap', 'bulk', 'all', 'cpu'):
        ap.add_argument('--' + a, action='store_true')
    ap.add_argument('--Ls', type=int, nargs='+', default=[8, 12, 16])
    ap.add_argument('--mcLs', type=int, nargs='+', default=[16, 24, 32, 48, 64])
    ap.add_argument('--u', type=float, default=3.0)
    ap.add_argument('--k', type=int, default=32)
    ap.add_argument('--R', type=int, default=512)
    ap.add_argument('--nsamp', type=int, default=400)
    ap.add_argument('--satL', type=int, default=16)
    ap.add_argument('--method', default='auto')
    args = ap.parse_args()

    xp = None
    if not args.cpu:
        try:
            import cupy
            xp = cupy
            print(f"DEVICE: {cupy.cuda.runtime.getDeviceProperties(0)['name'].decode()}")
        except Exception as e:
            print(f"cupy unavailable ({e}); CPU")

    if args.gate or args.all:
        if not gate(xp):
            print("GATES FAILED — refusing to score any prediction.")
            return 1
    if args.hscan or args.all:
        run_hscan(args, xp)
    if args.collapse or args.all:
        run_collapse(args, xp)
    if args.rscan or args.all:
        run_rscan(args, xp)
    if args.sat or args.all:
        run_sat(args, xp)
    if args.hsq or args.all:
        run_hsq(args, xp)
    if args.sat2 or args.all:
        run_sat2(args, xp)
    if args.stepa or args.all:
        run_stepa(args, xp)
    if args.yh or args.all:
        run_yh(args, xp)
    if args.gap or args.all:
        run_gap(args, xp)
    if args.bulk or args.all:
        run_bulk(args, xp)
    if args.mc or args.all:
        run_mc(args, xp)
    return 0


if __name__ == '__main__':
    sys.exit(main())
