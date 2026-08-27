#!/usr/bin/env python3
"""Two-sided gauge for N3 and N4, driving the REAL frozen adjudicators in
analyze_tier.py on planted divergence series.

N3 bands: see analyze_tier.n3_adjudicate (conjuncts i/ii/iii + sustained-posability).
N4 band: growth ratios g_v = median(1200-2399)/median(60-300); all 3 declared below
the 25th pctile of 64 random views; FIRE if any declared above the random median.
Prong coverage is named per plant (house rule: OR-gates must name the firing prong)."""
import numpy as np
from analyze_tier import n3_adjudicate, n4_adjudicate
rng = np.random.default_rng(20260826)
T = 2400; t = np.arange(T)
noise = lambda: np.exp(0.05*rng.standard_normal(T))
grow  = lambda r, s0: s0*np.exp(r*t)*noise()
sat   = lambda r, s0, cap: np.minimum(grow(r,s0), cap)*noise()

# ---- N3
micro = sat(0.02, 1e-12, 1.0)
coarse = 0.1*sat(0.02, 1e-13, 0.1); coarse[0]=1e-16
r = n3_adjudicate(micro, coarse); print(f"N3 planted-pass: {'PASS' if r['pass'] and r['posable'] else 'BAND ERROR'}")
assert r['pass'] and r['posable']
c_g = 2.0*sat(0.02, 1e-12, 2.0); c_g[0]=1e-16
r = n3_adjudicate(micro, c_g); print(f"N3 planted-amplification: {'FIRE' if not r['pass'] else 'MISSED'} conjuncts={r['conjuncts']}")
assert not r['pass'] and r['conjuncts'][1] == False
c_b = np.full(T, 1e-8)*noise(); c_b[2200:] = 1e-8*np.exp(0.077*np.arange(200))*noise()[2200:]; c_b[0]=1e-16
r = n3_adjudicate(micro, c_b); print(f"N3 planted-budget-burst: {'FIRE' if not r['pass'] else 'MISSED'} conjuncts={r['conjuncts']}")
assert not r['pass'] and r['conjuncts'] == (True, True, False), "conjunct (iii) must be the firing prong"
m_dead = np.concatenate([np.full(60, 1e-2), np.full(T-60, 1e-9)])*noise()
r = n3_adjudicate(m_dead, 0.1*m_dead); print(f"N3 planted-dead-transient: {'VOID' if not r['posable'] else 'MISSED'} (posability gate)")
assert not r['posable']

# ---- N4: planted in the smoke's own geometry — both classes start ULP, both climb
def view(r_early, r_late):
    v = np.empty(T); v[:300] = grow(r_early, 1e-6)[:300]
    v[300:] = v[299]*np.exp(r_late*(t[300:]-299))*noise()[300:]
    return v
decl = np.stack([view(0.02, 0.0005) for _ in range(3)])                    # closed: slow late growth
rand = np.stack([view(0.02, 0.004+0.001*rng.standard_normal()) for _ in range(64)])
r = n4_adjudicate(decl, rand); print(f"N4 planted-privileged: {'PASS' if r['pass'] and not r['fired'] else 'BAND ERROR'} decl={[f'{x:.1f}' for x in r['declared_ratios']]} rand25={r['random_pctiles'][25]:.1f}")
assert r['pass'] and not r['fired']
decl_e = np.stack([view(0.02, 0.004+0.001*rng.standard_normal()) for _ in range(3)])
r = n4_adjudicate(decl_e, rand); print(f"N4 planted-equalized: {'FIRE' if r['fired'] else 'MISSED'}")
assert r['fired']
print("gauge verdict: N3 and N4 PASS on planted truth and FIRE on planted violation,")
print("prongs named: (ii) amplification, (iii) budget-burst, posability VOID by dead transient,")
print("N4 fired by equalized growth. Two-sided, driving the real adjudicators.")
