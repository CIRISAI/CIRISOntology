"""K4 — the mixture null, on the peak state of every readable lattice size.

Uses the vectorized copula (phi4_fastcop.py, gated at 2.2e-15 against the adaptive
implementation and 283x faster).  The pre-registered adjudication is NOT pass/fail: if a
two-component Gaussian mixture, each component pairwise-only, reproduces the share, the
finding is that the order-3 structure is carried by a single latent binary collective mode.
That IDENTIFIES a mechanism and BOUNDS the interpretation; it does not kill the ridge's
existence.  What it kills is any reading of the ridge as irreducibly three-body.
"""
import sys, os, math, json
import numpy as np
from scipy import optimize, special
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phi4_fastcop import cells_vec
from ising_field import share3, LN2
from phi4_analyze import readout, RNG


def mixture_fast(p8):
    p = np.asarray(p8, float); p = p / p.sum()
    r = p.reshape(2, 2, 2)
    pa = [r[0].sum(), r[:, 0].sum(), r[:, :, 0].sum()]
    a0 = np.array([float(special.ndtri(1 - min(max(x, 1e-12), 1 - 1e-12))) for x in pa])

    def model(th):
        w = 1.0 / (1.0 + math.exp(-th[0])); mu = abs(th[1])
        rr = [math.tanh(t) for t in th[2:5]]
        m = w * cells_vec(a0 - mu, *rr) + (1 - w) * cells_vec(a0 + mu, *rr)
        return m / m.sum()

    def resid(th):
        return (model(th) - p) / np.sqrt(np.maximum(p, 1e-9))

    best = None
    for w0 in (-0.5, 0.0, 0.5):
        for mu0 in (0.1, 0.5, 1.0):
            try:
                s = optimize.least_squares(resid, np.array([w0, mu0, .3, .3, .3]),
                                           xtol=1e-13, ftol=1e-13, max_nfev=4000)
            except Exception:
                continue
            if best is None or s.cost < best.cost:
                best = s
    m = model(best.x)
    return m, dict(w=float(1 / (1 + math.exp(-best.x[0]))), mu=float(abs(best.x[1])),
                   rho=[float(math.tanh(t)) for t in best.x[2:5]]), \
        float(np.sqrt(np.mean((m - p) ** 2)))


def main():
    rows = json.load(open('phi4_ridge.json'))
    if os.path.exists('phi4_deep.json'):
        deep = json.load(open('phi4_deep.json'))
        # S3d: pool independent seeds at the same (L, u), exactly as phi4_analyze.py does,
        # so K4 is fitted on the same states the scorecard is scored on
        if os.path.exists('phi4_seeds32.json'):
            by = {}
            for r in deep + json.load(open('phi4_seeds32.json')):
                by.setdefault((r['L'], round(r['u'], 6)), []).append(r)
            merged = []
            for grp in by.values():
                if len(grp) == 1:
                    merged.append(grp[0]); continue
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
                merged.append(base)
            deep = merged
        k = {(r['L'], round(r['u'], 6)) for r in deep}
        rows = [r for r in rows if (r['L'], round(r['u'], 6)) not in k] + deep

    print("=" * 96)
    print("K4 — MIXTURE NULL (two-component Gaussian, each component pairwise-only)")
    print("  Adjudication is pre-registered and is NOT pass/fail.  Reproducing the share")
    print("  identifies the mechanism as a single latent binary collective mode -- the")
    print("  magnetisation-sector reading restated -- and bounds interpretation.  The")
    print("  ridge's EXISTENCE survives it either way.  What it would kill is any claim")
    print("  that the ridge is irreducibly three-body.")
    print("=" * 96)
    print(f"{'L':>4s} {'thr':>8s} {'u*':>8s} {'measured raw':>14s} {'mixture':>12s} "
          f"{'ratio':>7s} {'fit rms':>10s} {'w':>7s} {'mu':>7s} {'copula(K3)':>12s}")
    out = []
    for thr in ('theta0', 'median'):
        for L in sorted({r['L'] for r in rows}):
            sub = [r for r in rows if r['L'] == L and r['u'] > 0]
            if not sub:
                continue
            v = [(r, readout(r, thr, 'colin-r', nulls=False)) for r in sub]
            r0, d0 = max(v, key=lambda t: t[1]['excess'])
            if d0['z'] < 3:
                print(f"{L:>4d} {thr:>8s} {r0['u']:8.3f}   -- peak z = {d0['z']:.2f} < 3:"
                      f" below the instrument's reach, not fitted --")
                continue
            cnt = np.asarray(r0['counts'][thr]['colin-r'], float).sum(axis=0)
            p = cnt / cnt.sum()
            m, prm, rms = mixture_fast(p)
            sm = float(share3(m)[0]); sr = float(d0['share_raw'])
            dfull = readout(r0, thr, 'colin-r', nulls=True)
            print(f"{L:>4d} {thr:>8s} {r0['u']:8.3f} {sr:14.4e} {sm:12.4e} "
                  f"{sm/sr:7.3f} {rms:10.2e} {prm['w']:7.3f} {prm['mu']:7.3f} "
                  f"{dfull.get('copula_share', float('nan')):12.4e}")
            out.append(dict(L=L, thr=thr, u=r0['u'], raw=sr, mix=sm, rms=rms, **prm))
    json.dump(out, open('phi4_k4.json', 'w'))
    print("\n  A mixture ratio near 1 means the eight-cell state is reproduced by ONE")
    print("  latent binary mode plus pairwise Gaussian structure.  A ratio well below 1")
    print("  means there is order-3 structure the latent-mode picture does not supply.")


if __name__ == '__main__':
    main()
