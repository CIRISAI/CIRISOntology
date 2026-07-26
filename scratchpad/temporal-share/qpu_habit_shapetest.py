#!/usr/bin/env python3
"""Where exactly did K-SHAPE fail?  A model-free product test.

POST-HOC DIAGNOSIS, labelled as such.  The pre-registered kill fired: the
3-body decay is not a single exponential at the rate the in-job T1 audit fixes
(chi2 153 against a staked 26.5; a power law wins by dAIC 67).  Nothing below
un-fires it.  What follows only locates the failure, and it can locate it in
either of two very different places:

  (i) the SUBSTRATE is not memoryless -- its own 1-body relaxation is
      non-exponential, and the 3-body correlator faithfully tracks it; or
  (ii) the 3-body correlator decays differently from the product of the 1-body
      decays -- the whole coming apart on a schedule of its own.

These are distinguished with NO exponential assumption anywhere, and with no
interpolation, because the A1 circuits measure both quantities at the same
delays in the same shots.  For the parity state under independent channels the
single-slot moment obeys M_q(t) = m_q (1 - kappa_q(t)), so

    kappa_q(t) = 1 - M_q(t)/m_q        (m_q from the A7 arm's saturation)
    D(t)  =?=  kappa_1(t) kappa_2(t) kappa_3(t)

is a shape-vs-shape identity that holds for ANY per-qubit decay law, exponential
or not.  It is the actual content of the ledger reading: the whole-only
correlator decays exactly as the product of the parts' decays.

Usage: qenv/bin/python qpu_habit_shapetest.py qpu_habit_A_<jobid>.json
"""
import json
import math
import sys

import numpy as np
from scipy.optimize import curve_fit

import qpu_habit_pipeline as P


def main():
    path = sys.argv[1]
    data = json.load(open(path))
    fz = data["freeze"]
    recs = {r["tag"]: r for r in data["records"]}
    sets = []
    for pre in ("A8", "A9"):
        if f"{pre}|cal|000|0" in recs:
            sets.append(P.assignment_matrices(
                P.counts_to_p(recs[f"{pre}|cal|000|0"]["counts"]).ravel(),
                P.counts_to_p(recs[f"{pre}|cal|111|0"]["counts"]).ravel()))
    amats = [sum(s[q] for s in sets) / len(sets) for q in range(3)]

    def corr(counts):
        pc = P.correct_readout(P.counts_to_p(counts), amats)
        pc = np.clip(pc, 0, None)
        return pc / pc.sum()

    # ---- m_q (the equilibrium <Z>) from the A7 arm, which does saturate -----
    ts7 = fz["delays_t1_us"]
    p1_7 = [[], [], []]
    for t in ts7:
        pc = corr(recs[f"A7|exc|ZZZ|{t}"]["counts"])
        for s, ax in enumerate(((1, 2), (0, 2), (0, 1))):
            p1_7[s].append(float(pc.sum(axis=ax)[1]))
    fits = [P.fit_T1(ts7, p1_7[s]) for s in range(3)]
    pexc = [f["p_exc"] for f in fits]
    m = [1 - 2 * p for p in pexc]
    T1 = [f["T1"] for f in fits]
    gam = sum(1.0 / x for x in T1)
    print("A7 anchor: T1 =", [round(x, 1) for x in T1],
          " p_exc =", [round(x, 4) for x in pexc], " Gamma_1 = %.6f" % gam)

    # ---- is the 1-BODY decay itself exponential? (stretched-exponential fit)
    print("\n=== (1) is the SUBSTRATE's own 1-body relaxation exponential? ===")
    print("  fitting P(1|t) = (A-m) exp(-(t/T)^beta) + m to the A7 arm")
    t7 = np.array(ts7, float)
    betas = []
    for s in range(3):
        y = np.array(p1_7[s])
        sig = np.sqrt(np.clip(y * (1 - y), 1e-6, None) / fz["shots"]["A7"])

        def f1(x, A, mm, T, be):
            return (A - mm) * np.exp(-(x / T) ** be) + mm
        try:
            pe, _ = curve_fit(f1, t7, y, p0=[y[0], max(y[-1], 1e-3), T1[s], 1.0],
                              sigma=sig, maxfev=80000,
                              bounds=([0, 0, 5, 0.2], [1, 0.5, 5000, 3.0]))
            chi_s = float(np.sum(((y - f1(t7, *pe)) / sig) ** 2))
            def f0(x, A, mm, T):
                return (A - mm) * np.exp(-x / T) + mm
            p0_, _ = curve_fit(f0, t7, y, p0=[y[0], max(y[-1], 1e-3), T1[s]],
                               sigma=sig, maxfev=80000,
                               bounds=([0, 0, 5], [1, 0.5, 5000]))
            chi_e = float(np.sum(((y - f0(t7, *p0_)) / sig) ** 2))
            betas.append(pe[3])
            print(f"  slot {s} (q{fz['slots_abc'][s]}): beta = {pe[3]:.3f}"
                  f"   chi2 stretched {chi_s:.1f} vs pure exponential {chi_e:.1f}"
                  f"   (dof {len(t7)-4} / {len(t7)-3})")
        except Exception as e:
            print("  slot", s, "fit failed:", e)

    # ---- the MODEL-FREE product test, same circuits, same delays ------------
    print("\n=== (2) MODEL-FREE: does D(t) equal the product of the parts? ===")
    dC = fz["delays_classical_us"]
    rows = []
    for t in dC:
        pc = corr(recs[f"A1|classical|ZZZ|{t}"]["counts"])
        M = P.moments(pc)
        kap = []
        for s in range(3):
            mask = 1 << s
            kap.append(1.0 - M[mask] / m[s])
        D = P.D_stat(pc)
        rows.append((t, D, kap[0] * kap[1] * kap[2], kap))
    print("   t(us)      D_meas   prod(kappa)   ratio    kappa per slot")
    ratios = []
    for t, D, pr, kap in rows:
        ratios.append(D / pr if pr > 0 else float("nan"))
        print(f"  {t:7.1f}   {D:9.5f}   {pr:9.5f}   {D/pr:7.4f}   "
              f"{[round(float(x),4) for x in kap]}")
    ratios = np.array(ratios)
    # shot-noise scale on the ratio, from the same MC machinery the bands used
    print(f"\n  ratio D/prod(kappa): mean {ratios.mean():.4f}  sd {ratios.std():.4f}"
          f"  range [{ratios.min():.4f}, {ratios.max():.4f}]")
    print("  (a FLAT ratio means the whole-only correlator decays exactly as the")
    print("   product of the parts, whatever shape the parts take; a TRENDING")
    print("   ratio means the whole comes apart on a schedule of its own)")
    # trend test on the ratio
    t_arr = np.array([r[0] for r in rows])
    A = np.vstack([np.ones_like(t_arr), t_arr]).T
    beta, *_ = np.linalg.lstsq(A, ratios, rcond=None)
    resid = ratios - A @ beta
    sd = resid.std(ddof=2)
    slope_sd = sd / np.sqrt(np.sum((t_arr - t_arr.mean()) ** 2))
    print(f"  linear trend in the ratio: {beta[1]:+.3e} +- {slope_sd:.3e} per us"
          f"   ({abs(beta[1])/slope_sd:.1f} sigma)")

    # ---- stretched exponential on D itself ---------------------------------
    print("\n=== (3) stretched exponential on the 3-body correlator ===")
    tD = np.array([r[0] for r in rows]); yD = np.array([r[1] for r in rows])
    sig = np.full_like(yD, 1.0 / math.sqrt(fz["shots"]["A1"]))
    try:
        pe, _ = curve_fit(lambda x, A, T, be: A * np.exp(-(x / T) ** be), tD, yD,
                          p0=[1.0, 1 / gam, 1.0], sigma=sig, maxfev=80000,
                          bounds=([0.5, 5, 0.2], [1.5, 5000, 3.0]))
        chi_s = float(np.sum(((yD - pe[0] * np.exp(-(tD / pe[1]) ** pe[2])) / sig) ** 2))
        p0_, _ = curve_fit(lambda x, A, r: A * np.exp(-r * x), tD, yD,
                           p0=[1.0, gam], sigma=sig, maxfev=80000)
        chi_e = float(np.sum(((yD - p0_[0] * np.exp(-p0_[1] * tD)) / sig) ** 2))
        print(f"  D(t) = A exp(-(t/T)^beta):  beta = {pe[2]:.3f}, T = {pe[1]:.1f} us,"
              f" A = {pe[0]:.4f}   chi2 {chi_s:.1f} (dof {len(tD)-3})")
        print(f"  D(t) = A exp(-r t)       :  r = {p0_[1]:.5f} /us, A = {p0_[0]:.4f}"
              f"   chi2 {chi_e:.1f} (dof {len(tD)-2})")
        print(f"  1/T_stretched = {1/pe[1]:.5f} /us vs Gamma_1 = {gam:.5f} /us"
              f"   ratio {1/(pe[1]*gam):.3f}")
        if betas:
            print(f"  MEAN 1-body beta = {np.mean(betas):.3f}  vs 3-body beta = {pe[2]:.3f}")
    except Exception as e:
        print("  fit failed:", e)

    out = dict(job=path, T1=T1, p_exc=pexc, gamma=gam,
               product_test=[dict(t=r[0], D=r[1], prod_kappa=r[2],
                                  kappa=[float(x) for x in r[3]]) for r in rows],
               ratio_mean=float(ratios.mean()), ratio_sd=float(ratios.std()),
               ratio_trend_per_us=float(beta[1]), ratio_trend_sd=float(slope_sd),
               beta_1body=[float(x) for x in betas])
    with open(path.replace("qpu_habit_", "qpu_shapetest_"), "w") as f:
        json.dump(out, f, indent=2, default=float)
    print("\nsaved", path.replace("qpu_habit_", "qpu_shapetest_"))


if __name__ == "__main__":
    main()
