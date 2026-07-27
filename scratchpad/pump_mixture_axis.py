#!/usr/bin/env python3
"""The pump reframed as a convex combination -- and the SECOND axis that reframing exposes.

PUMP_RESULTS AMENDMENT 3 observes that a per-cell channel is linear and ferro is a
two-point mixture, so the pumped state is  1/2 K(d000) + 1/2 K(d111)  -- a convex
combination of two PRODUCT states, each share exactly zero.  Correct, and it means the
pumped state is a ONE-HIDDEN-BIT model: a latent bit chooses which product component,
and the three slots are conditionally independent given it.

That is exactly the object of Schneidman et al. 2003 Fig. 3 ("when one hidden binary
element determines the nature of pure pairwise interaction among the remaining elements,
the observable subnetwork can have an effective 3-body interaction"), whose abscissa is
the MIXTURE WEIGHT gamma = P(sigma4 = 0), not the noise amplitude of their Fig. 2.

Our campaign sat at gamma = 1/2 throughout, because that is what makes the input
sign-symmetric.  This sweeps the other axis.
"""
import itertools, json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pump_curve as PC
LN2 = math.log(2.0)
sh = lambda p: PC.share3_golden(p)

def delta(bits):
    p = np.zeros((2,2,2)); p[bits] = 1.0; return p

def mix(gamma):
    """gamma*|000> + (1-gamma)*|111>.  Pair marginals (gamma,0,0,1-gamma): perfectly
    correlated, so the pair-maxent IS the state -- share exactly zero at every gamma."""
    return gamma*delta((0,0,0)) + (1.0-gamma)*delta((1,1,1))

out = {"stage": "mixture_axis"}
print("1. THE DECOMPOSITION, checked exactly (AMENDMENT 3's claim)")
K = [PC.kernel(0.2, 0.15)]*3
lhs = PC.apply_percell(mix(0.5), K)
rhs = 0.5*PC.apply_percell(delta((0,0,0)), K) + 0.5*PC.apply_percell(delta((1,1,1)), K)
c0 = PC.apply_percell(delta((0,0,0)), K); c1 = PC.apply_percell(delta((1,1,1)), K)
print(f"   |K(ferro) - [K(d000)+K(d111)]/2|    = {np.abs(lhs-rhs).max():.3e}")
print(f"   share of component K(d000)          = {sh(c0):.3e}")
print(f"   share of component K(d111)          = {sh(c1):.3e}")
print(f"   share of the 50/50 mixture          = {sh(lhs):.6e}")
print("   -> constituents exactly zero, combination positive: Kahle's object, exactly.")
out["decomposition"] = {"max_dev": float(np.abs(lhs-rhs).max()),
                        "share_c0": sh(c0), "share_c1": sh(c1), "share_mix": sh(lhs)}

print()
print("2. INPUT share is zero at EVERY mixture weight (so gamma is a clean axis)")
w = max(sh(mix(g)) for g in (0.05,0.2,0.35,0.5,0.65,0.8,0.95))
print(f"   worst share of the un-pumped mixture over 7 weights = {w:.3e}")
out["input_share_max"] = float(w)

print()
print("3. THE SECOND AXIS: a UNITAL channel (a = 0) on an asymmetric mixture.")
print("   valve_needs_asymmetry needs BOTH hypotheses; at gamma != 1/2 the input is")
print("   NOT sign-symmetric, so the theorem does not apply and the pump should run.")
print(f"   {'gamma':>7}" + "".join(f"{f's={s}':>14}" for s in (0.05,0.10,0.20,0.30)))
rows=[]
for g in (0.50,0.45,0.40,0.30,0.20,0.10,0.05):
    vals=[sh(PC.apply_percell(mix(g), [PC.kernel(0.0,s)]*3)) for s in (0.05,0.10,0.20,0.30)]
    rows.append({"gamma":g,"share_by_s":vals})
    print(f"   {g:7.2f}" + "".join(f"{v:14.6e}" for v in vals))
out["unital_vs_gamma"]=rows

print()
print("4. Peak of the state-asymmetry pump, and its exponent in (1/2 - gamma)")
for s in (0.10,0.20):
    gs=np.linspace(0.5-0.45,0.5,181); v=[sh(PC.apply_percell(mix(g),[PC.kernel(0.0,s)]*3)) for g in gs]
    v=np.array(v); i=int(v.argmax())
    d=0.5-gs; m=(d>1e-3)&(d<0.05)&(v>1e-13)
    slope=np.polyfit(np.log(d[m]),np.log(v[m]),1)[0] if m.sum()>3 else float('nan')
    print(f"   s={s}: peak {v[i]:.6e} nat at gamma={gs[i]:.4f} "
          f"({100*v[i]/LN2:.2f}% of ln2); small-detuning exponent in (1/2-gamma) = {slope:.3f}")
    out[f"peak_s{s}"]={"peak":float(v[i]),"gamma":float(gs[i]),"exponent":float(slope)}

json.dump(out, open("pump_mixture_axis.json","w"), indent=1)
print("\nwrote pump_mixture_axis.json")

# ---------------------------------------------------------------------------
# 5. THE SECOND AXIS HAS ITS OWN CLOSED FORM.  Derived by the same route as
# PUMP_PREREG 4.3, with the input's magnetisation carrying the detuning.
#
# Input mix(gamma): m = 2*gamma-1 = -2*delta, pair r = 1, triple c = -2*delta.
# Through a UNITAL kernel (a=0, kappa=1-2s):  m -> -2*delta*kappa,
# r -> kappa^2, c -> -2*delta*kappa^3.
# Maximiser c* = 3*r*m/(1+2r) at r=kappa^2 gives  Dc = 4*delta*kappa^3*(1-kappa^2)/(1+2kappa^2),
# and Delta = 1/2*|g''|*Dc^2 with |g''| = (1+2r)/[(1+3r)(1-r)]:
#
#     Delta = 8 * delta^2 * kappa^6 * (1 - kappa^2) / [ (1+2kappa^2)(1+3kappa^2) ]
#
# Note the CONTRAST with the channel-asymmetry law, which carries (1-r0) in the
# DENOMINATOR: this one carries (1-kappa^2) in the NUMERATOR, so it VANISHES as
# the noise goes to zero and peaks at intermediate strength.
def closed_form_state_axis(delta, s):
    u = (1.0 - 2.0*s)**2
    return 8.0*delta*delta*u**3*(1.0-u)/((1.0+2.0*u)*(1.0+3.0*u))

print()
print("5. THE STATE-AXIS CLOSED FORM, derived here, tested against the exact solver")
print(f"   {'s':>6}{'delta':>8}{'exact':>15}{'closed form':>15}{'ratio':>9}")
worst = 0.0
for s in (0.05, 0.10, 0.20, 0.30):
    for d in (0.01, 0.02, 0.05, 0.10):
        ex = sh(PC.apply_percell(mix(0.5-d), [PC.kernel(0.0, s)]*3))
        cf = closed_form_state_axis(d, s)
        worst = max(worst, abs(cf/ex - 1.0))
        print(f"   {s:6.2f}{d:8.2f}{ex:15.6e}{cf:15.6e}{cf/ex:9.4f}")
print(f"   worst relative deviation over the 16 points = {100*worst:.2f}%")
out["state_axis_closed_form"] = {"formula":
    "8*delta^2*u^3*(1-u)/((1+2u)(1+3u)), u=(1-2s)^2, delta=1/2-gamma",
    "worst_rel_dev": float(worst)}
import json as _j; _j.dump(out, open("pump_mixture_axis.json","w"), indent=1)
