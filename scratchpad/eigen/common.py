"""Shared numerics for the eigen-alignment experiment (EIGEN_ALIGNMENT_PREREG.md).

All statistics follow the prereg's frozen definitions:
  Omega(k) = (1/r) * ||U_k^T B||_F^2 ,  r = rank(B)          (S6)
  a_j      = ||B^T u_j||^2                                    (S6)
  eta_k    = A_k * rho_k                                      (S5.2)

B is an orthonormal basis of the span of the 12 one-vs-rest centroid contrasts C
(1024 x 12, rank 11 by the counting identity of S5.1).  We never materialise B:
  ||U^T B||_F^2 = tr(P_C P_U) = tr( pinv(C^T C) (C^T U)(C^T U)^T )
which is exact and needs only the 12x12 Gram and the 12xk cross-product.
"""
import numpy as np

TOL_REL = 1e-9


def class_sums(X, labels, n_classes):
    """(n_classes, d) sums and (n_classes,) counts."""
    d = X.shape[1]
    S = np.zeros((n_classes, d), dtype=X.dtype)
    cnt = np.zeros(n_classes, dtype=np.int64)
    np.add.at(S, labels, X)
    np.add.at(cnt, labels, 1)
    return S, cnt


def contrasts_from_sums(S, cnt):
    """One-vs-rest centroid contrasts c_k = m_k - m_{not k}  (un-normalised).

    Classes with cnt == 0 return a zero row (they are dropped by the rank logic).
    """
    N = cnt.sum()
    tot = S.sum(axis=0)
    with np.errstate(invalid='ignore', divide='ignore'):
        m_k = S / cnt[:, None]
        m_nk = (tot[None, :] - S) / (N - cnt)[:, None]
    C = m_k - m_nk
    C[cnt == 0] = 0.0
    return C


def contrasts(X, labels, n_classes):
    S, cnt = class_sums(X, labels, n_classes)
    return contrasts_from_sums(S, cnt)


def gram_pinv_rank(C, tol_rel=TOL_REL):
    """pinv of C C^T (the 12x12 Gram of the contrast rows) and its numerical rank."""
    G = C @ C.T
    w, V = np.linalg.eigh(G)
    thr = max(w.max(), 0.0) * tol_rel
    keep = w > thr
    winv = np.where(keep, 1.0 / np.where(keep, w, 1.0), 0.0)
    return (V * winv) @ V.T, int(keep.sum())


def omega_and_a(C, U, ks, rank_override=None):
    """Return dict k->Omega(k) and a_j for j over U's columns.

    C : (m, d) contrast rows.   U : (d, J) orthonormal held-out principal directions.
    """
    Gp, r = gram_pinv_rank(C)
    if rank_override is not None:
        r = rank_override
    CU = C @ U                      # (m, J)
    # a_j = u_j^T P_C u_j = (C u_j)^T Gp (C u_j)
    a = np.einsum('ij,ik,kj->j', CU, Gp, CU)
    om = {}
    for k in ks:
        if k <= U.shape[1]:
            om[k] = float(a[:k].sum() / r)
    return om, a, r


def kmeans(X, k, seed, n_init=3, iters=30):
    """Plain k-means++ (no sklearn in this env). Returns labels."""
    rng = np.random.default_rng(seed)
    n = X.shape[0]
    best_lab, best_in = None, np.inf
    for _ in range(n_init):
        # k-means++ init
        idx = [int(rng.integers(n))]
        d2 = ((X - X[idx[0]]) ** 2).sum(1)
        for _ in range(k - 1):
            p = d2 / d2.sum() if d2.sum() > 0 else np.full(n, 1.0 / n)
            j = int(rng.choice(n, p=p))
            idx.append(j)
            d2 = np.minimum(d2, ((X - X[j]) ** 2).sum(1))
        Cn = X[idx].copy()
        lab = np.zeros(n, dtype=np.int64)
        for _ in range(iters):
            D = ((X ** 2).sum(1)[:, None] - 2 * X @ Cn.T + (Cn ** 2).sum(1)[None, :])
            newlab = D.argmin(1)
            if np.array_equal(newlab, lab):
                lab = newlab
                break
            lab = newlab
            for c in range(k):
                m = lab == c
                if m.any():
                    Cn[c] = X[m].mean(0)
                else:
                    Cn[c] = X[int(rng.integers(n))]
        D = ((X ** 2).sum(1)[:, None] - 2 * X @ Cn.T + (Cn ** 2).sum(1)[None, :])
        inertia = float(D[np.arange(n), lab].sum())
        if inertia < best_in:
            best_in, best_lab = inertia, lab.copy()
    return best_lab


def maxt_stepdown(obs, null, alpha=0.05):
    """Westfall-Young permutation maxT step-down.

    obs  : (J,) observed statistics (larger = more significant)
    null : (B, J) null statistics
    Returns adjusted p-values (J,) and the number rejected at FWER alpha.
    """
    J = obs.shape[0]
    B = null.shape[0]
    order = np.argsort(-obs)              # descending
    obs_s = obs[order]
    null_s = null[:, order]
    # successive maxima from the tail
    q = np.maximum.accumulate(null_s[:, ::-1], axis=1)[:, ::-1]   # q[:, j] = max over j..J-1
    p = (1.0 + (q >= obs_s[None, :]).sum(axis=0)) / (1.0 + B)
    p = np.maximum.accumulate(p)          # enforce monotonicity
    padj = np.empty(J)
    padj[order] = p
    nrej = 0
    for j in range(J):
        if p[j] <= alpha:
            nrej += 1
        else:
            break
    return padj, nrej


def parallel_analysis_rank(X, n_perm=100, seed=0, pct=95):
    """Horn parallel analysis on the centred cloud: count eigenvalues above the
    column-permuted null's `pct` percentile."""
    rng = np.random.default_rng(seed)
    Xc = X - X.mean(0)
    n, d = Xc.shape
    s = np.linalg.svd(Xc, compute_uv=False)
    ev = s ** 2
    m = min(n, d)
    nullev = np.empty((n_perm, m))
    for b in range(n_perm):
        Xp = np.empty_like(Xc)
        for j in range(d):
            Xp[:, j] = Xc[rng.permutation(n), j]
        Xp -= Xp.mean(0)
        sp = np.linalg.svd(Xp, compute_uv=False)
        nullev[b, :len(sp)] = sp ** 2
    thr = np.percentile(nullev, pct, axis=0)
    cnt = 0
    for i in range(m):
        if ev[i] > thr[i]:
            cnt += 1
        else:
            break
    return cnt, ev, thr
