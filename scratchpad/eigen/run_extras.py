"""S18 steps 4(P1c), 7 (Babel + part_d), 8 (secondary embedder)."""
import json, os, sys, time, collections
import numpy as np
sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen')
import corpora, embed, pipeline as pl
from run_main import E, build, zmat_A, zmat_B, span_deciles, arm, keep_mask, PRIMARY, SECONDARY, OUT
from common import maxt_stepdown

NSPLIT, NPERM, SEED = 200, 500, 20260819
R = {}


def dedup_streams(rows, D, thresh=0.99):
    """V4, per stream: cluster items with cos(Di,Dj) > thresh; report and dedup."""
    info, keep = {}, []
    for st in sorted({r['stream'] for r in rows}):
        idx = np.array([i for i, r in enumerate(rows) if r['stream'] == st])
        S = D[idx] @ D[idx].T
        n = len(idx)
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        pairs = 0
        for i in range(n):
            for j in range(i + 1, n):
                if S[i, j] > thresh:
                    pairs += 1
                    a, b = find(i), find(j)
                    if a != b:
                        parent[a] = b
        groups = collections.defaultdict(list)
        for i in range(n):
            groups[find(i)].append(i)
        in_cluster = sum(len(v) for v in groups.values() if len(v) > 1)
        frac = in_cluster / n
        reps = [v[0] for v in groups.values()]
        info[st] = {'n': n, 'pairs_gt_thresh': pairs, 'frac_items_in_clusters': float(frac),
                    'n_eff': len(reps),
                    'action': 'drop_stream' if frac > 0.20 else ('dedup' if frac > 0.05 else 'keep')}
        if frac > 0.20:
            continue
        keep += [int(idx[i]) for i in (reps if frac > 0.05 else range(n))]
    return sorted(keep), info


def transfer(model, A, X_A, labels, ZA, blocks):
    B_all = corpora.corpus_B()
    kb = keep_mask(B_all)
    B = [r for r, k in zip(B_all, kb) if k]
    clB = build(B, model)
    XB = clB['delta']
    keep, v4 = dedup_streams(B, XB)
    Bk = [B[i] for i in keep]
    XBk = XB[keep]
    ZB = zmat_B(Bk)
    bB = np.linalg.lstsq(ZB, XBk, rcond=None)[0]
    XBr = XBk - ZB @ bB
    XBr = XBr - XBr.mean(0)
    U = np.linalg.svd(XBr, full_matrices=False)[2][:40].T

    bA = np.linalg.lstsq(ZA, X_A, rcond=None)[0]
    XAr = X_A - ZA @ bA

    def om(lab):
        P = pl.onehot(lab, 12)
        cnt = P.sum(0)
        S = P.T @ XAr
        tot = XAr.sum(0)
        N = float(len(lab))
        C = S / cnt[:, None] - (tot[None, :] - S) / (N - cnt)[:, None]
        G = C @ C.T
        w, V = np.linalg.eigh(G)
        keepw = w > w.max() * 1e-9
        Gp = (V * np.where(keepw, 1 / np.where(keepw, w, 1), 0)) @ V.T
        CU = C @ U
        a = np.einsum('ij,ik,kj->j', CU, Gp, CU)
        return float(a[:11].sum() / keepw.sum()), a
    obs, a_obs = om(labels)
    rng = np.random.default_rng(SEED + 9)
    n1, n1b = [], []
    for _ in range(NPERM):
        n1.append(om(rng.permutation(labels))[0])
        l = labels.copy()
        for u in np.unique(blocks):
            m = blocks == u
            l[m] = rng.permutation(labels[m])
        n1b.append(om(l)[0])
    return {'omega_B_11': obs, 'p_N1': pl.perm_p(obs, n1), 'p_N1b': pl.perm_p(obs, n1b),
            'null_N1_median': float(np.median(n1)), 'n_B_used': len(keep),
            'V4': v4, 'streams_after': dict(collections.Counter(r['stream'] for r in Bk)),
            'degenerate_B_dropped': [r['id'] for r, k in zip(B_all, kb) if not k]}


def babel(model, X_A, labels):
    BB = corpora.corpus_babel()
    clb = build(BB, model)
    Xb = clb['delta']
    P = pl.onehot(labels, 12)
    cnt = P.sum(0)
    S = P.T @ X_A
    tot = X_A.sum(0)
    N = float(len(labels))
    C = S / cnt[:, None] - (tot[None, :] - S) / (N - cnt)[:, None]
    C = C / np.linalg.norm(C, axis=1, keepdims=True)
    base = [i for i, k in enumerate(corpora.KINDS) if k != corpora.RECORD]
    Cb = C[base]
    names = [corpora.KINDS[i] for i in base]
    pred = np.argmax(Xb @ Cb.T, axis=1)
    true = np.array([names.index(r['kind_target']) for r in BB])
    acc = int((pred == true).sum())
    rng = np.random.default_rng(SEED + 21)
    null = np.array([int((pred == rng.permutation(true)).sum()) for _ in range(10000)])
    from scipy.stats import binom
    return {'top1_correct': acc, 'n': len(BB),
            'p_permutation': float((1 + (null >= acc).sum()) / 10001),
            'p_binomial_ge': float(1 - binom.cdf(acc - 1, len(BB), 1 / 11)),
            'null_mean': float(null.mean()),
            'pred': [names[p] for p in pred], 'true': [names[t] for t in true]}


def partd(model, X_A, labels):
    H = corpora.corpus_held()
    clh = build(H, model)
    Xh = clh['delta']
    P = pl.onehot(labels, 12)
    cnt = P.sum(0)
    S = P.T @ X_A
    tot = X_A.sum(0)
    N = float(len(labels))
    C = S / cnt[:, None] - (tot[None, :] - S) / (N - cnt)[:, None]
    C = C / np.linalg.norm(C, axis=1, keepdims=True)
    pred = np.argmax(Xh @ C.T, axis=1)
    true = np.array([corpora.KIDX[r['kind_target']] for r in H])
    return {'n': len(H), 'kinds_covered': sorted({r['kind_target'] for r in H}),
            'top1_correct': int((pred == true).sum()),
            'chance': 1 / 12,
            'pred': [corpora.KINDS[p] for p in pred],
            'true': [corpora.KINDS[t] for t in true]}


def main():
    t0 = time.time()
    A_all = corpora.corpus_A()
    A = [r for r, k in zip(A_all, keep_mask(A_all)) if k]
    labels = np.array([corpora.KIDX[r['kind_target']] for r in A])
    strata = [(r['kind_target'], r['domain']) for r in A]
    splits = pl.make_splits(strata, NSPLIT, SEED)
    ZA = zmat_A(A)
    blocks = span_deciles(A)

    for model, tag in ((PRIMARY, 'primary'), (SECONDARY, 'secondary')):
        cl = build(A, model)
        X = cl['delta']
        R[tag] = {}
        R[tag]['dim'] = int(X.shape[1])
        R[tag]['P1c'] = transfer(model, A, X, labels, ZA, blocks)
        print(tag, 'P1c', R[tag]['P1c']['omega_B_11'], R[tag]['P1c']['p_N1'], flush=True)
        R[tag]['babel'] = babel(model, X, labels)
        print(tag, 'babel', R[tag]['babel']['top1_correct'], flush=True)
        R[tag]['partd'] = partd(model, X, labels)
        if tag == 'secondary':
            prep = pl.Prepared(X, ZA, splits)
            obs, n1 = arm(prep, labels, 12, 'sec-N1', log=False)
            _, n1b = arm(prep, labels, 12, 'sec-N1b', blocks=blocks, seed=SEED + 1, log=False)
            padj, nrej = maxt_stepdown(np.median(obs['a'], axis=0), n1['a'], alpha=0.05)
            ri = corpora.KIDX[corpora.RECORD]
            p95 = np.percentile(n1['eta'], 95, axis=0)
            R[tag]['P1a'] = {'omega': obs['omega'], 'rank_B': obs['rank'],
                             'p_N1': pl.perm_p(obs['omega'][11], n1['omega'][11]),
                             'p_N1b': pl.perm_p(obs['omega'][11], n1b['omega'][11]),
                             'null_N1_median': float(np.median(n1['omega'][11])),
                             'R_kind': int(nrej)}
            R[tag]['P2neg'] = {'eta': obs['eta'].tolist(), 'A': obs['A'].tolist(),
                               'rho': obs['rho'].tolist(),
                               'eta_null_p95': p95.tolist(),
                               'base_exceed': int(sum(1 for i in range(12)
                                                      if i != ri and obs['eta'][i] > p95[i])),
                               'record_exceeds_p95': bool(obs['eta'][ri] > p95[ri]),
                               'record_rank_ascending': int(np.where(np.argsort(obs['eta']) == ri)[0][0]) + 1}
            print('secondary P1a', R[tag]['P1a'], flush=True)
    json.dump(R, open(os.path.join(OUT, 'extras.json'), 'w'), indent=1, default=str)
    print('elapsed', time.time() - t0)


if __name__ == '__main__':
    main()
