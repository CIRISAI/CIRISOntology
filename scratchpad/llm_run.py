#!/usr/bin/env python3
import os, sys, json, time
import numpy as np
import llm_synergy as S
import fmri_whole_only as F

HERE = os.path.dirname(os.path.abspath(__file__))
B = int(os.environ.get("BINS", "2"))
rng = np.random.default_rng(0)


def measure_model(name, trained=True, n_pos=S.N_POS, b=B):
    t0 = time.time()
    A = S.extract(name, n_pos=n_pos, trained=trained)
    S.log(f"  extracted {name} trained={trained}: acts {A.shape} ({time.time()-t0:.1f}s)")
    r = S.whole_only(A, b, S.M_TRI, np.random.default_rng(1))
    Z = F.normal_score(A)
    # bias floors: MVPR (pairwise-preserving) for dI3; independent-shuffle for Omega sign
    dS, oS = S.null_floor(Z, b, r["I"], r["J"], r["K"], 60, np.random.default_rng(2), "mvpr")
    _, oSh = S.null_floor(Z, b, r["I"], r["J"], r["K"], 60, np.random.default_rng(3), "shuffle")
    z_dI3 = (r["mean_dI3_bits"] - dS.mean()) / dS.std(ddof=1)
    z_Om = (r["mean_Omega_nats"] - oSh.mean()) / oSh.std(ddof=1)
    tie = F.tie_report(A)
    out = dict(model=name, trained=trained, n_pos=int(A.shape[0]), d=int(A.shape[1]), b=b,
               mean_Omega_nats=r["mean_Omega_nats"], Omega_shuffle_mu=float(oSh.mean()),
               z_Omega_vs_shuffle=float(z_Om),
               mean_dI3_bits=r["mean_dI3_bits"], dI3_floor=float(dS.mean()),
               z_dI3_vs_mvpr=float(z_dI3), phi_median=r["phi_median"],
               phi_floor_median=None, tie_fraction=float(tie))
    # phi above floor: bootstrap CI of mean dI3 excess and phi
    exc = r["dI3"] - dS.mean()
    bs = [np.mean(rng.choice(exc, len(exc))) for _ in range(500)]
    out["dI3_excess_bits_mean"] = float(exc.mean())
    out["dI3_excess_CI"] = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
    S.log(f"  {name} trained={trained}: Omega={r['mean_Omega_nats']:+.5f}n "
          f"z_Om(shuffle)={z_Om:+.1f}  dI3={r['mean_dI3_bits']:.5f}b floor={dS.mean():.5f} "
          f"z_dI3(mvpr)={z_dI3:+.1f}  phi_med={r['phi_median']:.4f}  tie={tie:.1e}")
    return out, A


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    results = {}
    if cmd in ("all", "gpt2"):
        S.log("=== TRAINED vs UNTRAINED (sign reproduction) ===")
        rt, At = measure_model("gpt2", trained=True)
        ru, _ = measure_model("gpt2", trained=False)
        results["gpt2_trained"] = rt; results["gpt2_untrained"] = ru
        S.log("\n=== CALIBRATION (variant A on gpt2 trained pairwise base) ===")
        results["calib_A"] = S.calibrate(At, B, np.random.default_rng(10), "A")
        S.log("\n=== MIXED-CONTROL variants B, C ===")
        results["calib_B"] = S.calibrate(At, B, np.random.default_rng(11), "B")
        results["calib_C"] = S.calibrate(At, B, np.random.default_rng(12), "C")
        json.dump(results, open(os.path.join(HERE, f"llm_result_b{B}.json"), "w"), indent=1)
        S.log(f"\nwrote llm_result_b{B}.json")
    if cmd in ("all", "opt"):
        ro, _ = measure_model("facebook/opt-125m", trained=True)
        results_opt = ro
        json.dump(results_opt, open(os.path.join(HERE, f"llm_opt_b{B}.json"), "w"), indent=1)
        S.log("wrote llm_opt_b{}.json".format(B))


if __name__ == "__main__":
    t0 = time.time()
    main()
    S.log(f"total {time.time()-t0:.0f}s")
