#!/usr/bin/env python3
"""TIER-3 dose adjudicator: the settling-dose law for organization.

Known dose points (adjudicated rounds, not re-staked): warm-up 60 -> momx
residual 14.9, 90 -> 12.3, 150 -> 2.53. New targets: warm-up 30 and 120.
  D1 organization at 30: momx_resid(30) > random p75 of its own run
  D2 monotone dose: momx_resid(30) > momx_resid(120)
  D3 interpolation: momx_resid(120) in [2.53, 12.34] (the bracketing neighbors)
D4 (early level law, f=300 only) and D5 (budget) adjudicate via tier_battery."""
import sys, json
import numpy as np
from tier_battery import adjudicate_dir

def resid_of(report):
    return report["T_organize"]["momx_resid"], report["T_organize"]["rand_p75"]

def adjudicate(rep30, rep120):
    r30, p75_30 = resid_of(rep30)
    r120, _ = resid_of(rep120)
    return {
        "D1_organization_at_30": {"momx_resid": r30, "rand_p75": p75_30, "pass": bool(r30 > p75_30)},
        "D2_monotone": {"r30": r30, "r120": r120, "pass": bool(r30 > r120)},
        "D3_interpolation": {"r120": r120, "band": [2.53, 12.34], "pass": bool(2.53 <= r120 <= 12.34)},
    }

if __name__ == "__main__":
    reps = {d: adjudicate_dir(d) for d in sys.argv[1:3]}
    d30, d120 = sys.argv[1], sys.argv[2]
    out = {"battery": reps, "dose": adjudicate(reps[d30], reps[d120])}
    print(json.dumps(out, indent=2))
