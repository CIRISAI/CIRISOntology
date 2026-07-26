#!/usr/bin/env python3
"""Run-3 analysis: the sector-flow dichotomy, per QPU_HABIT_PREREG.md addendum 2.
Every rule is the pre-registered one.

Usage: qenv/bin/python qpu_sector_analyze.py qpu_habit_C_<jobid>.json
"""
import json
import math
import sys

import numpy as np

import qpu_habit_pipeline as P
from qpu_sector_bands import M_FERRO, M_PARITY, pair_cov, pair_mi

BAND = json.load(open("qpu_sector_bands.json"))


def main():
    path = sys.argv[1]
    data = json.load(open(path))
    fz = data["freeze"]
    recs = {r["tag"]: r for r in data["records"]}
    sets = []
    for pre in ("C9", "C0"):
        sets.append(P.assignment_matrices(
            P.counts_to_p(recs[f"{pre}|cal|000|0"]["counts"]).ravel(),
            P.counts_to_p(recs[f"{pre}|cal|111|0"]["counts"]).ravel()))
    amats = [(sets[0][q] + sets[1][q]) / 2 for q in range(3)]
    ro_fid = float(min(min(A[0, 0], A[1, 1]) for A in amats))
    drift = float(max(np.abs(sets[0][q] - sets[1][q]).max() for q in range(3)))
    print(f"readout fidelity {ro_fid:.4f} (floor 0.95)   drift across job {drift:.4f}"
          f" (ceiling 0.02)   [{'ok' if ro_fid >= .95 and drift <= .02 else 'VOID'}]")

    def corr(tag):
        pc = P.correct_readout(P.counts_to_p(recs[tag]["counts"]), amats)
        pc = np.clip(pc, 0, None)
        return pc / pc.sum()

    res = {"readout_fid": ro_fid, "drift": drift, "void": not (ro_fid >= .95 and drift <= .02)}
    dF = fz["delays_ferro_us"]
    pexc_nom = fz["p_exc_nominal"]

    # ---- C2 audit: kappa_q(t) measured DIRECTLY on C1's grid, no model ------
    sat = fz["delays_sat_us"]
    p1_sat = []
    for t in sat:
        pc = corr(f"C2|exc|ZZZ|{t}")
        p1_sat.append([float(pc.sum(axis=tuple(x for x in range(3) if x != q))[1])
                       for q in range(3)])
    pexc = [min(p1_sat[-1][q], 0.2) for q in range(3)]
    print(f"\nC2 audit: p_exc from saturation at t={sat[-1]:.0f} us: "
          f"{[round(x,4) for x in pexc]}  (nominal {pexc_nom})")
    kap = np.zeros((len(dF), 3))
    for i, t in enumerate(dF):
        pc = corr(f"C2|exc|ZZZ|{t}")
        for q in range(3):
            p1 = float(pc.sum(axis=tuple(x for x in range(3) if x != q))[1])
            kap[i, q] = (p1 - pexc[q]) / (1 - pexc[q])
    res["kappa"] = kap.tolist()

    # ---- C1 ferro: the bulge, against the curve built from measured kappa ---
    print("\n=== C1 FERRO — the whole-only bulge fed by a decaying pair habit ===")
    print("   t(us)   share_raw  share_corr    predicted   model   +-sd     z"
          "     pair cov (measured)         cov/(k_i k_j cov0)")
    sh, pred, covs, ratios = [], [], [], []
    cov0 = None
    for i, t in enumerate(dF):
        p = P.counts_to_p(recs[f"C1|ferro|ZZZ|{t}"]["counts"])
        pc = corr(f"C1|ferro|ZZZ|{t}")
        s = P.share(pc); sh.append(s)
        k = np.clip(kap[i], 0, 1.5)
        b = (1 - k) * np.array([1 - 2 * x for x in pexc])
        pr = P.share(P.dist_from_moments(P.apply_product_channel(M_FERRO, k, b)))
        pred.append(pr)
        cv = pair_cov(pc); covs.append(cv)
        if cov0 is None:
            cov0 = cv
        rr = []
        for j, (u, v) in enumerate(((0, 1), (0, 2), (1, 2))):
            d = k[u] * k[v] * cov0[j]
            rr.append(cv[j] / d if abs(d) > 1e-6 else float("nan"))
        ratios.append(rr)
        sdm = BAND["ferro_sim_sd"][i]
        print(f"  {t:7.1f}  {P.share(p):9.5f}  {s:9.5f}   {pr:9.5f} "
              f"{BAND['ferro_model'][i]:8.5f} {sdm:7.5f} {(s-pr)/max(sdm,1e-9):+6.2f}"
              f"   {[round(float(x),4) for x in cv]}   {[round(float(x),3) for x in rr]}")
    sh = np.array(sh); pred = np.array(pred)
    sdv = np.array(BAND["ferro_sim_sd"])
    chi2 = float(np.sum(((sh - pred) / sdv) ** 2))
    jpk = int(np.argmax(sh))
    print(f"\n  K-CURVE   chi2 = {chi2:.2f}  (dof 12, ZERO free parameters)"
          f"   staked <= {BAND['K_CURVE_chi2']['p99']:.2f}"
          f"   [{'PASS' if chi2 <= BAND['K_CURVE_chi2']['p99'] else 'FAIL'}]")
    ok_t = dF[jpk] in BAND["K_PEAK_t"]["support"]
    print(f"  K-PEAK-t  peak at {dF[jpk]:.1f} us   staked in "
          f"{[round(x,1) for x in BAND['K_PEAK_t']['support']]}"
          f"   [{'PASS' if ok_t else 'FAIL'}]")
    lo, hi = BAND["K_PEAK_h"]["p005"], BAND["K_PEAK_h"]["p995"]
    print(f"  K-PEAK-h  height {sh[jpk]:.5f}   staked [{lo:.5f}, {hi:.5f}]"
          f"   [{'PASS' if lo <= sh[jpk] <= hi else 'FAIL'}]")
    rr = np.array(ratios)[1:]
    rlo, rhi = BAND["K_PAIRMULT"]["p005"], BAND["K_PAIRMULT"]["p995"]
    inb = np.nanmin(rr) >= rlo and np.nanmax(rr) <= rhi
    rise = max(max(c[j] for j in range(3)) - cov0[j] for j, c in
               [(j, c) for c in covs for j in range(3)]) if False else \
        max(max(c[j] - cov0[j] for j in range(3)) for c in covs)
    print(f"  K-PAIRMULT ratio range [{np.nanmin(rr):.3f}, {np.nanmax(rr):.3f}]"
          f"   staked [{rlo:.3f}, {rhi:.3f}]   [{'PASS' if inb else 'FAIL'}]")
    print(f"             max rise of any pair cov above its t=0 value: {rise:+.4f}"
          f"   [{'PASS' if rise <= 0.02 else 'FAIL'}]")
    res.update(ferro_share=sh.tolist(), ferro_pred=pred.tolist(),
               ferro_cov=[[float(x) for x in c] for c in covs],
               K_CURVE=chi2, K_PEAK_t=dF[jpk], K_PEAK_h=float(sh[jpk]),
               K_PAIRMULT=[float(np.nanmin(rr)), float(np.nanmax(rr))],
               pair_cov_max_rise=float(rise))

    # ---- C3 parity: the pair sector must stay at exactly zero --------------
    print("\n=== C3 PARITY — no downward cascade: pairs must stay exactly independent ===")
    print("   t(us)    share      max pair MI      pair MI per pair")
    mis = []
    for t in fz["delays_parity_us"]:
        pc = corr(f"C3|classical|ZZZ|{t}")
        mi = pair_mi(pc); mis.append(max(mi))
        print(f"  {t:7.1f}  {P.share(pc):9.5f}   {max(mi):.3e}    "
              f"{['%.2e' % x for x in mi]}")
    thr = BAND["K_PAIRZERO_p999"]
    print(f"  K-PAIRZERO max over arm = {max(mis):.3e}   staked <= {thr:.3e}"
          f"   [{'PASS' if max(mis) <= thr else 'FAIL'}]")
    res["parity_max_pair_mi"] = float(max(mis))

    # ---- C4 / C5 the background-free nulls ---------------------------------
    print("\n=== C4 / C5 — the background-free nulls ===")
    n4 = [P.share(corr(f"C4|product|ZZZ|{t}")) for t in fz["delays_product_us"]]
    n5 = [P.share(corr(f"C5|plus|XXX|{t}")) for t in fz["delays_plus_us"]]
    print(f"  C4 product/Z shares: {['%.3e' % x for x in n4]}")
    print(f"     max {max(n4):.3e}  staked <= {BAND['nulls']['product/Z']['p999']:.3e}"
          f"   [{'PASS' if max(n4) <= BAND['nulls']['product/Z']['p999'] else 'FAIL'}]")
    print(f"  C5 plus/X shares:    {['%.3e' % x for x in n5]}")
    print(f"     max {max(n5):.3e}  staked <= {BAND['nulls']['plus/X']['p999']:.3e}"
          f"   [{'PASS' if max(n5) <= BAND['nulls']['plus/X']['p999'] else 'FAIL'}]")
    res["null_product"] = [float(x) for x in n4]
    res["null_plus"] = [float(x) for x in n5]
    with open(path.replace("qpu_habit_", "qpu_sector_verdict_"), "w") as f:
        json.dump(res, f, indent=2)
    print("\nsaved", path.replace("qpu_habit_", "qpu_sector_verdict_"))


if __name__ == "__main__":
    main()
