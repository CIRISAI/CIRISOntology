#!/usr/bin/env python3
"""Band addendum: the JOINT band on the kill statistic.

qpu_habit_bands.py banded rate_D against a Gamma_1 = sum(1/T1) taken as exact.
It is not exact: the primary anchor is MEASURED in-job by arm A7, and that fit
has its own error, which propagates straight into the kill statistic.  This
script Monte-Carlos BOTH arms together and reports the joint band, which is
the one staked.

Also bands the A7 arm itself (can 5 points x 4096 shots even measure T1?) and
the null controls' 99th percentiles.

Usage: qenv/bin/python qpu_habit_bands2.py [n_mc]
"""
import json
import math
import sys

import numpy as np

import os
import qpu_habit_pipeline as P
BOUT = "%s%s.json" % ("qpu_habit_bands2", "_v2" if "freeze2" in os.environ.get("QPU_FREEZE","") else "")
import qpu_habit_bands as B

RNG = np.random.default_rng(2718281)
fz = B.fz
T1 = B.T1
P_EXC = B.P_EXC


def sim_A7(rng, shots):
    """Simulate the in-job T1 audit: |111>, idle, read Z; fit each qubit."""
    ts = fz["delays_t1_us"]
    amats = B.sim_cal(fz["shots"]["A8"], rng)
    p1 = [[] for _ in range(3)]
    for t in ts:
        k, b = P.damping_channel(t, T1, [P_EXC] * 3)
        M = np.zeros(8)
        M[0] = 1.0
        for mask in range(1, 8):
            s = 1.0
            for q in range(3):
                if (mask >> q) & 1:
                    s *= -1.0          # |111> : <Z_q> = -1
            M[mask] = s
        true = P.dist_from_moments(P.apply_product_channel(M, k, b))
        meas = B.measured(true)
        meas = np.clip(meas.ravel(), 0, None); meas = meas / meas.sum()
        c = rng.multinomial(shots, meas) / shots
        pc = P.correct_readout(c.reshape(2, 2, 2), amats)
        pc = np.clip(pc, 0, None); pc = pc / pc.sum()
        p1[0].append(float(pc.sum(axis=(1, 2))[1]))
        p1[1].append(float(pc.sum(axis=(0, 2))[1]))
        p1[2].append(float(pc.sum(axis=(0, 1))[1]))
    fits = [P.fit_T1(ts, p1[s]) for s in range(3)]
    return fits


def main():
    n_mc = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    out = {}

    print("=== A7 in-job T1 audit: can it measure T1? ===")
    T1hat = np.zeros((n_mc, 3)); gam = np.zeros(n_mc); nfail = 0
    for r in range(n_mc):
        fits = sim_A7(RNG, fz["shots"]["A7"])
        for s in range(3):
            T1hat[r, s] = fits[s].get("T1", np.nan)
        if np.any(np.isnan(T1hat[r])):
            nfail += 1
            T1hat[r] = np.array(T1)          # fit failed: fall back, counted below
        gam[r] = sum(1.0 / T1hat[r, s] for s in range(3))
    print(f"  T1 fit failures: {nfail}/{n_mc}")
    for s in range(3):
        print(f"  slot {s} (q{fz['slots_abc'][s]}): true {T1[s]:7.2f}  fit "
              f"{np.nanmean(T1hat[:,s]):7.2f} +- {np.nanstd(T1hat[:,s]):5.2f} us "
              f"({100*np.nanstd(T1hat[:,s])/T1[s]:.2f} %)")
    gam_true = sum(1.0 / x for x in T1)
    print(f"  Gamma_1 = sum(1/T1): true {gam_true:.6f}  fit {gam.mean():.6f} "
          f"+- {gam.std():.6f}  ({100*gam.std()/gam_true:.2f} %)")
    out["A7_T1_fit"] = {
        "true_T1": [float(x) for x in T1],
        "fit_mean": [float(np.nanmean(T1hat[:, s])) for s in range(3)],
        "fit_sd": [float(np.nanstd(T1hat[:, s])) for s in range(3)],
        "gamma_true": float(gam_true), "gamma_mean": float(gam.mean()),
        "gamma_sd": float(gam.std()),
        "T1_range_ok": bool(np.all((T1hat > 50) & (T1hat < 800))),
    }

    print("\n=== JOINT band on the kill statistic (A1 rate / A7 Gamma) ===")
    dC = fz["delays_classical_us"]
    res = B.mc_arm(B.true_classical, dC, fz["shots"]["A1"], n_mc,
                   fz["shots"]["A8"], RNG)
    idx = list(range(len(dC)))
    floor_mean = res["floor"].mean(axis=0)
    t = np.array([dC[i] for i in idx], float)
    s_sd = np.std(np.clip(res["sh_cor"][:, idx] - floor_mean[idx], 1e-12, None), axis=0)
    y_mean = np.mean(np.clip(res["sh_cor"][:, idx] - floor_mean[idx], 1e-12, None), axis=0)
    sig_log = s_sd / np.maximum(y_mean, 1e-12)
    d_sd = np.std(np.abs(res["d_cor"][:, idx]), axis=0)
    d_mean = np.mean(np.abs(res["d_cor"][:, idx]), axis=0)
    sig_logd = d_sd / np.maximum(d_mean, 1e-12)
    RD, RS = [], []
    for r in range(n_mc):
        d = np.clip(np.abs(res["d_cor"][r, idx]), 1e-9, None)
        rate_d, _ = P.wls_logfit(t, d, sig_logd)
        y = np.clip(res["sh_cor"][r, idx] - floor_mean[idx], 1e-9, None)
        rate_s, _ = P.wls_logfit(t, y, sig_log)
        RD.append(rate_d / gam[r])
        RS.append(rate_s / (2 * gam[r]))
    RD = np.array(RD); RS = np.array(RS)
    print(f"  R_D  = rate_D / Gamma_hat  : {RD.mean():.4f} +- {RD.std():.4f}  "
          f"[p005 {np.quantile(RD,0.005):.4f}, p995 {np.quantile(RD,0.995):.4f}]")
    print(f"  R_S  = rate_S / 2 Gamma_hat: {RS.mean():.4f} +- {RS.std():.4f}  "
          f"[p005 {np.quantile(RS,0.005):.4f}, p995 {np.quantile(RS,0.995):.4f}]")
    out["joint_R_D"] = dict(mean=float(RD.mean()), sd=float(RD.std()),
                            p005=float(np.quantile(RD, 0.005)),
                            p995=float(np.quantile(RD, 0.995)))
    out["joint_R_S"] = dict(mean=float(RS.mean()), sd=float(RS.std()),
                            p005=float(np.quantile(RS, 0.005)),
                            p995=float(np.quantile(RS, 0.995)))
    SYS = 0.10
    lo = out["joint_R_D"]["p005"] * (1 - SYS)
    hi = out["joint_R_D"]["p995"] * (1 + SYS)
    out["K_RATE_band"] = [float(lo), float(hi)]
    out["K_RATE_sys_allowance"] = SYS
    print(f"  STAKED K-RATE band (99% joint MC widened by +-10% systematic): "
          f"[{lo:.4f}, {hi:.4f}]")

    print("\n=== chi2 of the exact-curve test, with the anchor fitted in-job ===")
    mu = res["sh_cor"].mean(axis=0); sd = res["sh_cor"].std(axis=0)
    chi2 = np.array([float(np.sum(((res["sh_cor"][r] - mu) / sd) ** 2))
                     for r in range(n_mc)])
    print(f"  dof {len(dC)}: mean {chi2.mean():.2f}  p99 {np.quantile(chi2,0.99):.2f}"
          f"  p999 {np.quantile(chi2,0.999):.2f}")
    out["K_SHAPE_chi2"] = dict(dof=len(dC), mean=float(chi2.mean()),
                               p99=float(np.quantile(chi2, 0.99)),
                               p999=float(np.quantile(chi2, 0.999)))

    print("\n=== null controls: 99th percentiles to stake (VOID above these) ===")
    for label, shots in (("A5/A6 (4096 shots)", fz["shots"]["A4"]),
                         ("A7 (4096 shots)", fz["shots"]["A7"])):
        vals = []
        amats_cache = None
        for r in range(400):
            amats = B.sim_cal(fz["shots"]["A8"], RNG)
            p = np.full((2, 2, 2), 0.125)
            pm = B.measured(p); pm = np.clip(pm.ravel(), 0, None); pm /= pm.sum()
            c = RNG.multinomial(shots, pm) / shots
            pc = P.correct_readout(c.reshape(2, 2, 2), amats)
            pc = np.clip(pc, 0, None); pc /= pc.sum()
            vals.append(P.share(pc))
        vals = np.array(vals)
        print(f"  {label}: mean {vals.mean():.3e}  p99 {np.quantile(vals,0.99):.3e}"
              f"  p999 {np.quantile(vals,0.999):.3e}")
        out[f"null_{label.split()[0].replace('/','_')}"] = dict(
            mean=float(vals.mean()), p99=float(np.quantile(vals, 0.99)),
            p999=float(np.quantile(vals, 0.999)))

    with open(BOUT, "w") as f:
        json.dump(out, f, indent=2, default=float)
    print("\nsaved qpu_habit_bands2.json")


if __name__ == "__main__":
    main()
