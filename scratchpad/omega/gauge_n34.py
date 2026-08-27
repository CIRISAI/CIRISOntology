#!/usr/bin/env python3
"""Two-sided gauge for N3 (tier closure within budget) and N4 (view privilege),
on planted divergence series with the frozen adjudicators.

N3 frozen bands (frames 0-2399):
  (i)  coarse_div(0) <= 1e-9 * max(micro_div)           [macro-matched construction]
  (ii) median over frames 1200-2399 of coarse/micro <= 0.5
  (iii) median per-frame growth ratio of coarse_div, over frames where
        coarse_div > 1% of its max, <= 1.05              [Aggregation budget]
N4 frozen band: log-slope of each declared view over frames 10-300
  all 4 below the 25th pct of 64 random-view slopes; FIRE if any above median."""
import numpy as np
rng = np.random.default_rng(20260826)
T = 2400; t = np.arange(T)

def n3_adjudicate(micro, coarse):
    i  = coarse[0] <= 1e-9*micro.max()
    ii = np.median(coarse[1200:]/np.maximum(micro[1200:],1e-300)) <= 0.5
    m  = coarse > 0.01*coarse.max()
    g  = coarse[1:][m[1:]]/np.maximum(coarse[:-1][m[1:]],1e-300)
    iii= np.median(g) <= 1.05
    return i and ii and iii, (bool(i),bool(ii),bool(iii))

def n4_adjudicate(decl, rand):        # decl: (4,T)  rand: (64,T)
    sl = lambda d: np.polyfit(t[10:300], np.log(np.maximum(d[10:300],1e-300)), 1)[0]
    ds = np.array([sl(d) for d in decl]); rs = np.array([sl(r) for r in rand])
    passed = all(ds < np.percentile(rs,25)); fired = any(ds > np.median(rs))
    return passed, fired

noise = lambda: np.exp(0.05*rng.standard_normal(T))
grow  = lambda r, s0: s0*np.exp(r*t)*noise()
sat   = lambda r, s0, cap: np.minimum(grow(r,s0), cap)*noise()

# N3 PASS: micro grows to saturation; coarse tracks at 0.1x, budget-respecting
micro = sat(0.02, 1e-12, 1.0)
coarse= 0.1*sat(0.02, 1e-13, 0.1); coarse[0]=1e-16
p3,_ = n3_adjudicate(micro, coarse); print(f"N3 planted-pass: {'PASS' if p3 else 'BAND ERROR'}")
# N3 FIRE a: coarse EXPANDS beyond budget in its own regime (ratio 1.08/frame)
c_f = sat(0.077, 1e-13, 10.0); c_f[0]=1e-16   # e^0.077=1.080
f3a,d3a = n3_adjudicate(micro, c_f); print(f"N3 planted-expansion: {'FIRE' if not f3a else 'MISSED'} conjuncts={d3a}")
# N3 FIRE b: coarse EXCEEDS micro (amplification)
c_g = 2.0*sat(0.02, 1e-12, 2.0); c_g[0]=1e-16
f3b,d3b = n3_adjudicate(micro, c_g); print(f"N3 planted-amplification: {'FIRE' if not f3b else 'MISSED'} conjuncts={d3b}")

# N4 PASS: declared slopes 0.01, random slopes ~0.05
decl = np.stack([grow(0.010,1e-10) for _ in range(4)])
rand = np.stack([grow(0.050+0.005*rng.standard_normal(),1e-10) for _ in range(64)])
p4,f4 = n4_adjudicate(decl, rand); print(f"N4 planted-privileged: {'PASS' if p4 and not f4 else 'BAND ERROR'}")
# N4 FIRE: declared statistically identical to random
decl_e = np.stack([grow(0.050+0.005*rng.standard_normal(),1e-10) for _ in range(4)])
p4e,f4e = n4_adjudicate(decl_e, rand); print(f"N4 planted-equalized: {'FIRE' if f4e else 'MISSED'} (pass={p4e})")

assert p3 and not f3a and not f3b and p4 and not f4 and f4e
print("gauge verdict: N3 and N4 pass on planted truth and FIRE on planted violation. Two-sided.")

# N3 FIRE c: budget conjunct (iii) ALONE -- late burst at 1.08/frame kept under micro
c_b = np.full(T, 1e-8)*noise()
c_b[2200:] = 1e-8*np.exp(0.077*np.arange(200))*noise()[2200:]
c_b[0] = 1e-16
f3c,d3c = n3_adjudicate(micro, c_b)
print(f"N3 planted-budget-burst: {'FIRE' if not f3c else 'MISSED'} conjuncts={d3c}")
assert not f3c and d3c == (True, True, False), "conjunct (iii) must be the firing prong"
print("prong coverage: (ii) fired by expansion+amplification plants, (iii) by budget-burst. Named.")
