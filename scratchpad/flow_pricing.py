#!/usr/bin/env python3
"""
flow_pricing.py -- pricing the FLOW (maintenance) reading of dark energy.

Pre-registration: scratchpad/FLOW_PRICING_PREREG.md, committed at 61187de
BEFORE this file existed.  Nothing here is tuned to reach an answer.

The claim under test:
    dark energy is the Landauer cost, per unit volume per unit time, of the
    error correction that keeps existing pattern from decaying,
        P        = N_maint * lambda * kB * T * ln2      [W/m^3]
        rho_DE   = P / (3H)                             [J/m^3]
    the second line being the IMPORTED bridge B1 (GR requires no such power).

Run:  ./temporal-share/qenv/bin/python flow_pricing.py
"""

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "temporal-share"))
import DE_LEDGER_MODEL as dl                                    # noqa: E402

OUT = []


def P(s=""):
    print(s)
    OUT.append(s)


def dex(x):
    return np.log10(x)


# ---------------------------------------------------------------------------
# 1. CONSTANTS AND THE TARGET
# ---------------------------------------------------------------------------
KB = 1.380649e-23              # J/K            (SI defining constant)
HBAR = 1.054571817e-34         # J s
HPL = 6.62607015e-34           # J s            (SI defining constant)
C = 2.99792458e8               # m/s            (SI defining constant)
G = 6.67430e-11                # m^3 kg^-1 s^-2 (CODATA 2018)
LN2 = np.log(2.0)
M_P = 1.67262192369e-27        # kg  proton
M_E = 9.1093837015e-31        # kg  electron
A_RAD = 7.565733e-16           # J m^-3 K^-4    (radiation constant, 4 sigma/c)
MPC = 3.0856775814913673e22    # m
MSUN = 1.98892e30              # kg
YR = 3.1557e7                  # s (Julian)

H0_KMSMPC = 67.4               # Planck 2018 -- same value DE_LEDGER_MODEL uses
H0 = H0_KMSMPC * 1e3 / MPC     # s^-1
T_HUB = 1.0 / H0               # s
OM_L = 0.6847                  # Planck 2018 TT,TE,EE+lowE+lensing
OM_M = 0.315
OM_B = 0.0493                  # omega_b h^2 = 0.02237
OM_STAR = 0.0027               # Fukugita & Peebles 2004  [FROM MEMORY, +-50%]
T_CMB = 2.7255                 # Fixsen 2009

RHO_CRIT = 3.0 * H0 ** 2 / (8 * np.pi * G)          # kg/m^3
U_CRIT = RHO_CRIT * C ** 2                          # J/m^3
RHO_DE = OM_L * U_CRIT                              # J/m^3   <- THE TARGET
P_REQ = 3.0 * H0 * RHO_DE                           # W/m^3   <- flow target

L_PL2 = HBAR * G / C ** 3                           # Planck area, m^2
R_HUB = C / H0
V_HUB = 4.0 / 3.0 * np.pi * R_HUB ** 3
T_DS = HBAR * H0 / (2.0 * np.pi * KB)               # de Sitter horizon temp

LAM_SHAPE = 1.671                                   # DE_LEDGER_MODEL.md S4
LAM_SHAPE_LO, LAM_SHAPE_HI = 1.33, 2.02

P("=" * 78)
P("FLOW PRICING -- dark energy as a maintenance (error-correction) power")
P("prereg: scratchpad/FLOW_PRICING_PREREG.md @ 61187de")
P("=" * 78)
P()
P("--- 1. CONSTANTS AND TARGET " + "-" * 50)
P(f"  H0                 = {H0_KMSMPC} km/s/Mpc = {H0:.6e} s^-1")
P(f"  Hubble time 1/H0   = {T_HUB:.4e} s = {T_HUB/YR/1e9:.3f} Gyr")
P(f"  rho_crit,0         = {RHO_CRIT:.4e} kg/m^3")
P(f"  u_crit,0 = rho c^2 = {U_CRIT:.4e} J/m^3")
P(f"  TARGET rho_DE      = {RHO_DE:.4e} J/m^3   (Omega_L = {OM_L})")
P(f"  TARGET P = 3 H rho_DE = {P_REQ:.4e} W/m^3")
P(f"  de Sitter horizon T_dS = hbar H /(2 pi kB) = {T_DS:.4e} K")
P(f"  Hubble volume      = {V_HUB:.4e} m^3   (radius {R_HUB:.4e} m)")
P()

# ---------------------------------------------------------------------------
# 2. CANDIDATE N_maint  [bits / m^3]
# ---------------------------------------------------------------------------
P("--- 2. CANDIDATE N_maint (bits/m^3) " + "-" * 42)

# 2a. CMB photon entropy, FIRST PRINCIPLES (not from a table)
s_cmb = (4.0 / 3.0) * A_RAD * T_CMB ** 3 / KB       # k_B units per m^3
N_cmb = s_cmb / LN2
u_cmb = A_RAD * T_CMB ** 4
n_gamma = 2 * 1.20205690 / np.pi ** 2 * (KB * T_CMB / (HBAR * C)) ** 3
P(f"  CMB: u = {u_cmb:.4e} J/m^3, s = {s_cmb:.4e} k/m^3, "
  f"n_gam = {n_gamma:.3e}/m^3, s/n = {s_cmb/n_gamma:.2f} k")
P(f"       N_cmb = {N_cmb:.4e} bits/m^3")

# 2b. baryons
n_b = OM_B * RHO_CRIT / M_P
n_star = OM_STAR * RHO_CRIT / M_P
P(f"  baryons: n_b = {n_b:.4e} /m^3 ; in stars n_* = {n_star:.4e} /m^3")


def sackur_tetrode(n, T, m):
    """entropy per particle, ideal monatomic gas, in k_B."""
    lam = HPL / np.sqrt(2.0 * np.pi * m * KB * T)
    return -np.log(n * lam ** 3) + 2.5


# 2c. IGM gas entropy, FIRST PRINCIPLES via Sackur-Tetrode (ionised H)
gas_ST = {}
for Tg in (1e5, 1e6, 1e7):
    s_per_b = sackur_tetrode(n_b, Tg, M_P) + sackur_tetrode(n_b, Tg, M_E)
    gas_ST[Tg] = n_b * s_per_b / LN2
    P(f"  IGM gas @ {Tg:.0e} K: S-T gives {s_per_b:.1f} k/baryon "
      f"-> N = {gas_ST[Tg]:.4e} bits/m^3")

# 2d. Egan & Lineweaver totals -> densities.  MANDATORY volume cross-check.
EL_S_GAS, EL_S_STARS, EL_S_NONCMB, EL_S_CMB = 7.1e81, 9.5e80, 1.0e86, 2.03e89
V_EL_implied = EL_S_CMB / s_cmb
R_EL_implied = (3.0 * V_EL_implied / (4 * np.pi)) ** (1 / 3.0)
V_EL_ph = 4.0 / 3.0 * np.pi * (14.0e3 * MPC) ** 3   # particle horizon, 14.0 Gpc
P()
P("  Egan & Lineweaver 2010 volume cross-check (PRE-REGISTERED as mandatory):")
P(f"    their S_CMB = {EL_S_CMB:.3e} k / (our first-principles s_CMB) "
  f"=> V = {V_EL_implied:.4e} m^3, R = {R_EL_implied/MPC/1e3:.2f} Gpc")
P(f"    a 14.0 Gpc particle horizon would give V = {V_EL_ph:.4e} m^3 "
  f"({dex(V_EL_ph/V_EL_implied):+.2f} dex different)")
P(f"    the Hubble volume is {V_HUB:.4e} m^3 "
  f"({dex(V_HUB/V_EL_implied):+.2f} dex from the implied one)")
P("    -> PREDECESSOR CORRECTION: DE_LEDGER_MODEL.md's K4 table compared E&L")
P("       totals (a horizon-volume count) against an energy computed in the")
P(f"       HUBBLE volume, crediting the model {dex(V_EL_implied/V_HUB):+.2f} dex "
  f"of bits it does not have.")
P("       This study works entirely in densities and is immune to that.")

N_el = {k: v / V_EL_implied / LN2 for k, v in
        dict(gas=EL_S_GAS, stars=EL_S_STARS, noncmb=EL_S_NONCMB).items()}
P(f"    E&L gas    -> {N_el['gas']:.4e} bits/m^3  "
  f"(Sackur-Tetrode @1e6 K gave {gas_ST[1e6]:.3e}: "
  f"agree to {N_el['gas']/gas_ST[1e6]:.2f}x)")
P(f"    E&L stars  -> {N_el['stars']:.4e} bits/m^3")
P(f"    E&L non-CMB photons (Gough's count) -> {N_el['noncmb']:.4e} bits/m^3")

# 2e. holographic bound on the Hubble horizon
N_holo = 4.0 * np.pi * R_HUB ** 2 / (4.0 * L_PL2 * LN2) / V_HUB
P(f"  holographic (Hubble horizon, A/4l_P^2): {N_holo:.4e} bits/m^3")
P()

# ---------------------------------------------------------------------------
# 3./4. THE PAIRINGS AND THE REQUIRED lambda
# ---------------------------------------------------------------------------
# (label, N bits/m^3, T K, legitimate?, note)
PAIRINGS = [
    ("stellar baryons, 1 bit each, at stellar interior T",
     n_star, 1e7, True, "N is a hard floor: one bit per baryon"),
    ("stellar baryons, 1 bit each, at stellar surface T",
     n_star, 5.8e3, True, ""),
    ("all baryons, 1 bit each, at warm IGM T",
     n_b, 1e6, True, "N is a hard floor"),
    ("stars, E&L entropy, at stellar interior T",
     N_el["stars"], 1e7, True, ""),
    ("IGM gas, Sackur-Tetrode, warm phase",
     gas_ST[1e6], 1e6, True, "first principles, no table"),
    ("IGM gas, Sackur-Tetrode, hot phase (WHIM)",
     gas_ST[1e7], 1e7, True, "first principles, no table"),
    ("IGM gas, E&L entropy, hot phase",
     N_el["gas"], 1e7, True, ""),
    ("starlight photons, at starlight T",
     N_el["noncmb"], 5e3, True, ""),
    ("dust re-emission photons, at dust T",
     N_el["noncmb"], 30.0, True, ""),
    ("CMB photons, at CMB T",
     N_cmb, T_CMB, True, "both first principles"),
    ("horizon d.o.f. (holographic), at de Sitter T",
     N_holo, T_DS, True, "SEE L4 -- this is an identity"),
    ("*** Gough: photon N at GAS T",
     N_el["noncmb"], 1e7, False, "ILLEGITIMATE: mismatched d.o.f."),
    ("*** holographic N at IGM T",
     N_holo, 1e6, False, "ILLEGITIMATE: mismatched d.o.f."),
]

P("--- 3./4. REQUIRED lambda FOR EACH (N,T) PAIRING " + "-" * 29)
P()
P("  stock  = N kB T ln2                 [J/m^3]  (the already-killed model)")
P("  f      = stock / rho_DE                      (stock shortfall factor)")
P("  lam_req/H0 = 3 rho_DE / stock = 3/f          (THE COLLAPSE TEST)")
P()
hdr = (f"  {'pairing':<52}{'N[bits/m3]':>11}{'T[K]':>10}"
       f"{'stock[J/m3]':>12}{'dex short':>10}{'lam/H0':>11}{'1/lam':>12}")
P(hdr)
P("  " + "-" * (len(hdr) - 2))
rows = []
for lab, N, T, legit, note in PAIRINGS:
    stock = N * KB * T * LN2
    f = stock / RHO_DE
    lam_req = 3.0 / f
    tau = 1.0 / (lam_req * H0)
    rows.append(dict(lab=lab, N=N, T=T, legit=legit, note=note,
                     stock=stock, f=f, lam=lam_req, tau=tau))
    if tau > 1e6 * YR:
        ts = f"{tau/YR/1e6:.3g} Myr"
    elif tau > YR:
        ts = f"{tau/YR:.3g} yr"
    else:
        ts = f"{tau:.3g} s"
    P(f"  {lab:<52}{N:>11.2e}{T:>10.3g}{stock:>12.2e}"
      f"{-dex(f):>10.1f}{lam_req:>11.3e}{ts:>12}")
P()
P("  NOTE the two *** rows are the ILLEGITIMATE controls (N from one system,")
P("  T from another).  They are excluded from the verdict by pre-registration.")
P()

legit_rows = [r for r in rows if r["legit"]]
lam_vals = np.array([r["lam"] for r in legit_rows])
matter_rows = [r for r in legit_rows if "horizon" not in r["lab"]]
lam_matter = np.array([r["lam"] for r in matter_rows])
P(f"  legitimate pairings: required lambda/H0 spans "
  f"{lam_vals.min():.3g} .. {lam_vals.max():.3g}")
P(f"  excluding the horizon/de Sitter row: "
  f"{lam_matter.min():.3g} .. {lam_matter.max():.3g}  "
  f"({dex(lam_matter.min()):.1f} .. {dex(lam_matter.max()):.1f} dex)")
holo = [r for r in legit_rows if "horizon" in r["lab"]][0]
P(f"  the horizon/de Sitter row alone requires lambda/H0 = {holo['lam']:.4f}")
P(f"    -- and 3*Omega_L = {3*OM_L:.4f}.  It is EXACTLY that, i.e. the pairing")
P("       returns stock = u_crit identically (Gibbons-Hawking), see L4.")
P()
P("  MAINTAINED-FRACTION NOTE (pre-registered): the flow picture may count only")
P("  ACTIVELY MAINTAINED bits.  N_maint <= N_total always, so every row's")
P("  lambda is a LOWER BOUND; a maintained fraction phi multiplies it by 1/phi.")
P("  The reformulation's own discipline makes its arithmetic WORSE.")
P()
P("  THE INVERSE QUESTION, which is the most legible form of the failure:")
P("  hold lambda at the shape fit's value and ask what N_maint is REQUIRED.")
P(f"     N_req = 3 rho_DE / (lambda kB T ln2),  lambda = {LAM_SHAPE} H0")
P(f"  {'T [K]':>12}{'N_req [bits/m3]':>18}{'per baryon':>14}"
  f"{'vs holo bound':>15}{'vs actual N':>14}")
lam_si_shape = LAM_SHAPE * H0
for Treq, Nact in ((T_CMB, N_cmb), (30.0, N_el["noncmb"]), (5e3, N_el["noncmb"]),
                   (1e6, gas_ST[1e6]), (1e7, gas_ST[1e7])):
    N_req = 3.0 * RHO_DE / (lam_si_shape * KB * Treq * LN2)
    P(f"  {Treq:>12.4g}{N_req:>18.3e}{N_req/n_b:>14.2e}"
      f"{N_req/N_holo:>15.2e}{N_req/Nact:>14.2e}")
P("  Read the last two columns: the required bit density is below the")
P("  holographic bound (so holography does not forbid it) but 20-24 orders of")
P("  magnitude above the bits any of these systems actually carries.  In the")
P("  most concrete terms: the IGM would have to be error-correcting ~1e25")
P("  bits per baryon, continuously, at 1e7 K.")
P()

# ---------------------------------------------------------------------------
# L1 -- lambda consistency with the shape fit
# ---------------------------------------------------------------------------
P("--- L1. lambda CONSISTENCY WITH THE SHAPE FIT " + "-" * 32)
P()
P("  In Core/Maintenance.lean, `rent_holds` says an entry is held steady when")
P("  the payment equals the decay.  In steady state the MAINTENANCE RATE IS")
P("  THE DECAY RATE: one symbol, one equation, two measurements.")
P(f"  shape leg (DESI DR2 BAO+CMB-lite, DE_LEDGER_MODEL.md S4): "
  f"lambda = {LAM_SHAPE} H0, 68% [{LAM_SHAPE_LO}, {LAM_SHAPE_HI}]")
P(f"  magnitude leg (this study, legitimate matter/radiation pairings): "
  f"lambda = {lam_matter.min():.2e} .. {lam_matter.max():.2e} H0")
r_lo, r_hi = lam_matter.min() / LAM_SHAPE, lam_matter.max() / LAM_SHAPE
P(f"  RATIO lambda_mag / lambda_shape = {r_lo:.2e} .. {r_hi:.2e}"
  f"   ({dex(r_lo):.1f} .. {dex(r_hi):.1f} dex)")
P(f"  pre-registered criterion: factor 10.  "
  f"{'PASS' if r_lo < 10 else 'KILL -- outcome (e) FIRES'}")
P()

# ---------------------------------------------------------------------------
# L2 -- free-energy budget
# ---------------------------------------------------------------------------
P("--- L2. FREE-ENERGY BUDGET " + "-" * 51)
P()
E_per_hubble = P_REQ * T_HUB
P(f"  required power density        P = 3 H rho_DE = {P_REQ:.4e} W/m^3")
P(f"  integrated over one Hubble time: P/H = 3 rho_DE = {E_per_hubble:.4e} J/m^3")
P(f"                                       = {E_per_hubble/U_CRIT:.3f} x u_crit")
P("    (this is parameter-free: independent of N, T and lambda)")
P()
u_m = OM_M * U_CRIT
u_b = OM_B * U_CRIT
u_star = OM_STAR * U_CRIT
P(f"  ALL matter (dark included)  Om_m u_crit = {u_m:.4e} J/m^3  "
  f"-> short by {E_per_hubble/u_m:.2f}x")
P(f"  all baryons                 Om_b u_crit = {u_b:.4e} J/m^3  "
  f"-> short by {E_per_hubble/u_b:.2f}x")
P(f"  all stellar mass            Om_* u_crit = {u_star:.4e} J/m^3  "
  f"-> short by {E_per_hubble/u_star:.2f}x")
P("  i.e. TOTAL ANNIHILATION of every particle of matter in the universe,")
P("  dark matter included, inside one Hubble time, still does not pay the bill.")
P()
psi0 = dl.psi_sfh(0.0)                       # Msun/yr/Mpc^3, MD14 eq.15
mdot = psi0 * MSUN / YR / MPC ** 3           # kg/s/m^3
P_star_cap = mdot * 0.007 * C ** 2           # every gram burned H->He instantly
P_star_full = mdot * C ** 2                  # total rest-mass conversion
P(f"  MD14 eq.15 psi(0) = {psi0:.5f} Msun/yr/Mpc^3 = {mdot:.4e} kg/s/m^3")
P(f"  HARD upper bound on stellar power (0.7% H->He, instantaneous): "
  f"{P_star_cap:.4e} W/m^3")
P(f"     -> short of P by {P_REQ/P_star_cap:.3e}x  "
  f"({dex(P_REQ/P_star_cap):.2f} dex)")
P(f"  even 100% rest-mass conversion at the star-formation rate: "
  f"{P_star_full:.4e} W/m^3")
P(f"     -> short of P by {P_REQ/P_star_full:.3e}x  "
  f"({dex(P_REQ/P_star_full):.2f} dex)")
P()

# ---------------------------------------------------------------------------
# L3 -- the waste heat
# ---------------------------------------------------------------------------
P("--- L3. THE WASTE HEAT: WHERE DOES THE ERASURE HEAT GO? " + "-" * 22)
P()
P("  Landauer heat is real heat.  Over one Hubble time the flow model deposits")
P(f"  {E_per_hubble:.3e} J/m^3 into whichever reservoir it names.")
P()
dU_over_U = E_per_hubble / u_cmb
y_dist = dU_over_U / 4.0
FIRAS_Y, FIRAS_MU = 1.5e-5, 9.0e-5
P("  (a) CMB reservoir:")
P(f"      dU/U = {E_per_hubble:.3e}/{u_cmb:.3e} = {dU_over_U:.3e}")
P(f"      Compton y ~ dU/(4U) = {y_dist:.3e}   vs COBE/FIRAS |y| < {FIRAS_Y:.1e}")
P(f"      VIOLATION by {y_dist/FIRAS_Y:.3e}x  ({dex(y_dist/FIRAS_Y):.1f} dex)")
P("      -> the CMB would not be a blackbody.  It is, to 1 part in 1e5.")
P()
for Tg, nam in ((1e6, "warm IGM"), (1e7, "hot IGM/WHIM")):
    u_igm = 1.5 * n_b * KB * Tg
    P(f"  (b) {nam} reservoir @ {Tg:.0e} K: thermal u = {u_igm:.3e} J/m^3, "
      f"deposit/u = {E_per_hubble/u_igm:.3e}x")
P("      -> the IGM would be hotter than observed by ~8 orders of magnitude.")
P()
S_dump = E_per_hubble / T_DS / KB
S_horizon = N_holo * LN2
P("  (c) de Sitter horizon reservoir:")
P(f"      entropy dumped in a Hubble time = (3 rho_DE)/T_dS/kB = {S_dump:.4e} k/m^3")
P(f"      horizon entropy density A/(4 l_P^2 V)               = {S_horizon:.4e} k/m^3")
P(f"      ratio = {S_dump/S_horizon:.4f}  (= 3 Omega_L = {3*OM_L:.4f}) -- ORDER UNITY,")
P("      but order unity BY THE SAME IDENTITY, not by a maintenance calculation.")
P()

# ---------------------------------------------------------------------------
# L4 -- rate bounds
# ---------------------------------------------------------------------------
P("--- L4. RATE BOUNDS (Margolus-Levitin) " + "-" * 39)
P()
P("  ML: a system of energy E performs at most nu = 2E/(pi hbar) orthogonalising")
P("  operations per second.  Required rate density = N * lambda  [ops/s/m^3].")
P()
P(f"  {'pairing':<52}{'N*lam[/s/m3]':>14}{'ML bound':>13}{'req/ML':>11}")
P("  " + "-" * 88)
for r in rows:
    if not r["legit"]:
        continue
    lam_si = r["lam"] * H0
    req = r["N"] * lam_si
    if "horizon" in r["lab"]:
        E_avail = U_CRIT                      # the whole energy budget
    elif "CMB" in r["lab"]:
        E_avail = u_cmb
    elif "photons" in r["lab"]:
        E_avail = 4.2e-15                     # EBL, ~100 nW/m^2/sr [MEMORY]
    elif "stellar baryons" in r["lab"] or "stars" in r["lab"]:
        E_avail = u_star
    else:
        E_avail = u_b
    ml = 2.0 * E_avail / (np.pi * HBAR)
    P(f"  {r['lab']:<52}{req:>14.2e}{ml:>13.2e}{req/ml:>11.2e}")
P()
holo_ratio = (N_holo * holo["lam"] * H0) / (2.0 * U_CRIT / (np.pi * HBAR))
P(f"  The horizon/de Sitter row sits at req/ML = {holo_ratio:.4f}.")
P("  PRE-REGISTERED PREDICTION (prereg L4): this ratio is a PURE NUMBER built")
P("  from 2pi (Hawking T), 4 (Bekenstein), ln2 (Landauer) and pi (ML).")
P("  Closed form, derived (not fitted): with N_holo = 3H/(4 c l_P^2 ln2),")
P("  lambda = 3 Omega_L H and ML = 3H^2/(4 pi^2 l_P^2 c),")
P(f"     req/ML = 3 Omega_L pi^2 / ln2 = {3*OM_L*np.pi**2/LN2:.4f}"
  f"   <- matches to {abs(holo_ratio - 3*OM_L*np.pi**2/LN2):.2e}")
P("  Every dimensionful constant -- H0, G, hbar, c -- has cancelled.  The only")
P("  survivor is the O(1) density fraction Omega_L.  As pre-registered, that is")
P("  evidence the pairing is a THERMODYNAMIC IDENTITY with no maintenance")
P("  content, NOT evidence the model works.")
P()
P("  Proof that the pairing is an identity (analytic, not numerical):")
P("     T_dS * S_horizon / V = [hbar H/(2 pi kB)] * [kB A/(4 l_P^2)] / V")
P("                          = hbar H (3/R) /(8 pi l_P^2)   [A/V = 3/R, R=c/H]")
P("                          = 3 H^2 c^2/(8 pi G) = rho_crit c^2   EXACTLY.")
stock_holo = holo["stock"]
P(f"     numerically: stock = {stock_holo:.6e} J/m^3 vs u_crit = {U_CRIT:.6e}")
P(f"     ratio = {stock_holo/U_CRIT:.10f}")
P()

# ---------------------------------------------------------------------------
# L5 -- w(z) UNDER THE FLOW READING
# ---------------------------------------------------------------------------
P("--- L5. w(z) UNDER THE FLOW READING " + "-" * 42)
P()
P("  Flow model: rho_DE = P/(3H) with P ~ n(t), so rho_flow ~ n(t)/H(t),")
P("  against the stock model's rho_stock ~ n(t).  Extra factor 1/H.")
P("  Since w = -1 - (1/3) dln rho/dln a and dlnH/dlna < 0, the flow reading is")
P("  MORE PHANTOM than the stock reading at every z -- predicted in the prereg.")
P()

lna, a_g, z_g = dl.lna, dl.a_g, dl.z_g
OM_R = dl.OM_R


def ledger_stock(lam, om_m=OM_M, z_start=20.0, n_iter=200, tol=1e-12):
    """dn/dtau = psi - lam n, integrated with an EXACT exponential step so it
       stays stable for lam >> 1 (the published solver overflows there)."""
    om_rec0 = 1.0 - om_m - OM_R
    psi = np.where(z_g > z_start, 0.0, dl.psi_sfh(z_g))
    rho_hat = np.ones_like(a_g)
    n = np.zeros_like(a_g)
    for _ in range(n_iter):
        E = np.sqrt(OM_R * a_g ** -4 + om_m * a_g ** -3 + om_rec0 * rho_hat)
        tau = dl.cumtrapz0(1.0 / E, lna)
        d = np.diff(tau)
        ex = np.exp(-lam * d)
        pm = 0.5 * (psi[1:] + psi[:-1])
        n = np.zeros_like(a_g)
        for i in range(len(d)):
            n[i + 1] = n[i] * ex[i] + (pm[i] / lam) * (1.0 - ex[i])
        rho_new = np.maximum(n / n[-1], 1e-300)
        m = a_g > 1e-3
        if np.max(np.abs(np.log(rho_new[m] / rho_hat[m]))) < tol:
            rho_hat = rho_new
            break
        rho_hat = rho_new
    E = np.sqrt(OM_R * a_g ** -4 + om_m * a_g ** -3 + om_rec0 * rho_hat)
    return dict(a=a_g, z=z_g, E=E, rho_hat=rho_hat, om_m=om_m,
                tau=dl.cumtrapz0(1.0 / E, lna), n=n,
                w=-1.0 - np.gradient(np.log(rho_hat), lna) / 3.0)


def ledger_flow(lam, om_m=OM_M, z_start=20.0, n_iter=200, tol=1e-12):
    """FLOW reading: rho ~ n/E."""
    om_rec0 = 1.0 - om_m - OM_R
    psi = np.where(z_g > z_start, 0.0, dl.psi_sfh(z_g))
    rho_hat = np.ones_like(a_g)
    for _ in range(n_iter):
        E = np.sqrt(OM_R * a_g ** -4 + om_m * a_g ** -3 + om_rec0 * rho_hat)
        tau = dl.cumtrapz0(1.0 / E, lna)
        d = np.diff(tau)
        ex = np.exp(-lam * d)
        pm = 0.5 * (psi[1:] + psi[:-1])
        n = np.zeros_like(a_g)
        for i in range(len(d)):
            n[i + 1] = n[i] * ex[i] + (pm[i] / lam) * (1.0 - ex[i])
        r = n / E
        rho_new = np.maximum(r / r[-1], 1e-300)
        m = a_g > 1e-3
        if np.max(np.abs(np.log(rho_new[m] / rho_hat[m]))) < tol:
            rho_hat = rho_new
            break
        rho_hat = rho_new
    E = np.sqrt(OM_R * a_g ** -4 + om_m * a_g ** -3 + om_rec0 * rho_hat)
    return dict(a=a_g, z=z_g, E=E, rho_hat=rho_hat, om_m=om_m,
                tau=dl.cumtrapz0(1.0 / E, lna),
                w=-1.0 - np.gradient(np.log(rho_hat), lna) / 3.0)


# GATE: reproduce the published variant-A numbers with the new stable solver
P("  GATE (machinery): the stable exponential-step solver must reproduce")
P("  DE_LEDGER_MODEL.md Table S2 (variant A) which used a different scheme.")
P(f"  {'lam/H0':>8}{'published w(0)':>16}{'this solver':>14}{'diff':>10}")
PUB = {0.0: -1.088, 1.0: -0.821, 2.0: -0.587}
gate_ok = True
for lam, wpub in PUB.items():
    s = ledger_stock(max(lam, 1e-8))
    wnow = float(np.interp(0.0, z_g[::-1], s["w"][::-1]))
    d = abs(wnow - wpub)
    gate_ok &= d < 0.005
    P(f"  {lam:>8.2f}{wpub:>16.3f}{wnow:>14.3f}{d:>10.4f}")
P(f"  GATE: {'PASS' if gate_ok else 'FAIL'} (bar: |diff| < 0.005 on all three)")
P()

P("  w(z): STOCK vs FLOW at the shape-fit lambda")
P(f"  {'z':>6}{'stock lam=1.67':>16}{'flow lam=1.67':>16}"
  f"{'flow lam=1e4':>15}{'flow lam=1e6':>15}")
s167, f167 = ledger_stock(LAM_SHAPE), ledger_flow(LAM_SHAPE)
f1e4, f1e6 = ledger_flow(1e4), ledger_flow(1e6)
for zq in (0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0):
    P(f"  {zq:>6.2f}{dl.at_z(s167,'w',zq):>16.3f}{dl.at_z(f167,'w',zq):>16.3f}"
      f"{dl.at_z(f1e4,'w',zq):>15.3f}{dl.at_z(f1e6,'w',zq):>15.3f}")
P()

# the acceleration test at the lambda the magnitude leg requires
P("  ACCELERATION TEST at the lambda the MAGNITUDE leg requires (lam >> H):")
P("    q0 = 0.5*(Om_m + (1+3w0) Om_DE);  the universe accelerates iff q0 < 0,")
P("    i.e. iff w0 < -1/(3 Om_DE) = "
  f"{-1.0/(3*OM_L):.4f}")
for nm, sol in (("stock, lam=1.67 (shape fit)", s167),
                ("flow,  lam=1.67 (shape fit)", f167),
                ("flow,  lam=1e4", f1e4),
                ("flow,  lam=1e6", f1e6)):
    w0 = dl.at_z(sol, "w", 0.0)
    om_rec0 = 1.0 - sol["om_m"] - OM_R
    q0 = 0.5 * (sol["om_m"] + (1.0 + 3.0 * w0) * om_rec0)
    P(f"    {nm:<30} w(0) = {w0:>7.3f}   q0 = {q0:>7.3f}   "
      f"{'ACCELERATES' if q0 < 0 else '*** DOES NOT ACCELERATE ***'}")
P()

# CPL projections and the DESI comparison
P("  CPL projection and DESI DR2 chi^2 (reusing DE_LEDGER_MODEL's likelihood)")
P(f"  {'model':<28}{'w0':>9}{'wa':>9}{'chi2':>9}{'Om_m':>8}{'dchi2 vs LCDM':>15}")
from scipy.optimize import minimize_scalar                      # noqa: E402

chi2_lcdm, _ = dl.chi2_profiled(dl.lcdm_sol(0.2954))


def best_om(fn, lam):
    r = minimize_scalar(lambda om: dl.chi2_profiled(fn(lam, om_m=om))[0],
                        bounds=(0.20, 0.45), method="bounded",
                        options=dict(xatol=1e-4))
    return float(r.x), float(r.fun)


P(f"  {'LCDM (Om_m=0.2954)':<28}{-1.0:>9.3f}{0.0:>9.3f}"
  f"{chi2_lcdm:>9.3f}{0.2954:>8.4f}{0.0:>15.3f}")
flow_prof = []
for nm, fn, lam in (("stock ledger, lam=1.67", ledger_stock, LAM_SHAPE),
                    ("FLOW ledger, lam=1.67", ledger_flow, LAM_SHAPE),
                    ("FLOW ledger, lam=1e4", ledger_flow, 1e4),
                    ("FLOW ledger, lam=1e6", ledger_flow, 1e6)):
    om, c2 = best_om(fn, lam)
    s = fn(lam, om_m=om)
    w0, wa = dl.fit_cpl(s)
    P(f"  {nm:<28}{w0:>9.3f}{wa:>9.3f}{c2:>9.3f}{om:>8.4f}{c2-chi2_lcdm:>15.3f}")
P()
P("  FLOW ledger: profile over lambda (Om_m re-minimised at each point)")
P(f"  {'lam/H0':>10}{'Om_m':>8}{'chi2':>10}{'dchi2 vs LCDM':>15}{'w(0)':>9}")
best = (1e9, None)
for lam in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0, 10.0, 1e2, 1e4, 1e6):
    om, c2 = best_om(ledger_flow, lam)
    s = ledger_flow(lam, om_m=om)
    w0z = dl.at_z(s, "w", 0.0)
    flow_prof.append((lam, om, c2, w0z))
    if c2 < best[0]:
        best = (c2, lam)
    P(f"  {lam:>10.4g}{om:>8.4f}{c2:>10.3f}{c2-chi2_lcdm:>15.3f}{w0z:>9.3f}")
P(f"  coarse best FLOW lambda: {best[1]:.4g} H0 (chi2 = {best[0]:.3f})")
fine = []
for lam in np.arange(3.0, 6.01, 0.25):
    om, c2 = best_om(ledger_flow, float(lam))
    fine.append((float(lam), om, c2))
lam_b, om_b, c2_b = min(fine, key=lambda t: t[2])
in1 = [t[0] for t in fine if t[2] <= c2_b + 1.0]
in4 = [t[0] for t in fine if t[2] <= c2_b + 4.0]
s_best = ledger_flow(lam_b, om_m=om_b)
w0b, wab = dl.fit_cpl(s_best)
P(f"  fine scan: FLOW best lambda = {lam_b:.2f} H0, Om_m = {om_b:.4f}, "
  f"chi2 = {c2_b:.3f} (dchi2 vs LCDM = {c2_b-chi2_lcdm:+.3f})")
P(f"     dchi2<=1 interval [{min(in1):.2f}, {max(in1):.2f}] H0 ; "
  f"dchi2<=4 [{min(in4):.2f}, {max(in4):.2f}] H0")
P(f"     CPL projection (w0, wa) = ({w0b:.3f}, {wab:.3f})")
P()
P("  SIDE-BY-SIDE, the two readings on the SAME data (DESI DR2 BAO + CMB-lite):")
P(f"    STOCK ledger best: dchi2 vs LCDM = -2.13  (DE_LEDGER_MODEL.md S4)")
P(f"    FLOW  ledger best: dchi2 vs LCDM = {c2_b-chi2_lcdm:+.2f}")
P("    -> the flow reading is WORSE on the shape too: the extra 1/H makes the")
P("       model more phantom, exactly as pre-registered in L5, and it loses")
P("       most of the predecessor's (already weak) 1.5-sigma preference.")
P()
P("  FLOW best-fit vs DESI DR2 published CPL point estimates:")
DESI = [("DESI+CMB", -0.42, 0.21, -1.75, 0.58),
        ("DESI+CMB+Pantheon+", -0.838, 0.055, -0.62, 0.205),
        ("DESI+CMB+Union3", -0.667, 0.088, -1.09, 0.29),
        ("DESI+CMB+DESY5", -0.752, 0.057, -0.86, 0.215)]
P(f"  {'combination':<24}{'w0':>9}{'wa':>9}{'|dw0|/sig':>11}{'|dwa|/sig':>11}")
for nm, w0d, sw0, wad, swa in DESI:
    P(f"  {nm:<24}{w0d:>9.3f}{wad:>9.3f}"
      f"{abs(w0b-w0d)/sw0:>11.2f}{abs(wab-wad)/swa:>11.2f}")
P()
P("  MEMORY-FLAGGED INPUTS -- do they change the verdict?  (prereg S8 requires")
P("  this check for every number marked 'from memory'.)")
P(f"    Omega_* = {OM_STAR} (+-50%): enters 2 of 11 legitimate rows; lambda ~ 1/N")
P(f"      so the shift is [{dex(1/1.5):+.2f}, {dex(1/0.5):+.2f}] dex against a "
  f"4.2-12.1 dex failure.  NO EFFECT.")
P(f"    FIRAS |y| < {FIRAS_Y:.1e}: the violation is "
  f"{dex(y_dist/FIRAS_Y):.1f} dex.  Even a 100x")
P("      misremembering of the FIRAS limit leaves a 6.8 dex violation.  NO EFFECT.")
P("    EBL 4.2e-15 J/m^3: used only as the ML denominator for photon rows,")
P("      which pass ML by >25 dex either way.  NO EFFECT.")
P("    -> no verdict in this study depends on a memory-flagged number.")
P()

# ---------------------------------------------------------------------------
# VERDICT
# ---------------------------------------------------------------------------
P("=" * 78)
P("VERDICT AGAINST THE PRE-REGISTERED OUTCOMES")
P("=" * 78)
P(f"  (a) SURVIVES ........................ NO")
P(f"  (b) hard rate kill (ML) ............. NO -- matter pairings pass ML by")
P(f"      ~30 dex; the rate is not the problem.")
P(f"  (c) same failure mode as stock ...... FIRES -- the only pairing reaching")
P(f"      the target with lambda ~ H is the horizon/de Sitter one, which is a")
P(f"      thermodynamic identity (stock/u_crit = {stock_holo/U_CRIT:.6f}), and the")
P(f"      published-style rescue needs mismatched d.o.f.")
P(f"  (d) empty reformulation ............. FIRES on that same row: required")
P(f"      lambda/H0 = {holo['lam']:.3f} = 3 Omega_L exactly.")
P(f"  (e) internal inconsistency (L1) ..... FIRES -- lambda_mag/lambda_shape =")
P(f"      {r_lo:.1e}..{r_hi:.1e} ({dex(r_lo):.1f}-{dex(r_hi):.1f} dex), bar was 10x.")
P(f"  (f) budget / waste heat ............. FIRES, parameter-free --")
P(f"      P/H = {E_per_hubble/U_CRIT:.2f} u_crit > all matter by "
  f"{E_per_hubble/u_m:.1f}x; stellar power short by {dex(P_REQ/P_star_cap):.1f} dex;")
P(f"      CMB y-distortion {y_dist:.1e} vs FIRAS {FIRAS_Y:.1e} "
  f"({dex(y_dist/FIRAS_Y):.1f} dex).")
P()

with open(os.path.join(HERE, "flow_pricing_output.txt"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")
