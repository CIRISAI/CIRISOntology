"""INDEPENDENT gate on scratchpad/pump_curve.py (task #9).

Nothing here imports pump_curve's solvers to check pump_curve's solvers.  The
share is recomputed by a THIRD method (Brent on the stationarity condition +
a dense grid bracket), the channel is checked bit-exactly against a MACHINE-
CHECKED rational identity in Core/Valve.lean, and the moment law is checked
against the prereg's own algebra.
"""
import itertools, math, sys, os
import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import pump_curve as PC

LN2 = math.log(2.0)
ok = lambda b: "PASS" if b else "**FAIL**"

BITS = np.array([[(i >> b) & 1 for b in (2,1,0)] for i in range(8)])
CHI  = np.array([1.0 if BITS[i].sum() % 2 == 0 else -1.0 for i in range(8)])
EVEN = [i for i in range(8) if BITS[i].sum() % 2 == 0]
ODD  = [i for i in range(8) if BITS[i].sum() % 2 == 1]

def H(p):
    q = np.asarray(p, float).ravel(); nz = q > 0
    return float(-(q[nz]*np.log(q[nz])).sum())

def share3_independent(p):
    """Third method: Brent root of log(prod_even) - log(prod_odd) on the chi line,
    bracketed by a dense grid.  Structurally unlike golden section and unlike the
    repository's bisection."""
    p8 = np.asarray(p, float).ravel()
    c0 = float(p8 @ CHI); A = 8.0*p8 - c0*CHI
    lo = float(np.max(-A[CHI > 0])); hi = float(np.min(A[CHI < 0]))
    cell = lambda c: (A + c*CHI)/8.0
    def g(c):
        q = cell(c)
        if q.min() <= 0: return np.nan
        return float(np.log(q[EVEN]).sum() - np.log(q[ODD]).sum())
    eps = (hi-lo)*1e-12
    lo2, hi2 = lo+eps, hi-eps
    glo, ghi = g(lo2), g(hi2)
    if not (np.isfinite(glo) and np.isfinite(ghi)) or glo*ghi > 0:
        grid = np.linspace(lo2, hi2, 200001)          # dense fallback bracket
        vals = np.array([H(cell(c)) for c in grid])
        return float(vals.max() - H(p8))
    cstar = brentq(g, lo2, hi2, xtol=1e-16, rtol=8.9e-16, maxiter=500)
    return float(H(cell(cstar)) - H(p8))

print("="*74); print("GATE 1  channel vs a MACHINE-CHECKED rational identity")
print("  Core/Valve.lean  channel3_damp_ferro : channel3 damp damp damp ferro = bulge")
print("  bulge = 9/16 on (0,0,0), 1/16 on each of the other seven.")
K = PC.kernel(0.5, 0.25)                      # damp: p01=1/2, p10=0
out = PC.apply_percell(PC.repetition(3), [K]*3).ravel()
want = np.full(8, 1/16.0); want[0] = 9/16.0
err = float(np.abs(out-want).max())
print(f"  max |computed - exact rational| = {err:.3e}   {ok(err < 1e-15)}")

print("="*74); print("GATE 2  plumb lines, share recomputed by an INDEPENDENT third method")
states = {
    "parity  (share_parity = ln2)":        (PC.parity_state(), LN2, "eq"),
    "ferro   (share_ferro = 0)":           (PC.repetition(3), 0.0, "eq"),
    "indep   (share_indep = 0)":           (np.full((2,2,2), 0.125), 0.0, "eq"),
    "product (share_prod3 = 0)":           (np.einsum('i,j,k->ijk',[.3,.7],[.2,.8],[.55,.45]), 0.0, "eq"),
    "signsym (share_eq_zero_of_signSym)":  (None, 0.0, "eq"),
    "bulge   (valve_upward_bound)":        (PC.apply_percell(PC.repetition(3), [K]*3),
                                            LN2 + 0.75*math.log(3) - (17/32)*math.log(17), "ge"),
}
rng = np.random.default_rng(7)
v = rng.random(4); ss = np.zeros(8)
for i in range(8):
    ss[i] = v[min(i, 7-i)]
ss /= ss.sum(); states["signsym (share_eq_zero_of_signSym)"] = (ss.reshape(2,2,2), 0.0, "eq")
allok = True
for name,(p,target,mode) in states.items():
    mine = share3_independent(p)
    theirs, gap = PC.share3(p)
    if mode == "eq":
        good = abs(mine-target) < 1e-12 and abs(theirs-target) < 1e-12
        print(f"  {name:38s} indep={mine: .12e} theirs={theirs: .12e} "
              f"2-solver gap={gap:.1e}  {ok(good)}")
    else:
        good = mine >= target - 1e-12 and theirs >= target - 1e-12
        print(f"  {name:38s} indep={mine: .12f} theirs={theirs: .12f} "
              f">= {target:.12f}  {ok(good)}")
    allok &= good
print(f"  cap: every reading <= ln2 ?  {ok(all(share3_independent(p) <= LN2+1e-12 for p,_,_ in states.values()))}")

print("="*74); print("GATE 3  two solvers vs the third, on random states")
worst_pair = worst_ind = 0.0; n = 4000
for i in range(n):
    p = rng.random(8); p /= p.sum()
    t, gp = PC.share3(p.reshape(2,2,2))
    m = share3_independent(p.reshape(2,2,2))
    worst_pair = max(worst_pair, gp); worst_ind = max(worst_ind, abs(t-m))
print(f"  {n} random states")
print(f"  worst golden-vs-bisection gap      = {worst_pair:.3e}   (staked 1e-12)  {ok(worst_pair<1e-12)}")
print(f"  worst (their mean) vs INDEPENDENT  = {worst_ind:.3e}   {ok(worst_ind<1e-11)}")

print("="*74); print("GATE 4  P-EVEN: Delta(-a,s) == Delta(+a,s) exactly, on ferro")
worst = 0.0
for s in (0.05,0.1,0.2,0.3,0.4):
    for a in (0.01,0.05,0.1,0.2):
        if abs(a) > 2*min(s,1-s): continue
        dp = share3_independent(PC.apply_percell(PC.repetition(3), [PC.kernel(a,s)]*3))
        dm = share3_independent(PC.apply_percell(PC.repetition(3), [PC.kernel(-a,s)]*3))
        worst = max(worst, abs(dp-dm))
print(f"  worst |Delta(+a)-Delta(-a)| = {worst:.3e}   {ok(worst < 1e-12)}")

print("="*74); print("GATE 5  moment law m=a, r=r0+a^2, c=3*r0*a+a^3  (prereg 4.3)")
worst = 0.0
for rho in (0.3,0.7,1.0):
    for s in (0.05,0.15,0.3):
        for a in (0.02,0.08,0.15):
            if abs(a) > 2*min(s,1-s): continue
            q = PC.apply_percell(PC.ferro_mix(rho,3), [PC.kernel(a,s)]*3).ravel()
            z = 1.0-2.0*BITS
            m = float(q @ z[:,0]); r = float(q @ (z[:,0]*z[:,1]))
            c = float(q @ (z[:,0]*z[:,1]*z[:,2]))
            k2 = (1-2*s)**2; r0 = k2*rho
            worst = max(worst, abs(m-a), abs(r-(r0+a*a)), abs(c-(3*r0*a+a**3)))
print(f"  worst deviation from the prereg's moment line = {worst:.3e}   {ok(worst < 1e-14)}")

print("="*74); print("GATE 6  Schneidman 2003 Fig. 1 -- the ONE external calibration")
def gate(fn):
    p = np.zeros((2,2,2))
    for x1 in (0,1):
        for x2 in (0,1):
            p[x1,x2,fn(x1,x2)] += 0.25
    return p
for nm, fn, ic3, ic2 in (("AND", lambda a,b: a&b, 0.0, 0.8113),
                         ("OR",  lambda a,b: a|b, 0.0, 0.8113),
                         ("XOR", lambda a,b: a^b, 1.0, 0.0)):
    p = gate(fn)
    s3 = share3_independent(p)/LN2
    multi = (sum(H(p.sum(axis=tuple(j for j in range(3) if j!=i))) for i in range(3)) - H(p))/LN2
    print(f"  {nm:4s} I_C^(3)={s3:7.4f} bits (paper {ic3:.4f})   "
          f"I_C^(2)={multi-s3:7.4f} bits (paper {ic2:.4f})   "
          f"{ok(abs(s3-ic3)<1e-9 and abs((multi-s3)-ic2)<5e-5)}")
