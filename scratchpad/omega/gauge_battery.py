#!/usr/bin/env python3
"""Two-sided gauge for the tier battery, driving adjudicate_arrays directly."""
import numpy as np
from tier_battery import adjudicate_arrays
rng = np.random.default_rng(20260827)
T = 2400; t = np.arange(T)
noise = lambda: np.exp(0.05 * rng.standard_normal(T))

def mk(level300, glate):
    v = np.empty(T); v[:300] = level300 * np.exp(0.01 * (t[:300] - 300)) * noise()[:300]
    v[300:] = v[299] * np.exp(np.log(glate) / 2100 * (t[300:] - 299)) * noise()[300:]
    return v

def build(P300, P1200, momx_g, ke_g, rand_g):
    views = [mk(P300[0], momx_g), mk(P300[1], 2.0), mk(P300[2], ke_g)]
    views += [mk(P300[3 + i], rand_g[i]) for i in range(64)]
    return np.stack(views)

P300 = np.concatenate([[5.0, 3.0, 1.0], rng.uniform(1, 6, 64)])
P1200 = 0.8 * P300                                    # ceilings shrink, as measured
rand_g = 0.8 * np.exp(0.3 * rng.standard_normal(64))  # residual ~ 1 around ceiling
# planted truth: momx organizes (resid ~15), ke protected (resid ~0.4)
r = adjudicate_arrays(build(P300, P1200, 12.0, 0.3, rand_g), P300, P1200, 1e-18)
ok = r["T_construction"]["premise_ok"] and r["T_budget"]["pass"] is True and r["T_levels"]["pass"] and r["T_organize"]["pass"] and r["T_protect"]["pass"]
print(f"planted truth: {'PASS all five' if ok else 'BAND ERROR ' + str(r)}")
assert ok
# fires, one prong at a time
r = adjudicate_arrays(build(P300, P1200, 0.8, 0.3, rand_g), P300, P1200, 1e-18)
print(f"planted no-organization: {'FIRE T-organize' if not r['T_organize']['pass'] else 'MISSED'}")
assert not r["T_organize"]["pass"]
r = adjudicate_arrays(build(P300, P1200, 12.0, 0.8, rand_g), P300, P1200, 1e-18)
print(f"planted unprotected ke: {'FIRE T-protect' if not r['T_protect']['pass'] else 'MISSED'}")
assert not r["T_protect"]["pass"]
shuf = np.concatenate([[5.0,3.0,1.0], rng.permutation(P300[3:])])
r = adjudicate_arrays(build(P300, P1200, 12.0, 0.3, rand_g), shuf, 0.8*shuf, 1e-18)
print(f"planted decorrelated levels: {'FIRE T-levels' if not r['T_levels']['pass'] else 'MISSED'} sp={r['T_levels']['spearman']}")
assert not r["T_levels"]["pass"]
v = build(P300, P1200, 12.0, 0.3, rand_g); v[0] = mk(5.0, 1.0)
v[0][1000:] *= np.exp(0.077 * np.arange(1400)); v[0] = np.minimum(v[0], 1e30)
r = adjudicate_arrays(v, P300, P1200, 1e-18)
print(f"planted budget burst: {'FIRE T-budget' if not r['T_budget']['pass'] else 'MISSED'} K={r['T_budget']['K']:.3f}")
assert not r["T_budget"]["pass"]
r = adjudicate_arrays(build(P300, P1200, 12.0, 0.3, rand_g), P300, P1200, 3e-4)
print(f"planted post-step zero misread as pre-step: {'VOID T-construction' if not r['T_construction']['premise_ok'] else 'MISSED'}")
assert not r["T_construction"]["premise_ok"]
print("gauge verdict: five arms PASS planted truth; each fires or voids on its own named plant. Two-sided.")
