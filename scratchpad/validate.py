#!/usr/bin/env python3
"""Validation for the LLM effect-size sized statement (team-lead required):
1. b=3 robustness of the trained-minus-untrained ~2% learned fraction.
2. Untrained-OPT control (+ trained-minus-untrained for OPT).
3. N-subsampling bias check (does the learned excess scale ~1/N like the fMRI
   b=3 trap, or is it N-stable = real?).
Caches activations to .npy so each model is extracted once.
"""
import os, sys, json, time
import numpy as np
import llm_synergy as S
import fmri_whole_only as F

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = [("gpt2", True), ("gpt2", False),
          ("facebook/opt-125m", True), ("facebook/opt-125m", False)]


def get_acts(name, trained):
    tag = name.replace("/", "_") + ("_T" if trained else "_U")
    p = os.path.join(HERE, f"act_{tag}.npy")
    if os.path.exists(p):
        return np.load(p)
    A = S.extract(name, n_pos=S.N_POS, trained=trained)
    np.save(p, A); return A


def measure(A, b, m_tri=3000, n_surr=60):
    """Return mean Omega (nats), mean dI3 (bits), floor, phi, and per-triplet arrays."""
    r = S.whole_only(A, b, m_tri, np.random.default_rng(1))
    Z = F.normal_score(A)
    dS, _ = S.null_floor(Z, b, r["I"], r["J"], r["K"], n_surr, np.random.default_rng(2), "mvpr")
    return dict(Omega=r["mean_Omega_nats"], dI3=r["mean_dI3_bits"],
                floor=float(dS.mean()), phi=r["phi_median"],
                dI3_excess=r["mean_dI3_bits"] - float(dS.mean()),
                dI3_arr=r["dI3"])


def f_star(curveA, key, val):
    fs = np.array([x["f"] for x in curveA])
    c = np.array([x[key] for x in curveA])
    if key == "Omega_nats":
        c = -c; val = -val
    o = np.argsort(c)
    return float(np.interp(val, c[o], fs[o]))


def main():
    t0 = time.time()
    out = {}
    acts = {}
    for name, tr in MODELS:
        acts[(name, tr)] = get_acts(name, tr)
        S.log(f"  acts {name} trained={tr}: {acts[(name,tr)].shape}")

    for b in (2, 3):
        S.log(f"\n===== b={b} =====")
        # calibration curve at this b (on gpt2 trained pairwise base)
        calA = S.calibrate(acts[("gpt2", True)], b, np.random.default_rng(10), "A")
        res = {}
        for name, tr in MODELS:
            m = measure(acts[(name, tr)], b)
            res[f"{name}|{tr}"] = {k: v for k, v in m.items() if k != "dI3_arr"}
            fO = f_star(calA, "Omega_nats", m["Omega"])
            fP = f_star(calA, "phi", m["phi"])
            res[f"{name}|{tr}"]["f_Omega"] = fO
            res[f"{name}|{tr}"]["f_phi"] = fP
            S.log(f"  {name:18s} trained={str(tr):5s}: Om={m['Omega']:+.5f} "
                  f"dI3={m['dI3']:.5f} floor={m['floor']:.5f} phi={m['phi']:.4f} "
                  f"f*(Om)={fO:.3f} f*(phi)={fP:.3f}")
        # learned = trained - untrained, per architecture, via f*
        for arch in ("gpt2", "facebook/opt-125m"):
            T = res[f"{arch}|True"]; U = res[f"{arch}|False"]
            learned_fO = T["f_Omega"] - U["f_Omega"]
            learned_fP = T["f_phi"] - U["f_phi"]
            res[f"{arch}|learned"] = dict(f_Omega=learned_fO, f_phi=learned_fP,
                                          dI3_excess_TmU=T["dI3_excess"] - U["dI3_excess"])
            S.log(f"  --> {arch:18s} LEARNED (T-U): f*(Om)={learned_fO:.3f} "
                  f"f*(phi)={learned_fP:.3f}  dI3_excess(T-U)={T['dI3_excess']-U['dI3_excess']:.5f}")
        out[f"b{b}"] = {"calibA": calA, "models": res}

    # N-subsampling bias check at b=3 (gpt2): learned excess vs 1/N
    S.log("\n===== N-subsampling bias check (b=3, gpt2 learned excess) =====")
    AT = acts[("gpt2", True)]; AU = acts[("gpt2", False)]
    nrows = []
    for N in (1000, 2000, 4000):
        mt = measure(AT[:N], 3, m_tri=3000, n_surr=40)
        mu = measure(AU[:N], 3, m_tri=3000, n_surr=40)
        learned = mt["dI3_excess"] - mu["dI3_excess"]
        om_learned = mt["Omega"] - mu["Omega"]
        nrows.append((N, learned, om_learned, mt["dI3_excess"], mu["dI3_excess"]))
        S.log(f"  N={N}: learned dI3_excess(T-U)={learned:.6f}  Omega(T-U)={om_learned:+.6f}")
    out["Nscan_b3"] = [dict(N=n, learned_dI3=l, learned_Om=o, T_exc=t, U_exc=u)
                       for (n, l, o, t, u) in nrows]
    # does learned scale with 1/N (bias) or flat (real)?
    Ns = np.array([r[0] for r in nrows]); learned = np.array([r[1] for r in nrows])
    from scipy.stats import pearsonr
    if len(Ns) >= 3:
        r_, p_ = pearsonr(1.0 / Ns, learned)
        out["Nscan_corr_1overN"] = [float(r_), float(p_)]
        S.log(f"  corr(1/N, learned dI3 excess) = {r_:+.2f} (p={p_:.3f})  "
              f"[flat/near-0 => real, strong+ => bias]")

    json.dump(out, open(os.path.join(HERE, "llm_validate.json"), "w"), indent=1)
    S.log(f"\nwrote llm_validate.json  ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
