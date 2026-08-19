"""S8 rank-resolution gauge (re-staked grid) + S22 Ruling 3 two-world LOKO gauge.

SYNTHETIC ONLY.  No corpus text, no embedding.  Runs BEFORE any embedding exists.

Planted worlds
--------------
rank7  : 12 class means constrained to a 7-dim planted subspace.
rank11 : 12 class means constrained to an 11-dim planted subspace (they span 11).
rank13 : as rank11, PLUS 2 extra structured (non-kind) directions carrying the same
         per-direction variance as an average class direction.  Rationale, recorded:
         with a 12-class partition the between-class subspace has rank exactly 11
         (S5.1 counting identity), so "13 class-carrying between-class directions"
         is not constructible.  The informative question the r=13 cell can answer is
         whether R_kind falsely counts strong NON-kind directions, which is exactly
         what the "not 13" clause needs.  This is an implementation specification of
         a generative model the prereg leaves unspecified; it is declared here.
worldI : Ruling 3 (i) -- 11 content classes + 1 relation-like class whose label is
         assigned by a frame-conditional rule: its items carry the content mean of a
         uniformly-random content class, so the label is not a content cluster.
worldII: Ruling 3 (ii) -- 12 content classes.
"""
import json, sys, time
import numpy as np
sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen')
from common import contrasts, maxt_stepdown

D = 1024
KS = [5, 7, 9, 11, 13, 15, 20, 30, 40]
JMAX = 40
GRID = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 9.0]
NDRAW = 200
NPERM_GAUGE = 200          # gauge-internal maxT permutations (prereg pins 500 only for N1/N1b on the corpus)
PC_J = [1, 2, 3, 5, 8, 11, 13]
CLASS_SIZES = [12, 12] + [10] * 10      # Corpus A half sizes: two 24-item kinds -> 12, ten 20-item kinds -> 10
NK = 12
RECORD_IDX = 11                          # a size-10 class, as testimonial (20 items) is


def batched_stats(Cb, U, ks, jmax):
    """Cb (B,m,d) contrast rows; U (d,J). Returns Omega dict arrays and a (B,J)."""
    G = np.einsum('bmd,bnd->bmn', Cb, Cb)
    w, V = np.linalg.eigh(G)
    thr = w.max(axis=1, keepdims=True) * 1e-9
    keep = w > thr
    winv = np.where(keep, 1.0 / np.where(keep, w, 1.0), 0.0)
    Gp = np.einsum('bmi,bi,bni->bmn', V, winv, V)
    r = keep.sum(axis=1).astype(float)
    CU = np.einsum('bmd,dj->bmj', Cb, U[:, :jmax])
    a = np.einsum('bij,bik,bkj->bj', CU, Gp, CU)
    oms = {k: a[:, :k].sum(axis=1) / r for k in ks if k <= jmax}
    return oms, a, r


def onehot_batch(labmat, K):
    """labmat (B,n) -> (B*K, n) indicator/count-normalised sum operator."""
    B, n = labmat.shape
    M = np.zeros((B, K, n))
    bidx = np.repeat(np.arange(B), n)
    M[bidx, labmat.ravel(), np.tile(np.arange(n), B)] = 1.0
    return M


def contrasts_from_M(M, X):
    """M (B,K,n) 0/1 membership -> contrasts (B,K,d)."""
    B, K, n = M.shape
    cnt = M.sum(axis=2)                        # (B,K)
    S = np.einsum('bkn,nd->bkd', M, X)
    tot = S.sum(axis=1)                        # (B,d)
    N = float(n)
    m_k = S / cnt[:, :, None]
    m_nk = (tot[:, None, :] - S) / (N - cnt)[:, :, None]
    return m_k - m_nk


def make_draw(rng, world, scale, labels):
    n = labels.shape[0]
    if world == 'rank7':
        rdim, extra, nclass_content = 7, 0, NK
    elif world == 'rank11':
        rdim, extra, nclass_content = 11, 0, NK
    elif world == 'rank13':
        rdim, extra, nclass_content = 11, 2, NK
    elif world == 'worldI':
        rdim, extra, nclass_content = 11, 0, NK - 1
    elif world == 'worldII':
        rdim, extra, nclass_content = 11, 0, NK
    else:
        raise ValueError(world)
    V = np.linalg.qr(rng.standard_normal((D, rdim + extra)))[0]
    Vc, Ve = V[:, :rdim], V[:, rdim:]
    # per-COORDINATE planted scale s (S8.1's arithmetic: ||mu_k|| = s*sqrt(r))
    coef = rng.standard_normal((nclass_content, rdim))
    MU = np.zeros((NK, D))
    MU[:nclass_content] = scale * (coef @ Vc.T)
    if world == 'worldI':
        # relation-like class: no content mean of its own; per-item topic drawn from
        # the 11 content classes (label assigned by a frame rule, not a content cluster)
        pass
    halves = []
    for _ in range(2):
        Xh = rng.standard_normal((n, D))
        mu_item = MU[labels]
        if world == 'worldI':
            rec = labels == RECORD_IDX
            pick = rng.integers(0, nclass_content, size=int(rec.sum()))
            mu_item = mu_item.copy()
            mu_item[rec] = MU[:nclass_content][pick]
        Xh += mu_item
        if extra:
            load = rng.standard_normal((n, extra)) * scale
            Xh += load @ Ve.T
        halves.append(Xh)
    return halves


def run_cell(world, scale, ndraw, seed, want_rkind):
    rng = np.random.default_rng(seed)
    labels = np.repeat(np.arange(NK), CLASS_SIZES)
    n = labels.shape[0]
    out = {'omega11': [], 'rkind': [], 'rho_gauge': [], 'pcrep': {j: [] for j in PC_J},
           'eta': [], 'A': [], 'rho_k': [], 'rank_b': []}
    for d in range(ndraw):
        X1, X2 = make_draw(rng, world, scale, labels)
        X2c = X2 - X2.mean(0)
        U2 = np.linalg.svd(X2c, full_matrices=False)[2].T          # (D, 124)
        C1 = contrasts(X1, labels, NK)
        oms, a, r = batched_stats(C1[None], U2, KS, JMAX)
        out['omega11'].append(float(oms[11][0]))
        out['rank_b'].append(float(r[0]))
        # centroid replication and PC replication across the two independent halves
        C2 = contrasts(X2, labels, NK)
        n1 = C1 / np.linalg.norm(C1, axis=1, keepdims=True)
        n2 = C2 / np.linalg.norm(C2, axis=1, keepdims=True)
        cosk = np.abs((n1 * n2).sum(1))
        out['rho_gauge'].append(float(np.median(cosk)))
        X1c = X1 - X1.mean(0)
        U1 = np.linalg.svd(X1c, full_matrices=False)[2].T
        for j in PC_J:
            out['pcrep'][j].append(float(abs(U1[:, j - 1] @ U2[:, j - 1])))
        # LOKO eta per draw: A_k on held-out top-11, rho_k = |cos| across halves
        CU11 = n1 @ U2[:, :11]
        A_k = (CU11 ** 2).sum(1)
        out['A'].append(A_k.tolist())
        out['rho_k'].append(cosk.tolist())
        out['eta'].append((A_k * cosk).tolist())
        if want_rkind:
            perm = np.array([rng.permutation(labels) for _ in range(NPERM_GAUGE)])
            M = onehot_batch(perm, NK)
            Cb = contrasts_from_M(M, X1)
            _, anull, _ = batched_stats(Cb, U2, KS, JMAX)
            _, nrej = maxt_stepdown(a[0], anull, alpha=0.05)
            out['rkind'].append(int(nrej))
    return out


def main():
    t0 = time.time()
    res = {'grid': GRID, 'ndraw': NDRAW, 'nperm_gauge': NPERM_GAUGE,
           'class_sizes': CLASS_SIZES, 'd': D, 'cells': {}}
    seed = 20260819
    for wi, world in enumerate(['rank7', 'rank11', 'rank13']):
        for si, s in enumerate(GRID):
            key = f'{world}@{s}'
            o = run_cell(world, s, NDRAW, seed + 1000 * wi + si, want_rkind=True)
            res['cells'][key] = {
                'omega11_median': float(np.median(o['omega11'])),
                'omega11_p2.5': float(np.percentile(o['omega11'], 2.5)),
                'omega11_p97.5': float(np.percentile(o['omega11'], 97.5)),
                'rkind_mean': float(np.mean(o['rkind'])),
                'rkind_sd': float(np.std(o['rkind'], ddof=1)),
                'rkind_median': float(np.median(o['rkind'])),
                'rho_gauge_median': float(np.median(o['rho_gauge'])),
                'pcrep': {str(j): float(np.median(v)) for j, v in o['pcrep'].items()},
                'rank_b_median': float(np.median(o['rank_b'])),
            }
            print(f'{key}: Om11={res["cells"][key]["omega11_median"]:.4f} '
                  f'Rk={res["cells"][key]["rkind_mean"]:.2f}+-{res["cells"][key]["rkind_sd"]:.2f} '
                  f'rho={res["cells"][key]["rho_gauge_median"]:.3f} '
                  f'[{time.time()-t0:.0f}s]', flush=True)
    # Ruling 3 two worlds
    for wi, world in enumerate(['worldI', 'worldII']):
        for si, s in enumerate(GRID):
            key = f'{world}@{s}'
            o = run_cell(world, s, NDRAW, seed + 50000 + 1000 * wi + si, want_rkind=False)
            eta = np.array(o['eta'])                     # (ndraw, 12)
            content = [i for i in range(NK) if i != RECORD_IDX]
            below = eta[:, RECORD_IDX] < eta[:, content].min(axis=1)
            res['cells'][key] = {
                'omega11_median': float(np.median(o['omega11'])),
                'eta_median': np.median(eta, axis=0).tolist(),
                'A_median': np.median(np.array(o['A']), axis=0).tolist(),
                'rho_k_median': np.median(np.array(o['rho_k']), axis=0).tolist(),
                'frac_12th_below_min_content': float(below.mean()),
                'rho_gauge_median': float(np.median(o['rho_gauge'])),
            }
            print(f'{key}: Om11={res["cells"][key]["omega11_median"]:.4f} '
                  f'frac12th_below_min={res["cells"][key]["frac_12th_below_min_content"]:.3f} '
                  f'[{time.time()-t0:.0f}s]', flush=True)
    with open('/home/emoore/CIRISOntology/scratchpad/eigen/out/gauge_raw.json', 'w') as f:
        json.dump(res, f, indent=1)
    print('done', time.time() - t0)


if __name__ == '__main__':
    main()
