"""Is E2's PRIMARY ruler trustworthy?  A gate on the estimator, not on the data.

E2 infers y_h from how a rescaled moment DRIFTS between two lattice sizes when the grid
was built assuming y_h = Y_H.  The algebra: with true scaling X(L,h) = L^(-Delta) F(h L^y),
evaluating at fixed u = h L^(Y_H) gives X L^Delta = F(u L^(y - Y_H)), so

    ln(X2 L2^D / X1 L1^D) = (dlnF/dlnu) (y - Y_H) ln(L2/L1)

and y is read off, with dlnF/dlnu measured at fixed L from the two neighbouring u values.
That is exact for a pure scaling function.  What it is NOT tested for is (a) the finite
difference in ln u on a grid of ratio 1.7, (b) a moment whose dlnF/dlnu is small, so the
division amplifies everything, and (c) corrections to scaling.  This file plants a known
y and asks the estimator to give it back, on the SAME grid the run uses.

No thresholds are moved by this file.  It decides how much of E2's spread is the ruler.
"""
import sys, os, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phi4_ridge import Y_H, BETA_NU

U0 = 1.15
US = [U0 * 1.7 ** (i - 5.5) for i in range(12)]
LS = [8, 12, 16, 24, 32]


def infer(vals, u0, Ls, Delta, corr=None):
    """vals[(L,u)] -> inferred y_h, by exactly the recipe phi4_analyze.py uses."""
    i = US.index(u0)
    L1, L2 = Ls[-2], Ls[-1]
    a, b = vals[(L2, US[i - 1])], vals[(L2, US[i + 1])]
    dln = math.log(abs(b / a)) / math.log(US[i + 1] / US[i - 1])
    v1 = vals[(L1, u0)] * L1 ** Delta
    v2 = vals[(L2, u0)] * L2 ** Delta
    return Y_H + math.log(v2 / v1) / (dln * math.log(L2 / L1))


def build(y_true, Delta, F, omega=None, amp=0.0):
    v = {}
    for L in LS:
        for u in US:
            x = u * L ** (y_true - Y_H)
            c = 1.0 + amp * L ** (-omega) if omega else 1.0
            v[(L, u)] = L ** (-Delta) * F(x) * c
    return v


print("=" * 84)
print("E2 PRIMARY-ESTIMATOR GATE — plant a known y_h, on the run's own u grid")
print("=" * 84)

# Scaling functions with different curvature; the run's moments are monotone in u near
# the peak (m, phi rise; kappa2, kappa3, U fall), so both signs of dlnF/dlnu are tested.
FAM = {
    'F = x/(1+x)      (rising, saturating)': lambda x: x / (1 + x),
    'F = x^0.7        (pure power, rising)': lambda x: x ** 0.7,
    'F = 1/(1+x)      (falling)':            lambda x: 1.0 / (1 + x),
    'F = x/(1+x)^2    (peaked at x=1)':      lambda x: x / (1 + x) ** 2,
    'F = x^2 e^{-x}   (peaked at x=2)':      lambda x: x * x * math.exp(-x),
}

for label, F in FAM.items():
    print(f"\n  {label}")
    for y_true in (2.4819, 1.8750):
        row = []
        for u0 in (US[5], US[6], US[7]):
            v = build(y_true, BETA_NU, F)
            try:
                row.append(infer(v, u0, LS, BETA_NU))
            except Exception:
                row.append(float('nan'))
        print(f"    true y_h = {y_true:.4f}  ->  inferred at u=u5,u6,u7: " +
              " ".join(f"{r:7.4f}" for r in row) +
              f"   worst error {max(abs(r-y_true) for r in row if np.isfinite(r)):.4f}")

print("\n  With a correction to scaling (1 + a L^-omega), omega = 0.832 (3D Ising):")
F = FAM['F = x/(1+x)^2    (peaked at x=1)']
for amp in (0.0, 0.2, 0.5, -0.5):
    v = build(2.4819, BETA_NU, F, omega=0.832, amp=amp)
    r = [infer(v, u0, LS, BETA_NU) for u0 in (US[5], US[6], US[7])]
    print(f"    a = {amp:+.1f}  ->  " + " ".join(f"{x:7.4f}" for x in r) +
          f"   worst error {max(abs(x-2.4819) for x in r):.4f}")

print("\n  Sensitivity to |dlnF/dlnu| (the estimator divides by it).  At the PEAK of F")
print("  the derivative passes through zero and the estimator must blow up -- the run's")
print("  own guard is |dlnX/dlnu| < 0.05 -> ungauged.  Planted check:")
F = FAM['F = x^2 e^{-x}   (peaked at x=2)']
v = build(2.4819, BETA_NU, F)
for j in range(2, 10):
    u0 = US[j]
    i = j
    a, b = v[(LS[-1], US[i - 1])], v[(LS[-1], US[i + 1])]
    dln = math.log(abs(b / a)) / math.log(US[i + 1] / US[i - 1])
    try:
        y = infer(v, u0, LS, BETA_NU)
    except Exception:
        y = float('nan')
    print(f"    u = {u0:7.3f}  dlnF/dlnu = {dln:+7.4f}  inferred y_h = {y:8.4f}  "
          f"err {abs(y-2.4819):7.4f}" + ("   <-- guard would ungauge" if abs(dln) < 0.05 else ""))
