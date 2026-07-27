#!/usr/bin/env python3
"""P-SCHNEIDMAN: reproduce Schneidman, Still, Berry & Bialek, PRL 91:238701 (2003),
Fig. 2 -- the published pump curve, and the campaign's one EXTERNAL calibration.

Fig. 2 caption (from the PDF text layer): "Correlated-information of orders 2 and 3
and the multi-information for 3 variables whose joint probability distribution is
given by noisy logical functions.  Each panel presents the I_C's and I values for a
noisy version of one boolean gate (XOR in first row, OR in second, AND in third), as
a function of noise amplitude.  The three types of noise are output noise
(probability of flipping s3), input noise (probability of flipping s1) and
input-dependent output noise (probability of flipping s3, given that s1 = 1 and
s2 = 1)."

Body text: "pure 2-body interactions such as AND and OR show a 3-body interaction
component for some types of noise (even for noise sources which are state
dependent). ... For these three functions, input noise only changes the strength of
the existing interactions, rather than introducing a new kind of effective
interaction."

Which COLUMN creates on AND is a figure reading we do not have, so this is staked as
a SHAPE agreement, not a numerical one (PUMP_PRIOR_ART_ADDENDUM sec A1).
Share = I_C^(3) is Core/Share.lean's `share`, which IS their Eq. 6.
"""
import itertools, json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pump_curve as PC
from gate_pump_indep import share3_independent   # spot-check only: the dense-grid
# fallback is far too slow for 9x51 panels, and the two were gated to 8.9e-16 at a4d3b38.
def sh(p):
    return PC.share3_golden(p)
LN2 = math.log(2.0)

def H(p):
    q = np.asarray(p, float).ravel(); nz = q > 0
    return float(-(q[nz]*np.log(q[nz])).sum())

def multi_information(p):
    """I = sum_i H(x_i) - H(x)  (their Eq. 3)."""
    return sum(H(p.sum(axis=tuple(j for j in range(3) if j != i))) for i in range(3)) - H(p)

GATES = {"AND": lambda a, b: a & b, "OR": lambda a, b: a | b, "XOR": lambda a, b: a ^ b}

def state(fn, kind, q):
    """s1, s2 uniform iid; s3 from the gate; q = noise amplitude in [0, 0.5]."""
    p = np.zeros((2, 2, 2))
    for s1, s2 in itertools.product((0, 1), repeat=2):
        if kind == "input":                      # flip s1 BEFORE the gate; observe the true s1
            for f, w in ((0, 1 - q), (1, q)):
                p[s1, s2, fn(s1 ^ f, s2)] += 0.25 * w
        elif kind == "output":                   # flip s3 AFTER the gate
            y = fn(s1, s2)
            p[s1, s2, y]     += 0.25 * (1 - q)
            p[s1, s2, y ^ 1] += 0.25 * q
        elif kind == "outdep":                   # flip s3 only when s1 = s2 = 1
            y = fn(s1, s2); qq = q if (s1 == 1 and s2 == 1) else 0.0
            p[s1, s2, y]     += 0.25 * (1 - qq)
            p[s1, s2, y ^ 1] += 0.25 * qq
    return p

KINDS = [("output", "P(flip s3)"), ("input", "P(flip s1)"), ("outdep", "P(flip s3|s1=s2=1)")]
grid = np.linspace(0.0, 0.5, 26)
out = {"stage": "schneidman_fig2", "grid": grid.tolist(), "panels": {}, "fig1": {}}

print("FIG. 1 -- the noiseless table (exact check)")
print(f"  {'gate':5s}{'I':>9}{'I_C^(3)':>10}{'I_C^(2)':>10}   paper")
paper1 = {"AND": (0.8113, 0.0, 0.8113), "OR": (0.8113, 0.0, 0.8113), "XOR": (1.0, 1.0, 0.0)}
for nm, fn in GATES.items():
    p = state(fn, "output", 0.0)
    I = multi_information(p)/LN2; i3 = sh(p)/LN2
    out["fig1"][nm] = {"I": I, "IC3": i3, "IC2": I - i3}
    pi, p3, p2 = paper1[nm]
    print(f"  {nm:5s}{I:9.4f}{i3:10.4f}{I-i3:10.4f}   I={pi} IC3={p3} IC2={p2}  "
          f"{'PASS' if abs(I-pi)<5e-5 and abs(i3-p3)<1e-9 and abs((I-i3)-p2)<5e-5 else '**FAIL**'}")

print("\nFIG. 2 -- I_C^(3) in bits vs noise amplitude (9 panels)")
print("  creation = I_C^(3) rises above 0 from a gate whose noiseless I_C^(3) is 0")
for nm, fn in GATES.items():
    for kind, lab in KINDS:
        ic3 = [sh(state(fn, kind, q))/LN2 for q in grid]
        ic2 = [multi_information(state(fn, kind, q))/LN2 - v for q, v in zip(grid, ic3)]
        out["panels"][f"{nm}/{kind}"] = {"IC3": ic3, "IC2": ic2, "label": lab}
        mx = float(np.max(ic3)); amx = float(grid[int(np.argmax(ic3))])
        base = ic3[0]
        creates = mx > base + 1e-9
        print(f"  {nm:4s} {lab:22s} IC3(0)={base:.4f}  max={mx:.4f} at q={amx:.2f}  "
              f"{'CREATES' if creates else 'no creation'}")

json.dump(out, open("pump_schneidman_fig2.json", "w"), indent=1)
print("\nSPOT-CHECK against the independent solver (dense-grid method):")
w=0.0
for nm,fn in GATES.items():
    for kind,_ in KINDS:
        for q in (0.1,0.3):
            st=state(fn,kind,q); w=max(w,abs(sh(st)-share3_independent(st)))
print(f"  worst |golden - independent| over 18 panel points = {w:.3e}")
print("\nwrote pump_schneidman_fig2.json")
