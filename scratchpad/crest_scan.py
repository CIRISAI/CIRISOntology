"""
Map the crest redshift z_c as a function of the PARTITION choice M_min.

The extensive branch stakes a frozen kill window z_c = 0.59 +/- 0.03.
Core/Provenance.lean proves (provenance_line) that the partition -- "which
degrees of freedom count as one unit" -- is NOT recoverable from the
correlation matrix. It is declared, not discovered.

So: how much does z_c depend on that declaration?
"""
import numpy as np
from scipy.optimize import brentq
from scipy.interpolate import CubicSpline
import crest_predict as C


def crest_of(Mmin, zlo=0.005, zhi=5.0, nz=44):
    zs = np.linspace(zlo, zhi, nz)
    vals = np.array([C.coordination_density(z, Mmin)[0] for z in zs])
    if not np.all(np.isfinite(vals)):
        good = np.isfinite(vals)
        zs, vals = zs[good], vals[good]
    spl = CubicSpline(zs, vals)
    d = spl.derivative()
    roots = [brentq(d, zs[i], zs[i + 1]) for i in range(len(zs) - 1)
             if d(zs[i]) * d(zs[i + 1]) < 0]
    # keep maxima only
    maxima = [r for r in roots if spl(r, 2) < 0]
    return maxima, zs, vals


print("=" * 72)
print("CREST REDSHIFT vs PARTITION CHOICE  (the provenance-line exposure)")
print("frozen kill window:  z_c = 0.59 +/- 0.03")
print("=" * 72)
print(f"{'M_min [Msun/h]':>16} {'mean sep [Mpc/h]':>18} {'z_crest':>12}   in window?")
print("-" * 72)

rows = []
for lgM in [10.0, 10.5, 11.0, 11.3, 11.5, 11.7, 12.0, 12.5, 13.0, 13.5, 14.0]:
    Mmin = 10 ** lgM
    maxima, zs, vals = crest_of(Mmin)
    n0 = C.n_above(Mmin, 0.0)
    sep = n0 ** (-1 / 3)
    if maxima:
        zc = maxima[0]
        hit = "YES  <<<" if abs(zc - 0.59) <= 0.03 else "no"
        print(f"{Mmin:16.2e} {sep:18.2f} {zc:12.3f}   {hit}")
        rows.append((lgM, zc))
    else:
        print(f"{Mmin:16.2e} {sep:18.2f} {'none':>12}   n/a")

print("-" * 72)

if len(rows) >= 3:
    lgs = np.array([r[0] for r in rows])
    zcs = np.array([r[1] for r in rows])
    order = np.argsort(lgs)
    lgs, zcs = lgs[order], zcs[order]
    # sensitivity
    slope = np.gradient(zcs, lgs)
    print("\nSENSITIVITY  dz_c / dlog10(M_min):")
    for lg, zc, sl in zip(lgs, zcs, slope):
        print(f"   log10 M_min = {lg:5.2f}   z_c = {zc:6.3f}   dz_c/dlogM = {sl:+7.3f}")

    # what M_min is required to land in the frozen window?
    f = CubicSpline(lgs, zcs - 0.59)
    sols = []
    for i in range(len(lgs) - 1):
        if f(lgs[i]) * f(lgs[i + 1]) < 0:
            sols.append(brentq(f, lgs[i], lgs[i + 1]))
    print("\nREQUIRED PARTITION to hit the frozen window z_c = 0.59:")
    if sols:
        for s in sols:
            # width of M_min range giving z_c within +/-0.03
            lo = brentq(lambda x: f(x) + 0.03, lgs[0], lgs[-1]) if \
                (f(lgs[0]) + 0.03) * (f(lgs[-1]) + 0.03) < 0 else None
            hi = brentq(lambda x: f(x) - 0.03, lgs[0], lgs[-1]) if \
                (f(lgs[0]) - 0.03) * (f(lgs[-1]) - 0.03) < 0 else None
            print(f"   log10 M_min = {s:.3f}  ->  M_min = {10**s:.2e} Msun/h")
            if lo and hi:
                print(f"   window +/-0.03 spans log10 M_min in "
                      f"[{min(lo,hi):.3f}, {max(lo,hi):.3f}]  "
                      f"= a factor {10**abs(hi-lo):.2f} in mass")
    else:
        print("   no M_min in the scanned range reproduces the frozen window")

print("\n" + "=" * 72)
print("VERDICT")
print("=" * 72)
print("""A crest EXISTS and is generic -- the extensive total really does climb,
crest and fall, so the qualitative story survives. But z_c is a steep
function of M_min, the declared unit. Two decades of halo mass move the
crest across essentially the entire interesting redshift range. The
frozen window z_c = 0.59 +/- 0.03 is therefore reachable, but only by
DECLARING the partition that puts it there -- and provenance_line proves
the instrument cannot supply that declaration. The prediction is one
free upstream choice deep.""")
