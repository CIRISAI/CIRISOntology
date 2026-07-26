#!/usr/bin/env python3
"""Band addendum 2 — re-staking K-SHAPE so it tests SHAPE, not fidelity.

A chi2 of the measured share against the noisy model's absolute expectation
would fire on state-preparation infidelity: the model knows about readout and
relaxation but not about prep error, the residual thermal population, or
measurement-induced relaxation, and a 2 % amplitude deficit alone puts several
points many sigma out.  Killing the rent clause for that would repeat run 1's
authoring error in new clothes.

The fix is to test the shape in the coordinate where the nuisance is exactly one
number.  The connected 3-body moment obeys D(t) = c0 * exp(-Gamma_1 t) with
Gamma_1 = sum(1/T1) fixed by the INDEPENDENT in-job audit, and c0 a
time-independent contraction that absorbs prep infidelity and any residual
readout mis-correction.  c0 cannot absorb a wrong rate or a wrong shape — which
is precisely what is being tested.

Staked here: the chi2 band for the fixed-slope fit (dof = n-1), and the
distribution of the family-comparison statistic under the true model.

Usage: qenv/bin/python qpu_habit_bands3.py [n_mc]
"""
import json
import math
import sys

import numpy as np
from scipy.optimize import curve_fit

import os
import qpu_habit_pipeline as P
BOUT = "%s%s.json" % ("qpu_habit_bands3", "_v2" if "freeze2" in os.environ.get("QPU_FREEZE","") else "")
import qpu_habit_bands as B
import qpu_habit_bands2 as B2

RNG = np.random.default_rng(577215)
fz = B.fz


def main():
    n_mc = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    dC = fz["delays_classical_us"]
    t = np.array(dC, float)

    res = B.mc_arm(B.true_classical, dC, fz["shots"]["A1"], n_mc,
                   fz["shots"]["A8"], RNG)
    dsd = np.abs(res["d_cor"]).std(axis=0)
    dmu = np.abs(res["d_cor"]).mean(axis=0)
    sig_log = dsd / np.maximum(dmu, 1e-12)

    gam = np.zeros(n_mc)
    for r in range(n_mc):
        fits = B2.sim_A7(RNG, fz["shots"]["A7"])
        vals = [f.get("T1", np.nan) for f in fits]
        if np.any(np.isnan(vals)):
            vals = B.T1
        gam[r] = sum(1.0 / x for x in vals)

    chi2_fixed, chi2_free, dAIC = [], [], []
    for r in range(n_mc):
        y = np.log(np.clip(np.abs(res["d_cor"][r]), 1e-12, None))
        w = 1.0 / sig_log ** 2
        # fixed slope = -Gamma_hat, intercept fitted: THE SHAPE TEST
        c0 = np.sum(w * (y + gam[r] * t)) / np.sum(w)
        r_fixed = y - (c0 - gam[r] * t)
        chi2_fixed.append(float(np.sum(w * r_fixed ** 2)))
        # both free: the rate test's residual
        X = np.vstack([np.ones_like(t), t]).T
        W = np.diag(w)
        beta = np.linalg.inv(X.T @ W @ X) @ (X.T @ W @ y)
        r_free = y - X @ beta
        chi2_free.append(float(np.sum(w * r_free ** 2)))
        # family comparison on |D| itself
        yy = np.abs(res["d_cor"][r])
        sw = np.maximum(dsd, 1e-9)
        try:
            pe, _ = curve_fit(lambda x, A, rr: A * np.exp(-rr * x), t, yy,
                              p0=[1.0, gam[r]], sigma=sw, maxfev=40000)
            ce = float(np.sum(((yy - pe[0] * np.exp(-pe[1] * t)) / sw) ** 2))
            pp, _ = curve_fit(lambda x, A, tau, al: A * (1 + x / tau) ** (-al),
                              t, yy, p0=[1.0, 50.0, 2.0], sigma=sw, maxfev=40000,
                              bounds=([0, 1e-2, 1e-3], [10, 1e5, 50]))
            cp = float(np.sum(((yy - pp[0] * (1 + t / pp[1]) ** (-pp[2])) / sw) ** 2))
            dAIC.append((ce + 4) - (cp + 6))
        except Exception:
            pass
    chi2_fixed = np.array(chi2_fixed); chi2_free = np.array(chi2_free)
    dAIC = np.array(dAIC)
    n = len(t)
    print(f"K-SHAPE: chi2 of log|D| vs fixed-slope model (dof {n-1})")
    print(f"  mean {chi2_fixed.mean():.2f}  p99 {np.quantile(chi2_fixed,0.99):.2f}"
          f"  p999 {np.quantile(chi2_fixed,0.999):.2f}")
    print(f"  (both-free residual chi2, dof {n-2}: mean {chi2_free.mean():.2f}"
          f"  p99 {np.quantile(chi2_free,0.99):.2f})")
    print(f"K-FAMILY: dAIC(exp - powerlaw) under the TRUE exponential model:")
    print(f"  mean {dAIC.mean():+.2f}  p99 {np.quantile(dAIC,0.99):+.2f}"
          f"  max {dAIC.max():+.2f}   (exp loses if dAIC > 0)")
    out = dict(
        K_SHAPE_chi2_dof=n - 1,
        K_SHAPE_chi2_mean=float(chi2_fixed.mean()),
        K_SHAPE_chi2_p99=float(np.quantile(chi2_fixed, 0.99)),
        K_SHAPE_chi2_p999=float(np.quantile(chi2_fixed, 0.999)),
        chi2_free_dof=n - 2, chi2_free_p99=float(np.quantile(chi2_free, 0.99)),
        dAIC_mean=float(dAIC.mean()), dAIC_p99=float(np.quantile(dAIC, 0.99)),
        dAIC_max=float(dAIC.max()), n_mc=n_mc,
        sigma_logD=[float(x) for x in sig_log],
        D_model=[float(x) for x in res["D_true"]],
        D_sd=[float(x) for x in dsd],
    )
    with open(BOUT, "w") as f:
        json.dump(out, f, indent=2)
    print("saved qpu_habit_bands3.json")


if __name__ == "__main__":
    main()
