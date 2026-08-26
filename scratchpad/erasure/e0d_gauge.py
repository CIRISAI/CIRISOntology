#!/usr/bin/env python3
"""E0d gauge — can the battery estimator read an underdamped memory at all?

Synthetic double-well underdamped Langevin (BAOAB) with KNOWN f0, Q, so tau_R is
known exactly. The estimator (battery.gains, unchanged) reads bit=sign(x), fibers=
within-well position x velocity. Verifies: (a) a closure defect exists above the
NULL floor, (b) tau_c tracks the known relaxation time, (c) the velocity component
carries the underdamped signature. THIS RUN uses placeholder f0/Q (dev); E0d proper
reruns with stage-2-pinned metadata values.
"""
import sys, json
import numpy as np
import importlib.util
_s = importlib.util.spec_from_file_location("bt", "../fiber_pilot/battery.py")
bt = importlib.util.module_from_spec(_s); _s.loader.exec_module(bt)

F0 = float(sys.argv[1]) if len(sys.argv) > 1 else 1090.0
Q  = float(sys.argv[2]) if len(sys.argv) > 2 else 7.0
FS = float(sys.argv[3]) if len(sys.argv) > 3 else 40000.0
DUR = 30.0
SUB = 8                       # sim substeps per sample
KT, EB_KT = 1.0, 4.0          # barrier = 4 kT
rng = np.random.default_rng(20260826)

w0 = 2*np.pi*F0; m = 1.0; x0 = 1.0
Eb = EB_KT*KT; 
# quartic U = Eb((x/x0)^2-1)^2 ; curvature at well = 8Eb/x0^2 = m w0^2 -> fix x0
x0 = np.sqrt(8*Eb/(m*w0**2))
gamma = m*w0/Q
tau_R = 2*m/gamma             # amplitude relaxation = Q/(pi f0)
dt = 1.0/(FS*SUB)
c1 = np.exp(-gamma/m*dt); c2 = np.sqrt(KT/m*(1-c1**2))
n = int(DUR*FS)
x, v = x0, 0.0
xs = np.empty(n)
F = lambda x: -4*Eb*x*(x*x/(x0*x0)-1)/(x0*x0)
for i in range(n):
    for _ in range(SUB):
        v += 0.5*dt*F(x)/m; x += 0.5*dt*v
        v = c1*v + c2*rng.standard_normal()
        x += 0.5*dt*v; v += 0.5*dt*F(x)/m
    xs[i] = x
coarse = (xs >= 0).astype(np.int8)
sw = np.mean(coarse[1:] != coarse[:-1])
print(f"f0={F0} Q={Q} fs={FS}  tau_R={tau_R*1000:.3f} ms  x0={x0:.4f}  switch/sample={sw:.5f}")

hz = [0.00005, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02]
g = bt.gains(xs, coarse, FS, hz, rng=np.random.default_rng(5))
# NULL: telegraph with same switch stats + independent within-well AR noise
null_force, null_coarse = bt.fp.__dict__ and None, None
p01 = np.mean(coarse[1:][coarse[:-1]==0]==1); p10 = np.mean(coarse[1:][coarse[:-1]==1]==0)
s = np.empty(n, np.int8); s[0]=1; u = rng.random(n)
for i in range(1, n):
    s[i] = 1-s[i-1] if u[i] < (p01 if s[i-1]==0 else p10) else s[i-1]
from scipy.signal import lfilter
fine = lfilter([1.0],[1.0,-1.2,0.3], rng.normal(0, 0.1, n+500))[500:]
fine = fine/fine.std()*np.std(xs[coarse==1]-np.mean(xs[coarse==1]))
xs_null = np.where(s==0,-x0,x0) + fine
gn = bt.gains(xs_null, s.astype(np.int8), FS, hz, rng=np.random.default_rng(6))
print(f"{'h(ms)':>8} {'REAL dyn_gain':>14} {'ci_lo':>9} {'NULL dyn_gain':>14}")
tau_c = None
for r, rn_ in zip(g, gn):
    print(f"{r['horizon_s']*1000:8.2f} {r['dyn_gain']:+14.5f} {r['dyn_ci'][0]:+9.5f} {rn_['dyn_gain']:+14.5f}")
    if tau_c is None and r['dyn_ci'][0] <= 0: tau_c = r['horizon_s']
print(f"\ntau_c (first dyn CI touching 0) = {None if tau_c is None else tau_c*1000} ms   vs known tau_R = {tau_R*1000:.2f} ms")
print(f"ratio = {'N/A' if tau_c is None else round(tau_c/tau_R,2)}   (E2 band: within 2x)")
