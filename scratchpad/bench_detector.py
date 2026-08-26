"""bench_detector.py — the two meters + surrogate null + GATE self-test.

C3 machinery (H, marginals_1, I_total, pairwise_maxent, C3) copied verbatim
from temporal_whole_only.py (gate-tested there). Adds:
  - pair meter: pairwise phi-correlation and pairwise MI on the binarized triple
  - matched pairwise-maxent multinomial surrogate null for C3
  - GATE self-test: exact + sampled three-coin parity -> C3~ln2 ; independent -> C3~0
Run standalone:  python3 bench_detector.py
"""
import numpy as np
from itertools import product

# ---------- entropy / maxent machinery (natural log) — COPIED from temporal_whole_only.py ----------

def H(p):
    p = np.asarray(p, dtype=float).ravel()
    p = p[p > 1e-15]
    return float(-np.sum(p * np.log(p)))

def marginals_1(p):
    return [p.sum(axis=(1, 2)), p.sum(axis=(0, 2)), p.sum(axis=(0, 1))]

def I_total(p):
    return sum(H(m) for m in marginals_1(p)) - H(p)

def pairwise_maxent(p, iters=20000, tol=1e-13):
    """Iterative proportional fitting to the maxent dist with p's pairwise marginals."""
    m12 = p.sum(axis=2); m13 = p.sum(axis=1); m23 = p.sum(axis=0)
    q = np.full_like(p, 1.0 / p.size)
    for _ in range(iters):
        q12 = q.sum(axis=2)
        q *= np.where(q12 > 0, m12 / np.where(q12 > 0, q12, 1), 0)[:, :, None]
        q13 = q.sum(axis=1)
        q *= np.where(q13 > 0, m13 / np.where(q13 > 0, q13, 1), 0)[:, None, :]
        q23 = q.sum(axis=0)
        q *= np.where(q23 > 0, m23 / np.where(q23 > 0, q23, 1), 0)[None, :, :]
        err = max(np.abs(q.sum(axis=2) - m12).max(),
                  np.abs(q.sum(axis=1) - m13).max(),
                  np.abs(q.sum(axis=0) - m23).max())
        if err < tol:
            break
    return q

def C3(p):
    return H(pairwise_maxent(p)) - H(p)

# ---------- empirical distribution from a binarized triple ----------

def triple_hist(bits_abc):
    """bits_abc: (T,3) array of 0/1. Returns normalized p[2,2,2] and counts."""
    b = np.asarray(bits_abc, dtype=int)
    counts = np.zeros((2, 2, 2), dtype=float)
    for x, y, z in b:
        counts[x, y, z] += 1
    T = counts.sum()
    return counts / T, counts

# ---------- pair meter (on the same binarized data) ----------

def bin_corr(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    sx, sy = x.std(), y.std()
    if sx < 1e-12 or sy < 1e-12:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])

def bin_mi(x, y):
    """Mutual information (nats) of two binary arrays from 2x2 counts."""
    x = np.asarray(x, int); y = np.asarray(y, int)
    T = len(x)
    j = np.zeros((2, 2))
    for a, b in zip(x, y):
        j[a, b] += 1
    j /= T
    px = j.sum(axis=1); py = j.sum(axis=0)
    mi = 0.0
    for a in range(2):
        for b in range(2):
            if j[a, b] > 0 and px[a] > 0 and py[b] > 0:
                mi += j[a, b] * np.log(j[a, b] / (px[a] * py[b]))
    return float(mi)

def pair_meter(bits_abc):
    """Returns max|corr| and max MI (nats) over the 3 pairs, plus per-pair."""
    b = np.asarray(bits_abc, int)
    A, B, Cc = b[:, 0], b[:, 1], b[:, 2]
    corrs = {'AB': bin_corr(A, B), 'AC': bin_corr(A, Cc), 'BC': bin_corr(B, Cc)}
    mis = {'AB': bin_mi(A, B), 'AC': bin_mi(A, Cc), 'BC': bin_mi(B, Cc)}
    return (max(abs(v) for v in corrs.values()), max(mis.values()), corrs, mis)

# ---------- matched pairwise-maxent multinomial surrogate null for C3 ----------

def surrogate_null(p_obs, T, n_surr=60, rng=None):
    """Draw T samples from the pairwise-maxent (order-3-free) distribution that
    matches p_obs's pairwise marginals; recompute C3 on each T-sample empirical.
    This is the finite-sample C3 bias floor with matched pairwise structure."""
    if rng is None:
        rng = np.random.default_rng()
    ptilde2 = pairwise_maxent(p_obs)
    flat = ptilde2.ravel()
    flat = np.clip(flat, 0, None); flat = flat / flat.sum()
    c3s = np.empty(n_surr)
    for i in range(n_surr):
        counts = rng.multinomial(int(round(T)), flat).reshape(2, 2, 2).astype(float)
        c3s[i] = C3(counts / counts.sum())
    return float(c3s.mean()), float(c3s.std(ddof=1)), c3s

def joint_detector(bits_abc, n_surr=60, rng=None):
    """Full joint detector: C3_obs, null mean/sd, excess, z."""
    p, counts = triple_hist(bits_abc)
    T = counts.sum()
    c3_obs = C3(p)
    mu, sd, _ = surrogate_null(p, T, n_surr=n_surr, rng=rng)
    excess = c3_obs - mu
    z = excess / sd if sd > 1e-12 else float('nan')
    return dict(c3_obs=c3_obs, null_mean=mu, null_sd=sd, excess=excess, z=z, T=int(T))


# =========================================================================
# GATE — validate machinery on synthetic BEFORE any hardware
# =========================================================================
if __name__ == "__main__":
    ln2 = np.log(2)
    print("=" * 70)
    print("GATE — C3 machinery self-test (must pass before hardware)")
    print("=" * 70)

    # (a) EXACT distributions
    parity = np.zeros((2, 2, 2))
    for a, b in product(range(2), repeat=2):
        parity[a, b, a ^ b] = 0.25
    indep = np.full((2, 2, 2), 1.0 / 8)
    print(f"(a) EXACT three-coin parity: C3 = {C3(parity):.6f}  (target ln2 = {ln2:.6f})")
    print(f"(a) EXACT three independent: C3 = {C3(indep):.6e}  (target 0)")
    ok_a = abs(C3(parity) - ln2) < 1e-6 and abs(C3(indep)) < 1e-9

    # (b) SAMPLED data at hardware-scale T, full pipeline incl. surrogate null
    rng = np.random.default_rng(20260724)
    T = 4000
    # parity samples
    a = rng.integers(0, 2, T); b = rng.integers(0, 2, T); c = a ^ b
    par_bits = np.stack([a, b, c], axis=1)
    jd_par = joint_detector(par_bits, n_surr=60, rng=rng)
    pm_par = pair_meter(par_bits)
    # independent samples
    a = rng.integers(0, 2, T); b = rng.integers(0, 2, T); c = rng.integers(0, 2, T)
    ind_bits = np.stack([a, b, c], axis=1)
    jd_ind = joint_detector(ind_bits, n_surr=60, rng=rng)
    pm_ind = pair_meter(ind_bits)

    print(f"\n(b) SAMPLED parity (T={T}): C3_obs={jd_par['c3_obs']:.4f} "
          f"null={jd_par['null_mean']:.4f}+/-{jd_par['null_sd']:.4f} "
          f"excess={jd_par['excess']:.4f} z={jd_par['z']:.1f} | "
          f"pair max|corr|={pm_par[0]:.4f} maxMI={pm_par[1]:.2e}")
    print(f"(b) SAMPLED indep  (T={T}): C3_obs={jd_ind['c3_obs']:.4f} "
          f"null={jd_ind['null_mean']:.4f}+/-{jd_ind['null_sd']:.4f} "
          f"excess={jd_ind['excess']:.4f} z={jd_ind['z']:.1f} | "
          f"pair max|corr|={pm_ind[0]:.4f} maxMI={pm_ind[1]:.2e}")

    ok_b = (jd_par['z'] > 5) and (abs(jd_ind['z']) < 3)
    print("\nGATE VERDICT:", "PASS" if (ok_a and ok_b) else "FAIL",
          f"(exact ok={ok_a}, sampled ok={ok_b})")
