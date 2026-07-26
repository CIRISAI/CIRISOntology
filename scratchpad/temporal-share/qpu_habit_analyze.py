#!/usr/bin/env python3
"""Analysis for the QPU habit-lifecycle jobs, per QPU_HABIT_PREREG.md.

Every rule here is the pre-registered one; nothing is chosen after the data.

Usage: qenv/bin/python qpu_habit_analyze.py qpu_habit_A_<jobid>.json [n_mc]
       qenv/bin/python qpu_habit_analyze.py qpu_habit_B_<jobid>.json
"""
import json
import math
import sys

import numpy as np

import qpu_habit_pipeline as P
import qpu_habit_bands as B

LN2 = math.log(2.0)
RNG = np.random.default_rng(161803)


def load(path):
    with open(path) as f:
        return json.load(f)


def parse(records):
    out = {}
    for r in records:
        out[r["tag"]] = r
    return out


def arm_p(rec):
    return P.counts_to_p(rec["counts"])


def analyze_A(data, n_mc=300):
    fz = data["freeze"]
    recs = parse(data["records"])
    amats = P.assignment_matrices(arm_p(recs["A8|cal|000|0"]).ravel(),
                                  arm_p(recs["A8|cal|111|0"]).ravel())
    ro_fid = float(min(min(A[0, 0], A[1, 1]) for A in amats))
    print(f"readout assignment fidelity (min) = {ro_fid:.4f}  "
          f"[{'ok' if ro_fid >= 0.95 else 'VOID'}]")

    def corr(p):
        pc = P.correct_readout(p, amats)
        pc = np.clip(pc, 0, None)
        return pc / pc.sum()

    res = {"readout_fid_min": ro_fid, "readout_ok": ro_fid >= 0.95}

    # ---------------- A7: the in-job T1 audit (the primary anchor) ----------
    ts7 = fz["delays_t1_us"]
    p1 = [[], [], []]
    for t in ts7:
        pc = corr(arm_p(recs[f"A7|exc|ZZZ|{t}"]))
        p1[0].append(float(pc.sum(axis=(1, 2))[1]))
        p1[1].append(float(pc.sum(axis=(0, 2))[1]))
        p1[2].append(float(pc.sum(axis=(0, 1))[1]))
    fits = [P.fit_T1(ts7, p1[s]) for s in range(3)]
    T1hat = [f["T1"] for f in fits]
    pexc = [max(f["p_exc"], 1e-4) for f in fits]
    gam = sum(1.0 / x for x in T1hat)
    T1pub = [fz["cal"]["T1_us"][str(q)] for q in fz["slots_abc"]]
    gam_pub = sum(1.0 / x for x in T1pub)
    print("\n=== A7 in-job T1 audit (the parameter-free anchor) ===")
    for s in range(3):
        print(f"  slot {s} (q{fz['slots_abc'][s]}): T1 = {T1hat[s]:7.2f} "
              f"+- {fits[s].get('T1_err', float('nan')):5.2f} us   "
              f"(published {T1pub[s]:7.2f}, drift {100*(T1hat[s]/T1pub[s]-1):+6.1f} %)"
              f"   p_exc = {fits[s]['p_exc']:.4f}")
    print(f"  Gamma_1 in-job {gam:.6f} /us   published {gam_pub:.6f} /us "
          f"({100*(gam/gam_pub-1):+.1f} %)")
    res["T1_injob"] = T1hat
    res["T1_published"] = T1pub
    res["p_exc_injob"] = pexc
    res["gamma_injob"] = gam
    res["gamma_published"] = gam_pub
    res["T1_range_ok"] = all(50 < x < 800 for x in T1hat)

    # ---------------- the noisy-model expectation AT the in-job anchor ------
    def true_cl(t):
        k, b = P.damping_channel(t, T1hat, pexc)
        return P.dist_from_moments(P.apply_product_channel(B.M_PARITY, k, b))

    dC = fz["delays_classical_us"]
    mc = B.mc_arm(true_cl, dC, fz["shots"]["A1"], n_mc, fz["shots"]["A8"], RNG)
    mu = mc["sh_cor"].mean(axis=0); sd = mc["sh_cor"].std(axis=0)
    floor = mc["floor"].mean(axis=0)
    dmu = np.abs(mc["d_cor"]).mean(axis=0); dsd = np.abs(mc["d_cor"]).std(axis=0)

    print("\n=== A1: the classical habit's unpaid decay (THE KILL LEG) ===")
    print("   t(us)   share_raw  share_corr   model    +-sd     z      D_meas   D_model")
    sh_meas, d_meas, sh_raw = [], [], []
    for i, t in enumerate(dC):
        p = arm_p(recs[f"A1|classical|ZZZ|{t}"])
        pc = corr(p)
        s_r, s_c, D = P.share(p), P.share(pc), P.D_stat(pc)
        sh_raw.append(s_r); sh_meas.append(s_c); d_meas.append(D)
        z = (s_c - mu[i]) / max(sd[i], 1e-12)
        print(f"  {t:7.1f}  {s_r:9.5f}  {s_c:9.5f}  {mu[i]:8.5f} {sd[i]:8.5f} "
              f"{z:+6.2f}  {D:8.5f}  {mc['D_true'][i]:8.5f}")
    sh_meas = np.array(sh_meas); d_meas = np.array(d_meas)
    res["A1"] = dict(t=dC, share_raw=[float(x) for x in sh_raw],
                     share_corr=[float(x) for x in sh_meas],
                     D=[float(x) for x in d_meas],
                     model_mean=[float(x) for x in mu],
                     model_sd=[float(x) for x in sd],
                     model_D=[float(x) for x in mc["D_true"]],
                     floor=[float(x) for x in floor])

    # K-SHAPE
    chi2 = float(np.sum(((sh_meas - mu) / sd) ** 2))
    res["chi2"] = chi2
    # PRE-REGISTERED FIT-POINT RULE: SNR >= 5 against the noisy model, which
    # must be evaluated at the IN-JOB anchor (the frozen-calibration statement
    # that all nine points would clear it was a prediction, and it can fail).
    snr = (mu - floor) / np.maximum(sd, 1e-12)
    idx = [i for i in range(len(dC)) if snr[i] >= 5.0]
    print(f"\n  SNR at the in-job anchor: {[round(float(x),1) for x in snr]}")
    print(f"  pre-registered fit points (SNR>=5): {[dC[i] for i in idx]}")
    res["snr_injob"] = [float(x) for x in snr]
    res["fit_idx"] = idx
    t = np.array(dC, float)
    sig_log = np.std(np.clip(mc["sh_cor"] - floor, 1e-12, None), axis=0) / \
        np.maximum(np.mean(np.clip(mc["sh_cor"] - floor, 1e-12, None), axis=0), 1e-12)
    sig_logd = dsd / np.maximum(dmu, 1e-12)
    y = np.clip(sh_meas - floor, 1e-9, None)
    ti = t[idx]
    rate_s, rate_s_sd = P.wls_logfit(ti, y[idx], sig_log[idx])
    rate_d, rate_d_sd = P.wls_logfit(ti, np.clip(np.abs(d_meas[idx]), 1e-9, None),
                                     sig_logd[idx])
    R_D = rate_d / gam
    R_S = rate_s / (2 * gam)
    print(f"\n  fitted rate of |D|   : {rate_d:.6f} +- {rate_d_sd:.6f} /us")
    print(f"  Gamma_1 (in-job A7)  : {gam:.6f} /us")
    print(f"  R_D = rate_D/Gamma_1 : {R_D:.4f}      <-- prediction 1, zero free parameters")
    print(f"  R_S = rate_S/2Gamma_1: {R_S:.4f}")
    # K-SHAPE proper: chi2 of log|D| against slope FIXED at -Gamma_1
    ly = np.log(np.clip(np.abs(d_meas[idx]), 1e-12, None))
    w = 1.0 / sig_logd[idx] ** 2
    c0 = float(np.sum(w * (ly + gam * ti)) / np.sum(w))
    chi2_fixed = float(np.sum(w * (ly - (c0 - gam * ti)) ** 2))
    print(f"  K-SHAPE chi2 (slope fixed at -Gamma_1, dof {len(idx)-1}): {chi2_fixed:.2f}"
          f"   [c0 = {math.exp(c0):.4f}]")
    res.update(rate_D=rate_d, rate_D_sd=rate_d_sd, rate_S=rate_s,
               R_D=R_D, R_S=R_S, chi2_shape_fixed=chi2_fixed,
               c0=float(math.exp(c0)), chi2_shape_dof=len(idx) - 1)

    # K-FAMILY: exponential vs power law on |D| (D is predicted EXACTLY
    # exponential, with no transient, so the family test is well posed there)
    from scipy.optimize import curve_fit
    w = 1.0 / np.maximum(dsd[idx], 1e-9)
    yy = np.abs(d_meas[idx])
    t = ti
    try:
        pe, _ = curve_fit(lambda x, A, r: A * np.exp(-r * x), t, yy,
                          p0=[1.0, gam], sigma=1 / w, maxfev=40000)
        rese = yy - pe[0] * np.exp(-pe[1] * t)
        pp, _ = curve_fit(lambda x, A, tau, al: A * (1 + x / tau) ** (-al), t, yy,
                          p0=[1.0, 50.0, 2.0], sigma=1 / w, maxfev=40000,
                          bounds=([0, 1e-2, 1e-3], [10, 1e5, 50]))
        resp = yy - pp[0] * (1 + t / pp[1]) ** (-pp[2])
        n = len(t)
        chi_e = float(np.sum((rese * w) ** 2)); chi_p = float(np.sum((resp * w) ** 2))
        aic_e = chi_e + 2 * 2; aic_p = chi_p + 2 * 3
        print(f"  family test on |D|: chi2 exp {chi_e:.2f} (k=2) vs power law "
              f"{chi_p:.2f} (k=3)   dAIC(exp-pow) = {aic_e-aic_p:+.2f}")
        res["family"] = dict(chi2_exp=chi_e, chi2_pow=chi_p,
                             dAIC_exp_minus_pow=float(aic_e - aic_p),
                             exp_params=[float(x) for x in pe],
                             pow_params=[float(x) for x in pp])
    except Exception as e:
        res["family"] = {"error": str(e)}
        print("  family test failed:", e)

    # ---------------- A2/A3: the quantum habit -----------------------------
    print("\n=== A2/A3: the quantum habit (GHZ, X basis) ===")
    dQ = fz["delays_quantum_us"]
    T2pub = [fz["cal"]["T2_us"][str(q)] for q in fz["slots_abc"]]

    def true_q(t):
        D = math.exp(-t * sum(1.0 / x for x in T2pub))
        M = np.zeros(8); M[0] = 1.0; M[7] = D
        return P.dist_from_moments(M)

    mcq = B.mc_arm(true_q, dQ, fz["shots"]["A2"], max(60, n_mc // 3),
                   fz["shots"]["A8"], RNG)
    muq = mcq["sh_cor"].mean(axis=0); sdq = mcq["sh_cor"].std(axis=0)
    print("   t(us)   share_X   share_Y   |rho|-share  model    +-sd")
    shq, shy, shr = [], [], []
    for i, t in enumerate(dQ):
        px = corr(arm_p(recs[f"A2|ghz|XXX|{t}"]))
        py = corr(arm_p(recs[f"A3|ghz|YXX|{t}"]))
        sx, sy = P.share(px), P.share(py)
        Dx, Dy = P.D_stat(px), P.D_stat(py)
        Dmag = math.hypot(Dx, Dy)
        sr = P.f_of_D(Dmag)
        shq.append(sx); shy.append(sy); shr.append(sr)
        print(f"  {t:7.1f}  {sx:8.5f}  {sy:8.5f}  {sr:10.5f}  {muq[i]:8.5f} {sdq[i]:8.5f}"
              f"   (D_X {Dx:+.4f}, D_Y {Dy:+.4f})")
    res["A2"] = dict(t=dQ, share_X=[float(x) for x in shq],
                     share_Y=[float(x) for x in shy],
                     share_phasetracked=[float(x) for x in shr],
                     model_mean=[float(x) for x in muq],
                     model_sd=[float(x) for x in sdq])
    idxq = [i for i in range(len(dQ)) if muq[i] > 5 * mcq["floor"].mean(axis=0)[i]]
    if len(idxq) >= 3:
        tq = np.array([dQ[i] for i in idxq])
        yq = np.clip(np.array([shr[i] for i in idxq]), 1e-9, None)
        sg = (sdq[idxq] / np.maximum(muq[idxq], 1e-12))
        rq, rq_sd = P.wls_logfit(tq, yq, sg)
        gam2 = sum(1.0 / x for x in T2pub)
        print(f"  fitted quantum share rate {rq:.5f} /us   vs published 2*sum(1/T2) "
              f"= {2*gam2:.5f}   ratio {rq/(2*gam2):.3f}")
        res["quantum_rate"] = dict(fitted=rq, predicted=2 * gam2,
                                   ratio=rq / (2 * gam2))
        rcl = res["rate_S"]
        print(f"\n  TWO-SECTOR ORDERING (measured): quantum share rate {rq:.5f} /us "
              f"vs classical {rcl:.5f} /us  -> ratio {rq/rcl:.2f}")
        res["ordering_measured"] = dict(quantum=rq, classical=rcl, ratio=rq / rcl)

    # ---------------- A4 ferro cross-check ---------------------------------
    print("\n=== A4: the ferro habit in Z (channel cross-check) ===")

    def true_f(t):
        k, b = P.damping_channel(t, T1hat, pexc)
        return P.dist_from_moments(P.apply_product_channel(B.M_FERRO, k, b))

    a4 = []
    for t in fz["delays_control_us"]:
        pc = corr(arm_p(recs[f"A4|ghz|ZZZ|{t}"]))
        pred = true_f(t)
        a4.append(dict(t=t, share=float(P.share(pc)), S_total=float(P.s_total(pc)),
                       share_pred=float(P.share(pred)),
                       S_total_pred=float(P.s_total(pred))))
        print(f"  t={t:7.1f}  share {P.share(pc):8.5f} (predicted {P.share(pred):8.5f})"
              f"   S_total {P.s_total(pc):8.5f} (predicted {P.s_total(pred):8.5f})")
    res["A4"] = a4

    # ---------------- null controls ----------------------------------------
    print("\n=== null controls (predicted 0 at every delay) ===")
    nulls = {}
    for tag in sorted(recs):
        if tag.startswith(("A5", "A6", "A7")):
            pc = corr(arm_p(recs[tag]))
            nulls[tag] = float(P.share(pc))
            print(f"  {tag:26s} share = {P.share(pc):.3e}")
    res["nulls"] = nulls
    res["null_max"] = float(max(nulls.values()))

    # ---------------- the 2x2 table ----------------------------------------
    print("\n=== the 2x2 table at t=0: prep x basis ===")
    z0 = fz["delays_classical_us"][0]; q0 = fz["delays_quantum_us"][0]
    c0 = fz["delays_control_us"][0]
    tbl = {
        "classical/Z": float(P.share(corr(arm_p(recs[f"A1|classical|ZZZ|{z0}"])))),
        "classical/X": float(P.share(corr(arm_p(recs[f"A5|classical|XXX|{c0}"])))),
        "ghz/X": float(P.share(corr(arm_p(recs[f"A2|ghz|XXX|{q0}"])))),
        "ghz/Z": float(P.share(corr(arm_p(recs[f"A4|ghz|ZZZ|{c0}"])))),
    }
    for k, v in tbl.items():
        print(f"  {k:14s} {v:9.5f}   (ideal {LN2 if k in ('classical/Z','ghz/X') else 0.0:.5f})")
    res["table_2x2"] = tbl
    return res


def analyze_B(data):
    fz = data["freeze"]
    recs = parse(data["records"])
    amats = P.assignment_matrices(arm_p(recs["B3|cal|000|0"]).ravel(),
                                  arm_p(recs["B3|cal|111|0"]).ravel())
    ro_fid = float(min(min(A[0, 0], A[1, 1]) for A in amats))

    def corr(p):
        pc = P.correct_readout(p, amats)
        pc = np.clip(pc, 0, None)
        return pc / pc.sum()

    res = {"readout_fid_min": ro_fid, "readout_ok": ro_fid >= 0.95, "arms": {}}
    print(f"readout assignment fidelity (min) = {ro_fid:.4f}")
    print("\n=== JOB B: mint, wrong code, and the false-positive floor ===")
    for kind in ("parity", "copy", "none"):
        r = recs[f"B1|mint|{kind}|0"]
        p_out = corr(arm_p(r))
        row = dict(share_out=float(P.share(p_out)), S_total_out=float(P.s_total(p_out)),
                   share_out_raw=float(P.share(arm_p(r))))
        if "counts_m" in r:
            p_in = corr(P.counts_to_p(r["counts_m"]))
            row["share_in"] = float(P.share(p_in))
            row["S_total_in"] = float(P.s_total(p_in))
        if "counts_joint_c_m" in r:
            ok = tot = 0
            for k, v in r["counts_joint_c_m"].items():
                cbits, mbits = k.split("|")
                # register strings are little-endian: slot s = char [-1-s]
                c_slots = [int(cbits.replace(" ", "")[-1 - s]) for s in range(3)]
                m_slots = [int(mbits.replace(" ", "")[-1 - s]) for s in range(3)]
                tot += v
                if kind == "parity" and c_slots[2] == (m_slots[0] ^ m_slots[1]):
                    ok += v
                elif kind == "copy" and c_slots[2] == m_slots[0]:
                    ok += v
                elif kind == "none" and c_slots == m_slots:
                    ok += v
            row["per_shot_theorem_fraction"] = ok / max(tot, 1)
        res["arms"][kind] = row
        print(f"  {kind:7s}: in share {row.get('share_in', float('nan')):8.5f} "
              f"-> out share {row['share_out']:8.5f}  (raw {row['share_out_raw']:8.5f})"
              f"  S_total {row['S_total_out']:8.5f}"
              f"  per-shot map held on {100*row.get('per_shot_theorem_fraction', float('nan')):.2f} % of shots")

    print("\n=== JOB B: rent vs default — share retained per bit erased ===")
    print("   T(us)  cycles  bits erased   share_corr   S_total    share_raw")
    rows = []
    for T in fz["rent_totals_us"]:
        for n in fz["rent_cycles"]:
            r = recs[f"B2|rent|{n}|{T}"]
            pc = corr(arm_p(r))
            row = dict(T=T, n=n, bits_erased=n, share=float(P.share(pc)),
                       S_total=float(P.s_total(pc)),
                       share_raw=float(P.share(arm_p(r))))
            rows.append(row)
            print(f"  {T:6.1f}  {n:5d}  {n:11d}   {row['share']:10.5f}  "
                  f"{row['S_total']:8.5f}  {row['share_raw']:9.5f}")
    res["rent"] = rows
    for T in fz["rent_totals_us"]:
        paid = [r for r in rows if r["T"] == T and r["n"] >= 1]
        unpaid = [r for r in rows if r["T"] == T and r["n"] == 0][0]
        best = max(paid, key=lambda r: r["share"])
        print(f"  T={T:6.1f}us: paid(n=1) {paid[0]['share']:.5f} vs unpaid "
              f"{unpaid['share']:.5f}  ->  {paid[0]['share']/max(unpaid['share'],1e-9):.1f}x"
              f"   ; spread over n=1,2,4: "
              f"{max(r['share'] for r in paid)-min(r['share'] for r in paid):.5f}")
    return res


def main():
    path = sys.argv[1]
    n_mc = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    data = load(path)
    which = data["which"]
    res = analyze_A(data, n_mc) if which == "A" else analyze_B(data)
    out = path.replace("qpu_habit_", "qpu_verdict_")
    with open(out, "w") as f:
        json.dump(res, f, indent=2, default=float)
    print("\nsaved", out)


if __name__ == "__main__":
    main()
