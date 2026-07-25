"""habit_ratio.py — FOLLOW-UP to habit_dynamics.py (results 6b97e15).

Three additions requested after the main run, all on measurement (1) LIFESPAN:

  A. THE DIMENSIONLESS RATIO tau_share / tau_pair. tau in kernel steps is
     unit-dependent and cannot classify across conditions; the ratio is
     clock-independent and answers the real question — does whole-only structure
     OUTLIVE pairwise structure (>1, DEEP HABIT), track it (~1), or die first (<1,
     FRAGILE)? Measured at every grid point, by two matched model-free definitions
     because the share decay rejects BOTH fitted families (so no fitted tau_share
     exists to divide with).

  B. IS THE DECAY QUANTIZED? Code/stabilizer states carry share at integer multiples
     of ln2. A substrate shedding whole-only bits one at a time would show PLATEAUS
     near integers in share/ln2. Curves are reported in units of ln2; no fit is forced.

  C. NULL VALIDITY AT HIGH COUPLING. The sibling run (ARRAY_CAP_RESULTS.md DIAG B)
     found the iid multinomial surrogate BROKEN for clip at kappa >= 0.35 (tau_int
     87-365, cross-run channels firing at z=34.9). This script runs the matching
     cross-run control for THIS reading — channels drawn from three independent runs,
     which cannot share structure — and reports where our own z-scores may be quoted.

Trajectories are reproduced with the same seeds/settle/N as habit_dynamics.py's
taxonomy, so the pair curves join to habit_taxonomy.json row-for-row.

Usage:  python3 habit_ratio.py --run
"""
import sys, os, json, time, argparse
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/emoore/CIRISArray')
sys.path.insert(0, '/home/emoore/CIRISArray/src')
sys.path.insert(0, HERE)

import habit_dynamics as HD
from habit_dynamics import (run_traj, lag_channels, analyze_at, TAX_DELTAS, CAP3)
import bench_detector as BD

LN2 = float(np.log(2))


# --- acf_time: COPIED VERBATIM from array_cap_diagnostics.py (sibling, DIAG B) -------
# Copied rather than imported because that module runs its full diagnostic at import.

def acf_time(x, maxlag=200):
    x = np.asarray(x, float) - np.mean(x)
    v = np.dot(x, x) / len(x)
    if v <= 0:
        return 0.0
    tau = 0.0
    for L in range(1, maxlag):
        c = np.dot(x[:-L], x[L:]) / (len(x) - L) / v
        if c <= 0:
            break
        tau += c
    return 1 + 2 * tau


def acf_time_units(sb, n_units=256, maxlag=200, window=32, rng=None):
    """Integrated autocorrelation time of the readout, averaged over independent
    (ossicle, cell) replica units, applied to the channel THIS experiment actually
    reads (oscillator b) rather than the phase metric.

    Returns THREE numbers, because the sibling's estimator is misleading here:
      tau_trunc  — the sibling's rule (stop at the first non-positive ACF term).
                   This substrate's ACF is OSCILLATORY with a strongly NEGATIVE lag-1
                   term, so the rule truncates immediately and returns 1.00 by
                   construction. That is an artifact of the stopping rule, not
                   evidence of independence, and must not be quoted as a clean bill.
      tau_fixed  — 1 + 2*sum_{L=1..window} rho(L), no truncation. With alternating
                   signs the sum largely cancels; tau_fixed < 1 means the samples are
                   ANTI-correlated and the effective sample size EXCEEDS T.
      acf1       — the lag-1 autocorrelation itself, so the sign is visible.
    """
    rng = rng or np.random.default_rng(0)
    U = sb.shape[1]
    idx = rng.choice(U, size=min(n_units, U), replace=False)
    x = sb[:, idx].astype(float)
    x = x - x.mean(axis=0, keepdims=True)
    v = (x * x).mean(axis=0)
    good = v > 0
    if not np.any(good):
        return 0.0, 0.0, 0.0
    x = x[:, good]; v = v[good]
    N = x.shape[0]
    rho = []
    for L in range(1, min(maxlag, N)):
        rho.append((x[:-L] * x[L:]).mean(axis=0) / v)
        if L >= window:
            break
    rho = np.array(rho)                                  # (L, units)
    # sibling's truncated rule
    tau_t = np.zeros(rho.shape[1]); running = np.ones(rho.shape[1], bool)
    for L in range(rho.shape[0]):
        running &= (rho[L] > 0)
        if not np.any(running):
            break
        tau_t += np.where(running, rho[L], 0.0)
    tau_trunc = float(np.mean(1 + 2 * tau_t))
    tau_fixed = float(np.mean(1 + 2 * rho.sum(axis=0)))
    return tau_trunc, tau_fixed, float(np.mean(rho[0]))


# --- model-free timescales ------------------------------------------------------------

def tau_e_crossing(d, y):
    """Lag INTERVAL over which y falls to 1/e of its value at the first lag, by
    log-linear interpolation. Model-free and identical in form for share and pair,
    so the two are matched and their ratio is meaningful."""
    d = np.asarray(d, float); y = np.asarray(y, float)
    if len(y) < 2 or y[0] <= 0:
        return float('nan')
    target = y[0] / np.e
    for i in range(1, len(y)):
        if y[i] <= target:
            if y[i] <= 0 or y[i - 1] <= 0:
                return float(d[i] - d[0])
            f = (np.log(y[i - 1]) - np.log(target)) / (np.log(y[i - 1]) - np.log(y[i]))
            return float(d[i - 1] + f * (d[i] - d[i - 1]) - d[0])
    return float('nan')            # never crossed within the swept range


def last_live(d, y, floor_mu, floor_sd, k=5.0):
    """Last lag whose value clears floor_mu + k*floor_sd."""
    live = [dd for dd, yy in zip(d, y) if yy > floor_mu + k * floor_sd]
    return float(max(live)) if live else 0.0


def pair_curve(sb, deltas, starts):
    """Pairwise meter vs lag on exactly the triples the share estimator sees."""
    mi, cr = [], []
    for D in deltas:
        ch = lag_channels(sb, D, starts)
        bits = np.column_stack([(x > np.median(x)).astype(np.int8) for x in ch])
        c, m, _, _ = BD.pair_meter(bits)
        cr.append(float(c)); mi.append(float(m))
    return np.array(mi), np.array(cr)


def starts_for(N, deltas, n_starts):
    hi = N - 1 - 2 * max(deltas)
    return np.unique(np.linspace(0, hi, n_starts).astype(int))


# =====================================================================================
# A + B — ratio and quantization over the taxonomy grid
# =====================================================================================

def run_grid(args, tax):
    rows = []
    for boundary in ('clip', 'fold'):
        for kap in args.kappas:
            for sig in args.sigmas:
                t0 = time.time()
                sb, rate = run_traj(kap, sig, boundary, args.seed, args.settle, args.Ntax)
                st = starts_for(args.Ntax, TAX_DELTAS, args.nstarts_tax)
                mi, cr = pair_curve(sb, TAX_DELTAS, st)
                tint, tfix, acf1 = acf_time_units(sb, rng=np.random.default_rng(args.seed))
                d = np.array(TAX_DELTAS, float)
                # pairwise floor from the large-lag plateau of the SAME curve
                tail = mi[d >= 96]
                fmu, fsd = float(tail.mean()), float(tail.std(ddof=1))
                key = (boundary, kap, sig)
                t = tax[key]
                y = np.array(t['excess'], float); s = np.array(t['sigma_pooled'], float)
                L_share = t['last_live_lag']
                L_pair = last_live(d, mi, fmu, fsd)
                te_share = tau_e_crossing(d, y)
                te_pair = tau_e_crossing(d, mi)
                rows.append(dict(
                    boundary=boundary, kappa=kap, sigma=sig, clip_rate=rate,
                    tau_int_trunc=tint, tau_int_fixed=tfix, acf1=acf1,
                    pair_mi=mi.tolist(), pair_corr=cr.tolist(),
                    pair_floor_mu=fmu, pair_floor_sd=fsd,
                    L_share=L_share, L_pair=L_pair,
                    ratio_L=(L_share / L_pair) if L_pair > 0 else float('nan'),
                    tau_e_share=te_share, tau_e_pair=te_pair,
                    ratio_tau_e=(te_share / te_pair) if te_pair and te_pair > 0 else float('nan'),
                    share_bits=(y / LN2).tolist(), CF=t['CF'], indep_z1=t['indep_z1'],
                    tie=t['tie']))
                r = rows[-1]
                print(f"  [{boundary}] k={kap:<5} s={sig:<7g} "
                      f"acf1={acf1:+.3f} tauFix={tfix:6.2f} "
                      f"L_sh={L_share:>5.0f} L_pr={L_pair:>5.0f} ratio_L={r['ratio_L']:>7.3f} "
                      f"tauE_sh={te_share:>6.2f} tauE_pr={te_pair:>6.2f} "
                      f"ratio_tauE={r['ratio_tau_e']:>6.3f} maxbits={max(y)/LN2:.4f} "
                      f"({time.time()-t0:.1f}s)")
                del sb
    return rows


# =====================================================================================
# C — cross-run control: channels from THREE independent runs cannot share structure
# =====================================================================================

def cross_run(args, points):
    out = []
    for (kap, sig, boundary) in points:
        trajs = []
        for sd in (args.seed, 424242, 777):
            sb, _ = run_traj(kap, sig, boundary, sd, args.settle, args.Ntax)
            trajs.append(sb)
        st = starts_for(args.Ntax, TAX_DELTAS, args.nstarts_tax)
        rng = np.random.default_rng(1234)
        D = 1
        # within-run reference (all three slots from run A)
        within = analyze_at(lag_channels(trajs[0], D, st), 'within',
                            n_surr=args.nsurr, n_shuf=0, rng=rng)
        # cross-run: slot j from run j — independent by construction, true share = 0
        ch = [np.concatenate([trajs[j][s + j * D] for s in st]).astype(np.float64)
              for j in range(3)]
        cross = analyze_at(ch, 'cross', n_surr=args.nsurr, n_shuf=0, rng=rng)
        tint, tfix, acf1 = acf_time_units(trajs[0], rng=np.random.default_rng(args.seed))
        out.append(dict(kappa=kap, sigma=sig, boundary=boundary,
                        tau_int_trunc=tint, tau_int_fixed=tfix, acf1=acf1,
                        within_share=within['share'], within_z=within['z'],
                        cross_share=cross['share'], cross_z=cross['z'],
                        cross_excess=cross['excess'], tie=cross['tie_max'],
                        verdict=('NULL_BROKEN' if abs(cross['z']) > 5 else 'NULL_SOUND')))
        r = out[-1]
        print(f"  k={kap:<5} s={sig:<7g} {boundary:<5} acf1={acf1:+.3f} "
              f"tauTrunc={tint:5.2f} tauFix={tfix:6.2f} | "
              f"within z={within['z']:>9.1f} | CROSS-RUN share={cross['share']:.3e} "
              f"z={cross['z']:>9.1f} -> {r['verdict']}")
        del trajs
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', action='store_true')
    ap.add_argument('--seed', type=int, default=20260725)
    ap.add_argument('--settle', type=int, default=2000)
    ap.add_argument('--Ntax', type=int, default=512)
    ap.add_argument('--nstarts-tax', type=int, default=8)
    ap.add_argument('--nsurr', type=int, default=60)
    ap.add_argument('--kappas', type=float, nargs='*',
                    default=[0.0, 0.02, 0.05, 0.10, 0.20, 0.35, 0.50])
    ap.add_argument('--sigmas', type=float, nargs='*',
                    default=[0.0, 1e-4, 1e-3, 1e-2, 1e-1])
    ap.add_argument('--out', type=str, default='habit_ratio_results.json')
    args = ap.parse_args()

    taxrows = json.load(open(os.path.join(HERE, 'habit_taxonomy.json')))['taxonomy']
    tax = {(r['boundary'], r['kappa'], r['sigma']): r for r in taxrows}

    print("=" * 100)
    print("A+B — tau_share/tau_pair ratio and quantization check, over the taxonomy grid")
    print("=" * 100)
    grid = run_grid(args, tax)

    print("\n" + "=" * 100)
    print("C — CROSS-RUN CONTROL: three independent runs; any |z|>5 proves the null broken")
    print("=" * 100)
    pts = [(0.05, 1e-3, 'clip'), (0.20, 1e-3, 'clip'), (0.35, 1e-3, 'clip'),
           (0.50, 1e-2, 'clip'), (0.35, 1e-3, 'fold'), (0.20, 1e-3, 'fold')]
    cr = cross_run(args, pts)

    # ---- lifespan-measurement ratio, from the 5-seed run already on disk ----
    life = json.load(open(os.path.join(HERE, 'habit_lifespan.json')))['lifespan']
    lif = {}
    for b in ('clip', 'fold'):
        L = life[b]
        d = np.array(L['deltas'], float)
        y = np.array(L['excess_mean'], float)
        s = np.array(L['excess_sem'], float)
        rows = L['rows']
        mi = np.array([np.mean([r['pair_maxMI'] for r in rows if r['delta'] == D])
                       for D in L['deltas']])
        tail = mi[d >= 64]
        fmu, fsd = float(tail.mean()), float(tail.std(ddof=1))
        L_share = last_live(d, y, 0.0, float(np.mean(s)))
        L_pair = last_live(d, mi, fmu, fsd)
        lif[b] = dict(L_share=L_share, L_pair=L_pair, ratio_L=L_share / L_pair,
                      tau_e_share=tau_e_crossing(d, y), tau_e_pair=tau_e_crossing(d, mi),
                      pair_mi=mi.tolist(), share_bits=(y / LN2).tolist(),
                      pair_floor_mu=fmu, pair_floor_sd=fsd)
        lif[b]['ratio_tau_e'] = lif[b]['tau_e_share'] / lif[b]['tau_e_pair']
    print("\n" + "=" * 100)
    print("MEASUREMENT 1 (kappa=0.05, 5 seeds) — the headline ratio")
    print("=" * 100)
    for b in ('clip', 'fold'):
        r = lif[b]
        print(f"  [{b}] L_share={r['L_share']:.0f} L_pair={r['L_pair']:.0f} "
              f"ratio_L={r['ratio_L']:.3f} | tau_e_share={r['tau_e_share']:.3f} "
              f"tau_e_pair={r['tau_e_pair']:.3f} ratio_tau_e={r['ratio_tau_e']:.3f}")
        print(f"        share in BITS (share/ln2) vs lag: "
              f"{', '.join('%.5f' % v for v in r['share_bits'][:6])} ...")

    allbits = [max(g['share_bits']) for g in grid]
    print(f"\n  QUANTIZATION: largest whole-only share anywhere on the grid = "
          f"{max(allbits):.4f} bits (= {max(allbits)*LN2:.4f} nats). "
          f"Integer plateaus require >= 1 bit.")

    path = os.path.join(HERE, args.out)
    json.dump(dict(grid=grid, cross_run=cr, lifespan=lif), open(path, 'w'),
              indent=1, default=float)
    print(f"wrote {path}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
