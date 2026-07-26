"""cft_e1_fine.py — E1 at sub-grid resolution: locate u* = h* L^(15/8) by a parabolic
fit in log u, so the ridge-locus exponent y_h carries an honest uncertainty rather than
the resolution of a geometric grid.

Pre-registered in CFT_RIDGE_PREREG.md (E1: y_h = 15/8, survives at +-0.06).
"""
import sys, os, json, math, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cft_ridge import measure, TC, Y_H, _dump

rows = []
for L in (8, 12, 16, 20):
    r = L // 4
    us = np.geomspace(1.9, 3.6, 9)
    vals = []
    t0 = time.time()
    for u in us:
        h = float(u) * L ** (-Y_H)
        vals.append(measure(L, TC, h, [r], method='auto', k=32,
                            want_corr=False)['r'][r]['ic3'])
    vals = np.array(vals)
    lu = np.log(us)
    j = int(np.argmax(vals))
    sl = slice(max(j - 2, 0), min(j + 3, len(us)))
    cf = np.polyfit(lu[sl], vals[sl], 2)
    u_star = float(np.exp(-cf[1] / (2 * cf[0])))
    i_star = float(np.polyval(cf, math.log(u_star)))
    # honest uncertainty: half-width in log u over which the fitted peak drops by 0.2%
    drop = 0.002 * i_star
    du = float(math.sqrt(abs(drop / cf[0]))) if cf[0] < 0 else float('nan')
    rows.append(dict(L=L, r=r, u_star=u_star, h_star=u_star * L ** (-Y_H),
                     ic3_star=i_star, du_log=du, secs=time.time() - t0,
                     scan_u=us.tolist(), scan_I=vals.tolist()))
    print(f"L={L:<3} r={r}  u* = {u_star:.4f}  (+-{du:.4f} in ln u at the 0.2% level)  "
          f"h* = {u_star * L ** (-Y_H):.6e}  I* = {i_star:.6e}  [{time.time()-t0:.0f}s]")
    print("      scan: " + "  ".join(f"{u:.3f}:{v:.5e}" for u, v in zip(us, vals)))

_dump('cft_e1_fine.json', rows)

Ls = np.array([r['L'] for r in rows], float)
hs = np.array([r['h_star'] for r in rows], float)
us = np.array([r['u_star'] for r in rows], float)
sl = np.diff(np.log(hs)) / np.diff(np.log(Ls))
print(f"\nE1  h*(L): local slopes {[f'{s:+.4f}' for s in sl]}   "
      f"global fit {np.polyfit(np.log(Ls), np.log(hs), 1)[0]:+.4f}   predicted {-Y_H:+.4f}")
print(f"    u* drift: " + "  ".join(f"L={int(l)}:{u:.4f}" for l, u in zip(Ls, us)))
dev = abs(sl[-1] + Y_H)
print(f"    |last local slope - (-15/8)| = {dev:.4f}  -> "
      f"{'SURVIVES' if dev < 0.06 else ('FIRES' if dev > 0.15 else 'marginal')}")
print(f"\nE2  I*(L): local slopes "
      f"{[f'{s:+.4f}' for s in np.diff(np.log([r['ic3_star'] for r in rows])) / np.diff(np.log(Ls))]}"
      f"   predicted {-0.75:+.4f}")
