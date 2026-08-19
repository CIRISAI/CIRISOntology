"""S18 steps 3-8: the primary measurement.  Reads only the on-disk embedding cache."""
import json, os, sys, time, collections
import numpy as np
sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen')
import corpora, embed, pipeline as pl
from common import maxt_stepdown, kmeans

OUT = '/home/emoore/CIRISOntology/scratchpad/eigen/out'
PRIMARY = 'BAAI/bge-large-en-v1.5'
SECONDARY = 'Qwen/Qwen3-Embedding-0.6B'
NSPLIT, NPERM, SEED = 200, 500, 20260819
KS = pl.KS
R = {}

import atexit as _atexit, json as _json, os as _os
_atexit.register(lambda: _json.dump(
    R, open(_os.path.join('out', 'main_checkpoint.json'), 'w'), indent=1, default=str))


def E(texts, model):
    return embed.embed(texts, model, cap_usd=2.00, verbose=False).astype(np.float64)


def build(rows, model, field_pair=('before', 'after')):
    b = E([r[field_pair[0]] for r in rows], model)
    a = E([r[field_pair[1]] for r in rows], model)
    ub, ua = pl.unit(b), pl.unit(a)
    dun = ua - ub
    return {'before': ub, 'after': ua, 'delta_un': dun, 'delta': pl.unit(dun),
            'cos_ba': (ub * ua).sum(1)}


def keep_mask(rows, models=(PRIMARY, SECONDARY)):
    """DEVIATION (forced): an item whose un-normalised Delta is exactly zero -- the
    embedder returns bit-identical vectors for `before` and `after` -- cannot be unit
    normalised (S4's Delta is undefined).  Such items are dropped from the cloud, on
    the UNION over both embedders so every arm uses the same item set, and the count
    is reported.  Cause: instrument insensitivity to that edit, not a data defect."""
    ok = np.ones(len(rows), dtype=bool)
    for m in models:
        b = pl.unit(E([r['before'] for r in rows], m))
        a = pl.unit(E([r['after'] for r in rows], m))
        ok &= np.linalg.norm(a - b, axis=1) > 0
    return ok


def build_span(rows, model):
    b = E(['The text reads: ' + r['span_before'] for r in rows], model)
    a = E(['The text reads: ' + r['span_after'] for r in rows], model)
    ub, ua = pl.unit(b), pl.unit(a)
    d = ua - ub
    n = np.linalg.norm(d, axis=1, keepdims=True)
    zero = n[:, 0] < 1e-12
    if zero.any():
        # identical span embeddings (short/near-identical spans): keep as zero rows,
        # REPORT the count — silently normalizing 0/0 was the NaN that killed the arm
        print(f"  [span] {int(zero.sum())} zero-delta span rows kept as zeros", flush=True)
    n[zero] = 1.0
    return d / n


def dummies(vals, drop_first=True):
    u = sorted(set(vals))
    if drop_first:
        u = u[1:]
    return np.array([[1.0 if v == c else 0.0 for c in u] for v in vals])


def zmat_A(rows, use_part=True):
    sp = np.log10(1.0 + np.array([r['span_chars'] for r in rows]))
    cols = [np.ones(len(rows)), sp]
    cols += [dummies([r['domain'] for r in rows])[:, j]
             for j in range(dummies([r['domain'] for r in rows]).shape[1])]
    if use_part:
        d = dummies([r['part'] for r in rows])
        cols += [d[:, j] for j in range(d.shape[1])]
    return np.column_stack(cols)


def zmat_B(rows):
    sp = np.log10(1.0 + np.array([r['span_chars'] for r in rows]))
    d = dummies([r['stream'] for r in rows])
    return np.column_stack([np.ones(len(rows)), sp] + [d[:, j] for j in range(d.shape[1])])


def span_deciles(rows, seed=7):
    rng = np.random.default_rng(seed)
    v = np.array([r['span_chars'] for r in rows], dtype=float)
    o = np.lexsort((rng.random(len(v)), v))
    blk = np.zeros(len(v), dtype=int)
    for i, part in enumerate(np.array_split(o, 10)):
        blk[part] = i
    return blk


def nontax_partition(rows):
    """domain(5) x span-tercile(3) = 15 cells, collapsed to 12 by merging the three
    smallest (iteratively: smallest cell merged into the currently smallest other)."""
    v = np.array([r['span_chars'] for r in rows], dtype=float)
    q = np.quantile(v, [1 / 3, 2 / 3])
    ter = np.digitize(v, q)
    cell = [f'{r["domain"]}|{t}' for r, t in zip(rows, ter)]
    cnt = collections.Counter(cell)
    mapping = {c: c for c in cnt}
    while len(set(mapping.values())) > 12:
        agg = collections.Counter()
        for c, m in mapping.items():
            agg[m] += cnt[c]
        order = [k for k, _ in sorted(agg.items(), key=lambda x: x[1])]
        src, dst = order[0], order[1]
        for c, m in list(mapping.items()):
            if m == src:
                mapping[c] = dst
    lev = sorted(set(mapping.values()))
    li = {l: i for i, l in enumerate(lev)}
    return np.array([li[mapping[c]] for c in cell]), len(lev)


def paired_perm_p(diff, nperm=10000, seed=3):
    rng = np.random.default_rng(seed)
    obs = diff.mean()
    s = rng.choice([-1.0, 1.0], size=(nperm, len(diff)))
    null = (s * diff).mean(axis=1)
    return (1.0 + int((null >= obs).sum())) / (1.0 + nperm), float(obs)


def arm(prep, labels, K, tag, nperm=NPERM, blocks=None, want_eta=True, seed=SEED, log=True,
        drop=None):
    P = pl.onehot(labels, K)
    obs = pl.full_stats(prep, P, want_eta=want_eta, drop=drop)
    pm = pl.perm_labels(labels, nperm, seed, blocks=blocks)
    t0 = time.time()
    null = pl.run_null(prep, pm, K, want_eta=want_eta, log=tag if log else None, drop=drop)
    print(f'  [{tag}] null done in {time.time()-t0:.0f}s', flush=True)
    return obs, null


def main():
    t0 = time.time()
    A_all = corpora.corpus_A()
    keep = keep_mask(A_all)
    A = [r for r, k in zip(A_all, keep) if k]
    R['degenerate_items_dropped'] = [r['id'] for r, k in zip(A_all, keep) if not k]
    labels = np.array([corpora.KIDX[r['kind_target']] for r in A])
    strata = [(r['kind_target'], r['domain']) for r in A]
    splits = pl.make_splits(strata, NSPLIT, SEED)
    ZA = zmat_A(A)
    blocks = span_deciles(A)
    R['n_A'] = len(A)
    R['split_class_min'] = int(min(np.bincount(labels[splits[s]], minlength=12).min()
                                   for s in range(NSPLIT)))
    R['split_class_sizes_example'] = np.bincount(labels[splits[0]], minlength=12).tolist()

    cl = build(A, PRIMARY)
    X = cl['delta']
    # ---- V1 / V1b : per-class embedding degeneracy
    v1 = {}
    for k, kn in enumerate(corpora.KINDS):
        m = labels == k
        v1[kn] = {'median_cos_ba': float(np.median(cl['cos_ba'][m])),
                  'median_norm_delta_un': float(np.median(np.linalg.norm(cl['delta_un'][m], axis=1)))}
    drop = np.array([v1[kn]['median_cos_ba'] > 0.999 or v1[kn]['median_norm_delta_un'] < 1e-3
                     for kn in corpora.KINDS])
    R['V1'] = {'per_class': v1, 'unmeasured': [corpora.KINDS[i] for i in np.where(drop)[0]],
               'global_median_cos': float(np.median(cl['cos_ba'])),
               'fired': bool(drop.any())}
    R['V3'] = {'min_class_n_in_any_half': R['split_class_min'],
               'fired': R['split_class_min'] < 9}

    prep = pl.Prepared(X, ZA, splits)
    prep_raw = pl.Prepared(X, ZA, splits, residualize=False)
    R['rank_B'] = None

    # ================= P1a primary (residualized incl. batch) =================
    print('P1a primary...', flush=True)
    obs, n1 = arm(prep, labels, 12, 'N1', drop=drop)
    _, n1b = arm(prep, labels, 12, 'N1b', blocks=blocks, seed=SEED + 1, drop=drop)
    R['rank_B'] = obs['rank']
    R['P1a'] = {
        'omega': obs['omega'],
        'omega11_ci': [float(np.percentile(obs['omega_splits'][11], 2.5)),
                       float(np.percentile(obs['omega_splits'][11], 97.5))],
        'p_N1': pl.perm_p(obs['omega'][11], n1['omega'][11]),
        'p_N1b': pl.perm_p(obs['omega'][11], n1b['omega'][11]),
        'null_N1_median': float(np.median(n1['omega'][11])),
        'null_N1b_median': float(np.median(n1b['omega'][11])),
        'null_N1_p99': float(np.percentile(n1['omega'][11], 99)),
        'rank_B': obs['rank'],
        'p_N1_by_k': {k: pl.perm_p(obs['omega'][k], n1['omega'][k]) for k in obs['omega']},
    }
    # R_kind via maxT step-down on the N1 null
    padj, nrej = maxt_stepdown(np.median(obs['a'], axis=0), n1['a'], alpha=0.05)
    padj_b, nrej_b = maxt_stepdown(np.median(obs['a'], axis=0), n1b['a'], alpha=0.05)
    R['P1b'] = {'R_kind_N1': int(nrej), 'R_kind_N1b': int(nrej_b),
                'a_obs': np.median(obs['a'], axis=0).tolist(),
                'a_null_median': np.median(n1['a'], axis=0).tolist(),
                'padj': padj.tolist()}
    # Omega by span decile (S7 N1b requirement)
    # descriptive (in-sample, so labelled): mean kind-subspace loading of an item's
    # Delta, per changed-span decile.  25 items per decile makes a per-decile split-half
    # Omega undefined; N1b is the inferential span control.
    bA0 = np.linalg.lstsq(ZA, X, rcond=None)[0]
    Xr0 = X - ZA @ bA0
    P0 = pl.onehot(labels, 12)
    C0, _ = None, None
    cnt0 = P0.sum(0)
    S0 = P0.T @ Xr0
    tot0 = Xr0.sum(0)
    C0 = S0 / cnt0[:, None] - (tot0[None, :] - S0) / (len(A) - cnt0)[:, None]
    Q0 = np.linalg.svd(C0.T, full_matrices=False)[0][:, :11]
    load = ((pl.unit(Xr0) @ Q0) ** 2).sum(1)
    R['P1a']['span_decile_descriptive'] = {}
    for dcl in range(10):
        m = blocks == dcl
        R['P1a']['span_decile_descriptive'][str(dcl)] = {
            'n': int(m.sum()),
            'median_span_chars': float(np.median([A[i]['span_chars'] for i in np.where(m)[0]])),
            'mean_kind_subspace_loading': float(load[m].mean())}
    R['P1a']['evr_top11'] = float(np.median(prep.evr[:, :11].sum(axis=1)))

    # ---- N4 comparators
    print('N4 comparators...', flush=True)
    Psd = np.zeros((prep.nsd, len(A), 12))
    for sd in range(prep.nsd):
        F = np.where(prep.Hf[sd] > 0)[0]
        Xr = X - ZA @ prep.betas[sd]
        lab = kmeans(Xr[F], 12, seed=1000 + sd)
        Psd[sd, F, lab] = 1.0
    Ck, cntk = pl.contrasts_batch_persd(prep, Psd, 'F')
    omk, _, rk = pl.omega_a_batch(Ck, prep.U)
    nt_lab, nt_lev = nontax_partition(A)
    Cn, _ = pl.contrasts_batch(prep, pl.onehot(nt_lab, nt_lev), 'F')
    omn, _, rn = pl.omega_a_batch(Cn, prep.U)
    om_tax = obs['omega_splits'][11]
    om_km = pl.split_reduce(omk[11])
    om_nt = pl.split_reduce(omn[11])
    p_nt, d_nt = paired_perm_p(om_tax - om_nt)
    R['N4'] = {'omega_taxonomy': float(np.median(om_tax)),
               'omega_kmeans': float(np.median(om_km)),
               'omega_nontaxonomy': float(np.median(om_nt)),
               'nontax_levels': int(nt_lev),
               'rank_kmeans': float(np.median(rk)), 'rank_nontax': float(np.median(rn)),
               'gap_kmeans_minus_tax': float(np.median(om_km - om_tax)),
               'p_tax_gt_nontax': p_nt, 'mean_diff_tax_minus_nontax': d_nt,
               'frac_splits_tax_gt_nontax': float((om_tax > om_nt).mean())}

    # ================= P2-neg : LOKO eta table =================
    print('P2-neg...', flush=True)
    eta_null = n1['eta']
    R['P2neg'] = {'kinds': corpora.KINDS, 'eta': obs['eta'].tolist(),
                  'A': obs['A'].tolist(), 'rho': obs['rho'].tolist(),
                  'eta_null_p95': np.percentile(eta_null, 95, axis=0).tolist(),
                  'eta_null_p99': np.percentile(eta_null, 99, axis=0).tolist(),
                  'A_null_median': np.median(n1['A'], axis=0).tolist()}
    ri = corpora.KIDX[corpora.RECORD]
    exceed95 = [i for i in range(12) if obs['eta'][i] > R['P2neg']['eta_null_p95'][i]]
    base_exceed = [i for i in exceed95 if i != ri]
    order = np.argsort(obs['eta'])
    R['P2neg']['base_kinds_exceeding_p95'] = len(base_exceed)
    R['P2neg']['record_exceeds_p95'] = bool(obs['eta'][ri] > R['P2neg']['eta_null_p95'][ri])
    R['P2neg']['record_exceeds_p99'] = bool(obs['eta'][ri] > R['P2neg']['eta_null_p99'][ri])
    R['P2neg']['record_rank_ascending'] = int(np.where(order == ri)[0][0]) + 1
    R['P2neg']['rho_record'] = float(obs['rho'][ri])
    R['P2neg']['A_record'] = float(obs['A'][ri])
    R['P2neg']['A_median_base'] = float(np.median([obs['A'][i] for i in range(12) if i != ri]))
    R['V5'] = {'base_kinds_detectable': len(base_exceed), 'fired': len(base_exceed) < 6}

    # LOKO-exclusion sensitivity: U_11 refit on the held-out half with kind k removed
    lo = np.zeros((prep.nsd, 12))
    CF, _ = pl.contrasts_batch(prep, pl.onehot(labels, 12), 'F')
    for sd in range(prep.nsd):
        Ftr = prep.Hf[sd] > 0
        Ecl = ~Ftr
        Xr = X - ZA @ prep.betas[sd]
        for k in range(12):
            m = Ecl & (labels != k)
            Xe = Xr[m]
            Xe = Xe - Xe.mean(0)
            U = np.linalg.svd(Xe, full_matrices=False)[2][:11].T
            g = CF[sd, k] / np.linalg.norm(CF[sd, k])
            lo[sd, k] = float(((g @ U) ** 2).sum())
    R['P2neg']['A_loko_excluded'] = np.median(pl.split_reduce(lo), axis=0).tolist()

    # ---- AUC table (LOO, full 1024-d, residualized-on-all arm; raw reported too)
    print('AUC...', flush=True)
    bA = np.linalg.lstsq(ZA, X, rcond=None)[0]
    Xres_all = X - ZA @ bA
    for nm, XX in (('residualized', Xres_all), ('raw', X)):
        sc = pl.loo_auc_scores(XX, labels, 12)
        tab = {}
        for k, kn in enumerate(corpora.KINDS):
            y = (labels == k).astype(int)
            a = pl.auc(y, sc[:, k])
            lo_, hi_ = pl.auc_boot(y, sc[:, k], 2000, seed=100 + k)
            tab[kn] = {'auc': float(a), 'ci95': [lo_, hi_]}
        R[f'AUC_{nm}'] = tab
    R['V5b'] = {'auc_record_ci_upper': R['AUC_residualized']['testimonial']['ci95'][1],
                'fired': R['AUC_residualized']['testimonial']['ci95'][1] < 0.70}

    # ================= Placebo P1 (K1c) =================
    print('Placebo P1 (before-cloud)...', flush=True)
    Xb = cl['before']
    prep_b = pl.Prepared(Xb, ZA, splits)
    obs_b = pl.full_stats(prep_b, pl.onehot(labels, 12), want_eta=False)
    d = obs['omega_splits'][11] - obs_b['omega_splits'][11]
    rng = np.random.default_rng(11)
    sgn = rng.choice([-1.0, 1.0], size=(NPERM, NSPLIT))
    nullmed = np.median(sgn * d[None, :], axis=1)
    R['K1c'] = {'omega_delta': float(np.median(obs['omega_splits'][11])),
                'omega_before': float(np.median(obs_b['omega_splits'][11])),
                'median_diff': float(np.median(d)),
                'p_paired': float((1 + (nullmed >= np.median(d)).sum()) / (1 + NPERM)),
                'frac_splits_delta_gt_before': float((d > 0).mean())}

    # ================= P1a-batch (V11) =================
    print('P1a-batch...', flush=True)
    R['P1a_batch'] = {}
    for part in ('a', 'b'):
        idx = [i for i, r in enumerate(A) if r['part'] == part]
        rows = [A[i] for i in idx]
        lab_p = np.array([corpora.KIDX[r['kind_target']] for r in rows])
        u = sorted(set(lab_p.tolist()))
        remap = {v: i for i, v in enumerate(u)}
        lab_p = np.array([remap[v] for v in lab_p])
        st = [(r['kind_target'], r['domain']) for r in rows]
        sp = pl.make_splits(st, NSPLIT, SEED + 77)
        Zp = zmat_A(rows, use_part=False)
        pr = pl.Prepared(X[idx], Zp, sp)
        o, nn = arm(pr, lab_p, len(u), f'N1-part{part}', log=False)
        R['P1a_batch'][part] = {'n': len(idx), 'n_classes': len(u),
                                'omega11': o['omega'][11], 'rank_B': o['rank'],
                                'p_N1': pl.perm_p(o['omega'][11], nn['omega'][11]),
                                'null_median': float(np.median(nn['omega'][11]))}
    fa = R['P1a_batch']['a']['p_N1'] >= 0.01
    fb = R['P1a_batch']['b']['p_N1'] >= 0.01
    R['V11'] = {'both_within_batch_fail': bool(fa and fb)}

    # ================= secondary arms =================
    print('secondary arms...', flush=True)
    R['arms'] = {}
    # raw (non-residualized)
    o, nn = arm(prep_raw, labels, 12, 'raw', log=False)
    R['arms']['raw_delta'] = {'omega11': o['omega'][11], 'p_N1': pl.perm_p(o['omega'][11], nn['omega'][11]),
                              'eta': o['eta'].tolist(), 'rank_B': o['rank']}
    # un-normalized delta (sensitivity, no null)
    pr_un = pl.Prepared(cl['delta_un'], ZA, splits)
    o_un = pl.full_stats(pr_un, pl.onehot(labels, 12), want_eta=False)
    R['arms']['unnormalized_delta'] = {'omega11': o_un['omega'][11], 'rank_B': o_un['rank']}
    # span-only arm
    Xs = build_span(A, PRIMARY)
    pr_s = pl.Prepared(Xs, ZA, splits)
    o_s, nn_s = arm(pr_s, labels, 12, 'span', log=False)
    R['arms']['span_only'] = {'omega11': o_s['omega'][11],
                              'p_N1': pl.perm_p(o_s['omega'][11], nn_s['omega'][11]),
                              'rank_B': o_s['rank']}
    # panel-modal label arm
    J = corpora.judgments()
    aids = {r['id'] for r in A}
    votes = collections.defaultdict(list)
    inv = {v: k for k, v in corpora.PLAIN.items()}
    offvocab = 0
    for j in J:
        if j['id'] in aids and j['condition'] == 'BASE':
            k = j.get('kind')
            if k in inv:
                votes[j['id']].append(inv[k])
            else:
                offvocab += 1
    keep, plab = [], []
    for i, r in enumerate(A):
        v = votes.get(r['id'], [])
        if len(v) < 2:
            continue
        c = collections.Counter(v).most_common()
        if len(c) > 1 and c[0][1] == c[1][1]:
            continue
        keep.append(i)
        plab.append(corpora.KIDX[c[0][0]])
    keep = np.array(keep)
    plab = np.array(plab)
    R['arms']['panel_modal'] = {'n_items': len(keep), 'offvocab_votes_BASE': offvocab,
                                'class_counts': np.bincount(plab, minlength=12).tolist()}
    if len(keep) > 50 and np.bincount(plab, minlength=12).min() >= 3:
        strat2 = [(int(plab[i]), A[keep[i]]['domain']) for i in range(len(keep))]
        sp2 = pl.make_splits(strat2, NSPLIT, SEED + 5)
        pr2 = pl.Prepared(X[keep], zmat_A([A[i] for i in keep]), sp2)
        o2, nn2 = arm(pr2, plab, 12, 'panel', log=False)
        R['arms']['panel_modal'].update({'omega11': o2['omega'][11], 'rank_B': o2['rank'],
                                         'p_N1': pl.perm_p(o2['omega'][11], nn2['omega'][11]),
                                         'eta': o2['eta'].tolist()})
    else:
        R['arms']['panel_modal']['note'] = 'class support too thin for the split-half arm'

    json.dump(R, open(os.path.join(OUT, 'main_primary.json'), 'w'), indent=1, default=str)
    print('elapsed', time.time() - t0, flush=True)


if __name__ == '__main__':
    main()
