#!/usr/bin/env python3
"""adequacy / meaning-is-third — INTER-SUBJECT stimulus-locked triadic structure.

All 155 development_fmri subjects watched the SAME movie (T=168 aligned). Build the
consensus (ISC) signal = mean over subjects per region, and ask whether the SHARED,
content-locked signal carries irreducible order-3 structure. Two floors, BOTH
autocorrelation-preserving (unlike the retracted iid bootstrap):

  (1) MVPR/phase-randomization null on the consensus — is there any order-3 in the
      shared signal beyond its own power+cross spectrum? (autocorrelation-safe)
  (2) per-subject CIRCULAR-SHIFT null — roll each subject by a random lag, then
      average. Preserves each subject's exact autocorrelation AND nonlinear pairwise
      structure; destroys ONLY alignment to the movie. Isolates order-3 that is
      specifically LOCKED TO THE CONTENT (not chance alignment / not within-subject bias).

CALIBRATION: treat one random global shift-config as pseudo-real and recompute the
shift-z; it must sit ~0 (validates the shift null is unbiased).

Reading (frozen): a content-locked triadic claim needs z_shift large AND z_mvpr>0.
z_shift is the load-bearing one (bias-matched by construction). Seed fixed.
Report only dimensionless z / whole-only fraction phi.
"""
import os, sys, json, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fmri_whole_only as base

CACHE = os.path.join(HERE, "cohort2_schaefer200_ts.npz")
B = 2; M = 4000; N_MVPR = 200; N_SHIFT = 300; SEED = 0


def log(m): print(m, flush=True)


def load_stack():
    z = np.load(CACHE, allow_pickle=True)
    arrs = [np.asarray(z[k], float) for k in sorted(z.files, key=lambda s: int(s.split("_")[1]))]
    T0 = 168
    X = np.stack([a for a in arrs if a.shape == (T0, 200)])   # (n, T, R)
    return X


def dI3_mean(A, tri, b):
    """mean ΔI3 over fixed triplets on a single (T,R) field A."""
    Z = base.normal_score(A)
    codes = base.eqfreq_codes(Z, b)
    I, J, K = tri[:, 0], tri[:, 1], tri[:, 2]
    dI3, TC = base.deltaI3_batch(base.joint_counts(codes, I, J, K, b), b)
    return float(np.mean(dI3)), float(np.nanmedian(dI3 / np.where(TC > 1e-9, TC, np.nan)))


def consensus(X):
    return X.mean(axis=0)                    # (T, R)


def shifted_consensus(X, rng):
    n, T, R = X.shape
    lags = rng.integers(1, T, size=n)        # non-zero lags
    out = np.empty_like(X)
    for i in range(n):
        out[i] = np.roll(X[i], lags[i], axis=0)
    return out.mean(axis=0)


def isc(X):
    """mean inter-subject correlation per region, averaged — movie-drive sanity."""
    n, T, R = X.shape
    Xz = (X - X.mean(1, keepdims=True)) / (X.std(1, keepdims=True) + 1e-9)
    # mean pairwise ISC via mean-vs-leaveout is heavy; use mean over subjects corr with group mean
    g = Xz.mean(0)                            # (T,R)
    gz = (g - g.mean(0)) / (g.std(0) + 1e-9)
    r = (Xz * gz[None]).mean(1)               # (n,R) corr of each subj with group
    return float(np.median(r))


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    X = load_stack()
    n, T, R = X.shape
    log(f"inter-subject: n={n} subjects, T={T}, R={R}, M={M} triplets")
    log(f"  median subject-vs-consensus ISC = {isc(X):.3f}  (movie-drive sanity; >0 expected)")

    tri = rng.integers(0, R, size=(M, 3))
    good = (tri[:, 0] != tri[:, 1]) & (tri[:, 0] != tri[:, 2]) & (tri[:, 1] != tri[:, 2])
    tri = tri[good]

    A = consensus(X)
    d_real, phi_real = dI3_mean(A, tri, B)
    log(f"  consensus ΔI3={d_real:.5f}  phi_med={phi_real:.4f}")

    # floor 1: MVPR on the consensus (autocorrelation + cross-spectrum preserved)
    Zc = base.normal_score(A)
    d_mvpr = np.empty(N_MVPR)
    for s in range(N_MVPR):
        As = base.mvpr_surrogate(Zc, rng)     # (T,R), same spectra, order-3 destroyed
        cs = base.eqfreq_codes(As, B)
        I, J, K = tri[:, 0], tri[:, 1], tri[:, 2]
        d_mvpr[s] = float(np.mean(base.deltaI3_batch(base.joint_counts(cs, I, J, K, B), B)[0]))
    z_mvpr = (d_real - d_mvpr.mean()) / d_mvpr.std(ddof=1)

    # floor 2: per-subject circular-shift consensus (content-alignment destroyed only)
    d_shift = np.empty(N_SHIFT)
    for s in range(N_SHIFT):
        d_shift[s] = dI3_mean(shifted_consensus(X, rng), tri, B)[0]
        if (s + 1) % 100 == 0:
            log(f"    shift-null {s+1}/{N_SHIFT}  running z_shift="
                f"{(d_real-d_shift[:s+1].mean())/ (d_shift[:s+1].std(ddof=1)+1e-12):+.2f}")
    z_shift = (d_real - d_shift.mean()) / d_shift.std(ddof=1)

    # calibration: a pseudo-real = one shifted consensus; its z under the shift null ~0
    A_pseudo = shifted_consensus(X, rng)
    d_pseudo = dI3_mean(A_pseudo, tri, B)[0]
    d_shift2 = np.array([dI3_mean(shifted_consensus(X, rng), tri, B)[0] for _ in range(N_SHIFT)])
    z_calib = (d_pseudo - d_shift2.mean()) / d_shift2.std(ddof=1)

    out = dict(n=int(n), M=int(tri.shape[0]), phi_consensus=phi_real,
               z_mvpr=float(z_mvpr), z_shift=float(z_shift), z_calib=float(z_calib),
               d_real=d_real, isc_median=isc(X))
    log("\n" + "=" * 66)
    log(f"  z_MVPR   (order-3 in shared signal, autocorr-safe) = {z_mvpr:+.2f}")
    log(f"  z_SHIFT  (content-LOCKED order-3, bias-matched)    = {z_shift:+.2f}   [load-bearing]")
    log(f"  z_CALIB  (shift-null on a pseudo-real, must be ~0) = {z_calib:+.2f}")
    if abs(z_calib) > 4:
        v = "SHIFT NULL MISCALIBRATED (z_calib off) — do not interpret z_shift"
    elif z_shift >= 5 and z_mvpr > 0:
        v = "CONTENT-LOCKED order-3 DETECTED — shared meaning carries irreducible triadic structure"
    elif abs(z_shift) <= 3:
        v = "NO content-locked order-3 — the shared signal is pairwise-reducible"
    else:
        v = "AMBIGUOUS content-locked lean (3<z<5)"
    log(f"  VERDICT: {v}")
    json.dump(out, open(os.path.join(HERE, "fmri_intersubject.json"), "w"), indent=1)
    log(f"  ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
