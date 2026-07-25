"""habit_dynamics.py — habit formation and lifespan on the REAL CIRISArray.

Pre-registered in scratchpad/HABIT_DYNAMICS_PREREG.md (committed BEFORE this ran, cb0e841).

THREE MEASUREMENTS, all as functions of something, all shape-first:
  (1) LIFESPAN  — k=3 temporal share of oscillator b at (t, t+D, t+2D) vs lag D.
                  Fit exponential A*exp(-D/tau)+c against power law A*D^-alpha+c, AICc.
  (2) FORMATION — share at fixed small lag vs elapsed time since randomized init.
  (3) TAXONOMY  — (ceiling fraction, lifespan tau) over the coupling x noise grid.

NOT a claim of order-3 / whole-only structure in the array. The level is expected,
clip-sensitive and IAAFT-uncertifiable (2026-07-24 hunt). The OBSERVABLE IS THE SHAPE:
a constant additive artifact is absorbed by the free plateau term c and drops out of
tau / alpha / tau_form. See prereg S0.

Substrate: /home/emoore/CIRISArray/src/runtime.py, Ossicle.KERNEL_CODE, RTX 4090.
Share machinery and the clip/fold kernel builder are IMPORTED from the sibling
experiment array_cap_experiment.py, not reimplemented.

Lag unit = ONE kernel logistic iteration, so the kernel is driven with iterations=1.
Gate 2 checks bit-identity of 100 such calls against one iterations=100 call.

Usage:
    python3 habit_dynamics.py --gate
    python3 habit_dynamics.py --run            # all three (gate runs first)
    python3 habit_dynamics.py --run --only lifespan|formation|taxonomy
"""
import sys, os, json, time, argparse
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/emoore/CIRISArray')
sys.path.insert(0, '/home/emoore/CIRISArray/src')
sys.path.insert(0, HERE)

import array_cap_experiment as ACE          # share machinery + clip/fold kernel builder
from array_cap_experiment import (LN2, H, shareK, caps_and_checks, emp_dist,
                                  surrogate_null, shuffle_floor, binarize_median,
                                  build_kernel, make_runtime)

CAP3 = LN2                                   # (k-2)*ln2 at k=3, machine-checked (ShareK.lean)


# =====================================================================================
# ANALYSIS — same machinery as the sibling, but with an externally supplied threshold
# (the formation curve must hold the binarization threshold fixed across the transient)
# =====================================================================================

def analyze_at(chans, tag, thresh=None, n_surr=60, n_shuf=5, rng=None):
    """chans: list of k float arrays. thresh: per-channel threshold, or None for each
    channel's own median. Returns the full pre-registered readout."""
    if rng is None:
        rng = np.random.default_rng(0)
    bits, ties, meds = [], [], []
    for j, x in enumerate(chans):
        x = np.asarray(x, dtype=np.float64)
        m = float(np.median(x)) if thresh is None else float(thresh[j])
        bits.append((x > m).astype(np.int8))
        ties.append(float(np.mean(x == m)))
        meds.append(m)
    bits = np.column_stack(bits)
    p, T = emp_dist(bits)
    r = caps_and_checks(p)
    r.update(tag=tag, T=T, tie_max=max(ties), thresh=meds)
    # pair meter on the SAME binarized data — does whole-only outlive pairwise, or not?
    import bench_detector as BD
    mc, mmi, _, _ = BD.pair_meter(bits)
    r['pair_maxcorr'] = float(mc); r['pair_maxMI'] = float(mmi)
    if n_surr > 0:
        mu, sd = surrogate_null(p, T, n_surr=n_surr, rng=rng)
        r['null_mean'], r['null_sd'] = mu, sd
        r['excess'] = r['share'] - mu
        r['z'] = (r['share'] - mu) / sd if sd > 1e-15 else float('nan')
    else:
        r['null_mean'] = r['null_sd'] = float('nan')
        r['excess'] = float('nan'); r['z'] = float('nan')
    if n_shuf > 0:
        smu, ssd = shuffle_floor(bits, n_shuf=n_shuf, rng=rng)
        r['shuffle_mean'], r['shuffle_sd'] = smu, ssd
    else:
        r['shuffle_mean'] = r['shuffle_sd'] = float('nan')
    r['CF'] = r['excess'] / CAP3
    r['CF_raw'] = r['share'] / CAP3
    return r


def share_only(chans, thresh=None):
    """share alone, no nulls — for the cheap block error bar (blocks share the same T,
    so the estimator bias is common to them and cancels out of their spread)."""
    bits = []
    for j, x in enumerate(chans):
        x = np.asarray(x, dtype=np.float64)
        m = float(np.median(x)) if thresh is None else float(thresh[j])
        bits.append((x > m).astype(np.int8))
    p, _ = emp_dist(np.column_stack(bits))
    return shareK(p)[0]


# =====================================================================================
# FITS — exponential vs power law, both with a free plateau that absorbs a constant
# artifact. Nonlinear parameter scanned on a grid, linear (A, c) solved exactly at each
# point: no local minima, no optimizer to trust.
# =====================================================================================

def _wls_linear(g, y, w):
    """Weighted least squares of y ~ A*g + c. Returns A, c, chi2."""
    X = np.column_stack([g, np.ones_like(g)])
    W = w[:, None]
    beta, *_ = np.linalg.lstsq(X * np.sqrt(W), y * np.sqrt(w), rcond=None)
    resid = y - X @ beta
    return float(beta[0]), float(beta[1]), float(np.sum(w * resid ** 2))


def _wls_linear_noc(g, y, w):
    """Same with c fixed to 0."""
    A = float(np.sum(w * g * y) / np.sum(w * g * g))
    resid = y - A * g
    return A, 0.0, float(np.sum(w * resid ** 2))


def _aicc(chi2, n, p):
    if n - p - 1 <= 0:
        return chi2 + 2 * p
    return chi2 + 2 * p + 2 * p * (p + 1) / (n - p - 1)


def fit_family(d, y, sigma, family, with_c=True, refine=True):
    """family 'exp': A*exp(-d/tau)+c ; 'pow': A*d^-alpha+c."""
    d = np.asarray(d, float); y = np.asarray(y, float)
    sigma = np.asarray(sigma, float)
    sigma = np.where(sigma > 0, sigma, np.max(sigma[sigma > 0]) if np.any(sigma > 0) else 1.0)
    w = 1.0 / sigma ** 2
    solve = _wls_linear if with_c else _wls_linear_noc
    if family == 'exp':
        grid = np.exp(np.linspace(np.log(0.2), np.log(4000.0), 600))
        basis = lambda t: np.exp(-d / t)
    elif family == 'pow':
        grid = np.exp(np.linspace(np.log(0.02), np.log(12.0), 600))
        basis = lambda a: d ** (-a)
    else:
        raise ValueError(family)
    best = None
    for th in grid:
        A, c, chi2 = solve(basis(th), y, w)
        if best is None or chi2 < best[2]:
            best = (th, (A, c), chi2)
    if refine:
        th0 = best[0]
        fine = np.exp(np.linspace(np.log(th0 / 1.3), np.log(th0 * 1.3), 400))
        for th in fine:
            A, c, chi2 = solve(basis(th), y, w)
            if chi2 < best[2]:
                best = (th, (A, c), chi2)
    th, (A, c), chi2 = best
    p = 3 if with_c else 2
    n = len(d)
    # 1-sigma interval on the nonlinear parameter by delta-chi2 = 1 along the profile
    lo = hi = th
    grid2 = np.exp(np.linspace(np.log(th / 20), np.log(th * 20), 3000))
    prof = np.array([solve(basis(t), y, w)[2] for t in grid2])
    ok = grid2[prof <= chi2 + 1.0]
    if len(ok):
        lo, hi = float(ok.min()), float(ok.max())
    return dict(family=family, theta=float(th), theta_lo=lo, theta_hi=hi,
                A=A, c=c, chi2=chi2, n=n, p=p, aicc=_aicc(chi2, n, p),
                chi2_red=chi2 / max(n - p, 1))


def compare_decay(d, y, sigma):
    """Full pre-registered decay comparison. Returns both fits and the verdict."""
    d = np.asarray(d, float)
    fE = fit_family(d, y, sigma, 'exp', with_c=True)
    fP = fit_family(d, y, sigma, 'pow', with_c=True)
    fE0 = fit_family(d, y, sigma, 'exp', with_c=False)
    fP0 = fit_family(d, y, sigma, 'pow', with_c=False)
    dAIC = fP['aicc'] - fE['aicc']          # positive favours EXPONENTIAL
    # DEGENERATE test (prereg S3): no decay signal to fit
    y = np.asarray(y, float); sigma = np.asarray(sigma, float)
    snr = float(np.max(y / np.where(sigma > 0, sigma, np.inf)))
    drop = float(y[0] - np.median(y[-3:]))
    degenerate = (snr < 3.0) or (fE['A'] <= 0) or (drop <= 0)
    if degenerate:
        verdict = 'DEGENERATE'
    elif dAIC >= 10:
        verdict = 'EXPONENTIAL'
    elif dAIC <= -10:
        verdict = 'POWER_LAW'
    else:
        verdict = 'INDETERMINATE'

    # ---- POST-HOC ADEQUACY TESTS (added after the first run; see results S3) ----
    # The prereg fixed the MODEL-SELECTION rule but not a goodness-of-fit rule. A
    # winner by AIC can still be a model that does not describe the data at all, and
    # a shape parameter can land below the instrument's resolution. Both happened.
    # These do not replace the pre-registered verdict, which is reported unchanged.
    best = fE if fE['aicc'] <= fP['aicc'] else fP
    adequacy = 'OK' if best['chi2_red'] <= 5.0 else 'BOTH_REJECTED'
    dmin = float(np.min(d))
    unresolved = (verdict == 'EXPONENTIAL' and fE['theta'] < dmin)
    # the sharpest single falsifier: what the fitted model predicts at the first lag
    # that sits on the floor, in units of that point's own error bar
    onfloor = np.where(np.abs(y) <= 3 * sigma)[0]
    over = None
    if len(onfloor):
        i = int(onfloor[0])
        if best['family'] == 'exp':
            pred = best['A'] * np.exp(-d[i] / best['theta']) + best['c']
        else:
            pred = best['A'] * d[i] ** (-best['theta']) + best['c']
        over = dict(delta=float(d[i]), predicted=float(pred), observed=float(y[i]),
                    sigma=float(sigma[i]),
                    n_sigma=float((pred - y[i]) / sigma[i]) if sigma[i] > 0 else float('inf'))
    return dict(exp=fE, pow=fP, exp_noc=fE0, pow_noc=fP0, dAIC=float(dAIC),
                verdict=verdict, snr=snr, drop=drop,
                adequacy=adequacy, chi2_red_best=best['chi2_red'],
                unresolved=bool(unresolved), overprediction=over,
                verdict_final=('BOTH_REJECTED' if adequacy == 'BOTH_REJECTED'
                               else ('UNRESOLVED' if unresolved else verdict)))


# =====================================================================================
# THE REAL KERNEL, driven one logistic iteration per call
# =====================================================================================

def run_traj(kappa, sigma, boundary, seed, settle, N, iters=1, osc=1, record=True):
    """Drive the REAL kernel. Returns (states_b [N, U] float32, clamp_binding_rate).
    U = n_ossicles * n_cells independent replica units. Frames are accumulated on the
    GPU and copied once, so the inner loop has no host synchronisation."""
    import cupy as cp
    rt = make_runtime(3, 64, kappa, seed)
    kern = build_kernel(boundary)
    oss = rt.array.ossicles
    n = oss.n_ossicles
    ncells = oss.params.n_cells
    U = n * ncells
    clipbuf = cp.zeros(n, dtype=cp.float32)
    clipacc = cp.zeros(n, dtype=cp.float64)
    block = 256
    grid = (n + block - 1) // block
    args = (oss.states, oss.outputs, oss.baselines, oss.gpu_params,
            cp.int32(n), cp.int32(ncells), cp.int32(iters), clipbuf)

    def burst():
        if sigma > 0:
            oss.states += cp.random.normal(0, sigma, oss.states.shape, dtype=cp.float32)
        clipbuf.fill(0)
        kern((grid,), (block,), args)
        clipacc[...] += clipbuf

    for _ in range(settle):
        burst()
    buf = cp.empty((N, U), dtype=cp.float32) if record else None
    for t in range(N):
        burst()
        if record:
            buf[t] = oss.states[:, osc, :].reshape(U)
    cp.cuda.Stream.null.synchronize()
    denom = float(n * 3 * iters * ncells) * (settle + N)
    rate = float(clipacc.sum()) / denom
    out = cp.asnumpy(buf) if record else None
    del buf, clipbuf, clipacc, oss.states
    cp.get_default_memory_pool().free_all_blocks()
    return out, rate


def lag_channels(sb, delta, starts):
    """k=3 temporal reading: oscillator b at (t, t+D, t+2D), pooled over units."""
    return [np.concatenate([sb[s + j * delta] for s in starts]).astype(np.float64)
            for j in range(3)]


# =====================================================================================
# GATES
# =====================================================================================

def gate_kernel():
    """GATE 2 + 3 (prereg S6): the lag unit is honest, and the instrumentation is inert.
      2. sigma=0: 100 calls at iterations=1  ==  1 call at iterations=100, BIT-IDENTICAL.
      3. the clamp-counter build reproduces the SHIPPED kernel bit-identically (CLIP).
    """
    import cupy as cp
    print("-" * 78)
    print("GATE 2/3 — kernel equivalence and instrumentation fidelity (real device)")
    ok = True
    for boundary in ('clip', 'fold'):
        rt = make_runtime(3, 64, 0.05, 12345)
        oss = rt.array.ossicles
        n, ncells = oss.n_ossicles, oss.params.n_cells
        s0 = oss.states.copy()
        kern = build_kernel(boundary)
        clipbuf = cp.zeros(n, dtype=cp.float32)
        block = 256; grid = (n + block - 1) // block

        def call(iters):
            kern((grid,), (block,),
                 (oss.states, oss.outputs, oss.baselines, oss.gpu_params,
                  cp.int32(n), cp.int32(ncells), cp.int32(iters), clipbuf))
            cp.cuda.Stream.null.synchronize()

        oss.states[...] = s0
        for _ in range(100):
            call(1)
        many = oss.states.copy()
        oss.states[...] = s0
        call(100)
        one = oss.states.copy()
        identical = bool(cp.all(many == one))
        maxdiff = float(cp.abs(many - one).max())
        print(f"  [{boundary}] 100x(iterations=1) vs 1x(iterations=100): "
              f"bit-identical = {identical}  maxdiff = {maxdiff:.3e}")
        ok &= identical

    # instrumentation fidelity: counter build vs the SHIPPED kernel, CLIP, sigma=0
    rt = make_runtime(3, 64, 0.05, 999)
    oss = rt.array.ossicles
    n, ncells = oss.n_ossicles, oss.params.n_cells
    s0 = oss.states.copy()
    block = 256; grid = (n + block - 1) // block
    clipbuf = cp.zeros(n, dtype=cp.float32)
    kern = build_kernel('clip')
    oss.states[...] = s0
    kern((grid,), (block,), (oss.states, oss.outputs, oss.baselines, oss.gpu_params,
                             cp.int32(n), cp.int32(ncells), cp.int32(50), clipbuf))
    cp.cuda.Stream.null.synchronize()
    instr = oss.states.copy()
    oss.states[...] = s0
    oss.kernel((grid,), (block,), (oss.states, oss.outputs, oss.baselines, oss.gpu_params,
                                   cp.int32(n), cp.int32(ncells), cp.int32(50)))
    cp.cuda.Stream.null.synchronize()
    shipped = oss.states.copy()
    same = bool(cp.all(instr == shipped))
    print(f"  [clip] instrumented build vs SHIPPED Ossicle kernel (50 iters): "
          f"bit-identical = {same}")
    ok &= same
    print(f"GATE 2/3: {'PASS' if ok else 'FAIL'}")
    return ok


def gate_fits():
    """GATE 4 (prereg S6): the fitter recovers the generating shape and family."""
    print("-" * 78)
    print("GATE 4 — fit machinery self-test")
    rng = np.random.default_rng(7)
    d = np.array([1, 2, 3, 4, 6, 8, 11, 16, 23, 32, 45, 64, 91, 128, 181, 256], float)
    sig = np.full(len(d), 2e-4)
    ok = True
    ytrue = 0.010 * np.exp(-d / 25.0) + 0.0010
    r = compare_decay(d, ytrue + rng.normal(0, sig), sig)
    err = abs(r['exp']['theta'] - 25.0) / 25.0
    print(f"  exp truth tau=25   -> tau_hat={r['exp']['theta']:.2f} ({err*100:.1f}% err) "
          f"dAIC={r['dAIC']:+.1f} verdict={r['verdict']}")
    ok &= err < 0.05 and r['verdict'] == 'EXPONENTIAL'
    ytrue = 0.010 * d ** (-1.2) + 0.0010
    r = compare_decay(d, ytrue + rng.normal(0, sig), sig)
    err = abs(r['pow']['theta'] - 1.2) / 1.2
    print(f"  pow truth alpha=1.2 -> a_hat={r['pow']['theta']:.3f} ({err*100:.1f}% err) "
          f"dAIC={r['dAIC']:+.1f} verdict={r['verdict']}")
    ok &= err < 0.05 and r['verdict'] == 'POWER_LAW'
    r = compare_decay(d, rng.normal(0, sig), sig)
    print(f"  pure noise          -> verdict={r['verdict']} (DEGENERATE required)")
    ok &= r['verdict'] == 'DEGENERATE'
    print(f"GATE 4: {'PASS' if ok else 'FAIL'}")
    return ok


# =====================================================================================
# MEASUREMENT 1 — LIFESPAN
# =====================================================================================

DELTAS = [1, 2, 3, 4, 6, 8, 11, 16, 23, 32, 45, 64, 91, 128, 181, 256]


def lifespan_one(sb, deltas, n_starts, rng, n_surr=60, n_shuf=5, dmax=None,
                 indep_check=()):
    """One trajectory -> excess(D) for every D, plus block error bars and the
    independence-safe single-start z at the pre-registered lags."""
    N = sb.shape[0]
    dmax = dmax or max(deltas)
    hi = N - 1 - 2 * dmax
    starts = np.unique(np.linspace(0, hi, n_starts).astype(int))
    rows = []
    for D in deltas:
        ch = lag_channels(sb, D, starts)
        r = analyze_at(ch, f'D{D}', n_surr=n_surr, n_shuf=n_shuf, rng=rng)
        # block error bar: 4 temporally separated blocks of starts, same T each
        nb = 4
        blocks = np.array_split(starts, nb)
        bs = [share_only(lag_channels(sb, D, b)) for b in blocks if len(b)]
        r['block_sd'] = float(np.std(bs, ddof=1)) if len(bs) > 1 else float('nan')
        r['sigma_pooled'] = r['block_sd'] / np.sqrt(len(bs)) if len(bs) > 1 else float('nan')
        if D in indep_check:
            ch1 = lag_channels(sb, D, [int(N // 4)])
            r1 = analyze_at(ch1, f'D{D}-single', n_surr=n_surr, n_shuf=0, rng=rng)
            r['indep_share'] = r1['share']; r['indep_excess'] = r1['excess']
            r['indep_z'] = r1['z']; r['indep_T'] = r1['T']
        r['delta'] = D
        rows.append(r)
    return rows


def measurement_lifespan(args):
    print("=" * 78)
    print("MEASUREMENT 1 — LIFESPAN: k=3 temporal share vs lag (kernel iterations)")
    print("=" * 78)
    out = {}
    for boundary in ('clip', 'fold'):
        per_seed = []
        for sd in args.seeds:
            t0 = time.time()
            sb, rate = run_traj(args.kappa0, args.sigma0, boundary, sd,
                                args.settle, args.Nlife)
            rng = np.random.default_rng(sd)
            rows = lifespan_one(sb, DELTAS, args.nstarts, rng, n_surr=args.nsurr,
                                n_shuf=5, indep_check=(1, 8, 64, 256))
            for r in rows:
                r.update(seed=sd, boundary=boundary, clip_rate=rate)
            per_seed.append(rows)
            print(f"  [{boundary} seed={sd}] {time.time()-t0:.1f}s  clamp-binding {rate:.3e}  "
                  f"excess(D=1)={rows[0]['excess']:.3e}  excess(D=256)={rows[-1]['excess']:.3e}  "
                  f"tie={max(r['tie_max'] for r in rows):.4f}")
            del sb
        # across-seed mean and real error bar
        d = np.array(DELTAS, float)
        E = np.array([[r['excess'] for r in rows] for rows in per_seed])   # (S, D)
        mean = E.mean(axis=0)
        sem = E.std(axis=0, ddof=1) / np.sqrt(E.shape[0])
        sem = np.where(sem > 0, sem, np.nanmax(sem))
        cmp_ = compare_decay(d, mean, sem)
        out[boundary] = dict(deltas=DELTAS, excess_mean=mean.tolist(),
                             excess_sem=sem.tolist(),
                             excess_by_seed=E.tolist(), fit=cmp_,
                             rows=[r for rows in per_seed for r in rows],
                             clip_rate=per_seed[0][0]['clip_rate'])
        f = cmp_['exp']; g = cmp_['pow']
        op = cmp_['overprediction']
        print(f"  --> [{boundary}] PREREG VERDICT {cmp_['verdict']}  dAIC={cmp_['dAIC']:+.1f}  "
              f"| ADEQUACY {cmp_['adequacy']} chi2_red={cmp_['chi2_red_best']:.3g}  "
              f"FINAL {cmp_['verdict_final']}")
        if op:
            print(f"      first floor lag D={op['delta']:.0f}: model predicts "
                  f"{op['predicted']:.3e}, observed {op['observed']:.3e} "
                  f"+/- {op['sigma']:.1e}  -> over-predicts by {op['n_sigma']:.3g} sigma")
        print(f"      "
              f"tau={f['theta']:.2f} [{f['theta_lo']:.2f},{f['theta_hi']:.2f}]  "
              f"alpha={g['theta']:.3f} [{g['theta_lo']:.3f},{g['theta_hi']:.3f}]")
    # shape stability verdict
    out['stability'] = shape_stability(out['clip'], out['fold'])
    print(f"  --> SHAPE STABILITY (clip vs fold): {out['stability']['verdict']} "
          f"({out['stability']['note']})")
    return out


def shape_stability(a, b):
    """Prereg S3 discriminator, applied to the SHAPE not the level."""
    va, vb = a['fit']['verdict'], b['fit']['verdict']
    if a['clip_rate'] == 0.0:
        return dict(verdict='TRIVIAL', note='clamp-binding rate is exactly zero under CLIP; '
                    'clip and fold are the same function on the data that occurred',
                    clip=va, fold=vb)
    if va != vb:
        return dict(verdict='ARTIFACT', note=f'model family flips: clip={va} fold={vb}',
                    clip=va, fold=vb)
    if va in ('DEGENERATE', 'INDETERMINATE'):
        return dict(verdict='MARGINAL', note=f'both {va}; no shape parameter to compare',
                    clip=va, fold=vb)
    key = 'exp' if va == 'EXPONENTIAL' else 'pow'
    ta, tb = a['fit'][key]['theta'], b['fit'][key]['theta']
    rel = abs(ta - tb) / max(abs(ta), abs(tb))
    if rel <= 0.20:
        v = 'STABLE'
    elif rel > 1.0:
        v = 'ARTIFACT'
    else:
        v = 'MARGINAL'
    return dict(verdict=v, note=f'{key} theta clip={ta:.4g} fold={tb:.4g} rel_diff={rel:.3f}',
                clip=va, fold=vb, theta_clip=ta, theta_fold=tb, rel_diff=rel)


# =====================================================================================
# MEASUREMENT 2 — FORMATION
# =====================================================================================

def measurement_formation(args):
    print("=" * 78)
    print("MEASUREMENT 2 — FORMATION: share at fixed small lag vs elapsed time from "
          "randomized init")
    print("=" * 78)
    out = {}
    for boundary in ('clip', 'fold'):
        for Df in (args.Df, args.Df2):
            curves, rates = [], []
            for i, sd in enumerate(args.form_seeds):
                sb, rate = run_traj(args.kappa0, args.sigma0, boundary, sd, 0, args.Nform)
                rates.append(rate)
                late = sb[int(0.75 * args.Nform):]
                # PRIMARY: attractor threshold, fixed across the transient.
                # SENSITIVITY (--form-perT, prereg S4): threshold recomputed within each t.
                thr = None if args.form_perT else [float(np.median(late))] * 3
                rng = np.random.default_rng(sd + 1000 * Df)
                ts, ex, zs, sh = [], [], [], []
                for t in range(args.Nform - 2 * Df):
                    ch = [sb[t + j * Df].astype(np.float64) for j in range(3)]
                    r = analyze_at(ch, f't{t}', thresh=thr, n_surr=args.nsurr_form,
                                   n_shuf=0, rng=rng)
                    ts.append(t); ex.append(r['excess']); zs.append(r['z']); sh.append(r['share'])
                curves.append(ex)
                if i == 0:
                    out[f'{boundary}_D{Df}_z'] = zs
                    out[f'{boundary}_D{Df}_share_seed0'] = sh
                del sb
            C = np.array(curves)
            mean = C.mean(axis=0)
            sem = C.std(axis=0, ddof=1) / np.sqrt(C.shape[0])
            t = np.arange(len(mean))
            res = formation_stats(t, mean, sem)
            res['clip_rate'] = float(np.mean(rates))
            out[f'{boundary}_D{Df}'] = dict(t=t.tolist(), excess_mean=mean.tolist(),
                                            excess_sem=sem.tolist(), **res)
            print(f"  [{boundary} D={Df}] VERDICT {res['verdict']}  "
                  f"excess(0)={mean[0]:.3e}  E_inf={res['E_inf']:.3e}  "
                  f"tau_form={res['tau_form']}  t90={res['t90']}  "
                  f"rho={res['spearman']:.3f}  clamp {np.mean(rates):.3e}")
    return out


def formation_stats(t, y, sem):
    """Prereg S4 outcome assignment."""
    from scipy.stats import spearmanr
    n = len(y)
    tail = y[int(0.75 * n):]
    E_inf = float(np.mean(tail))
    floor_sd = float(np.mean(sem))
    half = slice(0, n // 2)
    rho, pv = spearmanr(t[half], y[half])
    # fit E_inf*(1-exp(-t/tau)) by scanning tau, amplitude solved linearly
    w = 1.0 / np.where(sem > 0, sem, np.nanmax(sem)) ** 2
    best = None
    for tau in np.exp(np.linspace(np.log(0.2), np.log(2000.0), 900)):
        g = 1 - np.exp(-t / tau)
        A = float(np.sum(w * g * y) / max(np.sum(w * g * g), 1e-30))
        chi2 = float(np.sum(w * (y - A * g) ** 2))
        if best is None or chi2 < best[2]:
            best = (tau, A, chi2)
    tau_form, A_form, chi2 = best
    idx = np.where(y >= 0.9 * E_inf)[0]
    t90 = int(idx[0]) if len(idx) and E_inf > 0 else None
    plateau_clears = abs(E_inf) > 3 * floor_sd
    if not plateau_clears:
        verdict = 'NONE'
    elif y[0] > E_inf + 3 * floor_sd:
        verdict = 'DECAYS'
    elif abs(y[0] - E_inf) <= 0.10 * abs(E_inf):
        verdict = 'ALREADY_THERE'
    elif rho > 0 and pv < 0.01:
        verdict = 'BUILDS'
    else:
        verdict = 'INDETERMINATE'
    return dict(verdict=verdict, E_inf=E_inf, y0=float(y[0]), floor_sd=floor_sd,
                tau_form=float(tau_form), A_form=float(A_form), chi2=chi2,
                t90=t90, spearman=float(rho), spearman_p=float(pv))


# =====================================================================================
# MEASUREMENT 3 — TAXONOMY
# =====================================================================================

TAX_DELTAS = [1, 2, 3, 4, 5, 6, 8, 11, 16, 23, 32, 48, 64, 96, 128, 192]


def measurement_taxonomy(args):
    print("=" * 78)
    print("MEASUREMENT 3 — TAXONOMY: (ceiling fraction, lifespan) over coupling x noise")
    print("=" * 78)
    rows = []
    for boundary in ('clip', 'fold'):
        for kap in args.kappas:
            for sig in args.sigmas:
                t0 = time.time()
                sb, rate = run_traj(kap, sig, boundary, args.seed, args.settle, args.Ntax)
                rng = np.random.default_rng(args.seed)
                rr = lifespan_one(sb, TAX_DELTAS, args.nstarts_tax, rng,
                                  n_surr=args.nsurr_tax, n_shuf=0, indep_check=(1,))
                d = np.array(TAX_DELTAS, float)
                y = np.array([r['excess'] for r in rr])
                s = np.array([r['sigma_pooled'] for r in rr])
                s = np.where(np.isfinite(s) & (s > 0), s, np.nanmax(s[np.isfinite(s)]))
                cmp_ = compare_decay(d, y, s)
                cf = rr[0]['CF']
                vf = cmp_['verdict_final']
                # a lifespan is quoted only when a family actually describes the curve
                # AND the fitted constant sits at or above the instrument's resolution
                tau = cmp_['exp']['theta'] if vf == 'EXPONENTIAL' else float('nan')
                # model-free lifespan, always defined: the last lag clearing the floor
                lam = [dd for dd, yy, ss in zip(d, y, s) if yy > 5 * ss]
                lam = float(max(lam)) if lam else 0.0
                rows.append(dict(boundary=boundary, kappa=kap, sigma=sig, CF=cf,
                                 CF_raw=rr[0]['CF_raw'], share1=rr[0]['share'],
                                 z1=rr[0]['z'], indep_z1=rr[0].get('indep_z'),
                                 tie=max(r['tie_max'] for r in rr), clip_rate=rate,
                                 verdict=cmp_['verdict'], verdict_final=vf,
                                 adequacy=cmp_['adequacy'],
                                 chi2_red=cmp_['chi2_red_best'],
                                 overpred=cmp_['overprediction'],
                                 dAIC=cmp_['dAIC'], last_live_lag=lam,
                                 tau=tau, alpha=cmp_['pow']['theta'],
                                 tau_lo=cmp_['exp']['theta_lo'], tau_hi=cmp_['exp']['theta_hi'],
                                 excess=y.tolist(), sigma_pooled=s.tolist(),
                                 cap_ok=rr[0]['chk_cap_robust'],
                                 cap_hl_ok=rr[0]['chk_cap_headline'],
                                 corner=corner_of(cf, lam, vf)))
                print(f"  [{boundary}] k={kap:<5} s={sig:<7g} CF={cf:+.4f} "
                      f"lastlag={lam:>6.0f} tau={tau:>8.2f} {vf:<14} "
                      f"corner={rows[-1]['corner']:<17} clamp={rate:.2e} "
                      f"({time.time()-t0:.1f}s)")
                del sb
    return rows


def corner_of(cf, lifespan, verdict):
    """Prereg S5 corners. `lifespan` is the model-free last lag clearing the floor,
    used in place of the fitted tau because the fits proved inadequate (results S3);
    the thresholds themselves (CF >= 0.10, lifespan >= 20 iterations) are unchanged."""
    if not np.isfinite(lifespan):
        return 'unclassifiable'
    hi_cf = cf >= 0.10
    long_t = lifespan >= 20.0
    if hi_cf and long_t:
        return 'congealed-habit'
    if hi_cf and not long_t:
        return 'chaotic-churn'
    if (not hi_cf) and long_t:
        return 'frozen-but-empty'
    return 'memoryless-like'


def ascii_map(rows, boundary, key, kappas, sigmas, fmt='{:>9.4f}'):
    lines = []
    wid = 18 if key == 'corner' else 10
    lines.append(f'  sigma \\ kappa ' + ''.join(f'{k:>{wid}g}' for k in kappas))
    for s in sigmas:
        cells = []
        for k in kappas:
            m = [r for r in rows if r['boundary'] == boundary and r['kappa'] == k
                 and r['sigma'] == s]
            v = m[0][key] if m else float('nan')
            if isinstance(v, str):
                cells.append(f'{v[:17]:>18}')
            elif isinstance(v, (int, float)) and np.isfinite(v):
                cells.append(fmt.format(v))
            else:
                cells.append(f'{"n/a":>10}')
        lines.append(f'  {s:<13g}' + ''.join(cells))
    return '\n'.join(lines)


# =====================================================================================

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gate', action='store_true')
    ap.add_argument('--run', action='store_true')
    ap.add_argument('--only', type=str, default='all')
    ap.add_argument('--seed', type=int, default=20260725)
    ap.add_argument('--seeds', type=int, nargs='*', default=[20260725, 99, 7, 1337, 4242])
    ap.add_argument('--form-seeds', type=int, nargs='*',
                    default=[20260725, 99, 7, 1337, 4242, 555, 8080, 31337])
    ap.add_argument('--kappa0', type=float, default=0.05)
    ap.add_argument('--sigma0', type=float, default=1e-3)
    ap.add_argument('--settle', type=int, default=2000)
    ap.add_argument('--Nlife', type=int, default=1024)
    ap.add_argument('--Nform', type=int, default=256)
    ap.add_argument('--Ntax', type=int, default=512)
    ap.add_argument('--Df', type=int, default=1)
    ap.add_argument('--Df2', type=int, default=4)
    ap.add_argument('--form-perT', action='store_true')
    ap.add_argument('--nstarts', type=int, default=16)
    ap.add_argument('--nstarts-tax', type=int, default=8)
    ap.add_argument('--nsurr', type=int, default=60)
    ap.add_argument('--nsurr-form', type=int, default=30)
    ap.add_argument('--nsurr-tax', type=int, default=40)
    ap.add_argument('--kappas', type=float, nargs='*',
                    default=[0.0, 0.02, 0.05, 0.10, 0.20, 0.35, 0.50])
    ap.add_argument('--sigmas', type=float, nargs='*',
                    default=[0.0, 1e-4, 1e-3, 1e-2, 1e-1])
    ap.add_argument('--out', type=str, default='habit_dynamics_results.json')
    args = ap.parse_args()

    print("#" * 78)
    print("# GATE — machinery, kernel equivalence, instrumentation, fits")
    print("#" * 78)
    ok = ACE.gate()
    ok &= gate_kernel()
    ok &= gate_fits()
    if not ok:
        print("\nGATE FAILED — refusing to measure.")
        return 1
    if args.gate and not args.run:
        return 0

    import cupy as cp
    print(f"\nDEVICE: {cp.cuda.runtime.getDeviceProperties(0)['name'].decode()}\n")
    res = dict(args=vars(args))
    t0 = time.time()
    if args.only in ('all', 'lifespan'):
        res['lifespan'] = measurement_lifespan(args)
    if args.only in ('all', 'formation'):
        res['formation'] = measurement_formation(args)
    if args.only in ('all', 'taxonomy'):
        rows = measurement_taxonomy(args)
        res['taxonomy'] = rows
        for boundary in ('clip', 'fold'):
            print(f"\n  === CEILING FRACTION (excess / (k-2)ln2) at D=1 — {boundary} ===")
            print(ascii_map(rows, boundary, 'CF', args.kappas, args.sigmas))
            print(f"\n  === LIFESPAN: last lag clearing the floor at z>5, kernel "
                  f"iterations — {boundary} ===")
            print(ascii_map(rows, boundary, 'last_live_lag', args.kappas, args.sigmas,
                            '{:>10.0f}'))
            print(f"\n  === fitted tau (quoted ONLY where a family is adequate) — "
                  f"{boundary} ===")
            print(ascii_map(rows, boundary, 'tau', args.kappas, args.sigmas, '{:>10.2f}'))
            print(f"\n  === CORNER — {boundary} ===")
            print(ascii_map(rows, boundary, 'corner', args.kappas, args.sigmas))
            print(f"\n  === clamp-binding rate — {boundary} ===")
            print(ascii_map(rows, boundary, 'clip_rate', args.kappas, args.sigmas,
                            '{:>10.2e}'))
        viol = [r for r in rows if not r['cap_ok']]
        print(f"\n  cap violations (robust bound): {len(viol)}")
    print(f"\ntotal {time.time()-t0:.1f}s")

    path = os.path.join(HERE, args.out)
    with open(path, 'w') as f:
        json.dump(res, f, indent=1, default=float)
    print(f"wrote {path}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
