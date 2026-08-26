#!/usr/bin/env python3
"""adequacy cohort 2 — PAIRWISE-MATCHED null on the SAME movie data.

The MVPR null preserves only the LINEAR cross-spectrum, so content-driven
nonlinear/non-stationary PAIRWISE structure it fails to reproduce could inflate
the ΔI3 bias floor and masquerade as order-3. This null fixes that WITHOUT
touching the content: for each triplet, fit the pairwise-maxent model P* (exact
2-way marginals of the data, nonlinear included, zero true order-3) and draw the
bias floor by SAMPLING from P*. Any surviving excess is order-3 beyond the data's
own pairwise structure.

PRE-REGISTERED reading (frozen before running; iid caveat stated):
  z_pw_group = mean_i(z_pw_i)*sqrt(n).
  * |z_pw_group| <= 3  -> the MVPR +4.0σ was PAIRWISE-STRUCTURE BIAS the linear
      null missed. The movie lean is NOT genuine order-3. DECISIVE negative
      (this floor is if anything anti-conservative re: autocorrelation — iid
      draws have LESS bias than autocorrelated data — so a collapse here is a
      strong result, not a weak one).
  * z_pw_group stays large (comparable to +4) -> the excess is real order-3
      beyond the exact pairwise marginals: genuine content-driven whole-only
      structure. SUGGESTIVE, not decisive — the iid floor ignores autocorrelation
      (mildly anti-conservative), so the inter-subject stimulus-locked design
      (circular-shift null) is the clincher.
Reports MVPR z and pairwise z side by side per subject. Seed fixed.
"""
import os, sys, json, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fmri_whole_only as base

CACHE = os.path.join(HERE, "cohort2_schaefer200_ts.npz")
B = 2; M = base.M_TRIPLETS; N_SURR = base.N_SURR; SEED = 0
IPF_ITERS = base.IPF_ITERS


def log(m): print(m, flush=True)


def pairwise_maxent_Q(counts, b):
    """IPF -> P* (pairwise-maxent) per triplet, returned as (M, b^3) prob rows."""
    Mn = counts.shape[0]; T = counts[0].sum()
    P = (counts / T).reshape(Mn, b, b, b)
    Mab = P.sum(axis=3); Mac = P.sum(axis=2); Mbc = P.sum(axis=1)
    Q = np.ones((Mn, b, b, b)) / (b ** 3); eps = 1e-12
    for _ in range(IPF_ITERS):
        Q *= (Mab / (Q.sum(axis=3) + eps))[:, :, :, None]
        Q *= (Mac / (Q.sum(axis=2) + eps))[:, :, None, :]
        Q *= (Mbc / (Q.sum(axis=1) + eps))[:, None, :, :]
    Q = Q.reshape(Mn, -1)
    return Q / Q.sum(axis=1, keepdims=True)


def sample_counts(Q, T, rng):
    """Sample T iid draws from each row of Q (M, b^3) -> counts (M, b^3)."""
    Mn, K = Q.shape
    cdf = np.cumsum(Q, axis=1)
    U = rng.random((Mn, T))
    codes = (U[:, :, None] >= cdf[:, None, :]).sum(axis=2)      # (M,T) in [0,K-1]
    np.clip(codes, 0, K - 1, out=codes)
    off = codes + (np.arange(Mn) * K)[:, None]
    return np.bincount(off.ravel(), minlength=Mn * K).reshape(Mn, K)


def run_subject_both(ts, b, rng):
    Z = base.normal_score(ts); R = Z.shape[1]
    tri = rng.integers(0, R, size=(M, 3))
    good = (tri[:, 0] != tri[:, 1]) & (tri[:, 0] != tri[:, 2]) & (tri[:, 1] != tri[:, 2])
    tri = tri[good]; I, J, K = tri[:, 0], tri[:, 1], tri[:, 2]
    codes = base.eqfreq_codes(Z, b)
    cnt = base.joint_counts(codes, I, J, K, b)
    dI3_d, _ = base.deltaI3_batch(cnt, b); d_data = float(np.mean(dI3_d))
    T = ts.shape[0]
    # MVPR floor (as in cohort 1)
    d_mvpr = np.empty(N_SURR)
    for s in range(N_SURR):
        cs = base.eqfreq_codes(base.mvpr_surrogate(Z, rng), b)
        d_mvpr[s] = float(np.mean(base.deltaI3_batch(base.joint_counts(cs, I, J, K, b), b)[0]))
    z_mvpr = (d_data - d_mvpr.mean()) / d_mvpr.std(ddof=1)
    # PAIRWISE-MATCHED floor: sample from fitted P*
    Q = pairwise_maxent_Q(cnt, b)
    d_pw = np.empty(N_SURR)
    for s in range(N_SURR):
        d_pw[s] = float(np.mean(base.deltaI3_batch(sample_counts(Q, T, rng), b)[0]))
    z_pw = (d_data - d_pw.mean()) / d_pw.std(ddof=1)
    return float(z_mvpr), float(z_pw)


def main():
    t0 = time.time()
    z = np.load(CACHE, allow_pickle=True)
    arrs = [z[k] for k in sorted(z.files, key=lambda s: int(s.split("_")[1]))]
    # qc identical to cohort2
    good = []
    for a in arrs:
        a = np.asarray(a, float)
        if a.ndim == 2 and a.shape[0] >= base.MIN_T:
            a = a[:, a.std(axis=0) > 1e-9]
            if a.shape[1] >= 30:
                good.append(a)
    log(f"pairwise-matched null on {len(good)} subjects (movie, Schaefer-200)")
    rng = np.random.default_rng(SEED)
    zm, zp = [], []
    for i, ts in enumerate(good):
        a, b_ = run_subject_both(ts, B, rng)
        zm.append(a); zp.append(b_)
        if (i + 1) % 20 == 0 or i < 2:
            zm_a, zp_a = np.array(zm), np.array(zp)
            log(f"  [{i+1:3d}/{len(good)}] z_mvpr={a:+5.2f} z_pw={b_:+5.2f}  "
                f"Zgrp_mvpr={zm_a.mean()*np.sqrt(len(zm_a)):+.2f} "
                f"Zgrp_pw={zp_a.mean()*np.sqrt(len(zp_a)):+.2f}")
    zm, zp = np.array(zm), np.array(zp)
    n = len(zm)
    Zm = float(zm.mean() * np.sqrt(n)); Zp = float(zp.mean() * np.sqrt(n))
    out = dict(n=n, Zgroup_mvpr=Zm, Zgroup_pairwise=Zp,
               mean_z_mvpr=float(zm.mean()), mean_z_pw=float(zp.mean()),
               max_z_pw=float(zp.max()), n_pw_past5=int((zp >= 5).sum()))
    log("\n" + "=" * 66)
    log(f"  Z_group  MVPR (linear null)      = {Zm:+.2f}   (reproduces cohort-2 +4.0)")
    log(f"  Z_group  PAIRWISE-MATCHED null   = {Zp:+.2f}   (mean z_pw {zp.mean():+.3f}, "
        f"max {zp.max():+.2f}, #past5 {(zp>=5).sum()})")
    if abs(Zp) <= 3:
        v = "COLLAPSES -> the +4σ was pairwise-structure bias; movie lean NOT genuine order-3 (decisive)"
    elif Zp >= 5:
        v = "SURVIVES strongly -> real order-3 beyond exact pairwise; content-driven Logos (confirm w/ inter-subject shift null)"
    else:
        v = "PARTIAL -> shrinks but not gone; ambiguous, inter-subject stimulus-locked design needed"
    log(f"  VERDICT: {v}")
    json.dump(out, open(os.path.join(HERE, "fmri_cohort2_pairwise_null.json"), "w"), indent=1)
    log(f"  ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
