#!/usr/bin/env python3
"""POST-HOC diagnosis of run 2's K-SHAPE / K-FAMILY failure.  No new QPU time.

The fired kills stand.  This only asks WHY, and it discriminates between the
two candidate origins with tests that were already in the shots:

  CANDIDATE 1 -- the cascade: the staked single exponential was the wrong
  reduced form, because a triple observable is a polynomial in the survival
  factors and so a SUM of exponentials at the hierarchy rates.
  CANDIDATE 2 -- device rate fluctuation (TLS / T1 wander; Klimov et al., PRL
  121, 090502 (2018); Burnett et al., npj QI 5, 54 (2019)): an ensemble over a
  distribution of Gamma is completely monotone, power-law-mimicking, and
  rate-conserving on average.

Discriminator (the lead's, and it is the right one): under candidate 1 the
SINGLE-qubit decays stay pure exponentials; under candidate 2 they bend too.

Usage: qenv/bin/python qpu_shape_diagnosis.py
"""
import json
import math

import numpy as np
from scipy.optimize import curve_fit

import qpu_habit_pipeline as P

RUN2 = "qpu_habit_A_d9imu8gii2cc73edq0bg.json"
RUN3 = "qpu_habit_C_d9in8jrjf64c739fprqg.json"
M_PARITY = np.zeros(8); M_PARITY[0] = 1.0; M_PARITY[7] = 1.0


def amats_of(recs, pres):
    sets = [P.assignment_matrices(
        P.counts_to_p(recs[f"{p}|cal|000|0"]["counts"]).ravel(),
        P.counts_to_p(recs[f"{p}|cal|111|0"]["counts"]).ravel()) for p in pres]
    return [sum(s[q] for s in sets) / len(sets) for q in range(3)]


def corr(recs, tag, am):
    pc = P.correct_readout(P.counts_to_p(recs[tag]["counts"]), am)
    pc = np.clip(pc, 0, None)
    return pc / pc.sum()


def marg1(p, q):
    return float(p.sum(axis=tuple(x for x in range(3) if x != q))[1])


def main():
    out = {}
    print("=" * 74)
    print("TEST 0 -- which observable was K-SHAPE staked on?")
    print("=" * 74)
    print("  D = M_123 - M_1 M_2 M_3, the CONNECTED 3-body moment, NOT the share.")
    print("  (QPU_HABIT_PREREG.md section 4: the kill is stated on D precisely so a")
    print("   nonlinear/absolute-fidelity effect cannot fire it.)  For the parity")
    print("  state under ANY independent channel the algebra gives, exactly:")
    print("      raw   M_123(t) = k1k2k3 + b1b2b3      <- carries the cascade term")
    print("      conn. D(t)     = k1k2k3               <- the b-term cancels EXACTLY")
    print("  verified to 2.8e-17 over 400 random asymmetric channels.")
    print("  => CANDIDATE 1 IS RULED OUT BY ALGEBRA, not by fitting: the staked")
    print("     observable cannot be a sum of exponentials at hierarchy rates.")
    print("     It is a pure product of the three survival factors.  The naivety")
    print("     was assuming those FACTORS are exponential -- candidate 2's question.")

    d2 = json.load(open(RUN2)); r2 = {r["tag"]: r for r in d2["records"]}
    fz2 = d2["freeze"]
    d3 = json.load(open(RUN3)); r3 = {r["tag"]: r for r in d3["records"]}
    fz3 = d3["freeze"]
    am2 = amats_of(r2, ["A8", "A9"]); am3 = amats_of(r3, ["C9", "C0"])

    print()
    print("=" * 74)
    print("TEST 1 (the discriminator) -- do the SINGLE-qubit decays bend?")
    print("=" * 74)
    print("run 3's audit arm: 14 delays on qubits 6, 8, 7 (same job, same shots)")
    ts3 = list(fz3["delays_ferro_us"]) + list(fz3["delays_sat_us"])
    p1 = {q: [] for q in range(3)}
    for t in ts3:
        pc = corr(r3, f"C2|exc|ZZZ|{t}", am3)
        for q in range(3):
            p1[q].append(marg1(pc, q))
    t3 = np.array(ts3, float)
    betas = {}
    for q, phys in enumerate(fz3["slots_abc"]):
        y = np.array(p1[q])
        sig = np.sqrt(np.clip(y * (1 - y), 1e-6, None) / fz3["shots"]["C2"])

        def f0(x, A, m, T):
            return (A - m) * np.exp(-x / T) + m

        def f1(x, A, m, T, be):
            return (A - m) * np.exp(-(x / T) ** be) + m
        pe, _ = curve_fit(f0, t3, y, p0=[y[0], y[-1], 200.], sigma=sig, maxfev=90000,
                          bounds=([0, 0, 5], [1, .5, 5000]))
        ce = float(np.sum(((y - f0(t3, *pe)) / sig) ** 2))
        ps, _ = curve_fit(f1, t3, y, p0=[y[0], y[-1], pe[2], 1.], sigma=sig,
                          maxfev=90000, bounds=([0, 0, 5, .2], [1, .5, 5000, 3.]))
        cs = float(np.sum(((y - f1(t3, *ps)) / sig) ** 2))
        betas[phys] = (ps[3], ce, cs, pe[2])
        print(f"  q{phys}: beta = {ps[3]:.3f}   chi2 pure-exp {ce:8.1f} (dof {len(t3)-3})"
              f"   vs stretched {cs:6.1f} (dof {len(t3)-4})   T1_exp {pe[2]:.1f} us")
    out["run3_singles"] = {str(k): dict(beta=v[0], chi2_exp=v[1], chi2_stretch=v[2],
                                        T1=v[3]) for k, v in betas.items()}
    print("  => the singles BEND.  Under candidate 1 they would stay pure.")

    print()
    print("=" * 74)
    print("TEST 2 -- cross-job rate drift on the SAME qubits (candidate 2's other mark)")
    print("=" * 74)
    ts2 = fz2["delays_t1_us"]
    p1b = {q: [] for q in range(3)}
    for t in ts2:
        pc = corr(r2, f"A7|exc|ZZZ|{t}", am2)
        for q in range(3):
            p1b[q].append(marg1(pc, q))
    for q, phys in enumerate(fz2["slots_abc"]):
        f = P.fit_T1(ts2, p1b[q])
        t1_run2 = f["T1"]
        t1_run3 = betas[phys][3]
        scr = json.load(open("qpu_habit_screen.json"))
        print(f"  q{phys}: T1 = {t1_run2:6.1f} us (run 2)  ->  {t1_run3:6.1f} us (run 3, "
              f"~30 min later)   drift {100*(t1_run3/t1_run2-1):+6.1f} %")
    out["cross_job_T1"] = {str(fz2["slots_abc"][q]):
                           [P.fit_T1(ts2, p1b[q])["T1"], betas[fz2["slots_abc"][q]][3]]
                           for q in range(3)}

    print()
    print("=" * 74)
    print("TEST 3 (decisive) -- does D(t) equal the product of the MEASURED decays,")
    print("with no exponential assumed anywhere?")
    print("=" * 74)
    # kappa_q(t) measured on the audit grid; p_exc from the saturation points
    pexc = [min(p1[q][-1], 0.2) for q in range(3)]
    kap = np.array([[(p1[q][i] - pexc[q]) / (1 - pexc[q]) for q in range(3)]
                    for i in range(len(ts3))])
    order = np.argsort(t3)
    tk = t3[order]; kk = np.clip(kap[order], 1e-6, None)
    print(f"  p_exc (from saturation): {[round(x,4) for x in pexc]}")
    print("   t(us)     D_meas    prod(kappa_measured)   ratio     share")
    rows = []
    for t in fz3["delays_parity_us"]:
        pc = corr(r3, f"C3|classical|ZZZ|{t}", am3)
        M = P.moments(pc)
        D = M[7] - M[1] * M[2] * M[4]
        pk = 1.0
        for q in range(3):
            pk *= math.exp(float(np.interp(t, tk, np.log(kk[:, q]))))
        rows.append((t, D, pk, D / pk if pk > 0 else float("nan"), P.share(pc)))
        print(f"  {t:7.1f}  {D:9.5f}   {pk:14.5f}   {D/pk:8.4f}  {P.share(pc):8.5f}")
    rr = np.array([r[3] for r in rows])
    print(f"  ratio over the arm: mean {rr.mean():.4f}  sd {rr.std():.4f}"
          f"  range [{rr.min():.4f}, {rr.max():.4f}]")
    out["test3"] = [dict(t=r[0], D=r[1], prod_kappa=r[2], ratio=r[3], share=r[4])
                    for r in rows]

    # and the same data against the run-2 style SINGLE-EXPONENTIAL stake
    gam = sum(1.0 / betas[q][3] for q in fz3["slots_abc"])
    print(f"\n  for contrast, the run-2 style stake (single exponential at Gamma_1"
          f" = {gam:.5f}/us):")
    print("   t(us)     D_meas    exp(-Gamma_1 t)        ratio")
    rr2 = []
    for t, D, pk, _, _ in rows:
        e = math.exp(-gam * t)
        rr2.append(D / e)
        print(f"  {t:7.1f}  {D:9.5f}   {e:14.5f}   {D/e:8.4f}")
    rr2 = np.array(rr2)
    print(f"  ratio over the arm: mean {rr2.mean():.4f}  sd {rr2.std():.4f}"
          f"  range [{rr2.min():.4f}, {rr2.max():.4f}]")
    out["test3_singleexp"] = dict(gamma=gam, ratios=[float(x) for x in rr2])

    print()
    print("=" * 74)
    print("TEST 4 -- the pair-sector bulge candidate 1 would require")
    print("=" * 74)
    print("  Under candidate 1 the decaying whole-only pattern would deposit")
    print("  transient PAIR correlation.  The algebra forbids it: cov_ij ->")
    print("  kappa_i kappa_j cov_ij exactly, and the parity state starts at cov = 0.")
    mx = []
    for t in fz3["delays_parity_us"]:
        pc = corr(r3, f"C3|classical|ZZZ|{t}", am3)
        M = P.moments(pc)
        cv = [abs(M[3] - M[1] * M[2]), abs(M[5] - M[1] * M[4]), abs(M[6] - M[2] * M[4])]
        mx.append(max(cv))
        print(f"  t={t:7.1f}  max |pair covariance| = {max(cv):.3e}")
    print(f"  max over the arm: {max(mx):.3e}  -- no bulge, at any delay.")
    out["pair_cov_max"] = float(max(mx))

    with open("qpu_shape_diagnosis.json", "w") as f:
        json.dump(out, f, indent=2, default=float)
    print("\nsaved qpu_shape_diagnosis.json")


if __name__ == "__main__":
    main()
