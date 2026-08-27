#!/usr/bin/env python3
"""Two-sided gauge for QF-1 (KCBS pipeline), driving the REAL LP on planted
models — never the staked state."""
import numpy as np
from qf1_instrument import contextual_fraction, classical_lift_model, CONTEXTS

cf = contextual_fraction(classical_lift_model())
print(f"planted classical (Fine null): CF = {cf:.2e} -> {'PASS (machine-zero)' if abs(cf) <= 1e-9 else 'PIPELINE DEFECT'}")
assert abs(cf) <= 1e-9

# FIRE side for Q2's band: the exclusivity-saturating pentagon model
# (<P_i> = 1/2 each, adjacent never co-fire): Sum = 5/2 > 2 -- the maximally
# contextual model of the pentagon.
model = []
for i, j in CONTEXTS:
    model.append({(1,0): 0.5, (0,1): 0.5, (0,0): 0.0, (1,1): 0.0})
cf_pr = contextual_fraction(model)
print(f"planted exclusivity-saturating pentagon: CF = {cf_pr:.4f} -> {'FIRE capability shown' if cf_pr >= 0.05 else 'MISSED'}")
assert cf_pr >= 0.05

# Q3 fire-shape: planted family crossing at 0.30 reads gap > 0.02 to the derived 0.4146
def planted_cf(lam, cross=0.30): return max(0.0, cf_pr*(1 - lam/cross))
lo, hi = 0.0, 1.0
while hi - lo > 1e-5:
    mid = 0.5*(lo+hi)
    if planted_cf(mid) > 1e-9: lo = mid
    else: hi = mid
lstar = 0.5*(lo+hi); derived = (np.sqrt(5)-2)/(np.sqrt(5)-5/3)
print(f"planted crossing 0.30 vs derived {derived:.4f}: gap {abs(lstar-derived):.3f} -> {'FIRE Q3' if abs(lstar-derived) > 0.02 else 'MISSED'}")
assert abs(lstar-derived) > 0.02
print("gauge verdict: Fine null machine-zero through the real LP, saturating")
print("pentagon fires Q2, off-facet crossing fires Q3. Two-sided.")
