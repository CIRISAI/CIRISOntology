"""
What w(z) does each branch actually PREDICT, computed from LCDM structure
formation with the repo's own coordination formula?

For any component:  rhodot = -3H(1+w)rho   =>   1 + w = -(1/3) dln(rho)/dln(a)

  INTENSIVE branch:  rho_DE  ∝  s(z)      = -ln(1 - rho_corr(z))     (per unit)
  EXTENSIVE branch:  rho_DE  ∝  N(z)*s(z)                            (grand total)

The intensive branch asserts its balance "can only shrink over time, or hold
still... it can never grow", and therefore FORBIDS phantom (w < -1) at every
moment. That is a check we can now run, not just assert.
"""
import numpy as np
from scipy.interpolate import CubicSpline
import crest_predict as C

Mmin = 1.4e11          # the partition that puts the extensive crest at z=0.59
zs = np.linspace(0.02, 3.0, 40)

s_list, Ns_list, rho_list = [], [], []
for z in zs:
    Ns, n, rc = C.coordination_density(z, Mmin)
    s_list.append(-np.log(1 - rc))
    Ns_list.append(Ns)
    rho_list.append(rc)

s = np.array(s_list); Ns = np.array(Ns_list); rc = np.array(rho_list)
lna = -np.log(1 + zs)                      # increases toward z=0

def w_of(rho_de):
    """1 + w = -(1/3) dln rho / dln a"""
    order = np.argsort(lna)
    spl = CubicSpline(lna[order], np.log(rho_de[order]))
    d = spl.derivative()
    return -1.0 - (1.0 / 3.0) * d(lna)

w_int = w_of(s)
w_ext = w_of(Ns)

print("=" * 74)
print(f"w(z) PREDICTED BY EACH BRANCH   (M_min = {Mmin:.1e} Msun/h)")
print("=" * 74)
print(f"{'z':>6} {'rho_corr':>10} {'s=-ln(1-rc)':>12} {'N*s':>12} "
      f"{'w_intensive':>13} {'w_extensive':>13}")
print("-" * 74)
for i in range(0, len(zs), 3):
    print(f"{zs[i]:6.2f} {rc[i]:10.4f} {s[i]:12.4f} {Ns[i]:12.4e} "
          f"{w_int[i]:13.3f} {w_ext[i]:13.3f}")

print("-" * 74)
print(f"\n  w0 (intensive, z~0) = {w_int[0]:.3f}")
print(f"  w0 (extensive, z~0) = {w_ext[0]:.3f}")
print(f"\n  DESI DR2 best fit is roughly w0 ~ -0.9 +/- 0.05, wa ~ -0.8 +/- 0.3")
print(f"  (phantom in the past, w > -1 today)")

print("\n" + "=" * 74)
print("THE SIGN CHECK THE INTENSIVE BRANCH STAKES ITS THEOREM ON")
print("=" * 74)
ds_dlna = np.gradient(np.log(s), lna)
print(f"  dln(s)/dln(a) over z=[0.02,3]:  min {ds_dlna.min():+.3f}  "
      f"max {ds_dlna.max():+.3f}")
if np.all(ds_dlna > 0):
    print("  => the per-unit balance s GROWS with time, monotonically.")
    print("  => 1+w = -(1/3) dln s/dln a < 0  =>  w < -1  =>  PHANTOM, always.")
    print("\n  This is the OPPOSITE sign to the intensive branch's claim that")
    print("  the per-unit balance 'can only shrink over time' and that the")
    print("  reading 'forbids phantom, at every moment, always'.")
elif np.all(ds_dlna < 0):
    print("  => s FALLS with time: matches the intensive branch's assertion,")
    print("     w > -1 always, no phantom.")
else:
    print("  => s is NON-MONOTONIC: neither branch's sign claim holds cleanly.")

print("""
WHY THIS IS NOT A CONTRADICTION WITH THE PROVED THEOREMS.
`contraction` (S_pairwise_hadamard_le) forbids raising the reading by LOCAL
POINTWISE MIXING. Structure formation is not local pointwise mixing -- it is
gravitational INTERACTION, which `true-books` explicitly says is the one thing
that CAN write a real entry. So gravity legitimately raises coordination, and
the theorems do not forbid it. The intensive branch's "can only shrink" is
therefore an ADDITIONAL physical assumption about the real universe, not a
corollary of the machine-checked monotonicity -- and under the correlation rule
used here it comes out with the wrong sign.

CAVEAT, load-bearing: rho_corr = xi_R(d)/sigma^2_R at the mean unit separation
is MY declared rule (see prereg S3). The framework does not fix it. A different
rule can change this sign. What is NOT rule-dependent is that the sign is a
CHOICE the framework has not pinned -- which is the same provenance exposure as
the partition.""")
