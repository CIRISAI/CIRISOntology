#!/usr/bin/env python3
"""WATER_AMENDMENT_10: is the far arm AVAILABLE at the state points that matter?

Glass measured its own correlation length across its ladder: xi = 1.045 ->
1.111, a 6% move while the structural relaxation time moves by 2.5e5.  So the
Kob-Andersen transition is NOT a critical point with a diverging static length
and its far arm does not degrade at the cold end.

THIS CAMPAIGN'S LADDER CROSSES A WIDOM LINE, where xi GROWS.  So the contrast
glass supplied turns a caveat into an arithmetic question: at each state point,
is there a radius that is simultaneously (a) beyond the correlation length and
(b) inside the minimum-image limit L/2?  If not, the far arm is not merely
degraded -- it does not exist at that state point, at any tolerance.

Computes nothing about water; this is box arithmetic at water's number density.
"""
import numpy as np

RHO = 0.03342          # oxygen number density, A^-3
KMULT = 3.0            # far arm requires r_far >= KMULT * xi


def box(N):
    L = (N / RHO) ** (1.0 / 3.0)
    return L, L / 2.0


def main():
    print("water at rho = %.5f A^-3; minimum image caps any separation at L/2" % RHO)
    print()
    print("%8s %9s %9s %14s" % ("N", "L (A)", "L/2 (A)", "max usable xi"))
    for N in (2000, 4000, 8000, 16000, 32000, 112000):
        L, half = box(N)
        print("%8d %9.1f %9.1f %14.1f" % (N, L, half, half / KMULT))
    print()
    print("far arm requires r_far >= %.0f*xi AND r_far <= L/2, so it EXISTS iff"
          % KMULT)
    print("xi <= L/(2*%.0f).  The campaign's budgeted N = 4000 caps xi at %.1f A."
          % (KMULT, box(4000)[1] / KMULT))
    print()
    print("N required to keep the far arm alive at a given correlation length:")
    print("%10s %12s %14s" % ("xi (A)", "L needed (A)", "N needed"))
    for xi in (3.0, 5.0, 8.0, 10.0, 15.0, 20.0):
        Lneed = 2.0 * KMULT * xi
        print("%10.1f %12.1f %14.0f" % (xi, Lneed, RHO * Lneed ** 3))
    print()
    print("The campaign's own far-arm template sits at r = 7.0 A, which is")
    print("%.1f*xi at xi = 3 A and only %.1f*xi at xi = 5 A." % (7.0 / 3.0, 7.0 / 5.0))


main()
