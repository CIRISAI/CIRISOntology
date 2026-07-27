"""G11 adjudication: is the free-field discrepancy statistical or a sampler bias?
Independent seeds give the scatter; a longer run gives the 1/sqrt(N) test.  No threshold
is touched until this says which it is."""
import sys, os, numpy as np, cupy as cp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phi4_ridge import Phi4, Accum, free_propagator

L, m2f, R = 12, 0.5, 256
g = {'colin1': ((0, 0, 0), (1, 0, 0), (2, 0, 0))}
ex = free_propagator(L, m2f, [(0, 0, 0), (1, 0, 0), (2, 0, 0)])
print(f"exact: <phi^2>={ex[0]:.8f}  c(1)={ex[1]:.8f}  c(2)={ex[2]:.8f}")

for nsamp, gap, nseed in ((300, 3, 6), (2000, 6, 4)):
    res = []
    for sd in range(nseed):
        sim = Phi4(L, R, m2f, 0.0, 0.0, seed=1000 + 37 * sd)
        sim.tune(); sim.sweep(8000)
        acc = Accum(R, ['colin1'], ['theta0'])
        for _ in range(nsamp):
            sim.sweep(gap)
            acc.add_config(sim, g, {'theta0': [0.0]}, cp, do_counts=False)
        npts = acc.n * L ** 3
        mu = (acc.mom['colin1'] / npts).mean(axis=0)
        v = float(acc.phi2.sum() / (acc.n * R * L ** 3))
        res.append([v, float(mu[1]), float(mu[2])])
        del sim
        cp.get_default_memory_pool().free_all_blocks()
    res = np.array(res)
    m, s = res.mean(axis=0), res.std(axis=0, ddof=1) / np.sqrt(nseed)
    print(f"\nnsamp={nsamp} gap={gap} seeds={nseed}")
    for i, nm in enumerate(['<phi^2>', 'c(1)', 'c(2)']):
        z = (m[i] - ex[i]) / s[i] if s[i] > 0 else float('nan')
        print(f"  {nm:>8s}  {m[i]:.8f} +- {s[i]:.8f}   exact {ex[i]:.8f}   "
              f"rel {(m[i]/ex[i]-1)*100:+.3f}%   z={z:+.2f}")
