"""EIGEN2 main analysis — one CONFIG per process, checkpointed, resumable.

Usage:  python analysis.py <config>
        config in {primary, witness, ablation, raw, spandom, clearonly}

Every statistic follows EIGEN2_PREREG.md verbatim:
  * S4   x_i = normalize(e(C1_i)); placebo x'_i = normalize(e(C1P_i)); nuisance Z fit on
         the FITTING half and applied to the held-out half; `res` is PRIMARY.
  * S5.1 11 one-vs-rest centroid contrasts span exactly 10 dims -> rank(B) = 10.
  * S6   Omega(k) = (1/r)||U_k^T B||_F^2 ; Omega* = Omega(11) - median(N1 null) ;
         delta = median over splits of the per-split (Omega_C1 - Omega_C1P) ;
         psi = delta / Omega* (guarded, S13) ; a_j = ||B^T u_j||^2 ; maxT step-down.
  * S7   N1 free label permutation (GOVERNING), N1b span-decile-stratified (required
         conjunct), N1c batch-stratified and N1d difficulty-stratified (reported).
         N_perm = 500; p = (1 + #{null >= obs})/(1 + 500); exceedance counts reported.
  * S7.1 rivals: domain-11 (report merged into bulletin) and k-means-11.
  * S7.2 200 Euler-circuit splits, exact +-1 on kind AND batch, halves 237/237.
  * S7.3 paired comparisons: sign-flip for direction (NOT evidence on its own) and the
         500-permutation floor as the GOVERNING p.  AMENDMENTS.md A3 declares that for
         the rival comparisons the same item permutation pi_b is applied to BOTH label
         vectors.
"""
import json, os, sys, time

import numpy as np

sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen2run')
sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen')
import e2lib as L
import pipeline as pl
from common import maxt_stepdown, kmeans

KS = [5, 7, 9, 10, 11, 13, 15, 20, 30, 40]
JMAX = 40
NPERM = int(os.environ.get('E2_NPERM', L.NPERM))     # smoke-test override only
NSPLIT = int(os.environ.get('E2_NSPLIT', L.NSPLIT))

CONFIGS = {
    # name        arm             nuisance  clear_only  nulls
    'primary':   ('qwen',         'full',   False, ['N1', 'N1b', 'N1c', 'N1d']),
    'witness':   ('bge',          'full',   False, ['N1', 'N1b']),
    'ablation':  ('qwen_noinstr', 'full',   False, ['N1', 'N1b']),
    'raw':       ('qwen',         'none',   False, ['N1', 'N1b']),
    'spandom':   ('qwen',         'spandom', False, ['N1', 'N1b']),
    'clearonly': ('qwen',         'full',   True,  ['N1', 'N1b']),
    # AMENDMENTS.md A6, post-freeze: the frozen Z with only the domain dummies removed,
    # so that P1a's rival conjunct / K1b / K1d are evaluable rather than annihilated.
    'rivalnodom': ('qwen',        'nodom',  False, ['N1', 'N1b']),
}


def unit(V):
    n = np.linalg.norm(V, axis=1, keepdims=True)
    return V / np.where(n > 0, n, 1.0)


def reduce_dim(X, tol=1e-10):
    u, s, vt = np.linalg.svd(X, full_matrices=False)
    keep = s > s.max() * tol
    return X @ vt[keep].T, int(keep.sum())


def perm_indices(n, nperm, seed, blocks=None):
    """(nperm, n) index permutations; stratified within `blocks` when given."""
    rng = np.random.default_rng(seed)
    out = np.zeros((nperm, n), dtype=np.int64)
    base = np.arange(n)
    if blocks is None:
        for b in range(nperm):
            out[b] = rng.permutation(base)
    else:
        ub = np.unique(blocks)
        idx = {u: np.where(blocks == u)[0] for u in ub}
        for b in range(nperm):
            p = base.copy()
            for u in ub:
                i = idx[u]
                p[i] = i[rng.permutation(len(i))]
            out[b] = p
    return out


def stats(prep, labs, K, want_eta=False):
    return pl.full_stats(prep, pl.onehot(labs, K), ks=KS, want_eta=want_eta)


def signflip(d, nperm=10000, seed=11):
    rng = np.random.default_rng(seed)
    sgn = rng.choice([-1.0, 1.0], size=(nperm, len(d)))
    nullmed = np.median(sgn * d[None, :], axis=1)
    med = float(np.median(d))
    return {'median_diff': med,
            'p_signflip': float((1 + int((nullmed >= med).sum())) / (1 + nperm)),
            'frac_splits_gt': float((d > 0).mean())}


def perm_p(obs, null):
    null = np.asarray(null)
    exc = int((null >= obs).sum())
    return float((1.0 + exc) / (1.0 + len(null))), exc


def deciles(x):
    q = np.quantile(x, np.linspace(0, 1, 11)[1:-1])
    return np.searchsorted(q, x, side='right')


def main(cfg_name):
    t0 = time.time()
    arm, nuis, clear_only, nulls = CONFIGS[cfg_name]
    out_path = os.path.join(L.OUT, f'analysis_{cfg_name}.json')
    ck_path = os.path.join(L.OUT, f'analysis_{cfg_name}.ckpt.npz')

    rows_all = L.load_e2()
    meta = json.load(open(os.path.join(L.OUT, 'embed_meta.json')))
    dropped = set(meta['V7']['dropped_ids'])
    keep_idx = [i for i, r in enumerate(rows_all) if r['id'] not in dropped]
    if clear_only:
        keep_idx = [i for i in keep_idx if rows_all[i]['difficulty'] == 'clear']
    rows = [rows_all[i] for i in keep_idx]
    n = len(rows)

    XC = np.load(os.path.join(L.CACHE, f'X_{arm}_C1.npy')).astype(np.float64)[keep_idx]
    XP = np.load(os.path.join(L.CACHE, f'X_{arm}_C1P.npy')).astype(np.float64)[keep_idx]

    labels = L.labels_of(rows)
    batches = L.batches_of(rows)
    dom11, dom_names = L.domain11_of(rows)
    span = np.array([r['ctx_chars'] for r in rows], dtype=float)
    diff = np.array([1 if r['difficulty'] == 'hard' else 0 for r in rows])
    Z = L.nuisance_Z(rows, nuis if nuis != 'none' else 'none')
    resid = nuis != 'none'
    splits = L.make_splits(labels, batches, NSPLIT, L.SEED)

    R = {'config': cfg_name, 'arm': arm, 'nuisance': nuis, 'clear_only': clear_only,
         'n': n, 'z_cols': int(Z.shape[1]), 'residualize': resid,
         'nsplit': NSPLIT, 'nperm': NPERM, 'ks': KS,
         'ts': time.strftime('%Y-%m-%dT%H:%M:%S'),
         'split_check': dict(zip(['max_kind_imb', 'max_batch_imb', 'n1', 'n2'],
                                 [int(x) for x in L.split_violations(splits[0], labels,
                                                                     batches)]))}

    Xc, d1 = reduce_dim(unit(XC))
    Xp, d2 = reduce_dim(unit(XP))
    R['d_eff'] = [d1, d2]
    prepC = pl.Prepared(Xc, Z, splits, residualize=resid)
    prepP = pl.Prepared(Xp, Z, splits, residualize=resid)
    R['evr_top11'] = {'C1': float(np.median(prepC.evr[:, :11].sum(1))),
                      'C1P': float(np.median(prepP.evr[:, :11].sum(1)))}
    R['evr_ratio_C1_over_C1P'] = R['evr_top11']['C1'] / R['evr_top11']['C1P']
    print(f'[{cfg_name}] prepared n={n} d_eff={d1}/{d2} '
          f'[{time.time()-t0:.0f}s]', flush=True)

    # ---------------- observed ------------------------------------------------
    obsC = stats(prepC, labels, L.NK, want_eta=True)
    obsP = stats(prepP, labels, L.NK, want_eta=True)
    obsCd = stats(prepC, dom11, L.NK)
    obsPd = stats(prepP, dom11, L.NK)
    R['rank_B'] = {'tax': obsC['rank'], 'dom11': obsCd['rank']}
    R['omega_obs'] = {'C1_tax': obsC['omega'], 'C1P_tax': obsP['omega'],
                      'C1_dom11': obsCd['omega'], 'C1P_dom11': obsPd['omega']}
    gap_splits = {k: obsC['omega_splits'][k] - obsP['omega_splits'][k] for k in (10, 11)}
    gapd_splits = {k: obsCd['omega_splits'][k] - obsPd['omega_splits'][k] for k in (10, 11)}
    R['delta_obs'] = {str(k): {'median_of_diffs': float(np.median(gap_splits[k])),
                               'diff_of_medians': obsC['omega'][k] - obsP['omega'][k],
                               **signflip(gap_splits[k])} for k in (10, 11)}
    R['delta_dom11'] = {str(k): {'median_of_diffs': float(np.median(gapd_splits[k])),
                                 'diff_of_medians': obsCd['omega'][k] - obsPd['omega'][k]}
                        for k in (10, 11)}
    R['loko'] = {'kinds': L.KINDS, 'A': obsC['A'].tolist(), 'rho': obsC['rho'].tolist(),
                 'eta': obsC['eta'].tolist()}
    R['a_obs'] = np.median(obsC['a'], axis=0).tolist()

    # ---------------- k-means-11 rival ---------------------------------------
    km_om, km_drop = [], 0
    Psd = np.zeros((prepC.nsd, n, L.NK))
    for sd in range(prepC.nsd):
        F = prepC.Hf[sd] > 0
        lab = kmeans(Xc[F], L.NK, seed=L.SEED + sd)
        if len(np.unique(lab)) < L.NK:
            km_drop += 1
        full = np.zeros(n, dtype=np.int64)
        full[np.where(F)[0]] = lab
        Psd[sd] = pl.onehot(full, L.NK)
    Ckm, cntkm = pl.contrasts_batch_persd(prepC, Psd, 'F')
    omkm, _, rkm = pl.omega_a_batch(Ckm, prepC.U, KS)
    R['kmeans11'] = {'omega': {str(k): float(np.median(pl.split_reduce(v)))
                               for k, v in omkm.items()},
                     'rank_B_median': float(np.median(rkm)),
                     'splits_dropped': km_drop, 'frac_dropped': km_drop / prepC.nsd,
                     'rank_matched': bool(km_drop / prepC.nsd <= 0.10)}
    R['kmeans_minus_taxonomy'] = {str(k): R['kmeans11']['omega'][str(k)] - obsC['omega'][k]
                                  for k in (10, 11)}
    print(f'[{cfg_name}] observed Om11(C1)={obsC["omega"][11]:.5f} '
          f'C1P={obsP["omega"][11]:.5f} dom={obsCd["omega"][11]:.5f} '
          f'km={R["kmeans11"]["omega"]["11"]:.5f} [{time.time()-t0:.0f}s]', flush=True)
    L.atomic_json(R, out_path)

    # ---------------- nulls ---------------------------------------------------
    blockmap = {'N1': None, 'N1b': deciles(span), 'N1c': batches, 'N1d': diff}
    store = {}
    if os.path.exists(ck_path):
        z = np.load(ck_path, allow_pickle=True)
        store = {k: z[k] for k in z.files}
        print(f'[{cfg_name}] RESUME: {sorted(store)}', flush=True)

    for nm in nulls:
        key = f'{nm}_omC'
        if key in store and store[key].shape[0] >= NPERM:
            continue
        P = perm_indices(n, NPERM, L.SEED + 1000 + hash(nm) % 997, blockmap[nm])
        need_full = (nm == 'N1')
        omC = np.zeros((NPERM, len(KS)))
        omP = np.zeros((NPERM, len(KS)))
        omCd = np.zeros((NPERM, len(KS)))
        omPd = np.zeros((NPERM, len(KS)))
        aN = np.zeros((NPERM, JMAX))
        etaN = np.zeros((NPERM, L.NK))
        want_eta = (nm == 'N1' and cfg_name == 'primary')
        for b in range(NPERM):
            lp = labels[P[b]]
            sC = stats(prepC, lp, L.NK, want_eta=want_eta)
            omC[b] = [sC['omega'][k] for k in KS]
            aN[b] = np.median(sC['a'], axis=0)
            if want_eta:
                etaN[b] = sC['eta']
            sP = stats(prepP, lp, L.NK)
            omP[b] = [sP['omega'][k] for k in KS]
            if need_full:
                dp = dom11[P[b]]
                omCd[b] = [stats(prepC, dp, L.NK)['omega'][k] for k in KS]
                omPd[b] = [stats(prepP, dp, L.NK)['omega'][k] for k in KS]
            if (b + 1) % 50 == 0:
                snap = dict(store)
                snap.update({f'{nm}_omC': omC[:b + 1], f'{nm}_omP': omP[:b + 1],
                             f'{nm}_omCd': omCd[:b + 1], f'{nm}_omPd': omPd[:b + 1],
                             f'{nm}_a': aN[:b + 1], f'{nm}_eta': etaN[:b + 1]})
                np.savez(ck_path, **snap)
                print(f'[{cfg_name}] {nm} {b+1}/{NPERM} [{time.time()-t0:.0f}s]', flush=True)
        store[f'{nm}_omC'] = omC
        store[f'{nm}_omP'] = omP
        store[f'{nm}_omCd'] = omCd
        store[f'{nm}_omPd'] = omPd
        store[f'{nm}_a'] = aN
        store[f'{nm}_eta'] = etaN
        np.savez(ck_path, **store)

    # ---------------- assemble ------------------------------------------------
    ki = {k: i for i, k in enumerate(KS)}
    res = {}
    for nm in nulls:
        omC, omP = store[f'{nm}_omC'], store[f'{nm}_omP']
        e = {}
        for k in (10, 11):
            j = ki[k]
            p, exc = perm_p(obsC['omega'][k], omC[:, j])
            pp, excp = perm_p(obsP['omega'][k], omP[:, j])
            e[str(k)] = {
                'null_median': float(np.median(omC[:, j])),
                'null_p99': float(np.percentile(omC[:, j], 99)),
                'excess': obsC['omega'][k] - float(np.median(omC[:, j])),
                'p_N': p, 'exceedances': exc,
                'placebo_null_median': float(np.median(omP[:, j])),
                'placebo_excess': obsP['omega'][k] - float(np.median(omP[:, j])),
                'placebo_p_N': pp, 'placebo_exceedances': excp,
            }
            gnull = omC[:, j] - omP[:, j]
            gobs = R['delta_obs'][str(k)]['diff_of_medians']
            pg, excg = perm_p(gobs, gnull)
            e[str(k)]['gap_null_median'] = float(np.median(gnull))
            e[str(k)]['gap_null_p99'] = float(np.percentile(gnull, 99))
            e[str(k)]['p_gap'] = pg
            e[str(k)]['gap_exceedances'] = excg
        res[nm] = e
    R['nulls'] = res

    # rival comparisons (S7.3 + AMENDMENTS A3), on the N1 permutations
    omC, omP = store['N1_omC'], store['N1_omP']
    omCd, omPd = store['N1_omCd'], store['N1_omPd']
    riv = {}
    for k in (10, 11):
        j = ki[k]
        dobs = obsC['omega'][k] - obsCd['omega'][k]
        dnull = omC[:, j] - omCd[:, j]
        p, exc = perm_p(dobs, dnull)
        gobs = (R['delta_obs'][str(k)]['median_of_diffs']
                - R['delta_dom11'][str(k)]['median_of_diffs'])
        gnull = (omC[:, j] - omP[:, j]) - (omCd[:, j] - omPd[:, j])
        pg, excg = perm_p(gobs, gnull)
        sf = signflip(obsC['omega_splits'][k] - obsCd['omega_splits'][k])
        sfd = signflip(gap_splits[k] - gapd_splits[k])
        riv[str(k)] = {
            'omega_tax_minus_dom11': dobs, 'p_perm_paired': p, 'exceedances': exc,
            'p_N1_taxonomy_alone': res['N1'][str(k)]['p_N'],
            'signflip_omega': sf,
            'delta_tax_minus_dom11': gobs, 'p_perm_paired_delta': pg,
            'delta_exceedances': excg, 'signflip_delta': sfd,
            'dom11_excess': obsCd['omega'][k] - float(np.median(omCd[:, j])),
        }
    R['rival_domain11'] = riv

    # maxT -> R_kind, and the a_j shortfall
    aobs = np.median(obsC['a'], axis=0)
    padj, nrej = maxt_stepdown(aobs, store['N1_a'])
    R['R_kind'] = int(nrej)
    R['a_padj'] = padj.tolist()
    R['a_sum_le40'] = float(aobs.sum())
    R['a_shortfall_r_minus_sum'] = float(obsC['rank'] - aobs.sum())

    # V5 (LOKO vacuity, reporting only) — primary only, where the eta null exists
    if store.get('N1_eta') is not None and store['N1_eta'].any():
        p95 = np.percentile(store['N1_eta'], 95, axis=0)
        R['loko']['eta_null_p95'] = p95.tolist()
        R['loko']['n_kinds_above_p95'] = int((np.array(obsC['eta']) > p95).sum())
        R['V5_fired'] = bool(R['loko']['n_kinds_above_p95'] < 6)

    # ---------------- VG1, psi, verdict --------------------------------------
    j11 = ki[11]
    dmed = R['delta_obs']['11']['median_of_diffs']
    gnull11 = omC[:, j11] - omP[:, j11]
    p99 = float(np.percentile(gnull11, 99))
    pgap, excgap = perm_p(dmed, gnull11)          # gate A on the median-of-diffs
    pgap_dm, excgap_dm = perm_p(R['delta_obs']['11']['diff_of_medians'], gnull11)
    margin = max(0.010, p99)
    R['VG1'] = {
        'gateA_p_gap_N1': pgap, 'gateA_exceedances': excgap,
        'gateA_p_gap_on_diff_of_medians': pgap_dm,
        'gateA_pass': bool(pgap <= 0.01),
        'gap_null_p99': p99, 'margin_used': margin,
        'gateB_delta_median': dmed, 'gateB_pass': bool(dmed >= margin),
        'descriptor_delta_gt_0': bool(dmed > 0),
        'descriptor_p_paired': R['delta_obs']['11']['p_signflip'],
        'descriptor_frac_splits_gt': R['delta_obs']['11']['frac_splits_gt'],
        'VALID': bool(pgap <= 0.01 and dmed >= margin),
    }
    if not R['VG1']['VALID']:
        if dmed < 0:
            sf = signflip(-gap_splits[11])
            R['VG1']['sublabel'] = ('placebo strictly above'
                                    if sf['p_signflip'] <= 0.05 else 'gap not resolved')
            R['VG1']['reverse_signflip_p'] = sf['p_signflip']
        else:
            R['VG1']['sublabel'] = 'gap not resolved'

    om_star = {str(k): res['N1'][str(k)]['excess'] for k in (10, 11)}
    R['omega_star'] = om_star
    p99w = {str(k): res['N1'][str(k)]['null_p99'] - res['N1'][str(k)]['null_median']
            for k in (10, 11)}
    R['psi'] = {}
    for k in (10, 11):
        s = om_star[str(k)]
        w = p99w[str(k)]
        d = R['delta_obs'][str(k)]['median_of_diffs']
        if s > w:
            rng = np.random.default_rng(7)
            nb = 10000
            idx = rng.integers(0, NSPLIT, (nb, NSPLIT))
            nm_ = float(np.median(store['N1_omC'][:, ki[k]]))
            bd = np.median(gap_splits[k][idx], axis=1)
            bo = np.median(obsC['omega_splits'][k][idx], axis=1) - nm_
            bp = bd / np.where(np.abs(bo) > 1e-12, bo, np.nan)
            lo_b, hi_b = (float(np.nanpercentile(bp, 2.5)),
                          float(np.nanpercentile(bp, 97.5)))
            pn = (omC[:, ki[k]] - omP[:, ki[k]]) / np.where(
                np.abs(omC[:, ki[k]] - nm_) > 1e-12, omC[:, ki[k]] - nm_, np.nan)
            q = np.nanpercentile(pn, [2.5, 50, 97.5])
            lo_p, hi_p = float(d / s - (q[2] - q[1])), float(d / s - (q[0] - q[1]))
            R['psi'][str(k)] = {
                'value': d / s, 'defined': True,
                'ci_bootstrap': [lo_b, hi_b], 'ci_perm_width': [lo_p, hi_p],
                'ci_wider': [min(lo_b, lo_p), max(hi_b, hi_p)],
                'null_p99_width': w}
        else:
            R['psi'][str(k)] = {'defined': False, 'null_p99_width': w,
                                'note': 'psi UNDEFINED (Omega* below the null p99 width)'}

    # verdict cells
    def p1a(k):
        c = {'N1': res['N1'][str(k)]['p_N'] < 0.01,
             'N1b': res.get('N1b', {}).get(str(k), {}).get('p_N', 1.0) < 0.01,
             'rival_dom11': riv[str(k)]['p_perm_paired'] < 0.01
             and riv[str(k)]['omega_tax_minus_dom11'] > 0}
        return c, all(c.values())

    c11, ok11 = p1a(11)
    c10, ok10 = p1a(10)
    R['P1a'] = {'conjuncts_k11': c11, 'conjuncts_k10': c10,
                'DETECTED': bool(ok11 and ok10),
                'k_dependent': bool(ok11 and not ok10)}
    s11 = om_star['11']
    R['P1a']['strength'] = ('STRONG' if s11 >= 0.190 else
                            ('MODERATE' if s11 >= 0.020 else 'WEAK'))
    R['P1d'] = {'VG1_valid': R['VG1']['VALID'],
                'delta_privilege': bool(riv['11']['p_perm_paired_delta'] < 0.01
                                        and riv['11']['delta_tax_minus_dom11'] > 0),
                'PASS': bool(R['VG1']['VALID']
                             and riv['11']['p_perm_paired_delta'] < 0.01
                             and riv['11']['delta_tax_minus_dom11'] > 0)}
    if not R['VG1']['VALID']:
        cell = 'VOID-AS-INSTRUMENT'
        if (res['N1']['11']['placebo_p_N'] < 0.01
                and res.get('N1b', {}).get('11', {}).get('placebo_p_N', 1.0) < 0.01):
            cell = 'VOID-AS-INSTRUMENT (also KIND-IS-IN-THE-CONTEXT)'
    elif R['P1d']['PASS'] and R['P1a']['DETECTED']:
        cell = 'CHANGE-CARRIED ALIGNMENT'
    elif R['P1d']['PASS'] and not R['P1a']['DETECTED']:
        cell = 'CHANGE-READ, TAXONOMY-NULL'
    elif not R['P1d']['PASS'] and R['P1a']['DETECTED']:
        cell = 'CONTEXT-PRIVILEGED'
    else:
        cell = 'CHANGE-READ, NOTHING-PRIVILEGED'
    R['VERDICT_CELL'] = cell

    # S9.5 forward bands (primary statistic only)
    R['forward'] = {
        'omega_star_11': s11,
        'band': ('B (<0.03)' if s11 < 0.03 else
                 ('middle (0.03-0.15)' if s11 < 0.15 else
                  ('A (0.15-0.28)' if s11 <= 0.28 else 'A missed high (>0.28)'))),
        'delta_secondary': {'value': dmed, 'band': [0.020, 0.065],
                            'hit': bool(0.020 <= dmed <= 0.065)},
        'psi_secondary': ({'value': R['psi']['11']['value'], 'band': [0.15, 0.40],
                           'hit': bool(0.15 <= R['psi']['11']['value'] <= 0.40)}
                          if R['psi']['11']['defined'] else {'value': None,
                                                             'hit': None,
                                                             'note': 'psi UNDEFINED'}),
        'omega_star_C1P_secondary': {
            'value': res['N1']['11']['placebo_excess'], 'band': [0.12, 0.25],
            'hit': bool(0.12 <= res['N1']['11']['placebo_excess'] <= 0.25)},
    }
    # S10 P3 (EXPLORATORY)
    R['P3'] = {'omega_C1P_11': obsP['omega'][11],
               'p_N1': res['N1']['11']['placebo_p_N'],
               'p_N1b': res.get('N1b', {}).get('11', {}).get('placebo_p_N'),
               'beats_domain_rival': None}
    dobsP = obsP['omega'][11] - obsPd['omega'][11]
    dnullP = omP[:, j11] - omPd[:, j11]
    pP, excP = perm_p(dobsP, dnullP)
    R['P3']['omega_C1P_tax_minus_dom11'] = dobsP
    R['P3']['p_perm_paired'] = pP
    R['P3']['exceedances'] = excP
    R['P3']['beats_domain_rival'] = bool(pP < 0.01 and dobsP > 0)
    R['P3']['PASS'] = bool(R['P3']['p_N1'] < 0.01
                           and (R['P3']['p_N1b'] or 1.0) < 0.01
                           and R['P3']['beats_domain_rival'])

    R['seconds'] = time.time() - t0
    L.atomic_json(R, out_path)
    L.done_marker(f'ANALYSIS.{cfg_name}', {'artifact': out_path,
                                           'cell': cell, 'omega_star': s11,
                                           'seconds': R['seconds']})
    print(f'[{cfg_name}] DONE cell={cell} Om*={s11:.5f} delta={dmed:.5f} '
          f'[{time.time()-t0:.0f}s]', flush=True)


if __name__ == '__main__':
    main(sys.argv[1])
