"""
Symbolic check of the cuscuton background, aimed at ONE question:

  Can a smooth (non-clustering) preferred-foliation dark energy CROSS w = -1?

k-essence conventions: L = P(X, phi), X = -(1/2) g^{mu nu} d_mu phi d_nu phi.
In FRW with homogeneous phi: X = phidot^2 / 2, so sqrt(2X) = |phidot|.

  rho   = 2 X P_X - P
  p     = P
  c_s^2 = P_X / (P_X + 2 X P_XX)

Cuscuton:  P = eps * mu2 * sqrt(2X) - V(phi),  eps = +1 or -1.
"""
import sympy as sp

X, mu2, V, eps = sp.symbols('X mu2 V epsilon', positive=True), None, None, None
X = sp.Symbol('X', positive=True)
mu2 = sp.Symbol('mu^2', positive=True)
V = sp.Symbol('V', positive=True)
eps = sp.Symbol('epsilon')

print("=" * 70)
print("1. CUSCUTON BACKGROUND")
print("=" * 70)

P = eps * mu2 * sp.sqrt(2 * X) - V
P_X = sp.diff(P, X)
P_XX = sp.diff(P, X, 2)

rho = sp.simplify(2 * X * P_X - P)
print(f"  P      = {P}")
print(f"  P_X    = {sp.simplify(P_X)}")
print(f"  rho    = 2*X*P_X - P = {rho}")
print(f"  p      = P = {P}")

# sound speed
denom = sp.simplify(P_X + 2 * X * P_XX)
print(f"\n  c_s^2 denominator  P_X + 2*X*P_XX = {denom}")
print(f"  -> c_s^2 = {sp.simplify(P_X)} / {denom}   ==> INFINITE (degenerate)")

print("\n" + "=" * 70)
print("2. EQUATION OF STATE  --  the crux")
print("=" * 70)

w = sp.simplify(P / rho)
w_plus_1 = sp.simplify(w + 1)
print(f"  w      = p/rho = {w}")
print(f"  w + 1  = {w_plus_1}")
print("\n  With sqrt(2X) = |phidot| >= 0, V > 0, this is eps * mu^2 * |phidot| / V.")
print("  => sign(w+1) = sign(eps), FIXED for all time.")
print("  => eps=+1 gives w >= -1 always;  eps=-1 gives w <= -1 always.")
print("  => A SINGLE CUSCUTON CAN NEVER CROSS w = -1.  Crossing needs w+1")
print("     to change sign, but eps is a discrete choice in the Lagrangian.")

print("\n" + "=" * 70)
print("3. WHY THAT MATTERS: crossing == the crest, identically")
print("=" * 70)
t = sp.Symbol('t')
H = sp.Function('H', positive=True)(t)
rho_t = sp.Function('rho', positive=True)(t)
w_t = sp.Function('w')(t)
# continuity: rhodot = -3 H (1+w) rho
cont = sp.Eq(sp.diff(rho_t, t), -3 * H * (1 + w_t) * rho_t)
print(f"  continuity: {cont}")
print("  rho > 0 and H > 0  =>  rhodot = 0  <==>  w = -1.")
print("  So 'the grand total crests' and 'w crosses -1' are THE SAME EVENT.")
print("  The extensive branch's crest at z=0.59 IS its phantom crossing.")

print("\n" + "=" * 70)
print("4. TWO-COMPONENT CUSCUTON: does it cross?")
print("=" * 70)
V1, V2 = sp.symbols('V_1 V_2', positive=True)
m1, m2 = sp.symbols('mu_1^2 mu_2^2', positive=True)
f1, f2 = sp.symbols('|phidot_1| |phidot_2|', nonnegative=True)

# component 1: eps=+1 -> rho1 = V1, p1 = +m1 f1 - V1
# component 2: eps=-1 -> rho2 = V2, p2 = -m2 f2 - V2
rho_tot = V1 + V2
p_tot = (m1 * f1 - V1) + (-m2 * f2 - V2)
w_eff = sp.simplify(p_tot / rho_tot)
w_eff_p1 = sp.simplify(w_eff + 1)
print(f"  rho_tot   = {rho_tot}")
print(f"  p_tot     = {p_tot}")
print(f"  w_eff + 1 = {w_eff_p1}")
print("\n  => w_eff crosses -1 exactly when  mu_1^2|phidot_1| = mu_2^2|phidot_2|.")
print("  Both components have c_s^2 = infinity, so the SUM is still exactly")
print("  smooth. Crossing achieved, smoothness preserved.")
print("\n  COST: the crossing epoch is set by when that equality happens, which")
print("  is fixed by the two potentials + initial conditions. It is TUNED,")
print("  not derived. z_c = 0.59 would be an input, not a prediction.")

print("\n" + "=" * 70)
print("5. WHAT THE EXTENSIVE READING ACTUALLY DEMANDS")
print("=" * 70)
print("  Extensive branch:  rho_DE  ∝  S_total(t)  =  N(t) * s(t)")
print("    N(t) = number of coordinating units (grows: structure forms)")
print("    s(t) = per-unit coordination balance (falls: proved monotone)")
print("  Crest:  d/dt[N s] = 0   <=>   dlnN/dt = -dlns/dt")
print("  So the crossing redshift is NOT free: it is fixed by the competition")
print("  between how fast halos are being made and how fast per-unit")
print("  coordination decays. THAT is the derivation the branch owes.")
print("  (checked numerically in crest_predict.py)")
