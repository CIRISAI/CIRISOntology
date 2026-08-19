"""Core split-half / permutation machinery for the eigen-alignment experiment.

Every statistic follows EIGEN_ALIGNMENT_PREREG.md SS4-7 verbatim:
  * Delta_i = normalize( e_hat(after) - e_hat(before) )
  * nuisance residualization fit on the FITTING half, applied to the held-out half
  * contrasts on the fitting half, centring + SVD + statistics on the held-out half
  * Omega(k) = (1/rank(B)) * ||U_k^T B||_F^2 ; a_j = ||B^T u_j||^2
  * eta_k = A_k * rho_k  (LOKO, S5.2)
  * combination rule: median over the 200 splits; null = distribution of that median
    over the 500 whole-pipeline permutations (null-of-medians)
"""
import numpy as np
from common import maxt_stepdown, kmeans

JMAX = 40
KS = [5, 7, 9, 11, 13, 15, 20, 30, 40]


def unit(V):
    return V / np.linalg.norm(V, axis=-1, keepdims=True)


def make_splits(strata, nsplit, seed):
    rng = np.random.default_rng(seed)
    n = len(strata)
    cells = {}
    for i, s in enumerate(strata):
        cells.setdefault(s, []).append(i)
    out = np.zeros((nsplit, n), dtype=bool)
    for t in range(nsplit):
        for s, idx in cells.items():
            idx = np.array(idx)
            rng.shuffle(idx)
            k = len(idx) // 2
            if len(idx) % 2 == 1 and rng.random() < 0.5:
                k += 1
            out[t, idx[:k]] = True
    return out


def onehot(labels, K):
    P = np.zeros((len(labels), K))
    P[np.arange(len(labels)), labels] = 1.0
    return P


class Prepared:
    """Per split-direction: nuisance beta (fit on F), held-out top-JMAX PCs."""

    def __init__(self, X, Z, splits, jmax=JMAX, residualize=True):
        self.X = X
        self.Z = Z
        self.n, self.d = X.shape
        S = splits.shape[0]
        self.S = S
        self.nsd = 2 * S
        Hf = np.zeros((self.nsd, self.n))
        for s in range(S):
            Hf[2 * s] = splits[s].astype(float)
            Hf[2 * s + 1] = (~splits[s]).astype(float)
        self.Hf = Hf
        self.He = 1.0 - Hf
        self.betas = np.zeros((self.nsd, Z.shape[1], self.d))
        self.U = np.zeros((self.nsd, self.d, jmax))
        self.evr = np.zeros((self.nsd, jmax))
        for sd in range(self.nsd):
            F = Hf[sd] > 0
            E = ~F
            if residualize:
                b = np.linalg.lstsq(Z[F], X[F], rcond=None)[0]
            else:
                b = np.zeros((Z.shape[1], self.d))
            self.betas[sd] = b
            Xres = X - Z @ b
            Xe = Xres[E]
            Xe = Xe - Xe.mean(0)
            try:
                u, s_, vt = np.linalg.svd(Xe, full_matrices=False)
            except np.linalg.LinAlgError:
                # gesdd nonconvergence on a valid matrix: fall back to gesvd
                from scipy.linalg import svd as _ssvd
                u, s_, vt = _ssvd(Xe, full_matrices=False, lapack_driver='gesvd')
            self.U[sd] = vt[:jmax].T
            ev = s_ ** 2
            self.evr[sd] = ev[:jmax] / ev.sum()


def _sums(W, X):
    S, K, n = W.shape
    return (W.reshape(S * K, n) @ X).reshape(S, K, -1)


def contrasts_batch(prep, P, side='F'):
    """P (n,K) one-hot -> residualized one-vs-rest contrasts (nsd,K,d)."""
    H = prep.Hf if side == 'F' else prep.He
    K = P.shape[1]
    W = H[:, None, :] * P.T[None, :, :]
    cnt = W.sum(axis=2)
    SX = _sums(W, prep.X)
    SZ = _sums(W, prep.Z)
    tot = cnt.sum(axis=1)
    TX = SX.sum(axis=1)
    TZ = SZ.sum(axis=1)
    with np.errstate(invalid='ignore', divide='ignore'):
        mX = SX / cnt[:, :, None]
        mZ = SZ / cnt[:, :, None]
        nX = (TX[:, None, :] - SX) / (tot[:, None] - cnt)[:, :, None]
        nZ = (TZ[:, None, :] - SZ) / (tot[:, None] - cnt)[:, :, None]
    C = (mX - nX) - np.einsum('skz,szd->skd', (mZ - nZ), prep.betas)
    bad = cnt == 0
    C[bad] = 0.0
    return C, cnt


def contrasts_batch_persd(prep, Psd, side='F'):
    """Psd (nsd,n,K) per-split-direction labels."""
    H = prep.Hf if side == 'F' else prep.He
    W = H[:, :, None] * Psd
    W = np.transpose(W, (0, 2, 1))
    cnt = W.sum(axis=2)
    SX = _sums(W, prep.X)
    SZ = _sums(W, prep.Z)
    tot = cnt.sum(axis=1)
    TX = SX.sum(axis=1)
    TZ = SZ.sum(axis=1)
    with np.errstate(invalid='ignore', divide='ignore'):
        mX = SX / cnt[:, :, None]
        mZ = SZ / cnt[:, :, None]
        nX = (TX[:, None, :] - SX) / (tot[:, None] - cnt)[:, :, None]
        nZ = (TZ[:, None, :] - SZ) / (tot[:, None] - cnt)[:, :, None]
    C = (mX - nX) - np.einsum('skz,szd->skd', (mZ - nZ), prep.betas)
    C[cnt == 0] = 0.0
    return C, cnt


def omega_a_batch(C, U, ks=KS, jmax=JMAX, drop=None):
    """C (nsd,K,d), U (nsd,d,jmax). drop: boolean (K,) columns to exclude from B."""
    if drop is not None and drop.any():
        C = C[:, ~drop, :]
    G = np.einsum('skd,sld->skl', C, C)
    w, V = np.linalg.eigh(G)
    thr = np.maximum(w.max(axis=1, keepdims=True), 1e-300) * 1e-9
    keep = w > thr
    winv = np.where(keep, 1.0 / np.where(keep, w, 1.0), 0.0)
    Gp = np.einsum('smi,si,sni->smn', V, winv, V)
    r = keep.sum(axis=1).astype(float)
    CU = np.einsum('skd,sdj->skj', C, U[:, :, :jmax])
    a = np.einsum('skj,skl,slj->sj', CU, Gp, CU)
    om = {k: a[:, :k].sum(axis=1) / r for k in ks if k <= jmax}
    return om, a, r


def split_reduce(v):
    """(nsd,...) -> (S,...) by averaging the two directions of each split."""
    return 0.5 * (v[0::2] + v[1::2])


def full_stats(prep, P, ks=KS, want_eta=True, drop=None):
    """One pass of the whole pipeline for a given labelling."""
    CF, cntF = contrasts_batch(prep, P, 'F')
    om, a, r = omega_a_batch(CF, prep.U, ks, drop=drop)
    out = {'omega': {k: float(np.median(split_reduce(v))) for k, v in om.items()},
           'omega_splits': {k: split_reduce(v) for k, v in om.items()},
           'a': split_reduce(a), 'rank': float(np.median(r))}
    if want_eta:
        CE, cntE = contrasts_batch(prep, P, 'E')
        nF = np.linalg.norm(CF, axis=2)
        nE = np.linalg.norm(CE, axis=2)
        gF = CF / np.where(nF[:, :, None] > 0, nF[:, :, None], 1)
        gE = CE / np.where(nE[:, :, None] > 0, nE[:, :, None], 1)
        CU11 = np.einsum('skd,sdj->skj', gF, prep.U[:, :, :11])
        A = (CU11 ** 2).sum(axis=2)                       # (nsd,K)
        cos = np.abs(np.einsum('skd,skd->sk', gF, gE))    # (nsd,K)
        A_s = split_reduce(A)
        cos_s = cos[0::2]
        out['A'] = np.median(A_s, axis=0)
        out['rho'] = np.median(cos_s, axis=0)
        out['eta'] = out['A'] * out['rho']
    return out


def perm_labels(labels, nperm, seed, blocks=None):
    rng = np.random.default_rng(seed)
    out = np.zeros((nperm, len(labels)), dtype=np.int64)
    if blocks is None:
        for b in range(nperm):
            out[b] = rng.permutation(labels)
    else:
        ub = np.unique(blocks)
        for b in range(nperm):
            l = labels.copy()
            for u in ub:
                m = blocks == u
                l[m] = rng.permutation(labels[m])
            out[b] = l
    return out


def run_null(prep, permmat, K, ks=KS, want_eta=True, log=None, drop=None):
    res = {'omega': {k: [] for k in ks if k <= JMAX}, 'a': [], 'eta': [], 'A': [], 'rho': []}
    for b in range(permmat.shape[0]):
        P = onehot(permmat[b], K)
        s = full_stats(prep, P, ks, want_eta=want_eta, drop=drop)
        for k in res['omega']:
            res['omega'][k].append(s['omega'][k])
        res['a'].append(np.median(s['a'], axis=0))
        if want_eta:
            res['eta'].append(s['eta'])
            res['A'].append(s['A'])
            res['rho'].append(s['rho'])
        if log and (b + 1) % 50 == 0:
            print(f'   {log}: {b+1}/{permmat.shape[0]}', flush=True)
    res['omega'] = {k: np.array(v) for k, v in res['omega'].items()}
    res['a'] = np.array(res['a'])
    for key in ['eta', 'A', 'rho']:
        if res[key]:
            res[key] = np.array(res[key])
    return res


def perm_p(obs, null):
    return (1.0 + int((np.asarray(null) >= obs).sum())) / (1.0 + len(null))


def loo_auc_scores(X, labels, K):
    """Leave-one-out one-vs-rest centroid-contrast scores, full d-space."""
    n, d = X.shape
    P = onehot(labels, K)
    S = P.T @ X
    cnt = P.sum(0)
    tot = X.sum(0)
    N = float(n)
    sc = np.zeros((n, K))
    for i in range(n):
        Si = S - P[i][:, None] * X[i][None, :]
        ci = cnt - P[i]
        toti = tot - X[i]
        with np.errstate(invalid='ignore', divide='ignore'):
            mk = Si / ci[:, None]
            mn = (toti[None, :] - Si) / (N - 1 - ci)[:, None]
        C = mk - mn
        C = C / np.linalg.norm(C, axis=1, keepdims=True)
        sc[i] = C @ X[i]
    return sc


def auc(y, s):
    o = np.argsort(s)
    r = np.empty(len(s))
    sr = s[o]
    i = 0
    rank = np.arange(1, len(s) + 1, dtype=float)
    while i < len(s):
        j = i
        while j + 1 < len(s) and sr[j + 1] == sr[i]:
            j += 1
        rank[i:j + 1] = (i + j + 2) / 2.0
        i = j + 1
    r[o] = rank
    n1 = y.sum()
    n0 = len(y) - n1
    if n1 == 0 or n0 == 0:
        return np.nan
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


def auc_boot(y, s, nboot=2000, seed=1):
    rng = np.random.default_rng(seed)
    n = len(y)
    vals = []
    for _ in range(nboot):
        idx = rng.integers(0, n, n)
        if y[idx].sum() in (0, len(idx)):
            continue
        vals.append(auc(y[idx], s[idx]))
    v = np.array(vals)
    return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))
