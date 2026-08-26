#!/usr/bin/env python3
"""LLM whole-only synergy — effect-size calibration (rebuild).

Frozen per llm-effectsize-prereg.md. Turns the sign-only synergy result into a
sized statement: maps trained-model whole-only structure to an inferred order-3
fraction, and resolves the mixed positive-control puzzle.

Reuses fmri_whole_only primitives (normal_score, eqfreq_codes, joint_counts,
deltaI3_batch, mvpr_surrogate). Adds batched O-information (the SIGN).
Run: /home/emoore/whisper-venv/bin/python llm_synergy.py <cmd>
"""
import os, sys, json, time, warnings
warnings.filterwarnings("ignore")
os.environ["HF_HUB_OFFLINE"] = "1"; os.environ["TRANSFORMERS_OFFLINE"] = "1"
import numpy as np
import fmri_whole_only as F

HERE = os.path.dirname(os.path.abspath(__file__))
LOG2 = np.log(2.0)
LAYER = 6
N_POS = 4000
M_TRI = 3000
SEED = 0


def log(m): print(m, flush=True)


# ---------- activation extraction ----------
def extract(model_name, n_pos=N_POS, layer=LAYER, trained=True, seed=0):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig
    torch.set_num_threads(8); torch.manual_seed(seed)
    tok = AutoTokenizer.from_pretrained(model_name)
    if tok.pad_token is None: tok.pad_token = tok.eos_token
    if trained:
        m = AutoModelForCausalLM.from_pretrained(model_name, output_hidden_states=True,
                                                 dtype=torch.float32).eval()
    else:
        cfg = AutoConfig.from_pretrained(model_name); cfg.output_hidden_states = True
        m = AutoModelForCausalLM.from_config(cfg).eval()   # random init
    corpus = json.load(open(os.path.join(HERE, "wikitext_corpus.json")))
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(corpus))
    acts = []; ntok = 0; ci = 0
    with torch.no_grad():
        while ntok < n_pos and ci < len(order):
            line = corpus[order[ci]]; ci += 1
            ids = tok(line, return_tensors="pt", truncation=True, max_length=96)
            if ids["input_ids"].shape[1] < 8: continue
            hs = m(**ids).hidden_states[layer][0]          # (T,d)
            # subsample a few positions per sequence -> reduce within-seq autocorr
            T = hs.shape[0]; take = rng.choice(T, size=min(6, T), replace=False)
            acts.append(hs[take].numpy()); ntok += len(take)
    A = np.concatenate(acts, axis=0)[:n_pos]
    return A.astype(np.float64)


# ---------- O-information (nats), batched over triplets ----------
def entropy_nats(P, axis=None):
    with np.errstate(divide="ignore", invalid="ignore"):
        L = np.where(P > 0, np.log(P), 0.0)
    return -(P * L).sum(axis=axis)


def o_information_batch(counts, b):
    """counts:(M,b^3). Omega (nats): <0 synergy, >0 redundancy. Also TC, DeltaI3."""
    M = counts.shape[0]; T = counts[0].sum()
    P = (counts / T).reshape(M, b, b, b)
    Hfull = entropy_nats(P.reshape(M, -1), axis=1)
    Ma = P.sum((2, 3)); Mb = P.sum((1, 3)); Mc = P.sum((1, 2))
    Ha = entropy_nats(Ma, 1); Hb = entropy_nats(Mb, 1); Hc = entropy_nats(Mc, 1)
    Hij = entropy_nats(P.sum(3).reshape(M, -1), 1)   # H(Xi,Xj)
    Hik = entropy_nats(P.sum(2).reshape(M, -1), 1)   # H(Xi,Xk)
    Hjk = entropy_nats(P.sum(1).reshape(M, -1), 1)   # H(Xj,Xk)
    # Omega = (n-2)Hfull + sum_i [H(X_i) - H(X_{-i})], n=3
    Omega = Hfull + (Ha - Hjk) + (Hb - Hik) + (Hc - Hij)
    TC = Ha + Hb + Hc - Hfull
    return Omega, TC


def whole_only(A, b, m_tri, rng):
    """Returns dict: mean Omega (nats), mean DeltaI3 (bits), phi=DeltaI3/TC,
    and the per-triplet arrays for bootstrap."""
    Z = F.normal_score(A); d = Z.shape[1]
    tri = rng.integers(0, d, size=(m_tri, 3))
    g = (tri[:, 0] != tri[:, 1]) & (tri[:, 0] != tri[:, 2]) & (tri[:, 1] != tri[:, 2])
    tri = tri[g]; I, J, K = tri[:, 0], tri[:, 1], tri[:, 2]
    codes = F.eqfreq_codes(Z, b)
    cnt = F.joint_counts(codes, I, J, K, b)
    dI3, TCb = F.deltaI3_batch(cnt, b)               # bits
    Om, TCn = o_information_batch(cnt, b)            # nats
    phi = dI3 / np.where(TCb > 1e-9, TCb, np.nan)
    return dict(I=I, J=J, K=K, dI3=dI3, Omega=Om, TC_bits=TCb, phi=phi,
                mean_Omega_nats=float(np.mean(Om)),
                mean_dI3_bits=float(np.mean(dI3)),
                phi_median=float(np.nanmedian(phi)))


def null_floor(Z, b, I, J, K, n_surr, rng, kind="mvpr"):
    """Bias floor for DeltaI3 and Omega via matched surrogate."""
    dI3s = np.empty(n_surr); Oms = np.empty(n_surr)
    for s in range(n_surr):
        if kind == "mvpr":
            Zs = F.mvpr_surrogate(Z, rng)
        else:  # independent shuffle (kills all dependence)
            Zs = np.column_stack([rng.permutation(Z[:, j]) for j in range(Z.shape[1])])
        cs = F.eqfreq_codes(Zs, b); cnt = F.joint_counts(cs, I, J, K, b)
        d, _ = F.deltaI3_batch(cnt, b); o, _ = o_information_batch(cnt, b)
        dI3s[s] = float(d.mean()); Oms[s] = float(o.mean())
    return dI3s, Oms


# ---------- planting (three variants for the mixed-control puzzle) ----------
def plant(base_Z, f, rng, variant="A"):
    """Inject order-3 into disjoint triplets of a pairwise-preserving base.
    A: sign-parity (survives binning). B: sub-bin-width wash-out.
    C: pairwise-contaminating."""
    N, d = base_Z.shape
    P = d // 3
    cols = rng.permutation(d)[: 3 * P]
    g = base_Z[:, cols].copy()
    g1 = g[:, 0::3]; g2 = g[:, 1::3]; g3 = g[:, 2::3]
    if variant == "A":
        s = np.sign(g1 * g2) * np.abs(rng.standard_normal(g3.shape))
        g3n = (1 - f) * g3 + f * s
    elif variant == "B":
        # order-3 injected at amplitude far below the (median-split) bin width,
        # so rank-binning removes it: tiny continuous parity added to a large base
        s = np.sign(g1 * g2) * np.abs(rng.standard_normal(g3.shape))
        g3n = g3 + (f * 0.02) * s                     # ~50x weaker per f
    elif variant == "C":
        # plant that also shifts pairwise: add a term correlated with g1 (order-2)
        s = np.sign(g1 * g2) * np.abs(rng.standard_normal(g3.shape))
        g3n = (1 - f) * g3 + f * (0.5 * s + 0.5 * g1)  # half order-3, half pairwise
    Zp = base_Z.copy()
    Zp[:, cols[2::3]] = g3n
    planted_dims = cols.reshape(P, 3)
    return Zp, planted_dims


def calibrate(A, b, rng, variant="A", grid=(0, 0.02, 0.05, 0.10, 0.20, 0.30, 0.50, 1.0),
              n_surr=40):
    """Plant into a pairwise-preserving base of A; z(f), phi(f)."""
    Z = F.normal_score(A)
    base = F.normal_score(F.mvpr_surrogate(Z, rng))     # real pairwise, order3~0
    rows = []
    for f in grid:
        Zp, pdims = plant(base, f, rng, variant)
        I, J, K = pdims[:, 0], pdims[:, 1], pdims[:, 2]
        cp = F.eqfreq_codes(Zp, b); cnt = F.joint_counts(cp, I, J, K, b)
        dI3, TCb = F.deltaI3_batch(cnt, b); Om, _ = o_information_batch(cnt, b)
        d_data = float(dI3.mean()); om = float(Om.mean())
        phi = float(np.nanmedian(dI3 / np.where(TCb > 1e-9, TCb, np.nan)))
        ds, os_ = null_floor(Zp, b, I, J, K, n_surr, rng, "mvpr")
        z = (d_data - ds.mean()) / ds.std(ddof=1)
        zO = (om - os_.mean()) / os_.std(ddof=1)
        rows.append(dict(f=f, z_dI3=float(z), z_Omega=float(zO),
                         Omega_nats=om, phi=phi, dI3_bits=d_data))
        log(f"  {variant} f={f:.2f}  z_dI3={z:+8.1f}  z_Om={zO:+8.1f}  "
            f"Om={om:+.4f}n  phi={phi:.3f}")
    return rows


if __name__ == "__main__":
    print("use the driver commands in the run script")
