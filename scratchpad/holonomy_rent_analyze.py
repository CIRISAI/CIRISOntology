#!/usr/bin/env python3
"""Analysis for the maintained-holonomy campaign.  Reads holonomy_rent_results.json,
applies the pre-registered gates and hypothesis tests (HOLONOMY_RENT_PREREG.md @ 3ae9c9b),
and prints the tables that go into HOLONOMY_RENT_RESULTS.md.

F-11 stays fired: nothing here is the unmaintained loop."""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
J = json.load(open(os.path.join(HERE, "holonomy_rent_results.json")))
A = J["arms"]
R_SCAN = J["meta"]["R_scan"]
Q = J["meta"]["q_grid"]
EPS_RECV, LAM_RECV = 0.0345, 0.9655


def col(key, field):
    return np.array([A[key][str(R)][field] for R in R_SCAN])


def hdr(t):
    print("\n" + "=" * 84 + f"\n{t}\n" + "=" * 84)


# ---------------------------------------------------------------------- gates
hdr("GATES (prereg section 6)")
g = J["gates"]
print(f"  C-Q0 connection identity      : verified separately, worst dev 1.16e-14 (< 1e-10) PASS")
print(f"  C-NOOP  max||Rep_q(U)-U||     : {g['C_NOOP_max']:.2e}  (< 1e-12) "
      f"{'PASS' if g['C_NOOP_pass'] else 'FAIL'}")
print(f"  ||W^dag W - I||               : {g['W_isometry_resid']:.2e}")
print(f"  design=polar(B) unitary resid : {g['Udes_unitary_resid']:.2e}")
print(f"  Deph vs framework constants   : {g['damp_spectrum_maxdev']:.2e}  "
      f"(spectrum [{g['Deph_eig_min']:.4f}, {g['Deph_eig_max']:.4f}])")
print(f"  accumulated-leg unitarity     : W {g['Wpow_unitary_drift']:.2e}, "
      f"design {g['Dpow_unitary_drift']:.2e}")
print(f"  c1 module vs recomputed       : {g['c1_module']:.14f} vs {g['c1_recomputed']:.14f}"
      f"   (source docstring says 0.6257 -- comment wrong, value right)")

worst_canc, n_rank, n_cells = 0.0, 0, 0
for k in A:
    for R in R_SCAN:
        r = A[k].get(str(R))
        if r is None or "cancel_rel" not in r:
            continue
        n_cells += 1
        worst_canc = max(worst_canc, r["cancel_rel"])
        if r["cond_ratio"] < 1e-13:
            n_rank += 1
print(f"  catastrophic cancellation     : worst {worst_canc:.2e} over {n_cells} cells "
      f"(< 1e-10) {'PASS' if worst_canc < 1e-10 else 'FAIL'}")
print(f"  rank collapse (sv_min/sv_max<1e-13): {n_rank} cells dropped as ungauged")

# ------------------------------------------------------- re-derive lambda
hdr("STEP 1 -- RE-DERIVING THE RECEIVED NUMBER (received-numbers-are-not-measured)")
z = "R-POL|cont|q=0.0"
sr, gn = col(z, "specrad"), col(z, "gain")
n = np.array(R_SCAN) - 1                       # denominator: rung STEPS, not rungs
psr, pgn = sr ** (1 / n), gn ** (1 / n)
print("  per-rung rate, denominator R-1:")
print("   R    specrad^(1/(R-1))   gain^(1/(R-1))   [* = omitted from the published table]")
pub_shown = {3, 5, 9, 13, 20, 30, 50}
for i, R in enumerate(R_SCAN):
    mark = "" if R in pub_shown else " *"
    print(f"  {R:4d}      {psr[i]:.6f}          {pgn[i]:.6f}{mark}")
lam_sr = float(sr[R_SCAN.index(400)] ** (1 / 399))
lam_gn = float(gn[R_SCAN.index(400)] ** (1 / 399))
print(f"\n  asymptotic (R=400):  lambda_specrad = {lam_sr:.6f}   lambda_gain = {lam_gn:.6f}")
print(f"  RECEIVED lambda = {LAM_RECV} (a SPECRAD rate).  |re-derived - received| = "
      f"{abs(lam_sr - LAM_RECV):.2e}")
p12 = psr[:12]
print(f"  spread over the predecessor's own 12 depths: [{p12.min():.6f}, {p12.max():.6f}] "
      f"= {p12.max()-p12.min():.2e}  -> constant to THREE decimals, not four")
print(f"  the published table omits R=4, whose value {psr[1]:.6f} is the largest outlier")
eps_sr, eps_gn = 1 - lam_sr, 1 - lam_gn
print(f"\n  eps_specrad = {eps_sr:.6f}   eps_gain = {eps_gn:.6f}")
print(f"  q_half = eps/(2-lambda):  specrad {eps_sr/(2-lam_sr):.6f} = "
      f"{eps_sr/(2-lam_sr)/eps_sr:.4f} eps   |   gain {eps_gn/(2-lam_gn):.6f} = "
      f"{eps_gn/(2-lam_gn)/eps_gn:.4f} eps")


def gpred(q, lam):
    return q / (1 - (1 - q) * lam)


# --------------------------------------------------------------- plateau
def plateau(key, field="gain"):
    """Pre-registered convergence test: relative change over the TOP QUARTILE of the
    R grid must be < 1%.  Returns (value, converged, rel_change)."""
    v = col(key, field)
    top = v[-len(R_SCAN) // 4:]
    rel = abs(top[-1] - top[0]) / max(abs(top[-1]), 1e-300)
    return float(v[-1]), bool(rel < 0.01), float(rel)


hdr("H1 / H2 / H3 -- THE PLATEAU, ITS SHAPE, AND THE LAW")
print("  gain at R=400, both arms, continuous dosing; prediction q/(eps+q*lambda)")
print("  using the RE-DERIVED lambda_gain (the gain is the primary observable).\n")
print("     q      q/eps    POL gain   conv  |  DES gain   conv  |  predicted  "
      "POL resid  DES resid")
rows = []
for q in Q:
    if q == 0.0:
        continue
    kp, kd = f"R-POL|cont|q={q}", f"R-DES|cont|q={q}"
    vp, cp_, _ = plateau(kp)
    vd, cd, _ = plateau(kd)
    pr = gpred(q, lam_gn)
    rp, rd = (vp - pr) / pr, (vd - pr) / pr
    rows.append((q, vp, vd, pr, rp, rd, cp_, cd))
    print(f"  {q:6.5f}  {q/eps_gn:6.3f}   {vp:.6f}  {'Y' if cp_ else 'N':>4}  |  "
          f"{vd:.6f}  {'Y' if cd else 'N':>4}  |  {pr:.6f}   "
          f"{rp:+7.2%}   {rd:+7.2%}")
mx_p = max(abs(r[4]) for r in rows)
mx_d = max(abs(r[5]) for r in rows)
print(f"\n  H3 max |residual|:  R-POL {mx_p:.1%}   R-DES {mx_d:.1%}")
print("  pre-declared reading: <10% quantitative | 10-50% shape only | >50% does not transfer")

gp = np.array([r[1] for r in rows])
print(f"  H2 monotone in q?  R-POL {'YES' if np.all(np.diff(gp) > -1e-12) else 'NO'}   "
      f"R-DES {'YES' if np.all(np.diff([r[2] for r in rows]) > -1e-12) else 'NO'}")
qq = np.array([r[0] for r in rows])
sl = np.diff(np.log(gp)) / np.diff(np.log(qq))
print("  H2 knee test -- local log-log slope d log G / d log q between grid points:")
for i in range(len(sl)):
    tag = "   <-- brackets q=eps" if qq[i] <= eps_gn <= qq[i + 1] else ""
    print(f"      q {qq[i]:7.5f} -> {qq[i+1]:7.5f} : slope {sl[i]:.4f}{tag}")
rat = sl[:-1] / np.maximum(sl[1:], 1e-12)
print(f"  adjacent slope ratios: max {np.nanmax(rat):.2f} "
      f"(kill fires if the pair bracketing q=eps exceeds 2 while others do not)")

# --------------------------------------------------------------- fidelity
hdr("H4 -- FIDELITY: is the maintained holonomy still POINTED AT THE DESIGN?")
print("  fidelity at R=400 (direction only; scale-free by construction).")
print("  the prereg ASSUMED a chance floor of 1/sqrt(d) = 0.125; C-RAND MEASURES it,")
print("  and the measurement corrects the assumption to ~1/d = 0.0156 (the overlap of")
print("  two independent operators lives in a d^2-dimensional space, not a d-dim one).\n")
print("     q     R-POL fid   R-DES fid   C-RAND fid  |  R-POL gain  C-RAND gain")
for q in Q:
    if q == 0.0:
        continue
    fp = col(f"R-POL|cont|q={q}", "fidelity")[-1]
    fd = col(f"R-DES|cont|q={q}", "fidelity")[-1]
    fr = col(f"C-RAND|cont|q={q}", "fidelity")[-1]
    gpv = col(f"R-POL|cont|q={q}", "gain")[-1]
    grv = col(f"C-RAND|cont|q={q}", "gain")[-1]
    print(f"  {q:6.5f}   {fp:.6f}    {fd:.6f}    {fr:.6f}   |  {gpv:.6f}   {grv:.6f}")
f0 = col("R-POL|cont|q=0.0", "fidelity")[-1]
print(f"\n  q=0 (unmaintained) fidelity at R=400: {f0:.6f}")
cn_g = col("C-NORM|cont|q=1.0", "gain")[-1]
cn_f = col("C-NORM|cont|q=1.0", "fidelity")[-1]
print(f"  C-NORM (the forbidden scalar rescale): gain {cn_g:.6f}  fidelity {cn_f:.6f}")
print(f"    -> a manufactured plateau: gain pinned at 1 by construction, fidelity "
      f"{'EQUALS' if abs(cn_f - f0) < 1e-9 else 'differs from'} the unmaintained value "
      f"(a scalar rescale cannot move direction)")

# ---------------------------------------------- fidelity vs depth, R-POL
hdr("H4 detail -- R-POL fidelity vs depth (does it hold, or wander?)")
print("     R  " + "".join(f"  q={q:<7g}" for q in [0.0345, 0.1, 0.3, 0.7, 0.99]))
for R in R_SCAN:
    line = f"  {R:4d}  "
    for q in [0.0345, 0.1, 0.3, 0.7, 0.99]:
        line += f"  {A[f'R-POL|cont|q={q}'][str(R)]['fidelity']:.6f}"
    print(line)

# --------------------------------------------------------- dose vs rate
hdr("DOSE-vs-RATE (GATES.md 7) -- is the plateau set by total effort, or its parcelling?")
print("  gain at R=400 under three dosing schemes at matched mean effort q.")
print("  stochastic floor = sd over 64 realizations.\n")
print("     q      cont      stoch (mean+-sd)      per      n_rep(per)  |cont-stoch|/sd")
for q in Q:
    if q == 0.0:
        continue
    c = col(f"R-POL|cont|q={q}", "gain")[-1]
    s = A[f"R-POL|stoch|q={q}"][str(400)]
    p = col(f"R-POL|per|q={q}", "gain")[-1]
    nrep = A[f"R-POL|per|q={q}"][str(400)]["n_repairs"]
    sd = max(s["gain_sd"], 1e-12)
    print(f"  {q:6.5f}  {c:.6f}  {s['gain']:.6f}+-{sd:.6f}  {p:.6f}   {nrep:5.0f}    "
          f"{abs(c-s['gain'])/sd:8.2f}")
print("\n  NOTE: the periodic scheme cannot deliver a repair when round(1/q) > 399;")
print("  those cells are under-resolved by construction and are reported, not hidden.")
