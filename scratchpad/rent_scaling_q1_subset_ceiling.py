"""rent_scaling_q1_subset_ceiling.py — the attainable ceiling under FULL upkeep, per structure.

Prereg §2.4 (standing requirement): for every structure, report what fraction of the design
state's whole-only share full upkeep can actually hold. On a restorable substrate that is 1 by
construction; on a lossy one it is strictly less, and the deficit is the price of the
restorability failure measured in the currency the campaign actually cares about.

Three quantities, all exact, all from the GATED rent_islands.py solver (imported unmodified):
  ceiling_frac  = share_inf(q=1) / share_max   -- the headline
  Hc_deficit    = ln|S| - H(c*)                -- how far the deposit falls short of uniform
                                                  on S; zero iff the deposit is uniform, and
                                                  noise-free in the sense that it does not
                                                  depend on how the share is read off
  tv_from_uniform = 0.5 * sum_i |c*_i - 1/|S|| -- the restorability distance

share_inf uses rent_islands' pairwise-maxent correction, NOT k*ln2 - H(p): on a lossy
substrate the state is no longer pair-uniform and the naive reading OVER-reads the share (it
reported ceilings ABOVE share_max before the parent caught it). The O(leak^2) residual is
reported per row so the remaining error stays visible.

Cost measured before running: build + solve is under ~1 s per structure at k <= 20, so the
whole subset roster is affordable and NO cost cut is applied. That is stated because a cut
chosen after seeing which structures were lossy would be a selection.
"""
import sys, os, json, time, argparse
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rent_islands as RI
import rent_islands_design_check as DC

HERE = os.path.dirname(os.path.abspath(__file__))
EPS = [0.01, 0.05]                      # the prereg's grid, unchanged

# CPU only. rent_islands switches to the GPU at k >= 18; the GPU is in use by another
# campaign on this shared box (prereg §4 box discipline), so the switch is disabled rather
# than competed with. Pushing the threshold out of range is the whole change -- the solver
# and every number it produces are identical either way.
RI.GPU_FROM_K = 10_000


def _np(x):
    """rent_islands returns device arrays when it is on the GPU; numpy either way."""
    return x.get() if hasattr(x, 'get') else np.asarray(x)


def oa_full(N):
    H = DC.hadamard(N).copy()
    H = H * np.where(H[:, [0]] == -1, -1, 1)
    return np.ascontiguousarray(((1 - H[:, 1:]) // 2).astype(np.int8))


def main(src, out):
    D = json.load(open(src))
    rows = D['rows']
    cache = {}
    res = []
    t_all = time.time()
    for r in rows:
        N = r['order']
        if N not in cache:
            cache[N] = oa_full(N)
        S = np.unique(cache[N][:, r['cols']], axis=0)
        k = S.shape[1]
        L = RI.Lattice(r['label'], 'S', k, S=S, force_full=True)
        rec = dict(label=r['label'], order=N, k=k, ns=int(L.ns),
                   transitive=r['transitive'], restorable=r['restorable'],
                   profile_dev=r['profile_dev'], orbit_sizes=r['orbit_sizes'],
                   share_max=float(L.share_max))
        for eps in EPS:
            s = L.stat_share(1.0, eps, want=('state',))
            c = _np(s["c"]).astype(float)
            rec[f'ceiling_{eps}'] = float(s['share'])
            rec[f'ceiling_frac_{eps}'] = float(s['share'] / L.share_max)
            rec[f'Hc_deficit_{eps}'] = float(np.log(L.ns) - s['H_c'])
            rec[f'tv_{eps}'] = float(0.5 * np.abs(c - 1.0 / L.ns).sum())
            rec[f'leak_resid_rel_{eps}'] = float(s.get('leak', 0.0) ** 2
                                                 / max(s['share'], 1e-30))
        res.append(rec)
        print(f"  {r['label']:16s} k={k:2d} rest={str(r['restorable']):5s} "
              f"ceilfrac(.01)={rec['ceiling_frac_0.01']:.9f} "
              f"ceilfrac(.05)={rec['ceiling_frac_0.05']:.9f} "
              f"Hcdef(.05)={rec['Hc_deficit_0.05']:.3e} TV(.05)={rec['tv_0.05']:.3e}",
              flush=True)
        json.dump(res, open(out, 'w'), indent=1)

    print(f"\n{'='*84}")
    for eps in EPS:
        rest = [x[f'ceiling_frac_{eps}'] for x in res if x['restorable']]
        loss = [x[f'ceiling_frac_{eps}'] for x in res if not x['restorable']]
        print(f"eps={eps}: restorable n={len(rest)} ceiling_frac min={min(rest):.12f} "
              f"max={max(rest):.12f}")
        if loss:
            print(f"          LOSSY      n={len(loss)} ceiling_frac min={min(loss):.9f} "
                  f"max={max(loss):.9f}  worst deficit={1-min(loss):.3e}")
    print(f"[{time.time()-t_all:.0f}s] -> {out}")


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default=os.path.join(HERE, 'rent_scaling_q1_subset.json'))
    ap.add_argument('--out', default=os.path.join(HERE, 'rent_scaling_q1_subset_ceiling.json'))
    a = ap.parse_args()
    main(a.src, a.out)
