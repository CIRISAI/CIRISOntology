"""array_negentropy_controls.py — the two controls of ARRAY_NEGENTROPY_PREREG_ADDENDUM.md.

Pre-registered in scratchpad/ARRAY_NEGENTROPY_PREREG_ADDENDUM.md, committed at 00bcd4e BEFORE
this file existed.  Both controls can RETRACT a result this run already reported as SURVIVED
(P5, the interior noise optimum), and are written so that they can.

CONTROL 1 — THE MIXTURE NULL (Kahle, Olbrich, Jost & Ay, PRE 79:026201 (2009)).
A convex combination of an ordered and a disordered distribution manufactures higher-order
structure with NO dynamics.  A noise sweep from sigma=0 to sigma=0.1 IS a sweep from ordered
to disordered, so it is exactly the case this null attacks.  Triples are drawn WHOLE from
endpoint pool A or B with probability 1-lambda / lambda, so each endpoint's own within-triple
dependence is preserved; the mixture then goes through the IDENTICAL pipeline at the same
sample size and frame count.  Bar: the dynamical peak must EXCEED the straight line's peak.

CONTROL 2 — DOSE VS RATE.
The stationary distribution of the noisy map depends on sigma but NOT on the settle length --
once settled.  The test is whether that is true.  If sigma* scales as 1/settle the array was
never settled and the interior optimum is a transient dose effect.  Bars: |slope| < 0.3 for
log sigma* vs log settle, and peak height changing < 10% on doubling settle 2000 -> 4000.

Usage:
    python3 array_negentropy_controls.py --mixture
    python3 array_negentropy_controls.py --dose
"""
import sys, os, json, argparse, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import array_negentropy as AN

LN2 = float(np.log(2))
SIGMAS = [0.0, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1]


def _bridge(chans):
    """The pipeline, verbatim: rank-Gaussianize -> moment tensor -> closed-form bridge."""
    g = [AN.gaussianize(c) for c in chans]
    M = AN.moment_tensor(*g)[None]
    C = np.array([[[1., M[0, 1, 1, 0], M[0, 1, 0, 1]],
                   [M[0, 1, 1, 0], 1., M[0, 0, 1, 1]],
                   [M[0, 1, 0, 1], M[0, 0, 1, 1], 1.]]])
    return float(AN.coord_deg3_closed(M, C)[0])


def share_from_raw(R, delta=1, chan=1, nuse=None):
    """s3 for the triple (x_t, x_{t+d}, x_{t+2d}) from RAW states R (nframes,3,T)."""
    n = R.shape[0] - 2 * delta if nuse is None else min(nuse, R.shape[0] - 2 * delta)
    ws = [_bridge([R[t, chan], R[t + delta, chan], R[t + 2 * delta, chan]]) for t in range(n)]
    m = float(np.mean(ws)); se = float(np.std(ws, ddof=1) / np.sqrt(len(ws)))
    return 0.5 * (m * m - se * se), m, se


def mixture(drv, args):
    import cupy as cp
    rng = np.random.default_rng(args.seed)
    out = []
    lams = np.round(np.arange(0.0, 1.0001, 0.05), 3)
    specs = [
        # (label, endpoint A, endpoint B, the dynamical sweep to compare against)
        ('sigma@k0.00', dict(k=0.00, s=0.0), dict(k=0.00, s=1e-1), 'sigma', 0.00),
        ('sigma@k0.02', dict(k=0.02, s=0.0), dict(k=0.02, s=1e-1), 'sigma', 0.02),
        ('sigma@k0.05', dict(k=0.05, s=0.0), dict(k=0.05, s=1e-1), 'sigma', 0.05),
        ('kappa@s1e-3', dict(k=0.00, s=1e-3), dict(k=0.60, s=1e-3), 'kappa', 1e-3),
    ]
    for bnd in ('clip', 'fold'):
        for (lab, A, B, axis, fixed) in specs:
            print(f"\n=== MIXTURE NULL [{lab}] boundary={bnd} ===")
            RA = drv.raw_states(A['k'], A['s'], bnd, args.seed, args.settle, args.nframes)
            RB = drv.raw_states(B['k'], B['s'], bnd, args.seed + 1, args.settle, args.nframes)
            T = RA.shape[2]
            # --- the straight line
            mix = []
            for lam in lams:
                ws = []
                for t in range(args.nuse):
                    msk = cp.asarray(rng.random(T) < lam)
                    ch = [cp.where(msk, RB[t + j, 1], RA[t + j, 1]) for j in range(3)]
                    ws.append(_bridge(ch))
                m = float(np.mean(ws)); se = float(np.std(ws, ddof=1) / np.sqrt(len(ws)))
                mix.append(0.5 * (m * m - se * se))
            mix = np.array(mix)
            jm = int(np.argmax(mix))
            # --- the dynamics, same settings, same estimator
            dyn, xs = [], []
            if axis == 'sigma':
                for s in SIGMAS:
                    R = drv.raw_states(fixed, s, bnd, args.seed, args.settle, args.nframes)
                    dyn.append(share_from_raw(R, nuse=args.nuse)[0]); xs.append(s)
                    del R
            else:
                for k in (0.0, 0.02, 0.05, 0.10, 0.16, 0.22, 0.30, 0.45, 0.60):
                    R = drv.raw_states(k, fixed, bnd, args.seed, args.settle, args.nframes)
                    dyn.append(share_from_raw(R, nuse=args.nuse)[0]); xs.append(k)
                    del R
            dyn = np.array(dyn); jd = int(np.argmax(dyn))
            ratio = dyn[jd] / mix[jm] if mix[jm] > 0 else np.inf
            print("  lambda:  " + "  ".join(f"{l:.2f}" for l in lams[::4]))
            print("  mixture: " + "  ".join(f"{v:.1e}" for v in mix[::4]))
            print(f"  mixture peak      = {mix[jm]:.4e} nats at lambda = {lams[jm]}")
            print(f"  dynamical peak    = {dyn[jd]:.4e} nats at {axis} = {xs[jd]}")
            print(f"  RATIO dyn/mix     = {ratio:.3f}   -> "
                  f"{'DYNAMICS EXCEEDS the straight line' if ratio > 1 else 'MIXTURE ARTIFACT'}")
            out.append(dict(label=lab, boundary=bnd, axis=axis, lams=lams.tolist(),
                            mix=mix.tolist(), xs=xs, dyn=dyn.tolist(),
                            mix_peak=float(mix[jm]), mix_argmax=float(lams[jm]),
                            dyn_peak=float(dyn[jd]), dyn_argmax=float(xs[jd]),
                            ratio=float(ratio), verdict='DYN>MIX' if ratio > 1 else 'MIXTURE'))
            del RA, RB
            cp.get_default_memory_pool().free_all_blocks()
    with open(os.path.join(HERE, 'array_negentropy_mixture.json'), 'w') as f:
        json.dump(out, f, indent=1, default=float)
    print("\n" + "=" * 84)
    print("MIXTURE NULL SUMMARY")
    for r in out:
        print(f"  {r['label']:<12} {r['boundary']:<5} dyn {r['dyn_peak']:.3e} @ "
              f"{r['dyn_argmax']:<7} vs mix {r['mix_peak']:.3e} @ lam {r['mix_argmax']:<5} "
              f"ratio {r['ratio']:6.3f}  {r['verdict']}")
    return out


def dose(drv, args):
    import cupy as cp
    out = []
    settles = [250, 500, 1000, 2000, 4000]
    for bnd in ('clip', 'fold'):
        for kap in (0.02, 0.05):
            print(f"\n=== DOSE VS RATE  kappa={kap} boundary={bnd} ===")
            print("  settle   " + "".join(f"{s:>11g}" for s in SIGMAS) + "    sigma*     peak")
            rows = []
            for st in settles:
                vals = []
                for s in SIGMAS:
                    R = drv.raw_states(kap, s, bnd, args.seed, st, args.nframes)
                    vals.append(share_from_raw(R, nuse=args.nuse)[0])
                    del R
                    cp.get_default_memory_pool().free_all_blocks()
                vals = np.array(vals); j = int(np.argmax(vals))
                print(f"  {st:<8} " + "".join(f"{v:>11.2e}" for v in vals) +
                      f"  {SIGMAS[j]:>8g} {vals[j]:>9.3e}")
                rows.append(dict(settle=st, vals=vals.tolist(),
                                 sigma_star=SIGMAS[j], peak=float(vals[j])))
            ss = np.array([r['sigma_star'] for r in rows], dtype=float)
            pk = np.array([r['peak'] for r in rows], dtype=float)
            ok = ss > 0
            slope = (float(np.polyfit(np.log([r['settle'] for r, o in zip(rows, ok) if o]),
                                      np.log(ss[ok]), 1)[0]) if ok.sum() >= 3 else float('nan'))
            conv = abs(pk[-1] - pk[-2]) / max(pk[-2], 1e-300)
            print(f"  slope d(log sigma*)/d(log settle) = {slope:+.3f}   "
                  f"(|b| < 0.3 required; b ~ 1 is the fixed-dose signature)")
            print(f"  height change 2000 -> 4000 = {conv*100:+.1f} %   (< 10 % required)")
            print(f"  VERDICT: location {'INTRINSIC' if abs(slope) < 0.3 else 'DOSE ARTIFACT'}"
                  f" | height {'CONVERGED' if conv < 0.10 else 'NOT CONVERGED'}")
            out.append(dict(kappa=kap, boundary=bnd, rows=rows, slope=slope,
                            conv_2000_4000=float(conv)))
            cp.get_default_memory_pool().free_all_blocks()
    with open(os.path.join(HERE, 'array_negentropy_dose.json'), 'w') as f:
        json.dump(out, f, indent=1, default=float)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mixture', action='store_true')
    ap.add_argument('--dose', action='store_true')
    ap.add_argument('--rows', type=int, default=8)
    ap.add_argument('--cols', type=int, default=64)
    ap.add_argument('--settle', type=int, default=2000)
    ap.add_argument('--nframes', type=int, default=96)
    ap.add_argument('--nuse', type=int, default=64)
    ap.add_argument('--seed', type=int, default=20260725)
    args = ap.parse_args()
    import cupy as cp
    print(f"DEVICE: {cp.cuda.runtime.getDeviceProperties(0)['name'].decode()}")
    drv = AN.Driver(args.rows, args.cols)
    t0 = time.time()
    if args.mixture:
        mixture(drv, args)
    if args.dose:
        dose(drv, args)
    print(f"\nwall time {time.time()-t0:.0f}s")


if __name__ == '__main__':
    main()
