#!/usr/bin/env python3
"""Run 3 (addendum 2): freeze, gate and bands for the SECTOR-FLOW dichotomy.

Every band is simulation-derived, and the ferro arm's prediction is built the
way the hardware analysis will build it: from the per-qubit decay kappa_q(t)
MEASURED by the audit arm at the same delays, with no functional form assumed
anywhere (run 2 showed the substrate is not a single exponential, so assuming
one would be staking a criterion the device cannot meet).

Usage: qenv/bin/python qpu_sector_bands.py freeze
       qenv/bin/python qpu_sector_bands.py bands [n_mc]
"""
import json
import math
import sys
import time

import numpy as np

import qpu_habit_pipeline as P

LN2 = math.log(2.0)
RNG = np.random.default_rng(1618033)
FZ3 = "qpu_habit_freeze3.json"

M_PARITY = np.zeros(8); M_PARITY[0] = 1.0; M_PARITY[7] = 1.0
M_FERRO = np.array([1.0, 0, 0, 1.0, 0, 1.0, 1.0, 0])
M_PROD = np.zeros(8); M_PROD[0] = 1.0


def dt_align(x):
    return round(round(x / 0.064) * 0.064, 3)


def cmd_freeze():
    scr = json.load(open("qpu_habit_screen.json"))
    pick = None
    for r in scr["ranking"]:
        if r["worst_readout"] <= 0.015 and all(60 <= x <= 500 for x in r["T1"]):
            pick = r
            break
    trip = pick["trip"]; a, c, b = trip
    slots = [a, b, c]
    qi = {q: i for i, q in enumerate(scr["qubits"])}
    T1 = [pick["T1"][trip.index(q)] for q in slots]
    e0 = [float(scr["p1_prep0"][qi[q]]) for q in slots]
    e1 = [float(1 - scr["p1_prep1"][qi[q]]) for q in slots]
    from qiskit_ibm_runtime import QiskitRuntimeService
    be = QiskitRuntimeService().backend(P.BACKEND_NAME)
    props = be.properties()
    T2 = [props.t2(q) * 1e6 for q in slots]

    # locate the predicted bulge peak, then put the grid around it
    pexc = 0.03
    best = (0.0, -1.0)
    for t in np.arange(0, 300, 0.5):
        k, bb = P.damping_channel(float(t), T1, [pexc] * 3)
        s = P.share(P.dist_from_moments(P.apply_product_channel(M_FERRO, k, bb)))
        if s > best[1]:
            best = (float(t), s)
    tpk = best[0]
    grid = [0.0, 0.17 * tpk, 0.34 * tpk, 0.55 * tpk, 0.78 * tpk, 1.0 * tpk,
            1.32 * tpk, 1.75 * tpk, 2.35 * tpk, 3.2 * tpk, 4.5 * tpk, 6.5 * tpk]
    dF = [dt_align(x) for x in grid]
    T1med = sum(T1) / 3
    fz = {
        "v3": True, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "backend": P.BACKEND_NAME, "screen_job": scr["job_id"],
        "triple_path": trip, "slots_abc": slots,
        "worst_measured_readout": pick["worst_readout"],
        "cal": {"T1_us": {str(q): T1[i] for i, q in enumerate(slots)},
                "T2_us": {str(q): T2[i] for i, q in enumerate(slots)},
                "prob_meas1_prep0": {str(q): e0[i] for i, q in enumerate(slots)},
                "prob_meas0_prep1": {str(q): e1[i] for i, q in enumerate(slots)},
                "source": "screening job (measured)",
                "cz_error": {f"{a}_{c}": pick["cz"][0], f"{c}_{b}": pick["cz"][1]}},
        "predicted_peak_us": tpk, "predicted_peak_share": best[1],
        "delays_ferro_us": dF,
        "delays_sat_us": [dt_align(2.2 * T1med), dt_align(3.4 * T1med)],
        "delays_parity_us": [dt_align(x) for x in
                             (0, 0.35 / (2 * sum(1 / x for x in T1)),
                              1.0 / (2 * sum(1 / x for x in T1)),
                              2.0 / (2 * sum(1 / x for x in T1)),
                              3.3 / (2 * sum(1 / x for x in T1)),
                              5.0 / (2 * sum(1 / x for x in T1)))],
        "delays_product_us": [0.0, dF[6], dF[10]],
        "delays_plus_us": [dt_align(x) for x in (0, 4, 9, 16, 26, 40, 60)],
        "shots": {"C1": 8192, "C2": 4096, "cal": 8192},
        "p_exc_nominal": pexc,
    }
    with open(FZ3, "w") as f:
        json.dump(fz, f, indent=2)
    print(json.dumps({k: v for k, v in fz.items() if k != "cal"}, indent=2))
    print("T1", [round(x, 1) for x in T1], "T2", [round(x, 1) for x in T2])
    plan = P.plan_C(fz)
    print(f"JOB C: {len(plan)} circuits, est {P.estimate_seconds(plan):.1f} QPU s")


# --------------------------------------------------------------------------

def load():
    fz = json.load(open(FZ3))
    SL = fz["slots_abc"]
    T1 = [fz["cal"]["T1_us"][str(q)] for q in SL]
    E0 = [fz["cal"]["prob_meas1_prep0"][str(q)] for q in SL]
    E1 = [fz["cal"]["prob_meas0_prep1"][str(q)] for q in SL]
    return fz, T1, P.readout_channel(E0, E1)


def pair_cov(p):
    M = P.moments(p)
    return [M[3] - M[1] * M[2], M[5] - M[1] * M[4], M[6] - M[2] * M[4]]


def pair_mi(p):
    out = []
    for ax in (2, 1, 0):
        m = p.sum(axis=ax)
        r = m.sum(axis=1); c = m.sum(axis=0)
        mi = 0.0
        for i in range(2):
            for j in range(2):
                if m[i, j] > 1e-15:
                    mi += m[i, j] * math.log(m[i, j] / max(r[i] * c[j], 1e-300))
        out.append(mi)
    return out


def main_bands(n_mc=300):
    fz, T1, (ROK, ROB) = load()
    pexc = [fz["p_exc_nominal"]] * 3
    dF = fz["delays_ferro_us"]

    def truth(M, t):
        k, b = P.damping_channel(t, T1, pexc)
        return P.dist_from_moments(P.apply_product_channel(M, k, b))

    def meas(p):
        return P.dist_from_moments(P.apply_product_channel(P.moments(p), ROK, ROB))

    def sim_cal(shots, rng):
        out = []
        for prep in (0, 7):
            M = np.zeros(8); M[0] = 1.0
            z = [1.0 if not ((prep >> q) & 1) else -1.0 for q in range(3)]
            for mask in range(1, 8):
                s = 1.0
                for q in range(3):
                    if (mask >> q) & 1:
                        s *= z[q]
                M[mask] = s
            pp = P.dist_from_moments(P.apply_product_channel(M, ROK, ROB))
            pp = np.clip(pp.ravel(), 0, None); pp /= pp.sum()
            out.append(rng.multinomial(shots, pp) / shots)
        return P.assignment_matrices(out[0], out[1])

    def draw(p, shots, amats, rng):
        pm = np.clip(meas(p).ravel(), 0, None); pm /= pm.sum()
        pc = P.correct_readout((rng.multinomial(shots, pm) / shots).reshape(2, 2, 2),
                               amats)
        pc = np.clip(pc, 0, None)
        return pc / pc.sum()

    M_EXC = np.zeros(8); M_EXC[0] = 1.0
    for mask in range(1, 8):
        s = 1.0
        for q in range(3):
            if (mask >> q) & 1:
                s *= -1.0
        M_EXC[mask] = s

    sh_f = np.zeros((n_mc, len(dF)))
    pred_f = np.zeros((n_mc, len(dF)))
    cov_ratio = np.zeros((n_mc, len(dF), 3))
    peak_t = np.zeros(n_mc); peak_h = np.zeros(n_mc)
    for r in range(n_mc):
        amats = sim_cal(fz["shots"]["cal"], RNG)
        kap = np.zeros((len(dF), 3))
        for i, t in enumerate(dF):
            pf = draw(truth(M_FERRO, t), fz["shots"]["C1"], amats, RNG)
            sh_f[r, i] = P.share(pf)
            pe = draw(truth(M_EXC, t), fz["shots"]["C2"], amats, RNG)
            for q in range(3):
                p1 = float(pe.sum(axis=tuple(x for x in range(3) if x != q))[1])
                kap[i, q] = (p1 - pexc[q]) / (1 - pexc[q])
            cv = pair_cov(pf)
            for j, (u, v) in enumerate(((0, 1), (0, 2), (1, 2))):
                pr = kap[i, u] * kap[i, v]
                cov_ratio[r, i, j] = cv[j] / pr if abs(pr) > 1e-9 else np.nan
        # the PREDICTED ferro curve, built from the MEASURED kappas (no model)
        for i in range(len(dF)):
            k = np.clip(kap[i], 0, 1.5)
            b = (1 - k) * np.array([1 - 2 * x for x in pexc])
            pred_f[r, i] = P.share(P.dist_from_moments(
                P.apply_product_channel(M_FERRO, k, b)))
        j = int(np.argmax(sh_f[r])); peak_t[r] = dF[j]; peak_h[r] = sh_f[r, j]

    mu = sh_f.mean(axis=0); sd = sh_f.std(axis=0)
    resid = sh_f - pred_f
    rsd = resid.std(axis=0)
    chi2 = np.array([float(np.sum((resid[r] / rsd) ** 2)) for r in range(n_mc)])
    print("=== C1 FERRO: the whole-only bulge fed by a decaying pair habit ===")
    print("   t(us)    truth     sim mean +- sd      pred-from-kappa mean")
    for i, t in enumerate(dF):
        print(f"  {t:7.1f}  {P.share(truth(M_FERRO,t)):8.5f}  {mu[i]:8.5f} +- {sd[i]:7.5f}"
              f"    {pred_f[:,i].mean():8.5f}")
    print(f"\n  K-CURVE chi2 (dof {len(dF)}, ZERO free parameters): mean {chi2.mean():.2f}"
          f"  p99 {np.quantile(chi2,0.99):.2f}  p999 {np.quantile(chi2,0.999):.2f}")
    vals, cnts = np.unique(peak_t, return_counts=True)
    print(f"  K-PEAK location: mode {vals[np.argmax(cnts)]:.1f} us; distribution "
          f"{dict(zip([round(float(v),1) for v in vals],[int(c) for c in cnts]))}")
    print(f"  K-PEAK height: {peak_h.mean():.5f} +- {peak_h.std():.5f}"
          f"  [p005 {np.quantile(peak_h,0.005):.5f}, p995 {np.quantile(peak_h,0.995):.5f}]")
    cr = cov_ratio.reshape(n_mc, -1)
    print(f"  K-PAIRMULT cov/(kappa_i kappa_j cov0) : mean {np.nanmean(cr):.4f}"
          f"  sd {np.nanstd(cr):.4f}  [p005 {np.nanquantile(cr,0.005):.4f},"
          f" p995 {np.nanquantile(cr,0.995):.4f}]")

    print("\n=== C3 PARITY: the pair sector must stay at EXACTLY zero ===")
    dP = fz["delays_parity_us"]
    mis, shs = [], []
    for r in range(min(n_mc, 200)):
        amats = sim_cal(fz["shots"]["cal"], RNG)
        row_mi, row_s = [], []
        for t in dP:
            pp = draw(truth(M_PARITY, t), fz["shots"]["C1"], amats, RNG)
            row_mi.append(max(pair_mi(pp))); row_s.append(P.share(pp))
        mis.append(row_mi); shs.append(row_s)
    mis = np.array(mis); shs = np.array(shs)
    for i, t in enumerate(dP):
        print(f"  t={t:7.1f}  share {shs[:,i].mean():8.5f}  max pair MI "
              f"{mis[:,i].mean():.3e} (p99 {np.quantile(mis[:,i],0.99):.3e})")
    print(f"  K-PAIRZERO threshold (max over arm, p999): "
          f"{np.quantile(mis.max(axis=1),0.999):.3e}")

    print("\n=== C4/C5 the background-free nulls ===")
    nulls = {}
    for name, M, shots, ds in (("product/Z", M_PROD, fz["shots"]["C1"], fz["delays_product_us"]),
                               ("plus/X", M_PROD, fz["shots"]["C2"], fz["delays_plus_us"])):
        v = []
        for r in range(200):
            amats = sim_cal(fz["shots"]["cal"], RNG)
            for t in ds:
                v.append(P.share(draw(truth(M, t), shots, amats, RNG)))
        v = np.array(v)
        nulls[name] = dict(mean=float(v.mean()), p99=float(np.quantile(v, 0.99)),
                           p999=float(np.quantile(v, 0.999)))
        print(f"  {name}: mean {v.mean():.3e}  p99 {np.quantile(v,0.99):.3e}"
              f"  p999 {np.quantile(v,0.999):.3e}")

    out = dict(n_mc=n_mc, delays=dF,
               ferro_model=[float(P.share(truth(M_FERRO, t))) for t in dF],
               ferro_sim_mean=[float(x) for x in mu], ferro_sim_sd=[float(x) for x in sd],
               K_CURVE_chi2=dict(dof=len(dF), mean=float(chi2.mean()),
                                 p99=float(np.quantile(chi2, 0.99)),
                                 p999=float(np.quantile(chi2, 0.999))),
               K_PEAK_t=dict(mode=float(vals[np.argmax(cnts)]),
                             support=[float(v) for v in vals],
                             counts=[int(c) for c in cnts]),
               K_PEAK_h=dict(mean=float(peak_h.mean()), sd=float(peak_h.std()),
                             p005=float(np.quantile(peak_h, 0.005)),
                             p995=float(np.quantile(peak_h, 0.995))),
               K_PAIRMULT=dict(mean=float(np.nanmean(cr)), sd=float(np.nanstd(cr)),
                               p005=float(np.nanquantile(cr, 0.005)),
                               p995=float(np.nanquantile(cr, 0.995))),
               K_PAIRZERO_p999=float(np.quantile(mis.max(axis=1), 0.999)),
               nulls=nulls)
    with open("qpu_sector_bands.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nsaved qpu_sector_bands.json")


if __name__ == "__main__":
    if sys.argv[1] == "freeze":
        cmd_freeze()
    else:
        main_bands(int(sys.argv[2]) if len(sys.argv) > 2 else 300)
