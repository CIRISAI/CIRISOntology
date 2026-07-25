"""ising_ridge.py — finite-size scaling of the CRITICAL-RIDGE regime.

The fixed-h thermodynamic limit and the critical scaling trajectory are different limits
and they give different answers.  This measures the second one: T = T_c, h = h*(L) placed
by the magnetic scaling dimension (h* ~ L^-15/8), for a LOCAL triple (star) and a
WELL-SEPARATED one (collinear at r = L/4 and r = L/2).
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ising_field as IF

IF.DECORRELATE = True
try:
    import cupy as xp
except Exception:
    xp = np

HPK4 = 0.21077  # measured 4x4 peak field, the anchor
rows = []
rng = np.random.default_rng(20260725)
print(f"{'L':>4}{'h*':>10}{'geom':<12}{'excess':>13}{'CF%':>9}{'z':>9}{'N_eff':>10}{'F':>9}")
for L in (8, 16, 32, 64):
    hstar = HPK4 * (L / 4.0) ** (-15.0 / 8.0)
    R, n_samp, gap, burn = IF.mc_budget(L, L)
    bits, mags = IF.mc_run(L, L, IF.TC, float(hstar), R, burn, n_samp, gap, xp, seed=20260725)
    tau = IF.tau_int(xp.asnumpy(mags) if hasattr(xp, 'asnumpy') else np.asarray(mags))
    geos = {'star': ((1, 0), (0, 1), (L - 1, 0)),
            f'colin-r{max(L//4,1)}': ((0, 0), (L // 4, 0), (L // 2, 0)),
            f'colin-r{L//2}': ((0, 0), (L // 2, 0), (0, 0))}
    geos = {k: v for k, v in geos.items() if len(set(v)) == 3}
    for g, sites in geos.items():
        r = IF.analyse_block_counts(IF.triple_counts(bits, sites, L, L, xp), rng)
        r.update(Lx=L, Ly=L, T=IF.TC, h=float(hstar), geom=g, tau_int=tau, tag='ridge')
        rows.append(r)
        print(f"{L:>4}{hstar:>10.5f}{g:<12}{r['excess']:>13.4e}{r['excess']/IF.LN2*100:>9.4f}"
              f"{r['z']:>9.1f}{r['N_eff']:>10.1e}{r['F_max']:>9.0f}"
              f"{'' if r['trustworthy'] else '  UNTRUST'}")
    del bits, mags
    if hasattr(xp, 'get_default_memory_pool'):
        xp.get_default_memory_pool().free_all_blocks()
json.dump(rows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  'ising_mc_ridge.json'), 'w'), default=float)
print("wrote ising_mc_ridge.json")
