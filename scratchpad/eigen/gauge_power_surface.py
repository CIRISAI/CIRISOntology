"""Power surface for the replication-corpus design (Ruling 2's rebuild).

Sweeps the frozen gauge's synthetic construction (gauge.py, unmodified) over
corpus-size multipliers x planted scales in the rank11 world. Per cell: median
Omega(11), sigma_R, median centroid replication. Pure synthetic — no corpus
data touched. Reads off (a) n for sigma_R <= 0.66 (sharp rank claim), (b) n
for measured Omega >= 0.25 (STRONG reachable), once the real run locates the
signal's scale. DESIGN table, not evidence."""
import json, numpy as np
import gauge

MULTS = [1, 2, 4, 8]
SCALES = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
NDRAW = 100
base = list(gauge.CLASS_SIZES)
out = {'mults': MULTS, 'scales': SCALES, 'ndraw': NDRAW, 'base_n': int(sum(base)), 'cells': {}}
for m in MULTS:
    gauge.CLASS_SIZES = [c * m for c in base]
    n = sum(gauge.CLASS_SIZES)
    for s in SCALES:
        cell = gauge.run_cell('rank11', s, NDRAW, 20260819 + m * 1000 + int(s * 10), True)
        row = {'n': int(n),
               'omega11_median': float(np.median(cell['omega11'])),
               'sigma_R': float(np.std(cell['rkind'])),
               'rkind_mean': float(np.mean(cell['rkind'])),
               'rho_gauge_median': float(np.median(cell['rho_gauge']))}
        out['cells'][f'{m}x_s{s}'] = row
        print(f"[{m}x n={n}] scale={s}: omega={row['omega11_median']:.4f} "
              f"sigma_R={row['sigma_R']:.3f} rho={row['rho_gauge_median']:.3f}", flush=True)
        json.dump(out, open('out/power_surface.json', 'w'), indent=1)
print('done -> out/power_surface.json (done-marker: out/power_surface.DONE)')
open('out/power_surface.DONE','w').write('done')
