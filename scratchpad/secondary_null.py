#!/usr/bin/env python3
"""Confirmatory secondary null (pre-registered): pairwise-maxent RESAMPLE.

The primary MVPR surrogate preserves only the GAUSSIAN pairwise structure. If
real fMRI has non-Gaussian bivariate structure, the plug-in DeltaI3 bias floor
from a Gaussian surrogate can sit slightly low, inflating z as a null-model
artifact rather than genuine order-3.

This null fits, per triplet, the pairwise-maxent P* (IPF, matches ALL three
2-way marginals of the DATA exactly) and RESAMPLES T iid draws from it. P* has
TRUE order-3 = 0 but the data's full pairwise distribution. If the data's small
positive drift persists against THIS floor, it is genuine (sub-threshold)
order-3; if it vanishes, the MVPR drift was a Gaussian-surrogate artifact.

Run on a subject subset — enough to arbitrate the ~+0.22 sigma/subject drift.
"""
import os, sys, json, time
import numpy as np
import fmri_whole_only as F

B = int(sys.argv[1]) if len(sys.argv) > 1 else 2
N_SUBJ = int(sys.argv[2]) if len(sys.argv) > 2 else 30
M = 800
N_SURR = 60
SEED = 7
HERE = os.path.dirname(os.path.abspath(__file__))


def deltaI3_and_maxent(counts, b):
    """Like deltaI3_batch but also returns P* (pairwise-maxent) per triplet."""
    Mn = counts.shape[0]
    T = counts[0].sum()
    P = (counts / T).reshape(Mn, b, b, b)
    Hd = F.entropy_bits(P.reshape(Mn, -1), axis=1)
    Mab = P.sum(3); Mac = P.sum(2); Mbc = P.sum(1)
    Q = np.ones((Mn, b, b, b)) / (b ** 3)
    eps = 1e-12
    for _ in range(F.IPF_ITERS):
        Q *= (Mab / (Q.sum(3) + eps))[:, :, :, None]
        Q *= (Mac / (Q.sum(2) + eps))[:, :, None, :]
        Q *= (Mbc / (Q.sum(1) + eps))[:, None, :, :]
    Hstar = F.entropy_bits(Q.reshape(Mn, -1), axis=1)
    return (Hstar - Hd), Q.reshape(Mn, -1)


def resample_deltaI3(Pstar, T, b, rng):
    """Draw T iid samples from each triplet's P* (b^3 cells), return DeltaI3."""
    Mn, ncell = Pstar.shape
    cdf = np.cumsum(Pstar, axis=1)
    cdf[:, -1] = 1.0
    counts = np.zeros((Mn, ncell))
    u = rng.random((Mn, T))
    for m in range(Mn):
        idx = np.searchsorted(cdf[m], u[m])
        np.add.at(counts[m], np.clip(idx, 0, ncell - 1), 1)
    dI3, _ = F.deltaI3_batch(counts, b)
    return dI3


def main():
    ctrl, _ = F.load_controls()
    rng = np.random.default_rng(SEED)
    # spread across sites: take every k-th control
    idx = np.linspace(0, len(ctrl) - 1, N_SUBJ).astype(int)
    files = [ctrl[i] for i in idx]
    print(f"secondary (pairwise-maxent resample) null: b={B}, n={len(files)}, "
          f"M={M}, n_surr={N_SURR}", flush=True)
    z_mvpr, z_pmax = [], []
    for i, p in enumerate(files):
        ts = F.load_subject(p)
        if ts is None:
            continue
        Z = F.normal_score(ts); R = Z.shape[1]; T = Z.shape[0]
        tri = rng.integers(0, R, size=(M, 3))
        g = (tri[:, 0] != tri[:, 1]) & (tri[:, 0] != tri[:, 2]) & (tri[:, 1] != tri[:, 2])
        tri = tri[g]; I, J, K = tri[:, 0], tri[:, 1], tri[:, 2]
        codes = F.eqfreq_codes(Z, B)
        dI3_d, Pstar = deltaI3_and_maxent(F.joint_counts(codes, I, J, K, B), B)
        d_data = float(dI3_d.mean())
        # MVPR floor
        dm = np.empty(N_SURR)
        for s in range(N_SURR):
            Zs = F.mvpr_surrogate(Z, rng); cs = F.eqfreq_codes(Zs, B)
            dm[s] = float(F.deltaI3_batch(F.joint_counts(cs, I, J, K, B), B)[0].mean())
        zm = (d_data - dm.mean()) / dm.std(ddof=1)
        # pairwise-maxent resample floor
        dp = np.empty(N_SURR)
        for s in range(N_SURR):
            dp[s] = float(resample_deltaI3(Pstar, T, B, rng).mean())
        zp = (d_data - dp.mean()) / dp.std(ddof=1)
        z_mvpr.append(zm); z_pmax.append(zp)
        print(f"  [{i+1:2d}/{len(files)}] T={T:3d}  z_MVPR={zm:+.2f}  "
              f"z_pairmaxent={zp:+.2f}  (d={d_data:.4f} mvpr_mu={dm.mean():.4f} "
              f"pmax_mu={dp.mean():.4f})", flush=True)
    z_mvpr = np.array(z_mvpr); z_pmax = np.array(z_pmax)
    nm = len(z_mvpr)
    out = dict(b=B, n=nm, M=M, n_surr=N_SURR,
               mvpr_mean_z=float(z_mvpr.mean()),
               mvpr_Zgroup=float(z_mvpr.mean() * np.sqrt(nm)),
               pairmaxent_mean_z=float(z_pmax.mean()),
               pairmaxent_Zgroup=float(z_pmax.mean() * np.sqrt(nm)))
    print("\n=== SECONDARY NULL COMPARISON ===")
    print(f"  MVPR (Gaussian pairwise):      mean_z {z_mvpr.mean():+.3f}  "
          f"Zgroup {out['mvpr_Zgroup']:+.2f}")
    print(f"  pairwise-maxent resample:      mean_z {z_pmax.mean():+.3f}  "
          f"Zgroup {out['pairmaxent_Zgroup']:+.2f}")
    print("  If pairmaxent mean_z ~ 0 while MVPR > 0 -> the MVPR drift is a")
    print("  Gaussian-surrogate bias artifact; the true order-3 floor is clean.")
    json.dump(out, open(os.path.join(HERE, f"secondary_null_b{B}.json"), "w"), indent=1)


if __name__ == "__main__":
    t0 = time.time()
    main()
    print(f"done ({time.time()-t0:.0f}s)")
