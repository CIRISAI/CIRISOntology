"""S8 GAUGE at v2's geometry — SYNTHETIC ONLY, runs BEFORE any corpus text is embedded.

Prereg S8:
  geometry  : per-half n = 237, d = 1024, 11 classes at E2's exact half-sizes
              (AMENDMENTS.md A2 resolves the prereg's 236-sum vector to [18,20,20,20,20,
              20,20,20,20,29,30] = 237, which is the frozen construction's seed-0 half).
  worlds    : planted rank 6, planted rank 10, and "rank 10 + 3 structured non-kind
              directions" (S8's imported gauge.py declaration: 13 class-carrying
              between-class directions are not constructible at K = 11, so the r=13 cell
              asks whether R_kind falsely counts strong NON-kind directions).
  scales    : {0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0} x within-class sigma.
              Addition 1: the scale-0 row is MANDATORY, and defines
              Omega_gauge*(s) = Omega_gauge(s) - Omega_gauge(0).
  draws     : 200 per cell.
  returns   : sigma_R, R-hat (mean recovered R_kind) at every cell, rho_gauge at every
              cell, per-rank PC replication for j in {1,2,3,5,8,10,11,13}.

The generative model is gauge.py's, re-parameterised to NK = 11 / rank(B) = 10.  gauge.py
itself is NOT modified (it is hard-wired to NK = 12 and has no rank10 world, as S8 records).
"""
import json, os, sys, time
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen2run')
sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen')
import e2lib as L
from common import contrasts, maxt_stepdown

D = 1024
KS = [5, 7, 9, 10, 11, 13, 15, 20, 30, 40]
JMAX = 40
GRID = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0]
NDRAW = 200
NPERM_GAUGE = 200
PC_J = [1, 2, 3, 5, 8, 10, 11, 13]
CLASS_SIZES = [18, 20, 20, 20, 20, 20, 20, 20, 20, 29, 30]     # AMENDMENTS.md A2; sums 237
NK = 11
WORLDS = ['rank6', 'rank10', 'rank10p3']
SEED0 = 20260819


def batched_stats(Cb, U, ks, jmax):
    G = np.einsum('bmd,bnd->bmn', Cb, Cb)
    w, V = np.linalg.eigh(G)
    thr = np.maximum(w.max(axis=1, keepdims=True), 1e-300) * 1e-9
    keep = w > thr
    winv = np.where(keep, 1.0 / np.where(keep, w, 1.0), 0.0)
    Gp = np.einsum('bmi,bi,bni->bmn', V, winv, V)
    r = keep.sum(axis=1).astype(float)
    CU = np.einsum('bmd,dj->bmj', Cb, U[:, :jmax])
    a = np.einsum('bij,bik,bkj->bj', CU, Gp, CU)
    oms = {k: a[:, :k].sum(axis=1) / r for k in ks if k <= jmax}
    return oms, a, r


def onehot_batch(labmat, K):
    B, n = labmat.shape
    M = np.zeros((B, K, n))
    bidx = np.repeat(np.arange(B), n)
    M[bidx, labmat.ravel(), np.tile(np.arange(n), B)] = 1.0
    return M


def contrasts_from_M(M, X):
    B, K, n = M.shape
    cnt = M.sum(axis=2)
    S = np.einsum('bkn,nd->bkd', M, X)
    tot = S.sum(axis=1)
    N = float(n)
    m_k = S / cnt[:, :, None]
    m_nk = (tot[:, None, :] - S) / (N - cnt)[:, :, None]
    return m_k - m_nk


def make_draw(rng, world, scale, labels):
    n = labels.shape[0]
    if world == 'rank6':
        rdim, extra = 6, 0
    elif world == 'rank10':
        rdim, extra = 10, 0
    elif world == 'rank10p3':
        rdim, extra = 10, 3
    else:
        raise ValueError(world)
    V = np.linalg.qr(rng.standard_normal((D, rdim + extra)))[0]
    Vc, Ve = V[:, :rdim], V[:, rdim:]
    coef = rng.standard_normal((NK, rdim))
    MU = scale * (coef @ Vc.T)
    halves = []
    for _ in range(2):
        Xh = rng.standard_normal((n, D)) + MU[labels]
        if extra:
            Xh += (rng.standard_normal((n, extra)) * scale) @ Ve.T
        halves.append(Xh)
    return halves


def run_cell(args):
    world, scale, seed = args
    t0 = time.time()
    rng = np.random.default_rng(seed)
    labels = np.repeat(np.arange(NK), CLASS_SIZES)
    out = {'omega': {k: [] for k in KS}, 'rkind': [], 'rho_gauge': [],
           'pcrep': {j: [] for j in PC_J}, 'rank_b': []}
    for _ in range(NDRAW):
        X1, X2 = make_draw(rng, world, scale, labels)
        X2c = X2 - X2.mean(0)
        U2 = np.linalg.svd(X2c, full_matrices=False)[2].T
        C1 = contrasts(X1, labels, NK)
        oms, a, r = batched_stats(C1[None], U2, KS, JMAX)
        for k in KS:
            out['omega'][k].append(float(oms[k][0]))
        out['rank_b'].append(float(r[0]))
        C2 = contrasts(X2, labels, NK)
        n1 = C1 / np.linalg.norm(C1, axis=1, keepdims=True)
        n2 = C2 / np.linalg.norm(C2, axis=1, keepdims=True)
        out['rho_gauge'].append(float(np.median(np.abs((n1 * n2).sum(1)))))
        X1c = X1 - X1.mean(0)
        U1 = np.linalg.svd(X1c, full_matrices=False)[2].T
        for j in PC_J:
            out['pcrep'][j].append(float(abs(U1[:, j - 1] @ U2[:, j - 1])))
        perm = np.array([rng.permutation(labels) for _ in range(NPERM_GAUGE)])
        Cb = contrasts_from_M(onehot_batch(perm, NK), X1)
        _, anull, _ = batched_stats(Cb, U2, KS, JMAX)
        _, nrej = maxt_stepdown(a[0], anull, alpha=0.05)
        out['rkind'].append(int(nrej))
    row = {'world': world, 'scale': scale, 'n_per_half': int(sum(CLASS_SIZES)),
           'ndraw': NDRAW, 'nperm_gauge': NPERM_GAUGE,
           'omega_median': {str(k): float(np.median(v)) for k, v in out['omega'].items()},
           'omega11_p2.5': float(np.percentile(out['omega'][11], 2.5)),
           'omega11_p97.5': float(np.percentile(out['omega'][11], 97.5)),
           'rkind_mean': float(np.mean(out['rkind'])),
           'rkind_sd': float(np.std(out['rkind'], ddof=1)),
           'rkind_median': float(np.median(out['rkind'])),
           'rho_gauge_median': float(np.median(out['rho_gauge'])),
           'pcrep_median': {str(j): float(np.median(v)) for j, v in out['pcrep'].items()},
           'rank_b_median': float(np.median(out['rank_b'])),
           'seconds': time.time() - t0}
    return f'{world}@{scale}', row


def main():
    t0 = time.time()
    os.environ.setdefault('OMP_NUM_THREADS', '3')
    cells = [(w, s, SEED0 + 1000 * wi + int(s * 10))
             for wi, w in enumerate(WORLDS) for s in GRID]
    part = os.path.join(L.OUT, 'gauge11_partial.json')
    res = {}
    if os.path.exists(part):
        res = json.load(open(part)).get('cells', {})
        print(f'RESUME: {len(res)} cells already on disk', flush=True)
    todo = [c for c in cells if f'{c[0]}@{c[1]}' not in res]
    meta = {'grid': GRID, 'worlds': WORLDS, 'ndraw': NDRAW, 'd': D,
            'class_sizes': CLASS_SIZES, 'n_per_half': int(sum(CLASS_SIZES)),
            'nperm_gauge': NPERM_GAUGE, 'pc_j': PC_J, 'nk': NK}
    with Pool(9) as pool:
        for key, row in pool.imap_unordered(run_cell, todo):
            res[key] = row
            L.atomic_json({'_meta': meta, 'cells': res}, part)
            print(f'{key}: Om11={row["omega_median"]["11"]:.4f} '
                  f'Rk={row["rkind_mean"]:.2f}+-{row["rkind_sd"]:.2f} '
                  f'rho={row["rho_gauge_median"]:.3f} [{time.time()-t0:.0f}s]', flush=True)
    L.atomic_json({'_meta': meta, 'cells': res}, os.path.join(L.OUT, 'gauge11_raw.json'))

    # ---- S8's derived quantities -------------------------------------------------
    z0 = {w: res[f'{w}@0.0']['omega_median']['11'] for w in WORLDS}
    z0_10 = {w: res[f'{w}@0.0']['omega_median']['10'] for w in WORLDS}
    table = []
    for s in GRID:
        r = res[f'rank10@{s}']
        table.append({'scale': s,
                      'omega11': r['omega_median']['11'],
                      'omega11_excess': r['omega_median']['11'] - z0['rank10'],
                      'omega10': r['omega_median']['10'],
                      'omega10_excess': r['omega_median']['10'] - z0_10['rank10'],
                      'sigma_R_cell': r['rkind_sd'], 'Rhat': r['rkind_mean'],
                      'rho_gauge': r['rho_gauge_median']})
    adm = [t for t in table if abs(t['Rhat'] - 10.0) <= 3.0]
    sigma_R = max([t['sigma_R_cell'] for t in adm]) if adm else None
    summary = {'scale0_omega11': z0, 'rank10_table': table,
               'admissible_scales': [t['scale'] for t in adm],
               'sigma_R': sigma_R,
               'sigma_R_rule': 'largest across-scale s.d. of R_kind at planted rank 10 over '
                               'scales where |Rhat - 10| <= 3; undefined (=> treated as '
                               '> 1.5, V8 fires) if the admissible set is empty',
               'V8_fires_if_sigma_gt': 1.5, 'V3b_fires_if_rho_lt': 0.30,
               'elapsed_s': time.time() - t0}
    L.atomic_json(summary, os.path.join(L.OUT, 'gauge11_summary.json'))
    print(json.dumps(summary, indent=1), flush=True)
    L.done_marker('GAUGE', {'artifact': os.path.join(L.OUT, 'gauge11_raw.json'),
                            'summary': os.path.join(L.OUT, 'gauge11_summary.json'),
                            'sigma_R': sigma_R, 'seconds': time.time() - t0,
                            'ts': time.strftime('%Y-%m-%dT%H:%M:%S')})
    print('GAUGE DONE', time.time() - t0, flush=True)


if __name__ == '__main__':
    main()
