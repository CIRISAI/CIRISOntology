"""
Where does the DESI DR2 best-fit w0-waCDM actually cross w = -1?

The extensive branch (`dark-balance-extensive`) stakes a FROZEN kill window:
    z_c = 0.59 +/- 0.03
so this is a direct, dated test against data already in hand.

CPL:  w(a) = w0 + wa(1-a).   Crossing w = -1  =>  a_c = 1 + (1+w0)/wa,
                                                  z_c = 1/a_c - 1.

DESI DR2 values (arXiv:2503.14738 and quoting secondary sources -- see the
provenance note at the bottom):
  DESI BAO + CMB           : w0 = -0.42  +/- 0.21 , wa = -1.75 +/- 0.58   (3.1 sigma vs LCDM)
  DESI BAO + CMB + Pantheon+: w0 = -0.838 +/- 0.055, wa = -0.62  +0.22/-0.19

The w0-wa posterior is strongly anti-correlated. The correlation is NOT
published in the numbers I could retrieve, and it dominates the error on z_c,
so the result is reported as a function of rho rather than at one assumed value.
"""
import numpy as np

WINDOW_C, WINDOW_HW = 0.59, 0.03


def zc(w0, wa):
    a = 1.0 + (1.0 + w0) / wa
    return 1.0 / a - 1.0


def zc_sigma(w0, wa, sw0, swa, rho):
    """Linear propagation including the w0-wa correlation."""
    u = (1.0 + w0) / wa
    dz_du = -1.0 / (1.0 + u) ** 2
    du_dw0 = 1.0 / wa
    du_dwa = -(1.0 + w0) / wa**2
    A, B = dz_du * du_dw0, dz_du * du_dwa
    var = A**2 * sw0**2 + B**2 * swa**2 + 2 * A * B * rho * sw0 * swa
    return np.sqrt(max(var, 0.0))


CASES = [
    ("DESI BAO + CMB              ", -0.42, 0.21, -1.75, 0.58),
    ("DESI BAO + CMB + Pantheon+  ", -0.838, 0.055, -0.62, 0.205),
]

print("=" * 78)
print("DESI DR2 PHANTOM-CROSSING REDSHIFT vs THE FROZEN WINDOW 0.59 +/- 0.03")
print("=" * 78)

for name, w0, sw0, wa, swa in CASES:
    z = zc(w0, wa)
    print(f"\n{name}")
    print(f"   w0 = {w0:+.3f} +/- {sw0:.3f}   wa = {wa:+.3f} +/- {swa:.3f}")
    print(f"   central crossing  z_c = {z:.3f}")
    print(f"   offset from window centre: {z - WINDOW_C:+.3f} "
          f"({abs(z - WINDOW_C)/WINDOW_HW:.1f} window half-widths)")
    print(f"   {'rho':>6} {'sigma(z_c)':>12} {'tension vs 0.59':>17}")
    for rho in [0.0, -0.5, -0.8, -0.9, -0.95, -0.99]:
        s = zc_sigma(w0, wa, sw0, swa, rho)
        tens = abs(z - WINDOW_C) / s if s > 0 else float('inf')
        flag = "  <-- would fire" if tens > 3 else ""
        print(f"   {rho:6.2f} {s:12.4f} {tens:15.1f}s{flag}")

print("\n" + "=" * 78)
print("READING")
print("=" * 78)
print("""The two dataset combinations disagree about WHERE the crossing is, and
they disagree in the direction that matters for this project.

  * BAO + CMB (geometry + early universe, NO supernovae) puts the crossing
    near z ~ 0.50 -- close enough to 0.59 that the frozen window survives at
    any plausible correlation.
  * Adding Pantheon+ supernovae pulls the crossing down to z ~ 0.35, which is
    3+ sigma from the frozen window for strong anti-correlation.

That is exactly the split `dark-balance-intensive` was hoping for, but pointed
at the OTHER branch: the stance's stated hope is that the supernova compilations
carry a hidden systematic and that a geometry-only DR3 check will vindicate the
no-crossing reading. This calculation says the supernovae are ALSO what pushes
the crossing away from the extensive branch's frozen window. If the SNe are
right, the extensive window is in trouble now. If the SNe carry the suspected
systematic, the window survives -- but then so does the intensive branch's
escape route.

The two branches are therefore NOT cleanly separated by DR3 alone: the same
supernova systematic question moves both. The stance presents DR3's
geometry-only check as a single test that at most one branch survives. It is
better described as a test whose verdict depends on a systematic that is itself
the live question.

PROVENANCE, stated plainly: the w0/wa central values and errors above were
retrieved via web search summaries citing the DESI DR2 papers, NOT read off the
DESI papers directly. The 3.1 sigma (BAO+CMB) and 2.8-4.2 sigma (with SNe)
significances ARE confirmed from the arXiv:2503.14738 abstract. The w0-wa
CORRELATION is not in hand at all and dominates sigma(z_c) -- which is why it is
scanned rather than assumed. Before any of this is used against a claim, the
covariance should be taken from the DESI chains.""")
