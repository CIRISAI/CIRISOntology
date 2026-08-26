#!/usr/bin/env python3
"""
gcost_check.py -- numeric verification of the derived rent function f.

Adjudicates the stakes E1..E10 frozen in GCOST_DERIVATION.md Sec.7 BEFORE this file existed.

    THE LAW      G_inf(q) = q / (eps + q*lam),   eps = 1 - lam,
                 lam = decay eigenvalue of the tracked mode of the induced chain T_c
    THE FUNCTION f(gam, delta) = (1-delta)*gam / (gam + delta*(1-gam))
                 = minimum per-step repair dose holding retention >= 1-delta

ZERO FITTED PARAMETERS. Every constant is either a spectral quantity of the simulated
chain or a target chosen by the user. numpy only.
"""
import numpy as np

RNG = np.random.default_rng(20260826)
TOL_EXACT = 1e-12
TOL_BISECT = 1e-9

# ----------------------------------------------------------------------------
# the derived formulas -- written once, used everywhere, never refitted
# ----------------------------------------------------------------------------

def G_law(q, lam):
    """Stationary retention of the tracked mode. Derivation Sec.3.2."""
    eps = 1.0 - lam
    return q / (eps + q * lam)

def f_rent(gam, delta):
    """W*(gam, delta): minimum repair dose for retention >= 1-delta. Derivation Sec.4."""
    return (1.0 - delta) * gam / (gam + delta * (1.0 - gam))

def G_periodic(P, lam):
    """Cycle-averaged retention, full-strength reset every P steps. Derivation Sec.4.4."""
    if abs(1.0 - lam) < 1e-15:
        return 1.0
    return (1.0 - lam ** P) / (P * (1.0 - lam))

# ----------------------------------------------------------------------------
# chain construction: symmetric doubly-stochastic M, then T = (1-a) I + a M
# so the gap gam = a * (1 - m2) is tunable with the eigenvectors held fixed.
# ----------------------------------------------------------------------------

def sym_doubly_stochastic(n, rng, iters=500):
    A = rng.random((n, n)) + 0.05
    A = 0.5 * (A + A.T)
    for _ in range(iters):                      # symmetric Sinkhorn
        d = A.sum(axis=1)
        A = A / np.sqrt(np.outer(d, d))
        A = 0.5 * (A + A.T)
    return A / A.sum(axis=1, keepdims=True)

def chain_with_gap(M, gam_req):
    """T = (1-a)I + a M, a chosen to put the gap near gam_req.

    The REQUESTED gap is only a way to spread the grid.  Every prediction below uses the
    gap MEASURED off T (see actual_gap), because the derivation says eps is a spectral
    quantity of T_c -- read off the object, never assumed from the construction."""
    w = np.linalg.eigvalsh(M)
    m2 = np.max(w[w < 1.0 - 1e-9])              # second largest ALGEBRAIC eigenvalue
    a = min(gam_req / (1.0 - m2), 1.0)
    n = M.shape[0]
    T = (1.0 - a) * np.eye(n) + a * M
    assert np.linalg.eigvalsh(T).min() > 0, "non-lazy chain: tracked mode would oscillate"
    return T

def modes(T):
    """T symmetric -> orthonormal eigenbasis; eigenvalues sorted DESCENDING (algebraic).
    Index 0 is the stationary mode (eigenvalue 1); index 1 is the slowest decaying mode."""
    w, V = np.linalg.eigh(T)
    order = np.argsort(-w)
    return w[order], V[:, order]

def actual_gap(T):
    """gamma = 1 - lambda_2, measured off the chain."""
    return 1.0 - modes(T)[0][1]

# ----------------------------------------------------------------------------
# stationary states, solved exactly (no iteration-to-convergence anywhere)
# ----------------------------------------------------------------------------

def stat_affine_decay_first(T, p_des, q):
    """p_inf = (1-q) p_inf T + q p_des   (A5: decay then repair)."""
    n = T.shape[0]
    Aop = np.eye(n) - (1.0 - q) * T.T
    return np.linalg.solve(Aop, q * p_des)

def stat_affine_repair_first(T, p_des, q):
    """p_inf = ((1-q) p_inf + q p_des) T   (Sec.3.3)."""
    n = T.shape[0]
    Aop = np.eye(n) - (1.0 - q) * T.T
    return np.linalg.solve(Aop, q * (T.T @ p_des))

def stat_general_kernel(P):
    """Stationary distribution of an explicit kernel P (row-stochastic)."""
    n = P.shape[0]
    A = np.vstack([P.T - np.eye(n), np.ones(n)])
    b = np.zeros(n + 1); b[-1] = 1.0
    return np.linalg.lstsq(A, b, rcond=None)[0]

def retention(p_inf, mu, delta0):
    """Ledger coordinate = projection of (p_inf - mu) on the design deviation. Assumption A2."""
    return float(np.dot(p_inf - mu, delta0) / np.dot(delta0, delta0))

def bisect_wstar(Gfun, target, lo=0.0, hi=1.0, tol=TOL_BISECT):
    """Smallest q in [lo,hi] with Gfun(q) >= target. Gfun assumed monotone increasing."""
    if Gfun(hi) < target:
        return np.nan
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if Gfun(mid) >= target:
            hi = mid
        else:
            lo = mid
    return hi

# ----------------------------------------------------------------------------

GAMMAS = [0.02, 0.05, 0.12, 0.30, 0.60]          # > 1.5 orders of magnitude
QS = [0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.35, 0.5, 0.7, 0.9, 0.99]
DELTAS = [0.5, 0.2, 0.05, 0.02, 0.005]
N = 8

results = {}
def record(tag, ok, detail):
    results[tag] = (ok, detail)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag}: {detail}")

print("=" * 78)
print("gcost_check.py -- adjudicating GCOST_DERIVATION.md Sec.7 stakes E1..E10")
print("ZERO fitted parameters.  gamma grid:", GAMMAS)
print("=" * 78)

M = sym_doubly_stochastic(N, RNG)

# ---------------------------------------------------------------- E1 + E7 ---
print("\nE1 -- single tracked mode, affine deposit, decay-then-repair")
print(f"{'req':>6} {'gamma':>10} {'lam':>10} {'eps':>10} {'max|G-Glaw|':>14} {'max|Grf-lam*G|':>16}")
e1_worst = 0.0; e7_worst = 0.0
for gam_req in GAMMAS:
    T = chain_with_gap(M, gam_req)
    gam = actual_gap(T)
    w, V = modes(T)
    lam = w[1]                                  # slowest non-unit mode
    v2 = V[:, 1]
    mu = np.ones(N) / N
    s0 = 0.9 * (1.0 / N) / np.max(np.abs(v2))
    delta0 = s0 * v2
    p_des = mu + delta0
    assert p_des.min() > 0
    e1 = 0.0; e7 = 0.0
    for q in QS:
        G = retention(stat_affine_decay_first(T, p_des, q), mu, delta0)
        e1 = max(e1, abs(G - G_law(q, lam)))
        Grf = retention(stat_affine_repair_first(T, p_des, q), mu, delta0)
        e7 = max(e7, abs(Grf - lam * G_law(q, lam)))
    e1_worst = max(e1_worst, e1); e7_worst = max(e7_worst, e7)
    print(f"{gam_req:6.2f} {gam:10.6f} {lam:10.6f} {1-lam:10.6f} {e1:14.3e} {e7:16.3e}")
record("E1", e1_worst < TOL_EXACT, f"max |G_measured - q/(eps+q*lam)| = {e1_worst:.3e} (bar 1e-12)")
record("E7", e7_worst < TOL_EXACT, f"repair-then-decay = lam x decay-then-repair to {e7_worst:.3e}")

# ---------------------------------------------------------------------- E2 ---
print("\nE2 -- W* by bisection on the simulated chain vs f(gamma, delta)")
print("     gamma is MEASURED off T (1 - lambda_2), not taken from the construction")
print(f"{'req':>6} {'gamma':>10} {'delta':>7} {'W* measured':>13} {'f(gam,delta)':>13} {'abs err':>11}")
e2_worst = 0.0
for gam_req in GAMMAS:
    T = chain_with_gap(M, gam_req)
    w, V = modes(T); lam = w[1]; v2 = V[:, 1]
    gam = 1.0 - lam
    mu = np.ones(N) / N
    delta0 = (0.9 * (1.0 / N) / np.max(np.abs(v2))) * v2
    p_des = mu + delta0
    for d in DELTAS:
        Gf = lambda q: retention(stat_affine_decay_first(T, p_des, q), mu, delta0)
        wm = bisect_wstar(Gf, 1.0 - d)
        wp = f_rent(gam, d)
        err = abs(wm - wp)
        e2_worst = max(e2_worst, err)
        print(f"{gam_req:6.2f} {gam:10.6f} {d:7.3f} {wm:13.9f} {wp:13.9f} {err:11.3e}")
record("E2", e2_worst < 2 * TOL_BISECT,
       f"max |W*_measured - f| = {e2_worst:.3e} (bar 2e-9, bisection tol 1e-9)")

# ---------------------------------------------------------------------- E3 ---
print("\nE3 -- generic multi-mode deviation: f must be a FLOOR (G <= G_pred, W* >= f)")
print(f"{'gamma':>7} {'trial':>6} {'w2 share':>9} {'min(Gpred-G)':>13} {'min(W*-f)':>11}")
e3_viol = 0; e3_strict = 0; e3_cells = 0
for gam_req in GAMMAS:
    T = chain_with_gap(M, gam_req)
    w, V = modes(T); lam2 = w[1]; gam = 1.0 - lam2
    mu = np.ones(N) / N
    for trial in range(3):
        c = RNG.normal(size=N); c[0] = 0.0            # sum-zero: kill the stationary mode
        delta0 = V @ c
        delta0 = delta0 * (0.9 * (1.0 / N) / np.max(np.abs(delta0)))
        p_des = mu + delta0
        cc = V.T @ delta0
        wshare = cc[1] ** 2 / np.sum(cc[1:] ** 2)     # weight on the slowest mode
        gapG = np.inf; gapW = np.inf
        for q in QS:
            G = retention(stat_affine_decay_first(T, p_des, q), mu, delta0)
            gapG = min(gapG, G_law(q, lam2) - G)
            e3_cells += 1
            if G_law(q, lam2) - G < -1e-12: e3_viol += 1
        for d in DELTAS:
            Gf = lambda q: retention(stat_affine_decay_first(T, p_des, q), mu, delta0)
            wm = bisect_wstar(Gf, 1.0 - d)
            gapW = min(gapW, wm - f_rent(gam, d))
            if wm - f_rent(gam, d) < -2 * TOL_BISECT: e3_viol += 1
        if gapG > 1e-9: e3_strict += 1
        print(f"{gam:7.2f} {trial:6d} {wshare:9.4f} {gapG:13.3e} {gapW:11.3e}")
record("E3", e3_viol == 0,
       f"0 violations of the floor in {e3_cells} retention cells + {len(GAMMAS)*3*len(DELTAS)} "
       f"W* cells; strictly-below in {e3_strict}/{len(GAMMAS)*3} mixtures")

# ---------------------------------------------------------------------- E4 ---
print("\nE4 -- stochastic dosing (full reset w.p. q) has the SAME mean retention")
print("  AMENDMENT, declared: the frozen bar was 3*sd/sqrt(N) on a SINGLE run.  That estimator")
print("  is invalid here -- the samples are autocorrelated with time ~1/(1-(1-q)lam), so it")
print("  understates the standard error and is not a 3-sigma bar at all.  Both are reported:")
print("  the naive ratio (the letter of the stake) and the replicate-mean SE (a valid one).")
print(f"{'gamma':>7} {'q':>6} {'mean G':>10} {'pred':>10} {'naive x3SE':>11} {'repl x3SE':>10}")
e4_worst = 0.0; e4_naive_worst = 0.0
NREP, NSTEP = 40, 20000
for gam_req in [0.05, 0.30]:
    T = chain_with_gap(M, gam_req)
    w, V = modes(T); lam = w[1]; v2 = V[:, 1]
    delta0 = (0.9 * (1.0 / N) / np.max(np.abs(v2))) * v2
    nrm = np.dot(delta0, delta0)
    for q in [0.02, 0.1, 0.5]:
        rep_means = np.empty(NREP); pooled = []
        for r in range(NREP):
            d = delta0.copy(); s = np.empty(NSTEP)
            u = RNG.random(NSTEP)
            for t in range(NSTEP):
                d = d @ T
                if u[t] < q:
                    d = delta0.copy()
                s[t] = np.dot(d, delta0) / nrm
            rep_means[r] = s.mean(); pooled.append(s)
        m = rep_means.mean()
        se_rep = rep_means.std(ddof=1) / np.sqrt(NREP)
        alls = np.concatenate(pooled)
        se_naive = alls.std(ddof=1) / np.sqrt(alls.size)
        pred = G_law(q, lam)
        r_rep = abs(m - pred) / (3 * se_rep)
        r_nai = abs(m - pred) / (3 * se_naive)
        e4_worst = max(e4_worst, r_rep); e4_naive_worst = max(e4_naive_worst, r_nai)
        print(f"{1-lam:7.4f} {q:6.2f} {m:10.6f} {pred:10.6f} {r_nai:11.2f} {r_rep:10.2f}")
record("E4", e4_worst < 1.0,
       f"replicate-mean SE: worst |mean-pred| = {e4_worst:.2f} x 3SE (bar 1.0). "
       f"Naive single-run SE (the frozen, invalid estimator): {e4_naive_worst:.2f} x 3SE")

# ---------------------------------------------------------------------- E5 ---
print("\nE5 -- periodic dosing: closed form exact, and it BEATS continuous at matched q")
print(f"{'gamma':>7} {'P':>4} {'q=1/P':>7} {'periodic sim':>13} {'closed form':>12} {'continuous':>11}")
e5_err = 0.0; e5_beats = True
for gam in GAMMAS:
    T = chain_with_gap(M, gam)
    w, V = modes(T); lam = w[1]; v2 = V[:, 1]
    delta0 = (0.9 * (1.0 / N) / np.max(np.abs(v2))) * v2
    for P in [2, 5, 20, 50]:
        d = delta0.copy(); acc = []
        for k in range(P):
            acc.append(np.dot(d, delta0) / np.dot(delta0, delta0))
            d = d @ T
        sim = float(np.mean(acc))
        cf = G_periodic(P, lam)
        cont = G_law(1.0 / P, lam)
        e5_err = max(e5_err, abs(sim - cf))
        if not cf > cont + 1e-14: e5_beats = False
        print(f"{gam:7.2f} {P:4d} {1/P:7.3f} {sim:13.9f} {cf:12.9f} {cont:11.9f}")
record("E5", e5_err < TOL_EXACT and e5_beats,
       f"max |sim - (1-lam^P)/(P(1-lam))| = {e5_err:.3e}; periodic > continuous in every cell: {e5_beats}")

# ---------------------------------------------------------------------- E6 ---
print("\nE6 -- CONTROL: reading (a), proportional gain s -> (lam+q)s, must NOT match f")
print(f"{'gamma':>7} {'q/eps':>7} {'reading(a) G_inf':>17} {'law G_inf':>11} {'rel err':>10}")
e6_maxrel = 0.0
for gam in [0.05, 0.30]:
    lam = 1.0 - gam; eps = gam
    for r in [0.5, 0.9, 1.0, 1.1, 2.0]:
        q = r * eps
        rho = lam + q
        Ga = 0.0 if rho < 1 else (1.0 if abs(rho - 1) < 1e-15 else np.inf)
        Gl = G_law(q, lam)
        rel = np.inf if not np.isfinite(Ga) else abs(Ga - Gl) / Gl
        e6_maxrel = max(e6_maxrel, min(rel, 1e6))
        print(f"{gam:7.2f} {r:7.2f} {Ga:17.4g} {Gl:11.6f} {rel:10.4g}")
record("E6", e6_maxrel > 1.0,
       f"reading (a) departs from the law by up to {e6_maxrel:.3g} (>100% required): the check discriminates")

# ---------------------------------------------------------------------- E8 ---
print("\nE8 -- the ATLAS 2-bit chain, exact: lam = (1-2*eps_flip)^2")
print(f"{'eps_flip':>9} {'lam':>10} {'eps_chain':>10} {'q':>6} {'G exact':>10} {'q/(eps+q lam)':>14} {'err':>10}")
STATES = [(0, 0), (0, 1), (1, 0), (1, 1)]
CODE = {(0, 0), (1, 1)}
def atlas_kernel(epsf, w):
    idx = {s: i for i, s in enumerate(STATES)}
    P = np.zeros((4, 4))
    for s in STATES:
        for f1, p1 in ((0, 1 - epsf), (1, epsf)):
            for f2, p2 in ((0, 1 - epsf), (1, epsf)):
                t = (s[0] ^ f1, s[1] ^ f2); p = p1 * p2
                if t in CODE:
                    P[idx[s], idx[t]] += p
                else:
                    P[idx[s], idx[t]] += p * (1 - w)
                    P[idx[s], idx[(0, 0)]] += p * w * 0.5
                    P[idx[s], idx[(1, 1)]] += p * w * 0.5
    return P
e8_worst = 0.0
for epsf in [0.02, 0.05, 0.1, 0.2]:
    lam = (1 - 2 * epsf) ** 2
    for q in [0.1, 0.5, 0.794, 0.99]:
        pi = stat_general_kernel(atlas_kernel(epsf, q))
        pin = pi[0] + pi[3]
        G = 2 * pin - 1.0                        # A2: ledger zero is the induced equilibrium 1/2
        pred = G_law(q, lam)
        err = abs(G - pred); e8_worst = max(e8_worst, err)
        print(f"{epsf:9.2f} {lam:10.6f} {1-lam:10.6f} {q:6.3f} {G:10.6f} {pred:14.6f} {err:10.3e}")
record("E8", e8_worst < 1e-10, f"max |G_exact - law| = {e8_worst:.3e} with lam=(1-2eps)^2, no fit")

# ------------------------------------------------------------------ E9/E10 ---
print("\nE9/E10 -- second repair model: DAMAGE-CONDITIONAL reset (state-dependent, not affine)")

def lumpable_chain(n0, n1, alpha, beta, rng):
    """Exactly lumpable two-block chain; lumped kernel [[1-a,a],[b,1-b]], lam = 1-a-b."""
    n = n0 + n1
    W0 = rng.random((n0, n0)); W0 /= W0.sum(axis=1, keepdims=True)
    W1 = rng.random((n1, n1)); W1 /= W1.sum(axis=1, keepdims=True)
    u0 = rng.random(n0); u0 /= u0.sum()
    u1 = rng.random(n1); u1 /= u1.sum()
    T = np.zeros((n, n))
    T[:n0, :n0] = (1 - alpha) * W0
    T[:n0, n0:] = alpha * u1
    T[n0:, :n0] = beta * u0
    T[n0:, n0:] = (1 - beta) * W1
    return T, u0

def damage_conditional_kernel(T, n0, q, u0):
    """After the step, if outside the design block, reset to the design w.p. q."""
    n = T.shape[0]
    P = T.copy()
    leak = P[:, n0:].sum(axis=1) * q
    P[:, n0:] *= (1 - q)
    P[:, :n0] += np.outer(leak, u0)
    return P

print(f"{'case':>14} {'alpha':>6} {'beta':>6} {'lam':>9} {'q':>6} {'G exact':>10} {'law':>10} {'err':>10}")
e9_worst = 0.0
for (a, b) in [(0.03, 0.05), (0.10, 0.02), (0.25, 0.30)]:
    T, u0 = lumpable_chain(3, 4, a, b, RNG)
    lam = 1 - a - b
    n0 = 3
    mu_full = stat_general_kernel(T)
    mu0 = mu_full[:n0].sum()
    for q in [0.05, 0.2, 0.6, 0.95]:
        pi = stat_general_kernel(damage_conditional_kernel(T, n0, q, u0))
        s = pi[:n0].sum() - mu0
        G = s / (1.0 - mu0)
        pred = G_law(q, lam)
        err = abs(G - pred); e9_worst = max(e9_worst, err)
        print(f"{'lumpable':>14} {a:6.2f} {b:6.2f} {lam:9.6f} {q:6.2f} {G:10.6f} {pred:10.6f} {err:10.3e}")
record("E9", e9_worst < 1e-10,
       f"damage-conditional reset on a lumpable chain follows the law to {e9_worst:.3e} "
       f"with the LUMPED eps -- two repair models, one law")

# E9b: W* under the damage-conditional model vs f
print("\nE9b -- W* under the damage-conditional model vs f(gamma, delta)")
print(f"{'alpha':>6} {'beta':>6} {'gamma':>8} {'delta':>7} {'W* measured':>13} {'f':>13} {'err':>10}")
e9b_worst = 0.0
for (a, b) in [(0.03, 0.05), (0.25, 0.30)]:
    T, u0 = lumpable_chain(3, 4, a, b, RNG); n0 = 3
    gam = a + b
    mu0 = stat_general_kernel(T)[:n0].sum()
    for d in DELTAS:
        Gf = lambda q: (stat_general_kernel(damage_conditional_kernel(T, n0, q, u0))[:n0].sum()
                        - mu0) / (1.0 - mu0)
        wm = bisect_wstar(Gf, 1.0 - d)
        wp = f_rent(gam, d)
        err = abs(wm - wp); e9b_worst = max(e9b_worst, err)
        print(f"{a:6.2f} {b:6.2f} {gam:8.4f} {d:7.3f} {wm:13.9f} {wp:13.9f} {err:10.3e}")
record("E9b", e9b_worst < 2 * TOL_BISECT, f"max |W* - f| = {e9b_worst:.3e} under repair model 2")

# E10: non-lumpable partition -- the assumption must be load-bearing
print("\nE10 -- SCOPE: the same repair on a NON-lumpable partition")
Tn = sym_doubly_stochastic(7, RNG)
Tn = 0.6 * np.eye(7) + 0.4 * Tn
n0 = 3
u0 = np.zeros(3); u0[0] = 1.0
mu0 = stat_general_kernel(Tn)[:n0].sum()
# best-effort "lumped" lambda: the lumped 2-block kernel taken at the chain's stationary weights
mu_full = stat_general_kernel(Tn)
p0 = mu_full[:n0] / mu_full[:n0].sum(); p1 = mu_full[n0:] / mu_full[n0:].sum()
a_eff = float(p0 @ Tn[:n0, n0:].sum(axis=1)); b_eff = float(p1 @ Tn[n0:, :n0].sum(axis=1))
lam_eff = 1 - a_eff - b_eff
lump_defect = float(max(np.ptp(Tn[:n0, n0:].sum(axis=1)), np.ptp(Tn[n0:, :n0].sum(axis=1))))
print(f"  lumpability defect (spread of block-exit rates within a block) = {lump_defect:.3e}")
print(f"{'q':>6} {'G exact':>10} {'law(lam_eff)':>13} {'abs dev':>10}")
e10_dev = 0.0
for q in [0.05, 0.2, 0.6, 0.95]:
    pi = stat_general_kernel(damage_conditional_kernel(Tn, n0, q, u0))
    G = (pi[:n0].sum() - mu0) / (1.0 - mu0)
    pred = G_law(q, lam_eff)
    e10_dev = max(e10_dev, abs(G - pred))
    print(f"{q:6.2f} {G:10.6f} {pred:13.6f} {abs(G-pred):10.3e}")
record("E10", e10_dev > 1e-6,
       f"non-lumpable partition deviates by {e10_dev:.3e} -- the lumpability condition is load-bearing")

# ----------------------------------------------------------------------------
print("\n" + "=" * 78)
npass = sum(1 for ok, _ in results.values() if ok)
print(f"VERDICT: {npass}/{len(results)} stakes passed")
for tag, (ok, det) in results.items():
    print(f"  {'PASS' if ok else 'FAIL'}  {tag}: {det}")
print("=" * 78)
