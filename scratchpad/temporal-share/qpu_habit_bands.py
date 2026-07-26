#!/usr/bin/env python3
"""Derive EVERY pre-registered band for QPU_HABIT_PREREG.md from the noisy
model, before any hardware job.  Run-1 lesson (HW_RESULTS.md): never stake a
criterion the noisy device cannot meet — the band comes from the noisy model,
never from the ideal.

The idle arms need no Aer: the physics is exactly an independent asymmetric
bit-flip channel per qubit (amplitude damping / dephasing), which acts on the
Z-moments as z_q -> kappa_q z_q + b_q.  That map is implemented exactly in
qpu_habit_pipeline.apply_product_channel, so the "noisy simulation" of the idle
arms IS the analytic channel plus multinomial shot noise plus the readout
channel plus the readout correction — every step of the real pipeline.

Usage: qenv/bin/python qpu_habit_bands.py [n_mc]
"""
import itertools
import json
import math
import sys

import numpy as np

import os
import qpu_habit_pipeline as P
BOUT = "%s%s.json" % ("qpu_habit_bands", "_v2" if "freeze2" in os.environ.get("QPU_FREEZE","") else "")

LN2 = math.log(2.0)
RNG = np.random.default_rng(31415926)
fz = P.load_freeze()
# nominal residual excited-state population; run 1 fitted 0.025-0.065 in-job
P_EXC = fz.get("p_exc_nominal", 0.01)
SL = fz["slots_abc"]                       # [a, b, c]
T1 = [fz["cal"]["T1_us"][str(q)] for q in SL]
T2 = [fz["cal"]["T2_us"][str(q)] for q in SL]
E0 = [fz["cal"]["prob_meas1_prep0"][str(q)] for q in SL]
E1 = [fz["cal"]["prob_meas0_prep1"][str(q)] for q in SL]
RO_K, RO_B = P.readout_channel(E0, E1)

M_PARITY = np.zeros(8); M_PARITY[0] = 1.0; M_PARITY[7] = 1.0
# ferro (the Z-basis reading of GHZ): every PAIR moment is 1, the triple is 0
M_FERRO = np.array([1.0, 0, 0, 1.0, 0, 1.0, 1.0, 0])


def true_classical(t):
    """Z-basis distribution of the classical parity habit after idling t."""
    k, b = P.damping_channel(t, T1, [P_EXC] * 3)
    return P.dist_from_moments(P.apply_product_channel(M_PARITY, k, b))


def true_ferro(t):
    """Z-basis distribution of the GHZ prep (= the ferro habit) after idling t.

    NOT a null arm: the gate showed that damping a sign-symmetric habit MINTS
    whole-only share (the surviving |000> and the decaying |111> make a
    mixture of products, which generically carries some).  Its exact curve is a
    second, independent test of the same channel on a different initial state.
    """
    k, b = P.damping_channel(t, T1, [P_EXC] * 3)
    return P.dist_from_moments(P.apply_product_channel(M_FERRO, k, b))


def true_quantum(t):
    """X-basis distribution of the GHZ habit after idling t: uniform marginals,
    3-body coherence contracted by exp(-t/T2) per qubit."""
    D = math.exp(-t * sum(1.0 / x for x in T2))
    M = np.zeros(8); M[0] = 1.0; M[7] = D
    return P.dist_from_moments(M)


def measured(p):
    """Apply the readout channel to a true distribution."""
    return P.dist_from_moments(P.apply_product_channel(P.moments(p), RO_K, RO_B))


def sim_cal(shots, rng):
    """Simulated readout-calibration circuits -> assignment matrices."""
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
        p = P.dist_from_moments(P.apply_product_channel(M, RO_K, RO_B))
        p = np.clip(p.ravel(), 0, None); p = p / p.sum()
        out.append(rng.multinomial(shots, p) / shots)
    return P.assignment_matrices(out[0], out[1])


def mc_arm(true_fn, delays, shots, n_mc, cal_shots, rng):
    """Full pipeline Monte Carlo.  Returns per-delay stats and the rate-fit
    distribution, exactly as the hardware analysis will compute them."""
    ptrue = [true_fn(t) for t in delays]
    pmeas = [np.clip(measured(p).ravel(), 0, None) for p in ptrue]
    pmeas = [p / p.sum() for p in pmeas]
    sh_raw = np.zeros((n_mc, len(delays)))
    sh_cor = np.zeros((n_mc, len(delays)))
    d_cor = np.zeros((n_mc, len(delays)))
    fl_cor = np.zeros((n_mc, len(delays)))
    for r in range(n_mc):
        amats = sim_cal(cal_shots, rng)
        for i, pm in enumerate(pmeas):
            c = rng.multinomial(shots, pm) / shots
            pr = c.reshape(2, 2, 2)
            sh_raw[r, i] = P.share(pr)
            pc = P.correct_readout(pr, amats)
            pc = np.clip(pc, 0, None); pc = pc / pc.sum()
            sh_cor[r, i] = P.share(pc)
            d_cor[r, i] = P.D_stat(pc)
            # matched independent surrogate floor, ONE draw per replicate
            m = [pc.sum(axis=(1, 2)), pc.sum(axis=(0, 2)), pc.sum(axis=(0, 1))]
            prod = np.einsum('i,j,k->ijk', *m).ravel()
            prod = np.clip(prod, 0, None); prod = prod / prod.sum()
            fl_cor[r, i] = P.share(rng.multinomial(shots, prod) / shots)
    truth = np.array([P.share(p) for p in ptrue])
    return dict(delays=delays, truth=truth, sh_raw=sh_raw, sh_cor=sh_cor,
                d_cor=d_cor, floor=fl_cor,
                D_true=np.array([P.D_stat(p) for p in ptrue]))


def rate_fits(res, idx, expected_rate):
    """Weighted log-linear fit of floor-subtracted share, and of |D|, on the
    pre-registered point set `idx`.  Returns the two rate-ratio samples."""
    t = np.array([res["delays"][i] for i in idx], float)
    floor_mean = res["floor"].mean(axis=0)
    Rs, Rd = [], []
    n_mc = res["sh_cor"].shape[0]
    s_sd = np.std(np.clip(res["sh_cor"][:, idx] - floor_mean[idx], 1e-12, None), axis=0)
    y_mean = np.mean(np.clip(res["sh_cor"][:, idx] - floor_mean[idx], 1e-12, None), axis=0)
    sig_log = s_sd / np.maximum(y_mean, 1e-12)
    d_sd = np.std(np.abs(res["d_cor"][:, idx]), axis=0)
    d_mean = np.mean(np.abs(res["d_cor"][:, idx]), axis=0)
    sig_logd = d_sd / np.maximum(d_mean, 1e-12)
    for r in range(n_mc):
        y = np.clip(res["sh_cor"][r, idx] - floor_mean[idx], 1e-9, None)
        try:
            rate, _ = P.wls_logfit(t, y, sig_log)
            Rs.append(rate / expected_rate)
        except Exception:
            pass
        d = np.clip(np.abs(res["d_cor"][r, idx]), 1e-9, None)
        try:
            rate, _ = P.wls_logfit(t, d, sig_logd)
            Rd.append(rate / (expected_rate / 2.0))
        except Exception:
            pass
    return np.array(Rs), np.array(Rd)


def main():
    n_mc = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    out = {"n_mc": n_mc, "p_exc_nominal": P_EXC}
    rate_cl = fz["predicted_rate_classical_per_us"]
    rate_q = fz["predicted_rate_quantum_per_us"]

    print("=== ARM A1: classical parity habit, Z basis (THE KILL LEG) ===")
    dC = fz["delays_classical_us"]
    res = mc_arm(true_classical, dC, fz["shots"]["A1"], n_mc, fz["shots"]["A8"], RNG)
    rows = []
    for i, t in enumerate(dC):
        fm, fs = res["floor"][:, i].mean(), res["floor"][:, i].std()
        sm, ss = res["sh_cor"][:, i].mean(), res["sh_cor"][:, i].std()
        snr = (sm - fm) / max(ss, 1e-12)
        rows.append(dict(t=t, truth=float(res["truth"][i]), sim_mean=float(sm),
                         sim_sd=float(ss), floor_mean=float(fm), floor_sd=float(fs),
                         snr=float(snr), D_true=float(res["D_true"][i]),
                         D_sd=float(res["d_cor"][:, i].std())))
        print(f"  t={t:6.1f}us  true={res['truth'][i]:.5f}  sim={sm:.5f}+-{ss:.5f}"
              f"  floor={fm:.2e}+-{fs:.1e}  SNR={snr:6.1f}  D={res['D_true'][i]:.4f}")
    out["A1_points"] = rows
    idx = [i for i, r in enumerate(rows) if r["snr"] >= 5.0]
    print("  fit points (SNR>=5):", [dC[i] for i in idx])
    Rs, Rd = rate_fits(res, idx, rate_cl)
    out["A1_fit_idx"] = idx
    out["A1_R_share"] = dict(mean=float(Rs.mean()), sd=float(Rs.std()),
                             p01=float(np.quantile(Rs, 0.01)), p99=float(np.quantile(Rs, 0.99)),
                             p001=float(np.quantile(Rs, 0.001)), p999=float(np.quantile(Rs, 0.999)))
    out["A1_R_D"] = dict(mean=float(Rd.mean()), sd=float(Rd.std()),
                         p01=float(np.quantile(Rd, 0.01)), p99=float(np.quantile(Rd, 0.99)))
    print(f"  R_share (rate / 2*sum(1/T1)): mean {Rs.mean():.4f} sd {Rs.std():.4f} "
          f"[p01 {np.quantile(Rs,0.01):.4f}, p99 {np.quantile(Rs,0.99):.4f}]")
    print(f"  R_D     (rate / sum(1/T1)):   mean {Rd.mean():.4f} sd {Rd.std():.4f} "
          f"[p01 {np.quantile(Rd,0.01):.4f}, p99 {np.quantile(Rd,0.99):.4f}]")
    # chi2 of the exact-curve test
    chi2 = []
    fm = res["floor"].mean(axis=0)
    sd = res["sh_cor"].std(axis=0)
    mu = res["sh_cor"].mean(axis=0)
    for r in range(n_mc):
        chi2.append(float(np.sum(((res["sh_cor"][r] - mu) / sd) ** 2)))
    chi2 = np.array(chi2)
    out["A1_chi2"] = dict(dof=len(dC), mean=float(chi2.mean()),
                          p99=float(np.quantile(chi2, 0.99)))
    print(f"  exact-curve chi2 (dof={len(dC)}): mean {chi2.mean():.2f} "
          f"p99 {np.quantile(chi2,0.99):.2f}")

    print("\n=== ARM A2/A3: quantum GHZ habit, X basis ===")
    dQ = fz["delays_quantum_us"]
    resq = mc_arm(true_quantum, dQ, fz["shots"]["A2"], n_mc, fz["shots"]["A8"], RNG)
    rowsq = []
    for i, t in enumerate(dQ):
        fm2, sm, ss = resq["floor"][:, i].mean(), resq["sh_cor"][:, i].mean(), resq["sh_cor"][:, i].std()
        snr = (sm - fm2) / max(ss, 1e-12)
        rowsq.append(dict(t=t, truth=float(resq["truth"][i]), sim_mean=float(sm),
                          sim_sd=float(ss), floor_mean=float(fm2), snr=float(snr)))
        print(f"  t={t:6.1f}us  true={resq['truth'][i]:.5f}  sim={sm:.5f}+-{ss:.5f}"
              f"  floor={fm2:.2e}  SNR={snr:6.1f}")
    out["A2_points"] = rowsq
    idxq = [i for i, r in enumerate(rowsq) if r["snr"] >= 5.0]
    Rsq, Rdq = rate_fits(resq, idxq, rate_q)
    out["A2_fit_idx"] = idxq
    out["A2_R_share"] = dict(mean=float(Rsq.mean()), sd=float(Rsq.std()),
                             p01=float(np.quantile(Rsq, 0.01)), p99=float(np.quantile(Rsq, 0.99)))
    print("  fit points:", [dQ[i] for i in idxq])
    print(f"  R_share (rate / 2*sum(1/T2)): mean {Rsq.mean():.4f} sd {Rsq.std():.4f} "
          f"[p01 {np.quantile(Rsq,0.01):.4f}, p99 {np.quantile(Rsq,0.99):.4f}]")

    print("\n=== the two-sector ORDERING predicted by calibration ===")
    print(f"  classical share rate 2*sum(1/T1) = {rate_cl:.5f} /us  "
          f"(half-life of the entry {math.log(2)/rate_cl:.1f} us)")
    print(f"  quantum   share rate 2*sum(1/T2) = {rate_q:.5f} /us  "
          f"({math.log(2)/rate_q:.1f} us)")
    print(f"  predicted ratio quantum/classical = {rate_q/rate_cl:.3f}")
    out["ordering"] = dict(rate_classical=rate_cl, rate_quantum=rate_q,
                           ratio=rate_q / rate_cl)

    print("\n=== ARM A4: the ferro habit read in Z (channel cross-check, NOT a null) ===")
    dF = fz["delays_control_us"]
    resf = mc_arm(true_ferro, dF, fz["shots"]["A4"], max(60, n_mc // 4),
                  fz["shots"]["A8"], RNG)
    rowsf = []
    for i, t in enumerate(dF):
        sm, ss = resf["sh_cor"][:, i].mean(), resf["sh_cor"][:, i].std()
        stm = float(np.mean([P.s_total(true_ferro(t))]))
        rowsf.append(dict(t=t, truth=float(resf["truth"][i]), sim_mean=float(sm),
                          sim_sd=float(ss), S_total_true=stm))
        print(f"  t={t:6.1f}us  true share={resf['truth'][i]:.5f}  sim={sm:.5f}+-{ss:.5f}"
              f"  S_total(true)={stm:.5f}")
    out["A4_points"] = rowsf

    print("\n=== CONTROLS (predicted share ~ floor) ===")
    for name, fn, ts in (("A4 ghz/Z (ferro reading)", None, fz["delays_control_us"]),
                         ("A5 classical/X", None, fz["delays_control_us"]),
                         ("A6 product/Z", None, fz["delays_product_us"])):
        pass
    # A4: GHZ read in Z is the ferro mixture -> share 0 exactly; A5: a diagonal
    # state read in X has all X-moments zero -> uniform -> share 0 exactly.
    # A6: independent bits -> share 0 exactly.  All three read the floor.
    fl, fs = P.floor_share(np.full((2, 2, 2), 0.125), fz["shots"]["A4"], reps=600, rng=RNG)
    out["control_floor_4096"] = dict(mean=float(fl), sd=float(fs),
                                     p99=float(fl + 2.33 * fs))
    print(f"  uniform-state floor at 4096 shots: {fl:.3e} +- {fs:.1e} "
          f"(p99 ~ {fl+2.33*fs:.3e})")
    fl2, fs2 = P.floor_share(np.full((2, 2, 2), 0.125), fz["shots"]["A1"], reps=600, rng=RNG)
    out["control_floor_8192"] = dict(mean=float(fl2), sd=float(fs2))
    print(f"  uniform-state floor at 8192 shots: {fl2:.3e} +- {fs2:.1e}")

    print("\n=== JOB B: ideal predictions (Lean) ===")
    # mint: uniform -> parity
    unif = np.full((2, 2, 2), 0.125)
    par = np.zeros((2, 2, 2))
    for x in itertools.product((0, 1), repeat=3):
        if sum(x) % 2 == 0:
            par[x] = 0.25
    cop = np.zeros((2, 2, 2))
    for a in (0, 1):
        for b in (0, 1):
            cop[a, b, a] = 0.25
    print(f"  MINT   in: share {P.share(unif):.4f} S_tot {P.s_total(unif):.4f}"
          f"  out: share {P.share(par):.6f} S_tot {P.s_total(par):.6f}  (ln2 {LN2:.6f})")
    print(f"  COPY   out: share {P.share(cop):.6f} S_tot {P.s_total(cop):.6f}")
    out["B_ideal"] = dict(mint_share=float(P.share(par)), mint_stot=float(P.s_total(par)),
                          copy_share=float(P.share(cop)), copy_stot=float(P.s_total(cop)))

    # rent arms: paid = (a, b, a XOR b) with a,b relaxed for T; unpaid = idle T
    rows = []
    for T in fz["rent_totals_us"]:
        pa = 0.5 * math.exp(-T / T1[0]) + P_EXC * (1 - math.exp(-T / T1[0]))
        pb = 0.5 * math.exp(-T / T1[1]) + P_EXC * (1 - math.exp(-T / T1[1]))
        paid = np.zeros((2, 2, 2))
        for a in (0, 1):
            for b in (0, 1):
                paid[a, b, a ^ b] = (pa if a else 1 - pa) * (pb if b else 1 - pb)
        unpaid = true_classical(T)
        rows.append(dict(T=T, paid_share=float(P.share(paid)), paid_stot=float(P.s_total(paid)),
                         unpaid_share=float(P.share(unpaid)), unpaid_stot=float(P.s_total(unpaid)),
                         ratio=float(P.share(paid) / max(P.share(unpaid), 1e-12))))
        print(f"  T={T:6.1f}us  PAID share {P.share(paid):.5f}  UNPAID share "
              f"{P.share(unpaid):.5f}   ratio {P.share(paid)/max(P.share(unpaid),1e-12):.1f}x")
    out["B_rent_ideal"] = rows

    print("\n=== JOB B: NOISY bands (calibration-matched Aer, repeated) ===")
    import qpu_habit_gate as G
    R = 25
    acc = {}
    planB = P.plan_B(fz)
    for r in range(R):
        cnt = G.run(planB, noisy=True, shots_scale=1.0)
        amats = P.assignment_matrices(P.counts_to_p(cnt["B3|cal|000|0"]).ravel(),
                                      P.counts_to_p(cnt["B3|cal|111|0"]).ravel())
        for tag, c in cnt.items():
            p = P.counts_to_p(c)
            pc = P.correct_readout(p, amats)
            pc = np.clip(pc, 0, None); pc = pc / pc.sum()
            acc.setdefault(tag, {"share_raw": [], "share_corr": [],
                                 "S_total_corr": []})
            acc[tag]["share_raw"].append(P.share(p))
            acc[tag]["share_corr"].append(P.share(pc))
            acc[tag]["S_total_corr"].append(P.s_total(pc))
    rowsB = {}
    for tag in sorted(acc):
        d = {k: (float(np.mean(v)), float(np.std(v))) for k, v in acc[tag].items()}
        rowsB[tag] = {k: {"mean": m, "sd": s} for k, (m, s) in d.items()}
        print(f"  {tag:24s} share_corr {d['share_corr'][0]:.5f} +- {d['share_corr'][1]:.5f}"
              f"   raw {d['share_raw'][0]:.5f}   S_tot {d['S_total_corr'][0]:.5f}")
    out["B_noisy_bands"] = rowsB
    out["B_noisy_reps"] = R

    with open(BOUT, "w") as f:
        json.dump(out, f, indent=2, default=float)
    print("\nsaved qpu_habit_bands.json")


if __name__ == "__main__":
    main()
