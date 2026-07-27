"""G11z adjudication.

The gate's z-test on the free-field plumb line reported |z| = 11.6 on <phi^2> at a
relative deviation of +0.007% -- i.e. it failed on the ERROR BAR, not on the deviation,
and the error bar had moved 12x from the run recorded in the previous gate log at
identical settings.  Two things are asked here, and no threshold is touched until both
are answered:

  (a) is the sampler deterministic given its seed?  If it is not, the 4-seed scatter is
      not the only source of run-to-run spread and the previous log is not comparable.
  (b) what IS the honest across-seed error, measured with enough seeds that its own
      uncertainty is small?  At 4 seeds the sample SD has 3 dof and swings by a factor
      of ~3 at 95%; a 12x swing needs more than that to explain.

If the deviation is a real bias, the 1/sqrt(N) test separates it: doubling the samples
must halve the error but leave the deviation put.
"""
import sys, os, numpy as np, cupy as cp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phi4_ridge import Phi4, Accum, free_propagator

L, m2f, R = 12, 0.5, 256
g = {'colin1': ((0, 0, 0), (1, 0, 0), (2, 0, 0))}
ex = free_propagator(L, m2f, [(0, 0, 0), (1, 0, 0), (2, 0, 0)])
NM = ['<phi^2>', 'c(1)', 'c(2)']
print(f"exact: <phi^2>={ex[0]:.8f}  c(1)={ex[1]:.8f}  c(2)={ex[2]:.8f}")


def one(seed, nsamp, gap, nburn=8000):
    sim = Phi4(L, R, m2f, 0.0, 0.0, seed=seed)
    sim.tune(); sim.sweep(nburn)
    acc = Accum(R, ['colin1'], ['theta0'])
    for _ in range(nsamp):
        sim.sweep(gap)
        acc.add_config(sim, g, {'theta0': [0.0]}, cp, do_counts=False)
    mu = (acc.mom['colin1'] / (acc.n * L ** 3)).mean(axis=0)
    v = float(acc.phi2.sum() / (acc.n * R * L ** 3))
    d = float(sim.delta)
    del sim
    cp.get_default_memory_pool().free_all_blocks()
    return [v, float(mu[1]), float(mu[2])], d


# ---- (a) determinism -----------------------------------------------------------------
a1, d1 = one(1000, 300, 6)
a2, d2 = one(1000, 300, 6)
print(f"\n(a) same seed twice:  delta {d1:.6f} vs {d2:.6f}")
for i, nm in enumerate(NM):
    print(f"      {nm:>8s} {a1[i]:.10f}  {a2[i]:.10f}   diff {a1[i]-a2[i]:+.3e}")
print("      -> " + ("DETERMINISTIC" if max(abs(a1[i] - a2[i]) for i in range(3)) < 1e-12
                     else "NOT deterministic: run-to-run spread is not seed scatter alone"))

# ---- (b) honest error bar, and the 1/sqrt(N) test ------------------------------------
for nsamp, gap, nseed in ((500, 6, 16), (2000, 6, 16)):
    res = np.array([one(1000 + 37 * sd, nsamp, gap)[0] for sd in range(nseed)])
    m = res.mean(axis=0)
    s = res.std(axis=0, ddof=1) / np.sqrt(nseed)
    print(f"\n(b) nsamp={nsamp} gap={gap} seeds={nseed}  "
          f"(SD of the SD itself ~ {1/np.sqrt(2*(nseed-1))*100:.0f}%)")
    for i, nm in enumerate(NM):
        print(f"      {nm:>8s} {m[i]:.8f} +- {s[i]:.8f}  exact {ex[i]:.8f}  "
              f"rel {(m[i]/ex[i]-1)*100:+.4f}%  z={(m[i]-ex[i])/s[i]:+.2f}")
