#!/usr/bin/env python3
"""Human-fMRI whole-only remainder — adequacy's live kill.

Frozen per fmri-prereg.md (committed before any statistic on real data).

OBJECT: the order>=3 connected-information remainder S is blind to =
  DeltaI3 = TC_data - TC_pairwise-maxent = H(P*) - H(P_data) = KL(data||pairwise-maxent),
per triplet, on normal-scored (copula) CC200 fMRI, order 3 (as mouse V1 / BOSS).

NULL: multivariate phase-randomised surrogate (Prichard-Theiler, common phase all
regions) — preserves per-region power spectrum AND full cross-spectrum, destroys
order>=3, true DeltaI3=0; supplies the autocorrelation-matched bias floor.

DECISION: Z_group = mean_i(z_i)*sqrt(n).  >=+5 DETECTION (kill fires);
|Z|<=3 clean null (4th substrate); 3<Z<5 inconclusive.
Provenance lock: report only dimensionless fraction phi and z/sigma.
"""
import os, sys, glob, json, time
import numpy as np
from scipy.special import ndtri

DATA = os.path.expanduser("~/nilearn_data/ABIDE_pcp/cpac/filt_noglobal")
PHENO = os.path.expanduser("~/nilearn_data/ABIDE_pcp/Phenotypic_V1_0b_preprocessed1.csv")
HERE = os.path.dirname(os.path.abspath(__file__))

B = 2                 # primary binning (median split)
M_TRIPLETS = 1500
N_SURR = 100
MIN_T = 60
IPF_ITERS = 40
IPF_TOL = 1e-6
SEED = 0
LOG2 = np.log(2.0)


def log(m): print(m, flush=True)


# ---------- load ----------
def load_subject(path):
    ts = np.loadtxt(path, comments="#")     # (T, R)
    if ts.ndim != 2 or ts.shape[0] < MIN_T:
        return None
    sd = ts.std(axis=0)
    ts = ts[:, sd > 1e-9]
    if ts.shape[1] < 30:
        return None
    return ts


def normal_score(ts):
    """Rank -> ndtri per column (copula transform). Exact marginals Gaussian."""
    T, R = ts.shape
    ranks = np.argsort(np.argsort(ts, axis=0), axis=0) + 1.0
    return ndtri(ranks / (T + 1.0))


def eqfreq_codes(Z, b):
    """Equal-frequency bin each column into [0,b). Rank-based -> tie-robust."""
    T, R = Z.shape
    ranks = np.argsort(np.argsort(Z, axis=0), axis=0)     # 0..T-1
    codes = np.minimum((ranks * b) // T, b - 1).astype(np.int64)
    return codes


def region_entropies(codes, b):
    """H(X_r) in bits for each region."""
    T, R = codes.shape
    H = np.empty(R)
    for r in range(R):
        c = np.bincount(codes[:, r], minlength=b).astype(float)
        p = c / c.sum()
        p = p[p > 0]
        H[r] = -(p * np.log(p)).sum() / LOG2
    return H


def joint_counts(codes, I, J, K, b):
    """(M, b^3) counts for M triplets, one vectorised bincount."""
    T = codes.shape[0]
    M = len(I)
    b3 = b * b * b
    cj = codes[:, I]; ck = codes[:, J]; cl = codes[:, K]      # (T,M)
    jc = (cj * b + ck) * b + cl                                # (T,M) in [0,b3)
    off = jc + (np.arange(M) * b3)[None, :]
    cnt = np.bincount(off.ravel(), minlength=M * b3).reshape(M, b3)
    return cnt


def entropy_bits(P, axis=None):
    with np.errstate(divide="ignore", invalid="ignore"):
        L = np.where(P > 0, np.log(P), 0.0)
    return -(P * L).sum(axis=axis) / LOG2


def deltaI3_batch(counts, b):
    """counts: (M, b^3). Returns per-triplet DeltaI3 (bits), H_data, TC_data.
    DeltaI3 = H(P*) - H(P_data), P* = pairwise-maxent by IPF."""
    M = counts.shape[0]
    T = counts[0].sum()
    P = (counts / T).reshape(M, b, b, b)                       # axes M,a,b,c
    Hd = entropy_bits(P.reshape(M, -1), axis=1)
    # target pairwise marginals from data
    Mab = P.sum(axis=3)          # (M,a,b)
    Mac = P.sum(axis=2)          # (M,a,c)
    Mbc = P.sum(axis=1)          # (M,b,c)
    # marginal (1-way) entropies for TC
    Ma = P.sum(axis=(2, 3)); Mb = P.sum(axis=(1, 3)); Mc = P.sum(axis=(1, 2))
    Ha = entropy_bits(Ma, axis=1); Hb = entropy_bits(Mb, axis=1); Hc = entropy_bits(Mc, axis=1)
    TC = Ha + Hb + Hc - Hd
    # IPF to pairwise-maxent, start uniform
    Q = np.ones((M, b, b, b)) / (b * b * b)
    eps = 1e-12
    for _ in range(IPF_ITERS):
        q_ab = Q.sum(axis=3)
        Q *= (Mab / (q_ab + eps))[:, :, :, None]
        q_ac = Q.sum(axis=2)
        Q *= (Mac / (q_ac + eps))[:, :, None, :]
        q_bc = Q.sum(axis=1)
        Q *= (Mbc / (q_bc + eps))[:, None, :, :]
    Hstar = entropy_bits(Q.reshape(M, -1), axis=1)
    dI3 = Hstar - Hd                                           # >=0 up to numerics
    return dI3, TC


def mvpr_surrogate(Z, rng):
    """Common-phase multivariate phase randomisation: preserves every power
    spectrum and the full cross-spectrum, destroys order>=3."""
    T, R = Z.shape
    F = np.fft.rfft(Z, axis=0)
    nf = F.shape[0]
    ph = rng.uniform(0, 2 * np.pi, size=nf)
    ph[0] = 0.0
    if T % 2 == 0:
        ph[-1] = 0.0
    Fs = F * np.exp(1j * ph)[:, None]
    return np.fft.irfft(Fs, n=T, axis=0)


def tie_report(ts):
    """Fraction of exact duplicate values within columns (rank-based binning
    manufactures signal in proportion to ties)."""
    T, R = ts.shape
    dup = 0
    for r in range(R):
        u = np.unique(ts[:, r])
        dup += (T - len(u))
    return dup / (T * R)


# ---------- per-subject ----------
def run_subject(ts, b, m_triplets, n_surr, rng):
    Z = normal_score(ts)
    R = Z.shape[1]
    tri = rng.integers(0, R, size=(m_triplets, 3))
    # drop degenerate triplets (repeated region)
    good = (tri[:, 0] != tri[:, 1]) & (tri[:, 0] != tri[:, 2]) & (tri[:, 1] != tri[:, 2])
    tri = tri[good]
    I, J, K = tri[:, 0], tri[:, 1], tri[:, 2]

    codes = eqfreq_codes(Z, b)
    dI3_d, TC_d = deltaI3_batch(joint_counts(codes, I, J, K, b), b)
    d_data = float(np.mean(dI3_d))
    phi = dI3_d / np.where(TC_d > 1e-9, TC_d, np.nan)
    phi_med = float(np.nanmedian(phi))

    d_surr = np.empty(n_surr)
    for s in range(n_surr):
        Zs = mvpr_surrogate(Z, rng)
        cs = eqfreq_codes(Zs, b)
        dI3_s, _ = deltaI3_batch(joint_counts(cs, I, J, K, b), b)
        d_surr[s] = float(np.mean(dI3_s))
    mu, sd = d_surr.mean(), d_surr.std(ddof=1)
    z = (d_data - mu) / sd if sd > 0 else np.nan
    return dict(n_tri=int(len(I)), d_data=d_data, surr_mu=float(mu),
                surr_sd=float(sd), z=float(z), phi_med=phi_med)


# ---------- positive control ----------
def positive_control(ts_list, b, rng):
    """Plant a triadic (sign-parity) coupling into pairwise-preserving surrogate
    fields; confirm the instrument fires at realistic SNR. Un-planted triplets
    must stay null (validates the null too)."""
    log("\n" + "=" * 70)
    log("POSITIVE CONTROL — planted order-3 signal at a range of SNR f")
    log("=" * 70)
    P = 500                                   # disjoint planted triplets
    # build enough order-3-free columns from repeated MVPR surrogate draws
    # (each column carries the real field's autocorrelation; true order3 == 0)
    Z = normal_score(ts_list[0])
    R = Z.shape[1]
    blocks = []
    need = 3 * P
    while sum(b.shape[1] for b in blocks) < need:
        blocks.append(mvpr_surrogate(Z, rng))
    g = np.concatenate(blocks, axis=1)[:, :need]   # (T, 3P)
    g1 = g[:, 0::3]; g2 = g[:, 1::3]; g3 = g[:, 2::3]      # (T,P)
    # a genuinely order-3 (pairwise-null) target for the third region
    s = np.sign(g1 * g2) * np.abs(rng.standard_normal(g3.shape))
    fs = [0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0]
    n_surr = 60
    thr = None
    rows = []
    for f in fs:
        g3p = (1 - f) * g3 + f * s
        # planted field: interleave g1,g2,g3p as P triplets
        Zp = np.empty((g.shape[0], 3 * P))
        Zp[:, 0::3] = g1; Zp[:, 1::3] = g2; Zp[:, 2::3] = g3p
        I = np.arange(0, 3 * P, 3); J = I + 1; K = I + 2
        cp = eqfreq_codes(Zp, b)
        dI3_d, TC_d = deltaI3_batch(joint_counts(cp, I, J, K, b), b)
        d_data = float(np.mean(dI3_d))
        phi_med = float(np.nanmedian(dI3_d / np.where(TC_d > 1e-9, TC_d, np.nan)))
        dS = np.empty(n_surr)
        for si in range(n_surr):
            Zsu = mvpr_surrogate(Zp, rng)
            cs = eqfreq_codes(Zsu, b)
            dI3_s, _ = deltaI3_batch(joint_counts(cs, I, J, K, b), b)
            dS[si] = float(np.mean(dI3_s))
        z = (d_data - dS.mean()) / dS.std(ddof=1)
        rows.append((f, z, phi_med))
        log(f"  f={f:.2f}  planted z={z:8.2f}  phi_med={phi_med:.4f}")
        if thr is None and z >= 5:
            thr = f
    # un-planted control (f=0): same pipeline, must be null
    Zp0 = np.empty((g.shape[0], 3 * P))
    Zp0[:, 0::3] = g1; Zp0[:, 1::3] = g2; Zp0[:, 2::3] = g3
    I = np.arange(0, 3 * P, 3); J = I + 1; K = I + 2
    c0 = eqfreq_codes(Zp0, b)
    dI3_0, _ = deltaI3_batch(joint_counts(c0, I, J, K, b), b)
    d0 = float(np.mean(dI3_0))
    dS0 = np.empty(n_surr)
    for si in range(n_surr):
        Zsu = mvpr_surrogate(Zp0, rng); cs = eqfreq_codes(Zsu, b)
        dI3_s, _ = deltaI3_batch(joint_counts(cs, I, J, K, b), b)
        dS0[si] = float(np.mean(dI3_s))
    z0 = (d0 - dS0.mean()) / dS0.std(ddof=1)
    log(f"  UNPLANTED (f=0) control z={z0:.2f}  (must be within +-3)")
    log(f"  --> smallest f firing z>=5: {thr}")
    return dict(rows=rows, unplanted_z=float(z0), fire_threshold=thr)


# ---------- main ----------
def load_controls():
    import csv
    dx = {}
    with open(PHENO) as f:
        for row in csv.DictReader(f):
            fid = row.get("FILE_ID", "").strip()
            if fid and fid != "no_filename":
                try:
                    dx[fid] = int(row["DX_GROUP"])
                except Exception:
                    pass
    files = sorted(glob.glob(os.path.join(DATA, "*_rois_cc200.1D")))
    ctrl, allf = [], []
    for p in files:
        fid = os.path.basename(p).replace("_rois_cc200.1D", "")
        allf.append(p)
        if dx.get(fid) == 2:
            ctrl.append(p)
    return ctrl, allf


def main():
    t0 = time.time()
    b = int(sys.argv[1]) if len(sys.argv) > 1 else B
    which = sys.argv[2] if len(sys.argv) > 2 else "controls"
    ctrl, allf = load_controls()
    files = ctrl if which == "controls" else allf
    log("=" * 70)
    log(f"fMRI whole-only remainder — b={b}, sample={which}, "
        f"n_files={len(files)}, M={M_TRIPLETS}, n_surr={N_SURR}")
    log("=" * 70)
    rng = np.random.default_rng(SEED)

    # tie fraction on first few subjects (disclosure)
    ties = []
    for p in files[:10]:
        ts = load_subject(p)
        if ts is not None:
            ties.append(tie_report(ts))
    log(f"  exact-tie fraction (first 10 subj): median {np.median(ties):.2e}")

    results = []
    for i, p in enumerate(files):
        ts = load_subject(p)
        if ts is None:
            continue
        r = run_subject(ts, b, M_TRIPLETS, N_SURR, rng)
        r["file"] = os.path.basename(p); r["T"] = int(ts.shape[0]); r["R"] = int(ts.shape[1])
        results.append(r)
        if (i + 1) % 10 == 0 or i < 3:
            zs = np.array([x["z"] for x in results])
            log(f"  [{i+1:3d}/{len(files)}] {r['file'][:22]:22s} T={r['T']:3d} "
                f"z={r['z']:+6.2f}  running mean z={zs.mean():+.3f} "
                f"(Zgrp={zs.mean()*np.sqrt(len(zs)):+.2f})")

    z = np.array([x["z"] for x in results])
    n = len(z)
    Zgroup = float(z.mean() * np.sqrt(n))
    phi_med = float(np.median([x["phi_med"] for x in results]))
    out = dict(b=b, sample=which, n=n, mean_z=float(z.mean()),
               median_z=float(np.median(z)), max_z=float(z.max()),
               min_z=float(z.min()), Zgroup=Zgroup, phi_median=phi_med,
               tie_fraction=float(np.median(ties)),
               per_subject=results)

    log("\n" + "=" * 70)
    log(f"RESULT (b={b}, {which}, n={n})")
    log("=" * 70)
    log(f"  per-subject z: mean {z.mean():+.3f}  median {np.median(z):+.3f}  "
        f"[{z.min():+.2f}, {z.max():+.2f}]")
    log(f"  whole-only fraction phi: median {phi_med:.4f}")
    log(f"  Z_group = mean_z * sqrt(n) = {Zgroup:+.2f}")
    if Zgroup >= 5:
        v = "DETECTION — adequacy kill FIRES"
    elif abs(Zgroup) <= 3:
        v = "CLEAN NULL — adequacy extends to a 4th substrate"
    else:
        v = "INCONCLUSIVE"
    log(f"  VERDICT: {v}")

    op = os.path.join(HERE, f"fmri_result_b{b}_{which}.json")
    json.dump(out, open(op, "w"), indent=1)
    log(f"  wrote {op}   ({time.time()-t0:.0f}s)")
    return out, files


if __name__ == "__main__":
    out, files = main()
    if len(sys.argv) <= 3 or sys.argv[3] != "noctrl":
        rng = np.random.default_rng(123)
        ts0 = load_subject(files[0])
        pc = positive_control([ts0], int(sys.argv[1]) if len(sys.argv) > 1 else B, rng)
        op = os.path.join(HERE, "fmri_poscontrol.json")
        json.dump(pc, open(op, "w"), indent=1)
        print("wrote", op)
